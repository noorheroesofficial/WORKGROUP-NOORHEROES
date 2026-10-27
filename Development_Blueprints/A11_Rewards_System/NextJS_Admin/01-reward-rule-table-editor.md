# N-01 — Reward Rule Table Editor

> **⚠ DEPRECATED — superseded by `E31_Engagement_Tools_Admin_Suite/NextJS_Admin/03-xp-rule-management-ui.md`.** Backend counterpart B-09 is likewise deprecated in favor of E.31 B-03. Do not implement this file — implement E.31's XP Rule Management UI instead. Retained for historical/design-rationale reference only.

## 1. Feature Context
Part of Feature A.11 — Rewards System. Admin economy-configuration surface for the activity-type → XP/Noor-Heroes-Points reward-rule table.

## 2. Parent Feature
A.11 Rewards System — NextJS Admin

## 3. Sub-feature
N-01 Reward Rule Table Editor

## 4. Objective
Build the Reward Rule Table Editor page consuming B-09, restricted to `economy_design`/`product_admin` roles, per PRD §8.

## 5. Business Requirements
- Table of `activity_type` rows, each editable for `xp_value`, `noor_points_value`, age-band overrides, `daily_cap`.
- Editing a rule creates a **new version**, never mutates a live version — version history shown per `activity_type`.
- Restricted to `economy_design`/`product_admin` role.

## 6. Existing Architecture
Existing NextJS Admin Portal shell: `BaseResourceClient` pattern for CRUD resource clients, `apiClient.get/post/patch/delete` wrapper, `DataTable`, `RequirePermission`, `ConfirmationDialog`, `FilterPanel`/`SearchBar`/`EmptyState`/`ErrorView`/`LoadingState` shared components (`NEXT-JS-INSTRUCTIONS.md §5–8`).

## 7. Existing Code to Reuse
- `BaseResourceClient` (extended into a `RewardRuleResourceClient`).
- `DataTable`, `RequirePermission`, `ConfirmationDialog`, `LoadingState`, `ErrorView`, `EmptyState`.
- `apiClient.get/post` wrapper with existing auth-header attachment.
- `hasPermission(admin, permission)` utility.

## 8. Files to Create
- `src/features/rewards/rule-table/RewardRuleResourceClient.ts`
- `src/features/rewards/rule-table/RewardRuleTablePage.tsx`
- `src/features/rewards/rule-table/RewardRuleVersionHistoryDialog.tsx`
- `src/features/rewards/rule-table/RewardRuleEditForm.tsx`
- `src/features/rewards/rule-table/__tests__/RewardRuleTablePage.test.tsx`

## 9. Files to Modify
- Admin app route registry — add `/rewards/rules` route.
- Admin nav/sidebar config — add "Reward Rules" entry under a "Rewards" section, gated by `RequirePermission`.

## 10. Backend Requirements
Consumes B-09 (`/v1/admin/rewards/rules`).

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- `RewardRuleResourceClient extends BaseResourceClient` implementing `list()`, `get()`, `create()` (no `update()`/`delete()` exposed at the client layer — editing always calls `create()` to produce a new version, matching B-09's contract).
- `RewardRuleTablePage` renders via `DataTable` with a "Version History" action per row opening `RewardRuleVersionHistoryDialog`.
- Form validation (positive values, non-overlapping windows) mirrored client-side ahead of the server's own validation, for immediate feedback.
- Wrapped in `RequirePermission` for `economy_design`/`product_admin`.

## 13. API Contract
`GET /v1/admin/rewards/rules`, `POST /v1/admin/rewards/rules` (B-09).

## 14. Database Requirements
N/A (admin frontend; no local DB).

## 15. Validation
Client-side form validation mirrors B-09's server-side rules (positive values, no overlapping windows); UI test confirming a submitted edit always calls `create()`, never a mutating `PATCH` on an existing version.

## 16. Authentication
Reuses existing Admin session/auth flow (`signIn`, `useAdminSession()`).

## 17. Authorization
`RequirePermission` gate for `economy_design`/`product_admin`; unauthorized users see a permission-denied state, not a broken page.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Fetch failure | `ErrorView` with retry |
| Empty rule table (first-time setup) | `EmptyState` with a clear "add your first rule" call to action |
| Invalid submission | Inline field-level errors from `parseApiError` |
| Insufficient permission | `RequirePermission` renders a permission-denied state, not a 500/blank page |

## 19. Offline First
Not applicable (admin web).

## 20. Local Data
Not applicable.

## 21. Localization
Admin UI strings localized per the existing Admin Portal localization config (`fetchLocalizationConfig`, `updateLanguagePreference`); rule-table field labels included in that resource set.

## 22. RTL
Table/form layout mirrors correctly for Arabic admin locale, consistent with existing Admin Portal RTL support.

## 23. Analytics
N/A (internal admin action, audit-logged server-side per B-09).

## 24. Performance
`DataTable` pagination for large rule sets; version-history dialog fetches lazily on open, not preloaded for every row.

## 25. Security
Client never exposes a mutating action against a historical rule version — the UI structurally only offers "create new version," matching the backend's immutability guarantee.

## 26. Library Requirements
Existing Admin Portal stack (React, TypeScript, existing `DataTable`/form libraries already in use — reuse, do not introduce a new form library).

## 27. Testing
- Unit: form validation logic.
- Integration: create-new-version flow, permission-gated rendering.
- UI test confirming no mutating action exists against a historical version row.

## 28. Documentation
Component-level README/JSDoc noting the "always create, never mutate" UI contract, cross-referenced against B-09.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement `RewardRuleResourceClient`**
- Files to Create: `RewardRuleResourceClient.ts`
- Existing Files to Reuse: `BaseResourceClient`, `apiClient`.
- Definition of Done: `list()`/`get()`/`create()` implemented, no update/delete methods exposed.

**Task 02 — Build `RewardRuleTablePage`**
- Files to Create: `RewardRuleTablePage.tsx`
- Existing Files to Reuse: `DataTable`, `RequirePermission`, `LoadingState`, `ErrorView`, `EmptyState`.
- Definition of Done: table renders with correct states.

**Task 03 — Build `RewardRuleEditForm` & `RewardRuleVersionHistoryDialog`**
- Files to Create: both components.
- Implementation Details: form submission always calls `create()`.
- Tests: version-immutability UI test (mandatory).
- Definition of Done: test passing.

**Task 04 — Wire Route, Nav, and Permission Gate**
- Files to Modify: route registry, nav/sidebar config.
- Definition of Done: `/rewards/rules` reachable only to permitted roles.

**Task 05 — Add Tests & Documentation**
- Documentation: JSDoc per §28.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Reward Rule Table Editor live, versioned edit pattern enforced client-side and server-side, RBAC-gated.

## 31. Final Verification Checklist
- [ ] Edits always call `create()`, no mutating action against historical versions
- [ ] Version history correctly displayed per activity type
- [ ] `RequirePermission` correctly restricts to `economy_design`/`product_admin`
- [ ] Empty/loading/error states render correctly
- [ ] Localization and RTL verified
- [ ] Client-side validation mirrors server-side rules
