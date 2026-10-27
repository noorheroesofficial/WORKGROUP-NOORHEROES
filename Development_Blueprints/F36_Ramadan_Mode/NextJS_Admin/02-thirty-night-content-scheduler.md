# N-02 — Thirty-Night Content Scheduler

## 1. Feature Context
The editorial scheduling grid that assigns each of the 30 Ramadan nights to a piece of E.29-authored, scholar-reviewed content — the operational tool behind the PRD's single hardest deadline (100% scholar approval 3 weeks before Ramadan), while deliberately never becoming a second content editor.

## 2. Parent Feature
F.36 — Ramadan Mode

## 3. Sub-feature
3.2 Thirty-Night Content Scheduler (ID: **N-02**)

## 4. Objective
Build a 30-slot scheduling grid assigning existing E.29-authored content to each Ramadan night, linking out to E.29's editor for authoring rather than reimplementing it.

## 5. Business Requirements
- §8: 30-Night Content Scheduler — schedule each night's content assignment, reusing E.29's CMS for authoring/review.
- §9 Admin AI prompt item 2: assigns existing E.29-authored content to each of 30 night slots; links out to E.29's editor for authoring, never reimplementing it.
- §1.8: content-completeness deadline — all 30 nights' content must be scholar-approved at least 3 weeks before the actual Ramadan start date.

## 6. Existing Architecture
`src/features/ramadan/content-scheduler/`, reusing E.29's existing `CmsRepositoryImpl`/`useCmsArticles` pattern for content lookup/selection (per `NEXT-JS-INSTRUCTIONS.md` §3) rather than building a parallel content query layer.

## 7. Existing Code to Reuse
- E.29's `CmsRepositoryImpl` / `useCmsArticles` (content lookup for the assignment picker)
- `DataTable`, `RequirePermission`, `LoadingState`, `EmptyState`, `ErrorView`
- E.29's content-editor route (external link target, not embedded)

## 8. Files to Create
- `src/app/(dashboard)/ramadan/content-scheduler/page.tsx`
- `src/features/ramadan/content-scheduler/api/mission-schedule-resource-client.ts`
- `src/features/ramadan/content-scheduler/hooks/use-night-schedule.ts`
- `src/features/ramadan/content-scheduler/components/night-schedule-grid.tsx`
- `src/features/ramadan/content-scheduler/components/night-slot-assignment-dialog.tsx`
- `src/features/ramadan/content-scheduler/types/mission-schedule.ts`

## 9. Files to Modify
- `src/shared/components/dashboard-shell.tsx` — add "30-Night Scheduler" nav entry under Ramadan

## 10. NextJS Requirements
- **Page/Route:** `/ramadan/content-scheduler`.
- **Component:** `NightScheduleGrid` (30-slot grid, one card per night, status-colored by scholar-approval state sourced from E.29's review-queue); `NightSlotAssignmentDialog` (content picker reusing E.29's `useCmsArticles`, with an explicit "Edit in CMS" link out to E.29's editor rather than an inline editor).
- **API Client/Type Definition:** `MissionScheduleResourceClient` for `ramadan_missions`' night-to-content mapping; reuses E.29's existing content-list types for the picker, does not redefine them.
- **Form/Validation:** assignment form rejects selecting a `content_version_id` that is not scholar-approved for a night within the deadline window — cross-checked against E.29's review-status field.
- **Loading/Empty/Error State:** grid-level loading skeleton; empty slot styling distinct from assigned-but-unapproved styling.
- **Search/Filter/Sort:** filter grid by approval status (approved / pending / unassigned).
- **Responsive UI:** 30-card grid reflows for tablet/mobile admin usage.
- **Accessibility:** grid cards keyboard-navigable, status conveyed by icon+text, not color alone.

## 11. API Contract
**Flagged, do not guess:** content-assignment endpoints (mapping E.29 content to a Ramadan night) are not enumerated in PRD §3.4 as a distinct contract — confirm against E.29's actual CMS API surface and/or `ramadan_missions`' backend CRUD (also not explicitly enumerated, see B-03's §11) before implementation.

## 12. Database Requirements
N/A directly — reads/writes `ramadan_missions` and reads E.29's `content_items`/`content_versions` via their respective backend APIs only.

## 13. Validation
Assignment blocked for unapproved content within 3 weeks of the region's earliest Hijri start date — surfaced as a form-level warning, with the actual hard-block enforcement living server-side (do not assume this client-side check is the security boundary).

## 14. Authentication
Standard Admin Portal session.

## 15. Authorization
`RequirePermission permission="ramadan_content_schedule:write"` — behind `content_editor` per §8.

## 16. Error Handling
`QueryErrorState` for grid-fetch failures; assignment-save failure surfaces a clear per-slot error without discarding the rest of the grid's state.

## 17. Localization
Grid labels, status text, and dialog copy via `useTranslation()`.

## 18. RTL
Grid layout and status iconography direction-aware.

## 19. Analytics
Consistent with the Admin Portal's existing action-audit pattern if present (see N-01 §19 note) — not explicitly enumerated in PRD §1.19 for admin actions.

## 20. Performance
30-card grid renders without per-card network waterfalls — batch-fetch schedule + approval status in one query; picker dialog's content search is debounced via `useDebouncedValue`.

## 21. Caching
React Query caching for the schedule grid, invalidated on any successful assignment save.

## 22. Testing
Component tests: grid renders correct status styling per approval state; assignment dialog rejects an unapproved selection within the deadline window. Integration tests: full assign-content-to-night flow reflects correctly in B-03's mission-delivery endpoint on next fetch.

## 23. Documentation
Inline JSDoc noting this component must never embed a content editor — all authoring happens in E.29's existing CMS, reached only via the "Edit in CMS" link.

## 24. AI Coding Agent Implementation Steps

**Task 01 — Confirm the Content-Assignment API Contract**
Objective: Resolve the flagged gap in §11. Definition of Done: contract documented before Task 03.

**Task 02 — Define Types**
Objective: `MissionSchedule`, `NightSlot`. Files to Create: `types/mission-schedule.ts`. Definition of Done: types compile.

**Task 03 — Implement `MissionScheduleResourceClient`**
Objective: CRUD for night-to-content assignment. Files to Create: `api/mission-schedule-resource-client.ts`. Dependencies: Task 01, Task 02. Tests: repository unit tests. Definition of Done: tests pass.

**Task 04 — Implement `useNightSchedule` Hook**
Objective: React Query hook combining `ramadan_missions` schedule with E.29's approval status. Files to Create: `hooks/use-night-schedule.ts`. Dependencies: Task 03. Tests: hook tests. Definition of Done: tests pass.

**Task 05 — Build `NightScheduleGrid`**
Objective: 30-card status-colored grid with filtering. Files to Create: `components/night-schedule-grid.tsx`. Dependencies: Task 04. Tests: status-rendering tests. Definition of Done: tests pass.

**Task 06 — Build `NightSlotAssignmentDialog` Reusing E.29's Content Picker**
Objective: Content selection with "Edit in CMS" link-out, unapproved-content warning. Files to Create: `components/night-slot-assignment-dialog.tsx`. Existing Files to Reuse: E.29's `useCmsArticles`. Dependencies: Task 04. Tests: unapproved-selection-warning test. Definition of Done: test passes.

**Task 07 — Build the Page and Wire Navigation**
Objective: `/ramadan/content-scheduler` page. Files to Create: `app/(dashboard)/ramadan/content-scheduler/page.tsx`. Files to Modify: `dashboard-shell.tsx`. Dependencies: Task 05, Task 06. Tests: page integration test. Definition of Done: test passes.

**Task 08 — Add Localization, Accessibility, and Full Test Suite**
Objective: Complete §17/§22 coverage. Definition of Done: all green in CI.

**Task 09 — Final Code Review**
Objective: Confirm zero inline content-editing capability exists in this module — authoring only happens via the E.29 link-out. Definition of Done: checklist in §26 checked.

## 25. Definition of Done
Editors can schedule all 30 nights against E.29's existing content pipeline with clear, deadline-aware approval-status visibility, and zero duplicated authoring surface.

## 26. Final Verification Checklist
- [ ] Content-assignment API contract confirmed, not guessed, before implementation
- [ ] Grid correctly reflects E.29's live approval status per night
- [ ] Zero inline content-editing UI — all authoring reached via link-out to E.29
- [ ] Unapproved-content assignment warned client-side, blocked server-side
