# N-03 — Data Export Job Monitoring Dashboard

## 1. Feature Context
Part of Feature C.26's Admin Requirements (§8). Read-only operational health dashboard over B-03's export jobs, consuming B-07.

## 2. Parent Feature
C.26 Privacy, Consent, Account Security & Data Rights (Settings)

## 3. Sub-feature
**N-03 — Data Export Job Monitoring Dashboard**

## 4. Objective
Build a `product_admin`-gated, read-only dashboard showing export-job success/failure rates and processing time over time, sourced exclusively from B-07's aggregate endpoint — no per-family record ever rendered here.

## 5. Business Requirements
- §8: read-only dashboard, success/failure rates, average processing time, `product_admin` role.

## 6. Existing Architecture
Follows the same layered NextJS Admin pattern as N-01/N-02, using a charting component consistent with the platform's other admin dashboards (confirm the existing chart library/component used elsewhere in the admin portal, e.g. for C.19 N-02's health monitor, and reuse it rather than introducing a new charting dependency).

## 7. Existing Code to Reuse
- Existing admin dashboard chart component (confirm from a sibling health-monitor page, e.g. C.19 N-02 "Gate Lockout Health Monitor Dashboard" or C.23 N-02 — reuse its chart wrapper, not a new one).
- `BaseResourceClient` (read-only usage, `get`/aggregate call only — `never` generics on create/update/delete, mirroring C.21 N-01's structural read-only guard).
- `RequirePermission`, date-range picker component (existing, shared).

## 8. Files to Create
- `src/features/data-export-monitor/api/data-export-monitor-client.ts`
- `src/features/data-export-monitor/api/schemas.ts`
- `src/features/data-export-monitor/hooks/use-data-export-metrics.ts`
- `src/app/(dashboard)/product/data-export-monitor/page.tsx`

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `API_ENDPOINTS.DATA_EXPORT_METRICS.BASE`.
- Sidebar navigation — add under Product, gated by `RequirePermission`.

## 10. Backend Requirements
Consumes B-07 exclusively (`GET /v1/admin/data-exports/metrics`).

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- `DataExportMonitorClient extends BaseResourceClient<..., never, never, DataExportMetricsFilters>` — `never` generics on create/update, mirroring C.21 N-01's structural mutation guard, since this is aggregate-read-only by design.
- Dashboard: success/failure-rate chart over the selected date range, average processing-time metric, date-range filter.
- **No individual `data_request` row is ever rendered on this page** — that is N-04's job; this page must remain strictly aggregate.
- `RequirePermission permission="data-export-monitor:read"` — confirm/add to `AdminPermission` catalog, mapped to backend `product_admin`.

## 13. API Contract
Consumes B-07's contract as documented in that blueprint.

## 14. Database Requirements
Not applicable.

## 15. Validation
Date-range filter: `date_from <= date_to`, bounded max range per B-07's server-side cap.

## 16. Authentication
`useAdminSession()`.

## 17. Authorization
`RequirePermission`, `product_admin` only.

## 18. Error Handling
- `QueryErrorState`, `EmptyState` (zero jobs in range), `LoadingState`.
- Excessive date range → inline validation matching B-07's server-side cap.

## 19. Offline First
Not applicable.

## 20. Local Data
Not applicable.

## 21. Localization
Chart labels, date-range picker, metric labels via `useTranslation()`.

## 22. RTL
Full RTL layout including chart mirroring where applicable.

## 23. Analytics
Not specified; this dashboard is itself the analytics surface for export-job health.

## 24. Performance
Aggregate-only queries, bounded date range — never fetch per-family records to compute client-side aggregates.

## 25. Security
- `never` generic-type guard structurally prevents any mutation code from being written against this resource.
- No per-family identifier ever appears in this page's rendered output or network payloads (verified by a negative test).

## 26. Library Requirements
Reuse the existing admin chart library already used by sibling health-monitor pages — no new charting dependency introduced without confirming none already exists.

## 27. Testing
- Unit: `DataExportMonitorClient` Zod schema validation.
- Integration/UI: chart renders correctly from fixture aggregate data.
- Integration/UI: date-range filter re-queries correctly.
- Negative test: no per-family identifier appears anywhere in the rendered page or its network requests.
- Integration/UI: `RequirePermission` correctly restricts to `product_admin`.

## 28. Documentation
Document that this page is intentionally aggregate-only; per-record visibility is N-04's responsibility.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm Existing Chart Component**
- **Objective:** Locate the admin portal's existing dashboard chart wrapper before adding a new library.

**Task 02 — Resource Client with `never` Mutation Generics**
- **Files to Create:** `data-export-monitor-client.ts`, `schemas.ts`.

**Task 03 — `useDataExportMetrics` Hook**

**Task 04 — Dashboard Page**
- **Files to Create:** `page.tsx`.
- **Tests:** the per-family-identifier-absence negative test.

**Task 05 — Permission Wiring, Localization, RTL**

**Task 06 — Full Test Suite & Documentation**

## 30. Definition of Done
Export-job health metrics are visible to `product_admin` in a strictly aggregate, read-only dashboard reusing the platform's existing chart component, with a structural guarantee (via `never` generics and a negative test) that no per-family data ever surfaces here.

## 31. Final Verification Checklist
- [ ] `never` generics used for create/update/delete
- [ ] Reuses existing admin chart component, no new charting library added without confirming necessity
- [ ] No per-family identifier appears anywhere on this page (negative test passes)
- [ ] `RequirePermission` correctly restricts to `product_admin`
- [ ] Full localization and RTL verified
