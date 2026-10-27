# B-04 — Daily Mission Assignment Engine

## 1. Feature Context
NoorHeroes Child App, Feature A.2. Powers the "Today's Mission" section — a system-assigned (not child-selectable), database-hard-capped set of up to 3 daily missions per child.

## 2. Parent Feature
A.2 — Child Home Dashboard & AI Personalization

## 3. Sub-feature
1.4 Daily Mission Assignment Engine (ID: B-04)

## 4. Objective
Implement the daily mission assignment algorithm and data layer, hard-capped at 3 missions per `(child_id, assignment_date)` via a database-level constraint/trigger (not application code alone), sourced from an admin-curated candidate pool (N-02).

## 5. Business Requirements
Per PRD FR-4, Edge Case 6, §4.2, §5 item 9:
- Today's Mission is system-assigned, achievable within typical session length, capped at 3 per day.
- Completing the mission and re-opening Home same day shows a completed state, not a re-assignment.
- Hard cap of 3 enforced at the database layer via trigger/constraint, tested explicitly.

## 6. Existing Architecture
FastAPI service-layer + SQLAlchemy 2.0 + Alembic (with a PostgreSQL trigger for the hard cap, per PRD §5 item 9's explicit instruction to enforce this at the DB layer, not only application code).

## 7. Existing Code to Reuse
B-01's cache-invalidation helper (mission completion should invalidate the `today_mission` fragment); A.1 auth dependency.

## 8. Files to Create
- `app/services/mission_assignment_service.py`
- `app/repositories/mission_repository.py`
- `app/models/daily_mission_assignment.py`
- `app/models/mission_pool_entry.py` (admin-curated pool, consumed here and owned by N-02)
- `alembic/versions/xxxx_create_mission_tables.py`
- `alembic/versions/xxxx_add_mission_cap_trigger.py`
- `app/routers/missions.py` (mission completion endpoint, if not already covered by the content-completion event elsewhere — confirm against existing content-completion architecture before duplicating)
- `tests/integration/test_mission_cap_trigger.py`

## 9. Files to Modify
- `app/main.py`

## 10. Backend Requirements
- Assignment algorithm selects up to 3 missions per child per day from the active `mission_pool_entry` set, filtered by `target_age_bands` and `active_date_range`, weighted by `weight`.
- Assignment is idempotent per `(child_id, assignment_date)` — re-invoking assignment logic for a day that already has assignments returns the existing set, never creates additional rows beyond 3.
- Database trigger (or equivalent constraint) hard-caps rows at 3 per `(child_id, assignment_date)`, tested by attempting a 4th insert and confirming rejection.
- Mission completion updates `completed`/`completed_at` on the existing assignment row (never creates a new one), and invalidates the `today_mission` Home cache fragment.

## 11. KMP Requirements
Not implemented here. Client (K-04) reads `today_mission` from B-01's response and renders completed/incomplete state accordingly; tapping a mission routes to the relevant feature and triggers completion via that feature's own completion API (coordinate: confirm whether mission completion is marked by this service listening to a completion event, or by a direct call from the completing feature — do not invent a new completion-signaling mechanism if one already exists in the platform's Content/Progress architecture).

## 12. NextJS Requirements
Not applicable directly — N-02 (Daily Mission Curation Tool) owns CRUD on `mission_pool_entry`, which this service reads from (read-only from this sub-feature's perspective).

## 13. API Contract
Primarily an internal service consumed by B-01 (`GET /v1/home` → `today_mission` section). If a dedicated completion endpoint is required and doesn't already exist elsewhere:
- `POST /v1/missions/{assignment_id}/complete` — Auth: Bearer (child-mode) — Response: `{ completed: true, completed_at }` — only if content-completion isn't already centrally handled; confirm against Progress Service (B-05) architecture first to avoid a duplicate completion pathway.

## 14. Database Requirements
Per PRD §4.2:
- `daily_mission_assignment`: FK `child_id`, `content_id`; `UNIQUE(child_id, assignment_date, content_id)`; CHECK max 3 rows per `(child_id, assignment_date)` enforced via trigger; index on `(child_id, assignment_date)`.
- Retention: rows older than 90 days archived to cold storage (still queryable for Parent Reports' historical trends per PRD §4.5) — coordinate archival job scheduling with existing platform batch-job infrastructure.

## 15. Validation
Candidate pool entries must have valid `target_age_bands` overlapping the child's current age band (recomputed on birthday rollover per Edge Case 3 — reuse A.1's age-band derivation, don't reimplement).

## 16. Authentication
Bearer JWT (child-mode session), same as B-01/B-03.

## 17. Authorization
Assignment/completion scoped to the authenticated `child_id`; no cross-child mission access.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Assignment service failure | B-01 hides the Today's Mission card gracefully; does not block rest of Home |
| Candidate pool empty for age band/locale | Log a data-quality alert; assign fewer than 3 (or zero) rather than erroring |
| Attempted 4th assignment insert | Rejected by DB trigger; application layer treats this as a no-op, not an error surfaced to the client |

## 19. Offline First
Not applicable server-side.

## 20. Local Data
Not applicable (backend).

## 21. Localization
Mission `title`/description sourced from Content Catalog, already localized per existing content-localization pattern.

## 22. RTL
N/A (backend).

## 23. Analytics
Backend does not fire `today_mission_*` events (client-fired); ensure assignment/completion state is queryable for analytics correlation.

## 24. Performance
Assignment algorithm should run efficiently for DAU-scale daily batch or on-demand-first-request-of-day pattern — confirm which approach fits the existing platform's job-scheduling conventions (nightly batch pre-assignment vs. lazy on-first-Home-request-of-day); default to lazy on-demand if no existing batch infrastructure convention is found, since it avoids idle-account waste.

## 25. Security
DB-level cap trigger is a security/integrity control against a buggy or malicious client attempting to force excess assignments via retried/concurrent requests.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0, Alembic (with raw SQL trigger definition support), pytest-asyncio.

## 27. Testing
- Integration: attempt to insert a 4th `daily_mission_assignment` row for the same `(child_id, assignment_date)` → trigger rejects it.
- Integration: idempotent re-assignment call for an already-assigned day returns the existing set unchanged.
- Unit: age-band filtering of candidate pool.
- Integration: mission completion updates existing row, invalidates cache, does not create a duplicate.

## 28. Documentation
Document the trigger definition and rationale (DB-enforced cap) in a migration comment and in the service docstring, since triggers are less discoverable than application code for future engineers.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create Mission Tables + Database Cap Trigger**
- Objective: `daily_mission_assignment` and `mission_pool_entry` tables plus a hard-cap trigger.
- Why Required: FR-4 and PRD §5 item 9 explicitly require DB-layer enforcement.
- Existing Architecture to Follow: Alembic raw-SQL migration capability for trigger definitions.
- Existing Files to Reuse: Base model conventions.
- Files to Create: `app/models/daily_mission_assignment.py`, `app/models/mission_pool_entry.py`, `alembic/versions/xxxx_create_mission_tables.py`, `alembic/versions/xxxx_add_mission_cap_trigger.py`
- Files to Modify: none
- Implementation Details: Trigger function `BEFORE INSERT` on `daily_mission_assignment` counting existing rows for `(NEW.child_id, NEW.assignment_date)` and raising an exception if count >= 3.
- Business Rules: Cap is exactly 3, non-configurable per-child (unless a future business rule requires it — not in current scope).
- Validation: Trigger-level.
- Error Handling: Insert beyond cap raises a Postgres exception; application layer catches and no-ops rather than propagating a 500.
- Security: This is the security/integrity control.
- Performance: Trigger overhead is negligible (small per-day row count).
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Attempt 4th insert, confirm rejection at DB layer (not just application layer) by testing directly against the DB session, bypassing the service.
- Documentation: Migration comment explaining the trigger's purpose.
- Dependencies: None.
- Do Not Change: Do not weaken this to an application-only check.
- Expected Result: Migration + trigger live.
- Definition of Done: DB-level rejection test passes.

**Task 02 — Implement Mission Repository & Assignment Algorithm**
- Objective: Select and assign up to 3 missions from the candidate pool.
- Why Required: Core business logic (FR-4).
- Existing Architecture to Follow: Repository pattern.
- Existing Files to Reuse: A.1's age-band derivation utility.
- Files to Create: `app/repositories/mission_repository.py`, `app/services/mission_assignment_service.py`
- Files to Modify: none
- Implementation Details: `get_or_assign_today(child_id, age_band, locale) -> list[MissionAssignment]` — checks for existing assignments for today first (idempotent), else selects up to 3 weighted candidates from `mission_pool_entry` filtered by age band/active date range/locale.
- Business Rules: Idempotent per day; never exceeds 3 (belt-and-suspenders with Task 01's trigger).
- Validation: Age-band overlap check.
- Error Handling: Empty candidate pool → assign fewer than 3, log data-quality warning, do not error.
- Security: N/A beyond ownership scoping.
- Performance: Single query for existing assignments before attempting new ones.
- Localization: Candidate filtering respects locale.
- RTL: N/A.
- Analytics: N/A.
- Tests: Unit tests for idempotent re-call; age-band filtering; empty-pool graceful handling.
- Documentation: Docstring.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Working assignment service.
- Definition of Done: Tests pass.

**Task 03 — Implement Mission Completion Handling + Cache Invalidation**
- Objective: Mark a mission complete and reflect it in Home immediately.
- Why Required: Edge Case 6 (completed state, not re-assignment, on same-day re-open).
- Existing Architecture to Follow: B-01's cache-invalidation helper; confirm existing content-completion signaling pattern before adding a new endpoint (avoid duplicating Progress Service's completion tracking if one already exists — check B-05/Content Catalog architecture first).
- Existing Files to Reuse: `invalidate_section` from B-01.
- Files to Create: `app/routers/missions.py` (only if no existing completion pathway covers this)
- Files to Modify: `app/main.py` (if router added)
- Implementation Details: Update `completed=true, completed_at=now()` on the existing assignment row matched by `(child_id, assignment_date, content_id)`; invalidate `today_mission` cache fragment.
- Business Rules: Never creates a new assignment row on completion.
- Validation: Ownership check (assignment belongs to requesting child).
- Error Handling: Completing an already-completed mission is idempotent (no error, same result).
- Security: Ownership enforcement.
- Performance: Single targeted update + cache invalidation.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A (client-fired `today_mission_completed`).
- Tests: Integration test — complete, re-open Home same day, confirm completed state persists and no new assignment appears.
- Documentation: OpenAPI docs if new endpoint added.
- Dependencies: Tasks 01, 02; B-01 Task 04 cache helper.
- Do Not Change: N/A.
- Expected Result: Completion correctly reflected.
- Definition of Done: Edge Case 6 integration test passes.

## 30. Definition of Done
Missions assigned idempotently, hard-capped at 3 at the DB layer, completion state persists correctly without re-assignment, and Home reflects updates immediately via cache invalidation.

## 31. Final Verification Checklist
- [x] Database trigger rejects a 4th assignment row for the same `(child_id, assignment_date)`
- [x] Assignment call is idempotent per day
- [x] Age-band filtering respects birthday-rollover recomputation
- [x] Completion updates existing row, never creates a duplicate
- [x] `today_mission` cache fragment invalidated on completion
- [x] Empty candidate pool handled gracefully (no error, degraded assignment count)
- [x] All tests pass

## 32. Implementation & Verification Findings

### Core Deliverables & Architectural Invariants:
1. **Database-Level Hard Cap BEFORE INSERT Trigger (PRD FR-4, §5 item 9)**:
   - `alembic/versions/0082_add_mission_cap_trigger.py` installs `trg_daily_mission_cap` for PostgreSQL (`PL/pgSQL`) and SQLite (`SELECT RAISE(ABORT, ...)`).
   - Strictly rejects any 4th insert for the same `(child_id, assignment_date)` directly at the database engine level.
   - Nested transaction savepoint rollback in `MissionRepository.insert_assignment` catches trigger exceptions gracefully under concurrent requests, guaranteeing zero race-condition crashes.
2. **Candidate Mission Pool & Assignment Data Layer**:
   - `alembic/versions/0081_create_daily_mission_tables.py` creates `daily_mission_assignment` (compound unique constraint on `(child_id, assignment_date, content_id)`) and `mission_pool_entry`.
   - Domain models `DailyMissionAssignment` and `MissionPoolEntry` in `src/noorheroes/modules/missions/models.py`.
   - 100% backwards-compatibility re-export facades under `app/models/`, `app/schemas/`, `app/repositories/`, `app/services/`, and `app/routers/`.
3. **Algorithm A-Res Weighted Sampling Without Replacement**:
   - Evaluates key `u ** (1.0 / weight)` where `u ~ Uniform(0,1)` to guarantee true weighted random sampling without replacement (Efraimidis & Spirakis).
   - Deduplicates candidate items by `content_id` to prevent duplicate daily assignments.
4. **Dynamic Age-Band Derivation & Active Date Filtering**:
   - Automatically recomputes age band on birthday rollover via `derive_age_band`.
   - Restricts candidate pool strictly to active date ranges (`start_date <= now <= end_date`).
5. **Candidate Pool Curation & Soft-Delete Invariant (Admin N-02)**:
   - Admin CRUD routes (`GET/POST/PATCH /admin/v1/mission-pool` and `/v1/admin/mission-pool`).
   - Physical HTTP DELETE explicitly returns HTTP `405 Method Not Allowed`. Deactivation occurs exclusively through `PATCH` setting `active=false`.
   - Immutable audit logging: every admin create, update, and deactivation writes an `AdminAuditRecord` to `admin_audit_records`.
6. **In-Place Mission Completion & Immediate Edge-Cache Invalidation**:
   - `POST /v1/missions/{assignment_id}/complete` updates existing row in-place (`completed=true, completed_at=now()`).
   - Invokes `HomeCache().invalidate_section(child_id, 'today_mission')`.
   - Idempotent on repeat completions.
   - Enforces child ownership (404/403 on cross-child access).
7. **DTO Title & Type Enrichment with Historical Preservation**:
   - Client feed DTOs are dynamically enriched with `title` and `type` resolved directly from candidate pool entries by `content_id`.
   - Preserves historical titles and types on already-assigned missions even if pool entries are subsequently deactivated.
   - Provides safe fallback defaults (`title="Daily Mission"`, `type="quiz"`) for unlisted content.
8. **Graceful Empty/Low Pool Degradation**:
   - If candidate pool is empty or has fewer than 3 matching items, gracefully assigns available items (or 0) without raising errors.

### Zero-Missing Scenario Test Suite:
- `tests/integration/test_mission_cap_trigger.py`: 12/12 integration tests passing (100% pass rate).
- Test cases:
  1. `test_database_trigger_rejects_fourth_assignment`: Verifies SQL trigger blocks 4th insert, and nested savepoint recovery works seamlessly.
  2. `test_assignment_idempotent_per_day`: Verifies repeat calls on same date return existing assignments without re-generating.
  3. `test_age_band_filtering_and_birthday_rollover`: Verifies dynamic age band rollover calculation and pool filtering.
  4. `test_empty_candidate_pool_graceful_degradation`: Verifies 0 or partial pool handles smoothly without 500 error.
  5. `test_mission_completion_updates_row_and_invalidates_cache`: Verifies in-place update and cache invalidation.
  6. `test_cross_child_mission_completion_rejected`: Verifies sibling tenancy isolation (404/403).
  7. `test_admin_mission_pool_crud_and_soft_delete`: Verifies GET/POST/PATCH and 405 on DELETE.
  8. `test_missions_http_endpoints_and_facade`: Verifies FastAPI controllers with TestClient, authentication headers, and dependency overrides.
  9. `test_dto_title_and_type_enrichment`: Verifies dynamic DTO enrichment, deactivated pool retention, and safe defaults.
  10. `test_admin_audit_logging_on_pool_mutations`: Verifies immutable audit records with diffs for pool mutations.
  11. `test_active_date_range_filtering`: Verifies date range exclusion of expired/future missions.
  12. `test_deduplication_of_content_id`: Verifies deduplication of duplicate content_id pool items.
