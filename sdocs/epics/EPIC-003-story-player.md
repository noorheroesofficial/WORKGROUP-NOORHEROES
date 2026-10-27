---
id: EPIC-003
title: Story Player Core Playback Engine
status: planned
prd: ../../PRD_Documents/Child App (1-12)/Feature_A3_Stories_Module.md
prd_sections: ["1.7", "1.13", "1.14", "1.16"]
depends_on: [EPIC-002]
created: 2026-09-29
---

## Description
Implements the full-screen immersive Story Player core playback engine (K-03) wrapping `library:kmpplayer`'s `KMPPlayerController` and `AudioPlayerController` for video, audio, and text formats. Driven by a single sealed `PlayerState` machine as the sole source of truth for both engine commands and Compose overlay visibility, preventing state desynchronization bugs. Features session-scoped `client_event_id` UUID generation, throttled playback heartbeats (5–10s), safe-stop on media-unavailable with child-friendly recommendations, scrub-ahead clamp for restricted series, resume position persistence via `PlaybackSessionManager`, and visual fidelity to `Player.png`.

## Stories
- STORY-011 — Add StoryPlayerRoute as Full-Screen Destination
- STORY-012 — Implement Manifest and Playback Heartbeat Data Layer
- STORY-013 — Implement PlayerState Machine, Throttled Heartbeat, and Scrub Clamp
- STORY-014 — Wire KMPPlayerController, Safe-Stop on Unavailable, and PlaybackSessionManager
- STORY-015 — Implement StoryTextPlayer Composable for Text Stories
- STORY-016 — Implement StoryPlayerScreen Composable, Subtitle Overlay, and Telemetry
- STORY-017 — Integration Verification of Story Player Core Playback Engine

## Out of Scope
- Interactive branch moments and mid-story quizzes (deferred to K-04 / EPIC-004)
- Bedtime Mode ambient night sky and auto-sleep timer (deferred to K-05 / EPIC-005)
- Post-playback completion reward celebration & streak triggers (deferred to K-06 / EPIC-006)
