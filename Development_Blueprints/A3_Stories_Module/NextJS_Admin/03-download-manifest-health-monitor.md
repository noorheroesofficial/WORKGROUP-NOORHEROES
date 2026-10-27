# N-03 — Download Manifest Health Monitor

## 1. Feature Context
A simple read-only operational dashboard: manifest generation success/failure rate over time, sourced from B-15. Zero mutation UI exists on this page — it exists purely so ops/support can spot a degrading download pipeline before it becomes a support-ticket flood.

## 2. Parent Feature
Feature A.3 — Stories Module (Animated Storytelling System)

## 3. Sub-feature
3.3 Download Manifest Health Monitor (ID: **N-03**)

## 4. Objective
Build a read-only recharts dashboard against `GET /admin/v1/downloads/health` (B-15), with a date-range selector and a table fallback for accessibility.

## 5. Business Requirements
- §8: read-only view of manifest generation health/failure rates.
- §9: read-only dashboard (recharts), sourced from `GET /admin/v1/downloads/health`.

## 6. Existing Architecture
`src/features/download-health/` module. Recharts is an approved charting library per the existing Admin Portal conventions (already used elsewhere for dashboard metrics — reuse the existing chart wrapper component if one exists rather than a bare `recharts` import).

## 7. Existing Code to Reuse
- Existing dashboard chart wrapper component (confirm exact name/location — e.g., if `DashboardStats`/`useDashboardStats()` pattern already wraps recharts elsewhere, mirror it)
- `src/shared/components/loading-state.tsx::LoadingState`
- `src/shared/components/empty-state.tsx::EmptyState`

## 8. Files to Create
- `src/app/(dashboard)/stories/download-health/page.tsx`
- `src/features/download-health/api/download-health-repository.ts`
- `src/features/download-health/hooks/use-download-health.ts`
- `src/features/download-health/components/download-health-chart.tsx`
- `src/features/download-health/components/download-health-table.tsx` — accessible tabular fallback of the same data
- `src/features/download-health/types/health-timeseries.ts` — Zod schema

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `DOWNLOAD_HEALTH.GET`
- `src/shared/components/dashboard-shell.tsx` — nav item (read-scope, no special role beyond standard admin read access unless the codebase convention says otherwise)

## 10. NextJS Requirements
- `DownloadHealthChart`: line/bar chart of success vs. failure counts per time bucket, using the existing recharts wrapper pattern.
- `DownloadHealthTable`: the same underlying data rendered as an accessible table — always present (not just a toggle), since a chart-only view fails screen-reader accessibility.
- Date-range selector re-triggers the `useDownloadHealth()` query; no client-side re-aggregation of raw event data — this page only ever renders what B-15 already aggregated.

## 11. Required API
**Admin API (read-only)** — B-15: `GET /admin/v1/downloads/health`.

## 12. Authentication / Authorization
`useAdminSession()` base auth; standard admin read-scope gating (no special role beyond general admin access, since the endpoint itself is read-only per B-15).

## 13. Loading / Empty / Error States
Chart-loading skeleton; empty state for a date range with zero data; error state with retry.

## 14. Responsive UI / Accessibility
Chart resizes responsively; the always-present table fallback ensures screen-reader users get the same information as the visual chart.

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()` for date labels and counts.

## 16. Security
Read-only page — no mutation capability, no elevated-security considerations beyond standard admin authentication.

## 17. Testing
Unit: date-range-selector re-fetch behavior, empty-range handling. UI: chart and table render the identical underlying data (a consistency test comparing rendered chart data points against rendered table rows).

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schema & Add API Endpoint**
Objective: `health-timeseries.ts` response schema. Files: `types/health-timeseries.ts`, `api-endpoints.ts`. Tests: schema validation. Definition of Done: schema used by Task 03.

**Task 02 — Implement `DownloadHealthRepositoryImpl`**
Objective: Repository wrapping `apiClient.get()` for B-15's endpoint with date-range params. Tests: mocked-fetch test. Dependencies: Task 01. Definition of Done: test passes.

**Task 03 — Implement `useDownloadHealth` Hook**
Objective: React Query hook re-fetching on date-range change. Dependencies: Task 02. Tests: re-fetch-on-range-change test. Definition of Done: test passes.

**Task 04 — Implement `DownloadHealthChart` and `DownloadHealthTable`**
Objective: Chart + always-present accessible table rendering identical data. Follow: existing recharts wrapper pattern. Dependencies: Task 03. Tests: chart-table data-consistency test. Definition of Done: test passes.

**Task 05 — Implement the Page**
Objective: Compose date-range selector + chart + table + loading/empty/error states. Dependencies: Task 04. Definition of Done: page smoke test passes against a mocked API.

**Task 06 — Add Full Test Suite**
Objective: Complete coverage per §17. Definition of Done: all green in CI.

**Task 07 — Final Code Review**
Objective: Confirm zero mutation controls exist anywhere on this page; confirm the table fallback is always rendered, not gated behind a toggle. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] Page is strictly read-only — zero mutation controls anywhere
- [ ] Chart and table render the exact same underlying data (no independent re-aggregation)
- [ ] Table fallback always present for accessibility, not toggle-gated
- [ ] Date-range selector correctly re-fetches from B-15
- [ ] Empty date range shows a valid empty state, not an error

## 20. Definition of Done
Ops/support have an accessible, accurate, read-only view of download-manifest health sourced directly from B-15 — with zero risk of this page ever becoming a mutation surface.
