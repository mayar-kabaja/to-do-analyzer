import os
from flask import Flask, render_template

template_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
app = Flask(__name__, template_folder=template_dir)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "", 200


if __name__ == '__main__':
    # Bind to 0.0.0.0 so the server is reachable on all interfaces (e.g. Render, mobile on same network)
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 7001)))
