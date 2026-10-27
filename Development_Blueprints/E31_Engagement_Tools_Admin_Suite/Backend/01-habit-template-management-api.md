# B-01 — Habit Template Management API

## 1. Feature Context
Part of **Feature E.31 — Engagement Tools Admin Suite**, the consolidated admin-authoring layer for NoorHeroes' seven engagement mechanics. This sub-feature delivers the admin CRUD surface for **habit templates** (Salah, Quran, dua, good deed, dhikr, fasting) that power the child-facing Habit Tracker (A.7). Source of truth: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E31_Engagement_Tools_Admin_Suite.md` §1.7 FR-1, §3.4, §4, §5.

## 2. Parent Feature
Feature E.31 — Engagement Tools Admin Suite

## 3. Sub-feature
1.1 Habit Template Management API (Backend ID: **B-01**)

## 4. Objective
Allow content admins to create, list, update, and retire habit templates from the Admin Portal, while structurally guaranteeing that XP-value changes never retroactively alter already-awarded XP on historical `habit_logs`, and that retiring a template never deletes or cascades into historical check-in data.

## 5. Business Requirements
- FR-1 (PRD §1.7): screens — habit template list, template editor (cadence, XP value, icon, age applicability), seasonal habit set builder.
- CRUD: Create habit template; Read usage stats per template; Update XP value/cadence; Retire template (existing logs preserved).
- **Hard rule:** XP-value changes apply only to future check-ins, never retroactively.
- **Hard rule:** retiring a template never deletes historical `habit_logs`.
- Acceptance Criteria (PRD §1.9): updating a habit template's XP value must leave past check-ins' awarded XP unaffected; retiring a template must leave all historical `habit_logs` fully intact.
- Edge Case 1 (PRD §1.10): a retired template referenced by an active in-progress weekly challenge is not automatically invalidated — historical association remains intact; this is an editorial-process concern, not a hard system block.

## 6. Existing Architecture
FastAPI (Python 3.12) + SQLAlchemy 2.0 + PostgreSQL + Redis, per `FAST-API-INSTRUCTIONS.md`. This sub-feature **extends** the existing A.7 Habit Service — it does not introduce a new service. Existing layering to follow: Router → Service → Repository → Model/Schema, with dependency-injected auth/role checks and centralized exception handling, consistent with A.7's own implementation.

## 7. Existing Code to Reuse
- A.7 Habit Service's existing `habit_templates` SQLAlchemy model and `habit_logs` model (read-only reference from this layer).
- A.7's existing check-in evaluation logic that resolves `xp_awarded` at check-in time — this sub-feature must not alter that resolution logic, only add the admin-authoring endpoints in front of it.
- E.28's shared RBAC dependency (`require_role("content_editor")`) and Audit Log Service client.
- E.29's shared content-safety/upload-validation pipeline client, for template icon uploads.

## 8. Files to Create
- `app/routers/admin/habit_templates_router.py`
- `app/schemas/admin/habit_template_schemas.py` (`HabitTemplateCreate`, `HabitTemplateUpdate`, `HabitTemplateRead`, `HabitTemplateXPVersionRead`)
- `app/services/admin/habit_template_admin_service.py`
- `app/repositories/admin/habit_template_admin_repository.py`
- `tests/admin/test_habit_template_admin_api.py`
- `migrations/versions/xxxx_add_habit_template_xp_versioning.py` (if `xp_value` is not already versioned in A.7's schema)

## 9. Files to Modify
- `app/routers/admin/__init__.py` (register new router)
- `app/models/habit_template.py` (add `xp_value_versions` relationship if not already versioned)
- `app/core/audit.py` (register new audit action types: `habit_template.created`, `habit_template.updated`, `habit_template.retired`)

## 10. Backend Requirements
- **Database:** `habit_templates` table (existing, extended if needed with a `habit_template_xp_version` child table: `id`, `habit_template_id` FK, `xp_value`, `effective_from`, `created_by_admin_id`). `habit_logs` is read-only from this layer.
- **Migration:** Additive only — new versioning table, no destructive changes to `habit_templates` or `habit_logs`.
- **Model:** `HabitTemplate`, `HabitTemplateXPVersion` (new).
- **Schema/DTO:** `HabitTemplateCreate` (name, category, cadence, initial `xp_value`, icon_asset_id, age_band), `HabitTemplateUpdate` (cadence/icon/age-band — direct mutation), `HabitTemplateXPUpdate` (new `xp_value` — creates new version row, never mutates existing), `HabitTemplateRead` (includes `usage_stats`).
- **Repository:** `HabitTemplateAdminRepository` — `create()`, `list_with_usage_stats()`, `update_fields()`, `create_xp_version()`, `retire()`.
- **Service:** `HabitTemplateAdminService` — orchestrates validation, versioning logic, audit-log writes, upload-pipeline calls for icon assets.
- **Router:** `POST /v1/admin/habit-templates`, `GET /v1/admin/habit-templates`, `PATCH /v1/admin/habit-templates/{id}`, `POST /v1/admin/habit-templates/{id}/retire`.
- **Dependency Injection:** reuse `get_db_session`, `get_current_admin`, `require_role("content_editor")`.
- **Authentication/Authorization:** JWT admin session (E.28); `content_editor` role minimum for all mutating endpoints.
- **Validation:** cadence must be one of the supported enum values (`daily`, `weekly`, `seasonal`); age_band must reference a valid age-band registry entry; icon must pass E.29 upload-safety pipeline before persisting.
- **Business Rules:** `xp_value` PATCH always inserts a new `HabitTemplateXPVersion` row with `effective_from = now()`; historical `habit_logs.xp_awarded` values are never recalculated, since check-in-time XP resolution reads the version active at that moment. Retire sets `active=false` only — no delete, no cascade.
- **Exception Handling:** `404` for unknown template id, `422` for invalid cadence/age-band, `409` if attempting to retire an already-retired template.
- **Logging:** structured logs on create/update/retire with admin_id, template_id.
- **Caching:** invalidate any Redis-cached "active habit templates by age band" list used by A.7's child-facing endpoint on create/update/retire.
- **Transaction:** template update + XP version insert + audit log write occur within a single DB transaction.
- **Pagination/Filtering/Sorting:** `GET /v1/admin/habit-templates` supports pagination, filter by category/age_band/active status, sort by usage count or created_at.

## 11. KMP Requirements
N/A — this is an admin-only backend endpoint. The KMP app never calls `/v1/admin/*` routes; it continues consuming A.7's existing child-facing habit endpoints, which read the currently-effective `HabitTemplateXPVersion` transparently.

## 12. NextJS Requirements
Consumed by **N-01 Habit Template Management UI** (see `NextJS_Admin/01-habit-template-management-ui.md`). This backend sub-feature must expose all fields the UI's list/editor screens require, including `usage_stats` for the read view.

## 13. API Contract

### `POST /v1/admin/habit-templates`
- **Authentication:** Admin JWT (E.28 session)
- **Authorization:** `content_editor`+
- **Request:**
```json
{
  "name": "Fajr Salah Check-in",
  "category": "salah",
  "cadence": "daily",
  "xp_value": 10,
  "icon_asset_id": "uuid",
  "age_band": "6 to 9"
}
```
- **Response (201):**
```json
{
  "id": "uuid",
  "name": "Fajr Salah Check-in",
  "category": "salah",
  "cadence": "daily",
  "current_xp_value": 10,
  "icon_asset_id": "uuid",
  "age_band": "6 to 9",
  "active": true,
  "created_at": "2026-08-18T00:00:00Z"
}
```
- **Error Responses:** `401 UNAUTHORIZED`, `403 FORBIDDEN`, `422 VALIDATION_ERROR` (invalid cadence/age_band), `422 ICON_UPLOAD_REJECTED` (E.29 pipeline rejection)

### `GET /v1/admin/habit-templates`
- **Authentication:** Admin JWT · **Authorization:** `content_editor`+ (read)
- **Query params:** `page`, `page_size`, `category`, `age_band`, `active`, `sort`
- **Response (200):** paginated list, each item including `usage_stats.total_checkins`, `usage_stats.unique_children`

### `PATCH /v1/admin/habit-templates/{id}`
- **Request (non-versioned fields):** `{ "cadence": "weekly", "icon_asset_id": "uuid", "age_band": "9 to 12" }`
- **Request (versioned XP field, separate concern in same endpoint or dedicated sub-route):** `{ "xp_value": 15 }` → triggers new-version insert, `current_xp_value` reflects the new version going forward only
- **Response (200):** updated `HabitTemplateRead`
- **Error Responses:** `404 NOT_FOUND`, `422 VALIDATION_ERROR`

### `POST /v1/admin/habit-templates/{id}/retire`
- **Response (200):** `{ "id": "uuid", "active": false }`
- **Error Responses:** `404 NOT_FOUND`, `409 ALREADY_RETIRED`

## 14. Database Requirements
- `habit_templates`: existing table, add `active boolean default true` if not already present.
- `habit_template_xp_version` (new, if not already present in A.7's schema): `id PK`, `habit_template_id FK`, `xp_value int`, `effective_from timestamptz`, `created_by_admin_id FK`, indexed on `(habit_template_id, effective_from DESC)`.
- `habit_logs`: read-only from this sub-feature; no schema changes.
- No destructive migrations; no PostgreSQL credential changes.

## 15. Validation
- `cadence` ∈ {`daily`, `weekly`, `seasonal`}
- `age_band` must exist in the platform's age-band registry
- `xp_value` must be a positive integer within platform-configured bounds
- `icon_asset_id` must reference an asset that has passed E.29's content-safety pipeline

## 16. Authentication
Admin JWT bearer token issued by E.28's Admin Identity & Authentication Service; session validated on every request.

## 17. Authorization
`content_editor` role minimum for all create/update/retire operations, per E.28's RBAC matrix. Read (`GET`) available to any authenticated admin role with Engagement module visibility.

## 18. Error Handling
| Scenario | Response |
|---|---|
| Unknown template id | `404 NOT_FOUND` |
| Invalid cadence/age_band | `422 VALIDATION_ERROR` |
| Icon fails upload-safety pipeline | `422 ICON_UPLOAD_REJECTED` |
| Retiring an already-retired template | `409 ALREADY_RETIRED` |
| Unauthenticated request | `401 UNAUTHORIZED` |
| Insufficient role | `403 FORBIDDEN` |
| Database failure | `500 INTERNAL_ERROR` (logged, generic message returned) |

## 19. Offline First
N/A — internal admin backend, no offline requirement.

## 20. Local Data
N/A.

## 21. Localization
Habit template `name`/description fields should support the platform's localization key pattern (English/Hindi/Arabic/Urdu) consistent with how A.7 already localizes child-facing habit copy — reuse the existing localization-key foreign reference rather than storing raw strings per locale in this table.

## 22. RTL
N/A at the API layer (handled in NextJS UI, N-01).

## 23. Analytics
Emits `habit_template_created`, `habit_template_updated`, `habit_template_retired` (PRD §1.19) via the platform's shared analytics/event bus, with `admin_id`, `template_id`, `changed_fields` as parameters.

## 24. Performance
- `usage_stats` aggregation should be computed via an indexed query or a periodically-refreshed materialized view (not a live full-table scan of `habit_logs` per request) — evaluate against expected `habit_logs` volume.
- Redis cache invalidation on write to keep A.7's child-facing "active templates" list consistent without excessive cache churn.
- Async DB session usage throughout (no blocking calls in the async route handlers).

## 25. Security
- No child PII exposed by this endpoint set.
- All mutations audit-logged to E.28's immutable `audit_log` with admin identity, before/after diff.
- Icon assets routed through E.29's content-safety pipeline — no bypass path.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 (async), Pydantic v2, pytest + pytest-asyncio, httpx (test client), existing internal `audit_log_client` and `upload_safety_client` packages already used by A.7/E.29.

## 27. Testing
- **Unit tests:** service-layer XP-versioning logic; retire logic; validation rules.
- **Integration tests:** full create → update xp_value → verify historical `habit_logs.xp_awarded` unaffected (signature no-retroactivity test per PRD §5 item 1); full retire → verify `habit_logs` still queryable and intact.
- **Edge cases:** retiring a template referenced by an active challenge (Edge Case 1) — confirm no exception thrown, challenge remains valid.
- **Negative cases:** invalid cadence, invalid age_band, unauthorized/forbidden requests, unknown id.

## 28. Documentation
OpenAPI schema auto-generated via FastAPI; add descriptive docstrings on router functions covering the non-retroactivity guarantee explicitly, since this is a easy-to-misunderstand behavior for future maintainers.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create/Extend Database Models**
- Task ID: B-01-T01
- Objective: Add `HabitTemplateXPVersion` model (if not already present) and `active` flag on `HabitTemplate`.
- Why This Is Required: Non-retroactivity is only structurally guaranteed if XP values are versioned rows, not a single mutable column.
- Existing Architecture to Follow: A.7's existing SQLAlchemy model conventions in `app/models/habit_template.py`.
- Existing Files to Reuse: `app/models/habit_template.py`, `app/models/habit_log.py` (read-only reference).
- Files to Create: `app/models/habit_template_xp_version.py`.
- Files to Modify: `app/models/habit_template.py`.
- Implementation Details: FK relationship `HabitTemplate.xp_versions`, ordered by `effective_from DESC`; add `active` boolean column with default `True`.
- Business Rules: never allow deletion of a `HabitTemplateXPVersion` row via any endpoint.
- Validation: `xp_value > 0` at the DB constraint level (`CHECK`).
- Error Handling: migration must be additive/backward-compatible.
- Security: no PII in this table.
- Performance: index `(habit_template_id, effective_from DESC)`.
- Localization/RTL/Analytics: N/A at this task.
- Tests: migration up/down test.
- Documentation: migration docstring explaining the versioning rationale.
- Dependencies: none.
- Do Not Change: `habit_logs` table schema.
- Expected Result: new versioning table exists, `HabitTemplate.active` exists.
- Definition of Done: migration applies cleanly on staging with fixture data, rollback verified.

**Task 02 — Implement Repository Layer**
- Task ID: B-01-T02
- Objective: Build `HabitTemplateAdminRepository` with `create`, `list_with_usage_stats`, `update_fields`, `create_xp_version`, `retire`.
- Why This Is Required: Keep DB access isolated from service/business logic per existing layered architecture.
- Existing Architecture to Follow: Repository pattern used across A.7/A.11/A.12.
- Files to Create: `app/repositories/admin/habit_template_admin_repository.py`.
- Implementation Details: `create_xp_version` always INSERTs, never UPDATEs an existing version row.
- Error Handling: raise domain-specific exceptions (`TemplateNotFoundError`, `AlreadyRetiredError`) for the service layer to translate to HTTP errors.
- Tests: repository-level unit tests against a test DB/fixtures.
- Dependencies: Task 01.
- Do Not Change: existing A.7 child-facing repository methods.
- Expected Result: repository fully covers all required data operations.
- Definition of Done: unit tests green.

**Task 03 — Implement Service Layer**
- Task ID: B-01-T03
- Objective: Build `HabitTemplateAdminService` implementing validation, versioning orchestration, audit logging, cache invalidation, upload-pipeline integration.
- Files to Create: `app/services/admin/habit_template_admin_service.py`.
- Implementation Details: wraps repository calls in a single DB transaction per operation; calls `audit_log_client.record()` and `upload_safety_client.validate_asset()`.
- Business Rules: XP update path always calls `create_xp_version`, never `update_fields` for `xp_value`.
- Validation: cadence/age_band enum checks.
- Error Handling: translate domain exceptions to service-level errors.
- Security: role check delegated to router dependency, but service double-checks `content_editor`+ role as defense-in-depth.
- Tests: unit tests with mocked repository/audit/upload clients.
- Dependencies: Task 02.
- Expected Result: full business logic implemented and testable in isolation.
- Definition of Done: unit tests green, no direct DB calls in service tests (mocked).

**Task 04 — Implement API Endpoints**
- Task ID: B-01-T04
- Objective: Build FastAPI router with the four endpoints in §13.
- Files to Create: `app/routers/admin/habit_templates_router.py`.
- Files to Modify: `app/routers/admin/__init__.py`.
- Implementation Details: use `Depends(get_current_admin)`, `Depends(require_role("content_editor"))`; Pydantic response models per §13.
- Error Handling: map service exceptions to `404`/`409`/`422` via FastAPI exception handlers.
- Documentation: OpenAPI summary/description per endpoint, explicitly noting non-retroactivity behavior on the XP PATCH endpoint.
- Tests: endpoint-level tests via httpx async client.
- Dependencies: Task 03.
- Expected Result: all four endpoints functional end-to-end against a test DB.
- Definition of Done: integration tests green.

**Task 05 — Add Non-Retroactivity Regression Test (Signature Test)**
- Task ID: B-01-T05
- Objective: Prove the PRD's hardest guarantee.
- Implementation Details: seed a fixture `habit_log` with `xp_awarded=10` tied to an XP version effective before "now"; PATCH the template's `xp_value` to `15`; re-fetch the fixture `habit_log` and assert `xp_awarded` is still `10`.
- Tests: `tests/admin/test_habit_template_admin_api.py::test_xp_update_does_not_affect_historical_logs`.
- Dependencies: Tasks 01–04.
- Expected Result: test passes, proving structural non-retroactivity.
- Definition of Done: test is part of the CI-blocking suite per PRD §10.

**Task 06 — Retire Flow + Referenced-Challenge Edge Case Test**
- Task ID: B-01-T06
- Objective: Verify retire never cascades/deletes, and a retired template referenced by an active challenge doesn't break that challenge.
- Tests: `test_retire_preserves_habit_logs`, `test_retire_template_referenced_by_active_challenge_does_not_invalidate_challenge`.
- Dependencies: Tasks 01–04.
- Definition of Done: both tests pass.

**Task 07 — API Documentation & Final Review**
- Task ID: B-01-T07
- Objective: Finalize OpenAPI docs, run full lint/type-check, self-review against this blueprint's checklist.
- Dependencies: Tasks 01–06.
- Definition of Done: all checklist items in §31 verified.

## 30. Definition of Done
- All four endpoints implemented, authenticated, authorized, validated, and audit-logged.
- XP-value non-retroactivity proven by an automated regression test using fixture historical data.
- Retire never deletes/cascades into `habit_logs`.
- Redis cache invalidated correctly on write.
- Full pytest suite (unit + integration) green.
- OpenAPI documentation complete and accurate.
- No changes made to PostgreSQL/Redis credentials.

## 31. Final Verification Checklist
- [ ] `POST /v1/admin/habit-templates` creates a template with an initial XP version
- [ ] `GET /v1/admin/habit-templates` returns paginated list with usage stats
- [ ] `PATCH .../{id}` for non-versioned fields mutates in place
- [ ] `PATCH .../{id}` for `xp_value` inserts a new version row, never mutates existing
- [ ] Historical `habit_logs.xp_awarded` unaffected by XP-value update (regression test green)
- [ ] `POST .../{id}/retire` sets `active=false`, no delete, no cascade
- [ ] Retired-template-referenced-by-active-challenge edge case does not error
- [ ] Unauthorized (`401`) and forbidden (`403`) paths tested
- [ ] Invalid cadence/age_band rejected with `422`
- [ ] Icon upload routed through E.29 pipeline, rejection path tested
- [ ] Every mutation writes an audit log entry to E.28's shared `audit_log`
- [ ] Redis cache invalidated on create/update/retire
- [ ] No school/madrasa/institutional-tier logic introduced
- [ ] PostgreSQL and Redis credentials untouched
