---
id: api.playback-heartbeat
kind: api
title: Playback Heartbeat API (POST /v1/playback/{content_id})
status: draft
owner_story: STORY-012
version: 1
created: 2026-09-29
---

# Contract: api.playback-heartbeat

- **Kind**: API
- **Endpoint**: `POST /v1/playback/{content_id}`
- **Source**: `NoorHeroes-Backend/src/noorheroes/modules/content/playback_schemas.py` & `Development_Blueprints/A3_Stories_Module/KMP/03-story-player-core-playback-engine.md` (B-03)
- **Owner Story**: `STORY-012`
- **Status**: Draft

## Request Specification
- **Method**: `POST`
- **Path Parameter**: `content_id: String` (Episode content ID, e.g. `ep_01H8XVMQ2G0000000000000011`)
- **Headers**:
  - `Authorization: Bearer <child_token>` (Child session required)
  - `Content-Type: application/json`

### Body (JSON)
```json
{
  "eventType": "heartbeat",
  "positionSeconds": 142,
  "clientEventId": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Invariants
1. `eventType`: Enum `"heartbeat"` or `"seek"`.
2. `positionSeconds`: Non-negative integer representing current playback position.
3. `clientEventId`: Cryptographically valid UUID v4 generated once at session init and reused across all heartbeats and retries for this playback session.
4. Throttling: Must only be transmitted every 5–10s of actual playback time (never fired while paused or buffering).

## Response Specification (200 OK)
```json
{
  "acknowledged": true
}
```

## Error Specification
- Non-blocking contract: Any HTTP error or network timeout must fail gracefully and NEVER interrupt active media playback.
