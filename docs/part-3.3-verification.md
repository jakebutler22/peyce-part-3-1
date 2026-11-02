# Part 3.3 verification · November 2, 2026

Peyce is pronounced **pace** (/peɪs/). This is an agent-performed fictional localhost evaluation. The assignment-specific due time and unexpanded 100/85/70/50/0 rubric come from the user's saved transcription, not a new Canvas visit. No grade or student personal review is claimed.

## CHECK

Started at `698b2e4d432b4f16a75f29307bd9435b86b33f75`, clean tracked tree, existing public remote `jakebutler22/peyce-part-3-1`. Scoped branch: `codex/peyce-part-3-3`. [Baseline](evidence/3.3/baseline.json). The unchanged backend baseline was actually rerun: 86 tests passed. The prior 46 frontend count was historical; it was not rerun before editing. Archived Part 3.1/3.2 evidence was fingerprinted before changes.

The real ignored runtime ledger was 7/10; mock was the default. No initial localhost service was running. Existing tools: Node 24.12.0, npm 11.6.2, Python 3.14.7. No new dependency was added to either manifest. Fresh dependency installation is recorded separately in the clean-checkout evidence.

## TAKE ACTION → VERIFY

Implemented one explicit colour enum preference, new-session Repeat from finished saved history, controller-owned clear/cancel, cap-to-mock provenance, and active pace pronunciation/prompt 1.2. Current answers and deliberate choice remain authoritative. The original face questions, rule version, assets, six 4/6-second breathing cycles and private 5/4/3/2/1 grounding are retained.

Observed corrections and retests:

| Observation | Scoped change | Actual check |
| --- | --- | --- |
| S17 blocked the simulated capped dispatch but labeled the result OpenRouter fallback. | Return validated mock fragments and persist mock mode/source. | Preserved initial failure, repeated isolated API/SQL retests, and actual browser `Mock wording` at artificial 10/10. No real key or network in the cap fixture. |
| Back was disabled during the 360 ms selection transition. | Cancel its timeout/pending flag and allow deliberate Back/correction while retaining ordinary duplicate guards. | Two controller tests failed before repair; now pass. Actual GUI pending Back stayed at intro after the old timeout; repeated Enter advanced one question only. |
| Successful save retry left `saving unavailable` in optional-wording text. | Change only that stale label after acknowledgment, without requesting the provider. | Regression failed before repair; actual browser now shows `Saved on this computer` and `Local rule · optional wording not requested`. |

Routine final working-tree checks: **88 backend tests, 60 frontend tests, production build passed**. The API runner evaluates 16/18 declared scenarios twice; S09/S18 are explicitly GUI/controller cases. Both normalized repeat signatures match. See [layer notes](evidence/3.3/deterministic-layer-notes.md), [run 1](evidence/3.3/deterministic-run-1.json), [run 2](evidence/3.3/deterministic-run-2.json). One existing Starlette/httpx deprecation warning remains. A root pytest invocation initially omitted `PYTHONPATH`; the corrected documented invocation passed, with the command failure retained separately.

Actual browser evidence covers S01–S18 and B1–B3, supplementing those API cases rather than relabeling their layer. [Observations](evidence/3.3/gui-observations.json), [context](evidence/3.3/gui-context.json), [evaluation](part-3.3-evaluation.md). Development hot reload interrupted two fault/layout attempts during scoped edits; the affected observations were repeated after writes finished. A premature Finish selector while breathing was still active was a harness observation error, not an application failure or accelerated exercise.

Actual SQL evidence establishes saved finished skills, unknown skipped/repeated answers, versioned acknowledgment provenance, obsolete replies, retry without duplicate logical records, and zero foreign-key errors. A real owned backend process was stopped for unsaved/offline practice and restarted for saved-history verification. A saved active session became interrupted after an actual process restart; Stop/reload did not manufacture completion. [Restart](evidence/3.3/real-restart-sql.json), [retry/reload](evidence/3.3/save-retry-and-reload-sql.json), [pre-clear records](evidence/3.3/gui-sql-before-clear.json).

Cancel retained 20 fictional rows in the disposable UI DB. Confirmed clear removed all six related session tables; a subsequent colour-control session was also cleared before immediate SQL inspection. The artificial attempt ledger remained 10. The separate real runtime DB was never cleared or reset. [Cap/cancel](evidence/3.3/cap-and-cancel-sql.json), [final clear](evidence/3.3/clear-sql.json).

## Actual timing and presentation

| Guided skill | First instruction → final Finish, raw=counted | Exclusions | Entry/check-in separately | Scripted assumption |
| --- | --- | --- | --- | --- |
| Breathing, saved body cue | **74.4610 s** | 0 | 6.3289 s | Six-second deliberate reading wait plus all observed tool/response overhead; actual 60-second six-cycle pacing; final deliberate Finish. |
| Grounding, saved attention cue | **76.2400 s** | 0 | 6.3739 s | Six-second instruction wait; private 4 seconds per fictional item (20/16/12/8/4 s), every sense advanced in order, final Finish; all inter-call overhead counted. |

[Actual session/timing snapshots](evidence/3.3/gui-sql-before-faults.json). Both whole sequences are below 90 seconds at these assumptions; neither establishes a natural-human maximum. The application has no forced 90-second exit. No actual application-imposed eight-second closing delay existed: that old delay belonged to the October script. These runs preceded the Back/retry-label corrections; pacing/timer/skill files did not change. The frozen candidate clean checkout separately repeats a full normal-speed skill.

Pause/support overlap was observed in a stopped breathing session; the union excludes the shared interval once. Background downtime remains counted by the timer. Four simulated CSS viewports were inspected: 1440×900, 1280×800, 390×844, 360×800. Original distinguishable faces, responsive controls, balloon and support were inspected in actual screenshots. The 360 px DOM width equals scroll width. Minimal motion kept the actual balloon transform/size unchanged while `Breathe in gently` changed to `Breathe out slowly` after five seconds. This is simulated viewport and discrete-key evidence, not physical-device/screen-reader certification.

Opening another actual IAB tab left `document.visibilityState=visible`; genuine hidden-tab behavior therefore remains unverified. No synthetic event is substituted for a real visibility observation. Independent local support was opened from entry, ready/active breathing and grounding, history, optional loading, controlled faults and an actual backend outage, without activating emergency links. Its focus/return controls were exercised. The required hotline lookup was performed again on November 2.

## New live evidence, kept separate

Two bounded public metadata reads verified the exact current free model and supported options before dispatch. [Preflight](evidence/3.3/provider-preflight.json) links the official catalog/model page. Presence of a credential and safe configuration was checked separately from request success; secrets were never printed. Process-only live settings used the intended existing runtime DB and a 15-second timeout. No `.env` contents or unrelated project credentials were copied.

**Three actual generation attempts, numbers 8–10, all validated.** [Exact responses, context, settings and SQLite readback](evidence/3.3/live-variation.json). The same body-cue session/revision/answers/substantive context was requested independently twice, with distinct request IDs. Both selected `reflect`, `body`/`breathing`, `choice`: identical output is the observed result. One contrasting attention case selected `reflect`, `thought`/`grounding`, `choice`. Latencies were approximately 0.886, 0.565 and 0.584 seconds, including local request handling.

The provider selected approved IDs/references; application validation and construction supplied exact answer labels/wording. It did not control skill, timing or support. Three explanation rows and matching assistant acknowledgment turns are retained; other assistant question turns are not mislabeled as generated responses. Initial postprocessing used the wrong turns query column, then corrected the read-only query from the actual schema; no generation was retried.

Actual Vue history displayed the contrasting case as **Ready**, `Model-assisted · validated`, the exact model and revision, and no finished duration. [Screenshot](evidence/3.3/live-history-provenance.png). These API-ready cases are not completed skills. The cumulative durable count is **10/10**, $0 authorized, no paid fallback or automatic retry. The backend was returned to mock. Two repeated observations and one contrasting observation cannot establish broad reliability, peer usability or clinical benefit.

## Clean checkout and publication gate

Runnable source **`2f00ffb0c72826a0a2b8a8fa000eb04971e2ff53`** passed a separate fresh managed checkout. [Exact commands/environment/install/test outputs and SQL](evidence/3.3/clean-checkout.json), [actual GUI](evidence/3.3/clean-gui.json). Fresh Python3.14.7 virtual environment and `npm ci` installed the tracked requirements/lock without copying working dependencies, `.env`, credentials or database. The sanitized environment retained PATH/TMPDIR/LANG only, explicitly disabled dotenv and set mock; pytest also set `PYTHONPATH=backend` as documented. No source dependency was added.

Both documented loopback services started; status reported mock, no live configuration, test controls off and zero fixture attempts. **88 backend tests,60 frontend tests and production build passed**. The bow, balloon and three local fonts all returned HTTP200 with content hashes matching tracked files; no logged-in download or filesystem asset URL was required. The fresh SQLite contains exactly two new finished fictional sessions, validated mock provenance, complete lifecycle records and zero foreign-key errors.

Frozen-source whole timings, including all tool overhead: **breathing79.3108s** (entry6.4611s separately), **grounding74.0430s** (entry6.2417s separately), both zero exclusions. These repeat the stated six-second reading/normal60-second breathing and four-seconds-per-private-item grounding assumptions. [Finished breathing](evidence/3.3/clean-history-finished.png), [finished grounding](evidence/3.3/clean-grounding-finished.png). These are scripted browser runs, not recorded videos or natural-user studies.

The deterministic runner was executed twice more on the exact committed source; both report `app_matches_git_head=true`,16API passes,0API failures and the same normalized signature as earlier runs. [Final run1](evidence/3.3/final-deterministic-run-1.json), [final run2](evidence/3.3/final-deterministic-run-2.json). An extra invocation initially asked the runner to print an output path outside its checkout, causing a post-write relative-path ValueError; using an in-checkout ignored output path and copying the safe evidence corrected the harness invocation. No application or README setup defect, extra provider dispatch or hidden source change occurred.

The tracked checkout remained clean. Owned clean-test processes91698/91816 were stopped; only owned services were handled. The original runtime ledger remains10, separate from this fresh mock database's0. Final publication checks and any recording-ready restart are recorded by the later evidence/report packaging commit. No app code changes follow this source without establishing another candidate.

## Required recordings and remaining limits

**Finished-app demonstration and process screencast are incomplete.** Browser capabilities expose screenshots, not video; the native QuickTime recording action did not expose a controllable capture toolbar, and selecting the capture app timed out. No recording was produced or playback/access verified. This was reported early. [Exact recording-ready script and code explanation](part-3.3-demo-script.md) and [recording index](evidence/3.3/recordings.json) do not stand in for videos. No private desktop/email or credential material is included.

No peer participants, physical assistive-technology review, natural-user usability or clinical evaluation were performed. The student's personal source/report review and actual Canvas upload remain human tasks. Current source publication is separate from deploying a support service.
