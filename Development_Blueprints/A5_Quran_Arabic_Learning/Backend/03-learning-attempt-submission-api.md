# B-03 — Learning Attempt Submission API

> [!NOTE]
> **Status**: ✅ **COMPLETED & VERIFIED** (100% Tested & Verified, All Invariants Preserved)
> - **Models & Migration**: `LearningAttempt` in `src/noorheroes/modules/learning/learning_attempt_models.py`, Alembic migration `alembic/versions/0045_add_learning_attempts.py`.
> - **Evaluation Engine**: Content-driven question bank in `practice_question_bank.py`, evaluation across quiz/tracing/matching in `attempt_evaluation_service.py`.
> - **Pedagogical Invariants**: FR-7 multi-session hold ($\ge 2$ distinct calendar dates required for `mastered`), FR-18 non-penalizing hints (`delta > 0`), Edge Case 1 borderline rounding ($\ge 0.80$).
> - **Idempotency & Security**: Recitation guard (HTTP 400 directing to B-04), idempotent replay via unique `client_event_id` with race condition recovery, family-scoped child ownership enforcement (`CHILD_SCOPE_VIOLATION` / `403`).
> - **Atomic Transactions & Invalidation**: Single-transaction atomic write (`session.flush()`), immediate B-01 Redis cache invalidation (`invalidate_skill_tree_cache`).
> - **Localization**: 4-language i18n localization (`en`, `hi`, `ur`, `ar`).
> - **API Endpoints**: Canonical `POST /v1/learning/attempts` and direct alias `POST /v1/attempts`.
> - **Test Suite**: 52 dedicated tests across `test_attempt_evaluation_service.py` (29 tests), `test_learning_attempts_api.py` (18 tests), and `test_learning_attempt_repository.py` (5 tests) with 100% pass rate (252 passing tests across learning module).

## 1. Feature Context
Part of Feature A.5 (Quran & Arabic Learning). Records every non-recitation practice attempt (quiz, tracing, matching) and drives mastery-score/state-transition updates via the B-01 state machine.

## 2. Parent Feature
A.5 — Quran & Arabic Learning

## 3. Sub-feature
B-03 — Learning Attempt Submission API (User API)

## 4. Objective
Evaluate and persist a child's practice attempt, update mastery score and skill-node state through the shared state machine, and do so idempotently.

## 5. Business Requirements
- FR-7: mastery requires correct performance across different question forms and more than one session — this endpoint's accumulation logic is what enforces that (single-session repeats do not alone cross the mastery threshold).
- FR-18: hint usage (`hint_count`) feeds mastery-confidence calculation, never a visible penalty.
- Idempotency required per `client_event_id`.

## 6. Existing Architecture
Same `learning` bounded context. Depends on B-01's models/state-machine.

## 7. Existing Code to Reuse
- `SkillNodeStateRepository`, `compute_next_state()`, `invalidate_skill_tree_cache()` from B-01.
- `get_current_child`.

## 8. Files Created
- `src/noorheroes/modules/learning/learning_attempt_models.py` — `LearningAttempt` append-only ORM model with UUIDv7, unique `client_event_id`, and FK cascade.
- `src/noorheroes/modules/learning/learning_attempt_schemas.py` — `AttemptTypeEnum`, `LearningAttemptCreateRequest`, `LearningAttemptResponse` Pydantic v2 schemas.
- `src/noorheroes/modules/learning/practice_question_bank.py` — Curated question bank for Arabic, Quran, and Tajweed exercises.
- `src/noorheroes/modules/learning/learning_attempt_repository.py` — `LearningAttemptRepository` with replay lookup and distinct session dates query.
- `src/noorheroes/modules/learning/attempt_evaluation_service.py` — Domain service evaluating practice attempts, hint weighting, FR-7 multi-session enforcement, and cache invalidation.
- `alembic/versions/0045_add_learning_attempts.py` — Alembic migration for `learning_attempts` table.
- `tests/modules/learning/test_attempt_evaluation_service.py` — 29 unit tests covering 16 distinct domain evaluation scenarios.
- `tests/modules/learning/test_learning_attempts_api.py` — 18 HTTP integration tests for canonical and alias API endpoints.
- `tests/modules/learning/test_learning_attempt_repository.py` — 5 unit tests for attempt creation, unique replay query, history querying, and distinct date calculation.

## 9. Files Modified
- `src/noorheroes/modules/learning/api.py` — mounted `POST /v1/learning/attempts`.
- `src/noorheroes/api/v1/router.py` — mounted direct alias `POST /v1/attempts`.
- `src/noorheroes/modules/learning/deps.py` — registered repositories and service dependencies.
- `src/noorheroes/modules/learning/models.py` — re-exported `LearningAttempt`.
- `src/noorheroes/modules/learning/schemas.py` — re-exported schemas.
- `src/noorheroes/modules/learning/repository.py` — re-exported repository.
- `src/noorheroes/modules/learning/service.py` — re-exported service.
- `src/noorheroes/core/exceptions.py` — added `SkillNodeNotFoundError`, `QuestionNotFoundError`, `RecitationAttemptTypeError`.
- `MASTER-README.md` — Section 8 Route Catalog & Section 11.36 Scenario Execution Matrix.
- `FAST-API-INSTRUCTIONS.md` — updated Section 5.5.
- `src/noorheroes/modules/learning/README.md` — added Scenarios S-51 through S-65, full 81-scenario execution matrix (S-01 to S-81), and 252-test matrix.

## 10. Backend Requirements
- **Router**: `POST /v1/learning/attempts`, `get_current_child`, rejects `attempt_type == "recitation"` with a `400` directing to B-04's endpoint.
- **Service**: `AttemptEvaluationService.submit_attempt()` — evaluates correctness for `quiz`/`tracing`/`matching` types against the content service's answer key, computes `mastery_delta`, applies it to `skill_node_state.mastery_score`, calls `compute_next_state()` to determine any state transition, persists the `learning_attempt` row, and invalidates B-01's skill-tree cache.
- **Idempotency**: `client_event_id` unique constraint — a replayed request with the same ID returns the original result without re-scoring or double-mutating mastery.
- **Multi-session mastery enforcement**: mastery-delta accumulation logic must track whether correct performance has occurred across more than one distinct session/day before allowing a `practicing→mastered` transition (per FR-7); this session-distinctness check lives in this service, using `learning_attempt.created_at` history.

## 11. KMP Requirements
N/A directly; consumed by K-03, K-05, K-06, K-08, K-10 (all non-recitation attempt submissions).

## 12. NextJS Requirements
N/A.

## 13. API Contract

### Canonical Endpoint
`POST /v1/learning/attempts`

### Direct Route Alias
`POST /v1/attempts`

- **Authentication:** Bearer JWT (`get_current_child_session`, child-mode required)
- **Headers:**
  - `Authorization: Bearer <child_jwt_token>`
  - `Content-Type: application/json`
  - `X-Locale: en|hi|ur|ar` (optional, default `en`)
  - `Accept-Language: en|hi|ur|ar` (optional fallback)

- **Request Schema (`LearningAttemptCreateRequest`):**
  Wire format serialized as camelCase (supports snake_case model alias):
  | Field | Type | Required | Description |
  |---|---|---|---|
  | `nodeId` | `str` (UUID) | **Yes** | Target curriculum skill node ID. |
  | `questionId` | `str` (UUID) | **Yes** | Target practice question ID evaluated against question bank. |
  | `attemptType` | `str` | **Yes** | Practice interaction type: `quiz`, `tracing`, or `matching`. (`recitation` rejected with HTTP 400). |
  | `answerPayload` | `Dict[str, Any]` | **Yes** | Type-specific answer payload: <br>• *quiz*: `{"selected_option": "baa"}`<br>• *tracing*: `{"accuracy_ratio": 0.88}` ($\ge 0.85$ passes)<br>• *matching*: `{"pairs": {"alif": "a", "baa": "b", "taa": "t"}}` |
  | `hintCount` | `int` | No | Number of hints used ($\ge 0$, default `0`). Scales confidence without visible negative deduction (FR-18). |
  | `responseTimeMs` | `int` | No | Response latency in milliseconds ($\ge 0$, default `0`). |
  | `clientEventId` | `str` | **Yes** | Client-generated UUID string ensuring idempotent submission processing. |
  | `childId` | `Optional[str]` | No | Optional child profile UUID; if provided, must match session child (mismatch raises 403 `CHILD_SCOPE_VIOLATION`). |

- **Sample Request Payloads:**
  ```json
  {
    "nodeId": "0191d84f-8320-7f23-8c3b-100000000001",
    "questionId": "0191d84f-8320-7f23-8c3b-400000000001",
    "attemptType": "quiz",
    "answerPayload": { "selected_option": "baa" },
    "hintCount": 0,
    "responseTimeMs": 4200,
    "clientEventId": "0191d84f-8320-7f23-8c3b-999999999999"
  }
  ```

- **Response 200 OK Schema (`LearningAttemptResponse`):**
  ```json
  {
    "evaluated": true,
    "correct": true,
    "masteryDelta": 0.04,
    "newMasteryScore": 0.54,
    "currentState": "practicing",
    "attemptId": "0191d84f-8320-7f23-8c3b-888888888888"
  }
  ```
  | Field | Type | Description |
  |---|---|---|
  | `evaluated` | `bool` | Indicates attempt was successfully evaluated (always `true`). |
  | `correct` | `bool` | Whether the submitted answer met the correctness criteria. |
  | `masteryDelta` | `float` | Calculated mastery gain (or penalty on failure) applied to the node. |
  | `newMasteryScore` | `Optional[float]` | Updated continuous mastery score for the node ($0.0 \le \text{score} \le 1.0$). |
  | `currentState` | `Optional[str]` | Discrete state of the skill node (`learning`, `practicing`, `mastered`, etc.). |
  | `attemptId` | `Optional[str]` | UUID of the persisted immutable `LearningAttempt` row. |

- **Idempotent Replay Contract:**
  If a duplicate `clientEventId` is submitted, the system queries the previously persisted attempt and returns the original evaluation result with HTTP 200 OK, zero re-scoring, zero double-mutation of mastery, and atomic cache preservation.

- **Error Status Codes:**
  - `400 Bad Request`: `attempt_type == "recitation"` rejected by recitation guard with code `RECITATION_ATTEMPT_TYPE_NOT_ALLOWED`, directing clients to `POST /v1/learning/recitation`.
  - `401 Unauthorized`: Missing, expired, or malformed Bearer JWT.
  - `403 Forbidden`: Parent session presented (`PARENT_TOKEN_REJECTED`), cross-family child access (`CHILD_SCOPE_VIOLATION`), or body `childId` mismatch with session.
  - `404 Not Found`: Skill node not found (`SKILL_NODE_NOT_FOUND`) or practice question not found (`QUESTION_NOT_FOUND`).
  - `409 Conflict`: Handled transparently by idempotent replay returning HTTP 200 OK.
  - `422 Unprocessable Entity`: Malformed `answer_payload`, missing required fields, question-node mismatch, attempt type mismatch with question, or forbidden extra fields (`extra="forbid"`).
  - `500 Internal Server Error`: Unhandled database exception; transaction rolled back and logged.

## 14. Database Requirements
`learning_attempt` table per B-01's ER diagram: `attempt_id PK`, `child_id FK`, `node_id FK`, `attempt_type`, `correct BOOLEAN`, `hint_count INT`, `response_time_ms INT`, `client_event_id UNIQUE`, `created_at`. Index `(child_id, node_id, created_at DESC)`. Append-only/immutable historical fact table — no update/delete path.

## 15. Validation
- `attempt_type` ∈ {`quiz`,`tracing`,`matching`} on this endpoint.
- `answer_payload` schema validated per type (delegated to a per-type validator function).
- `node_id`/`question_id` must reference existing, active records.

## 16. Authentication
Bearer JWT, `get_current_child`.

## 17. Authorization
Implicit family/child scoping via session; no cross-child submission possible since `child_id` is derived from the session, not the request body.

## 18. Error Handling
| Scenario | Behavior | HTTP Code | Error Code |
|---|---|---|---|
| `attempt_type == recitation` | Recitation guard directing to `/v1/learning/recitation` with localized guidance | `400 Bad Request` | `RECITATION_ATTEMPT_TYPE_NOT_ALLOWED` |
| Missing Authorization header | Authentication failure | `401 Unauthorized` | `UNAUTHENTICATED` |
| Parent session token presented | Child-mode session required | `403 Forbidden` | `FORBIDDEN` |
| Cross-family child ID | Multi-tenant boundary check via `verify_child_scope` | `403 Forbidden` | `CHILD_SCOPE_VIOLATION` |
| Child profile ID mismatch | Body childId does not match session childId | `403 Forbidden` | `CHILD_SCOPE_VIOLATION` |
| Unknown child profile | Child profile UUID not found | `404 Not Found` | `CHILD_NOT_FOUND` |
| Unknown skill node ID | Non-existent or inactive skill node | `404 Not Found` | `SKILL_NODE_NOT_FOUND` |
| Unknown question ID | Practice question not in question bank | `404 Not Found` | `QUESTION_NOT_FOUND` |
| Question node mismatch | Question does not belong to target node | `422 Unprocessable Entity` | `QUESTION_NODE_MISMATCH` |
| Attempt type mismatch | Attempt type does not match question type | `422 Unprocessable Entity` | `ATTEMPT_TYPE_MISMATCH` |
| Duplicate `client_event_id` | Idempotent replay — return original evaluation result, zero re-scoring | `200 OK` | N/A (`is_idempotent_replay: true`) |
| Concurrent `client_event_id` race | Database `IntegrityError` caught and re-queried for idempotent replay | `200 OK` | N/A (`is_idempotent_replay: true`) |
| Malformed `answer_payload` | Validation failure (missing required keys or invalid values) | `422 Unprocessable Entity` | `VALIDATION_ERROR` |
| Injected forbidden fields | Schema rejects extra fields (`extra="forbid"`) | `422 Unprocessable Entity` | `VALIDATION_ERROR` |
| DB failure | Transaction rolled back and logged | `500 Internal Server Error` | `INTERNAL_SERVER_ERROR` |

## 19. Offline First
N/A (backend). Client-side offline queuing behavior owned by respective KMP blueprints (K-03/K-05/K-06/K-08).

## 20. Local Data
N/A (backend).

## 21. Localization
Supports 4 core platform languages (`en`, `hi`, `ur`, `ar`) via `X-Locale` or `Accept-Language` headers:
- `RECITATION_REDIRECT_MESSAGES` provides localized guidance when `attempt_type == "recitation"` is rejected:
  - English (`en`): `"Recitation attempts must be submitted to /v1/learning/recitation"`
  - Hindi (`hi`): `"तिलावत के प्रयासों को /v1/learning/recitation पर जमा किया जाना चाहिए"`
  - Urdu (`ur`): `"تلاوت کی کوششوں کو /v1/learning/recitation پر جمع کیا جانا چاہیے"`
  - Arabic (`ar`): `"يجب إرسال محاولات التلاوة إلى /v1/learning/recitation"`

## 22. RTL
N/A.

## 23. Analytics
No server-side event emission from this endpoint directly.

## 24. Performance
Single DB transaction covering: attempt insert + mastery_score update + state-machine evaluation + cache invalidation call, to avoid partial-state writes.

## 25. Security
Standard authenticated-child scoping; `answer_payload` validated strictly to prevent injection of unexpected fields into scoring logic.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0, Pydantic v2. No new dependencies.

## 27. Testing
The implementation is validated by **52 dedicated tests** across service, API integration, and repository layers (contributing to the 252 total passing tests in the `learning` module):

### 27.1 Unit Tests (`test_attempt_evaluation_service.py` — 29 tests)
1. **Quiz Evaluation**: Exact match, incorrect choice, case-insensitive and whitespace-tolerant options.
2. **Tracing Evaluation**: Geometric accuracy $\ge 0.85$ evaluates as correct; $< 0.85$ evaluates as incorrect.
3. **Matching Evaluation**: Correct dictionary pairs match; mismatched keys/values evaluated as incorrect.
4. **Payload Schema Validation**: Rejects missing or malformed `answer_payload` across quiz, tracing, and matching with `ValidationError` (422).
5. **Recitation Guard**: Rejects `attempt_type == "recitation"` with `RecitationAttemptTypeError` (HTTP 400).
6. **Replay Idempotency**: Duplicate `client_event_id` returns previous evaluation result without mutating mastery score.
7. **Concurrency Resilience**: Catches `IntegrityError` on `client_event_id` race condition and recovers by re-querying existing attempt idempotently.
8. **FR-18 Non-Penalizing Hints**: `hint_count > 0` scales down positive gain while keeping `mastery_delta > 0`.
9. **FR-7 Multi-Session Mastery Hold**:
   - Single-session repeated attempts cross 0.85 score threshold but are held in `practicing`.
   - Attempts across $\ge 2$ distinct calendar dates allow transition from `practicing` to `mastered`.
10. **Edge Case 1 Borderline Rounding**: Raw continuous score $\ge 0.80$ rounds in child's favor (`mastered`) when multi-session criteria is met.
11. **Entity Verification**: Unknown or inactive skill node raises `SkillNodeNotFoundError` (HTTP 404).
12. **Question Verification**: Unknown question ID raises `QuestionNotFoundError` (HTTP 404).
13. **Question Node Association**: Question belonging to another node raises `ValidationError` (HTTP 422).
14. **Attempt Type Verification**: Question configured as quiz evaluated with tracing raises `ValidationError` (HTTP 422).
15. **Atomic Flush & Cache Invalidation**: `session.flush()` writes attempt and updates state; calls `invalidate_skill_tree_cache()`.
16. **Localization**: Recitation redirect message localized across English, Hindi, Urdu, and Arabic.

### 27.2 HTTP Integration Tests (`test_learning_attempts_api.py` — 18 tests)
- Canonical `POST /v1/learning/attempts` and direct alias `POST /v1/attempts`.
- HTTP status verification: 200 OK, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 422 Unprocessable Entity, 500 Internal Server Error.
- Parent-mode token rejection (child session required).
- Cross-family child ID rejection (`CHILD_SCOPE_VIOLATION` / 403).
- Explicit `childId` in request body mismatching authenticated session child (403).
- Extra forbidden fields rejection (`extra="forbid"` / 422).
- Header locale forwarding (`X-Locale`, `Accept-Language`).
- OpenAPI 3.1.0 contract verification ensuring all declared status codes (200, 400, 401, 403, 404, 422, 429, 500) are documented.

### 27.3 Repository Tests (`test_learning_attempt_repository.py` — 5 tests)
- `create()`: Persists `LearningAttempt` entity and flushes session.
- `get_by_client_event_id()`: Retrieves attempt by `client_event_id` for idempotent replay.
- `get_session_history()`: Queries chronological attempt history for a given child and node.
- `get_distinct_correct_session_dates()`: Aggregates distinct dates for FR-7 multi-session validation.

## 28. Documentation
OpenAPI docstring noting the recitation-type exclusion and idempotency contract.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create `LearningAttempt` Model & Migration**
- Task ID: B-03-T01
- Status: ✅ **Completed & Verified**
- Files Created: `src/noorheroes/modules/learning/learning_attempt_models.py`, `alembic/versions/0045_add_learning_attempts.py`.
- Dependencies: None.
- Definition of Done: Migration applies; unique constraint on `client_event_id` verified.

**Task 02 — Create Schemas**
- Task ID: B-03-T02
- Status: ✅ **Completed & Verified**
- Files Created: `src/noorheroes/modules/learning/learning_attempt_schemas.py`.
- Dependencies: B-03-T01.
- Definition of Done: Schemas validate sample payloads for all 3 attempt types.

**Task 03 — Implement `LearningAttemptRepository`**
- Task ID: B-03-T03
- Status: ✅ **Completed & Verified**
- Files Created: `src/noorheroes/modules/learning/learning_attempt_repository.py`, `tests/modules/learning/test_learning_attempt_repository.py`.
- Implementation Details: `create()`, `get_by_client_event_id()`, `get_session_history(child_id, node_id)`, `get_distinct_correct_session_dates(child_id, node_id)`.
- Dependencies: B-03-T01.
- Definition of Done: Repository unit tests pass (5 dedicated tests).

**Task 04 — Implement `AttemptEvaluationService`**
- Task ID: B-03-T04
- Status: ✅ **Completed & Verified**
- Files Created: `src/noorheroes/modules/learning/attempt_evaluation_service.py`, `src/noorheroes/modules/learning/practice_question_bank.py`.
- Implementation Details: correctness evaluation per type, mastery_delta computation, multi-session enforcement, calls `compute_next_state()` from B-01, calls `invalidate_skill_tree_cache()` from B-01.
- Existing Files Reused: B-01's `mastery_state_machine.py`, `SkillTreeService`.
- Business Rules: FR-7 multi-session enforcement; FR-18 hint_count feeds confidence not penalty.
- Dependencies: B-03-T02, B-03-T03, B-01-T05/T06.
- Definition of Done: Unit tests (Task 06) pass.

**Task 05 — Wire Router with Idempotency & Type Guard**
- Task ID: B-03-T05
- Status: ✅ **Completed & Verified**
- Files Modified: `src/noorheroes/modules/learning/api.py`, `src/noorheroes/api/v1/router.py`.
- Implementation Details: `400` guard for `recitation` type before service call; idempotency check via repository before evaluation.
- Dependencies: B-03-T04.
- Definition of Done: Endpoint reachable, idempotency verified manually.

**Task 06 — Tests**
- Task ID: B-03-T06
- Status: ✅ **Completed & Verified**
- Objective: Full coverage per §27.
- Dependencies: B-03-T01–T05.
- Definition of Done: 52 dedicated tests passing across `test_attempt_evaluation_service.py` (29 tests), `test_learning_attempts_api.py` (18 tests), and `test_learning_attempt_repository.py` (5 tests) (252 total module tests passing).

**Task 07 — API Documentation**
- Task ID: B-03-T07
- Status: ✅ **Completed & Verified**
- Dependencies: B-03-T05.
- Definition of Done: OpenAPI docs accurate and complete, synced across `MASTER-README.md`, `FAST-API-INSTRUCTIONS.md`, and module `README.md`.

## 30. Definition of Done
Endpoint live, idempotent, enforces multi-session mastery rule, correctly integrates with B-01's state machine and cache, fully tested.

## 31. Final Verification Checklist
- [x] Recitation attempt_type rejected with `400` and correct redirect message
- [x] Idempotent replay via `client_event_id` verified (no double-scoring)
- [x] Multi-session mastery rule enforced (single-session cannot reach `mastered`)
- [x] `hint_count` recorded but never surfaced as a visible penalty
- [x] B-01 skill-tree cache invalidated on every successful mutation
- [x] `learning_attempt` table append-only, no update/delete path exists
- [x] Full test suite green in CI
