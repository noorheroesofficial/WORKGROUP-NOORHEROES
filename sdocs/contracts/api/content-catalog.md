---
id: api.content-catalog
kind: api
title: Content Catalog Stories API
status: stable
owner_story: STORY-002
version: 1
created: 2026-09-29
---

## Endpoint

```
GET /v1/content
```

## Request Query Parameters

```ts
{
  type: "story";
  category?: string;
  age_band?: "4 to 6" | "6 to 9" | "9 to 12" | "12 to 15" | "15 to 18+";
  locale?: "en" | "hi" | "ur" | "ar";
  format?: "video" | "audio" | "text";
  duration?: "short" | "medium" | "long";
  downloaded_only?: boolean;
  free_premium?: "free" | "premium" | "all";
  cursor?: string;
  limit?: number;
}
```

## Response — 200 OK

```ts
{
  items: Array<{
    id: string;
    seriesId: string;
    title: string;
    synopsis?: string | null;
    category: string;
    ageBands: string[];
    coverUrl?: string | null;
    episodeCount: number;
    scholarApprovalStatus: string;
    isBedtimeEligible: boolean;
    formats: string[];
    totalDurationSeconds: number;
    freeOrPremium: "free" | "premium";
  }>;
  nextCursor?: string | null;
  hasMore: boolean;
}
```

## Errors
- 400 — INVALID_FILTER (unrecognized category or format)
- 401 — UNAUTHORIZED (missing token)
- 403 — FORBIDDEN (parent-mode token used where child-mode required)
- 500 — INTERNAL_SERVER_ERROR

## Headers
- Request: `Authorization: Bearer <child_session_token>`, `X-Locale: <locale>`
- Response: `Content-Type: application/json`
