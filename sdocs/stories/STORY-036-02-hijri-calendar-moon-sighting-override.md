---
id: STORY-036-02
epic: EPIC-036
kind: feature
title: Hijri Calendar Authority Service & Regional Moon-Sighting Override
status: ready
priority: P1
prd: ../../PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md
depends_on: [STORY-036-01]
produces: [domain.hijri-calendar-service]
consumes: [type.ramadan-models]
created: 2026-09-30
---

## User Story
As the NoorHeroes platform backend, I want an authoritative internal Hijri calendar service with a regional moon-sighting override mechanism, so that Islamic dates are computed with high fidelity across all regions and disputed moon-sightings can be corrected without client-side date math.

## Acceptance Criteria
- [ ] AC1: Given a recognized region code, when `HijriCalendarService.get_dates(region)` is called and no override exists, then it returns algorithmically computed `hijri_start_date` and `eid_date` with `is_overridden: false`.
- [ ] AC2: Given a region with an active override in `moon_sighting_overrides`, when `HijriCalendarService.get_dates(region)` is called, then it returns the corrected dates with `is_overridden: true` and the associated `source_note`.
- [ ] AC3: Given an admin calling `apply_override()` with a corrected date within ±3 days of the algorithmic target, then the method creates an append-only row in `moon_sighting_overrides`, updates `ramadan_campaigns.eid_date`, sets `eid_date_overridden: true`, and returns the override confirmation.
- [ ] AC4: Given an override date deviating > 3 days from the algorithmic calculation (e.g. +5 days), when `apply_override()` is called, then the service rejects the input with `SanityBoundExceededException`.
- [ ] AC5: Given an unrecognized or unsupported region string, when `get_dates()` is called, then it raises `UnsupportedRegionException` without raising a 500 server crash.
- [ ] AC6: Given an updated override, when `CampaignLifecycleService` (B-01) subsequently queries campaign status, then the corrected date is immediately reflected in the response.

## Technical Notes
- Files in scope:
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/models/moon_sighting_override.py`
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/repositories/moon_sighting_override_repository.py`
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/services/hijri_calendar_service.py`
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/schemas/hijri_dates_schema.py`
  - `NoorHeroes-Backend/alembic/versions/xxxx_create_moon_sighting_override_table.py`
- Architecture refs: `sdocs/architecture-ref.md` Section 8.2 (Invariant 2), 8.3, 8.4; Blueprint B-02.
- Non-functional: Sole Hijri authority across the platform; leaf service with zero public routers; memory/Redis caching with override-invalidation.

## Test Approach
- Unit: Test algorithmic date computation across divergent regions (e.g. Middle East vs. North America); test ±3 days sanity bounds rejection.
- Integration: Test `apply_override()` appending to `moon_sighting_overrides` and immediately updating `ramadan_campaigns`; verify read-through from `get_dates()`.
- E2E: Verify that an override written via `HijriCalendarService` propagates to `GET /v1/ramadan/campaign-status`.

## Out of Scope
- Public HTTP router exposure (service is strictly internal).
- Super-admin authorization and push notification dispatch (owned by STORY-036-08).
