---
id: STORY-036-05
epic: EPIC-036
kind: feature
title: Ramadan Journey Progress & Idempotent Reward Engine Integration
status: ready
priority: P0
prd: ../../PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md
depends_on: [STORY-036-03]
produces: [api.ramadan-journey-progress]
consumes: [type.ramadan-models, api.ramadan-missions]
created: 2026-09-30
---

## User Story
As an authenticated child learner, I want to mark tonight's Ramadan mission complete and light a lantern on my Journey Map, so that I earn seasonal achievements and badges through the platform's trusted reward engine with zero risk of duplicate points on network retries.

## Acceptance Criteria
- [ ] AC1: Given an authenticated child session, when calling `POST /v1/ramadan/missions/{night}/complete` for an uncompleted night, then a progress row is inserted into `ramadan_journey_progress`, the lantern is marked lit, and reward issuance is dispatched to A.11's `RewardService` with `season_id` context.
- [ ] AC2: Given a mission completion grant, when verified in the database, then the points and badge grant flow through the shared `reward_ledger` table with zero parallel reward tables (Backend AI Prompt item 4 mandatory test).
- [ ] AC3: Given a completed mission, when `POST /v1/ramadan/missions/{night}/complete` is called again with the same night/session, then the API responds with HTTP 200, `already_completed: true`, and returns the original reward summary without dispatching a second reward grant (idempotent replay test).
- [ ] AC4: Given a child completing a past missed night retroactively (e.g. night 3 completed while on night 15), then the completion is recorded successfully and rewarded without date-based lockouts.
- [ ] AC5: Given a database conflict or concurrent duplicate request, then `UNIQUE(child_id, mission_id)` in `ramadan_journey_progress` prevents duplicate rows at the database level.
- [ ] AC6: Given a downstream temporary failure in A.11's reward engine after the progress row is inserted, then the service records an alertable partial-failure for retry and preserves the child's completion record without rollback.

## Technical Notes
- Files in scope:
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/models/journey_progress.py`
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/schemas/journey_progress_schema.py`
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/repositories/journey_progress_repository.py`
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/services/journey_progress_service.py`
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/routers/mission_router.py` (add `/complete` route)
  - `NoorHeroes-Backend/alembic/versions/xxxx_create_ramadan_journey_progress_table.py`
- Architecture refs: `sdocs/architecture-ref.md` Section 8.2 (Invariant 5), 8.3, 8.4; Blueprint B-05.
- Non-functional: `UNIQUE(child_id, mission_id)` structural constraint. Replay-safe HTTP 200 response. Shared `reward_ledger` integration.

## Test Approach
- Unit: Test idempotent repository insert logic under composite primary key conflict.
- Integration: Mandatory test verifying replayed completion generates no duplicate reward; mandatory test verifying reward lands in `reward_ledger`; test retroactive completion of missed nights.
- E2E: Complete night mission 1, verify lantern lit on journey map, verify badge awarded in child profile.

## Out of Scope
- Badge definition and artwork management (owned by A.11).
- Offline queuing and outbox synchronization (handled by Mobile K-03 and B.15 sync engine).
