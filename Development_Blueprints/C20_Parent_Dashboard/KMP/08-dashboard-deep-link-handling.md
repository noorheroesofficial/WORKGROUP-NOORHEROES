# Blueprint: Dashboard Deep Link Handling

## 1. Feature Context
Platform: NoorHeroes KMP App. Module `:feature:parent-dashboard`, integrating with `:core:navigation` and `:core:auth`.

## 2. Parent Feature
C.20 — Parent Dashboard.

## 3. Sub-feature
K-08 — Dashboard Deep Link Handling.

## 4. Objective
Register the `noorheroes://parent/dashboard` deep link and guarantee it always passes through C.19's Parent Gate revalidation, never bypassing it — including when originating from a push notification (owned by C.25).

## 5. Business Requirements
Source: PRD §6.8, §6.9.
- Deep link `noorheroes://parent/dashboard` reachable only through the standard Parent Gate flow even if accessed via a deep link (B.17's universal deep-link-revalidation principle).
- Not a notification source itself, but may be the landing target for parent-facing notification types (C.25), always passing through the Parent Gate on open.

## 6. Existing Architecture
Per `CORE_NAVIGATION_INSTRUCTIONS.md` §10 Scenario 1: "Deep Linking / Push Notifications — When a notification arrives, you can use the Navigator to jump straight to a specific route." The platform's `Route.requiredAuthState` property (§4 of that doc) is the mechanism for navigation guards — this is the same mechanism K-01's `ParentDashboardRoute` already declares, so deep links targeting this route are automatically subject to the same guard, provided the deep-link resolution path correctly routes through the standard `Navigator`/guard pipeline rather than a shortcut that bypasses it.

## 7. Existing Code to Reuse
- `ParentDashboardRoute` and its `requiredAuthState` (defined in K-01) — this sub-feature does not redefine the route, only ensures the deep-link resolution mechanism respects it.
- `Navigator.navigateTo()`.
- Deep-link parsing/URI-to-Route resolution mechanism (platform-level, likely in `:core:navigation` or an app-level deep-link handler — confirm exact location before modifying).

## 8. Files to Create
- `feature/parent-dashboard/src/commonTest/kotlin/.../DashboardDeepLinkGateEnforcementTest.kt`

## 9. Files to Modify
- App-level deep-link URI-to-Route resolver/registry — add mapping `noorheroes://parent/dashboard` → `ParentDashboardRoute`

## 10. KMP Requirements
- Register the URI pattern `noorheroes://parent/dashboard` in the platform's existing deep-link resolver, mapping to `ParentDashboardRoute`.
- Confirm (via Task 01's investigation) that the deep-link resolution pipeline resolves to a `Route` and then goes through the SAME `requiredAuthState`-checking mechanism as in-app `Navigator.navigateTo()` calls — if the deep-link pipeline has any code path that navigates directly to a Composable/NavController destination without passing through this guard, that is an architectural gap this sub-feature must close (per B.17's universal deep-link-revalidation principle), not merely document.
- If the app is cold-started via this deep link while unauthenticated or in a child-mode session, the resolved flow must redirect first through C.19's Parent Gate (or, if no session exists at all, standard login), landing on the Dashboard only after successful verification — never a direct bypass.

## 11. Files/Screens
No new screens — registration/wiring only.

## 12. NextJS Requirements
N/A.

## 13. API Contract
No backend contract — client-side navigation/deep-link registration only.

## 14. Database Requirements
N/A.

## 15. Validation
Deep link with malformed/extra parameters must fail closed to a safe default (e.g., standard login or Parent Gate), never crash or silently grant access.

## 16. Authentication
This sub-feature's entire purpose is authentication enforcement on a non-standard entry path (deep link vs. in-app tap).

## 17. Authorization
Same `requiredAuthState`/Parent Gate enforcement as in-app navigation — no weaker parallel path.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Deep link opened while unauthenticated | Redirect to standard login, then Parent Gate, then Dashboard |
| Deep link opened during active child-mode session | Redirect through Parent Gate (session switch/re-verification), never directly into parent data |
| Deep link opened with valid, already-elevated parent session within grace window | Direct-to-Dashboard (consistent with C.19's grace-window mechanic, not a weaker bypass) |
| Malformed deep-link URI | Fail closed to safe default screen |

## 19. Offline First
If opened while offline, standard K-07 offline-cache behavior applies once the gate is satisfied (or, if gate itself requires a network call for verification, standard C.19 offline-handling applies — owned by C.19, not this blueprint).

## 20. Local Data
N/A.

## 21. Localization
N/A (no user-facing strings introduced by this sub-feature beyond what C.19's gate screens already localize).

## 22. RTL
N/A.

## 23. Analytics
Deep-link opens may be tagged with a source parameter (e.g., `source: notification`) on the standard `parent_dashboard_viewed` event if the analytics schema supports an origin/source field — confirm against `CORE_ANALYTICS_INSTRUCTIONS.md` before adding.

## 24. Performance
N/A beyond standard navigation performance.

## 25. Security
This is the defining guarantee of this sub-feature: a deep link must never be a weaker authentication path than in-app navigation. This directly parallels B-01's backend guarantee (no bypass via a "new route") applied to the client-side navigation graph instead.

## 26. Library Requirements
No new dependencies.

## 27. Testing
1. Unit test: deep link resolves to `ParentDashboardRoute`.
2. **Mandatory test:** deep link opened with no active session redirects through login → Parent Gate → Dashboard, never directly.
3. **Mandatory test:** deep link opened during an active child-mode session redirects through Parent Gate, never directly into parent data.
4. Unit test: malformed deep-link URI fails closed to a safe default.
5. Unit test: deep link opened with an already-elevated parent session (within grace window) proceeds directly (correct, non-bypass fast path).

## 28. Documentation
KDoc citing PRD §6.8, §6.9, and the B.17 universal deep-link-revalidation principle.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Investigate Existing Deep-Link Resolution Pipeline**
- Task ID: K08-T01
- Objective: Confirm whether the platform's deep-link resolver already enforces `requiredAuthState`, or has a gap.
- Why This Is Required: Do-Not-Guess instruction — must verify actual behavior, not assume.
- Existing Architecture to Follow: App-level deep-link handler (location TBD by investigation).
- Existing Files to Reuse: N/A (investigation task).
- Files to Create: none.
- Files to Modify: none.
- Implementation Details: Search the codebase for the URI-to-Route resolver and trace whether it invokes the same guard path as `Navigator.navigateTo()`.
- Business Rules: B.17 universal deep-link-revalidation principle.
- Validation: N/A.
- Error Handling: N/A.
- Security: This investigation determines the security posture.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: N/A.
- Documentation: Record findings before Task 02.
- Dependencies: none.
- Do Not Change: N/A.
- Expected Result: Clear understanding of whether a gap exists.
- Definition of Done: Findings documented, informing Task 02's scope.

**Task 02 — Register URI Mapping and Close Any Guard Gap**
- Task ID: K08-T02
- Objective: Wire `noorheroes://parent/dashboard` correctly, closing any bypass found in Task 01.
- Why This Is Required: Core deliverable.
- Existing Architecture to Follow: Per Task 01's findings.
- Existing Files to Reuse: `ParentDashboardRoute` (K-01), `Navigator`.
- Files to Create: none.
- Files to Modify: App-level deep-link resolver/registry.
- Implementation Details: Per §10.
- Business Rules: §18.
- Validation: Malformed-URI fail-closed behavior.
- Error Handling: Per §18.
- Security: This IS the security fix if Task 01 found a gap.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: Source-tagging if supported.
- Tests: Covered in Task 03.
- Documentation: KDoc.
- Dependencies: Task 01, K-01.
- Do Not Change: Do not weaken the guard for any other existing deep-linked route while fixing this one.
- Expected Result: Deep link always passes through the same guard as in-app navigation.
- Definition of Done: Tests #2 and #3 in §27 pass.

**Task 03 — Write Test Suite**
- Task ID: K08-T03
- Objective: Cover §27, especially the two mandatory bypass-prevention tests.
- Why This Is Required: Security-critical verification.
- Existing Architecture to Follow: Existing navigation test conventions.
- Existing Files to Reuse: Fake session/auth-state test doubles.
- Files to Create: `DashboardDeepLinkGateEnforcementTest.kt`.
- Files to Modify: none.
- Implementation Details: 5 cases per §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: N/A.
- Security: Tests #2/#3 are the core security guarantee of this entire sub-feature.
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
Deep link registered and mapped correctly; provably never a weaker authentication path than in-app navigation, in any session state; all tests green.

## 31. Final Verification Checklist
- [ ] Investigation findings from Task 01 documented
- [ ] No bypass path confirmed via both mandatory tests
- [ ] Malformed URI fails closed
- [ ] Grace-window fast path is correct (not a bypass) and distinctly tested from the bypass-prevention tests
