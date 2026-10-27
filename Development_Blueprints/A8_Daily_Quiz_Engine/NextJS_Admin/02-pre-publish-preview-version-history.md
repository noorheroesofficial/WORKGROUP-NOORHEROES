# N-02 — Pre-Publish Preview & Version History

## 1. Feature Context
The publish gate for the question bank: no question reaches `published` status without an editor explicitly reviewing both a mobile-viewport render and a simulated screen-reader pass. Paired with a version-history view that makes B-01's version-lock guarantee visible and auditable to editors.

## 2. Parent Feature
Feature A.8 — Daily Quiz & Quiz Completion Engine

## 3. Sub-feature
3.2 Pre-Publish Preview & Version History (ID: **N-02**)

## 4. Objective
Build a mandatory pre-publish preview step (visual + screen-reader-simulation, both requiring explicit acknowledgment before the Publish control unlocks) and a per-question version-history list with diffs.

## 5. Business Requirements
PRD §8 ("Preview for Mobile and Screen Reader" — mandatory pre-publish step, publish blocked until acknowledged; "Version Lock After Publication" — editing creates a new version, live version stays immutable), §9 item 2/3.

## 6. Existing Architecture
`src/features/quiz-question-preview/` module, extending N-01's question detail view with a preview/version-history tab.

## 7. Existing Code to Reuse
- N-01's `QuestionBankRepositoryImpl` (extended with preview/version-history methods)
- `src/shared/components/require-permission.tsx::RequirePermission`
- Existing diff-viewer component, if one already exists elsewhere in the Admin Portal (confirm before building a new one)

## 8. Files to Create
- `src/app/(dashboard)/quiz-engine/question-bank/[id]/preview/page.tsx`
- `src/features/quiz-question-preview/api/question-preview-repository.ts`
- `src/features/quiz-question-preview/hooks/use-question-preview.ts`, `use-version-history.ts`, `use-publish-question.ts`
- `src/features/quiz-question-preview/components/mobile-preview-frame.tsx`
- `src/features/quiz-question-preview/components/screen-reader-simulation-view.tsx`
- `src/features/quiz-question-preview/components/version-history-list.tsx`

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `QUIZ_QUESTION_PREVIEW.*`, `QUIZ_QUESTION_VERSIONS.*` endpoints
- N-01's question detail page — add "Preview & Publish" tab entry point

## 10. NextJS Requirements
- `MobilePreviewFrame`: renders the question as it will appear on a mobile viewport, using the same component library/styling tokens as the mobile app where feasible, or a close visual approximation
- `ScreenReaderSimulationView`: text dump of the simulated screen-reader reading order for the question
- Both views require an explicit "I've reviewed this preview" acknowledgment checkbox each; the **Publish button remains disabled** (not hidden) until both acknowledgments are checked — this is the sub-feature's defining UX contract
- `VersionHistoryList`: chronological list of versions per question with diffs; a version being live/current is clearly marked; there is never an "edit" affordance on a published version, only a "create new version" action

## 11. Required API
**Admin API** — B-08: `GET /admin/v1/questions/{id}/preview`, `GET /admin/v1/questions/{id}/versions`.

## 12. Authentication / Authorization
`useAdminSession()` base auth; `content_editor` required to trigger publish; scholar-approval status (for Quran/Tajweed/Dua-tagged content) additionally gates the Publish control — both conditions must be satisfied, checked via `hasPermission()` plus the fetched approval-status field, never assumed client-side.

## 13. Loading / Empty / Error States
Preview-loading skeleton (mobile frame + screen-reader dump load independently, each with its own loading state); error state if preview rendering fails (does not silently allow publish — the acknowledgment checkboxes stay disabled until preview actually loads); version-history empty state for a brand-new unpublished question ("No published versions yet").

## 14. Responsive UI / Accessibility
`ScreenReaderSimulationView` itself must be genuinely screen-reader-accessible (not just a visual mock of one) — its content is read in the same order a real screen reader would encounter it; mobile preview frame scales appropriately on wide admin viewports.

## 15. Localization / RTL
Preview renders the question in each authored locale (locale switcher within the preview), including RTL rendering verification for Arabic/Urdu content — this is precisely the pre-publish check that catches RTL layout issues before children encounter them.

## 16. Security
Publish-gate logic (both acknowledgments + scholar-approval-if-applicable) is enforced server-side by B-08 as the authoritative check — this UI's disabling logic is a UX convenience mirroring that server rule, never a substitute for it; a direct API call without proper acknowledgment state must still be rejected server-side.

## 17. Testing
Unit: Publish button `disabled` until both acknowledgment checkboxes are checked (assert attribute, not styling). Unit: Publish button additionally disabled when scholar-approval is required but not yet granted. Integration: version-history correctly shows prior versions as non-editable, only "create new version" actionable. Accessibility: `ScreenReaderSimulationView` content order matches expected reading order for a sample question of each type.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Extend Repository with Preview/Version-History Methods**
Objective: `question-preview-repository.ts`. Files: repository, `api-endpoints.ts`. Definition of Done: methods match B-08's `/preview` and `/versions` contracts.

**Task 02 — Implement Data Hooks**
Objective: `use-question-preview`, `use-version-history`, `use-publish-question`. Dependencies: Task 01. Definition of Done: hooks wired correctly.

**Task 03 — Implement MobilePreviewFrame**
Objective: mobile-viewport render using shared styling tokens. Dependencies: Task 02. Definition of Done: renders all 5 question types correctly.

**Task 04 — Implement ScreenReaderSimulationView**
Objective: genuinely accessible reading-order text dump. Dependencies: Task 02. Tests: reading-order accessibility test. Definition of Done: test passes for all 5 types.

**Task 05 — Implement Dual-Acknowledgment Publish Gate**
Objective: Publish button disabled until both checkboxes checked and scholar-approval satisfied. Dependencies: Tasks 03–04. Tests: **mandatory gating test**. Definition of Done: test passes for both conditions independently and combined.

**Task 06 — Implement VersionHistoryList with Diffs**
Objective: chronological version list, no in-place-edit affordance on published versions. Dependencies: Task 02. Definition of Done: diff rendering verified against a multi-version fixture.

**Task 07 — Add Full Test Suite**
Objective: complete coverage per §17. Definition of Done: all green in CI.

**Task 08 — Final Code Review**
Objective: confirm publish gating is genuinely server-mirrored, not a client-only illusion. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] Publish button `disabled` until both preview acknowledgments are checked
- [ ] Publish button additionally disabled when scholar-approval is required but missing
- [ ] `ScreenReaderSimulationView` content order matches genuine screen-reader reading order
- [ ] Version history never presents a published version as directly editable
- [ ] Preview renders correctly across all 4 supported locales including RTL
- [ ] Server-side publish gate (B-08) independently verified as the authoritative check, not just this UI's convenience logic

## 20. Definition of Done
No question reaches `published` status without an editor explicitly reviewing both a mobile and screen-reader preview, with version history making B-01's version-lock guarantee fully visible and auditable.
