# Peyce · Part 3.1

Peyce (pronounced “pace”) is a research/design package and clickable Vue design prototype. It explores five original, optional face questions and transparent exercise choices. This coursework prototype is for fictional design review. No person is monitoring it; it is not a support service. **Work stops at Part 3.1.**

The exported [clickable HTML prototype](submissions/3.1/prototype.html) embeds the Vue build, images and licensed fonts. Open it locally in a browser for fictional review. Direct file opening was blocked by the agent browser policy; the Vue source was tested through the loopback preview.

## Run the prototype

Requires Node 24 (verified: 24.12.0) and npm (verified: 11.6.2).

```sh
cd frontend
npm ci
npm run dev
```

Open the printed local address: `http://127.0.0.1:5181/`. The server binds to the laptop's loopback interface. There is no hosted deployment. `npm run verify` runs the routing/clock tests and builds the frontend. `npm run build` writes ignored `frontend/dist/`. From the root, `node scripts/export-prototype.mjs` embeds that build into the offline HTML artifact.

## Artifact index

| Artifact | Contents |
| --- | --- |
| [Part 3.1 report](submissions/3.1/report.md) | Submission, immutable source reference, evidence and outstanding questions |
| [Design pipeline](docs/design-pipeline.md) | Compositions, screen contracts, routing table/examples, R/D matrix, timing, future MVC/model/data plan |
| [Research ledger](docs/research.md) | Every requested external source, findings, access limits and inference boundaries |
| [Assignment source](docs/assignment-source.md) | Supplied instructor summary and its provenance |
| [Flow SVG](docs/flow.svg) / [Mermaid source](docs/flow.mmd) | Readable exported design flow |
| [Verification](docs/verification.md) | Actual checks, screenshot index and untested limits |
| [Evidence log](docs/evidence-log.md) | Selected prompts and actual revisions |
| [Assets and provenance](docs/assets/provenance.md) | Original bow/balloon, exact generation prompts and material approximation limits |
| [Font licenses](docs/assets/font-licenses.md) | Locally bundled DM Sans and Playfair Display, OFL licenses |
| [Future backend structure](backend/README.md) | Documented FastAPI/SQLite boundaries only |
| [AI use](AI-USE.md) / [handoff](handoffs/current.md) | Actual tool roles, current status and Part 3.1 stop boundary |

## What is clickable

Opening → optional check-in → explainable suggestion or equal choices → ready → deliberate Start → breathing timing experiment or private 5/4/3/2/1 grounding → neutral ending. Back, skipping, alternatives, stopping, optional balloon color/minimal motion, fictional history and a scripted explanation-failure state are included. Crisis-resource access is independent of answers and available on every screen.

The Vue prototype uses fictional data in memory. It has no account, database, telemetry, microphone, camera, audio, live model call or backend. Reload clears choices; the two Past sessions records are explicitly fictional. Original questions are not STAI or a validated assessment. Matching is a versioned design heuristic, never a total anxiety score. No clinical outcome or blanket accessibility conformance is claimed.

## Implementable future direction

Vue views/components, a controller composable, separate question/matching/clock models, and asset registry demonstrate the intended boundaries. The eventual Vue/FastAPI/SQLite system and bounded model explanation request are designed in the documentation, not implemented. Instructor acceptance of structured button turns as a conversational-model experience is still unresolved. Release prerequisites and measured human timing/usability evidence remain future work.

The independent root is `/Users/jakebutler/Documents/ChatGPT/mental health vF`. The previous `Mental Health` repository was used only for read-only independence/fingerprint checks; no source, assets, database, credentials or history were copied.
