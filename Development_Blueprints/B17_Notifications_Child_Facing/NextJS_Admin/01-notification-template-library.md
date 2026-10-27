# N-01 — Notification Template Library

## 1. Feature Context
Part of Feature B.17 — Notifications (Child-Facing). Admin surface for CRUD over push/in-app templates, enforcing the hard billing/analytics-term blocklist for every child-facing template, with no override option for any admin role (FR-6).

## 2. Parent Feature
B.17 Notifications (Child-Facing) — NextJS Admin

## 3. Sub-feature
N-01 Notification Template Library

## 4. Objective
Build the Notification Template Library page: CRUD editor for templates tagged by target class (child-facing vs parent-facing) and type, with save-time blocklist validation surfacing the matched term and blocking the save for every role, mirroring A.7's mercy-toned-copy-review-queue pattern.

## 5. Business Requirements
- On save, for any template tagged child-facing, run it through the blocklist validator — block the save with the matched term highlighted, for every admin role, with no override option anywhere in this UI (PRD §9).
- Template Library CRUD permissions: full CRUD behind `content_editor` role; hard blocklist gate non-bypassable for any role (PRD §8).

## 6. Existing Architecture
- Extends the existing Admin Portal "Notification Management" module referenced in A.12's admin context (PRD §8 preamble).
- Mirrors the structure and blocklist-UI pattern of A.7's `Development_Blueprints/A7_Habit_Tracker/NextJS_Admin/03-mercy-toned-copy-localization-review-queue.md` — reuse its rejection-highlighting component rather than building a new one.
- Follows `NEXT-JS-INSTRUCTIONS.md` conventions for pages, API client layer, forms, and RBAC.

## 7. Existing Code to Reuse
- A.7's blocklist-rejection-highlighting UI component (adapted term list).
- Existing Admin Portal RBAC/role-context provider.
- Existing table/pagination/filter components used elsewhere in the Admin Portal.

## 8. Files to Create
- `app/(admin)/notifications/templates/page.tsx` — list view with filter by class/type.
- `app/(admin)/notifications/templates/[id]/page.tsx` — editor view (create/edit).
- `components/notifications/TemplateEditorForm.tsx`.
- `components/notifications/BlocklistViolationBanner.tsx` (or reuse A.7's equivalent, renamed/generalized if appropriate).
- `lib/api/notifications/templates.ts` — API client (`createTemplate`, `updateTemplate`, `getTemplate`, `listTemplates`).
- `lib/types/notifications.ts` — `NotificationTemplate`, `TemplateClass`, `TemplateType` types.
- `tests/notifications/TemplateEditorForm.test.tsx`.

## 9. Files to Modify
- Admin Portal navigation/sidebar — add "Notification Templates" entry under Notification Management.

## 10. Backend Requirements
Consumes B-04's `POST/GET/PATCH /v1/admin/notifications/templates` exactly as documented, including the `422` blocklist-violation response shape.

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- Page: template list with filter by class (child-facing/parent-facing) and type.
- Component: template editor form with body textarea, placeholder helper text, live preview.
- API Client: typed wrapper over B-04's endpoints.
- Type Definition: `NotificationTemplate` matching B-04's schema exactly.
- Form/Validation: client-side placeholder-syntax hint (non-authoritative — server is the source of truth for validation).
- Authentication/Authorization: `content_editor` role required for create/update; read available more broadly per existing RBAC.
- Loading/Empty/Error States: loading skeleton on list, empty state when no templates match filter, error state on API failure.
- Pagination/Filtering/Sorting: paginate template list; filter by class/type; sort by updated date.
- Responsive UI/Accessibility: keyboard-navigable form, ARIA labels on all inputs, responsive down to tablet width.
- Localization/RTL: editor UI itself supports the admin's own locale/RTL preference (distinct from the template content's target locale, which is a data field, not a UI-locale concern).
- Testing: unit + integration tests for the blocklist-rejection flow.

## 13. API Contract
Consumes B-04 §13 exactly: `POST/GET/PATCH /v1/admin/notifications/templates`, including the `422 { "error": "blocklist_violation", "matched_term": "..." }` response.

## 14. Database Requirements
N/A (frontend only; data owned by B-04's `notification_templates` table).

## 15. Validation
Client-side validation is advisory only (required fields, placeholder-syntax hints); the blocklist check is authoritative server-side and must never be bypassed or duplicated with a weaker client-only check that could give false confidence.

## 16. Authentication
Admin session via existing Admin Portal auth context.

## 17. Authorization
`content_editor` role gates create/update actions; UI hides/disables mutating controls for other roles rather than merely relying on the API's `403`.

## 18. Error Handling
| Scenario | System Behavior |
|---|---|
| Blocklist violation (`422`) | `BlocklistViolationBanner` shows the matched term, save blocked, no override control rendered for any role |
| Duplicate active template (`409`) | Inline error indicating an active template already exists for that type/class/locale |
| Network/API failure | Toast/error state with retry action |
| Unauthorized/forbidden | Mutating controls disabled/hidden; read-only view shown if role permits read |

## 19. Offline First
N/A (admin web, always-online assumption standard for this portal).

## 20. Local Data
N/A.

## 21. Localization
The template's `locale` field (EN/HI/AR/UR) is selected explicitly in the editor form as data, not inferred from the admin's own UI language.

## 22. RTL
Editor UI mirrors correctly if the admin's own locale is AR/UR; the template body textarea itself should support RTL text entry when `locale=ar|ur` is selected, regardless of the admin's own UI direction.

## 23. Analytics
Not applicable directly (no dedicated admin-analytics events specified for this sub-feature in the PRD); standard Admin Portal audit logging (via B-04's server-side persistence) is the system of record for template changes.

## 24. Performance
Template list paginated server-side; editor form avoids unnecessary re-renders on keystroke (debounced live preview).

## 25. Security
No client-side bypass of the blocklist is possible or attempted; the UI's rejection-highlighting is a UX affordance over the server's authoritative `422` response, never a substitute for it.

## 26. Library Requirements
Next.js (App Router), TypeScript, React, existing Admin Portal component library, existing form/validation library used elsewhere in the portal.

## 27. Testing
- Unit: `TemplateEditorForm` renders blocklist violation correctly from a mocked `422` response.
- Integration: full create → blocklist-violation → correct-term-highlighted → fix → successful-save flow.
- Accessibility: keyboard navigation and ARIA-label audit for the editor form.
- RBAC: non-`content_editor` role sees disabled/hidden mutating controls.

## 28. Documentation
Update Admin Portal user documentation (if one exists) describing the non-bypassable blocklist policy for child-facing templates.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement Types & API Client**
- Files to Create: `lib/types/notifications.ts`, `lib/api/notifications/templates.ts`.
- Implementation Details: types matching B-04's schema exactly, including the `422` error shape.

**Task 02 — Implement Template List Page**
- Files to Create: `app/(admin)/notifications/templates/page.tsx`.
- Implementation Details: paginated, filterable list.
- Loading/Empty/Error States: per §18.
- Tests: list rendering + filter test.

**Task 03 — Implement Template Editor Form**
- Files to Create: `TemplateEditorForm.tsx`, `[id]/page.tsx`.
- Existing Files to Reuse: A.7's blocklist-rejection UI pattern.
- Tests: form validation + submission test.

**Task 04 — Implement Blocklist Violation Handling**
- Objective: Surface the matched term, block save, no override for any role.
- Why Required: PRD §9 item 1, non-negotiable content-safety gate.
- Files to Create: `BlocklistViolationBanner.tsx` (or adapted reuse).
- Tests: mandatory test asserting no override control exists in the rendered DOM for any role.

**Task 05 — Implement RBAC-Gated Controls**
- Files to Modify: `TemplateEditorForm.tsx`, list page.
- Authorization: `content_editor` gate.
- Tests: RBAC rendering test per role.

**Task 06 — Add Accessibility & Responsive Layout**
- Files to Modify: all new components.
- Tests: accessibility audit test.

**Task 07 — Write Full Test Suite & Documentation**
- Tests: per §27.
- Documentation: per §28.

## 30. Definition of Done
- Full template CRUD implemented with correct RBAC gating.
- Blocklist violations are clearly surfaced with the matched term, with zero override path for any role.
- Accessible, responsive, and correctly localized/RTL-aware editor UI.

## 31. Final Verification Checklist
- [ ] Template list correctly paginates and filters by class/type
- [ ] Editor form creates/updates templates via B-04's API contract exactly
- [ ] Blocklist violation (`422`) correctly surfaces the matched term with no override control, for every role
- [ ] Duplicate-active-template conflict (`409`) shown with a clear inline error
- [ ] Mutating controls correctly hidden/disabled for non-`content_editor` roles
- [ ] Accessibility (keyboard nav, ARIA labels) verified
- [ ] Full test suite passes
