# Peyce Part 3.1 design pipeline

Status: a clickable Vue design prototype with fictional, in-memory data and scripted explanations. This is coursework, with no person monitoring it. The eventual stack is Vue, Python/FastAPI, and SQLite; only the frontend design experiment exists now. The [source brief](assignment-source.md), [research ledger](research.md), and [observed verification](verification.md) separate supplied requirements, design assumptions, and evidence.

## Composition decision

Two compositions were considered before implementation:

| Composition | Benefit | Cost and decision |
| --- | --- | --- |
| Editorial split entry: satin bow art on the left, name/copy/actions on the right; check-in becomes a central question | Distinct visual identity with a clear action hierarchy; the material study introduces the pink family while the balloon is reserved for breathing | Requires a genuine mobile reflow and careful balance. **Chosen**: mobile bow above title/actions, central check-in, quieter bow during check-in, minimal exercise decoration. |
| Centered invitation: name and bow above one compact column, balloon below the primary action | Simple first glance and fewer layout regions | Bow, large balloon, and all controls compete vertically on a phone; less deliberate laptop composition. Rejected as the primary entry composition; its quiet central column informs check-in and grounding. |

Tokens begin with white `#FFFFFF`, blush `#FFF8FB`, pink `#F4D4E1`, action rose `#A83E68`, and text `#30242B`. The rendered contrast checks, screenshots, and any subsequent refinements are recorded in verification, not inferred from these token values. Green/orange/red belong to labeled face answers. Wordmark spacing and restrained typography are presentation choices; instructions use legible interface lettering. No streaks, fake testimonials, anxiety dashboard, confetti, or medical symbols.

## Screens and interaction flow

[Mermaid source](flow.mmd) and [readable hand-authored SVG](flow.svg) show the design flow. The SVG is manually composed from this flow; it is not a claimed automated Mermaid export.

| Screen/state | Primary action and retained control |
| --- | --- |
| Entry | “A moment at your pace.” → Find an exercise; Choose an exercise enters equal choices directly. Laptop bow art is left of copy/actions; mobile bow is above them. Prototype notice and sticky-header support are visible. |
| Check-in notice | Explains five optional questions and that choosing a face advances after a brief selection indication. Start check-in or skip all. |
| Question 1–5 | One question; three equal face targets with text; honest “n of 5”; Back, Skip this question, Skip all, exit, and support. |
| Equal choices / neither | Choose an exercise or finish. Unknown/refused information cannot force a suggestion. Deliberate voluntary exploration remains possible. |
| Ready | One short rule reason, exercise instructions, Start, alternative, Back/exit, and support. No timer before Start. Breathing color selection is optional. Balloon appears in laptop breathing-ready and breathing practice; mobile ready omits the large preview. |
| Breathing | One clock drives 4/6 phases, balloon and cue. Pause/resume, stop/normal breathing, switch, and support remain available. |
| Grounding | One sense per screen, quiet quantity markers, private noticing, Next; Back, skip sense, stop, switch, support. |
| Completion | Neutral acknowledgment; Finish or try the other exercise. No claim of improvement. Optional checkout is a future option, not implemented here; it must never block exit. |
| Past sessions | Clearly fictional sample records; quiet exercise/status details without streaks, diagnostic score, or hidden profile. |
| Support overlay | Sticky-header access opens a modal with “No person is monitoring this prototype,” verified region-labeled resources, close/return to retained state, then stop/exit. Available independently of answers/model. |
| Failure / fallback | Scripted explanation remains available and exercise choice works; support and exit remain visible. Future model failure cannot become an exercise gate. |

Automatic advancement follows deliberate click/keyboard activation, never focus/hover. The controller retains a selection for 360 ms and rejects another answer for 850 ms; the face component suppresses held-key repeat. Focus moves to the next question heading. Opening support during a pending face selection freezes that transition; closing support resumes the single pending advancement. Back restores selection. Editing or skipping any prior answer invalidates a cached result and recomputes from the revised answers. Skip this question stores `null`; Skip all abandons and clears answer-based recommendation, then opens equal choices. Retaining both Skip controls is a reversible assumption from the supplied prompt, not a newly confirmed user preference. These statements describe the current source behavior; browser observations are recorded in verification.

Grounding Next/Skip uses one controller transition with a 500 ms guard against rapid repeated activation. Its view suppresses repeated Enter/Space keydown. Each new sense receives heading focus; a new deliberate activation is needed for another transition. Support opening pauses active breathing and return requires deliberate Resume, as does returning after tab backgrounding.

Face construction uses the same eyes, circle, line weight, size, order, and hit area across all questions. A smile/straight mouth/frown plus text communicates each answer without relying on color. Controls target at least 48×48 CSS pixels; face hit areas aim for 80 pixels or more where layout permits. These are design targets, not pixel values derived from Fitts’ law or a claim of WCAG conformance.

## Original question contract

These original present-moment questions are not STAI, diagnostic screening, suicide assessment, or a validated scale. Red never signals a crisis and answer speed is never interpreted.

| Brief ID / prototype ID | Question | Green / orange / red labels | Routing meaning |
| --- | --- | --- | --- |
| Q1 / `body` | How easy is it to let your shoulders and jaw soften right now? | Easy / Takes some effort / Hard right now | Stated body-tension cue only |
| Q2 / `thought` | How easy is it to set a repeating thought aside for a moment? | Easy / It comes back / It keeps pulling me in | Stated external-focus cue only |
| Q3 / `present` | How connected do you feel to what's around you? | Present / A little distracted / Far away | Present-focus cue; never labeled dissociation |
| Q4 / `breathing` | How does following a gentle breathing rhythm sound right now? | Comfortable / Not sure / I'd rather not | Current breathing preference, not suitability screening |
| Q5 / `grounding` | How does noticing a few things around you sound right now? | Comfortable / Not sure / I'd rather not | Current grounding preference |

## Deterministic rule table, specified before the prototype

Policy `peyce-routing-1.0` is a design heuristic, not a psychological test, diagnosis, total anxiety score, or treatment recommendation. The external studies do not validate it. Only Q1–Q3 use private ordinal cue values 0/1/2 corresponding to their selected text; Q4/Q5 use the same indices as preference identifiers, never severity values. Those numbers never appear in the interface. No total-red count is computed.

| Order | Condition | Result and approved explanation basis |
| --- | --- | --- |
| 1 | A current deliberate exercise selection, Stop, neither, or support request | Honor it immediately. Direct choice overrides any earlier suggestion; support never depends on a rule. |
| 2 | Q4 and Q5 both “I'd rather not” | No automatic suggestion. Offer Finish and voluntary exploration without pressure. |
| 3 | Exactly one activity is explicitly Comfortable; the other is declined, uncertain, or unknown | Suggest the comfortable activity. Cite only its expressed comfort. A skipped preference is not used as evidence or permission. |
| 4 | Both activities Comfortable; all Q1–Q3 answered; Q1 > max(Q2,Q3) | Suggest breathing; cite the selected body-tension answer and breathing comfort. |
| 5 | Both activities Comfortable; all Q1–Q3 answered; Q1 < max(Q2,Q3) | Suggest grounding; cite the relevant selected repeating-thought/present-focus cue and grounding comfort. |
| 6 | Both Comfortable but comparison ties, is all zero, or necessary cues are missing | Offer both with equal prominence; insufficient distinction is explicit. |
| 7 | No activity explicitly Comfortable, including one declined and the other uncertain/unknown | No automatic suggestion. Offer voluntary choices/finish; any declined activity is excluded from automatic routing. |

Prototype reason codes: `direct-choice`, `both-declined`, `breathing-comfort`, `grounding-comfort`, `body-cue`, `present-cue`, `equal-choice`. Tie/incomplete/no-comfort share `equal-choice` with no clinical certainty; Skip all clears the result rather than attaching an abandoned recommendation code. The rule version is a module constant and belongs in eventual stored offered results. Both declined and one-declined/no-comfort states allow a new deliberate exploration choice; this does not retrospectively convert refusal into recommendation permission.

| Fictional answers Q1/Q2/Q3; Q4/Q5 | Expected result | Why |
| --- | --- | --- |
| Hard / Easy / Present; Comfortable / Comfortable | Breathing | Body cue exceeds present-focus cues and breathing is comfortable. |
| Easy / Keeps pulling me in / A little distracted; Comfortable / Comfortable | Grounding | Present-focus cue exceeds body cue and grounding is comfortable. |
| Hard / Easy / Present; I'd rather not / Comfortable | Grounding | Explicit comfort wins; breathing refusal excludes automatic breathing. |
| Any body cues; I'd rather not / I'd rather not | Neither forced | Both refused; Finish and voluntary exploration. |
| Easy / Easy / Present; Comfortable / Comfortable | Equal choices | All zero provides no differentiation. |
| Takes some effort / It comes back / Present; Comfortable / Comfortable | Equal choices | Tied comparison, not a total severity judgment. |
| Hard / skipped / Present; Comfortable / Comfortable | Equal choices | Missing necessary cue prevents comparison. |
| Any or skipped cues; Comfortable / skipped | Breathing | The direct breathing comfort alone supplies the reason; skipped grounding is never cited. |
| All skipped, or Skip all | Equal choices | No personalized reason; Skip all clears the abandoned result. |
| Change Q4 from Comfortable to I'd rather not after a breathing suggestion, with Q5 Comfortable | Grounding | Stale breathing result is invalidated and recomputed. |

These are fictional design checks, not patient evidence or the later-stage 15-scenario evaluation requirement.

## Timing and motion plan

**Breathing:** 4-second inhale + 6-second exhale × 6 cycles = 60 seconds of pacing, no hold. Budget from first exercise instruction through the final planned step: 10 seconds for concise preparation/reading/start decision + 60 pacing + 8 completion/finish = **78 seconds** under that assumed reading/decision pace. Preparation is counted. There is no forced exit or promise that every person finishes within 90 seconds. The 4/6/60 protocol comes from the course brief; NHS guidance supports comfortable, unforced technique and uses a different duration/count example.

Written introduction: “Follow the balloon with a comfortable breath. In through your nose as it grows, then gently out through your mouth as it softens. No need to force it.” Active cues are “Breathe in gently” and “Breathe out slowly.” Stop and return to normal breathing or switch if uncomfortable. Balloon inflation is a timing metaphor, never respiratory monitoring or a target lung capacity. No microphone/camera. Spoken guidance is only a later, off-by-default design option.

A single monotonic clock derives elapsed active time, cycle, phase, cue, and normalized inflation. Pause captures elapsed time; resume resets the monotonic anchor, retaining phase. The visual remains continuous at boundaries rather than jumping from low to full. Backgrounding pauses the experiment; return requires deliberate resume, with no replay/flash through missed phases. Reduced motion retains timing and text cues with a static object/progress alternative. Actual checks of this behavior are reported separately.

**Grounding:** 5 seen, 4 felt, 3 heard, 2 smelled, 1 tasted in that order. Planned private noticing budgets 25/20/15/10/5 seconds = 75 seconds. Six seconds for ready instructions/start decision, four one-second transitions, and five seconds for final acknowledgment/finish add 15 = **90 seconds**. These are assumptions to examine, not measured human performance or a compulsory countdown. No typing or 15 separate confirmation taps. Skip unavailable stimuli; do not eat, seek unsafe objects, or force any sensation.

**Separate check-in:** illustrative 6-second notice + five 4-second decisions + five 0.36-second selection indications ≈28 seconds, plus self-paced corrections/navigation. This is a budget, not observed response performance. User-chosen pauses and support access are excluded under the assignment rule; ordinary instructions, transitions, and start/finish decisions are included. No response deadline is imposed.

## Finding → decision → tradeoff → verification plan

| Supplied finding (count) | Design decision | Tradeoff | Verification plan |
| --- | --- | --- | --- |
| R1 (38) | 60-second pacing; ≤90-second intended full skill budgets | Reading/decision time varies; grounding pace is assumed | Clock math, complete budget audit; later human timing study |
| R2 (30) | Clearly labeled support access on every screen and overlay | Visible support consumes space | Navigate all states at laptop/mobile; check label, close, and external-link behavior |
| R3 (39) | Stop/exit without penalty, optional skip/checkout | Incomplete history needs honest status | Stop at each skill stage; check neutral return/status |
| R4 (68) | Direct choices, alternatives, neither, and refusals outrank matching | More choice may add one decision | Exercise override/neither/Back scenarios; no timer before Start |
| D1 (54) | Quiet single-task screens and optional controls for everyone | Cannot reliably infer rising distress; no adaptive detector | Inspect content density; confirm no emotion inference from speed/colors |
| D2 (100) | One question or sense at a time; one active skill | Longer navigation path | Flow/keyboard check; no competing active exercise |
| D3 (148) | No chat typing, accounts, demographics or required disclosure | Five taps still cost effort; faces can feel evaluative | Copy review; Skip/direct-entry checks; later usability feedback on faces |
| D4 (31) | Support persists in exercises, history, failure and overlay | Must survive small viewport/focus states | State-by-state support and keyboard visibility audit |
| D5 (49) | Optional color and transparent current comfort routing | Cannot establish clinical matching; unknowns reduce certainty | Rule tests, no hidden defaults; extension/visual preference audit |
| D6 (97) | White space, restrained bow, minimal practice decoration, neutral ending | Less decorative impact during practice | Side-by-side visual critique; reduced motion; no continuous ornament motion |

Faces distinguish options but may imply approval/disapproval; text says none is right or wrong, red is not a risk flag, and controls are equal. Automatic progression lowers taps but can surprise; the notice, brief selection feedback, activation lock, Back, and predictable focus address that cost. A person may choose a different exercise because current preference outranks our limited heuristic. No study establishes that our aesthetic, faces, or policy produces clinical benefit.

## MVC and extension boundaries

| Boundary | Current prototype responsibility | Inputs → outputs |
| --- | --- | --- |
| Model/data | `frontend/src/data.js`, `matching.js`, `assets.js`; fictional questions/history, pure rule result, registry | Versioned answer IDs/null + explicit choices → approved result/reason; asset ID → presentation metadata |
| Controller | `frontend/src/usePrototype.js`, `clock.js`; navigation, revision invalidation, activation lock, clock, lifecycle | Deliberate UI events + visibility + monotonic time → current screen, selection, state, phase |
| View | `App.vue`, `FaceOption.vue`, `DecorativeObject.vue`, `BalloonPacer.vue` | State/props → accessible presentation; emits actions, no clinical inference |
| Future backend | FastAPI controllers, rule/content services, SQLite repository | Validated structured session → persisted minimal record; not implemented |

Decorative objects use a registry entry with ID, source, material, color variants, desktop/mobile placement, dimensions/aspect ratio, decorative status, reduced-motion behavior, and provenance/license reference. `DecorativeObject` reads that entry. Adding an asset requires one registry entry plus the asset, not rewriting each screen. A documented second-instance example belongs with the actual registry/provenance notes. Bow is decorative, excluded from accessibility announcements and quieter during check-in; exercise pages have minimal bow presence.

Pacing visuals are separate: the current `BalloonPacer` consumes normalized `inflation` in `[0,1]`, color, and reduced-motion flag; phase wording stays in the parent view and shares the controller’s clock. A future alternative may render that normalized input but cannot alter the clock, breathing rules, instructions, or support. Pink satin bow and pink latex balloon share a family but distinct material/lighting. Optional balloon colors recolor the source with CSS filters while retaining its highlight/shadow shapes. Asset generation, inspection, rights limitations, and low/mid/full evidence are in the actual asset notes and verification.

## Future session and conversation contract

No persistence exists now. A future minimal record separates structured turns, deterministic result, selected action, lifecycle, and explanation provenance:

```json
{
  "schemaVersion": "peyce-session-1",
  "sessionId": "future-generated-id",
  "createdAt": "ISO-8601",
  "questionVersion": "peyce-original-1.0",
  "turns": [{"index": 1, "questionId": "body", "questionVersion": "peyce-original-1.0", "answerId": null, "skipped": true, "revision": 1, "at": "ISO-8601"}],
  "offered": {"ruleVersion": "peyce-routing-1.0", "exercise": null, "reasonCode": "equal-choice", "at": "ISO-8601", "answerRevision": 1},
  "chosenExercise": null,
  "lifecycle": [{"state": "stopped", "at": "ISO-8601", "activeElapsedMs": 0}],
  "visualPreference": {"balloonColor": null, "explicitlyChosen": false},
  "checkout": null,
  "explanation": {"kind": "scripted", "textId": "equal-incomplete-1", "modelId": null, "requestVersion": null, "validation": "not-requested"}
}
```

Allowed lifecycle states include ready, active, paused, completed, and stopped; timestamps/active duration describe app state only. A future checkout stores its own original question/answer version, is optional, and never becomes an improvement score. Do not store hidden clinical profiles, totals, click speed, cursor paths, or social-media data. Persistence consent, identity, retention, deletion, encryption, and recovery policy require explicit future design/review before implementation. Prior history may offer an opt-in preference later, never override today’s answer.

**Proposed history use:** the review view shows chosen exercise, date/time and completed/stopped status, with an optional repeat action. Repeating opens today's ready screen rather than starting a timer or reusing an old recommendation. An explicitly saved balloon color may be offered as a visual preference, with an easy change/reset control. Earlier answers may be reviewed as dated structured conversation turns, never interpreted as the person's current state. Today's refusal or direct choice always overrides history. This adds convenience while requiring consent, retention/deletion controls and a minimal data model; none of that persistence exists in the current prototype.

**Bounded future model:** at the recommendation boundary, one small validated request contains the actual structured turns, approved exercise content IDs, computed rule result/reason code, and concise output constraints. It may produce only a brief acknowledgment or explanation of that already approved result. Proposed output is `{ "reasonCode": "approved-input-code", "explanation": "plain-text <=240 characters" }`; validation requires the reason code to equal input, output to omit new skills/instructions/diagnoses, and explanation to reference only selected answers/approved wording. Stronger semantic validation and expert review remain unresolved; schema alone cannot prove safety.

The model cannot change exercise, timing, content, crisis access, refusal, or choice; cannot diagnose, score, prescribe, or infer from unanswered questions. At most one request, proposed ≤2-second timeout, no retry funnel. Approved canned explanation is available immediately; failure, invalid output, or delay retains it and never blocks Start/choice/support. Store model ID, provider/request/prompt version, content/rule versions, validation result, and fallback status separately from user turns. Prototype explanations are scripted; no live call, fine-tuning, weights, training data, or SQLite integration is delivered.

## Alternatives, unresolved questions, and release prerequisites

**Decision for crisis-related input:** this design has no free-text input, suicide questions or crisis classifier. It cannot detect or exclude a crisis from the five answers; red is never a risk signal. An explicit Crisis support action always opens verified, region-labeled information, including during an explanation failure, and displays the no-monitoring notice. This route is application-controlled and does not rely on a system prompt or model decision. Any future addition of free text would require a separate input/safety design before implementation; the current bounded explanation model receives structured answers and has no authority to decide support access.

Open therapeutic chat was rejected: it imposes disclosure, introduces unbounded responses, and gives a model unnecessary decision power. A deterministic button exchange is compact and explainable but may not meet the instructor’s interpretation of conversational context; ask the instructor before later-stage integration. Historical routing was rejected for the current design because today’s refusal and comfort should control it. A total-red score was rejected because neither the questions nor weights are validated. Heavy 3D was not required for the visual experiment; asset realism and performance must be judged in rendered evidence.

Unresolved: instructor acceptance of structured button turns; expert wording/rule review; whether faces feel evaluative; timing/comfort across real users; support coverage beyond verified regions; accessibility on real assistive technology and devices; future model semantic validation; consent/retention/security; rights for commercial asset/model use. Automated design checks do not constitute the student’s required personal review.

Before any public support-service release: qualified content/safety review, privacy/security assessment, accessibility evaluation, actual consented usability evidence, content/model/asset rights review, operation/incident/support plans, appropriate legal/regulatory review, and instructor constraints must be addressed. This course package establishes none of those approvals. Source publication is a separate action. **Stop at Part 3.1**; backend/model integration, accounts, recordings, clinical testing, deployment, and Parts 3.2/3.3 await later authorization.

### Concrete decorative extension example

`assets.js` routes entries through `slot: opening` or `slot: checkin`; the view loops over `objectsFor(slot)` and presents each through DecorativeObject. To add a future decorative object in an existing composition, add one asset and one registry entry with a slot and the required material/color/placement/dimension/provenance fields. No screen rewrite is required. The registered `satin-bow-small` is an actual second instance demonstrating this path. Layout judgment is still necessary for multiple objects; decorative clutter and focus obstruction are not justified by extensibility. Pacing objects remain a separate contract.
