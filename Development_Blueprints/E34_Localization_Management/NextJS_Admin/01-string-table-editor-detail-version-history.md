# N-01 — String Table Editor & String Detail/Version History

## 1. Feature Context
The primary authoring workspace for translated strings, with an embedded ICU rule editor that catches malformed plural/gender/date syntax inline, before the localization manager even attempts to submit.

## 2. Parent Feature
E.34 — Localization Management

## 3. Sub-feature
2.1 String Table Editor & String Detail/Version History (ID: **N-01**)

## 4. Objective
Build the String Table Editor, String Detail/Version History, and embedded ICU Plural/Gender/Date Rule Editor component against B-01, with client-side ICU syntax validation as a fast pre-submission check (server remains authoritative).

## 5. Business Requirements
- §1.18 screens 1, 2, 5: String Table Editor, String Detail/Version History, ICU Rule Editor (component within String Detail).
- §7 Frontend AI prompt item 2: ICU editor with inline syntax validation, showing an inline error before submission for malformed input.
- FR-11 (UI reflection): version history clearly shows the prior published version remains servable while a new draft is under review.

## 6. Existing Architecture
`src/features/string-table/` module, following the filterable-data-table-plus-detail-editor pattern established by E.29's Content Library (E.29 N-01).

## 7. Existing Code to Reuse
- `src/shared/components/require-permission.tsx::RequirePermission`
- `src/shared/components/data-table.tsx::DataTable`
- E.29 N-02's review-status-pill visual pattern (reused for the Draft/Machine-Assisted/Editorial Review/Scholar Review/Published pill)

## 8. Files to Create
- `src/app/(dashboard)/platform/strings/page.tsx`
- `src/app/(dashboard)/platform/strings/[id]/page.tsx`
- `src/features/string-table/api/locale-string-repository.ts`
- `src/features/string-table/hooks/use-string-list.ts`, `use-string-detail.ts`, `use-update-translation.ts`
- `src/features/string-table/components/string-table-list.tsx`
- `src/features/string-table/components/string-detail-version-history.tsx`
- `src/features/string-table/components/review-stage-pill.tsx`
- `src/features/string-table/components/icu-rule-editor.tsx` — inline ICU syntax validation
- `src/features/string-table/types/locale-string.ts` — Zod schema

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `LOCALE_STRINGS.*` endpoints
- `src/shared/components/dashboard-shell.tsx` — nav item under "Platform" navigation group

## 10. NextJS Requirements
- `IcuRuleEditor`: performs a fast client-side ICU MessageFormat syntax check on every keystroke/blur (via a lightweight JS ICU parser), showing an inline error message before the submit action is even attempted — the server (B-01) remains the authoritative validator, this is a UX-speed layer only, never a replacement for the server check.
- `StringDetailVersionHistory`: lists all versions chronologically with their `review_stage`/`status`, clearly indicating which version is currently `published` (and therefore live on B-02's Delivery API) versus the newer draft under review.
- `ReviewStagePill`: identical visual treatment to E.29's established pattern, reused not reinvented.

## 11. Required API
**Admin API** — B-01: `POST /v1/admin/locales/strings`, `GET /v1/admin/locales/strings`, `PATCH /v1/admin/locales/strings/{id}`.

## 12. Authentication / Authorization
`useAdminSession()` base auth; `RequirePermission permission="localization_manager"`.

## 13. Loading / Empty / Error States
List loading skeleton; "No strings yet for this locale" empty state; **mandatory** inline ICU-syntax error state (shown before submission attempt); server-side validation error state as the defense-in-depth fallback.

## 14. Responsive UI / Accessibility
ICU syntax errors programmatically associated with the input field (`aria-describedby`), not conveyed by red-border styling alone.

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()` for the Admin Portal chrome itself; the string values being edited may themselves be RTL content (handled by the RTL-aware text input, cross-ref N-03).

## 16. Security
The client-side ICU check is explicitly a UX convenience, not a security boundary — mandatory test confirms the form still correctly surfaces the server's authoritative validation error if a malformed string somehow bypasses the client check (e.g., via a direct API call during testing), never silently trusting client-side validation alone.

## 17. Testing
Unit: ICU syntax client-side validator (valid/malformed fixtures). UI: **mandatory** — malformed ICU input shows an inline error before submission is attempted; version history correctly distinguishes published-and-live from draft-under-review. Integration: full create-string → edit → new-version-created flow.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schema & Add API Endpoints**
Objective: `locale-string.ts` schema. Files: `types/locale-string.ts`, `api-endpoints.ts`. Tests: schema validation. Definition of Done: schema used by Task 03.

**Task 02 — Implement `LocaleStringRepositoryImpl`**
Objective: Repository for B-01's three endpoints. Tests: mocked-fetch tests. Dependencies: Task 01. Definition of Done: tests pass.

**Task 03 — Implement `IcuRuleEditor` with Inline Validation**
Objective: Fast client-side ICU check, inline error display. Dependencies: Task 02. Tests: **mandatory** — malformed-input-shows-inline-error-before-submission test. Definition of Done: test passes.

**Task 04 — Implement `ReviewStagePill` (Reusing E.29's Pattern)**
Objective: Confirm direct visual-pattern reuse. Dependencies: E.29 N-02. Tests: reuse-not-duplication check. Definition of Done: zero duplicated status-pill styling logic.

**Task 05 — Implement `StringDetailVersionHistory`**
Objective: Chronological version list, published-vs-draft distinction. Dependencies: Task 04. Tests: published-vs-draft-distinction test. Definition of Done: test passes.

**Task 06 — Implement the List and Detail Pages**
Objective: Compose all components with loading/empty/error states. Dependencies: Tasks 03–05. Tests: full-page smoke tests. Definition of Done: tests pass.

**Task 07 — Add Full Test Suite**
Objective: Complete coverage per §17, including the mandatory inline-validation test. Definition of Done: all green in CI.

**Task 08 — Final Code Review**
Objective: Confirm the client-side ICU check never substitutes for the server's authoritative validation. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] ICU syntax errors shown inline before submission — mandatory test passing
- [ ] Server-side validation error still surfaces correctly if the client check is somehow bypassed
- [ ] Version history clearly distinguishes published-and-live from draft-under-review
- [ ] `ReviewStagePill` reused from E.29, not duplicated
- [ ] `localization_manager` scope enforced

## 20. Definition of Done
Localization managers can author and edit translations with fast, genuinely helpful ICU-syntax feedback and a clear, honest picture of which version is actually live versus still under review.
