# K-02 — Learning Stats Summary Widget

## 1. Feature Context
The condensed level/XP/streak/badges glance-card within Child Profile, sourced from B-01. Deliberately simpler than A.11's full Rewards Wallet — a quick-glance summary, not a full feature surface.

## 2. Parent Feature
Feature B.16 — Child Profile (Bottom Tab)

## 3. Sub-feature
2.2 Learning Stats Summary Widget (Offline & Degraded States) (ID: **K-02**)

## 4. Objective
Implement `ProfileRepository.getProgressSummary()` against B-01, with Room caching for offline rendering and an isolated graceful-degradation state that never blocks the rest of the Profile screen.

## 5. Business Requirements
- FR-5: Stats summary sourced from `GET /v1/children/{id}/progress`, a condensed subset distinct from A.9/A.11's full data.
- Edge Case 2: progress summary fetch fails → rest of Profile still renders/functions; only the stats section shows a graceful "may be unavailable right now" state.
- Empty State: new child, zero progress → friendly first-time framing.
- Loading State: skeleton shimmer on initial load; cached data with background refresh on subsequent visits.
- Offline State: renders from cached data when offline.

## 6. Existing Architecture
Extends K-01's `ProfileRepository`/`ProfileRepositoryImpl` (does not create a separate repository) — implements the `getProgressSummary()`/`observeCachedSummary()` methods declared in K-01's interface, backed by a new Room DAO.

## 7. Existing Code to Reuse
- `feature/profile/data/ProfileRepository.kt`, `ProfileRepositoryImpl.kt` (from K-01 — extend, do not duplicate)
- `:core:network` — existing Retrofit/OkHttp client conventions for authenticated child-session calls
- `:core:database` — Room `Dao`/`Entity` conventions
- `:core:design-system` — progress-ring component (reused, styled more minimally than A.11's Wallet header per PRD §2.1)

## 8. Files to Create
- `feature/profile/data/local/ProgressSummaryDao.kt`
- `feature/profile/data/local/ProgressSummaryEntity.kt`
- `feature/profile/data/remote/ProfileApiService.kt` (or extension of an existing shared API service) — `getProgressSummary(): ProgressSummaryDto`
- `feature/profile/ui/components/StatsSummaryCard.kt`
- `feature/profile/ui/components/StatsSummaryUnavailableState.kt`
- `feature/profile/ui/components/StatsSummaryEmptyState.kt`
- `test/feature/profile/ProgressSummaryRepositoryTest.kt`
- `androidTest/feature/profile/StatsSummaryCardTest.kt`

## 9. Files to Modify
- `feature/profile/data/ProfileRepositoryImpl.kt` — implement `getProgressSummary()`/`observeCachedSummary()` using `ProgressSummaryDao` + `ProfileApiService`
- `core-database/NoorHeroesDatabase.kt` — register `ProgressSummaryDao`/`ProgressSummaryEntity`

## 10. KMP Requirements
- `getProgressSummary()` calls B-01 with `id` derived internally (via K-01's session-derivation pattern) — never accepts an external `child_id`.
- On successful fetch, upsert into `ProgressSummaryEntity` (Room), keyed by the internally-derived `child_id`; `observeCachedSummary()` returns a `Flow` reading from Room, so the UI always renders from cache-then-refresh, never a raw one-shot network call.
- On fetch failure (`503 PROGRESS_SUMMARY_UNAVAILABLE`, network error, timeout), do **not** clear or corrupt the existing cached value — the UI falls back to the last-known-good cached summary if present, or the "unavailable" state if no cache exists yet.
- On a `403 CHILD_MISMATCH` or `409 SESSION_INVALID` response (should be structurally impossible given internal `child_id` derivation, but defensively handled), propagate a distinct signal up to `ChildProfileViewModel` (K-01) for the disabled-session redirect path — never silently swallow it.
- The "unavailable" state renders **only within** `StatsSummaryCard`'s bounds — `ChildProfileScreen`'s other sections (avatar, language toggle, Favorites/Downloads, Switch Profile) must remain fully rendered and interactive, verified by a dedicated isolation UI test (PRD §7 item 5).
- First-time/zero-progress: distinguish "successful fetch with all-zero values" (render `StatsSummaryEmptyState`) from "fetch failed" (render `StatsSummaryUnavailableState`) — these are different states with different copy, never conflated.

## 11. Required API
- `GET /v1/children/{id}/progress` (B-01)

## 12. Offline First
```
Remote (B-01)
    ↓ (on success)
ProgressSummaryDao (Room upsert)
    ↓
observeCachedSummary(): Flow<ProgressSummary>
    ↓
StatsSummaryCard (renders from Flow, background-refreshes)
```
- Initial local load: emit cached value immediately if present, then trigger a background refresh.
- Offline read: `Flow` continues emitting the last cached value; no network attempt blocks rendering.
- Network recovery: next screen resume or explicit pull-to-refresh (if present) triggers a fresh fetch.
- Cache invalidation: none required beyond B-01's own 60s server-side TTL — client cache is simply refreshed opportunistically, not aggressively invalidated.

## 13. Local Data
`ProgressSummaryEntity(childId: String [PK], level, xp, xpToNextLevel, streakCurrent, badgesCount, cachedAt)` — single row per child, upserted on every successful fetch.

## 14. Localization
Numeric values (XP, streak count, badge count) formatted per the active display locale's number formatting (from K-03), not hardcoded Western-numeral formatting where the locale calls for different conventions.

## 15. RTL
Progress ring and headline-number row mirror correctly in RTL (ring fill direction and numeral positioning consistent with the platform's established RTL numeric-display pattern used elsewhere, e.g., A.11's Wallet).

## 16. Analytics
Emit `child_profile_stats_load_failed` when the unavailable state renders (with error-class metadata, no PII); `child_profile_viewed`'s stats-portion is otherwise covered by K-01's screen-level event.

## 17. Performance
Room `Flow` query must be indexed by PK `childId` (trivial given one row per child); avoid re-fetching on every recomposition — fetch is triggered by `ChildProfileViewModel`'s lifecycle (screen entry/resume), not by the Composable's recomposition cycle.

## 18. Security
No new sensitive data — `level`/`xp`/`streak`/`badges` are non-PII progress metrics scoped strictly to the internally-derived `child_id`.

## 19. Testing
- Unit: `getProgressSummary()` upserts Room on success; does not clear cache on failure.
- Unit: distinguishes zero-progress-success from fetch-failure (two different resulting UI states from two different repository outcomes).
- UI: isolation test — simulate a failed fetch, assert `StatsSummaryCard` shows "unavailable" while `LanguageToggle`, `FavoritesDownloadsEntryRow`, and `SwitchProfileRow` (from K-01/K-03/K-04) remain rendered and tappable.
- UI: offline rendering from cache with no network call attempted blocking the UI thread.
- UI: skeleton-then-cached-then-refreshed sequence renders in the correct order.

## 20. AI Coding Agent Implementation Steps

**Task 01 — Create `ProgressSummaryEntity` & `ProgressSummaryDao`**
Objective: Room persistence for the cached summary. Follow: existing `core-database` `Entity`/`Dao` conventions. Files to Create: `ProgressSummaryEntity.kt`, `ProgressSummaryDao.kt`. Files to Modify: `NoorHeroesDatabase.kt`. Tests: DAO upsert test. Definition of Done: one row per `childId`, upsert-on-conflict.

**Task 02 — Create `ProfileApiService.getProgressSummary()`**
Objective: Typed client for B-01. Follow: existing Retrofit service conventions, child-session Bearer auth injection (shared interceptor). Files to Create: `ProfileApiService.kt`. Tests: DTO round-trip against B-01's documented five-field contract. Definition of Done: DTO physically cannot deserialize extra undocumented fields as authoritative data.

**Task 03 — Implement `getProgressSummary()`/`observeCachedSummary()` in `ProfileRepositoryImpl`**
Objective: Cache-then-refresh orchestration with failure-preserves-cache semantics. Follow: K-01's existing internal `child_id` derivation (extend, do not re-derive separately). Files to Modify: `ProfileRepositoryImpl.kt`. Business Rules: never clear cache on failure; distinguish zero-success from failure. Tests: full matrix per §19. Dependencies: Tasks 01–02. Definition of Done: `Flow`-based `observeCachedSummary()` is the only path the UI reads from.

**Task 04 — Implement `StatsSummaryCard`, Empty, and Unavailable States**
Objective: Three distinct render states (loaded, empty/first-time, unavailable) as isolated, independently-failing components. Follow: `:core:design-system` progress-ring component. Files to Create: `StatsSummaryCard.kt`, `StatsSummaryEmptyState.kt`, `StatsSummaryUnavailableState.kt`. Dependencies: Task 03. Definition of Done: unavailable state cannot visually or functionally block sibling sections.

**Task 05 — Add Isolation UI Test**
Objective: The PRD §7-item-5-mandated test proving failure isolation. Files to Create: `StatsSummaryCardTest.kt`. Dependencies: Task 04, K-01's `ChildProfileScreen`. Definition of Done: test simulates a failed fetch and asserts sibling sections remain fully functional.

**Task 06 — Add Analytics Instrumentation**
Objective: `child_profile_stats_load_failed` on the unavailable-state render path. Definition of Done: fires exactly once per failure occurrence, not once per recomposition.

**Task 07 — Final Code Review**
Objective: Confirm cache-preserved-on-failure behavior, empty-vs-unavailable distinction, isolation guarantee. Definition of Done: checklist in §21 checked.

## 21. Final Verification Checklist
- [x] Cache is never cleared/corrupted on a fetch failure (verified by `ProgressSummaryRepositoryTest`)
- [x] Zero-progress-success and fetch-failure render two distinct, correctly-differentiated states (verified by `ProgressSummaryRepositoryTest` & `StatsSummaryCardTest`)
- [x] Stats-section failure never blocks or visually disrupts sibling Profile sections (PRD §7 Item 5 isolation test passing in `StatsSummaryCardTest`)
- [x] `child_id` derived internally only, never accepted externally (verified by `ChildProfileStructuralTest`)
- [x] Offline rendering works from cache with no blocking network call (verified by `StatsSummaryCardTest`)
- [x] `child_profile_stats_load_failed` fires once per failure with `error_class` metadata and zero PII (verified by `ChildProfileViewModelTest`)
- [x] `403 CHILD_MISMATCH` and `409 SESSION_INVALID` defensive redirection to `Who Is Learning` (verified by `ChildProfileViewModelTest`)
- [x] 100% 4-locale string parity across English (`values`), Arabic RTL (`values-ar`), Urdu RTL (`values-ur`), and Hindi (`values-hi`)
- [x] Strict compliance with design system tokens (0 raw Material3 widgets, 0 hardcoded colors, 0 raw dimensions, 0 `CircleShape`)
- [x] Modularity ceiling strictly enforced: all 19 created and modified files well below 500 lines

## 22. Definition of Done
**Status: COMPLETED**  
The Learning Stats Summary widget renders level/XP/streak/badges from B-01 via a cache-then-refresh Room-backed repository, with a fully isolated graceful-degradation state, ready for use within K-01's `ChildProfileScreen`.

- **Test Suite:** 93 / 93 Tests Passing (`:feature:feature-profile:testAndroidHostTest`); 100% visual parity on Android simulator.
- **Metadata Compilation:** `:shared:compileCommonMainKotlinMetadata` passing cleanly across all multiplatform targets (Android, iOS).
- **Coverage:** DAO Upsert & Observe, Failure-Preserves-Cache Invariance, UI Sibling Isolation Guarantee (PRD §7 Item 5), Zero-Progress vs Fetch-Failure Distinction, Offline Banner & Recovery, 403 CHILD_MISMATCH Defensive Redirect.
