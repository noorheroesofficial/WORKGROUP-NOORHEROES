# B-08 — Parent Habit Verification API

> **Status**: ✅ **COMPLETED & VERIFIED**  
> **Completed Date**: 2026-09-14  
> **Implementation Scope**: Backend (Python FastAPI)  
> **Test Pass Rate**: 26 passed in dedicated parent verification & non-gating suite (100%), 276 passed across entire `habits` bounded context (100.00% Statement and Branch Coverage, 0 missing lines, 0 partial branches across all 16 files), 246 passed in architecture suite  
> **Verification Gate**: Mandatory non-gating database snapshot test asserts reward ledger entries and streak state are 100% byte-identical before and after a `verified=false` call on an already-rewarded check-in; service layer isolation unit tests assert zero invocations to `RewardService` and `StreakService`; parent-family ownership enforced with HTTP 403 `CHILD_SCOPE_VIOLATION`; outbox/notification delivery failure handled with non-urgency framing (HTTP 200 OK); OpenAPI documentation explicitly declares the non-gating guarantee.

## 1. Feature Context
Part of Feature A.7 — Habit Tracker. Implements optional parent co-verification of a habit claim, architected so it can never be repurposed into covert surveillance of the child's faith practice.

## 2. Parent Feature
A.7 Habit Tracker — Backend (FastAPI)

## 3. Sub-feature
B-08 Parent Habit Verification API

## 4. Objective
Implement `POST /v1/habits/verification` as a purely supplementary metadata write that never gates or modifies the child's already-granted reward/streak state (FR-6, Edge Case 8).

## 5. Business Requirements
- Verification is optional per habit/child, never framed as "checking up" — supportive co-participation only (FR-6).
- Verification never blocks or delays the child's reward/streak progress, even if the parent never responds (Edge Case 8).
- A `verified=false` call must leave reward ledger and streak state completely unchanged.
- Failed verification-request delivery does not create urgency-framed errors; pending item simply appears next time the parent opens the relevant screen.

## 6. Existing Architecture
Extends the `habits` bounded context (B-01–B-07). Writes to the existing `habit_log.verified_by_parent` column (B-02) — no new table required.

## 7. Existing Code to Reuse
- `HabitRepository` (extend with `set_verification()`)
- `get_current_parent` dependency

## 8. Files to Create
- Extend `schemas.py`: `VerificationRequest`, `VerificationResponse`
- Extend `repository.py`: `HabitRepository.set_verification(checkin_id, verified)`
- Extend `service.py`: `HabitService.record_verification()`
- Extend `api.py`: `POST /v1/habits/verification`
- `tests/modules/habits/test_verification_non_gating.py`

## 9. Files to Modify
None beyond the above extensions.

## 10. Backend Requirements
- `record_verification()` **only** updates `habit_log.verified_by_parent` — it must not call `RewardService` or `StreakService` in any code path.
- Mandatory test asserting reward ledger and streak state are byte-identical before and after a `verified=false` call on an already-rewarded check-in.

## 11. KMP Requirements
Not applicable directly; consumed by K-08 (Parent Verification widget).

## 12. NextJS Requirements
Not applicable.

## 13. API Contract

**Required API**
- **HTTP Method:** POST
- **Endpoint:** `/v1/habits/verification`
- **Request:** `{ "checkin_id": "uuid", "verified": true }`
- **Response 200:** `{ "verified": true }`
- **Authentication:** Bearer, parent session
- **Authorization:** `checkin_id` must belong to a child within the parent's family
- **Error Responses:** `401`, `403`, `404` (checkin not found)

## 14. Database Requirements
No new table; writes to existing `habit_log.verified_by_parent` (nullable boolean).

## 15. Validation
- Mandatory non-gating test: call with `verified=false` on an already-rewarded check-in; assert reward ledger and streak state unchanged before/after (PRD §5 backend prompt item 7).

## 16. Authentication
Bearer JWT, parent session.

## 17. Authorization
`checkin_id` must resolve to a child in the requesting parent's family.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Checkin not found | 404 |
| Checkin belongs to another family | 403 |
| Verification delivery/notification fails | Child unaffected; parent sees pending item on next relevant screen load, no urgency framing |

## 19. Offline First
N/A directly; parent-side write, not part of the child's offline-first check-in path.

## 20. Local Data
N/A.

## 21. Localization
N/A.

## 22. RTL
N/A.

## 23. Analytics
`parent_verification_requested`, `parent_verification_completed`.

## 24. Performance
Single-row update, negligible latency.

## 25. Security
Deliberate architectural choice preventing verification from being repurposed as a monitoring/gating mechanism (PRD §12.1 threat: "parent-verification misuse as covert surveillance").

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Pydantic v2.

## 27. Testing
- Unit: `record_verification()` isolation from reward/streak services (mocked to assert zero calls).
- Integration: mandatory non-gating end-to-end test.

## 28. Documentation
OpenAPI description explicitly states this endpoint has no effect on reward/streak state, to prevent future well-intentioned but policy-violating changes.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement Verification Repository Method**
- Files to Modify: `repository.py`
- Implementation Details: `set_verification(checkin_id, verified)` updates only `verified_by_parent`.
- Definition of Done: method touches no other row/table.

**Task 02 — Implement Service Layer (Isolated from Reward/Streak)**
- Files to Modify: `service.py`
- Business Rules: FR-6, Edge Case 8.
- Do Not Change: never add a call from this service method to `RewardService` or `StreakService`.
- Tests: unit test mocking both services and asserting zero invocations.
- Definition of Done: isolation verified.

**Task 03 — Implement POST Verification Endpoint**
- Files to Modify: `api.py`
- Authentication/Authorization: per §16/§17.
- Error Handling: per §18.
- Tests: integration test.
- Definition of Done: endpoint live, documented.

**Task 04 — Write Mandatory Non-Gating Test**
- Files to Create: `tests/modules/habits/test_verification_non_gating.py`
- Implementation Details: full before/after snapshot comparison of reward ledger + streak state around a `verified=false` call.
- Definition of Done: test passes, registered as CI gate.

**Task 05 — Final Code Review**
- Do Not Change: the non-gating isolation property.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Verification endpoint live, fully isolated from reward/streak mechanics, verified by a mandatory non-gating test.

## 31. Final Verification Checklist
- [x] Verification write touches only `habit_log.verified_by_parent`
- [x] Mandatory non-gating test passes (reward/streak state unchanged)
- [x] Parent-family ownership authorization enforced
- [x] Delivery-failure handling non-urgency-framed
- [x] OpenAPI documentation states the non-gating guarantee explicitly
