# N-03 — Listen-Count Aggregate Calibration Console

## 1. Feature Context
A small, `product_admin`-only settings form controlling the rounding/bucketing thresholds behind the privacy-safe `listen_count_aggregate` field children see on the Bedtime Audio Player — the most access-restricted surface in this feature set given its subtle privacy implications, gated stricter than the standard `content_editor` role used elsewhere in A.4's admin surface.

## 2. Parent Feature
Feature A.4 — Audio Bedtime Player & Bedtime Mode

## 3. Sub-feature
3.3 Listen-Count Aggregate Calibration Console (ID: **N-03**)

## 4. Objective
Build a settings form calling B-06's `PUT /admin/v1/config/listen-count-rounding`, restricted to `product_admin`, requiring a confirm-before-save step, and displaying the resulting audit-trail entry after a successful save.

## 5. Business Requirements
- §8 Admin Requirements: "Listen-Count Aggregate Calibration Tool: Admin-only control for the rounding/bucketing thresholds... to allow tuning without a code deploy."
- §9 (Admin AI prompt item 3): settings form (rounding threshold values) restricted to the `product_admin` role, calling `PUT /admin/v1/config/listen-count-rounding`; changing this value writes an `audit_log` row with before/after values.
- §12.5: restricted to senior `product_admin` role given its subtle privacy-tuning implications.

## 6. Existing Architecture
Follows the existing Admin Portal pattern for restricted, single-purpose settings forms (confirm the closest existing precedent — likely a system-configuration page gated by an elevated role — and mirror its RBAC-enforcement and audit-confirmation pattern rather than inventing a new one for this page).

## 7. Existing Code to Reuse
- `src/shared/components/require-permission.tsx::RequirePermission` (configured for `product_admin`, the stricter role)
- `src/shared/components/confirmation-dialog.tsx::ConfirmationDialog` (confirm-before-save step, mirroring A.3/N-01's reuse of this component for its Archive confirmation)
- Existing audit-log viewer/display component, if one exists in the Admin Portal (reuse for displaying the post-save audit entry; if none exists as a reusable component, render the returned before/after values inline rather than building a full audit-log browsing UI, which is out of scope for this sub-feature)

## 8. Files to Create
- `src/app/(dashboard)/config/listen-count-rounding/page.tsx`
- `src/features/listen-count-config/api/listen-count-config-repository.ts` — `ListenCountConfigRepositoryImpl` (`getCurrent()`, `update()`)
- `src/features/listen-count-config/hooks/use-listen-count-config.ts`
- `src/features/listen-count-config/components/rounding-threshold-form.tsx`
- `src/features/listen-count-config/types/listen-count-config.ts` — Zod schema (`round_above_1000_to_nearest: z.number().int().positive()`, `round_below_1000_to_nearest: z.number().int().positive()`)

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `LISTEN_COUNT_CONFIG.GET`, `LISTEN_COUNT_CONFIG.UPDATE`
- `src/shared/components/dashboard-shell.tsx` — nav item gated by `product_admin` only (not visible to `content_editor`-only admins, consistent with the stricter role)

## 10. NextJS Requirements
- `RoundingThresholdForm`: two numeric inputs (`round_above_1000_to_nearest`, `round_below_1000_to_nearest`), pre-populated from `getCurrent()`, client-side bounds validation mirroring B-06's server-side validation (positive integers within a sane range).
- Save flow: submitting the form opens `ConfirmationDialog` (given the privacy-tuning implications) before the actual `PUT` call fires — this is a deliberate extra friction step, not a standard immediate-save form.
- Post-save: display the returned before/after values (from B-06's audit-log-backed response, or a follow-up read) as an inline confirmation, e.g., "Rounding threshold above 1000 changed from 100 to 50."
- Access: the nav entry point and the page itself are both gated by `product_admin` — a `content_editor`-role admin should not even see this page listed in navigation, not merely be blocked after clicking in.

## 11. Required API
**Admin API** — B-06 `GET /admin/v1/config/listen-count-rounding` (initial load), `PUT /admin/v1/config/listen-count-rounding` (save).

## 12. Authentication / Authorization
`useAdminSession()` plus `RequirePermission permission="product_admin"` — this is the single most restrictive permission check in Feature A.4's entire admin surface; verify it is distinct from and stricter than the `content_editor` role gating N-01/N-02.

## 13. Loading / Empty / Error States
Loading skeleton while `getCurrent()` resolves; save-failure error state distinct from validation error (e.g., network/server error on `PUT` vs. a client-side bounds violation); success confirmation state showing the before/after values.

## 14. Responsive UI / Accessibility
Simple two-field form, standard responsive form layout; confirmation dialog keyboard-accessible and screen-reader-announced (reuses `ConfirmationDialog`'s existing accessibility behavior).

## 15. Localization / RTL
Standard `useTranslation()` for labels/helper text and confirmation-dialog copy; RTL only if the Admin Portal's existing localization scope supports it.

## 16. Security
- `product_admin`-only access enforced at both the navigation-visibility level and the page/route level (defense in depth, mirroring A.3/N-01's per-control RBAC convention).
- No client-side bypass of the confirm-before-save step is possible (the `PUT` call is only reachable from within the confirmed-dialog callback, not a directly-wired form-submit handler).

## 17. Testing
Unit: Zod schema bounds validation. Integration: `RequirePermission` boundary test (`content_editor` role cannot access the page/nav entry, `product_admin` can); confirm-before-save flow (form submit does not call `PUT` until the dialog is confirmed); post-save audit-value display renders correctly from a mocked response.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define the Zod Schema**
Objective: Bounded positive-integer schema for both threshold fields. Files to create: `types/listen-count-config.ts`. Tests: bounds-validation tests. Definition of Done: tests pass.

**Task 02 — Implement `ListenCountConfigRepositoryImpl`**
Objective: `getCurrent()`/`update()` wrapping B-06's two endpoints. Files to create: `api/listen-count-config-repository.ts`. Dependencies: Task 01. Tests: mocked-fetch tests per method. Definition of Done: tests pass.

**Task 03 — Implement `useListenCountConfig` Hook**
Objective: React Query wrapper for read + mutation. Files to create: `hooks/use-listen-count-config.ts`. Dependencies: Task 02. Definition of Done: hook wired correctly.

**Task 04 — Implement `RoundingThresholdForm` with Confirm-Before-Save**
Objective: Two-field form, `ConfirmationDialog`-gated submit, post-save before/after display. Files to create: `components/rounding-threshold-form.tsx`. Dependencies: Task 01, 03. Tests: confirm-before-save flow test (assert `PUT` not called until dialog confirmed). Definition of Done: test passes.

**Task 05 — Implement the Page with `product_admin` Gating**
Objective: Page composing the form, `RequirePermission permission="product_admin"`. Files to create: `app/(dashboard)/config/listen-count-rounding/page.tsx`. Files to modify: `dashboard-shell.tsx` (nav visibility). Dependencies: Task 04. Tests: RBAC boundary test (`content_editor` cannot see nav entry or access page). Definition of Done: test passes.

**Task 06 — Add Full Test Suite**
Objective: Complete coverage per §17. Definition of Done: all green in CI.

**Task 07 — Final Code Review**
Objective: Confirm `product_admin` gating is unbypassable at both nav and page level; confirm the confirm-before-save step cannot be circumvented. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] Form pre-populates from `GET /admin/v1/config/listen-count-rounding`
- [ ] Client-side bounds validation mirrors B-06's server-side validation
- [ ] Save requires explicit confirmation via `ConfirmationDialog` before the `PUT` call fires
- [ ] Post-save state displays the before/after values from the audit-backed response
- [ ] `product_admin` role required at both navigation-visibility and page/route level — `content_editor` cannot see or access this page
- [ ] No direct form-submit-to-`PUT` path exists that bypasses the confirmation dialog

## 20. Definition of Done
Senior admins can safely retune the listen-count privacy-rounding thresholds through a deliberately frictioned, `product_admin`-only console that surfaces the resulting audit trail — with zero access for standard content-editor admins and zero way to bypass the confirm-before-save step.
