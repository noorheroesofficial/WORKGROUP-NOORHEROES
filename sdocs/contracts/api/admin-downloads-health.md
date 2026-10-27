---
id: api.admin-downloads-health
kind: api
title: Admin Download & Sync Health Monitoring API (GET /v1/admin/downloads/health & GET /v1/admin/sync/health)
status: stable
owner_story: TASK-B07
version: 1
created: 2026-09-29
---

## Endpoints

```http
GET /v1/admin/downloads/health?window=72h
GET /v1/admin/sync/health?window=72h
```

## Auth & Security

- **Auth**: Bearer admin session token via `Depends(get_current_admin)`.
- **RBAC**: Requires at least one allowed scope or role: `admin:read`, `trust_safety`, `product_admin`, `super_admin`, or `*` (`Depends(require_any_scope(...))`).
- **Privacy Gate**: Strictly zero child or family identifying PII (aggregate rates and counts only).
- **Read-Only**: Purely operational aggregation surface; mutating HTTP methods (`POST`, `PUT`, `DELETE`, `PATCH`) return `405 Method Not Allowed`.
- **Anti-Caching Headers**:
  - `Cache-Control: no-store, no-cache, must-revalidate, private`
  - `Pragma: no-cache`

## Query Parameters

| Name | Type | Allowed Values | Default | Description |
|---|---|---|---|---|
| `window` | string | `24h`, `72h`, `7d`, `30d` | `72h` | Aggregation time window bounding the historical query range. |

---

## 1. Manifest Health Response — 200 OK

```ts
export interface ManifestHealthBucket {
  bucket: string; // ISO 8601 UTC hourly timestamp, e.g. "2026-08-17T00:00:00Z"
  issued: number; // Count of successfully issued download manifests
  cap_rejected: number; // Count of requests rejected due to storage cap
  entitlement_rejected: number; // Count of requests rejected due to missing entitlement / parental lock
  url_reissue_count: number; // Count of re-issued or resumed download URLs
}

export interface ManifestHealthResponse {
  series: ManifestHealthBucket[];
}
```

---

## 2. Sync Integrity Health Response — 200 OK

```ts
export interface SyncIntegrityBucket {
  bucket: string; // ISO 8601 UTC hourly timestamp, e.g. "2026-08-17T00:00:00Z"
  batches_processed: number; // Ingested client sync batch count
  events_applied: number; // Successfully applied domain events
  events_duplicate_prevented: number; // Positive signal: duplicate events correctly caught & prevented
  events_rejected: number; // Malformed or invalid events rejected
}

export interface RejectedEventTypeCount {
  event_type: string; // Classification identifier (e.g. "quiz_response", "habit_checkin")
  count: number; // Total rejection count for this event type
}

export interface SyncIntegrityHealthResponse {
  series: SyncIntegrityBucket[];
  rejected_by_event_type: RejectedEventTypeCount[];
}
```

---

## Errors

- `401 UNAUTHENTICATED`: Missing, expired, or invalid admin Bearer token (or child token provided).
- `403 FORBIDDEN`: Valid admin token lacking `admin:read`, `trust_safety`, or `product_admin` scopes.
- `405 METHOD NOT ALLOWED`: Mutation requests (`POST`, `PUT`, `DELETE`, `PATCH`) to monitoring endpoints.
- `422 VALIDATION_ERROR`: Unsupported `window` query parameter (e.g., `12h`, `1d`, `foo`).

---

## Architectural Guarantees & Invariants

1. **Positive Signal Framing (Blueprint B-07 §5 / §11)**:
   - `events_duplicate_prevented` represents deduplication health (positive signal), never alarmist framing.
2. **Short-TTL Redis Caching with Graceful DB Fallback (Blueprint B-07 §10 / §18)**:
   - Cached in Redis for 60 seconds (`admin:health:manifest:{window}`, `admin:health:sync:{window}`) to absorb dashboard refresh spikes.
   - Redis outage or network timeout gracefully falls through to database query without failing the request (returns 200 OK).
3. **Empty Window Grace Handling (Blueprint B-07 §18)**:
   - Ranges with zero activity return HTTP 200 with empty series `series: []`, never 404 or 500.
4. **Zero Child PII Exposure (Blueprint B-07 §25 / §30)**:
   - Aggregations expose zero child IDs, family IDs, session IDs, names, or individual content progress.
