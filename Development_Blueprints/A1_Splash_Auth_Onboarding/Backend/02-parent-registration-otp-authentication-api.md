# B-02 — Parent Registration & OTP Authentication API

> [!NOTE]
> **Status: Implemented & Verified**
> - **Module**: `src/noorheroes/modules/identity/`
> - **Models**: `AuthIdentifierOrm`, `OtpAttemptOrm`, `DeviceSessionOrm` in `src/noorheroes/modules/identity/otp_models.py`
> - **Database Migration**: `alembic/versions/0005_add_auth_identifier_and_otp_attempt.py`
> - **Domain Service**: `OtpAuthService` in `src/noorheroes/modules/identity/otp_service.py`
> - **Provider Gateway & Adapters**: `OtpProviderGateway`, `TwilioSmsProvider`, `SecondarySmsProvider`, `EmailOtpProvider`, `SandboxOtpProvider` in `src/noorheroes/infrastructure/otp/`
> - **Security & Cryptography**: `src/noorheroes/common/security/otp_hasher.py` (Argon2id code hashing, HMAC-SHA256 blind indexing, E.164 normalization, privacy masking)
> - **API Endpoints**: `POST /v1/identity/auth/register`, `POST /v1/identity/auth/otp/request`, `POST /v1/identity/auth/otp/verify`, `POST /v1/identity/auth/recovery/start` (with legacy PRD shorthands `/v1/auth/*`)
> - **Test Coverage**: `tests/modules/identity/test_otp_service.py` (16 passed), `tests/modules/identity/test_otp_api.py` (10 passed) — 100% passing across all 898 repository tests.

## 1. Feature Context
The core identity-establishment path for NoorHeroes: a parent registers with phone or email, receives a 6-digit OTP, and verifies it to obtain a session. No guest mode, no skip-login path exists anywhere in the app — this is the mandatory gate before any content. Must be enumeration-safe, abuse-resistant (OTP bombing/SMS pumping), and never leak whether an identifier is already registered before OTP success.

## 2. Parent Feature
Feature A.1 — Splash, Language Selection, Authentication & Onboarding

## 3. Sub-feature
1.2 Parent Registration & OTP Authentication API (ID: **B-02**)

## 4. Objective
Extend the existing `identity` module with phone/email registration (consent captured atomically), OTP request/verify with server-authoritative cooldowns and lockout, and enumeration-safe account recovery — all built on the existing `IdentityService`/`IdentityRouter` pattern.

## 5. Business Requirements
- FR-5: Registration requires explicit, separable consent checkboxes (3 required + 3 optional); submit blocked server-side too if required consents missing (`422 CONSENT_REQUIRED_MISSING`).
- FR-6: Phone OTP, Email OTP, or Google Login only — Apple Login explicitly not supported.
- FR-7: OTP is 6 digits, supports paste/auto-submit client-side; server enforces authoritative resend countdown.
- FR-8: Repeated OTP failure triggers progressive cooldown and risk-review flagging — never indefinite retry.
- FR-9: Never reveal via timing or content whether an identifier is already registered before OTP success.
- FR-10: New users → consent-already-captured → PIN setup → Add Child. Returning users → Profile Picker.
- FR-22: "Forgot access" routes through OTP re-verification — never a PIN-bypass shortcut.
- Edge Case: OTP SMS arriving after a second code was requested — both codes valid within their own TTL; server tracks multiple active codes per session.
- Edge Case: Device clock skew — OTP TTL validated with server time only.
- NFR: OTP delivery success ≥ 98%; OTP verification success on first attempt ≥ 85%; drop-off at OTP step ≤ 15%.

## 6. Existing Architecture
Existing `IdentityRouter`/`IdentityService` already implement `POST /v1/identity/auth/register` and `POST /v1/identity/auth/login/json` for email/password. This sub-feature **extends** that same router/service (does not replace it) with OTP semantics, following the identical layered pattern: Router → Service → Repository → Postgres, `BaseService`, `BaseRepository`, `OutboxWriter`, `RateLimitMiddleware`.

## 7. Existing Code to Reuse
- `modules/identity/api.py::IdentityRouter`
- `modules/identity/service.py::IdentityService` (extend, do not fork)
- `modules/identity/repository.py::UserRepository` (`get_by_email()` pattern — mirror for phone)
- `core/security.py::create_access_token`, `JwtClaims`
- `infrastructure/redis.py::get_redis_pool`
- `infrastructure/middleware/rate_limit.py`
- `common/outbox.py::OutboxWriter`
- `core/exceptions.py` (`ValidationError`, `RateLimitExceededError`, `AuthenticationError`)

## 8. Files to Create
- `src/noorheroes/modules/identity/otp_models.py` — `AuthIdentifierOrm`, `OtpAttemptOrm`, `DeviceSessionOrm`
- `alembic/versions/xxxx_add_auth_identifier_otp_device_session.py`
- `src/noorheroes/modules/identity/otp_schemas.py` — `RegisterRequest`, `OtpRequestRequest`, `OtpVerifyRequest`, `TokenResponse` (extend existing if present, else new)
- `src/noorheroes/modules/identity/otp_repository.py` — `AuthIdentifierRepository`, `OtpAttemptRepository`
- `src/noorheroes/modules/identity/otp_service.py` — `OtpAuthService(BaseService)`
- `src/noorheroes/infrastructure/otp/otp_provider_gateway.py` — `OtpProviderGateway` (primary/secondary SMS + email abstraction)
- `src/noorheroes/infrastructure/otp/providers/` — `TwilioSmsProvider`, `SecondarySmsProvider`, `EmailOtpProvider` (interface + stub/sandbox impl)
- `src/noorheroes/common/security/otp_hasher.py` — 6-digit code hashing (Argon2id, same primitive family as PIN)
- `tests/modules/identity/test_otp_service.py`
- `tests/modules/identity/test_otp_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/identity/api.py` — add `POST /v1/identity/auth/otp/request`, `POST /v1/identity/auth/otp/verify`, `POST /v1/identity/auth/recovery/start`
- `src/noorheroes/modules/identity/service.py::register_user()` — extend request schema to accept `identifier_type/identifier/consent/locale/device_id` (do not break existing email/password callers — add as a new method `register_via_identifier()` rather than mutating the existing signature)
- `src/noorheroes/core/settings.py` — add OTP provider config keys (names only, no secret values)

## 10. Backend Requirements
- `OtpAuthService.register(payload)`: normalize phone to E.164; check for existing identifier via hash lookup only (never plaintext); always return the same `registration_token`/`otp_channel`/`otp_ttl_seconds` shape and near-identical latency whether or not the identifier exists (pad artificially if needed to defeat timing attacks); reject only if required consents are false.
- `OtpAuthService.request_otp(registration_token, channel)`: generate 6-digit code, hash it (Argon2id), store `OtpAttemptOrm` with `expires_at` (5 min TTL, server clock), enforce escalating resend cooldown (60s→120s→300s) tracked in Redis per session; call `OtpProviderGateway.send()`, on primary failure automatically retry secondary provider within 5s, on total failure return `503 OTP_PROVIDER_UNAVAILABLE` (client offers fallback channel).
- `OtpAuthService.verify_otp(otp_id, code)`: compare against hash, server-time TTL check, max 5 attempts then lock with escalating cooldown; on success mint access(15min)/refresh(30day rotating) tokens bound to `device_id`, determine `is_new_family`/`next_step`.
- Multiple concurrently valid OTP codes per session must both work within their own TTL (do not invalidate the earlier code when a resend is requested).
- Risk scoring hook: call a synchronous, non-blocking risk-score function on register/otp-request (VOIP/disposable number flag, velocity) — score persisted for B-08's Risk Queue; does not block send unless score exceeds a hard threshold.

## 11. API Contract

### `POST /v1/identity/auth/register`
- Auth: none. Request: `{identifier_type, identifier, consent:{terms_version, privacy_version, child_data_version, personalization, voice, marketing}, locale, device_id}`. Response 200: `{registration_token, otp_channel, otp_ttl_seconds}`. Errors: `400 INVALID_IDENTIFIER`, `422 CONSENT_REQUIRED_MISSING`, `429 RATE_LIMITED`. Rate limit: 5/hr/identifier, 20/hr/device, 100/hr/IP.

### `POST /v1/identity/auth/otp/request`
- Auth: `registration_token`. Request: `{registration_token, channel}`. Response 200: `{otp_id, expires_at, resend_available_at}`. Errors: `429 OTP_PROVIDER_RATE_LIMITED`, `503 OTP_PROVIDER_UNAVAILABLE`.

### `POST /v1/identity/auth/otp/verify`
- Auth: `otp_id` + code. Request: `{otp_id, code}`. Response 200 (new): `{access_token, refresh_token, is_new_family: true, next_step: "pin_setup"}`. Response 200 (returning): `{access_token, refresh_token, is_new_family: false, next_step: "profile_picker"}`. Errors: `400 INVALID_CODE`, `410 OTP_EXPIRED`, `423 LOCKED_TOO_MANY_ATTEMPTS`.

### `POST /v1/identity/auth/recovery/start`
- Auth: none. Request: `{identifier_type, identifier}`. Response 200: identical shape to `/register`, enumeration-safe, routes into OTP flow.

## 12. Database Requirements
New tables per §4.1/§4.2 ER diagram in the PRD:
- `auth_identifier`: UNIQUE(`identifier_type`,`identifier_value_hash`); index on hash only (never index plaintext); `identifier_value_masked` for display.
- `otp_attempt`: FK `parent_id`; `code_hash`, `expires_at`, `attempt_count`, `verified`; index `(parent_id, created_at DESC)`; purge job after 30 days.
- `device_session`: FK `parent_id`; UNIQUE(`device_id`,`parent_id`); `refresh_token_hash` indexed; purge revoked/expired after 90 days.

## 13. Validation
- Phone normalized to E.164 server-side before hashing/storage.
- Consent: all three required flags must be `true` or reject with `422`.
- OTP code: exactly 6 numeric digits.
- Reject unexpected extra fields (Pydantic strict).

## 14. Authentication
- `/register`, `/otp/request`, `/otp/verify`, `/recovery/start` are pre-auth by design. `/otp/verify` success is what *creates* the session — must mint tokens inside the same request.

## 15. Authorization
- N/A pre-auth. Post-verify, downstream endpoints (PIN, children) require the newly issued Bearer token via existing `get_current_parent`.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| Identifier already registered (pre-verify) | Identical response to a new identifier — no signal |
| OTP provider outage | Auto-retry secondary within 5s; if both fail, `503` + client fallback-channel offer |
| Invalid/expired OTP | `400`/`410`, inline field error, other digits preserved client-side |
| 6th consecutive OTP attempt | `423 LOCKED_TOO_MANY_ATTEMPTS`, escalating cooldown logged for risk review |
| VOIP/disposable number | Allowed, flagged for elevated risk scoring, not auto-blocked |
| Device clock skew | Irrelevant — server time is sole source of truth for TTL |

## 17. Security
- OTP codes hashed at rest (Argon2id), never logged in plaintext.
- Enumeration-safety verified via identical response shape/timing on `/register` and `/recovery/start`.
- HMAC request signing on `/otp/*` endpoints to deter scripted abuse (per PRD §12.3).
- WAF rules tuned for OTP-bombing patterns (ops config, note in README).
- All failed attempts logged with device/IP (IP hashed after 30 days) for the internal Risk Service — never exposed to the client.
- Refresh tokens bound to `device_id`, rotated on every use.

## 18. Analytics
Emit via `OutboxWriter`: `registration_started`, `registration_submitted`, `otp_requested`, `otp_resend_requested`, `otp_verification_attempted`, `otp_verification_succeeded`, `otp_verification_failed`, `otp_lockout_triggered`, `otp_fallback_channel_offered`, `account_recovery_started`.

## 19. Performance
- Registration/OTP-request/verify are on the critical onboarding path — target consistent with bootstrap's p95 budget; OTP send request p95 < 1.5s.
- Resend-cooldown state in Redis (not Postgres) to keep the hot path fast.

## 20. Library Requirements
- `argon2-cffi` (reuse existing PIN-hashing dependency for OTP code hashing too).
- SMS/email provider SDKs behind the `OtpProviderGateway` interface — reference env var names only, never hardcode secrets.
- `phonenumbers` (Google libphonenumber Python port) for E.164 normalization.

## 21. Testing
- Unit: enumeration-safety (response shape/timing), lockout escalation (exactly at 6th attempt), multi-active-code TTL handling, E.164 normalization edge cases.
- Integration: simulated OTP-bombing pattern load test; primary-provider-outage → secondary-failover; DOB-irrelevant here but confirm server-time-only TTL under simulated clock skew.

## 22. Documentation
Module README documents required OTP/Google provider env var names (never values) per PRD backend AI-prompt requirement.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Create `auth_identifier`, `otp_attempt`, `device_session` Models & Migration**
Objective: Add the three new tables. Why: no existing schema supports OTP/multi-identifier auth. Follow: existing SQLAlchemy/Alembic conventions in `modules/identity/models.py`. Reuse: `Base`, `TimestampMixin`. Create: `otp_models.py`, migration file. Business Rules: unique hash-only index on `auth_identifier`; never index plaintext identifier. Security: no plaintext identifier column at all — hash + masked-display only. Tests: migration up/down smoke test. **Resolved architecture decision:** `FAST-API-INSTRUCTIONS.md` §5.1 documents the existing `identity` context as having only `User.email` + password login (`UserRepository.get_by_email()`), with no phone field and no existing multi-identifier table — so `auth_identifier` cannot be superseding anything that exists today. Decision: `auth_identifier` is additive and **complements** `User`/`FamilyAccount` permanently, not a transitional step toward replacing `User.email`. The existing email/password login path (`POST /v1/identity/auth/login/json`) is left completely untouched by this sub-feature; a `User` row gains a linked `auth_identifier` row only when that parent registers or logs in via phone/email-OTP/Google. Do Not Change: existing `User`/`FamilyAccount` tables or the existing password-login endpoint. Definition of Done: migration clean on fresh DB and staging dry-run; existing password-login integration test suite passes unmodified.

**Task 02 — Implement `OtpProviderGateway` & Provider Adapters**
Objective: Abstract SMS/email sending with primary/secondary failover. Why: FR requires 5s failover and never showing raw provider errors to the user. Follow: `infrastructure/` service pattern (mirrors `R2StorageService` abstraction style). Create: gateway + provider adapter files. Implementation: `send(channel, identifier, code) -> DeliveryResult`; try primary, on exception/timeout within budget, try secondary; env-flag-gated fixed test code (`000000`) accepted only in non-prod, hard-disabled in prod build config. Security: never log raw codes or raw provider error text. Tests: mock provider failure/failover unit tests. Definition of Done: failover path covered by test, prod-flag-disable verified.

**Task 03 — Implement OTP/Identifier Hashing Utility**
Objective: `otp_hasher.py` for Argon2id hashing of both identifiers (lookup hash) and OTP codes. Why: never store plaintext. Reuse: same Argon2id parameters as existing PIN hashing for consistency, benchmarked for latency. Tests: hash/verify round-trip, timing consistency. Definition of Done: benchmarked parameters documented.

**Task 04 — Implement `AuthIdentifierRepository` & `OtpAttemptRepository`**
Objective: Data access for identifier lookup-by-hash and OTP attempt tracking. Follow: `BaseRepository` pattern. Implementation: `get_by_identifier_hash()`, `create_otp_attempt()`, `increment_attempt_count()`, `mark_verified()`. Tests: unit tests per method. Definition of Done: repository methods covered.

**Task 05 — Implement `OtpAuthService.register()`**
Objective: Enumeration-safe registration + consent capture. Follow: `BaseService`, delegates consent write to B-05's `ConsentLedgerService` (call its method, do not duplicate consent-write logic here). Business Rules: identical response/latency regardless of identifier existence; reject only on missing required consent. Security: constant-time-equivalent response construction (pad latency if the existing-identifier branch is naturally faster). Tests: enumeration-safety test (timing + shape assertions). Dependencies: Task 01, 04, and B-05's service. Definition of Done: enumeration-safety test passes.

**Task 06 — Implement `OtpAuthService.request_otp()` and `.verify_otp()`**
Objective: Core OTP lifecycle. Follow: escalating Redis-tracked cooldown, Argon2id-hashed code storage, server-time TTL, 5-attempt lockout. Business Rules: multiple concurrently valid codes per session both work within their own TTL. Security: log failed attempts with device/IP (IP hashed after 30 days) for Risk Service only. Tests: lockout-at-exactly-6th-attempt, multi-code validity, server-time-only TTL. Dependencies: Tasks 02, 03, 04. Definition of Done: all listed test cases pass.

**Task 07 — Wire Token Issuance on Verify Success**
Objective: Mint access(15min)/refresh(30day rotating) tokens bound to `device_id` on successful verify, determine `is_new_family`/`next_step`. Reuse: `core/security.py::create_access_token`, existing `JwtClaims`. Business Rules: returning users → `profile_picker`; new users → `pin_setup` (consent already captured at registration). Tests: both branches. Definition of Done: token shape matches existing `TokenResponse` contract.

**Task 08 — Add Router Endpoints**
Objective: Wire `/otp/request`, `/otp/verify`, `/recovery/start` into `IdentityRouter`; extend `/register`. Follow: existing `openapi_extra` security-declaration pattern; no DB access in router. Tests: covered by Task 10. Definition of Done: all four endpoints live and documented.

**Task 09 — Add Rate Limiting & Risk Scoring Hook**
Objective: Apply per-identifier/device/IP limits; call synchronous risk-score function (stub acceptable if a full risk model isn't in scope — persist a `risk_score`/`risk_flags` column on `otp_attempt` or a lightweight `risk_flag` table for B-08 to consume). Tests: rate-limit breach returns 429; risk flag persisted for VOIP-flagged numbers. Definition of Done: risk data visible to B-08's queue query.

**Task 10 — Add Unit & Integration Tests**
Objective: Full coverage per §21. Files: `test_otp_service.py`, `test_otp_api.py`. Definition of Done: all cases green in CI, including simulated OTP-bombing load test.

**Task 11 — Update OpenAPI Documentation**
Objective: Regenerate and diff-classify. Definition of Done: non-breaking diff confirmed.

**Task 12 — Final Code Review**
Objective: Verify enumeration-safety end-to-end, no plaintext logging anywhere in the OTP path, layering rules respected. Definition of Done: checklist in §24 fully checked.

## 24. Final Verification Checklist
- [x] Enumeration-safety verified on `/register` and `/recovery/start` (shape + timing)
- [x] OTP codes hashed at rest, never logged in plaintext
- [x] Server-time-only TTL validation (clock-skew-proof)
- [x] Lockout triggers exactly at 6th attempt with escalating cooldown
- [x] Multiple concurrently valid OTP codes per session supported
- [x] Primary→secondary SMS provider failover within 5s tested
- [x] Non-prod fixed test code hard-disabled in production build config
- [x] Refresh tokens bound to `device_id`, rotated on use
- [x] Rate limits enforced (5/hr identifier, 20/hr device, 100/hr IP)
- [x] All analytics events in §18 emitted via `OutboxWriter`
- [x] No plaintext identifier column exists anywhere in the schema
- [x] No PostgreSQL/Redis credentials modified


## 25. Definition of Done
Phone/email registration, OTP request/verify, and enumeration-safe recovery are live on the existing `identity` module, fully abuse-resistant, fully tested, and produce the exact token/next-step contract K-03 (KMP Registration/OTP flow) depends on.
