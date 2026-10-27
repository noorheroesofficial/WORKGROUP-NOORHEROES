---
id: api.sync-batch
kind: api
title: Offline Sync Batch Ingestion API (POST /v1/sync/batch)
status: stable
owner_story: TASK-B04
version: 1
created: 2026-09-29
---

## Endpoint

```http
POST /v1/sync/batch
POST /v1/downloads/sync/batch (module parity alias)
```

## Auth & Security

- **Auth**: Bearer (child session token via `Depends(get_current_child_session)`)
- **Headers**:
  - `Cache-Control: no-store, no-cache, must-revalidate, private`
  - `Pragma: no-cache`

## Request

```ts
export interface SyncEventRequest {
  eventType: string; // e.g. "habit_checkin" | "quiz_response" | "story_progress" | "audio_progress" | "content_progress" | "reward_claim" | "points_earned"
  clientEventId: string; // Client-generated UUID string
  occurredAt: string; // ISO 8601 UTC timestamp
  payload: Record<string, unknown>; // Domain-specific event payload
}

export interface SyncBatchRequest {
  events: SyncEventRequest[]; // Bounded array: 1 <= length <= 500
}
```

## Response — 200 OK

```ts
export interface ProcessedEvent {
  clientEventId: string;
  status: "applied" | "duplicate" | "rejected";
  error?: string | null;
}

export interface SyncBatchResponse {
  processed: ProcessedEvent[];
}
```

## Errors

- `401 UNAUTHENTICATED`: Missing or invalid child Bearer token.
- `403 FORBIDDEN`: Non-child session token (parent tokens rejected).
- `422 VALIDATION_ERROR`: Empty events list, batch exceeding 500 events, or missing required fields (`clientEventId`, `eventType`, `occurredAt`).

## Architectural Guarantees & Invariants

1. **Causal In-Memory Sort**: Events sorted strictly by `occurred_at` ascending before processing. Furthest-valid-position stability on identical timestamps.
2. **Pre-Downstream Dedup**: Checked against `sync_event_log` via single `IN (...)` SQL query. Already applied events return `status='duplicate'` with **zero downstream service invocations**.
3. **Idempotency Pass-Through**: New events routed via `EVENT_TYPE_HANDLERS` passing `client_event_id` as the downstream idempotency key.
4. **Partial Failure Isolation**: Downstream failures leave event un-logged in `sync_event_log` for client retry; other valid events in the batch apply without head-of-line blocking.
5. **Concurrent Race Safety**: Nested transaction savepoints (`begin_nested`) resolve simultaneous duplicate insertions without aborting the transaction.
6. **Transactional Outbox**: Emits `OfflineSyncBatchIngested` (`offline_sync.batch_ingested`) capturing batch ingestion metrics.
