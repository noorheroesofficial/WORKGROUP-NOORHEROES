# Visual & System Blueprint: A11 Rewards System

## 1. Feature Context & Metadata
- **Feature Directory**: `Development_Blueprints/A11_Rewards_System/`
- **Target Feature ID**: A11
- **Related PRD Document**: `PRD_Documents/Child App (1-12)/Feature_A11_Rewards_System.md`
- **Mapped Screen Count**: 18 Screens Total
- **Primary User Role**: Child Learner
- **Feature Purpose**: Noor Stars/Coins Wallet, Achievements, Store & Family Board

---

## 2. Mandatory AI Implementation Directives (Multi-Image Rule)
> **CRITICAL MANDATORY AI INSTRUCTION:**
> For any screen or flow represented by multiple images in this feature, the AI coding agent **MUST read and inspect ALL constituent screen images collectively** before generating any UI, ViewModel, or API binding code.
> The agent must **NOT** implement a partial screen from a single image. It must synthesize all visual states (Initial, Populated, Active Input, Validation Error, Dialogs, Loading Spinners, and Empty States) into a single cohesive, production-ready component.

---

## 3. Exhaustive Screen Inventory & Exact File Paths (18 Screens Total)

| # | Exact Screen Image File Path | Screen Title / Visual State | UI Role | Primary API Dependency |
|---|---|---|---|---|
| 01 | `Screens/Mobile App/Rewards/Achievement Store-01.png` | Achievement Store 01 | Child Learner | Sourced from Backend/KMP task files |
| 02 | `Screens/Mobile App/Rewards/Achievement Store-02.png` | Achievement Store 02 | Child Learner | Sourced from Backend/KMP task files |
| 03 | `Screens/Mobile App/Rewards/Achievement Store-03.png` | Achievement Store 03 | Child Learner | Sourced from Backend/KMP task files |
| 04 | `Screens/Mobile App/Rewards/Achievement Store-04.png` | Achievement Store 04 | Child Learner | Sourced from Backend/KMP task files |
| 05 | `Screens/Mobile App/Rewards/Achievements-01.png` | Achievements 01 | Child Learner | Sourced from Backend/KMP task files |
| 06 | `Screens/Mobile App/Rewards/Achievements-02.png` | Achievements 02 | Child Learner | Sourced from Backend/KMP task files |
| 07 | `Screens/Mobile App/Rewards/Achievements-03.png` | Achievements 03 | Child Learner | Sourced from Backend/KMP task files |
| 08 | `Screens/Mobile App/Rewards/Achievements-04.png` | Achievements 04 | Child Learner | Sourced from Backend/KMP task files |
| 09 | `Screens/Mobile App/Rewards/Family Board.png` | Family Board | Child Learner | Sourced from Backend/KMP task files |
| 10 | `Screens/Mobile App/Rewards/Rewards Wallet-01.png` | Rewards Wallet 01 | Child Learner | Sourced from Backend/KMP task files |
| 11 | `Screens/Mobile App/Rewards/Rewards Wallet-02.png` | Rewards Wallet 02 | Child Learner | Sourced from Backend/KMP task files |
| 12 | `Screens/Mobile App/Rewards/Rewards Wallet-03.png` | Rewards Wallet 03 | Child Learner | Sourced from Backend/KMP task files |
| 13 | `Screens/Mobile App/Rewards/Rewards Wallet-04.png` | Rewards Wallet 04 | Child Learner | Sourced from Backend/KMP task files |
| 14 | `Screens/Mobile App/Rewards/Rewards Wallet-05.png` | Rewards Wallet 05 | Child Learner | Sourced from Backend/KMP task files |
| 15 | `Screens/Mobile App/Rewards/Rewards Wallet-06.png` | Rewards Wallet 06 | Child Learner | Sourced from Backend/KMP task files |
| 16 | `Screens/Mobile App/Rewards/Rewards Wallet-07.png` | Rewards Wallet 07 | Child Learner | Sourced from Backend/KMP task files |
| 17 | `Screens/Mobile App/Rewards/Rewards Wallet-08.png` | Rewards Wallet 08 | Child Learner | Sourced from Backend/KMP task files |
| 18 | `Screens/Mobile App/Rewards/Rewards Wallet-09.png` | Rewards Wallet 09 | Child Learner | Sourced from Backend/KMP task files |

---

## 4. Comprehensive 24-Point Screen Specifications (Applied to All Mapped Screens)

For every screen listed above, future AI coding agents must strictly adhere to the following 24-point implementation contract:

1. **Platform**: Defined per exact image path (Mobile App: Compose Multiplatform / M3; Parent/Admin Web: Next.js 14 App Router / Tailwind / shadcn/ui).
2. **Exact Screen Image Path**: Referenced individually in Section 3 and Section 5 below.
3. **Related PRD Document**: Sourced directly from `PRD_Documents/Child App (1-12)/Feature_A11_Rewards_System.md`.
4. **Related PRD Section/Feature**: Specified in the corresponding feature task markdown files.
5. **Purpose of the Screen**: Accurate visual and interactive reproduction of the design mockups.
6. **User Role**: `Child Learner`.
7. **Entry Point**: Mapped in the feature navigation graph.
8. **Previous Screen**: Documented in navigation state flow.
9. **Next Screen(s)**: Forward navigation destinations upon primary action completion.
10. **Navigation Conditions**: Validated against user authentication state, permissions, and network connectivity.
11. **Required API(s)**: Documented in the `Backend/` task files within this directory.
12. **Required Request Data**: Validated via Pydantic / Zod schemas.
13. **Required Response Data**: Serialized into immutable Kotlin / TypeScript DTOs.
14. **Required UI States**: Full support for Initial Loading, Populated Data, Empty State, Error State, and Action Spinners.
15. **Business Logic**: Enforced via clean architecture domain repositories and use cases.
16. **Validation Rules**: Client-side instant format feedback + authoritative server-side validation.
17. **Error Handling**: Non-blocking toasts or localized error cards with "Retry" buttons.
18. **Loading Behavior**: Shimmer/Skeleton loaders matching the exact card aspect ratios.
19. **Empty-State Behavior**: Themed Islamic illustration with encouraging empty state copy and primary CTA.
20. **Success Behavior**: Smooth animated transition with optional celebratory reward badges / XP particle effects.
21. **Edge Cases**: Long text wrapping, null fields, rapid double-tapping prevention, and graceful offline degradation.
22. **Authentication / Authorization**: Child session token or Parent PIN verification or Admin RBAC permission check.
23. **Permissions**: Camera/Microphone/Storage permissions requested just-in-time with clear parental explanations.
24. **Dependencies**: Upstream services and local SQLite / SQLDelight cache tables.

---

## 5. Detailed Screen-by-Screen Specifications

### Screen 01: `Achievement Store-01.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Rewards/Achievement Store-01.png`
- **3. Related PRD**: `PRD_Documents/Child App (1-12)/Feature_A11_Rewards_System.md`
- **4. Purpose**: Render Achievement Store 01 (Initial 6-card catalog browse state with `✨ All` filter and `✦ 630 NP` wallet header) with full visual fidelity to design assets.
- **5. User Role**: Child Learner
- **6. Navigation**: `AchievementStoreRoute` (`feature/feature-rewards/.../store/AchievementStoreScreen.kt` & `AchievementStoreComponents.kt`).
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 02: `Achievement Store-02.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Rewards/Achievement Store-02.png`
- **3. Related PRD**: `PRD_Documents/Child App (1-12)/Feature_A11_Rewards_System.md`
- **4. Purpose**: Render Achievement Store 02 (`Golden Lantern Avatar` owned item selected with teal border and bottom `"You already own this ✓"` expanded card) with full visual fidelity to design assets.
- **5. User Role**: Child Learner
- **6. Navigation**: `AchievementStoreRoute` (`SelectedStoreItemExpandedCard` in `AchievementStoreComponents.kt`).
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 03: `Achievement Store-03.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Rewards/Achievement Store-03.png`
- **3. Related PRD**: `PRD_Documents/Child App (1-12)/Feature_A11_Rewards_System.md`
- **4. Purpose**: Render Achievement Store 03 (`Star Sprout Avatar` unowned item selected with teal border and bottom `"Get for 150 NP"` purchase card) with full visual fidelity to design assets.
- **5. User Role**: Child Learner
- **6. Navigation**: `AchievementStoreRoute` -> `StoreItemDetailRoute` / `PurchaseConfirmationRoute` / `InsufficientPointsShortfallRoute`.
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 04: `Achievement Store-04.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Rewards/Achievement Store-04.png`
- **3. Related PRD**: `PRD_Documents/Child App (1-12)/Feature_A11_Rewards_System.md`
- **4. Purpose**: Render Achievement Store 04 (`🏅 Badges` category filtered view with `Quranic Explorer Badge` selected and `"Get for 60 NP"` CTA) with full visual fidelity to design assets.
- **5. User Role**: Child Learner
- **6. Navigation**: `AchievementStoreRoute` (`StoreCategory.BADGES` filter active).
- **7. UI State Handling**: Implements Shimmer Loading, Populated State, Empty State, Error State, and Action Loading.
- **8. Design System Tokens**: Follows project typography, fluid sizing tokens, M3 elevation, and full RTL layout support.

### Screen 05: `Achievements-01.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Rewards/Achievements-01.png`
- **3. Related PRD**: `PRD_Documents/Child App (1-12)/Feature_A11_Rewards_System.md` & Blueprint `KMP/04-achievements-screen-badge-grid-milestone-path.md`
- **4. Purpose**: Render Achievements 01 (`🏅 Badges` tab selected, `"🏅 5 of 12 earned"` gold pill, `"7 to unlock"`, `EARNED` 3-column grid with `Quran Star`, `Story Explorer`, `Daily Scholar`, `Story Seeker`, `Hafiz Seedling`, and top of `LOCKED` grid).
- **5. User Role**: Child Learner
- **6. Navigation**: `AchievementsRoute` (`feature/feature-rewards/.../achievements/AchievementsScreen.kt` & `achievements/components/BadgeGridSection.kt`) -> `BadgeDetailRoute(badgeId)` (`achievements/BadgeDetailScreen.kt`).
- **7. UI State Handling**: Managed by `AchievementsViewModel.kt` (`onScreenEnter()` remote-first refresh via `RewardsFreshnessPolicy`), Shimmer Loading, Populated State, Empty State Teaser, Offline Banner, and `BadgeUnlockModal`.
- **8. Design System Tokens**: Strictly consumes `NoorHeroesTheme` tokens with 4-locale parity and RTL layout support.

### Screen 06: `Achievements-02.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Rewards/Achievements-02.png`
- **3. Related PRD**: `PRD_Documents/Child App (1-12)/Feature_A11_Rewards_System.md` & Blueprint `KMP/04-achievements-screen-badge-grid-milestone-path.md`
- **4. Purpose**: Render Achievements 02 (`LOCKED` 3-column grid displaying all 7 locked badges: `7-Day Streak`, `Kindness Hero`, `Dua Master`, `Arabic Pioneer`, `Ramadan Star`, `Tajweed Learner`, `Family Champion`).
- **5. User Role**: Child Learner
- **6. Navigation**: `AchievementsRoute` (`achievements/components/BadgeGridSection.kt`) -> `BadgeDetailRoute(badgeId)` (`achievements/BadgeDetailScreen.kt`).
- **7. UI State Handling**: Managed by `AchievementsViewModel.kt` (`onScreenEnter()` via `RewardsFreshnessPolicy`).
- **8. Design System Tokens**: Strictly consumes `NoorHeroesTheme` tokens with 4-locale parity and RTL layout support.

### Screen 07: `Achievements-03.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Rewards/Achievements-03.png`
- **3. Related PRD**: `PRD_Documents/Child App (1-12)/Feature_A11_Rewards_System.md` & Blueprint `KMP/04-achievements-screen-badge-grid-milestone-path.md`
- **4. Purpose**: Render Achievements 03 (`🌱 Achievement Path` tab selected, `CURRENT LEVEL` `Learner` hero card (`1,240 XP total`, `640/600 XP in level`, `-40 XP to Scholar`), and vertical milestone path ladder: `Seedling` `0–200 XP`, `Sprout` `200–600 XP`, `Learner` `600–1,200 XP` `"YOU ARE HERE"`, `Scholar` `1,200–2,500 XP` `"NEXT"`, `Hafiz Hero` `2,500–5,000 XP`).
- **5. User Role**: Child Learner
- **6. Navigation**: `AchievementsRoute` (`achievements/components/AchievementPathSection.kt`) -> `AchievementLevelDetailRoute(levelId)` (`achievements/AchievementLevelDetailScreen.kt`).
- **7. UI State Handling**: Managed by `AchievementsViewModel.kt` (`onScreenEnter()` via `RewardsFreshnessPolicy`).
- **8. Design System Tokens**: Strictly consumes `NoorHeroesTheme` tokens with 4-locale parity and RTL layout support.

### Screen 08: `Achievements-04.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Rewards/Achievements-04.png`
- **3. Related PRD**: `PRD_Documents/Child App (1-12)/Feature_A11_Rewards_System.md` & Blueprint `KMP/04-achievements-screen-badge-grid-milestone-path.md`
- **4. Purpose**: Render Achievements 04 (Bottom scroll of `🌱 Achievement Path` showing the effort-philosophy card `"📊 XP is earned for effort — not accuracy. Every completed lesson, story, and habit counts."`).
- **5. User Role**: Child Learner
- **6. Navigation**: `AchievementsRoute` (`achievements/components/AchievementPathSection.kt`).
- **7. UI State Handling**: Managed by `AchievementsViewModel.kt` (`onScreenEnter()` via `RewardsFreshnessPolicy`).
- **8. Design System Tokens**: Strictly consumes `NoorHeroesTheme` tokens with 4-locale parity and RTL layout support.

### Screen 09: `Family Board.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Rewards/Family Board.png`
- **3. Related PRD**: `PRD_Documents/Child App (1-12)/Feature_A11_Rewards_System.md` (FR-9, FR-15, §1.18 #20–22) & Blueprint `KMP/08-family-board-experience.md`
- **4. Purpose**: Render the private, aggregate-only Family Board (`family/FamilyBoardScreen.kt`, `family/FamilyBoardComponents.kt`, `family/FamilyTreeJourneyIllustration.kt`), Family Goal Detail (`family/FamilyGoalDetailScreen.kt`), and Family Achievement Unlock Celebration modal (`family/FamilyAchievementCelebrationModal.kt`) with full visual fidelity to `Family Board.png` and zero per-sibling comparison elements.
- **5. User Role**: Child Learner / Family Group
- **6. Navigation**: `FamilyBoardRoute`, `FamilyGoalDetailRoute(goalId)`, and deep link `noorheroes://rewards/family-board` (`navigation/FamilyBoardDeepLinkHandler.kt`) wired in `RewardsNavGraph.kt`.
- **7. UI State Handling**: Managed by `FamilyBoardViewModel.kt` (`FamilyBoardUiState.kt`) supporting Loading Spinner, Populated Aggregate State (`"100 Du'as Together"` `70/100`, `847 habits this month`, `3 family members`, `12 badges earned`), `"Let's start together! 🌱"` Empty State (`totalAggregateProgress == 0`), Offline Room-Cached Display (`RewardsOfflineTopBanner` + auto-sync on reconnect), and Server-Confirmed Threshold Crossing Celebration Modal (`FamilyAchievementCelebrationModal.kt`).
- **8. Design System Tokens**: Strictly consumes `NoorHeroesTheme.colors.*`, `NoorHeroesTheme.typography.*`, `NoorHeroesTheme.spacing.*`, `NoorHeroesTheme.sizes.*`, `NoorHeroesTheme.shapes.*`, and `core-ui` primitives (`NoorCard`, `NoorDialog`, `PrimaryButton`) with 4-locale parity (`en`, `ar`, `hi`, `ur`) and full RTL support.

### Screen 10: `Rewards Wallet-01.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Rewards/Rewards Wallet-01.png`
- **3. Related PRD**: `PRD_Documents/Child App (1-12)/Feature_A11_Rewards_System.md` & Blueprint `KMP/02-rewards-wallet-hub-screen.md`
- **4. Purpose**: Render Populated Rewards Wallet Hub Top Section (`wallet/RewardsWalletHubScreen.kt`, `wallet/components/WalletBalanceHeaderCard.kt` (`5 LVL`, `1,240 XP`, `760 XP to Level 6`, `Noor Points 630`, gold `Spend` pill), `wallet/components/BadgesShelfSection.kt`, `wallet/components/WeeklyChallengeCard.kt` (`Quranic Explorer`, `4/7 days`, `3 days left`, `+100 NP on completion`), `wallet/components/DailyMissionsCard.kt` (`3 of 4 done`)).
- **5. User Role**: Child Learner
- **6. Navigation**: `RewardsWalletRoute` -> `AchievementStoreRoute`, `AchievementsRoute`, `WeeklyChallengeDetailRoute(challengeId)`.
- **7. UI State Handling**: Managed by `WalletViewModel.kt` (`onScreenEnter()` remote-first refresh via `RewardsFreshnessPolicy`).
- **8. Design System Tokens**: Strictly consumes `NoorHeroesTheme` tokens with 4-locale parity and RTL layout support.

### Screen 11: `Rewards Wallet-02.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Rewards/Rewards Wallet-02.png`
- **3. Related PRD**: `PRD_Documents/Child App (1-12)/Feature_A11_Rewards_System.md` & Blueprint `KMP/02-rewards-wallet-hub-screen.md`
- **4. Purpose**: Render Populated Rewards Wallet Hub Mid Section (`wallet/components/DailyMissionsCard.kt` + `wallet/components/RecentActivitySection.kt` with `"View all"` link).
- **5. User Role**: Child Learner
- **6. Navigation**: `RewardsWalletRoute` -> `TransactionHistoryRoute` (`wallet/TransactionHistoryScreen.kt`).
- **7. UI State Handling**: Managed by `WalletViewModel.kt` (`onScreenEnter()` via `RewardsFreshnessPolicy`).
- **8. Design System Tokens**: Strictly consumes `NoorHeroesTheme` tokens with 4-locale parity and RTL layout support.

### Screen 12: `Rewards Wallet-03.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Rewards/Rewards Wallet-03.png`
- **3. Related PRD**: `PRD_Documents/Child App (1-12)/Feature_A11_Rewards_System.md` & Blueprint `KMP/02-rewards-wallet-hub-screen.md`
- **4. Purpose**: Render Populated Rewards Wallet Hub Bottom Section (`wallet/components/RecentActivitySection.kt` displaying all 6 entries including `"Surah Sorter game"` `+85 XP`, plus 2-column `wallet/components/RewardsShortcutCards.kt` for `Achievement Store` (`630 NP available`) and `Family Board` (`Shared milestones`)).
- **5. User Role**: Child Learner
- **6. Navigation**: `RewardsWalletRoute` -> `TransactionHistoryRoute`, `AchievementStoreRoute`, `FamilyBoardRoute`.
- **7. UI State Handling**: Managed by `WalletViewModel.kt` (`onScreenEnter()` via `RewardsFreshnessPolicy`).
- **8. Design System Tokens**: Strictly consumes `NoorHeroesTheme` tokens with 4-locale parity and RTL layout support.

### Screen 13: `Rewards Wallet-04.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Rewards/Rewards Wallet-04.png`
- **3. Related PRD**: `PRD_Documents/Child App (1-12)/Feature_A11_Rewards_System.md` & Blueprint `KMP/02-rewards-wallet-hub-screen.md`
- **4. Purpose**: Render Shimmer Skeleton Loading Top Section (`wallet/components/RewardsSkeletonShimmer.kt`).
- **5. User Role**: Child Learner
- **6. Navigation**: `RewardsWalletRoute` (`state.isLoading == true`).
- **7. UI State Handling**: Shimmer skeleton matching exact card aspect ratios (`wallet/components/RewardsSkeletonShimmer.kt`).
- **8. Design System Tokens**: Strictly consumes `NoorHeroesTheme` tokens.

### Screen 14: `Rewards Wallet-05.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Rewards/Rewards Wallet-05.png`
- **3. Related PRD**: `PRD_Documents/Child App (1-12)/Feature_A11_Rewards_System.md` & Blueprint `KMP/02-rewards-wallet-hub-screen.md`
- **4. Purpose**: Render Shimmer Skeleton Loading Bottom Section (`wallet/components/RewardsSkeletonShimmer.kt` with 6 activity row placeholders and 2 bottom shortcut card placeholders).
- **5. User Role**: Child Learner
- **6. Navigation**: `RewardsWalletRoute` (`state.isLoading == true`).
- **7. UI State Handling**: Shimmer skeleton matching exact card aspect ratios (`wallet/components/RewardsSkeletonShimmer.kt`).
- **8. Design System Tokens**: Strictly consumes `NoorHeroesTheme` tokens.

### Screen 15: `Rewards Wallet-06.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Rewards/Rewards Wallet-06.png`
- **3. Related PRD**: `PRD_Documents/Child App (1-12)/Feature_A11_Rewards_System.md` & Blueprint `KMP/02-rewards-wallet-hub-screen.md`
- **4. Purpose**: Render Zero-History / New Child Empty State Top Section (`"Start learning to earn your first rewards"`, `1 LVL`, `0 XP`, `500 XP to Level 2`, `Noor Points 0`, disabled `"Earn to spend"` button in `wallet/components/WalletBalanceHeaderCard.kt`, 5 `Locked` badges with `"Complete activities to unlock badges"` in `wallet/components/BadgesShelfSection.kt`, and `"Your journey starts here"` oil-lamp card in `wallet/components/WeeklyChallengeCard.kt` (`EmptyJourneyCard`)).
- **5. User Role**: Child Learner
- **6. Navigation**: `RewardsWalletRoute` (`state.isZeroHistory == true`).
- **7. UI State Handling**: Managed by `WalletViewModel.kt`.
- **8. Design System Tokens**: Strictly consumes `NoorHeroesTheme` tokens.

### Screen 16: `Rewards Wallet-07.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Rewards/Rewards Wallet-07.png`
- **3. Related PRD**: `PRD_Documents/Child App (1-12)/Feature_A11_Rewards_System.md` & Blueprint `KMP/02-rewards-wallet-hub-screen.md`
- **4. Purpose**: Render Zero-History / New Child Empty State Bottom Section (`"★ Earn your first XP — pick an activity"` with 3 starter cards `Complete a Quran lesson +30 XP`, `Finish a knowledge quiz +20 XP`, `Log all 4 daily habits +15 XP` in `wallet/components/DailyMissionsCard.kt` (`StarterActivitiesSection`), and muted bottom shortcut cards in `wallet/components/RewardsShortcutCards.kt`).
- **5. User Role**: Child Learner
- **6. Navigation**: `RewardsWalletRoute` (`state.isZeroHistory == true`).
- **7. UI State Handling**: Managed by `WalletViewModel.kt`.
- **8. Design System Tokens**: Strictly consumes `NoorHeroesTheme` tokens.

### Screen 17: `Rewards Wallet-08.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Rewards/Rewards Wallet-08.png`
- **3. Related PRD**: `PRD_Documents/Child App (1-12)/Feature_A11_Rewards_System.md` & Blueprint `KMP/02-rewards-wallet-hub-screen.md`
- **4. Purpose**: Render Offline Cached State Top Section (`RewardsOfflineTopBanner` `"Offline — showing cached rewards"` with `"Retry"` button in `wallet/components/RewardsOfflineBanner.kt`, `"Cached"` header pill in `wallet/RewardsWalletHubScreen.kt`, `"760 XP to Level 6 · syncs when online"` + disabled `"Spend"` button in `wallet/components/WalletBalanceHeaderCard.kt`, `"Badges"` with `"cached"` indicator in `wallet/components/BadgesShelfSection.kt`, and `"Unavailable until reconnected"` warning card in `wallet/components/WeeklyChallengeCard.kt` (`OfflineNoticeCard`)).
- **5. User Role**: Child Learner
- **6. Navigation**: `RewardsWalletRoute` (`state.isOffline == true`).
- **7. UI State Handling**: Managed by `WalletViewModel.kt` + `RewardsFreshnessPolicy` Room cache fallback.
- **8. Design System Tokens**: Strictly consumes `NoorHeroesTheme` tokens.

### Screen 18: `Rewards Wallet-09.png`
- **1. Platform**: Mobile App (Compose Multiplatform / Material 3)
- **2. Exact Image Path**: `Screens/Mobile App/Rewards/Rewards Wallet-09.png`
- **3. Related PRD**: `PRD_Documents/Child App (1-12)/Feature_A11_Rewards_System.md` & Blueprint `KMP/02-rewards-wallet-hub-screen.md`
- **4. Purpose**: Render Offline Cached State Bottom Section (`wallet/components/RecentActivitySection.kt` with `"Cached"` label displaying top 3 cached items, muted bottom shortcut cards with offline icons in `wallet/components/RewardsShortcutCards.kt`, and full-width teal `"Try reconnecting"` button in `wallet/components/RewardsOfflineBanner.kt` (`RewardsOfflineBottomCta`)).
- **5. User Role**: Child Learner
- **6. Navigation**: `RewardsWalletRoute` (`state.isOffline == true`).
- **7. UI State Handling**: Managed by `WalletViewModel.kt` + `RewardsFreshnessPolicy` Room cache fallback.
- **8. Design System Tokens**: Strictly consumes `NoorHeroesTheme` tokens.

### Shared Cross-Feature Surfaces (#23–24, Blueprints K-09, K-10, K-11 & K-12): `RewardUnlockAnimation`, `BadgeUnlockModal`, `RewardsFreshnessPolicy`, `RewardAnalytics` & `RewardsLocalizationFoundation`
- **1. Platform**: Mobile App (`core:core-designsystem`, `core:rewards-client`, & `feature:feature-rewards`)
- **2. Implementation Files**:
  - `core/core-designsystem/src/commonMain/kotlin/com/noorheroes/core/designsystem/reward/RewardRevealTrigger.kt`
  - `core/core-designsystem/src/commonMain/kotlin/com/noorheroes/core/designsystem/reward/RewardUnlockAnimation.kt`
  - `core/core-designsystem/src/commonMain/kotlin/com/noorheroes/core/designsystem/reward/BadgeUnlockModal.kt`
  - `core/rewards-client/src/commonMain/kotlin/com/noorheroes/core/rewards/client/data/RewardsFreshnessPolicy.kt`
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/analytics/RewardAnalytics.kt`
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/localization/RewardsLocalizationFoundation.kt`
  - Delegating adapters in `core/core-ui/.../Rewards.kt`, `feature/feature-rewards/.../BadgeUnlockModal.kt`, and `feature/feature-rewards/.../RewardClaimConfirmation.kt`.
- **3. Related PRD**: `PRD_Documents/Child App (1-12)/Feature_A11_Rewards_System.md` (§2.1, FR-1, FR-2, FR-13, FR-17, §1.18 #23–24, §1.19) & Blueprints `KMP/09-reward-unlock-animation-badge-unlock-modal.md`, `KMP/10-rewards-data-freshness-cross-screen-invalidation-engine.md`, `KMP/11-rewards-cross-platform-analytics-instrumentation.md`, `KMP/12-rewards-localization-rtl-foundation.md`
- **4. Purpose**: Provide the single canonical, cross-feature `<= 2s` deterministic `RewardUnlockAnimation(xp, noorPoints, activityType, onDismiss)` and `BadgeUnlockModal(badge, onDismiss)`, the remote-first `RewardsFreshnessPolicy` ensuring all 12 Rewards screens/sub-screens always reflect fresh server state upon `onScreenEnter()`, the server-confirmation-gated zero-PII `RewardAnalytics` event emitter covering all 27 PRD §1.19 events across all 7 ViewModels, and the `RewardsLocalizationFoundation` 4-locale (`EN`/`HI`/`AR`/`UR`) & RTL foundation.

---

## 6. Verification & Sign-Off Summary (2026-09-26)
- **All 18 Design Screens (`Screens/Mobile App/Rewards`)**: Verified 100% visual, structural, data-model, 4-locale (`EN`/`HI`/`AR`/`UR`), and RTL parity across `:feature:feature-rewards` and `:core:core-designsystem`.
- **All 12 KMP Blueprints (`K-01` .. `K-12`)**: 100% implemented, wired, and verified across `:core:rewards-client`, `:core:core-designsystem`, `:core:core-ui`, `:core:core-common`, and `:feature:feature-rewards`.
- **Localization & RTL Completeness (`K-12`)**: `330` keys across `values`, `values-hi`, `values-ar`, and `values-ur` (`0` missing, `0` extra, `0` blank), `MinorUnitsFormatter` (`core-common/format`) + `TransactionLabelMapper` (`K-03`) numeral/locale integration, and `0` hardcoded `Text(...)` English strings verified by AST guard.
- **Rule & Token Audit (`NoorHeroes/docs/rule.md`)**: `0 violations` across 150 git-status files (`recheck_zero_gaps.py`).
- **Gradle Host Unit & Integration Tests**: `:core:rewards-client:testAndroidHostTest`, `:core:core-designsystem:testAndroidHostTest`, and `:feature:feature-rewards:testAndroidHostTest` (`147/147` tests passing) — `BUILD SUCCESSFUL`.




