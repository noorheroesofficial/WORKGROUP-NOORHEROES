# N-03 — Mission & Weekly Challenge Scheduler

> **⚠ DEPRECATED — superseded by `E31_Engagement_Tools_Admin_Suite/NextJS_Admin/02-challenge-mission-management-ui.md`.** Backend counterpart B-11 is likewise deprecated in favor of E.31 B-02. Do not implement this file — implement E.31's Challenge & Mission Management UI instead. Retained for historical/design-rationale reference only.

## 1. Feature Context
Part of Feature A.11 — Rewards System. Admin scheduling interface for Daily/Weekly/Seasonal missions, with automatic archive-status display (no manual archive action).

## 2. Parent Feature
A.11 Rewards System — NextJS Admin

## 3. Sub-feature
N-03 Mission & Weekly Challenge Scheduler

## 4. Objective
Build the Mission & Weekly Challenge Scheduler page consuming B-11, restricted to `content_editor`, per PRD §8/§9.

## 5. Business Requirements
- CRUD for `missions` (type: daily/weekly/seasonal, `eligibility_json`, `criteria_json`, `reward_json`, `starts_at`, `ends_at`).
- Expired missions automatically display an "Archived" status pill based on `ends_at` — no manual "archive" action/button exists anywhere on this page.
- Restricted to `content_editor` role.

## 6. Existing Architecture
Existing Admin Portal shell; reuses `DataTable` with a `StatusBadge` component for the computed active/scheduled/archived pill (per `NEXT-JS-INSTRUCTIONS.md`'s existing `StatusBadge` component).

## 7. Existing Code to Reuse
- `BaseResourceClient`, `DataTable`, `StatusBadge`, `RequirePermission`, `ConfirmationDialog`.
- Existing date/time picker component if already used elsewhere in the Admin Portal for scheduling (reuse, don't introduce a new one).

## 8. Files to Create
- `src/features/rewards/missions/MissionResourceClient.ts`
- `src/features/rewards/missions/MissionSchedulerPage.tsx`
- `src/features/rewards/missions/MissionScheduleForm.tsx`
- `src/features/rewards/missions/__tests__/MissionSchedulerPage.test.tsx`

## 9. Files to Modify
- Admin route registry — `/rewards/missions`.
- Admin nav/sidebar config.

## 10. Backend Requirements
Consumes B-11 (`/v1/admin/rewards/missions`).

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- `MissionSchedulerPage` renders `status` (active/scheduled/archived) via `StatusBadge`, sourced directly from the API's computed field — never a client-side-toggled value.
- `MissionScheduleForm` validates `starts_at < ends_at` client-side, ahead of the server's own validation.
- No "Archive" button/action exists anywhere in this UI, matching B-11's structural guarantee.

## 13. API Contract
Per B-11 §13.

## 14. Database Requirements
N/A (admin frontend).

## 15. Validation
UI test confirming no archive/delete action element exists on this page for any mission row, regardless of its status.

## 16. Authentication
Reuses existing Admin session/auth flow.

## 17. Authorization
`RequirePermission` gate for `content_editor`.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| `starts_at >= ends_at` submitted | Inline validation error, submission blocked |
| Overlapping daily-mission schedule | Inline conflict error surfaced from the server's `422` response |
| Fetch failure | `ErrorView` with retry |
| Empty mission list | `EmptyState` with "schedule your first mission" call to action |

## 19. Offline First
Not applicable (admin web).

## 20. Local Data
Not applicable.

## 21. Localization
Admin UI localized; mission title/description fields captured per the platform's multilingual content-authoring convention (consistent with other content-editor admin pages).

## 22. RTL
Table/form layout mirrors correctly for Arabic admin locale.

## 23. Analytics
N/A (audit-logged server-side).

## 24. Performance
`DataTable` pagination/filtering by type and status for large mission catalogs.

## 25. Security
Structural absence of a manual archive/delete action prevents accidental loss of historical mission data relied upon by the child-facing archive-not-disappear guarantee (B-05).

## 26. Library Requirements
Existing Admin Portal stack.

## 27. Testing
- Unit: schedule-validation logic.
- Integration: full CRUD flow, permission-gated rendering, no-archive-action UI test (mandatory).

## 28. Documentation
Component README noting archive status is always computed, never a settable field, cross-referenced against B-11.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement `MissionResourceClient`**
- Files to Create: `MissionResourceClient.ts`
- Existing Files to Reuse: `BaseResourceClient`.
- Definition of Done: CRUD methods implemented per B-11's contract.

**Task 02 — Build `MissionSchedulerPage`**
- Files to Create: `MissionSchedulerPage.tsx`
- Existing Files to Reuse: `DataTable`, `StatusBadge`, `RequirePermission`.
- Definition of Done: status pill correctly reflects server-computed value.

**Task 03 — Build `MissionScheduleForm`**
- Files to Create: `MissionScheduleForm.tsx`
- Implementation Details: client-side `starts_at < ends_at` validation.
- Tests: no-archive-action UI test (mandatory).
- Definition of Done: test passing.

**Task 04 — Wire Route, Nav, and Permission Gate**
- Files to Modify: route registry, nav config.
- Definition of Done: `/rewards/missions` reachable only to `content_editor`.

**Task 05 — Documentation & Final Review**
- Documentation: README per §28.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Mission Scheduler live, archive status always server-computed, RBAC-gated, no manual archive action present.

## 31. Final Verification Checklist
- [ ] Status pill always sourced from server-computed field, never client-toggled
- [ ] No archive/delete action exists on this page
- [ ] Schedule validation (`starts_at < ends_at`, no overlap) enforced client- and server-side
- [ ] `RequirePermission` restricts to `content_editor`
- [ ] Empty/loading/error states render correctly
- [ ] Localization and RTL verified
