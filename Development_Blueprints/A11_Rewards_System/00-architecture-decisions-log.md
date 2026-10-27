# Feature A.11 — Architecture Decisions Log

This log records all architectural decisions across Backend (`B-01`..`B-14`), KMP Mobile (`K-01`..`K-12`), and Next.js Admin (`N-01`..`N-06`) for **Feature A.11 — Gamified Rewards System**, aligned with `FAST-API-INSTRUCTIONS.md`, `NEXT-JS-INSTRUCTIONS.md`, `NoorHeroes/docs/rule.md`, and the KMP Core instruction files.

---

### 1. B-01 / K-01 — Dual-Currency Separation: XP vs. Noor Heroes Points (PRD §2.1)
**Finding:** Children and parents must never confuse cumulative effort progression (**XP**, which unlocks Hero Levels and never decreases) with spendable store currency (**Noor Heroes Points / NP**, which increments on activity completion and decrements on Cosmetic Store redemption).
**Decision:** Maintain two independent ledger columns (`total_xp` and `noor_points_balance`) in `ChildRewardWallet` (`core-database` `RewardWalletCacheEntity`) and visually distinguish XP (`📈` effort/level progress-bar metaphor) from Noor Heroes Points (`🪙` spendable coin/currency metaphor) across all wallet, store, and `RewardUnlockAnimation` surfaces.
**Files updated:** `KMP/01-shared-rewards-client-module.md`, `KMP/02-rewards-wallet-hub-screen.md`, `KMP/09-reward-unlock-animation-badge-unlock-modal.md`.

### 2. B-06 / K-07 — Zero Real-Money / IAP Affordances in Achievement Store (FR-14)
**Finding:** Ethical and COPPA/child-safety rules prohibit any real-money purchase, top-up, or payment-sheet entry point inside the Child App's Achievement Store.
**Decision:** When a child selects a cosmetic item whose NP cost exceeds `wallet.noorPointsBalance`, navigate to `InsufficientPointsShortfallScreen` displaying the exact point shortfall (`cost - balance`) and constructive `"Earn More Points"` shortcuts (`Daily Missions`, `Stories`, `Daily Quiz`) with zero payment or IAP affordances (`NoPaymentAffordanceUiTest`).
**Files updated:** `KMP/07-achievement-store-catalog-purchase-flow.md`.

### 3. B-07 / K-08 — Aggregate-Only Family Board & Anti-Sibling-Comparison Rule (FR-9, FR-15)
**Finding:** Sibling leaderboards or individual contribution breakdowns create unhealthy rivalry.
**Decision:** `GET /v1/family/{family_id}/board` and `FamilyBoardUiState` expose strictly family-wide aggregate metrics (`70/100` Du'as together, `847` habits this month, `3` family members, `12` badges earned) and cooperative Noor Tree growth milestones (`FamilyBoardNoComparisonUiTest`).
**Files updated:** `Backend/07-family-board-aggregation-api.md`, `KMP/08-family-board-experience.md`.

### 4. K-09 — Shared Cross-Feature `RewardUnlockAnimation` & `BadgeUnlockModal` in `core-designsystem` (FR-1, FR-2, FR-17)
**Finding:** Every completion flow across the Child App (A.3 K-06 Story Completion, A.4 Habits, A.7 Quizzes, A.9 Quests, A.10 Mini-Games, A.11 Missions/Challenges/Achievements) needs a celebratory reward reveal and badge unlock modal without duplicating UI code or introducing variable-reward ("slot machine") dark patterns.
**Decision:**
1. Place canonical `RewardUnlockAnimation`, `BadgeUnlockModal`, and `RewardRevealTrigger` (`DeterministicRewardVariantResolver`, `RewardActivityType`, `RewardAnimationVariant`, `BadgeUnlockUiModel`, `BadgeUiModel`) in `core:core-designsystem` (`com.noorheroes.core.designsystem.reward`) and export `NoorHeroesTheme.rewards`.
2. Enforce `MAX_REWARD_DURATION_MS = 2000L` (`<= 2s`), `0ms` static reduced-motion rendering (`LocalAdaptiveContext.current.accessibility.reduceMotion`), `0ms` non-blocking tap-through dismissal (`onDismiss`), and deterministic `activityType` lookup (`DeterministicRevealTest`, `RewardAnimationPerformanceTest`).
3. Delegate `core:core-ui` (`Rewards.kt`) and `feature:feature-rewards` (`BadgeUnlockModal.kt` and `RewardClaimConfirmation.kt`) directly to `core-designsystem`'s canonical implementation, and wire A.3 K-06 (`06-story-completion-reward-moral-summary-flow.md`) to consume `RewardUnlockAnimation(xp, noorPoints, activityType = "story_complete")` and `BadgeUnlockModal(badge, onDismiss)` with caller-controlled dismiss destinations.
**Files updated:** `KMP/09-reward-unlock-animation-badge-unlock-modal.md`, `A3_Stories_Module/KMP/06-story-completion-reward-moral-summary-flow.md`.

### 5. K-05 (Sharing) — PII-Free Shareable Achievement Card (FR-16)
**Finding:** Externally shared achievement cards must never leak child PII (full name, photo, email, age, location, or raw user ID).
**Decision:** Render shareable achievement cards exclusively from an allowlisted `ShareCardUiModel` containing only badge/milestone artwork, generic celebratory title, and NoorHeroes branding (`ShareCardPiiExclusionUiTest`).
**Files updated:** `KMP/05-parent-gated-achievement-sharing-flow.md`.

### 6. K-10 (Freshness) — Rewards Data Freshness & Cross-Screen Invalidation Engine (FR-13, K-01 §6)
**Finding:** Because reward issuance is strictly backend-orchestrated per learning feature (`POST /v1/content/{id}/complete` in Stories, `POST /v1/habits/{id}/checkin` in Habits, `POST /v1/quizzes/{id}/submit` in Quizzes) with no client-side `reportCompletion()` write path or shared client-side reward-event bus (per K-01 §6), a child earning points in Habits or Stories and immediately opening the Rewards tab would see a stale pre-award snapshot under a cache-first strategy.
**Decision:**
1. Implement `RewardsFreshnessPolicy` (`core:rewards-client`) enforcing an **always remote-first, Room-cache-as-instant-paint / offline-fallback** read policy across all five K-01 repositories (`WalletRepository`, `MissionsRepository`, `AchievementsRepository`, `AchievementStoreRepository`, `FamilyBoardRepository`).
2. Coalesce concurrent in-flight requests (`CompletableDeferred`) and debounce rapid repeated `refreshOnEnter()` triggers within `DEFAULT_DEBOUNCE_WINDOW_MS = 500L` to avoid redundant network load during rapid tab-switching while preserving `0ms` perceived initial paint from the Room cache.
3. Immediately invalidate all debounce timestamps for a child or family scope (`invalidateScope`, `invalidateAllChildScopes(childId)`, `invalidateAllFamilyScopes()`) whenever a reward claim (`claimMission`), store purchase (`purchaseStoreItem`), family goal contribution (`recordFamilyGoalContribution`), or optimistic wallet delta (`applyOptimisticPointsDelta`) occurs.
4. Wire `onScreenEnter()` on composition across all 12 screens and sub-screens in `:feature:feature-rewards` (`RewardsWalletHubScreen`, `TransactionHistoryScreen`, `TransactionDetailScreen`, `AchievementsScreen`, `BadgeDetailScreen`, `AchievementLevelDetailScreen`, `WeeklyChallengeDetailScreen`, `ArchivedChallengeScreen`, `SeasonalEventScreen`, `AchievementStoreScreen`, `StoreItemDetailScreen`, and `FamilyBoardScreen`), verified by `RewardsFreshnessPolicyTest` and `CrossScreenFreshnessInvalidationTest` (§15 cross-screen staleness scenario).
**Files updated:** `KMP/10-rewards-data-freshness-cross-screen-invalidation-engine.md`, `00-screen-to-code-visual-blueprint.md`.

### 7. K-11 — Server-Confirmation-Gated & Zero-PII Cross-Platform Analytics Instrumentation (PRD §1.19, §6.6)
**Finding:** Optimistic UI updates or offline Room-cached renders must never emit reward telemetry events, as that would inflate analytics counts on network failure or rollback; furthermore, COPPA/GDPR-K rules strictly forbid child/family PII in analytics payloads.
**Decision:**
1. Centralize all 27 PRD §1.19 events (`ALL_PRD_1_19_EVENTS`) in `RewardAnalytics` (`feature/feature-rewards/.../analytics/RewardAnalytics.kt`).
2. Gate every single emitter on `isServerConfirmed == true` (`emitIfServerConfirmed`) so optimistic UI deltas and offline Room cache reads (`isOffline == true`) never emit telemetry.
3. Enforce automated PII scrubbing (`sanitizeNoPii`) stripping `child_id`, `family_id`, `parent_id`, `user_id`, `nickname`, `child_name`, `email`, `phone`, `dob`, `ip_address`, and `device_id` before delegating to `AnalyticsTracker`.
**Files updated:** `KMP/11-rewards-cross-platform-analytics-instrumentation.md`, `feature/feature-rewards/FEATURE_REWARDS_INSTRUCTIONS.md`.

### 8. K-12 — 4-Locale (`EN`/`HI`/`AR`/`UR`) Localization, Arabic-Indic Numerals & RTL Foundation (PRD §1.18–1.20)
**Finding:** All 18 Rewards screens and celebration modals must support English (`en`), Hindi (`hi`), Arabic (`ar`), and Urdu (`ur`) with zero hardcoded strings, proper RTL mirroring (`LayoutDirection.Rtl`), locale-aware numerals (`٠-٩` / `۰-۹`), `+35%` text-expansion resilience, and deterministic key generation for admin-authored badges, missions, challenges, and store items (`B-02`, `B-04`, `B-05`, `B-06`).
**Decision:**
1. Maintain `330` synchronized string resources across `values`, `values-hi`, `values-ar`, and `values-ur` in `core/core-common/src/commonMain/composeResources/values*/strings_rewards.xml`.
2. Implement `RewardsLocalizationFoundation` and `RewardsKeyNamingConvention` in `:feature:feature-rewards`, integrating `MinorUnitsFormatter.formatPoints` (`core-common/format`) and `TransactionLabelMapper` (`K-03`), with defensive runtime English fallback (`resolveTranslationOrEnglishFallback`).
3. Enforce zero missing translations and zero hardcoded `Text(...)` English strings via `RewardsLocalizationCompletenessTest` (`commonTest`) and `RewardsResourceXmlFilesystemCompletenessTest` (`androidHostTest`) (`147/147` tests passing).
**Files updated:** `KMP/12-rewards-localization-rtl-foundation.md`, `00-screen-to-code-visual-blueprint.md`, `feature/feature-rewards/FEATURE_REWARDS_INSTRUCTIONS.md`.



