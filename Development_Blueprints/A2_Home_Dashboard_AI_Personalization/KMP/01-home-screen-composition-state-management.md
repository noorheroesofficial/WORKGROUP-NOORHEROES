# K-01 — Home Screen Composition & Section State Management

## 1. Feature Context
NoorHeroes Child App (Android/iOS, KMP). This is the root Composable module for the entire Home feature — every other KMP sub-feature (K-02 through K-08) plugs into the section-state model established here.

## 2. Parent Feature
A.2 — Child Home Dashboard & AI Personalization

## 3. Sub-feature
2.1 Home Screen Composition & Section State Management (ID: K-01)

## 4. Objective
Build the `:feature:home` module's `HomeScreen` Composable as a composition of independent section Composables, each driven by its own slice of a single `HomeUiState` exposed via `HomeViewModel: StateFlow<HomeUiState>`, where each section is modeled as `SectionState { Loading, Content(data), Error, Hidden }` — mirroring the backend's per-section graceful-degradation contract from B-01.

## 5. Business Requirements
Per PRD §6.1–6.4, §1.13, FR-1:
- Sections render in the exact fixed priority order (Greeting/Streak/XP → Today's Mission → Continue Learning → Continue Watching → Recommended → Daily Quiz → Habits → Weekly Challenge → Milestones → Bedtime Corner (conditional) → Islamic Fact); a Compose UI test must fail the build if reordered.
- Each section resolves independently — a slow/failed section never blocks others.
- Skeleton-screen loading per section (shimmer placeholders matching widget shape), not one full-screen spinner.
- Pull-to-refresh with brand-consistent (non-default-platform) indicator.
- Refresh triggers: app foreground after >15 min background, pull-to-refresh, immediately after any activity affecting Home's own sections.

## 6. Existing Architecture
Follow `NoorHeroes/core/` docs: `CORE_UI_INSTRUCTIONS.md` (Compose conventions), `CORE_NAVIGATION_INSTRUCTIONS.md`, `CORE_DATA_INSTRUCTIONS.md`, `CORE_NETWORK_INSTRUCTIONS.md`, `CORE_DESIGNSYSTEM_INSTRUCTIONS.md`. Module `:feature:home` depends on `:core:design-system`, `:core:network`, `:core:offline-cache` per PRD §6.1. Reuse Global Design System tokens established in Feature A.1's `:core:design-system` module — do not redefine colors/spacing/typography locally.

## 7. Existing Code to Reuse
- `:core:design-system` tokens (color, typography, spacing, elevation) from A.1.
- Existing Hilt DI module conventions from A.1's onboarding feature modules.
- Existing `NavigationEvent` sealed-class pattern if established in A.1's navigation graph.

## 8. Files to Create
- `feature/home/src/commonMain/kotlin/.../HomeScreen.kt`
- `feature/home/src/commonMain/kotlin/.../HomeViewModel.kt`
- `feature/home/src/commonMain/kotlin/.../HomeUiState.kt`
- `feature/home/src/commonMain/kotlin/.../SectionState.kt`
- `feature/home/src/commonMain/kotlin/.../HomeRepository.kt` (interface; implementation detailed further in K-07)
- `feature/home/src/commonMain/kotlin/.../components/GreetingStreakHeader.kt`
- `feature/home/src/androidUnitTest/.../HomeViewModelTest.kt`
- `feature/home/src/androidInstrumentedTest/.../HomeScreenSectionOrderTest.kt`

## 9. Files to Modify
- Root Gradle settings — register `:feature:home` module (if not already scaffolded)
- Main bottom-nav graph — register Home as default start destination

## 10. Backend Requirements
Consumes `GET /v1/home` (B-01). No backend code written here; `HomeRepository.getHome()` is the client-side contract point.

## 11. KMP Requirements
- `HomeUiState` models each of the 10 sections as an independent `SectionState` field (not one global loading/error flag).
- `HomeScreen` composed of independent section Composables, each collecting only its own state slice to minimize recomposition scope.
- Skeleton/shimmer Composable per section shape, shown during `Loading`.
- Pull-to-refresh gesture wired to `HomeViewModel.refresh()`.
- Foreground-resume-after-15-min-background triggers refresh via lifecycle observer.
- `home_viewed` analytics fired once per successful render (one-shot `LaunchedEffect` keyed on resolved-section identity, not on every state emission) — reuse `NoorHeroes/core/core-analytics/CORE_ANALYTICS_INSTRUCTIONS.md` conventions.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
Consumes `GET /v1/home` per B-01's contract (§13 of B-01's blueprint). `HomeRepository.getHome(): HomeUiState` maps the network DTO to `HomeUiState`.

## 14. Database Requirements
Not applicable in this sub-feature directly (local caching is K-07's scope). This sub-feature defines the in-memory state shape only.

## 15. Validation
`HomeUiState` mapping from the network DTO must handle a `null` `bedtime_corner` correctly as `SectionState.Hidden`, distinct from `SectionState.Error`.

## 16. Authentication
Reuses A.1's existing Bearer token attachment via the shared network interceptor (`:core:network`) — no new auth logic here.

## 17. Authorization
N/A at UI layer (enforced server-side); client simply renders what the scoped token returns.

## 18. Error Handling
Each section's `SectionState.Error` renders a section-local, non-blocking error affordance (not a full-screen error) per the backend's per-section degradation contract. Full-payload fetch failure (no cache, true first launch offline) is K-07's scope (Full-Screen Retry state).

## 19. Offline First
This sub-feature defines the state model that K-07's offline cache reads into; `HomeRepository` interface here should be cache-agnostic (K-07 implements the cache-first strategy behind this interface).

## 20. Local Data
Not implemented here (K-07's scope). Interface boundary only.

## 21. Localization
All section labels/copy sourced from shared string resources per `CORE_UI_INSTRUCTIONS.md` convention; no hardcoded user-facing strings.

## 22. RTL
Full layout mirroring for Arabic/Urdu via Compose's built-in `LayoutDirection` — verify horizontal rails and icons (e.g., back/forward affordances) mirror correctly.

## 23. Analytics
`home_viewed` (once per successful render), `home_section_rendered` (once per section as it resolves), `home_pull_to_refresh`. Reuse `CORE_ANALYTICS_INSTRUCTIONS.md` event-firing conventions — do not build a parallel analytics mechanism.

## 24. Performance
- Stable/immutable `HomeUiState` and section data classes (`@Immutable`/`@Stable` annotations) to minimize recomposition.
- Each section Composable reads only its own state slice (`collectAsState` scoped narrowly, e.g., via `derivedStateOf` or per-section `StateFlow` mapping) to avoid full-screen recomposition on a single section's update.
- Avoid main-thread blocking in state mapping (DTO → UI state) — perform on a background dispatcher.

## 25. Security
Content-safety regression UI test (recursive semantics-tree scan for billing-term blocklist) — client-side mirror of B-08's backend audit, non-negotiable per PRD §7 item 5.

## 26. Library Requirements
Jetpack Compose Multiplatform, Kotlin Coroutines/Flow, Hilt (or existing DI per `CORE_COMMON_INSTRUCTIONS.md`), existing networking stack per `CORE_NETWORK_INSTRUCTIONS.md`.

## 27. Testing
- Unit: `HomeViewModel` state-reduction per section, including first-day branching (though First-Day full behavior is K-07's scope, the state-shape support belongs here).
- Compose UI: each section's Loading/Content/Error/Hidden states independently rendered.
- Compose UI: section-order snapshot/semantics-tree traversal test that fails the build if reordered.
- Compose UI: content-safety regression test (billing-term blocklist scan across the rendered tree, multiple fixture states).

## 28. Documentation
Module README for `:feature:home` documenting the `SectionState` pattern and why it exists (mirrors backend degradation contract) so future contributors don't collapse it back into a single global loading flag.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define `HomeUiState` & `SectionState` Models**
- Objective: Core state shape for the entire Home feature.
- Why Required: Every other KMP Home sub-feature depends on this contract.
- Existing Architecture to Follow: `CORE_DATA_INSTRUCTIONS.md` state-modeling conventions.
- Existing Files to Reuse: none new.
- Files to Create: `HomeUiState.kt`, `SectionState.kt`
- Files to Modify: none
- Implementation Details: `sealed interface SectionState<out T> { object Loading; data class Content<T>(val data: T); object Error; object Hidden }`; `data class HomeUiState(val greeting: SectionState<Greeting>, val todayMission: SectionState<Mission>, ... val bedtimeCorner: SectionState<BedtimeCorner>, val isFirstDay: Boolean)` with fields in fixed order matching FR-1.
- Business Rules: `bedtimeCorner = Hidden` when backend returns `null`, not `Error`.
- Validation: N/A (pure data model).
- Error Handling: N/A.
- Security: N/A.
- Performance: `@Immutable` annotations on all state classes.
- Localization: N/A (labels resolved at render time via string resources, not baked into state).
- RTL: N/A.
- Analytics: N/A.
- Tests: Unit tests constructing various state combinations.
- Documentation: KDoc on `SectionState` explaining the four-state model rationale.
- Dependencies: None.
- Do Not Change: N/A.
- Expected Result: State model compiles.
- Definition of Done: Unit tests pass.

**Task 02 — Implement `HomeViewModel`**
- Objective: `StateFlow<HomeUiState>` exposing repository data mapped to state.
- Why Required: Core presentation-layer logic.
- Existing Architecture to Follow: MVVM/Clean Architecture per `CORE_UI_INSTRUCTIONS.md`.
- Existing Files to Reuse: `HomeRepository` interface (defined alongside, implemented in K-07).
- Files to Create: `HomeViewModel.kt`
- Files to Modify: none
- Implementation Details: `refresh()` calls repository, maps DTO → `HomeUiState`, updates `StateFlow`; foreground-resume trigger wired via a lifecycle-aware coroutine that checks elapsed background time (>15 min) before calling `refresh()`.
- Business Rules: Refresh triggers per §5 above.
- Validation: DTO-to-state mapping handles nulls correctly (Task 01's Hidden-vs-Error distinction).
- Error Handling: Repository failure for a specific section maps to `SectionState.Error` for that section only.
- Security: N/A.
- Performance: Mapping done off main thread.
- Localization: N/A.
- RTL: N/A.
- Analytics: Fires `home_viewed` once per successful full render via a one-shot mechanism, not per state emission.
- Tests: Unit tests for refresh-trigger logic (15-min threshold), per-section error mapping, first-day flag propagation.
- Documentation: KDoc.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Working ViewModel.
- Definition of Done: Unit tests pass.

**Task 03 — Build `HomeScreen` Composable + Section Composables**
- Objective: Root screen composing independent section Composables in fixed order.
- Why Required: Primary UI deliverable of this sub-feature.
- Existing Architecture to Follow: `:core:design-system` tokens; Compose conventions.
- Existing Files to Reuse: `:core:design-system` Surface/card tokens from A.1.
- Files to Create: `HomeScreen.kt`, `components/GreetingStreakHeader.kt` (other section Composables are owned by K-02 through K-06, K-08; K-01 provides the container and the Greeting/Streak header + shimmer skeleton shells)
- Files to Modify: none
- Implementation Details: `LazyColumn` (or equivalent) rendering sections in literal fixed order from `HomeUiState`; each section Composable receives its own `SectionState` slice; shimmer Composable shown for `Loading`; nothing emitted for `Hidden`.
- Business Rules: Order is literal/hardcoded to match FR-1 — not data-driven/configurable.
- Validation: N/A.
- Error Handling: Section-level error composable, non-blocking.
- Security: N/A (covered by Task 05 audit test).
- Performance: Each section reads only its own state slice; `@Stable` data classes minimize recomposition scope.
- Localization: All text via string resources.
- RTL: Verified via `LayoutDirection.Rtl` preview/test.
- Analytics: `home_section_rendered` fired per section on first resolution.
- Tests: Compose UI tests for Loading/Content/Error/Hidden per section shell.
- Documentation: KDoc on `HomeScreen` listing the fixed section order explicitly.
- Dependencies: Tasks 01, 02.
- Do Not Change: Do not make section order client-configurable.
- Expected Result: Rendering HomeScreen.
- Definition of Done: Compose UI tests pass.

**Task 04 — Section-Order Snapshot Test**
- Objective: Build-failing test if section order changes.
- Why Required: PRD §7 item 1 explicit requirement.
- Existing Architecture to Follow: Compose semantics-tree testing conventions.
- Existing Files to Reuse: Task 03 output.
- Files to Create: `HomeScreenSectionOrderTest.kt`
- Files to Modify: none
- Implementation Details: Traverse the semantics tree, assert section test-tags appear in the exact FR-1 order.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: N/A.
- Security: N/A.
- Performance: N/A.
- Localization: N/A.
- RTL: Run this test in both LTR and RTL configurations to confirm order (not just visual direction) is unaffected by RTL mirroring.
- Analytics: N/A.
- Tests: This task is the test.
- Documentation: Comment explaining why this test exists (FR-1 immutability).
- Dependencies: Task 03.
- Do Not Change: N/A.
- Expected Result: Passing order-verification test.
- Definition of Done: Test fails when order is deliberately broken in a scratch branch (verify the test is actually effective), then passes on correct order.

**Task 05 — Content-Safety Regression UI Test**
- Objective: Client-side mirror of B-08's blocklist audit.
- Why Required: PRD §7 item 5 — non-negotiable CI gate for this module.
- Existing Architecture to Follow: Compose semantics-tree text-node traversal.
- Existing Files to Reuse: Fixture state builders from Task 02's tests (free tier, premium tier, first-day, offline).
- Files to Create: Test file under `androidInstrumentedTest` (or shared KMP test source set if UI-testable cross-platform)
- Files to Modify: none
- Implementation Details: Recursively walk rendered semantics tree text nodes across multiple fixture `HomeUiState` values, assert no text node matches the blocklist (case-insensitive): `subscribe, upgrade, $, price, billing, trial, renew`.
- Business Rules: Zero tolerance, mirrors B-08.
- Validation: N/A.
- Error Handling: N/A.
- Security: This IS the control.
- Performance: N/A.
- Localization: Run across fixture states in multiple locales if feasible.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task is the test; include a canary sub-test injecting a billing term into a fixture to confirm the scan actually catches it.
- Documentation: Comment on zero-tolerance policy, cross-reference B-08.
- Dependencies: Task 03.
- Do Not Change: Do not weaken the blocklist without Trust & Safety sign-off (mirrors B-08 rule).
- Expected Result: Passing client-side safety suite.
- Definition of Done: Canary test proves detection works; full fixture matrix passes.

## 30. Definition of Done
`HomeScreen` renders all sections independently in fixed order with correct Loading/Content/Error/Hidden behavior per section; order and content-safety regression tests are CI-blocking and green; module documented.

## 31. Final Verification Checklist
- [ ] Section order matches FR-1 exactly, verified by a build-failing snapshot test
- [ ] Each section state (Loading/Content/Error/Hidden) independently verified via Compose UI tests
- [ ] `HomeUiState`/section models are `@Immutable`/`@Stable`
- [ ] Client-side content-safety regression test passes with a working canary
- [ ] `home_viewed`/`home_section_rendered` analytics fire correctly (once per render/resolution, not per recomposition)
- [ ] RTL layout verified for section order and mirroring
- [ ] Pull-to-refresh and 15-minute background-resume refresh triggers verified
- [ ] No colors/spacing/typography redefined outside `:core:design-system`
