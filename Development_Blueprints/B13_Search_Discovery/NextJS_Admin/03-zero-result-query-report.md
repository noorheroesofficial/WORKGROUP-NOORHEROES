# N-03 — Zero-Result Query Report

## 1. Feature Context
Part of Feature B.13 (Search & Discovery). Read-only, aggregated, privacy-safe reporting on the most common zero-result child search queries — a content-gap signal for editorial, never a per-child query log.

## 2. Parent Feature
B.13 — Search & Discovery

## 3. Sub-feature
N-03 — Zero-Result Query Report

## 4. Objective
Build a date-range-filterable, read-only table of the most frequent zero-result child search queries, sourced from an already content-safety-filtered, never-per-child-attributed backend aggregation (B-07).

## 5. Business Requirements
- Admin Requirements §8: aggregate, privacy-safe (no per-child attribution) reporting on the most common zero-result queries, helping editorial identify content gaps.
- Edge Case 3 (carried forward): recent-searches/popular-searches data must pass a content-safety filter before persisting/displaying beyond the originating child's device — this page must never display a raw, unfiltered per-child query log.
- RBAC: read-only behind `content_editor`.

## 6. Existing Architecture
New page under `src/features/search/`, following the same repository/hook/table pattern as N-01/N-02.

## 7. Existing Code to Reuse
- `DataTable`, `LoadingState`, `EmptyState`, `ErrorView`, `RequirePermission`.
- A date-range-picker component if one already exists elsewhere in the admin portal (e.g., used by another reporting page) — reused, not rebuilt.
- `search-monitoring-repository.ts` (N-02) extended with a zero-result-report method, or a sibling method on the same repository class.

## 8. Files to Create
- `src/features/search/hooks/use-zero-result-report.ts`.
- `src/features/search/types/zero-result-report.types.ts` (Zod schema matching B-07 §13's zero-result-report response).
- `src/features/search/components/zero-result-query-table.tsx`.
- `src/app/(dashboard)/search/zero-result-report/page.tsx`.
- `src/features/search/__tests__/use-zero-result-report.test.ts`.

## 9. Files to Modify
- `search-monitoring-repository.ts` (N-02) — add `getZeroResultReport(from, to)` method.
- Sidebar navigation config — add "Zero-Result Queries" entry.

## 10. Backend Requirements
Consumes B-07: `GET /admin/v1/search/zero-result-report?from=&to=`.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- Date-range selector (reused existing component if available) driving `useZeroResultReport({ from, to })`.
- `ZeroResultQueryTable` (`DataTable`) rendering `query_text_filtered`, `count`, sorted by `count` descending.
- Explicit UI copy/tooltip clarifying this is aggregated and privacy-filtered — no per-child drill-down affordance anywhere on this page (a structural UI guarantee: no row-click-through to any child-level detail).
- RBAC: `content_editor` only.

## 13. API Contract
`GET /admin/v1/search/zero-result-report?from=&to=` → `{ top_queries: [{ query_text_filtered, count }] }` per B-07 §13.

## 14. Database Requirements
N/A (frontend consumes API only).

## 15. Validation
Date-range inputs validated client-side (from ≤ to, bounded to a sane max range matching B-07's server-side bound) before request submission.

## 16. Authentication
Standard admin session via `apiClient`.

## 17. Authorization
`RequirePermission` for `content_editor`.

## 18. Error Handling
Standard `QueryErrorState`/`EmptyState`; invalid date range shows a client-side validation message before any request is fired.

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Table headers, date-range labels via `useTranslation`; date formatting via `useFormatters`.

## 22. RTL
Standard RTL support via existing layout conventions.

## 23. Analytics
No dedicated event beyond standard admin-page-view tracking, if present.

## 24. Performance
Date range bounded (matches B-07's server-side max-range validation); React Query caches per date-range key.

## 25. Security
**This page must have zero drill-down path to per-child data** — the UI itself has no click-through affordance beyond the aggregated row, reinforcing (at the frontend layer) the privacy guarantee B-07 already enforces server-side.

## 26. Library Requirements
Existing stack only.

## 27. Testing
- Hook test: date-range params correctly serialized.
- Component test: table renders aggregated rows only, with no interactive element that could imply per-child drill-down.
- RBAC test: page hidden/blocked for a role without `content_editor`.
- Invalid-date-range client-side validation test.

## 28. Documentation
TSDoc explicitly noting this page must never gain a per-child drill-down feature — any future addition of one would violate the feature's core privacy guarantee.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Define Types**
Files to create: `zero-result-report.types.ts`.

**Task 02 — Extend Repository & Add Hook**
Files to modify: `search-monitoring-repository.ts`; files to create: `use-zero-result-report.ts`.

**Task 03 — Build ZeroResultQueryTable & Date-Range Selector**
Files to create: `zero-result-query-table.tsx`.

**Task 04 — Assemble Page & Wire RBAC + Navigation**
Files to create: `page.tsx`; files to modify: sidebar config.

**Task 05 — Add Tests**

**Task 06 — Final Review**
Objective: confirm no row/interaction on this page provides any path to per-child-level data.

## 30. Definition of Done
- Report live, date-range-filterable, RBAC-gated, showing only aggregated data.

## 31. Final Verification Checklist
- [ ] No UI element on this page provides a path to per-child query data.
- [ ] Date range validated client-side and matches backend's bound.
- [ ] RBAC restricts access to `content_editor`.
- [ ] Empty state for no-data-in-range distinct from an error state.
- [ ] Localization and RTL verified.
