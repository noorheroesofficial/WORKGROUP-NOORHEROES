# N-01 — Admin Content Search Surface

## 1. Feature Context
Part of Feature B.13 (Search & Discovery). The operator-facing UI for B-06's unrestricted admin search endpoint — a read-only discovery/navigation tool linking out to existing content editors, with no inline content-mutation capability of its own.

## 2. Parent Feature
B.13 — Search & Discovery

## 3. Sub-feature
N-01 — Admin Content Search Surface

## 4. Objective
Build a search page with advanced filter controls (tag, status, language, review_state) calling `GET /admin/v1/search`, rendering results in the existing `DataTable` component, each row linking to its content item's editor in A.3/A.5/A.6's respective admin modules.

## 5. Business Requirements
- Admin Requirements §8: powerful search UI supporting filtering by tag, status, language, review state, querying the full content database directly — read-only, results link out to relevant content editors.
- RBAC: read-only behind `content_editor`/`support`/`trust_safety` role.

## 6. Existing Architecture
New page under `src/features/search/` in the Next.js Admin Portal, following the exact layered pattern from `NEXT-JS-INSTRUCTIONS.md` §2: UI Components → Custom React Query Hooks → Repository (`BaseResourceClient` extension) → `apiClient` → Backend REST API.

## 7. Existing Code to Reuse
- `BaseResourceClient` — extended for `SearchRepositoryImpl`.
- `SearchBar` component (existing, debounced search input — per `NEXT-JS-INSTRUCTIONS.md`'s Quick Reference) — reused directly, not rebuilt.
- `useDebouncedValue` hook — reused for the search input.
- `DataTable` component — for rendering results.
- `FilterPanel` component — container for the tag/status/language/review_state filter controls.
- `RequirePermission` — RBAC guard.
- `LoadingState`, `EmptyState`, `ErrorView`, `QueryErrorState` — standard state components.
- `usePaginationState` — pagination state management.
- `useTranslation`, `useFormatters` — localization.
- `DashboardShell` layout wrapper.

## 8. Files to Create
- `src/features/search/api/search-repository.ts` (`SearchRepositoryImpl extends BaseResourceClient`).
- `src/features/search/hooks/use-admin-search.ts` (React Query hook).
- `src/features/search/types/search.types.ts` (Zod schemas + TS types matching B-06 §13's response shape).
- `src/features/search/components/search-filter-panel.tsx` (tag multi-select, status/language/review_state dropdowns).
- `src/features/search/components/search-results-table.tsx`.
- `src/app/(dashboard)/search/page.tsx`.
- `src/features/search/__tests__/use-admin-search.test.ts`.
- `src/features/search/__tests__/search-results-table.test.tsx`.

## 9. Files to Modify
- Sidebar navigation config — add "Content Search" entry, gated by `RequirePermission`.

## 10. Backend Requirements
Consumes B-06 exclusively: `GET /admin/v1/search?q=&tag=&status=&language=&review_state=`.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- Page composes `SearchBar` (debounced via `useDebouncedValue`) + `SearchFilterPanel` + `DataTable`.
- `useAdminSearch({ q, tag, status, language, reviewState, page, limit })` React Query hook, calling `SearchRepositoryImpl.list()`.
- Each result row includes an "Open in editor" link/button navigating to the relevant content item's existing editor route in A.3/A.5/A.6's admin modules (by `content_type` + `content_id`) — no inline edit UI on this page itself.
- Filter changes reset pagination to page 1 (standard `DataTable` convention).
- Loading state via `LoadingState`; zero-result state via `EmptyState`; API error via `QueryErrorState`.
- RBAC: entire page wrapped in `RequirePermission` for `content_editor`/`support`/`trust_safety`.

## 13. API Contract
`GET /admin/v1/search?q=&tag=&status=&language=&review_state=` → `{ results: [...], result_count }` per B-06 §13.

## 14. Database Requirements
N/A (frontend consumes API only).

## 15. Validation
Filter dropdown values sourced from known enums (mirroring backend validation); tag multi-select sourced from an existing tag-list endpoint if one exists in `content`'s admin API (reuse, do not invent a new tag-listing endpoint here).

## 16. Authentication
Standard admin session via existing `apiClient` Bearer-token injection + refresh handling.

## 17. Authorization
`RequirePermission` guard at the page level; sidebar entry itself only rendered for permitted roles (existing `RequirePermission`-filtered sidebar pattern per `NEXT-JS-INSTRUCTIONS.md` §2).

## 18. Error Handling
Standard `QueryErrorState` for API failures; `EmptyState` for zero results (distinct copy from a loading/error state); no new error-handling pattern introduced beyond existing conventions.

## 19. Offline First
N/A (admin web, always-online assumption).

## 20. Local Data
N/A.

## 21. Localization
All labels/copy via `useTranslation`; date/number formatting (if any result metadata needs it) via `useFormatters`.

## 22. RTL
Standard RTL support via the existing global layout/CSS direction handling — no feature-specific RTL work expected beyond following existing component conventions.

## 23. Analytics
`admin_search_performed` — fired on successful query submission (internal/operator telemetry, per parent PRD §1.19).

## 24. Performance
Debounced search input avoids excessive requests; `DataTable` pagination avoids rendering unbounded result sets; React Query caching avoids redundant refetches on identical filter combinations.

## 25. Security
Read-only page — no mutation capability, reducing its own risk surface per PRD §12.5. Relies entirely on B-06's backend RBAC enforcement; frontend `RequirePermission` is a UX guard, not the security boundary.

## 26. Library Requirements
Existing stack only: Next.js 15 App Router, TypeScript, TanStack Query v5, Zod. No new dependency.

## 27. Testing
- Hook test: `useAdminSearch` correctly serializes filter params into the query.
- Component test: results table renders "Open in editor" links with correct target URLs per `content_type`.
- RBAC test: page redirects/hides for a role without `content_editor`/`support`/`trust_safety`.
- Empty-state test.

## 28. Documentation
Inline TSDoc on `SearchRepositoryImpl`/`useAdminSearch`; note in the module explaining this page is read-only by design and must never gain inline edit capability.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Define Types & Zod Schemas**
Files to create: `search.types.ts`.

**Task 02 — Implement SearchRepositoryImpl**
Objective: extend `BaseResourceClient`, call `GET /admin/v1/search`.
Files to create: `search-repository.ts`.

**Task 03 — Implement useAdminSearch Hook**
Files to create: `use-admin-search.ts`.

**Task 04 — Build SearchFilterPanel & SearchResultsTable**
Objective: reuse `FilterPanel`, `DataTable`, `SearchBar`, `useDebouncedValue`.
Files to create: two component files.

**Task 05 — Assemble Page & Wire RBAC + Navigation**
Files to create: `page.tsx`; files to modify: sidebar config.

**Task 06 — Add Tests**
Objective: hook, component, RBAC, empty-state tests per §27.

**Task 07 — Final Review**
Objective: confirm zero inline content-mutation UI exists on this page; confirm "Open in editor" links target the correct existing admin routes for each content type.

## 30. Definition of Done
- Page live at its sidebar entry, RBAC-gated correctly.
- All four filters functional and combinable.
- Results link out correctly to existing content editors.
- Full test coverage per §27.

## 31. Final Verification Checklist
- [ ] Page is read-only — no inline edit/mutation capability anywhere on it.
- [ ] All four filters (tag, status, language, review_state) functional and combinable.
- [ ] RBAC correctly restricts access to `content_editor`/`support`/`trust_safety`.
- [ ] "Open in editor" links resolve to the correct existing admin route per content type.
- [ ] Search input reuses the existing `SearchBar`/`useDebouncedValue` pattern, not a new implementation.
- [ ] Localization and RTL verified.
