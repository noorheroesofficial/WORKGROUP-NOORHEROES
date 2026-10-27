# B-04 — Child Disable & Session Revocation Service

## 1. Feature Context
Part of Feature C.21 — Multi-Child Management. Implements the reversible "Disable" action, the feature's core trust guarantee: data is never lost, but access is cut off immediately, everywhere.

## 2. Parent Feature
C.21 Multi-Child Management

## 3. Sub-feature
**B-04 — Child Disable & Session Revocation Service** (`POST /v1/children/{id}/disable`)

## 4. Objective
Immediately and irrevocably (until re-enabled) cut off a disabled child's ability to enter child mode from any device, while guaranteeing zero data loss — the defining distinction between "disable" and "delete."

## 5. Business Requirements
- FR-4: disable is reversible; child cannot enter child mode while disabled; active sessions and notification bindings revoked immediately; progress/history/rewards retained; re-enable available any time subject to capacity.
- Edge Case #2: parent disables a child while another device still has that child's session active → that device's session invalidated on its very next API call.
- NFR: "Data Preservation on Disable/Downgrade: Never delete or corrupt underlying data — hard, zero-tolerance guarantee."
- Acceptance Criteria: "Given a parent disables a child, then active sessions/notification bindings are revoked immediately while data remains fully intact."

## 6. Existing Architecture
New `Deletion Service`-adjacent logic lives in the existing `identity` context; session revocation reuses the existing Redis-backed JWT denylist infrastructure (`infrastructure/redis.py`) already used for logout (`AuthRepository.logout()` equivalent server-side pattern) and referenced in C.19's step-up/session model.

## 7. Existing Code to Reuse
- `get_redis_pool()` (`infrastructure/redis.py`) — reuse the existing Redis connection pool for the denylist; do not open a second pool.
- `require_elevated_session` — step-up dependency, reused.
- `ChildRepository.get_child_by_id_and_family()` — ownership lookup, reused.
- Existing JWT-denylist check inside `get_current_child` (or equivalent child-session verification dependency) — this sub-feature's job is to **populate** that denylist, not redefine how it's checked.

## 8. Files to Create
- `modules/identity/session_revocation.py` — new focused module encapsulating "revoke all active sessions/bindings for a child," reusable by both B-04 (disable) and B-06 (delete).

## 9. Files to Modify
- `modules/identity/api.py` — add `POST /v1/children/{id}/disable` route.
- `modules/identity/service.py` — add `disable_child()`.
- `modules/identity/repository.py` — add `set_status()`.
- `modules/notifications/repository.py` — add/extend `deactivate_binding(child_id)` for `device_profile_bindings` (B.17 dependency — confirm exact table/repository name against B.17's existing implementation before writing; do not invent a new binding table if one exists).
- `tests/modules/identity/test_children_disable.py` — new test module.

## 10. Backend Requirements
- Set `child.status = 'disabled'`.
- Enumerate every active session/refresh token issued for this `child_id` and add each to the Redis JWT denylist with a TTL matching the token's remaining lifetime (avoid an unbounded denylist).
- Deactivate the `device_profile_bindings` row(s) tied to this child (B.17 notification routing must stop targeting a disabled child).
- All of the above executes in a single service-layer transaction/operation sequence; if session revocation fails, the disable action must not silently report success (see Task 02).

## 11. KMP Requirements
K-04's disable confirmation flow calls this through the step-up gate; on success the card immediately reflects the disabled read-only state (K-02).

## 12. NextJS Requirements
Not applicable.

## 13. API Contract

**`POST /v1/children/{id}/disable`**
- **Auth:** Bearer + step-up.
- **Request:** none (path param `id` only).
- **Response 200:** updated `ChildProfileResponse` with `status: "disabled"`.
- **Error Responses:**
  - `404` — child not found/not owned.
  - `409` — child already disabled (or return `200` idempotently — decide and document; recommended: idempotent `200`, since re-disabling an already-disabled child is a harmless no-op, not a conflict).
  - `401` — missing session/step-up.

## 14. Database Requirements
`child.status` CHECK constraint already includes `'disabled'` (per §4.2). No new migration required beyond what B-01/B-02 already introduced.

## 15. Validation
Ownership validation only (`family_id` match); no request body to validate.

## 16. Authentication
Bearer parent session.

## 17. Authorization
Step-up required, no exceptions — this is a "mutating action" per FR-11's blanket rule.

## 18. Error Handling
| Scenario | Response |
|---|---|
| Child not found/not owned | `404` |
| Already disabled | `200` idempotent no-op (documented decision) |
| Step-up missing | `401` |
| Redis denylist write fails | `500`, and the status change must roll back — do not report success with a live stale session still valid |

## 19. Offline First
N/A — mutating action, requires connectivity.

## 20. Local Data
N/A backend; K-09 invalidates its local cache for this child on success.

## 21. Localization
N/A.

## 22. RTL
N/A.

## 23. Analytics
None server-side; `child_disable_initiated`/`_completed` fire client-side.

## 24. Performance
Single-row update + bounded Redis writes (one per active session, typically 1-3); well within p95 targets.

## 25. Security
This is the feature's most safety-critical guarantee: a disabled child must not remain reachable via a previously-issued token even for a single extra request. The denylist write and the status update must be treated as a single logical unit — a threat model entry in §12.1 explicitly calls out "stale session continuation after disable" as mitigated specifically by this control.

## 26. Library Requirements
No new libraries; reuses existing Redis client.

## 27. Testing
- **Highest-priority test (per PRD §5 backend AI prompt item 2):** create an active child session → call disable → assert the very next API call using that session's token is rejected.
- Unit: `disable_child()` sets status and calls session-revocation module.
- Unit: session-revocation module correctly enumerates and denylists all active tokens for a child (not just one).
- Integration: `device_profile_bindings` deactivated on disable.
- Integration: already-disabled child → idempotent `200`.
- Integration: step-up-missing rejection.
- Integration: Redis failure during revocation → status change rolls back, no partial-success state.

## 28. Documentation
Explicitly document in the OpenAPI description that this is a reversible, data-preserving action distinct from deletion, and that it revokes sessions immediately.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Session Revocation Module**
- **Objective:** Build a reusable `revoke_all_sessions_for_child(child_id)` helper.
- **Why Required:** Both B-04 (disable) and B-06 (delete) need identical "kill every live session for this child" behavior — a single shared implementation prevents drift.
- **Files to Create:** `modules/identity/session_revocation.py`.
- **Implementation Details:** Query active session/refresh-token records for `child_id` (reuse whatever session tracking A.1/C.19 already persists — do not invent a new session table), write each token's JTI to the Redis denylist with TTL = remaining token lifetime, via `get_redis_pool()`.
- **Dependencies:** Existing Redis pool, existing session-tracking table (locate via C.19's blueprint before assuming a name).
- **Tests:** Unit test with 3 simulated active sessions, assert all 3 denylisted.
- **Definition of Done:** Helper is transaction-safe and independently unit-tested before being wired into B-04's service method.

**Task 02 — Disable Service Method with Atomicity Guarantee**
- **Objective:** `disable_child()` sets status, deactivates bindings, revokes sessions — all-or-nothing.
- **Files to Modify:** `modules/identity/service.py`.
- **Implementation Details:** Wrap status update and binding deactivation in the request-scoped DB transaction (auto-committed by `get_db_session`); if Redis revocation raises, re-raise before the transaction commits so the DB change rolls back too — avoid the "disabled in DB but sessions still valid" inconsistent state.
- **Error Handling:** Surface a `500` with clear logging if Redis is unreachable; never report `200` success while sessions remain live.
- **Tests:** Failure-injection test simulating Redis unavailability.
- **Definition of Done:** No code path exists where the DB shows `disabled` but a live session remains valid.

**Task 03 — Binding Deactivation Integration**
- **Objective:** Ensure `device_profile_bindings` (B.17) stop targeting a disabled child.
- **Files to Modify:** `modules/notifications/repository.py` (confirm exact existing method name against B.17's implementation first).
- **Do Not Change:** B.17's binding creation/re-establishment logic — this task only deactivates, re-establishment on re-enable is explicitly out of scope here (owned by B.17/C.19's Who Is Learning flow per Edge Case #10).
- **Tests:** Integration test confirming binding row's active flag flips.
- **Definition of Done:** Binding correctly deactivated without touching unrelated notification logic.

**Task 04 — Router & Idempotency**
- **Objective:** Wire the route with step-up and idempotent-already-disabled handling.
- **Files to Modify:** `modules/identity/api.py`.
- **Definition of Done:** Route tested end-to-end including the idempotent-replay case.

## 30. Definition of Done
Disable is atomic across status, bindings, and session revocation; the highest-priority "next call rejected" test passes; no data outside `status`/bindings/sessions is touched.

## 31. Final Verification Checklist
- [ ] Live-session-rejected-on-next-call test passes (highest priority)
- [ ] All active sessions (not just one) are denylisted
- [ ] `device_profile_bindings` deactivated
- [ ] Disable/session-revocation is atomic (no partial-success state)
- [ ] Idempotent on already-disabled child
- [ ] Step-up enforced
- [ ] No PostgreSQL/Redis credential changes
