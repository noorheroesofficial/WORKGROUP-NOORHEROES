---
id: api.favorite-toggle
kind: api
title: Favorite Toggle Endpoint (POST /v1/favorites)
status: stable
owner_story: STORY-001
version: 1
created: 2026-09-29
---

## Endpoint

```http
POST /v1/favorites
```

## Request

```ts
export interface FavoriteToggleRequest {
  contentId: string;
  contentType?: "story" | "surah" | "dua";
  favorited?: boolean; // defaults to true
  clientRequestId?: string; // UUIDv4 / UUIDv7 idempotency key
  episodeId?: string; // backward-compatible alias for contentId
}
```

## Response — 200

```ts
export interface FavoriteToggleResponse {
  favorited: boolean;
  contentId?: string;
  episodeId?: string;
}
```

## Errors

- `401 UNAUTHENTICATED`: Missing or invalid child Bearer token.
- `403 FORBIDDEN`: Attempting to favorite inaccessible/withdrawn content on add path, or non-child session mode.
- `404 EPISODE_NOT_FOUND`: Referenced item not found in catalog.
- `422 VALIDATION_ERROR`: Missing `contentId`/`episodeId` or unsupported `contentType`.

## Invariants

- Endpoint strictly acts upon authenticated child session's `child_id`.
- Toggle is optimistic and idempotent (`clientRequestId`).
- Accessibility validation is enforced on add (`favorited: true`) and skipped on remove (`favorited: false`).
- Database uniqueness on `(child_id, content_id, content_type)` guarantees zero duplicate rows.

## Notes

- Supercedes legacy separate POST/DELETE verbs per Feature B.14 / Blueprint B-01.
