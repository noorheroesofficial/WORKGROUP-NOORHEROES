---
id: STORY-017
epic: EPIC-003
kind: integration
title: Integration and End-to-End Verification of Story Player Core Engine
status: ready
priority: P0
prd: ../../PRD_Documents/Child App (1-12)/Feature_A3_Stories_Module.md
depends_on: [STORY-011, STORY-012, STORY-013, STORY-014, STORY-015, STORY-016]
produces: []
consumes: [domain.story-player, repo.story-manifest, api.story-manifest, api.playback-heartbeat]
created: 2026-09-29
---

## User Story
As an engineering team, we want end-to-end integration verification across data, domain, player engine, presentation, and UI layers, ensuring zero state desynchronization, 100% token compliance, and passing tests.

## Acceptance Criteria
- [ ] AC1: Given all Story Player stories implemented, when unit test suite runs, all unit and presentation tests pass in `feature:feature-stories`.
- [ ] AC2: Given state desync test, asserts Compose controls never show "Playing" while the underlying `KMPPlayerController` reports buffering or error.
- [ ] AC3: Given the Design System compliance script (`rule.md`), asserts 0 hardcoded colors, 0 raw dp/sp, 0 raw shapes, 0 raw Material 3 components, and 0 files exceeding 500 lines.
- [ ] AC4: Given the codebase, asserts zero direct calls to platform Media3 or AVPlayer APIs exist.
- [ ] AC5: Given performance testing on low-end device profile, cold start to first rendered player frame with cached manifest achieves p95 < 1.5s.

## Technical Notes
- Files in scope: `feature/feature-stories/src/commonTest/kotlin/**`.
- Non-functional: Cold-start p95 < 1.5s with cached manifest.

## Test Approach
- Integration: Full scripted playback flow: load manifest → prepare → play → accumulate 10s → send heartbeat → pause → seek → complete.
- Regression: Full module build and test execution via Gradle.

## Out of Scope
- Interactive branch execution (covered in K-04).
