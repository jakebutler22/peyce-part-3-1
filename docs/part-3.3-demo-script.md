# Part 3.3 demonstration and process recording guide

Peyce is pronounced **pace** (/peɪs/). Both required movies are now actual recordings, with no audio or imitated student voice. The earlier shot plan is retained below as a guide; observed chapters in this section describe what was actually captured.

- [Finished-app demonstration](evidence/3.3/video/peyce-app-demo.mp4): **3:27.47**, including all five original questions/Back, actual mock/rule/colour choice, uncut normal-speed breathing, saved history/reload/fresh Repeat, all five grounding senses, skip/direct access, support/Resume/Stop, and a clearly archival genuine model receipt.
- [Process/code screencast](evidence/3.3/video/peyce-process-screencast.mp4): **1:51.47**, showing declared expectation, actual isolated historical failure, source correction/current-state/provenance code, inputs/outputs/state/failure/separation explanation, newly executed eight-assertion API/SQLite retest and actual Git diff.

| Movie | Observed chapter start |
| --- | --- |
| App |0:00 identity;0:13 original faces/Back;0:21.55 rule/mock;**0:29.6235–1:30.2745 complete breathing Start→Finish**;1:35.86 saved history/reload;1:45 fresh Repeat;1:55.83 all-five-senses grounding;2:53.17 skip/direct;2:55.57 support/Resume/Stop;3:16.35 archival genuine receipt;3:20.97 limits. |
| Process |0:00 historical reproduction/expectation;0:05.66 observed failure;0:20.02 repair decision;0:24.76 current-state guard;0:32.09 persisted provenance;0:46.14 code inputs/state;0:53.78 outputs/failure/separation;1:13.21 current-source retest;1:15.04 eight passing assertions;1:39.39 actual diff;1:44.17 limits. |

Source is **`2f00ffb0c72826a0a2b8a8fa000eb04971e2ff53`**. Dense actual browser frames (approximately 10 fps in active shots) are assembled by acquisition timestamps; output 15 fps holds duplicate genuine frames. Six app/four process between-chapter idle cuts are labeled on screen. The 60.651 s breathing span has no cut, interpolation or speed change. Grounding in this movie uses three seconds/item; the earlier fresh-checkout whole-skill measurements 79.3108/74.0430 s used the separately documented reading/four-second-item script. Captions are outside the application in a 96 px margin. Full streams decode; actual public media playback/seeking and anonymous download bytes are checked in the [recording index](evidence/3.3/recordings.json). GitHub blob pages do not preview these MP4s inline; download/open the MP4 or use the separate player. No hosted player or student personal review is claimed.

The process movie is **a controlled historical replay**, not newly discovered failure footage: archived source `2cc923846654e1492cea4f82494c4f4874674532` is extracted to a temporary directory with new SQLite; network and real credentials are prohibited. Four provenance expectations fail in the old result. The actual submitted-source retest passes 8/8 at the same artificial cap. This smaller reproduction starts at 10 directly; it is distinct from the original 16-case runner’s simulated 9→10 sequence. The real exhausted 10/10 ledger is never opened by this viewer. Recording generates no new provider request; the saved Model-assisted ready receipt is explicitly dated/archival.

Capture the localhost application and only necessary redacted developer evidence. Use fictional inputs and mock mode by default. Show source labeling honestly: Mock wording, Local fallback, or an explicitly identified saved genuine live receipt. Do not trigger a fresh provider call merely to record a screen, expose configuration/credentials, call support resources, imitate the student’s voice, or claim personal student narration/review.

## A. Finished-application demonstration

| Shot order | Actual action to record | Caption / explanation | Required visible evidence |
| --- | --- | --- | --- |
| A1 — identity and choices | Open Peyce; show the white/light-pink entry, bow and save choice | “Peyce, pronounced pace. Fictional localhost coursework. No person is monitoring.” | App running; Find an exercise, direct exercise choice, support and opt-in saving. |
| A2 — optional original check-in | Choose saving; start check-in. Use body=`Hard right now`, thought=`Easy`, present=`Present`, breathing=`Comfortable`, grounding=`Comfortable`. Briefly demonstrate Back/correction or a clearly separate Skip example. | “Five original optional questions. Selecting a face advances; Back and skipping remain available. These are not STAI or a diagnosis.” | Actual labeled SVG faces, notice, progress, automatic advance, correction/skip control. |
| A3 — rule and acknowledgment | Observe breathing ready and its genuine current source label; select an explicit balloon color | “The application chose this transparent rule result. Optional wording can acknowledge it but cannot change the skill, timing or support.” | Exact current reason, honest Mock/Model-assisted/Local-fallback label, Start and alternative simultaneously usable. |
| A4 — full normal-speed skill | Deliberately Start breathing and record all six 4/6 cycles continuously through completion, then Finish | “Six cycles: four seconds in, six out; no hold. A comfortable unforced breath. The balloon shows rhythm, not measured breathing.” | At least one full 60-second real-time skill, matching cue/balloon, Pause/Stop/support, immediate neutral completion and deliberate Finish. Do not speed up or cut this required complete skill. |
| A5 — history and reload | Open the actual saved session, then reload; show the same confirmed record and explicit preference | “History is real local SQLite data. Current answers appear once; earlier revisions and acknowledgment provenance remain inspectable.” | Dates, skill, finished/stopped status, current selected labels, source/model/version receipt and stored color. Never pass static fixtures off as runtime records. |
| A6 — repeat and current control | Use completed-session Repeat (or its final equivalent); show new ready state and new session evidence; change the current exercise or color if desired | “Repeat is optional. It creates today’s new session; it does not infer today’s feelings or reuse old timing, completion or wording.” | New session identity/lifecycle, default-ready state and current alternative; no old model output labeled new. |
| A7 — grounding | Choose grounding; show 5 seen → 4 felt → 3 heard → 2 smelled → 1 tasted, private noticing and one Next per sense | “No need to type, eat, drink or find an unavailable sensation. Back, skip, pause and stop remain available.” | All five senses and quantities in order; completion/stop status honestly retained. If this section is edited, label every time jump. |
| A8 — independent support | Open support from an exercise or history; close without activating any resource | “Local support information is independent of the provider and these answers. No person is monitoring this app.” | Region label, no-monitoring copy, reachable resources, focus/close behavior; practice requires deliberate Resume after support. |
| A9 — limits and evidence | Show the final report/evaluation entry and current mode | “These fictional scripted checks do not establish clinical benefit, real-person timing or full accessibility conformance.” | Real evidence/recording links and exact current build/source reference; no Canvas-submission or grade claim. |

Do not hide ordinary instruction/transition/closing time when discussing duration. Record entry/check-in separately. Only explicit user pauses and support intervals may be excluded from the counted skill span, with overlap counted once. The video duration and app’s measured sequence are different quantities; report each from its actual evidence.

## B. Process screencast

The strongest current narrative is the **actual S17 failure and correction**, reproduced only with a disposable fixture ledger and prohibited real transport:

1. Open [the predeclared fixtures](../backend/tests/fixtures/evaluation-3.3.json) at S17. State the expected cap behavior: validated mock wording, mock label, no dispatch and unchanged cap.
2. Open [the preserved initial-failure receipt](evidence/3.3/deterministic-initial-failure.json). It reports `mode=openrouter` / `status=fallback` at the simulated ten-attempt cap. Caption this as the actual initial controlled API/SQLite result; do not stage a genuine provider request or claim that the real ledger reached ten here.
3. Show the actual diff in `backend/app/explanations.py`: specific `LiveLimitReached` before dispatch and its dedicated mock-construction catch, plus the repository’s persisted provenance update. Explain that suppressing network activity was already correct, but source labeling was wrong.
4. Run the existing deterministic runner in its network-prohibited temporary databases or show its real terminal result. Open [run 1](evidence/3.3/deterministic-run-1.json) and [run 2](evidence/3.3/deterministic-run-2.json), navigate to S17 and B3, and show the same repeat signature. State explicitly that these are API/SQLite outcomes; they do not prove UI accessibility or real skill duration.
5. Show `backend/tests/test_evaluation.py` and S17 in `run_evaluation.py`: the assertions check mock mode/provenance, no extra dispatch, retained counter and repeatability. End with the unchanged active $0/ten-total authorization; fixture counters are not used to bypass it.

The controlled save-failure sequence below is another recording-ready option if its actual browser/network/SQL evidence is captured. The S17 option above has now been recorded; the save-failure alternative remains a guide, not newly captured footage.

Choose **one actual observed failure** in the final evaluation. A controlled mock fault is valid if visibly labeled. The alternative sequence below remains a ready candidate, not a claim that this save-failure sequence was recorded or happened in a new live provider request:

1. Show the baseline expectation: a saved session appears only after a committed snapshot receipt. Show the specific scenario’s expected result before running it.
2. In a disposable fictional database with local test controls enabled, reproduce a database-write failure. Keep the browser at ready/practice, show “Not confirmed saved,” and demonstrate that Start/Stop/support still work. Show the actual 503/network or test evidence; hide unrelated desktop/configuration.
3. Inspect the redacted evidence: failed write, unchanged row count or absent partial session, exact operation/session ID, and the controller’s pending/error state. Do not expose a runtime database containing unrelated material.
4. Explain the resulting decision and relevant actual scoped code change. If the code predates this run, clearly identify its historical date/commit and show its real diff; do not manufacture a new edit. For a newly discovered failure, show the actual failing expectation and smallest in-scope fix.
5. Remove the controlled fault and use Retry saving. Show actual browser acknowledgment, the committed SQLite rows, and the targeted regression result. Confirm one logical session/event sequence rather than duplicate retries. Keep the initial failure and retest evidence.
6. Show the code explanation below and the exact test supporting it. End with the limitation: a recovered local write is not a production reliability/security claim.

An alternative supported by historical evidence is the October 25 adapter-format failure. Show the original safe receipts and dated diff: HTTP 200 with all 1,000 tokens used on reasoning/truncation, then invalid content JSON, then the validated named `acknowledge_current_rule` response. Label this archival evidence and use a controlled reproduction if showing it dynamically. Do not consume calls or claim a current outage simply to restage the story.

## Generated-code explanation tied to the repository

### `backend/app/explanations.py` — cap-specific mock provenance

For the S17 process narrative, show `LiveLimitReached`, the reserve-before-dispatch condition and the dedicated `except LiveLimitReached` branch in `ModelService.explain()`.

- **Inputs:** a committed current snapshot, approved rule result, request/session/revision identity and the repository’s durable attempt-reservation result. The fixture uses its own disposable counter and disables real transport.
- **Outputs:** when reservation fails, approved mock fragments, rendered bounded text, `mode=mock`, `model_id=peyce-mock-1.0`, `status=validated`, and `validated-mock-live-limit` persistence provenance. No HTTP request is sent. Other provider errors retain their own fallback handling.
- **State/data flow:** the adapter asks the repository to reserve before constructing an outbound request; the specific exception selects the honest mock path; normal fragment rendering and repository finish/revision checks still apply. The frontend derives its source label from the returned mode/status, so correct backend provenance prevents a false live label.
- **Why here:** the adapter knows whether transport was allowed and which source produced the wording. Routing, Stop, support and timers remain in the application/controller. A general permission error must not silently masquerade as a validated live response.
- **Demonstrating test:** S17 and `backend/tests/test_evaluation.py` assert the returned/persisted mock source, unchanged ceiling and no extra dispatch, then rerun for the matching signature. The initial failure is retained separately instead of changing expectations to the old output.
- **Limit:** this simulated ceiling check proves that controlled branch and its SQL receipt, not free-endpoint availability, actual live variation or natural-human benefit.

### `frontend/src/sequence.js` — `SequenceTimer`

Show this actual file beside [its tests](../frontend/tests/sequence.test.js). It is compact enough to read on screen and connects directly to R1 and pause/support control.

- **Inputs:** one session-relative monotonic timestamp when instructions first appear; `exclude(cause, at)` and `include(cause, at)` for explicit user pause/support; a final `finish(at)`. Ordinary reading/Start/closing time and background downtime remain in the measured span.
- **Outputs:** one stable result containing raw, counted and excluded milliseconds; interval records; instruction/Finish offsets; separate entry time. Calling Finish twice returns the first result rather than extending a finished record.
- **Data flow:** `usePrototype.js` samples `performance.now()` relative to the current session anchor, records the same boundary in lifecycle events, and calls this timer. A snapshot sends its result to FastAPI; backend schema/domain/repository validation checks timing and saved lifecycle relationships before SQLite commit.
- **Why this component:** whole-sequence accounting is separate from `clock.js`, which controls the six breathing phases. The view renders cues and controls, the controller handles deliberate actions, and this small model computes interval arithmetic. No provider response can change the clock or subtract time.
- **Overlapping intervals:** `finish()` clips intervals to the instruction→Finish span, sorts them by start, and advances `edge`. Only the uncovered part beyond `edge` adds to excluded time. A support interval inside a pause therefore cannot be subtracted twice.
- **Concrete test:** `overlapping user/support intervals are subtracted once; background has no exclusion` supplies instructions at 1,000 ms, user pause [5,000,10,000], support [7,000,12,000], Finish 21,000. Raw is 20,000 ms; the union [5,000,12,000] is 7,000 ms; counted is 13,000 ms. These are accelerated logic-test values, not a measured wall-clock skill duration.
- **Failure boundary:** this class computes arithmetic; it cannot prove the UI events are genuine. Server checks reject invented exclusions/lifecycle mutations, and actual browser wall-clock checks establish the reported durations. Show the relevant observed result without claiming a unit test alone proves usability.

### Optional companion: `frontend/src/api.js` — `SaveQueue`

For the controlled-save-failure narrative, show `enqueue(payload)`: it captures a structured clone, chains writes in order, catches the previous failure before starting a later job, and returns the current job’s promise. The controller labels Saved only after that promise resolves for the current revision. Retrying keeps the original logical operation ID, while the server’s operations table makes a replay idempotent. The test `save queue captures values, preserves order and recovers after a failed write` demonstrates that mutating the caller’s revision after enqueue does not change the captured payload, and a rejected first write does not poison the second. The queue itself is not proof of persistence; the HTTP receipt and actual SQLite query supply that evidence.

## Capture acceptance checklist

The real recording index must establish: files exist and open/play; duration and normal-speed skill coverage; readable captions/code; truthful mock/live/archive labels; no credentials/private desktop; public reviewer access without the local login; actual chapters/timestamps; the controlled or genuine failure, evidence, decision/change and retest; and the on-screen code explanation. If capture is technically unavailable, mark the mandatory recording requirement incomplete and retain this exact shot list plus the running local app. Do not relabel this guide as a video.
