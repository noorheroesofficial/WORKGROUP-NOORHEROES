# N-05 — Fact Engagement Monitor Dashboard

## 1. Feature Context
Part of Feature B.18 (Islamic Facts Module). A read-only editorial content-quality dashboard, consuming B-07's aggregated engagement API.

## 2. Parent Feature
B.18 — Islamic Facts Module

## 3. Sub-feature
3.5 Fact Engagement Monitor Dashboard (ID: N-05)

## 4. Objective
Build a read-only dashboard (recharts) showing view/quiz-engagement rates per fact and per topic, sourced from B-07's aggregated endpoint, to inform editorial catalog-completeness and content-quality decisions.

## 5. Business Requirements
- §8: Fact Engagement Monitor (Read-only) — aggregate view of fact-view/quiz-engagement rates per fact/topic.
- §11.3 Dashboard Metrics: per-topic engagement rate, AI-fallback-used rate, scholar-approval-revocation frequency.

## 6. Existing Architecture
Next.js page within the Admin Portal's Content Management module, using `recharts` per the platform's existing charting convention.

## 7. Existing Code to Reuse
- Existing Admin Portal dashboard/chart component patterns (reuse chart wrapper components if the platform already has a standard `recharts` wrapper for admin dashboards).

## 8. Files to Create
- `app/(admin)/islamic-facts/engagement/page.tsx`.
- `components/islamic-facts/FactEngagementChart.tsx`.
- `components/islamic-facts/FactEngagementTable.tsx`.

## 9. Files to Modify
- `lib/api/islamicFacts.ts` (N-01) — add `getFactEngagement()`.
- Admin navigation/sidebar config — add "Fact Engagement" entry under Islamic Facts.

## 10. Backend Requirements
Consumes B-07's `GET /v1/admin/facts/engagement`. No backend code produced here.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- **Page/Route:** `/islamic-facts/engagement`.
- **Component:** `FactEngagementChart` (per-topic engagement rate bar chart), `FactEngagementTable` (sortable, paginated per-fact breakdown).
- **Filtering:** date-range filter control (enforces `from <= to`).
- **Authorization/Permissions:** `content_editor` role, read-only — no mutation actions exposed on this page regardless of role.
- **Loading State:** skeleton chart/table while data loads.
- **Empty State:** "No engagement data for this period" when the filtered result set is empty.
- **Error State:** friendly error state with retry, per the platform's general error-boundary convention.
- **Pagination:** paginated table view for per-fact breakdown when the catalog is large.
- **Sorting/Search:** sort table by engagement rate; filter by topic.
- **Responsive UI:** chart and table both responsive per existing Admin Portal dashboard conventions.
- **Accessibility:** chart includes an accessible data-table alternative (not chart-only) for screen-reader users, per standard dashboard accessibility practice.

## 13. API Contract
**Required API:** `GET /v1/admin/facts/engagement` (B-07).
**Authentication:** Bearer, admin.
**Authorization:** `content_editor` role, read-only.

## 14. Database Requirements
N/A directly — consumes B-07's aggregated read-only API.

## 15. Validation
Date-range picker enforces `from <= to`.

## 16. Authentication
Standard Admin Portal auth.

## 17. Authorization
`content_editor` role (read-only); no write actions exposed on this page regardless of role.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| API failure | Friendly error state with retry |
| Empty result (no engagement data yet) | "No engagement data for this period" empty state |
| Invalid date range | Inline validation error, submit blocked |

## 19. Offline First
N/A — online-only admin surface.

## 20. Local Data
N/A.

## 21. Localization
Admin chrome standard localization; topic/fact labels rendered as stored (may include Arabic/Urdu/Hindi text).

## 22. RTL
N/A beyond standard admin chrome handling; fact/topic labels rendered correctly within the LTR dashboard layout regardless of underlying script.

## 23. Analytics
N/A — this page displays analytics, it does not itself require separate instrumentation beyond standard admin page-view tracking if the platform does that generally.

## 24. Performance
Relies on B-07's server-side caching/aggregation; client renders pre-aggregated data, no heavy client-side computation.

## 25. Security
Read-only surface; no mutation risk. Standard admin RBAC (`content_editor`) applies.

## 26. Library Requirements
`recharts` (existing platform convention), existing Admin Portal table component — no new libraries.

## 27. Testing
- Unit: date-range validation.
- Unit: empty-state rendering.
- Integration: chart/table correctly render fixture engagement data from a mocked B-07 response.
- Accessibility: chart's data-table alternative passes automated a11y checks.

## 28. Documentation
Component documentation for `FactEngagementChart`/`FactEngagementTable`; API client documented with JSDoc.

## 29. AI Coding Agent Implementation Steps

**Task 01 — API Client**
Objective: `getFactEngagement()` in `lib/api/islamicFacts.ts`.
Dependencies: B-07 deployed or contract-mocked, N-01's API client file existing.
Definition of Done: Typed client function available.

**Task 02 — Chart Component**
Objective: `FactEngagementChart.tsx` (recharts bar chart, per-topic).
Dependencies: Task 01.
Definition of Done: Chart renders correctly with fixture data.

**Task 03 — Table Component**
Objective: `FactEngagementTable.tsx` (per-fact breakdown, sortable, paginated).
Dependencies: Task 01.
Definition of Done: Table renders and sorts correctly.

**Task 04 — Page Assembly**
Objective: `app/(admin)/islamic-facts/engagement/page.tsx` with date-range filter.
Dependencies: Tasks 02–03.
Definition of Done: Full page functioning end-to-end.

**Task 05 — Tests**
Dependencies: Task 04.
Definition of Done: All green including accessibility checks.

## 30. Definition of Done
- Read-only dashboard functioning against B-07, correct role gating, accessible chart/table presentation.

## 31. Final Verification Checklist
- [ ] Read-only — no mutation actions present on this page
- [ ] `content_editor` role gating verified
- [ ] Chart has an accessible data-table alternative
- [ ] Date-range filter validated
- [ ] Empty and loading states verified
