# K-03 — Dua Recall Quiz Flow

## 1. Feature Context
NoorHeroes — Feature A.6 Dua Learning. **Major scope correction:** `A8_Daily_Quiz_Engine/KMP/01-shared-quiz-engine-core-module.md` establishes `:core:quiz-engine` as a genuinely shared module and *explicitly lists this file* ("A6-K03") as one of four consumers. Its `QuizContext.DuaRecall` enum value and `QuizSessionScreen(context, childId, questionCount?, sourceId?) -> QuizResult` composable **are already the real, intended integration point** — this file's job is to call into that shared engine correctly, not to build a parallel quiz question screen, retry state, or counter-omission logic from scratch.

## 2. Parent Feature
A.6 Dua Learning

## 3. Sub-feature
K-03 — Dua Recall Quiz Flow (thin integration with `:core:quiz-engine`)

## 4. Objective
Wire the Dua Card Detail screen's "Practice Quiz" entry point to `:core:quiz-engine`'s `QuizSessionScreen(context = QuizContext.DuaRecall, childId, sourceId = duaId)`, handle the returned `QuizResult`, and confirm (or, if missing, request as a coordination item) the engine's support for the two dua-specific PRD requirements: supportive-retry-with-full-dua-card, and "Question X of Y" omission when `total_available == 1`.

## 5. Business Requirements
FR-6, FR-7; Edge Case 8. Per `A8-K01` §11: `QuizContext` already models per-context behavior, so these two requirements are plausibly already generic engine capabilities (e.g., a per-question "review content" slot) — **confirm against the engine's actual implementation before assuming a gap exists.**

## 6. Existing Architecture
`:core:quiz-engine` (established by A8-K01), consumed alongside `:feature:home`, `:feature:stories`, `:feature:learn`. Do not add dua-specific UI logic to `:core:quiz-engine` unilaterally — per its own module-boundary rule ("must not depend back on any `:feature:*` module"), the correct extension pattern is for `:feature:dua-learning` to *pass* dua-specific content (e.g., a "review slot" composable/callback) *into* the engine's contract, not for the engine to import dua types directly. **Note:** A8-K01 documents Hilt DI ("Existing Hilt DI module registration pattern"), which conflicts with `CORE_KMP_PLAYER_INSTRUCTIONS.md`'s real Koin usage examples seen elsewhere in this codebase — this is a genuine inconsistency in the project's own documentation that should be flagged to the architecture owner rather than silently resolved one way in this file.

## 7. Existing Code to Reuse
- `:core:quiz-engine`'s `QuizContext`, `QuizSessionScreen`, `QuizResult` (A8-K01) — the entire quiz UI/flow, not reimplemented
- `DuaCardDetailScreen` (K-02) — the "full dua card" content that must resurface on an incorrect answer, if the engine exposes a slot for it

## 8. Files to Create
- `feature/dua/src/commonMain/kotlin/.../quiz/DuaQuizEntryPoint.kt` — thin wrapper invoking `QuizSessionScreen(QuizContext.DuaRecall, childId, sourceId = duaId)` and handling the `QuizResult` callback
- `feature/dua/src/commonTest/kotlin/.../DuaQuizEntryPointTest.kt`
- `feature/dua/src/androidUiTest/kotlin/.../DuaQuizGatingButtonStateTest.kt`

## 9. Files to Modify
- `DuaCardDetailScreen.kt` (K-02) — mount `DuaQuizEntryPoint`, gated on server-confirmed `learnedStatus` (not purely optimistic, per the original PRD's non-optimistic-gate requirement, which still applies regardless of which module owns the quiz UI)
- `feature/dua/build.gradle.kts` — add `:core:quiz-engine` dependency

## 10. Backend Requirements
None owned here — see B-03 for the backend-side coordination (question bank ownership, `is_learned()` gate).

## 11. KMP Requirements
- "Practice Quiz" entry button disabled/secondary-styled until `learnedStatus` reflects a **server-confirmed** learned state (K-02's `DuaCardUiState`) — this gating logic lives in `feature:dua-learning`, upstream of the engine call, since the engine itself has no knowledge of dua-specific learned-state
- On tap, invoke `QuizSessionScreen(QuizContext.DuaRecall, childId, sourceId = duaId)`
- Handle `QuizResult(accuracyPercent, rewardGranted, conceptsTouched)` on return — `rewardGranted` likely already reflects A11's reward-ledger outcome (confirm against A8-K01's actual `QuizResult` semantics), meaning K-03 does not need to independently trigger any reward/badge UI beyond what the engine's result already communicates

## 12. NextJS Requirements
N/A.

## 13. API Contract
Owned by A8/`:core:quiz-engine` — see A8-B03/A8-K01 for the authoritative contract. `total_available`/counter-omission and incorrect-answer-retry behavior are the engine's responsibility; confirm rather than reimplement (Task 01 below).

## 14. Database Requirements
N/A directly — offline question bundling is the engine's concern (its own K-06, "offline quiz bank sync") layered on top of B-15's download manifest, which already lists `content_type` including `quiz`/`dua`.

## 15. Validation
N/A directly.

## 16. Authentication / 17. Authorization
Inherited from the engine's existing child-mode session handling.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Engine reports quiz-unavailable | Whatever generic state `:core:quiz-engine` already defines for this (confirm and reuse, don't invent a dua-specific "coming soon" message that duplicates it) |
| `QuizResult` callback never fires (user backs out) | Dua Card Detail screen simply re-renders in its prior state, no special handling needed |

## 19. Offline First
Delegated to the engine's own offline-bundling mechanism (A8-KMP/06).

## 20. Local Data
N/A directly in this file.

## 21. Localization / 22. RTL
Inherited from the engine.

## 23. Analytics
`dua_recall_quiz_started`/`_passed`/etc. — confirm whether `:core:quiz-engine` already emits context-parameterized analytics events generically (likely, given it's a shared module with 4 consumers) before adding dua-specific duplicate event firing.

## 24. Performance
N/A directly.

## 25. Security
The actual `NOT_YET_LEARNED` security gate lives server-side (B-02/B-03), enforced by the engine's backend call — this file's only responsibility is not showing a falsely-enabled button before server confirmation (§11).

## 26. Library Requirements
`:core:quiz-engine` dependency only.

## 27. Testing
- Unit: Practice Quiz button gating (server-confirmed only, never purely optimistic)
- Integration: full `QuizSessionScreen(QuizContext.DuaRecall, ...)` invocation → `QuizResult` handling
- **Confirm, via reading the engine's actual implementation once built**: counter-omission at `total_available == 1`, and supportive-retry-with-full-dua-card — if either is missing from the generic engine, file a coordination request with A8 rather than forking a dua-specific quiz screen

## 28. Documentation
Record the outcome of Task 01 (engine capability confirmation) so future maintainers know whether dua-specific retry/counter behavior is generic-engine or a filed gap.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm Engine Capabilities**
Task ID: K-03-T01. Objective: once `:core:quiz-engine` is built (A8-K01 et seq.), verify it actually supports (a) omitting "Question X of Y" at `total_available == 1`, and (b) a supportive-retry state that can surface dua-specific content (e.g., a passed-in review composable/callback). Why Required: avoid forking a second quiz UI. Definition of Done: documented finding; if either capability is missing, a coordination request filed against A8 rather than building a workaround in `feature:dua-learning`.

**Task 02 — Implement Entry Point Wrapper**
Task ID: K-03-T02. Files to Create: `DuaQuizEntryPoint.kt`. Dependencies: Task 01. Definition of Done: correctly invokes `QuizSessionScreen` with `QuizContext.DuaRecall` and the dua's id as `sourceId`.

**Task 03 — Implement Server-Confirmed Gating**
Task ID: K-03-T03. Files to Modify: `DuaCardDetailScreen.kt`. Business Rules: button enabled only after server-confirmed `learnedStatus`, not purely optimistic. Definition of Done: gating test passes.

**Task 04 — Handle `QuizResult`**
Task ID: K-03-T04. Definition of Done: badge/reward UI (K-04) correctly triggered from `QuizResult.rewardGranted`, not independently re-derived.

**Task 05 — Add Tests**
Task ID: K-03-T05. Definition of Done: all §27 scenarios covered, including the engine-capability confirmation from Task 01.

**Task 06 — Add Documentation**
Task ID: K-03-T06. Definition of Done: Task 01's finding recorded.

**Task 07 — Final Code Review**
Task ID: K-03-T07. Definition of Done: §31 checklist fully checked.

## 30. Definition of Done
Dua Recall Quiz correctly launches via `:core:quiz-engine`'s shared `QuizSessionScreen`, gated on server-confirmed learned status, with `QuizResult` correctly handled; no duplicate quiz UI built.

## 31. Final Verification Checklist
- [ ] No dua-specific quiz question/retry screen built outside `:core:quiz-engine`
- [ ] `QuizContext.DuaRecall` + `sourceId=duaId` used correctly
- [ ] Practice Quiz button gated on server-confirmed state only
- [ ] Engine's counter-omission and supportive-retry capabilities confirmed (not assumed) — gap filed with A8 if missing
- [ ] `QuizResult` handled without re-deriving reward/badge state independently

## 32. Addendum — What Changed From the Original Draft
The original draft built an entire standalone quiz UI (entry prompt, question screen, incorrect-retry state, ViewModel) as if A.6 owned quiz delivery outright. The real, already-existing `A8_Daily_Quiz_Engine/KMP/01` blueprint explicitly establishes `:core:quiz-engine` as a shared module and explicitly names this file as one of its four intended consumers. This is a large scope reduction: K-03's actual remaining job is a thin integration wrapper plus confirming (not assuming) that the shared engine supports the two dua-specific PRD requirements this feature cares about.
