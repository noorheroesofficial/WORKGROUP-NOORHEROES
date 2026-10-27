# N-01 — Fact Editor & Version History Management

## 1. Feature Context
Part of Feature B.18 (Islamic Facts Module). The primary admin authoring surface — full CRUD for facts and their versions, consuming B-06's admin API.

## 2. Parent Feature
B.18 — Islamic Facts Module

## 3. Sub-feature
3.1 Fact Editor & Version History Management (ID: N-01)

## 4. Objective
Build a CRUD form and list view for facts: topic (dropdown from Topic Registry), per-locale/age-band text variants, explanation, structured source citations, optional jurisprudential-scope note, and a searchable linked-quiz-question picker into A.8's Question Bank — with version history/diffs, publish gated on fresh scholar approval.

## 5. Business Requirements
- §8 Admin Requirements: Fact Editor — full CRUD (delete=withdraw) behind `content_editor` role, scholar-approval-gated publish. Editing a published fact creates a new version.
- §9 Admin AI Code-Generation Prompt item 1: version history with diffs; publish gated on a fresh `scholar_approval` row.

## 6. Existing Architecture
Next.js App Router, per `NEXT-JS-INSTRUCTIONS.md` conventions. Extends the Admin Portal's Content Management module. Reuses existing CRUD-table/form patterns and the Admin Portal's existing role-context for RBAC.

## 7. Existing Code to Reuse
- Existing Admin Portal CRUD-table/form component library (data table, form builder, validation wiring).
- Existing audit-logging convention (mutations automatically logged via the shared API client interceptor, if one exists).
- A.3/A.5/A.6's existing version-history/diff-viewer component, if already built — reuse rather than build a new diff UI.

## 8. Files to Create
- `app/(admin)/islamic-facts/page.tsx` — fact list/search/filter.
- `app/(admin)/islamic-facts/[id]/page.tsx` — fact editor with version history.
- `app/(admin)/islamic-facts/new/page.tsx` — create form.
- `components/islamic-facts/FactTable.tsx`.
- `components/islamic-facts/FactForm.tsx` — locale/age-band text variants, source citation list, jurisprudential-scope-note field, linked-quiz-question picker.
- `components/islamic-facts/FactVersionHistory.tsx` — diff viewer.
- `lib/api/islamicFacts.ts` — API client for B-06's endpoints.
- `types/islamicFacts.ts`.
- `lib/validation/factSchema.ts`.

## 9. Files to Modify
- Admin navigation/sidebar config — add "Islamic Facts" entry.

## 10. Backend Requirements
Consumes B-06 (`POST/PUT/GET/DELETE /v1/admin/facts...`). No backend code produced here.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- **Page/Route:** list page (`/islamic-facts`), create page (`/islamic-facts/new`), edit page (`/islamic-facts/[id]`).
- **Component:** `FactTable` (paginated, filterable by topic/locale/age-band/status, searchable by fact text), `FactForm` (topic dropdown from Topic Registry, per-locale/age-band text/explanation fields in a tabbed/accordion layout per locale, repeatable structured source citation list, optional jurisprudential-scope-note rich-text field, searchable linked-quiz-question picker querying A.8's Question Bank admin search endpoint), `FactVersionHistory` (diff viewer highlighting text/explanation/source changes across versions).
- **API Client:** `lib/api/islamicFacts.ts` typed wrapper over B-06.
- **Type Definitions:** `types/islamicFacts.ts`.
- **Form/Validation:** editing a published fact creates a NEW version — the form clearly labels this action "Save as new version," never implying an in-place update; publish action hard-disabled (not merely warned) until a fresh `scholar_approval` row exists for the version being published, mirroring B-06's server-side rule as a defense-in-depth UX layer.
- **Authentication/Authorization/Permissions:** `content_editor` role required for all CRUD actions; UI hides actions the current admin's role doesn't permit, backed by B-06's server-side enforcement.
- **Loading State:** skeleton table rows while list loads; form skeleton while an existing fact's data loads.
- **Empty State:** "No facts yet — create your first fact" call-to-action when the filtered list is empty.
- **Error State:** inline field-level errors for validation failures; toast for network/API failures with form state preserved (no data loss on submit failure); standard optimistic-concurrency conflict message with reload-and-retry prompt if another admin edited the same fact concurrently.
- **Pagination:** standard Admin Portal paginated table, page-size selector.
- **Filtering/Sorting/Search:** filter by topic, locale, age-band, status; sort by created date/status; search by fact text substring.
- **Responsive UI:** table collapses to a card list on narrow viewports, per existing Admin Portal responsive convention.
- **Accessibility:** form fields labeled with `aria-label`/`aria-describedby`; diff-viewer changes announced via appropriate ARIA live regions.
- **Delete action** performs a withdraw (soft delete), not a hard delete, with a confirmation dialog.

## 13. API Contract
**Required API:** `POST /v1/admin/facts`, `PUT /v1/admin/facts/{id}/versions`, `GET /v1/admin/facts`, `DELETE /v1/admin/facts/{id}` (all B-06).
**Authentication:** Bearer, admin.
**Authorization:** `content_editor` role.
**Error Responses:** `403` (wrong role), `422` (validation), `404` (unknown fact).

## 14. Database Requirements
N/A directly — consumes B-06's API, which owns the `fact`/`fact_version`/`scholar_approval` tables (B-01).

## 15. Validation
Client-side form validation mirrors B-01/B-06's server-side rules: at least one primary source required, topic must be selected from the registry, text required per targeted locale/age-band combination before that variant can be saved.

## 16. Authentication
Standard Admin Portal auth (existing session/JWT pattern).

## 17. Authorization
`content_editor` role required for all CRUD actions on this page; UI hides actions the current admin's role doesn't permit (in addition to B-06's server-side enforcement).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| API validation error (e.g., missing source) | Inline field-level error messages |
| Publish attempted without valid approval | Publish button disabled with explanatory tooltip, not a post-submit error |
| Network/API failure | Toast error, form state preserved |
| Concurrent edit conflict | Optimistic-concurrency conflict message, reload-and-retry prompt |

## 19. Offline First
N/A — Admin Portal is an online-only web application; no offline-first requirement for this surface.

## 20. Local Data
N/A — no local persistence beyond standard browser form-state retention during a single session (not offline storage).

## 21. Localization
Admin UI chrome follows the Admin Portal's own supported locale(s) (typically English); source-content fields must correctly accept and render English, Hindi, Arabic, and Urdu text input regardless of the admin chrome's own locale.

## 22. RTL
Source citation and text fields for Arabic/Urdu locale variants render RTL correctly within the (LTR) admin chrome — mixed-direction form field handling (`dir="auto"` or per-field direction detection).

## 23. Analytics
N/A — internal admin tool, not instrumented with product analytics beyond standard admin action audit logging (handled by B-06 server-side).

## 24. Performance
Paginated list avoids loading the full fact catalog at once; version-history diff computed client-side only for the currently-viewed fact, not pre-computed for the entire list.

## 25. Security
Publish-gate UI enforcement is a convenience layer only — B-06's server-side check remains the actual security boundary; code review must confirm this UI cannot be used to claim a fact is "published" without the server independently verifying the approval row.

## 26. Library Requirements
Existing Admin Portal component library (data table, form builder), React Hook Form or platform-equivalent (confirm existing convention), no new libraries introduced without confirming an existing equivalent doesn't already cover the need.

## 27. Testing
- Unit: form validation logic (required fields, source citation minimum).
- Unit: publish-button disabled-state logic matches B-06's server-side rule.
- Integration: create → edit (new version) → view diff → publish flow against a mocked B-06 API.
- Accessibility: form fields and diff viewer pass automated a11y checks.

## 28. Documentation
Component-level documentation (Storybook or equivalent, if the platform uses one) for `FactForm`/`FactVersionHistory`; API client documented with JSDoc.

## 29. AI Coding Agent Implementation Steps

**Task 01 — API Client**
Objective: `lib/api/islamicFacts.ts` wrapping B-06's endpoints.
Dependencies: B-06 deployed or contract-mocked.
Definition of Done: Typed client functions for all CRUD + version operations.

**Task 02 — List Page**
Objective: `app/(admin)/islamic-facts/page.tsx`, `FactTable.tsx`.
Dependencies: Task 01.
Definition of Done: Paginated, filterable, searchable list renders correctly.

**Task 03 — Editor Form**
Objective: `FactForm.tsx`, create/edit pages.
Dependencies: Task 01.
Definition of Done: Full form functioning with client-side validation mirroring B-06.

**Task 04 — Version History/Diff Viewer**
Objective: `FactVersionHistory.tsx`.
Existing Files to Reuse: A.3/A.5/A.6's diff-viewer component if it exists.
Dependencies: Task 03.
Definition of Done: Diff correctly highlights changes between versions.

**Task 05 — Publish Gate UI**
Objective: Hard-disable publish action without valid approval.
Dependencies: Task 03.
Definition of Done: Matches B-06's server-side enforcement exactly (no UI/server mismatch).

**Task 06 — Tests**
Objective: Coverage per §27.
Dependencies: Tasks 01–05.
Definition of Done: All green including a11y checks.

## 30. Definition of Done
- Full CRUD functioning against B-06.
- Version history/diff accurate.
- Publish gate matches server-side enforcement exactly.
- Accessibility, responsive, and RTL text-field handling verified.

## 31. Final Verification Checklist
- [ ] CRUD operations correctly call B-06's endpoints
- [ ] Editing a published fact creates a new version, never an in-place update
- [ ] Publish disabled without valid approval, matching server-side rule
- [ ] Version history/diff viewer accurate
- [ ] RTL text input verified for Arabic/Urdu fields
- [ ] Accessibility checks pass
- [ ] Role-gating (`content_editor`) verified in UI and confirmed backed by B-06's server-side check
