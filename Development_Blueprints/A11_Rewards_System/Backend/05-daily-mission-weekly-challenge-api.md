# B-05 — Daily Mission & Weekly Challenge API (User)

## 1. Feature Context
Part of Feature A.11 — Rewards System. Manages time-boxed Daily Missions (3/day) and Weekly/Seasonal Challenges, including the archive-not-disappear lifecycle.

## 2. Parent Feature
A.11 Rewards System — Backend (FastAPI)

## 3. Sub-feature
B-05 Daily Mission & Weekly Challenge API (User)

## 4. Objective
Implement `GET /v1/missions` and `POST /v1/missions/{id}/progress`, backing FR-10 and Edge Cases 4, 10.

## 5. Business Requirements
- Daily missions (3/day) and the active weekly challenge/seasonal event are returned in one call.
- Progress resets at window close; expired challenges archive rather than disappear (FR-10).
- Each challenge instance has its own distinct identity/ledger-reason-id; a claim against a genuinely new instance is legitimate, only a literal repeat claim on the same instance is blocked (Edge Case 10).
- Reward eligibility for challenge completion is unaffected by subscription tier (Edge Case 4).

## 6. Existing Architecture
Extends the `rewards` bounded context. Reward issuance on completion routes through B-01's `RewardService.award_points()` in-process — no parallel reward path inside this sub-feature.

## 7. Existing Code to Reuse
- B-01 `RewardService.award_points()`.
- `get_current_child` dependency.

## 8. Files to Create
- `src/noorheroes/modules/rewards/models.py` — extend with `Mission`, `MissionProgress`.
- `src/noorheroes/modules/rewards/schemas.py` — extend with `MissionsResponse`, `MissionProgressRequest`.
- `alembic/versions/<rev>_create_mission_tables.py`
- `tests/modules/rewards/test_missions_endpoint.py`
- `tests/modules/rewards/test_challenge_archive_lifecycle.py`
- `tests/modules/rewards/test_challenge_instance_reclaim.py`

## 9. Files to Modify
- `src/noorheroes/modules/rewards/service.py` — add `get_missions_for_child()`, `record_mission_progress()`.
- `src/noorheroes/modules/rewards/api.py` — add both routes.

## 10. Backend Requirements
- `missions.type IN ('daily','weekly','seasonal')` (CHECK constraint).
- `UNIQUE(child_id, mission_id)` on `mission_progress`.
- Archive state is computed from `ends_at` having passed, not a separate delete/archive flag — never physically remove expired missions.
- `POST /v1/missions/{id}/progress` is usually internal/event-consumer-driven (triggered by other features' completion events reporting progress toward a mission's `criteria_json`), idempotent via standard key pattern.
- Claim action on a completed mission/challenge triggers `RewardService.award_points()` with `reason_id` = the specific mission-instance ID.

## 11. KMP Requirements
Consumed by K-06 (Daily Mission & Weekly Challenge Experience).

## 12. NextJS Requirements
Missions authored/scheduled via B-11 (Admin Mission & Weekly Challenge Scheduler API).

## 13. API Contract

**Required API**
- **HTTP Method:** GET
- **Endpoint:** `/v1/missions?child_id=`
- **Response 200:** `{ "daily_missions": [...3 items...], "weekly_challenge": {"id":"...","progress":0.4,"expires_at":"..."}, "seasonal_event": {...} }`
- **Authentication:** Bearer, child-mode; scoped to own `child_id`.

**Required API — Progress**
- **HTTP Method:** POST
- **Endpoint:** `/v1/missions/{id}/progress`
- **Idempotency:** standard idempotency-key pattern.
- **Error Responses:** `404` unknown mission; `409` not applicable (idempotent replay returns original result, not an error).

## 14. Database Requirements
- `missions`: `id UUID PK`, `type VARCHAR CHECK`, `eligibility_json JSONB`, `criteria_json JSONB`, `reward_json JSONB`, `starts_at`, `ends_at TIMESTAMPTZ`. Index `(type, starts_at, ends_at)`.
- `mission_progress`: `child_id UUID FK`, `mission_id UUID FK`, `progress_json JSONB`, `completed_at`, `claimed_at TIMESTAMPTZ NULL`. `UNIQUE(child_id, mission_id)`. Index `(child_id)`.
- Retained for historical/archive display indefinitely (FR-10) — no purge job for expired `mission_progress`.

## 15. Validation
- Test: expired mission remains queryable in an archived state (`ends_at` in the past), never returns 404/deleted.
- Test: second claim against a new challenge instance (distinct `mission_id`) succeeds; repeat claim against the same instance is rejected/idempotently resolved.

## 16. Authentication
Bearer JWT, child-mode.

## 17. Authorization
Scoped to own `child_id`.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Query for missions after a challenge window closed | Returns the challenge in an archived state, not omitted |
| Progress-report for an already-completed mission | Idempotent no-op, returns current state |
| Claim on an already-claimed instance | Idempotent, returns original claim result |
| Claim on a genuinely new instance sharing the same mission "series" | Treated as legitimate, not a duplicate (Edge Case 10) |

## 19. Offline First
Progress-reporting calls are safely retriable by the client's offline outbox (K-06) without side effects beyond the first successful call.

## 20. Local Data
N/A (backend); client-side caching detailed in K-06.

## 21. Localization
Mission/challenge titles/descriptions resolved via `locale_key`/backend-provided translation keys, not hardcoded English.

## 22. RTL
N/A (backend).

## 23. Analytics
Emit `weekly_challenge_viewed/joined/completed/claimed/archived_viewed`, `daily_mission_viewed/completed`, `seasonal_event_banner_viewed/entered` per PRD §1.19 (client-fired, tied to these endpoints' responses).

## 24. Performance
Single query returning all three mission categories in one round trip; indexed by `(type, starts_at, ends_at)` for efficient active-window lookups.

## 25. Security
Reward issuance for missions/challenges routes exclusively through B-01, preventing a parallel reward-granting surface specific to this sub-feature.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, PostgreSQL (JSONB, CHECK constraints), Pydantic v2.

## 27. Testing
- Unit: window-boundary reset logic (daily reset, weekly-instance transition).
- Integration: mission completion → progress update → claim → ledger entry → wallet update chain.
- Archive-lifecycle and instance-reclaim tests per §15.

## 28. Documentation
OpenAPI docs noting the archive-not-disappear behavior explicitly, so API consumers don't mistake an expired challenge for a 404.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create Mission/MissionProgress Models & Migration**
- Files to Create: models + migration per §8/§14.
- Definition of Done: tables created with correct constraints.

**Task 02 — Implement `get_missions_for_child()`**
- Files to Modify: `service.py`
- Implementation Details: single query assembling daily/weekly/seasonal categories.
- Tests: unit test for correct category assembly.
- Definition of Done: correct response shape per §13.

**Task 03 — Implement `record_mission_progress()` with Reward Delegation**
- Files to Modify: `service.py`
- Existing Files to Reuse: `RewardService.award_points()`.
- Business Rules: FR-10, Edge Case 10.
- Implementation Details: on claim, call `award_points()` with `reason_id` = mission-instance ID.
- Definition of Done: correct reward issuance verified via mocked `RewardService`.

**Task 04 — Implement Endpoints**
- Files to Modify: `api.py`
- Authentication/Authorization: per §16/§17.
- Tests: integration tests.
- Definition of Done: both endpoints live.

**Task 05 — Implement Archive & Instance-Reclaim Tests (Mandatory)**
- Files to Create: `test_challenge_archive_lifecycle.py`, `test_challenge_instance_reclaim.py`
- Definition of Done: both tests passing.

**Task 06 — Add API Documentation**
- Documentation: OpenAPI notes on archive behavior.
- Definition of Done: docs reviewed.

**Task 07 — Final Code Review**
- Do Not Change: `RewardService` internals; PostgreSQL/Redis credentials.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Missions/challenges endpoint live; archive-not-disappear and instance-reclaim behaviors correctly implemented and tested; reward issuance delegated to B-01.

## 31. Final Verification Checklist
- [x] `GET /v1/missions` returns correct daily/weekly/seasonal shape
- [x] Expired challenges shown archived, never deleted/omitted
- [x] New-instance claim vs repeat-claim-on-same-instance correctly distinguished
- [x] Reward issuance delegated to `RewardService`, not reimplemented
- [x] Subscription-tier downgrade does not affect challenge reward eligibility
- [x] OpenAPI documentation complete
