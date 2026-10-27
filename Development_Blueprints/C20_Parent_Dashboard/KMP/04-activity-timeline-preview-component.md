# Blueprint: Activity Timeline Preview Component

## 1. Feature Context
Platform: NoorHeroes KMP App. Module `:feature:parent-dashboard`.

## 2. Parent Feature
C.20 — Parent Dashboard.

## 3. Sub-feature
K-04 — Activity Timeline Preview Component.

## 4. Objective
Render the last 3–5 chronological activity items (story, habit, lesson, reward) as an independently-loading Dashboard component, navigating to full detail within C.22 on tap.

## 5. Business Requirements
Source: PRD §1.7 FR-1, §1.10 Edge Case #1, §1.18 rows 4 & 9, §2.2, §1.19.
- Last 3–5 items, chronological, simple icons per activity type.
- Zero-activity → explicit "Once [Child] starts learning, you'll see their progress here" empty framing, never blank/broken chart.
- Tap item → navigate to relevant detail within C.22 (Per-Child Reports).

## 6. Existing Architecture
Builds on K-01's independent-slice ViewModel/state pattern. Timeline data sourced as part of B-02's aggregated `activity_timeline_preview` field (already fetched by K-01's `getDashboard(childId)` call — this component does not make its own separate API call, it renders a sub-slice of the already-fetched Dashboard payload).

## 7. Existing Code to Reuse
- K-01's `DashboardUiState`/`ParentDashboardViewModel` (extend, don't duplicate the fetch).
- `Navigator` for tap-through to C.22 detail.
- `:core:design-system` list-row/icon primitives.

## 8. Files to Create
- `feature/parent-dashboard/src/commonMain/kotlin/.../ActivityTimelinePreview.kt`
- `feature/parent-dashboard/src/commonTest/kotlin/.../ActivityTimelinePreviewTest.kt`

## 9. Files to Modify
- `DashboardUiState.kt` — add `activityTimelineState: ComponentState<List<ActivityTimelineItem>>` (already partially covered by B-02's response; this task formalizes the client-side slice)

## 10. KMP Requirements
- `ActivityTimelinePreview` Composable: renders up to 5 rows, each with type icon (story/habit/lesson/reward), title, relative/localized timestamp.
- Tap row → `Navigator.navigateTo(PerChildReportRoute(childId))` (C.22, confirmed exact signature `data class PerChildReportRoute(val childId: String) : Route` per C.22 K-01's already-written blueprint) — C.22's Per-Child Report screen is a single aggregated view (trend chart, habit calendar, skill mastery, AI interaction summary) rather than a per-item detail route, so a timeline-item tap navigates to that same screen (optionally with a scroll-to-item hint via a query/anchor parameter if C.22's screen supports one — confirm at C.22 implementation time) rather than a separate `ActivityDetailRoute`, which does not exist in C.22's confirmed route set.
- Empty state: explicit "Once [Child] starts learning, you'll see their progress here" copy (localized), rendered instead of a blank list.
- Independent loading/error slice per K-01's architecture, even though data arrives as part of the same aggregated API response (the ViewModel splits the single response into independent per-component slices at the state-mapping layer, so a malformed/missing `activity_timeline_preview` sub-field doesn't blank other components either).

## 11. Files/Screens
Composable within K-01's `ParentDashboardScreen`.

## 12. NextJS Requirements
N/A.

## 13. API Contract
Consumes the `activity_timeline_preview` field from `GET /v1/parent/dashboard?child_id=` (B-02) — no separate endpoint.

## 14. Database Requirements
N/A new — cached as part of the Dashboard aggregate via K-07.

## 15. Validation
N/A beyond standard null/empty-list handling.

## 16. Authentication
Inherits K-01's Parent Gate.

## 17. Authorization
Inherits K-01's family/child scoping.

## 18. Error Handling
If the `activity_timeline_preview` sub-field is missing/malformed in an otherwise-successful Dashboard response, this component shows its own "may be unavailable right now" placeholder without affecting sibling components (mirrors PRD §1.11 error table row for "Individual component data fetch failure").

## 19. Offline First
Cached as part of the Dashboard aggregate (K-07); renders from cache with staleness indicator when offline.

## 20. Local Data
Room-cached via K-07 as part of the aggregate payload.

## 21. Localization
Activity type labels and relative timestamps localized (`Instant.toLocalizedDateString()`).

## 22. RTL
Row layout (icon, title, timestamp) mirrors correctly.

## 23. Analytics
`activity_timeline_preview_viewed`, `activity_timeline_item_tapped` (PRD §1.19).

## 24. Performance
Lightweight list render (max 5 items) — no pagination needed at preview scope; avoid unnecessary recomposition via stable `ActivityTimelineItem` list.

## 25. Security
No new sensitive data beyond what B-02 already exposes to the authenticated parent for their own family's child.

## 26. Library Requirements
No new dependencies.

## 27. Testing
1. Unit test: renders up to 5 chronological items correctly ordered.
2. Unit test: zero-activity renders explicit empty-state copy, not a blank list.
3. Unit test: tap navigates to correct detail route with correct params.
4. Unit test: malformed/missing sub-field in aggregate response degrades gracefully without blanking siblings.
5. UI test: icons render correctly per activity type.

## 28. Documentation
KDoc citing PRD §1.18 rows 4 & 9, §1.19.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Add Timeline Slice to ViewModel State Mapping**
- Task ID: K04-T01
- Objective: Split aggregate response into independent timeline slice.
- Why This Is Required: Per-component independence guarantee.
- Existing Architecture to Follow: K-01's state-mapping layer.
- Existing Files to Reuse: `ParentDashboardViewModel`.
- Files to Create: none.
- Files to Modify: `DashboardUiState.kt`, `ParentDashboardViewModel.kt`.
- Implementation Details: Per §10.
- Business Rules: FR-1.
- Validation: N/A.
- Error Handling: Graceful degradation on malformed sub-field.
- Security: N/A.
- Performance: N/A.
- Localization: N/A (state only).
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 03.
- Documentation: KDoc.
- Dependencies: K-01.
- Do Not Change: N/A.
- Expected Result: Independent timeline slice available.
- Definition of Done: Matches §10.

**Task 02 — Build ActivityTimelinePreview Composable**
- Task ID: K04-T02
- Objective: Visual rendering including empty state.
- Why This Is Required: UI delivery.
- Existing Architecture to Follow: `:core:design-system` list-row primitives.
- Existing Files to Reuse: List-row/icon components.
- Files to Create: `ActivityTimelinePreview.kt`.
- Files to Modify: `ParentDashboardScreen.kt`.
- Implementation Details: Per §10.
- Business Rules: PRD §1.10 Edge Case #1.
- Validation: N/A.
- Error Handling: Independent placeholder on failure.
- Security: N/A.
- Performance: Stable list model.
- Localization: All copy localized including the empty-state framing sentence.
- RTL: Mirrors correctly.
- Analytics: `activity_timeline_preview_viewed`, `activity_timeline_item_tapped`.
- Tests: Covered in Task 03.
- Documentation: KDoc.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Component renders correctly in all states.
- Definition of Done: Matches PRD §1.18 rows 4 & 9.

**Task 03 — Write Test Suite**
- Task ID: K04-T03
- Objective: Cover §27.
- Why This Is Required: QA coverage.
- Existing Architecture to Follow: Existing test conventions.
- Existing Files to Reuse: Fake repository doubles.
- Files to Create: `ActivityTimelinePreviewTest.kt`.
- Files to Modify: none.
- Implementation Details: 5 cases per §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: N/A.
- Security: N/A.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test KDoc.
- Dependencies: Tasks 01–02.
- Do Not Change: N/A.
- Expected Result: All pass.
- Definition of Done: 100% of §27 green.

## 30. Definition of Done
Timeline renders up to 5 chronological items with correct empty-state and independent-failure handling, tap-through works, analytics fires, all tests green.

## 31. Final Verification Checklist
- [ ] Empty-state copy matches PRD framing, never a blank/broken visual
- [ ] Independent degradation from other components verified
- [ ] Tap-through route confirmed against C.22's actual route naming once available
- [ ] RTL verified
