# B-10 — Admin Streak Shield & Grace Threshold Configuration API

> **Status**: ✅ **COMPLETED & VERIFIED**  
> **Completed Date**: 2026-09-14  
> **Implementation Scope**: Backend (Python FastAPI)  
> **Test Pass Rate**: 17 passed in dedicated admin streak config suite (100%), 22 passed in timezone grace authority regression suite (100%), 15 passed in zero-missing defensive suite (100%), 310 passed across complete habits module test suite (100%), 413 passed across unified architectural, CI, routing, and i18n test suites (100% pass rate, 0 warnings, 0 failures)  
> **Verification Gate**: Singleton storage model (`habit_streak_config`) on ID `00000000-0000-0000-0000-000000000001`, check constraints enforcing positive bounds and ordering (`generous >= conservative`), reversible Alembic migration `0059_create_habit_streak_config_table.py` with default auto-seeding `(5, 3, 1, 2)` if empty on initial read (B-10 §18), 24-hour Redis caching (`habits:streak_config`) with synchronous eviction upon update and graceful offline fallback, immutable audit logging via `AdminService.log_action()` (`habit_streak_config.update`), dynamic injection into `TimezoneAuthorityService` (B-04) without redeploy, strict `product_admin` RBAC authorization (`content_editor` gets 403 Forbidden), dual-wire camelCase/snake_case schemas (`extra="forbid"`), dual-routing parity on `/v1/admin/habits/streak-config` and `/admin/v1/habits/streak-config`, robust FastAPI dependency injection wiring (`deps.py`), and OpenAPI 3.1.0 contract export.

## 1. Feature Context
Part of Feature A.7 — Habit Tracker. Lets `product_admin` tune the abuse-resistance thresholds consumed by B-04 (Timezone Authority) without a code deploy.

## 2. Parent Feature
A.7 Habit Tracker — Backend (FastAPI)

## 3. Sub-feature
B-10 Admin Streak Shield & Grace Threshold Configuration API

## 4. Objective
Implement `PATCH /v1/admin/habits/streak-config` for `change_count_30d` threshold, grace-window durations (generous/conservative), and recovery-window length — update-only, `product_admin` restricted.

## 5. Business Requirements
- Update-only (no create/delete — this is a singleton configuration).
- Restricted to `product_admin` role.
- Changes take effect for B-04's grace computation without redeploy.
- All values bounded to sane ranges to prevent operator error from breaking fairness guarantees.

## 6. Existing Architecture
Extends the `habits` admin surface (B-09's `admin_api.py`/router). Configuration stored as a singleton row or key-value config table, following whichever pattern the existing `admin` context uses for tunable platform settings (reuse that pattern rather than inventing a new one — if no existing tunable-config pattern exists elsewhere in the codebase, use a simple single-row `habit_streak_config` table as the minimal consistent choice).

## 7. Existing Code to Reuse
- `require_admin_scope("product_admin")`
- `AdminAuditRepository.log_action()` / `AdminService.log_action()` — **corrected model name:** `AdminAuditLog` (`src/noorheroes/modules/admin/models.py`), not a generic `AuditLog` (confirmed per `E28_Admin_Auth_RBAC_Operations_Dashboard/Backend/01`, `05`; consistent with B-09 §6)

## 8. Files to Create
- Extend `admin_api.py`: `PATCH /v1/admin/habits/streak-config`, `GET /v1/admin/habits/streak-config`
- Extend `models.py`: `HabitStreakConfig` (singleton row)
- `alembic/versions/<rev>_create_habit_streak_config_table.py`
- Extend `schemas.py`: `StreakConfigUpdateRequest`, `StreakConfigResponse`
- `tests/modules/habits/test_admin_streak_config_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/habits/timezone_authority.py` (B-04) — read threshold values from `HabitStreakConfig` instead of hardcoded constants

## 10. Backend Requirements
- Singleton config row (single source of truth), read by B-04's `compute_grace_window()`.
- Bounds validation on all fields (e.g., `change_count_30d` threshold must be a positive integer within a reasonable range).
- Every update writes an audit log row with before/after values.

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
Consumed by N-02 (Streak Shield & Grace Threshold Configuration Panel).

## 13. API Contract

**Required API (Admin API)**
- **HTTP Method:** PATCH / GET
- **Endpoint:** `/v1/admin/habits/streak-config`
- **Request:** `{ "change_count_30d_threshold": 5, "generous_grace_days": 3, "conservative_grace_days": 1, "recovery_window_days": 2 }`
- **Response 200:** current config object
- **Authentication:** Bearer, admin session
- **Authorization:** `product_admin` scope only
- **Error Responses:** `401`, `403`, `422` (out-of-bounds values)

## 14. Database Requirements
`habit_streak_config`: `id UUID PK (singleton)`, `change_count_30d_threshold INT`, `generous_grace_days INT`, `conservative_grace_days INT`, `recovery_window_days INT`, `updated_at TIMESTAMPTZ`, `updated_by_admin_id UUID`.

## 15. Validation
Bounds validation on every field; reject values that would make the grace logic non-functional (e.g., zero or negative durations).

## 16. Authentication
Bearer JWT, admin session.

## 17. Authorization
`product_admin` scope strictly required (stricter than B-09's dual-role option).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Out-of-bounds value | 422 with field-level error |
| Unauthorized/forbidden admin | 401/403 |
| Config row missing (first run) | Auto-seed with safe defaults on first read |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
N/A (numeric config, admin-facing only).

## 22. RTL
N/A.

## 23. Analytics
N/A (audit-logged admin action).

## 24. Performance
Singleton row read is cached in-memory/Redis by B-04 with short TTL to avoid a DB round-trip on every grace computation.

## 25. Security
Stricter single-role gate reflects the outsized fairness impact of these thresholds (PRD §8 CRUD permissions table).

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Pydantic v2.

## 27. Testing
Unit + integration tests for bounds validation, RBAC enforcement, and B-04 correctly picking up updated values (regression test against B-04's grace-path tests).

## 28. Documentation
OpenAPI docs; explicit warning in description that these values directly affect the feature's core fairness guarantees.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create HabitStreakConfig Singleton Model**
- **Status**: ✅ **COMPLETED**
- Files Created: `models.py` extension (`HabitStreakConfig`, `HABIT_STREAK_CONFIG_SINGLETON_ID`), Alembic migration `0059_create_habit_streak_config_table.py`.
- Definition of Done: Singleton table created with positive bounds check constraints and auto-seeded defaults `(5, 3, 1, 2)`.

**Task 02 — Implement Config Endpoints**
- **Status**: ✅ **COMPLETED**
- Files Created/Modified: `admin_api.py`, `admin_schemas.py` (`StreakConfigUpdateRequest`, `StreakConfigResponse`), `repository.py` (`HabitStreakConfigRepository`), `admin_service.py` (`HabitStreakConfigService`).
- Authentication/Authorization: `product_admin` scope strictly enforced (`require_any_scope("product_admin")`).
- Validation: Bounds checks (`1-100` threshold, `1-14` generous, `1-7` conservative, `1-14` recovery) and cross-field ordering (`generous >= conservative`).
- Definition of Done: GET/PATCH endpoints live, dual-mounted on `/v1/admin/habits/streak-config` and `/admin/v1/habits/streak-config`.

**Task 03 — Wire B-04 to Read Dynamic Config**
- **Status**: ✅ **COMPLETED**
- Files Modified: `timezone_authority.py`, `deps.py`.
- Implementation Details: Replaced hardcoded threshold constants with `get_dynamic_config()` reading Redis cache (`habits:streak_config`) or repository fallback, defaulting conservatively to `(5, 3, 1, 2)` if unavailable.
- Tests: Regression tests confirming B-04 grace-path tests pass dynamically without server redeploy.
- Definition of Done: B-04 correctly reflects admin-configured values at runtime.

**Task 04 — Add Audit Logging**
- **Status**: ✅ **COMPLETED**
- Reused Component: `AdminService.log_action()` (`admin` context, `AdminAuditLog` model per §7).
- Definition of Done: Immutable audit event `habit_streak_config.update` logged with before/after diffs on every update.

**Task 05 — Final Code Review**
- **Status**: ✅ **COMPLETED**
- Invariant Preserved: B-04 core day-boundary calculation logic preserved intact; only config lookup is dynamic.
- Expected Result: Zero-missing, zero-warning test pass across all 413 tests.

## 30. Definition of Done
Admin-tunable streak/grace configuration live, `product_admin`-restricted, correctly consumed by B-04 without redeploy.

## 31. Final Verification Checklist
- [x] Singleton config table created with safe defaults
- [x] PATCH/GET endpoints restricted to `product_admin`
- [x] Bounds validation rejects unsafe values
- [x] B-04 reads dynamic config with caching
- [x] Audit log records before/after values
- [x] Regression tests against B-04 grace-path tests pass

## 32. Technical Implementation & Test Verification Records
- **ORM Model**: `HabitStreakConfig` in `src/noorheroes/modules/habits/models.py` (Singleton UUID `00000000-0000-0000-0000-000000000001`).
- **Alembic Migration**: `alembic/versions/0059_create_habit_streak_config_table.py` (Single linear head).
- **Repository**: `HabitStreakConfigRepository` in `src/noorheroes/modules/habits/repository.py`.
- **Cache Manager**: `HabitCatalogCacheManager` in `src/noorheroes/modules/habits/cache.py` (24h TTL, synchronous invalidation).
- **Pydantic v2 Schemas**: `StreakConfigUpdateRequest`, `StreakConfigResponse` in `src/noorheroes/modules/habits/admin_schemas.py`.
- **Domain Service**: `HabitStreakConfigService` in `src/noorheroes/modules/habits/admin_service.py`.
- **Dependency Provider**: `get_habit_streak_config_repository` in `src/noorheroes/modules/habits/deps.py`.
- **Automated Test Results**:
  - `tests/modules/habits/test_admin_streak_config_api.py`: 17 passed
  - `tests/modules/habits/test_timezone_grace_logic.py`: 22 passed
  - `tests/modules/habits/test_habits_zero_missing_suite.py`: 15 passed
  - Complete Habits Module Suite: 310 passed
  - Unified System Test Suite: 413 passed in 12.06s (0 warnings, 0 failures)
- **CI / Architecture Checks**:
  - `scripts/check_migration_backward_compat.py`: Clean pass
  - `scripts/check_env_example_sync.py`: Clean pass (0 drift)
  - `scripts/check_resource_naming.py`: Clean pass
  - `scripts/export_openapi_schema.py`: Clean pass (`artifacts/openapi.json`)

