# K-01 — Bedtime Audio Player Core Screen

## 1. Feature Context
The dedicated, audio-first full-screen player for the nightly bedtime ritual — distinct from A.3's general video/text Story Player (K-03), but explicitly built on the same `:core:media-player` foundation rather than a parallel audio engine. This is the primary screen every other K-02 through K-07 sub-feature layers onto.

## 2. Parent Feature
Feature A.4 — Audio Bedtime Player & Bedtime Mode

## 3. Sub-feature
2.1 Bedtime Audio Player Core Screen (ID: **K-01**)

## 4. Objective
Build the `:feature:bedtime-audio` module's `BedtimeAudioPlayerScreen` Composable and `BedtimeAudioViewModel`, wrapping `library:kmpplayer`'s `AudioPlayerController`, driven by a `PlayerState`-equivalent sealed state consistent with A.3/K-03's state-machine discipline, fetching the audio manifest (B-02) on entry and rendering cover art, controls, and episode navigation.

## 5. Business Requirements
- FR-1: displays cover art, title, moral lesson teaser, source/scholar-approval status, episode list, privacy-safe listen counts.
- FR-2: Play/Pause, Seek, Playback Speed, Sleep Timer, Download, Next/Previous Episode controls.
- FR-7: playback continues uninterrupted if the screen locks or app backgrounds (foreground media service).
- FR-8: Next/Previous respects A.3's Sequential Unlock rules — Previous always available, Next gated.
- FR-9: listen counts are privacy-safe aggregates only (consumed from B-02's `listen_count_aggregate`).
- §1.8 NFR: audio start-to-first-sound p95 < 800ms cached, < 1.5s streamed; controls ≥56dp primary, ≥44dp secondary.
- §6.1–6.4: module `:feature:bedtime-audio`, depends on `:core:media-player` (shared Media3 foundation from A.3), `:core:design-system`, `:core:offline-cache`.

## 6. Existing Architecture
Per `CORE_KMP_PLAYER_INSTRUCTIONS.md`, all audio playback goes through `library:kmpplayer`'s `AudioPlayerController` and `AudioPlayer` UI component — this module never calls platform-specific Media3/AVPlayer APIs directly, mirroring the exact prohibition already enforced in A.3/K-03. `PlaybackSessionManager` (shared) persists resume position. This screen is a new module (`:feature:bedtime-audio`), not an extension of A.3's `:feature:stories` module, because it is a dedicated, differently-laid-out screen per the PRD's screen inventory (§1.18) — but it deliberately reuses every shared library/core module A.3 already established.

## 7. Existing Code to Reuse
- `library:kmpplayer::AudioPlayerController` (`prepare()`, `play()`, `pause()`, `seekTo()`)
- `library:kmpplayer::AudioPlayer` UI component
- `library:kmpplayer::PlaybackSessionManager.getResumePosition()`
- `library:kmpplayer::MediaSourceValidator.isValid()`, `TimeUtils.formatTime()`
- `library:kmpplayer::KMPPlayerAnalytics` (technical QoS, separate from business analytics)
- `core-network`: manifest-fetch client pattern (mirror A.3's `ManifestRepository`)
- `core-designsystem`: base component library, typography, tap-target sizing tokens
- `core-navigation/Route.kt`: full-screen destination pattern (mirror A.3/K-03's `StoryPlayerRoute`)

## 8. Files to Create
- `feature/bedtime-audio/player/BedtimeAudioPlayerScreen.kt`
- `feature/bedtime-audio/player/BedtimeAudioViewModel.kt` (+ `BedtimePlayerState` sealed class, Event file)
- `feature/bedtime-audio/player/CoverInfoHeader.kt`
- `feature/bedtime-audio/player/EpisodeListSheet.kt`
- `feature/bedtime-audio/data/BedtimeManifestRepository.kt` (B-02 client, extends/wraps A.3's `ManifestRepository` pattern with `format=audio`)
- `test/feature/bedtime-audio/BedtimeAudioViewModelTest.kt`
- `androidTest/feature/bedtime-audio/BedtimeAudioPlayerScreenTest.kt`

## 9. Files to Modify
- `core-navigation/Route.kt` — add `BedtimeAudioPlayerRoute(contentId)` as a distinct full-screen destination (system UI hidden, restored on exit), deep link `noorheroes://bedtime/{content_id}` (wired fully in K-06)

## 10. KMP Requirements
- `BedtimePlayerState` sealed class: `Loading, Buffering, Playing, Paused, Unavailable(reason), Completed(reward)` plus Bedtime-specific composed states from K-02/K-03/K-04 (`SleepTimerState`, calm-mode flag) rather than duplicating A.3/K-03's `PlayerState` — this is a parallel-but-consistent state machine for the audio-only surface, not a fork of A.3's exact type (different screen, different states like `ChoiceActive`/`QuizActive` are not applicable here).
- Manifest fetch (B-02, `format=audio`) on entry via `BedtimeManifestRepository`; `MediaSourceValidator.isValid()` checked before `controller.prepare()`.
- Resume position via `PlaybackSessionManager.getResumePosition()`, passed as the controller's start position on `prepare()`.
- Episode List Sheet: multi-part audio series, respects Sequential Unlock (reads unlock state from the manifest, same contract as A.3's episode list — reuse the unlock-state rendering component from `core-designsystem` if one exists, do not rebuild it).
- Next/Previous Episode: Previous always enabled; Next checks unlock state, shows the same lock-explanation pattern as A.3 (reuse the existing lock-explanation composable, do not duplicate).
- Foreground playback continuity: audio continues via a foreground `MediaSessionService` when backgrounded/screen-locked (the service itself is implemented/shared via `library:kmpplayer`; this screen configures and observes it, does not reimplement it).
- Loading/Buffering state renders an ambient glow pulse on the cover art (no platform spinner), title/cover visible immediately from cached manifest metadata even if audio itself buffers.

## 11. Required API
**User API** — B-02 `GET /v1/content/{id}/manifest?format=audio` (extended manifest fields), B-03 `POST /v1/content/{id}/complete` (consumed by K-04, not directly here).

## 12. Offline First
```
Downloaded Media (K-05's offline-cache, shared A.3 DownloadManager)
    ↓
BedtimeAudioViewModel (prefers local source if downloaded, else network from manifest)
    ↓
AudioPlayerController
    ↓
UI
```

## 13. Local Data
`PlaybackSessionManager`'s existing session provider persists resume position — reused, not reimplemented for this module.

## 14. Localization
Title, moral-lesson teaser, and all on-screen text sourced from shared localization resources (EN/HI/AR/UR); audio dub track selection resolves per active locale, consistent with A.3/K-03's caption/audio-track locale-resolution pattern.

## 15. RTL
Cover/header layout, control row order (previous/play/next), and scrub bar direction all mirror correctly for Arabic/Urdu; secondary control row (speed/timer/download/episode-list) also mirrors.

## 16. Analytics
`BedtimeAnalytics` (business events via `AnalyticsTracker`, technical QoS via `KMPPlayerAnalytics` — same separation of concerns as A.3/K-03): `bedtime_player_opened` (with `entry_source`), `bedtime_episode_list_opened`, `bedtime_episode_selected`, `bedtime_next_episode_tapped`, `bedtime_previous_episode_tapped`, `bedtime_next_episode_not_downloaded_shown`, `bedtime_media_unavailable_shown`, `app_backgrounded_during_bedtime_playback`, `bedtime_playback_resumed_after_background` — the latter two fired from the foreground `MediaSessionService`'s own lifecycle callbacks (§10's "continue playback via foreground `MediaSessionService`" requirement), not from Compose `onPause`/`onResume`, since the screen may not be composed at all while backgrounded audio continues.

## 17. Performance
- Cold start p95 < 1.5s with cached manifest; audio start-to-first-sound p95 < 800ms cached, < 1.5s streamed — manifest fetch and `controller.prepare()` must not block initial composable render.
- `BedtimePlayerState` fields stable/immutable data classes to prevent unnecessary recomposition.
- No main-thread blocking during buffering.

## 18. Security
- Manifest signed URLs (from B-02/A.3) short-TTL, never logged in plaintext, handled entirely by `library:kmpplayer`'s existing secure cache handling.
- No new credential surface.

## 19. Testing
- Unit: manifest-fetch success/failure handling, resume-position wiring, Next/Previous unlock-state gating.
- Player simulation: safe-stop transition to `Unavailable` on a fatal player error, verifying no raw technical text reaches any rendered string (mirror A.3/K-03's blocklist test approach).
- UI: cover art breathing animation renders correctly, control tap targets meet ≥56dp/≥44dp minimums, screen-reader labels present on all controls.
- Integration: cold-start timing measurement against the p95 budget on a low-end device profile.

## 20. AI Coding Agent Implementation Steps

**Task 01 — Add `BedtimeAudioPlayerRoute` as a Distinct Full-Screen Destination**
Objective: Route with system UI hidden/restored, deep link `noorheroes://bedtime/{content_id}`. Follow: A.3/K-03's `StoryPlayerRoute` pattern. Files to modify: `core-navigation/Route.kt`. Definition of Done: route compiles, system UI hide/restore verified manually.

**Task 02 — Implement `BedtimeManifestRepository`**
Objective: Thin client for B-02's `format=audio` manifest, reusing `core-network` conventions. Files to create: `BedtimeManifestRepository.kt`. Tests: fetch success/failure handling. Definition of Done: tests pass.

**Task 03 — Implement `BedtimePlayerState` and `BedtimeAudioViewModel` Skeleton**
Objective: Sole-source-of-truth state machine for this screen. Follow: `BaseViewModel`. Files to create: `BedtimeAudioViewModel.kt`. Tests: state-transition unit tests. Definition of Done: tests pass.

**Task 04 — Wire `AudioPlayerController` Integration**
Objective: `prepare()`/`play()`/`pause()`/`seekTo()` driven exclusively by `BedtimePlayerState` transitions; controller callbacks feed back into state updates. Dependencies: Task 03, `library:kmpplayer`. Tests: state-sync test (no overlay/controller divergence across a scripted event sequence). Definition of Done: desync test passes.

**Task 05 — Implement `CoverInfoHeader` and Core Controls Layout**
Objective: Cover art with breathing animation, title/teaser/scholar-badge, scrub bar, play/pause/next/prev, secondary row. Follow: `core-designsystem` tap-target and typography tokens. Dependencies: Task 03. Tests: tap-target-size UI test. Definition of Done: test passes.

**Task 06 — Implement `EpisodeListSheet` with Sequential Unlock**
Objective: Multi-part series list, Next gated / Previous always available, reusing A.3's lock-explanation composable. Dependencies: Task 02, 03. Tests: lock-explanation-shown-on-locked-tap test. Definition of Done: test passes.

**Task 07 — Wire Resume Position and Foreground Playback Continuity**
Objective: `PlaybackSessionManager` resume read/persist; verify continued playback on backgrounding via foreground `MediaSessionService`. Dependencies: Task 04. Tests: instrumented backgrounding test asserting playback position advances. Definition of Done: test passes.

**Task 08 — Add Analytics Instrumentation**
Objective: Business events per §16, technical QoS via `KMPPlayerAnalytics`, including `app_backgrounded_during_bedtime_playback`/`bedtime_playback_resumed_after_background` fired from the foreground `MediaSessionService`'s lifecycle callbacks (not Compose lifecycle, since audio may continue while the screen is not composed). Tests: fake-tracker assertions, exactly one call site per event; instrumented backgrounding test asserting both events fire in the correct order. Definition of Done: tests pass.

**Task 09 — Add Full Test Suite**
Objective: Complete coverage per §19. Definition of Done: all green.

**Task 10 — Final Code Review**
Objective: Confirm zero direct Media3/AVPlayer calls exist in this module (uses `library:kmpplayer` exclusively); confirm cold-start budget met. Definition of Done: checklist in §21 checked.

## 21. Final Verification Checklist
- [ ] `BedtimePlayerState` is the sole source of truth — no overlay/controller divergence
- [ ] Zero direct Media3/AVPlayer API calls anywhere in this module
- [ ] Cold start p95 < 1.5s with cached manifest; audio start p95 < 800ms cached / < 1.5s streamed
- [ ] All primary controls ≥56dp, secondary ≥44dp, screen-reader labeled
- [ ] Next Episode respects unlock state; Previous always available
- [ ] Playback continues via foreground service on background/screen-lock
- [ ] Resume position correctly read/persisted via `PlaybackSessionManager`
- [ ] All analytics events fire correctly with exactly one call site each, including `app_backgrounded_during_bedtime_playback`/`bedtime_playback_resumed_after_background` fired from the foreground service's own lifecycle, not Compose lifecycle
- [ ] Full RTL mirroring verified

## 22. Definition of Done
The Bedtime Audio Player reliably drives audio playback through `library:kmpplayer` with a single authoritative state machine, correct Sequential Unlock behavior, foreground playback continuity, and cold-start performance meeting the PRD's targets — providing the shared screen K-02 through K-06 all build directly on top of.
