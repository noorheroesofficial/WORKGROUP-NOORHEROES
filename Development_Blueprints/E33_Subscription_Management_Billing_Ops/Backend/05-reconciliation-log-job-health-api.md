# B-05 — Reconciliation Log & Job Health API

## 1. Feature Context
A read-only inspection window into C.24's already-hardened nightly reconciliation job — this sub-feature introduces no new drift-detection or auto-correction algorithm, it only surfaces the job's own output and run history for operational monitoring and dispute investigation.

## 2. Parent Feature
E.33 — Subscription Management & Billing Ops

## 3. Sub-feature
1.5 Reconciliation Log & Job Health API (ID: **B-05**)

## 4. Objective
Build `GET /v1/admin/reconciliation-log` and `GET /v1/admin/reconciliation-job/health`, reading exclusively from C.24's existing reconciliation job output.

## 5. Business Requirements
- FR-9: the Reconciliation Log Viewer surfaces every drift-correction event with before/after entitlement state, affected subscription, and timestamp.
- §5 Backend AI prompt item 6: read from C.24's existing reconciliation-job output, no new reconciliation algorithm.
- Edge Case 3: a missed job run is itself an alertable incident, and the next successful run must still catch accumulated drift — never silently treated as "nothing to reconcile."

## 6. Existing Architecture
`subscriptions` bounded context, `app/subscriptions/routers/reconciliation_router.py`, reading from C.24's existing `reconciliation_event` output table and job-run-history log — this sub-feature owns only the admin-facing read endpoints, not the job itself.

## 7. Existing Code to Reuse
- C.24: `app/subscriptions/services/reconciliation_job_service.py` (the job itself, unmodified)
- Cross-ref E.28's general job-failure monitoring widget/pattern

## 8. Files to Create
- `app/subscriptions/routers/reconciliation_router.py`
- `app/subscriptions/services/reconciliation_log_service.py` — read-only
- `app/subscriptions/repositories/reconciliation_log_repository.py` — read-only
- `app/subscriptions/schemas/reconciliation_schema.py`

## 9. Files to Modify
- `app/subscriptions/routers/__init__.py` — register router

## 10. Backend Requirements
- `ReconciliationLogService.get_log(date_from, date_to)`: reads `reconciliation_event` rows (owned by C.24, append-only) within the date range, no write path.
- `ReconciliationLogService.get_job_health()`: reads run-history metadata (last-successful-run timestamp, failure count) from C.24's job's own logging/metadata table — never recomputes or infers job health independently.
- This service has no method that triggers, retries, or modifies the reconciliation job itself — strictly observational.

## 11. Required API / API Contract
`GET /v1/admin/reconciliation-log?date_from=&date_to=` → `200` list with before/after state.
`GET /v1/admin/reconciliation-job/health` → `200 { last_successful_run, failure_count, recent_runs: [...] }`.

## 12. Database Requirements
No new tables — reads C.24's existing `reconciliation_event` and job-run-metadata tables.

## 13. Validation
`date_from`/`date_to` valid date range, `date_from <= date_to`.

## 14. Authentication
`get_current_admin`.

## 15. Authorization
`require_admin_scope("billing_ops")` (mutating-adjacent financial-integrity visibility; may extend to broader read access if PRD's `support`+ pattern applies — confirmed as `billing_ops`/`super_admin` per §2.3's click-mapping table for this specific screen).

## 16. Error Handling
`422` for invalid date range; empty list (not error) for no drift in the given period, matching the PRD's "No drift detected — all entitlements in sync" empty state.

## 17. Security
Strictly read-only by construction — mandatory structural test confirms zero write/trigger/retry method exists anywhere in this service, ensuring an admin can observe but never directly manipulate the reconciliation process itself.

## 18. Analytics
`reconciliation_job_run_completed` (with `drift_count`), `reconciliation_drift_corrected`, `reconciliation_job_failed` per §1.19.

## 19. Performance
Indexed on `reconciliation_event(subscription_id, corrected_at DESC)` (already specified by C.24's schema, §4.2), date-range-filtered queries.

## 20. Library Requirements
FastAPI, Pydantic v2, SQLAlchemy 2.0 async. No new libraries.

## 21. Testing
Unit: date-range validation. Integration: **mandatory** — this endpoint correctly surfaces a fixture drift-correction event with accurate before/after state, sourced from C.24's existing output, not a reimplemented computation; **mandatory** — structural test confirming zero write/trigger method exists in this service; job-health endpoint correctly reflects a fixture missed-run-then-recovered scenario (Edge Case 3).

## 22. Documentation
OpenAPI docstring noting this service is strictly observational over C.24's reconciliation job.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Define Schemas**
Objective: `ReconciliationEventSummary`, `JobHealthSummary`. Files: `schemas/reconciliation_schema.py`. Tests: schema validation. Definition of Done: schema used by Task 03.

**Task 02 — Implement `ReconciliationLogRepository` (Read-Only)**
Objective: Date-range-filtered reads from C.24's existing tables. Files: `repositories/reconciliation_log_repository.py`. Dependencies: Task 01. Tests: repository tests. Definition of Done: tests pass.

**Task 03 — Implement `ReconciliationLogService`**
Objective: `get_log()`, `get_job_health()`, both strictly read-only. Files: `services/reconciliation_log_service.py`. Dependencies: Task 02. Tests: **mandatory** — accurate before/after surfacing test. Definition of Done: test passes.

**Task 04 — Implement Router Endpoints**
Objective: Wire both endpoints, `billing_ops`-scope-gated. Files: `routers/reconciliation_router.py`. Dependencies: Task 03. Tests: endpoint integration tests. Definition of Done: tests pass.

**Task 05 — Confirm Strictly-Observational Guarantee**
Objective: **Mandatory** structural test confirming zero write/trigger/retry method exists in this service. Dependencies: Task 03. Definition of Done: test passes.

**Task 06 — Add Full Test Suite**
Objective: Complete coverage per §21, all mandatory tests included. Definition of Done: all green in CI.

**Task 07 — Final Code Review**
Objective: Confirm no reconciliation algorithm was reimplemented, only read access added. Definition of Done: checklist in §24 checked.

## 24. Final Verification Checklist
- [ ] Reads exclusively from C.24's existing reconciliation-job output — no reimplemented algorithm
- [ ] Zero write/trigger/retry method exists in this service — mandatory structural test passing
- [ ] Before/after state surfaced accurately for each drift-correction event
- [ ] Job health endpoint correctly reflects missed-then-recovered run scenarios
- [ ] `billing_ops` scope enforced

## 25. Definition of Done
Billing Ops has full observational visibility into reconciliation drift-correction history and job health, sourced entirely and provably from C.24's existing, already-hardened reconciliation engine.
