# Part 3.2 integration contract

Current implementation, reviewed October 24, 2026: Vue on `127.0.0.1:5181` proxies `/api` to FastAPI on `127.0.0.1:8012`. Default mock provider. Single-user localhost, fictional data only. Client generates UUID session and operation/request IDs. Save is explicitly selected before entry; unsaved mode remains usable without API/model/database. No browser-storage answer persistence; sessionStorage may retain an active session ID for interruption reconciliation only.

## HTTP

- GET `/api/status`: `{mode, model_id, live_configured, test_controls, question_version, policy_version}`; never a secret.
- PUT `/api/sessions/{id}/snapshot`: full `Snapshot`, returns `{session_id, revision, saved:true, result, status}`. Retry same operation id is idempotent. Older revisions409; same revision conflicting operation409. First snapshot must revision1; later may skip revision numbers if client coalesces, but never go backwards. No model wait in this endpoint.
- POST `/api/sessions/{id}/explanation`: `{revision, request_id}`. Optional `X-Peyce-Test-Fault` = `timeout|invalid|late|provider` only if server test controls enabled. Returns `{session_id, revision, request_id, mode, model_id, status, text, fragments, references, stale}`. Status `validated|fallback|obsolete`; stale responses never current. Server releases DB before bounded async provider work, then verifies same ready/revision. Request ID replay must not call provider again. Mock/live clearly distinguished.
- GET `/api/sessions`: `{sessions:[...]}` newest first. Each `{id, created_at, updated_at, exercise, status, color, result, explanation, timing}`. No hardcoded records.
- GET `/api/sessions/{id}`: full saved snapshot plus `turns`, `lifecycle`, `explanations` and metadata; useful inspectable conversation/history.
- DELETE `/api/sessions`: delete this local fictional history only (explicit UI confirmation); do not affect unrelated files.
- POST `/api/sessions/{id}/interrupt`: `{revision,operation_id}`; idempotent interrupt active/paused record only at same revision, never completed/stopped. Used best effort on pagehide/reload, no delivery guarantee.

Snapshot JSON (Pydantic validates extra fields forbidden):
```
{
 "operation_id":"uuid", "revision":1,
 "answers":[null,null,null,null,null],
 "answered":[false,false,false,false,false],
 "direct_choice":null,
 "exercise":null,
 "status":"checkin",
 "color":"pink", "color_explicit":false,
 "events":[], "timing":null
}
```
Answers integer0/1/2 or null; exactly5; answered false requires null; answered true+null is explicit skip. direct_choice/exercise null|breathing|grounding. status checkin|choice|ready|active|paused|completed|stopped|interrupted|finished. Color pink|red|pearl. Events max200: `{id:"uuid",kind:"instruction_visible|start|pause|resume|support_open|support_close|background_pause|sense_next|sense_skip|complete|stop|finish|leave",at_ms:0,active_ms:0,cause:"user|support|background|navigation|clock"}`; at_ms is session-relative monotonic span, not Unix. Optional timing `{raw_ms,counted_ms,excluded_ms,excluded_intervals:[{start_ms,end_ms,cause}],instruction_ms,finish_ms,entry_ms}`; server recomputes/validates arithmetic including union of only user-pause/support intervals. Background intervals are NOT silently excluded. Completion skill status may be completed before final Finish; final timing saved after Finish includes closing reading/decision time. A new exercise from done first finishes the prior snapshot and creates a new session (answers need not carry over).

Model approved grammar: provider chooses `reason_code` exactly matching rule, `opening_id` from `reflect|notice`, `reference_ids` drawn only from answered, policy-relevant question IDs, `closing_id` from `choice|change`. App/server inserts exact selected answer labels using fixed copy. Unknown fields/fragments/unsupported references => fallback. Different selections/references change actual acknowledgment; no unrestricted model prose. Direct-choice can use empty references and selected exercise; equal/neither references only when valid. Bounded rendered <=240 chars. Body reason references body/breathing; present reason relevant thought/present plus grounding; comfort reason only comfortable preference; both-declined only explicit refusals; equal-choice no skipped justification. Policy peyce-routing-1.0 and questions peyce-original-1.0 match existing client exactly.

Persistence uses sqlite3 with transactions/FKs, minimal schema migrations, unique operation/request IDs and revision checks. Conversation records assistant question + answer/skip only when answered, final validated assistant explanation separately sourced; invalidated revision records retained as historical/superseded. Full lifecycle events retained without duplicates. Model attempts retain safe status/provider/model/versions/selection provenance, not raw payload/credential. Restart marks active/paused interrupted, never completed. Database fault injection via `X-Peyce-Test-Fault: database` only with test flag. Failure must cause HTTP503 and frontend honest unsaved state, never block local exercise/support.

October 24 enforced boundaries:

- Any selected exercise must match the approved current rule result or an explicit direct choice; the server rejects a contradictory selection.
- For either skill, completed/finished exercise evidence requires Start before complete; finished additionally requires Finish after complete. Breathing retains its 60-second active/elapsed checks.
- Every later snapshot must contain the previously saved lifecycle as an unchanged prefix. Omission, reordering or mutation returns a conflict and rolls back that snapshot.
- Claimed exclusions must match the user-pause/support intervals reconstructed from lifecycle events, as well as pass union arithmetic. A numerically consistent invented exclusion is invalid. Instruction, pause/support and Finish events share the controller's timing offsets exactly; automatic background time is counted.
- Client history/detail requests apply only while their navigation/request context remains current. Older reads/errors cannot replace a newer response, reopen detail after Home, or restore rows after history clearing. These are client interaction guarantees, independent of provider output.

Environment: PEYCE_DB_PATH (ignored .runtime/peyce.sqlite3), PEYCE_MODEL_MODE=mock|openrouter, OPENROUTER_MODEL=nvidia/nemotron-3.5-lightning:free and OPENROUTER_API_KEY server only, PEYCE_LIVE_APPROVED_BUDGET_USD unset, PEYCE_LIVE_MAX_ATTEMPTS<=10, PEYCE_TEST_CONTROLS=0 by default. Mock is the default. Live mode requires the exact free model, available key, explicit $0 budget and verified zero input/output pricing. A configured budget is approval metadata, not a claim of exact billing control; bound calls/input/output and require verified per-model pricing before live evidence. No automatic retries. Public evidence must label live pending if missing.

Latest human steering: OpenRouter exact `nvidia/nemotron-3.5-lightning:free`, verified zero prompt/completion pricing, budget $0.00, at most ten outbound attempts including retries. No paid fallback. The catalog lacks response_format support; JSON grammar is prompted and strictly validated locally.
