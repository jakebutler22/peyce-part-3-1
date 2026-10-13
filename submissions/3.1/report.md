# Assignment 3.1 — Peyce: Research and Design

**Repository:** [https://github.com/jakebutler22/peyce-part-3-1](https://github.com/jakebutler22/peyce-part-3-1)

**Submitted design/code commit:** [`32bb48e5fd8acb2d967b965251e4491a388a83d9`](https://github.com/jakebutler22/peyce-part-3-1/commit/32bb48e5fd8acb2d967b965251e4491a388a83d9)

**Milestone:** Part 3.1 only. This report packages the fixed design commit above; the report itself is committed afterward.

Peyce (pronounced “pace”) is a coursework skills prototype proposing paced breathing and 5-4-3-2-1 grounding. Part 3.1 delivers an implementable design, research reasoning, model/data plans and a clickable design experiment. The assignment explicitly says a working application is not expected at this milestone. Current responses and history are scripted/fictional and remain in memory. No live model, backend, database or support service is offered or deployed. No person is monitoring the prototype. No code, assets or components were reused from the previous Mental Health project.

## Requirement-to-evidence map

| Part 3.1 requirement | Submitted evidence |
| --- | --- |
| Main experience, implementable design and sketch/flow | [Design notes](https://github.com/jakebutler22/peyce-part-3-1/blob/32bb48e5fd8acb2d967b965251e4491a388a83d9/docs/design-pipeline.md), [flow diagram](https://github.com/jakebutler22/peyce-part-3-1/blob/32bb48e5fd8acb2d967b965251e4491a388a83d9/docs/flow.png), [clickable HTML experiment](https://github.com/jakebutler22/peyce-part-3-1/blob/32bb48e5fd8acb2d967b965251e4491a388a83d9/submissions/3.1/prototype.html) and [laptop/mobile captures](https://github.com/jakebutler22/peyce-part-3-1/blob/32bb48e5fd8acb2d967b965251e4491a388a83d9/docs/screenshots/laptop-mobile-final.png) |
| Decisions grounded in R1–R4 and D1–D6; alternatives and tradeoffs | Full finding → decision → tradeoff → check matrix in the design notes; [instructor-source provenance](https://github.com/jakebutler22/peyce-part-3-1/blob/32bb48e5fd8acb2d967b965251e4491a388a83d9/docs/assignment-source.md) and [external evidence ledger](https://github.com/jakebutler22/peyce-part-3-1/blob/32bb48e5fd8acb2d967b965251e4491a388a83d9/docs/research.md) |
| Model role, relevant context and limits | Bounded request, output validation, approved fallback and model-provenance contract in the design notes |
| Expected saved data, history, personalization and user control | Versioned session/turn schema and proposed opt-in history use in the design notes; current history is visibly fictional |
| Useful project and agent documentation | [README and run instructions](https://github.com/jakebutler22/peyce-part-3-1/blob/32bb48e5fd8acb2d967b965251e4491a388a83d9/README.md), [AGENTS working rules](https://github.com/jakebutler22/peyce-part-3-1/blob/32bb48e5fd8acb2d967b965251e4491a388a83d9/AGENTS.md) and [future FastAPI/SQLite structure](https://github.com/jakebutler22/peyce-part-3-1/blob/32bb48e5fd8acb2d967b965251e4491a388a83d9/backend/README.md) |
| Verification and an actual revised/failed approach | [verification results](https://github.com/jakebutler22/peyce-part-3-1/blob/32bb48e5fd8acb2d967b965251e4491a388a83d9/docs/verification.md), [browser observations](https://github.com/jakebutler22/peyce-part-3-1/blob/32bb48e5fd8acb2d967b965251e4491a388a83d9/docs/browser-observations.json), [curated evidence log](https://github.com/jakebutler22/peyce-part-3-1/blob/32bb48e5fd8acb2d967b965251e4491a388a83d9/docs/evidence-log.md) and [before/after mobile revision](https://github.com/jakebutler22/peyce-part-3-1/blob/32bb48e5fd8acb2d967b965251e4491a388a83d9/docs/screenshots/mobile-revision-final.png) |
| AI-use disclosure and asset provenance | [AI-USE.md](https://github.com/jakebutler22/peyce-part-3-1/blob/32bb48e5fd8acb2d967b965251e4491a388a83d9/AI-USE.md), [original image provenance/prompts](https://github.com/jakebutler22/peyce-part-3-1/blob/32bb48e5fd8acb2d967b965251e4491a388a83d9/docs/assets/provenance.md) and [font licenses](https://github.com/jakebutler22/peyce-part-3-1/blob/32bb48e5fd8acb2d967b965251e4491a388a83d9/docs/assets/font-licenses.md) |

All evidence links are public, immutable URLs to the submitted commit; they do not depend on files beside the uploaded report. The HTML link is a downloadable local design artifact, not a deployed service. The README provides the tested localhost preview instructions.

## Experience and research reasoning

Entry offers “Find an exercise” or direct exercise choice. Five optional original questions appear one at a time, each with equal SVG smile/straight/frown controls and question-specific text. A notice explains automatic advancement; selection feedback, keyboard activation, Back, Skip this question and Skip all preserve correction and choice. A suggestion opens a ready screen with a short reason, deliberate Start and an alternative. Practice ends neutrally with Finish or the other exercise.

R1 motivates short, explicitly budgeted exercises. R2/D4 motivate persistent crisis-information access, including failure/history/overlay states. R3/R4 motivate stopping without penalty, direct choice, alternatives and honoring refusal. D1/D2/D6 motivate a quiet, single-task presentation without a presumed distress detector. D3 motivates private noticing and no required typing; D5 motivates optional visual preferences and explainable matching with minimal configuration.

A short check-in reduces open-chat disclosure but still costs effort. Faces are distinguishable yet can feel evaluative, so labels state no answer is right or wrong, color is never the sole meaning, and questions are skippable. Automatic advancement saves a tap but can surprise; prior notice, feedback and Back address that cost. A centered decorative composition was considered, but bow/balloon/control competition on mobile led to a split laptop opening and independently stacked mobile layout. Decoration becomes quieter during check-in and is absent during practice.

Matching is a versioned design heuristic, not an anxiety score or validated test. Current choice/refusal outranks a suggestion. Expressed comfort can supply a transparent reason; skipped preferences remain unknown. Only with complete body/present-focus cues and both activities comfortable is Q1 compared with max(Q2,Q3). With both activities comfortable, a tie or missing necessary body/present-focus cues yields equal choices. Changing an answer invalidates the stale suggestion. Face counts, response speed and historical answers never infer current distress. The instructor study and external studies do not validate these five questions or this policy.

## Proposed model, data and personalization

The future model receives the actual structured question/answer/skip turns, approved skill content, and the application's already computed rule result. One small request may produce a concise acknowledgment or explanation. It cannot diagnose, score anxiety, select/change an exercise, invent instructions, alter timing, override refusal or decide crisis access. Output must match the approved reason code and content constraints. A proposed two-second timeout or invalid output retains the immediately available canned explanation; access never waits for the model. Semantic validation and wording review remain open design work.

The proposed SQLite records include session/question/rule versions; answer-or-skip turns and revisions; offered recommendation/reason; chosen exercise; timestamps and paused/completed/stopped status; explicitly selected visual preferences; optional check-out; and model/request/content provenance stored separately from user turns. There is no hidden clinical profile or total score. Consent, retention, deletion and security require further design before persistence.

Future history shows exercise, date/time and completion status. An optional repeat opens today's ready screen, and an explicitly saved balloon color can be offered with change/reset controls. This reduces repeated configuration but adds storage/privacy responsibilities. Today's choice or refusal always wins. The current prototype saves nothing; its two sample records demonstrate presentation only.

## Timing and safety decisions

| Intended sequence, including ordinary instructions/transitions | Design budget and response assumption |
| --- | --- |
| Breathing | 10 seconds for instructions/start + six cycles of 4 seconds in/6 seconds out (60 seconds) + 8 seconds for completion/finish = **78 seconds** |
| Grounding | 6 seconds for ready instructions + noticing budgets of 25/20/15/10/5 seconds + four 1-second transitions + 5 seconds for completion/finish = **90 seconds** |
| Separate optional check-in | Approximately **28 seconds**: a 6-second notice, five 4-second decisions and five 0.36-second selection indications, excluding self-paced corrections |

These are intended reading/response assumptions, not measured human performance or deadlines. Preparation is counted within the exercise budget from the first exercise instruction. User-chosen pauses and crisis-support time are excluded as the assignment specifies. There is no forced exit. Breathing has no hold or forced depth; the balloon is a timing metaphor, not a breathing measurement. Grounding preserves 5 seen, 4 felt, 3 heard, 2 smelled and 1 tasted, with private noticing and one Next per sense. Unavailable sensations may be skipped; eating, drinking or approaching unsafe objects is unnecessary.

The deliberate crisis-input decision is to accept no free text and perform no crisis classification. The five answers cannot establish whether someone is in crisis, and red never signifies risk. An explicit Crisis support action opens verified, region-labeled information on every screen independently of any answer, model, classifier or system prompt. The overlay states that no person monitors the prototype. Adding free text would require a separate safety design. Only fictional scenarios were used; this application is not offered for real distress or clinical care.

## Recorded checks, revision and unresolved work

The unchanged Vue experiment passed **36 tests**, including refusal/unknown invariants across **1,024 answer combinations**, and built successfully. **25 browser checks passed**: required routing paths, Back correction, skipping, direct choice, keyboard/focus, double activation, grounding progression, stopping/alternatives, neutral ending, history/failure and support behavior. Actual 1440×900/1280×800 laptop and 390×844/360×800 mobile viewport captures were inspected and refined. The balloon's low/mid/near-full states and fixed-size minimal-motion mode were observed.

The implementation keeps matching separate from presentation and uses one elapsed-time clock for both breathing labels and inflation. Four seconds of each ten-second cycle are inhale and six are exhale; pause preserves elapsed time instead of resetting the cycle. This carries the pacing cue consistently without claiming to monitor respiration.

An actual mobile screenshot exposed Stop/progress hidden after focus scrolling and a magenta “red” balloon. Resetting task scroll/focus restored the controls; targeted recolor revisions produced the final red family. A pending face transition that could override an exit was also corrected and verified. These revisions connect control/visibility findings to observable design changes rather than a feature list. Agent checks and their limitations are disclosed in the linked evidence log and AI-USE.

Unresolved: whether structured button turns meet the instructor's eventual conversational-model interpretation; whether faces feel evaluative; real-user timing/comfort; future model semantic validation; consent/retention/security. Genuine hidden-tab behavior and direct-file execution were not observed with the available browser controls, although clock simulation and export syntax/assets checks passed. Mobile dimensions are simulated, not actual device tests; screen readers and broader accessibility remain untested. A single balloon image is deformed/recolored, so physical inflation is approximated. Source-access limits and asset/model rights are recorded in the evidence ledger/provenance. No clinical benefit, blanket WCAG conformance, completed student personal review or guaranteed grade is claimed.

**Part 3.1 is complete as a research/design submission.** No later-part implementation, evaluation or recording is presented as completed work.
