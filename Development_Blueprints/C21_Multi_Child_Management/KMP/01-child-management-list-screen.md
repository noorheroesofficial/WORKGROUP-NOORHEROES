# K-01 — Child Management List Screen

## 1. Feature Context
Part of Feature C.21 — Multi-Child Management. The primary entry surface reached from the Parent Dashboard (C.20), and the screen every other C.21 KMP sub-feature returns to.

## 2. Parent Feature
C.21 Multi-Child Management

## 3. Sub-feature
**K-01 — Child Management List Screen**

## 4. Objective
Render a trustworthy, accessible overview of every child in the family — active and disabled — with correct loading/empty/offline/capacity states, at the performance and stability bar the rest of the KMP app holds itself to.

## 5. Business Requirements
- §2.2 Screen: Child Management (List) — components, states (Default, Loading, Empty, Offline, Plan-capacity-at-limit), accessibility (status announced, not color-only), responsive rules (single-column mobile, 2-column tablet).
- §1.12 Empty State: zero children → only "+ Add Child" with a friendly prompt.
- §1.13 Loading State: skeleton card-list shimmer.
- §1.14 Offline State: list renders read-only from cache.
- Success Metric: Child Management view rate ≥ 50% (monthly, multi-child families); Crash-free sessions ≥ 99.6%.

## 6. Existing Architecture
Module `:feature:child-management` (Kotlin, Jetpack Compose, MVVM, Clean Architecture), depends on `:core:auth`, `:core:design-system`, `:core:network`, `:core:data`, `:core:navigation`, per the established KMP layering (`Feature Layer → Domain (optional UseCases) → core-data → core-network/core-database`).

## 7. Existing Code to Reuse
- `FamilyRepository` (extend or introduce `observeChildren()` in `:core:data`, following the `ContentRepository`/`Flow<List<Content>>` pattern documented in `CORE_DATA_INSTRUCTIONS.md` §10 Quick Reference: `FamilyRepository | Child Profiles | Flow<List<Child>> | Parent Dashboard`).
- `Navigator` / `Route` (`core-navigation`) — define `ChildManagementRoute: Route` per the existing sealed-interface pattern.
- Design-system card, skeleton-shimmer, and empty-state components from `:core:design-system` (per `CORE_DESIGNSYSTEM_INSTRUCTIONS.md` — reuse existing primitives, do not fork new ones for this screen).
- `NoorHeroesLogger` for error logging (per `CORE_DATA_INSTRUCTIONS.md` §5: "DO NOT swallow errors silently").

## 8. Files to Create
- `feature/child-management/src/commonMain/kotlin/.../ChildManagementListScreen.kt`
- `feature/child-management/src/commonMain/kotlin/.../ChildManagementViewModel.kt`
- `feature/child-management/src/commonMain/kotlin/.../ChildManagementUiState.kt`
- `feature/child-management/src/commonMain/kotlin/.../components/ChildListCard.kt`
- `feature/child-management/src/commonMain/kotlin/.../ChildManagementAnalytics.kt`
- `feature/child-management/src/commonMain/kotlin/.../di/ChildManagementModule.kt` (Koin)

## 9. Files to Modify
- `core-data/.../di/RepositoryModule.kt` — register `FamilyRepository.observeChildren()`/`refreshChildren()` if not already present from A.1.
- `core-navigation/.../Route.kt` — add `ChildManagementRoute`.
- `:feature:parent-dashboard` navigation graph — wire the module-shortcut entry point to `ChildManagementRoute`.

## 10. Backend Requirements
Consumes B-01 (`GET /v1/family/children`) exclusively for this screen's data.

## 11. KMP Requirements
- `ChildManagementViewModel` derives family context internally from `:core:auth` (no explicit family ID passed via navigation args, per the existing pattern seen in C.20's `ParentDashboardRoute`).
- State model: `ChildManagementUiState` as an immutable, stable `data class` (Compose stability) with sealed sub-states `Loading | Content(children: List<ChildCardState>) | Empty | Error`.
- Offline: initial render from `observeChildren()`'s local-cache emission; `refreshChildren()` called on screen entry to reconcile with B-01.
- Plan-capacity-at-limit is derived client-side by comparing the returned list's active count against the entitlement snapshot already cached by `:core:data` (per `CORE_DATA_INSTRUCTIONS.md`'s "Entitlement Service (reused, C.24)" — do not call a separate entitlement endpoint from this screen if the snapshot is already available).

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
Consumes B-01's contract as documented in that blueprint; no independent contract here.

## 14. Database Requirements
Local Room cache table for `Child` entities — reuse the entity already established for A.1's onboarding Add Child flow if present; extend with `status`, `displayOrder`, `dobLockedAt` columns to match B-01's response shape (coordinate with K-09, which owns the sync/caching implementation in depth).

## 15. Validation
None — read-only screen.

## 16. Authentication
Screen is only reachable once a parent session exists (enforced by `:core:auth` + navigation guard via `Route.requiredAuthState`).

## 17. Authorization
No additional authorization beyond standard parent session — this screen does not require step-up (matches B-01's non-step-up read contract).

## 18. Error Handling
| Scenario | UI Behavior |
|---|---|
| Network failure on refresh, cache available | Render cached list, show a subtle non-blocking error/retry affordance |
| Network failure, no cache (first load) | Error state with retry |
| Empty family | Empty state, "+ Add Child" only |

## 19. Offline First
Initial load always from local cache (`observeChildren()` Flow); `refreshChildren()` reconciles in the background. Per `CORE_DATA_INSTRUCTIONS.md` §8: "Observe data via a repository Flow... Call refresh()... UI reacts automatically via the Flow."

## 20. Local Data
Room-backed `Child` entity, one row per child, keyed by `childId`, `familyId` foreign reference.

## 21. Localization
All UI strings (status labels "Active"/"Disabled", empty-state copy, "+ Add Child", "Reorder") sourced from the shared localization dictionary — no hardcoded English strings. Support EN/HI/AR/UR.

## 22. RTL
Full RTL mirroring for Arabic/Urdu: card layout, status-pill position, overflow-menu anchor, single-column/2-column grid direction.

## 23. Analytics
`child_management_viewed` fired once per successful screen load (not per recomposition — guard with a `LaunchedEffect(Unit)` or ViewModel-level one-shot flag).

## 24. Performance
- Immutable/stable `ChildManagementUiState` to prevent unnecessary recomposition of unrelated cards when one card's state changes.
- `LazyColumn` (or platform equivalent) for the card list to avoid unbounded composition cost, though family sizes are small (≤ ~10).
- Avoid main-thread blocking during Room reads (already `suspend`/`Flow`-based by convention).

## 25. Security
No sensitive data rendered beyond what the parent already owns; no new permission surface.

## 26. Library Requirements
No new libraries — Compose, Koin, Room, Ktor already established per the core architecture docs.

## 27. Testing
- Unit: `ChildManagementViewModel` state derivation (Loading → Content/Empty/Error transitions).
- Unit: plan-capacity-at-limit derivation logic.
- UI: skeleton shimmer renders during initial load.
- UI: empty state renders correctly with zero children.
- UI: disabled cards render desaturated + status pill (cross-reference K-02 for full disabled-card behavior).
- UI: offline banner/indicator appears when `ConnectivityObserver` reports offline.

## 28. Documentation
Add a KDoc header to `ChildManagementViewModel` documenting its state-derivation contract and its dependency on `FamilyRepository.observeChildren()`.

## 29. AI Coding Agent Implementation Steps

**Task 01 — `FamilyRepository.observeChildren()`/`refreshChildren()`**
- **Objective:** Provide the offline-first data source this screen consumes.
- **Files to Modify:** `core-data/.../repository/FamilyRepositoryImpl.kt` (create if absent).
- **Implementation Details:** `observeChildren(): Flow<List<Child>>` reads Room; `suspend fun refreshChildren(): NoorResult<Unit>` calls B-01 via `:core:network`, upserts into Room.
- **Dependencies:** `:core:network`, `:core:database`.
- **Tests:** Repository unit test with a fake network layer confirming Room is updated post-refresh.
- **Definition of Done:** Flow emits cached data immediately, then updated data post-refresh, matching the offline-first contract.

**Task 02 — `ChildManagementUiState` & ViewModel**
- **Objective:** Build the immutable state model and its derivation logic.
- **Files to Create:** `ChildManagementUiState.kt`, `ChildManagementViewModel.kt`.
- **Implementation Details:** Collect `observeChildren()` in `viewModelScope`, map to sealed states, derive plan-capacity-at-limit from the cached entitlement snapshot.
- **Performance:** Ensure `data class` immutability for Compose stability.
- **Tests:** State-derivation unit tests for all four sealed states.
- **Definition of Done:** ViewModel is fully unit-testable without a running UI.

**Task 03 — Compose Screen & Card Component**
- **Objective:** Build `ChildManagementListScreen` and `ChildListCard`.
- **Files to Create:** `ChildManagementListScreen.kt`, `components/ChildListCard.kt`.
- **Implementation Details:** Skeleton shimmer, empty state, offline indicator, responsive single/2-column layout, RTL-aware layout via `LocalLayoutDirection`.
- **Localization/RTL:** All strings via the shared localization API; layout mirrors correctly under RTL.
- **Tests:** UI tests per §27.
- **Definition of Done:** Screen renders correctly across all states, locales, and layout directions.

**Task 04 — Navigation & Analytics Wiring**
- **Objective:** Register the route and fire the one-shot analytics event.
- **Files to Modify:** `core-navigation/.../Route.kt`, `:feature:parent-dashboard` nav graph.
- **Files to Create:** `ChildManagementAnalytics.kt`.
- **Definition of Done:** Screen reachable from the Dashboard shortcut; `child_management_viewed` fires exactly once per successful load.

## 30. Definition of Done
Screen renders all required states correctly, is offline-first, fully localized/RTL, stable/performant under Compose, and analytics-instrumented.

## 31. Final Verification Checklist
- [ ] Offline-first Flow-based data loading verified
- [ ] All states (Loading/Empty/Error/Offline/Capacity-at-limit) covered by tests
- [ ] Immutable/stable state model confirmed (no unnecessary recomposition)
- [ ] Full localization (EN/HI/AR/UR) and RTL verified
- [ ] Accessibility: status announced beyond color alone
- [ ] `child_management_viewed` fires exactly once per load
- [ ] No hardcoded strings
