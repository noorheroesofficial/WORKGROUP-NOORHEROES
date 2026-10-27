# N-06 — Editorial & Scholar Review Queues

## 1. Feature Context
The review workspaces for translation strings, built entirely on E.29's existing queue and decision-bar components — general UI copy through editorial-only review, Islamic-content-adjacent strings additionally through scholar review, with zero UI reimplementation of the segregation-of-duties pattern already proven there.

## 2. Parent Feature
E.34 — Localization Management

## 3. Sub-feature
2.6 Editorial & Scholar Review Queues (ID: **N-06**)

## 4. Objective
Build the Editorial Review Queue and Scholar Review Queue screens for translation strings, reusing E.29 N-04/N-05's queue-list, decision-bar, and self-review-block components directly, scoped to `item_type='locale_string_version'`.

## 5. Business Requirements
- §1.18 screens 10–11: Editorial Review Queue (general UI copy), Scholar Review Queue (Islamic-content-adjacent strings, shared with E.29).
- FR-10: Islamic-content-adjacent strings route through the same scholar-review discipline as E.29.
- Edge Case 2: a scholar rejection returns the specific locale's version to Draft without affecting other locales' published translations of the same key.

## 6. Existing Architecture
`src/features/translation-review/` module — a thin, scoped wrapper around E.29's existing `src/features/scholar-review/` and equivalent editorial-review components, not a parallel implementation.

## 7. Existing Code to Reuse
- E.29 N-04: `src/features/scholar-review/components/decision-action-bar.tsx::DecisionActionBar`, `segregation-of-duties-block.tsx::SegregationOfDutiesBlock` (reused directly, `isSelfEdited` logic unmodified)
- E.29 N-04/N-05's queue-list and pagination patterns
- `src/shared/hooks/use-pagination-state.ts::usePaginationState`

## 8. Files to Create
- `src/app/(dashboard)/review/translation-editorial-queue/page.tsx`
- `src/app/(dashboard)/review/translation-scholar-queue/[id]/page.tsx`
- `src/features/translation-review/api/translation-review-repository.ts` — thin wrapper scoping E.29's existing review endpoints to `item_type='locale_string_version'`
- `src/features/translation-review/hooks/use-translation-review-queue.ts`, `use-translation-review-detail.ts`
- `src/features/translation-review/components/translation-diff-view.tsx` — before/after string value comparison, reusing E.29's `VersionDiffPanel` pattern

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `TRANSLATION_REVIEW.*` (scoped query params on E.29's existing endpoints, not new endpoints)
- `src/shared/components/dashboard-shell.tsx` — nav items under existing "Review" navigation group

## 10. NextJS Requirements
- `TranslationReviewRepositoryImpl`: calls E.29's exact `GET /v1/admin/reviews`/`PATCH /v1/admin/reviews/{id}` endpoints with `item_type=locale_string_version` filtering — no new backend contract, confirmed against B-05's polymorphic queue-item extension.
- Queue and detail screens directly reuse `DecisionActionBar`/`SegregationOfDutiesBlock` from E.29 N-04 — the `isSelfEdited` derivation logic is imported, not reimplemented, so any future security fix to that logic automatically applies here.
- `TranslationDiffView`: reuses E.29's diff-rendering approach, adapted for plain-string (and ICU-formatted) value comparison rather than rich content.

## 11. Required API
**Admin API** — B-05 (via E.29's existing endpoints): `GET /v1/admin/reviews?item_type=locale_string_version`, `PATCH /v1/admin/reviews/{id}`.

## 12. Authentication / Authorization
`useAdminSession()` base auth; `RequirePermission permission="localization_manager"` for the editorial queue; `RequirePermission permission="scholar_reviewer"` for the scholar queue (identical to E.29's gating).

## 13. Loading / Empty / Error States
Reused directly from E.29 N-04/N-05's established states ("Queue clear", decision-submission errors, SoD-blocked state).

## 14. Responsive UI / Accessibility
Reused directly from E.29 N-04/N-05's established accessibility treatment.

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()`; the string values under review may themselves be RTL content, rendered with correct `dir` in the diff view.

## 16. Security
Zero reimplementation of `isSelfEdited`/segregation-of-duties logic is this sub-feature's guarantee — mandatory test confirms this module imports E.29's components directly rather than containing a parallel implementation, and confirms a scholar rejection here correctly reverts only the specific locale's version (cross-verified against B-05).

## 17. Testing
Unit: `item_type` query-scoping logic. UI: **mandatory** — structural test/import-check confirming `DecisionActionBar`/`SegregationOfDutiesBlock` are imported from E.29's module path, not duplicated. Integration: full editorial-only review flow for general UI copy; full editorial-then-scholar review flow for Islamic-content-adjacent strings; rejection reverts only the specific locale's version.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Implement `TranslationReviewRepositoryImpl` as a Scoped Wrapper**
Objective: Calls E.29's existing endpoints with `item_type=locale_string_version` filtering. Files: `api/translation-review-repository.ts`. Dependencies: B-05. Tests: mocked-fetch tests confirming correct scoping parameter. Definition of Done: tests pass.

**Task 02 — Import and Wire E.29's `DecisionActionBar`/`SegregationOfDutiesBlock`**
Objective: Direct reuse, zero reimplementation. Dependencies: E.29 N-04, Task 01. Tests: **mandatory** — import-path structural test confirming no duplicated component exists. Definition of Done: test passes.

**Task 03 — Implement `TranslationDiffView`**
Objective: Plain-string/ICU value before/after comparison, reusing E.29's diff pattern. Dependencies: Task 01. Tests: diff-rendering test for string values. Definition of Done: test passes.

**Task 04 — Implement the Editorial and Scholar Queue Pages**
Objective: Compose reused components + `TranslationDiffView` with `item_type`-scoped data. Dependencies: Tasks 01–03. Tests: full-page smoke tests. Definition of Done: tests pass.

**Task 05 — Verify Locale-Scoped Rejection Behavior**
Objective: **Mandatory** integration test confirming a scholar rejection reverts only the specific locale's version. Dependencies: Task 04, B-05. Definition of Done: test passes.

**Task 06 — Add Full Test Suite**
Objective: Complete coverage per §17, both mandatory tests included. Definition of Done: all green in CI.

**Task 07 — Final Code Review**
Objective: Confirm zero duplicated review-workflow UI logic exists in this module — everything safety-critical is imported from E.29. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] `DecisionActionBar`/`SegregationOfDutiesBlock` imported directly from E.29, not duplicated — mandatory structural test passing
- [ ] Editorial-only path correctly available for general UI copy
- [ ] Scholar review correctly required for Islamic-content-adjacent strings
- [ ] Rejection reverts only the specific locale's version — mandatory test passing
- [ ] `localization_manager`/`scholar_reviewer` scopes correctly gate their respective queues

## 20. Definition of Done
Translation review workspaces are fully functional and safety-consistent with E.29's proven review discipline, built entirely through reuse rather than a second, potentially divergent implementation.
