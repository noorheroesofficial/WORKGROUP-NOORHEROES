# N-06 — Reconciliation Incident Log (Read-Only)

## 1. Feature Context
Part of Feature A.11 — Rewards System. Strictly read-only integrity-auditing surface over every wallet-balance correction the standing reconciliation job (B-03) has ever made.

## 2. Parent Feature
A.11 Rewards System — NextJS Admin

## 3. Sub-feature
N-06 Reconciliation Incident Log (Read-Only)

## 4. Objective
Build the read-only Reconciliation Incident Log page consuming B-13, restricted to `trust_safety`/`product_admin`, per PRD §8/§9.

## 5. Business Requirements
- Read-only table of every wallet-balance correction the standing reconciliation job has made (`child_id` masked, `old_balance`, `new_balance`, `timestamp`).
- Restricted to `trust_safety`/`product_admin` role.
- Supports integrity/trust auditing over time via a correction-frequency trend view (an economy-health metric, ideally trending toward zero per PRD §11.3).

## 6. Existing Architecture
Existing Admin Portal shell; reuses `DataTable`, `FilterPanel`, `RequirePermission`, and the dashboard-metric-widget pattern already established for other admin dashboards (e.g., `DashboardRepositoryImpl`/`DashboardShell` per `NEXT-JS-INSTRUCTIONS.md §5/§8`).

## 7. Existing Code to Reuse
- `DataTable`, `FilterPanel`, `RequirePermission`, `LoadingState`, `EmptyState`, `ErrorView`.
- `DashboardShell`/existing chart component if one is already used elsewhere for a simple trend widget (reuse, don't introduce a new charting library for a single small widget).
- Read-only `BaseResourceClient` subset pattern established in N-05.

## 8. Files to Create
- `src/features/rewards/reconciliation/ReconciliationIncidentResourceClient.ts` (read-only client)
- `src/features/rewards/reconciliation/ReconciliationIncidentLogPage.tsx`
- `src/features/rewards/reconciliation/ReconciliationTrendWidget.tsx`
- `src/features/rewards/reconciliation/__tests__/ReconciliationIncidentLogPage.test.tsx`

## 9. Files to Modify
- Admin route registry — `/rewards/reconciliation-incidents`.
- Admin nav/sidebar config.

## 10. Backend Requirements
Consumes B-13 (`GET /v1/admin/rewards/reconciliation-incidents`).

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- `ReconciliationIncidentResourceClient` implements **only** `list()` — no mutating method exists on this client.
- `ReconciliationIncidentLogPage` renders the incident table plus a `ReconciliationTrendWidget` summarizing correction frequency over time (a simple count-over-time visualization, reusing whatever minimal charting approach the Admin Portal already uses elsewhere for similarly small dashboard widgets).
- Filter by date range and correction-magnitude threshold, supporting anomaly triage.

## 13. API Contract
`GET /v1/admin/rewards/reconciliation-incidents` (B-13).

## 14. Database Requirements
N/A (admin frontend).

## 15. Validation
UI test confirming no edit/delete control exists anywhere on this page, for any role, including `product_admin`.

## 16. Authentication
Reuses existing Admin session/auth flow.

## 17. Authorization
`RequirePermission` gate for `trust_safety`/`product_admin`.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| No incidents in range (a healthy sign, not an error) | `EmptyState` framed positively (e.g., "No corrections in this period — wallet integrity holding steady"), not a generic blank-table message |
| Fetch failure | `ErrorView` with retry |
| Insufficient permission | Permission-denied state |

## 19. Offline First
Not applicable (admin web).

## 20. Local Data
Not applicable.

## 21. Localization
Admin UI localized (labels, filter controls, trend-widget framing text).

## 22. RTL
Table/widget layout mirrors correctly for Arabic admin locale.

## 23. Analytics
N/A directly; this page itself surfaces an integrity/trust metric rather than emitting one.

## 24. Performance
`DataTable` pagination; trend widget aggregates server-side where feasible rather than pulling the full incident history client-side for charting.

## 25. Security
Read-only-by-design at both the client (no mutating methods) and backend (B-13, no write route) layers — this pairing is the page's defining trust property, preventing even well-intentioned manual "corrections" that would undermine the ledger's pure append-only integrity guarantee.

## 26. Library Requirements
Existing Admin Portal stack; minimal existing charting approach for the trend widget.

## 27. Testing
- Unit: date-range/threshold filter param construction.
- Integration: list/filter flow, permission-gated rendering, no-write-control UI test (mandatory).

## 28. Documentation
Component README stating this page is read-only by design and explaining the trend widget's "trending toward zero is healthy" framing for future admin-UX contributors.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement Read-Only `ReconciliationIncidentResourceClient`**
- Files to Create: `ReconciliationIncidentResourceClient.ts`
- Do Not Change: never add a create/update/delete method to this client.
- Definition of Done: only `list()` exists.

**Task 02 — Build `ReconciliationIncidentLogPage`**
- Files to Create: `ReconciliationIncidentLogPage.tsx`
- Existing Files to Reuse: `DataTable`, `FilterPanel`, `RequirePermission`.
- Tests: no-write-control UI test (mandatory).
- Definition of Done: test passing.

**Task 03 — Build `ReconciliationTrendWidget`**
- Files to Create: `ReconciliationTrendWidget.tsx`
- Implementation Details: correction-frequency-over-time summary, reusing existing minimal charting approach.
- Definition of Done: widget renders correctly against fixture data.

**Task 04 — Wire Route, Nav, and Permission Gate**
- Files to Modify: route registry, nav config.
- Definition of Done: `/rewards/reconciliation-incidents` reachable only to `trust_safety`/`product_admin`.

**Task 05 — Documentation & Final Review**
- Documentation: README per §28.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Reconciliation Incident Log live, verifiably read-only, RBAC-gated, with a correction-frequency trend widget supporting ongoing integrity auditing.

## 31. Final Verification Checklist
- [ ] No write/edit/delete control exists anywhere on this page, for any role
- [ ] `ReconciliationIncidentResourceClient` contains no mutating method definitions
- [ ] Trend widget renders correctly and frames zero-incidents as a healthy state
- [ ] Filter by date range / correction-magnitude functional
- [ ] `RequirePermission` restricts to `trust_safety`/`product_admin`
- [ ] Localization and RTL verified
