# B-03 — Ramadan Mission Content Delivery API

## 1. Feature Context
Serves each of the 30 nights' content unit (story, dua, mission) sourced entirely from E.29's existing Content Service via `season_id` scoping, with a server-computed gamification-suppression flag for the five Laylatul Qadr nights — no parallel content schema, no client-side date/night logic determining tone.

## 2. Parent Feature
F.36 — Ramadan Mode

## 3. Sub-feature
1.3 Ramadan Mission Content Delivery API (ID: **B-03**)

## 4. Objective
Build `GET /v1/ramadan/missions/{night}`, resolving the night's content unit from E.29's `content_versions` (`season_id`-scoped) and attaching a server-computed `gamification_suppressed` flag.

## 5. Business Requirements
- FR-7: each of the 30 nights follows the same `content_items`/`content_versions` schema as all other content, `season_id`-scoped — no parallel content schema.
- FR-12: Laylatul Qadr nights (21/23/25/27/29) deliberately suppress gamification, reliably applied, never dependent on manual editorial memory.
- §5 Backend AI prompt item 2: `gamification_suppressed` flag SERVER-COMPUTED for nights 21/23/25/27/29.
- Edge Case 5: missed nights remain completable retroactively, never locked out.

## 6. Existing Architecture
`ramadan` bounded context, `app/ramadan/routers/mission_router.py`, delegating content retrieval to E.29's existing `ContentService`/`ContentRepository` rather than duplicating query logic.

## 7. Existing Code to Reuse
- E.29's `app/content/services/content_service.py::ContentService.get_version(content_version_id)` (or equivalent per `content` context in `FAST-API-INSTRUCTIONS.md` §5.4)
- `app/shared/base_service.py::BaseService`
- `core/deps.py::get_current_parent` / `get_current_child`

## 8. Files to Create
- `app/ramadan/routers/mission_router.py`
- `app/ramadan/services/mission_service.py`
- `app/ramadan/repositories/mission_repository.py`
- `app/ramadan/schemas/mission_schema.py`
- `app/ramadan/models/mission.py`
- `alembic/versions/xxxx_create_ramadan_missions_table.py`

## 9. Files to Modify
- `app/ramadan/routers/__init__.py` — register router

## 10. Backend Requirements
- `MissionService.get_mission(night, region_or_season_context)`: looks up `ramadan_missions` for the given `night_number` within the caller's resolved campaign/season, then fetches the linked `content_version_id` via E.29's `ContentService` — no content fields are duplicated or cached redundantly in `ramadan_missions` beyond the FK.
- Suppression computation: `gamification_suppressed = ramadan_missions.is_laylatul_qadr` (persisted, editorially tagged via N-03, not derived from a hardcoded night list in application code — the single source of truth is the database column set by content scheduling).
- Not-yet-available handling: a night outside the currently active/unlocked range returns a distinct "not yet available" response state, while a past *missed* night remains fully servable and completable (Edge Case 5) — these are two different states and must not be conflated.
- Unpublished-content handling: if the linked `content_version_id` has not completed scholar approval (cross-ref N-06's deadline tracker), the endpoint must not serve draft content to end users.

## 11. Required API / API Contract
`GET /v1/ramadan/missions/{night}` → `200` night's content unit + `gamification_suppressed: boolean`. **Auth:** `get_current_parent`/`get_current_child`. **Validation:** `night` integer `1..30`. **Error Responses:** `404` for an unconfigured night; `409`/appropriate state payload for not-yet-unlocked vs. simply-missed (see §10).

## 12. Database Requirements
`ramadan_missions(mission_id PK, campaign_id FK, night_number, content_version_id FK, is_laylatul_qadr)`; `CHECK night_number BETWEEN 1 AND 30`; index `(campaign_id, night_number)`.

## 13. Validation
`night` bounded `1..30`; `content_version_id` must reference a scholar-approved, published version at request time.

## 14. Authentication
`get_current_parent` or `get_current_child`.

## 15. Authorization
Standard authenticated-session access — no elevated scope for read.

## 16. Error Handling
Unconfigured night (scheduling gap) → `404` with a clear error code distinguishing it from "not yet unlocked" (client-facing UX differs, per K-03).

## 17. Offline First
Content is designed for pre-download per B.15's existing pattern — this endpoint is the sync source; offline read-through is a KMP-side (K-03) concern, not implemented here.

## 18. Local Data
N/A server-side.

## 19. Localization
Content itself is multi-locale via E.29's existing localization pipeline (reused, not modified) — this endpoint passes through whatever locale-resolution E.29 already performs.

## 20. RTL
N/A server-side — content payload direction is a client rendering concern.

## 21. Analytics
No direct event emission from this endpoint itself; `ramadan_night_mission_completed`/`ramadan_lantern_lit` are emitted by B-05 on completion, not on content read.

## 22. Performance
Cache per `(campaign_id, night_number)` given content is static once published; invalidate on E.29 republish via existing cache-invalidation hooks (do not build a parallel invalidation mechanism).

## 23. Security
`gamification_suppressed` must never be settable/overridable by the client — computed server-side from the persisted `is_laylatul_qadr` column exclusively.

## 26. Library Requirements
FastAPI, Pydantic v2, SQLAlchemy 2.0 async, Redis (caching). No new libraries.

## 27. Testing
Unit: `gamification_suppressed` is `true` for exactly the five Laylatul Qadr nights and `false` otherwise (**mandatory**, Backend AI prompt item 2). Integration: content correctly sourced from `content_versions` via `season_id`; unpublished-content is never served; not-yet-unlocked vs. missed-but-completable states return distinct, correct payloads.

## 28. Documentation
OpenAPI docstring documenting the `gamification_suppressed` contract and its five-night scope explicitly.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Write Migration for `ramadan_missions`**
Objective: Night-to-content mapping table with `is_laylatul_qadr` tagging. Files to Create: `alembic/versions/xxxx_create_ramadan_missions_table.py`, `models/mission.py`. Dependencies: B-01's `ramadan_campaigns` (FK target). Tests: migration test. Definition of Done: schema created, `CHECK` constraint enforced.

**Task 02 — Implement `MissionRepository`**
Objective: `(campaign_id, night_number)`-indexed lookup. Files to Create: `repositories/mission_repository.py`. Dependencies: Task 01. Tests: repository tests. Definition of Done: tests pass.

**Task 03 — Implement `MissionService` Delegating to E.29's Content Service**
Objective: Fetch linked content via E.29's existing service, never duplicate content data. Existing Files to Reuse: E.29's `ContentService`. Files to Create: `services/mission_service.py`. Dependencies: Task 02. Do Not Change: E.29's content schema/service internals. Tests: content-delegation test. Definition of Done: tests pass.

**Task 04 — Implement Server-Computed Suppression Flag**
Objective: `gamification_suppressed` derived solely from `is_laylatul_qadr`. Dependencies: Task 03. Tests: **mandatory** — five-night correctness test. Definition of Done: test passes.

**Task 05 — Implement the Router Endpoint with State Handling**
Objective: `GET /v1/ramadan/missions/{night}`, distinguishing not-yet-unlocked vs. missed-but-completable vs. unconfigured. Files to Create: `routers/mission_router.py`. Files to Modify: `routers/__init__.py`. Dependencies: Task 04. Tests: endpoint integration tests for all three states. Definition of Done: tests pass.

**Task 06 — Add Caching with Invalidation on Republish**
Objective: Redis cache keyed `(campaign_id, night_number)`, invalidated via E.29's existing hook. Dependencies: Task 05. Tests: cache-hit/invalidation test. Definition of Done: test passes.

**Task 07 — Add Full Test Suite**
Objective: Complete coverage per §27. Definition of Done: all green in CI.

**Task 08 — Final Code Review**
Objective: Confirm zero content-data duplication outside the `content_version_id` FK and zero hardcoded Laylatul Qadr night list anywhere in this module. Definition of Done: checklist in §30 checked.

## 30. Final Verification Checklist
- [ ] `gamification_suppressed` correct for exactly nights 21/23/25/27/29 — mandatory test passing
- [ ] Content sourced from E.29's `content_versions` with zero duplication
- [ ] Unpublished content never served to end users
- [ ] Not-yet-unlocked and missed-but-completable states correctly distinguished
- [ ] Caching invalidates correctly on content republish

## 31. Definition of Done
Every night's content, including its tonal suppression flag, is served from a single authoritative, reused content pipeline with zero parallel schema or hardcoded editorial logic.
