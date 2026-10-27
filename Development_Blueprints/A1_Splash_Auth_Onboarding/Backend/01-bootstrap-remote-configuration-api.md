# B-01 — Bootstrap & Remote Configuration API

## 1. Feature Context
Entry-point backend service for NoorHeroes. Every app launch (Android/iOS) calls this endpoint before any other screen renders. It decides where the client routes to (Profile Picker / Add Child / Language-Intro-Login), whether the client must block on a forced update, whether maintenance mode is active, and hands back cacheable remote-config values (intro slides version, active consent version). No content, paywall, or auth screen is reachable before this call resolves.

## 2. Parent Feature
Feature A.1 — Splash, Language Selection, Authentication & Onboarding (`PRD_Documents/Child App (1-12)/Feature_A1_Splash_Auth_Onboarding.md`)

## 3. Sub-feature
1.1 Bootstrap & Remote Configuration API (ID: **B-01**)

## 4. Objective
Implement `GET /v1/identity/bootstrap` so that every client launch gets, in a single fast call: session validity, whether the family has children, forced/recommended update gates (computed server-side via semver, never trusting the client's own version claim), maintenance-mode status, and a short-TTL-cacheable remote-config payload.

## 5. Business Requirements
- FR-1: App must determine session validity at launch via `GET /v1/bootstrap` and route accordingly (valid session + children → Profile Picker; valid session, no children → Add Child; no session → Intro/Login).
- FR-2: App must support forced update (blocking) and recommended update (dismissible) gates evaluated at bootstrap.
- NFR: Bootstrap response p95 < 400ms.
- NFR: Auth service ≥ 99.9% uptime; the bootstrap endpoint must degrade gracefully, not hard-fail, on downstream slowness.
- Acceptance Criteria: Given a returning parent with an existing session and at least one child, when the app launches, the user lands directly on the Profile Picker without repeating intro/login.
- Never trust the client's self-reported app version for forced-update logic — compare server-side only, using a proper semver library.

## 6. Existing Architecture
- Modular monolith, layered `Router → Service → Repository → PostgreSQL`, per `FAST-API-INSTRUCTIONS.md` §1, §7.
- This endpoint belongs in the existing `identity` bounded context (`src/noorheroes/modules/identity/`) alongside `IdentityRouter`, `IdentityService`.
- Core dependency pattern: `Depends(get_db_session)`, `Depends(get_current_parent)` (existing), and a **new** optional-auth dependency (see §9) following the same `core/deps.py` pattern as `ParentSessionContext`.
- Redis usage pattern: `infrastructure/redis.py` → `get_redis_pool()` / `reset_redis_pool()` (already used for OTP/session cache elsewhere in the identity context — reuse the same pool, do not create a second Redis client).
- Rate limiting pattern: `RateLimitMiddleware` + `SlidingWindowRateLimiter` (existing, Redis-backed sliding window).
- Exception pattern: raise `DomainError` subclasses (`NotFoundError`, `ValidationError`, etc.) from `core/exceptions.py` — never a naked `HTTPException`.
- No client-visible microservice split: this is **not** a separate "Remote Config Service" deployment — it is a router + service + repository inside the existing `identity` module, consistent with "use existing architecture, do not invent a new one."

## 7. Existing Code to Reuse
- `src/noorheroes/core/deps.py::get_db_session`
- `src/noorheroes/core/deps.py::ParentSessionContext` (as the shape to model the *optional* variant on)
- `src/noorheroes/infrastructure/redis.py::get_redis_pool`
- `src/noorheroes/infrastructure/middleware/rate_limit.py::RateLimitMiddleware`, `SlidingWindowRateLimiter`
- `src/noorheroes/common/base_service.py::BaseService`
- `src/noorheroes/common/base_repository.py::BaseRepository`
- `src/noorheroes/common/outbox.py::OutboxWriter`
- `src/noorheroes/core/exceptions.py` (`NotFoundError`, `ValidationError`, base `DomainError`)
- `src/noorheroes/modules/identity/api.py` (`IdentityRouter` — add the new route here)
- `src/noorheroes/modules/identity/models.py` (`FamilyAccount`, `ChildProfile` — for has_children lookup)

## 8. Files to Create
- `src/noorheroes/modules/identity/remote_config_models.py` — `RemoteConfigOrm` SQLAlchemy model
- `alembic/versions/xxxx_add_remote_config_table.py` — migration
- `src/noorheroes/modules/identity/bootstrap_schemas.py` — `BootstrapResponse`, `RemoteConfigPayload` Pydantic schemas
- `src/noorheroes/modules/identity/remote_config_repository.py` — `RemoteConfigRepository(BaseRepository[RemoteConfigOrm])`
- `src/noorheroes/modules/identity/bootstrap_service.py` — `BootstrapService(BaseService)`
- `src/noorheroes/common/utils/semver_compare.py` — `compare_versions(client_version, min_version, recommended_version) -> UpdateGateResult`
- `tests/modules/identity/test_bootstrap_service.py`
- `tests/modules/identity/test_bootstrap_api.py`

## 9. Files to Modify
- `src/noorheroes/core/deps.py` — add `get_optional_parent()` dependency (returns `ParentSessionContext | None` instead of raising `AuthenticationError` on missing/invalid token) and `get_bootstrap_service()` factory
- `src/noorheroes/modules/identity/api.py` — register `GET /v1/identity/bootstrap`
- `src/noorheroes/modules/identity/models.py` — no schema change, but confirm `FamilyAccount.owner_parent_id` / `ChildProfile.family_id` indices support the has-children lookup (add index only if genuinely missing — do not touch unrelated columns)
- `src/noorheroes/scripts/export_openapi_schema.py` — no code change needed, re-run after route addition to refresh `openapi.json`

## 10. Backend Requirements
- **Router**: `GET /v1/identity/bootstrap`, optional bearer auth, headers `X-App-Version` (required), `X-Platform` (required: `android`/`ios`), `X-Locale` (optional).
- **Service** (`BootstrapService`):
  - Resolve session: if a valid bearer token is present, decode via `get_optional_parent`; look up `family_id`, count active (non-deleted) children.
  - Resolve version gate: fetch `RemoteConfigOrm` singleton row (cached), run `compare_versions(X-App-Version, min_supported_version, recommended_version)`.
  - Resolve maintenance flag from the same cached row.
  - Assemble `BootstrapResponse`.
  - Emit `bootstrap_completed` (success) or `bootstrap_failed` (exception path) via `OutboxWriter`.
- **Repository** (`RemoteConfigRepository`): single-row config table read (`get_active_config()`), used by both this feature and B-09 (admin write side).
- Async/non-blocking throughout — no blocking I/O in the request path.

## 11. Consuming Clients (context only — not built in this blueprint)
- **KMP App (K-01 — Splash, Bootstrap & App Update Gating Flow)**: calls this endpoint at launch, caches only the `remote_config` object client-side for 5 minutes, never caches `session_valid`.
- **NextJS Admin (N-05 — Remote Configuration & Release Management Panel)**: writes the same `remote_config` row via B-09; this endpoint only reads it.

## 12. API Contract

### `GET /v1/identity/bootstrap`
- **Auth:** Optional. `Authorization: Bearer <token>` header if present is validated via `get_optional_parent` — an invalid/expired token must **not** raise 401; it must be treated as `session_valid: false` (bootstrap must never hard-fail an app launch because of an expired token).
- **Request Headers:**
  - `Authorization: Bearer <token>` (optional)
  - `X-App-Version` (required, semver string, e.g. `4.2.0`)
  - `X-Platform` (required, enum: `android` | `ios`)
  - `X-Locale` (optional, BCP-47 tag, e.g. `en-US`, `ar-SA`)
- **Response 200:**
```json
{
  "session_valid": true,
  "family_id": "fam_8a1c...",
  "has_children": true,
  "min_supported_version": "4.2.0",
  "recommended_version": "5.1.0",
  "maintenance_mode": false,
  "remote_config": {
    "intro_slides_version": "3",
    "consent_version": "2025-11-01"
  }
}
```
- **Response 200 (unauthenticated / no session):**
```json
{
  "session_valid": false,
  "family_id": null,
  "has_children": false,
  "min_supported_version": "4.2.0",
  "recommended_version": "5.1.0",
  "maintenance_mode": false,
  "remote_config": { "intro_slides_version": "3", "consent_version": "2025-11-01" }
}
```
- **Error Codes:**
  - `503 MAINTENANCE_MODE` — returned instead of 200 when `maintenance_mode = true` (client still receives the same body as detail so it can render the maintenance screen with an estimated time if known)
  - `426 UPGRADE_REQUIRED` — returned instead of 200 when `X-App-Version < min_supported_version`
  - `422 VALIDATION_ERROR` — missing/malformed `X-App-Version` or `X-Platform` header, or `X-App-Version` is not valid semver
- **Rate Limiting:** 60 req/min/IP via existing `SlidingWindowRateLimiter`.
- **Caching:** `remote_config` object is safe for the client to cache 5 minutes client-side. `session_valid`/`has_children` must never be cached by the client. Server-side, the `RemoteConfigOrm` row is cached in Redis with a 60s TTL to keep the hot path off Postgres on every launch.

## 13. Database Requirements
New table `remote_config` (not present in the current `identity` ER diagram — additive migration only, no destructive change to existing tables):

| Column | Type | Notes |
|---|---|---|
| `config_id` | `uuid` PK | singleton row pattern (always exactly one active row) |
| `min_supported_version` | `varchar` | semver string |
| `recommended_version` | `varchar` | semver string |
| `maintenance_mode` | `boolean` | default `false` |
| `maintenance_estimated_end_at` | `timestamptz` | nullable |
| `consent_version` | `varchar` | pointer to the active consent document version (published via B-09's two-approver workflow) |
| `intro_slides_version` | `varchar` | |
| `otp_health_threshold_pct` | `numeric` | default `95.0` — admin-tunable OTP delivery health alert threshold, added to support B-07/N-02 (resolves what was originally an open "where does this threshold live" question in B-07) |
| `updated_at` | `timestamptz` | |
| `updated_by_admin_id` | `uuid` | FK to admin identity, nullable for seed row |

- This table is **Create/Update only** (no delete) at the application-role grant level — mirrors the "versioned, not destructive" rule stated for Remote Config CRUD permissions in the PRD Admin Requirements.
- Seed migration must insert exactly one row on creation so bootstrap never 500s on an empty table.

## 14. Validation
- `X-App-Version` must parse as valid semver (`MAJOR.MINOR.PATCH`) — reject with `422` if malformed, do not attempt best-effort parsing.
- `X-Platform` must be one of `android`, `ios` — reject unrecognized values with `422`.
- Reject silently-extra/unexpected fields on any future request body extensions (Pydantic strict schema, no request body on this GET today).

## 15. Authentication
- Optional. Uses a **new** `get_optional_parent` dependency (do not reuse `get_current_parent` as-is, since that raises `AuthenticationError` on invalid tokens — bootstrap must degrade to `session_valid: false` instead of failing the whole request).

## 16. Authorization
- No RBAC scope required — this is a public, pre-auth-safe endpoint by design (children/content are still gated behind consent+PIN downstream; bootstrap itself must be callable with zero session).

## 17. Error Handling
| Scenario | Behavior |
|---|---|
| Malformed/missing `X-App-Version` or `X-Platform` | `422 VALIDATION_ERROR`, no partial response |
| `X-App-Version` below `min_supported_version` | `426 UPGRADE_REQUIRED` with the same body as 200 so the client can still render the correct blocking screen with version numbers |
| `maintenance_mode = true` | `503 MAINTENANCE_MODE` |
| Expired/invalid bearer token | Treated as unauthenticated — `session_valid: false`, HTTP 200, never 401 |
| Redis cache unavailable | Fall back to direct Postgres read of `remote_config`; log a warning; do not fail the request |
| Postgres unavailable | Fail fast with `503`; this is the one true hard-fail case — client shows No-Connectivity/retry |

## 18. Localization
- `X-Locale` header is accepted for future use (e.g. localized maintenance messaging) but does not change response shape in this version — do not invent locale-specific fields not in the contract above.

## 19. Analytics
- Emit `bootstrap_completed` with properties `session_valid`, `has_children`, `latency_ms` on every successful resolution.
- Emit `bootstrap_failed` with `error_code` on the maintenance/upgrade/validation/hard-fail paths.
- Both emitted via `OutboxWriter.emit()` inside the request-scoped transaction, consistent with the existing Scenario 2 pattern in the architecture doc (never a direct Celery/event-bus call from the router).

## 20. Performance
- p95 target < 400ms — achieved primarily via the 60s Redis cache on the single `remote_config` row (avoids a Postgres round-trip on the hot path for the vast majority of launches).
- `has_children` lookup must use the existing indexed `(family_id)` index on `ChildProfile` — do not add a full table scan.
- No N+1: session resolution + config lookup + child-count must be at most 2 queries (1 cached config fetch, 1 indexed child-count query), never per-child iteration.

## 21. Security
- Never trust `X-App-Version` for anything beyond the update-gate comparison; it must not be used to bypass any other validation.
- Bootstrap must not leak whether a `family_id` exists for a given token beyond what the token's own claims already authorize (no enumeration surface here — token is already authenticated or not).
- Bearer token parsing reuses the existing JWT verification path (`ParentSessionContext` decode logic) — do not implement a second, parallel JWT decoder.

## 22. Library Requirements
- `semver` (PyPI) or `packaging.version` for server-side version comparison — use a proper library, not manual string splitting (per PRD backend AI-prompt requirement #6).
- No new dependency beyond this; reuse existing `redis`, `sqlalchemy[asyncio]`, `alembic`, `pydantic`.

## 23. Testing
- **Unit (`test_bootstrap_service.py`):**
  - Semver comparison: exactly-at-minimum version (should pass), one-patch-below-minimum (should 426), exactly-at-recommended (no banner needed vs below-recommended banner shown).
  - `has_children` true/false branches.
  - Maintenance-mode short-circuit before version-gate evaluation.
- **Integration (`test_bootstrap_api.py`):**
  - No `Authorization` header → 200, `session_valid: false`.
  - Expired token → 200, `session_valid: false` (never 401).
  - Missing `X-App-Version` → 422.
  - `maintenance_mode = true` seeded → 503.
  - Version below minimum → 426.
  - Redis cache cold vs warm path both return identical payload (cache-correctness test).
  - Rate limit: 61st request within a minute from the same IP → 429.

## 24. Documentation
- Update OpenAPI via existing `export_openapi_schema.py` script after route registration; re-run `classify_openapi_diff.py` to confirm this is a non-breaking additive change.
- Document required env vars for Redis TTL override, if any, in the module README (no secrets, names only).

## 25. AI Coding Agent Implementation Steps

**Task 01 — Create Remote Config Database Model & Migration**
- Objective: Add the `remote_config` singleton table.
- Why Required: No existing table can serve version-gate/maintenance/consent-pointer data.
- Existing Architecture to Follow: SQLAlchemy 2.0 declarative models under `modules/identity/`, `Base`/`TimestampMixin` from `infrastructure/db/base.py`.
- Existing Files to Reuse: `infrastructure/db/base.py::Base`, `TimestampMixin`.
- Files to Create: `src/noorheroes/modules/identity/remote_config_models.py`, `alembic/versions/xxxx_add_remote_config_table.py`.
- Files to Modify: none.
- Implementation Details: Define `RemoteConfigOrm` with columns per §13; Alembic migration includes a data-seed step inserting one default row.
- Business Rules: Table is Create/Update only — no DELETE grant for the application DB role, per PRD Admin Requirements CRUD table.
- Validation: Migration must be idempotent (safe re-run check for existing seed row).
- Error Handling: N/A (migration-time).
- Security: No PII in this table — safe to log freely.
- Performance: Single-row table, no indexing concerns beyond PK.
- Localization/RTL: N/A.
- Analytics: N/A.
- Tests: Migration up/down smoke test in CI.
- Documentation: Add table to module README.
- Dependencies: None.
- Do Not Change: Do not touch `parent`, `family`, `child`, or `consent_record` tables in this migration.
- Expected Result: `remote_config` table exists with exactly one seeded row after migration.
- Definition of Done: Migration runs clean on a fresh DB and on staging snapshot dry-run.

**Task 02 — Create Bootstrap Response & Remote Config Schemas**
- Objective: Define `BootstrapResponse`, `RemoteConfigPayload` Pydantic v2 schemas matching §12 exactly.
- Why Required: Contract-first typing for the router and for OpenAPI generation.
- Existing Architecture to Follow: `common/schemas.py::NoorHeroesBaseModel` (camelCase Pydantic base) — inherit from it, do not redefine base config.
- Existing Files to Reuse: `common/schemas.py`.
- Files to Create: `src/noorheroes/modules/identity/bootstrap_schemas.py`.
- Files to Modify: none.
- Implementation Details: Fields exactly as in §12 response bodies; `remote_config` as a nested model.
- Business Rules: `family_id`/`has_children` must be nullable/false-default when unauthenticated.
- Validation: Pydantic strict mode — reject unexpected fields.
- Error Handling: N/A.
- Security: No sensitive fields exposed (no token internals).
- Performance: N/A.
- Localization/RTL: N/A.
- Analytics: N/A.
- Tests: Schema validation unit tests (missing field, wrong type).
- Documentation: Docstrings per field for OpenAPI description text.
- Dependencies: Task 01 (for field alignment with the model).
- Do Not Change: Do not alter existing `IdentityService` schemas.
- Expected Result: Schemas import cleanly and serialize per the documented JSON shape.
- Definition of Done: `mypy`/pydantic validation passes; OpenAPI shows correct field docs.

**Task 03 — Implement Optional-Auth Dependency**
- Objective: Add `get_optional_parent()` to `core/deps.py` returning `ParentSessionContext | None`.
- Why Required: `get_current_parent` raises on invalid/missing tokens; bootstrap must never hard-fail on an expired token.
- Existing Architecture to Follow: Same JWT decode path as `get_current_parent`, but catch `AuthenticationError` internally and return `None` instead of re-raising.
- Existing Files to Reuse: `core/deps.py::get_current_parent`, `ParentSessionContext`.
- Files to Create: none.
- Files to Modify: `src/noorheroes/core/deps.py`.
- Implementation Details: Wrap existing token-decode call in try/except, log at debug level on failure (not warning/error — an expired token at launch is expected, not anomalous).
- Business Rules: Must not leak *why* the token was invalid to the client.
- Validation: N/A.
- Error Handling: Swallow `AuthenticationError` only; let unrelated exceptions propagate.
- Security: Do not log token contents, even masked, at this layer beyond what the existing decoder already redacts.
- Performance: Same cost as `get_current_parent` (single decode call).
- Localization/RTL: N/A.
- Analytics: N/A.
- Tests: Unit test — valid token, expired token, malformed token, no token — all four paths.
- Documentation: Docstring explaining why this differs from `get_current_parent`.
- Dependencies: none.
- Do Not Change: Do not modify `get_current_parent`'s existing raising behavior — other routes depend on it raising.
- Expected Result: New dependency available for bootstrap only (not swapped in elsewhere without review).
- Definition of Done: All four auth-path unit tests pass.

**Task 04 — Implement RemoteConfigRepository**
- Objective: `RemoteConfigRepository(BaseRepository[RemoteConfigOrm])` with `get_active_config()`.
- Why Required: Data-access layer for the singleton config row, shared by B-01 (read) and B-09 (write).
- Existing Architecture to Follow: `common/base_repository.py::BaseRepository` generic CRUD pattern.
- Existing Files to Reuse: `BaseRepository`.
- Files to Create: `src/noorheroes/modules/identity/remote_config_repository.py`.
- Files to Modify: none.
- Implementation Details: `get_active_config()` returns the single row (raise `NotFoundError` only if the seed migration somehow didn't run — should be treated as a deploy-config bug, not a normal runtime path).
- Business Rules: Repository must not expose an update/delete method here — write path belongs to B-09's repository method, kept separate to enforce the read/write RBAC split at the code-review level.
- Validation: N/A (delegated to schema layer).
- Error Handling: `NotFoundError` on missing seed row.
- Security: N/A.
- Performance: Single indexed PK read.
- Localization/RTL: N/A.
- Analytics: N/A.
- Tests: Unit test for found/not-found paths.
- Documentation: Docstring.
- Dependencies: Task 01.
- Do Not Change: Do not add write methods here.
- Expected Result: Repository returns the current config row reliably.
- Definition of Done: Unit tests green.

**Task 05 — Implement Semver Comparison Utility**
- Objective: `compare_versions(client_version, min_version, recommended_version) -> UpdateGateResult`.
- Why Required: PRD explicitly requires a proper semver library, server-side only comparison (backend AI-prompt requirement #6).
- Existing Architecture to Follow: Pure function in `common/utils/`, mirrors existing `common/utils/age_band.py` style (pure, side-effect-free, unit-testable in isolation).
- Existing Files to Reuse: `common/utils/` package pattern.
- Files to Create: `src/noorheroes/common/utils/semver_compare.py`.
- Files to Modify: none.
- Implementation Details: Use `semver` library; return a small result object/enum: `OK`, `RECOMMENDED_AVAILABLE`, `FORCED_UPDATE_REQUIRED`; raise `ValidationError` on unparseable input version.
- Business Rules: Below-minimum → forced; below-recommended but above-minimum → recommended banner only; at/above recommended → OK.
- Validation: Reject non-semver strings with `ValidationError`, not a silent fallback.
- Error Handling: Propagate `ValidationError` up to router → `422`.
- Security: N/A.
- Performance: O(1), negligible cost.
- Localization/RTL: N/A.
- Analytics: N/A.
- Tests: Table-driven unit tests for all three gate outcomes plus malformed-version case.
- Documentation: Docstring with examples.
- Dependencies: none.
- Do Not Change: N/A.
- Expected Result: Deterministic, correct gate classification for all boundary versions.
- Definition of Done: 100% branch coverage on this function.

**Task 06 — Implement BootstrapService**
- Objective: Orchestrate session resolution, child lookup, version gate, maintenance check, and Redis-cached config read into a single `BootstrapResponse`.
- Why Required: This is the core business logic the router delegates to, per the mandatory Router→Service→Repository layering.
- Existing Architecture to Follow: `BaseService` subclass; `OutboxWriter.emit()` for analytics events inside the same request-scoped transaction.
- Existing Files to Reuse: `BaseService`, `OutboxWriter`, `get_redis_pool`.
- Files to Create: `src/noorheroes/modules/identity/bootstrap_service.py`.
- Files to Modify: none.
- Implementation Details: `resolve_bootstrap(parent_ctx: ParentSessionContext | None, app_version: str, platform: str) -> BootstrapResponse`; cache-aside pattern against Redis (60s TTL) wrapping `RemoteConfigRepository.get_active_config()`; raises the appropriate `DomainError` subclass for the router to map to `426`/`503`/`422`.
- Business Rules: Maintenance-mode check happens before version-gate check (maintenance takes precedence per PRD error-code ordering: `503 MAINTENANCE_MODE`, `426 UPGRADE_REQUIRED`).
- Validation: Delegates to Task 05 for version parsing.
- Error Handling: Falls back to direct Postgres read on Redis failure (log warning, do not fail request); hard-fails only on Postgres failure.
- Security: No token internals in emitted analytics events.
- Performance: Target p95 < 400ms — verify with a load test after implementation (see Task 12).
- Localization/RTL: N/A.
- Analytics: Emits `bootstrap_completed`/`bootstrap_failed` via `OutboxWriter`.
- Tests: Full unit coverage per §23.
- Documentation: Docstring covering the maintenance-before-version-gate precedence rule explicitly (easy to get backwards).
- Dependencies: Tasks 01, 03, 04, 05.
- Do Not Change: Do not fold this logic into `IdentityService` — keep it a separate service class for clarity, both registered under the same `identity` module.
- Expected Result: Single method returns a fully-assembled, correct `BootstrapResponse` (or raises the correct `DomainError`) for every scenario in §23.
- Definition of Done: All unit tests pass; maintenance-before-upgrade precedence explicitly tested.

**Task 07 — Implement GET /v1/identity/bootstrap Router Endpoint**
- Objective: Wire the HTTP route.
- Why Required: Public entry point for the feature.
- Existing Architecture to Follow: `modules/identity/api.py::IdentityRouter` pattern, `openapi_extra` security declarations per `FAST-API-INSTRUCTIONS.md` §10.
- Existing Files to Reuse: `IdentityRouter`.
- Files to Create: none.
- Files to Modify: `src/noorheroes/modules/identity/api.py`, `src/noorheroes/core/deps.py` (add `get_bootstrap_service` factory).
- Implementation Details: `Annotated[ParentSessionContext | None, Depends(get_optional_parent)]`; required `X-App-Version`/`X-Platform` headers via `Header(...)`; map `DomainError` subclasses raised by the service to `426`/`503`/`422` HTTP responses (reuse the existing global exception-handler pattern — do not `try/except` inside the router itself; confirm the app-level handler already maps these).
- Business Rules: No DB query directly in the router (per Layer Rule #1 in the architecture doc) — router only calls the service.
- Validation: FastAPI header validation for required headers.
- Error Handling: Delegated to global exception handlers.
- Security: `openapi_extra={"security": []}` (explicitly public — do not mark `BearerAuth` as required).
- Performance: No blocking calls in the router itself.
- Localization/RTL: N/A.
- Analytics: N/A (handled in service).
- Tests: Covered by Task 12 (API-level integration tests).
- Documentation: `summary`/`description` per the existing endpoint doc style (see `create_child` example in the architecture doc §10).
- Dependencies: Task 06.
- Do Not Change: Do not add a DB session dependency directly to this router function.
- Expected Result: `GET /v1/identity/bootstrap` live and documented.
- Definition of Done: Manual curl/Swagger UI check returns the documented shape for both authed and unauthed calls.

**Task 08 — Add Rate Limiting Configuration**
- Objective: Apply 60 req/min/IP to this route.
- Why Required: Cheap but public endpoint — protect against abuse without hurting legitimate launch traffic.
- Existing Architecture to Follow: `RateLimitMiddleware`/`SlidingWindowRateLimiter` existing Redis-backed config pattern.
- Existing Files to Reuse: `infrastructure/middleware/rate_limit.py`.
- Files to Modify: rate-limit config registration (wherever existing per-route limits are declared — follow existing convention, do not hardcode a new middleware instance).
- Implementation Details: 60/min/IP as specified in §12.
- Business Rules: Must not rate-limit by `family_id` (endpoint is often called unauthenticated).
- Validation: N/A.
- Error Handling: `429` on breach (existing middleware behavior).
- Security: Protects against launch-storm/scripted abuse.
- Performance: Redis-backed, sub-millisecond overhead.
- Localization/RTL: N/A.
- Analytics: N/A.
- Tests: Integration test — 61st request in a minute returns 429.
- Documentation: Note the limit in the endpoint's OpenAPI description.
- Dependencies: Task 07.
- Do Not Change: Do not alter rate limits on other existing routes.
- Expected Result: Confirmed 429 behavior under load test.
- Definition of Done: Rate-limit integration test passes.

**Task 09 — Add Structured Logging & Outbox Analytics Events**
- Objective: Emit `bootstrap_completed`/`bootstrap_failed`.
- Why Required: Feeds the Onboarding Funnel Dashboard (N-01/B-07) — this is the first event in the funnel.
- Existing Architecture to Follow: `OutboxWriter.emit()` inside the active transaction (see Scenario 2/6 patterns in architecture doc).
- Existing Files to Reuse: `OutboxWriter`.
- Files to Modify: `bootstrap_service.py` (already covered in Task 06 — this task is the explicit verification pass).
- Implementation Details: Event envelope `event_name, family_id, parent_id, child_id, timestamp, properties` per PRD backend AI-prompt requirement #9; properties = `session_valid, has_children, latency_ms` (success) or `error_code` (failure).
- Business Rules: Every request path (success, 426, 503, 422) must emit exactly one event — no double-emission, no silent drops.
- Validation: N/A.
- Error Handling: N/A.
- Security: No PII in event properties.
- Performance: Async outbox write, does not block the response.
- Localization/RTL: N/A.
- Analytics: This task's entire purpose.
- Tests: Integration test asserting exactly one outbox row per request across all four response-code paths.
- Documentation: List the two events in the module README's event taxonomy section.
- Dependencies: Task 06.
- Do Not Change: Do not emit directly to Kafka/event bus from the service — always through `OutboxWriter` to preserve the transactional-outbox guarantee.
- Expected Result: Every bootstrap call produces exactly one analytics event.
- Definition of Done: Integration test confirms 1:1 request-to-event ratio across all paths.

**Task 10 — Add Unit Tests**
- Objective: Full unit coverage of `BootstrapService` and `compare_versions`.
- Why Required: Section 23 mandates this.
- Files to Create: `tests/modules/identity/test_bootstrap_service.py`, plus a unit test file for `semver_compare.py`.
- Implementation Details: All cases in §23 "Unit" bullet list.
- Dependencies: Tasks 05, 06.
- Expected Result / Definition of Done: All listed cases pass; branch coverage on the maintenance/version-gate precedence logic.

**Task 11 — Add Integration Tests**
- Objective: Full API-level coverage per §23 "Integration" bullet list.
- Files to Create: `tests/modules/identity/test_bootstrap_api.py`.
- Implementation Details: Spin up test client against a seeded test DB + test Redis; cover all cases in §23.
- Dependencies: Tasks 07, 08, 09.
- Expected Result / Definition of Done: All listed integration cases pass in CI.

**Task 12 — Update OpenAPI Documentation & Verify Non-Breaking**
- Objective: Regenerate `openapi.json`, run `classify_openapi_diff.py`.
- Files to Modify: none (generated artifact).
- Implementation Details: Run `python -m src.noorheroes.scripts.export_openapi_schema`, then the diff classifier against the baseline; confirm the diff is classified as additive/non-breaking.
- Dependencies: Task 07.
- Expected Result / Definition of Done: Diff classifier reports no breaking changes.

**Task 13 — Final Code Review**
- Objective: Verify layering rules (§11 of `FAST-API-INSTRUCTIONS.md`) were followed — no DB access in the router, no manual commits in service/repository, no naked exceptions.
- Dependencies: All prior tasks.
- Expected Result / Definition of Done: Review checklist (§26 below) fully checked.

## 26. Final Verification Checklist
- [ ] `remote_config` table created via additive-only migration, seeded with exactly one row
- [ ] No UPDATE/DELETE grant issue introduced (this table is app-writable via B-09, unlike `consent_record` — confirm this distinction is correct and intentional)
- [ ] `get_optional_parent` never raises on invalid/expired token
- [ ] Router contains zero direct DB/session calls
- [ ] Service contains zero `session.commit()` calls
- [ ] All errors raised as `DomainError` subclasses, never naked `HTTPException`
- [ ] Version comparison uses the `semver` library, not manual string parsing
- [ ] Maintenance-mode check precedes version-gate check
- [ ] `session_valid`/`has_children` never cached; `remote_config` cached both server-side (Redis, 60s) and documented as client-cacheable (5 min)
- [ ] Rate limit (60/min/IP) verified via test
- [ ] `bootstrap_completed`/`bootstrap_failed` emitted exactly once per request across all paths
- [ ] p95 latency measured < 400ms in load test
- [ ] Unit + integration test suites green in CI
- [ ] OpenAPI diff confirmed non-breaking
- [ ] No changes made to `parent`, `family`, `child`, `consent_record`, or any unrelated table/module
- [ ] No PostgreSQL/Redis credentials modified anywhere in this change

## 27. Definition of Done
`GET /v1/identity/bootstrap` is live, documented, rate-limited, cached, fully tested (unit + integration), emits correct funnel-analytics events, respects the maintenance-before-upgrade precedence rule, never hard-fails on an invalid token, and its migration is additive-only against the existing `identity` schema. K-01 (KMP Splash/Bootstrap flow) and B-07/N-01 (Onboarding Funnel Dashboard) can now be built against this contract without further backend changes.
