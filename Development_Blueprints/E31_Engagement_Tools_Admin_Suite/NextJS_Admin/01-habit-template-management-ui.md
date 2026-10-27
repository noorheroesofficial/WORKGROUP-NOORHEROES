# N-01 — Habit Template Management UI

## 1. Feature Context
Part of **Feature E.31 — Engagement Tools Admin Suite**. Delivers the Admin Portal screens for authoring habit templates, consuming **B-01 Habit Template Management API**. Source: PRD §1.18 Screens 1–3, §2, §6.

## 2. Parent Feature
Feature E.31 — Engagement Tools Admin Suite

## 3. Sub-feature
3.1 Habit Template Management UI (Admin ID: **N-01**)

## 4. Objective
Give content admins a data-table + editor experience for habit templates, clearly communicating (via helper text) that XP-value changes are versioned/forward-only, never retroactive — so admins never mistakenly believe they're editing history.

## 5. Business Requirements
- Screen Inventory (PRD §1.18): #1 Habit Template List, #2 Habit Template Editor (cadence/XP/icon/age), #3 Seasonal Habit Set Builder.
- FR-1 CRUD screens: list, editor, seasonal set builder (PRD §1.7).
- Non-Functional (PRD §1.8): No-Retroactivity Enforcement — the UI must clearly communicate this to admins, not just the backend enforce it.

## 6. Existing Architecture
React + TypeScript, per `noorheroes-admin/NEXT-JS-INSTRUCTIONS.md`, reusing E.28's Admin Portal shell/design-token package and role-scoped "Engagement" navigation group (PRD §2.3).

## 7. Existing Code to Reuse
- E.28's Admin Portal shell, sidebar navigation, design tokens, auth/session context.
- E.29's shared `ContentUploadRepository` for icon upload (PRD §6.4) — no parallel upload client implemented here.
- E.29's Content Library/editor "list → editor" data-table pattern (PRD §2.4) reused for consistency.

## 8. Files to Create
- `app/(admin)/engagement/habits/page.tsx` (Habit Template List)
- `app/(admin)/engagement/habits/[id]/page.tsx` (Habit Template Editor)
- `app/(admin)/engagement/habits/seasonal-set/page.tsx` (Seasonal Habit Set Builder)
- `components/engagement/habits/HabitTemplateTable.tsx`
- `components/engagement/habits/HabitTemplateEditorForm.tsx`
- `repositories/admin/HabitAdminRepository.ts`
- `types/admin/habitTemplate.ts`
- `__tests__/engagement/habits/HabitTemplateEditorForm.test.tsx`

## 9. Files to Modify
- `components/shell/EngagementNavGroup.tsx` (add Habits entry)
- `lib/analytics/EngagementAdminAnalytics.ts` (add habit template events)

## 10. Backend Requirements
Consumes **B-01** endpoints exclusively: `POST/GET/PATCH /v1/admin/habit-templates`, `POST /v1/admin/habit-templates/{id}/retire`. No new backend work originates from this sub-feature.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- **Page:** List page (table), Editor page (form), Seasonal Set Builder page.
- **Route:** `/engagement/habits`, `/engagement/habits/[id]`, `/engagement/habits/seasonal-set`.
- **Component:** `HabitTemplateTable` (data table with pagination/filter/sort), `HabitTemplateEditorForm` (cadence, XP value, icon upload, age band), `RetireConfirmDialog`.
- **API Client:** `HabitAdminRepository` mapping to B-01's four endpoints.
- **Type Definition:** `HabitTemplate`, `HabitTemplateXPVersion`, `HabitTemplateCreateInput`, `HabitTemplateUpdateInput`.
- **Form:** React Hook Form + Zod schema validation mirroring backend validation (cadence enum, age_band, xp_value positive integer).
- **Validation:** client-side pre-check mirrors server; server response is authoritative on submit.
- **Authentication:** inherits E.28 admin session context.
- **Authorization:** `content_editor`+ gate on create/update/retire actions (buttons hidden/disabled otherwise); read-only view for lower-privilege roles.
- **Permissions:** role check via shared `usePermission()` hook from E.28.
- **Loading State:** skeleton loading pattern (E.28/E.29/E.30 standard).
- **Empty State:** "Nothing here yet, create your first habit template."
- **Error State:** inline form errors + toast for API failures.
- **Pagination:** server-driven pagination via `HabitAdminRepository.list(page, pageSize)`.
- **Filtering:** by category, age_band, active status.
- **Sorting:** by usage count, created_at.
- **Search:** by template name.
- **Responsive UI:** table collapses to card view on narrow viewports, consistent with Admin Portal's dense-tool responsive pattern.
- **Accessibility:** keyboard-navigable table/form, ARIA labels on icon upload and rule-builder-adjacent controls.
- **Localization:** template name/description fields editable per-locale (English/Hindi/Arabic/Urdu) via the platform's localization-key editor component (reused, not reinvented).
- **RTL:** full RTL mirroring for Arabic/Urdu admin locale, if the Admin Portal itself supports locale switching; otherwise RTL applies only to localization-key content preview.
- **Analytics:** `habit_template_created`, `habit_template_updated`, `habit_template_retired` fired via `EngagementAdminAnalytics`.
- **Performance:** table virtualization if template count grows large; debounce search input.
- **Caching:** React Query (or existing Admin Portal data-fetching library) cache with invalidation on mutation.
- **Testing:** unit (form validation), UI (helper text presence), integration (full update-without-retroactive-effect flow, per PRD §6.10).

## 13. API Contract
Reuses B-01's contract verbatim (see `Backend/01-habit-template-management-api.md` §13). No new endpoints defined here.

## 14. Database Requirements
N/A (frontend-only sub-feature).

## 15. Validation
Client-side Zod schema mirrors backend: cadence enum, positive `xp_value`, valid `age_band`. Server remains authoritative.

## 16. Authentication
Inherits E.28 Admin Portal session/JWT handling — no separate auth implementation.

## 17. Authorization
`content_editor`+ required for create/update/retire actions; enforced both by hiding/disabling UI affordances and by the backend's own `403` as the authoritative guard (UI hiding is UX convenience, not the security boundary).

## 18. Error Handling
| Scenario | UI Behavior |
|---|---|
| API returns `422 VALIDATION_ERROR` | Inline field-level error messages |
| API returns `422 ICON_UPLOAD_REJECTED` | Icon upload area shows rejection reason from E.29 pipeline |
| API returns `404 NOT_FOUND` | Redirect to list with "Template not found" toast |
| API returns `403 FORBIDDEN` | Action buttons disabled with tooltip explaining required role |
| Network/server failure | Toast + retry affordance |

## 19. Offline First
N/A — internal operator tool, connectivity assumed (PRD §1.14).

## 20. Local Data
N/A.

## 21. Localization
English, Hindi, Arabic, Urdu supported for template display-name/description content via the platform's shared localization-key editor; admin UI chrome itself follows the Admin Portal's own supported admin-locale set.

## 22. RTL
Full RTL layout support for Arabic/Urdu content editing fields, consistent with PRD §2.5's RTL wireframe prompts for this module family.

## 23. Analytics
`EngagementAdminAnalytics` fires `habit_template_created` (trigger: successful create submit), `habit_template_updated` (trigger: successful update submit, params: `changed_fields`), `habit_template_retired` (trigger: retire confirm).

## 24. Performance
React Query cache with a short stale-time for the list view; debounce search/filter inputs (300ms); avoid re-rendering the entire table on single-row mutation (optimistic update + row-level patch).

## 25. Security
No sensitive data rendered beyond what E.28's RBAC already permits this admin role to see; no client-side bypass of retroactivity guarantees (UI never offers an "edit past check-ins" affordance, since none exists).

## 26. Library Requirements
React, TypeScript, React Hook Form, Zod, React Query (or Admin Portal's established data-fetching library), existing Admin Portal design-token package, Jest/React Testing Library.

## 27. Testing
- **Unit:** `HabitTemplateEditorForm` validation logic (cadence/age_band/xp_value).
- **UI tests:** confirm the XP Rule Editor equivalent helper text ("Changes apply only going forward; past check-ins are unaffected") is present on the habit template editor's XP field, per PRD §6.10.
- **Integration:** full habit-template-update-without-retroactive-effect flow (create → update XP → verify UI reflects new value going forward with no implication of history changing).

## 28. Documentation
Component-level JSDoc/Storybook entries (if the Admin Portal uses Storybook) documenting the versioned-XP UX pattern for reuse by N-03 (XP Rule Editor) and N-05 (Badge Criteria Builder), which share the same helper-text convention.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Types & API Client**
- Task ID: N-01-T01
- Objective: Define TypeScript types and `HabitAdminRepository` mapping to B-01's endpoints.
- Files to Create: `types/admin/habitTemplate.ts`, `repositories/admin/HabitAdminRepository.ts`.
- Dependencies: B-01 deployed to a reachable environment (or contract-mocked).
- Definition of Done: repository methods typed and unit-tested against a mocked API.

**Task 02 — Habit Template List Page**
- Task ID: N-01-T02
- Files to Create: `app/(admin)/engagement/habits/page.tsx`, `components/engagement/habits/HabitTemplateTable.tsx`.
- Implementation Details: pagination, filter, sort, search, loading/empty/error states.
- Dependencies: Task 01.
- Definition of Done: renders against mocked/live API with all states covered.

**Task 03 — Habit Template Editor**
- Task ID: N-01-T03
- Files to Create: `app/(admin)/engagement/habits/[id]/page.tsx`, `components/engagement/habits/HabitTemplateEditorForm.tsx`.
- Implementation Details: XP-value field displays non-retroactivity helper text; icon upload via shared `ContentUploadRepository`; retire action behind confirm dialog.
- Dependencies: Task 01.
- Definition of Done: UI test confirms helper text presence; full CRUD flow functional.

**Task 04 — Seasonal Habit Set Builder**
- Task ID: N-01-T04
- Files to Create: `app/(admin)/engagement/habits/seasonal-set/page.tsx`.
- Dependencies: Tasks 01–03.
- Definition of Done: builder screen functional, links back to list.

**Task 05 — Permission Gating & Accessibility Pass**
- Task ID: N-01-T05
- Implementation Details: role-based hide/disable of mutating actions; ARIA labels; keyboard navigation.
- Dependencies: Tasks 02–04.
- Definition of Done: accessibility audit checklist passes; forbidden-role UI states tested.

**Task 06 — Tests & Documentation**
- Task ID: N-01-T06
- Dependencies: Tasks 01–05.
- Definition of Done: §31 checklist verified.

## 30. Definition of Done
List/editor/seasonal-set screens fully functional against B-01; non-retroactivity helper text verified present; permission gating enforced; loading/empty/error states implemented; RTL/localization supported; tests green.

## 31. Final Verification Checklist
- [ ] Habit Template List renders with pagination/filter/sort/search
- [ ] Habit Template Editor form validates cadence/age_band/xp_value client-side
- [ ] XP-value field displays "changes apply only going forward" helper text
- [ ] Icon upload uses shared `ContentUploadRepository`, surfaces E.29 rejection reasons
- [ ] Retire action behind confirm dialog, no hard-delete affordance anywhere
- [ ] Seasonal Habit Set Builder screen functional
- [ ] `content_editor`+ gating enforced on all mutating actions
- [ ] Loading/empty/error states implemented
- [ ] Responsive, accessible, RTL-supported
- [ ] Analytics events fire correctly
- [ ] No school/madrasa/institutional-tier logic introduced
