# K-06 — Offline Progress Sync Outbox Integration

## 1. Feature Context
Part of Feature B.15 (Offline Downloads & Sync). The client-side counterpart to B-04 — every offline-capable feature module's write actions (habit check-ins, quiz responses, content progress, etc.) flow through this shared outbox on their way to the server.

## 2. Parent Feature
B.15 — Offline Downloads & Sync

## 3. Sub-feature
K-06 — Offline Progress Sync Outbox Integration

## 4. Objective
Wire every offline-capable feature module's write actions into the **existing** `core-data`/`core-database` `SyncQueue`/`SyncOperation`/`SyncHandler` infrastructure, submitting to B-04's `POST /v1/sync/batch` sorted by `occurred_at`, with correct outbox clearing on `applied`/`duplicate` responses.

## 5. Business Requirements
- FR-4: write local-first → queue immutable events with client-generated IDs → sync in causal order on reconnect → server deduplicates via idempotency keys → furthest-valid-position for progress; quiz attempts tracked separately.
- Edge Case 7: extended offline period generating many events → processed in correct causal order on reconnect, batched/paginated submission if needed.
- Edge Case 12: partial sync-batch success → unsynced events remain queued and retried; already-synced events' idempotency keys prevent reprocessing.
- §5 Android AI Prompt items 5–7: `SyncOutbox` stores `event_type`/`client_event_id`/`occurred_at`/`payload`; submits sorted by `occurred_at` ascending; removes `applied`+`duplicate` entries after submission, keeping only `rejected`; end-to-end multi-feature-module test into the same outbox.

## 6. Existing Architecture
This blueprint deliberately reuses, rather than replaces, the **already-existing** `core-data`'s `SyncQueue`/`SyncQueueImpl`/`SyncOperationDispatcher` and `core-database`'s `SyncQueueDao`/`SyncQueueEntity` (with its `sequenceNumber` field already designed for FIFO/causal ordering) and `core-network`'s `SyncOperation` sealed hierarchy/`SyncHandler` interface — per `CORE_DATA_INSTRUCTIONS.md` §3 and `CORE_NETWORK_INSTRUCTIONS.md` §4/§9, this infrastructure is explicitly described as "almost all write methods in repositories should use the SyncQueue." This blueprint's job is to add the B.15-specific `SyncOperation` subclasses/`SyncHandler` implementations and point `SyncOperationDispatcher`'s flush target at B-04's new `POST /v1/sync/batch` endpoint — **not** to build a new `SyncOutbox`/`SyncWorker` module as the PRD's generic AI prompt describes.

## 7. Existing Code to Reuse
- `core-data`'s `SyncQueue`/`SyncQueueImpl`, `SyncOperationDispatcher`.
- `core-database`'s `SyncQueueDao`, `SyncQueueEntity` (`sequenceNumber`, `status`: `PENDING`/`IN_FLIGHT`/`FAILED`/`DEAD_LETTER`).
- `core-network`'s `SyncOperation` sealed hierarchy, `SyncHandler<T>` interface, `ConnectivityObserver` (auto-flush trigger).
- `SafeDatabaseHelper.withTransaction()` — atomic local-write + `SyncQueueEntity` insert, per `CORE_DATABASE_INSTRUCTIONS.md`'s "Scenario 2" example.
- Existing per-feature repositories (`HabitsRewardsRepository.checkInHabit()`, `PlaybackSyncRepository`, quiz-attempt repository, etc.) as the callers this blueprint wires into the outbox.

## 8. Files to Create
- `core-network/src/commonMain/kotlin/.../model/sync/DownloadsSyncOperations.kt` — new `SyncOperation` subclasses for any B.15-specific event types not already covered by existing subclasses (e.g., if content-progress/quiz-response operations aren't already modeled).
- `core-data/src/commonMain/kotlin/.../sync/handlers/SyncBatchDispatchHandler.kt` — the handler that actually calls `POST /v1/sync/batch` with a sorted, batched submission (if `SyncOperationDispatcher` doesn't already batch-submit; extends it to do so per B-04's contract).
- `core-data/src/commonTest/kotlin/.../sync/CausalOrderSubmissionTest.kt`.
- `core-data/src/commonTest/kotlin/.../sync/MixedResponseOutboxClearingTest.kt`.
- `core-data/src/commonTest/kotlin/.../sync/MultiFeatureModuleOutboxTest.kt` (end-to-end).

## 9. Files to Modify
- `core-data`'s `SyncOperationDispatcher` — extend to batch multiple pending `SyncQueueEntity` rows (sorted by `sequenceNumber`/`occurred_at`) into a single `POST /v1/sync/batch` call, rather than one-operation-at-a-time submission (if that's the current behavior) — aligning the dispatcher with B-04's batch contract.
- Each offline-capable feature repository (`HabitsRewardsRepository`, quiz-attempt repository, `PlaybackSyncRepository`, etc.) — confirm each write method already enqueues via `SyncQueue.enqueue()` per the existing convention; add any missing `SyncOperation` subclass + `SyncHandler` for content types not yet covered.
- `core-network`'s `api/SyncApi.kt` (new or extended) — `POST /v1/sync/batch` Ktor client.

## 10. Backend Requirements
Submits to B-04: `POST /v1/sync/batch`.

## 11. KMP Requirements
- `client_event_id` generated once at action time (in the repository method, at the moment of the local write), not at flush time — guaranteeing idempotency survives multiple flush retries of the same queued operation.
- `SyncOperationDispatcher` batches all `PENDING` `SyncQueueEntity` rows, sorts by `occurred_at` (or the existing `sequenceNumber` if it's guaranteed monotonic with `occurred_at`) ascending, and submits as one `POST /v1/sync/batch` call — never relying on server-side reordering as the sole safeguard, per B-04's explicit "never trust array order" contract on both ends.
- On response, entries with `status: 'applied'` or `status: 'duplicate'` are removed from `SyncQueueDao`; entries with `status: 'rejected'` remain queued (or move to `FAILED`/`DEAD_LETTER` per existing status semantics) for retry or investigation.
- Auto-flush triggered by `ConnectivityObserver` reporting an online transition, consistent with existing `SyncQueue` behavior — no new connectivity-observation logic introduced.
- Large offline backlogs (Edge Case 7) submitted in bounded-size batches (matching B-04's server-side max batch size) across multiple sequential calls, not one unbounded request.
- Rollback: a permanently `FAILED`/`DEAD_LETTER` operation notifies its `SyncHandler.onFailed()` to roll back any optimistic local UI state, per the existing `SyncQueue` contract.
- End-to-end verification: a story-progress event and a habit-check-in event queued from two different feature modules into the same `SyncQueueDao`, flushed together in one batch on reconnect, each routed correctly server-side to its owning domain repository.

## 12. NextJS Requirements
N/A.

## 13. API Contract
`POST /v1/sync/batch` per B-04 §13 — request/response shape exactly as specified there; client never assumes `duplicate` is an error.

## 14. Database Requirements
Reuses `core-database`'s existing `SyncQueueEntity`/`SyncQueueDao` — no new local table introduced.

## 15. Validation
`client_event_id` generated as a UUID at action time; `occurred_at` captured at the same moment (device clock) — this blueprint does not attempt server-clock synchronization beyond what `core-network`'s existing `ServerTimePlugin`/clock-skew tracking already provides.

## 16. Authentication
Relies on the app-wide child-session bearer token already attached by `core-network`'s HTTP client interceptor for the batch submission call.

## 17. Authorization
N/A beyond standard child-session scoping.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Batch submission network failure | All pending entries remain queued, retried on next auto-flush trigger |
| Mixed `applied`/`duplicate`/`rejected` response | `applied`+`duplicate` cleared; `rejected` entries remain queued (existing `FAILED` status semantics) |
| Extended offline period, large backlog | Submitted in bounded-size sequential batches, not one unbounded request (Edge Case 7) |
| Permanent operation failure | `SyncHandler.onFailed()` invoked, local optimistic state rolled back per existing contract |

## 19. Offline First
This entire blueprint **is** the offline-first write path — local write always precedes and never blocks on the sync submission.

## 20. Local Data
`SyncQueueEntity` (existing `core-database` table) is the queue this blueprint operates on.

## 21. Localization
N/A (background sync mechanism, no direct UI copy).

## 22. RTL
N/A.

## 23. Analytics
`offline_progress_event_queued` (on enqueue), `offline_sync_batch_started`, `offline_sync_batch_completed`, `offline_sync_duplicate_prevented` (per `duplicate`-status entries in the response).

## 24. Performance
- Batched submission (not one-operation-per-request) is the core performance requirement here, directly aligned with B-04's server-side batch-processing design.
- `sequenceNumber`/`occurred_at`-sorted submission avoids server-side reordering overhead.
- No main-thread blocking — `SyncOperationDispatcher` runs on background dispatchers via the existing `DispatcherProvider`.

## 25. Security
`client_event_id` generated once at action time (never regenerated on retry) is the client-side half of the idempotency guarantee B-04 relies on — a bug regenerating this ID on retry would silently defeat server-side dedup, so this is called out as a mandatory, tested invariant (§27).

## 26. Library Requirements
Existing `core-network` (Ktor), `core-database` (Room), Koin. No new libraries — this blueprint is explicitly an integration/extension of existing infrastructure, not new tooling.

## 27. Testing
- Unit: `SyncOperationDispatcher` submits a batch sorted by `occurred_at` regardless of `SyncQueueDao` insertion order (§5 item 5's client-side counterpart to B-04's server-side ordering test).
- **Mixed-response clearing test (mandatory):** a batch response with `applied`, `duplicate`, and `rejected` entries correctly clears only the first two from the local queue, leaving `rejected` entries queued.
- **End-to-end multi-feature-module test (mandatory):** queue a story-progress event and a habit-check-in event from two different repositories into the same `SyncQueueDao` while offline; trigger flush on reconnect; verify both submit in one batch and route correctly.
- Unit: `client_event_id` is stable across multiple flush attempts of the same queued operation (never regenerated on retry).

## 28. Documentation
KDoc explicitly noting this blueprint extends the **existing** `SyncQueue`/`SyncOperation`/`SyncHandler` infrastructure rather than introducing a parallel outbox mechanism, with a pointer to `CORE_DATA_INSTRUCTIONS.md` §3 and `CORE_NETWORK_INSTRUCTIONS.md` §9 for the underlying contract.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Audit Existing SyncOperation Coverage**
Objective: identify which offline-capable feature event types (habit check-in, quiz response, story/audio/Quran progress) already have a `SyncOperation` subclass/`SyncHandler`, and which are missing.
Files to create (as needed): `DownloadsSyncOperations.kt` for any gaps found.

**Task 02 — Extend SyncOperationDispatcher for Batch Submission**
Objective: sort pending entries by `occurred_at`, submit as one `POST /v1/sync/batch` call, bounded-size chunking for large backlogs.
Files to modify: `SyncOperationDispatcher` (core-data).

**Task 03 — Implement SyncApi (Ktor)**
Objective: `POST /v1/sync/batch` client.
Files to create/modify: `SyncApi.kt`.

**Task 04 — Implement Response Handling (Outbox Clearing)**
Objective: clear `applied`+`duplicate`, retain `rejected`.
Files to modify: `SyncOperationDispatcher`.

**Task 05 — Add Causal-Order & Mixed-Response Tests (highest priority)**
Tests: `CausalOrderSubmissionTest.kt`, `MixedResponseOutboxClearingTest.kt`.

**Task 06 — Add End-to-End Multi-Feature-Module Test**
Tests: `MultiFeatureModuleOutboxTest.kt`.

**Task 07 — Wire Analytics Events**

**Task 08 — Final Review**
Objective: confirm no feature module bypasses `SyncQueue.enqueue()` for a write action that should be offline-durable; confirm `client_event_id` generation happens exactly once, at action time.

## 30. Definition of Done
- All offline-capable feature modules' writes confirmed routed through the existing `SyncQueue`.
- Batch submission sorted correctly and bounded-size chunked for large backlogs.
- Mixed-response outbox clearing verified.
- End-to-end multi-feature-module test green.

## 31. Final Verification Checklist
- [ ] No feature module bypasses `SyncQueue.enqueue()` for an offline-durable write action.
- [ ] `client_event_id` generated once at action time, stable across retries.
- [ ] Batch submitted sorted by `occurred_at`, never relying solely on server-side reordering.
- [ ] `applied`/`duplicate` entries cleared; `rejected` entries remain queued.
- [ ] Large offline backlog submitted in bounded, sequential batches.
- [ ] End-to-end multi-module batch test passes.
