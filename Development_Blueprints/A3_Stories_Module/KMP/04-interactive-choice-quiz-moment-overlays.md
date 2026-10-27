# K-04 — Interactive Choice & Quiz Moment Overlays

## 1. Feature Context
In-player overlays appearing at scripted timestamps: a max-3-option Choice Overlay reflecting an Islamic value, and a Pause-and-Quiz Moment overlay. Choice branching is deterministic and entirely client-side so playback is never blocked on a network round-trip; the 3-option cap is enforced defensively even though B-11/B-05 already constrain it upstream.

## 2. Parent Feature
Feature A.3 — Stories Module (Animated Storytelling System)

## 3. Sub-feature
2.4 Interactive Choice & Quiz Moment Overlays (ID: **K-04**)

## 4. Objective
Build the Choice Overlay and Quiz Moment Overlay Composables driven by `PlayerState.ChoiceActive`/`QuizActive` (from K-03), with deterministic client-side branch mirroring, input debouncing, and offline-safe event queuing to B-05.

## 5. Business Requirements
- FR-7: in-story interactive choice overlays, pause-and-quiz moments.
- §2.1 Design: two-to-three large, clearly differentiated option cards, never more than 3, no countdown-timer pressure.
- Edge Case 3: rapid repeated taps debounced/queued so no choice is silently dropped or double-counted.
- §7 Android AI Code-Generation Prompt requirement #4: Choice Overlay hard-enforces max 3 options via a `require()` assertion in debug builds, failing loudly rather than silently rendering a 4th option.

## 6. Existing Architecture
`feature:stories` player sub-package, layered directly on top of K-03's `PlayerState` machine — overlays are rendered conditionally based on `PlayerState.ChoiceActive`/`QuizActive`, never as an independent navigation destination.

## 7. Existing Code to Reuse
- `feature/stories/player/StoryPlayerViewModel.kt` (K-03, extend with choice/quiz handling)
- `core-designsystem`: rounded card components, icon set
- `feature/stories/data/ChoiceEventRepository.kt` (new, B-05 client — created here)

## 8. Files to Create
- `feature/stories/player/ChoiceOverlay.kt`
- `feature/stories/player/QuizMomentOverlay.kt` (thin wrapper delegating actual quiz UI to the shared A.8 Daily Quiz engine component if one exists — reuse, do not fork a parallel quiz UI)
- `feature/stories/data/ChoiceEventRepository.kt` (B-05 client, offline-queue-aware)
- `feature/stories/domain/BranchResolver.kt` (deterministic client-side branch logic mirroring server logic)
- `test/feature/stories/BranchResolverTest.kt`
- `androidTest/feature/stories/ChoiceOverlayTest.kt`

## 9. Files to Modify
- `feature/stories/player/StoryPlayerViewModel.kt` (K-03) — wire `ChoiceActive`/`QuizActive` state transitions at scripted timestamps from the manifest's `interactive_script`

## 10. KMP Requirements
- `ChoiceOverlay` accepts a maximum of 3 options; a `require(options.size <= 3)` assertion fails loudly in debug builds if manifest data ever violates this (defense in depth alongside B-11's server-side cap) — release builds degrade gracefully (render only the first 3, log an error) rather than crashing in production.
- Tap-input debouncing: a `Flow`-based debounce (or equivalent) on the choice-selection callback so rapid double-taps register exactly one selection, never zero and never two.
- `BranchResolver.resolve(choicePointId, selectedOptionId)`: deterministic, purely client-side, using the same `interactive_script` branch data bundled in the manifest — playback continues immediately on selection without waiting for `ChoiceEventRepository`'s network call.
- `ChoiceEventRepository.recordChoice()`: fire-and-forget from the player's perspective; queues locally (via `core-datastore`-backed outbox, mirroring K-07's sync pattern) if offline/failed, synced later — never retried inline in a way that could stall playback.
- No countdown timer on choice moments — children may take their time; the overlay remains visible until a selection is made.

## 11. Required API
**User API** — B-05 `POST /v1/content/{id}/choice` (non-blocking, fire-and-forget).

## 12. Offline First
```
Bundled interactive_script (from manifest, downloaded or streamed)
    ↓
BranchResolver (deterministic, client-side, zero network dependency for branching itself)
    ↓
ChoiceEventRepository (queues sync-only event, never gates playback)
```

## 13. Local Data
Offline choice-event outbox (core-datastore-backed), synced on reconnect — shares the sync-on-reconnect mechanism established by K-07 rather than building a parallel one.

## 14. Localization
Choice option labels and quiz question/answer text are server-supplied, already locale-resolved; overlay chrome (e.g., any "Choose one" prompt copy) sourced from shared localization resources.

## 15. RTL
Option card layout order mirrors in Arabic/Urdu; icon + label horizontal arrangement mirrors.

## 16. Analytics
Emit `story_choice_made` (choice_id, branch_taken), `story_quiz_moment_answered` via `AnalyticsTracker`.

## 17. Performance
Overlay appearance/dismissal must not cause a frame drop on the underlying video surface — render as a Compose overlay layer above the player surface (per K-03's architecture), never pausing the render loop itself.

## 18. Security
Choice/quiz data carries no sensitive information; no new security surface beyond standard input validation (reject malformed manifest `interactive_script` data gracefully per §10).

## 19. Testing
- Unit: `BranchResolver` determinism (same input always same branch), debounce behavior (rapid double-tap → exactly one selection), 3-option-cap `require()` assertion in debug builds.
- UI: Choice Overlay never renders a 4th option even with malformed fixture data (release-build graceful-degradation path), no countdown-timer element present, quiz overlay delegates to the shared A.8 component correctly.
- Integration: offline choice event queues and syncs correctly on reconnect (shared test harness with K-07 if practical).

## 20. AI Coding Agent Implementation Steps

**Task 01 — Implement `BranchResolver`**
Objective: Deterministic client-side branch resolution from `interactive_script` data. Follow: pure-function domain-layer conventions. Tests: determinism test, malformed-data graceful handling. Definition of Done: tests pass.

**Task 02 — Implement `ChoiceEventRepository` with Offline Outbox**
Objective: Fire-and-forget B-05 client with local queue-and-sync. Follow: `core-datastore` outbox pattern (mirror K-07's approach). Tests: offline-queue-then-sync test. Definition of Done: test passes.

**Task 03 — Implement `ChoiceOverlay` Composable with 3-Option Cap**
Objective: Max-3-option rendering, debug-build `require()` assertion, release-build graceful degradation, tap debouncing, no countdown timer. Dependencies: Task 01–02. Tests: cap-enforcement test (debug and release paths), debounce test. Definition of Done: tests pass, matches PRD's exact "never silently rendering a 4th option" requirement.

**Task 04 — Implement `QuizMomentOverlay` Delegating to Shared Quiz Component**
Objective: Thin wrapper reusing the existing A.8 Daily Quiz engine UI component (confirm its exact name/location in the codebase before forking anything new). Dependencies: existing A.8 component. Tests: delegation-correctness test. Definition of Done: no duplicated quiz-rendering logic exists between A.8 and this overlay.

**Task 05 — Wire Overlay Visibility into `StoryPlayerViewModel`**
Objective: Trigger `ChoiceActive`/`QuizActive` state transitions at scripted `interactive_script` timestamps, resume `Playing` on completion. Dependencies: K-03, Task 03–04. Tests: state-transition timing test. Definition of Done: test passes.

**Task 06 — Add Analytics Instrumentation**
Objective: `story_choice_made`, `story_quiz_moment_answered`. Tests: fake-tracker assertions. Definition of Done: exactly one call site per event.

**Task 07 — Full RTL Pass**
Objective: Verify option card and icon/label mirroring. Tests: RTL snapshot tests. Definition of Done: baselines captured.

**Task 08 — Add Full Test Suite**
Objective: Complete coverage per §19. Definition of Done: all green.

**Task 09 — Final Code Review**
Objective: Confirm playback is never blocked waiting on `ChoiceEventRepository`'s network call under any code path; confirm the 3-option cap holds in both debug and release builds. Definition of Done: checklist in §21 checked.

## 21. Final Verification Checklist
- [ ] Choice Overlay never renders more than 3 options, in debug (assertion) or release (graceful truncation) builds
- [ ] Rapid double-tap registers exactly one selection, never zero or two
- [ ] Branch resolution is fully deterministic and client-side — playback never waits on the network for branching
- [ ] No countdown-timer element exists on the Choice Overlay
- [ ] Offline choice events queue locally and sync on reconnect without loss or duplication
- [ ] Quiz Moment Overlay reuses the shared A.8 quiz component, no duplicated quiz UI logic
- [ ] `story_choice_made`/`story_quiz_moment_answered` events fire correctly
- [ ] Full RTL mirroring verified

## 22. Definition of Done
Interactive choice and quiz moments render reliably within the Story Player, branch deterministically without ever blocking playback, and record durable (if non-blocking) analytics/editorial signal via B-05.
