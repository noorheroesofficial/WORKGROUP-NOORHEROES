---
id: STORY-003
epic: EPIC-001
kind: feature
title: Implement StoryCatalogRepository, GetStoriesLibraryUseCase, and StoriesLibraryViewModel
status: done
priority: P0
prd: ../../PRD_Documents/Child App (1-12)/Feature_A3_Stories_Module.md
depends_on: [STORY-002]
produces: [domain.story-library]
consumes: [api.content-catalog, data.story-cache]
created: 2026-09-29
---

## User Story
As a child learner, I want the Stories Library state to load category rails with debounced filtering and offline fallback, so that browsing is smooth, fast, and responsive.

## Acceptance Criteria
- [x] AC1: Given the Downloads category, when `StoryCatalogRepository` reads stories, then it reads from local cache first with zero network dependency.
- [x] AC2: Given other categories, when network fails, then `StoryCatalogRepository` falls back to cached metadata with `isOffline = true`.
- [x] AC3: Given the filter panel, when user changes filter chips, then `StoriesLibraryViewModel` debounces requests by 300ms before triggering `GetStoriesLibraryUseCase`.
- [x] AC4: Given the ViewModel, when library or filter changes occur, then `stories_library_viewed` and `stories_category_filtered` analytics events fire.

## Technical Notes
- Files in scope: `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/domain/*`, `feature/feature-stories/src/commonMain/kotlin/com/noorheroes/feature/stories/presentation/*`.
- Extends `BaseViewModel`.
- Zero UI imports in domain and data layers.

## Test Approach
- Unit: Repository routing test (cache-first for downloads, network-first for others), ViewModel debounce and state reduction tests.

## Out of Scope
- Composable screen rendering (covered in STORY-004).
