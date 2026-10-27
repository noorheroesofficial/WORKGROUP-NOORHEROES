# K-10 — Renewal & Payment-Failure Notification Deep-Link Handling

## 1. Feature Context
Handles deep links from C.25-owned push notifications — renewal reminders (7-day/24-hour) and payment-failure alerts — routing the parent into the correct Subscription screen (landing, or directly into Retry Failed Payment).

## 2. Parent Feature
Feature C.24 — Subscription & Billing

## 3. Sub-feature
2.10 Renewal & Payment-Failure Notification Deep-Link Handling (ID: **K-10**)

## 4. Objective
Implement deep-link handling for `noorheroes://parent/subscription` (and a payment-failure-specific variant routing directly into K-06's Retry Failed Payment screen) triggered by C.25's push notifications, with graceful handling of stale/invalid payloads.

## 5. Business Requirements
- §6.9: renewal-reminder and payment-failure notifications (owned by C.25) deep-link here.
- FR-4: renewal reminder — annual plans notify 7 days and 24 hours before renewal; payment failure — parent receives email/push reminder, enters a grace period.
- Edge Case #7: parent-facing renewal notification is unaffected by the child's own bedtime/quiet-hours configuration (governed by C.25's own parent-notification-preferences, not C.23).

## 6. Existing Architecture
Extends the base deep-link `noorheroes://parent/subscription` (K-01) with payload-driven routing variants; integrates with C.25's existing notification-tap-to-deep-link dispatch mechanism (confirm exact integration point against C.25's implementation before wiring — Do Not Guess).

## 7. Existing Code to Reuse
- K-01's `SubscriptionRoute` and deep-link registration.
- K-06's `RetryFailedPaymentScreen` route.
- C.25's existing notification-payload-to-deep-link dispatch pattern.

## 8. Files to Create
- `feature/subscription/navigation/SubscriptionDeepLinkHandler.kt`
- `test/feature/subscription/SubscriptionDeepLinkHandlerTest.kt`

## 9. Files to Modify
- `core-navigation/Route.kt` — add a payment-failure-specific deep-link variant if distinct from the base subscription link (e.g., `noorheroes://parent/subscription/retry-payment`)
- `feature/subscription/navigation/SubscriptionRoute.kt` — ensure `RetryFailedPaymentRoute` (K-06) is deep-linkable directly, not only reachable via in-app navigation

## 10. KMP Requirements
- Renewal-reminder deep link → Subscription landing (K-01), with the renewal-reminder banner/context surfaced if applicable.
- Payment-failure deep link → routes directly into K-06's Retry Failed Payment screen, skipping the landing screen for a faster resolution path.
- Stale/invalid deep-link payload (e.g., referencing a subscription state that has since changed, such as a payment already recovered) → falls back gracefully to the Subscription landing screen showing current accurate state, never a broken/blank screen.
- This handler does not fire any notification itself — C.25 owns notification delivery; this sub-feature only owns the tap-to-navigate resolution.

## 11. Required API
None directly — relies on K-01's already-implemented `GET /v1/parent/subscription` call once the destination screen loads, to always show current accurate state regardless of what the notification payload implied.

## 12. Offline First
Deep-link navigation itself works offline (pure routing); the destination screen's own offline-state handling (K-01/K-06) applies once landed.

## 13. Local Data
None new.

## 14. Localization
N/A directly (no new UI copy — routes into existing localized screens).

## 15. RTL
N/A directly.

## 16. Analytics
`renewal_reminder_shown`, `grace_period_entered`, `grace_period_expired` per §1.19 — fired based on the resulting screen state after navigation resolves, not by this handler itself.

## 17. Performance
N/A — lightweight routing logic.

## 18. Security
Deep-link payload must not be trusted for entitlement state — the destination screen always re-fetches current state from the backend (K-01/K-06), never rendering directly from notification payload data (consistent with the platform-wide receipt/webhook-is-truth philosophy applied to the client's own notification-driven navigation).

## 19. Testing
- Unit test: renewal-reminder deep link routes to Subscription landing.
- Unit test: payment-failure deep link routes directly to Retry Failed Payment.
- Unit test: stale/invalid payload falls back gracefully to landing screen with current accurate state, not a crash or blank screen.
- Integration test: full notification-tap → deep-link → correct-screen-with-fresh-data flow.

## 20. AI Coding Agent Implementation Steps

**Task 01 — Register Payment-Failure Deep-Link Variant**
Objective: distinct deep link routing directly to Retry Failed Payment. Files to Modify: `core-navigation/Route.kt`. Dependencies: K-06.

**Task 02 — Implement `SubscriptionDeepLinkHandler`**
Objective: resolve incoming deep links to the correct destination per §10, with graceful stale-payload fallback. Files to Create: `SubscriptionDeepLinkHandler.kt`. Dependencies: Task 01.

**Task 03 — Integrate with C.25's Notification Dispatch**
Objective: confirm and wire the actual tap-to-deep-link trigger point. Dependencies: Task 02, C.25's notification implementation.

**Task 04 — Add Test Suite**
Objective: coverage per §19. Dependencies: Tasks 01–03.

## 21. Final Verification Checklist
- [ ] Renewal-reminder deep link routes to Subscription landing
- [ ] Payment-failure deep link routes directly to Retry Failed Payment
- [ ] Stale/invalid payload handled gracefully, never a crash or blank screen
- [ ] Destination screen always shows freshly-fetched state, never data trusted directly from the notification payload

## 22. Definition of Done
Both renewal-reminder and payment-failure notification deep links correctly route to their respective Subscription screens with always-fresh backend-sourced state, gracefully handling stale payloads.
