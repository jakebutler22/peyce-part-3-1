# Peyce local Part 3.2 API

Peyce is pronounced **peace** (/piːs/). This is a single-user localhost coursework system with fictional data. FastAPI persists opted-in structured conversations and exercise snapshots in SQLite; a separate optional request obtains a bounded model acknowledgment. It has no accounts, clinical readiness, public deployment, production security or support-service function. Archived Part 3.1 artifacts remain separate.

## CHECK: environment and commands

The implementation used Python **3.14.7** and an isolated `backend/.venv`. The planned installation was `python3 -m venv backend/.venv` followed by that interpreter's `pip install fastapi uvicorn httpx pytest`, then `pip install python-dotenv` for explicit server-only `.env` loading. Installed and verified: FastAPI **0.156.1**, Uvicorn **0.54.0**, Pydantic **2.14.1**, httpx **0.28.1**, pytest **9.1.1**, python-dotenv **1.2.4**. `requirements.txt` pins the complete resolved environment. The native `sqlite3` module supplies parameterized SQL and transactions; there is no ORM, SDK or model-weight download.

Run these commands from the project root:

```sh
python3 -m venv backend/.venv
backend/.venv/bin/python -m pip install -r backend/requirements.txt
# Preserve any existing local configuration:
if [ ! -f backend/.env ]; then cp backend/.env.example backend/.env; fi
backend/.venv/bin/python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8012
```

Start Vue separately using `npm --prefix frontend run dev` at `http://127.0.0.1:5181`. Vite intentionally proxies `/api` to `http://127.0.0.1:8012`; the backend does not grant broad CORS access. Do not bind either server to the LAN. Stop the owned server with Ctrl+C. No server is started by imports or tests except an isolated test lifespan.

`backend/.env` is loaded explicitly with existing process variables taking precedence. Mock mode is the default and makes no external request. The default SQLite location is the absolute project-local `backend/.runtime/peyce.sqlite3`; the example's relative path assumes the root commands above. Runtime databases/journals, `.env`, dependencies and temporary evidence are ignored by Git. Never overwrite an existing `.env` during setup.

## TAKE ACTION: small integration boundary

- `app/main.py`: thin HTTP composition and safe 409/404/503 errors.
- `app/schemas.py`: strict answers, statuses, lifecycle and complete-duration arithmetic.
- `app/domain.py`: exact `peyce-original-1.0` questions and `peyce-routing-1.0` matching parity with Vue; approved phrase grammar.
- `app/repository.py`: transactions, revision/operation/request identifiers, real history and schema version 1.
- `app/explanations.py`: bounded asynchronous mock/OpenRouter adapter; it never selects a skill or changes exercise timing/support.
- `app/config.py`: server-only configuration. No credential is sent to the client or included in status/provenance.

The API and JSON shape are documented in [`../docs/part-3.2-api-contract.md`](../docs/part-3.2-api-contract.md). Saving and explanation are separate endpoints, so provider latency cannot delay the save acknowledgment or Start. The server releases database transactions before waiting for the provider, and checks the same ready revision again afterward. A replayed request never invokes a provider twice. A pending replay can return the approved fallback; a stale replay returns obsolete. The client must also reject obsolete responses when its local navigation generation changes.

`sessions` stores current lifecycle/versions/fictional context/explicit visual choice and the snapshot. `revisions` preserves committed answer/choice/result history. `operations` makes mutation retries idempotent. `turns` stores the exact assistant question and user label/skip only for received turns, with revisions; absent turns remain absent. Validated model acknowledgments are separately sourced assistant turns. `lifecycle` retains unique event IDs without duplicate completion. `explanations` records safe mode/model/prompt/question/policy versions, references, validated phrase selections, displayed text and outcome/validation category; raw provider payloads are not stored. Diagnostics retain fixed invalid-stage/finish categories, bounded HTTP/token counts, optional integer upstream code or an allowlisted network-error class; provider prose, reasoning text, headers, URLs and exception strings are excluded. Older revision turns and explanations are marked superseded in detail responses. `live_budget` persists the outbound-attempt counter independently of history deletion.

Schema migration uses SQLite `PRAGMA user_version`. Version 0 creates version 1 tables; version 1 is retained; an unknown version fails without resetting data. Transactions and foreign keys preserve relationships. Later versions require an explicit migration. API delete clears only this database's saved sessions and cascading conversation/history rows; it deliberately leaves the outbound-attempt guard intact. Retention is local until the human clears the fictional history. It is not encrypted, authenticated or a multiuser health record.

A restart marks active/paused sessions interrupted and pending explanations obsolete. It never infers completion. Best-effort `/interrupt` accepts only the matching revision and cannot replace completed/stopped/finished states. A hard crash or unload may leave the last confirmed state until restart; it does not establish an exact exit time. Interrupted inference and an explicit Stop have different meanings.

Whole-sequence timing covers the first visible instruction through the final Finish. The server checks raw span and counted/excluded arithmetic, takes the union of allowed explicit user/support intervals, and counts background pauses. Lifecycle records anchor instruction/final offsets. Browser timing is still client evidence, not a secure physiological measurement. Breathing completion requires the recorded six-cycle active duration; finishing early must use Stop rather than claim completion.

## Bounded authorized live option

The human revised the original five-call prompt limit on 2026-10-20: **OpenRouter only, `nvidia/nemotron-3.5-lightning:free` only, $0.00, at most ten outbound attempts including failures, no paid fallback.** Root verification checks current model availability and zero prompt/completion pricing before enabling it. The adapter fails closed for a different model, nonzero pricing/budget, absent approval or credential, unverified pricing, exhausted persistent cap, or provider rejection. A credential alone does not enable paid use.

Configure only `backend/.env` using the commented values in `.env.example`; never paste a credential into chat or frontend code. With the authorized exact free-model configuration present, launch a separate deliberate live run using:

```sh
PEYCE_MODEL_MODE=openrouter backend/.venv/bin/python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8012
```

`GET /api/status` reports mode, configured model, configuration completeness and persisted attempt count without a key. A genuine live call happens only on an explicit explanation endpoint request after a ready snapshot. There are no automatic retries, model lists or paid fallbacks. Requests use OpenRouter `/api/v1/chat/completions`, prompt `peyce-acknowledgment-1.1`, exactly one forced `acknowledge_current_rule` function-shaped response, disabled optional reasoning, `require_parameters:true`, `allow_fallbacks:false`, maximum provider prompt/completion price zero, at most 5,000 UTF-8 bytes for messages/function schema and 1,000 output tokens. The free request still consumes an attempt if rejected or timed out. Timeout is eight seconds by default (maximum configurable fifteen). The actual response must identify the intended model; its matching provider alias without `:free` is accepted and persisted. Missing or different identity fails closed. No other provider adapter is enabled in this run.

The current exact-model catalog does not advertise `response_format` but supports named function selection. The adapter omits the unsupported parameter and forces a single correctly named data-only function call carrying the existing grammar. It requires no accompanying prose and at most 2,000 JSON argument characters. Duplicate keys, non-JSON constants, unknown function names, extra fields or unsupported references retain fixed fallback. No external function or second provider request executes. The application enforces the full approved grammar locally before display; provider-enforced schema compliance is not claimed.

The model receives current structured question/answer-or-skip turns and the approved deterministic result. It chooses an opening/closing phrase ID and eligible current-turn reference IDs. The server rejects extra fields, wrong reason/fragment IDs, irrelevant/skipped references and overlong output before assembling <=240 characters from fixed copy and exact answer labels. Only that constructed text may display. Different selections/references affect the acknowledgment. This is constrained conversation, not counseling; course acceptance of button-led conversation remains unconfirmed. Mock and fallback are always labeled separately from genuine provider evidence.

Official implementation references checked: [OpenRouter API request format](https://openrouter.ai/docs/api_reference/overview) and [structured output and endpoint support](https://openrouter.ai/docs/guides/features/structured-outputs). Provider support can change; a request error retains fixed fallback rather than dropping constraints.

The human explicitly authorized another retry on October 25. After four observed compatibility correction cycles, **attempt 7** returned validated current-answer fragments, was displayed as Model-assisted wording, and was persisted in the same breathing session that subsequently finished. Safe diagnostics report HTTP 200, `tool_calls`, 31 completion tokens and zero reasoning tokens. Persistent usage is **7/10**, $0.00 authorization, no paid fallback. Earlier timeout/invalid/HTTP 401 results remain actual failures, not relabeled successes. [Current verification](../docs/part-3.2-verification.md) and [live evidence](../docs/evidence/3.2/live-retry-2026-10-25/) distinguish the observed success from routine mock checks and remaining limits.

## VERIFY

From the project root:

```sh
PYTHON_DOTENV_DISABLED=1 PEYCE_MODEL_MODE=mock PYTHONPATH=backend backend/.venv/bin/python -m pytest backend/tests -q
```

Tests use disposable databases and mock mode; even adapter-shape tests replace the HTTP client and never contact a provider. They compare every one of 3,072 answer/direct-choice combinations against the actual Vue policy, exercise bounded grammar and persistent free-call limits, and cover HTTP/SQLite persistence, restart interruption, stale/duplicate requests, invalid output, provider timeout/error, database failures, completion and timing arithmetic. Running tests does not count as real live-model evidence. Starlette currently emits an httpx TestClient deprecation warning; tests pass, but migration to its future httpx2 path is deferred because httpx remains the actual adapter dependency.

The October 25 expanded suite passed **86 backend tests**. New fake-HTTP checks cover strict function envelopes/arguments, actual model identity and privacy-safe diagnostics without spending another live attempt. The frontend's **46 tests and build** also pass; final submitted-source verification is recorded separately by the root.

Fault injection is off by default. Only when `PEYCE_TEST_CONTROLS=1`, `X-Peyce-Test-Fault` accepts `timeout`, `invalid`, `provider`, `late` for explanation or `database` for history requests. Late is a deliberate test-only delay before bounded mock work; it is not evidence of a real outage. Routine verification must run these with mock mode. When controls are disabled, supplied fault headers return 400. The production-default local interface has no fault UI.

The root [`../docs/part-3.2-verification.md`](../docs/part-3.2-verification.md) records the actual running-browser, SQL, model and duration observations and their remaining limits. Passing API/unit tests alone does not establish visual quality, natural usability, genuine backgrounding or the assignment's live-model criterion.
