# N-01 — User Search & Parent Account Detail

## 1. Feature Context
The primary support workspace: search by any of four identifiers, then a masked-by-default parent account detail view bundling session management, entitlement inspection, support-safe metadata correction, account recovery initiation, and the entry point into the unmask-request flow.

## 2. Parent Feature
E.32 — User Management & Child Safety View

## 3. Sub-feature
2.1 User Search & Parent Account Detail (ID: **N-01**)

## 4. Objective
Build the User Search screen and Parent Account Detail screen against B-01/B-02/B-04/B-05/B-06, rendering every PII field through the server's masked/unmasked response shape without any client-side masking decision.

## 5. Business Requirements
- Search by parent ID, family ID, subscription ID, or support case ID; masked result list.
- Parent Account Detail: masked profile fields, session list with revoke, entitlement inspector (read-only), support-safe metadata correction form (server-schema-driven allowlist), account recovery initiation, unmask-request entry point.
- No component in this screen independently decides whether a field is masked — rendering is driven entirely by what the server response contains.

## 6. Existing Architecture
`src/features/user-search/` and `src/features/parent-account-detail/` modules, following the Admin Portal's dense professional-tool visual register (E.28 §2.1).

## 7. Existing Code to Reuse
- `src/shared/components/require-permission.tsx::RequirePermission`
- `src/shared/components/data-table.tsx::DataTable` (search results)
- `src/shared/components/confirmation-dialog.tsx::ConfirmationDialog` (session revoke, recovery initiation)
- `src/shared/hooks/use-admin-session.ts::useAdminSession`

## 8. Files to Create
- `src/app/(dashboard)/users/search/page.tsx`
- `src/app/(dashboard)/users/[parentId]/page.tsx`
- `src/features/user-search/api/user-search-repository.ts`
- `src/features/parent-account-detail/api/parent-account-repository.ts`
- `src/features/user-search/hooks/use-user-search.ts`
- `src/features/parent-account-detail/hooks/use-parent-detail.ts`, `use-sessions.ts`, `use-entitlements.ts`, `use-metadata-correction.ts`, `use-recovery-initiation.ts`
- `src/features/parent-account-detail/components/masked-field.tsx` — renders exactly what the server sends, no client-side mask logic
- `src/features/parent-account-detail/components/session-list-panel.tsx`
- `src/features/parent-account-detail/components/entitlement-inspector-panel.tsx` — read-only
- `src/features/parent-account-detail/components/metadata-correction-form.tsx`
- `src/features/parent-account-detail/components/account-recovery-action.tsx`
- `src/features/parent-account-detail/components/unmask-request-entry-point.tsx`
- `src/features/user-search/types/user-search.ts`, `src/features/parent-account-detail/types/parent-account.ts` — Zod schemas

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `USER_SEARCH.*`, `PARENT_ACCOUNT.*` endpoints
- `src/shared/components/dashboard-shell.tsx` — nav item under new "Users" group

## 10. NextJS Requirements
- `MaskedField`: a single, shared rendering component that displays exactly the string the server returns for a field — it contains no logic that decides masked-vs-unmasked; that decision was already made server-side by B-02. All PII-bearing fields on this screen route through this one component (structural consistency, no per-field ad-hoc rendering).
- `MetadataCorrectionForm`: renders fields strictly from the server-provided allowlist schema (B-05) — never a client-hardcoded field list, so the two stay in sync automatically.
- `EntitlementInspectorPanel`: read-only by construction — no input/save affordance anywhere in this component.
- `UnmaskRequestEntryPoint`: a button/link that navigates to N-03's submission form, pre-filled with this record's scope.

## 11. Required API
**Admin API** — B-01: `GET /v1/admin/users/search`. B-02 (indirectly, via masked response shape). B-04: sessions/verification/entitlements endpoints. B-05: `PATCH /v1/admin/users/{id}/metadata`. B-06: `POST /v1/admin/users/{id}/recovery/initiate`.

## 12. Authentication / Authorization
`useAdminSession()` base auth; `RequirePermission permission="support"` for the entire module.

## 13. Loading / Empty / Error States
Search: loading skeleton, "No results" empty state, validation error for zero/multiple identifiers. Detail: loading skeleton, session-revoke confirmation, metadata-correction validation errors, recovery-initiation rate-limit error state.

## 14. Responsive UI / Accessibility
Masked-field placeholders announced to screen readers as "masked" (not read as literal placeholder characters); all actions keyboard-operable.

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()`.

## 16. Security
`MaskedField`'s single-source-of-truth rendering is this screen's defining guarantee — mandatory test confirms the component renders the server's literal response value with zero independent mask/unmask branching logic.

## 17. Testing
Unit: `MaskedField` renders server value verbatim (no client logic). UI: **mandatory** — a mock masked-response fixture renders placeholder text, a mock unmasked-response fixture renders real values, both purely from server data. Integration: full search → select result → detail-loads-masked → metadata-correction-submits flow.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schemas & Add API Endpoints**
Objective: `user-search.ts`, `parent-account.ts` schemas. Files: `types/*.ts`, `api-endpoints.ts`. Tests: schema validation. Definition of Done: schemas used by Tasks 03+.

**Task 02 — Implement Repositories**
Objective: `UserSearchRepositoryImpl`, `ParentAccountRepositoryImpl`. Tests: mocked-fetch tests. Dependencies: Task 01. Definition of Done: tests pass.

**Task 03 — Implement `MaskedField`**
Objective: Server-response-verbatim rendering, zero client-side mask logic. Dependencies: Task 02. Tests: **mandatory** — masked/unmasked fixture rendering test. Definition of Done: test passes.

**Task 04 — Implement Search Screen**
Objective: Search form + `DataTable` results using `MaskedField`. Dependencies: Task 03. Tests: search-flow tests. Definition of Done: tests pass.

**Task 05 — Implement `SessionListPanel` and `EntitlementInspectorPanel`**
Objective: Session revoke action; read-only entitlement display. Dependencies: Task 02. Tests: revoke-confirmation test, read-only-no-input-affordance test. Definition of Done: tests pass.

**Task 06 — Implement `MetadataCorrectionForm`**
Objective: Server-schema-driven allowlist form. Dependencies: Task 02. Tests: unknown-field-never-rendered test. Definition of Done: test passes.

**Task 07 — Implement `AccountRecoveryAction` and `UnmaskRequestEntryPoint`**
Objective: Recovery initiation with confirmation; navigation to N-03 pre-filled with scope. Dependencies: Task 02. Tests: navigation-with-correct-scope test. Definition of Done: test passes.

**Task 08 — Implement the Parent Account Detail Page**
Objective: Compose all panels. Dependencies: Tasks 03–07. Tests: full-page smoke test. Definition of Done: test passes.

**Task 09 — Add Full Test Suite**
Objective: Complete coverage per §17, including the mandatory `MaskedField` test. Definition of Done: all green in CI.

**Task 10 — Final Code Review**
Objective: Confirm `MaskedField` is the sole PII-rendering path on this screen, with zero bypass. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] `MaskedField` renders exactly the server's response value, zero client-side mask/unmask logic — mandatory test passing
- [ ] Metadata correction form fields sourced from the server allowlist schema, never hardcoded
- [ ] Entitlement inspector is provably read-only
- [ ] Session revoke requires confirmation
- [ ] Unmask-request entry point pre-fills correct scope

## 20. Definition of Done
Support staff have a full search-to-detail workspace whose PII rendering is provably server-driven with zero independent client-side masking logic — the primary UI reinforcement of B-02's backend guarantee.
