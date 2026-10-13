# Future backend design only

Part 3.1 implements no backend. This folder documents an eventual Python/FastAPI and SQLite boundary; it contains no runnable API, database, account system, model call, or deployment configuration. The Vue prototype keeps fictional answers and sessions in memory. Reloading may reset them.

## Proposed structure, not implemented paths

```text
backend/
  app/
    main.py                     # future FastAPI composition root
    schemas/session.py          # validated session and structured-turn contracts
    schemas/explanation.py      # bounded explanation input/output
    controllers/session.py      # consent, lifecycle, explicit choices
    services/matching.py        # versioned deterministic rule service
    services/explanations.py    # one bounded call, validation, canned fallback
    repositories/sessions.py    # minimal SQLite persistence boundary
    content/skills.json         # reviewed immutable exercise copy and versions
  tests/                        # future API/privacy/contract tests
```

These comments describe responsibilities, not files that exist. The future server must implement the same approved matching policy as the client and retain the policy version used for each offered result. A model must not select a skill, change timing or instructions, infer a clinical profile, or control support access.

## Proposed contracts

- `POST /sessions`: create a session only after an explicit future persistence/consent decision; return session ID, content version, and rule version.
- `PUT /sessions/{id}/turns/{index}`: record the exact question version and answer ID or explicit skip, with a sequence/revision. Replacing a turn invalidates the previous offered recommendation.
- `POST /sessions/{id}/recommendation`: compute the approved rule result first; make at most one small explanation request with a timeout and schema validation. Return the rule result immediately with a scripted fallback whenever model output is unavailable. Client exercise access never waits for a model.
- `PATCH /sessions/{id}/lifecycle`: record an explicit exercise selection and paused/completed/stopped state. Never convert lack of an event into a clinical conclusion.
- `GET /sessions`: return only the user’s opted-in history; access, deletion, retention, authentication, encryption, and security policy remain release prerequisites.

Route names are proposals, not callable endpoints. Accounts and security details are deliberately unresolved, not implicitly safe. See [the session/model schema and limits](../docs/design-pipeline.md#future-session-and-conversation-contract).

SQLite is the intended eventual store; there is no real database in this submission. No microphone, camera, social-media dataset, diagnostic score, or hidden clinical profile is planned. Future runtime databases, secrets, environments, and dependencies must remain ignored by Git.
