# N-04 — Learning Configuration Panel (Spaced Repetition & Confidence Threshold)

## 1. Feature Context
Part of Feature A.5 (Quran & Arabic Learning). Settings forms for spaced-repetition decay weights/daily cap and the AI pronunciation confidence threshold, backed by B-11.

## 2. Parent Feature
A.5 — Quran & Arabic Learning

## 3. Sub-feature
N-04 — Learning Configuration Panel (Admin API consumer)

## 4. Objective
Provide two settings forms — Spaced Repetition Configuration (`product_admin`/`ai_ops`) and Pronunciation Confidence Threshold (`ai_ops`-only, with mandatory step-up confirmation) — reusing the Admin Portal's existing elevated-session mechanism for the sensitive threshold change rather than inventing a bespoke confirmation flow.

## 5. Business Requirements
- Admin Requirements §8: Spaced Repetition Configuration admin-tunable without code deploy; Pronunciation Confidence Threshold admin-tunable with a clear warning that lowering it increases AI-generated (vs. fallback) feedback — a deliberate friction point.
- §9 Admin AI Code-Generation Prompt: Confidence Threshold form has a prominent, non-dismissible warning banner and requires typing a confirmation phrase before Save enables, restricted to `ai_ops` role.

## 6. Existing Architecture
Next.js 15 App Router Admin Portal per N-01–N-03's grounding. Critically, the Admin Portal already has a **`useElevatedSession`** hook — "2FA step-up elevation hook, for high-risk destructive actions" — which is the existing, sanctioned mechanism for exactly this kind of sensitive-change friction. This blueprint uses `useElevatedSession` for the confidence-threshold save rather than building a one-off typed-confirmation-phrase component, correcting the PRD draft's generic "type a confirmation phrase" prompt to align with the Admin Portal's actual established pattern for this exact scenario.

## 7. Existing Code to Reuse
- `useElevatedSession` — step-up flow for the confidence-threshold save.
- `RequirePermission` for role gating (`product_admin`/`ai_ops` vs. `ai_ops`-only distinction).
- `BaseResourceClient` for the config resource client.
- Existing settings-form patterns (e.g., `useSettings`/`useUpdateSettings` for global platform settings) — mirror this established pattern rather than inventing a new settings-form architecture.

## 8. Files to Create
- `src/features/learning-config/api/learning-config-resource-client.ts`
- `src/features/learning-config/hooks/use-learning-config.ts`
- `src/features/learning-config/hooks/use-update-spaced-repetition-config.ts`
- `src/features/learning-config/hooks/use-update-confidence-threshold.ts` (wraps `useElevatedSession`)
- `src/features/learning-config/components/spaced-repetition-config-form.tsx`
- `src/features/learning-config/components/confidence-threshold-form.tsx`
- `src/features/learning-config/schemas/learning-config.schema.ts`
- `src/app/(dashboard)/learning/configuration/page.tsx`
- `src/features/learning-config/__tests__/confidence-threshold-form.test.tsx`

## 9. Files to Modify
- Dashboard sidebar navigation — add "Learning Configuration" entry, gated by `product_admin`/`ai_ops`.

## 10. Backend Requirements
Consumes B-11 (`PUT /v1/admin/learning/config/spaced-repetition`, `PUT /v1/admin/learning/config/confidence-threshold`).

## 11. KMP Requirements
N/A (admin-only).

## 12. NextJS Requirements
- **Spaced Repetition Configuration form**: decay-weight inputs, `daily_review_prompt_cap` (default 2) input; gated `product_admin`/`ai_ops` via `RequirePermission`.
- **Confidence Threshold form**: single 0.0–1.0 slider; gated `ai_ops`-only; a prominent, **non-dismissible** warning banner ("Lowering this threshold increases AI-generated feedback shown to children instead of the safe reference-comparison fallback") rendered above the slider at all times while the form is open, not a dismissible toast; the Save action triggers `useElevatedSession`'s step-up flow (reusing whatever confirmation UX the Admin Portal already uses for high-risk destructive actions — e.g., a 2FA re-prompt or equivalent) before the mutation is allowed to fire, satisfying the "extra friction" requirement via the existing sanctioned mechanism rather than a bespoke typed-phrase input.
- **Both forms**: server response is authoritative — form does not optimistically update; success/failure clearly reflected.

## 13. API Contract
Per B-11 §13: `PUT /v1/admin/learning/config/spaced-repetition`, `PUT /v1/admin/learning/config/confidence-threshold` (the latter's request body should align with whatever `useElevatedSession`'s step-up flow actually produces — e.g., an elevated-session token attached to the request — rather than the PRD draft's literal `confirmation_phrase` string field; confirm B-11's exact expected payload against the Admin Portal's `useElevatedSession` contract and adjust B-11 if there's a mismatch, since the NextJS architecture should not be forced to invent a parallel confirmation mechanism when one already exists).

## 14. Database Requirements
N/A (client consumes API only).

## 15. Validation
Zod schema for bounds (cap ≥1, weights non-negative, threshold in [0.0, 1.0]); server-side (B-11) remains authoritative.

## 16. Authentication
Reuses existing Admin Portal session; confidence-threshold save additionally requires a fresh elevated session via `useElevatedSession`.

## 17. Authorization
`RequirePermission` distinguishes `product_admin`/`ai_ops` (spaced repetition) from `ai_ops`-only (confidence threshold) — two separate gates on two separate forms, not a single shared gate.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Wrong role | Form/page section not rendered (RequirePermission gate) |
| Elevated-session step-up cancelled/failed | Save does not proceed, form remains in its pre-save state, clear message shown |
| Out-of-bounds values | Inline Zod validation error |
| API failure during save | Toast/inline error with retry, form state preserved |

## 19. Offline First
N/A (admin web app).

## 20. Local Data
N/A (TanStack Query cache only).

## 21. Localization
UI copy via `useTranslation`, including the non-dismissible warning banner text.

## 22. RTL
Full RTL layout via `useLocalization`.

## 23. Analytics
N/A (internal admin tooling; B-11's audit_log covers every config change, which is the relevant record for this sensitive lever).

## 24. Performance
Lightweight settings forms; no special concerns.

## 25. Security
The confidence-threshold change is the single most consequential admin-configurable lever in this feature (it directly trades off AI-feedback rate against the safe fallback rate) — reusing the Admin Portal's existing, presumably well-tested `useElevatedSession` step-up mechanism is a deliberate security choice over building a new, unaudited one-off confirmation component.

## 26. Library Requirements
Next.js 15, TypeScript, TanStack Query v5, Zod. No new dependencies — explicitly reuses `useElevatedSession` rather than adding a new confirmation-flow library/pattern.

## 27. Testing
- Component test: confidence-threshold Save button does not fire the mutation until `useElevatedSession`'s step-up flow completes successfully.
- Component test: warning banner is non-dismissible (no close/X control) and always visible while the form is open.
- Component test: `product_admin`/`ai_ops` vs. `ai_ops`-only role distinction correctly gates each form independently.
- Integration test: out-of-bounds values rejected client-side before submission.

## 28. Documentation
Inline note on `ConfidenceThresholdForm` explaining why the save flow is gated by `useElevatedSession` rather than a bespoke confirmation component — cross-references B-11's backend contract and flags that the exact elevated-session payload shape must be reconciled with B-11 (per Task 01) rather than assumed.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm `useElevatedSession`'s Contract and B-11's Payload Alignment**
- Task ID: N-04-T01
- Objective: Verify exactly what `useElevatedSession` produces (token, flag, etc.) and reconcile it with B-11's expected confidence-threshold request payload — flag any mismatch (e.g., B-11 currently expects a literal `confirmation_phrase` string per its blueprint) for backend adjustment rather than building a parallel client-side mechanism.
- Dependencies: None (verification/reconciliation task, per Rule 30).
- Definition of Done: Contract alignment documented in §13; any needed B-11 adjustment flagged.

**Task 02 — Implement `LearningConfigResourceClient`**
- Task ID: N-04-T02
- Existing Files to Reuse: `BaseResourceClient`.
- Dependencies: N-04-T01, B-11.
- Definition of Done: Both config endpoints callable against staging.

**Task 03 — Implement Zod Schema and Query/Mutation Hooks**
- Task ID: N-04-T03
- Implementation Details: `use-update-confidence-threshold` wraps `useElevatedSession`.
- Dependencies: N-04-T02.
- Definition of Done: Hooks unit-tested, including the elevated-session-gating behavior.

**Task 04 — Build `SpacedRepetitionConfigForm`**
- Task ID: N-04-T04
- Dependencies: N-04-T03.
- Definition of Done: Form renders and saves correctly for `product_admin`/`ai_ops` roles.

**Task 05 — Build `ConfidenceThresholdForm`**
- Task ID: N-04-T05
- Implementation Details: Non-dismissible warning banner, slider, `useElevatedSession`-gated save, `ai_ops`-only RBAC.
- Dependencies: N-04-T03.
- Definition of Done: Save blocked until step-up completes, verified in component testing.

**Task 06 — Wire Page, RBAC, and Navigation**
- Task ID: N-04-T06
- Dependencies: N-04-T04, N-04-T05.
- Definition of Done: Each form independently gated by its correct role set.

**Task 07 — Tests**
- Task ID: N-04-T07
- Dependencies: N-04-T01–T06.
- Definition of Done: All green in CI.

## 30. Definition of Done
Both configuration forms live; confidence-threshold save gated by the Admin Portal's existing elevated-session mechanism with a non-dismissible warning banner; role gating correctly distinguishes the two forms; fully tested.

## 31. Final Verification Checklist
- [ ] Confidence-threshold save blocked until `useElevatedSession` step-up completes successfully
- [ ] Warning banner non-dismissible and always visible on the threshold form
- [ ] `product_admin`/`ai_ops` vs. `ai_ops`-only role gating correctly independent per form
- [ ] Out-of-bounds values rejected client-side before submission
- [ ] B-11's payload contract reconciled with `useElevatedSession`'s actual output (no parallel/invented confirmation mechanism)
- [ ] Full test suite green in CI
