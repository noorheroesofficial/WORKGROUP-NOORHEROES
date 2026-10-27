# B-07 — Multi-Dimensional Rate Limiting Configuration

## 1. Feature Context
NoorHeroes must resist credential-stuffing and brute-force attacks that rotate a single identifying dimension (e.g., IP address) to evade a naive single-dimension rate limiter. This blueprint configures the existing Redis-backed sliding-window limiter across all four required dimensions. No school/institutional/madarsa logic applies.

## 2. Parent Feature
F.37 — Security Architecture (Cross-Cutting).

## 3. Sub-feature
B-07 — Multi-Dimensional Rate Limiting Configuration (Backend / FastAPI).

## 4. Objective
Implement rate limiting enforced independently at device, IP, phone, and account dimensions for the canonical auth endpoints, per the documented per-endpoint limits, per PRD FR-15 and §3.4/§3.5.

## 5. Business Requirements
- FR-15: "Rate limiting applies at device, IP, phone, and account levels" — restated as the complete, multi-dimensional requirement, beyond a single IP-based check alone.
- §3.4 canonical rate limits: `register` 5/hour/IP; `login` 10/hour/IP; `refresh` 30/hour/user; `verify-email` 10/hour/IP.
- §3.5: "Rate limiting at four dimensions: device, IP, phone, and account — never a single-dimension check alone, which would be trivially bypassable by rotating just one dimension."
- Negative Test §13.4 (implicit via edge cases): a limiter bypassable by rotating one dimension is explicitly the failure mode this blueprint must prevent.

## 6. Existing Architecture
- `infrastructure/middleware/rate_limit.py` — `RateLimitMiddleware` and `SlidingWindowRateLimiter`, Redis-backed, already exist per `FAST-API-INSTRUCTIONS.md` §4/§15 master reference table row: `RateLimitMiddleware | Infra Middleware | infrastructure/middleware/rate_limit.py | Redis sliding-window rate limit | FastAPI app | app.add_middleware(...)`.
- `core/exceptions.py::RateLimitExceededError` — existing HTTP 429 error type, already attributed to the same author line as `RateLimitMiddleware`, confirming this is an existing, working subsystem this blueprint configures/extends rather than builds from scratch.
- This blueprint's job is primarily **configuration and dimension-completeness**, not a new limiter implementation — confirm the existing `SlidingWindowRateLimiter` already supports multi-key/multi-dimension limiting; if it currently only supports a single key (e.g., IP-only), this becomes an extension task, not merely configuration.

## 7. Existing Code to Reuse
- `infrastructure/middleware/rate_limit.py::RateLimitMiddleware` / `SlidingWindowRateLimiter` — the core mechanism.
- `core/exceptions.py::RateLimitExceededError`.
- B-01's `JwtClaims` for the `account`-dimension key on authenticated endpoints (e.g., `refresh`'s 30/hour/user limit needs `sub`/`family_id` from the decoded token).

## 8. Files to Create
- `tests/infrastructure/test_multidimensional_rate_limiting.py`.
- `tests/infrastructure/test_rate_limit_bypass_resistance.py` (the single-dimension-rotation negative test).

## 9. Files to Modify
- `infrastructure/middleware/rate_limit.py` — extend `SlidingWindowRateLimiter`/`RateLimitMiddleware` to accept and independently enforce multiple dimension keys per request (device, IP, phone, account) if not already supported; apply the canonical per-endpoint limits from §3.4 to `register`, `login`, `refresh`, `verify-email`.
- `identity` context's auth router registrations — ensure each endpoint declares its correct dimension set and limit values.

## 10. Backend Requirements
- Each rate-limited endpoint is checked against **all applicable dimensions independently** — a request is rejected if *any* dimension's limit is breached, not only if *all* are breached (i.e., dimensions are ANDed as independent gates, not OR'd into a single combined check that could be gamed).
- Dimension key sources: `device` (device ID, from request header/body per existing client contract), `IP` (request source IP, respecting any existing proxy/`X-Forwarded-For` handling already in place), `phone` (from the OTP-challenge request body, for `register`/`login`/`verify-email`), `account` (from the authenticated `JwtClaims.sub`, for `refresh`).
- Canonical limits applied exactly as specified: `register` 5/hour/IP, `login` 10/hour/IP, `refresh` 30/hour/user, `verify-email` 10/hour/IP — confirm whether `register`/`login`/`verify-email` also need device/phone-dimension limits beyond the explicitly-stated IP limit (the PRD's per-endpoint table states IP explicitly; FR-15's general four-dimension requirement implies device/phone should also apply where the relevant identifier is available on that endpoint — implement all four dimensions where the endpoint has access to the relevant identifier, don't restrict to only the explicitly-tabulated dimension if others are available and meaningful).

## 11. KMP Requirements
N/A directly — client sends its existing device-ID header (already part of the existing request contract per `core-network`'s `AuthApiService`); no new client behavior required.

## 12. NextJS Requirements
N/A — Admin Portal authentication (E.28) is a separate, MFA-gated flow with its own rate-limiting needs, out of scope for this specific blueprint unless E.28 explicitly delegates its rate-limiting configuration here (confirm, don't assume).

## 13. API Contract
No new endpoint or request/response shape change. This blueprint constrains the internal rate-limiting behavior of the existing `POST /api/v1/auth/register`, `/login`, `/refresh`, `/verify-email` endpoints. Error Response: 429 with `RateLimitExceededError`'s existing error envelope, including a `Retry-After` header/field if the existing error type supports it (extend if not, following the existing envelope pattern).

## 14. Database Requirements
None — rate-limit counters live in Redis (sliding-window keys), not PostgreSQL. No credential changes to either store.

## 15. Validation
- Confirm each dimension's identifier is present and well-formed before applying its limit (e.g., a missing device ID on an endpoint that requires it should not silently skip that dimension's check — decide and document whether a missing identifier fails closed (reject) or is simply not checked for that dimension, and apply consistently).

## 16. Authentication
N/A directly — rate limiting applies to both pre-authentication endpoints (`register`, `login`, `verify-email`) and a post-authentication endpoint (`refresh`, using the account dimension from the validated JWT).

## 17. Authorization
N/A.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Any single dimension's limit breached | 429 `RateLimitExceededError`, request rejected regardless of other dimensions' remaining headroom |
| Redis unavailable for rate-limit counter check | Document and implement a fail-open vs. fail-closed decision explicitly (recommend fail-closed for auth endpoints specifically, given their sensitivity, consistent with B-02's fail-closed precedent for the denylist check) — do not leave this undefined |
| Attempt to bypass by rotating a single dimension (e.g., new IP, same device/phone) | Still blocked by the remaining dimensions' limits |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
429 error message should route through the existing localized error-envelope mechanism.

## 22. RTL
N/A.

## 23. Analytics
No dedicated event listed in PRD §1.19 specifically for rate-limit breaches; if the platform's existing security-monitoring/alerting already consumes `RateLimitExceededError` occurrences (per DevOps §10's "Alert on... " pattern), ensure this multi-dimensional configuration doesn't reduce visibility versus the current single-dimension setup — confirm existing alerting hooks remain intact.

## 24. Performance
Checking four dimensions per request adds up to four Redis round trips (or one multi-key pipelined round trip, preferable) — implement as a single pipelined/batched Redis call where the existing `SlidingWindowRateLimiter` architecture allows, to avoid materially increasing auth-endpoint latency.

## 25. Security
- Multi-dimensional enforcement exists specifically to prevent trivial bypass via single-dimension rotation (§3.5) — the negative test (§27) is the actual proof this holds.
- Ensure dimension identifiers themselves (phone number, device ID) are not logged in plaintext in a way that violates existing PII-handling conventions — reuse the platform's existing redaction pattern (`StructuredLoggingMiddleware`).

## 26. Library Requirements
No new library; extends the existing `SlidingWindowRateLimiter`/Redis infrastructure.

## 27. Testing
- **Unit:** each dimension's limit independently enforced (breach device limit alone → rejected even with IP/phone/account under their limits, and vice versa for each dimension).
- **Mandatory negative test:** simulate an attacker rotating exactly one dimension (e.g., new IP on every request) while holding device/phone/account constant — confirm still blocked once the non-rotated dimensions' limits are reached.
- **Integration:** exercise the actual `register`/`login`/`refresh`/`verify-email` endpoints against their documented canonical limits.
- **Failure-mode:** Redis unavailable — confirm the documented fail-open/fail-closed decision (§18) is what actually happens.

## 28. Documentation
Document the final dimension-to-endpoint matrix (which dimensions apply to which endpoint, with exact limits) as a single reference table, superseding any implicit/scattered configuration; document the Redis-unavailability fail policy explicitly.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm Existing Limiter's Multi-Dimension Capability**
- Task ID: B-07-T01
- Objective: Determine whether `SlidingWindowRateLimiter` already supports independent multi-key limiting or needs extension.
- Why This Is Required: Determines whether this is a configuration task or an extension task — must not assume either way.
- Existing Architecture to Follow: `infrastructure/middleware/rate_limit.py`'s current implementation.
- Existing Files to Reuse: same file (read, not yet modified).
- Files to Create: none yet.
- Files to Modify: none yet.
- Implementation Details: read the current implementation's key-construction logic.
- Business Rules / Validation / Error Handling / Security / Performance: N/A (audit only).
- Localization / RTL / Analytics: N/A.
- Tests: none yet.
- Documentation: audit findings feed Task 02.
- Dependencies: none.
- Do Not Change: nothing yet.
- Expected Result: clear answer on current capability.
- Definition of Done: documented finding.

**Task 02 — Extend/Configure the Limiter for Four Independent Dimensions**
- Task ID: B-07-T02
- Objective: Implement independent per-dimension checking per §10.
- Why This Is Required: Core deliverable.
- Existing Architecture to Follow: existing `SlidingWindowRateLimiter` sliding-window algorithm (reuse the algorithm, extend only the key/dimension handling).
- Existing Files to Reuse: `infrastructure/middleware/rate_limit.py`.
- Files to Create: none (extends existing file) unless the existing file's structure warrants a new `dimensions.py` companion module for key-derivation logic.
- Files to Modify: `infrastructure/middleware/rate_limit.py`.
- Implementation Details: per §10; each dimension checked and enforced independently (AND semantics, not OR).
- Business Rules: apply canonical §3.4 limits; extend to all four dimensions per endpoint where the identifier is available (§10).
- Validation: as in §15.
- Error Handling: as in §18, including the explicit Redis-unavailability decision.
- Security: prevents single-dimension-rotation bypass.
- Performance: pipelined Redis calls per §24.
- Localization / RTL: N/A.
- Analytics: confirm existing alerting hooks preserved (§23).
- Tests: unit tests per §27.
- Documentation: dimension-to-endpoint matrix.
- Dependencies: Task 01.
- Do Not Change: the underlying sliding-window algorithm's correctness (reuse, don't rewrite it).
- Expected Result: all four dimensions independently enforced per endpoint.
- Definition of Done: unit tests pass.

**Task 03 — Wire Canonical Limits to Auth Endpoints & Write the Bypass-Resistance Test**
- Task ID: B-07-T03
- Objective: Apply the exact §3.4 limits to `register`/`login`/`refresh`/`verify-email` and prove bypass-resistance.
- Why This Is Required: Configuration without the endpoint wiring and the negative test doesn't actually deliver the guarantee.
- Existing Architecture to Follow: `identity` context's router registration pattern.
- Existing Files to Reuse: Task 02's extended limiter.
- Files to Create: `tests/infrastructure/test_multidimensional_rate_limiting.py`, `tests/infrastructure/test_rate_limit_bypass_resistance.py`.
- Files to Modify: `identity` context's auth router endpoint decorators/registrations.
- Implementation Details: per §10's canonical limits; negative test per §27's mandatory bullet.
- Business Rules: exact limits, no deviation without explicit sign-off.
- Validation: as in §15.
- Error Handling: as in §18.
- Security: this task's negative test is the actual security proof.
- Performance: N/A beyond Task 02.
- Localization / RTL: N/A.
- Analytics: N/A beyond §23.
- Tests: integration + negative tests per §27.
- Documentation: final dimension-to-endpoint matrix.
- Dependencies: Task 01, Task 02.
- Do Not Change: N/A.
- Expected Result: all four auth endpoints correctly rate-limited across applicable dimensions, bypass-resistant.
- Definition of Done: integration and negative tests pass.

## 30. Definition of Done
Four-dimension rate limiting implemented and independently enforced (AND semantics) on `register`/`login`/`refresh`/`verify-email` at the canonical limits; single-dimension-rotation bypass proven impossible via a dedicated negative test; Redis-unavailability behavior explicitly decided and tested.

## 31. Final Verification Checklist
- [x] All four dimensions (device, IP, phone, account) independently enforced where the identifier is available per endpoint
- [x] Canonical limits exactly match §3.4 (register 5/hr/IP, login 10/hr/IP, refresh 30/hr/user, verify-email 10/hr/IP)
- [x] Single-dimension-rotation bypass attempt confirmed blocked by remaining dimensions
- [x] Redis-unavailability fail policy explicitly decided, documented, and tested
- [x] 429 error responses use the existing localized error envelope
- [x] No PII (phone, device ID) logged in plaintext
- [x] No PostgreSQL/Redis credential changes introduced

