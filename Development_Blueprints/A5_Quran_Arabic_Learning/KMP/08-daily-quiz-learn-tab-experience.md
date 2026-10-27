# K-08 — Daily Quiz Learn-Tab Experience

## 1. Feature Context
Part of Feature A.5 (Quran & Arabic Learning). Renders the Learn-tab instance of the shared Daily Quiz (5 questions, shared engine with A.8), with effort XP always awarded regardless of accuracy.

## 2. Parent Feature
A.5 — Quran & Arabic Learning (shared engine with A.8)

## 3. Sub-feature
K-08 — Daily Quiz Learn-Tab Experience

## 4. Objective
Render the Daily Quiz flow (question set, per-answer explanation, retry set, results/XP reveal) sourced from B-07, reusing A.8's existing quiz UI components rather than building a parallel quiz UI.

## 5. Business Requirements
- FR-15: 5 questions, types multiple choice/sequence/true-false/image-match/audio-match, per-answer explanation, incorrect answers enter a retry set within the same session.
- FR-16: completion awards effort XP regardless of accuracy; accuracy affects mastery, not participation XP.
- Empty State: zero quiz history → friendly first-time framing, not an empty chart.
- Offline: pre-downloaded subset of likely-quiz-content cacheable for offline attempts, syncing results on reconnect with idempotent submission.

## 6. Existing Architecture
This is an **integration layer** over A.8's existing Daily Quiz feature module/components — confirm A.8's actual Compose component library and ViewModel contract before building, per Rule 30 (Do Not Guess). Do not construct a parallel quiz-rendering implementation.

## 7. Existing Code to Reuse
- A.8's quiz-question rendering components (multiple choice/sequence/true-false/image-match/audio-match), retry-set UI, and results/XP-reveal screen — reused via composition/navigation, with `context=learn` passed through to source content from B-07.
- `LearningApi`/`LearningRepository` extended with the `context=learn` quiz-fetch call.

## 8. Files to Create
- `feature-learn/.../quiz/LearnDailyQuizEntryViewModel.kt` (thin wrapper supplying `context=learn` to A.8's quiz engine, not a new quiz UI)
- `feature-learn/src/commonTest/kotlin/.../LearnDailyQuizEntryTest.kt`

## 9. Files to Modify
- `LearnRoute` — add a route that delegates to A.8's existing quiz screen route with `context=learn`, per whichever pattern A.8 already establishes (confirm exact navigation contract before wiring).
- K-01's `SkillTreeScreen`/Home's Daily Quiz widget — entry points into this flow.

## 10. Backend Requirements
Consumes B-07 (`GET /v1/quizzes/daily?context=learn`), which itself delegates to A.8's shared Quiz Engine.

## 11. KMP Requirements
- **Delegation, not duplication**: this blueprint's ViewModel supplies `context=learn` and displays A.8's existing quiz screen/results/retry-set components — no new question-rendering, retry-set, or XP-reveal UI is built here.
- **Offline caching**: pre-download a subset of likely `context=learn` quiz content (via the existing offline-content-download pattern) for offline attempts; sync results on reconnect with idempotent submission (reuses A.8's existing idempotency mechanism if present, or `client_event_id`-style idempotency consistent with B-03's pattern — confirm against A.8's actual sync contract).
- **Empty state**: zero quiz history renders A.8's existing first-time framing (if A.8 already handles this) rather than a Learn-tab-specific reimplementation.
- **Entry points**: from the Skill Tree screen (K-01) and from Home's Daily Quiz widget (cross-feature, confirm Home's actual widget-to-quiz navigation contract before wiring).

## 12. NextJS Requirements
N/A directly.

## 13. API Contract
`GET /v1/quizzes/daily?context=learn` per B-07 §13; underlying question/answer submission contract is A.8's existing quiz-engine contract (confirm before assuming shape).

## 14. Database Requirements
Reuses A.8's existing quiz-content caching/sync schema if present, extended with a `context` discriminator rather than a parallel table — confirm against A.8's actual schema before creating anything new.

## 15. Validation
N/A client-side beyond what A.8's existing quiz components already validate.

## 16. Authentication
Reuses existing child-session auth.

## 17. Authorization
N/A beyond authenticated child session.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Quiz service unavailable | A.8's existing "quiz will be ready again soon" friendly message, reused as-is |
| Offline with no cached content | Clear unavailable state, does not block other Learn-tab content |

## 19. Offline First
Pre-downloaded subset of `context=learn` quiz content cacheable for offline attempts; results sync on reconnect idempotently.

## 20. Local Data
Reuses A.8's existing quiz-content local cache pattern, extended for the `context=learn` pool.

## 21. Localization
Reuses A.8's existing localization handling for quiz content.

## 22. RTL
Reuses A.8's existing RTL support for quiz UI.

## 23. Analytics
`daily_quiz_started`, `quiz_question_answered`, `quiz_explanation_viewed`, `quiz_retry_set_started`, `quiz_completed`, `quiz_effort_xp_awarded` via `AnalyticsTracker` — shared event taxonomy with A.8, with a `context=learn` parameter distinguishing source.

## 24. Performance
No new performance concerns beyond A.8's existing quiz-rendering performance profile.

## 25. Security
No new sensitive surface; standard authenticated-session flow, fully inherited from A.8's existing implementation.

## 26. Library Requirements
Koin, Ktor. No new UI libraries — this is intentionally a thin integration layer.

## 27. Testing
- Unit: `LearnDailyQuizEntryViewModel` correctly supplies `context=learn` to the underlying quiz-fetch call.
- Integration: full quiz flow renders using A.8's existing components with Learn-tab-sourced content.
- Integration: offline cached quiz content usable, results sync on reconnect.
- Contract test: confirms no duplicate quiz-rendering component was introduced (code-review/architecture-conformance check rather than a runtime test).

## 28. Documentation
KDoc explicitly stating this module is an integration layer over A.8, with a pointer to A.8's blueprint/documentation for the actual quiz-rendering implementation.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm A.8's Quiz Screen/ViewModel Contract**
- Task ID: K-08-T01
- Objective: Verify A.8's existing Compose quiz components, navigation route, and offline-sync contract before building anything.
- Why This Is Required: Rule 30 — must not duplicate an existing implementation.
- Dependencies: None (research/verification task).
- Definition of Done: Contract confirmed and documented in this file's §6/§13/§19 (update if it differs from the assumptions above).

**Task 02 — Implement `LearnDailyQuizEntryViewModel`**
- Task ID: K-08-T02
- Implementation Details: Thin wrapper supplying `context=learn`; delegates all rendering to A.8's components.
- Dependencies: K-08-T01, B-07.
- Definition of Done: Unit tests (Task 04) pass.

**Task 03 — Wire Entry Points and Navigation**
- Task ID: K-08-T03
- Files to Modify: `LearnRoute`, K-01's Skill Tree, Home's Daily Quiz widget.
- Dependencies: K-08-T02.
- Definition of Done: Both entry points correctly launch the `context=learn` quiz flow using A.8's existing screens.

**Task 04 — Tests**
- Task ID: K-08-T04
- Dependencies: K-08-T01–T03.
- Definition of Done: All green in CI.

## 30. Definition of Done
Learn-tab Daily Quiz live as a thin `context=learn` integration over A.8's existing quiz engine and UI, zero duplicated quiz-rendering logic, offline caching/sync working, fully tested.

## 31. Final Verification Checklist
- [ ] No duplicate quiz-question-rendering, retry-set, or results UI introduced (confirmed via architecture review against A.8)
- [ ] `context=learn` correctly passed through the full fetch→render→submit chain
- [ ] Effort XP awarded regardless of accuracy (inherited from A.8, verified via integration test)
- [ ] Offline cached quiz content usable, idempotent sync on reconnect
- [ ] Both entry points (Skill Tree, Home widget) correctly wired
- [ ] Full test suite green in CI
