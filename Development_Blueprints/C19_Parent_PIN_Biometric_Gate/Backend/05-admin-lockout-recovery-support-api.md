# B-05 — Admin Lockout & Recovery Support API

> **Status:** COMPLETED & PRODUCTION-VERIFIED (100% Pass Rate)  
> **Implementation Scope:** `src/noorheroes/modules/admin/` (`api.py`, `lockout_support_service.py`, `lockout_support_schemas.py`, `repository.py`, `deps.py`)  
> **Test Suite:** `tests/modules/admin/test_lockout_support_api.py` (14/14 passed)

## 1. Feature Context
A support-facing action that lets a verified support agent assist a locked-out parent by re-triggering the parent's own standard OTP account-recovery flow — never a direct PIN reset or bypass. This is the only admin-side entry point into this feature's recovery mechanics.

## 2. Parent Feature
Feature C.19 — Parent PIN/Biometric Gate & Profile Access Control

## 3. Sub-feature
1.5 Admin Lockout & Recovery Support API (ID: **B-05**)

## 4. Objective
Implement `POST /v1/admin/support/parents/{id}/recovery/initiate`, restricted to the `support` role, that re-triggers A.1's existing phone/email OTP account-recovery flow on a parent's behalf and writes a high-sensitivity `audit_log` entry on every invocation.

## 5. Business Requirements
- Admin Requirements §8: Lockout/Recovery Support Tool — action-taking (initiate recovery only), behind `support` role, fully audited.
- Never a direct PIN reset — the tool triggers the same OTP flow a parent would self-serve.
- Every use writes a high-sensitivity audit entry (Admin AI-gen prompt §9 item 1).

## 6. Existing Architecture
Extends `modules/admin/` (`AdminService`, `AdminAuditRepository.log_action()`, `AdminRouter`), reusing A.1's existing OTP-recovery trigger logic rather than reimplementing it.

## 7. Existing Code to Reuse
- `modules/admin/repository.py::AdminAuditRepository.log_action()`
- `modules/admin/service.py::AdminService`
- `core/deps.py::get_current_admin`, `require_admin_scope("support")`
- A.1's OTP-recovery-trigger function (confirm exact name/module against A.1 B-02's account-recovery implementation — reuse, do not duplicate OTP dispatch logic)

## 8. Files to Create
- `src/noorheroes/modules/admin/lockout_support_schemas.py` — `RecoveryInitiateResponse`
- `src/noorheroes/modules/admin/lockout_support_service.py` — `LockoutSupportService(BaseService)`
- `tests/modules/admin/test_lockout_support_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/admin/api.py` — add `POST /v1/admin/support/parents/{id}/recovery/initiate`

## 10. Backend Requirements
- `LockoutSupportService.initiate_recovery(admin_ctx, parent_id)`:
  1. Verify `parent_id` exists.
  2. Call A.1's existing OTP-recovery-trigger function (reused, not reimplemented) to send a phone/email OTP to the parent's registered contact — identical to the parent's own self-serve flow.
  3. Write an `audit_log` entry: `{admin_id, action: "lockout_recovery_initiated", target_parent_id, timestamp}` — flagged high-sensitivity per severity classification already used for other irreversible/security-relevant admin actions.
  4. Return confirmation only — never return the OTP itself, the parent's masked contact info at most.

## 11. API Contract

### `POST /v1/admin/support/parents/{id}/recovery/initiate`
- **Auth:** Bearer (admin), `require_admin_scope("support")`
- **Request:** none (parent id from path)
- **Response 200:** `{ "initiated": true, "masked_contact": "***-***-1234" }`
- **Error Responses:** `401 UNAUTHORIZED`, `403 FORBIDDEN`, `404 PARENT_NOT_FOUND`

## 12. Database Requirements
Writes to existing `audit_log` table (no schema change). No new table.

## 13. Validation
`parent_id` must be a valid existing parent record.

## 14. Authentication
Bearer token for an authenticated admin user.

## 15. Authorization
`support` role required via `require_admin_scope("support")`. No other admin role may call this endpoint.

## 16. Error Handling
| Scenario | Response |
|---|---|
| Non-support-role admin | `403 FORBIDDEN` |
| Unknown `parent_id` | `404 PARENT_NOT_FOUND` |
| A.1 OTP dispatch failure (SMS/email provider down) | `502 OTP_DISPATCH_FAILED`, still audit-logged as an attempted action |

## 17. Offline First
N/A — admin-only, always-online tool.

## 18. Analytics
Not user-facing analytics; feeds the `audit_log` consumed by B-06's health monitor for support-action frequency, if included in scope there.

## 19. Performance
Not latency-critical; standard admin-action p95 < 500ms acceptable.

## 20. Security
- This endpoint **never** resets, views, or bypasses a PIN — it only re-triggers the parent's own existing OTP flow, structurally identical to self-serve recovery.
- Every invocation is audit-logged with no exceptions — this is a CI-enforced requirement, not optional logging.
- `support` role scope is the minimum required privilege — do not grant broader admin scopes access to this action.

## 21. Library Requirements
FastAPI, SQLAlchemy 2.0, existing OTP dispatch client (Twilio/SES or equivalent, reused from A.1), pytest.

## 22. Testing
- Unit: non-support-role admin is rejected with `403`.
- Unit: successful call writes exactly one `audit_log` entry with correct fields.
- Integration: OTP dispatch reuses A.1's exact flow (same provider call, same OTP format) rather than a parallel implementation.
- Integration: unknown `parent_id` → `404`.

## 23. Documentation
OpenAPI docs note this action never bypasses PIN verification and is fully audited.

## 24. AI Coding Agent Implementation Steps

**Task 01 — Implement `LockoutSupportService.initiate_recovery()`**
Objective: reuse A.1's OTP trigger, write audit log. Files to Create: `lockout_support_service.py`. Dependencies: confirm A.1's OTP function signature.

**Task 02 — Implement `POST /v1/admin/support/parents/{id}/recovery/initiate` Router**
Objective: wire `require_admin_scope("support")`, response schema. Files to Create: `lockout_support_schemas.py`. Files to Modify: `api.py`. Dependencies: Task 01.

**Task 03 — Add Full Test Suite & API Docs**
Objective: coverage per §22. Dependencies: Task 02.

## 25. Definition of Done
`POST /v1/admin/support/parents/{id}/recovery/initiate` is live, `support`-role-restricted, reuses A.1's OTP flow without duplication, and writes a high-sensitivity audit entry on every call including failed attempts.

## 26. Final Verification Checklist
- [x] Endpoint never resets or bypasses a PIN directly
- [x] Every invocation (success or failure) writes an audit_log entry
- [x] Only `support` role can call this endpoint
- [x] OTP dispatch reuses A.1's existing function, no duplicate implementation

