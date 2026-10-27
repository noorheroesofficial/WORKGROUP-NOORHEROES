# B-05 — Ramadan Journey Progress & Reward Engine Integration

## 1. Feature Context
Records night-mission completion and routes every completion through A.11's existing, hardened reward-issuance path — the platform's second-highest-priority guarantee after B-01's region resolution, since a reward-duplication bug here would directly damage trust in the badge/reward economy platform-wide.

## 2. Parent Feature
F.36 — Ramadan Mode

## 3. Sub-feature
1.5 Ramadan Journey Progress & Reward Engine Integration (ID: **B-05**)

## 4. Objective
Implement idempotent night-completion recording in `ramadan_journey_progress`, routed through A.11's existing reward-issuance endpoint with `badges.season_id` scoping — no parallel reward logic.

## 5. Business Requirements
- FR-8: Ramadan-specific achievements plug into the existing achievement/badge system; `badges.season_id` scopes seasonal badges — no parallel reward mechanism.
- §5 Backend AI prompt item 4 (highest-priority guarantee #2): idempotent completion (`UNIQUE(child_id, mission_id)`), routed through A.11's EXISTING reward-issuance endpoint; no duplicate reward on replay; grant flows through the shared `reward_ledger` table.
- Edge Case 5: missed nights remain completable retroactively, never locked out.

## 6. Existing Architecture
`ramadan` bounded context, `app/ramadan/services/journey_progress_service.py`, calling A.11's `app/rewards/services/reward_service.py::RewardService` (exact method name to confirm against `rewards` context, §5.9 of `FAST-API-INSTRUCTIONS.md` — do not invent a method signature).

## 7. Existing Code to Reuse
- A.11's `RewardService` reward-issuance entry point (exact class/method per `rewards` context — confirm before implementation)
- A.11's `reward_ledger` table and `badges.season_id` column
- `app/shared/base_service.py::BaseService`

## 8. Files to Create
- `app/ramadan/services/journey_progress_service.py`
- `app/ramadan/repositories/journey_progress_repository.py`
- `app/ramadan/models/journey_progress.py`
- `app/ramadan/schemas/journey_progress_schema.py`
- `alembic/versions/xxxx_create_ramadan_journey_progress_table.py`

## 9. Files to Modify
- `app/ramadan/routers/mission_router.py` (B-03) — add the `POST /v1/ramadan/missions/{night}/complete` route per §11's proposed contract

## 10. Backend Requirements
- `JourneyProgressService.complete_mission(child_id, mission_id)`: inserts into `ramadan_journey_progress` with `UNIQUE(child_id, mission_id)`; on successful insert (not on a duplicate-key no-op), calls A.11's existing reward-issuance entry point with `season_id` context so the grant lands in the shared `reward_ledger` and any resulting badge is `season_id`-scoped.
- Idempotent replay: a repeated call for the same `(child_id, mission_id)` must be a safe no-op — no second reward call, no error surfaced to the client beyond a normal success response (replay-safety, not replay-rejection).
- Retroactive completion: a missed night's mission remains completable at any later point in (or after) the season — no date-based lockout in this service's logic.
- Transactional consistency: the progress-row insert and the reward-issuance call should be coordinated so a reward-issuance failure doesn't silently leave `ramadan_journey_progress` marking completion without a corresponding reward attempt (log as an alertable partial-failure condition if the two cannot be strictly transactional across service boundaries, mirroring B-08's partial-failure pattern).

## 11. Required API / API Contract
### Proposed Completion Endpoint (pending confirmation)
PRD §3.4 does not enumerate a distinct completion endpoint separately from `GET /v1/ramadan/missions/{night}` (B-03). Following the platform's existing REST conventions (resource-scoped action verb, mirrors B-08's action-endpoint shape), this blueprint proposes:

`POST /v1/ramadan/missions/{night}/complete` → `200 { "mission_id", "child_id", "completed_at", "already_completed": boolean, "reward": { ... A.11's existing reward-grant response shape ... } }`
- **Request body:** none required — `night` (path) plus the authenticated child session fully identify the completion target; no client-supplied `child_id` in the body (mirrors B-01's server-side-identity discipline, preventing a child session from completing on another child's behalf).
- **Auth:** `get_current_child`. **Authz:** child completes only for themselves.
- **Idempotency:** a second call for an already-completed `(child_id, mission_id)` returns `200` with `already_completed: true` and the original `reward` payload (not a fresh grant) — never a `409`/error, since safe replay is the entire point of this contract (§10).
- **Error Responses:** `404` if `night` has no configured mission for the child's active campaign.

**Mark PROPOSED in code review until a real contract is signed off** — this service layer (`JourneyProgressService`) is written to be contract-agnostic internally, so re-pointing the router to a confirmed alternate shape later is a router-layer change only, not a service-layer rewrite. **User API.**

## 12. Database Requirements
`ramadan_journey_progress(child_id FK, mission_id FK, completed_at)`; `UNIQUE(child_id, mission_id)`; index `(child_id)`. Append-only, no soft-delete (FR-11/§4.4).

## 13. Validation
`mission_id` must reference a valid, currently-existing `ramadan_missions` row; `child_id` must belong to the requesting session's family.

## 14. Authentication
`get_current_child`.

## 15. Authorization
Child may only complete missions for themselves.

## 16. Error Handling
Reward-issuance failure after a successful progress insert: logged as an alertable partial-failure, retried per A.11's own retry policy (reused, not reinvented) — the progress record itself is never rolled back for a downstream reward hiccup, since the child's completion is factually true regardless.

## 17. Offline First
Completion actions queue via B.15's existing outbox when offline; this endpoint's idempotency (§10) is precisely what makes safe replay-on-reconnect possible.

## 18. Local Data
N/A server-side.

## 19. Localization
N/A.

## 20. RTL
N/A.

## 21. Analytics
`ramadan_night_mission_completed`, `ramadan_lantern_lit` per §1.19, emitted on the first (non-replayed) successful completion only.

## 22. Performance
Single indexed insert plus one downstream reward-service call; reward-service call should be async/non-blocking relative to the client-facing response where A.11's existing pattern supports it.

## 23. Security
Idempotency via `UNIQUE(child_id, mission_id)` is the structural guarantee against reward duplication — not an application-level "check-then-insert" pattern, which would be race-prone under concurrent requests.

## 26. Library Requirements
FastAPI, Pydantic v2, SQLAlchemy 2.0 async. No new libraries.

## 27. Testing
Unit: idempotent-insert behavior under the `UNIQUE` constraint. Integration: **mandatory** — replayed completion produces no duplicate reward (Backend AI prompt item 4); **mandatory** — the actual grant is confirmed flowing through the shared `reward_ledger` table, not a Ramadan-local table; retroactive/missed-night completion succeeds regardless of current date.

## 28. Documentation
OpenAPI/internal docstring documenting the idempotency contract and the exact A.11 call path used.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Write Migration for `ramadan_journey_progress`**
Objective: Idempotency-enforcing table. Files to Create: `alembic/versions/xxxx_create_ramadan_journey_progress_table.py`, `models/journey_progress.py`. Dependencies: B-03's `ramadan_missions` (FK target). Tests: migration + constraint test. Definition of Done: `UNIQUE(child_id, mission_id)` enforced at the DB level.

**Task 02 — Implement `JourneyProgressRepository`**
Objective: Idempotent insert (insert-or-no-op on conflict). Files to Create: `repositories/journey_progress_repository.py`. Dependencies: Task 01. Tests: conflict-handling repository test. Definition of Done: tests pass.

**Task 03 — Confirm A.11's Reward-Issuance Entry Point**
Objective: Identify the exact existing method/endpoint (do not invent). Files to Read: A.11's `rewards` context service files. Definition of Done: exact call signature documented in this file's §7 before Task 04 proceeds.

**Task 04 — Implement `JourneyProgressService.complete_mission()`**
Objective: Insert-then-reward-call, idempotent on replay. Existing Files to Reuse: A.11's `RewardService` (per Task 03). Files to Create: `services/journey_progress_service.py`. Dependencies: Task 02, Task 03. Tests: **mandatory** — no-duplicate-reward-on-replay test; **mandatory** — grant-lands-in-shared-reward_ledger test. Definition of Done: both tests pass.

**Task 05 — Wire the Completion Endpoint**
Objective: Expose `POST /v1/ramadan/missions/{night}/complete` per §11's proposed contract, including the `already_completed`-on-replay response shape. Files to Modify: `routers/mission_router.py`. Dependencies: Task 04. Tests: endpoint integration tests, including a replay call asserting `already_completed: true` with the original reward payload. Definition of Done: tests pass; contract flagged for sign-off per §30.

**Task 06 — Implement Retroactive-Completion Support**
Objective: No date-based lockout for missed nights. Dependencies: Task 04. Tests: retroactive-completion test. Definition of Done: test passes.

**Task 07 — Implement Partial-Failure Logging**
Objective: Reward-issuance failure logged/alerted without rolling back progress. Dependencies: Task 04. Tests: partial-failure test. Definition of Done: test passes.

**Task 08 — Add Full Test Suite**
Objective: Complete coverage per §27, both mandatory tests included. Definition of Done: all green in CI.

**Task 09 — Final Code Review**
Objective: Confirm zero parallel reward-ledger or badge-issuance code exists anywhere in this module. Definition of Done: checklist in §30 checked.

## 30. Final Verification Checklist
- [ ] `UNIQUE(child_id, mission_id)` enforced at the database level
- [ ] Replayed completion produces no duplicate reward — mandatory test passing
- [ ] Grant confirmed flowing through the shared `reward_ledger` table — mandatory test passing
- [ ] Retroactive/missed-night completion succeeds at any later point
- [ ] Reward-issuance partial failure logged/alerted without rolling back progress
- [ ] `POST /v1/ramadan/missions/{night}/complete` implemented per §11's proposed contract, with `already_completed`/idempotent-replay response shape
- [ ] Proposed completion-endpoint contract flagged for real sign-off before production release

## 31. Definition of Done
Every night's completion is recorded exactly once and rewarded exactly once, through the platform's single existing reward engine, with zero possibility of duplicate or parallel reward issuance.
