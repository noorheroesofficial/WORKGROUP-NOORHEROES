# N-01 — Security Posture Dashboard

## 1. Feature Context
Security Engineering and leadership need one consolidated place to confirm F.37's entire architecture is healthy — MFA compliance, penetration-test disposition, backup-restore history, tabletop-exercise history — rather than checking each underlying system individually. This blueprint builds that single read-only Admin Portal page. No school/institutional/madarsa logic applies.

## 2. Parent Feature
F.37 — Security Architecture (Cross-Cutting).

## 3. Sub-feature
N-01 — Security Posture Dashboard (NextJS Admin).

## 4. Objective
Build a single, strictly read-only Security Posture Dashboard page aggregating MFA-enrollment compliance, penetration-test finding disposition, backup-restore-test history, and incident-response tabletop-exercise history, per PRD §8/§9.

## 5. Business Requirements
- PRD §8: "Security Posture Dashboard (Read-only): A consolidated view of MFA-enrollment compliance across all admin/scholar accounts, recent penetration-test finding status/disposition, backup-restore-test history and results, and incident-response-procedure tabletop-exercise history — giving Security Engineering and leadership one place to confirm this entire architecture's health, rather than checking each underlying system individually."
- CRUD permissions (§8): "Security Posture Dashboard = Read-only behind `super_admin`/`security` role."
- PRD §9 (Admin AI Code-Generation Prompt, verbatim): "This page performs NO mutating actions -- it is purely a consolidated health-check view for Security Engineering and leadership. Restricted to `super_admin`/`security` roles." and "No audit logging needed for this page since it performs no mutating actions."

## 6. Existing Architecture
Per `NEXT-JS-INSTRUCTIONS.md`:
- `DashboardShell` (§3, §8) — the standard application layout shell every dashboard page wraps in.
- `RequirePermission` (§8) — the RBAC authorization guard component: `<RequirePermission permission="...">` — used to restrict the page to `super_admin` role holders granted the `security_posture` resource_scope (resolved per §13 below; the PRD's own "`super_admin`/`security`" phrasing is shorthand, not a literal second role).
- `DataTable` (§8) — the accessible, paginated data-table component for the pen-test findings and backup-restore-test-history lists.
- `useAdminSession()` (§9) — for the current admin's role, to conditionally gate access alongside `RequirePermission`.
- `DashboardRepositoryImpl` / `useDashboardStats()` (§5/§9) — the existing pattern for dashboard-statistics data fetching; this page's data-fetching hooks should follow this same repository → hook pattern rather than inventing a new data-access approach.
- Zero-token-persistence-in-browser-storage principle (§1) already governs the whole Admin Portal — no new deviation introduced by this page.

## 7. Existing Code to Reuse
- `DashboardShell` for page layout.
- `RequirePermission` for RBAC gating.
- `DataTable` for tabular sections (pen-test findings, backup-restore history).
- `LoadingState`, `EmptyState`, `ErrorView`/`QueryErrorState` (§8) for the standard per-panel states.
- `apiClient.get(path, options)` (§6) for data fetching, following the `BaseResourceClient`/Repository pattern (§5) already used by `DashboardRepositoryImpl` and similar repository classes.
- `useFormatters()` (§9) for date formatting (test dates, exercise dates).

## 8. Files to Create
- `src/app/(dashboard)/security-posture/page.tsx` — the page route (path/segment name to be reconciled with the Admin Portal's actual existing routing convention under `src/app/(dashboard)/*`).
- `src/features/security-posture/repositories/security-posture-repository.ts` — following the `CmsRepositoryImpl`/`DashboardRepositoryImpl` pattern (§5).
- `src/features/security-posture/hooks/use-security-posture.ts` — following the `useDashboardStats()` hook pattern (§9).
- `src/features/security-posture/components/mfa-compliance-panel.tsx`
- `src/features/security-posture/components/pentest-findings-panel.tsx`
- `src/features/security-posture/components/backup-restore-history-panel.tsx`
- `src/features/security-posture/components/incident-tabletop-history-panel.tsx`
- Tests: `src/features/security-posture/__tests__/security-posture-page.test.tsx`, RBAC-gating test.

## 9. Files to Modify
- Admin Portal navigation/sidebar configuration — add a "Security Posture" entry visible only to admins holding the `security_posture` resource_scope (default: `super_admin`, extensible to any role via E.28's standard maker-checker role-permission workflow).
- `API_ENDPOINTS` constant file (per §10's `API_ENDPOINTS.DASHBOARD.STATS` pattern) — add the three now-confirmed endpoint constants (pen-test findings, backup-restore history, tabletop history per §13) immediately; add the MFA-compliance constant once E.28 confirms it.

## 10. Backend Requirements
This blueprint does not implement backend endpoints (that's this feature's Backend track, B-08 for backup-restore/incident data and E.28 for `admin_user`/MFA data) — it consumes them. Required backend data sources, per PRD §9: (a) MFA/passkey enrollment status per admin/scholar account, sourced from E.28's `admin_user` table; (b) penetration-test findings with disposition, sourced from a `penetration_test_findings` reference table; (c) backup-restore-test history, sourced from B-08's `backup_restore_tests` table; (d) incident-response tabletop-exercise history, sourced from B-08's tabletop-tracking mechanism.

## 11. KMP Requirements
N/A — Admin Portal only, no mobile app surface.

## 12. NextJS Requirements
- Page composed of four read-only panels (MFA compliance, pen-test findings, backup-restore history, tabletop history), each independently loading/erroring (a failure in one panel must not block the others from rendering).
- MFA compliance panel: table/list of admin/scholar accounts with enrollment status, visually flagging non-compliant accounts (e.g., a `StatusBadge` in a warning state per §8's `StatusBadge` component).
- Pen-test findings panel: `DataTable` of findings with disposition status (fixed / risk-accepted / compensating-control), paginated via `usePaginationState` (§9).
- Backup-restore history panel: `DataTable` of test runs with pass/fail (`StatusBadge`) and dates (`useFormatters()`).
- Tabletop-exercise history panel: list/table of exercise dates and findings-actioned status.
- Page and all four panels gated by `RequirePermission` for the `security_posture` resource_scope (default: `super_admin`); a non-permitted admin sees the standard `RequirePermission` fallback (§8: "fallback: rendered when unauthorized"), never a partially-rendered page.
- Zero mutating actions anywhere on this page — no create/edit/delete affordances, no form, no button that triggers a `POST`/`PATCH`/`DELETE` call. This is the page's single most important constraint per the PRD's explicit, repeated emphasis.

## 13. API Contract
**Three of four panels now defined (previously flagged as pending); one remains a genuine external dependency.**

- Pen-test findings panel → `GET /api/v1/admin/security/pentest-findings` (defined in **B-09**, §13 of that blueprint) — paginated, filterable by severity/status/disposition.
- Backup-restore history panel → `GET /api/v1/admin/security-posture/backup-restore-history` (defined in **B-08 Task 04**, §13 of that blueprint) — paginated.
- Incident tabletop-history panel → `GET /api/v1/admin/security-posture/incident-tabletop-history` (defined in **B-08 Task 04**, §13 of that blueprint) — paginated.
- MFA compliance panel → **still an external dependency, not invented here.** This data is sourced from E.28's `admin_user` table (per PRD §9), and E.28 is explicitly out of scope for the F.37 blueprint set (F.37 delegates admin auth/RBAC entirely to E.28). No `GET` endpoint for MFA-enrollment-compliance-by-account currently exists in any reviewed document. Do not invent one here — this remains a confirmed blocker specifically for the MFA panel until E.28's own blueprint execution defines it (e.g., a plausible shape would be `GET /api/v1/admin/security-posture/mfa-compliance`, matching the naming convention of the other three, but this is a proposal for E.28's owners to confirm or override, not an implemented contract).

**Auth model resolved against E.28's actual RBAC architecture (previously a proposed `security:read`/`super_admin`/`security`-role guess — corrected).** E.28's PRD enumerates its actual 9 admin roles: content editor, publisher, scholar reviewer, child-safety reviewer, support agent, billing ops, analyst, localization manager, and super admin — **no role literally named "security" exists**, despite F.37 §8/§9's own shorthand phrasing implying one. E.28's real authorization model (FR-5) is role + resource_scope + region + locale + action via its `role_permission` table. The three confirmed endpoints above are all gated on **role `super_admin` + resource_scope `security_posture`, action `read`**; the MFA-compliance endpoint (once E.28 defines it) should follow the same resource_scope+action pattern rather than a bespoke scheme, for consistency. All four panels' `RequirePermission` checks in the frontend should reference this same `security_posture:read`-equivalent permission key once the frontend's own permission-key naming is confirmed against `AdminAuthContext`'s server-provided permission set (per `NEXT-JS-INSTRUCTIONS.md` §6.4-equivalent — `AdminAuthContext` computes visible UI entirely from the server-provided role/permission response, never a hardcoded role-name check client-side, per E.28 §6's explicit testing requirement).

## 14. Database Requirements
N/A directly (NextJS Admin has no direct DB access; consumes backend APIs only). Underlying tables: `admin_user` (E.28, still external), `penetration_test_findings` (now defined by B-09), `backup_restore_tests` and `incident_tabletop_exercises` (now defined by B-08).

## 15. Validation
N/A — read-only page, no form input to validate.

## 16. Authentication
Standard Admin Portal session via `useAdminSession()`; no new authentication mechanism introduced.

## 17. Authorization
`RequirePermission` gates the entire page and, defensively, each panel individually (defense-in-depth consistent with the platform's B-06 principle: don't rely solely on a single top-level gate if panel-level data-fetching could otherwise be triggered independently) restricted to `super_admin`/`security` roles per PRD §8's explicit CRUD-permissions line. Never rely on hiding the nav entry alone (§12 Do's/Don'ts of `NEXT-JS-INSTRUCTIONS.md`: "Do NOT bypass `RequirePermission`... ensure backend endpoints enforce permissions") — the backend endpoint(s) this page calls must independently enforce the same RBAC restriction, not merely trust the frontend gate.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Individual panel's data fetch fails | That panel shows `ErrorView`/`QueryErrorState`; other panels continue to render normally |
| User lacks the `security_posture` resource_scope | `RequirePermission`'s standard unauthorized fallback, page content never rendered |
| No pen-test findings / no tabletop exercises yet logged | `EmptyState` per panel, not an error |
| Backend endpoint not yet available (during phased rollout) | Panel shows a clear "not yet available" state rather than a raw error, if distinguishable from a genuine fetch failure |

## 19. Offline First
N/A — Admin Portal is an online-only web application; no offline-first requirement per existing Admin Portal architecture.

## 20. Local Data
N/A — no client-side persistence beyond standard in-memory query-cache state (React Query or equivalent, per whatever the Admin Portal's existing data-fetching hook convention already uses — confirm and reuse, don't introduce a new state-management library).

## 21. Localization
Page and panel labels routed through `useTranslation()` (§9) per the Admin Portal's existing i18n convention; status labels (compliant/non-compliant, fixed/risk-accepted/compensating-control, pass/fail) must also be localized strings, not hardcoded English.

## 22. RTL
Admin Portal's existing RTL support (implied by the platform's Arabic/Urdu localization requirements) must be respected — `DataTable`, `StatusBadge`, and panel layouts should already handle RTL via the shared component library; no new RTL-specific work expected beyond using these existing components correctly (no hardcoded `left`/`right` CSS in this page's own styling).

## 23. Analytics
No dedicated end-user-facing analytics event is specified in PRD §1.19 for this internal admin page (those events are the security-signal events like `backup_restore_test_completed`, which this page merely displays, not emits). If the Admin Portal has an existing internal page-view analytics convention, apply it consistently with other admin pages — do not invent a new analytics pattern specific to this page.

## 24. Performance
Each panel's query should be independently cached/paginated (via `usePaginationState` for the tabular ones) to avoid one large monolithic fetch; large pen-test-findings or backup-restore-history datasets must use `DataTable`'s existing pagination rather than rendering unbounded lists.

## 25. Security
- Zero mutating actions — this is the page's core security property per PRD §9's explicit, repeated emphasis; any future feature request to add a mutating action to this page should be treated as a scope change requiring its own security review, not a minor addition.
- RBAC enforced both client-side (`RequirePermission`) and server-side (the consumed endpoint(s) must independently check `super_admin` role + `security_posture` resource_scope, not trust the frontend) — per §17.
- No audit logging required specifically because this page performs no mutating actions (PRD §9) — do not add audit-log calls here; that would be inconsistent with the PRD's explicit statement and would misleadingly suggest a mutating action occurred.

## 26. Library Requirements
No new library — reuse the existing `DataTable`, `RequirePermission`, `DashboardShell`, `StatusBadge`, `EmptyState`, `ErrorView` component library and the existing data-fetching hook pattern already used by `useDashboardStats()` and similar hooks.

## 27. Testing
- **RBAC-gating test:** an admin lacking the `security_posture` resource_scope (including a `super_admin` not yet granted it, and any of E.28's other 8 roles by default) is denied access (page/panels do not render content).
- **Per-panel rendering tests:** each of the four panels renders correctly given mock data (loading, populated, empty, error states each independently tested).
- **Independent-failure test:** one panel's fetch failing does not block the other three panels from rendering.
- **No-mutation test:** confirm (via code review / a lint-style check if feasible) that no `POST`/`PATCH`/`DELETE` call exists anywhere in this page's component tree or its repository/hook files.
- **Localization test:** confirm no hardcoded English strings exist outside the `useTranslation()` mechanism.

## 28. Documentation
Document the page's four data sources and their owning backend features (E.28, B-08, and the not-yet-confirmed `penetration_test_findings` source) in the component/repository file's header comment, so a future maintainer knows exactly where each panel's data originates; explicitly note the API-contract-pending flag from §13 until resolved.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm the Remaining Backend API Contract (MFA Panel Only — Blocking Prerequisite for That Panel)**
- Task ID: N-01-T01
- Objective: Three of four data sources are now defined (pen-test findings via B-09, backup-restore/tabletop history via B-08 Task 04 — see §13); this task's remaining scope is narrowed to confirming the fourth, the MFA-compliance endpoint, with E.28's owners before writing fetching code against a guessed contract.
- Why This Is Required: Rule "Do Not Guess" — API endpoints must never be invented; E.28 is out of scope for this blueprint set and hasn't yet defined this endpoint.
- Existing Architecture to Follow: `API_ENDPOINTS` constant pattern (§10 of `NEXT-JS-INSTRUCTIONS.md`); match the naming convention already set by the three confirmed endpoints (`/api/v1/admin/security-posture/...`).
- Existing Files to Reuse: `API_ENDPOINTS.DASHBOARD.STATS` as the naming-convention reference.
- Files to Create: none yet.
- Files to Modify: none yet.
- Implementation Details: coordinate with E.28's owners to finalize the MFA-compliance endpoint's path/response shape; the other three panels (Tasks 04 below) can proceed immediately since their contracts are now defined.
- Business Rules / Validation / Error Handling / Security / Performance: N/A at this task.
- Localization / RTL / Analytics: N/A.
- Tests: none yet.
- Documentation: record the confirmed MFA contract once available.
- Dependencies: E.28 (backend, external to this blueprint set).
- Do Not Change: N/A.
- Expected Result: MFA-compliance endpoint contract confirmed.
- Definition of Done: contract confirmed in writing before the MFA panel (Task 03) is wired to real data; if still unconfirmed, Task 03 proceeds with a clearly-marked mock/fixture and the panel is flagged as blocked for real-data wiring while the other three panels ship normally.

**Task 02 — Build the Page Shell, Routing, and RBAC Gate**
- Task ID: N-01-T02
- Objective: Scaffold the page route wrapped in `DashboardShell` and gated by `RequirePermission`.
- Why This Is Required: Establishes the container every panel renders inside, and the security gate first.
- Existing Architecture to Follow: `DashboardShell`, `RequirePermission` (§6/§7).
- Existing Files to Reuse: both components directly.
- Files to Create: `src/app/(dashboard)/security-posture/page.tsx`.
- Files to Modify: navigation/sidebar config.
- Implementation Details: `<RequirePermission permission="security_posture:read">` (permission-key string resolved to mirror E.28's resource_scope+action model — `security_posture` scope, `read` action; confirm the exact frontend permission-key serialization format against `AdminAuthContext`'s actual server-provided shape before finalizing, since this is the frontend's rendering of the backend's role+resource_scope+action triple, not a second independent naming scheme).
- Business Rules: read-only, gated to the `security_posture` resource_scope (default: `super_admin`).
- Validation: N/A.
- Error Handling: `RequirePermission`'s standard fallback.
- Security: client-side gate only — server-side enforcement is Task 01's contract's responsibility.
- Performance: N/A.
- Localization: page title via `useTranslation()`.
- RTL: inherited from `DashboardShell`.
- Analytics: N/A.
- Tests: RBAC-gating test per §27.
- Documentation: none beyond code comments.
- Dependencies: none beyond existing shared components.
- Do Not Change: `DashboardShell`/`RequirePermission` themselves.
- Expected Result: an empty, correctly-gated page shell.
- Definition of Done: RBAC test passes.

**Task 03 — Implement the MFA Compliance Panel**
- Task ID: N-01-T03
- Objective: Build the MFA/passkey enrollment compliance panel.
- Why This Is Required: First of four required panels (§9).
- Existing Architecture to Follow: `DataTable`/`StatusBadge` pattern.
- Existing Files to Reuse: `DataTable`, `StatusBadge`, `useFormatters()`.
- Files to Create: `mfa-compliance-panel.tsx`, its repository/hook slice.
- Files to Modify: none beyond its own new files.
- Implementation Details: list admin/scholar accounts with enrollment status, flag non-compliant via `StatusBadge` warning variant.
- Business Rules: read-only.
- Validation: N/A.
- Error Handling: per §18.
- Security: no mutating affordance.
- Performance: paginate if the account list is large.
- Localization: all labels via `useTranslation()`.
- RTL: inherited from shared components.
- Analytics: N/A.
- Tests: per §27's per-panel rendering tests.
- Documentation: data-source comment per §28.
- Dependencies: Task 01's confirmed MFA contract (still pending E.28 as of this writing), Task 02.
- Do Not Change: `admin_user` data model itself (E.28-owned).
- Expected Result: functional, read-only MFA compliance panel — built against a mock/fixture if Task 01's contract remains unconfirmed, clearly marked as such, and swapped to the real endpoint once E.28 defines it.
- Definition of Done: rendering tests pass for all states; real-data wiring confirmed done only once Task 01's MFA contract is finalized (track as a follow-up if shipped against a mock).

**Task 04 — Implement the Pen-Test Findings, Backup-Restore History, and Tabletop History Panels**
- Task ID: N-01-T04
- Objective: Build the remaining three panels.
- Why This Is Required: Completes PRD §9's required aggregation.
- Existing Architecture to Follow: same `DataTable`/`StatusBadge`/pagination pattern as Task 03.
- Existing Files to Reuse: `DataTable`, `StatusBadge`, `usePaginationState`, `useFormatters()`.
- Files to Create: `pentest-findings-panel.tsx`, `backup-restore-history-panel.tsx`, `incident-tabletop-history-panel.tsx`, their repository/hook slices.
- Files to Modify: none beyond their own new files.
- Implementation Details: per §12's per-panel descriptions.
- Business Rules: read-only, each panel independently loading/erroring (§18).
- Validation: N/A.
- Error Handling: per §18, including independent-failure isolation.
- Security: no mutating affordance in any of the three.
- Performance: `DataTable` pagination for potentially large findings/history lists.
- Localization: all labels via `useTranslation()`.
- RTL: inherited.
- Analytics: N/A.
- Tests: per-panel rendering tests, independent-failure test.
- Documentation: data-source comments (B-08 Task 04 for backup-restore/tabletop history, B-09 for pen-test findings — all three now concretely defined, see §13).
- Dependencies: B-08 Task 04 and B-09's confirmed contracts (both defined, no longer blocked), Task 02, Task 03 (for consistency of pattern).
- Do Not Change: N/A.
- Expected Result: all four panels complete and independently functional.
- Definition of Done: all §27 tests pass, including the independent-failure isolation test.

**Task 05 — No-Mutation & Final Accessibility/Localization Pass**
- Task ID: N-01-T05
- Objective: Verify and lock in the page's zero-mutating-action guarantee and complete accessibility/localization review.
- Why This Is Required: PRD §9's most explicitly repeated constraint; also the standard NextJS Admin quality bar (§25 accessibility per the platform's general requirements).
- Existing Architecture to Follow: platform accessibility/localization conventions already applied elsewhere in the Admin Portal.
- Existing Files to Reuse: N/A (review task).
- Files to Create: none.
- Files to Modify: any panel found to contain a stray mutating call or hardcoded string.
- Implementation Details: code review/lint pass across all four panels and the page shell for any `POST`/`PATCH`/`DELETE` call or hardcoded English string.
- Business Rules: zero mutations, full localization coverage.
- Validation: N/A.
- Error Handling: N/A.
- Security: confirms §25's core property.
- Performance: N/A.
- Localization: confirms §21.
- RTL: confirms §22 via visual/manual check if automated RTL testing isn't already standard.
- Analytics: N/A.
- Tests: the no-mutation test and localization test per §27.
- Documentation: final sign-off note in the page's header comment.
- Dependencies: Tasks 02–04.
- Do Not Change: N/A.
- Expected Result: page confirmed fully read-only, fully localized, fully accessible.
- Definition of Done: no-mutation test and localization test pass; page ready for review.

## 30. Definition of Done
Page built, gated by `RequirePermission` for the `security_posture` resource_scope (default: `super_admin`); three of four panels (pen-test findings, backup-restore history, tabletop history) functional against confirmed, concrete backend contracts (B-09, B-08 Task 04); the MFA-compliance panel functional against either the confirmed E.28 contract or a clearly-marked mock pending that confirmation; zero mutating actions anywhere; fully localized and RTL-correct; all tests passing.

## 31. Final Verification Checklist
- [ ] Pen-test findings, backup-restore-history, and tabletop-history contracts confirmed against B-09/B-08 (done — no longer guessed)
- [ ] MFA-compliance contract confirmed with E.28, or panel explicitly shipped against a marked mock with a tracked follow-up
- [ ] Page and all four panels gated by `RequirePermission` for the `security_posture` resource_scope (role `super_admin` by default, never an invented literal "security" role)
- [ ] Server-side endpoint(s) independently enforce the same RBAC restriction (not frontend-only)
- [ ] MFA compliance panel flags non-compliant accounts clearly
- [ ] Pen-test findings panel shows disposition status, paginated
- [ ] Backup-restore history panel shows pass/fail and dates, paginated
- [ ] Tabletop-exercise history panel shows exercise history
- [ ] One panel's fetch failure does not block the other three
- [ ] Zero mutating actions anywhere on the page (verified, not assumed)
- [ ] No audit logging added (correctly, per PRD §9's explicit statement)
- [ ] Full localization coverage, no hardcoded strings
- [ ] RTL rendering correct via shared component library
