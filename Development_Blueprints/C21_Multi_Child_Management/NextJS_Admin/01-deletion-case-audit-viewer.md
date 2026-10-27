# N-01 — Deletion Case Audit Viewer (Read-Only)

## 1. Feature Context
Part of Feature C.21 — Multi-Child Management's Admin Requirements (§8): a read-only compliance/support surface over the audit trail B-06 automatically produces.

## 2. Parent Feature
C.21 Multi-Child Management

## 3. Sub-feature
**N-01 — Deletion Case Audit Viewer (Read-Only)**

## 4. Objective
Give Support/Trust & Safety staff a paginated, searchable, strictly read-only table of every `child_deletion_case` record — with no restore/override affordance anywhere in the UI, matching the backend's equally strict read-only contract.

## 5. Business Requirements
- §8: "Deletion Case Audit Viewer (Read-only): Search by masked identifier, view the full `child_deletion_case` lifecycle. No override/restore capability."
- CRUD permissions: Read-only behind `support`/`trust_safety`.

## 6. Existing Architecture
Follows the NextJS Admin layered architecture (`NEXT-JS-INSTRUCTIONS.md`): Page → Custom Hook → Repository/`BaseResourceClient` → `apiClient` → Backend REST API, wrapped in `RequirePermission`.

## 7. Existing Code to Reuse
- `BaseResourceClient<TEntity, TCreate, TUpdate, TFilters>` — extend for `DeletionCaseResourceClient`, but only wire the `list`/`get` methods; deliberately never call/expose `create`/`update`/`delete` for this resource.
- `DataTable` (`shared/components/data-table`) — reuse for the paginated table, per the "Pattern 1: Building a Complete Directory Page" example in `NEXT-JS-INSTRUCTIONS.md`.
- `SearchBar`, `FilterPanel`, `usePaginationState`, `useDebouncedValue` — reused as-is.
- `RequirePermission` — gate the entire page.
- `StatusBadge` — reuse for rendering case status (`pending`/`purged`).

## 8. Files to Create
- `src/features/child-deletion-audit/api/deletion-case-resource-client.ts`
- `src/features/child-deletion-audit/api/schemas.ts` (Zod schemas for `DeletionCase`, `PaginatedDeletionCases`)
- `src/features/child-deletion-audit/hooks/use-deletion-cases.ts`
- `src/features/child-deletion-audit/index.ts` (public feature exports)
- `src/app/(dashboard)/support/child-deletion-cases/page.tsx`

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `API_ENDPOINTS.CHILD_DELETION_CASES.BASE` (path pending B-09's confirmation — coordinate directly with that blueprint before hardcoding).
- Sidebar navigation config — add the entry under Support, gated by `RequirePermission`.

## 10. Backend Requirements
Consumes B-09 exclusively (⚠ endpoint path pending confirmation, see that blueprint).

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- `DeletionCaseResourceClient extends BaseResourceClient<DeletionCase, never, never, DeletionCaseFilters>` — the `never` generics for create/update are a deliberate compile-time guard preventing accidental mutation code from ever being written against this resource.
- `useDeletionCases(filters)` — React Query hook wrapping `list()`, following the `useFamilyList`/`useUsers` pattern exactly.
- Page composes `FilterPanel` + `SearchBar` (debounced) + `DataTable`, matching the "Complete Directory Page" pattern verbatim.
- `RequirePermission permission="deletion-cases:read"` — this follows the frontend's own existing `resource:action` string convention (per `NEXT-JS-INSTRUCTIONS.md`'s documented `permission="users:read"` example), which is distinct from the backend's bare-role-name convention. Backend-side, this maps down to admins holding the `support` or `trust_safety` role (see B-09, now resolved) — confirm with the frontend's actual `AdminPermission` type definition that a `deletion-cases:read` entry either exists or should be added, mapped to those two backend roles.

## 13. API Contract
Consumes B-09's contract (`GET /v1/admin/child-deletion-cases`, now confirmed — see that blueprint's update note) as documented in that blueprint.

## 14. Database Requirements
Not applicable — Admin Portal has no direct DB access, per the established layering.

## 15. Validation
Search input is free text (masked-identifier search); no form validation needed since this page has no submission form.

## 16. Authentication
`useAdminSession()` — standard admin auth guard via `DashboardShell`/layout-level session check.

## 17. Authorization
`RequirePermission` wraps the entire page; the sidebar entry itself is also conditionally rendered via `RequirePermission`, per the existing "protect a button or navigation link" pattern.

## 18. Error Handling
- `QueryErrorState` for API failures (existing shared component, per the Quick Reference table).
- `EmptyState` when no matching cases.
- `LoadingState` during initial fetch.
- `403` from the backend (missing scope) → `ErrorView` with a clear "insufficient permissions" message, not a generic error.

## 19. Offline First
Not applicable — Admin Portal is not offline-first.

## 20. Local Data
Not applicable.

## 21. Localization
All column headers, status labels, empty-state copy, and search placeholder sourced via `useTranslation()`; dates formatted via `useFormatters().formatDate`.

## 22. RTL
Table and filter-panel layout must mirror correctly under RTL locales, consistent with the rest of the Admin Portal's localization architecture.

## 23. Analytics
Not specified in the PRD for this admin surface; none implemented unless the platform's existing Admin Portal analytics convention requires page-view tracking (check for an existing pattern before adding one here).

## 24. Performance
Server-side pagination via `DataTable`'s existing `page`/`pageSize`/`totalItems` props — never fetch the full dataset client-side; debounced search (300ms, matching `useUsers`' convention) to avoid excessive requests.

## 25. Security
- The `never` generic-type guard on create/update in `DeletionCaseResourceClient` is the primary structural security control preventing accidental mutation code.
- No delete/restore button exists anywhere in this page's component tree — verified by code review and a negative UI test.
- Masked identifiers only — never render raw `child_id`/`parent_id` in the table unless the masking scheme (per B-09) is specifically designed to allow partial reveal to authorized roles.

## 26. Library Requirements
No new libraries — TanStack Query, Zod, existing shared component library.

## 27. Testing
- Unit: `DeletionCaseResourceClient` correctly validates responses against its Zod schema.
- Integration/UI: table renders paginated results correctly.
- Integration/UI: search filters results correctly (debounced).
- Integration/UI: `RequirePermission` correctly hides the page/nav-entry for an admin lacking the required permission.
- Negative test: no restore/delete/edit affordance exists anywhere in the rendered page.

## 28. Documentation
Document in the feature's `index.ts` or a short README that this resource is intentionally read-only by design, cross-referencing B-09 and the PRD's explicit "no override/restore capability" requirement.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Wire Confirmed Endpoint Path & Permission String**
- **Objective:** B-09's path (`/v1/admin/child-deletion-cases`) is now confirmed; add `API_ENDPOINTS.CHILD_DELETION_CASES.BASE` and confirm/add a `deletion-cases:read` entry to the `AdminPermission` catalog mapped to the backend's `support`/`trust_safety` roles.
- **Definition of Done:** Both constants added, no longer blocking.

**Task 02 — Zod Schemas & Resource Client**
- **Objective:** Build `DeletionCase`/`PaginatedDeletionCases` Zod schemas and the read-only resource client.
- **Files to Create:** `schemas.ts`, `deletion-case-resource-client.ts`.
- **Implementation Details:** `class DeletionCaseResourceClient extends BaseResourceClient<DeletionCase, never, never, DeletionCaseFilters>`; only `list()`/`get()` are ever called.
- **Tests:** Schema-validation unit tests with both valid and malformed fixture payloads.
- **Definition of Done:** Client rejects malformed backend responses via Zod rather than passing through unvalidated data.

**Task 03 — `useDeletionCases` Hook**
- **Objective:** React Query wrapper following the `useFamilyList` pattern.
- **Files to Create:** `use-deletion-cases.ts`.
- **Tests:** Hook unit test with a mocked client.
- **Definition of Done:** Hook exposes `{ data, isLoading, error, refetch }` consistent with every other list hook in the codebase.

**Task 04 — Page Composition & Navigation Entry**
- **Objective:** Build the page and wire the sidebar entry behind `RequirePermission`.
- **Files to Create:** `page.tsx`.
- **Files to Modify:** sidebar navigation config.
- **Implementation Details:** `FilterPanel` + `SearchBar` + `DataTable`, matching the documented "Complete Directory Page" pattern.
- **Tests:** UI tests per §27, including the negative no-mutation-affordance test.
- **Definition of Done:** Page fully functional, permission-gated, and provably free of any mutation UI.

## 30. Definition of Done
Read-only viewer fully functional, permission-gated, structurally prevented (via `never` generics) from ever growing a mutation path, and fully localized.

## 31. Final Verification Checklist
- [ ] Endpoint path and permission string confirmed with B-09's owner
- [ ] `DeletionCaseResourceClient` uses `never` for create/update generics
- [ ] No mutation UI exists anywhere on the page (negative test passes)
- [ ] Pagination and debounced search verified
- [ ] `RequirePermission` correctly gates both the page and the nav entry
- [ ] Full localization and RTL verified
