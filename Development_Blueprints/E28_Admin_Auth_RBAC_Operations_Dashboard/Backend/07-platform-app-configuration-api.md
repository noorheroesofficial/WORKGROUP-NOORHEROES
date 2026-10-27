# B-07 — Platform App Configuration Management API

## 1. Feature Context
Part of E.28. Manages remote app configuration (force-update, trial length, defaults); production-environment changes always require maker-checker approval, non-production may proceed with single-admin approval (FR-13).

## 2. Parent Feature
E.28 — Admin Portal: Authentication, RBAC & Operations Dashboard

## 3. Sub-feature
B-07 — Platform App Configuration Management API

## 4. Objective
Implement `GET`/`PATCH /api/v1/admin/config` such that any change targeting `environment=production` creates a `change_proposal` via B-04, while non-production targets may apply directly for `admin+`.

## 5. Business Requirements
- FR-13: production config changes require maker-checker; non-production may proceed with single-admin approval.
- Acceptance Criteria: production config change requires maker-checker approval; identical change against non-production does not.

## 6. Existing Architecture
No existing app-configuration module. New submodule within `admin` context, structurally near-identical to B-06 (same maker-checker-routing pattern, different trigger condition — `environment` field instead of `requires_two_person_approval` flag).

## 7. Existing Code to Reuse
| Component | Location | Reuse For |
|---|---|---|
| `BaseRepository`, `BaseService` | `common/` | Scaffolding |
| `require_admin_permission` | B-03 | Route gating |
| `MakerCheckerService.create_proposal()` | B-04 | Production-change routing |
| `AuditLogService.log_action()` | B-05 | Direct-apply audit writes |
| `Environment` enum | `core/settings.py` | Reuse the platform's existing `LOCAL/DEVELOPMENT/STAGING/PRODUCTION` enum rather than inventing a parallel one |

## 8. Files to Create
- `src/noorheroes/modules/admin/app_config/models.py` — `AppConfigOrm`
- `src/noorheroes/modules/admin/app_config/schemas.py`
- `src/noorheroes/modules/admin/app_config/repository.py`
- `src/noorheroes/modules/admin/app_config/service.py`
- `src/noorheroes/modules/admin/app_config/api.py`
- `alembic/versions/xxxx_create_app_config_table.py`
- `tests/modules/admin/app_config/test_app_config_api.py`

## 9. Files to Modify
None outside this new submodule.

## 10. Backend Requirements
- **Model:** `app_config(config_id PK, environment, key, value jsonb, updated_at)` — `environment` reuses `core/settings.py::Environment`.
- **`GET /api/v1/admin/config`:** `admin+`.
- **`PATCH /api/v1/admin/config`:** if `environment == PRODUCTION`, always route to `MakerCheckerService.create_proposal(proposal_type="app_config_change", ...)`; else apply directly for `admin+` with an audit write.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
Consumed by `N-08 — App Configuration Editor`.

## 13. API Contract
### `GET /api/v1/admin/config`
- **Auth:** `admin+`
- **Response 200:** `{ "configs": [ { "config_id": "...", "environment": "production", "key": "force_update_min_version", "value": "1.4.0" } ] }`

### `PATCH /api/v1/admin/config`
- **Auth:** `admin+`
- **Request:** `{ "config_id": "...", "value": {...} }`
- **Response 200 (non-production, direct apply):** updated config object
- **Response 202 (production, proposal created):** `{ "status": "pending_approval", "proposal_id": "..." }`
- **Error Responses:** `404 CONFIG_NOT_FOUND`, `422`

## 14. Database Requirements
`app_config` composite-unique on `(environment, key)`; no cross-context FK.

## 15. Validation
`value` schema-validated per `key`'s expected type (e.g., `force_update_min_version` must be a valid semver string); `environment` must be a valid `Environment` enum value.

## 16. Authentication
Delegated to B-01/B-02.

## 17. Authorization
`admin+` baseline for all config operations (per PRD API table, no `super_admin` distinction here unlike feature flags — production-vs-non-production is the routing axis, not role tier).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Production change submitted | Always creates proposal, never applies directly, regardless of who submits it |
| Non-production change | Applies directly for admin+ |
| Unknown config_id | `404 CONFIG_NOT_FOUND` |
| Invalid value type for key | `422` |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Config values are technical, not user-facing text; no localization needed.

## 22. RTL
N/A.

## 23. Analytics
Supports `app_config_change_proposed`, `app_config_change_applied` (client-fired).

## 24. Performance
Config reads may be cached (Redis) for app-startup-time consumption by the mobile/web clients themselves — out of scope for this admin-management blueprint, noted for awareness only.

## 25. Security
Production-routing check must be evaluated server-side against the *actual* config row's `environment`, never trusted from client-supplied request metadata, preventing a client from mislabeling a production change as non-production to bypass maker-checker.

## 26. Library Requirements
No new libraries.

## 27. Testing
- Unit: production-routing (always proposal) vs. non-production (direct apply) branching.
- Integration: both paths end-to-end.
- Security test: client cannot spoof `environment` to bypass maker-checker (server resolves `environment` from the stored config row, not the request body).

## 28. Documentation
OpenAPI schema for both endpoints.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create `AppConfigOrm` + Migration**
- Task ID: B-07-T01
- Files to Create: `app_config/models.py`, migration.
- Implementation Details: Reuse `core/settings.py::Environment` enum for the `environment` column type.
- Definition of Done: Table live, `(environment, key)` unique.

**Task 02 — Implement Repository & Service**
- Task ID: B-07-T02
- Files to Create: `app_config/repository.py`, `app_config/service.py`.
- Dependencies: Task 01.
- Definition of Done: Unit tests pass.

**Task 03 — Implement PATCH Routing Logic**
- Task ID: B-07-T03
- Objective: Production always proposes; non-production applies directly.
- Implementation Details: Resolve `environment` from the stored config row server-side, never from client input, before branching.
- Dependencies: B-04 Task 03, B-05 Task 02.
- Tests: Both-path test, plus the environment-spoofing security test.
- Definition of Done: Both paths verified; spoofing attempt fails.

**Task 04 — Implement GET/PATCH Endpoints**
- Task ID: B-07-T04
- Files to Create: `app_config/api.py`.
- Dependencies: Task 02, Task 03, B-03 Task 05.
- Definition of Done: Integration tests pass.

**Task 05 — Full Test Suite + Documentation**
- Task ID: B-07-T05
- Dependencies: Tasks 01–04.
- Definition of Done: All §27 scenarios green; OpenAPI updated.

## 30. Definition of Done
- Config CRUD live; production changes always routed through maker-checker; non-production applies directly with audit write; environment resolved server-side, not client-spoofable.

## 31. Final Verification Checklist
- [ ] Production config PATCH always creates a proposal
- [ ] Non-production config PATCH applies directly with an audit entry
- [ ] `environment` resolved from the stored row, not client input (spoofing test passes)
- [ ] `(environment, key)` uniqueness enforced
- [ ] OpenAPI docs updated
