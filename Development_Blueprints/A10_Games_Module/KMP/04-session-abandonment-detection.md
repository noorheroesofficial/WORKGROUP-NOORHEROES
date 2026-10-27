# K-04 — Session Abandonment Detection

## 1. Feature Context
Part of **A.10 Games Module**. Covers lifecycle-based detection of a child closing the app or navigating away mid-round, ensuring zero reward/evidence is recorded for incomplete sessions (Edge Case 3, PRD §7 item 4).

## 2. Parent Feature
A.10 Games Module — KMP App (Android/iOS)

## 3. Sub-feature
**2.4 Session Abandonment Detection** `[K-04]`

## 4. Objective
Detect `GameSessionWrapper` reaching `ON_DESTROY` (or the Composable leaving composition) before a completion event has been recorded, fire `game_session_abandoned`, and explicitly avoid calling `GameSessionCompletionHandler`/`completeSession()` — verified via a lifecycle-simulation test asserting zero calls to the completion/evidence/reward path (PRD §7 item 4).

## 5. Business Requirements
- Edge Case 3: a child abandoning a session mid-round records no reward or evidence — distinct from A.8's quiz-resume pattern, a deliberate design simplification for Games (documented as such, not an oversight).
- §6.6 Analytics Mapping: abandonment detected via ViewModel lifecycle check, not requiring an explicit "I'm abandoning" signal from the child.
- FR-9: the child can simply start a new session at any time after abandonment — no special resume state to manage.

## 6. Existing Architecture
Builds directly on K-02's `GameSessionWrapper`/`GameSessionViewModel` and K-03's `GameSessionCompletionHandler`. Uses standard Compose/Android lifecycle observation (`DisposableEffect`/`ON_DESTROY` equivalent in Compose Multiplatform) combined with a ViewModel-level completion flag, consistent with the project's general pattern of lifecycle-aware state handling (no dedicated "abandonment" architecture doc exists; this follows standard KMP/Compose lifecycle idioms).

## 7. Existing Code to Reuse
- `NoorHeroesLogger` (`core-common/log`) for structured abandonment logging (with `leaveBreadcrumb` via `CrashReporter` for journey tracing, per `CORE_COMMON_INSTRUCTIONS.md` §4.2).
- `GameSessionCompletionHandler` (K-03) — this task ensures it is explicitly **not** called on abandonment.

## 8. Files to Create
```
feature/games/src/commonMain/kotlin/com/noorheroes/feature/games/session/SessionAbandonmentTracker.kt
feature/games/src/commonTest/kotlin/com/noorheroes/feature/games/session/SessionAbandonmentDetectionTest.kt
```

## 9. Files to Modify
```
feature/games/src/commonMain/kotlin/com/noorheroes/feature/games/session/GameSessionWrapper.kt    # wire lifecycle observation
feature/games/src/commonMain/kotlin/com/noorheroes/feature/games/session/GameSessionViewModel.kt  # add completion flag, onCleared() hook
```
**Do Not Change:** `GameSessionCompletionHandler`'s internal logic (K-03) — this task only ensures it is conditionally *not* invoked.

## 10. Backend Requirements
None implemented here. Consistent with B-03's design: a `game_session` row with `completed_at IS NULL` represents exactly this abandoned state — the backend never receives an explicit "abandon" signal, it simply never receives a completion call (§4.3 of B-03).

## 11. KMP Requirements
- `GameSessionViewModel` holds a `private var isCompleted: Boolean = false`, set `true` only inside the natural-completion path (K-03's success callback).
- `SessionAbandonmentTracker` observes the wrapper's lifecycle (`DisposableEffect { onDispose { ... } }` in Compose, or equivalent `ON_DESTROY` hook) and, if `isCompleted == false` at disposal, fires `game_session_abandoned` and explicitly skips any completion/evidence/reward call.
- No dedicated "abandonment" screen exists (PRD Screen Inventory item 8 — "implicit, no dedicated screen") — the child simply exits and can start a fresh session anytime (FR-9).
- Immediate replay ("Try Again") is explicitly **not** abandonment — verified as distinct from the abandonment path (it is a `GameSessionCompletionHandler`-adjacent "restart," not a lifecycle-destroy event).

## 12. NextJS Requirements
N/A.

## 13. API Contract
No API call is made on abandonment — this is the defining behavior under test. (Contrast: K-03's `completeSession()` call is the one path that must never fire here.)

## 14. Database Requirements
N/A directly; server-side reflection of abandonment is simply the absence of a completion call against the `game_session` row created at launch (B-03 §14) — no explicit "mark as abandoned" write occurs from the client.

## 15. Validation
N/A (no user input to validate in an abandonment path).

## 16. Authentication
N/A.

## 17. Authorization
N/A.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| App killed abruptly (process death) mid-round | No completion call was ever made; server-side session simply remains `completed_at IS NULL` indefinitely — acceptable per Edge Case 3's design (no cleanup job required for this table beyond standard retention, §4.5 of B-03) |
| Child navigates back mid-round via system back gesture | `ON_DESTROY`/`onDispose` fires, `game_session_abandoned` recorded, no completion call |
| Child briefly backgrounds the app then returns (not a true abandonment) | Must NOT be misdetected as abandonment — verified via a dedicated test distinguishing `ON_STOP`/backgrounding from `ON_DESTROY`/actual disposal (Android's process lifecycle nuance is explicitly tested, not assumed) |

## 19. Offline First
N/A — no network call is made on abandonment, so offline state is irrelevant to this specific path.

## 20. Local Data
N/A.

## 21. Localization
N/A — no user-facing text in the abandonment path (it's a silent, implicit state per Screen Inventory item 8).

## 22. RTL
N/A.

## 23. Analytics
`game_session_abandoned` — fired exactly once per abandoned session, with no accompanying evidence/reward events. This event, together with `game_session_completed`, must together account for 100% of started sessions with no gap (PRD §11.1: "together give a complete picture of session outcomes — no session should be unaccounted for by one or the other").

## 24. Performance
Lifecycle observation must be lightweight and not introduce any measurable overhead to the play experience — this is a passive disposal-time check, not an active polling mechanism.

## 25. Security
No security surface — this is a purely defensive correctness control ensuring no unearned reward/evidence path exists.

## 26. Library Requirements
Jetpack Compose Multiplatform (`DisposableEffect` or equivalent), Kotlinx Coroutines. No new dependencies.

## 27. Testing
- **Primary lifecycle test:** simulate `GameSessionWrapper` reaching disposal (`ON_DESTROY`/`onDispose`) before `isCompleted` is set, assert `GameSessionCompletionHandler.onSessionComplete()` (and therefore `MasteryRepository`/`RewardRepository`, transitively) receives **zero** calls (Mockito/MockK verification).
- Unit: `game_session_abandoned` analytics event fires exactly once on this path.
- Unit: natural completion path (`isCompleted = true` before disposal) does NOT fire `game_session_abandoned`.
- Unit: backgrounding (`ON_STOP`) alone, without full disposal, does NOT trigger abandonment detection (distinguishes true abandonment from a brief app-switch).
- Integration: "Try Again"/immediate replay does not trigger the abandonment path.

## 28. Documentation
KDoc explicitly documenting why this design deliberately does not support session resume (cross-referencing A.8's different quiz-resume pattern and the PRD's explicit rationale that games are short enough that restart-fresh is preferable to resume complexity).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Add Completion Flag to GameSessionViewModel**
- Objective: `private var isCompleted: Boolean = false`, set `true` only in K-03's success callback.
- Definition of Done: flag correctly reflects completion state in all test scenarios.

**Task 02 — Implement SessionAbandonmentTracker**
- Objective: Lifecycle observer firing `game_session_abandoned` and explicitly skipping completion calls when disposed with `isCompleted == false`.
- Files to Create: `SessionAbandonmentTracker.kt`.
- Definition of Done: correctly distinguishes `ON_DESTROY`/`onDispose` from `ON_STOP`/backgrounding.

**Task 03 — Wire Into GameSessionWrapper**
- Objective: Attach `DisposableEffect`/equivalent lifecycle hook at the wrapper's composition root.
- Definition of Done: primary lifecycle test (Task 05) passes.

**Task 04 — Wire Analytics Event**
- Objective: `game_session_abandoned` fired exactly once per abandoned session, no duplicate firing.
- Definition of Done: unit test confirms exactly-once firing.

**Task 05 — Add Primary Lifecycle Test**
- Objective: `SessionAbandonmentDetectionTest.kt` — Mockito/MockK zero-interaction verification on `GameSessionCompletionHandler`.
- Definition of Done: this test is treated as release-blocking, given it directly protects the platform's reward-integrity guarantee (no unearned rewards).

**Task 06 — Add Backgrounding-vs-Disposal Distinction Test**
- Objective: Confirm `ON_STOP` alone does not trigger abandonment.
- Definition of Done: test passes reliably across both Android and iOS lifecycle models (KMP cross-platform consideration).

**Task 07 — Add "Try Again" Non-Abandonment Test**
- Objective: Confirm immediate replay does not trigger the abandonment path.

**Task 08 — Add Documentation**
- Objective: KDoc on the deliberate no-resume design decision.

**Task 09 — Final Code Review**
- Objective: Confirm the abandonment path has zero code paths that could accidentally call the completion handler; confirm cross-platform (Android/iOS) lifecycle behavior parity.
- Definition of Done: review checklist (§31) fully checked.

## 30. Definition of Done
- Abandonment reliably detected via lifecycle disposal, distinct from mere backgrounding.
- Zero completion/evidence/reward calls verified on the abandonment path (primary test).
- `game_session_abandoned` fires exactly once per abandoned session.
- "Try Again" correctly excluded from the abandonment path.
- Behavior verified consistent across Android and iOS.

## 31. Final Verification Checklist
- [ ] Primary lifecycle test passing: zero completion-handler calls on abandonment
- [ ] `game_session_abandoned` fires exactly once, no duplicates
- [ ] `ON_STOP`/backgrounding correctly distinguished from true disposal/abandonment
- [ ] "Try Again"/immediate replay confirmed not to trigger abandonment path
- [ ] Behavior verified on both Android and iOS lifecycle models
- [ ] No completion, evidence, or reward network call ever fires on this path
- [ ] No files outside declared scope modified

---

## 32. Cross-Platform Dependencies
- Backend Dependency: None (no API call is ever made on this path, by design).
- KMP Dependency: K-02 (`GameSessionWrapper` lifecycle host), K-03 (`GameSessionCompletionHandler` must receive zero calls on this path).
- Admin Dependency: None.
- Database Dependency: None.
- External Service Dependency: None.
- Figma Dependency: None (PRD Screen Inventory item 8 — "implicit, no dedicated screen").
