---
id: STORY-016
epic: EPIC-003
kind: feature
title: Implement StoryPlayerScreen Composable, Subtitle Overlay, and Telemetry
status: ready
priority: P0
prd: ../../PRD_Documents/Child App (1-12)/Feature_A3_Stories_Module.md
depends_on: [STORY-014, STORY-015]
produces: []
consumes: [domain.story-player]
created: 2026-09-29
---

## User Story
As a child learner, I want an immersive full-screen story player matching `Player.png` with auto-hiding controls, circular back button, Islamic golden flourishes, caption toggle, subtitle banner, scrubber slider, and seamless telemetry.

## Acceptance Criteria
- [ ] AC1: Given `Player.png`, renders full-screen player with top chrome (circular back button, episode title, series title, caption toggle button, settings gear button, crescent moon motif, Islamic corner flourishes).
- [ ] AC2: Given center media area, renders large circular play/pause button (`controlLarge`), media surface, and "Choice moment →" placeholder pill button (K-04 seam).
- [ ] AC3: Given bottom controls, renders rounded dark semi-transparent subtitle card (`colors.scrim.copy(alpha = 0.75f)`) and horizontal scrubber slider with elapsed time and duration labels.
- [ ] AC4: Given user inactivity (3000ms), top and bottom chrome auto-hides; tapping anywhere on the media surface toggles control visibility.
- [ ] AC5: Given analytics tracker, emits `story_player_opened`, `story_playback_started`, `story_playback_paused`, `story_playback_resumed`, and `story_media_unavailable_shown`.
- [ ] AC6: Given `rule.md`, contains 0 raw colors, 0 raw dp/sp, 0 raw shapes, 0 raw Material 3 components, stays strictly `< 500 lines`, and maintains 100% 4-locale parity.
- [ ] AC7: Given audio-format episodes (`format == "audio"`), renders dedicated audio player view matching `Bedtime Player.png` with calm celestial stars, crescent moon, and audio narration wave / cover art.
- [ ] AC8: Given settings gear button (`⚙`), opens `VideoSettingsBottomSheet` for stream quality selection (`auto`, `1080p`, `720p`, `480p`, `360p`), audio track switching, and playback speed adjustment.

## Technical Notes
- Files in scope:
  - `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/ui/player/StoryPlayerScreen.kt`
  - `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/ui/player/StoryPlayerControls.kt`
  - `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/ui/player/StoryPlayerSubtitles.kt`
  - `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/ui/player/StoryAudioPlayerView.kt`
  - `core/core-common/src/commonMain/composeResources/values*/strings_stories.xml` (EN, AR, HI, UR strings)
- String keys to add across all 4 locales:
  - `story_player_play_cd`, `story_player_pause_cd`, `story_player_seek_forward_cd`, `story_player_seek_backward_cd`
  - `story_player_captions_on_cd`, `story_player_captions_off_cd`, `story_player_settings_cd`
  - `story_player_choice_moment_label`, `story_player_unavailable_title`, `story_player_unavailable_desc`, `story_player_unavailable_cta`
  - `story_player_scrubber_cd`, `story_player_loading`
- Visual reference: `Screens/Mobile App/Stories/Player.png` & `Bedtime Player.png`.

## Test Approach
- UI tests: Verify overlay visibility toggling, control auto-hide timer, play/pause tap interaction.
- Analytics tests: Fake `AnalyticsTracker` verifying exact emission counts for all playback events.

## Out of Scope
- Branch choice resolution (covered in K-04).
- Sleep timer dimming (covered in K-05).
