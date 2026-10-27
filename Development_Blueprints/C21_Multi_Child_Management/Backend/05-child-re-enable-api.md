# B-05 — Child Re-Enable API (Plan-Capacity Gated)

## 1. Feature Context
Part of Feature C.21 — Multi-Child Management. Mirror action to B-04's disable — restores a disabled child to full access, but only within current plan capacity, never as a silent failure.

## 2. Parent Feature
C.21 Multi-Child Management

## 3. Sub-feature
**B-05 — Child Re-Enable API (Plan-Capacity Gated)** (`POST /v1/children/{id}/enable`)

## 4. Objective
Restore a disabled child to `active` status with all prior data immediately intact, but block the action with a clear upsell path if doing so would exceed current plan capacity (FR-12).

## 5. Business Requirements
- FR-12: re-enabling a disabled child is itself subject to current plan capacity — blocked with clear upsell path if at limit, never a silent failure.
- Acceptance Criteria: "Given a parent re-enables a child within plan capacity, then the child becomes immediately able to enter child mode with all prior data intact; at capacity, re-enable is blocked with a clear upsell path."
- Edge Case #10: re-enabled child's notification binding is re-established the next time their profile is selected via Who Is Learning (C.19/B.17) — **not** orchestrated by this endpoint.

## 6. Existing Architecture
Same `identity` context service/repository pattern; reuses C.24's `SubscriptionService.get_entitlement()` exactly as B-03 does for creation.

## 7. Existing Code to Reuse
- `SubscriptionService.get_entitlement()` — reused capacity check, identical semantics to B-03.
- `require_elevated_session` — step-up.
- `ChildRepository.get_child_by_id_and_family()` — ownership lookup.
- `EntitlementLimitExceededError` → `403 PLAN_CAPACITY_EXCEEDED`.

## 8. Files to Create
None.

## 9. Files to Modify
- `modules/identity/api.py` — add `POST /v1/children/{id}/enable`.
- `modules/identity/service.py` — add `enable_child()`.
- `modules/identity/repository.py` — reuse `set_status()` from B-04.
- `tests/modules/identity/test_children_enable.py` — new test module.

## 10. Backend Requirements
- Re-check capacity: `active_child_count < max_child_limit` **including** the child being re-enabled in the prospective count (i.e., would re-enabling this child push the family over the limit).
- On success, set `child.status = 'active'`; no other field is touched — data was never modified by disable, so nothing needs restoring.
- Do **not** re-establish notification bindings here — that is explicitly B.17/C.19's responsibility on next profile selection (Edge Case #10); keep this endpoint's blast radius to `status` only.

## 11. KMP Requirements
K-04's re-enable confirmation flow; on `403 PLAN_CAPACITY_EXCEEDED`, routes to K-07's blocked state with upsell CTA to `:feature:subscription`.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract

**`POST /v1/children/{id}/enable`**
- **Auth:** Bearer + step-up.
- **Request:** none.
- **Response 200:** updated `ChildProfileResponse` with `status: "active"`.
- **Error Responses:**
  - `403 PLAN_CAPACITY_EXCEEDED` — `{ "current": 3, "limit": 3 }`.
  - `404` — not found/not owned.
  - `401` — missing session/step-up.

## 14. Database Requirements
No schema changes beyond what B-01/B-04 already introduced.

## 15. Validation
Ownership check; capacity check.

## 16. Authentication
Bearer parent session.

## 17. Authorization
Step-up required.

## 18. Error Handling
| Scenario | Response |
|---|---|
| At/over capacity | `403 PLAN_CAPACITY_EXCEEDED` with `{current, limit}` |
| Already active | `200` idempotent no-op |
| Not found/not owned | `404` |
| Step-up missing | `401` |

## 19. Offline First
N/A — mutating action, requires connectivity.

## 20. Local Data
N/A backend.

## 21. Localization
N/A.

## 22. RTL
N/A.

## 23. Analytics
None server-side; `child_enable_initiated`/`_completed`/`_blocked_plan_capacity` fire client-side.

## 24. Performance
Single-row update behind a cheap capacity check; well within performance targets.

## 25. Security
Capacity check is server-side only, consistent with B-03's guarantee that plan limits can never be bypassed by a client-side assumption.

## 26. Library Requirements
No new libraries.

## 27. Testing
- Unit: capacity-exceeded rejection with correct `{current, limit}`.
- Unit: capacity check correctly counts the target child as part of the prospective active set.
- Integration: full re-enable happy path — verify all prior progress/history/rewards data is intact (query related tables, confirm untouched).
- Integration: at-capacity rejection with upsell-routable error shape.
- Integration: step-up-missing rejection.

## 28. Documentation
Document `403 PLAN_CAPACITY_EXCEEDED` explicitly; document that this endpoint does not re-establish notification bindings (cross-reference B.17/C.19).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Capacity Re-Check Logic**
- **Objective:** Correctly determine whether re-enabling would exceed plan capacity.
- **Files to Modify:** `modules/identity/service.py`.
- **Implementation Details:** Count current `active` children for the family, compare `count + 1` (the child being enabled) against `max_child_limit` from `SubscriptionService.get_entitlement()`.
- **Business Rules:** The disabled child itself must not be double-counted if some other code path considers it "active" prematurely — verify against B-04's status semantics.
- **Tests:** Unit test at exactly-at-limit and one-under-limit boundary conditions.
- **Definition of Done:** Boundary conditions verified with explicit tests (off-by-one is the most likely bug here).

**Task 02 — Enable Service Method**
- **Objective:** `enable_child()` sets status only, touches nothing else.
- **Files to Modify:** `modules/identity/service.py`, `modules/identity/repository.py` (reuse `set_status()`).
- **Do Not Change:** Do not add binding re-establishment logic here — explicitly out of scope per Edge Case #10.
- **Tests:** Data-integrity test confirming progress/history/rewards rows are untouched across a disable→enable cycle.
- **Definition of Done:** Re-enable is a pure status flip with zero side effects beyond that field.

**Task 03 — Router Wiring**
- **Objective:** Attach step-up and route the endpoint.
- **Files to Modify:** `modules/identity/api.py`.
- **Definition of Done:** End-to-end test covering happy path, capacity block, and step-up rejection.

## 30. Definition of Done
Re-enable correctly gated by capacity with proper boundary handling; all prior data verified intact; no unintended side effects on notification bindings.

## 31. Final Verification Checklist
- [ ] Capacity boundary conditions tested (at-limit, one-under)
- [ ] Data-integrity test confirms zero data loss across disable→enable
- [ ] Notification-binding re-establishment explicitly NOT performed here
- [ ] Step-up enforced
- [ ] `403 PLAN_CAPACITY_EXCEEDED` payload shape matches B-03's for consistent client handling
