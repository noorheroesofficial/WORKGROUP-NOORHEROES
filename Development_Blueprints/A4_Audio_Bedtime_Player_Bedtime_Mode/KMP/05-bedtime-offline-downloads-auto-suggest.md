# K-05 — Bedtime Offline Downloads & Auto-Suggest

## 1. Feature Context
Bedtime is a predictable, recurring evening-use need often on congested home wifi, so offline parity is a first-class requirement, not a fallback. This sub-feature reuses A.3's Media3 `DownloadManager`/offline-cache stack entirely, adding only Bedtime-category-specific proactive download prompting and the offline-state UX unique to K-01's screen.

## 2. Parent Feature
Feature A.4 — Audio Bedtime Player & Bedtime Mode

## 3. Sub-feature
2.5 Bedtime Offline Downloads & Auto-Suggest (ID: **K-05**)

## 4. Objective
Wire K-01's Bedtime Audio Player to A.3's existing offline-download/cache mechanism, add Bedtime-category "auto-suggest download" prompting (prompt-only, never silent auto-download), and implement the offline-state UX for no-content and next-episode-not-downloaded scenarios specific to this screen.

## 5. Business Requirements
- FR-11: download uses the same entitlement/parent-policy checks as A.3's download manifest endpoint; Bedtime category content is prioritized for "auto-suggest download."
- §1.8 NFR: full offline playback parity with online, since bedtime is a predictable recurring need best served by pre-downloaded content.
- §1.10 Edge Case 5: no internet + no pre-downloaded content → calm fallback message, never a hard error.
- §1.10 Edge Case 9: repeated streaming failures in a low-connectivity region → system may proactively prompt (not auto-execute) "Would you like to download tonight's story for offline listening?"
- §1.10 Edge Case 11: Next Episode unlocked but not downloaded, offline → clear "needs internet" message, not a silent failure or hanging network call.

## 6. Existing Architecture
A.3's Media3 `DownloadManager` and per-`child_id` offline-cache namespace already exist and are the sole download/cache mechanism for the app — this sub-feature is purely a consumer of that existing infrastructure from K-01's screen, adding zero new download plumbing.

## 7. Existing Code to Reuse
- A.3's `DownloadRepository` / Media3 `DownloadManager` wrapper (exact class name confirmed against A.3's KMP codebase — reuse directly, do not wrap a second time unnecessarily)
- A.3's `POST /v1/downloads/manifest` client (shared entitlement/parent-policy check call)
- A.3's Downloads Manager UI (for viewing/retrying downloads — Bedtime content download entries appear there, no separate Downloads Manager screen is built for this feature)

## 8. Files to Create
- `feature/bedtime-audio/offline/BedtimeDownloadSuggestionEngine.kt` — detects Bedtime-category content and low-connectivity streaming-failure patterns, surfaces (never auto-executes) a download prompt
- `feature/bedtime-audio/offline/BedtimeOfflineStateComponents.kt` — no-content fallback message, next-episode-not-downloaded notice, specific to K-01's visual/calm-mode style
- `test/feature/bedtime-audio/BedtimeDownloadSuggestionEngineTest.kt`
- `androidTest/feature/bedtime-audio/BedtimeOfflineStatesTest.kt`

## 9. Files to Modify
- `feature/bedtime-audio/player/BedtimeAudioViewModel.kt` (K-01) — prefer local downloaded source over network per A.3's existing source-selection pattern; surface offline states via `BedtimePlayerState.Unavailable`/dedicated offline variant

## 10. KMP Requirements
- Source selection: `BedtimeAudioViewModel` prefers `KMPPlayerSource.Local` (via A.3's DownloadManager cache) when available, falling back to network per the manifest's signed URL — identical selection logic to A.3/K-03, reused not reimplemented.
- `BedtimeDownloadSuggestionEngine`: flags content as Bedtime-category-eligible for proactive suggestion (from the manifest/catalog's existing category metadata); detects repeated streaming failures (a simple failure-count-over-window heuristic, confirm against any existing low-connectivity-detection utility elsewhere in the codebase before building a new one) and surfaces a one-time, dismissible "Would you like to download tonight's story for offline listening?" prompt — never a silent/automatic download regardless of this signal.
- No-content offline fallback: when offline with zero downloaded bedtime-eligible content, render a calm "no story available right now, here's a dua to read together" fallback (reusing A.5's dua-rendering component per K-04's pattern) rather than a blank screen or hard error.
- Next-episode-not-downloaded offline notice: tapping Next on an unlocked-but-undownloaded episode while offline shows a clear "needs internet to fetch this episode" message and does not attempt a network call that could hang — stays on the current episode.
- Download entitlement/parent-policy checks reuse A.3's `POST /v1/downloads/manifest` call exactly as-is — no new entitlement logic introduced here.

## 11. Required API
**User API** — `POST /v1/downloads/manifest` (shared, A.3).

## 12. Offline First
```
Downloaded Media (A.3's DownloadManager cache, per-child_id namespace)
    ↓
BedtimeAudioViewModel (prefers Local source, else Network from manifest)
    ↓
AudioPlayerController
    ↓
UI (offline-state components when applicable)
```

## 13. Local Data
No new local store — reuses A.3's existing Media3 `DownloadManager` cache database entirely.

## 14. Localization
Offline fallback messages and "needs internet" notices sourced from shared localization resources across EN/HI/AR/UR.

## 15. RTL
Offline-state components (fallback card, not-downloaded notice) mirror correctly for Arabic/Urdu, consistent with K-01's existing RTL handling.

## 16. Analytics
`BedtimeAnalytics`: `bedtime_download_started`, `bedtime_download_completed`, `bedtime_next_episode_not_downloaded_shown`, `bedtime_offline_no_content_shown`.

## 17. Performance
No new performance surface — reuses A.3's already-optimized download/cache mechanism; the suggestion-engine's failure-count heuristic is a lightweight in-memory counter, not a persisted/queried structure.

## 18. Security
No new security surface — download entitlement/parent-policy checks are exactly A.3's existing, unmodified logic.

## 19. Testing
- Unit: `BedtimeDownloadSuggestionEngine` — Bedtime-category detection, failure-count-threshold triggering, prompt-only behavior (assert no download call is ever made without explicit user confirmation, even when the suggestion condition is met).
- UI: no-content offline fallback renders the calm dua-fallback message, not a blank/error screen.
- UI: next-episode-not-downloaded notice renders correctly and does not attempt a network call (mocked offline state, assert zero network client invocations).
- Integration: full offline download → bedtime playback → sleep-timer-expiry → auto-pause flow with airplane mode enabled throughout (shared integration scenario with K-02).

## 20. AI Coding Agent Implementation Steps

**Task 01 — Wire K-01's Source Selection to A.3's DownloadManager Cache**
Objective: Prefer local downloaded source, fall back to network. Files to modify: `BedtimeAudioViewModel.kt` (K-01). Follow: A.3/K-03's exact source-selection pattern. Tests: source-preference test (local available vs. not). Definition of Done: test passes.

**Task 02 — Implement `BedtimeDownloadSuggestionEngine`**
Objective: Bedtime-category detection + low-connectivity heuristic, prompt-only surfacing. Files to create: `BedtimeDownloadSuggestionEngine.kt`. Tests: prompt-only-never-auto-download assertion; failure-count-threshold test. Definition of Done: tests pass.

**Task 03 — Implement Offline-State Components**
Objective: No-content fallback (reusing A.5's dua component per K-04), next-episode-not-downloaded notice. Files to create: `BedtimeOfflineStateComponents.kt`. Dependencies: K-04's dua-rendering reuse. Tests: fallback-renders-correctly UI test. Definition of Done: test passes.

**Task 04 — Wire Offline States into `BedtimePlayerState`**
Objective: Surface no-content/not-downloaded states through K-01's state machine, never a raw crash/blank screen. Files to modify: `BedtimeAudioViewModel.kt`. Dependencies: Task 02–03. Tests: state-transition tests for both offline scenarios. Definition of Done: tests pass.

**Task 05 — Add Analytics Instrumentation**
Objective: Four events per §16. Tests: fake-tracker assertions. Definition of Done: exactly one call site per event.

**Task 06 — Add Full Test Suite Including the Shared Airplane-Mode Integration Scenario**
Objective: Complete coverage per §19, coordinating with K-02's sleep-timer integration test for the combined offline+timer scenario. Definition of Done: all green.

**Task 07 — Final Code Review**
Objective: Confirm zero new download/cache plumbing was introduced (pure reuse of A.3); confirm the suggestion engine never auto-downloads without explicit confirmation. Definition of Done: checklist in §21 checked.

## 21. Final Verification Checklist
- [ ] Source selection prefers local downloaded content, falls back to network — identical logic to A.3/K-03
- [ ] `BedtimeDownloadSuggestionEngine` never triggers a download without explicit user confirmation
- [ ] No-content offline state renders a calm fallback (dua suggestion), never a blank/error screen
- [ ] Next-episode-not-downloaded offline tap shows a clear message, attempts zero network calls
- [ ] Full offline download → playback → sleep-timer-expiry → auto-pause flow verified under airplane mode
- [ ] Download entitlement checks reuse A.3's existing `POST /v1/downloads/manifest` unmodified
- [ ] All four analytics events fire correctly

## 22. Definition of Done
Bedtime Audio playback achieves full offline parity by reusing A.3's download infrastructure entirely, with Bedtime-specific proactive (prompt-only) download suggestions and calm, non-alarming offline-state handling for both no-content and next-episode-not-downloaded scenarios.
