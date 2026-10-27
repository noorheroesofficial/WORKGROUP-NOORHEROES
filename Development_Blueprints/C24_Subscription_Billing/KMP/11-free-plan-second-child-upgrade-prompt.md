# K-11 — Free-Plan Second-Child Upgrade Prompt

## 1. Feature Context
A parent-mode-only modal shown when a Free-plan family attempts to add a second child profile beyond the plan's 1-child capacity — an upsell prompt into Subscription, never a dead end, and never reachable from child mode.

## 2. Parent Feature
Feature C.24 — Subscription & Billing

## 3. Sub-feature
2.11 Free-Plan Second-Child Upgrade Prompt (ID: **K-11**)

## 4. Objective
Build a `FreeplanUpgradePromptModal` triggered from C.21's Add Child flow when the family is on the Free plan and already has 1 active child, routing the parent to Plan Comparison (K-02) without affecting the existing child's data in any way.

## 5. Business Requirements
- FR-4: "Free plan second-child attempt → upgrade prompt shown in parent mode only, existing child's data unaffected."
- §1.18 Screen 14: Free-Plan Second-Child Upgrade Prompt (parent-mode only) — Modal, Entry: Add Child attempt beyond Free-plan capacity, Exit: Subscription landing.
- §1.9 Acceptance Criteria: "Given a free-tier parent attempts to add a second child, when blocked, then the upgrade prompt appears only in parent mode, with the existing child's data entirely unaffected."

## 6. Existing Architecture
Triggered from C.21's Add Child flow (`ChildManagementRepository`/Add Child screen) when its own capacity check fails — this modal is `:feature:subscription`'s contribution to that flow, not a rebuild of Add Child itself. Consumes B-06's entitlement check (`child_profile_activation` context) to determine the block.

## 7. Existing Code to Reuse
- K-07's `EntitlementRepository.check(CHILD_PROFILE_ACTIVATION, childId)` — the signal source for triggering this modal.
- K-02's `PlanComparisonScreen` — the modal's sole exit/CTA destination.
- `:core:design-system` modal/dialog components.

## 8. Files to Create
- `feature/subscription/ui/components/FreeplanUpgradePromptModal.kt`
- `feature/subscription/viewmodel/FreeplanUpgradePromptViewModel.kt`
- `test/feature/subscription/FreeplanUpgradePromptModalTest.kt`

## 9. Files to Modify
- C.21's Add Child flow — wire the capacity-exceeded case to present this modal instead of a generic error (coordinate with C.21's own blueprint; this file defines the modal's contract, C.21 owns the trigger point's exact call site)

## 10. KMP Requirements
- Modal presented only when the entitlement check returns `entitled: false, reason: child_capacity_exceeded` for a Free-plan family, and only within a parent-mode session — never reachable from a child-mode navigation graph (cross-ref K-08's structural test, which must be extended to cover this modal explicitly).
- Modal copy: clear, non-alarming upsell framing ("Add more children with a Mobile or Premium Family plan"), single primary CTA ("See Plans") routing to K-02, secondary "Not now" dismissal.
- Dismissal or CTA tap must never alter the existing child's data or state in any way — this modal is purely informational/navigational.

## 11. Required API
None directly — reacts to K-07's `EntitlementRepository.check()` result (`CHILD_PROFILE_ACTIVATION` context, B-06).

## 12. Offline First
If offline, the entitlement check falls back to cached state (K-07); if capacity status can't be determined offline, the Add Child attempt should show a connectivity-required message rather than a potentially-stale capacity prompt.

## 13. Local Data
None new.

## 14. Localization
Modal copy, CTA labels fully localized EN/HI/AR/UR.

## 15. RTL
Modal layout mirrors correctly in RTL.

## 16. Analytics
`free_plan_second_child_upsell_shown` per §1.19, fired on modal presentation.

## 17. Performance
Lightweight modal, no additional network call beyond the already-in-flight entitlement check.

## 18. Security
Must be verifiably unreachable from any child-mode session — extend K-08's blocklist-scan test to include this modal's composable explicitly.

## 19. Testing
- Unit test: modal presents only when entitlement check returns `child_capacity_exceeded` for a Free-plan family.
- UI test: "See Plans" CTA navigates to K-02; "Not now" dismisses with zero data mutation.
- UI test: existing child's data/state unaffected by any interaction with this modal (Acceptance Criteria explicit check).
- Structural test (extends K-08): confirm this modal's composable is not reachable from any child-mode-scoped navigation graph.

## 20. AI Coding Agent Implementation Steps

**Task 01 — Implement `FreeplanUpgradePromptViewModel`**
Objective: react to entitlement-check result, expose modal-visibility state. Files to Create: `FreeplanUpgradePromptViewModel.kt`. Dependencies: K-07.

**Task 02 — Implement `FreeplanUpgradePromptModal` Composable**
Objective: modal UI with upsell copy and CTA/dismiss actions. Files to Create: `FreeplanUpgradePromptModal.kt`. Dependencies: Task 01.

**Task 03 — Wire Trigger into C.21's Add Child Flow**
Objective: coordinate with C.21 to present this modal on capacity-exceeded. Files to Modify: C.21's Add Child flow (cross-feature coordination). Dependencies: Task 02.

**Task 04 — Extend K-08's Structural Test**
Objective: add this modal's composable to the child-mode-invisibility blocklist scan. Files to Modify: `SubscriptionChildModeInvisibilityTest.kt` (K-08). Dependencies: Task 02.

**Task 05 — Add Analytics & Test Suite**
Objective: `free_plan_second_child_upsell_shown`, coverage per §19. Dependencies: Tasks 01–04.

## 21. Final Verification Checklist
- [ ] Modal presents only for Free-plan capacity-exceeded case, parent mode only
- [ ] Existing child's data verifiably unaffected by any modal interaction
- [ ] "See Plans" CTA routes correctly to K-02
- [ ] Extended K-08 structural test confirms zero child-mode reachability
- [ ] RTL layout verified

## 22. Definition of Done
The Free-Plan Second-Child Upgrade Prompt correctly presents in parent mode only when a Free-plan family attempts to add a second child, leaves the existing child's data untouched, and routes into Plan Comparison, verified unreachable from child mode.
