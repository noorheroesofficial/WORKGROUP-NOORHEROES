# B-03 — Unmask Request & Approval Workflow (Maker-Checker)

## 1. Feature Context
The maker-checker gate standing between "masked by default" and "temporarily unmasked" — a distinct requester and a distinct, second approver, enforced at both the application layer and the database layer, exactly mirroring E.28's and E.29's proven self-approval-prevention pattern, per the PRD's explicit instruction to reuse rather than reinvent it.

## 2. Parent Feature
E.32 — User Management & Child Safety View

## 3. Sub-feature
1.3 Unmask Request & Approval Workflow (ID: **B-03**)

## 4. Objective
Build `unmask_request`/`unmask_grant`/`unmask_grant_approval` tables and the submit/approve/reject endpoints, with a dual-layer (application check + DB `CHECK`) guarantee that `approved_by != requested_by`, and time-boxed grant creation on approval.

## 5. Business Requirements
- Any `support`+ operator may submit an unmask request with a required justification and explicit scope (`parent_id` or `child_id`).
- Approval requires a second, distinct admin — the requester may never approve their own request.
- Approval creates a time-boxed `unmask_grant` (fixed TTL, e.g., 15 minutes, configurable).
- Rejection leaves the record masked with no grant created.
- No auto-approval on timeout — a stale-pending request is flagged for visibility, never silently approved.

## 6. Existing Architecture
`identity` bounded context, `app/identity/routers/unmask_workflow_router.py`, reusing E.28's self-approval-prevention pattern verbatim (application check mirrored from `app/admin/services/role_assignment_service.py`'s pattern, DB `CHECK` mirrored from the migration that added it there).

## 7. Existing Code to Reuse
- `app/shared/base_service.py::BaseService`, `app/shared/base_repository.py::BaseRepository`
- E.28's self-approval-prevention application-layer check (exact logic reused, not reimplemented)
- E.28's `AuditLogService.log_action()`
- E.29 B-03's dual-layer segregation-of-duties DB `CHECK` migration as the direct template for this table's constraint

## 8. Files to Create
- `app/identity/routers/unmask_workflow_router.py`
- `app/identity/services/unmask_workflow_service.py`
- `app/identity/repositories/unmask_request_repository.py`, `unmask_grant_repository.py` (write methods; B-02 owns a read-only variant)
- `app/identity/schemas/unmask_request_schema.py`
- `alembic/versions/xxxx_create_unmask_request_grant_tables.py`

## 9. Files to Modify
- `app/identity/routers/__init__.py` — register router

## 10. Backend Requirements
- `UnmaskWorkflowService.submit_request()`: creates `unmask_request` row (`status='pending'`), requires non-empty justification and valid scope.
- `UnmaskWorkflowService.approve()`: application-layer check `if approval.approved_by == request.requested_by: raise SelfApprovalError` (reused verbatim from E.28's pattern) BEFORE the DB write is attempted, then creates `unmask_grant_approval` row and `unmask_grant` row with `expires_at = now() + UNMASK_GRANT_TTL`.
- `UnmaskWorkflowService.reject()`: sets `status='rejected'`, no grant created.
- Database `CHECK` constraint on `unmask_grant_approval`: `approved_by != requested_by` — enforced even if application logic is ever bypassed (defense-in-depth, exact same rationale as E.28/E.29).
- Stale-pending monitoring: a scheduled/queryable flag for requests pending beyond a threshold (e.g., 24h), surfaced to N-03's queue UI — never auto-approved.

## 11. Required API / API Contract
`POST /v1/admin/unmask-requests` `{scope_type, scope_id, justification}` → `201`.
`GET /v1/admin/unmask-requests?status=pending` → list.
`GET /v1/admin/unmask-requests/{id}` → detail.
`PATCH /v1/admin/unmask-requests/{id}/approve` → `200` (creates grant) or `409 SELF_APPROVAL_NOT_ALLOWED`.
`PATCH /v1/admin/unmask-requests/{id}/reject` `{reason}` → `200`.

## 12. Database Requirements
`unmask_request(id, requested_by, scope_type, scope_id, justification, status, created_at)`.
`unmask_grant_approval(id, unmask_request_id, requested_by, approved_by, decision, created_at)` with `CHECK (approved_by IS NULL OR approved_by != requested_by)`.
`unmask_grant(id, unmask_request_id, admin_id, scope_type, scope_id, expires_at, created_at)` — the row B-02 reads.
Migration mirrors E.29 B-03's migration structure exactly for the `CHECK` constraint syntax.

## 13. Validation
Justification: required, non-empty, minimum length (e.g., 10 chars) to discourage placeholder text. Scope: exactly one of `parent_id`/`child_id`, must reference an existing record.

## 14. Authentication
`get_current_admin`.

## 15. Authorization
`require_admin_scope("support")` for submit; `require_admin_scope("support")` for approve/reject (any `support`+ admin other than the requester may approve — no separate elevated "approver" role required unless the PRD specifies one, matching E.28's pattern of role-symmetric maker-checker).

## 16. Error Handling
`409 SELF_APPROVAL_NOT_ALLOWED` when `approved_by == requested_by` (application check) — this must never surface as a raw DB constraint-violation `500`, the service catches and maps it, though the DB `CHECK` remains as the defense-in-depth backstop. `404` for missing request. `409` for approving/rejecting an already-decided request.

## 17. Security
This table's `CHECK` constraint is the mandatory, non-negotiable defense-in-depth layer — required test: attempt a direct-repository-level approval bypass with `approved_by == requested_by` and confirm the database itself rejects it independent of the service-layer check.

## 18. Analytics
Track request→approval latency, approve/reject ratio, stale-pending counts (feeds N-03's queue and general Trust & Safety oversight reporting).

## 19. Performance
Indexed on `status`, `requested_by`, `expires_at` (grants) for queue and expiry-scan queries.

## 20. Library Requirements
FastAPI, Pydantic v2, SQLAlchemy 2.0 async, Alembic. No new libraries.

## 21. Testing
Unit: self-approval application check, justification/scope validation. Integration: **mandatory** — direct DB-level self-approval attempt rejected by `CHECK` constraint even bypassing the service layer; full submit→approve→grant-created flow; full submit→reject→no-grant flow; stale-pending flag correctly surfaces without auto-approving.

## 22. Documentation
OpenAPI docstrings; migration comment explaining the `CHECK` constraint's rationale, referencing E.28/E.29 as the established pattern.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Write Migration for the Three Tables**
Objective: `unmask_request`, `unmask_grant_approval` (with `CHECK`), `unmask_grant`. Files: `alembic/versions/xxxx_create_unmask_request_grant_tables.py`. Tests: migration up/down test. Definition of Done: `CHECK` constraint present, verified via direct SQL insert test.

**Task 02 — Define Schemas**
Objective: `UnmaskRequestCreate`, `UnmaskRequestDetail`, `UnmaskDecision`. Files: `schemas/unmask_request_schema.py`. Dependencies: Task 01. Tests: validation tests. Definition of Done: schema tests pass.

**Task 03 — Implement Repositories**
Objective: CRUD for request/approval/grant rows. Files: `repositories/unmask_request_repository.py`, `unmask_grant_repository.py`. Dependencies: Task 01. Tests: repository unit tests. Definition of Done: tests pass.

**Task 04 — Implement `UnmaskWorkflowService` with Self-Approval Check**
Objective: Submit/approve/reject logic, application-layer self-approval check reused verbatim from E.28. Files: `services/unmask_workflow_service.py`. Dependencies: Task 03. Tests: **mandatory** — self-approval rejected at application layer. Definition of Done: test passes.

**Task 05 — Implement Router Endpoints**
Objective: Wire all five endpoints with scope gating. Files: `routers/unmask_workflow_router.py`. Dependencies: Task 04. Tests: endpoint integration tests. Definition of Done: tests pass.

**Task 06 — Verify Database-Level Constraint Independently**
Objective: **Mandatory** test performing a raw repository-level insert bypassing the service layer, confirming the DB `CHECK` alone rejects `approved_by == requested_by`. Dependencies: Task 01. Definition of Done: test passes.

**Task 07 — Wire Audit Logging and Stale-Pending Flag**
Objective: Log every submit/approve/reject; add stale-pending query/flag logic. Dependencies: Task 05. Tests: audit + stale-flag tests. Definition of Done: tests pass.

**Task 08 — Add Full Test Suite**
Objective: Complete coverage per §21, both mandatory tests included. Definition of Done: all green in CI.

**Task 09 — Final Code Review**
Objective: Confirm the `CHECK` constraint syntax and rationale exactly mirror E.28/E.29's established pattern, not a divergent reimplementation. Definition of Done: checklist in §24 checked.

## 24. Final Verification Checklist
- [ ] `approved_by != requested_by` enforced at BOTH application layer and DB `CHECK` — both mandatory tests passing
- [ ] Approval creates a time-boxed `unmask_grant`, rejection creates none
- [ ] No auto-approval exists anywhere in the codebase for stale-pending requests
- [ ] Pattern verified as a verbatim reuse of E.28's self-approval-prevention approach, not a reinvention
- [ ] Every submit/approve/reject action is audit-logged

## 25. Definition of Done
Unmasking is gated by a provably dual-layer-enforced maker-checker workflow producing only time-boxed grants — the backend guarantee B-02's masking service depends on and N-03's UI surfaces.
