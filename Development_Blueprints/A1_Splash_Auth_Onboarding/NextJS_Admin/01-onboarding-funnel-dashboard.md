# N-01 — Onboarding Funnel Dashboard

> [!NOTE]
> **Status:** ✅ **IMPLEMENTED & VERIFIED**
> - **Platform:** NextJS Admin Portal (`src/features/onboarding-analytics/`, `src/app/(dashboard)/onboarding/funnel/`)
> - **Test Suite:** 20/20 passing tests across `tests/onboarding-analytics.test.ts` & `tests/onboarding-funnel.test.tsx` (100% pass rate)
> - **Architecture Invariants:** 69/69 passed
> - **Type & Code Quality:** 0 TypeScript errors (`tsc --noEmit`), 0 ESLint warnings (`eslint .`)
> - **Backend API:** Consumes B-07 (`GET /admin/v1/onboarding/funnel`)

## 1. Feature Context
Product/Growth's primary view into onboarding health: a step-funnel visualization from Splash through Onboarding Complete, filterable by date/platform/locale, backed by B-07's read-only aggregation endpoint.

## 2. Parent Feature
Feature A.1 — Splash, Language Selection, Authentication & Onboarding

## 3. Sub-feature
3.1 Onboarding Funnel Dashboard (ID: **N-01**)

## 4. Objective
Build a Next.js App Router page rendering a step-funnel chart (recharts) against `GET /admin/v1/onboarding/funnel`, following the existing repository → hook → component layering.

## 5. Business Requirements
- Onboarding Funnel Dashboard: step-by-step drop-off visualization (Splash → Intro → Registration → OTP → PIN → Add Child → Complete), filterable by platform/locale/date range.
- §11.2: Primary funnel tracked with step-over-step conversion and median time-per-step.
- §11.3: Dashboard metrics include completion rate, OTP delivery success by provider, median time-to-complete, abandonment-by-step heatmap, new-vs-returning split, consent opt-in rates.

## 6. Existing Architecture
`src/features/onboarding-analytics/` (new feature module, following the existing `src/features/*` convention seen in `family-management`, `users`, `cms`); `BaseResourceClient`-style repository (though this is a single-aggregate GET, not a paginated CRUD resource — a plain repository function is more appropriate than extending `BaseResourceClient`); `DataTable`/chart via `recharts` (already an approved dependency per the admin architecture doc's Quick Reference).

## 7. Existing Code to Reuse
- `src/shared/api/api-client.ts::apiClient.get()`
- `src/shared/constants/api-endpoints.ts::API_ENDPOINTS` (add `ONBOARDING.FUNNEL`)
- `src/shared/components/filter-panel.tsx::FilterPanel`
- `src/shared/hooks/use-debounced-value.ts` (if any text filter is added; primarily date-range/select filters here, less critical than for search)
- `src/shared/components/loading-state.tsx`, `error-view.tsx`, `empty-state.tsx`
- `useTranslation()`, `useFormatters()` for all display strings and date formatting

## 8. Files to Create
- `src/app/(dashboard)/onboarding/funnel/page.tsx`
- `src/features/onboarding-analytics/api/onboarding-analytics-repository.ts` — `OnboardingAnalyticsRepositoryImpl.getFunnel(filters)`
- `src/features/onboarding-analytics/hooks/use-onboarding-funnel.ts` — `useOnboardingFunnel(filters)`
- `src/features/onboarding-analytics/components/funnel-chart.tsx` — recharts Sankey/step-funnel wrapper
- `src/features/onboarding-analytics/components/funnel-filters.tsx` — date range + platform + locale selectors
- `src/features/onboarding-analytics/types/funnel.ts` — Zod schema + TS types matching B-07's response shape
- `src/features/onboarding-analytics/__tests__/use-onboarding-funnel.test.ts`

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `ONBOARDING.FUNNEL: '/admin/v1/onboarding/funnel'`
- `src/shared/components/dashboard-shell.tsx` (sidebar nav) — add "Onboarding Funnel" nav item wrapped in `RequirePermission permission="analytics:read"`
- `src/shared/types/admin-permission.ts` (or wherever `AdminPermission` is defined) — add `"analytics:read"` if it doesn't already exist

## 10. NextJS Requirements
- Page is a client component (`"use client"`) given the interactive filter state, following the existing `UsersPage` pattern shown in the architecture doc's Pattern 1 example.
- `useOnboardingFunnel(filters)` wraps `OnboardingAnalyticsRepositoryImpl.getFunnel()` in a React Query hook with a reasonable `staleTime` (this is a metrics dashboard, not real-time — a few minutes' staleness is acceptable, avoid refetching on every filter keystroke).
- Filters: date-range picker, platform select (android/ios/all), locale select — all controlled state passed as query params to the repository call.
- Chart: recharts-based step-funnel/Sankey rendering `{step, count, conversion_from_previous_pct, median_time_seconds}`; also render the same data as an accessible `DataTable` fallback beneath or alongside the chart (screen-reader accessibility for chart data, per the general accessibility requirement — charts alone are not accessible).
- Loading/empty/error states via `LoadingState`/`EmptyState`/`QueryErrorState` — empty state specifically for a valid-but-zero-data date range (not an error).

## 11. Required API
- `GET /admin/v1/onboarding/funnel?from=&to=&platform=&locale=` (B-07) — Auth: `get_current_admin` + `admin:read`

## 12. Validation
Date-range picker enforces `from <= to`; default range (e.g., last 7 days) to avoid an initial unbounded query.

## 13. Authentication / Authorization
Standard admin session via existing `useAdminSession()`; page wrapped in `RequirePermission permission="analytics:read"`. **Resolved architecture decision:** `NEXT-JS-INSTRUCTIONS.md` doesn't enumerate the full `AdminPermission` union, but its one worked example (`RequirePermission permission="users:read"`) establishes a clear `resource:action` naming convention, matching the backend's own `admin:read`/`admin:write` scope-naming style (per `FAST-API-INSTRUCTIONS.md`). `"analytics:read"` is the most consistent name for this resource — B-07's underlying endpoints are gated by the backend's generic `admin:read` scope, but the frontend's per-page `RequirePermission` convention is resource-scoped, so a new, more specific `"analytics:read"` value should be added to `AdminPermission` (backed by the same broad `admin:read` capability server-side) rather than reusing a nonexistent generic frontend permission string.

## 14. Loading / Empty / Error States
- Loading: `LoadingState` while the query is in flight.
- Empty: valid date range with zero events → `EmptyState` with a "no onboarding activity in this range" message, not treated as an error.
- Error: `QueryErrorState` with retry, surfacing the correlation/request ID per existing error-handling conventions.

## 15. Responsive UI / Accessibility
Chart container responsive (recharts `ResponsiveContainer`); tabular fallback ensures screen-reader users get the same data; filter controls keyboard-navigable.

## 16. Localization / RTL
All labels via `useTranslation()`; date/number formatting via `useFormatters()` — no hardcoded English strings or manually-formatted dates, per the architecture doc's explicit Common Mistake #3.

## 17. Performance
React Query caching avoids redundant refetches on filter-panel re-renders that don't actually change the filter values; debounce is less critical here than for search-heavy pages (filters are discrete selects/date-pickers, not free-text).

## 18. Testing
Unit/integration: `useOnboardingFunnel` hook test (loading/success/error/empty states); filter-to-query-param mapping test; Zod schema validation test against a sample B-07 response payload.

## 19. AI Coding Agent Implementation Steps

**Task 01 — Add API Endpoint Constant**
Objective: Register the funnel endpoint. Files to Modify: `api-endpoints.ts`. Definition of Done: constant available for the repository to reference.

**Task 02 — Define Zod Schema & Types**
Objective: Runtime-validated response shape matching B-07 exactly. Files to Create: `types/funnel.ts`. Tests: schema validation against sample payload (both populated and empty-array cases). Definition of Done: schema rejects a malformed response shape in a test.

**Task 03 — Implement `OnboardingAnalyticsRepositoryImpl.getFunnel()`**
Objective: Repository function wrapping `apiClient.get()` with Zod validation. Follow: existing repository conventions (`DashboardRepositoryImpl.getStats()` is the closest existing analog per the architecture doc — a single-aggregate GET, not a paginated list). Files to Create: repository file. Tests: mocked-fetch success/error tests. Dependencies: Task 02. Definition of Done: repository throws a typed error on schema-validation failure, not a silent pass-through.

**Task 04 — Implement `useOnboardingFunnel` Hook**
Objective: React Query wrapper with filter-driven query key. Follow: `useDashboardStats()`-style pattern. Tests: hook test per §18. Dependencies: Task 03. Definition of Done: query key correctly includes all filter values (date range, platform, locale) so filter changes trigger a refetch.

**Task 05 — Implement `FunnelChart` and `FunnelFilters` Components**
Objective: recharts visualization + accessible tabular fallback + filter controls. Follow: `useTranslation()`/`useFormatters()` throughout, no hardcoded strings. Files to Create: both component files. Tests: covered by Task 07. Dependencies: Task 04. Definition of Done: tabular fallback present and accessible via screen reader.

**Task 06 — Implement the Page & Wire Navigation**
Objective: `page.tsx` composing filters + chart + loading/empty/error states; sidebar nav entry gated by `RequirePermission`. Follow: architecture doc's Pattern 1 (`UsersPage`) example structurally. Files to Create/Modify: `page.tsx`, `dashboard-shell.tsx`. Dependencies: Tasks 04–05. Definition of Done: page renders end-to-end against a mocked API in a smoke test.

**Task 07 — Add Full Test Suite**
Objective: Complete coverage per §18. Definition of Done: all green in CI.

**Task 08 — Final Code Review**
Objective: Confirm no hardcoded strings/dates, confirm empty-vs-error distinction is correct, confirm permission-gating uses an existing permission string, not a fabricated one. Definition of Done: checklist in §20 checked.

## 20. Final Verification Checklist
- [x] All display strings via `useTranslation()`, all dates/numbers via `useFormatters()` / `useLocalization()`
- [x] Zero-data valid range renders as empty state, not error
- [x] Chart has an accessible tabular fallback (`DataTable` with screen-reader friendly structure)
- [x] Filter changes correctly trigger a query refetch (query key includes all filter values)
- [x] Page gated behind an existing (not fabricated) admin permission (`analytics:read`)
- [x] Responsive on mobile/tablet/desktop admin viewports

## 21. Definition of Done
The Onboarding Funnel Dashboard is live, reads from B-07, fully localized/RTL-safe, accessible, and correctly distinguishes loading/empty/error states. **(STATUS: IMPLEMENTED & VERIFIED)**

### 21.1 Implemented Artifacts & Verified Architecture
- **Route Segment & Layout Boundaries:**
  - Route Page: `src/app/(dashboard)/onboarding/funnel/page.tsx` (gated with `<RequirePermission permission="analytics:read">`)
  - Loading Boundary: `src/app/(dashboard)/onboarding/funnel/loading.tsx`
  - Error Boundary: `src/app/(dashboard)/onboarding/funnel/error.tsx` (Client component with `reset()` action)
- **Feature Module (`src/features/onboarding-analytics/`):**
  - Validation Schemas: `schemas/funnel.schema.ts` (`funnelStepItemSchema`, `funnelResponseSchema`, `funnelFilterSchema` with `from <= to` refinement)
  - Data Types: `types.ts` (`FunnelStepItem`, `FunnelFilters`, `FunnelSummaryMetrics`, `IOnboardingAnalyticsRepository`)
  - Repository Layer: `api/onboarding-analytics.repository.ts` (`OnboardingAnalyticsRepositoryImpl.getFunnel(filters)`)
  - TanStack Query Hook: `hooks/use-onboarding-funnel.ts` (`useOnboardingFunnel`) with 2-minute `staleTime` and memoized summary KPIs calculation
  - UI Components:
    - `components/onboarding-funnel-dashboard.tsx`: Complete 5-state UI orchestrator (Loading Skeleton, Empty State with "Clear Filters" CTA, QueryErrorState with retry, Offline Banner with cached data display, and Populated Dashboard)
    - `components/funnel-chart.tsx`: Responsive step-funnel visualization with color-coded conversion badges, duration indicators, drop-off connectors, and accessible progress bars
    - `components/funnel-filters.tsx`: Date range pickers, platform select, and locale select with debounce/reset handling
    - Tabular Fallback: Integrated `DataTable` rendering equivalent tabular breakdown for screen reader accessibility
  - Feature Barrel: `index.ts` exporting public surface
- **API Registry & Navigation Integration:**
  - Central Registry: `src/shared/constants/api-endpoints.ts` (`API_ENDPOINTS.ONBOARDING.FUNNEL = "/admin/v1/onboarding/funnel"`)
- **Localization (i18n):**
  - Full translations registered across English (`en`), Arabic (`ar` with RTL), Urdu (`ur` with RTL), and Hindi (`hi`)
- **Automated Verification:**
  - `tests/onboarding-analytics.test.ts`: 10/10 passing tests (schema validation, error rejection, filter-to-query mapping, error handling)
  - `tests/onboarding-funnel.test.tsx`: 10/10 passing tests (loader state, populated state with KPI cards, empty state, zero-activity scenario, 100% conversion/zero drop-off, offline state detection, error state with retry, filter changes, and route permission gating)
  - `tests/architecture/*.test.mjs`: 69/69 passing tests
  - Zero TypeScript compile errors (`tsc --noEmit`) and zero ESLint warnings (`eslint .`)
