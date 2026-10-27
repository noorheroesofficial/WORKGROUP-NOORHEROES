# B-02 — Habit Check-In & Reward Idempotency Engine

> **Status**: ✅ **COMPLETED & VERIFIED**  
> **Completed Date**: 2026-09-14  
> **Implementation Scope**: Backend (Python FastAPI)  
> **Alembic Revision**: `0054_create_habit_log_table.py` (`head`)  
> **Test Pass Rate**: 52 passed in `tests/modules/habits` (100% pass rate, 91.88% coverage), 331 passed in unified architectural & i18n suites  
> **Mandatory CI Concurrency Gate**: `tests/modules/habits/test_checkin_concurrency.py` (10 concurrent requests → exactly 1 row, 1 reward, 10× 200 OK)

## 1. Feature Context
Part of Feature A.7 — Habit Tracker. This is the feature's single most safety-critical integrity guarantee: reward-farming must be structurally impossible.

## 2. Parent Feature
A.7 Habit Tracker — Backend (FastAPI)

## 3. Sub-feature
B-02 Habit Check-In & Reward Idempotency Engine

## 4. Objective
Implement `POST /v1/habits/check-ins` granting exactly one capped reward per `(child_id, habit_id, local_date)`, idempotent under both concurrent duplicate requests and client retries, backing FR-2, FR-3, FR-4, FR-20 and Edge Cases 1, 2, 10, 12.

## 5. Business Requirements
- Exactly one reward per `(child_id, habit_id, local_date)` — no exceptions, no admin override that bypasses the DB constraint.
- `local_date` is trusted from the client payload (captured at tap time), not server-processing time (Edge Case 1).
- Repeated/duplicate submissions return the **original** successful result (200), never an error (FR-3).
- `client_request_id` provides a second idempotency layer for accidental double-taps before a request completes (Edge Case 2).
- Backfilled historical check-ins (up to 14 days back) must reconcile correctly, oldest-first (Edge Case 12).
- Excessive tap volume must not yield extra reward and must not surface as a child-facing error (Edge Case 10).

## 6. Existing Architecture
- New `habits` bounded context (established in B-01) — this task extends `models.py`, `schemas.py`, `repository.py`, `service.py`, `api.py` within it.
- Reuse the existing `rewards` context's `RewardService.award_points()` (`src/noorheroes/modules/rewards/service.py`) for XP/Noor Heroes Points issuance — **do not** implement a parallel reward-granting mechanism inside `habits`; call the existing shared service exactly as `learning`'s quiz-submission flow does (§5.5, §6.5 pattern: `LearningRouter` → `LearningService` → shared reward issuance).
- Reuse `BaseRepository`/`BaseService` conventions.
- **Signature update (per A.11 B-01):** `award_points()` has been extended beyond the simple 4-arg form originally assumed here to `award_points(child_id, activity_type, reason_id, rule_version, xp, noor_points, idempotency_key, metadata=None) -> AwardResult`. Call it as `award_points(child_id=child_id, activity_type="habit_checkin", reason_id=f"{habit_id}:{local_date}", rule_version=<active version>, xp=..., noor_points=..., idempotency_key=client_request_id)` — reusing this endpoint's own `client_request_id` as the reward engine's idempotency key rather than minting a second one, since both are meant to represent the same logical event.

## 7. Existing Code to Reuse
- `RewardService.award_points(child_id, activity_type, reason_id, rule_version, xp, noor_points, idempotency_key, metadata=None) -> AwardResult` (`rewards` context, extended per A.11 B-01 — see §6 for the correct call shape)
- `get_current_child` dependency
- `HabitRepository` (extend from B-01)

## 8. Files to Create
- Extend `src/noorheroes/modules/habits/models.py` with full `HabitLog` model (unique constraints)
- `alembic/versions/<rev>_create_habit_log_table.py`
- Extend `schemas.py`: `HabitCheckInRequest`, `HabitCheckInResponse`
- Extend `repository.py`: `HabitRepository.create_check_in()`, `get_check_in_by_key()`
- Extend `service.py`: `HabitService.process_check_in()`
- Extend `api.py`: `POST /v1/habits/check-ins`
- `tests/modules/habits/test_checkin_idempotency.py`
- `tests/modules/habits/test_checkin_concurrency.py`

## 9. Files to Modify
- `src/noorheroes/modules/habits/service.py` — inject `RewardService`, call B-03 `StreakService` (built next) after successful check-in (stub call acceptable until B-03 lands; sequence B-02 before B-03 per numbering, but the streak-trigger call can be added as a follow-up hook — flag explicitly in code as `# TODO(B-03): trigger streak recalculation`).

## 10. Backend Requirements
- Database-level `UNIQUE(child_id, habit_id, local_date)` constraint on `habit_log` — the primary integrity guarantee, not an application-level check alone.
- Database-level `UNIQUE(client_request_id)` constraint.
- On unique-constraint violation (`IntegrityError`), catch it in the repository/service layer and re-fetch + return the original row's result rather than propagating a 500/409.
- `local_date` bounds validation: reject `> 1 day` in the future; accept up to `14 days` in the past.
- Daily cap enforcement delegated to `RewardService` (existing shared cap logic) — do not reimplement cap logic inside `habits`.

## 11. KMP Requirements
Not applicable directly; consumed by K-01/K-06 (`HabitRepository.checkIn()` → this endpoint, offline outbox).

## 12. NextJS Requirements
Not applicable.

## 13. API Contract

**Required API**
- **HTTP Method:** POST
- **Endpoint:** `/v1/habits/check-ins`
- **Request:**
```json
{ "habit_id": "uuid", "local_date": "2026-08-16", "timezone": "Asia/Dubai", "source": "self", "note_category": null, "client_request_id": "uuid" }
```
- **Response 200:**
```json
{ "checked": true, "reward": { "xp": 20, "noor_points": 10 }, "daily_cap_reached": false, "streak": { "current": 6, "state": "active" } }
```
- **Authentication:** Bearer, child-mode
- **Authorization:** child may only check in their own habits
- **Validation:** `local_date` bounds (§10); `habit_id` must belong to the child and be `active`
- **Error Responses:** `400` invalid/out-of-bounds `local_date`; `401` unauthenticated; `403` habit not owned by child; `404` unknown habit_id

## 14. Database Requirements
- `habit_log`: `log_id UUID PK`, `child_id UUID FK`, `habit_id UUID FK`, `local_date DATE`, `timezone VARCHAR`, `source VARCHAR`, `verified_by_parent BOOLEAN DEFAULT false`, `note_category VARCHAR NULL`, `client_request_id VARCHAR`, `created_at TIMESTAMPTZ`.
- `UNIQUE(child_id, habit_id, local_date)`, `UNIQUE(client_request_id)`.
- Index `(child_id, local_date DESC)`.
- Append-only/immutable per PRD §4.3 — no update/delete endpoints on this table.

## 15. Validation
- Concurrency test: 10 concurrent identical-key requests → exactly 1 row, 1 reward, 10× 200 responses (mandatory, non-bypassable CI gate per PRD §10).
- Boundary tests for both future and past `local_date` limits.

## 16. Authentication
Bearer JWT, child-mode session.

## 17. Authorization
Child restricted to own `child_id`/owned `habit_id`s only.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Duplicate check-in (same key) | Return original 200 result, no error, no new reward |
| Concurrent duplicate requests | DB constraint resolves race; all callers get consistent original result |
| `local_date` too far in future/past | 400, clear validation message |
| Habit not owned/inactive | 403/404 |
| Reward service failure | Check-in row still persists; reward marked pending/retried async — never lose the child's local success state |

## 19. Offline First
Endpoint designed to be safely retried by the client's offline outbox (K-06) any number of times without side effects beyond the first successful call.

## 20. Local Data
N/A (backend); client-side outbox detailed in K-06.

## 21. Localization
`note_category` values are enum keys resolved to localized labels client-side, not free text required server-side.

## 22. RTL
N/A.

## 23. Analytics
Emit `habit_checked_in` (fresh) vs `habit_checkin_duplicate_ignored` (idempotent replay) as a response flag the client uses to fire the correct event (per §6.6 of PRD Android section) — include a `was_duplicate: boolean` field in the response for this purpose.

## 24. Performance
Single round-trip write with constraint-based race resolution avoids explicit application-level locking; p95 sync target < 1s per PRD NFR.

## 25. Security
Reward-farming prevention is the primary security property of this endpoint; enforced at the database layer, not just application logic (defense-in-depth).

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, PostgreSQL unique constraints, Pydantic v2, pytest-asyncio for concurrency tests.

## 27. Testing
- Unit: bounds validation, duplicate-handling logic.
- Integration: full check-in flow with reward issuance.
- Concurrency: 10 parallel identical requests (mandatory).
- Backfill: historical `local_date` within 14-day window accepted; chronological reconciliation with B-03 once streak trigger is wired.

## 28. Documentation
OpenAPI schema with explicit idempotency-behavior description (200 on duplicate, not 409) so client/API consumers don't mistakenly treat replay as an error.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Extend HabitLog Model & Constraints**
- Objective: Add `HabitLog` with both unique constraints.
- Why Required: This is the structural reward-farming-prevention mechanism.
- Existing Architecture to Follow: `habits` context models pattern from B-01.
- Files to Modify: `src/noorheroes/modules/habits/models.py`
- Business Rules: FR-3.
- Do Not Change: do not weaken or remove the unique constraints under any future change without explicit sign-off.
- Definition of Done: model + constraints defined, migratable.

**Task 02 — Create Migration**
- Files to Create: `alembic/versions/<rev>_create_habit_log_table.py`
- Validation: constraints present as actual DB constraints, not app-only checks.
- Definition of Done: migration applies/rolls back cleanly.

**Task 03 — Create Request/Response Schemas**
- Files to Modify: `schemas.py`
- Implementation Details: `HabitCheckInRequest`/`Response` per §13.
- Validation: Pydantic validators for date bounds pre-check (defense-in-depth ahead of service-layer check).
- Definition of Done: schemas match contract exactly.

**Task 04 — Implement Repository Layer**
- Files to Modify: `repository.py`
- Implementation Details: `create_check_in()` catches `IntegrityError`, re-fetches existing row on conflict.
- Performance: single-statement insert with `ON CONFLICT DO NOTHING` + follow-up select, or catch-and-refetch — choose whichever the existing repository base class idiom uses elsewhere in the codebase for consistency.
- Tests: repository-level duplicate-handling unit test.
- Definition of Done: repository never raises on duplicate key; returns original row.

**Task 05 — Implement Service Layer with Reward Integration**
- Files to Modify: `service.py`
- Existing Files to Reuse: `RewardService.award_points()`
- Business Rules: FR-2, FR-3, FR-4, FR-20.
- Implementation Details: on fresh check-in, call `RewardService.award_points()`; on duplicate, skip reward call entirely and return cached result.
- Error Handling: reward-service failure does not roll back the check-in write.
- Tests: unit tests mocking `RewardService`.
- Definition of Done: correct reward-once-only behavior verified.

**Task 06 — Implement Endpoint**
- Files to Modify: `api.py`
- Authentication/Authorization: per §16/§17.
- Tests: integration test via test client.
- Definition of Done: endpoint live and documented.

**Task 07 — Add Local-Date Bounds Validation**
- Implementation Details: reject `local_date` > 1 day future, > 14 days past.
- Tests: boundary tests for both limits (mandatory per backend AI prompt item 2).
- Definition of Done: both boundary tests passing.

**Task 08 — Add Concurrency Test Suite (Mandatory CI Gate)**
- Files to Create: `tests/modules/habits/test_checkin_concurrency.py`
- Implementation Details: fire 10 concurrent identical-key requests via `asyncio.gather`; assert exactly 1 `habit_log` row, 1 reward grant, all 10 responses 200.
- Definition of Done: test passes reliably (no flakiness) and is wired as a non-bypassable CI gate per PRD §10 DevOps requirement.

**Task 09 — Add Error Handling & Logging**
- Implementation Details: §18 table behaviors; structured logging with correlation IDs; alert-worthy log line on unique-constraint-violation rate spikes (cross-ref N-06 monitoring dashboard).
- Definition of Done: all error paths verified by tests.

**Task 10 — Add API Documentation**
- Documentation: OpenAPI idempotency note; update `FAST-API-INSTRUCTIONS.md` `habits` context entry.
- Definition of Done: docs accurate and reviewed.

**Task 11 — Final Code Review**
- Do Not Change: unique constraints, `RewardService` internals, PostgreSQL/Redis credentials.
- Expected Result: PR merge-ready, CI green including the mandatory concurrency gate.

## 30. Definition of Done
- Reward-farming structurally impossible (DB-enforced), verified by concurrency test.
- Idempotent duplicate handling returns original result, never an error.
- Local-date bounds enforced both directions.
- Reward issuance correctly delegated to existing `RewardService`.

## 31. Final Verification Checklist
- [x] `UNIQUE(child_id, habit_id, local_date)` and `UNIQUE(client_request_id)` present as DB constraints (Verified in `0054_create_habit_log_table.py` & `models.py`)
- [x] 10-concurrent-request test passes (exactly 1 row, 1 reward, 10× 200) (Verified in `tests/modules/habits/test_checkin_concurrency.py`)
- [x] Both `local_date` boundary tests pass (Verified with bounds: -15d returns 400, -14d returns 200, +1d returns 200, +2d returns 400)
- [x] Duplicate submissions return original result, not an error (Verified: returns HTTP 200 with `was_duplicate=true`)
- [x] Reward issuance delegated to existing `RewardService`, not reimplemented (Injected via `deps.py` and called in `service.process_check_in`)
- [x] Error handling matches §18 (400, 401, 403, 404, 422, 500, and graceful reward service degradation)
- [x] OpenAPI documentation complete and idempotency behavior documented (Generated schema covers all 8 status codes and example envelopes)
- [x] CI concurrency gate wired as non-bypassable per DevOps requirement (`test_checkin_concurrency.py` CI blocking gate)
- [x] No PostgreSQL/Redis credential changes (Preserved baseline configurations)

## 32. Implementation Artifacts & Verified Files
- **Database Schema & Migration**:
  - `src/noorheroes/modules/habits/models.py`: `HabitLog` with `uq_habit_log_child_habit_date` and `uq_habit_log_client_request_id`
  - `alembic/versions/0054_create_habit_log_table.py`: Reversible schema migration
- **Domain Layer & Schemas**:
  - `src/noorheroes/modules/habits/schemas.py`: `HabitCheckInRequest`, `HabitCheckInResponse`, `HabitRewardResponse`, `HabitStreakResponse`, `HABIT_CHECKIN_RESPONSES`
  - `src/noorheroes/modules/habits/exceptions.py`: `InvalidLocalDateError`, `HabitInactiveError`, `InvalidChildIdError`, `HabitNotFoundError`
  - `src/noorheroes/modules/habits/events.py`: `HabitCheckedIn` (`habit_checked_in`)
  - `src/noorheroes/common/outbox_relay.py`: Celery `DISPATCH_TABLE` entry `habits.on_habit_checked_in`
  - `src/noorheroes/core/i18n.py`: 4-language translations (`en`, `hi`, `ur`, `ar`) in `ERROR_TRANSLATION_CATALOG`
- **Repository & Service**:
  - `src/noorheroes/modules/habits/repository.py`: `create_check_in()` with nested transaction SAVEPOINT race collision resolution
  - `src/noorheroes/modules/habits/service.py`: `process_check_in()` orchestrating bounds validation, `verify_child_scope`, reward delegation to `RewardService.award_points()`, Redis cache invalidation, and outbox emission
  - `src/noorheroes/modules/habits/deps.py`: `get_habit_service` and `verify_habit_child_scope`
- **API Router**:
  - `src/noorheroes/modules/habits/api.py`: Thin controller `POST /v1/habits/check-ins` with zero AST branching
- **Automated Test Suites**:
  - `tests/modules/habits/test_checkin_idempotency.py`: 27 unit, boundary, security, and repository idempotency tests
  - `tests/modules/habits/test_checkin_concurrency.py`: Mandatory CI Concurrency Gate (10 concurrent requests → 1 row, 1 reward, 10x 200)

