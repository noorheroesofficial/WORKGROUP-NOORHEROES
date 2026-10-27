# Blueprint: Module Shortcut Grid & Navigation

## 1. Feature Context
Platform: NoorHeroes KMP App. Module `:feature:parent-dashboard`. The Dashboard's primary navigation hub into every other Parent Area module.

## 2. Parent Feature
C.20 — Parent Dashboard.

## 3. Sub-feature
K-06 — Module Shortcut Grid & Navigation.

## 4. Objective
Render the 5-icon module shortcut grid (Child Management, Reports, Settings, Subscription, Support), navigate correctly to each destination module, and return to the Dashboard instantly from cache on back-navigation.

## 5. Business Requirements
Source: PRD §1.7 FR-1, FR-2, FR-4, FR-14, §1.10 Edge Case #7, §1.18 row 6, §2.1, §2.2, §6.3.
- 5-icon grid: Child Management (C.21), Reports (C.22), Settings/Screen-Time (C.23), Subscription (C.24), Support (C.25).
- Does not duplicate any linked module's own content — only links to it.
- Return-to-Dashboard-from-cache instantly, background refresh if stale.
- Formal Parent Mode visual register (C.19 §2.1), consistent with platform's general grid pattern (e.g., A.10's Games Hub).

## 6. Existing Architecture
Builds on K-01's screen shell. Uses `Navigator`/`Route` pattern (`core-navigation`) exclusively for all 5 destinations — no direct `NavController` references (module must remain decoupled per `CORE_NAVIGATION_INSTRUCTIONS.md` §9's dependency rules).

## 7. Existing Code to Reuse
- `Navigator.navigateTo()` (`core-navigation`).
- `:core:design-system` icon-grid primitive (per PRD's cross-reference to A.10's Games Hub grid pattern — reuse that same grid component if it exists as a shared design-system primitive rather than building a new one).

## 8. Files to Create
- `feature/parent-dashboard/src/commonMain/kotlin/.../ModuleShortcutGrid.kt`
- `feature/parent-dashboard/src/commonTest/kotlin/.../ModuleShortcutGridNavigationTest.kt`

## 9. Files to Modify
- `ParentDashboardScreen.kt` — slot in the grid, wire back-navigation-from-cache behavior

## 10. KMP Requirements
- `ModuleShortcutGrid` Composable: 5 icon+label buttons, each navigating via `Navigator.navigateTo(<respective Route>)`. **All 5 routes now confirmed against the already-written C.21–C.25 blueprints** (previously placeholders, resolved by cross-reference):
  - Children → `ChildManagementRoute` (C.21, `data object`, `core-navigation/.../Route.kt`)
  - Reports → `PerChildReportRoute(childId: String)` (C.22, `data class` — **requires the currently-selected child's `childId`** from K-02's active-child state, unlike the other 4 which take no argument)
  - Settings → `ControlsLandingRoute` (C.23, `data object`, `feature/parental-controls/.../ControlsRoutes.kt`)
  - Subscription → `SubscriptionRoute` (C.24, `feature/subscription/navigation/SubscriptionRoute.kt`, deep link `noorheroes://parent/subscription`)
  - Support → `SupportCenterRoute` (C.25, `feature/parent-notifications-support/.../SupportCenterRoute.kt` — distinct from `NotificationsInboxRoute`, which is the separate bell-icon target added to K-01, not this grid)
  All 5 confirmed to use `requiredAuthState = BaseAuthState.Parent::class`, consistent with `ParentDashboardRoute`.
- On return to `ParentDashboardRoute` via back-navigation, the screen must re-render instantly from the ViewModel's already-held `StateFlow` (no re-fetch triggered on simple back-navigation) — only a background staleness check/refresh if the cached data has exceeded its TTL (coordinates with K-07's staleness logic).
- Grid rendered in the "more formal Parent Mode visual register" (per C.19 §2.1 cross-reference), distinct from child-facing playful styling.

## 11. Files/Screens
Composable within K-01's `ParentDashboardScreen`; the 5 destination screens themselves are owned by C.21–C.25, not built here.

## 12. NextJS Requirements
N/A.

## 13. API Contract
No new API — pure client-side navigation. Each destination module owns its own API contract (C.21–C.25).

## 14. Database Requirements
N/A.

## 15. Validation
N/A — navigation only.

## 16. Authentication
Inherits K-01's Parent Gate; each destination module (C.21–C.25) independently re-validates the parent session per its own gate/auth requirements (this grid does not bypass those checks — it simply triggers standard `Navigator` calls, and each target `Route`'s own `requiredAuthState` governs access).

## 17. Authorization
Standard per-module checks (C.21–C.25's own authorization), unaffected by this grid.

## 18. Error Handling
If a destination module fails to load, that is owned by the destination module's own error handling — this grid's only responsibility is firing a correct `navigateTo()` call.

## 19. Offline First
Return-to-Dashboard-from-cache behavior (§10) is this sub-feature's offline/performance-adjacent responsibility; full offline caching mechanics are K-07's.

## 20. Local Data
N/A directly — relies on K-01's ViewModel `StateFlow` remaining alive across the navigation round-trip (standard ViewModel-scoped-to-navigation-graph lifecycle, not re-created on simple back-navigation).

## 21. Localization
Grid labels ("Children", "Reports", "Settings", "Subscription", "Support") localized via the localization package.

## 22. RTL
Grid layout mirrors correctly (icon+label order, grid flow direction).

## 23. Analytics
`module_shortcut_tapped` with `module: child_management|reports|settings|subscription|support` (PRD §1.19).

## 24. Performance
Instant re-render from cache on back-navigation is an explicit NFR (PRD Edge Case #7) — avoid any full re-fetch/blocking spinner on simple back-navigation.

## 25. Security
N/A beyond what's already covered by K-01's Parent Gate and each destination module's own auth.

## 26. Library Requirements
No new dependencies.

## 27. Testing
1. Unit test: each of the 5 grid buttons calls `Navigator.navigateTo()` with the correct target `Route`.
2. Integration test: navigate out to a module, back-navigate, confirm Dashboard re-renders instantly from cache (no loading spinner shown for already-fetched data).
3. Integration test: background refresh triggers only when cached data is stale (per K-07's TTL), not on every back-navigation.
4. UI test: grid renders in formal Parent Mode visual register (design-token assertion).

## 28. Documentation
KDoc citing PRD §1.18 row 6, §6.3, Edge Case #7.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Module Shortcut Routes Mapping**
- Task ID: K06-T01
- Objective: Map each grid icon to its target `Route`.
- Why This Is Required: Type-safe navigation per platform convention.
- Existing Architecture to Follow: `Route` sealed interface, `Navigator.navigateTo()`.
- Existing Files to Reuse: `Navigator`, target modules' `Route` definitions — all 5 now confirmed (`ChildManagementRoute`, `PerChildReportRoute(childId)`, `ControlsLandingRoute`, `SubscriptionRoute`, `SupportCenterRoute`), see §10.
- Files to Create: none (mapping lives inside Task 02's Composable).
- Files to Modify: none.
- Implementation Details: `List<ModuleShortcutItem(icon, labelKey, routeFactory: (childId: String) -> Route)>` — model each entry as a factory taking the active `childId` even though only the Reports entry uses it, so the grid's tap-handling code is uniform (`route = item.routeFactory(selectedChildId)`) rather than special-casing one button.
- Business Rules: FR-14.
- Validation: N/A.
- Error Handling: N/A.
- Security: N/A.
- Performance: N/A.
- Localization: `labelKey` resolved via localization package.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 03.
- Documentation: KDoc.
- Dependencies: none (may be a stub/placeholder mapping until C.21–C.25 routes exist; document as such).
- Do Not Change: N/A.
- Expected Result: Mapping structure defined.
- Definition of Done: All 5 modules represented.

**Task 02 — Build ModuleShortcutGrid Composable and Wire Cache-Return Behavior**
- Task ID: K06-T02
- Objective: Visual grid + instant-return-from-cache logic.
- Why This Is Required: Core UI and performance requirement.
- Existing Architecture to Follow: `:core:design-system` grid primitive (A.10 Games Hub pattern), C.19 formal visual register.
- Existing Files to Reuse: Grid/icon-button design-system components.
- Files to Create: `ModuleShortcutGrid.kt`.
- Files to Modify: `ParentDashboardScreen.kt` (ensure ViewModel/StateFlow persists across navigation round-trip; add staleness-triggered background refresh).
- Implementation Details: Per §10.
- Business Rules: FR-2, FR-14, Edge Case #7.
- Validation: N/A.
- Error Handling: N/A (delegated to destination modules).
- Security: N/A.
- Performance: This IS the performance-critical logic (instant cache render, no blocking re-fetch).
- Localization: Labels localized.
- RTL: Grid mirrors correctly.
- Analytics: `module_shortcut_tapped`.
- Tests: Covered in Task 03.
- Documentation: KDoc.
- Dependencies: Task 01, K-01, K-07 (for staleness TTL coordination).
- Do Not Change: Do not modify the 5 destination modules themselves.
- Expected Result: Grid renders and navigates correctly; back-navigation is instant.
- Definition of Done: Matches PRD Edge Case #7 exactly.

**Task 03 — Write Test Suite**
- Task ID: K06-T03
- Objective: Cover §27.
- Why This Is Required: QA coverage, especially the cache-return performance guarantee.
- Existing Architecture to Follow: Existing navigation/test conventions.
- Existing Files to Reuse: Fake `Navigator` test double.
- Files to Create: `ModuleShortcutGridNavigationTest.kt`.
- Files to Modify: none.
- Implementation Details: 4 cases per §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: N/A.
- Security: N/A.
- Performance: Test #2/#3 are performance-critical.
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
Grid renders all 5 shortcuts correctly, navigates via type-safe `Route`s, returns to Dashboard instantly from cache with background-refresh-only-if-stale, all tests green.

## 31. Final Verification Checklist
- [ ] All 5 routes match confirmed names exactly: `ChildManagementRoute`, `PerChildReportRoute(childId)`, `ControlsLandingRoute`, `SubscriptionRoute`, `SupportCenterRoute`
- [ ] Reports entry correctly passes the active `childId` from K-02's state; the other 4 do not
- [ ] Support grid icon targets `SupportCenterRoute`, not `NotificationsInboxRoute` (that's K-01's separate bell icon)
- [ ] Instant cache-render on back-navigation verified (no spinner flash)
- [ ] Background refresh only on stale data, not every return
- [ ] Formal Parent Mode visual register applied (not child-facing playful style)
- [ ] RTL verified
