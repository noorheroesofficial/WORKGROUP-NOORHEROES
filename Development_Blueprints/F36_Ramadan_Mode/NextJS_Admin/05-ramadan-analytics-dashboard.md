# N-05 — Ramadan Analytics Dashboard

## 1. Feature Context
A read-only metrics dashboard tracking the season's health against its own success targets — 70% journey-completion, 40% report-share rate, 15-25% Day 28-30 conversion — giving Growth/Engagement and Content leadership visibility without any write capability on this screen.

## 2. Parent Feature
F.36 — Ramadan Mode

## 3. Sub-feature
3.5 Ramadan Analytics Dashboard (ID: **N-05**)

## 4. Objective
Build a read-only dashboard displaying nightly completion-rate trend, fasting-approach distribution, certificate/Eid-card share rates, and Day 28-30 conversion rate against target.

## 5. Business Requirements
- §8: Ramadan Analytics Dashboard (Read-only) — completion rates, fasting-approach distribution, conversion performance.
- §9 Admin AI prompt item 5: read-only metrics dashboard.
- §11.2 Funnel Analysis: `ramadan_home_themed_viewed` → `ramadan_journey_map_viewed` → `ramadan_night_mission_completed` (repeated) → `ramadan_certificate_generated`; separately, `ramadan_conversion_card_shown` → `ramadan_conversion_card_converted`.
- §11.3 Dashboard Metrics: nightly completion-rate trend, fasting-approach distribution, certificate/Eid-card share rates, Day 28-30 conversion rate against the 15-25% target.
- §1.4 Success Metrics: the four target figures this dashboard exists to surface.

## 6. Existing Architecture
`src/features/ramadan/analytics-dashboard/`, following `DashboardRepositoryImpl`/`useDashboardStats`'s existing read-only-metrics pattern (per `NEXT-JS-INSTRUCTIONS.md` §3/§4) rather than a new dashboard architecture.

## 7. Existing Code to Reuse
- `DashboardRepositoryImpl` / `useDashboardStats` structural pattern (reference, not literal reuse — this is a distinct metrics set)
- `useFormatters` (for rate/percentage formatting)
- `LoadingState`, `ErrorView`, `EmptyState`
- Existing chart components if the Admin Portal has an established charting library — confirm before introducing a new one

## 8. Files to Create
- `src/app/(dashboard)/ramadan/analytics/page.tsx`
- `src/features/ramadan/analytics-dashboard/api/ramadan-analytics-resource-client.ts`
- `src/features/ramadan/analytics-dashboard/hooks/use-ramadan-analytics.ts`
- `src/features/ramadan/analytics-dashboard/components/completion-rate-chart.tsx`
- `src/features/ramadan/analytics-dashboard/components/fasting-approach-distribution.tsx`
- `src/features/ramadan/analytics-dashboard/components/conversion-funnel-card.tsx`
- `src/features/ramadan/analytics-dashboard/components/share-rate-summary.tsx`
- `src/features/ramadan/analytics-dashboard/types/ramadan-analytics.ts`

## 9. Files to Modify
- `src/shared/components/dashboard-shell.tsx` — add "Analytics" nav entry under Ramadan

## 10. NextJS Requirements
- **Page/Route:** `/ramadan/analytics`, entirely read-only (no mutation hooks anywhere in this module).
- **Component:** `CompletionRateChart` (nightly trend line), `FastingApproachDistribution` (breakdown by approach), `ConversionFunnelCard` (the two funnels from §11.2, actual vs. 15-25% target), `ShareRateSummary` (certificate/Eid-card share rates vs. the 40% target).
- **Filtering:** region and date-range filters.
- **Loading/Empty/Error State:** per-chart loading/empty/error handling so one metric's failure doesn't block the others.
- **Responsive UI/Accessibility:** charts include a data-table fallback or sufficient alt-text/aria-labels for non-visual access (per §22.7 Accessibility scenario requirement pattern used elsewhere in this instruction set).

## 11. API Contract
### Proposed Analytics Summary Endpoint (pending confirmation)
Not enumerated in PRD §3.4. Following the existing `useDashboardStats()`/`DashboardRepositoryImpl` pattern (§3/§4 of `NEXT-JS-INSTRUCTIONS.md`) — a single summary read rather than four separate round-trips — this blueprint proposes:

`GET /v1/admin/ramadan/analytics/summary?region=&date_from=&date_to=` → `200 { nightly_completion_trend: [{ night, completion_rate }], fasting_approach_distribution: { fasted_full, fasted_practice, education_only }, conversion_funnel: { home_viewed, journey_map_viewed, night_completed, certificate_generated, conversion_card_shown, conversion_card_converted }, share_rates: { certificate_share_rate, eid_card_share_rate } }`
- **Auth:** `get_current_admin`. **Authz:** `require_admin_scope("content_editor")` or `require_admin_scope("product_admin")` — read-only, per §8's CRUD table.
- Sourced from the platform's existing Analytics Event Bus (§3.2) — this endpoint aggregates pre-computed metrics server-side; the Admin Portal never computes rates from raw event data client-side.

**Mark PROPOSED in code review until a real contract is signed off** — `RamadanAnalyticsResourceClient` is written against this single-summary shape but can be split into per-metric calls later without a component-layer rewrite if the confirmed contract differs.

## 12. Database Requirements
N/A directly — reads from the platform's existing analytics/event store via its backend API, not `ramadan_*` operational tables directly.

## 13. Validation
N/A — read-only, no forms.

## 14. Authentication
Standard Admin Portal session.

## 15. Authorization
`RequirePermission permission="ramadan_analytics:read"` — behind `content_editor`/`product_admin` per §8, read-only (no write permission needed or granted on this page).

## 16. Error Handling
Per-chart `QueryErrorState` isolation — a single metric's fetch failure shows an inline error for that chart only, the rest of the dashboard remains functional.

## 17. Localization
All chart labels, legends, and metric names via `useTranslation()`; numeric/percentage formatting via `useFormatters()`.

## 18. RTL
Chart and legend layout direction-aware for Arabic/Urdu.

## 19. Analytics
This page displays analytics; it does not itself require additional instrumentation beyond standard Admin Portal page-view tracking if that pattern exists elsewhere.

## 20. Performance
Aggregate metrics fetched pre-computed from the backend (not computed client-side from raw event data); charts virtualize/paginate if the nightly-trend dataset grows large; region/date-range filter changes are debounced.

## 21. Caching
React Query caching with a reasonable staleness window (metrics don't need real-time freshness) — confirm an appropriate `staleTime` given this is a monitoring, not operational, surface.

## 22. Testing
Component tests: each chart renders correctly from mocked aggregate data, including zero-data/empty states. Integration test: filter changes (region/date-range) correctly refetch and update all four chart components independently.

## 23. Documentation
Inline JSDoc noting this module is strictly read-only — any future write capability belongs in a different sub-feature, not bolted onto this dashboard.

## 24. AI Coding Agent Implementation Steps

**Task 01 — Implement Against the Proposed Analytics Summary Contract**
Objective: Build to §11's proposed single-summary shape; flag for a joint frontend/backend/analytics contract review before production release. Definition of Done: contract documented in code comments; review flagged in the PR description.

**Task 02 — Define Types**
Objective: `NightlyCompletionPoint`, `FastingApproachDistribution`, `ConversionFunnelMetrics`, `ShareRateMetrics`. Files to Create: `types/ramadan-analytics.ts`. Definition of Done: types compile.

**Task 03 — Implement `RamadanAnalyticsResourceClient`**
Objective: Read-only client for the four metric groups. Files to Create: `api/ramadan-analytics-resource-client.ts`. Dependencies: Task 01, Task 02. Tests: repository unit tests. Definition of Done: tests pass.

**Task 04 — Implement `useRamadanAnalytics` Hook**
Objective: React Query hook(s) for region/date-range-filtered metrics. Files to Create: `hooks/use-ramadan-analytics.ts`. Dependencies: Task 03. Tests: hook tests. Definition of Done: tests pass.

**Task 05 — Build `CompletionRateChart` and `FastingApproachDistribution`**
Objective: Nightly trend and approach-breakdown visualizations with accessible fallbacks. Files to Create: `components/completion-rate-chart.tsx`, `components/fasting-approach-distribution.tsx`. Dependencies: Task 04. Tests: rendering/empty-state tests. Definition of Done: tests pass.

**Task 06 — Build `ConversionFunnelCard` and `ShareRateSummary`**
Objective: Funnel visualization against the 15-25% target; share-rate vs. 40% target. Files to Create: `components/conversion-funnel-card.tsx`, `components/share-rate-summary.tsx`. Dependencies: Task 04. Tests: target-comparison rendering tests. Definition of Done: tests pass.

**Task 07 — Build the Page with Filters and Wire Navigation**
Objective: `/ramadan/analytics` page, region/date-range filters. Files to Create: `app/(dashboard)/ramadan/analytics/page.tsx`. Files to Modify: `dashboard-shell.tsx`. Dependencies: Task 05, Task 06. Tests: filter-refetch integration test. Definition of Done: test passes.

**Task 08 — Add Localization, Accessibility Fallbacks, and Full Test Suite**
Objective: Complete §17/§10 accessibility/§22 coverage. Definition of Done: all green in CI.

**Task 09 — Final Code Review**
Objective: Confirm zero mutation capability exists anywhere in this module. Definition of Done: checklist in §26 checked.

## 25. Definition of Done
Leadership has clear, filterable, accessible read-only visibility into every one of the season's success-metric targets, with zero write capability anywhere on the page.

## 26. Final Verification Checklist
- [ ] Analytics summary built against the proposed §11 contract, flagged for real sign-off before production release
- [ ] Zero mutation/write capability anywhere in this module
- [ ] Each chart isolates its own loading/error/empty state independently
- [ ] All four §1.4 target metrics represented and comparable against their targets
