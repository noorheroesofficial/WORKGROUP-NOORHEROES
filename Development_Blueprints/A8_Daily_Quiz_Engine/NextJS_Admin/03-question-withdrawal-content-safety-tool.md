# N-03 — Question Withdrawal & Content Safety Tool

## 1. Feature Context
The trust-and-safety off-switch for the question bank: a "Withdraw" action (never a delete) that removes a question from future assembly while preserving every historical response referencing it, directly feeding B-06's mastery/reward exclusion guarantee on the backend.

## 2. Parent Feature
Feature A.8 — Daily Quiz & Quiz Completion Engine

## 3. Sub-feature
3.3 Question Withdrawal & Content Safety Tool (ID: **N-03**)

## 4. Objective
Build a reason-required Withdrawal action, distinct from delete, that keeps withdrawn questions visible in the Question Bank table with a status pill and a link to the resulting audit-log entry.

## 5. Business Requirements
PRD §8 ("Withdrawal Tool: Mark a question `is_withdrawn = true` (never hard-delete) with a required reason field"), §9 item 4, §5 item 5 (backend exclusion logic this tool triggers), §12.9 Security Checklist item on withdrawn-question exclusion.

## 6. Existing Architecture
`src/features/quiz-question-withdrawal/` module, extending N-01's table with a row-level "Withdraw" action and status pill, following the existing confirmation-modal pattern used elsewhere in the Admin Portal for irreversible-feeling actions.

## 7. Existing Code to Reuse
- N-01's `QuestionBankRepositoryImpl` (extended with a `withdraw()` method)
- Existing confirmation-modal component
- Existing audit-log link/viewer component (if one already exists elsewhere in the Admin Portal — confirm before building a new one)

## 8. Files to Create
- `src/features/quiz-question-withdrawal/components/withdraw-question-modal.tsx`
- `src/features/quiz-question-withdrawal/components/withdrawal-status-pill.tsx`
- `src/features/quiz-question-withdrawal/hooks/use-withdraw-question.ts`

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `QUIZ_QUESTION_WITHDRAW.*` endpoint
- N-01's Question Bank table — add "Withdraw" row action and status pill column

## 10. NextJS Requirements
- "Withdraw" action opens a confirmation modal requiring a non-empty `reason` field before the confirm control enables
- On success, the question remains visible in the table (never removed from the list view) with a `Withdrawn` status pill and the recorded reason viewable on hover/expand
- Withdrawal action gated to `content_editor` or `trust_safety` roles via `hasPermission()`
- Link from the withdrawn-status pill to the corresponding `audit_log` entry for that action

## 11. Required API
**Admin API** — B-08: `PATCH /admin/v1/questions/{id}` `{ is_withdrawn: true, reason }`.

## 12. Authentication / Authorization
`useAdminSession()` base auth; withdrawal control requires `content_editor` **or** `trust_safety` via `hasPermission()`, checked at the modal's confirm control (disabled, not hidden) and mirrored by B-08's independent role check — defense in depth.

## 13. Loading / Empty / Error States
Modal-submission loading state on confirm; error state if the withdrawal API call fails (modal stays open, error surfaced inline, question not optimistically marked withdrawn until success confirmed); table row itself has no separate empty state beyond N-01's existing table empty state.

## 14. Responsive UI / Accessibility
Confirmation modal fully keyboard-navigable and screen-reader-labeled (irreversible-feeling actions deserve explicit accessible confirmation, not just a visual dialog); status pill conveyed with text label, not color alone.

## 15. Localization / RTL
Modal copy and `reason` field label fully localized; RTL layout for the modal and status pill.

## 16. Security
- Role gating (`content_editor` or `trust_safety`) enforced client-side as UX convenience, with B-08's independent `403` as the authoritative check
- `reason` field is required both client-side (form validation) and server-side (B-08 `422` on empty reason) — this is an audit-trail integrity requirement, not just a UX nicety, since withdrawal reasons feed trust-and-safety review processes

## 17. Testing
Unit: confirm control `disabled` until `reason` field is non-empty. Unit: confirm control `disabled` for sessions lacking `content_editor`/`trust_safety`. Integration: successful withdrawal updates the row's status pill without removing it from the table. Integration: failed withdrawal (network error) keeps the question's prior state, error shown inline, modal remains open for retry.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Extend Repository with Withdraw Method**
Objective: `withdraw(id, reason)` on `QuestionBankRepositoryImpl`. Files: repository, `api-endpoints.ts`. Definition of Done: method matches B-08's contract.

**Task 02 — Implement useWithdrawQuestion Hook**
Objective: mutation hook with optimistic-free (success-confirmed-only) state update. Dependencies: Task 01. Definition of Done: hook only marks withdrawn on confirmed server success.

**Task 03 — Implement WithdrawQuestionModal**
Objective: reason-required confirmation modal. Dependencies: Task 02. Tests: reason-required gating test. Definition of Done: test passes.

**Task 04 — Implement WithdrawalStatusPill**
Objective: status pill + reason-on-hover + audit-log link. Dependencies: Task 02. Definition of Done: pill renders correctly for withdrawn vs. active questions.

**Task 05 — Wire Row Action into N-01's Table**
Objective: add "Withdraw" action and status pill column. Files to Modify: N-01's table component. Dependencies: Tasks 03–04. Definition of Done: action visible only with appropriate role, disabled otherwise.

**Task 06 — Add Full Test Suite**
Objective: complete coverage per §17. Definition of Done: all green in CI.

**Task 07 — Final Code Review**
Objective: confirm withdrawal is never presented or implemented as a hard delete anywhere in this module. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] Confirm control disabled until a non-empty `reason` is entered
- [ ] Confirm control disabled for sessions lacking `content_editor`/`trust_safety`
- [ ] Withdrawn questions remain visible in the table with a status pill, never removed from the list
- [ ] No delete affordance exists anywhere in this module — withdraw is the only removal-adjacent action
- [ ] Withdrawal reason viewable and linked to its `audit_log` entry
- [ ] Failed withdrawal leaves the question's prior state unchanged, error shown inline

## 20. Definition of Done
Trust-and-safety and content teams can withdraw a question with a mandatory audit-trailed reason, with the withdrawn item remaining visible and traceable — never silently deleted — directly enabling B-06's backend exclusion guarantee.
