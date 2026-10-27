---
id: STORY-022
epic: EPIC-004
kind: feature
title: Wire Choice and Quiz State Transitions into StoryPlayerViewModel
status: ready
priority: P0
prd: ../../PRD_Documents/Child App (1-12)/Feature_A3_Stories_Module.md
depends_on: [STORY-018, STORY-019, STORY-020, STORY-021]
produces: []
consumes: [domain.story-player, domain.branch-resolution, repo.choice-event]
created: 2026-09-29
---

## User Story
As the Story Player engine, I want `StoryPlayerViewModel` to automatically intercept scripted choice and quiz timestamps from the manifest, pause playback, activate the corresponding overlay state, resolve branching deterministically, and record analytics, so that the interactive story flows seamlessly.

## Acceptance Criteria
- [ ] AC1: Given playback reaches a timestamp matching a `ChoicePoint` in the manifest's `interactive_script`, `StoryPlayerViewModel` automatically pauses playback and transitions `PlayerState` to `PlayerState.ChoiceActive(choicePoint)`.
- [ ] AC2: Given playback reaches a timestamp matching a `QuizMoment`, `StoryPlayerViewModel` pauses playback and transitions `PlayerState` to `PlayerState.QuizActive(quizMoment)`.
- [ ] AC3: Given `PlayerEvent.SelectChoice(choicePointId, optionId)` received:
  - Invokes `branchResolver.resolve(...)` synchronously to obtain the deterministic `nextSegmentRef`.
  - Commands player controller to seek/switch to the new segment and resume `PlayerState.Playing`.
  - Dispatches `choiceEventRepository.recordChoice(...)` asynchronously (fire-and-forget; never awaiting network).
  - Emits analytics event `story_choice_made(choice_id = choicePointId, branch_taken = nextSegmentRef)` via `AnalyticsTracker`.
- [ ] AC4: Given `PlayerEvent.CompleteQuiz(quizMomentId, isCorrect)` received:
  - Resumes `PlayerState.Playing`.
  - Emits analytics event `story_quiz_moment_answered(quiz_id = quizMomentId, is_correct = isCorrect)` via `AnalyticsTracker`.
- [ ] AC5: Given already passed choice/quiz points, the engine marks them evaluated so seeking backward/forward does not infinitely re-trigger already answered overlays unless explicitly replayed.

## Technical Notes
- Files in scope:
  - `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/presentation/player/StoryPlayerViewModel.kt`
  - `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/presentation/player/PlayerState.kt`
  - `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/presentation/player/PlayerEvent.kt`
  - `feature/feature-stories/src/commonTest/kotlin/com/noorheroes/feature/stories/presentation/StoryPlayerViewModelChoiceTest.kt`
- Integrates `BranchResolver`, `ChoiceEventRepository`, and `AnalyticsTracker`.

## Test Approach
- Unit: Test timestamp trigger intercepts playback position and enters `PlayerState.ChoiceActive`.
- Unit: Test option selection transitions to `PlayerState.Playing` immediately without awaiting repository completion.
- Unit: Verify `story_choice_made` and `story_quiz_moment_answered` analytics events are dispatched with exact parameters.

## Out of Scope
- Full player screen scaffold (STORY-016).
- Bedtime mode night sky theme (EPIC-005).
