# B-07 — Operator Account Provisioning & Role Management API

## 1. Feature Context
The API that creates and manages the internal operator accounts (moderator/admin/scholar) themselves — role assignment is validated against E.28's live role registry so no operator can ever be assigned a role that doesn't actually exist, and disabling an account never cascades a delete that would sever attribution on past reviews/audit rows.

## 2. Parent Feature
E.32 — User Management & Child Safety View

## 3. Sub-feature
1.7 Operator Account Provisioning & Role Management API (ID: **B-07**)

## 4. Objective
Build create/list/detail/role-reassignment/disable/re-enable endpoints for operator accounts, validating every role assignment against E.28's live role registry and enforcing disable-never-cascade-delete.

## 5. Business Requirements
- Create a new moderator/admin/scholar operator account with an initial role.
- Reassign an operator's role at any time, validated against the currently live set of roles (E.28) — an unknown/retired role name is rejected.
- Disable an operator account: sets `active=false`, revokes active sessions, but never deletes the row or cascades a delete to content this operator has authored, reviewed, or is referenced by in any audit log.
- Re-enable restores the account to its prior role and active state.

## 6. Existing Architecture
`admin` bounded context (operator accounts are administrative identities, distinct from `identity`'s parent/child accounts), `app/admin/routers/operator_account_router.py`, validating against E.28's `app/admin/services/role_registry_service.py::RoleRegistryService.list_active_roles()`.

## 7. Existing Code to Reuse
- E.28: `RoleRegistryService.list_active_roles()` — the live role source of truth
- E.28: `AuditLogService.log_action()`
- C.21's disable-never-cascade-delete pattern (the exact mechanics reused for parent/child account disable, applied here to operator accounts)
- C.19's `SessionService.revoke_all_sessions()` (called on disable)

## 8. Files to Create
- `app/admin/routers/operator_account_router.py`
- `app/admin/services/operator_account_service.py`
- `app/admin/repositories/operator_account_repository.py`
- `app/admin/schemas/operator_account_schema.py`

## 9. Files to Modify
- `app/admin/routers/__init__.py` — register router

## 10. Backend Requirements
- `OperatorAccountService.create()`: validates initial role against `RoleRegistryService.list_active_roles()`, rejects unknown roles with `422`.
- `OperatorAccountService.reassign_role()`: same live-registry validation on every reassignment, not just creation.
- `OperatorAccountService.disable()`: sets `active=false`, calls `SessionService.revoke_all_sessions()`, does NOT delete the row, does NOT cascade-delete any `content_version.last_edited_by`, `review_decision.approved_by`, or `audit_log.actor_id` reference — foreign keys pointing to this operator remain intact (mirrors C.21's exact disable semantics).
- `OperatorAccountService.re_enable()`: restores `active=true` at the prior role (role itself re-validated against the live registry at re-enable time, in case it was retired while disabled — reject re-enable with the old role if so, requiring an explicit new-role reassignment instead).

## 11. Required API / API Contract
`POST /v1/admin/operators` `{name, email, initial_role}` → `201`.
`GET /v1/admin/operators` → list.
`GET /v1/admin/operators/{id}` → detail.
`PATCH /v1/admin/operators/{id}/role` `{new_role}` → `200` or `422 UNKNOWN_ROLE`.
`PATCH /v1/admin/operators/{id}/disable` → `200`.
`PATCH /v1/admin/operators/{id}/re-enable` → `200` or `409 ROLE_NO_LONGER_ACTIVE`.

## 12. Database Requirements
`operator_account` table (assumed to exist from E.28 or created here if not — confirm against E.28's schema; if E.28 already owns this table, this sub-feature adds only the disable/re-enable columns/logic, not a duplicate table). No cascade-delete foreign keys from `content_version`/`review_decision`/`audit_log` to `operator_account.id` — `ON DELETE RESTRICT` or soft-delete-only pattern, matching C.21.

## 13. Validation
`initial_role`/`new_role` validated against `RoleRegistryService.list_active_roles()` on every write, never a cached/stale role list.

## 14. Authentication
`get_current_admin`.

## 15. Authorization
`require_admin_scope("admin")` — operator provisioning/role management is an elevated action, above the baseline `support` scope used elsewhere in this feature.

## 16. Error Handling
`422 UNKNOWN_ROLE` for an invalid/retired role on create or reassignment; `409 ROLE_NO_LONGER_ACTIVE` if re-enabling an account whose prior role was retired while disabled; `404` for unknown operator.

## 17. Security
Role validation against the live registry (never a hardcoded or cached enum) is this sub-feature's core guarantee — mandatory test using a freshly-retired role confirms it can no longer be assigned. Disable-never-cascade-delete is the second core guarantee — mandatory test confirms a disabled operator's historical `content_version`/`review_decision`/`audit_log` foreign-key references remain intact and queryable after disable.

## 18. Analytics
Log operator account lifecycle events (create/role-change/disable/re-enable) for security/compliance oversight reporting.

## 19. Performance
Indexed lookups on `operator_account.id`, `active` status.

## 20. Library Requirements
FastAPI, Pydantic v2, SQLAlchemy 2.0 async, Alembic (if new columns/table needed). No new libraries.

## 21. Testing
Unit: role-validation-against-live-registry logic, disable-never-delete logic. Integration: **mandatory** — attempt to assign a retired role, confirm rejection; **mandatory** — disable an operator with existing authored content/reviews/audit rows, confirm those foreign-key references remain intact and unmodified after disable; full create→reassign→disable→re-enable lifecycle flow.

## 22. Documentation
OpenAPI docstrings; note that role validation always queries the live registry, never a cached value.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Confirm/Extend `operator_account` Schema**
Objective: Verify table ownership against E.28; add disable/re-enable columns if missing via migration. Files: `alembic/versions/xxxx_extend_operator_account.py` (if needed). Tests: migration test. Definition of Done: schema confirmed/extended.

**Task 02 — Define Schemas**
Objective: `OperatorAccountCreate`, `OperatorAccountDetail`, `RoleReassignment`. Files: `schemas/operator_account_schema.py`. Dependencies: Task 01. Tests: validation tests. Definition of Done: tests pass.

**Task 03 — Implement `OperatorAccountRepository`**
Objective: CRUD + disable/re-enable persistence, no cascade-delete logic anywhere. Files: `repositories/operator_account_repository.py`. Dependencies: Task 01. Tests: repository tests. Definition of Done: tests pass.

**Task 04 — Implement `OperatorAccountService` with Live Role-Registry Validation**
Objective: Create/reassign/disable/re-enable, validating every role write against `RoleRegistryService.list_active_roles()`. Files: `services/operator_account_service.py`. Dependencies: Task 03, E.28. Tests: **mandatory** — retired-role-rejected test. Definition of Done: test passes.

**Task 05 — Implement Router Endpoints**
Objective: Wire all six endpoints, `admin`-scope-gated. Files: `routers/operator_account_router.py`. Dependencies: Task 04. Tests: endpoint integration tests. Definition of Done: tests pass.

**Task 06 — Verify Disable-Never-Cascade-Delete**
Objective: **Mandatory** integration test with a fixture operator having existing authored/reviewed rows, confirming those references survive disable intact. Dependencies: Task 05. Definition of Done: test passes.

**Task 07 — Wire Audit Logging**
Objective: Log every lifecycle event. Dependencies: Task 05. Tests: audit-entry test per event type. Definition of Done: test passes.

**Task 08 — Add Full Test Suite**
Objective: Complete coverage per §21, both mandatory tests included. Definition of Done: all green in CI.

**Task 09 — Final Code Review**
Objective: Confirm zero cascade-delete foreign key exists from any content/review/audit table to `operator_account.id`. Definition of Done: checklist in §24 checked.

## 24. Final Verification Checklist
- [ ] Role validation always queries E.28's live registry — mandatory retired-role-rejected test passing
- [ ] Disable never cascades a delete — mandatory foreign-key-integrity test passing
- [ ] Disable revokes all active sessions via C.19
- [ ] Re-enable re-validates the prior role against the live registry
- [ ] `admin` scope enforced (elevated above baseline `support`)

## 25. Definition of Done
Operator accounts are provisioned and role-managed with every role write validated against the live registry, and disabling an operator never severs attribution on their historical work — mirroring C.21's proven disable semantics.
