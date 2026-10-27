# B-08 — Support Case Queue API

## 1. Feature Context
The case-tracking backbone tying together support interactions that don't fit neatly into a single other endpoint — including the child-deletion and parent-deletion-cancellation case types that cross-reference C.21's support-mediated cancellation flow.

## 2. Parent Feature
E.32 — User Management & Child Safety View

## 3. Sub-feature
1.8 Support Case Queue API (ID: **B-08**)

## 4. Objective
Build case list/detail/create/resolve endpoints with a typed `case_type` including deletion-related types, and an optional link to a triggering admin action (e.g., an `unmask_request.id` or a C.21 deletion-cancellation record).

## 5. Business Requirements
- Support cases are queued, filterable by type/status, and resolvable.
- Case types include (at minimum): general inquiry, child-deletion request, parent-deletion-cancellation request — the latter two cross-referencing C.21's existing deletion/cancellation mechanics rather than reimplementing them.
- A case may optionally link to a related admin action for traceability (e.g., "this case led to this unmask request").

## 6. Existing Architecture
`admin` bounded context, `app/admin/routers/support_case_router.py`, cross-referencing C.21's `app/identity/services/account_deletion_service.py` for deletion-related case types (read/link only, not owned here).

## 7. Existing Code to Reuse
- C.21: `AccountDeletionService` (referenced by ID for deletion-related cases, not duplicated)
- E.28's `AuditLogService.log_action()`

## 8. Files to Create
- `app/admin/routers/support_case_router.py`
- `app/admin/services/support_case_service.py`
- `app/admin/repositories/support_case_repository.py`
- `app/admin/schemas/support_case_schema.py`
- `alembic/versions/xxxx_create_support_case_table.py`

## 9. Files to Modify
- `app/admin/routers/__init__.py` — register router

## 10. Backend Requirements
- `SupportCaseService.create()`: creates a case with `case_type`, optional `related_parent_id`/`related_child_id`, optional `linked_action_type`/`linked_action_id` (e.g., pointing at an `unmask_request.id`).
- For `case_type='child_deletion'` or `'parent_deletion_cancellation'`, the service does not itself perform the deletion/cancellation — it links to and reads status from C.21's existing service, keeping deletion logic single-sourced.
- `SupportCaseService.resolve()`: sets `status='resolved'` with a resolution note.

## 11. Required API / API Contract
`POST /v1/admin/support-cases` `{case_type, related_parent_id?, related_child_id?, notes}` → `201`.
`GET /v1/admin/support-cases?status=&case_type=` → list.
`GET /v1/admin/support-cases/{id}` → detail (including linked-action summary if present).
`PATCH /v1/admin/support-cases/{id}/resolve` `{resolution_note}` → `200`.

## 12. Database Requirements
`support_case(id, case_type, related_parent_id, related_child_id, linked_action_type, linked_action_id, status, notes, resolution_note, created_by, created_at, resolved_at)`. Indexed on `status`, `case_type`, `related_parent_id`.

## 13. Validation
`case_type` enum-validated; `linked_action_type` (if present) restricted to a known set (`unmask_request`, `account_deletion`, etc.) with existence-checked `linked_action_id`.

## 14. Authentication
`get_current_admin`.

## 15. Authorization
`require_admin_scope("support")` for create/list/detail; `require_admin_scope("support")` for resolve (any support+ operator may resolve, matching this feature's general support-scope baseline).

## 16. Error Handling
`422` for invalid `case_type`/`linked_action_type`; `404` for unknown case or unresolvable linked-action reference.

## 17. Security
Deletion-related case types read from, and link to, C.21's existing deletion/cancellation service rather than re-implementing deletion mechanics — avoids a second, potentially inconsistent deletion code path.

## 18. Analytics
Case volume by type/status, resolution-time metrics for support-tooling oversight reporting.

## 19. Performance
Indexed queue queries; standard pagination via `usePaginationState`-equivalent backend pattern (offset/limit or cursor, matching existing admin list endpoint conventions).

## 20. Library Requirements
FastAPI, Pydantic v2, SQLAlchemy 2.0 async, Alembic. No new libraries.

## 21. Testing
Unit: `case_type`/`linked_action_type` validation. Integration: full create→list→resolve flow; deletion-related case correctly links to and reflects C.21's status without duplicating its logic; audit log entry per create/resolve.

## 22. Documentation
OpenAPI docstrings describing the `case_type` enum and the linked-action cross-reference pattern.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Write Migration for `support_case`**
Objective: Table with indexes on `status`, `case_type`, `related_parent_id`. Files: `alembic/versions/xxxx_create_support_case_table.py`. Tests: migration up/down test. Definition of Done: schema created.

**Task 02 — Define Schemas**
Objective: `SupportCaseCreate`, `SupportCaseDetail`, `SupportCaseResolve`. Files: `schemas/support_case_schema.py`. Dependencies: Task 01. Tests: validation tests. Definition of Done: tests pass.

**Task 03 — Implement `SupportCaseRepository`**
Objective: CRUD + filtered list queries. Files: `repositories/support_case_repository.py`. Dependencies: Task 01. Tests: repository tests. Definition of Done: tests pass.

**Task 04 — Implement `SupportCaseService`**
Objective: Create/resolve logic, linked-action cross-referencing to C.21 for deletion-related types. Files: `services/support_case_service.py`. Dependencies: Task 03, C.21. Tests: linked-action-reference tests. Definition of Done: tests pass.

**Task 05 — Implement Router Endpoints**
Objective: Wire all four endpoints. Files: `routers/support_case_router.py`. Dependencies: Task 04. Tests: endpoint integration tests. Definition of Done: tests pass.

**Task 06 — Wire Audit Logging**
Objective: Log create/resolve actions. Dependencies: Task 05. Tests: audit-entry test. Definition of Done: test passes.

**Task 07 — Add Full Test Suite**
Objective: Complete coverage per §21. Definition of Done: all green in CI.

**Task 08 — Final Code Review**
Objective: Confirm deletion-related case types never duplicate C.21's deletion logic. Definition of Done: checklist in §24 checked.

## 24. Final Verification Checklist
- [ ] `case_type` enum enforced, including deletion-related types
- [ ] Deletion-related cases link to, never duplicate, C.21's deletion/cancellation logic
- [ ] Resolve requires a resolution note
- [ ] Every create/resolve action is audit-logged
- [ ] `support`+ scope enforced

## 25. Definition of Done
Support cases — including deletion-related ones correctly cross-referencing C.21 — are queued, tracked, and resolvable through a single, consistent case API.
