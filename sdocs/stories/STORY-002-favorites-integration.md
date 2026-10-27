---
id: STORY-002
epic: EPIC-014
kind: integration
title: Child Favorites Management — integration
status: completed
priority: P0
prd: ../../PRD_Documents/Child App Supporting (13-18)/Feature_B14_Favorites.md
depends_on: [STORY-001, STORY-003]
produces: []
consumes: [api.favorite-toggle, api.favorites-listing, type.favorite-models]
created: 2026-09-29
---

## User Story

As an operator of the NoorHeroes platform, I want the favorite toggle API and favorites listing API to compose end-to-end with authentication, database persistence, and accessibility gating, so that the favorites feature delivers safe, per-child isolated bookmarking.

## Acceptance Criteria

- [x] AC1: An end-to-end scenario exercising `POST /v1/favorites` add → duplicate add → remove → verify removal operates consistently against database constraints.
- [x] AC2: Cross-story seam verification: `api.favorite-toggle` request/response types validate against `type.favorite-models` persistence invariants.
- [x] AC3: Concurrency verification: 10 concurrent add requests on the same child and content produce exactly one database record.
- [x] AC4: Cache invalidation verification: mutating favorite actions reliably trigger Redis cache purge for the child's favorites prefix (`favorites:{child_id}:*`).

## Technical Notes

- Files in scope: test files only (`tests/modules/content/test_favorite_toggle_api.py`, `tests/modules/content/test_favorite_api.py`). No production code changes.
- Architecture refs: `sdocs/architecture-ref.md`.
- All `consumes:` contracts are exercised through their real implementations.

## Test Approach

- Integration: end-to-end integration tests in `tests/modules/content/test_favorite_toggle_api.py` and `test_favorite_api.py`.
- No new unit tests — those belong to feature stories.

## Out of Scope

- New production code changes.
- Stories from other epics.
