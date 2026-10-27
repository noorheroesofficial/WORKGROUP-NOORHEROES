# B-01 — Bedtime Configuration API

> **Status: Implemented & Verified (2026-09-06)** — fully implemented in `src/noorheroes/modules/bedtime/` with migration `0038_add_bedtime_config.py`, database-level CHECK constraint (5–120), atomic dialect-aware upsert repository, safe-default fallback GET evaluation, strict parent-only write gate, midnight-crossing time range logic, transactional outbox events (`parent_bedtime_window_configured`, `parent_sleep_timer_ceiling_configured`), 4-language i18n catalogs (`en`, `hi`, `ur`, `ar`), and 79 passing tests across `tests/modules/bedtime/` + 11 transactional outbox tests (90 passing tests total).

## 1. Feature Context
The single source of truth for a child's parent-configured bedtime window and sleep-timer ceiling. Read by the Bedtime Audio Player (K-01/K-07) and the general Story Player's Bedtime Mode overlay (A.3/K-05) to decide whether to auto-apply calm visuals, and by the Sleep Timer Reliability Engine (K-02) to bound the child's selectable timer durations. Must fail safe (never force Bedtime Mode) if unreachable, and must correctly evaluate midnight-crossing windows (e.g., 20:00–07:00).

## 2. Parent Feature
Feature A.4 — Audio Bedtime Player & Bedtime Mode

## 3. Sub-feature
1.1 Bedtime Configuration API (ID: **B-01**)

## 4. Objective
Build a new `bedtime` bounded context (`BedtimeConfigOrm`, `BedtimeConfigRepository`, `BedtimeConfigService`, `BedtimeRouter`) exposing `GET/PUT /v1/parent-controls/{child_id}/bedtime`, deployed as a module within the existing Content & Playback Service rather than a standalone microservice, following the same Router → Service → Repository → Postgres layering used across the codebase (mirrors A.3's `content` module conventions).

## 5. Business Requirements
- FR-3: Sleep Timer ceiling is parent-configurable (bounded range); child freely chooses up to the ceiling.
- FR-12: Parent configures bedtime window start/end per child, sleep-timer max ceiling, auto-suggest/auto-start preference, and Bedtime Ritual indicator visibility.
- FR-13: Entering Bedtime Mode never requires re-authentication/PIN — this is a content-context state, not a security boundary.
- §3.4: `window_end` may be numerically "before" `window_start` (midnight-crossing) — this is valid input, not an error.
- §1.11 Error Handling: if config fetch fails, the player must default to NOT forcing Bedtime Mode (fail safe), never crash or block the Calm Mode toggle.
- Edge Case 4: window changes apply at next session, not mid-session (client-side caching rule, documented here as the API's caching contract).

## 6. Existing Architecture
No existing `bedtime` module exists in the FastAPI codebase. Per `FAST-API-INSTRUCTIONS.md`, new bounded contexts follow the established `modules/<context>/{models,schemas,repository,service,api}.py` layout, `BaseRepository`/`BaseService` inheritance, `core/deps.py` auth dependencies (`get_current_child`, `get_current_parent`), and `common/base_service.py` exception conventions already used by the `content` module (A.3/B-01). This sub-feature introduces the `bedtime` module using those exact same conventions — no parallel architecture.

## 7. Existing Code to Reuse
- `core/deps.py::get_current_child`, `get_current_parent` (parent-vs-child session distinction, same pattern as A.3/B-11's admin-vs-child gating)
- `common/base_service.py`, `common/base_repository.py`
- `core/exceptions.py` (`NotFoundError`, `ValidationError`)
- `infrastructure/db.py::Base`, `TimestampMixin` (from `modules/content/models.py`)
- `modules/content/api.py::ContentRouter` — as the structural template for router file layout (not imported, mirrored)

## 8. Files Created
- `src/noorheroes/modules/bedtime/models.py` — `BedtimeConfigOrm` (PK/FK `child_id`, `window_start: Time`, `window_end: Time`, `sleep_timer_ceiling_minutes: int`, `allow_until_episode_ends_option: bool`, `auto_suggest_download: bool`, `updated_at`)
- `alembic/versions/0038_add_bedtime_config.py` — includes DB-level `CHECK (sleep_timer_ceiling_minutes BETWEEN 5 AND 120)`
- `src/noorheroes/modules/bedtime/schemas.py` — `BedtimeConfigResponse`, `BedtimeConfigUpdateRequest`
- `src/noorheroes/modules/bedtime/repository.py` — `BedtimeConfigRepository` (extends `BaseRepository`)
- `src/noorheroes/modules/bedtime/service.py` — `BedtimeConfigService` (`get_config()`, `upsert_config()`, `is_within_window(now, config)` pure helper)
- `src/noorheroes/modules/bedtime/api.py` — `BedtimeRouter`
- `src/noorheroes/modules/bedtime/events.py` — `ParentBedtimeWindowConfiguredEvent`, `ParentSleepTimerCeilingConfiguredEvent`
- `src/noorheroes/modules/bedtime/README.md` — Canonical bounded context documentation
- `tests/modules/bedtime/test_bedtime_config_service.py`
- `tests/modules/bedtime/test_bedtime_config_api.py`
- `tests/modules/bedtime/test_bedtime_config_sqlite_integration.py`

## 9. Files Modified
- `src/noorheroes/api/v1/router.py` — register `BedtimeRouter` mounted alongside existing module routers
- `src/noorheroes/common/outbox_relay.py` — register `bedtime` domain events in outbox relay dispatch table
- `src/noorheroes/core/exceptions.py` — register `InvalidTimeRangeError` and `BedtimeConfigNotFoundError`
- `src/noorheroes/core/i18n.py` — add localized error messages across `en`, `hi`, `ur`, `ar`
- `alembic/env.py` — register `BedtimeConfigOrm` in target metadata
- `FAST-API-INSTRUCTIONS.md` — register `bedtime` bounded context across §5.13, §6, §7, §8, §9, §15
- `MASTER-README.md` — register `bedtime` bounded context across §1, §6, §9, §10, §11.27, §12
- `docs/TESTING.md` — register `tests/modules/bedtime/` suite in §2, §3, §4.7
- `artifacts/openapi.json` — export OpenAPI 3.1.0 schema with bedtime endpoints (0 breaking changes)

## 10. Backend Requirements
- `get_config(child_id, requester_ctx)`: child-mode sessions may only read their own `child_id`'s config; parent sessions may read any child in their family.
- `upsert_config(child_id, payload, requester_ctx)`: parent-session only; upserts (not inserts) — one row per child, created on first write.
- `is_within_window(now, config)`: pure function correctly evaluating both same-day windows (e.g., 14:00–16:00) and midnight-crossing windows (e.g., 20:00–07:00) — `now` between `window_start` and `window_end` accounting for the crossing case via `window_start > window_end` branch logic.
- Missing config row: `get_config()` returns a sensible safe-default response (`window_start: null`, `window_end: null`, i.e., "no auto-applied window configured") with `200`, never `404`/`500`.
- No business logic in `api.py`; no direct DB access in `service.py` (routed through `repository.py`).

## 11. API Contract

### `GET /v1/parent-controls/{child_id}/bedtime`
- Auth: Bearer (child-mode may read own config; parent-mode may read any child in-family).
- Response 200: `{ "window_start": "20:00"|null, "window_end": "07:00"|null, "sleep_timer_ceiling_minutes": 30, "allow_until_episode_ends_option": true, "auto_suggest_download": true, "updated_at": "..." }` — null window fields for an unconfigured child, not an error.
- Errors: `401 UNAUTHORIZED`, `403 FORBIDDEN` (child requesting another child's config, or parent outside the family).
- Caching: client caches 5–15 min; server sets `Cache-Control` accordingly.

### `PUT /v1/parent-controls/{child_id}/bedtime`
- Auth: Bearer (parent-session only).
- Request: same shape as response (minus `updated_at`).
- Validation: `window_end` numerically earlier than `window_start` is VALID (midnight-crossing); `sleep_timer_ceiling_minutes` must be 5–120.
- Errors: `401 UNAUTHORIZED`, `403 FORBIDDEN` (non-parent session, or child-mode token), `422 INVALID_TIME_RANGE` (only for genuinely malformed input, e.g., non-time strings — never for a valid midnight-crossing pair).

## 12. Database Requirements
- `bedtime_config`: PK = FK `child_id` (one row per child, upserted); `CHECK (sleep_timer_ceiling_minutes BETWEEN 5 AND 120)` enforced at the migration level.
- No independent deletion lifecycle — cascades only via the global account-deletion cascade already defined elsewhere in the schema (confirm existing cascade convention on the `Child` table and mirror it, do not invent a new cascade rule).
- No index required beyond the PK (single-row-per-child lookups only).

## 13. Validation
- `window_start`/`window_end`: valid `HH:MM` time values; equal start/end treated as "no window configured" (reject or normalize — confirmed behavior: treat as `422 INVALID_TIME_RANGE`, since a zero-length window is not meaningful).
- `sleep_timer_ceiling_minutes`: integer 5–120, both at Pydantic schema level and DB CHECK level (defense in depth).
- Pydantic strict schemas reject unexpected extra fields.

## 14. Authentication
Both endpoints require a valid Bearer token via `get_current_child`/`get_current_parent`, matching the exact dependency pattern already used across the codebase — no new auth mechanism.

## 15. Authorization
- `GET`: child-mode token scoped to its own `child_id` only; parent-mode token scoped to children within their family (reuse existing family-membership check, do not duplicate it).
- `PUT`: parent-mode token only; a child-mode token attempting `PUT` is rejected with `403 FORBIDDEN` regardless of claimed `child_id`.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| No config row exists yet | `200` with safe-default (no auto-applied window) response |
| Child-mode token attempts `PUT` | `403 FORBIDDEN` |
| Parent requests a child outside their family | `403 FORBIDDEN` |
| Malformed time string | `422 INVALID_TIME_RANGE` |
| Midnight-crossing window submitted | Accepted as valid — `200` |
| Database failure | `503`, structured error, logged with correlation ID |

## 17. Security
- Parent-only write access is the sole access-control property of this endpoint (per §12.1/§12.2 of the PRD) — must be verified via an explicit penetration-style test attempting `PUT` with a child-mode token.
- No PII beyond `child_id` (already an authenticated-scope identifier elsewhere in the system) is stored or returned.

## 18. Analytics
Emit via `OutboxWriter`: `parent_bedtime_window_configured`, `parent_sleep_timer_ceiling_configured` (both on successful `PUT`, with before/after values in the event payload for product analytics, not PII).

## 19. Performance
- Single-row PK lookups by `child_id` — no pagination, no N+1 risk.
- Async SQLAlchemy throughout; no blocking calls in the request path.
- Cacheable response (5–15 min client-side) reduces read load given this config changes infrequently.

## 20. Library Requirements
No new third-party libraries; reuses existing SQLAlchemy 2.0 async, Pydantic v2, Alembic already present in the codebase.

## 21. Testing
- Unit: `is_within_window()` correctness for same-day and midnight-crossing windows, evaluated at boundary instants (23:30, 05:00, exactly `window_start`, exactly `window_end`).
- Unit: safe-default response when no config row exists.
- Integration: `PUT` rejected for child-mode token (`403`); `PUT` accepted for parent-mode token within family; `PUT` rejected for parent outside family (`403`).
- Integration: `CHECK` constraint rejects a migration-level insert with `sleep_timer_ceiling_minutes` outside 5–120 (raw SQL test, bypassing app-level validation, to confirm the DB constraint itself is enforced).

## 22. Documentation
Add the `bedtime` module to the OpenAPI schema export; run the existing `classify_openapi_diff.py` check to confirm this is a purely additive, non-breaking change (new module, no existing endpoint touched).

## 23. AI Coding Agent Implementation Steps

**Task 01 — Create `BedtimeConfigOrm` Model & Migration**
Objective: New `bedtime_config` table, PK/FK `child_id`, with DB-level CHECK constraint on the sleep-timer ceiling. Why: no existing table stores this configuration. Follow: `modules/content/models.py` conventions (`Base`, `TimestampMixin`). Files to create: `models.py`, migration file. Business Rules: one row per child (upsert semantics), CHECK 5–120. Do Not Change: no existing tables touched. Tests: migration up/down smoke test; raw-SQL CHECK-violation test. Definition of Done: migration clean on fresh DB; CHECK constraint verified at the DB layer, not just app layer.

**Task 02 — Implement `BedtimeConfigRepository`**
Objective: `get_by_child_id()`, `upsert()` (`ON CONFLICT (child_id) DO UPDATE`). Follow: `BaseRepository`. Tests: upsert idempotency (second write updates, does not duplicate). Definition of Done: tests pass.

**Task 03 — Implement `BedtimeConfigService`**
Objective: `get_config()` (safe-default fallback), `upsert_config()` (parent-only, enforced via requester context passed in from the router layer), `is_within_window(now, config)` pure function. Follow: `BaseService`. Dependencies: Task 01–02. Tests: midnight-crossing boundary tests at 23:30/05:00; safe-default-when-unconfigured test. Definition of Done: all listed tests pass.

**Task 04 — Implement `BedtimeRouter`**
Objective: `GET`/`PUT /v1/parent-controls/{child_id}/bedtime`, wired to `get_current_child`/`get_current_parent`. Follow: existing router security-declaration (`openapi_extra`) pattern; no business logic in this file. Dependencies: Task 03. Tests: covered by Task 06. Definition of Done: both endpoints registered and documented.

**Task 05 — Enforce Authorization Boundaries**
Objective: Child-mode token scoped to own `child_id` on `GET`; parent-mode token required on `PUT`; family-membership check on parent reads/writes (reuse existing family-membership helper — confirm its location in `core/deps.py` or `modules/family/` before implementing a new one). Dependencies: Task 04. Tests: `403` tests per §16. Definition of Done: penetration-style test (child token attempts `PUT`) fails as expected.

**Task 06 — Add Unit & Integration Tests**
Objective: Full coverage per §21. Files: `test_bedtime_config_service.py`, `test_bedtime_config_api.py`. Definition of Done: all green in CI.

**Task 07 — Add Analytics Event Emission**
Objective: Emit `parent_bedtime_window_configured`/`parent_sleep_timer_ceiling_configured` via `OutboxWriter` on successful `PUT`. Dependencies: Task 04. Tests: fake-outbox assertion, exactly one emission per successful write. Definition of Done: test passes.

**Task 08 — Update OpenAPI Documentation**
Objective: Regenerate schema, confirm additive/non-breaking diff. Definition of Done: diff-classification passes.

**Task 09 — Final Code Review**
Objective: Confirm layering (no DB access in router/service, no business logic in repository), confirm midnight-crossing logic is genuinely correct (not a naive `start < end` check), confirm parent-only write is unbypassable. Definition of Done: checklist in §24 fully checked.

## 24. Final Verification Checklist
- [x] `bedtime_config` table created with PK/FK `child_id` and DB-level CHECK (5–120) constraint
- [x] `is_within_window()` correctly handles midnight-crossing windows at boundary instants
- [x] `GET` returns safe defaults (never 404/500) for an unconfigured child
- [x] `PUT` strictly rejects child-mode tokens (`403`) — verified via explicit test
- [x] Parent reads/writes scoped to their own family's children only
- [x] Midnight-crossing `window_end < window_start` accepted as valid, not rejected by a naive validator
- [x] Analytics events emitted on successful config writes
- [x] OpenAPI diff confirmed additive/non-breaking
- [x] No PostgreSQL/Redis credentials modified

## 25. Definition of Done
The `bedtime` module reliably serves and persists per-child bedtime window and sleep-timer-ceiling configuration, correctly handles midnight-crossing windows, fails safe toward "no auto-applied window" when unconfigured, and strictly enforces parent-only writes — forming the configuration foundation that K-02, K-03, K-07, and A.3's K-05 all read from.
