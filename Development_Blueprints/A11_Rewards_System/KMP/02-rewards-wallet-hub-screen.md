# K-02 — Rewards Wallet Hub Screen

## 1. Feature Context
Part of Feature A.11 — Rewards System. The Rewards bottom-nav tab's landing screen — a card-based dashboard consistent with A.2 Home and A.7 Habit Builder's established visual pattern.

## 2. Parent Feature
A.11 Rewards System — KMP App (Android/iOS)

## 3. Sub-feature
K-02 Rewards Wallet Hub Screen

## 4. Objective
Build the Rewards Wallet landing screen (§1.18 #1) with `WalletViewModel` exposing `StateFlow<WalletUiState>`, optimistic-then-reconciled balance display, backing FR-13.

## 5. Business Requirements
- XP progress bar, Noor Heroes Points coin balance, recent-transaction list, badge shelf preview rail, weekly challenge card, daily mission list, entry points to Achievement Store and Family Board — all on one dashboard.
- New-child empty state: "Start learning to earn your first XP!" framing, not a stark "0".
- Offline: cached balance with an explicit "offline, may be outdated" indicator.
- Every transaction reason text fully screen-reader-readable.

## 6. Existing Architecture
`feature-rewards`/`feature-rewards-domain` module pair, following the `feature-habits`/`feature-habits-domain` naming convention (A7 K-01). Koin DI, Compose Multiplatform, `core-navigation` `Navigator`, `core-analytics` `AnalyticsTracker`.

## 7. Existing Code to Reuse
- `:core:rewards-client`'s `WalletRepository` (K-01).
- `core-design-system` XP-progress-bar and coin-balance tokens (introduced here, then reused by K-03/K-04/K-07 per §2.1's "reusable themed components" requirement).
- `core-navigation` `Navigator`/`Route`.
- `core-analytics` `AnalyticsTracker`.

## 8. Files to Create
- `feature-rewards/src/commonMain/kotlin/.../wallet/RewardsWalletHubScreen.kt`
- `feature-rewards/src/commonMain/kotlin/.../wallet/WalletViewModel.kt`
- `feature-rewards/src/commonMain/kotlin/.../wallet/WalletUiState.kt`
- `feature-rewards-domain/src/commonMain/kotlin/.../GetWalletUseCase.kt`
- `feature-rewards/src/commonTest/kotlin/.../wallet/WalletViewModelTest.kt`
- `feature-rewards/src/androidInstrumentedTest/kotlin/.../wallet/RewardsWalletHubScreenUiTest.kt`

## 9. Files to Modify
- `core-navigation` `Route` registry — add Rewards Hub route (bottom-nav tab 4 of 5).
- App-level Koin module registration.

## 10. Backend Requirements
Consumes B-02 (`GET /v1/children/{id}/wallet`) via K-01's `WalletRepository`.

## 11. KMP Requirements
- `WalletViewModel` exposes `StateFlow<WalletUiState>` with optimistic local updates reconciled against the next successful server response — never left permanently optimistic (mandatory test, FR-13).
- Card-based dashboard composition: balance header, recent transactions, badge shelf rail (→ K-04), weekly challenge card (→ K-06), daily mission list (→ K-06).
- Tablet layout: Wallet + Badge Shelf side-by-side (responsive Compose layout).

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
`GET /v1/children/{id}/wallet` (B-02) via K-01.

## 14. Database Requirements (Local)
Consumes K-01's `wallet_cache` Room table for offline/instant-load display.

## 15. Validation
Unit test simulating a server response with a different balance than the optimistic local guess, asserting the UI state corrects to the server's authoritative value with no lingering discrepancy (mandatory, PRD §7 item 3).

## 16. Authentication
Reuses shared `core-network` Bearer token attachment (child-mode session).

## 17. Authorization
N/A at UI layer (enforced server-side).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Wallet fetch failure | Show cached `wallet_cache` with a persistent offline indicator |
| New child, zero history | Friendly "Start learning to earn your first XP!" empty state |
| Skeleton loading | Skeleton balance/ledger-list shimmer while first fetch is in flight |

## 19. Offline First
Cached balance display with offline indicator (§18); no write path on this screen (purchases/claims happen on K-06/K-07).

## 20. Local Data
```
Remote (GET /v1/children/{id}/wallet)
   ↓
WalletRepository (K-01)
   ↓
Room wallet_cache
   ↓
WalletUiState (optimistic overlay, reconciled on next server response)
```

## 21. Localization
Transaction reason labels resolved from `reason_type`/`reason_id` via string resources / backend-provided translation keys (EN/HI/AR/UR) — no hardcoded reward-reason strings.

## 22. RTL
Card layout (balance header, transaction list, badge rail) mirrors correctly; verified via dedicated RTL layout test.

## 23. Analytics
`wallet_viewed` fired on screen entry via `AnalyticsTracker.logEvent()`, tied to the server-confirmed wallet response (not fired on cached-only display).

## 24. Performance
Stable/immutable `WalletUiState` model prevents unnecessary recomposition on frequent balance updates; lazy list for transaction history.

## 25. Security
No new sensitive data handling at this layer.

## 26. Library Requirements
Compose Multiplatform, Koin, Ktor (via K-01), Room, kotlinx-coroutines.

## 27. Testing
- Unit: optimistic-update/reconcile correction logic (mandatory).
- UI: default/loading/empty/offline state rendering.
- Accessibility: transaction-entry content-description correctness test.

## 28. Documentation
KDoc on `WalletViewModel` explaining the optimistic-then-reconcile contract and why it must never remain permanently optimistic.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Scaffold `feature-rewards`/`feature-rewards-domain` Modules**
- Objective: establish the new feature module pair.
- Existing Architecture to Follow: `feature-habits`/`feature-habits-domain` convention.
- Files to Create: module `build.gradle.kts` files, package skeleton.
- Files to Modify: `settings.gradle.kts`, Koin registration.
- Definition of Done: modules compile and are DI-wired.

**Task 02 — Implement `GetWalletUseCase`**
- Files to Create: `GetWalletUseCase.kt`
- Existing Files to Reuse: K-01's `WalletRepository`.
- Definition of Done: use case returns correctly-mapped domain model.

**Task 03 — Implement `WalletViewModel` with Optimistic Reconciliation**
- Files to Create: `WalletViewModel.kt`, `WalletUiState.kt`
- Business Rules: FR-13.
- Tests: mandatory reconciliation-correction test.
- Definition of Done: test passes.

**Task 04 — Build `RewardsWalletHubScreen` Composable**
- Existing Files to Reuse: `core-design-system` XP/coin tokens.
- Files to Create: `RewardsWalletHubScreen.kt`
- Implementation Details: card-based dashboard, all documented states, tablet layout.
- Localization/RTL: per §21/§22.
- Analytics: `wallet_viewed` on entry.
- Tests: Compose UI tests per state.
- Definition of Done: all states render correctly, accessibility labels verified.

**Task 05 — Wire Navigation (Bottom-Nav Tab)**
- Files to Modify: `core-navigation` `Route` registry.
- Definition of Done: Rewards tab reachable as bottom-nav position 4 of 5.

**Task 06 — Final Code Review**
- Expected Result: PR merge-ready.

## 30. Definition of Done
Rewards Wallet Hub live, correct optimistic-reconcile behavior, all documented states, full accessibility/localization/RTL support.

## 31. Final Verification Checklist
- [x] `feature-rewards`/`feature-rewards-domain` modules scaffolded and DI-wired
- [x] Optimistic-update/reconcile correction test passes
- [x] All documented states (default, loading, empty, offline) render correctly
- [x] Accessibility labels correct per transaction entry
- [x] Localization (EN/HI/AR/UR) and RTL verified
- [x] Analytics wired via `AnalyticsTracker`
- [x] Bottom-nav Rewards tab registered and reachable
