# B-05 — Quiz Question Bank & Builder API

## 1. Feature Context
A reusable, taggable question bank feeding every quiz surface across the platform (A.3's post-story quiz, A.8's Daily Quiz Engine). Its defining guarantee: once a question's parent content publishes, that question version locks — irreversibly — and can never again be edited in place.

## 2. Parent Feature
E.29 — Content CMS & Scholar Review Workflow

## 3. Sub-feature
1.5 Quiz Question Bank & Builder API (ID: **B-05**)

## 4. Objective
Implement question CRUD with skill tags, difficulty, four question types, automatic distractor-quality checks, and an irreversible `version_locked` flag set exactly once at parent-content publish time.

## 5. Business Requirements
- FR-3: reusable skill-tagged question bank; types (MC, ordering, audio/image match, true/false); correct answer + explanation; difficulty/age/locale/skill tags; distractor-quality checks; mobile/screen-reader preview; version lock after publication.

## 6. Existing Architecture
`modules/content_cms/quiz/` sub-package, FK'd to `content_item` (B-01) for parent-content association.

## 7. Existing Code to Reuse
- `modules/content_cms/repository.py::ContentItemRepository` (B-01, parent-content lookup)
- `common/base_service.py`, `common/base_repository.py`

## 8. Files to Create
- `src/noorheroes/modules/content_cms/quiz/models.py` — `QuizQuestionOrm`
- `alembic/versions/xxxx_create_quiz_question.py`
- `src/noorheroes/modules/content_cms/quiz/schemas.py` — `QuestionCreateRequest`, `QuestionResponse`
- `src/noorheroes/modules/content_cms/quiz/repository.py` — `QuizQuestionRepository`
- `src/noorheroes/modules/content_cms/quiz/service.py` — `QuizQuestionService(BaseService)`
- `src/noorheroes/modules/content_cms/quiz/distractor_check.py` — distractor-quality validation logic
- `src/noorheroes/modules/content_cms/quiz/api.py` — `QuizRouter`
- `tests/modules/content_cms/quiz/test_quiz_question_service.py`
- `tests/modules/content_cms/quiz/test_version_lock_irreversibility.py`

## 9. Files to Modify
- `src/noorheroes/main.py` — register `QuizRouter` under `/v1/admin/questions`
- B-06's publish transition — must call `QuizQuestionService.lock_all_for_content(content_id)` on publish

## 10. Backend Requirements
- `QuizQuestionService.create(payload)`: validates `question_type` against the four canonical types; runs `distractor_check.run(question)` synchronously on save, storing results (advisory, not blocking) for editor feedback.
- `QuizQuestionService.update(question_id, payload)`: rejects (`409 QUESTION_VERSION_LOCKED`) if `version_locked=true`.
- `QuizQuestionService.lock_all_for_content(content_id)`: called exactly once, at the moment the parent `content_item` transitions to `published` (invoked by B-06) — sets `version_locked=true` on every question FK'd to that content; never resettable to `false` by any application code path.

## 11. API Contract

### `POST /v1/admin/questions` / `GET /v1/admin/questions` / `PATCH /v1/admin/questions/{id}`
- Auth: `content_editor`+ role. Validation: distractor-quality checks run automatically on save; `PATCH` against a `version_locked=true` question is rejected.

## 12. Database Requirements
- `quiz_question`: FK `content_id`; index `(content_id)`; `version_locked` boolean, default `false`, application code contains no path that sets it back to `false`.

## 13. Validation
- `question_type IN ('multiple_choice','ordering','audio_image_match','true_false')`.
- Skill tags validated against the existing skill taxonomy (A.9's Mastery Engine tag set — reuse, don't fork a parallel taxonomy).

## 14. Authentication
Admin Bearer via `get_current_admin`.

## 15. Authorization
`require_admin_scope("content_editor")`.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| Edit attempt on a version-locked question | `409 QUESTION_VERSION_LOCKED` |
| Invalid `question_type` | `422` |
| Unauthorized request | `401`/`403` |
| Database failure | `503`, logged |

## 17. Security
`version_locked` transition is one-way by construction — no update method in the repository accepts setting it to `false`, and the only code path that sets it `true` is B-06's publish call, never a direct client-facing endpoint.

## 18. Analytics
`quiz_question_created`, `quiz_question_distractor_check_run` audited via `AuditLogService`.

## 19. Performance
Distractor check is a synchronous, lightweight heuristic (not an AI call) — runs inline on save without materially affecting response latency.

## 20. Library Requirements
No new libraries.

## 21. Testing
- Unit: version-lock rejection of edit attempts, distractor-check correctness across question types.
- **Mandatory irreversibility test**: confirm `version_locked` can never be reset to `false` via any application code path once set, and that a locked question rejects an edit attempt (per PRD backend AI-prompt requirement #4).
- Integration: publish-triggers-lock-all-for-content flow (with B-06, mocked).

## 22. Documentation
Update OpenAPI schema.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Create `QuizQuestionOrm` Model & Migration**
Objective: Base table per the PRD ER diagram. Tests: migration smoke test. Definition of Done: clean migration.

**Task 02 — Implement `QuizQuestionRepository` with No `unlock()` Method**
Objective: Data access with `version_locked` settable only to `true`, never `false`, at the repository interface level. Tests: interface-shape test confirming no unlock method exists. Definition of Done: test passes.

**Task 03 — Implement Distractor-Quality Check**
Objective: `distractor_check.py` heuristic validation. Tests: distractor-quality-flag correctness. Definition of Done: test passes.

**Task 04 — Implement `QuizQuestionService`**
Objective: CRUD with version-lock rejection, `lock_all_for_content()`. Dependencies: Task 01–03. Tests: **mandatory irreversibility test**. Definition of Done: test passes.

**Task 05 — Add Router Endpoints**
Objective: Wire CRUD routes. Tests: covered by Task 06. Definition of Done: endpoints live, documented.

**Task 06 — Add Unit & Integration Tests**
Objective: Full coverage per §21. Definition of Done: all green in CI.

**Task 07 — Update OpenAPI Documentation**
Objective: Regenerate/diff-classify. Definition of Done: non-breaking diff confirmed.

**Task 08 — Final Code Review**
Objective: Confirm no code path anywhere resets `version_locked` to `false`. Definition of Done: checklist in §24 fully checked.

## 24. Final Verification Checklist
- [ ] `version_locked` set to `true` exactly once, at parent-content publish time, never resettable to `false`
- [ ] Edit attempt on a locked question rejected with `409`
- [ ] Distractor-quality check runs automatically on every save
- [ ] All four question types supported with correct-answer + explanation fields
- [ ] Skill tags reuse A.9's existing taxonomy, not a forked parallel one

## 25. Definition of Done
The question bank supports efficient authoring across all four question types with automatic quality checks and an irreversible publish-time version lock — feeding A.3's and A.8's quiz surfaces with provably stable, unedited-post-publish content.
