# Evidence: Dua Card Detail & Audio Playback Experience (Task K-02)

**Task**: `02-dua-card-detail-audio-playback-experience`  
**Parent PRD**: `PRD_Documents/Child App (1-12)/Feature_A6_Dua_Learning.md`  
**Task Blueprint**: `Development_Blueprints/A6_Dua_Learning/KMP/02-dua-card-detail-audio-playback-experience.md`  
**Visual References**: `Screens/Mobile App/Du'as/` (`Dua Card-01.png`, `Dua Card-02.png`)  
**Target Module**: `:feature:feature-dua`  
**Date**: 2026-11-14  
**Status**: AUDITED & VERIFIED (ZERO MISSING SCENARIOS)

---

## 1. Verified Acceptance Criteria Matrix

| Requirement / ID | Description | Acceptance Criteria | Result |
| :--- | :--- | :--- | :---: |
| **FR-2** | Simultaneous 4-Element Card Layout | • AC1: Large Arabic calligraphy, transliteration, translation, and audio play control are all simultaneously visible in one composition pass without extra taps.<br>• AC2: Context header displays category title, Arabic title, and source citation ("📜 Narrated by Al-Bukhari").<br>• AC3: Rendered via modular components (`DuaTextContentCard`, `DuaAudioPlayerBar`, `DuaDetailTopBar`, `DuaCardActionButtons`). | **100% VERIFIED** |
| **FR-3** | Interactive Child Actions per Dua | • AC1: Listen (Play / Pause / Replay with interactive tap-to-seek scrubber).<br>• AC2: Mark as Learned (child-initiated self-assessed toggle supporting both mark and un-mark per PRD Edge Case 2).<br>• AC3: Practice Recall Quiz (gated on learned status).<br>• AC4: Favorite (circular heart button toggle). | **100% VERIFIED** |
| **FR-4** | P0 Invariant: Always Free-Tier | • AC1: Zero entitlement checks, zero subscription gates, zero paywall UI in the entire screen and module.<br>• AC2: Fully accessible to Free, TrialExpired, and ActiveSubscriber accounts identically.<br>• AC3: Verified via CI-blocking unit test `DuaCardDetailAlwaysFreeTierTest.kt`. | **100% VERIFIED** |
| **FR-5** | Self-Assessed "Mark as Learned" & Quiz Gating | • AC1: Mark as Learned is child-initiated, optimistic, and bidirectional (can un-mark without revoking milestone history).<br>• AC2: Practice Recall Quiz button is locked/muted with lock icon (`Icons.Default.Lock`) when unlearned ("Practice Quiz (mark learned first)"). Tapping it surfaces child-friendly guidance via `SnackbarHost`.<br>• AC3: Practice Recall Quiz unlocks as an active primary teal button with brain icon 🧠 immediately when marked learned. | **100% VERIFIED** |
| **Synchronized Read-Along Highlight** | Word-by-Word Timestamp Synchronization | • AC1: Active Arabic word highlights in teal container box during playback.<br>• AC2: Scrubber subtitle displays live telemetry (e.g., "Read-along active — word 8 of 9").<br>• AC3: Pure KMP `ReadAlongHighlightController` with exact timestamp bounding and linear duration interpolation fallback.<br>• AC4: Sequential-exposure TalkBack/VoiceOver accessibility text builder for screen readers. | **100% VERIFIED** |
| **Audio Stack Integration** | Real AudioPlayerController Integration | • AC1: Injected with `AudioPlayerController` from `:library:kmpplayer` (`com.noorheroes.kmpplayer.core.audio`).<br>• AC2: Controls `play(KMPPlayerSource.Network(url))`, `pause()`, `resume()`, `seekTo(ms)`, `stop()`.<br>• AC3: Cleans up audio on screen disposal (`onCleared()`). | **100% VERIFIED** |
| **B-01 / B-02 / B-14 Contract** | Optimistic Mutations & Server Synchronization | • AC1: Consumes B-01 (`GET /v1/catalog/dua/{id}`).<br>• AC2: Dispatches B-02 (`POST /v1/progress`) with mandatory `client_request_id` idempotency field.<br>• AC3: Dispatches B-14 (`POST /v1/favorites`) with mandatory `client_request_id` idempotency field.<br>• AC4: Optimistic local Room database update via `DuaLocalDataSource` before network dispatch. | **100% VERIFIED** |
| **Design Tokens (`rule.md`)** | 100% Design Token Compliance | • AC1: Zero hardcoded hex colors, zero raw dp/sp, zero raw shapes.<br>• AC2: Bound 100% to `NoorHeroesTheme.colors`, `typography`, `spacing`, `shapes`, `sizes`.<br>• AC3: All files strictly $< 500$ lines (modularized into 5 focused UI files, largest is 191 lines). | **100% VERIFIED** |
| **Localization §21** | 4-Locale String Parity | • AC1: 15 string resources synchronized across `values`, `values-ar`, `values-ur`, and `values-hi`.<br>• AC2: Full RTL bidirectional text flow for Arabic calligraphy. | **100% VERIFIED** |
| **Error & Loading States** | Robust Offline & Loading Handling | • AC1: `NoorSkeleton` displayed while fetching initial content.<br>• AC2: `NoorAlert` with `AlertTone.Error` and interactive "Retry" button when network fails and no cache exists. | **100% VERIFIED** |

---

## 2. Visual Mockup Verification Matrix (Element-by-Element)

### Mockup 1: `Dua Card-01.png` (In-Playback / Initial Unlearned State)
| UI Element in Mockup | Mockup Specification | Implemented Component & Styling | Design System Tokens | Status |
| :--- | :--- | :--- | :--- | :---: |
| **Top Bar: Back Button** | Circular back button with left arrow icon, white surface, subtle border | `DuaDetailTopBar` (circular Box + `ArrowBack`) | `sizes.controlHeight`, `shapes.circle`, `colors.surface`, `sizes.borderThin` | **100% MATCH** |
| **Top Bar: Category Pill** | Centered yellow/amber pill with sun icon and `"Morning"` text | `Box` with `Row` (Sun icon + text) | `colors.warning`, `shapes.pill`, `spacing.space16`, `spacing.space6` | **100% MATCH** |
| **Top Bar: Favorite Button** | Circular button with unfavorited heart outline (`FavoriteBorder`), subtle border | `Box` with `Icon(Icons.Default.FavoriteBorder)` | `sizes.controlHeight`, `shapes.circle`, `colors.textSecondary` | **100% MATCH** |
| **Dua Content Card** | White rounded card container with elevation and 16dp inner padding | `DuaTextContentCard` using `NoorCard` | `shapes.card`, `colors.surface`, `elevation.card`, `spacing.space16` | **100% MATCH** |
| **Sub-Header Row** | Left pill: `"Upon Waking"` (teal subtle container); Right: `"دعاء الاستيقاظ"` (Arabic subtitle) | Header `Row` inside `DuaTextContentCard` | `colors.primarySubtle`, `colors.primary`, `typography.labelMedium`, `typography.bodyMedium` | **100% MATCH** |
| **Arabic Calligraphy** | 2-line large Arabic text with RTL flow, centered alignment | `DuaArabicWordFlow` + `DuaWordRow` | `typography.h1`, `colors.textPrimary`, `TextAlign.Center` | **100% MATCH** |
| **Active Word Highlight** | Word 8 `"وَإِلَيْهِ"` highlighted in rounded teal box during playback | Highlight box around active word in `DuaWordRow` | `colors.surfaceVariant`, `shapes.radius4`, `spacing.space6` | **100% MATCH** |
| **Divider Line** | Thin grey horizontal divider below Arabic text | `HorizontalDivider` | `colors.disabledSurface`, `sizes.borderThin` | **100% MATCH** |
| **Transliteration** | Bold English transliteration text | `Text` inside `DuaTextContentCard` | `typography.bodyLarge`, `colors.textPrimary` | **100% MATCH** |
| **Translation** | English translation paragraph | `Text` inside `DuaTextContentCard` | `typography.bodyMedium`, `colors.textPrimary` | **100% MATCH** |
| **Attribution Footnote** | Scroll icon (📜) + `"Narrated by Al-Bukhari"` | Footnote `Row` inside `DuaTextContentCard` | `typography.bodySmall`, `colors.textSecondary` | **100% MATCH** |
| **Audio Bar: Play/Pause** | Circular teal button with Pause icon (active playback) | Circular Box in `DuaAudioPlayerBar` | `colors.primary`, `colors.onPrimary`, `sizes.controlHeight`, `shapes.circle` | **100% MATCH** |
| **Audio Bar: Scrubber** | Horizontal linear progress indicator with rounded pill shape | `LinearProgressIndicator` (with seek callback) | `colors.primary`, `colors.disabledSurface`, `shapes.pill`, `spacing.space8` | **100% MATCH** |
| **Audio Bar: Subtitle** | Teal telemetry: `"Read-along active — word 8 of 9"` | `Text` below scrubber | `colors.primary`, `typography.labelSmall` | **100% MATCH** |
| **Audio Bar: Replay** | Circular button with refresh icon on right | Circular Box in `DuaAudioPlayerBar` | `colors.surfaceVariant`, `colors.textPrimary`, `sizes.avatarSmall`, `shapes.circle` | **100% MATCH** |
| **Button 1: Mark as Learned** | Full-width white card: grey outline circle + `"Mark as Learned"` text | `DuaMarkLearnedButton(isLearned = false)` | `colors.surface`, `colors.disabledText`, `colors.textPrimary`, `typography.labelLarge` | **100% MATCH** |
| **Button 2: Practice Quiz (Locked)** | Muted container with lock icon (🔒) + `"Practice Quiz (mark learned first)"` | `DuaPracticeQuizButton(isUnlocked = false)` | `colors.disabledSurface`, `colors.disabledText`, `typography.labelLarge` | **100% MATCH** |

### Mockup 2: `Dua Card-02.png` (Learned & Favorited State)
| UI Element in Mockup | Mockup Specification | Implemented Component & Styling | Design System Tokens | Status |
| :--- | :--- | :--- | :--- | :---: |
| **Top Bar: Attached Sub-Pill** | Below `"Morning"` pill: attached white pill with amber border + checkmark + `"Learned ✦"` | Sub-pill in `DuaDetailTopBar(isLearned = true)` | `colors.surface`, `colors.warning`, `shapes.pill`, `sizes.borderThin`, `typography.labelSmall` | **100% MATCH** |
| **Top Bar: Favorite Active** | Circular button with filled red heart (`Icons.Default.Favorite`) and red outline | `Box` with `Icon(Icons.Default.Favorite)` in `DuaDetailTopBar` | `colors.error`, `sizes.controlHeight`, `shapes.circle` | **100% MATCH** |
| **Audio Bar: Paused State** | Circular teal button with Play arrow icon (`Icons.Default.PlayArrow`) | `DuaAudioPlayerBar(isPlaying = false)` | `colors.primary`, `colors.onPrimary`, `Icons.Default.PlayArrow` | **100% MATCH** |
| **Button 1: Marked as Learned** | Full-width card with golden amber border, checkmark in amber circle, `"Marked as Learned"` | `DuaMarkLearnedButton(isLearned = true)` | `colors.warning`, `colors.onPrimary`, `shapes.circle`, `typography.labelLarge` | **100% MATCH** |
| **Button 2: Practice Quiz (Active)** | Solid primary teal button with brain icon (🧠) + `"Practice Quiz"` text | `DuaPracticeQuizButton(isUnlocked = true)` | `PrimaryButton`, `colors.primary`, `colors.onPrimary`, `typography.bodyLarge` | **100% MATCH** |

---

## 3. Design System Token & Rule Compliance Matrix (`rule.md`)

| Rule | Requirement | Metric | Result |
| :--- | :--- | :---: | :---: |
| **Rule 1: Hardcoded Colors** | 0 hex/palette literals | 0 occurrences across all K-02 Kotlin files | **100% COMPLIANT** |
| **Rule 2: Dimensions & Typography** | 0 raw `dp` / `sp` literals | Bound strictly to `spacing`, `sizes`, `typography` | **100% COMPLIANT** |
| **Rule 3: Canonical Primitives** | Use Core UI buttons, cards, text fields | Sourced from `NoorCard`, `PrimaryButton`, `NoorAlert`, `NoorSkeleton` | **100% COMPLIANT** |
| **Rule 4: Modularity Ceiling** | Maximum 500 lines per file | Modularized into 5 UI files + ViewModel + Controller (largest is 252 lines in `DuaRepositoryImpl.kt`) | **100% COMPLIANT** |
| **Rule 7: MVI Purity** | Immutable states, single event pipeline | `DuaCardUiState`, `DuaCardUiEvent`, `DuaCardUiEffect` | **100% COMPLIANT** |
| **Rule 8: Localization** | 100% key parity across 4 locales | 15 keys synchronized across EN, AR, UR, HI in `core-common` | **100% COMPLIANT** |
| **Rule 12: CI-Blocking Tests** | Always-Free invariant verified | Automated test `DuaCardDetailAlwaysFreeTierTest.kt` passing | **100% COMPLIANT** |

---

## 4. Test Execution & Build Verification

```powershell
$env:JAVA_HOME = "C:\Program Files\Java\jdk-21"; cd NoorHeroes; .\gradlew.bat :feature:feature-dua:testAndroidHostTest
```

### Test Results Summary
- **Outcome**: `BUILD SUCCESSFUL in 27s`
- **Actionable Tasks**: 100 actionable tasks (14 executed, 86 up-to-date)
- **Total Tests Completed**: 36 tests completed, 0 failed, 0 skipped
  - `DuaCardDetailAlwaysFreeTierTest` (3 tests: verify zero paywall UI, verify free accounts identical, verify no subscription checks) — **PASSED**
  - `ReadAlongHighlightControllerTest` (4 tests: active word bounding, linear interpolation fallback, telemetry formatting, sequential TalkBack string) — **PASSED**
  - `DuaCardViewModelTest` (7 tests: initial load, optimistic mark/un-mark learned, optimistic favorite, playback controls, seek word resolution, practice quiz gating, retry reload) — **PASSED**
  - `DuaLocalDataSourceTest` (3 tests: categories CRUD, duas CRUD/counts, single dua status updates with un-learning) — **PASSED**
  - `DuaRepositoryImplTest` (6 tests: cache-then-remote categories, baseline fallback, dua detail cache hit, optimistic bidirectional markLearned, optimistic toggleFavorite, always-free invariant) — **PASSED**
  - `DuaCatalogAlwaysFreeTierTest` (3 tests) — **PASSED**
  - `DuaCatalogViewModelTest` (7 tests) — **PASSED**
  - `DuaCategoryIconResolverTest` (3 tests) — **PASSED**

### Integration Compilation
```powershell
$env:JAVA_HOME = "C:\Program Files\Java\jdk-21"; cd NoorHeroes; .\gradlew.bat :shared:compileAndroidMain
```
- **Outcome**: `BUILD SUCCESSFUL in 10s`
- **Actionable Tasks**: 155 actionable tasks (30 executed, 125 up-to-date)
- **Verification**: Clean integration across navigation graphs, DI graph, and UI modules with zero errors.
