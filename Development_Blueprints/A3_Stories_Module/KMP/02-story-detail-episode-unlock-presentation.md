# K-02 — Story Detail & Episode Unlock Presentation

## 1. Feature Context
The pre-playback commitment screen: cover, synopsis, scholar-approval badge, episode list with per-episode lock state and specific unlock-condition text, related stories. Must reflect unlock changes in real time on return (no app restart required) and never show a bare lock icon without explanation.

## 2. Parent Feature
Feature A.3 — Stories Module (Animated Storytelling System)

## 3. Sub-feature
2.2 Story Detail & Episode Unlock Presentation (ID: **K-02**)

## 4. Objective
Build the Story Detail screen and its ViewModel, reading B-01's detail endpoint (which already embeds server-computed `unlock_state`/`unlock_condition` per episode), with a real-time-on-resume refresh and full withdrawn-content/paywall handling.

## 5. Business Requirements
- FR-3: cover, synopsis, episode list, age/source/scholar-approval tags, related stories, per-episode progress.
- FR-5: locked episodes show the specific unlock-condition text server-supplied, never a generic lock icon.
- Acceptance Criteria: Episode 2 unlocks immediately (real-time, not requiring app restart) once Episode 1 crosses threshold.
- Accessibility: episode list items individually labeled with lock state read aloud ("Episode 3, locked, complete Episode 2 to unlock").

## 6. Existing Architecture
`feature:stories` module, extends K-01's `StoryCatalogRepository`/data layer with a detail-specific read; no separate module.

## 7. Existing Code to Reuse
- `feature/stories/data/StoryCatalogRepository.kt` (K-01, extend with `getStoryDetail(id)`)
- `core-navigation`: `Navigator`, `Route` (deep link `noorheroes://stories/{episode_id}`)
- `core-ui`: `LoadStateContent`, `ErrorView`
- `core-designsystem`: `NoorHeroesTheme`, progress-ring component if one exists elsewhere

## 8. Files to Create
- `feature/stories/ui/StoryDetailScreen.kt`
- `feature/stories/ui/EpisodeListItem.kt` (lock badge/unlock-condition tooltip, progress ring)
- `feature/stories/ui/ParentGatedPaywallCard.kt`
- `feature/stories/viewmodel/StoryDetailViewModel.kt` (+ State/Event files)
- `test/feature/stories/StoryDetailViewModelTest.kt`
- `androidTest/feature/stories/StoryDetailScreenTest.kt`

## 9. Files to Modify
- `core-navigation/Route.kt` — add `StoryDetailRoute(episodeId)`
- `feature/stories/data/StoryCatalogRepository.kt` — add `getStoryDetail(id)`

## 10. KMP Requirements
- `StoryDetailViewModel`: fetches detail on entry and again `onResume` (lightweight re-fetch, not a full screen reload) so unlock-state changes from a just-completed episode are reflected without navigating away and back.
- Episode list items render `unlock_state`/`unlock_condition` exactly as supplied by B-01 — no client-side re-derivation of unlock logic (the client never computes unlock state itself, only displays what the server says).
- Tier-gated (paywall) vs. simply-locked distinguished by response metadata — paywall renders `ParentGatedPaywallCard` routing to Parent PIN Gate → Subscription (A.14), plain-locked renders the lock badge + condition text with no navigation on tap.
- Withdrawn content: `410` response renders a "no longer available" state rather than a generic error.

## 11. Required API
**User API** — B-01 `GET /v1/content/{id}`.

## 12. Offline First
Cache-first read from K-01's `StoryCatalogCache` when offline (last-known detail + unlock state); a banner indicates data may be stale if offline, since unlock state is server-authoritative and could have changed.

## 13. Local Data
Reuses K-01's `StoryCatalogCache` — no separate local store.

## 14. Localization
English, Hindi, Arabic, Urdu — synopsis/unlock-condition text is server-supplied and already locale-resolved by B-01; UI chrome labels (buttons, tab names) sourced from shared localization resources.

## 15. RTL
Episode list, progress rings, and lock badges mirror correctly; hero-image/metadata two-column tablet layout mirrors column order in RTL.

## 16. Analytics
Emit `story_detail_viewed`, `episode_lock_viewed`, `episode_unlock_condition_tapped`, `paywall_card_shown` via `AnalyticsTracker`.

## 17. Performance
Progress-ring and lock-badge rendering must use stable state classes to avoid recomposition thrash on the `onResume` re-fetch (only re-render items whose unlock state actually changed, not the entire list).

## 18. Security
No client-side unlock computation exists anywhere on this screen — purely a display of server-supplied state, eliminating an entire class of client-side unlock-bypass risk.

## 19. Testing
- Unit: paywall-vs-locked branching logic, withdrawn-content `410` handling, resume-refresh triggering exactly once per resume (not on every recomposition).
- UI: lock badge + condition text rendering, paywall card navigation to Parent Gate, related-stories rail rendering.
- Accessibility: TalkBack reads "Episode 3, locked, complete Episode 2 to unlock" verbatim from server-supplied `unlock_condition` text.

## 20. AI Coding Agent Implementation Steps

**Task 01 — Add `StoryDetailRoute` and Deep Link**
Objective: Route + `noorheroes://stories/{episode_id}` deep link registration. Follow: existing `Route`/deep-link conventions. Definition of Done: route compiles, deep link resolves in a manual test.

**Task 02 — Extend `StoryCatalogRepository` with `getStoryDetail()`**
Objective: Detail read with cache-first-offline fallback. Dependencies: K-01. Tests: cache-fallback-when-offline test. Definition of Done: test passes.

**Task 03 — Implement `StoryDetailViewModel`**
Objective: Fetch-on-entry + lightweight resume-refresh, paywall/locked/withdrawn branching. Follow: `BaseViewModel`. Dependencies: Task 02. Tests: resume-refresh-fires-once, branching-logic tests. Definition of Done: tests pass.

**Task 04 — Implement `EpisodeListItem` Composable**
Objective: Progress ring, lock badge with server-supplied condition text, tap-to-play for unlocked episodes. Follow: `core-designsystem`. Dependencies: Task 03. Tests: accessibility content-description test. Definition of Done: TalkBack test passes with exact PRD-example phrasing pattern.

**Task 05 — Implement `ParentGatedPaywallCard`**
Objective: Tier-gated card routing to the existing Parent PIN/Biometric Gate → Subscription flow. Follow: existing parent-gate component from A.1/C.19 (reuse, do not rebuild). Dependencies: Task 03. Tests: navigation-target test. Definition of Done: test passes.

**Task 06 — Implement `StoryDetailScreen`**
Objective: Full screen composition — hero, synopsis, episode list, related rail, withdrawn-state handling. Dependencies: Tasks 03–05. Tests: UI tests per §19. Definition of Done: all states render correctly per fixture data.

**Task 07 — Add Analytics Instrumentation**
Objective: Four events per §16. Tests: fake-tracker assertions. Definition of Done: exactly one call site per event.

**Task 08 — Full RTL and Accessibility Pass**
Objective: Verify mirroring and TalkBack traversal. Tests: per §19. Definition of Done: snapshot baselines captured.

**Task 09 — Add Full Test Suite**
Objective: Complete coverage per §19. Definition of Done: all green.

**Task 10 — Final Code Review**
Objective: Confirm zero client-side unlock-logic re-derivation exists anywhere in this screen's code. Definition of Done: checklist in §21 checked.

## 21. Final Verification Checklist
- [ ] Locked episodes always show the specific server-supplied unlock-condition text, never a bare lock icon
- [ ] Episode 2 reflects unlock immediately on resume after completing Episode 1, no app restart needed
- [ ] Tier-gated content renders the paywall card, not a plain lock, and routes through Parent Gate
- [ ] Withdrawn content renders a "no longer available" state, not a generic error
- [ ] No client-side unlock-state computation exists anywhere in this screen
- [ ] TalkBack reads lock state + condition text correctly per accessibility requirement
- [ ] Full RTL mirroring verified
- [ ] All four analytics events fire correctly

## 22. Definition of Done
Story Detail accurately and immediately reflects server-authoritative unlock state, correctly distinguishes locked/paywalled/withdrawn content, and hands off cleanly to K-03 (Story Player) on unlocked-episode tap.
