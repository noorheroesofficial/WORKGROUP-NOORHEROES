# K-01 — Search Entry Point & Landing Screen

## 1. Feature Context
Part of Feature B.13 (Search & Discovery). The universal entry point into search — reachable identically from Home and every tab, not a standalone bottom-nav destination itself.

## 2. Parent Feature
B.13 — Search & Discovery

## 3. Sub-feature
K-01 — Search Entry Point & Landing Screen

## 4. Objective
Build the new `feature-search` KMP module's landing surface: a consistent search-icon affordance across Home/every tab, the `SearchScreen` Composable with search bar + recent searches, wired into `core-navigation` as a distinct destination.

## 5. Business Requirements
- FR-1: Search UI sections — search bar with voice option, recent searches, filtered results grid, empty state.
- §2.1: search bar reachable identically from Home and every tab, leading magnifier + trailing microphone icon both always visible, no hidden/overflow voice menu.
- §2.2 Screen: Search Screen (Landing) — states: default with recent searches, default with no recent searches, voice-listening, voice-processing.
- §1.12: zero recent searches → section omitted or lightweight first-time hint, never an awkward empty-list placeholder.
- Accessibility: mic button has a distinct accessible label separate from the text-input field; recent items individually screen-reader-navigable.

## 6. Existing Architecture
New `feature-search` module, Kotlin/Compose/MVVM/Clean Architecture, following the identical structure of `feature-home`/`feature-onboarding` (per `CORE_COMMON_INSTRUCTIONS.md`'s module layout). Depends on `core-navigation`, `core-designsystem`, `core-analytics`, `core-network`, `core-data`. DI via Koin (project-wide standard — not Hilt, correcting the PRD's generic Android prompt assumption).

## 7. Existing Code to Reuse
- `core-navigation` — existing navigation-graph registration pattern (see `CORE_NAVIGATION_INSTRUCTIONS.md`) for adding `SearchScreen` as a destination reachable from any tab's top bar.
- `core-designsystem` — existing icon set (magnifier, microphone), rounded-input token, spacing/typography tokens (per `CORE_DESIGNSYSTEM_INSTRUCTIONS.md`) — no new design tokens invented here.
- `core-analytics` — `AnalyticsTracker` for `search_opened`.
- Existing top-bar/tab-scaffold component (wherever Home/other tabs currently render their top bar) — extended with the search-icon affordance, not duplicated per-tab.

## 8. Files to Create
- `feature-search/src/commonMain/kotlin/.../search/SearchScreen.kt` (Composable).
- `feature-search/src/commonMain/kotlin/.../search/SearchViewModel.kt`.
- `feature-search/src/commonMain/kotlin/.../search/SearchUiState.kt`.
- `feature-search/src/commonMain/kotlin/.../search/components/SearchBar.kt`.
- `feature-search/src/commonMain/kotlin/.../search/components/RecentSearchesList.kt`.
- `feature-search/src/commonMain/kotlin/.../search/components/ClearRecentSearchesAction.kt`.
- `feature-search/src/commonMain/kotlin/.../search/di/SearchModule.kt` (Koin module).
- `feature-search/src/commonTest/kotlin/.../SearchViewModelTest.kt`.
- `feature-search/src/commonTest/kotlin/.../SearchScreenUiTest.kt`.

## 9. Files to Modify
- App-level Koin module registration — include `SearchModule`.
- `core-navigation`'s nav-graph registration file — add `SearchScreen` destination.
- Existing Home/tab top-bar composable(s) — add the search-icon affordance consistently.

## 10. Backend Requirements
None directly created here; `SearchRepository` (backing this screen's recent-searches list) is built in K-04, consuming B-04's `GET /v1/search/recent`.

## 11. KMP Requirements
- `SearchViewModel` exposes `StateFlow<SearchUiState>` covering: query input text, recent-searches list, loading flag.
- `SearchScreen` renders: `SearchBar` (magnifier + mic, both always visible, no overflow menu), `RecentSearchesList` (omitted/hint-only when empty), `ClearRecentSearchesAction`.
- Tapping the search icon (Home/any tab) navigates to `SearchScreen` via `core-navigation`.
- Tapping a recent-search item re-runs that query, navigating into K-02's results screen.
- Mic tap transitions into K-03's voice sub-flow (this screen does not itself implement voice capture — delegates).
- Prevent unnecessary recomposition: `SearchUiState` is an immutable, stable data class; list state uses stable `ImmutableList` (or equivalent) wrapping to avoid Compose over-recomposition on unrelated state changes.

## 12. NextJS Requirements
N/A — client-only screen.

## 13. API Contract
Consumes B-04's `GET /v1/search/recent` (via K-04's `SearchRepository`, not duplicated here) for the recent-searches list shown on this screen.

## 14. Database Requirements
None directly — reads through K-04's Room-backed recent-searches cache.

## 15. Validation
Search-bar text input has no client-side content validation beyond a reasonable max-length guard matching B-01's `q` bound (200 chars) to avoid an obviously-oversized payload being typed.

## 16. Authentication
Screen assumes an already-authenticated child session (standard app-wide session gate); no additional auth handling here.

## 17. Authorization
N/A beyond standard child-session gating.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Recent-searches fetch failure | Section silently omitted or shows a lightweight retry affordance — never a jarring error screen on the landing surface |
| Navigation failure | Standard `core-navigation` error handling (no feature-specific override) |

## 19. Offline First
Recent searches read from local Room cache first (K-04), so this screen renders instantly regardless of connectivity; a background refresh syncs against B-04 when online.

## 20. Local Data
Reads (not owns) K-04's local recent-searches cache.

## 21. Localization
All strings (`placeholder`, `"Recent Searches"` label, hint copy) sourced from the existing localization/resource system — English, Hindi, Arabic, Urdu. No hardcoded user-facing strings.

## 22. RTL
Single-column layout mirrors correctly in RTL: magnifier/mic icon positions swap sides per `CORE_DESIGNSYSTEM_INSTRUCTIONS.md`'s existing RTL mirroring convention; tablet variant widens the search bar with no structural layout change.

## 23. Analytics
- `search_opened` — fired on navigation into `SearchScreen`.
- `search_recent_query_reused` — fired on recent-search-item tap (event itself defined here; full flow completion tracked in K-02).

## 24. Performance
- `SearchUiState` immutability + stable collection wrapping to minimize recomposition.
- Recent-searches list rendered from local cache (K-04) — no network round-trip blocks initial screen paint.
- No main-thread blocking work in `SearchViewModel` init.

## 25. Security
No new security surface — screen only reads locally-cached, already-authenticated data.

## 26. Library Requirements
Jetpack Compose, Koin (DI), existing `core-navigation`/`core-designsystem`/`core-analytics` modules. No new third-party library.

## 27. Testing
- Unit: `SearchViewModel` initial state, recent-searches-loaded state, empty-state branching.
- UI test: mic button has a distinct accessible label from the text field (accessibility-tree assertion).
- UI test: recent-search item tap navigates to results with the correct re-run query.
- UI test: empty-recent-searches state renders the lightweight hint, not an empty-list placeholder.

## 28. Documentation
KDoc on `SearchViewModel`/`SearchUiState`; module README noting `feature-search`'s dependency graph (`core-navigation`, `core-designsystem`, `core-analytics`, `core-data`).

## 29. AI Coding Agent Implementation Steps
**Task 01 — Scaffold feature-search Module**
Objective: create the module with standard `commonMain`/`androidMain`/`iosMain` source sets mirroring `feature-home`'s structure.
Existing architecture to follow: `CORE_COMMON_INSTRUCTIONS.md` module layout.
Files to create: module `build.gradle.kts`, package skeleton.

**Task 02 — Define SearchUiState**
Objective: immutable, stable state data class.
Files to create: `SearchUiState.kt`.

**Task 03 — Implement SearchViewModel**
Objective: exposes `StateFlow<SearchUiState>`; loads recent searches from K-04's repository (interface only at this point, if K-04 not yet built — depend on the interface, not the impl).
Files to create: `SearchViewModel.kt`.

**Task 04 — Build SearchBar, RecentSearchesList, ClearRecentSearchesAction Composables**
Objective: pixel/behavior match Figma "Search Screen (Landing)".
Files to create: component Composables.
Accessibility: distinct labels per §15/§27.

**Task 05 — Assemble SearchScreen & Wire Navigation**
Objective: compose the above into `SearchScreen`; register as a `core-navigation` destination; add the search-icon affordance to Home/tab top bars.
Files to modify: nav-graph file, top-bar composable(s).

**Task 06 — Register Koin Module**
Files to create: `SearchModule.kt`; files to modify: app-level Koin registration.

**Task 07 — Add Tests & Analytics**
Objective: full coverage per §27; wire `search_opened`/`search_recent_query_reused` via `core-analytics`.

**Task 08 — Final Review**
Objective: confirm RTL mirroring, localization completeness (no hardcoded strings), recomposition stability.

## 30. Definition of Done
- `SearchScreen` reachable from Home and every tab via a consistent icon.
- Recent searches render (or gracefully omit) correctly.
- Mic tap hands off cleanly into K-03.
- Full localization + RTL support verified.
- Unit + UI tests green.

## 31. Final Verification Checklist
- [ ] Search icon present and functionally identical from Home and every tab.
- [ ] Magnifier and mic icons both always visible, no overflow menu.
- [ ] Empty recent-searches state uses the lightweight hint pattern, not an empty-list placeholder.
- [ ] Mic button and text field have distinct accessible labels.
- [ ] RTL layout verified for Arabic.
- [ ] No hardcoded user-facing strings.
- [ ] `SearchUiState` is immutable/stable — no unnecessary recomposition observed in profiling.
