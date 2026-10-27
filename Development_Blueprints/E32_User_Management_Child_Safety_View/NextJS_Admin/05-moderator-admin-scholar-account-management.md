# N-05 — Moderator/Admin/Scholar Account Management

## 1. Feature Context
The operator-facing counterpart to N-01–N-04's parent/child-facing screens: provisioning, role-reassigning, and disabling/re-enabling the internal accounts that staff this entire module, with role options always sourced from E.28's live registry.

## 2. Parent Feature
E.32 — User Management & Child Safety View

## 3. Sub-feature
2.5 Moderator/Admin/Scholar Account Management (ID: **N-05**)

## 4. Objective
Build the operator user list, provisioning form, account detail/role-reassignment, and disable/re-enable confirmation flows against B-07, with the role dropdown populated exclusively from E.28's live role registry.

## 5. Business Requirements
- List/search operator accounts (moderator/admin/scholar).
- Provision a new operator account with an initial role.
- Reassign role at any time; role options always reflect the currently live registry, never a stale/hardcoded list.
- Disable/re-enable with confirmation dialogs; disabled accounts shown with a muted visual treatment (reuse C.21's pattern).

## 6. Existing Architecture
`src/features/operator-accounts/` module.

## 7. Existing Code to Reuse
- `src/shared/components/require-permission.tsx::RequirePermission`
- `src/shared/components/data-table.tsx::DataTable`
- `src/shared/components/confirmation-dialog.tsx::ConfirmationDialog`
- C.21's disabled-account muted visual treatment pattern (reused, not reinvented)
- E.28's role registry read endpoint (consumed here, not owned)

## 8. Files to Create
- `src/app/(dashboard)/operators/page.tsx`
- `src/app/(dashboard)/operators/new/page.tsx`
- `src/app/(dashboard)/operators/[id]/page.tsx`
- `src/features/operator-accounts/api/operator-account-repository.ts`
- `src/features/operator-accounts/hooks/use-operator-list.ts`, `use-operator-detail.ts`, `use-live-role-registry.ts`, `use-provision-operator.ts`, `use-reassign-role.ts`, `use-disable-reenable.ts`
- `src/features/operator-accounts/components/operator-provisioning-form.tsx`
- `src/features/operator-accounts/components/role-reassignment-dropdown.tsx`
- `src/features/operator-accounts/components/disable-reenable-confirmation.tsx`
- `src/features/operator-accounts/types/operator-account.ts` — Zod schema

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `OPERATOR_ACCOUNTS.*` endpoints
- `src/shared/components/dashboard-shell.tsx` — nav item under "Users" group, `admin`-scope-gated

## 10. NextJS Requirements
- `RoleReassignmentDropdown`: options fetched live from the role-registry endpoint on every mount — never a hardcoded enum in this component, so a retired role automatically disappears from the selectable list without a frontend deploy.
- Disabled operator rows render with C.21's exact muted-row visual treatment (reused component/class, not a new style).
- Provisioning form validates against the same live registry for the initial role.

## 11. Required API
**Admin API** — B-07: `POST /v1/admin/operators`, `GET /v1/admin/operators`, `GET /v1/admin/operators/{id}`, `PATCH /v1/admin/operators/{id}/role`, `PATCH /v1/admin/operators/{id}/disable`, `PATCH /v1/admin/operators/{id}/re-enable`. E.28's role registry read endpoint.

## 12. Authentication / Authorization
`useAdminSession()` base auth; `RequirePermission permission="admin"` for this entire module (elevated above the baseline `support` scope used elsewhere in E.32, matching B-07's elevated scope requirement).

## 13. Loading / Empty / Error States
List loading skeleton; provisioning validation errors (including `422 UNKNOWN_ROLE` mapped to a field-level error); re-enable `409 ROLE_NO_LONGER_ACTIVE` surfaced as a distinct state prompting a new role selection rather than a generic error.

## 14. Responsive UI / Accessibility
Role dropdown correctly announces when options have changed since last fetch (e.g., "role list updated") if a stale selection becomes invalid mid-session.

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()`.

## 16. Security
Role options sourced live on every render path, never cached across a long-lived session — mandatory test confirms a retired role does not appear as a selectable option even if the component was mounted before the role was retired.

## 17. Testing
Unit: live-registry-fetch-on-mount logic for the role dropdown. UI: **mandatory** — retired role does not appear in the dropdown after a fresh fetch; disabled operator rows use C.21's muted treatment (visual-regression or class-assertion test). Integration: full provision → reassign-role → disable → re-enable (with role-still-active) flow; full disable → re-enable-with-retired-role → blocked-with-new-role-prompt flow.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schema & Add API Endpoints**
Objective: `operator-account.ts` schema. Files: `types/operator-account.ts`, `api-endpoints.ts`. Tests: schema validation. Definition of Done: schema used by Task 03.

**Task 02 — Implement `OperatorAccountRepositoryImpl`**
Objective: Repository for B-07's six endpoints plus role-registry read. Tests: mocked-fetch tests. Dependencies: Task 01. Definition of Done: tests pass.

**Task 03 — Implement `RoleReassignmentDropdown` with Live Registry Fetch**
Objective: Options fetched fresh on mount, never hardcoded. Dependencies: Task 02. Tests: **mandatory** — retired-role-absent-from-options test. Definition of Done: test passes.

**Task 04 — Implement `OperatorProvisioningForm`**
Objective: Initial-role selection via the same live dropdown. Dependencies: Task 03. Tests: form validation tests. Definition of Done: tests pass.

**Task 05 — Implement `DisableReenableConfirmation` (Reusing C.21's Muted Treatment)**
Objective: Confirmation dialogs; disabled-row visual treatment reused from C.21. Dependencies: Task 02, C.21. Tests: reuse-not-reimplementation check. Definition of Done: zero duplicated styling logic.

**Task 06 — Implement the List, Provisioning, and Detail Pages**
Objective: Compose all components with loading/empty/error states. Dependencies: Tasks 03–05. Tests: full-page smoke tests. Definition of Done: tests pass.

**Task 07 — Add Full Test Suite**
Objective: Complete coverage per §17, including the mandatory retired-role test. Definition of Done: all green in CI.

**Task 08 — Final Code Review**
Objective: Confirm zero hardcoded role list exists anywhere in this module. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] Role dropdown options fetched live, never hardcoded — mandatory retired-role test passing
- [ ] Disabled operator rows reuse C.21's exact muted visual treatment
- [ ] `422 UNKNOWN_ROLE` and `409 ROLE_NO_LONGER_ACTIVE` surfaced as distinct, explained states
- [ ] `admin`-scope gating enforced on the entire module

## 20. Definition of Done
Admins can provision and manage operator accounts through a UI whose role options are provably always in sync with E.28's live registry, with disable/re-enable semantics visually consistent with C.21's established pattern.
