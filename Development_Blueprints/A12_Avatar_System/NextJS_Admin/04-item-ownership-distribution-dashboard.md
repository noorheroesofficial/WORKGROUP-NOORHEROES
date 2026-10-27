# N-04 — Item Ownership Distribution Dashboard

## 1. Feature Context
NoorHeroes Admin Portal (Next.js). Part of Feature A.12 — Avatar System. Read-only "Ownership Distribution" tab on each item's detail page, showing aggregate owned/equipped counts, backed by B-06.

## 2. Parent Feature
A.12 Avatar System — NextJS Admin

## 3. Sub-feature
N-04 Item Ownership Distribution Dashboard

## 4. Objective
Build a read-only ownership-distribution view surfacing aggregate owned/equipped counts per `avatar_item`, sourced from B-06's aggregate endpoint, never listing individual child identities — backing PRD §8/§9 item 3 and §11.3 Dashboard Metrics.

## 5. Business Requirements
- Aggregate-only display — never surfaces individual child identities, consistent with the platform's privacy-by-design principle (mirrors B-06's structural guarantee).
- Purely read-only; no mutating action on this surface.
- Serves as a content-popularity signal for future asset investment (PRD §8) and feeds the "most/least-popular equipped items" dashboard metric (PRD §11.3).

## 6. Existing Architecture
Follows the existing Admin Portal shell, integrated as a tab within N-02's item detail view (`src/app/(dashboard)/avatars/items/[itemId]/page.tsx` or a tab within the existing item edit dialog/detail route, depending on how N-02 structures its detail navigation — this task adds the "Ownership Distribution" tab to whichever detail surface N-02 establishes, not a standalone new route, per PRD §9's "Read-only 'Ownership Distribution' tab on each item's detail page" framing).

## 7. Existing Code to Reuse
- `DataTable`/chart component library already used elsewhere in the Admin Portal for aggregate dashboards (e.g., any existing analytics-summary widget pattern)
- `RequirePermission`, `hasPermission`, `useAdminSession` (per N-01/N-02/N-03)
- N-02's item detail navigation shell (this task extends it with a new tab rather than building a separate page)

## 8. Files to Create
- `src/features/avatar-items/components/OwnershipDistributionTab.tsx`
- `src/features/avatar-items/hooks/use-ownership-distribution.ts`

## 9. Files to Modify
- `src/features/avatar-items/components/AvatarItemFormDialog.tsx` or the item detail route established by N-02 — add the "Ownership Distribution" tab

## 10. Backend Requirements
Consumes B-06 (`GET /v1/admin/avatar-items/{itemId}/ownership-distribution`).

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- `OwnershipDistributionTab` displays `owned_count` and `equipped_count` as simple aggregate stat cards (or a small comparison chart if the Admin Portal has an existing lightweight charting convention — reuse it rather than introducing a new charting library for two numbers).
- Read-only; no form controls, no mutating actions.
- Loading, empty (zero-owner item), and error states per existing Admin Portal conventions.
- `RequirePermission permission="avatars:items:read"` (or the item catalog's existing read-scope convention) guarding tab visibility, consistent with N-02's broader read/write scope split.

## 13. API Contract
`GET /v1/admin/avatar-items/{itemId}/ownership-distribution` (B-06) — Admin API, Bearer admin session, `content_editor`/`trust_safety` scope.

## 14. Database Requirements
N/A (frontend consumes backend API only).

## 15. Validation
N/A (read-only, no form input).

## 16. Authentication
`useAdminSession` — admin Bearer session required.

## 17. Authorization
`RequirePermission` guarding tab visibility; backend (B-06) is the authoritative enforcement point and the sole source of the aggregate-only guarantee — the frontend does not attempt any additional aggregation or child-level lookup that could reintroduce a privacy leak.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Item has zero owners | Display `0`/`0` counts with a neutral "not yet owned by any child" framing, not an error state |
| Network/API failure | Error state with retry |
| Unauthorized | `RequirePermission` hides the tab; direct API `403` surfaced as a toast if somehow reached |

## 19. Offline First
Not applicable (Admin Portal is online-only by design).

## 20. Local Data
Not applicable.

## 21. Localization
Follow existing Admin Portal localization conventions (verify against existing pages, per N-01's precedent flag).

## 22. RTL
Follow existing Admin Portal RTL support level (verify against existing pages, per N-01's precedent flag).

## 23. Analytics
Not applicable (internal admin tooling, read-only aggregate display).

## 24. Performance
Single lightweight API call per tab view; React Query caching with a sensible stale-time given the aggregate data's low-precision-requirement nature (mirrors B-06's Redis-cached aggregate on the backend side).

## 25. Security
Aggregate-only response consumption — the frontend must never attempt to enrich this view with any additional child-identifying data from another endpoint, preserving the privacy-by-design guarantee established at the API layer (B-06).

## 26. Library Requirements
Next.js App Router, React Query, existing Admin Portal shared component/chart library.

## 27. Testing
Component test for `OwnershipDistributionTab` rendering across populated/zero-owner/error states; hook test for `use-ownership-distribution`; regression test confirming the component renders no child-identifying field even if a malformed/unexpected API response were to include one (defensive test, mirroring the backend's own schema-scan guarantee).

## 28. Documentation
Document the tab's integration point within N-02's item detail view in the Admin Portal's navigation/feature documentation.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement `use-ownership-distribution` Hook**
- Objective: React Query wrapper around B-06's endpoint.
- Files to Create: `hooks/use-ownership-distribution.ts`
- Tests: hook unit test (mocked API repository).
- Definition of Done: hook correctly fetches and caches the aggregate response.

**Task 02 — Build `OwnershipDistributionTab` Component**
- Objective: read-only aggregate stat display.
- Files to Create: `components/OwnershipDistributionTab.tsx`
- Existing Files to Reuse: existing Admin Portal stat-card/chart component convention.
- Tests: component render tests for populated/zero-owner/error states; defensive test confirming no child-identifying field is ever rendered.
- Definition of Done: tab renders correctly across all documented states.

**Task 03 — Integrate Tab into N-02's Item Detail View**
- Files to Modify: `AvatarItemFormDialog.tsx` or N-02's item detail route.
- Definition of Done: "Ownership Distribution" tab reachable from the existing item detail surface without disrupting N-02's existing form/table behavior.

**Task 04 — Final Code Review**
- Do Not Change: N-02's existing create/edit form logic beyond the additive tab integration; B-06's backend aggregate-only guarantee (frontend must not attempt to circumvent it).
- Expected Result: PR merge-ready.

## 30. Definition of Done
Ownership Distribution tab live within the item detail view, correctly displaying aggregate-only owned/equipped counts with zero individual child identities ever rendered, across all documented states.

## 31. Final Verification Checklist
- [ ] Tab displays correct aggregate owned/equipped counts
- [ ] Zero-owner item renders a neutral empty state, not an error
- [ ] No child-identifying field ever rendered (defensive test passing)
- [ ] `RequirePermission` guards tab visibility
- [ ] Loading/error states implemented
- [ ] Component and hook tests passing
- [ ] Tab correctly integrated into N-02's existing item detail view without disrupting existing behavior
