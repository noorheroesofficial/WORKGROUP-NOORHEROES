# N-03 — Override Audit Log

## 1. Feature Context
A read-only, paginated view into every `parent_overrides` record for support/trust-safety dispute investigation, with child identifiers masked (PRD C.23 §8, §9).

## 2. Parent Feature
Feature C.23 — Parental Controls (Screen Time, Bedtime, AI Permissions, Content Age Level)

## 3. Sub-feature
3.3 Override Audit Log (ID: **N-03**)

## 4. Objective
Build a paginated, searchable/filterable table of `parent_overrides` records (masked child identifier, type, minutes_granted, granted_by, timestamp), restricted to `support`/`trust_safety` roles, using the platform's standard `DataTable` component.

## 5. Business Requirements
- §8: Override Audit Log is read-only, behind `support`/`trust_safety`.
- Consistent with the platform's general append-only-audit-table read-access pattern (B-03's `parent_overrides` table).

## 6. Existing Architecture
Follows the exact `DataTable` + `usePaginationState` + `useDebouncedValue` pattern already established for `UsersPage` (per NEXT-JS-INSTRUCTIONS.md §11 Pattern 1) — this file is a close structural match to that existing example.

## 7. Existing Code to Reuse
- `DataTable`, `usePaginationState`, `useDebouncedValue`, `SearchBar`, `FilterPanel`
- `RequirePermission`
- `apiClient`/`BaseResourceClient` (this resource is a natural fit for `BaseResourceClient<OverrideAuditEntry, never, never, OverrideAuditFilters>` since it's list-only, no create/update/delete)

## 8. Files to Create
- `src/features/restriction-engine/api/override-audit.repository.ts` (extends `BaseResourceClient`, `list()` only exposed/used)
- `src/features/restriction-engine/api/schemas.ts` (extend from N-01, add `overrideAuditEntrySchema`, `paginatedOverrideAuditSchema`)
- `src/features/restriction-engine/hooks/use-override-audit-log.ts`
- `src/app/(dashboard)/restriction-engine/override-audit/page.tsx`
- `src/features/restriction-engine/__tests__/override-audit-log.test.tsx`

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `RESTRICTION_ENGINE.OVERRIDE_AUDIT`
- Sidebar navigation config — add "Override Audit Log" entry under a Trust & Safety section

## 10. NextJS Requirements
- `override-audit.repository.ts`: extends `BaseResourceClient<OverrideAuditEntry, never, never, OverrideAuditFilters>`, only `list(filters, signal)` is meaningfully used (create/update/delete are structurally unavailable for this read-only resource — do not expose action buttons for them anywhere in the UI).
- `useOverrideAuditLog(filters)`: React Query hook wrapping `list()`, following `useUsers`'s exact structure.
- Page component: mirrors the `UsersPage` pattern in NEXT-JS-INSTRUCTIONS.md §11 Pattern 1 — `FilterPanel` with `SearchBar` (search by masked child ref or `granted_by`), `DataTable` with columns for masked child identifier, type (`screen_time`/`bedtime`), `minutes_granted`, `granted_by`, `created_at` (formatted via `useFormatters().formatDate`).
- No row-level actions — this table has no edit/delete affordance anywhere in the UI, reflecting the backend's append-only, no-UPDATE/DELETE-grant design (B-03).

## 11. API Contract
### Required API (consumed)
- **HTTP Method:** GET — **Endpoint:** `/v1/admin/restrictions/overrides` (B-07, reading B-03's `parent_overrides`)
- **Authentication:** Bearer (admin), `support`/`trust_safety` scope
- **Response:** `PaginatedResponse<OverrideAuditEntry>` — `{ items, total, page, limit, totalPages }`, `child_id` masked

## 12. Database Requirements
N/A (frontend; backed by B-07/B-03's tables).

## 13. Validation
- Filter/search inputs validated as standard query-param shapes (date range, optional type filter) via Zod, matching `UserQueryFilters`'s pattern.

## 14. Authentication
Standard admin session (`useAdminSession()`).

## 15. Authorization
`RequirePermission permission="restriction_engine:override_audit:read"` (confirm exact string against actual `AdminPermission` enum — likely gated to `support`/`trust_safety` roles specifically, distinct from `product_admin`).

## 16. Error Handling
| Scenario | UI Behavior |
|---|---|
| Load failure | `DataTable`'s built-in `error`/`onRetry` handling |
| Empty result set | `DataTable`'s built-in empty state |
| Unauthorized (wrong role) | `RequirePermission` fallback (page-level, not just button-level) |

## 17. Offline First
N/A (admin web app).

## 18. Local Data
N/A.

## 19. Localization
Column headers, filter labels, and empty/error state copy via `useTranslation()`; dates via `useFormatters().formatDate`.

## 20. RTL
Table and filter panel must support RTL locales if enabled for the Admin Portal.

## 21. Analytics
No analytics events specified for this admin surface by the PRD beyond the audit data itself being the analytics artifact.

## 22. Performance
Standard server-side pagination via `DataTable`'s `page`/`pageSize`/`totalItems` props — never fetch the full unpaginated dataset client-side, consistent with `UsersPage`'s established pattern.

## 23. Security
Masked child identifiers even for authorized support/trust-safety staff — this is a deliberate PII-minimization design from B-07, and the frontend must not attempt to "unmask" or cross-reference the identifier client-side (no client-side join to a full child-profile lookup on this page).

## 24. Library Requirements
Next.js 15, TanStack Query v5, existing `DataTable`/`BaseResourceClient` infrastructure. No new dependencies.

## 25. Testing
- Component test: table renders masked identifiers correctly (never the raw `child_id`).
- Component test: no edit/delete action rendered anywhere in the row actions.
- Component test: pagination and search/filter wiring, mirroring `UsersPage`'s existing test pattern if one exists (reuse as a template).
- Component test: `RequirePermission` correctly blocks access for a non-support/trust_safety admin role.

## 26. Documentation
Inline comment noting explicitly that this page must never render an unmasked child identifier or add write actions, given the backend's deliberate append-only/PII-minimization design.

## 27. AI Coding Agent Implementation Steps

**Task 01 — Confirm Exact `AdminPermission` Strings for `support`/`trust_safety`**
- Objective: Verify against the real `AdminPermission` enum before use.

**Task 02 — Add API Endpoint Constant**
- Files to Modify: `api-endpoints.ts`

**Task 03 — Extend Zod Schemas**
- Files to Modify: `src/features/restriction-engine/api/schemas.ts`

**Task 04 — Implement `override-audit.repository.ts`**
- Files to Create: extends `BaseResourceClient`, list-only usage.

**Task 05 — Implement `useOverrideAuditLog` Hook**
- Files to Create: `use-override-audit-log.ts`

**Task 06 — Implement Page Component**
- Files to Create: `page.tsx`
- Implementation Details: Mirror `UsersPage`'s exact structure from NEXT-JS-INSTRUCTIONS.md §11 Pattern 1.

**Task 07 — Add Sidebar Navigation Entry**

**Task 08 — Add Masked-Identifier Rendering Test**

**Task 09 — Add No-Write-Actions Test**

**Task 10 — Add Pagination/Filter Tests**

**Task 11 — Add RBAC-Gating Test**

**Task 12 — Final Code Review**
- Objective: Confirm no unmasking logic and no write actions anywhere on this page.

## 28. Definition of Done
- Table displays masked identifiers, paginated, searchable/filterable.
- No edit/delete actions present anywhere.
- RBAC correctly restricts to `support`/`trust_safety` roles.

## 29. Final Verification Checklist
- [ ] Confirmed real `AdminPermission` strings for support/trust_safety
- [ ] Child identifiers rendered masked, never raw
- [ ] No write/edit/delete action anywhere on this page
- [ ] Server-side pagination used (no full-dataset client fetch)
- [ ] RBAC-gating tested
- [ ] Localization strings added
