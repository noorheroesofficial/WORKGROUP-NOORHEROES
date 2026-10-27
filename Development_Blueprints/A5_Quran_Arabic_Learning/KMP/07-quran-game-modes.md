# K-07 — Quran Game Modes

## 1. Feature Context
Part of Feature A.5 (Quran & Arabic Learning). Six playful practice game modes: ayah ordering, listen-and-select matching, missing word, surah-theme matching, recitation echo, and progressive-reveal memorization.

## 2. Parent Feature
A.5 — Quran & Arabic Learning

## 3. Sub-feature
K-07 — Quran Game Modes

## 4. Objective
Render all six Quran Game mode screens, routing non-recitation game types through B-03 and the Recitation Echo mode through K-04's shared recorder, with smooth drag-drop/tile interaction performance.

## 5. Business Requirements
- FR-5: Quran Game modes must include at minimum: ayah ordering, listen-and-select matching ayah, find-the-missing-word, surah-name-to-theme matching (child-safe/approved context only), recitation echo with pronunciation coaching, and progressive-reveal memorization.

## 6. Existing Architecture
`feature-learn` module conventions per K-01–K-06. Recitation Echo reuses K-04 in full, identical pattern to K-06's optional-record-step reuse.

## 7. Existing Code to Reuse
- K-04's full recitation module for Recitation Echo mode.
- `LearningApi`/`LearningRepository` (B-03) for the five non-recitation game types.
- `core-designsystem` tokens; existing drag-drop/gesture utilities if the design system already provides a reusable drag-drop primitive (confirm before building a new one).

## 8. Files to Create
- `feature-learn/.../games/AyahOrderingScreen.kt` + ViewModel
- `feature-learn/.../games/ListenSelectMatchingScreen.kt` + ViewModel
- `feature-learn/.../games/MissingWordScreen.kt` + ViewModel
- `feature-learn/.../games/SurahThemeMatchingScreen.kt` + ViewModel
- `feature-learn/.../games/ProgressiveRevealMemorizationScreen.kt` + ViewModel
- `feature-learn/.../games/ModeSelectorSheet.kt` (Composable modal, entry point referenced by K-01)
- `feature-learn/.../games/QuranGameUiState.kt` (shared per-mode state contract)
- `feature-learn/src/commonTest/kotlin/.../QuranGameModesTest.kt`

## 9. Files to Modify
- `LearnRoute` — add all six game-mode destinations plus the Mode Selector Sheet route.
- K-01's `SkillTreeScreen` — wire the mode-selector entry point to open `ModeSelectorSheet`.

## 10. Backend Requirements
Consumes B-03 for the five non-recitation modes, B-04 (via K-04 reuse) for Recitation Echo, and the `content` context's game-content endpoints (ayah sets for ordering/matching/missing-word, approved theme-matching pairs — confirm exact paths per Rule 30).

## 11. KMP Requirements
- **Ayah Ordering**: drag-drop or tap-to-order UI, submits final order as the `answer_payload` to B-03.
- **Listen & Select Matching Ayah**: audio playback (`core-kmp-player`) + selection UI, submits via B-03.
- **Missing Word**: fill-in-the-blank/selection UI, submits via B-03.
- **Surah Theme Matching**: matching UI using only child-safe/approved theme content supplied by the content service (this screen must not allow free-text or unapproved-content pairing — content is fully server-curated).
- **Recitation Echo**: directly embeds K-04's `RecitationRecorderOverlay`/`RecitationViewModel`, identical reuse pattern to K-06 — falls back to Listen-Only/AI-Feedback identically to Surah Learning's record path.
- **Progressive-Reveal Memorization**: reveals ayah text progressively (e.g., word-by-word fade-in/reveal-on-tap) as a memorization aid, submits a completion/attempt marker via B-03 if scored, or is a pure practice mode with no scored submission (confirm against content/product intent before implementation — do not assume scoring behavior).
- **Mode Selector Sheet**: modal listing all available game modes plus lesson-type entries (Surah Learning, Arabic Letters, Tajweed), routed from K-01.
- **Performance**: drag-drop/tile interactions must not cause recomposition/frame-drop — use stable keys and avoid unnecessary state hoisting during active gestures.

## 12. NextJS Requirements
N/A directly; theme-matching approved-content pairs managed via the `content` context's existing admin surface (not a new admin module for this blueprint).

## 13. API Contract
`POST /v1/learning/attempts` (B-03) for five modes; `POST /v1/learning/recitation` (B-04, via K-04) for Recitation Echo.

## 14. Database Requirements
No new local persistence; game content cached via the existing offline-content-download pattern where applicable (ayah sets, theme pairs).

## 15. Validation
Surah Theme Matching restricted entirely to server-curated approved content — no client-side content generation/free-text path exists.

## 16. Authentication
Reuses existing child-session auth.

## 17. Authorization
Recitation Echo inherits K-04's gating by direct reuse.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Game content load failure | Retry/fallback, friendly error state, does not block access to other game modes |
| Attempt submission failure | Non-blocking retry |
| Recitation Echo gating (mic/toggle false) | Automatically falls back to Listen-Only/AI-Feedback path identically to Surah Learning |

## 19. Offline First
Non-recitation game content downloadable/offline-usable where feasible; attempts queue via `SyncQueue` when offline. Recitation Echo inherits K-04's connectivity-required stance.

## 20. Local Data
Content cached via existing downloadable-content Room schema; attempts queued via `SyncQueue`.

## 21. Localization
All game instructional copy and content localized via `core-common/localization`.

## 22. RTL
Full RTL layout across all six modes, including drag-drop ordering direction correctness for RTL locales.

## 23. Analytics
`quran_game_started` (game_mode), `quran_game_completed` via `AnalyticsTracker`; Recitation Echo additionally fires K-04's existing recitation event set.

## 24. Performance
Drag-drop/tile interactions optimized for zero frame-drop; audio playback latency consistent with K-03's p95 targets.

## 25. Security
No new sensitive surface beyond what K-04 already governs for Recitation Echo; Surah Theme Matching's server-curated-only content is itself a content-safety control.

## 26. Library Requirements
Koin, Ktor, Room (SyncQueue), Compose Multiplatform, `core-kmp-player`. Reuses `core-audio-recording` via K-04 for Recitation Echo only.

## 27. Testing
- Unit: per-mode attempt-payload construction (ordering sequence, selection, missing-word answer, theme match).
- UI test: drag-drop ordering interaction responsiveness (no dropped frames in a scripted gesture test where feasible).
- Integration: Recitation Echo gating behavior matches K-03/K-06 exactly (parity test).
- Integration: Surah Theme Matching never presents unapproved/non-curated content (verified against a fixture content set).

## 28. Documentation
KDoc noting Recitation Echo is a direct reuse of K-04; noting Progressive-Reveal Memorization's scoring behavior once confirmed with product/content team.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm Game-Content APIs**
- Task ID: K-07-T01
- Objective: Verify `content` context endpoints for ayah-ordering sets, matching pairs, missing-word content, and approved theme-matching pairs.
- Dependencies: None (verification task, per Rule 30 — do not invent endpoints).
- Definition of Done: Endpoints confirmed and documented in §13.

**Task 02 — Build Ayah Ordering, Listen & Select Matching, Missing Word Screens**
- Task ID: K-07-T02
- Dependencies: K-07-T01, B-03.
- Definition of Done: All three screens render and submit correctly against staging.

**Task 03 — Build Surah Theme Matching Screen**
- Task ID: K-07-T03
- Implementation Details: Server-curated content only, no free-text/unapproved pairing path.
- Dependencies: K-07-T01, B-03.
- Definition of Done: Content-safety test (Task 06) passes.

**Task 04 — Embed K-04 as Recitation Echo**
- Task ID: K-07-T04
- Implementation Details: Direct composition of K-04's recorder flow, identical to K-06's Task 04 pattern.
- Dependencies: K-04.
- Definition of Done: Parity test confirms identical gating/fallback behavior to K-03/K-06.

**Task 05 — Build Progressive-Reveal Memorization Screen and Mode Selector Sheet**
- Task ID: K-07-T05
- Objective: Confirm scoring intent with product/content before finalizing submission behavior; build the modal entry point wiring all six modes plus lesson types.
- Dependencies: K-07-T01, K-01 (mode-selector entry point wiring).
- Definition of Done: Mode Selector Sheet correctly routes to all six game modes and the three lesson types (Surah/Letters/Tajweed).

**Task 06 — Tests**
- Task ID: K-07-T06
- Objective: Full coverage per §27, including the content-safety and Recitation-Echo-parity tests.
- Dependencies: K-07-T01–T05.
- Definition of Done: All green in CI.

## 30. Definition of Done
All six Quran Game modes live, non-recitation modes correctly submit to B-03, Recitation Echo correctly reuses K-04 with identical gating/fallback behavior, Mode Selector Sheet wired from K-01, fully tested.

## 31. Final Verification Checklist
- [ ] All six game modes implemented per FR-5's minimum list
- [ ] Recitation Echo behaves identically to K-03/K-06's record-step gating and fallback (parity verified)
- [ ] Surah Theme Matching never presents unapproved/non-curated content
- [ ] Drag-drop/tile interactions perform without frame drops
- [ ] Mode Selector Sheet correctly wired from K-01 and routes to all modes/lessons
- [ ] RTL layout verified, including drag-drop direction correctness
- [ ] Full test suite green in CI
