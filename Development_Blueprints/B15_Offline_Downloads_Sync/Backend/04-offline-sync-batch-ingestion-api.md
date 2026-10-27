# B-04 — Offline Sync Batch Ingestion API

## 1. Feature Context
Part of Feature B.15 (Offline Downloads & Sync). The system's single highest-priority integrity guarantee: the canonical entry point every offline-capable feature's queued client events (habit check-ins, quiz responses, story/audio/Quran progress, etc.) flow through on reconnect. Zero tolerance for duplicate rewards or lost progress.

## 2. Parent Feature
B.15 — Offline Downloads & Sync

## 3. Sub-feature
B-04 — Offline Sync Batch Ingestion API

## 4. Objective
Implement `POST /v1/sync/batch`, processing submitted events in ascending `occurred_at` order regardless of array order, performing pre-downstream-call idempotency dedup via B-05's `sync_event_log`, and routing each event to its owning domain service (`LearningService`, `RewardService`, and each consuming feature's own service) without reimplementing any of that business logic here.

## 5. Business Requirements
- FR-4: write-local-first → queue immutable events with client-generated IDs → sync in causal order on reconnect → server deduplicates via idempotency keys → furthest-valid-position for content progress; quiz attempts tracked separately.
- FR-9: rewards posted exactly once per qualifying completion event via the same idempotency-key mechanism used platform-wide (A.11) — sync never produces duplicate XP/Noor Heroes Points regardless of client retry count.
- Edge Case 7: extended offline period generating many events → processed in correct causal order on reconnect without overwhelming the server, batched/paginated if needed.
- Edge Case 8: a downloaded quiz package referencing later-withdrawn content — response still recorded for history on sync but excluded from mastery/reward calc (per A.8 FR-11); this service's job is correct delivery/ordering, not the withdrawal-exclusion logic itself.
- Edge Case 12: partial batch success (8 of 10 sync before a connection drop) — 2 unsynced events remain correctly queued and retried; the 8 already-synced events' idempotency keys prevent reprocessing if accidentally resubmitted.
- §5 Backend AI Prompt items 4–5: out-of-order array submission processed chronologically; replayed batch triggers **zero** downstream calls for already-processed events.

## 6. Existing Architecture
Same new `downloads` bounded context (`src/noorheroes/modules/downloads/`) houses the Offline Sync Engine alongside the Download Manifest Service, per the PRD's explicit framing of both as one canonical cross-cutting service pair — implemented as `src/noorheroes/modules/downloads/sync.py` (`SyncEngineService`) rather than a 12th bounded context, since it shares the same "canonical infra for every offline-capable feature" charter as B-01–B-03. Routing to downstream services uses direct in-process service calls (`LearningService`, `RewardService`, etc.), not Kafka — consistent with the platform's existing modular-monolith architecture (no event bus is introduced).

## 7. Existing Code to Reuse
- `core/deps.py` → `get_current_child`.
- `learning` module's `LearningService.submit_attempt()` — quiz/progress event routing target.
- `rewards` module's `RewardService.award_points()` — already idempotent-transaction-based (per `POST /v1/rewards/grant`'s existing pattern); B-04 supplies the same `client_event_id` as its idempotency key.
- `common/utils/clock.py` → `Clock`/`SystemClock` for consistent `occurred_at`/`processed_at` handling (and `TestClock` for deterministic ordering tests).
- `common/base_service.py` → `BaseService` for `SyncEngineService`.
- B-05's `SyncEventLogRepository` for the pre-downstream dedup lookup.

## 8. Files to Create
- `src/noorheroes/modules/downloads/sync.py` — `SyncEngineService(BaseService)` with `ingest_batch(child_ctx, events) -> List[ProcessedEvent]`.
- `src/noorheroes/modules/downloads/schemas.py` (extend) — `SyncEventRequest`, `SyncBatchRequest`, `ProcessedEvent`, `SyncBatchResponse`.
- `src/noorheroes/modules/downloads/routing.py` — `EVENT_TYPE_HANDLERS` registry mapping `event_type` → an async handler delegating to the owning domain service.
- `tests/modules/downloads/test_sync_batch_causal_order.py`.
- `tests/modules/downloads/test_sync_batch_pre_downstream_dedup.py`.
- `tests/modules/downloads/test_sync_batch_partial_failure.py`.

## 9. Files to Modify
- `modules/downloads/api.py` (B-01) — add `POST /v1/sync/batch` route to the shared `DownloadsRouter`.
- `modules/downloads/deps.py` — add `get_sync_engine_service` factory.

## 10. Backend Requirements
- `POST /v1/sync/batch`, `Depends(get_current_child)`.
- Sort the incoming `events[]` by `occurred_at` ascending in-memory before processing — **never** trust array order (§5 item 4).
- For each event, in sorted order: look up `client_event_id` in `sync_event_log` (B-05) **first**; if present with `status='applied'`, append `{ client_event_id, status: 'duplicate' }` to the response and **do not invoke any downstream service** for that event (§5 item 5, non-negotiable).
- For genuinely new events, route via `EVENT_TYPE_HANDLERS[event_type]` to the owning domain service, passing `client_event_id` through as that service's own idempotency key (e.g., `RewardService.award_points(..., idempotency_key=client_event_id)`).
- Record the outcome (`applied`/`rejected`) in `sync_event_log` in the same transaction as the downstream call where the downstream service supports transactional participation; otherwise record immediately after a confirmed downstream success/failure (never mark `applied` before the downstream call is confirmed).
- Malformed/unroutable events (`event_type` not in the registry) → `status: 'rejected'`, batch continues processing remaining events.
- Downstream service failure (timeout/5xx) → event remains un-logged (no `sync_event_log` row), so it is correctly retried on next batch submission — never mark `applied` on a failed downstream call.
- Content-progress events apply furthest-valid-position semantics (delegated to the owning service, e.g., `PlaybackSyncRepository`-equivalent backend logic); quiz attempts are tracked separately from progress, never merged.

## 11. KMP Requirements
Consumed by K-06 (Offline Progress Sync Outbox Integration) via `SyncOperationDispatcher`'s batch submission.

## 12. NextJS Requirements
N/A directly — batch volume/dedup/rejection metrics feed B-07, surfaced in N-02.

## 13. API Contract
**Endpoint:** `POST /v1/sync/batch`
**Auth:** Bearer, child-mode
**Request:**
```json
{ "events": [ { "event_type": "habit_checkin", "client_event_id": "uuid...", "occurred_at": "2026-08-17T10:00:00Z", "payload": {} } ] }
```
**Response 200:**
```json
{ "processed": [ { "client_event_id": "uuid...", "status": "applied" } ] }
```
**Idempotency:** per-event `client_event_id`; `status: "duplicate"` is a success outcome, never an error.
**Error Responses:** `401` (unauthenticated), `422` (malformed batch shape — e.g., missing `client_event_id`); individual bad events within an otherwise-valid batch are `status: "rejected"` in the 200 response, not a batch-level error.

## 14. Database Requirements
Uses B-05's `sync_event_log` exclusively for its own bookkeeping; writes to each owning domain's tables happen through that domain's already-hardened service/repository, never directly from `SyncEngineService`.

## 15. Validation
- `events` array required, reasonable max batch size enforced (e.g., 500) to bound per-request processing time — larger backlogs submitted across multiple batch calls (Edge Case 7), client-side chunking responsibility (K-06).
- Each event requires `event_type`, `client_event_id` (UUID), `occurred_at` (ISO 8601), `payload` (object).
- Unknown `event_type` → `rejected` per-event, not a batch-level `422`.

## 16. Authentication
`Depends(get_current_child)` — rejects non-child-mode tokens with `401`.

## 17. Authorization
Implicit family/child scoping; each routed event is additionally validated by its owning domain service against the same `child_id` (defense in depth — `SyncEngineService` never assumes the payload's internal references are safe without the downstream service's own checks).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Out-of-order array | Sorted by `occurred_at` before processing, transparently |
| Already-applied event replayed | `status: 'duplicate'`, zero downstream calls |
| Downstream service timeout/5xx | Event left un-logged, retried on next batch, not marked `applied` |
| Unknown `event_type` | `status: 'rejected'` for that event only, batch continues |
| Partial batch success | Unsynced events remain retriable; synced events' idempotency keys prevent reprocessing |
| Malformed batch shape | `422`, whole request rejected |
| Withdrawn-content quiz response | Recorded to history via `LearningService`, excluded from mastery/reward calc by that service's own logic (not B-04's concern) |

## 19. Offline First
N/A at backend layer — this is the reconnect-triggered sync target; offline queuing itself is entirely a KMP concern (K-06).

## 20. Local Data
N/A (backend).

## 21. Localization
N/A — data-only endpoint.

## 22. RTL
N/A.

## 23. Analytics
No direct client-facing analytics event; `offline_sync_batch_started`/`offline_sync_batch_completed`/`offline_sync_duplicate_prevented` are client-fired (K-06) based on this endpoint's response. Server-side: `OutboxWriter.emit()` for batch-level metrics consumed by B-07.

## 24. Performance
- In-memory sort of a bounded batch size (≤500) is negligible overhead relative to per-event downstream calls.
- Pre-downstream dedup lookup is a single indexed `sync_event_log(client_event_id)` query per event, batchable as one `IN (...)` query rather than N round-trips where the ORM supports it.
- Downstream calls within a batch execute sequentially in causal order (not parallelized), since later events may depend on earlier ones' state (e.g., furthest-position advancement) — documented as an intentional throughput/correctness tradeoff.

## 25. Security
- Pre-downstream-call dedup is the feature's highest-priority security-adjacent guarantee (prevents reward-duplication abuse via batch replay) — must be proven via a non-bypassable CI-gating test (§27).
- Each downstream service independently re-validates the event belongs to the authenticated child — `SyncEngineService` is a router, not a trust boundary of last resort.
- Standard rate limiting via existing `RateLimitMiddleware` on the batch endpoint (bounds abuse via rapid repeated large-batch submission).

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 (async), asyncpg. No Kafka/event-bus library introduced (correcting the PRD's generic Kafka-mention prompt — flagged as an architecture deviation, consistent with the B.15 breakdown's architecture note).

## 27. Testing
- Unit: array submitted out-of-order → asserted chronological processing order via a spy on `EVENT_TYPE_HANDLERS`.
- **Security/integrity test (mandatory, CI-blocking):** replay an already-applied batch → assert **zero** downstream handler invocations for those events, while genuinely new events in the same batch still process (§5 item 5).
- Integration: partial-batch failure — simulate a downstream 5xx for one event, assert the other events in the batch still apply, and the failed event remains retriable (un-logged) on resubmission.
- Integration: withdrawn-content quiz-response routing — recorded to history, excluded from reward calc (delegated assertion against `LearningService`'s existing test coverage, not reimplemented here).
- Staging-replay test against a historical fixture out-of-order/duplicate-laden batch (DevOps §10 CI gate).

## 28. Documentation
OpenAPI summary noting `status: "duplicate"` is a success outcome; explicit doc-comment on the pre-downstream-dedup guarantee and why it is architecturally non-bypassable.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Define Sync Batch Schemas**
Objective: `SyncEventRequest`, `SyncBatchRequest`, `ProcessedEvent`, `SyncBatchResponse`.
Files to create: extend `modules/downloads/schemas.py`.

**Task 02 — Build EVENT_TYPE_HANDLERS Routing Registry**
Objective: a registry mapping `event_type` string → async handler function delegating to the owning domain service.
Files to create: `modules/downloads/routing.py`.
Existing code to reuse: `LearningService.submit_attempt()`, `RewardService.award_points()`.

**Task 03 — Implement SyncEngineService.ingest_batch()**
Objective: sort by `occurred_at` → pre-downstream dedup lookup → route → record outcome.
Business rules: never mark `applied` before downstream confirmation; `duplicate` short-circuits before any handler call.
Files to create: `modules/downloads/sync.py`.

**Task 04 — Implement API Endpoint**
Objective: `POST /v1/sync/batch` wired into the shared `DownloadsRouter`.
Files to modify: `modules/downloads/api.py`, `modules/downloads/deps.py`.

**Task 05 — Add Causal-Order Test**
Tests: `test_sync_batch_causal_order.py`.

**Task 06 — Add Pre-Downstream-Dedup Test (highest priority)**
Tests: `test_sync_batch_pre_downstream_dedup.py`.
Definition of done: CI-blocking gate, non-negotiable per DevOps §10.

**Task 07 — Add Partial-Failure Test**
Tests: `test_sync_batch_partial_failure.py`.

**Task 08 — Add Staging-Replay Fixture Test & OpenAPI Docs**

**Task 09 — Final Code Review**
Objective: confirm zero downstream calls occur before the dedup lookup completes for every event; confirm no direct DB writes to any other module's tables from `SyncEngineService`.

## 30. Definition of Done
- `POST /v1/sync/batch` live, matches §13 contract exactly.
- Causal-order processing verified regardless of array order.
- Pre-downstream-call dedup verified as a CI-blocking gate.
- Partial-batch-failure retry semantics verified.
- Full test suite green including staging-replay fixtures.

## 31. Final Verification Checklist
- [ ] Events processed in `occurred_at` ascending order, never array order.
- [ ] Duplicate events trigger zero downstream calls — verified by automated test.
- [ ] Failed downstream calls never marked `applied`; remain retriable.
- [ ] Unknown `event_type` rejected per-event without failing the whole batch.
- [ ] No direct DB writes to other modules' tables from this service.
- [ ] No PostgreSQL/Redis credentials modified.
