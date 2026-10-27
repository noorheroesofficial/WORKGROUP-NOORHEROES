# B-02 — Usage Heartbeat & Server-Authoritative Enforcement Engine

## 1. Feature Context
This is the single most security-critical sub-feature in Parental Controls: the guarantee that device-clock manipulation can never extend a child's usage time, and that usage across multiple devices reconciles into one authoritative daily total (PRD C.23 FR-3, FR-4, §5 Backend AI Code-Generation Prompt items 1–2, 4, 7).

## 2. Parent Feature
Feature C.23 — Parental Controls (Screen Time, Bedtime, AI Permissions, Content Age Level)

## 3. Sub-feature
1.2 Usage Heartbeat & Server-Authoritative Enforcement Engine (ID: **B-02**)

## 4. Objective
Implement `POST /v1/children/{id}/usage-heartbeats`, computing elapsed foreground time exclusively from server-received timestamp deltas, maintaining a single authoritative `screen_time_usage_daily` row per child per day (`UNIQUE(child_id, local_date)`), evaluating limit/bedtime/warning state, and issuing a signed, expiring policy token for bounded offline enforcement.

## 5. Business Requirements
- FR-3 (hard, zero-exception): server-time-only accounting; device clock manipulation never resets usage counters; multi-device usage reconciled server-side.
- FR-4 (hard): offline mode enforces the last signed policy rather than allowing unlimited use when disconnected.
- FR-2 items 2–5: foreground-only increment; warning threshold notification; graceful finish at limit (client-driven, not server-forced); bedtime cutoff at content boundary.
- FR-5: bedtime stop never mid-word in an active Quran lesson (this API surfaces the state; client owns the graceful-stop mechanics — see K-08).
- Edge Case 4: offline beyond signed grace period fails closed to most conservative state.
- Edge Case 9: device revoked mid-in-flight-request — already-authenticated request completes.
- NFR: server-time-only accounting and cross-device reconciliation are the two highest-priority guarantees in this entire service (per PRD §5).

## 6. Existing Architecture
Lives in `modules/restrictions`, alongside B-01. Reuses `policy_logic.py::is_within_bedtime_window` from B-01. Uses Redis (`infrastructure/redis.py::get_redis_pool`) for fast-path counter increments, periodically synced to PostgreSQL, given this is the platform's highest-frequency child-mode API call (fired every 30–60s per active child session across the entire base).

## 7. Existing Code to Reuse
- `modules/restrictions/policy_logic.py::is_within_bedtime_window` (from B-01)
- `modules/restrictions/repository.py::ScreenTimePolicyRepository` (from B-01, read-only here)
- `infrastructure/redis.py::get_redis_pool`
- `core/deps.py::get_current_child`
- `common/utils/clock.py::Clock` / `SystemClock` (server time source — never client-supplied)
- `core/security.py` patterns for signed-token minting (JWT-style signing, reused conceptually for the offline policy token)

## 8. Files to Create
- `src/noorheroes/modules/restrictions/usage_models.py` — `ScreenTimeUsageDailyOrm`
- `src/noorheroes/modules/restrictions/usage_schemas.py` — `HeartbeatRequest`, `HeartbeatResponse`
- `src/noorheroes/modules/restrictions/usage_repository.py` — `ScreenTimeUsageRepository`
- `src/noorheroes/modules/restrictions/enforcement_service.py` — `RestrictionEnforcementService(BaseService)`
- `src/noorheroes/modules/restrictions/policy_token.py` — signed offline-policy token minting/verification
- `alembic/versions/xxxx_create_screen_time_usage_daily.py`
- `tests/modules/restrictions/test_enforcement_service.py`
- `tests/modules/restrictions/test_heartbeat_api.py`
- `tests/modules/restrictions/test_policy_token.py`

## 9. Files to Modify
- `src/noorheroes/modules/restrictions/api.py` — add `POST /v1/children/{id}/usage-heartbeats`
- `src/noorheroes/modules/restrictions/deps.py` — add `get_enforcement_service`

## 10. Backend Requirements
- `RestrictionEnforcementService.process_heartbeat(child_id, child_ctx, payload)`:
  1. Verify `child_ctx.child_id == child_id` (session-scoped, no cross-child heartbeat submission).
  2. Compute `local_date` via server clock (`Clock.now()`), not client-supplied date.
  3. Compute elapsed seconds using the **server's own received-timestamp delta** between this heartbeat and the last recorded heartbeat timestamp for this `child_id` (stored server-side, e.g., in Redis), completely ignoring `client_timestamp` for the calculation — `client_timestamp` is persisted only in a diagnostic log field.
  4. Redis fast-path: `INCRBY` a per-`child_id`-per-`local_date` counter key; periodically flush to `screen_time_usage_daily` (e.g., every N increments or T seconds) via a background sync task.
  5. Upsert into `screen_time_usage_daily` using `INSERT ... ON CONFLICT (child_id, local_date) DO UPDATE` to guarantee the single authoritative row regardless of which device's heartbeat triggered it.
  6. Load policy via `ScreenTimePolicyRepository.get_by_child_id`; compute `minutes_remaining`, `warning_threshold_crossed`, `limit_reached`.
  7. Compute `bedtime_active` via `is_within_bedtime_window`.
  8. Mint/refresh a signed offline-policy token (short expiry, e.g., grace window per platform config) included in the response for local caching.
  9. Return response shape sufficient for the client to make its own graceful-finish decision — the server never issues a forced-kill signal.
- Background Celery-style periodic task (or async task) flushing Redis counters to PostgreSQL — document as `sync_usage_counters_task` for ops visibility (implementation detail: reuse the platform's existing Celery infra from `localization` context as the pattern reference).
- `policy_token.py`: sign `{ child_id, policy_snapshot, issued_at, expires_at }` using the existing JWT signing key infra (`core/security.py`); `verify_and_check_expiry(token) -> (valid: bool, expired: bool)`.

## 11. API Contract

### `POST /v1/children/{id}/usage-heartbeats`
- **Auth:** Bearer (child-mode, `get_current_child`)
- **Request:** `{ "foreground_seconds_since_last_heartbeat": 30, "client_timestamp": "2026-08-17T10:00:00Z" }` (`client_timestamp` logged for diagnostics only)
- **Response 200:** `{ "minutes_used_today": 22, "minutes_remaining": 23, "limit_reached": false, "warning_threshold_crossed": false, "bedtime_active": false, "signed_policy_token": "...", "policy_token_expires_at": "..." }`
- **Error Responses:** `401 UNAUTHORIZED`, `404 CHILD_NOT_FOUND`, `422 VALIDATION_ERROR` (negative/absurd elapsed seconds), `500 INTERNAL_ERROR`

## 12. Database Requirements
`screen_time_usage_daily`: `child_id UUID FK`, `local_date DATE`, `minutes_used INT DEFAULT 0`, `UNIQUE(child_id, local_date)`, index `(child_id, local_date DESC)`. Retained for historical trend display (feeds C.22).

## 13. Validation
- `foreground_seconds_since_last_heartbeat`: integer, `0 <= value <= 120` (sane upper bound per heartbeat interval — reject implausible single-heartbeat jumps as a tamper signal, log for security monitoring rather than silently accepting).
- `client_timestamp`: accepted as any ISO-8601 string; never used in the increment calculation.

## 14. Authentication
`Depends(get_current_child)` — child-mode session token required.

## 15. Authorization
`child_ctx.child_id` must match the path `{id}` — no heartbeat submission for a different child even within the same family.

## 16. Error Handling
| Scenario | System Behavior |
|---|---|
| Device clock manipulated (client_timestamp skewed) | Ignored entirely for calculation; server-side delta used |
| Implausible elapsed-seconds value | Rejected 422, logged as potential tamper signal |
| Redis unavailable | Fall back to direct PostgreSQL upsert (degraded-but-correct path), alert ops |
| Two devices heartbeat concurrently | Both increment the same `(child_id, local_date)` row via `ON CONFLICT DO UPDATE`, no double-counting |
| Offline grace token expired | Client (K-07) fails closed; this API simply issues tokens with correct expiry on next contact |

## 17. Offline First
This API is the **source of truth** the offline client (K-07) caches against. It has no offline mode itself (child device must be online to heartbeat); its role is to produce the signed policy token that enables bounded offline enforcement client-side.

## 18. Local Data
N/A (backend) — token consumed by KMP `:core:restriction-engine`.

## 19. Localization
N/A — numeric/boolean payload only.

## 20. RTL
N/A.

## 21. Analytics
Backing data source for `restriction_warning_notification_fired`, `restriction_limit_reached`, `restriction_bedtime_block_shown` events (fired client-side based on this response, per K-08).

## 22. Performance
Highest-frequency child-mode endpoint platform-wide. Redis fast-path increment is mandatory, not optional, to avoid a synchronous PostgreSQL write per heartbeat. Async/non-blocking throughout. Monitor p99 latency as a CI/ops gate.

## 23. Security
This endpoint is the platform's primary defense surface against tamper attempts. Server-time-only accounting eliminates client-clock manipulation as an attack vector entirely (the dangerous capability simply isn't representable). Signed policy tokens prevent offline-client policy forgery.

## 24. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Redis (`redis.asyncio`), existing JWT signing utilities from `core/security.py`. No new third-party dependencies.

## 25. Testing
- Unit: simulated client with rolled-back/forward `client_timestamp` — confirm `minutes_used_today` computed entirely from server-side timing.
- Unit: two simulated device sessions heartbeat the same child/day — confirm single combined counter, not two independent totals.
- Unit: midnight-crossing bedtime evaluated correctly (reuse B-01's test matrix via shared `policy_logic.py`).
- Unit: signed policy token expiry — confirm an expired token is flagged as such on verification.
- Unit: response shape carries enough info for graceful client-side finish (no forced-kill field).
- Integration: full heartbeat sequence from below-limit → warning-crossed → limit-reached.
- Load test: sustained heartbeat volume simulating platform-scale concurrent active sessions.
- **CI-blocking gate**: server-time-only accounting test and cross-device reconciliation test must pass on every deploy touching this file.

## 26. Documentation
OpenAPI description must explicitly state that `client_timestamp` is diagnostic-only and never used for the actual increment — this is the platform's most important documented guarantee in this feature.

## 27. AI Coding Agent Implementation Steps

**Task 01 — Create `ScreenTimeUsageDailyOrm` Model**
- Files to Create: `src/noorheroes/modules/restrictions/usage_models.py`
- Implementation Details: `child_id FK`, `local_date DATE`, `minutes_used INT`, `UNIQUE(child_id, local_date)`.

**Task 02 — Create Migration**
- Files to Create: `alembic/versions/xxxx_create_screen_time_usage_daily.py`
- Implementation Details: unique constraint + composite index `(child_id, local_date DESC)`.

**Task 03 — Create Heartbeat Request/Response Schemas**
- Files to Create: `src/noorheroes/modules/restrictions/usage_schemas.py`
- Validation: bound `foreground_seconds_since_last_heartbeat` to a sane range.

**Task 04 — Implement `ScreenTimeUsageRepository`**
- Files to Create: `src/noorheroes/modules/restrictions/usage_repository.py`
- Implementation Details: `upsert_increment(child_id, local_date, delta_minutes)` using `INSERT ... ON CONFLICT DO UPDATE`.

**Task 05 — Implement Redis Fast-Path Counter Layer**
- Objective: Avoid synchronous PostgreSQL write per heartbeat given call volume.
- Implementation Details: Redis key pattern `usage:{child_id}:{local_date}`, `INCRBY` semantics, periodic flush task.
- Why This Is Required: PRD DevOps §10 explicitly calls out this endpoint as the platform's highest-volume call.

**Task 06 — Implement `policy_token.py` Signed Token Module**
- Objective: Mint/verify signed offline-policy tokens with expiry.
- Implementation Details: Reuse existing JWT signing key infra from `core/security.py`; do not invent a new signing mechanism.
- Tests: token expiry correctly flagged.

**Task 07 — Implement `RestrictionEnforcementService.process_heartbeat`**
- Objective: Core business logic per §10.
- Dependencies: Tasks 04, 05, 06, and B-01's `policy_logic.py`.
- Implementation Details: Server-time-only delta computation is the critical path — write this first and test it in isolation before wiring the rest.

**Task 08 — Implement API Endpoint**
- Files to Modify: `src/noorheroes/modules/restrictions/api.py`, `deps.py`
- Implementation Details: `Depends(get_current_child)`, no DB access in router.

**Task 09 — Add Server-Time-Only Accounting Test (CI-Blocking)**
- Objective: The single highest-priority test in this entire feature.
- Files to Create: `tests/modules/restrictions/test_enforcement_service.py`
- Implementation Details: Simulate manipulated `client_timestamp`; assert computed usage unaffected.

**Task 10 — Add Cross-Device Reconciliation Test (CI-Blocking)**
- Objective: Second-highest-priority test.
- Implementation Details: Simulate two concurrent device heartbeat streams for the same child/day; assert single correct combined total.

**Task 11 — Add Remaining Test Coverage**
- Files to Create: `tests/modules/restrictions/test_heartbeat_api.py`, `tests/modules/restrictions/test_policy_token.py`
- Coverage: midnight-crossing, warning threshold, limit-reached response shape, offline token expiry.

**Task 12 — Add Monitoring/Alerting Hooks**
- Objective: Latency/error-rate alerting given call volume (ops requirement, coordinate with DevOps).
- Implementation Details: Emit Prometheus metrics via existing telemetry infra.

**Task 13 — Add API Documentation**
- Objective: Document server-time-only guarantee explicitly in OpenAPI description.

**Task 14 — Final Code Review**
- Objective: Confirm Redis fast-path doesn't risk silent data loss on crash (flush-on-shutdown or acceptable bounded-loss window documented); confirm no `client_timestamp` value is used anywhere in arithmetic.

## 28. Definition of Done
- Server-time-only accounting test passes and is wired as a CI-blocking gate.
- Cross-device reconciliation test passes and is wired as a CI-blocking gate.
- Midnight-crossing bedtime evaluation reuses and passes B-01's test matrix.
- Signed policy token issuance/expiry verified.
- Load test confirms acceptable p99 latency at simulated platform scale.

## 29. Final Verification Checklist
- [ ] `client_timestamp` never appears in any increment/delta calculation (code-review confirmed, not just tested)
- [ ] `UNIQUE(child_id, local_date)` constraint enforced at DB level, not just application level
- [ ] Redis fast-path implemented with documented flush strategy
- [ ] Signed policy token expiry correctly enforced
- [ ] Response never includes a server-forced "kill" signal — only state for client-driven graceful finish
- [ ] CI pipeline has server-time-only and cross-device tests marked as blocking
- [ ] Load/performance test results documented
- [ ] OpenAPI documentation explicitly states the server-time-only guarantee
