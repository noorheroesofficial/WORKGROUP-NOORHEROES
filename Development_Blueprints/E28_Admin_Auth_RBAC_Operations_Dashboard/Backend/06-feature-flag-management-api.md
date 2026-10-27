# B-06 — Feature Flag Management API

## 1. Feature Context
Part of E.28. Read/update rollout percentage and targeting for platform feature flags; safety/AI-classified flags require two-person approval via B-04's maker-checker workflow (FR-9).

## 2. Parent Feature
E.28 — Admin Portal: Authentication, RBAC & Operations Dashboard

## 3. Sub-feature
B-06 — Feature Flag Management API

## 4. Objective
Implement `GET`/`PATCH /api/v1/admin/feature-flags` such that safety/AI-classified flags route through B-04's `change_proposal` mechanism, while all other flags apply directly for `admin+`.

## 5. Business Requirements
- FR-9: safety/AI flags require two-person approval (super admin); other flags require standard admin+ access.
- Edge Case 4: a flag not originally tagged safety/AI later reclassified — `requires_two_person_approval` must be explicitly re-evaluated and updated, never automatically inherited from naming similarity alone; but any flag genuinely touching AI/safety behavior must be correctly classified before its next toggle.
- Acceptance Criteria: super admin toggling a safety/AI flag requires a second super admin's approval; non-safety flag change by admin+ does not require this.

## 6. Existing Architecture
No existing feature-flag infrastructure in the codebase — new module within the `admin` context. Depends on B-03 (permission gating) and B-04 (maker-checker routing) and B-05 (audit writes).

## 7. Existing Code to Reuse
| Component | Location | Reuse For |
|---|---|---|
| `BaseRepository`, `BaseService` | `common/` | Scaffolding |
| `require_admin_permission` | B-03, `core/deps.py` | Route gating |
| `MakerCheckerService.create_proposal()` | B-04 | Safety/AI flag routing |
| `AuditLogService.log_action()` | B-05 | Direct-apply audit writes |
| `get_redis_pool()` | `infrastructure/redis.py` | Optional flag-evaluation cache for downstream services consuming flags |

## 8. Files to Create
- `src/noorheroes/modules/admin/feature_flags/models.py` — `FeatureFlagOrm`
- `src/noorheroes/modules/admin/feature_flags/schemas.py`
- `src/noorheroes/modules/admin/feature_flags/repository.py`
- `src/noorheroes/modules/admin/feature_flags/service.py`
- `src/noorheroes/modules/admin/feature_flags/api.py`
- `alembic/versions/xxxx_create_feature_flag_table.py`
- `tests/modules/admin/feature_flags/test_feature_flag_api.py`

## 9. Files to Modify
None outside this new submodule (registers its router in the main `api_v1_router`).

## 10. Backend Requirements
- **Model:** `feature_flag(flag_id PK, key UNIQUE, rollout_percentage int, targeting jsonb, requires_two_person_approval bool, updated_at)`.
- **`GET /api/v1/admin/feature-flags`:** `admin+`.
- **`PATCH /api/v1/admin/feature-flags`:** if target flag's `requires_two_person_approval=true`, call `MakerCheckerService.create_proposal(proposal_type="feature_flag_change", ...)`; else apply directly for `admin+` and write an audit entry via `AuditLogService.log_action()`.
- **Reclassification:** a distinct, explicitly-invoked action (not a side effect of a normal toggle) allowing an authorized admin to change `requires_two_person_approval` itself — this reclassification action is itself audited and, being a safety-relevant metadata change, should require `super_admin`.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
Consumed by `N-07 — Feature Flag Management UI`.

## 13. API Contract
### `GET /api/v1/admin/feature-flags`
- **Auth:** `admin+`
- **Response 200:** `{ "flags": [ { "flag_id": "...", "key": "...", "rollout_percentage": 25, "targeting": {}, "requires_two_person_approval": false } ] }`

### `PATCH /api/v1/admin/feature-flags`
- **Auth:** `admin+` (super admin for AI/safety flags, per PRD API table)
- **Request:** `{ "flag_id": "...", "rollout_percentage": 50, "targeting": {} }`
- **Response 200 (direct apply):** updated flag object
- **Response 202 (proposal created):** `{ "status": "pending_approval", "proposal_id": "..." }`
- **Error Responses:** `403 FORBIDDEN` (insufficient role for a safety/AI flag), `404 FLAG_NOT_FOUND`, `422`

## 14. Database Requirements
`feature_flag.key` unique; no cross-context FK.

## 15. Validation
`rollout_percentage` bounded 0–100; `targeting` schema-validated jsonb structure; `key` immutable after creation.

## 16. Authentication
Delegated to B-01/B-02.

## 17. Authorization
`admin+` baseline; `super_admin` for safety/AI-classified flags and for reclassification actions (B-03's permission matrix).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Non-super-admin attempts safety/AI flag toggle | `403 FORBIDDEN` |
| Unknown flag_id | `404 FLAG_NOT_FOUND` |
| Invalid rollout percentage | `422` |
| Duplicate key on create | `409 DUPLICATE_FLAG_KEY` |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Flag `key`/targeting rules are technical identifiers; no localization needed server-side.

## 22. RTL
N/A.

## 23. Analytics
Supports `feature_flag_toggled`, `feature_flag_two_person_approval_required_shown` (client-fired).

## 24. Performance
Flag reads should be cache-friendly (Redis) for downstream services evaluating flags at request time — though B-06 itself only covers the admin management API, not the runtime flag-evaluation SDK (out of scope, presumed to exist or be built separately).

## 25. Security
Reclassification of `requires_two_person_approval` is itself a sensitive action — audited, `super_admin`-gated, never silently inherited from key-naming patterns (Edge Case 4).

## 26. Library Requirements
No new libraries.

## 27. Testing
- Unit: direct-apply path (non-safety flag), proposal-routing path (safety/AI flag), reclassification action.
- Integration: both PATCH routing paths (§5 Backend AI prompt item 7 — tests for both routing paths).
- Edge Case 4 test: reclassification requires explicit action, never automatic.

## 28. Documentation
OpenAPI schema for both endpoints.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create `FeatureFlagOrm` + Migration**
- Task ID: B-06-T01
- Files to Create: `feature_flags/models.py`, migration.
- Definition of Done: Table live, `key` unique.

**Task 02 — Implement Repository & Service**
- Task ID: B-06-T02
- Files to Create: `feature_flags/repository.py`, `feature_flags/service.py`.
- Implementation Details: `list_flags()`, `get_by_key()`, `apply_direct_update()`, `reclassify()`.
- Dependencies: Task 01.
- Definition of Done: Unit tests pass.

**Task 03 — Implement PATCH Routing Logic (Both Paths)**
- Task ID: B-06-T03
- Objective: Route safety/AI flags to maker-checker, others direct.
- Implementation Details: Branch on `requires_two_person_approval`; direct path calls `AuditLogService.log_action()`; proposal path calls `MakerCheckerService.create_proposal()`.
- Dependencies: B-04 Task 03, B-05 Task 02.
- Tests: Both-path test per §5 Backend AI prompt item 7.
- Definition of Done: Both paths verified in integration tests.

**Task 04 — Implement GET/PATCH Endpoints**
- Task ID: B-06-T04
- Files to Create: `feature_flags/api.py`.
- Dependencies: Task 02, Task 03, B-03 Task 05.
- Definition of Done: Integration tests pass for all documented responses.

**Task 05 — Implement Reclassification Action**
- Task ID: B-06-T05
- Objective: Explicit, audited, super-admin-gated reclassification (Edge Case 4).
- Dependencies: Task 02.
- Definition of Done: Reclassification test confirms it never happens automatically.

**Task 06 — Full Test Suite + Documentation**
- Task ID: B-06-T06
- Dependencies: Tasks 01–05.
- Definition of Done: All §27 scenarios green; OpenAPI updated.

## 30. Definition of Done
- Feature flag CRUD live; safety/AI flags routed through maker-checker; other flags apply directly with audit write; reclassification explicit and audited.

## 31. Final Verification Checklist
- [ ] Safety/AI flag PATCH creates a proposal, never applies directly
- [ ] Non-safety flag PATCH applies directly with an audit entry
- [ ] Reclassification requires explicit super-admin action, never automatic (Edge Case 4)
- [ ] `rollout_percentage` bounds validated
- [ ] OpenAPI docs updated
