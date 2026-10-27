# N-02 — Role-Scoped Navigation & Permission-Driven Shell

## 1. Feature Context
Part of E.28. Governs navigation visibility across all Admin Portal screens per PRD §2.1 "Permission-Scoped Navigation" and §6.3/§6.4. Extends the existing `DashboardShell`, `RequirePermission`, `hasPermission()`, `useAdminSession()` infrastructure already present in `noorheroes-admin`.

## 2. Parent Feature
E.28 — Admin Portal: Authentication, RBAC & Operations Dashboard

## 3. Sub-feature
N-02 — Role-Scoped Navigation & Permission-Driven Shell

## 4. Objective
Compute the sidebar's visible navigation items entirely from the server-provided role/permission response, with zero hardcoded role-name checks anywhere in the rendering logic, so a future new role/permission requires no frontend code change (PRD §7 Frontend AI prompt item 2).

## 5. Business Requirements
- §2.1: navigation renders only modules/items the current admin's role permits; no greyed-out/disabled-but-visible treatment — items are simply absent ("hide, don't show-disabled").
- §6.3: sidebar items computed from role-scope, fetched once at login, re-validated on each protected route's mount.
- §6.4: `AdminAuthContext` holds identity/role/resolved permission set; mutating actions still rely on the backend's own independent check as the real boundary (frontend hiding is convenience only).

## 6. Existing Architecture
- `useAdminSession()` already returns `{ admin, isAuthenticated, isLoading, refreshSession, signOut }` — N-02 extends the `admin` claims shape to include the resolved permission set from B-03.
- `hasPermission(admin, permission)` already exists — returns `true` if admin has permission or is `SUPER_ADMIN`. This is a **flat** permission check today; N-02 must decide whether to extend its signature to accept resource/region/locale dimensions (matching B-03's multi-dimensional model) or keep it flat for navigation-visibility purposes (a reasonable simplification, since navigation visibility is coarser-grained than the full multi-dimensional API-level check B-03 enforces server-side) — **decision: keep `hasPermission()` flat for nav-visibility UX purposes; the real multi-dimensional enforcement always happens server-side per B-03, so no security regression results from a simpler client-side visibility heuristic.**
- `RequirePermission` component already exists (`<RequirePermission permission="users:read">`) — reused as-is for gating both nav items and in-page action buttons.
- `DashboardShell` already exists as the layout wrapper — N-02 extends it to render the 8 navigation groups (Operate/Users/Content/Review/Engagement/Commerce/Intelligence/Platform) from a data-driven registry, not a hardcoded JSX list.

## 7. Existing Code to Reuse
| Component | Location | Reuse For |
|---|---|---|
| `useAdminSession()` | `src/features/auth/hooks/` | Session/permission-set source of truth |
| `hasPermission()` | `src/shared/utils/` | Per-item visibility check |
| `RequirePermission` | `src/shared/components/` | Declarative gating |
| `DashboardShell` | `src/shared/components/dashboard-shell.tsx` | Layout wrapper, extended with data-driven nav |
| `useTranslation()` | `src/shared/hooks/` | Nav label localization |

## 8. Files to Create
- `src/shared/config/navigation-registry.ts` — data-driven nav-group/item registry (group key, item key, route, required permission — no role names)
- `src/shared/hooks/use-scoped-navigation.ts` — computes visible nav tree from `useAdminSession()` + registry
- `tests/shared/navigation/no-hardcoded-role-checks.test.ts` — static/lint-style test
- `tests/shared/navigation/scoped-navigation.test.tsx`

## 9. Files to Modify
- `src/shared/components/dashboard-shell.tsx` — render nav from `useScopedNavigation()` instead of any hardcoded item list
- `src/features/auth/hooks/use-admin-session.ts` — extend `admin` claims to carry the resolved permission set from B-03's role/permission response

## 10. NextJS Requirements
- Sidebar renders the 8 navigation groups (Operate/Users/Content/Review/Engagement/Commerce/Intelligence/Platform), each filtered to only the items the current admin's permission set includes.
- Fetch permission set once at login (via B-01/B-02's session establishment response, extended with role/permission data — coordinate with B-03's `GET /v1/admin/roles` or a dedicated "my permissions" resolved-claims endpoint if the login response itself doesn't already embed it).
- Re-validate on each protected route's mount — never trust a stale client-side cache for a mutating action's actual permission (the backend remains the real boundary per FR-5/Edge Case 6).
- Absent items are never rendered greyed-out — they simply don't exist in the DOM for that admin.

## 11. API Contract (Consumed)
- Session/login response (B-01/B-02) extended with resolved role/permission claims, or `GET /v1/admin/roles` (B-03) queried post-login to resolve the current admin's own permission set.

## 12. Database Requirements
N/A (frontend).

## 13. Validation
N/A (read-only navigation logic).

## 14. Authentication
Assumes an established session from N-01.

## 15. Authorization
This module is the **UX layer** of authorization — convenience only, never the actual boundary (which remains B-03's server-side `require_admin_permission()`).

## 16. Error Handling
- Permission-fetch failure on mount → fall back to a minimal/no-nav-items state with a retry affordance, never a crash or a "show everything" fail-open default (fail closed, not open, for a security-adjacent UI surface).
- Expired/invalidated session mid-navigation → redirect to login (existing middleware/session-check behavior).

## 17. Offline First
N/A (per PRD §6.7).

## 18. Local Data
Permission set held in React state/context for the session duration only — not persisted to `localStorage`/`sessionStorage`.

## 19. Localization
All nav labels via `useTranslation()`; the registry stores translation keys, not literal strings.

## 20. RTL
Sidebar must correctly mirror for RTL locales (AR/UR) — verify icon/label order and any collapse/expand affordances flip correctly.

## 21. Analytics
No dedicated event for navigation-item visibility itself; supports the general `operations_dashboard_viewed` and similar screen-view events fired by the destination screens themselves.

## 22. Performance
- Nav visibility computation is a pure client-side filter over a small, static registry — negligible cost; no need for memoization beyond standard React practice, but apply `useMemo` around the filtered list to avoid recomputation on every render.

## 23. Security
- **Zero hardcoded role-name checks (primary guarantee):** verified by a dedicated test (Task 04) — this is explicitly called out in the PRD as mirroring the extensible-registry-driven pattern established for B.17's notification categories.
- Fail-closed default: if the permission set fails to load, show no navigation items rather than all of them.
- Frontend hiding is never relied upon as the actual security boundary in any documentation or code comment — always paired with a note that B-03's server-side check is the real guarantee.

## 24. Library Requirements
No new libraries.

## 25. Testing
- **Mandatory test (§7 item 2):** no hardcoded role-name checks exist anywhere in the navigation-rendering logic — a future new role/permission requires zero frontend code change to be correctly reflected.
- Unit: `useScopedNavigation()` filtering logic across multiple fixture permission sets.
- Unit: fail-closed behavior on permission-fetch failure.
- Accessibility: keyboard navigation through the sidebar, screen-reader labels.

## 26. Documentation
Document the navigation-registry pattern in the NextJS admin manual as the canonical way to add a new nav item for E.29–E.34 modules going forward (add an entry to the registry with a permission key — no route-level or component-level role checks needed).

## 27. AI Coding Agent Implementation Steps

**Task 01 — Build the Navigation Registry**
- Task ID: N-02-T01
- Objective: Data-driven source of truth for all nav groups/items.
- Files to Create: `navigation-registry.ts`.
- Implementation Details: Array of `{ groupKey, itemKey, route, requiredPermission, labelKey }` — no role names anywhere in this structure, only permission keys.
- Dependencies: B-03's permission-key naming (coordinate resource_scope identifiers: `roles`, `audit-logs`, `feature-flags`, `config`, `dashboard`, `admin-users`, plus future E.29–E.34 scopes).
- Definition of Done: Registry covers all 8 nav groups and E.28's own screens at minimum.

**Task 02 — Extend `useAdminSession()` with Resolved Permission Set**
- Task ID: N-02-T02
- Files to Modify: `use-admin-session.ts`.
- Implementation Details: Fetch/store the permission set alongside existing `admin` claims; re-fetch on each protected route mount per §6.3.
- Dependencies: B-01/B-02 session response or B-03 roles endpoint.
- Definition of Done: `admin.permissions` available wherever `useAdminSession()` is consumed.

**Task 03 — Implement `useScopedNavigation()` Hook**
- Task ID: N-02-T03
- Files to Create: `use-scoped-navigation.ts`.
- Implementation Details: Filters the registry against `admin.permissions` via `hasPermission()`; returns the visible nav tree grouped by `groupKey`.
- Performance: `useMemo`-wrapped.
- Dependencies: Task 01, Task 02.
- Definition of Done: Returns correct filtered tree for multiple fixture permission sets.

**Task 04 — No-Hardcoded-Role-Checks Test (Signature Test)**
- Task ID: N-02-T04
- Objective: Prove zero hardcoded role-name checks in navigation-rendering logic.
- Files to Create: `tests/shared/navigation/no-hardcoded-role-checks.test.ts`.
- Implementation Details: Static scan of the navigation-rendering module's source for string-literal role names (e.g., `"super_admin"`, `"Content Editor"`) outside the registry/permission-key context; fail the test if any are found in conditional rendering logic.
- Dependencies: Tasks 01–03.
- Definition of Done: Test passes; documented as the canonical enforcement mechanism for future PRs touching navigation.

**Task 05 — Wire `DashboardShell` to the Registry-Driven Nav**
- Task ID: N-02-T05
- Files to Modify: `dashboard-shell.tsx`.
- Implementation Details: Replace any hardcoded nav-item JSX with a render loop over `useScopedNavigation()`'s output.
- Dependencies: Task 03.
- Definition of Done: Sidebar renders correctly across fixture roles with zero absent-item flicker/grey-out.

**Task 06 — Fail-Closed Error Handling**
- Task ID: N-02-T06
- Objective: Permission-fetch failure shows no items, not all items.
- Dependencies: Task 02.
- Tests: Fail-closed unit test.
- Definition of Done: Simulated fetch failure results in empty nav, not a fail-open state.

**Task 07 — Localization, RTL, Accessibility Pass**
- Task ID: N-02-T07
- Dependencies: Task 05.
- Definition of Done: All nav labels localized; RTL mirroring verified; keyboard/screen-reader accessible.

**Task 08 — Full Test Suite + Documentation**
- Task ID: N-02-T08
- Files to Create: `tests/shared/navigation/scoped-navigation.test.tsx`.
- Dependencies: Tasks 01–07.
- Definition of Done: All §25 scenarios green; navigation-registry pattern documented for future module authors.

## 28. Definition of Done
- Sidebar navigation entirely data/permission-driven, zero hardcoded role checks.
- Absent items simply don't render (no greyed-out state).
- Fail-closed on permission-fetch failure.
- Fully localized and RTL-correct.

## 29. Final Verification Checklist
- [ ] Signature test passes: zero hardcoded role-name checks in nav-rendering logic
- [ ] Navigation registry covers all 8 groups and is the sole source of truth for nav items
- [ ] Fail-closed verified on permission-fetch failure
- [ ] Absent items never render greyed-out/disabled
- [ ] Permission set re-validated on each protected route mount
- [ ] RTL mirroring verified for AR/UR
- [ ] Accessibility (keyboard/screen-reader) verified
