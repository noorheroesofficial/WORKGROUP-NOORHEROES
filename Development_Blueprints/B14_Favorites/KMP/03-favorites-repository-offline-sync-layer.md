# K-03 — Favorites Repository: Offline-First Data & Sync Layer

## 1. Feature Context
Part of Feature B.14 Favorites. The single data-access layer between K-01/K-02 and the backend (B-01/B-02), owning local caching and offline sync so no screen or component talks to the network directly.

## 2. Parent Feature
B.14 Favorites (`PRD_Documents/Child App — Supporting (13-18)/Feature_B14_Favorites.md`)

## 3. Sub-feature
2.3 Favorites Repository — Offline-First Data & Sync Layer — `K-03`

## 4. Objective
Implement `FavoritesRepository` with `toggle()` and `getFavorites(type)`, offline-first read-through caching, and a `SyncQueue`-backed outbox for offline toggle actions, structurally deriving `child_id` from the active session rather than accepting it as a parameter.

## 5. Business Requirements
- §1.8: Favorites grid and toggle actions function fully offline, syncing on reconnect.
- Edge Case 5: offline favorite attempt queues locally, syncs via idempotent request on reconnect.
- §7 Android AI Code-Generation Prompt item 4: repository must derive `child_id` internally, never accept one from a calling screen.
- §6.7: local outbox keyed by `client_request_id`, synced via background work on reconnect.

## 6. Existing Architecture
`core-data` module pattern: `SafeDatabaseHelper.withTransaction(tableName, entityType) { }` for all local writes; `SyncQueueDao`/`SyncQueueEntity` (statuses `PENDING`/`IN_FLIGHT`/`FAILED`/`DEAD_LETTER`) for offline mutation queueing, auto-flushed on connectivity via `SyncHandler` with rollback support. `NoorResult<T>` as the universal return type.

## 7. Existing Code to Reuse
- `SafeDatabaseHelper.withTransaction(...)`
- `SyncQueueDao` / `SyncQueueEntity` / `SyncHandler`
- `NoorResult<T>` / `Outcome<T, AppError>`
- **Resolved:** `core-auth/SessionActivationRepository` — `activate(childId): Result<ChildSession>`, `currentSession: StateFlow<ChildSession?>` (confirmed via `C19_Parent_PIN_Biometric_Gate/KMP/05-session-activation-cross-profile-state-clearing.md` §8) — this is the accessor `toggle()`/`getFavorites()` must read `child_id` from internally, satisfying §17's structural-authorization requirement

## 8. Files to Create
- `FavoritesRepository.kt` (interface + implementation)
- `FavoriteLocalDataSource.kt` (local cache read/write)
- `FavoriteRemoteDataSource.kt` (thin wrapper over B-01/B-02 network calls)
- `FavoriteEntity.kt` (local persistence model)
- Unit/integration tests: `FavoritesRepositoryTest.kt`

## 9. Files to Modify
None outside this module — this is a new, additive data layer.

## 10. Backend Requirements
Consumes B-01 (`POST /v1/favorites`) and B-02 (`GET /v1/children/{id}/favorites?type=`).

## 11. KMP Requirements
- `toggle(contentId, contentType, favorited, clientRequestId)` — always resolves `child_id` internally from the active session; the method signature must make it structurally impossible to pass an external `child_id`.
- `getFavorites(type)` — same internal-session-derivation guarantee.
- Initial local load from cache (offline-first read).
- Remote refresh merges into local cache on successful fetch.
- Fully offline read served from cache.
- Offline toggle queued into `SyncQueueDao` (`PENDING`), auto-flushed via `SyncHandler` on reconnect.
- On sync confirmation, reconcile local optimistic state with server-confirmed state; on rejection, roll back and surface via `NoorResult` error to K-01's ViewModel.
- Cache invalidated on any confirmed toggle for the active child, and on child-session switch (coordinates with K-04).

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
Wraps B-01/B-02 exactly as specified in their respective blueprints — no additional fields invented at this layer.

## 14. Database Requirements
Local: `FavoriteEntity` (via `core-data`'s existing local DB) + `SyncQueueEntity` rows for pending toggles. **Resolved naming convention:** `CORE_DATABASE_INSTRUCTIONS.md` documents a consistent `*Entity` suffix (`ChildProfileEntity`, `HabitEntity`, `SyncQueueEntity`, `DownloadEntity`), package `com.noorheroes.core.database.entity`, with the table name matching the class name lowercase-first (e.g. `tableName = "childProfileEntity"`) — no `*_cache` suffix convention exists. This entity should be `FavoriteEntity` with `tableName = "favoriteEntity"`, consistent with every other local entity in the codebase.

## 15. Validation
`contentType` restricted to the same allowlist as the backend (`story|surah|dua`) at the repository boundary, failing fast locally before a wasted network round trip.

## 16. Authentication
Delegates entirely to the existing network layer's bearer-token attachment (`core-network`); no auth logic duplicated here.

## 17. Authorization
**Structural guarantee (signature requirement for this sub-feature):** no method on `FavoritesRepository` accepts a `child_id` parameter from any caller — it is always derived internally from the active session. Enforced by interface design, verified by a dedicated test/code-review convention (PRD §7 item 4).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Network failure on toggle | Queued to `SyncQueue`, `NoorResult.Success` returned optimistically to the UI layer |
| Network failure on list fetch | Cached data returned via `NoorResult.Success` with a staleness flag; never a hard failure if cache exists |
| Server rejects toggle (inaccessible content) | `SyncHandler` rollback triggers; K-01 rolls back its optimistic UI state |
| No cache and no network | `NoorResult.Failure` with an appropriate `AppError`, surfaced by K-02 as an error/offline state |

## 19. Offline First
This entire sub-feature exists to implement offline-first behavior per PRD §1.8/§1.14 and Edge Case 5 — read always prefers cache-then-network; writes always queue when offline.

## 20. Local Data
`FavoriteEntity` cache rows + `SyncQueueEntity` outbox rows, both scoped implicitly to the active child session (never storing a foreign child's data in the same unscoped table without a `child_id` partition key — coordinate with K-04 on cache-key design).

## 21. Localization
N/A at this layer (no user-facing strings).

## 22. RTL
N/A at this layer.

## 23. Analytics
None fired directly by the repository — analytics remain owned by K-01 (toggle events) and K-02 (screen/view events), keeping this layer analytics-agnostic.

## 24. Performance
Cache-first reads avoid network latency on repeat views; `SyncQueue` batches/auto-flushes rather than firing one request per micro-interaction; avoid loading the entire favorites list into memory unbounded — support paged/lazy local queries consistent with K-02's pagination needs (Edge Case 4).

## 25. Security
No `child_id` ever accepted as an external parameter (see §17) — this is the repository's core security property, directly supporting FR-4.

## 26. Library Requirements
`core-data`, `core-network`, `core-common` (existing, no new library).

## 27. Testing
- Unit: `toggle()`/`getFavorites()` cannot be called with an external `child_id` (structural/compile-time or runtime-enforced test).
- Unit: cache-first read returns cached data before any network call resolves.
- Integration: offline-toggle → reconnect → sync → cache-reconciliation, full end-to-end (PRD §6.10).
- Integration: server-rejected toggle triggers rollback through to the repository's exposed state.

## 28. Documentation
Repository interface KDoc explicitly stating the no-external-child_id contract as a hard invariant for future maintainers.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Wire Active-Session Accessor.** Confirmed as `core-auth/SessionActivationRepository.currentSession` (`StateFlow<ChildSession?>`) — read `child_id` from this, not from any caller-supplied parameter.
**Task 02 — Define `FavoritesRepository` Interface.** `toggle()`, `getFavorites(type)`, no `child_id` parameter.
**Task 03 — Implement `FavoriteLocalDataSource`.** Cache read/write via `SafeDatabaseHelper.withTransaction`.
**Task 04 — Implement `FavoriteRemoteDataSource`.** Thin wrapper over B-01/B-02 endpoints.
**Task 05 — Implement Repository Logic.** Cache-first read, remote refresh, offline queueing via `SyncQueueDao`.
**Task 06 — Wire `SyncHandler` Rollback.** On server rejection, propagate rollback to consumers via `NoorResult`.
**Task 07 — Implement Cache Invalidation.** On confirmed toggle and on session switch (coordinate with K-04).
**Task 08 — Write Tests.** Per §27, with the no-external-`child_id` test treated as highest priority.
**Task 09 — Final Code Review.** Confirm K-01/K-02 consume only this repository, never call the network layer directly.

## 30. Definition of Done
No-external-`child_id` test green; offline-toggle-reconnect-sync integration test green; cache-first read verified; rollback-on-rejection verified end-to-end with K-01.

## 31. Final Verification Checklist
- [ ] `child_id` never accepted as an external parameter on any repository method
- [ ] Cache-first read implemented and tested
- [ ] Offline queueing via `SyncQueue` implemented and tested
- [ ] Rollback-on-rejection propagates correctly to K-01
- [ ] Cache invalidation wired for both toggle-confirmation and session-switch (K-04)
- [ ] No direct network calls from K-01/K-02 — repository is the sole data-access boundary
