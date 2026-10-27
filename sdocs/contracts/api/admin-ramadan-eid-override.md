---
id: api.admin-ramadan-eid-override
kind: api
title: Admin Eid Date Override & Notification API (POST /v1/admin/ramadan/eid-date-override)
status: draft
owner_story: STORY-036-08
version: 1
created: 2026-09-30
---

## Endpoint

```http
POST /v1/admin/ramadan/eid-date-override
```

## Description
Applies an authoritative moon-sighting date correction for a specific region's Eid date. Updates the campaign record via `HijriCalendarService.applyOverride()`, records an immutable audit trail, and triggers a regional one-time push notification via B.17's `NotificationDispatchService`.

## Auth & Security
- **Auth**: Bearer admin session token via `Depends(get_current_admin)`.
- **RBAC**: Strictly restricted to `super_admin` (`Depends(require_admin_scope("super_admin"))`).
  - Standard admin scopes (e.g. `content_editor`, `support_lead`) are rejected with `403 FORBIDDEN`.
- **Audit Logging**: Emits an immutable audit record via E.28's `AuditLogService.log_action()` with the acting admin ID, IP, region, and previous vs. new date.

## Request Body

```ts
export interface EidDateOverrideRequest {
  region: string;             // Valid region code, e.g. "US_EAST", "SA_RIYADH", "UK_LONDON"
  corrected_eid_date: string; // ISO 8601 Date (YYYY-MM-DD), e.g. "2027-03-10"
  source_note: string;        // Justification/authority (e.g. "Official High Judiciary Council announcement")
}
```

## Response — 200 OK

```ts
export interface EidDateOverrideResponse {
  override_id: string;
  region: string;
  previous_eid_date: string;
  corrected_eid_date: string;
  eid_date_overridden: true;
  notification_dispatched: boolean; // true if B.17 broadcast succeeded
  notification_job_id?: string;
  applied_at: string; // ISO 8601 UTC timestamp
  acting_admin_id: string;
}
```

## Errors
- `400 BAD_REQUEST`:
  - `corrected_eid_date` fails sanity-bound check (|delta| > 3 days from algorithmic date).
  - Malformed date or missing required fields.
- `401 UNAUTHORIZED`: Missing or invalid admin Bearer token.
- `403 FORBIDDEN`: Admin lacking `super_admin` scope (`"This action requires super_admin privileges."`).
- `404 NOT_FOUND`: No active Ramadan campaign exists for the specified region.

## Invariants
1. Subsequent calls to `GET /v1/ramadan/campaign-status` for the affected region immediately reflect the corrected `eid_date`.
2. Notification dispatch failure is logged as an alertable partial-failure but does **not** roll back the database date update.
3. Every invocation generates an append-only row in `moon_sighting_overrides` and an E.28 audit log record.
