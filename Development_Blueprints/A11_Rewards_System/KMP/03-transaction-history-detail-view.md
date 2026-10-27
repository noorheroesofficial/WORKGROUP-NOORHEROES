# K-03 — Transaction History & Detail View

## 1. Feature Context
Part of Feature A.11 — Rewards System. Paginated transaction history and single-entry detail view, reached from the Wallet Hub's balance/history component.

## 2. Parent Feature
A.11 Rewards System — KMP App (Android/iOS)

## 3. Sub-feature
K-03 Transaction History & Detail View

## 4. Objective
Build the Transaction History list and Transaction Detail screens (§1.18 #2–3), with deterministic, localized reason-label rendering.

## 5. Business Requirements
- Reason labels are human-readable and deterministic (e.g., "Completed Surah Al-Fatiha lesson +30 XP"), sourced from `reason_type`/`reason_id` mapped through a label-template registry.
- Full detail readable via screen reader.
- Offline browsing of previously synced history.

## 6. Existing Architecture
`feature-rewards` module (established in K-02). Reuses K-01's `WalletRepository` paginated `recent_ledger` reads.

## 7. Existing Code to Reuse
- K-01's `WalletRepository`.
- `core-common/format` number/date formatting utilities.
- `core-navigation` `Navigator`/`Route`.

## 8. Files to Create
- `feature-rewards/src/commonMain/kotlin/.../wallet/TransactionHistoryScreen.kt`
- `feature-rewards/src/commonMain/kotlin/.../wallet/TransactionDetailScreen.kt`
- `feature-rewards/src/commonMain/kotlin/.../wallet/TransactionLabelMapper.kt` (`reason_type`/`reason_id` → localized label)
- `feature-rewards/src/commonTest/kotlin/.../wallet/TransactionLabelMapperTest.kt`

## 9. Files to Modify
- `core-navigation` `Route` registry — add Transaction Detail route (per-entry).

## 10. Backend Requirements
Consumes B-02's paginated `recent_ledger` and Transaction Detail endpoint.

## 11. KMP Requirements
- `TransactionLabelMapper` maps `reason_type`/`reason_id` to a localized template string with interpolated XP/points values — a pure, unit-testable function, not embedded string concatenation in the Composable.
- Lazy-paginated list (no full-list recomposition per page load).

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
`GET /v1/children/{id}/wallet` (paginated `recent_ledger`), `GET /v1/children/{id}/wallet/transactions/{entry_id}` (B-02).

## 14. Database Requirements (Local)
Reuses K-01's `wallet_cache`-adjacent local history cache for offline browsing of previously fetched pages.

## 15. Validation
Unit test for reason-label formatting correctness across EN/HI/AR/UR locales, including correct number formatting (Arabic-Indic numeral handling where applicable per locale).

## 16. Authentication
Reuses shared `core-network` Bearer token attachment.

## 17. Authorization
N/A at UI layer.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| History fetch failure | Cached previously-fetched pages remain browsable; new-page fetch shows a retry affordance |
| Unknown `entry_id` (deep link to a stale/deleted-in-UI-only entry) | Friendly "transaction not found" state, not a crash |

## 19. Offline First
Previously synced pages remain browsable offline; new pagination requires connectivity.

## 20. Local Data
Cached history pages mirror the last-fetched server responses for offline re-browsing.

## 21. Localization
`TransactionLabelMapper` templates externalized per locale (EN/HI/AR/UR); no hardcoded reason text.

## 22. RTL
List item layout (icon + label + amount) mirrors correctly for Arabic/Urdu.

## 23. Analytics
No dedicated event beyond `wallet_viewed` (K-02); detail-view opens are considered part of the wallet-browsing funnel, not separately tracked unless a future requirement specifies otherwise.

## 24. Performance
Lazy-loaded, paginated list; large-history performance verified via a synthetic large-fixture test.

## 25. Security
No new sensitive data handling.

## 26. Library Requirements
Compose Multiplatform, Koin, kotlinx-datetime (date formatting), kotlinx-coroutines.

## 27. Testing
- Unit: `TransactionLabelMapper` formatting across all four locales (mandatory).
- UI: pagination scroll behavior, detail-view rendering.
- Accessibility: full detail screen-reader readability test.

## 28. Documentation
KDoc on `TransactionLabelMapper` documenting the template registry and how new `reason_type` values should be added by future feature authors.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement `TransactionLabelMapper`**
- Files to Create: `TransactionLabelMapper.kt`
- Implementation Details: `reason_type`/`reason_id` → localized template with interpolated values.
- Tests: multi-locale formatting test (mandatory).
- Definition of Done: correct labels across all four locales.

**Task 02 — Build `TransactionHistoryScreen`**
- Files to Create: `TransactionHistoryScreen.kt`
- Implementation Details: lazy-paginated list, offline-cached-page browsing.
- Localization/RTL: per §21/§22.
- Tests: pagination UI test.
- Definition of Done: correct rendering, no full-list recomposition on page load.

**Task 03 — Build `TransactionDetailScreen`**
- Files to Create: `TransactionDetailScreen.kt`
- Error Handling: unknown-entry friendly state.
- Tests: accessibility readability test.
- Definition of Done: full detail correctly rendered and accessible.

**Task 04 — Wire Navigation**
- Files to Modify: `core-navigation` `Route` registry.
- Definition of Done: Detail screen reachable per-entry from History.

**Task 05 — Documentation & Final Review**
- Documentation: KDoc per §28.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Transaction History and Detail screens live, deterministic localized labeling, offline-browsable, fully accessible.

## 31. Final Verification Checklist
- [x] `TransactionLabelMapper` correct across EN/HI/AR/UR
- [x] Pagination performant on large histories, no full-list recomposition
- [x] Offline browsing of previously synced pages verified
- [x] Detail screen fully screen-reader accessible
- [x] RTL layout verified
- [x] Unknown-entry state handled gracefully

## 32. Implementation Summary & Verification Evidence
- **Feature Code Created (`:feature:feature-rewards`)**:
  - `wallet/TransactionLabelMapper.kt`: Deterministic multi-locale mapper translating raw `reason_type` and `reason_id` with interpolated XP/NP amounts, Arabic-Indic/Urdu numeral formatting, and screen reader semantic descriptions across all 4 locales (EN, AR, HI, UR).
  - `wallet/TransactionUiState.kt`: Immutable MVI state models (`TransactionHistoryUiState`, `TransactionDetailUiState`, `TransactionFilter`, `TransactionCategory`, `TransactionHistoryItem`, `TransactionEvent`, `TransactionEffect`).
  - `wallet/TransactionViewModel.kt`: In-memory category filtering (`ALL`, `EARNED`, `SPENT`), fast in-memory detail resolution, remote fallback, and offline banner retry handling (`OnRetry`).
  - `wallet/components/TransactionItemRow.kt`: Category avatar badge with design-accurate emojis (`📖`, `🕌`, `⚡`, `✅`, `⭐`, `🎮`, `🛍️`, etc.), body/date text, XP/NP reward amount pill with color distinction (`primary` for XP, `accent` for NP, `error` for spent).
  - `wallet/components/TransactionDetailCard.kt`: `TransactionHeroCard`, `TransactionBreakdownCard` (with localized numerals), and `TransactionNotFoundCard` (graceful 404 state).
  - `wallet/TransactionHistoryScreen.kt`: Header navigation with AutoMirrored arrow back, balance overview bar, filter chips row, offline banner, shimmer loading, empty state, and 60fps lazy column.
  - `wallet/TransactionDetailScreen.kt`: Top bar with AutoMirrored arrow back, hero card, breakdown card, and not-found card.
- **Navigation & DI Integration**:
  - `core/core-navigation/.../Route.kt`: Added `TransactionDetailRoute(val entryId: String)` under `TransactionHistoryRoute`.
  - `shared/.../AppRoot.kt` & `shared/.../DummyUI.kt`: Hooked up `TransactionHistoryRoute` and `TransactionDetailRoute`.
  - `feature/feature-rewards/.../RewardsModule.kt`: Registered `viewModelOf(::TransactionViewModel)` into `rewardsModule`.
- **4-Locale Localization Resources (`:core:core-common`)**:
  - Added 32 localized transaction keys to `strings_rewards.xml` across all 4 locales (EN, AR, HI, UR) with 100% key parity.
- **Automated Test Coverage**:
  - `TransactionLabelMapperTest.kt` (8 tests): All reason types, numeral conversions, multi-locale translations, fallback.
  - `TransactionScreensTest.kt` (9 tests): Screen state contracts, accessibility descriptions, 1,000-item synthetic performance test (<100ms), Arabic/Urdu breakdown numerals, points-only XP/NP visual distinction, RTL auto-mirroring, not-found states.
  - `TransactionViewModelTest.kt` (12 tests): Load, pagination, in-memory filters, retry recovery, fast detail cache, remote detail, 404 handling, effect emissions.
  - Total `:feature:feature-rewards` test suite: 43/43 tests passing (100% pass rate).
- **Design System Compliance (`rule.md`)**:
  - 0 raw `.dp`, 0 raw `.sp`, 0 raw `Color(0x...)`, 0 raw Material3 components.
  - All files strictly `< 500 lines`.
  - Author `@author Sarvare Alam` on all created files.

## 33. UI Design Parity Verification Matrix (Screens 01–09 & Detail Views)

| Design Screen | UI Component / Scenario | Verification Evidence & Fidelity Match | Compliance Status |
|---|---|---|---|
| `Rewards Wallet-01.png` | Default Hub Header & Balance Card | Circular LVL indicator, level progress bar, "760 XP to Level 6", Noor Points sub-card with gold sparkle and amber "Spend" button. | 100% Match |
| `Rewards Wallet-01.png` | Badges Preview Shelf & Weekly Challenge | Horizontal rail with "See all" and 5 styled badges; "Quranic Explorer" 4/7 days challenge card with teal progress bar and "+100 NP on completion". | 100% Match |
| `Rewards Wallet-02.png` | Daily Missions Progress & Strikethrough | "3 of 4 done" header ratio; completed missions feature line-through text and muted `textSecondary` XP text; active mission shows vibrant teal XP. | 100% Match |
| `Rewards Wallet-02.png` | Recent Activity List (Top Items) | "Recent Activity" with "View all" action; 6 design-accurate entries (Quran +30 XP, Streak +50 NP, Ibrahim +25 XP, Quiz +20 XP, Habits +40 NP, Sorter +85 XP) with category-colored avatar backgrounds. | 100% Match |
| `Rewards Wallet-03.png` | Shortcut Cards & Bottom Navigation | Side-by-side equal-width cards for "Achievement Store" (630 NP available) and "Family Board" (Shared milestones) using theme tokens. | 100% Match |
| `Rewards Wallet-04.png` | Shimmer Skeleton (Top Surface) | `RewardsSkeletonShimmer`: animated alpha shimmering balance card, badges rail placeholders, and challenge card placeholders. | 100% Match |
| `Rewards Wallet-05.png` | Shimmer Skeleton (Bottom Surface) | Shimmer cards for daily missions, recent activity items, and shortcut cards. | 100% Match |
| `Rewards Wallet-06.png` | Zero-History Empty State (Top) | Level 1 (0 XP, "500 XP to Level 2"), disabled "Earn to spend" button; 5 locked badges with "Locked" label; Diya/lamp illustration in "Your journey starts here" hero card. | 100% Match |
| `Rewards Wallet-07.png` | Zero-History Starter Activities & Locked Shortcuts | "⭐ Earn your first XP — pick an activity" with 3 starter activity cards (Quran +30 XP, Quiz +20 XP, Habits +15 XP); disabled "Earn NP to unlock" store shortcut. | 100% Match |
| `Rewards Wallet-08.png` | Offline Cached State (Top) | Soft `errorContainer` top offline banner with red icon and solid red "Retry" button; red "Cached" pill badge on header; red " · syncs when online"; orange/peach "Unavailable until reconnected" card. | 100% Match |
| `Rewards Wallet-09.png` | Offline Cached State (Bottom) | "Recent Activity" shows "Cached" label; shortcut cards show disabled slashed wifi `📶🚫`; full-width Teal PrimaryButton "Try reconnecting". | 100% Match |
| `Screen 2 (History)` | `TransactionHistoryScreen` | Filter chips (`All`, `Earned`, `Spent`), balance summary bar (`⭐ XP` / `🪙 NP`), offline top banner retry, empty state, and 60fps lazy column. | 100% Match |
| `Screen 3 (Detail)` | `TransactionDetailScreen` | Auto-mirrored back button, `TransactionHeroCard` with XP/NP visual token distinction, `TransactionBreakdownCard` with localized Arabic/Urdu numerals, and friendly `TransactionNotFoundCard` 404 state. | 100% Match |
| Direct Detail Routing | Hub Recent Activity → Detail View | Tapping any recent activity item row in the Wallet Hub directly navigates to `TransactionDetailRoute(entryId)` with fallback to `TransactionHistoryRoute`. | 100% Match |

