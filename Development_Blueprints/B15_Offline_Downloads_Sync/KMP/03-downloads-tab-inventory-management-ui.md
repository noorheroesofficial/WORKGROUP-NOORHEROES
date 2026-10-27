# K-03 — Downloads Tab Inventory & Storage Management UI

## 1. Feature Context
Part of Feature B.15 (Offline Downloads & Sync). The primary child-facing surface for managing offline content — a tab within the shared `FavoritesAndDownloadsScreen` shell (sibling to B.14's Favorites tab).

## 2. Parent Feature
B.15 — Offline Downloads & Sync

## 3. Sub-feature
K-03 — Downloads Tab Inventory & Storage Management UI

## 4. Objective
Implement `DownloadsTabScreen` with a storage-used header, per-item progress/retry/remove, a "Clear All" flow with confirmation, and all required empty/loading/failed/license-expired states, fully usable offline.

## 5. Business Requirements
- FR-1: Downloads tab — download list, storage used vs. limit, remove, retry-failed, clear-all.
- FR-10: Clear All removes all downloads, frees storage, doesn't affect Favorites or progress history.
- FR-11: multiple downloads queue/process with resumable chunked transfer, each independently tracked for retry/failure.
- Edge Case 10: removing a single download while another is in progress affects only the targeted item.
- §1.12 Empty State: "Download a story to watch offline."
- §1.13 Loading States: per-item progress bar/percentage; skeleton shimmer on initial load.
- §1.14 Offline States: Downloads tab fully usable offline; storage-used reflects local device state directly.
- §2.2: states Default/Loading/In-progress-present/Failed-present/Empty/License-expired-present; accessibility — each row's state announced clearly, not color/icon alone; responsive — single-column mobile, 2-column tablet.

## 6. Existing Architecture
`DownloadsTabScreen` within the shared `FavoritesAndDownloadsScreen` shell (established by B.14); `DownloadsViewModel` exposing `StateFlow<DownloadsUiState>`, following the same ViewModel/Compose pattern as every other feature screen.

## 7. Existing Code to Reuse
- B.14's `FavoritesAndDownloadsScreen` shell and tab-switching scaffold.
- `core-designsystem`'s list-row/progress-indicator/confirmation-dialog primitives (similar density to A.7's Streak Calendar or A.11's Transaction History, per PRD §2.4).
- `core-analytics`'s `AnalyticsTracker`.
- K-02's `DownloadController`/`DownloadEntity` observation (`Flow<List<DownloadEntity>>`) as the primary offline-capable data source.
- `core-network`'s `ConnectivityObserver` for the online-refresh trigger only (not required for basic tab usability).

## 8. Files to Create
- `feature-downloads/src/commonMain/kotlin/.../downloads/DownloadsTabScreen.kt`.
- `feature-downloads/src/commonMain/kotlin/.../downloads/DownloadsViewModel.kt`.
- `feature-downloads/src/commonMain/kotlin/.../downloads/components/StorageUsedHeader.kt`.
- `feature-downloads/src/commonMain/kotlin/.../downloads/components/DownloadListRow.kt`.
- `feature-downloads/src/commonMain/kotlin/.../downloads/components/ClearAllConfirmationDialog.kt`.
- `feature-downloads/src/commonMain/kotlin/.../downloads/components/DownloadsEmptyState.kt`.
- `feature-downloads/src/commonMain/kotlin/.../downloads/components/DownloadsSkeleton.kt`.
- `feature-downloads/src/commonTest/kotlin/.../DownloadsViewModelTest.kt`.
- `feature-downloads/src/commonTest/kotlin/.../RemoveSingleDoesNotAffectOthersTest.kt`.

## 9. Files to Modify
- B.14's `FavoritesAndDownloadsScreen.kt` — mount `DownloadsTabScreen` in the Downloads tab slot (if not already stubbed).
- `DownloadsModule.kt` (Koin) — register `DownloadsViewModel`.

## 10. Backend Requirements
Consumes B-02 (`GET /v1/children/{id}/downloads`, `DELETE .../downloads/{content_id}`, `DELETE .../downloads`) for online refresh and remove/clear-all actions.

## 11. KMP Requirements
- Primary data source: `DownloadController`/`core-database`'s `Flow<List<DownloadEntity>>` — the tab renders correctly with **zero** network dependency (§1.14).
- Storage-used header computed directly from local `DownloadEntity` rows' `sizeBytes` sum, displayed against the cap fetched/cached from B-02's `storage_limit_bytes`.
- List row states: Default (thumbnail/title/type badge), In-progress (circular/linear progress + percentage), Failed (retry action), Complete (tap → offline playback), License-expired (re-download prompt, delegated to K-04).
- Retry action re-invokes `DownloadController.startDownload()` for the failed item, resuming rather than restarting (delegates to K-02).
- Remove action deletes only the targeted local file/`DownloadEntity` row and calls B-02's single-delete endpoint; verified not to affect any other in-progress download (Edge Case 10).
- "Clear All" → `ClearAllConfirmationDialog` → on confirm, removes all local files/`DownloadEntity` rows and calls B-02's clear-all endpoint; explicitly does **not** touch Favorites (B.14) local state.
- Empty state: friendly "Download a story to watch offline" illustration + copy, shown only when the list is genuinely empty (not during initial loading).
- Loading state: skeleton shimmer on first load only; subsequent refreshes use existing content with a subtle refresh indicator, not a full-screen skeleton replace.
- Responsive: single-column list on mobile, denser 2-column grid on tablet.
- Accessibility: each row's state (in-progress/failed/complete/expired) announced via a screen-reader-visible label, never relying on color or icon alone.
- Deep link `noorheroes://downloads` opens directly to this tab.
- Local "download complete" notification tap (from K-02) deep-links here.

## 12. NextJS Requirements
N/A.

## 13. API Contract
`GET /v1/children/{id}/downloads`, `DELETE /v1/children/{id}/downloads/{content_id}`, `DELETE /v1/children/{id}/downloads` — per B-02 §13.

## 14. Database Requirements
Reads/writes `core-database`'s `DownloadEntity` (K-02-owned) as the primary local source of truth; the B-02 API calls are best-effort server-side mirroring, not the tab's rendering dependency.

## 15. Validation
N/A (UI layer) — remove/clear-all are idempotent regardless of local/remote state drift (a remove-already-removed item is a silent no-op, matching B-02's idempotent `200` behavior).

## 16. Authentication
Relies on the app-wide child-session bearer token for the B-02 network calls; local `DownloadEntity` reads require no additional auth beyond the active child-mode session already gating the screen.

## 17. Authorization
N/A beyond standard child-session scoping (per-child data isolation is K-05's responsibility at the storage layer).

## 18. Error Handling
- Remove/clear-all network-call failure: local state still updates optimistically (file deleted, `DownloadEntity` row removed) with a background-retry sync to B-02 rather than blocking the UI action on network success — consistent with the platform's offline-first philosophy, since removing a local file is inherently a local-first action.
- Retry-failed-download failure: standard retriable error state on the row, not a full-screen error.
- Empty vs. error state clearly distinguished — a fetch/local-read error never renders as the friendly empty state.

## 19. Offline First
This screen is explicitly required to be fully usable offline (§1.14) — local `DownloadEntity` observation is the primary render path; the network calls are refresh/mutation-propagation only.

## 20. Local Data
`core-database`'s `DownloadEntity` (K-02-owned) is this screen's local data source.

## 21. Localization
All copy (empty state, storage-used text, row states, confirmation dialog) localized (English/Hindi/Arabic/Urdu), no hardcoded strings.

## 22. RTL
List/grid mirrors correctly; storage-used bar direction and row icon placement follow `core-designsystem` RTL convention.

## 23. Analytics
`downloads_tab_viewed`, `download_removed`, `downloads_cleared_all`, `download_completed` (observed transition), `download_resumed` (retry tap).

## 24. Performance
- `LazyColumn`/`LazyVerticalGrid` (per responsive breakpoint) for the download list to avoid eager rendering of large lists.
- Stable/immutable `DownloadsUiState` and row data classes to minimize recomposition during frequent progress updates from K-02.
- Storage-used sum computed reactively from the same `Flow` already being collected for the list, not a separate redundant query.

## 25. Security
No new security surface — per-child isolation enforced at the K-05/storage layer beneath this UI.

## 26. Library Requirements
Jetpack Compose, Koin. No new libraries.

## 27. Testing
- Unit: `DownloadsViewModel` state reduction across all required states (default/loading/in-progress/failed/empty/license-expired).
- **Isolation test (mandatory):** removing one download does not affect any other in-progress or complete download's state (Edge Case 10).
- UI test: empty state renders only when the list is genuinely empty, never during initial load.
- UI test: each row's state announced correctly for accessibility (no color-only encoding).
- UI test: responsive layout switches correctly between single-column and 2-column breakpoints.

## 28. Documentation
KDoc on `DownloadsViewModel` noting the local-first rendering philosophy and why network calls are refresh/mutation-only, not the rendering dependency.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Implement DownloadsViewModel**
Objective: `StateFlow<DownloadsUiState>` sourced primarily from `DownloadController`'s local `Flow`.
Files to create: `DownloadsViewModel.kt`.

**Task 02 — Build StorageUsedHeader Component**
Files to create: `StorageUsedHeader.kt`.

**Task 03 — Build DownloadListRow Component (all states)**
Files to create: `DownloadListRow.kt`.

**Task 04 — Build Empty & Skeleton States**
Files to create: `DownloadsEmptyState.kt`, `DownloadsSkeleton.kt`.

**Task 05 — Implement Remove & Clear-All Flows**
Files to create: `ClearAllConfirmationDialog.kt`.
Files to modify: `DownloadsViewModel.kt`.

**Task 06 — Assemble DownloadsTabScreen & Mount in Shell**
Files to create: `DownloadsTabScreen.kt`.
Files to modify: `FavoritesAndDownloadsScreen.kt`.

**Task 07 — Add Isolation Test (highest priority)**
Tests: `RemoveSingleDoesNotAffectOthersTest.kt`.

**Task 08 — Add Full Test Suite, Analytics, Deep Link Wiring**

**Task 09 — Final Review**
Objective: confirm the screen renders fully with airplane mode enabled (manual/automated offline-mode check).

## 30. Definition of Done
- `DownloadsTabScreen` live, fully offline-usable, all required states implemented.
- Remove/clear-all verified not to affect unrelated downloads or Favorites.
- Accessibility and responsive requirements verified.
- Full analytics coverage.

## 31. Final Verification Checklist
- [ ] Screen fully usable with no network connectivity.
- [ ] Storage-used figure accurate against local `DownloadEntity` sum.
- [ ] Removing one download never affects another — verified by test.
- [ ] Clear-all never touches Favorites local state.
- [ ] Each row's state announced via screen reader, not color/icon alone.
- [ ] Empty state distinguished from error state.
- [ ] Localization and RTL verified.
