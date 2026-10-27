# B-05 — Sync Event Log & Idempotent Dedup Store

## 1. Feature Context
Part of Feature B.15 (Offline Downloads & Sync). The persistence backbone underneath B-04 — an append-only audit log whose `UNIQUE(client_event_id)` constraint is the mechanism that makes pre-downstream-call dedup possible at all.

## 2. Parent Feature
B.15 — Offline Downloads & Sync

## 3. Sub-feature
B-05 — Sync Event Log & Idempotent Dedup Store

## 4. Objective
Implement the `sync_event_log` table, its `SyncEventLogRepository`, and a scheduled retention/pruning job, providing B-04 with a fast, race-safe dedup-lookup path and an audit trail distinguishing `applied`/`duplicate`/`rejected` outcomes.

## 5. Business Requirements
- FR-4: server deduplicates using idempotency keys.
- §4.3 Audit Fields: `sync_event_log` is append-only — every sync attempt logged, `status` distinguishing outcomes.
- §4.5 Retention Rules: `sync_event_log` retained for a rolling audit window (e.g., 90 days), then pruned — business-impact data lives permanently in each owning domain's own tables, not here.
- Edge Case 12: already-synced events' idempotency keys must reliably prevent reprocessing on accidental resubmission, even under concurrent/racing batch calls.

## 6. Existing Architecture
Table and repository live in the same new `downloads` bounded context (`src/noorheroes/modules/downloads/models.py` extended, `repository.py` extended) — not a separate context, since this table has no independent public API and exists solely to serve B-04.

## 7. Existing Code to Reuse
- `infrastructure/db/base.py` → `Base`, `TimestampMixin` (`created_at`/`updated_at`/`version`) — note: `sync_event_log` uses `processed_at` in addition to the mixin's `created_at`, since "logged" and "processed" are distinct moments for a `rejected`/retried event.
- `common/base_repository.py` → `BaseRepository[ModelT]` for standard CRUD, extended with a dedicated fast-path lookup method.
- Existing Celery infrastructure (per `localization/tasks.py`'s established pattern) for the retention/pruning scheduled job.

## 8. Files to Create
- `src/noorheroes/modules/downloads/models.py` (extend) — `SyncEventLogOrm`.
- `src/noorheroes/modules/downloads/tasks.py` — `prune_sync_event_log_task()` Celery periodic task.
- `tests/modules/downloads/test_sync_event_log_dedup_race.py`.
- `tests/modules/downloads/test_sync_event_log_retention_pruning.py`.
- Alembic migration: `create_sync_event_log_table.py`.

## 9. Files to Modify
- `modules/downloads/repository.py` — add `SyncEventLogRepository` with `get_by_client_event_id()`, `bulk_get_by_client_event_ids()`, `record_outcome()`.
- Celery beat schedule config — register `prune_sync_event_log_task` on a daily cadence.

## 10. Backend Requirements
- `sync_event_log` schema: `log_id UUID PK`, `child_id UUID FK`, `event_type VARCHAR`, `client_event_id VARCHAR UNIQUE`, `occurred_at TIMESTAMPTZ`, `status VARCHAR CHECK IN ('applied','duplicate','rejected')`, `processed_at TIMESTAMPTZ`.
- `bulk_get_by_client_event_ids()`: single `IN (...)` query for B-04's batch dedup lookup, avoiding N round-trips.
- `record_outcome()`: single-row insert, relying on the `UNIQUE(client_event_id)` constraint to make a racing concurrent insert for the same key fail safely (caught and treated as `duplicate` by B-04, not a `500`).
- `prune_sync_event_log_task()`: deletes rows older than the retention window (e.g., 90 days) in batched deletes to avoid long-held locks on a large table.

## 11. KMP Requirements
No direct KMP consumer — reachable only via B-04.

## 12. NextJS Requirements
No direct NextJS consumer — B-07 aggregates over this table (read-only) for N-02's metrics.

## 13. API Contract
No public HTTP endpoint — internal repository interface only:
```python
async def get_by_client_event_id(client_event_id: str) -> Optional[SyncEventLogOrm]: ...
async def bulk_get_by_client_event_ids(ids: list[str]) -> dict[str, SyncEventLogOrm]: ...
async def record_outcome(log: SyncEventLogOrm) -> SyncEventLogOrm: ...
```

## 14. Database Requirements
- New table `sync_event_log`: `UNIQUE(client_event_id)` is the dedup backbone; `INDEX (child_id, occurred_at)` for causal-order/audit queries.
- Append-only by convention — no `UPDATE`/`soft_delete` methods exposed on `SyncEventLogRepository`; only `INSERT` (`record_outcome`) and the pruning job's batched hard `DELETE`.
- No PostgreSQL/Redis credential changes.

## 15. Validation
`client_event_id` validated as non-empty by B-04's schema layer before reaching this repository; the `UNIQUE` DB constraint is the authoritative, race-safe enforcement — application-level pre-checks are a performance optimization, not the security boundary.

## 16. Authentication
N/A — internal repository, inherits caller's (B-04's) auth context.

## 17. Authorization
N/A — internal repository; `child_id` scoping is the caller's responsibility.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Concurrent insert race on same `client_event_id` | DB `UNIQUE` violation caught by B-04, treated as `duplicate`, not a `500` |
| Pruning job partial failure | Resumable — job re-run picks up remaining old rows; pruning is idempotent (deleting an already-deleted row range is a no-op) |
| Bulk lookup with empty ID list | Returns empty dict, no query executed |

## 19. Offline First
N/A (backend).

## 20. Local Data
N/A (backend).

## 21. Localization
N/A.

## 22. RTL
N/A.

## 23. Analytics
No direct emission — this table is the data source for B-07's `offline_sync_duplicate_prevented`-equivalent aggregate metric.

## 24. Performance
- `UNIQUE(client_event_id)` index doubles as the dedup-lookup index — no separate index needed.
- Batched pruning deletes (e.g., 10,000 rows per transaction) to avoid long lock hold times on a table that may grow large under high sync volume.
- `bulk_get_by_client_event_ids()` is mandatory for B-04's batch path — a per-event lookup loop is explicitly disallowed (N+1 anti-pattern).

## 25. Security
Append-only + `UNIQUE` constraint together make this table the non-bypassable source of truth for "has this event already been applied" — no code path outside `SyncEventLogRepository` may write to it directly (enforced by module-boundary convention, verified in code review).

## 26. Library Requirements
SQLAlchemy 2.0 (async), asyncpg, Celery (existing infra). No new libraries.

## 27. Testing
- Unit: `bulk_get_by_client_event_ids()` returns correct subset for a mixed known/unknown ID list.
- **Race test (mandatory):** two concurrent `record_outcome()` calls for the same `client_event_id` — assert exactly one succeeds, the other raises a caught `IntegrityError` translatable to `duplicate` by B-04.
- Integration: pruning job removes only rows older than the retention window, leaves recent rows untouched, and is safely re-runnable.

## 28. Documentation
Docstring on `SyncEventLogOrm` explicitly noting append-only convention and the retention window; docstring on `record_outcome()` explaining the caller's responsibility to catch and translate `IntegrityError`.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Create SyncEventLogOrm Model & Migration**
Files to create: extend `modules/downloads/models.py`, migration file.
Expected result: table exists with `UNIQUE(client_event_id)` and `(child_id, occurred_at)` index.

**Task 02 — Implement SyncEventLogRepository**
Objective: `get_by_client_event_id()`, `bulk_get_by_client_event_ids()`, `record_outcome()`.
Files to modify: `modules/downloads/repository.py`.

**Task 03 — Implement Retention Pruning Task**
Objective: `prune_sync_event_log_task()`, batched deletes, Celery-beat-scheduled.
Files to create: `modules/downloads/tasks.py`.

**Task 04 — Add Race-Safety Test (highest priority)**
Tests: `test_sync_event_log_dedup_race.py`.

**Task 05 — Add Retention Pruning Test**
Tests: `test_sync_event_log_retention_pruning.py`.

**Task 06 — Final Code Review**
Objective: confirm no code path outside `SyncEventLogRepository` writes to `sync_event_log` directly.

## 30. Definition of Done
- `sync_event_log` table live with correct constraints/indexes.
- `bulk_get_by_client_event_ids()` integrated into B-04's dedup path.
- Retention pruning job scheduled and verified idempotent.
- Race-safety test green.

## 31. Final Verification Checklist
- [ ] `UNIQUE(client_event_id)` constraint present and enforced at the DB level.
- [ ] Concurrent racing writes for the same key resolve safely (one succeeds, one caught as duplicate).
- [ ] Bulk lookup used by B-04, no N+1 per-event lookup loop.
- [ ] Pruning job batched, idempotent, and safely re-runnable.
- [ ] No code outside `SyncEventLogRepository` writes to this table.
- [ ] No PostgreSQL/Redis credentials modified.
