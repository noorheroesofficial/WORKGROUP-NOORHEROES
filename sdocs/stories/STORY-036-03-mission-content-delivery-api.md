---
id: STORY-036-03
epic: EPIC-036
kind: feature
title: Ramadan Mission Content Delivery API with Server-Computed Gamification Suppression
status: ready
priority: P0
prd: ../../PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md
depends_on: [STORY-036-01]
produces: [api.ramadan-missions]
consumes: [type.ramadan-models, api.ramadan-campaign-status]
created: 2026-09-30
---

## User Story
As an authenticated child or parent, I want to fetch the designated mission content for any of the 30 Ramadan nights, so that I receive scholar-approved stories, duas, and challenges with automatic spiritual calm and suppressed gamification during Laylatul Qadr nights.

## Acceptance Criteria
- [ ] AC1: Given night 12 of Ramadan, when `GET /v1/ramadan/missions/12` is requested, then the endpoint returns the night's content metadata sourced dynamically from E.29's `content_versions` with `gamification_suppressed: false`.
- [ ] AC2: Given any of the five Laylatul Qadr nights (21, 23, 25, 27, 29), when `GET /v1/ramadan/missions/{night}` is called, then the response has `gamification_suppressed: true` computed strictly from `ramadan_missions.is_laylatul_qadr` (Backend AI Prompt item 2 mandatory test).
- [ ] AC3: Given any non-Laylatul Qadr night (e.g. nights 1..20, 22, 24, 26, 28, 30), when mission content is requested, then `gamification_suppressed` is strictly `false`.
- [ ] AC4: Given a past missed night (e.g. night 5 when current night is 12), when `GET /v1/ramadan/missions/5` is called, then the content is returned with `is_unlocked: true`, enabling retroactive completion without lockout.
- [ ] AC5: Given a future night that has not unlocked yet according to the active campaign window, when `GET /v1/ramadan/missions/{night}` is called, then the endpoint returns HTTP 409 Conflict with state `not_yet_unlocked`.
- [ ] AC6: Given a night whose associated content version in E.29 is in draft state or lacking scholar approval, when queried by an end-user session, then the endpoint does not serve the draft content (HTTP 404 or 409).
- [ ] AC7: Given a night parameter outside `1..30` (e.g. 0 or 31), when requested, then the endpoint returns HTTP 400 Bad Request.

## Technical Notes
- Files in scope:
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/models/mission.py`
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/schemas/mission_schema.py`
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/repositories/mission_repository.py`
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/services/mission_service.py`
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/routers/mission_router.py`
  - `NoorHeroes-Backend/alembic/versions/xxxx_create_ramadan_missions_table.py`
- Architecture refs: `sdocs/architecture-ref.md` Section 8.2 (Invariant 3), 8.3, 8.4; Blueprint B-03.
- Non-functional: Zero parallel content storage (FK to `content_version_id` only); Redis caching per `(campaign_id, night_number)` with invalidation hooks on E.29 republish.

## Test Approach
- Unit: Mandatory test verifying `gamification_suppressed` is `true` for exactly nights 21, 23, 25, 27, 29 and `false` for all other 25 nights.
- Integration: Test E.29 `ContentService` delegation; test `not_yet_unlocked` future night vs. `is_unlocked: true` retroactive past night; test unapproved draft filtering.
- E2E: Verify child session fetching mission 27 and receiving reflection prompt with calm mode flags.

## Out of Scope
- Mission completion and reward issuance (owned by STORY-036-05).
- Content authoring and scholar review workflows (owned by E.29 CMS).
