# B-13 — Admin Reward Ledger Audit & Reconciliation Incident Viewer API (Admin, Read-Only)

> **⚠ FULLY DEPRECATED.**
> - The **`GET /v1/admin/rewards/ledger` (Ledger Audit Viewer)** portion is superseded by `E31_Engagement_Tools_Admin_Suite/Backend/04-reward-ledger-manual-grant-api.md`, which covers the same read-only ledger view plus the manual reward-grant tool this file never scoped. Implement E.31 B-04 instead.
> - The **`GET /v1/admin/rewards/reconciliation-incidents` (Reconciliation Incident Log)** portion — not covered anywhere in E.31 — has been extracted into its own clean blueprint: **`14-admin-reconciliation-incident-log-api.md` (B-14)**. Implement B-14 instead of this file.
>
> This file is retained for historical/design-rationale reference only. Do not implement anything directly from it.

## 1. Feature Context
Part of Feature A.11 — Rewards System. Two strictly read-only admin surfaces supporting dispute resolution and integrity auditing, with no write capability for any role by design.

## 2. Parent Feature
A.11 Rewards System — Backend (FastAPI)

## 3. Sub-feature
B-13 Admin Reward Ledger Audit & Reconciliation Incident Viewer API (Admin, Read-Only)

## 4. Objective
Implement `GET /v1/admin/rewards/ledger` and `GET /v1/admin/rewards/reconciliation-incidents`, both strictly read-only, per PRD §8/§9/§12.5.

## 5. Business Requirements
- Ledger Audit Viewer: search by masked child/family identifier, full append-only history for support/dispute resolution, `support`/`trust_safety` role.
- Reconciliation Incident Log: every wallet-balance correction the standing reconciliation job (B-03) has made, `trust_safety`/`product_admin` role.
- No edit/delete capability exists for either endpoint at the router layer, matching the backend's DB-level permission lockout on `reward_ledger`/`child_badges`.

## 6. Existing Architecture
Extends the `rewards` bounded context's admin surface, reading from B-01's `reward_ledger` and B-03's `reconciliation_incidents`.

## 7. Existing Code to Reuse
- B-01's `reward_ledger` (read-only from this module).
- B-03's `reconciliation_incidents`.
- `require_admin_scope("support")`/`require_admin_scope("trust_safety")`/`require_admin_scope("product_admin")`.
- Existing identifier-masking utility if one already exists elsewhere in the admin surface (reuse, don't reimplement).

## 8. Files to Create
- `tests/modules/rewards/test_ledger_audit_viewer_readonly.py`
- `tests/modules/rewards/test_reconciliation_log_readonly.py`
- `tests/modules/rewards/test_audit_access_logging.py`

## 9. Files to Modify
- `src/noorheroes/modules/rewards/schemas.py` — `LedgerAuditEntryResponse`, `ReconciliationIncidentResponse`.
- `src/noorheroes/modules/rewards/service.py` — `search_ledger_audit()`, `list_reconciliation_incidents()`.
- `src/noorheroes/modules/rewards/api.py` — add two GET-only admin routes.

## 10. Backend Requirements
- Both endpoints expose only `GET` handlers — no `POST`/`PATCH`/`DELETE` route exists anywhere in this router for these two resources.
- `search_ledger_audit()` masks child identifiers in results by default; full detail access is itself logged (who viewed which child's ledger, when) for dispute-audit-trail purposes.
- Pagination and filtering by date range, `reason_type`, and masked identifier.
- RBAC: `support`/`trust_safety` for the ledger viewer; `trust_safety`/`product_admin` for the reconciliation log.

## 11. KMP Requirements
Not applicable (admin-only).

## 12. NextJS Requirements
Consumed by N-05 (Reward Ledger Audit Viewer) and N-06 (Reconciliation Incident Log).

## 13. API Contract

**Required API — Ledger Audit**
- **HTTP Method:** GET
- **Endpoint:** `/v1/admin/rewards/ledger?child_id_masked=&date_from=&date_to=&reason_type=`
- **Auth:** Bearer, admin session, `support`/`trust_safety` scope.
- **Response 200:** paginated list of masked ledger entries.

**Required API — Reconciliation Incidents**
- **HTTP Method:** GET
- **Endpoint:** `/v1/admin/rewards/reconciliation-incidents`
- **Auth:** Bearer, admin session, `trust_safety`/`product_admin` scope.
- **Response 200:** paginated list of `{ "child_id_masked","old_balance","new_balance","corrected_at" }`.

## 14. Database Requirements
Read-only access to `reward_ledger` (B-01) and `reconciliation_incidents` (B-03); this module introduces no write-capable table.

## 15. Validation
Test: attempt to call any mutating verb against either route returns 405 (route does not exist) — confirming no write capability was accidentally introduced.

## 16. Authentication
Bearer JWT, admin session.

## 17. Authorization
`require_admin_scope("support")`/`"trust_safety"` (ledger); `"trust_safety"`/`"product_admin"` (reconciliation log).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Unauthorized/forbidden request | 401/403 |
| No matching results for a search | 200 with empty list, not an error |
| Any attempted mutating request | 405/404 — route does not exist |

## 19. Offline First
N/A (admin web).

## 20. Local Data
N/A.

## 21. Localization
Admin UI localization is N-05/N-06's concern.

## 22. RTL
N/A (backend).

## 23. Analytics
N/A directly; access to full (unmasked) ledger detail is itself logged for audit-trail purposes per §10.

## 24. Performance
Paginated queries against indexed columns (`(child_id, created_at DESC)` on `reward_ledger`, already present per B-01 §14).

## 25. Security
Read-only-by-design (no write route exists) is this sub-feature's primary integrity guarantee, matching the DB-level permission lockout on the underlying tables — a defense-in-depth pairing (PRD §12.5).

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, PostgreSQL, Pydantic v2.

## 27. Testing
- Unit: masking logic, filter/pagination logic.
- Integration: search/list flows, RBAC rejection tests, no-mutating-route test (mandatory).

## 28. Documentation
OpenAPI docs explicitly stating both endpoints are read-only by design, with no corresponding write capability anywhere in the backend for either resource.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement `search_ledger_audit()` with Masking**
- Files to Modify: `service.py`
- Implementation Details: masked identifiers by default, filter/pagination support.
- Tests: masking-correctness unit test.
- Definition of Done: correct masked results.

**Task 02 — Implement `list_reconciliation_incidents()`**
- Files to Modify: `service.py`
- Implementation Details: paginated read of B-03's `reconciliation_incidents`.
- Definition of Done: correct paginated results.

**Task 03 — Implement Read-Only Endpoints with RBAC**
- Files to Modify: `api.py`
- Authentication/Authorization: per §16/§17.
- Tests: RBAC + no-mutating-route tests (mandatory).
- Definition of Done: endpoints live, verifiably read-only.

**Task 04 — Wire Access Logging for Full-Detail Ledger Views**
- Implementation Details: log admin identity + viewed child/family identifier per detail access.
- Tests: access-logging test.
- Definition of Done: verified.

**Task 05 — Add Documentation & Final Review**
- Documentation: OpenAPI notes per §28.
- Do Not Change: never add a write route to either endpoint under any future requirement without explicit governance sign-off.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Both admin viewers live, read-only by design and by test, RBAC-protected, access to full ledger detail itself audit-logged.

## 31. Final Verification Checklist
- [ ] No mutating route exists for either resource
- [ ] Ledger identifiers masked by default; full-detail access logged
- [ ] RBAC correctly scoped per endpoint (`support`/`trust_safety` vs `trust_safety`/`product_admin`)
- [ ] Pagination/filtering functional
- [ ] OpenAPI documentation states read-only-by-design explicitly
