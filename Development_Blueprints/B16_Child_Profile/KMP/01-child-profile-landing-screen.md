# K-01 — Child Profile Landing Screen

## 1. Feature Context
The Profile bottom-nav tab's landing screen: a personal, glanceable hub composing avatar thumbnail, stats summary, language toggle, Favorites/Downloads entry, and Switch Profile row. This is the composition/orchestration shell that K-02, K-03, and K-04 plug into.

## 2. Parent Feature
Feature B.16 — Child Profile (Bottom Tab)

## 3. Sub-feature
2.1 Child Profile Landing Screen & Navigation Hub (ID: **K-01**)

## 4. Objective
Build `ChildProfileScreen`/`ChildProfileViewModel` with `child_id` derived exclusively from the active session, correct empty/loading/offline/disabled-session states, and navigation wiring into Avatar (A.12) and Favorites & Downloads (B.14/B.15) — without reimplementing either destination.

## 5. Business Requirements
- FR-1: Sections are avatar thumbnail, learning stats summary, language toggle, Switch Profile, Favorites/Downloads entry — canonical section list, nothing added or omitted.
- FR-4: A child cannot see sibling stats from this screen via any UI path.
- FR-9: Switching to another child/Parent Mode clears all previous child-sensitive UI state before the new session activates.
- FR-10: "Edit avatar" deep-links into the Avatar screen (A.12); Profile does not reimplement avatar customization.
- Empty State: new child, zero progress → "Start learning to see your progress here!" framing, not a blank/zero state.
- Loading State: skeleton avatar/stats shimmer on initial load, cached-then-background-refresh on subsequent visits.
- Offline State: renders from cached avatar/stats data; Favorites/Downloads remain functional per their own offline specs.

## 6. Existing Architecture
Mirrors B.14 (Favorites)'s established "repository derives id internally" pattern per PRD §6.4 — `ChildProfileViewModel` must not accept `child_id` as a navigation argument from any external source. Reuses `:core:auth`'s session provider (same one used by B.14) and `:core:navigation`'s existing bottom-nav `Route` structure.

## 7. Existing Code to Reuse
- `:core:auth` — session provider exposing the active child's `child_id` internally
- `:core:navigation` — existing `Route` sealed hierarchy, bottom-nav tab wiring
- `:core:design-system` — `NoorHeroesTheme`, card/skeleton components
- `:core:data` — `SyncQueue`-aware repository conventions (though this screen itself has no write actions beyond K-03's locale patch)
- A.12's Avatar screen route (deep-link target, not reimplemented)
- B.14/B.15's Favorites & Downloads screen shell route (navigation target, not reimplemented)

## 8. Files to Create
- `feature/profile/ui/ChildProfileScreen.kt`
- `feature/profile/ui/components/AvatarThumbnail.kt`
- `feature/profile/ui/components/FavoritesDownloadsEntryRow.kt`
- `feature/profile/viewmodel/ChildProfileViewModel.kt` (+ `ChildProfileUiState`, `ChildProfileEvent`)
- `feature/profile/data/ProfileRepository.kt` (interface) — full implementation shared with K-02/K-03
- `feature/profile/data/ProfileRepositoryImpl.kt`
- `test/feature/profile/ChildProfileViewModelTest.kt`
- `androidTest/feature/profile/ChildProfileScreenTest.kt`

## 9. Files to Modify
- `core-navigation/Route.kt` — add `ProfileRoute` (bottom-nav Tab 5 of 5) if not already present as a placeholder
- `core-data/di/RepositoryModule.kt` — register `ProfileRepositoryImpl`

## 10. KMP Requirements
- `ChildProfileViewModel` derives `child_id` **exclusively** from `:core:auth`'s session provider in its constructor/init — no public method on `ProfileRepository` or the ViewModel accepts an external `child_id` parameter (structural test required, mirroring B.14's exact reflection-based test pattern).
- Avatar thumbnail tap navigates to A.12's existing Avatar screen route — no avatar-editing UI is implemented within `:feature:profile`.
- Favorites/Downloads entry row navigates to the shared B.14/B.15 screen shell route — Profile does not duplicate that screen's content.
- First-time/zero-progress empty state rendered when the stats summary (from K-02) reports no progress yet — friendly framing, not a stark blank.
- Disabled-session redirect: on receiving a `409 SESSION_INVALID`-mapped signal from any Profile-owned API call (via K-02's repository call to B-01), gracefully navigate to Who Is Learning rather than showing an error screen or crashing (Edge Case 9).
- On Switch-Profile-success to a **different** child (handled by K-04's gate flow), `ChildProfileViewModel`'s cached/in-memory state for the previous child must be fully cleared before the new session's Profile renders — verified by a dedicated state-clearing test.
- Skeleton loading state on first composition; subsequent visits show cached data immediately with a background refresh indicator, not a blocking spinner.

## 11. Required API
- `GET /v1/children/{id}/progress` (B-01) — via K-02's `ProfileRepository.getProgressSummary()`, `id` derived internally
- No direct API call from `ChildProfileViewModel` itself beyond orchestrating K-02's and K-03's repository calls

## 12. Offline First
```
Remote (B-01 GET /v1/children/{id}/progress)
    ↓
ProfileRepository (K-02)
    ↓
Room cache
    ↓
ChildProfileScreen (renders from cache when offline)
```
Avatar and Favorites/Downloads entry rows remain tappable and route correctly offline — no special offline handling needed for pure navigation entries beyond their destination screens' own offline specs.

## 13. Local Data
Cached progress summary (Room, owned by K-02's repository implementation) and cached `display_locale` (owned by K-03) are both surfaced through this screen's composed `ChildProfileUiState` — the landing screen itself persists no additional local state beyond simple UI-transient values (scroll position, etc.).

## 14. Localization
All static labels (section headers, empty-state copy, "Switch Profile, requires parent PIN" accessible label) sourced from the shared localization/string-resource system — no hardcoded English fallback strings in `ChildProfileScreen.kt`.

## 15. RTL
Single-column mobile layout mirrors correctly in RTL (avatar/stats/toggle/entries stack order preserved, horizontal element mirroring only where directionally meaningful, e.g., chevron icons). Tablet's side-by-side stats/Favorites-Downloads layout also mirrors correctly.

## 16. Analytics
Emit `child_profile_viewed` on screen composition, `child_profile_avatar_tapped` on avatar navigation, `child_profile_favorites_downloads_tapped` on entry-row navigation, `disabled_session_redirect_triggered` (internal/integrity signal) on the disabled-session redirect path.

## 17. Performance
`ChildProfileUiState` must be stable/immutable (data class with `@Immutable`/`@Stable` annotations as appropriate) to prevent unnecessary recomposition of unrelated sections when only the stats-summary sub-state changes (K-02 updates independently). No main-thread blocking on session/state derivation.

## 18. Security
`child_id` is never accepted as an external parameter anywhere in `:feature:profile`'s public API surface (constructor injection from `:core:auth` only) — the single most important structural guarantee for this module, since it structurally prevents any caller (including a malicious/buggy navigation argument) from requesting a different child's data.

## 19. Testing
- Unit: reflection-based structural test confirming no public method on `ProfileRepository` or `ChildProfileViewModel` accepts a `child_id` parameter (mirrors B.14's exact pattern).
- Unit: state-clearing test — simulate Switch-Profile-success to a different child, assert `ChildProfileViewModel`'s new state contains zero residual data from the previous child.
- UI: first-time/zero-progress empty state renders correct copy; skeleton-then-cached-then-refreshed loading sequence; disabled-session redirect navigates to Who Is Learning without a crash or error flash.
- UI: avatar tap and Favorites/Downloads tap navigate to the correct destinations with correct analytics events fired.

## 20. AI Coding Agent Implementation Steps

**Task 01 — Define `ProfileRepository` Interface**
Objective: Shared contract consumed by K-01/K-02/K-03. Why: single repository avoids duplicated session-derivation logic across sub-features. Follow: `core-data` repository interface conventions. Files to Create: `ProfileRepository.kt`. Definition of Done: interface declares `getProgressSummary()`, `updateLocale()`, `observeCachedSummary()` — no method accepts `child_id`.

**Task 02 — Implement `ProfileRepositoryImpl` (Session-Derived `child_id`)**
Objective: Concrete implementation deriving `child_id` from `:core:auth` in its constructor. Follow: `AuthRepository`'s existing session-provider access pattern. Files to Create: `ProfileRepositoryImpl.kt`. Files to Modify: `RepositoryModule.kt` (DI registration). Tests: structural reflection test. Dependencies: Task 01. Definition of Done: `child_id` is a `private val` resolved once from the session provider, never a method parameter.

**Task 03 — Implement `ChildProfileViewModel`**
Objective: Orchestrate composed UI state from `ProfileRepository`, handle loading/empty/offline/disabled-session states. Follow: `BaseViewModel`, `StateFlow<ChildProfileUiState>` pattern per PRD §6.2. Files to Create: `ChildProfileViewModel.kt`. Business Rules: state-clearing on child switch. Tests: state-clearing test, disabled-session redirect test. Dependencies: Task 02. Definition of Done: `ChildProfileUiState` is stable/immutable.

**Task 04 — Implement `ChildProfileScreen` Composable**
Objective: Render all five canonical sections with correct states. Follow: `:core:design-system` components, `NoorHeroesTheme`. Files to Create: `ChildProfileScreen.kt`, `AvatarThumbnail.kt`, `FavoritesDownloadsEntryRow.kt`. Tests: covered by Task 06. Dependencies: Task 03. Definition of Done: screen composes only the five documented sections, no extras.

**Task 05 — Wire Navigation (Avatar, Favorites/Downloads, Bottom Nav)**
Objective: Correct routing to A.12 and B.14/B.15 without reimplementing either. Follow: existing `core-navigation` `Route` conventions. Files to Modify: `Route.kt`. Dependencies: Task 04. Definition of Done: no avatar-editing or favorites-listing UI exists inside `:feature:profile`.

**Task 06 — Add Analytics Instrumentation**
Objective: All events in §16. Follow: `AnalyticsTracker`, ViewModel-only emission. Definition of Done: one call site per event, no duplicate firing on recomposition.

**Task 07 — Add Full Test Suite**
Objective: Coverage per §19. Files to Create: `ChildProfileViewModelTest.kt`, `ChildProfileScreenTest.kt`. Definition of Done: all green in CI, structural test included.

**Task 08 — Final Code Review**
Objective: Confirm zero external `child_id` acceptance anywhere, state-clearing correctness, correct empty/offline/disabled-session handling. Definition of Done: checklist in §21 checked.

## 21. Final Verification Checklist
- [x] No public method on `ProfileRepository`/`ChildProfileViewModel` accepts an external `child_id` (verified by `ChildProfileStructuralTest`)
- [x] `child_id` resolved once from `:core:auth`'s session provider (`SessionActivationRepository`)
- [x] State-clearing verified on Switch-Profile-to-different-child transition (`ProfileStateClearingListener`)
- [x] Disabled-session signal routes to Who Is Learning gracefully, no crash (`disabled_session_redirect_triggered` -> `ProfilePickerRoute`)
- [x] First-time/zero-progress empty state shows friendly framing, not a blank state ("Start learning to see your progress here!" + activity picks)
- [x] Avatar/Favorites-Downloads entries navigate correctly without reimplementing either destination (`AvatarRoute`, `FavoritesDownloadsRoute`)
- [x] `ChildProfileUiState` is stable/immutable (`@Immutable`)
- [x] All analytics events in §16 & PRD §1.19 emitted correctly (11/11 events verified in `ChildProfileViewModelTest`)
- [x] 100% 4-locale parity across English (`values`), Arabic RTL (`values-ar`), Urdu RTL (`values-ur`), and Hindi (`values-hi`)
- [x] 93 / 93 automated tests passing across structural, ViewModel, and screen test suites; 100% visual parity verified on Android simulator
- [x] Strict compliance with design system tokens and modularity ceiling (< 500 lines per file)

## 22. Definition of Done
**Status: COMPLETED**  
`ChildProfileScreen` is live as Tab 5 of 5, composing all five canonical sections with session-derived `child_id`, correct loading/empty/offline/disabled-session handling, and navigation into A.12/B.14/B.15 — verified across all 8 mockups on Android simulator.
