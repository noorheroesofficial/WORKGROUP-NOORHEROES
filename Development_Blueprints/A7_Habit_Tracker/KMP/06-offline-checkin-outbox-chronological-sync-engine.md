# K-06 — Offline Check-In Outbox & Chronological Sync Engine

## 1. Feature Context
NoorHeroes KMP app. The shared offline-first write engine underlying every habit check-in interaction (checklist taps, Dhikr batches, good-deed logs), ensuring correct multi-day backfill reconciliation.

## 2. Parent Feature
A.7 Habit Tracker — KMP App (Android/iOS)

## 3. Sub-feature
K-06 Offline Check-In Outbox & Chronological Sync Engine

## 4. Objective
Build a Room-backed offline outbox for check-ins keyed by `client_request_id`, with a background sync worker processing queued items in ascending `local_date` order regardless of insertion order, backing FR-2, FR-20, Edge Cases 4 and 12.

## 5. Business Requirements
- Full offline check-in capability; local state updates immediately (FR-2).
- Offline items queued with `client_request_id`, generated at tap time and reused on retry (never regenerated).
- Sync processes items in ascending `local_date` order (oldest first) regardless of queue-insertion order, to ensure correct server-side streak recomputation across a gap (Edge Case 12).
- Two-children-share-device: a queued check-in stays attributed to the acting child's `child_id` captured at action time, not sync time, even if the active session switches before sync (Edge Case 4).
- Sync failures use exponential backoff, never surfaced as a child-facing error.

## 6. Existing Architecture
This is the canonical offline-outbox implementation for `feature-habits`. **Reconciliation required:** A2's blueprint (`feature/home/.../HabitCheckinOutboxDao.kt`, `HabitCheckinSyncWorker.kt`) already implements a simplified version of this same mechanism scoped to the Home widget's simplified contract. This sub-feature should either (a) generalize A2's existing outbox to the full B-02 contract and have the Home widget consume it, or (b) build the canonical version here and schedule A2's outbox for deprecation/migration in a follow-up. Flag this decision explicitly for architecture review rather than silently maintaining two outbox implementations for the same underlying data.

Uses **Room** (multiplatform, `BundledSQLiteDriver`) and the project's existing background-sync mechanism — verify whether the codebase uses `WorkManager` (Android-only, as A2's blueprint assumed) or a KMP-multiplatform-correct scheduling mechanism (e.g., a Koin-managed coroutine-based sync service triggered on network-availability callbacks from `core-network`) — **prefer the multiplatform-correct approach** for `feature-habits` since this app targets both Android and iOS, correcting A2's Android-only `WorkManager` assumption for the canonical implementation.

## 7. Existing Code to Reuse
- A2's `HabitCheckinOutboxDao.kt` pattern (as a reference, generalized rather than duplicated)
- `core-network` connectivity-observer utilities for reconnect-triggered sync
- `core-database` Room conventions

## 8. Files to Create
- `feature-habits/src/commonMain/kotlin/.../outbox/HabitCheckInOutboxDao.kt` (Room)
- `feature-habits/src/commonMain/kotlin/.../outbox/HabitCheckInOutboxEntity.kt`
- `feature-habits/src/commonMain/kotlin/.../outbox/HabitCheckInSyncEngine.kt` (multiplatform sync orchestrator)
- `feature-habits/src/commonTest/kotlin/.../ChronologicalSyncOrderTest.kt`
- `feature-habits/src/commonTest/kotlin/.../MultiChildAttributionTest.kt`

## 9. Files to Modify
- `HabitChecklistViewModel.kt` (K-01), `DhikrCounterViewModel.kt` (K-02), `GoodDeedViewModel.kt` (K-03) — all route through this shared outbox rather than implementing their own queuing

## 10. Backend Requirements
Consumes `POST /v1/habits/check-ins` (B-02), whose idempotency guarantees (DB unique constraint + `client_request_id`) make this outbox's retry-safe by design.

## 11. KMP Requirements
- `HabitCheckInOutboxEntity(client_request_id PK, child_id, habit_id, local_date, timezone, source, note_category, status, retry_count, created_at)`.
- `client_request_id` generated once at the tap/action moment; reused verbatim on every retry.
- `child_id` captured at action time and persisted with the outbox row — never re-resolved from "current session" at sync time (Edge Case 4).
- Sync engine processes the queue in **ascending `local_date`** order on each sync attempt, regardless of insertion order.
- Exponential backoff on transient failure; entries removed only on confirmed success or confirmed idempotent-duplicate response.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
`POST /v1/habits/check-ins` (B-02) — idempotent by design, safe for unlimited retry with the same `client_request_id`.

## 14. Database Requirements (Local)
Room table `habit_checkin_outbox` per §11 entity definition; index on `(status, local_date)` for efficient ordered-queue queries.

## 15. Validation
Mandatory test: queue check-ins for "today," "yesterday," and "3 days ago" in that insertion order (out of chronological order); assert sync submits them in chronological order regardless of queue-insertion order (PRD §7 Android prompt item 3).

## 16. Authentication
Shared `core-network` Bearer token attachment on each sync request.

## 17. Authorization
N/A at this layer (server-enforced per-request in B-02).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Network failure during sync | Exponential backoff retry; entry remains queued, never shown as a child-facing error |
| Server returns duplicate/idempotent success | Entry removed from queue, treated identically to a fresh success |
| Multi-day gap backfill | All queued entries reconciled in chronological order in a single sync pass |
| Device/session switch mid-queue | Queued entry's persisted `child_id` is used, not the currently-active session |

## 19. Offline First
This sub-feature **is** the offline-first mechanism for Habit Tracker — full write capability offline, synced opportunistically and correctly ordered on reconnect.

## 20. Local Data
```
Tap/action (any habit type)
   ↓
client_request_id + child_id captured at action time
   ↓
Room habit_checkin_outbox (queued)
   ↓
HabitCheckInSyncEngine (ascending local_date order)
   ↓
POST /v1/habits/check-ins (B-02, idempotent)
```

## 21. Localization
N/A (internal sync mechanism, no user-facing strings beyond the shared "syncing..." indicator owned by K-01).

## 22. RTL
N/A.

## 23. Analytics
`backfilled_checkin_synced` fired per successfully reconciled historical entry.

## 24. Performance
Batched sync pass processes the full ordered queue per trigger, avoiding one network round-trip per entry where feasible; respects existing network/battery-awareness conventions from `core-network`.

## 25. Security
`client_request_id` is a client-generated UUID, non-guessable/sequential; outbox data is low-sensitivity (habit-completion booleans and dates, not raw content).

## 26. Library Requirements
Room (`BundledSQLiteDriver`), Kotlin Coroutines, `core-network` connectivity observers, Koin.

## 27. Testing
- Mandatory: chronological sync-order test regardless of insertion order (§15).
- Mandatory: multi-child attribution correctness test (Edge Case 4) — queued entry retains acting child's `child_id` even after an active-session switch.
- Integration: full offline → backgrounded → reconnect → correct streak recomputation flow (coordinates with B-03's server-side recomputation), including a multi-day-gap backfill scenario.
- Unit: exponential backoff behavior, idempotent-duplicate handling.

## 28. Documentation
KDoc explaining why chronological (not insertion) order is required, tying directly to B-03's streak state-machine correctness dependency on gap-free historical reconstruction.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Outbox Entity, DAO, and Migration Strategy from A2's Existing Implementation**
- Objective: Canonical outbox schema; resolve the A2 reconciliation decision from §6.
- Why Required: Establishes single source of truth for offline habit writes across the whole app.
- Files to Create: `HabitCheckInOutboxEntity.kt`, `HabitCheckInOutboxDao.kt`
- Files to Modify: coordinate with A2's `HabitCheckinOutboxDao.kt` per the reconciliation decision.
- Tests: DAO CRUD unit tests, ordered-query test.
- Definition of Done: single canonical outbox schema in place; reconciliation decision documented and (if chosen) A2 migration path scheduled.

**Task 02 — Implement Multiplatform Sync Engine**
- Objective: `HabitCheckInSyncEngine` triggered on connectivity restoration.
- Files to Create: `HabitCheckInSyncEngine.kt`
- Implementation Details: ascending `local_date` ordered processing; exponential backoff; idempotent-duplicate handling.
- Business Rules: FR-20, Edge Case 12.
- Tests: mandatory chronological-order test (§15).
- Do Not Change: do not process in insertion order under any optimization; chronological order is a correctness requirement, not a preference.
- Definition of Done: chronological-order test passes.

**Task 03 — Implement Multi-Child Attribution Correctness**
- Objective: Verify `child_id` persisted at action time survives session switches.
- Files to Modify: `HabitCheckInSyncEngine.kt`
- Tests: mandatory multi-child attribution test (Edge Case 4).
- Definition of Done: test passes.

**Task 04 — Wire All Habit-Type ViewModels to the Shared Outbox**
- Files to Modify: `HabitChecklistViewModel.kt`, `DhikrCounterViewModel.kt`, `GoodDeedViewModel.kt`
- Definition of Done: no ViewModel implements its own ad hoc queuing; all route through `HabitCheckInSyncEngine`.

**Task 05 — Add Integration Test for Full Offline-Backfill Scenario**
- Files to Create: instrumented integration test per §27.
- Definition of Done: multi-day backfill scenario passes end-to-end, coordinated with B-03's server-side test fixtures.

**Task 06 — Final Code Review**
- Do Not Change: idempotency-key generation timing (must remain at action time, never regenerated on retry).
- Expected Result: PR merge-ready.

## 30. Definition of Done
Shared offline outbox live, chronologically-ordered sync verified, multi-child attribution correctness verified, all habit-type flows routed through the single canonical mechanism.

## 31. Final Verification Checklist
- [ ] Chronological sync-order test passes regardless of insertion order (mandatory)
- [ ] Multi-child attribution test passes (Edge Case 4, mandatory)
- [ ] `client_request_id` generated once at action time, never regenerated on retry
- [ ] Exponential backoff implemented for transient failures
- [ ] Idempotent-duplicate responses correctly clear the queue entry
- [ ] A2's existing outbox reconciliation decision documented and actioned
- [ ] All habit-type ViewModels route through this shared engine
- [ ] Full offline-backfill integration test passes
