# K-04 — Recent Searches Local Cache & Management

## 1. Feature Context
Part of Feature B.13 (Search & Discovery). The client-side Room cache backing K-01's recent-searches list, synced against B-04, with strict per-child-session isolation on shared devices.

## 2. Parent Feature
B.13 — Search & Discovery

## 3. Sub-feature
K-04 — Recent Searches Local Cache & Management

## 4. Objective
Build a Room-backed local cache of recent searches scoped per active child session, synced with B-04's `GET`/`DELETE /v1/search/recent`, with cap/pruning mirrored client-side.

## 5. Business Requirements
- FR-10: recent searches stored per-child, clearable by the child.
- Edge Case 4: two siblings sharing a device must never see cross-contaminated recent-search history — switching child sessions shows the new child's own (or empty) history only.
- §4.5: capped per child (rolling window, e.g., 20), clearable at any time.

## 6. Existing Architecture
New Room entity/DAO in `core-database`, following the existing multi-child, session-scoped local-cache pattern already established elsewhere in the app (per `CORE_DATABASE_INSTRUCTIONS.md`'s per-child data-isolation convention) — every query is parameterized by the currently-active `child_id`, sourced from the app's existing active-child-session mechanism (not re-derived here).

## 7. Existing Code to Reuse
- `core-database`'s existing Room setup/DAO conventions (per `CORE_DATABASE_INSTRUCTIONS.md`).
- `core-datastore`'s active-child-session accessor (used app-wide for the currently-selected child profile on a shared device) — this blueprint reads from it, does not reimplement child-session tracking.
- K-02's `SearchRepository` — extended here with recent-search-specific methods rather than a wholly separate repository, if architecturally cleaner; otherwise a dedicated `RecentSearchRepository` following the same Koin-injected pattern.

## 8. Files to Create
- `core-database/src/commonMain/kotlin/.../entity/RecentSearchEntity.kt`.
- `core-database/src/commonMain/kotlin/.../dao/RecentSearchDao.kt` (`insertAndPrune(childId, entry, cap)`, `observeForChild(childId): Flow<List<RecentSearchEntity>>`, `clearForChild(childId)`).
- `feature-search-domain/.../RecentSearchRepository.kt` (interface) + impl composing `RecentSearchDao` + B-04's API.
- `feature-search/src/commonTest/kotlin/.../RecentSearchCacheTest.kt`.
- `feature-search/src/commonTest/kotlin/.../RecentSearchChildIsolationTest.kt`.

## 9. Files to Modify
- `SearchViewModel.kt` (K-01) — source the recent-searches list from `RecentSearchRepository.observeForChild()` instead of a placeholder.
- `SearchModule.kt` — register `RecentSearchDao`/`RecentSearchRepository`.

## 10. Backend Requirements
Consumes B-04: `GET /v1/search/recent` (sync-on-read/refresh), `DELETE /v1/search/recent` (clear).

## 11. KMP Requirements
- `RecentSearchEntity` keyed by `(search_id, child_id)`; all DAO queries parameterized by `child_id`.
- On child-session switch (existing app-wide mechanism), the observed `Flow` automatically re-scopes to the new `child_id` — no manual cache-clear step required, since queries are always `child_id`-filtered at the source.
- Cap/prune client-side in lockstep with B-04's server-side cap (same default, e.g., 20) — insert-then-prune in a single DAO transaction.
- Re-run a past query: tapping a recent-search item feeds its `query_text` back into K-02's search-submission path.
- Clear-all action: local DAO clear + call to `DELETE /v1/search/recent`, with local clear applied optimistically and rolled back only if the network call fails outright (not left in an inconsistent state).
- Offline read: recent searches display from local cache even with no connectivity (no network dependency for reading this list).

## 12. NextJS Requirements
N/A.

## 13. API Contract
`GET /v1/search/recent` → `{ items: [...] }`; `DELETE /v1/search/recent` → `204`, per B-04 §13.

## 14. Database Requirements
Room table `recent_search_cache`: `search_id`, `child_id`, `query_text`, `input_method`, `created_at` — mirrors B-04's server schema shape, local-only cache (not source of truth; server is authoritative on conflict).

## 15. Validation
None beyond what K-01/K-02 already apply to query text at entry.

## 16. Authentication
N/A (local cache); network sync calls use the standard authenticated `core-network` client.

## 17. Authorization
Per-`child_id` query scoping is the authorization boundary here — every DAO method requires an explicit `child_id` parameter, with no "get all" method that could leak across children.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Sync-from-server failure | Local cache remains the display source of truth; retry on next natural refresh, not blocking |
| Clear-all network failure | Local optimistic clear rolled back, item list restored, user informed via standard non-alarming error affordance |
| Child-session switch mid-flight | In-flight queries for the old `child_id` are discarded/ignored on completion (stale-response guard) |

## 19. Offline First
Recent-searches list is fully offline-capable for reads; writes (new entries, clears) queue as best-effort sync rather than blocking on connectivity.

## 20. Local Data
Owns `recent_search_cache` Room table, described in §14.

## 21. Localization
N/A directly (data layer); display strings are K-01's concern.

## 22. RTL
N/A (data layer).

## 23. Analytics
Feeds `search_recent_query_reused` and `search_recent_searches_cleared`, fired from K-01's UI layer on successful interaction with this repository's methods.

## 24. Performance
Room queries indexed on `(child_id, created_at DESC)` matching B-04's server-side index shape; `Flow`-based observation avoids manual polling.

## 25. Security
Per-`child_id` scoping at the DAO layer is the primary safeguard against Edge Case 4's cross-sibling leakage — every query signature requires `child_id`, making an unscoped read a compile-time-visible anomaly during review.

## 26. Library Requirements
Room (via `core-database`), Kotlin Coroutines/Flow. No new persistence library.

## 27. Testing
- Unit: cap/prune behavior (insert 25, assert 20 remain).
- **Child-isolation test:** insert entries for Child A and Child B, switch active session, assert `observeForChild` returns only the active child's entries, verified for both directions of the switch.
- Optimistic-clear-with-rollback test (simulate network failure on `DELETE`).
- Stale-response guard test (session switches mid-request).

## 28. Documentation
KDoc noting the `child_id`-mandatory DAO signature convention and why (Edge Case 4 prevention).

## 29. AI Coding Agent Implementation Steps
**Task 01 — Define RecentSearchEntity & DAO**
Files to create: `RecentSearchEntity.kt`, `RecentSearchDao.kt`.
Business rules: every query method requires explicit `child_id`.

**Task 02 — Implement RecentSearchRepository**
Objective: compose DAO + B-04's API, cap/prune, optimistic clear with rollback.
Files to create: `RecentSearchRepository.kt` + impl.

**Task 03 — Wire Active-Child-Session Re-Scoping**
Objective: confirm `observeForChild` Flow re-emits correctly on session switch (using `core-datastore`'s existing active-child accessor).
Files to modify: `SearchViewModel.kt`.

**Task 04 — Add Child-Isolation Test (highest priority)**
Files to create: `RecentSearchChildIsolationTest.kt`.

**Task 05 — Add Cap/Prune & Rollback Tests**
Files to create: `RecentSearchCacheTest.kt`.

**Task 06 — Final Review**
Objective: confirm no DAO method exists without a `child_id` parameter.

## 30. Definition of Done
- Recent searches cached locally, synced with B-04.
- Cap/prune verified client-side.
- Child-isolation proven by test on a simulated shared-device session switch.

## 31. Final Verification Checklist
- [ ] Every DAO query method requires an explicit `child_id` parameter — no unscoped read exists.
- [ ] Session switch correctly re-scopes the observed recent-searches list.
- [ ] Cap/prune matches server-side default.
- [ ] Optimistic clear rolls back cleanly on network failure.
- [ ] Recent searches readable fully offline.
