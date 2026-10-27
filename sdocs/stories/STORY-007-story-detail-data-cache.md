---
id: STORY-007
epic: EPIC-002
kind: feature
title: Implement Story Detail API client, cache layer, and repository extension
status: done
priority: P0
prd: ../../PRD_Documents/Child App (1-12)/Feature_A3_Stories_Module.md
depends_on: [STORY-006]
produces: [api.story-detail, domain.story-detail]
consumes: [data.story-cache]
created: 2026-09-29
---

## User Story
As a child learner, I want story detail with server-computed episode unlock states retrieved and cached locally, so that I can view episode prerequisites both online and offline.

## Acceptance Criteria
- [x] AC1: Given network connectivity, `StoryCatalogApiService.getStoryDetail(id)` retrieves `StoryDetailResponseDto` from `GET /v1/content/{id}`.
- [x] AC2: Given cached detail, `StoryCatalogCache` caches and returns detail with TTL validation.
- [x] AC3: Given network failure, `StoryCatalogRepository.getStoryDetail(id)` falls back to cached metadata with `isOffline = true`.
- [x] AC4: Given HTTP 410 response, `StoryCatalogRepository` maps to `AppError.ContentWithdrawn`.

## Technical Notes
- Files in scope: `core/core-network`, `core/core-common`, `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/data/*`.
