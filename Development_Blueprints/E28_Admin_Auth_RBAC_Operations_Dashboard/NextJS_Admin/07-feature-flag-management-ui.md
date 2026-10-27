# N-07 — Feature Flag Management UI

## 1. Feature Context
Part of E.28. Screens #8–9 in PRD §1.18. Safety/AI-flagged toggles route to a Maker-Checker proposal (N-05); other flags apply directly for admin+.

## 2. Parent Feature
E.28 — Admin Portal: Authentication, RBAC & Operations Dashboard

## 3. Sub-feature
N-07 — Feature Flag Management UI

## 4. Objective
Build the Feature Flags List and Editor so that safety/AI-classified flag changes are clearly signaled as requiring two-person approval before submission, and route correctly to B-06's dual-path PATCH behavior.

## 5. Business Requirements
- FR-9: safety/AI flags require two-person approval; other flags require standard admin+ access.
- Edge Case 4: reclassification is explicit, never automatic.
- §1.19: `feature_flag_toggled`, `feature_flag_two_person_approval_required_shown`.

## 6. Existing Architecture
New feature module; uses `DataTable`, form primitives, `ConfirmationDialog` already present.

## 7. Existing Code to Reuse
| Component | Location | Reuse For |
|---|---|---|
| `DataTable` | `src/shared/components/` | Flags list |
| `ConfirmationDialog` | `src/shared/components/` | Toggle confirmation, especially the two-person-approval notice |
| `RequirePermission` | `src/shared/components/` | Gate super-admin-only actions (safety/AI flags) |

## 8. Files to Create
- `src/app/(dashboard)/platform/feature-flags/page.tsx`
- `src/app/(dashboard)/platform/feature-flags/[flagId]/page.tsx`
- `src/features/feature-flags/components/feature-flag-list.tsx`
- `src/features/feature-flags/components/feature-flag-editor.tsx`
- `src/features/feature-flags/hooks/use-feature-flags.ts`
- `src/features/feature-flags/hooks/use-update-feature-flag.ts`
- `src/features/feature-flags/api/feature-flags.repository.ts`
- `tests/features/feature-flags/feature-flag-routing.test.tsx`

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `FEATURE_FLAGS.BASE`

## 10. NextJS Requirements
- Flags List: table of flags (key, rollout %, `requires_two_person_approval` badge).
- Flag Editor: rollout %/targeting form; on submit, branch on `requires_two_person_approval` — safety/AI flags show the `feature_flag_two_person_approval_required_shown` notice and result in a pending-proposal state (link to N-05's Approval Queue); other flags apply directly with a standard success confirmation.
- Permission gating: standard admin+ for non-safety flags; `super_admin` enforced (via `RequirePermission`) for safety/AI flag edits.

## 11. API Contract (Consumed)
`GET`/`PATCH /api/v1/admin/feature-flags` (B-06).

## 12. Database Requirements
N/A.

## 13. Validation
Rollout percentage 0–100 client-side validated before submission.

## 14. Authentication
Assumes established session.

## 15. Authorization
`admin+` baseline, `super_admin` for safety/AI flags — enforced both via nav/route gating (N-02) and in-component `RequirePermission`.

## 16. Error Handling
`403 FORBIDDEN` for insufficient role on a safety/AI flag → clear message distinguishing this from a generic error; `404`/`422` standard handling.

## 17. Offline First
N/A.

## 18. Local Data
None persisted.

## 19. Localization
All labels localized, including the two-person-approval notice text.

## 20. RTL
Standard form/table RTL verification.

## 21. Analytics
Fire `feature_flag_toggled`, `feature_flag_two_person_approval_required_shown` at the appropriate submit-branch points.

## 22. Performance
Standard list/form performance; no special concerns given the small expected flag count.

## 23. Security
UI must never allow a non-super-admin to even attempt submitting a safety/AI flag change (gated pre-submission, not just relying on the server's 403) — consistent with "hide, don't show-disabled" where feasible, or clearly disabled with explanation where the flag's classification itself needs to be visible for context.

## 24. Library Requirements
No new libraries.

## 25. Testing
- Unit: both PATCH routing paths reflected correctly in the UI (direct-success vs. pending-approval).
- Unit: safety/AI flag edit gated to super_admin.
- Integration: Edge Case 4 — reclassification requires an explicit, separate action, never a side effect of a normal toggle.

## 26. Documentation
None beyond standard.

## 27. AI Coding Agent Implementation Steps

**Task 01 — Build Feature Flags List**
- Task ID: N-07-T01
- Files to Create: `feature-flag-list.tsx`, `use-feature-flags.ts`, `feature-flags/page.tsx`.
- Dependencies: B-06 GET endpoint.
- Definition of Done: List renders with correct `requires_two_person_approval` badges.

**Task 02 — Build Feature Flag Editor**
- Task ID: N-07-T02
- Files to Create: `feature-flag-editor.tsx`, `[flagId]/page.tsx`.
- Dependencies: Task 01.
- Definition of Done: Editor form functional.

**Task 03 — Implement Dual-Path Submission Handling**
- Task ID: N-07-T03
- Objective: Branch UI response on `requires_two_person_approval`.
- Files to Create: `use-update-feature-flag.ts`.
- Analytics: `feature_flag_toggled`, `feature_flag_two_person_approval_required_shown`.
- Dependencies: Task 02, B-06 PATCH endpoint.
- Definition of Done: Both paths tested and correctly reflected in UI state.

**Task 04 — Permission Gating for Safety/AI Flags**
- Task ID: N-07-T04
- Files to Modify: `feature-flag-editor.tsx`.
- Dependencies: Task 02.
- Definition of Done: Non-super-admin cannot submit a safety/AI flag change from the UI.

**Task 05 — Localization, RTL Pass**
- Task ID: N-07-T05
- Dependencies: Tasks 01–03.
- Definition of Done: All labels localized; RTL verified.

**Task 06 — Full Test Suite**
- Task ID: N-07-T06
- Files to Create: `tests/features/feature-flags/feature-flag-routing.test.tsx`.
- Dependencies: Tasks 01–05.
- Definition of Done: All §25 scenarios green.

## 28. Definition of Done
- Feature Flags List/Editor live, both PATCH routing paths correctly reflected in UI, safety/AI flags gated to super_admin.

## 29. Final Verification Checklist
- [ ] Both direct-apply and pending-approval paths correctly rendered
- [ ] Safety/AI flag edits gated to super_admin in the UI
- [ ] Reclassification is an explicit, separate action (Edge Case 4)
- [ ] `feature_flag_toggled`/`feature_flag_two_person_approval_required_shown` analytics fire correctly
- [ ] RTL layout verified
