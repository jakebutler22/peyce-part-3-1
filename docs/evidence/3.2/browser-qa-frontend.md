# Integrated frontend browser observations — 20 October 2026

Peyce is pronounced **peace** (/piːs/). This is actual local Vue → FastAPI → SQLite coursework verification with fictional selections. The dedicated Chrome extension-controlled tab used `http://127.0.0.1:5181/?verify=1`; the API ran in deterministic **mock** mode on `127.0.0.1:8012` with controlled faults enabled. No live model requests were made by this QA run.

The [machine-readable observations](browser-qa-frontend.json) retain the exact sampled values. Viewports were simulated CSS dimensions, not physical laptop/mobile devices. Some images are full-page captures at the stated viewport width and extend beyond the viewport height.

| Check | Actual observation | Selected evidence |
|---|---|---|
| 1440×900 and 1280×800 home | Explicit peace pronunciation, save initially unchecked, both entry actions visible. No horizontal overflow. | [1440](new-1440-home.jpg), [1280](new-1280-home.jpg) |
| 390×844 and 360×800 home | Single-column layout, full-width entry actions, 48px support control, 44px save-label target. No horizontal overflow. | [390](new-390-home.jpg), [360](new-360-home.jpg) |
| Original questions at 360px | Exact question and question-specific answer copy retained; three 316.8×82px answer targets. Brief selected/disabled state advances one question. | [Check-in](new-360-checkin.jpg) |
| Short/long/fallback ready wording | A genuine mock direct-choice acknowledgment and a 151-character thought/grounding acknowledgment displayed different actual selected context. Mobile reserved explanation area remained 112px. Start stayed available. | [390 long](new-390-ready-long-mock.jpg), [1280 short](new-1280-breathing-ready-short.jpg), [360 body cue](new-360-ready-mock.jpg) |
| Mobile scrolling and support | Header support remained reachable after scrolling. Local dialog opened; Shift+Tab from Close wrapped to Return, Escape closed it and returned focus to support. External call/text/chat links were never activated. | [360 support](new-360-support.jpg) |
| Minimal motion | Fixed `matrix(0.85,0,0,0.85,0,0)` across inhale/exhale while progress/cues changed. | [360 minimal motion](new-360-minimal-motion.jpg) |
| Actual balloon forms | Through actual Start/Pause/Resume controls, sampled scale pairs were low `(0.624757,0.723505)`, mid `(0.893441,0.921483)`, near full `(0.991533,0.993761)`. Targeted 2.0s/1.7s waits sampled the running clock; no page-state or clock injection. | [Low](new-1440-balloon-low.jpg), [Mid](new-1440-balloon-mid.jpg), [Near full](new-1440-balloon-full.jpg) |
| SQLite-backed saved history | Actual stopped session showed current ten Q/A turns once, earlier snapshots collapsed, stored explanation provenance, lifecycle, and time. Earlier revision 3 expanded to its actual original Q/A. | [1440 detail](new-1440-session-detail.jpg), [360 detail](new-360-session-detail.jpg), [Earlier revision](new-360-earlier-revision.jpg) |
| Delete decision | Clear revealed a separate explicit confirmation. Keep history retained the records. No final deletion was performed. | Recorded DOM observation in JSON |
| Initial database write fault | Fault enabled before revision 1: choice, ready, Start, support and Stop worked; footer reported not confirmed saved. Removing fault and Retry saving acknowledged the stopped record, exercising revision-1 bootstrap recovery. | [Unsaved ready](new-1440-unsaved-ready.jpg) |
| Database read fault | History displayed an honest unavailable message; local support opened. Removing fault and Try again restored actual saved rows. | [Read failure](new-1440-history-read-failure.jpg) |
| Invalid/provider/timeout faults | Invalid or failed output retained approved copy with Local fallback. Timeout first showed optional wording loading with enabled Start, then fallback. Start, support, Stop and Finish remained usable. These are controlled injections. | [Invalid fallback](new-1440-invalid-fallback.jpg), [Timeout fallback](new-1440-timeout-fallback.jpg) |
| Late response | Waited for actual optional-wording loading, then activated Start in the same supported CUA batch. After the 0.5s injected delay, the screen remained breathing with phase/progress; no explanation area, skill/navigation change or focus move appeared. | [Late response during practice](new-1440-late-response-practice.jpg) |
| Targeted contrast | Computed contrast on white: muted text 6.12:1; rose labels and white-on-rose primary 5.91:1; dark text 14.86:1. This is a targeted color check, not a complete accessibility audit. | Rendered DOM-style observation in JSON |

Two actual presentation issues were corrected and retested, one correction cycle per check:

1. Repeated full-snapshot conversation turns made the initial history detail excessively long. The default now renders current structured Q/A once. Earlier turns remain available in accessible, collapsed revision disclosures; explanation provenance identifies earlier revisions. The new laptop/mobile detail captures show ten current turns and reachable timing.
2. At 1280×800, the decorative grounding numbers wrapped as four numbers plus an isolated 1 with a displaced caption. A small CSS grid correction keeps all five numbers in order on one row and the caption below. Actual retest placed all number tops at `327.13px`, caption at `444.73px`, with no horizontal overflow. [Before](new-1280-grounding-ready.jpg) · [After](new-1280-grounding-ready-refined.jpg). Production build passed after correction.

Real backgrounding remains **unverified**: opening a second real Chrome tab did not make the practice tab's `document.hidden` true. A synthetic visibility event was not substituted. Screen-reader use, physical-device usability and natural human reading pace were not evaluated. The root agent owns the separate uninterrupted timing demonstration and actual backend-offline observation; this paused/stopped QA does not replace them.

Temporary viewport overrides were reset and only the dedicated QA tab was closed. Unrelated tabs and local servers were left untouched.
