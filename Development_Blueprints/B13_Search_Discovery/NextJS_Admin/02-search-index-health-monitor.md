# N-02 — Search Index Health Monitor

## 1. Feature Context
Part of Feature B.13 (Search & Discovery). Read-only dashboard giving editorial/product staff visibility into whether newly-published content is actually appearing in child search promptly, and which items are being rejected from indexing due to missing metadata.

## 2. Parent Feature
B.13 — Search & Discovery

## 3. Sub-feature
N-02 — Search Index Health Monitor

## 4. Objective
Build a read-only dashboard showing indexing-pipeline sync lag over time (chart) and a table of content items rejected from indexing due to missing `age_band_eligibility`, each linking to its content editor so the missing field can be filled in.

## 5. Business Requirements
- Admin Requirements §8: Search Index Health Monitor — sync lag/failures, rejected-due-to-missing-metadata documents, surfaced for editorial to quickly fix.
- RBAC: read-only behind `content_editor`/`product_admin`.
- DevOps §10: this dashboard is the human-facing counterpart to the backend's automated sync-lag/rejection-rate alerts (B-07).

## 6. Existing Architecture
New page under `src/features/search/`, reusing the existing `recharts`-based dashboard pattern already established for other admin metrics pages (per `useDashboardStats`'s existing precedent in `NEXT-JS-INSTRUCTIONS.md`).

## 7. Existing Code to Reuse
- `DataTable`, `LoadingState`, `EmptyState`, `ErrorView`, `RequirePermission`.
- Existing `recharts` usage pattern from the platform's other admin dashboard charts (reuse chart-wrapper conventions, don't introduce a new charting library).
- `SearchRepositoryImpl` (N-01) extended, or a sibling `SearchMonitoringRepositoryImpl` — whichever keeps the `search` feature module's API layer cleanest; both call B-07.

## 8. Files to Create
- `src/features/search/api/search-monitoring-repository.ts`.
- `src/features/search/hooks/use-index-health.ts`.
- `src/features/search/types/index-health.types.ts` (Zod schema matching B-07 §13's index-health response).
- `src/features/search/components/sync-lag-chart.tsx`.
- `src/features/search/components/rejected-items-table.tsx`.
- `src/app/(dashboard)/search/index-health/page.tsx`.
- `src/features/search/__tests__/use-index-health.test.ts`.

## 9. Files to Modify
- Sidebar navigation config — add "Search Index Health" entry under the Search section, gated by `RequirePermission`.

## 10. Backend Requirements
Consumes B-07: `GET /admin/v1/search/index-health`.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- `useIndexHealth()` React Query hook calling `GET /admin/v1/search/index-health`.
- `SyncLagChart` (recharts line/area chart) plotting sync lag over time.
- `RejectedItemsTable` (`DataTable`) listing `content_id`, `reason`, `detected_at`, with an "Open in editor" link per row (same linking pattern as N-01).
- Loading/empty/error states via existing components.
- RBAC: `content_editor`/`product_admin` only.

## 13. API Contract
`GET /admin/v1/search/index-health` → `{ sync_lag_seconds, rejected_items: [...] }` per B-07 §13.

## 14. Database Requirements
N/A (frontend consumes API only).

## 15. Validation
N/A (read-only display).

## 16. Authentication
Standard admin session via `apiClient`.

## 17. Authorization
`RequirePermission` for `content_editor`/`product_admin`.

## 18. Error Handling
Standard `QueryErrorState`/`EmptyState` conventions; zero rejected items renders a positive "all content indexed cleanly" empty state, not a generic placeholder.

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Chart labels, table headers, empty-state copy via `useTranslation`; timestamps via `useFormatters`.

## 22. RTL
Standard RTL support via existing layout conventions; chart mirroring follows whatever pattern the platform's other `recharts` dashboards already use.

## 23. Analytics
No dedicated event beyond standard admin-page-view tracking, if the platform has one; this page is itself an analytics/monitoring surface, not a source of new event taxonomy.

## 24. Performance
Sync-lag chart data should be reasonably bounded (e.g., last 24–72 hours) to avoid over-fetching; React Query caching avoids redundant refetch on tab revisit.

## 25. Security
Read-only; relies on B-07's backend RBAC as the actual security boundary.

## 26. Library Requirements
Existing stack: Next.js, TanStack Query, recharts (already in use elsewhere), Zod.

## 27. Testing
- Hook test: correct parsing of the index-health response shape.
- Component test: rejected-items table renders correct editor links per content type.
- RBAC test: page hidden/blocked for a role without `content_editor`/`product_admin`.
- Empty-state test (zero rejected items → positive-framing empty state, not generic).

## 28. Documentation
TSDoc noting this page is the human-facing counterpart to B-07's automated alerting.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Define Types**
Files to create: `index-health.types.ts`.

**Task 02 — Implement Repository & Hook**
Files to create: `search-monitoring-repository.ts`, `use-index-health.ts`.

**Task 03 — Build SyncLagChart**
Files to create: `sync-lag-chart.tsx`.

**Task 04 — Build RejectedItemsTable**
Files to create: `rejected-items-table.tsx`.

**Task 05 — Assemble Page & Wire RBAC + Navigation**
Files to create: `page.tsx`; files to modify: sidebar config.

**Task 06 — Add Tests**

**Task 07 — Final Review**

## 30. Definition of Done
- Dashboard live, RBAC-gated, showing accurate sync-lag chart and rejected-items table with working editor links.

## 31. Final Verification Checklist
- [ ] Sync-lag chart renders correctly from live B-07 data.
- [ ] Rejected items link correctly to their content editors.
- [ ] RBAC restricts access to `content_editor`/`product_admin`.
- [ ] Zero-rejected-items state uses positive framing, not a generic empty placeholder.
- [ ] Localization and RTL verified.
