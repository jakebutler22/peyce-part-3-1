# Part 3.1 verification · observed results

Date: 2026-10-13, America/New_York. These are fictional design checks by agents, not student personal review, participant usability research, clinical validation, or the later-stage 15-scenario requirement.

## Actual environment and checks

macOS laptop; Node24.12.0/npm11.6.2; Vue3.5.44, Vite8.3.4, plugin-vue6.0.10. `npm install` installed35 packages, audit36 packages, reported0 vulnerabilities. `npm run verify` passes36 Node tests and the production frontend build. The package lock pins the observed dependencies. Local HTTP preview at127.0.0.1:5181 returned200 and was inspected in the Codex in-app browser. Chrome was used only for a visibility experiment. No deployment or backend was run.

The browser's full-page screenshot API was used for exact requested CSS dimensions. The first ordinary laptop capture clipped to the native pane width; it was removed and replaced with a1440×900 full-page capture. Simulated mobile dimensions are viewport checks, **not actual iPhone tests**. Laptop1440×900 and1280×800, mobile390×844 and360×800 were inspected. Before/after and side-by-side contact sheets derive from actual screenshots, with labels added for documentation.

## Functional evidence

| Check | Observed result |
| --- | --- |
| Matching and question contract |36 pure tests pass. Exact five question/face-label sequences and grounding quantities tested. Safety invariants checked across all1,024 valid answer combinations. No total-red/total-anxiety score or click-speed inference exists. |
| Browser routing | Body-tension→breathing, present-focus→grounding, breathing refusal/grounding comfort→grounding, both declined→voluntary choices/Finish, missing body cue→equal, all skipped→equal, tie→equal. |
| Back correction | Previous Q5/Q4 selections visible. Changing Q4 from Comfortable to I'd rather not removes the breathing suggestion; grounding ready shown after recomputation. |
| Skipping/direct choice | Skip this question leaves unknown; Skip all discards abandoned recommendation and says no check-in needed. Direct choices and alternative exercises reach ready without check-in. |
| Face activation/focus | Double activation advances only one question. Enter deliberately activates the focused face; next H1 receives focus. Enter on that heading does not answer. Buttons do not answer on focus/hover. Physical sustained key holding was code-reviewed through repeat suppression, not manually held on a hardware keyboard. |
| Exit/overlay revision | Pending selection cannot override a deliberate home exit. Support holds a pending question transition, then advances once after Escape/return. |
| Grounding | One screen per sense; double Next advances once; Back restores previous sense; Skip this sense progresses; all five skipped senses reach a neutral completion. No typing,15 separate confirmations, eating/drinking or unsafe stimulus requirement. |
| Breathing clock | Pure tests verify4s inhale+6s exhale×6=60s, no hold, continuity at every boundary, one monotonic clock, pause/resume and completion clamp. Browser pause froze the balloon's transform. A full unpaused run showed cycle6 active at53.549s and completion by the72.449s follow-up snapshot; this brackets the transition rather than claiming a stopwatch measurement at exactly60s. |
| Motion | Actual low/mid/full transforms: scale(.63138,.728385),(.801542,.853768),(.998851,.999153). Near-full capture retains knot/shading. Minimal motion keeps scale fixed at.85/.85 while elapsed progress changes. OS reduced-motion initialization is source-reviewed; manual minimal-motion mode was exercised. |
| Stop/switch | Stop reaches EXERCISE STOPPED with Finish/other exercise. Alternatives reach ready; no timer starts before Start. Support during breathing pauses; closing leaves Resume. |
| History/failure | Two records are visibly fictional. Scripted explanation-failure screen leaves choice/Finish/support available. No live model/database called. |
| Support/focus | Every visited screen has Crisis support. Native modal has region labels and no-monitoring notice. Tab cycles Close→Call988→Text988→Chat→Call911→Return→Close after explicit endpoint refinement. Escape returns focus to support. No phone/SMS/chat action was activated. |
| Sticky mobile support | At360px and scrollY165.5, support remains top16/bottom64 with109.3×48px bounds. Both exercise-choice controls are316.8×206.8px. |

[Machine-readable browser observations](browser-observations.json) record25 completed passing checks plus one inconclusive visibility experiment. The tab-creation APIs kept both original documents `visible` in IAB and Chrome. Consequently, a genuine `document.hidden` event was not observed. The implemented visibility handler pauses without accumulating hidden time and requires deliberate Resume, and its clock contract passed simulation; **real backgrounding remains unverified**. The misleading “background pause” screenshot name was removed rather than used as proof.

## Visual and accessibility observations

The original generated satin bow and latex balloon were inspected as actual pixels and white alpha composites. Satin loops/knot/tails show fabric folds and sheen; the latex balloon has rounded highlights, tapered neck and tied knot. No prior-project art was reused. The bow stays static, becomes quiet in laptop check-in, is hidden in mobile check-in, and is absent in practice. It does not cover Back/name/support/focus areas. The registry's second instance and slot contract demonstrate extension without rewriting screens.

The five faces use identical circle/eye geometry and line weights, with smile/straight/frown mouth paths, ordered green/orange/red and question-specific text. At390px, all three answer controls measured343.2×82px; Back/Skip/support measured48px high. At360px, controls remain generous and no horizontal overflow was observed. Short-laptop question full-page height was806px initially, then800px after a16px lower-spacing revision. Text/controls remain legible in final captures.

The mobile breathing Stop/progress row was initially hidden after focus scrolling. Resetting scroll and preventing focus scroll restored the row at88–136px below the header. Initial “red” rendering was magenta; two targeted filter refinements produced the final red-family balloon while retaining the source shading. Single-source deformation/recolor remains an approximation, not measured physical inflation or a new photograph.

Locally bundled fonts were observed loaded: `document.fonts.status=loaded`, DM Sans and Playfair checks true. Official Google Fonts blob/hash verification and OFL files are retained. No remote font import remains.

[Contrast calculations](contrast.json), using rendered CSS tokens and the face-fill blends, show plum text14.86:1, muted text6.12:1, white/rose actions5.91:1 and focus outline8.70:1 on white. Face lines on their light fills are approximately4.61/3.92/4.52:1. Pale borders, decoration and hidden progress dots are not relied on as the only labels. These checks do not establish blanket WCAG conformance or test a screen reader.

## Screenshot index

| Artifact | Evidence |
| --- | --- |
| [Laptop opening](screenshots/01-home-laptop-1440-final.jpg) / [mobile opening](screenshots/02-home-mobile-390-final.jpg) | Final distinct layouts, typography and satin bow |
| [1280 opening](screenshots/04-home-laptop-1280.jpg) / [1280 question final](screenshots/05-checkin-laptop-1280-after.jpg) | Smaller laptop fit |
| [390 question](screenshots/03-checkin-mobile-390-before.jpg) / [360 question](screenshots/08-checkin-mobile-360.jpg) | Equal faces/text and hit areas; the390 capture predates final interaction refinements but its layout is unchanged |
| [Breathing ready](screenshots/06-breathing-ready-laptop-1280.jpg) / [neither](screenshots/07-neither-laptop-1280.jpg) | Transparent reasoning, deliberate Start and no forced path |
| [Grounding mobile](screenshots/10-grounding-mobile-360.jpg) / [support mobile](screenshots/11-support-mobile-360.jpg) / [history](screenshots/12-history-mobile-360.jpg) | Sense task, region-labeled resources and fictional record |
| [Balloon states](screenshots/balloon-states.png) | Side-by-side actual low/mid/near-full screenshots; originals14/15/16 retained |
| [Minimal motion](screenshots/17-minimal-motion-laptop-1440.jpg) / [completion](screenshots/18-completion-laptop-1440.jpg) | Fixed-size mode and neutral ending |
| [Laptop revision](screenshots/laptop-revision.png) / [mobile revision](screenshots/mobile-revision-final.png) | Actual before/after critique and correction |
| [Sticky support](screenshots/20-mobile-sticky-support.jpg) | Support remains visible after scroll |

## Requirement audit and limits

| Brief section | Concrete artifact/status |
| --- | --- |
| A: Part3.1 scope and finish | README, Vue prototype, report, backend README contracts only. No production/service/later-stage work. |
| B: bespoke direction/extensibility | Rendered screenshots, original generated assets, registry/components, OFL fonts, exact prompts/provenance. |
| C: five original optional faces | data.js, FaceOption, controller, pure and browser checks. Skip assumption is explicitly reversible in design notes. |
| D: explainable matching | Versioned table and fictional examples in design-pipeline precede implementation; matching.js tests. |
| E: exercises/ending/history | Actual frontend experiment; complete planned breathing78s/grounding90s budgets plus separate~28s check-in assumption. Human completion time is not measured or enforced. |
| F: model/session requirement | Future bounded request/response validation, fallback, session/turn/provenance schema and MVC in design-pipeline. Button-turn course acceptance remains unresolved. |
| G/H: instructor/external evidence | Supplied assignment-source, full R/D matrix, distinct external-source ledger, official support verification. No Canvas or original screenshot review claimed. |
| I: package, Git, independence | Root rules/index/disclosure, numbered prompt, flow, evidence, screenshots, submission and handoff; source then report packaging commits. |

The standalone HTML was mechanically exported from the verified build with embedded images/fonts/licenses; syntax, absence of external runtime asset references, and deterministic reproduction were checked separately. Direct `file:` opening was rejected by browser URL policy. It was not retried through another browser or a workaround, and direct-file execution is **unverified**. The Vue preview was actually exercised.

Untested: actual iPhone/touch hardware, Safari/Firefox, screen readers, high zoom/accessibility beyond the recorded checks, genuine backgrounding, direct-file execution, real user timing/usability, professional clinical/content/privacy/security/rights review and instructor approval. Research access limits: Fitts live demo unavailable; Macaulay full text unavailable, publisher abstract verified. No unsupported result is described as a pass.

[Independence evidence](independence.json): all190 tracked/unignored previous-project file hashes identical, previous HEAD unchanged and status clean. This repository has its own initial history and copies no previous code/assets. Ignored runtime caches were not fingerprinted; no writes to the previous root were performed. Final Git publication details are in report/handoff. Student personal review remains required.
