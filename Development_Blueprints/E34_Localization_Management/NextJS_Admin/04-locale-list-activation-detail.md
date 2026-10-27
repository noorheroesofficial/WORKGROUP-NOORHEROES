# N-04 — Locale List & Locale Activation Detail

## 1. Feature Context
The activation control surface whose single most important rule is that it never second-guesses the server: the "Activate" button's enabled/disabled state and explanatory text come entirely from B-03's dual-gate response, with zero independent client-side estimate of readiness.

## 2. Parent Feature
E.34 — Localization Management

## 3. Sub-feature
2.4 Locale List & Locale Activation Detail (ID: **N-04**)

## 4. Objective
Build the Locale List, Locale Activation Detail, and Locale Activation Blocked State screens against B-03, with the "Activate" action's disabled-state and explanatory copy derived entirely from the server's structured dual-gate response.

## 5. Business Requirements
- §1.18 screens 6–8: Locale List, Locale Activation Detail, Locale Activation Blocked State.
- §6.4: the "Activate" button's disabled-state derives entirely from the server's dual-gate check response, never a client-side-only coverage estimate.
- §7 Frontend AI prompt item 1: disabled-state and tooltip text derive entirely from the server's `{coverage_ok, review_complete}` structured response — a test confirms the UI never independently estimates or overrides this.

## 6. Existing Architecture
`src/features/locale-management/` module.

## 7. Existing Code to Reuse
- `src/shared/components/require-permission.tsx::RequirePermission`
- `src/shared/components/data-table.tsx::DataTable`
- N-02's `LocaleCoverageRow` (linked from, not duplicated)

## 8. Files to Create
- `src/app/(dashboard)/platform/locales/page.tsx`
- `src/app/(dashboard)/platform/locales/[code]/page.tsx`
- `src/features/locale-management/api/locale-activation-repository.ts`
- `src/features/locale-management/hooks/use-locale-list.ts`, `use-activation-gate-check.ts`, `use-activate-locale.ts`
- `src/features/locale-management/components/activate-button.tsx` — server-derived disabled state
- `src/features/locale-management/components/activation-blocked-explanation.tsx`
- `src/features/locale-management/types/locale-activation.ts` — Zod schema matching `{coverage_ok, review_complete}`

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `LOCALE_ACTIVATION.*` endpoints
- `src/shared/components/dashboard-shell.tsx` — nav item under "Platform" group

## 10. NextJS Requirements
- `ActivateButton`: `disabled = !gateCheck.coverage_ok || !gateCheck.review_complete` computed directly from the server's structured response — no separate client-side percentage comparison against a locally-held threshold value anywhere in this component's logic.
- `ActivationBlockedExplanation`: renders distinct explanatory text per failing gate (coverage vs. review-completeness vs. both), sourced from the same server response, linking to N-02's dashboard (coverage gap) or the review queue (review-completeness gap) as appropriate.
- Locale List shows current + future-ready (schema-ready but not yet activated) locales in a single view, per §1.18 screen 6.

## 11. Required API
**Admin API** — B-03: `GET /v1/admin/locales/coverage` (feeding the gate-check display), `POST /v1/admin/locales/{code}/activate`, `POST /v1/admin/locales/{code}/deactivate`.

## 12. Authentication / Authorization
`useAdminSession()` base auth; `RequirePermission permission="localization_manager"`.

## 13. Loading / Empty / Error States
Gate-check loading state; `409 COVERAGE_BELOW_THRESHOLD`/`409 REVIEW_INCOMPLETE` mapped to the blocked-state explanation, not a generic error toast; activation-success state.

## 14. Responsive UI / Accessibility
Blocked-state explanation programmatically associated with the disabled button (`aria-describedby`), not conveyed by disabled-styling alone.

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()`.

## 16. Security
The server-derived-only gate check is this screen's defining guarantee — mandatory test confirms that even if a client-side coverage percentage were somehow computable from other data on the page, the `ActivateButton`'s disabled state does not use it, using only the dedicated gate-check response fields.

## 17. Testing
Unit: `ActivateButton` disabled-state derivation logic. UI: **mandatory** — disabled-state and explanatory text change correctly across all four combinations of `{coverage_ok, review_complete}` fixture values, confirming no independent client estimate overrides the server response. Integration: full blocked-then-improving-then-successful-activation flow as fixture gate state changes.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schema & Add API Endpoints**
Objective: `locale-activation.ts` schema matching the dual-gate response shape. Files: `types/locale-activation.ts`, `api-endpoints.ts`. Tests: schema validation. Definition of Done: schema used by Task 03.

**Task 02 — Implement `LocaleActivationRepositoryImpl`**
Objective: Repository for B-03's three endpoints. Tests: mocked-fetch tests. Dependencies: Task 01. Definition of Done: tests pass.

**Task 03 — Implement `ActivateButton` with Server-Only Gate Derivation**
Objective: Disabled state computed exclusively from server response fields. Dependencies: Task 02. Tests: **mandatory** — four-combination gate-state test. Definition of Done: test passes.

**Task 04 — Implement `ActivationBlockedExplanation`**
Objective: Gate-specific explanatory text with links to relevant screens. Dependencies: Task 03. Tests: per-gate-failure copy test. Definition of Done: test passes.

**Task 05 — Implement the Locale List and Activation Detail Pages**
Objective: Compose all components with loading/empty/error states. Dependencies: Tasks 03–04. Tests: full-page smoke tests. Definition of Done: tests pass.

**Task 06 — Add Full Test Suite**
Objective: Complete coverage per §17, including the mandatory four-combination test. Definition of Done: all green in CI.

**Task 07 — Final Code Review**
Objective: Confirm zero independent client-side gate estimate exists anywhere in this module. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] "Activate" button disabled-state derives exclusively from the server's dual-gate response — mandatory four-combination test passing
- [ ] Blocked-state explanation correctly distinguishes coverage vs. review-completeness failures
- [ ] Locale List shows both current and future-ready locales
- [ ] `localization_manager` scope enforced

## 20. Definition of Done
Locale activation in the UI is provably a thin, honest reflection of the server's dual-gate decision, with zero risk of the interface ever suggesting a locale is ready when the backend's actual guarantees say otherwise.
