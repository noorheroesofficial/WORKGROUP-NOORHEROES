# N-08 — App Configuration Editor

## 1. Feature Context
Part of E.28. Screen #19 in PRD §1.18. Production-target changes route to a Maker-Checker proposal (N-05); non-production changes apply directly for admin+.

## 2. Parent Feature
E.28 — Admin Portal: Authentication, RBAC & Operations Dashboard

## 3. Sub-feature
N-08 — App Configuration Editor

## 4. Objective
Build the App Configuration Editor (force-update, trial length, environment-scoped defaults) so production changes are clearly signaled as requiring maker-checker approval, matching B-07's server-side routing.

## 5. Business Requirements
- FR-13: production config changes require maker-checker; non-production may apply directly for admin+.
- Acceptance Criteria: identical change proposed against production requires approval; against non-production does not.

## 6. Existing Architecture
New feature module, structurally near-identical to N-07 (same dual-path submission pattern, different trigger condition).

## 7. Existing Code to Reuse
| Component | Location | Reuse For |
|---|---|---|
| `DataTable` | `src/shared/components/` | Config list, grouped by environment |
| `ConfirmationDialog` | `src/shared/components/` | Save confirmation, production-approval notice |
| `RequirePermission` | `src/shared/components/` | admin+ gating |

## 8. Files to Create
- `src/app/(dashboard)/platform/config/page.tsx`
- `src/features/app-config/components/app-config-editor.tsx`
- `src/features/app-config/hooks/use-app-config.ts`
- `src/features/app-config/hooks/use-update-app-config.ts`
- `src/features/app-config/api/app-config.repository.ts`
- `tests/features/app-config/app-config-routing.test.tsx`

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `APP_CONFIG.BASE`

## 10. NextJS Requirements
- Editor grouped/filterable by environment; production-environment edits show an explicit "This change requires approval" notice before submission.
- On submit, branch on the server's response (`200` direct apply vs. `202` pending-approval) and reflect the correct confirmation state.

## 11. API Contract (Consumed)
`GET`/`PATCH /api/v1/admin/config` (B-07).

## 12. Database Requirements
N/A.

## 13. Validation
Value type validated client-side per config key's expected shape before submission.

## 14. Authentication
Assumes established session.

## 15. Authorization
`admin+`.

## 16. Error Handling
`404 CONFIG_NOT_FOUND`, `422` invalid value — standard handling.

## 17. Offline First
N/A.

## 18. Local Data
None persisted.

## 19. Localization
All labels localized.

## 20. RTL
Standard form/table RTL verification.

## 21. Analytics
Fire `app_config_change_proposed` (production path), `app_config_change_applied` (non-production path).

## 22. Performance
Small, infrequently-changed config set — no special performance concerns.

## 23. Security
Environment is always resolved from the server's stored config record for routing purposes — the UI must never attempt to locally determine or override which path a save will take; it reflects whatever the server response indicates.

## 24. Library Requirements
No new libraries.

## 25. Testing
- Unit: production vs. non-production submission branching correctly reflected in UI state.
- Integration: both paths end-to-end.

## 26. Documentation
None beyond standard.

## 27. AI Coding Agent Implementation Steps

**Task 01 — Build App Configuration List/Editor**
- Task ID: N-08-T01
- Files to Create: `app-config-editor.tsx`, `use-app-config.ts`, `config/page.tsx`.
- Dependencies: B-07 GET endpoint.
- Definition of Done: Editor renders, grouped by environment.

**Task 02 — Implement Dual-Path Submission Handling**
- Task ID: N-08-T02
- Files to Create: `use-update-app-config.ts`.
- Analytics: `app_config_change_proposed`, `app_config_change_applied`.
- Dependencies: Task 01, B-07 PATCH endpoint.
- Definition of Done: Both paths tested and correctly reflected in UI.

**Task 03 — Production-Change Approval Notice**
- Task ID: N-08-T03
- Objective: Explicit "requires approval" messaging before submitting a production change.
- Files to Modify: `app-config-editor.tsx`.
- Dependencies: Task 01.
- Definition of Done: Notice renders for production-targeted edits only.

**Task 04 — Localization, RTL Pass**
- Task ID: N-08-T04
- Dependencies: Tasks 01–02.
- Definition of Done: All labels localized; RTL verified.

**Task 05 — Full Test Suite**
- Task ID: N-08-T05
- Files to Create: `tests/features/app-config/app-config-routing.test.tsx`.
- Dependencies: Tasks 01–04.
- Definition of Done: All §25 scenarios green.

## 28. Definition of Done
- App Configuration Editor live, both PATCH routing paths correctly reflected, admin+-gated.

## 29. Final Verification Checklist
- [ ] Production changes show the "requires approval" notice
- [ ] Both direct-apply and pending-approval paths correctly rendered
- [ ] `app_config_change_proposed`/`_applied` analytics fire correctly
- [ ] Environment routing always reflects the server's determination, never client-side guessed
- [ ] RTL layout verified
