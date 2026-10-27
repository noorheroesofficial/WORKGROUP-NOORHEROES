---
id: STORY-004
epic: EPIC-001
kind: feature
title: Implement StoriesLibraryScreen, Rails, Offline Affordances, and FilterPanel
status: done
priority: P0
prd: ../../PRD_Documents/Child App (1-12)/Feature_A3_Stories_Module.md
depends_on: [STORY-003]
produces: []
consumes: [domain.story-library]
created: 2026-09-29
---

## User Story
As a child learner, I want to see visual category rails, skeleton loaders, themed empty states, and clear offline banners, matching the exact design mocks.

## Acceptance Criteria
- [x] AC1: Given loading state, when the screen renders, then skeleton cards matching `Stories-03.png` appear immediately.
- [x] AC2: Given populated state, when scrolling rails, then cards render with age badge, progress ring, duration pill, and episode counter matching `Stories-01.png` and `Stories-02.png`.
- [x] AC3: Given empty category, when selected, then empty state illustration and recommended alternatives render matching `Stories-04.png` and `Stories-05.png`.
- [x] AC4: Given offline state, when offline mode is active, then top warning banner, downloaded-ready section, and disabled items with "Requires connection" feedback render matching `Stories-06.png` and `Stories-07.png`.
- [x] AC5: Given Design System rules, all UI code uses `NoorHeroesTheme.colors.*`, `NoorHeroesTheme.spacing.*`, `NoorHeroesTheme.sizes.*`, `NoorHeroesTheme.typography.*`, canonical primitives from `core:core-ui`, and stays under 500 lines per file.

## Technical Notes
- Files in scope: `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/ui/*`.
- 100% string localization across `values`, `values-ar`, `values-hi`, `values-ur`.

## Test Approach
- UI / Composable tests for loading, populated, empty, and offline states.

## Out of Scope
- Story Detail navigation destination implementation (covered in K-02).
