# Blueprint: Subscription Reconciliation Job

## 1. Feature Context
Platform: NoorHeroes Backend (FastAPI + Celery). Module: `src/noorheroes/modules/subscriptions/`. Delivers the scheduled Reconciliation Job (`POST /api/v1/billing/reconcile`, Celery beat task) that catches webhook-delivery gaps by querying provider truth directly.

## 2. Parent Feature
C.24 — Subscription & Billing.

## 3. Sub-feature
B-04 — Subscription Reconciliation Job.

## 4. Objective
Run a scheduled Celery beat task that queries the store's provider-truth API for every trial/paid subscription, compares against local `subscription.state`, and auto-corrects any drift, logging every correction as an auditable event.

## 5. Business Requirements
Source: PRD §1.7 FR-6, §3.4 (`POST /api/v1/billing/reconcile`), §5 AI Code-Gen Prompt item 4, Edge Case #2.
- Runs on a schedule (Celery beat), not user-facing/on-demand by end users.
- Given webhook delivery is not guaranteed-once, this job is the platform's integrity backstop — a delayed webhook is honored within a grace window, then this job resolves any lingering ambiguity by querying the store directly.
- 100% job success rate is a hard NFR target (PRD §1.4).
- Every correction is logged as an auditable event, surfaced in N-05 (Reconciliation Job Monitor).

## 6. Existing Architecture
Per `FAST-API-INSTRUCTIONS.md`, Celery is part of the platform's infrastructure stack; no existing reconciliation-job pattern is documented in the inventory for this exact use case, though B.15/A.11 reference "reconciliation job" patterns per PRD §8 cross-ref — confirm their exact Celery task structure/naming convention before implementing rather than guessing a new one from scratch.

## 7. Existing Code to Reuse
- `SubscriptionStateMachine` (B-03) — reused here to validate/apply any corrective transition through the same legal-transition logic, not a bespoke correction path.
- `ReceiptValidationClient`/store provider-truth query capability (extend B-02's `infrastructure/store_billing/` client with a `query_subscription_status()` method).
- `SubscriptionRepository` — extend with `list_reconcilable_subscriptions()`, `record_reconciliation_correction()`.
- Existing Celery beat scheduling pattern (confirm exact `celery_app.py`/`beat_schedule` location per B.15/A.11's established pattern).

## 8. Files to Create
- `src/noorheroes/modules/subscriptions/tasks.py` — `reconcile_subscriptions` Celery beat task
- `src/noorheroes/modules/subscriptions/models.py` — add `ReconciliationCorrection` audit model (if not folded into `billing_webhook_event`)
- `tests/modules/subscriptions/test_subscription_reconciliation_job.py`

## 9. Files to Modify
- `src/noorheroes/infrastructure/store_billing/receipt_validator.py` (or a sibling client) — add `query_subscription_status()`
- `src/noorheroes/modules/subscriptions/repository.py` — add reconciliation query/record methods
- `src/noorheroes/modules/subscriptions/api.py` — add internal-only `POST /api/v1/billing/reconcile` trigger route (Celery-invoked/internal, not public)
- `celery_app.py` (or equivalent beat schedule config) — register the scheduled task

## 10. Backend Requirements
- Celery beat task `reconcile_subscriptions` (and an internal `POST /api/v1/billing/reconcile` for manual/on-demand trigger by ops):
  1. Query `SubscriptionRepository.list_reconcilable_subscriptions()` — all subscriptions in `trial`, `active_paid`, `renewal_pending`, or `past_due` state.
  2. For each, call the store provider-truth API (`query_subscription_status()`).
  3. Compare provider-truth state to local `subscription.state`.
  4. On drift, apply the correction through `SubscriptionStateMachine.transition()` (never a bespoke direct state write) and persist.
  5. Record the correction (`before_state`, `after_state`, `subscription_id`, `corrected_at`) as an auditable event.
  6. Emit `reconciliation_job_drift_corrected` analytics event.
  7. On job-level failure (not per-subscription), alert per PRD §10 DevOps ("Alert on Reconciliation Job failure or skipped runs").
- Locking: prevent overlapping runs if a prior run is still in progress (e.g., Redis lock or Celery task uniqueness).

## 11. KMP Requirements
Indirect — corrections made here are reflected the next time the client calls `GET /v1/parent/subscription` (B-05) or `GET /v1/entitlements/check` (B-06).

## 12. NextJS Requirements
Consumed read-only by N-05 (Reconciliation Job Monitor) — run history and drift corrections.

## 13. API Contract
- **HTTP Method:** POST
- **Endpoint:** `/api/v1/billing/reconcile`
- **Auth:** Internal/Celery only — not user-facing; if exposed as an HTTP route at all, gated behind an internal-service-only auth mechanism (not a parent/admin Bearer token)
- **Request:** none (or optional `{"subscription_id": "..."}` for a targeted manual re-run by ops tooling)
- **Response 200:** `{ "checked": 142, "corrected": 3, "run_id": "uuid" }`
- **Authentication:** Internal-service auth (not user-facing)
- **Authorization:** N/A (internal)
- **Validation:** N/A / optional `subscription_id` format check
- **Error Responses:** `500` on job-level failure; individual per-subscription provider-query failures are caught and logged, not raised as request-level errors

## 14. Database Requirements
Writes reconciliation-correction audit records (reuses `billing_webhook_event`-adjacent audit pattern or a dedicated `reconciliation_correction` table — confirm exact schema choice against PRD §4 before implementation; PRD does not explicitly define a separate table beyond referencing "reconciliation-correction log," so this may be modeled as a specialized `billing_webhook_event.event_type='reconciliation_correction'` row rather than a new table, pending architecture confirmation).

## 15. Validation
- Only subscriptions in an active/reconcilable state are queried (excludes already-`free`/terminal states).
- Corrections only ever move through legal state-machine transitions — never a direct state overwrite bypassing `SubscriptionStateMachine`.

## 16. Authentication
Internal/Celery-only; if an HTTP trigger route exists, it must not be reachable by parent or admin Bearer tokens.

## 17. Authorization
N/A (internal system process).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Provider-truth API unavailable for one subscription | Log, skip, continue with remaining subscriptions, do not fail the entire job run |
| Job-level failure (e.g., DB unavailable) | Alert (P0 per PRD §10), job fails cleanly, next scheduled run retries |
| Overlapping run detected | Skip/no-op with a log entry, do not run concurrently |
| Drift detected but correction would be an illegal state-machine transition | Log as an anomaly requiring manual investigation, do not force an invalid state |

## 19. Offline First
N/A (server-side scheduled job).

## 20. Local Data
N/A (backend).

## 21. Localization
N/A — internal job, no user-facing content.

## 22. RTL
N/A.

## 23. Analytics
`reconciliation_job_drift_corrected` (internal/integrity signal) per §1.19; job run summary metrics feed N-05's dashboard.

## 24. Performance
- Batch/paginate the reconcilable-subscription query to avoid a single unbounded query against a large subscriber base.
- Rate-limit/throttle calls to the store provider-truth API per store API quota constraints.
- Bounded total job runtime with alerting if a run exceeds an expected window.

## 25. Security
- No entitlement is ever granted or corrected by this job outside a legal state-machine transition — the same integrity guarantee as B-03.
- Internal-only reachability (not exposed to parent or admin Bearer-token auth paths).

## 26. Library Requirements
Celery (existing platform dependency); reuses B-02's store API client, extended with a status-query method.

## 27. Testing
1. Unit test: local state drifted from mocked provider-truth response → job corrects it, records the correction (PRD §5 item 4).
2. Unit test: no drift detected → no correction recorded, job completes cleanly.
3. Unit test: correction attempted only via `SubscriptionStateMachine.transition()`, never a direct write (structural/mock-call-assertion test).
4. Unit test: provider-truth API failure for one subscription doesn't halt the batch.
5. Unit test: overlapping run prevention (lock behavior).
6. Integration test: full reconciliation cycle against a store sandbox fixture with a deliberately injected drift scenario.
7. Integration test: job-failure alerting hook fires on a simulated DB outage mid-run.

## 28. Documentation
Task docstring explaining the reconciliation role as the platform's integrity backstop; runbook entry describing how to manually trigger a targeted reconciliation for a single subscription during a support investigation.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Extend Store Client with Provider-Truth Query**
- Task ID: B04-T01
- Objective: `query_subscription_status(subscription_ref)` against the store's own subscription-status API.
- Why This Is Required: The reconciliation job's core data source.
- Existing Architecture to Follow: Extend B-02's `infrastructure/store_billing/` client.
- Existing Files to Reuse: `receipt_validator.py` (B-02, Task 01).
- Files to Create: none (extend existing file, or add sibling module).
- Files to Modify: `infrastructure/store_billing/receipt_validator.py`.
- Implementation Details: Async method returning current provider-side subscription state.
- Business Rules: FR-6.
- Validation: N/A.
- Error Handling: Per-call timeout/failure typed distinctly from a "confirmed canceled" result.
- Security: No raw provider response logged beyond necessary state fields.
- Performance: Respect store API rate limits.
- Localization/RTL/Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: Docstring.
- Dependencies: B-02 Task 01.
- Do Not Change: Do not duplicate the receipt-validation logic — this is a distinct query, not a purchase verification.
- Expected Result: Reliable provider-truth state query.
- Definition of Done: Returns correct state for a known sandbox subscription.

**Task 02 — Implement Reconciliation Repository Methods**
- Task ID: B04-T02
- Objective: `list_reconcilable_subscriptions()`, `record_reconciliation_correction()`.
- Why This Is Required: Data access for the job.
- Existing Architecture to Follow: `BaseRepository[ModelT]`.
- Existing Files to Reuse: `SubscriptionRepository`.
- Files to Create: none (or new audit model if required per §14).
- Files to Modify: `repository.py`, possibly `models.py`.
- Implementation Details: Filter by reconcilable states; audit record includes before/after state, timestamp, subscription reference.
- Business Rules: FR-6.
- Validation: N/A.
- Error Handling: N/A.
- Security: No PII beyond existing subscription-record exposure.
- Performance: Paginated/batched query.
- Localization/RTL/Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: Docstring.
- Dependencies: none.
- Do Not Change: N/A.
- Expected Result: Queryable reconcilable set; correction records persisted.
- Definition of Done: Matches §14 schema decision.

**Task 03 — Implement Celery Beat Task**
- Task ID: B04-T03
- Objective: `reconcile_subscriptions` scheduled task per §10.
- Why This Is Required: The scheduled execution vehicle for this entire sub-feature.
- Existing Architecture to Follow: Existing Celery beat registration pattern (confirm against B.15/A.11's actual task file structure).
- Existing Files to Reuse: Tasks 01–02, B-03's `SubscriptionStateMachine`.
- Files to Create: `modules/subscriptions/tasks.py`.
- Files to Modify: `celery_app.py`/beat schedule config.
- Implementation Details: Per §10 steps 1–7; overlapping-run lock; batched processing.
- Business Rules: FR-6.
- Validation: Per §15.
- Error Handling: Per §18.
- Security: Corrections only via `SubscriptionStateMachine`.
- Performance: Batched, rate-limited, bounded runtime.
- Localization/RTL: N/A.
- Analytics: Emit `reconciliation_job_drift_corrected`.
- Tests: Covered in Task 04.
- Documentation: Task docstring + runbook note.
- Dependencies: Tasks 01–02, B-03.
- Do Not Change: Do not bypass the state machine for "quick" corrections.
- Expected Result: Job runs on schedule, corrects drift.
- Definition of Done: Matches §10 exactly.

**Task 04 — Write Test Suite**
- Task ID: B04-T04
- Objective: Cover all 7 scenarios in §27.
- Why This Is Required: 100% job-success-rate NFR target; CI confidence in the integrity backstop.
- Existing Architecture to Follow: pytest, Celery task testing pattern (eager mode), mocked store client.
- Existing Files to Reuse: Fixture factories for drifted-state scenarios.
- Files to Create: `tests/modules/subscriptions/test_subscription_reconciliation_job.py`.
- Files to Modify: none.
- Implementation Details: 7 test cases per §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert partial-failure resilience.
- Security: Assert corrections only occur via the state machine (mock/spy assertion).
- Performance: N/A.
- Localization/RTL: N/A.
- Analytics: Assert event emission on correction.
- Tests: This task IS the tests.
- Documentation: Test docstrings.
- Dependencies: Tasks 01–03.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 covered and green.

## 30. Definition of Done
`reconcile_subscriptions` Celery beat task runs on schedule, queries provider truth for every trial/paid subscription, corrects drift exclusively through `SubscriptionStateMachine`, logs every correction auditable, resilient to partial per-subscription failures, all tests green.

## 31. Final Verification Checklist
- [ ] Drift-correction test passes against a mocked provider-truth mismatch
- [ ] Corrections only ever applied via `SubscriptionStateMachine.transition()`
- [ ] Partial provider-API failure doesn't halt the full batch
- [ ] Overlapping-run prevention verified
- [ ] Job-failure alerting hook verified
- [ ] Correction audit record captures before/after state and timestamp
- [ ] Not reachable via parent/admin Bearer-token auth paths
