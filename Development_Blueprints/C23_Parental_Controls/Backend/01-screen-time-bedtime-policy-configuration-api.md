# B-01 — Screen-Time & Bedtime Policy Configuration API

## 1. Feature Context
Parents need genuine, server-authoritative control over daily screen-time limits and bedtime/quiet-hours windows per child (PRD C.23 §1.1). This sub-feature owns the **configuration surface** for that policy — the values a parent sets. Enforcement against those values (usage accounting, limit/bedtime evaluation) is owned by B-02.

## 2. Parent Feature
Feature C.23 — Parental Controls (Screen Time, Bedtime, AI Permissions, Content Age Level)

## 3. Sub-feature
1.1 Screen-Time & Bedtime Policy Configuration API (ID: **B-01**)

## 4. Objective
Implement `GET/PATCH /v1/children/{id}/restrictions` and the `screen-time-policy` sub-resource alias so a parent can read and update a child's `daily_limit_minutes`, `warning_threshold_minutes`, `bedtime_start`, and `bedtime_end`, with midnight-crossing bedtime windows evaluated correctly and every mutation gated behind fresh Parent Gate step-up verification. The GET response also surfaces a read-only `minutes_used_today` field (sourced from B-02's `screen_time_usage_daily` table) so KMP K-02's Screen Time Settings screen can display current-usage-today context without needing a separate endpoint or a child-mode heartbeat call (parent-mode sessions cannot call B-02's child-mode-only heartbeat endpoint).

> **Resolved gap:** the original breakdown flagged "current-usage-today data source" as an open question for K-02. Resolution: extend this endpoint's response rather than adding a new one, since this is already the parent-facing read path Settings screens call.

## 5. Business Requirements
- FR-1: Screen Time and Quiet Hours/Bedtime are canonical Controls sections reached under Parent Area → Controls.
- FR-2 (item 1): child session start loads the server-signed restriction policy.
- FR-3: server is authoritative for policy values; this API is the only writer.
- FR-12: every mutating Controls action requires step-up authentication via C.19's gate.
- Edge Case 5: a parent lowering a limit mid-session does not abruptly interrupt the active session (applies at next session); bedtime-window changes are evaluated continuously regardless of when configured (distinct from daily-limit "locked in at session start" semantics).
- Edge Case 7: two co-guardians adjusting the same value concurrently — last-write-wins, resulting value visible to both on next view.
- Edge Case 10: a daily limit of 0 minutes is a valid, unusual-but-accepted configuration.
- Empty State §1.12: no policy configured yet → explicit "no limit set" (unrestricted default), never an ambiguous blank field.

## 6. Existing Architecture
New bounded context `modules/restrictions` (Restriction Engine), following the established 10-context modular-monolith pattern (`models.py` / `schemas.py` / `repository.py` / `service.py` / `api.py`, `BaseService`, `BaseRepository[ModelT]`, `OutboxWriter`). Reuses `core/deps.py::get_current_parent`, `require_elevated_session` (step-up), `core/exceptions.py` domain errors, and the identity module's `ChildRepository` pattern for family-ownership checks. `get_policy()` additionally reads (read-only, no write coupling) from B-02's `screen_time_usage_daily` table via `ScreenTimeUsageRepository.get_by_child_and_date()` to populate `minutes_used_today` — this creates a soft dependency where B-02's model/repository must exist before this endpoint's GET path is complete; the PATCH path has no such dependency.

## 7. Existing Code to Reuse
- `core/deps.py::get_current_parent`, `require_elevated_session`
- `core/exceptions.py::NotFoundError`, `ValidationError`, `AuthorizationError`, `ChildScopeViolationError`
- `common/base_service.py::BaseService`, `common/base_repository.py::BaseRepository[ModelT]`
- `common/outbox.py::OutboxWriter`
- `modules/identity/models.py::ChildProfile` (FK target for `child_id`)

## 8. Files to Create
- `src/noorheroes/modules/restrictions/__init__.py`
- `src/noorheroes/modules/restrictions/models.py` — `ScreenTimePolicyOrm`
- `src/noorheroes/modules/restrictions/schemas.py` — `RestrictionsResponse`, `RestrictionsUpdateRequest`
- `src/noorheroes/modules/restrictions/repository.py` — `ScreenTimePolicyRepository(BaseRepository[ScreenTimePolicyOrm])`
- `src/noorheroes/modules/restrictions/service.py` — `RestrictionPolicyService(BaseService)`
- `src/noorheroes/modules/restrictions/api.py` — router mount point for all C.23 backend endpoints (shared across B-01–B-04)
- `src/noorheroes/modules/restrictions/deps.py` — `get_restriction_policy_service`
- `alembic/versions/xxxx_create_screen_time_policies.py`
- `tests/modules/restrictions/test_policy_service.py`
- `tests/modules/restrictions/test_policy_api.py`

## 9. Files to Modify
- `src/noorheroes/main.py` (or router registry) — mount `restrictions.api.router` at `/v1/children`
- `src/noorheroes/modules/identity/service.py::create_child_profile` — insert default (unrestricted) `ScreenTimePolicyOrm` row on child creation
- `src/noorheroes/modules/restrictions/schemas.py` (once B-02 exists) — extend `RestrictionsResponse` with `minutes_used_today: int`

## 9a. Cross-Sub-Feature Dependency
`minutes_used_today` requires B-02's `ScreenTimeUsageRepository` and `screen_time_usage_daily` table to exist. Implementation order: this file's PATCH path and core policy CRUD can ship independently of B-02, but the GET response's `minutes_used_today` field should be treated as a follow-up task once B-02 lands, not blocking B-01's initial release — default to `0` if B-02's table/repository is not yet available, never omit the field (KMP K-02 expects it to always be present).

## 10. Backend Requirements
- `RestrictionPolicyService.get_policy(child_id, parent_ctx)`: load by `child_id`, verify family ownership → `404` if not owned/found; if no row exists, return the unrestricted default shape (never a raw 404 for "not yet configured"). Additionally reads today's usage row (keyed by server-computed `local_date`, never a client-supplied date) from `screen_time_usage_daily` via B-02's repository and includes it as `minutes_used_today` (0 if no row exists yet for today).
- `RestrictionPolicyService.update_policy(child_id, parent_ctx, payload)`:
  1. Verify `require_elevated_session` step-up marker is present and fresh.
  2. Verify family ownership of `child_id`.
  3. Validate `bedtime_start`/`bedtime_end` as `time` values; accept any combination including midnight-crossing (`bedtime_start > bedtime_end` is valid and means overnight).
  4. Validate `daily_limit_minutes >= 0` (0 is valid — fully blocks the child) and `warning_threshold_minutes <= daily_limit_minutes` when both set.
  5. Upsert `ScreenTimePolicyOrm` (PK = `child_id`), update `updated_at`.
  6. Emit `ScreenTimePolicyConfigured`/`BedtimePolicyConfigured` outbox event(s) depending on which fields changed.
  7. Last-write-wins on concurrent updates — no optimistic-lock rejection for this table (explicitly low-stakes per PRD Edge Case 7).
- Bedtime evaluation helper `is_within_bedtime_window(start: time, end: time, now: time) -> bool` handling the midnight-crossing case, placed in `modules/restrictions/policy_logic.py` for reuse by B-02.

## 11. API Contract

### `GET /v1/children/{id}/restrictions`
- **Auth:** Bearer (parent)
- **Authorization:** family ownership of `child_id`
- **Response 200:** `{ "daily_limit_minutes": 45, "warning_threshold_minutes": 10, "bedtime_start": "20:00", "bedtime_end": "07:00", "minutes_used_today": 20, "updated_at": "..." }` (nulls for unset policy fields, `daily_limit_minutes: null` = unrestricted; `minutes_used_today` is always a non-null integer, read-only, sourced from B-02's `screen_time_usage_daily`)
- **Error Responses:** `401 UNAUTHORIZED`, `403 FORBIDDEN`, `404 CHILD_NOT_FOUND`

### `PATCH /v1/children/{id}/restrictions`
- **Auth:** Bearer (parent) + step-up (fresh Parent Gate pass, `require_elevated_session`)
- **Request:** `{ "daily_limit_minutes"?: 45, "warning_threshold_minutes"?: 10, "bedtime_start"?: "20:00", "bedtime_end"?: "07:00" }` (partial update)
- **Response 200:** same shape as GET
- **Error Responses:** `401 UNAUTHORIZED`, `403 FORBIDDEN` (not owned / step-up missing), `404 CHILD_NOT_FOUND`, `422 VALIDATION_ERROR`

### `GET/PATCH /v1/children/{id}/screen-time-policy`
- Alias/sub-resource restricted to the daily-limit fields only, same underlying service and table, consistent with platform API-naming conventions.

## 12. Database Requirements
`screen_time_policies`: `child_id UUID PK/FK → child_profiles.id`, `daily_limit_minutes INT NULL`, `warning_threshold_minutes INT NULL`, `bedtime_start TIME NULL`, `bedtime_end TIME NULL`, `updated_at TIMESTAMPTZ`. No separate index needed (PK lookup only).

## 13. Validation
- `daily_limit_minutes`: integer, `>= 0`, no upper bound enforced server-side beyond a sane cap (e.g., 1440).
- `warning_threshold_minutes`: integer, `>= 0`, should not exceed `daily_limit_minutes` when both present (soft validation warning, not a hard reject, since a parent could set warning threshold before limit).
- `bedtime_start`/`bedtime_end`: valid `HH:MM` time values; any combination accepted (midnight-crossing is valid).
- Reject unknown fields in the PATCH body.

## 14. Authentication
`Depends(get_current_parent)` for GET; PATCH additionally requires `Depends(require_elevated_session)`.

## 15. Authorization
Family-ownership check: `child_id` must belong to `parent_ctx.family_id`. Raise `ChildScopeViolationError` → `404` (not `403`, to avoid leaking child existence across families) on mismatch.

## 16. Error Handling
| Scenario | Response |
|---|---|
| No policy row yet | 200 with unrestricted-default shape |
| Child not found / not owned | 404 CHILD_NOT_FOUND |
| Missing/expired step-up on PATCH | 403 FORBIDDEN (step-up required) |
| Invalid bedtime time format | 422 VALIDATION_ERROR |
| Negative `daily_limit_minutes` | 422 VALIDATION_ERROR |
| Database failure | 500, logged with request ID |

## 17. Offline First
N/A — this is the authoritative write path; not consumed offline directly (B-02/KMP K-07 own offline policy caching).

## 18. Local Data
N/A (backend).

## 19. Localization
Response payload is locale-agnostic (raw minutes/times); client formats for display.

## 20. RTL
N/A (backend).

## 21. Analytics
Emits domain events consumed by the platform analytics pipeline: `screen_time_policy_configured`, `bedtime_policy_configured`.

## 22. Performance
Low-volume, low-frequency endpoint (parent-initiated only). Simple PK-indexed reads/writes; no N+1 risk.

## 23. Security
Step-up required on every mutation. No sensitive data in this table beyond policy numbers. Family-scoped access only.

## 24. Library Requirements
FastAPI, SQLAlchemy 2.0 (async), Pydantic v2, Alembic. No new third-party dependencies.

## 25. Testing
- Unit: midnight-crossing bedtime window evaluated correctly at 23:30/05:00 (within) and 14:00 (not within).
- Unit: `daily_limit_minutes = 0` accepted and persisted.
- Unit: PATCH without step-up marker rejected with 403.
- Unit: PATCH against a child not owned by caller's family rejected with 404.
- Integration: GET before any configuration returns unrestricted-default shape.
- Integration: concurrent PATCH from two simulated parent sessions — last write wins, both subsequent GETs return the same latest value.
- Integration (once B-02 lands): GET reflects `minutes_used_today` matching a seeded `screen_time_usage_daily` row for the current server-computed local date.
- Unit: GET returns `minutes_used_today: 0` (not null, not omitted) when no usage row exists yet for today.

## 26. Documentation
OpenAPI summary/description on both routes; document the midnight-crossing semantics explicitly in the endpoint description since it's a non-obvious behavior.

## 27. AI Coding Agent Implementation Steps

**Task 01 — Create `ScreenTimePolicyOrm` Model**
- Objective: Define the `screen_time_policies` table ORM model.
- Why This Is Required: Persistent storage for the policy configuration.
- Existing Architecture to Follow: `infrastructure/db/base.py::Base`, `TimestampMixin` pattern used across other modules.
- Files to Create: `src/noorheroes/modules/restrictions/models.py`
- Implementation Details: `child_id` as PK/FK to `child_profiles.id`; nullable `daily_limit_minutes`, `warning_threshold_minutes`, `bedtime_start`, `bedtime_end`; `updated_at` via `TimestampMixin`.
- Dependencies: None.
- Expected Result: Model importable and mapped correctly.
- Definition of Done: `alembic revision --autogenerate` detects the new table cleanly.

**Task 02 — Create Alembic Migration**
- Objective: Create `screen_time_policies` table in PostgreSQL.
- Files to Create: `alembic/versions/xxxx_create_screen_time_policies.py`
- Implementation Details: Standard `upgrade()`/`downgrade()`, FK constraint to `child_profiles.id` with `ON DELETE CASCADE`.
- Expected Result: Migration applies cleanly on staging DB.
- Definition of Done: `alembic upgrade head` succeeds; `downgrade` reverses cleanly.

**Task 03 — Create Request/Response Schemas**
- Objective: Define `RestrictionsResponse`, `RestrictionsUpdateRequest` Pydantic v2 DTOs.
- Files to Create: `src/noorheroes/modules/restrictions/schemas.py`
- Implementation Details: Inherit from `common/schemas.py::NoorHeroesBaseModel` (camelCase alias generation); all update fields `Optional`.
- Validation: `daily_limit_minutes: Optional[int] = Field(None, ge=0)`.
- Expected Result: Schemas validate correctly against example payloads.
- Definition of Done: Unit tests for schema validation pass.

**Task 04 — Implement `ScreenTimePolicyRepository`**
- Objective: CRUD access to `screen_time_policies`.
- Files to Create: `src/noorheroes/modules/restrictions/repository.py`
- Implementation Details: Extend `BaseRepository[ScreenTimePolicyOrm]`; add `get_by_child_id(child_id)`, `upsert(child_id, values)`.
- Dependencies: Task 01.
- Expected Result: Repository methods pass isolated DB tests.

**Task 05 — Implement `policy_logic.py` Bedtime Evaluation Helper**
- Objective: Shared midnight-crossing bedtime window evaluation function.
- Why This Is Required: Reused identically by B-02's enforcement engine — must not be duplicated/drifted.
- Files to Create: `src/noorheroes/modules/restrictions/policy_logic.py`
- Implementation Details: `is_within_bedtime_window(start: time, end: time, now: time) -> bool`; handle `start > end` (overnight) case explicitly.
- Tests: parametrized test matrix covering same-day and overnight windows at boundary times.

**Task 06 — Implement `RestrictionPolicyService`**
- Objective: Business logic for get/update policy with step-up and ownership checks.
- Files to Create: `src/noorheroes/modules/restrictions/service.py`
- Existing Architecture to Follow: `BaseService`, `OutboxWriter.emit()` pattern from `IdentityService.create_child_profile`.
- Implementation Details: Per §10 above.
- Dependencies: Tasks 03, 04, 05.
- Expected Result: Service methods covered by unit tests in Task 11.

**Task 07 — Implement API Router**
- Objective: Expose `GET/PATCH /v1/children/{id}/restrictions` and `/screen-time-policy` alias.
- Files to Create: `src/noorheroes/modules/restrictions/api.py`, `src/noorheroes/modules/restrictions/deps.py`
- Implementation Details: Follow the canonical router pattern (§10 of FAST-API-INSTRUCTIONS.md) — no DB access in router, only `Depends()` injection of the service.
- Dependencies: Task 06.

**Task 08 — Wire Default Policy Row on Child Creation**
- Objective: Ensure every new child gets an implicit unrestricted policy record (or the service handles absence gracefully — prefer the latter to avoid dual-write coupling).
- Files to Modify: `src/noorheroes/modules/identity/service.py` (only if the "explicit row" approach is chosen instead of "handle absence in service") — confirm with team preference before implementing; default to handling absence in `RestrictionPolicyService.get_policy` to avoid unnecessary coupling between `identity` and `restrictions` contexts.

**Task 09 — Register Router**
- Objective: Mount the new router in the app.
- Files to Modify: `src/noorheroes/main.py`
- Definition of Done: `/docs` shows the new endpoints under a `restrictions` tag.

**Task 10 — Add Authentication/Authorization**
- Objective: Enforce `get_current_parent` + `require_elevated_session` + family-ownership.
- Dependencies: Tasks 06, 07.

**Task 11 — Add Tests**
- Objective: Full unit + integration coverage per §25.
- Files to Create: `tests/modules/restrictions/test_policy_service.py`, `tests/modules/restrictions/test_policy_api.py`

**Task 12 — Add API Documentation**
- Objective: OpenAPI descriptions, especially midnight-crossing semantics.
- Files to Modify: `src/noorheroes/modules/restrictions/api.py` (docstrings/`description=` kwargs)

**Task 13 — Final Code Review**
- Objective: Confirm layering rules honored (no DB in router, no manual commits in service/repo), confirm no PostgreSQL/Redis credential files touched.

**Task 14 — Wire `minutes_used_today` into GET Response (Follow-Up, Once B-02 Lands)**
- Objective: Close the K-02 current-usage-today data-source gap by reading B-02's `screen_time_usage_daily` via its repository's `get_by_child_and_date()` method.
- Files to Modify: `service.py` (`get_policy`), `schemas.py` (`RestrictionsResponse`)
- Implementation Details: Read-only join; default to `0` if no row exists for today; never omit the field.
- Dependencies: B-02 must be implemented first.
- Definition of Done: GET response always includes a non-null `minutes_used_today` integer.

## 28. Definition of Done
- All 13 tasks complete; endpoints live and documented in `/docs`.
- Midnight-crossing bedtime evaluation verified by test.
- Step-up enforcement verified by test.
- Family-ownership isolation verified by test.
- No regression in existing `identity` module tests.

## 29. Final Verification Checklist
- [ ] `GET /v1/children/{id}/restrictions` returns unrestricted-default shape when unconfigured
- [ ] `PATCH` rejected without fresh step-up
- [ ] `PATCH` rejected for non-owned child (404, not 403)
- [ ] `daily_limit_minutes = 0` accepted
- [ ] Midnight-crossing bedtime window test passes (23:30, 05:00, 14:00 cases)
- [ ] Outbox events emitted on successful update
- [ ] No manual `session.commit()` in service/repository
- [ ] OpenAPI docs updated
- [ ] Unit + integration tests green in CI
- [ ] `minutes_used_today` present (never omitted/null) in every GET response, sourced correctly from B-02 once available
