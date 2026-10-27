# K-01 — Who Is Learning Profile Picker

## 1. Feature Context
The landing surface every returning session lands on: child tiles + Parent Profile tile + Add Child tile. **This screen already exists** as `ProfilePickerScreen` (A.1 K-08), built against `FamilyRepository.observeChildren()` and `core-ui`'s `ProfilePickerTile`. This sub-feature does not rebuild it — it hardens it against C.19's canonical, zero-exception rules (server-driven disabled-status filtering, exact tile-to-pipeline-stage routing) and is the reference point every other C.19/B.16 sub-feature routes through.

## 2. Parent Feature
Feature C.19 — Parent PIN/Biometric Gate & Profile Access Control

## 3. Sub-feature
2.1 Who Is Learning Profile Picker (ID: **K-01**)

## 4. Objective
Harden the existing `ProfilePickerScreen` (A.1 K-08) so its tile list is rendered exclusively from the server's active-children response (no client-side disabled-status filtering logic, structurally), and its tap-routing exactly matches C.19's four-stage pipeline (direct-to-restrictions for unlocked children, K-02's lock screen for locked children, K-03's Parent Gate for the Parent Profile tile).

## 5. Business Requirements
- FR-1: landing picker shows active child tiles + Parent Profile tile + Add Child tile; disabled children appear **only** inside Parent Profile, never here.
- FR-2: Parent Profile tile always requires PIN/biometric — zero exceptions.
- FR-3: child tile with no lock proceeds directly to restriction checks (K-05); with a lock, routes to K-02.
- Empty State (§1.12): zero children → Parent Profile tile + Add Child tile only, no error framing (already covered by K-08 for the post-deletion case; confirm it also covers the "brand-new family, zero children yet" case identically).

## 6. Existing Architecture
`feature/onboarding/ui/ProfilePickerScreen.kt` + `ProfilePickerViewModel.kt` (A.1 K-08), backed by `core-data`'s `FamilyRepository.observeChildren()` and `core-ui`'s `ProfilePickerTile`. **Architecture note:** C.19's own PRD (§6-7) specifies this canonical gate should live in a shared `:core:auth` module rather than `feature/onboarding`; before making changes, confirm against the KMP Core Architecture doc whether `feature/onboarding` is already treated as shared/reusable across features (as B.16 K-04 and B.16 K-08's own doc imply by calling into it from outside onboarding) or whether a genuine module relocation is warranted. If a relocation is warranted, treat it as a scoped Architecture Improvement (existing→problem→proposal→impact→implementation) rather than a silent rewrite — do not duplicate the screen into a second module.

## 7. Existing Code to Reuse
- `feature/onboarding/ui/ProfilePickerScreen.kt`, `ProfilePickerViewModel.kt` (A.1 K-08 — extend, do not recreate)
- `core-data/FamilyRepository.observeChildren()` (existing reactive `Flow<List<Child>>`)
- `core-ui/ProfilePickerTile` (existing component)
- `core-navigation/Route.kt::ProfilePickerRoute` (existing)

## 8. Files to Create
- `test/feature/onboarding/ProfilePickerServerFilteringTest.kt` — structural test asserting no disabled-status filtering exists client-side

## 9. Files to Modify
- `feature/onboarding/ui/ProfilePickerScreen.kt` — confirm/remove any client-side disabled-status filter; render exactly what `FamilyRepository.observeChildren()` returns
- `feature/onboarding/viewmodel/ProfilePickerViewModel.kt` — confirm tap-routing exactly matches: no-lock → restriction check (K-05's session-activation call), locked → `ChildLockRoute` (K-02), Parent Profile → `ParentGateRoute` (K-03)

## 10. KMP Requirements
- Tile list source of truth is exclusively the server response (B-01's reused `GET /v1/family/children`, A.1) — the client renders, it does not decide, which children are "active."
- Parent Profile tile tap → **always** navigates to K-03's Parent Gate, with no conditional skip under any circumstance (mirrors B.16 K-04's zero-exception requirement, but this is the tile that originates it).
- Add Child tile is gated behind K-03's Parent Gate (per FR-1) before reaching A.1's Add Child flow.
- Accessibility: each tile's content description includes lock status ("Ahmed, locked" / "Ahmed, no lock").
- Grid reflows for tablet without shrinking tap targets below 44dp.

## 11. Required API
`GET /v1/family/children` (reused from A.1) — no new endpoint; this sub-feature is a consumer only.

## 12. Offline First
Renders from `FamilyRepository`'s locally cached data when offline (existing `core-data` capability); no new offline handling required here.

## 13. Local Data
Consumes existing `core-data` cache; no new local persistence introduced by this sub-feature.

## 14. Localization
Tile labels, "Add Child," and Parent Profile label fully localized EN/HI/AR/UR (already covered by K-08; confirm coverage).

## 15. RTL
Grid and tile icon placement (lock overlay, parent silhouette badge) mirror correctly in RTL (already covered by K-08; confirm coverage).

## 16. Analytics
`who_is_learning_viewed` (on screen composition), `profile_tile_selected` (on any tile tap, with tile type as parameter).

## 17. Performance
Avoid unnecessary recomposition on tile grid when unrelated state changes elsewhere in the ViewModel; use stable/immutable data classes for tile list state.

## 18. Security
No lock-bypass logic may exist in this screen's routing — the structural test (§19) asserts the Parent Profile tile has exactly one destination (`ParentGateRoute`) in the navigation graph.

## 19. Testing
- Unit: tile list renders exactly the server response, with a test proving no local filter predicate exists (structural/code-search-style assertion or a fixture with a disabled child forced into the response, verifying it renders — since filtering must happen server-side only).
- UI: Parent Profile tile always navigates to `ParentGateRoute`.
- UI: empty state (zero children) renders Parent Profile + Add Child only.
- Integration: locked child tile → `ChildLockRoute`; unlocked child tile → direct restriction-check call (K-05).

## 20. AI Coding Agent Implementation Steps

**Task 01 — Audit Existing `ProfilePickerViewModel` for Client-Side Filtering**
Objective: confirm whether any disabled-status filter exists client-side; remove if present. Files to Modify: `ProfilePickerViewModel.kt`. Definition of Done: tile list is a direct map of the server response.

**Task 02 — Confirm/Harden Tap-Routing Table**
Objective: verify the three routing branches (no-lock, locked, Parent Profile) exactly match C.19 FR-1–FR-3. Files to Modify: `ProfilePickerScreen.kt`/`ProfilePickerViewModel.kt`. Dependencies: Task 01.

**Task 03 — Add Structural No-Client-Filter Test**
Objective: prove the invariant in code, not just by inspection. Files to Create: `ProfilePickerServerFilteringTest.kt`. Dependencies: Task 01.

**Task 04 — Add/Confirm Accessibility Content Descriptions**
Objective: lock status included per tile. Files to Modify: `ProfilePickerScreen.kt`. Dependencies: none.

**Task 05 — Add Analytics Instrumentation**
Objective: `who_is_learning_viewed`, `profile_tile_selected`. Dependencies: Task 02.

**Task 06 — Final Code Review**
Objective: confirm zero client-side filtering and zero-exception Parent Profile routing hold under every code path. Definition of Done: checklist in §21 checked.

## 21. Final Verification Checklist
- [x] No client-side disabled-status filtering logic exists anywhere in `ProfilePickerViewModel`
- [x] Parent Profile tile has exactly one navigation destination: `ParentGateRoute`
- [x] Empty state renders correctly for both "zero children ever" and "all children disabled" cases
- [x] Tile accessibility descriptions include lock status
- [x] RTL grid reflow verified

## 22. Definition of Done
`ProfilePickerScreen` (A.1 K-08, hardened here) renders exclusively from the server's active-children response, routes every tile through the correct C.19 pipeline stage with zero exceptions for Parent Profile, and is covered by a structural test proving no client-side filtering exists.

## 23. Verification & Compliance Record
- **Implementation Status**: COMPLETED (100% compliant with C.19 FR-1–FR-3 & visual assets)
- **Visual Design Matching**:
  - `Screens/Mobile App/Parent Area/Who is Learning_-01.png` (Default state)
  - `Screens/Mobile App/Parent Area/Who is Learning_-02.png` (Scrolled state with Add Child & Educational Banner)
  - `Screens/Mobile App/Parent Area/Who is Learning_-03.png` (Loading state with 4 shimmer skeleton cards)
  - `Screens/Mobile App/Parent Area/Who is Learning_-04.png` (Offline state with cached warning banner)
  - `Screens/Mobile App/Onboarding/Profiles.png` (Profiles variant with progress indicators and active card dot)
- **Unit & Structural Tests**:
  - `ProfilePickerServerFilteringTest.kt`: Validates zero client-side disabled filtering, zero-bypass Parent Gate, Add Child gate, lock routing, empty state, and analytics.
  - `ProfilePickerViewModelTest.kt`: Validates server mapping, retry, error states, and event dispatch.
- **Test Execution Result**:
  - `:feature:feature-onboarding:allTests` -> SUCCESS (0 failures)
  - `:shared:allTests` -> SUCCESS (0 failures)
