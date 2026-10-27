# N-11 — Seasonal Calendar Coordination View

## 1. Feature Context
Part of **Feature E.31 — Engagement Tools Admin Suite**. Delivers the shared, cross-module Seasonal Calendar — the Engagement navigation group's landing screen — consuming **B-11**. Source: PRD §1.18 Screen 29, §1.17 (Mermaid flow), §2.1 (Seasonal Calendar View), §2.5 (screen image prompts), §6.3.

## 2. Parent Feature
Feature E.31 — Engagement Tools Admin Suite

## 3. Sub-feature
3.11 Seasonal Calendar Coordination View (Admin ID: **N-11**)

## 4. Objective
Give super admins and content admins a single, color-coded, cross-mechanic timeline view for coordinating seasonal launches (e.g., Ramadan), while making unmistakably clear in the UI that this view is a scheduling convenience only — every underlying mechanic's own validation still applies independently when the admin drills into its editor.

## 5. Business Requirements
- Screen Inventory (PRD §1.18): #29 Seasonal Calendar (cross-mechanic coordination view) — Engagement navigation group landing screen, links out to each module's own editor.
- User Flow (PRD §1.16): "for a coordinated seasonal event, the admin uses the shared seasonal calendar view to schedule multiple mechanics together, while each mechanic's own independent validation still applies."
- UX spec (PRD §2.1): shared, cross-module calendar visualization showing scheduled habit sets, challenges, banners, and notification campaigns on one timeline, color-coded by mechanic type.

## 6. Existing Architecture
React + TypeScript, Admin Portal shell from E.28. This is the Engagement navigation group's landing route (PRD §6.3).

## 7. Existing Code to Reuse
E.28 shell/design tokens; a timeline/calendar visualization library already used elsewhere in the Admin Portal, if one exists (reuse rather than introduce a second charting/calendar dependency).

## 8. Files to Create
- `app/(admin)/engagement/page.tsx` (landing route → Seasonal Calendar)
- `components/engagement/calendar/SeasonalCalendarTimeline.tsx`
- `components/engagement/calendar/MechanicTypeLegend.tsx`
- `repositories/admin/SeasonalCalendarAdminRepository.ts`
- `types/admin/seasonalCalendar.ts`
- `__tests__/engagement/calendar/SeasonalCalendarTimeline.test.tsx`

## 9. Files to Modify
- `components/shell/EngagementNavGroup.tsx` (landing route wiring)

## 10. Backend Requirements
Consumes **B-11**: `GET /v1/admin/seasonal-calendar`.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- **Page:** Seasonal Calendar (Engagement group landing route).
- **Route:** `/engagement` (redirects/renders as the calendar view).
- **Component:** `SeasonalCalendarTimeline` (horizontal timeline, rows per mechanic type: Habits, Challenges, Banners, Notifications; color-coded blocks; highlighted seasonal-window shading, e.g., soft gold for a "Ramadan Window" per PRD §2.5), `MechanicTypeLegend`.
- **API Client:** `SeasonalCalendarAdminRepository`.
- **Type Definition:** `SeasonalCalendarItem`, `SeasonalCalendarWindow`.
- **Interaction:** clicking a timeline block navigates to that item's own editor (N-01 through N-10 respectively) — the calendar view itself has no create/edit affordance of its own, only navigation.
- **Authentication/Authorization:** readable by any Engagement-module-visible role; navigation into a specific mechanic's editor still gated by that mechanic's own role requirement (e.g., clicking through to a Manual Grant Tool block, if ever surfaced here, still requires `support`/`billing_ops`).
- **Loading/Empty/Error States:** standard; empty state: "Nothing scheduled in this window yet."
- **Pagination/Filtering/Sorting:** window navigation (previous/next period), filter by mechanic type.
- **Responsive/Accessibility/RTL:** timeline must remain legible and horizontally scrollable on narrow viewports; full RTL mirroring of the timeline direction for Arabic/Urdu locales.
- **Analytics:** view-level analytics for calendar usage (screen view event).
- **Performance:** virtualized/windowed rendering if the date range is large; lazy-load items outside the visible window.
- **Testing:** UI test confirming the calendar renders color-coded blocks per mechanic type and correctly links each block to its owning module's editor.

## 13. API Contract
Reuses B-11's contract verbatim (see `Backend/11-seasonal-cross-mechanic-coordination-api.md` §13).

## 14. Database Requirements
N/A.

## 15. Validation
Window `starts_at < ends_at` validated on the date-range picker controlling the visible calendar period.

## 16. Authentication
Inherits E.28 session.

## 17. Authorization
Read access per E.28's role-scoped sidebar pattern (PRD §2.3); this view itself performs no mutations, so it has no `content_editor`+ gate of its own — only navigation targets inherit their own respective gates.

## 18. Error Handling
| Scenario | UI Behavior |
|---|---|
| API failure loading the calendar window | Error state with retry affordance |
| Empty window | "Nothing scheduled in this window yet" empty state |
| Navigating to a block whose target editor requires a role the admin lacks | Standard forbidden-state handling in the target editor (not this view's responsibility) |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Item titles resolve through each underlying mechanic's own localization keys; calendar chrome (month/week labels, legend) localized per Admin Portal locale support.

## 22. RTL
Full RTL mirroring of the timeline's horizontal direction for Arabic/Urdu, per PRD §2.5's explicit Arabic RTL wireframe prompt for this exact screen.

## 23. Analytics
Screen-view analytics for the Seasonal Calendar (landing-page view event); no dedicated engagement-mechanic-specific events originate from this view itself (those fire from each mechanic's own create/update actions, per N-01–N-10).

## 24. Performance
Windowed/virtualized rendering for large date ranges; debounced window-navigation requests.

## 25. Security
This view introduces no new mutation surface; its sole responsibility is correct, honest visualization of what B-11 aggregates — it must never present a "schedule everything at once" affordance that could imply a bypass of individual mechanics' validation (consistent with B-11's non-bypass guarantee).

## 26. Library Requirements
React, TypeScript, a timeline/calendar visualization library (reuse existing Admin Portal dependency if present, else a lightweight addition), React Query, Jest/RTL.

## 27. Testing
- **UI test:** color-coded blocks render per mechanic type with correct legend mapping.
- **UI test:** clicking a block navigates to the correct owning module's editor route.
- **Integration:** full render against a seeded multi-mechanic fixture window (mirrors B-11's own integration test).

## 28. Documentation
Document that this view is intentionally read-only/navigation-only by design, referencing B-11's explicit non-bypass guarantee, so a future feature request to "add inline editing to the calendar" is evaluated against that constraint rather than casually implemented.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Types & API Client**
- Task ID: N-11-T01
- Files to Create: `types/admin/seasonalCalendar.ts`, `repositories/admin/SeasonalCalendarAdminRepository.ts`.
- Dependencies: B-11.
- Definition of Done: typed repository unit-tested.

**Task 02 — Seasonal Calendar Timeline Component**
- Task ID: N-11-T02
- Files to Create: `components/engagement/calendar/SeasonalCalendarTimeline.tsx`, `components/engagement/calendar/MechanicTypeLegend.tsx`.
- Implementation Details: color-coded rows per mechanic type; seasonal-window highlight shading.
- Dependencies: Task 01.
- Definition of Done: renders correctly against a seeded fixture window.

**Task 03 — Landing Route Wiring & Navigation-Out Links**
- Task ID: N-11-T03
- Files to Create: `app/(admin)/engagement/page.tsx`.
- Files to Modify: `components/shell/EngagementNavGroup.tsx`.
- Implementation Details: each block links to N-01 through N-10's respective editor routes.
- Dependencies: Task 02, N-01 through N-10 route definitions.
- Definition of Done: navigation-target test passes for each mechanic type.

**Task 04 — Accessibility & RTL Pass**
- Task ID: N-11-T04
- Dependencies: Task 02.
- Definition of Done: accessibility audit passes; RTL rendering verified.

**Task 05 — Tests & Documentation**
- Task ID: N-11-T05
- Dependencies: Tasks 01–04.
- Definition of Done: §31 checklist verified.

## 30. Definition of Done
Seasonal Calendar landing view functional against B-11, correctly color-coded and navigable into each of the ten mechanic-specific editors, with no mutation affordance of its own.

## 31. Final Verification Checklist
- [ ] Calendar renders color-coded blocks per mechanic type (Habits, Challenges, Banners, Notifications, etc.)
- [ ] Seasonal-window highlight shading renders correctly
- [ ] Each block navigates to the correct owning module's editor (N-01–N-10)
- [ ] View performs no mutations of its own
- [ ] Empty/error states implemented
- [ ] Responsive, accessible, RTL-supported
- [ ] Set as the Engagement navigation group's landing route
- [ ] No school/madrasa/institutional-tier logic introduced
