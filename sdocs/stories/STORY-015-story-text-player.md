---
id: STORY-015
epic: EPIC-003
kind: feature
title: Implement StoryTextPlayer Composable for Text-Format Stories
status: ready
priority: P1
prd: ../../PRD_Documents/Child App (1-12)/Feature_A3_Stories_Module.md
depends_on: [STORY-013]
produces: []
consumes: [domain.story-player]
created: 2026-09-29
---

## User Story
As a child learner, I want to read text-format stories with clear typography scaling, auto-scroll/paging, and audio narration synchronization, reporting into the same player state machine.

## Acceptance Criteria
- [ ] AC1: Given `StoryTextPlayer.kt`, renders text-format story content with dynamic typography scaling adhering to accessibility guidelines.
- [ ] AC2: Given text story reading progress, updates current position and reports into the shared `PlayerState` machine.
- [ ] AC3: Given bilingual Arabic/English content, renders bidirectional RTL/LTR text correctly with proper line height and Quranic/Arabic font styling.
- [ ] AC4: Given Design System rules (`rule.md`), contains 0 raw colors, 0 raw dp/sp, 0 raw shapes, and stays strictly under 500 lines.

## Technical Notes
- Files in scope:
  - `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/ui/player/StoryTextPlayer.kt`
- Architecture refs: `sdocs/architecture-ref.md` §6.1, §6.2, §6.4.

## Test Approach
- Compose UI test: Verify text renders with proper font scaling and line spacing.
- Unit: Verify progress tracking updates `PlayerState.Playing`.

## Out of Scope
- Video/audio player layout (covered in STORY-016).
- Choice points overlay (covered in K-04).
