---
id: STORY-006
epic: EPIC-002
kind: feature
title: Add StoryDetailRoute and deep link resolution
status: done
priority: P0
prd: ../../PRD_Documents/Child App (1-12)/Feature_A3_Stories_Module.md
depends_on: []
produces: []
consumes: []
created: 2026-09-29
---

## User Story
As a child learner, I want to navigate to the Story Detail screen from library rails or via deep links (`noorheroes://stories/{storyId}`), so that I can see episodes and story details.

## Acceptance Criteria
- [x] AC1: Given the navigation system, when resolving `StoryDetailRoute(storyId)`, then it routes to the destination with `analyticsName = "story_detail"`.
- [x] AC2: Deep link pattern `noorheroes://stories/{storyId}` maps cleanly to `StoryDetailRoute`.

## Technical Notes
- Files in scope: `core/core-navigation/src/commonMain/kotlin/com/noorheroes/core/navigation/Route.kt`.
