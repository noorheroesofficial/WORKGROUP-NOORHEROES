# N-04 — Delivery & Engagement Report Dashboard

## 1. Feature Context
Part of Feature B.17 — Notifications (Child-Facing). Read-only dashboard showing sent/delivered/opened rates per category over time, fatigue-backoff trigger frequency, restricted to `product_admin`/`content_editor` roles (PRD §9 item 4).

## 2. Parent Feature
B.17 Notifications (Child-Facing) — NextJS Admin

## 3. Sub-feature
N-04 Delivery & Engagement Report Dashboard

## 4. Objective
Build a read-only reporting dashboard visualizing the sent → delivered → opened funnel per notification category, the suppression-reason breakdown, and fatigue-backoff trigger frequency, sourced from B-08's reporting API.

## 5. Business Requirements
- Sent/delivered/opened rates per category over time (recharts) (PRD §9 item 4).
- Suppression-reason breakdown gives visibility distinguishing healthy suppression (quiet hours, stale condition) from potential calibration issues (frequency cap too aggressive) (PRD §11.1).
- Fatigue-backoff trigger frequency, restricted to `product_admin`/`content_editor` roles (PRD §9 item 4, §8).

## 6. Existing Architecture
- Extends the Admin Portal "Notification Management" module (PRD §8).
- Uses `recharts` per PRD §9 item 4's explicit specification.
- Follows `NEXT-JS-INSTRUCTIONS.md` conventions for dashboards/read-only reporting pages elsewhere in the portal.

## 7. Existing Code to Reuse
- Existing chart/dashboard components elsewhere in the Admin Portal (if a shared charting wrapper around `recharts` already exists, reuse it rather than a new one).
- Existing date-range-picker component used elsewhere in the portal.

## 8. Files to Create
- `app/(admin)/notifications/reports/delivery-engagement/page.tsx`.
- `components/notifications/FunnelChart.tsx`.
- `components/notifications/SuppressionBreakdownChart.tsx`.
- `components/notifications/FatigueBackoffTrendChart.tsx`.
- `lib/api/notifications/reports.ts` — API client.
- `lib/types/notifications.ts` — extend with `DeliveryEngagementReport`.
- `tests/notifications/DeliveryEngagementReport.test.tsx`.

## 9. Files to Modify
- Admin Portal navigation — add "Delivery & Engagement" entry under Notification Management → Reports.

## 10. Backend Requirements
Consumes B-08's `GET /v1/admin/notifications/reports/delivery-engagement` exactly as documented.

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- Page: read-only dashboard with date-range, category, and locale filters.
- Component: funnel chart (created → sent → delivered → opened).
- Component: suppression-reason breakdown chart.
- Component: fatigue-backoff trigger-frequency trend chart.
- API Client: typed wrapper over B-08's endpoint.
- Type Definition: `DeliveryEngagementReport` matching B-08's response shape.
- Authentication/Authorization: `product_admin`/`content_editor` role required to view this page at all (not just to mutate — this is a read-restricted page).
- Loading/Empty/Error States: loading skeleton for charts, empty state for a date range with no data, error state on API failure.
- Pagination/Filtering/Sorting: date-range filter, category filter, locale filter (no pagination needed for aggregate chart data).
- Responsive UI: charts resize/reflow correctly on smaller viewports.
- Caching: leverage B-08's Redis-cached response; avoid redundant client-side re-fetching on trivial UI interactions (e.g., don't re-fetch on chart hover).
- Testing: correct chart rendering from a known fixture API response.

## 13. API Contract
Consumes B-08 §13's `GET /v1/admin/notifications/reports/delivery-engagement` exactly.

## 14. Database Requirements
N/A (frontend only).

## 15. Validation
Date-range picker enforces a reasonable maximum window matching B-08's server-side validation (avoid submitting a request the server will reject with `422`).

## 16. Authentication
Admin session via existing Admin Portal auth context.

## 17. Authorization
Page-level gate: `product_admin`/`content_editor` only; other roles see an access-restricted state or the page is simply not navigable to them (consistent with existing Admin Portal RBAC-gated-navigation patterns).

## 18. Error Handling
| Scenario | System Behavior |
|---|---|
| No data for selected range | Empty-state illustration/message per chart, not a broken/blank chart |
| API failure | Error state with retry action |
| Invalid date range (client-caught before request) | Inline validation preventing the request |
| Unauthorized role | Page-level access-restricted state |

## 19. Offline First
N/A.

## 20. Local Data
N/A (relies on B-08's server-side Redis cache; no client-side persistence needed).

## 21. Localization
Dashboard UI localized per admin's own portal locale preference; the `locale` filter itself is a data filter on the underlying notification data, separate from UI locale.

## 22. RTL
Charts and layout correctly mirror for AR/UR admin UI locale, per existing portal RTL conventions.

## 23. Analytics
Not applicable (this page consumes analytics data, it does not itself emit product analytics events).

## 24. Performance
Leverage B-08's caching; avoid re-fetching the full report on every minor filter tweak — debounce filter-driven re-fetches.

## 25. Security
No raw child-identifying data rendered — all chart data is aggregate counts/rates, consistent with B-08's response contract.

## 26. Library Requirements
Next.js (App Router), TypeScript, React, `recharts`, existing Admin Portal component library.

## 27. Testing
- Unit: chart components render correctly from known fixture data.
- Integration: date-range/category/locale filter changes correctly re-fetch and re-render.
- RBAC: non-`product_admin`/`content_editor` roles cannot access this page.
- Edge case: empty-range response renders the correct empty state per chart.

## 28. Documentation
Document each chart's data source and metric definition (cross-referencing B-08 §5/§10) in code comments for future maintainers.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement Types & API Client**
- Files to Create: `lib/types/notifications.ts` extension, `lib/api/notifications/reports.ts`.

**Task 02 — Implement Dashboard Page Shell with Filters**
- Files to Create: `reports/delivery-engagement/page.tsx`.
- Existing Files to Reuse: existing date-range-picker component.
- Authorization: page-level RBAC gate.

**Task 03 — Implement Funnel Chart**
- Files to Create: `FunnelChart.tsx`.
- Library: `recharts`.
- Tests: fixture-data rendering test.

**Task 04 — Implement Suppression Breakdown Chart**
- Files to Create: `SuppressionBreakdownChart.tsx`.
- Tests: fixture-data rendering test.

**Task 05 — Implement Fatigue Backoff Trend Chart**
- Files to Create: `FatigueBackoffTrendChart.tsx`.
- Tests: fixture-data rendering test.

**Task 06 — Implement Loading/Empty/Error States**
- Files to Modify: dashboard page and chart components.
- Tests: state-rendering tests per §18.

**Task 07 — Write Full Test Suite & Documentation**
- Tests: per §27, including RBAC access test.
- Documentation: per §28.

## 30. Definition of Done
- Dashboard correctly visualizes the full funnel, suppression breakdown, and fatigue-backoff trend from B-08's API.
- Page-level RBAC restricts access to `product_admin`/`content_editor` only.
- Responsive, correctly empty/error/loading-stated, and RTL-aware.

## 31. Final Verification Checklist
- [ ] Funnel chart correctly renders created→sent→delivered→opened from live/fixture data
- [ ] Suppression-reason breakdown correctly categorizes and displays all reason types
- [ ] Fatigue-backoff trend chart renders correctly over the selected date range
- [ ] Date-range/category/locale filters correctly re-fetch and re-render
- [ ] Page is inaccessible to roles other than `product_admin`/`content_editor`
- [ ] Empty and error states render correctly for each chart
- [ ] Full test suite passes
