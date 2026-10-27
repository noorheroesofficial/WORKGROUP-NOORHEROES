# Runbook: Rewards Wallet Projection & Reconciliation Service

**Document ID:** `docs/runbooks/rewards_wallet_reconciliation.md`  
**Related Blueprint:** `Development_Blueprints/A11_Rewards_System/Backend/03-wallet-projection-reconciliation-service.md`  
**Related PRD:** `PRD_Documents/Child App (1-12)/Feature_A11_Rewards_System.md` (§1.4, §1.7 FR-3/FR-14, §1.19)  
**Audience:** Backend Engineers, Site Reliability Engineers (SRE), Trust & Safety / Support Operations

---

## 1. Operational Overview & Architecture

The NoorHeroes Rewards System enforces strict append-only ledger immutability (`reward_ledger_entries`). The `reward_wallets` table is a **repairable, derived projection cache** used to serve high-performance O(1) balance reads (p95 < 400ms).

To guarantee 100% wallet balance accuracy (PRD §1.4), the **Wallet Projection & Reconciliation Service (B-03)** maintains:
1. **`recompute_wallet(child_id)`**: An idempotent, pure mathematical recalculation of point balances and XP sums directly from the immutable ledger.
2. **`reconcile_wallets_task`**: A standing background Celery task executing on an hourly periodic schedule, scanning candidate child wallets, detecting any drift, healing the projection cache, logging audit records into `reconciliation_incidents`, and alerting on correction spikes.
3. **Admin Remediation API**: Scoped administrative endpoints allowing customer support to trigger immediate reconciliation on demand for reported discrepancies.

```
┌────────────────────────────────────────────────────────┐
│               REWARD LEDGER ENTRIES                    │
│    (Append-Only, Immutable Source of Truth, B-01)      │
└──────────────────────────┬─────────────────────────────┘
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
┌───────────────────────────┐ ┌──────────────────────────┐
│  RECOMPUTE PROJECTION     │ │ STANDING RECONCILIATION  │
│  - Sums points & XP       │ │ - Hourly Celery Beat     │
│  - Advisory/Row Lock      │ │ - Self-heals drift       │
│  - Pure derived state     │ │ - Logs incident audits   │
└────────────┬──────────────┘ └──────────┬───────────────┘
             │                           │
             ▼                           ▼
┌───────────────────────────┐ ┌──────────────────────────┐
│      REWARD_WALLETS       │ │ RECONCILIATION_INCIDENTS │
│ (Cached Derived Balance)  │ │ (Immutable Audit Trail)  │
└───────────────────────────┘ └──────────────────────────┘
```

---

## 2. Scheduled Reconciliation Job

### Celery Task: `rewards.reconcile_wallets`
- **Schedule**: Hourly (`schedule=3600.0s`, configurable via `settings.wallet_reconciliation_schedule_seconds`).
- **Batch Size**: 100 children per run (configurable via `settings.wallet_reconciliation_batch_size`).
- **P0 Spike Alert Threshold**: 10 corrections per batch (`settings.wallet_reconciliation_alert_threshold`).
- **Concurrency Protection**:
  - Uses transactional PostgreSQL advisory locks (`pg_advisory_xact_lock(hashtext('reward_wallet_' || child_id))`).
  - Employs row-level locking (`SELECT ... FOR UPDATE`) on `reward_wallets`.
  - On SQLite test engines, safely degrades to serializable in-memory transactions.
- **Cache Invalidation**:
  - Automatically purges Redis cache keys `wallet:{child_id}` upon correction.

---

## 3. Manual Single-Child Reconciliation (Support Tooling)

When customer support receives an inquiry regarding point balance mismatches, operators can force an immediate reconciliation using either the Admin API or the Celery CLI.

### Method A: Admin REST API (Recommended)

**Endpoint:** `POST /v1/admin/rewards/children/{id}/reconcile`  
**Headers:**
- `Authorization: Bearer <ADMIN_JWT_TOKEN>`
- `Accept-Language: en` (or `hi`, `ur`, `ar`)

**Example cURL:**
```bash
curl -X POST "https://api.noorheroes.com/v1/admin/rewards/children/01H8XVMQ2G0000000000000002/reconcile" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Accept-Language: en"
```

**Success Response (Drift Detected & Healed — 200 OK):**
```json
{
  "success": true,
  "childId": "01H8XVMQ2G0000000000000002",
  "driftDetected": true,
  "wallet": {
    "xp": 1240,
    "level": 7,
    "noorPoints": 380,
    "badges": [],
    "recentLedger": []
  },
  "incident": {
    "id": "019183ab-0000-7000-8000-000000000001",
    "childId": "01H8XVMQ2G0000000000000002",
    "oldBalance": 350,
    "newBalance": 380,
    "oldXp": 1200,
    "newXp": 1240,
    "driftAmount": 30,
    "reason": "manual_admin_reconciliation:admin_001",
    "correctedAt": "2026-09-03T04:30:00Z"
  },
  "message": "Wallet balance drift was detected and successfully healed from the immutable ledger."
}
```

### Method B: Celery Python Execution

From an operational container or production shell:
```python
from src.noorheroes.modules.rewards.tasks import reconcile_child_wallet_task

# Asynchronous background execution
task = reconcile_child_wallet_task.delay(
    child_id="01H8XVMQ2G0000000000000002",
    reason="support_ticket_SUP-8492",
)
print("Dispatched Task ID:", task.id)
```

### Method C: Admin Batch REST API (Maintenance Tooling)

**Endpoint:** `POST /v1/admin/rewards/reconciliation/batch`  
**Query Parameters:**
- `batch_size`: Integer (default 100, max 500)
- `alert_threshold`: Integer (default 10)

**Example cURL:**
```bash
curl -X POST "https://api.noorheroes.com/v1/admin/rewards/reconciliation/batch?batch_size=100&alert_threshold=10" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Accept-Language: en"
```

**Domain Events & Outbox Publishing:**
Whenever drift is healed, a `WalletReconciliationDriftCorrectedEvent` is automatically published via the transactional outbox (`outbox_events` table) with:
- `event_type`: `"wallet_reconciliation_drift_corrected"`
- `aggregate_type`: `"reward_wallet"`
- `aggregate_id`: `child_id`
- Payload: `incident_id`, `child_id`, `old_balance`, `new_balance`, `drift_amount`, `reason`, `corrected_at`.

---

## 4. Correction-Volume Spike Alerting (P0 Monitoring)

If the count of healed wallets during a single reconciliation run equals or exceeds the configured threshold (`settings.wallet_reconciliation_alert_threshold`, default 10):

### Triggered Alerts:
1. **Critical Structured Log**:
   ```json
   {
     "level": "CRITICAL",
     "logger": "noorheroes.modules.rewards.projection",
     "message": "P0_ALERT: wallet_reconciliation_spike_detected: 14 corrections exceeded threshold 10",
     "metric": "wallet_reconciliation_spike",
     "total_corrected": 14,
     "alert_threshold": 10,
     "duration_ms": 312.4
   }
   ```
2. **Prometheus Metrics**:
   - `wallet_reconciliation_spike_alerts_total`: Incremented by 1.
   - `wallet_reconciliation_corrections_total`: Incremented by the corrected count.
   - `wallet_reconciliation_runs_total{status="success"}`: Tracks total executions.

### Immediate Triage Protocol (P0):
1. **Check for Uncommitted Ledger Writes**: Verify whether a batch migration, bulk manual award, or external ETL process inserted rows directly into `reward_ledger_entries` without invoking `recompute_wallet`.
2. **Review Incident Audit Records**:
   ```bash
   curl -X GET "https://api.noorheroes.com/v1/admin/rewards/reconciliation/incidents?limit=20" \
     -H "Authorization: Bearer $ADMIN_TOKEN"
   ```
   Inspect `drift_amount` and `old_balance` vs `new_balance` to determine if balances increased (unprojected credits) or decreased (cache tampering attempt).
3. **Database Write Grant Verification**:
   Ensure `REVOKE UPDATE, DELETE ON reward_ledger_entries` (Migration 0017) remains enforced. Verify no rogue DB user has direct write grants on `reward_wallets`.

---

## 5. Disaster Recovery: Full Cache Rebuild from Scratch

In the event of database corruption or total cache loss, `reward_wallets` can be rebuilt with zero data loss directly from `reward_ledger_entries`:

```python
import asyncio
from src.noorheroes.infrastructure.db import AsyncSessionLocal
from src.noorheroes.modules.rewards.projection import recompute_wallet
from src.noorheroes.modules.rewards.repository import RewardRepository
from sqlalchemy import select
from src.noorheroes.modules.rewards.models import RewardLedgerEntry

async def rebuild_all_wallets():
    async with AsyncSessionLocal() as session:
        # Fetch all distinct children who possess ledger entries
        stmt = select(RewardLedgerEntry.child_id).distinct()
        res = await session.execute(stmt)
        children = res.scalars().all()
        print(f"Rebuilding {len(children)} child wallet projections...")

        for idx, child_id in enumerate(children, 1):
            await recompute_wallet(session=session, child_id=child_id)
            if idx % 100 == 0:
                await session.commit()
                print(f"Rebuilt {idx}/{len(children)}...")
        await session.commit()
        print("Wallet projection rebuild completed successfully.")

if __name__ == "__main__":
    asyncio.run(rebuild_all_wallets())
```
