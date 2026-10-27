# K-01 — Shared Quiz Engine Core Module

## 1. Feature Context
NoorHeroes — Feature A.8 Daily Quiz & Quiz Completion Engine. Source PRD §6.1–§6.3, §7 item 1.

## 2. Parent Feature
A.8 — Daily Quiz & Quiz Completion Engine

## 3. Sub-feature
K-01 — Shared Quiz Engine Core Module (`:core:quiz-engine`)

## 4. Objective
Stand up `:core:quiz-engine` as a genuinely shared core module — not a feature module — consumed by `:feature:home`, `:feature:stories`, `:feature:learn`, and `:feature:dua-learning`, establishing the `QuizContext` contract and `QuizSessionScreen` entry point every consumer will call into.

## 5. Business Requirements
FR-9 (engine embeddable/contextualized by the calling feature, single contract parameterized by count/pool, not forked per consumer); §6.1 (module boundary: core, not feature).

## 6. Existing Architecture
New core module alongside existing `:core:design-system`, `:core:network`, `:core:offline-cache`, `:core:media-player`, `:core:logger` (per `CORE_*_INSTRUCTIONS.md` set). Must not depend back on any `:feature:*` module — module-boundary discipline is a first-class requirement here since 4 features already assume this module exists (A5-K08, A6-K03, A2-K04, A3-K04 all reference the shared quiz engine).

## 7. Existing Code to Reuse
- `:core:design-system` tokens (quiz-screen skeleton styling)
- `:core:network` (Retrofit/OkHttp client conventions per `CORE_NETWORK_INSTRUCTIONS.md`)
- `:core:offline-cache` (Room conventions per `CORE_DATABASE_INSTRUCTIONS.md`)
- `:core:media-player` (audio-match question playback, K-03 dependency)
- Existing Hilt DI module registration pattern

## 8. Files to Create
- `core/quiz-engine/src/commonMain/kotlin/.../QuizContext.kt`
- `core/quiz-engine/src/commonMain/kotlin/.../QuizSessionScreen.kt`
- `core/quiz-engine/src/commonMain/kotlin/.../QuizResult.kt`
- `core/quiz-engine/src/commonMain/kotlin/.../di/QuizEngineModule.kt`
- `core/quiz-engine/build.gradle.kts`
- `core/quiz-engine/src/commonTest/kotlin/.../QuizResultContractTest.kt`
- `core/quiz-engine/src/commonTest/kotlin/.../ModuleBoundaryTest.kt`

## 9. Files to Modify
- root `settings.gradle.kts` — register `:core:quiz-engine` module
- `:feature:home`, `:feature:stories`, `:feature:learn`, `:feature:dua-learning` `build.gradle.kts` — add `:core:quiz-engine` dependency

## 10. Backend Requirements
Consumes B-03's context-parameterized delivery API (contract confirmed, not consumed directly in this module — wired in K-02).

## 11. KMP Requirements
- Public `QuizContext` enum: `HomeDaily`, `StoryPost`, `LearnPractice`, `DuaRecall`
- Single `QuizSessionScreen` composable: `(context: QuizContext, childId: String, questionCount: Int? = null, sourceId: String? = null) -> QuizResult`
- `QuizResult` data class: `accuracyPercent`, `rewardGranted`, `conceptsTouched` — returned via typed navigation result mechanism (callback or `SavedStateHandle`-backed result flow), **not** a shared mutable singleton
- Hilt DI wiring scoped to the quiz session lifecycle
- Module-boundary lint/test: `:core:quiz-engine` must not import from any `:feature:*` module

## 12. NextJS Requirements
N/A.

## 13. API Contract
Per B-03 §13 (consumed in K-02, not this module).

## 14. Database Requirements
N/A directly (scaffolding only; Room entities defined in K-06).

## 15. Validation
`questionCount`/`sourceId` are nullable and validated contextually — `sourceId` required for `StoryPost`/`LearnPractice`/`DuaRecall`, not required for `HomeDaily`.

## 16. Authentication
Inherits existing child-mode bearer session from `:core:network`.

## 17. Authorization
N/A at this module's scaffolding layer (delegated to B-03 server-side checks).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Consumer passes invalid `QuizContext`/`sourceId` combination | Compile-time-enforced where possible (sealed parameter validation); runtime `IllegalArgumentException` in debug builds only, graceful no-op entry-point suppression in release |
| Module accidentally depends on a `:feature:*` module | Build-time failure via module-boundary test/lint (Task 07) |

## 19. Offline First
N/A at this scaffolding layer (owned by K-06).

## 20. Local Data
N/A at this scaffolding layer.

## 21. Localization / 22. RTL
N/A (module contract only; no strings rendered directly by this sub-feature).

## 23. Analytics
N/A (module scaffolding; analytics wiring is K-02's `QuizAnalytics`).

## 24. Performance
Module-level: ensure `:core:quiz-engine` does not pull in unnecessary feature-module transitive dependencies (bundle-size discipline given it's linked into all 4 consumer app targets).

## 25. Security
No new sensitive data handling at this scaffolding layer.

## 26. Library Requirements
Hilt, Kotlin Coroutines, Jetpack Compose Multiplatform — existing dependency set, no new libraries introduced.

## 27. Testing
- Unit: `QuizResult` contract shape stable and correctly typed across all 4 contexts
- Build/lint: module-boundary test asserting `:core:quiz-engine` has zero `:feature:*` imports (signature test — this is the guarantee the other 3 consuming-feature blueprints already assume holds)
- Unit: `sourceId` requiredness validated per context

## 28. Documentation
Module README documenting the "shared core, not feature module" architectural decision explicitly, since 4 different feature teams (A2/A3/A5/A6) depend on this boundary being respected long-term.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Register Gradle Module**
Task ID: K-01-T01. Files to Create: `core/quiz-engine/build.gradle.kts`. Files to Modify: `settings.gradle.kts`. Definition of Done: module builds cleanly with declared dependencies only.

**Task 02 — Define QuizContext & QuizResult Contracts**
Task ID: K-01-T02. Files to Create: `QuizContext.kt`, `QuizResult.kt`. Definition of Done: contract types compile and are stable/immutable data classes.

**Task 03 — Implement QuizSessionScreen Entry Composable Stub**
Task ID: K-01-T03. Files to Create: `QuizSessionScreen.kt`. Implementation Details: entry signature only at this stage (full state machine is K-02). Definition of Done: composable accepts the documented parameters and returns `QuizResult` via typed callback.

**Task 04 — Wire Hilt DI Module**
Task ID: K-01-T04. Files to Create: `di/QuizEngineModule.kt`. Definition of Done: DI graph resolves without circular dependencies.

**Task 05 — Wire Consumer Module Dependencies**
Task ID: K-01-T05. Files to Modify: 4 `:feature:*` `build.gradle.kts` files. Definition of Done: all 4 consumers can import `:core:quiz-engine` types.

**Task 06 — Add Module-Boundary Test**
Task ID: K-01-T06. Files to Create: `ModuleBoundaryTest.kt`. Definition of Done: signature test passes, fails the build if a `:feature:*` import is introduced.

**Task 07 — Add Contract Tests**
Task ID: K-01-T07. Files to Create: `QuizResultContractTest.kt`. Definition of Done: full coverage per §27.

**Task 08 — Add Documentation**
Task ID: K-01-T08. Definition of Done: README documents the shared-core boundary decision.

**Task 09 — Final Code Review**
Task ID: K-01-T09. Definition of Done: §31 checklist fully checked.

## 30. Definition of Done
`:core:quiz-engine` module registered and buildable; `QuizContext`/`QuizResult` contracts stable; all 4 consuming feature modules wired; module-boundary test enforced in CI.

## 31. Final Verification Checklist
- [ ] `:core:quiz-engine` has zero `:feature:*` imports (module-boundary test passing)
- [ ] `QuizContext` covers all 4 required values, no forked per-feature enums
- [ ] `QuizResult` returned via typed navigation result, no shared mutable global state
- [ ] All 4 consuming feature modules successfully depend on this module
- [ ] Hilt DI graph resolves cleanly
