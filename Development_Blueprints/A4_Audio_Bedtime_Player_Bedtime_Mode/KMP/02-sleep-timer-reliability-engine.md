# K-02 — Sleep Timer Reliability Engine

## 1. Feature Context
The single most safety-critical piece of Feature A.4: a sleep timer that must reach 100% reliability, because failure means a child's device blaring audio at 2am. Backed by both an in-process foreground-service countdown (for normal-case UI accuracy) and an `AlarmManager`-scheduled fallback (for OS process-death resilience) — never a plain coroutine `delay()` in a ViewModel.

## 2. Parent Feature
Feature A.4 — Audio Bedtime Player & Bedtime Mode

## 3. Sub-feature
2.2 Sleep Timer Reliability Engine (ID: **K-02**)

## 4. Objective
Implement `SleepTimerState` as a sealed class and back it with both a foreground Service holding a coroutine countdown and an `AlarmManager.setExactAndAllowWhileIdle` fallback alarm targeting the same expiry instant, driving a smooth volume-ramp fade-out and auto-pause through K-01's `BedtimePlayerState` machine — never a raw bypass of it.

## 5. Business Requirements
- FR-3: Sleep Timer options bounded by parent-set ceiling (B-01); child freely chooses up to the ceiling, or "until episode ends" if allowed.
- FR-6: expiry triggers a gentle audio fade-out (not abrupt cut) over a configurable duration (default 15s), followed by auto-pause.
- §1.8 NFR: sleep-timer-expiry auto-pause must be foreground-service-backed, not UI-thread-only — 100% reliability, non-negotiable.
- §1.10 Edge Case 1: natural completion before timer expiry cancels the now-moot timer cleanly, no leftover fade/pause attempt.
- §1.10 Edge Case 2: mid-playback timer change applies from the change moment, cancels/reschedules any pending fade under the old timer.
- §1.10 Edge Case 8: sleep-timer expiry coinciding with natural episode completion — completion/ending sequence takes precedence (handled jointly with K-04).
- §6.4/§7 Android AI Prompt: dual foreground-Service + `AlarmManager` architecture is the feature's most safety-critical implementation detail.

## 6. Existing Architecture
No existing sleep-timer mechanism exists elsewhere in the codebase to reuse — this is new, safety-critical infrastructure. It integrates with, but does not modify, K-01's `BedtimePlayerState` machine: all pause/fade actions are expressed as calls into K-01's ViewModel/controller, never a direct/raw `AudioPlayerController` call from this module bypassing the state machine.

## 7. Existing Code to Reuse
- `library:kmpplayer::AudioPlayerController` (`pause()`, and its volume-control surface for the fade ramp — confirm whether `AudioPlayerController` exposes a settable volume property; if not, coordinate a minimal additive API surface with the `library:kmpplayer` module rather than working around it)
- K-01's `BedtimeAudioViewModel`/`BedtimePlayerState` (this module drives transitions through it)
- K-07's `BedtimeRepository.getConfig()` (sleep-timer ceiling source)
- Android `Service`, `AlarmManager`, `BroadcastReceiver` platform APIs (no KMP abstraction needed here — Android-specific per the PRD's explicit Android AI prompt; iOS equivalent noted separately below)

## 8. Files to Create
- `feature/bedtime-audio/timer/SleepTimerState.kt` (sealed class: `Off, Active(remainingSeconds), Warning(secondsLeft), FadingOut, Expired`)
- `feature/bedtime-audio/timer/SleepTimerControl.kt` (Composable: selector + persistent countdown chip)
- `feature/bedtime-audio/timer/SleepTimerForegroundService.kt` (Android: in-process coroutine countdown)
- `feature/bedtime-audio/timer/SleepTimerAlarmScheduler.kt` (Android: `AlarmManager.setExactAndAllowWhileIdle` fallback scheduling)
- `feature/bedtime-audio/timer/SleepTimerExpiryReceiver.kt` (Android: `BroadcastReceiver` triggering the same auto-pause/fade logic if the foreground service was killed)
- `feature/bedtime-audio/timer/SleepTimerFadeController.kt` (volume-ramp logic, 200–500ms tick interval, platform-agnostic where possible)
- `feature/bedtime-audio/timer/GoodnightIdleState.kt` (Composable: the calm terminal screen shown after auto-pause completes — Screen Inventory §1.18 item 9 — distinct from `SleepTimerState.Expired`, which is the state-machine value; this is its dedicated visual render, not an inline fragment of `SleepTimerControl`)
- `test/feature/bedtime-audio/SleepTimerStateTest.kt`
- `androidTest/feature/bedtime-audio/SleepTimerReliabilityTest.kt` (process-death simulation)

## 9. Files to Modify
- `feature/bedtime-audio/player/BedtimeAudioViewModel.kt` (K-01) — accept `SleepTimerState` updates and route pause/fade actions through `BedtimePlayerState` transitions

## 10. KMP Requirements
- `SleepTimerState` sealed class exactly as specified: `Off, Active(remainingSeconds), Warning(secondsLeft), FadingOut, Expired`.
- Sleep Timer Selector renders **only** options ≤ the parent-set ceiling (from K-07) plus "until episode ends" if `allow_until_episode_ends_option` is true — options above the ceiling are not rendered disabled, they do not appear at all.
- Dual-timer architecture (Android): foreground Service coroutine countdown for the primary UI-driving timer, plus `AlarmManager.setExactAndAllowWhileIdle` scheduled at the identical expiry instant as a fallback; if the in-process timer is killed by the OS, the `BroadcastReceiver` triggers the same fade/pause logic path (not a separate/divergent implementation).
- iOS equivalent: since iOS background execution differs fundamentally from Android's `AlarmManager` model, the iOS implementation must use the platform's background audio session + a scheduled local notification or background task API as the fallback mechanism — confirm the exact iOS background-task API available to the app's existing background-audio entitlement setup before implementing; do not assume Android's exact API surface transfers directly.
- Fade-out: smooth volume ramp (200–500ms coroutine ticks) over the configured duration (default 15s, overridable per-content via B-02's `recommended_fade_duration_seconds` if populated) — never an abrupt volume-to-zero jump or a hard `pause()` without the ramp.
- Mid-playback timer extension: changing from e.g. 15 to 30 minutes recalculates expiry from the **change moment**, cancels any pending fade/pause callback scheduled under the old timer, and reschedules both the in-process timer and the `AlarmManager` fallback.
- Natural completion before timer expiry: cancel the pending timer (both in-process and `AlarmManager` fallback) cleanly — no leftover fade/pause attempt firing against already-stopped audio.
- All auto-pause/auto-fade actions call into K-01's `BedtimeAudioViewModel`'s exposed transition methods (e.g., `onSleepTimerExpired()`) — never a raw `controller.pause()` call from this module bypassing `BedtimePlayerState`.
- Wake-lock/foreground-service scope released promptly on pause/completion (battery NFR) — no continuous wake-lock beyond what's needed for active playback.
- `GoodnightIdleState`: on reaching `SleepTimerState.Expired` (fade + auto-pause complete), render this dedicated calm terminal composable — Screen Inventory §1.18 item 9, distinct from `SleepTimerControl`'s countdown-chip UI — offering only "Resume playback" or "Exit player" actions, no further interaction required from the child; also reachable via a manual pause-and-leave (not exclusively sleep-timer-driven).

## 11. Required API
None directly — reads K-07's cached `BedtimeRepository.getConfig()` for the sleep-timer ceiling.

## 12. Offline First
Fully local/on-device mechanism; the only network dependency is the initial config fetch (K-07), which itself fails safe (defaults to no ceiling override needed since the timer itself is client-managed — confirm K-07's fail-safe default still yields a sane conservative ceiling for the selector to render, per B-01's safe-default response).

## 13. Local Data
No new local persistence required — timer state is session-scoped (not persisted across app restarts per Edge Case 3: no auto-resume on next foreground open after a force-kill).

## 14. Localization
Sleep timer duration labels (e.g., "30 minutes", "Until episode ends") sourced from shared localization resources across EN/HI/AR/UR; duration formatting respects locale-specific number formatting.

## 15. RTL
Sleep Timer Selector list and countdown chip mirror correctly for Arabic/Urdu layouts.

## 16. Analytics
`BedtimeAnalytics`: `sleep_timer_opened`, `sleep_timer_set` (with `duration_minutes`), `sleep_timer_changed_mid_playback`, `sleep_timer_expired`, `sleep_timer_fade_started`, `sleep_timer_auto_paused`, `bedtime_goodnight_idle_shown` (fired once when `GoodnightIdleState` is actually rendered — both the sleep-timer-driven path and the manual pause-and-leave path) — all fired tied to actual foreground-service/`AlarmManager` timer callbacks or the corresponding UI-render event, never optimistic UI timing, so these events accurately reflect real playback-engine state for the reliability-monitoring alert described in the PRD's DevOps section.

## 17. Performance
- Fade-out volume ramp ticks (200–500ms) must not introduce jank in the surrounding UI — verify no main-thread blocking during the ramp.
- Foreground service resource usage minimal; wake-lock scope released immediately on pause/completion to avoid overnight battery drain if accidentally left running past the timer's intended scope.

## 18. Security
No new security surface. Sleep-timer auto-pause/auto-exit must not interfere with B-03's completion idempotency — if a session is paused/exited via the sleep timer mid-episode, no completion call has fired, so there is nothing to reconcile with K-04's silent-completion flow.

## 19. Testing
- Unit: `SleepTimerState` transition logic including mid-playback extension (Edge Case 2) and natural-completion-before-expiry cleanup (Edge Case 1).
- **Foreground-service reliability test (signature test for this sub-feature):** instrumented test simulating process trim/low-memory conditions, verifying the `AlarmManager` fallback still fires the auto-pause within acceptable tolerance (±5 seconds) even if the primary in-process timer is killed.
- Unit: fade-out uses a smooth volume ramp, never an abrupt cut (assert multiple intermediate volume values are set, not a single jump-to-zero call).
- UI: Sleep Timer Selector renders only options ≤ parent ceiling (mocked ceiling values).
- Unit: expiry-vs-natural-completion race — when both occur at the same instant, verify K-04's completion path takes precedence over the fade (this test may need to be co-located with or cross-referenced against K-04's test suite).

## 20. AI Coding Agent Implementation Steps

**Task 01 — Implement `SleepTimerState` Sealed Class**
Objective: The five-state sealed class exactly as specified. Files to create: `SleepTimerState.kt`. Tests: state-shape unit tests. Definition of Done: compiles, used by all subsequent tasks.

**Task 02 — Implement `SleepTimerForegroundService` (In-Process Countdown)**
Objective: Foreground Service holding a coroutine-based countdown, emitting `SleepTimerState` updates. Files to create: `SleepTimerForegroundService.kt`. Dependencies: Task 01. Tests: countdown accuracy under normal conditions. Definition of Done: test passes.

**Task 03 — Implement `SleepTimerAlarmScheduler` and `SleepTimerExpiryReceiver` (Fallback)**
Objective: `AlarmManager.setExactAndAllowWhileIdle` scheduled at the same expiry instant; `BroadcastReceiver` triggers identical auto-pause/fade logic on fire. Files to create: `SleepTimerAlarmScheduler.kt`, `SleepTimerExpiryReceiver.kt`. Dependencies: Task 01–02. Tests: **the process-death simulation instrumented test** — kill the hosting process mid-countdown, verify the `AlarmManager` fallback still results in playback paused at the correct time. Definition of Done: this test passes; treat as a launch-blocking gate per the PRD's §15 go/no-go requirement.

**Task 04 — Implement `SleepTimerFadeController` (Volume Ramp)**
Objective: Smooth volume ramp over the configured fade duration (default 15s), 200–500ms ticks. Files to create: `SleepTimerFadeController.kt`. Dependencies: `library:kmpplayer`'s volume-control surface (coordinate additive API if not already exposed). Tests: multi-tick ramp assertion, never a single jump-to-zero call. Definition of Done: test passes.

**Task 05 — Implement `SleepTimerControl` Composable**
Objective: Selector rendering only options ≤ parent ceiling (K-07), persistent countdown chip, expiring-warning state. Files to create: `SleepTimerControl.kt`. Dependencies: Task 01, K-07. Tests: ceiling-filtering UI test. Definition of Done: test passes.

**Task 06 — Wire Auto-Pause/Fade into K-01's `BedtimePlayerState` (No Raw Bypass)**
Objective: All timer-triggered actions route through `BedtimeAudioViewModel`'s exposed transition methods. Files to modify: `BedtimeAudioViewModel.kt` (K-01). Dependencies: Task 02–04. Tests: assert zero direct `AudioPlayerController.pause()` calls originate from this module — all calls go through the ViewModel. Definition of Done: test passes.

**Task 07 — Implement Mid-Playback Timer Extension and Natural-Completion Cleanup**
Objective: Edge Case 1 and 2 logic — reschedule on change, cancel cleanly on natural completion. Dependencies: Task 02–03, 06. Tests: both edge-case unit tests. Definition of Done: tests pass.

**Task 08 — Implement `GoodnightIdleState` Composable**
Objective: Dedicated calm terminal screen (Screen Inventory item 9) reachable via sleep-timer expiry or manual pause-and-leave, offering only Resume/Exit actions. Files to create: `GoodnightIdleState.kt`. Dependencies: Task 02–03 (`SleepTimerState.Expired`). Tests: renders on both entry paths (timer-expiry and manual pause-and-leave); no additional interaction affordances beyond Resume/Exit. Definition of Done: tests pass.

**Task 09 — Add Analytics Instrumentation**
Objective: Seven events per §16 (including `bedtime_goodnight_idle_shown`), tied to real timer callbacks or the corresponding UI-render event. Dependencies: Task 08. Tests: fake-tracker assertions. Definition of Done: exactly one call site per event.

**Task 10 — iOS Background-Fallback Equivalent**
Objective: Confirm and implement the iOS equivalent of the `AlarmManager` fallback using the platform's actual available background-task/notification API. Dependencies: Task 03. Tests: iOS-equivalent reliability test. Definition of Done: iOS reliability parity confirmed (or explicitly documented as a follow-up if the iOS platform capability genuinely differs enough to require a separate design review — do not silently ship a weaker guarantee without flagging it).

**Task 11 — Add Full Test Suite**
Objective: Complete coverage per §19. Definition of Done: all green.

**Task 12 — Final Code Review**
Objective: Confirm zero raw bypass of `BedtimePlayerState`; confirm the reliability test is genuinely a launch-blocking CI gate; confirm `GoodnightIdleState` is reachable from both entry paths. Definition of Done: checklist in §21 checked.

## 21. Final Verification Checklist
- [ ] `SleepTimerState` implemented exactly as the five-state sealed class specified
- [ ] Dual-mechanism reliability (foreground Service + `AlarmManager` fallback) verified via a process-death simulation test
- [ ] Fade-out is a smooth multi-tick volume ramp, never an abrupt cut
- [ ] Sleep Timer Selector renders only options ≤ parent ceiling — no disabled-but-visible options above it
- [ ] Mid-playback timer extension reschedules correctly from the change moment, cancelling stale callbacks
- [ ] Natural completion before expiry cancels the timer cleanly with no leftover fade/pause attempt
- [ ] All auto-pause/fade actions route through `BedtimePlayerState`, zero raw controller bypass
- [ ] Wake-lock/foreground-service scope released promptly on pause/completion
- [ ] `GoodnightIdleState` renders on both the sleep-timer-expiry path and the manual pause-and-leave path, offering only Resume/Exit
- [ ] All seven analytics events fire tied to real timer callbacks or the corresponding UI-render event, not optimistic UI timing
- [ ] iOS fallback mechanism confirmed against actual platform capability, not assumed from Android's API

## 22. Definition of Done
The Sleep Timer reliably fades and auto-pauses audio within tolerance even under simulated OS process death, drives all state changes through K-01's authoritative player state machine, and meets the PRD's non-negotiable 100% reliability target — verified by a dedicated, CI-gated process-death simulation test on both platforms.
