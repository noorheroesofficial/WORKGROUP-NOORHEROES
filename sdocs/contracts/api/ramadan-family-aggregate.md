---
id: api.ramadan-family-aggregate
kind: api
title: Family Ramadan Aggregate API (GET /v1/ramadan/family-aggregate)
status: draft
owner_story: STORY-036-06
version: 1
created: 2026-09-30
---

## Endpoint

```http
GET /v1/ramadan/family-aggregate
```

## Description
Provides parents with an aggregate overview of the entire family's Ramadan journey and participation without exposing individual sibling comparative data.

## Auth & Security
- **Auth**: Bearer parent token via `Depends(get_current_parent)`.
- **Authorization**: Scoped to the parent's own household only.
- **Structural Anti-Sibling Comparison Guarantee**:
  - The response schema contains **zero per-child array fields** (e.g. no `children: [...]`, no `leaderboard`, no ranked lists).
  - Verifiable via automated schema reflection tests.
  - Multi-child households celebrate collective family milestones without ranking siblings.

## Request

```http
GET /v1/ramadan/family-aggregate HTTP/1.1
Host: api.noorheroes.com
Authorization: Bearer <parent_token>
```
*(No query parameters or request body)*

## Response — 200 OK

```ts
export interface FamilyRamadanAggregateResponse {
  family_id: string;
  season_id: string; // e.g. "ramadan_1448"
  total_nights_in_season: number; // 30
  current_night: number;          // 1..30
  family_missions_completed: number; // Total collective mission completions across all children
  family_lanterns_lit: number;       // Distinct nights with at least one completion in household
  family_participation_rate: number; // 0.0 to 1.0 (family engagement index)
  fasting_participation: {
    education_entries: number;
    practice_entries: number;
    full_fast_entries: number;
  };
  collective_milestones: {
    milestone_id: string;
    title: string;
    achieved: boolean;
    unlocked_at?: string;
  }[];
  is_mid_season_join: boolean; // true if household joined after Ramadan Day 1
}
```

## Response — 200 OK (New Household / Empty State)

```json
{
  "family_id": "f1e2d3c4-...",
  "season_id": "ramadan_1448",
  "total_nights_in_season": 30,
  "current_night": 14,
  "family_missions_completed": 0,
  "family_lanterns_lit": 0,
  "family_participation_rate": 0.0,
  "fasting_participation": {
    "education_entries": 0,
    "practice_entries": 0,
    "full_fast_entries": 0
  },
  "collective_milestones": [],
  "is_mid_season_join": true
}
```

## Errors
- `401 UNAUTHORIZED`: Missing or invalid parent token.
- `403 FORBIDDEN`: Attempting to access another family's data.

## Invariants
1. **Structural Omission**: Under no circumstances does the response contain child IDs, child names, or per-child breakdown arrays.
2. **Graceful Zero Handling**: New households or households joining mid-season receive a valid `200 OK` response with `is_mid_season_join: true`; pre-join nights are treated as not applicable rather than missed.
3. **Caching**: Cached in Redis with short TTL (e.g. 60s), invalidated upon new mission completion or fasting log submission.
