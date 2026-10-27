---
id: STORY-036-08
epic: EPIC-036
kind: feature
title: Super-Admin Moon-Sighting Eid Date Override & Regional Notification API
status: ready
priority: P0
prd: ../../PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md
depends_on: [STORY-036-01, STORY-036-02]
produces: [api.admin-ramadan-eid-override]
consumes: [type.ramadan-models, domain.hijri-calendar-service, api.ramadan-campaign-status]
created: 2026-09-30
---

## User Story
As an authorized super admin, I want to apply an authoritative moon-sighting Eid date correction for an affected region and trigger an immediate broadcast push notification, so that families' apps automatically re-sync to the confirmed Eid date upon next open.

## Acceptance Criteria
- [ ] AC1: Given an admin session with `super_admin` scope, when calling `POST /v1/admin/ramadan/eid-date-override` with a valid region and corrected date, then the service invokes `HijriCalendarService.applyOverride()`, updates `ramadan_campaigns.eid_date`, sets `eid_date_overridden = true`, and returns HTTP 200.
- [ ] AC2: Given an admin with only `content_editor` or other lower privileges, when attempting to call this endpoint, then the request is rejected with HTTP 403 Forbidden (`"This action requires super_admin privileges"`).
- [ ] AC3: Given a successful Eid date override, when a subsequent call to `GET /v1/ramadan/campaign-status` is made for that region, then the response immediately reflects the corrected `eid_date` and `eid_date_overridden: true` (Backend AI Prompt item 6 mandatory test).
- [ ] AC4: Given a successful date update, then the service triggers a one-time push broadcast targeting all active families in the region via B.17's `NotificationDispatchService`.
- [ ] AC5: Given a scenario where notification dispatch encounters a transient downstream failure, then the service logs an alertable partial-failure warning and preserves the database date correction without rolling it back.
- [ ] AC6: Given any override execution, then an immutable audit log entry is recorded in E.28's `AuditLogService` recording acting admin ID, region, previous date, corrected date, and source note.
- [ ] AC7: Given an input date deviating > 3 days from the algorithmic calculation, then the request is rejected with HTTP 400 Bad Request.

## Technical Notes
- Files in scope:
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/schemas/eid_override_schema.py`
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/services/eid_override_service.py`
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/routers/admin_eid_override_router.py`
- Architecture refs: `sdocs/architecture-ref.md` Section 8.2 (Invariant 8), 8.3, 8.4; Blueprint B-08.
- Non-functional: Strictly gated to `super_admin`. Dispatches regional push via B.17. Emits E.28 audit log.

## Test Approach
- Unit: Test role verification rejecting non-super-admin tokens; test sanity-bound validation on override date.
- Integration: Mandatory test verifying subsequent `campaign-status` call reflects corrected date; mandatory test verifying `content_editor` is rejected and only `super_admin` succeeds; test notification dispatch and partial-failure logging.
- E2E: Admin submits moon-sighting override for `US_EAST`, checks campaign status reflects new Eid date, and checks notification dispatch was enqueued.

## Out of Scope
- Routine campaign CRUD operations (handled by STORY-036-01 admin router).
- Mobile push notification client receipt rendering (owned by Mobile B.17 integration).
