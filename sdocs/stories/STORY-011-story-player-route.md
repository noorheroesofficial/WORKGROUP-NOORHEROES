---
id: STORY-011
epic: EPIC-003
kind: feature
title: Add StoryPlayerRoute as a Distinct Full-Screen Destination
status: ready
priority: P0
prd: ../../PRD_Documents/Child App (1-12)/Feature_A3_Stories_Module.md
depends_on: []
produces: []
consumes: []
created: 2026-09-29
---

## User Story
As a child learner, I want to tap an episode and enter an immersive full-screen story player destination where system bars are automatically hidden and restored on exit.

## Acceptance Criteria
- [ ] AC1: Given `Route.kt`, `StoryPlayerRoute(episodeId: String, seriesId: String? = null)` is defined as a serializable `@Serializable` destination in `core-navigation`.
- [ ] AC2: Given deep link `noorheroes://stories/{episodeId}`, it routes to `StoryPlayerRoute`.
- [ ] AC3: Given the navigation destination, system UI (status and navigation bars) is hidden on screen entry and restored cleanly on navigation exit.
- [ ] AC4: Given `analyticsName`, the route reports `"story_player"`.

## Technical Notes
- Files in scope: `core/core-navigation/src/commonMain/kotlin/com/noorheroes/core/navigation/Route.kt`.
- Architecture refs: `sdocs/architecture-ref.md` §6.1, §6.3.
- Invariants: Pure Kotlin Multiplatform navigation route with zero Compose UI imports.

## Test Approach
- Unit: Verify `Route.StoryPlayerRoute` serialization and route parameter extraction.
- Integration: Deep link resolution test from string URI to destination.

## Out of Scope
- Playback engine state management (covered in STORY-013).
- Media rendering (covered in STORY-014 and STORY-016).
