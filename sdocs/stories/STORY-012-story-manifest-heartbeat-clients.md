---
id: STORY-012
epic: EPIC-003
kind: feature
title: Implement Signed Manifest and Playback Heartbeat Data Layer
status: ready
priority: P0
prd: ../../PRD_Documents/Child App (1-12)/Feature_A3_Stories_Module.md
depends_on: [STORY-011]
produces: [api.story-manifest, api.playback-heartbeat, repo.story-manifest]
consumes: []
created: 2026-09-29
---

## User Story
As the story player client, I want to fetch short-TTL signed streaming manifests (B-07) and transmit progress heartbeats (B-03) through resilient repositories, so that media playback streams securely and progress syncs to the server.

## Acceptance Criteria
- [ ] AC1: Given `ManifestRepository.getManifest(contentId)`, calls `GET /v1/content/{id}/manifest` with child auth token and returns `StoryManifest` DTO/domain model.
- [ ] AC2: Given HTTP 410 response on manifest fetch, maps cleanly to `AppError.ContentWithdrawn` enabling safe-stop.
- [ ] AC3: Given `PlaybackHeartbeatRepository.sendHeartbeat(...)`, issues `POST /v1/playback/{content_id}` with `eventType`, `positionSeconds`, and `clientEventId`.
- [ ] AC4: Given network timeout or server error on heartbeat, returns non-blocking `NoorResult.Failure` without throwing exceptions or disrupting playback.

## Technical Notes
- Files in scope:
  - `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/data/remote/ManifestApiService.kt`
  - `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/data/repository/ManifestRepositoryImpl.kt`
  - `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/data/repository/PlaybackHeartbeatRepositoryImpl.kt`
  - `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/domain/repository/ManifestRepository.kt`
  - `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/domain/repository/PlaybackHeartbeatRepository.kt`
- Architecture refs: `sdocs/architecture-ref.md` §6.1, §6.2.
- Invariants: Signed CDN URLs must never be logged or persisted in plaintext beyond `kmpplayer` secure cache.

## Test Approach
- Unit: Mock HTTP responses for manifest fetch (200 OK with captions/audio tracks, 404, 410).
- Unit: Mock HTTP responses for heartbeat (`POST /v1/playback/{content_id}`).
- Failure test: Assert heartbeat network errors do not propagate exceptions.

## Out of Scope
- Throttling calculation (handled by ViewModel in STORY-013).
- Media3/AVPlayer low-level decoding (handled by kmpplayer in STORY-014).
