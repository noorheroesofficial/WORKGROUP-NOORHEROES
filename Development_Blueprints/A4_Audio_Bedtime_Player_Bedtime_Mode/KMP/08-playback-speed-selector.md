# K-08 — Playback Speed Selector

## 1. Feature Context
A simple, low-light-friendly modal letting the child choose a comfortable listening speed (0.8x/1.0x/1.2x) for the Bedtime Audio Player. Called out as its own screen/component in the PRD's screen inventory (§1.18, item 5) and its own analytics event (`playback_speed_changed`), but was only generically referenced as part of K-01's "secondary control row" without a dedicated component, file, or event — this sub-feature closes that gap.

## 2. Parent Feature
Feature A.4 — Audio Bedtime Player & Bedtime Mode

## 3. Sub-feature
2.8 Playback Speed Selector (ID: **K-08**)

## 4. Objective
Build `PlaybackSpeedSelector` as a simple list-style modal (matching the Sleep Timer Selector's low-light simplicity requirement), reading available speeds from B-02's `playback_speed_options` manifest field, applying the selected rate to `AudioPlayerController`, and correctly re-deriving completion-threshold math at the new speed (coordinating with K-04's percentage-based, not wall-clock-based, completion detection).

## 5. Business Requirements
- FR-2: Playback Speed (e.g., 0.8x/1x/1.2x) is one of the required controls on the Audio Bedtime Player.
- §1.8 NFR: all controls large-tap-target (≥56dp primary / ≥44dp secondary), high-contrast, full screen-reader support — speed selector is a secondary control (≥44dp entry point) but its modal options list must still meet the same low-light-usability bar as the Sleep Timer Selector.
- §2.2: "speed/timer selectors are simple list-style modals, not complex gesture-based pickers (low-light, possibly half-asleep child usage context demands maximum simplicity)."
- §1.10 Edge Case 7: playback speed changed mid-episode → completion-threshold calculation must still be based on actual content consumed (percentage of total duration), not wall-clock time, so a 1.5x-speed listen still correctly registers full completion.
- §1.19: `playback_speed_changed` analytics event.

## 6. Existing Architecture
`AudioPlayerController` (`library:kmpplayer`) already exposes a settable playback-rate property (confirm the exact method/property name — likely mirrors ExoPlayer's `setPlaybackParameters`/`playbackSpeed` — before wiring; this sub-feature does not add rate-control capability to the player library, it only adds the UI and manifest-driven option list on top of an existing capability). Modeled directly on K-02's Sleep Timer Selector's list-style-modal pattern (same simplicity/accessibility bar), sharing visual conventions but with no functional dependency on K-02 beyond that stylistic precedent.

## 7. Existing Code to Reuse
- `library:kmpplayer::AudioPlayerController` (playback-rate property/method)
- K-02's `SleepTimerControl.kt` list-style modal pattern (visual/structural precedent — mirror the simple vertical list convention, not a shared component)
- B-02's `playback_speed_options` manifest field (K-01's already-fetched manifest data)
- K-01's `BedtimePlayerState` (speed selection is a lightweight UI-state concern layered on the existing state machine, not a new state branch)

## 8. Files to Create
- `feature/bedtime-audio/player/PlaybackSpeedSelector.kt`
- `test/feature/bedtime-audio/PlaybackSpeedSelectorTest.kt`
- `androidTest/feature/bedtime-audio/PlaybackSpeedSelectorUiTest.kt`

## 9. Files to Modify
- `feature/bedtime-audio/player/BedtimeAudioViewModel.kt` (K-01) — add `setPlaybackSpeed(rate: Float)` calling `AudioPlayerController`'s rate property, and expose current `playbackSpeed` as part of the screen's observable state
- `feature/bedtime-audio/player/BedtimeAudioPlayerScreen.kt` (K-01) — wire the speed-selector icon in the secondary control row to open `PlaybackSpeedSelector`

## 10. KMP Requirements
- `PlaybackSpeedSelector`: simple vertical list of speed options sourced from B-02's `playback_speed_options` (e.g., `[0.8, 1.0, 1.2]`) — no hardcoded option list in the composable itself, since content-specific overrides could exist in a future manifest revision.
- Current selection highlighted; selecting a new option applies immediately (no separate "confirm" step, consistent with the low-friction list-modal pattern) and closes the sheet.
- Rate change applies to `AudioPlayerController` immediately, mid-playback, without a pause/resume glitch.
- Completion-threshold math (owned by K-04) must remain percentage-of-duration-consumed based regardless of the active rate — this sub-feature's only obligation is to ensure the rate change is correctly reflected in whatever position/duration values K-04 reads (i.e., don't let a rate change desync the controller's reported position), not to reimplement K-04's threshold logic itself.
- Accessibility: options list items ≥44dp tap targets, screen-reader labeled with the speed value and "currently selected" state.

## 11. Required API
None — `playback_speed_options` already arrives via K-01's existing manifest fetch (B-02); no separate network call.

## 12. Offline First
Fully local — speed selection and application require no network access; works identically online/offline.

## 13. Local Data
No persistence of a chosen speed across sessions is specified by the PRD (each session starts at the default 1.0x) — confirm this against the PRD before adding any cross-session persistence; do not add speculative persistence beyond what's specified.

## 14. Localization
Speed labels (e.g., "0.8x — Slower", "1.0x — Normal", "1.2x — Faster") sourced from shared localization resources across EN/HI/AR/UR; numeric formatting respects locale conventions.

## 15. RTL
List items and the modal sheet mirror correctly for Arabic/Urdu.

## 16. Analytics
`BedtimeAnalytics`: `playback_speed_changed` (with the new rate value), fired exactly once per user-initiated speed change (not on the initial default-rate load).

## 17. Performance
Rate change must not introduce audio glitching/stuttering — verify via manual/instrumented check that `AudioPlayerController`'s rate-change call is glitch-free at the player-library level (if glitching is observed, this is a `library:kmpplayer` concern to flag, not something to work around in this module).

## 18. Security
No new security surface.

## 19. Testing
- Unit: selector renders options exactly matching `playback_speed_options` from the manifest (no hardcoded fallback list masking a missing/malformed manifest field — confirm the correct empty/error-state behavior if the field is absent, likely falling back to a safe default `[1.0]`).
- Unit: `setPlaybackSpeed()` correctly calls `AudioPlayerController`'s rate-setting API with the selected value.
- UI: current-selection highlighting; tap-target size ≥44dp; screen-reader labels present.
- Integration (coordinate with K-04): completion-threshold correctness at 1.5x speed remains percentage-based, not wall-clock (this is primarily K-04's test, but this sub-feature's rate-change implementation must not break it — a regression check against K-04's existing Edge-Case-7 test is sufficient, not a duplicate test).

## 20. AI Coding Agent Implementation Steps

**Task 01 — Add `setPlaybackSpeed()` to `BedtimeAudioViewModel`**
Objective: Wire a rate-change call through to `AudioPlayerController`, expose current rate as observable state. Files to modify: `BedtimeAudioViewModel.kt` (K-01). Tests: rate-setting call-shape test. Definition of Done: test passes.

**Task 02 — Implement `PlaybackSpeedSelector` Composable**
Objective: List-style modal sourced from the manifest's `playback_speed_options`, current-selection highlighting, immediate-apply-on-select behavior. Files to create: `PlaybackSpeedSelector.kt`. Follow: K-02's Sleep Timer Selector's list-modal visual convention. Dependencies: Task 01. Tests: options-match-manifest test, safe-default-when-field-absent test. Definition of Done: tests pass.

**Task 03 — Wire the Speed-Selector Entry Point in `BedtimeAudioPlayerScreen`**
Objective: Secondary-row speed icon opens the selector. Files to modify: `BedtimeAudioPlayerScreen.kt` (K-01). Dependencies: Task 02. Tests: covered by Task 05. Definition of Done: entry point wired and tappable.

**Task 04 — Add Analytics Instrumentation**
Objective: `playback_speed_changed` fired exactly once per user-initiated change, never on initial load. Dependencies: Task 01. Tests: fake-tracker assertion (no emission on default-rate mount, one emission per actual change). Definition of Done: test passes.

**Task 05 — Add Full Test Suite**
Objective: Complete coverage per §19. Definition of Done: all green.

**Task 06 — Regression-Check Against K-04's Completion-Threshold Test**
Objective: Confirm this sub-feature's rate-change implementation does not desync the position/duration values K-04's percentage-based completion detection relies on. Dependencies: K-04. Definition of Done: K-04's existing Edge-Case-7 test still passes with this module's changes present.

**Task 07 — Final Code Review**
Objective: Confirm the options list is genuinely manifest-driven, not hardcoded; confirm accessibility tap-target/labeling requirements are met. Definition of Done: checklist in §21 checked.

## 21. Final Verification Checklist
- [ ] Speed options rendered directly from B-02's `playback_speed_options`, with a safe `[1.0]` default if the field is absent — never a hardcoded list masking a manifest gap
- [ ] Rate change applies immediately mid-playback with no glitch
- [ ] Current selection visibly highlighted, ≥44dp tap targets, screen-reader labeled
- [ ] `playback_speed_changed` fires exactly once per user-initiated change, never on initial mount
- [ ] K-04's percentage-based completion-threshold test still passes with a rate change applied mid-session
- [ ] Full RTL mirroring verified

## 22. Definition of Done
Children can adjust playback speed via a simple, low-light-friendly list modal sourced from the manifest's speed options, with the rate change correctly reflected everywhere K-04's completion logic and analytics depend on accurate playback position/duration — closing the PRD's screen-inventory and analytics-event gap left open by K-01's original scope.
