# N-04 — Comp Grant Tool

## 1. Feature Context
The deliberate, justified issuance surface for the platform's one sanctioned entitlement exception — a required reason code, a visible preview of the resulting effect, and a confirmation step, designed so a comp grant can never be issued casually or by accident.

## 2. Parent Feature
E.33 — Subscription Management & Billing Ops

## 3. Sub-feature
2.4 Comp Grant Tool (ID: **N-04**)

## 4. Objective
Build the Comp Grant Tool screen against B-04, with submit disabled until a reason code is provided, and a clear preview of the resulting entitlement effect before final confirmation.

## 5. Business Requirements
- §1.18 screen 9: Comp Grant Tool (reason code, audited).
- §2.2: reason-code dropdown/field required, duration/scope specification, entitlement-effect preview, confirmation step.
- §7 Frontend AI prompt item 2: submit action is disabled until a non-empty `reason_code` is selected/entered — test confirms submission is blocked without it.

## 6. Existing Architecture
`src/features/comp-grant-tool/` module, reached from N-03's Subscription Detail screen.

## 7. Existing Code to Reuse
- `src/shared/components/require-permission.tsx::RequirePermission`
- `src/shared/components/confirmation-dialog.tsx::ConfirmationDialog`

## 8. Files to Create
- `src/app/(dashboard)/commerce/subscriptions/[id]/comp-grant/page.tsx`
- `src/features/comp-grant-tool/api/comp-grant-repository.ts`
- `src/features/comp-grant-tool/hooks/use-issue-comp-grant.ts`, `use-reason-codes.ts`
- `src/features/comp-grant-tool/components/comp-grant-form.tsx`
- `src/features/comp-grant-tool/components/entitlement-effect-preview.tsx`
- `src/features/comp-grant-tool/types/comp-grant.ts` — Zod schema

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `COMP_GRANT.*` endpoints

## 10. NextJS Requirements
- `CompGrantForm`: `reason_code` selection sourced from a live reason-code registry (or a fixed, reviewed enum if the PRD does not specify a dynamic registry — confirm against backend schema; default to enum-driven dropdown); submit button `disabled` until `reason_code` is non-empty — this is a direct form-state binding, not a separately-maintained validation flag that could drift out of sync.
- `EntitlementEffectPreview`: renders the resulting entitlement level/duration before submission, computed from the form's current values, so the admin sees exactly what will be granted before confirming.
- Confirmation step required after the form is valid, before the actual `POST` fires.

## 11. Required API
**Admin API** — B-04: `POST /v1/admin/subscriptions/{id}/comp-grant`.

## 12. Authentication / Authorization
`useAdminSession()` base auth; `RequirePermission permission="billing_ops"` (comp-grant issuance restricted to `billing_ops` specifically, per §12.5).

## 13. Loading / Empty / Error States
Form validation error for missing reason code (though structurally the submit button is disabled, a defense-in-depth server-error-mapped message is still shown if the request is somehow attempted); issuance success state confirming the grant now appears in N-03's timeline.

## 14. Responsive UI / Accessibility
Submit-disabled state communicated via both the disabled attribute and an accessible explanation ("Select a reason to continue"), not disabled-styling alone.

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()`.

## 16. Security
The disabled-until-reason-code-present submit gating is this screen's defining guarantee — mandatory test confirms the submit button is genuinely disabled (not merely styled to look disabled) with an empty `reason_code`, and that no code path can dispatch the mutation while it is empty (e.g., no keyboard-Enter bypass).

## 17. Testing
Unit: `reason_code`-empty disables submit-state logic. UI: **mandatory** — submission is blocked (both button-disabled and no dispatch on Enter/other bypass) without a reason code. Integration: full issue-comp-grant → N-03-timeline-reflects-it flow.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schema & Add API Endpoints**
Objective: `comp-grant.ts` schema with required `reason_code`. Files: `types/comp-grant.ts`, `api-endpoints.ts`. Tests: schema validation. Definition of Done: schema used by Task 03.

**Task 02 — Implement `CompGrantRepositoryImpl`**
Objective: Repository for B-04's endpoint. Tests: mocked-fetch tests. Dependencies: Task 01. Definition of Done: tests pass.

**Task 03 — Implement `CompGrantForm` with Disabled-Until-Reason-Code Gating**
Objective: Direct form-state-bound submit-disable logic. Dependencies: Task 02. Tests: **mandatory** — submit-blocked-without-reason-code test, including Enter-key-bypass check. Definition of Done: test passes.

**Task 04 — Implement `EntitlementEffectPreview`**
Objective: Live preview computed from current form values. Dependencies: Task 03. Tests: preview-updates-with-form-changes test. Definition of Done: test passes.

**Task 05 — Implement the Comp Grant Tool Page with Confirmation Step**
Objective: Compose form + preview + confirmation dialog before dispatch. Dependencies: Tasks 03–04. Tests: full-flow smoke test. Definition of Done: test passes.

**Task 06 — Add Full Test Suite**
Objective: Complete coverage per §17, including the mandatory gating test. Definition of Done: all green in CI.

**Task 07 — Final Code Review**
Objective: Confirm no bypass exists for the reason-code-required submit gate. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] Submit disabled until `reason_code` is non-empty — mandatory test passing, including keyboard-bypass check
- [ ] Entitlement-effect preview accurately reflects current form values before submission
- [ ] Confirmation step required before the mutation dispatches
- [ ] `billing_ops` scope enforced

## 20. Definition of Done
Comp grants are issued only through a deliberate, gated, previewed, and confirmed flow — impossible to trigger without a genuine, entered justification.
