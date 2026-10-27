# K-09 — Weekly Habit Report — In-App Parent View

## 1. Feature Context
NoorHeroes KMP app, parent-facing surface within `feature-habits`. Renders the highlights-framed Weekly Habit Report and per-habit detail drill-in.

## 2. Parent Feature
A.7 Habit Tracker — KMP App (Android/iOS)

## 3. Sub-feature
K-09 Weekly Habit Report — In-App Parent View

## 4. Objective
Build the Weekly Habit Report and Per-Habit Detail screens rendering B-07's single-child, highlights-framed report data, with a structural UI test verifying zero per-child comparative elements (FR-21).

## 5. Business Requirements
- Highlights framing, never raw failure/success scorecards (FR-21).
- Single-child-at-a-time rendering enforced at the component level — no simultaneous sibling comparison layout, mirroring K-05's Family Garden constraint.
- Zero-history state handled gracefully, not as an error.

## 6. Existing Architecture
Lives in `feature-habits`'s parent-facing package (per K-08's corrected module convention — no shared Parent Area module exists). **Confirmed strong precedent found:** `C22_Per_Child_Reports/KMP/01-per-child-report-screen-and-state-architecture.md` establishes the canonical NoorHeroes parent-report architecture — module `:feature:reports`, `PerChildReportRoute`/`PerChildReportScreen`/`PerChildReportViewModel`/`ReportRepository` (interface), a `PerChildReportUiState` holding independent `ComponentState` (`Loading`/`Content`/`Delayed`/`NoActivity`/`Error`/`Offline`) sealed-interface slices per report component rather than one screen-wide loading flag, a single shared `selectedDateRange`, gated via `BaseAuthState.Parent::class`. This sub-feature mirrors that exact architecture rather than inventing its own.

## 7. Existing Code to Reuse
- C.22's `PerChildReportRoute`/`Screen`/`ViewModel`/`Repository` naming and `ComponentState` sealed-interface pattern (per §6) — apply the same shape to `WeeklyHabitReportScreen`/`WeeklyHabitReportViewModel`/`HabitReportRepository`/`HabitReportUiState`.
- `core-navigation`'s `BaseAuthState.Parent::class` route-gating convention (confirmed also used by C.20 K-01, C.23 K-01).
- `core-design-system` chart/summary components if already established elsewhere.

## 8. Files to Create
- `feature-habits/src/commonMain/kotlin/.../parent/report/WeeklyHabitReportScreen.kt`
- `feature-habits/src/commonMain/kotlin/.../parent/report/WeeklyHabitReportViewModel.kt`
- `feature-habits/src/commonMain/kotlin/.../parent/report/WeeklyHabitReportUiState.kt` (per-component `ComponentState` slices, mirroring C.22)
- `feature-habits/src/commonMain/kotlin/.../parent/report/WeeklyHabitReportDetailScreen.kt`
- `feature-habits-domain/src/commonMain/kotlin/.../GetWeeklyHabitReportUseCase.kt`
- `feature-habits/src/androidInstrumentedTest/kotlin/.../NoComparativeUiStructuralTest.kt`

## 9. Files to Modify
- `:feature:parent-dashboard`'s Child Progress navigation (C.20) — add Habits entry point routing into `feature-habits`

## 10. Backend Requirements
Consumes `GET /v1/children/{id}/habit-report?period=weekly` (B-07).

## 11. KMP Requirements
- Weekly Habit Report: highlights-framed summary, single child in view at a time.
- Per-Habit Detail drill-in from the summary.
- Structural UI test enumerating rendered components on both screens, asserting no component ever receives more than one child's data simultaneously.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
`GET /v1/children/{id}/habit-report?period=weekly` (B-07).

## 14. Database Requirements (Local)
Room cache of last-fetched report for offline viewing (reports change weekly, cache TTL can be generous).

## 15. Validation
Structural UI test verifying zero per-child comparative UI elements — mirrors B-07's single-child-only API schema guarantee at the presentation layer.

## 16. Authentication
Shared `core-network` Bearer token attachment, parent-session scoped.

## 17. Authorization
Route gated via `BaseAuthState.Parent::class` (per C.22/C.20/C.23's confirmed convention, §6); data-level authorization enforced server-side by B-07.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Zero habit history | "Just getting started" highlights-framed empty state, not an error |
| Report fetch fails | Cached last report shown if available; otherwise a calm retry prompt |

## 19. Offline First
Cached last-fetched report available offline; not a write path.

## 20. Local Data
```
GET /v1/children/{id}/habit-report?period=weekly
   ↓
GetWeeklyHabitReportUseCase
   ↓
Room weekly_report_cache
   ↓
WeeklyHabitReportScreen
```

## 21. Localization
Report copy sourced from B-13's approved templates via B-07; fully localized.

## 22. RTL
Report layout, charts/summaries, and detail drill-in verified for RTL.

## 23. Analytics
`weekly_habit_report_viewed` via `AnalyticsTracker`.

## 24. Performance
Lightweight read-only screens; no special performance constraints beyond standard list/chart rendering.

## 25. Security
No elevated risk; standard parent-session scoping.

## 26. Library Requirements
Compose Multiplatform, Koin, Ktor, Room.

## 27. Testing
- Structural: no-comparative-UI test (mandatory).
- Unit: cache-fallback behavior.
- UI: highlights-framing content rendering, empty state.

## 28. Documentation
KDoc noting the single-child-at-a-time rendering constraint explicitly, cross-referencing B-07's API-level guarantee.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement `GetWeeklyHabitReportUseCase` + Cache**
- Files to Create: use case, Room cache entity/DAO.
- Tests: cache-fallback unit test.
- Definition of Done: correctly fetches and caches single-child report data.

**Task 02 — Build Weekly Habit Report Screen**
- Files to Create: `WeeklyHabitReportScreen.kt`
- Business Rules: FR-21 highlights framing.
- Tests: content-rendering UI test.
- Definition of Done: screen renders correctly with highlights framing and empty state.

**Task 03 — Build Per-Habit Detail Screen**
- Files to Create: `WeeklyHabitReportDetailScreen.kt`
- Definition of Done: drill-in navigation works correctly from summary.

**Task 04 — Write Mandatory Structural No-Comparison UI Test**
- Files to Create: `NoComparativeUiStructuralTest.kt`
- Definition of Done: test passes, registered as CI gate alongside K-05's and B-07's equivalents.

**Task 05 — Wire Navigation & Analytics**
- Files to Modify: `:feature:parent-dashboard`'s Child Progress navigation (C.20).
- Definition of Done: entry point correctly reachable; events wired.

**Task 06 — Final Code Review**
- Do Not Change: single-child-at-a-time rendering constraint.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Weekly Habit Report and detail screens live, highlights-framed, structurally verified free of sibling-comparison UI.

## 31. Final Verification Checklist
- [ ] Structural no-comparative-UI test passes (mandatory)
- [ ] Report content uses highlights framing, not raw scorecards
- [ ] Zero-history empty state handled gracefully
- [ ] Per-Habit Detail drill-in works correctly
- [ ] Localization and RTL verified
- [ ] Analytics events wired
