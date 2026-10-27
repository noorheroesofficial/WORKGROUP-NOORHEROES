# Evidence: Bedtime Audio Player Core Screen & Visual Fidelity (K-01 / K-03)

**Task**: `01-bedtime-audio-player-core-screen` & `03-calm-mode-bedtime-theme-application`  
**Parent PRD**: `PRD_Documents/Child App (1-12)/Feature_A4_Audio_Bedtime_Player_Bedtime_Mode.md`  
**Task Blueprints**: 
- `Development_Blueprints/A4_Audio_Bedtime_Player_Bedtime_Mode/KMP/01-bedtime-audio-player-core-screen.md`
- `Development_Blueprints/A4_Audio_Bedtime_Player_Bedtime_Mode/KMP/03-calm-mode-bedtime-theme-application.md`
**Visual Blueprint**: `Development_Blueprints/A4_Audio_Bedtime_Player_Bedtime_Mode/00-screen-to-code-visual-blueprint.md`  
**Reference Mockups**: 
- `Screens/Mobile App/Bedtime Audio/Audio Player.png` (Screen 01)
- `Screens/Mobile App/Bedtime Audio/Dua Card.png` (Screen 02)
- `Screens/Mobile App/Bedtime Audio/Sleep Timer.png` (Screen 03)
- `Screens/Mobile App/Stories/Bedtime Player.png`  
**Date**: 2026-10-11  
**Status**: 100% AUDITED, VERIFIED & PASSING (ZERO MISSING SCENARIOS)  

---

## 1. Verified Screen-to-Code Implementation Inventory (All 3 Screens)

### Screen 01: `Audio Player.png` (Core Screen)
- **Top Navigation Bar**:
  - Circular back button: `IconButton` (`sizes.controlHeight`, `shapes.circle`, `colors.surfaceSunken`) with `Icons.AutoMirrored.Filled.ArrowBack`.
  - Header text: Centered `Text` with `typography.labelMedium`, `colors.textSecondary` ("BEDTIME STORY.").
  - Circular playlist / episodes button: `IconButton` (`sizes.controlHeight`, `shapes.circle`, `colors.surfaceSunken`) with `Icons.AutoMirrored.Filled.List`.
- **Active Sleep Timer Pill**:
  - Centered chip below top bar: `ActiveSleepTimerChip` with `shapes.pill`, `colors.surfaceSunken`, `sizes.borderThin` in amber `colors.primary`.
  - Displays crescent moon icon, remaining time e.g. "Sleep timer · 30 min", and close "X" dismiss button.
- **Center Cover Artwork (`BreathingCoverArt`)**:
  - Outer radial glow aura (`radius28`) pulsating at 3500ms cycle ($0.98\text{f} \leftrightarrow 1.02\text{f}$) in isolated recomposition scope.
  - Reduced motion accessibility: When `reduceMotion` is active, strictly locks to a static 1.0f scale and 0.35f alpha.
  - Inner card surface: `radius24`, gradient background, crescent moon icon (`colors.primary`), and glowing lantern emblem with Arabic "بِسْمِ اللَّه" in `typography.arDua`.
- **Story Metadata Block (`CoverInfoHeader`)**:
  - Title: `manifest.title` ("Moonlit Lantern") in display `typography.h1` with `colors.textPrimary`.
  - Subtitle: Localized `bedtime_player_episode_subtitle` ("Episode 2 of 3 · Bedtime Series") in `typography.bodyMedium`.
  - Moral lesson quote: Localized `bedtime_player_moral_quote` ("\"Trusting in Allah brings peace to the heart...\"") in warm amber `colors.primary`.
  - Trust badge: `Icons.AutoMirrored.Filled.MenuBook` + `bedtime_player_scholar_reviewed` in `typography.labelSmall`.
- **Scrubber & Duration (`AudioScrubber`)**:
  - `NoorSlider` with amber primary track and rounded thumb.
  - Timestamps: Elapsed time ("4:49") and total duration ("8:00") in `typography.bodySmall`.
- **Primary Playback Controls (`PrimaryControlsRow`)**:
  - Previous track: Circular button (`sizes.controlHeight`, `shapes.circle`, `surfaceSunken`) with `SkipPrevious`.
  - Play/Pause toggle: Large circular button (`sizes.counter`, `shapes.circle`, `colors.surface`) with amber border (`sizes.borderMedium`, `colors.primary`) and Play/Pause icons or buffering spinner.
  - Next track: Circular button (`sizes.controlHeight`, `shapes.circle`, `surfaceSunken`) with `SkipNext`.
- **Secondary Action Rail (`SecondaryControlsRow`)**:
  - Speed selector: Speedometer icon + "1x" label.
  - Sleep timer toggle: Crescent moon icon + "Timer" label (active state highlighted in amber `colors.primary`).
  - Offline save toggle: Download icon + "Save" / "Saved" label.
  - Episodes sheet button: List icon + "Episodes" label.
  - Every item renders in a sunken circular container (`sizes.touchTarget`, `shapes.circle`, `surfaceSunken`).

---

### Screen 02: `Dua Card.png` (Evening Dua Reflection Card)
- **Background Scrim**: Nocturnal dark scrim (`colors.scrim`) with 36 ambient stars (`BedtimeAmbientStars`).
- **Parchment Card**:
  - Surface: `radius28` rounded container, `fillMaxWidth(0.92f)`, `colors.surface` with subtle border.
  - Gentle fade-in: `Animatable` tween with 850ms duration (instant if `reduceMotion` enabled).
- **Header**: Centered uppercase "EVENING DUA" in `typography.labelMedium`, `colors.primary`.
- **Arabic Calligraphy**: "بِسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا" in `typography.arDua`, `colors.textPrimary`.
- **Ornamental Divider**: Thin golden hairlines flanking a golden crescent moon icon (`Icons.Default.Nightlight`).
- **Transliteration**: "Bismika Allahumma amutu wa ahya" in italic `typography.bodyLarge`.
- **Translation**: "\"In Your name, O Allah, I die and I live.\"" in `typography.bodyMedium`.
- **Sleeping Companion Mascot**: Circular container (`sizes.avatarMedium`, `shapes.circle`, `primarySubtle`) with crescent moon/sleeping lantern.
- **Attribution**: "Narrated by Al-Bukhari" in `typography.bodySmall`, `colors.textSecondary`.
- **Action Buttons**:
  - "Done" button: Wide `SecondaryButton` (`ButtonSize.Large`).
  - Optional "Next Episode" button when unlocked in sequential series.
  - **Zero Gamification**: Zero XP counters, badges, points, or celebratory particle bursts.

---

### Screen 03: `Sleep Timer.png` (Sleep Timer Sheet)
- **Modal Sheet Container**: `NoorBottomSheet` with `surface` background and `radius24` rounded top corners.
- **Header**:
  - Golden crescent moon icon (`colors.primary`) + "Sleep Timer" in `typography.h2`.
  - Circular close button (`sizes.controlHeight`, `shapes.circle`, `surfaceSunken`) with `Icons.Default.Close`.
- **Subtitle**: "Playback will fade out gently when the timer ends." in `typography.bodyMedium`.
- **Radio Option Cards (`SleepTimerOptionCard`)**:
  - 4 options: "15 minutes", "30 minutes" (selected), "45 minutes", "Until episode ends".
  - Selected state: `colors.primary` border (`sizes.borderDefault`), `surfaceSunken` container, filled amber center dot (`sizes.iconSmall`).
  - Unselected state: `colors.borderStrong` border (`sizes.borderThin`), `surface` container, empty circular radio ring.
- **Action CTA**: Wide `SecondaryButton` ("Turn off timer") with `ButtonSize.Large`.

---

## 2. Design System & Rule Compliance Audit (`NoorHeroes\docs\rule.md`)

| Rule | Requirement | Audited Metric | Result |
|:---|:---|:---:|:---:|
| **Rule 1 (Zero Hardcoded Hex)** | No `Color(0x...)` or raw palette values | 0 raw hex violations across all files | **100% COMPLIANT** |
| **Rule 1 (Zero Hardcoded DP/SP)** | No raw `dp` or `sp` literals | 0 raw dimension violations | **100% COMPLIANT** |
| **Rule 1 (Zero Hardcoded Shapes)** | No raw `RoundedCornerShape` or `CircleShape` | 0 raw shape violations (all via `NoorHeroesTheme.shapes`) | **100% COMPLIANT** |
| **Rule 2 (Localization Parity)** | All 4 locales synchronized | 100% parity across `values`, `values-ar`, `values-ur`, `values-hi` | **100% COMPLIANT** |
| **Rule 8 (File Line Ceiling)** | Every Kotlin source file strictly $< 500$ lines | Max lines: `BedtimeAudioViewModel.kt` (496 lines), `Route.kt` (489 lines) | **100% COMPLIANT** |

### Line Count Audit
```
NoorHeroes\feature\feature-bedtime-audio\src\commonMain\kotlin\com\noorheroes\feature\bedtime\audio\ui\BedtimeAudioPlayerScreen.kt: 428 lines
NoorHeroes\feature\feature-bedtime-audio\src\commonMain\kotlin\com\noorheroes\feature\bedtime\audio\ui\CoverInfoHeader.kt: 249 lines
NoorHeroes\feature\feature-bedtime-audio\src\commonMain\kotlin\com\noorheroes\feature\bedtime\audio\ui\BreathingCoverArt.kt: 157 lines
NoorHeroes\feature\feature-bedtime-audio\src\commonMain\kotlin\com\noorheroes\feature\bedtime\audio\ui\BedtimeAudioControls.kt: 291 lines
NoorHeroes\feature\feature-bedtime-audio\src\commonMain\kotlin\com\noorheroes\feature\bedtime\audio\ending\DuaReflectionEndingCard.kt: 252 lines
NoorHeroes\feature\feature-bedtime-audio\src\commonMain\kotlin\com\noorheroes\feature\bedtime\audio\ui\SleepTimerSheet.kt: 252 lines
NoorHeroes\feature\feature-bedtime-audio\src\commonMain\kotlin\com\noorheroes\feature\bedtime\audio\ui\BedtimeAmbientStars.kt: 88 lines
NoorHeroes\feature\feature-bedtime-audio\src\commonMain\kotlin\com\noorheroes\feature\bedtime\audio\presentation\BedtimeAudioViewModel.kt: 496 lines
NoorHeroes\core\core-navigation\src\commonMain\kotlin\com\noorheroes\core\navigation\Route.kt: 489 lines
```

---

## 3. Test Suite Verification & Results

- **Gradle Task**: `./gradlew :feature:feature-bedtime-audio:testAndroidHostTest :androidApp:compileDevDebugKotlin :shared:compileAndroidMain`
- **Result**: **110 of 110 tests passing (100% Green)**.

| Test Class | Test Count | Result |
|:---|:---:|:---:|
| `BedtimeRepositoryTest` | 10 | **10/10 PASSED** |
| `BedtimeRepositoryExtendedTest` | 5 | **5/5 PASSED** |
| `BedtimeDeepLinkHandlerTest` | 19 | **19/19 PASSED** |
| `BedtimeAudioViewModelTest` | 21 | **21/21 PASSED** |
| `BedtimeOfflineStatesTest` | 11 | **11/11 PASSED** |
| `BedtimeDownloadSuggestionEngineTest` | 8 | **8/8 PASSED** |
| `DuaEndingCardTest` | 9 | **9/9 PASSED** |
| `BedtimeCompletionExtendedTest` | 9 | **9/9 PASSED** |
| `BedtimeCompletionFlowTest` | 7 | **7/7 PASSED** |
| `BedtimeCalmModeResolverTest` | 6 | **6/6 PASSED** |
| `CalmModeThemeTest` | 5 | **5/5 PASSED** |
| **Total** | **110** | **110/110 PASSED (100%)** |
