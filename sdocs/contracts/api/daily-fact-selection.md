---
id: api.daily-fact-selection
kind: api
title: Child Fact-of-the-Day Selection API (GET /v1/facts/daily)
status: stable
owner_story: TASK-B18-02
version: 1
created: 2026-10-11
---

## Endpoint

```http
GET /v1/facts/daily
GET /v1/content/facts/daily
```

## Auth & Security

- **Auth**: Bearer token via authenticated child session (`ChildSessionContext` / `get_current_child`).
- **Server-Side Age-Band Derivation**: Child age band is derived exclusively from server session profile; any client-supplied `age_band` query parameter is structurally ignored.
- **Sibling Tenancy Isolation**: If `child_id` query parameter is provided, it must match session token child ID (`403 FORBIDDEN` on mismatch).
- **Graceful Degradation Guarantee**: Always returns 200 with a valid scholar-approved fact (via dedup progressive relaxation or evergreen fallback); never returns "no fact".

---

## 1. Request Parameters

### Query Parameters

- `child_id` (string, optional): Sibling boundary check; if provided, must strictly match session token.
- `surface` (string, optional): Surface invocation context: `"home_card"` (default) or `"resurfacing_prompt"`.
- `timezone` (string, optional): Client timezone string (e.g. `UTC`, `Asia/Riyadh`).
- `age_band` (string, optional): Client-supplied parameter (parsed but structurally ignored).

### Headers

- `X-Locale` / `Accept-Language` (string, optional): Target language override (`en`, `ar`, `ur`, `hi`). Defaults to `en`.

---

## 2. Response Contract — 200 OK

```ts
export interface DailyFactResponse {
  factId: string;                 // Canonical UUIDv7 identifier of fact entity
  text: string;                   // Age-appropriate, localized statement of the fact
  topic: string;                  // Registered thematic topic (e.g., quran, sunnah, civilization)
  scholarApproved: boolean;       // Hard structural guarantee (always true)
  approvalVersion: string;        // Version identifier of active approved version (e.g., "v1", "legacy")
  explanation?: string | null;    // Contextual explanation for the fact statement
  occasion?: string | null;       // Active Islamic calendar greeting occasion (e.g., "Jummah Mubarak", "Ramadan Kareem")
  sourceCitation?: string | null; // Primary source reference string
  category?: string | null;       // Backward-compatible category string matching topic
  isEvergreen?: boolean;          // True if delivered via evergreen fallback candidate pool
}
```

*Note: Dual-wire serialization supports both camelCase (`factId`, `scholarApproved`, `approvalVersion`) and snake_case.*

---

## 3. Error Responses

- `401 UNAUTHORIZED`: Missing, invalid, or expired child session token.
- `403 FORBIDDEN`: Sibling tenancy mismatch (`child_id` param != session child).
- `405 METHOD_NOT_ALLOWED`: Calling POST, PUT, DELETE, PATCH on `/v1/facts/daily`.
