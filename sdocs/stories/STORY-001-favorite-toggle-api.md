---
id: STORY-001
epic: EPIC-014
kind: feature
title: Favorite Toggle API Endpoint
status: completed
priority: P0
prd: ../../PRD_Documents/Child App Supporting (13-18)/Feature_B14_Favorites.md
depends_on: []
produces: [api.favorite-toggle, type.favorite-models]
consumes: []
created: 2026-09-29
---

## User Story

As a child learner, I want to tap a heart/save icon on any story, surah, or dua to toggle saving it to my personal favorites list, so that I can easily revisit content I love without seeing my siblings' bookmarks.

## Acceptance Criteria

- [x] AC1: Given an authenticated child session, when `POST /v1/favorites` is invoked with `favorited: true`, `contentId`, and `contentType`, then the item is saved to `favorite` and returns `200` with `favorited: true`.
- [x] AC2: Given an authenticated child session, when `POST /v1/favorites` is invoked with `favorited: false`, then the favorite row is removed and returns `200` with `favorited: false`.
- [x] AC3: Given rapid duplicate requests with the same `clientRequestId`, then the operation behaves idempotently and never produces duplicate rows or errors.
- [x] AC4: Given content that is withdrawn or inaccessible to the child, when attempting to favorite (`favorited: true`), then the request is rejected with `403 FORBIDDEN` and no favorite row is written.
- [x] AC5: Given content that was previously favorited and is now inaccessible, when removing (`favorited: false`), then removal succeeds without accessibility check.
- [x] AC6: Given an unauthenticated or parent-session request, then the endpoint rejects with `401` or `403` respectively.
- [x] AC7: Given an unsupported `contentType` (not in story, surah, dua) or empty `contentId`, then the endpoint returns `422 VALIDATION_ERROR`.

## Technical Notes

- Files in scope:
  - `src/noorheroes/modules/content/api.py`
  - `src/noorheroes/modules/content/favorite_service.py`
  - `src/noorheroes/modules/content/favorite_repository.py`
  - `src/noorheroes/modules/content/favorite_schemas.py`
  - `tests/modules/content/test_favorite_toggle_api.py`
- Architecture refs: `sdocs/architecture-ref.md`, `Development_Blueprints/B14_Favorites/Backend/01-favorite-toggle-api.md`.
- Strict child scoping: Implicit from `Depends(get_current_child_session)`.

## Test Approach

- Unit & Integration:
  - `tests/modules/content/test_favorite_toggle_api.py`: 29 test cases covering positive add/remove, idempotency, accessibility gating (403), un-gated removal, schema validation, parameter pollution (extra='forbid'), outbox state transition deduplication, SQLite in-memory persistence, concurrency protection, and auth boundaries.
  - `tests/modules/content/test_favorite_api.py`: 25 test cases for route parity and backward compatibility.
  - `tests/modules/content/test_favorite_service.py`: 17 unit test cases for service logic.


## Out of Scope

- Paginated listing `GET /v1/children/{id}/favorites` (STORY-003 / Blueprint B-02).
- Offline downloads management (B.15).
