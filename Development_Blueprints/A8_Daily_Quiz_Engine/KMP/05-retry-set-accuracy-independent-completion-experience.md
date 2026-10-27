# K-05 — Retry Set & Accuracy-Independent Completion Experience

## 1. Feature Context
NoorHeroes — Feature A.8 Daily Quiz & Quiz Completion Engine. Source PRD §2.1, §7 item 5, FR-5, Edge Cases 3/11, Screen Inventory items 10–12.

## 2. Parent Feature
A.8 — Daily Quiz & Quiz Completion Engine

## 3. Sub-feature
K-05 — Retry Set & Accuracy-Independent Completion Experience

## 4. Objective
Build the Retry Set Entry/Question flow and the Completion/Effort-XP-Reveal screen, with the completion screen's visual treatment provably unaffected by accuracy — the client-side embodiment of the platform's defining hard rule for this feature.

## 5. Business Requirements
FR-5 (unconditional reward, never visually or structurally conditioned on accuracy), §2.1 (Retry Set Framing — supportive subtitle, not a punishment lap; Effort XP Reveal always positive/celebratory regardless of accuracy), Edge Case 3 (bounded retry, supportive framing on conclusion), Edge Case 11 (no retry-set UI when zero misses).

## 6. Existing Architecture
Built inside `:core:quiz-engine` (K-01–K-04), reusing K-03's type-specific renderers for retry questions and K-04's explanation overlay unchanged.

## 7. Existing Code to Reuse
- K-03 renderer composables (reused as-is for retry questions)
- K-04 `ExplanationOverlay`
- `:core:design-system` celebratory-animation components (reward reveal)

## 8. Files to Create
- `core/quiz-engine/src/commonMain/kotlin/.../completion/RetrySetIntroScreen.kt`
- `core/quiz-engine/src/commonMain/kotlin/.../completion/QuizCompletionScreen.kt`
- `core/quiz-engine/src/commonMain/kotlin/.../completion/QuizCompletionUiState.kt`
- `core/quiz-engine/src/androidUiTest/kotlin/.../CompletionScreenAccuracyInvarianceTest.kt`
- `core/quiz-engine/src/androidUiTest/kotlin/.../RetrySetFramingTest.kt`

## 9. Files to Modify
- `QuizSessionViewModel.kt` (K-02) — `RetrySetIntro`/`Completed` state wiring

## 10. Backend Requirements
Consumes B-05's `retry_set_question_ids` and completion response, B-06's `reward` payload.

## 11. KMP Requirements
- Retry Set Entry screen: visually distinguished framing (e.g., "Let's try these again" subtitle), own short progress indicator separate from the main set's
- Retry questions reuse K-03's type-specific renderers unchanged
- Zero-miss case: skip Retry Set Entry entirely, proceed directly to Completion (Edge Case 11 — no empty/skipped-feeling intermediate step)
- Bounded retry-round conclusion: after the single retry round, session concludes with supportive framing regardless of remaining incorrect answers (Edge Case 3)
- **Completion screen composable must NOT branch its visual treatment (colors, animation, layout) based on `accuracyPercent`** — only the numeric text content legitimately differs
- Always positive/celebratory tone and visual treatment at completion, independent of score

## 12. NextJS Requirements
N/A.

## 13. API Contract
Per B-05 §13 (`retry_set_question_ids`, `reward`, `accuracy_percent`).

## 14. Database Requirements
N/A.

## 15. Validation
N/A (presentation layer; business rule enforcement is server-side per B-06).

## 16. Authentication
N/A.

## 17. Authorization
N/A.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Completion API call fails after main set finishes | Local state preserved, retried with idempotent `client_request_id`, child not forced to re-answer |
| Retry-set fetch fails | Falls back to concluding the session directly with supportive framing rather than blocking on an unavailable retry set |

## 19. Offline First
Retry-set and completion flow function fully offline against a locally-bundled question set (K-06); completion syncs on reconnect via idempotent `client_request_id`.

## 20. Local Data
N/A directly (data-source-agnostic, per K-02's repository interface).

## 21. Localization / 22. RTL
Retry/completion copy fully localized (EN/HI/AR/UR), reviewed for supportive, non-punitive tone in every locale; RTL layout for both screens.

## 23. Analytics
`quiz_retry_set_started`, `quiz_retry_question_answered`, `quiz_retry_limit_reached`, `quiz_completed` (accuracy_percent, total_questions), `quiz_effort_xp_awarded`, `quiz_mastery_confidence_updated`.

## 24. Performance
Completion celebratory animation must not block the reward-reveal render; stable/immutable `QuizCompletionUiState`.

## 25. Security
No new sensitive data handling; this sub-feature's core value is a UX-integrity guarantee, not a data-security one.

## 26. Library Requirements
Jetpack Compose, `:core:design-system` — existing dependencies only.

## 27. Testing
- UI: **signature test** — render Completion screen with `accuracyPercent=0` and `accuracyPercent=100`, assert the rendered composable tree (excluding only the numeric text content) uses identical component types, colors, and layout structure in both cases
- UI: Retry Set Entry framing visually distinguished from main-set question screens
- UI: zero-miss flow skips Retry Set Entry entirely, no empty intermediate screen shown
- UI: bounded-retry conclusion after 1 round, supportive copy shown regardless of remaining misses (no third round offered client-side, mirroring B-05's server enforcement)

## 28. Documentation
Completion screen doc explicitly documents the accuracy-independent-visual-treatment rule as the client-side verification point for the platform's defining hard rule (FR-5) — cross-referenced from B-06's docs.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement RetrySetIntroScreen**
Task ID: K-05-T01. Files to Create: `RetrySetIntroScreen.kt`. Implementation Details: distinguished framing, separate progress indicator. Definition of Done: `RetrySetFramingTest.kt` passes.

**Task 02 — Wire Retry Questions to K-03 Renderers**
Task ID: K-05-T02. Dependencies: K-03. Definition of Done: retry questions render via existing type-specific renderers unchanged.

**Task 03 — Implement Zero-Miss Skip Path**
Task ID: K-05-T03. Definition of Done: zero-miss flow verified to skip Retry Set Entry entirely.

**Task 04 — Implement QuizCompletionScreen (Accuracy-Invariant)**
Task ID: K-05-T04. Files to Create: `QuizCompletionScreen.kt`, `QuizCompletionUiState.kt`. Business Rules: FR-5, no accuracy-conditional visual branching. Tests: `CompletionScreenAccuracyInvarianceTest.kt` (signature test). Definition of Done: 0%/100% structural-identity test passes.

**Task 05 — Wire to QuizSessionViewModel**
Task ID: K-05-T05. Files to Modify: `QuizSessionViewModel.kt`. Definition of Done: `RetrySetIntro`/`Completed` states render correctly end-to-end.

**Task 06 — Add Analytics**
Task ID: K-05-T06. Definition of Done: all 6 listed events fire correctly and exactly once per occurrence.

**Task 07 — Add Localization/RTL**
Task ID: K-05-T07. Definition of Done: tone review passed for all 4 locales, RTL layout verified.

**Task 08 — Final Code Review**
Task ID: K-05-T08. Definition of Done: §31 checklist fully checked.

## 30. Definition of Done
Retry Set flow supportively framed and correctly bounded; zero-miss case skips retry entirely; Completion screen provably accuracy-invariant in visual treatment (signature test passing), always celebratory.

## 31. Final Verification Checklist
- [ ] Completion screen structural-identity signature test passing (0% vs. 100% accuracy)
- [ ] Retry Set Entry visually distinguished, own progress indicator
- [ ] Zero-miss flow skips Retry Set Entry with no empty intermediate step
- [ ] Bounded retry (1 round) enforced client-side, consistent with B-05's server enforcement
- [ ] Completion tone/visual treatment always positive regardless of score
- [ ] All 6 completion/retry analytics events verified firing correctly
