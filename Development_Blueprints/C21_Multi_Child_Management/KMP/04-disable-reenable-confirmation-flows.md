# K-04 — Disable & Re-Enable Confirmation Flows

## 1. Feature Context
Part of Feature C.21 — Multi-Child Management. Implements the two reversible lifecycle actions, each behind a step-up gate and a lightweight confirmation step.

## 2. Parent Feature
C.21 Multi-Child Management

## 3. Sub-feature
**K-04 — Disable & Re-Enable Confirmation Flows**

## 4. Objective
Let a parent disable a child (immediate, reversible, data-preserving) or re-enable one (immediate, capacity-checked), each gated by step-up and confirmed with a lightweight modal — never a silent action.

## 5. Business Requirements
- §1.18 #8/#9: Disable Confirmation and Re-Enable Confirmation, both step-up gated.
- Acceptance Criteria: disable revokes sessions/bindings immediately while retaining data; re-enable within capacity restores access with data intact; at capacity, blocked with upsell.

## 6. Existing Architecture
Compose modal/screen within `:feature:child-management`, invoked from K-02's action menu.

## 7. Existing Code to Reuse
- `ParentGateLauncher.requireParentAuth()` (C.19).
- `FamilyRepository.disableChild()`/`enableChild()` — new thin wrappers over B-04/B-05, following the same pattern as K-03's `createChild()`/`updateChild()`.

## 8. Files to Create
- `feature/child-management/src/commonMain/kotlin/.../DisableConfirmationScreen.kt`
- `feature/child-management/src/commonMain/kotlin/.../ReEnableConfirmationScreen.kt`

## 9. Files to Modify
- `core-data/.../FamilyRepositoryImpl.kt` — add `disableChild(childId)`/`enableChild(childId)`.
- `ChildManagementViewModel.kt` — add disable/enable action handlers.

## 10. Backend Requirements
Consumes B-04 (disable) and B-05 (enable).

## 11. KMP Requirements
- Both flows: step-up gate → confirmation modal → action → optimistic UI update on success (card flips to disabled/active immediately, matching K-01's list state).
- Enable flow specifically handles `403 PLAN_CAPACITY_EXCEEDED` by routing to K-07's blocked state instead of showing a generic error.
- Neither flow performs any local data mutation beyond the `status` field — no client-side assumption about progress/history being touched.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
Consumes B-04/B-05 contracts as documented in those blueprints.

## 14. Database Requirements
Local Room `Child.status` updated optimistically post-success; K-09 owns the broader cache-invalidation contract.

## 15. Validation
None beyond what the backend enforces; confirmation modal is a UX safeguard, not a validation step.

## 16. Authentication
Parent session required.

## 17. Authorization
Step-up required before either action.

## 18. Error Handling
| Scenario | UI Behavior |
|---|---|
| Enable at capacity | Route to K-07 blocked state with upsell CTA |
| Network failure | Inline retry, card state unchanged until success |
| Step-up cancelled by user | Return to list, no action taken |

## 19. Offline First
Both actions blocked entirely while offline (mutating, requires connectivity, per §1.14).

## 20. Local Data
Optimistic `status` flip on success only; no optimistic update before server confirmation (given the safety-criticality of disable's session-revocation guarantee, do not flip the UI before the server confirms).

## 21. Localization
Confirmation copy, button labels, and the plan-capacity-blocked messaging all localized across EN/HI/AR/UR.

## 22. RTL
Modal layout and button order mirrored correctly under RTL.

## 23. Analytics
`child_disable_initiated`/`_completed`, `child_enable_initiated`/`_completed`/`_blocked_plan_capacity`.

## 24. Performance
Lightweight modal, no heavy computation; network round-trip is the dominant cost, within backend's stated performance targets.

## 25. Security
Step-up is mandatory and non-bypassable client-side (mirrors K-03's enforcement pattern) — this is a defense-in-depth UX control layered on top of the backend's own step-up enforcement, not a substitute for it.

## 26. Library Requirements
No new libraries.

## 27. Testing
- Integration test: full disable → re-enable cycle, verifying card state transitions correctly at each step (per PRD §13.2 Test Case #2).
- UI test: enable-blocked-by-capacity routes to K-07, not a generic error.
- UI test: step-up cancellation returns to the list with zero action taken.
- Unit: `disableChild()`/`enableChild()` repository wrappers correctly propagate error codes.

## 28. Documentation
Document in KDoc that these flows deliberately do not perform optimistic UI updates before server confirmation, given the safety-criticality of the underlying actions.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Repository Wrappers**
- **Objective:** `disableChild()`/`enableChild()` in `:core:data`.
- **Files to Modify:** `FamilyRepositoryImpl.kt`.
- **Tests:** Unit tests for both success and error-code propagation.
- **Definition of Done:** Both methods correctly surface `403 PLAN_CAPACITY_EXCEEDED` as a typed error the UI can distinguish from a generic failure.

**Task 02 — Confirmation Screens**
- **Objective:** Build both modal/screen components with step-up gating.
- **Files to Create:** `DisableConfirmationScreen.kt`, `ReEnableConfirmationScreen.kt`.
- **Implementation Details:** Step-up → confirm → call repository → update ViewModel state on success → navigate back to K-01's list.
- **Localization/RTL:** Verify all copy and layout.
- **Tests:** UI tests per §27.
- **Definition of Done:** Both flows independently tested end-to-end including the capacity-block routing case.

**Task 03 — Full-Cycle Integration Test**
- **Objective:** Verify the complete disable → re-enable cycle.
- **Definition of Done:** Test passes with correct card-state transitions at every step, matching the PRD's explicit happy-path test case.

## 30. Definition of Done
Both flows are step-up gated, correctly handle capacity blocking on enable, and never optimistically update state ahead of server confirmation.

## 31. Final Verification Checklist
- [ ] Full disable → re-enable cycle tested end-to-end
- [ ] Enable-blocked-by-capacity routes to K-07 correctly
- [ ] No optimistic UI update before server confirmation
- [ ] Step-up enforced on both flows
- [ ] Full localization and RTL verified
