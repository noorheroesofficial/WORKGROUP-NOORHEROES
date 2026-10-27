---
id: STORY-020
epic: EPIC-004
kind: feature
title: Implement ChoiceOverlay Composable with 3-Option Cap & Tap Debounce
status: ready
priority: P0
prd: ../../PRD_Documents/Child App (1-12)/Feature_A3_Stories_Module.md
depends_on: [STORY-018, STORY-019]
produces: []
consumes: [domain.branch-resolution]
created: 2026-09-29
---

## User Story
As a young child learner, I want an encouraging, beautiful, and unpressured interactive choice overlay with large clear cards, so that I can thoughtfully reflect on Islamic values and make decisions without anxiety or accidental multi-taps.

## Acceptance Criteria
- [ ] AC1: Given `PlayerState.ChoiceActive`, `ChoiceOverlay` renders as an in-player composable overlay above the video surface with a dark scrim, matching `Screens/Mobile App/Stories/Choice.png`.
- [ ] AC2: Given `options` list, `ChoiceOverlay` hard-enforces a maximum of 3 options:
  - In debug builds: `require(options.size <= 3) { "ChoiceOverlay accepts at most 3 options, received ${options.size}" }` fails loudly.
  - In release builds: gracefully truncates via `options.take(3)` and logs an error, never rendering a 4th card or crashing in production.
- [ ] AC3: Given user interaction, no countdown-timer element or progress countdown is present anywhere on the screen ("Take your time — there is no rush ✨").
- [ ] AC4: Given rapid repeated taps on an option card, a tap-debouncing guard (`500ms` window or selection lock) ensures exactly one selection event is dispatched to the callback.
- [ ] AC5: Given choice card rendering, each card displays an emoji/icon badge and bold legible text on a large rounded card surface (`NoorTheme.shapes.largeCardCornerRadius`).
- [ ] AC6: Given Design System rules (`NoorHeroes/docs/rule.md`), zero raw colors, zero raw dp/sp, zero raw shapes, and zero raw Material 3 components are used; file length is strictly `< 500 lines`.
- [ ] AC7: Given RTL locales (Arabic, Urdu), card layout and internal icon/text ordering properly mirror.

## Technical Notes
- Files in scope:
  - `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/presentation/player/overlay/ChoiceOverlay.kt`
  - `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/presentation/player/overlay/ChoiceOptionCard.kt`
  - `feature/feature-stories/src/commonTest/kotlin/com/noorheroes/feature/stories/presentation/ChoiceOverlayTest.kt`
- Conforms to screen mockup `Screens/Mobile App/Stories/Choice.png`.
- Debouncing implementation: state-based atomic lock `var isSelectionLocked by remember { mutableStateOf(false) }` or Kotlin Coroutines `debounce`.

## Test Approach
- Compose UI Test: Assert debug build throws `IllegalArgumentException` when 4 options are provided.
- Compose UI Test: Assert release build renders exactly 3 cards when 4 options are provided in fixture.
- Compose UI Test: Assert no countdown timer or progress indicator exists in the semantic tree.
- Compose UI Test: Rapid 5-tap click test verifies `onOptionSelected` is invoked exactly once.

## Out of Scope
- Story player video playback engine (STORY-014).
- Quiz moment overlay (STORY-021).
