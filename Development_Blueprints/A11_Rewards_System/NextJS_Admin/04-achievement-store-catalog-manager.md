# N-04 — Achievement Store Catalog Manager

## 1. Feature Context
Part of Feature A.11 — Rewards System. Admin CRUD for the Achievement Store catalog, with "Deactivate" as the only removal affordance.

## 2. Parent Feature
A.11 Rewards System — NextJS Admin

## 3. Sub-feature
N-04 Achievement Store Catalog Manager

## 4. Objective
Build the Achievement Store Catalog Manager page consuming B-12, restricted to `content_editor`, per PRD §8/§9.

## 5. Business Requirements
- CRUD for `catalog_items` (type, `price_points`, `eligibility_json`, `active` toggle).
- Delete relabeled "Deactivate" (`active=false` only) — preserves existing ownership records; no destructive delete affordance anywhere in the UI.
- Restricted to `content_editor` role.

## 6. Existing Architecture
Existing Admin Portal shell; mirrors the catalog-manager pattern already established for other content catalogs (e.g., A.5/A.6's content managers), reusing `DataTable`, `RequirePermission`, `ConfirmationDialog`.

## 7. Existing Code to Reuse
- `BaseResourceClient`, `DataTable`, `RequirePermission`, `ConfirmationDialog`, `CurrencyText`/`MoneyField`-style numeric input pattern (adapted for `price_points`, a points value rather than currency, but reusing the same input-component structure).

## 8. Files to Create
- `src/features/rewards/catalog/CatalogItemResourceClient.ts`
- `src/features/rewards/catalog/CatalogManagerPage.tsx`
- `src/features/rewards/catalog/CatalogItemForm.tsx`
- `src/features/rewards/catalog/__tests__/CatalogManagerPage.test.tsx`

## 9. Files to Modify
- Admin route registry — `/rewards/catalog`.
- Admin nav/sidebar config.

## 10. Backend Requirements
Consumes B-12 (`/v1/admin/rewards/catalog-items`, `.../deactivate`).

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- `CatalogManagerPage` renders items via `DataTable` with category filter, active/inactive `StatusBadge`.
- Row action is "Deactivate" (via `ConfirmationDialog`, explaining that this preserves existing ownership records), never "Delete" — the UI has no delete affordance at all, matching B-12's structural guarantee.
- `CatalogItemForm` validates `price_points > 0` client-side.

## 13. API Contract
Per B-12 §13.

## 14. Database Requirements
N/A (admin frontend).

## 15. Validation
UI test confirming no "Delete" button/menu-item exists anywhere on this page, only "Deactivate."

## 16. Authentication
Reuses existing Admin session/auth flow.

## 17. Authorization
`RequirePermission` gate for `content_editor`.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Invalid `price_points` (≤0) | Inline validation error |
| Fetch failure | `ErrorView` with retry |
| Empty catalog | `EmptyState` with "add your first item" call to action |
| Deactivate confirmation cancelled | No change, dialog closes |

## 19. Offline First
Not applicable (admin web).

## 20. Local Data
Not applicable.

## 21. Localization
Admin UI localized; item name/description fields captured per the platform's multilingual content-authoring convention.

## 22. RTL
Table/form layout mirrors correctly for Arabic admin locale.

## 23. Analytics
N/A (audit-logged server-side).

## 24. Performance
`DataTable` pagination/filtering by type and active status for large catalogs.

## 25. Security
Structural absence of a delete affordance in the UI mirrors B-12's backend guarantee — a defense-in-depth pairing preventing accidental ownership-record breakage.

## 26. Library Requirements
Existing Admin Portal stack.

## 27. Testing
- Unit: `price_points` validation.
- Integration: full CRUD + deactivate flow, no-delete-affordance UI test (mandatory).

## 28. Documentation
Component README noting "Deactivate" is intentionally the only removal action, cross-referenced against B-12.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement `CatalogItemResourceClient`**
- Files to Create: `CatalogItemResourceClient.ts`
- Existing Files to Reuse: `BaseResourceClient`.
- Definition of Done: `list()`/`create()`/`update()`/`deactivate()` implemented; no `delete()` method exposed.

**Task 02 — Build `CatalogManagerPage`**
- Files to Create: `CatalogManagerPage.tsx`
- Existing Files to Reuse: `DataTable`, `RequirePermission`, `ConfirmationDialog`.
- Definition of Done: category filter, active/inactive badge, Deactivate action functional.

**Task 03 — Build `CatalogItemForm`**
- Files to Create: `CatalogItemForm.tsx`
- Implementation Details: `price_points > 0` validation.
- Tests: no-delete-affordance UI test (mandatory).
- Definition of Done: test passing.

**Task 04 — Wire Route, Nav, and Permission Gate**
- Files to Modify: route registry, nav config.
- Definition of Done: `/rewards/catalog` reachable only to `content_editor`.

**Task 05 — Documentation & Final Review**
- Documentation: README per §28.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Achievement Store Catalog Manager live, deactivate-only removal enforced in the UI, RBAC-gated.

## 31. Final Verification Checklist
- [ ] No "Delete" affordance exists anywhere on this page
- [ ] Deactivate confirmation explains ownership-preservation clearly
- [ ] `price_points > 0` validated client- and server-side
- [ ] `RequirePermission` restricts to `content_editor`
- [ ] Empty/loading/error states render correctly
- [ ] Localization and RTL verified
