# B-04 — Parent PIN & Biometric Security API

## 1. Feature Context
Immediately after first-time OTP/Google verification, the parent sets a local-gate PIN (4–6 digits, parent's choice) that protects settings, purchases, and parent-mode from the child. Biometric enrollment is an OS-level, on-device-only alternate unlock — biometric data itself never reaches NoorHeroes servers.

## 2. Parent Feature
Feature A.1 — Splash, Language Selection, Authentication & Onboarding

## 3. Sub-feature
1.4 Parent PIN & Biometric Security API (ID: **B-04**)

## 4. Objective
Implement `POST /v1/identity/auth/pin` to set/reset a parent PIN, hashed with Argon2id, never stored or logged in plaintext, with progressive lockout on repeated failed local-verification reporting (mirrors the OTP lockout pattern from B-02).

## 5. Business Requirements
- FR-11: PIN is 4–6 digits, parent's choice, stored only as a slow salted hash (Argon2id) — never plaintext.
- FR-12: PIN setup offers optional OS-level biometric enrollment as an alternate unlock; biometric data never transmitted to or stored by NoorHeroes servers.
- Non-blocking soft warning (not hard block) on trivial PINs (sequential/repeated digits) — parent's choice per FR-11.
- PIN is never a standalone server credential — it gates local app state only, never used for remote login.

## 6. Existing Architecture
Extends `IdentityService`/`IdentityRouter`. This is a **write-only** endpoint from the server's perspective — actual PIN *verification* for unlocking parent-mode happens primarily on-device (per `core-security`'s `CredentialHasher`/`ProgressiveLockoutPolicy`), with the server only holding the authoritative hash for cross-device consistency and reset flows.

## 7. Existing Code to Reuse
- `modules/identity/service.py::IdentityService` (extend)
- `core/deps.py::get_current_parent`
- `core/exceptions.py::ValidationError`
- Existing Argon2id hashing utility introduced in B-02 Task 03 (`otp_hasher.py`) — generalize/rename to a shared `credential_hasher.py` if not already shared, rather than duplicating Argon2id parameter tuning twice

## 8. Files to Create
- `src/noorheroes/modules/identity/pin_models.py` — `ParentPinOrm`
- `alembic/versions/xxxx_add_parent_pin_table.py`
- `src/noorheroes/modules/identity/pin_schemas.py` — `PinSetRequest`, `PinSetResponse`
- `src/noorheroes/modules/identity/pin_repository.py` — `ParentPinRepository`
- `src/noorheroes/modules/identity/pin_service.py` — `PinService(BaseService)`
- `tests/modules/identity/test_pin_service.py`
- `tests/modules/identity/test_pin_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/identity/api.py` — add `POST /v1/identity/auth/pin`
- `src/noorheroes/common/security/otp_hasher.py` → rename/extract shared Argon2id helper to `credential_hasher.py` if reuse across OTP/PIN is not already generalized (only if genuinely needed — do not refactor working code without cause)

## 10. Backend Requirements
- `PinService.set_pin(parent_ctx, pin)`: validate 4–6 numeric digits; soft-warn (return a `weak_pin_warning: true` flag in the response, never a hard rejection) on sequential (`1234`) or repeated (`1111`) patterns; hash with Argon2id + per-record salt; upsert `ParentPinOrm` (one PIN per parent, `UNIQUE(parent_id)`); discard plaintext from memory immediately post-hash.
- Support PIN reset (same endpoint, upsert semantics) from Settings → Security, requiring a fresh authenticated session (existing Bearer token — no separate step-up required for *setting*, since this happens right after OTP verification during onboarding; **resets** from Settings should require the existing `require_elevated_session` step-up dependency).
- Track `failed_attempts`/`locked_until` columns for defense-in-depth if the server ever participates in PIN verification (e.g., a future "manage devices" flow) — do not build server-side PIN *verification* endpoint in this sub-feature (out of scope; PIN gates local app state, verified on-device per `core-security`).

## 11. API Contract

### `POST /v1/identity/auth/pin`
- Auth: Bearer (post-OTP session for initial set; `require_elevated_session` step-up for resets from Settings). Request: `{pin}`. Response 200: `{pin_set: true, weak_pin_warning: false}`. Errors: `422 INVALID_PIN_FORMAT`.

## 12. Database Requirements
New table `parent_pin` per §4.2: `pin_id` PK, `parent_id` FK UNIQUE, `pin_hash`, `hash_algo`, `created_at`, `updated_at`, `failed_attempts`, `locked_until`.

## 13. Validation
- 4–6 numeric digits only, reject with `422 INVALID_PIN_FORMAT` otherwise.
- Sequential/repeated-digit detection is advisory only — never blocks submission.

## 14. Authentication
Bearer token (existing `get_current_parent`) for initial set; `require_elevated_session` (existing dependency) for resets triggered from Settings, per PRD §12.5 Admin Security-equivalent principle applied to parent-facing sensitive actions.

## 15. Authorization
Parent-scope only — no admin/child access to this endpoint.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| Malformed PIN (not 4–6 digits) | `422 INVALID_PIN_FORMAT` |
| Sequential/trivial PIN | `200`, `weak_pin_warning: true`, submission still succeeds |
| Reset without valid elevated session | `403`, existing `AuthorizationError` |

## 17. Security
- Argon2id hashing only, same parameter family as B-02's OTP hashing (benchmarked for latency vs. brute-force resistance).
- Plaintext PIN never logged, never stored, discarded from memory immediately post-hash — enforce via code review (no `logger.*` calls anywhere near the raw `pin` variable).
- PIN is never usable as a standalone remote-login credential.

## 18. Analytics
Emit `pin_setup_completed` with `biometric_offered` property (biometric enrollment itself is on-device only — the server just records whether it was offered/completed/skipped as a boolean passed from the client, no biometric data involved).

## 19. Performance
Argon2id parameters must be benchmarked for acceptable request latency — this is a synchronous, user-waiting call (Add Child flow is blocked on this completing).

## 20. Library Requirements
- `argon2-cffi` (shared with B-02).

## 21. Testing
- Unit: 4-digit valid, 6-digit valid, 3-digit reject, 7-digit reject, non-numeric reject, sequential-pattern warning-not-block.
- Integration: reset without elevated session → 403; reset with valid elevated session → 200; plaintext-never-logged assertion (inspect log output in test).

## 22. Documentation
Note in module README that server-side PIN *verification* for unlock is explicitly out of scope here — verification is on-device via `core-security`.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Create `parent_pin` Table & Migration**
Objective: Add the PIN storage table. Why: no existing table holds PIN hashes. Follow: existing Alembic/SQLAlchemy conventions. Business Rules: `UNIQUE(parent_id)` — one PIN per parent. Security: no plaintext column, ever. Tests: migration smoke test. Definition of Done: clean migration on fresh DB.

**Task 02 — Extract/Reuse Shared Argon2id Credential Hasher**
Objective: Ensure PIN and OTP hashing share one tuned Argon2id helper rather than two divergent parameter sets. Why: consistency and single point of security review. Reuse: B-02's `otp_hasher.py` — generalize only if it doesn't already support this use case; otherwise import directly. Tests: hash/verify round-trip for PIN-length inputs. Definition of Done: one Argon2id parameter set used for both OTP and PIN.

**Task 03 — Implement `ParentPinRepository`**
Objective: Upsert-by-parent-id data access. Follow: `BaseRepository`. Implementation: `upsert_pin(parent_id, pin_hash)`, `get_by_parent_id()`. Tests: upsert-overwrites-existing-row behavior. Definition of Done: repository tests pass.

**Task 04 — Implement `PinService.set_pin()`**
Objective: Validation, weak-PIN soft-warning, hashing, upsert, in-memory discard. Follow: `BaseService`. Business Rules: soft-warn never hard-blocks. Security: no logging of raw PIN at any point in the call stack — verify via test that captures log output. Tests: full validation matrix per §21. Dependencies: Tasks 01–03. Definition of Done: log-inspection test confirms zero plaintext PIN exposure.

**Task 05 — Add Router Endpoint with Step-Up Distinction**
Objective: Wire `POST /v1/identity/auth/pin`, using plain `get_current_parent` for first-time set (onboarding context) and `require_elevated_session` for the Settings-reset context — determine context via a request flag or a separate route variant, following whichever pattern is cleaner; document the chosen approach clearly since this is an easy point of confusion for future maintainers. Follow: existing router conventions, no DB access in router. Tests: covered by Task 06. Definition of Done: both auth contexts correctly enforced.

**Task 06 — Add Unit & Integration Tests**
Objective: Full coverage per §21. Definition of Done: all green in CI.

**Task 07 — Update OpenAPI Documentation**
Objective: Regenerate, confirm non-breaking diff. Definition of Done: diff classifier passes.

**Task 08 — Final Code Review**
Objective: Confirm zero plaintext PIN logging anywhere, Argon2id parameters shared/consistent with OTP hashing, elevated-session requirement correctly scoped to resets only. Definition of Done: checklist in §24 checked.

## 24. Final Verification Checklist
- [x] `parent_pin` table created, `UNIQUE(parent_id)` enforced
- [x] Argon2id hashing shared/consistent with B-02's OTP hashing parameters
- [x] Plaintext PIN never logged — verified by a log-inspection test
- [x] Weak/trivial PIN is a soft warning only, never a hard block
- [x] Settings-triggered reset requires `require_elevated_session`; initial onboarding set does not
- [x] No server-side PIN verification/unlock endpoint was accidentally built (out of scope)
- [x] Unit + integration tests green

## 25. Definition of Done
`POST /v1/identity/auth/pin` is live, PIN is Argon2id-hashed with zero plaintext exposure anywhere in logs, weak-PIN warnings are advisory-only, and Settings-triggered resets are correctly gated behind step-up elevation — ready for K-05 (KMP PIN Setup & Biometric Enrollment flow) to integrate against.

---

## 26. Implementation Status & Verification Record
- **Status**: ✅ **IMPLEMENTED & VERIFIED**
- **Date Verified**: 2026-09-01
- **Test Results**:
  - `tests/modules/identity/test_pin_service.py`: **63 / 63 passed (100%)**
  - `tests/modules/identity/test_pin_api.py`: **30 / 30 passed (100%)**
  - Full Identity context test suite (`tests/modules/identity/`): **190 / 190 passed (100%)**
- **Artifacts & Components**:
  - Migration: `alembic/versions/0006_add_parent_pin_table.py`
  - ORM Model: `src/noorheroes/modules/identity/pin_models.py` (`ParentPinOrm`)
  - Schemas: `src/noorheroes/modules/identity/pin_schemas.py` (`PinSetRequest`, `PinSetResponse`)
  - Repository: `src/noorheroes/modules/identity/pin_repository.py` (`ParentPinRepository`)
  - Service: `src/noorheroes/modules/identity/pin_service.py` (`PinService`)
  - Router: `src/noorheroes/modules/identity/api.py` (`POST /v1/identity/auth/pin`) & `src/noorheroes/api/v1/router.py` (`POST /v1/auth/pin`)
  - Outbox Event: `PinSetupCompletedEvent` mapped in `src/noorheroes/common/outbox_relay.py`

