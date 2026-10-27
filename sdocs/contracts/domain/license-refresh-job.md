---
id: domain.license-refresh-job
kind: worker
title: License & Entitlement Periodic Refresh Job (downloads.refresh_download_entitlements)
status: stable
owner_story: TASK-B06
version: 1
created: 2026-09-29
---

## Celery Worker Contract

```python
@celery_app.task(
    name="downloads.refresh_download_entitlements",
    acks_late=True,
    max_retries=3,
    default_retry_delay=300,
)
def refresh_download_entitlements_task(
    batch_size: int = 100,
    max_batches: int = 100,
    initial_cursor: Optional[str] = None,
) -> Dict[str, Any]: ...
```

## Periodic Beat Schedule Contract

```python
beat_schedule["refresh_download_entitlements_periodic"] = {
    "task": "downloads.refresh_download_entitlements",
    "schedule": 21600.0,  # Runs every 6 hours
    "args": (100, 100),
}
```

## Outbox Telemetry Event Contract

```python
class DownloadEntitlementsRefreshed(NoorHeroesBaseModel):
    scanned_count: int = Field(default=0, description="Total completed records scanned.")
    expired_count: int = Field(default=0, description="Total records transitioned to license_expired.")
    withdrawn_count: int = Field(default=0, description="Total records flagged as withdrawn.")
    failed_count: int = Field(default=0, description="Total records that encountered check failures.")
    executed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
```

## Architectural Guarantees & Invariants

1. **Strict Non-Deletion Invariant (PRD §4.4, Blueprint B-06 §4 / §10)**:
   - ZERO SQL `DELETE` queries executed during refresh. Expired or revoked items transition to `status='license_expired'`, preserving child download inventory for graceful client UI re-auth / re-download prompts (Mobile Task K-04).
2. **Child Safety Withdrawn Content Flagging (PRD FR-5 / §12.7)**:
   - Content unpublished or withdrawn by trust/safety teams gets `withdrawn=True` (additive boolean column).
   - Prevents offline playback loops while preserving child inventory visibility per FR-5.
   - Restoration supported: un-flags (`withdrawn=False`) if content is republished.
3. **Deterministic Keyset Cursor Pagination (Blueprint B-06 §10 / §24)**:
   - Scans records ordered by `download_id.asc()` where `download_id > cursor`.
   - Prevents `OFFSET` query degradation and transaction locks on high-volume tables.
   - Crash-resumable via `initial_cursor`.
4. **Intra-Run Lookup Caching & Batch Prefetch (Blueprint B-06 §24)**:
   - In-memory `withdrawal_cache`, `entitlement_cache`, and `child_active_cache` eliminate redundant remote service round-trips for shared content IDs across distinct children.
5. **Partial-Row Failure Isolation (Blueprint B-06 §10 / §18)**:
   - Traps row-level exceptions; transient failure on an individual record increments `failed_count` and continues processing remaining rows.
6. **Decoupled from Storage Cap (PRD §1.10 Edge Case 4)**:
   - Lowering parent storage cap NEVER causes the refresh job to expire or delete existing completed downloads.
