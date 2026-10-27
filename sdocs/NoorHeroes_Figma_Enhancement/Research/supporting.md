# Supporting mobile feature research



Documentation only. No Figma/source changes. Scope B13–B18 and F35–F37 mobile impact.



All Search (5), Favorites (9), Child Profile (8), Facts (8), Ramadan Mode (21), and Deep Link Resolver (1) PNGs were visually opened: 52 image files. No admin images inspected. PRD product/UX inventories and related KMP behavior were inspected. Blueprint implementation/test claims are historical documentation, not current test evidence.



## Source excerpts and mandatory FR coverage



### B13

Source: `PRD_Documents/Child App Supporting (13-18)/Feature_B13_Search_Discovery.md`



### 1.7 Functional Requirements

**FR-1** Child Search UI sections: search bar with a voice option, recent searches, filtered results grid (story/lesson/dua), and an empty state (source: screen catalog "Search — UI Sections: Search bar with voice option, recent searches, filtered results grid (story/lesson/dua), empty state").
**FR-2** User actions: type or speak a query, apply a type/age filter, open a result (source: screen catalog "User Actions: Type or speak a query, apply type/age filter, open a result").
**FR-3** Search results are pre-filtered through the child-safe taxonomy; **no raw/unmoderated text ever renders** anywhere in the search UI — not in result titles, not in auto-suggestions, not in the empty state (source §6.11 — a hard, zero-exception rule).
**FR-4** The search index **excludes anything below the child's age band** — age-ineligible content is not merely de-prioritized in ranking, it is structurally absent from the index results returned for that child's session (source: navigation table — restated as a hard rule, not a ranking preference).
**FR-5** Child Search Detailed Workflow (source §6.11, items 1–5): (1) child types or speaks a query, (2) the query is normalized for language and passed through an age-safe query policy, (3) only published, age-eligible content is retrieved, (4) results are ranked by relevance, child level, parent settings, locale, and offline availability, (5) a safe, friendly empty state is shown for no-results queries — **never a raw "no results" error**.
**FR-6** Voice Search validation rules: an explicit microphone affordance is required (no ambient/always-listening search), parent permission is required, short retention or on-device processing is preferred, and **raw audio is not stored for model training by default** (source §6.11 Validation Rules — directly consistent with A.5's voice-data zero-retention principle, applied here to search specifically).
**FR-7** Admin search is a **separate, more powerful, non-age-restricted surface** supporting advanced filtering by tag, status, language, and review state — it is operator-only and must never be confused with or share a code path that could leak its unrestricted results into the child-facing search surface (source §6.11 Business Rules).
**FR-8** Search results route to the correct destination screen by content type: a story result opens Story Detail (A.3), a surah result opens Surah Learning (A.5), a dua result opens Dua Learning (A.6) (source: Search Flow diagram).
**FR-9** Search supports semantic/multilingual understanding — a query in the child's locale should surface relevant results even when the query phrasing doesn't exactly match indexed text (e.g., searching "the whale prophet" should surface Prophet Yunus content) (source: Feature Reference "Search System" features: "Semantic search... Multilingual understanding").
**FR-10** Recent searches are stored per-child (consistent with the platform's per-child, not-shared-across-siblings data-isolation principle established for Favorites/A.3) and are clearable by the child.
**FR-11** A parent-facing search surface exists separately within the Parent Area, allowing parents to search their own child's reports, stories, and habits (source: Feature Reference use case "Search child progress | Parent | Parent searches reports, stories, habits") — this is a distinct surface from child search, scoped to parent-session-authenticated data only.
**FR-12** Age eligibility for search results is recomputed automatically whenever a child's age changes (daily DOB-based recomputation, consistent with the platform's age-based content filtering system) — search never relies on a stale cached age band.



### 1.10 Edge Cases

1. A child's query exactly matches the title of a piece of content that exists but is below their current age band → the content is excluded from results entirely (not shown with a "not available yet" label) — the search index's age-band exclusion is a hard filter at the index/query layer, never a display-time suppression that could be bypassed by leaking the existence of ineligible content.
2. A child speaks a voice query that the transcription service interprets with low confidence → rather than searching for a likely-garbled transcription and returning confusing/irrelevant results, the system either asks the child to try again or falls back to a "did you mean..." simplified clarification, never silently searching a bad transcription and showing a friendly-looking but nonsensical empty state.
3. A child types a query containing language that would be inappropriate if echoed back verbatim → recent-searches storage and any aggregate "popular searches" admin reporting must pass through a content-safety filter before being persisted/displayed anywhere beyond the originating child's own device.
4. Two siblings share a device; recent searches must never carry over between child sessions (consistent with the platform-wide multi-child session-isolation rule) — switching from Child A to Child B must show Child B's own (or empty) recent-search history, never Child A's.
5. A query matches content across multiple types (e.g., "Yusuf" matches both a Prophet Yusuf story and a related dua) → results are grouped/filterable by type (FR-2) so the child isn't presented with an undifferentiated mixed list that's hard to scan.
6. The search backend experiences a partial outage (e.g., the semantic/ML ranking layer is down but basic keyword matching still works) → the system falls back to simpler keyword-based ranking rather than returning zero results or an error, consistent with the platform's general graceful-degradation philosophy (A.2/A.3).
7. A child searches while offline → search functions against the locally-cached/downloaded content index only, clearly indicating results are limited to downloaded content, rather than failing outright or claiming zero results when the issue is actually connectivity, not absence of matching content.
8. An Admin's search query is structured to closely resemble a child-search query format → the two surfaces are served by entirely separate API endpoints/services with separate auth scopes (per FR-7's hard separation requirement), so no input format similarity could cause cross-contamination between the unrestricted Admin index and the age-filtered child index.
9. A parent's Parent Area search query happens to match content terms that could also resolve in the child-facing catalog → the Parent Area search is scoped to the parent's own family's reports/progress/habit data, not the general content catalog.
10. A child's age-band recomputation (FR-12) happens to run mid-search-session → the currently-displayed result set is not abruptly mutated mid-view (avoiding a jarring "items disappearing" experience), but the next search query issued reflects the updated age band correctly.
11. A semantic search match surfaces content that is technically topically relevant but contextually less ideal for the current season (e.g., searching "Eid" outside Eid season) → ranking should sensibly favor currently-relevant seasonal content when an active seasonal mode is in effect, but should not hard-exclude non-currently-seasonal content, since year-round browsing of seasonal content is fine — a ranking-quality consideration, tunable by content/editorial teams, not a hard exclusion rule.
12. A voice search session is interrupted (e.g., a phone call comes in mid-recording) → the partial audio capture is discarded cleanly, no partial/garbled query is submitted, and the child is returned to the search bar in a normal, ready-to-retry state rather than a stuck "processing" state.



### 1.11 Error Handling

| Scenario | System Behavior |
|---|---|
| Zero results for a query | Friendly, safe empty state (FR-5) — never a raw "no results" error |
| Voice transcription low-confidence | Ask child to try again or offer a simplified clarification (Edge Case 2), never search a bad transcription silently |
| Search backend partial outage (ranking layer down) | Graceful fallback to simpler keyword matching (Edge Case 6) |
| Offline search | Scoped to locally-cached content index, clearly indicated as such (Edge Case 7) |
| Voice session interrupted | Partial audio discarded cleanly, search bar returns to ready state (Edge Case 12) |



### 1.12 Empty States
- Zero search results → friendly safe empty state with a suggestion (e.g., "Try searching for a Prophet's name or a feeling like 'kindness'") rather than a stark "no results."
- Zero recent searches yet (new child / cleared history) → recent-searches section simply omitted or shows a lightweight first-time hint, never an awkward empty list placeholder.



### 1.13 Loading States
- Search results: skeleton result-card shimmer while query processes.
- Voice search: a clear "Listening..." state during capture, then "Searching..." during processing — two distinct, honest states rather than one ambiguous spinner.



### 1.14 Offline States
- Search functions against the locally-cached/downloaded content index when offline (Edge Case 7), clearly labeled.



### 1.15 Permission States
- **Microphone (voice search):** explicit per-tap affordance, parent permission required (FR-6) — denied/unavailable microphone access falls back gracefully to text-only search with no nagging re-prompt beyond the platform-standard one-time OS re-prompt affordance.



### 1.18 Screen Inventory (Complete — Zero Missing)

| # | Screen | Type | Entry Points | Exit Points |
|---|---|---|---|---|
| 1 | Search Screen (landing, with recent searches) | Primary | Home search icon, any tab's search icon | Search Results |
| 2 | Voice Search — Listening State | Screen variant | Search Screen microphone tap | Search Results / Search Screen (retry) |
| 3 | Voice Search — Processing/Transcribing State | Screen variant | After Listening completes | Search Results / Clarification Prompt |
| 4 | Voice Search — Low-Confidence Clarification Prompt | Screen variant | Low-confidence transcription | Retry / Search Screen |
| 5 | Search Results (grid, filterable by type) | Screen | Query submission (text or voice) | Story Detail, Surah Learning, Dua Learning |
| 6 | Type Filter Selector | Component | Search Results | Filtered Search Results |
| 7 | Empty Search State (no results) | Screen variant | Zero-result query | Search Screen (retry) |
| 8 | Recent Searches List (component) | Component | Search Screen | Re-run a past query → Search Results |
| 9 | Clear Recent Searches Action | Component | Recent Searches List | Confirms → empty recent searches |
| 10 | Offline Search Results (cached-content-only) | Screen variant | Search Screen/Results, no connectivity | Story/Surah/Dua Detail (if downloaded) |
| 11 | Parent Area Search (reports/stories/habits) | Screen (Parent Area) | Parent Dashboard search entry | Relevant report/progress detail screen |
| 12 | Admin Search (advanced, operator-only) | Admin screen | Admin Portal nav | Content detail/editor (Admin context) |



Coverage: each FR above is retained as an exact requirement. B13 admin FR7; B17 admin campaign FR7; F35 architectural/evaluation/deployment FRs and F37 backend/admin FRs are non-mobile-screen constraints, excluded from design prompts but not omitted. FRs defining child safety, privacy, voice, gates, isolation and AI behavior apply to every consuming screen. F35/F37 create no dedicated mobile screen (§1.18).



### B14

Source: `PRD_Documents/Child App Supporting (13-18)/Feature_B14_Favorites.md`



### 1.7 Functional Requirements

**FR-1** Favorites screen UI sections: a saved-item grid and a type filter (source: screen catalog "Favorites — UI Sections: Saved item grid, type filter").
**FR-2** User actions: open a favorited item, remove it from favorites (source: screen catalog "User Actions: Open item, Remove from favorites").
**FR-3** Favoriting entry points are the "save" action available on Story Detail, Surah Learning, and Dua Learning detail screens (source: screen catalog "Entry Points: Profile, Story/Quran detail 'save' action").
**FR-4** **Favorites are strictly per-child, never shared across siblings** — each child has their own independent favorites list, with no UI surface anywhere (including Parent Area reports) that merges or displays favorites across multiple children as a combined view (source: navigation table — restated as a hard platform-wide data-isolation rule applied here).
**FR-5** A favorite toggle (add/remove) is idempotent and optimistic — toggling the same item rapidly never produces a duplicate favorite record or an inconsistent final state (consistent with the platform's general idempotent-toggle pattern established for habit favorites/check-ins elsewhere).
**FR-6** Favoriting an item is only possible for content the child already has access to — favoriting never bypasses age-band eligibility, entitlement, or unlock-state restrictions; the save action itself is simply unavailable (not erroring, just not offered) on content the child cannot already open.
**FR-7** If favorited content is later withdrawn or archived by Admin, the Favorites grid shows a clear "no longer available" state for that item rather than a broken link or silent disappearance, consistent with the platform-wide withdrawn-content handling pattern (A.3/A.6).
**FR-8** The Favorites grid supports filtering by content type (Stories/Surahs/Duas) consistent with FR-1, using the same type-iconography established in Search (B.13).
**FR-9** Favorites and Downloads (B.15) share a single screen shell with two tabs, reachable from the Profile tab; the two tabs are independently functional and do not share data models, only a UI container.



### 1.10 Edge Cases

1. A child favorites an episode within a series, and the series is later restructured/renumbered by Admin (a content-lifecycle edge case referenced in A.3 Edge Case 11) → the favorite reference resolves to the new canonical content ID rather than silently breaking, consistent with A.3's established resolution rule.
2. A child favorites an item, then their age band changes (birthday rollover) such that they would no longer be newly-eligible for that specific content type if encountering it fresh today → the existing favorite and its accessibility are **not retroactively revoked** — a child keeps access to and the favorited status of content they already had access to, consistent with the platform's general non-retroactive-restriction philosophy (distinct from a *new* search/browse encounter, which would respect current age-band filtering).
3. Two siblings share a device; switching from Child A to Child B mid-session → the Favorites grid must fully reset to Child B's own list with zero visual or data carryover from Child A's session, consistent with the platform-wide multi-child session-isolation rule (FR-4).
4. A child favorites the maximum reasonable number of items (a very large list, e.g., hundreds) → the Favorites grid paginates/lazy-loads gracefully rather than degrading performance or crashing; there is no hard cap on favorites count by product design (favoriting is free and low-stakes), but the UI must scale gracefully regardless.
5. A child attempts to favorite an item while offline → the action queues locally (optimistic update shown immediately) and syncs on reconnect, using an idempotent toggle request so a queued duplicate doesn't create an inconsistent state once synced.
6. A favorited item's content type changes its fundamental nature (an unusual content-lifecycle edge case, e.g., a piece of content is re-tagged from one content type to another by Admin) → the Favorites grid's type filter correctly reflects the item under its new type going forward, without leaving an orphaned reference under the old type filter.
7. A child taps "remove from favorites" on an item, then immediately re-taps "save" before the first request has confirmed (a rapid undo) → idempotent, last-tap-wins handling ensures the final state matches the child's actual last intended action without a race condition.
8. A parent, while in Parent Preview mode for a specific child (cross-ref A.3's Parent Story Insights pattern), views that child's favorited content as part of understanding their interests → this is a legitimate, single-child-scoped preview, not a violation of FR-4's per-child isolation rule (the isolation rule is about siblings never seeing each other's favorites, not about a parent never being able to see their own child's favorites in an appropriate context).
9. A child favorites an item that requires a specific download/offline package to actually play, and that item is later removed from the Downloads tab (B.15) for storage-management reasons → the favorite itself persists independently of download state; the favorited item simply requires connectivity again to play, consistent with favoriting and downloading being two independent, non-coupled actions on the same content item.



### 1.11 Error Handling

| Scenario | System Behavior |
|---|---|
| Favorite-toggle submission fails (network) | Optimistic local update already shown; retried via background sync, never shown as a child-facing error |
| Favorites grid fetch failure | Cached last-known list rendered with a staleness indicator, never a blank/broken screen |
| Favorited content withdrawn | Clear "no longer available" state per item (FR-7), never a broken link or crash |
| Favorite-toggle attempted on inaccessible content (a tampered/stale client state edge case) | Server rejects the toggle request with a graceful response; client re-syncs accessibility state |



### 1.12 Empty States
- Zero favorites yet → friendly "Tap the heart on any story, surah, or dua to save it here" guided empty state, consistent with the platform's general empty-state philosophy (A.3/A.6).



### 1.13 Loading States
- Favorites grid: skeleton card-grid shimmer while loading.



### 1.14 Offline States
- Favorites grid renders from cache fully offline; toggle actions queue and sync on reconnect (Edge Case 5).



### 1.15 Permission States
- No new runtime permissions specific to this feature.



### 1.18 Screen Inventory (Complete — Zero Missing)

| # | Screen / Component | Type | Entry Points | Exit Points |
|---|---|---|---|---|
| 1 | Favorites & Downloads Screen Shell (tabbed container, shared with B.15) | Primary | Profile tab | Favorites tab content / Downloads tab content |
| 2 | Favorites Tab (saved item grid + type filter) | Screen | Favorites & Downloads Screen Shell | Item Detail (Story/Surah/Dua) |
| 3 | Type Filter Selector (component, shared visual pattern with B.13) | Component | Favorites Tab | Filtered Favorites grid |
| 4 | Favorite Toggle (heart/save icon, component on detail screens) | Component | Story Detail, Surah Learning, Dua Learning | Inline state toggle, no navigation |
| 5 | Empty State — No Favorites Yet | Screen variant | Favorites Tab, zero favorites | Browse content (Stories/Learn tab) |
| 6 | "No Longer Available" Item State (component, within grid) | Component | Favorites Tab, withdrawn item | Dismiss / suggests browsing alternative |
| 7 | Offline Favorites Tab State | Screen variant | Favorites Tab, no connectivity | N/A (fully functional from cache) |



Coverage: each FR above is retained as an exact requirement. B13 admin FR7; B17 admin campaign FR7; F35 architectural/evaluation/deployment FRs and F37 backend/admin FRs are non-mobile-screen constraints, excluded from design prompts but not omitted. FRs defining child safety, privacy, voice, gates, isolation and AI behavior apply to every consuming screen. F35/F37 create no dedicated mobile screen (§1.18).



### B15

Source: `PRD_Documents/Child App Supporting (13-18)/Feature_B15_Offline_Downloads_Sync.md`



### 1.7 Functional Requirements

**FR-1** Downloads tab UI sections: download list, storage used vs. device/parent-set limit, remove action, retry-failed action (source: screen catalog "Favorites & Downloads — UI Sections: Two tabs — Favorites (liked content) and Downloads (offline manifest with storage used / device limit)"; "User Actions: Unlike, remove a download, retry a failed/incomplete download, clear all downloads").
**FR-2** Download Flow (canonical, source §7.10/§21.17, items 1–6): (1) verify entitlement and parent download policy, (2) request a signed manifest, (3) download resumable chunks with checksums, (4) encrypt or sandbox local media where the platform supports it, (5) store version, locale, expiry, and license terms locally, (6) refresh entitlement periodically — offline access is time-bounded, not indefinite.
**FR-3** Downloads are subject to a per-child download cap set by the parent (source: navigation table, "Downloads... Subject to per-child download cap set by parent") — attempting to download beyond the cap shows a clear "cap reached" message.
**FR-4** Offline Progress Flow (canonical, source §7.10/§21.17): write to local database first (offline-first) → queue immutable events with client-generated IDs → sync in causal order once connectivity returns → server deduplicates using idempotency keys → content progress uses the furthest-valid position; quiz attempts remain separately tracked.
**FR-5** Withdrawn content becomes unavailable after the next policy/entitlement refresh, while the child's safe progress history is preserved (source §7.10/§21.17 — the canonical rule this feature's entitlement-refresh mechanism enforces).
**FR-6** Interrupted/failed downloads resume with exponential backoff rather than restarting from zero (source: Offline Content Flow diagram).
**FR-7** License-expired downloads show a clear re-download prompt instead of silently failing (source: screen catalog navigation flow note).
**FR-8** Downloaded media is encrypted or sandboxed locally where the platform supports it (source §7.10/§21.17, item 4) — raw, freely-extractable media files are never left in an unprotected, generally-accessible device location.
**FR-9** Offline progress sync posts rewards exactly once per qualifying completion event via the same idempotency-key mechanism used platform-wide (A.11) — sync never produces duplicate XP/Noor Heroes Points regardless of how many times a client retries the sync call.
**FR-10** A "Clear all downloads" action removes all downloaded media for that child, freeing device storage, without affecting favorites (B.14) or server-side progress history — downloading and favoriting are independent, decoupled actions on the same content item.
**FR-11** Multiple downloads queue and process with resumable chunked transfer (not necessarily strictly serial — the platform may parallelize within reasonable concurrency limits), each tracked independently for retry/failure purposes.
**FR-12** Per-child download isolation: one child's downloaded content is never exposed to or accessible from a sibling's session on a shared device, consistent with the platform-wide multi-child isolation principle.



### 1.10 Edge Cases

1. A child downloads content, then their age band changes such that the content would no longer be newly-offered today → the existing download remains valid and playable, consistent with the platform's non-retroactive-restriction philosophy.
2. Two downloads are in progress simultaneously when the device loses connectivity → both pause cleanly and independently resume, never cross-contaminating each other's progress.
3. A child attempts to download content already fully downloaded → treated as a no-op (or "already downloaded" confirmation) rather than re-downloading from scratch or creating a duplicate manifest entry.
4. A parent reduces the per-child download cap below the amount already downloaded → existing downloads are not forcibly deleted, but no new downloads are permitted until usage drops back under the new cap.
5. A download's signed manifest URL expires mid-download → the client transparently requests a fresh signed manifest and resumes from the last successfully-downloaded chunk.
6. The same content item is requested for download by two different children on the same shared device → each child's download is stored in a separate, isolated namespace; the access-control layer enforces per-child isolation regardless of any underlying byte-level storage sharing.
7. A child generates many offline progress events over an extended offline period → on reconnect, the sync pipeline processes the full queued batch in correct causal order without overwhelming the server, using batched/paginated submission if needed.
8. A downloaded quiz/question-bank package references a question later withdrawn for safety reasons → per A.8 FR-11, the response is still recorded for history on sync but excluded from mastery/reward calculation; this engine's job is correct delivery/ordering, not the withdrawal-exclusion business logic itself.
9. A child's device runs out of storage mid-download → fails gracefully with a clear "not enough storage" message, distinct from a generic failure/retry message.
10. A child removes a single download while a different download is actively in progress → only the targeted item is affected; the in-progress download continues normally.
11. Parental controls disable downloads entirely for a child while existing downloads exist → existing downloads remain playable unless the parent has also explicitly revoked existing offline content (two distinct controls, consistent with A.3/A.4's pattern); only new download attempts are blocked.
12. A sync batch partially succeeds (e.g., 8 of 10 events sync before a connection drop) → the 2 unsynced events remain correctly queued locally and are retried on next reconnect, with the 8 already-synced events' idempotency keys preventing reprocessing if accidentally resubmitted.



### 1.11 Error Handling

| Scenario | System Behavior |
|---|---|
| Download interrupted | Resumes from last successful chunk with exponential backoff (FR-6) |
| Insufficient device storage | Clear "not enough storage" message, distinct from generic retry messaging |
| Signed manifest URL expires mid-download | Transparently re-requests a fresh manifest, resumes from last chunk |
| Per-child download cap reached | Clear "cap reached" message, no download begins (FR-3) |
| License/entitlement expired | Clear re-download prompt, never a silent failure (FR-7) |
| Offline sync batch partially fails | Unsynced events remain queued, retried on next reconnect (Edge Case 12) |
| Checksum validation failure | Chunk re-downloaded, never accepted as valid; overall download not marked complete until all chunks pass |



### 1.12 Empty States
- Zero downloads yet → friendly "Download a story to watch offline" guided empty state.



### 1.13 Loading States
- Downloads tab: per-item progress bar/percentage during active download; skeleton list shimmer on initial load.



### 1.14 Offline States
- The Downloads tab itself is fully usable offline; storage-used reporting reflects local device state directly.



### 1.15 Permission States
- Standard device storage access (no special runtime permission typically required for app-sandboxed storage on modern Android).



### 1.18 Screen Inventory (Complete — Zero Missing)

| # | Screen / Component | Type | Entry Points | Exit Points |
|---|---|---|---|---|
| 1 | Favorites & Downloads Screen Shell (tabbed, shared with B.14) | Primary | Profile tab | Downloads tab / Favorites tab content |
| 2 | Downloads Tab (download list + storage used) | Screen | Screen Shell | Item playback (offline), Remove/Retry |
| 3 | Storage Used / Device Limit Indicator | Component | Downloads Tab header | N/A |
| 4 | Per-Item Download Progress | Component | Downloads Tab, active download | Completed state |
| 5 | Download Cap Reached Message | Screen variant/Toast | Tap Download beyond cap | Dismiss |
| 6 | Download Failed — Retry Action | Component | Downloads Tab, failed item | Retry → resumes |
| 7 | Insufficient Storage Message | Screen variant/Toast | Download attempt, storage full | Dismiss |
| 8 | License/Entitlement Expired — Re-download Prompt | Screen variant | Open expired item | Re-download flow |
| 9 | Clear All Downloads Confirmation | Modal | "Clear All" action | Confirm/Cancel |
| 10 | Remove Single Download Action | Component | Downloads Tab, per item | Item removed |
| 11 | Empty State — No Downloads Yet | Screen variant | Downloads Tab, zero downloads | Browse content |
| 12 | Download Initiation Control | Component | Story Detail, Surah Learning, etc. | Download begins / Cap message |
| 13 | Parent Download Cap/Policy Configuration | Screen (Parent Area) | Parent Controls | Saves configuration |



Coverage: each FR above is retained as an exact requirement. B13 admin FR7; B17 admin campaign FR7; F35 architectural/evaluation/deployment FRs and F37 backend/admin FRs are non-mobile-screen constraints, excluded from design prompts but not omitted. FRs defining child safety, privacy, voice, gates, isolation and AI behavior apply to every consuming screen. F35/F37 create no dedicated mobile screen (§1.18).



### B16

Source: `PRD_Documents/Child App Supporting (13-18)/Feature_B16_Child_Profile.md`



### 1.7 Functional Requirements

**FR-1** Child Profile UI sections: avatar thumbnail, learning stats summary, language toggle, "Switch Profile" (PIN-gated to Parent Mode), Favorites/Downloads entry (source: screen catalog, restated verbatim as the canonical section list).
**FR-2** User actions: view stats, change display language, open Favorites/Downloads, request Parent Mode switch (source: screen catalog).
**FR-3** "Switch Profile" **always re-prompts the PIN/biometric gate** — there is no grace-window exception for this specific transition out of Child Mode, even though the Parent Area's own internal re-entry (once already in Parent Mode) may use a short configurable grace window per the platform's general re-gating rule; the **Child-Mode-to-Parent-Mode transition itself has zero grace-window exception** (source: screen catalog — restated as a hard rule for this specific transition; cross-ref C.19 for the grace-window mechanics that apply only *within* an already-unlocked Parent session).
**FR-4** **A child cannot see sibling stats from this screen** — the learning stats summary is strictly scoped to the active child's own session, with no UI path, query parameter, or navigation route from Profile that could expose another child's data (source: screen catalog; cross-ref the platform-wide "No Lateral Sibling Access" rule).
**FR-5** Learning stats summary is sourced from `GET /v1/children/{id}/progress` (source: screen catalog "Connected APIs") — this is the **same underlying progress data** the Mastery Engine (A.9) and Reward System (A.11) already compute, presented here in a condensed, child-friendly summary rather than recomputed independently.
**FR-6** The language toggle changes the **display language** only — it does not affect content availability/locale-eligibility (a separate concept governed by the platform's age/locale content-filtering system) and takes effect immediately without requiring an app restart.
**FR-7** Favorites and Downloads are reached from Profile as a single shared entry point into the tabbed "Favorites & Downloads" screen (B.14/B.15) — Profile itself does not duplicate that screen's content, only links to it.
**FR-8** The "Switch Profile" action's destination depends on what's selected next: tapping a different child avatar routes into that child's session (after the appropriate per-child lock, if configured, per A.1's Child Lock Screen); tapping "Parent Profile" routes into Parent Mode (always PIN/biometric gated, per FR-3); both paths route **through the Who Is Learning profile picker**, not directly (source: Profile Flow diagram — "Switch profile / go to Parent Area → Lock gate → Profile picker or Parent Dashboard").
**FR-9** Switching to another child's profile, or entering Parent Mode, **clears all previous child-sensitive UI state** before activating the new session (cross-ref A.1 §6.2 item 5) — Profile is one of the screens this clearing must visibly apply to, since it's a common transition point.
**FR-10** The "Edit avatar" action (where surfaced from Profile, per the platform's general avatar-customization entry points) deep-links into the Avatar screen (A.12) — Profile does not reimplement avatar customization itself.



### 1.10 Edge Cases

1. A child rapidly taps "Switch Profile" multiple times before the gate screen fully renders → idempotent handling ensures only one gate prompt is shown, not multiple stacked navigation pushes.
2. A child's progress summary data fails to load (network/service issue) → the rest of Profile (avatar, language toggle, navigation entries) still renders and functions; only the stats summary section shows a graceful "may be unavailable right now" state rather than blocking the entire screen.
3. A deep link (from a notification or elsewhere) attempts to land directly on a specific child's Profile stats while no active child session exists → per the platform-wide rule, it resolves through Who Is Learning first, never bypassing the profile-selection/lock gate (cross-ref A.1's general deep-link-resolution rule).
4. A parent successfully passes the Switch Profile gate, intending to enter Parent Mode, but then backs out/cancels before reaching the Parent Dashboard → the child's original session remains intact and active; canceling mid-transition never leaves the app in an ambiguous or logged-out state.
5. A child changes the display language, then immediately navigates to another tab (e.g., Home) → the new language applies consistently across that other tab too, not just Profile itself (since this is a global app-language setting, not a Profile-screen-local one).
6. Two children share a device; Child A's Profile is open, then the OS backgrounds/kills the app, and it's reopened later → the app must correctly re-resolve to whichever child's session was actually last active server-side (or require re-selection via Who Is Learning if the session has expired), never defaulting to a stale or incorrect child's Profile.
7. A child's age band changes (birthday rollover) while their Profile is open → the stats summary reflects updated, accurate values on next refresh; no special handling is needed beyond the platform's general daily age-recomputation job already covering this.
8. A child attempts to access Favorites/Downloads while offline → both function fully from cache (per B.14/B.15's own offline specs); Profile's entry point itself doesn't need special offline handling beyond simply still being tappable and routing correctly.
9. A parent has disabled a specific child's profile (cross-ref C.21's disable/re-enable pattern) while that child happens to be the currently active session at the moment of disabling (an unusual but possible race, e.g., a parent disabling from a second device) → the next API call from that child's session (including a Profile refresh) should gracefully detect the now-invalid/disabled session and route back to Who Is Learning rather than continuing to serve a session for a profile the parent just disabled.



### 1.11 Error Handling

| Scenario | System Behavior |
|---|---|
| Progress summary fetch fails | Graceful "may be unavailable right now" inline state on just that section; rest of Profile unaffected |
| Switch Profile gate fails (wrong PIN repeatedly) | Standard lockout/cooldown per A.1's Parent PIN error-handling pattern; original child session remains active throughout |
| Deep link attempts to bypass the gate | Resolved through Who Is Learning regardless, per the platform-wide deep-link rule |
| Disabled-session redirect detected mid-use | Graceful redirect to Who Is Learning, not a crash or a confusing error state |



### 1.12 Empty States
- New child, zero progress yet → stats summary shows a friendly first-time framing ("Start learning to see your progress here!") rather than a stark zero/blank state.



### 1.13 Loading States
- Profile screen: skeleton avatar/stats shimmer on initial load; subsequent visits use cached data with background refresh.



### 1.14 Offline States
- Profile renders from cached avatar/stats data when offline, with Favorites/Downloads entries remaining fully functional per their own offline specs; Switch Profile and language-toggle actions that don't require a network round-trip (the toggle itself is typically a local setting, synced when connectivity returns) remain usable.



### 1.15 Permission States
- No new runtime permissions specific to this feature.



### 1.18 Screen Inventory (Complete — Zero Missing)

| # | Screen / Component | Type | Entry Points | Exit Points |
|---|---|---|---|---|
| 1 | Child Profile Screen (landing) | Primary | Bottom nav "Profile" tab | Avatar, Favorites & Downloads, Switch Profile gate |
| 2 | Avatar Thumbnail (component, links to A.12) | Component | Child Profile Screen | Avatar Screen (A.12) |
| 3 | Learning Stats Summary (component) | Component | Child Profile Screen | N/A (display only) |
| 4 | Stats Summary — Unavailable State (component variant) | Component variant | Progress fetch failure | N/A |
| 5 | Language Toggle (component/modal) | Component | Child Profile Screen | Applies immediately, no navigation |
| 6 | Switch Profile Action (component) | Component | Child Profile Screen | Lock Gate |
| 7 | Lock Gate (PIN/biometric, shared with A.1) | Screen | Switch Profile Action | Who Is Learning (success) / Child Profile Screen (fail/cancel) |
| 8 | Favorites & Downloads Entry Point (component) | Component | Child Profile Screen | Favorites & Downloads Screen Shell (B.14/B.15) |
| 9 | First-Time / Zero-Progress Empty State (stats summary variant) | Component variant | Child Profile Screen, new child | N/A |
| 10 | Offline Child Profile State | Screen variant | Child Profile Screen, no connectivity | Functions from cache |
| 11 | Disabled-Session Redirect (implicit, no dedicated screen) | N/A (transition) | Any API call detecting a disabled session | Who Is Learning |



Coverage: each FR above is retained as an exact requirement. B13 admin FR7; B17 admin campaign FR7; F35 architectural/evaluation/deployment FRs and F37 backend/admin FRs are non-mobile-screen constraints, excluded from design prompts but not omitted. FRs defining child safety, privacy, voice, gates, isolation and AI behavior apply to every consuming screen. F35/F37 create no dedicated mobile screen (§1.18).



### B17

Source: `PRD_Documents/Child App Supporting (13-18)/Feature_B17_Notifications_Child_Facing.md`



### 1.7 Functional Requirements

**FR-1** Child-facing notification classes: approved learning reminder (daily reminder), bedtime story, streak-at-risk, new content, seasonal event, and the child-side copy of reward/milestone notifications (source §21.16, NoorHeroes Blueprint notification-use-case table — restated as the canonical child-facing class list).
**FR-2** Notification Flow (canonical, source §7.9 "Notification Flow" diagram): (1) a domain event or schedule creates a notification intent, (2) the policy engine checks consent, quiet hours, frequency budget, locale, entitlement, and device, (3) on pass, a template renderer produces parent-or-child-safe copy; on fail, the notification is suppressed, (4) a delivery adapter sends via FCM push or email, (5) a receipt event updates delivery analytics, (6) on open, the deep link **revalidates auth and content state**.
**FR-3** **Parent controls per-child reminders and quiet hours** — every reminder type is individually toggleable per child, and quiet-hours/bedtime windows are configured per child (source §21.16; cross-ref C.23).
**FR-4** **Maximum frequency and fatigue budgets are server-enforced** — never solely a client-side mute or a campaign-level setting that could be bypassed by an automated trigger path (source §21.16 — restated as a hard rule applying uniformly to every trigger source, scheduled or event-driven).
**FR-5** **Deep links validate session, child, content availability, and parent gate** — tapping any notification re-runs the exact same checks normal in-app navigation would, never granting a shortcut past any of them (source §21.16).
**FR-6** **Child notification copy contains no billing or sensitive analytics** — this is a template-authoring-time constraint enforced by content governance, not merely a convention (source §21.16, restated as a hard rule with zero exceptions, including for milestone/reward notifications that might otherwise be tempted to reference subscription tier or similar).
**FR-7** **Every campaign supports preview, test audience, schedule, cancel, and kill switch** (source §21.16) — applies to admin-authored campaigns layered on top of the automated trigger catalog (e.g., a seasonal-event push), not the purely automated triggers themselves, which are config-driven rather than campaign-authored.
**FR-8** **Firebase issues one token per app installation, not per child** — NoorHeroes implements per-child notification targeting through an **exclusive active-profile binding**: the installation token is bound to either the Parent Profile or exactly one selected child at any given time, with the binding atomically deactivated and reactivated on every profile switch (source: NoorHeroes Blueprint "Firebase Push Notification System" / "Firebase Notification Routing" — restated as the canonical architecture this feature's delivery layer depends on).
**FR-9** Two devices belonging to the same family may have **independent bindings** — e.g., one device actively bound to Child A while another device (or the same device at a different time) is bound to Child B or the Parent Profile; logout revokes all bindings for that session/device (source §7.9/NoorHeroes Blueprint, restated).
**FR-10** Every child-targeted notification passes a **server-side policy check against that child's `screen_time_policies`** (quiet hours/bedtime) before send — **client-side mute alone is never trusted** (source: NoorHeroes Blueprint "Quiet Hours & Bedtime" card — a hard rule).
**FR-11** Per-category daily/weekly frequency caps prevent notification fatigue; **engagement nudges back off automatically after repeated non-opens** (source: NoorHeroes Blueprint "Frequency Capping" card) — this auto-backoff is itself a server-side policy behavior, not a one-time static cap.
**FR-12** Specific trigger conditions (representative, source-confirmed): Daily reminder fires when the daily goal is not met by a configurable threshold hour; Streak risk fires on late-day inactivity with an active streak (e.g., "7PM with no activity and active streak"); Bedtime story fires 30 minutes before the configured bedtime; New content fires when new story/lesson content is published within the child's age/locale eligibility; Reward notifications fire when the Reward Service posts a ledger entry crossing a notify-worthy threshold (badge/level/weekly-challenge-completion); Seasonal notifications fire via an Islamic-calendar-date scheduling job (Ramadan mode activation, Eid content unlock) targeting the family (parent + active children).
**FR-13** In-app (non-push) notifications also exist for some triggers (e.g., "Tomorrow's episode is ready" on sequential-unlock-threshold-met) — these surface within the app's own UI (e.g., a Home banner) rather than as a device push, but still pass through the same policy engine for consent/eligibility purposes.



### 1.10 Edge Cases

1. A child's device switches profiles (Child A → Parent Profile) at nearly the same instant a streak-risk notification intent for Child A is being processed → the delivery adapter must check the binding's active status at actual send time, not just at intent-creation time, so a notification doesn't deliver to a binding that has since been deactivated; if the binding changed before send, the notification for Child A is held/redirected appropriately (e.g., delivered once Child A's binding is active again, or discarded if no longer relevant) rather than incorrectly delivered to whatever profile is now active on that device.
2. Two siblings share one device, and both have an active streak at risk on the same evening, but only one can be the "active profile" at any moment → each child's streak-risk evaluation and notification intent is independent and correctly scoped to whichever profile is active *at delivery time* for that specific device; if Child B's profile is active when Child A's streak-risk notification would otherwise fire on this shared device, the system does not deliver Child A's notification to this device at all in that moment (it may still be eligible for delivery via a different family device bound to Child A, if one exists, per FR-9's independent-bindings rule).
3. A child's bedtime window spans midnight (cross-ref A.4's bedtime-window edge case) → the bedtime-story trigger's "30 minutes before bedtime" calculation must correctly handle a bedtime window crossing midnight, consistent with A.4's established midnight-crossing-window logic.
4. A new content item is published, but by the time the New Content notification's delivery actually processes, the content has been very quickly withdrawn (a rare but possible race) → the policy engine's "content availability" check (part of FR-5's deep-link validation, but also relevant at send-time for this specific trigger) should prevent sending a notification promoting content that's no longer available; if the notification was already sent before withdrawal, the deep link's own revalidation-on-open will gracefully handle the now-unavailable content rather than crashing.
5. A child taps a notification while their device has no connectivity → the deep link's revalidation requires connectivity for the actual session/content checks; the app should show a clear "reconnect to open this" state rather than a confusing partial navigation or crash.
6. A parent changes a child's quiet-hours configuration while a notification intent for that child is already queued (created before the change, not yet sent) → the policy engine should re-evaluate against the **current** quiet-hours configuration at actual send time, not the configuration that was active when the intent was created, ensuring a parent's just-made change takes effect immediately rather than after a stale intent already in the queue.
7. A child's streak transitions out of an "at risk" state (e.g., they complete the qualifying activity) after a streak-risk notification intent was created but before it was sent → the notification should be canceled/suppressed rather than sent with now-inaccurate "your streak is at risk" messaging, since the underlying condition is no longer true.
8. A device is shared and currently has no active profile binding at all (e.g., immediately after a logout, before any profile is re-selected) → no child- or parent-targeted notification is deliverable to this device until a new binding is established; this is the expected, safe default state, not an error condition.
9. An admin-authored seasonal campaign (e.g., Ramadan mode activation) targets "family-wide (parent + active children)" → this must correctly resolve to delivering an appropriately-worded version to the parent's binding AND to each currently-active child's binding across however many devices the family has, respecting each binding's own policy checks independently (a child's own quiet-hours still apply to their copy of a family-wide campaign).
10. A push token becomes invalid (e.g., app uninstalled, token rotated by the OS) → the Lifecycle stage of the routing pipeline (FR-8's architecture) must detect and remove invalid tokens, refresh rotated ones, and avoid repeatedly attempting delivery to a dead token, consistent with standard FCM lifecycle management.
11. A child's age-band/eligibility changes (birthday rollover) between when a "New Content" notification intent was created (content was eligible) and when it's actually sent → the eligibility should be re-checked at send time using the child's current age band, not the age band at intent-creation time, consistent with the platform's general "always use current, not stale, eligibility" principle.



### 1.11 Error Handling

| Scenario | System Behavior |
|---|---|
| Active profile binding changes between intent creation and send | Binding status re-checked at send time; notification held/redirected/discarded as appropriate, never misdelivered (Edge Case 1) |
| Notification deep link tapped offline | Clear "reconnect to open this" state, never a crash or confusing partial navigation |
| Quiet-hours/eligibility configuration changes after intent creation, before send | Re-evaluated against current configuration at send time, not stale intent-creation-time configuration (Edge Case 6) |
| Underlying trigger condition resolves before send (e.g., streak no longer at risk) | Notification intent canceled/suppressed (Edge Case 7) |
| Push token invalid/expired | Detected and removed by the Lifecycle stage; no repeated delivery attempts to a dead token |
| Content withdrawn after a promoting notification already sent | Deep-link revalidation on open gracefully handles unavailable content, consistent with the platform's withdrawn-content UX pattern |



### 1.12 Empty States
- No notification history yet (new child) → N/A for push notifications themselves; any in-app notification-history list (if surfaced to the child at all, which is more typically a parent-area concept) would show a simple "nothing yet" state.



### 1.13 Loading States
- Deep-link revalidation on open: a brief loading state while session/child/content checks complete, before landing on the resolved destination.



### 1.14 Offline States
- Deep links tapped offline show a clear reconnect prompt (Edge Case 5); the underlying notification itself was still delivered via FCM's own offline-queuing behavior at the OS level, which is outside this feature's direct control but compatible with it.



### 1.15 Permission States
- **Notification permission (OS-level):** if denied, the child simply doesn't receive push notifications; in-app banner-style notifications (FR-13) remain unaffected since they don't require this permission. No special in-app re-prompt nagging beyond the platform-standard one-time OS re-prompt affordance.



### 1.18 Screen Inventory (Complete — Zero Missing)

| # | Screen / Component | Type | Entry Points | Exit Points |
|---|---|---|---|---|
| 1 | OS Push Notification (system-rendered, not an app screen) | System | FCM delivery | Tap → Deep Link Resolution |
| 2 | Deep Link Resolution — Loading State | Screen variant | Notification tap | Resolved destination screen |
| 3 | Deep Link Resolution — Offline/Reconnect Prompt | Screen variant | Notification tap, no connectivity | Retry → resumes resolution |
| 4 | Deep Link Resolution — Session/Lock Gate (if required) | Screen (shared with A.1) | Deep link requiring re-auth | Resolved destination screen / Who Is Learning |
| 5 | Deep Link Resolution — Content Unavailable Fallback | Screen variant | Deep link to withdrawn/unavailable content | Suggested alternative / Home |
| 6 | In-App Notification Banner (e.g., "Tomorrow's episode is ready") | Component | Home or relevant feature screen | Relevant content destination |
| 7 | Bedtime Story Notification Destination (A.4 Bedtime Player) | Screen (A.4) | Bedtime Story notification tap | N/A (A.4's own flow) |
| 8 | Streak-Risk Notification Destination (A.7 Habit Builder) | Screen (A.7) | Streak Risk notification tap | N/A (A.7's own flow) |
| 9 | New Content Notification Destination (relevant content detail) | Screen (A.3/A.5/A.6) | New Content notification tap | N/A (destination feature's own flow) |
| 10 | Reward/Milestone Notification Destination (A.11 Rewards Wallet/Achievements) | Screen (A.11) | Reward notification tap | N/A (A.11's own flow) |
| 11 | Parent Per-Child Reminder/Quiet-Hours Configuration (Parent Area, cross-ref C.23) | Screen (Parent Area) | Parent Controls | Saves configuration |



Coverage: each FR above is retained as an exact requirement. B13 admin FR7; B17 admin campaign FR7; F35 architectural/evaluation/deployment FRs and F37 backend/admin FRs are non-mobile-screen constraints, excluded from design prompts but not omitted. FRs defining child safety, privacy, voice, gates, isolation and AI behavior apply to every consuming screen. F35/F37 create no dedicated mobile screen (§1.18).



### B18

Source: `PRD_Documents/Child App Supporting (13-18)/Feature_B18_Islamic_Facts_Module.md`



### 1.7 Functional Requirements

**FR-1** Each fact stores: fact text by locale and age band, topic and related-content linkage, primary and secondary source references, scholar approval and version, an explanation, a linked quiz item, and jurisprudential-scope/exclusion notes where relevant (source §21.9 — restated verbatim as the canonical, complete data-field list for this content type).
**FR-2** Fact cards display: age band, topic, source, scholar approval, explanation, related story, and quiz (source: NoorHeroes Blueprint "Islamic Facts" card — restated as the canonical display contract).
**FR-3** **Disputed/jurisprudentially-sensitive topics stay out of child-facing auto-generation** — no fact touching contested fiqh matters may be produced via AI generation for child-facing display; such topics, if covered at all, require full human scholar authorship with explicit jurisprudential-scope notes, never an AI-drafted starting point (source: NoorHeroes Blueprint — restated as a hard, zero-exception rule).
**FR-4** **Spaced repetition resurfaces forgotten facts** — Islamic Facts is a participating domain in the shared Mastery Engine's (A.9) cross-domain spaced-repetition scheduler, subject to the same global daily-prompt cap as Quran/Arabic/Tajweed (source: NoorHeroes Blueprint; cross-ref A.9 FR-8/§5 item 5).
**FR-5** The Home "Islamic Fact of the Day" card (A.2's existing widget) is this module's primary surface; this document owns the fact-content data model and detail/quiz flow that the Home card links into, not a duplicate of Home's own card-rendering logic.
**FR-6** Each fact's `explanation` field must be distinct from its `fact text` — the card states the fact, and a deeper explanation (available via tap-through to Fact Detail) provides the "why," consistent with the platform's general "teach the reasoning, not just the answer" pedagogy already established in A.8's Per-Answer Explanation pattern.
**FR-7** A fact's linked quiz item routes through the shared Quiz Engine (A.8) using the same five-question-type contract, parameterized for this context (typically 1 question per fact, consistent with the brevity of a single fact) — this module does not implement a parallel quiz mechanism.
**FR-8** Facts are deduped against a child's own recently-seen history (consistent with A.5 §1.7 FR-13's "no repeat within a rolling 30-day window where catalog size allows" rule, restated here as this module's own deduplication policy) before being selected as "today's fact."
**FR-9** A fact's `related_content` linkage (to a Story, Surah, or Dua) must reference real, currently-eligible content for the requesting child — a stale/withdrawn related-content reference is excluded from display rather than producing a broken link, consistent with the platform-wide withdrawn-content handling pattern.
**FR-10** Facts surfaced during an active seasonal mode (Ramadan/Eid) are weighted toward seasonally-relevant topics where available, consistent with the platform's general calendar-aware recommendation principle (cross-ref A.2's Islamic-calendar-event reason codes), without hard-excluding non-seasonal facts from selection eligibility.
**FR-11** Scholar approval records are versioned (consistent with the platform's content-versioning pattern established in A.3/A.5/A.6) — editing a fact's text/explanation/sources creates a new version requiring fresh scholar sign-off before it can replace the currently-published version; children always see the latest *published* (approved) version, never a draft.



### 1.10 Edge Cases

1. A child's age band changes (birthday rollover) and the previously-shown "today's fact" text version was age-band-specific → on next fact selection, the system correctly resolves to the age-band-appropriate text variant for the child's new band, without needing any special migration (since fact text is already locale/age-band-keyed per FR-1).
2. The fact catalog for a child's specific age band/locale combination is very small (e.g., a newly-added locale with few facts so far) → the dedup window (FR-8) gracefully relaxes (e.g., allowing repeats sooner) rather than failing to produce a "fact of the day" at all, consistent with the general "fall back to a sensible default rather than show nothing" principle established elsewhere (A.5 Edge Case 1).
3. A fact's linked quiz item references a question that is later withdrawn for safety reasons → consistent with A.8 FR-11/A.9 FR-10, any already-recorded response is preserved for history but excluded from mastery/reward calculation; this module's own responsibility is simply to stop offering that quiz link until a replacement exists.
4. Two facts on closely related topics could each independently qualify as "today's fact" on the same day across different surfaces (e.g., Home's daily card and a spaced-repetition resurfacing prompt elsewhere) → this is acceptable, consistent with A.9's general "repetition across distinct contexts has its own spaced-repetition value" principle (A.9 §1.10 Edge Case 6), though the selection logic should avoid showing the *exact same* fact instance twice within the same day across surfaces for a single child.
5. A scholar revokes approval on a fact version that a child has already seen and engaged with (quiz answered, etc.) → consistent with the platform's general non-retroactive-revocation principle, the child's historical engagement/mastery-evidence record from that interaction is preserved; only future selection eligibility is affected.
6. A fact's `related_content` was valid at content-authoring time but the underlying Story/Surah/Dua content item is later restructured (e.g., a series renumbering, per A.3 Edge Case 11) → the related-content reference resolves to the new canonical content ID rather than breaking, consistent with the platform's established content-restructuring resolution rule.
7. A child encounters the Fact of the Day during an active Ramadan seasonal mode, but the day's seasonally-weighted selection pool happens to be exhausted (all seasonal facts already shown this season) → falls back gracefully to the general (non-seasonal-weighted) selection pool rather than failing to produce a fact.
8. An admin attempts to mark a fact as approved without an actual scholar-review record attached (a process/tooling-bypass attempt) → rejected by the admin tooling's validation, consistent with the platform's established content-governance pattern (A.3/A.5/A.6's scholar-approval gates).
9. A child offline encounters a "Fact of the Day" that was cached before going offline, then later (still offline) tries to access the linked quiz which requires the Quiz Engine's online question-set assembly → if the question bank wasn't pre-downloaded, the quiz link shows a clear "needs internet" state rather than a silent failure, consistent with the platform's general offline-content-availability messaging pattern.



### 1.11 Error Handling

| Scenario | System Behavior |
|---|---|
| Fact-of-the-Day selection service fails | Falls back to a cached/default evergreen fact rather than showing no fact at all, consistent with A.2's general per-section graceful-degradation pattern |
| Fact Detail fetch fails | Cached last-known data shown with a staleness indicator, or a friendly retry state if no cache exists |
| Linked related-content reference is withdrawn/stale | That specific link omitted gracefully (FR-9), rest of Fact Detail unaffected |
| Linked quiz question withdrawn | Quiz link removed/hidden until a replacement exists (Edge Case 3) |
| Scholar approval revoked on the currently-displayed fact mid-session | The child's already-open view is not abruptly altered mid-view; only future selections are affected, consistent with the platform's general non-disruptive-mid-session-change principle |



### 1.12 Empty States
- A locale/age-band combination with zero published facts yet → Home's Fact of the Day card simply omits itself for that session (consistent with A.2's per-section graceful-omission pattern) rather than showing an empty/broken card.



### 1.13 Loading States
- Fact Detail: skeleton card shimmer while loading.



### 1.14 Offline States
- A previously-cached Fact of the Day remains viewable offline; the linked quiz requires connectivity unless its question data was separately pre-downloaded (Edge Case 9).



### 1.15 Permission States
- No new runtime permissions specific to this feature.



### 1.18 Screen Inventory (Complete — Zero Missing)

| # | Screen / Component | Type | Entry Points | Exit Points |
|---|---|---|---|---|
| 1 | Islamic Fact of the Day Card (Home widget, owned by A.2, content sourced here) | Component | Home | Fact Detail |
| 2 | Fact Detail Screen | Screen | Fact of the Day Card, spaced-repetition resurfacing prompt, related-content linkage from elsewhere | Related Content (Story/Surah/Dua), Linked Quiz |
| 3 | Linked Quiz (shared A.8 instance, 1 question) | Screen (A.8) | Fact Detail | Quiz Completion Result (A.9) |
| 4 | Related Content Link (component, within Fact Detail) | Component | Fact Detail | Story Detail / Surah Learning / Dua Card Detail |
| 5 | Spaced-Repetition Resurfacing Prompt (shared component pattern, cross-domain with A.5/A.9) | Component | Skill Tree / Home, cross-domain capped | Fact Detail |
| 6 | Scholar-Approval Indicator (component, within Fact Detail) | Component | Fact Detail | N/A (display only) |
| 7 | Empty/Omitted State (Home card, zero eligible facts) | N/A (absence of component) | N/A | N/A |
| 8 | Offline Fact Detail (cached) | Screen variant | Fact Detail, no connectivity | Quiz link shows "needs internet" if not pre-downloaded |



Coverage: each FR above is retained as an exact requirement. B13 admin FR7; B17 admin campaign FR7; F35 architectural/evaluation/deployment FRs and F37 backend/admin FRs are non-mobile-screen constraints, excluded from design prompts but not omitted. FRs defining child safety, privacy, voice, gates, isolation and AI behavior apply to every consuming screen. F35/F37 create no dedicated mobile screen (§1.18).



### F35

Source: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F35_AI_Layer_Microservices_Architecture.md`



### 1.7 Functional Requirements

**FR-1** AI Microservices Architecture (canonical, source NoorHeroes Blueprint, five services with explicit controls):
- **Recommendation Service** — ranks stories, lessons, habits, missions, and next-best actions. Controls: uses age, language, progress, parent preferences, and safety tags.
- **Narration Service** — generates or selects tone-aware narration variants and subtitle translations. Controls: approved voices, bedtime limits, **no child voice cloning without explicit consent**.
- **Learning Service** — adapts Quran, Arabic, dua, and quiz difficulty to mastery level. Controls: **separates educational hints from religious rulings**.
- **Moderation Service** — filters prompts, outputs, search, admin content, and child-generated text. Controls: audit logs, remote kill switch, parent review, admin queue (cross-ref E.30's full specification of this service's console/queue surface).
- **Insights Service** — creates parent reports, habit analytics, growth insights, and recommendations. Controls: privacy-preserving aggregation; child PII minimized.
**FR-2** **AI Rule: AI should increase trust, not risk** (source — the governing design principle every service above must satisfy; restated as the ceiling principle already operationalized in C.23 FR-7 for parent-controllable settings, here extended to the underlying services' own default behavior).
**FR-3** **Scholar-Reviewed AI Responses: religious answers must map to approved knowledge cards. Anything about rulings, aqeedah, halal/haram, prayer, or fiqh receives stricter confidence thresholds and review paths** (source — restated, shared verbatim with E.30 FR-2, since this is the Learning/Recommendation Services' actual behavioral contract, not merely a moderation-console concern).
**FR-4** **Child-Safe Moderation: the AI layer blocks unsafe topics, refuses sensitive conversations, strips personal data, and offers warm redirects suitable for children** (source — restated, shared with E.30 FR-3).
**FR-5** **Religious rulings with legitimate scholarly difference of opinion are never improvised by the model — these route to an approved-answer set or a scholar handoff. Every response cites its approved source content in the parent/admin-visible history. The AI must never claim to be human, a scholar, or "a friend who keeps secrets," and must never encourage emotional dependency** (source §12.2 — four distinct, hard behavioral rules governing every AI service's output).
**FR-6** **Model output is never published as permanent curriculum content without passing through the standard human review pipeline** (source §12.2 — restated as the requirement that AI-generated content (e.g., a Recommendation Service's suggested next story, if ever authored rather than merely ranked from existing approved content) cannot bypass E.29's content CMS review chain).
**FR-7** **Voice Q&A and Pronunciation Coaching: push-to-talk only — never an always-listening microphone. Recording state is always visibly displayed to the child. Process the minimum necessary audio for the task. Raw audio is deleted after response/scoring by default; derived scores are stored only when useful and consented to. Parents can disable voice features globally or on a per-child basis** (source §12.3 — restated as the Narration/Learning Services' canonical voice-handling contract, the architectural origin point of A.5's own voice-recording guarantees).
**FR-8** **AI may summarize (Insights Service): consistency, skill strengths and refresh needs, story themes enjoyed, healthy usage, suggested next activity. AI must not: diagnose developmental, behavioral, or religious conditions; compare siblings; infer sensitive traits; present uncertain conclusions as settled facts** (source §12.4 — restated, shared verbatim with C.20/C.22's Content Safety Validator scope).
**FR-9** **Evaluation & Safety Gating: maintain ongoing test suites for age appropriateness, Islamic factuality against the approved corpus, refusal correctness, citation correctness, PII leakage, toxicity/unsafe-advice detection, multilingual consistency, pronunciation-scoring bias across accents, and recommendation diversity. Release gate: every model or prompt change requires offline evaluation, reviewer sign-off for high-risk features, a canary release, and a defined rollback path before reaching general availability** (source §12.5 — the complete, canonical evaluation-suite taxonomy and release-gate process, of which E.30's Evaluation Harness is the operational implementation).
**FR-10** **Architecture style: modular monolith at launch**, extracted into separate services only when load or operational ownership justifies it — candidate extraction points (deferred until justified): media transcoding/delivery, notification dispatch, analytics ingestion, **recommendation inference**, **AI tutor and voice processing**, subscription webhook handling (source §3.1 — restated as the architectural philosophy governing how/when these five logical AI "services" actually become physically separate deployable services).
**FR-11** **Keep the recommendation corpus small and curated rather than a general LLM tutor at this stage** (source §18.4 Risks — a deliberate scope-discipline principle, the architectural restraint underlying FR-1's Recommendation/Learning Service designs).
**FR-12** Distributed tracing is specifically required for AI flows (alongside media and subscription flows), given they involve the most cross-service hops and the highest cost of a silent failure (source §20.2).



### 1.10 Edge Cases

1. The Recommendation Service's candidate ranking surfaces a piece of content that technically exists in the approved corpus but has since been withdrawn (cross-ref E.29's content lifecycle) → the citation/safety verifier must check current content availability at serve-time, not merely at corpus-indexing time, excluding withdrawn content from any recommendation regardless of how recently it was indexed.
2. A canary release of a new model version shows acceptable aggregate evaluation metrics but a specific religious-rulings-category test case in the evaluation suite fails → per FR-9's release gate, this is a release-blocking critical finding regardless of how strong the aggregate metrics look, since religious-rulings accuracy is held to its own elevated bar (cross-ref E.30 FR-2's stricter confidence threshold, the consumer-facing manifestation of this same gating principle).
3. The Narration Service is asked to generate a narration variant using a child's own recorded voice as a style reference, with the parent having consented to voice-feature use generally but not specifically to voice-cloning → consistent with FR-1's "no child voice cloning without explicit consent" being its own distinct consent category, general voice-feature consent does NOT imply voice-cloning consent — the two are never bundled into a single broader permission.
4. The Insights Service, in summarizing a child's habit consistency, would naturally need to reference a specific date range during which the child's behavior notably changed (e.g., right around a documented life event the parent mentioned in a support ticket, which the Insights Service has no access to and shouldn't) → the service has no access to such external context by design (its inputs are strictly the platform's own learning/habit data), so it correctly limits itself to describing the observable pattern ("consistency dipped during this period") without ever speculating about external causes, consistent with FR-8's "must not infer sensitive traits" principle extended to causal speculation generally.
5. A load spike on the Recommendation Service (e.g., a viral content moment driving unusually high traffic) reaches a level where the candidate-extraction threshold genuinely seems justified → this triggers the documented extraction evaluation process (FR-10), but extraction itself is a deliberate, reviewed architectural decision with its own rollout plan — never an emergency ad-hoc split performed reactively under load pressure without the standard service-extraction review.
6. An evaluation suite test for "pronunciation-scoring bias across accents" reveals a systematic scoring disadvantage for a specific regional Arabic dialect → this is treated as a critical finding for any model update touching pronunciation scoring specifically, blocking release until addressed, consistent with the principle that bias findings are not treated as lower-priority than safety findings when the bias itself constitutes an unfair child-facing outcome.
7. A model/prompt change is approved and canary-released, but a previously-unseen failure mode emerges during the canary window itself (not caught by the offline evaluation suite) → the defined rollback path (FR-9) must be actually executable within the canary window, reverting to the prior known-good model/prompt version without requiring a full redeploy cycle, consistent with the platform's general feature-flag-based kill-switch philosophy (cross-ref E.30's kill switch, E.34's rollback-strategy pattern).



### 1.11 Error Handling

| Scenario | System Behavior |
|---|---|
| Recommendation references withdrawn content | Excluded at serve-time via the citation/safety verifier, regardless of indexing freshness |
| Religious-rulings test case fails in an otherwise-passing evaluation run | Treated as a release-blocking critical finding, never offset by strong aggregate metrics |
| General voice-feature consent present, voice-cloning consent absent | Voice cloning never proceeds — the two consents are never conflated |
| Canary release reveals a new failure mode mid-window | Rollback path executed within the canary window, no full redeploy required |
| Accent-specific pronunciation-scoring bias detected | Treated as a critical finding for any release touching pronunciation scoring |



### 1.12 Empty States
- A locale/age-band with too little approved corpus content for meaningful recommendation ranking → the Recommendation Service falls back to a sensible, clearly-non-personalized default set rather than an empty result, consistent with A.2's own established graceful-degradation pattern for this exact scenario.



### 1.13 Loading States
- N/A at this architectural-document level; individual consuming features (A.2/A.5/B.13) own their own loading-state UX.



### 1.14 Offline States
- N/A at this architectural-document level; AI services are inherently server-side and require connectivity, with each consuming feature owning its own offline-fallback UX (e.g., A.5's listen-only offline fallback).



### 1.15 Permission States
- Voice-cloning consent and general voice-feature consent are tracked as two distinct, separately-grantable permissions (Edge Case 3), consistent with C.26's general per-consent-type granularity.



### 1.18 Screen Inventory (Complete — Zero Missing)

> As a cross-cutting architecture document, this feature has no dedicated UI screens of its own — its operator-facing surfaces are E.30's AI Moderation Console (already fully specified) and E.30's Evaluation Harness Dashboard/Release Gate Decision screens (already specified). This document's "screens" are the conceptual architecture diagrams above, which inform every consuming feature's own UI.

| # | Surface | Owning Document | Relationship to This Document |
|---|---|---|---|
| 1 | AI Moderation Queue/Detail | E.30 | Operates downstream of the Moderation Service specified here |
| 2 | Evaluation Harness Dashboard | E.30 | Operationalizes this document's §1.7 FR-9 release-gate requirement |
| 3 | Kill Switch Confirmation | E.30 | Operates on the AI features/services architected here |
| 4 | AI Insight Report (consumer) | C.20/C.22 | Consumes the Insights Service specified here |
| 5 | Pronunciation Coaching UI (consumer) | A.5 | Consumes the Learning/Narration Services specified here |
| 6 | Search Voice Query (consumer) | B.13 | Consumes the Moderation Service specified here |



Coverage: each FR above is retained as an exact requirement. B13 admin FR7; B17 admin campaign FR7; F35 architectural/evaluation/deployment FRs and F37 backend/admin FRs are non-mobile-screen constraints, excluded from design prompts but not omitted. FRs defining child safety, privacy, voice, gates, isolation and AI behavior apply to every consuming screen. F35/F37 create no dedicated mobile screen (§1.18).



### F36

Source: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md`



### 1.7 Functional Requirements

**FR-1** Activation Window & Lifecycle (canonical): Pre-Ramadan Countdown (14 days before); Ramadan Mode Active (30 days, Hijri, regionalized); Laylatul Qadr Window (nights 21, 23, 25, 27, 29 — gamification deliberately suppressed); Eid Transition (last 2 days + Eid day); Eid Celebration (3 days); Post-Eid Tail (14 days after Eid).
**FR-2** **The activation window is keyed to the Region setting on the Parent Profile, not device locale.**
**FR-3** **A moon-sighting-disputed Eid date triggers an Admin override that updates the `ramadan_campaigns` record and pushes a one-time notification; in-progress UI re-syncs on next app open.**
**FR-4** **Hijri start date: server-side Hijri calendar service with a regional moon-sighting override table.**
**FR-5** Child UX Flow: Home re-themes; Lantern Progress Path (30-night journey map); each night unlocks a themed mission set (story, dua, optional fasting log); completion feeds the standard reward engine (A.11); Laylatul Qadr surfaces dedicated scholar-approved content; Eid transitions to Eid Mode with a certificate available.
**FR-6** Parent UX Flow: Ramadan section on Parent Dashboard with family-level aggregate rollup; per-child Fasting Tracker toggle (hidden for young children by default); certificate generation/share via the standard Parent Gate.
**FR-7** Each of the 30 nights follows the same `content_items`/`content_versions` schema as all other content, scoped with a `season_id` — no parallel content schema.
**FR-8** Ramadan-specific achievements plug into the existing achievement/badge system; `badges.season_id` scopes seasonal badges — no parallel reward mechanism.
**FR-9** **Fasting-tracking content for young children must avoid any framing that could pressure a child medically unready to fast; the parent toggle exists specifically to let a parent exclude a child from this feature entirely.**
**FR-10** Fasting Tracker supports three parent-configurable approaches per child: full fast / practice / education-only, with the child only able to log within the allowed range.
**FR-11** Database additions: `ramadan_campaigns`, `ramadan_missions`, `ramadan_journey_progress`, `fasting_logs`, `ramadan_certificates` — all additive, none replacing an existing table.
**FR-12** **Laylatul Qadr nights deliberately suppress gamification** — no leaderboard-style framing, no competitive badge call-outs during these nights, a calmer reflection-oriented register.
**FR-13** The Day 28-30 conversion moment shows a **soft, never-blocking** card with standard purchase-flow terms shown first — never an interrupting paywall.
**FR-14** Family member invites support a read-only Family Ramadan Report link for extended family.



### 1.10 Edge Cases

1. A family's Region changes mid-Ramadan → window recalculates going forward; already-completed nights are preserved.
2. A child's age band changes mid-Ramadan → completed nights remain credited; remaining nights reflect the new age band going forward.
3. A parent changes a child's fasting approach partway through → existing log entries preserved; no new entries beyond the new scope offered going forward.
4. Two children on different fasting approaches → Family Aggregate Bar reflects each child's own scope without implying comparison.
5. A child misses several nights → missed nights remain completable retroactively, never locked out, consistent with the platform's anti-shaming philosophy.
6. The content-completeness deadline arrives with a gap discovered → release-blocking incident with explicit escalation.
7. A family's trial lapses before day 28 → the Ramadan-day-count-specific conversion card simply doesn't apply; C.24's standard messaging takes over instead.
8. A Family Ramadan Report invite link is shared with someone without the app installed → gracefully prompts installation/account context, never a broken page.



### 1.11 Error Handling

| Scenario | System Behavior |
|---|---|
| Moon-sighting dispute changes Eid date | Admin override updates `ramadan_campaigns`; one-time notification; UI re-syncs on next open |
| Content-completeness gap discovered near deadline | Release-blocking incident, explicit escalation |
| Family Region changes mid-Ramadan | Window recalculates going forward; prior progress preserved |
| Missed nights | Remain completable retroactively |
| Day 28-30 card conflicts with trial lifecycle | Card simply doesn't apply if irrelevant; standard messaging takes over |



### 1.12 Empty States
- A new family joining mid-Ramadan → prior nights marked "not applicable" rather than missed.



### 1.13 Loading States
- Brief themed loading transition entering the activation window.



### 1.14 Offline States
- Journey Map and current night's content function offline if pre-downloaded; sync follows B.15's standard pattern.



### 1.15 Permission States
- Fasting Tracker visibility is parent-permissioned per child; hidden, not shown-disabled, if not enabled.



### 1.18 Screen Inventory (Complete — Zero Missing)

| # | Screen | Type | Entry Points | Exit Points |
|---|---|---|---|---|
| 1 | Ramadan Prep / Countdown | Screen | Home, 14 days before activation | Parent Prep Checklist |
| 2 | Ramadan Home (themed) | Primary | App open during activation window | Journey Map, themed Stories/Rewards |
| 3 | Ramadan Journey Map (Lantern Progress Path) | Primary | Ramadan Home | Mission Detail, Night Recap |
| 4 | Night Recap | Screen | Journey Map, completed night | Back to Journey Map |
| 5 | Mission Detail (Ramadan) | Screen | Journey Map, current night | Story Player, Dua of the Night, Fasting Tracker entry |
| 6 | Ramadan Story Player | Screen | Mission Detail | Mission Detail (completed) |
| 7 | Fasting Tracker Toggle & Log | Component/Screen | Mission Detail, Parent Settings | Mission Detail |
| 8 | Laylatul Qadr Reflection (calmer variant) | Screen variant | Journey Map, nights 21/23/25/27/29 | Night Recap (calmer variant) |
| 9 | Eid Countdown | Screen | Ramadan Home, last 2 days | Eid Home |
| 10 | Eid Home (themed) | Screen | Eid Countdown, Eid day onward | Eid Reward Reveal, Eid Card Generator |
| 11 | Eid Reward Reveal | Screen | Eid Home | Eid Card Generator |
| 12 | Eid Card Generator | Screen | Eid Home | Parent Gate → Share |
| 13 | Ramadan Complete Certificate | Screen | Eid Home, Journey Map | Parent Gate → Share/Print |
| 14 | Post-Eid "Keep the Habit" | Screen | Home, 14 days post-Eid | A.7's Habit Builder |
| 15 | Ramadan Settings Card (Parent) | Screen (Parent Area) | Family Overview | Fasting approach per child, reminders, invites |
| 16 | Ramadan Dashboard Tab (Parent) | Screen (Parent Area) | Parent Dashboard, active window only | Per-child detail, Family Aggregate |
| 17 | Family Ramadan Aggregate | Screen (Parent Area) | Ramadan Dashboard Tab | Per-child detail |
| 18 | Family Ramadan Report (printable) | Screen (Parent Area) | Ramadan Dashboard Tab, Post-Eid | Certificate generation, Family member invite |
| 19 | Conversion Moment Card (Day 28-30) | Component/Modal | Home, Ramadan Dashboard | C.24's standard purchase flow |
| 20 | Family Member Invite (read-only report link) | Screen (Parent Area) | Ramadan Settings Card, Family Report | External share |



Coverage: each FR above is retained as an exact requirement. B13 admin FR7; B17 admin campaign FR7; F35 architectural/evaluation/deployment FRs and F37 backend/admin FRs are non-mobile-screen constraints, excluded from design prompts but not omitted. FRs defining child safety, privacy, voice, gates, isolation and AI behavior apply to every consuming screen. F35/F37 create no dedicated mobile screen (§1.18).



### F37

Source: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F37_Security_Architecture.md`



### 1.7 Functional Requirements

**FR-1** JWT Authentication Flow (canonical, source §13.1, the architectural origin point this document specifies once for every feature to reuse): (1) parent requests an OTP challenge; (2) auth service records hashed challenge metadata and rate-limit counters; (3) OTP provider sends the code; (4) parent verifies the code; (5) auth service issues a short-lived access token and a rotating refresh token; (6) a device/session record is created; (7) parent PIN or biometric step-up creates a short-lived elevated token for sensitive actions; (8) selecting a child creates a child-mode token containing only child-safe scopes.
**FR-2** **Token claims (canonical, source §13.1): `sub`, `family_id`, `mode`, optional `child_id`, `scopes`, `device_id`, `auth_time`, `consent_version`, `session_id`** — this exact claim set is the single schema every token-issuing and token-validating code path across the entire platform must use, never a feature-specific variant.
**FR-3** **Authorization is computed from role + resource scope + region + locale + action** (source §13.2/§11.6 — restated as the canonical, platform-wide authorization model, already operationalized per-role in E.28's RBAC matrix).
**FR-4** **The API Gateway performs no business authorization decisions on its own — every domain service rechecks ownership and scope independently. This prevents a single gateway misconfiguration from becoming a system-wide authorization bypass** (source §13.2/§3.3 — a hard, zero-exception architectural rule already reflected in every prior feature's "service-layer enforcement, not gateway-layer" pattern, e.g., E.28's structural child-mode-token rejection, E.32's PII Masking Service).
**FR-5** **Child-mode tokens carry only child-safe scopes; Parent dashboard APIs explicitly reject child-mode tokens rather than silently returning empty data, so a scope mismatch is observable rather than silently masked** (source §13.2 — restated as the rationale behind C.20's structural Parent-Session-Only Gate pattern, with the explicit-rejection-not-silent-empty-response design choice called out here as the general principle).
**FR-6** **Every child-scoped query is double-checked against family ownership AND active child session — a parent's JWT alone is never sufficient to read a specific child's data outside their own family** (source §13.2 — the architectural origin of C.19's strict session-to-child_id binding and B.14's per-child isolation guarantees).
**FR-7** **Parent identity: phone/email OTP or Google login (no Apple login). JWT access + refresh token pair; refresh rotation on use; Redis-backed denylist for revoked tokens. Child profiles are not independently authenticated accounts — they are PIN/biometric/pattern-locked profiles under one parent session** (source "Security Architecture" card — restated as the canonical parent/child identity model).
**FR-8** **Platform Security & Role Taxonomy (Dual-Axis Authorization Model):** The system strictly enforces a dual-axis authorization architecture: (1) **Customer Account Tiers (Client Scope):** `guest`, `registered` (free), and `premium` (active subscription, evaluated via `parent_entitlements` and `JwtClaims.is_premium`); (2) **Internal Administrative RBAC (Staff Scope):** The 9 canonical roles defined in E.28 (`super_admin`, `product_admin`, `content_editor`, `scholar`, `moderator`, `support`, `billing_ops`, `analytics_viewer`, `trust_safety`) enforced via `admin_users.role` and `require_admin_scope()`. Consumer tokens cannot access admin routes, and customer PII is masked by default.
**FR-9** **Parent Mode re-gates on every entry (PIN/biometric, short grace window)** (source — restated, the architectural origin of C.19's zero-exception Switch-Profile gating with its client-side-UX-only grace-window design).
**FR-10** Data Encryption (canonical, source §13.3): TLS in transit; encryption at rest for the database and object storage; managed secret storage with rotation; **PIN and lock-pattern hashes use a slow, salted hashing algorithm (e.g., bcrypt or argon2) — never a fast general-purpose hash**; **biometric verification relies entirely on OS-level assertions; NoorHeroes never stores biometric templates itself.**
**FR-11** API Security (canonical, source §13.4): WAF, rate limiting, and bot/credential-stuffing detection at the gateway layer; SAST, dependency scanning, container scanning, and regular penetration testing as part of CI/CD and a recurring security calendar; **MFA/passkeys required for admin and scholar accounts** — a higher bar than the parent-facing OTP+PIN model.
**FR-12** Content Upload Validation Pipeline (canonical, complete 11-step sequence, source §13.5): (1) extension and MIME allowlist validation; (2) file-signature verification (magic bytes, not just trusting the extension); (3) size/duration/dimension limits; (4) antivirus and malware scanning; (5) image/video adult-content AI classifier; (6) audio transcription plus text-safety scan; (7) text adult/sexual/violent/extremist safety scan; (8) metadata stripping (EXIF, GPS, author info); (9) perceptual hash check against a known-content blocklist; (10) **quarantine before transcoding — assets are never in child-delivery storage during this stage**; (11) human child-safety review.
**FR-13** Child Safety Controls (canonical, source §13.8): no open direct messages or public comments anywhere in the product; no unsafe external links reachable without a parent gate; parent gate required around all external sharing actions; content age and region eligibility enforced at the API layer, not just hidden in the UI; scholar and child-safety approval required before any content reaches a child, with no seasonal-content exception; an AI emergency kill switch exists and is regularly tested; a report/feedback path is available on all media; support and moderation escalation paths carry defined severity SLAs.
**FR-14** Vulnerability Prevention (canonical, source §13.9): immutable or tamper-evident audit logs (append-only at the database-role level, not just the application level); tested backup restores — a backup that has never been restored is not a verified backup; a documented incident-response procedure with parent-notification steps for any data-breach scenario.
**FR-15** **Rate limiting applies at device, IP, phone, and account levels** (source — restated as the complete, multi-dimensional rate-limiting requirement, beyond a single IP-based check alone).



### 1.10 Edge Cases

1. A domain service's own independent authorization check fails to catch a request the gateway would have otherwise blocked (e.g., a temporary gateway WAF rule lapses) → consistent with FR-4's defense-in-depth design, this is precisely the scenario the "gateway makes no business-authorization decisions" architecture is meant to render survivable — the domain service's own check remains the actual authoritative gate regardless of gateway-layer state, so a gateway-layer gap alone should never result in an actual authorization bypass.
2. A refresh token is used after having already been rotated (e.g., a replayed/stolen old refresh token) → the Redis-backed denylist must correctly reject this reuse attempt, treating it as a signal of potential compromise (consistent with standard refresh-token-rotation security practice) rather than silently accepting it.
3. An admin/scholar account's MFA device is lost → a documented, audited recovery path exists (consistent with E.28's general account-recovery patterns), never a silent MFA bypass for this elevated-privilege account class specifically.
4. Content uploaded by a trusted internal source (e.g., a Content Editor uploading directly via the CMS) is tempting to fast-track past some of the 11 pipeline steps given the apparent lower risk → this temptation must be explicitly resisted architecturally — the pipeline applies identically regardless of upload source's perceived trust level, since the actual risk (a compromised editor account, a supply-chain-compromised asset, human error) is not eliminated by source trust alone.
5. A penetration test discovers a finding that, while technically valid, would require disproportionate effort relative to its actual risk to remediate immediately → findings are triaged by severity with defined remediation SLAs (FR-?, cross-ref the platform's general severity-SLA pattern), but every finding still requires a documented disposition (fixed, risk-accepted-with-sign-off, or compensating-control-applied) — never a finding that simply goes unaddressed without an explicit decision.
6. A data-breach incident occurs that, on initial assessment, appears to affect only non-sensitive data (e.g., aggregate analytics) → the incident-response procedure must still be fully invoked to confirm this assessment is correct before concluding parent notification isn't warranted, since an initial scoping assessment made under time pressure is exactly the kind of judgment a structured procedure exists to verify rather than shortcut.
7. A backup-restore test reveals the backup is not actually restorable as expected (a genuine "backup that turns out not to be a backup" scenario) → this is itself a critical incident requiring immediate remediation (rebuilding the actual restorable backup process) and a root-cause investigation into how an unverified, non-functional backup process went undetected, never simply noted and left for a future cycle.



### 1.11 Error Handling

| Scenario | System Behavior |
|---|---|
| Child-mode token used against a Parent Dashboard endpoint | Explicit rejection with a clear error, never silently returning empty/masked data (FR-5) |
| Replayed/stolen rotated refresh token | Rejected via the Redis-backed denylist, treated as a potential compromise signal |
| Gateway-layer authorization gap (e.g., a lapsed WAF rule) | Domain service's own independent authorization check remains authoritative, preventing actual bypass |
| Penetration-test finding with disproportionate remediation cost | Requires an explicit documented disposition, never left unaddressed silently |
| Backup found non-restorable during a verification test | Treated as a critical incident, immediate remediation, root-cause investigation |



### 1.12 Empty States
- N/A at this architectural-document level.



### 1.13 Loading States
- N/A at this architectural-document level.



### 1.14 Offline States
- N/A at this architectural-document level; each feature's own offline-fallback design (e.g., A.5/B.13/B.15's listen-only/cached-policy patterns) already incorporates this architecture's authentication/authorization guarantees into their respective offline-handling designs.



### 1.15 Permission States
- N/A at this architectural-document level beyond what's already specified by FR-3/FR-8's role taxonomy, operationalized per-feature throughout this documentation suite.



### 1.18 Screen Inventory (Complete — Zero Missing)

> As with F.35, this is a cross-cutting architecture document with no dedicated UI screens of its own. Every security mechanism specified here is operationalized through screens already fully documented in their owning features.

| # | Surface | Owning Document | Relationship to This Document |
|---|---|---|---|
| 1 | Parent PIN/Biometric Gate, Who Is Learning | C.19 | Implements FR-1/FR-7/FR-9's authentication/re-gating flow |
| 2 | Admin Login / 2FA | E.28 | Implements FR-11's MFA-on-admin-accounts requirement |
| 3 | Child Lock Verification | C.19/C.23 | Implements FR-10's slow-hash credential storage |
| 4 | AI Moderation Console Kill Switch | E.30 | Implements FR-13's AI emergency kill switch |
| 5 | Media Library / Quarantine Detail | E.29 | Implements FR-12's upload-pipeline quarantine step |
| 6 | PII Masking / Unmask Workflow | E.32 | Implements FR-6's double-checked child-scoped query principle |
| 7 | Audit Log Viewer | E.28 | Implements FR-14's immutable, tamper-evident audit logging |



Coverage: each FR above is retained as an exact requirement. B13 admin FR7; B17 admin campaign FR7; F35 architectural/evaluation/deployment FRs and F37 backend/admin FRs are non-mobile-screen constraints, excluded from design prompts but not omitted. FRs defining child safety, privacy, voice, gates, isolation and AI behavior apply to every consuming screen. F35/F37 create no dedicated mobile screen (§1.18).



## Independent surfaces and state mapping



### Search (B13, screen)

PRD: `PRD_Documents/Child App Supporting (13-18)/Feature_B13_Search_Discovery.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: `Screens/Mobile App/Search/Search-01.png`; `Screens/Mobile App/Search/Search-02.png`

Exact observed labels: Search; Recent Searches; Clear all; Try searching for; Prophet Ibrahim; Surah Al-Asr; Morning duas; Letter Trace; Start typing or tap the mic to search; Your recent searches will appear here

Behavior: Any tab search icon → landing; recent/suggested query → Results; x removes one query, Clear all clears active child history; back restores invoking tab; mic explicit tap plus parent consent and OS permission → Listening. Suggestions must be moderated and age-eligible.

States: recent populated, first-time, offline local history, fetch failure omitted

Conflict / limits: Search input appears clipped after du; do not infer exact full placeholder. Letter Trace/Tajweed suggestions exceed explicit story/surah/dua destination contract: confirm routing.



### Voice Search — Listening (B13, state)

PRD: `PRD_Documents/Child App Supporting (13-18)/Feature_B13_Search_Discovery.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: `Screens/Mobile App/Search/Voice Search-01.png`

Exact observed labels: Listening...; Say what you’re looking for; Tap to simulate speech →; Cancel

Behavior: Explicit mic tap only; cancel/interruption discards partial audio → Search; completion → Processing; denied permission → text-only Search. Simulation control is prototype annotation pending approval.

States: listening, permission denied, parent permission absent, interrupted, cancel

Conflict / limits: 



### Voice Search — Processing (B13, state)

PRD: `PRD_Documents/Child App Supporting (13-18)/Feature_B13_Search_Discovery.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: `Screens/Mobile App/Search/Voice Search-02.png`

Exact observed labels: Processing...; Finding results for you; Cancel

Behavior: Processing complete → Results; low-confidence → clarification; cancel → Search; no partial/garbled search. Raw audio not training data.

States: processing, low confidence, error, cancel

Conflict / limits: 



### Voice Search — Clarification (B13, overlay)

PRD: `PRD_Documents/Child App Supporting (13-18)/Feature_B13_Search_Discovery.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: Missing verified image reference

Exact observed labels: Missing; do not invent approved copy.

Behavior: Low confidence asks retry or approved simplified clarification; retry → Listening, cancel → Search. No raw transcription leakage.

States: low-confidence

Conflict / limits: Required copy and reference absent; do not author approved copy.



### Search Results (B13, screen)

PRD: `PRD_Documents/Child App Supporting (13-18)/Feature_B13_Search_Discovery.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: `Screens/Mobile App/Search/Results.png`

Exact observed labels: Prophet Ibrahim; 1 result for "Prophet Ibrahim"; All 16; Stories 5; Surahs 4; Story; Prophet Ibrahim (AS); Islamic Stories · 4 episodes

Behavior: Type chips All/Stories/Surahs/Duas requery; story → A3 Story Detail, surah → A5 Surah Learning, dua → A6 Dua Learning; close query clears input; mic → voice. Eligibility is authoritative server filtering, never adjustable beyond safe eligibility.

States: results, loading skeleton, filter selected, friendly zero results, API error retry, offline downloaded-only

Conflict / limits: 1 result contradicts filter counts All16/Stories5/Surahs4; screenshot is list vs PRD grid; age filter FR2 vs KMP no age parameter needs clarification.



### Parent Area Search (B13, screen)

PRD: `PRD_Documents/Child App Supporting (13-18)/Feature_B13_Search_Discovery.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: Missing verified image reference

Exact observed labels: Missing; do not invent approved copy.

Behavior: Gated Parent Dashboard → parent family reports/story activity/habits search; report → C22, story activity → A3 activity view, habit → A7 detail. Parent-session only; no child/admin search leakage.

States: initial, loading, results, empty, error retry, offline connectivity required

Conflict / limits: No supplied screen reference or verified exact copy; KMP07 specifies no offline cache.



### Favorites (B14, screen)

PRD: `PRD_Documents/Child App Supporting (13-18)/Feature_B14_Favorites.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: `Screens/Mobile App/Favorites/Favorites-01.png`; `Screens/Mobile App/Favorites/Favorites-02.png`; `Screens/Mobile App/Favorites/Favorites-03.png`; `Screens/Mobile App/Favorites/Favorites-04.png`

Exact observed labels: Saved; Favorites; Downloads; All 10; Stories 4; Surahs 3; No longer available; Prophet Ibrahim (AS); Moonlit Lantern; Prophet Yusuf (AS); Kindness Like Rain; Surah Al-Asr; Surah Al-Fatiha; Surah Al-Ikhlas; Upon Waking; Morning Dua; Travel Dua; You’re offline — showing your cached favorites

Behavior: Profile Favorites & Downloads → shared Saved shell Favorites; Downloads tab → B15; filter by content type; item → A3/A5/A6 detail; heart removes optimistically idempotently; withdrawn item cannot open; back → Profile. Save only eligible/unlocked/entitled content. All data active-child scoped.

States: populated, loading, empty, filtered, cached offline, withdrawn item, optimistic retry

Conflict / limits: Default/Loading/Offline pills are testing controls visible in references; approval required before omission. Offline favorite is not guaranteed downloaded playback.



### Downloads (B15, screen)

PRD: `PRD_Documents/Child App Supporting (13-18)/Feature_B15_Offline_Downloads_Sync.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: `Screens/Mobile App/Favorites/Favorites-05.png`; `Screens/Mobile App/Favorites/Favorites-06.png`; `Screens/Mobile App/Favorites/Favorites-07.png`; `Screens/Mobile App/Favorites/Favorites-08.png`; `Screens/Mobile App/Favorites/Favorites-09.png`

Exact observed labels: Saved; Favorites; Downloads; Device storage used; 0.1 GB / 3 GB; 7 items downloaded · Plays without internet; Downloading... 62%; Queued; Download paused — tap Retry; Retry; Access renewed — re-download to play; Re-download; Clear All Downloads; No downloads yet; Download stories, surahs, and du’as to enjoy them offline — no internet needed!; Look for the download button on any content

Behavior: Profile → Saved Downloads; completed item → owning offline player if license valid; retry resumable chunks and revalidate entitlement/cap; remove deletes only active child media; Clear All → confirmation; favorite tab independently scoped; content progress/history/favorites persist. Offline outbox causal sync/dedupe, reward exactly once.

States: populated, loading, queued, downloading, failed retry, expired license, empty, cap reached, insufficient storage, withdrawn after policy refresh

Conflict / limits: 0.0GB with 4 items/download progress fixture contradictory; exact values are fixtures, not live data; cap/expiry toast copy missing.



### Clear All Downloads Confirmation (B15, overlay)

PRD: `PRD_Documents/Child App Supporting (13-18)/Feature_B15_Offline_Downloads_Sync.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: Missing verified image reference

Exact observed labels: Missing; do not invent approved copy.

Behavior: Clear all → confirm/cancel; confirm removes active-child downloaded media only; cancel retains list and storage; no removal of favorites or progress.

States: confirm, cancel

Conflict / limits: Required modal reference/copy missing.



### Parent Download Cap and Policy (B15, screen)

PRD: `PRD_Documents/Child App Supporting (13-18)/Feature_B15_Offline_Downloads_Sync.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: Missing verified image reference

Exact observed labels: Missing; do not invent approved copy.

Behavior: Parent Controls → own child cap configuration; save policy; subsequent attempts over cap show supportive cap-reached state. Standard parent session and own-family constraints.

States: loading, saved, validation, error retry, offline policy pending

Conflict / limits: No screenshot or exact field bounds/copy verified; confirmation needed before executing.



### Child Profile (B16, screen)

PRD: `PRD_Documents/Child App Supporting (13-18)/Feature_B16_Child_Profile.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: `Screens/Mobile App/Child Profile/Child Profile-01.png`; `Screens/Mobile App/Child Profile/Child Profile-02.png`; `Screens/Mobile App/Child Profile/Child Profile-05.png`; `Screens/Mobile App/Child Profile/Child Profile-06.png`; `Screens/Mobile App/Child Profile/Child Profile-07.png`; `Screens/Mobile App/Child Profile/Child Profile-08.png`

Exact observed labels: Aisha; Islamic Explorer; Language; English; Favorites & Downloads; Saved content & offline items; Settings; Notifications, privacy & more; Switch Profile; Requires parent permission; Sign Out; Level; day streak; badges; Level 1 · Just starting out; Start your journey to earn XP and level up!; Earn your first XP — pick an activity; Listen to your first story; Complete a knowledge quiz; Learn your first du’a; Offline — showing cached profile; Retry; Available offline; Unavailable until reconnected; Try reconnecting

Behavior: Tab5 → active child profile; avatar → A12; Favorites & Downloads → shared Saved; language → Choose Language; Switch Profile ALWAYS parent gate then Who Is Learning then selected child lock or parent session; cancel/failure preserves child; successful switch clears child UI before rendering new identity. Stats display-only unless approved progress route. Disabled session → picker; cold start resolve session not saved screen identity.

States: default, skeleton, zero progress, stats unavailable partial, cached offline, return/resume, disabled session

Conflict / limits: Screenshot Settings/Sign Out are beyond canonical B16 sections, need source-owned gated destination. Screenshot disables offline language/switch, contradicts PRD §1.14/§6.7 local language and usable offline actions. Fixture XP/streak/name are not live data.



### Choose Language (B16, overlay)

PRD: `PRD_Documents/Child App Supporting (13-18)/Feature_B16_Child_Profile.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: `Screens/Mobile App/Child Profile/Child Profile-03.png`

Exact observed labels: Choose Language; English; العربية; اردو; Français; Cancel

Behavior: Single selected display locale applies instantly app-wide; cancel dismisses untouched; offline apply locally and sync on reconnect per PRD. Content eligibility locale unaffected.

States: selected, unselected, saving optimistic, retry sync, offline

Conflict / limits: Screenshot Français differs from blueprint हिन्दी and PRD En/Hi/Ar/Ur localization; approval decision required.



### Switch Profile Parent Permission (B16, overlay)

PRD: `PRD_Documents/Child App Supporting (13-18)/Feature_B16_Child_Profile.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: `Screens/Mobile App/Child Profile/Child Profile-04.png`

Exact observed labels: Parent Permission Required; Enter your 4-digit parent PIN to switch profiles; Cancel

Behavior: Shared C19 gate: 4 PIN boxes numeric keypad/backspace; always new gate child→parent no grace bypass; success→picker; failure/cancel→same child; repeated failure inherits lockout. OS biometric alternative per C19.

States: input, invalid PIN, lockout, biometric fallback, cancel

Conflict / limits: Reuse C19 prompt rather than duplicate independent gate screen.



### Deep Link Resolver (B17, state)

PRD: `PRD_Documents/Child App Supporting (13-18)/Feature_B17_Notifications_Child_Facing.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: `Screens/Mobile App/Notifications/Deep Link Resolver.png`

Exact observed labels: Opening...; Just a moment

Behavior: OS push→resolve session/child/content/parent gate; offline→reconnect retry; required auth→shared gate/picker; unavailable→safe alternative/Home. Bedtime→A4; streak→A7; content→A3/A5/A6; reward→A11. No gate bypass or sibling disclosure.

States: loading, offline retry, unavailable, gate required, resolved

Conflict / limits: Only loading image verified; offline/unavailable exact copy absent.



### In-App Notification Banner (B17, component)

PRD: `PRD_Documents/Child App Supporting (13-18)/Feature_B17_Notifications_Child_Facing.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: Missing verified image reference

Exact observed labels: Tomorrow’s episode is ready

Behavior: Lightweight dismissible Home/feature banner; tap to eligible destination; billing/sensitive analytics prohibited in child copy; follows same consent/policy checks. OS notifications use platform UI, not a new app inbox.

States: shown, dismissed, tapped

Conflict / limits: PRD example copy not verified finalized copy; inbox/preferences governed C25 not B17.



### Islamic Fact Detail (B18, screen)

PRD: `PRD_Documents/Child App Supporting (13-18)/Feature_B18_Islamic_Facts_Module.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: `Screens/Mobile App/Facts/Fact Detail-01.png`; `Screens/Mobile App/Facts/Fact Detail-02.png`; `Screens/Mobile App/Facts/Fact Detail-03.png`; `Screens/Mobile App/Facts/Fact Detail-04.png`; `Screens/Mobile App/Facts/Fact Detail-05.png`; `Screens/Mobile App/Facts/Fact Detail-06.png`

Exact observed labels: Islamic Fact; Prayer; Muslims pray five times a day to stay connected with Allah; Primary Source; Sahih Bukhari, Book 10, Hadith 505; Additional Source; Sahih Muslim, Book 4, Hadith 1555; Scholar Approved; Reviewed Jun 2026 · v1.2; Please Note; Learn More; Related Story; The Prophet’s ﷺ Love for Prayer; Test Your Knowledge; 5 questions · 2 min; Start; What does this mean?; You’re offline — showing cached content; Related content and quizzes need an internet connection

Behavior: Home fact/spaced repetition → Detail; approval information expands inline; eligible related story/surah/dua→owner detail; linked quiz → shared A8 parameterized fact quiz; stale linkage omitted; withdrawn fact friendly unavailable; offline cached content; unavailable undownloaded quiz needs internet; Home omits card if zero eligible facts. Only approved published versions.

States: default, loading, cached offline, approval expanded, related missing, quiz missing, withdrawn, fetch error

Conflict / limits: Religious explanation/source references copied as visual evidence only: no independent scholar verification. Screenshot linked quiz 5 questions differs typically1 PRD. Missing visible age band FR2. Must preserve full explanation in source layers; do not recreate text from partial OCR.



### Islamic Facts Browse (B18, screen)

PRD: `PRD_Documents/Child App Supporting (13-18)/Feature_B18_Islamic_Facts_Module.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: `Screens/Mobile App/Facts/Facts Browse.png`

Exact observed labels: Islamic Facts; All Topics; Prayer; Fasting; Quran; Verified; Tap to learn more

Behavior: Observed topic-filtered browse list→Fact Detail; back→entry. Existing mobile source addition beyond PRD primary Home card/detail flow; preserve only after source reconciliation.

States: all topics, selected topic, loading, empty, offline

Conflict / limits: PRD §1.18 no Facts Browse destination; existing screen requires approval/source-flow mapping. Religious list copy must retain actual source, never regenerate.



### Ramadan Prep / Countdown (F36, screen)

PRD: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: `Screens/Mobile App/Ramadan Mode/Prep-Countdown.png`

Exact observed labels: Ramadan is Coming; Starts in your region in; FAMILY PREP; Set children’s fasting approach; Enable nightly reminders; Invite extended family; Complete Family Prep →

Behavior: 14 days before server region-adjusted start; parent prep action→gated parent Ramadan Settings/checklist; countdown values dynamic; child must not configure family settings.

States: countdown, prep complete, region change, offline stale, activation

Conflict / limits: All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.



### Ramadan Home (F36, screen)

PRD: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: `Screens/Mobile App/Ramadan Mode/Ramadan Home.png`

Exact observed labels: Night 12 of Ramadan; Assalamu Alaikum, Sara; TONIGHT’S JOURNEY; Night 12: The Story of Patience; Story · Dua of the Night · Mission; Journey Map; Dua Tonight; My Rewards; Family; View progress

Behavior: A2 Home seasonal variant: journey→Map; tonight→Mission; dua→A6; rewards→A11; Family requires gate→parent Ramadan Dashboard.

States: active, loading, pre-downloaded offline, phase change, Qadr calmer

Conflict / limits: All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.



### Ramadan Journey Map (F36, screen)

PRD: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: `Screens/Mobile App/Ramadan Mode/Journey Map (Lanterns).png`

Exact observed labels: 30-Night Journey; Night 12 of 30; Completed; Tonight; Laylatul Qadr; Ahead; Start Tonight’s Mission →

Behavior: 30 lantern nodes; tonight/missed→Mission; complete→Recap; Qadr nights21/23/25/27/29→Reflection; future unavailable; new join prior nights not applicable, missed still completable.

States: tonight, completed, ahead, missed, new join, Qadr, offline

Conflict / limits: All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.



### Ramadan Mission Detail (F36, screen)

PRD: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: `Screens/Mobile App/Ramadan Mode/Mission Detail.png`

Exact observed labels: Night 12 Mission; The Story of Patience; Complete your three tasks for tonight; Story; Listen to tonight’s Ramadan story; Dua of the Night; Learn Dua Al-Istikharah; Fasting Log; Record today’s fasting (if enabled)

Behavior: Story→seasonal Player using A3/A4; dua→A6; fasting only parent-enabled allowed approach→Log; back→Map; task completion feeds existing reward engine, no parallel XP.

States: tasks incomplete, complete, fasting hidden, offline downloaded, withdrawn

Conflict / limits: All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.



### Ramadan Story Player (F36, screen)

PRD: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: `Screens/Mobile App/Ramadan Mode/Story Player.png`

Exact observed labels: The Story of Patience; Story Complete ✓

Behavior: Shared A3/A4 player with seasonal context; playback controls preserve owner behavior; completion returns Mission and persists progress; interruption restores furthest valid position.

States: playing, paused, buffering, offline downloaded, complete, interrupted

Conflict / limits: All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.



### Fasting Tracker (F36, screen)

PRD: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: `Screens/Mobile App/Ramadan Mode/Fasting Tracker-01.png`; `Screens/Mobile App/Ramadan Mode/Fasting Tracker-02.png`

Exact observed labels: Night 12 Log; Suhoor eaten; Fasting intention made; Iftar completed

Behavior: Child log only permitted parent approach; practice partial log, full fast allowed full log, education-only no log; changes preserve prior nights; parent radio controls belong Settings not child.

States: full fast, practice, education-only, hidden young child, offline outbox, save retry

Conflict / limits: All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.



### Laylatul Qadr Reflection (F36, screen)

PRD: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: `Screens/Mobile App/Ramadan Mode/Laylatul Qadr Reflection.png`

Exact observed labels: Laylatul Qadr; The Night of Power — Night 25; SCHOLAR-APPROVED CONTENT; Begin Tonight’s Reflection; No scores, no comparisons — just you and this blessed night

Behavior: Qadr nights21/23/25/27/29 calm reflection→calm Recap; approved content only; suppress competitive badges/leaderboard/reward call-outs; normal rewards internal no distracting UI.

States: reflection, loading, offline downloaded, complete

Conflict / limits: All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.



### Night Recap (F36, screen)

PRD: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: `Screens/Mobile App/Ramadan Mode/Night Recap.png`

Exact observed labels: Night 12 Complete!; Your lantern is lit; Story read; Dua learned; XP earned; + 50 Noor XP; Back to Journey Map

Behavior: Completed mission→Recap→Map; actual reward value owner A11; Qadr recap suppress gamification.

States: standard, Qadr calm, pending sync, duplicate completion

Conflict / limits: All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.



### Eid Countdown (F36, screen)

PRD: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: `Screens/Mobile App/Ramadan Mode/Eid Countdown.png`

Exact observed labels: Eid is Almost Here!; You’ve completed 28 nights — Masha’Allah!; Preview Eid Celebration →

Behavior: Last2days region-adjusted→Eid preview; server override next-open resync, one-time notification; no hardcoded device-locale calendar.

States: countdown, date override, offline stale, Eid transition

Conflict / limits: All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.



### Eid Home (F36, screen)

PRD: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: `Screens/Mobile App/Ramadan Mode/Eid Home.png`

Exact observed labels: Eid Mubarak!; You completed your 30-night journey!; Open Your Eid Reward!; Tap to reveal your special badge; Generate Eid Card; Ramadan Certificate; Family Report; Share Journey

Behavior: Eid3days seasonal Home; reward→Reveal; card→Generator; certificate→Certificate; family report/share→Parent Gate then parent/report/share owner.

States: Eid active, incomplete journey copy conditional, reward revealed, offline

Conflict / limits: All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.



### Eid Reward Reveal (F36, screen)

PRD: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: `Screens/Mobile App/Ramadan Mode/Eid Reward Reveal.png`

Exact observed labels: Your Eid Reward; Tap to Reveal

Behavior: Tap reveals existing season-scoped badge/reward once; proceed Card/Home; no generated rewards or duplicate ledger posts.

States: unrevealed, revealed, already claimed, offline pending

Conflict / limits: All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.



### Eid Card Generator (F36, screen)

PRD: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: `Screens/Mobile App/Ramadan Mode/Eid Card Generator.png`

Exact observed labels: Create Eid Card; Eid Mubarak!; Wishing you joy and blessings; Choose design; Add message; Parent Gate → Share; Generate & Share (Parent Gate)

Behavior: Design→message→parent gate generation/sharing; no child name/DOB/location in artifact; cancel returns editor; share OS simulation only in Figma.

States: choose design, message, generating, error retry, gate cancel, share

Conflict / limits: All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.



### Ramadan Complete Certificate (F36, screen)

PRD: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: `Screens/Mobile App/Ramadan Mode/Ramadan Certificate.png`

Exact observed labels: NOORHEROES — RAMADAN 2026; Certificate of Completion; Completed all 30 nights of the Ramadan Learning Journey; Scholar-reviewed content · Ramadan 1447 AH; Download; Share (Parent Gate)

Behavior: Eid Home/Map→certificate; generation/share/print parent-gated per FR6; PII excluded; only true completion claims and campaign dates.

States: eligible, not complete, generation, retry, gate cancel, share/print

Conflict / limits: All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.



### Post-Eid Keep the Habit (F36, screen)

PRD: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: `Screens/Mobile App/Ramadan Mode/Post-Eid Keep the Habit.png`

Exact observed labels: Keep the Momentum Going!; Your Ramadan streak was amazing — don’t let it end; Continue daily Dua habit; Weekly Quran reading goal; Gratitude journaling (new); Build My Habit Plan →

Behavior: 14day tail→A7 Habit Builder; optional selections; no guilt pressure; gratitude journaling needs existing A7 requirement, not new product.

States: tail active, selected, dismissed, habit transition

Conflict / limits: All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.



### Parent Ramadan Settings (F36, screen)

PRD: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: `Screens/Mobile App/Ramadan Mode/Parent-Ramadan Settings.png`

Exact observed labels: Ramadan Settings; Configure each child’s experience; Fasting approach; Practice fasting; Education only; Family Invite Link; Generate Invite Link

Behavior: Gated parent Family Overview→per-child approach full/practice/education and separate visibility toggle/reminders/invite; future nights only; hidden for young by default; failed save keeps saved state.

States: loading, saved, approach changed, tracker hidden, save error, offline queued

Conflict / limits: All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.



### Parent Ramadan Dashboard (F36, screen)

PRD: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: `Screens/Mobile App/Ramadan Mode/Parent-Ramadan Dashboard.png`

Exact observed labels: Ramadan Dashboard; Family Progress; Full Family Report; Printable & shareable

Behavior: Conditional tab within C20 only active window; family→Aggregate; report→Report; own child detail individually via C22, no comparisons.

States: active window, absent outside, cached, loading, empty, error

Conflict / limits: All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.



### Family Ramadan Aggregate (F36, screen)

PRD: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: `Screens/Mobile App/Ramadan Mode/Parent-Family Aggregate.png`

Exact observed labels: Family Ramadan Journey; Family Total; missions completed this Ramadan

Behavior: Parent dashboard→aggregate-only totals; child detail separate authorized entry, never per-child array/comparative bars in aggregate.

States: aggregate, empty, cached, error

Conflict / limits: All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.



### Family Ramadan Report (F36, screen)

PRD: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: `Screens/Mobile App/Ramadan Mode/Parent-Family Report.png`

Exact observed labels: Family Report; Total missions completed; Stories read; Duas learned; Fasting logs; Laylatul Qadr reflections; Print; Share Link

Behavior: Dashboard/post-Eid→printable aggregate-only report; print/share parent gate; invite→read-only link; no sibling comparison or identifying child breakdown exported.

States: report, cached, print, share, generation retry

Conflict / limits: All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.



### Conversion Moment Card (F36, component)

PRD: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: `Screens/Mobile App/Ramadan Mode/Parent-Family Report⑲ Conversion Card (Day 28-30).png`

Exact observed labels: SOFT REMINDER — DAY 28; Continue Your Family’s Journey; Annual Family Plan — £59.99/year; Continue with Annual Plan →; Not now

Behavior: Embedded dismissible component only day28–30 AND active trial; terms before seasonal persuasion; CTA→C24 existing gated purchase; absent lapsed/converted; never blocking modal.

States: eligible trial, dismissed, lapsed absent, converted absent, offline absent

Conflict / limits: All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.



### Family Member Invite (F36, screen)

PRD: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md` §1.7; §1.18; §2.2–2.3; §1.10–1.15

Images: `Screens/Mobile App/Ramadan Mode/Parent-Family Member Invite.png`

Exact observed labels: Invite Family Members; Read-Only Report Link; Copy Link; Share

Behavior: Parent Settings/Report→generate own-family read-only link; copy/share with parent gate; recipient without app graceful install/account prompt; expiry/auth access contract unverified.

States: generation, link ready, copy feedback, share, failure retry, expired link

Conflict / limits: All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.



## Critical reconciliation addendum

### Islamic Fact Detail

Religious explanation/source references copied as visual evidence only: no independent scholar verification. Screenshot linked quiz 5 questions differs typically1 PRD. Missing visible age band FR2. Must preserve full explanation in source layers; do not recreate text from partial OCR. Approval displayed visually is not independent approval evidence; source references and paraphrased hadith require scholar verification before execution.

### Ramadan Prep / Countdown

All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.

### Ramadan Home

All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.

### Ramadan Journey Map

All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.

### Ramadan Mission Detail

All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.

### Ramadan Story Player

All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data. Story is an observed excerpt, not a complete verified curriculum item. Obtain existing approved full content; do not expand it.

### Fasting Tracker

All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data. Parent-controlled approach radios cannot be editable in child log. Education-only must omit log; young unenabled child must hide entry completely; neutral supportive tone.

### Laylatul Qadr Reflection

All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data. Screenshot quote is partial religious translation; preserve source layers exactly pending verified translation/source approval, do not complete it.

### Night Recap

All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.

### Eid Countdown

All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.

### Eid Home

All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.

### Eid Reward Reveal

All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.

### Eid Card Generator

All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.

### Ramadan Complete Certificate

All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.

### Post-Eid Keep the Habit

All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.

### Parent Ramadan Settings

All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.

### Parent Ramadan Dashboard

All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data.

### Family Ramadan Aggregate

All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data. Screenshot includes INDIVIDUAL PROGRESS Sara/Yusuf with separate bars despite KMP08 no-per-child-array/no-comparative-UI contract. Remove only through explicit conflict approval; preserve original reference.

### Family Ramadan Report

All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data. Screenshot Fasting logs 12 (Sara only) exposes per-child attribution vs aggregate-only contract; confirm approved export fields and exclusion.

### Conversion Moment Card

All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data. Screenshot persuasion precedes terms, contradicting FR13 terms-first. £59.99/year is fixture, not verified store price. Reference isolated screenshot is not permission for a blocking paywall/modal.

### Family Member Invite

All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data. Screenshot promises Link expires in 30 days. No account required to view; KMP08 flags invite contract unknown, so expiry/access promise unverified. Token is visibly truncated example; never embed real share token.

## Exact educational-copy ledger

Screenshot text is visual evidence, not independent religious verification. Preserve actual Figma text layers when available; typographic apostrophe, ﷺ glyph, ellipsis and linebreak parity require layer comparison.

### Islamic Fact Detail

Islamic Fact

Prayer

Muslims pray five times a day to stay connected with Allah

Primary Source

Sahih Bukhari, Book 10, Hadith 505

Additional Source

Sahih Muslim, Book 4, Hadith 1555

Scholar Approved

Reviewed Jun 2026 · v1.2

Please Note

Learn More

Related Story

The Prophet’s ﷺ Love for Prayer

Test Your Knowledge

5 questions · 2 min

Start

What does this mean?

You’re offline — showing cached content

Related content and quizzes need an internet connection

The five daily prayers (Salah) are Fajr (dawn), Dhuhr (midday), Asr (afternoon), Maghrib (sunset), and Isha (night). Each prayer is a time to pause, remember Allah, and ask for His guidance. The Prophet Muhammad ﷺ taught us that prayer is like a river we bathe in five times a day—it washes away our mistakes and keeps us spiritually clean. By praying regularly, we build a strong relationship with Allah and stay mindful of our actions throughout the day.

The exact timing of prayers may vary slightly between different schools of Islamic thought (madhabs).

This fact has been reviewed and approved by qualified Islamic scholars to ensure accuracy and appropriateness for children. The review date and version help us maintain up-to-date content.

### Ramadan Story Player

The Story of Patience

Story Complete ✓

In a land blessed by gentle breezes and the call to prayer, there lived a young boy named Zayd who loved Ramadan... Each night he would light a small lantern by his window, a reminder that patience is a gift from Allah...

### Laylatul Qadr Reflection

Laylatul Qadr

The Night of Power — Night 25

SCHOLAR-APPROVED CONTENT

Begin Tonight’s Reflection

No scores, no comparisons — just you and this blessed night

"Laylatul Qadr is better than a thousand months. The angels and the Spirit descend therein..." — Al-Qadr, 3-4



## Independent completeness review

- B13 §1.18: primary Search, Results, Parent Search have independent records. Listening, Processing, Clarification, Empty and Offline are variants; type filter/recent/clear are component behavior in Search/Results. Admin Search is deliberately excluded. Parent Search has no local/Figma matching reference and remains execution-blocked for exact approved copy/layout.
- B14 §1.18: shared Saved shell belongs Favorites/Downloads prompts, not a redundant third screen; filters/toggle/withdrawn component are covered inline; empty/cached offline are variants. No Favorites empty screenshot was located in supplied nine-image cluster; missing exact empty approved copy must remain flagged.
- B15 §1.18: Downloads, Clear-All overlay and Parent Policy have independent records. Storage/progress/cap/full/expiry/retry/remove/empty/initiation are owner variants/components. License-expiry prompt, cap/full message, confirmation and parent-policy exact labels/form bounds are missing, not invented. Parent Policy mandatory screen absent visual sources is a gap.
- B16 §1.18: Profile includes zero/loading/offline/partial stats; Language overlay independent; shared Parent Gate reused; avatar/full Favorites link to own features; disabled session is redirect, not a new screen. Cold start resolves session and never restores a prior sibling identity from saved UI state. Screenshot lower/upper halves are one scrolling screen.
- B17 §1.18: OS push is system surface; Deep Link resolution states and in-app banner owned here. Bedtime/habit/content/reward destination screens reused from A4/A7/A3/A5/A6/A11; per-child reminder configuration belongs C23. No independent child notification inbox is mandated by B17; parent inbox belongs C25.
- B18 §1.18: Fact Detail plus owner A8 linked Quiz/result; Home widget/repetition/approval/related link are components, zero-eligible card omission is intentional. Facts Browse exists visually but absent canonical PRD inventory, requires explicit reconciliation rather than silently omitted/treated required.
- F36 §1.18: all 20 catalogue surfaces accounted; twenty means 19 screen/variant surfaces and one embedded Conversion component, not twenty linear mandatory destinations. Night Recap can be visited from completed node without replay. Fasting education-only is variant; parent toggle belongs Settings. Dua of Night reuses A6. Parent prep checklist is embedded in Prep reference and cannot be child editable. Parent per-child detail route source should be confirmed (existing report/journey drilldown), not invented.
- F35/F37 §1.18 explicitly no dedicated mobile screens; consuming owned screens implement their constraints. Do not create AI tutor or security architecture screen.

## FR-by-FR coverage routing

| Feature | Requirement routing |
|---|---|
| B13 | FR1–2 Search/Results/voice; FR3–5 all search safe/index/empty guardrails; FR6 voice permission/audio; FR7 excluded admin surface isolation; FR8 destination switch; FR9 locale retrieval (production behavior, manually seeded prototype); FR10 clear/per-child recents; FR11 Parent Search missing visual; FR12 birthday recomputation next query, no abrupt current-view mutation. |
| B14 | FR1–2 Favorites grid/filter/open/remove; FR3 owner detail save; FR4 active-child isolation; FR5 optimistic idempotent toggle/error recovery; FR6 no save on inaccessible content; FR7 withdrawn state; FR8 type chips; FR9 shared Saved tab shell. |
| B15 | FR1 Downloads/storage/remove/retry; FR2 entitlement/manifests/checksum/sandbox/version/expiry production contract; FR3 Parent Policy/cap; FR4 causal offline outbox/progress/quiz separation; FR5 withdrawn after refresh/history preserved; FR6 resumable backoff; FR7 expired redownload; FR8 protected local media; FR9 exactly-once rewards; FR10 active-child Clear-All leaves favorites/history; FR11 independently queued transfers; FR12 per-child isolation. |
| B16 | FR1–2 Profile sections/actions; FR3 always Parent Gate zero grace; FR4 own-child stats; FR5 shared progress engine data; FR6 immediate display-only language/eligibility separate; FR7 shared Saved entry; FR8 gate→picker→child lock/parent; FR9 UI cleared before new session; FR10 Avatar deep link. |
| B17 | FR1 approved category copy; FR2 policy→template→delivery→resolver production contract; FR3 C23 per-child reminder/quiet hours; FR4 server fatigue caps; FR5 resolver all gates; FR6 no child billing/sensitive data; FR7 excluded admin campaign safety; FR8–9 exclusive installation binding/devices/logout production rule; FR10 quiet-hours server check; FR11 backoff; FR12 event-specific destinations; FR13 banner same policy. |
| B18 | FR1 detail full fields incl age/source/scope/approval/explanation/link; FR2 display contract missing age in screenshot; FR3 no disputed AI generation; FR4 capped shared mastery repetition; FR5 Home widget owner; FR6 distinct explanation; FR7 owner Quiz (count conflict); FR8 recent-fact dedupe; FR9 invalid related omission; FR10 seasonal ranking only; FR11 only current published approved version. |
| F35 | FR1 service contracts reused consuming screens; FR2 trust ceiling; FR3–6 approved knowledge/religious thresholds/moderation/source citations/human publication review; FR7 explicit visible voice/minimized audio/parent disable; FR8 no diagnosis/sibling comparison/sensitive inference/false certainty in Insights; FR9 evaluations/reviewer/canary/rollback operational; FR10 launch modular monolith no UI effect; FR11 curated corpus no general tutor; FR12 tracing production-only. |
| F36 | FR1 phase-driven variants; FR2 Parent Region; FR3 next-open date resync/one push; FR4 server Hijri authoritative; FR5 Home→Map→Mission shared content/reward/Eid; FR6 gated parents/tracker/certificate; FR7 season-scoped content schema; FR8 owner seasonal achievements; FR9 unpressured/young hidden; FR10 three allowed approaches; FR11 additive backend only; FR12 calm Qadr suppression; FR13 embedded terms-first active-trial card; FR14 read-only invite. |
| F37 | FR1 owned OTP/session/gates; FR2 canonical claims backend not UI; FR3–6 role/resource/region/locale/action plus family+active-child checks and explicit rejection; FR7 no Apple login/child independent accounts; FR8 consumer/staff isolation; FR9 parent entry re-gate vs specific B16 zero grace; FR10 OS biometric/no templates/slow hash; FR11 gateway/CI/admin MFA excluded operational; FR12 upload safety excluded staff workflow but all child media approved; FR13 media report/feedback, parent external links/sharing, no public comments/DMs; FR14 immutable audits/tested restore/incident notice operational; FR15 rate-limit failure state owned auth. |

Figma wiring simulates these contracts with authored variants/explicit test paths. It cannot prove server isolation, delivery policy, voice retention, authorization, calendar correctness, licenses or reward deduplication. Production acceptance remains separate.
