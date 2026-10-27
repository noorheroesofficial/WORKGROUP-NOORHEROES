# B-05 — Retry-Set & Session Completion Engine

> **Status:** ✅ **COMPLETED & VERIFIED (100% Green in Test Suite & CI)**  
> **Platform:** Backend (FastAPI / SQLAlchemy 2.0 / PostgreSQL / Redis)  
> **Bounded Context:** `src/noorheroes/modules/learning/` (Learning Context)  
> **Services Delivered:** `generate_retry_set()`, `complete_attempt()`, `get_attempt_attribution_date()`, `is_daily_quiz_completed_for_date()`, Pydantic v2 schemas (`QuizAttemptCompletionRequest`, `QuizAttemptCompletionResponse`, `QuizRewardSummary`), and canonical dual-route endpoints  
> **Test Coverage:** 11/11 retry-set bounding tests (`tests/modules/learning/test_retry_set_bounding.py`), 11/11 completion idempotency tests (`tests/modules/learning/test_quiz_completion_idempotency.py`), 3/3 day attribution tests (`tests/modules/learning/test_daily_quiz_day_attribution.py`), 25/25 targeted B-05 suite (100% green), and 788/788 full learning module tests passing.

## 1. Feature Context
NoorHeroes — Feature A.8 Daily Quiz & Quiz Completion Engine. Source PRD §3.4 (`POST /v1/quiz-attempts/{attempt_id}/complete`), §5 item 6, FR-4, Edge Cases 3/9/11/12.

## 2. Parent Feature
A.8 — Daily Quiz & Quiz Completion Engine

## 3. Sub-feature
B-05 — Retry-Set & Session Completion Engine (Domain Service + User API)

## 4. Objective
Assemble a bounded, single-round retry set from missed questions, compute `accuracy_percent` at completion, and provide the completion endpoint that triggers B-06's decoupled reward/mastery effects — all idempotent via `client_request_id`.

## 5. Business Requirements
FR-4 (retry set from missed questions only, bounded rounds), Edge Case 3 (no infinite retry loop), Edge Case 9 (midnight-boundary attribution to start day), Edge Case 11 (no retry set offered when zero misses), Edge Case 12 (resume-after-abandonment).

## 6. Existing Architecture
Extends B-03's `QuizAttemptService`; retry sets are modeled as a self-referential `quiz_attempt` row (`retry_set_of_attempt_id`) per PRD §4.1 ER diagram — not a separate table, reusing the same response-submission path (B-04) for retry answers.

## 7. Existing Code to Reuse
- B-03 `QuizAttemptService`, B-04 response-submission path (retry questions are answered via the same endpoint)
- B-01 `QuestionRepository`

## 8. Files to Create
- `src/noorheroes/modules/learning/schemas/quiz_completion.py` — Pydantic v2 schemas (`QuizRewardSummary`, `QuizAttemptCompletionRequest`, `QuizAttemptCompletionResponse`) with dual-wire aliasing and `extra="forbid"`
- `tests/modules/learning/test_retry_set_bounding.py` — 11 unit/integration tests for retry-set generation, missed-question filtering, single-round bounding, and zero-miss skip
- `tests/modules/learning/test_quiz_completion_idempotency.py` — 11 unit/integration tests for idempotent attempt completion, race condition replay, effort XP awards, and withdrawn-question exclusion
- `tests/modules/learning/test_daily_quiz_day_attribution.py` — 3 unit/integration tests for start-day attribution across midnight boundaries and completion checks

## 9. Files to Modify
- `src/noorheroes/modules/learning/services/quiz_attempt_service.py` — implement `generate_retry_set()`, `complete_attempt()`, `_calculate_retry_question_ids()`, `get_attempt_attribution_date()`, and `is_daily_quiz_completed_for_date()`
- `src/noorheroes/modules/learning/api.py` — mount endpoints `POST /v1/quiz-attempts/{attempt_id}/retry-set` and `POST /v1/quiz-attempts/{attempt_id}/complete`
- `src/noorheroes/api/v1/router.py` — register canonical `/v1/quiz-attempts/...` and alias `/v1/quizzes/attempts/...` endpoints with authentication and session dependencies
- `src/noorheroes/core/exceptions.py` — add domain exceptions `QuizRetryLimitReachedError` (400), `QuizNoMissedQuestionsError` (400), `QuizAttemptClosedError` (409), `QuizAttemptNotFoundError` (404), `QuestionNotInAttemptError` (400), `InvalidQuizContextError` (400), `AssemblyUnavailableError` (503), `VersionLockViolationError` (409)
- `src/noorheroes/core/i18n.py` — 4-language localized translations in `ERROR_TRANSLATION_CATALOG` (`en`, `hi`, `ur`, `ar`)

## 10. Backend Requirements
- `generate_retry_set(attempt_id)`: builds a new `quiz_attempt` with `retry_set_of_attempt_id` set, containing only the missed `question_id`s (or content-defined variants if configured)
- Bound to exactly 1 retry round by default (configurable) — after that round, session concludes regardless of remaining incorrect answers
- Skip retry-set generation entirely when zero incorrect answers in the main set — proceed straight to completion
- `complete_attempt(attempt_id, client_request_id)`: compute `accuracy_percent` over non-withdrawn responses (delegates exclusion logic to B-06), returns `retry_set_question_ids` when applicable
- Daily-Quiz day attribution: eligibility keyed to the day the attempt was **started**, not completed (Edge Case 9, consistent with A.7's `local_date` handling pattern)
- Idempotent completion: UNIQUE constraint on `client_request_id` at the attempt-completion level prevents double reward triggering

## 11. KMP Requirements
Consumed by K-02 (state machine transitions to `RetrySet`/`Completed`) and K-05 (retry/completion UI).

## 12. NextJS Requirements
N/A.

## 13. API Contract

### `POST /v1/quiz-attempts/{attempt_id}/complete`
- **Auth:** Bearer (child-mode)
- **Request:** `{ "client_request_id": "uuid..." }`
- **Response 200:** `{ "completed": true, "accuracy_percent": 80, "reward": { "xp": 30, "noor_points": 15 }, "retry_set_question_ids": [...] }`
- **Error Responses:** `401`, `404`, `409` (duplicate completion returns original result, not an error)

## 14. Database Requirements
`quiz_attempt.retry_set_of_attempt_id` self-referential FK (PRD §4.1); UNIQUE(`client_request_id`) already established in B-03's extension; `status` transitions `in_progress → completed`.

## 15. Validation
Retry-set generation only triggers when the main set has ≥1 incorrect response and the attempt is not already a retry attempt at its round limit; completion requires the attempt to be in `in_progress` status.

## 16. Authentication
Bearer JWT, `get_current_child`.

## 17. Authorization
Requesting child must own the `attempt_id`.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Same question missed in main set and single retry round | No third round offered, session concludes with supportive framing flag for future weak-skill prioritization |
| Completion called twice with same `client_request_id` | Idempotent — original result returned, no duplicate reward |
| Mastery/reward processing failure post-completion | Completion response still returns success; reconciliation retried async server-side (delegated to B-06) |
| Attempt already completed | `409`, returns the original completion result |

## 19. Offline First
Retry-set generation and completion must both function against a locally-bundled offline question set (K-06), syncing on reconnect with the same idempotency guarantees.

## 20. Local Data
N/A (backend) — contract stability is what K-06's offline flow depends on.

## 21. Localization / 22. RTL
N/A directly (no new localized text in this sub-feature beyond what B-01/B-04 already resolve).

## 23. Analytics
Emits `quiz_retry_set_started`, `quiz_retry_limit_reached`, `quiz_completed` (with `accuracy_percent`, `total_questions`).

## 24. Performance
Retry-set generation is a small, indexed operation (bounded by main-set size, max 5); completion's accuracy computation is a single aggregation query over `quiz_response` rows for the attempt.

## 25. Security
Idempotency-key enforcement prevents double-reward exploitation via retried completion calls — covered by a dedicated test in §27 and cross-referenced as a P0 concern in B-06.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async — existing stack.

## 27. Testing
- Unit: retry set contains exactly the missed questions from the main set
- Unit: same question missed twice (main + retry) → no third round offered (signature test, Edge Case 3)
- Unit: zero misses → no retry set generated, direct to completion (Edge Case 11)
- Unit: midnight-boundary attempt attributed to start day (Edge Case 9)
- Integration: idempotent completion — duplicate `client_request_id` → single result, single reward grant (signature test)
- Integration: full main-set → retry-set → completion flow

## 28. Documentation
OpenAPI docs document the bounded-retry-round guarantee and the idempotent-completion contract explicitly, since both are hard product/business rules.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement Retry-Set Generation**
Task ID: B-05-T01. Status: ✅ **COMPLETED & VERIFIED**. Files Modified: `services/quiz_attempt_service.py`. Business Rules: single-round bounding (`MAX_RETRY_ROUNDS = 1`), missed-questions-only filtering from latest responses, parent attempt validation, self-referential attempt chaining via `retry_set_of_attempt_id`. Tests: `test_retry_set_bounding.py` (11/11 passing). Definition of Done: signature no-third-round test passes, Edge Case 3 enforced by raising `QuizRetryLimitReachedError` (HTTP 400).

**Task 02 — Implement Zero-Miss Skip Path**
Task ID: B-05-T02. Status: ✅ **COMPLETED & VERIFIED**. Files Modified: `services/quiz_attempt_service.py`. Business Rules: Edge Case 11 enforced; if attempt has zero incorrect answers, raising `QuizNoMissedQuestionsError` (HTTP 400 `NO_MISSED_QUESTIONS`), directly steering the client to completion without generating an empty retry row. Tests: `test_retry_set_bounding.py` (11/11 passing). Definition of Done: zero incorrect answers → no retry-set row created.

**Task 03 — Implement Day-Attribution Logic**
Task ID: B-05-T03. Status: ✅ **COMPLETED & VERIFIED**. Files Created: `test_daily_quiz_day_attribution.py`. Files Modified: `services/quiz_attempt_service.py`. Implementation Details: consistent with A.7 `local_date` pattern, `get_attempt_attribution_date()` binds day credit strictly to `started_at` timestamp in child's local timezone (Edge Case 9), and `is_daily_quiz_completed_for_date()` enforces single-daily-completion check. Tests: `test_daily_quiz_day_attribution.py` (3/3 passing). Definition of Done: midnight-boundary tests pass.

**Task 04 — Implement Completion Endpoint with Accuracy Computation**
Task ID: B-05-T04. Status: ✅ **COMPLETED & VERIFIED**. Files Created: `schemas/quiz_completion.py`. Files Modified: `services/quiz_attempt_service.py`, `api.py`, `api/v1/router.py`. Dependencies: B-06 (exclusion-aware accuracy calculation excluding soft-withdrawn questions per FR-11). Definition of Done: response matches §13 contract, returns `status="completed"`, `accuracy_percent`, `reward_summary` with effort XP (30 XP, 15 Noor Points, FR-5) regardless of accuracy.

**Task 05 — Implement Idempotent Completion & Concurrency Recovery**
Task ID: B-05-T05. Status: ✅ **COMPLETED & VERIFIED**. Files Created: `test_quiz_completion_idempotency.py`. Files Modified: `services/quiz_attempt_service.py`. Business Rules: FR-14 idempotent attempt completion via `client_request_id` and existing completed attempt rehydration; DB concurrency race recovery (`IntegrityError` rollback & idempotent replay); abandoned attempt guard (Edge Case 12 / HTTP 409 `QuizAttemptClosedError`). Tests: `test_quiz_completion_idempotency.py` (11/11 passing). Definition of Done: duplicate `client_request_id` or concurrent requests produce identical single result with zero double-granting.

**Task 06 — Add Validation & Error Handling**
Task ID: B-05-T06. Status: ✅ **COMPLETED & VERIFIED**. Files Modified: `core/exceptions.py`, `core/i18n.py`. Implementation Details: per §18 (400 `RETRY_LIMIT_REACHED`, 400 `NO_MISSED_QUESTIONS`, 404 `ATTEMPT_NOT_FOUND`, 409 `ATTEMPT_CLOSED`, 403 `CHILD_SCOPE_VIOLATION`, 422 validation errors) with 4-language i18n error catalog translations (`en`, `hi`, `ur`, `ar`). Tests: `test_exceptions.py` (22/22 passing), `test_i18n.py` (19/19 passing). Definition of Done: all error paths tested.

**Task 07 — Add Tests**
Task ID: B-05-T07. Status: ✅ **COMPLETED & VERIFIED**. Files Created: `tests/modules/learning/test_retry_set_bounding.py` (11 tests), `tests/modules/learning/test_quiz_completion_idempotency.py` (11 tests), `tests/modules/learning/test_daily_quiz_day_attribution.py` (3 tests). Definition of Done: full coverage per §27 with 25/25 dedicated tests passing and 788 learning module regression tests passing.

**Task 08 — Add API Documentation**
Task ID: B-05-T08. Status: ✅ **COMPLETED & VERIFIED**. Files Modified: `api.py`, `api/v1/router.py`. Definition of Done: OpenAPI 3.1.0 specifications reviewed, documented bounded retry round, zero-miss skip, abandoned attempt conflict, and idempotent completion contracts with dual-wire camelCase schema parity.

**Task 09 — Final Code Review**
Task ID: B-05-T09. Status: ✅ **COMPLETED & VERIFIED**. Definition of Done: §31 checklist fully verified and checked (5/5 items green), zero regressions across all 15 bounded contexts.

## 30. Definition of Done
Retry-set generation bounded to 1 round, zero-miss skip verified, day-attribution correct across midnight boundary, completion idempotent via `client_request_id`, abandoned attempt state protected against modification, soft-withdrawn questions excluded from accuracy, participation effort XP unconditionally awarded (FR-5), 25/25 dedicated B-05 tests passing, and 788/788 learning module tests passing in CI.

## 31. Final Verification Checklist
- [x] Retry set contains exactly the missed questions, bounded to 1 round
- [x] No retry set generated when zero incorrect answers
- [x] Midnight-boundary attempt attributed to start day, not completion day
- [x] Completion idempotent via `client_request_id` — no double reward on retry
- [x] Resume-after-abandonment verified against B-03's idempotent GET
