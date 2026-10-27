# B-07 — Admin Download & Sync Health Monitoring API

## 1. Feature Context
Part of Feature B.15 (Offline Downloads & Sync). Read-only operational visibility into the two canonical services (Download Manifest Service, Offline Sync Engine) for `product_admin`/`trust_safety` staff — the backend counterpart consumed by N-01 and N-02.

## 2. Parent Feature
B.15 — Offline Downloads & Sync

## 3. Sub-feature
B-07 — Admin Download & Sync Health Monitoring API

## 4. Objective
Implement two read-only admin endpoints aggregating manifest-issuance health (success/failure/cap-rejection/URL-expiry-retry rates) and sync-integrity health (batch volume, duplicate-prevention rate, rejected-event breakdown by domain/event-type), restricted to `product_admin`/`trust_safety` RBAC scopes.

## 5. Business Requirements
- §8 Admin Requirements: Download Manifest Health Monitor (read-only) — issuance success/failure, cap-rejection rates, signed-URL-expiry retry rates. Offline Sync Integrity Monitor (read-only) — sync-batch volume, duplicate-prevention rate (positive signal), rejected-event rate by domain/event-type.
- CRUD permissions: both monitors are read-only behind `product_admin`/`trust_safety`.
- §11 Analytics: `offline_sync_duplicate_prevented` framed as a positive integrity-health signal, not a warning.
- DevOps §10: alert on download-failure-rate spikes, sync-batch latency for large batches, and any production-detected duplicate event that should have been caught by dedup (P0) — this API is the human-facing read surface for those same underlying metrics.

## 6. Existing Architecture
Two `GET` routes on the same `downloads` bounded context's `DownloadsRouter` (or a nested `admin` sub-router within it), aggregating over `download_record` (B-01), the `DownloadManifestIssued` outbox events (B-01), and `sync_event_log` (B-05) — no new metrics-storage system introduced; aggregation is computed via SQL over existing tables, following the same approach as other admin read-only dashboards in the platform.

## 7. Existing Code to Reuse
- `core/deps.py` → `get_current_admin`, `require_admin_scope("admin:read")` (or the `trust_safety` scope equivalent).
- `infrastructure/redis.py` → short-TTL caching for expensive aggregate queries (consistent with B-03's caching approach).
- `common/base_service.py`/`base_repository.py` for consistency, even though these are read-only aggregate queries rather than standard CRUD.

## 8. Files to Create
- `src/noorheroes/modules/downloads/admin_schemas.py` — `ManifestHealthResponse`, `SyncIntegrityHealthResponse`.
- `src/noorheroes/modules/downloads/admin_repository.py` — aggregate query methods.
- `tests/modules/downloads/test_admin_health_monitoring_api.py`.
- `tests/modules/downloads/test_admin_health_rbac.py`.

## 9. Files to Modify
- `modules/downloads/api.py` — add `GET /v1/admin/downloads/health`, `GET /v1/admin/sync/health` routes.
- `modules/downloads/deps.py` — add `get_admin_health_service` factory.

## 10. Backend Requirements
- `GET /v1/admin/downloads/health`: issuance success/failure rate, cap-rejection rate (derived from `DownloadManifestIssued` outbox events' rejection-reason field), signed-URL-expiry re-issuance rate, all as time-bucketed series (e.g., hourly over the last 72 hours, configurable window).
- `GET /v1/admin/sync/health`: sync-batch volume over time, `duplicate`-status rate as a percentage of total processed events (framed positively in the response's field naming, e.g., `duplicates_correctly_prevented`), `rejected`-status breakdown grouped by `event_type`.
- Both endpoints support a `window` query param (e.g., `24h`, `72h`, `7d`) bounding the aggregation range.
- Aggregate queries cached in Redis with a short TTL (e.g., 60s) to keep dashboard load fast without hammering PostgreSQL on every admin page view.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
Consumed by N-01 (`GET /v1/admin/downloads/health`) and N-02 (`GET /v1/admin/sync/health`) via each dashboard's respective hook.

## 13. API Contract
**Endpoint 1:** `GET /v1/admin/downloads/health?window=72h`
**Response 200:**
```json
{ "series": [ { "bucket": "2026-08-17T00:00:00Z", "issued": 120, "cap_rejected": 4, "entitlement_rejected": 1, "url_reissue_count": 8 } ] }
```
**Endpoint 2:** `GET /v1/admin/sync/health?window=72h`
**Response 200:**
```json
{ "series": [ { "bucket": "2026-08-17T00:00:00Z", "batches_processed": 340, "events_applied": 1200, "events_duplicate_prevented": 45, "events_rejected": 3 } ], "rejected_by_event_type": [ { "event_type": "quiz_response", "count": 2 } ] }
```
**Auth (both):** Bearer, admin, `Depends(get_current_admin)` + `admin:read`/`trust_safety` scope.

## 14. Database Requirements
Read-only aggregate queries over `download_record`, outbox event history (or a materialized subset thereof), and `sync_event_log`. No new tables owned by this sub-feature.

## 15. Validation
`window` param restricted to an allow-list of valid values (`24h|72h|7d|30d`); invalid value → `422`.

## 16. Authentication
`Depends(get_current_admin)` on both routes.

## 17. Authorization
`admin:read`/`trust_safety` scope required via `require_admin_scope()`; a valid admin token without this scope receives `403`.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| No events in the selected window | `200`, empty `series[]`, not an error |
| Invalid `window` value | `422` |
| Redis cache failure | Falls through to a direct (slower) DB aggregate query, never fails the request |
| Unauthorized/insufficient scope | `401`/`403` respectively |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
N/A — admin-portal-side localization (if any) is handled by N-01/N-02's rendering layer, not this API's response shape.

## 22. RTL
N/A.

## 23. Analytics
This API **is** the analytics/monitoring read surface for B.15; it does not itself emit further analytics events.

## 24. Performance
- Time-bucketed aggregation queries use indexed timestamp columns (`created_at`/`occurred_at`) with the existing `(child_id, status)`/`(child_id, occurred_at)` indexes from B-01/B-05 supporting the underlying scans.
- Redis caching absorbs repeat dashboard-refresh load.
- Bounded `window` values prevent an admin from triggering an unbounded full-history aggregation.

## 25. Security
- Strictly read-only — no mutation surface on either route.
- Scope-gated to `product_admin`/`trust_safety` only; no broader admin role can access these by default.
- No per-child or per-family identifying detail is exposed — all figures are aggregate counts/rates, consistent with child-data privacy posture (no admin visibility into a specific child's download list, per B-02 §12).

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 (async), Redis. No new libraries.

## 27. Testing
- Unit: aggregate query correctness against a fixture dataset spanning multiple buckets/event types.
- Unit: `window` param validation (valid/invalid values).
- **RBAC test:** request without `admin:read`/`trust_safety` scope → `403`.
- Integration: cache-hit vs. cache-miss paths both return identical, correct data.

## 28. Documentation
OpenAPI summaries for both routes; explicit doc note that `events_duplicate_prevented` is a positive signal, not a warning metric.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Define Admin Health Schemas**
Files to create: `modules/downloads/admin_schemas.py`.

**Task 02 — Implement Aggregate Repository Queries**
Objective: time-bucketed issuance and sync-integrity aggregation queries.
Files to create: `modules/downloads/admin_repository.py`.

**Task 03 — Implement Admin Health Routes**
Objective: `GET /v1/admin/downloads/health`, `GET /v1/admin/sync/health`, scope-gated.
Files to modify: `modules/downloads/api.py`, `modules/downloads/deps.py`.

**Task 04 — Add Redis Caching**
Objective: short-TTL cache on both aggregate queries.

**Task 05 — Add RBAC Test**
Tests: `test_admin_health_rbac.py`.

**Task 06 — Add Full Test Suite & OpenAPI Docs**

**Task 07 — Final Code Review**
Objective: confirm no per-child/per-family identifying data leaks into either response shape.

## 30. Definition of Done
- Both admin health endpoints live, matching §13 contracts.
- RBAC verified restricting access to `product_admin`/`trust_safety`.
- No per-child data exposed in either response.
- Full test suite green.

## 31. Final Verification Checklist
- [ ] Both endpoints strictly read-only.
- [ ] RBAC correctly restricts to `product_admin`/`trust_safety`.
- [ ] No per-child/per-family identifying data in either response.
- [ ] `duplicates_correctly_prevented`-style framing used for the dedup metric, not alarmist framing.
- [ ] Redis cache failure never fails the request.
- [ ] No PostgreSQL/Redis credentials modified.
