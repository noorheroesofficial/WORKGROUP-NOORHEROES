# N-01 — Avatar Base Library Management

## 1. Feature Context
NoorHeroes Admin Portal (Next.js). Part of Feature A.12 — Avatar System. CRUD interface for the global `avatars` base library that A.1's Add Child flow references, backed by B-04.

## 2. Parent Feature
A.12 Avatar System — NextJS Admin

## 3. Sub-feature
N-01 Avatar Base Library Management

## 4. Objective
Build a CRUD table page for avatar base entries (`name`, `base_asset_key` upload), with no delete action exposed (only create/update), consistent with B-04's non-destructive design.

## 5. Business Requirements
- Full create/read/update; no delete/retire action on this page — base entries referenced by `ChildProfile.avatar_id` must remain permanently resolvable (PRD §8, B-04 §5).
- Restricted to `content_editor` permission.
- New/edited base entries route into the modesty/appropriateness review queue (N-03) before becoming selectable — this page surfaces `status` (pending_review/published/rejected) read-only; the review action itself lives in N-03, not duplicated here.

## 6. Existing Architecture
Follows the existing Admin Portal shell: `src/app/(dashboard)/avatars/bases/page.tsx` route, `src/features/avatar-bases/{api,hooks,components}` feature module, reusing `DataTable`, `usePaginationState`, `RequirePermission` exactly as the existing `useUsers`/Users Directory pattern and the A.7 `habit-types` module (N-01) demonstrate (per `NEXT-JS-INSTRUCTIONS.md` §7/§Patterns).

## 7. Existing Code to Reuse
- `DataTable` (`src/shared/components/data-table`)
- `usePaginationState` (`src/shared/hooks/use-pagination-state`)
- `RequirePermission` (RBAC guard component)
- `hasPermission(admin, permission)` utility
- `useAdminSession` for current admin's role/permissions
- Asset-upload component pattern (existing R2 pre-signed-upload flow used elsewhere in the Admin Portal, e.g., media/content asset uploads)

## 8. Files to Create
- `src/app/(dashboard)/avatars/bases/page.tsx`
- `src/features/avatar-bases/api/avatar-bases-repository.ts`
- `src/features/avatar-bases/hooks/use-avatar-bases.ts` (paginated list, mirrors `useUsers`/`useHabitTypes`)
- `src/features/avatar-bases/hooks/use-create-avatar-base.ts`
- `src/features/avatar-bases/hooks/use-update-avatar-base.ts`
- `src/features/avatar-bases/components/AvatarBaseTable.tsx`
- `src/features/avatar-bases/components/AvatarBaseFormDialog.tsx`
- `src/features/avatar-bases/types.ts`

## 9. Files to Modify
- Admin Portal sidebar/navigation config — add "Avatar Bases" entry under a new "Avatar System" section

## 10. Backend Requirements
Consumes B-04 (`GET/POST/PATCH /v1/admin/avatars`).

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- CRUD table using `DataTable` with columns: name, base_asset_key preview thumbnail, status (pending_review/published/rejected badge), created_at.
- Create/Edit form dialog with `base_asset_key` upload via the existing R2 pre-signed-upload component.
- No delete action anywhere on this page (structural omission, mirroring B-04's no-delete-endpoint design).
- `RequirePermission permission="avatars:bases:write"` guarding create/edit actions; read-only view for lower-permission roles.
- Pagination, filtering (by status), sorting (by name/created_at).
- Loading, empty, and error states per existing Admin Portal conventions.

## 13. API Contract
`GET/POST/PATCH /v1/admin/avatars` (B-04) — Admin API, Bearer admin session, `content_editor` scope.

## 14. Database Requirements
N/A (frontend consumes backend API only).

## 15. Validation
Form validation: required `name`, required `base_asset_key` upload (valid file type/size per existing media-upload validation conventions), server remains authoritative for uniqueness (B-04 §15).

## 16. Authentication
`useAdminSession` — admin Bearer session required for the route.

## 17. Authorization
`RequirePermission` guarding write actions; `hasPermission` check for conditional UI — never rely on client-side hiding alone, since B-04 enforces this server-side too.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Duplicate name/key on create | Inline form error surfaced from the `409` response |
| Network/API failure | Error state with retry, consistent with existing Admin Portal error-boundary pattern |
| Unauthorized | `RequirePermission` hides the action; direct API `403` surfaced as a toast if somehow reached |
| Upload failure | Inline upload-retry affordance, form remains open with prior fields intact |

## 19. Offline First
Not applicable (Admin Portal is online-only by design).

## 20. Local Data
Not applicable.

## 21. Localization
Admin Portal UI localization per existing conventions — verify against existing Admin pages before assuming multi-locale support here (per A.7 N-01's precedent flag; the `name` field itself is stored as a translation key per B-04, but the Admin Portal's own chrome may be English-only).

## 22. RTL
Follow existing Admin Portal RTL support level — verify against an existing Admin page before assuming RTL is in scope for internal tooling (per A.7 N-01's precedent flag).

## 23. Analytics
Not applicable (internal admin tooling; audit log is the operational record of truth, per B-04/B-05).

## 24. Performance
Standard paginated table performance via `DataTable`/`usePaginationState`, consistent with the Users Directory reference pattern.

## 25. Security
`RequirePermission` client-side guard is defense-in-depth only — backend (B-04) is the authoritative enforcement point, per `NEXT-JS-INSTRUCTIONS.md`'s explicit rule to never bypass `RequirePermission` while still ensuring backend endpoints enforce permissions.

## 26. Library Requirements
Next.js App Router, React Query (per existing hook patterns), existing Admin Portal shared component library, existing R2 upload component.

## 27. Testing
Component tests for `AvatarBaseTable`/`AvatarBaseFormDialog`; hook tests for create/update mutations; RBAC-guard rendering tests (permission present vs. absent); regression test confirming no delete affordance renders anywhere on this page.

## 28. Documentation
Update Admin Portal navigation documentation with the new Avatar System section.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Scaffold `avatar-bases` Feature Module**
- Objective: `src/features/avatar-bases/{api,hooks,components}` following the `habit-types` reference pattern (A.7 N-01).
- Existing Architecture to Follow: `src/features/habit-types` module structure.
- Files to Create: `types.ts`, `api/avatar-bases-repository.ts`
- Definition of Done: module compiles with typed API client methods.

**Task 02 — Implement List/Create/Update Hooks**
- Files to Create: `hooks/use-avatar-bases.ts`, `use-create-avatar-base.ts`, `use-update-avatar-base.ts`
- Existing Files to Reuse: `usePaginationState` pattern.
- Tests: hook unit tests (mocked API repository).
- Definition of Done: hooks correctly wrap B-04's endpoints with React Query.

**Task 03 — Build `AvatarBaseTable` Component**
- Files to Create: `components/AvatarBaseTable.tsx`
- Existing Files to Reuse: `DataTable`.
- Implementation Details: columns per §12; pagination/filtering/sorting; no delete action column/button.
- Tests: component render test with mock data, including a regression assertion that no delete button exists.
- Definition of Done: table renders correctly with all documented states.

**Task 04 — Build `AvatarBaseFormDialog` Component**
- Files to Create: `components/AvatarBaseFormDialog.tsx`
- Implementation Details: create/edit form with asset upload and validation per §15.
- Tests: form validation tests, including upload-failure retry.
- Definition of Done: form correctly creates/updates via the hooks from Task 02.

**Task 05 — Wire Page Route with RBAC Guard**
- Files to Create: `src/app/(dashboard)/avatars/bases/page.tsx`
- Files to Modify: sidebar/navigation config.
- Authentication/Authorization: `RequirePermission` per §17.
- Definition of Done: route live, reachable via navigation, correctly RBAC-guarded.

**Task 06 — Final Code Review**
- Do Not Change: existing `src/features/users`/`src/features/habit-types` modules (reference only, not modified).
- Expected Result: PR merge-ready.

## 30. Definition of Done
Avatar Base Library Management page live, RBAC-guarded, fully functional create/read/update with no destructive delete action, tested.

## 31. Final Verification Checklist
- [ ] CRUD table renders with pagination/filtering/sorting
- [ ] Create/Edit form validates required fields and asset upload
- [ ] No delete action exists anywhere on the page (regression test passing)
- [ ] `RequirePermission` guards all write actions
- [ ] Loading/empty/error states implemented
- [ ] Component and hook tests passing
