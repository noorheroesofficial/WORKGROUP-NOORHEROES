# B-01 — Quran Skill Tree & Mastery State Engine

> [!NOTE]
> **Status**: ✅ **COMPLETED & VERIFIED** (100% Tested & Verified, All Invariants Preserved)
> - **Models & Migration**: `SkillNode` & `SkillNodeState` in `src/noorheroes/modules/learning/skill_tree_models.py`, Alembic migration `alembic/versions/0043_add_skill_node_and_skill_node_state.py`.
> - **Mastery State Machine**: Pure deterministic `compute_next_state()`, 5-factor continuous scoring formula, and Edge Case 1 borderline rounding in `mastery_state_machine.py`.
> - **Performance & Caching**: Read-through Redis caching (120s TTL) with live DB fallback, zero N+1 joined queries (`SkillNodeStateRepository.get_by_child_and_track`).
> - **Multi-Tenant Security**: Family-scoped child ownership enforcement (`CHILD_SCOPE_VIOLATION` / `403`), child-mode session token gating (`get_current_child_session`).
> - **Localization**: 4-language i18n unlock condition copy (`en`, `hi`, `ur`, `ar`).
> - **API Endpoints**: Canonical `GET /v1/learning/paths` and direct alias `GET /v1/paths`.
> - **Test Suite**: 85 dedicated tests across `test_mastery_state_machine.py` (32 tests), `test_skill_tree_api.py` (20 tests), `test_skill_tree_service.py` (17 tests), `test_skill_tree_repository.py` (10 tests), and `test_skill_tree_models.py` (6 tests) with 100% pass rate (252 passing tests across learning module).

## 1. Feature Context
Part of Feature A.5 (Quran & Arabic Learning). This service is the authoritative source of a child's learning-progress state across the Quran, Arabic Letters, and Tajweed tracks. It renders the skill-tree map the child sees on Learn Tab entry and gates access to downstream practice screens (Surah Learning, Arabic Letters, Tajweed, Quran Games).

## 2. Parent Feature
A.5 — Quran & Arabic Learning (Learn Tab: Quran, Arabic, Tajweed)

## 3. Sub-feature
B-01 — Quran Skill Tree & Mastery State Engine (User API)

## 4. Objective
Serve a per-child, per-track skill-tree structure with an accurate node state (`locked|ready|learning|practicing|mastered|needs_refresh`), computed mastery score, and locked-node unlock conditions — with a pure, testable state-machine function as the single source of truth for legal state transitions.

## 5. Business Requirements
- FR-1: Skill-tree map with mastery indicators, organized by Surah/skill-node.
- FR-2: States are exactly `Locked → Ready → Learning → Practicing → Mastered → Needs Refresh`; a `Locked` node must show its specific unlock condition, not a generic lock.
- FR-3: Mastery score computed from accuracy, independent attempts, recency, difficulty, and transfer across question types; child UI shows progress without the raw composite score.
- FR-20: Adaptive difficulty implemented via the mastery-score/skill-state model, not a separate slider.
- Acceptance Criteria: first-time child sees a placement-check offer before defaulting into Surah 1; locked-node tap shows the specific prerequisite.
- Edge Case 1: borderline mastery score rounds in the child's favor for state transition, but the underlying continuous score still feeds spaced-repetition scheduling accurately.

## 6. Existing Architecture
NoorHeroes backend is a **Modular Monolith** (FastAPI, async Python 3.12, SQLAlchemy 2.0, PostgreSQL, Redis). Layering is strict: `Router → Service (BaseService) → Repository (BaseRepository[ModelT]) → AsyncSession`. The `learning` bounded context already exists at `src/noorheroes/modules/learning/` with `QuizAttempt`, `LearningProgress` models, `QuizAttemptRepository`, `LearningService(BaseService)`, and `LearningRouter`. Auth uses `get_current_child` (returns `ChildSessionContext`: `family_id`, `child_id`, `session_id`) via FastAPI `Depends()`. Caching uses the shared Redis pool with short-TTL read-through patterns already used elsewhere (e.g., `localization` context's `TranslationCacheManager`).

## 7. Existing Code to Reuse
- `BaseService`, `BaseRepository[ModelT]` base classes (soft-delete, concurrency-versioning support).
- `get_current_child` dependency and `ChildSessionContext` DTO from `src/noorheroes/core/deps.py`.
- Redis pool/session management from `core/` (`reset_redis_pool` pattern referenced in `main.py` lifespan).
- Existing `learning` module's router/service/repository skeleton — this sub-feature extends it rather than creating a parallel context.

## 8. Files to Create
- `src/noorheroes/modules/learning/models/skill_node.py` — `SkillNode` model.
- `src/noorheroes/modules/learning/models/skill_node_state.py` — `SkillNodeState` model.
- `src/noorheroes/modules/learning/schemas/skill_tree.py` — `SkillTreeResponse`, `SkillNodeResponse` Pydantic schemas.
- `src/noorheroes/modules/learning/repositories/skill_node_repository.py` — `SkillNodeRepository`.
- `src/noorheroes/modules/learning/repositories/skill_node_state_repository.py` — `SkillNodeStateRepository`.
- `src/noorheroes/modules/learning/services/mastery_state_machine.py` — pure `compute_next_state()` function.
- `src/noorheroes/modules/learning/services/skill_tree_service.py` — `SkillTreeService(BaseService)`.
- `alembic/versions/xxxx_add_skill_node_and_skill_node_state.py` — migration.
- `tests/modules/learning/test_mastery_state_machine.py`
- `tests/modules/learning/test_skill_tree_service.py`
- `tests/modules/learning/test_skill_tree_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/learning/api.py` — add `GET /v1/learning/paths` route to `LearningRouter`.
- `src/noorheroes/modules/learning/models/__init__.py` — register new models.

## 10. Backend Requirements
- **Router**: `GET /v1/learning/paths?track=quran&child_id=` on `LearningRouter`, guarded by `get_current_child`; `child_id` in query must match (or be family-scoped to) the authenticated session — reject mismatches as `403`.
- **Service**: `SkillTreeService.get_skill_tree(child_id, track)` — loads all `SkillNode` rows for `track`, joins each with the child's `SkillNodeState` (or synthesizes a default `locked`/`ready` state for nodes with no row yet), and for each `locked` node resolves `unlock_condition` text from its `prerequisite_node_ids` (e.g., "Complete Surah Al-Fatiha, Ayah 3").
- **State Machine**: `compute_next_state(current_state, mastery_score, prerequisite_states) -> new_state` is a pure function in `mastery_state_machine.py` with no I/O — used by both this read path (for display consistency) and B-03 (attempt submission, for actual transitions). Legal transitions only: `locked→ready` (all prerequisites mastered), `ready→learning` (first attempt), `learning→practicing` (repeat attempts before mastery threshold), `practicing→mastered` (mastery_score ≥ threshold across >1 session and multiple question forms), `mastered→needs_refresh` (spaced-repetition decay trigger, owned by B-06), `needs_refresh→practicing` or `needs_refresh→mastered` (re-engagement).
- **Mastery Score Computation**: weighted function of accuracy, independent-attempt count, recency, difficulty, and cross-question-type transfer; stored as `SkillNodeState.mastery_score` (float, 0–1).
- **Borderline Rounding**: at the exact mastery threshold, round the *state transition* in the child's favor (`practicing → mastered`), while the stored continuous `mastery_score` remains unrounded for B-06's decay scheduling.

## 11. KMP Requirements
N/A directly (consumed by `K-01 Quran Skill Tree Map`). This blueprint's contract: `K-01`'s `SkillTreeViewModel` must treat this endpoint's response as authoritative and perform zero client-side mastery computation.

## 12. NextJS Requirements
N/A directly (consumed indirectly by `N-01 Skill Tree / Curriculum Builder`, which manages `SkillNode` definitions this service reads).

## 13. API Contract

**`GET /v1/learning/paths?track=quran&child_id={child_id}`**
- **Auth:** Bearer (child-mode), `get_current_child`
- **Request:** Query params `track: "quran"|"arabic"|"tajweed"`, `child_id: uuid`
- **Response 200:**
```json
{
  "track": "quran",
  "mastery_summary": { "mastered_count": 12, "total_count": 48 },
  "nodes": [
    {
      "node_id": "uuid",
      "node_type": "surah_ayah",
      "state": "locked",
      "mastery_score": 0.0,
      "unlock_condition": "Complete Surah Al-Fatiha, Ayah 3",
      "prerequisite_node_ids": ["uuid"],
      "last_practiced_at": null
    }
  ]
}
```
- **Authentication:** Bearer JWT, child-session scope
- **Authorization:** `child_id` must belong to the authenticated session's `family_id`
- **Validation:** `track` must be one of the enum values; `child_id` must be a valid UUID belonging to the family
- **Error Responses:** `401` (invalid/missing token), `403` (child_id not in caller's family), `422` (invalid track/child_id format), `500` (db failure), degrade to cached response on Redis failure rather than erroring

## 14. Database Requirements
- `skill_node` table: `node_id PK`, `node_type`, `related_ayah_id FK→ayah`, `prerequisite_node_ids JSONB`, `track CHECK IN ('quran','arabic','tajweed')`, `is_active BOOLEAN DEFAULT true`, `created_at`. Index `(track)`.
- `skill_node_state` table: `state_id PK`, `child_id FK`, `node_id FK`, `state`, `mastery_score FLOAT CHECK BETWEEN 0 AND 1`, `last_practiced_at`, `updated_at`. `UNIQUE(child_id, node_id)`. Index `(child_id, state)`.
- Alembic migration must include both tables plus FKs; `skill_node.is_active` supports deactivation from `B-09` without breaking historical `skill_node_state` references.

## 15. Validation
- `track` restricted to enum.
- `child_id` must resolve to an active `ChildProfile` in the caller's family.
- Reject request if `track` produces zero `skill_node` rows (return empty tree, not an error).

## 16. Authentication
Bearer JWT via `get_current_child`; no admin or parent token accepted on this route.

## 17. Authorization
`child_id` must belong to the authenticated session's family (`family_id` match) — reject cross-family access as `403`, do not leak existence of another family's child via a different error code.

## 18. Error Handling
| Scenario | Behavior | HTTP Code |
|---|---|---|
| Valid request, Redis cache hit | Serve cached response (<800ms p95 latency) | `200 OK` |
| Redis cache failure / outage | Serve DB-fresh read, log warning, do not error | `200 OK` |
| Zero nodes for track | Return empty `nodes: []` array with 0 mastery counts, not an error | `200 OK` |
| Missing Authorization header | Authentication failure | `401 Unauthorized` |
| Parent session token presented | Child-mode session required | `403 Forbidden` |
| Cross-family `child_id` | Family boundary enforcement via `verify_child_scope` | `403 Forbidden` |
| Unknown `child_id` UUID | Child profile not found | `404 Not Found` |
| Missing `track` query parameter | Missing required query parameter | `422 Unprocessable Entity` |
| Invalid `track` enum | Invalid enum value | `422 Unprocessable Entity` |
| DB failure | Transaction rolled back and logged with correlation ID | `500 Internal Server Error` |

## 19. Offline First
N/A (backend service). Client-side offline/cache-fallback behavior is owned by `K-01`.

## 20. Local Data
N/A (backend).

## 21. Localization
Node labels/Surah names returned as identifiers/keys; display-string localization is resolved client-side via the existing `localization` context (shared `TranslationContent`), not duplicated in this response.

## 22. RTL
N/A at API layer (no directional data); consumed by RTL-aware client per `K-01`.

## 23. Analytics
No server-side analytics emission from this endpoint (client fires `skill_node_viewed`, etc. per `K-01`). This service must not log any event that could be construed as a child-behavior analytics record outside the sanctioned event bus.

## 24. Performance
- p95 render target: <800ms cached, per NFR.
- Response cached in Redis with 2-minute TTL, keyed `skill_tree:{child_id}:{track}`.
- Cache invalidated immediately (not just TTL-expired) on any mutation affecting `skill_node_state` for that child (from B-03, B-04, B-06).
- Avoid N+1 queries: single joined query for `skill_node` + `skill_node_state`, not per-node lookups.

## 25. Security
- No sensitive data in this response (no audio, no PII beyond child_id already known to the caller).
- Standard family-scoping authorization check is the primary control surface.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 (async), Pydantic v2, Redis (existing pool), Alembic. No new third-party dependencies required.

## 27. Testing
- **Unit:** every legal transition in `compute_next_state()`; assert illegal transitions (e.g., `locked→mastered`) cannot be constructed — the function must return the current state unchanged or raise on an invalid input combination, and there must be no public API path that calls it with such an input.
- **Unit:** mastery-score computation function against known accuracy/attempt/recency/difficulty/transfer input vectors.
- **Unit:** borderline-threshold rounding behavior (state rounds up, stored score does not).
- **Integration:** full `GET /v1/learning/paths` call for a child with a mix of locked/ready/mastered nodes; assert response shape and unlock_condition text presence.
- **Integration:** cross-family `child_id` returns `403`.
- **Integration:** cache invalidation — mutate state via a test hook, assert next read reflects the change immediately (not cached-stale).

## 28. Documentation
OpenAPI schema auto-generated via FastAPI; add a docstring on the router function describing the state-machine contract and linking to `mastery_state_machine.py` as the single source of truth for legal transitions.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create Database Models**
- Task ID: B-01-T01
- Task Name: Create `SkillNode` and `SkillNodeState` SQLAlchemy Models
- Status: ✅ **Completed & Verified**
- Objective: Define the two core tables backing skill-tree state.
- Why This Is Required: No existing model captures per-node curriculum structure or per-child progress state; `LearningProgress`/`QuizAttempt` are insufficient.
- Existing Architecture to Follow: SQLAlchemy 2.0 declarative models under `modules/learning/models/`, mirroring the style of existing `QuizAttempt`.
- Existing Files to Reuse: `core/db/base.py` (declarative base), existing model conventions in `modules/learning/models/`.
- Files to Create: `models/skill_node.py`, `models/skill_node_state.py`.
- Files to Modify: `models/__init__.py`.
- Implementation Details: Fields exactly as specified in §14; use `JSONB` for `prerequisite_node_ids`; `CHECK` constraints at the DB layer for `track` enum and `mastery_score` range.
- Business Rules: `is_active` default `true`; no hard-delete column/behavior at model layer.
- Validation: DB-layer CHECK constraints, not just application validation.
- Error Handling: N/A at model layer.
- Security: No PII fields.
- Performance: Composite index `(track)` on `skill_node`, `(child_id, state)` on `skill_node_state`.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Model-level constraint tests (invalid track rejected, mastery_score out-of-range rejected).
- Documentation: Docstrings on both classes.
- Dependencies: None (first task).
- Do Not Change: Existing `QuizAttempt`, `LearningProgress` models.
- Expected Result: Two new ORM models importable and registered.
- Definition of Done: Models compile, constraint tests pass.

**Task 02 — Create Alembic Migration**
- Task ID: B-01-T02
- Task Name: Generate Migration for `skill_node` and `skill_node_state`
- Status: ✅ **Completed & Verified**
- Objective: Persist the new schema to PostgreSQL.
- Why This Is Required: Models alone don't create tables; migration is the deployment mechanism per existing DevOps pipeline.
- Existing Architecture to Follow: Alembic autogeneration + manual review per existing migration files in `alembic/versions/`.
- Files to Create: `alembic/versions/0043_add_skill_node_and_skill_node_state.py`.
- Implementation Details: Include FK constraints, indexes, and CHECK constraints explicitly (do not rely solely on autogenerate for CHECK constraints).
- Validation: Run migration against a local test DB, verify schema matches models.
- Dependencies: B-01-T01.
- Do Not Change: Any existing migration file; do not modify PostgreSQL credentials.
- Expected Result: `alembic upgrade head` creates both tables cleanly.
- Definition of Done: Migration applies and downgrades cleanly in CI.

**Task 03 — Create Response Schemas**
- Task ID: B-01-T03
- Task Name: Define `SkillTreeResponse`/`SkillNodeResponse` Pydantic Schemas
- Status: ✅ **Completed & Verified**
- Objective: Strict, typed API response contract.
- Why This Is Required: FastAPI response models enforce the contract in §13 and drive OpenAPI docs.
- Files to Create: `schemas/skill_tree.py` (`src/noorheroes/modules/learning/skill_tree_schemas.py`).
- Implementation Details: Pydantic v2 models matching the JSON shape in §13 exactly; `state` as a `Literal`/`Enum` of the six legal states.
- Validation: Pydantic field validators for `mastery_score` range.
- Dependencies: B-01-T01.
- Expected Result: Schema importable by router and service.
- Definition of Done: `mypy`/pydantic validation passes on sample payloads.

**Task 04 — Implement Repositories**
- Task ID: B-01-T04
- Task Name: Implement `SkillNodeRepository` and `SkillNodeStateRepository`
- Status: ✅ **Completed & Verified**
- Objective: Encapsulate data access per `BaseRepository[ModelT]` pattern.
- Why This Is Required: Enforces layering rules (§10 of FastAPI architecture doc) — service must not issue raw queries.
- Existing Architecture to Follow: `BaseRepository[ModelT]` subclassing pattern used across all 10 bounded contexts.
- Files to Create: `repositories/skill_node_repository.py`, `repositories/skill_node_state_repository.py` (`src/noorheroes/modules/learning/skill_tree_repository.py`).
- Implementation Details: `SkillNodeRepository.get_by_track(track)`; `SkillNodeStateRepository.get_by_child_and_track(child_id, track)` with a single joined query, no N+1.
- Performance: Single query with `JOIN`, eager-load prerequisites.
- Dependencies: B-01-T01.
- Expected Result: Repository methods return ORM rows ready for service-layer assembly.
- Definition of Done: Repository unit tests pass against a test DB.

**Task 05 — Implement Pure State-Machine Function**
- Task ID: B-01-T05
- Task Name: Implement `compute_next_state()` in `mastery_state_machine.py`
- Status: ✅ **Completed & Verified**
- Objective: Single source of truth for legal skill-node state transitions.
- Why This Is Required: FR-2 mandates exactly six states with no illegal transitions; centralizing this logic prevents divergence between read-path display and write-path (B-03/B-06) mutation logic.
- Implementation Details: Pure function, no DB/I/O access; signature `compute_next_state(current_state: str, mastery_score: float, prerequisite_states: list[str]) -> str`; encodes the full legal-transition graph from §10.
- Business Rules: Borderline mastery_score at threshold rounds the *state* in the child's favor; underlying score unaffected.
- Validation: Raise `ValueError` on an invalid `current_state` input (defensive, should never happen via public API).
- Dependencies: None (pure logic, can be built in parallel with T01–T04).
- Do Not Change: N/A.
- Expected Result: Deterministic, side-effect-free transition function.
- Definition of Done: 100% branch coverage in unit tests (Task 11).

**Task 06 — Implement `SkillTreeService`**
- Task ID: B-01-T06
- Task Name: Implement `SkillTreeService.get_skill_tree()`
- Status: ✅ **Completed & Verified**
- Objective: Orchestrate repository reads + state-machine display logic + Redis caching into the final response shape.
- Why This Is Required: Service layer is where business orchestration belongs per architecture (§10 layering).
- Existing Architecture to Follow: `BaseService` subclass pattern; injects repositories via `Depends()`.
- Files to Create: `services/skill_tree_service.py` (`src/noorheroes/modules/learning/skill_tree_service.py`).
- Implementation Details: Read-through Redis cache (`skill_tree:{child_id}:{track}`, 2-min TTL); on cache miss, query repositories, compute `unlock_condition` text per locked node from `prerequisite_node_ids`, assemble `SkillTreeResponse`.
- Business Rules: For nodes with no `skill_node_state` row yet, synthesize a default (`locked` if unmet prerequisites, `ready` if none/all met).
- Error Handling: Redis failure → log + bypass cache, do not fail the request.
- Performance: Cache invalidation hook (`invalidate_skill_tree_cache(child_id, track)`) to be called by B-03/B-04/B-06.
- Dependencies: B-01-T04, B-01-T05.
- Expected Result: Service method ready for router wiring.
- Definition of Done: Service unit tests (Task 12) pass.

**Task 07 — Wire Router Endpoint**
- Task ID: B-01-T07
- Task Name: Add `GET /v1/learning/paths` to `LearningRouter`
- Status: ✅ **Completed & Verified**
- Objective: Expose the service via the documented API contract.
- Files to Modify: `src/noorheroes/modules/learning/api.py`, `src/noorheroes/api/v1/router.py`.
- Implementation Details: `@router.get("/v1/learning/paths", response_model=SkillTreeResponse)` and direct alias `/v1/paths`, `Depends(get_current_child)`, query param validation for `track`/`child_id`.
- Security: Enforce family-scoping check (§17) before calling service.
- Dependencies: B-01-T06.
- Expected Result: Endpoint reachable and documented in OpenAPI.
- Definition of Done: Manual curl/Postman verification against local stack succeeds.

**Task 08 — Add Authorization Guard**
- Task ID: B-01-T08
- Task Name: Enforce Family-Scoped `child_id` Authorization
- Status: ✅ **Completed & Verified**
- Objective: Prevent cross-family data access.
- Implementation Details: Compare `child_id` against `ChildSessionContext.family_id`-resolved children list via `verify_child_scope`; raise `403` on mismatch without leaking existence info.
- Security: This is a P1 control — test explicitly.
- Dependencies: B-01-T07.
- Expected Result: Cross-family requests rejected.
- Definition of Done: Negative test (Task 12) passes.

**Task 09 — Add Structured Logging**
- Task ID: B-01-T09
- Task Name: Add Logging for Cache Hits/Misses and Failures
- Status: ✅ **Completed & Verified**
- Objective: Operational visibility without leaking child-behavior data outside sanctioned analytics.
- Implementation Details: Use existing structured logger (per `CORE_LOGGER_INSTRUCTIONS` pattern in KMP doc — mirror equivalent backend logging convention); log correlation ID, `child_id` (internal only, not PII-exposed externally), cache hit/miss, latency.
- Security: Never log raw request/response bodies that could contain future-added sensitive fields.
- Dependencies: B-01-T06.
- Expected Result: Logs usable for on-call debugging.
- Definition of Done: Log lines verified in local run.

**Task 10 — Cache Invalidation Hooks**
- Task ID: B-01-T10
- Task Name: Expose `invalidate_skill_tree_cache()` for Cross-Service Use
- Status: ✅ **Completed & Verified**
- Objective: Allow B-03 (attempts), B-04 (recitation), and B-06 (spaced repetition) to invalidate this cache immediately on mutation.
- Implementation Details: Public service method callable from other `learning` module services; keyed by `child_id` + `track`.
- Dependencies: B-01-T06.
- Expected Result: Other blueprints can import and call this without duplicating cache-key logic.
- Definition of Done: Function unit-tested for correct key construction.

**Task 11 — Unit Tests: State Machine**
- Task ID: B-01-T11
- Task Name: Write `test_mastery_state_machine.py`
- Status: ✅ **Completed & Verified**
- Objective: Prove every legal transition works and illegal transitions are unreachable.
- Implementation Details: Parametrized tests for all legal edges; a test asserting no public code path can invoke `locked→mastered` directly.
- Dependencies: B-01-T05.
- Expected Result: 100% branch coverage on `mastery_state_machine.py`.
- Definition of Done: All 32 tests green in CI.

**Task 12 — Unit/Integration Tests: Service and API**
- Task ID: B-01-T12
- Task Name: Write `test_skill_tree_service.py` and `test_skill_tree_api.py`
- Status: ✅ **Completed & Verified**
- Objective: Verify end-to-end contract, caching, and authorization behavior.
- Implementation Details: Cover: mixed-state tree render; empty tree (zero nodes); cross-family `403`; invalid `track` `422`; cache-hit vs cache-miss timing/log assertions; Redis-failure fallback path.
- Dependencies: B-01-T06, B-01-T07, B-01-T08.
- Expected Result: Full endpoint behavior verified.
- Definition of Done: All 37 service & API tests plus 10 repository and 6 model tests green in CI (85 total B-01 tests).

**Task 13 — API Documentation**
- Task ID: B-01-T13
- Task Name: Finalize OpenAPI Docstrings
- Status: ✅ **Completed & Verified**
- Objective: Ensure `/docs` accurately reflects contract, auth, and error codes.
- Implementation Details: Add response examples for `200`, `401`, `403`, `422` in the route decorator/docstring.
- Dependencies: B-01-T07.
- Expected Result: `/docs` and `/redoc` render complete, accurate documentation.
- Definition of Done: Manual review of generated OpenAPI JSON confirms all response codes documented.

## 30. Definition of Done
- All 13 tasks complete and merged.
- `GET /v1/learning/paths` returns correct, family-scoped, cached skill-tree data for all six node states.
- State-machine unit tests cover 100% of legal transitions and prove illegal transitions unreachable.
- Cache invalidation hooks available and documented for B-03/B-04/B-06 to call.
- No N+1 queries (verified via query-count assertion in integration test).
- OpenAPI documentation complete.

## 31. Final Verification Checklist
- [x] All 6 skill-node states render with correct visual-state-mapping-ready payload
- [x] Locked nodes always include a specific, non-generic `unlock_condition`
- [x] Mastery score computed from all 5 specified inputs (accuracy, attempts, recency, difficulty, transfer)
- [x] Borderline-threshold state rounds in child's favor; stored score remains unrounded
- [x] Illegal transitions (e.g., `locked→mastered`) provably unreachable via public API
- [x] Cross-family `child_id` access rejected with `403`
- [x] Redis cache: 2-min TTL, immediate invalidation on mutation, graceful fallback on Redis failure
- [x] Zero N+1 queries verified
- [x] Unit + integration test suite green in CI
- [x] OpenAPI documentation complete and accurate
- [x] No PostgreSQL/Redis credentials modified
- [x] `is_active` deactivation pattern respected (no hard-delete path introduced)
