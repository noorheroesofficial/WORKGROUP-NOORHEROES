# B-02 — Refresh-Token Rotation & Redis Denylist

## 1. Feature Context
NoorHeroes parent sessions use a JWT access/refresh pair. This blueprint implements the rotation-on-use and Redis-backed denylist mechanics that make a stolen refresh token detectable and unusable after its first legitimate rotation. Builds directly on B-01's canonical `JwtClaims` schema. No school/institutional/madarsa logic applies.

## 2. Parent Feature
F.37 — Security Architecture (Cross-Cutting).

## 3. Sub-feature
B-02 — Refresh-Token Rotation & Redis Denylist (Backend / FastAPI).

## 4. Objective
Implement refresh-token rotation on `POST /api/v1/auth/refresh`, with the old token immediately denylisted in Redis and reuse attempts rejected and logged as a security signal, per PRD FR-1/FR-7 and Acceptance Criterion §1.9 ("a replayed/stolen old refresh token" edge case, §1.10 item 2).

## 5. Business Requirements
- FR-7: "JWT access + refresh token pair; refresh rotation on use; Redis-backed denylist for revoked tokens."
- Edge Case §1.10.2: a refresh token used after already being rotated must be rejected by the denylist and treated as a compromise signal, never silently accepted.
- Error table §1.11: "Replayed/stolen rotated refresh token → Rejected via the Redis-backed denylist, treated as a potential compromise signal."
- Rate limit (canonical, §3.4): `refresh` 30/hour/user.
- `logout` immediately revokes the refresh token into the denylist (§3.4).

## 6. Existing Architecture
- `identity` bounded context owns auth endpoints (`FAST-API-INSTRUCTIONS.md` §5.1).
- `infrastructure/redis.py` — existing Redis infrastructure module; this task adds the denylist storage here, not a new Redis client.
- `infrastructure/middleware/rate_limit.py` + `SlidingWindowRateLimiter` — existing Redis-backed rate limiter (reused by B-07 for the `refresh` endpoint's 30/hour/user limit; this blueprint assumes that limiter is applied to the refresh route, coordinate with B-07 rather than re-implementing).
- `core/exceptions.py` — houses `RateLimitExceededError`; add any new denylist-specific exception here following the same pattern.
- Database: `parent_sessions` table (`refresh_hash`, `parent_id`, `device_id`, `revoked`) per PRD §4.2.

## 7. Existing Code to Reuse
- `infrastructure/redis.py` for the Redis client/connection.
- `core/security.py::create_access_token` (from B-01) for issuing the new access/refresh pair.
- `core/schemas/jwt_claims.py::JwtClaims` (from B-01) as the payload shape for the newly-issued tokens.
- `common/base_repository.py` pattern for any `parent_sessions` repository access.

## 8. Files to Create
- `src/noorheroes/identity/services/refresh_token_service.py` (or the equivalent existing service location within `identity` — confirm actual existing file before creating a new one; do not duplicate if a token-refresh service already exists) — rotation + denylist orchestration logic.
- `tests/identity/test_refresh_rotation.py`.
- `tests/identity/test_refresh_replay_rejected.py`.

## 9. Files to Modify
- `identity` context's `POST /api/v1/auth/refresh` route handler — wire to the rotation service.
- `identity` context's `POST /api/v1/auth/logout` route handler — wire immediate revocation into the same denylist.
- `parent_sessions` repository — add `refresh_hash` lookup/update and `revoked` flag methods if not already present.

## 10. Backend Requirements
- On `POST /api/v1/auth/refresh`: (1) hash the incoming refresh token, (2) look up `parent_sessions` by `refresh_hash`, (3) reject if not found, already `revoked`, or present in the Redis denylist, (4) if valid: add the old token's hash to the Redis denylist with a TTL matching its remaining validity, (5) issue a new refresh token, update `parent_sessions.refresh_hash` to the new hash, (6) issue a new access token via B-01's `JwtClaims`/`create_access_token`.
- On `POST /api/v1/auth/logout`: immediately add the current refresh token's hash to the Redis denylist and set `parent_sessions.revoked = true`.
- Denylist check must occur before any other refresh-processing logic (fail fast).
- Concurrent-refresh race: use an atomic Redis operation (e.g., `SETNX` or a Lua script) so two near-simultaneous refresh attempts with the same token cannot both succeed.

## 11. KMP Requirements
Client-side (`core-security`/`core-network`, not implemented in this backend blueprint but must be respected): on every successful refresh, discard the old token and store only the newly-issued one (PRD §6.4); `provideHttpClient`'s automatic-token-refresh-on-401 behavior (per `CORE_NETWORK_INSTRUCTIONS.md` §5) must call the same `/auth/refresh` endpoint this blueprint implements.

## 12. NextJS Requirements
N/A directly — Admin Portal uses its own `httpOnly` cookie-based refresh flow (`NEXT-JS-INSTRUCTIONS.md` §1: "Refresh tokens are stored in httpOnly, SameSite=Strict, Secure cookies managed by backend endpoints"). Confirm whether Admin refresh shares this same `/api/v1/auth/refresh` endpoint or a separate admin-scoped one before assuming reuse — do not guess; flag as **unknown pending confirmation** if the admin auth endpoint path differs.

## 13. API Contract
`POST /api/v1/auth/refresh` — Request: existing refresh-token payload (unchanged shape). Response: new access + refresh token pair (unchanged shape). Auth: refresh token itself is the credential (no Bearer access token required). Validation: token must hash-match an active, non-revoked, non-denylisted `parent_sessions` row. Error Responses: 401 for invalid/revoked/denylisted token (do not distinguish "expired" vs "replayed" in the client-facing error body — that distinction is for internal logging only, so as not to help an attacker probe token state); 429 on rate-limit breach (30/hour/user, coordinate with B-07).
`POST /api/v1/auth/logout` — Request/response unchanged; internal behavior now includes denylist write.

## 14. Database Requirements
`parent_sessions.refresh_hash` stores a hash (never the raw token) — already specified (PRD §4.2); this blueprint's rotation logic must update this column on every successful refresh, never leaving a stale hash. Index `(parent_id, revoked)` already specified — reuse, do not add a redundant index. No PostgreSQL credential changes.

## 15. Validation
- Refresh token hash must exist in `parent_sessions` and match `revoked = false`.
- Refresh token hash must not be present in the Redis denylist.
- Reject with generic 401 (not a detailed reason) to avoid oracle-style probing.

## 16. Authentication
This blueprint extends B-01's issuance mechanics specifically for the refresh flow; no independent authentication scheme is introduced.

## 17. Authorization
N/A — refresh/logout are session-lifecycle operations, not resource-authorization decisions (those live in B-06).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Refresh token not found / already revoked | 401 |
| Refresh token found in Redis denylist (replay) | 401 + log `auth_refresh_token_reuse_detected` as a security event, per PRD §1.19 |
| Redis unavailable during denylist check | Fail closed — reject the refresh request rather than risk accepting a replayed token (explicit architectural decision; document this trade-off in code comments) |
| Rate limit exceeded | 429 via existing `RateLimitExceededError` |
| Concurrent refresh race on same token | Only one request succeeds; the other receives 401 as if replayed |

## 19. Offline First
N/A (server-side).

## 20. Local Data
N/A (server-side); client-side token storage discipline is KMP's `core-security`/`TokenStore` responsibility (§11).

## 21. Localization
N/A — error responses use existing generic error-envelope localization already handled by the platform's i18n layer, no new user-facing strings introduced here.

## 22. RTL
N/A.

## 23. Analytics
Emit per PRD §1.19: `auth_refresh_token_rotated` (success), `auth_refresh_token_reuse_detected` (internal/security signal, P0-alertable per PRD §10 DevOps Requirements).

## 24. Performance
Denylist check and write must be a single low-latency Redis round trip (or one atomic Lua script) to avoid adding meaningful latency to the refresh path, which is a comparatively high-frequency endpoint (30/hour/user ceiling implies frequent legitimate use).

## 25. Security
- Old token must be denylisted **before** (or atomically with) the new token being issued — never a window where both old and new tokens are simultaneously valid.
- Denylist entries must expire (TTL) rather than accumulate forever — set TTL to the original refresh token's remaining lifetime, not a fixed arbitrary value.
- Treat any reuse-detected event as a P0 alert per PRD §10 ("Alert (P0) on any detected refresh-token-reuse-after-rotation event").

## 26. Library Requirements
Reuse existing Redis client library already wired in `infrastructure/redis.py`; no new dependency required. If atomic check-and-set is needed beyond what the existing client exposes, use its native Lua-scripting support rather than adding a new library.

## 27. Testing
- **Unit:** rotation correctly denylists old hash and persists new hash.
- **Unit:** logout immediately denylists and marks `revoked = true`.
- **Integration:** full refresh flow issues a valid new token pair.
- **Negative (mandatory, PRD §13.4):** "Attempt to reuse a rotated-away refresh token → rejected, logged as a potential compromise signal."
- **Concurrency:** two simultaneous refresh attempts with the same token — exactly one succeeds.
- **Failure-mode:** Redis unavailable → refresh request fails closed (rejected), not open.

## 28. Documentation
Document the rotation/denylist sequence diagram (mirroring PRD §1.17's Mermaid flow) in the `identity` context's internal docs; document the fail-closed Redis-unavailability decision explicitly so it isn't "fixed" to fail-open by a future contributor unaware of the rationale.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Add Redis Denylist Storage Helper**
- Task ID: B-02-T01
- Objective: Implement a small helper (e.g., `RefreshTokenDenylist`) wrapping Redis add/check/TTL operations for rotated-out token hashes.
- Why This Is Required: Rotation and logout both need the same denylist primitive; implement once, reuse twice.
- Existing Architecture to Follow: `infrastructure/redis.py` connection pattern.
- Existing Files to Reuse: `infrastructure/redis.py`.
- Files to Create: `src/noorheroes/infrastructure/redis_denylist.py` (or co-located within `infrastructure/redis.py` if that file already groups related helpers — check existing file organization first).
- Files to Modify: none yet.
- Implementation Details: `add(token_hash: str, ttl_seconds: int) -> None`, `contains(token_hash: str) -> bool`.
- Business Rules: TTL must equal remaining token validity, never a fixed constant.
- Validation: N/A at this layer.
- Error Handling: allow Redis connection errors to propagate to the caller (Task 02/03 decide fail-closed behavior).
- Security: never log the raw token, only its hash.
- Performance: single round trip per operation.
- Localization / RTL / Analytics: N/A.
- Tests: unit tests with a test Redis instance/fakeredis.
- Documentation: docstring explaining TTL rationale.
- Dependencies: none.
- Do Not Change: Redis connection configuration/credentials.
- Expected Result: reusable denylist helper.
- Definition of Done: unit tests pass.

**Task 02 — Implement Refresh Rotation Logic**
- Task ID: B-02-T02
- Objective: Implement the full rotate-on-refresh sequence in the `identity` context.
- Why This Is Required: Core deliverable of this blueprint.
- Existing Architecture to Follow: `identity` context service pattern, B-01's `JwtClaims`/`create_access_token`.
- Existing Files to Reuse: Task 01's denylist helper, `parent_sessions` repository.
- Files to Create: `src/noorheroes/identity/services/refresh_token_service.py` (confirm no equivalent already exists first).
- Files to Modify: `identity`'s `/auth/refresh` route handler.
- Implementation Details: sequence per §10; use an atomic check-and-denylist to close the concurrency race (§10, §27).
- Business Rules: fail closed on Redis unavailability (§18).
- Validation: as in §15.
- Error Handling: as in §18.
- Security: never allow old and new token to be simultaneously valid (§25).
- Performance: single Redis round trip where possible (§24).
- Localization / RTL: N/A.
- Analytics: emit `auth_refresh_token_rotated` on success.
- Tests: unit + integration + concurrency tests per §27.
- Documentation: sequence diagram per §28.
- Dependencies: Task 01, B-01 complete.
- Do Not Change: token TTL values, signing mechanics (owned by B-01).
- Expected Result: rotation fully functional and race-safe.
- Definition of Done: all §27 tests pass.

**Task 03 — Implement Replay Detection & Logout Revocation**
- Task ID: B-02-T03
- Objective: Reject reuse of a denylisted token as a security event; wire logout to revoke immediately.
- Why This Is Required: PRD edge case §1.10.2 and error table §1.11 explicitly require this, not merely rotation itself.
- Existing Architecture to Follow: `core/exceptions.py` pattern for the rejection error type.
- Existing Files to Reuse: Task 01's denylist helper.
- Files to Create: none (extends Task 02's service).
- Files to Modify: `identity`'s `/auth/logout` route handler; `refresh_token_service.py`.
- Implementation Details: on `/refresh`, check denylist before DB lookup; on `/logout`, denylist immediately + set `revoked = true`.
- Business Rules: reuse is always treated as a potential-compromise signal, never silently accepted (§5).
- Validation: as in §15.
- Error Handling: as in §18, including the P0-alertable log event.
- Security: emit `auth_refresh_token_reuse_detected` for monitoring/alerting integration (§25/§28 DevOps).
- Performance: N/A beyond Task 02.
- Localization / RTL: N/A.
- Analytics: `auth_refresh_token_reuse_detected`.
- Tests: negative test per §27 ("Attempt to reuse a rotated-away refresh token").
- Documentation: note the P0-alert wiring expectation for DevOps (out of scope to configure the actual alerting pipeline in this task — flag as a DevOps follow-up if no alerting hook exists yet).
- Dependencies: Task 01, Task 02.
- Do Not Change: N/A.
- Expected Result: replay attempts are rejected and logged; logout is immediate.
- Definition of Done: negative and logout tests pass.

## 30. Definition of Done
Rotation, denylisting, replay-rejection, and logout-revocation all implemented and tested against a real (or fakeredis-backed) Redis instance; rate limiting on `/refresh` coordinated with B-07; fail-closed behavior on Redis outage documented and tested; no PostgreSQL/Redis credential changes.

## 31. Final Verification Checklist
- [x] Old refresh token denylisted before/atomically with new token issuance
- [x] Denylist entries carry correct TTL (not permanent, not premature expiry)
- [x] Replay of a rotated-away token rejected and logged as `auth_refresh_token_reuse_detected`
- [x] Logout immediately revokes (denylist + `parent_sessions.revoked = true`)
- [x] Concurrent-refresh race produces exactly one success
- [x] Redis-unavailability path fails closed, tested explicitly
- [x] Rate limiting present on `/refresh` (30/hour/user)
- [x] No raw refresh token ever logged
- [x] Unit + integration + negative + concurrency tests green

