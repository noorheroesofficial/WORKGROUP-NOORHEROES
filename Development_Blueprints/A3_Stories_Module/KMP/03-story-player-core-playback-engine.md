# K-03 — Story Player Core Playback Engine (Video/Audio/Text)

## 1. Feature Context
The immersive full-screen player wrapping `library:kmpplayer`'s `KMPPlayerController`/`AudioPlayerController` for video/audio/text formats, driven by a single sealed state that is the sole source of truth for both actual playback and all Compose overlay visibility — preventing the desync bugs (e.g., "Playing" controls shown while ExoPlayer buffers) the PRD explicitly calls out.

## 2. Parent Feature
Feature A.3 — Stories Module (Animated Storytelling System)

## 3. Sub-feature
2.3 Story Player Core Playback Engine (Video/Audio/Text) (ID: **K-03**)

## 4. Objective
Build `StoryPlayerViewModel` and the player Composable wrapping `library:kmpplayer`, implementing throttled heartbeats, safe-stop on media-unavailable, session-scoped idempotent completion calls, and cold-start performance targets — as the shared engine that K-04, K-05, and K-06 layer on top of.

## 5. Business Requirements
- FR-7: video/audio/text formats with play/pause, caption toggle, audio-track selection, quality selection.
- §6.4 State Management: single sealed `PlayerState` is the sole source of truth for both Media3 calls and Compose overlay visibility.
- §6.5 API Mapping: heartbeats throttled 5–10s of actual playback time; `client_event_id` generated once per session, reused on retry.
- FR-16 / Error Handling: media withdrawn mid-playback → safe stop, age-appropriate explanation, recommended alternative — never a raw error/crash.
- NFR: cold start (cached manifest) p95 < 1.5s; video start-to-first-frame p95 < 2s on 3G-equivalent throttling.

## 6. Existing Architecture
`feature:stories` module's player sub-package, built on top of `library:kmpplayer`'s existing `KMPPlayerController` (video/text via `KMPPlayer` UI component), `AudioPlayerController` (audio via `AudioPlayer` UI component), and `PlaybackSessionManager` (resume-position persistence) — per `CORE_KMP_PLAYER_INSTRUCTIONS.md`. Explicitly does NOT call platform-specific Media3/AVPlayer APIs directly (prohibited by the core player module's usage rules).

## 7. Existing Code to Reuse
- `library:kmpplayer::rememberKMPPlayerController()`, `KMPPlayerController` (`prepare()`, `play()`, `pause()`, `seekTo()`)
- `library:kmpplayer::AudioPlayerController` (audio format)
- `library:kmpplayer::PlaybackSessionManager` (`getResumePosition()`)
- `library:kmpplayer::KMPPlayer`, `AudioPlayer` UI components
- `library:kmpplayer::KMPPlayerAnalytics` (technical QoS tracking, separate from business analytics)
- `library:kmpplayer::MediaSourceValidator.isValid()`, `TimeUtils.formatTime()`
- `core-network`: manifest-fetch client for B-07

## 8. Files to Create
- `feature/stories/player/StoryPlayerScreen.kt`
- `feature/stories/player/StoryPlayerViewModel.kt` (+ `PlayerState` sealed class, Event file)
- `feature/stories/player/StoryTextPlayer.kt` (text-format renderer, not covered by `library:kmpplayer`'s video/audio components)
- `feature/stories/data/ManifestRepository.kt` (B-07 client)
- `feature/stories/data/PlaybackHeartbeatRepository.kt` (B-03 client, throttled)
- `test/feature/stories/StoryPlayerViewModelTest.kt`
- `androidTest/feature/stories/StoryPlayerScreenTest.kt`

## 9. Files to Modify
- `core-navigation/Route.kt` — add `StoryPlayerRoute(episodeId)` as a distinct full-screen destination (system UI hidden, restored on exit)

## 10. KMP Requirements
- `PlayerState` sealed class: `Loading, Buffering, Playing, Paused, ChoiceActive(choicePointId), QuizActive, Unavailable(reason), Completed(reward)` — the SOLE source of truth driving both `KMPPlayerController` calls and Compose overlay visibility; no code path may show "Playing" UI while the underlying controller reports buffering.
- Manifest fetch (B-07) on entry; `MediaSourceValidator.isValid()` checked before `controller.prepare()`.
- Heartbeat throttling: driven by `library:kmpplayer`'s player-state callbacks (playing/paused/position), NOT a naive wall-clock timer that keeps firing while paused — sent every 5–10s of actual playback time via `PlaybackHeartbeatRepository` (B-03).
- `client_event_id` generated once at session start (`StoryPlayerViewModel.init`), reused identically on any retry of the eventual completion call (K-06 consumes this same ID) — never regenerated mid-session.
- Scrub-ahead UX clamp: when the manifest indicates `scrub_restricted: true`, the scrubber clamps forward-seek to furthest-reached-position + small tolerance; this is explicitly a UX nicety only — real enforcement is B-07's server-side re-validation, not this clamp.
- Safe-stop: on a fatal `KMPPlayerError` from the controller, transition immediately to `PlayerState.Unavailable(reason)` — render a child-friendly message + "Recommended for you instead" card sourced from the manifest's fallback field; never surface raw `KMPPlayerError` codes or technical text to the child.
- Resume position: read via `PlaybackSessionManager.getResumePosition()` and passed as `KMPPlayerConfig(startPositionMs=...)` on `prepare()`.
- Text-format stories use a dedicated `StoryTextPlayer` Composable (not part of `library:kmpplayer`, which is video/audio-focused) but still reports into the same `PlayerState` machine for consistency with the completion/choice/quiz flow.

## 11. Required API
**User API** — B-07 `GET /v1/content/{id}/manifest`, B-03 `POST /v1/playback/{content_id}`.

## 12. Offline First
```
Downloaded Media (K-07's DownloadRepository cache)
    ↓
StoryPlayerViewModel (prefers local KMPPlayerSource.Local if downloaded, else Network from manifest)
    ↓
KMPPlayerController
    ↓
UI
```
Heartbeats queue locally when offline and sync on reconnect (delegated to K-07's sync mechanism, this sub-feature only needs to fail heartbeat sends gracefully without blocking playback).

## 13. Local Data
`PlaybackSessionManager`'s existing `PlaybackSessionProvider` (DataStore/Room-backed per the core player module's note) persists resume position — reused, not reimplemented.

## 14. Localization
Captions/audio-track selection defaults resolve per active locale; on mid-session OS locale change, re-evaluate available tracks on resume (fallback to original audio + captions if no dub exists for the new locale, never silent/blank audio).

## 15. RTL
Caption text rendering right-to-left for Arabic/Urdu; player control layout (back, caption toggle, settings gear) mirrors position.

## 16. Analytics
Business events via `AnalyticsTracker`: `story_player_opened`, `story_playback_started`, `story_playback_paused`, `story_playback_resumed`, `story_media_unavailable_shown`. Technical QoS via `library:kmpplayer`'s `KMPPlayerAnalytics` (separate concern — buffering/error rates, not business funnel events).

## 17. Performance
- Cold start p95 < 1.5s with a cached manifest — manifest fetch and `controller.prepare()` must not block the initial composable render (show branded loading spinner with cover art immediately, per PRD §1.13).
- No main-thread blocking during buffering; `library:kmpplayer` handles the heavy lifting per its documented responsibility boundary.
- Prevent unnecessary recomposition: `PlayerState` fields must be stable/immutable data classes.

## 18. Security
- Manifest signed URLs (from B-07) are short-TTL and never persisted to disk in plaintext beyond `library:kmpplayer`'s own secure cache handling; this ViewModel does not log the raw playback URL.
- `client_event_id` generated client-side using a secure UUID generator — no predictable/sequential IDs.

## 19. Testing
- Unit: heartbeat throttling driven by actual player-state callbacks (not wall-clock), `client_event_id` stability across retries, scrub-clamp logic for `scrub_restricted` series.
- Player simulation tests: safe-stop transition on a simulated `KMPPlayerError`, verifying no raw error text reaches any rendered string.
- Integration: cold-start timing measurement against the p95 budget on a low-end device profile (per PRD NFR).

## 20. AI Coding Agent Implementation Steps

**Task 01 — Add `StoryPlayerRoute` as a Distinct Full-Screen Destination**
Objective: Route with system UI (status/nav bars) hidden, restored on exit; deep link `noorheroes://stories/{episode_id}`. Follow: existing full-screen-destination pattern if one exists elsewhere, else establish it here per `core-navigation` conventions. Definition of Done: route compiles, system UI hide/restore verified manually.

**Task 02 — Implement `ManifestRepository` and `PlaybackHeartbeatRepository`**
Objective: Thin clients for B-07/B-03. Follow: `core-network` conventions. Tests: manifest fetch success/failure handling, heartbeat send failure is non-blocking. Definition of Done: tests pass.

**Task 03 — Implement `PlayerState` Sealed Class and `StoryPlayerViewModel` Skeleton**
Objective: Establish the single source of truth state machine, session-scoped `client_event_id` generation. Follow: `BaseViewModel`. Tests: `client_event_id` stability test. Definition of Done: test passes.

**Task 04 — Wire `KMPPlayerController`/`AudioPlayerController` Integration**
Objective: `prepare()`/`play()`/`pause()`/`seekTo()` calls driven exclusively by `PlayerState` transitions; player-state callbacks feed back into `PlayerState` updates (bidirectional but state-machine-governed, never UI-assumed). Dependencies: Task 03, `library:kmpplayer`. Tests: state-sync test asserting overlay visibility never diverges from actual controller state across a scripted sequence of events. Definition of Done: desync test passes.

**Task 05 — Implement Throttled Heartbeat Sending**
Objective: 5–10s throttle driven by `Player.Listener`-equivalent callbacks from `library:kmpplayer`, not a wall-clock timer. Dependencies: Task 02, 04. Tests: heartbeat does not fire while paused, fires within the throttle window while playing. Definition of Done: tests pass.

**Task 06 — Implement Safe-Stop on Media-Unavailable**
Objective: `PlayerState.Unavailable(reason)` transition on fatal `KMPPlayerError`, child-friendly message + recommended-alternative card, zero raw technical text. Dependencies: Task 04. Tests: technical-text blocklist assertion (e.g., no "Exception", "Error code", "0x" substrings in any rendered string) per the PRD's own stated test approach. Definition of Done: blocklist test passes.

**Task 07 — Implement Scrub-Ahead UX Clamp**
Objective: Forward-seek clamp for `scrub_restricted: true` series, explicitly documented as non-authoritative. Dependencies: Task 02, 04. Tests: clamp boundary test. Definition of Done: test passes.

**Task 08 — Implement `StoryTextPlayer` Composable**
Objective: Text-format story renderer reporting into the same `PlayerState` machine. Follow: `core-designsystem` typography/scaling conventions (dynamic text scaling per PRD accessibility requirement). Dependencies: Task 03. Tests: text-scaling UI test. Definition of Done: test passes.

**Task 09 — Wire Resume Position via `PlaybackSessionManager`**
Objective: Read resume position on prepare, persist on session end. Dependencies: Task 04, `library:kmpplayer::PlaybackSessionManager`. Tests: resume-position round-trip test. Definition of Done: test passes.

**Task 10 — Implement `StoryPlayerScreen` Composable**
Objective: Full-screen player UI wrapping `KMPPlayer`/`AudioPlayer`/`StoryTextPlayer` per format, auto-hiding minimal chrome. Dependencies: Tasks 01–09. Tests: cold-start timing test, UI tests per §19. Definition of Done: p95 cold-start budget met on test device profile.

**Task 11 — Add Analytics Instrumentation**
Objective: Business events per §16, technical QoS via `KMPPlayerAnalytics`. Tests: fake-tracker assertions. Definition of Done: exactly one call site per event.

**Task 12 — Add Full Test Suite**
Objective: Complete coverage per §19. Definition of Done: all green.

**Task 13 — Final Code Review**
Objective: Confirm zero direct Media3/AVPlayer calls exist in this module's code (per `library:kmpplayer`'s explicit "DON'T" rule), confirm `PlayerState` is genuinely the sole source of truth with no bypass paths. Definition of Done: checklist in §21 checked.

## 21. Final Verification Checklist
- [ ] `PlayerState` is the sole source of truth — no code path shows overlay UI diverging from actual controller state
- [ ] Heartbeats throttled to actual playback time (5–10s), never fire while paused
- [ ] `client_event_id` generated once per session, identical across retries
- [ ] Safe-stop on media-unavailable shows child-friendly message + alternative, zero raw technical text (blocklist-tested)
- [ ] Scrub-ahead clamp applied for `scrub_restricted` series, documented as non-authoritative
- [ ] Cold start p95 < 1.5s with cached manifest
- [ ] No direct Media3/AVPlayer API calls anywhere in this module (uses `library:kmpplayer` exclusively)
- [ ] Resume position correctly read/persisted via `PlaybackSessionManager`
- [ ] Text-format stories report into the same `PlayerState` machine as video/audio

## 22. Definition of Done
The Story Player reliably drives video/audio/text playback through `library:kmpplayer` with a single authoritative state machine, safe-stop handling, throttled heartbeats, and cold-start performance meeting the PRD's targets — providing the shared engine K-04 (choice/quiz overlays), K-05 (Bedtime Mode), and K-06 (completion flow) all build directly on top of.
