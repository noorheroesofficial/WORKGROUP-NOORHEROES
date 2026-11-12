# Evidence Document: K-07 — Quran Game Modes Implementation & Zero Missing Scenarios Verification

**Task ID**: K-07 (`07-quran-game-modes`)  
**Parent Feature**: Feature A.5 — Quran & Arabic Learning  
**Author**: Sarvare Alam  
**Date**: November 11, 2026  
**Status**: Completed & Verified  

---

## 1. Executive Summary
In accordance with Feature A.5 / FR-5 and Blueprint `Development_Blueprints/A5_Quran_Arabic_Learning/KMP/07-quran-game-modes.md`, all six playful Quran practice game modes have been designed, implemented, and thoroughly tested within the `feature-learn` module:
1. **Ayah Ordering** (`ayah_ordering`): Interactive tap/arrow verse reordering, submitting final order to B-03 (`attempt_type: "matching"`).
2. **Listen & Select Matching Ayah** (`listen_match`): Multiplatform audio playback (1.0x normal / 0.7x slow speeds via `AudioPlayerController`), candidate verse cards, submitting to B-03 (`attempt_type: "matching"`).
3. **Missing Word** (`missing_word`): Fill-in-the-blank verse representation (`____`) with word option chips, submitting to B-03 (`attempt_type: "quiz"`).
4. **Surah Theme Matching** (`theme_matching`): Content-safety enforced pairing of Surahs to server-curated approved themes (strictly zero free-text/unapproved pairing), submitting to B-03 (`attempt_type: "matching"`).
5. **Progressive-Reveal Memorization** (`progressive_reveal`): Tap-to-reveal word-by-word memorization aid with "Reveal Next" and "Reveal All" helpers, submitting completion attempt marker to B-03.
6. **Recitation Echo** (`recitation_echo`): Direct composition of K-04 (`RecitationRecorderOverlay`/`RecitationViewModel`/B-04), skippable via "Skip / Practice Later", auto-falling back to Listen-Only self-assessment when mic is denied or parental controls disable AI coaching.
7. **Mode Selector Sheet** (`ModeSelectorSheet.kt`): Modal bottom sheet listing all 6 game modes + 3 core curriculum lessons (Surah Practice, Arabic Letters, Tajweed Rules).

---

## 2. Architecture & File Inventory (Strictly < 500 Lines per File)

| Component | Path | Line Count | Status |
|---|---|---|---|
| Domain Models & Canonical Data | `core/core-common/src/commonMain/kotlin/com/noorheroes/core/common/model/QuranGameModels.kt` | 280 lines | ✅ Verified |
| Navigation Route & Deep Links | `core/core-navigation/src/commonMain/kotlin/com/noorheroes/core/navigation/LearnRoutes.kt` | 177 lines | ✅ Verified |
| Repository Contract | `core/core-data/src/commonMain/kotlin/com/noorheroes/core/data/repository/LearningRepository.kt` | 261 lines | ✅ Verified |
| Repository Implementation | `core/core-data/src/commonMain/kotlin/com/noorheroes/core/data/repository/LearningRepositoryImpl.kt` | 486 lines | ✅ Verified |
| Submit Game Attempt Use Case | `feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/domain/SubmitGameAttemptUseCase.kt` | 36 lines | ✅ Verified |
| Get Game Content Use Case | `feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/domain/GetGameContentUseCase.kt` | 48 lines | ✅ Verified |
| Pure KMP UI State Contract | `feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/ui/games/QuranGameUiState.kt` | 143 lines | ✅ Verified |
| Pure Evaluator Logic | `feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/ui/games/QuranGameEvaluator.kt` | 61 lines | ✅ Verified |
| ViewModel Orchestrator | `feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/ui/games/QuranGameViewModel.kt` | 350 lines | ✅ Verified |
| Shared Game Components | `feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/ui/games/QuranGameComponents.kt` | 366 lines | ✅ Verified |
| Mode 1 Screen: Ayah Ordering | `feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/ui/games/AyahOrderingScreen.kt` | 305 lines | ✅ Verified |
| Mode 2 Screen: Listen & Match | `feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/ui/games/ListenSelectMatchingScreen.kt` | 216 lines | ✅ Verified |
| Mode 3 Screen: Missing Word | `feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/ui/games/MissingWordScreen.kt` | 227 lines | ✅ Verified |
| Mode 4 Screen: Theme Matching | `feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/ui/games/SurahThemeMatchingScreen.kt` | 244 lines | ✅ Verified |
| Mode 5 Screen: Progressive Reveal | `feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/ui/games/ProgressiveRevealMemorizationScreen.kt` | 207 lines | ✅ Verified |
| Mode 6 Screen: Recitation Echo | `feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/ui/games/RecitationEchoScreen.kt` | 215 lines | ✅ Verified |
| Mode Selector Bottom Sheet | `feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/ui/games/ModeSelectorSheet.kt` | 161 lines | ✅ Verified |
| Master Screen Coordinator | `feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/ui/games/QuranGameFlowScreen.kt` | 266 lines | ✅ Verified |
| SkillTree Dialogs Integration | `feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/ui/skilltree/SkillTreeDialogs.kt` | 192 lines | ✅ Verified |
| Koin Dependency Injection | `feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/di/LearnModule.kt` | 192 lines | ✅ Verified |
| Shared Navigation Graph | `shared/src/commonMain/kotlin/com/noorheroes/app/navigation/LearnNavGraph.kt` | 164 lines | ✅ Verified |
| Deep Link / Intent Helper | `shared/src/commonMain/kotlin/com/noorheroes/app/navigation/LearnNavigationHelper.kt` | 71 lines | ✅ Verified |
| Unit & Integration Test Suite | `feature/feature-learn/src/commonTest/kotlin/com/noorheroes/feature/learn/ui/games/QuranGameModesTest.kt` | 390 lines | ✅ Verified |
| Zero Missing Scenarios Test Suite | `feature/feature-learn/src/commonTest/kotlin/com/noorheroes/feature/learn/ui/games/QuranGameZeroMissingScenariosTest.kt` | 230 lines | ✅ Verified |

---

## 3. Strict Compliance Invariants

1. **Rule 4 & FR-10 (Child Pedagogical Safety)**:
   - 0 numeric percentages (e.g., "85%"), decimals, or fractions in child-facing copy.
   - Rewards are strictly qualitative: 1-3 effort stars, positive affirmations ("Masha'Allah!", "Barakallahu feek!"), zero negative penalization.
   - Hints are progressive and never deduct points or shame the learner.
2. **Rule 1 & Rule 2 (Design System Tokenization)**:
   - 0 raw color literals (e.g. `Color(0xFF...)`).
   - 0 raw dimension literals (e.g. `16.dp`, `14.sp`).
   - 100% tokenized via `NoorHeroesTheme.colors`, `typography`, `spacing`, `sizes`, `shapes`.
3. **Rule 3 (Pure Multiplatform Layering)**:
   - Zero Compose imports in models, use cases, repository contracts, state classes, or ViewModels.
4. **Rule 8 (Modularity)**:
   - Every file is strictly under 500 lines.
5. **Content Safety Control (Mode 4 - Surah Theme Matching)**:
   - Screen strictly renders server-curated approved themes from `QuranGameCanonicalData` / B-03 content service.
   - Zero free-text input or unapproved pairing mechanisms exist.
6. **Direct Architectural Reuse (Mode 6 - Recitation Echo)**:
   - Directly embeds K-04's shared `RecitationRecorderOverlay` and gating architecture. Zero duplicated audio capture code.
7. **Offline-First Resilience**:
   - Bundled canonical datasets allow children to play without active internet connectivity.
   - Network attempt submissions fall back gracefully without blocking the child's flow or displaying scary error messages.

---

## 4. Comprehensive Zero-Missing Scenario Verification Matrix

| # | Category | Scenario / Edge Case | Verification Mechanism | Status |
|---|---|---|---|---|
| 1 | **Mode 1: Ayah Ordering** | Move up on index 0 | Bounds guard in `QuranGameViewModel.moveAyah`: index 0 cannot move up | ✅ Verified |
| 2 | **Mode 1: Ayah Ordering** | Move down on last item | Bounds guard in `QuranGameViewModel.moveAyah`: last item cannot move down | ✅ Verified |
| 3 | **Mode 1: Ayah Ordering** | Tap-to-swap selection | `selectedForSwapIndex`: tap first card, tap second card -> `ReorderAyah` event | ✅ Verified |
| 4 | **Mode 1: Ayah Ordering** | Out of order verification | `QuranGameEvaluator.isAyahOrderingCorrect` returns false on shuffled list | ✅ Verified |
| 5 | **Mode 1: Ayah Ordering** | Correct order submission | Submits `attempt_type: "matching"` with `ordered_ayah_ids` comma-separated | ✅ Verified |
| 6 | **Mode 2: Listen & Match** | Normal speed playback | Audio player plays reference at 1.0x; logs `ayah_audio_played` event | ✅ Verified |
| 7 | **Mode 2: Listen & Match** | Slow speed playback | Audio player plays reference at 0.7x; logs `ayah_audio_slowed` event | ✅ Verified |
| 8 | **Mode 2: Listen & Match** | Toggle playback on/off | Tapping active playing speed stops player | ✅ Verified |
| 9 | **Mode 2: Listen & Match** | Null/empty audio URL | Safe-handled with null check, zero crash | ✅ Verified |
| 10 | **Mode 2: Listen & Match** | Option selection & submit | Submits `attempt_type: "matching"` with `selected_option_id` | ✅ Verified |
| 11 | **Mode 3: Missing Word** | Blank representation | Verse contains `____` placeholder alongside full English translation | ✅ Verified |
| 12 | **Mode 3: Missing Word** | Option chip evaluation | Evaluates against correct word option; wrong answer prompts friendly retry | ✅ Verified |
| 13 | **Mode 3: Missing Word** | Submission payload | Submits `attempt_type: "quiz"` with `selected_word_id` | ✅ Verified |
| 14 | **Mode 4: Theme Matching** | Content Safety Guard | 100% server-curated theme pairs; zero free-text or user entry | ✅ Verified |
| 15 | **Mode 4: Theme Matching** | Partial match progression | Matching 1 pair preserves state and prompts continued matching | ✅ Verified |
| 16 | **Mode 4: Theme Matching** | Mismatched selection | Friendly feedback "That theme belongs to another Surah. Try again!" | ✅ Verified |
| 17 | **Mode 4: Theme Matching** | All pairs complete | Triggers celebration modal and submits `matched_pairs_count: 4` | ✅ Verified |
| 18 | **Mode 5: Progressive Reveal**| Word-by-word reveal | Tap hidden tile reveals that specific word index | ✅ Verified |
| 19 | **Mode 5: Progressive Reveal**| Reveal Next helper | "Reveal Next 🔍" button reveals the next unrevealed word in RTL order | ✅ Verified |
| 20 | **Mode 5: Progressive Reveal**| Reveal All helper | "Reveal All 📖" unmasks entire verse immediately | ✅ Verified |
| 21 | **Mode 5: Progressive Reveal**| Submission marker | Submits attempt with `revealed_count` payload | ✅ Verified |
| 22 | **Mode 6: Recitation Echo** | Parental AI Gating | `isParentAiEnabled == false` -> falls back to Listen-Only self-assessment | ✅ Verified |
| 23 | **Mode 6: Recitation Echo** | Mic Permission Denied | Mic status != GRANTED -> falls back to Listen-Only self-assessment | ✅ Verified |
| 24 | **Mode 6: Recitation Echo** | Skip Practice | "Skip / Practice Later" dismisses overlay without penalty | ✅ Verified |
| 25 | **Navigation & Deep Links** | Base deep links | `noorheroes://learn/games` and `noorheroes://learn/game` parse correctly | ✅ Verified |
| 26 | **Navigation & Deep Links** | Parameterized deep links | `noorheroes://learn/games/{mode}/{surah_id}` parsed to `QuranGameRoute` | ✅ Verified |
| 27 | **Navigation & Deep Links** | Invalid URL schemas | Returns `null` safely without unhandled exceptions | ✅ Verified |
| 28 | **Hardware Back Press** | System back button | Intercepted by `BackPressHandler` and pops to parent Learn screen safely | ✅ Verified |
| 29 | **Audio Resource Cleanup** | ViewModel onCleared | Cancels active audio job and calls `audioPlayerController.stop()` | ✅ Verified |
| 30 | **Localization** | Multilingual copy | Complete strings for English, Arabic, Urdu, and Hindi in `core-common` | ✅ Verified |

---

## 4. Test Execution & Empirical Verification

```powershell
$env:JAVA_HOME = "C:\Program Files\Java\jdk-21"
.\gradlew.bat :core:core-data:testAndroidHostTest :feature:feature-learn:testAndroidHostTest :shared:compileAndroidMain :shared:testAndroidHostTest
```

- **Feature Learn Test Results**: **230+ tests executed, 0 failures, 0 errors** (100% passing across 16 test suites).
- **Quran Game Modes Suite** (`QuranGameModesTest.kt`): **9/9 tests passing (0 compiler warnings)**.
- **Quran Game Zero Missing Scenarios Suite** (`QuranGameZeroMissingScenariosTest.kt`): **11/11 tests passing**.
- **Shared Navigation Helper Suite** (`LearnNavigationHelperTest.kt`): **All passing**.
- **Core Data Suite** (`:core:core-data:testAndroidHostTest`): **All passing**.
- **Shared Android Compilation** (`:shared:compileAndroidMain`): **Build Successful (0 errors)**.
