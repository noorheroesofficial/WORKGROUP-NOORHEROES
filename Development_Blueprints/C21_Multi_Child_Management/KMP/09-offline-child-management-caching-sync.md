# K-09 — Offline Child Management Caching & Sync

## 1. Feature Context
Part of Feature C.21 — Multi-Child Management. The `:core:data` layer implementation underpinning every other KMP sub-feature's offline-first behavior in this domain.

## 2. Parent Feature
C.21 Multi-Child Management

## 3. Sub-feature
**K-09 — Offline Child Management Caching & Sync**

## 4. Objective
Provide a reliable, Flow-based, offline-first local cache of the family's children that every screen in this feature reads from, with correct read-only offline behavior and connectivity-aware auto-refresh.

## 5. Business Requirements
- §1.14 Offline States: list renders read-only from cache; all mutating actions require connectivity, shown clearly.
- NFR (Performance): list load p95 < 500ms — the local-cache-first pattern is what makes this achievable on the client regardless of network latency.

## 6. Existing Architecture
`:core:data`'s `FamilyRepository`, per `CORE_DATA_INSTRUCTIONS.md`: "Observe data via a repository Flow... Call refresh()... UI reacts automatically via the Flow." This is the concrete implementation task underlying K-01 through K-08's data dependency.

## 7. Existing Code to Reuse
- `ConnectivityObserver` — existing abstraction (per `CORE_DATA_INSTRUCTIONS.md` §9 "Don't: Access platform APIs directly — always go through ConnectivityObserver").
- `DispatcherProvider` — injected dispatchers, not hardcoded.
- Room `Child` entity/DAO — extend the existing one from A.1's onboarding flow rather than creating a parallel table.

## 8. Files to Create
- `core-data/src/commonMain/kotlin/.../repository/FamilyRepositoryImpl.kt` (if not already created incrementally by K-01/K-03's tasks — this sub-feature is where its full offline-sync contract is finalized and tested).

## 9. Files to Modify
- `core-database/.../ChildEntity.kt` — extend with `status`, `displayOrder`, `dobLockedAt` columns matching B-01's response shape.
- `core-database/.../ChildDao.kt` — add queries: `observeChildren(familyId): Flow<List<ChildEntity>>`, `upsertAll(children: List<ChildEntity>)`, `deleteById(childId)`.
- `core-data/.../di/RepositoryModule.kt` — register the finalized `FamilyRepository` binding.

## 10. Backend Requirements
Consumes B-01 for refresh; invalidated/updated by every mutating sub-feature (B-02 through B-08) via their respective repository wrappers.

## 11. KMP Requirements
- `observeChildren(): Flow<List<Child>>` — always emits from Room first; UI never blocks on network.
- `refreshChildren(): NoorResult<Unit>` — calls B-01, upserts the result into Room in a single transaction (replace-all-for-family semantics, since the list is small and B-01 returns the complete authoritative set every time — no need for complex diffing).
- Auto-refresh triggers: screen entry (K-01), and network-recovery events observed via `ConnectivityObserver` (per the "Scenario: Implementing an Offline-First Screen" pattern in `CORE_DATA_INSTRUCTIONS.md`).
- Cache invalidation after any successful mutation (disable/enable/delete/reorder/edit/create): each mutating repository method re-upserts the affected row(s) into Room immediately on success — no reliance on waiting for the next full refresh.
- Offline write attempts: repository methods for mutating actions check `ConnectivityObserver` state upfront and return a typed `NoorResult.Failure` with an `isOffline` flag the UI maps to "connect to make changes" messaging, rather than attempting and failing a doomed network call.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
Consumes B-01/B-02/B-03/B-04/B-05/B-06/B-07's contracts collectively; this sub-feature is the integration point, not a new contract itself.

## 14. Database Requirements
Room table `child` (local): `childId PK, familyId, nickname, dob, dobLockedAt, status, displayOrder, avatarId, createdAt, updatedAt` — mirrors B-01's response shape field-for-field to avoid a lossy mapping layer.

## 15. Validation
None — this is a data-synchronization layer, not a business-rule layer (rules are enforced server-side and surfaced via typed errors from each mutating call).

## 16. Authentication
Repository methods require an authenticated parent session, sourced from `:core:auth`, consistent with every other sub-feature.

## 17. Authorization
None beyond what individual mutating calls (B-02 through B-08) already enforce; this layer is a pass-through, not a policy layer.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Refresh fails, cache exists | Flow continues emitting cached data; error surfaced separately (e.g., a dismissible banner), never blocking the cached view |
| Refresh fails, no cache | Propagate as a genuine error state to the UI |
| Mutating call attempted offline | Return `isOffline` failure immediately, no network attempt made |
| Mutating call succeeds | Immediately re-upsert affected row(s), do not wait for next full refresh |

## 19. Offline First
This entire sub-feature **is** the offline-first implementation for C.21 — every other KMP sub-feature depends on it rather than talking to `:core:network` directly (per the architectural rule "Feature Modules → core-network or core-database" is prohibited; "Feature Modules → core-data" is the only allowed path).

## 20. Local Data
Room-backed, single source of truth for what every screen renders; network is purely a synchronization input, never read directly by the UI layer.

## 21. Localization
N/A — data layer only.

## 22. RTL
N/A — data layer only.

## 23. Analytics
None directly; this layer does not fire product-analytics events itself.

## 24. Performance
- Avoid main-thread blocking: all Room/network operations wrapped in `withContext(dispatchers.io)`.
- Avoid memory leaks: `Flow` collection scoped to `viewModelScope`/screen lifecycle, never held longer than needed.
- Replace-all-for-family upsert is a single transaction, not N individual row writes.

## 25. Security
No new security surface — reuses existing authenticated network layer and local Room encryption-at-rest (if configured platform-wide) without introducing feature-specific exceptions.

## 26. Library Requirements
No new libraries — Room, Ktor/Retrofit, Kotlin Coroutines/Flow already established.

## 27. Testing
- Unit: `observeChildren()` emits cached data immediately without waiting for a network call.
- Unit: `refreshChildren()` correctly upserts B-01's response into Room (replace-all-for-family).
- Unit: each mutating wrapper re-upserts only the affected row(s) on success, without requiring a full refresh.
- Integration: offline → online transition — a mutating action blocked while offline succeeds automatically-retriable (or clearly re-triggerable) once connectivity returns (confirm exact UX contract: auto-retry vs. manual re-tap — default to manual re-tap unless a `SyncQueue`-based approach is explicitly chosen, given these are step-up-gated actions that can't be silently replayed after the fact).
- Unit: main-thread-blocking check (static analysis or benchmark test) confirms no Room/network call occurs off the IO dispatcher.

## 28. Documentation
KDoc documenting the "replace-all-for-family" upsert strategy and explicitly why per-mutation re-upserting (rather than always waiting for a full refresh) is used, so future maintainers understand the caching contract.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Room Entity & DAO Extension**
- **Objective:** Extend `ChildEntity`/`ChildDao` to match B-01's full response shape.
- **Files to Modify:** `ChildEntity.kt`, `ChildDao.kt`.
- **Tests:** DAO unit tests for `observeChildren`/`upsertAll`/`deleteById`.
- **Definition of Done:** Schema matches B-01's contract field-for-field.

**Task 02 — `FamilyRepositoryImpl` Offline-First Contract**
- **Objective:** Implement `observeChildren()`/`refreshChildren()` plus per-mutation re-upsert hooks used by K-01 through K-08.
- **Files to Modify:** `FamilyRepositoryImpl.kt`.
- **Implementation Details:** Cache-first Flow; replace-all-for-family upsert on refresh; connectivity pre-check on every mutating method before attempting a network call.
- **Tests:** Full suite per §27.
- **Definition of Done:** Every other C.21 KMP sub-feature can depend on this repository without needing its own ad hoc caching logic.

**Task 03 — Connectivity-Aware Auto-Refresh**
- **Objective:** Trigger `refreshChildren()` on network recovery, in addition to screen-entry-driven refresh (owned by K-01).
- **Files to Modify:** `FamilyRepositoryImpl.kt` (or a dedicated sync coordinator if the existing `SyncQueue`/`SyncOperationDispatcher` pattern is the established convention for this — confirm against `sync/` package structure in `CORE_DATA_INSTRUCTIONS.md` before choosing an approach).
- **Tests:** Integration test simulating offline → online transition.
- **Definition of Done:** Refresh fires automatically on reconnect without requiring the user to manually pull-to-refresh.

## 30. Definition of Done
Offline-first contract is fully implemented, tested, and consumed uniformly by every other C.21 KMP sub-feature without duplicated caching logic.

## 31. Final Verification Checklist
- [ ] `observeChildren()` cache-first behavior verified
- [ ] Replace-all-for-family refresh upsert tested
- [ ] Per-mutation re-upsert verified for every mutating sub-feature (B-02 through B-08 wrappers)
- [ ] Offline mutating-action pre-check (no doomed network attempts) verified
- [ ] Connectivity-recovery auto-refresh verified
- [ ] No main-thread blocking (IO dispatcher usage confirmed)
- [ ] No feature module bypasses this layer to call `:core:network`/`:core:database` directly
