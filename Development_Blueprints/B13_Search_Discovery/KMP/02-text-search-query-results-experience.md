# K-02 — Text Search Query & Results Experience

## 1. Feature Context
Part of Feature B.13 (Search & Discovery). The core query-to-results loop for typed search, consuming B-01's `GET /v1/search`.

## 2. Parent Feature
B.13 — Search & Discovery

## 3. Sub-feature
K-02 — Text Search Query & Results Experience

## 4. Objective
Implement debounced text-query submission, the filterable Search Results screen, and safe empty-state handling, with strict result-routing by content type.

## 5. Business Requirements
- FR-2: type a query, apply a type/age filter, open a result.
- FR-8: story result → Story Detail (A.3); surah result → Surah Learning (A.5); dua result → Dua Learning (A.6).
- §1.13 Loading States: skeleton result-card shimmer while query processes.
- §1.12: zero results → friendly, safe empty state with a constructive suggestion, never a raw "no results" error.
- §2.2 Screen: Search Results — states default/loading/filtered/empty/offline; filter chips announce selected state; result cards individually labeled with title + content type.

## 6. Existing Architecture
Extends `feature-search` (K-01's module). `SearchRepository` interface + Ktor-based implementation in `core-network`, following the existing repository pattern used by other features' `*Repository` classes (Koin-injected, not Hilt).

## 7. Existing Code to Reuse
- `core-network`'s `HttpClient` factory (Ktor) — for `GET /v1/search` calls.
- `core-designsystem`'s existing grid/card components — per §2.4, visually consistent with A.3's Stories Library and A.10's Games Hub grid patterns; reuse those card primitives rather than building a new grid component from scratch.
- `core-analytics`'s `AnalyticsTracker`.
- A.3/A.5/A.6's existing deep-link/navigation targets for Story Detail, Surah Learning, Dua Learning (do not build new destination screens — route into the existing ones).

## 8. Files to Create
- `feature-search/src/commonMain/kotlin/.../search/SearchResultsScreen.kt`.
- `feature-search/src/commonMain/kotlin/.../search/components/TypeFilterChipRow.kt`.
- `feature-search/src/commonMain/kotlin/.../search/components/SearchResultCard.kt`.
- `feature-search/src/commonMain/kotlin/.../search/components/EmptySearchState.kt`.
- `feature-search/src/commonMain/kotlin/.../search/components/SearchResultsSkeleton.kt`.
- `core-network/src/commonMain/kotlin/.../api/SearchApi.kt` (Ktor client for `GET /v1/search`).
- `feature-search-domain/.../SearchRepository.kt` (interface) + `SearchRepositoryImpl.kt`.
- `feature-search/src/commonTest/kotlin/.../SearchDebounceTest.kt`.
- `feature-search/src/commonTest/kotlin/.../EmptyStateBlocklistUiTest.kt`.

## 9. Files to Modify
- `SearchViewModel.kt` (K-01) — extend `SearchUiState` with a `results` sub-state and debounced-submission logic; delegate to `SearchRepository.search()`.
- `SearchModule.kt` (Koin) — register `SearchApi`, `SearchRepositoryImpl`.

## 10. Backend Requirements
Consumes B-01 exclusively: `GET /v1/search?q=&type=&child_id=` (note: `child_id` is not actually sent as a client param per B-01's server-derivation guarantee — the client only sends `q`/`type`; auth token carries child identity).

## 11. KMP Requirements
- Debounce text-query submission 300–400ms after the last keystroke — no request fired per keystroke.
- On submission, call `SearchRepository.search(query, type)` → renders `SearchResultsSkeleton` during the in-flight call.
- Render `TypeFilterChipRow` (All/Stories/Surahs/Duas); selecting a chip re-issues the query with the `type` param and updates chip selected/unselected announcement state for accessibility.
- Render `SearchResultCard` grid with a small content-type badge per card (reusing A.3/A.5/A.6's existing iconography, per PRD §2.1).
- On zero results, render `EmptySearchState`: warm illustration + constructive suggestion copy (e.g., "Try searching for a Prophet's name or a feeling like 'kindness'") — content sourced from localization resources, never a raw technical string.
- Result-card tap: switch on `content_type`, navigate to the correct destination screen via `core-navigation` deep link into A.3/A.5/A.6.
- Apply standard entitlement/unlock checks at the destination screen (delegated, not reimplemented here).
- Offline state delegates to K-05 (Offline Search) rather than duplicating offline logic in this screen.

## 12. NextJS Requirements
N/A.

## 13. API Contract
`GET /v1/search?q=&type=` → `{ results: [{ content_id, content_type, title, thumbnail_url }], result_count }` per B-01 §13. Client never sends an `age_band`-shaped parameter (none exists in the request DTO).

## 14. Database Requirements
None directly — results are not cached to Room in this blueprint (K-05 handles the offline-content-index cache separately, which is a different dataset).

## 15. Validation
Client-side max-length guard on query text (200 chars, matching B-01) before submission — a UX guard, not a security control (server validates authoritatively).

## 16. Authentication
Relies on the app-wide child-session bearer token already attached by `core-network`'s HTTP client interceptor.

## 17. Authorization
N/A beyond standard session; destination-screen entitlement checks are each destination feature's own responsibility.

## 18. Error Handling
- Empty Search State renders **only** pre-written, localization-sourced copy — a UI test scans all text nodes on this screen against a blocklist of raw technical error terms (`"Exception"`, `"Error code"`, `"404"`, `"null"`) and asserts none are present, mirroring A.3's Media-Unavailable screen test pattern.
- API failure (non-zero-result error) → a distinct, non-alarming error state (not conflated with the friendly empty-results state) with a retry action.

## 19. Offline First
This screen delegates offline behavior entirely to K-05; when offline, `SearchResultsScreen` renders K-05's offline-results variant rather than attempting (and failing) a network call.

## 20. Local Data
None owned here.

## 21. Localization
Empty-state suggestion copy, filter-chip labels, and result-card type badges are all localized (English/Hindi/Arabic/Urdu) with no hardcoded strings.

## 22. RTL
Result grid mirrors correctly in RTL; filter-chip row order and card content-type badge position mirror per `core-designsystem` convention.

## 23. Analytics
`search_query_submitted` (with `input_method: "text"`, `query_length`), `search_results_shown` (`result_count`), `search_zero_results_shown`, `search_type_filter_applied`, `search_result_tapped` (`content_type`).

## 24. Performance
- Debounce prevents request-per-keystroke.
- Result-card grid uses lazy-loading (`LazyVerticalGrid`/equivalent) to avoid rendering all results eagerly on large result sets.
- Image loading (thumbnails) uses the existing app-wide image-loading pattern (caching, placeholder) — not reimplemented here.
- Stable/immutable state types to minimize recomposition on filter changes.

## 25. Security
No new security surface — results already server-filtered by B-01's hard age-band guarantee; client performs no additional filtering that could be mistaken for a security boundary.

## 26. Library Requirements
Jetpack Compose, Ktor (via `core-network`), Koin. No Retrofit/OkHttp (correcting the PRD's generic Android prompt).

## 27. Testing
- Unit: debounce logic with a virtual/test clock — assert only one search call fires after a rapid keystroke sequence followed by a pause.
- UI test: Empty Search State blocklist scan (§18).
- Parameterized UI test: result-card tap routes correctly for all three content types (`story`→Story Detail, `surah`→Surah Learning, `dua`→Dua Learning).
- UI test: filter-chip selected/unselected state correctly announced for accessibility.

## 28. Documentation
KDoc on `SearchRepository`/`SearchApi`; note on why debounce duration is 300–400ms (balances responsiveness vs. request volume).

## 29. AI Coding Agent Implementation Steps
**Task 01 — Implement SearchApi (Ktor)**
Objective: `GET /v1/search` client.
Files to create: `SearchApi.kt`.

**Task 02 — Implement SearchRepository**
Objective: interface + Ktor-backed impl.
Files to create: `SearchRepository.kt`, `SearchRepositoryImpl.kt`.

**Task 03 — Extend SearchViewModel with Debounced Query Handling**
Objective: 300–400ms debounce, results sub-state, loading/error/empty branching.
Files to modify: `SearchViewModel.kt`.
Tests: virtual-clock debounce test.

**Task 04 — Build Results UI Components**
Objective: `TypeFilterChipRow`, `SearchResultCard`, `EmptySearchState`, `SearchResultsSkeleton`, matching Figma "Search Results".
Files to create: component Composables.

**Task 05 — Implement Result Routing**
Objective: content-type-switched navigation into A.3/A.5/A.6's existing destinations.
Files to create/modify: navigation wiring in `SearchResultsScreen.kt`.
Tests: parameterized routing UI test.

**Task 06 — Add Empty-State Blocklist Test**
Files to create: `EmptyStateBlocklistUiTest.kt`.

**Task 07 — Wire Analytics Events**

**Task 08 — Final Review**
Objective: confirm no per-keystroke network calls in a manual/profiled check; confirm RTL and localization completeness.

## 30. Definition of Done
- Debounced search functional, one request per settled input.
- All three content types route correctly on tap.
- Empty state passes the blocklist scan.
- Full analytics event coverage.

## 31. Final Verification Checklist
- [ ] Only one network call fires after a rapid keystroke burst.
- [ ] Empty state never renders raw technical text — verified by automated scan.
- [ ] All three result types route to their correct destination — verified by parameterized test.
- [ ] Filter chips correctly announce selected state for accessibility.
- [ ] RTL grid mirroring verified.
- [ ] No hardcoded strings.
