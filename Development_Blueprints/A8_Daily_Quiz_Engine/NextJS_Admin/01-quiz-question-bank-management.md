# N-01 — Quiz Question Bank Management

## 1. Feature Context
The editorial home base for the shared Quiz Engine's question bank: CRUD across all 5 question types, consumed identically by Home's Daily Quiz, Stories' post-episode quiz, Learn-tab practice, and Dua recall. Every question authored here flows into B-02's assembly engine for all four contexts at once.

## 2. Parent Feature
Feature A.8 — Daily Quiz & Quiz Completion Engine

## 3. Sub-feature
3.1 Quiz Question Bank Management (ID: **N-01**)

## 4. Objective
Build the Question Bank Editor — type-aware CRUD form, skill-tag linking, and a non-blocking distractor quality check — against B-08's admin API.

## 5. Business Requirements
PRD §8 (Question Bank & Reusable Skills — CRUD across 5 types, distractor quality check tool), §9 item 1 (heuristic warnings, not hard blocks).

## 6. Existing Architecture
`src/features/quiz-question-bank/` module, following the existing `DataTable`/`RequirePermission`/form-with-Zod-validation pattern established across other Admin Portal content editors (e.g., A.5/A.6 Content Editors).

## 7. Existing Code to Reuse
- `src/shared/components/data-table.tsx::DataTable`
- `src/shared/components/require-permission.tsx::RequirePermission`
- `src/shared/hooks/use-pagination-state.ts::usePaginationState`
- `src/shared/api/base-resource-client.ts::BaseResourceClient`
- Existing skill-tag multi-select component (A.5 Skill Tree Builder, reused not forked)

## 8. Files to Create
- `src/app/(dashboard)/quiz-engine/question-bank/page.tsx`
- `src/features/quiz-question-bank/api/question-bank-repository.ts` — `QuestionBankRepositoryImpl`
- `src/features/quiz-question-bank/hooks/use-question-bank.ts`, `use-create-question.ts`, `use-update-question.ts`
- `src/features/quiz-question-bank/components/question-type-selector.tsx`
- `src/features/quiz-question-bank/components/question-form.tsx` — per-type prompt/options/correct-answer/explanation fields
- `src/features/quiz-question-bank/components/distractor-quality-check-panel.tsx`
- `src/features/quiz-question-bank/types/question.ts` — Zod discriminated-union schema per type

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `QUIZ_QUESTIONS.*` endpoints
- `src/shared/components/dashboard-shell.tsx` — nav item gated by `content_editor`

## 10. NextJS Requirements
- `QuestionTypeSelector`: multiple_choice | sequence | true_false | image_match | audio_match, switching the form's field set
- `QuestionForm`: prompt content (text/image/audio per type), answer options + correct-answer designation, explanation text + `source_citation`, difficulty/age_band/locale/skill_tags (multi-select linking to skill_node entities)
- `DistractorQualityCheckPanel`: runs a simple client-side heuristic (near-duplicate option text, no plausible-but-wrong option for multiple choice) and surfaces **warnings, not hard blocks** — submission remains allowed, requiring human judgment
- Scholar-approval status indicator shown inline for Quran/Tajweed/Dua-tagged questions before publish is allowed
- Table view: pagination, filter (type/skill/status/age_band), search, sort

## 11. Required API
**Admin API** — B-08: `POST/PATCH /admin/v1/questions`.

## 12. Authentication / Authorization
`useAdminSession()` base auth; write actions require `content_editor` via `hasPermission()`, checked at both the form-submit control (disabled, not hidden) and mirrored by B-08's independent `403` — defense in depth.

## 13. Loading / Empty / Error States
Table-loading skeleton; empty state ("No questions yet — create the first one"); form-submission error state distinct from table-load error, surfacing B-08's validation messages inline per field.

## 14. Responsive UI / Accessibility
Form collapses to single-column on narrow viewports; distractor-quality warnings conveyed with both an icon and text label, never color alone; table rows collapse to stacked cards on mobile.

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()`; question-content fields support multi-locale entry (EN/HI/AR/UR) within the same form, each locale tab independently RTL-aware for Arabic/Urdu entry.

## 16. Security
- `content_editor` gating enforced via `hasPermission()` at the component level, mirrored by B-08's independent `403` — defense in depth
- No client-side bypass of the scholar-approval requirement for tagged content — the publish control itself reflects approval status, not just a warning banner

## 17. Testing
Unit: per-type form field rendering (all 5 types); distractor-quality heuristic produces warnings without blocking submit. Integration: create → appears in table; edit → creates new version per B-08/B-01 version-lock (never an in-place mutation reflected in the UI as an edit-in-place). Permission: submit control disabled for non-`content_editor` sessions (assert `disabled` attribute).

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schemas & Add API Endpoints**
Objective: per-type discriminated-union schema for `question.ts`. Files: `types/question.ts`, `api-endpoints.ts`. Definition of Done: schema validated against B-08's contract for all 5 types.

**Task 02 — Implement `QuestionBankRepositoryImpl`**
Objective: repository for B-08's CRUD endpoints. Follow: existing repository conventions. Dependencies: Task 01. Definition of Done: mocked-fetch tests pass.

**Task 03 — Implement Data Hooks**
Objective: `use-question-bank`, `use-create-question`, `use-update-question`. Dependencies: Task 02. Definition of Done: hooks wired correctly.

**Task 04 — Implement QuestionTypeSelector & QuestionForm**
Objective: type-aware field rendering. Dependencies: Task 03. Tests: per-type field-rendering test. Definition of Done: all 5 types render correct fields.

**Task 05 — Implement DistractorQualityCheckPanel**
Objective: non-blocking heuristic warnings. Dependencies: Task 04. Tests: warning-without-block test. Definition of Done: submission succeeds despite warnings present.

**Task 06 — Implement Question Bank Page**
Objective: compose `RequirePermission` + `DataTable` + form + pagination/filter/search + states. Dependencies: Task 05. Definition of Done: page smoke test passes against mocked API.

**Task 07 — Add Full Test Suite**
Objective: complete coverage per §17. Definition of Done: all green in CI.

**Task 08 — Final Code Review**
Objective: confirm permission gating is genuinely disabling controls (not just styling), confirm version-lock is respected on edit. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] All 5 question types render correct type-specific form fields
- [ ] Distractor quality check surfaces warnings without blocking submission
- [ ] Submit control `disabled` (not merely styled) for non-`content_editor` sessions
- [ ] Editing a published question creates a new version (B-01/B-08 version-lock respected, never shown as an in-place edit)
- [ ] Scholar-approval status visible inline for tagged content
- [ ] Skill-tag multi-select correctly links to existing skill_node entities

## 20. Definition of Done
Editors can author, tag, and quality-check questions across all 5 types through a single form-driven table, with scholar-approval and version-lock guarantees from B-01/B-08 fully respected client-side.
