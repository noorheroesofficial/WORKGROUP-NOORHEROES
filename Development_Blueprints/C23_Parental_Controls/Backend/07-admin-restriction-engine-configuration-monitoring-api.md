# B-07 — Admin Restriction Engine Configuration & Monitoring API

## 1. Feature Context
Internal admin/ops need to tune platform-wide default screen-time/bedtime suggestions, manage the AI-permission-default-by-age-band ceiling table that B-04 enforces against, and monitor Restriction Engine health and override activity for support/trust-safety investigation (PRD C.23 §8, §9).

## 2. Parent Feature
Feature C.23 — Parental Controls (Screen Time, Bedtime, AI Permissions, Content Age Level)

## 3. Sub-feature
1.7 Admin Restriction Engine Configuration & Monitoring API (ID: **B-07**)

## 4. Objective
Implement admin-scoped endpoints for (a) platform-wide default screen-time/bedtime suggestion configuration, (b) the AI-permission-default-by-age-band ceiling table (the same table B-04 reads for its enforcement), (c) a read-only Restriction Engine health monitor, and (d) a read-only, paginated override audit log.

## 5. Business Requirements
- §8 Admin Requirements: Restriction Engine Configuration Defaults (update-only, `product_admin`); Health Monitor (read-only, `product_admin`/`content_editor`); Override Audit Log (read-only, `support`/`trust_safety`).
- §12.5: AI-permission-default-by-age-band table changes require `ai_ops` sign-off given platform-wide safety-ceiling implications.
- Configuration Default changes write an immutable audit_log row (reuse `modules/admin::AdminAuditLog`).

## 6. Existing Architecture
Lives in `modules/restrictions` for the config/monitoring logic, using `modules/admin::AdminAuditRepository.log_action()` for audit trail and `core/deps.py::require_admin_scope()` for RBAC. This is the authoritative source B-04's `ai_ceiling.py` reads from — B-04's Task 04 depends on this sub-feature's age-band ceiling table existing.

## 7. Existing Code to Reuse
- `core/deps.py::get_current_admin`, `require_admin_scope(scope: str)`
- `modules/admin/service.py::AdminService.log_action()` — immutable audit trail
- `modules/admin/repository.py::AdminAuditRepository`
- `common/base_repository.py::PageResult`, pagination pattern

## 8. Files to Create
- `src/noorheroes/modules/restrictions/admin_models.py` — `RestrictionDefaultsOrm`, `AiPermissionCeilingOrm`
- `src/noorheroes/modules/restrictions/admin_schemas.py` — `RestrictionDefaultsResponse/UpdateRequest`, `AiCeilingTableResponse/UpdateRequest`, `HealthMonitorResponse`, `OverrideAuditLogEntry`
- `src/noorheroes/modules/restrictions/admin_repository.py` — `RestrictionDefaultsRepository`, `AiCeilingRepository`
- `src/noorheroes/modules/restrictions/admin_service.py` — `RestrictionAdminService(BaseService)`
- `alembic/versions/xxxx_create_restriction_defaults_ai_ceiling.py`
- `tests/modules/restrictions/test_admin_service.py`
- `tests/modules/restrictions/test_admin_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/restrictions/api.py` — add admin sub-router (or a separate `admin_api.py` mounted under `/v1/admin/restrictions`)
- `src/noorheroes/modules/restrictions/ai_ceiling.py` (B-04) — read `AiCeilingRepository` instead of any hardcoded/placeholder default once this sub-feature is live

## 10. Backend Requirements
- `GET/PATCH /v1/admin/restrictions/defaults` — suggested (never enforced) default screen-time/bedtime values shown to parents during initial configuration; `require_admin_scope("product_admin")`.
- `GET/PATCH /v1/admin/restrictions/ai-ceiling` — the age-band → AI-capability-ceiling table; PATCH requires an additional `ai_ops` sign-off marker (a secondary approval field/flow — confirm exact sign-off mechanism against the platform's existing dual-approval pattern, if any, before inventing one; at minimum require `require_admin_scope("ai_ops")` in addition to `product_admin`).
- `GET /v1/admin/restrictions/health` — read-only aggregate metrics: heartbeat-processing latency (p50/p95/p99), override-grant frequency by type, limit/bedtime-block event volume over a selectable time window; `require_admin_scope("product_admin")` or `("content_editor")`.
- `GET /v1/admin/restrictions/overrides` — paginated, read-only list of `parent_overrides` (from B-03), masked child identifier; `require_admin_scope("support")` or `("trust_safety")`.
- Every configuration-default change writes an `AdminAuditLog` row via `AdminService.log_action()`.

## 11. API Contract

### `GET/PATCH /v1/admin/restrictions/defaults`
- **Auth:** Bearer (admin) + `product_admin` scope
- **Request (PATCH):** `{ "suggested_daily_limit_minutes": 45, "suggested_bedtime_start": "20:00", "suggested_bedtime_end": "07:00" }`
- **Response 200:** same shape
- **Error Responses:** `401`, `403`, `422`

### `GET/PATCH /v1/admin/restrictions/ai-ceiling`
- **Auth:** Bearer (admin) + `product_admin` + `ai_ops` scopes (PATCH only)
- **Request (PATCH):** `{ "age_band": "4 to 6", "ai_enabled_default": true, "voice_interaction_default": false, "curated_only_default": true }`
- **Response 200:** full ceiling table
- **Error Responses:** `401`, `403` (missing `ai_ops` sign-off), `422`

### `GET /v1/admin/restrictions/health`
- **Auth:** Bearer (admin) + `product_admin`/`content_editor` scope
- **Response 200:** `{ "heartbeat_latency_p99_ms": 120, "override_grant_frequency": {...}, "block_event_volume": {...} }`

### `GET /v1/admin/restrictions/overrides`
- **Auth:** Bearer (admin) + `support`/`trust_safety` scope
- **Response 200:** paginated `PageResult[OverrideAuditLogEntry]` with masked `child_id`

## 12. Database Requirements
`restriction_defaults`: singleton/config row. `ai_permission_ceiling`: `age_band PK`, `ai_enabled_default`, `voice_interaction_default`, `curated_only_default`, `updated_at`, `updated_by`. Health monitor reads aggregates from `screen_time_usage_daily`/`parent_overrides`/`child_restriction_events` (no new table). Override audit log reads directly from B-03's `parent_overrides`.

## 13. Validation
- Ceiling table values must be internally consistent (e.g., `curated_only_default=true` implies `ai_enabled_default=true`).
- Defaults are suggestions only — must never be interpreted as enforced limits by B-01/B-02 when a child has no configured policy (explicit non-goal, confirm B-01's "no limit = unrestricted" default is untouched by this table).

## 14. Authentication
`Depends(get_current_admin)`.

## 15. Authorization
`require_admin_scope()` per endpoint per §10/§11; ceiling-table PATCH requires the additional `ai_ops` sign-off.

## 16. Error Handling
| Scenario | Response |
|---|---|
| Missing required scope | 403 FORBIDDEN |
| Ceiling PATCH without `ai_ops` sign-off | 403 FORBIDDEN |
| Invalid age band | 422 VALIDATION_ERROR |

## 17. Offline First
N/A (admin web only).

## 18. Local Data
N/A.

## 19. Localization
Admin portal-side i18n handled by NextJS layer (N-01/N-02/N-03); this API returns raw values.

## 20. RTL
N/A (backend).

## 21. Analytics
Feeds N-02's health monitor dashboard directly.

## 22. Performance
Health monitor aggregation queries should use pre-aggregated/indexed reads, not full-table scans over `screen_time_usage_daily` at admin-portal request time — consider a materialized view or scheduled aggregation job if volume warrants (coordinate with DevOps given B-02's high write volume).

## 23. Security
Ceiling-table changes are the platform's most safety-sensitive admin action in this feature — the dual-scope (`product_admin` + `ai_ops`) requirement is non-negotiable and must be tested explicitly. Override audit log masks child identifiers to limit PII exposure even to authorized support staff.

## 24. Library Requirements
FastAPI, SQLAlchemy 2.0 async. No new dependencies.

## 25. Testing
- Unit: ceiling-table PATCH rejected without `ai_ops` scope even when `product_admin` scope is present.
- Unit: override audit log masks child identifiers correctly.
- Integration: B-04's `ai_ceiling.py` correctly reads updated values after a PATCH here (cross-feature test).
- Integration: health monitor aggregates match manually-computed expected values against seeded test data.

## 26. Documentation
OpenAPI documents the dual-approval requirement for ceiling-table changes and the masking behavior of the override audit log.

## 27. AI Coding Agent Implementation Steps

**Task 01 — Create `RestrictionDefaultsOrm` and `AiPermissionCeilingOrm` Models**
- Files to Create: `admin_models.py`

**Task 02 — Create Migration**
- Files to Create: `alembic/versions/xxxx_create_restriction_defaults_ai_ceiling.py`
- Implementation Details: Seed the ceiling table with sane initial per-age-band defaults matching the platform's current AI-safety posture (confirm actual current defaults against `ai_safety` module rather than inventing values).

**Task 03 — Create Admin Schemas**
- Files to Create: `admin_schemas.py`

**Task 04 — Implement Repositories**
- Files to Create: `admin_repository.py`

**Task 05 — Implement `RestrictionAdminService`**
- Dependencies: Tasks 01–04.
- Implementation Details: Per §10; dual-scope check for ceiling PATCH.

**Task 06 — Wire B-04's `ai_ceiling.py` to Read This Table**
- Files to Modify: `modules/restrictions/ai_ceiling.py`
- Dependencies: B-04 must already exist; this task closes the loop between B-04's enforcement and B-07's configuration.

**Task 07 — Implement Health Monitor Aggregation Query**
- Objective: Efficient aggregate reads; consider materialized view given B-02's write volume.

**Task 08 — Implement Override Audit Log Endpoint with Masking**
- Implementation Details: Mask `child_id` (e.g., partial ID or family-level identifier only) per support/trust-safety access pattern.

**Task 09 — Implement API Router**
- Files to Modify/Create: `admin_api.py` or extend `restrictions/api.py`

**Task 10 — Add RBAC Scope Enforcement Tests**
- Files to Create: `tests/modules/restrictions/test_admin_service.py`
- Coverage: dual-scope requirement for ceiling changes.

**Task 11 — Add Cross-Feature Integration Test with B-04**
- Objective: Confirm ceiling updates here are correctly enforced there.

**Task 12 — Add Admin Audit Log Wiring**
- Implementation Details: `AdminService.log_action()` call on every defaults/ceiling change.

**Task 13 — Add API Documentation**

**Task 14 — Final Code Review**

## 28. Definition of Done
- Ceiling-table PATCH enforces dual-scope (`product_admin` + `ai_ops`) requirement, tested.
- B-04 correctly reads updated ceiling values (cross-feature integration test passes).
- Health monitor and override audit log are strictly read-only with correct RBAC scoping.
- All configuration-default changes produce an immutable admin audit log row.

## 29. Final Verification Checklist
- [ ] Dual-scope enforcement on ceiling-table PATCH tested
- [ ] B-04 integration confirmed working end-to-end
- [ ] Override audit log masks child identifiers
- [ ] Health monitor uses efficient aggregation (not full-table scans)
- [ ] Every config-default change writes an immutable audit log row
- [ ] OpenAPI documents dual-approval and masking behavior
