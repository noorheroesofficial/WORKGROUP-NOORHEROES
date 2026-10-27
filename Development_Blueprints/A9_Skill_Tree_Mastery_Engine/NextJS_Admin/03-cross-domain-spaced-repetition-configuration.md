# N-03 — Cross-Domain Spaced Repetition Configuration

## 1. Feature Context
Part of Feature A.9 (Skill Tree & Mastery Engine). A simple settings form for the GLOBAL daily-review-prompt cap (B-11) — explicitly labeled as applying across ALL domains combined, not per-domain, to avoid admin confusion.

## 2. Parent Feature
A.9 — Skill Tree & Mastery Engine

## 3. Sub-feature
N-03 — Cross-Domain Spaced Repetition Configuration (Admin Page)

## 4. Objective
Build a settings form for `daily_review_prompt_cap` (default 2), with explanatory copy clarifying the global/cross-domain scope, restricted to `product_admin` role, backed by B-11's `GET/PUT /admin/v1/mastery/spaced-repetition-config`.

## 5. Business Requirements
- Admin AI Code-Generation Prompt (A.9 PRD §9) item 4: settings form for the global cap, "explicitly labeled as applying across ALL domains combined, not per-domain, with explanatory copy clarifying this scope to avoid admin confusion." Restricted to `product_admin`.

## 6. Existing Architecture
React + TypeScript Admin Portal. Simple single-value settings-form pattern (reuse whatever generic settings-form component the Admin Portal already has, if one exists, e.g., for other global platform settings).

## 7. Existing Code to Reuse
- Existing settings-form pattern/component (if the Admin Portal has a generic single-value config editor elsewhere, reuse it rather than building a bespoke one for this single field).
- Existing RBAC role-guard for `product_admin`.

## 8. Files to Create
- `app/admin/mastery/spaced-repetition-config/page.tsx`
- `app/admin/mastery/spaced-repetition-config/components/SpacedRepetitionConfigForm.tsx`
- `lib/api/masterySpacedRepetitionConfig.ts`
- `lib/types/spacedRepetitionConfig.ts`
- `__tests__/admin/mastery/spaced-repetition-config/SpacedRepetitionConfigForm.test.tsx`

## 9. Files to Modify
None (self-contained new page; no existing per-domain config surface to migrate away from, per the PRD's framing this is a net-new centralization, not a migration of an existing per-domain UI).

## 10. Backend Requirements
N/A (consumes B-11).

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- **Form field:** single numeric input, `daily_review_prompt_cap`, default 2, minimum 1, sane maximum (e.g., 10, matching B-11's validation bound).
- **Explanatory copy:** prominent text explicitly stating this cap applies across ALL learning domains combined (e.g., "A child will see at most this many review prompts per day, total, across Quran, Arabic, Tajweed, and any other domain — not this many per domain") — this copy is a first-class requirement, not decoration, given the explicit admin-confusion risk called out in the PRD.
- **Save confirmation:** clear success feedback on save; current value always visible (not just on load, but reflected accurately after save).
- **RBAC:** `product_admin` only.

## 13. API Contract
Consumes B-11's `GET/PUT /admin/v1/mastery/spaced-repetition-config` exactly.

## 14. Database Requirements
N/A (frontend only).

## 15. Validation
Client-side mirrors B-11's bounds (`>= 1`, sane upper bound) before submission.

## 16. Authentication
Reuses existing Admin Portal auth/session context.

## 17. Authorization
`product_admin` role required.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Invalid value (0, negative, or above the sane upper bound) | Submit blocked client-side with inline error |
| Server rejects (`422`) | Field-level error shown from server response |
| Fetch failure on load | Error state with retry, not a form defaulting silently to an unknown value |
| Wrong role | Access-denied state |

## 19. Offline First
N/A (admin web app).

## 20. Local Data
N/A.

## 21. Localization
Per N-01 §21's platform-wide Admin Portal localization scope decision — the explanatory "applies across all domains" copy is especially important to get right if localized, since it's the primary anti-confusion mechanism.

## 22. RTL
Per N-01 §22's decision.

## 23. Analytics
N/A (audit logging via B-11 covers change tracking).

## 24. Performance
Trivial (single-value form); no special performance considerations.

## 25. Security
`product_admin`-gated; low direct security risk but meaningful product-quality risk if misconfigured (an overly high cap could overwhelm children with review prompts) — the explanatory copy is itself a risk-mitigation control.

## 26. Library Requirements
No new libraries.

## 27. Testing
- Unit: bounds validation.
- Component test: explanatory "applies across all domains" copy is present and visible in the rendered form (a deliberate, testable requirement given the PRD's explicit emphasis on avoiding admin confusion).
- RBAC test: non-`product_admin` access denied.
- Integration: save → B-11 reflects new value → B-07's scheduler (verified at the backend layer, cross-referenced here) picks up the change.

## 28. Documentation
Note in the page linking back to B-07's scheduler behavior, so admins understand the downstream effect of changing this value.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Build API Client & Types**
- Task ID: N-03-T01
- Objective: Typed client for B-11's config endpoint.
- Why This Is Required: Foundation for the form.
- Existing Architecture to Follow: Existing Admin Portal API-client conventions.
- Existing Files to Reuse: Existing typed-fetch wrapper.
- Files to Create: `lib/api/masterySpacedRepetitionConfig.ts`, `lib/types/spacedRepetitionConfig.ts`.
- Files to Modify: None.
- Implementation Details: `getConfig()`, `updateConfig(cap: number)`.
- Business Rules: N/A. Validation: Type-safe shape.
- Error Handling: Typed error propagation. Security: N/A. Performance: N/A.
- Localization: N/A. RTL: N/A. Analytics: N/A.
- Tests: N/A (thin layer).
- Documentation: TSDoc.
- Dependencies: B-11.
- Do Not Change: N/A.
- Expected Result: Working client.
- Definition of Done: Types match B-11's schema.

**Task 02 — Build SpacedRepetitionConfigForm with Explanatory Copy**
- Task ID: N-03-T02
- Objective: The settings form itself, with the mandatory cross-domain-scope explanatory copy.
- Why This Is Required: Core deliverable; the explanatory copy is explicitly called out in the PRD as necessary to prevent admin confusion.
- Existing Architecture to Follow: Existing settings-form pattern.
- Existing Files to Reuse: Existing form/input components.
- Files to Create: `SpacedRepetitionConfigForm.tsx`, `page.tsx`.
- Files to Modify: None.
- Implementation Details: Single numeric input, bounds validation, prominent explanatory copy per §12, save confirmation.
- Business Rules: Update-only (no create/delete concept for this singleton config).
- Validation: Per §15. Error Handling: Per §18.
- Security: `product_admin` RBAC gate.
- Performance: N/A. Localization: Per decision. RTL: Per decision.
- Analytics: N/A.
- Tests: `SpacedRepetitionConfigForm.test.tsx` including the explanatory-copy-present assertion.
- Documentation: Page-level comment per §28.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Working, clearly-scoped settings form.
- Definition of Done: Tests green including the explanatory-copy assertion and RBAC test.

## 30. Definition of Done
Cross-Domain Spaced Repetition Configuration page live, `product_admin`-gated, with prominent explanatory copy preventing per-domain-vs-global confusion, correctly reading from and writing to B-11's config endpoint.

## 31. Final Verification Checklist
- [ ] Form correctly reads/writes `daily_review_prompt_cap`
- [ ] Explanatory "applies across all domains" copy present and prominent
- [ ] Bounds validation matches B-11's server-side rules
- [ ] `product_admin` RBAC enforced
- [ ] Save confirmation and error states both handled
- [ ] Value change verified to propagate to B-07's scheduler behavior (cross-checked against backend)
