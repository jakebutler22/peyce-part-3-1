# Peyce Part 3.1 — evidence ledger

Access date for every entry: **October 13, 2026 (America/New_York)**. Sources were reopened with the browsing tool during this work. “Accessible” means readable page/source text, not that an interactive demonstration was run. All cited evidence below comes from the publisher, institution, standards body, or project's own repository. Summaries are paraphrases; protected assessment items, scoring keys, conversation datasets, and model weights are not reproduced.

The supplied instructor overview is a separate source, summarized in [assignment-source.md](assignment-source.md). It describes **15 patients, 13 clinicians, 15 prototype evaluations, and 150 participant-task combinations**. Its R/D counts are mentions, not effect sizes. It is **not** the Austin et al. JMIR study below. External sources supplement the instructor's requirements; they do not validate Peyce's five original questions or its routing rules.

## 1. State/trait distinction and instrument boundary

**Metadata:** Mind Garden, *State-Trait Anxiety Inventory for Adults (STAI-AD)*, author Charles D. Spielberger; publisher product page, no page publication date shown. The page identifies copyright years 1968 and 1977. [Publisher source](https://www.mindgarden.com/145-state-trait-anxiety-inventory-for-adults).

**Access:** Product description, specifications, and administration-license description readable. No licensed manual or scoring key acquired.

**Finding:** The publisher distinguishes anxiety experienced at a particular time from a more enduring tendency. The instrument has two 20-item scales, with four possible responses per item. Administration outside the publisher's platform requires a purchased license.

**Peyce implication (design inference):** Ask about current experience and willingness without labeling the person. Write original, optional, question-specific face labels and explain that the check-in is a design heuristic.

**Does not establish:** Peyce is not STAI, shortened STAI, a validated anxiety measure, or an adaptation inheriting its norms. Three faces and five original questions have no psychometric validity established here. No protected item wording or STAI scoring is used.

## 2. App access within ongoing DBT

**Metadata:** Austin, S. F., Jansen, J. E., Petersen, C. J., Jensen, R., & Simonsen, E. (2020). *Mobile App Integration Into Dialectical Behavior Therapy for Persons With Borderline Personality Disorder: Qualitative and Quantitative Study*. **JMIR Mental Health, 7**(6), e14913. Published June 11, 2020. [Full article](https://mental.jmir.org/2020/6/e14913/); [DOI](https://doi.org/10.2196/14913). The duplicate supplied JMIR link is consolidated here.

**Access:** Full article page readable, including abstract, methods, discussion, and limitations.

**Finding:** Twenty-four participants receiving DBT used the app; 20 completed questionnaires and eight were interviewed. Participants perceived easier access to strategies and a shared information source with therapists. The authors note a small sample, perceptions that may differ from behavior, and no systematic symptom, behavior-change, or alliance measurement.

**Peyce implication (design inference):** Make skill access direct and language clear; distinguish a coursework prototype from professionally integrated care.

**Does not establish:** Standalone treatment effectiveness, clinical outcomes for Peyce, crisis coverage, or clinically valid selection from its faces. This sample is separate from the instructor's ongoing study.

## 3. Target distance and width

**Metadata:** Wallner, S., Danet, O., Eilersen, T., & Tved, J. (2012), *An Interactive Visualisation of Fitts's Law with JavaScript and D3*, University of Copenhagen course project. [Requested live demo](http://simonwallner.at/ext/fitts/); [repository](https://github.com/SimonWallner/uit-fitts-law); [README](https://github.com/SimonWallner/uit-fitts-law/blob/master/readme.md); [HTML source](https://github.com/SimonWallner/uit-fitts-law/blob/master/index.html).

**Access:** Both HTTP and HTTPS demo requests returned a browsing-tool “Internal Error.” Repository README and HTML source were readable. **The live demo was not run.**

**Finding:** The authors illustrate the relationship between target distance, width, and movement difficulty. HTML explicitly describes an educational illustration rather than a controlled experiment. The README contains MIT licensing text, credited to Simon Wallner and Jesper Tved; GitHub's absent license badge does not negate that text.

**Peyce implication (design inference):** Keep equal face targets generous, stationary, and separated, with reachable Back/Skip controls. Our approximate 80-pixel face areas and 48-pixel control minimum are design targets.

**Does not establish:** An exact pixel requirement, measured click-time improvement, or optimal layout for distress. The legacy D3 stack is not a dependency recommendation. Any future source copying would require retaining relevant license notices and checking library licenses.

## 4. DBT context and comprehensive-care boundary

**Metadata:** University of Washington, Behavioral Research & Therapy Clinics, *Dialectical Behavior Therapy*, institutional overview; no page publication date shown. [Institutional source](https://depts.washington.edu/uwbrtc/about-us/dialectical-behavior-therapy/).

**Access:** Full overview text readable.

**Finding:** The page describes acceptance and change; mindfulness, distress tolerance, emotion regulation, and interpersonal effectiveness; and four comprehensive DBT components: skills training, individual treatment, phone coaching, and a therapist consultation team.

**Peyce implication (design inference):** Contextualize brief present-focused practice and respectful choice. Preserve the ability to decline, switch, or stop rather than defining the person by a response.

**Does not establish:** That these two prototype exercises constitute comprehensive DBT, therapy, coaching, or clinical care. Treatment-effect statements about DBT cannot be transferred to Peyce. The overview does not validate the original check-in or the matching policy.

## 5. Interpretable model research and its limits

**Metadata:** SteveKGYang/MentalLLaMA repository, *MentaLLaMA: Interpretable Mental Health Analysis on Social Media with Large Language Models*; Kailai Yang and collaborators, repository README noting WWW 2024 acceptance. [Repository/README](https://github.com/SteveKGYang/MentalLLaMA); [LICENSE](https://github.com/SteveKGYang/MentalLLaMA/blob/main/LICENSE).

**Access:** README, ethical-considerations section, and LICENSE readable. No models or datasets installed or evaluated for this ledger.

**Finding:** The project studies mental-health analysis of social-media text with generated explanations. Its ethical statement limits material to non-clinical research, disclaims diagnosis/advice, and identifies risks from incorrect predictions, inappropriate explanations, bias, and overgeneralization. The LICENSE is MIT, copyright 2023 NaCTeM.

**Peyce implication (design inference):** Store explanation provenance separately from structured answers. The planned model may briefly explain an approved deterministic rule result; validated canned text remains available on delay or failure.

**Does not establish:** Valid interpretation of three-face answers, safe exercise matching, clinical safety, or the truth of an explanation because it sounds plausible. Code licensing does not settle all weight, base-model, and dataset rights. No diagnostic examples, social-media data, or training pipeline are needed for Part 3.1.

## 6. Counseling-language benchmarks as a contrast

**Metadata:** EmoCareAI/ChatPsychiatrist repository, README titled *ChatPsychiatrist*, linking *ChatCounselor: A Large Language Models for Mental Health Support* and reporting PGAI CIKM 2023 acceptance. README dates its first release July 28, 2023. [Repository/README](https://github.com/EmoCareAI/ChatPsychiatrist); [LICENSE](https://github.com/EmoCareAI/ChatPsychiatrist/blob/master/LICENSE).

**Access:** README and Apache-2.0 license header readable. No counseling transcripts, weights, or training code imported for this ledger.

**Finding:** The README describes counseling-domain fine-tuning and language-content evaluation. Its single-turn comparison is judged by GPT-4 using counseling-skill categories. These are reported language/benchmark results, not clinical outcome measurements.

**Peyce implication (design inference):** Use this as a contrast: limit the future model to concise explanation of structured turns and approved content. Exclude open-ended therapeutic chat, diagnostic personas, generated exercise instructions, and model control over refusals, timing, or support access.

**Does not establish:** Effective treatment, safe deployment, clinical outcomes, or validation of Peyce's matching rules. The repository's treatment-recommendation claims are not adopted. An Apache-2.0 code license is not blanket clearance for counseling data or model weights.

## 7. Click speed is not an anxiety detector

**Metadata:** Macaulay, M. (2004). *The speed of mouse-click as a measure of anxiety during human-computer interaction*. **Behaviour & Information Technology, 23**(6), 427–433. [Publisher abstract](https://www.tandfonline.com/doi/abs/10.1080/01449290412331294651); [DOI](https://doi.org/10.1080/01449290412331294651).

**Access:** Direct publisher open returned a browsing-tool “Internal Error.” A publisher-domain search result exposed the article metadata and abstract. **Full text was not accessed.** The journal volume is 2004; the page separately reports online publication November 8, 2010. The later online date does not replace the volume citation.

**Finding:** The abstract reports two groups of 30 under different interaction conditions. It found no correlation between mouse-click speed and state anxiety, although click speed differed across groups/conditions.

**Peyce implication (design inference):** Never infer anxiety or route exercises using click speed, hesitation, pointer paths, device, or face color alone. Responses express content or preference; they are not covert measurements.

**Does not establish:** That every imaginable behavioral signal is useless. Abstract-only access prevents inspection of detailed measures and statistical analyses; no broader claim is made.

## 8. Gentle breathing technique; different duration

**Metadata:** NHS, *Breathing exercises for stress*. Page last reviewed June 12, 2026; next review due June 12, 2029. [Official guidance](https://www.nhs.uk/mental-health/self-help/guides-tools-and-activities/breathing-exercises-for-stress/).

**Access:** Full guidance page readable.

**Finding:** Guidance describes comfortable, unforced breathing, gentle nasal inhalation and exhalation through the mouth. Its example optionally counts up to five each way and repeats for at least five minutes.

**Peyce implication (design inference):** Use comfortable, non-demanding copy. The balloon is a timing metaphor, with no respiratory sensing; stopping, returning to normal breathing, or switching remains available.

**Does not establish:** An optimal 4-second inhale/6-second exhale dose, six-cycle protocol, or benefit in one minute. Peyce's 60-second pacing and ≤90-second intended complete exercise budget come from the course brief and explicit design assumptions, not this NHS example. Technique guidance is not medical suitability screening.

## 9. Predictable controls and accessibility targets

### 9a. Target Size (Enhanced)

**Metadata:** W3C Web Accessibility Initiative, WCAG 2.2 Understanding document for **SC 2.5.5, Target Size (Enhanced), Level AAA**. [W3C source](https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html).

**Access:** Full explanatory page readable. Understanding documents explain the criteria; they are informative rather than the normative standard itself.

**Finding:** The enhanced target criterion uses at least 44×44 CSS pixels for pointer targets, with equivalent-target, inline, user-agent-control, and essential exceptions. It discusses the difficulty of small targets and the value of larger targets for sequential actions.

**Peyce implication (design inference):** Set a deliberate ≥48×48 CSS-pixel control target and larger equal face areas where space permits; measure rendered bounds at laptop and simulated mobile sizes rather than infer them from appearance.

**Does not establish:** That 48 pixels follows mathematically from Fitts's law, that every inline link must be 44 pixels, or that Peyce meets all WCAG requirements. Contrast, focus, keyboard use, alternatives, reflow, and motion need separate checks.

### 9b. On Input

**Metadata:** W3C Web Accessibility Initiative, WCAG 2.2 Understanding document for **SC 3.2.2, On Input, Level A**. [W3C source](https://www.w3.org/WAI/WCAG22/Understanding/on-input.html).

**Access:** Full explanatory page readable.

**Finding:** A change to a control's setting should not unexpectedly change context without advance notice. The document distinguishes setting changes from deliberate link/button activation; state-changing buttons can fall within its discussion.

**Peyce implication (design inference):** Explain before check-in that choosing a face advances once. Activate only on deliberate click/keyboard input, briefly confirm selection, move focus predictably, prevent repeated activation from answering a later question, and allow correction with Back. These are applied design safeguards, not proof that any auto-advance implementation conforms.

**Does not establish:** That notice alone guarantees accessible progression, or that a passed build/test suite proves WCAG conformance. Verify real focus order, screen-reader behavior, keyboard activation, and correction; record device/assistive-technology limitations.

## Research verification and unresolved evidence

**CHECK:** Read the complete saved Part 3.1 prompt and applicable AGENTS instructions. Confirm the canonical independent project path before writing this ledger. Scope research to the nine supplied source groups; consolidate the duplicated JMIR URL.

**TAKE ACTION:** Reopen all requested URLs. Follow repository file links to inspect the Fitts README/HTML, MentaLLaMA LICENSE, and ChatPsychiatrist LICENSE. Retrieve the unavailable Macaulay publisher abstract through a publisher-domain search. Keep clinical, experimental, instructional, benchmark, and standards evidence distinct.

**VERIFY:** All nine requested source groups are represented, including both W3C references. Each entry records metadata, actual access level, relevant finding, design inference, and claim boundary. No proprietary STAI items or scoring are copied. The Fitts live-demo failure and Macaulay full-text limitation remain unresolved; they do not prevent the scoped design decisions above. Repository branches and web pages may change after the stated access date.

None of this research establishes clinical readiness, validates Peyce's routing policy, approves a public support service, or replaces the student's own review. The instructor's acceptance of button-led structured turns as the required conversational experience remains an unresolved course question. Expert content/safety review and real usability evidence belong to future release prerequisites, not claimed Part 3.1 outcomes.
