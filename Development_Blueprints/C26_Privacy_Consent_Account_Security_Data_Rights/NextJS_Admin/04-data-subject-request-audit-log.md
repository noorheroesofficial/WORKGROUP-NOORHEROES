# N-04 — Data Subject Request Audit Log

## 1. Feature Context
Part of Feature C.26's Admin Requirements (§8). A read-only, paginated, masked-identifier compliance view over every `data_request` record, consuming B-08 and directly mirroring C.21 N-01's established pattern.

## 2. Parent Feature
C.26 Privacy, Consent, Account Security & Data Rights (Settings)

## 3. Sub-feature
**N-04 — Data Subject Request Audit Log**

## 4. Objective
Build a `support`/`trust_safety`/`compliance`-gated, strictly read-only, paginated table of `data_request` records, with zero mutation affordance anywhere — the exact structural pattern C.21 N-01 already established for `child_deletion_case`.

## 5. Business Requirements
- §8: read-only, paginated table of `data_request` records (masked family identifier, type, status, timestamps), `support`/`trust_safety`/`compliance` roles.

## 6. Existing Architecture
Directly mirrors C.21 N-01 ("Deletion Case Audit Viewer") — same `never`-generic resource-client pattern, same `DataTable`/`FilterPanel`/`SearchBar` composition, same masking approach. Reuse C.21 N-01's masking utility/component if it exists as a shared piece, rather than reimplementing.

## 7. Existing Code to Reuse
- `BaseResourceClient<TEntity, never, never, TFilters>` pattern (verbatim from C.21 N-01).
- `DataTable`, `SearchBar`, `FilterPanel`, `usePaginationState`, `useDebouncedValue`, `RequirePermission`, `StatusBadge` — all reused as-is per C.21 N-01's precedent.
- C.21 N-01's masking utility for family identifiers, if shared — confirm before writing a second one.

## 8. Files to Create
- `src/features/data-request-audit/api/data-request-resource-client.ts`
- `src/features/data-request-audit/api/schemas.ts`
- `src/features/data-request-audit/hooks/use-data-requests.ts`
- `src/features/data-request-audit/index.ts`
- `src/app/(dashboard)/support/data-requests/page.tsx`

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `API_ENDPOINTS.DATA_REQUESTS.BASE`.
- Sidebar navigation — add under Support, gated by `RequirePermission`.

## 10. Backend Requirements
Consumes B-08 exclusively (`GET /v1/admin/data-requests`).

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- `DataRequestResourceClient extends BaseResourceClient<DataRequest, never, never, DataRequestFilters>` — the `never` generics are the same deliberate compile-time mutation guard C.21 N-01 uses.
- `useDataRequests(filters)` — React Query hook following the `useDeletionCases`/`useFamilyList` pattern exactly.
- Page composes `FilterPanel` (type: export/delete, status: preparing/ready/failed) + `SearchBar` (debounced, masked-identifier search) + `DataTable`.
- `RequirePermission permission="data-requests:read"` — confirm/add to `AdminPermission` catalog, mapped to backend `support`/`trust_safety`/`compliance`.

## 13. API Contract
Consumes B-08's contract as documented in that blueprint.

## 14. Database Requirements
Not applicable.

## 15. Validation
Filter inputs only (type/status enums, free-text search) — no submission form on this page.

## 16. Authentication
`useAdminSession()`.

## 17. Authorization
`RequirePermission` wraps the entire page and the sidebar entry.

## 18. Error Handling
- `QueryErrorState`, `EmptyState`, `LoadingState` — all reused shared components.
- `403` from backend (missing scope) → clear insufficient-permissions message.

## 19. Offline First
Not applicable.

## 20. Local Data
Not applicable.

## 21. Localization
Column headers, status labels, filter labels, search placeholder via `useTranslation()`; dates via `useFormatters().formatDate`.

## 22. RTL
Full RTL mirroring for table and filter panel, consistent with C.21 N-01's established pattern.

## 23. Analytics
Not specified; follow the platform's existing admin page-view convention if one exists, otherwise none added.

## 24. Performance
Server-side pagination via `DataTable`'s existing props, debounced search (300ms, matching the established convention) — never fetch the full dataset client-side.

## 25. Security
- `never` generic-type guard is the primary structural control preventing accidental mutation code.
- No restore/delete/edit affordance anywhere in the page's component tree, verified by a negative test.
- Masked identifiers only, never raw `family_id`.

## 26. Library Requirements
No new libraries.

## 27. Testing
- Unit: `DataRequestResourceClient` Zod validation.
- Integration/UI: pagination, filtering by type/status, debounced search.
- Integration/UI: `RequirePermission` correctly hides page/nav-entry for unauthorized roles.
- Negative test: no restore/delete/edit affordance exists anywhere in the rendered page (mirrors C.21 N-01's identical test).

## 28. Documentation
Document that this resource is intentionally read-only by design, cross-referencing B-08 and C.21 N-01's identical established pattern.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm B-08 Endpoint and Reuse C.21 N-01's Masking Utility**
- **Objective:** Confirm B-08's finalized path and locate C.21 N-01's masking helper if shared.

**Task 02 — Zod Schemas & Resource Client**
- **Files to Create:** `schemas.ts`, `data-request-resource-client.ts`.
- **Implementation Details:** `never` generics for create/update, mirroring C.21 N-01 exactly.

**Task 03 — `useDataRequests` Hook**

**Task 04 — Page Composition & Navigation Entry**
- **Files to Create:** `page.tsx`.
- **Tests:** negative no-mutation-affordance test.

**Task 05 — Localization, RTL, Full Test Suite & Documentation**

## 30. Definition of Done
A read-only, paginated, masked, permission-gated Data Subject Request Audit Log is live, structurally prevented from ever growing a mutation path, and directly mirrors C.21 N-01's already-proven pattern.

## 31. Final Verification Checklist
- [ ] `DataRequestResourceClient` uses `never` for create/update generics
- [ ] No mutation UI exists anywhere on the page (negative test passes)
- [ ] Pagination and debounced search verified
- [ ] `RequirePermission` correctly gates page and nav entry for `support`/`trust_safety`/`compliance`
- [ ] Masking utility reused from C.21 N-01 if available, not duplicated
- [ ] Full localization and RTL verified
