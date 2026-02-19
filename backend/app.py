import json
import os
from urllib.request import Request, urlopen
from urllib.error import URLError

from flask import Flask, render_template, send_from_directory, request, jsonify

# ML API (run with: cd backend && uvicorn api:app --reload)
ML_API_BASE = os.environ.get("ML_API_BASE", "http://127.0.0.1:8000")

frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
frontend_static_dir = os.path.join(frontend_dir, "static")
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
    """Proxy to ML API: bulk predict priority + category for task texts."""
    try:
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
