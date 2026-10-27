# B-05 — Continue Learning & Continue Watching Progress API

## 1. Feature Context
NoorHeroes Child App, Feature A.2. Tracks the furthest-valid resume position per content item per child, powering the "Continue Learning" and "Continue Watching" rails on Home.

## 2. Parent Feature
A.2 — Child Home Dashboard & AI Personalization

## 3. Sub-feature
1.5 Continue Learning & Continue Watching Progress API (ID: B-05)

## 4. Objective
Implement `GET /v1/progress/resume`, returning deduplicated, type-segmented furthest-valid resume positions, resolving the sync-race edge case deterministically (most-recently-interacted item wins when two items of the same type are equally "furthest").

## 5. Business Requirements
Per PRD FR-3, Edge Case 1, §3.4, §4.2:
- Furthest-valid resume position per content type, sourced from Progress Service, never duplicated across "Continue Learning" and "Continue Watching" (type-segmented, not incorrectly deduplicated across types).
- Two equally "furthest" same-type items (sync race) → show only the most-recently-interacted-with one; the other surfaces lower in Recommended Next Step, not duplicated.
- Withdrawn content between cache time and tap time → graceful "no longer available," silent cache removal client-side (client concern; server must return a clean 404-equivalent signal, not a raw 404).

## 6. Existing Architecture
FastAPI service-layer pattern; this is one of B-01's fan-out dependencies — conform to the `ProgressClient` contract from B-01 Task 02.

## 7. Existing Code to Reuse
Content Catalog client (for withdrawn-content checks); A.1 auth dependency.

## 8. Files to Create
- `app/routers/progress.py`
- `app/services/progress_service.py`
- `app/repositories/progress_repository.py`
- `app/models/progress_record.py`
- `alembic/versions/xxxx_create_progress_record_table.py`
- `tests/unit/test_progress_dedup_race.py`

## 9. Files to Modify
- `app/main.py`

## 10. Backend Requirements
- `progress_record` upserted by each content feature (Stories, Quran, Quiz) on activity — this sub-feature owns the *read/aggregation* API and the table schema, not necessarily every write path (coordinate: other features write `furthest_position_percent` via their own completion/progress-update calls against this shared table/service).
- Query returns, per `content_type`, the single most-recently-updated `progress_record` where `0 < furthest_position_percent < 100` (in-progress, not completed), bounded to a max rail size (10 items) server-side.
- Deduplication is by `content_type` grouping, not by squashing all content types into one list.

## 11. KMP Requirements
Not implemented here. Consumed by K-02 (Continue Learning/Watching rails).

## 12. NextJS Requirements
Not applicable directly.

## 13. API Contract

**Endpoint:** `GET /v1/progress/resume`
**Auth:** Bearer (child-mode)
**Response 200:** Array of furthest-valid positions per content type, deduplicated per content item, e.g.:
```json
{
  "continue_learning": [ { "content_id": "...", "content_type": "story", "progress_percent": 42, "updated_at": "..." } ],
  "continue_watching": [ { "content_id": "...", "content_type": "video", "progress_percent": 60, "updated_at": "..." } ]
}
```

## 14. Database Requirements
Per PRD §4.2: `progress_record(progress_id PK, child_id FK, content_id FK, content_type, furthest_position_percent, updated_at)`; `UNIQUE(child_id, content_id)`; index on `(child_id, content_type, updated_at DESC)`.

## 15. Validation
`furthest_position_percent` bounded `[0,100]`; upsert logic must never allow position to regress below a previously recorded value from an out-of-order/late-arriving update (use a `WHERE furthest_position_percent < :new_value OR updated_at < :new_updated_at` conditional upsert, or equivalent, to resolve the sync-race deterministically by recency).

## 16. Authentication
Bearer JWT (child-mode session).

## 17. Authorization
Scoped to authenticated `child_id`; no cross-child progress access.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Progress Service failure | B-01 hides `continue_learning`/`continue_watching` sections gracefully |
| Withdrawn content referenced | Content Catalog lookup returns "unavailable"; this service excludes it from the response rather than returning a broken reference |

## 19. Offline First
Not applicable server-side.

## 20. Local Data
Not applicable (backend). See K-02/K-07 for client caching.

## 21. Localization
Content titles resolved via Content Catalog (already localized).

## 22. RTL
N/A (backend).

## 23. Analytics
Backend does not fire `continue_learning_resumed`/`continue_watching_resumed` (client-fired).

## 24. Performance
Query must use the `(child_id, content_type, updated_at DESC)` index; avoid N+1 lookups against Content Catalog by batching content-id lookups for withdrawn-content filtering.

## 25. Security
Scoped strictly to `child_id`; no enumeration of other children's progress via content_id guessing (authorization check on every row returned, not just at the query's WHERE clause level, as defense-in-depth).

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0, Alembic, pytest-asyncio.

## 27. Testing
- Unit: sync-race resolution (two same-type items, equal position, different `updated_at` → most recent wins).
- Unit: type-segmentation (no cross-type dedup bleed).
- Integration: withdrawn-content exclusion.
- Integration: progress-regression prevention (late-arriving stale update does not overwrite a newer position).

## 28. Documentation
OpenAPI docs; note the conditional-upsert race-resolution logic explicitly since it's easy to regress accidentally.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create `progress_record` Table + Migration**
- Objective: Shared progress table per PRD ER diagram.
- Why Required: Foundational data layer, shared write target for other content features.
- Existing Architecture to Follow: Alembic/SQLAlchemy conventions.
- Existing Files to Reuse: Base model class.
- Files to Create: `app/models/progress_record.py`, `alembic/versions/xxxx_create_progress_record_table.py`
- Files to Modify: none
- Implementation Details: Exact fields/constraints per PRD §4.2.
- Business Rules: `UNIQUE(child_id, content_id)` — one row per child+content.
- Validation: CHECK `furthest_position_percent BETWEEN 0 AND 100`.
- Error Handling: N/A.
- Security: N/A.
- Performance: Index per spec.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Migration test.
- Documentation: Docstring noting this table is a shared write target across content features.
- Dependencies: None.
- Do Not Change: Do not alter PostgreSQL credentials.
- Expected Result: Table created.
- Definition of Done: Migration passes.

**Task 02 — Implement Conditional Upsert (Race-Safe Progress Write Helper)**
- Objective: Provide a reusable upsert function other content features can call safely.
- Why Required: Resolves Edge Case 1 (sync race) at the write layer, not just the read layer.
- Existing Architecture to Follow: Repository pattern.
- Existing Files to Reuse: Task 01 model.
- Files to Create: `app/repositories/progress_repository.py`
- Files to Modify: none
- Implementation Details: `upsert_progress(child_id, content_id, content_type, position, occurred_at)` using `INSERT ... ON CONFLICT (child_id, content_id) DO UPDATE ... WHERE progress_record.updated_at < EXCLUDED.updated_at` (recency-guarded upsert).
- Business Rules: Never regress position from an out-of-order update.
- Validation: Position bounds enforced.
- Error Handling: N/A (upsert is atomic).
- Security: N/A.
- Performance: Single atomic statement, no read-then-write race window.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Concurrency test — two near-simultaneous writes with different `occurred_at`, assert the later one wins deterministically.
- Documentation: Docstring explaining the conflict-resolution guard clause.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Race-safe upsert helper.
- Definition of Done: Concurrency test passes.

**Task 03 — Implement `GET /v1/progress/resume` Read API**
- Objective: Type-segmented, deduplicated resume-position query.
- Why Required: Client-facing contract for K-02 and B-01.
- Existing Architecture to Follow: Router pattern from B-01.
- Existing Files to Reuse: Content Catalog client (withdrawn-content filtering).
- Files to Create: `app/routers/progress.py`, `app/services/progress_service.py`
- Files to Modify: `app/main.py`
- Implementation Details: Group by `content_type`, filter `0 < position < 100`, order by `updated_at DESC`, cap at 10 per type, exclude withdrawn content via Content Catalog batch lookup.
- Business Rules: Type-segmented, not globally deduplicated.
- Validation: Response schema validation.
- Error Handling: Content Catalog failure → include item anyway (fail-open for this non-safety-critical enrichment) or exclude conservatively — choose exclude-conservatively to avoid a dead-link tap, consistent with Edge Case 12's graceful handling philosophy.
- Security: Authorization check on every returned row.
- Performance: Batched Content Catalog lookups, indexed query.
- Localization: Pass-through localized titles.
- RTL: N/A.
- Analytics: N/A.
- Tests: Integration tests for type-segmentation, withdrawn-content exclusion, cap enforcement.
- Documentation: OpenAPI docs.
- Dependencies: Tasks 01, 02.
- Do Not Change: N/A.
- Expected Result: Working endpoint.
- Definition of Done: All tests pass.

## 30. Definition of Done
Deduplicated, race-resolved, type-segmented resume API integrated as a B-01 fan-out dependency; all tests green.

## 31. Final Verification Checklist
- [x] `UNIQUE(child_id, content_id)` enforced
- [x] Conditional upsert prevents regression from out-of-order writes
- [x] Sync-race edge case resolved deterministically (most recent wins)
- [x] Type-segmentation confirmed (no cross-type dedup bleed)
- [x] Withdrawn content excluded gracefully, no dead links
- [x] Cross-child authorization enforced on every row
- [x] All tests pass

## 32. Implementation & Verification Summary

- **Completed Components**:
  1. **Database Migration (`alembic/versions/0083_create_progress_record_table.py`)**:
     - Created table `progress_record` with primary key `id` (VARCHAR(36)), `child_id`, `content_id`, `content_type`, `furthest_position_percent`, `title`, `thumbnail_url`, `created_at`, `updated_at`.
     - Added unique constraint `uq_progress_record_child_content` on `(child_id, content_id)`.
     - Added check constraint `ck_progress_record_position_bounds` (`furthest_position_percent >= 0.0 AND furthest_position_percent <= 100.0`).
     - Added index `ix_progress_record_child_type_updated` on `(child_id, content_type, updated_at DESC)`.
  2. **Core Domain Model (`src/noorheroes/modules/progress/models.py`)**:
     - `ProgressRecord(Base)` mapping all fields with standard timestamps and constraints.
  3. **Data Transfer Objects (`src/noorheroes/modules/progress/schemas.py`)**:
     - `ProgressItemDTO`, `ProgressResumeResponse`, `ProgressUpsertRequest`, and `ProgressUpsertResponse`.
     - Dual-wire camelCase and snake_case support with aliases (`continueLearning`/`continue_learning`, `continueWatching`/`continue_watching`, `contentId`/`content_id`, `furthestPositionPercent`/`furthest_position_percent`).
  4. **Data Access Repository (`src/noorheroes/modules/progress/repository.py`)**:
     - `ProgressRepository.upsert_progress`: Recency-guarded conditional upsert ensuring monotonic progression (`furthest_position_percent = max(existing, new)`), preventing stale network packets from regressing child progress.
     - `ProgressRepository.get_in_progress_records`: Fetches records filtered strictly by `0.0 < furthest_position_percent < 100.0`, sorted by `updated_at DESC`.
  5. **Domain Service (`src/noorheroes/modules/progress/service.py`)**:
     - `ProgressService.get_resume_rails`: Type segmentation into `continue_learning` (`story`, `quran`, `quiz`, `lesson`) and `continue_watching` (`video`, `animation`, `episode`) with zero cross-type dedup bleed; recency sorting for sync-race resolution; catalog withdrawn content filtering; and capping each rail at 10 items.
     - `ProgressService.record_progress`: Validates child tenancy and forwards updates to repository.
  6. **FastAPI Endpoints & DI (`src/noorheroes/modules/progress/api.py`, `deps.py`)**:
     - `GET /v1/progress/resume`: Authenticated via `ChildSessionContext`, child-scoped.
     - `POST /v1/progress/record`: Idempotent, monotonic progress recording.
  7. **Backwards-Compatibility Facade (`app/`)**:
     - Re-exported all components under `app/models/progress_record.py`, `app/repositories/progress_repository.py`, `app/services/progress_service.py`, `app/schemas/progress.py`, and `app/routers/progress.py`.
  8. **Upstream Integration**:
     - Mounted in `src/noorheroes/api/v1/router.py`.
     - Updated `ProgressClient` in `src/noorheroes/modules/home/clients/progress_client.py` to seamlessly parse dual keys.
- **Verification Results**:
  - `tests/unit/test_progress_dedup_race.py`: 16/16 tests passed (100% pass rate across all edge cases).
  - `tests/integration/test_progress_integration.py`: 4/4 integration tests passed (regression prevention, withdrawn content, concurrency simulation, HTTP cycle).
  - Combined Regression Suite (progress unit, progress integration, mission cap trigger, home aggregation, app facade, home degradation): 70/70 tests passed (100% green).
  - OpenAPI classification: Purely MINOR additive changes (`+ /v1/progress/resume`, `+ /v1/progress/record`), 0 breaking changes.
