# B-09 — Admin User & Role Administration

## 1. Feature Context
Part of E.28. Admin user lifecycle management (list, detail, deactivation, role assignment) — the Role List and Admin User Deactivation screens (§1.18 #13, #20) not otherwise covered by B-01 (login) or B-03 (role/permission matrix itself).

## 2. Parent Feature
E.28 — Admin Portal: Authentication, RBAC & Operations Dashboard

## 3. Sub-feature
B-09 — Admin User & Role Administration

## 4. Objective
Implement admin user list/detail/deactivation and role-assignment endpoints, using soft deactivation (never hard delete) to preserve historical audit-actor references (PRD §4.4).

## 5. Business Requirements
- §1.18 Screen #20: Admin User Deactivation (component, within Role/User management).
- §4.4: `admin_user.active = false` used for deactivation rather than deletion, preserving historical audit-actor references.
- Implicit requirement: super admins manage which admins hold which roles (supports FR-3's maker-checker for role changes, via B-04).

## 6. Existing Architecture
Depends on B-01 (`admin_user` model), B-03 (`admin_role_assignment`), B-04 (role-change proposals — role *re-assignment* on an existing admin routes through the same maker-checker mechanism as B-03's permission changes, since it is equally a role-related mutation), B-05 (audit writes on deactivation).

## 7. Existing Code to Reuse
| Component | Location | Reuse For |
|---|---|---|
| `AdminUserRepository` | B-01, `modules/admin/repository.py` | Extend with list/deactivate methods |
| `AdminRoleAssignmentOrm` | B-03 | Role assignment records |
| `AuditLogService.log_action()` | B-05 | Deactivation audit writes |
| `BaseRepository.list_paginated()` | `common/base_repository.py` | Paginated admin user list |

## 8. Files to Create
- `src/noorheroes/modules/admin/users/schemas.py` — `AdminUserListResponse`, `AdminUserDetailResponse`, `DeactivateAdminUserRequest`
- `src/noorheroes/modules/admin/users/service.py` — `AdminUserManagementService`
- `src/noorheroes/modules/admin/users/api.py` — list/detail/deactivate endpoints
- `tests/modules/admin/users/test_admin_user_management.py`

## 9. Files to Modify
- `src/noorheroes/modules/admin/repository.py` (B-01's `AdminUserRepository`) — add `list_paginated()`, `deactivate()`

## 10. Backend Requirements
- **`GET /v1/admin/users`:** paginated, filterable by role/status.
- **`GET /v1/admin/users/{id}`:** detail including current role assignment(s).
- **`POST /v1/admin/users/{id}/deactivate`:** sets `active=false`; business rule — reject if this would leave zero active `super_admin` accounts (a platform-availability safety check, distinct from and in addition to RBAC's self-elevation rules); writes an audit entry.
- **Role reassignment:** exposed via B-03's role-assignment write path, itself routed through B-04's maker-checker (a role reassignment is a role-permission-adjacent change and should not bypass the same distinct-approver discipline FR-3 establishes for permission changes).

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
Consumed by `N-09 — Admin User Management & Deactivation`.

## 13. API Contract
### `GET /v1/admin/users?role=&status=&cursor=&limit=`
- **Auth:** `super_admin`
- **Response 200:** `{ "items": [ { "admin_id": "...", "email": "...", "role": "Content Editor", "active": true } ], "next_cursor": "...", "has_more": false }`

### `GET /v1/admin/users/{id}`
- **Response 200:** full detail including role assignment history

### `POST /v1/admin/users/{id}/deactivate`
- **Request:** `{ "reason": "string" }`
- **Response 200:** `{ "admin_id": "...", "active": false }`
- **Error Responses:** `409 LAST_SUPER_ADMIN_CANNOT_DEACTIVATE`, `404 ADMIN_USER_NOT_FOUND`

## 14. Database Requirements
No hard delete anywhere in this module — `active=false` only, per §4.4.

## 15. Validation
`reason` required on deactivation (audit trail quality); pagination/filter params validated.

## 16. Authentication
Delegated to B-01/B-02.

## 17. Authorization
`super_admin` for list/detail/deactivate (via B-03's `require_admin_permission("admin-users", ...)`).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Deactivating the last active super admin | `409 LAST_SUPER_ADMIN_CANNOT_DEACTIVATE` — platform-availability safety rule |
| Unknown admin_id | `404 ADMIN_USER_NOT_FOUND` |
| Deactivating an admin with pending maker-checker proposals as proposer | Proposals remain queryable, referencing the now-inactive actor (no cascading deletion) |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Role display names localized client-side.

## 22. RTL
N/A.

## 23. Analytics
Supports `admin_user_deactivated` (client-fired).

## 24. Performance
Cursor-based pagination on the user list, consistent with `BaseRepository.list_paginated()`.

## 25. Security
Deactivation is audited (B-05); the last-super-admin-protection rule prevents an accidental or malicious total lockout of platform administration capability.

## 26. Library Requirements
No new libraries.

## 27. Testing
- Unit: deactivation service logic including last-super-admin guard.
- Integration: list/detail/deactivate full flow.
- Edge case: deactivating an admin who has pending proposals as proposer — proposals remain intact and queryable.

## 28. Documentation
OpenAPI schema for all three endpoints.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Extend `AdminUserRepository` with List/Deactivate**
- Task ID: B-09-T01
- Files to Modify: `modules/admin/repository.py`.
- Implementation Details: `list_paginated(filters)`, `deactivate(admin_id)`.
- Dependencies: B-01 Task 03.
- Definition of Done: Methods unit-tested.

**Task 02 — Implement `AdminUserManagementService`**
- Task ID: B-09-T02
- Files to Create: `users/service.py`.
- Implementation Details: `list_users()`, `get_user_detail()`, `deactivate_user()` including the last-super-admin guard (count active super admins via B-03's role-assignment data before permitting deactivation of one).
- Dependencies: Task 01, B-03 Task 03.
- Definition of Done: Guard logic tested against a single-super-admin fixture scenario.

**Task 03 — Wire Audit Write on Deactivation**
- Task ID: B-09-T03
- Implementation Details: Call `AuditLogService.log_action()` on successful deactivation.
- Dependencies: Task 02, B-05 Task 02.
- Definition of Done: Deactivation produces a corresponding audit entry.

**Task 04 — Implement List/Detail/Deactivate Endpoints**
- Task ID: B-09-T04
- Files to Create: `users/api.py`.
- Dependencies: Tasks 01–03, B-03 Task 05.
- Definition of Done: Integration tests pass.

**Task 05 — Full Test Suite + Documentation**
- Task ID: B-09-T05
- Dependencies: Tasks 01–04.
- Definition of Done: All §27 scenarios green; OpenAPI updated.

## 30. Definition of Done
- Admin user list/detail/deactivation live, `super_admin`-gated.
- Deactivation soft (never hard delete), audited, and blocked if it would remove the last active super admin.

## 31. Final Verification Checklist
- [ ] Deactivation never hard-deletes a row
- [ ] Last-super-admin protection verified
- [ ] Deactivation produces an audit log entry
- [ ] Pending proposals referencing a deactivated admin remain queryable
- [ ] Pagination/filtering functional on the user list
- [ ] OpenAPI docs updated
