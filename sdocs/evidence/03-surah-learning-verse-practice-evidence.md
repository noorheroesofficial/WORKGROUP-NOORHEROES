# Evidence: Surah Learning Verse Practice Flow (Task K-03 / Feature A.5)

**Task**: `03-surah-learning-verse-practice`  
**Parent PRD**: `PRD_Documents/Child App (1-12)/Feature_A5_Quran_Arabic_Learning.md`  
**Task Blueprint**: `Development_Blueprints/A5_Quran_Arabic_Learning/KMP/03-surah-learning-verse-practice.md`  
**Backend Alignment**: `NoorHeroes-Backend` API contracts (`GET /v1/learning/surah/{surahId}`, `POST /v1/learning/attempts`, `POST /v1/learning/recitation`)  
**Design Reference Mockups**:
- `Screens/Mobile App/Learn/Surah Practice-01.png` (Top bar, Surah title, transliteration toggle, Tajweed note card, active ayah card with green highlight border, play/record controls)
- `Screens/Mobile App/Learn/Surah Practice-02.png` (Second verse active state, slow audio 0.7x toggle, progressive articulation hint dialog)
- `Screens/Mobile App/Learn/Feedback.png` (AI Pronunciation Coaching modal: decorative waveform, supportive coaching feedback card, progress trend indicator, primary/secondary action CTAs)  
**Date**: 2026-11-10  
**Status**: AUDITED, TESTED & PASSING (`344 ACTIONABLE GRADLE TASKS`, 100% GREEN ACROSS ALL 10 MODULES; `0` STATIC AUDIT VIOLATIONS)

---

## 1. Key Implementation & Architectural Deliverables

1. **Visual Design & Typography Parity (`Surah Practice-01.png`, `Surah Practice-02.png`, `Feedback.png`)**:
   - **Ayah Card (`SurahAyahCard.kt` — 428 lines)**: Active card highlighted with green border (`colors.primary`, `sizes.borderMedium`), circular warm gold ayah number badge (`colors.accentContainer` / `colors.accent`), authoritative Uthmani typography with full diacritics (`typography.quranText`), phonetically verified transliteration (`typography.bodyMedium`), English translation, inline audio play/pause button with playing state border, 0.7x slow-play toggle pill (`surah_speed_slow` / `surah_speed_normal`), and recitation record button (`primary` -> `errorSurface` recording state with pulsing indicator), subtle Hint button and green Done button.
   - **Top Bar & Context Cards (`SurahTajweedAndStatusCards.kt` — 284 lines)**: Top navigation bar with back arrow and title, independent transliteration toggle pill (`surah_transliteration_toggle`), independent translation toggle pill (`surah_translation_toggle`), contextual warm-gold Tajweed rule note card (`surah_tajweed_note_title`), and listen-only banner (`surah_listen_only_mode`).
   - **AI Pronunciation Coaching Modal (`SurahFeedbackScreen.kt` — 363 lines)**: Renders decorative recitation waveform, encouraging feedback card (`Well done, [childName]!`), supportive trend indicator (`Getting closer each time`), self-assessment reference audio comparison prompt when `fallbackToReference == true`, and continuation CTAs (`Continue >`, `↺ Try Again`) adhering strictly to Rule 4 (zero pass/fail binary, zero religious judgment).
   - **Progressive Hint Overlay (`SurahHintDialog.kt` — 35 lines)**: Modal dialog displaying non-punitive articulation guidance with `PrimaryButton` dismiss action.
   - **Screen Scaffold (`SurahLearningScreen.kt` — 303 lines)**: Main container with `BackPressHandler`, explicit AI processing dialog overlay (`isAiProcessing`), offline cache notice banner (`isOffline`), load error retry state, `NoorBanner` retry on audio failure, `CircularProgressIndicator` on initial load, and full MVI state binding.

2. **Multiplatform Audio Player & Speed Control (`kmpplayer`)**:
   - Added `implementation(project(":library:kmpplayer"))` to `feature:feature-learn:build.gradle.kts`.
   - Wired `AudioPlayerController` in `SurahLearningViewModel` for playback of high-bitrate MP3/WAV verse audio from canonical CDN or offline cache.
   - Supports 0.7x slow-speed toggle (`setPlaybackSpeed(0.7f)`) enabling children to hear articulation at reduced pace without pitch distortion.

3. **FastAPI Endpoints, DTOs & Dual Wire Parity (`core-common`, `core-network`)**:
   - Extended `HttpEndpoints.Learning`: added `ATTEMPTS`, `RECITATION`, `HINTS`, `SURAH_CONTENT`.
   - Implemented `SurahPracticeDtos.kt`: `SurahContentDto`, `AyahItemDto`, `TajweedNoteDto`, `LearningAttemptRequestDto`, `LearningAttemptResponseDto`, and `RecitationResponseDto` supporting dual camelCase and snake_case deserialization without default-value masking bugs.
   - Added `getSurahContent`, `submitAttempt`, and `submitRecitation` to `LearningApi` and verified contract with `SurahLearningBackendParityContractTest`.

4. **Domain Layer & Canonical Offline Content (`core-data`, `feature-learn`)**:
   - Created `QuranContentCanonicalData.kt` with authoritative Uthmani text, transliteration, and translation for Surah Al-Asr (Surah 103) as offline fallback.
   - Extended `LearningRepository` and `LearningRepositoryImpl` to provide offline-first data fetching and attempt telemetry submissions.
   - Created `GetSurahContentUseCase`, `SubmitAyahPracticedUseCase`, and `SubmitRecitationAttemptUseCase`.

5. **Navigation & Deep Linking (`core-navigation`, `shared`)**:
   - Defined `SurahLearningRoute(surahId: String = "103")` in `LearnRoutes.kt` with deep link support (`/surah/`).
   - Registered destination in `LearnNavGraph.kt` and wired `onNavigateToNode` to route verse practice directly from the skill tree map.

---

## 2. Design System, Layer Purity & File Line Count Audit (`rule.md`)

Static audit executed across all 108 changed and untracked files (`scratch/recheck_zero_gaps.py`, exit code `0`, `0` violations):

| Rule | Requirement | Audited Metric | Result |
| :--- | :--- | :---: | :---: |
| **Rule 1 (Zero Raw Literals)** | No `Color(0x...)`, `Color.*`, `PrimitiveColors.*`, `.dp`, `.sp`, `RoundedCornerShape`, `CircleShape`, or unstyled Material `Card`/`Button`/`AlertDialog` imports in feature UI | `0` violations across 108 files | **100% COMPLIANT** |
| **Rule 2 (4-Locale + Format Parity)** | Equal string key sets & `%1$d`/`%1$s` format placeholders across `values`, `values-ar`, `values-hi`, `values-ur` | `144/144` unique keys + identical placeholders | **100% COMPLIANT** |
| **Rule 3 (Pure Architecture Layers)** | Zero `androidx.compose.*` or `core.designsystem.*` imports in DTO, API, Repository, UseCase, ViewModel, Navigation routes | `0` violations across pure layers | **100% COMPLIANT** |
| **Rule 4 (Child-Safe Feedback)** | Zero religious judgment, zero binary pass/fail grades, non-punitive supportive feedback | Verified in `SurahFeedbackScreen.kt` & tests | **100% COMPLIANT** |
| **Rule 5 (Touch Targets & A11y)** | $\ge 48\text{dp}$ touch targets, `Role.Button`, content descriptions, RTL-safe Material icons, `BackPressHandler` | Verified across all UI composables | **100% COMPLIANT** |
| **Rule 8 (File Line Ceiling)** | Every touched/created file strictly $< 500$ lines | Max file: `OnboardingNavGraph.kt` (`494` lines); Surah max: `SurahAyahCard.kt` (`428` lines); ViewModel max: `SurahLearningViewModel.kt` (`430` lines) | **100% COMPLIANT** |
| **Protected Directories** | Zero edits in `PRD_Documents/`, `Development_Blueprints/`, `Screens/`, `NoorHeroes/docs/prompt-kmp.md` | `0` modified/deleted/created | **100% COMPLIANT** |

---

## 3. Empirical Verification Suite & Results

### Multi-Module Gradle Test Execution:
```powershell
$env:JAVA_HOME = 'C:\Program Files\Java\jdk-21'
Set-Location 'c:\Users\Sarva\Documents\WORKGROUP-NOORHEROES\NoorHeroes'
.\gradlew.bat :core:core-common:testAndroidHostTest :core:core-designsystem:testAndroidHostTest :core:core-database:testAndroidHostTest :core:core-network:testAndroidHostTest :core:core-data:testAndroidHostTest :core:core-ui:testAndroidHostTest :core:core-navigation:testAndroidHostTest :feature:feature-learn:testAndroidHostTest :shared:testAndroidHostTest :androidApp:compileDevDebugKotlin :androidApp:testDevDebugUnitTest --console=plain
```

### Result:
- **Build Status**: `BUILD SUCCESSFUL in 1m 27s`
- **Actionable Tasks**: `344 actionable tasks: 58 executed, 286 up-to-date`
- **Failures / Errors**: `0`
- **Test Modules Passing**:
  - `:core:core-common:testAndroidHostTest` — PASSED
  - `:core:core-designsystem:testAndroidHostTest` — PASSED
  - `:core:core-database:testAndroidHostTest` — PASSED
  - `:core:core-network:testAndroidHostTest` — PASSED (includes `SurahLearningBackendParityContractTest`)
  - `:core:core-data:testAndroidHostTest` — PASSED (includes `LearningRepositoryImplTest`)
  - `:core:core-ui:testAndroidHostTest` — PASSED
  - `:core:core-navigation:testAndroidHostTest` — PASSED
  - `:feature:feature-learn:testAndroidHostTest` — PASSED (includes `SurahLearningViewModelTest` & `SurahLearningZeroMissingScenariosTest` with 21 exhaustive edge case suites)
  - `:shared:testAndroidHostTest` — PASSED
  - `:androidApp:compileDevDebugKotlin` & `:androidApp:testDevDebugUnitTest` — PASSED

---

## 4. Comprehensive Zero-Missing Scenario Verification Matrix

| Scenario Index | Test Method Name | Verified Edge Condition |
| :---: | :--- | :--- |
| **001** | `scenario_001_initialSurahLoad_successful` | Authoritative Uthmani text, transliteration, Tajweed notes, first ayah active |
| **002** | `scenario_002_transliterationTogglePersistsAcrossSessions` | Transliteration toggle state updates and persists in SavedStateHandle |
| **003** | `scenario_003_audioPlaybackStartAndPauseSequence` | Multi-verse audio toggling, active ayah switching, audio player synchronization |
| **004** | `scenario_004_slowSpeedPlaybackToggle` | 0.7x slow-speed toggle and 1.0x restoration with analytics telemetry |
| **005** | `scenario_005_markAyahPracticed_optimisticUpdateAndPersistence` | Local optimistic marking, non-blocking backend submission, set addition |
| **006** | `scenario_006_recordingStartAndStop_submitsAttemptAndPresentsFeedback` | Audio recording lifecycle, childId resolution, feedback presentation |
| **007** | `scenario_007_clearFeedback_resumesPracticeState` | Dismissing feedback modal cleanly restores practice viewport |
| **008** | `scenario_008_surahLoadFailure_presentsRetryStateAndRecovers` | Graceful network error handling and recovery on retry |
| **009** | `scenario_009_recitationSubmissionFailure_showsNonPunitiveToast` | Safe handling of backend recitation timeouts without blocking practice |
| **010** | `scenario_010_allAyatPracticed_canContinueToNextLesson` | Full completion of all ayat in Surah unlocks next progression |
| **011** | `scenario_011_practiceWithMissingAuth_fallsBackToGuestChildGracefully` | Unauthenticated / guest state defaults safely to `"guest_child"` |
| **012** | `scenario_012_activeAyahSelectionWithoutAudioPlay` | Selecting ayah manually updates active card without triggering unwanted audio |
| **013** | `scenario_013_independentTranslationToggle` | Translation toggle operates independently of transliteration |
| **014** | `scenario_014_canRecordGatedOnMicAndParentAi` | Record button hidden / disabled when microphone permission or parent AI is denied |
| **015** | `scenario_015_audioLoadFailureRetriesWithFallbackBeforeError` | Audio failures execute exponential backoff across `_low.mp3` & CDN fallback |
| **016** | `scenario_016_markPracticedFailureIsNonBlocking` | Offline sync / network error during progress submission never rolls back local completion |
| **017** | `scenario_017_processDeathRestoresBothToggles` | Process death and state restoration restores both `isTransliterationOn` and `isTranslationOn` |
| **018** | `scenario_018_audioPlayerCompletionResetsPlayingState` | Player track end / completion event (`KMPPlayerStatus.ENDED`) automatically clears playing state |
| **019** | `scenario_019_aiProcessingStateDuringRecitationEvaluation` | Explicit `isAiProcessing` state and processing modal dialog during AI evaluation |
| **020** | `scenario_020_fallbackToReferenceFlaggedOnRecitationOutage` | Low confidence / network outage activates self-assessment mode with reference audio comparison |
| **021** | `scenario_021_offlineStateNoticeHandled` | Offline practice state renders cache notice banner without dead ends |

