# B-02 — Content Search Indexing Sync

## 1. Feature Context
Part of Feature B.13 (Search & Discovery). Keeps the `search_index_entry` read-model (introduced by B-01) synchronized with the source-of-truth content in A.3/A.5/A.6, replacing the PRD's Kafka-consumer "Indexing Pipeline" with an outbox-driven sync consistent with the platform's existing transactional-outbox pattern.

## 2. Parent Feature
B.13 — Search & Discovery

## 3. Sub-feature
B-02 — Content Search Indexing Sync

## 4. Objective
Ensure every published, age-tagged content item from `content` (and any future dedicated learning-content contexts) is reflected in `search_index_entry` promptly and correctly, with a hard fail-closed rule: content missing a determinable `age_band_eligibility` is excluded from the index rather than indexed with an ambiguous "visible to everyone" default.

## 5. Business Requirements
- §5 item 2 (PRD backend prompt, adapted): every indexed document MUST include `age_band_eligibility` and `is_published`; a content item published without a determinable `age_band_eligibility` is REJECTED from indexing entirely.
- §4.4 Soft Delete Rules: when content is withdrawn/archived in A.3/A.5/A.6, the corresponding `search_index_entry` is removed/flagged so it stops surfacing.
- DevOps §10: alert on sync-consumer lag and on the rate of content rejected due to missing metadata spiking.
- Rollback Plan §15.2: any deploy touching field-validation logic requires a staging reindex against a fixture multi-age-band catalog before promotion.

## 6. Existing Architecture
Implemented as an **outbox-consumer sync job**, not a Kafka consumer — the platform already has `common/outbox.py` (`OutboxWriter`, `OutboxEventOrm`) and an existing `OutboxRelay` (per `FAST-API-INSTRUCTIONS.md` §15 master table) that dispatches outbox events to background workers. This blueprint adds a `SearchIndexSyncWorker` that subscribes to `ContentPublished`/`ContentUpdated`/`ContentWithdrawn` events emitted by `content` module's `ContentService` via the existing `OutboxWriter.emit()` call already made at content publish/update/withdraw time (no new emission mechanism needed if `content` already emits these events; if not, this blueprint adds the emit calls to `ContentService`, not a parallel mechanism).

## 7. Existing Code to Reuse
- `common/outbox.py` → `OutboxEventOrm`, `OutboxWriter`.
- `common/outbox_relay.py` → `OutboxRelay` background dispatch worker (reuse the existing relay/consumer runner rather than building a second one).
- `content` module's `ContentRepository`/`ContentService` — source of truth for `age_band_eligibility`-equivalent metadata and `is_published`/`is_withdrawn` state.
- `common/utils/clock.py` → `Clock` for `indexed_at` timestamping (testable via `TestClock`).

## 8. Files to Create
- `src/noorheroes/modules/search/sync_worker.py` — `SearchIndexSyncWorker` (handles `ContentPublished`, `ContentUpdated`, `ContentWithdrawn`).
- `src/noorheroes/modules/search/repository.py` (extend, if not already present from B-01) — `upsert_index_entry()`, `remove_index_entry()`, `mark_rejected()`.
- `tests/modules/search/test_sync_worker.py`.
- `tests/modules/search/test_fail_closed_indexing.py`.

## 9. Files to Modify
- `src/noorheroes/modules/content/service.py` — confirm/add `OutboxWriter.emit()` calls for `ContentPublished`/`ContentUpdated`/`ContentWithdrawn` if not already present (do not duplicate if `content` already emits equivalent events for other consumers — reuse the same event, add a new handler, not a new emission).
- Worker/process entrypoint config — register `SearchIndexSyncWorker` alongside the existing `OutboxRelay` worker process.

## 10. Backend Requirements
- On `ContentPublished`/`ContentUpdated`: upsert `search_index_entry` with `age_band_eligibility`, `is_published=true`, `locale`, `indexed_at=Clock.now()`.
- **Fail closed:** if the source content event payload has no resolvable `age_band_eligibility`, do not upsert — instead write a `rejected_from_indexing` record (or flag) capturing `content_id` and `reason`, surfaced to B-07/N-02.
- On `ContentWithdrawn`: remove or flag (`is_published=false`) the corresponding `search_index_entry` row so it stops surfacing in B-01's query results.
- Idempotent upsert: duplicate delivery of the same event must not create duplicate rows or corrupt state.
- Out-of-order tolerance: an `Updated` event arriving before its `Created`/`Published` counterpart must not crash the worker — either buffer briefly or upsert-on-first-seen.
- Non-blocking: indexing failure must never roll back or block the source content transaction in `content` module.

## 11. KMP Requirements
N/A — backend-internal sync process, no client surface.

## 12. NextJS Requirements
N/A directly — surfaced read-only via B-07/N-02 (Search Index Health Monitor), not built here.

## 13. API Contract
No public HTTP API — this is an internal worker/consumer. Internal contract: consumes `OutboxEventOrm` rows of `aggregate_type="content"` with event types `ContentPublished`, `ContentUpdated`, `ContentWithdrawn`.

## 14. Database Requirements
- `search_index_entry` (defined in B-02's companion migration if not already created by B-01 — coordinate to avoid duplicate migrations).
- New table `search_index_rejection` (or a `rejected_reason` nullable column on `search_index_entry`): `content_id`, `reason`, `detected_at` — feeds B-07/N-02's rejected-items report.
- `indexed_at` column mandatory for sync-freshness monitoring.

## 15. Validation
- `age_band_eligibility` must resolve to a non-empty, valid subset of `AgeBand` values — anything else is a rejection, not a partial index.
- `is_published` must be an explicit boolean from the source event, never defaulted.

## 16. Authentication
N/A (internal worker, no external caller).

## 17. Authorization
N/A (internal worker).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Missing `age_band_eligibility` | Reject from indexing, log to `search_index_rejection` (fail closed) |
| Duplicate event delivery | Idempotent upsert, no duplicate row |
| Out-of-order events | Buffer/upsert-on-first-seen, no crash |
| Indexing write failure | Retry with backoff (`common/utils/retry.py`'s `retry_with_backoff`); never blocks source transaction |
| Content withdrawn but index entry missing | No-op (already absent), logged at debug level only |

## 19. Offline First
N/A (backend).

## 20. Local Data
N/A (backend).

## 21. Localization
`locale` propagated verbatim from source content event onto the index entry; no translation performed at index time.

## 22. RTL
N/A.

## 23. Analytics
No user-facing analytics; operational metrics only (sync lag, rejection rate) feed B-07/N-02's read-only monitoring endpoints.

## 24. Performance
Upserts are single-row, indexed on `content_id` PK — no batch/bulk-scan operations on the hot path. Sync lag is the primary performance signal, alertable per DevOps §10.

## 25. Security
Fail-closed-on-missing-metadata is itself a security/content-safety control (a misconfiguration-defense pattern per PRD §12.2) — ambiguous metadata must never default to "visible to everyone."

## 26. Library Requirements
Existing outbox/worker infrastructure only (`common/outbox.py`, `common/outbox_relay.py`); `common/utils/retry.py` for backoff. No Kafka client library.

## 27. Testing
- Unit: upsert logic for each event type; fail-closed rejection for missing `age_band_eligibility`; idempotent duplicate-event handling.
- Integration: fixture content set spanning all age bands processed end-to-end, resulting index state asserted exactly (Rollback Plan §15.2's staging-verification pattern, run as an automated integration test here).
- Out-of-order delivery test.

## 28. Documentation & Operational Runbook

### 28.1 Overview & Remediation Context
As mandated by **PRD Feature B.13 §15.2 (Rollback Plan)** and **§10 (DevOps Requirements)**, the `search_index_entry` table is a derived read-model projection rather than an irreplaceable primary source of truth. If search index corruption, schema migration regressions, field-validation changes, or deployment rollbacks occur, an operator or automated CI/CD pipeline can completely rebuild and resynchronize the index from primary catalog sources (`StorySeriesOrm`, `StoryEpisodeOrm`, `ContentCatalogItem`) using the operational reindexing tool.

### 28.2 Operational Reindex CLI Tool
Canonical CLI script: `scripts/reindex_search_catalog.py` (delegating to `src/noorheroes/scripts/reindex_search_catalog.py`).

#### Syntax & Usage:
```bash
# 1. Dry-Run Validation (computes age-band eligibility and counts without mutating database)
python scripts/reindex_search_catalog.py --dry-run

# 2. Live Full Catalog Reindex (executes idempotent upserts with fail-closed rejection logging)
python scripts/reindex_search_catalog.py --batch-size 100
```

#### Output Example:
```text
--- Search Catalog Reindex Summary ---
Total Scanned : 142
Indexed (Pass): 138
Rejected (FC) : 4
Withdrawn     : 0
Errors        : 0
Dry Run Mode  : False
--------------------------------------
```

### 28.3 Rollback Remediation Protocol (PRD §15.2)
1. **Trigger Condition:** Detected index corruption, roll back of backend deployment touching age-band filtering, or staging promotion verification.
2. **Step 1 — Verify Alembic Schema State:** Ensure database revision is aligned with target release:
   ```bash
   alembic upgrade head
   ```
3. **Step 2 — Execute Automated Staging Invariant Suite:** Run automated reindex fixture integration test to confirm zero safety regressions:
   ```bash
   pytest tests/modules/search/test_fail_closed_indexing.py -k test_fixture_multi_age_band_catalog_reindex_integration
   ```
4. **Step 3 — Trigger Reindex Batch Script:** Execute `python scripts/reindex_search_catalog.py` against active database.
5. **Step 4 — Verify Telemetry & Sync Metrics:** Inspect `SearchRepository.get_sync_metrics()` or query `search_index_rejection` to ensure `sync_lag_seconds` resets to ~0 and rejections are logged with actionable editorial error messages.

### 28.4 DevOps Incident Playbooks
- **Alert 1: High Sync-Consumer Lag (`sync_lag_seconds > 120s`)**:
  - *Cause:* Celery worker starvation, Redis broker disconnection, or heavy database lock contention during content publishing bursts.
  - *Action:* Verify Celery worker concurrency (`celery -A src.noorheroes.core.celery_app inspect active`), inspect Outbox Relay process (`src/noorheroes/common/outbox_relay.py`), and confirm tasks `search.sync_content_published`, `search.sync_content_updated`, `search.sync_content_withdrawn` are consuming without backpressure.
- **Alert 2: Rejection Rate Spike (`search_index_rejection` count anomaly)**:
  - *Cause:* Editorial team publishing batch content lacking `age_band_eligibility` or containing unapproved custom strings (e.g. `"all_ages"`).
  - *Action:* Query recent rejections via `GET /admin/v1/search/operations/rejections` (B-07) or SQL `SELECT * FROM search_index_rejection ORDER BY detected_at DESC LIMIT 50;`. Export affected `content_id` list to editorial team for taxonomy tagging.


## 29. AI Coding Agent Implementation Steps
**Task 01 — Confirm/Add Content Outbox Events**
Objective: verify `content` module emits `ContentPublished`/`ContentUpdated`/`ContentWithdrawn` via `OutboxWriter`; add if missing.
Existing architecture to follow: `OutboxWriter.emit(event, aggregate_type, aggregate_id)` pattern already used elsewhere (e.g., `ChildProfileCreated`).
Do not change: any existing event contract already consumed by other modules.

**Task 02 — Extend search_index_entry Schema for Rejection Tracking**
Objective: add `search_index_rejection` table/column.
Files to create: migration.

**Task 03 — Implement SearchIndexSyncWorker**
Objective: consumer handling all three event types with fail-closed and idempotent-upsert logic.
Files to create: `modules/search/sync_worker.py`.
Business rules: fail-closed on missing `age_band_eligibility`; non-blocking on the source transaction.

**Task 04 — Wire Worker into Existing Relay/Process**
Objective: register `SearchIndexSyncWorker` alongside `OutboxRelay`.
Files to modify: worker entrypoint config.

**Task 05 — Add Tests**
Objective: full coverage per §27, including the fixture multi-age-band reindex integration test.

**Task 06 — Add Operational Alerting Hooks**
Objective: expose sync-lag and rejection-rate metrics for DevOps alerting (§10) and for B-07's read model.

**Task 07 — Final Code Review**
Objective: confirm non-blocking behavior verified (a forced indexing failure does not roll back a `content` publish transaction in a test).

## 30. Definition of Done
- All three content lifecycle events correctly reflected in `search_index_entry`.
- Fail-closed behavior verified by test.
- Non-blocking behavior verified by test.
- Sync-lag and rejection metrics exposed for B-07/N-02.

## 31. Final Verification Checklist
- [x] Content missing `age_band_eligibility` is excluded, never defaulted to visible.
- [x] Withdrawn content is removed/flagged from the index.
- [x] Duplicate event delivery does not corrupt state.
- [x] Out-of-order delivery does not crash the worker.
- [x] Indexing failure never blocks/rolls back the source `content` transaction.
- [x] Sync-lag metric available for alerting.
- [x] Rejection list available for editorial follow-up (B-07/N-02).

## 32. Sign-Off & Implementation Ledger
- **Status:** COMPLETED & VERIFIED
- **Date:** 2026-09-26
- **Components Implemented:**
  - `alembic/versions/0088_create_search_index_rejection_table.py`: Created `search_index_rejection` table with composite and single-column indexes.
  - `src/noorheroes/modules/search/models.py`: Added `SearchIndexRejectionOrm` and `SearchIndexRejection` alias.
  - `src/noorheroes/modules/search/repository.py`: Implemented `upsert_index_entry()`, `remove_index_entry()`, `record_rejection()`, `get_rejections()`, and `get_sync_metrics()`.
  - `src/noorheroes/modules/search/sync_worker.py`: Implemented `SearchIndexSyncWorker` with strict fail-closed validation, outbox event routing, idempotent upserts, out-of-order tolerance, and non-blocking safety wrappers.
  - `src/noorheroes/modules/search/tasks.py`: Registered Celery background tasks `search.sync_content_published`, `search.sync_content_updated`, `search.sync_content_withdrawn`, and alias `content.on_content_published`.
  - `src/noorheroes/common/outbox_relay.py`: Updated `DISPATCH_TABLE` to map content lifecycle events to search sync Celery tasks.
  - `src/noorheroes/core/celery_app.py`: Included `src.noorheroes.modules.search.tasks` in worker configuration.
  - `src/noorheroes/modules/content/events.py`: Extended `ContentPublished`, `ContentUpdated`, and `ContentWithdrawn` domain event definitions.
  - `tests/unit/test_search_rejection_migration.py`: 2/2 passed.
  - `tests/modules/search/test_sync_worker.py`: 17/17 passed (including retry_with_backoff, query delisting, duplicate updates, out-of-order corrupted updates, operational reindex script, and content transaction isolation).
  - `tests/modules/search/test_fail_closed_indexing.py`: 12/12 passed (including non-string elements, whitespace, enum variants, rejection audit queries, and fixture multi-age-band catalog reindex integration).
  - `tests/modules/search/test_age_band_bypass_security.py`: 24/24 passed.
  - `tests/modules/search/test_child_search_api.py`: 20/20 passed.
  - **Total Search Test Suite:** 152/152 passed across all search test modules (100% green, 0 regressions).

