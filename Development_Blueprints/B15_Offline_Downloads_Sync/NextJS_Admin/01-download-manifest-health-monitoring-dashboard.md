# N-01 — Download Manifest Health Monitoring Dashboard

## 1. Feature Context
Part of Feature B.15 (Offline Downloads & Sync). Read-only operational visibility for `product_admin`/`trust_safety` into manifest-issuance health — the human-facing counterpart to B-07's automated alerting.

## 2. Parent Feature
B.15 — Offline Downloads & Sync

## 3. Sub-feature
N-01 — Download Manifest Health Monitoring Dashboard

## 4. Objective
Build a read-only dashboard showing manifest issuance success/failure rate, cap-rejection trend, and signed-URL expiry-refetch rate over a selectable time window, restricted to `product_admin`/`trust_safety`.

## 5. Business Requirements
- §8 Admin Requirements: Download Manifest Health Monitor (read-only) — issuance success/failure rates, cap-rejection rates, signed-URL-expiry retry rates.
- CRUD permissions: read-only behind `product_admin`/`trust_safety`.
- DevOps §10: this dashboard is the human-facing counterpart to the backend's automated download-failure-rate-spike alerting.

## 6. Existing Architecture
New page under `src/features/downloads/`, reusing the existing `recharts`-based dashboard pattern already established for other admin metrics pages (per `useDashboardStats`'s existing precedent in `NEXT-JS-INSTRUCTIONS.md` §7).

## 7. Existing Code to Reuse
- `DataTable`, `LoadingState`, `EmptyState`, `ErrorView`/`QueryErrorState`, `RequirePermission`, `DashboardShell`.
- Existing `recharts` chart-wrapper conventions already used by other admin dashboards.
- `apiClient.get()` pattern (per `NEXT-JS-INSTRUCTIONS.md` §6) for the underlying fetch.
- `hasPermission(admin, permission)` for RBAC gating.

## 8. Files to Create
- `src/features/downloads/api/downloads-monitoring-repository.ts`.
- `src/features/downloads/hooks/use-download-manifest-health.ts`.
- `src/features/downloads/types/manifest-health.types.ts` (Zod schema matching B-07 §13's manifest-health response).
- `src/features/downloads/components/manifest-issuance-chart.tsx`.
- `src/features/downloads/components/cap-rejection-trend-chart.tsx`.
- `src/app/(dashboard)/downloads/manifest-health/page.tsx`.
- `src/features/downloads/__tests__/use-download-manifest-health.test.ts`.

## 9. Files to Modify
- Sidebar navigation config — add "Download Manifest Health" entry under a Downloads section, gated by `RequirePermission`.

## 10. Backend Requirements
Consumes B-07: `GET /v1/admin/downloads/health?window=`.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- `useDownloadManifestHealth(window)` React Query hook calling `GET /v1/admin/downloads/health`.
- `ManifestIssuanceChart` (recharts line/area chart) plotting issued/cap-rejected/entitlement-rejected/url-reissue counts per time bucket.
- `CapRejectionTrendChart` isolating the cap-rejection series with a clear trend line.
- Window selector (`24h|72h|7d|30d`) driving the hook's query param, matching B-07's allow-listed values.
- Loading/empty/error states via existing components; zero-data-in-window renders a neutral "no activity in this window" empty state, not an error.
- RBAC: `product_admin`/`trust_safety` only.

## 13. API Contract
`GET /v1/admin/downloads/health?window=72h` → `{ series: [{ bucket, issued, cap_rejected, entitlement_rejected, url_reissue_count }] }` per B-07 §13.

## 14. Database Requirements
N/A (frontend consumes API only).

## 15. Validation
Window selector restricted to the same allow-list B-07 validates server-side (`24h|72h|7d|30d`) — client never sends an arbitrary value.

## 16. Authentication
Standard admin session via `apiClient`.

## 17. Authorization
`RequirePermission` for `product_admin`/`trust_safety`.

## 18. Error Handling
Standard `QueryErrorState`/`EmptyState` conventions; zero-issuance-activity in the selected window is a neutral empty state, distinct from a genuine fetch error.

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Chart labels, window-selector labels, empty-state copy via `useTranslation`; timestamps via `useFormatters`.

## 22. RTL
Standard RTL support via existing layout conventions; chart mirroring follows the platform's other `recharts` dashboards' existing pattern.

## 23. Analytics
No dedicated event beyond standard admin-page-view tracking, if the platform has one; this page is itself a monitoring surface.

## 24. Performance
Query data bounded by the selected window (max 30 days) to avoid over-fetching; React Query caching avoids redundant refetch on tab revisit; chart re-render minimized via memoized series-transform functions.

## 25. Security
Read-only; relies on B-07's backend RBAC as the actual security boundary. No per-child/per-family data surfaced (aggregate metrics only, per B-07 §25).

## 26. Library Requirements
Existing stack: Next.js, TanStack Query, recharts, Zod.

## 27. Testing
- Hook test: correct parsing of the manifest-health response shape for each window value.
- Component test: cap-rejection trend chart renders correctly from a fixture series.
- RBAC test: page hidden/blocked for a role without `product_admin`/`trust_safety`.
- Empty-state test: zero-activity window renders the neutral empty state, not an error.

## 28. Documentation
TSDoc noting this page is the human-facing counterpart to B-07's automated alerting.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Define Types**
Files to create: `manifest-health.types.ts`.

**Task 02 — Implement Repository & Hook**
Files to create: `downloads-monitoring-repository.ts`, `use-download-manifest-health.ts`.

**Task 03 — Build ManifestIssuanceChart**
Files to create: `manifest-issuance-chart.tsx`.

**Task 04 — Build CapRejectionTrendChart**
Files to create: `cap-rejection-trend-chart.tsx`.

**Task 05 — Assemble Page, Window Selector & Wire RBAC + Navigation**
Files to create: `page.tsx`; files to modify: sidebar config.

**Task 06 — Add Tests**

**Task 07 — Final Review**

## 30. Definition of Done
- Dashboard live, RBAC-gated, showing accurate issuance and cap-rejection charts across all supported window values.

## 31. Final Verification Checklist
- [ ] Charts render correctly from live B-07 data across all window values.
- [ ] RBAC restricts access to `product_admin`/`trust_safety`.
- [ ] Zero-activity window renders a neutral empty state, not an error.
- [ ] No per-child/per-family identifying data surfaced.
- [ ] Localization and RTL verified.
