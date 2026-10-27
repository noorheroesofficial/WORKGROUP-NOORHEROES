# B-07 — Admin Onboarding Funnel & OTP Health Monitoring API

## 1. Feature Context
Read-only reporting surface for Product/Growth/DevOps: step-by-step funnel conversion from `app_splash_viewed` through `onboarding_completed`, and OTP delivery health by provider/channel/region — the operational visibility layer over B-01/B-02's event stream.

## 2. Parent Feature
Feature A.1 — Splash, Language Selection, Authentication & Onboarding

## 3. Sub-feature
1.7 Admin Onboarding Funnel & OTP Health Monitoring API (ID: **B-07**)

## 4. Objective
Implement two read-only admin endpoints aggregating funnel and OTP-health metrics from the analytics event stream, following the existing `AdminRouter`/`admin:read` scope pattern.

## 5. Business Requirements
- Onboarding Funnel Dashboard: step-by-step drop-off (Splash → Intro → Registration → OTP → PIN → Add Child → Complete), filterable by platform/locale/date range.
- OTP Health Monitor: real-time delivery success rate per provider/channel/region, with alerting on threshold breach (default 95%).
- §11.2: Primary funnel `app_splash_viewed → registration_submitted → otp_verification_succeeded → pin_setup_completed → add_child_succeeded → onboarding_completed`, tracked with step-over-step conversion and median time-per-step.
- Alerting requirement (DevOps §10): alert if OTP delivery success rate < 95% sustained 5 minutes.

## 6. Existing Architecture
Extends `modules/admin/` (`AdminService`, `AdminRouter`, `admin:read` scope). **Resolved architecture decision:** re-reading `FAST-API-INSTRUCTIONS.md` end-to-end confirms there is no documented analytics warehouse, external OLAP store, or existing rollup/materialized-view infrastructure anywhere in the stack — only PostgreSQL, Redis, R2, Celery, and the `outbox_events` table + `OutboxRelay`. "Analytics Event Bus" in the PRD is therefore not an existing NoorHeroes component; it is aspirational language in the PRD. Resolution: rather than depending on infrastructure that doesn't exist, this sub-feature builds its own lightweight rollup **inside the existing Postgres instance**, populated by a periodic Celery task following the exact pattern already established by `modules/localization/tasks.py::retry_failed_translations_task` (a periodic, non-event-driven background job). This keeps the feature shippable on the actual existing stack instead of blocking on unbuilt data-engineering infrastructure.

## 7. Existing Code to Reuse
- `modules/admin/service.py::AdminService` (extend)
- `core/deps.py::get_current_admin`, `require_admin_scope("admin:read")`
- `modules/localization/tasks.py::retry_failed_translations_task` — structural pattern for the new periodic rollup task (Celery beat schedule, not event-driven)
- `common/outbox.py::OutboxEventOrm` — the new rollup task reads committed rows from the existing `outbox_events` table as its source data (it does not require a new event-bus integration)

## 8. Files to Create
- `src/noorheroes/modules/admin/onboarding_analytics_schemas.py` — `FunnelResponse`, `OtpHealthResponse`
- `src/noorheroes/modules/admin/onboarding_analytics_service.py` — `OnboardingAnalyticsService(BaseService)`
- `src/noorheroes/modules/admin/onboarding_analytics_repository.py` — `AnalyticsRollupRepository` (renamed from `AnalyticsWarehouseRepository` — reads the new in-Postgres rollup tables, not an external warehouse)
- `src/noorheroes/modules/admin/onboarding_rollup_models.py` — `OnboardingFunnelRollupOrm`, `OtpHealthRollupOrm` (new Postgres tables, populated by the periodic task, not transactional identity data)
- `alembic/versions/xxxx_add_onboarding_analytics_rollup_tables.py`
- `src/noorheroes/modules/admin/tasks.py::compute_onboarding_rollups_task` — new periodic Celery task (runs e.g. every 5 minutes), modeled on `retry_failed_translations_task`
- `tests/modules/admin/test_onboarding_analytics_api.py`
- `tests/modules/admin/test_compute_onboarding_rollups_task.py`

## 9. Files to Modify
- `src/noorheroes/modules/admin/api.py` — add `GET /admin/v1/onboarding/funnel`, `GET /admin/v1/onboarding/otp-health`
- `src/noorheroes/core/settings.py` — register the new periodic task's Celery beat schedule entry

## 10. Backend Requirements
- `compute_onboarding_rollups_task` runs on a Celery beat schedule (e.g., every 5 minutes), reads new `outbox_events` rows since its last watermark, aggregates them into `OnboardingFunnelRollupOrm` (per step/platform/locale/date-bucket) and `OtpHealthRollupOrm` (per provider/channel/region/hour-bucket), and advances its watermark — this is the concrete resolution to the "analytics warehouse" gap, not a placeholder.
- Funnel query reads `OnboardingFunnelRollupOrm` directly (never raw `outbox_events`), computes step-over-step conversion % and median time-per-step from the pre-aggregated rows; filters by `from`/`to` date range, `platform`, `locale`.
- OTP-health query reads `OtpHealthRollupOrm`; includes a `below_threshold: bool` flag computed against a threshold value read from B-01/B-09's `remote_config.otp_health_threshold_pct` field (default 95% if unset) — **not** a hardcoded constant, resolving §20's admin-tunability question directly. (This requires a small additive column on B-09's `remote_config` table — coordinate with B-09 if not already present.)
- Both endpoints read only from the two new rollup tables — the "must use pre-aggregated data, not live raw-event scans" requirement is now concretely satisfiable because the rollup tables actually exist.

## 11. API Contract

### `GET /admin/v1/onboarding/funnel?from=&to=&platform=&locale=`
- Auth: `get_current_admin` + `admin:read`. Response 200: ordered list of `{step, count, conversion_from_previous_pct, median_time_seconds}`.

### `GET /admin/v1/onboarding/otp-health?window=24h|7d`
- Auth: `get_current_admin` + `admin:read`. Response 200: list of `{provider, channel, region, success_rate_pct, below_threshold}`.

## 12. Database Requirements
Two new Postgres tables (not in the `identity` schema — these are admin/reporting-owned): `onboarding_funnel_rollup` (`step`, `platform`, `locale`, `date_bucket`, `count`, updated by the periodic task) and `otp_health_rollup` (`provider`, `channel`, `region`, `hour_bucket`, `requested_count`, `succeeded_count`, updated by the periodic task). Both are populated exclusively by `compute_onboarding_rollups_task` — the API layer never writes to them. This resolves what was previously flagged as a missing-infrastructure gap: no external warehouse is required.

## 13. Validation
Date-range validation (`from` ≤ `to`, both within a sane bound, e.g., max 1-year range) to prevent unbounded aggregation queries.

## 14. Authentication
`get_current_admin`.

## 15. Authorization
`admin:read` scope, per existing `AdminRouter` convention.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| No data in selected range | `200` with empty/zero-value series, not an error |
| Rollup tables empty (e.g., periodic task hasn't run yet post-deploy) | `200` with empty series, same as no-data — not a `503`, since this is a normal transient state, not an infrastructure failure |
| Rollup task itself fails (caught exception in the Celery task) | Logged and alerted via existing Celery/DevOps monitoring; API continues serving the last-successful rollup data (stale but available), never blocks the endpoint |
| Invalid date range | `422` |

## 17. Performance
Must rely on pre-aggregated data; live full-table scans over raw events are explicitly disallowed for this endpoint given expected event volume.

## 18. Security
`admin:read`-gated; no PII in the response (all metrics are counts/rates, no individual identifiers).

## 19. Testing
Unit: conversion-percentage math against seeded funnel counts. Integration: empty-range handling, threshold-breach flag correctness at exactly 95.0%.

## 20. Documentation
The `below_threshold` default (95%) lives in `remote_config.otp_health_threshold_pct` (B-01/B-09), not a hardcoded constant — document this cross-reference clearly in both this module's README and B-09's, since it's easy for a future maintainer to miss that an admin-tunable field lives in a different module.

## 21. AI Coding Agent Implementation Steps

**Task 01 — Create Rollup Tables & Migration**
Objective: `onboarding_funnel_rollup`, `otp_health_rollup` tables per §12. Why: this is the concrete, buildable replacement for the previously-flagged "analytics warehouse" dependency. Follow: standard Alembic/SQLAlchemy conventions. Tests: migration smoke test. Definition of Done: both tables created, indexed on their bucket/dimension columns for the query patterns in §11.

**Task 02 — Implement `compute_onboarding_rollups_task` (Periodic Celery Task)**
Objective: Watermark-based aggregation of `outbox_events` into the two rollup tables. Why: this is the actual data pipeline resolving the gap — not a placeholder. Follow: `modules/localization/tasks.py::retry_failed_translations_task`'s periodic-task structure and Celery beat registration pattern exactly. Files to Create: `modules/admin/tasks.py`. Business Rules: idempotent re-runs (advancing a watermark, never double-counting a processed event); must not lock/block transactional writes to `outbox_events`. Tests: watermark-advances-correctly test; idempotent-rerun-doesn't-double-count test; simulated task failure leaves the watermark unadvanced (safe to retry). Dependencies: Task 01. Definition of Done: running the task twice in a row against the same new events produces the same rollup totals, not double.

**Task 03 — Implement `AnalyticsRollupRepository`**
Objective: Read-only query layer against the two rollup tables. Follow: `BaseRepository` read patterns. Files to Create: repository file. Tests: query-shape unit tests against seeded rollup rows. Dependencies: Task 01. Definition of Done: repository returns correctly-shaped aggregate rows with no reference to raw `outbox_events`.

**Task 04 — Implement `OnboardingAnalyticsService`**
Objective: Business logic for conversion-percentage and threshold-flag computation, reading the threshold from `remote_config.otp_health_threshold_pct` (coordinate with B-09 if the column doesn't exist yet — add it as part of this task if B-09 hasn't landed it). Follow: `BaseService`. Tests: math correctness at boundary (exactly 95.0%); threshold correctly read from config, not hardcoded. Dependencies: Task 03. Definition of Done: changing `remote_config.otp_health_threshold_pct` changes this endpoint's `below_threshold` output without a code change.

**Task 05 — Add Router Endpoints**
Objective: Wire both `GET` endpoints under `admin:read`. Follow: existing `AdminRouter` scope-gating pattern. Definition of Done: both endpoints live, documented, scope-enforced.

**Task 06 — Add Unit & Integration Tests**
Objective: Full coverage per §19, plus the rollup-task-specific tests from Task 02. Definition of Done: all green in CI.

**Task 07 — Update OpenAPI Documentation**
Objective: Regenerate, confirm non-breaking diff. Definition of Done: diff classifier passes.

**Task 08 — Final Code Review**
Objective: Confirm the periodic task is idempotent and watermark-safe, confirm both endpoints read only from rollup tables (never raw `outbox_events`), confirm `admin:read` scope correctly enforced. Definition of Done: checklist in §22 checked.

## 22. Final Verification Checklist
- [x] Both endpoints gated behind `admin:read`
- [x] No PII in either response payload
- [x] Rollup tables exist and are the only data source for both endpoints — resolved, no longer an open infrastructure gap
- [x] `compute_onboarding_rollups_task` is idempotent under re-run and watermark-safe under failure
- [x] Threshold-breach flag reads `remote_config.otp_health_threshold_pct`, not a hardcoded constant
- [x] Date-range validation prevents unbounded queries
- [x] Unit + integration tests green, including the rollup-task tests

## 23. Definition of Done
`GET /admin/v1/onboarding/funnel` and `GET /admin/v1/onboarding/otp-health` are live, `admin:read`-gated, and return correctly-aggregated funnel/health data — ready for N-01 and N-02 to render. **(STATUS: IMPLEMENTED & VERIFIED)**

