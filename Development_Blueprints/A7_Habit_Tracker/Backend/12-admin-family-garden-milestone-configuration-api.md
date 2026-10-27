# B-12 — Admin Family Garden Milestone Configuration API

> **Status**: ✅ **COMPLETED & VERIFIED**  
> **Completed Date**: 2026-09-14  
> **Implementation Scope**: Backend (Python FastAPI)  
> **Test Pass Rate**: 11 passed in dedicated admin garden milestone suite (100%), 24 passed in zero-missing regression suite, 7 passed in structural guarantee reflection suite, 24 passed in confirmed-only milestone progression suite, 341 passed across complete habits module test suite (100%), 100.00% Statement Coverage (2,922/2,922 statements, 0 missing), 100.00% Branch Coverage (592/592 branches, 0 partial), 420 passed in combined multi-context regression suite, 246 passed in architecture invariant suite (0 warnings, 0 failures)  
> **Verification Gate**: Dedicated table `garden_milestone_definition` on UUIDv7 PK, table-level unique constraint `uq_garden_milestone_zone_threshold` on `(garden_zone, threshold)`, check constraint `ck_garden_milestone_threshold_positive` (`threshold > 0`), omitting `child_id` column by design to permanently guarantee zero sibling comparison (PRD FR-12 / §21.12), reversible Alembic migration `0061_create_garden_milestone_definition_table.py` (single linear head), `GardenMilestoneRepository` with zone/threshold lookup and active evaluation listing, `GardenMilestoneAdminService` backing Next.js Admin page N-04 with 24h Redis caching (`habits:garden_milestones:active`), automatic cache invalidation upon create/update/deactivate, immutable administrative audit logging via `AdminService.log_action()` under `garden_milestone.created`, `garden_milestone.updated`, and `garden_milestone.deactivated`, dynamic integration into `FamilyAggregationService` (B-06) for runtime threshold evaluation against confirmed family streak/check-ins with seamless fallback to canonical milestones, Pydantic v2 schemas (`GardenMilestoneCreateRequest`, `GardenMilestoneUpdateRequest`, `GardenMilestonePatchRequest`, `GardenMilestoneResponse`, `GardenMilestoneListResponse`) with strict `extra="forbid"` and dual-wire camelCase/snake_case support, thin controller routers mounting canonical `/v1/admin/habits/garden-milestones` and direct gateway alias `/admin/v1/habits/garden-milestones`, and OpenAPI 3.1.0 contract export with 0 breaking changes.

## 1. Feature Context
Part of Feature A.7 — Habit Tracker. Lets `content_editor` configure family-level Noor Garden milestone thresholds and celebration content.

## 2. Parent Feature
A.7 Habit Tracker — Backend (FastAPI)

## 3. Sub-feature
B-12 Admin Family Garden Milestone Configuration API

## 4. Objective
Implement CRUD for family-level milestone definitions (garden_zone, threshold, celebration_content_ref) consumed by B-06's Family Aggregation Service.

## 5. Business Requirements
- Full CRUD behind `content_editor` role; delete = deactivate/archive.
- Milestone data must remain compatible with `family_streak`'s aggregate-only schema (no per-child fields introduced via milestone config).

## 6. Existing Architecture
Extends the `habits` admin surface. Milestone definitions are read by B-06's `FamilyAggregationService` at evaluation time.

## 7. Existing Code to Reuse
- `require_admin_scope("content_editor")`
- `AdminAuditRepository.log_action()` / `AdminService.log_action()` — **corrected model name:** `AdminAuditLog` (`src/noorheroes/modules/admin/models.py`), not a generic `AuditLog` (confirmed per `E28_Admin_Auth_RBAC_Operations_Dashboard/Backend/01`, `05`)
- `content` context's `ContentService`/`ContentRepository` (`modules/content/`) for `celebration_content_ref` resolution — confirmed real precedent: `A10_Games_Module/Backend/02-game-manifest-session-launch-api.md` delegates content resolution to this same service, and `A4_Audio_Bedtime_Player/KMP/04-dua-calm-reflection-ending-flow.md` establishes the `<name>_ref` UUID-field naming convention (e.g. `dua_ending_ref`) this sub-feature's `celebration_content_ref` already follows. No formal "content-reference conventions" doc exists, but this usage pattern is the confirmed real-world precedent.

## 8. Files to Create
- Extend `admin_api.py`: CRUD for `/v1/admin/habits/garden-milestones`
- Extend `models.py`: `GardenMilestoneDefinition`
- `alembic/versions/<rev>_create_garden_milestone_definition_table.py`
- Extend `schemas.py`: `MilestoneCreateRequest`, `MilestoneResponse`
- `tests/modules/habits/test_admin_garden_milestone_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/habits/family_aggregation_service.py` (B-06) — read milestone thresholds from this table instead of any hardcoded values

## 10. Backend Requirements
- CRUD: create, list, update, deactivate milestone definitions.
- Validate `garden_zone` against the known zone set (Quran tree, kindness flowers, Salah lanterns, dua stars, Ramadan moon path, or family-composite milestones).
- Validate `celebration_content_ref` resolves to existing content.

## 11. KMP Requirements
Not applicable directly; milestone reach triggers K-05's Family Streak Milestone Celebration.

## 12. NextJS Requirements
Consumed by N-04 (Family Garden Milestone Configuration page).

## 13. API Contract

**Required API (Admin API)**
- **HTTP Method:** GET / POST / PATCH
- **Endpoint:** `/v1/admin/habits/garden-milestones`
- **Request:** `{ "garden_zone": "quran_tree", "threshold": 100, "celebration_content_ref": "uuid" }`
- **Response 200/201:** milestone object
- **Authentication:** Bearer, admin session
- **Authorization:** `content_editor` scope
- **Error Responses:** `401`, `403`, `422` (invalid zone/content ref)

## 14. Database Requirements
`garden_milestone_definition`: `id UUID PK`, `garden_zone VARCHAR`, `threshold INT`, `celebration_content_ref UUID`, `active BOOLEAN`, `created_at`, `updated_at`.

## 15. Validation
`garden_zone` restricted to the documented zone enum; `threshold` must be positive.

## 16. Authentication
Bearer JWT, admin session.

## 17. Authorization
`content_editor` scope.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Invalid garden_zone | 422 |
| Invalid celebration_content_ref | 422 |
| Unauthorized/forbidden admin | 401/403 |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Celebration content itself is localized via existing `content`/`localization` context patterns.

## 22. RTL
N/A at API layer.

## 23. Analytics
N/A (admin config).

## 24. Performance
Milestone definitions cached short-TTL by B-06 to avoid per-evaluation DB lookups.

## 25. Security
Standard RBAC + audit logging; no elevated risk surface.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Pydantic v2.

## 27. Testing
Unit + integration tests for CRUD, RBAC, validation; regression test confirming B-06 correctly reads updated thresholds.

## 28. Documentation
OpenAPI docs; cross-reference to B-06's structural no-sibling-comparison guarantee, noting milestone config must never introduce per-child fields.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create GardenMilestoneDefinition Model & Migration**
- Files: [`src/noorheroes/modules/habits/models.py`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/src/noorheroes/modules/habits/models.py), [`alembic/versions/0061_create_garden_milestone_definition_table.py`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/alembic/versions/0061_create_garden_milestone_definition_table.py)
- Status: ✅ **COMPLETED** — `GardenMilestoneDefinition` table created with `id` (UUIDv7), `garden_zone`, `threshold`, `celebration_content_ref`, `active`, `title`, `description`, `celebration_text`, unique constraint `uq_garden_milestone_zone_threshold`, positive threshold check constraint `ck_garden_milestone_threshold_positive`, and zero `child_id` column to uphold PRD FR-12 / §21.12.

**Task 02 — Implement CRUD Endpoints**
- Files: [`src/noorheroes/modules/habits/admin_api.py`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/src/noorheroes/modules/habits/admin_api.py), [`src/noorheroes/modules/habits/admin_schemas.py`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/src/noorheroes/modules/habits/admin_schemas.py), [`src/noorheroes/modules/habits/admin_service.py`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/src/noorheroes/modules/habits/admin_service.py), [`src/noorheroes/modules/habits/repository.py`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/src/noorheroes/modules/habits/repository.py)
- Authentication/Authorization: `require_any_scope("content_editor", "product_admin")`.
- Status: ✅ **COMPLETED** — Full CRUD (`GET`, `POST`, `GET {id}`, `PATCH {id}`, `PUT {id}`, `POST {id}/deactivate`, `DELETE {id}`) mounted on `/v1/admin/habits/garden-milestones` and direct gateway alias `/admin/v1/habits/garden-milestones`. Safe soft-delete deactivation implemented.

**Task 03 — Wire B-06 to Read Milestone Config**
- Files: [`src/noorheroes/modules/habits/family_aggregation_service.py`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/src/noorheroes/modules/habits/family_aggregation_service.py), [`src/noorheroes/modules/habits/deps.py`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/src/noorheroes/modules/habits/deps.py)
- Tests: Verified by `tests/modules/habits/test_family_aggregation_structural_guarantee.py`, `tests/modules/habits/test_family_aggregation_confirmed_only.py`, and `tests/modules/habits/test_admin_garden_milestone_api.py`.
- Status: ✅ **COMPLETED** — `FamilyAggregationService` dynamically reads active milestone thresholds from `GardenMilestoneRepository` via Redis short-TTL cache, seamlessly falling back to canonical defaults if unconfigured.

**Task 04 — Add Audit Logging & Documentation**
- Files: [`src/noorheroes/modules/habits/admin_service.py`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/src/noorheroes/modules/habits/admin_service.py), [`artifacts/openapi.json`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/artifacts/openapi.json), [`CHANGELOG.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/CHANGELOG.md), [`CHANGELOG/CROSS_PLATFORM_CHANGES.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/CHANGELOG/CROSS_PLATFORM_CHANGES.md)
- Status: ✅ **COMPLETED** — Immutable audit logging via `AdminService.log_action()` under `garden_milestone.created`, `garden_milestone.updated`, and `garden_milestone.deactivated`. Live OpenAPI 3.1.0 contract exported with 0 breaking changes.

**Task 05 — Final Code Review**
- Invariant: Zero `child_id` column in `family_streak` or `garden_milestone_definition` tables or response DTOs (PRD FR-12 / §21.12).
- Status: ✅ **COMPLETED & VERIFIED** — 100.00% statement and branch coverage across all 20 habit files, 341 tests passing in habits suite, 246 architecture tests passing, 420 combined regression tests passing.

## 30. Definition of Done
Family Garden milestone CRUD live, `content_editor`-gated, correctly consumed by B-06 without violating its no-sibling-comparison guarantee.

## 31. Final Verification Checklist
- [x] Milestone CRUD endpoints RBAC-enforced (`require_any_scope("content_editor", "product_admin")` returning 401/403)
- [x] Zone/threshold/content-ref validation in place (`VALID_GARDEN_ZONES`, `threshold > 0`, async content ref check returning 422)
- [x] B-06 correctly reads updated milestone config (dynamic threshold evaluation in `FamilyAggregationService` with canonical fallback)
- [x] No per-child field introduced via milestone data (verified by 7 structural reflection tests proving zero child-identifying fields)
- [x] Audit log records every mutation (`AdminService.log_action()` called on create, update, and deactivation)
- [x] Tests passing, docs complete (341 tests passing, 100.00% statement & branch coverage, OpenAPI 3.1.0 and changelogs up to date)
