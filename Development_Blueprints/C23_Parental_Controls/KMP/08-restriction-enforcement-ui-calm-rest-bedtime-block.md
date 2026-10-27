# K-08 — Restriction Enforcement UI (Calm Rest / Bedtime Block / Override Resume)

## 1. Feature Context
The child-facing moment of enforcement — arguably the single UI surface in the entire app most at risk of feeling punitive if mishandled. Must be warm, calm, and never abrupt (PRD C.23 §12.7, §2.1–2.2, §1.18 Screens #10–15).

## 2. Parent Feature
Feature C.23 — Parental Controls (Screen Time, Bedtime, AI Permissions, Content Age Level)

## 3. Sub-feature
2.8 Restriction Enforcement UI (Calm Rest / Bedtime Block / Override Resume) (ID: **K-08**)

## 4. Objective
Build `CalmRestScreen`, `BedtimeBlockScreen`, the Mid-Content Bedtime Cutoff variant, the Warning Notification in-app component, and the Parent Override Gate resume flow, observing K-07's `HeartbeatState` and using only warm, non-alarming visual tokens.

## 5. Business Requirements
- §12.7 (defining child-wellbeing commitment): graceful-finish-never-abrupt-cutoff, calm non-shaming rest-screen/bedtime-block UX.
- FR-2 items 4–5: current short activity allowed to finish/save before block; bedtime stops at content boundary, never mid-word in an active Quran lesson.
- Edge Case 1: mid-quiz limit reached → question completes, score saves, then rest screen.
- Edge Case 2: mid-episode bedtime cutoff → pauses at nearest natural content boundary, not literally mid-sentence.
- Edge Case 3: override granted while blocked → unblocks the same session immediately, no re-entry required.
- §7 item 3: UI test scanning color usage — no red/alarm-toned token anywhere on Calm Rest/Bedtime Block screens.

## 6. Existing Architecture
Module: lives in the Child Mode app shell (not `:feature:parental-controls`, which is Parent-Mode-only), consuming K-07's `HeartbeatState` Flow. Reuses the Parent Override Gate screen shared with C.19 (do not build a parallel gate UI).

## 7. Existing Code to Reuse
- K-07's `UsageHeartbeatManager.heartbeatState: Flow<HeartbeatState>`
- C.19's Parent Gate screen/launcher (shared, reused here for the override flow — confirm the exact composable/route name from C.19's KMP blueprints before wiring)
- `:core:design-system` — confirm the design system's calm/warm token set (per PRD §2.1) has no red/alarm tokens accidentally available to this screen's palette

## 8. Files to Create
- `feature/child-mode-shell/src/commonMain/kotlin/.../ui/CalmRestScreen.kt`
- `feature/child-mode-shell/src/commonMain/kotlin/.../ui/BedtimeBlockScreen.kt`
- `feature/child-mode-shell/src/commonMain/kotlin/.../ui/MidContentBedtimeCutoffVariant.kt`
- `feature/child-mode-shell/src/commonMain/kotlin/.../ui/WarningNotificationBanner.kt`
- `feature/child-mode-shell/src/commonMain/kotlin/.../ui/OverrideAuditConfirmationComponent.kt`
- `feature/child-mode-shell/src/commonMain/kotlin/.../viewmodel/RestrictionEnforcementViewModel.kt`
- `feature/child-mode-shell/src/commonTest/kotlin/.../RestrictionEnforcementViewModelTest.kt`
- `feature/child-mode-shell/src/androidUiTest/kotlin/.../CalmRestScreenColorAuditTest.kt`

## 9. Files to Modify
- Child Mode app shell root — observe `HeartbeatState`; when `limitReached` transitions true, allow the current short activity to complete (do not interrupt mid-call), then route to `CalmRestScreen`; when `bedtimeActive` transitions true, route to `BedtimeBlockScreen` (new session attempt) or `MidContentBedtimeCutoffVariant` (mid-session, pausing at the nearest content boundary)

## 10. KMP Requirements
- `RestrictionEnforcementViewModel`: observes K-07's `HeartbeatState`; exposes derived UI events (`ShowWarning`, `ShowCalmRest`, `ShowBedtimeBlock`, `ShowMidContentCutoff`) without itself performing any local-time calculation.
- **Graceful finish**: the current in-progress short activity (e.g., quiz question, current audio segment) must be allowed to complete before the block UI appears — this is enforced by *when* the shell checks `HeartbeatState` (at natural activity-boundary checkpoints), not by the server ever forcibly interrupting mid-call (already guaranteed by B-02's design).
- `CalmRestScreen`: warm illustration, "Mashallah! Great learning today. Time to rest." (or localized equivalent), subtle "Ask a grown-up for more time" link → Parent Override Gate. States: Default, Override-requested (loading), Override-granted (session resumes).
- `BedtimeBlockScreen`: shown on new-session attempt during bedtime window.
- `MidContentBedtimeCutoffVariant`: shown when bedtime begins mid-session; pauses playback/activity at the nearest natural content boundary (reuse A.4's "stop at boundary, never mid-word" logic for audio content specifically; generalize the same principle for non-audio content types).
- `WarningNotificationBanner`: in-app component shown when `warningThresholdCrossed` is true, does not block interaction.
- Override flow: tapping "Ask a grown-up for more time" launches the shared Parent Gate; on success, calls B-03's override-grant endpoint (via a repository call, not a direct raw network call from this ViewModel — confirm/reuse the appropriate repository), then observes K-07's next heartbeat to confirm unblock and resumes the session **without requiring the child to re-enter**.
- **Zero red/alarm-toned color tokens** anywhere on `CalmRestScreen`/`BedtimeBlockScreen` — enforced by only referencing the design system's designated "calm" token subset, never the general palette.

## 11. API Contract
### Required API (consumed, indirectly via repositories)
- Reads: K-07's `HeartbeatState` (already wraps B-02)
- Writes: B-03's `POST /v1/restriction-overrides` (via the override-request repository call, triggered after Parent Gate success)

## 12. Database Requirements
N/A.

## 13. Validation
N/A (display/state-driven, no user input beyond the override-request tap and Parent Gate interaction).

## 14. Authentication
The override request itself requires passing the shared Parent Gate (C.19), which the child cannot pass without a parent physically present — this is the security boundary, not an app-level auth check on this screen.

## 15. Authorization
N/A beyond the Parent Gate requirement for the override path.

## 16. Error Handling
| Scenario | UI Behavior |
|---|---|
| Override request fails (network) | Inline error on the gate/loading state, allow retry |
| Parent Gate cancelled | Return to Calm Rest/Bedtime Block screen unchanged, no error toast |
| Heartbeat state momentarily unavailable | Retain last known enforcement state (per K-07 §10) rather than flickering the UI |

## 17. Offline First
Enforcement UI reacts to whatever `HeartbeatState` K-07 currently holds (server-derived or fail-closed-offline) — this layer has no independent offline logic of its own; it is a pure consumer/renderer of K-07's state.

## 18. Local Data
N/A (consumes K-07's state only).

## 19. Localization
"Mashallah! Great learning today. Time to rest." and all other copy fully localized in EN/HI/AR/UR (PRD provides explicit Arabic wording as a reference translation — use platform localization pipeline, not a hardcoded Arabic string).

## 20. RTL
All enforcement screens must mirror correctly in RTL, including the illustration/text layout balance.

## 21. Analytics
`restriction_warning_notification_fired`, `restriction_limit_reached`, `restriction_calm_rest_screen_shown`, `restriction_bedtime_block_shown`, `restriction_bedtime_midcontent_cutoff_shown`, `restriction_override_requested`, `restriction_override_granted` (with `minutes_granted`, `granted_by`).

## 22. Performance
Must not introduce jank or ANR risk during the enforcement transition (a moment where a child may be actively engaged in content) — test transition smoothness explicitly. `@Immutable` state throughout.

## 23. Security
No security-sensitive logic in this layer beyond correctly gating the override path behind the shared Parent Gate — reuse, never reimplement, that gate.

## 24. Library Requirements
Jetpack Compose, Koin, `core-design-system`'s calm token subset.

## 25. Testing
- Unit: `RestrictionEnforcementViewModel` correctly maps `HeartbeatState` transitions to the right UI event, with no local-time derivation.
- UI test (color audit): scan `CalmRestScreen` and `BedtimeBlockScreen` composable output for any red/alarm-toned design-system color token — assert zero matches (per §7 item 3 of the PRD's Android prompt).
- UI test: no countdown-timer composable present on either screen.
- Integration test: full limit-reached → graceful-finish (current activity completes) → Calm Rest Screen → Parent Gate → override-granted → session resumes without re-entry.
- Integration test: midnight-crossing bedtime mid-session → Mid-Content Cutoff variant → pauses at content boundary, never mid-word (coordinate with A.4's existing audio-boundary test fixtures).

## 26. Documentation
KDoc on `CalmRestScreen.kt` and `BedtimeBlockScreen.kt` stating explicitly: "This screen must never use red/alarm color tokens or a countdown timer — this is a hard, tested UX requirement, not a style preference."

## 27. AI Coding Agent Implementation Steps

**Task 01 — Confirm Design System's Calm Token Subset**
- Objective: Identify the exact `core-design-system` tokens designated "calm"/warm before building screens, to scope the color-audit test correctly.

**Task 02 — Implement `RestrictionEnforcementViewModel`**
- Files to Create: `viewmodel/RestrictionEnforcementViewModel.kt`
- Dependencies: K-07's `UsageHeartbeatManager`.

**Task 03 — Implement `CalmRestScreen`**
- Files to Create: `ui/CalmRestScreen.kt`
- Implementation Details: Only calm tokens; "Ask a grown-up for more time" link.

**Task 04 — Implement `BedtimeBlockScreen`**

**Task 05 — Implement `MidContentBedtimeCutoffVariant`**
- Implementation Details: Reuse A.4's content-boundary-pause logic for audio; generalize for other content types.

**Task 06 — Implement `WarningNotificationBanner`**

**Task 07 — Wire Override Request Flow**
- Implementation Details: Launch shared C.19 Parent Gate; on success, call B-03's override endpoint via the appropriate repository; observe next heartbeat for unblock confirmation.

**Task 08 — Implement `OverrideAuditConfirmationComponent`**

**Task 09 — Wire Graceful-Finish Checkpoint Logic into Child Mode Shell**
- Files to Modify: Child Mode app shell.
- Implementation Details: Check `HeartbeatState` at natural activity-boundary checkpoints, never mid-call.

**Task 10 — Add Color-Audit UI Test**
- Files to Create: `CalmRestScreenColorAuditTest.kt`
- Objective: Automated, CI-enforced — not a manual design review only.

**Task 11 — Add Full Enforcement-Flow Integration Test**

**Task 12 — Add Localization Strings (including reference Arabic wording from PRD)**

**Task 13 — Final Code Review**
- Objective: Confirm zero red/alarm tokens, zero countdown-timer composables, correct reuse of C.19's Parent Gate.

## 28. Definition of Done
- Color-audit test passes (zero red/alarm tokens).
- Full limit-reached → graceful-finish → Calm Rest → override → resume flow verified end-to-end.
- Mid-content bedtime cutoff verified to pause at a natural boundary, never mid-word.

## 29. Final Verification Checklist
- [ ] Automated color-audit test passes on both enforcement screens
- [ ] No countdown-timer composable present
- [ ] Graceful-finish checkpoint logic confirmed (no mid-call interruption)
- [ ] Override flow reuses C.19's shared Parent Gate (not reimplemented)
- [ ] Session resumes without re-entry after override grant
- [ ] Localization (including Arabic reference wording) and RTL verified
