# N-02 — Quiz Builder (Question Bank & Editor)

## 1. Feature Context
The reusable question-authoring surface embedded both standalone and inside the Story Editor's Quiz tab (N-01). Its defining UI guarantee: once a question's `version_locked` flag is server-confirmed true, the editor renders it fully read-only — no edit interaction is possible, full stop.

## 2. Parent Feature
E.29 — Content CMS & Scholar Review Workflow

## 3. Sub-feature
2.2 Quiz Builder (Question Bank & Editor) (ID: **N-02**)

## 4. Objective
Build the Question Bank browse and type-specific Question Editor against B-05, with distractor-quality-check display, a mobile/screen-reader preview variant, and a structurally read-only rendering for version-locked questions.

## 5. Business Requirements
- FR-3: reusable skill-tagged question bank, four question types, correct answer + explanation, difficulty/age/locale/skill tags, distractor-quality checks, mobile/screen-reader preview, version lock after publication.
- §7 frontend AI-prompt requirement #5: render a "Version Locked" read-only state for any `version_locked=true` question, sourced from the server, never a local client-side flag.

## 6. Existing Architecture
`src/features/quiz-builder/` module, embeddable both as a standalone route and within N-01's Story Editor Quiz tab.

## 7. Existing Code to Reuse
- `src/shared/components/data-table.tsx::DataTable`
- `src/shared/components/require-permission.tsx::RequirePermission`
- `src/shared/api/base-resource-client.ts::BaseResourceClient`

## 8. Files to Create
- `src/app/(dashboard)/quiz-builder/page.tsx` — Question Bank
- `src/app/(dashboard)/quiz-builder/[id]/page.tsx` — Question Editor
- `src/features/quiz-builder/api/quiz-repository.ts`
- `src/features/quiz-builder/hooks/use-question-bank.ts`, `use-question-detail.ts`
- `src/features/quiz-builder/components/question-editor/` — `MultipleChoiceEditor.tsx`, `OrderingEditor.tsx`, `AudioImageMatchEditor.tsx`, `TrueFalseEditor.tsx`
- `src/features/quiz-builder/components/distractor-quality-panel.tsx`
- `src/features/quiz-builder/components/mobile-screen-reader-preview.tsx`
- `src/features/quiz-builder/components/version-locked-banner.tsx`
- `src/features/quiz-builder/types/question.ts` — Zod schema (discriminated union per `question_type`)

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `QUIZ_BUILDER.*` endpoints
- `src/features/content-cms/components/story-editor-tabs/QuizTab.tsx` (N-01) — embeds this module's Question Editor

## 10. NextJS Requirements
- Question Editor selects the type-specific sub-component based on `question_type`; each renders correct-answer + explanation fields alongside difficulty/age/locale/skill tags.
- `version_locked` state read exclusively from the server response — when true, the entire editor form renders in a read-only mode (all inputs `disabled`, no save button), with `VersionLockedBanner` explaining why.
- `DistractorQualityPanel` displays automated check results returned on save, as advisory feedback, not a blocking gate in the UI (the check itself already ran server-side).

## 11. Required API
**Admin API** — B-05: `POST/GET/PATCH /v1/admin/questions`.

## 12. Authentication / Authorization
`useAdminSession()` base auth; `RequirePermission permission="content_editor"`.

## 13. Loading / Empty / Error States
Question Bank loading skeleton, empty state; edit-attempt-on-locked-question shows the banner rather than a generic error; save-failure error state.

## 14. Responsive UI / Accessibility
Each question type's editor keyboard-navigable; the mobile/screen-reader preview variant is a first-class, testable view, not an afterthought.

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()` for tags/labels; question content itself is authored per-locale via the `locale` tag field.

## 16. Security
`version_locked` enforcement is UI-defense-in-depth alongside B-05's server-side `409` rejection — the UI must never even attempt a save call against a locked question, tested explicitly.

## 17. Testing
Unit: type-specific editor field validation, `version_locked`-derives-from-server-not-local-flag logic. UI: **mandatory** — no edit interaction possible on a version-locked question (confirmed via server-fixture `version_locked=true`). Integration: full create → distractor-check-display → save flow per question type.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schema & Add API Endpoints**
Objective: `question.ts` discriminated-union schema. Files: `types/question.ts`, `api-endpoints.ts`. Tests: per-type schema validation. Definition of Done: schema used by Task 03.

**Task 02 — Implement `QuizRepositoryImpl`**
Objective: Repository for B-05's three endpoints. Tests: mocked-fetch tests. Dependencies: Task 01. Definition of Done: tests pass.

**Task 03 — Implement the Four Type-Specific Question Editors**
Objective: MC/ordering/audio-image-match/true-false editors. Dependencies: Task 02. Tests: per-type field validation. Definition of Done: tests pass.

**Task 04 — Implement `VersionLockedBanner` and Read-Only Gating**
Objective: Server-sourced `version_locked` check disabling the entire form. Dependencies: Task 03. Tests: **mandatory** — no-edit-interaction-on-locked-question test. Definition of Done: test passes.

**Task 05 — Implement `DistractorQualityPanel` and Preview**
Objective: Advisory quality feedback display, mobile/screen-reader preview variant. Dependencies: Task 02. Tests: preview-rendering test. Definition of Done: test passes.

**Task 06 — Implement Question Bank Page**
Objective: Browse/filter by skill tag/difficulty/type. Dependencies: Task 02. Tests: empty-state test. Definition of Done: test passes.

**Task 07 — Wire Embedding into N-01's Quiz Tab**
Objective: Confirm the standalone Question Editor components are reusable inside N-01's `QuizTab.tsx` without duplication. Dependencies: N-01. Definition of Done: no duplicated editor logic between standalone and embedded contexts.

**Task 08 — Add Full Test Suite**
Objective: Complete coverage per §17. Definition of Done: all green in CI.

**Task 09 — Final Code Review**
Objective: Confirm the version-locked check is genuinely server-sourced and structurally blocks all edit paths. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] All four question types have dedicated, correctly-validating editors
- [ ] `version_locked=true` renders a fully read-only form with an explanatory banner, sourced from the server
- [ ] Zero save call attempted against a version-locked question
- [ ] Distractor-quality results displayed as advisory feedback
- [ ] Mobile/screen-reader preview functions correctly
- [ ] Question Editor components reused (not duplicated) between standalone and Story-Editor-embedded contexts

## 20. Definition of Done
The Quiz Builder provides a correct, type-aware authoring experience for all four question types with a structurally enforced, server-sourced version lock — reusable standalone and embedded within N-01's Story Editor.
