"""HTTP-to-SQLite regression checks using fictional, disposable sessions only.

These exercise the integrated application boundary. They never read the local
demonstration database and never select a live model mode.
"""

from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
import time
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from app.schemas import ExplanationRequest


def uid():
    return str(uuid4())


def event(kind, at_ms, active_ms=0, cause="user"):
    return {"id": uid(), "kind": kind, "at_ms": at_ms,
            "active_ms": active_ms, "cause": cause}


def snapshot(revision=1, **changes):
    value = {
        "operation_id": uid(), "revision": revision,
        "answers": [2, 0, 0, 0, 0], "answered": [True] * 5,
        "direct_choice": None, "exercise": "breathing", "status": "ready",
        "color": "pink", "color_explicit": False,
        "events": [event("instruction_visible", 10000)], "timing": None,
    }
    value.update(changes)
    return value


@pytest.fixture
def settings(tmp_path):
    return Settings(db_path=str(tmp_path / "integration.sqlite3"),
                    test_controls=True, model_mode="mock",
                    model_timeout_seconds=0.08, test_late_seconds=0.2)


@pytest.fixture
def client(settings):
    with TestClient(create_app(settings)) as value:
        yield value


def save(client, session_id, value, **kwargs):
    return client.put(f"/api/sessions/{session_id}/snapshot", json=value, **kwargs)


def detail(client, session_id):
    response = client.get(f"/api/sessions/{session_id}")
    assert response.status_code == 200, response.text
    return response.json()


def finish_flow(client, session_id):
    value = snapshot()
    assert save(client, session_id, value).status_code == 200
    events = value["events"] + [event("start", 12000)]
    assert save(client, session_id, snapshot(2, events=events, status="active")).status_code == 200
    events += [event("complete", 72000, 60000, "clock")]
    assert save(client, session_id, snapshot(3, events=events, status="completed")).status_code == 200
    events += [event("finish", 76000, 60000)]
    timing = {"raw_ms": 66000, "counted_ms": 66000, "excluded_ms": 0,
              "excluded_intervals": [], "instruction_ms": 10000,
              "finish_ms": 76000, "entry_ms": 10000}
    final = snapshot(4, events=events, status="finished", timing=timing)
    response = save(client, session_id, final)
    assert response.status_code == 200, response.text
    return final


def test_complete_session_survives_app_restart_and_has_single_lifecycle(client, settings):
    session_id = uid()
    final = finish_flow(client, session_id)
    replay = save(client, session_id, final)
    assert replay.status_code == 200
    before = detail(client, session_id)
    assert before["status"] == "finished"
    assert len(before["turns"]) >= 10
    assert sum(item["kind"] == "complete" for item in before["lifecycle"]) == 1
    assert sum(item["kind"] == "finish" for item in before["lifecycle"]) == 1
    with TestClient(create_app(settings)) as restarted:
        after = detail(restarted, session_id)
        assert after["status"] == "finished"
        assert after["timing"]["counted_ms"] == 66000
        listed = restarted.get("/api/sessions").json()["sessions"]
        assert any(item["id"] == session_id and item["status"] == "finished" for item in listed)


def test_revisions_and_operation_replay_cannot_replace_newer_answers(client):
    session_id = uid()
    first = snapshot()
    assert save(client, session_id, first).status_code == 200
    newer = snapshot(3, answers=[0, 2, 2, 0, 0], exercise="grounding")
    assert save(client, session_id, newer).status_code == 200
    assert save(client, session_id, snapshot(2)).status_code == 409
    assert save(client, session_id, snapshot(3)).status_code == 409
    assert save(client, session_id, newer).status_code == 200
    latest = detail(client, session_id)
    assert latest["revision"] == 3
    assert latest["answers"] == [0, 2, 2, 0, 0]
    assert latest["result"]["code"] == "present-cue"


def test_explicit_skip_is_a_turn_and_unknown_unreceived_answer_is_not(client):
    session_id = uid()
    value = snapshot(answers=[None] * 5, answered=[True, False, False, False, False],
                     exercise=None, status="checkin", events=[])
    assert save(client, session_id, value).status_code == 200
    saved = detail(client, session_id)
    assert len(saved["turns"]) == 2
    assert saved["answers"] == [None] * 5
    assert saved["answered"] == [True, False, False, False, False]


@pytest.mark.parametrize("fault", ["timeout", "invalid", "provider"])
def test_provider_failure_retains_result_and_auditable_fallback(client, fault):
    session_id = uid()
    assert save(client, session_id, snapshot()).status_code == 200
    request_id = uid()
    response = client.post(f"/api/sessions/{session_id}/explanation",
                           json={"revision": 1, "request_id": request_id},
                           headers={"X-Peyce-Test-Fault": fault})
    assert response.status_code == 200, response.text
    result = response.json()
    assert result["status"] == "fallback"
    assert result["mode"] == "mock"
    assert result["stale"] is False
    assert result["text"]
    assert len(result["text"]) <= 240
    persisted = detail(client, session_id)
    assert persisted["status"] == "ready"
    assert persisted["result"]["code"] == "body-cue"
    expected_outcome = {"timeout": "fallback-timeout", "invalid": "fallback-invalid",
                        "provider": "fallback-provider"}[fault]
    assert any(item["request_id"] == request_id and item["outcome"] == "fallback"
               and item["validation"] == expected_outcome
               for item in persisted["explanations"])


def test_explanation_request_replay_does_not_add_attempt(client):
    session_id = uid()
    assert save(client, session_id, snapshot()).status_code == 200
    request = {"revision": 1, "request_id": uid()}
    first = client.post(f"/api/sessions/{session_id}/explanation", json=request)
    second = client.post(f"/api/sessions/{session_id}/explanation", json=request)
    assert first.status_code == second.status_code == 200
    assert first.json() == second.json()
    assert len(detail(client, session_id)["explanations"]) == 1


def test_pending_request_replay_calls_provider_once_and_preserves_final_receipt(client, monkeypatch):
    session_id, request = uid(), {"revision": 1, "request_id": uid()}
    assert save(client, session_id, snapshot()).status_code == 200
    service = client.app.state.model_service
    original = service.provider_fragments
    calls = []

    async def observed(*args, **kwargs):
        calls.append(1)
        return await original(*args, **kwargs)

    monkeypatch.setattr(service, "provider_fragments", observed)
    with ThreadPoolExecutor(max_workers=1) as pool:
        pending = pool.submit(client.post, f"/api/sessions/{session_id}/explanation",
                              json=request, headers={"X-Peyce-Test-Fault": "late"})
        deadline = time.monotonic() + 1
        while not detail(client, session_id)["explanations"] and time.monotonic() < deadline:
            time.sleep(0.005)
        assert detail(client, session_id)["explanations"]
        replay = client.post(f"/api/sessions/{session_id}/explanation", json=request)
        assert replay.status_code == 200
        assert replay.json()["status"] == "fallback"
        final = pending.result(timeout=2)
    assert final.json()["status"] == "validated"
    repeated = client.post(f"/api/sessions/{session_id}/explanation", json=request)
    assert repeated.json() == final.json()
    assert len(calls) == 1
    saved = detail(client, session_id)
    assert len(saved["explanations"]) == 1
    assert sum(turn["source"] == "validated-mock-acknowledgment" for turn in saved["turns"]) == 1


def test_replaying_prior_validated_explanation_after_start_is_marked_obsolete(client):
    session_id = uid()
    ready = snapshot()
    assert save(client, session_id, ready).status_code == 200
    request = {"revision": 1, "request_id": uid()}
    assert client.post(f"/api/sessions/{session_id}/explanation", json=request).json()["status"] == "validated"
    assert save(client, session_id, snapshot(2, status="active", events=ready["events"] + [event("start", 12000)])).status_code == 200
    repeated = client.post(f"/api/sessions/{session_id}/explanation", json=request)
    assert repeated.json()["status"] == "obsolete"
    assert repeated.json()["stale"] is True
    assert detail(client, session_id)["status"] == "active"


def test_late_explanation_becomes_obsolete_after_exercise_starts(client):
    session_id = uid()
    ready = snapshot()
    assert save(client, session_id, ready).status_code == 200
    with ThreadPoolExecutor(max_workers=1) as pool:
        pending = pool.submit(client.post, f"/api/sessions/{session_id}/explanation",
                              json={"revision": 1, "request_id": uid()},
                              headers={"X-Peyce-Test-Fault": "late"})
        time.sleep(0.04)
        events = ready["events"] + [event("start", 12000)]
        assert save(client, session_id, snapshot(2, status="active", events=events)).status_code == 200
        response = pending.result(timeout=2)
    assert response.status_code == 200, response.text
    assert response.json()["stale"] is True
    assert response.json()["status"] == "obsolete"
    saved = detail(client, session_id)
    assert saved["status"] == "active"
    assert saved["revision"] == 2
    assert saved["exercise"] == "breathing"
    assert saved["explanations"][0]["outcome"] == "obsolete"


def test_validated_mock_is_contextual_and_persisted_separately_from_user_turns(client):
    examples = [([2, 0, 0, 0, 0], "breathing", "body-cue"),
                ([0, 2, 0, 0, 0], "grounding", "present-cue")]
    texts = []
    for answers, exercise, reason in examples:
        session_id = uid()
        assert save(client, session_id, snapshot(answers=answers, exercise=exercise)).status_code == 200
        response = client.post(f"/api/sessions/{session_id}/explanation",
                               json={"revision": 1, "request_id": uid()})
        assert response.status_code == 200, response.text
        body = response.json()
        assert body["status"] == "validated"
        assert body["mode"] == "mock"
        assert body["fragments"]["reason_code"] == reason
        assert body["references"]
        texts.append(body["text"])
        saved = detail(client, session_id)
        assert saved["explanations"][0]["text"] == body["text"]
        assert any(turn["source"] == "validated-mock-acknowledgment"
                   and turn["role"] == "assistant" for turn in saved["turns"])
        assert all(turn["source"] == "structured-turn" for turn in saved["turns"] if turn["role"] == "user")
    assert texts[0] != texts[1]


def test_http_records_have_valid_sql_relationships_not_only_json_snapshots(client):
    session_id = uid()
    finish_flow(client, session_id)
    repository = client.app.state.repository
    with repository.connection() as db:
        assert db.execute("PRAGMA foreign_key_check").fetchall() == []
        assert db.execute("PRAGMA user_version").fetchone()[0] == 1
        row = db.execute("SELECT status,revision,context FROM sessions WHERE id=?", (session_id,)).fetchone()
        assert tuple(row) == ("finished", 4, "fictional-local-coursework")
        assert db.execute("SELECT COUNT(*) FROM revisions WHERE session_id=?", (session_id,)).fetchone()[0] == 4
        assert db.execute("SELECT COUNT(*) FROM operations WHERE session_id=?", (session_id,)).fetchone()[0] == 4
        assert db.execute("SELECT COUNT(*) FROM turns WHERE session_id=? AND role='user'", (session_id,)).fetchone()[0] == 20
        assert db.execute("SELECT COUNT(*) FROM lifecycle WHERE session_id=? AND kind='complete'", (session_id,)).fetchone()[0] == 1


def test_database_fault_leaves_no_partial_session_and_retry_is_once(client):
    session_id = uid()
    value = snapshot()
    rejected = save(client, session_id, value, headers={"X-Peyce-Test-Fault": "database"})
    assert rejected.status_code == 503
    assert client.get(f"/api/sessions/{session_id}").status_code == 404
    assert save(client, session_id, value).status_code == 200
    assert save(client, session_id, value).status_code == 200
    saved = detail(client, session_id)
    assert len(saved["turns"]) == 10
    assert len(saved["lifecycle"]) == 1


def test_midtransaction_lifecycle_conflict_rolls_back_new_revision_and_turns(client):
    session_id = uid()
    original = snapshot()
    assert save(client, session_id, original).status_code == 200
    altered_event = dict(original["events"][0], active_ms=1)
    bad = snapshot(2, answers=[0, 2, 2, 0, 0], exercise="grounding", events=[altered_event])
    assert save(client, session_id, bad).status_code == 409
    saved = detail(client, session_id)
    assert saved["revision"] == 1
    assert saved["answers"] == original["answers"]
    assert len(saved["turns"]) == 10
    with client.app.state.repository.connection() as db:
        assert db.execute("SELECT COUNT(*) FROM revisions WHERE session_id=?", (session_id,)).fetchone()[0] == 1
        assert db.execute("SELECT COUNT(*) FROM operations WHERE session_id=?", (session_id,)).fetchone()[0] == 1


def test_reused_operation_id_with_different_action_is_not_acknowledged_as_saved(client):
    session_id = uid()
    original = snapshot()
    assert save(client, session_id, original).status_code == 200
    altered = dict(original, answers=[0, 2, 2, 0, 0], exercise="grounding")
    assert save(client, session_id, altered).status_code == 409
    assert detail(client, session_id)["answers"] == original["answers"]


def test_restart_marks_only_active_or_paused_as_interrupted(client, settings):
    ids = {status: uid() for status in ("active", "paused", "stopped", "ready")}
    for status, session_id in ids.items():
        events = [event("instruction_visible", 10000)]
        if status != "ready":
            events += [event("start", 12000)]
        if status == "paused":
            events += [event("pause", 15000, 3000)]
        elif status == "stopped":
            events += [event("stop", 15000, 3000)]
        assert save(client, session_id, snapshot(status=status, events=events)).status_code == 200
    with TestClient(create_app(settings)) as restarted:
        for original, session_id in ids.items():
            expected = "interrupted" if original in {"active", "paused"} else original
            assert detail(restarted, session_id)["status"] == expected


def test_restart_preserves_a_pending_attempt_as_obsolete_instead_of_claiming_success(client, settings):
    session_id = uid()
    assert save(client, session_id, snapshot()).status_code == 200
    request = {"revision": 1, "request_id": uid()}
    # Simulate the durable state left when a process ends after reserving a
    # request but before a provider response. No provider is called here.
    client.app.state.repository.begin_explanation(
        session_id, ExplanationRequest(**request), "mock", "peyce-mock-1.0")
    with TestClient(create_app(settings)) as restarted:
        saved = detail(restarted, session_id)
        assert saved["status"] == "ready"
        assert saved["explanations"][0]["outcome"] == "obsolete"
        assert saved["explanations"][0]["validation"] == "interrupted-request"
        replay = restarted.post(f"/api/sessions/{session_id}/explanation", json=request)
        assert replay.json()["status"] == "obsolete"
        assert replay.json()["stale"] is True


def test_interrupt_is_idempotent_and_does_not_rewrite_a_confirmed_finish(client):
    session_id = uid()
    events = [event("instruction_visible", 10000), event("start", 12000)]
    assert save(client, session_id, snapshot(status="active", events=events)).status_code == 200
    request = {"revision": 1, "operation_id": uid()}
    for _ in range(2):
        response = client.post(f"/api/sessions/{session_id}/interrupt", json=request)
        assert response.status_code == 200, response.text
    assert detail(client, session_id)["status"] == "interrupted"
    completed_id = uid()
    finish_flow(client, completed_id)
    response = client.post(f"/api/sessions/{completed_id}/interrupt",
                           json={"revision": 4, "operation_id": uid()})
    assert response.status_code == 200
    assert detail(client, completed_id)["status"] == "finished"


def test_stale_interrupt_cannot_mark_newer_active_revision_as_left(client):
    session_id = uid()
    ready = snapshot()
    assert save(client, session_id, ready).status_code == 200
    assert save(client, session_id, snapshot(2, status="active", events=ready["events"] + [event("start", 12000)])).status_code == 200
    response = client.post(f"/api/sessions/{session_id}/interrupt",
                           json={"revision": 1, "operation_id": uid()})
    assert response.status_code == 409
    assert detail(client, session_id)["status"] == "active"


@pytest.mark.parametrize("change", [
    {"answers": [0, 1, 2, None]},
    {"answers": [True, 0, 0, 0, 0]},
    {"answers": [0, 0, 0, 0, 3]},
    {"answers": [0, 0, 0, 0, 0], "answered": [False] * 5},
    {"unexpected_clinical_score": 9},
])
def test_invalid_snapshot_is_rejected_before_sql_write(client, change):
    session_id = uid()
    assert save(client, session_id, snapshot(**change)).status_code == 422
    assert client.get(f"/api/sessions/{session_id}").status_code == 404


def test_cannot_fabricate_breathing_completion_from_a_status_label(client):
    session_id = uid()
    invalid = snapshot(status="completed", events=[event("complete", 20000, 8000)])
    assert save(client, session_id, invalid).status_code == 422
    assert client.get(f"/api/sessions/{session_id}").status_code == 404


def test_cannot_bypass_complete_validation_by_sending_finished_directly(client):
    session_id = uid()
    invalid = snapshot(status="finished", events=[event("finish", 20000, 8000)])
    assert save(client, session_id, invalid).status_code == 422
    assert client.get(f"/api/sessions/{session_id}").status_code == 404


def test_timing_counts_overlapping_allowed_intervals_once_and_rejects_double_subtraction(client):
    events = [event("instruction_visible", 10000), event("start", 12000),
              event("complete", 78000, 60000, "clock"), event("finish", 82000, 60000)]
    timing = {"raw_ms": 72000, "counted_ms": 66000, "excluded_ms": 6000,
              "excluded_intervals": [
                  {"start_ms": 20000, "end_ms": 24000, "cause": "user"},
                  {"start_ms": 22000, "end_ms": 26000, "cause": "support"}],
              "instruction_ms": 10000, "finish_ms": 82000, "entry_ms": 10000}
    valid = snapshot(status="finished", events=events, timing=timing)
    response = save(client, uid(), valid)
    assert response.status_code == 200, response.text
    timing["excluded_ms"], timing["counted_ms"] = 8000, 64000
    assert save(client, uid(), snapshot(status="finished", events=events, timing=timing)).status_code == 422


def test_background_pause_cannot_be_excluded_as_permitted_user_pause(client):
    timing = {"raw_ms": 66000, "counted_ms": 65000, "excluded_ms": 1000,
              "excluded_intervals": [{"start_ms": 20000, "end_ms": 21000, "cause": "background"}],
              "instruction_ms": 10000, "finish_ms": 76000, "entry_ms": 10000}
    assert save(client, uid(), snapshot(timing=timing)).status_code == 422


def test_arithmetically_correct_timing_cannot_omit_first_visible_instruction(client):
    timing = {"raw_ms": 65000, "counted_ms": 65000, "excluded_ms": 0,
              "excluded_intervals": [], "instruction_ms": 11000,
              "finish_ms": 76000, "entry_ms": 10000}
    events = [event("instruction_visible", 10000), event("start", 12000),
              event("complete", 72000, 60000, "clock"), event("finish", 76000, 60000)]
    assert save(client, uid(), snapshot(status="finished", timing=timing, events=events)).status_code == 422


def test_controlled_database_read_failure_is_explicit_and_does_not_delete_history(client):
    session_id = uid()
    assert save(client, session_id, snapshot()).status_code == 200
    for path in ("/api/sessions", f"/api/sessions/{session_id}"):
        response = client.get(path, headers={"X-Peyce-Test-Fault": "database"})
        assert response.status_code == 503
    assert detail(client, session_id)["status"] == "ready"


def test_clear_history_deletes_records_but_does_not_recreate_demo_sessions(client):
    assert client.get("/api/sessions").json() == {"sessions": []}
    session_id = uid()
    assert save(client, session_id, snapshot()).status_code == 200
    assert client.delete("/api/sessions").status_code == 200
    assert client.get("/api/sessions").json() == {"sessions": []}
    assert client.get(f"/api/sessions/{session_id}").status_code == 404


def test_test_fault_headers_fail_closed_when_not_explicitly_enabled(settings):
    with TestClient(create_app(replace(settings, test_controls=False))) as normal:
        session_id = uid()
        response = save(normal, session_id, snapshot(), headers={"X-Peyce-Test-Fault": "database"})
        assert response.status_code == 400
        assert normal.get(f"/api/sessions/{session_id}").status_code == 404


def test_unknown_schema_version_is_refused_without_resetting_existing_rows(client, settings):
    session_id = uid()
    assert save(client, session_id, snapshot()).status_code == 200
    with client.app.state.repository.connection() as db:
        db.execute("PRAGMA user_version=99")
    with pytest.raises(RuntimeError, match="Unsupported schema version"):
        with TestClient(create_app(settings)):
            pass
    with client.app.state.repository.connection() as db:
        assert db.execute("PRAGMA user_version").fetchone()[0] == 99
        assert db.execute("SELECT status FROM sessions WHERE id=?", (session_id,)).fetchone()[0] == "ready"
