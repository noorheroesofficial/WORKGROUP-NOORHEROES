# K-08 — Child-Mode Billing Invisibility Safeguard

## 1. Feature Context
The structural, test-enforced guarantee that no billing/subscription content — screens, composables, upsell prompts, or text — is ever reachable from a child-mode session, anywhere in the app. This is the Android-side enforcement of C.24's defining child-safety commitment (FR-8), verified at the point of consumption across every child-facing screen, not just at `:feature:subscription`'s own boundary.

## 2. Parent Feature
Feature C.24 — Subscription & Billing

## 3. Sub-feature
2.8 Child-Mode Billing Invisibility Safeguard (ID: **K-08**)

## 4. Objective
Implement a content-safety-style UI test (mirroring A.2's billing-content-absence pattern) that renders Home, Stories, Learn, Rewards, and Profile screens under a child-mode session fixture and asserts none of them contain any composable from `:feature:subscription` or any text matching billing-related terms.

## 5. Business Requirements
- FR-8: purchases, AI controls, external links, deletion/export, and profile edits require parent PIN; child mode never exposes billing or account-management controls.
- §5 AI Code-Gen Prompt item 7 (Backend, mirrored client-side here): structural child-mode-token rejection; §7 item 3 (Android): content-safety-style UI test.
- Cross-ref A.2's platform-wide no-billing-content-to-child rule — this sub-feature is its concrete enforcement point for the Subscription feature specifically.

## 6. Existing Architecture
Follows A.2's existing billing-content-absence test pattern exactly (confirm exact fixture/test-harness location in A.2's KMP blueprints before building a divergent pattern here — reuse, do not reinvent).

## 7. Existing Code to Reuse
- A.2's child-mode session test fixture and blocklist-scan test harness.
- `:feature:subscription`'s full composable inventory (K-01 through K-06, K-09, K-10) as the blocklist source.

## 8. Files to Create
- `test/childsafety/SubscriptionChildModeInvisibilityTest.kt` — renders Home/Stories/Learn/Rewards/Profile under a child-mode fixture, asserts zero `:feature:subscription` composables and zero billing-term text matches
- `test/childsafety/BillingTermBlocklist.kt` — shared blocklist of billing-related terms/strings (e.g., "subscribe," "trial," "$," "billing," "plan," "upgrade") reused by the text-scan assertion

## 9. Files to Modify
- Navigation graphs for Home/Stories/Learn/Rewards/Profile — audit and confirm no conditional path exists that could route to `:feature:subscription` under a child-mode session (fix if found, do not just test around it)

## 10. KMP Requirements
- The test renders each of the five child-mode-reachable screens under a `ChildSessionContext` fixture and performs a composable-tree scan for any `:feature:subscription` package-prefixed composable.
- A parallel text-scan asserts no rendered text matches the shared billing-term blocklist (`BillingTermBlocklist.kt`).
- This test must be added to the CI-blocking suite, re-run on every release touching child-mode navigation (mirrors PRD §13.5 regression-case requirement).
- If any violation is found during initial implementation, the underlying navigation/composable-inclusion bug must be fixed, not the test relaxed.

## 11. Required API
None — this is a pure client-side structural/UI test sub-feature.

## 12. Offline First
N/A.

## 13. Local Data
N/A.

## 14. Localization
The billing-term blocklist must cover terms in all four supported locales (EN/HI/AR/UR) to catch localized billing copy leaking into child-mode screens, not just English terms.

## 15. RTL
N/A directly, though the blocklist-scan must still function correctly against RTL-rendered (Arabic/Urdu) text content.

## 16. Analytics
N/A.

## 17. Performance
N/A — this is a test-suite sub-feature, not a runtime performance concern.

## 18. Security
**This entire sub-feature IS a security/child-safety control.** Its test must be treated as a non-bypassable CI gate, consistent with PRD §12.9's pre-launch security checklist item: "Android-side billing-content-absence verified across every child-mode-reachable screen."

## 19. Testing
- The blocklist-scan test itself, covering all five specified screens (Home, Stories, Learn, Rewards, Profile).
- A deliberately-broken fixture test (temporarily inject a subscription composable into one screen in a test-only branch) to prove the scan actually catches violations, not just passes trivially on an already-clean tree.
- Multi-locale text-scan verification (EN/HI/AR/UR blocklist terms all checked).

## 20. AI Coding Agent Implementation Steps

**Task 01 — Build Shared Billing-Term Blocklist**
Objective: multi-locale list of billing-related terms/strings. Files to Create: `BillingTermBlocklist.kt`. Dependencies: none.

**Task 02 — Implement Composable-Tree Scan Test Harness**
Objective: render each of the 5 screens under a child-mode fixture, scan for `:feature:subscription` composables. Files to Create: `SubscriptionChildModeInvisibilityTest.kt`. Dependencies: A.2's existing fixture pattern, Task 01.

**Task 03 — Audit & Fix Navigation Graphs**
Objective: confirm/fix that no child-mode-reachable path can route into `:feature:subscription`. Files to Modify: relevant navigation graph files. Dependencies: Task 02 (run test first to detect any existing violation).

**Task 04 — Register as CI-Blocking Regression Suite**
Objective: ensure this test runs on every release touching child-mode navigation. Dependencies: Tasks 01–03.

**Task 05 — Add Deliberately-Broken Fixture Verification**
Objective: prove the test actually catches violations (temporary test-only injection, then removed). Dependencies: Task 02.

## 21. Final Verification Checklist
- [ ] Zero `:feature:subscription` composables reachable from any of the 5 child-mode screens
- [ ] Zero billing-term text matches across all 4 locales
- [ ] Test proven to actually catch violations (not a trivially-passing no-op)
- [ ] Registered as a CI-blocking, release-gating regression test
- [ ] Any discovered violation fixed at the navigation/composable-inclusion level, not test-relaxed

## 22. Definition of Done
A CI-blocking structural test confirms zero billing/subscription content is reachable from any child-mode session across Home, Stories, Learn, Rewards, and Profile, in all four supported locales, with any discovered violation fixed at the source.
