# B-14 — Admin Reconciliation Incident Log API (Admin, Read-Only)

> **Split out from B-13** on 2026-08-18 after discovering `E31_Engagement_Tools_Admin_Suite` duplicates B-13's Ledger Audit Viewer portion (superseded by E.31 B-04) but has no equivalent for the reconciliation-incident surface. This file is the clean, standalone replacement for that surviving portion — implement this instead of B-13, whose combined file is now fully deprecated (see the deprecation note at the top of `13-admin-reward-ledger-audit-reconciliation-viewer-api.md`).

## 1. Feature Context
Part of Feature A.11 — Rewards System. A strictly read-only surface over every wallet-balance correction the standing reconciliation job (B-03) has ever made — not covered by E.31's Engagement Tools Admin Suite, and remains uniquely owned by A.11.

## 2. Parent Feature
A.11 Rewards System — Backend (FastAPI)

## 3. Sub-feature
B-14 Admin Reconciliation Incident Log API (Admin, Read-Only)

## 4. Objective
Implement `GET /v1/admin/rewards/reconciliation-incidents`, strictly read-only, restricted to `trust_safety`/`product_admin`.

## 5. Business Requirements
- Every wallet-balance correction the standing reconciliation job (B-03) has made, `trust_safety`/`product_admin` role.
- No edit/delete capability exists for this endpoint at the router layer, matching the backend's DB-level design (B-03's `reconciliation_incidents` table has no application write grant outside B-03's own job).

## 6. Existing Architecture
Extends the `rewards` bounded context's admin surface, reading from B-03's `reconciliation_incidents` table.

## 7. Existing Code to Reuse
- B-03's `reconciliation_incidents` table.
- `require_admin_scope("trust_safety")`/`require_admin_scope("product_admin")`.

## 8. Files to Create
- `tests/modules/rewards/test_reconciliation_log_readonly.py`

## 9. Files to Modify
- `src/noorheroes/modules/rewards/schemas.py` — `ReconciliationIncidentResponse`.
- `src/noorheroes/modules/rewards/service.py` — `list_reconciliation_incidents()`.
- `src/noorheroes/modules/rewards/api.py` — add one GET-only admin route.

## 10. Backend Requirements
- Endpoint exposes only `GET` — no `POST`/`PATCH`/`DELETE` route exists for this resource anywhere.
- Pagination and filtering by date range and correction-magnitude threshold.
- RBAC: `trust_safety`/`product_admin`.

## 11. KMP Requirements
Not applicable (admin-only).

## 12. NextJS Requirements
Consumed by N-06 (Reconciliation Incident Log) — unchanged, already correctly scoped to only this endpoint.

## 13. API Contract

**Required API**
- **HTTP Method:** GET
- **Endpoint:** `/v1/admin/rewards/reconciliation-incidents?date_from=&date_to=&min_magnitude=`
- **Auth:** Bearer, admin session, `trust_safety`/`product_admin` scope.
- **Response 200:** paginated list of `{ "child_id_masked","old_balance","new_balance","corrected_at" }`.

## 14. Database Requirements
Read-only access to `reconciliation_incidents` (B-03); this module introduces no write-capable table.

## 15. Validation
Test: attempt to call any mutating verb against this route returns 404/405 (route does not exist).

## 16. Authentication
Bearer JWT, admin session.

## 17. Authorization
`require_admin_scope("trust_safety")`/`"product_admin"`.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Unauthorized/forbidden request | 401/403 |
| No incidents in range | 200 with empty list, not an error |
| Any attempted mutating request | 405/404 — route does not exist |

## 19. Offline First
N/A (admin web).

## 20. Local Data
N/A.

## 21. Localization
Admin UI localization is N-06's concern.

## 22. RTL
N/A (backend).

## 23. Analytics
N/A; this surfaces an integrity metric rather than emitting one.

## 24. Performance
Paginated queries against B-03's `(child_id)` index.

## 25. Security
Read-only-by-design is this endpoint's primary integrity guarantee — no role, including `product_admin`, can mutate reconciliation history through this API.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, PostgreSQL, Pydantic v2.

## 27. Testing
- Unit: filter/pagination logic.
- Integration: list flow, RBAC rejection tests, no-mutating-route test (mandatory).

## 28. Documentation
OpenAPI docs explicitly stating this endpoint is read-only by design, with no corresponding write capability anywhere in the backend.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement `list_reconciliation_incidents()`**
- Files to Modify: `service.py`
- Implementation Details: paginated read of B-03's `reconciliation_incidents`, filter by date range/magnitude.
- Definition of Done: correct paginated results.

**Task 02 — Implement Read-Only Endpoint with RBAC**
- Files to Modify: `api.py`
- Authentication/Authorization: per §16/§17.
- Tests: RBAC + no-mutating-route tests (mandatory).
- Definition of Done: endpoint live, verifiably read-only.

**Task 03 — Add Documentation & Final Review**
- Documentation: OpenAPI notes per §28.
- Do Not Change: never add a write route to this endpoint.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Reconciliation Incident Log endpoint live, read-only by design and by test, RBAC-protected.

## 31. Final Verification Checklist
- [ ] No mutating route exists for this resource
- [ ] RBAC correctly scoped (`trust_safety`/`product_admin`)
- [ ] Pagination/filtering functional
- [ ] OpenAPI documentation states read-only-by-design explicitly
- [ ] Confirmed not duplicated anywhere in E.31
