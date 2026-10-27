# Blueprint: Report Offline Caching & Deep Link Handling

## 1. Feature Context
Platform: NoorHeroes KMP App. Module: `:feature:reports`, integrating `:core:offline-cache` and `:core:navigation`. Delivers the offline read-caching layer and deep-link entry points for the whole Per-Child Reports feature.

## 2. Parent Feature
C.22 — Per-Child Reports.

## 3. Sub-feature
K-09 — Report Offline Caching & Deep Link Handling.

## 4. Objective
Provide read-only offline caching for all report screens (K-01 through K-06) via `:core:offline-cache`, and implement the `noorheroes://parent/reports/{child_id}` deep links with mandatory Parent Gate revalidation on every entry, including the "Your weekly report is ready" notification landing target.

## 5. Business Requirements
Source: PRD §6.7, §6.8, §6.9, §1.14 Offline States.
- In-app report views render from cache when offline (read-only); export/share actions are blocked offline (delegated to K-07/K-08, this blueprint only owns the read-cache and deep-link plumbing).
- Deep links: `noorheroes://parent/reports/{child_id}`, `noorheroes://parent/reports/{child_id}/ai-history`.
- Landing target for "Your weekly report is ready" push notifications (owned by C.25), always passing through the Parent Gate via B17's `DeepLinkResolutionHandler`/`RequiresLockGate` resolve-before-navigate contract.

## 6. Existing Architecture
Reuses `:core:offline-cache` (Room) infrastructure per `CORE_DATABASE_INSTRUCTIONS.md`/`CORE_DATASTORE_INSTRUCTIONS.md`, `:core:navigation`'s deep-link registration pattern per `CORE_NAVIGATION_INSTRUCTIONS.md`, and B17's `DeepLinkResolutionHandler`/`RequiresLockGate` resolve-before-navigate contract (`core-notifications`) for notification-originated entries — reused as-is, not reimplemented per-feature.

## 7. Existing Code to Reuse
- `:core:offline-cache` Room database setup and DAO conventions.
- `:core:navigation`'s deep-link registration mechanism and B17's confirmed `DeepLinkResolutionHandler` (`core-notifications`), which intercepts every notification-tap intent and always resolves against the server (B17 B-06's `GET /v1/notifications/resolve`) before navigation, returning a `DeepLinkResolution` sealed class (`Valid`, `RequiresLockGate`, `ContentUnavailable`, `SessionExpiredOrMismatch`, `Offline`) — the `RequiresLockGate` outcome is what routes a notification-triggered report deep link through the Parent Gate. Direct (non-notification) app-link entry to this feature's routes is separately guarded at the navigation layer by each `Route.requiredAuthState = BaseAuthState.Parent` (K-01 through K-06), which is unreachable without an active Parent Mode session — the two mechanisms are complementary, not duplicative.
- `ConnectivityObserver` (`core-data`/`core-common`, reused from K-07/K-08).
- C.20 K-07's `DashboardRepositoryImpl`/`DashboardCacheEntity` read-through-cache pattern (attempt network fetch → write-through to a `CacheEntity` on success → on failure/offline, read from the `CacheEntity` and return with a `stale: Boolean` flag) — this blueprint applies the identical pattern per report type rather than inventing a new caching approach.

## 8. Files to Create
- `feature/reports/src/androidMain/kotlin/.../ReportsRoomDatabase.kt` (or shared Room setup per platform convention)
- `feature/reports/src/commonMain/kotlin/.../ReportCacheDao.kt` (interface, actual DAO per-platform if required by the platform's Room/SQLDelight setup)
- `feature/reports/src/commonMain/kotlin/.../ReportDeepLinks.kt`
- `feature/reports/src/commonTest/kotlin/.../ReportDeepLinkGateRevalidationTest.kt`
- `feature/reports/src/commonTest/kotlin/.../ReportOfflineCacheSyncTest.kt`

## 9. Files to Modify
- `ReportRepository.kt` (K-01) — wrap all `get*` methods with a cache-then-network-refresh pattern, falling back to cache when offline
- App-level deep-link registration — register `noorheroes://parent/reports/{child_id}` and `.../ai-history`
- C.25's notification-landing configuration — point "Your weekly report is ready" at the `PerChildReportRoute` deep link

## 10. KMP Requirements
- `ReportRepository` implementations (per K-01/K-02/.../K-06's individual methods) follow C.20 K-07's `DashboardRepositoryImpl` pattern exactly: attempt network fetch via `:core:network`; on success, write-through to the report type's `CacheEntity` (Room) and return fresh data; on failure (network error) or when `ConnectivityObserver` reports offline, read from the `CacheEntity` and return with a `stale: Boolean` flag set on the returned domain model — on a network failure while online (e.g., server error), surface the actual error rather than silently falling back to stale cache.
- `ReportDeepLinks.register(navigator)`: registers both deep-link patterns. Direct app-link entry is guarded by each screen's `Route.requiredAuthState = BaseAuthState.Parent` (unreachable outside an active Parent Mode session); notification-originated entry additionally passes through `DeepLinkResolutionHandler` (`core-notifications`, B17), whose `RequiresLockGate` outcome routes through the Parent Gate before the destination `Route` is ever reached — together these ensure no deep-link path (direct or notification-originated) bypasses parent verification.
- Notification landing: C.25's "Your weekly report is ready" notification payload resolves to the `PerChildReportRoute(childId)` deep link via `DeepLinkResolutionHandler`, following B17 B-02's existing resolve-before-navigate contract.

## 11. Files to Create — continued
Cache invalidation: on successful online fetch, previous cache entry for that key is overwritten (not appended); cache entries are **not** used to satisfy export/share actions (K-07/K-08 always require a fresh online call regardless of cache state, per Edge Case #9).

## 12. NextJS Requirements
N/A.

## 13. API Mapping
N/A directly — this blueprint wraps the repository methods defined across K-01 through K-06, each mapped to its respective backend endpoint (B-01 through B-06).

## 14. Database Requirements (Local)
Room tables per cached report type, mirroring `DashboardCacheEntity`'s shape (`dashboard_cache(child_id, report_type_nullable, payload_json, cached_at)`, C.20 K-07 §14): `PerChildReportCacheEntity`, `SkillDetailCacheEntity`, `AiHistoryCacheEntity`, `SafetyReportCacheEntity`, `MonthlyFamilyReportCacheEntity`, `AiInsightReportCacheEntity` — each keyed by the relevant scope (`childId`+range, `childId`+`skillId`, `familyId`, etc.) storing the serialized payload plus a `cachedAt: Instant` timestamp used to compute the `stale` flag and "as of" freshness labeling while offline. Exact DAO/table-creation conventions confirmed against `core-database`'s established patterns per C.20 K-07 §7, not invented independently.

## 15. Validation
Deep-link `childId` path segment must be a well-formed identifier before being passed to `PerChildReportRoute`; malformed deep links fail gracefully to a generic error/home screen, not a crash.

## 16. Authentication
Every deep-link entry point is parent-verified: direct app-links via `Route.requiredAuthState = BaseAuthState.Parent`, notification-originated links via B17's `DeepLinkResolutionHandler`/`RequiresLockGate` — no exceptions, regardless of prior session state.

## 17. Authorization
Server-side family-ownership checks (per each respective backend endpoint) remain the ultimate authority; the client-side gate revalidation is a UX/security-defense-in-depth layer, not a replacement for server-side checks.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Offline, cache available | Cached content rendered with "as of [cached_at]" freshness label |
| Offline, no cache available | Explicit "you're offline and this hasn't loaded yet" state, not a blank screen |
| Online, server error | Fresh error surfaced, not masked by stale cache |
| Malformed deep-link `childId` | Graceful fallback to home/error screen, no crash |
| Deep-link entry with an expired/invalid session | Parent Gate revalidation blocks entry, routes to gate flow first |

## 19. Offline First
This blueprint IS the offline-first implementation for all read-only report screens; export/share actions explicitly remain online-only per Edge Case #9 (owned by K-07/K-08, respected here by never routing those actions through the cache layer).

## 20. Local Data
Per §14 — Room tables per report type, `cached_at` timestamp on each for freshness labeling.

## 21. Localization
"As of [time]" freshness labels and offline-state messages are locale-resolved, including locale-appropriate relative-time formatting (e.g., "2 hours ago" translated correctly, not just the raw string substituted).

## 22. RTL
Freshness labels and offline-state banners mirror correctly for Arabic/Urdu.

## 23. Analytics
`report_delayed_state_shown` / `report_no_activity_state_shown` fired when the corresponding cached/empty states render (shared analytics events across K-01 through K-06, wired centrally here where the cache-fallback logic lives).

## 24. Performance
Cache reads must be fast (local Room query, no network dependency) so offline rendering feels instant; write-through on successful network fetch happens off the main thread.

## 25. Security
Cached report data is stored using the platform's existing local-storage security conventions (no plaintext sensitive data beyond what's already deemed acceptable for on-device caching elsewhere in the app) — confirm the platform's existing encryption-at-rest convention for `:core:offline-cache` rather than inventing a new one for this feature specifically.

## 26. Library Requirements
No new dependencies; reuses `:core:offline-cache`'s existing Room/SQLDelight setup.

## 27. Testing
1. Unit test: successful online fetch write-throughs to cache correctly.
2. Unit test: offline fetch with available cache returns cached data with correct freshness timestamp.
3. Unit test: offline fetch with no cache returns the explicit "hasn't loaded yet" state, not a crash or blank screen.
4. **Deep-link gate-revalidation test:** confirm every registered deep link is guarded (`requiredAuthState` for direct links, `DeepLinkResolutionHandler`/`RequiresLockGate` for notification-originated links), with no code path bypassing either.
5. Integration test: full offline-cache-then-reconnect-refresh flow (cached view shown offline, then automatically refreshed on reconnect).
6. Integration test: notification-triggered deep link correctly lands on `PerChildReportRoute` with the correct `childId` and passes gate revalidation.

## 28. Documentation
KDoc explaining the cache-then-refresh pattern and explicitly noting that export/share actions never consult this cache layer (Edge Case #9 boundary).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Set Up Room Cache Tables for Each Report Type**
- Task ID: K09-T01
- Objective: Local persistence schema for offline read caching.
- Why This Is Required: Foundation for offline-first rendering across K-01 through K-06.
- Existing Architecture to Follow: `:core:offline-cache`'s existing Room/SQLDelight conventions per `CORE_DATABASE_INSTRUCTIONS.md`.
- Existing Files to Reuse: `:core:offline-cache` base setup.
- Files to Create: `ReportCacheDao.kt`, platform-specific Room database extension.
- Files to Modify: none.
- Implementation Details: Per §14.
- Business Rules: PRD §6.7, §1.14.
- Validation: N/A.
- Error Handling: N/A.
- Security: Reuse existing encryption-at-rest convention.
- Performance: Indexed lookups per cache key.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: Schema docstring.
- Dependencies: none.
- Do Not Change: `:core:offline-cache`'s shared infrastructure used by other features.
- Expected Result: Cache tables exist and are queryable.
- Definition of Done: Schema matches §14.

**Task 02 — Wrap ReportRepository Methods with Cache-Then-Refresh Pattern**
- Task ID: K09-T02
- Objective: Every `get*` method in `ReportRepository` (K-01 through K-06) reads through the cache-then-network pattern.
- Why This Is Required: Delivers offline-first behavior consistently across the whole feature.
- Existing Architecture to Follow: Repository pattern established across K-01–K-06.
- Existing Files to Reuse: `ReportRepository.kt` (extend all existing methods).
- Files to Create: none.
- Files to Modify: `ReportRepository.kt`.
- Implementation Details: Per §10.
- Business Rules: PRD §6.7, §1.14.
- Validation: N/A.
- Error Handling: Per §18.
- Security: N/A.
- Performance: Off-main-thread write-through.
- Localization: Freshness label formatting.
- RTL: N/A.
- Analytics: `report_delayed_state_shown`/`report_no_activity_state_shown`.
- Tests: Covered in Task 04.
- Documentation: KDoc.
- Dependencies: Task 01, K-01 through K-06's repository method signatures.
- Do Not Change: The underlying network-call logic of each method (only wraps it).
- Expected Result: All report reads offline-capable.
- Definition of Done: Cache-then-refresh verified for every report type.

**Task 03 — Register Deep Links with B17's DeepLinkResolutionHandler**
- Task ID: K09-T03
- Objective: Deep links reachable, always gate-revalidated.
- Why This Is Required: PRD §6.8/§6.9's explicit requirement.
- Existing Architecture to Follow: `:core:navigation` deep-link registration, B17's `DeepLinkResolutionHandler`.
- Existing Files to Reuse: `core-notifications::DeepLinkResolutionHandler`.
- Files to Create: `ReportDeepLinks.kt`.
- Files to Modify: App-level deep-link registration, C.25's notification-landing config.
- Implementation Details: Per §10.
- Business Rules: PRD §6.8, §6.9, B.17's universal rule.
- Validation: Malformed `childId` handled gracefully.
- Error Handling: Per §18.
- Security: Gate revalidation is the primary control here.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: KDoc.
- Dependencies: Task 02, B17's `DeepLinkResolutionHandler` must exist.
- Do Not Change: `DeepLinkResolutionHandler`'s implementation itself.
- Expected Result: Deep links reachable and correctly gated.
- Definition of Done: Task 04's gate-revalidation test passes for every registered deep link.

**Task 04 — Write Test Suite**
- Task ID: K09-T04
- Objective: Cover §27.
- Why This Is Required: QA coverage for offline behavior and deep-link security.
- Existing Architecture to Follow: Kotlin test + Room in-memory test database conventions.
- Existing Files to Reuse: Existing offline-cache test utilities.
- Files to Create: `ReportOfflineCacheSyncTest.kt`, `ReportDeepLinkGateRevalidationTest.kt`.
- Files to Modify: none.
- Implementation Details: 6 test cases per §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert exact states.
- Security: Gate-revalidation test is critical.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test KDoc.
- Dependencies: Tasks 01–03.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 green.

## 30. Definition of Done
All six report screens (K-01–K-06) read-cache offline correctly with freshness labeling, deep links registered and gate-revalidated on every entry including notification landings, export/share actions never consult the cache layer, all tests green.

## 31. Final Verification Checklist
- [ ] Every report screen renders correctly offline from cache with an "as of" freshness label
- [ ] No-cache-available offline state is explicit, never a blank screen
- [ ] Deep-link gate-revalidation test confirms no bypass path exists, including for notification-triggered entries
- [ ] Export/share actions (K-07/K-08) never read from this cache layer
- [ ] Localization of relative-time freshness labels verified
- [ ] Encryption-at-rest convention matches the platform's existing `:core:offline-cache` standard
