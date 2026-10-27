---
id: STORY-014
epic: EPIC-003
kind: feature
title: Wire KMPPlayerController, Safe-Stop on Unavailable, and PlaybackSessionManager
status: ready
priority: P0
prd: ../../PRD_Documents/Child App (1-12)/Feature_A3_Stories_Module.md
depends_on: [STORY-013]
produces: []
consumes: [domain.story-player, repo.story-manifest]
created: 2026-09-29
---

## User Story
As a child learner, I want smooth video/audio playback powered by `library:kmpplayer`, resuming from where I left off, with safe and comforting recovery if media becomes unavailable.

## Acceptance Criteria
- [ ] AC1: Given `StoryPlayerViewModel`, binds to `KMPPlayerController` / `AudioPlayerController` via `prepare()`, `play()`, `pause()`, and `seekTo()`, driven strictly by `PlayerState` transitions.
- [ ] AC2: Given `PlaybackSessionManager`, retrieves previous resume position on `prepare()` and saves updated progress position on session exit.
- [ ] AC3: Given a fatal media error or withdrawn content, immediately safe-stops to `PlayerState.Unavailable(reason, fallbackRecommendation)` showing a child-friendly message and alternative story recommendation.
- [ ] AC4: Given the safe-stop error view, asserts via blocklist testing that zero raw technical text, exception names, error codes, or stack traces reach the child.
- [ ] AC5: Given the implementation, verifies zero direct calls to platform `androidx.media3` or `AVPlayer` APIs exist in the codebase.
- [ ] AC6: Given offline playback, prefers `KMPPlayerSource.Local` if content is downloaded locally, otherwise falls back to signed `Network` playback URL from manifest.

## Technical Notes
- Files in scope:
  - `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/presentation/player/StoryPlayerViewModel.kt`
  - `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/presentation/player/PlayerControllerBridge.kt`
- Dependencies: `implementation(project(":library:kmpplayer"))` in `feature:feature-stories`.
- Architecture refs: `sdocs/architecture-ref.md` §6.1, §6.2.

## Test Approach
- Unit: Safe-stop simulation asserting transition to `PlayerState.Unavailable`.
- Blocklist test: Regex asserting absence of "Exception", "0x", "Media3", "Error code" in child-facing error messages.
- Unit: Resume position retrieval and persistence verification.

## Out of Scope
- Text-format rendering (covered in STORY-015).
- Player screen Compose layout (covered in STORY-016).
