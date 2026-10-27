# N-02 — Plan Deactivation/Reactivation & Entitlement Matrix

## 1. Feature Context
The confirmation-gated lifecycle actions for a plan, plus a cross-plan comparison view — deactivation and reactivation are deliberately separate, confirmed actions distinct from routine editing, reinforcing that they carry a different (and in deactivation's case, explicitly non-retroactive) blast radius.

## 2. Parent Feature
E.33 — Subscription Management & Billing Ops

## 3. Sub-feature
2.2 Plan Deactivation/Reactivation & Entitlement Matrix (ID: **N-02**)

## 4. Objective
Build the Plan Deactivation and Reactivation confirmation modals against B-01, plus the Entitlement Matrix cross-plan comparison screen.

## 5. Business Requirements
- §1.18 screens 3–4: Plan Deactivation Confirmation, Plan Reactivation Confirmation.
- §1.18 screen 5: Entitlement Matrix (cross-plan comparison view).
- FR-7: deactivation confirmation copy explicitly states existing subscribers are unaffected.
- Edge Case 2: reactivation restores prior configuration, distinct from creating a new plan.

## 6. Existing Architecture
`src/features/plan-lifecycle/` and `src/features/entitlement-matrix/` modules.

## 7. Existing Code to Reuse
- `src/shared/components/confirmation-dialog.tsx::ConfirmationDialog`
- `src/shared/components/data-table.tsx::DataTable` (matrix grid)
- N-01's `PlanRepositoryImpl` (reused, not duplicated)

## 8. Files to Create
- `src/features/plan-lifecycle/components/plan-deactivation-confirmation.tsx`
- `src/features/plan-lifecycle/components/plan-reactivation-confirmation.tsx`
- `src/app/(dashboard)/commerce/entitlement-matrix/page.tsx`
- `src/features/entitlement-matrix/api/entitlement-matrix-repository.ts`
- `src/features/entitlement-matrix/hooks/use-entitlement-matrix.ts`
- `src/features/entitlement-matrix/components/entitlement-matrix-grid.tsx`

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `ENTITLEMENT_MATRIX.*` (or reuse `PLANS.*` list endpoint, aggregated client-side)
- `src/shared/components/dashboard-shell.tsx` — nav item for Entitlement Matrix under "Commerce"

## 10. NextJS Requirements
- `PlanDeactivationConfirmation`: copy explicitly states "Existing subscribers keep their current entitlements — only new subscriptions will be blocked," sourced as a fixed, reviewed string (not dynamically generated, to avoid any drift from the actual guarantee).
- `PlanReactivationConfirmation`: copy explicitly distinguishes this action from creating a new plan, confirming the prior configuration will be restored under the same plan identity.
- `EntitlementMatrixGrid`: read-only cross-plan comparison table, one row per entitlement dimension, one column per plan — reuses N-01's plan-list data, no separate write path.

## 11. Required API
**Admin API** — B-01: `POST /v1/admin/plans/{id}/deactivate`, `POST /v1/admin/plans/{id}/reactivate`, `GET /v1/admin/plans` (list, reused for the matrix).

## 12. Authentication / Authorization
`useAdminSession()` base auth; `RequirePermission permission="billing_ops"`.

## 13. Loading / Empty / Error States
Confirmation-pending state; deactivate/reactivate error state (e.g., reactivating an already-active plan); matrix loading skeleton.

## 14. Responsive UI / Accessibility
Confirmation dialogs fully keyboard-operable, focus trapped correctly per standard modal accessibility pattern.

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()`.

## 16. Security
Deactivation/reactivation confirmation copy is fixed, reviewed text rather than dynamically assembled — avoiding any risk of the UI's stated guarantee drifting out of sync with the backend's actual (structural, per B-01) non-retroactivity behavior.

## 17. Testing
Unit: confirmation copy content matches the fixed, reviewed strings. UI: deactivation confirmation requires explicit confirm before the API call fires; reactivation confirmation distinguishes itself from plan creation in its copy. Integration: full deactivate → plan-shows-inactive-existing-subscribers-unaffected flow (cross-verified against B-01); full reactivate → plan-restored flow; matrix correctly reflects current plan list.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Implement `PlanDeactivationConfirmation`**
Objective: Fixed-copy confirmation dialog. Files: `components/plan-deactivation-confirmation.tsx`. Dependencies: N-01's repository. Tests: confirm-before-call test. Definition of Done: test passes.

**Task 02 — Implement `PlanReactivationConfirmation`**
Objective: Fixed-copy confirmation dialog distinguishing from plan creation. Files: `components/plan-reactivation-confirmation.tsx`. Dependencies: N-01's repository. Tests: copy-content test. Definition of Done: test passes.

**Task 03 — Define Zod Schema & Implement `EntitlementMatrixRepositoryImpl`**
Objective: Aggregate plan-list data for the matrix view. Files: `api/entitlement-matrix-repository.ts`. Dependencies: N-01. Tests: mocked-fetch tests. Definition of Done: tests pass.

**Task 04 — Implement `EntitlementMatrixGrid`**
Objective: Read-only cross-plan comparison table. Dependencies: Task 03. Tests: grid-rendering test. Definition of Done: test passes.

**Task 05 — Implement the Entitlement Matrix Page**
Objective: Compose grid with loading/empty states. Dependencies: Task 04. Tests: full-page smoke test. Definition of Done: test passes.

**Task 06 — Add Full Test Suite**
Objective: Complete coverage per §17. Definition of Done: all green in CI.

**Task 07 — Final Code Review**
Objective: Confirm confirmation copy accurately reflects B-01's actual structural guarantees. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] Deactivation confirmation copy explicitly states existing subscribers are unaffected
- [ ] Reactivation confirmation copy distinguishes itself from plan creation
- [ ] Entitlement Matrix is read-only, reuses N-01's plan data (no duplicated fetch logic)
- [ ] `billing_ops` scope enforced

## 20. Definition of Done
Plan lifecycle actions are deliberately confirmed and accurately explained, and Billing Ops has a clear cross-plan comparison view for entitlement configuration.
