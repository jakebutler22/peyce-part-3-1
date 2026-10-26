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


def tool_message(fragments):
    return {"content": None, "tool_calls": [{"id": "fixture-call", "type": "function",
            "function": {"name": "acknowledge_current_rule", "arguments": json.dumps(fragments)}}]}


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
                                  json={"model": settings.model_id, "choices": [{"message": tool_message(fragments)}]})

    monkeypatch.setattr("app.explanations.httpx.AsyncClient", FakeClient)
    snapshot = {"answers": [2, 0, 0, 0, 0], "answered": [True] * 5,
                "exercise": "breathing", "direct_choice": None}
    actual, model_id, diagnostic = asyncio.run(ModelService(settings, repository).provider_fragments(snapshot, match_exercise(snapshot["answers"])))
    assert actual == fragments and model_id == settings.model_id
    assert diagnostic == {"http_status": 200}
    assert len(captured) == 1
    url, body = captured[0]
    assert url == "https://openrouter.ai/api/v1/chat/completions"
    assert body["provider"] == {"require_parameters": True, "allow_fallbacks": False, "max_price": {"prompt": 0, "completion": 0}}
    assert body["model"] == settings.model_id
    assert "response_format" not in body
    assert len(body["tools"]) == 1
    assert body["tools"][0]["type"] == "function"
    function = body["tools"][0]["function"]
    assert function["name"] == "acknowledge_current_rule"
    assert function["parameters"]["additionalProperties"] is False
    assert function["parameters"]["properties"]["reason_code"]["enum"] == ["body-cue"]
    assert function["parameters"]["required"] == ["reason_code", "opening_id", "reference_ids", "closing_id"]
    assert body["tool_choice"] == {"type": "function", "function": {"name": "acknowledge_current_rule"}}
    assert "no Markdown fences" in body["messages"][0]["content"]
    assert body["max_tokens"] == 1000
    assert body["reasoning"] == {"enabled": False, "exclude": True}
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


@pytest.mark.parametrize("case,expected_stage", [
    ("response-size", "response-size"),
    ("response-json", "response-json"),
    ("response-envelope", "response-envelope"),
    ("missing-model", "model-identity"),
    ("unapproved-model", "model-identity"),
    ("missing-calls", "tool-calls"),
    ("extra-calls", "tool-calls"),
    ("non-function-call", "tool-envelope"),
    ("wrong-function", "tool-name"),
    ("missing-arguments", "tool-arguments-missing"),
    ("large-arguments", "tool-arguments-size"),
    ("arguments-json", "tool-arguments-json"),
    ("truncated-json", "tool-arguments-truncated"),
    ("duplicate-arguments", "tool-arguments-json"),
    ("non-json-constant", "tool-arguments-json"),
    ("unexpected-prose", "unexpected-prose"),
    ("old-content-only", "unexpected-prose"),
    ("fragment-schema", "fragment-schema"),
    ("unsupported-reference", "fragment-schema"),
])
def test_invalid_live_shaped_responses_have_safe_stage_diagnostics_without_network(tmp_path, monkeypatch, case, expected_stage):
    settings = free_settings(tmp_path)
    repository = Repository(settings.db_path)
    repository.initialize()
    session_id = str(uuid4())
    repository.save(session_id, Snapshot(operation_id=uuid4(), revision=1,
                                        answers=[2, 0, 0, 0, 0], answered=[True] * 5,
                                        exercise="breathing", status="ready"))
    private_marker = "fixture-private-provider-material"
    fragments = {"reason_code": "body-cue", "opening_id": "notice", "reference_ids": ["body"], "closing_id": "change"}
    message = tool_message(fragments)
    message["reasoning"] = private_marker
    function = message["tool_calls"][0]["function"]
    body = {"model": settings.model_id,
            "choices": [{"finish_reason": "tool_calls", "message": message}],
            "usage": {"completion_tokens": 1000, "completion_tokens_details": {"reasoning_tokens": 950}, "private": private_marker},
            "private": private_marker}
    raw = None
    if case == "response-size":
        raw = (private_marker + "x" * 16001).encode()
    elif case == "response-json":
        raw = private_marker.encode()
    elif case == "response-envelope":
        body["choices"] = {"private": private_marker}
    elif case == "missing-model":
        body.pop("model")
    elif case == "unapproved-model":
        body["model"] = private_marker
    elif case == "missing-calls":
        message.pop("tool_calls")
    elif case == "extra-calls":
        message["tool_calls"].append(dict(message["tool_calls"][0], id="fixture-second-call"))
    elif case == "non-function-call":
        message["tool_calls"][0]["type"] = private_marker
    elif case == "wrong-function":
        function["name"] = private_marker
    elif case == "missing-arguments":
        function["arguments"] = None
    elif case == "large-arguments":
        function["arguments"] = private_marker + "x" * 2001
    elif case == "arguments-json":
        function["arguments"] = private_marker
    elif case == "truncated-json":
        body["choices"][0]["finish_reason"] = "length"
        function["arguments"] = '{"reason_code":'
    elif case == "duplicate-arguments":
        function["arguments"] = '{"reason_code":"' + private_marker + '",' + json.dumps(fragments)[1:]
    elif case == "non-json-constant":
        function["arguments"] = '{"reason_code":NaN}'
    elif case == "unexpected-prose":
        message["content"] = private_marker
    elif case == "old-content-only":
        message.pop("tool_calls")
        message["content"] = json.dumps(fragments)
    elif case == "fragment-schema":
        function["arguments"] = json.dumps(dict(fragments, private=private_marker))
    elif case == "unsupported-reference":
        function["arguments"] = json.dumps(dict(fragments, reference_ids=[private_marker]))

    calls = []

    class FakeClient:
        def __init__(self, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def post(self, url, **kwargs):
            calls.append(1)
            request = httpx.Request("POST", url, headers={"Authorization": "Bearer " + private_marker})
            options = {"content": raw} if raw is not None else {"json": body}
            return httpx.Response(200, request=request, headers={"X-Private": private_marker}, **options)

    monkeypatch.setattr("app.explanations.httpx.AsyncClient", FakeClient)
    response = asyncio.run(ModelService(settings, repository).explain(session_id, ExplanationRequest(revision=1, request_id=uuid4())))
    assert len(calls) == 1
    assert response["status"] == "fallback"
    assert response["fragments"] is None
    assert response["diagnostic"]["invalid_stage"] == expected_stage
    assert response["diagnostic"]["http_status"] == 200
    if case.startswith("truncated-"):
        assert response["diagnostic"]["finish_reason"] == "length"
        assert response["diagnostic"]["completion_tokens"] == 1000
        assert response["diagnostic"]["reasoning_tokens"] == 950
    with repository.connection() as db:
        row = db.execute("SELECT validation,response_json FROM explanations").fetchone()
        assert row["validation"] == "fallback-invalid"
        receipt = json.loads(row["response_json"])
        assert receipt["diagnostic"] == response["diagnostic"]
        assert private_marker not in row["response_json"]
    assert private_marker not in json.dumps(repository.get(session_id))


def test_diagnostic_allowlist_omits_provider_strings_and_unbounded_or_boolean_counts():
    from app.explanations import response_diagnostic, safe_diagnostic
    private_marker = "fixture-private-provider-material"
    diagnostic = response_diagnostic({
        "choices": [{"finish_reason": private_marker}],
        "usage": {"completion_tokens": True, "completion_tokens_details": {"reasoning_tokens": 1000001}},
    }, 200)
    assert diagnostic == {"http_status": 200, "finish_reason": "other"}
    assert safe_diagnostic({"invalid_stage": private_marker, "finish_reason": private_marker,
                            "http_status": 999, "completion_tokens": -1, "reasoning_tokens": 1.5,
                            "model": private_marker, "reasoning": private_marker}) == {}


def test_valid_response_diagnostics_do_not_change_the_approved_model_contribution(tmp_path, monkeypatch):
    settings = free_settings(tmp_path)
    repository = Repository(settings.db_path)
    repository.initialize()
    session_id = str(uuid4())
    repository.save(session_id, Snapshot(operation_id=uuid4(), revision=1,
                                        answers=[2, 0, 0, 0, 0], answered=[True] * 5,
                                        exercise="breathing", status="ready"))
    fragments = {"reason_code": "body-cue", "opening_id": "notice", "reference_ids": ["body"], "closing_id": "change"}

    class FakeClient:
        def __init__(self, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def post(self, url, **kwargs):
            return httpx.Response(200, request=httpx.Request("POST", url), json={
                "model": settings.model_id.removesuffix(":free"),
                "choices": [{"finish_reason": "tool_calls", "message": tool_message(fragments)}],
                "usage": {"completion_tokens": 44, "completion_tokens_details": {"reasoning_tokens": 0}},
            })

    monkeypatch.setattr("app.explanations.httpx.AsyncClient", FakeClient)
    response = asyncio.run(ModelService(settings, repository).explain(session_id, ExplanationRequest(revision=1, request_id=uuid4())))
    assert response["status"] == "validated"
    assert response["fragments"] == fragments
    assert response["diagnostic"] == {"http_status": 200, "finish_reason": "tool_calls", "completion_tokens": 44, "reasoning_tokens": 0}
    saved = repository.get(session_id)
    assert saved["exercise"] == "breathing" and saved["result"]["code"] == "body-cue"
    assert saved["explanations"][0]["prompt_version"] == "peyce-acknowledgment-1.1"
