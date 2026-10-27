---
id: api.in-app-notifications
kind: api
title: In-App Notification Fetch API (GET /v1/notifications/in-app)
status: stable
owner_story: TASK-B17-09
version: 1
created: 2026-10-09
---

## Endpoint

```http
GET /v1/notifications/in-app
```

## Auth & Security

- **Auth**: Bearer token via authenticated child session (`ChildSessionContext` / `get_current_child`).
- **Security Invariant (Blueprint B-09 §15, §25)**: Scoped strictly to the authenticated child's own `target_child_id`. Never returns sibling notifications on a shared device, ensuring strict profile isolation and zero cross-child notification leakage.
- **Read-Only Projection (Blueprint B-09 §5, §10)**: This endpoint queries already-`sent`, policy-approved notification intents. It NEVER triggers fresh policy evaluations or mutations at fetch time.

---

## 1. Request Parameters

None (read-only query against the authenticated child session context).

---

## 2. Response Contracts

### 2.1 Success Response — 200 OK

```ts
export interface InAppNotificationItem {
  instanceId: string;           // RFC 9562 UUIDv7 notification intent identifier (instance_id)
  type: string;                 // Trigger class: "new_content", "episode_ready", "daily_reminder", etc.
  renderedCopy: string;         // Pre-rendered, child-safe, policy-approved notification copy (rendered_copy)
  destination: string;          // Deep-link destination route identifier (e.g. "story_detail", "home")
  params?: Record<string, any>; // Optional routing parameters (e.g. {"contentId": "story_123"})
  expiresAt?: string | null;    // Expiration timestamp in ISO 8601 UTC (expires_at)
}

export interface InAppNotificationListResponse {
  notifications: InAppNotificationItem[];
}
```

*Note: Dual-wire compatibility supports both camelCase (`instanceId`, `renderedCopy`, `expiresAt`) and snake_case (`instance_id`, `rendered_copy`, `expires_at`).*

---

## 3. Error Responses

- `401 UNAUTHORIZED`: Missing, invalid, or expired child session Bearer token.
- `405 METHOD_NOT_ALLOWED`: Mutating HTTP methods (`POST`, `PUT`, `DELETE`, `PATCH`) are disallowed on read-only projection endpoint.
- `500 INTERNAL_SERVER_ERROR`: Database connectivity failure (client falls back to not rendering banner without crashing).

---

## 4. Core Invariants & System Behavior

| Scenario | System Behavior |
|:---|:---|
| **Eligible In-App Notifications Present** | Returns `200 OK` with populated `notifications` list containing pre-rendered copy and destination routing. |
| **No Eligible Notifications** | Returns `200 OK` with an empty `notifications: []` array, never an error code. (Blueprint B-09 §18) |
| **Expired Notifications** | Notifications where `expires_at <= now` are automatically filtered out and excluded from the response. (Blueprint B-09 §144) |
| **Sibling Profile Isolation** | When Child A and Child B share a device, Child A's call returns ONLY intents where `target_child_id == child_a_id`. Child B's intents are completely invisible to Child A. |
| **Client-Side Dismissal** | Dismissal is tracked locally on the mobile client (K-03); the backend returns all currently-eligible instances and the client suppresses previously-dismissed `instanceId` items. |
| **Non-In-App Notification Types** | Filtered out at query time; only recognized in-app-eligible trigger classes are returned. |
| **Unauthenticated Request** | Returns `401 UNAUTHORIZED` with the Universal Error Envelope. |
