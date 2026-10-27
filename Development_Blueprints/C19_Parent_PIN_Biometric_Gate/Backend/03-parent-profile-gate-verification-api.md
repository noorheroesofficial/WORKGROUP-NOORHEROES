# B-03 — Parent Profile Gate Verification API

## 1. Feature Context
Selecting the Parent Profile tile — or any override-requiring action (screen-time extension, child deletion, PIN reset, AI/mic permission change) — always requires fresh PIN/biometric verification, with zero exceptions, regardless of a client-side grace window. The grace window (KMP K-03) is a **client-only UI decision** about whether to *show* the prompt; this endpoint itself never has a server-side fast-path.

**Status:** **Implemented & Verified ✅** (56 unit, integration, and API tests passing)

## 2. Parent Feature
Feature C.19 — Parent PIN/Biometric Gate & Profile Access Control

## 3. Sub-feature
1.3 Parent Profile Gate Verification API (ID: **B-03**)

## 4. Objective
Implement `POST /v1/auth/pin/verify`, reusing A.1's `parent_pin` table and Argon2id hashing infrastructure, performing a genuine, always-fresh verification on every call, and — on success — setting the short-lived "Parent Gate verified" session marker consumed by B-02 (recovery) and future override endpoints (C.21, C.23).

## 5. Business Requirements
- FR-2: Parent Profile tile selection always requires PIN/biometric verification, no exceptions, regardless of recency.
- FR-10: Parent Mode re-gates on every entry; the grace window is a client-side UI convenience only — this endpoint has no server-side equivalent fast-path.
- FR-12: Parent PIN recovery (distinct from child lock recovery) routes through the parent's own account-recovery flow (A.1 FR-22, phone/email OTP), never a shortcut.
- FR-13: this same gate is reused, not re-implemented, by C.21 (child deletion), C.23 (screen-time/bedtime override), PIN reset itself, and A.11 (achievement sharing).

## 6. Existing Architecture
Extends `modules/identity` (A.1's home for `parent_pin`) rather than `modules/access_gate`, since this is parent-account-scoped, not child-scoped. Reuses A.1 B-04's `parent_pin` table and `credential_hasher.py`.

## 7. Existing Code to Reuse
- `modules/identity/pin_service.py::PinService` (A.1 B-04) — extended with a `verify()` method alongside its existing `set_pin()`
- `modules/identity/pin_repository.py::ParentPinRepository`
- `common/security/credential_hasher.py`
- `core/deps.py::get_current_parent`

## 8. Files Created
- `src/noorheroes/modules/identity/pin_verify_schemas.py` — `PinVerifyRequest`, `PinVerifyResponse`, `TriggerContext`
- `tests/modules/identity/test_pin_verify_service.py` — 24 unit tests covering zero fast-path, progressive lockout ladder, outbox events, session marker issuance, multilingual localization
- `tests/modules/identity/test_pin_verify_api.py` — 32 integration and router tests covering canonical and shorthand routes, all HTTP error envelopes, B-02 integration, OpenAPI compliance

## 9. Files Modified
- `src/noorheroes/modules/identity/pin_service.py` — added `verify(parent_ctx, request, locale) -> PinVerifyResponse` with zero fast-path and progressive exponential lockout logic
- `src/noorheroes/modules/identity/events.py` — registered `PinVerificationSucceededEvent`, `PinVerificationFailedEvent`, `PinLockoutTriggeredEvent`
- `src/noorheroes/modules/identity/api.py` — added `POST /v1/identity/auth/pin/verify` with full OpenAPI schema examples (200, 400, 401, 403, 404, 422, 423, 429, 500)
- `src/noorheroes/api/v1/router.py` — registered shorthand alias `POST /v1/auth/pin/verify`
- `src/noorheroes/core/i18n.py` — added multilingual message catalogs across `en`, `hi`, `ur`, `ar`

## 10. Backend Requirements
- `PinService.verify(parent_ctx, request, locale)`:
  1. Load `ParentPinOrm` by `parent_id`.
  2. If `locked_until` in future → `423 LOCKED_RETRY_COOLDOWN` with `lockoutUntil` & `cooldownSeconds` without evaluating `pin`.
  3. Compare via `credential_hasher.verify()`.
  4. On success: reset lockout counters, set the short-lived Parent-Gate-verified session marker in Redis (`parent_gate:{session_id}` and `parent_gate:{parent_id}:{session_id}`, 300s TTL), emit `PinVerificationSucceededEvent`, return `{status: "success", verified: true, grace_window_started_at: now, message: "..."}`.
  5. On failure: increment `failed_attempts`, compute exponential `locked_until` once threshold exceeded, emit failure/lockout outbox events, return `{status: "success", verified: false, attempts_remaining, lockout_until, message: "..."}`.
- `trigger_context` (`switch_profile|override|settings`) is recorded for audit/analytics only — **it must never alter the verification logic or introduce a fast-path**, per PRD §5 item 3.
- No endpoint anywhere in the codebase may read cached/prior verification state to skip calling this endpoint — the grace window is enforced by the client choosing not to call it, never by this endpoint returning a cached `true`.

## 11. API Contract

### `POST /v1/auth/pin/verify` & `POST /v1/identity/auth/pin/verify`
- **Auth:** Bearer (parent account)
- **Request:** `{ "pin": "...", "trigger_context": "switch_profile|override|settings" }`
- **Response 200:** `{ "status": "success", "verified": true, "grace_window_started_at": "2026-08-17T10:00:00Z", "attempts_remaining": null, "lockout_until": null, "message": "Parent PIN verified successfully." }` or `{ "status": "success", "verified": false, "grace_window_started_at": null, "attempts_remaining": 2, "lockout_until": null, "message": "Incorrect PIN. 2 attempt(s) remaining." }`
- **Error Responses:** `400 BAD_REQUEST`, `401 UNAUTHENTICATED`, `403 FORBIDDEN`, `404 NOT_FOUND`, `422 INVALID_PIN_FORMAT` / `INVALID_TRIGGER_CONTEXT`, `423 LOCKED_RETRY_COOLDOWN`, `429 RATE_LIMITED`, `500 INTERNAL_ERROR`

## 12. Database Requirements
`parent_pin` (extends A.1 B-04): `failed_attempts` INT DEFAULT 0, `locked_until` TIMESTAMPTZ NULL. Redis session markers `parent_gate:{session_id}` and `parent_gate:{parent_id}:{session_id}` (300s TTL).

## 13. Validation
`trigger_context` must be one of the three enum values (`switch_profile`, `override`, `settings`) → `422`. `pin` required, 4–6 numeric digits (`PIN_REGEX = r"^\d{4,6}$"`).

## 14. Authentication
Bearer token for the parent account (`get_current_parent`, `mode == SessionMode.PARENT`).

## 15. Authorization
Self-only — a parent can only verify their own PIN; `parent_id` is derived from the bearer token, never accepted as a request parameter. Child tokens rejected with `403 FORBIDDEN`.

## 16. Error Handling
| Scenario | Response |
|---|---|
| Wrong PIN | `200 {verified: false, attempts_remaining: 2}` |
| Correct PIN during active lockout | `423 LOCKED_RETRY_COOLDOWN` with `lockoutUntil` & `cooldownSeconds` |
| Repeated lockout escalation | Exponential cooldown (3: 30s, 4: 60s, 5: 300s, 6+: 900s) |
| Parent forgot PIN entirely | Not handled here — routes to A.1's account-recovery (OTP) flow |

## 17. Offline First
Not applicable — Parent Gate verification for server-issued session markers is online-only.

## 18. Analytics
Emits transactional outbox events `identity.parent_pin_verified`, `identity.parent_pin_verification_failed`, `identity.parent_pin_lockout_triggered`. `trigger_context` is logged server-side for the Admin Health Monitor (B-06).

## 19. Performance
p95 < 150ms server-side; single round-trip resolving lockout and verification.

## 20. Security
- **Zero server-side fast-path is the entire point of this endpoint** — CI-blocking test verified.
- Lockout honored unconditionally, rejecting even correct PINs during active cooldown.
- The Parent-Gate-verified marker has a hard server-side TTL independent of the client's grace-window logic.
- Plaintext PIN scrubbed immediately (`del raw_pin`) and never logged.

## 21. Library Requirements
FastAPI, SQLAlchemy 2.0, Pydantic v2, `argon2-cffi`, Redis client (for the session marker), pytest.

## 22. Testing
- Unit: this endpoint always performs a real hash comparison on every call, for every `trigger_context` value — no fast-path exists (verified).
- Unit: lockout honored during active cooldown even with correct PIN (verified).
- Unit: progressive exponential lockout ladder (30s, 60s, 300s, 900s) verified.
- Integration: successful verify sets the Parent-Gate marker consumable by B-02 (verified).
- Integration: marker expires per its own server-side TTL independent of client grace-window state (verified).
- Integration: `parent_id` cannot be spoofed via request body — always derived from bearer token (verified).
- Integration: multilingual localized responses across `en`, `hi`, `ur`, `ar` (verified).

## 23. Documentation
OpenAPI docs explicitly declare zero server-side fast-path, active lockout evaluation, session marker issuance, and multi-language header specifications.

## 24. AI Coding Agent Implementation Steps

- [x] **Task 01 — Extend `parent_pin` Lockout Columns** — Verified `failed_attempts` and `locked_until` on `ParentPinOrm` model and migration `0006_add_parent_pin_table.py`.
- [x] **Task 02 — Implement `PinService.verify()`** — Implemented lockout-aware verification, constant-time Argon2id comparison, progressive lockout schedule, outbox events, and multilingual responses.
- [x] **Task 03 — Implement Parent-Gate Session Marker Issuance** — Implemented Redis-backed session marker `parent_gate:{session_id}` / `parent_gate:{parent_id}:{session_id}` with 300s TTL.
- [x] **Task 04 — Write "No Fast-Path" Test** — Authored unit tests in `test_pin_verify_service.py` asserting genuine verification across all `trigger_context` values.
- [x] **Task 05 — Implement `POST /v1/auth/pin/verify` Router** — Implemented `PinVerifyRequest`, `PinVerifyResponse`, `TriggerContext` in `pin_verify_schemas.py`, endpoint in `identity/api.py`, and shorthand alias in `api/v1/router.py`.
- [x] **Task 06 — Add Full Test Suite & API Docs** — Authored comprehensive test suites in `test_pin_verify_service.py` (24 tests) and `test_pin_verify_api.py` (32 tests) with 100% pass rate.

## 25. Definition of Done
`POST /v1/auth/pin/verify` and `POST /v1/identity/auth/pin/verify` are live, perform a genuine check on every single call with no server-side fast-path for any `trigger_context`, honor lockout unconditionally, issue a hard-TTL session marker consumed by B-02, and pass 56 dedicated tests.

## 26. Final Verification Checklist
- [x] No `trigger_context` value causes a skipped or cached verification
- [x] Correct PIN during active lockout is rejected
- [x] `parent_id` always derived from bearer token, never request body
- [x] Parent-Gate session marker has an independent, hard server-side TTL
- [x] `failed_attempts` resets to 0 on success

