# N-02 — Parent Web Portal Application Shell, Routing & Shared Foundation

## 1. Feature Context
Part of Feature D.27 — Parent Web Account Portal. This is the foundational sub-feature every other Parent Web Portal screen (N-03–N-10) depends on: the application shell, the exact 23-route router with zero wildcard, the scope-restricted `apiClient`, the shared `StepUpModal`, the `SessionContext`, and the design-token consumption that makes this a genuinely third-layer structural guarantee (alongside B-01's gateway allowlist and B-02's application middleware) that child data and purchase-initiation can never reach this surface.

## 2. Parent Feature
D.27 Parent Web Account Portal (`account.noorheroes.com`)

## 3. Sub-feature
**N-02 — Parent Web Portal Application Shell, Routing & Shared Foundation**

## 4. Objective
Scaffold a new, standalone TypeScript web application (`noorheroes-account-portal`, distinct from `noorheroes-admin`) whose router defines exactly the 23 routes in PRD §1.18, whose `apiClient` is structurally incapable of calling any child-scoped or purchase-initiation endpoint, and whose shared components (`StepUpModal`, "Manage on Mobile" guidance pattern, `SessionContext`) are built once here and reused identically by every subsequent screen sub-feature.

## 5. Business Requirements
- §6.1/§6.2: "A modern web framework... TypeScript... the application's router defines only these routes — there is no catch-all or wildcard route capable of resolving to a child-data or purchase-flow page."
- §6.4: "no global state container in this codebase ever holds child-scoped data."
- §6.5: "A shared `apiClient` wrapper restricts its own configured base-route set to the explicit allowlist — even at the frontend code level, there is no helper function exposing a child-scoped or purchase-initiation call."
- §2.1: Web-Specific Design System Extensions — Responsive Layout Grid, Step-Up Modal Pattern, "Manage on Mobile" Guidance Pattern, each "one shared component, not 5 different implementations."
- §7 Frontend AI Code-Generation Prompt, items 1–2, 5: exact-23-route router with a fabricated-route 404 test; strictly limited `apiClient` with a test asserting no child-scoped/purchase function exists; shared `StepUpModal` invoked identically across all sensitive actions.
- NFR "Performance": "Page load p95 < 1.5s... a low-complexity, low-interactivity surface by design."

## 6. Existing Architecture
This is explicitly a **new, separate application** from `noorheroes-admin`, not a route group within it — confirmed by the PRD's own framing ("a second, narrower client surface," "complementary relationship to the Mobile App," distinct domain `account.noorheroes.com` vs. the admin portal's own domain) and by this project's clarified scoping decision that the Parent Web Portal and the NextJS Admin Portal are two separate deployable apps. It reuses `noorheroes-admin`'s **tooling conventions** (Next.js App Router, TypeScript, TanStack Query v5, Zod, the layered UI → Hook → Repository → `apiClient` → API architecture documented in `NEXT-JS-INSTRUCTIONS.md`) and its **design-token package** (Dual-User Design Rule), but is its own codebase, its own deployment, and its own `apiClient` instance scoped to a different, narrower allowlist than the admin portal's.

**Flagged, not guessed:** `NEXT-JS-INSTRUCTIONS.md` documents only `noorheroes-admin`; no equivalent core-architecture document exists yet for this new Parent Web Portal codebase. This sub-feature's Task 01 must confirm the exact shared design-token package name/location and the repository/monorepo structure (new standalone repo vs. a new package within an existing monorepo) before scaffolding, rather than assuming either.

## 7. Existing Code to Reuse
- The shared design-token package consumed by `noorheroes-admin` (per `NEXT-JS-INSTRUCTIONS.md` §1's "Backend-Driven Localization" and the Dual-User Design Rule referenced throughout the PRD) — exact package name/location to be confirmed (Task 01).
- `noorheroes-admin`'s architectural pattern as a structural reference only (`BaseResourceClient`, `apiClient` HTTP boundary, Zod schema validation, `useTranslation()`/`useFormatters()`) — reused as a pattern to replicate in this new codebase, not as shared runtime code, unless the platform's actual monorepo structure allows genuine package sharing (confirm in Task 01).
- `parseApiError`, `logger`/`redact()` patterns from `noorheroes-admin` — replicated (or shared, if monorepo structure allows) for consistent error handling and PII-safe logging.

## 8. Files to Create
- `noorheroes-account-portal/src/app/layout.tsx` — root layout, design-token/theme provider.
- `noorheroes-account-portal/src/app/(portal)/router-config.ts` — the exact 23-route definition, no wildcard.
- `noorheroes-account-portal/src/shared/api/api-client.ts` — scope-restricted HTTP boundary.
- `noorheroes-account-portal/src/shared/api/allowed-endpoints.ts` — the explicit, code-level endpoint allowlist mirroring B-01/B-02.
- `noorheroes-account-portal/src/shared/context/session-context.tsx` — `SessionContext` provider.
- `noorheroes-account-portal/src/shared/components/step-up-modal.tsx`
- `noorheroes-account-portal/src/shared/components/manage-on-mobile-card.tsx`
- `noorheroes-account-portal/src/shared/components/portal-shell.tsx` — sidebar/top-nav layout shell.
- `noorheroes-account-portal/src/shared/hooks/use-offline-status.ts`
- `noorheroes-account-portal/src/shared/analytics/analytics-client.ts` — wrapper tagging `client_surface: web_portal`.
- `noorheroes-account-portal/tests/routing/no-wildcard-route.test.ts`
- `noorheroes-account-portal/tests/api/api-client-scope.test.ts`
- `noorheroes-account-portal/tests/routing/full-route-crawl.test.ts`

## 9. Files to Modify
None — this is a new application; there are no pre-existing files to modify.

## 10. Backend Requirements
Depends on B-01 (CORS/origin allowlist), B-02 (route-capability middleware), B-03 (step-up parity endpoints) being live before this shell's `apiClient` and `StepUpModal` can be integration-tested end-to-end; can be scaffolded and unit-tested in isolation before those land.

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- **Router:** Define exactly the 23 routes from PRD §1.18 (Login/OTP, Portal Account Home, Account & Security, Password/PIN Reset, Devices & Sessions, Device Revocation Confirmation, Subscription & Invoices, Invoice Detail, Cancellation Confirmation, Restore-Purchase Guidance, Consent & Privacy, Consent Detail, Withdraw Consent Confirmation, Data Export Request, Export Status Tracking, Parent Deletion Request, Deletion Warning, Deletion Confirmation, Deletion Status/Countdown, Support Center, FAQ Search, Contact Support Form, Ticket History/Detail). No `[...catchAll]` or wildcard segment exists anywhere in the App Router route tree.
- **`apiClient`:** exposes only named functions for the B-01 §10 allowlisted endpoints; no generic `request(path)` escape hatch that could reach an arbitrary path — every call site is a named, typed function (e.g. `requestOtp()`, `verifyOtp()`, `getSubscription()`), never a raw path string constructed by a caller.
- **`SessionContext`:** holds `parentId`, session-freshness state, step-up-elevation state; explicitly typed to make it structurally impossible to add a `childId` or child-scoped field without a deliberate, reviewed type change.
- **`StepUpModal`:** a single shared component (OTP/password/passkey per B-03's chosen mechanism) invoked identically by N-04 (PIN/password reset), N-05 (device revoke), N-06 (cancel subscription), N-07 (withdraw consent), N-08 (export request), N-09 (deletion request) — never a per-screen reimplementation.
- **`ManageOnMobileCard`:** the shared "icon + short text + Open the NoorHeroes app" component, used by N-06's Subscription screen wherever a purchase/upgrade/restore action would otherwise appear.
- **`PortalShell`:** sidebar/top-nav layout across the 8 sections, responsive per §1.13/§2.1.
- **Offline handling:** `useOfflineStatus()` connectivity listener, disabling action buttons and showing a banner when offline (§1.14).
- **Analytics wrapper:** tags every event with `client_surface: web_portal` per §6.6.
- **Graceful degradation:** core account-view screens remain functional with JavaScript disabled or on older browsers, per Edge Case 7.

## 13. API Contract
Not applicable directly — this sub-feature builds the `apiClient` infrastructure that N-03–N-10 populate with calls against each owning feature's already-defined contract (A.1, B-03, C.21/C.23, C.24, C.25, C.26).

## 14. Database Requirements
Not applicable (frontend).

## 15. Validation
Router-level: any URL not matching one of the 23 defined routes resolves to a standard Next.js 404 — verified structurally (no catch-all exists to intercept it) and by test.

## 16. Authentication
`SessionContext` reflects the authenticated parent's session state, sourced from N-03's login flow; unauthenticated access to any protected route redirects to Login/OTP.

## 17. Authorization
Not applicable at this layer beyond session-authentication gating — per-action step-up authorization is enforced by `StepUpModal` + each calling screen's backend endpoint (B-03's elevation marker check).

## 18. Error Handling
| Scenario | System Behavior |
|---|---|
| Navigation to a fabricated/child-data-resembling URL | Standard 404 (Edge Case 3) |
| `apiClient` call attempted against a non-allowlisted path | Structurally impossible — no such function exists to call (compile-time prevention, not just runtime rejection) |
| Session expires mid-form | In-progress form data preserved locally where reasonably feasible; fresh login prompted (Edge Case 5) |
| Offline mid-session | Connectivity banner shown, action buttons disabled (§1.14) |
| JavaScript disabled / unusual browser | Graceful degradation for core account-view screens (Edge Case 7) |

## 19. Offline First
Standard web offline-detection only (a connectivity listener); this is not an offline-first architecture like the KMP app's — mutating actions require connectivity, banner shown when offline.

## 20. Local Data
No persistent local storage of session/auth data in `localStorage`/`sessionStorage` (consistent with `noorheroes-admin`'s "Zero Token Persistence in Browser Storage" principle, reused here) — access tokens live in memory (`SessionContext`), refresh via `httpOnly` cookies per the same pattern `noorheroes-admin` already establishes.

## 21. Localization
Full EN/HI/AR/UR support via the shared design-token/localization package; RTL layout mirroring for Arabic/Urdu across the entire shell (sidebar, modals, forms).

## 22. RTL
Full RTL layout support built into `PortalShell`, `StepUpModal`, and `ManageOnMobileCard` from the start, since every subsequent screen composes on top of these shared components.

## 23. Analytics
Analytics wrapper (`analytics-client.ts`) fires all events in PRD §1.19 tagged `client_surface: web_portal`; this sub-feature builds the wrapper, individual screens (N-03–N-10) fire their specific events through it.

## 24. Performance
Page load p95 < 1.5s target (§1.8 NFR) applies platform-wide; shell must avoid unnecessary client-side JS for a "low-complexity, low-interactivity surface by design" — favor server components/SSR where the framework supports it for initial render, matching the low-interactivity design intent.

## 25. Security
- **Zero Token Persistence in Browser Storage**, mirroring `noorheroes-admin`'s established principle — access tokens in memory only.
- The `apiClient`'s named-function-only design (no raw path escape hatch) is this sub-feature's most important structural security property — it is the frontend-code-level third layer of the defense-in-depth model alongside B-01 (gateway) and B-02 (application middleware).
- `SessionContext`'s type-level exclusion of any child-scoped field is a compile-time guardrail, not just a runtime one.

## 26. Library Requirements
Next.js App Router, TypeScript, TanStack Query v5, Zod — matching `noorheroes-admin`'s established stack per `NEXT-JS-INSTRUCTIONS.md` §1, for consistency and shared team familiarity, confirmed rather than assumed as the mandated stack for this new codebase (Task 01).

## 27. Testing
- Unit: `apiClient` module — enumerate its exported functions and assert none corresponds to a child-scoped or purchase-initiation endpoint (§7 item 2's required test).
- Integration/E2E: navigation to a fabricated child-data-resembling route (e.g. `/children/123/progress`) returns a standard 404 (§7 item 1's required test).
- Integration/E2E: full crawl of all 23 defined routes confirms none resolve to child data or a purchase flow (§6.10's required test).
- Unit: `SessionContext` type definition contains no child-scoped field (static type-level check, e.g. a compile-time assertion test).
- Integration: `StepUpModal` renders and behaves identically regardless of which calling screen invokes it (shared-component parity test, foundational for N-04–N-09's individual step-up tests).
- Integration: offline banner appears and action buttons disable correctly when connectivity drops.

## 28. Documentation
Establish a project README explaining this is a standalone application (not a route group of `noorheroes-admin`), documenting the shared design-token package dependency, the `apiClient`'s named-function-only convention, and the 23-route closed router as a hard architectural invariant every future contributor must preserve.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm Scaffolding Decisions (blocking)**
- **Objective:** Confirm the shared design-token package's exact name/location, the repository structure (new standalone repo vs. monorepo package), and the exact web framework/tooling versions to match `noorheroes-admin`'s conventions.
- **Why This Is Required:** No core-architecture document exists yet for this new codebase; rule 30 prohibits inventing infrastructure decisions.
- **Definition of Done:** Written confirmation obtained.

**Task 02 — Scaffold the Application**
- **Dependencies:** Task 01.
- **Definition of Done:** New Next.js/TypeScript app builds and runs locally, consuming the confirmed design-token package.

**Task 03 — Define the Exact 23-Route Router**
- **Files to Create:** `router-config.ts`, App Router page stubs for each of the 23 screens (populated fully by N-03–N-10).
- **Tests:** no-wildcard-route test, full-route-crawl test.

**Task 04 — Build the Scope-Restricted `apiClient`**
- **Files to Create:** `api-client.ts`, `allowed-endpoints.ts`.
- **Dependencies:** B-01's finalized allowlist.
- **Tests:** the named-function-only scope test (§7 item 2).

**Task 05 — Build `SessionContext`**
- **Files to Create:** `session-context.tsx`.
- **Definition of Done:** Type-level exclusion of child-scoped fields verified.

**Task 06 — Build Shared `StepUpModal`**
- **Files to Create:** `step-up-modal.tsx`.
- **Dependencies:** B-03's step-up OTP endpoints.

**Task 07 — Build `ManageOnMobileCard` and `PortalShell`**
- **Files to Create:** `manage-on-mobile-card.tsx`, `portal-shell.tsx`.

**Task 08 — Offline Detection and Analytics Wrapper**
- **Files to Create:** `use-offline-status.ts`, `analytics-client.ts`.

**Task 09 — Graceful Degradation Pass**
- **Objective:** Verify core account-view screens remain usable with JS disabled, per Edge Case 7.

**Task 10 — Full Test Suite & Documentation**

## 30. Definition of Done
A standalone, TypeScript Parent Web Portal application exists with an exactly-23-route closed router, a structurally scope-restricted `apiClient`, and shared `StepUpModal`/`ManageOnMobileCard`/`SessionContext`/`PortalShell` components ready for N-03–N-10 to build screens against — with zero wildcard routes and zero child-scoped or purchase-initiation capability anywhere in the codebase, verified by automated tests.

## 31. Final Verification Checklist
- [ ] Task 01's scaffolding decisions confirmed in writing before implementation began
- [ ] Router defines exactly 23 routes, no wildcard/catch-all
- [ ] `apiClient` exposes only named functions matching B-01's allowlist — no raw-path escape hatch
- [ ] `SessionContext` contains no child-scoped field (type-level verified)
- [ ] `StepUpModal` is a single shared component ready for reuse by N-04–N-09
- [ ] `ManageOnMobileCard` ready for reuse by N-06
- [ ] Zero Token Persistence in Browser Storage principle followed
- [ ] Full localization and RTL foundation in place
- [ ] Full route-crawl and apiClient-scope tests pass
