---
id: domain.story-library
kind: repo
title: Story Library Repository & Domain Interface
status: stable
owner_story: STORY-003
version: 1
created: 2026-09-29
---

## Interface

```ts
export interface StoryCatalogRepository {
  getStoriesLibrary(filters: StoryFilter): Promise<NoorResult<StoryLibraryResult>>;
  getDownloadedStories(): Promise<Array<StoryItem>>;
}
```

## Types

```ts
export interface StoryLibraryResult {
  rails: Array<CategoryRail>;
  hasMore: boolean;
  nextCursor?: string | null;
  isOffline: boolean;
}

export interface CategoryRail {
  category: StoryCategory;
  title: string;
  items: Array<StoryItem>;
  isEmpty: boolean;
}

export interface StoryItem {
  id: string;
  seriesId: string;
  title: string;
  subtitle?: string | null;
  category: StoryCategory;
  ageBand: string;
  durationMinutes: number;
  coverUrl?: string | null;
  episodeCount: number;
  isDownloaded: boolean;
  progressPercent: number;
  isCompleted: boolean;
  isBedtimeEligible: boolean;
  isFree: boolean;
}
```

## Error Semantics
- Network failures fall back to cached data with `isOffline = true`.
- Downloads category read is 100% cache-first with zero network requirement.
