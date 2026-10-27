# K-02 — Fact-Linked Quiz Launch Integration

## 1. Feature Context
Part of Feature B.18 (Islamic Facts Module). Wires Fact Detail's "Quick Quiz" card to A.8's existing shared quiz UI — deliberately zero local quiz UI code.

## 2. Parent Feature
B.18 — Islamic Facts Module

## 3. Sub-feature
2.2 Fact-Linked Quiz Launch Integration (ID: K-02)

## 4. Objective
Launch `:core:quiz-engine`'s existing `QuizSessionScreen` composable from Fact Detail with `QuizContext` parameterized for the `islamic_facts` domain, mirroring how A.6's Dua Recall and A.3's Story Post-completion contexts already invoke it.

## 5. Business Requirements
- FR-7: fact's linked quiz routes through the shared Quiz Engine, parameterized (typically 1 question) — no parallel quiz mechanism.
- §7 Android AI Code-Generation Prompt item 2: quiz launch must invoke the EXISTING `QuizSessionScreen`, verified via integration test to reuse the exact same shared composable/repository code path as other domains.
- Edge Case 9 / §6.7 Offline Support: quiz requires connectivity unless bundled offline; clear "needs internet" state otherwise.

## 6. Existing Architecture
Consumes `:core:quiz-engine`'s public API only — `QuizSessionScreen(context: QuizContext)`. This sub-feature adds zero new quiz composables, ViewModels, or repositories.

## 7. Existing Code to Reuse
- `:core:quiz-engine`'s `QuizSessionScreen`, `QuizContext`, `QuizSessionViewModel` (A.8's existing code, imported not duplicated).
- A.6/A.3's existing invocation pattern for parameterizing `QuizContext` for a specific domain — mirror exactly.

## 8. Files to Create
- `feature-facts/src/commonMain/kotlin/.../FactQuizEntryCard.kt` (Composable, part of Fact Detail's UI, launches the shared quiz screen).
- `feature-facts/src/commonTest/kotlin/.../FactQuizLaunchIntegrationTest.kt`.

## 9. Files to Modify
- `FactDetailScreen.kt` (K-01) — wire the Quick Quiz card's tap action to launch `QuizSessionScreen` via navigation.

## 10. Backend Requirements
Consumes B-04 (`GET /v1/quizzes/fact/{fact_id}`) indirectly through `:core:quiz-engine`'s existing repository, which itself calls A.8's contract — this module does not call B-04 directly; it delegates entirely to `:core:quiz-engine`'s existing data layer, configured with the facts-scoped endpoint.

## 11. KMP Requirements
- `QuizContext` constructed with `domain = "islamic_facts"`, `sourceFactId = factId`, `questionCount = 1`.
- Navigation: Fact Detail's Quick Quiz card tap → `:core:navigation` route into `QuizSessionScreen` with the constructed context.
- Quiz completion routes back to Fact Detail (or to the shared Quiz Completion Result screen owned by A.9, per existing A.6/A.3 pattern — confirm exact post-completion routing convention before assuming).
- Response feeds Mastery Engine exactly as any other quiz attempt — no local scoring/state handling.
- Offline: if quiz question data wasn't part of an offline-downloaded package, the Quick Quiz card shows a "needs internet" state rather than attempting to launch and failing silently.

## 12. NextJS Requirements
N/A.

## 13. API Contract
No direct API call from this sub-feature — delegates to `:core:quiz-engine`'s existing repository/API client, itself pointed at B-04's endpoint contract.

## 14. Database Requirements
None new — offline quiz-question bundling (if pre-downloaded) is handled entirely by `:core:quiz-engine`'s existing offline-cache mechanism.

## 15. Validation
`factId` and resolved `linked_quiz_id` (from Fact Detail's already-fetched payload) validated non-null before enabling the Quick Quiz card; absent/null → card not rendered (per K-01's availability-flag convention).

## 16. Authentication
Reuses existing child-session auth via `:core:quiz-engine`'s existing network layer.

## 17. Authorization
N/A beyond authenticated child session.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| No linked quiz question | Quick Quiz card not rendered (K-01's availability flag) |
| Linked question withdrawn mid-session | Card hidden on next Fact Detail load |
| Offline, question not pre-downloaded | "Needs internet" state shown on the card itself, tap disabled |
| Quiz launch failure | Standard `:core:quiz-engine` error handling (unchanged, not reimplemented here) |

## 19. Offline First
Card-level "needs internet" state; actual offline quiz-taking (if pre-downloaded) is entirely `:core:quiz-engine`'s existing offline capability, unmodified.

## 20. Local Data
None new in this sub-feature.

## 21. Localization
Card labels ("Quick Quiz," "Needs internet") localized via existing resource system.

## 22. RTL
Inherits `:core:quiz-engine`'s existing RTL support for the quiz screen itself; the entry card in Fact Detail follows K-01's RTL handling.

## 23. Analytics
`fact_quiz_started`, `fact_quiz_completed` fired by `FactsAnalytics`, correlated with `:core:quiz-engine`'s own internal analytics (both fire; this module's events are domain-specific funnel markers, not a replacement for the shared engine's own event emission).

## 24. Performance
No new heavy computation; navigation-and-delegate pattern only.

## 25. Security
No new attack surface; inherits `:core:quiz-engine`'s existing security posture entirely.

## 26. Library Requirements
None new — consumes `:core:quiz-engine` as an existing dependency.

## 27. Testing
- **Integration test (signature test):** confirm launching the quiz from Fact Detail invokes the exact same `QuizSessionScreen`/`QuizSessionViewModel`/repository code path used by A.6's Dua Recall — no parallel quiz UI exists.
- Unit: `QuizContext` constructed correctly (`domain="islamic_facts"`, correct `sourceFactId`, `questionCount=1`).
- Unit: "needs internet" state shown correctly when offline and question not pre-downloaded.

## 28. Documentation
KDoc noting this is a pure delegation integration, cross-referencing A.6/A.3's equivalent integration points for consistency.

## 29. AI Coding Agent Implementation Steps

**Task 01 — `FactQuizEntryCard` Composable**
Objective: Render the Quick Quiz entry card with correct availability/offline states.
Existing Architecture to Follow: K-01's availability-flag conditional-rendering convention.
Files to Create: `FactQuizEntryCard.kt`.
Dependencies: K-01 complete.
Definition of Done: Card renders/hides correctly per state.

**Task 02 — Wire Quiz Launch**
Objective: Tap action constructs `QuizContext` and navigates into `:core:quiz-engine`'s `QuizSessionScreen`.
Existing Files to Reuse: `:core:quiz-engine`'s public composable/context classes (import only).
Files to Modify: `FactDetailScreen.kt`.
Dependencies: Task 01.
Definition of Done: Passes Task 03's reuse-verification test.

**Task 03 — Reuse-Verification Integration Test**
Objective: Prove identical code path to A.6/A.3's quiz launches.
Files to Create: `FactQuizLaunchIntegrationTest.kt`.
Dependencies: Task 02.
Definition of Done: Test green, code review confirms zero duplicated quiz UI.

**Task 04 — Offline State Handling**
Objective: "Needs internet" card state.
Dependencies: Task 01, K-03 (offline caching) available for reference.
Definition of Done: Verified via test.

**Task 05 — Documentation**
Dependencies: Tasks 01–04.
Definition of Done: KDoc complete.

## 30. Definition of Done
- Quiz launch reuses `:core:quiz-engine`'s exact existing composable/repository path.
- Zero new quiz scoring/state code introduced.
- Offline "needs internet" state correctly distinguishes from a generic error.
- Reuse-verification test passes.

## 31. Final Verification Checklist
- [ ] Reuse-verification test confirms identical code path to A.6/A.3
- [ ] No new quiz UI/state/scoring code introduced anywhere in this sub-feature
- [ ] "Needs internet" state distinct from generic error state
- [ ] Card correctly hidden when no linked quiz or question withdrawn
- [ ] Analytics events firing alongside (not replacing) the shared engine's own events
