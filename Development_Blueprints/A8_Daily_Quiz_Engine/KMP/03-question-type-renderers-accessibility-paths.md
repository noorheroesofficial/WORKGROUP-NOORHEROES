# K-03 — Question Type Renderers & Accessibility Interaction Paths

## 1. Feature Context
NoorHeroes — Feature A.8 Daily Quiz & Quiz Completion Engine. Source PRD §2.2, §6.2, §7 item 3, FR-2, Edge Case 7, Screen Inventory items 2–7, 9.

## 2. Parent Feature
A.8 — Daily Quiz & Quiz Completion Engine

## 3. Sub-feature
K-03 — Question Type Renderers & Accessibility Interaction Paths

## 4. Objective
Build the 5 first-class question-type renderer composables behind a single dispatcher, sharing one screen skeleton, with mandatory non-visual/non-auditory alternative interaction paths for sequence-ordering, audio-match, and image-match types.

## 5. Business Requirements
FR-2 (all 5 types first-class, reusable across every consuming context), NFR Accessibility (§1.8: "preview for mobile and screen reader" verified path; image-match/audio-match require non-visual/non-auditory alternatives), Edge Case 7 (media-load-failure graceful skip).

## 6. Existing Architecture
Built inside `:core:quiz-engine` (K-01/K-02), using `:core:design-system` tokens for the shared screen skeleton (progress indicator, question-content area, answer-options area, persistent Hint control) and `:core:media-player` for audio-match playback.

## 7. Existing Code to Reuse
- `:core:design-system` component tokens (cards, buttons, grids)
- Hint Overlay component (shared with A.5, per PRD §1.18 Screen Inventory item 7)
- `:core:media-player` playback controls

## 8. Files to Create
- `core/quiz-engine/src/commonMain/kotlin/.../renderers/QuestionTypeRenderer.kt` (dispatcher)
- `core/quiz-engine/src/commonMain/kotlin/.../renderers/MultipleChoiceRenderer.kt`
- `core/quiz-engine/src/commonMain/kotlin/.../renderers/SequenceOrderingRenderer.kt`
- `core/quiz-engine/src/commonMain/kotlin/.../renderers/TrueFalseRenderer.kt`
- `core/quiz-engine/src/commonMain/kotlin/.../renderers/ImageMatchRenderer.kt`
- `core/quiz-engine/src/commonMain/kotlin/.../renderers/AudioMatchRenderer.kt`
- `core/quiz-engine/src/commonMain/kotlin/.../renderers/MediaLoadFailureNotice.kt`
- `core/quiz-engine/src/androidUiTest/kotlin/.../SequenceOrderingTapToPlaceTest.kt`
- `core/quiz-engine/src/androidUiTest/kotlin/.../MediaLoadFailureSkipTest.kt`
- `core/quiz-engine/src/androidUiTest/kotlin/.../RendererAccessibilityTest.kt` (×5, one per renderer, table-driven)

## 9. Files to Modify
- `QuizSessionScreen.kt` (K-01/K-02) — dispatch to `QuestionTypeRenderer` per active question's `type`

## 10. Backend Requirements
Consumes B-03's question payload shape (`prompt`, `options`, `media_url`) and B-04's response submission.

## 11. KMP Requirements
- `QuestionTypeRenderer` dispatcher switches on `question.type`, delegating to one of the 5 renderers
- `SequenceOrderingRenderer` **must** provide a non-drag, tap-to-place alternative interaction mode (not drag-only) — mandatory accessibility path, not optional
- `AudioMatchRenderer` provides a text-transcript fallback option
- `ImageMatchRenderer` provides descriptive alt-text per option
- Shared screen skeleton across all 5 types: progress indicator ("Question 2 of 5" / dots), question-content area, answer-options area (2–4 cards / drag-or-tap tiles / dual buttons / tap-to-match grid), persistent Hint control
- States per type: Default, Answer-selected-not-yet-submitted, Submitting, Explanation-shown, Media-loading, Media-load-failed-skip
- Media-load-failure → graceful skip (treated as unanswered, brief "comes back another time" notice via `MediaLoadFailureNotice`), never a hard block (Edge Case 7)
- Answer-option grids reflow for tablet (more columns) without changing the interaction model

## 12. NextJS Requirements
N/A.

## 13. API Contract
Per B-03/B-04 §13 (question `prompt_payload`/`options`/`media_url` shape).

## 14. Database Requirements
N/A (rendering layer; data sourced via K-02's repository).

## 15. Validation
Client validates a selection/arrangement is present before enabling submit (where applicable per type), never bypassing server-side answer-correctness validation.

## 16. Authentication
N/A directly (inherited session).

## 17. Authorization
N/A.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Image/audio asset fails to load | `MediaLoadFailureNotice` shown, question treated as unanswered, session proceeds (Edge Case 7) |
| Malformed `prompt_payload` for declared type | Defensive fallback rendering (generic text-only presentation) rather than a crash |
| Hint request fails | Generic encouragement fallback message, non-blocking |

## 19. Offline First
Renderers consume the same internal question model whether server-fetched (K-02) or locally-bundled (K-06) — no renderer-level branching on data source.

## 20. Local Data
N/A directly (data-source-agnostic by design).

## 21. Localization / 22. RTL
All question text/audio-transcript/image-alt-text localized (EN/HI/AR/UR); full RTL layout for Arabic-script content across all 5 renderers, including drag/tap-to-place directionality for `SequenceOrderingRenderer`.

## 23. Analytics
`quiz_question_presented` (with `question_type`), `quiz_media_skip_due_to_load_failure`, `hint_requested`.

## 24. Performance
Prevent ANR/UI lag on media-heavy renderers (image/audio); avoid unnecessary recomposition via stable question-state parameters; lazy-load media assets, not eagerly for all questions in the set at once.

## 25. Security
No new sensitive data handling.

## 26. Library Requirements
Jetpack Compose, `:core:media-player`, `:core:design-system` — existing dependencies only.

## 27. Testing
- UI: each of the 5 renderers individually (rendering correctness, selection/arrangement interaction)
- UI: `SequenceOrderingRenderer` tap-to-place path exercised end-to-end **without ever issuing a drag gesture** (signature test, accessibility-mandatory)
- UI: media-load-failure graceful skip — question excluded, session proceeds, no crash
- Accessibility: screen-reader pass per renderer (5 total), verifying alt-text/transcript presence
- UI: tablet reflow test (answer-option grid column count changes, interaction model unchanged)

## 28. Documentation
Renderer dispatcher documented with the accessibility-mandatory note on `SequenceOrderingRenderer`'s tap-to-place path — this is a hard requirement, not a nice-to-have, per PRD §2.2 Accessibility.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement Shared Screen Skeleton**
Task ID: K-03-T01. Files to Create: shared skeleton components within renderer package. Definition of Done: progress indicator, content area, options area, Hint control consistent across all 5 renderers.

**Task 02 — Implement MultipleChoiceRenderer**
Task ID: K-03-T02. Files to Create: `MultipleChoiceRenderer.kt`. Definition of Done: 2–4 option cards, selection state, UI test passing.

**Task 03 — Implement SequenceOrderingRenderer with Tap-to-Place**
Task ID: K-03-T03. Files to Create: `SequenceOrderingRenderer.kt`. Accessibility: non-drag tap-to-place mandatory. Tests: `SequenceOrderingTapToPlaceTest.kt` (signature test). Definition of Done: tap-to-place path completes end-to-end without any drag gesture.

**Task 04 — Implement TrueFalseRenderer**
Task ID: K-03-T04. Files to Create: `TrueFalseRenderer.kt`. Definition of Done: large dual-button UI test passing.

**Task 05 — Implement ImageMatchRenderer with Alt-Text**
Task ID: K-03-T05. Files to Create: `ImageMatchRenderer.kt`. Accessibility: descriptive alt-text per option. Definition of Done: screen-reader test confirms alt-text presence.

**Task 06 — Implement AudioMatchRenderer with Transcript Fallback**
Task ID: K-03-T06. Files to Create: `AudioMatchRenderer.kt`. Dependencies: `:core:media-player`. Accessibility: text-transcript fallback. Definition of Done: transcript-fallback test passing.

**Task 07 — Implement Media-Load-Failure Graceful Skip**
Task ID: K-03-T07. Files to Create: `MediaLoadFailureNotice.kt`. Tests: `MediaLoadFailureSkipTest.kt`. Definition of Done: signature test passes, session proceeds with question excluded.

**Task 08 — Implement Dispatcher**
Task ID: K-03-T08. Files to Create: `QuestionTypeRenderer.kt`. Dependencies: Tasks 02–07. Definition of Done: dispatch correctness verified for all 5 types.

**Task 09 — Add Accessibility Tests**
Task ID: K-03-T09. Files to Create: `RendererAccessibilityTest.kt`. Definition of Done: screen-reader pass verified per renderer.

**Task 10 — Add Localization/RTL**
Task ID: K-03-T10. Definition of Done: all 5 renderers verified in RTL layout with Arabic content.

**Task 11 — Final Code Review**
Task ID: K-03-T11. Definition of Done: §31 checklist fully checked.

## 30. Definition of Done
All 5 question-type renderers implemented behind a single dispatcher; `SequenceOrderingRenderer`'s tap-to-place accessibility path verified end-to-end without any drag gesture; media-load-failure gracefully skips; full RTL/localization support verified.

## 31. Final Verification Checklist
- [ ] `SequenceOrderingRenderer` tap-to-place path works end-to-end with zero drag gestures issued
- [ ] `AudioMatchRenderer` text-transcript fallback present and functional
- [ ] `ImageMatchRenderer` descriptive alt-text present per option
- [ ] Media-load-failure treated as graceful skip, never a hard error
- [ ] Answer-option grids reflow correctly for tablet without changing interaction model
- [ ] Full RTL layout verified for all 5 renderers with Arabic-script content
