# K-04 — Mastery Result Offline Handling & Sync

## 1. Feature Context
Part of Feature A.9 (Skill Tree & Mastery Engine). Handles the case where a quiz attempt completes while the device is offline — since the Quiz Completion Result screen (K-02) requires a live server computation, this sub-feature provides the deferred, reconnect-triggered path to eventually show it.

## 2. Parent Feature
A.9 — Skill Tree & Mastery Engine

## 3. Sub-feature
K-04 — Mastery Result Offline Handling & Sync (Shared Offline Flow)

## 4. Objective
Detect offline quiz-attempt completion, show a simple "Saved! We'll show your results when you're back online" interim screen instead of attempting `QuizCompletionResultScreen`, and queue a deferred navigation to the real Result screen once connectivity returns and the attempt has synced.

## 5. Business Requirements
- A.9 PRD §6.7 Offline Support: "The Result screen itself requires connectivity (mastery computation is server-side)... offline quiz completions defer their Result screen until reconnect, showing a simpler 'saved, will show your results when you're back online' interim state instead."
- Android AI Prompt item 5: exact offline-then-reconnect-then-show-result sequence must be integration-tested.
- Consistency with A.5's AI pronunciation feedback pattern (another server-computed-feedback flow already handling this class of problem).

## 6. Existing Architecture
Kotlin, Jetpack Compose, MVVM. Reuses the platform's existing connectivity-monitoring utility (`:core:network` or `:core:common`, whichever already exposes network-state observation — reuse it, don't build a new connectivity monitor) and A.8's offline quiz-attempt queuing (A.8 KMP `06-offline-quiz-bank-sync-withdrawn-question-handling.md`, which already handles offline quiz submission generally).

## 7. Existing Code to Reuse
- A.8's offline attempt-queuing/sync mechanism — this sub-feature hooks into that existing sync completion signal rather than building a parallel offline queue specifically for mastery results.
- Existing connectivity-observer utility (`:core:network` or `:core:common`).
- K-01's `MasteryRepository`, K-02's `QuizCompletionResultScreen`.

## 8. Files to Create
- `core/mastery-engine/src/commonMain/kotlin/.../presentation/OfflineResultInterimScreen.kt`
- `core/mastery-engine/src/commonMain/kotlin/.../data/DeferredResultNavigationQueue.kt` — tracks attempt IDs awaiting result-screen display post-sync.
- `core/mastery-engine/src/androidInstrumentedTest/kotlin/.../OfflineReconnectResultFlowTest.kt`

## 9. Files to Modify
- `:feature:learn` (A.5) quiz-completion navigation logic — branch on connectivity state at completion time; route to `OfflineResultInterimScreen` instead of `QuizCompletionResultScreen` when offline.
- A.8's offline-sync completion handler — add a hook/callback that `DeferredResultNavigationQueue` can observe to trigger the deferred navigation once a queued attempt has synced.

## 10. Backend Requirements
N/A (client-side orchestration around existing B-04/B-06 endpoints, which are unaware of client connectivity state).

## 11. KMP Requirements
- **Connectivity detection at completion time:** when a quiz attempt completes, check current connectivity via the existing observer; if offline, do NOT attempt to call `MasteryRepository.getResult()` or render `QuizCompletionResultScreen` at all.
- **`OfflineResultInterimScreen`:** simple, calm "Saved! We'll show your results when you're back online" message — no error framing (this is an expected, handled state, not a failure).
- **`DeferredResultNavigationQueue`:** persists (at minimum in-memory for the current app session, ideally via a small local store surviving process death) the set of `attempt_id`s awaiting result display; on reconnect + sync-completion signal from A.8's offline-sync mechanism, triggers navigation into `QuizCompletionResultScreen` for the now-synced attempt.
- **Reconnect trigger:** observes the same connectivity signal used elsewhere in the app; on transition offline→online, checks the deferred queue and, once A.8's sync confirms the attempt is processed server-side, navigates automatically (or prompts the child gently, depending on whether the child has since navigated elsewhere in the app — a sensible UX fallback if the child is no longer on a relevant screen when sync completes).

## 12. NextJS Requirements
N/A.

## 13. API Contract
No new backend endpoints — orchestrates existing calls to B-04 (evidence, already handled by A.8's offline-sync queue) and B-06 (`GET /v1/mastery/result/{attempt_id}`, called only once connectivity + sync are both confirmed).

## 14. Database Requirements
Local-only: `DeferredResultNavigationQueue` may use a small Room table or DataStore entry to survive process death between offline-completion and reconnect (confirm against `CORE_DATASTORE_INSTRUCTIONS.md`/`CORE_DATABASE_INSTRUCTIONS.md` for the platform's preferred lightweight-persistence mechanism for this kind of transient queue).

## 15. Validation
Only attempts genuinely completed offline (not attempts that simply had a slow/failed single request while online) enter this deferred flow — distinguish "offline at completion time" from "online but request failed," which should instead use standard retry/error handling, not this offline-specific path.

## 16. Authentication
N/A (client-side orchestration; underlying calls reuse existing auth).

## 17. Authorization
N/A.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Quiz attempt completes offline | `OfflineResultInterimScreen` shown, no error state, attempt queued for deferred result display |
| Reconnect occurs but A.8's sync hasn't yet confirmed the attempt processed server-side | Deferred queue waits for the sync-completion signal, does not prematurely call `getResult()` (which would 404/error against an attempt the server hasn't processed yet) |
| Child navigates away before sync/reconnect completes | Deferred entry persists; on next app open (or next reconnect) with the entry still pending, the app can surface the result then, rather than losing it |
| Sync ultimately fails (e.g., attempt data corrupted) | Falls back to A.8's existing offline-sync failure handling (not re-solved here — this sub-feature only owns the "sync succeeded, now show the result" hop) |

## 19. Offline First
This entire sub-feature IS the offline-first handling for this specific data type (server-computed result). It correctly acknowledges that unlike `skill_node_state` (offline-viewable via K-01's cache), the Result screen's data cannot be offline-first by nature — this sub-feature manages that limitation gracefully rather than pretending it doesn't exist.

## 20. Local Data
Deferred-navigation queue entries (attempt IDs + timestamps), stored locally per §14.

## 21. Localization
"Saved! We'll show your results when you're back online" and any related copy localized EN/HI/AR/UR.

## 22. RTL
Interim screen layout mirrors correctly in RTL.

## 23. Analytics
No new dedicated event beyond the standard `quiz_result_screen_shown` (fired once the deferred result is eventually shown, same event as the online path — analytically, a deferred result-view is still a result-view, just delayed).

## 24. Performance
Connectivity check at completion time must be fast/non-blocking (reuse the existing observer's current cached state, not a fresh network probe that could itself hang).

## 25. Security
No new attack surface; deferred queue only stores non-sensitive attempt IDs.

## 26. Library Requirements
No new libraries — reuses existing connectivity-observer and local-persistence tooling already in the KMP stack.

## 27. Testing
- Integration test (Android AI Prompt item 5, mandatory): exact offline-then-reconnect-then-show-result sequence — complete an attempt offline, verify `OfflineResultInterimScreen` shown (not an error, not the real Result screen), reconnect, verify A.8's sync completes, verify automatic navigation into `QuizCompletionResultScreen` with correct data.
- Unit: `DeferredResultNavigationQueue` add/observe/clear logic.
- Unit: connectivity-check branching at completion time (offline → interim screen; online → normal Result screen).

## 28. Documentation
Document the distinction between "offline at completion" (this flow) vs. "online but request failed" (standard error/retry handling) clearly, since conflating the two would produce confusing UX.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement Connectivity-Branch at Quiz Completion**
- Task ID: K-04-T01
- Objective: Correctly detect offline-at-completion and branch navigation accordingly.
- Why This Is Required: The entry point for this entire sub-feature's logic.
- Existing Architecture to Follow: Existing connectivity-observer utility.
- Existing Files to Reuse: `:core:network`/`:core:common`'s connectivity observer.
- Files to Create: None (logic added to `:feature:learn`'s completion-handling code, or a small shared helper in `:core:mastery-engine` if a reusable branch-point makes sense across future domains).
- Files to Modify: `:feature:learn`'s quiz-completion navigation logic.
- Implementation Details: At completion, check cached connectivity state; branch to `OfflineResultInterimScreen` vs. `QuizCompletionResultScreen` accordingly.
- Business Rules: Only genuine offline-at-completion triggers this path (per §15's validation distinction).
- Validation: Per §15. Error Handling: N/A here (handled downstream).
- Security: N/A. Performance: Non-blocking connectivity check.
- Localization: N/A (this task is branching logic). RTL: N/A. Analytics: N/A.
- Tests: Unit test for the branching decision.
- Documentation: Inline comment on the online-vs-offline distinction.
- Dependencies: K-02 (Result screen exists as the online-path target).
- Do Not Change: K-02's Result screen itself.
- Expected Result: Correct branching at completion time.
- Definition of Done: Unit test green for both branches.

**Task 02 — Build OfflineResultInterimScreen**
- Task ID: K-04-T02
- Objective: Calm, non-error interim UI.
- Why This Is Required: Explicit UX requirement from A.9 PRD §6.7.
- Existing Architecture to Follow: `:core:design-system` component conventions.
- Existing Files to Reuse: Design-system typography/illustration tokens (reuse existing "saved"/success iconography if available, don't invent new visual language for a one-off screen).
- Files to Create: `OfflineResultInterimScreen.kt`.
- Files to Modify: None.
- Implementation Details: Simple message screen, no action buttons required beyond perhaps a "Continue exploring" dismiss.
- Business Rules: Never framed as an error/failure.
- Validation/Error Handling/Security/Performance: N/A.
- Localization: Full string coverage. RTL: Full mirroring.
- Analytics: N/A.
- Tests: Basic UI test (renders correctly, no error iconography).
- Documentation: KDoc.
- Dependencies: None.
- Do Not Change: N/A.
- Expected Result: Working interim screen.
- Definition of Done: UI test green in both LTR/RTL.

**Task 03 — Implement DeferredResultNavigationQueue + Reconnect Trigger**
- Task ID: K-04-T03
- Objective: Track and eventually resolve deferred result displays.
- Why This Is Required: Completes the loop — without this, offline attempts would never show their result at all.
- Existing Architecture to Follow: A.8's existing offline-sync completion signal, existing lightweight-persistence pattern.
- Existing Files to Reuse: A.8's sync-completion hook (extend, don't fork a parallel sync mechanism).
- Files to Create: `DeferredResultNavigationQueue.kt`.
- Files to Modify: A.8's offline-sync completion handler (add an observable hook).
- Implementation Details: Queue entry added on offline completion (Task 01's branch); on A.8's sync-completion signal for a queued `attempt_id`, trigger navigation to `QuizCompletionResultScreen` if the app is in a state where that's reasonable (foreground, on a relevant screen) — otherwise persist for next relevant opportunity (e.g., next app open).
- Business Rules: Per §18's error-handling table.
- Validation: N/A. Error Handling: Per §18.
- Security: N/A. Performance: Lightweight persistence, no polling loop (event/signal-driven).
- Localization: N/A. RTL: N/A.
- Analytics: `quiz_result_screen_shown` fired once the deferred result is finally displayed.
- Tests: `OfflineReconnectResultFlowTest.kt` — the full mandatory integration test per Android AI Prompt item 5.
- Documentation: KDoc explaining the queue's lifecycle.
- Dependencies: Tasks 01-02, A.8's offline-sync mechanism.
- Do Not Change: A.8's core offline-sync retry/failure logic (only hook into its completion signal).
- Expected Result: Full offline-to-result loop working.
- Definition of Done: Mandatory integration test (offline → interim → reconnect → sync → auto-navigate to real Result screen) passes.

## 30. Definition of Done
Offline quiz completions correctly show a calm interim state instead of attempting the connectivity-dependent Result screen; deferred navigation reliably resolves once reconnect + server-side sync are both confirmed, verified by the mandatory end-to-end integration test.

## 31. Final Verification Checklist
- [ ] Offline-at-completion correctly detected and branched (not conflated with "online but failed")
- [ ] `OfflineResultInterimScreen` never uses error/failure framing
- [ ] Deferred queue survives the child navigating away before reconnect
- [ ] Reconnect + A.8 sync-completion correctly triggers automatic navigation to the real Result screen
- [ ] Mandatory offline→reconnect→result integration test passing
- [ ] No duplicate/parallel offline-sync mechanism built (hooks into A.8's existing one)
- [ ] Full EN/HI/AR/UR localization + RTL on the interim screen
