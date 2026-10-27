---
id: STORY-008
epic: EPIC-002
kind: feature
title: Implement GetStoryDetailUseCase and StoryDetailViewModel with real-time onResume refresh
status: done
priority: P0
prd: ../../PRD_Documents/Child App (1-12)/Feature_A3_Stories_Module.md
depends_on: [STORY-007]
produces: []
consumes: [domain.story-detail]
created: 2026-09-29
---

## User Story
As a child learner, I want episode unlock states to refresh in real time when returning to Story Detail after completing an episode, without restarting the app or reloading the entire screen.

## Acceptance Criteria
- [x] AC1: Given screen entry, `StoryDetailViewModel` loads detail and emits `story_detail_viewed` analytics.
- [x] AC2: Given returning from playback (`OnResume`), `StoryDetailViewModel` performs a lightweight re-fetch that updates episode unlock states without full screen recreation.
- [x] AC3: Given locked episode click, fires `episode_lock_viewed`, `episode_unlock_condition_tapped`, and shows unlock condition tooltip.
- [x] AC4: Given tier-gated episode click, fires `paywall_card_shown` and displays parent-gated paywall modal.
- [x] AC5: Given withdrawn story (410), sets `isWithdrawn = true` and renders friendly unavailable state.

## Technical Notes
- Files in scope: `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/domain/usecase/*`, `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/presentation/detail/*`.
