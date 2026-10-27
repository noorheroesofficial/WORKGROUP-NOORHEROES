---
id: api.ramadan-campaign-status
kind: api
title: Ramadan Campaign Status API (GET /v1/ramadan/campaign-status)
status: draft
owner_story: STORY-036-01
version: 1
created: 2026-09-30
---

## Endpoint

```http
GET /v1/ramadan/campaign-status
```

## Description
Returns the active Ramadan campaign lifecycle state, current night number, and authoritative dates for the authenticated parent's household.

## Auth & Security
- **Auth**: Bearer parent session token via `Depends(get_current_parent)`.
- **Authorization**: Standard authenticated parent access; no elevated scope required for status check.
- **Server-Side Region Resolution (Critical Security Invariant)**:
  - The caller's `region` is resolved **exclusively** from the authenticated parent's Profile record on the server.
  - Zero `region` parameter is accepted or recognized on the request query/body (structural guarantee).
  - Any client-supplied region parameter in query string or headers is completely ignored.

## Request

```http
GET /v1/ramadan/campaign-status HTTP/1.1
Host: api.noorheroes.com
Authorization: Bearer <parent_token>
```
*(No query parameters or request body)*

## Response — 200 OK

```ts
export type RamadanCampaignPhase =
  | 'pre_ramadan_countdown' // 14 days before start date
  | 'active'                 // 30 days active journey
  | 'laylatul_qadr'          // Nights 21, 23, 25, 27, 29 active
  | 'eid_transition'         // Last 2 days + Eid day
  | 'eid_celebration'        // 3 days of Eid
  | 'post_eid_tail'          // 14 days post-Eid habit transition
  | 'not_active';            // Season unconfigured or outside activation window

export interface CampaignStatusResponse {
  phase: RamadanCampaignPhase;
  current_night: number | null; // 1..30 when phase in active/laylatul_qadr/eid_transition; null otherwise
  hijri_start_date: string | null; // ISO 8601 Date (YYYY-MM-DD), e.g. "2027-02-08"
  eid_date: string | null; // ISO 8601 Date (YYYY-MM-DD), e.g. "2027-03-10"
  eid_date_overridden: boolean; // true if adjusted via moon-sighting admin override
  server_time: string; // ISO 8601 UTC timestamp, e.g. "2027-02-19T18:00:00Z"
}
```

## Response — 200 OK (Unconfigured / Inactive Region)

```json
{
  "phase": "not_active",
  "current_night": null,
  "hijri_start_date": null,
  "eid_date": null,
  "eid_date_overridden": false,
  "server_time": "2026-11-15T12:00:00Z"
}
```

## Errors
- `401 UNAUTENTICATED`: Missing, invalid, or expired parent Bearer token.
- `500 INTERNAL_SERVER_ERROR`: Unhandled database or calendar service failure.

## Invariants
1. `current_night` is non-null if and only if `phase` is one of `['active', 'laylatul_qadr', 'eid_transition']`.
2. `current_night` satisfies `1 <= current_night <= 30`.
3. When `phase == 'not_active'`, response status code is strictly `200 OK` (never 404 or 400).
4. `server_time` is the authoritative clock for client UI synchronization; clients never rely on device local clock.

## Proposed Admin Campaign CRUD Endpoints (Supervised)

```http
GET /v1/admin/ramadan/campaigns?page=1&page_size=20
POST /v1/admin/ramadan/campaigns
PATCH /v1/admin/ramadan/campaigns/{campaign_id}
```
- **RBAC**: Requires `require_admin_scope("content_editor")`.
- **Constraint**: `PATCH` strictly forbids mutating `eid_date_overridden` directly (only reachable via B-08).
- **Audit**: All admin mutations write immutable rows via E.28's `AuditLogService`.
