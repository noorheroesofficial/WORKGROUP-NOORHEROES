# N-01 — Lockout & Recovery Support Tool

## 1. Feature Context
A single action added to the existing Support Case view: "Initiate Account Recovery for This Parent." It re-triggers the parent's own standard OTP recovery flow — it does not reset or view a PIN — and every use writes a high-sensitivity audit entry.

## 2. Parent Feature
Feature C.19 — Parent PIN/Biometric Gate & Profile Access Control

## 3. Sub-feature
3.1 Lockout & Recovery Support Tool (ID: **N-01**)

## 4. Objective
Add a `ConfirmationDialog`-gated "Initiate Account Recovery" action to the existing Support Case detail view, wired to B-05's endpoint, restricted to the `support` role, with clear confirmation copy stating this does not reset the PIN directly.

## 5. Business Requirements
- Admin Requirements §8: action-taking (initiate recovery only), behind `support` role, fully audited.
- Never a direct PIN reset — same OTP flow the parent would use themselves.
- Every use writes a high-sensitivity `audit_log` entry.

## 6. Existing Architecture
Extends the existing Support module (`src/features/support/`), following the same `ConfirmationDialog`-based structural pattern used by N-04 (A.1's Risk & Fraud Review Queue decision action) — state → dialog → mutation.

## 7. Existing Code to Reuse
- `src/shared/components/confirmation-dialog.tsx::ConfirmationDialog`
- `src/shared/components/require-permission.tsx::RequirePermission`
- Existing Support Case detail view (`src/features/support/components/support-case-detail.tsx` or equivalent — confirm exact path before adding the action)

## 8. Files to Create
- `src/features/support/api/lockout-recovery-repository.ts` — `LockoutRecoveryRepositoryImpl.initiate(parentId)`
- `src/features/support/hooks/use-initiate-recovery.ts`
- `src/features/support/components/initiate-recovery-dialog.tsx`

## 9. Files to Modify
- `src/features/support/components/support-case-detail.tsx` (or equivalent) — add the "Initiate Account Recovery" action, wrapped in `RequirePermission` for `support`
- `src/shared/constants/api-endpoints.ts` — add `SUPPORT.INITIATE_RECOVERY`

## 10. NextJS Requirements
- `useInitiateRecovery()`: mutation hook calling `POST /v1/admin/support/parents/{id}/recovery/initiate` (B-05); on success, shows a confirmation toast with the masked contact the OTP was sent to; on failure, surfaces the specific error (`403`, `404`, `502`).
- `InitiateRecoveryDialog`: `ConfirmationDialog` with explicit copy: "This will send the parent a standard account-recovery code — it will not reset or reveal their PIN." No destructive/danger styling (this is a supportive, non-destructive action), but still requires explicit confirmation given its sensitivity.
- Action is disabled (not hidden) with a tooltip for non-`support`-role admins viewing the same case, consistent with the platform's "hide, don't dead-end" pattern being an intentional exception here — support staff specifically should see the action exists even if their current role variant lacks it, per standard admin-portal RBAC UX (confirm against existing `RequirePermission` convention: hide vs. disable — follow whichever the Support module already does elsewhere).

## 11. Required API
`POST /v1/admin/support/parents/{id}/recovery/initiate` (B-05).
**Admin API**

## 12. Validation
No form fields — the action itself is the only input (confirmation dialog, no free-text).

## 13. Authentication
Existing Admin Portal auth context (Bearer session).

## 14. Authorization
`support` role required — enforced both by `RequirePermission` (UI-level, hide/disable) and B-05's server-side `require_admin_scope("support")` (authoritative).

## 15. Error Handling
- Loading state on the dialog's confirm button during the mutation.
- Success: toast confirmation with masked contact info.
- `403`: inline error, "You don't have permission for this action."
- `404`: inline error, "Parent record not found."
- `502`: inline error, "Recovery message could not be sent — try again shortly."

## 16. Loading States
Confirm button shows a spinner during the in-flight mutation; dialog cannot be dismissed mid-request to avoid a duplicate double-submit.

## 17. Responsive UI
Action button and dialog follow the existing Support module's responsive breakpoints — no new layout pattern introduced.

## 18. Accessibility
Dialog focus-trapped, confirm/cancel buttons keyboard-navigable, action announced to screen readers on success/failure.

## 19. Localization
Admin Portal is typically EN-only for internal tooling (confirm against NextJS Core Architecture doc's localization scope for admin-facing surfaces before assuming otherwise); if the Admin Portal does support localization, apply the existing i18n convention.

## 20. Testing
- Unit: `useInitiateRecovery` hook success/error branches.
- Component: dialog renders correct confirmation copy, disabled/hidden for non-`support` roles.
- Integration: full click → confirm → success-toast flow against a mocked B-05 response.

## 21. AI Coding Agent Implementation Steps

**Task 01 — Implement `LockoutRecoveryRepositoryImpl`**
Objective: typed API client method for B-05. Files to Create: `lockout-recovery-repository.ts`. Dependencies: B-05 live.

**Task 02 — Implement `useInitiateRecovery` Hook**
Objective: React Query mutation wrapping the repository call. Files to Create: `use-initiate-recovery.ts`. Dependencies: Task 01.

**Task 03 — Implement `InitiateRecoveryDialog`**
Objective: `ConfirmationDialog`-based UI with the specified copy. Files to Create: `initiate-recovery-dialog.tsx`. Dependencies: Task 02.

**Task 04 — Wire Action into Support Case Detail View**
Objective: add the action, `RequirePermission`-gated. Files to Modify: `support-case-detail.tsx`. Dependencies: Task 03.

**Task 05 — Add Full Test Suite**
Objective: coverage per §20. Dependencies: Task 01–04.

## 22. Definition of Done
Support agents with the `support` role can initiate a parent's standard OTP recovery from within the existing Support Case view, with clear non-bypass confirmation copy, correct loading/error states, and server-side-enforced role restriction.

## 23. Final Verification Checklist
- [ ] Action never resets or reveals a PIN — confirmation copy makes this explicit
- [ ] `support` role enforced both client- and server-side
- [ ] Duplicate-submit prevented during in-flight request
- [ ] Success/error states clearly surfaced to the agent
