# B-02 — Child Lock Recovery API

## 1. Feature Context
When a child forgets their lock, recovery must **always** route through a freshly-verified Parent Profile session — never a generic "forgot lock" bypass. This is a hard, zero-exception platform rule (PRD FR-6). This sub-feature issues a scoped recovery token reachable only after B-03's Parent Gate has already succeeded in the current session.

## 2. Parent Feature
Feature C.19 — Parent PIN/Biometric Gate & Profile Access Control

## 3. Sub-feature
1.2 Child Lock Recovery API (ID: **B-02**)

## 4. Objective
Implement `POST /v1/children/{id}/lock/recover`, enforcing that it is unreachable without a bearer token representing an already-verified Parent Profile session, and that the child's original lock configuration is preserved unchanged if the parent abandons the flow before setting a new lock.

## 5. Business Requirements
- FR-6: lock recovery never routes through a generic bypass — always via verified Parent Profile.
- Edge Case 4: parent backs out before resetting the new lock → original lock configuration remains unchanged and functional.
- This is flagged in the PRD's own backend AI-generation prompt as one of the two highest-priority guarantees in the entire service (alongside strict session-to-child_id binding, B-04).

## 6. Existing Architecture
Lives in `modules/access_gate` alongside B-01. Depends on a session-level "Parent Gate freshly verified" flag issued by B-03 — this is **not** a database flag but a short-lived, server-side verification marker (e.g., a signed claim on the bearer token or a Redis-backed session flag with a short TTL) set only immediately after `POST /v1/auth/pin/verify` succeeds.

## 7. Existing Code to Reuse
- `modules/access_gate/lock_repository.py::ChildLockRepository` (B-01, extend with `update_lock_config`)
- `core/deps.py` — extend with `require_verified_parent_gate` dependency consuming B-03's session marker
- `common/security/credential_hasher.py`

## 8. Files to Create
- `src/noorheroes/modules/access_gate/recovery_schemas.py` — `LockRecoveryResponse`
- `src/noorheroes/modules/access_gate/recovery_service.py` — `ChildLockRecoveryService`
- `tests/modules/access_gate/test_recovery_service.py`
- `tests/modules/access_gate/test_recovery_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/access_gate/api.py` — add `POST /v1/children/{id}/lock/recover`
- `src/noorheroes/core/deps.py` — add `require_verified_parent_gate` dependency

## 10. Backend Requirements
- `require_verified_parent_gate` dependency: rejects with `403 PARENT_GATE_NOT_VERIFIED` any request whose bearer token/session does not carry a fresh (non-expired) Parent Gate verification marker set by B-03.
- `ChildLockRecoveryService.initiate_recovery(child_id, parent_ctx)`: validates family ownership of `child_id`, issues a short-lived, single-use `recovery_token` (JWT or opaque, TTL ~5 minutes) scoped to `child_id` + `parent_id`.
- A separate, existing "set/reset child lock" endpoint (owned by A.1's onboarding config, or extended here if not present) must itself require a valid `recovery_token` when called in a recovery context — confirm against A.1's child-lock-configuration endpoint before adding a new one (do not duplicate).
- If the parent abandons the flow (token expires unused), no lock-config mutation occurs — the original `child_lock` row is untouched by design, since recovery only issues a token; it does not itself mutate the lock.

## 11. API Contract

### `POST /v1/children/{id}/lock/recover`
- **Auth:** Bearer, **and** `require_verified_parent_gate` (session must carry a fresh Parent Gate success marker from B-03)
- **Request:** none (child id from path)
- **Response 200:** `{ "recovery_token": "..." }`
- **Error Responses:** `401 UNAUTHORIZED`, `403 PARENT_GATE_NOT_VERIFIED`, `404 CHILD_NOT_FOUND`

## 12. Database Requirements
No new persistent table. `recovery_token` is issued as a signed, short-TTL token (not persisted) or, if server-side revocation is desired, a lightweight `recovery_token` row in Redis with TTL — no PostgreSQL table required.

## 13. Validation
`child_id` must exist and belong to caller's family. No request body to validate beyond auth context.

## 14. Authentication
Bearer token **plus** the fresh Parent Gate marker — this is a compound authentication requirement, not satisfied by a valid bearer token alone.

## 15. Authorization
Family ownership of `child_id`. The Parent Gate marker itself must belong to the same parent/family as the target child.

## 16. Error Handling
| Scenario | Response |
|---|---|
| No Parent Gate marker present, or expired | `403 PARENT_GATE_NOT_VERIFIED` |
| Unknown/not-owned `child_id` | `404 CHILD_NOT_FOUND` |
| Recovery token requested repeatedly | Each call issues a new independent token; no rate limiting beyond the Parent Gate's own lockout (B-03) |

## 17. Offline First
Not applicable — recovery is an online-only, parent-present flow by design (no offline recovery path exists or should exist).

## 18. Analytics
Feeds client-side `lock_recovery_initiated` event (KMP K-04) upon receiving a successful `recovery_token`.

## 19. Performance
Single indexed lookup plus token issuance — p95 < 150ms.

## 20. Security
- **This endpoint's entire security value is that it is unreachable without B-03 having already succeeded in this session.** The `require_verified_parent_gate` dependency must be structurally impossible to bypass — no alternate code path, no default-allow.
- `recovery_token` is single-purpose (scoped to one `child_id`), short-TTL, and must not be reusable across children or sessions.
- No PIN/pattern value is ever part of this endpoint's request or response.

## 21. Library Requirements
FastAPI, PyJWT (or existing token-issuance utility if one exists — confirm against A.1's session-token issuance code before adding a new JWT dependency), Redis (if token revocation tracking is used).

## 22. Testing
- Unit: request without a fresh Parent Gate marker → `403 PARENT_GATE_NOT_VERIFIED` (highest-priority test in this sub-feature).
- Unit: request with an **expired** Parent Gate marker → `403`.
- Integration: full flow — B-03 verify succeeds → B-02 recover succeeds → token usable exactly once against the lock-set endpoint.
- Integration: abandoned recovery (token unused, expires) → original `child_lock` row unchanged.
- Integration: cross-family `child_id` → `404`.

## 23. Documentation
Document the compound-auth requirement explicitly in the OpenAPI description — this is not a standard Bearer-only endpoint.

## 24. AI Coding Agent Implementation Steps

**Task 01 — Design & Implement Parent Gate Session Marker**
Objective: define how B-03's success is carried forward (signed claim vs. Redis flag) and implement `require_verified_parent_gate`. Files to Create/Modify: `core/deps.py`. Dependencies: B-03 must define the marker-setting side first (coordinate).

**Task 02 — Implement `ChildLockRecoveryService.initiate_recovery()`**
Objective: family-ownership check + scoped token issuance. Files to Create: `recovery_service.py`. Dependencies: Task 01.

**Task 03 — Write "No Bypass Without Fresh Parent Gate" Test**
Objective: the sub-feature's single highest-priority guarantee. Files to Create: `test_recovery_service.py`. Dependencies: Task 02.

**Task 04 — Implement `POST /v1/children/{id}/lock/recover` Router**
Objective: wire dependency chain and response schema. Files to Modify: `api.py`. Files to Create: `recovery_schemas.py`. Dependencies: Task 02.

**Task 05 — Add Full Test Suite & API Docs**
Objective: coverage per §22. Dependencies: Task 04.

## 25. Definition of Done
`POST /v1/children/{id}/lock/recover` is live, structurally unreachable without a fresh Parent Gate verification in the current session, issues a single-use scoped token, and never mutates lock configuration itself.

## 26. Final Verification Checklist
- [x] No code path reaches this endpoint's business logic without `require_verified_parent_gate` passing
- [x] Expired Parent Gate marker is rejected, not silently accepted
- [x] `recovery_token` is scoped to exactly one `child_id` and single-use
- [x] Abandoned recovery leaves `child_lock` completely unchanged
- [x] Cross-family access returns `404`

---

## 27. Implementation Status
- **Status**: **Implemented & Verified**
- **Core Components**:
  - `src/noorheroes/core/deps.py`: `require_verified_parent_gate`, `set_parent_gate_marker`
  - `src/noorheroes/core/exceptions.py`: `ParentGateNotVerifiedError`, `InvalidRecoveryTokenError`
  - `src/noorheroes/core/i18n.py`: Localized translations for `PARENT_GATE_NOT_VERIFIED`, `INVALID_RECOVERY_TOKEN`, `LOCK_RECOVERY_INITIATED`, `LOCK_RECOVERY_SUCCESS` (`en`, `hi`, `ur`, `ar`)
  - `src/noorheroes/modules/access_gate/recovery_schemas.py`: `LockRecoveryResponse`
  - `src/noorheroes/modules/access_gate/events.py`: `ChildLockRecoveryInitiatedEvent`
  - `src/noorheroes/modules/access_gate/recovery_service.py`: `ChildLockRecoveryService` (`initiate_recovery`, `validate_and_consume_recovery_token`)
  - `src/noorheroes/modules/access_gate/lock_service.py`: `ChildLockService.configure_lock` (recovery token consumption)
  - `src/noorheroes/modules/access_gate/api.py`: `POST /v1/children/{id}/lock/recover`
  - `tests/modules/access_gate/test_recovery_service.py`: 9 unit tests
  - `tests/modules/access_gate/test_recovery_api.py`: 8 router & integration tests
  - Full module test suite: 59 passed in `tests/modules/access_gate/`

