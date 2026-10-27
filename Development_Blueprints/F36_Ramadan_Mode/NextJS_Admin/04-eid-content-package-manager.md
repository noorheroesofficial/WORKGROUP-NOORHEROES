# N-04 — Eid Content Package Manager

## 1. Feature Context
Manages the celebration-content assignments (Eid Home imagery, reward-reveal content, card templates) that power K-05's Eid experience, reusing E.29's existing Media Library rather than building a parallel media manager.

## 2. Parent Feature
F.36 — Ramadan Mode

## 3. Sub-feature
3.4 Eid Content Package Manager (ID: **N-04**)

## 4. Objective
Build a CRUD interface for Eid-transition/celebration content assignments, reusing E.29's Media Library for asset selection.

## 5. Business Requirements
- §8: Eid Content Package Manager — manages Eid-transition/celebration content.
- §9 Admin AI prompt item 4: manages Eid content assignments, reusing E.29's Media Library.

## 6. Existing Architecture
`src/features/ramadan/eid-package-manager/`, reusing E.29's existing media-selection component/hook (confirm exact name in E.29's feature module before implementation — do not invent one).

## 7. Existing Code to Reuse
- E.29's Media Library selector component (exact name TBD, confirm before implementation)
- `DataTable`, `RequirePermission`, `LoadingState`, `EmptyState`, `ErrorView`

## 8. Files to Create
- `src/app/(dashboard)/ramadan/eid-package/page.tsx`
- `src/features/ramadan/eid-package-manager/api/eid-package-resource-client.ts`
- `src/features/ramadan/eid-package-manager/hooks/use-eid-package.ts`
- `src/features/ramadan/eid-package-manager/components/eid-package-form.tsx`
- `src/features/ramadan/eid-package-manager/components/eid-package-list.tsx`
- `src/features/ramadan/eid-package-manager/types/eid-package.ts`

## 9. Files to Modify
- `src/shared/components/dashboard-shell.tsx` — add "Eid Package" nav entry under Ramadan

## 10. NextJS Requirements
- **Page/Route:** `/ramadan/eid-package`.
- **Component:** `EidPackageList` (assigned Eid-content items — Eid Home theme assets, reward-reveal content, card templates); `EidPackageForm` (assignment form embedding E.29's Media Library selector for asset picking).
- **Form/Validation:** required fields before publish (e.g., at least one Eid Home theme asset and one card template assigned) — exact required-field set to confirm against E.29's media schema/§9's description rather than invented wholesale.
- **Loading/Empty/Error State:** standard shared-component states.
- **Responsive UI/Accessibility:** standard `DataTable`/form patterns.

## 11. API Contract
**Flagged, do not guess:** content-assignment endpoints against E.29's Media Library are not enumerated in PRD §3.4 — confirm against E.29's actual Media Library API surface before implementation.

## 12. Database Requirements
N/A directly — reads/writes E.29's media tables and `ramadan_missions`/Eid-scoped content references via their backend APIs only.

## 13. Validation
Required-field validation before publish per §10; asset type/format validation delegated to E.29's existing Media Library validation (reused, not duplicated).

## 14. Authentication
Standard Admin Portal session.

## 15. Authorization
`RequirePermission permission="ramadan_content_schedule:write"` — behind `content_editor` per §8.

## 16. Error Handling
`QueryErrorState` for fetch failures; form-level error surfacing for save failures, with the Media Library's own error handling reused for asset-selection failures rather than reimplemented.

## 17. Localization
Form labels and list copy via `useTranslation()`.

## 18. RTL
Form/list layout direction-aware.

## 19. Analytics
Consistent with the Admin Portal's existing action-audit pattern if present.

## 20. Performance
Small, infrequently-changed dataset — no special performance consideration; Media Library selector's own performance characteristics are inherited as-is.

## 21. Caching
React Query caching for the package list, invalidated on save.

## 22. Testing
Component tests: `EidPackageForm` required-field validation. Integration test: full assign-Eid-content flow reflects correctly for K-05's consuming screens on next fetch.

## 23. Documentation
Inline JSDoc noting all asset selection must go through E.29's Media Library component — no independent upload/asset-management UI in this module.

## 24. AI Coding Agent Implementation Steps

**Task 01 — Confirm E.29's Media Library Component and API Contract**
Objective: Resolve the flagged gap in §11 and identify the exact reusable component. Definition of Done: findings documented before Task 03.

**Task 02 — Define Types**
Objective: `EidPackage`, `EidPackageAssignment`. Files to Create: `types/eid-package.ts`. Definition of Done: types compile.

**Task 03 — Implement `EidPackageResourceClient`**
Objective: CRUD for Eid content assignments. Files to Create: `api/eid-package-resource-client.ts`. Dependencies: Task 01, Task 02. Tests: repository unit tests. Definition of Done: tests pass.

**Task 04 — Implement `useEidPackage` Hook**
Objective: React Query list/mutation hook. Files to Create: `hooks/use-eid-package.ts`. Dependencies: Task 03. Tests: hook tests. Definition of Done: tests pass.

**Task 05 — Build `EidPackageForm` Embedding E.29's Media Library Selector**
Objective: Assignment form with required-field validation. Files to Create: `components/eid-package-form.tsx`. Existing Files to Reuse: E.29's Media Library selector. Dependencies: Task 04. Tests: required-field validation test. Definition of Done: test passes.

**Task 06 — Build `EidPackageList`**
Objective: List/table of current assignments. Files to Create: `components/eid-package-list.tsx`. Dependencies: Task 04. Tests: rendering tests. Definition of Done: tests pass.

**Task 07 — Build the Page and Wire Navigation**
Objective: `/ramadan/eid-package` page. Files to Create: `app/(dashboard)/ramadan/eid-package/page.tsx`. Files to Modify: `dashboard-shell.tsx`. Dependencies: Task 05, Task 06. Tests: page integration test. Definition of Done: test passes.

**Task 08 — Add Localization and Full Test Suite**
Objective: Complete §17/§22 coverage. Definition of Done: all green in CI.

**Task 09 — Final Code Review**
Objective: Confirm zero independent media-upload/management UI exists outside E.29's reused component. Definition of Done: checklist in §26 checked.

## 25. Definition of Done
Editors can assemble the complete Eid celebration content package entirely through E.29's existing Media Library, with zero parallel asset-management surface.

## 26. Final Verification Checklist
- [ ] Media Library API contract confirmed, not guessed, before implementation
- [ ] All asset selection routed through E.29's reused component
- [ ] Required-field validation blocks incomplete publish
- [ ] Assignment changes correctly reflected in K-05's consuming screens
