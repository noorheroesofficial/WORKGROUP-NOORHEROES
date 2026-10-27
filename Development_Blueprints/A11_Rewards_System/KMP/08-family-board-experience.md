# K-08 — Family Board Experience

## 1. Feature Context
Part of Feature A.11 — Rewards System. Celebrates shared sibling accomplishment via a single immersive, aggregate-only visual — conceptually paired with, but visually distinct from, A.7's Noor Garden.

## 2. Parent Feature
A.11 Rewards System — KMP App (Android/iOS)

## 3. Sub-feature
K-08 Family Board Experience

## 4. Objective
Build the Family Board, Family Goal Detail, and Family Achievement Unlock Celebration screens (§1.18 #20–22), backing FR-9, FR-15.

## 5. Business Requirements
- Aggregate-only visualization — never simultaneous side-by-side sibling comparison, enforced as a layout constraint.
- Empty state: new multi-child family, "let's start together" framing.
- Celebration trigger on threshold crossing, dismiss → Family Board.

## 6. Existing Architecture
`feature-rewards` module. Consumes B-07 via K-01's `FamilyBoardRepository`. Mirrors A.7's Noor Garden's no-comparison layout-constraint pattern (A.7 K-05), applied to this feature's own visual treatment.

## 7. Existing Code to Reuse
- K-01's `FamilyBoardRepository` and its structurally-tested `FamilyBoardDto`.
- A.7's Noor Garden no-comparison layout pattern as design precedent (not shared code, since the visual treatment is deliberately distinct per PRD §2.4).

## 8. Files to Create
- `feature-rewards/src/commonMain/kotlin/.../family/FamilyBoardScreen.kt`
- `feature-rewards/src/commonMain/kotlin/.../family/FamilyGoalDetailScreen.kt`
- `feature-rewards/src/commonMain/kotlin/.../family/FamilyAchievementCelebrationModal.kt`
- `feature-rewards/src/commonMain/kotlin/.../family/FamilyBoardViewModel.kt`
- `feature-rewards/src/androidInstrumentedTest/kotlin/.../family/FamilyBoardNoComparisonUiTest.kt`

## 9. Files to Modify
- `core-navigation` `Route` registry — Family Board, Family Goal Detail routes.
- Deep-link handler — `noorheroes://rewards/family-board`.

## 10. Backend Requirements
Consumes B-07 (`GET /v1/family/{family_id}/board`).

## 11. KMP Requirements
- `FamilyBoardViewModel` consumes K-01's structurally-verified `FamilyBoardDto` — no local transformation ever introduces a per-child field.
- Layout constraint enforced in the Composable itself: only aggregate/single-progress visuals are composable within this screen's component tree (no sibling-indexed list/grid component exists in this screen's implementation).

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
`GET /v1/family/{family_id}/board` (B-07).

## 14. Database Requirements (Local)
Room cache of last-fetched board response for offline display.

## 15. Validation
UI test (mandatory, CI-blocking): Family Board screen renders with zero per-child comparative UI elements — verified by scanning the rendered Compose tree/semantics for any element bound to a per-sibling data source, mirroring B-07's backend structural test.

## 16. Authentication
Reuses shared `core-network` Bearer token attachment.

## 17. Authorization
N/A at UI layer (server-side family-scoping per B-07).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Fetch failure | Cached board shown with offline indicator |
| New multi-child family, zero contributions | "Let's start together" empty-state framing |
| Threshold crossed while screen is open | Celebration modal triggers in place, no manual refresh required |

## 19. Offline First
Cached aggregate progress with sync-on-reconnect; celebration triggers only on a confirmed server-side threshold-crossing signal, not client-inferred.

## 20. Local Data
```
Remote (GET /v1/family/{family_id}/board)
   ↓
FamilyBoardRepository (K-01)
   ↓
Room family_board_cache
   ↓
FamilyBoardViewModel state (aggregate-only)
```

## 21. Localization
Goal titles/descriptions resolved via `locale_key`; celebration copy localized EN/HI/AR/UR.

## 22. RTL
Immersive illustrated layout mirrors correctly for Arabic/Urdu (text overlays, progress labels).

## 23. Analytics
`family_board_viewed`, `family_goal_progress_updated` (aggregate only), `family_achievement_unlocked`.

## 24. Performance
Illustrated/animated visuals kept lightweight (vector/Lottie-style assets per existing design-system convention, not heavy raster sequences) to avoid jank on lower-end devices.

## 25. Security
No new sensitive data handling; the primary property here is the no-comparison UI guarantee (§15), a child-wellbeing/trust property rather than a data-confidentiality one.

## 26. Library Requirements
Compose Multiplatform, Koin, Room, kotlinx-coroutines.

## 27. Testing
- Unit: aggregate-progress display-mapping logic.
- UI: no-comparison structural test (mandatory, CI-blocking), empty-state rendering, celebration-trigger-and-dismiss flow.

## 28. Documentation
KDoc explicitly stating the layout-constraint rule: this screen's component tree must never include a sibling-indexed data-bound element, cross-referenced against B-07's backend guarantee.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement `FamilyBoardViewModel`**
- Files to Create: `FamilyBoardViewModel.kt`
- Existing Files to Reuse: K-01's `FamilyBoardRepository`.
- Definition of Done: correct aggregate-only state exposed.

**Task 02 — Build `FamilyBoardScreen` & `FamilyGoalDetailScreen`**
- Files to Create: both screens.
- Implementation Details: aggregate-only visuals, empty-state framing.
- Localization/RTL: per §21/§22.
- Definition of Done: correctly rendered, structurally free of per-sibling UI.

**Task 03 — Build `FamilyAchievementCelebrationModal`**
- Files to Create: celebration modal.
- Implementation Details: triggered on server-confirmed threshold crossing, dismiss → Family Board.
- Definition of Done: verified via test.

**Task 04 — Implement No-Comparison Structural UI Test (Mandatory CI Gate)**
- Files to Create: `FamilyBoardNoComparisonUiTest.kt`
- Definition of Done: test passes, wired as non-bypassable CI gate.

**Task 05 — Wire Navigation & Deep Link**
- Files to Modify: `core-navigation` `Route` registry, deep-link handler.
- Definition of Done: `noorheroes://rewards/family-board` verified.

**Task 06 — Final Code Review**
- Do Not Change: never introduce a per-sibling data-bound UI element to this screen.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Family Board experience live, structurally verified (backend + client) to carry zero per-sibling comparison, celebration flow correct.

## 31. Final Verification Checklist
- [x] No-comparison structural UI test passes (CI-blocking)
- [x] Empty state shows "let's start together" framing
- [x] Celebration modal triggers on confirmed threshold crossing, dismiss returns to Family Board
- [x] Deep link `noorheroes://rewards/family-board` verified
- [x] Localization/RTL verified (EN/AR/HI/UR 4-locale parity across 322 keys)
- [x] Offline cached display verified with automatic sync-on-reconnect

## 32. Verification Sign-Off Ledger
- **Status**: COMPLETED & RE-VERIFIED WITH ZERO MISSING SCENARIOS (2026-09-26)
- **Author**: Sarvare Alam
- **Created / Updated Files**:
  - `core/rewards-client/src/commonMain/kotlin/com/noorheroes/core/rewards/client/data/dto/FamilyBoardDto.kt` (47 lines): Aggregate-only `FamilyBoardDto` & `FamilyGoalDto` with optional aggregate summary and goal metadata (`habits_this_month`, `total_family_participants`, `badges_earned_together`, `description`, `locale_key`, `reward_xp`, `reward_points`) verified by `FamilyBoardDtoReflectionTest`.
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/family/FamilyBoardUiState.kt` (328 lines): Aggregate-only `@Serializable` UI models (`FamilyGoalUiModel`, `FamilySummaryStatsUiModel`, `FamilyCelebrationUiModel`, `FamilyMilestoneStageUiModel`, `FamilyBoardUiState`), `FamilyBoardMapper` (`mapGoals`, `mapGoal`, `mapSummaryStats`), and `FamilyBoardAuditHelper`.
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/family/FamilyBoardViewModel.kt` (363 lines): MVI state orchestration consuming `FamilyBoardRepository`, `ConnectivityObserver`, `AuthStateProvider`, `AnalyticsTracker` (`family_board_viewed`, `family_goal_progress_updated`, `family_achievement_unlocked`), `"Let's start together"` empty-state detection, offline Room cache fallback with sync-on-reconnect, and server-confirmed threshold-crossing celebration triggering.
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/family/FamilyTreeJourneyIllustration.kt` (245 lines): Immersive vector/Compose illustration matching `Screens/Mobile App/Rewards/Family Board.png` (shared glowing Noor Tree with golden fruit orbs, rolling emerald hills, curved dashed trail, teal 4-point star waypoints `✦`, 3 abstract glowing golden light orbs feeding diagonal light rays into the shared tree, and RTL horizontal mirroring — zero human figures or sibling comparison elements).
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/family/FamilyBoardComponents.kt` (412 lines): `resolveLocalizedGoalTitle` & `resolveLocalizedGoalDescription` (`locale_key` support), `FamilyBoardTopHeader` (with RTL arrow mirroring), `FamilyGoalProgressCard` (`"100 Du'as Together"`, `"70/100"`, `"Combined family progress"`, `"30 to next milestone"`, true `0f` fill on `0%`), `FamilyAggregateSummaryCard` (`847 habits this month`, `3 family members`, `12 badges earned`, `"Individual progress available in Parent Dashboard"`), and `FamilyEmptyStartTogetherCard` (`"Let's start together! 🌱"`).
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/family/FamilyBoardScreen.kt` (197 lines): Root Composable for `Family Board.png` with in-place `FamilyAchievementCelebrationModal` overlay, snackbar error handling, and offline banner.
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/family/FamilyGoalDetailScreen.kt` (360 lines): Shared goal detail screen (§1.18 #21) with 4 cooperative growth stages (`25% Shared Roots`, `50% Growing Trunk`, `75% Glowing Canopy`, `100% Radiant Family Tree` + milestone counts), snackbar error handling, and contribution guide.
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/family/FamilyAchievementCelebrationModal.kt` (181 lines): Server-confirmed Family Achievement Unlock Celebration modal (§1.18 #22) with dismiss-to-board navigation.
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/navigation/FamilyBoardDeepLinkHandler.kt` (100 lines): Deep-link parser and router for `noorheroes://rewards/family-board` and `?goal_id=...`.
  - `core/core-navigation/src/commonMain/kotlin/com/noorheroes/core/navigation/RewardsRoutes.kt` (167 lines): Added `FamilyGoalDetailRoute(val goalId: String)` alongside `FamilyBoardRoute`.
  - `shared/src/commonMain/kotlin/com/noorheroes/app/navigation/RewardsNavGraph.kt` (236 lines) & `AppRoot.kt` (225 lines): Registered `FamilyBoardRoute` and `FamilyGoalDetailRoute` in the shared navigation graph.
  - `feature/feature-rewards/src/commonTest/kotlin/com/noorheroes/feature/rewards/family/FamilyBoardNoComparisonUiTest.kt` (221 lines), `FamilyBoardViewModelTest.kt` (302 lines), `FamilyBoardTestFakes.kt` (125 lines), and `src/androidInstrumentedTest/kotlin/com/noorheroes/feature/rewards/family/FamilyBoardNoComparisonUiTest.kt` (116 lines): 19 Family Board unit, structural, and instrumented tests (`122/122` total passing tests in `:feature:feature-rewards:testAndroidHostTest`, `0 violations` on `audit_k08.py`).


