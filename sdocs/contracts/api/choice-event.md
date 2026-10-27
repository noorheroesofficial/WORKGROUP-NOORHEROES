---
id: api.choice-event
kind: api
title: Interactive Choice Event API (POST /v1/content/{id}/choice)
status: draft
owner_story: STORY-019
version: 1
created: 2026-09-29
---

# Contract: api.choice-event

- **Kind**: API
- **Endpoint**: `POST /v1/content/{id}/choice`
- **Source**: `NoorHeroes-Backend/src/noorheroes/modules/content/choice_schemas.py` & `Development_Blueprints/A3_Stories_Module/KMP/04-interactive-choice-quiz-moment-overlays.md` (B-05)
- **Owner Story**: `STORY-019`
- **Status**: Draft

## Request Specification
- **Method**: `POST`
- **Path Parameter**: `id: String` (Episode content ID, e.g. `ep_01H8XVMQ2G0000000000000011`)
- **Headers**:
  - `Authorization: Bearer <child_token>` (Child session required)
  - `Content-Type: application/json`

### Body (JSON)
```json
{
  "choicePointId": "cp_01H8XVMQ2G0000000000000001",
  "selectedOptionId": "opt_trust",
  "clientEventId": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Invariants
1. `choicePointId`: Non-empty ID matching a scripted choice point in the manifest.
2. `selectedOptionId`: Valid option ID selected by the child learner.
3. `clientEventId`: Cryptographically valid UUID v4 string enforcing idempotency and preventing duplicate recording on replay/retry.
4. Non-Blocking Execution: Client-side branch playback must NEVER wait on this network request. It is fire-and-forget from the player perspective.

## Response Specification (200 OK)
```json
{
  "branchContentRef": "segment_fire_walk_forward"
}
```

## Error Specification
- `400 Bad Request`: Malformed UUID or empty IDs.
- `401 Unauthorized`: Missing or invalid Bearer token.
- `404 Not Found`: Choice point or content ID does not exist.
- Network Outage: Failed transmissions are queued in a local `core-datastore` outbox and synchronized upon reconnection.
