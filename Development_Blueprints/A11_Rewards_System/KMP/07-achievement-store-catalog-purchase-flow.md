# K-07 — Achievement Store (Catalog Browse & Purchase Flow)

## 1. Feature Context
Part of Feature A.11 — Rewards System. The only spend-side UI in the reward economy; browses the admin-managed catalog and executes purchases with a hard guarantee against any payment/IAP affordance.

## 2. Parent Feature
A.11 Rewards System — KMP App (Android/iOS)

## 3. Sub-feature
K-07 Achievement Store (Catalog Browse & Purchase Flow)

## 4. Objective
Build the Achievement Store grid, Item Detail, and Purchase Confirmation/Shortfall screens (§1.18 #17–19), backing FR-1, FR-8, FR-11.

## 5. Business Requirements
- Insufficient-points path renders a shortfall screen with the gap amount and "earn more" deep-link suggestions — never a "buy points" affordance.
- Purchase idempotency key generated once at purchase-tap time, reused on retry.
- Purchase success navigates toward Avatar Inventory (A.12 boundary — this screen stops at inventory grant confirmation).

## 6. Existing Architecture
`feature-rewards` module. Consumes B-06 via K-01's `AchievementStoreRepository`.

## 7. Existing Code to Reuse
- K-01's `AchievementStoreRepository`.
- `core-design-system` price-tag/item-card tokens.
- `core-navigation` deep links into other feature modules (for "earn more" suggestions).

## 8. Files to Create
- `feature-rewards/src/commonMain/kotlin/.../store/AchievementStoreScreen.kt`
- `feature-rewards/src/commonMain/kotlin/.../store/StoreItemDetailScreen.kt`
- `feature-rewards/src/commonMain/kotlin/.../store/PurchaseConfirmationScreen.kt`
- `feature-rewards/src/commonMain/kotlin/.../store/InsufficientPointsShortfallScreen.kt`
- `feature-rewards/src/commonMain/kotlin/.../store/AchievementStoreViewModel.kt`
- `feature-rewards/src/commonTest/kotlin/.../store/PurchaseIdempotencyKeyReuseTest.kt`
- `feature-rewards/src/androidInstrumentedTest/kotlin/.../store/NoPaymentAffordanceUiTest.kt`

## 9. Files to Modify
- `core-navigation` `Route` registry — Store, Item Detail, Purchase Confirmation routes.

## 10. Backend Requirements
Consumes B-06 (`GET /v1/catalog-items`, `POST /v1/rewards/claims`).

## 11. KMP Requirements
- Idempotency key generated once at the moment "Buy" is tapped (not regenerated on retry) — reused identically across any retry, per K-01's repository contract.
- Insufficient-points UI branch triggered strictly from a `402`-mapped `NoorResult.Error` variant; renders shortfall + deep links to "earn more" activities.
- Category filtering, owned/locked visual states.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
`GET /v1/catalog-items`, `POST /v1/rewards/claims` (B-06).

## 14. Database Requirements (Local)
Room `catalog_items_cache` (K-01) for offline browsing; purchases require connectivity, never queued.

## 15. Validation
UI test (mandatory) asserting the shortfall screen never renders any "buy points," "add funds," or payment-related UI element, since no such capability exists in this app by design.

## 16. Authentication
Reuses shared `core-network` Bearer token attachment.

## 17. Authorization
N/A at UI layer (server-side scoping per B-06).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Insufficient balance (`402`) | Shortfall screen with gap + earn-more deep links |
| Duplicate purchase tap | Idempotent replay via reused key; UI shows the single success state, no double-charge visual |
| Offline purchase attempt | Buy action disabled/blocked with an explicit "connect to buy" message, no silent failure |
| Catalog fetch failure | Cached catalog shown with offline indicator; Buy disabled while offline |

## 19. Offline First
Catalog browse is offline-tolerant (cached); purchase requires connectivity by design (B-06 §19).

## 20. Local Data
```
Remote (GET /v1/catalog-items)
   ↓
AchievementStoreRepository (K-01)
   ↓
Room catalog_items_cache
   ↓
AchievementStoreViewModel state (owned/locked/insufficient-eligible per item)
```

## 21. Localization
Item names/categories/price labels localized; price tags always paired with text, never icon-only (accessibility + localization combined requirement).

## 22. RTL
Grid/detail/confirmation layouts mirror correctly for Arabic/Urdu.

## 23. Analytics
`achievement_store_viewed/item_viewed/purchase_attempted/purchase_completed/purchase_insufficient_points`, `avatar_item_equipped_post_purchase` (the latter fired once A.12's equip flow confirms, cross-feature event).

## 24. Performance
Catalog grid uses stable item keys; image/asset loading for item art follows the platform's existing image-loading conventions (no new image pipeline introduced here).

## 25. Security
No payment/IAP code path exists anywhere in this screen set — verified by the mandatory UI test in §15, mirroring B-06's backend schema-scan guarantee.

## 26. Library Requirements
Compose Multiplatform, Koin, Room, kotlinx-coroutines.

## 27. Testing
- Unit: idempotency-key reuse-on-retry test (mandatory).
- UI: no-payment-affordance test on the shortfall screen (mandatory).
- Integration: purchase → atomic debit+inventory grant confirmed → navigation toward Avatar Inventory.

## 28. Documentation
KDoc noting the hard architectural rule: no payment/IAP UI element may ever be added to this screen set, cross-referenced against B-06's backend guarantee.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement `AchievementStoreViewModel`**
- Files to Create: `AchievementStoreViewModel.kt`
- Business Rules: FR-1, FR-8, FR-11.
- Implementation Details: idempotency-key generation at tap-time.
- Tests: idempotency-key reuse test (mandatory).
- Definition of Done: test passing.

**Task 02 — Build `AchievementStoreScreen` & `StoreItemDetailScreen`**
- Existing Files to Reuse: `core-design-system` price-tag/item-card tokens.
- Localization/RTL/Accessibility: per §21/§22.
- Definition of Done: category filtering, owned/locked states correctly rendered.

**Task 03 — Build `PurchaseConfirmationScreen` & `InsufficientPointsShortfallScreen`**
- Files to Create: both screens.
- Error Handling: per §18.
- Tests: no-payment-affordance UI test (mandatory).
- Definition of Done: test passing.

**Task 04 — Wire Offline Buy-Disable Behavior**
- Implementation Details: Buy action disabled while offline, explicit messaging.
- Definition of Done: verified via connectivity-toggle test.

**Task 05 — Wire Navigation & Deep Links**
- Files to Modify: `core-navigation` `Route` registry.
- Definition of Done: earn-more deep links route correctly to originating feature modules.

**Task 06 — Final Code Review**
- Do Not Change: never add a payment/IAP UI element to this screen set.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Achievement Store live; purchase flow idempotent and connectivity-gated; shortfall screen verifiably free of any payment affordance.

## 31. Final Verification Checklist
- [x] Idempotency key generated once at tap-time, reused on retry
- [x] Shortfall screen contains zero payment/IAP elements (mandatory UI test passing)
- [x] Offline Buy action disabled with clear messaging
- [x] Category filtering and owned/locked states correct
- [x] Purchase success flow navigates toward Avatar Inventory (A.12 boundary respected)
- [x] Localization/RTL verified

## 32. Verification Sign-Off Ledger (2026-09-25)
- **Files Created & Updated (`< 500 lines` ceiling strictly enforced):**
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/store/AchievementStoreUiState.kt` (264 lines)
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/store/AchievementStoreViewModel.kt` (465 lines)
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/store/AchievementStoreScreen.kt` (362 lines)
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/store/AchievementStoreComponents.kt` (286 lines)
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/store/StoreItemDetailScreen.kt` (419 lines)
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/store/PurchaseConfirmationScreen.kt` (266 lines)
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/store/InsufficientPointsShortfallScreen.kt` (409 lines)
  - `core/rewards-client/src/commonMain/kotlin/com/noorheroes/core/rewards/client/data/AchievementStoreRepository.kt` (208 lines — persists `owned = true` in Room `catalog_items_cache` alongside wallet balance reconciliation upon purchase confirmation)
  - `core/core-navigation/src/commonMain/kotlin/com/noorheroes/core/navigation/RewardsRoutes.kt` (127 lines — `StoreItemDetailRoute`, `PurchaseConfirmationRoute`, `InsufficientPointsShortfallRoute`)
  - `core/core-common/src/commonMain/composeResources/values*/strings_rewards.xml` (286 keys across `values`, `values-ar`, `values-hi`, `values-ur` — 100% 4-locale parity)
  - `feature/feature-rewards/src/commonTest/kotlin/com/noorheroes/feature/rewards/store/StoreTestFakes.kt` (202 lines)
  - `feature/feature-rewards/src/commonTest/kotlin/com/noorheroes/feature/rewards/store/PurchaseIdempotencyKeyReuseTest.kt` (311 lines — 9 unit & integration tests)
  - `feature/feature-rewards/src/commonTest/kotlin/com/noorheroes/feature/rewards/store/NoPaymentAffordanceUiTest.kt` (87 lines — 4 UI audit tests)
  - `feature/feature-rewards/src/androidInstrumentedTest/kotlin/com/noorheroes/feature/rewards/store/NoPaymentAffordanceUiTest.kt` (46 lines)
- **Visual & Architectural Fidelity:**
  - 100% pixel-accurate reproduction of `Screens/Mobile App/Rewards/Achievement Store-01.png` through `Achievement Store-04.png` (Circular `←` back button + bold `h1` `"Achievement Store"` title + `✦ {balance} NP` pill, horizontal category filter chips `All`/`Avatars`/`Themes`/`Badges`, 2-column grid with stable `key(item.id)`, initial unselected 6-card browse state (`01.png`), owned green `✓` badge & `"You already own this ✓"` bottom card (`02.png`), unowned `"Get for {cost} NP"` bottom card (`03.png`), and `Badges` filtered state (`04.png`)).
  - Closed-economy rule strictly enforced (`ShortfallScreenAuditHelper` + `NoPaymentAffordanceUiTest`).
  - Tap-time idempotency key generated once and reused identically across retries (`PurchaseIdempotencyKeyReuseTest`).


