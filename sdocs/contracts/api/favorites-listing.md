---
id: api.favorites-listing
kind: api
title: Child Favorites Listing & Type-Filtered Retrieval Endpoint (GET /v1/children/{id}/favorites)
status: stable
owner_story: STORY-003
version: 1
created: 2026-09-29
---

## Endpoint

```http
GET /v1/children/{id}/favorites
```

## Request

### Path Parameters
- `id` (string, required): Child profile identifier (UUIDv7/UUIDv4 string). Must equal the authenticated child profile (`session.child_id`).

### Query Parameters
- `type` (string, optional): Content type filter. Supported: `"story"`, `"surah"`, `"dua"`, `"all"`. Case-insensitive with whitespace trimming. Omitted or `"all"` returns all favorited content types.
- `cursor` (string, optional): Opaque URL-safe base64 keyset pagination cursor token.
- `limit` (integer, optional, default: 20): Maximum items to return per page. Clamped to range `[1, 50]`.

### Headers
- `Authorization` (string, required): Bearer token for active **child-mode** session.
- `X-Locale` / `Accept-Language` (string, optional): Preferred locale for content title localization (e.g. `"en"`, `"ar"`, `"ur"`, `"hi"`).

## Response — 200 OK

```ts
export interface FavoriteItemResponse {
  id: string; // Favorite row UUID
  contentId: string; // Resolved canonical content ID (or episodeId)
  contentType: "story" | "surah" | "dua";
  originalEpisodeId?: string | null; // Set when series restructured from legacy episode
  seriesId?: string | null; // Associated series ID for story episodes
  seriesTitle?: string | null; // Associated series title
  episodeNumber?: number | null; // Episode number within series
  title: string; // Localized title
  thumbnailUrl?: string | null; // Content or series cover artwork URL
  durationSeconds?: number | null; // Content duration in seconds
  available: boolean; // Server-authoritative content availability flag
  isAvailable: boolean; // Dual-wire alias auto-synchronized with available
  favoritedAt: string; // ISO 8601 UTC timestamp of bookmark creation
  episodeId?: string; // Legacy dual-wire alias for contentId
}

export interface FavoriteListResponse {
  items: FavoriteItemResponse[]; // Standard PageResult items collection
  nextCursor?: string | null; // Opaque base64 token for next page (null when hasMore is false)
  hasMore: boolean; // True if more items exist beyond current page
  favorites?: FavoriteItemResponse[]; // Dual-wire compatibility property alias for items
}
```

## Errors

- `401 UNAUTHENTICATED`: Missing or expired Bearer token.
- `403 FORBIDDEN`:
  - Path parameter `{id}` does NOT match authenticated `session.child_id` (attempted sibling or cross-family access).
  - Calling with a parent-mode session token.
- `422 VALIDATION_ERROR`:
  - Unsupported `type` query parameter (e.g. `"podcast"`, `"book"`, `"video"`).
  - Malformed or invalid pagination `cursor` token (`code: "INVALID_CURSOR"`).
- `405 METHOD_NOT_ALLOWED`: Mutating HTTP methods (`POST`, `PUT`, `DELETE`, `PATCH`) called on this read-only endpoint.

## Core Invariants & Zero-Missing-Scenarios Guarantees

1. **Strict Sibling Isolation (CI-Blocking Signature Gate):** Server-side verification comparing path `{id}` against `session.child_id`. Mismatches unconditionally return HTTP 403 Forbidden with localized message `"Cannot access favorites of another child"`. Cross-child access is never silently rescoped.
2. **Withdrawn Content Preservation (FR-7, PRD §5 Item 4):** When content is withdrawn or archived, the favorite row is NEVER purged from the database. The endpoint returns `available: false` and `is_available: false`.
3. **Cascading Parent Series Withdrawal:** When an episode itself is active (`is_withdrawn: false`) but its parent series is withdrawn (`is_withdrawn: true`), the endpoint resolves `available: false`.
4. **Canonical Restructuring Resolution:** Restructured episodes transparently resolve to the canonical `content_id` and updated title/thumbnail while preserving `original_episode_id`. If canonical series is withdrawn, resolves `available: false`.
5. **Dua Withdrawal Resolution:** Withdrawn Duas resolve to `available: false` with localized title, preserving the favorite record.
6. **Surah Dynamic Access Checking:** Dispatches to registered surah access checkers dynamically.
7. **Orphan / Purged Content Degradation:** Missing catalog references gracefully degrade with `available: false` and title `"Story Episode"` or `"Dua"`, never throwing unhandled 500 errors.
8. **Keyset Cursor Pagination (Zero Duplicates):** Paginates deterministically on `(created_at DESC, id DESC)`. Limit clamped to `[1, 50]`.
9. **Redis Short-TTL Caching & Resiliency:** Caches responses under `favorites:{child_id}:{type}:{cursor}:{limit}` with 60s TTL. Instant cache purge on favorite toggle mutations. Graceful fallback to database queries if Redis is unavailable.
10. **Dual-Wire Wire Compatibility:** Full dual-wire support for both `camelCase` (`contentId`, `isAvailable`, `nextCursor`) and `snake_case` (`content_id`, `is_available`, `next_cursor`).
