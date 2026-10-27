# K-01 — Splash, Bootstrap & App Update Gating Flow

> **Status:** ✅ **Implemented & Verified** (Live simulator verified on Android `emulator-5554` with live FastAPI backend)

## 1. Feature Context
The very first thing every user sees. Renders the branded Splash, calls B-01's bootstrap endpoint, and routes to the correct downstream destination — or intercepts with Forced Update / Maintenance / No-Connectivity as graph-level gates before any other screen can render.

## 2. Parent Feature
Feature A.1 — Splash, Language Selection, Authentication & Onboarding

## 3. Sub-feature
2.1 Splash, Bootstrap & App Update Gating Flow (ID: **K-01**)

## 4. Objective
Build the `:feature:onboarding` Splash/Bootstrap Compose screens and `SplashViewModel`, calling B-01's `GET /v1/identity/bootstrap` via `core-network`'s `AuthApiService`, with graph-level interceptors for Forced Update, Maintenance, and No-Connectivity — never standard back-stack entries.

## 5. Business Requirements
- FR-1: Determine session validity at launch and route accordingly.
- FR-2: Support forced update (blocking) and recommended update (dismissible) gates evaluated at bootstrap.
- NFR: Splash branded loading, max display 2.5s even if bootstrap is slow — bootstrap continues in background, splash transitions to a lightweight "connecting..." state if it overruns.
- Offline: No network at launch → "No internet connection — retry" with explicit retry control.
- §6.3 (Android Requirements): Forced-update and maintenance screens are graph-level interceptors evaluated before the graph renders, not standard back-stack entries.

## 6. Existing Architecture
`core-navigation`'s `Navigator`/`Route` pattern; `core-network`'s `ConnectivityObserver` and `safeCall` wrapper; `core-ui`'s `BaseViewModel<State,Event>` and `LoadStateContent`; `core-datastore`'s `RemoteConfigRepository` for the 5-minute client-side cache of the `remote_config` portion only.

## 7. Existing Code to Reuse
- `core-network`: `AuthApiService` (add `bootstrap()` method), `ConnectivityObserver`, `safeCall`
- `core-navigation`: `Navigator`, `Route` sealed interface
- `core-ui`: `BaseViewModel<State, Event>`, `LoadStateContent`, `ErrorBoundary`
- `core-datastore`: `RemoteConfigRepository`, `PreferenceManager`
- `core-common`: `NoorResult<T>`, `AppError` hierarchy
- `core-designsystem`: `NoorHeroesTheme`, `fluidDp`

## 8. Files to Create
- `feature/onboarding/ui/SplashScreen.kt`
- `feature/onboarding/ui/ForcedUpdateScreen.kt`
- `feature/onboarding/ui/RecommendedUpdateBanner.kt` (composable, not a full screen)
- `feature/onboarding/ui/MaintenanceModeScreen.kt`
- `feature/onboarding/ui/NoConnectivityScreen.kt`
- `feature/onboarding/viewmodel/SplashViewModel.kt`, `SplashState.kt`, `SplashEvent.kt`
- `feature/onboarding/navigation/OnboardingGraphInterceptor.kt` — evaluates Forced Update/Maintenance before the nav graph renders
- `core-network/api/BootstrapDto.kt` — `BootstrapResponseDto`, `RemoteConfigDto`
- `feature/onboarding/data/BootstrapRepository.kt` (or extend existing `AuthRepository` if bootstrap logically belongs there)
- `test/feature/onboarding/SplashViewModelTest.kt`
- `androidTest/feature/onboarding/SplashScreenTest.kt`

## 9. Files to Modify
- `core-network/api/AuthApiService.kt` — add `suspend fun bootstrap(appVersion: String, platform: String, locale: String?): NoorResult<BootstrapResponseDto>`
- `core-navigation/Route.kt` — add `SplashRoute`, `ForcedUpdateRoute`, `MaintenanceModeRoute`, `NoConnectivityRoute` (all `data object`, `requiredAuthState` = unauthenticated-compatible since this precedes auth entirely)

## 10. KMP Requirements
- `SplashViewModel` calls `BootstrapRepository.fetchBootstrap()` on init via `launchSafely`; enforces the 2.5s max-display cap via a parallel `delay(2500)` race — whichever resolves first drives the UI transition, but the actual bootstrap call continues in the background regardless (never cancelled by the timeout).
- Routing decision matrix: `session_valid && has_children` → `ProfilePickerRoute`; `session_valid && !has_children` → `AddChildRoute`; `!session_valid` → `LanguageSelectionRoute` (K-02).
- Forced update (HTTP 426 from bootstrap, or `maintenance_mode` 503): render as a graph-level interceptor via `OnboardingGraphInterceptor`, evaluated before `NavHost` composition — no back button, no dismiss.
- Recommended update: dismissible banner overlay, state persisted in-memory only (per-session), reappears next app launch if dismissed (do not persist "dismissed" to DataStore — must reappear next session per PRD).
- `ConnectivityObserver.observeConnectivity()` drives `NoConnectivityScreen` display — do not rely on request timeout alone (§6.7 requirement).
- Cache only the `remote_config` sub-object client-side via `RemoteConfigRepository`, 5-minute TTL; `session_valid`/`has_children` are never cached.

## 11. Required API
- `GET /v1/identity/bootstrap` (B-01) — headers `X-App-Version`, `X-Platform`, `X-Locale`, optional `Authorization`.

## 12. Offline First
Splash/Bootstrap is the one screen in this feature that must gracefully degrade fully offline: bundled Splash asset renders regardless of connectivity; `ConnectivityObserver` short-circuits straight to `NoConnectivityScreen` if offline at launch, without waiting for a request timeout.

## 13. Local Data
No local draft data at this stage (that begins at K-02/K-07). `RemoteConfigRepository`'s 5-minute cache is the only local state here.

## 14. Localization
Locale is passed via `X-Locale` header (resolved from the OS/previously-persisted preference) but Splash itself has no user-facing text beyond the brand lockup — full localization begins at K-02.

## 15. RTL
N/A for Splash itself (logo-only); Forced Update/Maintenance/No-Connectivity screens must support full RTL mirroring per the Global Design System rules.

## 16. Analytics
Emit `app_splash_viewed` (platform, app_version, locale) on screen entry; `bootstrap_completed`/`bootstrap_failed` are emitted server-side by B-01 — do not double-emit from the client; `forced_update_blocked` (current_version, min_supported_version) client-side when the interceptor renders.

## 17. Performance
- Splash hard-capped at 2.5s display regardless of bootstrap latency.
- Cold start to Splash render target < 1.5s on low-end Android — verify no heavy synchronous work (DI graph construction, DataStore reads) blocks the first frame.
- Avoid unnecessary recomposition during the bootstrap-pending → routed transition (stable `SplashState`).

## 18. Security
No certificate-pinning logic here (handled by `core-network`'s existing `HttpClientEngine` config) — confirm bootstrap calls go through the same pinned client as all other API calls, not a bypassed unpinned client for "just the launch call."

## 19. Testing
- Unit (`SplashViewModelTest`): all four routing-decision branches; 2.5s-cap-vs-slow-bootstrap race behavior; forced-update/maintenance short-circuit before other routing logic.
- UI (`SplashScreenTest`): Loading/Content/Error state rendering; `NoConnectivityScreen` retry control triggers a fresh bootstrap call.
- Accessibility: not a primary concern for Splash itself, but Forced Update/Maintenance/No-Connectivity screens need standard `contentDescription` coverage.

## 20. AI Coding Agent Implementation Steps

**Task 01 — Add `bootstrap()` to `AuthApiService` and DTOs**
Objective: Network-layer contract for B-01. Follow: existing `safeCall` wrapper pattern in `core-network`. Files to Create: `BootstrapDto.kt`. Files to Modify: `AuthApiService.kt`. Tests: DTO (de)serialization test against the exact B-01 JSON shape. Definition of Done: DTO round-trips correctly against sample payloads for both authed and unauthed responses.

**Task 02 — Add New Routes to `core-navigation`**
Objective: `SplashRoute`, `ForcedUpdateRoute`, `MaintenanceModeRoute`, `NoConnectivityRoute`. Follow: existing `Route` sealed-interface pattern with `analyticsName`. Files to Modify: `Route.kt`. Definition of Done: all four routes compile and are `@Serializable`.

**Task 03 — Implement `BootstrapRepository`**
Objective: Repository wrapping `AuthApiService.bootstrap()` plus `RemoteConfigRepository` cache-write. Follow: `core-data` repository pattern. Files to Create: `BootstrapRepository.kt`. Tests: cache-write-on-success, cache-untouched-on-failure. Dependencies: Task 01. Definition of Done: repository correctly separates cacheable (`remote_config`) from non-cacheable (`session_valid`) fields.

**Task 04 — Implement `SplashViewModel`**
Objective: Orchestrate the 2.5s-cap race, routing-decision matrix, and error states. Follow: `BaseViewModel<SplashState, SplashEvent>`, `launchSafely`. Business Rules: bootstrap call is never cancelled by the display-cap timeout. Tests: full routing matrix + race-condition tests. Dependencies: Task 03. Definition of Done: all unit tests in §19 pass.

**Task 05 — Implement Splash/ForcedUpdate/Maintenance/NoConnectivity Composables**
Objective: Build the four screens per the Global Design System tokens (`NoorHeroesTheme`, no hardcoded colors/spacing). Files to Create: four Composable files. Accessibility: `contentDescription` on all interactive elements, 44dp min touch targets via `Modifier.noorHeroesTouchTarget()`. RTL: verified via `LayoutDirection` preview variants. Tests: `SplashScreenTest` per §19. Dependencies: Task 04. Definition of Done: Compose UI tests pass in both LTR and RTL preview configurations.

**Task 06 — Implement `OnboardingGraphInterceptor`**
Objective: Evaluate Forced Update/Maintenance before `NavHost` composition, not as back-stack entries. Follow: existing `NavigationHandler` pattern in the app-root/shared module. Files to Create: interceptor file. Business Rules: no back button, no dismiss on Forced Update/Maintenance. Tests: interceptor short-circuits normal graph rendering when either condition is true. Dependencies: Task 04. Definition of Done: back-press is fully inert on Forced Update/Maintenance screens (verified by test).

**Task 07 — Wire `ConnectivityObserver` for No-Connectivity Detection**
Objective: Short-circuit to `NoConnectivityScreen` on offline detection, not timeout-only. Follow: existing `ConnectivityObserver.observeConnectivity()` Flow. Tests: simulated offline-at-launch scenario. Dependencies: Task 04. Definition of Done: offline detection happens before any bootstrap network timeout would have fired.

**Task 08 — Add Analytics Instrumentation**
Objective: Emit `app_splash_viewed`, `forced_update_blocked` via `AnalyticsTracker`. Follow: `core-analytics` injection pattern (ViewModel-only, never duplicated in Composables). Tests: fake-tracker assertion tests. Dependencies: Task 04. Definition of Done: exactly one call site per event, in the ViewModel.

**Task 09 — Add Full Test Suite**
Objective: Complete unit + UI test coverage per §19. Definition of Done: all green, including Robolectric/Espresso if used for the interceptor test.

**Task 10 — Final Code Review**
Objective: Confirm no business logic leaked into Composables, no hardcoded design tokens, cache separation (cacheable vs never-cached fields) correctly implemented. Definition of Done: checklist in §21 checked.

## 21. Final Verification Checklist
- [x] Splash hard-capped at 2.5s display; bootstrap call itself never cancelled by the cap
- [x] Routing matrix (4 branches) fully covered by tests
- [x] Forced Update/Maintenance render as graph-level interceptors, not back-stack entries — back press inert
- [x] Recommended Update dismissal is session-only (reappears next launch), not persisted
- [x] `NoConnectivityScreen` triggered by `ConnectivityObserver`, not timeout-only
- [x] Only `remote_config` cached client-side (5 min); `session_valid`/`has_children` never cached
- [x] `app_splash_viewed`/`forced_update_blocked` emitted exactly once each, from the ViewModel only
- [x] Full RTL support verified on all four screens
- [x] Cold start to Splash render measured < 1.5s on a low-end device profile

## 22. Definition of Done
Splash/Bootstrap flow is live, correctly routes all four session/children combinations, blocks on forced update and maintenance without a bypass, degrades gracefully offline, and hands off cleanly to K-02 (unauthenticated) or K-08 (authenticated with children) or K-06 (authenticated, no children). **(STATUS: IMPLEMENTED & VERIFIED)**
