"""Domain/adapter checks: no genuine provider is contacted by this suite."""
import asyncio
from itertools import product
import json
from pathlib import Path
import subprocess
from uuid import uuid4
import httpx
import pytest
from app.config import Settings
from app.domain import allowed_references, match_exercise, render_fragments
from app.explanations import ModelService
from app.repository import Repository
from app.schemas import ExplanationRequest, Snapshot


def test_every_answer_combination_and_direct_choice_matches_existing_vue_policy():
    combinations = [{"answers": list(a), "direct_choice": choice}
                    for a in product((None, 0, 1, 2), repeat=5)
                    for choice in (None, "breathing", "grounding")]
    root = Path(__file__).resolve().parents[2]
    script = "import { matchExercise } from './frontend/src/matching.js'; let s=''; for await (const c of process.stdin) s+=c; process.stdout.write(JSON.stringify(JSON.parse(s).map(x=>matchExercise(x.answers,x.direct_choice))));"
    completed = subprocess.run(["node", "--input-type=module", "-e", script],
                               input=json.dumps(combinations), cwd=root, text=True,
                               capture_output=True, check=True)
    assert json.loads(completed.stdout) == [match_exercise(item["answers"], item["direct_choice"]) for item in combinations]


def test_grammar_is_bounded_and_contextual_across_all_answer_combinations():
    for answers in product((None, 0, 1, 2), repeat=5):
        snapshot = {"answers": list(answers), "answered": [True] * 5}
        result = match_exercise(answers)
        fragments = {"reason_code": result["code"], "opening_id": "notice", "reference_ids": allowed_references(snapshot, result)[:2], "closing_id": "change"}
        text = render_fragments(fragments, snapshot, result)
        assert len(text) <= 240
        for reference in fragments["reference_ids"]:
            assert answers[["body", "thought", "present", "breathing", "grounding"].index(reference)] is not None


@pytest.mark.parametrize("change", [
    {"reason_code": "grounding-comfort"}, {"opening_id": "diagnose"},
    {"closing_id": "exercise-instruction"}, {"reference_ids": ["thought"]},
    {"reference_ids": []}, {"reference_ids": ["body", "body"]},
    {"unapproved_text": "Provider prose must never display"},
])
def test_model_cannot_extend_the_enforced_construction_grammar(change):
    snapshot = {"answers": [2, 0, 0, 0, 0], "answered": [True] * 5}
    fragments = {"reason_code": "body-cue", "opening_id": "reflect", "reference_ids": ["body", "breathing"], "closing_id": "choice"}
    fragments.update(change)
    with pytest.raises(ValueError):
        render_fragments(fragments, snapshot, match_exercise(snapshot["answers"]))


def free_settings(tmp_path, **changes):
    value = dict(db_path=str(tmp_path / "guard.sqlite3"), model_mode="openrouter",
                 model_id="nvidia/nemotron-3.5-lightning:free", api_key="test-only-placeholder",
                 approved_budget_usd=0, budget_approved=True, pricing_verified=True,
                 input_price_per_million=0, output_price_per_million=0,
                 live_max_attempts=3)
    value.update(changes)
    return Settings(**value)


def test_free_authorization_fails_closed_for_paid_model_changed_price_or_missing_approval(tmp_path):
    assert free_settings(tmp_path).live_configured
    for change in ({"model_id": "paid-model"}, {"approved_budget_usd": 1},
                   {"pricing_verified": False}, {"budget_approved": False},
                   {"input_price_per_million": 0.1}, {"api_key": ""}):
        assert not free_settings(tmp_path, **change).live_configured


def test_persisted_outbound_cap_survives_restart_and_clear_history(tmp_path):
    settings = free_settings(tmp_path)
    repository = Repository(settings.db_path)
    repository.initialize()
    assert [repository.reserve_live_attempt(settings) for _ in range(4)] == [True, True, True, False]
    repository.clear()
    restarted = Repository(settings.db_path)
    restarted.initialize()
    assert not restarted.reserve_live_attempt(settings)
    with restarted.connection() as db:
        assert tuple(db.execute("SELECT attempts,reserved_usd FROM live_budget").fetchone()) == (3, 0)


def test_openrouter_adapter_passes_real_turn_context_and_zero_price_constraints_without_network(tmp_path, monkeypatch):
    settings = free_settings(tmp_path)
    repository = Repository(settings.db_path)
    repository.initialize()
    captured = []
    fragments = {"reason_code": "body-cue", "opening_id": "notice", "reference_ids": ["body"], "closing_id": "change"}

    class FakeClient:
        def __init__(self, **kwargs):
            assert kwargs["follow_redirects"] is False

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def post(self, url, json, headers):
            captured.append((url, json))
            # The fixture credential is intentionally not retained or printed.
            return httpx.Response(200, request=httpx.Request("POST", url),
                                  json={"model": settings.model_id, "choices": [{"message": {"content": __import__("json").dumps(fragments)}}]})

    monkeypatch.setattr("app.explanations.httpx.AsyncClient", FakeClient)
    snapshot = {"answers": [2, 0, 0, 0, 0], "answered": [True] * 5,
                "exercise": "breathing", "direct_choice": None}
    actual, model_id = asyncio.run(ModelService(settings, repository).provider_fragments(snapshot, match_exercise(snapshot["answers"])))
    assert actual == fragments and model_id == settings.model_id
    assert len(captured) == 1
    url, body = captured[0]
    assert url == "https://openrouter.ai/api/v1/chat/completions"
    assert body["provider"] == {"require_parameters": True, "allow_fallbacks": False, "max_price": {"prompt": 0, "completion": 0}}
    assert body["model"] == settings.model_id
    assert "response_format" not in body
    assert '"additionalProperties":false' in body["messages"][0]["content"]
    assert '"enum":["body-cue"]' in body["messages"][0]["content"]
    assert "no Markdown fences" in body["messages"][0]["content"]
    assert body["max_tokens"] == 1000
    assert [m["content"] for m in body["messages"] if m["role"] == "user"] == ["Hard right now", "Easy", "Present", "Comfortable", "Comfortable"]


@pytest.mark.parametrize("category,expected", [
    ("http", "fallback-provider-http-429-code-429"),
    ("network", "fallback-provider-ConnectError"),
])
def test_provider_diagnostics_retain_only_safe_status_or_class(tmp_path, monkeypatch, category, expected):
    settings = Settings(db_path=str(tmp_path / "diagnostics.sqlite3"), model_mode="mock")
    repository = Repository(settings.db_path)
    repository.initialize()
    session_id = str(uuid4())
    repository.save(session_id, Snapshot(operation_id=uuid4(), revision=1,
                                        answers=[2, 0, 0, 0, 0], answered=[True] * 5,
                                        exercise="breathing", status="ready"))
    service = ModelService(settings, repository)

    async def fail(*args):
        request = httpx.Request("POST", "https://provider.invalid", headers={"Authorization": "Bearer fixture-private-token"})
        if category == "network":
            raise httpx.ConnectError("fixture-private-error-description", request=request)
        response = httpx.Response(429, request=request, json={"error": {"code": 429, "message": "fixture-private-provider-prose"}})
        response.raise_for_status()

    monkeypatch.setattr(service, "provider_fragments", fail)
    response = asyncio.run(service.explain(session_id, ExplanationRequest(revision=1, request_id=uuid4())))
    assert response["status"] == "fallback"
    saved = repository.get(session_id)
    assert saved["explanations"][0]["validation"] == expected
    assert "fixture-private" not in json.dumps(saved)
