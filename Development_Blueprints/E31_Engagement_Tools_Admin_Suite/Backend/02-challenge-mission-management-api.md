# B-02 — Challenge & Mission Management API

> **Reconciliation note (2026-08-18):** A.11 Rewards System's own blueprint originally specified an equivalent admin surface at `A11_Rewards_System/Backend/11-admin-mission-challenge-scheduler-api.md` (B-11). That file is now marked deprecated in favor of this one — this file (E.31 B-02) is authoritative for mission/challenge admin CRUD.

## 1. Feature Context
Part of **Feature E.31 — Engagement Tools Admin Suite**. Delivers the admin CRUD surface for daily missions, weekly challenges, and seasonal events consumed by the child-facing Reward/Habit systems (A.7/A.11). Source: PRD §1.7 FR-2, §3.4, §5 item 5.

## 2. Parent Feature
Feature E.31 — Engagement Tools Admin Suite

## 3. Sub-feature
1.2 Challenge & Mission Management API (Backend ID: **B-02**)

## 4. Objective
Let content admins author the daily mission pool, weekly challenges, and seasonal events, with hard server-side enforcement that weekly challenges never overlap in date range for the same age band, and that the daily mission pool always has enough variety per age band to avoid repetition.

## 5. Business Requirements
- FR-2 (PRD §1.7): screens — daily mission template pool, weekly challenge builder, seasonal event scheduler, challenge calendar view. CRUD: create, read completion rates, update reward/threshold, archive.
- **Hard rule:** weekly challenges cannot overlap in date range per age band.
- **Hard rule:** `ends_at > starts_at`.
- **Hard rule:** `goal_type` must match a supported event type.
- Edge Case 3 (PRD §1.10): two admins simultaneously creating overlapping challenges — the second to actually complete (by timestamp) is rejected, regardless of draft-start order.
- Acceptance Criteria (PRD §1.9): overlapping weekly-challenge date ranges for the same age band must be rejected.

## 6. Existing Architecture
Extends A.11's Reward Service (challenge/mission linkage) per PRD §3.3. FastAPI/SQLAlchemy 2.0/PostgreSQL, following the same Router → Service → Repository layering as B-01.

## 7. Existing Code to Reuse
- A.11's existing mission/challenge domain concepts and reward-linkage logic (this sub-feature does not reimplement reward issuance).
- A.7's event-type registry (for `goal_type` validation) if shared, or A.11's own registry if goal types are reward-domain specific.
- E.28's audit log client and RBAC dependency.
- E.29's upload-safety pipeline, if challenge templates carry imagery.

## 8. Files to Create
- `app/routers/admin/challenges_router.py`
- `app/schemas/admin/challenge_schemas.py`
- `app/services/admin/challenge_admin_service.py`
- `app/repositories/admin/challenge_admin_repository.py`
- `tests/admin/test_challenge_admin_api.py`
- `migrations/versions/xxxx_add_challenge_age_band_overlap_index.py`

## 9. Files to Modify
- `app/routers/admin/__init__.py`
- `app/core/audit.py` (add `challenge.created`, `challenge.updated`, `challenge.archived`, `weekly_challenge_overlap_rejected`)

## 10. Backend Requirements
- **Database:** `challenges`/`missions` tables (new or extended from A.11), with `age_band`, `starts_at`, `ends_at`, `goal_type`, `reward_config`, `status`.
- **Migration:** add a constraint-supporting index on `(age_band, starts_at, ends_at)` for efficient overlap detection; consider a PostgreSQL exclusion constraint (`EXCLUDE USING gist`) on `(age_band WITH =, daterange(starts_at, ends_at) WITH &&)` for true atomic overlap prevention at the DB layer, since the application-layer check-then-insert has a race window (Edge Case 3).
- **Model:** `Challenge`, `Mission` (daily pool entries), `SeasonalEvent`.
- **Schema/DTO:** `ChallengeCreate` (target, reward, `starts_at`, `ends_at`, `age_band`, `goal_type`), `ChallengeUpdate` (reward/threshold only), `MissionCreate`.
- **Repository:** `create()`, `list_with_completion_rates()`, `update_reward_threshold()`, `archive()`, `check_overlap()`.
- **Service:** orchestrates overlap validation, `goal_type` registry validation, audit logging.
- **Router:** `POST /v1/admin/challenges`, `GET /v1/admin/challenges`, `PATCH /v1/admin/challenges/{id}`, `POST /v1/admin/challenges/{id}/archive`.
- **Dependency Injection:** `get_current_admin`, `require_role("content_editor")`.
- **Authentication/Authorization:** admin JWT, `content_editor`+.
- **Validation:** `ends_at > starts_at`; `goal_type` in registry; date-range/age-band overlap check.
- **Business Rules:** overlap rejection must be atomic — prefer a DB-level exclusion constraint over an application read-then-write check to correctly handle Edge Case 3's concurrent-submission race.
- **Exception Handling:** `409 DATE_RANGE_OVERLAP` on constraint violation, translated from the DB integrity error.
- **Logging:** structured logs including rejected-overlap attempts (feeds `weekly_challenge_overlap_rejected` analytics event).
- **Caching:** invalidate any cached "active challenges by age band" list on write.
- **Transaction:** create/update wrapped in a transaction; rely on DB constraint for atomicity rather than an application-level lock.
- **Pagination/Filtering/Sorting:** list endpoint supports pagination, filter by age_band/status/type, sort by starts_at.

## 11. KMP Requirements
N/A — admin-only. KMP app continues consuming A.7/A.11's existing child-facing challenge endpoints.

## 12. NextJS Requirements
Consumed by **N-02 Challenge & Mission Management UI**. The UI's client-side overlap pre-check (fast UX warning) is advisory only — this backend's DB-level rejection remains authoritative per PRD §7 item 4.

## 13. API Contract

### `POST /v1/admin/challenges`
- **Authorization:** `content_editor`+
- **Request:**
```json
{
  "type": "weekly_challenge",
  "title_key": "ramadan_fasting_challenge",
  "target": 5,
  "goal_type": "habit_checkin_count",
  "reward_config": { "xp_bonus": 100 },
  "starts_at": "2026-09-01T00:00:00Z",
  "ends_at": "2026-09-08T00:00:00Z",
  "age_band": "6 to 9"
}
```
- **Response (201):** full `ChallengeRead` object
- **Error Responses:** `401`, `403`, `422 VALIDATION_ERROR`, `409 DATE_RANGE_OVERLAP`, `422 INVALID_GOAL_TYPE`

### `GET /v1/admin/challenges`
- Query params: `page`, `page_size`, `age_band`, `status`, `type`
- Response includes `completion_rate` per item

### `PATCH /v1/admin/challenges/{id}`
- Request: `{ "target": 6, "reward_config": { "xp_bonus": 120 } }`
- Response: updated `ChallengeRead`

### `POST /v1/admin/challenges/{id}/archive`
- Response: `{ "id": "uuid", "status": "archived" }`

## 14. Database Requirements
- `challenges` table with exclusion constraint on `(age_band, daterange(starts_at, ends_at))` to guarantee atomic non-overlap.
- `missions` table for the daily pool (no date-range overlap constraint needed — pool entries are not date-bound the same way).
- Index `(age_band, starts_at, ends_at)`.

## 15. Validation
`ends_at > starts_at`; `goal_type` ∈ registered event types; `age_band` valid; `target` positive integer.

## 16. Authentication
Admin JWT (E.28).

## 17. Authorization
`content_editor`+ for mutations; broader read access per E.28 RBAC matrix.

## 18. Error Handling
| Scenario | Response |
|---|---|
| Overlapping date range, same age band | `409 DATE_RANGE_OVERLAP` |
| `ends_at <= starts_at` | `422 VALIDATION_ERROR` |
| Unregistered `goal_type` | `422 INVALID_GOAL_TYPE` |
| Unknown challenge id | `404 NOT_FOUND` |
| Unauthenticated/forbidden | `401`/`403` |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
`title_key`/description reference localization keys (English/Hindi/Arabic/Urdu), not raw strings, consistent with platform pattern.

## 22. RTL
N/A at API layer.

## 23. Analytics
`mission_created`, `weekly_challenge_created`, `weekly_challenge_overlap_rejected` (internal), `seasonal_event_scheduled` (PRD §1.19).

## 24. Performance
DB-level exclusion constraint avoids race-prone read-then-write overlap checks under concurrent load; completion-rate aggregation should use an indexed/materialized approach for scale.

## 25. Security
All mutations audit-logged; no PII exposure; role-scoped per E.28.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Pydantic v2, PostgreSQL `btree_gist` extension (for the exclusion constraint), pytest-asyncio.

## 27. Testing
- Unit: validation logic, goal_type registry checks.
- Integration: overlap rejection; concurrent-submission race test (fire two overlapping creates simultaneously, confirm exactly one succeeds).
- Edge cases: Edge Case 3 (concurrent overlapping submissions).
- Negative cases: `ends_at <= starts_at`, invalid goal_type, unauthorized.

## 28. Documentation
OpenAPI docs; explicit note on the exclusion-constraint-based overlap guarantee for future maintainers.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Database Model & Exclusion Constraint**
- Task ID: B-02-T01
- Objective: Create/extend `Challenge`/`Mission` models with a PostgreSQL exclusion constraint guaranteeing atomic non-overlap per age band.
- Why Required: Edge Case 3 requires the guarantee to be race-proof, not just application-checked.
- Files to Create: `app/models/challenge.py` (if not present), migration enabling `btree_gist` extension and adding the exclusion constraint.
- Validation: `ends_at > starts_at` as a `CHECK` constraint.
- Tests: migration test; constraint-violation test.
- Dependencies: none.
- Do Not Change: A.11's existing reward-issuance tables.
- Definition of Done: constraint verified via direct SQL insert test.

**Task 02 — Repository Layer**
- Task ID: B-02-T02
- Files to Create: `app/repositories/admin/challenge_admin_repository.py`.
- Implementation Details: `create()` catches `IntegrityError` from the exclusion constraint and re-raises as `DateRangeOverlapError`.
- Dependencies: Task 01.
- Definition of Done: unit tests green.

**Task 03 — Service Layer**
- Task ID: B-02-T03
- Files to Create: `app/services/admin/challenge_admin_service.py`.
- Implementation Details: `goal_type` registry validation before DB insert attempt; audit logging.
- Dependencies: Task 02.
- Definition of Done: unit tests green with mocked repository.

**Task 04 — API Endpoints**
- Task ID: B-02-T04
- Files to Create: `app/routers/admin/challenges_router.py`.
- Implementation Details: map `DateRangeOverlapError` → `409`; map registry errors → `422`.
- Dependencies: Task 03.
- Definition of Done: integration tests green.

**Task 05 — Concurrency Regression Test**
- Task ID: B-02-T05
- Objective: Prove Edge Case 3's guarantee.
- Implementation Details: use `asyncio.gather` to fire two overlapping challenge-create requests simultaneously against the same age band; assert exactly one `201` and one `409`.
- Tests: `tests/admin/test_challenge_admin_api.py::test_concurrent_overlapping_challenge_creation`.
- Dependencies: Tasks 01–04.
- Definition of Done: test passes deterministically across multiple runs (not flaky), part of CI-blocking suite.

**Task 06 — Documentation & Final Review**
- Task ID: B-02-T06
- Dependencies: Tasks 01–05.
- Definition of Done: checklist in §31 fully verified.

## 30. Definition of Done
All endpoints implemented and tested; overlap rejection proven atomic under concurrency; audit logging in place; OpenAPI docs complete.

## 31. Final Verification Checklist
- [ ] Weekly challenge overlap rejected for same age band (`409`)
- [ ] Concurrent overlapping submissions: exactly one succeeds (regression test green)
- [ ] `ends_at <= starts_at` rejected
- [ ] Invalid `goal_type` rejected
- [ ] Completion-rate read endpoint functional
- [ ] Archive sets status without deleting historical data
- [ ] Audit log entries written for every mutation
- [ ] Unauthorized/forbidden paths tested
- [ ] No school/madrasa/institutional-tier logic introduced
- [ ] PostgreSQL/Redis credentials untouched
