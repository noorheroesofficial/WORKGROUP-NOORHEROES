---
id: STORY-036-06
epic: EPIC-036
kind: feature
title: Family Ramadan Aggregate API with Anti-Sibling Comparison Structural Guarantee
status: ready
priority: P1
prd: ../../PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md
depends_on: [STORY-036-04, STORY-036-05]
produces: [api.ramadan-family-aggregate]
consumes: [type.ramadan-models, api.ramadan-journey-progress, api.ramadan-fasting-logs]
created: 2026-09-30
---

## User Story
As an authenticated parent, I want to view a collective, family-wide summary of our household's Ramadan progress without seeing a ranked sibling breakdown, so that our family celebrates togetherness and spiritual growth without harmful competition between children.

## Acceptance Criteria
- [ ] AC1: Given an authenticated parent session, when `GET /v1/ramadan/family-aggregate` is requested, then the response provides family-level metrics (`family_missions_completed`, `family_lanterns_lit`, `family_participation_rate`, `fasting_participation`) with zero per-child array fields (Backend AI Prompt item 5 mandatory structural test).
- [ ] AC2: Given a response schema reflection test on `FamilyRamadanAggregateResponse`, then the test verifies that no field or nested type contains a list of children, child IDs, or individual completion tallies.
- [ ] AC3: Given a multi-child family where children follow different fasting approaches (e.g. child A is `education_only`, child B is `fasted_practice`), when the aggregate is computed, then the response aggregates counts across categories without comparing or ranking the children.
- [ ] AC4: Given a new household joining mid-season (e.g. joining on night 14), when the aggregate is retrieved, then the response indicates `is_mid_season_join: true` and treats pre-join nights as not applicable rather than missed.
- [ ] AC5: Given a parent requesting the aggregate for a family other than their own, then the endpoint returns HTTP 403 Forbidden.
- [ ] AC6: Given high dashboard traffic, then the response is cached in Redis for 60 seconds and invalidated automatically upon new mission completions or fasting logs for that family.

## Technical Notes
- Files in scope:
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/schemas/family_aggregate_schema.py`
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/repositories/family_aggregate_repository.py`
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/services/family_aggregate_service.py`
  - `NoorHeroes-Backend/src/noorheroes/modules/ramadan/routers/family_aggregate_router.py`
- Architecture refs: `sdocs/architecture-ref.md` Section 8.2 (Invariant 6), 8.3, 8.4; Blueprint B-06.
- Non-functional: Anti-sibling comparison enforced at DTO and schema levels. Redis cache with 60s TTL.

## Test Approach
- Unit: Reflection test asserting `FamilyRamadanAggregateResponse` model has no `children` attribute or array of child entities.
- Integration: Test aggregate calculations for multi-child family with diverse fasting approaches; test mid-season join empty state handling; test caching and invalidation on mission completion.
- E2E: Parent logs into dashboard and views aggregate summary showing total family lanterns lit.

## Out of Scope
- Detailed per-child progress management (accessible only through individual child profile views in Parent Area).
- Printable family report export (owned by STORY-036-07).
