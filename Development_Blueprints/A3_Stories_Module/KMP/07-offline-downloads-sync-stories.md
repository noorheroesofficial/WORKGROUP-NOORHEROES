# K-07 — Offline Downloads & Sync (Stories Scope)

## 1. Feature Context
Integrates `library:kmpplayer`'s `DownloadRepository` for Stories-specific offline playback, with per-`child_id` cache sandboxing so siblings sharing a device never cross-access each other's downloaded media, and a general-purpose offline-event sync outbox reused by K-04 and K-06.

## 2. Parent Feature
Feature A.3 — Stories Module (Animated Storytelling System)

## 3. Sub-feature
2.7 Offline Downloads & Sync (Stories Scope) (ID: **K-07**)

## 4. Objective
Build the Downloads Manager screen and sync infrastructure on top of `library:kmpplayer::DownloadRepository`, consuming B-08's unlock-aware manifest, scoping cache storage per `child_id`, and providing the offline-outbox mechanism K-04/K-06 depend on.

## 5. Business Requirements
- §6.7 Offline Support: downloaded episodes via Media3 `DownloadManager` with a custom `Cache` scoped per `child_id`; offline choice/quiz logic runs entirely client-side from the bundled `interactive_script`.
- Edge Case 4: two siblings share a device — Child A's downloads never exposed in Child B's Stories Library.
- Edge Case 7: parent disables downloads entirely while in-progress downloads exist → halted gracefully; already-completed downloads remain playable until offline access is additionally revoked (two distinct controls).
- §1.14 Offline States: Downloads category always available offline, fully functional.

## 6. Existing Architecture
`feature:stories` module, built directly on `library:kmpplayer::DownloadRepository` (per `CORE_KMP_PLAYER_INSTRUCTIONS.md` — never access `DownloadDao` directly, always go through `DownloadRepository`).

## 7. Existing Code to Reuse
- `library:kmpplayer::DownloadRepository` (`startDownload()`, `downloads: StateFlow`)
- `library:kmpplayer::cache` package (Media3 `DownloadManager`-backed caching)
- `core-datastore`: outbox pattern for offline-event sync (heartbeats, choices, completions)

## 8. Files to Create
- `feature/stories/ui/DownloadsManagerScreen.kt`
- `feature/stories/viewmodel/DownloadsManagerViewModel.kt` (+ State/Event files)
- `feature/stories/data/StoryDownloadRepository.kt` (wraps `library:kmpplayer::DownloadRepository` with a `child_id`-scoped cache-key prefix and manifest-driven episode selection)
- `feature/stories/data/OfflineEventOutbox.kt` (shared sync mechanism for heartbeats/choices/completions)
- `feature/stories/data/DownloadPolicyRepository.kt` (reads parent `allow_new_downloads`/`offline_access_revoked` flags)
- `test/feature/stories/StoryDownloadRepositoryTest.kt`
- `androidTest/feature/stories/child-isolation-cache-test.kt`

## 9. Files to Modify
- `core-navigation/Route.kt` — add `DownloadsManagerRoute`

## 10. KMP Requirements
- `StoryDownloadRepository.startDownload(childId, contentId)`: fetches B-08's manifest, calls `library:kmpplayer::DownloadRepository.startDownload()` per included episode with a cache key prefixed by `child_id` — this prefix is the sandboxing mechanism; verified by an explicit cross-child isolation test (Edge Case 4).
- Bundles `interactive_script` alongside the downloaded media package so K-04's choice/quiz overlays work fully offline.
- Resumable downloads: partial/failed downloads resumable via `library:kmpplayer::DownloadRepository`'s existing progress `StateFlow`, never restarted from zero.
- `DownloadPolicyRepository` exposes two independent flags: `allow_new_downloads` (gates starting new downloads — halting in-progress downloads gracefully, not silently failing, when flipped false mid-download) and `offline_access_revoked` (gates whether already-downloaded content remains playable — a separate, more severe control).
- `OfflineEventOutbox`: generic queue-and-sync mechanism for any Stories event that must work offline-first (heartbeats from B-03, choices from B-05, completion from B-04) — a single shared implementation rather than three bespoke queues, consumed by K-03, K-04, K-06.

## 11. Required API
**User API** — B-08 `POST /v1/downloads/manifest`.

## 12. Offline First
```
B-08 Manifest (unlock-aware, entitlement-checked)
    ↓
StoryDownloadRepository (child_id-scoped cache key)
    ↓
library:kmpplayer::DownloadRepository (Media3 DownloadManager)
    ↓
Local Cache (sandboxed per child_id)
    ↓
K-03 Player (prefers local KMPPlayerSource.Local when available)
```
`OfflineEventOutbox` handles the reverse direction: local event → queue → sync on reconnect, for heartbeats/choices/completions.

## 13. Local Data
- Per-child-scoped Media3 cache (via `library:kmpplayer::cache`, custom `Cache` key prefix).
- `OfflineEventOutbox`'s local queue (core-datastore or Room-backed, per existing outbox conventions elsewhere in the app).

## 14. Localization
Downloads Manager UI chrome (empty state, retry buttons, quality selector) sourced from shared localization resources.

## 15. RTL
Downloads list layout, progress indicators, and retry controls mirror correctly.

## 16. Analytics
Emit `story_download_started`, `story_download_completed`, `story_download_failed`, `story_download_removed` via `AnalyticsTracker`.

## 17. Performance
Download progress `StateFlow` collection must not block the UI thread; large download lists use `LazyColumn` with stable keys.

## 18. Security
- Cross-child cache isolation is a hard security/privacy requirement, not just a UX nicety — explicitly integration-tested (Edge Case 4).
- Downloaded media stored in app-sandboxed storage only, never exposed via shared/public storage paths (per PRD §12.4 Mobile Security).

## 19. Testing
- Unit: `allow_new_downloads` vs `offline_access_revoked` independence (flipping one never affects the other's behavior), resumable-download-not-restarted-from-zero logic.
- **Mandatory integration test**: Child B's player cannot resolve Child A's downloaded cache entries when both profiles exist on the same device (per PRD Android AI-prompt requirement #5).
- Integration: full offline flow — download a fixture episode → simulate airplane mode → play to completion → verify completion event queues locally with the correct `client_event_id` → simulate reconnect → verify exactly one sync call fires (per PRD Android AI-prompt requirement #10).

## 20. AI Coding Agent Implementation Steps

**Task 01 — Add `DownloadsManagerRoute`**
Objective: Route registration. Follow: existing `Route` pattern. Definition of Done: route compiles.

**Task 02 — Implement `DownloadPolicyRepository`**
Objective: Reads `allow_new_downloads`/`offline_access_revoked` as two independent flags. Follow: `core-network`/`core-datastore` conventions. Tests: independence test. Definition of Done: test passes.

**Task 03 — Implement `StoryDownloadRepository` with Child-Scoped Cache Keys**
Objective: Wraps `library:kmpplayer::DownloadRepository`, manifest-driven episode selection, `child_id`-prefixed cache keys. Dependencies: Task 02, B-08. Tests: cache-key-prefix correctness. Definition of Done: test passes.

**Task 04 — Implement Mandatory Cross-Child Cache Isolation Test**
Objective: Confirm Child B cannot resolve Child A's cached media on the same device. Dependencies: Task 03. Definition of Done: test passes and is registered as a required CI/regression check per PRD requirement.

**Task 05 — Implement `OfflineEventOutbox`**
Objective: Shared queue-and-sync mechanism for heartbeats/choices/completions. Follow: existing outbox conventions elsewhere in the app if any exist (reuse pattern, not necessarily the exact class). Tests: queue-then-sync-exactly-once test. Definition of Done: test passes, matches the PRD's "exactly one sync call fires on reconnect" requirement.

**Task 06 — Implement `DownloadsManagerViewModel` and Screen**
Objective: Download list, progress, retry, empty state ("Download a story to watch offline"), graceful halt on policy change. Dependencies: Task 03–05. Tests: graceful-halt-not-silent-failure test. Definition of Done: test passes.

**Task 07 — Wire `interactive_script` Bundling into Download Package**
Objective: Ensure choice/quiz data downloads alongside media for full offline K-04 functionality. Dependencies: Task 03. Tests: offline choice-overlay functional test using only downloaded data. Definition of Done: test passes.

**Task 08 — Implement Full Offline-to-Sync Integration Test**
Objective: Download → airplane mode → complete → reconnect → exactly one sync call, per PRD requirement #10. Dependencies: Task 05, K-03/K-06. Definition of Done: test passes.

**Task 09 — Add Analytics Instrumentation**
Objective: Four events per §16. Tests: fake-tracker assertions. Definition of Done: exactly one call site per event.

**Task 10 — Full RTL Pass**
Objective: Verify mirroring. Tests: RTL snapshot tests. Definition of Done: baselines captured.

**Task 11 — Add Full Test Suite**
Objective: Complete coverage per §19. Definition of Done: all green.

**Task 12 — Final Code Review**
Objective: Confirm no direct `DownloadDao` access exists anywhere (only via `DownloadRepository`), confirm the cross-child isolation guarantee holds under code review, not just the automated test. Definition of Done: checklist in §21 checked.

## 21. Final Verification Checklist
- [ ] Mandatory cross-child cache isolation test passes — Child B cannot access Child A's downloads
- [ ] `allow_new_downloads` and `offline_access_revoked` are independently controllable, verified by test
- [ ] Resumable downloads never restart from zero on retry
- [ ] `interactive_script` bundled with downloads — offline choice/quiz overlays fully functional
- [ ] Full offline-to-sync flow (download → airplane mode → complete → reconnect) results in exactly one sync call
- [ ] No direct `DownloadDao` access anywhere — exclusively via `library:kmpplayer::DownloadRepository`
- [ ] Downloaded media stored in app-sandboxed storage only
- [ ] All four analytics events fire correctly

## 22. Definition of Done
Offline downloads are unlock-aware, per-child sandboxed, policy-gated by two independent controls, and back a fully functional offline playback + choice + quiz + sync experience — providing the shared `OfflineEventOutbox` that K-03, K-04, and K-06 all depend on.
