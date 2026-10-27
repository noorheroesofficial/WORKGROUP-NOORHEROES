# N-01 — Favoriting Pattern Monitor Dashboard

## 1. Feature Context
Part of Feature B.14 Favorites. The only NextJS Admin sub-feature for this PRD — Favorites has no admin-authored content of its own, so this read-only aggregate dashboard is the entirety of the Admin surface (PRD §8).

## 2. Parent Feature
B.14 Favorites (`PRD_Documents/Child App — Supporting (13-18)/Feature_B14_Favorites.md`)

## 3. Sub-feature
3.1 Favoriting Pattern Monitor Dashboard — `N-01`

## 4. Objective
Build a read-only, aggregate, privacy-safe dashboard showing the most and least frequently favorited content platform-wide, filterable by content type and date range, for the `content_editor` role.

## 5. Business Requirements
- PRD §8: "Aggregate, privacy-safe (never per-child) reporting... a content-curation signal for editorial." No CRUD surfaces needed.
- PRD §9: "NEVER exposes any per-child favorite list or identity — only aggregate counts per content_id... purely an editorial/curation signal, with no mutation capability on this page at all."
- "No audit logging needed for this page since it performs no mutating actions."

## 6. Existing Architecture
Next.js 15 App Router: `src/proxy.ts` middleware → `src/app/(dashboard)/*` pages → `DashboardShell` → `src/features/<feature>/` (components/hooks/api). `BaseResourceClient<Entity, Create, Update, Filters>` pattern with Zod validation, called only via React Query hooks, never directly in components. `apiClient` (`src/lib/api-client.ts`) injects Bearer token + `X-Request-ID`. Endpoints centralized in `API_ENDPOINTS` (`src/shared/constants/api-endpoints.ts`). RBAC via `<RequirePermission permission="...">` + `hasPermission(admin, permission)`.

**Resolved research finding — permission string, use the PRD's literal value:** B.14's own PRD §8 states verbatim "CRUD permissions: Favoriting Pattern Monitor = Read-only behind `content_editor` role." B.13's real admin pages use bare role names (`content_editor`, `support`, `trust_safety`, `product_admin`, `ai_ops`), not the colon-namespaced style (`users:read`) shown as an example elsewhere in `NEXT-JS-INSTRUCTIONS.md` — that colon-style example is a pre-existing inconsistency in the docs, not something this feature should resolve on its own. **Use the bare role name `content_editor`**, matching both the PRD and actual B.13 precedent.

**Resolved research finding — Admin Portal is NOT English-only (corrects an earlier assumption in this blueprint):** `NEXT-JS-INSTRUCTIONS.md` documents a mandatory `useTranslation`/`useFormatters` pattern with explicit "do NOT hardcode English strings" guidance, a `useLocalization` hook that checks active locale/RTL status, and locale values including `'hi'|'ar'|'en'`. This page must localize all copy and support RTL like any other Admin Portal page — see §21/§22 below, corrected from the original draft.

**Resolved — nav registration:** new pages are registered via the sidebar navigation config consumed by `DashboardShell` (`src/shared/components/dashboard-shell.tsx`, per `NEXT-JS-INSTRUCTIONS.md`); the exact sidebar config file path is not named in the docs — locate it by finding where B.13's `02-search-index-health-monitor.md`/`03-zero-result-query-report.md` (the closest sibling read-only monitor pages) register their own nav entries, and follow the same file.

## 7. Existing Code to Reuse
- `DashboardShell`, `RequirePermission`
- `DataTable` / chart component patterns already used in B.13's `02-search-index-health-monitor.md` and `03-zero-result-query-report.md` (closest sibling read-only monitor pages — reuse their layout convention rather than inventing a new one)
- `apiClient`, `API_ENDPOINTS`
- `useDebouncedValue`/`FilterPanel` if filter-heavy (this page has only two filters: content_type, date range — evaluate whether the full `FilterPanel` is warranted or a simpler inline filter bar suffices)

## 8. Files to Create
- `src/app/(dashboard)/favorites/pattern-report/page.tsx`
- `src/features/favorites/api/favoritesPatternReportClient.ts` (extends `BaseResourceClient` or a read-only equivalent, since this is a report endpoint, not a full CRUD resource)
- `src/features/favorites/components/FavoritingPatternChart.tsx`
- `src/features/favorites/hooks/useFavoritingPatternReport.ts` (React Query hook)
- `src/features/favorites/types/favoritesPatternReport.ts` (TypeScript types + Zod schema)
- Tests: `FavoritingPatternChart.test.tsx`, `useFavoritingPatternReport.test.ts`

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add the `GET /admin/v1/favorites/pattern-report` endpoint constant
- Admin navigation/menu config — add an entry point to this dashboard (exact nav config file not independently verified in this research pass — locate via the existing B.13 admin pages' nav registration)

## 10. Backend Requirements
Consumes B-04 (`GET /admin/v1/favorites/pattern-report`) exactly as specified there — this blueprint does not invent additional backend fields.

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- Page under `<RequirePermission permission="content_editor">` (bare role name, per the resolved §6 finding — matches PRD §8 and B.13 precedent, not a namespaced string).
- `content_type` filter (dropdown/chip: All/Stories/Surahs/Duas).
- Date-range filter.
- Recharts-based ranked bar chart or table (most/least favorited).
- Loading skeleton, empty state (no activity in range), error state (API failure).
- No mutation controls anywhere on this page — purely read-only by design.
- Responsive layout consistent with the rest of the Admin Portal.
- Accessible chart (data-table fallback / alt-text for screen readers).

## 13. API Contract
Consumes B-04's `GET /admin/v1/favorites/pattern-report`. **As flagged in B-04, the exact response field names are not yet confirmed against the PRD** — this page's TypeScript types and Zod schema must be finalized only after B-04's contract is confirmed, not built against an assumed shape.

## 14. Database Requirements
Not applicable (consumes API only).

## 15. Validation
Zod schema validates the API response shape (via `BaseResourceClient`'s existing validation pattern); filter inputs (content_type enum, date range) validated client-side before the query fires.

## 16. Authentication
Handled by `apiClient`'s existing Bearer token injection + refresh/401 handling.

## 17. Authorization
`RequirePermission` gate for `content_editor` (or the platform's equivalent read-only favorites-report permission) — page renders nothing (or an access-denied state) for any other role.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| API failure | Error boundary/inline error state, retry affordance |
| Empty result set | Friendly empty state ("No favoriting activity in this range") |
| Unauthorized/forbidden | Page-level access-denied state via `RequirePermission`, no partial data flash |
| Loading | Skeleton/loading state, no layout shift on data arrival |

## 19. Offline First
Not applicable — Admin Portal is an online-only web context.

## 20. Local Data
None — React Query cache only, standard TTL per the platform's existing query-client configuration.

## 21. Localization
**Corrected per §6's resolved finding:** the Admin Portal is not EN-only. All copy on this page (filter labels, chart axis labels/legend, empty/error/loading state text, permission-denied messaging) must go through `useTranslation`/`useFormatters` — no hardcoded English strings, consistent with `NEXT-JS-INSTRUCTIONS.md`'s explicit "do NOT hardcode English strings" instruction. Date-range filter values must use the existing locale-aware date formatter, not a hardcoded EN format.

## 22. RTL
**Corrected per §6's resolved finding:** this page must support RTL via the platform's `useLocalization` hook, which checks active locale/RTL status — filter bar, chart, and table/legend layout must mirror correctly for Arabic/Urdu admin users, consistent with every other Admin Portal page.

## 23. Analytics
No dedicated analytics event specified in the PRD for this admin page.

## 24. Performance
React Query caching avoids redundant refetches on filter no-ops; chart rendering should handle a reasonably large content catalog without jank — confirm expected data volume (number of distinct `content_id`s platform-wide) before committing to a specific chart library configuration.

## 25. Security
Zero per-child data must ever reach the client — this is enforced primarily by B-04's backend contract, but this page's types/rendering must never introduce a per-child field even if one were accidentally present in a future API response (defensive typing).

## 26. Library Requirements
Recharts (per PRD §9), React Query, Zod — all already in use elsewhere in the Admin Portal; no new library introduced.

## 27. Testing
- Unit: chart component renders correctly given aggregate fixture data.
- Unit: filter state correctly narrows the query params sent to the API.
- Integration: `RequirePermission` correctly blocks non-`content_editor` roles.
- Integration: empty/error/loading states render correctly.
- Defensive test: response containing an unexpected per-child-shaped field is never rendered (guards against a future backend regression).

## 28. Documentation
Page-level README or component doc noting the read-only, no-mutation, zero-per-child-data invariants for future maintainers.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Confirm B-04's Exact Response Contract.** Do not proceed to Task 02 until this is confirmed (see §13).
**Task 02 — Add API Endpoint Constant.** `API_ENDPOINTS.favorites.patternReport`.
**Task 03 — Build API Client.** Read-only client/hook wrapping `GET /admin/v1/favorites/pattern-report`.
**Task 04 — Build `FavoritingPatternChart` Component.** Recharts-based, reusing B.13's monitor-page layout convention.
**Task 05 — Build Page & Filters.** `content_type` + date-range filters.
**Task 06 — Wire `RequirePermission`.** `permission="content_editor"` (confirmed, §6).
**Task 07 — Implement Loading/Empty/Error States.**
**Task 08 — Localize All Copy and Verify RTL.** Via `useTranslation`/`useFormatters`/`useLocalization` (corrected requirement, §21/§22) — not optional for this page.
**Task 09 — Add Navigation Entry.** Register the page in the sidebar config consumed by `DashboardShell`, following B.13's monitor-page registration pattern (§6).
**Task 10 — Write Tests.** Per §27.
**Task 11 — Final Code Review.** Confirm no mutation affordance exists anywhere on the page and all copy is localized.

## 30. Definition of Done
Page renders aggregate data correctly with working filters; RBAC test green; zero-per-child-data defensive test green; loading/empty/error states verified; no mutation controls present.

## 31. Final Verification Checklist
- [ ] Read-only — no mutation UI anywhere on the page
- [ ] `content_editor` (or confirmed equivalent) permission enforced
- [ ] Filters (content_type, date range) function correctly
- [ ] Zero per-child data ever rendered, including defensively against malformed API responses
- [ ] Loading/empty/error states implemented
- [ ] API response contract confirmed against B-04 before shipping, not assumed
- [ ] Accessible chart (screen-reader fallback) implemented
- [ ] All copy localized via `useTranslation`/`useFormatters`, no hardcoded English strings
- [ ] RTL layout verified for Arabic/Urdu admin locale
- [ ] Nav entry registered in sidebar config, following B.13's monitor-page pattern
