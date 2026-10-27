# Blueprint: Child Switcher Component

## 1. Feature Context
Platform: NoorHeroes KMP App. Module `:feature:parent-dashboard`. Builds on K-01's screen/ViewModel shell.

## 2. Parent Feature
C.20 — Parent Dashboard.

## 3. Sub-feature
K-02 — Child Switcher Component.

## 4. Objective
Render the avatar+name chip row (including archived/disabled children in a visually distinguished state), and switch the Dashboard's active child context on tap, triggering K-01's per-component re-fetch.

## 5. Business Requirements
Source: PRD §1.7 FR-1, FR-2, §1.10 Edge Cases #2, #3, §1.18 row 2 & 8, §2.2, §2.3.
- Chip row: avatar + name per child, including archived/disabled in visually distinguished style.
- Disabled child selectable for read-only viewing; no live-session actions offered.
- Archived (post-downgrade) profiles clearly distinguished from active, not mixed indistinguishably.
- Tap → refresh Dashboard for selected child; fires `dashboard_child_switched`.

## 6. Existing Architecture
Builds on K-01's `ParentDashboardViewModel`/`DashboardUiState`. Uses `FamilyRepository` (core-common interface, per `CORE_COMMON_INSTRUCTIONS.md` §4.6) as the source of the child list itself (distinct from per-child dashboard data, which comes from `DashboardRepository`). `ChildProfile` model (`core-common`) already has `syncState`/`ageBand` fields per §7 of that doc — confirm whether it also carries a `status` (active/disabled/archived) field before assuming its shape; if not present, this blueprint must add it via `FamilyRepository`'s existing extension points rather than inventing a parallel model.

## 7. Existing Code to Reuse
- `ChildProfile` model (`core-common`).
- `FamilyRepository` (`core-common` interface) for the child list itself.
- K-01's `ParentDashboardViewModel` — extend with `onChildSelected(childId: String)` method.
- `:core:design-system` chip/avatar components (confirm exact names before use).

## 8. Files to Create
- `feature/parent-dashboard/src/commonMain/kotlin/.../ChildSwitcherChips.kt` (Composable)
- `feature/parent-dashboard/src/commonTest/kotlin/.../ChildSwitcherStateTest.kt`

## 9. Files to Modify
- `ParentDashboardViewModel.kt` — add `childList: StateFlow<List<ChildSwitcherItem>>`, `onChildSelected(childId)`
- `DashboardUiState.kt` — add `selectedChildId`, `childList` (with `ChildSwitcherItem(childId, name, avatarUrl, status: ACTIVE|DISABLED|ARCHIVED)`)

## 10. KMP Requirements
- `ChildSwitcherChips` Composable: horizontal scrollable row, one chip per `ChildSwitcherItem`, highlighted state for `selectedChildId`, visually distinguished style (e.g., reduced opacity + label badge) for `DISABLED`/`ARCHIVED` status.
- Tap handler calls `viewModel.onChildSelected(childId)`, which updates `selectedChildId` and triggers K-01's independent re-fetch of all 4 dashboard component slices scoped to the new child.
- Selecting a `DISABLED`/`ARCHIVED` child sets a `isReadOnly: true` flag on the resulting `DashboardUiState`, which downstream components (K-03–K-06) must respect by hiding/disabling any live-action affordances.
- Fire `dashboard_child_switched` analytics event on successful switch.

## 11. Files/Screens
Composable only; no new screen (lives within K-01's `ParentDashboardScreen`).

## 12. NextJS Requirements
N/A.

## 13. API Contract
Triggers `DashboardRepository.getDashboard(childId)` (B-02) via K-01's ViewModel — no new API of its own; the child list itself is sourced from the existing `FamilyRepository`/child-listing API (owned by C.21, not duplicated here per PRD FR-14).

## 14. Database Requirements
N/A new — reads `FamilyRepository`'s existing local cache/child list.

## 15. Validation
`onChildSelected` must reject a `childId` not present in `childList` (defensive check against a malformed deep link or stale UI state).

## 16. Authentication
Inherits K-01's Parent Gate requirement.

## 17. Authorization
Child list itself is already scoped to the authenticated family via `FamilyRepository`; no additional check needed here beyond K-01's family-derivation guarantee.

## 18. Error Handling
If `FamilyRepository`'s child list fetch fails, the chip row shows its own independent error/retry affordance (consistent with K-01's per-component independence principle) without blocking the rest of the Dashboard.

## 19. Offline First
Child list rendered from `FamilyRepository`'s existing offline-cache behavior (already governed by that repository, not re-implemented here).

## 20. Local Data
N/A new — reuses `FamilyRepository`'s existing Room-backed cache.

## 21. Localization
Status labels ("Archived", "Disabled") sourced from localization package, not hardcoded.

## 22. RTL
Chip row must reverse direction correctly in RTL; avatar+label internal alignment mirrors.

## 23. Analytics
`dashboard_child_switched` (PRD §1.19) — fired with the newly selected `childId`'s status (active/disabled/archived) as a parameter if the analytics schema supports it (confirm against `CORE_ANALYTICS_INSTRUCTIONS.md` before adding new parameters).

## 24. Performance
Chip row is one of the fastest-loading components (PRD §1.13: "child switcher chips load fast/first") — avoid blocking it on the same fetch as the slower weekly-report/timeline data; it should hydrate from `FamilyRepository`'s cache independently and immediately.

## 25. Security
Read-only enforcement for disabled/archived children is a UI-layer courtesy; the actual authoritative enforcement of "no live actions for disabled children" lives in each downstream module's own backend (C.21 etc.) — this component must not be the sole gate.

## 26. Library Requirements
No new dependencies.

## 27. Testing
1. Unit test: selecting a child updates `selectedChildId` and triggers re-fetch.
2. Unit test: selecting a disabled/archived child sets `isReadOnly: true`.
3. Unit test: chips render active/disabled/archived states with distinct visual treatment (UI test / snapshot).
4. Unit test: `onChildSelected` rejects an unknown `childId`.
5. UI test: chip row loads independently of slower components (no shared loading gate).

## 28. Documentation
KDoc on `ChildSwitcherChips` and the new `ViewModel` methods, citing PRD §1.18 rows 2 & 8.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Extend DashboardUiState and ViewModel**
- Task ID: K02-T01
- Objective: Add child-list/selection state and switching logic.
- Why This Is Required: Core mechanism of this sub-feature.
- Existing Architecture to Follow: K-01's `DashboardUiState`/`ParentDashboardViewModel`.
- Existing Files to Reuse: `FamilyRepository`, `ChildProfile`.
- Files to Create: none.
- Files to Modify: `DashboardUiState.kt`, `ParentDashboardViewModel.kt`.
- Implementation Details: Per §10.
- Business Rules: FR-1, FR-2, Edge Cases #2, #3.
- Validation: Reject unknown `childId`.
- Error Handling: Independent chip-row error state.
- Security: N/A.
- Performance: Fast/first-loading via independent cache hydration.
- Localization: N/A (state only).
- RTL: N/A.
- Analytics: `dashboard_child_switched` event trigger point.
- Tests: Covered in Task 03.
- Documentation: KDoc.
- Dependencies: K-01.
- Do Not Change: Do not alter other components' state slices.
- Expected Result: ViewModel supports child switching.
- Definition of Done: Matches §10.

**Task 02 — Build ChildSwitcherChips Composable**
- Task ID: K02-T02
- Objective: Visual chip row.
- Why This Is Required: UI delivery.
- Existing Architecture to Follow: `:core:design-system` chip/avatar primitives, C.19 formal visual register.
- Existing Files to Reuse: Design-system components (confirm names).
- Files to Create: `ChildSwitcherChips.kt`.
- Files to Modify: `ParentDashboardScreen.kt` (slot it in).
- Implementation Details: Per §10; distinguished styling for disabled/archived.
- Business Rules: PRD §2.2.
- Validation: N/A.
- Error Handling: Independent error/retry.
- Security: N/A.
- Performance: Avoid unnecessary recomposition (stable `ChildSwitcherItem` list).
- Localization: Status labels localized.
- RTL: Mirrors correctly.
- Analytics: N/A (fired from ViewModel callback).
- Tests: Covered in Task 03.
- Documentation: KDoc.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Chips render and are tappable.
- Definition of Done: Matches PRD §2.2 component description.

**Task 03 — Write Test Suite**
- Task ID: K02-T03
- Objective: Cover §27.
- Why This Is Required: QA coverage.
- Existing Architecture to Follow: Existing Compose/Kotlin test conventions.
- Existing Files to Reuse: Fake `FamilyRepository`/`DashboardRepository` test doubles.
- Files to Create: `ChildSwitcherStateTest.kt`.
- Files to Modify: none.
- Implementation Details: 5 cases per §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: N/A.
- Security: N/A.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test KDoc.
- Dependencies: Tasks 01–02.
- Do Not Change: N/A.
- Expected Result: All pass.
- Definition of Done: 100% of §27 green.

## 30. Definition of Done
Chip row renders all children including distinguished archived/disabled states, switching triggers correct re-fetch and read-only flagging, analytics fires, all tests green.

## 31. Final Verification Checklist
- [ ] Archived/disabled visually distinguished, not mixed indistinguishably
- [ ] Switching re-fetches all 4 dashboard components for new child
- [ ] Chip row loads independently/fast per PRD §1.13
- [ ] `dashboard_child_switched` fires correctly
- [ ] RTL verified
