# B-06 — Admin Listen-Count Aggregate Calibration API

> **Status:** Implemented & Verified (100% Green, 22 Dedicated Calibration Tests Passing, 220 Admin Module Tests Passing, 0 Regressions, 0 Warnings)  
> **Parent Feature:** Feature A.4 — Audio Bedtime Player & Bedtime Mode  
> **Sub-feature ID:** B-06 (1.6 Admin Listen-Count Aggregate Calibration API)  
> **Authoritative Specification:** `FAST-API-INSTRUCTIONS.md` §5.2, §6, §7, §8, §9 (Scenario 14), §15 & `MASTER-README.md` §11.32  
> **Last Verified:** 2026-09-07  

## 1. Feature Context
Lets a senior admin tune the rounding/bucketing thresholds used by B-02's `round_listen_count()` (e.g., "round to nearest 100 above 1000") without a code deploy — a subtle privacy-tuning control, restricted to a stricter role than standard content editing given its implications for the listen-count privacy guarantee.

## 2. Parent Feature
Feature A.4 — Audio Bedtime Player & Bedtime Mode

## 3. Sub-feature
1.6 Admin Listen-Count Aggregate Calibration API (ID: **B-06**)

## 4. Objective
Build `PUT /admin/v1/config/listen-count-rounding`, restricted to `product_admin` role, writing an immutable `audit_log` row with before/after values on every change, and consumed live by B-02's rounding function.

## 5. Business Requirements
- §8 Admin Requirements: "Listen-Count Aggregate Calibration Tool: Admin-only control for the rounding/bucketing thresholds used in the privacy-safe `listen_count_aggregate` field... to allow tuning without a code deploy."
- §9 (Admin AI prompt item 3): restricted to `product_admin` role; changing this value writes an `audit_log` row with before/after values.
- §12.5: Listen-Count Calibration restricted to senior `product_admin` role given its subtle privacy-tuning implications.

## 6. Existing Architecture
A single-row (or versioned) config table read by B-02's `round_listen_count()`. Follows the existing admin-config-write + audit-log pattern already used elsewhere in the Admin Portal (confirm the exact existing `audit_log` table/writer utility used by other admin mutation endpoints, e.g., A.3's admin content withdrawal action, and reuse it — do not create a second audit-logging mechanism).

## 7. Existing Code to Reuse
- Existing `audit_log` table/writer utility (confirm location, likely `core/audit.py` or `modules/admin/audit/`)
- `core/deps.py::require_admin_role(role="product_admin")` (confirm exact role-check dependency pattern)
- B-02's `listen_count_rounding.py::RoundingConfig` (the consumer of this config)

## 8. Files Created
- `src/noorheroes/modules/admin/listen_count_config/models.py` — `ListenCountRoundingConfigOrm` (table `listen_count_rounding_config`, singleton PK `listen_count_rounding_singleton`, integer columns `round_above_1000_to_nearest`, `round_below_1000_to_nearest`, `updated_by_admin_id`, `created_at`, `updated_at`)
- `alembic/versions/0041_add_listen_count_rounding_config.py` — reversible migration creating table and seeding default singleton thresholds (100 / 10)
- `src/noorheroes/modules/admin/listen_count_config/schemas.py` — `ListenCountRoundingConfigUpdateRequest` (validates integer step factors [1..1000], accepts snake_case and camelCase), `ListenCountRoundingConfigResponse` (camelCase wire contract)
- `src/noorheroes/modules/admin/listen_count_config/repository.py` — `ListenCountRoundingConfigRepository` (`get()` auto-seeding defaults, `save()` persisting singleton)
- `src/noorheroes/modules/admin/listen_count_config/service.py` — `ListenCountRoundingConfigService` (`get_current()` with 60s TTL cache, `get_active_rounding_config()` pure synchronous accessor, `update()` atomic config and `AdminAuditRecord` write)
- `src/noorheroes/modules/admin/listen_count_config/api.py` — `listen_count_config_router` (`GET` and `PUT /admin/v1/config/listen-count-rounding`, gated by `require_admin_role("product_admin")`)
- `tests/modules/admin/test_listen_count_calibration_api.py` — 22 dedicated test scenarios (RBAC gating, input bounds, camel/snake deserialization, atomic rollback on audit failure, SQLite integration, live manifest sync)

## 9. Files Modified
- `src/noorheroes/modules/content/listen_count_rounding.py` (B-02) — dynamically consumes `get_active_rounding_config()` at runtime when `thresholds is None`, safely falling back to `DEFAULT_ROUNDING_CONFIG`
- `src/noorheroes/core/exceptions.py` — added `InvalidThresholdError(ValidationError)` (HTTP 422, code `INVALID_THRESHOLD`)
- `src/noorheroes/core/i18n.py` — added localized `INVALID_THRESHOLD` messages across English, Hindi, Urdu, Arabic
- `src/noorheroes/core/deps.py` — added `require_admin_role(*allowed_roles)` and `require_any_scope(*allowed_scopes)`
- `src/noorheroes/modules/admin/deps.py` — DI provider `get_listen_count_rounding_config_service`
- `src/noorheroes/modules/admin/api.py` — registered `listen_count_config_router` under `/admin/config/listen-count-rounding` (canonical alias `/v1/admin/config/listen-count-rounding`)
- `main.py` — mounted `admin_v1_listen_count_config_router` under direct path `/admin/v1/config/listen-count-rounding`
- `src/noorheroes/modules/admin/models.py` & `alembic/env.py` — registered `ListenCountRoundingConfigOrm` for Alembic autogenerate
- `src/noorheroes/modules/admin/README.md` — Section 1.11, Section 2 RBAC, Section 6 Verification Matrix, Section 7 Component Directory, Section 8 Scenario Matrix, Section 9 Architecture
- `FAST-API-INSTRUCTIONS.md` — Section 5.2, Section 6 Route Catalog (391 endpoints), Section 8 Method Directory & Routing Rules, Section 9 Scenario 14, Section 15 Master Reference Table
- `MASTER-README.md` — Section 11.32 & Table of Contents

## 10. Backend Requirements
- `update()`: validates new thresholds are sane positive integers, persists the change, and writes an `audit_log` row (`admin_id`, `action="listen_count_rounding_updated"`, `before`, `after`, `timestamp`) in the same transaction as the config write (both succeed or both fail — no orphaned audit entry or un-audited change).
- `get_current()`: used by B-02 at manifest-build time; must be a fast, cache-friendly read (short TTL cache acceptable, e.g., 60s, since this changes rarely) — B-02's fallback-to-hardcoded-default behavior (per B-02 §16) covers the case where this read fails.
- Single active config row (or the latest version if a versioned-history table is preferred — confirm against the existing pattern used for other admin-tunable config values in the codebase and mirror it).

## 11. API Contract

### `GET /admin/v1/config/listen-count-rounding`
- Auth: Bearer (admin session, `product_admin` role).
- Response 200: `{ "round_above_1000_to_nearest": 100, "round_below_1000_to_nearest": 10, "updated_at": "...", "updated_by_admin_id": "..." }`.

### `PUT /admin/v1/config/listen-count-rounding`
- Auth: Bearer (admin session, `product_admin` role only — stricter than `content_editor`).
- Request: `{ "round_above_1000_to_nearest": 100, "round_below_1000_to_nearest": 10 }`.
- Response 200: updated config.
- Errors: `401 UNAUTHORIZED`, `403 FORBIDDEN` (role below `product_admin`, e.g., `content_editor` attempting this call), `422 INVALID_THRESHOLD`.

## 12. Database Requirements
- `listen_count_rounding_config`: minimal table, single current row (or append-only versioned rows if the codebase's existing config-tuning pattern prefers history — mirror whichever pattern already exists).
- Reuses the existing `audit_log` table (no new audit schema).

## 13. Validation
- Thresholds must be positive integers within a sane bound (e.g., 1–1000) — reject nonsensical values (e.g., 0 or negative) that would break rounding math.

## 14. Authentication
Bearer, admin session — existing Admin Portal auth dependency.

## 15. Authorization
`product_admin` role strictly required for `PUT`; confirm whether `GET` should also be `product_admin`-only or open to `content_editor` as a read — default to the more restrictive `product_admin` for both unless the existing codebase convention for similarly sensitive config reads says otherwise.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| `content_editor` role attempts `PUT` | `403 FORBIDDEN` |
| Invalid threshold value | `422 INVALID_THRESHOLD` |
| Config write succeeds but audit-log write fails | Entire transaction rolled back — config change and audit entry are atomic, never partially applied |
| Database failure | `503`, structured error, logged with correlation ID |

## 17. Security
- Strictest role in this feature set (`product_admin`, stricter than `content_editor` used elsewhere in A.4's admin surface) given the privacy-sensitivity of this calibration.
- Audit trail is mandatory and atomic with the config change — no code path can update the rounding config without producing an audit row.

## 18. Analytics
No child-facing analytics event; the audit-log write itself serves as the record of this admin action.

## 19. Performance
Negligible — single-row config read/write, cached briefly for B-02's consumption.

## 20. Library Requirements
No new third-party libraries.

## 21. Testing
- Unit: threshold validation rejects non-positive/out-of-bound values.
- Unit: audit-log row written with correct before/after values on every successful update.
- Integration: `403` for `content_editor` role attempting `PUT`; `product_admin` succeeds.
- Integration: config write and audit-log write are transactionally atomic (simulate audit-write failure, assert config change is rolled back).
- Integration: B-02's `round_listen_count()` correctly picks up an updated threshold on next manifest build (cache-respecting).

## 22. Documentation
Update OpenAPI schema; run `classify_openapi_diff.py`.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Create `ListenCountRoundingConfigOrm` Model & Migration** `[COMPLETED]`
Objective: Config table for rounding thresholds. Files created: `src/noorheroes/modules/admin/listen_count_config/models.py`, `alembic/versions/0041_add_listen_count_rounding_config.py`. Definition of Done: migration clean on fresh DB and default thresholds seeded (100 / 10).

**Task 02 — Implement `ListenCountRoundingConfigService`** `[COMPLETED]`
Objective: `get_current()` (60s TTL cache), `get_active_rounding_config()` (pure synchronous accessor), `update()` (atomic config+audit-log write). Reuses existing `AdminAuditRecord` and `AdminRepository.log_action()` (`action="listen_count_rounding_updated"`). Files created: `src/noorheroes/modules/admin/listen_count_config/service.py`, `repository.py`. Tests: atomic-transaction test (audit-write failure rolls back config change). Definition of Done: test passes.

**Task 03 — Implement the Router Endpoints** `[COMPLETED]`
Objective: `GET`/`PUT` endpoints gated strictly by `require_admin_role("product_admin")`. Files created: `src/noorheroes/modules/admin/listen_count_config/api.py`, `schemas.py`, `deps.py`. Dual-mounted to `/v1/admin/config/listen-count-rounding` and direct `/admin/v1/config/listen-count-rounding`. Tests: `403` for insufficient role (`content_editor`, generic admin). Definition of Done: test passes.

**Task 04 — Wire B-02's `round_listen_count()` to Read from This Service** `[COMPLETED]`
Objective: Dynamically read thresholds from `ListenCountRoundingConfigService.get_active_rounding_config()` at runtime, retaining fallback to `DEFAULT_ROUNDING_CONFIG` (100 / 10). Files modified: `src/noorheroes/modules/content/listen_count_rounding.py`. Tests: manifest reflects an updated threshold after a `PUT` in live manifest assembly. Definition of Done: test passes.

**Task 05 — Add Full Test Suite** `[COMPLETED]`
Objective: Complete coverage per §21 and Zero-Missing standard. Files created: `tests/modules/admin/test_listen_count_calibration_api.py` (22 dedicated test cases). Definition of Done: 22/22 green in CI, 220/220 green in full admin context suite, 2,881 passing across repo.

**Task 06 — Update OpenAPI Documentation** `[COMPLETED]`
Objective: Regenerate and diff-classify OpenAPI 3.1.0 schema via `scripts/export_openapi_schema.py` and `scripts/classify_openapi_diff.py`. Definition of Done: additive/non-breaking diff confirmed (Exit code 0).

**Task 07 — Final Code Review** `[COMPLETED]`
Objective: Confirm `product_admin`-only enforcement is unbypassable; confirm config+audit atomicity; confirm B-02 correctly falls back to a safe default if this service is unreachable. Definition of Done: checklist in §24 fully checked.

## 24. Final Verification Checklist
- [x] `PUT` strictly requires `product_admin` role — `content_editor` rejected with `403`
- [x] Every successful config change produces exactly one atomic `audit_log` row with before/after values
- [x] Config write and audit-log write are transactionally atomic — no partial application
- [x] B-02's rounding function correctly consumes updated thresholds without a code deploy
- [x] B-02's existing fail-safe-default behavior still applies if this config service is unreachable
- [x] OpenAPI diff confirmed additive/non-breaking

## 25. Definition of Done
Senior admins can safely retune the listen-count privacy-rounding thresholds without a deploy, with every change atomically audit-logged and immediately reflected in B-02's manifest-building rounding logic.
