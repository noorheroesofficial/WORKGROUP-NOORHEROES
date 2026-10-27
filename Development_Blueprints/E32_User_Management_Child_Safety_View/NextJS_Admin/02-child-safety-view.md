# N-02 — Child-Safety View

## 1. Feature Context
A masked, read-only, tightly scoped window into a specific child's age-band, progress, and safety-flag history — reusing N-01's `MaskedField` component so this second surface never introduces a divergent masking implementation.

## 2. Parent Feature
E.32 — User Management & Child Safety View

## 3. Sub-feature
2.2 Child-Safety View (ID: **N-02**)

## 4. Objective
Build the Child-Safety View and Moderation/Flag History screens, reusing N-01's `MaskedField`, scoped strictly to the referenced child with no incidental sibling surfacing.

## 5. Business Requirements
- Displays age-band, learning progress, moderation-flag history, and AI-safety-flag counts for a single child.
- Masked by default, same as N-01.
- Scoped strictly to the child being viewed — never incidentally lists or links to sibling children without an explicit, separate navigation action.

## 6. Existing Architecture
`src/features/child-safety-view/` module, reached from N-01's parent detail (child list) or directly via B-01 search results.

## 7. Existing Code to Reuse
- N-01's `MaskedField` (reused as-is)
- `src/shared/components/require-permission.tsx::RequirePermission`
- `src/shared/components/data-table.tsx::DataTable` (flag history)

## 8. Files to Create
- `src/app/(dashboard)/users/children/[childId]/page.tsx`
- `src/features/child-safety-view/api/child-safety-repository.ts`
- `src/features/child-safety-view/hooks/use-child-safety-detail.ts`, `use-flag-history.ts`
- `src/features/child-safety-view/components/child-profile-summary.tsx`
- `src/features/child-safety-view/components/moderation-flag-history-table.tsx`
- `src/features/child-safety-view/components/safety-flag-count-badge.tsx`
- `src/features/child-safety-view/types/child-safety.ts` — Zod schema

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `CHILD_SAFETY.*` endpoints

## 10. NextJS Requirements
- `ChildProfileSummary`: uses `MaskedField` from N-01 for any PII-adjacent field (e.g., name) — no local reimplementation.
- `ModerationFlagHistoryTable`: read-only, chronological, scoped exclusively via `childId` route param — the repository call is parameterized so no cross-child data can leak into the view.
- Unmask-request entry point identical pattern to N-01, scoped to `child_id` instead of `parent_id`.

## 11. Required API
**Admin API** — child-safety read endpoints (owned within B-01/B-02's masking path, extended to child-scoped reads if a dedicated backend read path is needed — confirmed as reusing B-02's masking service against child-scoped queries, no new backend sub-feature required).

## 12. Authentication / Authorization
`useAdminSession()` base auth; `RequirePermission permission="support"`.

## 13. Loading / Empty / Error States
Loading skeleton; "No flags on record" empty state for flag history; not-found state for an invalid `childId`.

## 14. Responsive UI / Accessibility
Same masked-field accessibility treatment as N-01.

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()`.

## 16. Security
Strict `childId`-scoped queries only — mandatory test confirms the flag-history table never renders rows belonging to a different child than the route param, even if the API response were malformed (component-level defensive filter as a second layer beyond the API contract).

## 17. Testing
Unit: `childId`-scoping defensive filter. UI: reuse of `MaskedField` confirmed (no duplicate masking component). Integration: full navigate-to-child → masked-view-loads → unmask-request-entry-point-scoped-correctly flow.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schema & Add API Endpoints**
Objective: `child-safety.ts` schema. Files: `types/child-safety.ts`, `api-endpoints.ts`. Tests: schema validation. Definition of Done: schema used by Task 03.

**Task 02 — Implement `ChildSafetyRepositoryImpl`**
Objective: `childId`-parameterized repository calls. Tests: mocked-fetch tests. Dependencies: Task 01. Definition of Done: tests pass.

**Task 03 — Implement `ChildProfileSummary` (Reusing `MaskedField`)**
Objective: Confirm direct reuse from N-01. Dependencies: N-01, Task 02. Tests: reuse-not-duplication check. Definition of Done: zero duplicated masking code.

**Task 04 — Implement `ModerationFlagHistoryTable`**
Objective: `childId`-scoped, defensively filtered table. Dependencies: Task 02. Tests: **mandatory** — cross-child-leak defensive-filter test. Definition of Done: test passes.

**Task 05 — Implement the Child-Safety View Page**
Objective: Compose summary + flag history + unmask entry point. Dependencies: Tasks 03–04. Tests: full-page smoke test. Definition of Done: test passes.

**Task 06 — Add Full Test Suite**
Objective: Complete coverage per §17. Definition of Done: all green in CI.

**Task 07 — Final Code Review**
Objective: Confirm zero duplicated masking logic exists outside N-01's `MaskedField`. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] `MaskedField` reused from N-01, not duplicated
- [ ] Flag history strictly scoped to the route `childId` — mandatory defensive-filter test passing
- [ ] Unmask-request entry point correctly scoped to `child_id`
- [ ] No incidental sibling-child data surfaced

## 20. Definition of Done
Support staff have a masked, strictly-scoped Child-Safety View built entirely on N-01's proven masking component, with zero duplicated or divergent masking logic.
