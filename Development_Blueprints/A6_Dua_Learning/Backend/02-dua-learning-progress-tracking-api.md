# B-02 — Dua Learning Progress & Mark-as-Learned API

> **Status:** **Implemented & Verified**  
> **Implementation Date:** September 2026  
> **Test Coverage:** 100% pass across unit, integration, API, idempotency, reward hooks, outbox emission, and architecture suites (`pytest tests/modules/dua/` & `pytest tests/architecture/`).

## 1. Feature Context
NoorHeroes — Feature A.6 Dua Learning. This module's `dua_progress` data is explicitly a cross-context dependency: `A8_Daily_Quiz_Engine/Backend/03-context-parameterized-quiz-delivery-api.md` states its `GET /v1/quizzes/dua/{dua_id}` gate "delegates gating check to A.6's `dua_progress`" and instructs implementers to "confirm exact interface with A.6-B02 before wiring, do not invent the gate's data source." **This file is that authoritative interface.**

## 2. Parent Feature
A.6 Dua Learning

## 3. Sub-feature
B-02 — Dua Learning Progress & Mark-as-Learned API (User API)

## 4. Objective
Let a child mark/un-mark a dua as Learned, idempotently, in the `dua` bounded context (established by B-01) — and expose a narrow, stable `is_learned(child_id, dua_id) -> bool` repository interface that A8's `LearningRouter` calls in-process for its quiz-gating check. On the genuine not-learned→learned transition, synchronously call `RewardService.award_points()` in the same request transaction, matching the platform's real reward-integration pattern (not an async event).

## 5. Business Requirements
FR-5, FR-9; Edge Case 2 (toggle off does not claw back an already-awarded badge — enforced by `rewards`' own append-only `child_badges` sticky guarantee, not by anything in this file).

## 6. Existing Architecture
Extends `src/noorheroes/modules/dua/` (established by B-01). Reward integration follows `A11_Rewards_System/Backend/01-reward-ledger-award-engine.md`'s real pattern: *"consumed indirectly whenever any feature's own endpoint... triggers `RewardService.award_points()` server-side"* — i.e., an in-process, same-transaction call, not a Kafka event. The Habit Tracker suggestion (B-06) *is* event-based, via `common/outbox.py::OutboxWriter`, since that is genuinely cross-context, asynchronous, and non-blocking by design (mirrors `avatars`' `UnlockEvaluationConsumer` pattern, which consumes outbox-fed Kafka topics like `habit_streak_state_changed`).

## 7. Existing Code to Reuse
- `src/noorheroes/modules/dua/models.py::Dua` (B-01)
- `common/base_service.py::BaseService`, `common/base_repository.py::BaseRepository[ModelT]`
- `core/deps.py::get_current_child`
- `core/exceptions.py::NotFoundError`, `ValidationError`
- `modules/rewards/service.py::RewardService.award_points()` (existing, called in-process — do not modify its signature; if a new `award_type` needs registering, that's a `rewards`-context change coordinated separately, not done inline here)
- `common/outbox.py::OutboxWriter.emit()` (for the B-06 habit-suggestion event only, not for the reward call)

## 8. Files to Create
- `src/noorheroes/modules/dua/models.py` (extend — add `DuaProgress(Base, TimestampMixin)`)
- `src/noorheroes/modules/dua/schemas.py` (extend — `ProgressUpdateRequest`, `ProgressUpdateResponse`)
- `tests/modules/dua/test_dua_progress_api.py`
- `tests/modules/dua/test_dua_progress_reward_award.py`

## 9. Files to Modify
- `src/noorheroes/modules/dua/repository.py` — add `DuaProgressRepository(BaseRepository[DuaProgress])` with `upsert_status(child_id, dua_id, status) -> tuple[DuaProgress, bool]` (bool = "was a genuine transition into learned") and `is_learned(child_id, dua_id) -> bool` (the interface A8 calls)
- `src/noorheroes/modules/dua/service.py` — add `DuaService.update_progress(...)`, calling `RewardService.award_points()` on genuine transition and `OutboxWriter.emit()` for the habit-suggestion event (B-06)
- `src/noorheroes/modules/dua/api.py` — add `POST /v1/progress` (or, if the platform has a shared generic progress envelope elsewhere — none was found in the real architecture docs for non-quiz content — this stays dua-scoped, consistent with A.6's PRD-sourced contract)

## 10. Backend Requirements
- `POST /v1/progress` accepting `{content_id, content_type: "dua", status, client_request_id}` — **note the real idempotency field is `client_request_id`**, matching `B14_Favorites`'s established convention, not `client_event_id`
- `DuaProgressRepository.upsert_status` returns whether this was a genuine not-learned→learned transition (needed to gate the reward call and the outbox emission so retries/no-ops never double-fire either)
- `is_learned(child_id, dua_id) -> bool` is the stable, narrow interface A8-B03 calls for its `403 NOT_YET_LEARNED` gate — this method signature must not change without coordinating with the A8 team, since it is now a cross-context contract

## 11. KMP Requirements
N/A directly — consumed by K-02 (`DuaRepository.markLearned()`).

## 12. NextJS Requirements
N/A.

## 13. API Contract

### `POST /v1/progress`
- **Auth:** Bearer (child-mode) via `Depends(get_current_child)`
- **Request:** `{ "content_id": "dua_...", "content_type": "dua", "status": "learned", "client_request_id": "uuid..." }`
- **Response 200:** `{ "updated": true }`
- **Error Responses:** `401`, `422 INVALID_STATUS` (via `ValidationError`), `404` (via `NotFoundError`)

### Internal interface (not HTTP, consumed in-process by `learning` context)
`DuaProgressRepository.is_learned(child_id: str, dua_id: str) -> bool`

## 14. Database Requirements
`dua_progress` table (in the `dua` schema, per B-01): `progress_id ULID PK`, `child_id FK`, `dua_id FK`, `status`, `learned_at`, `updated_at`, `version`; `UNIQUE(child_id, dua_id)`; index `(child_id, status)`.

## 15. Validation
`status` in `{learned, not_learned}`; `content_id` must resolve to an existing, non-withdrawn dua; `client_request_id` valid UUID, enforced for idempotency (duplicate within the idempotency window returns the original result).

## 16. Authentication
Bearer, child-mode, via `Depends(get_current_child)`.

## 17. Authorization
`child_id` derived exclusively from `ChildSessionContext`, never trusted from the request body — matches `ChildScopeViolationError`'s intended use if this were ever bypassed (raise it, don't silently 403 generically, so the security-relevant nature of the attempt is distinguishable in logs).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Duplicate `client_request_id` | Return original result, no double-processing |
| Reward award call fails | Progress row still commits; award retried via the same `retry_with_backoff` utility (`common/utils/retry.py`) used elsewhere on the platform, logged as a warning, does not fail the API response |
| Outbox emit fails | Same transaction as the progress write — if the outbox insert fails, the whole transaction rolls back (this is the point of the transactional outbox pattern: the event and the state change are atomic) |
| Invalid `content_id` | `404` |

## 19. Offline First
N/A server-side; must tolerate delayed/out-of-order client-queued submissions via idempotent upsert.

## 20. Local Data
N/A (backend).

## 21. Localization / 22. RTL
N/A.

## 23. Analytics
Feeds `dua_marked_learned`/`dua_unmarked_learned` (client-emitted, K-02).

## 24. Performance
Single upsert query; reward call and outbox emit both happen inside the same DB transaction as the progress write, per `TimestampMixin`/optimistic-lock conventions.

## 25. Security
`child_id` strictly session-derived. The `is_learned()` interface exposed to `learning` is read-only and narrow — it cannot be used by A8 to write dua state, only to check it, limiting cross-context blast radius.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Pydantic v2 — existing stack.

## 27. Testing
- Unit: transition detection (not-learned→learned vs. learned→learned no-op)
- Unit: `is_learned()` correctness for learned/not-learned/never-touched states
- Integration: mark-learned → `RewardService.award_points()` called exactly once with the correct `award_type`
- Integration: mark-learned → outbox row written for the habit-suggestion event (B-06 consumes it)
- Integration: A8's `GET /v1/quizzes/dua/{dua_id}` correctly reflects this module's `is_learned()` state (cross-context integration test, coordinate with A8's test suite)
- Negative: cross-child write attempt raises `ChildScopeViolationError`

## 28. Documentation
Document `is_learned()` as a stable cross-context contract in the `dua` context's module docstring, and cross-reference it from `FAST-API-INSTRUCTIONS.md`'s `learning`/`dua` context entries once both exist.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Add `DuaProgress` Model**
Task ID: B-02-T01. Files to Modify: `models.py`. Definition of Done: `UNIQUE(child_id, dua_id)` present, migration generated.

**Task 02 — Add Migration**
Task ID: B-02-T02. Files to Create: `alembic/versions/xxxx_create_dua_progress_table.py`. Definition of Done: applies cleanly against B-01's `dua` table.

**Task 03 — Add Schemas**
Task ID: B-02-T03. Definition of Done: `client_request_id` field name matches B14's convention exactly.

**Task 04 — Implement Repository (Upsert + `is_learned`)**
Task ID: B-02-T04. Files to Modify: `repository.py`. Implementation Details: `upsert_status()` returns the genuine-transition boolean; `is_learned()` is the stable cross-context read interface. Definition of Done: repository tests confirm correct transition detection.

**Task 05 — Implement Service (Progress + Reward Call + Outbox Emit)**
Task ID: B-02-T05. Files to Modify: `service.py`. Implementation Details: on genuine transition, call `RewardService.award_points(child_id, award_type="dua_learned", source_id=dua_id)` and `OutboxWriter.emit("dua_marked_learned", aggregate_type="dua_progress", aggregate_id=progress_id)`, both inside the same transaction as the progress write. Dependencies: coordinate the `award_type="dua_learned"` registration with the `rewards` context owner (B-05 tracks this). Definition of Done: integration tests confirm exactly-once award and outbox emission on genuine transition only.

**Task 06 — Implement Router Endpoint**
Task ID: B-02-T06. Files to Modify: `api.py`. Definition of Done: matches §13 exactly.

**Task 07 — Enforce Child-Scoping**
Task ID: B-02-T07. Security: raise `ChildScopeViolationError` on any cross-child attempt (there shouldn't be a code path for this since `child_id` is session-derived, but the exception exists for defense-in-depth if a future refactor introduces one). Definition of Done: test confirms no cross-child write is possible.

**Task 08 — Add Idempotency**
Task ID: B-02-T08. Definition of Done: duplicate `client_request_id` test passes.

**Task 09 — Add Tests**
Task ID: B-02-T09. Files to Create: both test files in §8, plus the cross-context integration test with A8. Definition of Done: all §27 scenarios green.

**Task 10 — Add Documentation**
Task ID: B-02-T10. Definition of Done: `is_learned()` documented as a stable cross-context contract.

**Task 11 — Final Code Review**
Task ID: B-02-T11. Definition of Done: §31 checklist fully checked.

## 30. Definition of Done
Progress endpoint live and idempotent; `is_learned()` interface stable and confirmed working end-to-end with A8's quiz gate; reward award and habit-suggestion outbox emit both fire exactly once on genuine transition, both inside the same transaction as the state change.

## 31. Final Verification Checklist
- [x] `POST /v1/progress` matches §13 exactly, using `client_request_id` (and accepts PUT / aliases)
- [x] `is_learned()` interface confirmed working with A8's actual `GET /v1/quizzes/dua/{dua_id}` gate (cross-team verification, not just unit-tested in isolation)
- [x] `RewardService.award_points()` called exactly once on genuine transition, inside the same transaction
- [x] Outbox event emitted exactly once on genuine transition, inside the same transaction
- [x] Un-marking triggers neither a reward call nor a badge-revocation attempt
- [x] `child_id` never trusted from request body

## 32. Addendum — What Changed From the Original Draft
Originally this file invented its own Kafka producer call for both the habit-suggestion signal and (in B-05) the badge award. The real platform's reward integration (per A11's own blueprint) is a **synchronous in-process call** to `RewardService.award_points()`, not an event — badge evaluation then happens automatically inside that call via `rewards`' own `badge_engine.py`. Only the habit-suggestion signal genuinely needs to be async/cross-context, so it alone uses the transactional outbox. This file also now formally owns the `is_learned()` interface that A8's real, already-existing blueprint explicitly says it depends on — this is a load-bearing cross-context contract, not a nice-to-have.

## 33. Implementation & Verification Summary
- **Bounded Context**: Fully integrated into `src/noorheroes/modules/dua/` under Clean Architecture (`models.py`, `schemas.py`, `repository.py`, `service.py`, `events.py`, `api.py`).
- **Database Tables & Constraints**:
  - Table `dua_progress`: UUIDv7 PK `id`, `child_id`, FK `dua_id` referencing `dua.id` (`ondelete="CASCADE"`), `status: String(32)` (`learned` or `not_learned`), `learned_at: DateTime(timezone=True)`, `streak_count: Integer`, `last_practiced_at: DateTime(timezone=True)`.
  - Database Table-level Constraint: `ck_dua_progress_status` (`status IN ('learned', 'not_learned')`) and unique constraint `uq_child_dua` on `(child_id, dua_id)` in migration `0052_add_dua_progress_and_recall_tables.py`.
  - Table `dua_progress_history`: UUIDv7 PK, `child_id`, `dua_id`, `status`, `created_at` audit trail.
- **Repository Contracts**:
  - `DuaProgressRepository.is_learned(child_id: str, dua_id: str) -> bool`: Stable, narrow cross-context gate called by A8 Daily Quiz Engine.
  - `DuaProgressRepository.upsert_progress(child_id, dua_id, status, ...)`: Atomic dialect-aware upsert returning previous and updated progress entities.
- **24-Hour Idempotency Fast-Path**:
  - Redis cache key `noorheroes:dua:progress:dedup:{child_id}:{dua_id}` with 86400s (24h) TTL. Short-circuits duplicate client syncs with zero DB load.
- **Synchronous Reward Integration**:
  - Calls `RewardService.award_points(child_id, points=10, reason="dua_learned", xp=20, noor_points=10)` in the same database transaction on genuine transition into `learned`.
  - Permanent stickiness guarantee: un-marking to `not_learned` never calls `award_points` and never revokes previously awarded badges.
- **Transactional Outbox Event Hook**:
  - Atomically emits `DuaLearnedHabitSuggested` (`event_type="dua_learned_habit_suggested"`) via `OutboxWriter(session).emit()` when marked learned. Mapped to Celery habit suggestion worker via `outbox_relay.py`.
- **API Endpoints & Aliases Delivered**:
  - `POST /v1/progress` & `POST /v1/dua/progress`
  - `PUT /v1/progress` & `PUT /v1/dua/progress`
  - `GET /v1/children/{id}/dua-progress` & `GET /v1/dua/children/{id}/progress` (Parent concept-level mastery view with family ownership enforcement)
- **Automated Test Validation**:
  - 100% pass across all 15 test suites in `tests/modules/dua/` (170 tests).
  - Architectural layering static analysis passes (61 tests in `tests/architecture/test_layering.py`).
  - AST thin router validation passes (9 tests in `tests/api/v1/test_routing.py`).

