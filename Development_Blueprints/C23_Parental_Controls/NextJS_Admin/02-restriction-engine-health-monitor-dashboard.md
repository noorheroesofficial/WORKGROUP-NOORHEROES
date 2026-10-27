# N-02 — Restriction Engine Health Monitor Dashboard

## 1. Feature Context
A read-only operational dashboard giving admins/product visibility into heartbeat-processing latency, override-grant frequency, and limit/bedtime-block event volume — a calibration and health signal (PRD C.23 §8, §11.3).

## 2. Parent Feature
Feature C.23 — Parental Controls (Screen Time, Bedtime, AI Permissions, Content Age Level)

## 3. Sub-feature
3.2 Restriction Engine Health Monitor Dashboard (ID: **N-02**)

## 4. Objective
Build a read-only, recharts-based dashboard visualizing heartbeat-processing latency (p50/p95/p99), override-grant frequency by type, and limit/bedtime-block event volume over a selectable time window, sourced from B-07's health endpoint.

## 5. Business Requirements
- §8: Health Monitor is read-only, behind `product_admin`/`content_editor`.
- §11.3 Dashboard Metrics: screen-time policy configuration rate/typical limits, override-grant frequency/typical minutes, bedtime-block frequency, AI-permissions configuration distribution.
- §11.2 Funnel Analysis: `restriction_warning_notification_fired` → `restriction_limit_reached` → `restriction_calm_rest_screen_shown` → (`restriction_override_requested` → `_granted` OR session ends).

## 6. Existing Architecture
Follows the Admin Portal's read-only dashboard pattern (comparable to `useDashboardStats`/`DashboardRepositoryImpl`). Uses `recharts` per the platform's established admin charting library (already referenced in NEXT-JS-INSTRUCTIONS.md's `DashboardRepositoryImpl` context).

## 7. Existing Code to Reuse
- `DashboardRepositoryImpl`/`useDashboardStats` pattern as the direct architectural precedent
- `RequirePermission`
- `LoadingState`, `ErrorView`/`QueryErrorState`
- `useFormatters()` for date/number formatting on chart axes

## 8. Files to Create
- `src/features/restriction-engine/api/health-monitor.repository.ts`
- `src/features/restriction-engine/hooks/use-restriction-health.ts`
- `src/features/restriction-engine/components/heartbeat-latency-chart.tsx`
- `src/features/restriction-engine/components/override-grant-frequency-chart.tsx`
- `src/features/restriction-engine/components/block-event-volume-chart.tsx`
- `src/features/restriction-engine/components/date-range-filter.tsx` (or reuse an existing shared filter component if one exists)
- `src/app/(dashboard)/restriction-engine/health/page.tsx`
- `src/features/restriction-engine/__tests__/health-monitor-dashboard.test.tsx`

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `RESTRICTION_ENGINE.HEALTH`
- Sidebar navigation config — add "Health Monitor" entry

## 10. NextJS Requirements
- `health-monitor.repository.ts::getHealth(dateRange, signal)` → B-07's `GET /v1/admin/restrictions/health`.
- `useRestrictionHealth(dateRange)`: React Query hook, standard stale-time/caching per `useDashboardStats` convention.
- Three recharts visualizations: latency line/area chart (p50/p95/p99 series), override-grant-frequency bar chart split by `screen_time`/`bedtime`, block-event-volume time series.
- Date-range filter control (reuse existing shared component if present in `src/shared/components/`).
- Fully read-only — no mutation hooks, no write actions anywhere on this page.
- Accessible chart-data-table fallback for screen readers (per project accessibility requirement).

## 11. API Contract
### Required API (consumed)
- **HTTP Method:** GET — **Endpoint:** `/v1/admin/restrictions/health` (B-07)
- **Authentication:** Bearer (admin), `product_admin`/`content_editor` scope

## 12. Database Requirements
N/A (frontend; backed by B-07's aggregation queries).

## 13. Validation
- Date-range input bounded to sane min/max (e.g., not more than 12 months) to avoid over-fetching heavy aggregation queries.

## 14. Authentication
Standard admin session (`useAdminSession()`).

## 15. Authorization
`RequirePermission permission="restriction_engine:health:read"` (confirm exact string against actual `AdminPermission` enum).

## 16. Error Handling
| Scenario | UI Behavior |
|---|---|
| Load failure | `QueryErrorState` with retry, correlation ID shown |
| Empty data for selected range | `EmptyState` with guidance to widen the range |

## 17. Offline First
N/A (admin web app).

## 18. Local Data
N/A.

## 19. Localization
Chart labels/legends and date-range control localized via `useTranslation()`/`useFormatters()`.

## 20. RTL
Chart layout and legend positioning must support RTL locales if the Admin Portal enables them.

## 21. Analytics
This page itself visualizes the analytics defined in PRD §11 (funnel, dashboard metrics); it is a consumer, not a producer, of those events.

## 22. Performance
Charts should render from a single aggregated API response (per §22 of B-07, using pre-aggregated data) rather than client-side aggregation over raw records — avoid re-fetching on every filter tweak without debouncing.

## 23. Security
Read-only surface; no elevated-session requirement (lower risk than N-01's ceiling-table editor).

## 24. Library Requirements
Next.js 15, TanStack Query v5, recharts (CDN/npm per existing platform convention — confirm exact import path against current Admin Portal recharts usage).

## 25. Testing
- Component test: charts render correctly given mocked aggregate data.
- Component test: empty state renders for a date range with no data.
- Component test: date-range filter triggers a new query with correct parameters.

## 26. Documentation
Inline comments explaining each chart's data source mapping to B-07's response shape.

## 27. AI Coding Agent Implementation Steps

**Task 01 — Confirm recharts Usage Convention**
- Objective: Verify exact import/setup pattern against existing Admin Portal dashboard code before introducing new chart boilerplate.

**Task 02 — Add API Endpoint Constant**
- Files to Modify: `api-endpoints.ts`

**Task 03 — Implement Repository**
- Files to Create: `health-monitor.repository.ts`

**Task 04 — Implement Query Hook**
- Files to Create: `use-restriction-health.ts`

**Task 05 — Implement Latency Chart Component**
- Files to Create: `heartbeat-latency-chart.tsx`

**Task 06 — Implement Override-Grant-Frequency Chart Component**

**Task 07 — Implement Block-Event-Volume Chart Component**

**Task 08 — Implement Date-Range Filter**

**Task 09 — Implement Page Route**
- Files to Create: `page.tsx`

**Task 10 — Add Accessible Data-Table Fallback for Each Chart**

**Task 11 — Add Sidebar Navigation Entry**

**Task 12 — Add Component Tests**

**Task 13 — Final Code Review**
- Objective: Confirm the page is strictly read-only with no accidental write actions.

## 28. Definition of Done
- All three charts render correctly from B-07's aggregate data.
- Date-range filtering works correctly.
- Fully read-only, RBAC-gated.

## 29. Final Verification Checklist
- [ ] Confirmed real `AdminPermission` string used
- [ ] All three charts tested with mocked data
- [ ] Empty state tested
- [ ] Accessible fallback present for each chart
- [ ] No write/mutation actions present anywhere on this page
- [ ] Localization strings added
