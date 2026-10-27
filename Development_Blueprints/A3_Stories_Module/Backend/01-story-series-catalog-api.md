# B-01 — Story & Series Catalog API

## 1. Feature Context
The entry point into the Stories Module: a filterable, paginated, locale-aware catalog of story series/episodes (Bedtime, Prophet Stories, Islamic Shorts, Series, Values & Manners, Ramadan & Eid) and a Story Detail read that surfaces per-episode unlock state, scholar-approval provenance, and withdrawn-content handling. Must never expose unreviewed or withdrawn content, and must never leak locked-episode media access at this layer (that is enforced downstream by B-07).

## 2. Parent Feature
Feature A.3 — Stories Module (Animated Storytelling System)

## 3. Sub-feature
1.1 Story & Series Catalog API (ID: **B-01**)

## 4. Objective
Extend the existing `content` bounded context (`ContentItem`, `Series`, `ContentRepository`, `ContentService`, `ContentRouter`) with Stories-specific catalog and detail reads: category/age-band/locale/format/downloaded-only filtering, cursor pagination, per-episode `unlock_state` annotation (read-only consumption of B-02's engine), and `410 CONTENT_WITHDRAWN` handling — without forking a parallel catalog stack.

## 5. Business Requirements
- FR-1: Library organizes content into exactly: Bedtime Stories, Prophet Stories, Islamic Shorts, Animated Series, Values & Manners, Ramadan & Eid, Downloads.
- FR-2: Filters: age band, duration, language, format (video/audio/text), topic, downloaded-only, free/premium.
- FR-3: Story Detail returns cover, synopsis, episode list (series), age/source/scholar-approval tags, related stories, per-episode progress.
- FR-5: Locked episodes carry the specific unlock-condition text server-side (UI renders it; this API supplies it), never a bare lock flag with no context.
- Edge Case 10: withdrawn content becomes unavailable/non-discoverable while referencing history rows (favorites, progress) remain intact.
- NFR: catalog list p95 acceptable under 10-min CDN-edge cache per filter+locale+age-band combination, invalidated on catalog publish events.

## 6. Existing Architecture
The `content` context already exposes `ContentItem`/`Series` models, `ContentRepository.get_by_age_band()/get_series_by_id()`, `ContentService.get_content_by_id()/list_catalog_by_age_band()`, and `ContentRouter` (`GET/POST /v1/content/catalog`). Stories introduces two Stories-specific extension tables (`story_episode`, `content_moral_version` — the latter owned by B-06) that FK into the existing `Series`/`ContentItem` rows rather than duplicating a parallel catalog. This sub-feature **extends** `ContentRepository`/`ContentService`/`ContentRouter` in place, following the same Router → Service → Repository → Postgres layering, `BaseService`/`BaseRepository`, and Redis edge-cache pattern used elsewhere in the module.

## 7. Existing Code to Reuse
- `modules/content/api.py::ContentRouter`
- `modules/content/service.py::ContentService` (extend, do not fork)
- `modules/content/repository.py::ContentRepository` (`get_by_age_band()` pattern — mirror for full filter set)
- `modules/content/models.py::ContentItem`, `Series`
- `core/deps.py::get_current_child`, `get_current_parent`
- `infrastructure/redis.py::get_redis_pool`
- `common/base_service.py`, `common/base_repository.py`
- `core/exceptions.py` (`NotFoundError`, `ValidationError`)

## 8. Files to Create
- `src/noorheroes/modules/content/story_models.py` — `StoryEpisodeOrm` (FK `series_id` → `Series.series_id`; fields per PRD §4: `episode_number`, `format`, `duration_seconds`, `unlock_threshold_config` JSONB, `scholar_approval_status`, `is_bedtime_eligible`, `is_withdrawn`)
- `alembic/versions/xxxx_add_story_episode.py`
- `src/noorheroes/modules/content/story_schemas.py` — `StoryCatalogFilterParams`, `StorySummaryResponse`, `StoryDetailResponse`, `EpisodeSummaryResponse` (with `unlock_state: "unlocked"|"locked"`, `unlock_condition: str | None`)
- `src/noorheroes/modules/content/story_repository.py` — `StoryEpisodeRepository` (extends `BaseRepository`)
- `tests/modules/content/test_story_catalog_service.py`
- `tests/modules/content/test_story_catalog_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/content/service.py::ContentService` — add `list_story_catalog(filters, cursor)` and `get_story_detail(content_id, child_ctx)` methods (additive; do not change existing `list_catalog_by_age_band()` signature/behavior used by other content types)
- `src/noorheroes/modules/content/api.py::ContentRouter` — add `GET /v1/content` (Stories-scoped catalog, `type=story`) and `GET /v1/content/{id}`
- `src/noorheroes/modules/content/repository.py::ContentRepository` — add cursor-pagination helper shared with `StoryEpisodeRepository`

## 10. Backend Requirements
- `list_story_catalog()`: filter by `category, age_band, locale, format, downloaded_only, type=story`; exclude rows where `story_episode.is_withdrawn = true`; cursor-based pagination, `limit` capped at 30.
- `get_story_detail()`: assemble synopsis, episode list, scholar-approval tags, related content IDs; for each episode call B-02's `UnlockEngine.get_unlock_state(child_id, episode_id)` (read-only, never recompute unlock logic here) and attach `unlock_state` + `unlock_condition` text.
- Withdrawn content: `GET /v1/content/{id}` on a `story_episode.is_withdrawn=true` row returns `410 CONTENT_WITHDRAWN` (not `404`); the same row is excluded from all list/search results.
- Response caching: 10-minute Redis/CDN-edge cache keyed on `(filters_hash, locale, age_band)`; explicit invalidation triggered by the catalog-publish outbox event consumed from B-11.

## 11. API Contract

### `GET /v1/content?type=story&category=&age_band=&locale=&format=&downloaded_only=`
- Auth: Bearer (child-mode). Response 200: paginated array of story/series summaries. Pagination: cursor-based, `limit` max 30/page. Caching: 10-min CDN-edge cacheable per filter-combination+locale+age-band, invalidated on catalog publish events. Errors: `400 INVALID_FILTER`, `401 UNAUTHORIZED`.

### `GET /v1/content/{id}`
- Auth: Bearer (child-mode). Response 200: full Story Detail — synopsis, episode list with `unlock_state` per episode (`unlocked|locked` + `unlock_condition` text if locked), scholar-approval metadata, related content IDs. Errors: `404 CONTENT_NOT_FOUND`, `410 CONTENT_WITHDRAWN`, `401 UNAUTHORIZED`.

## 12. Database Requirements
- `story_episode`: FK `series_id` → `Series.series_id`; `UNIQUE(series_id, episode_number)`; index `(series_id, episode_number)`.
- Soft delete: `story_episode.is_withdrawn = true` used instead of deletion; never hard-delete (owned/mutated by B-14, read-only here).
- No modification to existing `Series`/`ContentItem` tables beyond the new FK relationship from `story_episode`.

## 13. Validation
- Reject unknown/invalid `category`, `age_band`, `locale`, `format` filter values (`400 INVALID_FILTER`) rather than silently ignoring them.
- `limit` clamped server-side to 30 regardless of client-requested value.
- Pydantic strict schemas — reject unexpected extra query params.

## 14. Authentication
- Both endpoints require a valid child-mode Bearer token via existing `get_current_child` dependency.

## 15. Authorization
- No additional RBAC beyond authenticated child session; entitlement/premium-tier gating is surfaced as response metadata only here (hard enforcement happens at B-07 manifest issuance, never at catalog read).

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| Withdrawn content requested by ID | `410 CONTENT_WITHDRAWN`, distinct from `404` |
| Unknown content ID | `404 CONTENT_NOT_FOUND` |
| Invalid filter combination | `400 INVALID_FILTER` with field-level detail |
| Empty category/age-band result | `200` with empty array — client renders empty state, not an error |
| Redis cache unavailable | Fall through to direct DB read, log degraded-cache warning, do not fail the request |
| Database failure | `503`, structured error, logged with correlation ID |

## 17. Security
- No PII in catalog/detail responses.
- Cache keys never include child-identifying data (cache is content-scoped, not child-scoped) to avoid cross-child cache leakage; `unlock_state` is fetched live per-request from B-02, never cached alongside the content payload.
- Rate limiting via existing gateway middleware (no new bespoke limiter needed for read-only catalog traffic).

## 18. Analytics
Emit via `OutboxWriter`: `stories_library_viewed`, `stories_category_filtered`, `story_detail_viewed`, `episode_lock_viewed`, `episode_unlock_condition_tapped`.

## 19. Performance
- Catalog list and detail reads are cache-first; cache-hit path must not touch Postgres.
- N+1 avoidance: episode list + unlock-state annotation batched in a single call to B-02 (`get_unlock_states_bulk(child_id, episode_ids)`), never one Unlock Engine call per episode in a loop.
- Async SQLAlchemy throughout; no blocking calls in the request path.

## 20. Library Requirements
- No new third-party libraries; reuses existing SQLAlchemy 2.0 async, Redis client, Pydantic v2 already present in the `content` module.

## 21. Testing
- Unit: filter-combination correctness, withdrawn-content exclusion from lists, `410` vs `404` distinction, cursor pagination boundaries.
- Integration: cache invalidation on catalog-publish event, bulk unlock-state annotation correctness against a seeded multi-episode series fixture.

## 22. Documentation
Update OpenAPI schema (`export_openapi_schema.py`) and run `classify_openapi_diff.py` to confirm the change is additive/non-breaking to existing `content` consumers (e.g., A.2 Home Dashboard's catalog reads).

## 23. AI Coding Agent Implementation Steps

**Task 01 — Create `StoryEpisodeOrm` Model & Migration**
Objective: Add the `story_episode` table FK'd to the existing `Series`. Why: no existing schema carries episode-level unlock/format/bedtime/withdrawal metadata. Follow: existing SQLAlchemy/Alembic conventions in `modules/content/models.py`. Reuse: `Base`, `TimestampMixin`. Create: `story_models.py`, migration file. Business Rules: `UNIQUE(series_id, episode_number)`. Do Not Change: existing `ContentItem`/`Series` table definitions — only add the new FK'd table. Tests: migration up/down smoke test. Definition of Done: migration clean on fresh DB and staging dry-run.

**Task 02 — Implement Story Catalog & Detail Schemas**
Objective: `story_schemas.py` with filter params and response DTOs including `unlock_state`/`unlock_condition`. Follow: existing Pydantic v2 strict-schema conventions in the module. Tests: schema validation rejects unexpected fields/invalid enums. Definition of Done: schemas importable and used by Task 04/05.

**Task 03 — Implement `StoryEpisodeRepository`**
Objective: Data access for episode rows scoped to a series, withdrawn-exclusion built into the base query. Follow: `BaseRepository` pattern. Implementation: `list_by_series()`, `get_by_id()` (raises typed not-found vs withdrawn distinction upstream in the service, not the repository). Tests: withdrawn rows excluded from `list_by_series()` by default. Definition of Done: repository methods covered by unit tests.

**Task 04 — Extend `ContentService` with `list_story_catalog()` and `get_story_detail()`**
Objective: Business logic assembling catalog/detail responses, calling B-02's bulk unlock-state read. Follow: `BaseService`, additive methods only (existing `list_catalog_by_age_band()` untouched). Business Rules: withdrawn → `410`; unknown → `404`. Dependencies: Task 01–03, B-02's `UnlockEngine.get_unlock_states_bulk()`. Tests: withdrawn/not-found distinction, bulk unlock-state batching (assert exactly one call to the Unlock Engine per detail request, not N calls). Definition of Done: service methods pass all listed tests.

**Task 05 — Add Router Endpoints**
Objective: Wire `GET /v1/content` (type=story) and `GET /v1/content/{id}` into `ContentRouter`. Follow: existing `openapi_extra` security-declaration pattern; no DB access in router. Tests: covered by Task 07. Definition of Done: both endpoints live, documented, and gated by `get_current_child`.

**Task 06 — Implement Redis Edge-Cache Layer**
Objective: 10-minute cache keyed on `(filters_hash, locale, age_band)`, invalidated on catalog-publish outbox event. Reuse: `infrastructure/redis.py::get_redis_pool`. Business Rules: cache never keyed by child ID; unlock-state always fetched live, never cached. Tests: cache-hit skips DB, invalidation event clears the correct keys. Definition of Done: cache-hit/miss/invalidate paths all tested.

**Task 07 — Add Unit & Integration Tests**
Objective: Full coverage per §21. Files: `test_story_catalog_service.py`, `test_story_catalog_api.py`. Definition of Done: all cases green in CI.

**Task 08 — Update OpenAPI Documentation**
Objective: Regenerate and diff-classify against baseline. Definition of Done: non-breaking diff confirmed, no existing `content` consumer contract broken.

**Task 09 — Final Code Review**
Objective: Verify layering rules respected (no DB access in router, no business logic in repository), withdrawn-content handling correct end-to-end, cache never leaks across children. Definition of Done: checklist in §24 fully checked.

## 24. Final Verification Checklist
- [ ] `GET /v1/content` supports all FR-2 filters (category, age band, duration, language, format, downloaded-only, free/premium)
- [ ] Withdrawn content returns `410 CONTENT_WITHDRAWN` from detail read and is excluded from all list results
- [ ] Unknown content ID returns `404 CONTENT_NOT_FOUND`
- [ ] Unlock state/condition text attached per episode via a single bulk call to B-02 (no N+1)
- [ ] Cursor pagination capped at 30/page regardless of client-requested limit
- [ ] 10-minute cache keyed by filters+locale+age-band only (never child-scoped), invalidated on publish events
- [ ] Empty-result categories return `200` with empty array, not an error
- [ ] All analytics events in §18 emitted via `OutboxWriter`
- [ ] Existing `content` module consumers (e.g., A.2 Home Dashboard) unaffected — OpenAPI diff confirmed non-breaking
- [ ] No PostgreSQL/Redis credentials modified

## 25. Definition of Done
Stories Library and Story Detail reads are live on the existing `content` module, correctly filter/paginate/cache, correctly surface server-computed unlock state per episode, and correctly distinguish withdrawn from not-found content — forming the read foundation that B-02 through B-15 and every KMP/NextJS Stories screen depend on.
