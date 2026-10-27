# B-06 — Account Recovery Initiation API

## 1. Feature Context
A support-initiated trigger into A.1/C.19's existing OTP-based recovery flow — this endpoint never issues, resets, or views a credential itself; it only starts the same recovery path a parent could trigger themselves.

## 2. Parent Feature
E.32 — User Management & Child Safety View

## 3. Sub-feature
1.6 Account Recovery Initiation API (ID: **B-06**)

## 4. Objective
Build `POST /v1/admin/users/{parent_id}/recovery/initiate`, delegating entirely to A.1/C.19's existing OTP-recovery service, with audit logging of the initiation event.

## 5. Business Requirements
- Support staff can initiate account recovery on a parent's behalf when the parent cannot self-serve (e.g., contacting support directly).
- Recovery always proceeds through the existing OTP mechanism — delivered to the parent's on-file, verified channel — never a direct password/credential reset performed by an admin.
- Initiation is audit-logged.

## 6. Existing Architecture
`identity` bounded context, thin delegation to A.1's `app/identity/services/recovery_service.py::RecoveryService.initiate_otp_recovery()`.

## 7. Existing Code to Reuse
- A.1/C.19: `RecoveryService.initiate_otp_recovery()` (used as-is, not reimplemented)
- E.28's `AuditLogService.log_action()`

## 8. Files to Create
- `app/identity/routers/user_recovery_router.py`
- `app/identity/services/user_recovery_initiation_service.py` — thin delegation + audit wrapper only

## 9. Files to Modify
- `app/identity/routers/__init__.py` — register router

## 10. Backend Requirements
- `UserRecoveryInitiationService.initiate()` calls `RecoveryService.initiate_otp_recovery(parent_id)` unmodified and wraps it with an audit log entry recording which admin triggered it.
- No alternate/bypass recovery path is introduced — this service has no method that sets or reveals a credential directly, by construction.

## 11. Required API / API Contract
`POST /v1/admin/users/{parent_id}/recovery/initiate` → `202` (OTP dispatched to parent's verified channel). `404` for unknown parent, `429` if the underlying rate-limit (owned by A.1/C.19) rejects it.

## 12. Database Requirements
None owned here.

## 13. Validation
`parent_id` existence check (propagated from `RecoveryService`).

## 14. Authentication
`get_current_admin`.

## 15. Authorization
`require_admin_scope("support")`.

## 16. Error Handling
Propagate `RecoveryService`'s existing error semantics unmodified (`404`, `429`), plus `403` for scope failure.

## 17. Security
This endpoint's entire safety property is that it has no independent credential-handling logic — it is a thin, audited trigger into an already-hardened flow. Mandatory test confirms no method in this service sets, reads, or returns a credential/OTP value directly.

## 18. Analytics
Log support-initiated recovery volume for support-tooling usage metrics.

## 19. Performance
No new query paths.

## 20. Library Requirements
FastAPI, Pydantic v2. No new libraries.

## 21. Testing
Unit: delegation-only logic (mock `RecoveryService`, assert correct call, assert no independent credential logic exists). Integration: full initiate → OTP dispatched (mocked) → audit-log-created flow; **mandatory** — structural test confirming this service exposes zero credential-value-returning method.

## 22. Documentation
OpenAPI docstring stating explicitly that this endpoint never resets a credential directly and always routes through the parent's own verified OTP channel.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Implement `UserRecoveryInitiationService` as a Thin Delegation Wrapper**
Objective: Call `RecoveryService.initiate_otp_recovery()` unmodified, wrap with audit logging. Files: `services/user_recovery_initiation_service.py`. Dependencies: A.1/C.19 (existing). Tests: delegation test. Definition of Done: test passes.

**Task 02 — Implement the Router Endpoint**
Objective: `POST` endpoint wired to service. Files: `routers/user_recovery_router.py`. Dependencies: Task 01. Tests: endpoint integration tests. Definition of Done: tests pass.

**Task 03 — Confirm No Direct Credential-Handling Path Exists**
Objective: **Mandatory** structural test. Dependencies: Task 01. Definition of Done: test passes.

**Task 04 — Wire Audit Logging**
Objective: Log every initiation with acting admin + target parent. Dependencies: Task 02. Tests: audit-entry test. Definition of Done: test passes.

**Task 05 — Add Full Test Suite**
Objective: Complete coverage per §21. Definition of Done: all green in CI.

**Task 06 — Final Code Review**
Objective: Confirm zero divergence from A.1/C.19's existing recovery semantics. Definition of Done: checklist in §24 checked.

## 24. Final Verification Checklist
- [ ] Recovery always routes through the existing OTP mechanism, never a direct credential reset
- [ ] Zero method in this service returns/sets a credential value directly — mandatory structural test passing
- [ ] Every initiation is audit-logged with the acting admin
- [ ] `support`+ scope enforced

## 25. Definition of Done
Support staff can initiate account recovery for a parent through a thin, audited trigger into the existing OTP flow, with zero new credential-handling surface introduced.
