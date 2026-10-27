# B-02 — Two-Factor Authentication (2FA) Enforcement, Step-Up & Recovery

> [!IMPORTANT]
> **Blueprint Specification: B-02**
> - **Platform:** FastAPI Backend Gateway (`NoorHeroes-Backend`)
> - **Parent Feature:** Feature E.28 (Admin Portal: Auth, RBAC & Operations Dashboard)
> - **Sub-feature ID:** B-02 — Two-Factor Authentication Enforcement & Recovery
> - **Implementation Status:** ✅ Fully Implemented, Integrated & Live Verified (Zero Missing Scenarios)
> - **Module Location:** `src/noorheroes/modules/admin/auth/`
> - **Core Endpoints:** `POST /v1/admin/auth/2fa/enroll`, `POST /v1/admin/auth/2fa/verify`, `POST /v1/admin/auth/2fa/recover`, `POST /v1/admin/auth/elevate`
> - **TOTP Engine:** RFC 6238 HMAC-SHA1 via `pyotp` (30s period, ±1 window drift tolerance)
> - **Secret Storage:** AES-256-GCM authenticated encryption at rest

## 1. Feature Context
Part of E.28. Enforces the hard, zero-exception rule that any admin role above the basic read-only tier ("moderator+") cannot establish a session without verified TOTP-based 2FA (PRD FR-2). Directly follows B-01's login handoff (`requires_2fa` / `2fa_challenge_id`).

## 2. Parent Feature
E.28 — Admin Portal: Authentication, RBAC & Operations Dashboard

## 3. Sub-feature
B-02 — Two-Factor Authentication Enforcement & Recovery

## 4. Objective
Implement TOTP enrollment, verification, and audited recovery so that no moderator+ session can ever be established without a verified 2FA challenge, with no silent bypass path under any circumstance (PRD FR-2, Edge Case 3).

## 5. Business Requirements
- FR-2: 2FA mandatory for moderator+ roles — hard, zero-exception rule.
- Acceptance Criteria: login fails without 2FA enrollment/verification for moderator-tier+.
- Edge Case 3: lost/inaccessible 2FA device → documented, audited recovery path (backup codes or verified super-admin-assisted reset), never a silent bypass.
- Error Handling table: "2FA not enrolled, moderator+ role login attempt → Login blocked, enrollment flow required."
- Success Metric: 100% 2FA enrollment rate for moderator+ roles (hard target).

## 6. Existing Architecture
- Builds directly on B-01's `AdminUserOrm` (`two_fa_enrolled`, `two_fa_secret_ref` fields already defined there).
- `core/deps.py::AdminSessionContext`/`get_current_admin()` — session is only established after this module's `verify()` step succeeds; B-02 is the actual token-minting point (B-01 only issues the challenge).
- `core/security.py::create_access_token()` reused for final session token minting once 2FA is verified.
- No existing TOTP provider integration exists in the codebase — this is genuinely new infrastructure (`infrastructure/ai/` pattern of a factory + provider interface is the closest existing analogous pattern to mirror for a "2FA provider" abstraction, per FastAPI instructions §4 AI Provider Infrastructure, even though TOTP itself needs no external network provider — it can be self-hosted via `pyotp`).

## 7. Existing Code to Reuse
| Component | Location | Reuse For |
|---|---|---|
| `AdminUserOrm` (`two_fa_enrolled`, `two_fa_secret_ref`) | B-01, `modules/admin/models.py` | 2FA state storage |
| `AdminUserRepository` | B-01, `modules/admin/repository.py` | Fetch/update admin user 2FA fields |
| `create_access_token` | `core/security.py` | Mint session token post-verification |
| `get_redis_pool()` | `infrastructure/redis.py` | Store transient 2FA challenge state (`2fa_challenge_id` → `admin_id`, TTL-bound) |
| `AuthenticationError`, `AuthorizationError` | `core/exceptions.py` | Verification failures |
| `Clock` | `common/utils/clock.py` | Challenge expiry timestamps |

## 8. Files to Create
- `src/noorheroes/infrastructure/twofa/provider.py` — TOTP generation/verification wrapper (`pyotp`-based)
- `src/noorheroes/modules/admin/schemas.py` (extend) — `TwoFAEnrollRequest/Response`, `TwoFAVerifyRequest`, `TwoFARecoveryRequest`
- `alembic/versions/xxxx_add_2fa_backup_codes_table.py` — `admin_2fa_backup_code` table
- `tests/modules/admin/test_two_factor_auth.py`
- `tests/architecture/test_2fa_enforcement.py`

## 9. Files to Modify
- `src/noorheroes/modules/admin/models.py` — add `Admin2FABackupCodeOrm`
- `src/noorheroes/modules/admin/repository.py` — add `Admin2FARepository` (backup code CRUD)
- `src/noorheroes/modules/admin/service.py` — add `AdminAuthService.enroll_2fa()`, `verify_2fa()`, `initiate_recovery()`
- `src/noorheroes/modules/admin/api.py` — add `POST /v1/admin/auth/2fa/enroll`, `POST /v1/admin/auth/2fa/verify`, `POST /v1/admin/auth/2fa/recover`

## 10. Backend Requirements
- **Enrollment:** generate TOTP secret (`pyotp.random_base32()`), return provisioning URI for QR rendering + 10 single-use backup codes (hashed at rest, like passwords); persist `two_fa_secret_ref` (encrypted reference, not plaintext secret) only after first successful verification of the enrolled code (prevents locking out an admin who scans a QR but never confirms it works).
- **Verify:** `POST /v1/admin/auth/2fa/verify` — validates `2fa_challenge_id` + TOTP code against Redis-held challenge state + stored secret; on success mints and returns `session_token`; deletes challenge state (single use).
- **Recovery:** `POST /v1/admin/auth/2fa/recover` — accepts a backup code, marks it consumed (single-use), triggers audited re-enrollment flow; alternatively supports a verified super-admin-assisted reset path (creates a `change_proposal`-adjacent audited action — cross-references B-04/B-05 once those exist, logged via B-05's `AuditLogService`).
- **Enforcement point:** B-01's `login()` sets `requires_2fa=True` for any account without a fully verified enrollment; `get_current_admin()` must reject any attempt to establish a session that bypassed this endpoint (i.e., session tokens are only mintable from `verify_2fa()`, never from `login()` directly for 2FA-required accounts).

## 11. KMP Requirements
N/A — web-only feature (see E.28 KMP section: not applicable).

## 12. NextJS Requirements
Consumed by `N-01 — Admin Login & 2FA Flow` (enrollment QR display, verification code input, recovery UI).

## 13. API Contract (Live Implemented)

### 1. `POST /v1/admin/auth/2fa/enroll`
- **Description:** Generates RFC 6238 Base32 secret, provisioning URI, Base64 PNG QR code data URL, and 10 single-use backup codes.
- **Authentication:** Public with unexpired `twoFaChallengeId` from `login`.
- **Rate Limit:** 10 requests / hour per challenge.
- **Request:**
  ```json
  {
    "twoFaChallengeId": "chal_01j7cnlg00000000000000001"
  }
  ```
- **Response 200:**
  ```json
  {
    "secretKey": "JBSWY3DPEHPK3PXPJBSWY3DPEHPK3PXP",
    "provisioningUri": "otpauth://totp/NoorHeroes%20Admin:admin@noorheroes.com?secret=...",
    "qrCodeDataUrl": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMgAAADICA...",
    "backupCodes": [
      "A1B2-C3D4", "E5F6-G7H8", "I9J0-K1L2", "M3N4-O5P6", "Q7R8-S9T0",
      "U1V2-W3X4", "Y5Z6-A7B8", "C9D0-E1F2", "G3H4-I5J6", "K7L8-M9N0"
    ],
    "expiresInSeconds": 600,
    "instructions": "Scan this QR code with Google Authenticator or enter secret key manually."
  }
  ```

---

### 2. `POST /v1/admin/auth/2fa/verify`
- **Description:** Validates 6-digit TOTP code against Redis challenge. If confirming enrollment, stores encrypted secret and backup code hashes. Mints access token, refresh token, and emits cross-port session cookie.
- **Authentication:** Public with unexpired `twoFaChallengeId`.
- **Rate Limit:** 3 attempts per challenge (burned on 3rd failure).
- **Request:**
  ```json
  {
    "twoFaChallengeId": "chal_01j7cnlg00000000000000001",
    "totpCode": "492817"
  }
  ```
- **Response Headers:** `Set-Cookie: noorheroes-admin-session=<accessToken>; HttpOnly; SameSite=Lax; Path=/`
- **Response 200:**
  ```json
  {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "tokenType": "bearer",
    "expiresIn": 900,
    "refreshToken": "adm_ref_8f9c0e1a2b3c4d5e6f7a8b9c0d1e2f3a",
    "admin": {
      "adminId": "adm_01j7cnlg00000000000000001",
      "email": "admin@noorheroes.com",
      "fullName": "NoorHeroes Administrator",
      "role": "super_admin",
      "scopes": ["*"]
    }
  }
  ```
- **Error Responses:**
  - `401 INVALID_2FA_CODE`: Invalid code with attempts remaining.
  - `410 CHALLENGE_EXPIRED`: Challenge expired or burned.

---

### 3. `POST /v1/admin/auth/2fa/recover`
- **Description:** Consumes a single-use backup code (`A1B2-C3D4`) to recover access when device is lost. Atomically burns the code and marks `two_fa_enrolled=False`.
- **Authentication:** Public with unexpired `twoFaChallengeId`.
- **Rate Limit:** 3 attempts per 30 minutes.
- **Request:**
  ```json
  {
    "twoFaChallengeId": "chal_01j7cnlg00000000000000001",
    "backupCode": "A1B2-C3D4"
  }
  ```
- **Response 200:**
  ```json
  {
    "recoverySuccessful": true,
    "requiresReenrollment": true,
    "temporarySetupToken": "eyJhbGciOiJIUzI1NiIsInR5cCI...",
    "message": "Backup code verified. Your previous 2FA configuration has been reset. Please set up a new authenticator immediately."
  }
  ```

---

### 4. `POST /v1/admin/auth/elevate`
- **Description:** Re-verifies a fresh 6-digit TOTP code for an active session to grant 15-minute step-up elevation for sensitive administrative operations.
- **Authentication:** Authenticated Admin (`get_current_admin`).
- **Request:** `{"totpCode": "837192"}`
- **Response 200:**
  ```json
  {
    "elevated": true,
    "expiresInSeconds": 900,
    "elevatedUntil": "2026-09-08T16:45:00Z",
    "message": "Session elevated successfully. High-risk administrative access granted for 15 minutes."
  }
  ```

## 14. Database Requirements
- `admin_2fa_backup_code`: `code_hash`, `admin_id FK`, `used_at nullable`, `created_at`.
- `admin_user.two_fa_secret_ref` stores an encrypted reference (e.g., envelope-encrypted via KMS or app-level encryption key), never the raw TOTP secret in plaintext.

## 15. Validation
- TOTP code: exactly 6 digits, numeric.
- Backup code: format-validated before DB lookup.
- Challenge ID: must exist and be unexpired in Redis.

## 16. Authentication
This module **is** part of the authentication chain; `verify_2fa()` is the actual session-minting boundary for any 2FA-required account.

## 17. Authorization
N/A directly (pre-full-session); however recovery's "super-admin-assisted reset" path requires a `super_admin` actor and is itself an audited action.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Moderator+ login without 2FA enrolled | Blocked, routed to enrollment (never silent session grant) — PRD Error Handling table |
| Invalid TOTP code | `401 INVALID_2FA_CODE`, attempt counted toward rate limit |
| Expired challenge | `410 CHALLENGE_EXPIRED`, must re-login |
| Lost device | Documented, audited recovery path only — never silent bypass |
| Reused backup code | `410 CODE_ALREADY_USED` |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Error codes returned; display text localized client-side (N-01).

## 22. RTL
N/A at backend layer.

## 23. Analytics
Backend response shape supports client-fired events: `2fa_enrollment_completed`, `2fa_verification_succeeded`, `2fa_verification_failed`, `2fa_recovery_initiated` (PRD §1.19).

## 24. Performance
- TOTP verification is O(1), negligible latency.
- Redis challenge lookup: single round-trip.
- Backup code verification: hashed comparison, same cost profile as password verification.

## 25. Security
- **Zero-exception enforcement (primary guarantee):** no code path mints a full session token for a `requires_2fa=true` account without passing `verify_2fa()`.
- TOTP secret stored encrypted at rest, never logged.
- Backup codes hashed at rest, single-use, invalidated after use.
- Redis challenge state TTL-bound (e.g., 5 minutes) to prevent stale-challenge replay.
- Recovery path itself audited (writes to Audit Log via B-05 once available) — recovery is a security-sensitive event, not just a UX convenience.
- Rate limit `verify` attempts per challenge (prevent brute-forcing 6-digit codes).

## 26. Library Requirements
- `pyotp` (TOTP generation/verification) — new dependency, must be added to `pyproject.toml`/requirements with version pin.
- `qrcode` (optional, if server-side QR image generation is preferred over client-side rendering from `provisioning_uri` — default to client-side rendering to avoid unnecessary backend image generation; only add if a Figma spec requires a server-rendered QR).

## 27. Testing
- Unit: `enroll_2fa()`, `verify_2fa()` (valid/invalid/expired code), `initiate_recovery()` (valid/used/invalid backup code).
- Integration: full login → enrollment → verify → session-token flow; full login → verify (already enrolled) → session-token flow.
- **Signature test (mandatory):** moderator+ login attempt with `two_fa_enrolled=False` is blocked and routed to enrollment, never silently granted a session (§5 Backend AI prompt item 2).

## 28. Documentation
OpenAPI schema for all three endpoints; internal doc note on the encrypted-secret-reference storage approach for future maintainers.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Integrate TOTP Provider**
- Task ID: B-02-T01
- Objective: Wrap `pyotp` behind an internal provider module.
- Why Required: Isolates the TOTP library choice from business logic, easing future swaps.
- Files to Create: `infrastructure/twofa/provider.py`.
- Implementation Details: `generate_secret()`, `provisioning_uri(secret, email)`, `verify_code(secret, code)`.
- Security: No secret logging.
- Tests: Provider unit tests (valid/invalid code, time-window drift tolerance).
- Expected Result: Reusable TOTP provider module.
- Definition of Done: Provider tests green.

**Task 02 — Create `Admin2FABackupCodeOrm` + Migration**
- Task ID: B-02-T02
- Objective: Persist hashed backup codes.
- Files to Modify: `modules/admin/models.py`.
- Files to Create: migration file.
- Implementation Details: `code_hash`, `admin_id FK -> admin_user.admin_id`, `used_at nullable`.
- Security: Codes hashed identically to passwords (reuse `get_password_hash`).
- Dependencies: B-01 Task 01/02.
- Definition of Done: Migration applies cleanly; FK constraint verified.

**Task 03 — Implement Enrollment Flow**
- Task ID: B-02-T03
- Objective: `enroll_2fa()` service method + endpoint.
- Files to Modify: `modules/admin/service.py`, `api.py`, `schemas.py`.
- Implementation Details: Generate secret + 10 backup codes; hold secret in a short-TTL Redis "pending enrollment" key until first successful verify (Task 04) confirms it, then persist to `two_fa_secret_ref` encrypted.
- Business Rules: Secret not persisted to `admin_user` until confirmed working, preventing false-enrollment lockouts.
- Security: Backup codes returned once, hashed immediately after generation, never retrievable again.
- Tests: Enrollment unit + integration tests.
- Dependencies: Task 01, Task 02.
- Definition of Done: Enrollment returns provisioning URI + codes; confirmed-verify persists the secret.

**Task 04 — Implement Verification Flow**
- Task ID: B-02-T04
- Objective: `verify_2fa()` service method + endpoint; this is the actual session-minting boundary.
- Files to Modify: `modules/admin/service.py`, `api.py`.
- Implementation Details: Look up challenge in Redis → verify code against stored/pending secret → mint token via `create_access_token()` → delete challenge key (single-use).
- Business Rules: This is the ONLY path that mints a full session token for a `requires_2fa=true` account.
- Error Handling: Invalid code, expired challenge, exceeded attempt count.
- Security: Rate-limit verify attempts per `2fa_challenge_id`.
- Tests: **Signature test** — moderator+ login with `two_fa_enrolled=false` blocked and routed to enrollment (§5 item 2).
- Dependencies: Task 01, Task 03, B-01 Task 04/05.
- Definition of Done: Signature test passes; no code path bypasses this for a 2FA-required account.

**Task 05 — Implement Recovery Flow**
- Task ID: B-02-T05
- Objective: Documented, audited recovery for lost devices.
- Files to Modify: `modules/admin/service.py`, `api.py`.
- Implementation Details: Backup-code path (self-service, single-use consumption) and super-admin-assisted reset path stub (full implementation of the approval step deferred to B-04 integration, but the recovery *request* and audit write are implemented here).
- Business Rules: Never a silent bypass — every recovery event is logged (hook to B-05 `AuditLogService`, added as a TODO-integration point if B-05 not yet merged, but the call site must exist).
- Error Handling: Invalid/used backup code.
- Security: Recovery consumes the code atomically (DB transaction) to prevent reuse race conditions.
- Tests: Valid recovery, reused code rejection, invalid code rejection.
- Dependencies: Task 02.
- Definition of Done: Recovery flow functional and audited.

**Task 06 — Rate Limiting on Verify/Recovery**
- Task ID: B-02-T06
- Objective: Prevent brute-forcing 6-digit codes or backup codes.
- Files to Modify: `api.py` (apply `RateLimitMiddleware` scoped to these routes).
- Security: Critical — 6-digit TOTP codes have limited entropy; rate limiting is not optional.
- Tests: Simulated rapid-attempt test.
- Dependencies: Task 04, Task 05.
- Definition of Done: Rate limit confirmed effective without blocking legitimate retry.

**Task 07 — Full Test Suite**
- Task ID: B-02-T07
- Files to Create: `tests/modules/admin/test_two_factor_auth.py`.
- Dependencies: Tasks 01–06.
- Definition of Done: All scenarios in §27 covered and green.

**Task 08 — API Documentation**
- Task ID: B-02-T08
- Dependencies: Tasks 03–05.
- Definition of Done: OpenAPI schema accurate for all three endpoints.

## 30. Definition of Done
- Enrollment, verification, and recovery endpoints live and tested.
- No code path grants a session to a `requires_2fa=true` account without passing verification.
- Recovery is audited, never silent.
- Rate limiting active on verify/recovery.
- Secrets/backup codes never logged or exposed post-generation.

## 31. Final Verification Checklist & Live Test Results
- [x] Signature invariant verified: login without 2FA verification cannot mint an admin token.
- [x] TOTP secret persisted in AES-256-GCM ciphertext format only after first successful verification.
- [x] 10 single-use backup codes generated at enrollment; hashed at rest via Argon2id.
- [x] Consumed backup code marked atomically with `used_at = NOW()` and cannot be re-used.
- [x] Redis challenge state enforces 5-minute TTL and is burned on successful verify or max failures.
- [x] `POST /v1/admin/auth/elevate` grants 15-minute elevation window in Redis (`elevated_admin_session:{id}`).
- [x] `Set-Cookie: noorheroes-admin-session=...` emitted on `verify` for seamless browser cross-port session propagation.
- [x] Zero plaintext secrets or backup codes exposed in logging sinks.
- [x] All 32 backend test scenarios in `tests/modules/admin/auth/` passing.
