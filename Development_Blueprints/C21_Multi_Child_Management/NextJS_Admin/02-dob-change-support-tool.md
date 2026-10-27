# N-02 — DOB Change Support Tool

## 1. Feature Context
Part of Feature C.21 — Multi-Child Management's Admin Requirements (§8): the Admin Portal surface for the single sanctioned bypass of B-02's DOB-immutability guarantee.

## 2. Parent Feature
C.21 Multi-Child Management

## 3. Sub-feature
**N-02 — DOB Change Support Tool**

## 4. Objective
Let Support staff correct a genuinely wrong, locked DOB from within a Support Case view, requiring a mandatory reason and identity-verification confirmation, calling B-10's dedicated backend endpoint and never bypassing the confirmation step client-side.

## 5. Business Requirements
- §8: "DOB Change Support Tool: the one legitimate path for post-lock DOB correction — requires documented reason and identity verification, fully audited."
- §9 Admin AI Prompt: "an action 'Correct Child Date of Birth' requiring a mandatory reason field and identity-verification confirmation before calling a dedicated backend endpoint... Every use writes a high-sensitivity audit_log entry... Restricted to support role."

## 6. Existing Architecture
Follows the same high-risk-action pattern already established for `DeleteFamilyButton`/`useDeleteFamily` in `NEXT-JS-INSTRUCTIONS.md` §15 ("Complete End-to-End High-Risk Action Example") — this sub-feature is a direct structural analog, reusing `useElevatedSession()` for identity verification rather than inventing a parallel mechanism.

## 7. Existing Code to Reuse
- `useElevatedSession()` — reused verbatim for the identity-verification step (OTP-based elevation), exactly as `DeleteFamilyButton` uses it.
- `ConfirmationDialog` — reused for the confirmation modal, with `isDanger` set given the sensitivity.
- `RequirePermission permission="dob-correction:write"` — frontend `resource:action` string (per the existing `users:read`-style convention), mapping down to the backend's confirmed bare `support` role (B-10). Confirm this specific `AdminPermission` entry exists or add it, mapped to `support`.
- `apiClient.patch()` — via a dedicated repository method, never called directly from the component.

## 8. Files to Create
- `src/features/child-deletion-audit/api/dob-correction-client.ts` (or a new `src/features/support-tools/` feature module if DOB correction doesn't logically belong alongside the deletion-audit feature — confirm module boundary before creating).
- `src/features/support-tools/hooks/use-dob-correction.ts`
- `src/features/support-tools/components/dob-correction-action.tsx`

## 9. Files to Modify
- Support Case detail view/page — embed the "Correct Child Date of Birth" action.
- `src/shared/constants/api-endpoints.ts` — add the DOB-correction endpoint (path pending B-10's confirmation).

## 10. Backend Requirements
Consumes B-10 exclusively (⚠ endpoint path pending confirmation, see that blueprint).

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- `useDobCorrection()` — React Query mutation hook, structurally identical to `useDeleteFamily()`: accepts `{ elevatedToken, childId, newDob, reason }`.
- Form: mandatory `reason` textarea (non-empty, minimum length validated via Zod), `newDob` date picker, and the `useElevatedSession()` OTP step before submission is enabled.
- `ConfirmationDialog` with `isDanger` shown before the final submit, restating the old and new DOB values for a last-look confirmation.
- On success, the Support Case view reflects the correction (e.g., an inline audit note referencing the new `audit_logs` entry, if the case view surfaces recent actions).

## 13. API Contract
Consumes B-10's contract as documented in that blueprint (`{ newDob, reason, identityVerificationConfirmed }`) at `PATCH /v1/admin/children/{id}/dob-correction`, now confirmed. Note B-10's one remaining open item: whether a server-side elevation/OTP-verification mechanism already exists — if B-10's Task 01 concludes a new backend primitive is needed, `identityVerificationConfirmed` here may instead become a real `elevatedToken` parameter sourced from this component's own `useElevatedSession()` call, matching the `useDeleteFamily` pattern exactly. Confirm the final field shape with B-10's implementer before finalizing this component's mutation payload.

## 14. Database Requirements
Not applicable — Admin Portal has no direct DB access.

## 15. Validation
- `reason`: Zod `.min(20)` or similar substantive-length requirement (exact threshold to be agreed with the reason validation already enforced server-side in B-10 — client-side should mirror, not diverge from, the server's actual minimum).
- `newDob`: valid date, not in the future, roughly consistent with reasonable child age bounds (client-side sanity check only; server is authoritative).

## 16. Authentication
`useAdminSession()` standard guard.

## 17. Authorization
`RequirePermission permission="dob-correction:write"` (narrower than general admin write, mirroring B-10's `support:write` scope) wraps the action component.

## 18. Error Handling
- Form-level Zod validation errors shown inline.
- API `422` (reason/confirmation missing) mapped to a clear inline error, even though the client-side form should make this state unreachable — defense in depth.
- API `403` (missing scope) → `ErrorView`.
- Elevation (`useElevatedSession`) failure → surfaced via the existing OTP-retry UX already established for `useDeleteFamily`.

## 19. Offline First
Not applicable — Admin Portal.

## 20. Local Data
Not applicable.

## 21. Localization
Form labels, warning/confirmation copy, and the "Correct Child Date of Birth" action label all sourced via `useTranslation()`.

## 22. RTL
Form and dialog layout mirrored correctly under RTL.

## 23. Analytics
Not specified in the PRD; the `audit_logs` entry created server-side (B-10) is the authoritative record of use, not a product-analytics event.

## 24. Performance
Single-action form, no performance concerns beyond standard mutation-hook loading states.

## 25. Security
- This is the platform's single sanctioned bypass of DOB immutability — the client-side form must make it structurally impossible to submit without both a non-empty reason and a completed elevation step (submit button disabled until both conditions hold).
- Reuses `useElevatedSession()` exactly as the existing high-risk `useDeleteFamily` pattern does — no parallel, weaker identity-verification mechanism is introduced.
- Never logs the reason/OTP/old-new-DOB values to `console`/client-side analytics — rely entirely on the server-side `audit_logs` entry as the record.

## 26. Library Requirements
No new libraries — reuses TanStack Query, Zod, existing `ConfirmationDialog`.

## 27. Testing
- Unit: Zod schema rejects empty/too-short `reason`.
- Integration/UI: submit button disabled until both `reason` is valid and elevation is completed.
- Integration/UI: `ConfirmationDialog` correctly restates old/new DOB before final submit.
- Integration/UI: `RequirePermission` correctly hides the action for an admin lacking `dob-correction:write`.
- Integration: full end-to-end correction flow (mocked backend) verifying the mutation payload matches B-10's contract exactly.

## 28. Documentation
Document prominently that this component is the sole legitimate DOB-correction path in the Admin Portal, cross-referencing B-10 and the backend's database-trigger sanction mechanism, so no one is tempted to build a second, weaker path elsewhere.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Wire Confirmed Endpoint Path & Permission String; Confirm Elevation Mechanism**
- **Objective:** B-10's path (`/v1/admin/children/{id}/dob-correction`) and role (`support`) are now confirmed. The one remaining item — whether `useElevatedSession()` alone suffices or B-10 introduces a new backend elevation primitive — should be resolved alongside B-10's Task 01 before finalizing this component's mutation payload shape.
- **Definition of Done:** Endpoint constant and permission string added; final mutation payload shape confirmed with B-10's implementer.

**Task 02 — Resource Client & Mutation Hook**
- **Objective:** Build the API client and `useDobCorrection()` mutation hook.
- **Files to Create:** `dob-correction-client.ts`, `use-dob-correction.ts`.
- **Implementation Details:** Mirrors `useDeleteFamily()`'s structure exactly — `mutate({ elevatedToken, childId, newDob, reason })`.
- **Tests:** Unit tests for the client and hook.
- **Definition of Done:** Hook correctly requires an `elevatedToken` parameter, structurally impossible to call without one.

**Task 03 — Form & Confirmation UI**
- **Objective:** Build the reason/date form, elevation step, and confirmation dialog.
- **Files to Create:** `dob-correction-action.tsx`.
- **Implementation Details:** Submit disabled until `reason` valid and `hasElevation` true (from `useElevatedSession()`); `ConfirmationDialog` restates old/new DOB.
- **Tests:** UI tests per §27.
- **Definition of Done:** Structurally impossible to submit without both gates satisfied.

**Task 04 — Support Case View Integration**
- **Objective:** Embed the action within the existing Support Case detail view, behind `RequirePermission`.
- **Files to Modify:** Support Case page/component.
- **Tests:** Permission-gating integration test.
- **Definition of Done:** Action visible only to admins with `dob-correction:write`; fully functional end-to-end against a mocked B-10.

## 30. Definition of Done
DOB correction tool is fully functional, reuses the established high-risk-action pattern (`useElevatedSession` + `ConfirmationDialog`), structurally prevents submission without both a valid reason and completed elevation, and is permission-gated.

## 31. Final Verification Checklist
- [ ] Endpoint path, permission string, and module placement confirmed with B-10's owner
- [ ] Submit structurally blocked until reason is valid AND elevation completed
- [ ] `ConfirmationDialog` restates old/new DOB before final submit
- [ ] `RequirePermission` correctly gates the action
- [ ] No sensitive values (reason/OTP/DOB) logged client-side
- [ ] Full localization and RTL verified
- [ ] Mutation payload matches B-10's contract exactly
