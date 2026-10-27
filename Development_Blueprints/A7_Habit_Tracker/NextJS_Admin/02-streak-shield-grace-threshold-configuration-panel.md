# N-02 — Streak Shield & Grace Threshold Configuration Panel

## 1. Feature Context
NoorHeroes Admin Portal. Settings form for the fairness-critical streak/grace thresholds backing B-10, restricted to `product_admin`.

## 2. Parent Feature
A.7 Habit Tracker — NextJS Admin

## 3. Sub-feature
N-02 Streak Shield & Grace Threshold Configuration Panel

## 4. Objective
Build a settings form for `change_count_30d` threshold, generous/conservative grace-window durations, and recovery-window length, restricted to `product_admin`, with client and server bounds validation.

## 5. Business Requirements
- Update-only singleton configuration (no create/delete).
- `product_admin` permission strictly required — stricter than N-01's dual-role option.
- Display current effective values with explicit change confirmation before save, given the fairness-critical nature of these values.

## 6. Existing Architecture
`src/app/(dashboard)/habits/streak-config/page.tsx`, `src/features/habit-streak-config/{api,hooks,components}`.

## 7. Existing Code to Reuse
`useAdminSession`, `RequirePermission`, `hasPermission`, existing Admin Portal settings-form pattern (reuse whichever existing singleton-config page pattern exists elsewhere in the Admin Portal, if any, for consistency).

## 8. Files to Create
- `src/app/(dashboard)/habits/streak-config/page.tsx`
- `src/features/habit-streak-config/api/streak-config-repository.ts`
- `src/features/habit-streak-config/hooks/use-streak-config.ts`
- `src/features/habit-streak-config/hooks/use-update-streak-config.ts`
- `src/features/habit-streak-config/components/StreakConfigForm.tsx`
- `src/features/habit-streak-config/components/ChangeConfirmationDialog.tsx`

## 9. Files to Modify
- Admin Portal sidebar/navigation config — add "Streak & Grace Config" entry, `product_admin`-only visibility

## 10. Backend Requirements
Consumes B-10 (`/v1/admin/habits/streak-config`).

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- Form fields: `change_count_30d_threshold`, `generous_grace_days`, `conservative_grace_days`, `recovery_window_days`.
- Explicit confirmation dialog before submitting a change (given fairness-critical impact).
- Display current effective values on load; show previous value alongside new value in the confirmation step.
- `RequirePermission permission="habits:streak-config:write"` (or the project's equivalent `product_admin`-scoped permission string).

## 13. API Contract
`GET/PATCH /v1/admin/habits/streak-config` (B-10) — Admin API, `product_admin` scope.

## 14. Database Requirements
N/A (frontend only).

## 15. Validation
Client-side bounds pre-check mirroring B-10's server validation (positive integers within documented sane ranges); server remains authoritative.

## 16. Authentication
`useAdminSession`.

## 17. Authorization
`RequirePermission` strictly `product_admin`-scoped; no dual-role option (stricter than N-01).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Out-of-bounds value | Inline field error surfaced from the 422 response |
| Unauthorized | `RequirePermission` hides the entire panel for non-`product_admin` roles |
| Save fails | Error toast, form state preserved for retry |

## 19. Offline First
Not applicable.

## 20. Local Data
Not applicable.

## 21. Localization
**Confirmed:** Admin Portal supports multi-locale via `useTranslation()`/`updateLanguagePreference('hi'|'ar'|'en')` (`NEXT-JS-INSTRUCTIONS.md`) — form labels and help text on this panel must use `useTranslation()`, not hardcoded English.

## 22. RTL
**Confirmed:** drive layout via `useLocalization()`'s RTL status; form field order/alignment must mirror correctly.

## 23. Analytics
Not applicable (audit-logged admin action per B-10, not product analytics).

## 24. Performance
Lightweight singleton-form page; no special performance requirements.

## 25. Security
Stricter single-role gate reflects the outsized fairness impact of these values (PRD §8); client-side guard is defense-in-depth only, B-10 is authoritative.

## 26. Library Requirements
Next.js App Router, React Query, existing Admin Portal form components.

## 27. Testing
Form validation tests, confirmation-dialog flow test, RBAC-guard rendering test (`product_admin` vs. other roles).

## 28. Documentation
Inline help text on the form explaining the fairness impact of each field, mirroring B-10's OpenAPI documentation warning.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Scaffold `habit-streak-config` Feature Module**
- Files to Create: `types.ts`, `api/streak-config-repository.ts`
- Definition of Done: module compiles with typed API client.

**Task 02 — Implement Get/Update Hooks**
- Files to Create: `hooks/use-streak-config.ts`, `use-update-streak-config.ts`
- Definition of Done: hooks correctly wrap B-10's endpoints.

**Task 03 — Build `StreakConfigForm` with Confirmation Dialog**
- Files to Create: `StreakConfigForm.tsx`, `ChangeConfirmationDialog.tsx`
- Implementation Details: bounds validation, before/after value display in confirmation.
- Tests: form and confirmation-flow tests.
- Definition of Done: save flow correctly requires explicit confirmation.

**Task 04 — Wire Page Route with Strict RBAC Guard**
- Files to Create: `page.tsx`
- Files to Modify: sidebar/navigation config.
- Definition of Done: route only visible/accessible to `product_admin`.

**Task 05 — Final Code Review**
- Expected Result: PR merge-ready.

## 30. Definition of Done
Streak/grace configuration panel live, `product_admin`-restricted, with explicit change confirmation and bounds validation.

## 31. Final Verification Checklist
- [ ] Form displays current effective values on load
- [ ] Bounds validation matches B-10's server-side rules
- [ ] Explicit confirmation required before save
- [ ] Panel only accessible to `product_admin` role
- [ ] Error handling matches §18
- [ ] Tests passing
