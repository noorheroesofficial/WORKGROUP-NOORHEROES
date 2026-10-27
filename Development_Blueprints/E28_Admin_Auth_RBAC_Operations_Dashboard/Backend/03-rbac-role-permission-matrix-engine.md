# B-03 — RBAC Role & Permission Matrix Engine

## 1. Feature Context
Part of E.28. Replaces the existing flat `admin:read`/`admin:write` scope check (currently the only authorization mechanism in `AdminRouter`) with the PRD-mandated multi-dimensional model: **role + resource_scope + region + locale + action** (FR-5). This is the authorization backbone every other Admin module (E.29–E.34) queries.

## 2. Parent Feature
E.28 — Admin Portal: Authentication, RBAC & Operations Dashboard

## 3. Sub-feature
B-03 — RBAC Role & Permission Matrix Engine

## 4. Objective
Implement the canonical nine-role model (FR-4), a queryable role/permission matrix, and a service-layer authorization check that is the actual security boundary regardless of what the UI hides (FR-5, Edge Case 6).

## 5. Business Requirements
- FR-4: canonical roles — Super Admin, Content Editor, Publisher, Scholar Reviewer, Child Safety Reviewer, Support Agent, Billing Ops, Analyst, Localization Manager.
- FR-5: authorization computed from role + resource scope + region + locale + action — not a flat lookup.
- Edge Case 6: a role lacking a permission attempting to directly call a downstream endpoint (bypassing UI) is rejected identically at the service layer — the UI's hiding is convenience, never the boundary.
- Acceptance Criteria: `GET /v1/admin/roles` / `PATCH /v1/admin/roles/{id}/permissions` gated to `super_admin`.

## 6. Existing Architecture
- Current state: `require_admin_scope(required_scope: str)` in `core/deps.py` is a flat string-scope factory (`Depends(require_admin_scope("admin:write"))`) — this is the pattern B-03 must **generalize**, not discard; existing call sites (`AdminRouter`, `ContentRouter`'s `admin:write` check, `NotificationRouter`'s `admin:write` check) will need to migrate to the new multi-dimensional dependency over time, but B-03 itself only needs to ship the new mechanism and apply it within the `admin` module's own routes — downstream module migration is each module's own responsibility when E.29–E.34 are built.
- `AdminSessionContext` (`core/deps.py`) currently carries `scopes: list[str]` — B-03 extends this DTO to also carry the resolved permission matrix (or a resolver reference) so `require_admin_permission()` can evaluate multi-dimensional checks without re-querying the DB on every request (cache in Redis, see Task 06).
- Depends on B-01 (`admin_user`) for `admin_id` identity.

## 7. Existing Code to Reuse
| Component | Location | Reuse For |
|---|---|---|
| `require_admin_scope` (pattern, not code) | `core/deps.py` | Structural template for `require_admin_permission()` |
| `AdminSessionContext` | `core/deps.py` | Extend with resolved permission set |
| `BaseRepository[ModelT]` | `common/base_repository.py` | `RoleRepository`, `RolePermissionRepository` |
| `get_redis_pool()` | `infrastructure/redis.py` | Cache resolved permission matrix per session |
| `AuthorizationError` | `core/exceptions.py` | 403 on permission denial |

## 8. Files to Create
- `src/noorheroes/modules/admin/rbac/models.py` — `RoleOrm`, `RolePermissionOrm`, `AdminRoleAssignmentOrm`
- `src/noorheroes/modules/admin/rbac/schemas.py` — `RoleResponse`, `PermissionResponse`, `RoleListResponse`
- `src/noorheroes/modules/admin/rbac/repository.py` — `RoleRepository`, `RolePermissionRepository`
- `src/noorheroes/modules/admin/rbac/service.py` — `RbacService`
- `src/noorheroes/modules/admin/rbac/api.py` — `GET /v1/admin/roles`, `POST /v1/admin/roles` (Super Admin role creation)
- `alembic/versions/xxxx_create_rbac_tables.py`
- `alembic/versions/xxxx_seed_canonical_roles.py` (data migration seeding FR-4's nine roles)
- `tests/modules/admin/rbac/test_rbac_engine.py`
- `tests/modules/admin/rbac/test_service_layer_authorization_boundary.py`

## 9. Files to Modify
- `src/noorheroes/core/deps.py` — add `require_admin_permission(resource: str, action: str)` dependency factory; extend `AdminSessionContext` with `role_id`/resolved scope
- `src/noorheroes/modules/admin/service.py` — remove/deprecate ad-hoc flat-scope checks in favor of `RbacService`

## 10. Backend Requirements
- **Models (§4.1/§4.2 of PRD):**
  - `role(role_id PK, name, requires_2fa)`
  - `role_permission(role_id FK, permission_key, resource_scope, region, locale)` — composite key reflecting the multi-dimensional model, index `(role_id, resource_scope)`
  - `admin_role_assignment(admin_id FK, role_id FK, assigned_at)`
- **Seed data:** the nine canonical roles from FR-4, each with `requires_2fa=true` except possibly the most basic tier (per PRD §3.4 wording "for a role below moderator tier" — the PRD does not name a role below moderator tier among the nine listed, so seed all nine as `requires_2fa=true` unless/until a specific non-moderator role is defined elsewhere; do not invent a tenth role).
- **`GET /v1/admin/roles`:** `super_admin`-only, lists roles + their permission grants.
- **`require_admin_permission(resource, action)`:** resolves `admin_id` → role(s) → matches against `role_permission` rows scoped by `resource_scope`/region/locale relevant to the request context → raises `AuthorizationError` (403) if no matching grant.
- **Service-layer enforcement (FR-6 alignment, Edge Case 6):** this check must be invoked inside each module's own service/router dependency chain, never assumed satisfied by gateway-level or UI-level filtering.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
Consumed by `N-02 — Role-Scoped Navigation Shell` (nav visibility) and `N-04 — Role & Permission Matrix Management` (editor UI, read path only — writes go through B-04's maker-checker).

## 13. API Contract
### `GET /v1/admin/roles`
- **Auth:** `super_admin` (via `require_admin_permission("roles", "read")`)
- **Response 200:**
```json
{
  "roles": [
    { "role_id": "role_01H...", "name": "Content Editor", "requires_2fa": true,
      "permissions": [ { "permission_key": "content:write", "resource_scope": "content", "region": "*", "locale": "*" } ] }
  ]
}
```
- **Error Responses:** `401 UNAUTHENTICATED`, `403 FORBIDDEN`

### `POST /v1/admin/roles`
- **Auth:** `super_admin` only (via `require_admin_role("super_admin")`)
- **Summary:** Creates a new administrative role with fine-grained multi-dimensional permissions.
- **Request Body (201):**
```json
{
  "role_key": "curriculum_lead",
  "name": "Curriculum Lead",
  "description": "Oversees educational pathways",
  "requires_2fa": true,
  "permissions": [
    {
      "permission_key": "content:publish",
      "resource_scope": "*",
      "region": "*",
      "locale": "*"
    }
  ]
}
```
- **Response 201:** Created `RoleDto` with assigned permissions.
- **Audit:** Records immutable administrative audit trail event (`ROLE_CREATED`).
- **Error Responses:** `401 UNAUTHENTICATED`, `403 FORBIDDEN` (non-super-admin), `409 CONFLICT` (duplicate `role_key`), `422 UNPROCESSABLE_ENTITY` (invalid slug format).

Note: `PATCH /v1/admin/roles/{id}/permissions` is specified in the PRD but its actual persistence behavior (creating a `change_proposal`, self-elevation rejection) belongs to B-04 — B-03 exposes the read/query surface and the underlying `role_permission` write method that B-04's approval-application step calls internally; B-03 does **not** expose a direct public PATCH endpoint itself, since PRD §3.4 explicitly states PATCH here "creates a `change_proposals` row rather than applying immediately."


## 14. Database Requirements
- `role_permission` composite key per §4.2; index `(role_id, resource_scope)`.
- Seed migration inserts exactly the nine FR-4 roles — no additional roles invented.
- No FK from `admin_role_assignment`/`role` to `identity` tables (maintains B-01's isolation guarantee).

## 15. Validation
- `permission_key`/`resource_scope`/`region`/`locale` combinations validated against an allow-listed set of known resource scopes (defined as each E.29–E.34 module comes online; B-03 ships the mechanism plus whatever resource scopes E.28 itself needs — `roles`, `audit-logs`, `feature-flags`, `config`, `dashboard`, `admin-users`).
- Reject unknown `role_id` on assignment.

## 16. Authentication
Delegated to B-01/B-02 (`get_current_admin`); this module assumes a valid `AdminSessionContext` is already present.

## 17. Authorization
This module **is** the authorization engine. `require_admin_permission()` is the canonical dependency every Admin route (including this module's own) must use going forward instead of the flat `require_admin_scope()`.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Unauthenticated request | `401` |
| Authenticated but role lacks permission | `403 FORBIDDEN` — identical whether triggered via UI-hidden action or direct API call bypassing UI (Edge Case 6) |
| Unknown `role_id` | `404 ROLE_NOT_FOUND` |
| Malformed resource_scope/region/locale query | `422` |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
`role.name` values are stable identifiers; display-name translation (if the Admin UI wants localized role labels) happens client-side via the `localization` context's existing translation dictionary pattern — do not hardcode translated role names in this table.

## 22. RTL
N/A at backend layer.

## 23. Analytics
N/A directly (role list is a read view; `role_change_proposed` analytics event belongs to B-04's proposal creation, not this read-only module).

## 24. Performance
- Cache resolved per-admin permission set in Redis (keyed by `admin_id`, short TTL or explicit invalidation on role-assignment change) to avoid a multi-table join on every authorized request.
- Index `(role_id, resource_scope)` supports the primary lookup pattern.
- N+1 avoidance: `GET /v1/admin/roles` eager-loads permissions in a single query (`selectinload`), not per-role round trips.

## 25. Security
- **Service-layer-is-the-real-boundary guarantee (primary):** `require_admin_permission()` must be applied inside route dependency chains, never trusted to be redundant with UI hiding. Verified by the direct-API-bypass test (Task 06).
- Only `super_admin` may read the full role/permission matrix.
- Permission cache invalidated immediately on any role-assignment or role-permission change (freshness matters for a security control — stale-cache privilege retention is a real risk).

## 26. Library Requirements
No new libraries — SQLAlchemy 2.0 async, existing Redis client.

## 27. Testing
- Unit: `RbacService` permission resolution across multiple role/resource/region/locale combinations.
- Unit: cache invalidation on role change.
- Integration: `GET /v1/admin/roles` (success, 401, 403).
- **Signature test:** direct API call to a permission-restricted resource, bypassing the UI, is rejected identically to how the UI would have prevented it (Edge Case 6).

## 28. Documentation
OpenAPI schema for `GET /v1/admin/roles`; internal doc describing the multi-dimensional authorization model and how downstream modules (E.29+) should integrate `require_admin_permission()`.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create RBAC Models**
- Task ID: B-03-T01
- Objective: `role`, `role_permission`, `admin_role_assignment` tables per §4.1 ER diagram.
- Files to Create: `modules/admin/rbac/models.py`.
- Implementation Details: As specified in §10 Backend Requirements.
- Security: No FK to `identity` tables.
- Tests: Model smoke test.
- Dependencies: B-01 Task 01 (for `admin_user` FK target).
- Definition of Done: Models compile, Alembic autogenerate correct.

**Task 02 — Migration + Canonical Role Seed Data**
- Task ID: B-03-T02
- Objective: Create tables and seed the nine FR-4 roles.
- Files to Create: two migration files (schema + data seed).
- Business Rules: Exactly the nine named roles, no invented roles.
- Tests: Migration up/down; seed-data assertion test (nine rows, correct names).
- Dependencies: Task 01.
- Definition of Done: Fresh DB migrate produces exactly the nine canonical roles.

**Task 03 — Implement `RoleRepository` / `RolePermissionRepository`**
- Task ID: B-03-T03
- Objective: Data access for roles/permissions.
- Files to Create: `modules/admin/rbac/repository.py`.
- Implementation Details: `list_roles_with_permissions()` using `selectinload` to avoid N+1.
- Performance: Single-query eager load.
- Tests: Repository unit tests.
- Dependencies: Task 01, Task 02.
- Definition of Done: Query returns roles with nested permissions in one round trip.

**Task 04 — Implement `RbacService` & Permission Resolution**
- Task ID: B-03-T04
- Objective: Core multi-dimensional authorization logic.
- Files to Create: `modules/admin/rbac/service.py`.
- Implementation Details: `resolve_permissions(admin_id) -> PermissionSet`; `has_permission(permission_set, resource, action, region=None, locale=None) -> bool`.
- Business Rules: FR-5 — role + resource_scope + region + locale + action, not flat lookup.
- Performance: Redis-cache the resolved `PermissionSet` per `admin_id`.
- Tests: Multiple role/resource/region/locale combination unit tests.
- Dependencies: Task 03.
- Definition of Done: Resolution logic covers all combination edge cases in tests.

**Task 05 — Implement `require_admin_permission()` Dependency**
- Task ID: B-03-T05
- Objective: FastAPI dependency factory replacing/extending `require_admin_scope()`.
- Files to Modify: `core/deps.py`.
- Implementation Details: `def require_admin_permission(resource: str, action: str)` returns a dependency raising `AuthorizationError` on denial.
- Security: This is the actual enforcement point — must be usable by every future Admin route.
- Tests: Dependency unit test with mocked `RbacService`.
- Dependencies: Task 04.
- Definition of Done: Dependency importable and usable via `Depends(require_admin_permission("roles", "read"))`.

**Task 06 — Direct API-Bypass Security Test (Signature Test)**
- Task ID: B-03-T06
- Objective: Prove the service layer, not the UI, is the real boundary.
- Files to Create: `tests/modules/admin/rbac/test_service_layer_authorization_boundary.py`.
- Implementation Details: Call a permission-gated endpoint directly with a token for a role lacking the permission, bypassing any UI; assert `403`.
- Dependencies: Task 05.
- Definition of Done: Test passes; documented as the canonical pattern for all future Admin modules to replicate.

**Task 07 — Implement `GET /v1/admin/roles`**
- Task ID: B-03-T07
- Objective: Expose the role/permission read API.
- Files to Create: `modules/admin/rbac/api.py`.
- Implementation Details: Per §13 API contract.
- Dependencies: Task 03, Task 05.
- Definition of Done: Integration test passes for success/401/403.

**Task 08 — Full Test Suite + Documentation**
- Task ID: B-03-T08
- Files to Create: `tests/modules/admin/rbac/test_rbac_engine.py`.
- Dependencies: Tasks 01–07.
- Definition of Done: All §27 scenarios green; OpenAPI updated.

**Task 09 — Implement `POST /v1/admin/roles` (Super Admin Role Creation)**
- Task ID: B-03-T09
- Objective: Expose Super Admin role provisioning endpoint with composite permission assignment and immutable audit logging.
- Files to Modify:
  - `src/noorheroes/modules/admin/rbac/schemas.py` (`CreateRolePermissionRequest`, `CreateRoleRequest`)
  - `src/noorheroes/modules/admin/rbac/repository.py` (`create_role` with conflict detection)
  - `src/noorheroes/modules/admin/rbac/service.py` (`create_role` with `AdminRepository.log_action` audit)
  - `src/noorheroes/modules/admin/rbac/api.py` (`POST /v1/admin/roles` endpoint)
  - `src/noorheroes/modules/admin/deps.py` (inject `AdminRepository` into `RbacService`)
  - `tests/modules/admin/rbac/test_rbac_api.py` (integration tests)
- Implementation Details:
  - Validates snake_case slug format (`^[a-z0-9_]+$`, 2–50 chars).
  - Enforces `ConflictError` (HTTP 409) if `role_key` already exists.
  - Persists `RoleOrm` and multi-dimensional `RolePermissionOrm` rows.
  - Records an immutable `ROLE_CREATED` audit log entry.
- Security: Strictly gated via `require_admin_role("super_admin")`.
- Definition of Done: `POST /v1/admin/roles` returns 201 Created with `RoleDto`; 401 on unauthenticated, 403 on non-super-admin, 409 on duplicate slug, 422 on invalid slug. Tests pass 100%.

## 30. Definition of Done
- Nine canonical roles seeded exactly as FR-4 specifies.
- Multi-dimensional permission resolution working and cached.
- `require_admin_permission()` available as the standard dependency for all Admin routes.
- Direct-API-bypass test proves service-layer enforcement (Edge Case 6).
- `GET /v1/admin/roles` live, `super_admin`-gated.
- `POST /v1/admin/roles` live, `super_admin`-gated for provisioning new custom roles with audit logging.

## 31. Final Verification Checklist
- [ ] Exactly nine roles seeded, matching FR-4 names precisely
- [ ] `role_permission` composite key and index present
- [ ] Permission resolution covers role + resource_scope + region + locale + action
- [ ] Direct-API-bypass test (Edge Case 6) passes
- [ ] Redis permission cache invalidated on role-assignment/permission change
- [ ] `GET /v1/admin/roles` gated to `super_admin` only
- [ ] `POST /v1/admin/roles` gated to `super_admin` only with audit log emission
- [ ] Duplicate `role_key` creation rejected with 409 Conflict
- [ ] No FK/shared table with `identity` context
- [ ] OpenAPI docs updated

