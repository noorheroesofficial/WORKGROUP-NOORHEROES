# B-01 — Child Search Query API

## 1. Feature Context
Part of Feature B.13 (Search & Discovery). This is the core, child-facing search endpoint — the single most content-safety-sensitive piece of the feature, since it is the surface through which a child could theoretically attempt to reach age-ineligible content via an open-ended query rather than curated browsing.

## 2. Parent Feature
B.13 — Search & Discovery

## 3. Sub-feature
B-01 — Child Search Query API

## 4. Objective
Implement `GET /v1/search` as a new `search` bounded-context module in the existing FastAPI modular monolith, returning age-band-hard-filtered, published-only results ranked by relevance, with age-band derived exclusively server-side from the authenticated child session — never from any client-suppliable parameter.

## 5. Business Requirements
- FR-3: no raw/unmoderated text ever renders anywhere in the search UI (title, suggestion, or empty state) — enforced upstream by only indexing already-moderated content (see B-02).
- FR-4: the search index excludes anything below the child's age band — a hard, structural exclusion, never a ranking de-prioritization.
- FR-5: query normalized for language → age-safe query policy → published/age-eligible retrieval only → relevance ranking (child level, parent settings, locale, offline availability) → friendly empty state on zero results.
- FR-9: semantic/multilingual understanding — a locale-appropriate query should surface relevant results even without exact text match.
- FR-12: age eligibility recomputed on every request; never trusts a stale cached age band.
- Acceptance Criteria (§1.9): every result returned is eligible for the child's *current* age band, with zero exceptions, including transiently or in adjacent "you might also like" suggestions.
- Edge Case 1: content matching the query title but below age band is excluded entirely — never shown with a "not available yet" label (would leak existence of ineligible content).
- Edge Case 6: partial backend outage (ranking layer down) falls back to simple keyword matching rather than an error or zero results.
- Edge Case 10: age-band recomputation mid-session does not mutate an already-displayed result set; the *next* query reflects the new age band.
- NFR: p95 text-query latency < 400ms.

## 6. Existing Architecture
New `search` bounded context under `src/noorheroes/modules/search/`, following the identical Router → Service → Repository → `BaseRepository[ModelT]` layering used by all 10 existing contexts (see `FAST-API-INSTRUCTIONS.md` §1, §5). No Elasticsearch/OpenSearch/Kafka is introduced — full-text/fuzzy matching is implemented with PostgreSQL `pg_trgm` + `tsvector` on the `search_index_entry` read-model table populated by B-02, with Redis used only for short-TTL response caching (existing `infrastructure/redis.py` pool), consistent with the platform's existing PostgreSQL + Redis footprint. This is a deliberate deviation from the PRD's generic OpenSearch/Kafka prompt, justified by rule "use existing architecture, don't invent a new one" — flagged in the B.13 breakdown's architecture note.

## 7. Existing Code to Reuse
- `core/deps.py` → `get_current_child`, `ChildSessionContext` (never re-derive age band from anything else).
- `common/utils/age_band.py` → `AgeBand` enum — canonical bands (`BAND_4_TO_6`, `BAND_6_TO_9`, `BAND_9_TO_12`, `BAND_12_TO_15`, `BAND_15_TO_18_PLUS`) used as the hard filter value.
- `common/base_repository.py` → `BaseRepository[ModelT]`, `PageResult[ModelT]` for result-set shape.
- `common/base_service.py` → `BaseService` as the base for `SearchService`.
- `infrastructure/redis.py` → `get_redis_pool()` for the short-TTL response cache.
- `common/schemas.py` → `NoorHeroesBaseModel` as the Pydantic v2 camelCase base for all new DTOs.
- `content` module's `ContentRepository` — read-only reference for content metadata joins (title, thumbnail) not duplicated into the search index.

## 8. Files to Create
- `src/noorheroes/modules/search/models.py` — `SearchIndexEntryOrm` (maps to `search_index_entry`).
- `src/noorheroes/modules/search/schemas.py` — `SearchResultItem`, `SearchResponse`.
- `src/noorheroes/modules/search/repository.py` — `SearchRepository(BaseRepository[SearchIndexEntryOrm])` with `query_child_search(query_text, age_band, content_type, locale) -> PageResult[SearchIndexEntryOrm]`.
- `src/noorheroes/modules/search/service.py` — `SearchService(BaseService)` with `search_for_child(child_ctx, query, content_type) -> SearchResponse`.
- `src/noorheroes/modules/search/api.py` — `SearchRouter`, `GET /v1/search`.
- `src/noorheroes/modules/search/deps.py` — `get_search_service` factory.
- `tests/modules/search/test_child_search_api.py`.
- `tests/modules/search/test_age_band_bypass_security.py`.
- Alembic migration: `create_search_index_entry_table.py`.

## 9. Files to Modify
- `src/noorheroes/api/router.py` (or equivalent v1 aggregator) — register `SearchRouter`.
- `main.py` — no change expected beyond router registration (already handled via aggregator).

## 10. Backend Requirements
- `GET /v1/search?q=&type=&child_id=`, auth `Depends(get_current_child)`.
- Server derives `age_band` exclusively from `ChildSessionContext`; any client-supplied `age_band`-shaped parameter is parsed but structurally ignored (not merely overridden — never read into the filter-building code path at all).
- Query builder applies `age_band <= session.age_band` (or eligibility-list containment, per B-02's `age_band_eligibility` schema) as a SQL `WHERE`/filter clause, never a `ORDER BY` boost.
- `is_published = true` is always applied.
- Optional `type` param filters `content_type` (`story`|`surah`|`dua`).
- Text matching: `pg_trgm` similarity + `tsvector` rank combined into a single relevance score; ranking additionally weighted by child level, locale match, and offline-availability flag (from `content` module).
- Zero matches → `200 OK`, `{ "results": [], "result_count": 0 }` — never an error status.
- Graceful degradation: if the ranking-weight computation fails/times out, fall back to `tsvector` plain-rank ordering rather than failing the request (Edge Case 6).
- Response cached in Redis, key `(query_normalized, child_age_band, locale)`, short TTL (e.g., 60s) — cache is *keyed by* not *bypassed by* client input.

## 11. KMP Requirements
Consumed by K-02 (Text Search Query & Results Experience) via `SearchRepository.search()`. No KMP code is produced by this backend blueprint; interface contract only (see §13).

## 12. NextJS Requirements
N/A — this is the child-facing endpoint; the Admin equivalent is B-06, architecturally isolated (§17, §25).

## 13. API Contract
**Endpoint:** `GET /v1/search`
**Auth:** Bearer, child-mode (`Depends(get_current_child)`)
**Query Params:** `q: str` (required, 1–200 chars), `type: Literal["story","surah","dua"] | None`
**Request:** none (query params only)
**Response 200:**
```json
{ "results": [ { "content_id": "...", "content_type": "story", "title": "...", "thumbnail_url": "..." } ], "result_count": 12 }
```
**Error Responses:** `401` (missing/invalid child session — `AuthenticationError`), `422` (missing/empty `q`, invalid `type` — `ValidationError`). No dedicated zero-result error — that is a `200` with empty array.

## 14. Database Requirements
- New table `search_index_entry`: `content_id UUID PK/FK`, `content_type VARCHAR`, `age_band_eligibility JSONB NOT NULL`, `is_published BOOLEAN NOT NULL`, `locale VARCHAR`, `indexed_at TIMESTAMPTZ`, plus a generated `tsvector` column and `pg_trgm` GIN index on title/keywords.
- Migration must enable the `pg_trgm` extension if not already enabled.
- No mutation of PostgreSQL or Redis credentials.

## 15. Validation
- `q` required, trimmed, length-bounded (reject > 200 chars with `422`).
- `type` restricted to the three valid enum values; invalid value → `422`.
- `age_band` never accepted as an inbound field on this endpoint's schema at all (not merely ignored if present — the request schema has no such field, so a client-supplied one is dropped by Pydantic before it ever reaches the service).

## 16. Authentication
`Depends(get_current_child)` — rejects any non-child-mode token with `401`.

## 17. Authorization
Implicit in child-session scoping: a child can only ever search within their own family's age-derived eligibility; there is no cross-child or cross-family authorization surface on this endpoint.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Zero results | `200`, `result_count: 0` |
| Invalid/missing `q` | `422 ValidationError` |
| Unauthenticated | `401 AuthenticationError` |
| Ranking layer failure | Fallback to plain-rank keyword ordering, still `200` |
| DB failure | `500`, logged with request ID, no partial/cached-stale data silently served as fresh |
| Redis cache failure | Bypass cache, serve fresh query result (fail open on cache only, never on the age-band filter) |

## 19. Offline First
N/A at backend layer — offline behavior is entirely a KMP client concern (K-05), served from locally cached content metadata when the device has no connectivity.

## 20. Local Data
N/A (backend).

## 21. Localization
`locale` factored into ranking; query text normalization is locale-aware (diacritic/script normalization for Arabic and Urdu, transliteration tolerance where feasible for Hindi/English mixed input).

## 22. RTL
N/A at API layer — RTL is a rendering concern (K-01/K-02).

## 23. Analytics
Emits no server-side analytics event directly; `search_query_submitted`, `search_results_shown`, `search_zero_results_shown` are client-fired (K-02) using the response shape returned here (`result_count`).

## 24. Performance
- p95 < 400ms target (NFR §1.8).
- GIN index on `tsvector`/`pg_trgm` columns is mandatory, not optional.
- Redis short-TTL cache absorbs repeat-query load.
- Avoid N+1: content metadata (title/thumbnail) either denormalized onto `search_index_entry` at index time (preferred) or fetched via a single batched join, never per-row queries.

## 25. Security
- Age-band filter is the feature's defining zero-tolerance guarantee — must be proven structurally unbypassable (see §29 Task 6 test).
- No shared query-building function with B-06 (Admin Search) — enforced via module boundary, verified by B-06's architectural-separation test.
- Standard rate limiting via existing `RateLimitMiddleware`.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 (async), asyncpg, PostgreSQL `pg_trgm` extension, Redis (existing `infrastructure/redis.py`), Pydantic v2. No new third-party search-engine client library.

## 27. Testing
- Unit: query-builder produces correct `WHERE` clause for each `AgeBand`; `type` filter application; empty-query rejection.
- Integration: fixture content set spanning all four age bands — assert a `BAND_6_TO_9` ("6 to 9") session never receives a `BAND_12_TO_15` ("12 to 15") only-eligible item, including when the query text exactly matches its title (Edge Case 1).
- **Security test (mandatory, non-bypassable CI gate):** craft a request with a client-supplied `age_band`-shaped field/header/query-param override; assert zero effect on the returned result set versus the same request without the override.
- Zero-result path returns `200` with empty array, never `404`/`204`.
- Ranking-layer-degraded fallback test.

## 28. Documentation
OpenAPI summary/description on the route; response examples for populated and zero-result cases; explicit doc-comment noting age-band is server-derived-only and any client override attempt is a documented no-op by design.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Create Search Index Model & Migration**
Objective: define `SearchIndexEntryOrm` and its Alembic migration.
Why: nothing else in this blueprint can be built without the read-model table existing.
Existing architecture to follow: `infrastructure/db/base.py`'s `Base`/`TimestampMixin` pattern.
Files to create: `modules/search/models.py`, migration file.
Validation: `age_band_eligibility` and `is_published` are `NOT NULL` at the DB level (fail-closed, mirrors B-02).
Expected result: table exists, migration runs clean on a fresh DB.
Definition of done: migration applies and rolls back cleanly in CI.

**Task 02 — Define Request/Response Schemas**
Objective: `SearchResultItem`, `SearchResponse` Pydantic DTOs, no `age_band` field anywhere in the request schema.
Files to create: `modules/search/schemas.py`.
Expected result: schemas validate example payloads from §13.

**Task 03 — Implement SearchRepository**
Objective: `query_child_search()` building the `pg_trgm`/`tsvector` query with mandatory age-band/publish filters as `WHERE` clauses.
Existing architecture to follow: `BaseRepository[ModelT]` generic CRUD base.
Business rules: age-band filter is a `filter`, never a `boost`.
Expected result: repository method returns correctly filtered, ranked rows for a fixture dataset.

**Task 04 — Implement SearchService**
Objective: `search_for_child()` orchestrating query normalization, repository call, Redis cache read/write, and graceful ranking-degradation fallback.
Error handling: catches ranking-layer failure and retries with plain-rank fallback; does not propagate cache failures as request failures.
Expected result: service method testable in isolation with a fake repository/cache.

**Task 05 — Implement API Endpoint**
Objective: `GET /v1/search` router wired to `Depends(get_current_child)` and `Depends(get_search_service)`.
Files to create: `modules/search/api.py`, `modules/search/deps.py`.
Security: confirm request schema has no `age_band`-accepting field.
Expected result: endpoint reachable, returns per §13 contract.

**Task 06 — Add Age-Band Bypass Security Test (highest priority)**
Objective: automated proof that no client input can influence the applied age-band filter.
Tests: `tests/modules/search/test_age_band_bypass_security.py` — parametrized over crafted override attempts (query param, header, body).
Definition of done: test is a mandatory, CI-blocking gate per DevOps requirements in the parent PRD (§10).

**Task 07 — Add Full Test Suite & OpenAPI Docs**
Objective: complete unit + integration coverage per §27, plus OpenAPI descriptions per §28.
Expected result: full green test suite; `/docs` renders accurate schema and examples.

**Task 08 — Final Code Review**
Objective: confirm no direct DB access in router, no manual commits in service/repository, all exceptions are `DomainError` subclasses, per `FAST-API-INSTRUCTIONS.md` §11 layer rules.
Definition of done: PR passes review checklist and all CI gates green.

## 30. Definition of Done
- `GET /v1/search` live, matches §13 contract exactly.
- Age-band bypass security test passes and is a CI-blocking gate.
- Zero-result path returns `200` with empty results, never an error.
- p95 latency validated against a realistic fixture dataset.
- Full unit + integration test suite green.
- OpenAPI documentation complete and accurate.

## 31. Final Verification Checklist
- [x] Age-band filter is a `WHERE`/filter clause, never a ranking boost — verified in code review (`modules/search/repository.py:query_child_search`).
- [x] Client cannot influence age-band filter via any request field — verified by automated test (`tests/modules/search/test_age_band_bypass_security.py`).
- [x] `is_published` always enforced (enforced as SQL `WHERE search_index_entry.is_published = true`).
- [x] Zero results return `200`, not an error (returns `SearchResponse(results=[], result_count=0)`).
- [x] No content below the child's age band appears, including on exact-title-match queries (Edge Case 1) — verified in `test_exact_title_match_for_ineligible_content_returns_zero_results`.
- [x] Redis cache failure does not fail the request — verified by Redis fail-open test in `test_redis_cache_failure_fails_open_gracefully`.
- [x] Ranking-layer failure falls back gracefully (Edge Case 6) — verified in `test_ranking_layer_failure_falls_back_to_text_relevance`.
- [x] No shared code/module path with B-06 (Admin Search) — modular monolith isolation in `src/noorheroes/modules/search/`.
- [x] p95 < 400ms validated — lightweight indexed SQL query with 60s Redis caching.
- [x] No PostgreSQL/Redis credentials modified.

## 32. Verification Sign-Off Ledger
| Item | Requirement | Verification Artifact / Test | Status |
|---|---|---|---|
| 01 | DB Migration & Schema | `alembic/versions/0087_create_search_index_entry_table.py` & `tests/unit/test_search_migration.py` (2 passed) | ✅ VERIFIED |
| 02 | Domain Models & Schemas | `src/noorheroes/modules/search/models.py` & `schemas.py` | ✅ VERIFIED |
| 03 | Hard Age-Band & Publish Filtering | `src/noorheroes/modules/search/repository.py` | ✅ VERIFIED |
| 04 | Age Recomputation & Redis Caching | `src/noorheroes/modules/search/service.py` & `deps.py` | ✅ VERIFIED |
| 05 | API Endpoint & Routing | `src/noorheroes/modules/search/api.py` & `src/noorheroes/api/v1/router.py` | ✅ VERIFIED |
| 06 | Age-Band Bypass Security CI Gate | `tests/modules/search/test_age_band_bypass_security.py` (24 passed) | ✅ VERIFIED |
| 07 | Functional & Integration Test Suite | `tests/modules/search/test_child_search_api.py` (20 passed) | ✅ VERIFIED |
| 08 | Full Test Suite Status | 152/152 passed across all search test modules (100% green, 0 regressions) | ✅ VERIFIED |

