"""Controlled historical/current S17 reproduction. No local credential or database access."""
import importlib
import json
import os
from pathlib import Path
import socket
import sqlite3
import sys
import types
from uuid import uuid4

source, db_path, commit, label = sys.argv[1:]
# The extracted source has no .env. Prevent dotenv reading any file regardless.
dotenv = types.ModuleType("dotenv")
dotenv.load_dotenv = lambda *args, **kwargs: False
sys.modules["dotenv"] = dotenv
os.environ["PEYCE_DB_PATH"] = db_path
os.environ["PEYCE_MODEL_MODE"] = "mock"
os.environ["PYTHON_DOTENV_DISABLED"] = "1"
sys.path.insert(0, source)
from fastapi.testclient import TestClient
from app.config import Settings
from app.main import create_app
import app.explanations as adapter

network_attempts = []
def denied_connect(*args, **kwargs):
    network_attempts.append("socket-blocked")
    raise RuntimeError("Network forbidden in controlled reproduction")
socket.socket.connect = denied_connect
class DeniedAsyncClient:
    def __init__(self, *args, **kwargs):
        network_attempts.append("provider-transport-blocked")
        raise RuntimeError("Provider transport forbidden in controlled reproduction")
adapter.httpx.AsyncClient = DeniedAsyncClient

settings = Settings(db_path=db_path, model_mode="openrouter",
                    model_id="nvidia/nemotron-3.5-lightning:free",
                    api_key="fictional-placeholder-not-a-credential",
                    approved_budget_usd=0, budget_approved=True,
                    live_max_attempts=10, input_price_per_million=0,
                    output_price_per_million=0, pricing_verified=True,
                    model_timeout_seconds=0.2, test_controls=False)
uid = lambda: str(uuid4())
session_id, request_id = uid(), uid()
snapshot = {"operation_id": uid(), "revision": 1,
            "answers": [2, 0, 0, 0, 0], "answered": [True] * 5,
            "direct_choice": None, "exercise": "breathing", "status": "ready",
            "color": "pink", "color_explicit": False,
            "events": [{"id": uid(), "kind": "instruction_visible", "at_ms": 10000,
                        "active_ms": 0, "cause": "user"}], "timing": None}
with TestClient(create_app(settings)) as client:
    with sqlite3.connect(db_path) as db:
        db.execute("UPDATE live_budget SET attempts=10 WHERE id=1")
    saved = client.put(f"/api/sessions/{session_id}/snapshot", json=snapshot)
    if saved.status_code != 200:
        raise RuntimeError("Fixture save failed")
    request = {"revision": 1, "request_id": request_id}
    response = client.post(f"/api/sessions/{session_id}/explanation", json=request)
    replay = client.post(f"/api/sessions/{session_id}/explanation", json=request)
    body = response.json()
    with sqlite3.connect(db_path) as db:
        db.row_factory = sqlite3.Row
        ledger = dict(db.execute("SELECT attempts,reserved_usd FROM live_budget WHERE id=1").fetchone())
        receipt = dict(db.execute("SELECT mode,model_id,outcome,validation FROM explanations WHERE request_id=?", (request_id,)).fetchone())
        turns = [dict(row) for row in db.execute("SELECT role,source FROM turns WHERE session_id=? AND role='assistant' AND sequence=99", (session_id,))]
        count = db.execute("SELECT COUNT(*) FROM explanations WHERE session_id=?", (session_id,)).fetchone()[0]
    clear = client.delete("/api/sessions")
    with sqlite3.connect(db_path) as db:
        attempts_after_clear = db.execute("SELECT attempts FROM live_budget WHERE id=1").fetchone()[0]

checks = {"http_200": response.status_code == 200,
          "mode_is_mock": body.get("mode") == "mock",
          "status_is_validated": body.get("status") == "validated",
          "persisted_mode_is_mock": receipt["mode"] == "mock",
          "persisted_mock_source": any(t["source"] == "validated-mock-acknowledgment" for t in turns),
          "zero_network_dispatch": len(network_attempts) == 0,
          "replay_same_receipt": body == replay.json() and count == 1,
          "ledger_still_ten_after_clear": ledger["attempts"] == attempts_after_clear == 10}
print(json.dumps({"label": label, "source_commit": commit,
                  "scope": "controlled S17 archive reproduction; disposable SQLite; fictional input; no live provider",
                  "input": {"answers": snapshot["answers"], "status": "ready", "fixture_attempts": 10},
                  "predeclared_expected": {"mode": "mock", "status": "validated", "persisted_source": "validated-mock-acknowledgment", "attempts": 10, "network_dispatches": 0},
                  "http_status": response.status_code,
                  "response": {key: body.get(key) for key in ("mode", "status", "model_id", "text", "fragments", "stale")},
                  "sql": {"live_budget": ledger, "explanation": receipt, "assistant_turns": turns,
                          "explanation_rows": count, "attempts_after_clear": attempts_after_clear},
                  "checks": checks, "result": "PASS" if all(checks.values()) else "FAIL (expected for historical BEFORE)",
                  "network_attempts": len(network_attempts), "real_runtime_accessed": False,
                  "dotenv_disabled": True, "credential": "fictional placeholder only"}, indent=2))
