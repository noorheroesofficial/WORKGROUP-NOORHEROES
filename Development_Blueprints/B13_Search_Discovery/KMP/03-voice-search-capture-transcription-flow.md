# K-03 — Voice Search Capture & Transcription Flow

## 1. Feature Context
Part of Feature B.13 (Search & Discovery). The client-side counterpart to B-03, reusing the `core-audio-recording` module established in Feature A.5 (its own K-04 blueprint) — this blueprint does **not** build a second, parallel audio-capture implementation.

## 2. Parent Feature
B.13 — Search & Discovery

## 3. Sub-feature
K-03 — Voice Search Capture & Transcription Flow

## 4. Objective
Implement the voice-search sub-state machine (`Idle → Listening → Transcribing → Results | ClarificationNeeded | Error`) using `core-audio-recording`'s in-memory-buffer-only recorder, streaming directly to B-03 via Ktor multipart, with the identical zero-retention discipline established in A.5.

## 5. Business Requirements
- FR-6: explicit mic affordance only, parent permission required, no ambient listening.
- §1.13: distinct "Listening..." and "Searching..."/Transcribing states — two honest states, not one ambiguous spinner.
- §2.1: calm, pulsing waveform/glow during capture — never an alarming or overly energetic visual.
- Edge Case 2: low-confidence transcription → Clarification Prompt, never a silent search of garbled text.
- Edge Case 12: interrupted session → partial audio discarded cleanly, search bar returns to ready state, never a stuck "processing" state.
- §1.15: mic permission denied/unavailable → graceful fallback to text-only search, no nagging re-prompt beyond the platform-standard one-time OS re-prompt.

## 6. Existing Architecture
Reuses `core-audio-recording` (built in A.5's K-04) exactly as-is — its public API (`start()`, `stop(): ByteArray`, streaming-upload helper) has no file-path-accepting method anywhere, structurally preventing file-based recording. This blueprint adds voice-search-specific state (`SearchVoiceViewModel`/state extension) and a new `SearchVoiceApi` (Ktor) call to B-03's endpoint, following A.5's `RecitationApi`/`RecitationViewModel` as the direct architectural precedent.

## 7. Existing Code to Reuse
- `core-audio-recording`'s `RecitationRecorder`-equivalent abstraction (A.5 K-04) — same `start()`/`stop(): ByteArray` API, reused for voice search's mic capture (may share the exact same recorder class if its API is generic enough, or a thin voice-search-specific wrapper over the same underlying in-memory-buffer primitive — confirm during implementation which is cleaner, but never a second `AudioRecord`/file-capable implementation).
- `core-common/permission`'s platform-agnostic RECORD_AUDIO permission abstraction.
- `core-network`'s `HttpClient` (Ktor) with streaming multipart-from-`ByteArray` support (already extended for this purpose in A.5).
- `core-analytics`'s `AnalyticsTracker`.
- `core-designsystem` tokens for the calm waveform/glow visual language (reuse A.5's "Listening... checking" tone).

## 8. Files to Create
- `feature-search/src/commonMain/kotlin/.../search/voice/SearchVoiceViewModel.kt` (or extension of `SearchViewModel` — implementation choice, but state machine must be isolated/testable).
- `feature-search/src/commonMain/kotlin/.../search/voice/SearchVoiceUiState.kt` (sealed: `Idle, Listening, Transcribing, Results(data), ClarificationNeeded, Error`).
- `feature-search/src/commonMain/kotlin/.../search/voice/VoiceListeningScreen.kt` (Composable).
- `feature-search/src/commonMain/kotlin/.../search/voice/VoiceTranscribingScreen.kt` (Composable).
- `feature-search/src/commonMain/kotlin/.../search/voice/VoiceClarificationPromptScreen.kt` (Composable).
- `core-network/src/commonMain/kotlin/.../api/SearchVoiceApi.kt` (Ktor streaming-multipart client for `POST /v1/search/voice`).
- `feature-search/src/commonTest/kotlin/.../SearchVoiceStateMachineTest.kt` (includes weak-reference GC test).
- `feature-search/src/androidInstrumentedTest/kotlin/.../SearchVoicePrivacyInstrumentedTest.kt` (CI-blocking storage-scan test).

## 9. Files to Modify
- `SearchViewModel.kt`/`SearchModule.kt` (K-01) — wire voice sub-flow entry from the mic tap.
- App-level Koin registration — register `SearchVoiceApi`.

## 10. Backend Requirements
Consumes B-03 exclusively: `POST /v1/search/voice`.

## 11. KMP Requirements
- State machine: `Idle → Listening → Transcribing → Results(data) | ClarificationNeeded | Error`, using `core-audio-recording`'s recorder capturing directly into an in-memory `ByteArray`, never a file.
- On reaching `Results`, `ClarificationNeeded`, or `Error`, explicitly null the held audio buffer reference in the same state-transition code path — not relying on scope-exit alone (identical discipline to A.5's `RecitationViewModel`).
- Mic tap → `Listening` state only after explicit tap (never ambient) → render `VoiceListeningScreen` (calm pulsing waveform, "Listening..." text, "Cancel" link).
- On capture stop → `Transcribing` state → render `VoiceTranscribingScreen` ("Searching..." text) → call `SearchVoiceApi` streaming the `ByteArray` directly (no temp file).
- On `clarification_needed: true` response → `ClarificationNeeded` state → render `VoiceClarificationPromptScreen` (distinct screen, never the Results screen).
- On confident response → `Results(data)` state → hand off to K-02's `SearchResultsScreen` rendering path with the returned results.
- Mic-permission denied/unavailable → fall back directly to K-01's text-search entry, no dead-end state.
- Interrupted session (e.g., incoming call, backgrounding mid-Listening) → discard partial buffer, return to `Idle`, never a stuck `Transcribing` state.
- No microphone hardware detected at app start → hide the mic affordance entirely (mirrors A.5's Edge Case 5 handling), not shown-disabled.

## 12. NextJS Requirements
N/A.

## 13. API Contract
`POST /v1/search/voice` per B-03 §13, client-side: `SearchVoiceApi.submitVoiceSearch(audioBytes: ByteArray): VoiceSearchResponseDto` via Ktor streaming multipart directly from the `ByteArray` (no `File` object ever constructed, matching A.5's `RecitationApi` pattern exactly).

## 14. Database Requirements
**None.** This is, like A.5's recitation module, a flow that must never touch `core-database`/Room in any form — no queued-upload table, nothing, by the same intentional-absence design rationale as A.5 K-04 §14.

## 15. Validation
Minimum capture-duration guard client-side (avoid submitting a near-zero-length buffer) before invoking the upload — a UX guard; B-03 also validates server-side.

## 16. Authentication
Standard app-wide child-session bearer token via `core-network`'s interceptor.

## 17. Authorization
N/A beyond standard session.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Mic permission denied | Fallback to text-only search, no nagging re-prompt beyond platform-standard |
| No mic hardware | Mic affordance hidden entirely at app start |
| Session interrupted mid-capture | Buffer discarded, state returns to `Idle` |
| Low-confidence transcription | `ClarificationNeeded` screen, never `Results` |
| Network/provider failure | `Error` state with retry, buffer still nulled |

## 19. Offline First
Voice search explicitly requires connectivity (mirrors A.5) — offline shows a clear "needs internet" state; K-01's text search remains available as the offline alternative (no raw-audio queuing, which would extend on-device audio lifetime).

## 20. Local Data
None (see §14).

## 21. Localization
"Listening...", "Searching...", clarification-prompt copy all localized (English/Hindi/Arabic/Urdu); no hardcoded strings.

## 22. RTL
Waveform/glow visual and "Cancel" link mirror correctly in RTL layout.

## 23. Analytics
`search_voice_listening_started`, `search_voice_transcription_low_confidence` (fired only on the server-confirmed low-confidence response, never a client-side heuristic guess).

## 24. Performance
- No main-thread blocking during capture (recorder runs on its established coroutine dispatcher per `core-audio-recording`'s existing design).
- Buffer nulled promptly to allow garbage collection — verified by weak-reference test.
- No ANR risk from long-running capture (bounded max-capture-duration, consistent with any existing cap in `core-audio-recording`).

## 25. Security
- **Zero-retention is this blueprint's defining guarantee**, verified by an instrumented privacy test identical in structure to A.5's: record a test query, submit it, then scan the app's full sandboxed storage directory tree and assert zero new files were created during the entire test run.
- No parallel/duplicate audio-capture implementation — a second implementation would itself be a privacy-architecture risk.

## 26. Library Requirements
`core-audio-recording` (reused, not reimplemented), Ktor (via `core-network`), Koin. No Hilt, no Retrofit+OkHttp.

## 27. Testing
- Unit: state-machine transition correctness for every path (`Idle→Listening→Transcribing→Results`, `...→ClarificationNeeded`, `...→Error`, interrupted-session→`Idle`).
- Weak-reference test: confirm the held audio buffer becomes garbage-collectable shortly after reaching a terminal state.
- UI test: `ClarificationPromptScreen` and `Results` screen are visually/structurally distinct; `Results` never renders when `clarification_needed` is true.
- **Instrumented privacy test (CI-blocking, mandatory):** full storage-directory-tree scan post-flow, zero new files asserted.
- Permission-denied fallback test.
- No-hardware-detected test (mic affordance absent, not disabled).

## 28. Documentation
KDoc explicitly stating the zero-file-write guarantee and pointing to the instrumented test enforcing it; note on reuse of A.5's `core-audio-recording` (not a new module).

## 29. AI Coding Agent Implementation Steps
**Task 01 — Confirm core-audio-recording Reusability**
Objective: verify A.5's recorder API is generic enough for voice search's needs; if a thin wrapper is required, keep it minimal and delegate entirely to the existing module.
Do not change: `core-audio-recording`'s public API surface.

**Task 02 — Define SearchVoiceUiState & State Machine**
Files to create: `SearchVoiceUiState.kt`, `SearchVoiceViewModel.kt`.
Business rules: explicit buffer null on every terminal-state transition.

**Task 03 — Implement SearchVoiceApi (Ktor Streaming Multipart)**
Files to create: `SearchVoiceApi.kt`.

**Task 04 — Build Voice Flow Screens**
Objective: `VoiceListeningScreen`, `VoiceTranscribingScreen`, `VoiceClarificationPromptScreen`, matching Figma.
Files to create: three Composables.

**Task 05 — Wire Mic-Permission & No-Hardware Handling**
Objective: fallback-to-text and hide-affordance-entirely paths.
Files to modify: `SearchViewModel.kt`/`SearchModule.kt` (K-01).

**Task 06 — Add Weak-Reference & State-Machine Tests**
Files to create: `SearchVoiceStateMachineTest.kt`.

**Task 07 — Add Instrumented Privacy Test (highest priority)**
Files to create: `SearchVoicePrivacyInstrumentedTest.kt`.

**Task 08 — Wire Analytics & Final Review**
Objective: confirm zero duplicate audio-capture implementation exists in the codebase after this change.

## 30. Definition of Done
- Full voice state machine functional and tested.
- Instrumented zero-file-write test passes as a CI-blocking gate.
- Clarification and Results screens verified structurally distinct.
- Graceful fallback for denied permission / no hardware.

## 31. Final Verification Checklist
- [ ] No second audio-capture implementation introduced — `core-audio-recording` reused as-is.
- [ ] Zero files written to device storage during the entire voice-search flow — verified by instrumented test.
- [ ] Audio buffer reference explicitly nulled on every terminal state.
- [ ] `ClarificationNeeded` and `Results` are structurally distinct, never both renderable for the same response.
- [ ] Mic-denied and no-hardware cases both handled gracefully, without a dead end.
- [ ] Interrupted session returns cleanly to `Idle`, never stuck in `Transcribing`.
