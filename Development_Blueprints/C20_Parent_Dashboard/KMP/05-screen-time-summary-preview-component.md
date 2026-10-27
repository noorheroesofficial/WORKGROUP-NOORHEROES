# Blueprint: Screen-Time Summary Preview Component

## 1. Feature Context
Platform: NoorHeroes KMP App. Module `:feature:parent-dashboard`.

## 2. Parent Feature
C.20 — Parent Dashboard.

## 3. Sub-feature
K-05 — Screen-Time Summary Preview Component.

## 4. Objective
Render a calm, non-judgmental healthy-usage/screen-time status summary, navigating to full Screen Time & Bedtime Settings (C.23) on tap.

## 5. Business Requirements
Source: PRD §1.7 FR-1, FR-9, §1.18 row 5, §2.1, §2.2.
- Trend-oriented, non-judgmental copy (e.g., "Healthy balance this week" per PRD §2.5 image prompt).
- Tap → full Screen Time & Bedtime Settings (C.23).

## 6. Existing Architecture
Data sourced as part of B-02's aggregated `screen_time_summary` field (Restriction Engine, C.23, is B-02's upstream data source) — same "split from single aggregate response" pattern as K-04.

## 7. Existing Code to Reuse
- K-01's `DashboardUiState`/`ParentDashboardViewModel` state-mapping layer.
- `Navigator` for tap-through to `:feature:parental-controls` (C.23).
- `:core:design-system` progress-bar/status-badge primitives.

## 8. Files to Create
- `feature/parent-dashboard/src/commonMain/kotlin/.../ScreenTimeSummaryCard.kt`
- `feature/parent-dashboard/src/commonTest/kotlin/.../ScreenTimeSummaryCardTest.kt`

## 9. Files to Modify
- `DashboardUiState.kt` — add `screenTimeState: ComponentState<ScreenTimeSummary>`

## 10. KMP Requirements
- `ScreenTimeSummaryCard` Composable: simple horizontal usage bar + calm status label (e.g., "Healthy balance this week"), never alarming/red-flag styling per FR-9's trend-oriented, non-judgmental requirement.
- Tap → `Navigator.navigateTo(ControlsLandingRoute)` (C.23 — **confirmed exact route name** from C.23 K-01's already-written blueprint: `data object ControlsLandingRoute : Route` in `feature/parental-controls/.../navigation/ControlsRoutes.kt`, `requiredAuthState = BaseAuthState.Parent::class`, reached explicitly "from C.20's Parent Dashboard module shortcut grid via `navigator.navigateTo(ControlsLandingRoute)`" per that blueprint's own text).
- Fires `screen_time_summary_viewed` on render, `module_shortcut_tapped(module="screen_time")` on tap (PRD §2.3 click-mapping table treats this tap as a module-shortcut event, not a separate event name).
- Independent loading/error slice.

## 11. Files/Screens
Composable within K-01's `ParentDashboardScreen`.

## 12. NextJS Requirements
N/A.

## 13. API Contract
Consumes `screen_time_summary` field from `GET /v1/parent/dashboard?child_id=` (B-02) — no separate endpoint.

## 14. Database Requirements
N/A new — cached as part of the Dashboard aggregate via K-07.

## 15. Validation
N/A beyond standard null handling.

## 16. Authentication
Inherits K-01's Parent Gate.

## 17. Authorization
Inherits K-01's family/child scoping.

## 18. Error Handling
Independent "may be unavailable right now" placeholder on sub-field failure, per K-01's per-component independence principle.

## 19. Offline First
Cached as part of the Dashboard aggregate (K-07).

## 20. Local Data
Room-cached via K-07.

## 21. Localization
Status label and any usage-bar copy fully localized — no hardcoded "Healthy balance this week" string; sourced as a copy key resolved via the localization package (server may supply the specific trend phrase, or the client selects from a localized template set based on a status enum returned by the API — confirm exact mechanism against B-02's final response shape).

## 22. RTL
Usage bar direction and status label alignment mirror correctly in RTL.

## 23. Analytics
`screen_time_summary_viewed`, `module_shortcut_tapped` with `module: screen_time` (PRD §1.19, §2.3).

## 24. Performance
Lightweight — single bar + label, no chart library needed.

## 25. Security
No new sensitive data beyond what B-02/C.23 already expose to the authenticated parent.

## 26. Library Requirements
No new dependencies.

## 27. Testing
1. Unit test: renders usage bar + status label correctly.
2. Unit test: tap navigates to C.23 route.
3. Unit test: independent failure isolation from sibling components.
4. UI test: never renders alarming/red-flag styling (visual regression or explicit color-token assertion against the design-system's calm palette).

## 28. Documentation
KDoc citing PRD §1.18 row 5, FR-9.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Add Screen-Time Slice to ViewModel State Mapping**
- Task ID: K05-T01
- Objective: Split aggregate response into independent screen-time slice.
- Why This Is Required: Per-component independence guarantee.
- Existing Architecture to Follow: K-01's state-mapping layer.
- Existing Files to Reuse: `ParentDashboardViewModel`.
- Files to Create: none.
- Files to Modify: `DashboardUiState.kt`, `ParentDashboardViewModel.kt`.
- Implementation Details: Per §10.
- Business Rules: FR-1.
- Validation: N/A.
- Error Handling: Graceful degradation.
- Security: N/A.
- Performance: N/A.
- Localization: N/A (state only).
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 03.
- Documentation: KDoc.
- Dependencies: K-01.
- Do Not Change: N/A.
- Expected Result: Independent screen-time slice available.
- Definition of Done: Matches §10.

**Task 02 — Build ScreenTimeSummaryCard Composable**
- Task ID: K05-T02
- Objective: Visual rendering, calm/non-judgmental.
- Why This Is Required: UI delivery per FR-9.
- Existing Architecture to Follow: `:core:design-system` progress-bar/status-badge primitives.
- Existing Files to Reuse: Design-system primitives.
- Files to Create: `ScreenTimeSummaryCard.kt`.
- Files to Modify: `ParentDashboardScreen.kt`.
- Implementation Details: Per §10.
- Business Rules: FR-9.
- Validation: N/A.
- Error Handling: Independent placeholder.
- Security: N/A.
- Performance: N/A.
- Localization: Status label localized, no hardcoded copy.
- RTL: Mirrors correctly.
- Analytics: `screen_time_summary_viewed`, `module_shortcut_tapped(screen_time)`.
- Tests: Covered in Task 03.
- Documentation: KDoc.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Component renders correctly.
- Definition of Done: Matches PRD §1.18 row 5, FR-9 tone requirement.

**Task 03 — Write Test Suite**
- Task ID: K05-T03
- Objective: Cover §27.
- Why This Is Required: QA coverage.
- Existing Architecture to Follow: Existing test conventions.
- Existing Files to Reuse: Fake repository doubles.
- Files to Create: `ScreenTimeSummaryCardTest.kt`.
- Files to Modify: none.
- Implementation Details: 4 cases per §27.
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
Screen-time summary renders calmly, non-judgmentally, tap-through works, independent failure isolation verified, all tests green.

## 31. Final Verification Checklist
- [ ] No alarming/red-flag visual styling anywhere in this component
- [ ] Tap-through route confirmed against C.23's actual route once available
- [ ] Independent degradation verified
- [ ] RTL verified
