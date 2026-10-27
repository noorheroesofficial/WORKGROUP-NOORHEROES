# B-05 — Child Lock Configuration API

## 1. Feature Context
Each child can have an independent app lock (none/pattern/PIN/biometric toggle). This sub-feature owns the **setting** of that lock value; C.19 B-01 already owns its **verification** on the same `child_lock` table (PRD C.23 FR-9, FR-10 — "this document owns the setting of these values, C.19 owns their verification").

## 2. Parent Feature
Feature C.23 — Parental Controls (Screen Time, Bedtime, AI Permissions, Content Age Level)

## 3. Sub-feature
1.5 Child Lock Configuration API (ID: **B-05**)

## 4. Objective
Implement `GET/PATCH /v1/children/{id}/lock`, hashing any submitted raw pattern/PIN value server-side immediately using the existing shared Argon2id hasher, never storing or logging plaintext, and never persisting the raw value beyond the single hashing operation.

## 5. Business Requirements
- FR-9: configure per-child app lock (PIN/pattern/biometric toggle); view/revoke handled separately by B-06.
- FR-10: only salted hashes/OS biometric assertions are stored; raw patterns and PINs are never logged.
- Consistent with C.19's storage rule — this document restates the configuration-side guarantee C.19 already established for verification.

## 6. Existing Architecture
Extends `modules/access_gate` (established by C.19 B-01, which owns the same `child_lock` table for verification). Reuses `common/security/credential_hasher.py` (Argon2id) exactly as C.19 B-01 does — **do not implement a second hashing utility**.

## 7. Existing Code to Reuse
- `src/noorheroes/common/security/credential_hasher.py` — shared Argon2id hash/verify utility (from C.19 B-01/A.1 B-04)
- `src/noorheroes/modules/access_gate/lock_repository.py::ChildLockRepository` — extend with a `set_lock()` method rather than creating a parallel repository
- `src/noorheroes/modules/identity/models.py::ChildLockOrm` (referenced by C.19 B-01) — the shared `child_lock` table
- `core/deps.py::get_current_parent`, `require_elevated_session`

## 8. Files to Create
- `src/noorheroes/modules/access_gate/lock_config_schemas.py` — `LockConfigResponse`, `LockConfigUpdateRequest`
- `src/noorheroes/modules/access_gate/lock_config_service.py` — `ChildLockConfigService(BaseService)` (distinct service class from C.19's verification service, same repository/table)
- `tests/modules/access_gate/test_lock_config_service.py`
- `tests/modules/access_gate/test_lock_config_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/access_gate/lock_repository.py` — add `set_lock(child_id, lock_type, value_hash)` and `get_lock_config(child_id)` methods alongside the existing verification-focused methods from C.19 B-01
- `src/noorheroes/modules/access_gate/api.py` — add `GET/PATCH /v1/children/{id}/lock` to the shared router (already mounted by C.19 B-01)

## 10. Backend Requirements
- `ChildLockConfigService.get_config(child_id, parent_ctx)`: verify family ownership → return `{ lock_type, configured: bool }` (never the hash itself).
- `ChildLockConfigService.set_lock(child_id, parent_ctx, payload)`:
  1. Require fresh step-up (`require_elevated_session`) — consistent with C.19/C.21's identical requirement, no weaker mechanism introduced here.
  2. Verify family ownership.
  3. Validate `lock_type in ('none', 'pattern', 'pin', 'fingerprint')`.
  4. If `lock_type == 'none'`: clear `value_hash`, set `lock_type = 'none'`.
  5. If `lock_type in ('pattern', 'pin')`: hash `value` immediately via `credential_hasher.hash()`, persist only `value_hash`; discard the raw `value` from memory/logs immediately after hashing — never log the request body's raw field.
  6. If `lock_type == 'fingerprint'`: no server-side value to store (OS-assertion-only, consistent with C.19 B-01's fingerprint handling) — just set `lock_type = 'fingerprint'`, clear any prior `value_hash`.
  7. Reset `failed_attempts` and `locked_until` to their defaults on any lock-type change (a fresh configuration should not inherit a prior lockout state).
  8. Emit `ChildLockTypeSet` outbox event.

## 11. API Contract

### `GET /v1/children/{id}/lock`
- **Auth:** Bearer (parent)
- **Response 200:** `{ "lock_type": "pattern", "configured": true }`
- **Error Responses:** `401 UNAUTHORIZED`, `403 FORBIDDEN`, `404 CHILD_NOT_FOUND`

### `PATCH /v1/children/{id}/lock`
- **Auth:** Bearer (parent) + step-up (fresh Parent Gate pass)
- **Request:** `{ "lock_type": "pattern", "value": "..." }` (raw value; hashed server-side immediately, never stored/logged in plaintext)
- **Response 200:** `{ "lock_type": "pattern", "configured": true }`
- **Error Responses:** `401 UNAUTHORIZED`, `403 FORBIDDEN`, `404 CHILD_NOT_FOUND`, `422 INVALID_LOCK_TYPE`

## 12. Database Requirements
Reuses `child_lock` (owned/established by C.19 B-01): `child_id PK/FK`, `lock_type CHECK IN ('none','pattern','pin','fingerprint')`, `value_hash`, `failed_attempts`, `locked_until`, `updated_at`. No new table, no new migration required unless columns are missing (confirm against C.19 B-01's migration before assuming completeness).

## 13. Validation
- `lock_type`: must match one of the four enum values.
- `value`: required and non-empty for `pattern`/`pin`; ignored/absent for `none`/`fingerprint`.
- Reject requests where `value` is present but `lock_type` doesn't require it (defensive validation against accidental raw-value logging).

## 14. Authentication
`Depends(get_current_parent)` for GET; PATCH additionally requires `Depends(require_elevated_session)`.

## 15. Authorization
Family-ownership check: `child_id` must belong to `parent_ctx.family_id`.

## 16. Error Handling
| Scenario | Response |
|---|---|
| Invalid `lock_type` | 422 INVALID_LOCK_TYPE |
| Missing step-up on PATCH | 403 FORBIDDEN |
| Child not found/not owned | 404 CHILD_NOT_FOUND |
| `value` missing when required by `lock_type` | 422 VALIDATION_ERROR |

## 17. Offline First
N/A — configuration write requires connectivity; offline verification (using the previously synced hash) is owned by KMP's local secure cache (C.19 K-06), not this API.

## 18. Local Data
N/A (backend).

## 19. Localization
N/A — lock type is an enum value, not display text.

## 20. RTL
N/A.

## 21. Analytics
Backing source for `child_lock_type_set`.

## 22. Performance
Low-volume, parent-initiated only. Single PK-indexed upsert.

## 23. Security
This endpoint's defining guarantee: raw pattern/PIN values exist in memory only for the duration of the hashing call and are never persisted or logged. Code review must explicitly verify no logging middleware captures the raw request body for this route (check `StructuredLoggingMiddleware` exclusions/redaction rules).

## 24. Library Requirements
Reuses existing Argon2id hasher; no new dependencies.

## 25. Testing
- Unit: raw `value` is never present in any persisted row or log output (inspect actual hash output, not the plaintext).
- Unit: `lock_type = 'none'` clears any existing hash.
- Unit: `lock_type = 'fingerprint'` stores no value hash.
- Unit: lock-type change resets `failed_attempts`/`locked_until`.
- Unit: PATCH rejected without fresh step-up.
- Integration: set lock → verify via C.19 B-01's verification endpoint succeeds with the newly configured value (cross-feature integration test).

## 26. Documentation
OpenAPI description must state explicitly that raw values are hashed immediately and never logged, and must cross-reference C.19 B-01 as the verification-side companion.

## 27. AI Coding Agent Implementation Steps

**Task 01 — Confirm `child_lock` Table Completeness**
- Objective: Verify the table already has all needed columns from C.19 B-01's migration before assuming no new migration is needed.
- Why This Is Required: Avoid a duplicate/conflicting migration.

**Task 02 — Extend `ChildLockRepository` with Configuration Methods**
- Files to Modify: `src/noorheroes/modules/access_gate/lock_repository.py`
- Implementation Details: Add `set_lock()`, `get_lock_config()` alongside existing verification methods — same class, same table, additive only.

**Task 03 — Create Configuration Schemas**
- Files to Create: `src/noorheroes/modules/access_gate/lock_config_schemas.py`

**Task 04 — Implement `ChildLockConfigService`**
- Files to Create: `src/noorheroes/modules/access_gate/lock_config_service.py`
- Implementation Details: Per §10; reuse `credential_hasher.py` exactly as C.19 B-01 does.
- Dependencies: Task 02, Task 03.

**Task 05 — Add Endpoints to Existing `access_gate` Router**
- Files to Modify: `src/noorheroes/modules/access_gate/api.py`
- Implementation Details: Add to the router already mounted by C.19 B-01 — do not create a second router/mount point for the same table.

**Task 06 — Add Step-Up Enforcement**
- Dependencies: Task 05.

**Task 07 — Add Raw-Value Non-Persistence/Non-Logging Test**
- Files to Create: `tests/modules/access_gate/test_lock_config_service.py`
- Implementation Details: Assert no log line or DB row contains the raw submitted value.

**Task 08 — Add Cross-Feature Integration Test with C.19 B-01**
- Objective: Set a lock here, verify it succeeds via C.19's verification endpoint.
- Files to Create: `tests/modules/access_gate/test_lock_config_api.py`

**Task 09 — Add API Documentation**
- Objective: Cross-reference C.19 B-01 explicitly.

**Task 10 — Final Code Review**
- Objective: Confirm `StructuredLoggingMiddleware` does not capture raw request bodies for this route; confirm no duplicate `child_lock`-adjacent table was created.

## 28. Definition of Done
- Lock configuration set/get works correctly for all four lock types.
- Raw value never persisted or logged (verified by test and code review).
- Cross-feature integration with C.19 B-01 verification confirmed.

## 29. Final Verification Checklist
- [ ] No duplicate `child_lock` table or router created
- [ ] Raw value hashed immediately, discarded from memory, never logged
- [ ] Lock-type change resets lockout state
- [ ] Step-up required on PATCH
- [ ] Cross-feature test with C.19 B-01 verification passes
- [ ] OpenAPI documents the configuration/verification split with C.19
