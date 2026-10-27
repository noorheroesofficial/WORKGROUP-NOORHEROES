# K-09 — Downgrade Child-Selector Trigger (Delegates to C.21)

## 1. Feature Context
The trigger point on the KMP side for the trial-cancellation/downgrade child-selection flow — C.24 owns detecting *when* the selector must appear; C.21 owns the selector screen itself and the actual disable mechanics. This sub-feature wires that handoff correctly, with zero duplicate disable logic.

## 2. Parent Feature
Feature C.24 — Subscription & Billing

## 3. Sub-feature
2.9 Downgrade Child-Selector Trigger (Delegates to C.21) (ID: **K-09**)

## 4. Objective
Detect a downgrade/trial-cancellation event that reduces plan `child_capacity` below `active_child_count`, and trigger C.21's existing Child Selector screen/flow via its `ChildManagementRepository` — with a test confirming this module calls C.21's repository rather than implementing a parallel selector or disable mechanism.

## 5. Business Requirements
- §1.18 Screen 12: Trial-Cancellation/Downgrade Child Selector — "shared trigger, owned by C.21."
- §5 AI Code-Gen Prompt item 5 (Android): downgrade flow delegates to C.21's existing `ChildManagementRepository`.
- Cross-ref B-07 (backend orchestration) — this is the KMP-side mirror of that same "delegate, never duplicate" constraint.

## 6. Existing Architecture
Consumes C.21's existing `ChildManagementRepository` and its Child Selector screen/navigation route (confirm exact class/route names against C.21's actual KMP implementation before wiring — Do Not Guess).

## 7. Existing Code to Reuse
- C.21's `ChildManagementRepository` (disable-mechanics owner).
- C.21's Child Selector screen/route (UI owner).
- K-01's `SubscriptionViewModel` state (source of the `active_child_count`/`child_capacity` mismatch signal).

## 8. Files to Create
- `feature/subscription/trigger/DowngradeSelectionTrigger.kt` — observes subscription state for a capacity mismatch and initiates navigation into C.21's selector
- `test/feature/subscription/DowngradeSelectionTriggerTest.kt`

## 9. Files to Modify
- `feature/subscription/viewmodel/SubscriptionViewModel.kt` — expose a `requiresChildSelection: Boolean` derived state
- Navigation graph — wire the trigger to launch C.21's existing selector route

## 10. KMP Requirements
- `DowngradeSelectionTrigger` observes `SubscriptionUiState` for `active_child_count > child_capacity`; on detection, navigates to C.21's Child Selector route (does not render its own selector UI).
- On the selector's completion (parent selection made, or C.21's own 24-hour deterministic-fallback notice shown), this module's only remaining responsibility is to refresh `SubscriptionViewModel`'s state — it does not process the selection result itself.
- No local implementation of "which child stays active" logic anywhere in `:feature:subscription`.

## 11. Required API
None directly — this module reacts to state already fetched via `GET /v1/parent/subscription` (B-05); the actual disable call is C.21's (`POST /v1/children/{id}/disable`), invoked through its repository, not called directly from here.

## 12. Offline First
N/A — this trigger only activates in response to a state already reflecting a real subscription change, which itself requires connectivity to have occurred.

## 13. Local Data
None new.

## 14. Localization
N/A directly (no new UI copy owned by this sub-feature — the selector screen's copy is C.21's).

## 15. RTL
N/A directly.

## 16. Analytics
`downgrade_initiated` fired when the trigger detects the capacity mismatch and navigates into C.21's flow (client-side mirror of B-07's server-side event).

## 17. Performance
N/A — infrequent, event-driven trigger.

## 18. Security
**Defining constraint:** this module must never implement its own disable UI or logic — verified by a test confirming it calls C.21's `ChildManagementRepository` rather than a parallel implementation (PRD §7 item 5).

## 19. Testing
- Unit test: capacity mismatch in `SubscriptionUiState` correctly triggers navigation to C.21's Child Selector route.
- Unit test: this module calls C.21's `ChildManagementRepository`/navigation route — mock/spy assertion confirming no parallel disable logic exists (PRD §7 item 5 — critical test).
- Integration test: full downgrade → child-selector (C.21) → disable (C.21) → `SubscriptionViewModel` state refresh.

## 20. AI Coding Agent Implementation Steps

**Task 01 — Expose Capacity-Mismatch State in `SubscriptionViewModel`**
Objective: `requiresChildSelection: Boolean` derived from `active_child_count`/`child_capacity`. Files to Modify: `SubscriptionViewModel.kt`. Dependencies: K-01.

**Task 02 — Implement `DowngradeSelectionTrigger`**
Objective: observe the mismatch, navigate into C.21's existing selector route. Files to Create: `DowngradeSelectionTrigger.kt`. Dependencies: Task 01, C.21's selector route available.

**Task 03 — Wire State Refresh on Selector Completion**
Objective: re-fetch subscription state after C.21's flow completes. Files to Modify: `SubscriptionViewModel.kt`. Dependencies: Task 02.

**Task 04 — Add Delegation-Verification Test Suite**
Objective: coverage per §19, with the delegation-not-duplication test as priority. Dependencies: Tasks 01–03.

## 21. Final Verification Checklist
- [ ] Capacity mismatch correctly triggers navigation into C.21's existing selector (no local selector UI built)
- [ ] Delegation to `ChildManagementRepository` verified by test (no parallel disable logic)
- [ ] `SubscriptionViewModel` state correctly refreshes after selector completion
- [ ] `downgrade_initiated` analytics event fires at the correct trigger point

## 22. Definition of Done
A capacity-reducing downgrade or trial cancellation correctly triggers navigation into C.21's existing Child Selector flow, with zero duplicate selection/disable logic in `:feature:subscription`, verified by a delegation test.
