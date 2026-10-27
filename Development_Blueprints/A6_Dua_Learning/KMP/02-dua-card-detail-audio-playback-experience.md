# K-02 — Dua Card Detail & Audio Playback Experience

## 1. Feature Context
NoorHeroes — Feature A.6 Dua Learning. Source PRD §2.1/§2.2, §6.2–§6.5, §7 items 1–3. Re-derived against the real `CORE_KMP_PLAYER_INSTRUCTIONS.md`.

## 2. Parent Feature
A.6 Dua Learning

## 3. Sub-feature
K-02 — Dua Card Detail & Audio Playback Experience

## 4. Objective
Render the complete Dua Card in one composition pass with read-along highlight, optimistic-then-server-confirmed Mark-as-Learned, and Favorite toggling — using the real `AudioPlayerController`/`AudioPlayer` (audio-only playback, not the video-oriented `KMPPlayer`).

## 5. Business Requirements
FR-2, FR-3, FR-5; Edge Case 12 (single-active-audio-session).

## 6. Existing Architecture
`CORE_KMP_PLAYER_INSTRUCTIONS.md`: `AudioPlayerController` (interface, `koinInject<AudioPlayerController>()`), methods `.play(KMPPlayerSource.Network(url))`, `.setRepeatMode(RepeatMode)`; UI component `AudioPlayer(controller, modifier)`. `PlaybackSessionManager` (`koinInject`) implements "Continue Watching"-style resume via a `PlaybackSessionProvider` (DataStore/Room-backed) — reused here for resume-position, though duas are short enough this may rarely trigger. `KMPPlayerAnalytics` interface for QoS/engagement tracking, composed with the app's `CompositeAnalyticsTracker`. Favoriting consumes `B14_Favorites`'s real shared `POST /v1/favorites` (`content_type: "dua"`, `client_request_id`).

## 7. Existing Code to Reuse
- `AudioPlayerController`, `AudioPlayer` composable, `KMPPlayerSource.Network`, `KMPPlayerAnalytics` (all real, `core/kmpplayer`)
- `DuaRepository` (K-01) — extended, not forked
- `core/designsystem`'s `NoorColorScheme`/`ThemeSpec` for the three-line Arabic/transliteration/translation layout (built here if not already present, following those tokens)

## 8. Files to Create
- `feature/dua/src/commonMain/kotlin/.../detail/DuaCardDetailScreen.kt`
- `feature/dua/src/commonMain/kotlin/.../detail/DuaCardViewModel.kt`
- `feature/dua/src/commonMain/kotlin/.../detail/DuaCardUiState.kt`
- `feature/dua/src/commonMain/kotlin/.../detail/ReadAlongHighlightController.kt`
- `feature/dua/src/androidUiTest/kotlin/.../DuaCardDetailElementsTest.kt`
- `feature/dua/src/androidUiTest/kotlin/.../DuaCardDetailAlwaysFreeTierTest.kt`
- `feature/dua/src/commonTest/kotlin/.../DuaCardViewModelTest.kt`

## 9. Files to Modify
- `DuaRepository`/`DuaRepositoryImpl` (K-01) — add `getDuaDetail(id)`, `markLearned(id)` (→ B-02's `POST /v1/progress`), `toggleFavorite(id)` (→ B14's `POST /v1/favorites`, `content_type: "dua"`)

## 10. Backend Requirements
Consumes B-01 (`GET /v1/catalog/dua/{id}`), B-02 (`POST /v1/progress`, `client_request_id`), B14 (`POST /v1/favorites`).

## 11. KMP Requirements
- `DuaCardViewModel` holds `DuaCardUiState(content, learnedStatus, isFavorited, playbackState)`
- `learnedStatus`/`isFavorited`: optimistic-update-then-reconcile
- Playback via `koinInject<AudioPlayerController>()` + `AudioPlayer` composable; single-active-audio-session behavior is `AudioPlayerController`'s existing responsibility (per `CORE_KMP_PLAYER_INSTRUCTIONS.md` — confirm it already handles cross-controller session exclusivity, or whether `KMPPiPManager`-adjacent global state is needed, before assuming it's automatic)

## 12. NextJS Requirements
N/A.

## 13. API Contract
Per B-01 §13, B-02 §13, B14-B01 §13 (`client_request_id`, not `client_event_id`).

## 14. Database Requirements
Local Room cache for dua detail (`getRoomDatabase()`) + `SyncQueueEntity`-based outbox for queued mark-learned/favorite actions (shared with K-07).

## 15. Validation
Client mirrors server withdrawn-state checks but treats server as authoritative.

## 16. Authentication
Existing child-mode bearer via `core/network`.

## 17. Authorization
No entitlement check anywhere in this screen.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Audio fails to load/play | `AudioPlayerController`'s existing retry/error-state handling; fall back to a lower-bitrate source if configured |
| Mark-as-learned submission fails | Optimistic local update, queued via `SyncQueueEntity`, never blocks further interaction |
| Favorite toggle fails | Optimistic + retry |
| Dua withdrawn while open | Graceful "temporarily unavailable" + suggested alternative |

## 19. Offline First
Remote → `DuaRepositoryImpl` → Room (`SafeDatabaseHelper`) → UI; mark-learned/favorite actions queue via `SyncQueueDao`/`SyncQueueEntity` (shared K-07 mechanism) when offline.

## 20. Local Data
Cached dua detail; `SyncQueueEntity` rows for pending mutations.

## 21. Localization
Transliteration/translation independently localizable; Arabic locale-independent.

## 22. RTL
Full RTL; Arabic text uses the established Naskh-style typeface from A.5 (confirm the exact `core/designsystem` token name for this typeface before referencing it as if already named).

## 23. Analytics
Via `KMPPlayerAnalytics`(playback) + `AnalyticsTracker`(business events): `dua_card_opened`, `dua_audio_played`, `dua_marked_learned`, `dua_unmarked_learned`, `dua_favorited`, `dua_unfavorited`, `dua_unavailable_shown`.

## 24. Performance
Stable/immutable `DuaCardUiState`; coroutine cancellation on screen exit; avoid main-thread blocking during audio buffering (delegated to `AudioPlayerController`'s existing implementation).

## 25. Security
No new sensitive data; standard bearer-token reuse.

## 26. Library Requirements
Koin, Coroutines/Flow, Compose Multiplatform, `core/kmpplayer` (`AudioPlayerController`/`AudioPlayer`), Room via `core/database`.

## 27. Testing
- Unit: optimistic-update/reconcile for mark-learned and favorite
- UI: all four elements present in the semantics tree on initial render
- UI: read-along highlight has an accessible sequential-exposure fallback
- **Always-free-tier UI regression** (CI-blocking signature test for this screen)
- Integration: confirm `AudioPlayerController`'s actual single-session behavior (verify, don't assume, per §11)

## 28. Documentation
Component doc for the three-line layout and read-along controller; note the confirmed (or newly-implemented) single-session playback behavior.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Extend Repository for Detail/Progress/Favorite**
Task ID: K-02-T01. Files to Modify: `DuaRepositoryImpl.kt`. Definition of Done: methods implemented, using real `client_request_id` field name.

**Task 02 — Verify `AudioPlayerController`'s Single-Session Behavior**
Task ID: K-02-T02. Objective: confirm (read `CORE_KMP_PLAYER_INSTRUCTIONS.md` in full, or the actual controller implementation) whether cross-controller session exclusivity is automatic. Definition of Done: documented finding; if not automatic, a coordination task filed with the player-module owner rather than reimplementing session management locally.

**Task 03 — Implement DuaCardUiState & ViewModel**
Task ID: K-02-T03. Definition of Done: optimistic-update tests pass for both success and rollback-on-failure.

**Task 04 — Build Three-Line Layout Component**
Task ID: K-02-T04. Files to Modify: `core/designsystem` (if the token doesn't exist yet). Definition of Done: renders correctly across all four locales.

**Task 05 — Integrate `AudioPlayerController`/`AudioPlayer`**
Task ID: K-02-T05. Definition of Done: playback works, session-exclusivity behavior matches Task 02's finding.

**Task 06 — Implement Read-Along Highlight Controller**
Task ID: K-02-T06. Definition of Done: accessible fallback verified by test.

**Task 07 — Implement DuaCardDetailScreen**
Task ID: K-02-T07. Definition of Done: all four elements present on initial render.

**Task 08 — Implement Offline Outbox Integration**
Task ID: K-02-T08. Existing Files to Reuse: `SyncQueueDao`/`SyncQueueEntity` (shared K-07). Definition of Done: offline-queue-then-sync test passes.

**Task 09 — Add Analytics**
Task ID: K-02-T09. Definition of Done: events verified via test double.

**Task 10 — Implement Always-Free-Tier Regression Test**
Task ID: K-02-T10. Definition of Done: CI-blocking, passes.

**Task 11 — Add Remaining Tests & Documentation**
Task ID: K-02-T11. Definition of Done: all §27 scenarios covered.

**Task 12 — Final Code Review**
Task ID: K-02-T12. Definition of Done: §31 checklist fully checked.

## 30. Definition of Done
Dua Card renders all required elements, plays audio via the real `AudioPlayerController`, supports optimistic mark-learned/favorite with offline queuing, provably free of paywall UI.

## 31. Final Verification Checklist
- [ ] Uses real `AudioPlayerController`/`AudioPlayer`, not an invented player wrapper
- [ ] Uses Koin, not Hilt
- [ ] `client_request_id` used, not `client_event_id`
- [ ] Single-active-audio-session behavior confirmed (not assumed) against the real controller
- [ ] Always-free-tier UI regression test passes and is CI-blocking
- [ ] Offline outbox uses real `SyncQueueDao`/`SyncQueueEntity`, not an invented outbox table

## 32. Addendum — What Changed From the Original Draft
Corrected from an invented `:core:media-player` "lightweight audio-only wrapper" to the real, already-documented `AudioPlayerController`/`AudioPlayer` classes, from Hilt to Koin, and from `client_event_id` to the platform's real `client_request_id` idempotency field. Also flags that single-active-audio-session behavior needs to be *verified* against the real controller rather than assumed, since the original draft simply asserted it as a given.
