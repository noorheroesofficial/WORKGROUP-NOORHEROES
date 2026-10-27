# N-04 — Role & Permission Matrix Management

## 1. Feature Context
Part of E.28. Screens #13–14 in PRD §1.18 (Role List, Permission Matrix Editor). Save actions always create a Maker-Checker proposal, never apply immediately (PRD §7 Frontend AI prompt item 3).

## 2. Parent Feature
E.28 — Admin Portal: Authentication, RBAC & Operations Dashboard

## 3. Sub-feature
N-04 — Role & Permission Matrix Management

## 4. Objective
Build the Role List and Permission Matrix Editor such that every save results in a pending Maker-Checker proposal with no code path applying a change immediately, and the current admin's own role-change save action is disabled/hidden (self-elevation UX guard) — a client-side reinforcement of B-04's server-side guarantee.

## 5. Business Requirements
- FR-3: role changes require a second admin's approval; no self-elevation.
- Acceptance Criteria: proposing admin's own approval is never sufficient; self-elevation attempt rejected regardless of target role.
- §2.1: Maker-Checker Visual Language — clearly state-labeled workflow, proposer/approver identities always visibly distinct.

## 6. Existing Architecture
Extends `DataTable` (Role List) and introduces a new grid-editor pattern (Permission Matrix Editor — role × resource_scope × region × locale × action grid), which has no direct existing analog in the current component library; built from `DataTable`/form primitives already present rather than a wholly new grid component where avoidable.

## 7. Existing Code to Reuse
| Component | Location | Reuse For |
|---|---|---|
| `DataTable` | `src/shared/components/` | Role List |
| `RequirePermission` | `src/shared/components/` | Gate to `super_admin` |
| `ConfirmationDialog` | `src/shared/components/` | Save-as-proposal confirmation |
| `useAdminSession()` | `src/features/auth/hooks/` | Current admin identity, for self-elevation UX guard |
| `usePaginationState`, `useDebouncedValue` | `src/shared/hooks/` | Role List pagination/search if needed |

## 8. Files to Create / Implemented
- `src/app/(dashboard)/platform/roles-permissions/page.tsx` — Role List & Permissions Management View (guarded by `RequirePermission`)
- `src/features/roles-permissions/types.ts` — Role, Permission, and Category Catalog contracts
- `src/features/roles-permissions/schemas/role.schema.ts` — Zod wire schemas and validation
- `src/features/roles-permissions/api/role.repository.ts` — Role repository (`getRoles`, `createRole`)
- `src/features/roles-permissions/hooks/use-roles.ts` — TanStack React Query hooks (`useRoles`, `useCreateRoleMutation`)
- `src/features/roles-permissions/components/create-role-dialog.tsx` — Super Admin role creation modal with permission picker
- `src/features/roles-permissions/components/roles-table.tsx` — Roles and permissions matrix data table
- `src/features/roles-permissions/components/roles-permissions-view.tsx` — Top-level metrics and view shell
- `tests/roles-permissions.test.ts` — Vitest unit and validation test suite


## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `ROLES.BASE`, `ROLES.PERMISSIONS(roleId)`

## 10. NextJS Requirements
- Role List: `DataTable` of roles (name, `requires_2fa`, permission count).
- Permission Matrix Editor: grid of `role_permission` rows (resource_scope × region × locale × action), editable, with a single "Save" action.
- Save action **always** results in a pending Maker-Checker proposal — display a clear "Pending approval" confirmation after save, redirecting to (or linking) the Approval Queue (N-05).
- Self-elevation UX guard: if the target role of the edit matches the current admin's own role (per `useAdminSession()`), disable the Save button with an explanatory tooltip/message — purely a UX reinforcement, since B-04 rejects this server-side regardless.

## 11. API Contract (Consumed)
- `GET /v1/admin/roles` (B-03) — List all canonical and custom roles with permissions
- `POST /v1/admin/roles` (B-03) — Super Admin creation of new administrative role
- `PATCH /v1/admin/roles/{id}/permissions` (B-03/B-04) → always returns a pending-proposal response shape


## 12. Database Requirements
N/A (frontend).

## 13. Validation
Permission-key/resource-scope combination validated client-side against the known set returned by `GET /v1/admin/roles` before submission (defense against obviously-invalid submissions, not a substitute for server-side validation).

## 14. Authentication
Assumes established session.

## 15. Authorization
`super_admin` only — gated via `RequirePermission` at both the route and the Save-action level.

## 16. Error Handling
- `403 SELF_ELEVATION_BLOCKED` from the server → clear, distinct error message (should rarely surface given the client-side guard, but must be handled gracefully as a defense-in-depth server response).
- Standard network/validation error handling via `QueryErrorState`.

## 17. Offline First
N/A.

## 18. Local Data
None persisted.

## 19. Localization
All labels/messages via `useTranslation()`, including permission-key display names (map technical keys to translated human-readable labels).

## 20. RTL
Grid editor layout must mirror correctly for RTL locales — verify column order/direction explicitly, since grid/table RTL mirroring is a common failure point.

## 21. Analytics
Fire `role_change_proposed` on successful proposal creation.

## 22. Performance
Role List uses standard pagination; Permission Matrix Editor's grid should avoid re-rendering the entire grid on every cell edit (scope state updates to the specific row/cell changed).

## 23. Security
Save action must have **no code path** that applies a change immediately — verified by the mandatory UI test (Task 04). Self-elevation guard is UX-only; the actual enforcement is always B-04's server-side check.

## 24. Library Requirements
No new libraries, unless the grid-editor UX genuinely requires a dedicated data-grid library beyond what `DataTable` provides — evaluate `DataTable`'s extensibility first before introducing a new dependency.

## 25. Testing
- **Mandatory test (§7 item 3):** confirm there is no code path where the Permission Matrix Editor's save action applies a change immediately without first creating a proposal.
- Unit: self-elevation guard disables Save for the current admin's own role.
- Integration: full role-change-proposal creation flow, confirming redirect/link to Approval Queue.
- UI test: `403 SELF_ELEVATION_BLOCKED` server response handled gracefully even though the client-side guard should normally prevent reaching it.

## 26. Documentation
Note in the NextJS admin manual that any future "save" action on a high-risk Admin resource should follow this same pending-proposal pattern rather than direct apply.

## 27. AI Coding Agent Implementation Steps

**Task 01 — Build Role List Page**
- Task ID: N-04-T01
- Files to Create: `role-list.tsx`, `use-roles.ts`, `roles/page.tsx`.
- Implementation Details: `DataTable` of roles from `GET /v1/admin/roles`.
- Dependencies: B-03 endpoint.
- Definition of Done: Role List renders and links into the Permission Matrix Editor per role.

**Task 02 — Build Permission Matrix Editor Grid**
- Task ID: N-04-T02
- Files to Create: `permission-matrix-editor.tsx`, `[roleId]/permissions/page.tsx`.
- Implementation Details: Editable grid over `role_permission` rows for the selected role.
- Performance: Scoped state updates per cell/row edit.
- Dependencies: Task 01.
- Definition of Done: Grid renders and captures edits correctly.

**Task 03 — Implement Save-as-Proposal Flow**
- Task ID: N-04-T03
- Files to Create: `use-propose-role-change.ts`.
- Implementation Details: Save button → `PATCH /v1/admin/roles/{id}/permissions` → always results in pending-proposal confirmation UI, link to Approval Queue.
- Analytics: `role_change_proposed`.
- Dependencies: Task 02, B-04 endpoint.
- Definition of Done: Save always shows "Pending approval" state, never an immediate-apply confirmation.

**Task 04 — Never-Immediate-Apply Signature Test**
- Task ID: N-04-T04
- Objective: Prove no code path applies a change immediately.
- Files to Create: `tests/features/rbac/permission-matrix-editor.test.tsx`.
- Implementation Details: Trace every branch of the save handler; assert all paths call the proposal-creation endpoint, none call a hypothetical direct-apply endpoint.
- Dependencies: Task 03.
- Definition of Done: Test passes; documented as the canonical proof point for §7 item 3.

**Task 05 — Implement Self-Elevation UX Guard**
- Task ID: N-04-T05
- Objective: Disable Save when target role matches the current admin's own role.
- Files to Modify: `permission-matrix-editor.tsx`.
- Implementation Details: Compare target `role_id` against `useAdminSession().admin.role_id`.
- Dependencies: Task 02, N-02 Task 02 (session/permission extension).
- Definition of Done: Save disabled with explanatory message for own-role edits.

**Task 06 — Error Handling for Server-Side Self-Elevation Rejection**
- Task ID: N-04-T06
- Objective: Graceful handling of `403 SELF_ELEVATION_BLOCKED` as defense-in-depth.
- Dependencies: Task 03, Task 05.
- Definition of Done: Error state renders clearly if this response is ever received.

**Task 07 — Localization, RTL, Accessibility Pass**
- Task ID: N-04-T07
- Dependencies: Tasks 01–03.
- Definition of Done: All labels localized; RTL grid mirroring verified.

**Task 08 — Full Test Suite + Documentation**
- Task ID: N-04-T08
- Dependencies: Tasks 01–07.
- Definition of Done: All §25 scenarios green.

**Task 09 — Build Create Role Dialog (Super Admin Role Creation)**
- Task ID: N-04-T09
- Objective: Accessible modal dialog allowing Super Administrators to provision new roles with custom permissions.
- Files to Create: `src/features/roles-permissions/components/create-role-dialog.tsx`, `use-roles.ts` (`useCreateRoleMutation`).
- Implementation Details:
  - Accessible modal dialog (`role="dialog"`, `aria-modal="true"`).
  - Real-time slug auto-generation from role display name with manual override option.
  - 2FA enforcement toggle switch (enabled by default for security).
  - Categorized multi-select permission picker covering standard platform features.
  - Custom permission sub-form for adding arbitrary scoped permission rules (`permissionKey`, `resourceScope`, `region`, `locale`).
  - Gracefully displays validation and 409 Conflict errors without losing form inputs.
- Definition of Done: Modal allows Super Admin to create role via `POST /v1/admin/roles`, invalidating query cache and instantly displaying the new role in `RolesTable`.

## 28. Definition of Done
- Role List and Permission Matrix Editor live, `super_admin`-gated.
- Super Admin Create Role Dialog live and integrated with `POST /v1/admin/roles`.
- Save always creates a pending proposal, proven by a dedicated test.
- Self-elevation UX guard present as defense-in-depth reinforcement of B-04's server-side rejection.

## 29. Final Verification Checklist
- [ ] Signature test passes: save action never applies immediately
- [ ] Self-elevation UX guard disables Save for the admin's own role
- [ ] `403 SELF_ELEVATION_BLOCKED` handled gracefully if received
- [ ] Proposal confirmation links to the Approval Queue
- [ ] Super Admin Create Role Dialog allows creating custom roles with granular permissions
- [ ] Duplicate role key rejected with 409 Conflict error banner
- [ ] `role_change_proposed` analytics event fires correctly

- [ ] RTL grid layout verified
