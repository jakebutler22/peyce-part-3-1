# Assignment source and provenance

Peyce (“pace”) Part 3.1 is a research/design submission with a clickable design prototype. The controlling user request stops at Part 3.1, protects the previous project, permits scoped dependencies and source publication, and prohibits deployment of a support service.

The full supplied master prompt is archived in [prompts/01-peyce-3.1.md](../prompts/01-peyce-3.1.md). The new repository’s [AGENTS.md](../AGENTS.md) records the supplied working rules. The prompt says the instructor overview originally arrived as five screenshots in a planning conversation; those original research screenshots were not available during the first design pass. On 2026-10-13, the user additionally supplied the full assignment overview as pasted text and a screenshot of the Part 3.1 submission page. Both were read for submission preparation. The pasted overview refers to an R/D table but does not include the table itself; its mention counts below still come from the earlier supplied summary. Canvas was not accessed. Private course/account screenshots and the original course attachment are not publication artifacts.

## Directly supplied milestone and submission requirements

The Part 3.1 design paragraph asks for an implementable main experience with a sketch or flow diagram, the model's role, expected stored data, important decisions connected to the instructor's R/D findings, personalization and user control, alternatives/tradeoffs, and unresolved questions. README, AGENTS and design notes must be useful. The overview explicitly states that a working application is not expected at this milestone and permits small design experiments.

The following implementation paragraph describes the next milestone: completing a skill through the running interface, a real model contribution, SQLite persistence, measured duration and failure/exit behavior. The later completion/evaluation paragraphs describe fifteen fictional scenarios, live-model variation, demonstration/process recordings and clean-checkout evidence. Those later requirements are not Part 3.1 deliverables and are not claimed complete here.

Section 8 requires one `report.md` per part, with a repository URL, a commit identifying the submitted version, accessible links to milestone-relevant design/evidence/recordings, a brief completion/evidence/unresolved account, AI-USE in the repository and a curated redacted evidence log containing a failed or revised approach. No Part 3.1 recording requirement appears in the supplied overview. The submission screenshot shows one upload and a single fulfillment criterion with Complete = 100 points; its hidden longer rubric description was not supplied. A score cannot be established by an agent audit.

## Supplied instructor overview

The ongoing study summary involved 15 patients, 13 clinicians, 15 prototype evaluations, and 150 participant-task combinations. The counts below indicate mentions in that supplied summary, not clinical effect sizes. This study is separate from Austin et al.’s 2020 JMIR study.

| Finding | Supplied count | Meaning in the brief |
| --- | ---: | --- |
| R1 | 38 | Around 60 seconds comfortable; attention declines beyond 90–100 seconds. |
| R2 | 30 | Frictionless crisis access. |
| R3 | 39 | Stop or leave without penalty. |
| R4 | 68 | Control and choice rather than automatic routing. |
| D1 | 54 | Simplify as distress rises; no reliable detector is supplied. |
| D2 | 100 | One action/skill at a time. |
| D3 | 148 | Minimize disclosure and emotional effort. |
| D4 | 31 | Persistent safety access, including inside exercises. |
| D5 | 49 | Personalization without configuration burden. |
| D6 | 97 | Low stimulus, nonjudgmental language, no condescending cheerfulness. |

## Assignment requirements versus design choices

**Supplied requirements:** research/design artifacts; implementable screens and flow; eventual Vue/FastAPI/SQLite direction; conversational model context and persistent session/conversation history in the future design; breathing with 4-second inhale, 6-second exhale, six cycles and no hold; grounding in 5/4/3/2/1 sense order; short exercises and ongoing control; evidence, limitations, AI disclosure, verification, and a source reference.

**Current design choices:** five original face questions, button-led structured turns, deterministic matching, editorial split entry screen, central single-question composition, bow/balloon presentation, private notice-and-Next grounding, 48-pixel minimum control target, scripted explanations, and fictional in-memory history. These choices are not instructor-approved clinical procedures, validated measures, or proven consequences of the external sources. The five questions are neither STAI items nor a shortened/adapted STAI.

The instructor’s acceptance of a button-led exchange as the eventual conversational experience remains a question to resolve before later model integration; it does not delay this design submission. Future implementation, recordings, broader scenario evaluation, model integration, and release evidence belong to later work and are not claimed complete by this package.

## Review and safety boundary

This source may be public as coursework. The prototype must not be offered, deployed, linked, or recommended as a service someone can rely on during distress. Fictional scenario review by a peer is design feedback only. No clinical readiness, actual user benefit, student personal review, or instructor approval is inferred from automated checks. Public-release prerequisites are in [design-pipeline.md](design-pipeline.md).
