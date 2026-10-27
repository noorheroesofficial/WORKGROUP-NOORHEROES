# N-03 — Laylatul Qadr Content Set Manager

## 1. Feature Context
A filtered, editorially-distinct view of N-02's scheduler scoped to exactly the five Laylatul Qadr nights, enforcing the `is_laylatul_qadr` tag that is the entire database-level mechanism by which K-04's gamification suppression works — a missing tag here is a direct tonal-integrity failure downstream.

## 2. Parent Feature
F.36 — Ramadan Mode

## 3. Sub-feature
3.3 Laylatul Qadr Content Set Manager (ID: **N-03**)

## 4. Objective
Build a filtered scheduler view for nights 21/23/25/27/29 with required `is_laylatul_qadr` tagging enforcement.

## 5. Business Requirements
- §8: Laylatul Qadr Content Set Manager — curate and tag the five special-night content units.
- §9 Admin AI prompt item 3: filtered scheduler view for nights 21/23/25/27/29 with required `is_laylatul_qadr` tagging.
- FR-12: Laylatul Qadr nights deliberately suppress gamification, reliably applied, never dependent on manual editorial memory — this screen is the one place that memory is actually exercised, so its validation must be a hard block, not a suggestion.

## 6. Existing Architecture
`src/features/ramadan/laylatul-qadr-manager/`, built as a filtered composition over N-02's `NightScheduleGrid`/`MissionScheduleResourceClient` — not a separate data layer.

## 7. Existing Code to Reuse
- N-02's `MissionScheduleResourceClient`, `useNightSchedule` (filtered to five nights)
- N-02's `NightSlotAssignmentDialog` (extended with a required tagging checkbox)
- `DataTable`, `RequirePermission`

## 8. Files to Create
- `src/app/(dashboard)/ramadan/laylatul-qadr/page.tsx`
- `src/features/ramadan/laylatul-qadr-manager/components/laylatul-qadr-grid.tsx`
- `src/features/ramadan/laylatul-qadr-manager/components/laylatul-qadr-tag-field.tsx`

## 9. Files to Modify
- `src/shared/components/dashboard-shell.tsx` — add "Laylatul Qadr" nav entry under Ramadan

## 10. NextJS Requirements
- **Page/Route:** `/ramadan/laylatul-qadr`.
- **Component:** `LaylatulQadrGrid` — reuses N-02's grid component, hard-filtered to `night_number IN (21, 23, 25, 27, 29)`, with a visually distinct editorial header signaling the calmer-tone requirement to editors (a UX reminder, not a UI enforcement mechanism).
- **Form/Validation:** `LaylatulQadrTagField` — the `is_laylatul_qadr` checkbox is required and pre-checked/locked `true` for these five slots specifically (an editor cannot accidentally leave it unchecked, since this view exists only for these five nights) — the actual server-side guarantee remains B-03's persisted column read, this UI simply removes the chance of editorial oversight.
- **Loading/Empty/Error State:** consistent with N-02's grid states, scoped to five items.
- **Responsive UI/Accessibility:** consistent with N-02.

## 11. API Contract
Reuses N-02's confirmed content-assignment contract (see N-02 §11 flag), filtered client-side to the five night numbers — no new endpoint.

## 12. Database Requirements
N/A directly — same `ramadan_missions.is_laylatul_qadr` column N-02/B-03 already reference.

## 13. Validation
`is_laylatul_qadr` must be `true` for every assignment made through this view — enforced by the view not offering an unchecked state at all (structural UI guarantee, mirroring K-04's structural client-side guarantee).

## 14. Authentication
Standard Admin Portal session.

## 15. Authorization
`RequirePermission permission="ramadan_content_schedule:write"` — behind `content_editor`, same scope as N-02.

## 16. Error Handling
Consistent with N-02 — per-slot error surfacing on save failure.

## 17. Localization
Editorial guidance text (e.g., a tone reminder banner) and labels via `useTranslation()`.

## 18. RTL
Grid layout direction-aware, consistent with N-02.

## 19. Analytics
Consistent with the Admin Portal's existing action-audit pattern if present.

## 20. Performance
Trivial — five-item dataset, no special performance consideration beyond N-02's baseline.

## 21. Caching
Shares N-02's React Query cache key space (filtered view, same underlying data) — invalidation on save must refresh both this view and N-02's full grid.

## 22. Testing
Component tests: **mandatory** — the tag field never renders an unchecked/false state within this view (structural UI test). Integration test: saving from this view correctly sets `is_laylatul_qadr=true` and the change is reflected in both this filtered view and N-02's full grid.

## 23. Documentation
Inline JSDoc explaining why this view exists separately from N-02 despite sharing its data layer — the editorial-tone reminder and the tagging-guarantee UX are the entire justification.

## 24. AI Coding Agent Implementation Steps

**Task 01 — Build `LaylatulQadrGrid` as a Filtered N-02 Composition**
Objective: Reuse N-02's grid, hard-filtered to five nights. Files to Create: `components/laylatul-qadr-grid.tsx`. Dependencies: N-02 complete. Tests: filter-correctness test. Definition of Done: test passes.

**Task 02 — Build `LaylatulQadrTagField`**
Objective: Locked-true tagging field, no unchecked state offered. Files to Create: `components/laylatul-qadr-tag-field.tsx`. Dependencies: Task 01. Tests: **mandatory** — no-unchecked-state structural test. Definition of Done: test passes.

**Task 03 — Build the Page with Editorial Guidance Banner**
Objective: `/ramadan/laylatul-qadr` page with tone-reminder banner. Files to Create: `app/(dashboard)/ramadan/laylatul-qadr/page.tsx`. Files to Modify: `dashboard-shell.tsx`. Dependencies: Task 01, Task 02. Tests: page integration test. Definition of Done: test passes.

**Task 04 — Verify Cross-View Cache Invalidation**
Objective: Save here correctly refreshes N-02's grid too. Dependencies: Task 03. Tests: cross-invalidation test. Definition of Done: test passes.

**Task 05 — Add Localization and Full Test Suite**
Objective: Complete §17/§22 coverage, mandatory test included. Definition of Done: all green in CI.

**Task 06 — Final Code Review**
Objective: Confirm no code path in this view can produce an `is_laylatul_qadr=false` save. Definition of Done: checklist in §26 checked.

## 25. Definition of Done
The five most tonally sensitive nights of the season are scheduled through a view that makes correct tagging structurally unavoidable, closing the exact gap FR-12 warns against.

## 26. Final Verification Checklist
- [ ] Tag field never offers an unchecked state within this view — mandatory test passing
- [ ] Save correctly reflected in both this view and N-02's full grid
- [ ] Editorial tone-reminder banner present and localized
