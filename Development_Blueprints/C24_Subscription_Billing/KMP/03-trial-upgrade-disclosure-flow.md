# K-03 — Trial & Upgrade Disclosure Flow

## 1. Feature Context
The mandatory, unhurried disclosure screen shown before any purchase confirmation — trial length, post-trial price, renewal date, auto-renew statement — with a "Continue to Purchase" action that hands off to the OS billing sheet. A Direct Upgrade Disclosure variant serves non-trial upgrades.

## 2. Parent Feature
Feature C.24 — Subscription & Billing

## 3. Sub-feature
2.3 Trial & Upgrade Disclosure Flow (ID: **K-03**)

## 4. Objective
Build `TrialDisclosureScreen` (and its Direct Upgrade variant) so the "Continue to Purchase" button is enabled only after all four disclosure elements (trial length, post-trial price, renewal date, auto-renew statement) are actually composed on screen — not merely present in the ViewModel — before handing off to K-04's Play Billing flow.

## 5. Business Requirements
- FR-3: parent sees trial length, post-trial price, renewal date, and auto-renew disclosure before confirming; confirmation only through the platform purchase flow.
- §2.2 Trial Disclosure screen: components are the four disclosure rows, "Continue to Purchase" CTA, transition state before the external sheet opens.
- Edge Case #10: mid-trial direct upgrade uses the Direct Upgrade Disclosure variant, superseding scheduled day-7 conversion.

## 6. Existing Architecture
Part of `:feature:subscription`. Receives selected plan code (and trial-vs-direct-upgrade mode) as nav arguments from K-02.

## 7. Existing Code to Reuse
- `:core:design-system` typography/spacing tokens for "calm, clear, unhurried" disclosure visual language (§2.1).
- `PlanComparisonViewModel`'s already-fetched plan pricing data (avoid re-fetching for disclosure figures).

## 8. Files to Create
- `feature/subscription/ui/TrialDisclosureScreen.kt`
- `feature/subscription/viewmodel/TrialDisclosureViewModel.kt`
- `test/feature/subscription/TrialDisclosureScreenTest.kt`

## 9. Files to Modify
- `feature/subscription/navigation/SubscriptionRoute.kt` — add `TrialDisclosureRoute` (with `isDirectUpgrade: Boolean` argument)

## 10. KMP Requirements
- Compute `renewal_date` client-side from `trial_length + today`, or source directly from the plan catalog response if the backend supplies it — confirm exact field source before implementation (Do Not Guess).
- "Continue to Purchase" button `enabled` state is driven by a Compose-level check that all four disclosure `Text` composables have actually been laid out (e.g., gate on a post-first-composition flag), not just ViewModel field non-nullness — this is a UI test requirement, not just a logic requirement (PRD §7 item 4).
- On confirm, transitions to a brief "Proceeding to purchase" state before launching K-04's Play Billing handoff.
- "Cancel" link returns to Plan Comparison without initiating any purchase.

## 11. Required API
None directly — this screen composes data already fetched by K-02's plan catalog call; no additional network call.

## 12. Offline First
N/A — reachable only after Plan Comparison has successfully loaded plan data; if connectivity drops before "Continue to Purchase" is tapped, K-04's Play Billing launch will itself fail gracefully with a connectivity error.

## 13. Local Data
None new.

## 14. Localization
All four disclosure rows, the auto-renew statement, and "Continue to Purchase"/"Cancel" fully localized EN/HI/AR/UR — this is the platform's core "no surprise charging" trust commitment and must never rely on approximate/machine-only translation for financial terms.

## 15. RTL
Disclosure card layout, button, and cancel link mirror correctly in RTL.

## 16. Analytics
`trial_disclosure_viewed` on screen composition.

## 17. Performance
No network call on this screen; instant render from already-fetched data.

## 18. Security
No purchase or receipt logic lives here — this screen only collects informed confirmation and hands off to K-04.

## 19. Testing
- UI test: "Continue to Purchase" is disabled/absent until all four disclosure elements are actually composed on screen (PRD §7 item 4 — critical test).
- UI test: Direct Upgrade Disclosure variant renders correctly for the mid-trial-upgrade case (Edge Case #10).
- UI test: "Cancel" returns to Plan Comparison, no purchase initiated.
- Unit: `TrialDisclosureViewModel` correctly computes/sources all four disclosure fields for a given plan.

## 20. AI Coding Agent Implementation Steps

**Task 01 — Implement `TrialDisclosureViewModel`**
Objective: source/compute the four disclosure fields for the selected plan and mode (trial vs. direct upgrade). Files to Create: `TrialDisclosureViewModel.kt`. Dependencies: K-02.

**Task 02 — Implement `TrialDisclosureScreen` Composable with Gated CTA**
Objective: render four disclosure rows, gate "Continue to Purchase" on full composition per §10. Files to Create: `TrialDisclosureScreen.kt`. Dependencies: Task 01.

**Task 03 — Wire Navigation to K-04**
Objective: "Continue to Purchase" launches K-04's Play Billing handoff with plan/trial-mode arguments; "Cancel" returns to Plan Comparison. Files to Modify: `SubscriptionRoute.kt`. Dependencies: Task 02.

**Task 04 — Add Analytics & Test Suite**
Objective: `trial_disclosure_viewed`, coverage per §19, including the critical CTA-gating UI test. Dependencies: Tasks 01–03.

## 21. Final Verification Checklist
- [ ] "Continue to Purchase" verified disabled until all four disclosure elements are actually rendered on screen
- [ ] Direct Upgrade Disclosure variant correctly triggered for mid-trial upgrade (Edge Case #10)
- [ ] All disclosure copy fully localized, no hardcoded English fallback for financial terms
- [ ] "Cancel" path verified to initiate zero purchase action
- [ ] RTL layout verified

## 22. Definition of Done
`TrialDisclosureScreen` (and Direct Upgrade variant) renders all four required disclosure elements, gates the purchase CTA on their actual composition, and correctly hands off to K-04 only after informed confirmation.
