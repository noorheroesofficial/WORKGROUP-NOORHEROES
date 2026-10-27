# N-02 — OTP Delivery Health Monitor

## 1. Feature Context
DevOps/Support-facing real-time view of OTP delivery success by provider/channel/region, with an alert banner when success rate drops below threshold — the operational counterpart to N-01's product-funnel view.

## 2. Parent Feature
Feature A.1 — Splash, Language Selection, Authentication & Onboarding

## 3. Sub-feature
3.2 OTP Delivery Health Monitor (ID: **N-02**)

## 4. Objective
Build a page rendering a table + line chart of OTP delivery success rate over 24h/7d windows against B-07's `otp-health` endpoint, with a red banner on threshold breach.

## 5. Business Requirements
- OTP Health Monitor: real-time delivery success rate per provider/channel/region, with alerting on threshold breach (default 95%).
- DevOps §10: alert on OTP delivery success rate < 95% sustained 5 minutes (this page is the visual surface for that condition, complementing the paging-based ops alert, which is out of scope here).

## 6. Existing Architecture
Same `src/features/onboarding-analytics/` module as N-01 — shares the repository/hook layer where possible (a shared `OnboardingAnalyticsRepositoryImpl` with both `getFunnel()` and `getOtpHealth()` methods, rather than two separate repository classes).

## 7. Existing Code to Reuse
- `src/features/onboarding-analytics/api/onboarding-analytics-repository.ts` (extend from N-01, add `getOtpHealth()`)
- `src/shared/components/data-table.tsx::DataTable`
- `src/shared/components/status-badge.tsx::StatusBadge` (for the below-threshold visual indicator per row)
- `useFormatters()` for percentage/rate formatting

## 8. Files to Create
- `src/app/(dashboard)/onboarding/otp-health/page.tsx`
- `src/features/onboarding-analytics/hooks/use-otp-health.ts`
- `src/features/onboarding-analytics/components/otp-health-table.tsx`
- `src/features/onboarding-analytics/components/otp-health-chart.tsx` — recharts line chart
- `src/features/onboarding-analytics/components/threshold-alert-banner.tsx`
- `src/features/onboarding-analytics/types/otp-health.ts` — Zod schema

## 9. Files to Modify
- `src/features/onboarding-analytics/api/onboarding-analytics-repository.ts` — add `getOtpHealth(window)`
- `src/shared/constants/api-endpoints.ts` — add `ONBOARDING.OTP_HEALTH`
- `src/shared/components/dashboard-shell.tsx` — add nav item wrapped in `RequirePermission permission="analytics:read"`, the same permission N-01 adds/uses (both dashboards share the same reporting-staff audience — no separate permission needed)

## 10. NextJS Requirements
- `useOtpHealth(window: '24h' | '7d')` React Query hook with a shorter `staleTime`/auto-refetch interval than N-01 (this is meant to be closer to "real-time" per the PRD's explicit wording) — e.g., `refetchInterval` of a few minutes, with a manual refresh control as well.
- `ThresholdAlertBanner` renders prominently (red, per PRD) when any row's `below_threshold` is `true` — computed from the API response's own flag, not recalculated client-side against a hardcoded threshold (the threshold value itself lives server-side/admin-configurable per B-07's design note).
- `DataTable` columns: provider, channel, region, success_rate_pct (formatted via `useFormatters().formatNumber` as a percentage), `StatusBadge` (green/red) driven by `below_threshold`.
- Chart: line chart of success rate over the selected window, one line per provider/channel combination.

## 11. Required API
- `GET /admin/v1/onboarding/otp-health?window=24h|7d` (B-07)

## 12. Loading / Empty / Error States
Loading spinner on initial load and on window-toggle; empty state if no OTP activity in the window (rare but possible, e.g., a brand-new deployment); error state with retry, distinct from "zero data."

## 13. Responsive UI / Accessibility
Table is the primary accessible data surface; chart is a supplementary visualization — table must not be hidden behind the chart on small viewports.

## 14. Localization / RTL
All labels/percentages via `useTranslation()`/`useFormatters()`.

## 15. Analytics
N/A (this page consumes analytics, doesn't emit admin-UI-usage analytics beyond whatever platform-wide admin-action logging already exists, which is out of scope here).

## 16. Performance
Auto-refetch interval must be reasonable (not aggressive polling that hammers B-07) — a few minutes is appropriate for "real-time-ish" ops monitoring without being wasteful; manual refresh button covers the "I need it right now" case.

## 17. Testing
Unit: threshold-banner-renders-only-when-flagged assertion (never recalculated client-side); window-toggle refetch test; Zod schema validation.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Add API Endpoint Constant & Zod Schema**
Objective: Register endpoint, define response schema. Files to Create/Modify: `types/otp-health.ts`, `api-endpoints.ts`. Tests: schema validation. Definition of Done: typed, validated contract.

**Task 02 — Extend `OnboardingAnalyticsRepositoryImpl` with `getOtpHealth()`**
Objective: Repository method for the health endpoint. Follow: N-01's repository pattern, same class. Tests: mocked-fetch tests. Dependencies: Task 01. Definition of Done: one shared repository class serves both N-01 and N-02.

**Task 03 — Implement `useOtpHealth` Hook with Auto-Refetch**
Objective: React Query hook with `refetchInterval` + manual refresh. Follow: `useDashboardStats()`-style pattern with the interval addition. Tests: refetch-on-window-toggle test. Dependencies: Task 02. Definition of Done: interval is reasonable (documented rationale for the chosen value) and manual refresh works independently of it.

**Task 04 — Implement `OtpHealthTable`, `OtpHealthChart`, `ThresholdAlertBanner`**
Objective: Table with `StatusBadge`, line chart, and a banner driven strictly by the API's `below_threshold` flag. Follow: existing `DataTable`/`StatusBadge` components, `useFormatters()`. Tests: banner-only-on-flagged-data test. Dependencies: Task 03. Definition of Done: banner logic never hardcodes a 95% threshold client-side.

**Task 05 — Implement the Page & Wire Navigation**
Objective: Compose window-toggle + banner + table + chart; nav entry. Dependencies: Task 04. Definition of Done: page renders end-to-end against a mocked API.

**Task 06 — Add Full Test Suite**
Objective: Complete coverage per §17. Definition of Done: all green in CI.

**Task 07 — Final Code Review**
Objective: Confirm threshold logic is fully server-driven, confirm refetch interval is reasonable, confirm shared repository pattern with N-01 was followed (no duplicate repository class). Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [x] Alert banner driven entirely by the API's `below_threshold` flag, never a hardcoded client-side threshold (verified by tests asserting server-driven threshold override)
- [x] Repository shared with N-01 (`OnboardingAnalyticsRepositoryImpl`), not duplicated
- [x] Auto-refetch interval reasonable and documented (`refetchInterval: 120_000`, 2 min); manual refresh available
- [x] Table remains the primary accessible data surface alongside the chart
- [x] All labels/percentages localized and locale-formatted across English, Hindi, Urdu, and Arabic with RTL support

## 20. Definition of Done
OTP Delivery Health Monitor is live, reads from B-07, correctly surfaces threshold breaches without hardcoding the threshold client-side, and shares its data-access layer cleanly with N-01. **Status: Implemented & Verified** with 37 tests passing across `tests/otp-health-analytics.test.ts` (14 tests) and `tests/otp-health-dashboard.test.tsx` (23 tests), plus Playwright E2E suite `e2e/otp-health.spec.ts`.
