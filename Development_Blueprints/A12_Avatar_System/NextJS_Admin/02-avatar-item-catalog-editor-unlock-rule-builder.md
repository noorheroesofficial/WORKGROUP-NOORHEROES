# N-02 — Avatar Item Catalog Editor & Unlock Rule Builder

## 1. Feature Context
NoorHeroes Admin Portal (Next.js). Part of Feature A.12 — Avatar System. CRUD interface for the `avatar_items` catalog with a structured Unlock Rule Builder, backed by B-03.

## 2. Parent Feature
A.12 Avatar System — NextJS Admin

## 3. Sub-feature
N-02 Avatar Item Catalog Editor & Unlock Rule Builder

## 4. Objective
Build a CRUD table + form page for `avatar_items` (name, slot, asset/icon upload) with a structured, non-free-form Unlock Rule Builder offering three mutually-exclusive options (badge/level/habit-milestone), and a "Delete" action relabeled "Retire Item" — backing FR-4, FR-10, and PRD §9 Admin AI Code-Generation Prompt items 1–2.

## 5. Business Requirements
- Unlock Rule Builder is a guided UI, never a raw JSON text field — three mutually-exclusive options: (a) tied to badge (searchable dropdown of existing badges), (b) tied to achievement level (dropdown of existing levels), (c) tied to habit milestone (dropdown of recognized types + threshold input) (PRD §9).
- Form submission calls B-03's validation endpoint; a non-existent badge/level/milestone reference surfaces inline, not as a generic error (FR-4).
- "Delete" button is relabeled "Retire Item" with explanatory copy: "Children who already own this item keep it. It just won't be unlockable by new children going forward." — never a hard delete (FR-10).
- Newly-created/updated items route into the modesty/appropriateness review queue (N-03) before becoming visible to children — this page shows `status` read-only; approval itself is N-03's concern.

## 6. Existing Architecture
Follows the existing Admin Portal shell: `src/app/(dashboard)/avatars/items/page.tsx` route, `src/features/avatar-items/{api,hooks,components}` feature module, reusing `DataTable`, `usePaginationState`, `RequirePermission` per the same pattern as N-01/A.7 N-01. The Unlock Rule Builder's "structured builder, not free-form JSON" principle mirrors A.7 N-01's reward-rule-reference-must-resolve-to-an-existing-entry validation philosophy, extended here into a full three-way discriminated form control.

## 7. Existing Code to Reuse
- `DataTable`, `usePaginationState`, `RequirePermission`, `hasPermission`, `useAdminSession` (per N-01)
- Existing searchable-dropdown component (used elsewhere in the Admin Portal for cross-entity reference fields, e.g., content-to-category linkage)
- Existing R2 pre-signed-upload component (per N-01)

## 8. Files to Create
- `src/app/(dashboard)/avatars/items/page.tsx`
- `src/features/avatar-items/api/avatar-items-repository.ts`
- `src/features/avatar-items/hooks/use-avatar-items.ts`
- `src/features/avatar-items/hooks/use-create-avatar-item.ts`
- `src/features/avatar-items/hooks/use-update-avatar-item.ts`
- `src/features/avatar-items/hooks/use-retire-avatar-item.ts`
- `src/features/avatar-items/components/AvatarItemTable.tsx`
- `src/features/avatar-items/components/AvatarItemFormDialog.tsx`
- `src/features/avatar-items/components/UnlockRuleBuilder.tsx` (badge/level/habit-milestone three-way selector)
- `src/features/avatar-items/types.ts`

## 9. Files to Modify
- Admin Portal sidebar/navigation config — add "Avatar Items" entry under the "Avatar System" section (established in N-01)

## 10. Backend Requirements
Consumes B-03 (`GET/POST/PATCH/DELETE /v1/admin/avatar-items`); the `UnlockRuleBuilder`'s badge/level/habit-milestone dropdowns source their options from existing badge/achievement-level/habit-milestone-type list endpoints (owned by the not-yet-blueprinted A.11 Rewards System and A.7's habit-type registry, per B-03's flagged cross-context dependency) — if those list endpoints do not yet exist at implementation time, this is flagged as a blocking dependency to resolve with the A.11/A.7 backend teams rather than guessed or stubbed silently.

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- CRUD table using `DataTable` with columns: name, slot, unlock rule summary (human-readable, e.g., "Badge: 7-Day Streak Champion"), status, retired indicator.
- Create/Edit form dialog: name, slot dropdown (outfit|glow|accessory), asset upload, icon upload, and `UnlockRuleBuilder`.
- `UnlockRuleBuilder`: a radio/tab selector for the three mutually-exclusive rule types, each revealing its own sub-form (searchable badge dropdown / achievement-level dropdown / habit-milestone-type dropdown + numeric threshold input); only one shape is ever submitted, matching B-03's `UnlockRuleSchema` discriminated union exactly.
- Form's "Save" action calls B-03's create/update endpoint; a `422 INVALID_UNLOCK_RULE_REFERENCE` response surfaces inline on the relevant dropdown field, not as a generic toast.
- "Delete" button relabeled "Retire Item"; confirmation dialog includes the exact explanatory copy from PRD §9.
- `RequirePermission permission="avatars:items:write"` guarding create/edit/retire actions.
- Pagination, filtering (by slot, status, retired), sorting (by name/created_at).
- Loading, empty, and error states per existing Admin Portal conventions.

## 13. API Contract
`GET/POST/PATCH/DELETE /v1/admin/avatar-items` (B-03) — Admin API, Bearer admin session, `content_editor` scope.

## 14. Database Requirements
N/A (frontend consumes backend API only).

## 15. Validation
Form validation: required `name`/`slot`/asset upload; `UnlockRuleBuilder` requires exactly one complete sub-form filled (client-side pre-check for UX), server (B-03) remains authoritative for reference-existence validation.

## 16. Authentication
`useAdminSession` — admin Bearer session required for the route.

## 17. Authorization
`RequirePermission` guarding write/retire actions; `hasPermission` check for conditional UI — backend (B-03) is the authoritative enforcement point.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| `422 INVALID_UNLOCK_RULE_REFERENCE` on save | Inline error on the specific `UnlockRuleBuilder` field (badge/level/milestone dropdown), not a generic toast |
| Retire attempted on an already-retired item | Idempotent success, button state reflects already-retired |
| Network/API failure | Error state with retry, consistent with existing Admin Portal error-boundary pattern |
| Unauthorized | `RequirePermission` hides the action; direct API `403` surfaced as a toast if somehow reached |
| Badge/level/milestone-type list endpoint unavailable | `UnlockRuleBuilder` shows a clear "unable to load options" state per rule-type tab, not a silent empty dropdown |

## 19. Offline First
Not applicable (Admin Portal is online-only by design).

## 20. Local Data
Not applicable.

## 21. Localization
Follow existing Admin Portal localization conventions (verify against existing pages, per N-01's precedent flag); item `name` itself is stored as a translation key server-side (B-03).

## 22. RTL
Follow existing Admin Portal RTL support level (verify against existing pages, per N-01's precedent flag).

## 23. Analytics
Not applicable (internal admin tooling; `AdminAuditLog` is the operational record of truth, per B-03).

## 24. Performance
Standard paginated table performance via `DataTable`/`usePaginationState`; `UnlockRuleBuilder`'s searchable badge dropdown should debounce search input to avoid excessive list-endpoint calls.

## 25. Security
`RequirePermission` client-side guard is defense-in-depth only — B-03 is the authoritative enforcement point for both RBAC and unlock-rule-reference validity, per `NEXT-JS-INSTRUCTIONS.md`'s explicit rule.

## 26. Library Requirements
Next.js App Router, React Query, existing Admin Portal shared component library, existing searchable-dropdown and R2 upload components.

## 27. Testing
Component tests for `AvatarItemTable`/`AvatarItemFormDialog`/`UnlockRuleBuilder` (all three rule-type sub-forms); hook tests for create/update/retire mutations; RBAC-guard rendering tests; inline-error-surfacing test for `422 INVALID_UNLOCK_RULE_REFERENCE`; regression test confirming "Retire Item" copy matches PRD §9 exactly and never performs a hard delete.

## 28. Documentation
Update Admin Portal navigation documentation with the "Avatar Items" entry.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Scaffold `avatar-items` Feature Module**
- Objective: `src/features/avatar-items/{api,hooks,components}` following the N-01/A.7 N-01 reference pattern.
- Files to Create: `types.ts`, `api/avatar-items-repository.ts`
- Definition of Done: module compiles with typed API client methods, including the `UnlockRuleSchema` discriminated-union type matching B-03's backend schema exactly.

**Task 02 — Implement List/Create/Update/Retire Hooks**
- Files to Create: `hooks/use-avatar-items.ts`, `use-create-avatar-item.ts`, `use-update-avatar-item.ts`, `use-retire-avatar-item.ts`
- Tests: hook unit tests (mocked API repository), including `422` error-surfacing behavior.
- Definition of Done: hooks correctly wrap B-03's endpoints with React Query.

**Task 03 — Build `UnlockRuleBuilder` Component**
- Files to Create: `components/UnlockRuleBuilder.tsx`
- Existing Files to Reuse: existing searchable-dropdown component.
- Implementation Details: three-way mutually-exclusive selector, sourcing badge/level/milestone-type options from their respective list endpoints; submits exactly one discriminated shape.
- Tests: component tests for all three sub-forms, including the "unable to load options" fallback state.
- Definition of Done: builder produces a payload matching B-03's `UnlockRuleSchema` exactly for all three types.

**Task 04 — Build `AvatarItemTable` and `AvatarItemFormDialog` Components**
- Files to Create: `components/AvatarItemTable.tsx`, `components/AvatarItemFormDialog.tsx`
- Existing Files to Reuse: `DataTable`, `UnlockRuleBuilder` (Task 03), R2 upload component.
- Implementation Details: columns per §12; "Retire Item" relabeled delete action with exact PRD §9 explanatory copy.
- Tests: component render tests; inline `422` error-surfacing test; retire-confirmation-copy regression test.
- Definition of Done: table and form render and function correctly across all documented states.

**Task 05 — Wire Page Route with RBAC Guard**
- Files to Create: `src/app/(dashboard)/avatars/items/page.tsx`
- Files to Modify: sidebar/navigation config.
- Definition of Done: route live, reachable via navigation, correctly RBAC-guarded.

**Task 06 — Final Code Review**
- Do Not Change: existing `src/features/avatar-bases` module (N-01, reference only); B-03's backend schema (this task's frontend must match it, not redefine it).
- Expected Result: PR merge-ready.

## 30. Definition of Done
Avatar Item Catalog Editor live, RBAC-guarded, with a fully structured (non-free-form) Unlock Rule Builder correctly matching B-03's validated schema, and a "Retire Item" action that never hard-deletes.

## 31. Final Verification Checklist
- [ ] CRUD table renders with pagination/filtering/sorting
- [ ] `UnlockRuleBuilder` offers exactly three mutually-exclusive rule types, no free-form JSON field anywhere
- [ ] `422 INVALID_UNLOCK_RULE_REFERENCE` surfaces inline on the correct field
- [ ] "Delete" is relabeled "Retire Item" with the exact PRD §9 explanatory copy, never a hard delete
- [ ] `RequirePermission` guards all write/retire actions
- [ ] Loading/empty/error states implemented, including badge/milestone-list-unavailable fallback
- [ ] Component and hook tests passing
