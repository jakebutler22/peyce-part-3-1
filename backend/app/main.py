"""Thin localhost API. It serves no clinical/support service or accounts."""
from contextlib import asynccontextmanager
import sqlite3
from uuid import UUID
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
from .config import Settings
from .domain import POLICY_VERSION, QUESTION_VERSION
from .explanations import ModelService
from .repository import Conflict, Missing, Repository
from .schemas import ExplanationRequest, InterruptRequest, Snapshot


def create_app(settings=None):
    config = settings or Settings()
    repository = Repository(config.db_path)
    model_service = ModelService(config, repository)

    @asynccontextmanager
    async def lifespan(app):
        repository.initialize()
        yield

    api = FastAPI(title="Peyce local fictional coursework", version="0.2.0", lifespan=lifespan)
    api.state.settings = config
    api.state.repository = repository
    api.state.model_service = model_service

    @api.exception_handler(Conflict)
    async def conflict_handler(request, error):
        return JSONResponse(status_code=409, content={"detail": str(error)})

    @api.exception_handler(Missing)
    async def missing_handler(request, error):
        return JSONResponse(status_code=404, content={"detail": str(error)})

    @api.exception_handler(sqlite3.Error)
    async def database_handler(request, error):
        return JSONResponse(status_code=503, content={"detail": "Local fictional history is unavailable. Your local exercise and support remain available."})

    def fault_control(value):
        if value and not config.test_controls:
            raise HTTPException(400, "Test controls are disabled")
        if value not in (None, "database", "timeout", "invalid", "late", "provider"):
            raise HTTPException(400, "Unknown test fault")
        if value == "database":
            raise sqlite3.OperationalError("injected database failure")
        return value

    @api.get("/api/status")
    def status():
        mode, model_id = model_service.identity()
        with repository.connection() as db:
            attempts = db.execute("SELECT attempts FROM live_budget WHERE id=1").fetchone()[0]
        return dict(mode=mode, model_id=model_id, live_configured=config.live_configured,
                    test_controls=config.test_controls, question_version=QUESTION_VERSION,
                    policy_version=POLICY_VERSION, live_attempts=attempts, live_max_attempts=config.live_max_attempts)

    @api.put("/api/sessions/{session_id}/snapshot")
    def snapshot(session_id: UUID, snapshot: Snapshot, x_peyce_test_fault: str | None = Header(default=None)):
        fault_control(x_peyce_test_fault)
        return repository.save(str(session_id), snapshot)

    @api.post("/api/sessions/{session_id}/explanation")
    async def explanation(session_id: UUID, body: ExplanationRequest, x_peyce_test_fault: str | None = Header(default=None)):
        fault = fault_control(x_peyce_test_fault)
        return await model_service.explain(str(session_id), body, fault)

    @api.get("/api/sessions")
    def sessions(x_peyce_test_fault: str | None = Header(default=None)):
        fault_control(x_peyce_test_fault)
        return {"sessions": repository.list()}

    @api.get("/api/sessions/{session_id}")
    def session(session_id: UUID, x_peyce_test_fault: str | None = Header(default=None)):
        fault_control(x_peyce_test_fault)
        return repository.get(str(session_id))

    @api.delete("/api/sessions")
    def delete_sessions(x_peyce_test_fault: str | None = Header(default=None)):
        fault_control(x_peyce_test_fault)
        return repository.clear()

    @api.post("/api/sessions/{session_id}/interrupt")
    def interrupt(session_id: UUID, body: InterruptRequest, x_peyce_test_fault: str | None = Header(default=None)):
        fault_control(x_peyce_test_fault)
        return repository.interrupt(str(session_id), body)

    return api


app = create_app()
