---
id: STORY-013
epic: EPIC-003
kind: feature
title: Implement PlayerState Machine, Throttled Heartbeat, and Scrub Clamp
status: ready
priority: P0
prd: ../../PRD_Documents/Child App (1-12)/Feature_A3_Stories_Module.md
depends_on: [STORY-012]
produces: [domain.story-player]
consumes: [api.story-manifest, api.playback-heartbeat, repo.story-manifest]
created: 2026-09-29
---

## User Story
As the story player orchestrator, I want a single authoritative `PlayerState` machine, session-scoped `client_event_id` UUID generation, throttled playback heartbeats, and scrub-ahead clamping, so that playback state is completely desync-free and progress is accurately tracked.

## Acceptance Criteria
- [ ] AC1: Given `StoryPlayerViewModel.init`, a cryptographically secure UUID v4 `client_event_id` is generated once and remains identical across all heartbeats and retries for this playback session.
- [ ] AC2: Given `PlayerState`, it is a sealed hierarchy (`Loading`, `Buffering`, `Playing`, `Paused`, `ChoiceActive`, `QuizActive`, `Unavailable`, `Completed`) driving all overlay visibility.
- [ ] AC3: Given playback progress updates, heartbeats are sent every 5–10s of actual playback time, and never fired while paused, buffering, or scrubbed.
- [ ] AC4: Given `scrub_restricted = true` in the manifest, seeking forward beyond `furthestReachedPositionMs + 5000ms` is clamped to that boundary.
- [ ] AC5: Given user scrub/seek gesture, sends a seek event with `eventType = "seek"` and new target position to the heartbeat repository.

## Technical Notes
- Files in scope:
  - `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/presentation/player/PlayerState.kt`
  - `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/presentation/player/PlayerEvent.kt`
  - `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/presentation/player/PlayerEffect.kt`
  - `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/presentation/player/StoryPlayerViewModel.kt`
- Architecture refs: `sdocs/architecture-ref.md` §6.1, §6.2.
- Invariants: `PlayerState` is the sole source of truth; no code path shows "Playing" controls while the state is `Buffering`.

## Test Approach
- Unit: Verify `client_event_id` stability across multiple operations and retries.
- Unit: Verify heartbeat throttling triggers at 5-10s intervals during playing and does not fire when paused.
- Unit: Verify scrub clamp restricts target seek position when `scrubRestricted = true`.

## Out of Scope
- Controller binding (covered in STORY-014).
- Text player rendering (covered in STORY-015).
