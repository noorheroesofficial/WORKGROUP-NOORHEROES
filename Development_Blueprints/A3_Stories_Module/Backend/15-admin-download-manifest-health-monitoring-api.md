# B-15 — Admin Download Manifest Health Monitoring API

## 1. Feature Context
A read-only operational dashboard API surfacing manifest generation success/failure rate over time, so ops/support can spot degraded download health (e.g., CDN signing issues) before it becomes a support-ticket flood.

## 2. Parent Feature
Feature A.3 — Stories Module (Animated Storytelling System)

## 3. Sub-feature
1.15 Admin Download Manifest Health Monitoring API (ID: **B-15**)

## 4. Objective
Implement `GET /admin/v1/downloads/health` inside the existing `media` + `admin` modules, aggregating B-08's `download_manifest_record` data (plus manifest-failure logging if not already captured) into a time-series suitable for the N-03 recharts dashboard.

## 5. Business Requirements
- §8 Admin Requirements: Download Manifest Monitor — read-only view of manifest generation health/failure rates.
- §9 Admin AI Code-Generation Prompt: read-only dashboard (recharts) sourced from `GET /admin/v1/downloads/health`.
- §10 DevOps: alert on completion-event idempotency-violation attempts and AI-timeout-fallback rate — this endpoint's data feeds the analogous download-health alerting.

## 6. Existing Architecture
Extends the existing `media` module with a read-only aggregation endpoint over B-08's data, following the existing `admin` module's read-scope RBAC pattern (`AdminRouter`'s `admin:read` scope as the model to mirror).

## 7. Existing Code to Reuse
- `modules/media/download_repository.py::DownloadManifestRepository` (B-08, extend with a time-series aggregation query)
- `core/deps.py::get_current_admin`, `require_admin_scope()`

## 8. Files to Create
- `src/noorheroes/modules/media/health_schemas.py` — `DownloadHealthResponse` (time-bucketed success/failure counts)
- `src/noorheroes/modules/media/health_service.py` — `DownloadHealthService(BaseService)`
- `tests/modules/media/test_download_health_service.py`
- `tests/modules/media/test_download_health_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/media/api.py::MediaRouter` — add `GET /admin/v1/downloads/health`
- `src/noorheroes/modules/media/download_models.py::DownloadManifestRecordOrm` (B-08) — confirm a `status` (`success|failed`) column exists to support failure-rate aggregation; add via migration here if B-08 did not already include it, since manifest *generation attempts* that fail may not currently produce a persisted row at all (coding agent must first confirm B-08 logs failed attempts, not only successful ones — if not, add a minimal `download_manifest_attempt_log` table here rather than retrofitting B-08)

## 10. Backend Requirements
- `DownloadHealthService.get_health_timeseries(from_date, to_date, bucket)`: aggregates count of successful vs. failed manifest-generation attempts per time bucket (e.g., hourly/daily), read-only.
- If B-08 currently only persists successful manifests, this sub-feature adds a lightweight `download_manifest_attempt_log` (attempt outcome, timestamp, failure_reason) written by B-08's service on both success and failure paths — coordinate this as an additive change to B-08, not a breaking one.
- No mutation endpoints exist on this router at all.

## 11. API Contract

### `GET /admin/v1/downloads/health`
- Auth: Admin Bearer (admin read scope). Response 200: time-series `{ buckets: [{ period: "2026-08-16T00:00:00Z", success_count: N, failure_count: N }] }`.

## 12. Database Requirements
- Reads `download_manifest_record` (B-08); may add `download_manifest_attempt_log` if B-08 doesn't already capture failed attempts (see §10).

## 13. Validation
- `from_date`/`to_date` range validated (reject inverted or excessively large ranges to protect query performance).

## 14. Authentication
Admin Bearer via `get_current_admin`.

## 15. Authorization
Read-only admin scope (mirrors `AdminRouter`'s `admin:read` — no write scope needed since this router has no mutations).

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| No data in requested range | `200` with empty buckets array, not an error |
| Invalid date range | `400 INVALID_RANGE` |
| Database failure | `503`, logged |

## 17. Security
Read-only surface — no mutation capability, minimal security surface beyond standard admin authentication.

## 18. Analytics
N/A — this endpoint itself surfaces operational data, it does not emit child-facing analytics events.

## 19. Performance
- Aggregation query must use the existing `(child_id, expires_at)` index or a new time-bucketed index on `created_at`/`status` as appropriate — avoid full table scans on what could become a large `download_manifest_record` table over time.

## 20. Library Requirements
No new libraries — frontend (N-03) handles chart rendering via recharts; this API only returns aggregated JSON.

## 21. Testing
- Unit: time-bucketing correctness, empty-range handling.
- Integration: aggregation correctness against a seeded fixture of mixed success/failure manifest attempts across multiple time buckets.

## 22. Documentation
Update OpenAPI schema.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Confirm/Add Failure-Attempt Capture in B-08's Write Path**
Objective: Ensure failed manifest-generation attempts are persisted somewhere queryable (either an added `status` column on `download_manifest_record` or a new `download_manifest_attempt_log` table). Follow: existing SQLAlchemy/Alembic conventions. Do Not Change: B-08's existing successful-manifest behavior/contract. Tests: failed attempt produces a queryable row. Definition of Done: migration clean, failure capture verified.

**Task 02 — Implement `DownloadHealthResponse` Schema**
Objective: Time-bucketed response shape. Tests: schema validation. Definition of Done: schema used by Task 04.

**Task 03 — Implement Time-Series Aggregation Query**
Objective: `get_health_timeseries()` grouping success/failure counts per bucket. Dependencies: Task 01. Tests: bucketing correctness against a seeded multi-day fixture. Definition of Done: test passes.

**Task 04 — Add Router Endpoint**
Objective: Wire `GET /admin/v1/downloads/health` with read-only admin scope. Tests: covered by Task 05. Definition of Done: endpoint live, documented.

**Task 05 — Add Unit & Integration Tests**
Objective: Full coverage per §21. Definition of Done: all green in CI.

**Task 06 — Update OpenAPI Documentation**
Objective: Regenerate/diff-classify. Definition of Done: non-breaking diff confirmed.

**Task 07 — Final Code Review**
Objective: Confirm this router has zero mutation endpoints; confirm the failure-capture addition to B-08 is additive/non-breaking. Definition of Done: checklist in §24 fully checked.

## 24. Final Verification Checklist
- [ ] Endpoint is strictly read-only — no mutation capability anywhere on this router
- [ ] Failed manifest-generation attempts are captured and included in the health data (not just successes)
- [ ] Time-bucketing aggregation is correct against a seeded multi-bucket fixture
- [ ] Empty date ranges return a valid empty response, not an error
- [ ] Addition of failure-capture to B-08's write path is confirmed non-breaking to B-08's existing contract
- [ ] No PostgreSQL/Redis credentials modified

## 25. Definition of Done
Ops/support have accurate, queryable visibility into download-manifest generation health over time — feeding N-03's dashboard and supporting the PRD's operational-monitoring intent for the Download Manifest Service.
