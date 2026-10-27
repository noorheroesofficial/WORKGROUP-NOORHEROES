# N-02 — Badge & Achievement Definition Manager

> **⚠ PARTIALLY DEPRECATED — badge CRUD superseded by `E31_Engagement_Tools_Admin_Suite/NextJS_Admin/05-badge-management-ui.md`.** Mirrors backend B-10's split: E.31's Badge Management UI covers `badges` CRUD but has no `achievement_definitions` (cumulative level) management and no Simulate/dry-run preview tool. Do not implement this file's badge-CRUD screens — implement E.31's Badge Management UI instead. This file's achievement-definition CRUD and Simulate-tool sections remain A.11-owned pending the same architecture-owner decision flagged in B-10.

## 1. Feature Context
Part of Feature A.11 — Rewards System. Admin CRUD for badges/achievement definitions, including a non-mutating criteria "Simulate" dry-run tool.

## 2. Parent Feature
A.11 Rewards System — NextJS Admin

## 3. Sub-feature
N-02 Badge & Achievement Definition Manager

## 4. Objective
Build CRUD forms for `badges`/`achievement_definitions` consuming B-10, including the Simulate tool, restricted to `content_editor`.

## 5. Business Requirements
- CRUD forms for badges (code, structured `criteria_json` builder, `locale_key`, optional `season_id`) and achievement_definitions (`criteria_json`, linked `badge_id`, `xp_value`).
- "Simulate" tool: given a pasted/selected fixture activity history, preview whether criteria would trigger — clearly labeled dry-run, writes no real data.
- Restricted to `content_editor` role.

## 6. Existing Architecture
Existing Admin Portal shell; reuses `BaseResourceClient`, `DataTable`, `RequirePermission`, form components already established for other content-management admin pages (e.g., Quiz/Dua content editors per A.6/A.8's NextJS blueprints) — mirror that structured-JSON-builder pattern rather than inventing a new one.

## 7. Existing Code to Reuse
- `BaseResourceClient`, `DataTable`, `RequirePermission`, `ConfirmationDialog`.
- Existing structured-JSON criteria-builder component if one already exists from another content-editor admin page (e.g., A.9's mastery criteria builder, if built) — reuse rather than duplicate; confirm before building a new one.

## 8. Files to Create
- `src/features/rewards/badges/BadgeResourceClient.ts`
- `src/features/rewards/badges/AchievementDefinitionResourceClient.ts`
- `src/features/rewards/badges/BadgeManagerPage.tsx`
- `src/features/rewards/badges/BadgeCriteriaBuilderForm.tsx`
- `src/features/rewards/badges/SimulateCriteriaDialog.tsx`
- `src/features/rewards/badges/__tests__/SimulateCriteriaDialog.test.tsx`

## 9. Files to Modify
- Admin route registry — `/rewards/badges`.
- Admin nav/sidebar config.

## 10. Backend Requirements
Consumes B-10 (`/v1/admin/rewards/badges`, `/v1/admin/rewards/achievements`, simulate endpoint).

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- `BadgeManagerPage` lists badges/achievements via `DataTable` with create/edit forms.
- `SimulateCriteriaDialog` clearly labeled "Preview only — no data will be saved," disables any save affordance while displaying simulation results.
- Duplicate-code validation surfaced inline before submission attempt (client-side pre-check ahead of the server's own uniqueness constraint).

## 13. API Contract
Per B-10 §13.

## 14. Database Requirements
N/A (admin frontend).

## 15. Validation
UI test confirming the Simulate dialog's "Run Simulation" action never triggers a create/update network call — only the dedicated simulate endpoint.

## 16. Authentication
Reuses existing Admin session/auth flow.

## 17. Authorization
`RequirePermission` gate for `content_editor`.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Duplicate badge code | Inline field error, submission blocked |
| Malformed criteria JSON | Field-level validation error from the structured builder, not a raw JSON parse error shown to the admin |
| Simulate call failure | Error state within the dialog, does not affect the underlying badge/achievement list |

## 19. Offline First
Not applicable (admin web).

## 20. Local Data
Not applicable.

## 21. Localization
Admin UI localized; `locale_key` field lets content editors specify the child-facing localization key without this page performing translation itself.

## 22. RTL
Form/dialog layout mirrors correctly for Arabic admin locale.

## 23. Analytics
N/A (audit-logged server-side).

## 24. Performance
Criteria builder avoids unnecessary re-renders on large criteria trees; simulate results paginated/virtualized if a large fixture history is used.

## 25. Security
Simulate tool's non-mutating guarantee enforced both server-side (B-10) and client-side (no save affordance ever shown alongside simulation results).

## 26. Library Requirements
Existing Admin Portal stack.

## 27. Testing
- Unit: criteria-builder field validation.
- Integration: CRUD flow, duplicate-code rejection, simulate no-writes UI test (mandatory).

## 28. Documentation
Component README explaining the `criteria_json` builder's supported operators/fields, cross-referenced against B-04/B-10's schema.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement Resource Clients**
- Files to Create: `BadgeResourceClient.ts`, `AchievementDefinitionResourceClient.ts`
- Existing Files to Reuse: `BaseResourceClient`.
- Definition of Done: CRUD methods implemented per B-10's contract.

**Task 02 — Build `BadgeManagerPage` & `BadgeCriteriaBuilderForm`**
- Files to Create: both components.
- Existing Files to Reuse: `DataTable`, `RequirePermission`, existing structured-JSON builder pattern if present.
- Definition of Done: CRUD flow functional, duplicate-code inline validation working.

**Task 03 — Build `SimulateCriteriaDialog`**
- Files to Create: `SimulateCriteriaDialog.tsx`
- Implementation Details: clearly labeled dry-run, no save affordance.
- Tests: no-writes UI test (mandatory).
- Definition of Done: test passing.

**Task 04 — Wire Route, Nav, and Permission Gate**
- Files to Modify: route registry, nav config.
- Definition of Done: `/rewards/badges` reachable only to `content_editor`.

**Task 05 — Documentation & Final Review**
- Documentation: criteria-builder README per §28.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Badge & Achievement Definition Manager live, Simulate tool verifiably non-mutating, RBAC-gated.

## 31. Final Verification Checklist
- [ ] CRUD flow functional for badges and achievement definitions
- [ ] Duplicate badge code rejected with inline error
- [ ] Simulate dialog never triggers a write, clearly labeled as preview-only
- [ ] `RequirePermission` restricts to `content_editor`
- [ ] Localization and RTL verified
- [ ] Criteria-builder documentation complete
