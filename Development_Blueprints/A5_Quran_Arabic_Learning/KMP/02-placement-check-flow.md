# K-02 — Placement Check Flow

## 1. Feature Context
Part of Feature A.5 (Quran & Arabic Learning). First-time-learner flow letting a child skip redundant beginner content by answering a short question set, backed by B-02.

## 2. Parent Feature
A.5 — Quran & Arabic Learning

## 3. Sub-feature
K-02 — Placement Check Flow

## 4. Objective
Present the placement-check question flow, submit responses to B-02, and route the resulting recommended/provisional skill-tree state back into K-01 — always offering an explicit "start from the beginning" alternative.

## 5. Business Requirements
- Acceptance Criteria: first-time skill-tree render offers a placement-check option before defaulting into Surah 1.
- Edge Case 9: Tajweed-prerequisite provisional handling must be visibly reflected (not silently skipped) if the flow surfaces any interim confirmation.

## 6. Existing Architecture
Same `feature-learn` module conventions as K-01: Koin DI, Ktor networking, Compose Multiplatform UI, `core-navigation`'s `Navigator`/`Route` pattern, `AnalyticsTracker`.

## 7. Existing Code to Reuse
- `LearnRoute.PlacementCheck` (defined in K-01-T01).
- `AnalyticsTracker`.
- Shared question-rendering components from `core-designsystem` if an existing quiz/question-answer UI kit exists (reuse rather than rebuild; confirm against Feature A.8's Daily Quiz component library before creating new question-rendering UI).

## 8. Files to Create
- `feature-learn/.../placement/PlacementCheckScreen.kt`
- `feature-learn/.../placement/PlacementCheckViewModel.kt`
- `feature-learn/.../placement/PlacementCheckUiState.kt`
- `feature-learn-domain/.../SubmitPlacementCheckUseCase.kt`
- `core-network/.../api/LearningApi.kt` — extend with `submitPlacementCheck()`
- `feature-learn/src/commonTest/kotlin/.../PlacementCheckViewModelTest.kt`

## 9. Files to Modify
- `core-data/.../repository/LearningRepository.kt`/Impl — add `submitPlacementCheck()`.
- `LearnRoute` — ensure `PlacementCheck` destination wired.

## 10. Backend Requirements
Consumes B-02 (`POST /v1/learning/placement-check`) exclusively.

## 11. KMP Requirements
- **Presentation**: question-by-question flow (reusing shared quiz-question components where they exist), with a clearly visible "start from the beginning" alternative at every step, never forcing completion.
- **Submission**: `PlacementCheckViewModel` collects responses, submits via `SubmitPlacementCheckUseCase`, and on success invalidates/refreshes K-01's cached skill-tree state so the returned `recommended_starting_nodes`/`provisional_states` are reflected immediately on return to the Skill Tree screen.
- **Edge Case 9 UX**: if the response indicates Tajweed-track nodes were marked provisional, no special interstitial is required here (the state itself renders correctly on K-01 as `ready` with a visible "confirm your understanding" affordance or `needs_refresh` scheduling) — this screen's responsibility ends at correct submission and navigation back to the Skill Tree.
- **Failure handling**: submission failure shows a non-blocking retry option; the "start from beginning" alternative remains available regardless of submission outcome.

## 12. NextJS Requirements
N/A.

## 13. API Contract
`POST /v1/learning/placement-check` per B-02 §13.

## 14. Database Requirements
No local persistence beyond the shared `SkillNodeCacheEntity` refresh (K-01) after successful submission — this screen does not need its own cache table since placement-check is a one-time flow.

## 15. Validation
Client-side: ensure all required questions answered before enabling submit; server remains authoritative (B-02 validates payload completeness).

## 16. Authentication
Reuses existing child-session auth via `core-network`.

## 17. Authorization
N/A beyond authenticated child session.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Submission API failure | Non-blocking retry, "start from beginning" always available |
| Duplicate-submission `409` from B-02 | Treat as success — navigate to Skill Tree using the returned prior result |

## 19. Offline First
Placement check requires connectivity to submit; if offline, show a clear "needs internet to place you correctly" message with the "start from beginning" alternative immediately available (consistent with the app's stance on connectivity-gated AI/scoring flows).

## 20. Local Data
N/A beyond triggering K-01's cache refresh on success.

## 21. Localization
Question/answer text localized via existing `core-common/localization` provider.

## 22. RTL
Full RTL support for question flow layout.

## 23. Analytics
`placement_check_started`, `placement_check_completed` via `AnalyticsTracker`.

## 24. Performance
Lightweight flow; no special performance concerns beyond standard Compose recomposition hygiene.

## 25. Security
No sensitive data; standard authenticated-session flow.

## 26. Library Requirements
Koin, Ktor, Compose Multiplatform. Consistent with K-01.

## 27. Testing
- Unit: `PlacementCheckViewModel` submission flow (success, failure-retry, duplicate-409-treated-as-success).
- UI test: "start from beginning" alternative always visible/tappable regardless of flow state.
- Integration: successful submission triggers K-01's skill-tree cache refresh.

## 28. Documentation
KDoc noting this screen never blocks a child from skipping to "start from beginning."

## 29. AI Coding Agent Implementation Steps

**Task 01 — Extend `LearningApi`/`LearningRepository` with Placement Submission**
- Task ID: K-02-T01
- Files to Modify: `LearningApi.kt`, `LearningRepository`/Impl.
- Dependencies: B-02 (backend contract finalized).
- Definition of Done: `submitPlacementCheck()` call succeeds against staging.

**Task 02 — Implement `SubmitPlacementCheckUseCase`**
- Task ID: K-02-T02
- Files to Create: `feature-learn-domain/.../SubmitPlacementCheckUseCase.kt`.
- Dependencies: K-02-T01.
- Definition of Done: Use case unit-tested.

**Task 03 — Implement `PlacementCheckViewModel`**
- Task ID: K-02-T03
- Files to Create: ViewModel + UiState.
- Implementation Details: Response collection, submission, duplicate-409-as-success handling, K-01 cache-refresh trigger, analytics.
- Dependencies: K-02-T02.
- Definition of Done: Unit tests (Task 05) pass.

**Task 04 — Build `PlacementCheckScreen` Composable**
- Task ID: K-02-T04
- Implementation Details: Question flow UI, prominent "start from beginning" alternative at every step.
- Existing Files to Reuse: shared quiz-question components if available (confirm against A.8 before building new).
- Dependencies: K-02-T03.
- Definition of Done: Screen renders correctly in Compose Preview across loading/default/error states.

**Task 05 — Tests**
- Task ID: K-02-T05
- Dependencies: K-02-T01–T04.
- Definition of Done: All green in CI.

## 30. Definition of Done
Placement check flow live, always offers "start from beginning," correctly refreshes K-01's skill-tree state on success, fully tested.

## 31. Final Verification Checklist
- [ ] "Start from beginning" alternative visible and functional at every step
- [ ] Successful submission immediately reflected in K-01's Skill Tree on return
- [ ] Duplicate-submission `409` treated as success, not an error
- [ ] Offline state shows a clear connectivity-needed message with the beginning-alternative still available
- [ ] RTL/localization verified
- [ ] Full test suite green in CI
