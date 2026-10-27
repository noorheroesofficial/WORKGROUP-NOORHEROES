---
id: repo.story-manifest
kind: repo
title: Manifest & Playback Heartbeat Repository Interface
status: draft
owner_story: STORY-012
version: 1
created: 2026-09-29
---

# Contract: repo.story-manifest

- **Kind**: Domain Repository Interface
- **Owner Story**: `STORY-012`
- **Status**: Draft

## Repository Interfaces

```kotlin
interface ManifestRepository {
    suspend fun getManifest(contentId: String): NoorResult<StoryManifest>
}

interface PlaybackHeartbeatRepository {
    suspend fun sendHeartbeat(
        contentId: String,
        eventType: String,
        positionSeconds: Int,
        clientEventId: String,
    ): NoorResult<Boolean>
}
```

## Domain Manifest Entity

```kotlin
data class StoryManifest(
    val contentId: String,
    val playbackUrl: String,
    val expiresAt: String,
    val format: String, // "video", "audio", "text"
    val durationSeconds: Int,
    val captions: List<StoryCaptionTrack>,
    val audioTracks: List<StoryAudioTrack>,
    val qualities: List<String>,
    val scrubRestricted: Boolean,
)

data class StoryCaptionTrack(
    val language: String,
    val label: String,
    val url: String,
    val format: String,
)

data class StoryAudioTrack(
    val language: String,
    val label: String,
    val url: String,
    val isDefault: Boolean,
)
```

## Invariants
1. `ManifestRepository` caches signed manifests with short TTL to meet the cold-start p95 < 1.5s budget.
2. `PlaybackHeartbeatRepository` returns `NoorResult.Failure` without throwing exceptions, ensuring playback is never interrupted by heartbeat errors.
