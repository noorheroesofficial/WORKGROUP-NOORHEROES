# N-02 — Challenge & Mission Management UI

> **Reconciliation note (2026-08-18):** supersedes `A11_Rewards_System/NextJS_Admin/03-mission-weekly-challenge-scheduler.md` (now deprecated).

## 1. Feature Context
Part of **Feature E.31 — Engagement Tools Admin Suite**. Delivers the Admin Portal screens for daily missions, weekly challenges, and seasonal events, consuming **B-02 Challenge & Mission Management API**. Source: PRD §1.18 Screens 4–6, §2, §6, §7 item 4.

## 2. Parent Feature
Feature E.31 — Engagement Tools Admin Suite

## 3. Sub-feature
3.2 Challenge & Mission Management UI (Admin ID: **N-02**)

## 4. Objective
Give content admins a fast, error-preventing authoring experience for missions/challenges/seasonal events, with an inline client-side date-range-overlap warning shown before submission (fast UX pre-check), while the server's own rejection (B-02) remains authoritative.

## 5. Business Requirements
- Screen Inventory (PRD §1.18): #4 Daily Mission Template Pool, #5 Weekly Challenge Builder, #6 Seasonal Event Scheduler/Challenge Calendar View.
- FR-2 screens/CRUD (PRD §1.7).
- Frontend AI Code-Gen Prompt item 4 (PRD §7): inline overlap warning BEFORE submission.

## 6. Existing Architecture
React + TypeScript, Admin Portal shell from E.28.

## 7. Existing Code to Reuse
E.28's shell/design tokens; E.29's list→editor data-table pattern; shared calendar/date-range-picker component if one already exists in the Admin Portal's component library (reuse rather than reimplement).

## 8. Files to Create
- `app/(admin)/engagement/challenges/page.tsx` (Mission Pool + Challenge List, tabbed)
- `app/(admin)/engagement/challenges/[id]/page.tsx` (Weekly Challenge Builder / Mission Editor)
- `app/(admin)/engagement/challenges/calendar/page.tsx` (Seasonal Event Scheduler / Calendar View)
- `components/engagement/challenges/ChallengeTable.tsx`
- `components/engagement/challenges/ChallengeBuilderForm.tsx`
- `components/engagement/challenges/DateRangeOverlapWarning.tsx`
- `repositories/admin/ChallengeAdminRepository.ts`
- `types/admin/challenge.ts`
- `__tests__/engagement/challenges/DateRangeOverlapWarning.test.tsx`

## 9. Files to Modify
- `components/shell/EngagementNavGroup.tsx`
- `lib/analytics/EngagementAdminAnalytics.ts`

## 10. Backend Requirements
Consumes **B-02** endpoints: `POST/GET/PATCH /v1/admin/challenges`, `POST /v1/admin/challenges/{id}/archive`.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- **Page:** Mission Pool tab, Weekly Challenge Builder, Seasonal Event Scheduler/Calendar.
- **Route:** `/engagement/challenges`, `/engagement/challenges/[id]`, `/engagement/challenges/calendar`.
- **Component:** `ChallengeTable`, `ChallengeBuilderForm` (target/reward/date-range/age-band), `DateRangeOverlapWarning` (client-side pre-check component).
- **API Client:** `ChallengeAdminRepository`.
- **Type Definition:** `Challenge`, `Mission`, `SeasonalEvent`, `ChallengeCreateInput`.
- **Form:** React Hook Form + Zod; `ends_at > starts_at` validated client-side.
- **Validation:** client fetches existing challenges for the selected age_band on date-field blur/change and locally checks for overlap, surfacing `DateRangeOverlapWarning` before submit — this is advisory; the actual submit still round-trips to B-02 for the authoritative check.
- **Authentication/Authorization:** `content_editor`+ gate on mutations.
- **Loading/Empty/Error States:** standard Admin Portal patterns.
- **Pagination/Filtering/Sorting:** by age_band, status, type.
- **Responsive/Accessibility/RTL:** standard.
- **Analytics:** `mission_created`, `weekly_challenge_created`, `seasonal_event_scheduled`.
- **Performance:** debounce the overlap pre-check query; avoid firing it on every keystroke.
- **Testing:** UI test for inline warning (PRD §7 item 4 signature requirement); integration test for full create-with-overlap-rejected flow.

## 13. API Contract
Reuses B-02's contract verbatim (see `Backend/02-challenge-mission-management-api.md` §13).

## 14. Database Requirements
N/A.

## 15. Validation
Client-side: `ends_at > starts_at`, required fields, advisory overlap pre-check. Server-side (B-02) remains authoritative via exclusion-constraint-backed `409`.

## 16. Authentication
Inherits E.28 session.

## 17. Authorization
`content_editor`+ for create/update/archive.

## 18. Error Handling
| Scenario | UI Behavior |
|---|---|
| Server returns `409 DATE_RANGE_OVERLAP` despite passing client pre-check (race condition) | Clear, non-alarming error message explaining another admin just claimed that slot; form retains entered data for adjustment |
| `422 VALIDATION_ERROR` | Inline field errors |
| `422 INVALID_GOAL_TYPE` | Inline error on goal-type selector |
| `403 FORBIDDEN` | Action disabled with role-requirement tooltip |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Challenge title/description via localization-key editor.

## 22. RTL
Full RTL support for content-editing fields and the calendar view's timeline direction.

## 23. Analytics
`mission_created`, `weekly_challenge_created`, `weekly_challenge_overlap_rejected` (client-observed instance of the server rejection), `seasonal_event_scheduled`.

## 24. Performance
Debounced (400ms) overlap pre-check API call; calendar view virtualizes/lazily loads events outside the visible window.

## 25. Security
Client-side overlap check is UX-only — never trusted as the authorization boundary; server's exclusion-constraint-backed `409` remains the sole source of truth, explicitly documented so no future refactor mistakenly treats the client check as sufficient.

## 26. Library Requirements
React, TypeScript, React Hook Form, Zod, a date-range-picker library (reuse Admin Portal's existing one if present), React Query, Jest/RTL.

## 27. Testing
- **UI test:** inline overlap warning appears when selected dates/age-band match an existing challenge, BEFORE submission (PRD §7 item 4 signature test).
- **Integration:** full flow — client pre-check passes (no visible warning) but server still independently validates on submit; and the reverse — client pre-check warns, admin adjusts, submit succeeds.
- **Unit:** form validation logic.

## 28. Documentation
Document the explicit "advisory only, server authoritative" nature of the overlap pre-check for future maintainers.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Types & API Client**
- Task ID: N-02-T01
- Files to Create: `types/admin/challenge.ts`, `repositories/admin/ChallengeAdminRepository.ts`.
- Dependencies: B-02.
- Definition of Done: typed repository, unit-tested against mocked API.

**Task 02 — Challenge/Mission List & Tabs**
- Task ID: N-02-T02
- Files to Create: `app/(admin)/engagement/challenges/page.tsx`, `components/engagement/challenges/ChallengeTable.tsx`.
- Dependencies: Task 01.
- Definition of Done: list renders with pagination/filter/sort/all states.

**Task 03 — Challenge Builder Form with Overlap Pre-Check**
- Task ID: N-02-T03
- Files to Create: `components/engagement/challenges/ChallengeBuilderForm.tsx`, `components/engagement/challenges/DateRangeOverlapWarning.tsx`.
- Implementation Details: debounced client-side overlap query against `GET /v1/admin/challenges?age_band=&overlaps_with=`; render `DateRangeOverlapWarning` inline before submit is enabled/attempted.
- Dependencies: Task 01.
- Definition of Done: UI test for inline warning passes.

**Task 04 — Seasonal Event Scheduler / Calendar View**
- Task ID: N-02-T04
- Files to Create: `app/(admin)/engagement/challenges/calendar/page.tsx`.
- Dependencies: Tasks 01–03.
- Definition of Done: calendar renders scheduled challenges/events correctly.

**Task 05 — Permission Gating & Accessibility**
- Task ID: N-02-T05
- Dependencies: Tasks 02–04.
- Definition of Done: role-gated actions verified; accessibility audit passes.

**Task 06 — Tests & Documentation**
- Task ID: N-02-T06
- Dependencies: Tasks 01–05.
- Definition of Done: §31 checklist verified.

## 30. Definition of Done
List/builder/calendar screens functional against B-02; inline overlap pre-check implemented and tested as advisory-only; server rejection remains authoritative and is gracefully surfaced when it fires despite a clean client pre-check.

## 31. Final Verification Checklist
- [ ] Daily Mission Template Pool screen functional
- [ ] Weekly Challenge Builder validates `ends_at > starts_at` client-side
- [ ] Inline overlap warning shown before submission when dates/age-band match an existing challenge
- [ ] Server `409 DATE_RANGE_OVERLAP` handled gracefully even when client pre-check passed (race condition)
- [ ] Seasonal Event Scheduler / Calendar View renders correctly
- [ ] `content_editor`+ gating enforced
- [ ] Loading/empty/error states implemented
- [ ] Responsive, accessible, RTL-supported
- [ ] Analytics events fire correctly
- [ ] No school/madrasa/institutional-tier logic introduced
