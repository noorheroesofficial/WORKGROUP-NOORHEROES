# B-07 — Child Profile Reorder API

## 1. Feature Context
Part of Feature C.21 — Multi-Child Management. A low-risk convenience action letting a parent reorder how children appear across the app, implemented as an atomic batch update.

## 2. Parent Feature
C.21 Multi-Child Management

## 3. Sub-feature
**B-07 — Child Profile Reorder API** (`PATCH /v1/family/children/order`)

## 4. Objective
Persist a parent-chosen display order for all children in the family as a single all-or-nothing operation, independent of any other in-flight mutation on a different child.

## 5. Business Requirements
- FR-2: reorder listed among the standard per-child actions.
- Edge Case #4: a parent reorders children while one is mid-deletion-confirmation for a different child → independent actions, neither blocks the other.

## 6. Existing Architecture
Standard `identity` context Router → Service → Repository flow; no new infrastructure.

## 7. Existing Code to Reuse
- `require_elevated_session`.
- `ChildRepository.get_by_family_id()` (B-01) — to validate the submitted ID set against the family's actual children before applying.

## 8. Files to Create
None.

## 9. Files to Modify
- `modules/identity/api.py` — add `PATCH /v1/family/children/order`.
- `modules/identity/service.py` — add `reorder_children()`.
- `modules/identity/repository.py` — add `bulk_update_display_order()`.
- `modules/identity/schemas.py` — add `ChildReorderRequest { orderedChildIds: list[UUID] }`.
- `tests/modules/identity/test_children_reorder.py` — new test module.

## 10. Backend Requirements
- Accept `ordered_child_ids: list[UUID]`; validate the set is exactly equal to the family's current non-deleted children (no missing IDs, no foreign IDs, no duplicates) before applying anything.
- Apply the full reorder in a single transaction — any validation failure aborts the entire batch, no partial reordering.
- Assign `display_order` by list position (`0..n-1`).

## 11. KMP Requirements
K-06's reorder mode calls this once per "confirm" tap, sending the complete locally-reordered ID list.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract

**`PATCH /v1/family/children/order`**
- **Auth:** Bearer + step-up.
- **Request:**
```json
{ "orderedChildIds": ["uuid1", "uuid2", "uuid3"] }
```
- **Response 200:** the refreshed, reordered list (same shape as B-01's response).
- **Error Responses:**
  - `422` — ID set doesn't exactly match the family's current children (missing, extra, or duplicate IDs).
  - `401` — missing session/step-up.

## 14. Database Requirements
No new schema; uses `child.display_order` established in B-01.

## 15. Validation
Strict set-equality validation: `set(orderedChildIds) == set(currently_owned_child_ids)`. Reject on any mismatch with a clear, specific error rather than silently ignoring extras/missing entries.

## 16. Authentication
Bearer parent session.

## 17. Authorization
Step-up required.

## 18. Error Handling
| Scenario | Response |
|---|---|
| ID set mismatch (missing/extra/duplicate) | `422`, entire batch rejected, no partial update |
| Step-up missing | `401` |
| Empty family (nothing to reorder) | `200` no-op |

## 19. Offline First
N/A — mutating action, requires connectivity; K-06 keeps local reorder state client-side until "confirm" is tapped, so brief offline browsing of a not-yet-saved order is acceptable UX, not a backend concern.

## 20. Local Data
N/A backend.

## 21. Localization
N/A.

## 22. RTL
N/A — though note that RTL locales (Arabic/Urdu) reverse the *visual* drag direction client-side; the ID-list-based API contract is direction-agnostic, no backend concern.

## 23. Analytics
None server-side; `child_reorder_completed` fires client-side.

## 24. Performance
Single bulk update statement (`CASE ... WHEN` or per-row update inside one transaction), bounded by family size (≤ ~10 rows); trivial performance cost.

## 25. Security
Reused ownership scoping prevents a parent from reordering another family's children by supplying foreign IDs — the strict set-equality check is itself a security control, not just a UX nicety.

## 26. Library Requirements
No new libraries.

## 27. Testing
- Unit: set-equality validation rejects missing/extra/duplicate IDs.
- Unit: `bulk_update_display_order()` assigns order by list position correctly.
- Integration: all-or-nothing — a deliberately invalid batch leaves the existing order completely untouched.
- Integration: concurrent reorder + unrelated per-child mutation (e.g., disable) on a different child do not interfere with each other.
- Integration: step-up-missing rejection.

## 28. Documentation
Document the strict set-equality validation rule explicitly in the OpenAPI description, since it's a common integration-error source for client developers.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Reorder Validation Logic**
- **Objective:** Implement strict set-equality validation before any write.
- **Files to Modify:** `modules/identity/service.py`.
- **Implementation Details:** Fetch the family's current child ID set via `ChildRepository.get_by_family_id()`, compare against the submitted list as sets; on mismatch raise `ValidationError` with a message identifying missing/extra IDs (do not leak other families' IDs in the error, only which submitted IDs are invalid).
- **Tests:** Unit tests for missing, extra, and duplicate ID scenarios.
- **Definition of Done:** All three mismatch types are independently tested and correctly rejected.

**Task 02 — Atomic Bulk Update**
- **Objective:** Apply the new `display_order` values in a single transaction.
- **Files to Modify:** `modules/identity/repository.py`.
- **Implementation Details:** Use a single `UPDATE ... FROM (VALUES ...)` statement or SQLAlchemy bulk update construct — avoid N sequential single-row updates where an all-or-nothing bulk statement is available.
- **Tests:** Integration test confirming atomicity — inject a failure mid-batch (e.g., via a mocked constraint violation) and confirm zero rows change.
- **Definition of Done:** Confirmed all-or-nothing behavior under simulated partial failure.

**Task 03 — Router Wiring**
- **Objective:** Attach step-up and route the endpoint.
- **Files to Modify:** `modules/identity/api.py`.
- **Definition of Done:** End-to-end test covering happy path, validation rejection, and independence from unrelated concurrent mutations.

## 30. Definition of Done
Reorder is strictly validated, fully atomic, and provably independent of concurrent unrelated per-child mutations.

## 31. Final Verification Checklist
- [ ] Set-equality validation covers missing/extra/duplicate cases
- [ ] Bulk update is atomic (all-or-nothing verified under simulated failure)
- [ ] Independence from concurrent unrelated mutation tested
- [ ] Step-up enforced
- [ ] OpenAPI documents the set-equality validation rule
