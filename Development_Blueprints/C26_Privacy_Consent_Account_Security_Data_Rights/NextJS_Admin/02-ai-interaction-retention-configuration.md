# N-02 — AI Interaction Retention Configuration

## 1. Feature Context
Part of Feature C.26's Admin Requirements (§8). A single-value settings form for the AI Interaction History retention window, consuming B-06.

## 2. Parent Feature
C.26 Privacy, Consent, Account Security & Data Rights (Settings)

## 3. Sub-feature
**N-02 — AI Interaction Retention Configuration**

## 4. Objective
Build a `trust_safety`/`ai_ops`-gated settings form for the default `ai_safety_event` retention window, making explicit in the UI that changes are forward-only (never retroactive).

## 5. Business Requirements
- §8: update-only, elevated `trust_safety`/`ai_ops` role.
- B-06's stated guarantee: changes apply to new ingestions only, never retroactively.

## 6. Existing Architecture
**Depends on B-06, which itself depends on B-02's cross-feature resolution with C.22.** Do not build this page until B-06 is confirmed unblocked. Follows the same layered NextJS Admin pattern as N-01.

## 7. Existing Code to Reuse
- `BaseResourceClient` pattern (update-only usage — `list`/`get` for the single config value, `create`/`delete` unused).
- Existing single-value settings-form pattern, if one exists elsewhere in the admin portal (check before building a bespoke one).
- `RequirePermission`.

## 8. Files to Create
- `src/features/ai-retention-config/api/ai-retention-config-client.ts`
- `src/features/ai-retention-config/api/schemas.ts`
- `src/features/ai-retention-config/hooks/use-ai-retention-config.ts`
- `src/app/(dashboard)/trust-safety/ai-retention-config/page.tsx`

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `API_ENDPOINTS.AI_RETENTION_CONFIG.BASE`.
- Sidebar navigation — add under Trust & Safety, gated by `RequirePermission`.

## 10. Backend Requirements
Consumes B-06 exclusively (`GET/PATCH /v1/admin/ai-interaction-retention-config`).

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- Simple form: current `retention_days` value, editable, with an explicit inline notice ("Changes apply to new AI interactions going forward only — existing records keep their original retention date") sourced directly from B-06's forward-only guarantee, not a generic disclaimer.
- Submit calls `PATCH`; success shows updated value; `403` for non-`trust_safety`/`ai_ops` roles shows a clear insufficient-permissions message (page itself should already be hidden from those roles via `RequirePermission`, this is defense-in-depth).
- `RequirePermission permission="ai-retention-config:manage"` — confirm/add to the `AdminPermission` catalog, mapped to backend `trust_safety`/`ai_ops`.

## 13. API Contract
Consumes B-06's contract as documented in that blueprint.

## 14. Database Requirements
Not applicable.

## 15. Validation
`retention_days` positive integer within the confirmed maximum bound (per B-06 §13 — surface the same bound client-side for inline validation, sourced from the same confirmed value, not a separately guessed number).

## 16. Authentication
`useAdminSession()`.

## 17. Authorization
`RequirePermission`, `trust_safety`/`ai_ops` only.

## 18. Error Handling
- `QueryErrorState` for load failure.
- Inline validation for out-of-bounds input.
- `403` handled with a specific message per §12.

## 19. Offline First
Not applicable.

## 20. Local Data
Not applicable.

## 21. Localization
Form labels and the forward-only notice text via `useTranslation()`.

## 22. RTL
Full RTL layout.

## 23. Analytics
Not specified; standard admin audit trail (server-side, per B-06).

## 24. Performance
Trivial single-value form.

## 25. Security
Elevated-role gating both at the page level (`RequirePermission`) and defense-in-depth at the API-error-handling level.

## 26. Library Requirements
No new libraries.

## 27. Testing
- Unit: schema validation for `retention_days` bounds.
- Integration/UI: form loads current value, submits update, shows success.
- Integration/UI: forward-only notice text is present and matches B-06's actual guarantee wording.
- Integration/UI: `RequirePermission` hides page/nav entry for unauthorized roles.

## 28. Documentation
Document that the confirmed maximum bound value must stay in sync with B-06's backend-enforced maximum — flag as a value that must be updated in both places if changed.

## 29. AI Coding Agent Implementation Steps

**Task 00 — Confirm B-06 Is Unblocked**
- **Objective:** Verify B-06's own dependency on B-02's resolution has cleared.

**Task 01 — Resource Client & Schema**
- **Files to Create:** `ai-retention-config-client.ts`, `schemas.ts`.

**Task 02 — `useAiRetentionConfig` Hook**

**Task 03 — Settings Form Page with Forward-Only Notice**
- **Files to Create:** `page.tsx`.
- **Definition of Done:** Notice text accurately reflects B-06's forward-only guarantee.

**Task 04 — Permission Wiring, Localization, RTL**

**Task 05 — Full Test Suite & Documentation**

## 30. Definition of Done
AI retention configuration is editable behind the correct elevated role, with an accurate forward-only notice, and only after B-06's own dependency chain (B-02) has cleared.

## 31. Final Verification Checklist
- [ ] B-06 confirmed unblocked before implementation
- [ ] Forward-only notice text accurate and localized
- [ ] Bounds validation matches B-06's confirmed backend maximum
- [ ] `RequirePermission` correctly restricts to `trust_safety`/`ai_ops`
- [ ] Full localization and RTL verified
