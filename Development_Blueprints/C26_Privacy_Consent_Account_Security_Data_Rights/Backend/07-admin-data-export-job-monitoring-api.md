# B-07 — Admin Data Export Job Monitoring API

## 1. Feature Context
Part of Feature C.26's Admin Requirements (§8). Read-only operational visibility into the Data Export Service (B-03) for `product_admin`.

## 2. Parent Feature
C.26 Privacy, Consent, Account Security & Data Rights (Settings)

## 3. Sub-feature
**B-07 — Admin Data Export Job Monitoring API**

## 4. Objective
Expose aggregated, read-only success/failure-rate and processing-time metrics over `data_request` (`type='export'`) rows for `product_admin`, without any mutation surface.

## 5. Business Requirements
- §8: "Data Export Job Monitor (Read-only): Visibility into export-job success/failure rates and processing times."
- CRUD permissions: Read-only behind `product_admin`.

## 6. Existing Architecture
Reads exclusively from B-03's `data_request` table — no new table, no write path. Lives in `modules/admin/` as an aggregation endpoint over `modules/data_rights`'s repository, following the same cross-module read-only aggregation pattern used elsewhere (e.g., C.20's dashboard aggregation reading from multiple owning modules).

## 7. Existing Code to Reuse
- `modules/data_rights/repository.py::DataRequestRepository` (B-03) — add read-only aggregation query methods here, not a duplicate repository.
- `modules/admin/api.py` — existing `AdminRouter` RBAC pattern.

## 8. Files to Create
- `src/noorheroes/modules/admin/data_export_monitor_schemas.py`
- `tests/modules/admin/test_data_export_monitor_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/data_rights/repository.py` — add `get_success_failure_rates(date_from, date_to)`, `get_avg_processing_time(date_from, date_to)` (read-only aggregation methods, alongside B-03's existing mutation methods).
- `src/noorheroes/modules/admin/api.py` — add `GET /v1/admin/data-exports/metrics`.

## 10. Backend Requirements
- Aggregate `COUNT(*) WHERE status='ready'`, `COUNT(*) WHERE status='failed'` grouped by day/week over the requested range.
- Aggregate `AVG(completed_at - requested_at) WHERE status='ready'` for processing time.
- Strictly `product_admin` role, read-only — no endpoint in this sub-feature ever writes to `data_request`.

## 11. API Contract

### `GET /v1/admin/data-exports/metrics?date_from=&date_to=`
- **Auth:** `product_admin` role
- **Response 200:** `{ "success_count": 120, "failure_count": 3, "avg_processing_seconds": 42, "by_period": [ { "period": "2026-08-10", "success": 15, "failure": 0 } ] }`

## 12. Database Requirements
None new — read-only aggregation queries against B-03's `data_request` table, using its existing `(family_id, requested_at DESC)` index (add a supplementary index on `(status, requested_at)` if aggregation query plans indicate it's needed — confirm via `EXPLAIN` before adding, not preemptively).

## 13. Validation
`date_from`/`date_to` required, `date_from <= date_to`.

## 14. Authentication
Existing admin session mechanism.

## 15. Authorization
`product_admin` role only.

## 16. Error Handling
| Scenario | Response |
|---|---|
| Non-`product_admin` role | `403` |
| Invalid date range | `422` |
| Large range causing slow aggregation | Paginate `by_period` or cap the max range (confirm max range with the team; do not allow unbounded queries) |

## 17. Offline First
N/A.

## 18. Local Data
N/A.

## 19. Localization
N/A — raw metrics, admin UI localizes labels.

## 20. RTL
N/A backend.

## 21. Analytics
This endpoint itself is the analytics surface; no further instrumentation needed.

## 22. Performance
Aggregation query only, bounded date range, no per-row admin access to family data (aggregate-only, avoiding unnecessary exposure of individual family records in this particular view — individual-record visibility is B-08's job, not this one's).

## 23. Security
Read-only, aggregate-only — this endpoint never returns individual family-identifying `data_request` rows, keeping its exposure surface minimal relative to B-08's per-record audit log.

## 24. Library Requirements
No new libraries.

## 25. Testing
- Unit: non-`product_admin` rejected.
- Integration: aggregation correctness against fixture `data_request` rows spanning success/failure/multiple periods.
- Integration: response contains no individual family-identifying data (aggregate-only contract test).
- Integration: unbounded/excessive date range rejected or capped.

## 26. Documentation
OpenAPI notes this is aggregate-only; per-record visibility is B-08.

## 27. AI Coding Agent Implementation Steps

**Task 01 — Add Aggregation Query Methods to `DataRequestRepository`**
- **Files to Modify:** `modules/data_rights/repository.py`.
- **Dependencies:** B-03 must exist first.

**Task 02 — Implement Metrics Endpoint with RBAC**
- **Files to Modify:** `admin/api.py`.
- **Definition of Done:** `product_admin` enforced; response contains no per-family identifiers.

**Task 03 — Full Test Suite & Documentation**

## 28. Definition of Done
Export-job health metrics are visible to `product_admin` in aggregate form only, with no individual-family exposure, reusing B-03's existing table without a parallel write/read path.

## 29. Final Verification Checklist
- [ ] Strictly read-only — no mutation endpoint added
- [ ] `product_admin` role enforced
- [ ] Response is aggregate-only, no per-family identifiers
- [ ] Date range bounded/capped
- [ ] No new table — reads B-03's existing `data_request`
- [ ] No PostgreSQL/Redis credential changes
