---
id: STORY-002
epic: EPIC-001
kind: feature
title: Implement StoryCatalogApi, DTOs, and StoryCatalogCache
status: done
priority: P0
prd: ../../PRD_Documents/Child App (1-12)/Feature_A3_Stories_Module.md
depends_on: [STORY-001]
produces: [api.content-catalog, data.story-cache]
consumes: []
created: 2026-09-29
---

## User Story
As a child learner, I want story catalog metadata to be retrieved from the backend API and cached locally, so that I can browse stories both online and offline.

## Acceptance Criteria
- [x] AC1: Given network connectivity, when querying `StoryCatalogApi`, then `GET /v1/content?type=story` returns a parsed `StoryCatalogPaginatedDto`.
- [x] AC2: Given cached responses, when saving and retrieving from `StoryCatalogCache`, then round-trip serialization succeeds and expired items (> 10 min TTL) are evicted.

## Technical Notes
- Files in scope: `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/data/*`.
- Contracts: implements `api.content-catalog` and `data.story-cache`.

## Test Approach
- Unit: API client serialization test, cache store round-trip test.

## Out of Scope
- ViewModel and UI rendering (covered in STORY-003, STORY-004).
