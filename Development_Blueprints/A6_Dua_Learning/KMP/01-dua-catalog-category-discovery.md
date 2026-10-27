# K-01 — Dua Catalog & Category Discovery

## 1. Feature Context
NoorHeroes — Feature A.6 Dua Learning. Source PRD §6/§7, §2.2, §2.4, Screen Inventory items 1–2, 14–15. Re-derived against the real KMP core module docs (`CORE_NETWORK_INSTRUCTIONS.md`, `CORE_DATABASE_INSTRUCTIONS.md`, `CORE_NAVIGATION_INSTRUCTIONS.md`, `CORE_ANALYTICS_INSTRUCTIONS.md`) — see §32 for what changed.

## 2. Parent Feature
A.6 Dua Learning

## 3. Sub-feature
K-01 — Dua Catalog & Category Discovery

## 4. Objective
Render the category landing screen and per-category dua lists, using the real network/data/navigation stack, with a CI-blocking regression test proving no paywall UI ever appears.

## 5. Business Requirements
FR-1, FR-4, FR-13; baseline six categories plus admin-added ones (K-09); empty-state for sparse categories.

## 6. Existing Architecture
DI is **Koin** (`koinInject<T>()`), not Hilt — confirmed by `CORE_KMP_PLAYER_INSTRUCTIONS.md`'s real usage examples (`koinInject<AudioPlayerController>()`). Networking follows `CORE_NETWORK_INSTRUCTIONS.md`: `safeCall<T> { }` wrapper around requests, `HttpResponse.toAppError(): AppError` for error mapping, `PagedResponseDto<T>` for paginated responses, `provideHttpClient()`. Local persistence follows `CORE_DATABASE_INSTRUCTIONS.md`: Room via `getRoomDatabase()`, `SafeDatabaseHelper`, with `SyncQueueDao`/`SyncQueueEntity` for the offline-outbox pattern (shared with K-07). Navigation via `CORE_NAVIGATION_INSTRUCTIONS.md`'s `Navigator.navigateTo()`/`NavigationAction` sealed class, not a bespoke nav graph API. Repository naming follows the real `XxxRepository`/`XxxRepositoryImpl` convention seen in `CORE_DATA_INSTRUCTIONS.md` (`AuthRepository`/`AuthRepositoryImpl`).

## 7. Existing Code to Reuse
- `core/network`: `safeCall<T>{}`, `provideHttpClient()`, `PagedResponseDto<T>`, `HttpResponse.toAppError()`
- `core/database`: `getRoomDatabase()`, `SafeDatabaseHelper`
- `core/navigation`: `Navigator.navigateTo()`, `NavigationAction`
- `core/analytics`: `AnalyticsTracker` interface, `CompositeAnalyticsTracker`
- `core/designsystem`: `Modifier.noorHeroesSafeArea()`, `NoorColorScheme` — category tile/shimmer components if already present, else built here following `ThemeSpec` conventions

## 8. Files to Create
- `feature/dua/src/commonMain/kotlin/.../catalog/DuaCatalogScreen.kt`
- `feature/dua/src/commonMain/kotlin/.../catalog/DuaCategoryListScreen.kt`
- `feature/dua/src/commonMain/kotlin/.../catalog/DuaCatalogViewModel.kt`
- `feature/dua/src/commonMain/kotlin/.../data/DuaApiService.kt` (following `AuthApiService`'s naming convention)
- `feature/dua/src/commonMain/kotlin/.../data/DuaRepository.kt` / `DuaRepositoryImpl.kt`
- `feature/dua/src/commonMain/kotlin/.../data/DuaLocalDataSource.kt` (Room, via `getRoomDatabase()`)
- `feature/dua/src/commonTest/kotlin/.../DuaCatalogViewModelTest.kt`
- `feature/dua/src/androidUiTest/kotlin/.../DuaCatalogAlwaysFreeTierTest.kt`

## 9. Files to Modify
- Koin module registration (`diModule.kt` or equivalent) — register `DuaRepository`, `DuaApiService`
- `Navigator`'s route registry — add the Dua nested graph under Learn

## 10. Backend Requirements
Consumes B-01's real contract: `GET /v1/catalog?type=dua&category=&locale=&cursor=&limit=` (cursor-based, matching `PagedResponseDto<T>`'s real shape — **not** an offset `page`/`page_size` envelope, correcting the original draft).

## 11. KMP Requirements
- `DuaCatalogViewModel` exposes `DuaCatalogUiState` (categories, loading, error, cached-stale flag)
- `DuaRepositoryImpl.getCatalog(category, locale)` — cache-then-network via `SafeDatabaseHelper`/Room, wrapped in `safeCall<T>{}`
- Deep link registration via `Navigator`'s `NavigationAction` for `noorheroes://learn/dua/category/{category}`
- No client-side entitlement check performed anywhere (always-free by design)

## 12. NextJS Requirements
N/A.

## 13. API Contract
Per B-01 §13 (cursor-based `{items, next_cursor, has_more}`).

## 14. Database Requirements
Local Room entity `DuaCatalogCacheEntity` via `getRoomDatabase()`, following `CORE_DATABASE_INSTRUCTIONS.md`'s existing entity conventions.

## 15. Validation
Category list fetched from B-11's `GET /v1/dua/categories` via K-09, not hardcoded.

## 16. Authentication
Existing child-mode bearer via `core/network`'s auth interceptor (shared session).

## 17. Authorization
No entitlement check anywhere in this module.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Catalog fetch failure | `HttpResponse.toAppError()` mapped to a local `AppError`, cached last-known catalog rendered with a subtle staleness indicator |
| Empty category | Empty state per PRD §1.12 |

## 19. Offline First
`SafeDatabaseHelper`-backed cache-then-network, consistent with the real Room-based offline pattern documented in `CORE_DATABASE_INSTRUCTIONS.md`.

## 20. Local Data
Room-cached catalog per category+locale.

## 21. Localization
Category labels/dua titles rendered in active locale; sourced from B-11's category metadata (K-09), not hardcoded strings.

## 22. RTL
Full RTL layout via `NoorColorScheme`/`ThemeSpec` conventions.

## 23. Analytics
Via `AnalyticsTracker` (real interface, `core/analytics`): `dua_learning_landing_viewed`, `dua_category_selected`, `dua_search_performed`.

## 24. Performance
Stable/immutable `DuaCatalogUiState`; lazy list/grid rendering; coroutine cancellation on screen exit (ViewModel-scoped).

## 25. Security
Standard bearer-token reuse via `core/network`'s existing interceptor.

## 26. Library Requirements
Koin (DI), Kotlin Coroutines/Flow, Compose Multiplatform, `core/network`'s Ktor-based HTTP client (`provideHttpClient()`), Room via `core/database` — all existing platform dependencies.

## 27. Testing
- Unit: `DuaCatalogViewModel` category-filter/search logic, cache-then-network transitions
- UI: empty/loading/error states
- **Always-free-tier UI regression (CI-blocking)**: render against free/trial-expired/premium fixtures, assert identical composable tree

## 28. Documentation
Module README describing the catalog data flow and the always-free-tier invariant.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Scaffold Feature Module**
Task ID: K-01-T01. Files to Modify: `settings.gradle.kts`. Existing Architecture to Follow: existing `:feature:*` module conventions. Definition of Done: module builds.

**Task 02 — Implement Network Layer**
Task ID: K-01-T02. Files to Create: `DuaApiService.kt`. Existing Files to Reuse: `provideHttpClient()`, `safeCall<T>{}`, `PagedResponseDto<T>`. Definition of Done: service compiles and is mockable.

**Task 03 — Implement Local Data Source**
Task ID: K-01-T03. Files to Create: `DuaLocalDataSource.kt`. Existing Files to Reuse: `getRoomDatabase()`, `SafeDatabaseHelper`. Definition of Done: Room entity CRUD tested.

**Task 04 — Implement Repository**
Task ID: K-01-T04. Files to Create: `DuaRepository.kt`/`DuaRepositoryImpl.kt`. Existing Architecture to Follow: `AuthRepository`/`AuthRepositoryImpl` naming/interface-impl split. Definition of Done: cache-then-network emission order verified by test.

**Task 05 — Implement ViewModel**
Task ID: K-01-T05. Files to Create: `DuaCatalogViewModel.kt`. Definition of Done: unit tests pass.

**Task 06 — Implement Screens, Consuming K-09's Dynamic Category Metadata**
Task ID: K-01-T06. Files to Create: `DuaCatalogScreen.kt`, `DuaCategoryListScreen.kt`. Dependencies: K-09. Definition of Done: renders correctly across states, no hardcoded category icon/label map (see K-01 §32/K-09).

**Task 07 — Register Navigation & Koin Module**
Task ID: K-01-T07. Files to Modify: `Navigator` route registry, Koin DI module. Definition of Done: navigation and deep link verified.

**Task 08 — Add Analytics**
Task ID: K-01-T08. Implementation Details: via real `AnalyticsTracker` interface. Definition of Done: events verified via test double.

**Task 09 — Implement Always-Free-Tier Regression Test**
Task ID: K-01-T09. Definition of Done: CI-blocking test passes.

**Task 10 — Add Remaining Tests & Documentation**
Task ID: K-01-T10. Definition of Done: all §27 scenarios covered; README written.

**Task 11 — Final Code Review**
Task ID: K-01-T11. Definition of Done: §31 checklist fully checked.

## 30. Definition of Done
Catalog/category screens functional, offline-first via the real Room/`SafeDatabaseHelper` pattern, localized, RTL-correct, provably free of paywall UI.

## 31. Final Verification Checklist
- [ ] Uses Koin (`koinInject`), not Hilt
- [ ] Uses cursor-based pagination matching `PagedResponseDto<T>`, not offset/page
- [ ] Cache-then-network via `SafeDatabaseHelper`/Room
- [ ] Always-free-tier UI regression test passes and is CI-blocking
- [ ] Category rendering is data-driven (K-09), not hardcoded
- [ ] Navigation via `Navigator`/`NavigationAction`, not a bespoke API

## 32. Addendum (superseding the prior K-09 addendum, still valid)
Corrected from Hilt to Koin, from a generic `:core:*` module-name placeholder scheme to the real `core/network`/`core/database`/`core/navigation`/`core/analytics` classes documented in the KMP Core-Architecture docs, and from an assumed offset-pagination catalog response to the real cursor-based shape matching B-01's corrected contract. The prior addendum about K-09 owning dynamic category metadata (rather than a hardcoded icon map) still applies unchanged.
