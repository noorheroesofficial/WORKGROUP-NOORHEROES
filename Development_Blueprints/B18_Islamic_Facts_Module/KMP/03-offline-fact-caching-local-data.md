# K-03 — Offline Fact Caching & Local Data

## 1. Feature Context
Part of Feature B.18 (Islamic Facts Module). Provides offline-first local persistence for the daily fact and Fact Detail payloads, consumed by K-01's ViewModel.

## 2. Parent Feature
B.18 — Islamic Facts Module

## 3. Sub-feature
2.3 Offline Fact Caching & Local Data (ID: K-03)

## 4. Objective
Implement Room-backed local caching of the daily fact and Fact Detail payloads so previously-viewed facts remain viewable offline, with a distinct "needs internet" signal for the linked-quiz section when its data wasn't separately pre-downloaded.

## 5. Business Requirements
- §1.14 Offline States: previously-cached Fact of the Day remains viewable offline; linked quiz requires connectivity unless pre-downloaded.
- Edge Case 9: offline child accesses a cached Fact of the Day, then tries the linked quiz which requires online question-set assembly — if not pre-downloaded, shows clear "needs internet" state, not silent failure.
- §6.7 Offline Support: daily fact and Fact Detail cached for offline viewing.

## 6. Existing Architecture
`:core:offline-cache` module's existing Room database and offline-first repository pattern (local cache → remote refresh → UI) — reused, not reimplemented locally. Consistent with the platform's general offline-content-availability messaging pattern.

## 7. Existing Code to Reuse
- `:core:offline-cache`'s existing Room `Database` instance and DAO-registration convention.
- `:core:offline-cache`'s existing cache-invalidation/staleness-indicator pattern (used by other content types) — reuse rather than build a facts-specific caching mechanism from scratch.
- `:core:network`'s existing connectivity-observer utility for detecting online/offline state.

## 8. Files to Create
- `feature-facts-data/src/commonMain/kotlin/.../local/FactEntity.kt` (Room entity).
- `feature-facts-data/src/commonMain/kotlin/.../local/FactDao.kt`.
- `feature-facts-data/src/commonMain/kotlin/.../FactsRepositoryImpl.kt` (extend from K-01 — add offline-first read logic).
- `feature-facts/src/commonTest/kotlin/.../OfflineFactCacheTest.kt`.
- `feature-facts/src/commonTest/kotlin/.../OfflineQuizUnavailableStateTest.kt`.

## 9. Files to Modify
- `:core:offline-cache`'s database module — register `FactEntity`/`FactDao` in the existing Room database schema (migration required if the DB is already versioned).

## 10. Backend Requirements
None new — consumes B-02/B-03's existing response payloads for caching.

## 11. KMP Requirements
- `FactsRepositoryImpl.getDailyFact()` / `getFactDetail()`: check local cache first, return immediately if fresh (same local day for daily fact), then trigger a background remote refresh, emitting updated state if the remote result differs.
- Offline read: if remote call fails and a local cache entry exists, return cached data with a staleness flag; if no cache exists, propagate the error for K-01's error state.
- Cache invalidation: daily fact cache invalidated at local-day rollover; Fact Detail cache invalidated on a reasonable TTL (e.g., matching the platform's general content-cache TTL convention — confirm existing convention before inventing a new TTL value).
- Quiz-availability check: a separate flag (not the fact cache itself) indicates whether the linked quiz's question data was part of an offline-downloaded content package; K-02's `FactQuizEntryCard` reads this flag to decide between normal/disabled/"needs internet" states.
- Retry on network recovery: `:core:network`'s connectivity observer triggers a background refresh attempt when connectivity is restored.

## 12. NextJS Requirements
N/A.

## 13. API Contract
No new API — consumes B-02/B-03's existing contracts as the remote data source for the offline-first repository.

## 14. Database Requirements
Local Room schema: `fact_cache(fact_id PK, payload_json, cached_at, is_stale)`. Migration added to `:core:offline-cache`'s existing Room schema version chain.

## 15. Validation
Cached payload deserialization failure (e.g., schema drift after an app update) → treat as cache miss, fall back to remote fetch, do not crash.

## 16. Authentication
N/A — local storage layer.

## 17. Authorization
Cache is child-session-scoped (existing `:core:offline-cache` convention for per-child local data isolation, if the platform's cache is multi-profile-aware — confirm before assuming a shared cache is acceptable, given multiple children may use one device per C.21 Multi-Child Management).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Remote fetch fails, cache exists | Cached data + staleness indicator |
| Remote fetch fails, no cache | Error/retry state (K-01) |
| Cached payload fails to deserialize | Treated as cache miss, remote fetch attempted |
| Quiz data not pre-downloaded, offline | "Needs internet" state (K-02), not a silent failure |

## 19. Offline First
This entire sub-feature is the offline-first implementation: Remote Data → Repository → Local Storage → UI, per the standard KMP offline-first flow.

## 20. Local Data
Room database, `fact_cache` table, scoped per active child profile.

## 21. Localization
Cached payload includes the already-localized text from the API response (per the child's locale at cache-write time); if locale changes, cache is treated as stale for that fact and refetched.

## 22. RTL
N/A at the data layer.

## 23. Analytics
None new; cache-hit/miss telemetry could feed into general offline-usage analytics if the platform already tracks that (confirm existing convention rather than adding a facts-specific metric).

## 24. Performance
Room queries indexed on `fact_id`; cache-first read avoids unnecessary network round-trips for same-day daily fact re-renders (e.g., app backgrounding/foregrounding).

## 25. Security
Cached fact content is non-sensitive (no PII); standard `:core:offline-cache` encryption-at-rest policy applies if the platform encrypts the local DB (inherit existing policy, do not weaken it for this table).

## 26. Library Requirements
Room (via `:core:offline-cache`), Kotlinx Serialization (existing platform convention for payload JSON storage) — no new libraries.

## 27. Testing
- Unit: cache-first read returns cached data immediately, background refresh updates state.
- Unit: offline read with no cache propagates error correctly.
- Unit: cached-payload deserialization failure falls back to remote fetch gracefully.
- Unit: quiz-unavailable-offline state distinct from a generic content error (Edge Case 9).
- Integration: cache invalidation at local-day rollover for the daily fact.

## 28. Documentation
KDoc on `FactsRepositoryImpl` documenting the offline-first read/refresh contract and the distinct quiz-availability flag.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Room Entity & DAO**
Objective: `FactEntity`, `FactDao`.
Existing Architecture to Follow: `:core:offline-cache`'s existing entity/DAO conventions.
Files to Create: `FactEntity.kt`, `FactDao.kt`.
Dependencies: None (can proceed in parallel with K-01's early tasks).
Definition of Done: Entity/DAO compile and integrate into the existing Room schema with a valid migration.

**Task 02 — Offline-First Repository Logic**
Objective: Extend `FactsRepositoryImpl` with cache-first read + background refresh.
Files to Modify: `FactsRepositoryImpl.kt`.
Dependencies: Task 01, K-01's repository interface.
Definition of Done: Passes Task 05 unit tests.

**Task 03 — Cache Invalidation**
Objective: Local-day rollover invalidation for daily fact; TTL-based invalidation for detail.
Dependencies: Task 02.
Definition of Done: Verified via test.

**Task 04 — Quiz-Availability Flag Wiring**
Objective: Expose a distinct flag for K-02's "needs internet" state, separate from the fact-content cache.
Dependencies: Task 02.
Definition of Done: K-02 correctly reads this flag.

**Task 05 — Tests**
Objective: Full coverage per §27.
Dependencies: Tasks 01–04.
Definition of Done: All green.

**Task 06 — Documentation**
Dependencies: Task 05.
Definition of Done: KDoc complete.

## 30. Definition of Done
- Offline-first read/refresh functioning per standard KMP pattern.
- Cache invalidation correct for both daily fact (day rollover) and detail (TTL).
- Quiz-availability distinctly signaled from general content-cache state.
- Multi-child profile scoping confirmed correct if applicable.
- Tests green, documentation complete.

## 31. Final Verification Checklist
- [ ] Cache-first read with background refresh verified
- [ ] Offline read with no cache surfaces a proper error/retry state, not a crash
- [ ] Deserialization failure falls back gracefully, no crash
- [ ] Quiz "needs internet" state distinct from generic content error (Edge Case 9)
- [ ] Cache correctly scoped per active child profile (multi-child device scenario)
- [ ] Room migration applied cleanly to existing schema
