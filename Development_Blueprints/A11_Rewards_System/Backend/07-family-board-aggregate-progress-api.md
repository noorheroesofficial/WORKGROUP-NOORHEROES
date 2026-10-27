# B-07 — Family Board Aggregate Progress API (User)

## 1. Feature Context
Part of Feature A.11 — Rewards System. Aggregate-only, multi-child sibling goal tracking, structurally guaranteed to carry no per-sibling comparison data — the same architectural guarantee already established by A.7's Family Garden (`family_streak`).

## 2. Parent Feature
A.11 Rewards System — Backend (FastAPI)

## 3. Sub-feature
B-07 Family Board Aggregate Progress API (User)

## 4. Objective
Implement `GET /v1/family/{family_id}/board`, backing FR-9, FR-15 and Edge Case 6, mirroring A.7 §3.4's Family Garden endpoint's structural no-child-field guarantee.

## 5. Business Requirements
- No public leaderboard, no sibling ranking, no per-sibling breakdown anywhere in this schema or response (FR-9).
- Only combined/aggregate progress is shown (FR-15).
- Only confirmed, synced sibling contributions count toward threshold evaluation — an offline/unsynced sibling event does not prematurely cross a threshold from another sibling's freshly-synced perspective (Edge Case 6).

## 6. Existing Architecture
Extends the `rewards` bounded context, following the exact same structural pattern as A.7's `family_streak` table/endpoint (no `child_id` column anywhere).

## 7. Existing Code to Reuse
- A.7's `family_streak` structural introspection test pattern (mirrored here for `family_board_goal`).
- `get_current_child`/`get_current_parent` dependencies (either may read the family's own board).

## 8. Files to Create
- `src/noorheroes/modules/rewards/models.py` — extend with `FamilyBoardGoal`.
- `alembic/versions/<rev>_create_family_board_goal_table.py`
- `tests/modules/rewards/test_family_board_no_child_field.py`
- `tests/modules/rewards/test_family_board_synced_only_aggregation.py`

## 9. Files to Modify
- `src/noorheroes/modules/rewards/schemas.py` — `FamilyBoardResponse` (aggregate-only fields).
- `src/noorheroes/modules/rewards/service.py` — `get_family_board(family_id)`.
- `src/noorheroes/modules/rewards/api.py` — add route.

## 10. Backend Requirements
- `family_board_goal` schema has **no `child_id` column anywhere** — structurally guaranteed, not just unused.
- Threshold evaluation only counts confirmed, synced contributions (no partial credit for in-flight/unsynced sibling events).
- Family Achievement Unlock event triggered when `aggregate_progress >= target`.

## 11. KMP Requirements
Consumed by K-08 (Family Board Experience).

## 12. NextJS Requirements
Not applicable (no admin-facing surface specified for this sub-feature beyond general content/goal seeding, which is out of scope for this blueprint).

## 13. API Contract

**Required API**
- **HTTP Method:** GET
- **Endpoint:** `/v1/family/{family_id}/board`
- **Response 200:** `{ "goals": [ { "goal_id":"...", "title":"...", "aggregate_progress": 70, "target": 100 } ] }` — no per-child field exists in this schema at all.
- **Authentication:** Bearer (parent or child session, family-scoped).
- **Authorization:** requester must belong to `family_id`.

## 14. Database Requirements
`family_board_goal`: `goal_id UUID PK`, `family_id UUID FK`, `title VARCHAR`, `aggregate_progress INT`, `target INT`. Index `(family_id)`. No `child_id` column anywhere on this table.

## 15. Validation
- Structural introspection test: scan table columns + response schema for any field name containing "child" — assert zero matches (mandatory, mirrors A.7's pattern).
- Test: an unsynced sibling contribution does not prematurely cross a threshold from a different sibling's freshly-synced read.

## 16. Authentication
Bearer JWT, parent or child session.

## 17. Authorization
Requester must belong to the requested `family_id`; no cross-family access.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| New multi-child family, zero contributions | Return the goal's description with `aggregate_progress: 0`, not an empty/404 response |
| Cross-family access attempt | 403 |
| Sibling contribution still offline/unsynced | Not counted yet; aggregate reflects only confirmed, synced data (Edge Case 6) |

## 19. Offline First
N/A for this read endpoint; individual sibling contribution events reaching this aggregate are each subject to their own originating feature's offline/sync behavior.

## 20. Local Data
N/A (backend); client-side caching detailed in K-08.

## 21. Localization
Goal titles resolved via `locale_key`/translation keys, not hardcoded.

## 22. RTL
N/A (backend).

## 23. Analytics
Emit `family_board_viewed`, `family_goal_progress_updated` (aggregate only), `family_achievement_unlocked` per PRD §1.19.

## 24. Performance
Simple aggregate read, cacheable briefly given goals change infrequently relative to read frequency.

## 25. Security
Structural no-child-id-field schema design is this endpoint's primary sibling-comparison-leakage mitigation (PRD §12.1), verified by an automated introspection test, not just a code-review convention.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, PostgreSQL, Pydantic v2.

## 27. Testing
- Unit: aggregate-progress computation correctness.
- Integration: two siblings contribute → combined threshold crossed → celebration event, no per-sibling breakdown ever exposed.
- Structural introspection test (mandatory CI gate).

## 28. Documentation
OpenAPI docs explicitly noting the aggregate-only, no-per-child-data guarantee as a documented contract property, not an implementation detail.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create `FamilyBoardGoal` Model & Migration**
- Files to Create: model + migration per §8/§14.
- Business Rules: FR-9, FR-15.
- Do Not Change: never add a `child_id`/per-sibling column to this table under any future requirement without explicit governance sign-off.
- Definition of Done: table created, structurally child-field-free.

**Task 02 — Implement `get_family_board()`**
- Files to Modify: `service.py`
- Implementation Details: aggregate-only query, synced-contributions-only counting logic.
- Business Rules: Edge Case 6.
- Tests: synced-only aggregation test.
- Definition of Done: correct aggregate values, no premature threshold-crossing.

**Task 03 — Implement Endpoint**
- Files to Modify: `api.py`
- Authentication/Authorization: per §16/§17.
- Tests: integration test.
- Definition of Done: endpoint live.

**Task 04 — Implement Structural No-Child-Field Test (Mandatory CI Gate)**
- Files to Create: `test_family_board_no_child_field.py`
- Implementation Details: reflection/introspection scan of table columns and response schema for any field name containing "child."
- Definition of Done: test passes, wired as non-bypassable CI gate.

**Task 05 — Wire Family Achievement Unlock Trigger**
- Implementation Details: emit `family_achievement_unlocked` when `aggregate_progress >= target`.
- Definition of Done: trigger verified via test.

**Task 06 — Add Documentation**
- Documentation: OpenAPI notes per §28.
- Definition of Done: docs reviewed.

**Task 07 — Final Code Review**
- Do Not Change: schema's structural no-child-field guarantee.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Family Board endpoint live, aggregate-only, structurally verified to carry no per-sibling data, synced-only threshold evaluation correct.

## 31. Final Verification Checklist
- [ ] `family_board_goal` has no `child_id`/per-sibling column anywhere
- [ ] Structural introspection test passes (CI-blocking)
- [ ] Only synced contributions count toward threshold crossing
- [ ] Cross-family access rejected
- [ ] Family Achievement Unlock event fires correctly on threshold crossing
- [ ] OpenAPI documentation states the aggregate-only guarantee explicitly
