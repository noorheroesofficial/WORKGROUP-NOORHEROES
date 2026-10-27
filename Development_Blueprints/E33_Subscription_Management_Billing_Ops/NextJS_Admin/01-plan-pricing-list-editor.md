# N-01 — Plan/Pricing List & Editor

## 1. Feature Context
The authoring surface where non-retroactivity is made visible and deliberate in the UI: the entitlement-update form defaults to new-subscribers-only, and "apply to existing subscribers" is a separate, explicitly-confirmed secondary action — never a default-checked convenience.

## 2. Parent Feature
E.33 — Subscription Management & Billing Ops

## 3. Sub-feature
2.1 Plan/Pricing List & Editor (ID: **N-01**)

## 4. Objective
Build the Plan/Pricing List and Plan Editor screens against B-01, with the entitlement-update form's `apply_to_existing` control implemented as a distinct, secondary, separately-confirmed action.

## 5. Business Requirements
- FR-1/FR-2: Plan/Pricing Editor screen; create plan; update entitlements.
- §7 Frontend AI prompt item 3: the entitlement-update form defaults to new-subscribers-only scope, with "apply to existing subscribers" presented as a separate, explicitly-confirmed action (e.g., a secondary checkbox with its own confirmation step) rather than a default-checked option — a test must confirm default submission never includes `apply_to_existing=true` unless explicitly checked and confirmed.

## 6. Existing Architecture
`src/features/plan-management/` module, following the Admin Portal's dense professional-tool visual register (E.28 §2.1), reached from the "Commerce" navigation group.

## 7. Existing Code to Reuse
- `src/shared/components/require-permission.tsx::RequirePermission`
- `src/shared/components/data-table.tsx::DataTable`
- `src/shared/components/confirmation-dialog.tsx::ConfirmationDialog`

## 8. Files to Create
- `src/app/(dashboard)/commerce/plans/page.tsx`
- `src/app/(dashboard)/commerce/plans/[id]/page.tsx`
- `src/app/(dashboard)/commerce/plans/new/page.tsx`
- `src/features/plan-management/api/plan-repository.ts`
- `src/features/plan-management/hooks/use-plan-list.ts`, `use-plan-detail.ts`, `use-create-plan.ts`, `use-update-entitlements.ts`
- `src/features/plan-management/components/plan-editor-form.tsx`
- `src/features/plan-management/components/entitlement-update-form.tsx`
- `src/features/plan-management/components/apply-to-existing-secondary-action.tsx` — the isolated, separately-confirmed control
- `src/features/plan-management/types/plan.ts` — Zod schema

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `PLANS.*` endpoints
- `src/shared/components/dashboard-shell.tsx` — nav item under new "Commerce" group

## 10. NextJS Requirements
- `EntitlementUpdateForm`: submits with `apply_to_existing` omitted (or `false`) by default — this field is never bound to the form's primary submit button state.
- `ApplyToExistingSecondaryAction`: a visually and structurally separate control (own checkbox, own explanatory copy about the broader blast radius, own confirmation dialog) — checking it and confirming it is the only way `apply_to_existing=true` is ever included in the outgoing request payload.
- Plan list shows active/deactivated status with clear visual distinction.

## 11. Required API
**Admin API** — B-01: `POST /v1/admin/plans`, `PATCH /v1/admin/plans/{id}`.

## 12. Authentication / Authorization
`useAdminSession()` base auth; `RequirePermission permission="billing_ops"`.

## 13. Loading / Empty / Error States
List loading skeleton; "No plans yet" empty state; entitlement-update validation errors; the broader-application confirmation step explicitly names the number of affected existing subscribers before final confirmation, where available.

## 14. Responsive UI / Accessibility
`ApplyToExistingSecondaryAction`'s explanatory copy is programmatically associated with its checkbox (`aria-describedby`), not conveyed by placement/proximity alone.

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()`.

## 16. Security
The isolation of `apply_to_existing` into its own secondary, separately-confirmed component is this screen's defining guarantee — mandatory test confirms the default form submission payload never includes `apply_to_existing: true` under any circumstance short of the explicit secondary confirmation flow completing.

## 17. Testing
Unit: default form payload omits/falses `apply_to_existing`. UI: **mandatory** — default submission never includes `apply_to_existing=true`; **mandatory** — the secondary action requires both the checkbox and its own confirmation step before the flag is included. Integration: full plan-creation flow; full entitlement-update (default, new-subscribers-only) flow; full apply-to-existing broader-application flow with its distinct confirmation.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schema & Add API Endpoints**
Objective: `plan.ts` schema. Files: `types/plan.ts`, `api-endpoints.ts`. Tests: schema validation. Definition of Done: schema used by Task 03.

**Task 02 — Implement `PlanRepositoryImpl`**
Objective: Repository for B-01's endpoints. Tests: mocked-fetch tests. Dependencies: Task 01. Definition of Done: tests pass.

**Task 03 — Implement `PlanEditorForm`**
Objective: Create/edit form for pricing/entitlements/child capacity. Dependencies: Task 02. Tests: form validation tests. Definition of Done: tests pass.

**Task 04 — Implement `EntitlementUpdateForm` Defaulting to New-Subscribers-Only**
Objective: Default payload never includes `apply_to_existing=true`. Dependencies: Task 02. Tests: **mandatory** — default-omits-flag test. Definition of Done: test passes.

**Task 05 — Implement `ApplyToExistingSecondaryAction`**
Objective: Isolated checkbox + confirmation dialog, sole path to `apply_to_existing=true`. Dependencies: Task 04. Tests: **mandatory** — flag only included after both checkbox and confirmation complete. Definition of Done: test passes.

**Task 06 — Implement the List, New, and Editor Pages**
Objective: Compose all components with loading/empty/error states. Dependencies: Tasks 03–05. Tests: full-page smoke tests. Definition of Done: tests pass.

**Task 07 — Add Full Test Suite**
Objective: Complete coverage per §17, both mandatory tests included. Definition of Done: all green in CI.

**Task 08 — Final Code Review**
Objective: Confirm zero code path in this module can set `apply_to_existing=true` outside the isolated secondary-action flow. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] Default entitlement-update submission never includes `apply_to_existing=true` — mandatory test passing
- [ ] `apply_to_existing=true` reachable only via the isolated secondary action with its own confirmation — mandatory test passing
- [ ] Plan list clearly distinguishes active/deactivated status
- [ ] `billing_ops` scope enforced on the entire module

## 20. Definition of Done
Plan authoring correctly reflects the platform's non-retroactive-by-default philosophy at the UI level, with the higher-risk broader-application path structurally isolated and impossible to trigger accidentally.
