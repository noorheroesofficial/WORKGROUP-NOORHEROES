# B-04 — Quiz Response Submission & Answer Validation API

> **Status:** ✅ **COMPLETED & VERIFIED (100% Green in Test Suite & CI)**  
> **Platform:** Backend (FastAPI / SQLAlchemy 2.0 / PostgreSQL / Redis)  
> **Bounded Context:** `src/noorheroes/modules/learning/` (Learning Context)  
> **Services Delivered:** `QuizResponseRepository`, `QuizResponse`, Pydantic v2 schemas (`QuizResponseSubmissionRequest`, `QuizResponseSubmissionResponse`, `QuizExplanationResponse`), discriminated validators, and `QuizAttemptService.submit_response()`  
> **Test Coverage:** 19/19 response submission tests (`tests/modules/learning/test_quiz_response_submission.py`), 4/4 tampering penetration tests (`tests/modules/learning/test_quiz_response_tampering.py`), 134/134 learning quiz engine suite tests (100% green).

## 1. Feature Context
NoorHeroes — Feature A.8 Daily Quiz & Quiz Completion Engine. Source PRD §3.4 (`POST /v1/quiz-attempts/{attempt_id}/responses`), §5 item 3, FR-3, FR-7, FR-14.

## 2. Parent Feature
A.8 — Daily Quiz & Quiz Completion Engine

## 3. Sub-feature
B-04 — Quiz Response Submission & Answer Validation API (User API)

## 4. Objective
Record each per-question answer with the full FR-7 data model, validate server-side that the submitted question actually belongs to the requesting attempt's assembled set (rejecting tampering), and return the pre-fetched explanation in the same round-trip.

## 5. Business Requirements
FR-3 (immediate, never-skippable explanation), FR-7 (`question_id`, `content_version_id`, attempt number, answer, response time, hint count, offline flag), FR-14 (idempotency via `client_request_id`), §12.1/§12.2 answer-injection threat mitigation.

## 6. Existing Architecture
Extends `src/noorheroes/modules/learning/api.py` and adds a new service method to B-03's `QuizAttemptService`. Response persistence follows the append-only/immutable pattern already used elsewhere in the platform for historical-fact tables (consistent with A.3/A.5/A.6 progress-history conventions).

## 7. Existing Code to Reuse
- B-03 `QuizAttemptService` (attempt lookup, ownership check)
- B-01 `QuestionRepository` (explanation/source_citation lookup)
- Existing idempotency-key enforcement pattern (`client_request_id` UNIQUE constraint, platform-wide convention per PRD §9.3 reference)

## 8. Files to Create
- `src/noorheroes/modules/learning/models/quiz_response.py`
- `src/noorheroes/modules/learning/schemas/quiz_response.py`
- `src/noorheroes/modules/learning/repositories/quiz_response_repository.py`
- `alembic/versions/0065_create_quiz_response_table.py`
- `tests/modules/learning/test_quiz_response_submission.py`
- `tests/modules/learning/test_quiz_response_tampering.py`

## 9. Files to Modify
- `src/noorheroes/modules/learning/api.py` — add `POST /v1/quiz-attempts/{attempt_id}/responses`
- `src/noorheroes/modules/learning/services/quiz_attempt_service.py` — add `submit_response()` method

## 10. Backend Requirements
- Persist `question_id`, `answer_json`, `response_time_ms`, `hint_count`, `offline`, `client_request_id`, `correct` (server-computed), `attempt_id`
- **Server-side set-membership validation**: reject `400` if `question_id` is not a member of the attempt's assembled question set, even if that `question_id` is otherwise valid/published elsewhere — this is the sub-feature's defining security requirement
- Return `{ correct, explanation: { text, source_citation } }` pre-fetched from B-01, no separate round-trip
- `client_request_id` UNIQUE constraint enforces idempotent replay (duplicate submission returns the original recorded result, not a new row)

## 11. KMP Requirements
Consumed by K-03 (question renderers submit) and K-04 (explanation overlay renders the response).

## 12. NextJS Requirements
N/A.

## 13. API Contract

### `POST /v1/quiz-attempts/{attempt_id}/responses`
- **Auth:** Bearer (child-mode)
- **Request:** `{ "question_id": "...", "answer_json": {...}, "response_time_ms": 4200, "hint_count": 1, "offline": false, "client_request_id": "uuid..." }`
- **Response 200:** `{ "correct": true, "explanation": { "text": "...", "source_citation": "..." } }`
- **Error Responses:** `400` (question_id not in assembled set), `401`, `404` (attempt not found), `409` (ownership mismatch)

## 14. Database Requirements
`quiz_response` (PRD §4.2): FK `attempt_id`, `question_id`; UNIQUE(`client_request_id`); Index `(attempt_id)`, Index `(question_id, created_at DESC)`; append-only/immutable — never updated after insert (PRD §4.3).

## 15. Validation
`question_id` must exist in the attempt's assembled set (server-side, not client-trusted); `answer_json` shape validated per the question's `type` (reuse B-01's per-type discriminated schema); `attempt_id` must belong to the requesting child.

## 16. Authentication
Bearer JWT, `get_current_child`.

## 17. Authorization
Requesting child must own the `attempt_id` referenced — cross-child attempt access rejected (`409`/`403`).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| `question_id` not in assembled set (tampering) | `400`, response not persisted |
| Duplicate `client_request_id` | Idempotent replay — returns original result, no duplicate row |
| Attempt not found | `404` |
| Attempt owned by a different child | `403`/`409` |
| Malformed `answer_json` for question type | `422` |
| Database failure | Standard rollback, client retries with same `client_request_id` |

## 19. Offline First
`offline: true` flag recorded when submitted from K-06's offline outbox; submission is safely replayable on reconnect via `client_request_id`.

## 20. Local Data
N/A (backend) — but response contract must exactly match what K-06's outbox queues locally.

## 21. Localization / 22. RTL
Explanation `text`/`source_citation` resolved to the requesting child's locale (reuses B-01's localized payload fields).

## 23. Analytics
Server-side event source for client-emitted `quiz_question_answered` and `quiz_explanation_viewed` (client fires these on receipt of this response).

## 24. Performance
Single indexed lookup for set-membership check; explanation lookup joined in the same query as the response insert to avoid a second round-trip.

## 25. Security
This endpoint's defining security property is the answer-injection defense (§12.1) — covered by a dedicated penetration-style test (§27) submitting a response for a `question_id` outside the assembled set.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Pydantic v2 — existing stack.

## 27. Testing
- Unit: set-membership validation rejects out-of-set `question_id` with `400` (signature test, §5 item 3)
- Unit: idempotent duplicate submission returns original result, no duplicate row
- Integration: all 5 question types' `answer_json` shapes accepted and scored correctly
- Negative: cross-child attempt access rejected

## 28. Documentation
OpenAPI docs explicitly document the `400` tampering-rejection contract as a documented security behavior, not an incidental validation error.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create QuizResponse Model & Migration**
Task ID: B-04-T01. Status: ✅ **COMPLETED & VERIFIED**. Files Created: `models/quiz_response.py`, `alembic/versions/0065_create_quiz_response_table.py`. Definition of Done: full FR-7 data model (`question_id`, `content_version_id`, `attempt_number`, `answer_json`, `response_time_ms`, `hint_count`, `offline`, `client_request_id`, `correct`), append-only constraint enforced (no update method exposed on the repository).

**Task 02 — Create Response Schemas**
Task ID: B-04-T02. Status: ✅ **COMPLETED & VERIFIED**. Files Created: `schemas/quiz_response.py`. Definition of Done: per-type `answer_json` validation matches B-01's discriminated union, DTOs with camelCase/snake_case dual-wire aliasing via `NoorHeroesBaseModel`.

**Task 03 — Implement Repository**
Task ID: B-04-T03. Status: ✅ **COMPLETED & VERIFIED**. Files Created: `repositories/quiz_response_repository.py`. Definition of Done: idempotent insert via `client_request_id` UNIQUE constraint, append-only immutability enforced (`update()` raises `NotImplementedError`).

**Task 04 — Implement Set-Membership Validation (Signature Security Task)**
Task ID: B-04-T04. Status: ✅ **COMPLETED & VERIFIED**. Files Modified: `services/quiz_attempt_service.py`. Security: this is the P0 requirement of this sub-feature. Tests: `test_quiz_response_tampering.py` (4/4 passing). Definition of Done: tampering test passes, verified as a non-bypassable CI gate.

**Task 05 — Implement Response Endpoint with Pre-Fetched Explanation**
Task ID: B-04-T05. Status: ✅ **COMPLETED & VERIFIED**. Files Modified: `api.py`, `api/v1/router.py`. Dependencies: Task 04. Definition of Done: single round-trip returns `correct` + `explanation` (`text`, `source_citation`), mounted at canonical `/v1/quiz-attempts/{attempt_id}/responses` and modular alias.

**Task 06 — Add Validation & Error Handling**
Task ID: B-04-T06. Status: ✅ **COMPLETED & VERIFIED**. Implementation Details: per §18 (400 on set-membership tampering, 403 on cross-child attempt, 404 on non-existent attempt or question, 409 on completed/abandoned attempt, 422 on malformed answer_json). Definition of Done: all error paths tested.

**Task 07 — Add Tests**
Task ID: B-04-T07. Status: ✅ **COMPLETED & VERIFIED**. Files Created: `test_quiz_response_submission.py` (19/19 passing), `test_quiz_response_tampering.py` (4/4 passing). Definition of Done: full coverage per §27.

**Task 08 — Add API Documentation**
Task ID: B-04-T08. Status: ✅ **COMPLETED & VERIFIED**. Definition of Done: OpenAPI docs reviewed, tampering-rejection behavior and status responses documented.

**Task 09 — Final Code Review**
Task ID: B-04-T09. Status: ✅ **COMPLETED & VERIFIED**. Definition of Done: §31 checklist fully checked (10/10 items).

## 30. Definition of Done
Response submission endpoint live, set-membership validation enforced and tested as a CI-gating test, idempotent replay verified, explanation pre-fetch confirmed single-round-trip, full FR-7 persistence verified, 134/134 quiz tests passing.

## 31. Final Verification Checklist
- [x] `400` rejection verified for out-of-set `question_id` submission (penetration-style test)
- [x] Idempotent duplicate submission returns original result, no duplicate `quiz_response` row
- [x] All 5 question types' `answer_json` shapes validated and scored correctly
- [x] Explanation returned in the same round-trip as the answer result
- [x] `quiz_response` rows are genuinely append-only/immutable
- [x] Cross-child attempt access rejected with `403`
- [x] Full FR-7 data model persisted (`question_id`, `content_version_id`, `attempt_number`, `answer_json`, `response_time_ms`, `hint_count`, `offline`, `client_request_id`, `correct`)
- [x] Retry attempt sequence number automatically derived as `2` for retry set attempts
- [x] All error handling paths verified (`404` attempt not found, `409` attempt closed/abandoned, `422` malformed answer_json)
- [x] Arabic session locale resolves translated explanation text and citation


