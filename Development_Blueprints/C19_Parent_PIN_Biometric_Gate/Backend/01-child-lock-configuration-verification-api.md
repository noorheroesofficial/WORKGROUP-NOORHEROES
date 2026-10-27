# B-01 — Child Lock Configuration & Verification API

> **Status:** ✅ **Implemented & Verified** (Production Ready)  
> **Module Location:** `src/noorheroes/modules/access_gate/`  
> **Test Suites:** `tests/modules/access_gate/test_lock_repository.py` (5 tests), `tests/modules/access_gate/test_lock_service.py` (17 tests), `tests/modules/access_gate/test_lock_api.py` (20 tests) — **42/42 passed (100%)**  
> **Database Migration:** `alembic/versions/0012_update_child_lock_type_check_constraint.py`  
> **Documentation:** `FAST-API-INSTRUCTIONS.md` §5.12, `MASTER-README.md` §11.6, `00_GAP_ANALYSIS_AND_CONFLICT_RESOLUTION_REGISTER.md` Gap 09  

## 1. Feature Context
The per-child lock is the first stage of the canonical four-stage profile-access pipeline (PRD C.19 §1.7 FR-7). Each child can be configured with an independent lock type — none, pattern, PIN, or fingerprint — and this sub-feature owns server-side verification of that lock, including progressive lockout. Biometric ("fingerprint") is an OS-level assertion only; no biometric data ever reaches this API.

## 2. Parent Feature
Feature C.19 — Parent PIN/Biometric Gate & Profile Access Control

## 3. Sub-feature
1.1 Child Lock Configuration & Verification API (ID: **B-01**)

## 4. Objective
Implement `POST /v1/children/{id}/lock/verify`, extending the existing `child_lock` table (introduced in A.1) with `failed_attempts`/`locked_until` columns, so that a locked child's pattern/PIN is verified server-side with salted Argon2id hashing and progressive, exponential-cooldown lockout that is honored even against a correct credential submitted mid-cooldown.

## 5. Business Requirements
- FR-4: every child can have a different lock type (`none|pattern|pin|fingerprint`), fully independent per child.
- FR-5: Pattern/PIN compare against a salted, slow hash; raw gesture points are never logged. Fingerprint is OS-biometric-assertion-only — never stored or transmitted.
- FR-7 (stage 2): "Verify If Locked" — pattern/PIN/biometric with a retry limit; recovery routes through Parent Profile (B-02), never a generic bypass.
- FR-12: failed attempts trigger progressively longer lockout.
- FR-15: offline verification uses the locally cached salted hash (KMP K-02/K-06); this API is the server-authoritative path used when online.
- NFR (Security): Argon2id-class hashing; zero biometric data storage — this platform's single most security-critical guarantee.

## 6. Existing Architecture
Extends A.1's `child_lock` table and reuses the shared Argon2id `credential_hasher.py` introduced for OTP/PIN hashing (A.1 B-02/B-04) rather than re-implementing hashing. Lives in a new `modules/access_gate` module (Child Lock Service, per PRD §3.3) since this is a distinct bounded context from `modules/identity` (parent-level auth) — `modules/identity` is extended for parent PIN (B-03), `modules/access_gate` owns child-lock and session-activation logic.

## 7. Existing Code to Reuse
- `src/noorheroes/common/security/credential_hasher.py` — shared Argon2id hash/verify utility (generalized from A.1 B-04's `otp_hasher.py`)
- `src/noorheroes/modules/identity/models.py::ChildLockOrm` — existing `child_lock` table definition (A.1)
- `core/deps.py::get_current_parent_device_context` — device-scoped bearer auth dependency
- `core/exceptions.py::ValidationError`, `NotFoundError`

## 8. Files to Create
- `src/noorheroes/modules/access_gate/__init__.py`
- `src/noorheroes/modules/access_gate/lock_schemas.py` — `LockVerifyRequest`, `LockVerifyResponse`
- `src/noorheroes/modules/access_gate/lock_repository.py` — `ChildLockRepository`
- `src/noorheroes/modules/access_gate/lock_service.py` — `ChildLockService(BaseService)`
- `src/noorheroes/modules/access_gate/api.py` — router mount point for all C.19 endpoints (shared across B-01–B-04)
- `alembic/versions/xxxx_add_child_lock_lockout_columns.py` — adds `failed_attempts`, `locked_until` to `child_lock` if not already present
- `tests/modules/access_gate/test_lock_service.py`
- `tests/modules/access_gate/test_lock_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/identity/models.py` — confirm/extend `ChildLockOrm` with `failed_attempts` (int, default 0), `locked_until` (nullable timestamptz)
- `src/noorheroes/main.py` (or router registry) — mount `access_gate.api.router` at `/v1/children`

## 10. Backend Requirements
- `ChildLockService.verify(child_id, parent_ctx, lock_type, value)`:
  1. Load `ChildLockOrm` by `child_id`, verify family ownership against `parent_ctx.family_id` → `404` if not found/not owned.
  2. If `locked_until` is in the future, return `verified: false` with `423 LOCKED_RETRY_COOLDOWN` **without evaluating the submitted credential at all** — a correct credential must not be evaluated during an active cooldown.
  3. Compare `value` against `value_hash` using `credential_hasher.verify()`.
  4. On success: reset `failed_attempts` to 0, clear `locked_until`, return `{verified: true}`.
  5. On failure: increment `failed_attempts`; once `failed_attempts` crosses the configured threshold, compute `locked_until = now + exponential_cooldown(failed_attempts)`; return `{verified: false, attempts_remaining, lockout_until}`.
- Fingerprint (`lock_type == "fingerprint"`) verification is an OS-assertion pass-through: the client only calls this endpoint after a successful on-device `BiometricPrompt` result; the server records the attempt outcome for lockout purposes but never receives biometric data.
- Discard the submitted `value` from memory/logs immediately after hashing/comparison.

## 11. API Contract

### `POST /v1/children/{id}/lock/verify`
- **Auth:** Bearer (parent-owned device, pre-child-session-activation context)
- **Authorization:** caller's device/family must own `child_id`
- **Request:** `{ "lock_type": "pattern|pin|fingerprint", "value_hash_or_assertion": "..." }`
- **Response 200:** `{ "verified": true }` or `{ "verified": false, "attempts_remaining": 2, "lockout_until": null }`
- **Error Responses:** `401 UNAUTHORIZED`, `404 CHILD_NOT_FOUND`, `422 INVALID_LOCK_TYPE`, `423 LOCKED_RETRY_COOLDOWN`, `500 INTERNAL_ERROR`

## 12. Database Requirements
`child_lock` (extends A.1): `child_id` PK/FK, `lock_type` CHECK IN `('none','pattern','pin','fingerprint')`, `value_hash`, `failed_attempts` INT DEFAULT 0, `locked_until` TIMESTAMPTZ NULL, `updated_at`. No new table — additive migration only.

## 13. Validation
- `lock_type` must match one of the four enum values → `422 INVALID_LOCK_TYPE` otherwise.
- `value_hash_or_assertion` required and non-empty for `pattern`/`pin`; may be an assertion token for `fingerprint`.
- Reject verify calls against a child with `lock_type == "none"` — such a child should never reach this endpoint (client routes directly past lock).

## 14. Authentication
Bearer token representing the requesting parent/device context (pre-session, i.e., before a child-mode session token exists — this endpoint is one of the few reachable without an active child session, since it is what produces one).

## 15. Authorization
Family-ownership check: `child_id` must belong to the same `family_id` as the authenticated device/parent context. No cross-family access under any condition.

## 16. Error Handling
| Scenario | Response |
|---|---|
| Wrong credential | `200 {verified: false, attempts_remaining}` |
| Correct credential during active lockout | `423 LOCKED_RETRY_COOLDOWN` (credential not evaluated) |
| Unknown `child_id` or not owned by caller's family | `404 CHILD_NOT_FOUND` |
| Invalid `lock_type` | `422 INVALID_LOCK_TYPE` |
| Database failure | `500 INTERNAL_ERROR`, logged with correlation ID, no PII in log |

## 17. Offline First
This endpoint is the **server-authoritative** path. KMP (K-02/K-06) implements a client-side cached-hash fallback for offline use; when connectivity is available, this endpoint is always the source of truth and the client must reconcile any offline-verified state against it on reconnect where applicable to lockout counters.

## 18. Analytics
Emits no client-facing analytics directly; success/failure outcomes feed `lock_verification_succeeded`/`lock_verification_failed`/`lock_lockout_triggered` events raised client-side (KMP K-02) upon receiving this API's response.

## 19. Performance
Verification must resolve in a single indexed lookup (`child_id` PK) plus one Argon2id comparison — target p95 < 150ms server-side (client target overall is < 200ms per PRD NFR, inclusive of network).

## 20. Security
- Argon2id salted hashing, no plaintext PIN/pattern ever logged or stored.
- Lockout is honored unconditionally during cooldown, even against a correct credential — this is a CI-blocking test (see §26 Task 04).
- Fingerprint path never receives or persists biometric data — structurally enforced by never adding a biometric-data field to the request schema.

## 21. Library Requirements
FastAPI, SQLAlchemy 2.0 (async), Pydantic v2, `argon2-cffi` (via existing `credential_hasher.py`), pytest, pytest-asyncio.

## 22. Testing
- Unit: correct credential succeeds and resets `failed_attempts`.
- Unit: incorrect credential increments `failed_attempts` and eventually sets `locked_until`.
- Unit: **correct credential submitted while `locked_until` is in the future is still rejected** (highest-priority test, PRD §5 item 1).
- Unit: `lock_type` enum validation.
- Integration: cross-family `child_id` access → `404`.
- Integration: full lockout-then-cooldown-expiry-then-retry flow.

## 23. Documentation
Update OpenAPI schema with request/response examples for all three lock types and both success/failure/lockout response shapes.

## 24. AI Coding Agent Implementation Steps

**Task 01 — Extend `child_lock` Schema**
Objective: add `failed_attempts`/`locked_until` columns if not already present. Files to Create: migration. Files to Modify: `ChildLockOrm`. Definition of Done: migration applies cleanly against A.1's existing table.

**Task 02 — Implement `ChildLockRepository`**
Objective: family-scoped lookup, atomic increment/reset of lockout counters. Files to Create: `lock_repository.py`. Dependencies: Task 01.

**Task 03 — Implement `ChildLockService.verify()`**
Objective: full lockout-aware verification logic per §10. Files to Create: `lock_service.py`. Dependencies: Task 02.

**Task 04 — Write Lockout-Honored-During-Cooldown Test**
Objective: the single highest-priority guarantee in this sub-feature. Files to Create: `test_lock_service.py`. Dependencies: Task 03.

**Task 05 — Implement `POST /v1/children/{id}/lock/verify` Router**
Objective: wire request/response schemas, error mapping. Files to Create/Modify: `api.py`, `lock_schemas.py`. Dependencies: Task 03.

**Task 06 — Add Full Test Suite & API Docs**
Objective: coverage per §22, OpenAPI examples per §23. Dependencies: Task 05.

## 25. Definition of Done
`POST /v1/children/{id}/lock/verify` is live, family-ownership-scoped, honors progressive lockout unconditionally (including against correct credentials mid-cooldown), never logs raw credential values, and is covered by the full test suite in §22.

## 26. Final Verification Checklist
- [ ] Correct credential during active lockout is rejected
- [ ] `failed_attempts` resets to 0 on success
- [ ] Cross-family `child_id` access returns `404`, not `403` (no existence leak)
- [ ] No raw PIN/pattern value appears in logs
- [ ] Biometric path never receives biometric data in the request schema
- [ ] OpenAPI docs updated with all response variants
