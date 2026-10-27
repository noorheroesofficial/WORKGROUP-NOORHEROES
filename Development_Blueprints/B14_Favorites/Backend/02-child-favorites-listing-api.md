# B-02 — Child Favorites Listing & Type-Filtered Retrieval API

## 1. Feature Context
Part of Feature B.14 Favorites. Serves the Favorites Tab grid (K-02) with the authenticated child's own favorites, type-filtered, with withdrawn-content resolution.

## 2. Parent Feature
B.14 Favorites (`PRD_Documents/Child App — Supporting (13-18)/Feature_B14_Favorites.md`)

## 3. Sub-feature
1.2 Child Favorites Listing & Type-Filtered Retrieval API — `B-02`

## 4. Objective
Return a strictly per-child-scoped, type-filterable, paginated favorites list, resolving each item's current availability without ever deleting the underlying favorite row.

## 5. Business Requirements
- FR-4: favorites are strictly per-child — this endpoint is the primary attack surface for cross-child leakage and must be defended accordingly.
- FR-7: withdrawn/archived content shows `available:false`, never a broken link.
- FR-8: type filtering (Stories/Surahs/Duas), same iconography pattern as B.13 Search.
- Edge Case 1: series restructuring — favorite resolves to the new canonical `content_id`.
- Edge Case 4: no hard cap on favorites count; grid must paginate gracefully.
- Source: PRD §1.7, §1.10, §3.4 `GET /v1/children/{id}/favorites?type=`.

## 6. Existing Architecture
Same `content` module as B-01. **Resolved — pagination convention confirmed:** the platform uses cursor-based keyset pagination, not offset/page-based. `FAST-API-INSTRUCTIONS.md` documents `PageResult[ModelT]` (`items`, `next_cursor`, `has_more`) as the standard paginated response envelope, produced via `BaseRepository.list_paginated(cursor: Optional[str], limit: int) -> PageResult[ModelT]`. This endpoint's paginated response and repository method must follow that exact convention rather than inventing an offset/page-number scheme. Redis caching via `get_redis_pool()`, short-TTL pattern already used for `TranslationCacheManager`.

## 7. Existing Code to Reuse
- `core/deps.py::get_current_child`
- `common/base_repository.py` (pagination helpers, if present)
- `infrastructure/redis.py::get_redis_pool`
- Content withdrawal/archive status fields already exposed by A.3 (`is_withdrawn`)/A.5/A.6 source-of-truth services

## 8. Files to Create
- `tests/modules/content/test_favorites_listing_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/content/api.py::ContentRouter` — add `GET /v1/children/{id}/favorites`
- `src/noorheroes/modules/content/service.py`/`favorite_service.py` — `FavoriteService.list_for_child(child_id, content_type, page)`
- `src/noorheroes/modules/content/repository.py`/`favorite_repository.py` — filtered/paginated query + availability join

## 10. Backend Requirements
- Path parameter `{id}` must equal the authenticated session's own `child_id`; mismatch → reject, never silently rescope.
- `type` query param optional; omitted = all types.
- Each returned item resolves `available` from the source content's current withdrawal/archive state at read time.
- Canonical `content_id` resolution for restructured/renumbered series (delegates to the content module's existing resolution rule, per A.3 Edge Case 11).
- Cache: short TTL keyed by `(child_id, type)`, invalidated on any toggle for that child (coordinate invalidation call from B-01's service).

## 11. KMP Requirements
Consumed by K-02 (grid rendering) and K-03 (repository). Contract only in this blueprint.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
**Required API:** Child Favorites Listing
**HTTP Method:** `GET`
**Endpoint:** `/v1/children/{id}/favorites?type=`
**Request:** path `id` (child id), optional query `type` (`story|surah|dua`), optional query `cursor` (string), optional query `limit` (int)
**Response 200:**
```json
{
  "items": [
    {
      "content_id": "string",
      "content_type": "story",
      "title": "string",
      "thumbnail_url": "string",
      "available": true
    }
  ],
  "next_cursor": "string|null",
  "has_more": true
}
```
**Authentication:** Bearer (child-mode)
**Authorization:** `id` must match the authenticated session's own `child_id` — strictly enforced server-side, not merely omitted client-side.
**Validation:** `type`, if present, must be in the content-type allowlist.
**Error Responses:** `401` unauthorized, `403` `id` does not match session child (attempted sibling/cross-family access), `422` invalid `type` value.

*Contract source: PRD §3.4 for the core fields (`content_id`, `content_type`, `title`, `thumbnail_url`, `available`); the PRD's illustrative response uses a bare `favorites` array without pagination envelope, but Edge Case 4 explicitly requires graceful pagination for large lists. **Resolved:** wrapped in the platform's standard `PageResult` envelope (`items`/`next_cursor`/`has_more`, confirmed in `FAST-API-INSTRUCTIONS.md`) rather than inventing a bespoke pagination shape — the field name changes from the PRD's illustrative `favorites` to the standard `items` to stay consistent with every other paginated endpoint in the codebase; flag this naming delta to the API contract owner for sign-off since it's a deliberate consistency correction, not a literal PRD transcription.*

## 14. Database Requirements
Reads from `favorite` table (canonical shape, post-B-03) joined against each content type's withdrawal/archive status. Index `(child_id, content_type, created_at DESC)` supports both filtered and unfiltered queries efficiently.

## 15. Validation
- `id` (path) format validation (UUID).
- `type` query param allowlist validation.

## 16. Authentication
Bearer JWT, child-mode, via `Depends(get_current_child)`.

## 17. Authorization
**Signature test for this endpoint:** reject any request where path `id` != session `child_id`, including same-family sibling ids. This must be a mandatory, CI-blocking test per the PRD's DevOps requirements.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Favorites grid fetch failure | Client renders cached last-known list with staleness indicator (K-02); this endpoint returns a standard `500` |
| Sibling/cross-family `id` attempt | `403`, logged as a potential isolation-violation signal |
| Empty list | `200` with `favorites: []`, not an error |
| Redis cache failure | Fallback to direct DB read, never a broken response |
| Withdrawn item | `available:false` in the response, row not omitted |

## 19. Offline First
Not backend-owned; client (K-03) caches this response locally for offline reads.

## 20. Local Data
N/A (backend blueprint).

## 21. Localization
`title` is returned as-is from the content's already-localized source record (localization owned by A.3/A.5/A.6, not duplicated here).

## 22. RTL
N/A at the API layer.

## 23. Analytics
Downstream: KMP fires `favorites_tab_viewed`/`favorites_type_filter_applied` on successful fetch (K-02 owns this).

## 24. Performance
Indexed query, short-TTL cache. Avoid N+1 when resolving `available` per item — batch the withdrawal-status lookup across all returned `content_id`s in one query per content type rather than per-item round trips.

## 25. Security
Strict per-child scoping is this endpoint's defining security property (OWASP Broken Access Control). No secrets touched. Do not modify PostgreSQL/Redis credentials.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 (async), Pydantic v2, Redis client (existing `infrastructure/redis.py`).

## 27. Testing
- Unit: type filtering, `available` resolution, canonical `content_id` resolution after restructuring.
- Integration: sibling-`id` access attempt → `403` (CI-blocking).
- Integration: withdraw a favorited item → list shows `available:false`, row still present.
- Integration: cache invalidation after a toggle reflects immediately in the next list call.

## 28. Documentation
Update OpenAPI schema; document the strict `id`-must-match-session rule prominently given its security criticality.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Confirm B-03 Migration Applied.** Same precondition as B-01.
**Task 02 — Define Response Schemas.** `FavoriteListItem`, `FavoriteListResponse`.
**Task 03 — Implement Repository Query.** `FavoriteRepository.list_paginated(child_id, content_type, cursor, limit) -> PageResult[FavoriteListItem]`, following the platform's standard cursor-based `BaseRepository.list_paginated` convention (not offset/page-based); joined with availability resolution, batch-resolve to avoid N+1.
**Task 04 — Implement Service Logic.** `FavoriteService.list_for_child(...)`.
**Task 05 — Add Router Endpoint.** `GET /v1/children/{id}/favorites`.
**Task 06 — Enforce Path/Session `id` Match.** Reject on mismatch with `403`.
**Task 07 — Add Redis Caching.** Short TTL, keyed `(child_id, type)`; wire invalidation call from B-01's toggle service.
**Task 08 — Add Error Handling.** Per §18.
**Task 09 — Write Tests.** Per §27, sibling-isolation test flagged as highest priority.
**Task 10 — Update OpenAPI Documentation.**
**Task 11 — Final Code Review.** Confirm cache invalidation is wired from B-01, not just this endpoint's own writes.

## 30. Definition of Done
Sibling-isolation test green (CI-blocking); withdrawn-content resolution test green; cache invalidation verified end-to-end with B-01; OpenAPI updated.

## 31. Final Verification Checklist
- [ ] Path `id` strictly validated against session `child_id`
- [ ] Type filter functioning correctly
- [ ] `available` resolved without deleting favorite rows
- [ ] Cache invalidated on toggle
- [ ] No N+1 queries on availability resolution
- [ ] PostgreSQL/Redis credentials untouched
