# B-06 — Admin Gate & Lockout Health Monitoring API

## 1. Feature Context
A read-only aggregate dashboard feed giving `product_admin`/`trust_safety` staff visibility into lock-verification failure rates, lockout-trigger frequency by lock type, and Parent Gate success/failure rates — without ever exposing raw PIN/pattern/biometric data.

## 2. Parent Feature
Feature C.19 — Parent PIN/Biometric Gate & Profile Access Control

## 3. Sub-feature
1.6 Admin Gate & Lockout Health Monitoring API (ID: **B-06**)

## 4. Objective
Implement `GET /v1/admin/security/gate-health-metrics`, aggregating B-01/B-03's lockout and verification outcomes into trend/frequency metrics, restricted to `product_admin`/`trust_safety` roles, read-only.

## 5. Business Requirements
- Admin Requirements §8: Gate/Lockout Health Monitor — read-only, `product_admin`/`trust_safety` roles.
- §11.3: lock-type distribution, lockout-trigger frequency, grace-window utilization rate, restriction-check-failure-reason breakdown.
- Never displays raw PINs, patterns, or biometric data (hard rule, §9 item 2).

## 6. Existing Architecture
Extends `modules/admin/`. Reads aggregate data derived from B-01's `child_lock` lockout events and B-03's `parent_pin` lockout events and B-04's `failure_reason` distribution — via either a dedicated append-only `gate_event_log` table populated by B-01/B-03/B-04 on each verification/lockout event, or a scheduled aggregation job. Recommend an append-only `gate_event_log` for accurate trend analysis (confirm against existing analytics-event-bus pattern before introducing a new table — B.17/other modules may already emit to a shared event bus that this can consume instead of a bespoke table).

## 7. Existing Code to Reuse
- `modules/admin/repository.py::AdminAuditRepository` (pattern reference, not directly reused for metrics)
- `core/deps.py::get_current_admin`, `require_admin_scope`
- Existing Analytics Event Bus (PRD §3.2 architecture diagram references `EVENTBUS` — confirm exact module before building a parallel logging path)

## 8. Files to Create
- `src/noorheroes/modules/access_gate/gate_event_models.py` — `GateEventOrm` (append-only: `event_type`, `lock_type`, `outcome`, `child_id`/`parent_id` nullable, `family_id`, `created_at`) — only if no existing event bus can be queried directly
- `src/noorheroes/modules/admin/gate_health_schemas.py` — `GateHealthMetricsResponse`
- `src/noorheroes/modules/admin/gate_health_service.py` — `GateHealthMetricsService(BaseService)` (read-only, aggregation queries)
- `alembic/versions/xxxx_add_gate_event_log.py` (only if new table required)
- `tests/modules/admin/test_gate_health_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/admin/api.py` — add `GET /v1/admin/security/gate-health-metrics`
- `src/noorheroes/modules/access_gate/lock_service.py` (B-01) — emit event on verify/lockout
- `src/noorheroes/modules/identity/pin_service.py` (B-03) — emit event on verify/lockout
- `src/noorheroes/modules/access_gate/session_service.py` (B-04) — emit event on restriction failure

## 10. Backend Requirements
- `GateHealthMetricsService.get_metrics(date_range, filters)`:
  1. Aggregate lock-verification failure rate (failures / total attempts) over the requested range.
  2. Aggregate lockout-trigger frequency grouped by `lock_type`.
  3. Aggregate Parent Gate success/failure rate.
  4. Aggregate restriction-check `failure_reason` breakdown (from B-04).
  5. All queries strictly aggregate-only — no query path returns row-level PIN/pattern/hash data; the response schema structurally excludes any credential field.
- Support date-range and optional `lock_type`/`family_id`-scoped filtering (family-scoped only for `trust_safety` investigations, not general dashboard use).

## 11. API Contract

### `GET /v1/admin/security/gate-health-metrics`
- **Auth:** Bearer (admin), `require_admin_scope("product_admin")` or `require_admin_scope("trust_safety")`
- **Query Params:** `start_date`, `end_date`, `lock_type` (optional)
- **Response 200:** `{ "lock_verification_failure_rate": 0.04, "lockout_trigger_frequency": {"pin": 12, "pattern": 3, "fingerprint": 0}, "parent_gate_success_rate": 0.97, "restriction_failure_breakdown": {"screen_time_exhausted": 8, "bedtime_window": 5, ...} }`
- **Error Responses:** `401 UNAUTHORIZED`, `403 FORBIDDEN`, `422 INVALID_DATE_RANGE`

## 12. Database Requirements
Either a new append-only `gate_event_log` table (if no existing event bus is queryable) or aggregation over the existing Analytics Event Bus's storage. Read-only for this endpoint regardless.

## 13. Validation
`start_date`/`end_date` valid ISO dates, `end_date >= start_date`, range capped (e.g., max 90 days) to bound aggregation query cost.

## 14. Authentication
Bearer token for an authenticated admin user.

## 15. Authorization
`product_admin` or `trust_safety` role only. Strictly read-only — no update/delete capability exists on this endpoint or module.

## 16. Error Handling
| Scenario | Response |
|---|---|
| Unauthorized role | `403 FORBIDDEN` |
| Invalid date range | `422 INVALID_DATE_RANGE` |
| No data in range | `200` with zeroed/empty aggregates, not an error |
| Database failure | `500 INTERNAL_ERROR` |

## 17. Offline First
N/A — admin dashboard, always-online.

## 18. Analytics
This endpoint **is** the analytics surface; no further instrumentation needed beyond standard admin-page-view tracking if the Admin Portal has a global convention for that.

## 19. Performance
Aggregation queries should use appropriate indexes on `created_at`/`event_type`/`lock_type`; consider a materialized view or periodic rollup if the underlying event volume grows large, rather than raw aggregation on every dashboard load — add caching (short TTL, e.g., 5 min) if load testing shows this is necessary.

## 20. Security
- Structurally impossible to leak raw credential data — the response schema has no field capable of carrying it, and the underlying query never selects `value_hash`/`pin_hash` columns.
- Read-only role separation strictly enforced.

## 21. Library Requirements
FastAPI, SQLAlchemy 2.0, Pydantic v2, Redis (optional, for short-TTL caching), pytest.

## 22. Testing
- Unit: response schema never includes any credential-adjacent field (structural/type-level assertion).
- Unit: non-`product_admin`/`trust_safety` role rejected with `403`.
- Integration: aggregation correctness against seeded lockout/verification event fixtures.
- Integration: date-range validation edge cases (inverted range, > max span).

## 23. Documentation
OpenAPI docs list all aggregate fields with descriptions; explicitly note in the description that this endpoint never returns row-level or credential data.

## 24. AI Coding Agent Implementation Steps

**Task 01 — Confirm/Build Event-Logging Path**
Objective: determine whether an existing Analytics Event Bus can be queried directly, or whether `gate_event_log` is needed. Files to Create (if needed): `gate_event_models.py`, migration. Dependencies: none — do this first to avoid rework in B-01/B-03/B-04.

**Task 02 — Instrument B-01/B-03/B-04 to Emit Gate Events**
Objective: wire event emission into existing verify/lockout/restriction-failure code paths. Files to Modify: `lock_service.py`, `pin_service.py`, `session_service.py`. Dependencies: Task 01.

**Task 03 — Implement `GateHealthMetricsService.get_metrics()`**
Objective: aggregation queries per §10. Files to Create: `gate_health_service.py`. Dependencies: Task 02.

**Task 04 — Implement `GET /v1/admin/security/gate-health-metrics` Router**
Objective: wire `require_admin_scope`, query params, response schema. Files to Create: `gate_health_schemas.py`. Files to Modify: `api.py`. Dependencies: Task 03.

**Task 05 — Add Full Test Suite & API Docs**
Objective: coverage per §22, including the structural no-credential-leak assertion. Dependencies: Task 04.

## 25. Definition of Done
`GET /v1/admin/security/gate-health-metrics` is live, restricted to `product_admin`/`trust_safety`, aggregates lockout/verification/restriction-failure data accurately, and is structurally incapable of leaking credential data.

## 26. Final Verification Checklist
- [x] Response schema has no field capable of carrying credential data
- [x] Only `product_admin`/`trust_safety` roles can access this endpoint
- [x] Aggregation correctness verified against seeded fixtures
- [x] Date-range validation covers inverted ranges and max-span overflow
- [x] No write/update capability exists anywhere in this module

