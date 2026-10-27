# K-05 — Offline Search & Cached Content Index

## 1. Feature Context
Part of Feature B.13 (Search & Discovery). Handles search when the device has no connectivity, scoping results to locally-downloaded/favorited content metadata rather than failing outright or falsely claiming zero results.

## 2. Parent Feature
B.13 — Search & Discovery

## 3. Sub-feature
K-05 — Offline Search & Cached Content Index

## 4. Objective
Detect no-connectivity state and route search queries against the existing offline-content-cache index (downloaded/favorited content metadata) instead of attempting a failing network call, with a clearly-labeled offline-results UI state.

## 5. Business Requirements
- Edge Case 7: searching while offline must function against the locally-cached/downloaded content index, clearly indicating results are limited to downloaded content, rather than failing outright or claiming zero results when the actual issue is connectivity.
- §1.14: search functions against the locally-cached/downloaded content index when offline, clearly labeled.
- §2.2 Screen: Search Results — Offline state (cached-only, labeled).

## 6. Existing Architecture
Reuses the platform's **existing offline-content-cache index** (already built for A.3's Offline Downloads/Sync feature, per B.15's own blueprint and A.3's offline-cache pattern) — this blueprint does not build a second, parallel offline-content index. It adds a connectivity-aware routing layer in front of K-02's search path.

## 7. Existing Code to Reuse
- A.3/B.15's existing offline-content-cache Room tables (downloaded/favorited content metadata) — queried read-only here, not duplicated.
- `core-network`'s existing connectivity-observer utility (used app-wide for other offline-aware features) — reused for no-network detection, not reimplemented.
- K-02's `SearchResultCard`/grid components — reused for rendering offline results, with an added offline-indicator banner.

## 8. Files to Create
- `feature-search/src/commonMain/kotlin/.../search/offline/OfflineSearchResultsBanner.kt` (Composable — the "offline results" indicator).
- `feature-search-domain/.../OfflineSearchUseCase.kt` (queries the existing offline-content-cache index by text match against locally-cached titles/tags).
- `feature-search/src/commonTest/kotlin/.../OfflineSearchTest.kt`.

## 9. Files to Modify
- `SearchViewModel.kt`/`SearchRepository` (K-02) — on connectivity-observer reporting offline, route query submission to `OfflineSearchUseCase` instead of `SearchApi`; on reconnect, resume normal online routing.
- `SearchResultsScreen.kt` (K-02) — render `OfflineSearchResultsBanner` when in offline mode.

## 10. Backend Requirements
None — this flow makes no network call by design when offline.

## 11. KMP Requirements
- Connectivity-observer check occurs before query submission; if offline, `OfflineSearchUseCase` runs a local text match (simple contains/startsWith or existing local search utility, if the offline-cache index already exposes one) against the downloaded-content-cache index's title/tag fields.
- Results rendered through the same `SearchResultCard` grid as K-02, with `OfflineSearchResultsBanner` clearly indicating "Showing results from your downloads" (or equivalent localized copy) — never silently identical to the online results screen.
- Zero offline matches → a distinct message clarifying limited-to-downloads scope, **not** the same "zero results" empty state as K-02's online empty state (avoids conflating "nothing matches at all" with "nothing in your downloads matches, but more might be available online").
- On reconnect mid-session, the next query issued uses the normal online path (B-01) — the currently-displayed offline result set is not silently swapped underneath the user.
- Offline result-card taps route to the destination screen only if the target content is itself downloaded/available offline (delegates to that destination feature's own offline-availability handling).

## 12. NextJS Requirements
N/A.

## 13. API Contract
None (offline path makes no network call).

## 14. Database Requirements
Read-only queries against the existing offline-content-cache Room tables (owned by A.3/B.15, not this blueprint) — no new tables created here.

## 15. Validation
Same query-text length guard as K-02, applied before local matching.

## 16. Authentication
N/A (local-only operation).

## 17. Authorization
N/A — offline results are inherently already scoped to content the child's device has downloaded, which was itself subject to B-01-equivalent age-band filtering at download time (per A.3/B.15's download-manifest API, which is itself age-band-gated).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Offline + zero downloaded matches | Distinct "nothing in your downloads matches" message, not the generic online empty state |
| Offline-cache index read failure | Graceful fallback to a simple "search unavailable offline" message rather than a crash |
| Reconnect mid-session | Next query uses online path; current results not silently replaced |

## 19. Offline First
This entire blueprint *is* the offline-first behavior for Search — the canonical implementation of the platform's offline-first search requirement.

## 20. Local Data
Reads (does not own) the existing offline-content-cache index from A.3/B.15.

## 21. Localization
Offline-indicator banner copy and the offline-zero-match message are both localized (English/Hindi/Arabic/Urdu).

## 22. RTL
Banner and result grid mirror correctly in RTL, consistent with K-02.

## 23. Analytics
`search_offline_mode_shown` — fired when the offline path is engaged.

## 24. Performance
Local text matching against the offline-cache index is bounded by the (typically small) size of a single device's downloaded-content set — no pagination/infinite-scroll concern expected at this scale.

## 25. Security
No new security surface — offline results are drawn exclusively from content already downloaded under existing age-band-gated download rules.

## 26. Library Requirements
Existing `core-network` connectivity observer, existing offline-cache Room DAOs. No new library.

## 27. Testing
- Test simulating airplane mode: assert results are still shown from the local cache with the offline indicator visible (mirrors the PRD's Android testing-strategy requirement in §6.10).
- Test: offline zero-match message is distinct from the online empty state.
- Test: reconnect mid-session does not mutate the currently-displayed result set.

## 28. Documentation
KDoc noting this reuses A.3/B.15's existing offline-content-cache index and does not introduce a parallel one.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Implement OfflineSearchUseCase**
Objective: local text match against the existing offline-content-cache index.
Files to create: `OfflineSearchUseCase.kt`.
Do not change: A.3/B.15's offline-cache table schema — read-only consumer.

**Task 02 — Wire Connectivity-Aware Routing**
Objective: route query submission to online (K-02) or offline (this blueprint) path based on the existing connectivity observer.
Files to modify: `SearchViewModel.kt`/`SearchRepository`.

**Task 03 — Build OfflineSearchResultsBanner**
Files to create: `OfflineSearchResultsBanner.kt`.
Files to modify: `SearchResultsScreen.kt` (K-02) to conditionally render it.

**Task 04 — Handle Offline Zero-Match State**
Objective: distinct message from the online empty state.

**Task 05 — Add Airplane-Mode Simulation Test**
Files to create: `OfflineSearchTest.kt`.

**Task 06 — Final Review**
Objective: confirm no duplicate offline-content index was created; confirm reconnect-mid-session behavior does not surprise-swap results.

## 30. Definition of Done
- Offline queries return locally-cached results with a clear indicator.
- Airplane-mode test passes.
- Reconnect behavior verified non-disruptive.

## 31. Final Verification Checklist
- [ ] Offline search never claims zero results due to connectivity alone — always clearly scoped to downloads.
- [ ] Offline indicator banner always visible during offline results.
- [ ] No parallel/duplicate offline-content index introduced.
- [ ] Reconnect mid-session does not silently mutate the displayed result set.
- [ ] Offline zero-match message is distinct from the online empty state.
