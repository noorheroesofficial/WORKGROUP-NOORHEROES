---
id: api.ramadan-fasting-logs
kind: api
title: Fasting Log API (POST /v1/ramadan/fasting-logs)
status: draft
owner_story: STORY-036-04
version: 1
created: 2026-09-30
---

## Endpoint

```http
POST /v1/ramadan/fasting-logs
```

## Description
Records a daily fasting status entry for a child, strictly constrained by the parent's configured `fasting_approach`.

## Auth & Security
- **Auth**: Bearer child token via `Depends(get_current_child)` or parent-on-behalf via `Depends(get_current_parent)`.
- **Authorization**:
  - Child can only log for themselves (`session.child_id == request.child_id`).
  - Parent can log on behalf of their own family's child only.
- **Server-Side Approach Enforcement (Child Wellbeing Invariant)**:
  - Validates `status` against the child's live parent-configured `fasting_approach` stored in A.7 Habit Service.
  - `education_only`: Child may ONLY submit `education_only`. Attempts to submit `fasted_full` or `fasted_practice` return `403 FORBIDDEN`.
  - `fasted_practice`: Child may submit `education_only` or `fasted_practice`.
  - `fasted_full`: Child may submit any of `education_only`, `fasted_practice`, or `fasted_full`.
  - Fasting Tracker must be parent-enabled for the child; if disabled, returns `403 FORBIDDEN`.

## Request Body

```ts
export type FastingStatus = 'fasted_full' | 'fasted_practice' | 'education_only';

export interface FastingLogCreateRequest {
  child_id: string; // UUID v4
  night: number;    // integer 1..30
  status: FastingStatus;
  client_timestamp?: string; // ISO 8601 UTC
}
```

## Response — 201 Created / 200 OK

```ts
export interface FastingLogResponse {
  log_id: string;
  child_id: string;
  night_number: number;
  status: FastingStatus;
  logged_at: string; // ISO 8601 UTC timestamp
  message: string;   // Child-safe encouraging message (zero shaming)
}
```

## Errors
- `400 BAD_REQUEST`: Invalid `night` (outside 1..30) or malformed payload.
- `401 UNAUTHORIZED`: Missing or invalid Bearer token.
- `403 FORBIDDEN`:
  - `status` exceeds parent-configured approach (`"Selected fasting option is not permitted under the current parental settings."`).
  - Fasting tracker is disabled by parent (`"Fasting tracker is not enabled for this profile."`).
  - Cross-child or cross-family access violation.
- `409 CONFLICT`: Duplicate submission for same night (if strict unique; updates allowed with idempotent 200 OK).

## Invariants
1. Hard boundary: Zero possibility of an `education_only` child submitting `fasted_full` or `fasted_practice`.
2. Append-only storage: Historical log entries are permanent; mid-season parent changes to `fasting_approach` never mutate past entries.
3. Anti-shaming: Error responses and rejection messages use gentle, non-pressuring terminology.
