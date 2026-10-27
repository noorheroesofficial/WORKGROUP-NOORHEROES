# K-10 — Rewards Data Freshness & Cross-Screen Invalidation Engine

## 1. Feature Context
Part of Feature A.11 — Rewards System. Ensures the Wallet Hub and related screens never display a stale cache after a reward was awarded from a *different* feature's screen (e.g., a Habit check-in, a Story completion) — a direct consequence of K-01 §6's correction that reward issuance is backend-orchestrated per-feature rather than a client-side shared call the Rewards module could observe directly.

## 2. Parent Feature
A.11 Rewards System — KMP App (Android/iOS)

## 3. Sub-feature
K-10 Rewards Data Freshness & Cross-Screen Invalidation Engine

## 4. Objective
Implement a cache-freshness strategy so that navigating into any Rewards screen (Wallet Hub, Achievements, Missions) always triggers a fresh fetch when the local cache could plausibly be stale, rather than trusting an indefinitely-long cache lifetime.

## 5. Business Requirements
- A child who checks in a habit (A.7), then immediately opens the Rewards tab, must see the updated balance, not a pre-award cached snapshot (a direct UX consequence of FR-13's "optimistic, reconciled" promise applying platform-wide, not just within the Rewards feature's own screens).
- No indefinite cache staleness: a simple "always refetch on screen-enter, with cache as instant-paint fallback while the fresh fetch completes" strategy is acceptable and matches the existing platform convention (remote-first, cache-as-fallback, not cache-first).

## 6. Existing Architecture
Extends `:core:rewards-client` (K-01). Because there is no shared client-side "reward was just awarded" event bus (the corrected architecture per K-01 §6 keeps award issuance entirely server-side, per-feature), this module solves the freshness problem structurally at the read layer instead: every Rewards screen's `ViewModel.onScreenEnter()` triggers a network refresh unconditionally (remote-first), using the Room cache purely as the instant-paint layer while that refresh is in flight — never as a substitute for a fresh read.

## 7. Existing Code to Reuse
- K-01's `WalletRepository`/`MissionsRepository`/etc. — this task adds a consistent `refreshOnEnter()` convention to each, not a new repository.
- `core-navigation`'s lifecycle-aware navigation callback (screen-enter detection), if the platform's `Navigator`/`Route` pattern already exposes one; otherwise standard Compose `LaunchedEffect(Unit)`-on-composition per screen, following whatever the project's established "refresh on screen enter" idiom already is elsewhere (confirm via an existing example, e.g. Home's own remote-first refresh pattern, before introducing a new idiom).

## 8. Files to Create
- `core/rewards-client/src/commonMain/kotlin/.../data/RewardsFreshnessPolicy.kt` — shared "always remote-first, cache-as-fallback" policy applied consistently across `WalletRepository`, `MissionsRepository`, `AchievementStoreRepository`, `FamilyBoardRepository`.
- `core/rewards-client/src/commonTest/kotlin/.../data/RewardsFreshnessPolicyTest.kt`

## 9. Files to Modify
- K-01's repository implementations — apply the freshness policy consistently (cache read is a fallback for the *display* layer while a fetch is in flight, never a reason to skip the fetch).
- K-02, K-04, K-06's ViewModels — ensure each calls its repository's remote-first refresh on screen composition, not only on pull-to-refresh.

## 10. Backend Requirements
None new; relies on B-02's existing short-TTL server-side cache invalidation (on new ledger entry) as the source-of-truth freshness guarantee — this client-side task ensures the client actually *asks* at the right moments, complementing rather than duplicating that guarantee.

## 11. KMP Requirements
- Every Rewards screen ViewModel triggers a remote fetch on screen-enter (not merely on first app launch), with the last-cached value painted instantly while that fetch resolves, then replaced once the fresh response arrives.
- No screen in this feature ever displays only a cached value with a live network path available and unused — cache is a *fallback for offline*, not a default *instead of* fetching.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
Reuses B-02/B-04/B-05/B-06/B-07 exactly as already specified in K-01; no new endpoint.

## 14. Database Requirements (Local)
No new tables; this task governs *when* K-01's existing Room caches are read vs. refreshed, not their schema.

## 15. Validation
Integration test: simulate an award occurring "elsewhere" (direct fixture ledger insert, bypassing the app), then navigate into the Wallet Hub screen — assert the displayed balance reflects the fresh value within one screen-enter cycle, not the stale pre-award cache.

## 16. Authentication
N/A (policy-layer concern, reuses existing auth).

## 17. Authorization
N/A.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Screen-enter refresh fails (offline) | Falls back to last-cached value with an offline indicator, consistent with each screen's already-documented offline state |
| Rapid repeated screen-enters (e.g., fast tab-switching) | Refresh calls are debounced/de-duplicated to avoid redundant network load |

## 19. Offline First
Cache remains the offline fallback exactly as documented per-screen (K-02/K-04/K-06/K-07/K-08); this task only changes the *online* default from "cache-first" to "remote-first, cache-as-instant-paint."

## 20. Local Data
No schema change; behavioral policy only, applied across K-01's existing cache tables.

## 21. Localization
N/A.

## 22. RTL
N/A.

## 23. Analytics
No new events; existing `*_viewed` events (K-02/K-04/K-06) now correspond to a genuine fresh-data view rather than a potentially-stale cached one.

## 24. Performance
Debounce/de-duplicate rapid repeated refresh triggers to avoid unnecessary network load on fast navigation; refresh must not block the initial cached paint (perceived performance preserved).

## 25. Security
No new sensitive data handling.

## 26. Library Requirements
Compose Multiplatform lifecycle APIs, Koin, kotlinx-coroutines (debounce operators).

## 27. Testing
- Unit: freshness-policy debounce/de-duplication logic.
- Integration: cross-screen staleness scenario per §15 (mandatory).

## 28. Documentation
KDoc explaining *why* this module exists: it is the client-side mitigation for the architectural trade-off accepted in K-01 §6 (no shared client-side reward-event bus), documented so a future contributor understands the reasoning rather than reintroducing a stale-cache bug.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement `RewardsFreshnessPolicy`**
- Files to Create: `RewardsFreshnessPolicy.kt`
- Implementation Details: remote-first-with-cache-fallback helper applied consistently across K-01's repositories.
- Tests: debounce/de-duplication unit test.
- Definition of Done: policy correctly wraps each repository's read path.

**Task 02 — Apply Policy to K-01's Repositories**
- Files to Modify: `WalletRepository.kt`, `MissionsRepository.kt`, `AchievementStoreRepository.kt`, `FamilyBoardRepository.kt`
- Definition of Done: each repository refreshes remotely on every call, using cache only as instant-paint/offline fallback.

**Task 03 — Wire Screen-Enter Refresh Triggers**
- Files to Modify: K-02, K-04, K-06's ViewModels
- Definition of Done: each screen refreshes on enter, not only on first load or manual pull-to-refresh.

**Task 04 — Implement Cross-Screen Staleness Integration Test (Mandatory)**
- Files to Create: `RewardsFreshnessPolicyTest.kt` (and a cross-screen integration test alongside it)
- Definition of Done: test per §15 passing.

**Task 05 — Documentation & Final Review**
- Documentation: KDoc per §28.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Every Rewards screen reliably shows fresh data after a reward awarded elsewhere in the app, without introducing excessive redundant network calls.

## 31. Final Verification Checklist
- [x] Cross-screen staleness integration test passes (award-elsewhere → fresh Wallet Hub read)
- [x] Rapid repeated screen-enters debounced/de-duplicated
- [x] Offline fallback behavior unchanged (cache still serves when genuinely offline)
- [x] All Rewards screens' ViewModels apply the freshness policy consistently
- [x] KDoc documents the architectural rationale

## 32. Verification Sign-Off Ledger (Executed 2026-09-26)
- **Status**: COMPLETED & VERIFIED (2026-09-26)
- **Author**: Sarvare Alam
- **Shared Freshness & Invalidation Policy**:
  - Implemented `RewardsFreshnessPolicy` (`core/rewards-client/src/commonMain/kotlin/com/noorheroes/core/rewards/client/data/RewardsFreshnessPolicy.kt`, 221 lines) providing remote-first reads, Room cache persistence/fallback, concurrent in-flight request de-duplication (`CompletableDeferred`), rapid screen-enter debounce (`DEFAULT_DEBOUNCE_WINDOW_MS = 500L`), `invalidateScope(scopeKey)`, `invalidateAllChildScopes(childId)`, and `invalidateAllFamilyScopes()`.
- **Repository Integration (All 5 K-01 Repositories)**:
  - Applied `RewardsFreshnessPolicy` and `refreshOnEnter(childId/familyId, forceRefresh)` across `WalletRepositoryImpl`, `MissionsRepositoryImpl`, `AchievementsRepositoryImpl`, `AchievementStoreRepositoryImpl`, and `FamilyBoardRepositoryImpl`, with cross-screen scope invalidation on `claimMission`, `purchaseStoreItem`, and `recordFamilyGoalContribution`, plus singleton DI binding in `RewardsClientModule`.
- **ViewModel & Screen-Enter Triggers (All 12 Rewards Screens & Sub-Screens)**:
  - Wired `onScreenEnter()` across all 12 screens/sub-screens in `:feature:feature-rewards`:
    1. `RewardsWalletHubScreen` (`WalletViewModel.onScreenEnter()`)
    2. `TransactionHistoryScreen` (`TransactionHistoryViewModel.onScreenEnter()`)
    3. `TransactionDetailScreen` (`TransactionHistoryViewModel.onScreenEnter()`)
    4. `AchievementsScreen` (`AchievementsViewModel.onScreenEnter()`)
    5. `BadgeDetailScreen` (`AchievementsViewModel.onScreenEnter()`)
    6. `AchievementLevelDetailScreen` (`AchievementsViewModel.onScreenEnter()`)
    7. `WeeklyChallengeDetailScreen` (`MissionsViewModel.onScreenEnter()`)
    8. `ArchivedChallengeScreen` (`MissionsViewModel.onScreenEnter()`)
    9. `SeasonalEventScreen` (`MissionsViewModel.onScreenEnter()`)
    10. `AchievementStoreScreen` (`AchievementStoreViewModel.onScreenEnter()`)
    11. `StoreItemDetailScreen` (`AchievementStoreViewModel.onScreenEnter()`)
    12. `FamilyBoardScreen` (`FamilyBoardViewModel.onScreenEnter()`)
- **18-Screen KMP UI Fidelity Audit (`Screens/Mobile App/Rewards`)**:
  - Verified 100% visual, structural, and data-model parity across `Rewards Wallet-01..09.png`, `Achievements-01..04.png`, `Achievement Store-01..04.png`, and `Family Board.png`.
- **Automated Verification**:
  - `:core:rewards-client:testAndroidHostTest` (`RewardsFreshnessPolicyTest`, 7 unit tests) — **PASSED**
  - `:feature:feature-rewards:testAndroidHostTest` (`CrossScreenFreshnessInvalidationTest`, 6 end-to-end tests covering §15 cross-screen staleness, rapid debounce, offline fallback, Achievements/Missions refresh, and cross-screen mutation invalidation) — **PASSED**
  - `recheck_zero_gaps.py` (`NoorHeroes/docs/rule.md` compliance across 141 files) — **0 violations**


