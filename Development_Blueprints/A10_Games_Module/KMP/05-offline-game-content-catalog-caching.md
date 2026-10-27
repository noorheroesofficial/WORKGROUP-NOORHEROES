# K-05 — Offline Game Content & Catalog Caching

## 1. Feature Context
Part of **A.10 Games Module**. Covers offline-first support: local catalog caching for the Games Hub, downloadable game content, and idempotent outbox-based sync of evidence/reward submissions made while offline (PRD §6.7, Edge Case 8).

## 2. Parent Feature
A.10 Games Module — KMP App (Android/iOS)

## 3. Sub-feature
**2.5 Offline Game Content & Catalog Caching** `[K-05]`

## 4. Objective
Complete `GamesRepositoryImpl`'s offline-first data flow (remote → repository → local storage → UI), enabling full offline gameplay for downloaded games and reliable, idempotent sync of queued evidence/reward submissions on reconnect (PRD §6.7: "requiring no new offline infrastructure" — reuse the existing outbox pattern rather than building a parallel one).

## 5. Business Requirements
- Edge Case 8: downloaded/cached games fully playable offline; evidence/reward events queue for sync on reconnect, idempotently.
- §1.14 Offline States: downloaded games playable offline; non-downloaded games show a clear "connect to internet or download" affordance, not a dead tile.
- §1.11 Error Handling: Games Hub catalog fetch failure renders cached last-known catalog with a subtle "may be outdated" indicator.
- §6.7: downloadable content follows A.5's existing offline-manifest pattern; session completion while offline queues via the shared outbox pattern already established in A.8/A.9.

## 6. Existing Architecture
Builds on `core-data`'s documented `SyncQueue`/`SyncQueueImpl` (`CORE_DATA_INSTRUCTIONS.md` §3) for outbound operation reliability, and the general "Offline-First Screen" scenario pattern (§8: observe via repository `Flow`, call `refresh()` to trigger network fetch + DB update, UI reacts automatically). Local persistence uses the project's `core-database` layer (Room/SQLDelight — exact technology confirmed against `CORE_DATABASE_INSTRUCTIONS.md`, not fully reviewed in this blueprint pass; implementation must follow whatever DAO/schema conventions that document specifies rather than inventing a new local-storage pattern).

## 7. Existing Code to Reuse
- `SyncQueue.enqueue()` (`core-data/sync`) — reused for queuing the K-03 completion call when offline, exactly as other write-path repositories do (e.g., `HabitsRewardsRepository.checkInHabit()`).
- `ConnectivityObserver` (referenced in `CORE_DATA_INSTRUCTIONS.md` §9 Do/Don't — "Access platform APIs directly... Always go through an abstraction like `ConnectivityObserver`") — used to trigger auto-flush on reconnect.
- A.5's existing offline-manifest/download pattern for domain-specific game content (reused, not reimplemented, per PRD §6.7).
- `ContentRepository`'s `Flow<List<Content>>` pattern (`CORE_DATA_INSTRUCTIONS.md` §10 Quick Reference) as the structural precedent for `GamesRepository.observeCatalog()`'s local-cache-backed implementation.

## 8. Files to Create
```
core/database/src/commonMain/kotlin/com/noorheroes/core/database/dao/GameCatalogDao.kt
core/database/src/commonMain/kotlin/com/noorheroes/core/database/entity/GameCatalogEntity.kt
core/data/src/commonMain/kotlin/com/noorheroes/core/data/sync/handlers/GameSessionCompletionSyncHandler.kt
feature/games/src/commonTest/kotlin/com/noorheroes/feature/games/offline/OfflineGamesCatalogTest.kt
feature/games/src/commonTest/kotlin/com/noorheroes/feature/games/offline/OfflineSessionSyncTest.kt
```

## 9. Files to Modify
```
core/data/src/commonMain/kotlin/com/noorheroes/core/data/repository/GamesRepositoryImpl.kt  # add local-cache-backed observeCatalog(), refresh(), offline manifest resolution
core/data/src/commonMain/kotlin/com/noorheroes/core/data/di/RepositoryModule.kt              # register GameCatalogDao, sync handler
```
**Do Not Change:** `SyncQueueImpl`'s core dispatch logic — register a new handler type, don't modify the queue's internals; A.5's offline-manifest/download internals — call its existing public interface.

## 10. Backend Requirements
None implemented here; relies on B-01's cache-invalidation-aware catalog endpoint and B-03's idempotent (`client_request_id`-keyed) completion endpoint, both already designed for safe offline replay.

## 11. KMP Requirements
- `GamesRepositoryImpl.observeCatalog()`: emits from local `GameCatalogDao` `Flow` immediately (cache-first), then triggers a background `refresh()` that fetches `GET /v1/games` and updates the local DB, which the `Flow` automatically re-emits (per §8 "Offline-First Screen" scenario pattern).
- `refresh()` failure (no connectivity) leaves the last-cached data in place; UI (K-01) surfaces the "may be outdated" indicator based on a `lastSyncedAt` timestamp field on the cached entity, not a hard error.
- Downloaded game content (for offline manifest resolution) follows A.5's existing download-manifest pattern — `GamesRepositoryImpl.getManifest()` (K-02) checks local download status first before attempting a network call when offline.
- `GameSessionCompletionSyncHandler` implements the `SyncOperationDispatcher`'s handler contract (per `core-data/sync/handlers` package structure) for the `client_request_id`-keyed completion call, ensuring idempotent replay on reconnect.
- Non-downloaded games while offline show the "connect to internet or download" affordance (§1.14) rather than a dead/unresponsive tile — this is a UI-layer concern wired here at the repository-state level (`GameManifest` resolution returns a distinct `NotAvailableOffline` outcome rather than a generic error).

## 12. NextJS Requirements
N/A.

## 13. API Contract
No new contract; this blueprint completes the **client-side implementation** of consuming B-01 (`GET /v1/games`) and B-03 (`POST .../complete`) in an offline-resilient way — both already designed (cache-friendly TTL/invalidation; idempotent `client_request_id`) to support this.

## 14. Database Requirements
Local (client-side) schema, per `core-database` conventions (exact DAO framework confirmed against `CORE_DATABASE_INSTRUCTIONS.md`):
```
GameCatalogEntity(
    gameId: String (PK),
    title: String,
    skillArea: String,
    skillNodeIds: List<String>,
    thumbnailUrl: String,
    ageBandTier: String,
    isDailyQuizEntry: Boolean,
    lastSyncedAt: Instant
)
```
Downloaded-game-content storage reuses A.5's existing local schema — no new table for content itself, only the catalog metadata above is new to this module.

## 15. Validation
`lastSyncedAt` staleness threshold (beyond which the "may be outdated" indicator shows) should follow the same convention as other cached-catalog surfaces in the app (e.g., A.5's content catalog) — confirm the exact threshold value against existing precedent rather than inventing a new one; do not hardcode an arbitrary number without cross-checking.

## 16. Authentication
Relies on existing child-session-scoped network client for the underlying `refresh()` network call; local cache reads require no additional auth (already scoped to the active child profile via existing local-DB child-scoping conventions).

## 17. Authorization
N/A beyond what B-01 already enforces server-side; cached data reflects whatever the server was willing to return for this child at last sync — never expanded or re-filtered locally.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| `refresh()` fails, no local cache exists yet (first launch offline) | Empty/offline state shown, not a crash — distinct from "stale cache" case |
| `refresh()` fails, stale cache exists | Stale cache rendered with "may be outdated" indicator |
| Offline session-completion queued, `SyncQueue` flush fails repeatedly | Standard `SyncQueue` retry/backoff (existing infrastructure, not reimplemented); if permanently failed, `SyncHandler` rollback notification triggers (per `CORE_DATA_INSTRUCTIONS.md` §3 "Internal Behavior" — reused as-is) |
| Manifest requested offline for a non-downloaded game | `NotAvailableOffline` outcome → UI shows download/connect affordance, not an error |

## 19. Offline First
```
Remote: GET /v1/games (B-01)
   ↓
GamesRepositoryImpl.refresh()
   ↓
GameCatalogDao (local Room/SQLDelight table)
   ↓
GamesRepositoryImpl.observeCatalog(): Flow<List<GameCatalogItem>>
   ↓
GamesHubViewModel (K-01) — cache-first emission, background refresh
```
```
Offline action: session completion (K-03)
   ↓
SyncQueue.enqueue(GameSessionCompletionOperation(clientRequestId, ...))
   ↓ (persisted to core-database immediately)
ConnectivityObserver reports online
   ↓
Auto-flush: GameSessionCompletionSyncHandler executes POST .../complete (B-03)
   ↓ (idempotent via client_request_id, safe even if the exact same call was partially attempted pre-offline)
Success → local session marked synced; Failure → SyncHandler rollback path
```

## 20. Local Data
`GameCatalogEntity` (§14) is the only new local table; downloaded game content itself continues to live under A.5's existing local storage schema (reused, not duplicated).

## 21. Localization
Cached `title` strings reflect whatever locale was active at last sync; a locale change while offline will show stale-locale text until the next successful `refresh()` — this is an accepted, documented limitation consistent with how other cached catalogs behave in this app (confirm against A.5's existing precedent).

## 22. RTL
N/A directly (data layer); rendering is K-01's concern.

## 23. Analytics
`games_offline_download_prompted`, `games_offline_download_completed` (PRD §1.19) — fired by the UI layer (K-01/K-02) when the offline/download affordance is shown/actioned, informed by this module's `NotAvailableOffline` signal.

## 24. Performance
- Cache-first emission ensures instant Games Hub render even on cold start with connectivity (perceived performance improvement beyond the raw 600ms network target).
- Background `refresh()` does not block the UI thread; runs via `DispatcherProvider`-injected IO dispatcher.
- Local DB queries indexed on `skillArea` for filtered-view performance parity with the server-side index (B-01 §14).

## 25. Security
No new sensitive data stored locally (catalog metadata only, no PII); downloaded content storage reuses A.5's existing security posture for cached learning content.

## 26. Library Requirements
Room or SQLDelight (per `core-database`'s existing choice — confirm and reuse exactly, do not introduce a second local-DB technology), Kotlinx Coroutines/Flow. No new dependencies beyond what `core-database`/`core-data` already provide.

## 27. Testing
- Unit: `observeCatalog()` emits cached data immediately, then updated data after a successful `refresh()`.
- Unit: `refresh()` failure with existing cache leaves cache intact, flags staleness.
- Unit: `refresh()` failure with no cache shows empty/offline state, not a crash.
- Integration: full offline session-completion → `SyncQueue` persistence → simulated reconnect → idempotent replay → success confirmed via B-03 mock.
- Integration: `SyncQueue` permanent-failure path triggers rollback notification correctly (mirrors existing `SyncQueue` behavior, verified for this specific operation type).
- Integration: manifest request offline for a non-downloaded game returns `NotAvailableOffline`, not a generic error.

## 28. Documentation
Document the staleness-threshold value and its cross-reference source (A.5's existing precedent) explicitly in code comments, to prevent future arbitrary changes without understanding the shared convention.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Local Schema**
- Objective: `GameCatalogEntity` + `GameCatalogDao` per §14, following `core-database`'s existing DAO conventions exactly.
- Definition of Done: schema reviewed against `CORE_DATABASE_INSTRUCTIONS.md` for consistency (confirm ORM/framework choice before implementing).

**Task 02 — Implement Cache-First observeCatalog()**
- Objective: `GamesRepositoryImpl.observeCatalog()` emits from `GameCatalogDao.observeAll()` `Flow`, triggers background `refresh()`.
- Existing Files to Reuse: `ContentRepository`'s `Flow<List<Content>>` pattern as structural precedent.
- Definition of Done: cache-first emission verified via test (data appears before network call resolves).

**Task 03 — Implement refresh() with Staleness Handling**
- Objective: Network fetch → DB upsert → `lastSyncedAt` update; failure paths per §18.
- Definition of Done: both "stale cache exists" and "no cache exists" failure paths tested distinctly.

**Task 04 — Implement Offline Manifest Resolution**
- Objective: `getManifest()` (extending K-02's method) checks local download status before attempting network when offline; returns `NotAvailableOffline` for non-downloaded games.
- Existing Files to Reuse: A.5's existing download-manifest pattern.
- Definition of Done: offline non-downloaded-game test confirms correct outcome type (not a generic error).

**Task 05 — Implement GameSessionCompletionSyncHandler**
- Objective: Register a new `SyncOperationDispatcher` handler for `GameSessionCompletionOperation`, reusing `SyncQueue.enqueue()`/existing retry-backoff/rollback infrastructure.
- Existing Files to Reuse: `HabitsRewardsRepository.checkInHabit()`'s sync-queue integration as structural precedent.
- Definition of Done: idempotent-replay integration test (Task 08) passes.

**Task 06 — Wire ConnectivityObserver Auto-Flush**
- Objective: Confirm existing auto-flush-on-reconnect behavior correctly picks up queued `GameSessionCompletionOperation`s without any Games-specific polling logic.
- Definition of Done: reconnect-triggers-flush test passes using the existing `ConnectivityObserver` abstraction.

**Task 07 — Register DI Bindings**
- Objective: Wire `GameCatalogDao`, `GameSessionCompletionSyncHandler` into `RepositoryModule.kt`.

**Task 08 — Add Offline Sync Integration Test**
- Objective: `OfflineSessionSyncTest.kt` — full offline-completion → reconnect → idempotent-replay round trip.
- Definition of Done: test confirms no duplicate reward/evidence submission occurs even if the sync operation is retried multiple times.

**Task 09 — Add Catalog Caching Tests**
- Objective: `OfflineGamesCatalogTest.kt` per §27.

**Task 10 — Add Documentation**
- Objective: Staleness-threshold rationale documented; local-schema choice documented.

**Task 11 — Final Code Review**
- Objective: Confirm no parallel/duplicate offline infrastructure was introduced (reuse of existing `SyncQueue`/`ConnectivityObserver` confirmed structurally, not just functionally).
- Definition of Done: review checklist (§31) fully checked.

## 30. Definition of Done
- Games Hub renders instantly from cache on cold start, updates in background.
- Stale-cache and no-cache offline states both handled distinctly and gracefully.
- Offline session completions queue and replay idempotently on reconnect with zero duplicate submissions.
- Non-downloaded games offline show the correct affordance, not a dead tile or generic error.
- No new, parallel offline infrastructure introduced — existing `SyncQueue`/`ConnectivityObserver` reused throughout.

## 31. Final Verification Checklist
- [ ] Cache-first catalog emission verified (data visible before network resolves)
- [ ] Stale-cache vs. no-cache offline states both distinctly tested
- [ ] Offline session-completion queue-and-replay confirmed idempotent (no duplicate rewards)
- [ ] Non-downloaded-game-offline case returns `NotAvailableOffline`, not a generic error
- [ ] `SyncQueue`/`ConnectivityObserver` reused, not reimplemented
- [ ] Local schema reviewed against `core-database` conventions for consistency
- [ ] Staleness threshold cross-checked against existing app precedent (not invented)
- [ ] No files outside declared scope modified

---

## 32. Cross-Platform Dependencies
- Backend Dependency: B-01 (catalog refresh), B-03 (queued offline completions).
- KMP Dependency: K-01 (consumes the cached catalog), K-02 (offline manifest resolution), A.5's existing offline-manifest/download pattern (reused).
- Admin Dependency: None directly.
- Database Dependency: Room (`core-database`, confirmed — see §6 resolution) — new `GameCatalogEntity` table.
- External Service Dependency: `ConnectivityObserver` (existing `core-data` abstraction, reused).
- Figma Dependency: Offline/Download-Required Notice component (PRD Screen Inventory item 10).
