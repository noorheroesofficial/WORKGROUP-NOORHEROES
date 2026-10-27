# K-07 — Home Offline Cache, First-Day Empty State & Deep Linking

## 1. Feature Context
NoorHeroes Child App (KMP). Implements the `HomeRepository` concrete cache-or-network strategy that K-01's interface depends on, the First-Day guided empty state, and Home's deep-link entry point.

## 2. Parent Feature
A.2 — Child Home Dashboard & AI Personalization

## 3. Sub-feature
2.7 Home Offline Cache, First-Day Empty State & Deep Linking (ID: K-07)

## 4. Objective
Implement `HomeLocalCache` (Room) persisting the last successful `/v1/home` payload per `child_id`, cache-first cold-start rendering with a persistent non-alarming offline badge, strict per-`child_id` cache isolation on profile switch, the First-Day guided empty-state branching, causal-order offline habit-check-in reconciliation on reconnect, and the `noorheroes://home/section/{section_id}` deep link.

## 5. Business Requirements
Per PRD FR-15, FR-16, Edge Case 7, Edge Case 10, §6.7, §6.8, §7 items 4, 6, 7:
- Full cached-Home rendering with persistent, non-alarming offline indicator; never a blank/error screen if a cache exists.
- Cache strictly keyed per `child_id`, cleared/isolated on profile switch (zero cross-child leakage).
- First-Day empty state: replaces Continue Learning/Weekly Challenge/Milestones with a single "Start My First Mission" CTA, state-driven conditional render (not a separate screen/Activity).
- True first-launch offline (no cache, no network): friendly retry screen, never a raw technical error.
- Deep link scrolls to the matching section without re-triggering a full data reload if the screen is already in memory.
- Reconcile locally-queued offline habit check-ins in causal order before showing "live" data, avoiding a visible streak regression flash (shared responsibility with K-03; this sub-feature owns the reconciliation-before-render sequencing at the Home level).

## 6. Existing Architecture
Follow `CORE_DATABASE_INSTRUCTIONS.md` (Room) and `CORE_DATASTORE_INSTRUCTIONS.md`/`CORE_DATA_INSTRUCTIONS.md` for cache-first repository patterns and `CORE_NAVIGATION_INSTRUCTIONS.md` for deep-link handling.

## 7. Existing Code to Reuse
K-01's `HomeUiState`/`HomeRepository` interface; K-03's outbox/sync worker (this sub-feature sequences reconciliation relative to Home's cache-then-refresh flow, without duplicating K-03's sync logic).

## 8. Files to Create
- `feature/home/src/androidMain/kotlin/.../data/local/HomeLocalCacheDao.kt` (Room)
- `feature/home/src/commonMain/kotlin/.../data/HomeRepositoryImpl.kt`
- `feature/home/src/commonMain/kotlin/.../components/FirstDayEmptyState.kt`
- `feature/home/src/commonMain/kotlin/.../components/FullScreenRetry.kt`
- `feature/home/src/commonMain/kotlin/.../navigation/HomeDeepLinkHandler.kt`
- `feature/home/src/androidInstrumentedTest/.../HomeCacheIsolationTest.kt`
- `feature/home/src/androidUnitTest/.../HomeRepositoryCacheFirstTest.kt`

## 9. Files to Modify
- `HomeViewModel.kt`, `HomeUiState.kt`, `HomeScreen.kt` (K-01) — wire real `HomeRepositoryImpl`, first-day branching, offline badge
- Navigation graph — register `noorheroes://home/section/{section_id}` deep link
- Profile-switch flow (existing, from A.1/Profile Picker) — hook cache-clear-on-switch

## 10. Backend Requirements
Consumes `GET /v1/home` (B-01), including `is_first_day` flag.

## 11. KMP Requirements
- `HomeLocalCacheDao` stores the last successful full `/v1/home` response payload (serialized) per `child_id`.
- `HomeRepositoryImpl.getHome()`: on cold start, read cache immediately for instant render, then attempt a background network refresh; on refresh success, update cache and `HomeUiState`; on refresh failure, keep showing cached data with an offline badge.
- Cache read/write strictly scoped by `child_id`; on profile switch, clear (or simply never read) another child's cache entry — verified via an explicit isolation test (Multiple siblings sharing a device, per Edge Case 7).
- `is_first_day == true` → `HomeUiState` carries a flag that `HomeScreen` (K-01) uses to swap Continue Learning/Weekly Challenge/Milestones for a single `FirstDayEmptyState` CTA Composable.
- True cold-start-offline-no-cache → render `FullScreenRetry` (friendly copy, retry control), never a raw error.
- Deep link handler resolves `section_id`, and if `HomeScreen` is already composed/in memory, scrolls to it via `bringIntoViewRequester` without a full data reload; if not in memory, launches Home normally then scrolls once loaded.
- Reconciliation sequencing: on reconnect, wait for K-03's outbox sync to complete (or timeout) before treating the next `HomeUiState` refresh as "live," to avoid a visible streak regression flash.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
`GET /v1/home` (B-01 §13), consumed with `If-None-Match` ETag support for efficient background refresh.

## 14. Database Requirements (Local)
Room table `home_cache(child_id PK, payload_json, cached_at)`. One row per child; overwritten on each successful refresh; never merged/joined across children.

## 15. Validation
Deserialized cache payload validated against the same `HomeUiState`-mapping logic as a fresh network response, so a stale/malformed cache entry degrades gracefully (e.g., falls through to `FullScreenRetry` if truly corrupt) rather than crashing.

## 16. Authentication
Reuses shared network-layer Bearer token attachment for the background refresh call.

## 17. Authorization
N/A directly; cache isolation by `child_id` is the relevant access-control concern here (§7 Multi-Child Isolation).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Cache exists, network fails | Render cached data + offline badge, never blank/error |
| No cache, no network (true first launch offline) | `FullScreenRetry` with retry control |
| No cache, network succeeds | Normal render |
| Corrupt/unparseable cache entry | Treated as no-cache; fall through to network or `FullScreenRetry` |

## 19. Offline First
This sub-feature is the primary implementation of Home's offline-first contract:
```
Remote Data (GET /v1/home)
   ↓
HomeRepositoryImpl (cache-first read, background refresh)
   ↓
HomeLocalCache (Room, keyed by child_id)
   ↓
HomeUiState → HomeScreen
```
Scenarios: initial local load, remote refresh, offline read, retry, sync (habit outbox via K-03), cache invalidation (on refresh success), network recovery (reconciliation sequencing).

## 20. Local Data
Room `home_cache` table as above; strictly per-`child_id`, cleared/ignored on profile switch.

## 21. Localization
Cached payload retains whatever localization was baked into the response at cache time; if the child's language changes, the next successful network refresh supersedes the stale-language cache (acceptable per existing platform convention — flag if a more aggressive cache-invalidation-on-language-change behavior is required elsewhere in the app).

## 22. RTL
`FirstDayEmptyState` and `FullScreenRetry` Composables follow the same RTL mirroring rules as the rest of Home.

## 23. Analytics
`home_offline_state_shown`, `home_first_day_empty_state_shown`, `home_first_mission_started_from_empty_state`.

## 24. Performance
Cache read must be fast enough to support "instant" cold-start render (target: perceptible render well under the p95 cold-load budget from B-01, since this is a local disk read, not a network call). Background refresh must not block the already-rendered cached UI.

## 25. Security
Cache isolation per `child_id` is the primary security-adjacent concern (prevents a sibling profile switch from momentarily showing stale data belonging to another child) — verify via the explicit isolation test, not just by code review.

## 26. Library Requirements
Room, Kotlin Coroutines/Flow, existing navigation/deep-link library, kotlinx.serialization (or existing serialization library) for cache payload storage.

## 27. Testing
- Unit: cache-first read returns cached data immediately, then updates after background refresh.
- Integration: cache-isolation test — switch between two child profiles on the same device, assert no fragment of child A's cached data ever renders for child B, even momentarily.
- Compose UI: `FirstDayEmptyState` renders correctly when `is_first_day=true`, replacing exactly the three specified sections.
- Compose UI: `FullScreenRetry` renders on true cold-start-offline (no cache, no network).
- Integration: deep link to an already-in-memory `HomeScreen` scrolls without a full reload; deep link to a cold-started Home launches then scrolls once loaded.
- Integration: reconnect sequencing — outbox sync (K-03) completes before the next "live" Home render, no visible streak regression flash.

## 28. Documentation
Module documentation describing the full offline-first data flow diagram (§19) and the explicit multi-child cache-isolation guarantee, since this is a repeatedly-tested trust property across the codebase (referenced by other multi-child features).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement `HomeLocalCacheDao` (Room)**
- Objective: Per-child cache table.
- Why Required: Foundation for cache-first rendering.
- Existing Architecture to Follow: `CORE_DATABASE_INSTRUCTIONS.md`.
- Existing Files to Reuse: Existing Room database module.
- Files to Create: `data/local/HomeLocalCacheDao.kt`, entity class
- Files to Modify: Room database module (register)
- Implementation Details: `child_id` primary key; `payload_json` (serialized `HomeUiState`-mappable DTO); `cached_at` timestamp.
- Business Rules: One row per child; overwritten, not appended.
- Validation: N/A.
- Error Handling: N/A.
- Security: Isolation by primary key.
- Performance: Single-row lookups by primary key.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: DAO unit tests.
- Documentation: KDoc.
- Dependencies: None.
- Do Not Change: N/A.
- Expected Result: Cache table live.
- Definition of Done: DAO tests pass.

**Task 02 — Implement `HomeRepositoryImpl` (Cache-First + Background Refresh)**
- Objective: Concrete repository implementing K-01's `HomeRepository` interface.
- Why Required: Core offline-first logic.
- Existing Architecture to Follow: Repository pattern from `CORE_DATA_INSTRUCTIONS.md`.
- Existing Files to Reuse: Task 01 DAO, K-01's `HomeRepository` interface, network client.
- Files to Create: `data/HomeRepositoryImpl.kt`
- Files to Modify: DI registration binding interface to implementation
- Implementation Details: `getHome(childId): Flow<HomeUiState>` emits cached value first (if present), then network result on completion, updating cache on success; on network failure, emits the cached value tagged with an offline flag (no additional emission needed if already showing cache).
- Business Rules: Never regress to a blank state if a cache entry exists.
- Validation: Corrupt cache handled per §18 table.
- Error Handling: Per §18.
- Security: `childId`-scoped reads/writes exclusively.
- Performance: Cache read is synchronous-fast (local disk), network is async.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Unit tests for cache-first emission order; corrupt-cache fallback.
- Documentation: KDoc.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Working repository.
- Definition of Done: Tests pass.

**Task 03 — Implement Cache Isolation on Profile Switch**
- Objective: Guarantee zero cross-child cache leakage.
- Why Required: Edge Case 7 (multi-child device sharing).
- Existing Architecture to Follow: Existing profile-switch flow from A.1/Profile Picker.
- Existing Files to Reuse: Task 01/02, existing profile-switch navigation hook.
- Files to Create: none (wiring into existing profile-switch flow)
- Files to Modify: Profile-switch flow entry point — ensure `HomeViewModel`/`HomeRepositoryImpl` is re-scoped or explicitly re-queried with the new `child_id` on switch, never reusing an in-memory state from the prior child.
- Implementation Details: On profile switch, `HomeViewModel` instance is recreated or explicitly reset (per existing DI/ViewModel-scoping convention for per-profile state), and any in-flight cache read/write for the prior child is not allowed to write into the new child's render.
- Business Rules: Zero cross-child leakage, verified explicitly.
- Validation: N/A.
- Error Handling: N/A.
- Security: This IS the security-adjacent control for this task.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Integration test switching rapidly between two profiles, asserting no fragment of profile A ever renders under profile B's session, including during in-flight async operations.
- Documentation: KDoc on the isolation guarantee.
- Dependencies: Task 02.
- Do Not Change: N/A.
- Expected Result: Verified isolation.
- Definition of Done: Rapid-switch integration test passes with zero leakage.

**Task 04 — Build `FirstDayEmptyState` and `FullScreenRetry` Composables**
- Objective: UI for first-day and true-offline-cold-start states.
- Why Required: FR-15, Edge Case scenario for true offline first launch.
- Existing Architecture to Follow: `:core:design-system` tokens.
- Existing Files to Reuse: none.
- Files to Create: `components/FirstDayEmptyState.kt`, `components/FullScreenRetry.kt`
- Files to Modify: `HomeScreen.kt` (branch on `isFirstDay`/no-cache-no-network state)
- Implementation Details: `FirstDayEmptyState` replaces exactly the three specified sections (Continue Learning, Weekly Challenge, Milestones) with a single centered "Start My First Mission" CTA — implemented as a state-driven conditional render within `HomeScreen`, not a separate Activity/screen; `FullScreenRetry` shown only when both cache and network are unavailable.
- Business Rules: State-driven, not a separate navigation destination.
- Validation: N/A.
- Error Handling: `FullScreenRetry` includes a retry control that re-triggers `HomeViewModel.refresh()`.
- Security: N/A.
- Performance: N/A.
- Localization: String resources.
- RTL: Verified.
- Analytics: `home_first_day_empty_state_shown`, `home_first_mission_started_from_empty_state`, `home_offline_state_shown`.
- Tests: Compose UI tests for both states.
- Documentation: KDoc.
- Dependencies: Task 02.
- Do Not Change: N/A.
- Expected Result: Working states.
- Definition of Done: Compose UI tests pass.

**Task 05 — Implement Deep Link Handler**
- Objective: `noorheroes://home/section/{section_id}` navigation.
- Why Required: PRD §6.8, §7 item 6.
- Existing Architecture to Follow: `CORE_NAVIGATION_INSTRUCTIONS.md` deep-link registration pattern.
- Existing Files to Reuse: Existing deep-link dispatcher (from A.1/notification-routing infrastructure) if present.
- Files to Create: `navigation/HomeDeepLinkHandler.kt`
- Files to Modify: Navigation graph
- Implementation Details: On deep-link receipt, check if `HomeScreen` is already composed (via existing navigation back-stack/state check); if so, invoke `bringIntoViewRequester` to scroll without reloading; if not, navigate to Home normally, then scroll once the target section resolves to `Content`.
- Business Rules: No full reload if already in memory.
- Validation: N/A.
- Error Handling: Unknown `section_id` falls back to plain Home launch (no crash).
- Security: N/A.
- Performance: Avoids redundant network calls when already in memory.
- Localization: N/A.
- RTL: Scroll-to behavior verified in RTL layout.
- Analytics: N/A specified beyond existing deep-link analytics conventions.
- Tests: Integration tests for both in-memory and cold-start deep-link paths.
- Documentation: KDoc.
- Dependencies: Task 02, K-01 Task 03.
- Do Not Change: N/A.
- Expected Result: Working deep link.
- Definition of Done: Both integration test paths pass.

**Task 06 — Sequence Offline Habit Reconciliation Before Live Render**
- Objective: Avoid visible streak regression flash on reconnect.
- Why Required: Edge Case 10.
- Existing Architecture to Follow: Coordinates with K-03's `HabitCheckinSyncWorker`.
- Existing Files to Reuse: K-03's sync worker/outbox.
- Files to Create: none (sequencing logic added to `HomeRepositoryImpl`/`HomeViewModel`)
- Files to Modify: `data/HomeRepositoryImpl.kt`, `HomeViewModel.kt`
- Implementation Details: On network-recovery trigger, await (with a bounded timeout) K-03's pending outbox sync completion signal before treating the subsequent Home refresh as authoritative/"live" — if the timeout elapses, proceed anyway rather than blocking indefinitely.
- Business Rules: Bounded wait, never indefinite blocking.
- Validation: N/A.
- Error Handling: Timeout fallback proceeds without blocking the user.
- Security: N/A.
- Performance: Bounded timeout prevents UI freeze.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Integration test simulating queued offline check-ins + reconnect, asserting the streak value shown never visibly regresses then jumps back up.
- Documentation: KDoc explaining the bounded-wait rationale.
- Dependencies: Task 02; K-03's sync worker.
- Do Not Change: N/A.
- Expected Result: No visible regression flash.
- Definition of Done: Integration test passes.

## 30. Definition of Done
Home renders instantly from cache on cold start, never blank when a cache exists, strictly isolates cache per child, correctly branches to First-Day/FullScreenRetry states, supports in-memory-aware deep linking, and sequences offline reconciliation to avoid visual regressions; all tests green.

## 31. Final Verification Checklist
- [ ] Cold start with cache renders instantly, background-refreshes silently
- [ ] Cold start with no cache and no network shows `FullScreenRetry`, never a raw error
- [ ] Cache strictly isolated per `child_id`, verified via rapid profile-switch test
- [ ] First-Day empty state replaces exactly the three specified sections, state-driven not a separate screen
- [ ] Deep link to an in-memory Home scrolls without reload; cold-start deep link launches then scrolls
- [ ] Offline habit reconciliation sequenced before "live" render, no visible streak regression flash, bounded timeout respected
- [ ] All tests pass
