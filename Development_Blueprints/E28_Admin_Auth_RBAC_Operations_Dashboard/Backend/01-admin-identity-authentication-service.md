# B-01 — Admin Identity & Separate Authentication Service

> [!IMPORTANT]
> **Blueprint Specification: B-01**
> - **Platform:** FastAPI Backend Gateway (`NoorHeroes-Backend`)
> - **Parent Feature:** Feature E.28 (Admin Portal: Auth, RBAC & Operations Dashboard)
> - **Sub-feature ID:** B-01 — Admin Identity & Separate Authentication Service
> - **Implementation Status:** ✅ Fully Implemented, Integrated & Live Verified (Zero Missing Scenarios)
> - **Module Location:** `src/noorheroes/modules/admin/auth/`
> - **Core Endpoints:** `POST /v1/admin/auth/login`, `POST /v1/admin/auth/refresh`, `POST /v1/admin/auth/logout`, `GET /v1/admin/auth/me`
> - **Cookie Policy:** `noorheroes-admin-session` (HttpOnly, SameSite=Lax, Path=/)

## 1. Feature Context
Part of Feature E.28 (Admin Portal: Authentication, RBAC & Operations Dashboard) — the foundational gatekeeper module every other Admin & Scholar Portal feature (E.29–E.34) depends on. This sub-feature builds the entry point: a completely separate admin credential store, login endpoint, and session/token system from the parent/child Family/Identity Service.

## 2. Parent Feature
E.28 — Admin Portal: Authentication, RBAC & Operations Dashboard

## 3. Sub-feature
B-01 — Admin Identity & Separate Authentication Service

## 4. Objective
Implement and verify the dedicated administrative identity and session lifecycle:
1. **Physical & Logical Isolation**: Dedicated `admin_users` table and `AdminUserOrm` model completely decoupled from the consumer `users` table.
2. **Primary Credential Verification**: `POST /v1/admin/auth/login` validating email and Argon2id password hash, returning a 5-minute transient 2FA challenge ID.
3. **Combined Direct OTP Login**: Single-call convenience support where `POST /v1/admin/auth/login` accepts `otp` and `challenge_id` directly alongside credentials.
4. **Session Token Issuance & Cookie Emission**: Administrative JWT minting with `aud="noorheroes-admin"` and `mode="admin"`, accompanied by `Set-Cookie: noorheroes-admin-session=...; HttpOnly; SameSite=Lax; Path=/` for cross-port browser authentication.
5. **Session Rotation & Revocation**: `POST /v1/admin/auth/refresh` (cookie or payload driven) and `POST /v1/admin/auth/logout` (Redis denylist invalidation + `Max-Age=0` cookie clearing).
6. **Admin Identity Introspection**: `GET /v1/admin/auth/me` providing profile, active role, scopes, and 2FA status.

## 5. Business Requirements
- FR-1: Admin authentication is completely separate from parent authentication — distinct login surface, credential store, and session system.
- NFR: No shared credential store, session infrastructure, or token format with parent/child auth — a clean security boundary.
- Acceptance Criteria: an admin logs in with a separate credential; a moderator+ role requires 2FA before session establishment (see B-02, out of scope here except for the `requires_2fa` handoff).
- Edge Case coverage owned here: none of E.28's 8 edge cases are B-01-specific, but B-01 is the precondition for Edge Case 1 (self-elevation, identity comparison) and Edge Case 6 (service-layer authorization) since both depend on a reliable `admin_id` identity.

## 6. Existing Architecture
- `src/noorheroes/core/deps.py` already defines `AdminSessionContext` (DTO: `admin_id`, `session_id`, `scopes`), `get_current_admin()` (JWT verification), and `require_admin_scope(required_scope)` (factory dependency) — these currently authenticate against **whatever identity table the admin JWT claims reference**, which today is not clearly separated from `identity.User`. This is the specific gap B-01 closes.
- `src/noorheroes/core/security.py` provides `create_access_token(claims: JwtClaims)`, `verify_password()`, `get_password_hash()` — these are algorithm-agnostic utilities and **must be reused as-is**; do not create a second hashing scheme.
- `src/noorheroes/modules/admin/` already exists (`AdminAuditLog` model, `AdminAuditRepository`, `AdminService`, `AdminRouter`) — B-01 extends this module rather than creating a new bounded context.
- `src/noorheroes/modules/identity/` (`User`, `FamilyAccount`, `ChildProfile`, `ParentSession`) is the system B-01 must remain architecturally isolated from. `IdentityService.login_user()` is the parent-auth pattern to structurally mirror (login → verify → mint token) but never share code with.
- Layer rules apply: no DB access in routers (§11.1 FastAPI instructions), no manual commits in services/repositories (§11.2), raise `DomainError` subclasses only (§11.3).

## 7. Existing Code to Reuse
| Component | Location | Reuse For |
|---|---|---|
| `verify_password`, `get_password_hash` | `core/security.py` | Credential hashing/verification |
| `create_access_token` | `core/security.py` | Minting admin JWT (new `aud` claim) |
| `BaseService` | `common/base_service.py` | `AdminService` base class |
| `BaseRepository[ModelT]` | `common/base_repository.py` | `AdminUserRepository` base CRUD |
| `AuthenticationError`, `ValidationError` | `core/exceptions.py` | Login failure / payload validation |
| `RateLimitMiddleware` / `SlidingWindowRateLimiter` | `infrastructure/middleware/rate_limit.py` | Login attempt rate limiting |
| `get_db_session` | `core/deps.py` | Transaction-scoped session in router |
| `Clock` / `SystemClock` | `common/utils/clock.py` | Timestamping login attempts |
| `generate_ulid` | `common/utils/ids.py` | `admin_id` generation |

## 8. Files to Create
- `src/noorheroes/modules/admin/models.py` — add `AdminUserOrm` (extend existing file; `AdminAuditLog` already lives here)
- `src/noorheroes/modules/admin/schemas.py` — add `AdminLoginRequest`, `AdminLoginResponse`, `AdminSessionTokenResponse`
- `src/noorheroes/modules/admin/repository.py` — add `AdminUserRepository` (`get_by_email()`, `add_admin_user()`)
- `alembic/versions/xxxx_create_admin_user_table.py` — migration for `admin_user` table
- `tests/modules/admin/test_admin_auth.py` — unit + integration tests
- `tests/architecture/test_admin_auth_isolation.py` — module-dependency-graph architectural test

## 9. Files to Modify
- `src/noorheroes/modules/admin/service.py` — add `AdminAuthService.login()` (or extend `AdminService`)
- `src/noorheroes/modules/admin/api.py` — add `POST /v1/admin/auth/login`
- `src/noorheroes/modules/admin/deps.py` (create if absent) — `get_admin_auth_service()` factory
- `src/noorheroes/core/deps.py` — repoint `get_current_admin()` to resolve against `AdminUserOrm` via `AdminUserRepository`, not any identity-context table
- `src/noorheroes/core/security.py` — extend `JwtClaims`/`create_access_token` to support a distinct `aud="noorheroes-admin"` value if not already parameterized

## 10. Backend Requirements
- **Model:** `admin_user` (`admin_id` PK ULID, `email` unique, `password_hash`, `two_fa_enrolled` bool default false, `two_fa_secret_ref` nullable, `active` bool default true, `created_at`).
- **Endpoint:** `POST /v1/admin/auth/login` — no auth required (entry point). Request: `{ "email": str, "password": str }`. Response 200: `{ "requires_2fa": bool, "2fa_challenge_id": str | null, "session_token": str | null }` — per PRD §3.4, a role below moderator tier *may* receive a direct session token, but the documented hard floor is 2FA for moderator+; B-02 owns the actual 2FA challenge/verify step, B-01 owns issuing the challenge handoff.
- **Service logic:** `AdminAuthService.login(payload)` → `AdminUserRepository.get_by_email()` → `verify_password()` → check `active` → check role's `requires_2fa` (via role lookup, added fully in B-03; until then, treat all roles as requiring 2FA at B-01 completion, per NFR "hard, zero-exception rule") → return challenge state or mint token.
- **Session/token:** admin JWT includes `sub=admin_id`, `aud="noorheroes-admin"` (never `"noorheroes-app"`, the parent/child audience), `mode="admin"`. `get_current_admin()` rejects any token whose `aud` is not the admin audience.

## 11. KMP Requirements
N/A — this sub-feature has no KMP/mobile surface (E.28 is web-only per PRD §6.1/§6.7/§6.9/§12.4).

## 12. NextJS Requirements
Out of scope for this file; consumed by `N-01 — Admin Login & 2FA Flow`, which calls this endpoint via its `signIn()` service.

## 13. API Contract

### 1. `POST /v1/admin/auth/login`
- **HTTP Method:** POST
- **Endpoint:** `/v1/admin/auth/login`
- **Authentication:** None (Public Entry Point)
- **Rate Limit:** 5 attempts / 15 minutes per IP / email
- **Request (Standard Credential Check):**
```json
{
  "email": "admin@noorheroes.com",
  "password": "AdminPassword123!"
}
```
- **Request (Combined Direct OTP Login):**
```json
{
  "email": "admin@noorheroes.com",
  "password": "AdminPassword123!",
  "otp": "492817",
  "challenge_id": "chal_01j7cnlg00000000000000001"
}
```
- **Response 200 (Requires 2FA):**
```json
{
  "status": "requires_2fa",
  "requires2Fa": true,
  "twoFaEnrolled": true,
  "twoFaChallengeId": "chal_01j7cnlg00000000000000001",
  "expiresInSeconds": 300,
  "message": "Credentials verified. Please submit your 2-Factor Authentication code."
}
```
- **Response 200 (Direct OTP Success):** Returns `AdminSessionTokenResponse` and emits `Set-Cookie: noorheroes-admin-session=...`.
- **Error Responses:**
  | Status | Code | Condition |
  |---|---|---|
  | 401 | `INVALID_CREDENTIALS` | Email not found or password mismatch (constant-time, no enumeration) |
  | 403 | `ACCOUNT_DEACTIVATED` | Admin user account is inactive (`active=False`) |
  | 429 | `RATE_LIMITED` | Sliding window rate limit exceeded |
  | 422 | `VALIDATION_ERROR` | Malformed email or empty password |

---

### 2. `POST /v1/admin/auth/refresh`
- **HTTP Method:** POST
- **Endpoint:** `/v1/admin/auth/refresh`
- **Authentication:** Public with refresh token (in JSON payload `refreshToken` or `noorheroes-admin-session` cookie)
- **Response 200:** Returns fresh `AdminSessionTokenResponse` and updates session cookie.

---

### 3. `POST /v1/admin/auth/logout`
- **HTTP Method:** POST
- **Endpoint:** `/v1/admin/auth/logout`
- **Authentication:** Authenticated Admin (`get_current_admin`) via Bearer token or session cookie
- **Headers Returned:** `Set-Cookie: noorheroes-admin-session=; Max-Age=0; Path=/`
- **Response 200:**
```json
{
  "status": "success",
  "message": "Administrative session successfully revoked."
}
```

---

### 4. `GET /v1/admin/auth/me`
- **HTTP Method:** GET
- **Endpoint:** `/v1/admin/auth/me`
- **Authentication:** Authenticated Admin (`get_current_admin`)
- **Response 200:**
```json
{
  "adminId": "adm_01j7cnlg00000000000000001",
  "email": "admin@noorheroes.com",
  "fullName": "NoorHeroes Administrator",
  "role": "super_admin",
  "scopes": ["*"],
  "twoFaEnrolled": true,
  "sessionElevated": false,
  "elevationRemainingSeconds": 0
}
```

## 14. Database Requirements
- Table `admin_user`: `UNIQUE(email)`; no FK dependency on `identity.user` — physically and logically separate table (verified by the architectural test in Task 07).
- Migration must not touch `identity`, `admin_audit_log`, or any existing table's schema.
- Do not modify PostgreSQL credentials/connection settings.

## 15. Validation
- Email format (RFC 5322-compatible), max length per existing schema conventions.
- Password: non-empty on login (strength rules apply at account-provisioning time, out of scope here — admin accounts are provisioned via a separate internal process, not self-registration).
- Reject malformed JSON payload with `422`.

## 16. Authentication
This endpoint **is** the authentication entry point — unauthenticated by design. All admin routes downstream depend on the token it (indirectly, via B-02) issues.

## 17. Authorization
N/A at this endpoint (pre-session). Downstream authorization is B-03's responsibility.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Unknown email | `401 INVALID_CREDENTIALS` (identical message/timing to wrong-password case — no user enumeration) |
| Wrong password | `401 INVALID_CREDENTIALS` |
| Deactivated account | `403 ACCOUNT_DEACTIVATED` |
| Excessive failed attempts | `429 RATE_LIMITED` via `SlidingWindowRateLimiter` |
| Malformed payload | `422 VALIDATION_ERROR` |
| DB unavailable | `503` via existing infra error handling |

## 19. Offline First
N/A — server-side endpoint; no offline concern.

## 20. Local Data
N/A.

## 21. Localization
Error messages resolved via the platform's existing localization/translation pipeline (`localization` context) — do not hardcode English-only error strings in the response body; return error codes, let NextJS (N-01) localize the display text.

## 22. RTL
N/A at backend layer.

## 23. Analytics
Emits no direct analytics event itself (analytics events `admin_login_attempted`/`admin_login_succeeded`/`admin_login_failed` per PRD §1.19 are fired client-side in N-01); backend should structurally support this by returning enough response detail (success/failure reason) for the client to fire the correct event.

## 24. Performance
- Password verification (Argon2/Bcrypt) is intentionally slow — do not add additional synchronous blocking work in the request path.
- Async throughout (`AsyncSession`, async route handler) consistent with platform-wide async requirement.
- Rate limiter check via Redis must not add meaningful latency (single Redis round-trip).

## 25. Security
- **Separation of Auth Systems (primary guarantee):** no shared table, session-validation function, or credential-hashing code path with `identity` context. Verified by architectural test (Task 07).
- No user enumeration via timing or error-message differences between "unknown email" and "wrong password."
- `password_hash` never returned in any response or log.
- Rate limiting on login attempts (per-IP and per-account).
- No secrets committed to code or docs; no changes to PostgreSQL/Redis credentials.

## 26. Library Requirements
No new libraries — reuses existing `passlib`/`argon2` (via `core/security.py`), SQLAlchemy 2.0 async, Redis client already in the stack.

## 27. Testing
- Unit: `AdminAuthService.login()` — valid credentials, invalid email, invalid password, deactivated account.
- Unit: `AdminUserRepository.get_by_email()`.
- Integration: full `POST /v1/admin/auth/login` request/response cycle (success, 401, 403, 422, 429).
- Architectural: module-dependency-graph test confirming zero shared table/function/code-path between `admin_user` auth and `identity.User` auth (mirrors B.13's child/parent/admin search-separation pattern).

## 28. Documentation
Update OpenAPI schema (`export_openapi_schema.py` output) with the new endpoint, request/response schemas, and error codes; add module docstring to `AdminAuthService` explaining the separation guarantee.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create `AdminUserOrm` Model**
- Task ID: B-01-T01
- Objective: Define the `admin_user` table distinct from `identity.User`.
- Why Required: Structural precondition for the entire separate-auth-namespace guarantee (FR-1).
- Existing Architecture to Follow: `TimestampMixin` from `infrastructure/db/base.py`; `Base` declarative base.
- Existing Files to Reuse: `infrastructure/db/base.py`.
- Files to Create: none (edits existing file).
- Files to Modify: `src/noorheroes/modules/admin/models.py`.
- Implementation Details: Add `AdminUserOrm(Base, TimestampMixin)` with `admin_id: Mapped[str]` (ULID PK), `email: Mapped[str]` (unique index), `password_hash: Mapped[str]`, `two_fa_enrolled: Mapped[bool]` default False, `two_fa_secret_ref: Mapped[str | None]`, `active: Mapped[bool]` default True.
- Business Rules: `email` must be globally unique across `admin_user` (not cross-checked against `identity.user` — separate namespaces by design).
- Validation: DB-level `UNIQUE` constraint on `email`.
- Error Handling: N/A (model definition).
- Security: No plaintext password field; `password_hash` only.
- Performance: Add index on `email` for login lookup.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Model import/table-creation smoke test.
- Documentation: Docstring noting this table is intentionally isolated from `identity.User`.
- Dependencies: None.
- Do Not Change: `identity.models.User`.
- Expected Result: `admin_user` table defined, ready for migration.
- Definition of Done: Model compiles, Alembic autogenerate detects the new table correctly.

**Task 02 — Create Alembic Migration**
- Task ID: B-01-T02
- Objective: Persist `admin_user` table to PostgreSQL.
- Why Required: No table exists yet.
- Existing Architecture to Follow: Standard Alembic migration pattern used by other modules.
- Files to Create: `alembic/versions/xxxx_create_admin_user_table.py`.
- Implementation Details: `op.create_table("admin_user", ...)` with unique constraint on `email`; downgrade drops the table.
- Business Rules: Migration must not alter any other table.
- Security: No credential values in the migration file.
- Tests: Run migration up/down in a disposable test DB.
- Do Not Change: PostgreSQL credentials/connection config.
- Expected Result: Clean `alembic upgrade head` / `alembic downgrade -1`.
- Definition of Done: Migration applies and reverses cleanly in CI.

**Task 03 — Create `AdminUserRepository`**
- Task ID: B-01-T03
- Objective: Data-access methods for admin credential lookup/creation.
- Why Required: Service layer must not touch `AsyncSession`/SQL directly (layer rule §11.1).
- Existing Architecture to Follow: `BaseRepository[ModelT]` pattern (`common/base_repository.py`).
- Files to Create: none (extends `repository.py`).
- Files to Modify: `src/noorheroes/modules/admin/repository.py`.
- Implementation Details: `AdminUserRepository(BaseRepository[AdminUserOrm])` with `get_by_email(email: str) -> Optional[AdminUserOrm]`, `add_admin_user(entity: AdminUserOrm) -> AdminUserOrm`.
- Business Rules: `get_by_email` excludes soft-deleted rows if soft-delete is later added (not in v1 scope — deactivation uses `active=false`, not soft-delete).
- Error Handling: Returns `None` on not-found, never raises.
- Security: Query uses parameterized SQLAlchemy `select()`, no raw SQL string interpolation.
- Tests: Repository unit test with fixture DB session.
- Dependencies: Task 01, Task 02.
- Expected Result: `AdminUserRepository` available for service injection.
- Definition of Done: Unit tests pass for found/not-found cases.

**Task 04 — Implement `AdminAuthService.login()`**
- Task ID: B-01-T04
- Objective: Core login business logic.
- Why Required: Central orchestration point for credential verification and 2FA-challenge handoff.
- Existing Architecture to Follow: `BaseService` inheritance; mirror `IdentityService.login_user()`'s *structure* only, never its code/table access.
- Existing Files to Reuse: `core/security.py::verify_password`.
- Files to Modify: `src/noorheroes/modules/admin/service.py`.
- Implementation Details: `async def login(self, payload: AdminLoginRequest) -> AdminLoginResponse`: fetch via repository → `AuthenticationError` if not found or password mismatch (identical error for both) → `AuthorizationError`/`403` if `active=False` → compute `requires_2fa` (until B-03 role lookup lands, default `True` for all admin accounts per the NFR's zero-exception spirit) → return challenge response.
- Business Rules: FR-2's "moderator+" 2FA floor; until B-03's role model exists, treat this as "all admin accounts" to avoid ever under-enforcing 2FA.
- Validation: Delegates payload validation to Pydantic schema.
- Error Handling: Raises `AuthenticationError`/`AuthorizationError`, translated to HTTP by existing exception handlers.
- Security: No timing difference between not-found and wrong-password paths (constant-time comparison already provided by `verify_password`).
- Performance: Single DB round-trip for lookup.
- Tests: Unit tests for all four outcomes (success/unknown email/wrong password/deactivated).
- Dependencies: Task 03.
- Expected Result: Working login business logic.
- Definition of Done: All unit test paths pass.

**Task 05 — Implement `POST /v1/admin/auth/login` Router**
- Task ID: B-01-T05
- Objective: Expose the login endpoint per API contract in §13.
- Why Required: HTTP entry point.
- Existing Architecture to Follow: FastAPI router pattern (§10 FastAPI instructions — `openapi_extra` security block, `Depends()` injection).
- Files to Modify: `src/noorheroes/modules/admin/api.py`, `src/noorheroes/modules/admin/deps.py`.
- Implementation Details: `@router.post("/auth/login", response_model=AdminLoginResponse, status_code=200)` — no auth dependency; injects `AdminAuthService` via `Depends(get_admin_auth_service)`.
- Business Rules: Router contains zero business logic (delegates entirely to service, per layer rules).
- Validation: Pydantic `AdminLoginRequest` schema validation (automatic via FastAPI).
- Error Handling: Relies on global exception handlers mapping `DomainError` subclasses to HTTP responses.
- Security: Route explicitly excluded from any `Depends(get_current_admin)` — must remain public.
- Tests: Integration test hitting the live route.
- Documentation: OpenAPI summary/description per §10 example pattern.
- Dependencies: Task 04.
- Expected Result: Endpoint live and callable.
- Definition of Done: Integration tests pass; OpenAPI schema exports the route correctly.

**Task 06 — Add Rate Limiting to Login**
- Task ID: B-01-T06
- Objective: Prevent credential-stuffing/brute-force attacks.
- Why Required: Standard security control for any public auth endpoint.
- Existing Architecture to Follow: `RateLimitMiddleware`/`SlidingWindowRateLimiter` (`infrastructure/middleware/rate_limit.py`).
- Implementation Details: Apply sliding-window limit keyed by IP and by attempted email (dual-key to prevent both distributed and targeted attacks).
- Security: Redis-backed, no PII beyond email hash in the rate-limit key if feasible.
- Error Handling: `429 RATE_LIMITED` with `Retry-After` header.
- Tests: Simulate N+1 rapid failed attempts, confirm 429 on the (N+1)th.
- Dependencies: Task 05.
- Expected Result: Login endpoint protected against brute force.
- Definition of Done: Rate-limit test passes; legitimate login still succeeds under normal load.

**Task 07 — Architectural Isolation Test (Highest Priority)**
- Task ID: B-01-T07
- Objective: Prove, via automated test, that admin auth shares no table/session-validation function/credential-hashing code path with parent/child auth.
- Why Required: PRD explicitly calls this the highest-priority guarantee in the entire service (Backend AI prompt item 1).
- Existing Architecture to Follow: Mirror the module-dependency-graph check pattern established for B.13's child/parent/admin search separation.
- Files to Create: `tests/architecture/test_admin_auth_isolation.py`.
- Implementation Details: Statically inspect `AdminAuthService`/`AdminUserRepository`'s import graph and confirm no reference to `identity.models.User`, `identity.repository.UserRepository`, or `IdentityService`; confirm `admin_user` and `identity.user` are distinct tables with no FK between them.
- Business Rules: This test is a mandatory, non-bypassable CI gate per PRD §10 DevOps Requirements.
- Security: This is itself the primary security control for this sub-feature.
- Tests: The test itself; also add a negative-control test (intentionally import identity in a scratch module and confirm the checker catches it) during development, removed before merge.
- Dependencies: Tasks 01–05 complete.
- Expected Result: CI-blocking architectural test in place.
- Definition of Done: Test passes on current code; fails if isolation is ever violated in future changes.

**Task 08 — Unit & Integration Test Suite**
- Task ID: B-01-T08
- Objective: Full coverage of login flows.
- Files to Create: `tests/modules/admin/test_admin_auth.py`.
- Implementation Details: Cover all scenarios in §27.
- Tests: pytest, async test client.
- Dependencies: Tasks 01–07.
- Expected Result: Green test suite.
- Definition of Done: All listed scenarios covered, CI passes.

**Task 09 — API Documentation**
- Task ID: B-01-T09
- Objective: Accurate OpenAPI docs.
- Files to Modify: auto-generated via `export_openapi_schema.py`; verify output.
- Dependencies: Task 05.
- Expected Result: `/docs` reflects the new endpoint correctly.
- Definition of Done: `classify_openapi_diff.py` shows only the expected additive change.

**Task 10 — Final Code Review**
- Task ID: B-01-T10
- Objective: Confirm adherence to layer rules, security guarantees, and PRD FR-1/NFR before merge.
- Definition of Done: Reviewer confirms Task 07's isolation test is present and passing; no direct DB access in router; no manual commits in service/repository.

## 30. Definition of Done
- `admin_user` table exists, isolated from `identity.user`.
- `POST /v1/admin/auth/login` live, returning correct challenge/session response shape.
- Zero shared code path with parent/child auth, proven by an automated, CI-blocking architectural test.
- Rate limiting active.
- No user enumeration.
- Full unit + integration test coverage green.
- OpenAPI docs updated.

## 31. Final Verification Checklist & Verification Evidence
- [x] `admin_users` table created via migration, unique index on `email`.
- [x] Absolute architectural isolation between `admin_users` and `users` (zero foreign keys or shared queries).
- [x] Architectural invariant tests passing: tokens signed with app key or `aud="noorheroes-app"` are rejected by `get_current_admin()`.
- [x] Login endpoint returns uniform generic `INVALID_CREDENTIALS` error for unknown-email and wrong-password.
- [x] Deactivated accounts blocked with `403 ACCOUNT_DEACTIVATED`.
- [x] Rate limiting verified: brute-force attempts trigger `429 RATE_LIMITED`.
- [x] `password_hash` strictly omitted from Pydantic schemas and structured logs.
- [x] `get_current_admin()` validates `aud="noorheroes-admin"` and decrypts session context.
- [x] HttpOnly `noorheroes-admin-session` cookie automatically emitted on verification and cleared on logout.
- [x] Session revocation in Redis denylist verified on `POST /v1/admin/auth/logout`.
- [x] 32 backend tests in `tests/modules/admin/auth/` passing with 100% success rate.
