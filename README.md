# Peyce · Part 3.2

Peyce is pronounced **peace** (/piːs/). It is a single-user localhost Vue → FastAPI → SQLite coursework application for **fictional use only**. Complete a gentle breathing sequence or private 5/4/3/2/1 grounding, choose whether to save the structured conversation/actions, and inspect acknowledged sessions in real SQLite-backed history. No person is monitoring it; it is not a support service. **Stop after Part 3.2.**

The model has a small optional role: choose approved acknowledgment fragments/references for the current deterministic result. It cannot choose a skill, diagnose, score, change timing or control support. **A genuine live contribution was validated and displayed on October 25:** the seventh authorized OpenRouter attempt supplied current-answer references and approved phrase IDs, which the application validated, rendered and persisted. The interface showed Model-assisted wording. Earlier provider/format failures remain separately recorded; the persistent total is **7/10 attempts**, within the **$0.00** authorization. The service was returned to default **mock mode**, restarted to verify durable history, then stopped after verification. [Verification](docs/part-3.2-verification.md) records the result, actual revisions and remaining limits.

## Run locally

Verified environment: Node **24.12.0**, npm **11.6.2**, Python **3.14.7**. Python and frontend dependencies are pinned. From this project root:

```sh
python3 -m venv backend/.venv
backend/.venv/bin/python -m pip install -r backend/requirements.txt
npm --prefix frontend ci
if [ ! -f backend/.env ]; then cp backend/.env.example backend/.env; fi
```

Start the mock backend in one terminal:

```sh
PEYCE_MODEL_MODE=mock backend/.venv/bin/python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8012
```

Start Vue in another:

```sh
npm --prefix frontend run dev
```

Open `http://127.0.0.1:5181/`. Vite proxies `/api` to the loopback backend; no wide CORS or hosted deployment is configured. The ports are strict: inspect a conflict rather than stopping an unrelated service. Stop only your owned terminals with Ctrl+C; the same commands restart them. The archived direct-file HTML export is a Part 3.1 artifact, not the Part 3.2 running stack. Do not rerun its export script over the archived submission.

For routine verification:

```sh
PYTHON_DOTENV_DISABLED=1 PEYCE_MODEL_MODE=mock PYTHONPATH=backend backend/.venv/bin/python -m pytest backend/tests -q
npm --prefix frontend test
npm --prefix frontend run build
```

The October 25 adapter review passed **86 backend tests**, **46 frontend tests**, and the build; routine tests use mocks/fake HTTP. The new **live-model** breathing session completed all six cycles, Finish and SQLite-backed history in **88.6376 seconds** from first instructions, with **zero exclusions**; entry/check-in was **6.3333 seconds** separately. [Live timing/events](docs/evidence/3.2/live-retry-2026-10-25/live-timing.json) and [saved provenance](docs/evidence/3.2/live-retry-2026-10-25/live-validated-session.json) preserve that actual result. Earlier browser checks covered four simulated viewports, SQLite history, injected faults, real reload/restart and a stopped-backend outage; support and unsaved practice remained available. The October 24 **mock** 83.1024-second run and October 20 88.1449-second run remain separately dated. These scripted results include tool/decision overhead and are not natural-human timing or clinical evidence. See [current verification](docs/part-3.2-verification.md) for assumptions and remaining limits.

## Configuration, history and failure behavior

The ignored server-only `backend/.env` loads without overriding existing process variables. Never overwrite an existing configuration or put a credential in Vue, a URL, Git or chat. The secret-free [example](backend/.env.example) documents the settings. Default history is the ignored `backend/.runtime/peyce.sqlite3` (schema version 1). Choose saving before entry; unsaved use remains available without an API/model/database. Saved labels follow acknowledgments. Failed writes show an honest unconfirmed state and leave Start/Stop/support available.

History is actual SQLite data, with an empty state when nothing is saved. It records exact questions/answer labels/explicit skips, revisioned choices and approved rule results, lifecycle events, explicit balloon preference, whole-sequence timing and separately sourced model provenance. No hidden anxiety score or model-inferred clinical state is stored. Records remain locally until **Past sessions → Clear saved history → Yes, clear history**. That action clears related session records but retains the outbound-call guard. The database is not encrypted/authenticated and is not a production health record. Tests always use disposable databases.

Explicit Stop remains stopped. Completion requires the final exercise transition; closing Finish is timed separately. Refresh/restart cannot manufacture completion: best-effort recovery and backend restart label unfinished active/paused records interrupted. A hard close cannot guarantee an unload write or an exact departure time.

The human's revised live authorization is **OpenRouter, exact `nvidia/nemotron-3.5-lightning:free`, $0, maximum ten outbound attempts including failures**. There is no paid fallback or automatic retry. [Backend setup](backend/README.md#bounded-authorized-live-option) describes deliberate live mode, current pricing verification, credential handling, timeout and persistent call cap. Provider output must pass the strict application-controlled fragment grammar before any wording is displayed. Native provider schema enforcement is not claimed for this model. A failed live call remains labeled local fallback; [verification](docs/part-3.2-verification.md) reports actual live attempts/results.

Test faults are disabled by default. For a deliberate local mock check, set `PEYCE_TEST_CONTROLS=1` on the backend and open the development URL with `?verify`; its labeled controls inject save/provider/invalid/timeout/late faults. They are controlled tests, not genuine outages. Never use them to manufacture live evidence.

## Current artifacts

| Artifact | Contents |
| --- | --- |
| [Part 3.2 implementation](docs/part-3.2-implementation.md) | MVC/service boundaries, data/state/model contracts, R/D tradeoffs, changes and limits |
| [Part 3.2 verification](docs/part-3.2-verification.md) | Actual commands, expected/observed checks, timing, SQL, browser/live distinction and pending gates |
| [API contract](docs/part-3.2-api-contract.md) / [backend setup](backend/README.md) | Callable routes, strict snapshots, mock/live configuration and persistence policy |
| [Part 3.2 evidence](docs/evidence/3.2/) | New integrated screenshots, safe fictional SQL/session/timing and provider evidence |
| [October 24 review](docs/evidence/3.2/review-2026-10-24/audit.md) | Dated mock timing, pause/support overlap, save recovery, navigation fixes and the model blocker that remained then |
| [October 25 live retry](docs/evidence/3.2/live-retry-2026-10-25/outcome.md) | Free-model catalog, actual failed approaches, validated live wording, complete live timing and durable history; previous mock timing is not relabeled live |
| [AI use](AI-USE.md) / [evidence log](docs/evidence-log.md) / [handoff](handoffs/current.md) | Actual assistance, revised approaches and active stop boundary |

The instructor-facing single `submissions/3.2/report.md` is packaged after the verified source/evidence commit, so it can cite a real immutable source SHA. Source publication and a generated report do not establish a guaranteed grade, student personal review or Canvas submission.

## Preserved Part 3.1 research/design

| Historical artifact | Contents |
| --- | --- |
| [Part 3.1 report](submissions/3.1/report.md) / [clickable HTML](submissions/3.1/prototype.html) | Archived submission and immutable source/evidence; historical pronunciation is preserved |
| [Design pipeline](docs/design-pipeline.md) / [flow SVG](docs/flow.svg) | Composition, routing examples, original MVC/model plan and R/D reasoning |
| [Research ledger](docs/research.md) / [assignment provenance](docs/assignment-source.md) | Source access/licensing/inference limits and supplied milestone interpretation |
| [Part 3.1 verification](docs/verification.md) | Historical observations/screenshots, not new backend/model evidence |
| [Asset provenance](docs/assets/provenance.md) / [font licenses](docs/assets/font-licenses.md) | Original bow/balloon and licensed local fonts; approximate inflation/recoloring limits |

Five original optional face questions remain exact and versioned; they are not STAI or a validated assessment. Matching is a private design heuristic: current choice/refusal/unknown answers and support outrank a suggestion. Quiet decoration, generous controls and one-task screens remain design choices, not evidence of clinical benefit. A genuine hidden-tab/return round trip, physical held-key repeat, real-device/screen-reader use, natural usability, instructor acceptance of button-led conversation and student personal review remain limits. One validated live contribution establishes the model integration for the observed case; it does not establish reliability across every case or resolve those human/accessibility limits. No accounts, training, production persistence, deployment, support service or Part 3.3 evaluation is added.

The independent root is `/Users/jakebutler/Documents/ChatGPT/mental health vF`. The previous `Mental Health` repository remains read-only; its Git history/private data are not reused. Part 3.1 submission files and immutable history are preserved.
