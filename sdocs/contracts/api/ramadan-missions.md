---
id: api.ramadan-missions
kind: api
title: Ramadan Mission Content Delivery API (GET /v1/ramadan/missions/{night})
status: draft
owner_story: STORY-036-03
version: 1
created: 2026-09-30
---

## Endpoint

```http
GET /v1/ramadan/missions/{night}
```

## Description
Fetches the designated content unit for a specific Ramadan night (1..30). Reuses E.29's Content Service via `content_version_id` link and delivers server-computed gamification suppression for Laylatul Qadr nights.

## Auth & Security
- **Auth**: Bearer child token via `Depends(get_current_child)` or parent session via `Depends(get_current_parent)`.
- **Authorization**: Standard authenticated session.
- **Server-Computed Suppression Flag**:
  - `gamification_suppressed: true` is computed on the server directly from `ramadan_missions.is_laylatul_qadr`.
  - True for exactly the five odd nights: 21, 23, 25, 27, 29.
  - Clients are strictly prohibited from deriving or overriding this flag.

## Path Parameters
- `night`: integer, `1..30`.

## Response — 200 OK

```ts
export interface MissionContentItem {
  id: string; // content item UUID
  version_id: string; // content_versions UUID (E.29)
  title: string;
  summary: string;
  category: 'story' | 'dua' | 'quran_challenge' | 'charity_mission';
  media_type: 'video' | 'audio' | 'interactive_text';
  duration_seconds: number;
  thumbnail_url: string;
  stream_url?: string;
  dua_arabic_text?: string;
  dua_translation?: string;
  dua_transliteration?: string;
}

export interface RamadanMissionResponse {
  mission_id: string;
  night_number: number; // 1..30
  is_laylatul_qadr: boolean;
  gamification_suppressed: boolean; // true for nights 21, 23, 25, 27, 29
  title: string;
  theme: string; // e.g. "Patience and Gratitude"
  content: MissionContentItem;
  reflection_prompt?: string; // Calmer reflection prompt on Laylatul Qadr
  fasting_tracker_enabled: boolean; // Parent-permissioned flag for current child
  is_unlocked: boolean; // true if night <= current_night (or retroactive)
}
```

## Errors
- `400 BAD_REQUEST`: Night parameter outside range `1..30`.
- `401 UNAUTHORIZED`: Missing or invalid Bearer token.
- `404 NOT_FOUND`: Mission not configured for requested night.
- `409 CONFLICT`: Night requested has not unlocked yet (state: `not_yet_unlocked`). Note: missed past nights remain `200 OK` (retroactive access).

## Invariants
1. `gamification_suppressed === true` strictly if and only if `night_number` in `[21, 23, 25, 27, 29]`.
2. Content data is sourced dynamically via E.29's `ContentService.get_version(content_version_id)`; zero content fields are duplicated in Ramadan tables.
3. Unpublished or unreviewed content drafts are never served (`status === 'published'` required).
4. Retroactive completion: Past missed nights (`night < current_night`) are always returned with `is_unlocked: true`.
