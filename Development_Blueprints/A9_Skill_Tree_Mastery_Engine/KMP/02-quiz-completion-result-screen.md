# K-02 — Quiz Completion Result Screen

## 1. Feature Context
Part of Feature A.9 (Skill Tree & Mastery Engine). The shared, reusable `QuizCompletionResultScreen` Composable rendered immediately after any quiz/practice session completes, regardless of originating domain — strengths, one next step, and the `Review Mistakes`/`Try Again`/`Continue` decision point.

## 2. Parent Feature
A.9 — Skill Tree & Mastery Engine

## 3. Sub-feature
K-02 — Quiz Completion Result Screen (Shared Screen)

## 4. Objective
Build `QuizCompletionResultScreen(attemptId: String) -> ResultAction` as a single reusable, domain-blind Composable backed by `MasteryResultViewModel`, with equal-weight action buttons, conditional "Review Mistakes" visibility, and full accessibility/localization/RTL support.

## 5. Business Requirements
- FR-6, FR-7 (via B-06 consumption).
- §2.1 UX Requirements: Strengths section, single Next Step card, three equally-weighted non-hierarchical buttons (`Review Mistakes` only if mistakes exist).
- §2.1 Accessibility: all three buttons equally reachable/labeled via screen reader; no default-focused button implies a "correct" choice.
- Screen Inventory #1-3: Quiz Completion Result Screen, Strengths Summary Component, "One Next Step" Recommendation Card.

## 6. Existing Architecture
Kotlin, Jetpack Compose, MVVM, Clean Architecture. `:core:quiz-engine`'s `QuizSessionScreen` (A.8) is the direct architectural precedent for a shared, reusable, domain-blind Composable. Navigation: launched by `:core:quiz-engine`'s session-completion handoff (A.8 §6.3's `QuizResult` callback) before returning control to the calling feature.

## 7. Existing Code to Reuse
- `:core:design-system` button/card/typography tokens (existing primary/secondary button styling).
- `:core:quiz-engine`'s session-completion handoff pattern (this screen is the next hop after that handoff).
- K-01's `MasteryRepository.getResult()`.
- A.8's "Per-Answer Explanation" component pattern (reused by the Review Mistakes screen this flow leads into — not rebuilt here).

## 8. Files to Create
- `core/mastery-engine/src/commonMain/kotlin/.../presentation/QuizCompletionResultScreen.kt`
- `core/mastery-engine/src/commonMain/kotlin/.../presentation/MasteryResultViewModel.kt`
- `core/mastery-engine/src/commonMain/kotlin/.../presentation/ResultAction.kt` — sealed class (`ReviewMistakes`, `TryAgain`, `Continue`).
- `core/mastery-engine/src/commonMain/kotlin/.../presentation/components/StrengthsSummary.kt`
- `core/mastery-engine/src/commonMain/kotlin/.../presentation/components/NextStepCard.kt`
- `core/mastery-engine/src/commonTest/kotlin/.../MasteryResultViewModelTest.kt`
- `core/mastery-engine/src/androidInstrumentedTest/kotlin/.../QuizCompletionResultScreenUiTest.kt`

## 9. Files to Modify
- `:feature:learn` (A.5) — wire its quiz-session-completion navigation to route into this shared screen and handle the returned `ResultAction` per its own domain logic (e.g., `TryAgain` → fresh A.8 quiz session; `Continue` → back to skill tree).

## 10. Backend Requirements
N/A (consumes B-06 via K-01).

## 11. KMP Requirements
- **Composable signature:** `QuizCompletionResultScreen(attemptId: String, onAction: (ResultAction) -> Unit)` — no domain-specific logic inside; all navigation decisions delegated to the caller via `onAction`.
- **`MasteryResultViewModel`:** fetches `MasteryRepository.getResult(attemptId)` once on entry (`init` block or `LaunchedEffect`), exposes a `StateFlow<ResultUiState>` (Loading/Success/Error).
- **Conditional Review Mistakes button:** rendered ONLY when `has_mistakes == true` — exactly two buttons (`Try Again`, `Continue`) when `false` (Android AI Prompt item 3).
- **Equal visual weight:** `Review Mistakes` and `Try Again` use IDENTICAL secondary-button design-system tokens; `Continue` uses the standard primary-button token (its only differentiation being the platform's normal primary/secondary convention, not an implied "better choice").
- **Mastery celebration layering:** when `transitioned: true` toward `mastered` is detected in the result (via K-01's skill-state data, cross-referenced), layer a small celebratory accent on top of the standard result screen, per §2.1 States — never replacing the standard layout.
- **Loading state:** brief "calculating your progress..." shown if the fetch hasn't resolved within a short budget.

## 12. NextJS Requirements
N/A.

## 13. API Contract
Consumes B-06's `GET /v1/mastery/result/{attempt_id}` response shape exactly, via K-01's `MasteryRepository.getResult()`.

## 14. Database Requirements
N/A (no local persistence for this screen's data — always a fresh server fetch per K-01's design).

## 15. Validation
`attemptId` passed in must be non-blank; ViewModel surfaces an error state if the fetch fails or `attemptId` is invalid.

## 16. Authentication
Reuses the child-session Bearer token attached automatically by `:core:network` (via K-01).

## 17. Authorization
N/A at this layer (server enforces attempt ownership per B-06).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| `getResult()` fetch fails (network/server error) | Error state shown with a retry affordance; never silently blank |
| `has_mistakes = false` | Exactly two buttons rendered (Try Again, Continue) |
| Fetch pending beyond a short budget | "calculating your progress..." loading state (near-instant given B-06's p95 target) |

## 19. Offline First
This screen requires connectivity (server-computed feedback) — per A.9 PRD §6.7, offline quiz completions defer showing this screen entirely; that deferral logic lives in K-04, not here. This screen itself assumes it's only ever launched when connectivity is available.

## 20. Local Data
N/A (always fresh fetch, no caching for this specific data per K-01's design).

## 21. Localization
All strings (`strengths` display wrapper text, `next_step` label/reason if not already localized server-side, button labels "Review Mistakes"/"Try Again"/"Continue") must be localized EN/HI/AR/UR via `:core:design-system`'s string-resource pattern.

## 22. RTL
Full RTL layout support for Arabic/Urdu — button order, icon mirroring (the "gentle upward sparkle" accent), text alignment all mirror correctly; verified via RTL-mode UI tests.

## 23. Analytics
`quiz_result_screen_shown` (`strengths_count`, `next_step_skill_id`), `quiz_result_review_mistakes_selected`, `quiz_result_try_again_selected`, `quiz_result_continue_selected` — fired via K-05's shared `MasteryAnalytics` interface.

## 24. Performance
Minimize recomposition: `ResultUiState` modeled as an immutable, stable data class; avoid re-fetching on recomposition (fetch only in `init`/`LaunchedEffect(attemptId)` keyed correctly). No main-thread blocking during the fetch (suspend function via ViewModel scope).

## 25. Security
No raw score ever rendered (enforced upstream by K-01's DTOs having no such field to begin with — this screen literally cannot display what it doesn't receive).

## 26. Library Requirements
Jetpack Compose, Hilt (ViewModel injection) — no new libraries.

## 27. Testing
- Unit: `MasteryResultViewModel`'s has-mistakes-conditional button-visibility logic.
- Unit: DTO reflection test confirming no raw score field anywhere in `:core:mastery-engine`'s public data classes (covered in K-01, referenced here as a dependency).
- UI test: `has_mistakes = false` → exactly two buttons present, not three (Android AI Prompt item 3).
- UI test: `Review Mistakes` and `Try Again` render with IDENTICAL secondary-button styling tokens (Android AI Prompt item 4).
- UI test: Result screen never displays a percentage/score number anywhere in its semantics tree (accessibility-tree scan).
- Integration test: full quiz-completion → mastery-result → Try-Again-relaunches-fresh-attempt flow, verified across at least two different domains (e.g., a Quran context and a Dua-recall context) using the same shared module code path.

## 28. Documentation
KDoc on `QuizCompletionResultScreen` explicitly stating it must contain zero domain-specific logic — any domain-specific navigation belongs in the calling feature's `onAction` handler, not here.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement MasteryResultViewModel**
- Task ID: K-02-T01
- Objective: State management for the result fetch.
- Why This Is Required: Separates fetch/state logic from the Composable per MVVM.
- Existing Architecture to Follow: Existing ViewModel conventions (Hilt `@HiltViewModel`, `StateFlow` exposure) from `:core:quiz-engine`.
- Existing Files to Reuse: K-01's `MasteryRepository`.
- Files to Create: `MasteryResultViewModel.kt`, `ResultAction.kt`.
- Files to Modify: None.
- Implementation Details: Fetch on init, expose `StateFlow<ResultUiState>` (Loading/Success(QuizResultDto)/Error).
- Business Rules: Single fetch per screen entry, not per recomposition.
- Validation: `attemptId` non-blank.
- Error Handling: Error state with retry.
- Security: N/A. Performance: Fetch off main thread (suspend + viewModelScope).
- Localization: N/A (ViewModel layer). RTL: N/A.
- Analytics: N/A (fired from the Composable/screen layer, Task 03).
- Tests: `MasteryResultViewModelTest.kt`.
- Documentation: KDoc.
- Dependencies: K-01.
- Do Not Change: K-01's repository interface.
- Expected Result: Working ViewModel.
- Definition of Done: Unit tests green including error-state handling.

**Task 02 — Build StrengthsSummary & NextStepCard Components**
- Task ID: K-02-T02
- Objective: Reusable presentational components for the two content sections.
- Why This Is Required: Screen Inventory items #2-3.
- Existing Architecture to Follow: `:core:design-system` component conventions.
- Existing Files to Reuse: Design-system typography/card tokens.
- Files to Create: `components/StrengthsSummary.kt`, `components/NextStepCard.kt`.
- Files to Modify: None.
- Implementation Details: Pure, stateless Composables taking display data as parameters.
- Business Rules: `NextStepCard` always renders exactly one recommendation (never a list UI).
- Validation: N/A. Error Handling: N/A. Security: N/A. Performance: Stable/immutable parameter types to avoid unnecessary recomposition.
- Localization: String resources for all display text. RTL: Layout mirrors correctly.
- Analytics: N/A.
- Tests: Component-level UI tests (snapshot or semantics-based).
- Documentation: KDoc.
- Dependencies: None (pure presentational).
- Do Not Change: N/A.
- Expected Result: Two reusable components.
- Definition of Done: Component tests green in both LTR and RTL.

**Task 03 — Assemble QuizCompletionResultScreen with Equal-Weight Action Buttons**
- Task ID: K-02-T03
- Objective: Full screen assembly with conditional button logic and analytics.
- Why This Is Required: The core deliverable of this sub-feature.
- Existing Architecture to Follow: `:core:quiz-engine`'s `QuizSessionScreen` pattern for domain-blind, callback-driven navigation.
- Existing Files to Reuse: Tasks 01-02's outputs, K-05's `MasteryAnalytics` interface (once available — coordinate sequencing, or stub the interface call if K-05 isn't yet built).
- Files to Create: `QuizCompletionResultScreen.kt`.
- Files to Modify: None.
- Implementation Details: Compose the loading/success/error states from the ViewModel's `StateFlow`; render `Review Mistakes` conditionally; wire equal-weight styling tokens per §11.
- Business Rules: Zero domain-specific logic; all three buttons return via `onAction` callback.
- Validation: N/A. Error Handling: Error state with retry.
- Security: N/A. Performance: Stable state, no unnecessary recomposition.
- Localization: Full EN/HI/AR/UR string coverage. RTL: Full mirrored layout.
- Analytics: Fires `quiz_result_screen_shown` on successful load, and the three selection events on button taps.
- Tests: `QuizCompletionResultScreenUiTest.kt` (button-count test, equal-styling test, no-score-in-semantics-tree test).
- Documentation: KDoc per §28.
- Dependencies: Tasks 01-02, K-01.
- Do Not Change: N/A.
- Expected Result: Fully working, reusable Result screen.
- Definition of Done: All UI tests green (button visibility, equal styling, no-score-in-semantics-tree, RTL).

**Task 04 — Wire A.5's :feature:learn Consumption**
- Task ID: K-02-T04
- Objective: Integrate this shared screen into A.5's existing quiz-completion flow.
- Why This Is Required: Proves the shared-module pattern actually works end-to-end for a real domain consumer.
- Existing Architecture to Follow: A.5's existing navigation graph.
- Existing Files to Reuse: A.5's quiz-session navigation code.
- Files to Create: None.
- Files to Modify: A.5's `:feature:learn` navigation wiring.
- Implementation Details: Route `:core:quiz-engine`'s session-completion callback into `QuizCompletionResultScreen`; handle `ResultAction.TryAgain` (relaunch A.8 quiz session with a new `attempt_id`), `ResultAction.Continue` (return to skill tree), `ResultAction.ReviewMistakes` (navigate to Review Mistakes screen).
- Business Rules: All domain-specific routing decisions live here, in `:feature:learn`, not in the shared module.
- Validation/Error Handling/Security/Performance: N/A beyond standard navigation handling.
- Localization: N/A (delegated). RTL: N/A. Analytics: N/A.
- Tests: Integration test — full quiz-completion → result → Try-Again-relaunches-fresh-attempt flow for a Quran context.
- Documentation: N/A (integration task).
- Dependencies: Task 03.
- Do Not Change: `:core:quiz-engine`'s session-completion callback contract.
- Expected Result: A.5's quiz flow now uses the shared Result screen.
- Definition of Done: Integration test green for at least the Quran domain; ready for a second domain (e.g., Dua-recall) to prove reusability per §27.

## 30. Definition of Done
`QuizCompletionResultScreen` live as a fully reusable, domain-blind Composable with correct conditional button visibility, equal-weight styling, mastery-celebration layering, full accessibility/localization/RTL support, and verified integration with A.5's quiz-completion flow.

## 31. Final Verification Checklist
- [ ] Zero domain-specific logic inside the shared Composable
- [ ] `has_mistakes=false` → exactly two buttons (verified by UI test)
- [ ] Review Mistakes / Try Again use identical secondary-button tokens
- [ ] No percentage/score anywhere in the semantics tree (accessibility-tree scan test)
- [ ] Full EN/HI/AR/UR localization + RTL mirroring verified
- [ ] Mastery-celebration accent layers correctly without replacing standard layout
- [ ] Integration test passes across ≥2 domains using the same shared code path
- [ ] All four analytics events firing correctly via K-05's interface
