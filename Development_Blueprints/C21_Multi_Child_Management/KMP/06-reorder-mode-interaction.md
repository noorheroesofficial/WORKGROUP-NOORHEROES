# K-06 — Reorder Mode Interaction

## 1. Feature Context
Part of Feature C.21 — Multi-Child Management. A low-risk convenience interaction letting a parent reorder how children appear across the app.

## 2. Parent Feature
C.21 Multi-Child Management

## 3. Sub-feature
**K-06 — Reorder Mode Interaction**

## 4. Objective
Let a parent enter a reorder mode, rearrange children via drag-handles or up/down controls, and persist the new order as a single atomic save, independent of any other in-flight action elsewhere in the app.

## 5. Business Requirements
- §2.1: Reorder Mode — simple drag-handles or up/down arrow controls per row.
- §1.18 #13: Reorder Mode — entry "Reorder" action, exit "Saves new order."
- Edge Case #4: reorder while another child is mid-deletion-confirmation elsewhere → independent, non-blocking.

## 6. Existing Architecture
Local, in-memory reorder state within `ChildManagementViewModel`, committed via a single batch call to `:core:data` on confirm.

## 7. Existing Code to Reuse
- `FamilyRepository.reorderChildren(orderedChildIds)` — new thin wrapper over B-07.
- Design-system drag-handle/reorderable-list primitive from `:core:design-system` if one exists; otherwise implement with Compose's standard drag-gesture APIs, kept local to this component.

## 8. Files to Create
- `feature/child-management/src/commonMain/kotlin/.../ReorderModeScreen.kt`

## 9. Files to Modify
- `core-data/.../FamilyRepositoryImpl.kt` — add `reorderChildren(orderedChildIds: List<String>)`.
- `ChildManagementViewModel.kt` — add local reorder-draft state, separate from the committed list state.

## 10. Backend Requirements
Consumes B-07 exclusively.

## 11. KMP Requirements
- Reorder mode maintains its own local draft list, decoupled from `ChildManagementUiState.Content.children`, so an in-progress drag never affects the main list's rendering elsewhere.
- On "confirm," submit the complete draft-ordered ID list in one call; on success, replace the committed state; on failure, revert the draft to the last known committed order and show a retry affordance.
- Reorder mode is entirely independent state — entering/exiting it must not interfere with, or be interfered by, any other per-child action (e.g., a deletion flow for a different child proceeding concurrently), satisfying Edge Case #4.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
Consumes B-07's contract as documented in that blueprint.

## 14. Database Requirements
Local Room `displayOrder` column updated only after server confirmation of the batch save (mirrors K-05's "never optimistic before server confirms" principle, applied here for consistency rather than because reorder itself is high-risk).

## 15. Validation
None client-side beyond ensuring the draft list always contains every currently-known child exactly once (a client-side sanity check mirroring B-07's server-side set-equality validation).

## 16. Authentication
Parent session required.

## 17. Authorization
Step-up required before the commit call (reorder is a mutating action per FR-11's blanket rule).

## 18. Error Handling
| Scenario | UI Behavior |
|---|---|
| Save fails (network/validation) | Revert draft to last committed order, show retry |
| Step-up cancelled | Exit reorder mode, no change persisted |

## 19. Offline First
Reorder mode is browsable offline (pure local UI state), but the final commit is blocked until connectivity is available, consistent with all other mutating actions in this feature.

## 20. Local Data
Draft state is ephemeral (ViewModel-scoped, not persisted to Room until server confirms).

## 21. Localization
"Reorder" entry-point label and any instructional copy localized across EN/HI/AR/UR.

## 22. RTL
Drag direction and up/down control semantics correctly adapted for RTL locales — "up" remains vertically up, but any horizontal drag affordance (if used) mirrors direction.

## 23. Analytics
`child_reorder_completed` on successful commit only (not fired for an abandoned reorder session).

## 24. Performance
Local list reordering must not trigger full-list recomposition on every drag frame — use stable keys per item and minimal-diff list updates.

## 25. Security
Step-up required on commit, consistent with the feature's blanket mutating-action rule; no elevated risk beyond that (reordering carries no data-loss or access-control implications).

## 26. Library Requirements
No new libraries — implemented with Compose's existing gesture/animation APIs.

## 27. Testing
- Unit: draft-list local-state management (add/move/no-duplicate-loss under repeated drags).
- UI test: reorder mode entry/exit does not affect the main list's unrelated card states.
- Integration test: reorder proceeding concurrently with a deletion flow on a different child — both complete independently without interference (Edge Case #4).
- UI test: failed save reverts to the last committed order.

## 28. Documentation
KDoc documenting that draft state is intentionally decoupled from committed state, and why (to satisfy Edge Case #4's independence requirement).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Repository Wrapper**
- **Objective:** `reorderChildren(orderedChildIds)` in `:core:data`.
- **Files to Modify:** `FamilyRepositoryImpl.kt`.
- **Tests:** Unit test for the request payload shape and error-code propagation (`422` set-mismatch).
- **Definition of Done:** Wrapper correctly surfaces B-07's validation error as a typed, UI-distinguishable error.

**Task 02 — Local Draft State Management**
- **Objective:** Implement decoupled draft-list state in the ViewModel.
- **Files to Modify:** `ChildManagementViewModel.kt`.
- **Implementation Details:** `draftOrder: List<String>` initialized from the committed list on reorder-mode entry; mutated locally on each drag/move; discarded (not committed) on cancel.
- **Tests:** Unit tests for draft mutation correctness.
- **Definition of Done:** Draft state never corrupts or is corrupted by the committed list state.

**Task 03 — Reorder Mode UI**
- **Objective:** Build the drag-handle/up-down-control UI.
- **Files to Create:** `ReorderModeScreen.kt`.
- **Performance:** Stable item keys, minimal recomposition per drag frame.
- **Localization/RTL:** Verify per §21/§22.
- **Tests:** UI tests per §27.
- **Definition of Done:** Smooth, performant reorder interaction verified across locales and layout directions.

## 30. Definition of Done
Reorder mode is fully independent of other concurrent actions, correctly commits atomically, and reverts cleanly on failure.

## 31. Final Verification Checklist
- [ ] Draft state decoupled from committed list state (tested)
- [ ] Concurrent independence from other per-child actions verified (Edge Case #4)
- [ ] Failed save reverts correctly
- [ ] Step-up enforced on commit
- [ ] Full localization and RTL verified
- [ ] `child_reorder_completed` fires only on successful commit
