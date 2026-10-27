# K-01 — Games Hub Screen & Skill-Area Filtering

## 1. Feature Context
Part of **A.10 Games Module**. Covers the `GamesHubScreen` — the child-facing tile-grid landing surface, entirely trusting the server's already age-band-filtered response (PRD §6.4, §7 item 1).

## 2. Parent Feature
A.10 Games Module — KMP App (Android/iOS)

## 3. Sub-feature
**2.1 Games Hub Screen & Skill-Area Filtering** `[K-01]`

## 4. Objective
Render a filter-chip row plus a `LazyVerticalGrid` of `GameTile` composables sourced entirely from `GET /v1/games` (B-01), with zero client-side age-band filtering logic — a structural absence of such logic is itself the correctness requirement (PRD §7 item 1).

## 5. Business Requirements
- FR-1: Hub sections include pinned Daily Quiz tile, Arabic Letters games, skill-area-grouped mini-games.
- FR-8: filtering is automatic and server-derived; no manual age-band override exposed to the child.
- NFR: Games Hub tile grid load p95 < 600ms (cached) (§1.8).
- §1.12 Empty States: zero-games-for-filter shows a friendly "more games coming soon" message.
- §1.13 Loading States: skeleton tile-grid shimmer.
- §1.14 Offline States: cached tiles rendered with "may be outdated" indicator; non-downloaded tiles show connect/download affordance.

## 6. Existing Architecture
KMP Clean Architecture: Feature/UI → Domain (UseCases, optional) → `core-data` (repository implementations) → `core-network`/`core-database` (`CORE_DATA_INSTRUCTIONS.md` §1). New module `:feature:games` depends on `:core:common`, `:core:navigation`, `:core:ui` (design system), `:core:data` (via repository interface), consistent with PRD §6.1. Screens are Composables; `GamesHubViewModel` extends the project's `BaseViewModel` pattern (implied by `Navigator: Lazy<Navigator>` property documented in `CORE_NAVIGATION_INSTRUCTIONS.md` §4).

## 7. Existing Code to Reuse
- `NoorResult<T>` / `Outcome<T, AppError>` (`core-common/result`) — standard repository return type.
- `AppError` hierarchy (`core-common/error`) for error-state mapping.
- `DispatcherProvider` (injected, never `Dispatchers.IO` directly) — `core-common`.
- `Navigator` / `Route` (`core-navigation`) — `GamesHubRoute` as a new `data object`/`data class Route`.
- `ContentRepository` pattern (`core-data`) as the closest existing precedent for a `Flow<List<...>>`-based catalog repository — mirror its shape for `GamesRepository.observeCatalog()`.
- Design system components from `core-ui` (tile card, filter chip primitives) per `CORE_DESIGNSYSTEM_INSTRUCTIONS.md` — reuse existing card/chip components rather than building new ones from scratch.
- `AgeBand` model (`core-common/model`) — standardized across the platform to canonical age bands: `4 to 6`, `6 to 9`, `9 to 12`, `12 to 15`, `15 to 18+`. This module displays the canonical `age_band_tier` string returned by the server verbatim, ensuring end-to-end consistency.

## 8. Files to Create
```
feature/games/src/commonMain/kotlin/com/noorheroes/feature/games/GamesHubRoute.kt
feature/games/src/commonMain/kotlin/com/noorheroes/feature/games/ui/GamesHubScreen.kt
feature/games/src/commonMain/kotlin/com/noorheroes/feature/games/ui/GameTile.kt
feature/games/src/commonMain/kotlin/com/noorheroes/feature/games/ui/SkillAreaFilterChipRow.kt
feature/games/src/commonMain/kotlin/com/noorheroes/feature/games/GamesHubViewModel.kt
feature/games/src/commonMain/kotlin/com/noorheroes/feature/games/GamesHubUiState.kt
feature/games/src/commonMain/kotlin/com/noorheroes/feature/games/di/GamesFeatureModule.kt
core/data/src/commonMain/kotlin/com/noorheroes/core/data/repository/GamesRepository.kt        # interface
core/data/src/commonMain/kotlin/com/noorheroes/core/data/repository/GamesRepositoryImpl.kt    # implementation (catalog portion only; manifest/session added in K-02/K-03)
feature/games/src/commonTest/kotlin/com/noorheroes/feature/games/GamesHubViewModelTest.kt
feature/games/src/commonTest/kotlin/com/noorheroes/feature/games/GamesHubStructuralAbsenceTest.kt
```

## 9. Files to Modify
```
core/navigation/src/commonMain/kotlin/com/noorheroes/core/navigation/Route.kt   # register GamesHubRoute
app/src/commonMain/kotlin/.../NavigationHandler.kt                              # wire GamesHubScreen into NavHost
core/data/src/commonMain/kotlin/com/noorheroes/core/data/di/RepositoryModule.kt # register GamesRepository
```
**Do Not Change:** `:feature:quiz-engine` (A.8) internals — the Daily Quiz tile only deep-links into it, per §11 below.

## 10. Backend Requirements
None implemented here; consumes B-01 (`GET /v1/games`) exactly as documented, with no additional backend changes required.

## 11. KMP Requirements
- `GamesHubScreen` Composable: filter-chip row (`SkillAreaFilterChipRow`) + `LazyVerticalGrid` of `GameTile`, 2-column mobile / 3–4-column tablet (PRD §2.2 Responsive Rules).
- `GameTile` shows thumbnail, title, skill-area icon badge, informational-only age-band micro-label (never a selectable control, PRD §2.1).
- Daily Quiz tile pinned near top, visually distinct; tapping it deep-links into `:core:quiz-engine` (A.8) — not reimplemented here.
- `GamesHubViewModel` calls `GamesRepository.observeCatalog(skillArea, domain)` and renders whatever the server returns with **zero additional filtering logic** — this absence is itself tested (Task/Test in §27).
- States: Default, Filtered-by-skill-area, Loading (skeleton shimmer), Empty-for-filter, Offline (downloaded-only actionable).

## 12. NextJS Requirements
N/A.

## 13. API Contract
Consumes `GET /v1/games` exactly as defined in B-01 §13. No new contract introduced here.

## 14. Database Requirements
Local Room/SQLDelight caching of the catalog response is owned by K-05, not this blueprint; K-01's `GamesRepository.observeCatalog()` interface is defined here but its offline-cache-backed implementation is completed in K-05.

## 15. Validation
No client-side validation of server response beyond basic null/shape safety (deserialization failure maps to `AppError.Validation` or `AppError.Server.Error`, never a crash).

## 16. Authentication
Relies on the existing child-session-scoped network client (`core-network`) attaching the child Bearer token automatically; no auth logic added in this feature module.

## 17. Authorization
N/A beyond what B-01 enforces server-side; this screen displays only what the server is willing to return for the active child session.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Catalog fetch failure (network) | Render cached last-known catalog (via K-05's local cache) with a subtle "may be outdated" indicator — never a hard error blocking the screen |
| Game asset/thumbnail fails to load | Graceful retry with backoff; fallback placeholder image, never a crash |
| Empty result for skill-area filter | Friendly empty state with link to a populated skill area |
| Deserialization/shape mismatch | Logged via `NoorHeroesLogger`, mapped to `AppError`, generic non-blocking error state shown |

## 19. Offline First
```
Remote Data (GET /v1/games)
   ↓
GamesRepositoryImpl
   ↓
Local Cache (Room/SQLDelight, owned by K-05)
   ↓
GamesHubViewModel (observes Flow)
   ↓
GamesHubScreen (UI)
```
This blueprint defines the `Flow`-based observation contract; K-05 completes the local-cache-backed implementation.

## 20. Local Data
Interface-level only here (`GamesRepository.observeCatalog(): Flow<NoorResult<List<GameCatalogItem>>>`); concrete local storage schema defined in K-05.

## 21. Localization
All UI text (`title`, filter-chip labels, empty-state copy) localized for English, Hindi, Arabic, Urdu via `core-common/localization`'s reactive localization provider — no hardcoded strings.

## 22. RTL
Filter-chip row and tile grid must mirror correctly for Arabic/Urdu (RTL) — grid reading order right-to-left, chip row reversed, consistent with `CORE_DESIGNSYSTEM_INSTRUCTIONS.md` RTL conventions.

## 23. Analytics
- `games_hub_viewed` — fired on successful initial render.
- `games_skill_area_filtered` — fired on filter-chip selection change.
- `game_tile_tapped` — fired on tile tap, immediately before manifest fetch (K-02).
Use the existing analytics module per `CORE_ANALYTICS_INSTRUCTIONS.md` conventions (event name, trigger, parameters — not invented ad hoc).

## 24. Performance
- No client-side re-filtering avoids redundant computation (also a correctness requirement, §11).
- `LazyVerticalGrid` with stable, immutable item keys (`game_id`) to minimize unnecessary recomposition.
- Thumbnail images loaded via the platform's existing image-loading pipeline with placeholder/error states (avoid main-thread blocking).
- Target: tile grid render p95 < 600ms including cache-hit path.

## 25. Security
No sensitive data displayed; relies entirely on the server-side age-band enforcement from B-01 — this module has no independent security boundary to maintain beyond correctly trusting (not re-deriving) the server response.

## 26. Library Requirements
Jetpack Compose Multiplatform, Koin (DI), Kotlinx Coroutines/Flow, Kotlinx Serialization. No new third-party libraries required beyond what `:core:data`/`:core:network` already provide.

## 27. Testing
- **Structural absence test (primary):** `GamesHubStructuralAbsenceTest` — static/reflective or code-review-assisted test asserting `GamesHubViewModel` contains no age-band comparison/filtering code path at all.
- Unit: `GamesHubViewModel` correctly maps `NoorResult.Success`/`Failure` to UI state.
- Unit: empty-filter-result maps to the empty state, not an error state.
- UI test: Games Hub tile grid never renders a tile the server didn't include in its response (verified via a mocked repository returning a known fixed set).
- UI test: filter-chip selection triggers the correct repository call parameters.
- Accessibility test: tile grid navigable in logical reading order via screen reader; filter chips correctly announce selected/unselected state.

## 28. Documentation
KDoc on `GamesHubViewModel`/`GamesRepository` documenting the "trust-server-only" filtering contract explicitly, so future maintainers do not accidentally reintroduce client-side filtering logic.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define GamesRepository Interface**
- Objective: `GamesRepository.observeCatalog(skillArea: String?, domain: String?): Flow<NoorResult<List<GameCatalogItem>>>`.
- Existing Files to Reuse: `ContentRepository` interface shape as precedent.
- Definition of Done: interface compiles, documented with KDoc on the trust-server-only contract.

**Task 02 — Implement Repository (Network-Only Path)**
- Objective: `GamesRepositoryImpl` calling `GET /v1/games` via `core-network`, mapping DTO → domain `GameCatalogItem`.
- Files to Create: `GamesRepositoryImpl.kt`.
- Definition of Done: unit test confirms correct DTO-to-domain mapping.

**Task 03 — Define UI State**
- Objective: `GamesHubUiState` sealed class (`Loading`, `Content`, `Empty`, `Error`, `Offline`).
- Definition of Done: exhaustive `when` handling verified by UI tests.

**Task 04 — Implement GamesHubViewModel**
- Objective: Calls `observeCatalog()`, maps directly to UI state with **zero filtering logic**.
- Business Rules: no age-band comparison code anywhere in this class.
- Definition of Done: structural absence test (Task 09) passes.

**Task 05 — Build GamesHubScreen Composable**
- Objective: Filter-chip row + `LazyVerticalGrid` per §11.
- Existing Files to Reuse: `core-ui` card/chip primitives.
- Definition of Done: matches Figma (once provided) responsive rules (2-col mobile / 3–4-col tablet).

**Task 06 — Build GameTile Composable**
- Objective: Thumbnail, title, skill-area badge, informational age-band micro-label.
- Definition of Done: micro-label confirmed non-interactive (no tap target).

**Task 07 — Wire Navigation Route**
- Objective: `GamesHubRoute` registered in `core-navigation`, reachable from Home's "Trending Games" rail and Rewards screen entry.
- Definition of Done: navigation test confirms both entry points route correctly.

**Task 08 — Add Analytics Events**
- Objective: Wire `games_hub_viewed`, `games_skill_area_filtered`, `game_tile_tapped` per `CORE_ANALYTICS_INSTRUCTIONS.md` conventions.
- Definition of Done: analytics call verified via mocked analytics client in tests.

**Task 09 — Add Structural Absence Test**
- Objective: Confirm no age-band filtering logic exists in `GamesHubViewModel`.
- Definition of Done: test passes and is documented as guarding against future regression.

**Task 10 — Add Remaining Tests**
- Objective: Full suite per §27.

**Task 11 — Add Localization & RTL Verification**
- Objective: All strings localized; RTL layout verified for Arabic/Urdu.
- Definition of Done: RTL screenshot/manual verification checklist item.

**Task 12 — Final Code Review**
- Objective: Confirm zero client-side age-band logic, confirm reuse of existing design-system components rather than duplicated new ones.
- Definition of Done: review checklist (§31) fully checked.

## 30. Definition of Done
- Games Hub renders exactly what the server returns, with zero client-side age-band filtering (verified by structural absence test).
- All states (Loading/Content/Empty/Error/Offline) implemented and tested.
- Daily Quiz tile correctly deep-links into A.8's existing engine without reimplementation.
- Localization/RTL verified across English/Hindi/Arabic/Urdu.
- Analytics events firing correctly.

## 31. Final Verification Checklist
- [ ] Structural absence test passing (no age-band filtering logic in ViewModel)
- [ ] Tile grid never renders a server-omitted tile (mocked-repository UI test)
- [ ] All five UI states implemented and tested
- [ ] Daily Quiz tile delegates to `:core:quiz-engine`, not reimplemented
- [ ] Localization complete for EN/HI/AR/UR
- [ ] RTL layout verified for Arabic/Urdu
- [ ] Analytics events verified via mocked client
- [ ] Accessibility (screen reader order, chip state announcement) verified
- [ ] No files outside declared scope modified

---

## 32. Cross-Platform Dependencies
- Backend Dependency: B-01 (`GET /v1/games`), sole data source.
- KMP Dependency: K-02 (tile tap launches a session), `:core:quiz-engine` (A.8, Daily Quiz tile deep link).
- Admin Dependency: N-01 (publish/withdraw state determines what this screen can ever show).
- Database Dependency: Local Room cache (`GameCatalogEntity`, completed in K-05).
- External Service Dependency: None.
- Figma Dependency: Games Hub screen (tile grid + skill-area filter chips) — Figma Required per the original feature breakdown.
