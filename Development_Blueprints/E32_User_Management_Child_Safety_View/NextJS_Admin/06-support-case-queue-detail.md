# N-06 — Support Case Queue & Detail

## 1. Feature Context
The general case-tracking workspace tying together support interactions, including deletion-related cases whose detail view links out to (never re-implements) C.21's existing deletion/cancellation views.

## 2. Parent Feature
E.32 — User Management & Child Safety View

## 3. Sub-feature
2.6 Support Case Queue & Detail (ID: **N-06**)

## 4. Objective
Build the Support Case Queue and Detail screens against B-08, with a linked-action panel that navigates to the referenced unmask request or deletion-cancellation record rather than duplicating its display.

## 5. Business Requirements
- Filterable queue by `case_type`/`status`.
- Case detail: notes, related parent/child, linked-action reference (if present), resolve action with required resolution note.
- Deletion-related case types link out to C.21's existing detail views for the actual deletion/cancellation mechanics.

## 6. Existing Architecture
`src/features/support-cases/` module.

## 7. Existing Code to Reuse
- `src/shared/components/require-permission.tsx::RequirePermission`
- `src/shared/components/data-table.tsx::DataTable`
- `src/shared/hooks/use-pagination-state.ts::usePaginationState`
- C.21's deletion/cancellation detail view (linked to, not embedded/duplicated)

## 8. Files to Create
- `src/app/(dashboard)/support-cases/page.tsx`
- `src/app/(dashboard)/support-cases/[id]/page.tsx`
- `src/features/support-cases/api/support-case-repository.ts`
- `src/features/support-cases/hooks/use-case-queue.ts`, `use-case-detail.ts`, `use-resolve-case.ts`
- `src/features/support-cases/components/case-type-filter.tsx`
- `src/features/support-cases/components/linked-action-panel.tsx` — link-out, not embed
- `src/features/support-cases/components/resolve-case-form.tsx`
- `src/features/support-cases/types/support-case.ts` — Zod schema

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `SUPPORT_CASES.*` endpoints
- `src/shared/components/dashboard-shell.tsx` — nav item under "Support" group

## 10. NextJS Requirements
- `LinkedActionPanel`: for `linked_action_type='unmask_request'`, links to N-03's detail page by ID; for `linked_action_type='account_deletion'`, links to C.21's existing detail view by ID — this component never re-renders the linked record's own detail content, only a summary + navigation link, to avoid two divergent renderings of the same underlying data.
- `CaseTypeFilter`: enum-driven from the same `case_type` values B-08 validates against.

## 11. Required API
**Admin API** — B-08: `POST /v1/admin/support-cases`, `GET /v1/admin/support-cases`, `GET /v1/admin/support-cases/{id}`, `PATCH /v1/admin/support-cases/{id}/resolve`.

## 12. Authentication / Authorization
`useAdminSession()` base auth; `RequirePermission permission="support"`.

## 13. Loading / Empty / Error States
Queue loading skeleton, "No cases" empty state; resolve-form validation error for missing resolution note; linked-action-not-found state (e.g., referenced record was itself since deleted/archived) shown distinctly from a general load error.

## 14. Responsive UI / Accessibility
Case list filterable/sortable with keyboard-accessible controls; linked-action link clearly labeled with its destination context (e.g., "View linked unmask request").

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()`.

## 16. Security
`LinkedActionPanel`'s link-out-not-embed design avoids creating a second rendering surface for sensitive linked data (e.g., an unmask request's justification) that could drift out of sync with, or bypass, that record's own access-control-gated detail page.

## 17. Testing
Unit: `case_type` filter enum consistency with backend. UI: linked-action panel renders a navigation link, not embedded sensitive content, for both linked-action types. Integration: full create-case (via B-08, e.g., triggered from N-03) → queue-shows-case → resolve-with-note flow; deletion-related case links correctly to C.21's existing view.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schema & Add API Endpoints**
Objective: `support-case.ts` schema. Files: `types/support-case.ts`, `api-endpoints.ts`. Tests: schema validation. Definition of Done: schema used by Task 03.

**Task 02 — Implement `SupportCaseRepositoryImpl`**
Objective: Repository for B-08's four endpoints. Tests: mocked-fetch tests. Dependencies: Task 01. Definition of Done: tests pass.

**Task 03 — Implement `CaseTypeFilter` and Queue Page**
Objective: Filterable list. Dependencies: Task 02. Tests: filter-tests. Definition of Done: tests pass.

**Task 04 — Implement `LinkedActionPanel` (Link-Out, Not Embed)**
Objective: Navigation links to N-03/C.21 detail pages, no embedded rendering of the linked record's sensitive content. Dependencies: Task 02. Tests: **mandatory** — confirms no sensitive linked-record field is rendered directly in this panel, only a summary + link. Definition of Done: test passes.

**Task 05 — Implement `ResolveCaseForm`**
Objective: Required resolution-note form. Dependencies: Task 02. Tests: validation test. Definition of Done: test passes.

**Task 06 — Implement the Queue and Detail Pages**
Objective: Compose all components with loading/empty/error states. Dependencies: Tasks 03–05. Tests: full-page smoke tests. Definition of Done: tests pass.

**Task 07 — Add Full Test Suite**
Objective: Complete coverage per §17. Definition of Done: all green in CI.

**Task 08 — Final Code Review**
Objective: Confirm `LinkedActionPanel` never duplicates sensitive linked-record content. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] Queue correctly filters by `case_type`/`status`
- [ ] `LinkedActionPanel` links out to N-03/C.21 rather than embedding sensitive content — mandatory test passing
- [ ] Resolve requires a resolution note
- [ ] `support`+ scope enforced

## 20. Definition of Done
Support cases — including deletion-related ones correctly cross-referencing C.21 without duplicating its detail rendering — are queued, tracked, and resolvable through a consistent UI workspace.
