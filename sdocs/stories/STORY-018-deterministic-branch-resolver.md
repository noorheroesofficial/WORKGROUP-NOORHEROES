---
id: STORY-018
epic: EPIC-004
kind: feature
title: Implement Pure-Domain Deterministic BranchResolver
status: ready
priority: P0
prd: ../../PRD_Documents/Child App (1-12)/Feature_A3_Stories_Module.md
depends_on: [EPIC-003]
produces: [domain.branch-resolution]
consumes: [domain.story-player]
created: 2026-09-29
---

## User Story
As a child learner watching an interactive animated story, I want my choice selection to immediately and deterministically branch the storyline without delay, so that my storytelling experience is smooth, instant, and never stalls on network requests.

## Acceptance Criteria
- [ ] AC1: Given a `ChoicePoint` with valid `options` and a `selectedOptionId`, `BranchResolver.resolve()` deterministically returns `BranchResolutionResult.Resolved` containing the exact `nextSegmentRef` defined in the manifest.
- [ ] AC2: Given identical inputs `(ChoicePoint, selectedOptionId)`, `BranchResolver.resolve()` always returns the exact same outcome with 100% mathematical determinism.
- [ ] AC3: Given debug mode (`isDebug = true`), if `choicePoint.options.size > 3`, `BranchResolver.resolve()` throws an `IllegalArgumentException` failing loudly as required by PRD Section 7.
- [ ] AC4: Given release mode (`isDebug = false`), if `choicePoint.options.size > 3`, `BranchResolver.resolve()` gracefully truncates to `choicePoint.options.take(3)` and resolves successfully without crashing in production.
- [ ] AC5: Given a `selectedOptionId` that does not exist in `choicePoint.options`, `BranchResolver.resolve()` returns `BranchResolutionResult.Error(Reason.OPTION_NOT_FOUND)`.
- [ ] AC6: Given pure execution, `BranchResolver` has zero network dependencies, zero disk I/O, and executes synchronously in under 1ms.

## Technical Notes
- Files in scope:
  - `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/domain/model/ChoiceModels.kt`
  - `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/domain/branching/BranchResolver.kt`
  - `feature/feature-stories/src/commonTest/kotlin/com/noorheroes/feature/stories/domain/BranchResolverTest.kt`
- Conforms to contract `domain.branch-resolution`.
- Invariants: Pure Kotlin domain layer, zero Android/iOS platform dependencies, zero coroutine delays.

## Test Approach
- Unit: Determinism verification across 1,000 permutations.
- Unit: Debug mode `require(options.size <= 3)` assertion test.
- Unit: Release mode graceful truncation to 3 options test.
- Unit: Missing option ID error handling test.

## Out of Scope
- Network recording of choice events (STORY-019).
- Composable UI rendering (STORY-020).
