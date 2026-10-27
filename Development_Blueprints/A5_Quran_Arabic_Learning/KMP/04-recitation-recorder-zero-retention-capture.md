# K-04 — Recitation Recorder & Zero-Retention Audio Capture

## 1. Feature Context
Part of Feature A.5 (Quran & Arabic Learning). The client-side counterpart to B-04's zero-retention guarantee — captures a child's recitation attempt entirely in memory, streams it to the server, and guarantees no audio file is ever written to device storage at any point, even temporarily.

## 2. Parent Feature
A.5 — Quran & Arabic Learning

## 3. Sub-feature
K-04 — Recitation Recorder & Zero-Retention Audio Capture

## 4. Objective
Build a new `core-audio-recording` module exposing an API structurally incapable of file-based recording, and a `RecitationViewModel` state machine that explicitly nulls its audio buffer reference immediately on reaching a terminal state — mirroring B-04's server-side zero-retention guarantee on-device.

## 5. Business Requirements
- FR-9: mic-denied/parent-disabled state falls back to listen-only, not a dead end.
- FR-10: feedback never implies religious/spiritual validity — never a numeric score shown to the child.
- FR-11: raw audio not retained after processing by default.
- FR-12: low-confidence results fall back to reference-comparison self-assessment.
- FR-13: parent per-child mic/AI disable — no UI path bypasses it.
- Edge Case 2: parent disabling mid-session must gracefully exit to listen-only on next app-state check, never a dangling broken record control.
- Edge Case 5: no microphone hardware → recitation UI hidden entirely (not shown-disabled), via device-capability detection at app start.
- Edge Case 10: network-drop mid-upload retry allowed, but raw audio still discarded post-processing.
- §7 Android AI Code-Generation Prompt: the full set of hard privacy requirements for this module (adapted below to the project's actual Koin/Ktor/Room-based KMP architecture rather than the prompt's original Hilt/Retrofit assumptions).

## 6. Existing Architecture
New **`core-audio-recording`** KMP module (mirrors the existing `core-kmp-player` module's structure/placement but is a distinct module scoped purely to microphone capture, per PRD §6.1's explicit note that it's "separate from `:core:media-player` used for playback"). DI via Koin (project-wide standard, not Hilt). Networking via Ktor with streaming multipart support (not Retrofit+OkHttp). No Room/local-database involvement in this module whatsoever — this is the one module in the entire app that must NEVER touch `core-database`, by design.

## 7. Existing Code to Reuse
- `core-common/permission`'s platform-agnostic runtime permission abstraction — for RECORD_AUDIO permission checks (do not reimplement platform permission handling).
- `core-network`'s `HttpClient` factory — extended here with streaming multipart-from-`ByteArray` support (confirm Ktor's multipart API supports streaming from an in-memory buffer without an intermediate file; this is a hard requirement, not an implementation preference).
- `core-analytics`'s `AnalyticsTracker` — but note: analytics event data classes for this feature must be typed with NO field capable of carrying audio/transcript data (structural, not just convention).
- `core-designsystem` tokens from K-01-T08 (node-state/feedback-iconography extension) for the coaching-feedback visual language.
- K-13's `ParentalControlsRepository` for the server-confirmed AI-toggle read.

## 8. Files to Create
- `core-audio-recording/src/commonMain/kotlin/.../RecitationRecorder.kt` (expect/actual interface — `start()`, `stop(): ByteArray`, streaming-upload helper; NO file-path-accepting method exists anywhere in this API)
- `core-audio-recording/src/androidMain/kotlin/.../RecitationRecorder.android.kt` (actual impl using `AudioRecord` with a `ByteArray` sink, NOT `MediaRecorder`-to-file)
- `core-audio-recording/src/iosMain/kotlin/.../RecitationRecorder.ios.kt` (actual impl using the iOS audio-capture equivalent with an in-memory buffer sink)
- `feature-learn/.../recitation/RecitationViewModel.kt`
- `feature-learn/.../recitation/RecitationUiState.kt` (sealed state: `Idle, Recording, Uploading, AwaitingFeedback, FeedbackShown, FallbackToReference, Error`)
- `feature-learn/.../recitation/RecitationRecorderOverlay.kt` (Composable)
- `feature-learn/.../recitation/AiPronunciationFeedbackScreen.kt` (Composable)
- `feature-learn/.../recitation/ListenOnlySelfAssessmentScreen.kt` (Composable)
- `feature-learn/.../recitation/MicPermissionRationaleModal.kt` (Composable)
- `feature-learn-domain/.../SubmitRecitationUseCase.kt`
- `core-network/.../api/RecitationApi.kt` (Ktor streaming-multipart client for `POST /v1/learning/recitation`)
- `feature-learn/src/commonTest/kotlin/.../RecitationViewModelTest.kt` (includes weak-reference GC test)
- `feature-learn/src/androidInstrumentedTest/kotlin/.../RecitationRecorderPrivacyInstrumentedTest.kt` (CI-blocking file-system-scan test)

## 9. Files to Modify
- App-level Koin module registration — wire `core-audio-recording` DI.
- K-03's `SurahLearningViewModel` — delegate recording-state observation to this module rather than duplicating.
- CI pipeline config — mark the privacy instrumented test as a mandatory, non-bypassable gate on any PR touching `core-audio-recording` (mirrors B-04's backend CI gate).

## 10. Backend Requirements
Consumes B-04's `POST /v1/learning/recitation` exclusively.

## 11. KMP Requirements
- **`RecitationRecorder` public API**: ONLY `start()`, `stop(): ByteArray`, and a streaming-upload helper — structurally impossible for any caller to request file-based recording, since no method in the public API accepts or returns a file path.
- **Audio capture**: directly into an in-memory buffer (`AudioRecord`/platform-equivalent with a `ByteArray`/`ByteBuffer` sink) — never a file-writing recorder API.
- **Upload**: streamed to the server as a multipart request body directly from memory via `RecitationApi`, never written to a temp file on device storage at any point in the lifecycle, even transiently.
- **`RecitationViewModel` state machine**: `Idle → Recording → Uploading → AwaitingFeedback → FeedbackShown(confidenceBand, templateText) | FallbackToReference | Error`. On entering `FeedbackShown`, `FallbackToReference`, or `Error`, explicitly set the held audio `ByteArray` reference to `null` in the same state-transition code path — not relying on scope-exit alone.
- **Record-button gating**: visible only when BOTH RECORD_AUDIO runtime permission is granted AND a server-confirmed parent AI-toggle value (fetched via K-13's `ParentalControlsRepository`) is true; if either is false/denied, render `ListenOnlySelfAssessmentScreen` instead, with zero record-button nodes anywhere in the composable tree.
- **Device-capability detection (Edge Case 5)**: at app start, detect absence of microphone hardware and hide the recitation-recording UI entirely (identical UX to parent-disabled), not shown-disabled.
- **`AiPronunciationFeedbackScreen`**: waveform-style decorative visual (not data-precise), 1-2 categorical coaching-copy strings keyed by `confidence_band`, "Try Again"/"Continue" actions — NEVER renders a numeric score, percent, or confidence value as visible text anywhere on the screen.
- **`ListenOnlySelfAssessmentScreen`**: rendered for mic-denied/parent-disabled/no-hardware/low-confidence-fallback cases — a single consistent screen variant reused across all these triggers.
- **`MicPermissionRationaleModal`**: one-time explainer, non-repeated nagging beyond the platform-standard one-time re-prompt affordance.
- **Mid-session parent-disable (Edge Case 2)**: on next app-state check (e.g., process resume, or a periodic toggle re-check while the recorder screen is active), gracefully exit any in-progress recording UI to listen-only mode — never leave a dangling record button that silently fails.
- **Offline (Edge Case per §6.7)**: recitation/AI feedback explicitly requires connectivity; client shows a clear "needs internet" state rather than queuing raw audio locally (queuing would extend on-device audio lifetime, in tension with data minimization) — self-assessment offered immediately as the offline alternative.
- **Hint control**: routes to K-10, available during Surah Learning's recitation flow same as any other exercise.

## 12. NextJS Requirements
N/A directly (this module consumes B-04's runtime behavior, which itself is governed by B-10's template library and B-11's confidence threshold — no direct admin dependency at the client layer).

## 13. API Contract
`POST /v1/learning/recitation` per B-04 §13, client-side: `RecitationApi.submitRecitation(audioBytes: ByteArray, ayahId: String, childId: String): RecitationFeedbackDto` via Ktor streaming multipart directly from the `ByteArray` (no `File` object ever constructed).

## 14. Database Requirements
**None.** This is the one module that must never write to `core-database`/Room in any form — no `RecitationCacheEntity`, no queued-upload table, nothing. This absence is an intentional architectural property (mirrors B-04's "nothing to back up" DR stance), not an oversight.

## 15. Validation
N/A beyond standard audio-format/size sanity checks before upload (delegated to the platform capture API's own constraints).

## 16. Authentication
Reuses existing child-session auth via `core-network`'s `HttpClient`.

## 17. Authorization
Client-side gate (permission + parent-toggle, both required for the record button to render) is a UX convenience only — B-04 re-validates server-side on every request regardless, so this client-side gate is not a substitute for that defense-in-depth control, merely a good-UX front door to it.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Parent disables mid-session (Edge Case 2) | Graceful exit to listen-only on next app-state check, no dangling broken control |
| Network drop mid-upload (Edge Case 10) | Local retry of the in-memory buffer only until server ack; raw audio still discarded (buffer nulled) post-processing regardless of retry outcome — no extended in-memory retention loophole |
| Inference low-confidence/error from B-04 | Route to `FallbackToReference`/`ListenOnlySelfAssessmentScreen`, not a degraded feedback screen |
| No microphone hardware (Edge Case 5) | Recitation UI hidden entirely at app start, identical UX to parent-disabled |
| Offline | Clear "needs internet" state, no local audio queuing |

## 19. Offline First
Recitation explicitly requires connectivity by design (see §11) — this is a deliberate exception to the app's general offline-first posture, justified by the data-minimization principle (queuing audio would extend its on-device lifetime).

## 20. Local Data
None (see §14) — the entire point of this module is the absence of local audio persistence.

## 21. Localization
Coaching-phrase copy (`templateText`) is server-supplied per the child's locale (via B-10's `locale`-scoped templates) — the client renders whatever text is returned, never synthesizes or translates it locally.

## 22. RTL
Full RTL layout for Arabic/Urdu coaching-feedback copy and screen layout.

## 23. Analytics
`recitation_record_started`, `recitation_record_submitted`, `recitation_ai_feedback_shown` (confidence_band only), `recitation_fallback_to_reference_shown`, `recitation_listen_only_used` via `AnalyticsTracker` — the event parameter data classes for these events must be typed with no field capable of holding raw audio, transcript text, or numeric confidence, enforced structurally (a Kotlin data class simply has no such field, not merely "please don't populate it").

## 24. Performance
p95 round-trip < 3s target (communicated via an explicit "Listening... checking your recitation" loading state, distinct from instant UI feedback elsewhere in the app, honestly setting expectations rather than implying instant judgment).

## 25. Security
This module's restricted public API (no file-path-accepting methods) is itself a security control, not just engineering convenience — it makes a class of privacy bugs structurally impossible rather than merely discouraged, per the PRD's explicit framing. This is the client-side mirror of B-04's server-side zero-retention guarantee, and both must be verified by CI-blocking automated tests (Task 09 below), not code-review checklists alone.

## 26. Library Requirements
Koin (DI), Ktor (streaming multipart from `ByteArray`, NOT Retrofit+OkHttp as the earlier PRD draft assumed — corrected here to match the project's actual Ktor-based `core-network`), platform-native audio-capture APIs (`AudioRecord` on Android, AVAudioEngine/equivalent in-memory capture on iOS — NOT `MediaRecorder`-to-file on Android). No Room/local-database dependency in this module.

## 27. Testing
- **Unit**: weak-reference test — hold a `WeakReference` to the audio `ByteArray`, trigger the transition to `FeedbackShown`/`Error`/`FallbackToReference`, force GC, assert the buffer becomes garbage-collectable shortly after (proves the explicit-null discipline, not just scope-exit reliance).
- **UI test**: scan the full composable tree when permission or parent-toggle is false — assert zero nodes with a "record" content-description/semantics tag exist anywhere.
- **UI test**: scan all text nodes on `AiPronunciationFeedbackScreen` — assert none match a regex for a standalone number followed by `%` or a decimal between 0 and 1 (proves no numeric score ever renders).
- **Instrumented test (CI-blocking, the signature privacy guarantee)**: start a recording, stop it (obtain a `ByteArray`), submit via a mocked repository, then use a file-system scanner walking the app's full sandboxed storage directory tree, asserting ZERO new files were created during the entire test run.
- **Integration**: full submit→feedback flow with mocked server responses for high-confidence, low-confidence-fallback, and service-error scenarios, verifying identical safe UX for the latter two (same `ListenOnlySelfAssessmentScreen`/`FallbackToReference` path).
- **Integration**: Edge Case 2 — simulated mid-session parent-disable triggers graceful exit to listen-only on the next app-state check.

## 28. Documentation
KDoc on `RecitationRecorder` explicitly stating the "no file-path method exists" design constraint and why (structural privacy guarantee). KDoc on `RecitationViewModel`'s state machine documenting the explicit-null discipline as load-bearing, not optional cleanup.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Scaffold `core-audio-recording` Module**
- Task ID: K-04-T01
- Objective: Create the new KMP module with `commonMain`/`androidMain`/`iosMain` source sets, mirroring `core-kmp-player`'s module structure but as a fully separate module.
- Why This Is Required: PRD explicitly requires this to be a distinct module from the media-player module.
- Dependencies: None.
- Do Not Change: Do not add this module as a dependency of `core-database` or vice versa.
- Definition of Done: Module builds and is registered in the project's module graph.

**Task 02 — Implement `RecitationRecorder` (expect/actual)**
- Task ID: K-04-T02
- Files to Create: common `expect` interface + `androidMain`/`iosMain` `actual` implementations.
- Implementation Details: Public API restricted to `start()`, `stop(): ByteArray`, streaming-upload helper. Android impl uses `AudioRecord` with a `ByteArray` sink (not `MediaRecorder`). iOS impl uses an equivalent in-memory-buffer capture API.
- Security: No method anywhere in this class accepts or returns a file path — verify via code review checklist AND the structural absence itself (there's no test that can "prove a negative" here beyond API surface review, so this is enforced by design/review, backed by Task 09's behavioral proof).
- Dependencies: K-04-T01.
- Definition of Done: `start()`/`stop()` work correctly on both platforms in manual testing.

**Task 03 — Implement Streaming Multipart Upload in `RecitationApi`**
- Task ID: K-04-T03
- Files to Create: `core-network/.../api/RecitationApi.kt`.
- Implementation Details: Ktor multipart request streamed directly from the `ByteArray`, no intermediate `File` object constructed at any point.
- Dependencies: B-04 (backend contract), K-04-T01.
- Definition of Done: Upload succeeds against staging's mocked pronunciation-inference endpoint.

**Task 04 — Implement `RecitationViewModel` State Machine**
- Task ID: K-04-T04
- Files to Create: `RecitationViewModel.kt`, `RecitationUiState.kt`.
- Implementation Details: Full sealed-state machine per §11; explicit-null discipline on every terminal-state transition, in the same code path as the transition itself (not a separate cleanup call that could be skipped).
- Existing Files to Reuse: `AnalyticsTracker`, K-13's `ParentalControlsRepository`.
- Dependencies: K-04-T02, K-04-T03, K-13.
- Definition of Done: Unit tests (Task 09) pass, including the weak-reference GC test.

**Task 05 — Implement Device-Capability Detection (Edge Case 5)**
- Task ID: K-04-T05
- Implementation Details: App-start check for microphone hardware presence; result cached in memory for the session, consumed by the record-button-visibility gate.
- Dependencies: K-04-T01.
- Definition of Done: On a simulated no-mic device/emulator config, recitation UI is confirmed absent (not disabled).

**Task 06 — Build `RecitationRecorderOverlay` and `AiPronunciationFeedbackScreen`**
- Task ID: K-04-T06
- Implementation Details: Overlay UI for active recording; feedback screen with waveform-decorative visual, categorical coaching copy, never a numeric score.
- Existing Files to Reuse: `core-designsystem` feedback-iconography tokens (K-01-T08).
- Dependencies: K-04-T04.
- Definition of Done: Screens render correctly in Compose Preview across all states; manual scan confirms no numeric score text present.

**Task 07 — Build `ListenOnlySelfAssessmentScreen` and `MicPermissionRationaleModal`**
- Task ID: K-04-T07
- Dependencies: K-04-T04.
- Definition of Done: Screens render correctly for mic-denied/parent-disabled/no-hardware/low-confidence-fallback triggers, verified to be the same reused component across all four.

**Task 08 — Wire Mid-Session Parent-Disable Handling (Edge Case 2)**
- Task ID: K-04-T08
- Implementation Details: Re-check the parent AI-toggle on app-state resume/periodic check while the recorder is active; on disable, transition gracefully to `ListenOnlySelfAssessmentScreen`.
- Dependencies: K-04-T04, K-13.
- Definition of Done: Integration test (Task 09) confirms graceful transition, no dangling broken control.

**Task 09 — Write Privacy-Critical Tests**
- Task ID: K-04-T09
- Task Name: Weak-Reference GC Test, Record-Button-Absence UI Test, Numeric-Score-Absence UI Test, Instrumented File-System-Scan Test
- Objective: Prove the client-side zero-retention and no-judgment guarantees automatically.
- Implementation Details: Per §27's four privacy-critical test descriptions; the instrumented file-system-scan test is the signature CI-blocking guarantee, mirroring B-04's backend equivalent.
- Dependencies: K-04-T02–T08.
- Definition of Done: All tests pass and the instrumented test is configured as a mandatory, non-bypassable CI gate on any PR touching `core-audio-recording`.

**Task 10 — Full Integration Test Suite**
- Task ID: K-04-T10
- Objective: Remaining coverage per §27 (high/low/error confidence scenarios, offline state).
- Dependencies: K-04-T01–T09.
- Definition of Done: All green in CI.

**Task 11 — Documentation**
- Task ID: K-04-T11
- Dependencies: K-04-T02, K-04-T04.
- Definition of Done: KDoc complete per §28.

## 30. Definition of Done
`core-audio-recording` module live with a structurally file-path-free public API; `RecitationViewModel` explicit-null discipline proven via weak-reference test; instrumented file-system-scan test proves zero on-device audio persistence (CI-blocking); no numeric score ever renders; Edge Cases 2, 5, and 10 verified; full RTL/localization support; fully tested and documented.

## 31. Final Verification Checklist
- [ ] `RecitationRecorder`'s public API has no method accepting or returning a file path
- [ ] Audio captured directly to an in-memory buffer, never `MediaRecorder`-to-file
- [ ] Audio streamed to server directly from memory, never via an intermediate temp file
- [ ] Audio `ByteArray` reference explicitly nulled in the same code path as every terminal-state transition
- [ ] Weak-reference test confirms buffer becomes garbage-collectable shortly after terminal state
- [ ] Instrumented file-system-scan test confirms ZERO new files created during a full record→submit flow (CI-blocking)
- [ ] Record button rendered only when BOTH permission AND parent toggle are true; zero record-content-description nodes otherwise
- [ ] No numeric score/percent/confidence value ever rendered as visible text
- [ ] No microphone hardware → recitation UI hidden entirely, not shown-disabled
- [ ] Mid-session parent-disable gracefully exits to listen-only, no dangling broken control
- [ ] `core-audio-recording` has zero dependency on `core-database`/Room
- [ ] Analytics event data classes structurally cannot carry audio/transcript/raw-confidence data
- [ ] Uses Koin/Ktor per actual project architecture (not Hilt/Retrofit as in the earlier PRD draft)
- [ ] Full test suite green in CI, instrumented privacy test is a mandatory CI gate
