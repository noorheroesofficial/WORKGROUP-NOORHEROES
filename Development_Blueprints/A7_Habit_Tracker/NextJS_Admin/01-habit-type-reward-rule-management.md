# N-01 — Habit Type & Reward Rule Management

## 1. Feature Context
NoorHeroes Admin Portal (Next.js). CRUD interface for the global habit-type catalog and reward-rule linkage backing B-09.

## 2. Parent Feature
A.7 Habit Tracker — NextJS Admin

## 3. Sub-feature
N-01 Habit Type & Reward Rule Management

## 4. Objective
Build a CRUD table page for global habit type definitions (type enum, default age-band visibility, linked reward-rule reference), with Delete relabeled "Deactivate" (sets `active=false` only).

## 5. Business Requirements
- Full CRUD, delete = deactivate only (PRD §8).
- Restricted to `content_editor`/`product_admin` permission.
- Reward-rule reference must resolve to an existing entry in the shared rewards table.

## 6. Existing Architecture
Follows the existing Admin Portal shell: `src/app/(dashboard)/habits/types/page.tsx` route, `src/features/habit-types/{api,hooks,components}` feature module, reusing `DataTable`, `usePaginationState`, `RequirePermission` exactly as the existing `useUsers`/Users Directory pattern demonstrates (per `NEXT-JS-INSTRUCTIONS.md` §7/§Patterns).

## 7. Existing Code to Reuse
- `DataTable` (`src/shared/components/data-table`)
- `usePaginationState` (`src/shared/hooks/use-pagination-state`)
- `RequirePermission` (RBAC guard component)
- `hasPermission(admin, permission)` utility
- `useAdminSession` for current admin's role/permissions

## 8. Files to Create
- `src/app/(dashboard)/habits/types/page.tsx`
- `src/features/habit-types/api/habit-types-repository.ts`
- `src/features/habit-types/hooks/use-habit-types.ts` (paginated list, mirrors `useUsers`)
- `src/features/habit-types/hooks/use-create-habit-type.ts`
- `src/features/habit-types/hooks/use-update-habit-type.ts`
- `src/features/habit-types/hooks/use-deactivate-habit-type.ts`
- `src/features/habit-types/components/HabitTypeTable.tsx`
- `src/features/habit-types/components/HabitTypeFormDialog.tsx`
- `src/features/habit-types/types.ts`

## 9. Files to Modify
- Admin Portal sidebar/navigation config — add "Habit Types" entry under a Habit Tracker section

## 10. Backend Requirements
Consumes B-09 (`/v1/admin/habits/types`).

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- CRUD table using `DataTable` with columns: type, label, default age-band visibility summary, reward-rule reference, active status.
- Create/Edit form dialog with type-code uniqueness client-side pre-check (server remains authoritative).
- "Deactivate" action (not "Delete") with confirmation dialog.
- `RequirePermission permission="habits:types:write"` guarding create/edit/deactivate actions; read-only view for lower-permission roles.
- Pagination, filtering (by active status), sorting (by type/label).
- Loading, empty, and error states per existing Admin Portal conventions.

## 13. API Contract
`GET/POST/PATCH /v1/admin/habits/types` (B-09) — Admin API, Bearer admin session, `content_editor`/`product_admin` scope.

## 14. Database Requirements
N/A (frontend consumes backend API only).

## 15. Validation
Form validation: required `type`, unique-type client pre-check, valid reward-rule reference selection (dropdown sourced from existing rewards-rule list endpoint if available, otherwise a text reference field pending backend support).

## 16. Authentication
`useAdminSession` — admin Bearer session required for the route.

## 17. Authorization
`RequirePermission` guarding write actions; `hasPermission` check for conditional UI (e.g., hiding the Deactivate button entirely for read-only roles) — never rely on client-side hiding alone, since B-09 enforces this server-side too.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Duplicate type on create | Inline form error surfaced from the 409 response |
| Network/API failure | Error state with retry, consistent with existing Admin Portal error-boundary pattern |
| Unauthorized | `RequirePermission` hides the action; direct API 403 surfaced as a toast if somehow reached |

## 19. Offline First
Not applicable (Admin Portal is online-only by design).

## 20. Local Data
Not applicable.

## 21. Localization
**Confirmed:** the Admin Portal has first-class multi-locale support, not English-only — `NEXT-JS-INSTRUCTIONS.md` documents `useLocalization()` (active locale/RTL status), `useFormatters()`, `useTranslation()`, and `updateLanguagePreference(language: 'hi'|'ar'|'en')`. All UI strings on this page must go through `useTranslation()` rather than hardcoded English text.

## 22. RTL
**Confirmed:** use `useLocalization()`'s RTL status to drive layout direction, consistent with every other Admin Portal page — this page is in scope for RTL, not exempt.

## 23. Analytics
Not applicable (internal admin tooling; audit log is the operational record of truth, per B-09).

## 24. Performance
Standard paginated table performance via `DataTable`/`usePaginationState`, consistent with the Users Directory reference pattern.

## 25. Security
`RequirePermission` client-side guard is defense-in-depth only — backend (B-09) is the authoritative enforcement point, per `NEXT-JS-INSTRUCTIONS.md`'s explicit "do NOT bypass `RequirePermission`... ensure backend endpoints enforce permissions" rule.

## 26. Library Requirements
Next.js App Router, React Query (per existing hook patterns), existing Admin Portal shared component library.

## 27. Testing
Component tests for `HabitTypeTable`/`HabitTypeFormDialog`; hook tests for CRUD mutations; RBAC-guard rendering tests (permission present vs. absent).

## 28. Documentation
Update Admin Portal navigation documentation (if one exists) with the new Habit Types section.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Scaffold `habit-types` Feature Module**
- Objective: `src/features/habit-types/{api,hooks,components}` following the `useUsers` reference pattern.
- Existing Architecture to Follow: `src/features/users` module structure.
- Files to Create: `types.ts`, `api/habit-types-repository.ts`
- Definition of Done: module compiles with typed API client methods.

**Task 02 — Implement List/Create/Update/Deactivate Hooks**
- Files to Create: `hooks/use-habit-types.ts`, `use-create-habit-type.ts`, `use-update-habit-type.ts`, `use-deactivate-habit-type.ts`
- Existing Files to Reuse: `usePaginationState` pattern from `useUsers`.
- Tests: hook unit tests (mocked API repository).
- Definition of Done: hooks correctly wrap B-09's endpoints with React Query.

**Task 03 — Build `HabitTypeTable` Component**
- Files to Create: `components/HabitTypeTable.tsx`
- Existing Files to Reuse: `DataTable`.
- Implementation Details: columns per §12; pagination/filtering/sorting.
- Tests: component render test with mock data.
- Definition of Done: table renders correctly with all documented states.

**Task 04 — Build `HabitTypeFormDialog` Component**
- Files to Create: `components/HabitTypeFormDialog.tsx`
- Implementation Details: create/edit form with validation per §15.
- Tests: form validation tests.
- Definition of Done: form correctly creates/updates via the hooks from Task 02.

**Task 05 — Wire Page Route with RBAC Guard**
- Files to Create: `src/app/(dashboard)/habits/types/page.tsx`
- Files to Modify: sidebar/navigation config.
- Authentication/Authorization: `RequirePermission` per §17.
- Definition of Done: route live, reachable via navigation, correctly RBAC-guarded.

**Task 06 — Final Code Review**
- Do Not Change: existing `src/features/users` module (reference only, not modified).
- Expected Result: PR merge-ready.

## 30. Definition of Done
Habit Type & Reward Rule Management page live, RBAC-guarded, fully functional CRUD with deactivate-only delete, tested.

## 31. Final Verification Checklist
- [ ] CRUD table renders with pagination/filtering/sorting
- [ ] Create/Edit form validates type uniqueness and reward-rule reference
- [ ] Delete action is "Deactivate" only, not a hard delete
- [ ] `RequirePermission` guards all write actions
- [ ] Loading/empty/error states implemented
- [ ] Component and hook tests passing
