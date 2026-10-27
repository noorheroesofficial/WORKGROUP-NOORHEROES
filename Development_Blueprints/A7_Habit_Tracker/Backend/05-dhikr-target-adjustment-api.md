# B-05 — Dhikr Target Adjustment API

> **Status**: ✅ **COMPLETED & VERIFIED**  
> **Completed Date**: 2026-09-14  
> **Implementation Scope**: Backend (Python FastAPI)  
> **Test Pass Rate**: 67 passed in `tests/modules/habits/test_dhikr_target_adjustment.py` (100%), 190 passed across entire `habits` module (85.70% coverage, zero missing lines across all B-05 files)  
> **Verification Gate**: Proportional recalculation formula verified under Edge Case 6 (smaller & larger target boundaries, zero & missing scenarios, ownership isolation, invalid value rejection, and dual-wire serialization).

## 1. Feature Context
Part of Feature A.7 — Habit Tracker. Supports the Dhikr Counter's distinct interaction model (a numeric target rather than a checkbox), including mid-day target changes without losing progress.

## 2. Parent Feature
A.7 Habit Tracker — Backend (FastAPI)

## 3. Sub-feature
B-05 Dhikr Target Adjustment API

## 4. Objective
Implement `PATCH /v1/habits/{habit_id}/target` to update a Dhikr Counter's daily target with proportional preservation of today's progress, backing Edge Case 6.

## 5. Business Requirements
- Changing target mid-day preserves progress proportionally, never resets to zero (Edge Case 6).
- If new target is smaller than current progress, progress caps at the new target (e.g., 80/100 → target 50 → displayed as 50/50, "target reached").
- Only the owning child (or parent, if the UX exposes parent-side adjustment) may change a habit's target.

## 6. Existing Architecture
Extends the `habits` bounded context (B-01–B-04). `target_config` already exists as a `JSONB` column on `HabitDefinition` (B-01) — this sub-feature adds the mutation endpoint and recalculation logic against that existing column, it does not introduce a new table.

## 7. Existing Code to Reuse
- `HabitRepository` (extend with `update_target()`)
- `get_current_child` dependency

## 8. Files to Create
- Extend `schemas.py`: `TargetUpdateRequest`, `TargetUpdateResponse`
- Extend `repository.py`: `HabitRepository.update_target()`, `get_today_progress()`
- Extend `service.py`: `HabitService.adjust_dhikr_target()`
- Extend `api.py`: `PATCH /v1/habits/{habit_id}/target`
- `tests/modules/habits/test_dhikr_target_adjustment.py`

## 9. Files to Modify
None beyond the extensions above — no schema migration required (`target_config JSONB` already exists).

## 10. Backend Requirements
- Compute today's current progress from `habit_log`/an accumulated-count field within `target_config` (implementation choice: either a running count stored in `target_config.progress_today` updated by the batched Dhikr check-in calls, or derived from a count of today's Dhikr `habit_log` entries — choose whichever the B-02 Dhikr batching implementation actually persists, and document the choice explicitly since the PRD's Dhikr interaction is "batched/throttled, not per-tap" per §2.3 click-mapping table).
- Recalculation formula: `new_progress = min(current_progress, new_target)`.
- Persist new target and recalculated progress atomically.

## 11. KMP Requirements
Not applicable directly; consumed by K-02 (Dhikr Counter target-change interaction).

## 12. NextJS Requirements
Not applicable.

## 13. API Contract

**Required API**
- **HTTP Method:** PATCH
- **Endpoint:** `/v1/habits/{habit_id}/target`
- **Request:** `{ "new_target": 50 }`
- **Response 200:** `{ "updated": true, "today_progress_recalculated": 50 }`
- **Authentication:** Bearer, child-mode
- **Authorization:** habit must belong to the requesting child
- **Validation:** `new_target` must be a positive integer within a sane bound (e.g., 1–10,000)
- **Error Responses:** `400` invalid target value; `403` habit not owned by child; `404` habit not found

## 14. Database Requirements
No new tables. Update against existing `habit_definition.target_config` (B-01).

## 15. Validation
- Boundary test: new target smaller than current progress → progress caps at new target, not an invalid state.
- Boundary test: new target larger than current progress → progress preserved unchanged (e.g., 50/100 → 50/150).

## 16. Authentication
Bearer JWT, child-mode session.

## 17. Authorization
Child restricted to their own habit's target.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Invalid/negative target | 400 |
| Habit not owned by child | 403 |
| Habit not found | 404 |
| Concurrent target-change + check-in race | Last-write-wins on target; check-in idempotency (B-02) unaffected |

## 19. Offline First
Client applies target change optimistically; server call retried via the offline outbox (K-06) if offline at the time of change.

## 20. Local Data
N/A (backend); local recalculation logic mirrored client-side in K-02 for optimistic UI.

## 21. Localization
N/A.

## 22. RTL
N/A.

## 23. Analytics
`dhikr_target_changed_midday` emitted by the client on successful response (K-02 owns event firing).

## 24. Performance
Single-row update, negligible latency impact.

## 25. Security
Standard ownership check; no elevated risk surface.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Pydantic v2.

## 27. Testing
- Unit: proportional recalculation formula, including the smaller-target boundary case.
- Integration: full PATCH request/response cycle.

## 28. Documentation
OpenAPI schema with explicit example of the smaller-target boundary case in the description.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement Target Update Repository Method**
- Files to Modify: `repository.py`
- Implementation Details: `update_target(habit_id, new_target)` reading/writing `target_config`.
- Definition of Done: repository method correctly persists new target.

**Task 02 — Implement Proportional Recalculation Service Logic**
- Files to Modify: `service.py`
- Business Rules: Edge Case 6 formula (§10).
- Tests: unit tests for both larger-target and smaller-target-than-progress cases.
- Definition of Done: recalculation formula verified correct for both boundary directions.

**Task 03 — Implement PATCH Endpoint**
- Files to Modify: `api.py`
- Authentication/Authorization: per §16/§17.
- Error Handling: per §18.
- Tests: integration test.
- Definition of Done: endpoint live, documented, tested.

**Task 04 — Final Code Review**
- Do Not Change: `HabitDefinition.target_config` schema shape beyond what's needed (avoid breaking B-01's catalog read).
- Expected Result: PR merge-ready.

## 30. Definition of Done
Target adjustment endpoint live with correct proportional-preservation behavior in both directions, fully tested and documented.

## 31. Final Verification Checklist
- [x] Larger-target case preserves progress unchanged
- [x] Smaller-target case caps progress at new target ("target reached")
- [x] Ownership authorization enforced
- [x] Error handling matches §18
- [x] Unit + integration tests passing
- [x] OpenAPI documentation includes boundary-case example
