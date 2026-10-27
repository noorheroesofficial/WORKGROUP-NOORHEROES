# N-02 — Bedtime Configuration Analytics Dashboard

## 1. Feature Context
A new, read-only recharts dashboard giving product/admin stakeholders visibility into bedtime-window adoption, sleep-timer-ceiling calibration, and ritual-completion trends — sourced exclusively from B-05's pre-aggregated endpoint, structurally incapable of displaying any individual child's data.

## 2. Parent Feature
Feature A.4 — Audio Bedtime Player & Bedtime Mode

## 3. Sub-feature
3.2 Bedtime Configuration Analytics Dashboard (ID: **N-02**)

## 4. Objective
Build a new read-only Admin Portal page consuming `GET /admin/v1/bedtime/analytics` (B-05), rendering adoption-rate trend, sleep-timer-ceiling distribution, and ritual-completion-rate trend via recharts, with date-range filtering and standard RBAC.

## 5. Business Requirements
- §8 Admin Requirements: "Bedtime Configuration Analytics (Read-only): Aggregate, privacy-safe view of bedtime-window adoption rates, average sleep-timer-ceiling settings, ritual-completion-rate trends — never exposing individual child detail."
- §9 (Admin AI prompt item 2): dashboard (recharts) showing adoption rate over time, distribution of sleep-timer-ceiling settings (histogram), ritual-completion-rate trend — NEVER exposing any individual `child_id`-level row.

## 6. Existing Architecture
Follows the same pattern as A.3's existing read-only admin analytics page (Download Manifest Health Monitor, `03-download-manifest-health-monitor.md`) — a new page under `src/app/(dashboard)/`, a dedicated `src/features/bedtime-analytics/` module, `RequirePermission`-gated, consuming a single read-only aggregate endpoint via React Query.

## 7. Existing Code to Reuse
- A.3's Download Manifest Health Monitor page structure (mirror its page/feature-module layout exactly, since it is the closest existing precedent: a read-only, recharts-based, aggregate-only admin analytics page)
- `src/shared/components/require-permission.tsx::RequirePermission`
- `src/shared/hooks/use-pagination-state.ts` (if date-range pagination/paging of trend data benefits from it)
- Existing recharts wrapper components already established in the Admin Portal (confirm and reuse existing chart-wrapper components rather than importing recharts primitives ad hoc, if such wrappers exist)

## 8. Files to Create
- `src/app/(dashboard)/bedtime/analytics/page.tsx`
- `src/features/bedtime-analytics/api/bedtime-analytics-repository.ts` — `BedtimeAnalyticsRepositoryImpl` (single `getAnalytics(dateRange, bucket)` method)
- `src/features/bedtime-analytics/hooks/use-bedtime-analytics.ts` (React Query)
- `src/features/bedtime-analytics/components/adoption-rate-trend-chart.tsx`
- `src/features/bedtime-analytics/components/sleep-timer-ceiling-histogram.tsx`
- `src/features/bedtime-analytics/components/ritual-completion-trend-chart.tsx`
- `src/features/bedtime-analytics/components/date-range-filter.tsx`
- `src/features/bedtime-analytics/types/bedtime-analytics.ts` — Zod schemas matching B-05's response shape (no `child_id`-shaped field anywhere in these types)

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `BEDTIME_ANALYTICS.GET`
- `src/shared/components/dashboard-shell.tsx` — nav item gated by the appropriate analytics-read permission

## 10. NextJS Requirements
- `AdoptionRateTrendChart`: line chart, X-axis = period (weekly buckets by default), Y-axis = adoption rate percentage.
- `SleepTimerCeilingHistogram`: bar chart, X-axis = ceiling-minute buckets (e.g., 5–15, 16–30, 31–45, 46–60, 60+), Y-axis = family count.
- `RitualCompletionTrendChart`: line chart, X-axis = date, Y-axis = completion rate percentage.
- `DateRangeFilter`: bounded date-range picker (matching B-05's server-side max-range cap, e.g., 12 months) plus a bucket-granularity selector (`daily`/`weekly`/`monthly`).
- All three charts render directly from B-05's response shape with zero client-side aggregation of per-child data (there is no per-child data to aggregate — the API only ever returns pre-aggregated series).
- Empty-data periods render an explicit "no data for this range" state per chart, not a broken/empty chart canvas.

## 11. Required API
**Admin API** — B-05 `GET /admin/v1/bedtime/analytics?start_date=&end_date=&bucket=`.

## 12. Authentication / Authorization
`useAdminSession()` for base auth; `RequirePermission` gating the page with the same analytics-read role B-05's backend enforces (confirm exact role name against B-05's implementation — likely a read-level analytics role, not `product_admin`).

## 13. Loading / Empty / Error States
Skeleton loaders for each chart while the query is in flight; per-chart empty state for zero-data ranges; page-level error state with retry if the aggregate fetch fails entirely.

## 14. Responsive UI / Accessibility
Charts stack vertically on narrow viewports; each chart includes accessible data-table fallback or ARIA labeling for screen readers (recharts accessibility layer or an accompanying visually-hidden data table, per whichever pattern the Admin Portal's existing chart components already establish).

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()` for chart labels and date formatting; RTL only if the Admin Portal's existing localization scope supports it (confirm, do not assume).

## 16. Security
- Read-only page; zero mutating actions.
- Structural guarantee: the TypeScript types backing this page's data have no `child_id` field, so even a backend regression exposing one would not be renderable without a corresponding frontend type/rendering change (defense in depth, though the primary guarantee lives in B-05's backend).

## 17. Testing
Unit: chart components render correctly given a fixture matching B-05's response shape; empty-data-state rendering. Integration: `RequirePermission` boundary test (insufficient role hides/redirects); date-range filter correctly re-triggers the query with updated params.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Types Matching B-05's Response Shape**
Objective: `bedtime-analytics.ts` types, structurally incapable of representing a `child_id` field. Files to create: `types/bedtime-analytics.ts`. Tests: schema shape test. Definition of Done: test passes.

**Task 02 — Implement `BedtimeAnalyticsRepositoryImpl`**
Objective: Single read method wrapping B-05's endpoint. Files to create: `api/bedtime-analytics-repository.ts`. Follow: A.3's Download Manifest Health Monitor repository pattern. Dependencies: Task 01. Tests: mocked-fetch test. Definition of Done: test passes.

**Task 03 — Implement `useBedtimeAnalytics` Hook**
Objective: React Query wrapper with date-range/bucket params. Files to create: `hooks/use-bedtime-analytics.ts`. Dependencies: Task 02. Definition of Done: hook wired correctly.

**Task 04 — Implement the Three Chart Components**
Objective: `AdoptionRateTrendChart`, `SleepTimerCeilingHistogram`, `RitualCompletionTrendChart`, each with an explicit empty-data state. Files to create: three component files. Dependencies: Task 01, existing chart-wrapper reuse (confirmed per §7). Tests: render-with-fixture tests, empty-state tests. Definition of Done: tests pass.

**Task 05 — Implement `DateRangeFilter`**
Objective: Bounded range picker + bucket selector, re-triggering the query on change. Files to create: `components/date-range-filter.tsx`. Dependencies: Task 03. Tests: filter-change-retriggers-query test. Definition of Done: test passes.

**Task 06 — Implement the Page**
Objective: Compose all components with loading/empty/error states, `RequirePermission`-gated. Files to create: `app/(dashboard)/bedtime/analytics/page.tsx`. Dependencies: Tasks 03–05. Definition of Done: full-page smoke test against a mocked API passes.

**Task 07 — Add Full Test Suite**
Objective: Complete coverage per §17. Definition of Done: all green in CI.

**Task 08 — Final Code Review**
Objective: Confirm no code path in this module can render a `child_id` or other individual identifier; confirm the page is genuinely read-only (no mutating API calls anywhere in the module). Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] All three charts render correctly from B-05's pre-aggregated response
- [ ] No TypeScript type or rendered UI element in this module can represent a `child_id`
- [ ] Empty-data ranges render an explicit "no data" state per chart, not a broken canvas
- [ ] Date-range filter correctly bounded and re-triggers the query on change
- [ ] `RequirePermission` correctly gates the page at the appropriate analytics-read role
- [ ] Zero mutating API calls exist anywhere in this module

## 20. Definition of Done
Product/admin stakeholders can view bedtime-window adoption, sleep-timer-ceiling calibration, and ritual-completion trends on a dedicated, read-only, RBAC-gated dashboard, with a structural guarantee that no individual child's data can ever be rendered.
