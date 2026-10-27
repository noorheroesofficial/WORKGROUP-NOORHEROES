# Blueprint: Per-Child Report Screen & State Architecture

## 1. Feature Context
Platform: NoorHeroes KMP App (Kotlin Multiplatform, Compose, Android/iOS). New module `:feature:reports`. Delivers the screen shell, ViewModel, and state architecture that K-02 through K-09 build upon.

## 2. Parent Feature
C.22 — Per-Child Reports.

## 3. Sub-feature
K-01 — Per-Child Report Screen & State Architecture.

## 4. Objective
Build `PerChildReportScreen` (Compose) and `PerChildReportViewModel`, reachable only via `:core:auth`'s Parent Gate (C.19/C.20) success path, modeling each of the four report components (trend chart, habit calendar, skill mastery grid, AI interaction summary) as an independently-loading/failing state slice, with a single date range applied to all of them via one repository call.

## 5. Business Requirements
Source: PRD §6.1–§6.4, §6.10, §1.10 Edge Case #1, §1.13 Loading States, §2.2 Screen-Level Design, §1.7 FR-14.
- Module `:feature:reports`, depends on `:core:auth`, `:core:design-system`, `:core:network`, `:core:offline-cache`.
- Each component is an independent loading/content/error/offline state slice.
- A single selected date range governs the whole report view — the ViewModel never independently re-filters one component's already-fetched data to a different range than another's (FR-14, mirrors C.20 B-02/K-01's single-range convention).
- Skeleton shimmer per component independently.
- Reachable only via C.19/C.20 Parent Gate success path.

## 6. Existing Architecture
Per `CORE_COMMON_INSTRUCTIONS.md`, `CORE_DATA_INSTRUCTIONS.md`, `CORE_NAVIGATION_INSTRUCTIONS.md`, and C.20 KMP Blueprint K-01 (`01-parent-dashboard-landing-screen.md`):
- `NoorResult<T>` (`Outcome<T, AppError>`) is the standard fallible-operation return type.
- `AuthStateProvider`/`AuthRepository` (core-auth) expose parent/family session state — derive internally, never accept as a parameter (established "derive internally" pattern from B.16/C.20 K-01).
- `DispatcherProvider` injected for coroutine dispatching.
- `LocalDateProvider.currentFamilyLocalDate()` for date-boundary logic (e.g., "as of" freshness labeling, clamped-range communication for Edge Case #1).
- `BaseViewModel` (`navigator: Lazy<Navigator>`) as the base class.
- C.20 K-01 establishes `ParentDashboardRoute`/`ParentDashboardScreen` as the sibling pattern this module directly mirrors, one navigation level deeper.

## 7. Existing Code to Reuse
- `AuthStateProvider`/`AuthRepository` for deriving parent/family session — never accept `family_id`/`child_id` as an externally-supplied constructor parameter beyond what navigation passes as the target child.
- `NoorResult<T>`/`Outcome.Success`/`Outcome.Failure`.
- `Navigator` interface (`core-navigation`).
- `BaseViewModel`.
- Design tokens from `:core:design-system`, Parent-Mode formal visual register established in C.19 §2.1/C.20 §2.1.
- `DashboardRepository` pattern established in C.20 K-01 as the sibling interface this module's `ReportRepository` mirrors.

## 8. Files to Create
- `feature/reports/src/commonMain/kotlin/.../PerChildReportRoute.kt`
- `feature/reports/src/commonMain/kotlin/.../PerChildReportScreen.kt`
- `feature/reports/src/commonMain/kotlin/.../PerChildReportViewModel.kt`
- `feature/reports/src/commonMain/kotlin/.../PerChildReportUiState.kt`
- `feature/reports/src/commonMain/kotlin/.../ReportRepository.kt` (interface)
- `feature/reports/src/commonMain/kotlin/.../di/ReportsModule.kt` (Koin module)
- `feature/reports/src/commonTest/kotlin/.../PerChildReportViewModelTest.kt`
- `feature/reports/src/commonTest/kotlin/.../ReportRepositorySingleRangeStructuralTest.kt`

## 9. Files to Modify
- App-level Koin DI root registration — include `ReportsModule`
- Navigation graph registration — register `PerChildReportRoute`

## 10. KMP Requirements
- `Route`: `@Serializable data class PerChildReportRoute(val childId: String) : Route { override val requiredAuthState = BaseAuthState.Parent::class; override val analyticsName = "per_child_report" }` — confirmed exact class per `core-navigation::BaseAuthState.Parent`, the same guard used by C.20 K-01's `ParentDashboardRoute` and C.23 K-01's `ControlsLandingRoute`.
- `PerChildReportUiState`: data class with 4 independent slices — `trendChart`, `habitCalendar`, `skillMasterySummary`, `aiInteractionSummary` — each `sealed interface ComponentState { object Loading; data class Content(...); data class Delayed(val asOf: Instant); object NoActivity; data class Error(val error: AppError); object Offline }`, plus a shared `selectedDateRange: DateRange` and `rangeClampedAtAccountStart: Boolean` (Edge Case #1).
- `PerChildReportViewModel(reportRepository: ReportRepository, authStateProvider: AuthStateProvider, dispatchers: DispatcherProvider) : BaseViewModel()`. Exposes `StateFlow<PerChildReportUiState>`.
- On init, derive `familyId` from `authStateProvider`; accept `childId` from navigation args (`PerChildReportRoute.childId`); trigger a single `reportRepository.getReport(childId, selectedDateRange)` call producing all four component slices together.
- Changing the date range triggers exactly one re-fetch call with the new range, updating all four slices atomically — never partial-range updates.
- Handle the server's `rangeClampedAtAccountStart` flag by surfacing a clear boundary message in the UI state.
- Handle zero-activity, delayed-analytics, and offline states per component, mapped from the repository's response.

## 11. Files to Create — Screen Composable
- `PerChildReportScreen`: top date-range filter pill, `TrendChartCard`, `HabitCalendarCard`, `SkillMasteryGridCard` (K-02 renders detail internals), `AiInteractionSummaryCard` (links to K-03), export/share action buttons (K-07/K-08 own their flows, this screen only hosts the trigger buttons).
- Each card independently renders its own `ComponentState` (skeleton shimmer while `Loading`, content while `Content`, delayed banner while `Delayed`, empty framing while `NoActivity`, cached-with-badge while `Offline`, retry affordance while `Error`).

## 12. NextJS Requirements
N/A.

## 13. API Mapping
`ReportRepository.getReport(childId: String, from: LocalDate, to: LocalDate): NoorResult<PerChildReportData>` → `GET /v1/parent/reports/{child_id}?from=&to=` (Backend B-01).

## 14. Database Requirements (Local)
`:core:offline-cache` (Room) stores the last successfully fetched `PerChildReportData` per `(childId, from, to)` for offline read (delegated in full to K-09, but this ViewModel's state model must accommodate an `Offline` variant sourced from cache).

## 15. Validation
`childId` must be present in navigation args (route is not reachable without it); date range must be `from <= to`, validated before triggering the repository call.

## 16. Authentication
Route requires `BaseAuthState.Parent` — unreachable without a successful C.19/C.20 Parent Gate pass.

## 17. Authorization
`childId` scoping is enforced server-side (Backend B-01); the client does not perform its own family-ownership check, but must gracefully surface a `403`/`404` `ChildScopeViolationError` as an `Error` state if it somehow occurs (e.g., stale deep link to a since-unlinked child).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Repository call fails entirely | All four slices show `Error` with retry |
| One backend component degraded (server-side graceful placeholder) | That slice's `Content` renders the "may be unavailable right now" placeholder text from the server payload |
| Offline | All slices show `Offline` sourced from cache, export/share buttons disabled |
| `rangeClampedAtAccountStart: true` | Non-error informational banner, not an `Error` state |

## 19. Offline First
In-app view renders from `:core:offline-cache` when offline (read-only); full mechanics delegated to K-09.

## 20. Local Data
Room-cached `PerChildReportData` keyed by `(childId, from, to)`.

## 21. Localization
All UI copy (empty-state framing, delayed banner, clamped-range message) sourced from the platform's string-resource/localization system — English, Hindi, Arabic, Urdu — no hardcoded strings.

## 22. RTL
Full RTL layout mirroring for Arabic/Urdu — date-range filter pill, card stacking order, and chart label alignment all mirror correctly; verified against C.19/C.20's established Parent-Mode RTL patterns.

## 23. Analytics
`per_child_report_viewed` fired on successful initial load; `report_date_range_filtered` fired on every date-range change, both via `PerChildReportAnalytics` (K wiring, consistent with C.20's analytics pattern).

## 24. Performance
- Single repository call per range change (never N calls for N components).
- `Stable`/`Immutable` annotations on `PerChildReportUiState` and its slices to prevent unnecessary recomposition.
- Coroutine cancellation on rapid successive date-range changes (cancel in-flight fetch before starting a new one).
- No main-thread blocking during date-range computation.

## 25. Security
No `family_id`/`child_id` accepted as a raw constructor parameter beyond what navigation provides; all authorization enforcement is server-side, client only reflects results.

## 26. Library Requirements
Koin (DI), Kotlinx Coroutines, Kotlinx DateTime — all existing platform dependencies, no new libraries.

## 27. Testing
- Unit: single date-range applied to all four slices via one repository call (structural test).
- Unit: rapid date-range changes cancel the prior in-flight fetch.
- Unit: `rangeClampedAtAccountStart` correctly surfaced as an informational, non-error state.
- UI test: skeleton shimmer renders independently per card while loading.
- UI test: offline state disables export/share buttons.

## 28. Documentation
KDoc on `PerChildReportViewModel` and `ReportRepository` explaining the single-range-per-fetch contract; module README describing the four-slice state model.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define PerChildReportUiState and Route**
- Task ID: K01-T01
- Objective: Model the four independent component slices plus shared date-range state.
- Why This Is Required: Foundation for every other KMP sub-feature in this blueprint set.
- Existing Architecture to Follow: C.20 K-01's `DashboardUiState` sibling pattern.
- Existing Files to Reuse: `Route` interface, `BaseAuthState`.
- Files to Create: `PerChildReportRoute.kt`, `PerChildReportUiState.kt`.
- Files to Modify: none.
- Implementation Details: Per §10.
- Business Rules: FR-14.
- Validation: N/A.
- Error Handling: `Error`/`Offline`/`Delayed`/`NoActivity` variants per slice.
- Security: `requiredAuthState` correctly set.
- Performance: `@Immutable`/`@Stable` annotations.
- Localization: N/A at this layer.
- RTL: N/A at this layer.
- Analytics: `analyticsName` set on the route.
- Tests: Covered in Task 05.
- Documentation: KDoc.
- Dependencies: none.
- Do Not Change: C.20's `DashboardUiState`.
- Expected Result: State model compiles and is importable.
- Definition of Done: Matches §10 exactly.

**Task 02 — Implement ReportRepository Interface and Network Implementation**
- Task ID: K01-T02
- Objective: Single-call fetch of all four components for a given range.
- Why This Is Required: FR-14's client-side enforcement point.
- Existing Architecture to Follow: `:core:network`'s Ktor-based `HttpClient` (`OkHttp` engine on Android, `Darwin` on iOS, per `CORE_NETWORK_INSTRUCTIONS.md`), `NoorResult<T>` wrapping.
- Existing Files to Reuse: `:core:network` base client.
- Files to Create: `ReportRepository.kt` (interface + impl).
- Files to Modify: none.
- Implementation Details: `getReport(childId, from, to): NoorResult<PerChildReportData>` maps to Backend B-01's contract exactly.
- Business Rules: FR-14.
- Validation: N/A.
- Error Handling: Maps HTTP errors to `AppError` variants.
- Security: No client-side authorization logic (server-enforced).
- Performance: Single network call per fetch.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 05.
- Documentation: KDoc.
- Dependencies: Task 01, Backend B-01 must be live.
- Do Not Change: `:core:network` base client internals.
- Expected Result: Repository returns correctly mapped data.
- Definition of Done: Contract match with Backend B-01 §13 verified.

**Task 03 — Implement PerChildReportViewModel**
- Task ID: K01-T03
- Objective: Wire session derivation, single-fetch-per-range logic, and state emission.
- Why This Is Required: Core presentation logic.
- Existing Architecture to Follow: `BaseViewModel`, `AuthStateProvider` derive-internally pattern.
- Existing Files to Reuse: `AuthStateProvider`, `DispatcherProvider`.
- Files to Create: `PerChildReportViewModel.kt`.
- Files to Modify: none.
- Implementation Details: Per §10.
- Business Rules: FR-14, Edge Case #1.
- Validation: `from <= to` before fetch.
- Error Handling: Per §18.
- Security: Session derived internally, never passed as a param.
- Performance: Coroutine cancellation on rapid range changes.
- Localization: N/A at this layer (copy resolution happens in Compose layer).
- RTL: N/A.
- Analytics: Fires `per_child_report_viewed`/`report_date_range_filtered`.
- Tests: Covered in Task 05.
- Documentation: KDoc.
- Dependencies: Tasks 01–02.
- Do Not Change: `BaseViewModel` internals.
- Expected Result: ViewModel correctly emits state for all scenarios.
- Definition of Done: All §18 scenarios verified.

**Task 04 — Implement PerChildReportScreen Composable**
- Task ID: K01-T04
- Objective: Render the four independent cards plus date-range filter and action buttons.
- Why This Is Required: User-facing delivery of this sub-feature.
- Existing Architecture to Follow: `:core:design-system` tokens, C.19/C.20 Parent-Mode visual register.
- Existing Files to Reuse: Design-system card/skeleton components.
- Files to Create: `PerChildReportScreen.kt`.
- Files to Modify: Navigation graph registration.
- Implementation Details: Per §11.
- Business Rules: FR-14.
- Validation: N/A.
- Error Handling: Per-card error/retry UI.
- Security: N/A.
- Performance: `@Stable` state consumption, no unnecessary recomposition.
- Localization: All copy from string resources.
- RTL: Full mirroring verified.
- Analytics: N/A (ViewModel-level).
- Tests: Covered in Task 05.
- Documentation: KDoc.
- Dependencies: Task 03.
- Do Not Change: `:core:design-system` component internals.
- Expected Result: Screen renders correctly across all states.
- Definition of Done: Matches §2.2 PRD screen-level design requirements.

**Task 05 — Write Test Suite**
- Task ID: K01-T05
- Objective: Cover §27.
- Why This Is Required: QA coverage for the foundational state architecture every other sub-feature depends on.
- Existing Architecture to Follow: Kotlin test + Compose UI test conventions used elsewhere in the KMP app.
- Existing Files to Reuse: Existing test fixtures for `AuthStateProvider`/session mocking.
- Files to Create: `PerChildReportViewModelTest.kt`, `ReportRepositorySingleRangeStructuralTest.kt`.
- Files to Modify: none.
- Implementation Details: 5 test cases per §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert exact state transitions.
- Security: N/A.
- Performance: Cancellation test is important here.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test KDoc.
- Dependencies: Tasks 01–04.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 green.

## 30. Definition of Done
`:feature:reports` module scaffolded, `PerChildReportScreen`/`PerChildReportViewModel` live, single date range applied atomically to all four components via one repository call, all states (loading/content/delayed/no-activity/offline/error) correctly rendered, all tests green.

## 31. Final Verification Checklist
- [ ] Single repository call per date-range change, never per-component independent calls
- [ ] All four component slices independently render loading/content/error/offline
- [ ] `rangeClampedAtAccountStart` surfaced as informational, not error (Edge Case #1)
- [ ] Session derived internally from `:core:auth`, never passed as a raw parameter
- [ ] No unnecessary recomposition (stability annotations verified)
- [ ] Full localization (EN/HI/AR/UR) and RTL mirroring verified
- [ ] Reachable only via Parent Gate success path
