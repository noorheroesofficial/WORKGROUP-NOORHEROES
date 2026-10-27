# Blueprint: Parent Dashboard Landing Screen

## 1. Feature Context
Platform: NoorHeroes KMP App (Kotlin Multiplatform, Compose, Android/iOS). New module `:feature:parent-dashboard`. This blueprint delivers the screen shell, ViewModel, and state architecture that K-02 through K-08 build upon.

## 2. Parent Feature
C.20 — Parent Dashboard.

## 3. Sub-feature
K-01 — Parent Dashboard Landing Screen.

## 4. Objective
Build `ParentDashboardScreen` (Compose) and `ParentDashboardViewModel`, reachable only via `:core:auth`'s Parent Gate (C.19) success path, modeling each Dashboard component as an independently-loading/failing state slice, deriving the active family/parent session exclusively from `:core:auth`.

## 5. Business Requirements
Source: PRD §6.1–§6.4, §6.10, §1.10 Edge Cases #1, #2, #4, #6, §1.13 Loading States, §2.2 Screen-Level Design.
- Module `:feature:parent-dashboard`, depends on `:core:auth`, `:core:design-system`, `:core:network`, `:core:offline-cache`.
- Each component (child switcher, weekly report, timeline, screen-time summary) is an independent loading/content/error slice.
- `ParentDashboardViewModel` derives `family_id`/parent session entirely from `:core:auth`'s session provider — never an externally-supplied parameter (mirrors B.16's established "derive internally" pattern).
- Skeleton shimmer per component independently; child switcher chips load fast/first.

## 6. Existing Architecture
Per `CORE_COMMON_INSTRUCTIONS.md`, `CORE_DATA_INSTRUCTIONS.md`, `CORE_NAVIGATION_INSTRUCTIONS.md`:
- `NoorResult<T>` (`Outcome<T, AppError>`) is the standard fallible-operation return type.
- `AuthStateProvider` (core-common) / `AuthRepository` (core-data) expose auth state; `ParentDashboardRoute` is already referenced as an example destination in `CORE_NAVIGATION_INSTRUCTIONS.md` §10 Scenario 2, confirming this is the platform's established naming convention.
- `DispatcherProvider` injected for coroutine dispatching (never hardcode `Dispatchers.IO`).
- `LocalDateProvider.currentFamilyLocalDate()` for any date-boundary logic (e.g., "as of" freshness labeling).
- Repository pattern: `FamilyRepository` (core-common interface) for child-profile data.

## 7. Existing Code to Reuse
- `AuthStateProvider` / `AuthRepository` for deriving active parent/family session — do not accept `family_id` as a constructor or method parameter anywhere in this ViewModel/Repository chain.
- `NoorResult<T>` / `Outcome.Success` / `Outcome.Failure` for all repository calls.
- `Navigator` interface (`core-navigation`) — `ParentDashboardRoute` already anticipated in the navigation architecture doc.
- `BaseViewModel` (referenced in `CORE_NAVIGATION_INSTRUCTIONS.md` as providing `navigator: Lazy<Navigator>`) as the base class.
- Design tokens from `:core:design-system`, Parent-Mode formal visual register established in C.19 §2.1 (per PRD §2's cross-reference).

## 8. Files to Create
- `feature/parent-dashboard/src/commonMain/kotlin/.../ParentDashboardRoute.kt` (Route definition)
- `feature/parent-dashboard/src/commonMain/kotlin/.../ParentDashboardScreen.kt`
- `feature/parent-dashboard/src/commonMain/kotlin/.../ParentDashboardViewModel.kt`
- `feature/parent-dashboard/src/commonMain/kotlin/.../DashboardUiState.kt`
- `feature/parent-dashboard/src/commonMain/kotlin/.../DashboardRepository.kt` (interface)
- `feature/parent-dashboard/src/commonMain/kotlin/.../di/ParentDashboardModule.kt` (Koin module)
- `feature/parent-dashboard/src/commonTest/kotlin/.../ParentDashboardViewModelTest.kt`
- `feature/parent-dashboard/src/commonTest/kotlin/.../DashboardRepositoryFamilyScopeStructuralTest.kt`

## 9. Files to Modify
- App-level Koin DI root registration — include `ParentDashboardModule`
- Navigation graph registration (wherever `Route` implementations are registered to composables) — register `ParentDashboardRoute`

## 10. KMP Requirements
- `Route`: `@Serializable data object ParentDashboardRoute : Route { override val requiredAuthState = BaseAuthState.Parent::class; override val analyticsName = "parent_dashboard" }`. **Confirmed exact class name** — `BaseAuthState.Parent` is used verbatim by C.23's already-written `ControlsLandingRoute` and C.22's `PerChildReportRoute` blueprints (both explicitly cross-reference `ParentDashboardRoute` as the pattern they mirror), resolving the earlier placeholder.
- **Missing component identified during cross-reference with C.25's already-written blueprints:** the screen needs a notification bell icon in its header/chrome, distinct from the "Support" module-shortcut-grid icon (K-06). C.25 KMP/01 (`notifications-inbox-screen-read-state-sync.md`) explicitly states: "Parent Dashboard's bell icon (C.20's `ParentDashboardScreen`) — wire navigation to `NotificationsInboxRoute` (coordinate with C.20's module shortcut grid if not already wired)." Add a `NotificationBellIcon` composable to the screen scaffold (header area, alongside or near the child switcher), navigating via `Navigator.navigateTo(NotificationsInboxRoute)` (C.25) — this is a 6th, chrome-level entry point, separate from the 5-icon module shortcut grid's "Support" icon (which targets `SupportCenterRoute` instead, per K-06's corrected routing).
- `DashboardUiState`: data class with 4 independent slices, each `sealed interface ComponentState { object Loading; data class Content(...); data class Error(val error: AppError) }` — for child switcher, weekly report, activity timeline, screen-time summary.
- `ParentDashboardViewModel(dashboardRepository: DashboardRepository, authStateProvider: AuthStateProvider, dispatchers: DispatcherProvider) : BaseViewModel()`. Exposes `StateFlow<DashboardUiState>`.
- On init, derive `familyId`/active `childId` from `authStateProvider` (never accept as constructor param) and trigger independent fetches for each component.
- Switching child (via K-02) triggers re-fetch of all 4 components scoped to the new `childId`, while `familyId` remains fixed to the session's own family.
- Handle disabled/archived child selection → repository returns a read-only-flagged state; ViewModel surfaces this to UI (K-02 renders the distinction).
- Handle zero-activity empty state and offline state (delegated to K-07 for caching specifics, but this ViewModel's state model must accommodate an `Offline` variant).

## 11. Files to Create — Screen Composable
`ParentDashboardScreen` composes: child switcher (K-02), weekly report card (K-03), activity timeline (K-04), screen-time summary (K-05), module shortcut grid (K-06) — this blueprint owns the scaffold/layout only; each component's own rendering logic is delivered by its respective K-0x blueprint. Skeleton shimmer shown per-component independently while `ComponentState.Loading`.

## 12. NextJS Requirements
N/A.

## 13. API Contract
Consumes `GET /v1/parent/dashboard?child_id=` (B-02) via `DashboardRepository.getDashboard(childId): NoorResult<DashboardData>`.

## 14. Database Requirements
Local Room caching schema is K-07's responsibility; this blueprint defines the `DashboardRepository` interface method signatures that K-07 implements against Room + network.

## 15. Validation
`DashboardRepository`'s public methods must accept only `childId` — no method may accept an externally-supplied `familyId` (enforced by Task 03's structural test).

## 16. Authentication
Reachable only via `:core:auth`'s Parent Gate success path (C.19) — `requiredAuthState` on the `Route` enforces this at the navigation-guard layer.

## 17. Authorization
`familyId` derivation exclusively from the authenticated session — never externally injectable, preventing any code path from viewing another family's dashboard.

## 18. Error Handling
- Each component slice independently transitions to `Error` on its own fetch failure without affecting sibling slices.
- Full-screen error only if the initial session/family derivation itself fails (should be unreachable given the Parent Gate precondition, but must degrade gracefully rather than crash if it somehow occurs).

## 19. Offline First
Full offline-caching implementation is K-07; this ViewModel's state model includes a `stale: Boolean` flag on each component slice to support K-07's "may be outdated" indicator.

## 20. Local Data
Room-backed via K-07; this blueprint's `DashboardRepository` interface is Room-agnostic (interface only), keeping the ViewModel decoupled from the specific persistence mechanism per `core-data`'s repository pattern.

## 21. Localization
No hardcoded strings in Composables — all copy resolved via the platform's `localization` package (`core-common`), supporting English/Hindi/Arabic/Urdu.

## 22. RTL
Layout must mirror correctly in RTL (Arabic/Urdu) per platform's Compose RTL support (`LayoutDirection`); child switcher chip row, module grid, and card layouts must all be tested in RTL preview.

## 23. Analytics
`parent_dashboard_viewed` fired once the screen reaches a stable rendered state (not on every recomposition) — use existing `CORE_ANALYTICS_INSTRUCTIONS.md` conventions (not read in this pass; confirm exact analytics-firing API before implementation rather than inventing one).

## 24. Performance
- Independent component slices prevent one slow/failing fetch from blocking others (Compose recomposition scoped per slice via stable, immutable state classes).
- Avoid unnecessary recomposition: `DashboardUiState` and its nested slices must be `@Immutable`/`@Stable` per `core-common`'s modeling convention (§7 of `CORE_COMMON_INSTRUCTIONS.md`: "All models are `@Immutable`").
- Coroutine cancellation handled correctly on `ViewModel` clear (via `viewModelScope`/`appScope` conventions).

## 25. Security
No sensitive data handled directly in this shell screen beyond what's already governed by underlying domain data; session derivation exclusively from `:core:auth` prevents any bypass.

## 26. Library Requirements
No new third-party libraries — uses existing Koin, Kotlin Coroutines/Flow, Compose Multiplatform per platform conventions.

## 27. Testing
1. Unit test: each component slice transitions Loading → Content independently.
2. Unit test: simulated failure of weekly-report fetch does not block/blank timeline or screen-time-summary components (PRD Android AI Code-Gen Prompt item 1).
3. **Structural/reflection test (mandatory):** confirm no public method on `DashboardRepository` accepts an externally-supplied `family_id` parameter (mirrors B.16/C.19 pattern).
4. Unit test: child-switch triggers re-fetch of all 4 components for the new `childId`.
5. UI test: skeleton shimmer renders independently per component during loading.
6. Integration test: full Parent Gate success → Dashboard load flow.

## 28. Documentation
KDoc on `ParentDashboardViewModel` and `DashboardRepository` citing PRD §6.1–§6.4; author attribution per platform convention ("Mention Sarvare Alam as author in class-level KDoc" — `CORE_COMMON_INSTRUCTIONS.md` §10).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Route and DashboardUiState Models**
- Task ID: K01-T01
- Objective: Type-safe navigation destination and state model.
- Why This Is Required: Foundation for screen and ViewModel.
- Existing Architecture to Follow: `Route` sealed interface pattern (`CORE_NAVIGATION_INSTRUCTIONS.md`).
- Existing Files to Reuse: `Route`, `BaseAuthState` hierarchy.
- Files to Create: `ParentDashboardRoute.kt`, `DashboardUiState.kt`.
- Files to Modify: none.
- Implementation Details: Per §10 above; `BaseAuthState.Parent` is now confirmed (cross-referenced against C.22/C.23's already-written blueprints), no further confirmation needed. Also create `NotificationBellIcon.kt` (header chrome, navigates to `NotificationsInboxRoute`) as part of this task's screen-scaffold deliverable — the missing component identified in §10.
- Business Rules: PRD §6.3 Navigation Flow.
- Validation: N/A.
- Error Handling: N/A.
- Security: `requiredAuthState` guard.
- Performance: `@Immutable` state classes.
- Localization: N/A (no strings in these files).
- RTL: N/A.
- Analytics: `analyticsName = "parent_dashboard"`.
- Tests: Covered in Task 05.
- Documentation: KDoc.
- Dependencies: none.
- Do Not Change: Do not modify `Route` interface itself or other existing routes.
- Expected Result: Route and state types compile and are usable.
- Definition of Done: Matches §10 spec.

**Task 02 — Define DashboardRepository Interface**
- Task ID: K01-T02
- Objective: Data-access contract, family-scope-safe by construction.
- Why This Is Required: Decouples ViewModel from network/cache implementation; enforces the "derive internally" security pattern.
- Existing Architecture to Follow: `core-data` repository interface pattern.
- Existing Files to Reuse: `NoorResult<T>`.
- Files to Create: `DashboardRepository.kt` (interface).
- Files to Modify: none.
- Implementation Details: `interface DashboardRepository { suspend fun getDashboard(childId: String): NoorResult<DashboardData>; suspend fun getReport(type: ReportType, childId: String): NoorResult<ReportData> }` — no `familyId` parameter anywhere.
- Business Rules: PRD §6.4.
- Validation: N/A.
- Error Handling: `NoorResult` per `core-data` convention.
- Security: No externally-supplied family scope — this is the structural guarantee.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 05 (structural test).
- Documentation: KDoc.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Interface compiles; implementation deferred to K-07.
- Definition of Done: No method signature accepts `familyId`.

**Task 03 — Implement ParentDashboardViewModel**
- Task ID: K01-T03
- Objective: Core state-management logic.
- Why This Is Required: Central orchestrator of the screen.
- Existing Architecture to Follow: `BaseViewModel`, `AuthStateProvider`, `DispatcherProvider` injection conventions.
- Existing Files to Reuse: `BaseViewModel`, `AuthStateProvider`, `DispatcherProvider`.
- Files to Create: `ParentDashboardViewModel.kt`.
- Files to Modify: none.
- Implementation Details: Per §10; independent `StateFlow` slice updates per component via parallel coroutine launches.
- Business Rules: PRD §6.4, Edge Cases #1, #2, #4.
- Validation: N/A.
- Error Handling: Per-slice error isolation.
- Security: Session-derived `familyId` only.
- Performance: Parallel fetches, `@Stable` state.
- Localization: N/A (ViewModel has no strings).
- RTL: N/A.
- Analytics: Fire `parent_dashboard_viewed` on stable render.
- Tests: Covered in Task 05.
- Documentation: KDoc, author tag.
- Dependencies: Tasks 01–02.
- Do Not Change: Do not modify `BaseViewModel`.
- Expected Result: ViewModel functional against a fake/mock `DashboardRepository`.
- Definition of Done: All Task 05 tests pass.

**Task 04 — Implement ParentDashboardScreen Composable Shell**
- Task ID: K01-T04
- Objective: Screen scaffold hosting the 5 child components.
- Why This Is Required: Visual delivery of the landing screen.
- Existing Architecture to Follow: `:core:design-system` tokens, Parent-Mode formal visual register (C.19 §2.1).
- Existing Files to Reuse: Design-system components (buttons, cards, skeleton shimmer primitives) — confirm exact component names against `CORE_DESIGNSYSTEM_INSTRUCTIONS.md` before use (not read in this pass; do not invent component names).
- Files to Create: `ParentDashboardScreen.kt`.
- Files to Modify: Navigation graph registration.
- Implementation Details: Vertically scrolling, card-based layout per PRD §2.4; slots for K-02 through K-06's components, each independently observing its `DashboardUiState` slice.
- Business Rules: PRD §2.2.
- Validation: N/A.
- Error Handling: Per-component error rendering.
- Security: N/A (UI layer).
- Performance: Stable keys for LazyColumn items if used; avoid unnecessary recomposition.
- Localization: All strings via localization package.
- RTL: Layout mirrors correctly.
- Analytics: N/A (fired from ViewModel).
- Tests: Covered in Task 05 (UI tests).
- Documentation: KDoc.
- Dependencies: Task 03.
- Do Not Change: N/A.
- Expected Result: Screen renders with skeleton/content/error states per component.
- Definition of Done: Matches PRD §2.2 wireframe description.

**Task 05 — Write Test Suite**
- Task ID: K01-T05
- Objective: Cover §27 scenarios.
- Why This Is Required: PRD Android AI Code-Gen Prompt items 1–2 mandate specific tests.
- Existing Architecture to Follow: Kotlin test + Compose UI testing conventions already used elsewhere in the codebase.
- Existing Files to Reuse: Existing fake `AuthStateProvider`/repository test doubles if present.
- Files to Create: `ParentDashboardViewModelTest.kt`, `DashboardRepositoryFamilyScopeStructuralTest.kt`.
- Files to Modify: none.
- Implementation Details: 6 test cases per §27, including the reflection-based structural test on `DashboardRepository`.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: N/A.
- Security: Structural test is security-critical.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A (RTL is a manual/preview verification, not unit-tested here).
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test KDoc.
- Dependencies: Tasks 01–04.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 green.

## 30. Definition of Done
`:feature:parent-dashboard` module compiles, `ParentDashboardScreen`/`ParentDashboardViewModel` functional with independent per-component state slices, session-derived family scoping structurally enforced, reachable only via Parent Gate, all tests green.

## 31. Final Verification Checklist
- [ ] Reflection-based structural test confirms no externally-supplied `familyId` anywhere in `DashboardRepository`
- [ ] Independent component failure does not blank other components (verified by test)
- [ ] `requiredAuthState` correctly gates navigation to this Route
- [ ] All state classes `@Immutable`/`@Stable`
- [ ] No hardcoded strings
- [ ] RTL layout verified via preview
