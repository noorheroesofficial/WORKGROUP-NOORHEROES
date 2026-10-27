# N-04 — Revenue Analytics Dashboard

## 1. Feature Context
A read-only dashboard surfacing the platform's primary monetization health metrics — trial-to-paid conversion rate, annual-vs-monthly plan share, churn/cancellation trend — sourced from C.24's subscription/invoice data. **Note:** full detail owned by E.33; this blueprint implements C.24's own ownership sketch (§8, §11.5).

## 2. Parent Feature
Feature C.24 — Subscription & Billing

## 3. Sub-feature
3.4 Revenue Analytics Dashboard (ID: **N-04**)

## 4. Objective
Build a `product_admin`/`commerce_admin`-restricted, read-only analytics dashboard tracking trial-to-paid conversion (≥25% Phase 3 exit criterion), annual-plan share (≥40%), and churn/cancellation trends, sourced from a read-only aggregated endpoint.

## 5. Business Requirements
- §11.3/§11.5: trial-to-paid conversion rate, annual-vs-monthly plan share, cancellation/downgrade rate, payment-failure/grace-period-recovery rate, reconciliation-drift-correction frequency.
- §1.4 Success Metrics: trial-to-paid ≥25%, annual-plan share ≥40% of paid — these are the primary go/no-go metrics for Phase 3 (PRD §15.3).
- Comp grants (E.33-owned) must be clearly separated from real revenue in all reporting.

## 6. Existing Architecture
`src/features/commerce/` (extends N-01–N-03's feature folder); charting via `recharts` per the platform's existing admin chart convention.

## 7. Existing Code to Reuse
- Existing `recharts`-based chart components used elsewhere in the Admin Portal (confirm exact shared chart-wrapper component before building a new one).
- `src/shared/components/date-range-picker.tsx` (or equivalent) for time-window filtering.

## 8. Files to Create
- `src/features/commerce/api/revenue-analytics-repository.ts`
- `src/features/commerce/hooks/use-revenue-analytics.ts`
- `src/features/commerce/components/revenue-analytics-dashboard.tsx`
- `src/app/(dashboard)/commerce/revenue/page.tsx`

## 9. Files to Modify
- Sidebar navigation config — add "Revenue Analytics" under Commerce, `product_admin`/`commerce_admin`-gated

## 10. NextJS Requirements
- `useRevenueAnalytics(dateRange)`: fetches aggregated conversion/churn/plan-mix metrics for the selected window.
- Charts: trial-to-paid conversion funnel (mirrors PRD §11.2's `plan_comparison_viewed`→`trial_disclosure_viewed`→`trial_started`→`trial_auto_converted` funnel), annual-vs-monthly plan-share pie/bar, cancellation/downgrade trend line, comp-grants-excluded revenue figures clearly labeled as such.
- Explicit go/no-go threshold markers on the conversion/annual-share charts (25%/40%) for at-a-glance Phase 3 tracking.

## 11. Required API
Read-only aggregated revenue/conversion metrics endpoint — exact contract owned by E.33's backend specification. **Admin API.**

## 12. Validation
Date-range picker constrained to valid historical windows (no future-dated ranges).

## 13. Authentication
Existing Admin Portal auth context (Bearer session).

## 14. Authorization
`product_admin`/`commerce_admin` role, read-only, enforced via `RequirePermission` and server-side check.

## 15. Error Handling
Chart-level empty/error states (e.g., insufficient data for the selected window) rendered per-chart, not a single dashboard-wide failure.

## 16. Loading States
Chart skeletons while data loads; date-range change triggers a scoped re-fetch with its own loading indicator, not a full-page reload.

## 17. Responsive UI
Charts reflow to stacked single-column on narrow viewports; recharts responsive-container pattern.

## 18. Accessibility
Charts include accessible data-table fallback or summary text (screen-reader users should not rely solely on visual chart rendering for these go/no-go metrics).

## 19. Localization
Admin Portal typically EN-only for internal tooling (confirm against `NEXT-JS-INSTRUCTIONS.md`); number/percentage formatting still locale-correct if the admin's own locale preference is honored elsewhere in the portal.

## 20. Testing
- Unit: `useRevenueAnalytics` hook success/error/empty branches.
- Component: charts render correct data shape from a mocked aggregated response.
- Component: go/no-go threshold markers render at the correct 25%/40% positions.
- RBAC: non-`product_admin`/`commerce_admin` users blocked from the route.

## 21. AI Coding Agent Implementation Steps

**Task 01 — Implement `RevenueAnalyticsRepositoryImpl`**
Objective: typed aggregated-metrics API client. Files to Create: `revenue-analytics-repository.ts`. Dependencies: backend aggregation endpoint live (E.33).

**Task 02 — Implement `useRevenueAnalytics` Hook**
Objective: date-range-scoped query hook. Files to Create: `use-revenue-analytics.ts`. Dependencies: Task 01.

**Task 03 — Implement Dashboard Charts**
Objective: conversion funnel, plan-share, churn-trend charts with threshold markers. Files to Create: `revenue-analytics-dashboard.tsx`. Dependencies: Task 02.

**Task 04 — Wire Page Route & Navigation**
Objective: `/commerce/revenue` page, RBAC-gated nav entry. Files to Create/Modify: page file, sidebar nav config. Dependencies: Task 03.

**Task 05 — Add Full Test Suite**
Objective: coverage per §20. Dependencies: Tasks 01–04.

## 22. Definition of Done
`product_admin`/`commerce_admin` roles can view a read-only revenue analytics dashboard tracking conversion, plan mix, and churn against the Phase 3 exit-criteria thresholds, with comp grants clearly excluded from real-revenue figures.

## 23. Final Verification Checklist
- [ ] Trial-to-paid conversion and annual-plan-share charts render with correct 25%/40% threshold markers
- [ ] Comp grants clearly separated from real revenue in all displayed figures
- [ ] `product_admin`/`commerce_admin` role enforced client- and server-side
- [ ] Per-chart empty/error states verified independently
- [ ] Accessible fallback (table/summary text) present for chart data
