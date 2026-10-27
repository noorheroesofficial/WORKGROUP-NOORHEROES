# K-01 — Stories Library & Category Discovery

## 1. Feature Context
The Stories tab landing screen: horizontally-scrollable category rails (Bedtime, Prophet Stories, Islamic Shorts, Series, Values & Manners, Ramadan & Eid, Downloads) with a sticky filter bar, fully offline-browsable for the Downloads category and gracefully degraded for everything else.

## 2. Parent Feature
Feature A.3 — Stories Module (Animated Storytelling System)

## 3. Sub-feature
2.1 Stories Library & Category Discovery (ID: **K-01**)

## 4. Objective
Build the `feature:stories` module's Library screen — category rails, filter panel, empty/loading/error/offline states — backed by a repository that reads B-01's catalog API with a local cache-first read for the Downloads category.

## 5. Business Requirements
- FR-1: exactly the seven defined categories.
- FR-2: filters — age band, duration, language, format, downloaded-only, free/premium.
- §1.12 Empty States: "More stories for you are on the way" per empty category, never a blank grid.
- §1.13 Loading States: skeleton category rails.
- §1.14 Offline States: Downloads category always available offline; other categories show cached metadata browsable, non-downloaded items show "connect to internet or download" rather than a dead tap.

## 6. Existing Architecture
New `feature:stories` module (per PRD §6.1), following the established Clean Architecture/MVVM layering used across other feature modules: `data` (repository, remote/local sources) → `domain` (use cases) → `presentation` (ViewModel, Compose UI). Depends on `core-network`, `core-datastore`, `core-designsystem`, `core-ui`, `core-navigation`.

## 7. Existing Code to Reuse
- `core-network`: Retrofit/Ktor client conventions for the catalog API call
- `core-datastore`: local cache storage pattern (for offline-browsable cached catalog metadata)
- `core-designsystem`: `NoorHeroesTheme`, rail/card components if already established elsewhere (e.g., Home's rail pattern from A.2 — reuse the same rail Composable rather than building a parallel one)
- `core-ui`: `LoadStateContent`, `EmptyStateView`, `ErrorView`
- `core-navigation`: `Navigator`, `Route`

## 8. Files to Create
- `feature/stories/ui/StoriesLibraryScreen.kt`
- `feature/stories/ui/CategoryFilterPanel.kt`
- `feature/stories/viewmodel/StoriesLibraryViewModel.kt` (+ State/Event files)
- `feature/stories/data/StoryCatalogRepository.kt`
- `feature/stories/data/remote/StoryCatalogApi.kt`
- `feature/stories/data/local/StoryCatalogCache.kt`
- `feature/stories/domain/GetStoriesLibraryUseCase.kt`
- `test/feature/stories/StoriesLibraryViewModelTest.kt`
- `androidTest/feature/stories/StoriesLibraryScreenTest.kt`

## 9. Files to Modify
- `core-navigation/Route.kt` — add `StoriesLibraryRoute`

## 10. KMP Requirements
- `StoryCatalogRepository.getLibrary(filters)`: cache-first for the Downloads category (reads local downloaded-episode index maintained by K-07's `DownloadRepository`), network-first-with-cache-fallback for all other categories.
- `StoriesLibraryViewModel`: exposes a single sealed `LibraryUiState` (Loading, Content(rails), Empty(category), Error) per rail/category combination — never a single global loading flag masking per-category empty states.
- Filter panel state (age band, duration, language, format, downloaded-only, free/premium) held in the ViewModel, re-triggers `GetStoriesLibraryUseCase` on change with debounced re-fetch (avoid a network call per keystroke/toggle-flicker).
- Offline non-Downloads items: rendered with a distinct visual affordance ("connect to internet or download") rather than a dead/no-op tap target — tapping surfaces an explanatory toast/snackbar, not silent failure.

## 11. Required API
**User API** — B-01 `GET /v1/content?type=story&category=&age_band=&locale=&format=&downloaded_only=`.

## 12. Offline First
```
Remote Catalog API (B-01)
    ↓
StoryCatalogRepository (cache-first for Downloads, network-first-with-fallback otherwise)
    ↓
StoryCatalogCache (core-datastore-backed local metadata cache)
    ↓
StoriesLibraryViewModel / UI
```
Downloads category sourced entirely from K-07's local download index — zero network dependency. Other categories browsable from last-cached metadata when offline, with a clear non-interactive affordance on items that aren't actually downloaded.

## 13. Local Data
`StoryCatalogCache` persists the last-fetched catalog page per filter combination (bounded cache size/TTL, evicted on next successful network refresh) via `core-datastore`.

## 14. Localization
English, Hindi, Arabic, Urdu — category names, filter labels, empty-state copy all sourced from the shared localization resource system, never hardcoded strings.

## 15. RTL
Category rail scroll direction mirrors in Arabic/Urdu; filter chip row order mirrors; category icons (moon, lantern, scroll) do not require mirroring themselves but their surrounding layout does.

## 16. Analytics
Emit `stories_library_viewed`, `stories_category_filtered` via the existing `AnalyticsTracker` (per `CORE_ANALYTICS_INSTRUCTIONS.md` conventions), fired from the ViewModel only.

## 17. Performance
- Rail scrolling must avoid unnecessary recomposition — use stable/immutable data classes for rail item state and `key()` on `LazyRow` items.
- Skeleton loading state must render immediately (no blocking network wait before first paint).

## 18. Security
No sensitive data on this screen; entitlement/premium badges are informational only (enforcement happens server-side at B-07, never trusted client-side here).

## 19. Testing
- Unit: filter-change debounce behavior, cache-first-for-Downloads routing logic, offline-affordance state derivation.
- UI: empty-state-per-category rendering, skeleton-to-content transition, RTL rail-direction snapshot tests.
- Accessibility: TalkBack traversal across filter chips and rail items with correct content descriptions (including lock/premium state where applicable).

## 20. AI Coding Agent Implementation Steps

**Task 01 — Scaffold `feature:stories` Module & Add Route**
Objective: Establish the module following existing Clean Architecture conventions; add `StoriesLibraryRoute`. Follow: an existing feature module (e.g., `feature:onboarding`) as the structural template. Definition of Done: module compiles, route registered.

**Task 02 — Implement `StoryCatalogApi` and `StoryCatalogCache`**
Objective: Remote client for B-01's endpoint + local cache layer. Follow: `core-network`/`core-datastore` conventions. Tests: cache read/write round-trip. Definition of Done: both layers independently testable.

**Task 03 — Implement `StoryCatalogRepository` with Cache/Network Routing**
Objective: Cache-first for Downloads, network-first-with-fallback otherwise. Dependencies: Task 02. Tests: routing-logic unit tests for both category types, offline-fallback test. Definition of Done: tests pass.

**Task 04 — Implement `GetStoriesLibraryUseCase`**
Objective: Domain-layer orchestration between filters and repository. Dependencies: Task 03. Tests: filter-passthrough correctness. Definition of Done: test passes.

**Task 05 — Implement `StoriesLibraryViewModel`**
Objective: Per-category `LibraryUiState`, debounced filter re-fetch. Follow: `BaseViewModel`. Dependencies: Task 04. Tests: debounce timing, per-category state independence. Definition of Done: tests pass.

**Task 06 — Implement `StoriesLibraryScreen` and `CategoryFilterPanel` Composables**
Objective: Rails, sticky filter bar, empty/loading/error/offline states per §11 PRD requirements. Follow: `core-designsystem`/`core-ui` components, reuse Home's rail pattern if available. Dependencies: Task 05. Tests: UI tests per §19. Definition of Done: all visual states render correctly per fixture data.

**Task 07 — Implement Offline Non-Downloads Affordance**
Objective: Distinct non-interactive visual state + explanatory feedback for offline non-downloaded items. Dependencies: Task 06. Tests: offline-simulated UI test. Definition of Done: test passes, no dead silent taps.

**Task 08 — Add Analytics Instrumentation**
Objective: `stories_library_viewed`, `stories_category_filtered`. Follow: `AnalyticsTracker` injection. Tests: fake-tracker assertions. Definition of Done: exactly one call site per event.

**Task 09 — Full RTL and Accessibility Pass**
Objective: Verify rail direction, filter chip order, TalkBack traversal. Tests: per §19. Definition of Done: snapshot baselines captured for LTR/RTL.

**Task 10 — Add Full Test Suite**
Objective: Complete coverage per §19. Definition of Done: all green.

**Task 11 — Final Code Review**
Objective: Confirm no premium/entitlement enforcement logic lives client-side, confirm cache never serves stale-forever data (TTL/eviction present). Definition of Done: checklist in §21 checked.

## 21. Final Verification Checklist
- [ ] All seven categories render correctly with correct filter support
- [ ] Downloads category fully functional offline with zero network dependency
- [ ] Non-Downloads categories browsable from cache when offline, with a clear non-dead-tap affordance on non-downloaded items
- [ ] Empty-category state matches PRD copy, never a blank grid
- [ ] Skeleton loading renders immediately, no blocking network wait
- [ ] Filter changes debounced, not fired per keystroke/toggle-flicker
- [ ] `stories_library_viewed`/`stories_category_filtered` events fire correctly
- [ ] Full RTL mirroring verified for rails and filter bar
- [ ] No client-side entitlement/premium enforcement (informational badges only)

## 22. Definition of Done
The Stories Library renders all seven categories with correct filtering, offline-first Downloads browsing, graceful degradation elsewhere, and hands off cleanly to K-02 (Story Detail) on card tap.
