# K-03 — Habit & Good Deed Check-In Widget (Offline-First)

## 1. Feature Context
NoorHeroes Child App (KMP). Renders the frictionless, same-screen habit check-in checklist on Home, fully functional offline via a local outbox.

## 2. Parent Feature
A.2 — Child Home Dashboard & AI Personalization

## 3. Sub-feature
2.3 Habit & Good Deed Check-In Widget (Offline-First) (ID: K-03)

## 4. Objective
Build the habit checklist Composable with optimistic local updates, a Room-backed offline outbox using tap-time-generated idempotent `client_event_id`s, WorkManager-based retry on reconnect, and correct handling of `409 ALREADY_CHECKED_TODAY` as success (not rollback).

## 5. Business Requirements
Per PRD FR-7, FR-8, §6.7, §7 item 3, Edge Case 10:
- Same-screen check-in for at least Salah, Quran, dua, good deed, dhikr; deep-link to full Habit Builder for fasting/detailed logging.
- Streak display never shaming (gold fill, "Mercy Day" icon, never red warning).
- Optimistic UI update on tap, before network resolves.
- Offline: queue to local outbox with tap-time `client_event_id`, retry via WorkManager on reconnect, reusing the same UUID.
- `409 ALREADY_CHECKED_TODAY` treated as success — must NOT roll back the optimistic UI.
- Reconcile locally-queued offline check-ins in causal order on reconnect (deduplicated via idempotency keys) before showing "live" data, avoiding a visible streak regression flash.
- Empty state: friendly "ask a grown-up to set up your first habit" prompt when zero habits configured.

## 6. Existing Architecture
Follow `CORE_DATABASE_INSTRUCTIONS.md` (Room) and `CORE_DATA_INSTRUCTIONS.md` (repository/offline-outbox pattern) — reuse an existing outbox pattern if one already exists elsewhere in the codebase (e.g., from another offline-mutation feature) rather than inventing a new one.

## 7. Existing Code to Reuse
K-01's `SectionState`/`HomeUiState`; existing WorkManager setup/conventions from `CORE_DATA_INSTRUCTIONS.md`; `:core:design-system` streak/gold-fill tokens (per PRD §2.1 Home-Specific Design System Extensions).

## 8. Files to Create
- `feature/home/src/commonMain/kotlin/.../components/HabitChecklistWidget.kt`
- `feature/home/src/androidMain/kotlin/.../data/local/HabitCheckinOutboxDao.kt` (Room)
- `feature/home/src/commonMain/kotlin/.../data/HabitRepository.kt`
- `feature/home/src/androidMain/kotlin/.../sync/HabitCheckinSyncWorker.kt` (WorkManager)
- `feature/home/src/androidUnitTest/.../HabitCheckinOptimisticUpdateTest.kt`

## 9. Files to Modify
- `HomeScreen.kt` (K-01) — slot in habit widget
- `HomeUiState.kt` (K-01) — add `habits` field
- Room database module — register `HabitCheckinOutboxDao`/entity
- WorkManager initialization — register `HabitCheckinSyncWorker`

## 10. Backend Requirements
Consumes `POST /v1/habits/check-ins` (B-03) and the `habits` section of `GET /v1/home` (B-01).

## 11. KMP Requirements
- Checklist rows (icon + label + tap target) per configured habit.
- Tap → immediate optimistic local state update (checkbox ticks) before network call resolves.
- On network failure, write to Room outbox with a UUID `client_event_id` generated **at tap time** (not retry time), enqueue `HabitCheckinSyncWorker`.
- On `409 ALREADY_CHECKED_TODAY` response, treat as success — do not roll back the optimistic tick.
- On a genuine permanent failure (e.g., validation error, not network/idempotent-duplicate), roll back the optimistic tick and surface a subtle retry affordance.
- Streak mini-calendar peek; Mercy Day icon (gentle moon/star) instead of a crossed-out flame on a missed day.
- Deep link "Habit Builder" for fasting tracker/detailed logging.
- Empty state Composable when zero habits configured.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
`POST /v1/habits/check-ins` — Request `{ habit_id, date, client_event_id }` — Response `{ checked, current_streak, xp_awarded }` — `409 ALREADY_CHECKED_TODAY` treated client-side as success (per B-03 §13).

## 14. Database Requirements (Local)
Room table `habit_checkin_outbox(client_event_id PK, habit_id, date, created_at, retry_count, status)` — entries removed on confirmed sync (success or idempotent-duplicate), retained with incremented `retry_count` on transient failure.

## 15. Validation
`client_event_id` generated once per tap and persisted with the outbox entry — retries must reuse the same ID, never regenerate.

## 16. Authentication
Reuses shared network-layer Bearer token attachment.

## 17. Authorization
N/A at UI layer.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Network failure on tap | Optimistic tick stands; queued to outbox; subtle "saving..." indicator |
| `409 ALREADY_CHECKED_TODAY` | Treated as success; no rollback |
| Genuine validation failure (e.g., invalid habit_id) | Roll back optimistic tick; show retry affordance |
| Zero habits configured | Friendly setup-prompt empty state, not an empty checklist |

## 19. Offline First
This is the offline-first reference implementation for the Home feature: full write capability offline via the outbox, synced on reconnect in causal (submission) order, deduplicated via `client_event_id`.

## 20. Local Data
```
Remote Data (POST /v1/habits/check-ins)
   ↓
HabitRepository
   ↓
Room outbox (habit_checkin_outbox) — offline queue
   ↓
HomeUiState.habits (optimistic + reconciled)
```

## 21. Localization
Habit labels via string resources or pre-localized backend strings (follow K-01's established pattern); empty-state copy localized.

## 22. RTL
Checklist row layout (icon + label + checkbox) mirrors correctly; streak mini-calendar peek direction verified for RTL.

## 23. Analytics
`habit_checkin_widget_viewed`, `habit_checkin_completed_from_home`, `habit_checkin_failed_queued_offline`.

## 24. Performance
Outbox sync via WorkManager respects existing battery/network constraints conventions (`CORE_DATA_INSTRUCTIONS.md`); avoid tight-loop retry (exponential backoff per WorkManager's standard policy).

## 25. Security
`client_event_id` is a client-generated UUID, not guessable/sequential; no sensitive data in the outbox beyond habit/date references.

## 26. Library Requirements
Room, WorkManager, Kotlin Coroutines, existing network stack.

## 27. Testing
- Unit: optimistic update applies immediately on tap.
- Unit: `409` response does NOT trigger rollback (explicit regression test per PRD §7 item 8).
- Unit: genuine failure DOES trigger rollback.
- Integration: offline tap → outbox entry created → reconnect → `HabitCheckinSyncWorker` syncs → outbox entry cleared.
- Integration: causal-order reconciliation with multiple queued check-ins avoids a visible streak regression flash.

## 28. Documentation
KDoc explicitly calling out the `409`-is-success behavior as a deliberate design decision (to prevent future "bug fix" regressions that would break FR-8's non-punitive UX).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Room Outbox Entity + DAO**
- Objective: Local persistence for queued check-ins.
- Why Required: Offline-first requirement (FR-16 analog for habits, PRD §7 item 3).
- Existing Architecture to Follow: `CORE_DATABASE_INSTRUCTIONS.md` Room conventions.
- Existing Files to Reuse: Existing Room database module setup.
- Files to Create: `data/local/HabitCheckinOutboxDao.kt`, entity class
- Files to Modify: Room database module (register DAO/entity)
- Implementation Details: `client_event_id` as primary key, `status` enum (`PENDING`, `SYNCING`, `SYNCED`).
- Business Rules: One row per attempted check-in tap, keyed by its UUID.
- Validation: N/A.
- Error Handling: N/A.
- Security: N/A.
- Performance: Indexed by `status` for efficient WorkManager queries.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: DAO unit tests (insert/query/delete).
- Documentation: KDoc.
- Dependencies: None.
- Do Not Change: N/A.
- Expected Result: Outbox table live.
- Definition of Done: DAO tests pass.

**Task 02 — Implement `HabitRepository` with Optimistic Update + Outbox Fallback**
- Objective: Core offline-first write logic.
- Why Required: Central business logic of this sub-feature.
- Existing Architecture to Follow: Repository pattern from `CORE_DATA_INSTRUCTIONS.md`.
- Existing Files to Reuse: Task 01 DAO.
- Files to Create: `data/HabitRepository.kt`
- Files to Modify: none
- Implementation Details: `checkIn(habitId)` generates `client_event_id` at call time, attempts network call; on success or `409`, updates local `HomeUiState` optimistically-confirmed; on network failure, writes to outbox and returns an optimistic-pending result; on genuine validation failure, returns a rollback signal.
- Business Rules: `409` = success; genuine failure = rollback (explicit branching, not a generic catch-all).
- Validation: N/A.
- Error Handling: Distinguishes network failure (queue) vs. validation failure (rollback) vs. idempotent-duplicate (success) as three distinct paths.
- Security: N/A.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: `habit_checkin_failed_queued_offline` fired on the queue path.
- Tests: Unit tests for all three branching paths (success/queue/rollback).
- Documentation: KDoc with explicit warning about the three-path branching.
- Dependencies: Task 01.
- Do Not Change: Do not collapse the three error paths into a single generic handler.
- Expected Result: Working repository.
- Definition of Done: Branching unit tests pass.

**Task 03 — Implement `HabitCheckinSyncWorker` (WorkManager)**
- Objective: Reconnect-triggered outbox sync in causal order.
- Why Required: Edge Case 10 (causal-order reconciliation, dedup, no streak regression flash).
- Existing Architecture to Follow: Existing WorkManager conventions/constraints.
- Existing Files to Reuse: Task 01 DAO, Task 02 repository.
- Files to Create: `sync/HabitCheckinSyncWorker.kt`
- Files to Modify: WorkManager initialization (register worker, network-constraint trigger)
- Implementation Details: On network-available trigger, process outbox entries in `created_at` ascending order (causal order), calling the same repository check-in path (reusing the persisted `client_event_id`), removing synced entries.
- Business Rules: Causal order preserved; no reordering.
- Validation: N/A.
- Error Handling: Transient failure increments `retry_count` with backoff; does not drop the entry.
- Security: N/A.
- Performance: Batched processing, not one Worker invocation per entry.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Integration test — queue 3 offline check-ins, simulate reconnect, verify sync order and no duplicate `habit_checkin` rows server-side (coordinate with B-03's idempotency test).
- Documentation: KDoc.
- Dependencies: Tasks 01, 02.
- Do Not Change: N/A.
- Expected Result: Working sync worker.
- Definition of Done: Causal-order integration test passes.

**Task 04 — Build `HabitChecklistWidget` Composable + Empty State**
- Objective: UI for the checklist, streak peek, and empty state.
- Why Required: Primary UI deliverable.
- Existing Architecture to Follow: `:core:design-system` streak/gold-fill tokens.
- Existing Files to Reuse: K-01 shimmer, Task 02 repository.
- Files to Create: `components/HabitChecklistWidget.kt`
- Files to Modify: `HomeScreen.kt`, `HomeUiState.kt`
- Implementation Details: Checklist rows with tap-to-optimistically-check; streak mini-calendar with Mercy Day icon on missed days (never red/crossed-out flame); empty-state Composable when zero habits.
- Business Rules: Positive-framed visuals only (PRD §2.1).
- Validation: N/A.
- Error Handling: Subtle "saving..." indicator during queued state.
- Security: N/A.
- Performance: Minimal recomposition on single-row tap (row-scoped state).
- Localization: String resources.
- RTL: Row layout mirrors correctly.
- Analytics: `habit_checkin_widget_viewed`, `habit_checkin_completed_from_home`.
- Tests: Compose UI tests for tap interaction, empty state, Mercy Day icon rendering.
- Documentation: KDoc.
- Dependencies: Tasks 02, 03.
- Do Not Change: Do not use red/warning color treatment for missed streaks (explicit design rule).
- Expected Result: Working widget.
- Definition of Done: Compose UI tests pass.

## 30. Definition of Done
Habit check-in works fully offline with correct optimistic-update/rollback/idempotent-success branching, causal-order sync on reconnect, and non-shaming streak visuals; all tests green.

## 31. Final Verification Checklist
- [ ] Optimistic tick applies immediately on tap
- [ ] `409 ALREADY_CHECKED_TODAY` does not roll back the optimistic UI
- [ ] Genuine validation failure does roll back with a retry affordance
- [ ] Offline check-ins queue with tap-time `client_event_id`, reused on retry
- [ ] Reconnect sync processes queue in causal order, no duplicate server-side rows
- [ ] Streak visuals never use shaming/red treatment; Mercy Day icon used correctly
- [ ] Empty state shown when zero habits configured
- [ ] All tests pass
