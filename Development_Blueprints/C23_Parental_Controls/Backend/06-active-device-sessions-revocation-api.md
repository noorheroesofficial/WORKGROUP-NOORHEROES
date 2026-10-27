# B-06 — Active Device Sessions & Revocation API

## 1. Feature Context
Under Child Locks & Sessions, a parent can view every active device a child is using and revoke any of them, force-logging-out that session (PRD C.23 FR-9, §2.3, §3.4).

## 2. Parent Feature
Feature C.23 — Parental Controls (Screen Time, Bedtime, AI Permissions, Content Age Level)

## 3. Sub-feature
1.6 Active Device Sessions & Revocation API (ID: **B-06**)

## 4. Objective
Implement `GET /v1/sessions` and `DELETE /v1/sessions/{id}` for family/child-mode session listing and revocation, force-logging-out the revoked session while allowing an already-authenticated in-flight request to complete.

## 5. Business Requirements
- FR-9: view/revoke active device list; revoking a device force-logs-out that session.
- Edge Case 9: a device revoked mid-in-flight-request — the in-flight request completes if already authenticated before revocation, but subsequent requests fail immediately.
- PRD §3.4/§3.3: this contract is described as "reused from A.1/C.19's session list contract."

## 6. Existing Architecture — Resolved
The PRD states this endpoint is "reused from A.1/C.19's session list contract." **This was investigated by reading C.19 B-04 ("Child-Mode Session Activation & Sibling Isolation API") in full.** Finding: C.19 B-04 issues a **stateless, signed JWT `session_token`** (claims `{family_id, child_id, device_id, exp}`) via `POST /v1/sessions/child-mode` — there is no persisted, listable session record with `device_name`/`last_active_at` anywhere in the reviewed codebase. C.19 B-04 §12 explicitly notes revocation as *optional*: "if server-side revocation is required, a lightweight `child_session` Redis entry keyed by token ID with TTL = `expires_at`." B-06 is the sub-feature that makes this optional mechanism **required and concrete**.

**Resolution — build net-new, coordinated with C.19 B-04:**
1. Add a `device_sessions` Postgres table (listing/display data: `session_id`, `child_id`, `family_id`, `device_name`, `last_active_at`, `revoked_at`) — a row is inserted at the moment C.19 B-04's `SessionActivationService.activate()` issues a `session_token`. This requires a small, additive change to C.19 B-04's `session_service.py` (insert one row on successful activation) — coordinate this as a cross-feature dependency, not a duplicate implementation.
2. Implement the Redis-backed revocation denylist that C.19 B-04 left optional, keyed by `session_token`'s JWT ID (`jti` claim), TTL = token `exp`. This is a shared mechanism: C.19 B-04's `require_child_session` dependency (and the equivalent parent-session check) must consult this denylist on every request — a small addition to `core/deps.py`, owned here since B-06 is what makes revocation a real, required guarantee.
3. Implement `GET /v1/sessions` / `DELETE /v1/sessions/{id}` net-new in `modules/access_gate` (the module already owning `child_lock` and session-activation per C.19 B-01/B-04).

## 7. Existing Code to Reuse
- `core/deps.py::ParentSessionContext`, `ChildSessionContext` — existing session DTOs, extended (not replaced) with a denylist check
- `modules/access_gate/session_token.py` (C.19 B-04) — the JWT issuance/validation utility; extend with `jti` claim support if not already present, needed to key the Redis denylist
- `modules/access_gate/session_service.py::SessionActivationService.activate()` (C.19 B-04) — extend to insert the `device_sessions` listing row
- `infrastructure/redis.py::get_redis_pool`

## 8. Files to Create
- `src/noorheroes/modules/access_gate/session_models.py` — `DeviceSessionOrm`
- `src/noorheroes/modules/access_gate/session_schemas.py` — `SessionListResponse`, `SessionResponse`
- `src/noorheroes/modules/access_gate/session_repository.py` — `DeviceSessionRepository`
- `src/noorheroes/modules/access_gate/session_revocation.py` — Redis denylist helper (`add_to_denylist(jti, ttl)`, `is_revoked(jti) -> bool`), consumed by `core/deps.py`
- `src/noorheroes/modules/access_gate/session_service.py` (extend C.19 B-04's file, do not create a parallel one) — add `DeviceSessionService(BaseService)` alongside the existing `SessionActivationService`
- `alembic/versions/xxxx_create_device_sessions.py`
- `tests/modules/access_gate/test_session_service.py`
- `tests/modules/access_gate/test_session_api.py`
- `tests/modules/access_gate/test_session_revocation_denylist.py`

## 9. Files to Modify
- `src/noorheroes/modules/access_gate/api.py` — add `GET /v1/sessions`, `DELETE /v1/sessions/{id}`
- `src/noorheroes/modules/access_gate/session_service.py::SessionActivationService.activate()` (C.19 B-04) — insert a `device_sessions` row on successful activation, including `jti` from the issued token
- `src/noorheroes/modules/access_gate/session_token.py` (C.19 B-04) — ensure the signed JWT includes a `jti` (JWT ID) claim if not already present, so it can key the Redis denylist
- `src/noorheroes/core/deps.py::require_child_session` (C.19 B-04) and `get_current_parent` — add a denylist check (`session_revocation.is_revoked(jti)`) before accepting any token as valid

## 10. Backend Requirements
- `DeviceSessionService.list_sessions(parent_ctx)`: return all active (non-revoked) sessions across all children in the family, including `device_name`, `last_active_at`, `child_id`, from `device_sessions`.
- `DeviceSessionService.revoke_session(session_id, parent_ctx)`:
  1. Require fresh step-up.
  2. Verify family ownership of the session.
  3. Mark `revoked_at = now()` in `device_sessions`; add the session's `jti` to the Redis revocation denylist (TTL = remaining time to the token's `exp`, so denylist entries self-expire and never accumulate indefinitely).
  4. **Do not** retroactively fail a request that was already authenticated before this revocation timestamp — the denylist check happens at token-validation time on each new request (in `core/deps.py::require_child_session`/`get_current_parent`), so an in-flight request that already passed auth naturally completes; only the *next* request from that device fails.
  5. Emit `DeviceRevoked` outbox event.
- Extension to C.19 B-04's `SessionActivationService.activate()`: after issuing `session_token`, insert a `device_sessions` row (`session_id = jti`, `child_id`, `family_id`, `device_name` from the request's device context, `last_active_at = now()`, `revoked_at = NULL`).

## 11. API Contract

### `GET /v1/sessions`
- **Auth:** Bearer (parent)
- **Response 200:** `{ "sessions": [ { "session_id": "...", "child_id": "...", "device_name": "...", "last_active_at": "..." } ] }`
- **Error Responses:** `401 UNAUTHORIZED`

### `DELETE /v1/sessions/{id}`
- **Auth:** Bearer (parent) + step-up
- **Response 204:** No content
- **Error Responses:** `401 UNAUTHORIZED`, `403 FORBIDDEN`, `404 SESSION_NOT_FOUND`

## 12. Database Requirements
`device_sessions` (net-new): `session_id PK` (= token `jti`), `child_id FK`, `family_id FK`, `device_name VARCHAR`, `last_active_at TIMESTAMPTZ`, `revoked_at TIMESTAMPTZ NULL`, index `(family_id, revoked_at)`. Redis: denylist keys `session_revocation:{jti}`, TTL = seconds remaining until token `exp` at time of revocation.

## 13. Validation
- `session_id` must belong to the caller's family.

## 14. Authentication
`Depends(get_current_parent)` for GET; PATCH/DELETE additionally requires `Depends(require_elevated_session)`.

## 15. Authorization
Family-ownership check on the session record.

## 16. Error Handling
| Scenario | Response |
|---|---|
| Session not found/not owned | 404 SESSION_NOT_FOUND |
| Missing step-up on DELETE | 403 FORBIDDEN |
| Revocation during in-flight request from that device | In-flight request (already authenticated) completes; next request fails auth |

## 17. Offline First
N/A (backend).

## 18. Local Data
N/A (backend); consumed by K-06's Active Device List UI.

## 19. Localization
`device_name` is a raw string (device model/OS), not localized; `last_active_at` formatted client-side.

## 20. RTL
N/A.

## 21. Analytics
Backing source for `device_revoked`.

## 22. Performance
Low-volume, parent-initiated only.

## 23. Security
Revocation denylist check must be enforced on every authenticated request path (`get_current_parent`, `get_current_child`/`require_child_session`), not only at login — otherwise a revoked session's still-valid JWT would continue to work until natural expiry, violating "force-logs-out." This closes a gap C.19 B-04 explicitly left optional ("if server-side revocation is required") — B-06 makes it a hard requirement.

## 24. Library Requirements
Redis (`infrastructure/redis.py::get_redis_pool`, already used elsewhere in the codebase), PyJWT (already used by C.19 B-04 for token issuance — reuse its `jti` claim support rather than adding a new JWT library).

## 25. Testing
- Unit: revoke a session → confirm subsequent request with that session's token fails auth via the denylist check.
- Unit: an in-flight request already past auth-check completes even if revocation occurs mid-request (simulate via test timing/mocking).
- Unit: denylist entry TTL matches the token's remaining `exp` time (no indefinite accumulation).
- Integration: full activate (C.19 B-04) → list → revoke → child-mode session force-logged-out flow, proving the cross-feature wiring works end-to-end.
- Integration: `device_sessions` row is correctly created at activation time (proves the C.19 B-04 extension is wired correctly).

## 26. Documentation
OpenAPI description must state the in-flight-request exception explicitly, since it's a subtle, easy-to-misimplement behavior.

## 27. AI Coding Agent Implementation Steps

**Task 01 — Confirm C.19 B-04 Is Implemented and Add `jti` Claim**
- Objective: Verify `session_token.py`'s JWT issuance includes a `jti` (JWT ID) claim; add it if missing, since it's required to key both `device_sessions.session_id` and the Redis denylist.
- Files to Modify: `modules/access_gate/session_token.py` (C.19 B-04)
- This task blocks all subsequent tasks — it's a small, additive change to existing code, not a rebuild.

**Task 02 — Create `DeviceSessionOrm` Model**
- Files to Create: `session_models.py`

**Task 03 — Create Migration**
- Files to Create: `alembic/versions/xxxx_create_device_sessions.py`

**Task 04 — Create Schemas**
- Files to Create: `session_schemas.py`

**Task 05 — Implement `DeviceSessionRepository`**
- Files to Create: `session_repository.py`

**Task 06 — Implement Redis Revocation Denylist Helper**
- Files to Create: `session_revocation.py`
- Implementation Details: `add_to_denylist(jti, ttl_seconds)`, `is_revoked(jti) -> bool`.

**Task 07 — Wire Denylist Check into Token Validation**
- Files to Modify: `core/deps.py::require_child_session`, `get_current_parent` (C.19 B-04's dependencies)
- Implementation Details: Call `session_revocation.is_revoked(jti)` before accepting any token; reject with 401 if revoked.
- Dependencies: Task 06.

**Task 08 — Extend `SessionActivationService.activate()` to Insert Listing Row**
- Files to Modify: `modules/access_gate/session_service.py` (C.19 B-04's existing file)
- Implementation Details: On successful activation, insert one `device_sessions` row keyed by the issued token's `jti`.
- Dependencies: Tasks 01, 02, 05.

**Task 09 — Implement `DeviceSessionService` (list/revoke)**
- Files to Modify: `modules/access_gate/session_service.py` (add alongside `SessionActivationService`, not a parallel file)
- Dependencies: Tasks 02–08.

**Task 10 — Implement API Endpoints**
- Files to Modify: `modules/access_gate/api.py`
- Implementation Details: `GET /v1/sessions`, `DELETE /v1/sessions/{id}`.

**Task 11 — Add Step-Up Enforcement on DELETE**

**Task 12 — Add In-Flight-Request Exception Test**
- Files to Create: `tests/modules/access_gate/test_session_service.py`

**Task 13 — Add Denylist TTL and Cross-Feature Integration Tests**
- Files to Create: `tests/modules/access_gate/test_session_revocation_denylist.py`, `tests/modules/access_gate/test_session_api.py`
- Coverage: full C.19 B-04 activate → B-06 list → revoke → force-logout flow.

**Task 14 — Add API Documentation**

**Task 15 — Final Code Review**
- Objective: Confirm no parallel/duplicate session mechanism was built alongside C.19 B-04's existing `SessionActivationService` — this file extends it.

## 28. Definition of Done
- `device_sessions` row is correctly created at C.19 B-04 activation time.
- Revocation denylist is enforced on every authenticated request path, confirmed by cross-feature integration test.
- Revocation correctly force-logs-out a session on its next request while allowing an already-authenticated in-flight request to complete.

## 29. Final Verification Checklist
- [ ] `jti` claim added to C.19 B-04's token issuance (or confirmed already present)
- [ ] `device_sessions` row created at activation time (cross-feature integration test passes)
- [ ] Redis denylist enforced in `core/deps.py` on every authenticated request path
- [ ] Denylist entries self-expire via TTL matching token `exp`
- [ ] In-flight-request exception tested
- [ ] Step-up required on DELETE
- [ ] No duplicate/parallel session-activation service created
- [ ] OpenAPI documents the in-flight-request behavior
