# K-07 — Plan-Capacity-Blocked State & Subscription Upsell Routing

## 1. Feature Context
Part of Feature C.21 — Multi-Child Management. The shared blocked-state UI reached from both Add Child (K-03) and Enable (K-04) when the family is at or over its plan's child-capacity limit.

## 2. Parent Feature
C.21 Multi-Child Management

## 3. Sub-feature
**K-07 — Plan-Capacity-Blocked State & Subscription Upsell Routing**

## 4. Objective
Present a clear, non-punitive inline block with a direct path to Subscription & Billing (C.24) whenever a capacity-gated action (Add Child or Enable) is rejected by the backend with `403 PLAN_CAPACITY_EXCEEDED`.

## 5. Business Requirements
- FR-8/FR-12: capacity gating on Add Child and Enable, both blocked inline with a clear upsell path.
- §1.18 #6: Plan-Capacity-Blocked State (Add Child) — entry: Add Child attempt beyond capacity; exit: Subscription & Billing (C.24).
- Android AI Prompt item 6: "Implement plan-capacity-blocked states for Add Child and Enable with a CTA to `:feature:subscription`."

## 6. Existing Architecture
Shared Compose state/component within `:feature:child-management`, parameterized by which action triggered it (Add vs. Enable), routing out to `:feature:subscription` via `Navigator`.

## 7. Existing Code to Reuse
- `Navigator.navigateTo(SubscriptionRoute)` — `:feature:subscription`'s existing entry route, reused, not reimplemented.
- Design-system blocked/upsell-state component if one already exists elsewhere in the app (check `:core:design-system` before building a new one).

## 8. Files to Create
- `feature/child-management/src/commonMain/kotlin/.../PlanCapacityBlockedState.kt`

## 9. Files to Modify
- `ChildManagementViewModel.kt` — route `403 PLAN_CAPACITY_EXCEEDED` responses from both `createChild()` and `enableChild()` calls into this shared blocked-state UI, carrying the `{current, limit}` detail through.

## 10. Backend Requirements
Consumes the `403 PLAN_CAPACITY_EXCEEDED` error shape from B-03 and B-05.

## 11. KMP Requirements
- Single shared Composable parameterized by `triggeringAction: CapacityBlockTrigger (AddChild | Enable)` and the `{current, limit}` values, so copy can differ slightly ("You've reached your plan's child limit" vs. "Re-enabling this child would exceed your plan's limit") without forking the component.
- CTA button routes to `:feature:subscription`'s existing entry route.
- Dismissing the blocked state (without tapping the CTA) returns cleanly to K-01's list with zero side effects.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
Consumes the error shape documented in B-03 §13 / B-05 §13 (`{current, limit}`).

## 14. Database Requirements
None.

## 15. Validation
None.

## 16. Authentication
Inherits the parent session already established.

## 17. Authorization
None beyond what the triggering action (K-03/K-04) already enforced.

## 18. Error Handling
This component **is** the error-handling surface for capacity errors — it has no further error states of its own beyond a standard network-failure retry if the CTA navigation itself somehow fails (unlikely, purely local routing).

## 19. Offline First
Not directly relevant — this state is only reached after a network round-trip already completed (the `403` response itself).

## 20. Local Data
None.

## 21. Localization
Both Add-Child and Enable copy variants, plus the CTA label, localized across EN/HI/AR/UR.

## 22. RTL
Layout mirrored correctly under RTL.

## 23. Analytics
`child_add_blocked_plan_capacity`, `child_enable_blocked_plan_capacity` — fired with the triggering action distinguishing which event.

## 24. Performance
Lightweight, stateless-beyond-props component; negligible cost.

## 25. Security
None beyond what the triggering actions already enforce; this component itself performs no privileged operation.

## 26. Library Requirements
No new libraries.

## 27. Testing
- UI test: Add-Child-triggered blocked state renders with correct copy and fires `child_add_blocked_plan_capacity`.
- UI test: Enable-triggered blocked state renders with correct copy and fires `child_enable_blocked_plan_capacity`.
- UI test: CTA routes to `:feature:subscription`'s entry route correctly.
- UI test: dismiss without CTA returns cleanly with no side effects.

## 28. Documentation
KDoc documenting the shared-component-with-trigger-parameter pattern, so future capacity-gated actions elsewhere in the app can reuse this component rather than forking a new blocked state.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Shared Blocked-State Component**
- **Objective:** Build the parameterized Composable.
- **Files to Create:** `PlanCapacityBlockedState.kt`.
- **Implementation Details:** `enum class CapacityBlockTrigger { AddChild, Enable }`; component takes `trigger`, `current: Int`, `limit: Int` as parameters and derives copy/analytics event accordingly.
- **Tests:** UI tests per §27 for both trigger variants.
- **Definition of Done:** One component correctly serves both trigger contexts without duplicated layout code.

**Task 02 — Error Routing from K-03/K-04**
- **Objective:** Wire `403 PLAN_CAPACITY_EXCEEDED` from both call sites into this shared component.
- **Files to Modify:** `ChildManagementViewModel.kt`.
- **Implementation Details:** Both `createChild()` and `enableChild()` error paths check for the typed capacity-exceeded error and navigate to this state with the correct `trigger` value, rather than falling through to a generic error toast.
- **Tests:** Integration tests confirming both call sites correctly route here rather than showing a generic error.
- **Definition of Done:** No capacity-exceeded error from either flow ever surfaces as a generic/unhelpful error message.

**Task 03 — Subscription CTA Routing**
- **Objective:** Wire the CTA to `:feature:subscription`.
- **Files to Modify:** `PlanCapacityBlockedState.kt`.
- **Definition of Done:** Navigation verified via test; no coupling introduced beyond the existing `Navigator`/`Route` abstraction (per `CORE_NAVIGATION_INSTRUCTIONS.md`'s "Data Layers must not depend on core-navigation" and "core-navigation must never depend on a specific feature" rules — this component depends on navigation, not the reverse).

## 30. Definition of Done
Both capacity-exceeded error paths (Add Child, Enable) route to this single shared, correctly-parameterized, fully localized blocked state with working upsell CTA.

## 31. Final Verification Checklist
- [ ] Both trigger variants render correct copy and fire correct analytics event
- [ ] CTA correctly routes to `:feature:subscription`
- [ ] Dismiss-without-CTA path has zero side effects
- [ ] Neither Add-Child nor Enable capacity errors ever fall through to a generic error message
- [ ] Full localization and RTL verified
