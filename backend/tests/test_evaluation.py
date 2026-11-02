"""The predeclared scenario supplement uses isolated SQLite and mock transport."""
from run_evaluation import MATRIX, run_suite


def test_part33_matrix_predeclares_eighteen_distinct_cases_and_exact_selections():
    assert [case["id"] for case in MATRIX["scenarios"]] == [f"S{i:02}" for i in range(1, 19)]
    assert [check["id"] for check in MATRIX["behaviors"]] == ["B1", "B2", "B3"]
    for case in MATRIX["scenarios"]:
        assert case["initial_state"] and case["actions"] and case["expected"]
        for selected in case["inputs"]:
            assert len(selected["selections"]) == len(selected["answers"]) == len(selected["answered"]) == 5
            assert [item["question_id"] for item in selected["selections"]] == ["body", "thought", "present", "breathing", "grounding"]


def test_part33_api_sql_scenarios_cross_case_invariants_and_repeatability():
    first, second = run_suite(), run_suite()
    assert first["repeat_signature"] == second["repeat_signature"]
    assert first["summary"]["api_scenarios_passed"] == 16
    assert first["summary"]["scenarios_requiring_controller_gui"] == ["S09", "S18"]
    assert first["summary"]["api_cross_case_assertions_passed"] == 2
    assert first["summary"]["real_network_calls"] == 0
    capped = next(case for case in first["scenarios"] if case["id"] == "S17")["observed"]
    assert capped["after_cap_mode"] == capped["persisted_mode"] == "mock"
    assert capped["final_attempts"] == 10 and capped["simulated_transport_calls"] == 1
