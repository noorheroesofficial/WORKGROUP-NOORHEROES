# K-09 — Dynamic Category Metadata Rendering

## 1. Feature Context
NoorHeroes — Feature A.6 Dua Learning. Companion to B-11 (real `dua_category` lookup table + `GET /v1/dua/categories`). Re-derived against the real KMP core modules — see §32.

## 2. Parent Feature
A.6 Dua Learning

## 3. Sub-feature
K-09 — Dynamic Category Metadata Rendering

## 4. Objective
Fetch category metadata (icon key, localized label, sort order) from B-11's real `GET /v1/dua/categories` instead of hardcoding it client-side, so an admin-added category (via N-04) renders correctly with zero app release.

## 5. Business Requirements
PRD §4.2, §2.1.

## 6. Existing Architecture
Same architecture-improvement rationale as before, now correctly grounded: `DuaCategoryMetadataRepository` (real `XxxRepository`/`XxxRepositoryImpl` split, per `CORE_DATA_INSTRUCTIONS.md`'s convention) fetches via `safeCall<T>{}`/`provideHttpClient()` (`core/network`), caches via `getRoomDatabase()`/`SafeDatabaseHelper` (`core/database`), injected via Koin (`koinInject<DuaCategoryMetadataRepository>()`).

## 7. Existing Code to Reuse
- `core/network`'s `safeCall<T>{}`, `PagedResponseDto<T>`-adjacent response handling
- `core/database`'s `getRoomDatabase()`, `SafeDatabaseHelper`
- `core/designsystem`'s icon asset library — `DuaCategoryIconResolver` maps `icon_key` values to it

## 8. Files to Create
- `feature/dua/src/commonMain/kotlin/.../catalog/DuaCategoryMetadataRepository.kt` / `DuaCategoryMetadataRepositoryImpl.kt`
- `feature/dua/src/commonMain/kotlin/.../catalog/DuaCategoryIconResolver.kt`
- `feature/dua/src/commonTest/kotlin/.../DuaCategoryIconResolverTest.kt`
- `feature/dua/src/androidUiTest/kotlin/.../DuaCategoryUnknownIconFallbackTest.kt`

## 9. Files to Modify
- `DuaRepository`/`DuaRepositoryImpl` (K-01) — add `getCategoryMetadata()`
- `DuaCatalogViewModel.kt`, `DuaCatalogScreen.kt` (K-01) — consume metadata instead of a hardcoded list

## 10. Backend Requirements
Consumes B-11 (`GET /v1/dua/categories`).

## 11. KMP Requirements
- `DuaCategoryMetadataRepositoryImpl.getCategories()` — cache-then-network via `SafeDatabaseHelper`
- `DuaCategoryIconResolver.resolve(iconKey: String): IconResource` — known-key mapping with a generic fallback, never throws
- Tiles render in `sort_order`; label rendered in active locale from the metadata payload

## 12. NextJS Requirements
N/A.

## 13. API Contract
Per B-11 §13 (`GET /v1/dua/categories`).

## 14. Database Requirements
Local Room entity for cached category metadata, via `getRoomDatabase()`.

## 15. Validation
`icon_key` resolution never throws — always resolves to a matched icon or the default fallback.

## 16. Authentication
Existing child-mode bearer via `core/network`.

## 17. Authorization
No entitlement check — always-free content metadata.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Fetch failure | Cached last-known metadata; if no cache exists (first launch, offline), a minimal built-in six-category fallback |
| Unrecognized `icon_key` | Generic default icon, correct label still shown |
| Missing label for active locale | Fall back to English |

## 19. Offline First
Remote (B-11) → `DuaCategoryMetadataRepositoryImpl` → Room cache → UI.

## 20. Local Data
Cached category metadata.

## 21. Localization
Fully data-driven per-locale labels from the API payload.

## 22. RTL
Unchanged from K-01's existing RTL handling — only the data source changes.

## 23. Analytics
N/A directly (feeds K-01's existing `dua_category_selected`).

## 24. Performance
Small list; cache aggressively (6-hour TTL matching B-11).

## 25. Security
No new sensitive data.

## 26. Library Requirements
`core/network`, `core/database`, `core/designsystem`, Koin — existing dependencies only.

## 27. Testing
- Unit: `DuaCategoryIconResolver` known/unknown key handling
- Unit: cache-then-network and offline-fallback-to-built-in-defaults logic
- UI: unrecognized `icon_key` renders the fallback, not a crash or blank tile
- Integration: a category added via N-04/B-11 renders correctly on next refresh without an app update

## 28. Documentation
Doc note on the icon-fallback contract.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement Category Metadata Repository**
Task ID: K-09-T01. Files to Create: `DuaCategoryMetadataRepository.kt`/`Impl.kt`. Existing Architecture to Follow: `core/network`/`core/database` cache-then-network pattern. Definition of Done: repository unit tests confirm correct emission and offline fallback.

**Task 02 — Implement Icon Resolver**
Task ID: K-09-T02. Files to Create: `DuaCategoryIconResolver.kt`. Definition of Done: no-throw behavior confirmed for any input.

**Task 03 — Wire Into `DuaRepository`**
Task ID: K-09-T03. Files to Modify: `DuaRepositoryImpl.kt`. Definition of Done: `getCategoryMetadata()` available and testable.

**Task 04 — Update Catalog Screen/ViewModel**
Task ID: K-09-T04. Files to Modify: `DuaCatalogViewModel.kt`, `DuaCatalogScreen.kt`. Do Not Change: K-01's always-free-tier regression test's assertions (must still pass). Definition of Done: catalog renders correctly for the six baseline categories and a newly admin-added test category.

**Task 05 — Implement Built-In Default Fallback**
Task ID: K-09-T05. Definition of Done: cold-start-offline test confirms the screen is never empty.

**Task 06 — Add Tests & Documentation**
Task ID: K-09-T06. Definition of Done: all §27 scenarios covered; fallback contract documented.

**Task 07 — Final Code Review**
Task ID: K-09-T07. Definition of Done: §31 checklist fully checked.

## 30. Definition of Done
Category rendering fully data-driven from B-11's real API, with graceful icon fallback and offline-default safety net; K-01's existing tests still pass.

## 31. Final Verification Checklist
- [ ] Category tiles render from real API metadata (B-11), not a hardcoded list
- [ ] Unrecognized `icon_key` falls back gracefully
- [ ] Offline cold-start falls back to a minimal built-in default set
- [ ] A category added via N-04/B-11 renders correctly without an app update
- [ ] Uses Koin, `core/network`, `core/database` — real classes, not placeholders

## 32. Addendum — What Changed From the Original Draft
Corrected from Hilt/generic `:core:offline-cache` placeholders to Koin and the real `core/network`/`core/database` classes (`safeCall<T>{}`, `getRoomDatabase()`, `SafeDatabaseHelper`). The core architecture-improvement rationale (data-driven category rendering, per B-01/B-11's addenda) is unchanged.
