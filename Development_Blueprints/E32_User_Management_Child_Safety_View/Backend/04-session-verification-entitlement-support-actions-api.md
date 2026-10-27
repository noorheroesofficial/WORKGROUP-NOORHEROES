# B-04 — Session, Verification & Entitlement Support Actions API

## 1. Feature Context
A thin, reused-not-rebuilt layer of support actions — revoking a session, resending a verification, and reading (never editing) entitlement state — assembled from C.19 and C.24's existing services rather than duplicated.

## 2. Parent Feature
E.32 — User Management & Child Safety View

## 3. Sub-feature
1.4 Session, Verification & Entitlement Support Actions API (ID: **B-04**)

## 4. Objective
Build thin admin-scoped endpoints that delegate to C.19's session service (revoke, list) and C.19's verification service (resend), plus a read-only entitlement inspection endpoint delegating to C.24.

## 5. Business Requirements
- Support staff can view a parent's active sessions and revoke one or all.
- Support staff can trigger a verification resend (email/phone) on a parent's behalf.
- Support staff can inspect (read-only) a parent's current entitlements/subscription state for troubleshooting — no edit capability here (billing changes belong to E.33).

## 6. Existing Architecture
`identity` bounded context, thin router delegating to C.19's `SessionService`/`VerificationService` and C.24's `EntitlementService` (`subscriptions` context) — no duplicated business logic.

## 7. Existing Code to Reuse
- C.19: `app/identity/services/session_service.py::SessionService.revoke_session()`, `.list_sessions()`
- C.19: `app/identity/services/verification_service.py::VerificationService.resend()`
- C.24: `app/subscriptions/services/entitlement_service.py::EntitlementService.get_entitlements()` (read-only call)
- E.28's `AuditLogService.log_action()`

## 8. Files to Create
- `app/identity/routers/user_support_actions_router.py`
- `app/identity/services/user_support_actions_service.py` — thin orchestration/delegation layer only

## 9. Files to Modify
- `app/identity/routers/__init__.py` — register router

## 10. Backend Requirements
- `UserSupportActionsService` contains no independent session/verification/entitlement business logic — every method is a thin, audit-logged delegation to the existing C.19/C.24 services, explicitly to avoid a second, divergent implementation of session or entitlement handling.
- Entitlement inspection is strictly read-only — the service exposes no write/update method, by construction (mirrors E.29 B-09's insert-only-repository pattern of enforcing a guarantee by omission).

## 11. Required API / API Contract
`GET /v1/admin/users/{parent_id}/sessions` → list.
`DELETE /v1/admin/users/{parent_id}/sessions/{session_id}` → `204`.
`POST /v1/admin/users/{parent_id}/verification/resend` `{channel}` → `202`.
`GET /v1/admin/users/{parent_id}/entitlements` → read-only entitlement summary.

## 12. Database Requirements
None owned here — reads/writes occur entirely through C.19/C.24's existing repositories.

## 13. Validation
`channel` enum (`email`/`phone`) for resend; `parent_id`/`session_id` existence checked by the delegated services (propagate their `404`s).

## 14. Authentication
`get_current_admin`.

## 15. Authorization
`require_admin_scope("support")` for all four endpoints.

## 16. Error Handling
`404` for unknown parent/session (propagated from C.19); `403` for scope failure; `429` if C.19's verification-resend rate-limiting rejects the request (propagated, not re-implemented here).

## 17. Security
Every action audit-logged with the acting admin and target parent. This layer is deliberately thin to avoid becoming a second source of truth for session/entitlement logic that could drift from C.19/C.24's guarantees over time.

## 18. Analytics
Log support-action volume by type (session revocations, verification resends) for support-tooling usage metrics.

## 19. Performance
No new query paths — delegates entirely to already-optimized C.19/C.24 service methods.

## 20. Library Requirements
FastAPI, Pydantic v2. No new libraries.

## 21. Testing
Unit: delegation-only logic (mock C.19/C.24 services, assert correct method calls with correct arguments, assert no independent business logic exists). Integration: full revoke-session flow, full resend-verification flow, entitlement read returns C.24's data unmodified; **mandatory** — confirm no write/update method exists anywhere in this service for entitlements (static/reflection-style test, mirroring E.29 B-09's pattern).

## 22. Documentation
OpenAPI docstrings noting these endpoints are thin wrappers over C.19/C.24, with links to those features' own documentation for the underlying business rules.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Implement `UserSupportActionsService` as a Thin Delegation Layer**
Objective: Methods that call C.19/C.24 directly, zero independent logic. Files: `services/user_support_actions_service.py`. Dependencies: C.19, C.24 (existing). Tests: mock-based delegation tests. Definition of Done: tests pass.

**Task 02 — Implement Router Endpoints**
Objective: Wire all four endpoints. Files: `routers/user_support_actions_router.py`. Dependencies: Task 01. Tests: endpoint integration tests. Definition of Done: tests pass.

**Task 03 — Confirm Read-Only Entitlement Guarantee**
Objective: **Mandatory** structural test confirming no write/update method exists for entitlements in this service. Dependencies: Task 01. Definition of Done: test passes.

**Task 04 — Wire Audit Logging**
Objective: Log every support action. Dependencies: Task 02. Tests: audit-entry test per action type. Definition of Done: test passes.

**Task 05 — Add Full Test Suite**
Objective: Complete coverage per §21. Definition of Done: all green in CI.

**Task 06 — Final Code Review**
Objective: Confirm this layer introduces zero divergent reimplementation of C.19/C.24 logic. Definition of Done: checklist in §24 checked.

## 24. Final Verification Checklist
- [ ] All four endpoints delegate entirely to existing C.19/C.24 services — no duplicated logic
- [ ] Entitlement inspection is provably read-only — mandatory structural test passing
- [ ] Every action is audit-logged
- [ ] `support`+ scope enforced on all endpoints

## 25. Definition of Done
Support staff have session, verification, and entitlement inspection actions available through a thin, audit-logged layer that reuses C.19/C.24 without duplicating or diverging from their existing guarantees.
