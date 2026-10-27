# K-06 — Daily Mission & Weekly Challenge Experience

## 1. Feature Context
Part of Feature A.11 — Rewards System. Renders Daily Missions (3/day), the Weekly Challenge, Seasonal Events, and the Archived Challenge view, with claim handling.

## 2. Parent Feature
A.11 Rewards System — KMP App (Android/iOS)

## 3. Sub-feature
K-06 Daily Mission & Weekly Challenge Experience

## 4. Objective
Build the Weekly Challenge Card/Detail, Daily Mission List, Seasonal Event Banner/Screen, Archived Challenge View, and Reward Claim Confirmation (§1.18 #10–16), backing FR-10.

## 5. Business Requirements
- Progress synced from `GET /v1/missions`; claim action updates the wallet in place.
- Archived Challenge View renders expired-but-not-deleted challenges distinctly.
- Duplicate-claim UI race avoided by disabling the Claim button on tap (server-side idempotency per B-05 is the actual guarantee; this is a UX-quality complement, not the safety mechanism).

## 6. Existing Architecture
`feature-rewards` module. Consumes B-05 via K-01's `MissionsRepository`.

## 7. Existing Code to Reuse
- K-01's `MissionsRepository`.
- `core-design-system` progress-bar/challenge-card tokens.
- `core-navigation` deep-link handling (`noorheroes://rewards/challenges`).

## 8. Files to Create
- `feature-rewards/src/commonMain/kotlin/.../missions/MissionsViewModel.kt`
- `feature-rewards/src/commonMain/kotlin/.../missions/DailyMissionListSection.kt`
- `feature-rewards/src/commonMain/kotlin/.../missions/WeeklyChallengeCard.kt`
- `feature-rewards/src/commonMain/kotlin/.../missions/WeeklyChallengeDetailScreen.kt`
- `feature-rewards/src/commonMain/kotlin/.../missions/ArchivedChallengeScreen.kt`
- `feature-rewards/src/commonMain/kotlin/.../missions/SeasonalEventBanner.kt`, `SeasonalEventScreen.kt`
- `feature-rewards/src/commonMain/kotlin/.../missions/RewardClaimConfirmation.kt`
- `feature-rewards/src/commonTest/kotlin/.../missions/MissionsViewModelTest.kt`

## 9. Files to Modify
- `core-navigation` `Route` registry — Weekly Challenge Detail, Archived Challenge, Seasonal Event routes.
- Deep-link handler — `noorheroes://rewards/challenges`.

## 10. Backend Requirements
Consumes B-05 (`GET /v1/missions`, `POST /v1/missions/{id}/progress`).

## 11. KMP Requirements
- `MissionsViewModel` distinguishes active vs. archived challenge state from the response's `expires_at`, rendering the Archived variant automatically — never a manually-toggled client-side flag.
- Claim button disabled immediately on tap (optimistic UI lock), re-enabled only on error response, to complement (not replace) B-05's server-side idempotency.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
`GET /v1/missions`, `POST /v1/missions/{id}/progress` (B-05).

## 14. Database Requirements (Local)
Room cache of last-fetched missions/challenge response for offline display; claim actions require connectivity consistent with other write-adjacent actions in this feature area (progress-reporting itself, per B-05 §19, is safely retriable via outbox if the platform's general sync-queue pattern is applied here — confirm against K-10's outbox scope before assuming automatic inclusion).

## 15. Validation
UI test: an expired challenge is rendered via `ArchivedChallengeScreen`, never omitted or shown as a 404/empty state.

## 16. Authentication
Reuses shared `core-network` Bearer token attachment.

## 17. Authorization
N/A at UI layer.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Missions fetch failure | Cached missions shown with offline indicator |
| Claim failure (network) | Claim button re-enabled, retry affordance shown, no premature "claimed" state |
| Claim on an already-claimed instance | Server returns idempotent original result; UI shows the same success state without treating it as an error |

## 19. Offline First
Cached mission/challenge state with sync-on-reconnect for reads; claims themselves require connectivity per B-05's design intent (server-authoritative claim confirmation needed for the wallet-update-in-place UX).

## 20. Local Data
```
Remote (GET /v1/missions)
   ↓
MissionsRepository (K-01)
   ↓
Room missions_cache
   ↓
MissionsViewModel state (active/archived derived from expires_at)
```

## 21. Localization
Mission/challenge titles and seasonal (Ramadan/Eid) copy resolved via `locale_key`/translation keys.

## 22. RTL
Card/list layouts mirror correctly for Arabic/Urdu, including seasonal banner text.

## 23. Analytics
`weekly_challenge_viewed/joined/completed/claimed/archived_viewed`, `daily_mission_viewed/completed`, `seasonal_event_banner_viewed/entered` via `AnalyticsTracker`.

## 24. Performance
Mission list/challenge card use stable keys to avoid recomposition thrash when only one item's progress updates.

## 25. Security
No new sensitive data handling.

## 26. Library Requirements
Compose Multiplatform, Koin, Room, kotlinx-coroutines.

## 27. Testing
- Unit: active-vs-archived derivation logic from `expires_at`.
- UI: archived-state rendering, claim-confirmation flow, claim-button disable-on-tap behavior.
- Integration: claim → server confirmation → wallet-update-in-place.

## 28. Documentation
KDoc explaining that claim-button disable-on-tap is a UX complement, not the actual idempotency guarantee (which lives server-side in B-05).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement `MissionsViewModel`**
- Files to Create: `MissionsViewModel.kt`
- Business Rules: FR-10, active/archived derivation.
- Tests: derivation-logic unit test.
- Definition of Done: correct state categorization.

**Task 02 — Build Daily Mission & Weekly Challenge Card/List Composables**
- Files to Create: `DailyMissionListSection.kt`, `WeeklyChallengeCard.kt`
- Definition of Done: correct rendering on Wallet Hub (K-02 integration point) and standalone.

**Task 03 — Build Weekly Challenge Detail & Archived Challenge Screens**
- Files to Create: `WeeklyChallengeDetailScreen.kt`, `ArchivedChallengeScreen.kt`
- Tests: archived-state UI test (mandatory).
- Definition of Done: test passing.

**Task 04 — Build Seasonal Event Banner/Screen**
- Files to Create: `SeasonalEventBanner.kt`, `SeasonalEventScreen.kt`
- Localization/RTL: per §21/§22.
- Definition of Done: correctly rendered when a seasonal event is active.

**Task 05 — Build Reward Claim Confirmation with Idempotent-Aware UX**
- Files to Create: `RewardClaimConfirmation.kt`
- Implementation Details: claim-button disable-on-tap, re-enable-on-error.
- Tests: claim-flow integration test.
- Definition of Done: verified.

**Task 06 — Wire Navigation & Deep Links**
- Files to Modify: `core-navigation` `Route` registry, deep-link handler.
- Definition of Done: `noorheroes://rewards/challenges` routes correctly.

**Task 07 — Final Code Review**
- Expected Result: PR merge-ready.

## 30. Definition of Done
Mission/challenge experience live, archive-not-disappear behavior correctly rendered, claim flow robust against duplicate taps and network failure.

## 31. Final Verification Checklist
- [x] Active/archived state correctly derived from `expires_at`, never manually toggled
- [x] Archived challenges rendered distinctly, never omitted
- [x] Claim button disabled on tap, re-enabled only on error
- [x] Deep link `noorheroes://rewards/challenges` verified
- [x] Localization/RTL verified including seasonal content
- [x] Analytics events fire correctly

## 32. Verification Sign-Off & Ledger
- **Status:** Complete & Fully Verified
- **Implementation Date:** 2026-09-25
- **Verified Invariants:**
  - Active vs. Archived challenge state derived strictly from `expires_at` (never manually toggled, never 404/deleted). Both `WeeklyChallengeDetailScreen` and `SeasonalEventScreen` automatically delegate to `ArchivedChallengeScreen` when `isExpired == true`.
  - Idempotent-aware UX: Claim button disabled immediately upon tap, re-enabled only on error, server-authoritative idempotency preserved (`wasDuplicate = true` verified).
  - Production Navigation & Component Integration: Wired in `AppRoot.kt` and `RewardsWalletHubScreen.kt` connecting the wallet weekly challenge card to `WeeklyChallengeDetailScreen`, with `SeasonalEventBanner` and `DailyMissionListSection` integrated into the challenge & seasonal detail views.
  - Seasonal Event Experience: Ramadan/Eid banner and dedicated screen with full claim lifecycle, expired archive delegation, and state persistence verified.
  - Challenge Lookup: Explicit ID matching with fallback gracefully handles multi-event state.
  - Design system compliance: Zero raw `.dp`, zero raw `.sp`, zero raw `Color(0x...)`, zero raw M3 components, all files < 500 lines.
  - 100% 4-locale parity across EN, AR, HI, and UR (239 keys in `strings_rewards.xml` across all 4 locales).
  - Multiplatform verification: Full unit test suite passed (122/122 tests, 0 failures across `feature-rewards` [96 tests: 22 in `MissionsViewModelTest` + 6 in `ArchivedChallengeUiTest` + 68 existing] & `rewards-client` [26 tests]), iOS Simulator Arm64 compilation passed, Android app compilation passed.
- **Lead Architect / Author:** @author Sarvare Alam

