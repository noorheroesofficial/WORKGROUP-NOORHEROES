# N-02 — Gate & Lockout Health Monitor Dashboard

## 1. Feature Context
A read-only dashboard for `product_admin`/`trust_safety` staff: lock-verification failure-rate trend, lockout-trigger frequency by lock type, and Parent Gate success/failure rate. Never displays raw PINs, patterns, or biometric data.

## 2. Parent Feature
Feature C.19 — Parent PIN/Biometric Gate & Profile Access Control

## 3. Sub-feature
3.2 Gate & Lockout Health Monitor Dashboard (ID: **N-02**)

## 4. Objective
Build a new read-only monitor page at `/security/gate-health`, rendering B-06's aggregate metrics as a trend chart plus summary cards, with date-range filtering and strict `product_admin`/`trust_safety` role gating.

## 5. Business Requirements
- Admin Requirements §8: Gate/Lockout Health Monitor — read-only, `product_admin`/`trust_safety` roles.
- §11.3: lock-type distribution, lockout-trigger frequency, grace-window utilization rate, restriction-check-failure-reason breakdown.
- Never displays raw PINs, patterns, or biometric data (hard rule).

## 6. Existing Architecture
New `src/features/gate-health/` module, following the same page/feature-module structure as A.1's N-02 OTP Delivery Health Monitor (also a read-only aggregate dashboard) — reuse that structural pattern rather than inventing a new one.

## 7. Existing Code to Reuse
- `src/shared/components/require-permission.tsx::RequirePermission`
- `src/shared/hooks/use-date-range-filter.ts` (confirm existing convention from A.1's N-02 OTP Health Monitor before building a new one)
- Existing chart component used by A.1's N-02 (confirm library — likely a shared `TrendChart`/`MetricCard` component pair)

## 8. Files to Create
- `src/app/(dashboard)/security/gate-health/page.tsx`
- `src/features/gate-health/api/gate-health-repository.ts` — `GateHealthRepositoryImpl.getMetrics(dateRange, filters)`
- `src/features/gate-health/hooks/use-gate-health-metrics.ts`
- `src/features/gate-health/components/gate-health-summary-cards.tsx`
- `src/features/gate-health/components/lockout-frequency-chart.tsx`
- `src/features/gate-health/components/restriction-failure-breakdown-chart.tsx`
- `src/features/gate-health/types/gate-health-metrics.ts` — Zod schema

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `SECURITY.GATE_HEALTH_METRICS`
- `src/shared/components/dashboard-shell.tsx` — nav item under a Security section, gated by `product_admin`/`trust_safety`

## 10. NextJS Requirements
- `useGateHealthMetrics(dateRange, filters)`: React Query hook against B-06's `GET /v1/admin/security/gate-health-metrics`, with a sensible default range (e.g., last 30 days) and a max-range guard matching the backend's cap.
- `GateHealthSummaryCards`: lock-verification failure rate, Parent Gate success rate as top-line `MetricCard`s.
- `LockoutFrequencyChart`: bar/trend chart of lockout-trigger frequency grouped by `lock_type`.
- `RestrictionFailureBreakdownChart`: breakdown of `failure_reason` distribution from B-04's data.
- Entire page wrapped in `RequirePermission` for `product_admin` OR `trust_safety` — no partial rendering for unauthorized roles (redirect or empty-state, not a broken partial dashboard).

## 11. Required API
`GET /v1/admin/security/gate-health-metrics` (B-06).
**Admin API**

## 12. Loading States
Skeleton loaders for summary cards and charts while the query is in flight.

## 13. Empty States
"No gate activity in the selected range" when aggregates are all zero — not treated as an error.

## 14. Error States
Standard error boundary/inline error card on `500`/`422` (invalid date range), with a retry action.

## 15. Pagination / Filtering
Date-range picker (default last 30 days, capped per B-06's max-span validation); optional `lock_type` filter reflected in the query string for shareable/bookmarkable dashboard views.

## 16. Responsive UI
Charts and cards reflow to a single column on narrower admin-portal viewports, consistent with existing dashboard breakpoints.

## 17. Accessibility
Charts include accessible data-table fallbacks or ARIA labels summarizing key values; summary cards are screen-reader-navigable.

## 18. Localization
Admin Portal internal-tooling scope (confirm against NextJS Core Architecture doc); apply existing i18n convention if the Admin Portal is localized.

## 19. Performance
Query results cached client-side (React Query default staleTime, e.g., 5 min) matching B-06's server-side caching TTL to avoid redundant fetches on rapid navigation.

## 20. Testing
- Unit: `useGateHealthMetrics` hook success/error/empty branches.
- Component: `RequirePermission` correctly blocks non-authorized roles from rendering the page content.
- Component: charts render correctly against a fixture metrics payload, and never render any field resembling raw credential data (structural assertion on the component's prop typing).
- Integration: date-range filter correctly re-queries and updates the URL query string.

## 21. AI Coding Agent Implementation Steps

**Task 01 — Implement `GateHealthRepositoryImpl`**
Objective: typed API client for B-06. Files to Create: `gate-health-repository.ts`, `gate-health-metrics.ts` (Zod schema). Dependencies: B-06 live.

**Task 02 — Implement `useGateHealthMetrics` Hook**
Objective: React Query hook with date-range/filter params. Files to Create: `use-gate-health-metrics.ts`. Dependencies: Task 01.

**Task 03 — Implement Summary Cards & Charts**
Objective: `GateHealthSummaryCards`, `LockoutFrequencyChart`, `RestrictionFailureBreakdownChart`. Files to Create: three component files. Dependencies: Task 02.

**Task 04 — Implement Page & RBAC Gating**
Objective: `/security/gate-health/page.tsx`, `RequirePermission` wrapper, nav item. Files to Create: `page.tsx`. Files to Modify: `dashboard-shell.tsx`. Dependencies: Task 03.

**Task 05 — Add Full Test Suite**
Objective: coverage per §20. Dependencies: Task 01–04.

## 22. Definition of Done
`/security/gate-health` is live, restricted to `product_admin`/`trust_safety`, renders B-06's aggregate metrics with date-range filtering, correct loading/empty/error states, and structurally never surfaces credential-adjacent data.

## 23. Final Verification Checklist
- [ ] Page fully gated behind `product_admin`/`trust_safety`, no partial render for other roles
- [ ] No component prop or rendered value resembles raw PIN/pattern/biometric data
- [ ] Date-range filter respects B-06's max-span validation
- [ ] Empty state distinguished from error state
- [ ] Charts have accessible fallbacks
