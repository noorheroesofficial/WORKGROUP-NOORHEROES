# B-04 — Badge & Achievement Progress Engine
**Status: Implemented & Verified**

## 1. Feature Context
Part of Feature A.11 — Rewards System. Evaluates discrete badge unlocks and cumulative achievement-level progress after every ledger append, and enforces the platform-wide "badges are sticky once earned" guarantee.

## 2. Parent Feature
A.11 Rewards System — Backend (FastAPI)

## 3. Sub-feature
B-04 Badge & Achievement Progress Engine

## 4. Objective
Implement `badges`/`child_badges` (discrete) and `achievement_definitions`/`achievement_progress` (cumulative) evaluation, triggered after every B-01 ledger append, backing FR-2, FR-3 (stickiness generalization from A.6 Edge Case 2), Edge Cases 3 and 12.

## 5. Business Requirements
- Badges (discrete unlocks) and Achievements (cumulative levels) are structurally distinct (FR-2).
- Server-side-only criteria evaluation; no client-side badge-award logic anywhere.
- Once earned, a badge is never revoked, even if the underlying achievement counter is later corrected downward (Edge Case 3, generalizing A.6 Edge Case 2 platform-wide).
- Retroactive correction that newly qualifies a badge awards it with the actual original criteria-met timestamp where determinable.
- Seasonal badges (`season_id`) close for new qualification when the season ends but are retained permanently once earned (Edge Case 12).

## 6. Existing Architecture
Extends the `rewards` bounded context. Evaluation hook is invoked in-process immediately after B-01's `create_ledger_entry()` succeeds, within the same service-layer call, consistent with the Modular Monolith's in-process convention (B-01 §6).

## 7. Existing Code to Reuse
- B-01's `RewardService.award_points()` call site (hook point for evaluation).
- Notification Service (existing platform notification dispatch, per PRD §3.2 `NOTIFSVC`) for badge-unlock parent push.

## 8. Files to Create
- `src/noorheroes/modules/rewards/models.py` — extend with `Badge`, `ChildBadge`, `AchievementDefinition`, `AchievementProgress`.
- `src/noorheroes/modules/rewards/badge_engine.py` — `evaluate_badges(child_id, activity_type, context) -> list[BadgeUnlockResult]`.
- `alembic/versions/<rev>_create_badge_achievement_tables.py`
- `alembic/versions/<rev>_revoke_child_badges_write_grants.py`
- `tests/modules/rewards/test_badge_stickiness.py`
- `tests/modules/rewards/test_badge_retroactive_award.py`
- `tests/modules/rewards/test_seasonal_badge_retention.py`

## 9. Files to Modify
- `src/noorheroes/modules/rewards/service.py` — call `evaluate_badges()` after every successful ledger append.

## 10. Backend Requirements
- `UNIQUE(child_id, badge_id)` on `child_badges`.
- Migration revokes UPDATE and DELETE grants on `child_badges` for the application DB role — badges are write-once facts, structurally enforced.
- Criteria stored as structured `criteria_json`, evaluated server-side against the child's current achievement counters/ledger history.
- On threshold met: insert `child_badges` row, trigger parent push notification (via existing Notification Service), and include the unlock in the calling award's response payload for immediate client display.
- Malformed/legacy `criteria_json` is skipped and logged, never crashes the award pipeline.

## 11. KMP Requirements
Consumed by K-04 (Achievements Screen) via B-02's wallet `badges` field and a dedicated badge/achievement detail read (this task's own list endpoints, see §13).

## 12. NextJS Requirements
Definitions managed via B-10 (Admin Badge & Achievement Definition Management API).

## 13. API Contract

**Required API — Achievement/Badge Detail (User, read)**
- **HTTP Method:** GET
- **Endpoint:** `/v1/children/{id}/achievements`
- **Response 200:** `{ "badges": [...], "achievement_levels": [{"achievement_id":"...","level":3,"progress":0.6}] }`
- **Authentication:** Bearer, child-mode; scoped to own `{id}`.

Internal (not HTTP): `evaluate_badges(child_id, activity_type, context) -> list[BadgeUnlockResult]`, called from B-01's award path.

## 14. Database Requirements
- `badges`: `id UUID PK`, `code VARCHAR UNIQUE`, `criteria_json JSONB`, `locale_key VARCHAR`, `season_id UUID NULL`. Index `(season_id)`.
- `child_badges`: `child_id UUID FK`, `badge_id UUID FK`, `earned_at TIMESTAMPTZ`, `reason_id VARCHAR`. `UNIQUE(child_id, badge_id)`, append-only. Index `(child_id, earned_at DESC)`.
- `achievement_definitions`: `id UUID PK`, `criteria_json JSONB`, `badge_id UUID FK NULL`, `xp_value INT`.
- `achievement_progress`: `child_id UUID FK`, `achievement_id UUID FK`.

## 15. Validation
- Test: retroactive counter correction that newly qualifies a badge awards it with the original criteria-met timestamp where determinable.
- Test: a downward correction never revokes an already-earned badge.

## 16. Authentication
Bearer JWT, child-mode, for the read endpoint; internal evaluation function has no direct external auth surface.

## 17. Authorization
Read endpoint scoped to own `child_id`.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Malformed `criteria_json` | Skip evaluation for that badge, log, continue processing others |
| Badge already earned, criteria evaluated again | No-op (idempotent via `UNIQUE(child_id, badge_id)`) |
| Achievement counter corrected downward post-award | Badge/achievement level already granted is never revoked |

## 19. Offline First
N/A (backend); evaluation always server-side, synchronous with the award.

## 20. Local Data
N/A (backend).

## 21. Localization
Badge/achievement names resolved via `locale_key` client-side; no localized text stored/returned server-side beyond the key.

## 22. RTL
N/A.

## 23. Analytics
Emit `badge_unlocked`, `achievement_level_progressed` per PRD §1.19.

## 24. Performance
Evaluation runs synchronously within the award call path; keep criteria evaluation lightweight (indexed counter lookups, not full ledger scans per evaluation) to avoid inflating the B-01 p95 < 300ms budget.

## 25. Security
No client-side badge-award logic anywhere; server-side-only evaluation is the primary anti-gaming defense (PRD §12.1).

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, PostgreSQL (JSONB), Pydantic v2.

## 27. Testing
- Unit: criteria evaluation logic against fixture achievement histories.
- Integration: full award → badge threshold met → badge granted → notification triggered chain.
- Permission: `child_badges` UPDATE/DELETE rejected at DB layer.
- Stickiness/retroactive/seasonal-retention tests per §15.

## 28. Documentation
Document `criteria_json` schema/DSL for badge/achievement authors (Admin, B-10) with worked examples.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create Badge/Achievement Models & Migrations**
- Files to Create: models, two migrations per §8.
- Definition of Done: tables created; `child_badges` write grants revoked.

**Task 02 — Implement `evaluate_badges()`**
- Files to Create: `badge_engine.py`
- Business Rules: FR-2, Edge Case 3, Edge Case 12.
- Implementation Details: evaluate discrete badge criteria + cumulative achievement progress against the child's current counters.
- Error Handling: malformed criteria skipped/logged.
- Tests: criteria-evaluation unit tests.
- Definition of Done: correct unlock detection for fixture histories.

**Task 03 — Wire Evaluation Hook into Award Path**
- Files to Modify: `service.py`
- Implementation Details: call `evaluate_badges()` after successful `create_ledger_entry()`.
- Definition of Done: badges unlock correctly as part of the same award call.

**Task 04 — Implement Stickiness & Retroactive-Award Logic**
- Business Rules: Edge Case 3.
- Tests: `test_badge_stickiness.py`, `test_badge_retroactive_award.py` (mandatory).
- Do Not Change: never add an UPDATE/DELETE path to `child_badges` under any future requirement without explicit governance sign-off.
- Definition of Done: both tests passing.

**Task 05 — Implement Seasonal Badge Retention Logic**
- Business Rules: Edge Case 12.
- Tests: `test_seasonal_badge_retention.py`.
- Definition of Done: season-closed badges remain earnable-if-already-qualified, retained permanently once earned.

**Task 06 — Implement Achievement Read Endpoint**
- Files to Modify: `api.py`
- Authentication/Authorization: per §16/§17.
- Tests: integration test.
- Definition of Done: endpoint live.

**Task 07 — Wire Notification Trigger**
- Implementation Details: call existing Notification Service on badge unlock.
- Definition of Done: notification dispatch verified (mocked in tests).

**Task 08 — Documentation & Final Review**
- Documentation: `criteria_json` schema doc.
- Do Not Change: `child_badges` write-lockout.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Badge/achievement evaluation live, server-side-only, stickiness and seasonal-retention guarantees enforced and tested. Status: Verified Complete.

## 31. Final Verification Checklist
- [x] `UNIQUE(child_id, badge_id)` present
- [x] `child_badges` UPDATE/DELETE rejected at DB layer (Migration `0021_revoke_child_badges_write_grants.py`)
- [x] Stickiness test passing (downward correction never revokes — `test_badge_stickiness.py`)
- [x] Retroactive-award test passing (original timestamp preserved where determinable — `test_badge_retroactive_award.py`)
- [x] Seasonal-retention test passing (`test_seasonal_badge_retention.py`)
- [x] Badge unlock triggers parent notification (`NotificationService.dispatch_notification`)
- [x] Achievement read endpoint scoped correctly (`GET /v1/children/{id}/achievements` via `verify_target_child_scope`)
- [x] `criteria_json` schema documented (`docs/architecture/criteria_dsl.md`)
