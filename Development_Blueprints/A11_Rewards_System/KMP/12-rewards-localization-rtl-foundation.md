# K-12 — Rewards Localization & RTL Foundation

## 1. Feature Context
Part of Feature A.11 — Rewards System. Externalizes every child-facing string across the Rewards feature to the platform's localization resource system and verifies RTL correctness across all screens.

## 2. Parent Feature
A.11 Rewards System — KMP App (Android/iOS)

## 3. Sub-feature
K-12 Rewards Localization & RTL Foundation

## 4. Objective
Ensure all reward-reason labels, badge/achievement names, mission/challenge copy, and store item descriptions are fully externalized (EN/HI/AR/UR) with correct RTL mirroring across K-02 through K-09.

## 5. Business Requirements
- No hardcoded child-facing strings anywhere in the Rewards feature.
- RTL mirroring across Wallet, Achievements, Achievement Store, Family Board, and Challenge screens.
- Correct number/currency-style formatting for XP and Noor Heroes Points per locale.
- Pluralization rules correctly applied for transaction/badge counts.

## 6. Existing Architecture
Reuses the platform's existing localization/resource-string architecture (per `CORE_DATASTORE_INSTRUCTIONS.md`/`CORE_COMMON_INSTRUCTIONS.md`'s localization conventions) and `core-common/format` for number/date formatting — no new localization pipeline introduced.

## 7. Existing Code to Reuse
- Existing string-resource system and translation-key conventions.
- `core-common/format` number formatting utilities (reused by K-03's `TransactionLabelMapper`).

## 8. Files to Create
- Localization resource entries (EN/HI/AR/UR) for every user-facing string introduced across K-02–K-09 (organized per the project's existing resource-file convention, e.g. per-module string resource files).
- `feature-rewards/src/commonTest/kotlin/.../localization/RewardsLocalizationCompletenessTest.kt` — asserts every string key used across the feature has a translation in all four locales.

## 9. Files to Modify
- K-02 through K-09's Composables — replace any inline/hardcoded strings identified during implementation with resource-key references.

## 10. Backend Requirements
None new; consumes `locale_key`/`reason_type` fields already returned by B-02/B-04/B-05/B-06/B-07.

## 11. KMP Requirements
- `RewardsLocalizationCompletenessTest` scans every string-resource key referenced within the Rewards feature module and asserts a translation exists for all four supported locales — a structural completeness guard, not just a manual QA pass.
- Text-expansion tolerance verified in card/tile layouts (German/Arabic-length-variance-style testing pattern applied to Arabic/Urdu specifically) — no truncated or overlapping text in badge tiles, mission cards, or price tags.
- Arabic-Indic numeral handling for XP/points display, per-locale, where the platform's existing number-formatting convention specifies it.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
N/A (consumes existing localization-key-bearing fields from already-specified endpoints).

## 14. Database Requirements (Local)
N/A.

## 15. Validation
`RewardsLocalizationCompletenessTest` passes with zero missing translations across EN/HI/AR/UR (mandatory).

## 16. Authentication
N/A.

## 17. Authorization
N/A.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Missing translation key at runtime (should be prevented by the completeness test, but as a defensive fallback) | Falls back to the English string rather than rendering a raw key or blank text |

## 19. Offline First
N/A (localization resources are bundled, not fetched).

## 20. Local Data
N/A.

## 21. Localization
This entire sub-feature *is* the localization work: full EN/HI/AR/UR coverage across every Rewards screen (K-02–K-09).

## 22. RTL
Full RTL verification pass across Wallet, Transaction History, Achievements, Achievement Store, Family Board, and Challenge screens — snapshot/UI tests per screen for the Arabic and Urdu locales.

## 23. Analytics
N/A.

## 24. Performance
N/A beyond standard resource-loading conventions.

## 25. Security
N/A.

## 26. Library Requirements
Existing platform localization/resource system, `core-common/format`.

## 27. Testing
- Unit: localization-completeness test (mandatory).
- Snapshot/UI: RTL rendering across all six listed screens, for both Arabic and Urdu.
- Text-expansion tolerance test on card/tile layouts.

## 28. Documentation
Document the string-resource key naming convention used across the Rewards feature, so future badge/mission/catalog additions (admin-authored content, per B-04/B-05/B-06/B-10/B-11/B-12) follow a consistent key-naming pattern the client can resolve reliably.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Audit K-02–K-09 for Hardcoded Strings**
- Objective: identify every user-facing string across the feature not yet resource-key-backed.
- Files to Modify: K-02 through K-09's Composables, as needed.
- Definition of Done: zero hardcoded strings remain.

**Task 02 — Populate EN/HI/AR/UR Resource Entries**
- Files to Create: resource files per §8.
- Definition of Done: every identified key has all four locale entries.

**Task 03 — Implement Localization Completeness Test (Mandatory)**
- Files to Create: `RewardsLocalizationCompletenessTest.kt`
- Definition of Done: test passes, wired as a CI gate for this feature module.

**Task 04 — Verify RTL Rendering Across All Screens**
- Tests: RTL snapshot tests per screen (Wallet, History, Achievements, Store, Family Board, Challenges).
- Definition of Done: all six screens verified correct in Arabic and Urdu.

**Task 05 — Verify Text-Expansion Tolerance**
- Tests: card/tile layout expansion test.
- Definition of Done: no truncation/overlap in badge tiles, mission cards, price tags.

**Task 06 — Documentation & Final Review**
- Documentation: key-naming convention doc per §28.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Every Rewards-feature string fully localized across EN/HI/AR/UR, RTL-correct across all screens, completeness-guarded by an automated test.

## 31. Final Verification Checklist
- [x] Zero hardcoded user-facing strings remain in the Rewards feature
- [x] Localization completeness test passes (all four locales, all keys)
- [x] RTL verified across Wallet, History, Achievements, Store, Family Board, Challenges
- [x] Text-expansion tolerance verified (no truncation/overlap)
- [x] Arabic-Indic numeral handling verified where applicable
- [x] Key-naming convention documented for future admin-authored content

---

## 32. String-Resource Key Naming Convention & Verification Sign-Off Ledger (2026-09-26)

### A. Admin-Authored & Bundled Key Naming Convention (`RewardsKeyNamingConvention` — §28)
| Content Surface (Backend Source) | Key Pattern | Helper Method | Example Key |
| :--- | :--- | :--- | :--- |
| **Badge Title** (`B-04` / `B-10`) | `rewards_badge_<slug>` | `RewardsKeyNamingConvention.badgeTitleKey(slug)` | `rewards_badge_quran_star` |
| **Badge Description** (`B-04` / `B-10`) | `rewards_badge_<slug>_desc` | `RewardsKeyNamingConvention.badgeDescriptionKey(slug)` | `rewards_badge_quran_star_desc` |
| **Daily Mission Title** (`B-05` / `B-12`) | `rewards_mission_<slug>` | `RewardsKeyNamingConvention.missionTitleKey(slug)` | `rewards_mission_quran_lesson` |
| **Weekly / Seasonal Challenge** (`B-05` / `B-12`) | `rewards_challenge_<slug>_title` | `RewardsKeyNamingConvention.challengeTitleKey(slug)` | `rewards_challenge_ramadan_week_1_title` |
| **Store Item Title** (`B-06` / `B-11`) | `rewards_store_item_<slug>_title` | `RewardsKeyNamingConvention.storeItemTitleKey(slug)` | `rewards_store_item_golden_lantern_avatar_title` |
| **Store Item Description** (`B-06` / `B-11`) | `rewards_store_item_<slug>_desc` | `RewardsKeyNamingConvention.storeItemDescriptionKey(slug)` | `rewards_store_item_golden_lantern_avatar_desc` |
| **Ledger Reason Label** (`B-02`) | `rewards_reason_<reason_type>` | `RewardsKeyNamingConvention.ledgerReasonKey(type)` | `rewards_reason_surah_completed` |
| **Accessibility Description** (`K-02`–`K-09`) | `cd_<surface>_<element>` | `RewardsKeyNamingConvention.contentDescriptionKey(s, e)` | `cd_store_item_card` |

### B. Implementation & Test Files
- `core/core-common/src/commonMain/composeResources/values/strings_rewards.xml` (330 keys)
- `core/core-common/src/commonMain/composeResources/values-hi/strings_rewards.xml` (330 keys)
- `core/core-common/src/commonMain/composeResources/values-ar/strings_rewards.xml` (330 keys)
- `core/core-common/src/commonMain/composeResources/values-ur/strings_rewards.xml` (330 keys)
- `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/localization/RewardsLocalizationFoundation.kt` (integrates `MinorUnitsFormatter.formatPoints` from `core-common/format` & `LocalizationFormatter`)
- `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/wallet/TransactionLabelMapper.kt` (reuses `RewardsLocalizationFoundation` numeral and locale resolution per `K-12 §7`)
- `feature/feature-rewards/src/commonTest/kotlin/com/noorheroes/feature/rewards/localization/RewardsLocalizationCompletenessTest.kt` (8 unit & integration tests)
- `feature/feature-rewards/src/androidHostTest/kotlin/com/noorheroes/feature/rewards/localization/RewardsResourceXmlFilesystemCompletenessTest.kt` (3 structural XML & source-code AST tests)
- Updated `DailyMissionsCard.kt`, `RecentActivitySection.kt`, `TransactionDetailCard.kt`, `TransactionHistoryScreen.kt`, `DailyMissionListSection.kt`, `SeasonalEventScreen.kt`, `WeeklyChallengeCard.kt`, `WeeklyChallengeDetailScreen.kt`, `BadgeUnlockModal.kt` (`K-09`), and `RewardUnlockAnimation.kt` (`K-09`) to replace all remaining inline formatted strings with `Res.string.*` resource keys.
- **Automated Verification**:
  - `python recheck_zero_gaps.py`: **`0 violations` across 150 git-status files** (`NoorHeroes/docs/rule.md`).
  - `./gradlew :feature:feature-rewards:testAndroidHostTest`: **`147 / 147` tests passing (`BUILD SUCCESSFUL`)**.
  - `./gradlew :core:core-designsystem:testAndroidHostTest`: **`BUILD SUCCESSFUL`**.


