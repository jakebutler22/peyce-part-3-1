# Peyce — Part 3.3 submission

Peyce is pronounced **pace** (/peɪs/). This report covers fictional localhost coursework, not a deployed support service.

**Status: application, evaluation, design review, documentation and clean-checkout verification completed; required finished-app and process recordings are incomplete.** Available browser tools expose screenshots only, and the native recording action did not provide a controllable capture toolbar. This blocker was reported early. Scripts and screenshots below are not videos. Full fulfillment or a guaranteed grade cannot be claimed while this required item is missing.

Repository: [jakebutler22/peyce-part-3-1](https://github.com/jakebutler22/peyce-part-3-1). Runnable submitted source: [`2f00ffb0c72826a0a2b8a8fa000eb04971e2ff53`](https://github.com/jakebutler22/peyce-part-3-1/tree/2f00ffb0c72826a0a2b8a8fa000eb04971e2ff53). Final evidence/documentation snapshot: [`68519acd03a1e7110351d3994213854e49314a79`](https://github.com/jakebutler22/peyce-part-3-1/tree/68519acd03a1e7110351d3994213854e49314a79). The later commit containing this report packages those existing immutable references; it changes no application code. Archived Parts 3.1/3.2 remain preserved.

The [saved execution request](https://github.com/jakebutler22/peyce-part-3-1/blob/2f00ffb0c72826a0a2b8a8fa000eb04971e2ff53/prompts/03-peyce-3.3-master-prompt.md) transcribes the assignment-specific November 2, 2026, 11:59 p.m. America/New_York deadline and single unexpanded 100/85/70/50/0 criterion. The images were unavailable for this execution; Canvas was not opened. No instructor acceptance, student personal review, peer participation or upload is implied.

## Finished application

The existing Vue → FastAPI → SQLite system supports optional original face questions, automatic advancement with cancellable Back, unknown/skipped answers, transparent rule suggestions or direct choice, deliberate Start, both guided skills and honest finished/stopped/interrupted history. The white/pink composition, satin bow, realistic balloon and extensible asset registry remain. Four actual simulated laptop/phone layouts were inspected.

Personalization remembers only an explicitly selected balloon-colour enum in browser storage. Optional Repeat from a finished saved session creates a new UUID with unknown current answers, fresh timing and new wording; it never imports previous feelings or completion. Current refusal/choice outranks history and suggestions. Saving remains opt-in. Acknowledged SQLite writes, failed/pending saving, retry, reload and real backend restart were checked. Clear requires confirmation; cancel retains data; confirmed deletion cascades related session records and resets remembered colour while retaining provider-attempt accounting.

Records remain on the computer until cleared. Browser colour storage is separate from optional SQLite answer/activity/provenance storage and is disclosed. This single-user storage is unencrypted/unauthenticated coursework, not a production health record. The model receives current committed fictional answer turns and approved rule/reference context through the backend only. It cannot choose skills, generate exercise instructions, change timing, resume Stop or gate locally rendered support. There is no open-ended chatbot, distress detector, diagnosis, score, account or model training.

## Requirement-to-evidence mapping

All links below are pinned to existing commits.

| Part 3.3 requirement | Actual result and evidence |
| --- | --- |
| Complete/refine history and personalization | New-session Repeat, explicit colour continuity, truthful persistence and confirmed clear: [implementation/evaluation](https://github.com/jakebutler22/peyce-part-3-1/blob/68519acd03a1e7110351d3994213854e49314a79/docs/part-3.3-evaluation.md), [actual GUI](https://github.com/jakebutler22/peyce-part-3-1/blob/68519acd03a1e7110351d3994213854e49314a79/docs/evidence/3.3/gui-observations.json), [clear SQL](https://github.com/jakebutler22/peyce-part-3-1/blob/68519acd03a1e7110351d3994213854e49314a79/docs/evidence/3.3/clear-sql.json). |
| Revisit original design/research choices | Original → alternative → evidence → decision → cost mapped to R1–R4/D1–D6: [design review](https://github.com/jakebutler22/peyce-part-3-1/blob/68519acd03a1e7110351d3994213854e49314a79/docs/part-3.3-design-review.md). Instructor findings remain separate from external research; original questions are not STAI or clinically validated. |
| Documentation and clean checkout | Exact source, fresh pinned installation, sanitized mock environment, 88 backend/60 frontend tests, build, five asset HTTP/hash checks and two browser-completed saved skills: [clean-checkout record](https://github.com/jakebutler22/peyce-part-3-1/blob/68519acd03a1e7110351d3994213854e49314a79/docs/evidence/3.3/clean-checkout.json), [README](https://github.com/jakebutler22/peyce-part-3-1/blob/68519acd03a1e7110351d3994213854e49314a79/README.md). |
| At least fifteen scenarios, including failures | Eighteen predeclared cases, actual GUI variants and API/SQL supplements: [exact inputs/expectations](https://github.com/jakebutler22/peyce-part-3-1/blob/2f00ffb0c72826a0a2b8a8fa000eb04971e2ff53/backend/tests/fixtures/evaluation-3.3.json), [outcome matrix](https://github.com/jakebutler22/peyce-part-3-1/blob/68519acd03a1e7110351d3994213854e49314a79/docs/part-3.3-evaluation.md). |
| Repeatable mocks and three cross-case checks | Final deterministic [run 1](https://github.com/jakebutler22/peyce-part-3-1/blob/68519acd03a1e7110351d3994213854e49314a79/docs/evidence/3.3/final-deterministic-run-1.json) / [run 2](https://github.com/jakebutler22/peyce-part-3-1/blob/68519acd03a1e7110351d3994213854e49314a79/docs/evidence/3.3/final-deterministic-run-2.json): 16 API/SQL cases each, zero failures, matching signature and exact committed application; S09/S18 explicitly remain GUI/controller cases. B1–B3 are mapped below. |
| Small relevant repeated live selection | Three newly validated requests: same body context twice, one attention contrast, distinct provenance/settings and SQLite receipts: [live evidence](https://github.com/jakebutler22/peyce-part-3-1/blob/68519acd03a1e7110351d3994213854e49314a79/docs/evidence/3.3/live-variation.json). |
| Surprising finding and untested limitation | Cap blocking did not ensure truthful source labeling; repaired after preserved failure. Natural-human comfort/timing remains untested: [decision record](https://github.com/jakebutler22/peyce-part-3-1/blob/68519acd03a1e7110351d3994213854e49314a79/docs/part-3.3-design-review.md). |
| Finished-app demonstration and process screencast/code explanation | **INCOMPLETE: no video or verified playback/reviewer-access link.** [Recording index](https://github.com/jakebutler22/peyce-part-3-1/blob/68519acd03a1e7110351d3994213854e49314a79/docs/evidence/3.3/recordings.json) and [exact app/process shots/code explanation](https://github.com/jakebutler22/peyce-part-3-1/blob/68519acd03a1e7110351d3994213854e49314a79/docs/part-3.3-demo-script.md) are preparation only. |
| Safe peer testing and bounded model use | Mock default; host configuration clamps the stricter user ceiling to ten, already exhausted. No paid substitution/retry. History clearing preserves the real counter; the fresh checkout remained mock-only and never used or reset the real ledger. No peer test is invented. [Verification](https://github.com/jakebutler22/peyce-part-3-1/blob/68519acd03a1e7110351d3994213854e49314a79/docs/part-3.3-verification.md). |
| One report, AI-use and curated failed/revised approach | This file is the single upload. [AI-USE](https://github.com/jakebutler22/peyce-part-3-1/blob/68519acd03a1e7110351d3994213854e49314a79/AI-USE.md), [evidence/decision log](https://github.com/jakebutler22/peyce-part-3-1/blob/68519acd03a1e7110351d3994213854e49314a79/docs/evidence-log.md), [preserved S17 failure](https://github.com/jakebutler22/peyce-part-3-1/blob/68519acd03a1e7110351d3994213854e49314a79/docs/evidence/3.3/deterministic-initial-failure.json). |

## Eighteen evaluated outcomes

These are selected fictional variants, not all possible inputs. All routine cases use mock/fallback, including the artificial cap fixture. The linked matrix preserves exact labels/IDs, initial state, actions, declared expectations, versions, observed results and layer distinctions. API synthetic offsets never establish real exercise duration.

| Case | Observed outcome |
| --- | --- |
| S01 saved body cue | Correct breathing option; deliberate six-cycle completion and finished saved history. |
| S02 attention cue | Grounding; all five senses in order, private noticing, final Finish and saved record. |
| S03 one skip | Body answer stayed unknown; rationale did not claim it was supplied; choice remained. |
| S04 skip/direct | Both skills available without questions or fabricated answer turns. |
| S05 Back/correction | Current corrected context replaced the old suggestion; GUI refusal variant chose grounding. |
| S06 tie/insufficient | Transparent choice; no fabricated certainty or score. |
| S07 preference conflict | Current refusal/direct selection outranked suggestion/history. |
| S08 return/repeat | Explicit red retained after reload; fresh UUID/unknown answers/null old timing; saving opt-in reset. |
| S09 backend outage | Actual owned backend stopped; unsaved practice and local support worked without a Saved claim. |
| S10 pause/support | Closing support preserved explicit pause; deliberate Resume; overlap subtracted once. |
| S11 unfinished exit | Stop/reload/real process restart preserved stopped/interrupted, never fabricated completion. |
| S12 three fault types | Distinct controlled provider/timeout/invalid-output failures kept labeled fallback and usable controls. |
| S13 late output | After-Start GUI remained active; API Start/correction replies became obsolete rather than replacing current context. |
| S14 save failure/retry | Honest unconfirmed state, one recovered logical session, no duplicate events; stale retry label repaired/retested. |
| S15 real restart | Saved answers/status/colour/provenance survived; actual SQL foreign-key checks were empty. |
| S16 clear | Cancel retained twenty disposable rows; confirmed clear left six related tables empty and attempt guard unchanged. |
| S17 cap boundary | Initial wrong provenance preserved; corrected artificial 10/10 returned validated mock with no extra dispatch. |
| S18 keyboard/layout/motion | Pending Back cancelled; repeated Enter advanced once; four viewport checks, visible support, still balloon with changing cues. |

**B1, independent support:** controller assertions plus actual entry, both active/ready skills, history, loading, controlled failures and actual backend outage observations. Support never needed API/model permission; emergency links were not activated.

**B2, current user/application authority:** API cross-case helper plus real controller/browser skip, correction, refusal, direct choice, pause/resume, late response, Stop and interruption checks. No model/history/timer fabricated completion or resumed a stopped exercise.

**B3, persistence/provenance:** API/SQL helper plus real receipts, history, retry/reload/restart/cancel/clear and cap observations. Confirmed records agreed with committed SQLite; mock/fallback/live labels stayed distinct. The real ledger was separate from disposable fixture counters.

## New live repetition and measured timing

The exact free model/options and zero input/output prices were checked against current official metadata before dispatch: [preflight](https://github.com/jakebutler22/peyce-part-3-1/blob/68519acd03a1e7110351d3994213854e49314a79/docs/evidence/3.3/provider-preflight.json). Credential/configuration availability was distinguished from successful requests. Only server-side OpenRouter `nvidia/nemotron-3.5-lightning:free` was used, prompt `peyce-acknowledgment-1.2`, forced single `acknowledge_current_rule`, temperature 0.2, output cap 1,000, reasoning disabled, 15-second bound, zero-price routing, no automatic retry/paid fallback.

Attempts 8/9 used identical substantive body context `[2,0,0,0,0]`, one session/revision, separate request IDs. Both validated `reflect`, references `body`/`breathing`, closing `choice`, at approximately 0.886/0.565 seconds. Attempt 10, a **single contrasting observation** `[0,2,0,0,0]`, validated `reflect`, `thought`/`grounding`, `choice`, approximately 0.584 seconds. Identical repeated output is the result; variation was not manufactured. Three explanation receipts match the validated assistant turns. Actual Vue history displayed the contrast as Model-assisted/validated/**Ready**, with no finished duration. These API cases are not completed skills or a broad reliability study. The real durable counter advanced 7→10; $0 authorization and ten-attempt cap remain, with no further live allowance. Mock was restored.

On the exact source in a fresh checkout, real normal-speed browser timings were:

| Skill | First instruction → final Finish | Excluded time | Entry/check-in separately |
| --- | --- | --- | --- |
| Breathing | **79.3108 seconds** | 0 | 6.4611 seconds |
| Grounding | **74.0430 seconds** | 0 | 6.2417 seconds |

The script allowed six seconds to read, then all 60 seconds of actual breathing pacing, or private four seconds per grounding item (20/16/12/8/4 seconds); all application/tool/inter-call overhead and final Finish remained counted. Earlier working-tree observations 74.4610/76.2400 seconds remain separate. There was no imposed eight-second application closing delay to remove; that old wait was script-specific. No 90-second forced exit was added. A separate actual pause/support run excluded the union 2.3108 seconds, not the summed 3.8054 seconds. These are scripted interface timings, not natural-user or clinical evidence.

## Design finding, generated code and remaining human work

The surprising finding was that **preventing a capped provider dispatch did not itself ensure truthful provenance**. S17 initially retained OpenRouter/fallback labeling. The specific `LiveLimitReached` path now constructs the existing approved mock fragments, sets actual mode/model/status, and persists the matching source. Blocking transport and accurately explaining its origin needed separate assertions.

The [actual adapter](https://github.com/jakebutler22/peyce-part-3-1/blob/2f00ffb0c72826a0a2b8a8fa000eb04971e2ff53/backend/app/explanations.py) takes committed snapshot/rule context and a revisioned request, attempts a bounded reservation, and returns validated approved fragments or labeled fallback/mock. [Repository completion](https://github.com/jakebutler22/peyce-part-3-1/blob/2f00ffb0c72826a0a2b8a8fa000eb04971e2ff53/backend/app/repository.py) rechecks current state, marks stale results obsolete and stores actual mode/source. The Vue controller displays that source while retaining Start/Stop/support authority. This belongs in the service/repository, not the presentation view: the durable cap and provenance must hold for any caller. The S17 runner asserts mock identity, no extra dispatch, replay and unchanged accounting after clear. The recording guide also explains the actual `SequenceTimer` input/output and union-of-intervals behavior. **This written explanation does not satisfy the required on-screen code/process recording.**

A relevant untested limitation is whether natural users find the face wording comfortable and can read/decide at the scripted pace. Later consented fictional-task usability sessions, including assistive-technology users, could measure comprehension/correction/timing without claiming clinical benefit. No such participants were used. A genuine alternate IAB tab remained `visibilityState=visible`; real hidden-tab behavior, physical held keys/devices and screen-reader operation therefore remain unverified.

To complete the outstanding recording requirement, capture the scoped finished-app and process chapters from the exact guide, include at least one complete normal-speed skill, show the real controlled failure/evidence/change/retest and actual generated-code explanation, then verify readable web-playable files and durable reviewer access without a local login. Add real links/timestamps to this report; do not relabel stills or scripts as recordings. Keep private desktop/email/credentials outside capture. The student must personally review the source/report and perform the Canvas upload. No support service was deployed.
