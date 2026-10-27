# K-04 — Dua / Calm-Reflection Ending & Quiet Reward Flow

## 1. Feature Context
Closes every Bedtime Mode listening session with a genuinely calming, spiritually grounding moment instead of a bright "level up" screen — the reward is still recorded (via B-03's `silent_completion`), just never celebrated visually in this context.

## 2. Parent Feature
Feature A.4 — Audio Bedtime Player & Bedtime Mode

## 3. Sub-feature
2.4 Dua / Calm-Reflection Ending & Quiet Reward Flow (ID: **K-04**)

## 4. Objective
On completion threshold reached while `forceCalmMode` (K-03) is true, call B-03's completion endpoint with `silent_completion: true` and render the Dua/Calm-Reflection Ending Card instead of the standard celebratory completion screen — verified to contain zero XP/points/badge counters while still confirming the reward was recorded via a separate repository-level assertion.

## 5. Business Requirements
- FR-10: on reaching the completion threshold, the player transitions directly to a dua/calm-reflection card — reward still recorded quietly, not visually celebrated.
- §2.1: Dua Ending Card — warm parchment-on-navy card, gentle fade-in (≥800ms), no XP/badge counters visible even though the reward was recorded.
- §1.10 Edge Case 7: completion-threshold calculation based on actual content consumed (percentage of duration), not wall-clock time — correct even at altered playback speed.
- §1.10 Edge Case 8: sleep-timer expiry coinciding with natural completion — completion/ending sequence takes precedence (child still gets the calm dua ending, not pre-empted by a fade cutting off the dua itself).

## 6. Existing Architecture
Reuses A.5/Dua Learning's existing dua content-rendering pattern (Arabic + transliteration + translation) rather than building a new text-rendering component — confirm the exact shared composable A.5 uses for this and reuse it directly. Completion flow itself is new to this module (K-01's screen), calling B-03's shared, already-extended completion endpoint.

## 7. Existing Code to Reuse
- A.5/Dua Learning's dua-text rendering composable (Arabic + transliteration + translation layout) — reuse directly, do not reimplement
- K-01's `BedtimeAudioViewModel`/`BedtimePlayerState` (completion-threshold detection hooks into this state machine)
- K-03's `forceCalmMode` resolved value (read-only input to this sub-feature's branching decision)
- B-02's `dua_ending_ref` manifest field (content reference to render)

## 8. Files to Create
- `feature/bedtime-audio/ending/DuaReflectionEndingCard.kt`
- `feature/bedtime-audio/ending/BedtimeCompletionRepository.kt` (B-03 client, `completeEpisode(contentId, silentCompletion: Boolean)`)
- `test/feature/bedtime-audio/BedtimeCompletionFlowTest.kt`
- `androidTest/feature/bedtime-audio/DuaEndingCardTest.kt`

## 9. Files to Modify
- `feature/bedtime-audio/player/BedtimeAudioViewModel.kt` (K-01) — detect completion threshold (percentage-of-duration-consumed based, not wall-clock), branch to `DuaReflectionEndingCard` when `forceCalmMode` is true, call `BedtimeCompletionRepository.completeEpisode(silentCompletion=true)`

## 10. KMP Requirements
- Completion-threshold detection: based on percentage of actual content consumed (using `AudioPlayerController`'s reported position/duration), not wall-clock elapsed time — so a 1.5x-speed listen still correctly registers full completion at the same content-percentage threshold as 1x speed.
- On threshold reached with `forceCalmMode == true`: call `BedtimeCompletionRepository.completeEpisode(contentId, silentCompletion=true)` (B-03), then transition `BedtimePlayerState` to a completion state rendering `DuaReflectionEndingCard` instead of any standard celebratory completion UI.
- On threshold reached with `forceCalmMode == false`: standard (non-bedtime) completion flow applies — this module does not alter that path, it only adds the calm-mode branch.
- `DuaReflectionEndingCard`: dua text (reusing A.5's rendering pattern) via `dua_ending_ref` (B-02), sleepy/calm Noor companion illustration variant, single low-key "Done"/"Next Episode" action, gentle fade-in (≥800ms) — the composable tree for this card must contain **zero** XP/points/badge counter views, verified by a dedicated UI test.
- Reward-recorded-but-not-celebrated verification: a **separate repository-level test** (not a UI assertion) confirms `BedtimeCompletionRepository.completeEpisode()` was actually called with `silentCompletion=true` — decoupling "was the reward recorded" from "was it visually celebrated" as two independently-tested facts.
- Edge Case 8 handling: if sleep-timer expiry (K-02) and natural completion threshold occur at the same instant, this module's completion path takes precedence — coordinate with K-02 via a shared "completion in progress" guard so K-02's fade-out logic checks and yields if a completion transition has already begun.
- Next Episode offer: if unlocked (per K-01's Sequential Unlock check), offered from the Dua Ending Card with the same Bedtime Mode treatment retained if still within the window.

## 11. Required API
**User API** — B-03 `POST /v1/content/{id}/complete` (with `silent_completion: true`).

## 12. Offline First
Completion calls queue/retry per the existing offline-heartbeat-and-completion pattern established in A.3/K-03 (fail gracefully without blocking the UI transition to the Dua Ending Card — the child should see the calm ending immediately even if the network call is still in flight/retrying in the background).

## 13. Local Data
No new local persistence; reuses A.3's existing offline completion-queue mechanism if one exists (confirm and reuse, do not build a parallel queue).

## 14. Localization
Dua text (Arabic + transliteration + translation) via A.5's existing localization resources; "Done"/"Next Episode" labels via shared localization resources across EN/HI/AR/UR.

## 15. RTL
Dua card layout mirrors correctly (text alignment, companion illustration placement, action button position) for Arabic/Urdu — reuse A.5's already-verified RTL handling for the dua-text component itself.

## 16. Analytics
`BedtimeAnalytics`: `bedtime_completion_threshold_reached`, `bedtime_reward_recorded_silently`, `dua_ending_card_shown`.

## 17. Performance
Completion-threshold percentage calculation is a lightweight comparison against `AudioPlayerController`'s existing position/duration reporting — no additional polling loop introduced beyond what K-01 already observes.

## 18. Security
No new security surface; completion call reuses B-03's existing idempotency-key handling (via K-01's session-scoped `client_event_id`, generated once per session per A.3/K-03's established convention — reused here, not regenerated).

## 19. Testing
- Unit: completion-threshold detection correctness at altered playback speeds (Edge Case 7) — assert percentage-based, not wall-clock-based.
- Unit: `forceCalmMode` branching — calm-mode sessions route to `DuaReflectionEndingCard`; non-calm sessions route to the standard completion flow (unaffected).
- **UI test:** `DuaReflectionEndingCard` composable tree contains no XP/points/badge counter views anywhere.
- **Repository-level test:** confirms the reward completion call still occurred with `silentCompletion=true`, independent of the UI assertion above.
- Integration: Edge Case 8 — simulate simultaneous sleep-timer expiry and natural completion, verify the Dua Ending Card is shown (not pre-empted by the fade).

## 20. AI Coding Agent Implementation Steps

**Task 01 — Implement `BedtimeCompletionRepository`**
Objective: Thin client for B-03's completion endpoint, threading `silentCompletion` and the session's existing `client_event_id`. Files to create: `BedtimeCompletionRepository.kt`. Follow: `core-network` conventions, A.3/K-03's idempotency-key reuse pattern. Tests: call-shape test asserting correct field population. Definition of Done: test passes.

**Task 02 — Implement Percentage-Based Completion-Threshold Detection**
Objective: Threshold check based on content-consumed percentage, not wall-clock time. Files to modify: `BedtimeAudioViewModel.kt` (K-01). Tests: altered-playback-speed correctness test (Edge Case 7). Definition of Done: test passes.

**Task 03 — Implement `DuaReflectionEndingCard` Composable**
Objective: Dua text (reusing A.5's rendering pattern), sleepy companion illustration, single low-key action, ≥800ms fade-in. Files to create: `DuaReflectionEndingCard.kt`. Dependencies: A.5's dua composable, B-02's `dua_ending_ref`. Tests: **no-XP/badge-counter UI test**. Definition of Done: test passes.

**Task 04 — Wire Calm-Mode Branching into the Completion Path**
Objective: On threshold reached with `forceCalmMode=true`, call Task 01's repository with `silentCompletion=true`, transition to Task 03's card; non-calm sessions unaffected. Files to modify: `BedtimeAudioViewModel.kt`. Dependencies: Task 01–03, K-03. Tests: branching test for both calm and non-calm sessions. Definition of Done: test passes.

**Task 05 — Implement the Reward-Still-Recorded Repository-Level Test**
Objective: Independent confirmation the completion call fired with `silentCompletion=true`, decoupled from the UI assertion in Task 03. Files to create: part of `BedtimeCompletionFlowTest.kt`. Dependencies: Task 04. Definition of Done: test passes.

**Task 06 — Implement Edge Case 8 Precedence Guard**
Objective: Shared "completion in progress" guard so K-02's fade-out yields if a completion transition has already begun at the same instant. Files to modify: `BedtimeAudioViewModel.kt`, coordinate with K-02's fade controller. Dependencies: Task 04, K-02. Tests: simultaneous-expiry-and-completion integration test. Definition of Done: test passes.

**Task 07 — Wire Next Episode Offer from the Dua Ending Card**
Objective: Offer Next Episode if unlocked, retaining Bedtime Mode treatment. Dependencies: K-01's Sequential Unlock check, Task 03. Tests: unlocked-vs-locked offer test. Definition of Done: test passes.

**Task 08 — Add Analytics Instrumentation**
Objective: Three events per §16. Tests: fake-tracker assertions. Definition of Done: exactly one call site per event.

**Task 09 — Add Full Test Suite**
Objective: Complete coverage per §19. Definition of Done: all green.

**Task 10 — Final Code Review**
Objective: Confirm the Dua Ending Card genuinely contains zero reward-celebration UI while the underlying reward call is independently verified to have occurred; confirm Edge Case 8 precedence is correctly implemented. Definition of Done: checklist in §21 checked.

## 21. Final Verification Checklist
- [ ] Completion-threshold detection is percentage-of-content-consumed based, correct at any playback speed
- [ ] `forceCalmMode=true` sessions call B-03 with `silent_completion=true` and route to the Dua Ending Card
- [ ] `forceCalmMode=false` sessions are entirely unaffected by this sub-feature's changes
- [ ] `DuaReflectionEndingCard` composable tree verified to contain zero XP/points/badge views
- [ ] Reward-call-occurred fact independently verified via a repository-level test, decoupled from the UI assertion
- [ ] Edge Case 8 (simultaneous timer expiry + completion) resolves in favor of the completion/dua flow
- [ ] Next Episode offered correctly when unlocked, retaining Bedtime Mode treatment
- [ ] All three analytics events fire correctly

## 22. Definition of Done
Every Bedtime Mode session closes with a genuinely calm, non-celebratory Dua ending while the reward is reliably and identically recorded server-side — independently verified via decoupled UI and repository-level tests, with correct precedence over a simultaneously expiring sleep timer.
