# K-06 — Cancellation, Retry-Payment & Restore-Purchase Flows

## 1. Feature Context
Three related parent-initiated actions from the Subscription landing screen: Cancel (with confirmation), Retry Failed Payment (reachable from a PastDue banner/notification), and Restore Purchase.

## 2. Parent Feature
Feature C.24 — Subscription & Billing

## 3. Sub-feature
2.6 Cancellation, Retry-Payment & Restore-Purchase Flows (ID: **K-06**)

## 4. Objective
Implement the Cancel Confirmation screen, Retry Failed Payment screen, and Restore Purchase action, each calling its respective B-05 endpoint and updating UI state only from the backend response.

## 5. Business Requirements
- FR-4: cancel → access continues until period end, then reverts to Free.
- Edge Case #5: restore-purchase re-validates the existing receipt server-side, re-establishes entitlement without a new purchase.
- §1.18 Screens 10, 11, 18: Cancel Flow, Retry Failed Payment, Restore Purchase Action.

## 6. Existing Architecture
Part of `:feature:subscription`; consumes `SubscriptionRepository.cancel()`/`restore()`, and K-04's `PlayBillingClientWrapper` for the retry-payment handoff.

## 7. Existing Code to Reuse
- `SubscriptionRepository` (K-01/K-04).
- `PlayBillingClientWrapper` (K-04) — retry payment reuses the same Play Billing launch mechanism.
- `:core:design-system` confirmation-dialog pattern.

## 8. Files to Create
- `feature/subscription/ui/CancelConfirmationScreen.kt`
- `feature/subscription/ui/RetryFailedPaymentScreen.kt`
- `feature/subscription/ui/components/RestorePurchaseButton.kt`
- `feature/subscription/viewmodel/CancelRestoreViewModel.kt`
- `test/feature/subscription/CancelRestoreViewModelTest.kt`

## 9. Files to Modify
- `feature/subscription/data/SubscriptionRepository.kt` — add `cancel()`, `restore(receipt)`
- `feature/subscription/ui/SubscriptionLandingScreen.kt` — wire Cancel/Restore actions
- `feature/subscription/navigation/SubscriptionRoute.kt` — add `CancelConfirmationRoute`, `RetryFailedPaymentRoute`

## 10. KMP Requirements
- Cancel: confirmation screen → `SubscriptionRepository.cancel()` → on success, update landing screen state to `Canceled` with `access_until` shown; explicit copy that access continues until that date.
- Retry Failed Payment: reachable from a PastDue banner (K-10's deep link) or the landing screen; launches K-04's Play Billing flow for the failed payment method, on success calls backend to confirm recovery.
- Restore Purchase: a button/action calling `SubscriptionRepository.restore(receipt)` (obtaining the receipt via the Play Billing Library's own restore/query-purchases API first); shows "nothing to restore" as a valid, non-error outcome.
- All three flows require connectivity; disabled with clear messaging if offline.

## 11. Required API
`POST /v1/parent/subscription/cancel`, `POST /v1/parent/subscription/restore` (both B-05). **User API.**

## 12. Offline First
All three actions require connectivity; offline state disables the actions with explicit "requires connection" messaging rather than allowing a queued/optimistic action (billing actions must not be optimistically applied).

## 13. Local Data
None new beyond K-01's subscription snapshot cache, which these actions update on success.

## 14. Localization
Cancel confirmation copy, retry-payment messaging, and restore-purchase outcomes ("restored" / "nothing to restore" / error) fully localized EN/HI/AR/UR.

## 15. RTL
All three screens/components mirror correctly in RTL.

## 16. Analytics
`cancellation_initiated`→`cancellation_completed`, `restore_purchase_initiated`→`restore_purchase_completed`, `payment_recovered` per §1.19.

## 17. Performance
No special concerns; standard loading-state-during-mutation pattern for all three actions.

## 18. Security
Cancel is explicitly a reversible-until-period-end action (PRD §2.3 — "Step-up not required"), consistent with C.24's own hard rule that only purchases/AI controls/external links/deletion/profile-edits require step-up PIN — cancel does not, but must still require an active parent session.

## 19. Testing
- Unit: cancel success updates state to `Canceled` with correct `access_until` displayed.
- Unit: restore with no active purchase shows "nothing to restore," not an error state.
- UI: cancel confirmation dialog copy matches "access continues until period end" framing exactly.
- UI: retry-payment flow reuses K-04's Play Billing launch correctly.
- UI: all three actions disabled offline with correct messaging.

## 20. AI Coding Agent Implementation Steps

**Task 01 — Implement Repository Methods**
Objective: `cancel()`, `restore(receipt)`. Files to Modify: `SubscriptionRepository.kt`. Dependencies: K-01.

**Task 02 — Implement `CancelRestoreViewModel`**
Objective: state management for all three flows. Files to Create: `CancelRestoreViewModel.kt`. Dependencies: Task 01.

**Task 03 — Implement Cancel Confirmation Screen**
Objective: confirmation dialog/screen with correct access-continues copy. Files to Create: `CancelConfirmationScreen.kt`. Dependencies: Task 02.

**Task 04 — Implement Retry Failed Payment Screen**
Objective: reuse K-04's Play Billing launch for payment retry. Files to Create: `RetryFailedPaymentScreen.kt`. Dependencies: Task 02, K-04.

**Task 05 — Implement Restore Purchase Button/Flow**
Objective: query Play Billing's existing purchases, call `restore()`, handle "nothing to restore." Files to Create: `RestorePurchaseButton.kt`. Dependencies: Task 02.

**Task 06 — Wire Navigation & Add Analytics/Test Suite**
Objective: entry points from landing screen and PastDue banner; events per §16; coverage per §19. Files to Modify: `SubscriptionLandingScreen.kt`, `SubscriptionRoute.kt`. Dependencies: Tasks 01–05.

## 21. Final Verification Checklist
- [ ] Cancel confirmation copy explicitly states access continues until period end
- [ ] Restore "nothing to restore" verified as a non-error outcome
- [ ] Retry-payment reuses K-04's Play Billing launch, not a duplicate implementation
- [ ] All three actions disabled offline with clear messaging
- [ ] RTL layout verified

## 22. Definition of Done
Cancel, Retry Failed Payment, and Restore Purchase flows all function correctly against B-05's endpoints, with UI state updated only from backend responses and correct offline/localization/RTL handling.
