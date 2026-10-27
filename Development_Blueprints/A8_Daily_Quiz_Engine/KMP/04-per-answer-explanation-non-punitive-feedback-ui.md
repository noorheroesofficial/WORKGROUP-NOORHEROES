# K-04 — Per-Answer Explanation & Non-Punitive Feedback UI

## 1. Feature Context
NoorHeroes — Feature A.8 Daily Quiz & Quiz Completion Engine. Source PRD §2.1, §2.2 (Per-Answer Explanation Overlay), §7 item 4, FR-3, Screen Inventory item 8.

## 2. Parent Feature
A.8 — Daily Quiz & Quiz Completion Engine

## 3. Sub-feature
K-04 — Per-Answer Explanation & Non-Punitive Feedback UI

## 4. Objective
Build the Per-Answer Explanation Overlay so it renders structurally identically regardless of answer correctness — teaching the correct concept every time, never treating an incorrect answer as a punitive event — as a bottom-sheet over the still-visible question.

## 5. Business Requirements
FR-3 (immediate, never-skippable explanation, always presented), §2.1 (non-punitive incorrect-answer treatment — supportive iconography, not a harsh red X as the dominant element), §2.2 (explanation content identical regardless of correctness, never hidden or abbreviated for incorrect answers).

## 6. Existing Architecture
Built inside `:core:quiz-engine` (K-01/K-02/K-03), using `:core:design-system` bottom-sheet component conventions and the Islamic Facts source-citation pattern already established elsewhere in the app.

## 7. Existing Code to Reuse
- `:core:design-system` bottom-sheet component
- Existing source-citation tag component (Islamic Facts pattern)
- Hint Overlay component (progressive/partial hints, shared with A.5)

## 8. Files to Create
- `core/quiz-engine/src/commonMain/kotlin/.../explanation/ExplanationOverlay.kt`
- `core/quiz-engine/src/commonMain/kotlin/.../explanation/ExplanationOverlayState.kt`
- `core/quiz-engine/src/androidUiTest/kotlin/.../ExplanationStructuralParityTest.kt`

## 9. Files to Modify
- `QuizSessionViewModel.kt` (K-02) — `ExplanationShown` state carries `correct`/`explanation` payload from B-04's response

## 10. Backend Requirements
Consumes B-04's pre-fetched `{ correct, explanation: { text, source_citation } }` — no separate round-trip after submission.

## 11. KMP Requirements
- Bottom-sheet-style overlay, question content remains visible above it (not a full-screen transition)
- Renders **identically in structure** whether `correct=true` or `false` — only the small leading icon and a brief lead-in phrase differ; explanation text/source-citation rendering is the byte-for-byte same code path for both cases
- Correct-answer restatement always shown, regardless of the child's answer
- Supportive iconography for incorrect answers (soft upward-sparkle style, never a dominant harsh red X)
- Pre-fetched — no additional loading state between submission and explanation display (payload already present in `ExplanationShown` state)
- "Next" control advances to next question / retry set / completion per K-02's state machine

## 12. NextJS Requirements
N/A.

## 13. API Contract
Per B-04 §13 (`explanation.text`, `explanation.source_citation`).

## 14. Database Requirements
N/A.

## 15. Validation
N/A (display-only component; correctness already computed server-side by B-04).

## 16. Authentication
N/A.

## 17. Authorization
N/A.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| `explanation` payload missing/malformed | Fallback generic "Let's review this together" message, never a blank overlay |
| Source citation absent for a question that doesn't have one | Citation chip simply omitted, not rendered as empty |

## 19. Offline First
Explanation payload sourced identically whether the question came from server (K-02) or bundled offline set (K-06) — no branching in this component.

## 20. Local Data
N/A directly.

## 21. Localization / 22. RTL
Explanation text/citation fully localized (EN/HI/AR/UR); RTL layout for the bottom sheet, including RTL-correct icon/text ordering.

## 23. Analytics
`quiz_explanation_viewed` fires on overlay display (not skippable — always fires per FR-3).

## 24. Performance
No additional network round-trip (payload pre-fetched); overlay animation should not block main-thread question-content rendering underneath it.

## 25. Security
No new sensitive data handling.

## 26. Library Requirements
Jetpack Compose, `:core:design-system` — existing dependencies only.

## 27. Testing
- UI: **signature test** — assert the Explanation overlay's semantics tree, with the correct-vs-incorrect icon node excluded from comparison, is otherwise structurally identical between a correct and incorrect answer rendering of the same question
- UI: source-citation chip renders when present, omitted (not blank) when absent
- UI: overlay is genuinely non-blocking of the underlying question content (bottom-sheet, not full-screen)
- Localization: RTL layout verified for the overlay in Arabic

## 28. Documentation
Component doc explicitly states the structural-identity requirement as a hard rule (not an implementation detail), since it's the direct client-side embodiment of the platform's non-punitive-feedback commitment (PRD §12.7 Child Safety Requirements).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define ExplanationOverlayState**
Task ID: K-04-T01. Files to Create: `ExplanationOverlayState.kt`. Definition of Done: state carries `correct`, `text`, `sourceCitation` with no correctness-conditional fields beyond the icon/lead-in.

**Task 02 — Implement ExplanationOverlay Composable**
Task ID: K-04-T02. Files to Create: `ExplanationOverlay.kt`. Implementation Details: single code path for text/citation rendering; only icon + lead-in phrase branch on `correct`. Definition of Done: manual visual QA confirms bottom-sheet, question visible above.

**Task 03 — Wire to QuizSessionViewModel's ExplanationShown State**
Task ID: K-04-T03. Files to Modify: `QuizSessionViewModel.kt`. Definition of Done: overlay displays immediately on state transition, no loading flicker.

**Task 04 — Add Structural Parity Test (Signature Test)**
Task ID: K-04-T04. Files to Create: `ExplanationStructuralParityTest.kt`. Definition of Done: semantics-tree comparison test passes with icon node excluded.

**Task 05 — Add Localization/RTL**
Task ID: K-04-T05. Definition of Done: RTL layout verified in Arabic.

**Task 06 — Add Analytics**
Task ID: K-04-T06. Definition of Done: `quiz_explanation_viewed` fires on every overlay display, verified by test.

**Task 07 — Final Code Review**
Task ID: K-04-T07. Definition of Done: §31 checklist fully checked.

## 30. Definition of Done
Explanation overlay renders structurally identically regardless of correctness (signature test passing), always shown pre-fetched with no extra loading state, fully localized/RTL.

## 31. Final Verification Checklist
- [ ] Structural-parity signature test passing (correct vs. incorrect rendering, icon node excluded)
- [ ] Explanation is never skippable and always shown after every answer
- [ ] No additional loading state between submission and explanation display
- [ ] Incorrect-answer treatment uses supportive iconography, never a dominant harsh red X
- [ ] RTL layout verified in Arabic
