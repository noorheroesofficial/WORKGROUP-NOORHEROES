# K-03 — Surah Learning (Verse-by-Verse Practice)

## 1. Feature Context
Part of Feature A.5 (Quran & Arabic Learning). The core verse-by-verse practice experience — listen, repeat, optionally record, mark practiced — feeding both B-03 (non-recitation attempts) and B-04 (recitation) via the shared Recitation Recorder module (K-04).

## 2. Parent Feature
A.5 — Quran & Arabic Learning

## 3. Sub-feature
K-03 — Surah Learning (Verse-by-Verse Practice)

## 4. Objective
Render the ayah-by-ayah practice screen with Quranic-typography Arabic text, translation/transliteration toggles, inline Tajweed highlighting, audio playback, and a conditional record entry point — with correct offline playback and graceful audio-failure fallback.

## 5. Business Requirements
- FR-8: ayah-by-ayah list with audio, translation toggle, inline Tajweed-rule highlighting, recitation recorder; actions: listen, repeat, record, hint, mark practiced.
- FR-9: mic-denied/parent-disabled state falls back to listen-only, not a dead end.
- NFR: audio playback start p95 < 600ms for cached/downloaded ayah audio.
- NFR: Quranic Arabic typography — distinct Naskh/Uthmani-style typeface, correct diacritic (tashkeel) rendering verified across devices/OS versions.
- Error Handling: ayah audio load failure retries with backoff, falls back to lower-bitrate/alternate CDN source before a hard error.

## 6. Existing Architecture
`feature-learn` module conventions per K-01/K-02. Audio playback (not recording) reuses the existing `:core:media-player`/`CORE_KMP_PLAYER_INSTRUCTIONS` module used by A.3/A.4 for story/media playback — this screen's ayah audio playback is NOT part of the new `:core:audio-recording` module (that module, built in K-04, is exclusively for microphone capture).

## 7. Existing Code to Reuse
- `core-kmp-player` (existing shared playback engine per `CORE_KMP_PLAYER_INSTRUCTIONS.md`) for ayah audio play/slow-play — do not build a parallel playback engine.
- `LearningApi`/`LearningRepository` (extended here for attempt submission via B-03).
- `core-designsystem`'s Quranic-typography token (new, added here — coordinate with K-01's design-token extension task to avoid duplication).
- `core-database` offline-content-download pattern (existing, used by A.3/A.4 for downloadable media) for ayah audio caching.

## 8. Files to Create
- `feature-learn/.../surah/SurahLearningScreen.kt`
- `feature-learn/.../surah/SurahLearningViewModel.kt`
- `feature-learn/.../surah/SurahLearningUiState.kt`
- `feature-learn-domain/.../GetSurahContentUseCase.kt`
- `feature-learn-domain/.../SubmitAyahPracticedUseCase.kt` (wraps B-03's attempt submission for `attempt_type="tracing"`-style "mark practiced" events, or a dedicated non-scored progress marker if content team confirms ayah-marking isn't itself a scored attempt — verify against B-03's `attempt_type` enum before assuming)
- `feature-learn/src/commonTest/kotlin/.../SurahLearningViewModelTest.kt`

## 9. Files to Modify
- `core-network/.../api/LearningApi.kt` — add Surah/Ayah content-fetch endpoint (confirm against `content` context's existing catalog API — this may already exist as `GET /v1/content/catalog`-style endpoint per architecture doc §6 item 4, reuse rather than duplicate).
- `core-data/.../repository/ContentRepository.kt` (existing `content` context repository, if present) — extend for ayah-level fetch with Tajweed-rule markers.

## 10. Backend Requirements
Consumes the `content` context's existing Quran-content read API (Surah/Ayah/translation/Tajweed-marker data — confirm exact endpoint per Rule 30, do not invent a new one if `GET /v1/content/catalog` or a dedicated Quran-content endpoint already exists) and B-03 for "mark practiced"/practice-attempt submission.

## 11. KMP Requirements
- **Ayah list**: Quranic-typography Arabic (Naskh/Uthmani), optional transliteration, translation toggle — both independently controllable, never forced on.
- **Inline Tajweed highlighting**: rendered as inline markers within ayah text per content-service-provided rule spans.
- **Audio controls**: play + slow-play per ayah via `core-kmp-player`; retry-with-backoff on load failure, falls back to alternate CDN/bitrate before a hard error.
- **Record entry point**: conditionally rendered based on BOTH RECORD_AUDIO permission AND server-confirmed parent AI-toggle (delegates actual recording UI/logic entirely to K-04's `RecitationRecorder`/`RecitationViewModel` — this screen only decides whether to show the entry point and routes into K-04's flow).
- **Hint control**: routes to K-10's Hint Overlay.
- **"Mark practiced" action**: submits via B-03 (or a dedicated lightweight progress-marker call if `attempt_type` doesn't cleanly cover ayah-marking — confirm exact mechanism against B-03's contract before implementation).
- **States**: Default, Recording-active, AI-processing, Feedback-shown, Listen-only-mode, Error (audio load failure) — the Recording/AI-processing/Feedback states are owned by K-04's `RecitationViewModel`, this screen's `SurahLearningViewModel` observes/delegates to it rather than duplicating state.
- **Offline**: downloaded ayah audio/lesson content fully usable offline for listen/repeat/trace flows.

## 12. NextJS Requirements
N/A directly; ayah/translation/Tajweed content is managed via `N-02 Quran Content Management Extension`.

## 13. API Contract
Content-fetch: existing `content` context Quran-content endpoint (confirm exact path — do not invent). "Mark practiced"/attempt submission: B-03's `POST /v1/learning/attempts`.

## 14. Database Requirements
Reuses the existing offline-content-download Room schema (per `core-database`'s established pattern from A.3/A.4) for cached ayah audio/text; no new table required if the existing downloadable-media schema is generic enough — confirm before creating a parallel table.

## 15. Validation
N/A client-side beyond standard empty/error-state handling.

## 16. Authentication
Reuses existing child-session auth via `core-network`.

## 17. Authorization
Record entry point additionally gated on the parent AI-toggle read (via K-13's `ParentalControlsRepository`) — client-side gating is a UX convenience only; B-04 re-validates server-side regardless (defense in depth, per B-04's design).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Ayah audio load failure | Retry with backoff, fallback to alternate CDN/bitrate, then hard error only as last resort |
| Mic permission or parent toggle false | Record entry point not rendered at all; screen shows Listen-Only mode instead (delegates to K-04's Listen-Only screen variant) |
| "Mark practiced" submission failure | Non-blocking retry, does not block continued practice |

## 19. Offline First
Downloaded ayah audio/lesson content fully usable offline (listen/repeat/trace); recitation coaching requires connectivity (owned by K-04) — offline recitation attempts are not queued (per K-04's data-minimization design), self-assessment offered immediately as the offline alternative.

## 20. Local Data
Remote content → `ContentRepository`/`LearningRepository` → Room-cached downloadable content → `SurahLearningViewModel` → UI.

## 21. Localization
Translation/transliteration text localized via `core-common/localization`; both remain user-accessible, independently toggleable, never forced on (per source guidance extended to a user-accessible toggle where lesson design permits).

## 22. RTL
Full RTL rendering with correct diacritic (tashkeel) display verified across devices/OS versions — this is called out in the PRD as the single most typography-critical screen in the app; dedicated device-matrix visual-regression testing recommended (cross-ref QA requirements).

## 23. Analytics
`surah_learning_opened`, `ayah_audio_played`, `ayah_audio_slowed`, `ayah_marked_practiced` via `AnalyticsTracker`.

## 24. Performance
Audio playback start p95 < 600ms for cached/downloaded audio; prevent main-thread blocking during audio load (async via `core-kmp-player`'s existing coroutine-based API).

## 25. Security
No sensitive data beyond what K-04's recitation flow already governs (this screen itself doesn't touch audio recording).

## 26. Library Requirements
Koin, Ktor, Room, Compose Multiplatform, existing `core-kmp-player` engine. No new playback library introduced.

## 27. Testing
- Unit: translation/transliteration toggle independence.
- Unit: record-entry-point visibility logic (permission AND parent-toggle both required).
- UI test: Tajweed inline highlighting renders correctly against sample marked-up ayah text.
- Integration: audio-load-failure retry/fallback sequence.
- Integration: offline playback of downloaded content succeeds without network.

## 28. Documentation
KDoc noting the Quranic-typography requirement is a content-integrity concern, not a stylistic one, per PRD NFR.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm/Extend Content-Fetch API**
- Task ID: K-03-T01
- Objective: Verify the existing `content` context's Quran-content endpoint shape (Surah/Ayah/translation/Tajweed markers) before building a client call — do not invent a new backend endpoint here.
- Dependencies: None (research/verification task, per Rule 30).
- Definition of Done: Confirmed endpoint documented in this file's §13 (update if it differs from the placeholder assumption).

**Task 02 — Implement Content Fetch in `LearningApi`/`ContentRepository`**
- Task ID: K-03-T02
- Files to Modify: `LearningApi.kt` or existing `ContentRepository`.
- Dependencies: K-03-T01.
- Definition of Done: Content fetch succeeds against staging.

**Task 03 — Extend Offline-Download Caching for Ayah Content**
- Task ID: K-03-T03
- Files to Modify/Create: Reuse existing downloadable-media Room schema per A.3/A.4 pattern, extend if needed.
- Dependencies: K-03-T02.
- Definition of Done: Ayah audio/text downloadable and readable offline.

**Task 04 — Implement `GetSurahContentUseCase`/`SubmitAyahPracticedUseCase`**
- Task ID: K-03-T04
- Files to Create: use cases in `feature-learn-domain`.
- Dependencies: K-03-T02, B-03.
- Definition of Done: Use cases unit-tested.

**Task 05 — Implement `SurahLearningViewModel`**
- Task ID: K-03-T05
- Implementation Details: Orchestrates content state, delegates recording states to K-04's `RecitationViewModel`, handles toggle logic, analytics.
- Dependencies: K-03-T04, K-04 (recording delegation contract).
- Definition of Done: Unit tests (Task 07) pass.

**Task 06 — Build `SurahLearningScreen` Composable**
- Task ID: K-03-T06
- Implementation Details: Ayah list, Quranic typography, inline Tajweed markers, audio controls via `core-kmp-player`, conditional record entry point, hint control routing to K-10.
- Dependencies: K-03-T05, K-01-T08 (design tokens).
- Definition of Done: Renders correctly across all documented states in Compose Preview; RTL/diacritic rendering visually verified on device matrix.

**Task 07 — Tests**
- Task ID: K-03-T07
- Dependencies: K-03-T01–T06.
- Definition of Done: All green in CI.

## 30. Definition of Done
Surah Learning screen live with correct Quranic typography, working audio playback with retry/fallback, correctly gated record entry point delegating to K-04, offline support, full RTL/localization/accessibility, fully tested.

## 31. Final Verification Checklist
- [ ] Translation/transliteration toggles independently controllable, never forced on
- [ ] Record entry point rendered only when BOTH permission and parent toggle are true
- [ ] Ayah audio load failure retries with backoff and CDN/bitrate fallback before hard error
- [ ] Offline playback works for downloaded content
- [ ] Diacritic (tashkeel) rendering verified correct across device/OS matrix
- [ ] No duplicate playback engine built (reuses `core-kmp-player`)
- [ ] No duplicate recording logic built (delegates fully to K-04)
- [ ] Full test suite green in CI
