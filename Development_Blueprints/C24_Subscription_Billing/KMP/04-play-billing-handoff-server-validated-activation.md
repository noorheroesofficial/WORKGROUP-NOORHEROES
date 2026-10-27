# K-04 — Play Billing Handoff & Server-Validated Activation

## 1. Feature Context
The purchase-execution core of the entire feature: launches the Google Play Billing Library's own UI, then treats its local purchase callback strictly as a signal to submit to the backend — never as entitlement truth itself. UI entitlement state updates only from the backend's response.

## 2. Parent Feature
Feature C.24 — Subscription & Billing

## 3. Sub-feature
2.4 Play Billing Handoff & Server-Validated Activation (ID: **K-04**)

## 4. Objective
Implement the Play Billing Library integration so that after a successful local purchase callback, the app immediately calls `SubscriptionRepository.subscribe(receipt)` (B-02) and updates UI state only from that backend response — with a test proving the UI never shows "active" purely from the SDK's local callback.

## 5. Business Requirements
- §5 AI Code-Gen Prompt item 1 (Android): Play Billing local result is a signal to submit to backend, never entitlement truth itself.
- FR-3: confirmation happens through the platform purchase flow only, never a custom form.
- Edge Case #10: mid-trial direct upgrade is a supported explicit path, taking effect immediately per FR-9.

## 6. Existing Architecture
Part of `:feature:subscription`; integrates the Google Play Billing Library (new dependency for this module) per `:feature:subscription`'s technical requirements (§6.1).

## 7. Existing Code to Reuse
- `SubscriptionRepository` (K-01, extend with `subscribe(receipt, plan, isTrial)`).
- `SubscriptionViewModel` (K-01) — entitlement state update path.

## 8. Files to Create
- `feature/subscription/billing/PlayBillingClientWrapper.kt` — thin wrapper around the Play Billing Library
- `feature/subscription/viewmodel/PurchaseHandoffViewModel.kt`
- `test/feature/subscription/PurchaseHandoffViewModelTest.kt`

## 9. Files to Modify
- `feature/subscription/data/SubscriptionRepository.kt` — implement `subscribe()` wrapping `POST /api/v1/billing/subscribe`
- `feature/subscription/ui/TrialDisclosureScreen.kt` — wire "Continue to Purchase" to launch this flow

## 10. KMP Requirements
- `PlayBillingClientWrapper.launchPurchaseFlow(activity, plan)` launches the official SDK UI; on its local callback (`onPurchasesUpdated`), extract the receipt/purchase token only — do not derive any UI-facing entitlement state from it.
- `PurchaseHandoffViewModel.onPurchaseCallback(receipt)` immediately calls `SubscriptionRepository.subscribe(receipt, plan, isTrial)`; UI transitions to "active"/"trial" state **exclusively** from this call's response.
- On backend rejection (fabricated/unverifiable receipt — should not occur with a genuine Play purchase, but must be handled defensively), show a clear error state, never a false "active" state.
- On backend timeout/network failure post-purchase, show a retry-eligible pending state (the purchase happened at the store level; the app must reconcile rather than silently drop it — consider a retry-on-resume mechanism).

## 11. Required API
`POST /api/v1/billing/subscribe` (B-02). **User API.**

## 12. Offline First
Purchase flow requires connectivity by definition; if the backend call fails post-purchase due to connectivity, queue a retry-on-reconnect rather than losing the completed store purchase silently (cross-ref B-04's reconciliation job as an eventual backstop).

## 13. Local Data
Transient pending-purchase state may be locally persisted (not just in-memory) so a retry can survive process death between the store purchase completing and the backend confirming it.

## 14. Localization
Error/pending-state messaging fully localized EN/HI/AR/UR.

## 15. RTL
Pending/error state layouts mirror correctly in RTL.

## 16. Analytics
`trial_started`, `upgrade_completed` fired only after backend confirmation (mirrors B-02's server-side emission, client-side for funnel completeness).

## 17. Performance
Minimize the window between store purchase completion and backend confirmation call; show a clear "Proceeding to purchase" → "Confirming" transition so the parent never sees a stuck/ambiguous state.

## 18. Security
**Defining security property:** the UI must never show an "active" entitlement state derived purely from the Play Billing SDK's local callback before the backend confirms it — this is the client-side enforcement of C.24's platform-wide receipt-is-truth guarantee.

## 19. Testing
- Unit test: UI state remains non-"active" immediately after the SDK callback, transitioning to "active" only after the backend response resolves (PRD §7 item 1 — critical test).
- Unit test: backend rejection of a receipt produces an error state, never a false "active" state.
- Integration test: full trial-start → disclosure → Play Billing handoff → server-validated-activation flow (PRD §6.10).
- Integration test: post-purchase backend-call failure triggers a retryable pending state, not silent data loss.

## 20. AI Coding Agent Implementation Steps

**Task 01 — Integrate Google Play Billing Library**
Objective: add dependency, implement `PlayBillingClientWrapper`. Files to Create: `PlayBillingClientWrapper.kt`. Dependencies: none.

**Task 02 — Implement `SubscriptionRepository.subscribe()`**
Objective: wrap `POST /api/v1/billing/subscribe`. Files to Modify: `SubscriptionRepository.kt`. Dependencies: none.

**Task 03 — Implement `PurchaseHandoffViewModel`**
Objective: orchestrate SDK callback → backend submission → UI state update, per §10. Files to Create: `PurchaseHandoffViewModel.kt`. Dependencies: Tasks 01–02.

**Task 04 — Implement Pending-State Persistence & Retry**
Objective: survive process death between store purchase and backend confirmation. Files to Modify: `PurchaseHandoffViewModel.kt`. Dependencies: Task 03.

**Task 05 — Wire into TrialDisclosureScreen**
Objective: "Continue to Purchase" launches this flow. Files to Modify: `TrialDisclosureScreen.kt`. Dependencies: Task 03.

**Task 06 — Add Analytics & Critical Test Suite**
Objective: `trial_started`/`upgrade_completed` events; coverage per §19, especially the SDK-callback-never-shows-active test. Dependencies: Tasks 01–05.

## 21. Final Verification Checklist
- [ ] UI never shows "active" purely from the local SDK callback (test-verified)
- [ ] Backend response is the sole driver of entitlement UI state
- [ ] Fabricated/rejected receipt produces a clear error state, not a false success
- [ ] Post-purchase backend-call failure is retryable, not silently dropped
- [ ] Full trial-to-activation integration test passes against store sandbox

## 22. Definition of Done
Play Billing purchase flow launches correctly, and UI entitlement state updates exclusively from `POST /api/v1/billing/subscribe`'s backend response — never from the SDK's local callback alone — with resilient handling of post-purchase backend-call failures.
