# N-03 — Consent Audit Viewer

## 1. Feature Context
Compliance staff's read-only window into the consent ledger: search by family ID or masked identifier, view the full immutable history. Zero mutation UI exists on this page by design — it mirrors B-08's zero-update/delete backend guarantee.

## 2. Parent Feature
Feature A.1 — Splash, Language Selection, Authentication & Onboarding

## 3. Sub-feature
3.3 Consent Audit Viewer (ID: **N-03**)

## 4. Objective
Build a search-and-view page against `GET /admin/v1/consent/audit`, gated behind `compliance_read` permission and step-up MFA re-auth, with zero update/delete controls anywhere on the page.

## 5. Business Requirements
- Consent Audit Viewer: search by masked parent identifier/family ID, view full consent history (immutable ledger) — never shows raw plaintext identifiers, only masked.
- CRUD permissions: Consent Audit = Read-only, no Update/Delete role exists for any admin role — this must be true of the UI too, not just the API.
- §12.5: requires `compliance_read` role + step-up MFA re-auth if session older than 15 minutes.

## 6. Existing Architecture
`src/features/consent-audit/` module; `RequirePermission` for `compliance_read` gating; `useElevatedSession()` for the step-up MFA requirement (existing hook, same one used in the `DeleteFamilyButton` high-risk-action example in the architecture doc — reused here for a *read*-sensitivity reason rather than a destructive-action reason, which is a slightly different use case worth noting in code comments).

## 7. Existing Code to Reuse
- `src/features/auth/hooks/use-elevated-session.ts::useElevatedSession()`
- `src/shared/components/require-permission.tsx::RequirePermission`
- `src/shared/components/search-bar.tsx::SearchBar`
- `src/shared/components/empty-state.tsx::EmptyState`
- `src/shared/hooks/use-debounced-value.ts`

## 8. Files to Create
- `src/app/(dashboard)/consent-audit/page.tsx`
- `src/features/consent-audit/api/consent-audit-repository.ts` — `ConsentAuditRepositoryImpl.search(query)`
- `src/features/consent-audit/hooks/use-consent-audit-search.ts`
- `src/features/consent-audit/components/consent-timeline.tsx` — read-only timeline rendering
- `src/features/consent-audit/components/step-up-gate.tsx` — wraps the page content, prompts for fresh OTP if session elevation is stale/absent
- `src/features/consent-audit/types/consent-record.ts` — Zod schema

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `CONSENT_AUDIT.SEARCH`
- `src/shared/components/dashboard-shell.tsx` — nav item gated by `compliance_read`

## 10. NextJS Requirements
- Page wraps its content in both `RequirePermission permission="compliance_read"` (existing pattern) and a `StepUpGate` component built on `useElevatedSession()` — if `hasElevation` is false or stale (>15 min, mirroring B-08's server-side check — the client enforces this as UX, the server is the actual authority per §12.5), render an OTP re-entry prompt (via `requestElevation(otp)`) before rendering search results.
- Search input requires at least one of `family_id`/`identifier` (mirrors B-08's server-side requirement) — disable the search action until one is provided, do not allow an unfiltered full search.
- `ConsentTimeline` renders ordered ledger entries (version, decision, region, timestamp) — **zero** edit/delete buttons, icons, or affordances anywhere in this component, by design, permanently.
- Masked identifiers only — the component must not even have a prop slot for a raw identifier value, structurally preventing an accidental future regression.

## 11. Required API
- `GET /admin/v1/consent/audit?family_id=&identifier=` (B-08) — Auth: `compliance_read` + step-up MFA

## 12. Authentication / Authorization
`useAdminSession()` for base auth; `RequirePermission permission="compliance_read"` for the page gate; `useElevatedSession()` for the step-up requirement specifically on this page.

## 13. Loading / Empty / Error States
Loading during search; empty state for no-match search results (distinct copy from "no search performed yet" initial state); error state with retry, including a specific message if the step-up elevation itself fails (invalid OTP) distinct from a general API error.

## 14. Responsive UI / Accessibility
Timeline is a simple ordered list — must be fully readable/navigable via screen reader, no critical information conveyed by color alone (decision granted/denied needs a text label, not just a colored dot).

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()` usage; timeline reads correctly in RTL (chronological order semantics preserved, just visual direction mirrored).

## 16. Security
This is the highest-sensitivity read surface in the entire admin feature set — the final code review must specifically verify zero mutation affordances exist anywhere in this module's component tree, not just the obvious page-level actions.

## 17. Testing
Unit: zero-mutation-controls-rendered assertion (search the rendered component tree for any button/icon implying edit/delete and assert none exist, under every permission/data state); step-up-gate blocks content until elevation is fresh; search requires at least one parameter.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schema & Add API Endpoint**
Objective: Response contract matching B-08's masked-only shape. Files to Create/Modify: `types/consent-record.ts`, `api-endpoints.ts`. Tests: schema rejects a payload containing an unexpected raw-identifier-shaped field (defensive test). Definition of Done: schema physically cannot represent a raw identifier value.

**Task 02 — Implement `ConsentAuditRepositoryImpl.search()`**
Objective: Repository wrapping `apiClient.get()` with the search params. Follow: existing repository conventions. Tests: mocked-fetch tests, at-least-one-param-required test. Dependencies: Task 01. Definition of Done: repository itself refuses an unfiltered call (defense in depth alongside the UI-level disable).

**Task 03 — Implement `StepUpGate` Component**
Objective: Wrap page content, require fresh `useElevatedSession()` elevation before rendering search UI. Follow: the `DeleteFamilyButton` example's `requestElevation(otp)` pattern from the architecture doc, adapted for a read-gate rather than a single destructive action. Tests: renders OTP prompt when elevation is absent/stale, renders content when fresh. Definition of Done: content is provably unreachable without a fresh elevation token.

**Task 04 — Implement `useConsentAuditSearch` Hook**
Objective: React Query hook, only fires when at least one search param is present (disabled query until then). Follow: existing query-hook conventions. Tests: covered by Task 05. Dependencies: Task 02. Definition of Done: no query fires on page load before a search is submitted.

**Task 05 — Implement `ConsentTimeline` (Zero Mutation Affordances)**
Objective: Read-only ordered list rendering. Follow: no interactive edit/delete elements, ever. Tests: the explicit zero-mutation-controls test per §17. Dependencies: Task 04. Definition of Done: test passes by asserting an absence, not just a positive rendering check.

**Task 06 — Implement the Page**
Objective: Compose `RequirePermission` + `StepUpGate` + `SearchBar` + `ConsentTimeline` + states. Files to Create: `page.tsx`. Dependencies: Tasks 03–05. Definition of Done: full page smoke test against a mocked API and mocked elevation state.

**Task 07 — Add Full Test Suite**
Objective: Complete coverage per §17. Definition of Done: all green in CI.

**Task 08 — Final Code Review**
Objective: Exhaustive search of the module's component tree for any mutation affordance; confirm masked-only data flow end-to-end; confirm step-up gate cannot be bypassed via direct navigation. Definition of Done: checklist in §19 checked, with the zero-mutation assertion specifically called out as reviewed.

## 19. Final Verification Checklist
- [x] Zero edit/delete/update UI affordances anywhere in this module — verified by an explicit negative-assertion test
- [x] Raw/plaintext identifiers cannot be represented by any type or component prop in this module
- [x] Step-up MFA gate blocks all content until a fresh elevation exists
- [x] Search requires at least one parameter, enforced at both UI and repository layers
- [x] Page gated behind `compliance_read` via `RequirePermission`
- [x] Empty-search-result and no-search-yet states are visually/textually distinct

## 20. Definition of Done
The Consent Audit Viewer is live, reads from B-08, structurally incapable of exposing raw identifiers or offering any mutation, and correctly enforces both permission-based and step-up-MFA-based access control. **(STATUS: IMPLEMENTED & VERIFIED)**

### 20.1 Implemented Artifacts & Verified Architecture
- **Route Segment & Layout Boundaries:**
  - Route Page: `src/app/(dashboard)/consent-audit/page.tsx` (gated with `<RequirePermission permission="compliance_read">`)
  - Loading Boundary: `src/app/(dashboard)/consent-audit/loading.tsx` (skeleton loading state preventing layout shift)
  - Error Boundary: `src/app/(dashboard)/consent-audit/error.tsx` (Client component with `reset()` action and Sentry/logger integration)
- **Feature Module (`src/features/consent-audit/`):**
  - Validation Schemas: `schemas/consent-audit.schema.ts` (`consentAuditItemSchema`, `consentAuditSearchResponseSchema`, `consentAuditSearchParamsSchema` with single-parameter refinement and `.strict()` defensive rejection of raw PII)
  - Data Types: `types.ts` (`ConsentAuditItem`, `ConsentAuditSearchResponse`, `ConsentAuditSearchParams`, `IConsentAuditRepository`)
  - Repository Layer: `api/consent-audit.repository.ts` (`ConsentAuditRepositoryImpl.search()` with defense-in-depth parameter validation and `X-Elevated-Token` forwarding)
  - TanStack Query Hook: `hooks/use-consent-audit-search.ts` (`useConsentAuditSearch`) with 30s `staleTime`, 5m `gcTime`, and idle-before-search invariant
  - UI Components:
    - `components/consent-audit-viewer.tsx`: 5-state UI orchestrator (Initial Prompt, Loading Skeleton, Populated Timeline with Search Summary Bar, EmptyState, and Error State with retry)
    - `components/step-up-gate.tsx`: Step-Up MFA challenge (<15 min freshness per PRD §12.5) matching `03-Two-Factor Verification.png`, 6-digit TOTP validation, in-memory token handling, and session countdown timer
    - `components/consent-timeline.tsx`: Accessible `<ol>` ordered list with chronological node indicators, status badges for privacy directives (`personalization_consent`, `voice_consent`, `marketing_consent`), policy versions (`terms_version`, `privacy_version`, `child_data_version`), provenance metadata, and permanent zero-mutation UI guarantees
  - Feature Barrel: `index.ts` exporting public surface
- **API Registry & Navigation Integration:**
  - Central Registry: `src/shared/constants/api-endpoints.ts` (`API_ENDPOINTS.CONSENT_AUDIT.SEARCH = "/v1/admin/consent/audit"`)
  - Sidebar Navigation: `src/shared/constants/nav-items.ts` (`/consent-audit` with `permission: "compliance_read"`)
- **Localization (i18n):**
  - Full 41/41 translation key parity across English (`en`), Arabic (`ar` with RTL), Urdu (`ur` with RTL), and Hindi (`hi`)
- **Automated Verification:**
  - `tests/consent-audit-analytics.test.ts`: 12/12 passing tests (schema validation, strict unmasked PII rejection, search param validation, repository URL/header generation)
  - `tests/consent-audit-components.test.tsx`: 16/16 passing tests (StepUpGate challenge, 5-state rendering, zero-mutation DOM assertion, permission gating, accessible labels)
  - `e2e/consent-audit.spec.ts`: 6 E2E Playwright scenarios (unauthenticated redirect, permission gating, step-up MFA challenge, TOTP elevation, zero-mutation assertion, distinct EmptyState)
  - `tests/contract/schema-drift.test.ts`: Verified zero schema drift against OpenAPI contracts
  - `tests/navigation-links.test.ts`: Route mapping verified
  - `tests/architecture/*.test.mjs`: 69/69 passing tests
  - 0 lint errors (`npm run lint`), 0 type errors (`npm run type-check`)
