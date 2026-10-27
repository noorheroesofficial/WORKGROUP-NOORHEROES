---
id: api.ramadan-journey-progress
kind: api
title: Ramadan Journey Progress & Reward Completion API (POST /v1/ramadan/missions/{night}/complete)
status: draft
owner_story: STORY-036-05
version: 1
created: 2026-09-30
---

## Endpoint

```http
POST /v1/ramadan/missions/{night}/complete
```

## Description
Marks a night's mission complete, lights the lantern on the child's Journey Map, and triggers reward/badge issuance via A.11's hardened reward engine. Guarantees safe idempotent replay.

## Auth & Security
- **Auth**: Bearer child token via `Depends(get_current_child)`.
- **Authorization**: Child can only mark completion for their own session (`child_id` resolved server-side from session context; never accepted in request body).
- **Idempotency & Replay Safety (Critical Guarantee #2)**:
  - Database primary key `(child_id, mission_id)` in `ramadan_journey_progress` prevents duplicate records.
  - Replayed calls return `200 OK` with `already_completed: true` and the original reward summary.
  - Exactly one reward transaction is ever dispatched to A.11's `RewardService` and written to `reward_ledger`.

## Path Parameters
- `night`: integer, `1..30`.

## Request Body
*(No request body required; child session + night path parameter fully define target).*

## Response — 200 OK (First Completion)

```ts
export interface SeasonalRewardGrant {
  ledger_id: string; // UUID in shared reward_ledger
  points_awarded: number;
  badge_earned?: {
    badge_id: string;
    season_id: string; // e.g. "ramadan_1448"
    title: string;
    icon_url: string;
  };
  total_lanterns_lit: number; // 1..30
}

export interface MissionCompleteResponse {
  mission_id: string;
  child_id: string;
  night_number: number;
  completed_at: string; // ISO 8601 UTC timestamp
  already_completed: false;
  lantern_lit: true;
  reward: SeasonalRewardGrant;
}
```

## Response — 200 OK (Idempotent Replay)

```json
{
  "mission_id": "c1f7b9e0-...",
  "child_id": "a2b3c4d5-...",
  "night_number": 12,
  "completed_at": "2027-02-19T18:24:12Z",
  "already_completed": true,
  "lantern_lit": true,
  "reward": {
    "ledger_id": "e9d8c7b6-...",
    "points_awarded": 50,
    "badge_earned": null,
    "total_lanterns_lit": 12
  }
}
```

## Errors
- `401 UNAUTHORIZED`: Missing or invalid child Bearer token.
- `404 NOT_FOUND`: Mission unconfigured for this night in active campaign.
- `409 CONFLICT`: Future night not yet unlocked (unless retroactive access policy applies).

## Invariants
1. Database constraint `UNIQUE(child_id, mission_id)` strictly enforced.
2. Shared reward engine: All reward allocations route through A.11's `RewardService` and land in `reward_ledger`. Zero parallel reward tables.
3. Retroactive completion: Past missed nights remain completable retroactively at any subsequent point in the season.
4. Partial-failure resilience: If reward engine issuance experiences temporary downtime after progress row insertion, progress is preserved and an alertable partial-failure is logged for retry.
