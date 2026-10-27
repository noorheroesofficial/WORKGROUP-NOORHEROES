---
id: type.favorite-models
kind: type
title: Favorite Persistence Entity and DTOs
status: stable
owner_story: STORY-001
version: 1
created: 2026-09-29
---

## Shape

```ts
export interface FavoriteEntity {
  id: string; // UUIDv7
  childId: string; // UUID of child profile
  contentId: string; // UUID of favorited story/surah/dua
  contentType: "story" | "surah" | "dua";
  episodeId?: string | null; // Legacy foreign key to story_episode
  createdAt: string; // ISO 8601 UTC timestamp
}

export interface FavoriteToggleDTO {
  childId: string;
  contentId: string;
  contentType: string;
  favorited: boolean;
  clientRequestId?: string | null;
}

export interface FavoriteListItemDTO {
  id: string;
  contentId: string;
  contentType: "story" | "surah" | "dua";
  originalEpisodeId?: string | null;
  seriesId?: string | null;
  seriesTitle?: string | null;
  episodeNumber?: number | null;
  title: string;
  thumbnailUrl?: string | null;
  durationSeconds?: number | null;
  available: boolean;
  isAvailable: boolean;
  favoritedAt: string;
  episodeId?: string;
}

export interface FavoriteListResponseDTO {
  items: FavoriteListItemDTO[];
  nextCursor?: string | null;
  hasMore: boolean;
  favorites?: FavoriteListItemDTO[];
}
```

## Invariants

- Composite unique constraint `(child_id, content_id, content_type)`.
- `content_type` constrained to enum set: `story`, `surah`, `dua`.
- Cascade delete on referenced `episode_id` if story episode is purged.
- No soft-delete on `favorite` table; unfavoriting deletes row.

## Notes

- Shared table referenced by Stories (A.3), Quran/Arabic (A.5), and Dua Learning (A.6).
