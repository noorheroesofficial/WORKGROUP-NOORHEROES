# K-01 — Controls Landing & Module Navigation

## 1. Feature Context
Controls is reached from the Parent Dashboard's module shortcut grid and fans out into five focused sub-screens (Screen Time, Bedtime, AI Permissions, Content Age Level, Child Locks & Sessions). This sub-feature owns the landing list and its navigation wiring only (PRD C.23 §1.18 Screen #1, §2.4).

## 2. Parent Feature
Feature C.23 — Parental Controls (Screen Time, Bedtime, AI Permissions, Content Age Level)

## 3. Sub-feature
2.1 Controls Landing & Module Navigation (ID: **K-01**)

## 4. Objective
Build `ControlsLandingScreen` as the entry point into the `:feature:parental-controls` module, with type-safe `Route`s for every sub-screen and deep-link support, following the platform's "one clear focus per screen" navigation philosophy.

## 5. Business Requirements
- FR-1: Controls area sections reached under Parent Area → Controls (Screen Time, Quiet Hours/Bedtime, AI Permissions, Content Age Level, plus Child Locks & Sessions).
- §2.4: simple settings-list landing leading into focused single-purpose sub-screens.
- §6.8: deep links `noorheroes://parent/controls/screen-time`, `.../bedtime`, `.../ai-permissions`, `.../content-age-level`, `.../child-locks`.

## 6. Existing Architecture
New module `:feature:parental-controls`, depends on `:core:navigation` (`Navigator`, `Route`), `:core:design-system`, `:core:auth` (for `requiredAuthState` guard = Parent Mode). Reached from C.20's Parent Dashboard module shortcut grid via `navigator.navigateTo(ControlsLandingRoute)`.

## 7. Existing Code to Reuse
- `core-navigation::Navigator`, `Route` (sealed interface)
- `core-navigation::BaseAuthState.Parent` (for `requiredAuthState`)
- `core-design-system` list/card components (confirm exact component names against the design-system module before inventing new ones)
- C.20's Parent Dashboard shortcut grid (entry point — modify to add a Controls tile if not already present)

## 8. Files to Create
- `feature/parental-controls/src/commonMain/kotlin/.../navigation/ControlsRoutes.kt` — `ControlsLandingRoute`, `ScreenTimeSettingsRoute`, `BedtimeSettingsRoute`, `AiPermissionsSettingsRoute`, `ContentAgeLevelSettingsRoute`, `ChildLocksAndSessionsRoute` (all `@Serializable data class`/`data object` per child, taking `childId: String` where applicable)
- `feature/parental-controls/src/commonMain/kotlin/.../ui/ControlsLandingScreen.kt`
- `feature/parental-controls/src/commonMain/kotlin/.../viewmodel/ControlsLandingViewModel.kt`
- `feature/parental-controls/src/commonMain/kotlin/.../di/ParentalControlsModule.kt` (Koin)
- `feature/parental-controls/src/commonTest/kotlin/.../ControlsLandingViewModelTest.kt`

## 9. Files to Modify
- App-level deep-link router registration — add the five `noorheroes://parent/controls/*` patterns mapping to the routes above
- C.20 Parent Dashboard module grid — add a "Controls" entry point tile if not already wired

## 10. KMP Requirements
- `ControlsLandingViewModel`: exposes a simple static list of five navigable entries (no network call needed for the landing list itself — it's a static menu); each entry navigates via `navigator.value.navigateTo(route)`.
- `ControlsLandingScreen` Composable: renders the five entries as list items using existing `core-design-system` list components; each item's `analyticsName` fires `controls_landing_viewed` on screen entry (via `LaunchedEffect`) and a per-item-tap event on navigation.
- Auth guard: `ControlsLandingRoute.requiredAuthState = BaseAuthState.Parent::class` — unreachable outside Parent Mode.

## 11. API Contract
N/A — this screen makes no network calls; each sub-screen owns its own API calls per K-02 through K-06.

## 12. Database Requirements
N/A.

## 13. Validation
N/A (static navigation menu).

## 14. Authentication
Route-level guard via `requiredAuthState = BaseAuthState.Parent::class`.

## 15. Authorization
N/A beyond Parent Mode guard (per-child authorization happens in each sub-screen once a child context is selected).

## 16. Error Handling
N/A — no data fetching on this screen.

## 17. Offline First
Fully available offline (static navigation).

## 18. Local Data
N/A.

## 19. Localization
All five entry labels and any descriptive subtext sourced from the shared string resources (EN/HI/AR/UR) — no hardcoded strings.

## 20. RTL
List layout must mirror correctly in RTL (Arabic/Urdu) via the design system's RTL-aware list component.

## 21. Analytics
`controls_landing_viewed` on screen entry.

## 22. Performance
Trivial static screen; no special performance concerns. Use `@Immutable` state per `core-common` conventions to avoid unnecessary recomposition.

## 23. Security
N/A beyond the Parent Mode route guard.

## 24. Library Requirements
Jetpack Compose, Koin (DI), `core-navigation`, `core-design-system`. No new third-party dependencies.

## 25. Testing
- Unit: `ControlsLandingViewModel` navigation-intent emission for each of the five entries.
- UI test: all five entries render with correct localized labels in EN and one RTL locale (AR).
- UI test: deep link `noorheroes://parent/controls/screen-time` lands directly on `ScreenTimeSettingsScreen`, bypassing the landing list.

## 26. Documentation
KDoc on `ControlsRoutes.kt` documenting each route's required `childId` parameter contract (per `core-navigation`'s "pass IDs, not large objects" rule).

## 27. AI Coding Agent Implementation Steps

**Task 01 — Define Route Sealed Classes**
- Files to Create: `navigation/ControlsRoutes.kt`
- Implementation Details: Each route `@Serializable`, sets `requiredAuthState` and `analyticsName` per `core-navigation`'s `Route` interface contract.

**Task 02 — Register Deep Links**
- Files to Modify: app-level deep-link router.
- Implementation Details: Map the five `noorheroes://parent/controls/*` URIs to the corresponding `Route`s.

**Task 03 — Implement `ControlsLandingViewModel`**
- Files to Create: `viewmodel/ControlsLandingViewModel.kt`
- Implementation Details: Static entry list; `onEntryClicked(entry)` calls `navigator.value.navigateTo(route)`.

**Task 04 — Implement `ControlsLandingScreen` Composable**
- Files to Create: `ui/ControlsLandingScreen.kt`
- Implementation Details: Use existing design-system list/card components; fire `controls_landing_viewed` via `LaunchedEffect(Unit)`.

**Task 05 — Register Koin Module**
- Files to Create: `di/ParentalControlsModule.kt`

**Task 06 — Add Entry Point in Parent Dashboard**
- Files to Modify: C.20's dashboard shortcut grid.

**Task 07 — Add Unit Tests**
- Files to Create: `ControlsLandingViewModelTest.kt`

**Task 08 — Add UI/Deep-Link Tests**

**Task 09 — Add Localization Strings**
- Implementation Details: Add EN/HI/AR/UR entries for all five labels to the shared string resources.

**Task 10 — Final Code Review**
- Objective: Confirm no business logic leaked into this landing screen (it should remain a pure navigation menu).

## 28. Definition of Done
- All five entries navigate correctly.
- Deep links land on the correct destination screen directly.
- Fully localized and RTL-correct.
- `controls_landing_viewed` fires exactly once per screen entry.

## 29. Final Verification Checklist
- [ ] All five routes defined with correct `requiredAuthState`/`analyticsName`
- [ ] Deep links tested for all five patterns
- [ ] No hardcoded strings
- [ ] RTL layout verified
- [ ] Entry point wired from C.20 dashboard
- [ ] Unit + UI tests green
