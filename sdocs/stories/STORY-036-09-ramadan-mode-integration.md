---
id: STORY-036-09
epic: EPIC-036
kind: integration
title: Ramadan Mode End-to-End Contract & Seam Integration
status: ready
priority: P0
prd: ../../PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md
depends_on: [STORY-036-06, STORY-036-07, STORY-036-08]
produces: []
consumes: [api.ramadan-campaign-status, domain.hijri-calendar-service, api.ramadan-missions, api.ramadan-fasting-logs, api.ramadan-journey-progress, api.ramadan-family-aggregate, api.ramadan-certificates, api.admin-ramadan-eid-override]
created: 2026-09-30
---

## User Story
As the engineering team and QA, we want an automated end-to-end integration test suite that exercises all seams and contracts of Ramadan Mode (EPIC-036), so that cross-feature workflows (lifecycle resolution, mission delivery, fasting bounds, reward replay safety, family rollups, certificate generation, and moon-sighting overrides) work seamlessly together without regressions.

## Acceptance Criteria
- [ ] AC1: Given a simulated Ramadan season from Day 1 to Day 30, when a child progresses through each day, then `GET /v1/ramadan/campaign-status` accurately tracks current night, `GET /v1/ramadan/missions/{night}` delivers the correct content with `gamification_suppressed: true` on exactly nights 21, 23, 25, 27, 29, and `POST /v1/ramadan/missions/{night}/complete` records progress and dispatches points/badges to `reward_ledger`.
- [ ] AC2: Given an attempt to submit `fasted_full` for an `education_only` child during the journey, then the fasting log API rejects the attempt with HTTP 403 while allowing `education_only` logging.
- [ ] AC3: Given replayed network requests for mission completion on night 15, then the API responds with HTTP 200 `already_completed: true` and verifies zero duplicate records in `reward_ledger`.
- [ ] AC4: Given a parent querying `GET /v1/ramadan/family-aggregate` after multiple children participate, then the response provides accurate family-level totals with zero per-child arrays.
- [ ] AC5: Given the end of the season, when a parent passes the Parent Gate and invokes `POST /v1/ramadan/certificates`, then a valid PII-free certificate URL is produced and persisted in `ramadan_certificates`.
- [ ] AC6: Given a mid-season moon-sighting dispute, when a super admin executes `POST /v1/admin/ramadan/eid-date-override`, then the campaign status immediately reflects the updated Eid date, a push notification job is dispatched, and subsequent client status checks reflect the correction.
- [ ] AC7: Given a parent who changes account region mid-Ramadan, then future phases recalculate against the new region while historical journey progress rows remain completely intact.

## Technical Notes
- Files in scope:
  - `NoorHeroes-Backend/tests/integration/test_ramadan_mode_e2e.py`
  - `NoorHeroes-Backend/tests/integration/test_ramadan_contracts_conformance.py`
- Architecture refs: `sdocs/architecture-ref.md` Section 8; All Blueprints B-01 to B-08.
- Non-functional: Exercises all 8 seams across `ramadan` bounded context; CI-blocking test suite.

## Test Approach
- Unit: N/A (integration story).
- Integration: Full lifecycle simulation with simulated parent and child sessions using FastAPI TestClient and SQLite/PostgreSQL test fixtures.
- E2E: Complete journey simulation from Pre-Ramadan Countdown → Active Journey → Laylatul Qadr suppression → Eid Date Override → Certificate generation.

## Out of Scope
- Production code modifications (integration stories author test fixtures and assertions only).
