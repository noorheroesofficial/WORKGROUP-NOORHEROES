# N-05 — Locale Chain Configuration & Deprecation

## 1. Feature Context
The configuration screen for per-locale fallback ordering, plus the deliberately higher-friction confirmation for the rare, significant decision to deprecate a locale entirely — distinct from a routine deactivation.

## 2. Parent Feature
E.34 — Localization Management

## 3. Sub-feature
2.5 Locale Chain Configuration & Deprecation (ID: **N-05**)

## 4. Objective
Build the Locale Chain Configuration screen and Locale Deprecation Confirmation modal against B-04, surfacing cycle-rejection errors clearly and framing deprecation as distinct from routine deactivation.

## 5. Business Requirements
- §1.18 screens 9, 13: Locale Chain Configuration, Locale Deprecation Confirmation.
- FR-9: locale-chain fallback explicit and ordered per locale.
- Edge Case 5: deprecating/deactivating a locale entirely is a rare, significant decision requiring its own careful, explicit handling distinct from routine string-level fallback.

## 6. Existing Architecture
`src/features/locale-chain-config/` module.

## 7. Existing Code to Reuse
- `src/shared/components/confirmation-dialog.tsx::ConfirmationDialog`
- `src/shared/components/require-permission.tsx::RequirePermission`

## 8. Files to Create
- `src/app/(dashboard)/platform/locales/[code]/chain/page.tsx`
- `src/features/locale-chain-config/api/locale-chain-repository.ts`
- `src/features/locale-chain-config/hooks/use-locale-chain.ts`, `use-set-chain.ts`
- `src/features/locale-chain-config/components/chain-config-form.tsx`
- `src/features/locale-chain-config/components/locale-deprecation-confirmation.tsx` — distinct, higher-friction copy from routine deactivation

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `LOCALE_CHAIN.*` endpoints
- `src/shared/components/dashboard-shell.tsx` — nav item under "Platform" group

## 10. NextJS Requirements
- `ChainConfigForm`: fallback-locale selector, surfaces `422 SELF_REFERENTIAL_CHAIN`/`422 CYCLIC_CHAIN` errors from B-04 with clear, specific explanatory text (not a generic validation error).
- `LocaleDeprecationConfirmation`: explicitly distinct copy and confirmation friction from N-04's routine deactivation confirmation — states this is a significant, rare action affecting all users currently on that locale, requiring a typed confirmation (e.g., typing the locale code) rather than a single click, mirroring the platform's general higher-friction-for-higher-stakes-action pattern.

## 11. Required API
**Admin API** — B-04: `GET`/`PUT /v1/admin/locales/{code}/chain`.

## 12. Authentication / Authorization
`useAdminSession()` base auth; `RequirePermission permission="localization_manager"`.

## 13. Loading / Empty / Error States
Chain config loading state; cycle-rejection error states (self-reference vs. multi-hop, distinctly worded); deprecation confirmation typed-input validation.

## 14. Responsive UI / Accessibility
Deprecation confirmation's higher-friction typed-input step is fully keyboard-operable and clearly labeled.

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()`.

## 16. Security
Deprecation's higher-friction confirmation (typed locale-code entry, not a single click) is this screen's defining guarantee against accidental triggering of a rare, high-impact action — mandatory test confirms the deprecation action cannot fire without the correct typed confirmation matching the target locale code.

## 17. Testing
Unit: cycle-error-message mapping. UI: **mandatory** — locale deprecation requires typed-confirmation matching the locale code before the action can fire, distinct from N-04's simpler deactivation confirmation. Integration: full chain-configuration-save flow; cycle-rejection correctly surfaces specific error text; full deprecation-with-typed-confirmation flow.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schema & Add API Endpoints**
Objective: Chain-config schema. Files: `types/*.ts` (or inline), `api-endpoints.ts`. Tests: schema validation. Definition of Done: schema used by Task 03.

**Task 02 — Implement `LocaleChainRepositoryImpl`**
Objective: Repository for B-04's chain endpoints. Tests: mocked-fetch tests. Dependencies: Task 01. Definition of Done: tests pass.

**Task 03 — Implement `ChainConfigForm` with Cycle-Error Surfacing**
Objective: Distinct error messages for self-reference vs. multi-hop cycles. Dependencies: Task 02. Tests: cycle-error-mapping tests. Definition of Done: tests pass.

**Task 04 — Implement `LocaleDeprecationConfirmation` with Typed Confirmation**
Objective: Higher-friction confirmation requiring typed locale-code match. Dependencies: N-04's repository (shares the deactivate/deprecate action space). Tests: **mandatory** — action blocked without correct typed match. Definition of Done: test passes.

**Task 05 — Implement the Chain Configuration Page**
Objective: Compose form with loading/error states. Dependencies: Task 03. Tests: full-page smoke test. Definition of Done: test passes.

**Task 06 — Add Full Test Suite**
Objective: Complete coverage per §17, including the mandatory typed-confirmation test. Definition of Done: all green in CI.

**Task 07 — Final Code Review**
Objective: Confirm deprecation's friction is genuinely higher than routine deactivation's, not merely relabeled. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] Cycle-rejection errors (self-reference and multi-hop) surface with distinct, specific text
- [ ] Deprecation requires typed locale-code confirmation, not a single click — mandatory test passing
- [ ] Deprecation copy clearly distinguishes itself from routine deactivation
- [ ] `localization_manager` scope enforced

## 20. Definition of Done
Locale fallback chains are configured with clear cycle-error feedback, and locale deprecation — a rare, high-impact decision — is deliberately harder to trigger by accident than routine configuration changes.
