# B-03 — Habit Check-In & Streak Tracking API

## 1. Feature Context
NoorHeroes Child App, Feature A.2. Powers the Habit & Good Deed Check-in widget on Home (client-side counterpart: K-03) and feeds the `habits` section and `streak`/`xp` fields of the B-01 Home Aggregation response.

## 2. Parent Feature
A.2 — Child Home Dashboard & AI Personalization

## 3. Sub-feature
1.3 Habit Check-In & Streak Tracking API (ID: B-03)

## 4. Objective
Implement `POST /v1/habits/check-ins` with database-enforced idempotency and one-check-in-per-day-per-habit uniqueness, atomic streak/XP computation, and "Mercy Day" non-punitive missed-day handling, referenced by Home's streak bar.

## 5. Business Requirements
Per PRD FR-7, FR-8, §3.4, §4.2, §5 items 8:
- Support same-screen check-in for at least Salah, Quran reading, daily dua, good deed, dhikr.
- `client_event_id` enforces idempotency for offline-queued duplicate submissions.
- `UNIQUE(habit_id, checkin_date)` DB constraint prevents double check-ins for the same day (not just app-level dedup); a duplicate submit returns idempotent success (`409 ALREADY_CHECKED_TODAY` treated as success by the client), not a hard error.
- Streak display must never use shaming language/visuals; a missed day is handled via "Mercy Day" protection logic, not a broken-streak penalty.

## 6. Existing Architecture
Follow FastAPI + SQLAlchemy 2.0 + Alembic conventions from Core-Architecture docs. This is a mutation endpoint invalidating the `habits` fragment of B-01's Redis cache (`home:{child_id}`) — reuse B-01's `invalidate_section` cache helper rather than writing a new cache-invalidation mechanism.

## 7. Existing Code to Reuse
- B-01's `app/cache/home_cache.py` (`invalidate_section`).
- A.1's child-mode Bearer auth dependency.
- Existing Alembic migration conventions.

## 8. Files to Create
- `app/routers/habits.py`
- `app/services/habit_service.py`
- `app/repositories/habit_repository.py`
- `app/schemas/habit.py`
- `app/models/habit_definition.py`, `app/models/habit_checkin.py`
- `alembic/versions/xxxx_create_habit_tables.py`
- `tests/unit/test_habit_service_mercy_day.py`
- `tests/integration/test_habit_checkin_idempotency.py`

## 9. Files to Modify
- `app/main.py` — register `habits` router

## 10. Backend Requirements
- `POST /v1/habits/check-ins` validates `habit_id` ownership (belongs to the requesting `child_id`), inserts a `habit_checkin` row, catches the unique-violation on `(habit_id, checkin_date)` and converts it to an idempotent success response rather than a 500/409-as-error.
- Streak computation: consecutive-day count with Mercy Day logic — a single missed day within an active streak does not reset it to zero (defined precisely in Task 03 below); exact Mercy Day business rule must be confirmed against the Habit Tracker feature (A.7) if that feature owns the canonical Mercy Day algorithm — do not invent a divergent algorithm; if A.7's blueprint/code is not yet available, implement the rule stated in this PRD (FR-8: "a missed day must be handled via Mercy Day protection logic (defined in A.7 Habit Tracker, referenced here as a Home-display rule)") as a placeholder service function clearly marked for reconciliation with A.7.
- XP award per check-in (fixed or habit-weighted amount — confirm with existing rewards/XP model if one exists elsewhere in the codebase; do not invent a new XP economy in isolation).

## 11. KMP Requirements
Not implemented here. Consumed by K-03 (`HabitRepository.checkIn()`), which generates `client_event_id` at tap-time and reuses it on retry.

## 12. NextJS Requirements
Not applicable — no admin surface owns habit check-in data directly in this sub-feature (Habit definitions/parent configuration are owned by other features, e.g., C.23 Parental Controls / A.7 Habit Tracker admin surfaces, out of scope here).

## 13. API Contract

**Endpoint:** `POST /v1/habits/check-ins`
**Auth:** Bearer (child-mode)
**Request:**
```json
{ "habit_id": "habit_...", "date": "2026-06-22", "client_event_id": "uuid..." }
```
**Response 200:**
```json
{ "checked": true, "current_streak": 6, "xp_awarded": 10 }
```
**Validation:** `client_event_id` enforces idempotency.
**Error Codes:** `409 ALREADY_CHECKED_TODAY` — treated as idempotent success by the client, not a hard error.
**Rate Limiting:** 60 req/min/child.

## 14. Database Requirements
Per PRD §4.2:
- `habit_definition`: FK `child_id`; CHECK `habit_type IN ('salah','quran','dua','good_deed','dhikr','fasting')`; index on `(child_id, active)`.
- `habit_checkin`: FK `habit_id`; `UNIQUE(habit_id, checkin_date)`; `UNIQUE(client_event_id)`; index on `(habit_id, checkin_date DESC)`. Append-only/immutable — never edited post-insert.
- Soft delete: `habit_definition.active = false` instead of deletion, preserving historical `habit_checkin` rows for streak/report accuracy.

## 15. Validation
`habit_id` must belong to the authenticated `child_id` (reject cross-child habit references with `403`/`404`, not a generic 500). `date` must be a valid ISO date not in the future beyond the server's current date (per server time, not client-claimed time, to prevent streak manipulation).

## 16. Authentication
Bearer JWT (child-mode session), same dependency as B-01.

## 17. Authorization
Endpoint scoped to the authenticated `child_id`; a request referencing a `habit_id` owned by a different child returns an authorization error with no data leakage about the other child's habit.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Duplicate check-in (same day, replay or double-tap) | `409 ALREADY_CHECKED_TODAY`, idempotent success semantics |
| `habit_id` not owned by child | `403`/`404`, no leakage |
| Database failure on write | Standard 5xx; client (K-03) queues via offline outbox and retries |
| Invalid `date` (future-dated beyond server time) | `422` |

## 19. Offline First
Not applicable server-side; this endpoint is the sync target for K-03's offline outbox. Must be safely replayable (idempotent) since the client may call it multiple times with the same `client_event_id` after reconnect.

## 20. Local Data
Not applicable (backend). See K-03 for Room-based outbox.

## 21. Localization
`habit_type`/`label` values returned are either locale-agnostic keys (client-localized) or pre-localized strings depending on the existing platform convention — follow whatever pattern A.1's child-profile fields already use (e.g., `preferred_language`-driven server-side localization vs. client-side string-resource keys); do not introduce a second localization pattern.

## 22. RTL
N/A (backend).

## 23. Analytics
Backend does not fire `habit_checkin_completed_from_home` (client-fired per PRD §1.19); ensure the response contains enough data (`current_streak`, `xp_awarded`) for the client to attach correct analytics properties.

## 24. Performance
Single-row insert + streak recomputation must be fast enough to keep the client's optimistic-update reconciliation snappy; avoid recomputing the full historical streak from scratch on every check-in if a materialized/incremental approach is feasible (e.g., store `current_streak` on `habit_definition` and increment/adjust rather than re-scanning all `habit_checkin` rows every time) — but only optimize this way if it doesn't compromise correctness of the Mercy Day logic; correctness takes priority over micro-optimization here.

## 25. Security
`UNIQUE` constraints are DB-layer security against duplicate-submission abuse, not just data integrity. No PII beyond `child_id`/`habit_id` references in logs.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 (async), Alembic, asyncpg (or existing driver), pytest-asyncio.

## 27. Testing
- Unit: Mercy Day streak computation across scenarios (no miss, one miss, two consecutive misses).
- Integration: concurrent duplicate submission (same `client_event_id`) → exactly one `habit_checkin` row.
- Integration: cross-child `habit_id` access attempt → rejected, no leakage.
- Integration: DB-level unique-violation on `(habit_id, checkin_date)` correctly converted to idempotent success response.

## 28. Documentation
OpenAPI docs for `POST /v1/habits/check-ins`; note in the docstring that `409 ALREADY_CHECKED_TODAY` is a *success-equivalent* response for client purposes, to avoid future maintainers "fixing" it into a hard error.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create Database Models & Migration**
- Objective: `habit_definition` and `habit_checkin` tables per PRD ER diagram.
- Why Required: Foundational data layer.
- Existing Architecture to Follow: Existing Alembic migration conventions and SQLAlchemy 2.0 declarative model style.
- Existing Files to Reuse: Base model class (`Base`, timestamp mixins) if already defined in the codebase.
- Files to Create: `app/models/habit_definition.py`, `app/models/habit_checkin.py`, `alembic/versions/xxxx_create_habit_tables.py`
- Files to Modify: none
- Implementation Details: Fields exactly per PRD §4.2; `UNIQUE(habit_id, checkin_date)`, `UNIQUE(client_event_id)`, indexes as specified.
- Business Rules: `habit_checkin` is append-only — no `updated_at`/update path in the model design.
- Validation: DB-level CHECK constraint on `habit_type`.
- Error Handling: N/A at model level.
- Security: Constraints are the security control against duplicate abuse.
- Performance: Indexes per spec support fast streak queries.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Migration up/down test; constraint-violation test (attempt duplicate insert, expect DB error).
- Documentation: Docstring noting append-only design.
- Dependencies: None.
- Do Not Change: Do not modify PostgreSQL credentials.
- Expected Result: Migration applied cleanly.
- Definition of Done: `alembic upgrade head` succeeds; constraint tests pass.

**Task 02 — Create Request/Response Schemas**
- Objective: Pydantic models for the endpoint.
- Why Required: Type-safe I/O contract.
- Existing Architecture to Follow: Schema conventions from B-01.
- Existing Files to Reuse: none.
- Files to Create: `app/schemas/habit.py`
- Files to Modify: none
- Implementation Details: `HabitCheckInRequest(habit_id, date, client_event_id)`, `HabitCheckInResponse(checked, current_streak, xp_awarded)`.
- Business Rules: N/A.
- Validation: `client_event_id` must be a valid UUID string.
- Error Handling: N/A.
- Security: N/A.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Schema validation unit tests.
- Documentation: Docstrings.
- Dependencies: none.
- Do Not Change: N/A.
- Expected Result: Schema file.
- Definition of Done: Tests pass.

**Task 03 — Implement Habit Repository & Mercy Day Streak Logic**
- Objective: Data-access layer + streak computation with Mercy Day protection.
- Why Required: Core business logic (FR-8).
- Existing Architecture to Follow: Repository pattern from Core-Architecture FastAPI docs.
- Existing Files to Reuse: Task 01 models.
- Files to Create: `app/repositories/habit_repository.py`, `app/services/habit_service.py`
- Files to Modify: none
- Implementation Details: `insert_checkin(habit_id, date, client_event_id)` catches unique-violation and returns an "already checked" sentinel rather than raising; `compute_streak(habit_id)` implements Mercy Day (one missed day within an otherwise-continuous streak does not zero it — mark clearly as pending reconciliation with A.7 Habit Tracker's canonical algorithm if that feature's implementation differs).
- Business Rules: Streak/XP must never decrease from a "missed" day alone.
- Validation: `habit_id` ownership check before insert attempt.
- Error Handling: Unique-violation → idempotent success path, not exception bubbling to a 500.
- Security: Ownership check prevents cross-child writes.
- Performance: Streak computed incrementally where possible.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Unit tests for Mercy Day scenarios; integration test for concurrent duplicate insert race (two simultaneous requests with the same `client_event_id`).
- Documentation: Docstring flagging the Mercy Day algorithm as needing reconciliation with A.7 if that feature defines it independently.
- Dependencies: Tasks 01, 02.
- Do Not Change: N/A.
- Expected Result: Working repository/service.
- Definition of Done: Mercy Day and idempotency tests pass.

**Task 04 — Implement Router + Cache Invalidation + Rate Limiting**
- Objective: Expose `POST /v1/habits/check-ins`.
- Why Required: Client-facing entry point.
- Existing Architecture to Follow: Router pattern from B-01.
- Existing Files to Reuse: B-01's `invalidate_section(child_id, "habits")` cache helper; A.1 auth dependency; existing rate-limit dependency.
- Files to Create: `app/routers/habits.py`
- Files to Modify: `app/main.py`
- Implementation Details: On successful (or idempotent-duplicate) check-in, call `invalidate_section(child_id, "habits")` so B-01's next read reflects the update immediately, satisfying FR-17 (in-place streak/XP bar update).
- Business Rules: Ownership + rate limit (60/min/child) enforced.
- Validation: Request schema validation via Task 02 models.
- Error Handling: Per §18 table.
- Security: Ownership enforcement.
- Performance: Cache invalidation is a single targeted Redis operation, not a full-key bust.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A (client-fired).
- Tests: Integration test confirming a subsequent `GET /v1/home` reflects the updated streak without waiting for TTL expiry.
- Documentation: OpenAPI docs.
- Dependencies: Task 03; B-01 Task 04 (cache helper) must exist.
- Do Not Change: N/A.
- Expected Result: Full working endpoint.
- Definition of Done: All integration tests pass, including cross-sub-feature cache-invalidation test with B-01.

## 30. Definition of Done
Idempotent, DB-constrained check-in endpoint with correct Mercy Day streak behavior and immediate Home cache reflection; all tests green.

## 31. Final Verification Checklist
- [x] `UNIQUE(habit_id, checkin_date)` enforced at DB layer
- [x] `UNIQUE(client_event_id)` enforced at DB layer
- [x] Duplicate submission returns idempotent success, not a hard error
- [x] Mercy Day logic does not zero a streak on a single missed day
- [x] Cross-child `habit_id` access rejected with no data leakage
- [x] Habit check-in invalidates only the `habits` cache fragment (not full Home cache)
- [x] Rate limiting enforced (60/min/child)
- [x] All tests pass
