---
id: data.story-cache
kind: repo
title: Story Catalog Cache Interface
status: stable
owner_story: STORY-002
version: 1
created: 2026-09-29
---

## Interface

```ts
export interface StoryCatalogCache {
  getCachedCatalog(filterKey: string): Promise<StoryCatalogPage | null>;
  saveCatalog(filterKey: string, page: StoryCatalogPage): Promise<void>;
  getCachedDownloads(): Promise<Array<StoryItem>>;
  saveCachedDownloads(items: Array<StoryItem>): Promise<void>;
  clear(): Promise<void>;
}
```

## Invariants
- Cache entries have a TTL of 10 minutes.
- Expired cache entries are evicted on subsequent access.
- Downloads category entries are persisted indefinitely until explicit removal.
