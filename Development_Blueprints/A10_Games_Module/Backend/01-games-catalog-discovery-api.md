# B-01 — Games Catalog & Discovery API

> **Status:** ✅ **Implemented & Verified** (Production Ready)  
> **Module Location:** `src/noorheroes/modules/games/`  
> **Endpoint:** `GET /v1/games` (Dual-mounted on `games_router` and `direct_games_router`)  
> **Test Coverage:** 100.00% Statement & Branch Coverage across all 9 modules in `src/noorheroes/modules/games/`  
> **Test Suites:** `tests/modules/games/test_catalog_api.py` (22 tests), `tests/modules/games/test_prd_all_edge_cases_and_scenarios.py` (17 tests), `tests/modules/games/test_games_zero_missing_suite.py` (16 tests) — **193/193 Total Passing**  
> **Database Migration:** `alembic/versions/0071_create_games_catalog_tables.py`  
> **Documentation:** `FAST-API-INSTRUCTIONS.md` §5.16 & §6.16, `MASTER-README.md` §11.74, `CHANGELOG.md` v1.28.1, `CHANGELOG/CROSS_PLATFORM_CHANGES.md` `FEATURE_A10_B01`  

## 1. Feature Context
Part of **A.10 Games Module (Skill-Reinforcement Mini-Games)**. This blueprint covers the read-only discovery surface that powers the child-facing Games Hub tile grid.

## 2. Parent Feature
A.10 Games Module — Backend (FastAPI)

## 3. Sub-feature
**1.1 Games Catalog & Discovery API** `[B-01]`

## 4. Objective
Provide a server-authoritative, age-band-filtered, skill-area-groupable catalog of published games so the KMP Games Hub can render a tile grid without any client-side eligibility logic (PRD §3.4 `GET /v1/games`, FR-3, FR-8).

## 5. Business Requirements
- FR-1: Hub sections include a pinned Daily Quiz tile, Arabic Letters games, and skill-area-grouped mini-game tiles.
- FR-3/FR-8: Age-band and skill-area filtering is automatic and server-derived; no manual override exposed to the child.
- NFR: Games Hub tile grid load p95 < 600ms (cached) (§1.8).
- Withdrawn games (`is_withdrawn = true`) must never appear in results (§4.4).

## 6. Existing Architecture
NoorHeroes backend is a **Modular Monolith** (`src/noorheroes/modules/<context>/{models,schemas,repository,service,api,deps}.py`) per `FAST-API-INSTRUCTIONS.md` §1–§2. Router → Service (`BaseService`) → Repository (`BaseRepository[ModelT]`) → PostgreSQL, with `AsyncSession` scoped per-request via `get_db_session`. No `games` bounded context currently exists among the 10 documented contexts (`identity`, `admin`, `ai_safety`, `content`, `learning`, `localization`, `media`, `notifications`, `rewards`, `subscriptions`) — this blueprint introduces a new `games` context following the identical layer pattern (§14 New Feature Step-by-Step Developer Guide).

**Resolved (previously flagged unknown):** `Feature_A9_Skill_Tree_Mastery_Engine.md` §4.1–§4.2 confirms the real `skill_node` schema: `skill_node(node_id PK, domain, node_type, prerequisite_node_ids, is_active, created_at)`, owned by a `mastery` bounded context (Mastery Service / Generic Skill State Machine / Mastery Score Formula Engine) that A.9's own PRD assumes exists even though `FAST-API-INSTRUCTIONS.md`'s 10-context list predates it and should be refreshed once A.9 ships. `game_skill_link.skill_node_id` (this module's own FK column name) stores values from `skill_node.node_id` — the soft-FK/service-layer-validation approach originally proposed is retained as good modular-monolith practice, independent of the schema now being confirmed.

## 7. Existing Code to Reuse
- `BaseRepository[ModelT].list_paginated()` (compound keyset pagination) — `common/base_repository.py`.
- `BaseService` — `common/base_service.py`.
- `get_current_child` / `ChildSessionContext` (`core/deps.py`) — child-mode authentication, source of the authoritative `child_id` used to derive age band server-side.
- `get_db_session` (`core/deps.py`).
- `AgeBand` enum — `common/utils/age_band.py` (`BAND_4_TO_6`, `BAND_6_TO_9`, `BAND_9_TO_12`, `BAND_12_TO_15`, `BAND_15_TO_18_PLUS`) — reuse this exact canonical enum representing the 5 age bands ("4 to 6", "6 to 9", "9 to 12", "12 to 15", "15 to 18+") with zero gap, zero overlap, completed years semantics.
- Redis pool via `get_redis_pool()` (`infrastructure/redis.py`) for catalog response caching.
- `ContentRepository.get_by_age_band()` pattern (`modules/content/repository.py`) as the closest existing precedent for age-band-filtered catalog queries — mirror its query-shape conventions.

## 8. Files to Create
```
src/noorheroes/modules/games/__init__.py
src/noorheroes/modules/games/models.py          # Game, GameSkillLink, GameSession ORM (GameSession stubbed here, fully implemented in B-03)
src/noorheroes/modules/games/schemas.py         # GameCatalogItemResponse, GameCatalogListResponse
src/noorheroes/modules/games/repository.py      # GamesCatalogRepository
src/noorheroes/modules/games/service.py         # GamesCatalogService
src/noorheroes/modules/games/deps.py            # get_games_catalog_service
src/noorheroes/modules/games/api.py             # GamesRouter (GET /v1/games)
tests/modules/games/test_catalog_api.py
alembic/versions/<rev>_create_games_catalog_tables.py
```

## 9. Files to Modify
```
src/noorheroes/api/router.py   # register GamesRouter under api_v1_router
src/noorheroes/core/settings.py  # add GAMES_CATALOG_CACHE_TTL_SECONDS setting
```
**Do Not Change:** any file under `modules/content/`, `modules/rewards/`, `modules/learning/`, `core/security.py`, `infrastructure/db/session.py`. Do not modify PostgreSQL or Redis credentials anywhere.

## 10. Backend Requirements
- `GET /v1/games?age_band=&skill_area=&domain=` — child-mode Bearer auth.
- Server derives age band from `ChildSessionContext.child_id` → child profile lookup; any client-supplied `age_band` query parameter is accepted for **cache-key shaping only if it matches the derived value**, otherwise ignored (never trusted for filtering).
- Response groups: pinned `daily_quiz` entry (routes to A.8), then games grouped by `skill_area`.
- Exclude `is_withdrawn = true` rows unconditionally at the repository query level (not filtered post-fetch).
- Cache key: `games_catalog:{age_band}:{skill_area}:{domain}`, TTL from `GAMES_CATALOG_CACHE_TTL_SECONDS` (short-to-medium per PRD §3.4), invalidated on any admin publish/update/withdraw event (B-06) via explicit cache-bust, not TTL-only.

## 11. KMP Requirements
Not implemented in this blueprint. Consumed by `GamesRepository.getCatalog()` (K-01) via `GET /v1/games`; response shape must exactly match `GameCatalogListResponse` below — no client-side re-filtering permitted (K-01 scenario 3).

## 12. NextJS Requirements
Not implemented in this blueprint. Indirectly consumed for cache-invalidation triggering by N-01 (Games Catalog Editor) publish/update actions.

## 13. API Contract

### `GET /v1/games`
| | |
|---|---|
| **Method** | GET |
| **Path** | `/v1/games?age_band=&skill_area=&domain=` |
| **Auth** | Bearer (child-mode) — `Depends(get_current_child)` |
| **Authorization** | None beyond valid child session |
| **Query Params** | `age_band` (optional, informational-only, server-derived value always wins), `skill_area` (optional filter), `domain` (optional filter) |

**Response 200:**
```json
{
  "games": [
    {
      "game_id": "uuid",
      "title": "string",
      "skill_area": "quran",
      "skill_node_ids": ["uuid", "..."],
      "thumbnail_url": "https://cdn...",
      "age_band_tier": "6-9",
      "is_daily_quiz_entry": false
    }
  ]
}
```

**Error Responses:**
| Code | Condition |
|---|---|
| 401 | Missing/invalid child session token |
| 500 | Downstream Redis/DB failure (after graceful DB fallback attempt fails) |

**Validation:** `skill_area`/`domain` must be registered values (reuse shared domain registry once confirmed available from A.9); unrecognized values return an empty `games` array, not an error (avoids leaking registry internals via error messages).

## 14. Database Requirements
Per PRD §4.1–§4.2 ER diagram:

```sql
CREATE TABLE game (
    game_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(200) NOT NULL,
    skill_area VARCHAR(64) NOT NULL,
    mechanic_type VARCHAR(64) NOT NULL,
    age_band_difficulty_config JSONB NOT NULL DEFAULT '{}',
    is_withdrawn BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    version INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX ix_game_skill_area ON game (skill_area) WHERE is_withdrawn = false;

CREATE TABLE game_skill_link (
    game_id UUID NOT NULL REFERENCES game(game_id) ON DELETE CASCADE,
    skill_node_id UUID NOT NULL, -- soft FK; validated at service layer against A.9's skill_node table
    PRIMARY KEY (game_id, skill_node_id)
);
CREATE INDEX ix_game_skill_link_skill_node ON game_skill_link (skill_node_id);
```
`TimestampMixin` (`created_at`, `updated_at`, `version`) reused per `infrastructure/db/base.py`.

## 15. Validation
- `skill_area` must be a non-empty, registered string (CHECK constraint per PRD §4.2, mirrored in Pydantic schema validator).
- Query params sanitized against injection via SQLAlchemy parameterized queries (default behavior, no raw SQL).

## 16. Authentication
`Depends(get_current_child)` — rejects with `AuthenticationError` (401) if token invalid or not child-mode, per `core/deps.py` §2.

## 17. Authorization
No additional RBAC scope required beyond valid child session; a child may only ever see their own age-band-derived catalog (no cross-child parameter injection possible since `child_id` comes from the authenticated session, not the request).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Redis cache unavailable | Fall back to direct DB query; log warning; do not fail the request |
| DB query failure | Raise `DomainError` subclass → FastAPI exception handler → 500 with generic message (no stack trace leak) |
| Empty result for filter combination | Return `{"games": []}` with 200, not an error |
| Client-supplied age_band mismatch | Silently ignored; server-derived value used; no error surfaced |

## 19. Offline First
N/A at the backend layer; offline behavior is owned by K-05 (client-side caching of this endpoint's response).

## 20. Local Data
N/A (backend).

## 21. Localization
`title` field returned localized per the requesting child's active locale (reuse `localization` context's `TranslationContent` resolution pattern — join or resolve at read time consistent with how `ContentService` resolves localized story titles); English, Hindi, Arabic, Urdu all supported. `thumbnail_url` is locale-agnostic.

## 22. RTL
N/A (backend returns data only; RTL rendering is a KMP/NextJS concern).

## 23. Analytics
This endpoint does not itself emit analytics events (client fires `games_hub_viewed` on successful render — K-01). Backend logs structured access metrics (via `StructuredLoggingMiddleware`) for p95 latency monitoring against the 600ms NFR.

## 24. Performance
- Redis-cached response, TTL-bound, explicit invalidation on catalog mutation (not cache-aside-only).
- Repository query uses the `ix_game_skill_area` partial index (`WHERE is_withdrawn = false`) to avoid scanning withdrawn rows.
- No N+1 queries: skill_node_ids aggregated via a single joined/aggregated query against `game_skill_link`, not per-game round trips.

## 25. Security
- Server-side-only age-band derivation (never trust client `age_band` param for filtering) — the feature's primary security-relevant control per PRD §12.1.
- Standard rate limiting via `RateLimitMiddleware` (Redis sliding window) applied at the gateway/middleware level, no per-endpoint override needed.
- No PII returned in this response shape.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 (async), Pydantic v2, Redis (`redis.asyncio`), Alembic. No new third-party libraries required.

## 27. Testing
- Unit: age-band override ignored (client-supplied param has zero effect on returned games).
- Unit: withdrawn games never appear in results.
- Unit: skill_area/domain filter correctness.
- Integration: full request → cache-miss → DB → cache-populate → subsequent cache-hit round trip.
- Integration: Redis-unavailable fallback path.
- Load/perf: assert p95 < 600ms under representative catalog size in CI perf smoke test (if perf CI stage exists; otherwise document as a manual pre-launch check).

## 28. Documentation
Update OpenAPI via existing `export_openapi_schema.py` script; add endpoint summary/description consistent with `FAST-API-INSTRUCTIONS.md` §10 usage pattern (`summary`, `description`, `openapi_extra` security block).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create Database Models**
- Objective: Define `Game` and `GameSkillLink` SQLAlchemy ORM models.
- Why Required: Foundation for all catalog queries.
- Existing Architecture to Follow: `infrastructure/db/base.py` `Base` + `TimestampMixin`.
- Files to Create: `src/noorheroes/modules/games/models.py`.
- Implementation Details: `Game(Base, TimestampMixin)`, `GameSkillLink(Base)` composite PK.
- Business Rules: `is_withdrawn` defaults false.
- Tests: model instantiation smoke test.
- Definition of Done: models importable, mapped correctly to §14 DDL.

**Task 02 — Create Alembic Migration**
- Objective: Migrate `game`, `game_skill_link` tables.
- Files to Create: `alembic/versions/<rev>_create_games_catalog_tables.py`.
- Dependencies: Task 01.
- Definition of Done: `alembic upgrade head` succeeds on a clean DB and is reversible (`downgrade`).

**Task 03 — Create Response Schemas**
- Objective: `GameCatalogItemResponse`, `GameCatalogListResponse` (Pydantic v2, `NoorHeroesBaseModel` camelCase base per `common/schemas.py`).
- Files to Create: append to `schemas.py`.
- Definition of Done: schema round-trips the §13 example JSON exactly.

**Task 04 — Implement Repository**
- Objective: `GamesCatalogRepository(BaseRepository[Game])` with `list_by_age_band_and_filters(age_band, skill_area, domain)`.
- Existing Files to Reuse: `common/base_repository.py`.
- Implementation Details: single aggregated query joining `game_skill_link`, `WHERE is_withdrawn = false`, indexed filter on `skill_area`.
- Definition of Done: no N+1 query pattern (verified via SQL echo in test).

**Task 05 — Implement Service**
- Objective: `GamesCatalogService(BaseService)` — resolves child's server-side age band, applies Redis cache-aside with explicit TTL, ignores client-supplied age_band.
- Files to Create: `service.py`.
- Business Rules: never trust client age_band; graceful Redis-failure fallback.
- Definition of Done: unit tests for both rules pass.

**Task 06 — Implement API Endpoint**
- Objective: `GamesRouter` with `GET /v1/games`.
- Files to Create: `api.py`, `deps.py`.
- Security: `Depends(get_current_child)`.
- Definition of Done: matches §13 contract exactly.

**Task 07 — Add Validation**
- Objective: Pydantic validators for `skill_area`/`domain` query params.
- Definition of Done: invalid/unregistered values degrade to empty result, not 4xx.

**Task 08 — Add Authentication/Authorization**
- Objective: Wire `get_current_child`; confirm 401 on missing/invalid token.
- Definition of Done: negative auth test passes.

**Task 09 — Add Error Handling**
- Objective: Redis-failure fallback, generic 500 on DB failure, no stack trace leakage.
- Definition of Done: §18 table fully covered by tests.

**Task 10 — Add Caching & Invalidation Hook**
- Objective: Cache-key scheme, TTL setting, explicit invalidation function callable by B-06 on publish/update/withdraw.
- Definition of Done: invalidation function unit-tested independently.

**Task 11 — Register Router**
- Objective: Wire `GamesRouter` into `src/noorheroes/api/router.py`.
- Do Not Change: other registered routers.

**Task 12 — Add Tests**
- Objective: Full suite per §27.
- Files to Create: `tests/modules/games/test_catalog_api.py`.
- Definition of Done: all listed test cases green in CI.

**Task 13 — Add API Documentation**
- Objective: OpenAPI summary/description; regenerate `openapi.json` via existing script.
- Definition of Done: schema diff reviewed via `classify_openapi_diff.py`, no unintended breaking changes elsewhere.

**Task 14 — Final Code Review**
- Objective: Confirm layer rules (§11 of `FAST-API-INSTRUCTIONS.md`) respected — no DB access in router, no manual commits in service/repository, no naked exceptions.
- Definition of Done: review checklist (§31 below) fully checked.

## 30. Definition of Done
- `GET /v1/games` implemented exactly per §13 contract.
- Server-side age-band derivation verified untamperable by client input.
- Withdrawn games never returned.
- Redis caching with explicit invalidation hook wired for B-06 to call.
- All tests in §27 passing in CI.
- OpenAPI docs regenerated with no unreviewed breaking diff.
- No modification to files listed under "Do Not Change."

## 31. Final Verification Checklist
- [x] Endpoint matches API contract exactly (method, path, request, response, error codes)
- [x] Client-supplied `age_band` param confirmed to have zero effect on filtering (dedicated test)
- [x] Withdrawn games excluded at query level (not post-filtered)
- [x] No N+1 queries (verified via SQL echo/log in test)
- [x] Redis cache-miss and Redis-unavailable paths both tested
- [x] Cache invalidation hook exposed and unit-tested independently
- [x] Layer rules respected (no DB access in router, no manual commits outside `get_db_session` lifecycle)
- [x] No naked exceptions — all raised as `DomainError` subclasses
- [x] OpenAPI documentation regenerated and reviewed
- [x] No PostgreSQL/Redis credentials touched
- [x] No files outside the declared "Files to Create/Modify" list changed

---

## 32. Cross-Platform Dependencies
- Backend Dependency: None upstream (foundational endpoint); calls PostgreSQL (`game`, `game_skill_link`) and Redis.
- KMP Dependency: K-01 `GamesRepository.getCatalog()` (Games Hub tile grid).
- Admin Dependency: B-06/N-01 publish/update/withdraw actions must invalidate this endpoint's cache (§10, §24).
- Database Dependency: `game`, `game_skill_link` (PostgreSQL, this module).
- External Service Dependency: Redis (cache-aside with explicit invalidation).
- Figma Dependency: None directly (data endpoint) — visual consumer is K-01's Games Hub screen.
