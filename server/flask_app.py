"""Flask (WSGI) twin of server/app.py for hosts without ASGI (e.g. PythonAnywhere)."""
import json
import os
from pathlib import Path

from flask import Flask, abort, jsonify, request, send_from_directory

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
WEBAPP = ROOT / "webapp"
API_TOKEN = os.environ.get("API_TOKEN", "")

app = Flask(__name__, static_folder=None)


@app.get("/")
def index():
    return send_from_directory(WEBAPP, "index.html")


@app.get("/api/signals")
def get_signals():
    return jsonify(json.loads((DATA / "signals.json").read_text()))


@app.post("/api/signals")
def add_signals():
    if API_TOKEN and request.headers.get("X-API-Token") != API_TOKEN:
        abort(401)
    body = request.get_json(force=True)
    if isinstance(body, dict):
        body = [body]
    path = DATA / "signals.json"
    current = json.loads(path.read_text())
    known = {(s["symbol"], s["candle_open"]) for s in current}
    added = [s for s in body if (s["symbol"], s["candle_open"]) not in known]
    current.extend(added)
    path.write_text(json.dumps(current, indent=2))
    return jsonify({"added": len(added)})
