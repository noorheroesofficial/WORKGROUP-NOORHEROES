# Evidence Document: K-10 — Progressive Hint Overlay Implementation & Zero Missing Scenarios Verification

**Task ID**: K-10 (`10-progressive-hint-overlay`)  
**Parent Feature**: Feature A.5 — Quran & Arabic Learning  
**Author**: Sarvare Alam  
**Date**: November 11, 2026  
**Status**: Completed & Verified  

---

## 1. Executive Summary

In accordance with Feature A.5 / FR-18 / Edge Case 8 and Blueprint `Development_Blueprints/A5_Quran_Arabic_Learning/KMP/10-progressive-hint-overlay.md`, the **Progressive Hint Overlay** has been implemented, integrated, and verified within the `feature-learn` module:

1. **Zero Client-Side Content Synthesis (§11, §28)**: The overlay renders server-supplied hint text verbatim; strictly zero local content synthesis or answer reveals.
2. **Zero `hint_count` Mutation (§11)**: The overlay is strictly read-only. Calling exercise screens track their own `hint_count` and submit it in their B-03/B-04 attempt payloads, avoiding double-counting or side-effects.
3. **Progressive Hint Levels 1..3 (§11)**: Delivers step-by-step partial clues (e.g. general clue $\to$ elimination clue $\to$ focused connection) up to `max_level` without revealing the full answer (FR-18).
4. **Graceful Fallback Handling (Edge Case 8 / §18)**: When question types lack partial hints (e.g., True/False) or when network drops, delivers explanatory micro-hints via `HintCanonicalData` rendered identically to standard hints with no broken UI state.
5. **Clean State Resumption (§11)**: Dismissing the overlay returns the child seamlessly to their active exercise state with zero state loss.
6. **Child Pedagogical Safety (Rule 4 / FR-10)**: 100% gentle, encouraging tone. Verified via positive allowlists and zero occurrences of negative words (`wrong`, `fail`, `penalty`, `demote`, `error`).
7. **UX Spec Compliance (§11)**: Secondary, non-pulsing `ExerciseHintButton` that is always available but never pressures the child.
8. **4-Locale Parity**: Localized strings added across `values`, `values-ar`, `values-hi`, and `values-ur` in `strings_learn.xml`.

---

## 2. Architecture & File Inventory (Strictly < 500 Lines per File)

| Component | Path | Line Count | Status |
|---|---|---|---|
| Network Hint DTOs | `core/core-network/src/commonMain/kotlin/com/noorheroes/core/network/model/learning/LearningHintDtos.kt` | 27 lines | ✅ Verified |
| Network Learning API | `core/core-network/src/commonMain/kotlin/com/noorheroes/core/network/api/LearningApi.kt` | 258 lines | ✅ Verified |
| Domain Hint Model | `core/core-common/src/commonMain/kotlin/com/noorheroes/core/common/model/ExerciseHintModels.kt` | 26 lines | ✅ Verified |
| Canonical Hint Data | `core/core-common/src/commonMain/kotlin/com/noorheroes/core/common/model/HintCanonicalData.kt` | 89 lines | ✅ Verified |
| Learning Repository Contract | `core/core-data/src/commonMain/kotlin/com/noorheroes/core/data/repository/LearningRepository.kt` | 331 lines | ✅ Verified |
| Repository Hint Delegate | `core/core-data/src/commonMain/kotlin/com/noorheroes/core/data/repository/LearningHintDelegate.kt` | 51 lines | ✅ Verified |
| Repository Helpers | `core/core-data/src/commonMain/kotlin/com/noorheroes/core/data/repository/LearningRepositoryHelpers.kt` | 92 lines | ✅ Verified |
| Repository Implementation | `core/core-data/src/commonMain/kotlin/com/noorheroes/core/data/repository/LearningRepositoryImpl.kt` | 458 lines | ✅ Verified |
| Get Hint UseCase | `feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/domain/GetHintUseCase.kt` | 30 lines | ✅ Verified |
| Hint Overlay UI State | `feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/ui/hint/HintOverlayUiState.kt` | 52 lines | ✅ Verified |
| Hint Overlay ViewModel | `feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/ui/hint/HintOverlayViewModel.kt` | 167 lines | ✅ Verified |
| Hint Overlay Composable | `feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/ui/hint/HintOverlay.kt` | 376 lines | ✅ Verified (matches Quiz Question-02.png bottom sheet & close '✕' button) |
| UI Design Fidelity Verification | `sdocs/evidence/16-hint-overlay-ui-design-fidelity-verification.md` | 135 lines | ✅ 100% Verified |
| Koin DI Module | `feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/di/LearnModule.kt` | 240 lines | ✅ Verified |
| Unit Test Suite | `feature/feature-learn/src/commonTest/kotlin/com/noorheroes/feature/learn/ui/hint/HintOverlayViewModelTest.kt` | 213 lines | ✅ Verified |
| Zero-Missing Scenarios Suite | `feature/feature-learn/src/commonTest/kotlin/com/noorheroes/feature/learn/ui/hint/HintOverlayZeroMissingScenariosTest.kt` | 407 lines | ✅ Verified |
| Exercise Parity Test Suite | `feature/feature-learn/src/commonTest/kotlin/com/noorheroes/feature/learn/ui/hint/HintOverlayExerciseParityTest.kt` | 226 lines | ✅ Verified |
| In-Memory Test Doubles | `feature/feature-learn/src/commonTest/kotlin/com/noorheroes/feature/learn/ui/hint/HintOverlayTestFakes.kt` | 57 lines | ✅ Verified |

---

## 3. Blueprint Checklist Verification (§31)

| Blueprint §31 Verification Item | Status | Evidence / Implementation Details |
|---|---|---|
| Hint text always exactly server-provided, never client-synthesized | ✅ PASS | Verified via `scenario_005_zeroClientSynthesis_serverTextRenderedVerbatim`. Consumes verbatim DTO string. |
| `hint_count` mutation happens only in invoking screen's attempt, never in overlay | ✅ PASS | Verified via `scenario_009_invariant_hintCountNotPresentOrMutatedInViewModel` and `parity_callingScreensTrackOwnHintCount_overlayRemainsPurelyReadOnly`. |
| Fallback text renders identically to a normal hint (no broken-state UI) | ✅ PASS | Verified via `scenario_007_fallbackRendersIdenticalUiStructure`. Uses identical Composable container. |
| Dismissing overlay resumes exact prior exercise state | ✅ PASS | Verified via `scenario_010_overlayDismissal_emitsDismissEffect_preservingPriorState`, `parity_surahPractice_hintOverlayDismissal_preservesAyahIndexAndPlayback`, and `parity_dailyQuiz_hintOverlayDismissal_preservesSelectedOptionWithoutEarlySubmission`. |
| Hint control styled per UX spec (secondary, non-pulsing) | ✅ PASS | `ExerciseHintButton` styled with subtle border, surface container, small icon, and non-pulsing animation. |
| Full test suite green in CI | ✅ PASS | 10 core tests + 25 zero-missing scenario tests + 7 parity tests = 42 dedicated tests passing (318 module-wide). |

---

## 4. Design System Governance Verification (`rule.md`)

- [x] **Rule 1 — Zero Hardcoded Colors**: 100% tokenized through `NoorHeroesTheme.colors` (`primary`, `surface`, `surfaceVariant`, `textPrimary`, `textSecondary`, `borderSubtle`).
- [x] **Rule 2 — Zero Hardcoded Dimensions**: Sourced from `NoorHeroesTheme.spacing` (`space2`..`space24`) and `NoorHeroesTheme.sizes` (`iconSmall`, `iconDefault`, `touchTarget`, `borderThin`, `borderMedium`).
- [x] **Rule 3 — Zero Hardcoded Typography**: Sourced from `NoorHeroesTheme.typography` (`h2`, `bodyMedium`, `bodyLarge`, `labelSmall`).
- [x] **Rule 4 — Child Pedagogical Safety**: Supportive tone, lightbulb accent, zero negative evaluation words.
- [x] **Rule 5 — Canonical UI Primitives**: Built with `NoorCustomDialog`, `NoorCard`, `PrimaryButton`, `SecondaryButton`.
- [x] **Rule 6 — 100% Localization**: Localized across English, Arabic, Hindi, Urdu in `strings_learn.xml`.
- [x] **Rule 7 — Pure Multiplatform Layering**: Pure KMP models and state machines without UI dependencies.
- [x] **Rule 8 — File Modularity**: 100% of files strictly $< 500$ lines.

---

## 5. Test Execution Evidence

```
> Task :core:core-data:testAndroidHostTest UP-TO-DATE
> Task :feature:feature-learn:compileAndroidHostTest
> Task :feature:feature-learn:testAndroidHostTest

BUILD SUCCESSFUL in 41s
113 actionable tasks: 16 executed, 97 up-to-date
Configuration cache entry reused.
Total Feature Tests Executed: 318 passed, 0 failed, 0 skipped
```

---

## 6. Comprehensive Zero-Missing Scenario Matrix (S-A05-K10-001..025)

| Scenario ID | Test Name | Invariant / Requirement Verified | Status |
|---|---|---|---|
| **S-A05-K10-001** | `scenario_001_initialHintLoad_setsLevelOneAndActiveClue` | Initial load fetches Level 1 partial clue and sets question ID | ✅ PASS |
| **S-A05-K10-002** | `scenario_002_progressionFromLevelOneToLevelTwo` | Advancing to Level 2 fetches deeper partial clue | ✅ PASS |
| **S-A05-K10-003** | `scenario_003_progressionToMaxLevelThree_disablesNextAction` | Max level 3 disables `canRequestNextLevel` ("Need More Help?" CTA disappears) | ✅ PASS |
| **S-A05-K10-004** | `scenario_004_capper_requestPastMaxLevelDoesNotIncrement` | Level capper guards against calls when `hintLevel >= maxLevel` | ✅ PASS |
| **S-A05-K10-005** | `scenario_005_zeroClientSynthesis_serverTextRenderedVerbatim` | Zero client synthesis: server-provided clue rendered 100% verbatim | ✅ PASS |
| **S-A05-K10-006** | `scenario_006_edgeCase8_questionsWithoutPartialHint_fallbackToMicroHint` | Edge Case 8: Questions without partial hints deliver canonical micro-hints | ✅ PASS |
| **S-A05-K10-007** | `scenario_007_fallbackRendersIdenticalUiStructure` | Fallback micro-hints render identically to standard hints with no broken UI | ✅ PASS |
| **S-A05-K10-008** | `scenario_008_telemetry_hintRequestedEmittedWithParameters` | Analytics `hint_requested` event logged with `question_id`, `hint_level`, `max_level` | ✅ PASS |
| **S-A05-K10-009** | `scenario_009_invariant_hintCountNotPresentOrMutatedInViewModel` | Blueprint §11/§27: No `hint_count` state or mutation exists in ViewModel | ✅ PASS |
| **S-A05-K10-010** | `scenario_010_overlayDismissal_emitsDismissEffect_preservingPriorState` | Dismiss emits `DismissOverlay` effect, resuming exercise state without state loss | ✅ PASS |
| **S-A05-K10-011** | `scenario_011_childSafety_zeroNegativeBlockwordsInCanonicalHints` | Rule 4 / FR-10: 0 negative evaluation words across all canonical hints | ✅ PASS |
| **S-A05-K10-012** | `scenario_012_offlineResilience_deliversCanonicalHintSmoothly` | Offline mode smoothly falls back to canonical hints for active question | ✅ PASS |
| **S-A05-K10-013** | `scenario_013_localeForwarding_passedToRepository` | Child's active locale forwarded faithfully to repository and API | ✅ PASS |
| **S-A05-K10-014** | `scenario_014_boundary_blankQuestionId_safelyResolves` | Blank or whitespace question ID sanitized safely without crashing | ✅ PASS |
| **S-A05-K10-015** | `scenario_015_boundary_levelClamping_outOfRangeLevelsCoerced` | Negative or > 3 levels coerced strictly to valid [1, 3] range | ✅ PASS |
| **S-A05-K10-016** | `scenario_016_fr18_hintsNeverRevealFullAnswer` | FR-18: Clues remain partial; full answers never disclosed | ✅ PASS |
| **S-A05-K10-017** | `scenario_017_rapidClicks_doesNotTriggerMultipleSimultaneousRequests` | Rapid multi-clicking throttled; in-flight request blocks duplicate dispatches | ✅ PASS |
| **S-A05-K10-018** | `scenario_018_uiState_levelIndicatorFormattedCorrectly` | Level indicator string formatted ("Hint 1 of 3", "Hint 2 of 3", etc.) | ✅ PASS |
| **S-A05-K10-019** | `scenario_019_edgeCase8_maxLevelOne_immediatelyDisablesNextButton` | Questions with `maxLevel = 1` disable next button immediately at Level 1 | ✅ PASS |
| **S-A05-K10-020** | `scenario_020_fr10_rule4_zeroScoresOrPenaltiesInUiState` | Rule 4 / FR-10: State model contains zero score/grade/penalty fields | ✅ PASS |
| **S-A05-K10-021** | `scenario_021_networkFailure_handlesDegradationSafely` | Transport/network failures cleanly set safe error without crashing | ✅ PASS |
| **S-A05-K10-022** | `scenario_022_unknownQuestionId_gracefullyFallbackWithoutException` | Unmapped question IDs fall back cleanly to general encouragement | ✅ PASS |
| **S-A05-K10-023** | `scenario_023_repeatedDismissCalls_idempotentAndSafe` | Repeated or rapid dismiss calls are idempotent and non-throwing | ✅ PASS |
| **S-A05-K10-024** | `scenario_024_getHintUseCase_clampingAndSanitization` | Domain UseCase sanitizes inputs and clamps levels before repository call | ✅ PASS |
| **S-A05-K10-025** | `scenario_025_canonicalData_coverageForCurriculumExercises` | Canonical coverage verified across Quran, Tajweed, Letters, and Games | ✅ PASS |

---

## 7. Cross-Exercise State-Preservation Parity Matrix (HintOverlayExerciseParityTest)

| Parity Test ID | Test Method Name | Exercise Flow | Verified Invariant | Status |
|---|---|---|---|---|
| **P-A05-K10-001** | `parity_dailyQuiz_hintOverlayDismissal_preservesSelectedOptionWithoutEarlySubmission` | Daily Quiz (`DailyQuizQuestionScreen`) | Dismissing hint overlay leaves child's selected option intact with `isAnswerSubmitted = false` | ✅ PASS |
| **P-A05-K10-002** | `parity_surahPractice_hintOverlayDismissal_preservesAyahIndexAndPlayback` | Surah Practice (`SurahLearningScreen`) | Dismissing hint overlay preserves `activeAyahIndex`, `isTransliterationOn`, and `playbackSpeed` | ✅ PASS |
| **P-A05-K10-003** | `parity_arabicLetters_hintOverlayDismissal_preservesStageAndTracingProgress` | Arabic Letters (`ArabicLettersLearningFlowScreen`) | Dismissing hint overlay leaves active stage, completed stages, and strokes intact | ✅ PASS |
| **P-A05-K10-004** | `parity_tajweedRules_hintOverlayDismissal_preservesSequentialStep` | Tajweed (`TajweedLearningFlowScreen`) | Dismissing hint overlay preserves step sequence, listen speed, and identification state | ✅ PASS |
| **P-A05-K10-005** | `parity_quranGame_hintOverlayDismissal_preservesActiveTimerAndScore` | Quran Games (`QuranGameFlowScreen`) | Dismissing hint overlay preserves active game timer and streak count | ✅ PASS |
| **P-A05-K10-006** | `parity_callingScreensTrackOwnHintCount_overlayRemainsPurelyReadOnly` | All Exercises | Invoking screens maintain and submit their own `hint_count`; overlay performs 0 mutation | ✅ PASS |
| **P-A05-K10-007** | `parity_offlineFallback_rendersIdenticalCardHierarchy` | Offline Fallback | Fallback card hierarchy, typography, and dismiss behavior match online state | ✅ PASS |

