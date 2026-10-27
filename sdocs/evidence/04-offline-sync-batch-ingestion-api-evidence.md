# Evidence: Offline Sync Batch Ingestion API & Idempotent Dedup Store (B-04)

**Task**: `04-offline-sync-batch-ingestion-api`  
**Epic**: `EPIC-015` (Offline Downloads & Sync Engine)  
**Parent PRD**: `PRD_Documents/Child App Supporting (13-18)/Feature_B15_Offline_Downloads_Sync.md`  
**Task Blueprint**: `Development_Blueprints/B15_Offline_Downloads_Sync/Backend/04-offline-sync-batch-ingestion-api.md`  
**Contract**: `api.sync-batch` (`sdocs/contracts/api/sync-batch.md`)  
**Date**: 2026-09-29  
**Status**: VERIFIED & CLOSED (100% Zero-Missing-Scenarios Pass Rate)  

---

## 1. Verified Acceptance Criteria Matrix

| Criterion ID | Requirement / Invariant | Acceptance Criteria & Scenario | Result |
|:---|:---|:---|:---:|
| **AC-01** | **Canonical Entry Point (Blueprint B-04 §4 / §13)** | `POST /v1/sync/batch` (and module parity alias `POST /v1/downloads/sync/batch`) centralizes the ingestion of all client events queued offline during disconnection (habit checkins, quiz responses, story/audio progress, reward claims, points earned). | **PASSED** |
| **AC-02** | **In-Memory Causal Sorting (Blueprint B-04 §6, PRD Edge Case 7)** | Array order received from mobile clients is treated as untrusted; events are sorted in-memory strictly by `occurred_at` ascending before processing. Older events always process before newer events. | **PASSED** |
| **AC-03** | **Furthest-Valid-Position Timestamp Stability (Blueprint B-04 §6, PRD Edge Case 14)** | When multiple events share identical timestamps, the original order in the submitted list is preserved stably, satisfying furthest-valid-position progress guarantees. | **PASSED** |
| **AC-04** | **Pre-Downstream Deduplication (Blueprint B-04 §8, PRD §5 Item 5)** | Queries `sync_event_log` in a single SQL `IN (...)` batch lookup (`SyncEventLogRepository.bulk_get_by_client_event_ids()`). Already applied events short-circuit with `status='duplicate'` and **zero downstream service invocations**. | **PASSED** |
| **AC-05** | **Downstream Idempotency Pass-Through (Blueprint B-04 §9)** | Genuinely new events dispatch through `EVENT_TYPE_HANDLERS` registry (`habit_checkin`, `quiz_response`, `story_progress`, `audio_progress`, `content_progress`, `reward_claim`, `points_earned`), passing `client_event_id` directly as the downstream idempotency key. | **PASSED** |
| **AC-06** | **Partial-Batch Failure Isolation (Blueprint B-04 §10, PRD Edge Case 12)** | Downstream handler 5xx/timeout/failure leaves the event **UN-LOGGED** in `sync_event_log` for client retry on next reconnect; other valid events in the batch proceed and persist `applied` without head-of-line blocking. | **PASSED** |
| **AC-07** | **Concurrent Savepoint Race Collision Safety (Blueprint B-04 §25)** | `SyncEventLogRepository.record_outcome` wraps database insertion in a nested savepoint (`async with session.begin_nested()`), safely resolving concurrent collision `IntegrityError` without aborting the transaction. | **PASSED** |
| **AC-08** | **Bounded Batch Size Enforcement (Blueprint B-04 §15 / §24)** | Enforces array bounds of 1 to 500 events via `SyncBatchRequest(min_length=1, max_length=500, extra="forbid")`. Empty lists and oversized batches reject with HTTP 422 Unprocessable Entity. | **PASSED** |
| **AC-09** | **Child Bearer Authentication & Headers (Blueprint B-04 §16 / §25)** | Gated by `Depends(get_current_child_session)`. Unauthenticated requests return 401; parent tokens return 403. Anti-caching headers (`no-store, no-cache, private`, `Pragma: no-cache`) served on all responses. | **PASSED** |
| **AC-10** | **Transactional Outbox Batch Metrics (Blueprint B-04 §23)** | Emits `OfflineSyncBatchIngested` (`offline_sync.batch_ingested`) containing `batch_id`, `child_id`, `total_events`, `applied_count`, `duplicate_count`, and `rejected_count` for B-07 sync health monitoring. | **PASSED** |
| **AC-11** | **Append-Only Idempotent Dedup Store (Blueprint B-04 §14, Blueprint B-05)** | Database migration `0093_create_sync_event_log_table.py` creates table `sync_event_log` with `log_id VARCHAR(36) PK` (UUIDv7), `client_event_id VARCHAR(64) UNIQUE INDEX`, composite index `(child_id, occurred_at)`, and status check constraint (`applied`, `duplicate`, `rejected`). | **PASSED** |
| **AC-12** | **DevOps §10 CI-Blocking Staging-Replay Test (Blueprint B-04 §27 / §30)** | Multi-day 15-event backlog with 3 pre-seeded duplicates executed chronologically in causal order; replaying the entire batch triggers **zero downstream invocations** with 100% duplicate protection and outbox metric verification. | **PASSED** |

---

## 2. Test Execution Log

### 2.1 Dedicated Task B-04 Test Suites (19 Tests)

**Command**:
```powershell
pytest tests/modules/downloads/ -k "sync_batch" -v
```

**Output**:
```text
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Sarva\Documents\WORKGROUP-NOORHEROES\NoorHeroes-Backend
configfile: pyproject.toml
plugins: anyio-4.14.2, asyncio-1.4.0, cov-7.1.0
asyncio: mode=Mode.STRICT, debug=False
collected 19 items

tests/modules/downloads/test_sync_batch_api.py::test_sync_batch_success_canonical_route PASSED [  5%]
tests/modules/downloads/test_sync_batch_api.py::test_sync_batch_module_parity_alias PASSED    [ 10%]
tests/modules/downloads/test_sync_batch_api.py::test_sync_batch_unauthenticated_returns_401 PASSED [ 15%]
tests/modules/downloads/test_sync_batch_api.py::test_sync_batch_parent_session_returns_403 PASSED [ 21%]
tests/modules/downloads/test_sync_batch_api.py::test_sync_batch_empty_list_returns_422 PASSED  [ 26%]
tests/modules/downloads/test_sync_batch_api.py::test_sync_batch_exceeding_max_size_returns_422 PASSED [ 31%]
tests/modules/downloads/test_sync_batch_api.py::test_sync_batch_camel_case_dual_wire_parsing PASSED [ 36%]
tests/modules/downloads/test_sync_batch_causal_order.py::test_scrambled_timestamps_processed_chronologically PASSED [ 42%]
tests/modules/downloads/test_sync_batch_causal_order.py::test_reverse_chronological_submission_inverts_to_oldest_first PASSED [ 47%]
tests/modules/downloads/test_sync_batch_causal_order.py::test_identical_timestamps_preserve_stable_submission_order PASSED [ 52%]
tests/modules/downloads/test_sync_batch_causal_order.py::test_mixed_domain_events_chronological_interleaving PASSED [ 57%]
tests/modules/downloads/test_sync_batch_partial_failure.py::test_downstream_failure_leaves_event_unlogged_for_retry PASSED [ 63%]
tests/modules/downloads/test_sync_batch_partial_failure.py::test_subsequent_batch_retry_succeeds_after_transient_failure PASSED [ 68%]
tests/modules/downloads/test_sync_batch_partial_failure.py::test_unregistered_event_type_rejected_without_aborting_batch PASSED [ 73%]
tests/modules/downloads/test_sync_batch_pre_downstream_dedup.py::test_replay_applied_batch_triggers_zero_downstream_calls PASSED [ 78%]
tests/modules/downloads/test_sync_batch_pre_downstream_dedup.py::test_mixed_batch_dispatches_only_new_events PASSED [ 84%]
tests/modules/downloads/test_sync_batch_pre_downstream_dedup.py::test_downstream_handler_receives_client_event_id_as_idempotency_key PASSED [ 89%]
tests/modules/downloads/test_sync_batch_pre_downstream_dedup.py::test_concurrent_duplicate_insertion_race_safety_via_savepoint PASSED [ 94%]
tests/modules/downloads/test_sync_batch_staging_replay.py::test_staging_replay_fixture_causal_execution_and_duplicate_immunity PASSED [100%]

============================= 19 passed in 1.48s ==============================
```

### 2.2 Downloads Module Full Regression Suite (122 Tests)

**Command**:
```powershell
pytest tests/modules/downloads/ -v
```

**Result**: `122 passed in 9.80s` (100% pass rate)

### 2.3 Media Downloads Manifest Parity Suite (52 Tests)

**Command**:
```powershell
pytest tests/modules/media/test_download_manifest_api.py -v
```

**Result**: `52 passed in 4.67s` (100% pass rate)

**Combined Regression Total**: **174 passed, 0 failed, 0 skipped**.

---

## 3. CI/CD Pre-Flight Automated Script Checks

| Script | Command | Result |
|---|---|:---:|
| **OpenAPI Schema Export** | `python scripts/export_openapi_schema.py` | **PASSED** (Exported to `artifacts/openapi.json`) |
| **Migration Backward Compat** | `python scripts/check_migration_backward_compat.py` | **PASSED** (Clean backward compatibility) |
| **Env Example Synchronization** | `python scripts/check_env_example_sync.py` | **PASSED** (0 drift against Settings) |
| **Env Drift Detection** | `python scripts/check_env_drift.py` | **PASSED** (0 drift detected) |
| **Resource Naming Conventions** | `python scripts/check_resource_naming.py` | **PASSED** (100% tier naming compliance) |

---

## 4. Production Verification Summary

- **Zero Missing Scenarios**: All 19 dedicated unit, integration, and staging replay scenarios pass with zero warnings.
- **Zero Downstream Duplicate Invocations**: Verified by automated test spy; replayed batches short-circuit before any downstream call.
- **Strict Child Token Session Gate**: 401 on unauthenticated, 403 on parent session.
- **Clean OpenAPI Documentation**: All schemas (`SyncBatchRequest`, `SyncBatchResponse`, `SyncEventRequest`, `ProcessedEvent`) exported with strict `extra="forbid"` and parameter documentation.
