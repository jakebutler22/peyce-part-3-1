# Deterministic evaluation layer notes

The predeclared inputs, exact labels, initial states, actions and expectations are in `backend/tests/fixtures/evaluation-3.3.json`. They were saved before the scenario runner was executed. The fixture includes all eighteen S01–S18 cases and the three behavior-check mappings.

The API/SQLite supplement runs sixteen cases. S09 and S18 concern local unsaved controls, keyboard/layout and motion, so its outputs explicitly mark them **not evaluated at the API layer**. B2 and B3 have executable cross-case helpers in `backend/tests/run_evaluation.py`. B1 is a local controller/UI property; the runner points to `assertSupportAccess` and the B1 tests in `frontend/tests/personalization.test.js`. The separate controller suite covers B1/B2 and personalization with mocked transport. Actual GUI observations remain separate.

Synthetic lifecycle offsets test arithmetic, state transitions and database relationships; they do not establish actual skill duration, visible sense order, phase/balloon synchronization, focus, viewport quality or physical-key behavior. A recreated FastAPI lifespan is labeled as such and does not establish a real process restart. The root evaluation supplies browser, process and real-wall-clock evidence.

Commands run from the repository root, using the existing backend virtual environment:

```sh
PYTHONPATH=backend PYTHON_DOTENV_DISABLED=1 PEYCE_MODEL_MODE=mock backend/.venv/bin/python -m pytest -q backend/tests
PYTHON_DOTENV_DISABLED=1 PEYCE_MODEL_MODE=mock backend/.venv/bin/python backend/tests/run_evaluation.py --output docs/evidence/3.3/deterministic-run-1.json --run-label run-1
PYTHON_DOTENV_DISABLED=1 PEYCE_MODEL_MODE=mock backend/.venv/bin/python backend/tests/run_evaluation.py --output docs/evidence/3.3/deterministic-run-2.json --run-label run-2
```

No dependency was installed for this runner. `.env` loading is disabled; every scenario gets a temporary disposable database. Accidental asynchronous provider dispatch fails the suite. S17 replaces the transport with a local fixture, simulates the 9→10 boundary, and proves that subsequent requests produce an honestly labeled mock without another dispatch. This does not spend or reset the real ledger.

The unchanged baseline passed 86 backend tests. The isolated initial S17 failure is preserved in `deterministic-initial-failure.json`: the ceiling suppressed dispatch but returned an OpenRouter fallback. The correction switches the response **and persisted provenance/source** to the existing validated mock construction. It preserves the ledger through replay and history deletion. Active pronunciation is now pace (/peɪs/), with prompt version `peyce-acknowledgment-1.2`; archived 1.1 evidence is unchanged.

After the correction, 88 backend tests passed. Two standalone runner executions each produced sixteen API-layer passes, zero API failures, two API behavior-check passes, and the same normalized repeat signature. UUIDs and database timestamps are checked within each scenario but excluded from the normalized observations. The JSON context records the base Git HEAD, whether application files match that HEAD, and their actual hashes; an uncommitted working tree is not presented as a clean source commit. The final package must pin these files to its verified source.

The existing Starlette/httpx test-client deprecation warning remains; it did not fail these checks. No live-model reliability, human participation, clinical benefit or completed GUI evaluation is inferred from this supplement.
