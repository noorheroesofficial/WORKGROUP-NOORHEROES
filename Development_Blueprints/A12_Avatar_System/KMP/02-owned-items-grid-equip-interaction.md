# K-02 — Owned Items Grid & Equip/Unequip Interaction

## 1. Feature Context
NoorHeroes KMP app (Android/iOS). Part of Feature A.12 — Avatar System. Implements the owned-items grid interaction layer within the Avatar Screen (K-01): equip/unequip actions with optimistic UI, one-equipped-per-slot local invariant, and server reconciliation.

## 2. Parent Feature
A.12 Avatar System — KMP App (Android/iOS)

## 3. Sub-feature
K-02 Owned Items Grid & Equip/Unequip Interaction

## 4. Objective
Implement `AvatarViewModel`'s `equip()`/`unequip()` actions as optimistic, locally-slot-invariant, server-reconciled operations, backing FR-2, FR-6, NFR Performance (equip latency p95 < 300ms), and Edge Case 4.

## 5. Business Requirements
- Equip is optimistic: the avatar preview updates immediately on tap, before the server responds (FR-6).
- One-equipped-item-per-slot is enforced in the client's local state model as well as the server's, for instant correct local UX (mirroring B-01's server-side invariant).
- Server rejection (e.g., `403 ITEM_NOT_OWNED` from a stale client state) rolls back the optimistic change and shows a brief non-alarming "couldn't equip that" message — never leaves the UI in an incorrect optimistic state.
- Rapid repeated taps across items in the same slot resolve to a stable last-tap-wins state, without flicker or an inconsistent intermediate render (Edge Case 4).
- Equip action tap-to-local-update latency budget < 300ms (server-confirmed round trip; local optimistic update itself is near-instant).

## 6. Existing Architecture
Extends `feature-avatar`/`feature-avatar-domain` established in K-01. Follows the platform's standard optimistic-update pattern already established by A.2 Home's habit-checkin widget and A.7's Habit Builder checklist (per-row/per-item independent optimistic state via a keyed state map, not a single screen-wide loading flag) — this sub-feature applies the identical pattern at the item/slot level instead of the habit-row level.

## 7. Existing Code to Reuse
- `AvatarViewModel`/`AvatarUiState`/`InventoryRepository` (K-01)
- `core-network` Ktor client setup
- `core-analytics` `AnalyticsTracker`
- Optimistic-update/reconciliation pattern reference from A.7 K-01's `HabitChecklistViewModel` (per-row `RowState` keying, adapted here to per-slot equipped-item keying)

## 8. Files to Create
- `feature-avatar/src/commonMain/kotlin/.../grid/OwnedItemsGrid.kt` (Composable)
- `feature-avatar-domain/src/commonMain/kotlin/.../EquipItemUseCase.kt`
- `feature-avatar-domain/src/commonMain/kotlin/.../UnequipItemUseCase.kt`
- `feature-avatar/src/commonTest/kotlin/.../EquipReconciliationTest.kt`
- `feature-avatar/src/commonTest/kotlin/.../OneEquippedPerSlotLocalInvariantTest.kt`

## 9. Files to Modify
- `feature-avatar/src/commonMain/kotlin/.../screen/AvatarViewModel.kt` (K-01) — add `equip(itemId)`/`unequip(itemId)` action handlers
- `feature-avatar/src/commonMain/kotlin/.../data/InventoryRepository.kt` (K-01) — add `equip()`/`unequip()` methods calling B-01's endpoints

## 10. Backend Requirements
Consumes `POST /v1/children/{id}/inventory/{itemId}/equip` and `POST /v1/children/{id}/inventory/{itemId}/unequip` (B-01).

## 11. KMP Requirements
- `AvatarViewModel.equip(itemId)`: immediately updates `AvatarUiState.equippedBySlot[slot] = itemId` (optimistic), immediately re-renders the 3D preview via K-01's `Avatar3DRenderer`, then calls `InventoryRepository.equip()`.
- On success response, no visible change (already optimistically correct); on failure (e.g., `403 ITEM_NOT_OWNED`), roll back `equippedBySlot[slot]` to the previously-equipped item and surface a brief, non-alarming inline message.
- Local one-equipped-per-slot enforcement: `equippedBySlot` is a `Map<Slot, ItemId>` by construction — assigning a new value for a slot key inherently replaces the prior value, structurally preventing two simultaneously-equipped items in one slot at the type level.
- Rapid-tap handling: use a `Channel`/debounced coroutine sequencing per slot so that only the last tap's request is authoritative for that slot's final reconciliation, while still sending each request (idempotent server-side per B-01) — avoid a naive "cancel-in-flight" approach that could drop a legitimately final request.
- `unequip(itemId)` mirrors the same optimistic/reconcile pattern, clearing `equippedBySlot[slot]` to a "nothing equipped in this slot" sentinel only where the PRD's underlying data model allows an empty slot (cross-reference B-01/Edge Case 2's default-equipped-state guarantee — in practice every slot always has *some* default item equipped, so `unequip` should be understood as "return to default," not "leave empty," unless product confirms otherwise; treat this as a flagged assumption pending explicit product confirmation rather than guessed silently).

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
`POST /v1/children/{id}/inventory/{itemId}/equip` (B-01) — Response `{ equipped: true, slot }`; `POST /v1/children/{id}/inventory/{itemId}/unequip` (B-01) — Response `{ equipped: false }`.

## 14. Database Requirements (Local)
No new local table; equip/unequip actions taken online write through directly to `avatar_inventory_cache` (K-01) upon server confirmation. Offline queuing is K-06's separate outbox concern — this sub-feature assumes connectivity for its core reconcile logic and delegates to K-06 when offline.

## 15. Validation
Unit test simulating a server rejection (`403 ITEM_NOT_OWNED`) and asserting the UI state rolls back to the previously-equipped item, never left in the optimistic (incorrect) state (mandatory, per PRD §7 Android prompt item 1). Unit test asserting the local `equippedBySlot` map never holds two items claiming the same slot under any sequence of rapid taps (mandatory, per PRD §7 Android prompt item 2).

## 16. Authentication
Reuses shared `core-network` Bearer token attachment (child-mode session).

## 17. Authorization
N/A at UI layer (enforced server-side, B-01); client-side ownership assumptions are always subordinate to server confirmation.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Equip request rejected (`403 ITEM_NOT_OWNED`) | Roll back optimistic state to previously-equipped item; brief "couldn't equip that" message |
| Network failure during equip | Optimistic state remains pending; retried via K-06's outbox on reconnect (delegated, not re-implemented here) |
| Rapid repeated taps in the same slot | Last tap's target becomes the final authoritative local state; all requests sent, server's idempotent handling (B-01) resolves the true final state |
| Unequip on an item not currently equipped | No-op locally; server call still made for consistency, idempotent response expected |

## 19. Offline First
This sub-feature's core reconcile logic assumes connectivity; offline equip actions are captured and queued by K-06's outbox, with this sub-feature's optimistic-update layer providing the immediate visual feedback regardless of connectivity state.

## 20. Local Data
Equip/unequip confirmed state written through to `avatar_inventory_cache` (K-01) on server success; optimistic pending state held in `AvatarUiState` only until reconciled.

## 21. Localization
"Couldn't equip that" and related inline messages resolved via string resources (English, Hindi, Arabic, Urdu) — no hardcoded user-facing strings.

## 22. RTL
Grid item selection/equipped-indicator visuals mirror correctly for RTL locales; verified via a dedicated RTL layout test.

## 23. Analytics
`avatar_item_equipped`, `avatar_item_unequipped` fired via `AnalyticsTracker.logEvent()` upon optimistic action (not upon server confirmation, consistent with the platform's existing "fire on user action, not round trip" analytics convention used elsewhere — flagged as following existing precedent rather than a new decision).

## 24. Performance
Optimistic local update is near-instant (<100ms perceived); server-confirmed round trip budget p95 < 300ms per PRD NFR. Row/item-scoped recomposition only — equipping one item must not trigger recomposition of unrelated grid items or slots.

## 25. Security
No new sensitive data handling; server remains authoritative for all ownership/equip state (§17).

## 26. Library Requirements
Compose Multiplatform, Koin, Ktor, kotlinx-coroutines (`Channel`/`Flow` for tap-sequencing).

## 27. Testing
- Unit (P0): server-rejection rollback test — simulate `403 ITEM_NOT_OWNED`, assert UI state reverts correctly.
- Unit (P0): one-equipped-per-slot local-state transition test — equip two different items in the same slot in sequence, assert only the most recent is ever marked equipped.
- Unit: rapid-tap sequencing test — multiple taps in quick succession resolve to a stable final state matching the last tap.
- UI: equipped-state visual indicator updates instantly on tap (optimistic), independent of network latency in the test harness.

## 28. Documentation
KDoc on `AvatarViewModel.equip()`/`unequip()` explaining the optimistic/reconcile/rollback contract and its relationship to B-01's server-side invariant.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement `EquipItemUseCase`/`UnequipItemUseCase`**
- Objective: domain-layer use cases wrapping `InventoryRepository.equip()`/`.unequip()`.
- Existing Architecture to Follow: `feature-avatar-domain` use-case pattern from K-01.
- Files to Create: `EquipItemUseCase.kt`, `UnequipItemUseCase.kt`
- Tests: use-case unit tests (mocked repository).
- Definition of Done: use cases correctly delegate to repository and surface success/failure results.

**Task 02 — Extend `InventoryRepository` with Equip/Unequip Methods**
- Objective: `equip(itemId)`/`unequip(itemId)` Ktor calls to B-01's endpoints.
- Files to Modify: `feature-avatar/src/commonMain/kotlin/.../data/InventoryRepository.kt`
- Tests: repository unit tests (mocked Ktor client) including a `403` rejection fixture.
- Definition of Done: repository methods correctly surface both success and rejection results to the ViewModel layer.

**Task 03 — Implement Optimistic Equip/Unequip in `AvatarViewModel`**
- Objective: core optimistic-update/reconcile/rollback logic with local one-equipped-per-slot enforcement.
- Files to Modify: `AvatarViewModel.kt` (K-01)
- Implementation Details: `Map<Slot, ItemId>` keying per §11; rollback-on-rejection; tap-sequencing via `Channel`.
- Business Rules: PRD Android prompt items 1–2 (P0).
- Tests: mandatory rollback test and one-equipped-per-slot test (§27, both P0).
- Do Not Change: do not defer the optimistic state update into a delayed/async block that could race with the render pass.
- Definition of Done: both P0 tests pass.

**Task 04 — Build `OwnedItemsGrid` Composable**
- Objective: UI implementation of the owned-items grid grouped by slot, with equipped-state visual indicator.
- Files to Create: `OwnedItemsGrid.kt`
- Implementation Details: tap handler invokes `AvatarViewModel.equip()`; equipped indicator bound to `equippedBySlot`.
- Localization/RTL: per §21/§22.
- Analytics: `avatar_item_equipped`/`avatar_item_unequipped` on tap.
- Tests: Compose UI test for equip-tap visual update and rapid-tap stability.
- Definition of Done: grid renders and responds correctly across all fixture states.

**Task 05 — Final Code Review**
- Do Not Change: K-01's `Avatar3DRenderer`/`AvatarUiState` structure beyond the additive `equip`/`unequip` fields.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Equip/unequip actions are optimistic, correctly reconciled against server responses with rollback on rejection, and enforce one-equipped-item-per-slot both locally and (via B-01) server-side, meeting the p95 < 300ms latency budget.

## 31. Final Verification Checklist
- [ ] Equip/unequip optimistic update is synchronous and immediate on tap
- [ ] Server-rejection rollback test passes (P0)
- [ ] One-equipped-per-slot local invariant test passes (P0)
- [ ] Rapid-tap sequencing resolves to a stable, correct final state
- [ ] Equipped-state visual indicator updates instantly and correctly
- [ ] Localization (EN/HI/AR/UR) and RTL verified
- [ ] Analytics events wired via `AnalyticsTracker`
- [ ] Performance budget (p95 < 300ms) validated
- [ ] Item/slot-scoped recomposition only (no unrelated grid re-renders)
