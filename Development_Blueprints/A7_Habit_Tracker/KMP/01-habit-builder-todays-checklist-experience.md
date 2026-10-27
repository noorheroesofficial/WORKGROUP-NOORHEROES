# K-01 — Habit Builder — Today's Checklist Experience

## 1. Feature Context
NoorHeroes KMP app (Android/iOS). Primary screen for Feature A.7 — Habit Tracker: today's parent-enabled habit checklist with per-row independent optimistic state.

## 2. Parent Feature
A.7 Habit Tracker — KMP App (Android/iOS)

## 3. Sub-feature
K-01 Habit Builder — Today's Checklist Experience

## 4. Objective
Build the Habit Builder screen rendering today's checklist, with `HabitChecklistViewModel` capturing `local_date`/`timezone` synchronously at tap time and per-row independent optimistic state, backing FR-1, FR-2, FR-5.

## 5. Business Requirements
- Show only parent-enabled, age-appropriate habits (FR-5), scoped by B-01's `GET /v1/habits`.
- Tap-to-local-update latency < 100ms (NFR Performance) — instantaneous optimistic feedback.
- Each row's optimistic state is independent — tapping one habit must not disable/loading-state any other row.
- Default, all-complete (calm celebratory), partial, Mercy-Day-active, offline, and empty states all rendered distinctly.
- Full accessibility labeling per row including current check-in state.

## 6. Existing Architecture
NoorHeroes KMP app: Clean Architecture, Compose Multiplatform UI, **Koin** for DI (not Hilt — this corrects the PRD draft's Android-only Hilt assumption; Koin is the project's actual multiplatform DI per `core-common`'s `di` package), **Ktor** for networking (not Retrofit+OkHttp — per `core-network`), **Room** for local caching (per `core-database`, KMP-multiplatform with `BundledSQLiteDriver`, not Android-only Room), navigation via the project's custom `Navigator`/`Route`/`NavigationAction` pattern (per `core-navigation`, not raw Compose `NavController`), analytics via the `AnalyticsTracker` interface (`logEvent(name, params)`, per `core-analytics`). New feature module: `feature-habits` (UI) + `feature-habits-domain` (use cases), following the existing `feature-onboarding`/`feature-onboarding-domain` and `feature-learn`/`feature-learn-domain` naming convention.

**Reconciliation note:** `feature/home` already contains a simplified `HabitChecklistWidget.kt`/`HabitRepository.kt` (A2 blueprint K-03) and `feature/dua-learning` contains `HabitReminderSuggestionCard.kt` (A6 blueprint K-05), both built against a simplified check-in contract (`{habit_id, date, client_event_id}` → `{checked, current_streak, xp_awarded}`). This sub-feature establishes the canonical `feature-habits-domain` repository against B-01/B-02's full contract (`local_date`, `timezone`, `source`, `note_category`, `client_request_id` → `reward{xp,noor_points}`, `daily_cap_reached`, `streak{current,state}`). The Home widget and Dua reminder card should be refactored in a follow-up to consume `feature-habits-domain`'s repository rather than maintaining parallel implementations — flag this refactor explicitly rather than silently duplicating logic.

## 7. Existing Code to Reuse
- `core-common` `di`/`error`/`result`/`datetime` packages
- `core-network` Ktor client setup
- `core-database` Room/`BundledSQLiteDriver` setup
- `core-navigation` `Navigator`/`Route` pattern
- `core-analytics` `AnalyticsTracker`
- `core-design-system` tokens (non-alarming streak iconography, per PRD §2.1)

## 8. Files to Create
- `feature-habits/src/commonMain/kotlin/.../checklist/HabitBuilderScreen.kt` (Composable)
- `feature-habits/src/commonMain/kotlin/.../checklist/HabitChecklistViewModel.kt`
- `feature-habits/src/commonMain/kotlin/.../checklist/HabitChecklistUiState.kt` (`Map<habitId, RowState>`, not a single screen-wide loading flag)
- `feature-habits/src/commonMain/kotlin/.../data/HabitRepository.kt`
- `feature-habits-domain/src/commonMain/kotlin/.../GetTodaysHabitsUseCase.kt`
- `feature-habits-domain/src/commonMain/kotlin/.../CheckInHabitUseCase.kt`
- `feature-habits/src/commonTest/kotlin/.../HabitChecklistViewModelTest.kt` (fake-clock tap-time capture test)
- `feature-habits/src/androidInstrumentedTest/kotlin/.../HabitBuilderScreenUiTest.kt`

## 9. Files to Modify
- App-level Koin module registration — wire `feature-habits`/`feature-habits-domain` DI graph
- `core-navigation` `Route` registry — add Habit Builder route
- Deep-link handler (owned by K-07) — route `noorheroes://habits` here

## 10. Backend Requirements
Consumes `GET /v1/habits` (B-01), `POST /v1/habits/check-ins` (B-02).

## 11. KMP Requirements
- `HabitChecklistViewModel` captures `LocalDate.now()`/`TimeZone.currentSystemDefault()` (kotlinx-datetime, multiplatform-correct API — not `java.time`/`TimeZone.getDefault()` which are JVM/Android-only) **synchronously in the tap handler**, not in a later coroutine that could execute after a delay.
- Per-row optimistic state via `Map<habitId, RowState>` in `HabitChecklistUiState`, not a screen-wide loading flag.
- Streak summary chip, "View Streak History" (→ K-04) and "Open Noor Garden" (→ K-05) navigation via `Navigator`.
- Tablet layout with persistent Noor Garden preview panel (responsive Compose layout).
- Full accessibility labeling: "Fajr prayer, not yet checked in today" pattern per row.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
`GET /v1/habits?child_id=` (B-01) — `POST /v1/habits/check-ins` (B-02, actual write delegated to K-06's offline outbox).

## 14. Database Requirements (Local)
Room table `habit_catalog_cache` mirroring the last-fetched `GET /v1/habits` response for offline/instant-load display; not the write path (write path is K-06's separate outbox table).

## 15. Validation
Unit test using a fake `Clock`/`TimeZone` provider that advances time between tap and request-send, asserting the request payload reflects tap-time date, not send-time date (mandatory, per PRD §7 Android prompt item 1).

## 16. Authentication
Reuses shared `core-network` Bearer token attachment (child-mode session).

## 17. Authorization
N/A at UI layer (enforced server-side, B-01/B-02).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Network failure on catalog load | Show cached `habit_catalog_cache` with a small persistent offline indicator |
| Zero habits configured | Friendly "ask a grown-up to set up your first habit" empty state with parent deep link |
| Check-in tap while offline | Delegated to K-06's outbox; row shows optimistic-pending state, not an error |

## 19. Offline First
Catalog read is cached locally (§14); check-in writes are fully offline-capable via K-06's outbox — this screen only owns the optimistic-UI and cached-read behavior, not the outbox mechanics itself.

## 20. Local Data
```
Remote Data (GET /v1/habits)
   ↓
HabitRepository
   ↓
Room habit_catalog_cache
   ↓
HabitChecklistUiState (per-row optimistic overlay)
```

## 21. Localization
Habit labels resolved via string resources / backend-provided translation keys (English, Hindi, Arabic, Urdu) — no hardcoded user-facing strings.

## 22. RTL
Checklist row layout (icon + label + checkbox) mirrors correctly; verified via a dedicated RTL layout test.

## 23. Analytics
`habit_builder_viewed`, `habit_checked_in`, `habit_checkin_duplicate_ignored` (fired based on the `was_duplicate` response flag from B-02) via `AnalyticsTracker.logEvent()`.

## 24. Performance
Row-scoped recomposition only (per-row `RowState` keys prevent whole-list recomposition on a single tap); tap-to-local-update latency budget < 100ms.

## 25. Security
No new sensitive data handling at this layer.

## 26. Library Requirements
Compose Multiplatform, Koin, Ktor, Room (`BundledSQLiteDriver`), kotlinx-datetime, kotlinx-coroutines.

## 27. Testing
- Unit: fake-clock tap-time capture test (mandatory).
- Unit: per-row independent optimistic state (tapping one row doesn't affect another's `RowState`).
- UI: empty state, all-complete state, offline indicator rendering.
- Accessibility: row content-description correctness test.

## 28. Documentation
KDoc on `HabitChecklistViewModel` explicitly explaining why tap-time capture must be synchronous (ties to B-02's client-trusted `local_date` design).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Scaffold `feature-habits`/`feature-habits-domain` Modules**
- Objective: Establish the new feature module pair.
- Why Required: No dedicated Habit Tracker module exists yet; current habit code is scattered across `feature/home` and `feature/dua-learning`.
- Existing Architecture to Follow: `feature-learn`/`feature-learn-domain` module-pair convention.
- Files to Create: module `build.gradle.kts` files, package skeleton.
- Files to Modify: root `settings.gradle.kts` to register new modules; Koin app-module registration.
- Dependencies: `core-common`, `core-network`, `core-database`, `core-design-system`, `core-navigation`, `core-analytics`.
- Definition of Done: modules compile and are wired into the app's DI graph.

**Task 02 — Implement `GetTodaysHabitsUseCase` + `HabitRepository`**
- Objective: Domain-layer read of today's catalog.
- Existing Architecture to Follow: repository pattern from `core-data`/`CORE_DATA_INSTRUCTIONS.md`.
- Files to Create: `HabitRepository.kt`, `GetTodaysHabitsUseCase.kt`
- Implementation Details: Ktor call to `GET /v1/habits`, cached to Room `habit_catalog_cache`.
- Tests: repository unit tests (mocked Ktor client).
- Definition of Done: use case returns correctly-cached, correctly-mapped domain model.

**Task 03 — Implement `HabitChecklistViewModel` with Tap-Time Capture**
- Objective: Core ViewModel logic including the fake-clock-testable tap-time capture.
- Files to Create: `HabitChecklistViewModel.kt`, `HabitChecklistUiState.kt`
- Implementation Details: `Map<habitId, RowState>`; synchronous `LocalDate`/`TimeZone` capture in tap handler.
- Business Rules: tap-time capture must not be deferred to a coroutine.
- Tests: mandatory fake-clock test (§15).
- Do Not Change: do not move date/timezone capture into an async block.
- Definition of Done: fake-clock test passes.

**Task 04 — Build `HabitBuilderScreen` Composable**
- Objective: UI implementation of all documented states.
- Existing Files to Reuse: `core-design-system` streak/gold-fill tokens.
- Files to Create: `HabitBuilderScreen.kt`
- Implementation Details: checklist rows, streak chip, empty/offline/all-complete states, tablet layout variant.
- Localization/RTL: per §21/§22.
- Analytics: `habit_builder_viewed` on screen entry.
- Tests: Compose UI tests for each state.
- Definition of Done: all documented states render correctly, accessibility labels verified.

**Task 05 — Wire Navigation & Deep Link Registration**
- Files to Modify: `core-navigation` `Route` registry.
- Dependencies: coordinates with K-07 for `noorheroes://habits` deep link.
- Definition of Done: screen reachable via Home widget deep link and direct navigation.

**Task 06 — Final Code Review**
- Do Not Change: existing `feature/home`/`feature/dua-learning` habit code should be flagged for refactor, not silently deleted, in this task — coordinate removal with a follow-up ticket once consumers are repointed.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Habit Builder screen live with correct tap-time capture, per-row optimistic state, all documented UI states, full accessibility/localization/RTL support.

## 31. Final Verification Checklist
- [ ] `feature-habits`/`feature-habits-domain` modules scaffolded and DI-wired
- [ ] Tap-time `LocalDate`/`TimeZone` capture is synchronous (fake-clock test passes)
- [ ] Per-row optimistic state independent (no whole-list recomposition on single tap)
- [ ] All documented states (default, all-complete, partial, Mercy-Day, offline, empty) render correctly
- [ ] Accessibility labels correct per row
- [ ] Localization (EN/HI/AR/UR) and RTL verified
- [ ] Analytics events wired via `AnalyticsTracker`
- [ ] Existing `feature/home`/`feature/dua-learning` habit code flagged for follow-up refactor, not silently duplicated
