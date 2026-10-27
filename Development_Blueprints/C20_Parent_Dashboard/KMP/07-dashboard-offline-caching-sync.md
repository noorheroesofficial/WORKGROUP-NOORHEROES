# Blueprint: Dashboard Offline Caching & Sync

## 1. Feature Context
Platform: NoorHeroes KMP App. Module `:feature:parent-dashboard`, backed by `:core:offline-cache`/`:core:database` (Room) and `:core:network`.

## 2. Parent Feature
C.20 — Parent Dashboard.

## 3. Sub-feature
K-07 — Dashboard Offline Caching & Sync.

## 4. Objective
Implement the concrete `DashboardRepository` (interface defined in K-01) backed by Room caching, providing full offline rendering with a persistent "may be outdated" indicator, and cache-then-refresh behavior on reconnection.

## 5. Business Requirements
Source: PRD §1.14, §6.7, §7 (Android AI Code-Gen Prompt item 5), §1.18 row 10.
- Dashboard renders from last-cached data when offline, with clear "may be outdated" indicator.
- Module shortcuts requiring connectivity indicate this clearly on tap rather than navigating into a broken destination.
- Cache-then-refresh pattern consistent with platform's general approach.

## 6. Existing Architecture
Per `CORE_DATA_INSTRUCTIONS.md`: `core-data` orchestrates between `core-network` and `core-database`; `SyncQueue`/`SyncQueueImpl` handles outbound write reliability (not directly relevant here since Dashboard is read-mostly, per PRD §1.10 Edge Case #6: "this is a read-mostly screen, not a collaborative-editing surface"); `ConnectivityObserver` is the platform's abstraction for online/offline state (never poll platform APIs directly). Repository pattern: implement `DashboardRepositoryImpl : DashboardRepository`.

## 7. Existing Code to Reuse
- `ConnectivityObserver` (`core-data`/`core-common`) for online/offline state.
- `NoorResult<T>` / `Outcome` for all repository method returns.
- `DispatcherProvider` for `withContext(dispatchers.io)` main-safety.
- Room database setup pattern from `core-database` (per `CORE_DATABASE_INSTRUCTIONS.md` — not read in this pass; confirm exact DAO/table-creation conventions before implementation rather than inventing Room boilerplate inconsistent with existing patterns).
- "Furthest wins"/idempotency conventions are write-path concerns (per `CORE_DATA_INSTRUCTIONS.md` §9) — not directly applicable here since Dashboard has no local write path, but the general Room caching pattern from `PlaybackSyncRepository` or `ContentRepository`-style read-through caching is the closest existing analog to follow.

## 8. Files to Create
- `feature/parent-dashboard/src/commonMain/kotlin/.../local/DashboardCacheDao.kt` (or `core-database` if the platform convention centralizes all DAOs there — confirm before creating in the feature module)
- `feature/parent-dashboard/src/commonMain/kotlin/.../local/DashboardCacheEntity.kt`
- `feature/parent-dashboard/src/commonMain/kotlin/.../DashboardRepositoryImpl.kt`
- `feature/parent-dashboard/src/commonTest/kotlin/.../DashboardOfflineCachingTest.kt`

## 9. Files to Modify
- `di/ParentDashboardModule.kt` (from K-01) — bind `DashboardRepository` to `DashboardRepositoryImpl`

## 10. KMP Requirements
- `DashboardRepositoryImpl.getDashboard(childId)`: read-through cache — attempt network fetch via `:core:network`; on success, write to `DashboardCacheEntity` (Room) and return fresh data; on failure (network error) or when `ConnectivityObserver` reports offline, read from `DashboardCacheEntity` and return with a `stale: true` flag on the returned domain model.
- Same pattern for `getReport(type, childId)`.
- Cache entity stores the full serialized Dashboard/report payload keyed by `(childId, type?)` plus a `cachedAt: Instant` timestamp used to compute staleness against a TTL (coordinated with B-02's server-side cache TTL conceptually, but independently enforced client-side).
- Module shortcuts (K-06) that require connectivity (i.e., navigating into a module whose own data is not cached) must check `ConnectivityObserver` before navigating and show an inline "requires connection" indicator instead of navigating into a broken/blank destination screen (PRD §1.14).
- On reconnection (`ConnectivityObserver` transitions offline→online), trigger a background refresh of the currently-displayed child's Dashboard data, updating the `StateFlow` in place without a jarring full-screen reload.

## 11. Files/Screens
No new screens — implements the data layer consumed by K-01's ViewModel and surfaces the "may be outdated" indicator via K-01's `DashboardUiState` (`stale: Boolean` field, anticipated in K-01's blueprint).

## 12. NextJS Requirements
N/A.

## 13. API Contract
Consumes B-02 (`GET /v1/parent/dashboard`) and B-03 (`GET /v1/parent/dashboard/reports/{type}`) via `:core:network`; no new backend contract.

## 14. Database Requirements
New local Room table(s): `dashboard_cache(child_id, report_type_nullable, payload_json, cached_at)` — exact DDL/DAO conventions per `core-database`'s established patterns (confirm before finalizing column types/indices).

## 15. Validation
Cache reads must never silently serve data for a `childId` other than the one requested (family/child-scope integrity must be preserved in the cache key, mirroring the server-side family-ownership guarantee).

## 16. Authentication
N/A directly — this repository is only ever invoked from within `:feature:parent-dashboard`, which is itself gated by `:core:auth`'s Parent Gate (K-01).

## 17. Authorization
Cache must be wiped/scoped correctly on logout — per `CORE_DATA_INSTRUCTIONS.md`'s `AuthRepository.logout()` "deep clean" pattern (wipes Child Lock hashes, Entitlement snapshots); this Dashboard cache table must be added to that same logout-wipe routine to prevent data leakage between users on a shared device.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Network fetch fails, cache exists | Serve cached data with `stale: true` |
| Network fetch fails, no cache exists | Show explicit empty/error state (not a crash) |
| Offline, module shortcut requires connectivity | Inline "requires connection" indicator, no navigation |
| Reconnection | Background refresh, no jarring full reload |

## 19. Offline First
This IS the offline-first implementation for the Dashboard feature.

## 20. Local Data
Room-backed cache per §14.

## 21. Localization
"May be outdated" indicator copy localized via localization package.

## 22. RTL
Staleness indicator (icon/badge) mirrors correctly in RTL layouts.

## 23. Analytics
`dashboard_offline_state_shown` (PRD §1.19).

## 24. Performance
Read-through cache must not add perceptible latency on the happy (online) path — cache write should be fire-and-forget after a successful network response, not block the UI update.

## 25. Security
Cache wiped on logout (§17); no sensitive data persisted beyond what the API already returns to the authenticated owner; Room database encryption follows the platform's existing `core-database` encryption-at-rest convention (confirm existing convention, do not introduce a new one).

## 26. Library Requirements
No new dependencies — uses existing Room/SQLDelight (whichever `core-database` uses) and Kotlin Coroutines.

## 27. Testing
1. Unit test: successful network fetch writes to cache and returns fresh data.
2. Unit test: network failure with existing cache returns cached data with `stale: true`.
3. Unit test: network failure with no cache returns explicit error/empty state.
4. **Mandatory airplane-mode simulation test (PRD §7 item 5):** simulate airplane mode, confirm Dashboard renders fully from cache rather than blocking or erroring.
5. Unit test: reconnection triggers background refresh without full-screen reload.
6. Unit test: cache is correctly scoped per `childId` (no cross-child data leakage).
7. Unit test: logout wipes the Dashboard cache table.

## 28. Documentation
KDoc citing PRD §1.14, §7 item 5, and the logout deep-clean integration point.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Room Cache Entity and DAO**
- Task ID: K07-T01
- Objective: Local persistence schema.
- Why This Is Required: Foundation for offline rendering.
- Existing Architecture to Follow: `core-database` DAO/entity conventions.
- Existing Files to Reuse: `core-database` base setup (confirm exact conventions before finalizing).
- Files to Create: `DashboardCacheEntity.kt`, `DashboardCacheDao.kt`.
- Files to Modify: none.
- Implementation Details: Per §14.
- Business Rules: N/A.
- Validation: `childId` scoping.
- Error Handling: N/A.
- Security: No new sensitive fields beyond API payload.
- Performance: Indexed by `child_id`.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: KDoc.
- Dependencies: none.
- Do Not Change: Do not modify unrelated `core-database` tables.
- Expected Result: Entity/DAO compile and function.
- Definition of Done: Matches §14.

**Task 02 — Implement DashboardRepositoryImpl (Read-Through Cache)**
- Task ID: K07-T02
- Objective: Concrete repository implementing K-01's interface.
- Why This Is Required: Core deliverable.
- Existing Architecture to Follow: `core-data` orchestration pattern, `ConnectivityObserver`.
- Existing Files to Reuse: `ConnectivityObserver`, `NoorResult`, `DispatcherProvider`, `:core:network` client.
- Files to Create: `DashboardRepositoryImpl.kt`.
- Files to Modify: `di/ParentDashboardModule.kt`.
- Implementation Details: Per §10.
- Business Rules: PRD §1.14.
- Validation: Cache-key scoping per §15.
- Error Handling: Per §18.
- Security: N/A here (Task 03 handles logout wipe).
- Performance: Fire-and-forget cache write on success path.
- Localization: N/A (data layer).
- RTL: N/A.
- Analytics: N/A (fired from ViewModel/UI layer based on returned `stale` flag).
- Tests: Covered in Task 04.
- Documentation: KDoc.
- Dependencies: Task 01, K-01's `DashboardRepository` interface.
- Do Not Change: Do not modify `ConnectivityObserver` itself.
- Expected Result: Full offline-first read-through cache functional.
- Definition of Done: Airplane-mode test passes.

**Task 03 — Integrate Logout Deep-Clean**
- Task ID: K07-T03
- Objective: Wipe Dashboard cache on logout.
- Why This Is Required: Prevent data leakage between users on shared devices, matching `AuthRepository.logout()`'s existing deep-clean pattern.
- Existing Architecture to Follow: `AuthRepository.logout()` (`core-data`).
- Existing Files to Reuse: `AuthRepository.logout()`.
- Files to Create: none.
- Files to Modify: `AuthRepository.logout()` implementation (add `DashboardCacheDao.clearAll()` call) — or, if direct modification of a core-data class is discouraged for a feature-module blueprint, register a logout-hook/listener mechanism if one already exists in the codebase (confirm before choosing approach).
- Implementation Details: Ensure Dashboard cache table is wiped alongside `ChildLockDao`/`EntitlementSnapshotDao`.
- Business Rules: Security/privacy requirement.
- Validation: N/A.
- Error Handling: N/A.
- Security: Prevents data leakage — security-relevant.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04 (test #7).
- Documentation: Comment explaining the integration point.
- Dependencies: Task 01, existing `AuthRepository.logout()`.
- Do Not Change: Do not alter `logout()`'s existing wipe behavior for other tables — only add this table to the same routine.
- Expected Result: Cache cleared on logout.
- Definition of Done: Test #7 passes.

**Task 04 — Write Test Suite**
- Task ID: K07-T04
- Objective: Cover §27, notably the mandatory airplane-mode test.
- Why This Is Required: PRD §7 item 5 explicit mandate.
- Existing Architecture to Follow: Existing Kotlin test + fake `ConnectivityObserver`/network-client conventions.
- Existing Files to Reuse: Test doubles.
- Files to Create: `DashboardOfflineCachingTest.kt`.
- Files to Modify: none.
- Implementation Details: 7 cases per §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: N/A.
- Security: Test #7 (logout wipe) is privacy-critical.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test KDoc.
- Dependencies: Tasks 01–03.
- Do Not Change: N/A.
- Expected Result: All pass.
- Definition of Done: 100% of §27 green, including the mandatory airplane-mode simulation.

## 30. Definition of Done
`DashboardRepositoryImpl` provides full offline-first read-through caching, staleness correctly flagged, cache wiped on logout, all tests green including the mandatory airplane-mode test.

## 31. Final Verification Checklist
- [ ] Airplane-mode simulation test passing
- [ ] Cache correctly scoped per `childId`, no cross-child leakage
- [ ] Logout wipes this cache alongside existing sensitive-data wipe routine
- [ ] Background refresh on reconnection does not cause jarring reload
- [ ] Module shortcuts requiring connectivity show inline indicator, never a broken destination
