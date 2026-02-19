import json
import os
from urllib.request import Request, urlopen
from urllib.error import URLError

from flask import Flask, render_template, send_from_directory, request, jsonify

# On Render (single service): set USE_INPROCESS_ML=true so Flask loads models and serves predict.
# Locally: run uvicorn api:app (port 8000) and leave unset to proxy.
ML_API_BASE = os.environ.get("ML_API_BASE", "http://127.0.0.1:8000")
USE_INPROCESS_ML = os.environ.get("USE_INPROCESS_ML", "").lower() in ("1", "true", "yes")

# Optional: load models in-process (for Render single-service deploy)
_vectorizer = _priority_model = _category_model = None
if USE_INPROCESS_ML:
    try:
        import pickle
        _backend_dir = os.path.dirname(os.path.abspath(__file__))
        _models_dir = os.path.join(_backend_dir, "models")
        with open(os.path.join(_models_dir, "vectorizer.pkl"), "rb") as f:
            _vectorizer = pickle.load(f)
        with open(os.path.join(_models_dir, "priority_model.pkl"), "rb") as f:
            _priority_model = pickle.load(f)
        with open(os.path.join(_models_dir, "category_model.pkl"), "rb") as f:
            _category_model = pickle.load(f)
    except Exception:
        _vectorizer = _priority_model = _category_model = None

# Resolve frontend path relative to this file so it works from any CWD (e.g. Render: start from repo root)
_backend_dir = os.path.dirname(os.path.abspath(__file__))
_repo_root = os.path.abspath(os.path.join(_backend_dir, ".."))
frontend_dir = os.path.join(_repo_root, "frontend")
frontend_static_dir = os.path.join(frontend_dir, "static")
if not os.path.isdir(frontend_dir):
    import sys
    print(f"[WARN] frontend_dir not found: {frontend_dir} (backend_dir={_backend_dir})", file=sys.stderr)
app = Flask(
    __name__,
    template_folder=frontend_dir,
    static_folder=frontend_static_dir,
    static_url_path="/static",
)


@app.route("/")
def index():
    base = request.url_root.rstrip("/")
    return render_template(
        "index.html",
        og_image_url=f"{base}/static/og-image.png",
        og_url=request.url,
    )


@app.route("/style.css")
def style():
    return send_from_directory(frontend_dir, "style.css")


@app.route("/app.js")
def app_js():
    return send_from_directory(frontend_dir, "app.js")


@app.route("/favicon.ico")
def favicon_ico():
    """Many browsers request /favicon.ico by default; serve our icon."""
    return send_from_directory(frontend_static_dir, "favicon.jpg", mimetype="image/jpeg")


@app.route("/health")
def health():
    return "", 200


@app.route("/api/predict_bulk", methods=["POST"])
def api_predict_bulk():
    """Predict priority + category (in-process or proxy to ML API)."""
    try:
        data = request.get_json(force=True, silent=True) or {}
        texts = data.get("texts") or []
        if not texts:
            return jsonify({"results": []}), 200

        if _vectorizer is not None and _priority_model is not None and _category_model is not None:
            # In-process (e.g. Render single service)
            X_vec = _vectorizer.transform(texts)
            priorities = _priority_model.predict(X_vec)
            categories = _category_model.predict(X_vec)
            results = [
                {"text": t, "priority": p, "category": c}
                for t, p, c in zip(texts, priorities, categories)
            ]
            return jsonify({"results": results}), 200

        # Proxy to external ML API (local dev)
        body = request.get_data()
        req = Request(
            f"{ML_API_BASE}/predict_bulk",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(req, timeout=30) as resp:
            return jsonify(json.load(resp)), 200
    except URLError as e:
        return jsonify({"error": "ML service unavailable", "detail": str(e)}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Bind to 0.0.0.0 so the server is reachable on all interfaces (e.g. Render, mobile on same network)
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 7001)))
