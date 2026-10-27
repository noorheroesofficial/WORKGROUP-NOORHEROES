---
id: STORY-036-01
epic: EPIC-036
kind: feature
title: Ramadan Campaign Lifecycle & Region-Keyed Activation Window Service
status: ready
priority: P0
prd: ../../PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md
depends_on: []
produces: [api.ramadan-campaign-status, type.ramadan-models]
consumes: []
created: 2026-09-30
---

## User Story
As an authenticated parent, I want to retrieve my household's current Ramadan campaign lifecycle phase and night number based strictly on my registered account region, so that my family's journey aligns with our geographic Islamic calendar with zero risk of client date manipulation.

## Acceptance Criteria
- [ ] AC1: Given an authenticated parent session with profile region `US_EAST`, when `GET /v1/ramadan/campaign-status` is called, then the response contains `phase`, `current_night`, `hijri_start_date`, and `eid_date` computed strictly from the `ramadan_campaigns` record for `US_EAST`.
- [ ] AC2: Given an incoming request with a client-supplied query parameter `?region=SA_RIYADH`, when the parent's actual profile region is `US_EAST`, then the service computes the phase from `US_EAST` and ignores the query parameter completely (structural absence from request schema verified).
- [ ] AC3: Given server time during the 14 days prior to `hijri_start_date`, when campaign status is checked, then `phase` is `pre_ramadan_countdown` and `current_night` is `null`.
- [ ] AC4: Given server time during night 12 of Ramadan, when campaign status is checked, then `phase` is `active` and `current_night` is `12`.
- [ ] AC5: Given server time during night 27 of Ramadan, when campaign status is checked, then `phase` is `laylatul_qadr` and `current_night` is `27`.
- [ ] AC6: Given a region with no active campaign configured in `ramadan_campaigns`, when campaign status is checked, then the endpoint returns HTTP 200 with `phase: "not_active"` and null dates (never 404 or 500).
- [ ] AC7: Given a parent who changes their Profile region mid-Ramadan, when campaign status is requested subsequently, then future phases compute against the new region while existing `ramadan_journey_progress` records remain completely intact.
- [ ] AC8: Given an admin with `content_editor` scope, when querying `GET /v1/admin/ramadan/campaigns`, then a paginated list of regional campaigns is returned.

## Technical Notes
- Files in scope:
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/models/campaign.py`
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/schemas/campaign_status_schema.py`
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/schemas/admin_campaign_schema.py`
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/repositories/campaign_repository.py`
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/services/campaign_lifecycle_service.py`
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/routers/campaign_router.py`
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/routers/admin_campaign_router.py`
  - `NoorHeroes-Backend/alembic/versions/xxxx_create_ramadan_campaigns_table.py`
- Architecture refs: `sdocs/architecture-ref.md` Section 8.1, 8.2 (Invariant 1), 8.4; Blueprint B-01.
- Non-functional: Indexed lookup on `region`; response cached per region with short TTL (60s). Zero client-supplied region parameter in request schema.

## Test Approach
- Unit: Test phase date arithmetic across all 6 phases (`pre_ramadan_countdown`, `active`, `laylatul_qadr`, `eid_transition`, `eid_celebration`, `post_eid_tail`, `not_active`).
- Integration: Test `GET /v1/ramadan/campaign-status` resolving strictly from authenticated Parent Profile; verify injecting `?region=OTHER` has zero effect; verify `not_active` returns HTTP 200; verify admin campaign CRUD and audit logging.
- E2E: Mid-Ramadan region change simulation verifying journey progress is preserved.

## Out of Scope
- Hijri lunar date calculation algorithms (owned by STORY-036-02).
- Admin Eid date override write path (owned by STORY-036-08).
