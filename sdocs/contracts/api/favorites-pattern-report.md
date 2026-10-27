---
id: api.favorites-pattern-report
kind: api
title: Admin Favoriting Pattern Monitor API Endpoint (GET /admin/v1/favorites/pattern-report)
status: stable
owner_story: STORY-004
version: 1
created: 2026-09-29
---

## Endpoint

```http
GET /admin/v1/favorites/pattern-report
```
Canonical Alias:
```http
GET /v1/admin/favorites/pattern-report
```

## Request

### Query Parameters
- `content_type` (string, optional): Filter by content type (`"story"`, `"surah"`, `"dua"`). Whitespace-trimmed, case-insensitive. `"all"`, `""`, or omitted retrieves all content types. Any unknown value returns HTTP 422 `VALIDATION_ERROR`.
- `date_from` / `from` / `start_date` (string, optional): Start date bounding in ISO-8601 (`YYYY-MM-DDTHH:MM:SSZ`) or date (`YYYY-MM-DD`) format.
- `date_to` / `to` / `end_date` (string, optional): End date bounding in ISO-8601 or date format.
- `limit` (integer, optional, default: 50): Maximum number of items to return in the ranking. Clamped to `[1, 100]`.
- `order` (string, optional, default: `"desc"`): Sort direction. `"desc"` for most frequently favorited items, `"asc"` for least frequently favorited items.

### Headers
- `Authorization` (string, required): Admin Bearer JWT with `content_editor`, `admin:read`, or `*` scope.
- `X-Correlation-ID` / `X-Request-ID` (string, optional): End-to-end tracing identifier.

### Validation Invariants
- If both `date_from` and `date_to` are provided, `date_from <= date_to` must hold. Violations return HTTP 422.
- Date string parsing validates standard ISO-8601 / calendar formats; invalid formats return HTTP 422.

---

## Response — 200 OK

```ts
export interface FavoritingPatternItem {
  contentId: string;       // Unique content item identifier (story episode, surah, or dua)
  contentType: "story" | "surah" | "dua"; // Type classification
  favoriteCount: number;    // Aggregate bookmark count across all children platform-wide
  title?: string | null;   // Localized content title if resolvable, else null
}

export interface FavoritingPatternReportSummary {
  totalFavorites: number;        // Sum of all bookmarks across filtered items
  uniqueContentCount: number;    // Count of distinct content items in the dataset
  contentTypeFilter?: string | null; // Filter applied (null if all types included)
  dateFrom?: string | null;      // ISO string of date bounding start
  dateTo?: string | null;        // ISO string of date bounding end
  order: "desc" | "asc";         // Sort order applied
}

export interface FavoritingPatternReportResponse {
  items: FavoritingPatternItem[];
  summary: FavoritingPatternReportSummary;
  total: number; // Count of items in this response page
}
```

### JSON Response Example

```json
{
  "items": [
    {
      "contentId": "ep_01H8XVMQ2G0000000000000011",
      "contentType": "story",
      "favoriteCount": 142,
      "title": "The Brave Little Falcon"
    },
    {
      "contentId": "surah_001",
      "contentType": "surah",
      "favoriteCount": 98,
      "title": null
    },
    {
      "contentId": "dua_morning_01",
      "contentType": "dua",
      "favoriteCount": 45,
      "title": null
    }
  ],
  "summary": {
    "totalFavorites": 285,
    "uniqueContentCount": 3,
    "contentTypeFilter": null,
    "dateFrom": "2026-09-01T00:00:00Z",
    "dateTo": "2026-09-29T23:59:59Z",
    "order": "desc"
  },
  "total": 3
}
```

---

## Critical Structural Privacy Invariant (PRD §8, §9, §12.5)

- **Zero Per-Child Exposure**: Sourced exclusively from aggregate queries (`COUNT(*)` grouped by `(content_id, content_type)`).
- **Zero Identifying Columns**: The endpoint and underlying query NEVER select, group by, filter by individual child, or serialize any `child_id`, child name, parent identifier, or family account token.
- **Pure Aggregate Signal**: Designed purely as a content curation and editorial health signal for the Next.js Admin Portal.

---

## Errors

| Status | Code | Cause |
|---|---|---|
| `401` | `UNAUTHENTICATED` | Missing or invalid admin Bearer JWT token |
| `403` | `FORBIDDEN` | Missing required admin scope (`content_editor`, `admin:read`, `*`) or caller is a child/parent token |
| `405` | `METHOD_NOT_ALLOWED` | Read-only endpoint; POST, PUT, DELETE, PATCH return 405 in Universal Error Envelope |
| `422` | `VALIDATION_ERROR` | Unsupported `content_type`, invalid date string format, or `date_from > date_to` |
| `500` | `INTERNAL_SERVER_ERROR` | Database or unexpected error; formatted in Universal Error Envelope |
