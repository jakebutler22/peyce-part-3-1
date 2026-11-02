# Peyce · Part 3.3

Peyce is pronounced **pace** (/peɪs/). It is a single-user localhost **Vue → FastAPI → SQLite** coursework application for fictional use. Five optional original face questions lead to a transparent suggestion or deliberate choice, then paced breathing or private 5/4/3/2/1 grounding. Saving is optional. No person is monitoring it; it is not a deployed support service.

The application/evaluation and clean-checkout gate pass at runnable source [`2f00ffb`](https://github.com/jakebutler22/peyce-part-3-1/tree/2f00ffb0c72826a0a2b8a8fa000eb04971e2ff53): **88 backend tests, 60 frontend tests and build**, **18 fictional scenarios** with actual GUI variants, repeatable **16-case API/SQLite** checks, and B1–B3 assertions. Fresh-checkout normal-speed mock skills measured **79.3108 s breathing / 74.0430 s grounding**, instructions through Finish, zero exclusions; entry **6.4611/6.2417 s** is separate. Three newly validated live requests included one body context repeated twice and one grounding contrast; cumulative allowance is **10/10**, $0, no retries/paid fallback. [Evaluation](docs/part-3.3-evaluation.md) separates every layer and earlier timings. **Both mandatory recordings remain missing** because available tools could not control the capture toolbar; [the script/code explanation](docs/part-3.3-demo-script.md) is not a video. This is the outstanding required gate, so Part 3.3 is not fully complete. No Canvas submission is claimed.

## Run locally in mock mode

Recorded project environment: Node **24.12.0**, npm **11.6.2**, Python **3.14.7**. Dependencies are pinned in `backend/requirements.txt` and `frontend/package-lock.json`. From the project root:

```sh
cd "/Users/jakebutler/Documents/ChatGPT/mental health vF"
python3 -m venv backend/.venv
backend/.venv/bin/python -m pip install -r backend/requirements.txt
npm --prefix frontend ci
```

A fresh checkout uses its own clone path in the first command. Mock operation needs no credential or `.env` file. Start the backend in one terminal:

```sh
PYTHON_DOTENV_DISABLED=1 PEYCE_MODEL_MODE=mock PEYCE_DB_PATH=backend/.runtime/peyce.sqlite3 backend/.venv/bin/python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8012
```

Start Vue in another terminal from the same root:

```sh
npm --prefix frontend run dev
```

Open `http://127.0.0.1:5181/`. `GET http://127.0.0.1:8012/api/status` reports safe mode/version information. Vite proxies `/api` to loopback FastAPI. Neither command deploys a service. Ports are strict: inspect a conflict and stop only owned processes with Ctrl+C. The same commands restart them. Do not overwrite an existing ignored `backend/.env`; the explicit mock command disables dotenv loading and provider use.

The Part 3.1 direct-file HTML export is archived design evidence. Do not rerun its exporter over that submission. [Actual clean-checkout evidence](docs/evidence/3.3/clean-checkout.json) verifies the README setup at source `2f00ffb0c72826a0a2b8a8fa000eb04971e2ff53` in a separate managed checkout, with sanitized mock environment and no copied `.env`, key, database, virtual environment or modules. Pinned pip installation and `npm ci` (36 packages) succeeded; tests/build passed, five tracked art/font routes returned 200 with matching bytes, and two browser-completed saved flows had no foreign-key errors or provider attempts. This is an agent reproducibility check, not an independent human study.

## Repeatable checks

```sh
PYTHON_DOTENV_DISABLED=1 PEYCE_MODEL_MODE=mock PYTHONPATH=backend backend/.venv/bin/python -m pytest backend/tests -q
npm --prefix frontend test
npm --prefix frontend run build
```

The standalone fictional evaluation runner uses disposable databases and prohibits real provider transport:

```sh
PYTHON_DOTENV_DISABLED=1 PEYCE_MODEL_MODE=mock backend/.venv/bin/python backend/tests/run_evaluation.py --output docs/evidence/3.3/deterministic-local.json --run-label local-repeat
```

The frozen-source [final run 1](docs/evidence/3.3/final-deterministic-run-1.json) / [final run 2](docs/evidence/3.3/final-deterministic-run-2.json) explicitly match source `2f00ffb` and signature `40c3018a01404a5b91d56ef90bada849b4a45258244faf8de941413c8b39c9f3`: 16 API/SQLite cases pass, S09/S18 remain outside that layer, and no real network or wall-clock claim is made. Earlier working-tree runs remain preserved separately. The fixture declares expectations before execution. [Actual GUI observations](docs/evidence/3.3/gui-observations.json), separate SQL readback and cross-case UI checks complete the coverage rather than relabeling fixtures as UI evidence.

An actual initial **S17 failure** is preserved: at the simulated live-call ceiling, dispatch was blocked but the result was labeled OpenRouter fallback rather than mock. The corrected cap path returns a validated, honestly labeled mock without an outbound request. [Initial failure](docs/evidence/3.3/deterministic-initial-failure.json) and both retests retain the change. Tests never reset or use the real runtime/provider ledger.

## History, personalization and privacy

Saving is explicitly selected before entry; unsaved practice works without FastAPI/model/SQLite. The ignored default database is `backend/.runtime/peyce.sqlite3`, schema version 1. Only acknowledged writes display Saved; pending/failed saves stay visibly unconfirmed and leave exercises, Stop and support usable. Retry retains logical operation IDs so an accepted write cannot be duplicated simply by replaying it.

History contains actual SQLite sessions, understandable dates, exercise/status, current exact question/answer-or-skip records, revision audit, lifecycle/timing and separately labeled acknowledgment provenance. It does not contain a total anxiety score or model-inferred clinical profile. Current answers appear once; earlier snapshots remain expandable. Stop remains stopped. Reload/restart reconcile unfinished active/paused records as interrupted rather than inventing completion; abrupt-close delivery is best effort.

An explicitly selected balloon colour is also remembered as one allowed colour enum in browser local storage (`peyce-balloon-color-v1`), separately from session/answer data. It can work during unsaved use; storage failure is reported. **Repeat this exercise** appears for a finished saved skill and creates a fresh session with no previous answers, model output, timing or completion. Saving for the new visit remains optional. History never determines today’s feelings or overrides the current choice/refusal.

Records remain locally until **Past sessions → Clear history and colour → Yes, clear history and colour**. Cancel preserves them. Confirmed clearing removes related SQLite session data and the remembered colour, while retaining the outbound-call guard. A browser-storage clearing failure is reported. This is unencrypted, unauthenticated single-user coursework storage, not a production health record or secure-erasure guarantee.

## Model and safety boundaries

The optional model selects only approved acknowledgment fragments/current-answer references for the deterministic result. It cannot select a skill, diagnose, score, invent exercise instructions, change timing, resume a stopped exercise or control support. Current prompt version is **`peyce-acknowledgment-1.2`**; the pronunciation changed to pace while retaining the proven single named `acknowledge_current_rule` data contract. No arbitrary function or follow-up provider call executes. The application validates exact fields/references and constructs bounded wording; native provider schema compliance is not claimed.

Mock is the default for setup, tests, clean checkout and peers. The human’s stricter live authorization remains **OpenRouter only, exact `nvidia/nemotron-3.5-lightning:free`, $0.00, at most ten cumulative generation attempts including failures**, with finite bounds, no automatic retry or paid substitution. The November 2 ledger advanced **7→10/10** for the [three validated live observations](docs/evidence/3.3/live-variation.json), after [fresh zero-price preflight](docs/evidence/3.3/provider-preflight.json). **No generation attempts remain.** Do not reset the ledger through a new database/checkout or use the broader peer ceiling to bypass it. Keep credentials server-only, ignored and out of logs/chat/recordings. The existing [backend setup](backend/README.md#bounded-authorized-live-option) describes the adapter, but its October 25 counts are historical; routine use must remain mock.

Two independent same-body requests produced identical approved fragments/text at 0.885877/0.565010 s; the single attention contrast used thought/grounding references at 0.583934 s. All used prompt 1.2, temperature 0.2 and the same bounded function contract. Actual saved-history UI displayed Model-assisted provenance. These are ready-state requests, not completed exercises, and the tiny sample establishes no general reliability or clinical benefit.

The genuine October 25 contribution is preserved at [source/evidence `2cc9238`](https://github.com/jakebutler22/peyce-part-3-1/tree/2cc923846654e1492cea4f82494c4f4874674532): one validated live case and **88.6376-second** breathing sequence, zero exclusions, **6.3333-second** entry/check-in separately. Its ten-second reading and eight-second closing waits were script decisions, not application-imposed delays. It does not satisfy the new repeated-live or both-skill timing gates by itself.

Support content is local and independent of answers/provider/database. The clearly labeled dialog states no person is monitoring; no risk classifier or red-face crisis inference exists. Do not activate emergency resources during testing. Original faces, quiet satin/latex assets, fixed 4/6×6 breathing, private 5/4/3/2/1 grounding and reduced motion remain. This is not STAI or a validated treatment recommendation.

Test faults are off by default. For deliberate mock-only reproduction, enable backend `PEYCE_TEST_CONTROLS=1` and open the development URL with `?verify`; the labeled controls inject save/provider/invalid/timeout/late faults. Controlled faults are never evidence of a genuine provider outage.

## Artifact index and preserved milestones

| Artifact | Contents |
| --- | --- |
| [Part 3.3 design review](docs/part-3.3-design-review.md) | Original choices, alternatives, dated evidence, decisions, costs and R1–R4/D1–D6 mapping |
| [Part 3.3 evaluation](docs/part-3.3-evaluation.md) | Eighteen scenario outcomes, B1–B3 assertions, wall-clock skill observations, live repetitions and limits |
| [Clean checkout](docs/evidence/3.3/clean-checkout.json) / [clean GUI](docs/evidence/3.3/clean-gui.json) | Exact frozen source, sanitized fresh setup, actual completed skills/SQL, assets and commands |
| [Part 3.3 recording guide](docs/part-3.3-demo-script.md) | Exact app/process shots and actual generated-code explanation; no video claimed |
| [Part 3.3 evidence](docs/evidence/3.3/) | Baseline, initial failures/retests, repeated deterministic results, actual GUI/screenshots/SQL, genuine live variation |
| [AI use](AI-USE.md) / [evidence log](docs/evidence-log.md) / [handoff](handoffs/current.md) | Tool roles, dated changes and actual current status |
| [Part 3.2 report](submissions/3.2/report.md), [implementation](docs/part-3.2-implementation.md), [API contract](docs/part-3.2-api-contract.md), [verification](docs/part-3.2-verification.md) | Preserved historical integrated milestone and October 25 genuine live success; earlier “peace” pronunciation remains historical |
| [Part 3.1 report](submissions/3.1/report.md), [design pipeline](docs/design-pipeline.md), [flow](docs/flow.svg), [research](docs/research.md), [assignment source](docs/assignment-source.md) | Preserved original design/research, not new integration evidence |
| [Assets](docs/assets/provenance.md) / [fonts](docs/assets/font-licenses.md) | Original generated cutouts, licensed local fonts and deformation/recolouring limits |

One final `submissions/3.3/report.md` will identify the real submitted source/evidence and later packaging commit, requirement outcomes and accessible recordings or their precise unmet status. No self-referential future SHA, guaranteed grade or Canvas submission is implied.

The independent project is `/Users/jakebutler/Documents/ChatGPT/mental health vF`, continuing [jakebutler22/peyce-part-3-1](https://github.com/jakebutler22/peyce-part-3-1). The repository’s historical name/history are retained. Older Mental Health/Expedia-lite projects and archived submissions remain outside this work. Physical devices, screen readers, natural-human usability, clinical effectiveness, instructor acceptance of constrained conversation and the student’s personal source/report review are not established by agent checks. Stop after the authorized Part 3.3 package; no support-service deployment.
