# N-02 — Mastery Formula Version Manager

## 1. Feature Context
Part of Feature A.9 (Skill Tree & Mastery Engine). The governed Admin Portal UI for creating new mastery-scoring formula versions (B-10) — a create-only, mandatory-rationale workflow enforcing the non-retroactivity principle at the tooling level.

## 2. Parent Feature
A.9 — Skill Tree & Mastery Engine

## 3. Sub-feature
N-02 — Mastery Formula Version Manager (Admin Page)

## 4. Objective
Build a form to create a new `mastery_formula_version` (weights + mandatory rationale), a version-history table, and explicitly NO edit-in-place action anywhere in the UI — restricted to `learning_science`/`ai_ops` roles.

## 5. Business Requirements
- Admin AI Code-Generation Prompt (A.9 PRD §9) item 3: create-form with weight validation, mandatory rationale, activation flips prior version's `active=false`, NO "edit existing version" action anywhere, version-history table, `learning_science`/`ai_ops` role restriction.
- Edge Case 9 / non-retroactivity principle, enforced here at the tooling level.

## 6. Existing Architecture
React + TypeScript Admin Portal. Reference `NEXT-JS-INSTRUCTIONS.md` for form/validation/table conventions.

## 7. Existing Code to Reuse
- Existing Admin Portal form-validation library/pattern (whatever the platform uses — e.g., react-hook-form + zod, or equivalent already established).
- Existing RBAC role-guard components, extended to check `learning_science`/`ai_ops` roles.
- Existing "history table" / audit-log display pattern if one already exists elsewhere in the Admin Portal (reuse its table-with-metadata-columns pattern rather than building a bespoke one).

## 8. Files to Create
- `app/admin/mastery/formula-versions/page.tsx`
- `app/admin/mastery/formula-versions/components/FormulaVersionCreateForm.tsx`
- `app/admin/mastery/formula-versions/components/FormulaVersionHistoryTable.tsx`
- `lib/api/masteryFormulaVersions.ts`
- `lib/types/masteryFormulaVersion.ts`
- `lib/validation/formulaWeightsSchema.ts` — zod (or equivalent) schema for weight-sum/bounds validation, mirroring B-10's server-side rules.
- `__tests__/admin/mastery/formula-versions/FormulaVersionCreateForm.test.tsx`

## 9. Files to Modify
None outside this sub-feature's own new page (no existing component needs migration here, unlike N-01).

## 10. Backend Requirements
N/A (consumes B-10).

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- **Create form fields:** `accuracy`, `attempts`, `recency`, `difficulty`, `transfer_bonus` (each a 0-1 weight input, e.g., slider or numeric input with live sum display), and a REQUIRED `rationale` textarea (submit button disabled until non-empty and above a minimum length).
- **Live weight-sum validation:** show the running sum as the admin adjusts weights, with a clear visual indicator when it's not close to 1.0 (soft warning) vs. genuinely invalid (hard block per B-10's server-side tolerance).
- **No edit action:** the version-history table has NO "edit" button/action on any row — only view (and the create form is the only mutation entry point). This absence is a deliberate design decision, not an oversight — a code-review checklist item for this page.
- **Version history table:** columns for weights (summarized or expandable), `rationale`, `effective_from`, `created_by` (admin name), `active` badge — sorted newest-first.
- **RBAC:** page and the create form gated behind `learning_science` OR `ai_ops` role; other admin roles see a read-only history view (if product intent allows broader read access) or an access-denied state (confirm against B-10's read-scope decision).

## 13. API Contract
Consumes B-10's `GET/POST /admin/v1/mastery/formula-versions` exactly as specified there.

## 14. Database Requirements
N/A (frontend only).

## 15. Validation
Client-side mirrors B-10's server-side rules: weights in `[0,1]`, sum within tolerance of 1.0, `rationale` non-empty with a sensible minimum length (discourage placeholder text) — server remains authoritative, client-side is a UX improvement.

## 16. Authentication
Reuses existing Admin Portal auth/session context.

## 17. Authorization
`learning_science` or `ai_ops` role required for creation; read-scope per B-10's confirmed decision.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Weights don't sum close to 1.0 (client-side check) | Submit button disabled/warning shown before hitting the server |
| Server rejects with `422` (weight/rationale validation) | Field-level error messages surfaced from the server response, not a generic toast |
| Missing rationale | Submit blocked client-side; server-side `422` as defense-in-depth if somehow bypassed |
| Wrong role attempts access | Access-denied state, not a broken form |

## 19. Offline First
N/A (admin web app).

## 20. Local Data
N/A.

## 21. Localization
Per N-01 §21's platform-wide Admin Portal localization scope decision.

## 22. RTL
Per N-01 §22's decision.

## 23. Analytics
N/A (audit logging via B-10 is the relevant tracking mechanism, not product analytics).

## 24. Performance
Small dataset (formula versions are created infrequently) — no pagination/virtualization required for the history table in practice, though a reasonable page-size cap is still good defensive practice if the table could theoretically grow large over years of operation.

## 25. Security
This is one of the most sensitive Admin Portal pages in the feature — role-gating and the structural absence of an edit-in-place action are both load-bearing governance controls, not cosmetic; treat any future request to "add a quick edit button here" as a red flag against Edge Case 9's non-retroactivity principle.

## 26. Library Requirements
No new libraries beyond the existing Admin Portal form/validation stack.

## 27. Testing
- Unit: weight-sum validation logic (boundary cases: exactly 1.0, just outside tolerance, negative values).
- Component test: submit button disabled until rationale is provided.
- **Explicit negative test:** confirm no edit/update UI affordance exists anywhere on this page (guards against future accidental addition).
- RBAC test: non-`learning_science`/`ai_ops` roles cannot access the create form.
- Integration: create → history table reflects new version with correct `active` flag transition.

## 28. Documentation
Page-level comment/README note explaining why there is intentionally no edit action, referencing Edge Case 9, for any future engineer tempted to add one.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Build API Client, Types & Weight-Validation Schema**
- Task ID: N-02-T01
- Objective: Typed client + shared validation schema mirroring B-10.
- Why This Is Required: Foundation for the form and history table.
- Existing Architecture to Follow: Existing Admin Portal API-client and validation-schema conventions.
- Existing Files to Reuse: Existing typed-fetch wrapper, existing zod/validation-library usage elsewhere in the Admin Portal.
- Files to Create: `lib/api/masteryFormulaVersions.ts`, `lib/types/masteryFormulaVersion.ts`, `lib/validation/formulaWeightsSchema.ts`.
- Files to Modify: None.
- Implementation Details: Schema validates weight bounds + sum tolerance identically to B-10's server-side rule (keep the tolerance value in sync — document it in both places with a cross-reference comment).
- Business Rules: N/A. Validation: This IS the validation layer.
- Error Handling: Typed error propagation. Security: N/A. Performance: N/A.
- Localization: N/A. RTL: N/A. Analytics: N/A.
- Tests: Unit tests for the validation schema's boundary cases.
- Documentation: TSDoc, cross-reference comment to B-10's server-side tolerance.
- Dependencies: B-10.
- Do Not Change: N/A.
- Expected Result: Working client + validation layer.
- Definition of Done: Validation schema unit tests green.

**Task 02 — Build FormulaVersionCreateForm**
- Task ID: N-02-T02
- Objective: The mandatory-rationale, weight-validated create form.
- Why This Is Required: Core deliverable; the only mutation entry point for this data.
- Existing Architecture to Follow: Existing form-component conventions.
- Existing Files to Reuse: Existing form/input/slider components.
- Files to Create: `FormulaVersionCreateForm.tsx`.
- Files to Modify: None.
- Implementation Details: Live weight-sum display, disabled submit until valid + rationale present, server-error surfacing per §18.
- Business Rules: No save-without-rationale path exists, client or server.
- Validation: Task 01's schema.
- Error Handling: Per §18.
- Security: `learning_science`/`ai_ops` RBAC gate on the form itself (not just the page).
- Performance: N/A. Localization: Per decision. RTL: Per decision.
- Analytics: N/A.
- Tests: `FormulaVersionCreateForm.test.tsx` (submit-disabled-until-valid test).
- Documentation: N/A.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Working create form.
- Definition of Done: Component tests green including the disabled-until-valid case.

**Task 03 — Build FormulaVersionHistoryTable (No Edit Action)**
- Task ID: N-02-T03
- Objective: Version-history display with a deliberate absence of edit functionality.
- Why This Is Required: Makes the non-retroactivity principle visible/enforced in the actual admin workflow, not just documented.
- Existing Architecture to Follow: Existing table-component conventions.
- Existing Files to Reuse: Existing history/audit-table pattern if present elsewhere.
- Files to Create: `FormulaVersionHistoryTable.tsx`.
- Files to Modify: None.
- Implementation Details: Columns per §12; view-only row actions (e.g., "view full weights" expand), no edit button anywhere.
- Business Rules: This is the enforcement point — no edit UI exists.
- Validation/Error Handling/Security/Performance: N/A beyond standard table concerns.
- Localization: Per decision. RTL: Per decision. Analytics: N/A.
- Tests: Explicit negative test confirming no edit affordance exists in the rendered output.
- Documentation: Page-level comment per §28.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Working, edit-free history table.
- Definition of Done: Negative test green; manual review confirms no edit path exists anywhere in the page.

## 30. Definition of Done
Mastery Formula Version Manager page live, `learning_science`/`ai_ops`-gated, enforcing mandatory rationale and weight validation on every new version, with a version-history table that structurally has no edit-in-place action anywhere.

## 31. Final Verification Checklist
- [ ] Create form enforces mandatory, non-trivial rationale
- [ ] Weight bounds/sum validation matches B-10's server-side tolerance
- [ ] `learning_science`/`ai_ops` RBAC enforced
- [ ] No edit-in-place action exists anywhere on the page (explicitly tested)
- [ ] Version history correctly reflects `active` flag transitions after each creation
- [ ] Page-level documentation explains the intentional absence of an edit action
