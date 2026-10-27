# B-02 — Placement Check API

> [!NOTE]
> **Status**: ✅ **COMPLETED & VERIFIED** (100% Tested & Verified, All Invariants Preserved)
> - **Models & Migration**: `PlacementCheckLog` & `SpacedReviewSchedule` in `src/noorheroes/modules/learning/placement_check_models.py`, Alembic migration `alembic/versions/0044_add_placement_check_and_spaced_review.py`.
> - **Evaluation Engine**: Content-driven question bank in `placement_question_bank.py`, pure scoring and Edge Case 9 Tajweed safeguards in `placement_check_service.py`.
> - **Idempotency & Security**: HTTP 409 duplicate submission guard returning prior evaluated results, admin re-check override with flag reset, family-scoped child ownership enforcement (`CHILD_SCOPE_VIOLATION` / `403`).
> - **Atomic Transactions & Invalidation**: Single-transaction atomic write (`session.flush()`), immediate B-01 Redis cache invalidation (`invalidate_skill_tree_cache`).
> - **Localization**: 4-language i18n localization (`en`, `hi`, `ur`, `ar`).
> - **API Endpoints**: Canonical `POST /v1/learning/placement-check` and `GET /v1/learning/placement-check/questions`, plus direct aliases `POST /v1/placement-check` and `GET /v1/placement-check/questions`.
> - **Test Suite**: 51 dedicated tests across `test_placement_check_service.py` (17 tests), `test_placement_check_api.py` (24 tests), and `test_placement_check_repository.py` (10 tests) with 100% pass rate (252 passing tests across learning module).

## 1. Feature Context
Part of Feature A.5 (Quran & Arabic Learning). Lets a first-time learner skip redundant beginner content by answering a short set of questions that seed their skill-tree state, respecting prior knowledge.

## 2. Parent Feature
A.5 — Quran & Arabic Learning

## 3. Sub-feature
B-02 — Placement Check API (User API)

## 4. Objective
Accept placement-check responses and produce recommended starting nodes and provisional skill-node states, with special handling so foundational Tajweed prerequisites are never silently skipped.

## 5. Business Requirements
- Acceptance Criteria: first-time skill-tree render offers a placement-check option before defaulting into Surah 1.
- Edge Case 9: a placement check that would place a child past Surah-tree nodes with un-verified Tajweed prerequisites must either (a) mark those prerequisite nodes provisionally `Ready` pending a light confirmation check, or (b) explicitly schedule them for near-term review — never silently skip them, since recitation correctness depends on them.

## 6. Existing Architecture
Same modular monolith / `learning` context described in B-01. This endpoint writes into the same `skill_node_state` table B-01 reads and must invalidate B-01's Redis cache on write.

## 7. Existing Code to Reuse
- `SkillNodeRepository`, `SkillNodeStateRepository` from B-01.
- `mastery_state_machine.compute_next_state()` from B-01 (for initializing provisional states consistently).
- `SkillTreeService.invalidate_skill_tree_cache()` from B-01.
- `get_current_child` dependency.

## 8. Files Created
- `src/noorheroes/modules/learning/placement_check_models.py` — `PlacementCheckLog`, `SpacedReviewSchedule` ORM models.
- `src/noorheroes/modules/learning/placement_check_schemas.py` — `PlacementCheckRequest`, `PlacementCheckResponse`, `PlacementQuestionOption`, `PlacementQuestionResponse`, `LocalizedQuestionBankResponse`, `PlacementCheckRecheckRequest` Pydantic v2 schemas.
- `src/noorheroes/modules/learning/placement_question_bank.py` — content-driven question bank across all learning tracks with localized prompts and options in EN, HI, UR, AR.
- `src/noorheroes/modules/learning/placement_check_repository.py` — `PlacementCheckLogRepository` (including `set_recheck_allowed`), `SpacedReviewScheduleRepository`.
- `src/noorheroes/modules/learning/placement_check_service.py` — `PlacementCheckService` scoring, Edge Case 9 Tajweed safeguards, 409 idempotency handling, question bank retrieval, atomic flush, cache invalidation.
- `alembic/versions/0044_add_placement_check_and_spaced_review.py` — reversible migration for `placement_check_log` and `spaced_review_schedule`.
- `tests/modules/learning/test_placement_check_service.py` — 17 unit/service tests.
- `tests/modules/learning/test_placement_check_api.py` — 24 API integration and security tests.
- `tests/modules/learning/test_placement_check_repository.py` — 10 repository data access tests.

## 9. Files Modified
- `src/noorheroes/modules/learning/api.py` — mounted `POST /v1/learning/placement-check` and `GET /v1/learning/placement-check/questions`.
- `src/noorheroes/api/v1/router.py` — mounted direct aliases `POST /v1/placement-check` and `GET /v1/placement-check/questions`.
- `src/noorheroes/modules/learning/deps.py` — registered repositories and service dependencies.
- `src/noorheroes/modules/learning/models/__init__.py` — registered models.
- `FAST-API-INSTRUCTIONS.md` — synchronized Sections 5.5, 6, 7, 8, 9, 15.
- `MASTER-README.md` — synchronized Section 11.35 and routes table.

## 10. Backend Requirements
- **Router**: `POST /v1/learning/placement-check`, `get_current_child`.
- **Service**: `PlacementCheckService.evaluate(child_id, responses)` — scores responses against a placement-check question bank (content-driven, sourced from `content` context), determines `recommended_starting_nodes`, and for any node whose prerequisites were not directly tested, applies the Edge Case 9 rule: Tajweed-track prerequisite nodes get `provisional_state="ready"` + a `spaced_review_schedule` entry for near-term confirmation (calls into B-06's scheduling table), non-Tajweed prerequisite nodes may be marked `ready` outright if response evidence supports it.
- **Idempotency**: a child may only have one "official" placement check; a second submission attempt is rejected (`409`) unless an admin-issued re-placement flag is set — return existing prior result instead of re-scoring.

## 11. KMP Requirements
N/A directly; consumed by `K-02 Placement Check Flow`.

## 12. NextJS Requirements
N/A.

## 13. API Contract

**`POST /v1/learning/placement-check`**
- **Auth:** Bearer (child-mode)
- **Request:**
```json
{ "child_id": "uuid", "responses": [ { "question_id": "uuid", "answer": "..." } ] }
```
- **Response 200:**
```json
{
  "recommended_starting_nodes": ["uuid", "uuid"],
  "provisional_states": { "uuid": "ready" }
}
```
- **Authentication:** Bearer JWT, child-mode
- **Authorization:** `child_id` must match caller's family
- **Validation:** `responses` non-empty; each `question_id` must exist in the placement-check question bank
- **Error Responses:** `401`, `403`, `409` (already placed), `422` (malformed/incomplete responses), `500`

**`GET /v1/learning/placement-check/questions`**
- **Auth:** Bearer (child-mode)
- **Headers:** `X-Locale: en|hi|ur|ar` or `Accept-Language: en|hi|ur|ar`
- **Response 200:**
```json
{
  "total": 6,
  "locale": "en",
  "questions": [
    {
      "id": "q_diag_arab_01",
      "track": "arabic",
      "prompt": "Which letter makes the 'Baa' sound?",
      "options": [
        { "id": "opt_01", "text": "ب", "is_correct": true },
        { "id": "opt_02", "text": "ت", "is_correct": false }
      ]
    }
  ]
}
```
- **Authentication:** Bearer JWT, child-mode
- **Error Responses:** `401`, `403`, `500`

## 14. Database Requirements
No new tables. Writes to existing `skill_node_state` (from B-01) and `spaced_review_schedule` (from B-06 — this task has a soft dependency on B-06's table existing; if built out of order, create the table here and let B-06 reuse it). Add a `placement_check_completed_at` timestamp column to a per-child learning-profile record (extend `LearningProgress` model from the existing `learning` context, or add a dedicated `placement_check_log` table: `log_id PK`, `child_id FK`, `completed_at`, `recommended_starting_nodes JSONB`).

## 15. Validation
- `responses` array non-empty and each entry references a real question.
- Reject if child already has a `placement_check_log` row (idempotency).

## 16. Authentication
Bearer JWT, `get_current_child`.

## 17. Authorization
Family-scoped `child_id` check, identical pattern to B-01.

## 18. Error Handling
| Scenario | Behavior | HTTP Code |
|---|---|---|
| Duplicate submission | Return prior result in error details | `409 Conflict` |
| Incomplete/empty responses | Validation error on `responses` field | `422 Unprocessable Entity` |
| Unknown question_id | Unknown diagnostic question reference | `422 Unprocessable Entity` |
| Injected forbidden fields | Schema rejects extra fields (`extra="forbid"`) | `422 Unprocessable Entity` |
| Missing Authorization | Missing bearer token | `401 Unauthorized` |
| Parent session token | Child-mode session required | `403 Forbidden` |
| Cross-family child_id | Family boundary enforcement via `verify_child_scope` | `403 Forbidden` |
| Child profile not found | Non-existent profile UUID | `404 Not Found` |
| DB failure | Transaction rolled back and logged | `500 Internal Server Error` |

## 19. Offline First
N/A (backend).

## 20. Local Data
N/A (backend).

## 21. Localization
Question bank content is locale-resolved by the client/content service; this API deals only in `question_id`/`answer` identifiers.

## 22. RTL
N/A at API layer.

## 23. Analytics
No server-side event emission; client fires `placement_check_started`/`placement_check_completed` per K-02.

## 24. Performance
Single-transaction write (responses scoring + `skill_node_state` seeding + `spaced_review_schedule` seeding) to avoid partial-placement states on failure.

## 25. Security
Standard family-scoping; no elevated risk surface (no audio, no PII beyond existing child context).

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0, Pydantic v2. No new dependencies.

## 27. Testing
- Unit: scoring logic for a range of response patterns.
- Unit: Edge Case 9 branch — Tajweed prerequisite handling produces `ready`-provisional or near-term-review scheduling, never silent skip.
- Integration: full submission → skill_node_state + spaced_review_schedule rows created correctly.
- Integration: duplicate submission returns `409` with prior result, does not re-score.
- Integration: cross-family rejection.

## 28. Documentation
OpenAPI docstring explaining the Edge Case 9 behavior explicitly, since it's a non-obvious business rule.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create Schemas**
- Task ID: B-02-T01
- Status: ✅ **Completed & Verified**
- Objective: Define `PlacementCheckRequest`/`PlacementCheckResponse` Pydantic schemas per §13.
- Why Required: Type-safe contract for router.
- Files Created: `src/noorheroes/modules/learning/placement_check_schemas.py`.
- Dependencies: None.
- Definition of Done: Schemas validate sample payloads, enforce CamelCase alias generators, provide 4-track schema definitions.

**Task 02 — Create `placement_check_log` Table & Migration**
- Task ID: B-02-T02
- Status: ✅ **Completed & Verified**
- Objective: Persist idempotency record and recommended-nodes history.
- Existing Architecture Followed: Alembic migration pattern from B-01-T02.
- Files Created: `src/noorheroes/modules/learning/placement_check_models.py` (`PlacementCheckLog`, `SpacedReviewSchedule`) and migration `alembic/versions/0044_add_placement_check_and_spaced_review.py`.
- Dependencies: None.
- Definition of Done: Migration applies cleanly with reversible downgrade.

**Task 03 — Implement `PlacementCheckService.evaluate()`**
- Task ID: B-02-T03
- Status: ✅ **Completed & Verified**
- Objective: Core scoring + provisional-state logic, including Edge Case 9 handling.
- Existing Files Reused: `SkillNodeRepository`, `SkillNodeStateRepository`, `compute_next_state()`.
- Business Rules: Tajweed-track prerequisites never silently skipped — always `ready`-provisional + near-term review scheduling.
- Dependencies: B-02-T01, B-02-T02, B-01-T04/T05.
- Definition of Done: All scoring branches and Edge Case 9 invariant tests pass.

**Task 04 — Wire Idempotency Guard**
- Task ID: B-02-T04
- Status: ✅ **Completed & Verified**
- Objective: Reject duplicate submissions with `409` + prior result (unless admin re-check override is enabled).
- Dependencies: B-02-T03.
- Definition of Done: Duplicate-submission tests pass (HTTP 409 returns previously computed recommended nodes).

**Task 05 — Wire Router + Cache Invalidation**
- Task ID: B-02-T05
- Status: ✅ **Completed & Verified**
- Objective: Expose `POST /v1/learning/placement-check` (and direct alias `POST /v1/placement-check`); call B-01's `invalidate_skill_tree_cache()` after successful write.
- Files Modified: `src/noorheroes/modules/learning/api.py`, `src/noorheroes/api/v1/router.py`.
- Dependencies: B-02-T03, B-02-T04.
- Definition of Done: Endpoint reachable; subsequent `GET /v1/learning/paths` reflects new state immediately.

**Task 06 — Tests**
- Task ID: B-02-T06
- Status: ✅ **Completed & Verified**
- Objective: Full unit + integration coverage per §27.
- Dependencies: B-02-T01–T05.
- Definition of Done: 51 dedicated tests passing across `test_placement_check_service.py` (17 tests), `test_placement_check_api.py` (24 tests), and `test_placement_check_repository.py` (10 tests) (252 total module tests passing).

**Task 07 — API Documentation**
- Task ID: B-02-T07
- Status: ✅ **Completed & Verified**
- Objective: Document Edge Case 9 rule explicitly in OpenAPI docstring.
- Dependencies: B-02-T05.
- Definition of Done: OpenAPI documentation includes Edge Case 9 safeguards, status codes (200, 400, 401, 403, 404, 409, 422, 429, 500), and request/response examples.

**Task 08 — Diagnostic Question Bank & Admin Re-Check Support**
- Task ID: B-02-T08
- Status: ✅ **Completed & Verified**
- Objective: Provide question retrieval endpoint `GET /v1/learning/placement-check/questions` (and direct alias `GET /v1/placement-check/questions`) across EN, HI, UR, AR and administrative re-check toggle.
- Files Created/Modified: `src/noorheroes/modules/learning/placement_question_bank.py`, `src/noorheroes/modules/learning/placement_check_repository.py` (`set_recheck_allowed`), `src/noorheroes/modules/learning/placement_check_service.py` (`get_question_bank`, `set_recheck_allowed`), `src/noorheroes/modules/learning/api.py`, `src/noorheroes/api/v1/router.py`.
- Definition of Done: Question bank and admin recheck toggle fully tested and documented.

## 30. Definition of Done
Endpoint live, idempotent, correctly seeds skill-tree state including the Tajweed-prerequisite safeguard, cache-invalidates B-01, fully tested and documented.

## 31. Final Verification Checklist
- [x] Duplicate placement-check submission returns `409` with prior result, no re-scoring
- [x] Tajweed-track prerequisites never silently skipped (Edge Case 9 verified via test)
- [x] Cross-family `child_id` rejected
- [x] B-01 skill-tree cache invalidated immediately after successful placement check
- [x] Single-transaction write (no partial-placement state possible on failure)
- [x] Diagnostic question bank endpoint accessible with localized prompts across 4 languages (EN, HI, UR, AR)
- [x] Admin re-check override toggles `is_recheck_allowed` flag and resets to `False` upon re-evaluation
- [x] Full test suite green in CI
