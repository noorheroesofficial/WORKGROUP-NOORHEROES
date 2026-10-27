---
id: api.deep-link-resolution
kind: api
title: Notification Deep Link Resolution API (GET /v1/notifications/resolve)
status: stable
owner_story: TASK-B17-06
version: 1
created: 2026-10-09
---

## Endpoint

```http
GET /v1/notifications/resolve?deep_link_token={token}
```

## Auth & Security

- **Auth**: Bearer token via active session (`DeviceCallerContext`, supporting both parent and child session modes).
- **Security Invariant (PRD FR-5)**: Deep links never grant a bypass past in-app security controls, session authentication, or profile boundaries. Every open re-evaluates session validity, child-profile matching, content availability, and parent gate checks on the backend.
- **Anti-Bypass Protection**: Raw notification payload destination is never trusted without this server round-trip.

---

## 1. Request Parameters

```ts
export interface DeepLinkResolveParams {
  deep_link_token: string; // Originating RFC 9562 delivery UUIDv7 or intent token
}
```

---

## 2. Response Contracts

### 2.1 Success Response — 200 OK (`valid: true`)

```ts
export interface DeepLinkResolveSuccessResponse {
  valid: true;
  destination: string;           // e.g. "habit_builder", "bedtime_player", "story_player"
  params?: Record<string, any>;  // Destination arguments (e.g. {"habitId": "habit_123"})
  deliveryId?: string;           // Originating delivery record UUIDv7
}
```

### 2.2 Re-Route / Fallback Response — 200 OK (`valid: false`)

```ts
export type DeepLinkResolutionReason =
  | "child_mismatch"        // Opened by sibling profile -> re-routes to Who Is Learning
  | "content_unavailable"   // Target content withdrawn since send -> falls back to Home
  | "requires_lock_gate"    // Destination requires Parent Gate / PIN lock verification
  | "session_expired";      // Active session expired or invalid -> falls back to Login

export interface DeepLinkResolveFallbackResponse {
  valid: false;
  reason: DeepLinkResolutionReason;
  fallbackDestination: "who_is_learning" | "home" | "parent_gate" | "login" | string;
  deliveryId?: string;
}
```

*Note: Dual-wire compatibility supports both camelCase (`fallbackDestination`, `deliveryId`) and snake_case.*

---

## 3. Error Responses

- `401 UNAUTHORIZED`: Missing or invalid session Bearer token.
- `404 DEEP_LINK_NOT_FOUND`: Token cannot be resolved to any delivery or intent record.
- `500 INTERNAL_SERVER_ERROR`: Unhandled server exception.

---

## 4. Core Invariants & System Behavior

| Scenario | System Behavior |
|:---|:---|
| **Child Mismatch** (Notification intended for Child A opened while Child B is active) | Returns `valid: false, reason: "child_mismatch", fallbackDestination: "who_is_learning"`. Never routes into Child A's state; does NOT update `opened_at` receipt. (PRD §5 Item 5, Edge Case 2) |
| **Child Match** (Notification intended for Child A opened while Child A is active) | Returns `valid: true, destination: "...", params: {...}`. Updates `notification_deliveries.opened_at` and `status='opened'`. Emits `NotificationOpened` and `NotificationDeepLinkResolved`. |
| **Parent Gate Required** (Child session taps parent-gated link) | Returns `valid: false, reason: "requires_lock_gate", fallbackDestination: "parent_gate"`. |
| **Content Withdrawn** (Story or episode withdrawn/archived since send) | Returns `valid: false, reason: "content_unavailable", fallbackDestination: "home"`. Zero client crash. (PRD Edge Case 4) |
| **Session Expired** (Active session expired or invalid) | Returns `valid: false, reason: "session_expired", fallbackDestination: "login"`. |
| **Offline Handling** | Server round-trip is mandatory; client shows reconnect state when unreachable without attempting local-only bypass. (PRD Edge Case 5) |
