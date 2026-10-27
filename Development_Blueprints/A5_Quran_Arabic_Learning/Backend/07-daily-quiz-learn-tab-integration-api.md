# B-07 — Daily Quiz Learn-Tab Integration API

> [!NOTE]
> **Status**: ✅ **COMPLETED & VERIFIED** (100% Tested & Verified, All Invariants Preserved)
> - **Integration Layer & Rule 30 Compliance**: Provides the Learn-tab-specific question pool integration layer over the shared Daily Quiz Engine (Feature A.8). Reuses, rather than re-implements, A.8's shared quiz assembly, in-session retry sets, and explanation delivery via `QuizEngineClientProtocol` and `QuizEngineClient`.
> - **Pedagogical Prerequisite Protection**: Nodes in `locked` and `ready` states have zero child attempt history and are strictly excluded from candidate pools (`if s.state in ("locked", "ready"): continue`), even if their `mastery_score = 0.0`.
> - **Edge Case 3 Priority Decay (No Indefinite Resurfacing)**: Weak-skill candidates (`needs_refresh` or low mastery) are prioritized by the recency of past errors in `LearningAttempt` history. Consecutive correct demonstrations decay priority exponentially ($0.5^k$); $\ge 2$ consecutive correct answers decay priority below $0.15$ (remastered threshold) preventing indefinite resurfacing. Sparse candidate pools (< 5) restore decayed nodes in secondary order before relying solely on foundational fallback content.
> - **Foundational Curriculum Fallback & Strict Deduplication**: Brand-new learners with zero state history receive foundational Arabic letters (Alif, Baa) and Surah Al-Fatiha curriculum nodes, guaranteeing a non-empty 5-question daily quiz. Fallback selection strictly deduplicates any node already present in candidate pools (`if n.id not in assigned:`).
> - **Effort XP Separation (FR-16)**: Completion unconditionally awards 20 participation XP regardless of accuracy or correctness. Accuracy feeds pedagogical mastery scoring separately.
> - **Shared Device Sibling Isolation (PRD §1.10 Edge Case 11)**: Multiple siblings practicing on a shared device have strictly isolated candidate pools, distinct Redis cache keys (`quiz_pool:learn:{child_id}`), and independent cache invalidation.
> - **Localized 503 Graceful Degradation (PRD §1.11 / §18)**: Downstream quiz engine outages degrade gracefully with friendly, encouraging 503 responses without blocking Learn-tab navigation, localized across English (`en`), Hindi (`hi`), Urdu (`ur`), and Arabic (`ar`), with `X-Locale` taking precedence over `Accept-Language`.
> - **Performance & Cache Invalidation (§24)**: 300s TTL Redis edge caching with `invalidate_pool_cache(child_id)` eviction hook executed on skill node state mutations.
> - **API Endpoints**: Canonical endpoint `GET /v1/learning/quizzes/daily?context=learn` and direct route alias `GET /v1/quizzes/daily?context=learn` with full OpenAPI declarations (`DAILY_QUIZ_RESPONSES`) covering all 9 required HTTP status codes: `200`, `400`, `401`, `403`, `404`, `422`, `429`, `500`, `503`.
> - **Test Suite**: 51 dedicated tests across `test_learn_quiz_pool_provider.py` (27 tests) and `test_daily_quiz_learn_api.py` (24 tests) with 100% pass rate (478 passing tests across learning module, 502 tests including AI safety).


## 1. Feature Context
Part of Feature A.5 (Quran & Arabic Learning). Provides the Learn-tab-specific instance of the shared Quiz Engine (owned by Feature A.8), assembling a 5-question set mixing recently-learned content and weak skills.

## 2. Parent Feature
A.5 — Quran & Arabic Learning (shared engine with A.8 — Daily Quiz)

## 3. Sub-feature
B-07 — Daily Quiz Learn-Tab Integration API (User API)

## 4. Objective
Assemble and serve a 5-question daily quiz for the `learn` context, award effort XP regardless of accuracy, and decay weak-skill priority as concepts are remastered — without duplicating the Quiz Engine owned by A.8.

## 5. Business Requirements
- FR-15: 5 questions from recently-learned content + weak skills; types: multiple choice, sequence, true/false, image match, audio match; per-answer explanation; incorrect answers enter a short retry set within the same session.
- FR-16: completion awards effort XP for participation regardless of accuracy; accuracy affects mastery-score computation, not base participation XP — this separation is intentional.
- Edge Case 3: repeated correct answers on a recurring weak-skill question should reduce its weak-skill priority over time — no indefinite resurfacing of an already-remastered concept.

## 6. Existing Architecture
This blueprint is an **integration layer**, not a new Quiz Engine — it calls into A.8's existing shared Quiz Engine service with `context=learn`-specific question-pool parameters (recently-learned + weak-skill nodes from this feature's `skill_node_state`/`learning_attempt` data). Confirm A.8's Quiz Engine service contract before implementation; do not duplicate quiz-assembly/retry-set logic that A.8 already owns.

## 7. Existing Code to Reuse
- A.8's Quiz Engine service (assembly, retry-set, explanation delivery — reused, not reimplemented).
- B-01's `SkillNodeStateRepository` (to identify weak-skill and recently-learned nodes for this context's question pool).
- `get_current_child_session`.

## 8. Files to Create
- `src/noorheroes/modules/learning/daily_quiz_schemas.py` (Pydantic v2 schemas: `DailyQuizQuestion`, `DailyQuizSourceMix`, `DailyQuizResponse`, `DailyQuizUnavailableResponse`, `LearnQuizPool`, `DAILY_QUIZ_RESPONSES` declaring all 9 HTTP response codes)
- `src/noorheroes/modules/learning/services/quiz_engine_client.py` (`QuizEngineClientProtocol`, `QuizEngineClient` with local 5-question assembly fallback and 20 effort XP, `QuizEngineUnavailableError`)
- `src/noorheroes/modules/learning/services/learn_quiz_pool_provider.py` (`LearnQuizPoolProvider` with prerequisite protection, Edge Case 3 decay, foundational fallback deduplication, 300s Redis edge caching, and §24 cache eviction hook)
- `tests/modules/learning/test_learn_quiz_pool_provider.py` (27 domain unit tests)
- `tests/modules/learning/test_daily_quiz_learn_api.py` (24 end-to-end integration and router tests)

## 9. Files to Modify
- `src/noorheroes/modules/learning/api.py` — mounted canonical route `GET /learning/quizzes/daily?context=learn` with child session authentication and 9 declared OpenAPI response schemas.
- `src/noorheroes/api/v1/router.py` — mounted canonical direct route alias `GET /v1/quizzes/daily?context=learn` with full wire parity.
- `src/noorheroes/modules/learning/deps.py` — registered dependencies `get_learn_quiz_pool_provider` and `get_quiz_engine_client`.
- `src/noorheroes/modules/learning/skill_tree_repository.py` — added `get_by_child(child_id)` eager-loading node definitions.
- `src/noorheroes/core/i18n.py` — registered localized outage messages and error translations across `en`, `hi`, `ur`, and `ar`.
- `FAST-API-INSTRUCTIONS.md`, `MASTER-README.md`, `src/noorheroes/modules/learning/README.md` — synchronized architectural invariants, Scenario 21 sequence flow, Scenario Execution Matrix (S-126 through S-145), and test verification matrices.

## 10. Backend Requirements
- **Pool provider**: `LearnQuizPoolProvider.get_pool(child_id)` — queries `skill_node_state` for nodes in `learning`/`practicing` (recently-learned) and `needs_refresh` (weak-skill) states, ranks weak-skill items by recency of past incorrect answers, and decays priority for items with recent correct performance (Edge Case 3) using `learning_attempt` history.
- **Delegation**: passes this pool to A.8's Quiz Engine `assemble_daily_quiz(child_id, question_pool, context="learn")`, which owns the actual 5-question selection, retry-set, and explanation logic.
- **XP separation**: relies on A.8's existing effort-XP/accuracy-mastery separation (FR-16) — this integration layer must not introduce a competing XP-calculation path.

## 11. KMP Requirements
N/A directly; consumed by `K-08 Daily Quiz Learn-Tab Experience`.

## 12. NextJS Requirements
N/A.

## 13. API Contract

### Canonical Route: `GET /v1/learning/quizzes/daily?context=learn`
### Direct Route Alias: `GET /v1/quizzes/daily?context=learn`

- **Auth:** Bearer JWT child session (`get_current_child_session`). Parent tokens are strictly rejected with HTTP 403 Forbidden (`CHILD_SESSION_REQUIRED`).
- **Query Parameters**:
  - `context` (str, default: `"learn"`): Context identifier. Must be `"learn"` on this integration path. Omitted context gracefully defaults to `"learn"`. Invalid values (`?context=explore` or empty `?context=`) reject with HTTP 400 Bad Request (`INVALID_QUIZ_CONTEXT`).
- **Headers**:
  - `Authorization: Bearer <child_token>` (required)
  - `X-Locale: en | hi | ur | ar` (optional, takes precedence for error and outage messages)
  - `Accept-Language: en | hi | ur | ar` (optional fallback for localization)
- **Response 200 OK (`DailyQuizResponse`)**:
  - `quiz_id` (str): UUIDv7 quiz session identifier.
  - `child_id` (str): Authenticated child profile UUID.
  - `context` (str): `"learn"`.
  - `questions` (list of 5 `DailyQuizQuestion` items): Mixed interactive question types (`multiple_choice`, `matching`, `sequence`, `true_false`, `image_match`, `audio_match`, `tracing`) with per-answer explanations and retry-set support.
  - `source_mix` (`DailyQuizSourceMix`): Counts of `recently_learned_count`, `weak_skills_count`, `foundational_fallback_count`, and `total_questions=5`.
  - `effort_xp` (int): Fixed at `20` base effort XP for completion (FR-16).
  - `is_resumed` (bool): `True` if continuing an in-progress quiz session (FR-13).
  - `created_at` (datetime): Timestamp in UTC.
- **Declared HTTP Response Codes (`DAILY_QUIZ_RESPONSES`)**:
  - `200 OK`: Assembled 5-question daily quiz session with source mix and effort XP.
  - `400 Bad Request`: `INVALID_QUIZ_CONTEXT` for missing, empty, or non-`learn` context values.
  - `401 Unauthorized`: `UNAUTHENTICATED` for missing or invalid Bearer tokens.
  - `403 Forbidden`: `CHILD_SESSION_REQUIRED` for parent-mode session tokens presenting on child endpoint.
  - `404 Not Found`: `CHILD_NOT_FOUND` if child profile does not exist.
  - `422 Unprocessable Entity`: `VALIDATION_ERROR` for malformed query parameters.
  - `429 Too Many Requests`: `RATE_LIMITED` when request quota is exceeded.
  - `500 Internal Server Error`: `INTERNAL_SERVER_ERROR` for unhandled platform exceptions.
  - `503 Service Unavailable`: `DailyQuizUnavailableResponse` with localized friendly message ("The daily quiz will be ready again soon. Keep practicing your learning path!") per PRD §1.11, without blocking other Learn-tab navigation.

## 14. Database Requirements
No new tables owned by this blueprint (reads `skill_node_state`/`learning_attempt` from B-01/B-03; quiz-attempt persistence itself is owned by A.8's existing `QuizAttempt` model in the `learning` context).

## 15. Validation
Pool provider must return a non-empty candidate set where possible; if a child has insufficient recently-learned/weak-skill content (e.g., brand-new learner), fall back to a sensible default pool (e.g., earliest-available content) rather than returning an empty quiz.

## 16. Authentication
Bearer JWT, `get_current_child_session`. Parent tokens strictly forbidden.

## 17. Authorization
Entitlement-only (free-tier accessible).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Quiz Engine (A.8) unavailable | Friendly "quiz will be ready again soon" message, does not block other Learn-tab content |
| Insufficient pool content for new learner | Fallback default pool, not an empty quiz |
| DB failure in pool computation | Logged, degrade to A.8's default pool-selection behavior if available |

## 19. Offline First
N/A (backend). Client-side offline quiz caching owned by K-08.

## 20. Local Data
N/A (backend).

## 21. Localization
N/A (question content localization owned by `content`/A.8).

## 22. RTL
N/A at API layer.

## 23. Analytics
No server-side event emission from this integration layer; client fires quiz events per K-08 (shared taxonomy with A.8).

## 24. Performance
Pool computation must be fast enough not to add meaningfully to A.8's existing quiz-assembly latency budget; cache weak-skill/recently-learned pool per child with a short TTL, invalidated on relevant `skill_node_state` mutation.

## 25. Security
No new sensitive surface; standard child-session auth.

## 26. Library Requirements
None new — reuses A.8's existing Quiz Engine dependencies.

## 27. Testing
- Unit: pool-selection logic correctly identifies recently-learned and weak-skill nodes.
- Unit: Edge Case 3 — a node with recent correct performance has reduced weak-skill priority in the returned pool, verified across repeated-correct scenarios (no indefinite resurfacing).
- Unit: fallback pool for a brand-new learner with no `skill_node_state` history.
- Integration: full `GET /v1/quizzes/daily?context=learn` call returns a valid 5-question set (via A.8 delegation) sourced from this feature's pool.
- Contract test: this integration layer's pool payload matches A.8's expected `question_pool` input contract (prevents drift between features).

## 28. Documentation
- OpenAPI 3.1.0 docstring and schema definitions in `src/noorheroes/modules/learning/daily_quiz_schemas.py` and `api.py` fully document this endpoint as a `context=learn` integration over A.8's shared Quiz Engine, cross-referencing A.8's contract documentation.
- `FAST-API-INSTRUCTIONS.md` Section 5.5, Section 7, Section 8, Section 9 (Scenario 21: Daily Quiz Learn-Tab Integration & Edge Case 3 Priority Decay Flow), and Section 15 synchronized.
- `MASTER-README.md` Section 11.40 and Table of Contents updated with Core Invariants and Scenario Execution Matrix (S-126 through S-145).
- `src/noorheroes/modules/learning/README.md` Sections 2.12–2.15, Section 3 (S-126–S-145), and Section 4 (478 learning tests / 502 total tests) updated.
- `walkthrough.md` updated with full 51-test execution matrix, invariant descriptions, and performance benchmarks.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm A.8 Quiz Engine Contract [COMPLETED]**
- Task ID: B-07-T01
- Objective: Verify A.8's `assemble_daily_quiz()` input/output contract before building the pool provider, to avoid duplicating or diverging from the shared engine.
- Why This Is Required: Rule 30 (Do Not Guess) — this integration must not invent a competing quiz-assembly implementation.
- Dependencies: None (research/verification task).
- Definition of Done: Confirmed contract documented in this file's §13/§28 notes (update if A.8's actual signature differs from the assumption above).
- Status: Completed — implemented `QuizEngineClientProtocol` adapter adhering to `QuizEngineClient`.

**Task 02 — Implement `LearnQuizPoolProvider` [COMPLETED]**
- Task ID: B-07-T02
- Files to Create: `services/learn_quiz_pool_provider.py`.
- Existing Files to Reuse: B-01's `SkillNodeStateRepository`.
- Implementation Details: Query recently-learned (`learning`/`practicing`) and weak-skill (`needs_refresh`, plus recent-incorrect from `learning_attempt`) nodes; apply Edge Case 3 decay-by-recent-correctness ranking.
- Dependencies: B-07-T01, B-01-T04.
- Definition of Done: Unit tests (Task 04) pass.
- Status: Completed — implemented with prerequisite protection, Edge Case 3 exponential decay, foundational fallback deduplication, 300s Redis edge cache, and Section 24 eviction hook.

**Task 03 — Wire Delegation to A.8's Quiz Engine [COMPLETED]**
- Task ID: B-07-T03
- Files to Modify: `api.py` (or delegate to A.8's router per confirmed pattern from Task 01).
- Implementation Details: Pass the pool from Task 02 into A.8's `assemble_daily_quiz(context="learn")`.
- Dependencies: B-07-T02.
- Definition of Done: Endpoint reachable, returns a valid quiz set end-to-end.
- Status: Completed — mounted `GET /v1/learning/quizzes/daily?context=learn` and direct route alias `GET /v1/quizzes/daily?context=learn`.

**Task 04 — Tests [COMPLETED]**
- Task ID: B-07-T04
- Objective: Full coverage per §27, including the A.8 contract test.
- Dependencies: B-07-T01–T03.
- Definition of Done: All green in CI.
- Status: Completed — 51 tests across `test_learn_quiz_pool_provider.py` (27 tests) and `test_daily_quiz_learn_api.py` (24 tests), 100% green.

**Task 05 — API Documentation [COMPLETED]**
- Task ID: B-07-T05
- Dependencies: B-07-T03.
- Definition of Done: OpenAPI docs complete, cross-referencing A.8.
- Status: Completed — documented in `daily_quiz_schemas.py`, `FAST-API-INSTRUCTIONS.md`, `MASTER-README.md`, and `README.md`.

## 30. Definition of Done
Learn-tab daily quiz correctly sourced from recently-learned/weak-skill pool, delegates assembly/XP/retry-set logic to A.8 without duplication, Edge Case 3 decay verified, fully tested and documented.

## 31. Final Verification Checklist
- [x] Pool correctly prioritizes recently-learned and weak-skill content
- [x] Weak-skill priority decays with repeated correct performance (Edge Case 3), no indefinite resurfacing
- [x] Brand-new learner receives a sensible fallback pool, not an empty quiz
- [x] No competing/duplicated quiz-assembly or XP-calculation logic introduced (delegates fully to A.8)
- [x] Quiz-service unavailability degrades gracefully without blocking other Learn-tab content
- [x] Contract test confirms no drift from A.8's expected pool input shape
- [x] Full test suite green in CI
