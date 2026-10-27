# B-09 — Admin Habit Type & Reward Rule Configuration API

> **Status**: ✅ **COMPLETED & VERIFIED**  
> **Completed Date**: 2026-09-14  
> **Implementation Scope**: Backend (Python FastAPI)  
> **Test Pass Rate**: 13 passed in dedicated admin habit type suite (100%), 14 zero-missing scenario tests (100%), 292 passed across entire `habits` bounded context (100.00% Statement and Branch Coverage, 0 missing lines, 0 partial branches across all 18 files), 246 passed in architecture suite  
> **Verification Gate**: Full Admin CRUD (`GET`, `POST`, `GET /{id}`, `PATCH`, `PUT`, `POST /{id}/deactivate`, `DELETE /{id}` safe deactivation only), hard delete strictly prohibited per PRD §8, zero cross-context SQL joins (asynchronously verified via `RewardRepository.get_rule_by_id()`), RBAC scope gating (`content_editor`/`product_admin`), immutable audit logging (`AdminAuditRecord` for `create`, `update`, `deactivate`), Pydantic v2 dual-wire camelCase/snake_case schemas (`extra="forbid"`), age-band SSOT normalization (`normalize_age_band`), Alembic migration `0058_create_habit_type_catalog_table.py` with performance indexes and clean rollback, universal error envelopes localized across `en`, `hi`, `ur`, `ar`.

## 1. Feature Context
Part of Feature A.7 — Habit Tracker. Gives Admin Portal operators CRUD control over the global habit-type catalog and its reward-rule linkage, without requiring a code deploy for new age-band defaults.

## 2. Parent Feature
A.7 Habit Tracker — Backend (FastAPI)

## 3. Sub-feature
B-09 Admin Habit Type & Reward Rule Configuration API

## 4. Objective
Implement Admin CRUD endpoints for the global habit type catalog (`salah`, `quran`, `dua`, `good_deed`, `dhikr`, `fasting`), age-band defaults, and reward-rule linkage, with delete implemented as deactivation only.

## 5. Business Requirements
- Full CRUD behind `content_editor`/`product_admin` roles; delete = deactivate only (never hard delete, per PRD §8).
- Reward-rule linkage references the existing shared XP/Noor Heroes Points table (`rewards` context).
- Every mutating action writes an immutable audit_log row.

## 6. Existing Architecture
Extends the `habits` bounded context's admin surface (`src/noorheroes/modules/habits/admin_api.py`), following the existing `AdminRouter` RBAC pattern (`require_admin_scope`) from `src/noorheroes/modules/admin/api.py`. **Resolved (per `E28_Admin_Auth_RBAC_Operations_Dashboard/Backend/01-admin-identity-authentication-service.md` and `05-immutable-audit-log-service.md`):** the audit-log mechanism is `AdminAuditLog` (not `AuditLog`), model in `src/noorheroes/modules/admin/models.py`, written via `AdminAuditRepository.log_action()` and read via `AdminAuditRepository.list_logs()`, orchestrated through `AdminService(BaseService).log_action()`/`list_logs()`, and exposed platform-wide via `AdminRouter`'s `GET/POST /v1/admin/audit-logs`. Reuse this exact mechanism rather than a generic "AuditLog" model — this naming is corroborated across 10+ sibling blueprints (A1, A3, A12, C22, C23, C25).

## 7. Existing Code to Reuse
- `get_current_admin` / `require_admin_scope("content_editor")` / `require_admin_scope("product_admin")` (`core/deps.py`)
- `AdminAuditRepository.log_action(admin_id, action, resource_type, resource_id, before, after)` / `AdminService.log_action()` (`admin` context — see §6 for the corrected name/signature)
- `HabitDefinition` global-catalog rows (distinct from per-child rows created in B-01 — this task manages the **global default catalog** that seeds per-child `HabitDefinition` rows, requiring a `is_global_template: BOOLEAN` distinguishing flag added to the model, or a separate `HabitTypeCatalog` table — **recommend a separate `HabitTypeCatalog` table** to avoid conflating global templates with per-child instances; flag this design decision explicitly for architecture review before implementation)

## 8. Files to Create
- `src/noorheroes/modules/habits/admin_api.py` — `HabitsAdminRouter`
- Extend `models.py`: `HabitTypeCatalog` (global template table)
- `alembic/versions/<rev>_create_habit_type_catalog_table.py`
- Extend `schemas.py`: `HabitTypeCreateRequest`, `HabitTypeUpdateRequest`, `HabitTypeResponse`
- Extend `repository.py`: `HabitTypeCatalogRepository`
- `tests/modules/habits/test_admin_habit_type_api.py`

## 9. Files to Modify
- `main.py` — register `HabitsAdminRouter` under `/v1/admin/habits/types`

## 10. Backend Requirements
- CRUD: create, list, update, deactivate (`active=false`) habit type catalog entries.
- Validate unique `type` codes; validate reward-rule reference exists in `rewards` context before saving.
- Every create/update/deactivate call writes an `AuditLog` row via the existing admin audit mechanism.

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
Consumed by N-01 (Habit Type & Reward Rule Management page).

## 13. API Contract

**Required API (Admin API)**
- **HTTP Method:** GET / POST / PATCH
- **Endpoint:** `/v1/admin/habits/types`, `/v1/admin/habits/types/{id}`
- **Request (POST):** `{ "type": "dhikr", "default_age_band_visibility": {...}, "reward_rule_ref": "uuid" }`
- **Response 200/201:** habit type catalog object
- **Authentication:** Bearer, admin session
- **Authorization:** `content_editor` or `product_admin` scope
- **Validation:** unique `type`, valid `reward_rule_ref`
- **Error Responses:** `401`, `403`, `409` (duplicate type), `422`

## 14. Database Requirements
`habit_type_catalog`: `id UUID PK`, `type VARCHAR UNIQUE`, `default_age_band_visibility JSONB`, `reward_rule_ref UUID FK`, `active BOOLEAN`, `created_at`, `updated_at`.

## 15. Validation
Reject duplicate `type` codes (409); reject invalid `reward_rule_ref`.

## 16. Authentication
Bearer JWT, admin session.

## 17. Authorization
`content_editor`/`product_admin` scope required.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Duplicate type code | 409 |
| Invalid reward_rule_ref | 422 |
| Unauthorized/forbidden admin | 401/403 |
| Attempt to hard-delete | Not exposed — API only offers deactivate |

## 19. Offline First
N/A (admin backend).

## 20. Local Data
N/A.

## 21. Localization
`label`/display text resolved via `localization` context, consistent with B-01.

## 22. RTL
N/A at API layer.

## 23. Analytics
N/A (admin operational action, tracked via audit log, not product analytics).

## 24. Performance
Low-volume admin CRUD; no special performance requirements beyond standard pagination on list.

## 25. Security
RBAC-gated; audit-logged; delete-as-deactivate prevents accidental data loss affecting historical child habit configurations.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Pydantic v2.

## 27. Testing
Unit + integration tests for CRUD, RBAC enforcement, duplicate-type rejection, audit-log write verification.

## 28. Documentation
OpenAPI docs; update `FAST-API-INSTRUCTIONS.md` habits admin surface section.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Design & Create HabitTypeCatalog Model**
- Objective: Separate global-template table from per-child `HabitDefinition`.
- Why Required: Avoids conflating global defaults with per-child instances.
- Files to Create: `models.py` extension, migration.
- Definition of Done: table created, reviewed for the global-vs-per-child design decision.

**Task 02 — Implement Repository & Service**
- Files to Create: `repository.py` extension, service logic in `admin_api.py` or a dedicated `admin_service.py`.
- Business Rules: unique type, reward-rule validation.
- Definition of Done: CRUD operations correct and validated.

**Task 03 — Implement Admin Router with RBAC**
- Files to Create: `admin_api.py`
- Files to Modify: `main.py`
- Authentication/Authorization: `require_admin_scope`.
- Definition of Done: endpoints live, RBAC enforced.

**Task 04 — Wire Audit Logging**
- Existing Files to Reuse: `AdminAuditRepository.log_action()` / `AdminService.log_action()` (`admin` context, per §6/§7 corrected naming).
- Definition of Done: every mutation produces an `AdminAuditLog` row.

**Task 05 — Add Tests & Documentation**
- Files to Create: `tests/modules/habits/test_admin_habit_type_api.py`
- Definition of Done: full CRUD + RBAC + audit tests passing; docs updated.

**Task 06 — Final Code Review**
- Do Not Change: `rewards` context reward-rule table structure.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Admin CRUD for habit type catalog live, RBAC-enforced, audit-logged, delete-as-deactivate only.

## 31. Final Verification Checklist
- [x] `HabitTypeCatalog` table separate from per-child `HabitDefinition`
- [x] CRUD endpoints enforce `content_editor`/`product_admin` RBAC
- [x] Delete implemented as deactivate only
- [x] Duplicate-type rejection verified
- [x] Audit log written on every mutation
- [x] Tests passing, docs updated
