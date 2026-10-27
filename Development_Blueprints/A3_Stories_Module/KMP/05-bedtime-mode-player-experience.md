# K-05 — Bedtime Mode Player Experience

## 1. Feature Context
A calming theme/behavior overlay on the same player Composable (not a separate screen) — dimmed navy/teal palette, calmer narration, sleep timer, and a dua/reflection ending instead of a bright reward animation. Resolved once at player entry so a mid-session bedtime-window crossing never causes a flicker.

## 2. Parent Feature
Feature A.3 — Stories Module (Animated Storytelling System)

## 3. Sub-feature
2.5 Bedtime Mode Player Experience (ID: **K-05**)

## 4. Objective
Implement `isBedtimeMode` as a boolean resolved once at player-launch time and passed into K-03's player Composable, driving a dimmed theme override, sleep timer control, and a dua-ending path — independent of the device's light/dark theme setting.

## 5. Business Requirements
- FR-11: dims UI, disables stimulating reward animations, calmer/slower narration, soft nasheed underscore, always ends with dua/reflection.
- FR-12: parent-configured sleep timer fades audio/dims screen, can auto-pause/auto-exit at expiry.
- §2.1 Design: Bedtime Theme Override is independent of system light/dark theme — a content-context state, not a display preference.
- Edge Case 6: bedtime-eligible story started just before the window begins, finishes just after → visual/narration treatment evaluated at story-start time and held consistent for the session (no mid-session flicker); ending dua/reflection treatment respects the window state at completion time if materially different.

## 6. Existing Architecture
`feature:stories` player sub-package, a pure theme/behavior overlay on K-03's shared player Composable — explicitly NOT a separate screen/Activity/Route, per the PRD's Android AI-prompt requirement #6.

## 7. Existing Code to Reuse
- `feature/stories/player/StoryPlayerScreen.kt` (K-03, extend with `isBedtimeMode` parameter)
- `core-designsystem`: theming override mechanism (confirm existing pattern for content-context theme overrides, e.g., how any existing "focus mode" or similar override is implemented, and follow it — do not invent a parallel theming system)
- Parent bedtime-window configuration (read from existing parent settings surface, likely under C.23 Parental Controls — confirm exact repository/API and reuse, do not duplicate)

## 8. Files to Create
- `feature/stories/player/BedtimeThemeOverlay.kt`
- `feature/stories/player/SleepTimerControl.kt`
- `feature/stories/player/DuaReflectionEndingCard.kt`
- `feature/stories/viewmodel/BedtimeModeResolver.kt` (resolves `isBedtimeMode` once at entry from time-window + Bedtime Corner entry point)
- `test/feature/stories/BedtimeModeResolverTest.kt`
- `androidTest/feature/stories/BedtimeModePlayerTest.kt`

## 9. Files to Modify
- `feature/stories/player/StoryPlayerScreen.kt` (K-03) — accept `isBedtimeMode: Boolean` parameter, apply theme override and behavior branches
- `feature/stories/player/StoryPlayerViewModel.kt` (K-03) — branch reward-reveal/ending logic based on `isBedtimeMode`

## 10. KMP Requirements
- `BedtimeModeResolver.resolve(entryPoint, currentTime, parentBedtimeWindow)`: pure function evaluated exactly once when the player screen is composed/launched — the result is passed down as an immutable parameter, never re-evaluated mid-session even if the window boundary is crossed during playback.
- Theme override applies regardless of device light/dark mode — dimmed navy/teal palette, reduced/removed geometric border framing (per §2.1, simplified relative to standard theme), no flashing elements under any circumstance (stricter reduced-motion than standard mode).
- Reward-reveal behavior branches: standard mode shows the brief celebratory reveal (K-06); Bedtime Mode suppresses it and instead shows `DuaReflectionEndingCard` — XP/reward is still recorded quietly server-side (B-04 is unaffected; this is purely a presentation branch).
- Sleep Timer: options 15/30/45/60 min or "until story ends"; a distinct "Sleep Timer Expiring" gentle fade-warning state before auto-pause; auto-pause/auto-exit calls K-03's `PlayerState` transitions (pause via `KMPPlayerController.pause()`), never a raw platform timer bypassing the state machine.
- Ending-treatment exception: per Edge Case 6, the ending card's window-state check happens at completion time (may differ from the entry-time `isBedtimeMode` resolution if materially different) — this is the one deliberate exception to "resolved once at entry," and must be implemented as a separate, explicit check at the completion step, not a re-evaluation of the whole `isBedtimeMode` flag.

## 11. Required API
None directly — reads existing parent bedtime-window configuration (via whatever repository already serves C.23 Parental Controls) and B-04's completion response (for the reward data shown quietly in the dua ending).

## 12. Offline First
Bedtime-window configuration should be cached locally (via the existing parent-settings local cache, not a new one) so bedtime-mode resolution works fully offline.

## 13. Local Data
Reuses existing parent-settings local cache — no new local store introduced by this sub-feature.

## 14. Localization
Dua/reflection text, sleep-timer labels, and calmer narration cues (if text-rendered) sourced from shared localization resources across EN/HI/AR/UR.

## 15. RTL
Sleep timer control and dua card layout mirror correctly; star-particle ambient overlay is symmetric and requires no directional mirroring itself.

## 16. Analytics
Emit `bedtime_mode_entered`, `bedtime_sleep_timer_set`, `bedtime_session_ended_with_dua` via `AnalyticsTracker`.

## 17. Performance
Reduced-motion enforcement must not introduce jank elsewhere — verify the dimmed-theme recomposition doesn't cascade into unnecessary re-renders of the underlying video surface.

## 18. Security
No new security surface; sleep-timer auto-pause/auto-exit must not interfere with B-04's completion idempotency (if a session is paused/exited mid-story, no completion call has fired yet — nothing to reconcile).

## 19. Testing
- Unit: `BedtimeModeResolver` determinism (mocked time-window boundary cases per Edge Case 6), sleep-timer expiry state transitions.
- UI: dimmed theme applies regardless of device light/dark mode (mocked both), no flashing elements verified via a reduced-motion assertion, dua ending replaces (not supplements) the standard reward reveal.
- Integration: mid-session window-boundary crossing does NOT cause the standard-vs-bedtime visual treatment to flicker (explicit Edge Case 6 regression test).

## 20. AI Coding Agent Implementation Steps

**Task 01 — Implement `BedtimeModeResolver`**
Objective: Pure function resolving `isBedtimeMode` once at entry from entry-point + time-window. Follow: domain-layer pure-function conventions. Tests: mocked time-window boundary cases, Bedtime Corner explicit-entry override. Definition of Done: Edge Case 6 test scenarios pass.

**Task 02 — Confirm and Wire Parent Bedtime-Window Configuration Source**
Objective: Locate the existing repository/API serving C.23 Parental Controls' bedtime-window setting and reuse it (never duplicate). Tests: config-read correctness. Definition of Done: no new parallel settings storage introduced.

**Task 03 — Implement `BedtimeThemeOverlay`**
Objective: Dimmed navy/teal theme, simplified border framing, star-particle ambient overlay, independent of device theme. Follow: `core-designsystem`'s theming-override pattern. Dependencies: Task 01. Tests: theme-independence-from-device-setting test. Definition of Done: test passes for both device light and dark modes.

**Task 04 — Implement `SleepTimerControl`**
Objective: 15/30/45/60/until-story-ends options, expiring-warning state, auto-pause/auto-exit via K-03's `PlayerState`. Dependencies: K-03. Tests: expiry-state-transition test, auto-pause-uses-state-machine test (not a raw bypass). Definition of Done: tests pass.

**Task 05 — Implement `DuaReflectionEndingCard`**
Objective: Calm ending replacing the standard reward reveal in Bedtime Mode, still reflecting the quietly-recorded reward data from B-04's response. Dependencies: K-06 (completion flow), Task 01. Tests: reward-still-recorded-but-not-celebrated assertion. Definition of Done: test passes.

**Task 06 — Wire `isBedtimeMode` into `StoryPlayerScreen`/`ViewModel`**
Objective: Thread the resolved flag through K-03's existing player Composable and ViewModel as an immutable entry parameter; implement the Edge Case 6 completion-time exception explicitly. Dependencies: K-03, Task 01, 05. Tests: no-mid-session-flicker regression test, completion-time-exception test. Definition of Done: both tests pass.

**Task 07 — Add Analytics Instrumentation**
Objective: Three events per §16. Tests: fake-tracker assertions. Definition of Done: exactly one call site per event.

**Task 08 — Full RTL and Reduced-Motion Pass**
Objective: Verify mirroring and confirm zero flashing elements under any circumstance. Tests: per §19. Definition of Done: baselines captured, reduced-motion assertion passes.

**Task 09 — Add Full Test Suite**
Objective: Complete coverage per §19. Definition of Done: all green.

**Task 10 — Final Code Review**
Objective: Confirm Bedtime Mode is genuinely a theme/behavior overlay on the same Composable/Route (not a forked screen), confirm the entry-time-resolution-with-one-explicit-exception design is implemented exactly as specified. Definition of Done: checklist in §21 checked.

## 21. Final Verification Checklist
- [ ] `isBedtimeMode` resolved exactly once at player entry, never flickers on mid-session window-boundary crossing
- [ ] Ending-treatment exception (completion-time re-check) implemented as the one deliberate exception, per Edge Case 6
- [ ] Dimmed theme applies independent of device light/dark mode
- [ ] Zero flashing elements under any circumstance (stricter than standard mode)
- [ ] Sleep timer auto-pause/auto-exit routes through K-03's `PlayerState` machine, never a raw bypass
- [ ] Reward still recorded server-side in Bedtime Mode, just not celebratorily displayed
- [ ] Bedtime Mode is implemented as a theme/behavior overlay on the same Composable, not a separate screen/Activity
- [ ] All three analytics events fire correctly
- [ ] Full RTL mirroring verified

## 22. Definition of Done
Bedtime Mode delivers a calm, theme-consistent, non-flickering, reduced-stimulation playback experience with a functioning sleep timer and dua ending, layered cleanly on top of K-03's shared player engine without forking a parallel screen.
