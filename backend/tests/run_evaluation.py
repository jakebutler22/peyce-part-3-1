"""Repeatable Part 3.3 API/SQLite supplement, never a GUI or live-model test.

Run from the repository with backend/.venv/bin/python backend/tests/run_evaluation.py
--output docs/evidence/3.3/deterministic-run-1.json --run-label run-1.
Every database is temporary; real runtime state and credentials are never opened.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from tempfile import TemporaryDirectory
import time
from unittest.mock import patch
from uuid import uuid4

os.environ["PYTHON_DOTENV_DISABLED"] = "1"
os.environ["PEYCE_MODEL_MODE"] = "mock"
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

import httpx
from fastapi.testclient import TestClient
from app.config import Settings
from app.domain import CONTENT_VERSION, POLICY_VERSION, PROMPT_VERSION, QUESTION_VERSION
from app.main import create_app

FIXTURE = Path(__file__).parent / "fixtures/evaluation-3.3.json"
MATRIX = json.loads(FIXTURE.read_text())
CASES = {item["id"]: item for item in MATRIX["scenarios"]}


def uid():
    return str(uuid4())


def event(kind, at, active=0, cause="user"):
    return {"id": uid(), "kind": kind, "at_ms": at, "active_ms": active, "cause": cause}


def snapshot(selected, revision=1, **changes):
    value = {"operation_id": uid(), "revision": revision,
             "answers": list(selected["answers"]), "answered": list(selected["answered"]),
             "direct_choice": selected["direct_choice"], "exercise": None, "status": "choice",
             "color": "pink", "color_explicit": False, "events": [], "timing": None}
    value.update(changes)
    return value


def save(client, session_id, value, expected=200, fault=None):
    response = client.put(f"/api/sessions/{session_id}/snapshot", json=value,
                          headers={"X-Peyce-Test-Fault": fault} if fault else {})
    assert response.status_code == expected, response.text
    return response.json()


def detail(client, session_id):
    response = client.get(f"/api/sessions/{session_id}")
    assert response.status_code == 200, response.text
    return response.json()


def explain(client, session_id, revision=1, request_id=None, fault=None):
    response = client.post(f"/api/sessions/{session_id}/explanation",
                           json={"revision": revision, "request_id": request_id or uid()},
                           headers={"X-Peyce-Test-Fault": fault} if fault else {})
    assert response.status_code == 200, response.text
    return response.json()


class FixtureContext:
    def __enter__(self):
        self.temp = TemporaryDirectory(prefix="peyce-fictional-evaluation-")
        self.settings = Settings(db_path=str(Path(self.temp.name) / "fictional.sqlite3"),
                                 model_mode="mock", api_key="", model_id="",
                                 test_controls=True, model_timeout_seconds=0.04,
                                 test_late_seconds=0.08)
        self.client_context = TestClient(create_app(self.settings))
        self.client = self.client_context.__enter__()
        self.repository = self.client.app.state.repository
        return self

    def __exit__(self, *args):
        self.client_context.__exit__(*args)
        self.temp.cleanup()

    def sql(self, query, arguments=()):
        with self.repository.connection() as database:
            return [tuple(row) for row in database.execute(query, arguments)]

    def counts(self):
        return {table: self.sql(f"SELECT COUNT(*) FROM {table}")[0][0]
                for table in ("sessions", "revisions", "operations", "turns", "lifecycle", "explanations")}


def completed_flow(context, selected, skill="breathing", color="pink"):
    client, session_id = context.client, uid()
    events = [event("instruction_visible", 10000)]
    common = dict(exercise=skill, color=color, color_explicit=color != "pink")
    save(client, session_id, snapshot(selected, events=events, status="ready", **common))
    acknowledgment = explain(client, session_id)
    events += [event("start", 12000)]
    save(client, session_id, snapshot(selected, 2, events=events, status="active", **common))
    if skill == "breathing":
        events += [event("complete", 72000, 60000, "clock")]
        finish, active = 76000, 60000
    else:
        events += [event("sense_next", at) for at in (17000, 22000, 27000, 32000, 37000)]
        events += [event("complete", 37001)]
        finish, active = 43000, 0
    save(client, session_id, snapshot(selected, 3, events=events, status="completed", **common))
    events += [event("finish", finish, active)]
    timing = {"raw_ms": finish - 10000, "counted_ms": finish - 10000, "excluded_ms": 0,
              "excluded_intervals": [], "instruction_ms": 10000, "finish_ms": finish, "entry_ms": 10000}
    final = snapshot(selected, 4, events=events, status="finished", timing=timing, **common)
    save(client, session_id, final)
    return session_id, detail(client, session_id), acknowledgment, final


def S01(context, case):
    session_id, saved, acknowledgment, _ = completed_flow(context, case["inputs"][0])
    expected = case["expected"]
    assert saved["status"] == expected["status"] and saved["result"]["code"] == expected["rule"]
    assert saved["exercise"] == expected["exercise"]
    assert saved["timing"]["counted_ms"] == expected["counted_ms"]
    assert max(item["active_ms"] for item in saved["lifecycle"]) == expected["active_ms"]
    assert acknowledgment["mode"] == "mock" and acknowledgment["status"] == "validated"
    assert any(item["id"] == session_id for item in context.client.get("/api/sessions").json()["sessions"])
    foreign_keys = len(context.sql("PRAGMA foreign_key_check"))
    assert foreign_keys == 0
    return {"rule": saved["result"]["code"], "exercise": saved["exercise"], "status": saved["status"],
            "counted_ms": saved["timing"]["counted_ms"], "active_ms": max(item["active_ms"] for item in saved["lifecycle"]), "mode": acknowledgment["mode"],
            "complete_events": sum(e["kind"] == "complete" for e in saved["lifecycle"]), "foreign_key_errors": foreign_keys}


def S02(context, case):
    _, saved, acknowledgment, _ = completed_flow(context, case["inputs"][0], "grounding")
    expected = case["expected"]
    senses = [item for item in saved["lifecycle"] if item["kind"] == "sense_next"]
    assert saved["result"]["code"] == expected["rule"] and saved["exercise"] == expected["exercise"]
    assert saved["status"] == expected["status"] and len(senses) == expected["sense_actions"]
    assert saved["timing"]["counted_ms"] == expected["counted_ms"]
    return {"rule": saved["result"]["code"], "exercise": saved["exercise"], "status": saved["status"],
            "sense_actions": len(senses), "synthetic_step_order": ["seen", "felt", "heard", "smelled", "tasted"],
            "counted_ms": saved["timing"]["counted_ms"], "mode": acknowledgment["mode"]}


def S03(context, case):
    selected, session_id = case["inputs"][0], uid()
    response = save(context.client, session_id, snapshot(selected))
    assert response["result"]["code"] == case["expected"]["rule"] and response["result"]["exercise"] is None
    first = detail(context.client, session_id)
    skipped = [turn for turn in first["turns"] if turn["role"] == "user" and turn["question_id"] == "body"]
    assert len(skipped) == 1 and skipped[0]["skipped"] == 1 and first["answers"][0] is None
    save(context.client, session_id, snapshot(dict(selected, direct_choice="grounding"), 2, exercise="grounding", status="ready"))
    wording = explain(context.client, session_id, 2)
    assert "body" not in wording["references"]
    return {"rule": response["result"]["code"], "skipped_body_unknown": first["answers"][0] is None,
            "skip_recorded": True, "references": wording["references"]}


def S04(context, case):
    skills, user_turns = [], []
    for selected in case["inputs"]:
        session_id, skill = uid(), selected["direct_choice"]
        response = save(context.client, session_id, snapshot(selected, exercise=skill, status="ready"))
        assert response["result"]["code"] == case["expected"]["rule"]
        count = sum(t["role"] == "user" for t in detail(context.client, session_id)["turns"])
        assert count == 0
        assert explain(context.client, session_id)["references"] == []
        skills.append(response["result"]["exercise"])
        user_turns.append(count)
    assert skills == ["breathing", "grounding"]
    return {"allowed_direct_skills": skills, "user_turns": user_turns, "references": []}


def S05(context, case):
    session_id, events = uid(), [event("instruction_visible", 10000)]
    save(context.client, session_id, snapshot(case["inputs"][0], exercise="breathing", status="ready", events=events))
    old = explain(context.client, session_id)
    save(context.client, session_id, snapshot(case["inputs"][1], 2, exercise="grounding", status="ready", events=events))
    new = explain(context.client, session_id, 2)
    saved = detail(context.client, session_id)
    current_users = [turn for turn in saved["turns"] if turn["role"] == "user" and not turn["superseded"]]
    current_question_ids = [turn["question_id"] for turn in current_users]
    assert len(current_question_ids) == len(set(current_question_ids)) == case["expected"]["current_unique_questions"]
    assert old["fragments"]["reason_code"] == case["expected"]["old_rule"]
    assert new["fragments"]["reason_code"] == saved["result"]["code"] == case["expected"]["new_rule"]
    assert "thought" in new["references"] and "body" not in new["references"]
    assert saved["explanations"][0]["superseded"] is True
    return {"old_rule": old["fragments"]["reason_code"], "new_rule": saved["result"]["code"],
            "exercise": saved["exercise"], "current_unique_questions": len(set(current_question_ids)),
            "current_user_turns": len(current_users), "new_references": new["references"], "old_superseded": True}


def S06(context, case):
    results = []
    for selected in case["inputs"]:
        response = save(context.client, uid(), snapshot(selected))
        assert response["result"]["code"] == case["expected"]["rule"] and response["result"]["exercise"] is None
        assert not any("score" in key for key in response["result"])
        results.append({"input": selected["name"], "rule": response["result"]["code"], "exercise": None})
    return {"variants": results, "clinical_score_present": False}


def S07(context, case):
    results = []
    for selected, rule, skill in zip(case["inputs"], case["expected"]["rules"], case["expected"]["exercises"]):
        response = save(context.client, uid(), snapshot(selected, exercise=skill, status="ready" if skill else "choice"))
        assert response["result"]["code"] == rule and response["result"]["exercise"] == skill
        results.append({"input": selected["name"], "rule": rule, "exercise": skill})
    return {"variants": results, "current_choice_wins": True}


def S08(context, case):
    old_id, old, _, _ = completed_flow(context, case["inputs"][0], color="red")
    new_id = uid()
    save(context.client, new_id, snapshot(case["inputs"][1], exercise="breathing", status="ready", color=old["color"], color_explicit=True))
    repeated = detail(context.client, new_id)
    assert old_id != new_id and repeated["status"] == case["expected"]["new_status"]
    assert repeated["color"] == case["expected"]["remembered_color"] and repeated["color_explicit"] is True
    assert repeated["answers"] == case["expected"]["new_answers"] and repeated["timing"] is None
    assert repeated["explanations"] == [] and repeated["events"] == []
    return {"fresh_id": old_id != new_id, "new_status": repeated["status"], "color": repeated["color"],
            "all_answers_unknown": all(a is None for a in repeated["answers"]), "no_inherited_timing": repeated["timing"] is None,
            "no_inherited_model_output": repeated["explanations"] == [], "old_status": detail(context.client, old_id)["status"]}


def S10(context, case):
    selected, session_id = case["inputs"][0], uid()
    events = [event("instruction_visible", 10000), event("start", 12000), event("pause", 20000, 8000),
              event("support_open", 22000, 8000, "support"), event("support_close", 24000, 8000, "support"),
              event("resume", 26000, 8000), event("complete", 78000, 60000, "clock"), event("finish", 82000, 60000)]
    timing = {"raw_ms": 72000, "counted_ms": 66000, "excluded_ms": 6000,
              "excluded_intervals": [{"start_ms": 20000, "end_ms": 26000, "cause": "user"},
                                     {"start_ms": 22000, "end_ms": 24000, "cause": "support"}],
              "instruction_ms": 10000, "finish_ms": 82000, "entry_ms": 10000}
    save(context.client, session_id, snapshot(selected, status="finished", exercise="breathing", events=events, timing=timing))
    observed = detail(context.client, session_id)["timing"]
    assert all(observed[key] == case["expected"][key] for key in ("raw_ms", "counted_ms", "excluded_ms"))
    return {key: observed[key] for key in ("raw_ms", "counted_ms", "excluded_ms")}


def S11(context, case):
    selected, outcomes = case["inputs"][0], []
    for original in ("active", "paused", "stopped"):
        session_id = uid()
        events = [event("instruction_visible", 10000), event("start", 12000)]
        if original == "paused":
            events += [event("pause", 15000, 3000)]
        elif original == "stopped":
            events += [event("stop", 15000, 3000), event("finish", 17000, 3000)]
        save(context.client, session_id, snapshot(selected, status=original, exercise="breathing", events=events))
        if original == "active":
            receipt = context.client.post(f"/api/sessions/{session_id}/interrupt", json={"revision": 1, "operation_id": uid()})
            assert receipt.status_code == 200
            saved = detail(context.client, session_id)
        else:
            with TestClient(create_app(context.settings)) as restarted:
                saved = detail(restarted, session_id)
        assert not any(e["kind"] == "complete" for e in saved["lifecycle"]) and saved["timing"] is None
        outcomes.append(saved["status"])
    assert outcomes == case["expected"]["statuses"]
    return {"statuses": outcomes, "complete_events": 0, "finished_timing_created": False,
            "restart_kind": "application lifespan, not process"}


def S12(context, case):
    outcomes = []
    for fault, expected in zip(("provider", "timeout", "invalid"), case["expected"]["validations"]):
        session_id = uid()
        save(context.client, session_id, snapshot(case["inputs"][0], status="ready", exercise="breathing"))
        response = explain(context.client, session_id, fault=fault)
        saved = detail(context.client, session_id)
        assert response["status"] == "fallback" and response["mode"] == "mock"
        assert saved["status"] == "ready" and saved["exercise"] == case["expected"]["exercise_unchanged"]
        assert saved["explanations"][0]["validation"] == expected
        outcomes.append({"fault": fault, "status": response["status"], "mode": response["mode"], "validation": expected})
    return {"variants": outcomes, "exercise": "breathing", "status": "ready"}


def S13(context, case):
    variants = []
    for action in ("start", "correction"):
        session_id, events = uid(), [event("instruction_visible", 10000)]
        save(context.client, session_id, snapshot(case["inputs"][0], status="ready", exercise="breathing", events=events))
        with ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(explain, context.client, session_id, 1, None, "late")
            deadline = time.monotonic() + 2
            while not detail(context.client, session_id)["explanations"] and time.monotonic() < deadline:
                time.sleep(0.002)
            assert detail(context.client, session_id)["explanations"]
            selected = case["inputs"][0] if action == "start" else case["inputs"][1]
            if action == "start":
                events += [event("start", 12000)]
            save(context.client, session_id, snapshot(selected, 2, status="active" if action == "start" else "ready",
                                                     exercise="breathing" if action == "start" else "grounding", events=events))
            response = future.result(timeout=3)
        saved = detail(context.client, session_id)
        assert response["status"] == "obsolete" and response["stale"] is True
        assert saved["status"] == ("active" if action == "start" else "ready") and saved["revision"] == 2
        assert saved["explanations"][0]["stale"] == 1
        variants.append({"action": action, "old_result": response["status"], "stale": response["stale"],
                         "current_status": saved["status"], "current_rule": saved["result"]["code"]})
    return {"variants": variants}


def S14(context, case):
    session_id, value = uid(), snapshot(case["inputs"][0], status="ready", exercise="breathing", events=[event("instruction_visible", 10000)])
    save(context.client, session_id, value, expected=case["expected"]["first_http"], fault="database")
    assert context.client.get(f"/api/sessions/{session_id}").status_code == 404
    save(context.client, session_id, value)
    save(context.client, session_id, value)
    counts = context.counts()
    user_turns = sum(turn["role"] == "user" for turn in detail(context.client, session_id)["turns"])
    assert counts["sessions"] == case["expected"]["sessions"] and counts["lifecycle"] == case["expected"]["lifecycle_events"]
    assert user_turns == case["expected"]["user_turns"] and counts["operations"] == 1
    return {"first_http": 503, "absent_after_failure": True, "sessions": counts["sessions"],
            "lifecycle_events": counts["lifecycle"], "user_turns": user_turns, "operations": counts["operations"]}


def S15(context, case):
    session_id, before, _, _ = completed_flow(context, case["inputs"][0], color="red")
    with TestClient(create_app(context.settings)) as restarted:
        after = detail(restarted, session_id)
        assert after == before
        assert any(item["id"] == session_id for item in restarted.get("/api/sessions").json()["sessions"])
    foreign_keys = len(context.sql("PRAGMA foreign_key_check"))
    assert foreign_keys == case["expected"]["foreign_key_errors"]
    assert after["explanations"][0]["mode"] == case["expected"]["mode"]
    return {"status": after["status"], "color": after["color"], "mode": after["explanations"][0]["mode"],
            "foreign_key_errors": foreign_keys, "exact_detail_preserved": after == before,
            "restart_kind": "application lifespan, not process"}


def S16(context, case):
    completed_flow(context, case["inputs"][0])
    with context.repository.connection() as database:
        database.execute("UPDATE live_budget SET attempts=7 WHERE id=1")
    assert context.client.delete("/api/sessions").status_code == 200
    counts = context.counts()
    attempts = context.sql("SELECT attempts FROM live_budget")[0][0]
    assert all(count == 0 for count in counts.values()) and attempts == case["expected"]["attempts"]
    return {"remaining_sessions": counts["sessions"], "related_rows": sum(counts.values()), "attempts": attempts,
            "guard_is_artificial_disposable_fixture": True, "confirmation_cancel": "requires controller/GUI"}


def S17(context, case):
    session_id = uid()
    selected = case["inputs"][0]
    save(context.client, session_id, snapshot(selected, status="ready", exercise="breathing"))
    default = explain(context.client, session_id)
    assert default["mode"] == "mock" and context.sql("SELECT attempts FROM live_budget")[0][0] == 0
    settings = replace(context.settings, model_mode="openrouter", model_id="nvidia/nemotron-3.5-lightning:free",
                       api_key="fictional-transport-placeholder", budget_approved=True, approved_budget_usd=0,
                       pricing_verified=True, live_max_attempts=10)
    # Set a simulated ledger only inside this disposable database. Real ledger is never opened.
    with context.repository.connection() as database:
        database.execute("UPDATE live_budget SET attempts=9 WHERE id=1")
    calls = []
    fragments = {"reason_code": "body-cue", "opening_id": "notice", "reference_ids": ["body"], "closing_id": "change"}

    class FakeClient:
        def __init__(self, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def post(self, url, **kwargs):
            calls.append(1)
            return httpx.Response(200, request=httpx.Request("POST", url), json={
                "model": settings.model_id, "choices": [{"finish_reason": "tool_calls", "message": {
                    "content": None, "tool_calls": [{"type": "function", "function": {
                        "name": "acknowledge_current_rule", "arguments": json.dumps(fragments)}}]}}]})

    with TestClient(create_app(settings)) as configured, patch("app.explanations.httpx.AsyncClient", FakeClient):
        boundary_id = uid()
        save(configured, boundary_id, snapshot(selected, status="ready", exercise="breathing"))
        boundary = explain(configured, boundary_id)
        assert boundary["mode"] == "openrouter" and len(calls) == 1
        capped_id, capped_request = uid(), uid()
        save(configured, capped_id, snapshot(selected, status="ready", exercise="breathing"))
        capped = explain(configured, capped_id, request_id=capped_request)
        replay = explain(configured, capped_id, request_id=capped_request)
        assert capped == replay and capped["mode"] == case["expected"]["after_cap_mode"]
        assert capped["status"] == "validated" and capped["model_id"] == case["expected"]["after_cap_model"]
        saved = detail(configured, capped_id)
        assert saved["explanations"][0]["mode"] == "mock"
        assert saved["explanations"][0]["validation"] == "validated-mock-live-limit"
        assert any(t["source"] == "validated-mock-acknowledgment" for t in saved["turns"])
        assert len(saved["explanations"]) == 1 and len(calls) == case["expected"]["simulated_dispatches"]
        assert configured.delete("/api/sessions").status_code == 200
    attempts = context.sql("SELECT attempts FROM live_budget")[0][0]
    assert attempts == case["expected"]["final_attempts"]
    return {"default_mode": default["mode"], "default_dispatches": 0, "simulated_transport_calls": len(calls),
            "after_cap_mode": capped["mode"], "after_cap_model": capped["model_id"], "after_cap_status": capped["status"],
            "persisted_mode": saved["explanations"][0]["mode"], "replay_same_receipt": capped == replay,
            "final_attempts": attempts, "real_network_calls": 0, "transport_is_mock_not_live_evidence": True}


def assert_B2(observations):
    """Cross-case API invariants. Controller/button meaning needs separate tests."""
    assert observations["S01"]["status"] == "finished" and observations["S01"]["active_ms"] == 60000
    assert observations["S02"]["sense_actions"] == 5
    assert observations["S03"]["skipped_body_unknown"] and "body" not in observations["S03"]["references"]
    assert observations["S04"]["allowed_direct_skills"] == ["breathing", "grounding"]
    assert observations["S05"]["new_rule"] == "present-cue" and observations["S05"]["exercise"] == "grounding"
    assert observations["S07"]["current_choice_wins"]
    assert observations["S10"]["excluded_ms"] == 6000
    assert observations["S11"]["statuses"] == ["interrupted", "interrupted", "stopped"]
    assert observations["S11"]["complete_events"] == 0
    assert all(item["stale"] and item["old_result"] == "obsolete" for item in observations["S13"]["variants"])
    return {"id": "B2", "result": "pass-at-api-layer", "cases": MATRIX["behaviors"][1]["cases"],
            "assertion": "assert_B2", "limits": "API invariants do not establish actual button, clock, animation or focus behavior."}


def assert_B3(observations):
    """Cross-case receipts/committed rows, distinct from browser saved labels."""
    assert observations["S01"]["foreign_key_errors"] == 0 and observations["S01"]["mode"] == "mock"
    assert observations["S05"]["old_superseded"] and observations["S05"]["current_user_turns"] == 5
    assert observations["S08"]["fresh_id"] and observations["S08"]["no_inherited_model_output"]
    assert observations["S11"]["finished_timing_created"] is False
    assert all(item["mode"] == "mock" and item["status"] == "fallback" for item in observations["S12"]["variants"])
    assert observations["S14"]["operations"] == observations["S14"]["sessions"] == 1
    assert observations["S15"]["exact_detail_preserved"]
    assert observations["S16"]["related_rows"] == 0 and observations["S16"]["attempts"] == 7
    assert observations["S17"]["persisted_mode"] == "mock" and observations["S17"]["final_attempts"] == 10
    return {"id": "B3", "result": "pass-at-api-layer", "cases": MATRIX["behaviors"][2]["cases"],
            "assertion": "assert_B3", "limits": "No actual GUI saved label or process-restart observation is inferred."}


def run_suite():
    outcomes, observations = [], {}
    # Any accidental real AsyncClient dispatch fails the suite before networking.
    with patch("app.explanations.httpx.AsyncClient.post", side_effect=AssertionError("Network prohibited in deterministic evaluation")):
        for case in MATRIX["scenarios"]:
            implementation = globals().get(case["id"])
            record = {"id": case["id"], "title": case["title"], "inputs": case["inputs"],
                      "initial_state": case["initial_state"], "actions": case["actions"],
                      "expected": case["expected"], "layers": case["automated_layers"],
                      "other_layers_required": case["required_other_layers"], "mode": "mock; no live network",
                      "evidence_path": case["evidence_path"]}
            if implementation is None:
                record.update(result="not-evaluated-at-api-layer", observed="Local controller/GUI behavior; root evidence required.")
            else:
                with FixtureContext() as context:
                    observed = implementation(context, case)
                observations[case["id"]] = observed
                record.update(result="pass-at-api-layer", observed=observed)
            outcomes.append(record)
    behaviors = [{"id": "B1", "result": "not-evaluated-at-api-layer", "cases": MATRIX["behaviors"][0]["cases"],
                  "assertion": "frontend/tests/personalization.test.js: assertSupportAccess and B1 tests",
                  "limits": "Support is local controller/UI. API checks cannot prove its reachability."},
                 assert_B2(observations), assert_B3(observations)]
    summary = {"predeclared_scenarios": 18, "api_scenarios_passed": sum(o["result"] == "pass-at-api-layer" for o in outcomes),
               "scenarios_requiring_controller_gui": [o["id"] for o in outcomes if o["result"] != "pass-at-api-layer"],
               "api_cross_case_assertions_passed": 2, "api_failures": 0, "real_network_calls": 0,
               "actual_gui_claim": False, "real_wall_clock_duration_claim": False, "real_runtime_accessed": False}
    result = {"scenarios": outcomes, "behavior_checks": behaviors, "summary": summary}
    result["repeat_signature"] = hashlib.sha256(json.dumps(result, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    parser.add_argument("--run-label", required=True)
    arguments = parser.parse_args()
    result = run_suite()
    app_files = sorted((ROOT / "backend/app").glob("*.py"))
    result["context"] = {"run_label": arguments.run_label, "python": platform.python_version(),
                         "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                         "app_matches_git_head": subprocess.run(["git", "diff", "--quiet", "--", "backend/app"], cwd=ROOT).returncode == 0,
                         "app_file_sha256": {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in app_files},
                         "question_version": QUESTION_VERSION, "policy_version": POLICY_VERSION,
                         "prompt_version": PROMPT_VERSION, "content_version": CONTENT_VERSION,
                         "fixture_sha256": hashlib.sha256(FIXTURE.read_bytes()).hexdigest(),
                         "fixture_path": str(FIXTURE.relative_to(ROOT)),
                         "controlled_database": "New TemporaryDirectory for every API scenario; destroyed on exit",
                         "environment": "dotenv loading disabled; mock mode; real async transport prohibited"}
    target = Path(arguments.output)
    if not target.is_absolute():
        target = ROOT / target
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(target.relative_to(ROOT)), "summary": result["summary"], "repeat_signature": result["repeat_signature"]}))


if __name__ == "__main__":
    main()
