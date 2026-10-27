# K-02 — Per-Child Action Menu & Disabled Card State

## 1. Feature Context
Part of Feature C.21 — Multi-Child Management. The interactive surface on each `ChildListCard` (K-01) that routes to every other per-child action in this feature.

## 2. Parent Feature
C.21 Multi-Child Management

## 3. Sub-feature
**K-02 — Per-Child Action Menu & Disabled Card State**

## 4. Objective
Present the correct set of actions per child based on status — full menu for active children, a deliberately restricted menu for disabled children — and route correctly to Edit, Disable/Enable, Delete, and the Per-Child Report.

## 5. Business Requirements
- §1.18 Screen Inventory #3: Per-Child Action Menu — Edit, Disable/Enable, Delete, view Report.
- §1.18 #14: Disabled Child Read-Only Card State — exit points: Re-Enable, view historical Report only.
- Android AI Prompt item 5: "Render disabled child cards with ONLY 'Enable' and 'View Report' actions... 'Edit' is absent; deletion of a disabled child IS permitted without requiring re-enable first."

## 6. Existing Architecture
Compose component within `:feature:child-management`, driven by `ChildManagementViewModel`'s per-card state (K-01).

## 7. Existing Code to Reuse
- `Navigator.navigateTo()` for routing to Report (C.22) and Child Locks & Sessions (C.23) routes — these are owned by other features; this component only triggers navigation, never implements those screens.
- Design-system overflow-menu/dropdown component from `:core:design-system`.

## 8. Files to Create
- `feature/child-management/src/commonMain/kotlin/.../components/PerChildActionMenu.kt`

## 9. Files to Modify
- `components/ChildListCard.kt` (K-01) — embed the action menu.

## 10. Backend Requirements
None directly — this is a pure client-side routing/rendering component; underlying actions call B-04/B-05/B-06 through their respective sub-features (K-04/K-05).

## 11. KMP Requirements
- Menu contents are a pure function of `ChildCardState.status`: `Active → [Edit, Disable, Delete, View Report]`; `Disabled → [Enable, Delete, View Report]` (Edit explicitly absent).
- Tapping Delete on a disabled child routes directly into K-05's warning flow — no re-enable gate.
- Tapping View Report routes to C.22 (Per-Child Reports) — cross-feature navigation via `Navigator`, out of scope to implement C.22 itself here.
- Tapping Child Locks & Sessions (where surfaced) routes to C.23 — same cross-feature boundary.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
None — no direct network calls from this component.

## 14. Database Requirements
None.

## 15. Validation
None.

## 16. Authentication
Inherits the parent session already established by the parent screen (K-01).

## 17. Authorization
No additional authorization at the menu-rendering level; the destination actions (K-04/K-05) each independently enforce step-up.

## 18. Error Handling
N/A — pure navigation/rendering component; destination screens own their own error handling.

## 19. Offline First
Menu renders regardless of connectivity; destination mutating actions (K-04/K-05) independently block themselves offline.

## 20. Local Data
None.

## 21. Localization
Menu item labels ("Edit", "Disable", "Enable", "Delete", "View Report") sourced from the localization dictionary.

## 22. RTL
Overflow menu anchors and opens correctly mirrored under RTL.

## 23. Analytics
None directly fired by the menu itself; destination screens fire their own `_initiated` events on selection.

## 24. Performance
Menu-item list is a pure derivation from `status` — no additional state or recomposition cost beyond the parent card's existing re-render.

## 25. Security
No security surface — the menu only routes; it cannot bypass step-up since every destination independently enforces it.

## 26. Library Requirements
No new libraries.

## 27. Testing
- UI test: active child's menu shows exactly `[Edit, Disable, Delete, View Report]`.
- UI test: disabled child's menu shows exactly `[Enable, Delete, View Report]` — explicit assertion that "Edit" is absent.
- UI test: tapping Delete on a disabled child routes directly to K-05 without an intermediate re-enable prompt.
- UI test: RTL menu anchoring.

## 28. Documentation
KDoc on the menu-item-derivation function documenting the status → action-set mapping explicitly, since this is a documented, tested business rule (not incidental UI behavior).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Action-Set Derivation Function**
- **Objective:** Pure function mapping `ChildStatus → List<ChildAction>`.
- **Files to Create:** within `PerChildActionMenu.kt`.
- **Business Rules:** Active → Edit/Disable/Delete/Report; Disabled → Enable/Delete/Report (no Edit).
- **Tests:** Unit test covering both statuses exhaustively (use a `when` expression with no `else` branch so a future third status forces a compile error, not a silent gap).
- **Definition of Done:** Function is exhaustive and independently unit-tested.

**Task 02 — Compose Menu Component**
- **Objective:** Render the derived action set with correct routing per item.
- **Files to Create:** `PerChildActionMenu.kt`.
- **Implementation Details:** Each menu item's `onClick` triggers the appropriate `Navigator.navigateTo()` call or invokes the appropriate ViewModel action (for Disable/Enable/Delete, which route into step-up-gated flows owned by K-04/K-05).
- **Localization/RTL:** Verify menu anchor and text direction under RTL locales.
- **Tests:** UI tests per §27.
- **Definition of Done:** Both status variants render and route correctly, verified by tests.

## 30. Definition of Done
Action-set-per-status rule is exhaustively enforced and tested; all routes correctly reach their owning feature/screen.

## 31. Final Verification Checklist
- [ ] Active-child menu exactly matches spec
- [ ] Disabled-child menu exactly matches spec (Edit absent, confirmed by test)
- [ ] Delete reachable directly from a disabled card without re-enable
- [ ] RTL menu anchoring verified
- [ ] No hardcoded strings
