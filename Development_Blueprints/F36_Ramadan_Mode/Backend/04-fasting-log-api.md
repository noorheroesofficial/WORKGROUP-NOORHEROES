# B-04 — Fasting Log API

## 1. Feature Context
Lets a child log a night's fasting status strictly within the range their parent has configured, so that fasting-related content never pressures a child who is medically or age-unready to fast — the parent-configured `fasting_approach` is enforced server-side as a hard boundary, not a client-side suggestion.

## 2. Parent Feature
F.36 — Ramadan Mode

## 3. Sub-feature
1.4 Fasting Log API (ID: **B-04**)

## 4. Objective
Build `POST /v1/ramadan/fasting-logs`, validating the submitted `status` against the child's parent-configured `fasting_approach` and rejecting anything beyond it.

## 5. Business Requirements
- FR-9: fasting-tracking content for young children must avoid pressuring framing; the parent toggle exists to let a parent exclude a child entirely.
- FR-10: three parent-configurable approaches per child — full fast / practice / education-only — child can only log within the allowed range.
- §5 Backend AI prompt item 3: `education_only` cannot submit `fasted_full`/`fasted_practice` (mandatory test).
- Edge Case 3: parent changes a child's fasting approach partway through — existing log entries preserved; no new entries beyond the new scope offered going forward.
- §1.15 Permission States: Fasting Tracker visibility is parent-permissioned per child; hidden, not shown-disabled, if not enabled.

## 6. Existing Architecture
`ramadan` bounded context reusing A.7's Habit Service (`app/habits/`) for the underlying approach-configuration storage where applicable, per PRD §3.3 ("Habit Service (reused, A.7) — Fasting log entries, parent-configured approach enforcement").

## 7. Existing Code to Reuse
- A.7's habit/approach-configuration repository (exact class TBD — confirm against `habits` context in `FAST-API-INSTRUCTIONS.md` §5.11 before implementation; do not invent a class name)
- `app/shared/base_service.py::BaseService`
- `core/deps.py::get_current_child`, `get_current_parent`

## 8. Files to Create
- `app/ramadan/routers/fasting_log_router.py`
- `app/ramadan/services/fasting_log_service.py`
- `app/ramadan/repositories/fasting_log_repository.py`
- `app/ramadan/schemas/fasting_log_schema.py`
- `app/ramadan/models/fasting_log.py`
- `alembic/versions/xxxx_create_fasting_logs_table.py`

## 9. Files to Modify
- `app/ramadan/routers/__init__.py` — register router

## 10. Backend Requirements
- `FastingLogService.create_log(child_id, night, status, requesting_session)`: loads the child's current `fasting_approach` (from A.7's existing configuration store, not duplicated here) and rejects the request if `status` exceeds what that approach allows (`education_only` → only `education_only` accepted; `fasted_practice` → `education_only`/`fasted_practice` accepted; `fasted_full` → all three accepted).
- Enforces the Fasting Tracker is enabled at all for the child before accepting any log — server-side independent enforcement, never trusting client-side hiding alone (§12.2 OWASP Broken Access Control).
- Mid-Ramadan approach change: existing rows are never mutated or deleted; only future submissions are constrained to the new, possibly-narrower scope.
- Idempotent-friendly per `(child_id, night)` — a resubmission for the same night updates rather than duplicates (exact semantics — update vs. reject-duplicate — flagged as a contract detail to confirm against product intent; default to reject-duplicate with a clear error unless told otherwise, since fasting logs are typically a factual daily record, not a replayable event).

## 11. Required API / API Contract
`POST /v1/ramadan/fasting-logs` `{ "child_id", "night", "status": "fasted_full"|"fasted_practice"|"education_only" }` → `200`/`201`. **Auth:** `get_current_child` (or parent-on-behalf, per A.7's existing pattern). **Validation:** `status` bounded by parent-configured approach. **Error Responses:** `403` if `status` exceeds the configured approach; `403` if Fasting Tracker isn't enabled for the child at all; `404` for an invalid `night`.

## 12. Database Requirements
`fasting_logs(log_id PK, child_id FK, night_number, status, logged_at)`; index `(child_id, night_number)`. Append-only per FR-11/§4.4 (no soft-delete).

## 13. Validation
`status` enum-constrained to the three values; `night` bounded `1..30`; server-side cross-check against the child's live `fasting_approach` on every write (never cached at request time — approach could have just changed).

## 14. Authentication
`get_current_child` / `get_current_parent` (on-behalf submission per A.7's existing session pattern).

## 15. Authorization
Child may only log for themselves; parent-on-behalf (if supported by A.7's pattern) scoped to their own family's children only.

## 16. Error Handling
Attempted `status` beyond the configured approach → `403` with a clear, child-safe error message (never framed as failure/shame, consistent with platform's anti-shaming philosophy). Tracker-not-enabled → `403`.

## 17. Offline First
Log submissions queue via B.15's existing outbox when offline (client-side concern, K-03) — this endpoint must be safely replay-tolerant for a queued-then-synced submission (see idempotency note in §10).

## 18. Local Data
N/A server-side.

## 19. Localization
N/A — status values are enum codes; display strings are client-side.

## 20. RTL
N/A.

## 21. Analytics
`ramadan_fasting_log_entry_added`, `ramadan_fasting_approach_changed` (the latter emitted by A.7's approach-configuration endpoint, not this one — cross-reference, do not duplicate emission).

## 22. Performance
Lightweight single-row write; no special caching needed (write-heavy, read-light table).

## 23. Security
Server-side approach-boundary enforcement is this sub-feature's core guarantee — client-side hiding of disallowed options (K-03) is a UX convenience only, never the actual security boundary.

## 26. Library Requirements
FastAPI, Pydantic v2, SQLAlchemy 2.0 async. No new libraries.

## 27. Testing
Unit: enum/approach-boundary validation logic for all three approach levels. Integration: **mandatory** — `education_only` child's `fasted_full`/`fasted_practice` submission is rejected (Backend AI prompt item 3); mid-Ramadan approach-change test confirming prior entries preserved and only future entries constrained; tracker-not-enabled rejection test.

## 28. Documentation
OpenAPI docstring enumerating the three status values and their approach-gating rules explicitly.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Write Migration for `fasting_logs`**
Objective: Append-only log table. Files to Create: `alembic/versions/xxxx_create_fasting_logs_table.py`, `models/fasting_log.py`. Tests: migration test. Definition of Done: schema created.

**Task 02 — Define Request/Response Schemas**
Objective: `FastingLogCreateRequest`/`Response` with the three-value enum. Files to Create: `schemas/fasting_log_schema.py`. Dependencies: Task 01. Tests: schema validation tests. Definition of Done: tests pass.

**Task 03 — Implement `FastingLogRepository`**
Objective: `(child_id, night_number)`-indexed writes/reads. Files to Create: `repositories/fasting_log_repository.py`. Dependencies: Task 01. Tests: repository tests. Definition of Done: tests pass.

**Task 04 — Implement `FastingLogService` with Approach-Boundary Enforcement**
Objective: Cross-check every write against the child's live `fasting_approach` from A.7. Existing Files to Reuse: A.7's approach-configuration repository (confirm exact class). Files to Create: `services/fasting_log_service.py`. Dependencies: Task 03. Tests: **mandatory** — `education_only` rejection test. Definition of Done: test passes.

**Task 05 — Implement Tracker-Enabled Gate**
Objective: Reject writes for a child whose tracker isn't parent-enabled. Dependencies: Task 04. Tests: gate-rejection test. Definition of Done: test passes.

**Task 06 — Implement the Router Endpoint**
Objective: `POST /v1/ramadan/fasting-logs`. Files to Create: `routers/fasting_log_router.py`. Files to Modify: `routers/__init__.py`. Dependencies: Task 05. Tests: endpoint integration tests. Definition of Done: tests pass.

**Task 07 — Implement Mid-Ramadan Approach-Change Handling**
Objective: Confirm prior-entry preservation, future-only constraint. Dependencies: Task 04. Tests: **mandatory** — approach-change edge-case test. Definition of Done: test passes.

**Task 08 — Add Full Test Suite**
Objective: Complete coverage per §27. Definition of Done: all green in CI.

**Task 09 — Final Code Review**
Objective: Confirm the approach-boundary check reads live configuration on every request, never a stale/cached value. Definition of Done: checklist in §30 checked.

## 30. Final Verification Checklist
- [ ] `education_only` child cannot submit `fasted_full`/`fasted_practice` — mandatory test passing
- [ ] Tracker-not-enabled requests rejected server-side independent of client UI
- [ ] Mid-Ramadan approach change preserves prior entries, constrains only future ones
- [ ] Approach check reads live configuration, not a stale/cached value

## 31. Definition of Done
No child can ever log a fasting status beyond what their parent has explicitly configured, enforced as an unbypassable server-side boundary — this module's most important child-wellbeing guarantee alongside K-04's gamification suppression.
