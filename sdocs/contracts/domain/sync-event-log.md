---
id: domain.sync-event-log
kind: repo
title: Sync Event Log & Idempotent Dedup Store
status: stable
owner_story: TASK-B05
version: 1
created: 2026-09-29
---

## Model Schema (`sync_event_log`)

```sql
CREATE TABLE sync_event_log (
    log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    child_id UUID NOT NULL REFERENCES children(id) ON DELETE CASCADE,
    event_type VARCHAR(64) NOT NULL,
    client_event_id VARCHAR(128) NOT NULL UNIQUE,
    occurred_at TIMESTAMPTZ NOT NULL,
    status VARCHAR(32) NOT NULL CHECK (status IN ('applied', 'duplicate', 'rejected')),
    processed_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()
);

CREATE INDEX ix_sync_event_log_child_occurred ON sync_event_log (child_id, occurred_at);
```

---

## Repository Interface

```python
class SyncEventLogRepository(BaseRepository[SyncEventLogOrm]):
    async def get_by_client_event_id(
        self,
        client_event_id: str,
    ) -> Optional[SyncEventLogOrm]: ...

    async def bulk_get_by_client_event_ids(
        self,
        ids: list[str],
    ) -> dict[str, SyncEventLogOrm]: ...

    async def record_outcome(
        self,
        log: SyncEventLogOrm,
    ) -> SyncEventLogOrm: ...

    async def prune_older_than(
        self,
        cutoff: datetime,
        batch_size: int = 10000,
        max_batches: int = 100,
    ) -> int: ...
```

---

## Core Invariants & Guarantees

1. **Unique Client Event ID Constraint (Blueprint B-05 §10 / §14)**:
   - `UNIQUE(client_event_id)` serves as the physical deduplication backbone.
   - Bulk lookup `bulk_get_by_client_event_ids()` uses a single `WHERE client_event_id IN (...)` query to eliminate N+1 latency before downstream dispatch.
2. **Savepoint-Protected Concurrency Race Safety (Blueprint B-05 §18 / §27)**:
   - `record_outcome()` wraps database insertions in nested savepoints (`async with session.begin_nested()`).
   - If two concurrent threads attempt to insert the same `client_event_id` simultaneously, the duplicate insertion traps the `IntegrityError`, rolls back cleanly without poisoning the outer transaction, and returns the existing row as `duplicate`.
3. **Rolling Audit Retention Pruning (PRD §4.5, Blueprint B-05 §5 / §10)**:
   - Automated Celery task `downloads.prune_sync_event_log` prunes rows older than 90 days.
   - Execution is bounded in sub-batches (`batch_size=10,000`, `max_batches=100`) via `SELECT log_id ... LIMIT batch_size` followed by `DELETE ... WHERE log_id IN (...)` to avoid table locks.
   - Completely decoupled from `download_record`: pruning sync event logs NEVER deletes or mutates child media downloads.
