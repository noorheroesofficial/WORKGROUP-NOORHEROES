---
id: STORY-021
epic: EPIC-004
kind: feature
title: Implement QuizMomentOverlay Delegating to Shared Quiz Delegate
status: ready
priority: P1
prd: ../../PRD_Documents/Child App (1-12)/Feature_A3_Stories_Module.md
depends_on: [STORY-018]
produces: []
consumes: [domain.story-player]
created: 2026-09-29
---

## User Story
As a child learner, I want mid-story pause-and-quiz moments to present quick, engaging checks of understanding that feel seamlessly integrated, so that I can reinforce my moral learning before resuming the adventure.

## Acceptance Criteria
- [ ] AC1: Given `PlayerState.QuizActive`, `QuizMomentOverlay` renders as an in-player overlay layer above the video surface.
- [ ] AC2: Given modular architecture, `QuizMomentOverlay` acts as a thin composable wrapper that delegates actual question rendering and answer evaluation to a shared `QuizEngineDelegate` (or `@Composable (questionId: String, onAnswered: (Boolean) -> Unit) -> Unit` slot), preventing any duplication of quiz UI logic between Feature A.3 and Feature A.8.
- [ ] AC3: Given the child submits an answer, the overlay invokes `onQuizCompleted(result)` to signal the ViewModel to resume playback.
- [ ] AC4: Given the overlay chrome, title, question prompt, and feedback banners use Design System tokens (`NoorTheme.typography`, `NoorTheme.colorScheme`, `NoorTheme.dimensions`).
- [ ] AC5: Given Design System rules (`NoorHeroes/docs/rule.md`), zero raw colors, zero raw dp/sp, zero raw shapes, and zero raw Material 3 components are used; file length is strictly `< 500 lines`.

## Technical Notes
- Files in scope:
  - `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/presentation/player/overlay/QuizMomentOverlay.kt`
  - `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/presentation/player/overlay/QuizEngineDelegate.kt`
  - `feature/feature-stories/src/commonTest/kotlin/com/noorheroes/feature/stories/presentation/QuizMomentOverlayTest.kt`
- Implements slot/delegate pattern to allow seamless injection of Feature A.8 Daily Quiz engine once implemented.

## Test Approach
- Compose UI Test: Verify `QuizMomentOverlay` properly delegates to the injected slot or `QuizEngineDelegate`.
- Compose UI Test: Verify answering or completing the quiz fires `onQuizCompleted` callback exactly once.
- Compose UI Test: Verify zero raw styling and proper semantic tree accessibility nodes.

## Out of Scope
- Full A.8 quiz gamification / points ledger (Feature A.8 / A.11).
- Interactive choice cards (STORY-020).
