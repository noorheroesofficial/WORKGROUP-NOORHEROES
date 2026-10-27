# K-06 — Offline Inventory Cache & Equip Outbox Sync

## 1. Feature Context
NoorHeroes KMP app (Android/iOS). Part of Feature A.12 — Avatar System. Implements full offline rendering of the last-synced inventory state and an outbox mechanism for equip/unequip actions taken while offline, syncing on reconnect.

## 2. Parent Feature
A.12 Avatar System — KMP App (Android/iOS)

## 3. Sub-feature
K-06 Offline Inventory Cache & Equip Outbox Sync

## 4. Objective
Implement Room-backed offline rendering of `avatar_inventory_cache` and a WorkManager/coroutine-scheduled outbox for equip/unequip actions taken offline, backing FR-6 (offline-tolerant equip) and PRD §1.14 Offline States.

## 5. Business Requirements
- Last-synced avatar state (owned items, equipped state) renders fully offline (PRD §1.14).
- Equip actions taken offline queue and sync on reconnect, consistent with the platform's offline-first equip pattern (FR-6).
- Locked-item criteria display uses cached catalog data even offline; auto-unlock evaluation itself requires connectivity (it's a server-side process, B-02) — the child is never blocked from viewing/equipping their already-owned items offline (§1.14).
- Offline-queued equip actions must reconcile correctly with server state on sync — including the case where a queued equip is rejected on sync (e.g., ownership state changed server-side in the interim).

## 6. Existing Architecture
Extends `feature-avatar`/`feature-avatar-domain` established in K-01–K-05. Follows the platform's standard offline-outbox pattern already established by A.7 K-06's habit check-in outbox (Room-backed outbox table + WorkManager-scheduled sync worker) — this sub-feature applies the identical mechanism to equip/unequip actions instead of habit check-ins. Per A.7 K-01's precedent, the project's actual stack is **Room with `BundledSQLiteDriver`** (KMP-multiplatform) for local storage and the project's existing background-work scheduling mechanism (WorkManager on Android; the project's established KMP-multiplatform equivalent on iOS, per `core-database`/`core-network`'s existing sync-worker conventions) — not an Android-only WorkManager assumption.

## 7. Existing Code to Reuse
- `InventoryRepository`/`avatar_inventory_cache` (K-01)
- `EquipItemUseCase`/`UnequipItemUseCase` (K-02)
- A.7 K-06's offline-outbox Room table + sync-worker pattern (structural reference)
- `core-network` connectivity-observer utility (existing reconnect-detection mechanism)

## 8. Files to Create
- `feature-avatar/src/commonMain/kotlin/.../offline/EquipOutboxEntry.kt` (Room entity)
- `feature-avatar/src/commonMain/kotlin/.../offline/EquipOutboxDao.kt`
- `feature-avatar/src/commonMain/kotlin/.../offline/EquipOutboxSyncWorker.kt`
- `feature-avatar-domain/src/commonMain/kotlin/.../QueueOfflineEquipUseCase.kt`
- `feature-avatar/src/commonTest/kotlin/.../EquipOutboxSyncTest.kt`

## 9. Files to Modify
- `feature-avatar/src/commonMain/kotlin/.../screen/AvatarViewModel.kt` (K-01/K-02) — when `equip()`/`unequip()` is invoked while offline (per `core-network` connectivity state), route through `QueueOfflineEquipUseCase` instead of the direct online call, while still applying the same optimistic local UI update from K-02
- `core-database` Room database schema registration — register `EquipOutboxEntry`/`EquipOutboxDao`

## 10. KMP Requirements
- `EquipOutboxEntry` (Room entity): `id`, `childId`, `itemId`, `action` (`EQUIP`|`UNEQUIP`), `slot`, `queuedAt`, `syncStatus` (`PENDING`|`SYNCING`|`FAILED`).
- `QueueOfflineEquipUseCase`: when offline, writes an `EquipOutboxEntry` and immediately applies K-02's optimistic local state update — the child's experience is identical whether online or offline (instant visual feedback either way).
- `EquipOutboxSyncWorker`: triggered on reconnect (via `core-network`'s connectivity observer), processes pending outbox entries in `queuedAt` order, calling B-01's equip/unequip endpoints (idempotent server-side, safe for retry).
- On sync success, the outbox entry is removed and the local optimistic state is confirmed (no visible change, since it was already correct).
- On sync rejection (e.g., `403 ITEM_NOT_OWNED` — ownership state changed server-side while offline), the outbox entry is marked `FAILED`, removed, and the local state is rolled back per K-02's existing rejection-handling logic, with a non-alarming message shown to the child on next screen view.
- If multiple offline equip actions were queued for the *same slot* (e.g., child tried on three different offline outfits in sequence), only the **last** queued action for that slot needs to actually reach the server as authoritative (earlier same-slot entries are superseded) — the outbox processor should collapse same-slot entries to the most recent before syncing, consistent with the platform's last-tap-wins principle (mirroring K-02's rapid-tap handling, extended to the offline-queue case).

## 11. Backend Requirements
Consumes `POST /v1/children/{id}/inventory/{itemId}/equip`/`.../unequip` (B-01) — both are idempotent and safe for the outbox's retry/redelivery pattern.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
`POST /v1/children/{id}/inventory/{itemId}/equip` / `.../unequip` (B-01), invoked by `EquipOutboxSyncWorker` on reconnect.

## 14. Database Requirements (Local)
Room table `equip_outbox`: `id TEXT PK`, `child_id TEXT`, `item_id TEXT`, `action TEXT`, `slot TEXT`, `queued_at INTEGER`, `sync_status TEXT`. Index `(child_id, slot, queued_at)` to support the same-slot-collapse logic (§10).

## 15. Validation
Unit test simulating the full offline-equip-then-reconnect-then-sync flow: queue an offline equip, simulate reconnect, assert the sync worker calls B-01's endpoint exactly once for the correct final item, and the outbox entry is cleared on success (mandatory offline-sync integration test per PRD §6.10/§7).

## 16. Authentication
Reuses shared `core-network` Bearer token attachment; the sync worker authenticates identically to any other online request once connectivity resumes.

## 17. Authorization
N/A at UI/outbox layer (enforced server-side, B-01, upon actual sync).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Equip attempted while offline | Optimistic local update applied immediately (K-02's logic); action queued in `equip_outbox` |
| Multiple offline equips in the same slot | Collapsed to the last-queued action before sync; only that one reaches the server |
| Sync fails due to server-side ownership rejection | Outbox entry marked `FAILED`, removed; local state rolled back per K-02; non-alarming message shown |
| Sync worker interrupted mid-batch (app killed) | Remaining pending entries persist in Room and resume processing on next connectivity/app-start event, no data loss |
| Reconnect while another equip is already syncing | Sync worker processes entries sequentially per child to avoid racing concurrent writes to the same slot |

## 19. Offline First
This sub-feature **is** the offline-first mechanism for equip/unequip — K-01/K-02's read/optimistic-update layers depend on this sub-feature's outbox to fully honor the offline-tolerant equip requirement (FR-6) rather than only working online.

## 20. Local Data
```
AvatarViewModel.equip() [offline detected via core-network]
   ↓
QueueOfflineEquipUseCase → Room equip_outbox (+ optimistic UI update via K-02)
   ↓
[reconnect detected]
   ↓
EquipOutboxSyncWorker → collapse same-slot entries → POST equip/unequip (B-01)
   ↓
[success] clear outbox entry / [rejection] rollback + clear outbox entry
```

## 21. Localization
Sync-failure messages resolved via string resources (English, Hindi, Arabic, Urdu), reusing K-02's existing rejection-message localization.

## 22. RTL
N/A directly (no new user-facing layout beyond reusing K-02's existing rejection-message presentation, already RTL-verified there).

## 23. Analytics
Contributes to the same `avatar_item_equipped`/`avatar_item_unequipped` events fired optimistically by K-02 regardless of online/offline path; no duplicate firing on successful sync (the event already fired at the moment of the optimistic action, not again at sync confirmation).

## 24. Performance
Outbox processing runs on reconnect via the existing background-work scheduling mechanism, batched and sequential per child to avoid redundant network calls; same-slot collapsing (§10) reduces unnecessary sync traffic for a child who tried on several items offline before settling on one.

## 25. Security
No new sensitive data handling; the outbox stores only item/slot/action identifiers, no payment or PII data (consistent with FR-5's no-payment-path guarantee).

## 26. Library Requirements
Room (`BundledSQLiteDriver`), the project's existing background-work scheduling mechanism (WorkManager on Android / KMP-multiplatform equivalent on iOS per `core-network`/`core-database` conventions), kotlinx-coroutines.

## 27. Testing
- Unit: `EquipOutboxEntry` same-slot-collapse logic — multiple queued entries for one slot reduce to exactly one authoritative sync call.
- Integration (mandatory): full offline-equip → reconnect → sync flow, asserting exactly one correct server call and correct outbox cleanup.
- Integration: sync rejection correctly rolls back local state and clears the failed outbox entry.
- Integration: app-killed-mid-sync recovery — pending entries persist and resume correctly on next launch/reconnect.

## 28. Documentation
KDoc on `EquipOutboxSyncWorker` explaining the same-slot-collapse rule and its relationship to K-02's rapid-tap last-tap-wins principle, generalized to the offline-queue case.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define `EquipOutboxEntry` Room Entity & DAO**
- Objective: local outbox schema per §14.
- Existing Architecture to Follow: A.7 K-06's habit-check-in outbox entity/DAO structure.
- Files to Create: `EquipOutboxEntry.kt`, `EquipOutboxDao.kt`
- Files to Modify: `core-database` Room schema registration.
- Tests: DAO unit tests (insert, query by slot, delete).
- Definition of Done: entity persists and queries correctly.

**Task 02 — Implement `QueueOfflineEquipUseCase`**
- Objective: offline-path equip/unequip queuing, applying K-02's optimistic update simultaneously.
- Files to Create: `QueueOfflineEquipUseCase.kt`
- Files to Modify: `AvatarViewModel.kt` (route to this use case when `core-network` reports offline).
- Tests: unit test confirming optimistic update fires identically whether online or offline.
- Definition of Done: offline equip is visually indistinguishable from online equip to the child.

**Task 03 — Implement Same-Slot Collapse Logic**
- Objective: reduce multiple queued same-slot entries to the last one before sync.
- Files to Modify: `EquipOutboxDao.kt` or a dedicated collapse function called by the sync worker.
- Tests: unit test with three same-slot queued entries, asserting only the last is synced.
- Definition of Done: collapse logic verified correct and does not affect entries in different slots.

**Task 04 — Implement `EquipOutboxSyncWorker`**
- Objective: reconnect-triggered sequential sync processing.
- Files to Create: `EquipOutboxSyncWorker.kt`
- Existing Architecture to Follow: A.7 K-06's sync-worker pattern.
- Implementation Details: subscribe to `core-network` connectivity observer; process pending entries sequentially per child; handle success/rejection per §18.
- Tests (mandatory): full offline-equip-then-reconnect-then-sync integration test.
- Definition of Done: mandatory integration test passes.

**Task 05 — Implement Rejection Rollback Integration**
- Objective: wire sync-rejection handling to K-02's existing rollback logic.
- Files to Modify: `EquipOutboxSyncWorker.kt`
- Tests: sync-rejection integration test.
- Definition of Done: rejected offline equip correctly rolls back and clears the outbox entry.

**Task 06 — Add App-Killed-Mid-Sync Recovery Test & Documentation**
- Files to Create: `tests/.../EquipOutboxSyncTest.kt`
- Documentation: KDoc per §28.
- Definition of Done: recovery test passes; documentation complete.

**Task 07 — Final Code Review**
- Do Not Change: A.7 K-06's habit-outbox implementation (structural reference only, not modified); K-02's optimistic-update/rollback logic (reused, not duplicated).
- Expected Result: PR merge-ready.

## 30. Definition of Done
Equip/unequip actions taken offline are queued, visually indistinguishable from online actions, correctly collapsed per-slot, and reliably synced on reconnect with correct rollback handling on server rejection — with no data loss even if the app is killed mid-sync.

## 31. Final Verification Checklist
- [ ] `EquipOutboxEntry`/`EquipOutboxDao` implemented and registered in `core-database`
- [ ] Offline equip applies the identical optimistic UI update as online equip (K-02 reused, not duplicated)
- [ ] Same-slot collapse logic verified (only the last queued action per slot syncs)
- [ ] Full offline-equip → reconnect → sync integration test passes
- [ ] Sync-rejection correctly rolls back local state and clears the outbox entry
- [ ] App-killed-mid-sync recovery verified (no data loss)
- [ ] No duplicate analytics firing on sync confirmation (fired once, at optimistic-action time)
- [ ] No PII/payment data ever stored in the outbox
