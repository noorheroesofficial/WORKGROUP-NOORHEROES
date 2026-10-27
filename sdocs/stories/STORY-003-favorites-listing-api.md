---
id: STORY-003
epic: EPIC-014
kind: feature
title: Child Favorites Listing & Type-Filtered Retrieval API Endpoint
status: completed
priority: P0
prd: ../../PRD_Documents/Child App Supporting (13-18)/Feature_B14_Favorites.md
depends_on: [STORY-001]
produces: [api.favorites-listing]
consumes: [type.favorite-models]
created: 2026-09-29
---

## User Story

As a child learner, I want to retrieve my saved favorites (stories, surahs, and duas) with optional type filtering and pagination, so that I can browse my favorite content easily and resume playback/learning without ever seeing a sibling's bookmarks.

## Acceptance Criteria

- [x] AC1: Given an authenticated child session, when `GET /v1/children/{id}/favorites` is requested with `{id}` matching the authenticated child's ID, the server returns `200 OK` with a standard `PageResult` envelope (`items`, `nextCursor`, `hasMore`).
- [x] AC2 (CI-Blocking Signature): When `{id}` in the path does NOT match the authenticated child's ID, the request is strictly rejected with HTTP `403 FORBIDDEN` (`Cannot access favorites of another child`), never silently rescoped.
- [x] AC3: When unauthenticated, returns `401 UNAUTHENTICATED`; when called with parent-mode token, returns `403 FORBIDDEN`.
- [x] AC4: When query parameter `type` is supplied (`story`, `surah`, `dua`), returns only favorites matching that content type; case-insensitive and whitespace-tolerant.
- [x] AC5: When an unsupported `type` parameter is supplied (e.g. `podcast`, `video`, `quiz`), returns `422 VALIDATION_ERROR` in the Universal Error Envelope.
- [x] AC6: When an episode was restructured into a canonical ID, the listing returns the canonical `content_id` and updated title transparently while preserving `original_episode_id`.
- [x] AC7: When content has been withdrawn from circulation, it remains in the favorites listing with `available: false` / `is_available: false` (underlying row is never deleted).
- [x] AC8: When cursor and limit are provided, keyset cursor pagination is performed with no duplicates across pages; limit is clamped to [1, 50].
- [x] AC9: Responses are cached in Redis for 60 seconds and invalidated on toggle mutations.

## Technical Notes

- Files in scope:
  - `src/noorheroes/modules/content/api.py`
  - `src/noorheroes/modules/content/favorite_service.py`
  - `src/noorheroes/modules/content/favorite_repository.py`
  - `src/noorheroes/modules/content/favorite_schemas.py`
  - `src/noorheroes/modules/content/deps.py`
  - `tests/modules/content/test_favorites_listing_api.py`
- Architecture refs: `sdocs/architecture-ref.md`, `Development_Blueprints/B14_Favorites/Backend/02-child-favorites-listing-api.md`.
- Strict child scoping: Verified via path parameter comparison with `session.child_id`.

## Test Approach

- Unit & Integration:
  - `tests/modules/content/test_favorites_listing_api.py`: 40 test cases covering CI-blocking sibling 403 test, own child session 200, type filtering (story, surah, dua, all), case normalization, invalid type 422, keyset pagination, empty states, withdrawn content resolution, cascading parent series withdrawal, canonical series withdrawal, withdrawn dua resolution, orphan/purged content degradation (zero 500s), dynamic surah access checkers, series restructuring canonical resolution, Redis short-TTL caching and invalidation, malformed cursor rejection, mutating HTTP 405 guards, and multi-child database isolation.
  - Full content module test suite: 94/94 favorites suite tests passing (100% green, 0 regressions across listing, toggle, and legacy routes).

