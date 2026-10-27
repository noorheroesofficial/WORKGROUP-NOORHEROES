---
id: api.admin-fact-engagement
kind: api
title: Admin Fact Engagement Monitoring API (GET /v1/admin/facts/engagement)
status: stable
owner_story: TASK-B18-07
version: 1
created: 2026-10-13
---

## Endpoint

```http
GET /v1/admin/facts/engagement
```

## Auth & Security

- **Auth**: Bearer token via authenticated admin session (`AdminSessionContext`).
- **Role Requirement**: `require_admin_role("content_editor")`.
- **Read-Only Invariant**: Pure read-only aggregation across operational and telemetry records with zero mutation.
- **Caching**: Short TTL (300s) Redis caching with graceful fail-safe to database evaluation on cache misses or connection errors.

---

## 1. Request Parameters

### Query Parameters

- `topic` (string, optional): Filter aggregates by registered thematic topic slug.
- `date_from` / `from` (datetime, optional): Start timestamp of evaluation window (ISO 8601).
- `date_to` / `to` (datetime, optional): End timestamp of evaluation window (ISO 8601).
- `page` (int, default: 1): 1-indexed page number (>= 1).
- `page_size` (int, default: 20): Bounded page size (1 <= page_size <= 100).

---

## 2. Response Contract — 200 OK

```ts
export interface FactEngagementItem {
  factId: string;
  topic: string;
  textSnippet: string;
  impressionsCount: number;
  viewsCount: number;
  quizStartsCount: number;
  quizCompletionsCount: number;
  viewRate: number;              // views / impressions
  quizEngagementRate: number;    // quizStarts / views
}

export interface TopicAggregateMetric {
  topic: string;
  totalFacts: number;
  aggregateImpressions: number;
  aggregateViews: number;
  averageViewRate: number;
  averageQuizEngagementRate: number;
}

export interface FactEngagementMonitoringResponse {
  items: FactEngagementItem[];
  topicAggregates: TopicAggregateMetric[];
  page: number;
  pageSize: number;
  totalCount: number;
  aiFallbackUsedRate: number;
  scholarApprovalRevocationFrequency: number;
}
```

---

## 3. Error Responses

- `401 UNAUTHORIZED`: Missing or invalid admin Bearer token.
- `403 FORBIDDEN`: Insufficient role (caller lacks `content_editor`).
- `422 UNPROCESSABLE_ENTITY`: Invalid pagination bounds or inverted date range (`date_from > date_to`).
- `503 SERVICE_UNAVAILABLE`: Analytics backend unreachable and no cached response available.
