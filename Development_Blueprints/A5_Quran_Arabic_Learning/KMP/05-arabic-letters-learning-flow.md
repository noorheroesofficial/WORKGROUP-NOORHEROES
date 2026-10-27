# K-05 — Arabic Letters Learning Flow

## 1. Feature Context
Part of Feature A.5 (Quran & Arabic Learning). Teaches Arabic letters via hear-and-match, tracing, word-context, and word-building exercises, feeding attempts to B-03 and enforcing multi-session mastery.

## 2. Parent Feature
A.5 — Quran & Arabic Learning

## 3. Sub-feature
K-05 — Arabic Letters Learning Flow

## 4. Objective
Render the four Arabic Letters exercise screens (Hear & Match, Tracing, Word Context, Word-Building) in sequence, with a non-gesture-dependent tracing alternative, submitting each attempt to B-03 and never allowing single-session mastery.

## 5. Business Requirements
- FR-6: Hear-and-match, tracing, isolated/initial/medial/final form matching, harakah sound pairing, find-the-letter-in-word, build-a-word-from-sound-tiles — with spaced review scheduling.
- FR-7: play phoneme → select 1-of-4 → trace correct shape → letter in familiar word → scheduled for spaced review; mastery requires correct performance across different question forms and more than one session.
- NFR/Accessibility: tracing exercises must have a non-gesture-dependent alternative (multiple-choice shape matching) for assistive-input users.

## 6. Existing Architecture
`feature-learn` module conventions per K-01–K-04. Reuses `core-kmp-player` for phoneme audio playback (not `core-audio-recording`, since these exercises don't record the child's voice).

## 7. Existing Code to Reuse
- `LearningApi`/`LearningRepository` (B-03 attempt submission) from K-01/K-03's extensions.
- K-10's Hint Overlay routing.
- `core-designsystem` tokens.
- `core-common/permission` if tracing gesture requires any capability check (unlikely, but confirm for stylus/assistive-input detection).

## 8. Files to Create
- `feature-learn/.../letters/HearAndMatchScreen.kt` + ViewModel
- `feature-learn/.../letters/TracingScreen.kt` + ViewModel (includes non-gesture alternative UI)
- `feature-learn/.../letters/WordContextScreen.kt` + ViewModel
- `feature-learn/.../letters/WordBuildingScreen.kt` + ViewModel
- `feature-learn/.../letters/ArabicLettersUiState.kt` (shared sequencing state)
- `feature-learn-domain/.../SubmitLetterAttemptUseCase.kt`
- `feature-learn/src/commonTest/kotlin/.../ArabicLettersFlowTest.kt`

## 9. Files to Modify
- `LearnRoute` — add `HearAndMatch`, `Tracing`, `WordContext`, `WordBuilding` destinations.

## 10. Backend Requirements
Consumes B-03 (`POST /v1/learning/attempts`, `attempt_type: "matching"|"tracing"`) and the `content` context's letter-lesson content endpoint (confirm exact path per Rule 30 before assuming).

## 11. KMP Requirements
- **Hear & Match**: phoneme playback via `core-kmp-player`, 1-of-4 letter selection UI.
- **Tracing**: gesture-based tracing canvas PLUS a non-gesture-dependent multiple-choice shape-matching alternative, toggleable/auto-offered for assistive-input users (detected via platform accessibility service state where feasible, or a persistent user-accessible toggle).
- **Word Context**: renders the letter within a familiar, content-team-approved word.
- **Word-Building**: sound-tile drag/tap-to-build game mode.
- **Sequencing**: hear-and-match → trace → word-context, per FR-7, with each step's attempt submitted individually to B-03 (not batched), so B-03's multi-session mastery enforcement operates on real historical data.
- **Isolated/initial/medial/final letter-form matching, harakah sound pairing, find-the-letter-in-word**: implemented as variant question types within Hear & Match/Word Context screens, driven by content-service question metadata, not hardcoded per-letter logic.
- **Spaced review**: no client-side scheduling logic — entirely server-driven via B-06, this flow just submits attempts.

## 12. NextJS Requirements
N/A directly.

## 13. API Contract
`POST /v1/learning/attempts` per B-03 §13, `attempt_type: "matching"` (hear-and-match, word-context, word-building) or `"tracing"` (tracing screen, including the non-gesture alternative — same attempt_type, different `answer_payload` shape).

## 14. Database Requirements
No new local persistence; letter-lesson content cached via the existing offline-content-download pattern (shared with K-03).

## 15. Validation
N/A client-side beyond standard input handling; server-side (B-03) is authoritative on correctness evaluation.

## 16. Authentication
Reuses existing child-session auth.

## 17. Authorization
N/A beyond authenticated child session.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Audio playback failure | Retry/fallback via `core-kmp-player`'s existing error handling |
| Attempt submission failure | Non-blocking retry, does not block continued practice |
| Tracing gesture input unavailable/unreliable | Non-gesture alternative always accessible, never a dead end |

## 19. Offline First
Lesson content/audio downloadable and usable offline; attempt submission requires connectivity (queued for sync on reconnect per the app's standard offline-write pattern via `core-data`'s `SyncQueue`, consistent with other non-recitation attempt types).

## 20. Local Data
Content cached via existing downloadable-content Room schema; attempt submissions queued via `core-data`'s `SyncQueue` when offline, synced on reconnect.

## 21. Localization
All instructional copy and content localized via `core-common/localization`.

## 22. RTL
Full RTL layout; letter-shape rendering itself is inherently script-correct (Arabic letterforms), UI chrome around it mirrors for RTL locales.

## 23. Analytics
`arabic_letter_lesson_started`, `arabic_letter_traced`, `arabic_letter_matched`, `arabic_word_built` via `AnalyticsTracker`.

## 24. Performance
Standard Compose recomposition hygiene; tracing canvas must not introduce input lag (use efficient gesture-tracking, avoid excessive recomposition during drag).

## 25. Security
No sensitive data; standard authenticated-session flow.

## 26. Library Requirements
Koin, Ktor, Room (via `core-data`'s `SyncQueue` for offline attempt queuing), Compose Multiplatform, `core-kmp-player`.

## 27. Testing
- Unit: sequencing logic (hear-and-match → trace → word-context) submits each step independently.
- UI test: non-gesture tracing alternative is always reachable and functionally equivalent.
- Integration: offline attempt submission queues via `SyncQueue` and syncs on reconnect.

## 28. Documentation
KDoc noting the non-gesture alternative is an accessibility requirement, not an optional enhancement.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm Letter-Lesson Content API**
- Task ID: K-05-T01
- Objective: Verify the `content` context's letter-lesson endpoint shape before building client calls.
- Dependencies: None (verification task).
- Definition of Done: Endpoint confirmed and documented in §13.

**Task 02 — Implement `SubmitLetterAttemptUseCase`**
- Task ID: K-05-T02
- Dependencies: K-05-T01, B-03.
- Definition of Done: Use case unit-tested.

**Task 03 — Build Hear & Match, Word Context, Word-Building Screens**
- Task ID: K-05-T03
- Dependencies: K-05-T02.
- Definition of Done: Screens render correctly in Compose Preview.

**Task 04 — Build Tracing Screen with Non-Gesture Alternative**
- Task ID: K-05-T04
- Implementation Details: Gesture canvas + multiple-choice shape-matching fallback, both submitting to the same `attempt_type: "tracing"` contract.
- Dependencies: K-05-T02.
- Definition of Done: UI test confirms the alternative is reachable and functionally equivalent.

**Task 05 — Wire Sequencing & Routes**
- Task ID: K-05-T05
- Files to Modify: `LearnRoute`.
- Dependencies: K-05-T03, K-05-T04.
- Definition of Done: Full hear→trace→word-context sequence navigable end-to-end.

**Task 06 — Tests**
- Task ID: K-05-T06
- Dependencies: K-05-T01–T05.
- Definition of Done: All green in CI.

## 30. Definition of Done
All four Arabic Letters screens live, sequenced correctly, non-gesture tracing alternative verified, offline content/attempt handling working, fully tested.

## 31. Final Verification Checklist
- [ ] Non-gesture tracing alternative always available and functionally equivalent
- [ ] Each exercise step submits its own attempt (no batching that would defeat multi-session mastery tracking)
- [ ] Offline attempt submission queues and syncs correctly
- [ ] RTL/localization verified
- [ ] Full test suite green in CI
