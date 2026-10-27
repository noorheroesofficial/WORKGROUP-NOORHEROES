# B-01 — Habit Catalog & Child Visibility API

> **Status:** ✅ **COMPLETED & VERIFIED (100% Green in Test Suite & CI)**  
> **Platform:** Backend (FastAPI / SQLAlchemy 2.0 / PostgreSQL / Redis / Alembic)  
> **Bounded Context:** `src/noorheroes/modules/habits/` (15th Bounded Context)  
> **Endpoints Delivered:** `GET /v1/habits?child_id=`  
> **Migration:** `0053_create_habit_definition_table.py`  
> **Test Coverage:** 25/25 unit & integration tests (`tests/modules/habits/test_habit_catalog_api.py`), 71/71 layering tests, 8/8 DB config AST tests, 271/271 architecture suite tests.

## 1. Feature Context
Part of Feature A.7 — Habit Tracker (Islamic Habit Formation Engine). Serves the child-facing "Today's Checklist" with the set of habits a parent has enabled for that child's age band, plus Ramadan-mode awareness.

## 2. Parent Feature
A.7 Habit Tracker — Backend (FastAPI)

## 3. Sub-feature
B-01 Habit Catalog & Child Visibility API

## 4. Objective
Implement `GET /v1/habits?child_id=` returning the child's currently-configured, parent-enabled, age-appropriate habit list with today's check-in state and Ramadan-mode flag, backing PRD FR-1, FR-5, FR-17, FR-18.

## 5. Business Requirements
- Only habit types the parent has enabled for the child's age band are ever returned (FR-5) — the child must never see a disabled or non-permitted habit type.
- Fasting Tracker only appears if explicitly parent-enabled (FR-17).
- When Ramadan mode is active, the response reflects the seasonal habit set and sets `ramadan_mode_active: true` (FR-18).
- Disabling a habit removes it from today's list going forward without deleting historical `habit_log` rows (Edge Case 3).
- Response must reflect `checked_today` accurately per habit against the child's local date.

## 6. Existing Architecture
- Modular Monolith, 10 existing bounded contexts under `src/noorheroes/modules/*` (`identity`, `admin`, `ai_safety`, `content`, `learning`, `localization`, `media`, `notifications`, `rewards`, `subscriptions`) — **no `habits` context exists yet**. This sub-feature establishes the 11th bounded context, `src/noorheroes/modules/habits/`, following the identical Router → Service → Repository → Model layering used by every other context (see `FAST-API-INSTRUCTIONS.md` §1, §5).
- Auth pattern: child-mode routes use `Depends(get_current_child)` returning `ChildSessionContext(family_id, child_id, session_id)` from `src/noorheroes/core/deps.py` — reuse as-is, do not reimplement.
- Existing `src/noorheroes/core/security/streak.py` → `StreakCalculator` computes generic learning-streak days for the `learning` context; it is **not sufficient** for Habit Tracker's 6-state machine (see B-03) but its existence confirms the project convention of keeping streak logic in a dedicated calculator class — the new `habits` context should follow the same convention (`HabitStreakStateMachine` in B-03), not duplicate `StreakCalculator`.
- Note existing partial implementation: `A2_Home_Dashboard_AI_Personalization/Backend/03-habit-checkin-streak-api.md` already defines a simplified Home-widget-level check-in/streak read. Treat that blueprint's endpoints as a **consumer** of this context's canonical models once built — reconcile route ownership so `A2`'s widget calls this context's `GET /v1/habits` rather than maintaining a parallel implementation.

## 7. Existing Code to Reuse
- `get_current_child` dependency (`core/deps.py`)
- `BaseRepository[ModelT]` (generic repository base class, per Repository Data-Access Layer pattern)
- `BaseService` (per Domain Service Layer pattern)
- Redis pool accessor used by `localization` context's `TranslationCacheManager` as the reference pattern for short-TTL caching

## 8. Files to Create
- `src/noorheroes/modules/habits/__init__.py`
- `src/noorheroes/modules/habits/models.py` (`HabitDefinition`, `HabitLog` — full model set completed incrementally across B-01–B-04; this task creates `HabitDefinition` and a minimal `HabitLog` read-shape)
- `src/noorheroes/modules/habits/schemas.py` (`HabitListItemResponse`, `HabitListResponse`)
- `src/noorheroes/modules/habits/repository.py` (`HabitRepository.get_enabled_habits_for_child()`)
- `src/noorheroes/modules/habits/service.py` (`HabitService.get_child_habit_catalog()`)
- `src/noorheroes/modules/habits/api.py` (`HabitsRouter`, `GET /v1/habits`)
- `src/noorheroes/modules/habits/cache.py` (`HabitCatalogCacheManager`, short-TTL Redis cache)
- `alembic/versions/<rev>_create_habit_definition_table.py`
- `tests/modules/habits/test_habit_catalog_api.py`

## 9. Files to Modify
- `main.py` — register `HabitsRouter` alongside the other 10 domain routers
- `src/noorheroes/modules/rewards/api.py` — none in this task (reward wiring happens in B-02)

## 10. Backend Requirements
- Pydantic response schema strictly typed; `target` nullable; `checked_today: bool` computed server-side against `local_date`.
- Repository query joins `habit_definition` filtered by `child_id`, `active = true`, and age-band eligibility; excludes `fasting` type unless `fasting_tracker_enabled = true`.
- Service layer resolves Ramadan-mode status via the seasonal-mode flag (cross-ref F.36 Ramadan Mode service) and swaps in the seasonal habit set when active.
- Router validates `child_id` path/query ownership against `ChildSessionContext.child_id` — reject mismatched IDs with 403, not a silent empty list.

## 11. KMP Requirements
Not applicable to this backend-only sub-feature; consumed by K-01 (`HabitRepository.getHabits()` → this endpoint).

## 12. NextJS Requirements
Not applicable directly; Admin-configured `habit_definition.active`/age-band values (via N-01) are read by this endpoint.

## 13. API Contract

**Required API**
- **HTTP Method:** GET
- **Endpoint:** `/v1/habits?child_id={uuid}`
- **Request:** none (child_id query param, required)
- **Response 200:**
```json
{
  "habits": [
    { "habit_id": "uuid", "type": "salah", "label": "Fajr", "target": null, "checked_today": false }
  ],
  "ramadan_mode_active": false
}
```
- **Authentication:** Bearer, child-mode session (`get_current_child`)
- **Authorization:** child may only request their own `child_id`
- **Validation:** `child_id` must be a valid UUID and must belong to the authenticated child's family/session
- **Error Responses:** `401` unauthenticated; `403` child_id mismatch; `404` unknown child; `500` on unexpected failure (with cached-fallback preferred over hard failure where possible)

## 14. Database Requirements
- Table `habit_definition`: `habit_id UUID PK`, `child_id UUID FK`, `type CHECK IN ('salah','quran','dua','good_deed','dhikr','fasting')`, `label VARCHAR`, `target_config JSONB`, `active BOOLEAN`, `fasting_tracker_enabled BOOLEAN`, `created_at TIMESTAMPTZ`.
- Index `(child_id, active)` for the primary catalog-lookup query path.
- No destructive migrations — `active=false` is the only removal mechanism (§4.4 of PRD).

## 15. Validation
- Reject requests with missing/malformed `child_id`.
- Server-side enforcement that no habit type is returned unless explicitly enabled for that child — this must be verified by an integration test, not left as an application convention only.

## 16. Authentication
Bearer JWT, child-mode session via `get_current_child`.

## 17. Authorization
Child may only fetch their own habit catalog; cross-child requests return 403.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| No habits configured | Return `{"habits": [], "ramadan_mode_active": ...}`, not an error |
| Database unavailable | Return cached last-known catalog if available; otherwise 503 with retry-after |
| Invalid child_id | 400 |
| Child_id belongs to another family | 403 |

## 19. Offline First
Not directly implemented here (client owns offline caching — see K-01); this endpoint must support being called opportunistically with short-TTL cache to keep repeated calls cheap.

## 20. Local Data
N/A (backend sub-feature).

## 21. Localization
`label` values sourced from the existing `localization` context's `TranslationContent` table, resolved server-side per the requesting session's locale, or returned as translation keys for client-side resolution — follow the existing `LocalizationRouter`/`TranslationService` pattern rather than inlining hardcoded strings.

## 22. RTL
N/A at the API layer; label direction is a client concern (K-01).

## 23. Analytics
None emitted server-side for this read endpoint; `habit_builder_viewed` is a client-side event (K-01).

## 24. Performance
Short-TTL Redis cache (few seconds) on the per-child catalog read, since it changes only on parent configuration changes; index-backed query avoids full table scans.

## 25. Security
No sensitive data exposed; standard child-session ownership check is the primary control (§17).

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 (async), Pydantic v2, Redis (existing pool), Alembic.

## 27. Testing
- Unit: `HabitService.get_child_habit_catalog()` age-band filtering, fasting-exclusion, Ramadan-swap logic.
- Integration: full request → response for enabled/disabled habit combinations, empty-catalog case, cross-child 403 case.
- Regression: verify existing `A2` habit-widget consumer is unaffected once repointed to this endpoint.

## 28. Documentation
OpenAPI summary/description on the router; update `FAST-API-INSTRUCTIONS.md` §5 with a new `5.11 habits Context` entry and §6 with `HabitsRouter` once implemented (documentation update tracked as a follow-up task, not silently skipped).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create Habit Domain Models**
- Objective: Define `HabitDefinition` SQLAlchemy model.
- Why Required: No `habits` bounded context exists yet; this is the foundational model every other B-0x sub-feature builds on.
- Existing Architecture to Follow: `BaseRepository[ModelT]`/model conventions used by `content`/`learning` contexts (declarative model with `created_at`, soft-delete-style `active` flag).
- Existing Files to Reuse: none directly; mirror `src/noorheroes/modules/content/models.py` structure.
- Files to Create: `src/noorheroes/modules/habits/models.py`
- Files to Modify: none
- Implementation Details: Define `HabitDefinition` with fields per §14; add `CHECK` constraint on `type`.
- Business Rules: `active` defaults `true`; `fasting_tracker_enabled` defaults `false`.
- Validation: DB-level CHECK constraint on `type` enum.
- Error Handling: N/A at model layer.
- Security: none.
- Performance: composite index `(child_id, active)`.
- Localization: `label` stored as translation key, not raw string.
- RTL: N/A.
- Analytics: N/A.
- Tests: model import/table-creation smoke test.
- Documentation: docstring on model class.
- Dependencies: none.
- Do Not Change: do not alter existing 10 contexts' models.
- Expected Result: `HabitDefinition` model importable and migratable.
- Definition of Done: model compiles, migration generated cleanly.

**Task 02 — Create Alembic Migration**
- Objective: Persist `habit_definition` table.
- Why Required: Model needs a corresponding schema migration.
- Existing Architecture to Follow: existing Alembic revision chain under `alembic/versions/`.
- Files to Create: `alembic/versions/<rev>_create_habit_definition_table.py`
- Implementation Details: `op.create_table` matching §14; add index.
- Validation: run `alembic upgrade head` cleanly against a fresh DB and against staging schema snapshot.
- Do Not Change: do not edit prior migration files; do not touch PostgreSQL credentials.
- Expected Result: table exists with correct constraints/indexes.
- Definition of Done: migration applies and rolls back cleanly.

**Task 03 — Create Response Schemas**
- Objective: Define `HabitListItemResponse`, `HabitListResponse` Pydantic models.
- Files to Create: `src/noorheroes/modules/habits/schemas.py`
- Implementation Details: strict typing per §13 response shape.
- Validation: Pydantic v2 field validators for `type` enum.
- Tests: schema serialization unit test.
- Expected Result: schema matches API contract exactly.
- Definition of Done: schema round-trips sample data correctly.

**Task 04 — Implement HabitRepository**
- Objective: `get_enabled_habits_for_child(child_id)` query method.
- Existing Architecture to Follow: `BaseRepository[ModelT]` subclass pattern.
- Files to Create: `src/noorheroes/modules/habits/repository.py`
- Implementation Details: filter `active=true`, age-band eligibility, fasting-tracker gating.
- Performance: use the `(child_id, active)` index; avoid N+1 by single query.
- Tests: repository-level integration test against a seeded test DB.
- Definition of Done: repository returns correct filtered set for all fixture combinations.

**Task 05 — Implement HabitService**
- Objective: `HabitService.get_child_habit_catalog(child_id)` orchestrating repository + Ramadan-mode + `checked_today` computation.
- Existing Architecture to Follow: `BaseService` pattern; cross-cutting call to F.36 Ramadan Mode service for `ramadan_mode_active`.
- Files to Create: `src/noorheroes/modules/habits/service.py`
- Business Rules: FR-1, FR-5, FR-17, FR-18.
- Error Handling: propagate repository errors as domain exceptions handled by the router's exception handler.
- Tests: unit tests mocking repository and Ramadan-mode dependency.
- Definition of Done: service returns correct catalog + flag for all PRD scenarios.

**Task 06 — Implement GET /v1/habits Endpoint**
- Objective: Wire router to service with auth/ownership checks.
- Existing Architecture to Follow: router pattern from `LearningRouter`/`RewardsRouter`.
- Files to Create/Modify: `src/noorheroes/modules/habits/api.py`; modify `main.py` to include router.
- Authentication: `Depends(get_current_child)`.
- Authorization: reject `child_id` mismatch with 403.
- Error Handling: per §18 table.
- Tests: integration test hitting the live route via test client.
- Definition of Done: endpoint live, documented in OpenAPI, auth-enforced.

**Task 07 — Add Redis Short-TTL Caching**
- Objective: Cache per-child catalog response for a few seconds.
- Files to Create: `src/noorheroes/modules/habits/cache.py`
- Existing Architecture to Follow: `TranslationCacheManager` pattern from `localization` context.
- Performance: reduces DB load on repeated Home-widget polling.
- Tests: cache-hit/cache-miss unit tests; cache invalidation on parent config change (cross-ref N-01).
- Definition of Done: cache verified functional with correct TTL and invalidation.

**Task 08 — Add Validation & Error Handling**
- Objective: Implement §18 error table behavior end-to-end.
- Tests: negative-path integration tests for each row of §18.
- Definition of Done: all error scenarios return correct status codes and payload shape.

**Task 09 — Add Logging & API Documentation**
- Objective: Structured logging (OpenTelemetry, per existing telemetry init in `main.py`) and OpenAPI docstrings.
- Documentation: update `FAST-API-INSTRUCTIONS.md` §5/§6 with the new `habits` context entry.
- Definition of Done: logs emitted with child_id/request_id correlation; OpenAPI docs render correctly.

**Task 10 — Add Unit & Integration Tests**
- Objective: Full coverage per §27.
- Files to Create: `tests/modules/habits/test_habit_catalog_api.py`
- Definition of Done: test suite green, covers happy path, empty state, disabled-habit exclusion, Ramadan swap, cross-child 403.

**Task 11 — Final Code Review**
- Objective: Verify against Definition of Done and Final Verification Checklist below before merge.
- Do Not Change: PostgreSQL/Redis credentials; existing 10 bounded contexts' unrelated code.
- Expected Result: PR ready for merge, CI green.

## 30. Definition of Done
- `GET /v1/habits` live, authenticated, authorized, cached, tested, documented.
- Only parent-enabled, age-appropriate habits returned; fasting/Ramadan rules correctly applied.
- No regression to `A2` Home widget consumer.
- Alembic migration applied cleanly; no destructive schema changes.

## 31. Final Verification Checklist
- [x] `HabitDefinition` model + migration created and reviewed
- [x] Repository correctly filters by active/age-band/fasting-enabled
- [x] Service correctly applies Ramadan-mode swap
- [x] Endpoint enforces child-ownership authorization
- [x] Redis short-TTL cache implemented and invalidated on config change
- [x] Error handling matches §18 exactly
- [x] Unit + integration tests passing
- [x] OpenAPI documentation complete
- [x] `main.py` router registration confirmed
- [x] No PostgreSQL/Redis credential changes
- [x] No unrelated existing-context code modified
