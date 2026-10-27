# K-11 — Rewards Cross-Platform Analytics Instrumentation

## 1. Feature Context
Part of Feature A.11 — Rewards System. Wires the complete §1.19 event taxonomy across every Rewards screen, tied strictly to server-confirmed responses.

## 2. Parent Feature
A.11 Rewards System — KMP App (Android/iOS)

## 3. Sub-feature
K-11 Rewards Cross-Platform Analytics Instrumentation

## 4. Objective
Implement `RewardAnalytics` firing every event from PRD §1.19 via the existing `AnalyticsTracker` interface, tied to server-confirmed responses only, never optimistic UI state.

## 5. Business Requirements
- Every event listed in PRD §1.19 is emitted from the correct screen/action.
- Events fire only after server confirmation (e.g., `wallet_viewed` on a confirmed wallet response, not on cache-only display) so analytics reflect real ledger outcomes.
- No PII in analytics payloads.

## 6. Existing Architecture
Reuses `core-analytics`'s `AnalyticsTracker.logEvent(name, params)` interface (existing, confirmed via `CORE_ANALYTICS_INSTRUCTIONS.md`'s Koin-module registration pattern) — no new analytics SDK or pipeline introduced.

## 7. Existing Code to Reuse
- `AnalyticsTracker` interface (`core-analytics`).
- Existing event-naming/parameter conventions already established by other features' analytics wiring (e.g., A.7's `habit_checked_in`).

## 8. Files to Create
- `feature-rewards/src/commonMain/kotlin/.../analytics/RewardAnalytics.kt` — typed wrapper around `AnalyticsTracker` exposing one function per §1.19 event.
- `feature-rewards/src/commonTest/kotlin/.../analytics/RewardAnalyticsServerConfirmationTest.kt`

## 9. Files to Modify
- K-02 through K-08's ViewModels/screens — wire the appropriate `RewardAnalytics` calls at each documented trigger point.

## 10. Backend Requirements
None new; consumes existing endpoint responses as the confirmation signal for each event.

## 11. KMP Requirements
- `RewardAnalytics` exposes one strongly-typed function per event (e.g., `fun walletViewed()`, `fun badgeUnlocked(badgeId: String)`, `fun achievementStorePurchaseCompleted(itemId: String, newBalance: Int)`) rather than free-form string/map construction at each call site — reduces the risk of a typo'd event name or missing parameter.
- Every function's implementation is called only from a code path that has already received a successful server response for the relevant action (never from an optimistic-update code path).

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
N/A directly; piggybacks on B-02/B-04/B-05/B-06/B-07/B-08's response confirmations.

## 14. Database Requirements (Local)
N/A.

## 15. Validation
Test asserting each `RewardAnalytics` function is only invoked from call sites gated behind a successful server response type (verified via a structural/lint-style check or a mocked-ViewModel test per event, per PRD §6.6 Android convention: "tied to actual server-confirmed responses (not optimistic UI state alone)").

## 16. Authentication
N/A.

## 17. Authorization
N/A.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Analytics call fails silently (network-level, handled by `AnalyticsTracker` internally) | No impact on the calling screen's own success/error state — analytics failures are non-blocking |

## 19. Offline First
Analytics events queued by `AnalyticsTracker`'s own existing offline-buffering behavior (if any) — this task does not introduce a separate queue.

## 20. Local Data
N/A.

## 21. Localization
N/A (event names/params are not user-facing strings).

## 22. RTL
N/A.

## 23. Analytics
This entire sub-feature *is* the analytics wiring; full event list per PRD §1.19: `reward_ledger_entry_created`, `badge_unlocked`, `achievement_level_progressed`, `wallet_viewed`, `weekly_challenge_viewed/joined/completed/claimed/archived_viewed`, `daily_mission_viewed/completed`, `seasonal_event_banner_viewed/entered`, `achievement_store_viewed/item_viewed/purchase_attempted/purchase_completed/purchase_insufficient_points`, `avatar_item_equipped_post_purchase`, `family_board_viewed`, `family_goal_progress_updated`, `family_achievement_unlocked`, `achievement_share_gate_opened/completed`.

## 24. Performance
`AnalyticsTracker` calls are fire-and-forget from the calling screen's perspective; no blocking on the UI thread.

## 25. Security
No PII in any event payload — verified per event during code review; masked/child-safe identifiers only where an identifier is needed at all.

## 26. Library Requirements
`core-analytics`'s existing `AnalyticsTracker`.

## 27. Testing
- Unit: server-confirmation-gating test per event category (mandatory).
- Integration: full flow per screen (K-02–K-08) firing the correct event at the correct trigger point.

## 28. Documentation
KDoc listing every event this module owns, cross-referenced against PRD §1.19, so future contributors can see the full taxonomy in one place.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement `RewardAnalytics` Typed Wrapper**
- Files to Create: `RewardAnalytics.kt`
- Implementation Details: one function per §1.19 event.
- Definition of Done: full event taxonomy covered, no free-form event construction at call sites.

**Task 02 — Wire Wallet/Achievements/Missions Events**
- Files to Modify: K-02, K-03, K-04, K-06 ViewModels.
- Tests: server-confirmation-gating tests.
- Definition of Done: correct events fire at correct trigger points.

**Task 03 — Wire Store/Family Board/Sharing Events**
- Files to Modify: K-07, K-08, K-05 ViewModels.
- Definition of Done: correct events fire at correct trigger points.

**Task 04 — Documentation & Final Review**
- Documentation: event-taxonomy KDoc per §28.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Every PRD §1.19 event wired, fired only on server-confirmed outcomes, with no PII in any payload.

## 31. Final Verification Checklist
- [x] All §1.19 events implemented in `RewardAnalytics` (all 27 PRD §1.19 events exposed as strongly-typed functions + `ALL_PRD_1_19_EVENTS` set)
- [x] Every event verified to fire only post-server-confirmation (`isServerConfirmed == true`), never on optimistic state alone (`WalletEvent.ApplyOptimisticDelta`) or offline Room cache fallbacks (`isOffline == true`)
- [x] No PII present in any event payload (`RewardAnalytics.sanitizeNoPii` strips `child_id`, `family_id`, `parent_id`, `nickname`, `email`, `phone`, `dob`, etc.)
- [x] Each K-02–K-08 screen/ViewModel (`WalletViewModel`, `TransactionViewModel`, `AchievementsViewModel`, `ShareCardViewModel`, `MissionsViewModel`, `AchievementStoreViewModel`, `FamilyBoardViewModel`, and `RewardsModule.kt`) wired to the correct events
- [x] KDoc lists the full event taxonomy and architectural invariants

---

## 32. Verification Sign-Off Ledger (2026-09-26)
- **Implementation & Test Suite**:
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/analytics/RewardAnalytics.kt`
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/di/RewardsModule.kt`
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/wallet/WalletViewModel.kt`
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/wallet/TransactionViewModel.kt`
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/achievements/AchievementsViewModel.kt`
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/missions/MissionsViewModel.kt`
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/store/AchievementStoreViewModel.kt`
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/family/FamilyBoardViewModel.kt`
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/sharing/ShareCardViewModel.kt`
  - `feature/feature-rewards/src/commonTest/kotlin/com/noorheroes/feature/rewards/analytics/RewardAnalyticsServerConfirmationTest.kt`
  - `feature/feature-rewards/src/commonTest/kotlin/com/noorheroes/feature/rewards/analytics/RewardAnalyticsViewModelGatingTest.kt`
- **Automated Verification**:
  - `python recheck_zero_gaps.py`: **0 violations across all 61 `:feature:feature-rewards` files / 146 git-status files** (`NoorHeroes/docs/rule.md` compliance).
  - `./gradlew :feature:feature-rewards:testAndroidHostTest`: **136/136 tests passing** (`BUILD SUCCESSFUL`).


