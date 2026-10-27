---
id: STORY-036-04
epic: EPIC-036
kind: feature
title: Fasting Log API with Strict Parent-Configured Approach Enforcement
status: ready
priority: P0
prd: ../../PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md
depends_on: [STORY-036-01]
produces: [api.ramadan-fasting-logs]
consumes: [type.ramadan-models]
created: 2026-09-30
---

## User Story
As an authenticated child learner or parent on their behalf, I want to submit daily fasting logs constrained strictly within the parent-configured fasting approach, so that children medically or developmentally unready to fast are never pressured or shamed.

## Acceptance Criteria
- [ ] AC1: Given a child whose parent configured `fasting_approach = 'education_only'`, when a submission is made with `status = 'fasted_full'` or `status = 'fasted_practice'`, then the API rejects the request with HTTP 403 Forbidden and a child-safe explanation (Backend AI Prompt item 3 mandatory test).
- [ ] AC2: Given a child with `education_only`, when submitting `status = 'education_only'`, then the API accepts the entry with HTTP 201 Created and persists the log in `fasting_logs`.
- [ ] AC3: Given a child with `fasting_approach = 'fasted_practice'`, when submitting either `education_only` or `fasted_practice`, then the API accepts and persists the log.
- [ ] AC4: Given a child with `fasting_approach = 'fasted_full'`, when submitting any of `fasted_full`, `fasted_practice`, or `education_only`, then the API accepts and persists the log.
- [ ] AC5: Given a child whose parent has disabled the Fasting Tracker entirely, when any fasting log submission is attempted, then the API rejects the write with HTTP 403 Forbidden (`"Fasting tracker is not enabled for this profile"`).
- [ ] AC6: Given a parent who changes the child's approach partway through Ramadan, then all existing `fasting_logs` rows are preserved and only future log submissions are constrained to the new approach.
- [ ] AC7: Given a child attempting to submit a log for a different child's ID, when session validation executes, then the request is rejected with HTTP 403 Forbidden.

## Technical Notes
- Files in scope:
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/models/fasting_log.py`
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/schemas/fasting_log_schema.py`
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/repositories/fasting_log_repository.py`
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/services/fasting_log_service.py`
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/routers/fasting_log_router.py`
  - `NoorHeroes-Backend/alembic/versions/xxxx_create_fasting_logs_table.py`
- Architecture refs: `sdocs/architecture-ref.md` Section 8.2 (Invariant 4), 8.3, 8.4; Blueprint B-04.
- Non-functional: Live configuration cross-check on every write against A.7 Habit Service (never cached on write path). Anti-shaming error copy.

## Test Approach
- Unit: Test approach-boundary matrix for all 3 approach values (`education_only`, `fasted_practice`, `fasted_full`) against all 3 status submissions.
- Integration: Mandatory test confirming `education_only` child submitting `fasted_full` returns HTTP 403; test disabled tracker rejection; test mid-season approach transition preserving historical rows.
- E2E: Parent setting approach to `fasted_practice` and child logging practice fast successfully.

## Out of Scope
- Habit tracker UI rendering and toggle components (owned by Mobile K-03).
- Family aggregate calculation (owned by STORY-036-06).
