# K-02 — Quiz Session State Management & Resume Flow

## 1. Feature Context
NoorHeroes — Feature A.8 Daily Quiz & Quiz Completion Engine. Source PRD §6.4, §7 item 2, Edge Case 12.

## 2. Parent Feature
A.8 — Daily Quiz & Quiz Completion Engine

## 3. Sub-feature
K-02 — Quiz Session State Management & Resume Flow

## 4. Objective
Implement `QuizSessionViewModel`'s sealed state machine, trusting B-03's backend-guaranteed idempotent resume rather than building separate client-side resume-detection logic — this is the behavioral core every consuming feature's quiz entry relies on.

## 5. Business Requirements
§6.4 (state machine: `Assembling → QuestionActive(index) → Submitting → ExplanationShown → (NextQuestion | RetrySet | Completed)`), Edge Case 12 (resume-after-abandonment via simple re-fetch, no separate resume detection).

## 6. Existing Architecture
Built inside `:core:quiz-engine` (K-01), following the existing MVVM/Clean Architecture ViewModel conventions (`CORE_COMMON_INSTRUCTIONS.md`, `CORE_NAVIGATION_INSTRUCTIONS.md`) and existing Repository pattern (`CORE_DATA_INSTRUCTIONS.md`).

## 7. Existing Code to Reuse
- K-01's `QuizContext`/`QuizResult` contracts
- Existing Repository interface conventions (`CORE_DATA_INSTRUCTIONS.md`)
- Existing coroutine-scoped ViewModel lifecycle pattern

## 8. Files to Create
- `core/quiz-engine/src/commonMain/kotlin/.../QuizSessionViewModel.kt`
- `core/quiz-engine/src/commonMain/kotlin/.../QuizSessionState.kt`
- `core/quiz-engine/src/commonMain/kotlin/.../QuizRepository.kt`
- `core/quiz-engine/src/commonMain/kotlin/.../QuizAnalytics.kt`
- `core/quiz-engine/src/commonTest/kotlin/.../QuizSessionStateMachineTest.kt`
- `core/quiz-engine/src/commonTest/kotlin/.../QuizResumeFlowTest.kt`

## 9. Files to Modify
- `QuizSessionScreen.kt` (K-01) — wire to `QuizSessionViewModel`

## 10. Backend Requirements
Consumes B-03 (`GET /v1/quizzes/...`, idempotent resume), B-04 (`submitResponse`), B-05 (`completeAttempt`).

## 11. KMP Requirements
- `QuizSessionViewModel` sealed state: `Assembling`, `QuestionActive(index, question)`, `Submitting`, `ExplanationShown(correct, explanation)`, `RetrySetIntro`, `Completed(accuracyPercent, reward)`
- On re-entering a quiz context with an in-progress backend attempt, the ViewModel simply re-calls the same repository fetch — **no separate client-side "is this a resume?" detection logic**, trusting the backend's idempotent response (B-03)
- `QuizRepository.startQuiz(context, childId)` → context-appropriate `GET`; `submitResponse()` → `POST .../responses`; `completeAttempt()` → `POST .../complete`
- `QuizAnalytics` fires `quiz_started` with the correct `context` sourced from the calling feature's parameter (single wrapper, no per-feature duplication)
- Coroutine cancellation on screen exit; stable/immutable state classes to avoid unnecessary recomposition

## 12. NextJS Requirements
N/A.

## 13. API Contract
Per B-03/B-04/B-05 §13.

## 14. Database Requirements
N/A directly at this layer (offline data source is K-06's concern; `QuizRepository` interface here is source-agnostic).

## 15. Validation
State transitions are compile-time-restricted to the sealed class's valid paths (no illegal transition possible, e.g. `Assembling → Completed` directly).

## 16. Authentication
Inherits child-mode bearer session via `:core:network`.

## 17. Authorization
N/A at this layer (server-enforced).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| `Assembling` fetch fails (network/server) | Transition to an error-with-retry state, never a silent stuck spinner |
| `Submitting` fails (network) | Optimistic local advance, background retry, never re-prompt an already-answered question |
| Backend returns an in-progress attempt on resume | ViewModel treats it identically to a fresh `Assembling → QuestionActive` transition at the resumed index — no special-cased resume state |
| Process death mid-session | State restored via `SavedStateHandle`, re-fetch confirms via B-03 |

## 19. Offline First
`QuizRepository` interface is source-agnostic (server vs. locally-bundled) — full offline wiring is K-06; this sub-feature defines the interface contract K-06 implements against.

## 20. Local Data
N/A directly (interface only; implementation in K-06).

## 21. Localization / 22. RTL
N/A (state layer; no UI strings here).

## 23. Analytics
`QuizAnalytics` fires `quiz_started`, `quiz_abandoned` (last_question_index), `quiz_resumed` — single shared wrapper avoiding per-feature duplicate analytics code.

## 24. Performance
Stable/immutable state classes verified via Compose stability checks; coroutine jobs scoped and cancelled on `ViewModel.onCleared()`; no main-thread blocking on state transitions.

## 25. Security
No new sensitive data handling; relies entirely on B-03/B-04/B-05's server-side authorization.

## 26. Library Requirements
Kotlin Coroutines/Flow, Hilt — existing dependencies only.

## 27. Testing
- Unit: every state transition in the sealed state machine, shared once in `:core:quiz-engine`, not duplicated per feature (signature test)
- Unit: resume flow — simulate an in-progress backend attempt on re-entry, assert ViewModel re-fetches via the same repository call with no separate resume-detection branch (signature test, Edge Case 12)
- Unit: `Submitting` failure triggers optimistic advance + background retry, never a re-prompt
- Unit: coroutine cancellation on screen exit (no leaked jobs)

## 28. Documentation
State-machine diagram and the "trust backend idempotent resume, no client-side resume detection" architectural decision documented prominently — this is a deliberate simplification other engineers might otherwise "fix" by adding redundant client logic.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Sealed State Machine**
Task ID: K-02-T01. Files to Create: `QuizSessionState.kt`. Definition of Done: sealed class compiles, illegal transitions unrepresentable.

**Task 02 — Implement QuizRepository Interface**
Task ID: K-02-T02. Files to Create: `QuizRepository.kt`. Definition of Done: interface is source-agnostic (server vs. bundled), ready for K-06 implementation.

**Task 03 — Implement QuizSessionViewModel**
Task ID: K-02-T03. Files to Create: `QuizSessionViewModel.kt`. Business Rules: no separate resume-detection logic. Tests: `QuizResumeFlowTest.kt` (signature test). Definition of Done: resume test passes.

**Task 04 — Implement QuizAnalytics Wrapper**
Task ID: K-02-T04. Files to Create: `QuizAnalytics.kt`. Definition of Done: `quiz_started` fires with correct `context` across all 4 consumers via a single shared call site.

**Task 05 — Wire ViewModel to QuizSessionScreen**
Task ID: K-02-T05. Files to Modify: `QuizSessionScreen.kt`. Definition of Done: screen renders per state without illegal-transition crashes.

**Task 06 — Add State Machine Tests**
Task ID: K-02-T06. Files to Create: `QuizSessionStateMachineTest.kt`. Definition of Done: full coverage per §27.

**Task 07 — Add Documentation**
Task ID: K-02-T07. Definition of Done: state diagram + resume-trust decision documented.

**Task 08 — Final Code Review**
Task ID: K-02-T08. Definition of Done: §31 checklist fully checked.

## 30. Definition of Done
State machine implemented and tested once for all 4 consumers; resume flow trusts backend idempotency with no redundant client logic; analytics wrapper shared, not duplicated.

## 31. Final Verification Checklist
- [ ] All sealed state transitions tested, no illegal transition representable
- [ ] Resume-after-abandonment verified via simple re-fetch, no separate client-side detection branch
- [ ] `Submitting` failure never re-prompts an already-answered question
- [ ] `QuizAnalytics` shared across all 4 consumers, no per-feature duplication
- [ ] No coroutine leaks on screen exit
