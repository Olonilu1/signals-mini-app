"""Serves the Mini App dashboard and the signals API."""
import json
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
WEBAPP = ROOT / "webapp"
API_TOKEN = os.environ.get("API_TOKEN", "")

app = FastAPI(title="Signals Mini App")


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(WEBAPP / "index.html")


@app.get("/api/signals")
async def get_signals() -> JSONResponse:
    return JSONResponse(json.loads((DATA / "signals.json").read_text()))


@app.post("/api/signals")
async def add_signals(request: Request) -> dict:
    if API_TOKEN and request.headers.get("X-API-Token") != API_TOKEN:
        raise HTTPException(status_code=401, detail="bad token")
    body = await request.json()
    if isinstance(body, dict):
        body = [body]
    path = DATA / "signals.json"
    current = json.loads(path.read_text())
    known = {(s["symbol"], s["candle_open"]) for s in current}
    added = [s for s in body if (s["symbol"], s["candle_open"]) not in known]
    current.extend(added)
    path.write_text(json.dumps(current, indent=2))
    return {"added": len(added)}
