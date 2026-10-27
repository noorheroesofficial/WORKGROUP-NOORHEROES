# B-03 — Wallet Projection & Reconciliation Service

## 1. Feature Context
Part of Feature A.11 — Rewards System. Maintains the derived, fully rebuildable `reward_wallets` cache and the standing integrity job that self-heals any drift against the append-only ledger (B-01).

## 2. Parent Feature
A.11 Rewards System — Backend (FastAPI)

## 3. Sub-feature
B-03 Wallet Projection & Reconciliation Service

## 4. Objective
Implement `recompute_wallet(child_id)` as a fully rebuildable projection and a scheduled reconciliation job that detects and self-heals wallet-balance drift, backing FR-3, FR-14 and the Integrity NFR.

## 5. Business Requirements
- `reward_wallets.cached_balance` is a repairable projection, never a direct write target outside this service.
- The reconciliation job runs on a configurable interval (e.g., hourly), corrects drift, and logs every correction as a distinct audit event.
- Wallet-balance-projection accuracy target: 100%, verified via this standing job (PRD §1.4).

## 6. Existing Architecture
Celery is already part of the platform's infrastructure stack (`FAST-API-INSTRUCTIONS.md` — Celery listed alongside PostgreSQL/Redis/R2/OpenTelemetry). This task follows the existing Celery-task convention used by `localization`'s `translate_content_task` (`modules/localization/tasks.py`) as the direct precedent for a scheduled/background task in this codebase.

## 7. Existing Code to Reuse
- Celery app/worker configuration (existing infra).
- `translate_content_task` (`modules/localization/tasks.py`) as the structural precedent for task definition/scheduling.
- B-01's `reward_ledger` read access.

## 8. Files to Create
- `src/noorheroes/modules/rewards/models.py` — add `RewardWallet` model (if not already minimally present) and `ReconciliationIncident` audit model.
- `src/noorheroes/modules/rewards/projection.py` — `recompute_wallet(child_id)`.
- `src/noorheroes/modules/rewards/tasks.py` — `reconcile_wallets_task` (Celery, scheduled).
- `alembic/versions/<rev>_create_reward_wallets_reconciliation_tables.py`
- `tests/modules/rewards/test_wallet_projection_rebuild.py`
- `tests/modules/rewards/test_reconciliation_job.py`

## 9. Files to Modify
- `src/noorheroes/modules/rewards/service.py` — inject projection module for use by B-02's wallet reads.
- Celery beat schedule config — register `reconcile_wallets_task` on an hourly (configurable) interval.

## 10. Backend Requirements
- `recompute_wallet(child_id)`: sums **all** `reward_ledger` rows for that child from scratch, writes the result to `reward_wallets.cached_balance`/`xp` — a pure, idempotent, side-effect-only-on-that-table operation.
- Reconciliation job: for every child whose `reward_wallets.cached_balance` does not match a live ledger-sum query, call `recompute_wallet`, and insert a `ReconciliationIncident` row (`child_id`, `old_balance`, `new_balance`, `timestamp`).
- Job must be safely re-runnable and must not double-correct or thrash under concurrent runs (use a row lock or advisory lock per child during correction).
- Alert (P0) on correction-volume spikes (hook for N-06/DevOps monitoring).

## 11. KMP Requirements
Not applicable (backend-only); indirectly benefits K-02's wallet display accuracy.

## 12. NextJS Requirements
Read-only surface for reconciliation incidents is N-06 (Reconciliation Incident Log), backed by B-13.

## 13. API Contract
No public HTTP endpoint — internal projection function + scheduled Celery task. `ReconciliationIncident` rows are exposed read-only via B-13's admin endpoint.

## 14. Database Requirements
- `reward_wallets`: `child_id UUID PK/FK`, `currency VARCHAR`, `cached_balance INT`, `xp INT`, `updated_at TIMESTAMPTZ`. No application write grant outside this module's projection function.
- `reconciliation_incidents`: `id UUID PK`, `child_id UUID FK`, `old_balance INT`, `new_balance INT`, `corrected_at TIMESTAMPTZ`.
- Index `(child_id)` on both tables.

## 15. Validation
- Test: manually corrupt a wallet's `cached_balance`, run `recompute_wallet`, assert corrected to the true ledger sum.
- Test: reconciliation job touches only genuinely-drifted children's wallets, leaves correct ones untouched, with an incident row per correction.

## 16. Authentication
N/A (internal service/scheduled task).

## 17. Authorization
N/A (no direct external caller); incident data exposed read-only to `trust_safety`/`product_admin` via B-13.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Drift detected | Self-heal via `recompute_wallet`, log incident, continue to next child |
| Concurrent award during reconciliation for the same child | Row/advisory lock ensures the recompute reflects a consistent snapshot; a subsequent award simply updates the now-correct baseline normally |
| Reconciliation job itself fails mid-run | Resumable — job processes children independently, a partial run leaves already-corrected children corrected; job re-run picks up remaining drifted children |

## 19. Offline First
N/A (backend).

## 20. Local Data
N/A (backend).

## 21. Localization
N/A.

## 22. RTL
N/A.

## 23. Analytics
Emit `wallet_reconciliation_drift_corrected` (internal) per PRD §1.19.

## 24. Performance
Job must not starve normal request throughput; batched processing (e.g., paginated child cursor) rather than a single unbounded query across the full child population.

## 25. Security
Prevents wallet-balance manipulation via cache tampering by making the cache fully rebuildable and continuously self-verified (PRD §12.1).

## 26. Library Requirements
Celery, SQLAlchemy 2.0 async, PostgreSQL advisory locks or row-level locking, Alembic.

## 27. Testing
- Unit: `recompute_wallet` correctness against a fixture ledger.
- Integration: full reconciliation-job run against a mixed drifted/correct child population.
- Load: reconciliation across a large simulated child population within an acceptable job-duration budget.

## 28. Documentation
Operational runbook note: how to manually trigger reconciliation for a single child (support tooling), and how correction-volume alerting works.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create `reward_wallets` & `reconciliation_incidents` Models + Migration**
- Files to Create: models + migration per §8/§14.
- Definition of Done: tables created, no stray write grants beyond this module.

**Task 02 — Implement `recompute_wallet(child_id)`**
- Files to Create: `projection.py`
- Business Rules: FR-3.
- Tests: corrupted-balance-correction test.
- Definition of Done: idempotent, correct rebuild from ledger sum.

**Task 03 — Implement Scheduled Reconciliation Task**
- Files to Create: `tasks.py`
- Existing Files to Reuse: `translate_content_task` scheduling pattern.
- Implementation Details: per-child drift detection, locked correction, incident logging.
- Performance: batched/paginated child processing.
- Tests: mixed-population reconciliation test.
- Definition of Done: job runs correctly on schedule, only touches drifted wallets.

**Task 04 — Wire Alerting Hook**
- Implementation Details: emit a structured log/metric on correction-volume spike, consumed by DevOps monitoring (N-06 cross-reference).
- Definition of Done: alert-worthy signal verifiably emitted under a simulated spike.

**Task 05 — Add Documentation**
- Documentation: operational runbook per §28.
- Definition of Done: reviewed and merged.

**Task 06 — Final Code Review**
- Do Not Change: `reward_ledger` (read-only from this module); PostgreSQL/Redis credentials.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Wallet projection fully rebuildable from the ledger; scheduled reconciliation self-heals drift and logs every correction; no other module can write `reward_wallets` directly.

## 31. Final Verification Checklist
- [x] `recompute_wallet` proven idempotent and correct against fixture ledgers
- [x] Reconciliation job corrects only drifted wallets, logs an incident per correction
- [x] Job is safely re-runnable / lock-protected against concurrent correction
- [x] Correction-volume alerting hook verified
- [x] No application write grant on `reward_wallets` outside this module
- [x] Operational runbook documented
