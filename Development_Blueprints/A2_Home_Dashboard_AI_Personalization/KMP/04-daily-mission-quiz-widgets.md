# K-04 — Daily Mission & Daily Quiz Widgets

## 1. Feature Context
NoorHeroes Child App (KMP). Renders "Today's Mission" and "Daily Quiz" sections on Home.

## 2. Parent Feature
A.2 — Child Home Dashboard & AI Personalization

## 3. Sub-feature
2.4 Daily Mission & Daily Quiz Widgets (ID: K-04)

## 4. Objective
Build both widgets as independent Composables with correct completed-state rendering (no re-assignment/replay on same-day re-open), consuming B-04 (missions) and the quiz-of-day data surfaced via B-01.

## 5. Business Requirements
Per PRD FR-4, Edge Case 6, Edge Case 11, §2.2:
- Today's Mission: system-assigned, progress ring if partial, completed state with positive reinforcement on re-open (not re-assignment).
- Daily Quiz: "X questions, ~1 min," completed/celebratory state after finishing; not replayable same day by default (unless retry-for-mastery explicitly enabled — default not-replayable).
- Both hide gracefully on their respective service failure.
- Quiz cached for offline play if pre-downloaded.

## 6. Existing Architecture
Plugs into K-01's `SectionState`/`HomeUiState`. Follow `CORE_UI_INSTRUCTIONS.md`.

## 7. Existing Code to Reuse
K-01's `SectionState`, shimmer pattern; existing Quiz Player module (feature-external — this widget only launches it, does not reimplement quiz-taking logic).

## 8. Files to Create
- `feature/home/src/commonMain/kotlin/.../components/TodayMissionCard.kt`
- `feature/home/src/commonMain/kotlin/.../components/DailyQuizWidget.kt`
- `feature/home/src/commonMain/kotlin/.../models/MissionItem.kt`, `.../models/DailyQuizSummary.kt`

## 9. Files to Modify
- `HomeScreen.kt`, `HomeUiState.kt` (K-01)

## 10. Backend Requirements
Consumes `sections.today_mission` (B-04 via B-01) and `sections.daily_quiz` (B-01, quiz-of-day source).

## 11. KMP Requirements
- Mission card: icon, short label, progress ring if partially done; completed state shows positive-reinforcement visual, not a "come back tomorrow" negative framing.
- Quiz widget: question count + estimated time; completed-state checkmark variant; tapping a completed quiz does not relaunch it (default), shows the celebratory state instead.
- Tap routes to relevant feature screen (deep link by `content_type`) with entitlement check, per PRD §2.3.
- Quiz-of-day playable offline if pre-downloaded (reuse existing offline-download availability check from K-02/B.15).

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
`sections.today_mission.items[]` and `sections.daily_quiz{quiz_id, question_count, completed_today}` from B-01's `GET /v1/home` response.

## 14. Database Requirements
Not applicable directly (state read from `HomeUiState`).

## 15. Validation
`completed_today` flag from backend is authoritative for quiz replay-blocking — client must not infer completion from local state alone (avoids drift if the child completes the quiz on a different device).

## 16. Authentication
N/A (inherits session).

## 17. Authorization
N/A at UI layer.

## 18. Error Handling
Both widgets hide gracefully (`SectionState.Error` → hidden) on their respective service failure, per PRD §2.2 table ("Hides if quiz service fails" / assignment-service failure hides card).

## 19. Offline First
Quiz-of-day playable offline if pre-downloaded; mission card shows last-cached mission if stale (>24h marked "may be outdated" per PRD §2.2 table — coordinate exact staleness-marking behavior with K-07's offline cache implementation).

## 20. Local Data
Reads from `HomeUiState` (populated via K-07's cache-or-network `HomeRepository`); quiz offline-playability check reads existing offline-download local store.

## 21. Localization
Widget labels via string resources; mission/quiz titles pre-localized from backend.

## 22. RTL
Progress ring and checkmark iconography mirror appropriately (progress ring direction should remain visually consistent, not literally mirrored in a confusing way — follow existing Design System RTL guidance for circular progress indicators).

## 23. Analytics
`today_mission_viewed/started/completed`, `daily_quiz_widget_viewed`, `daily_quiz_started_from_home`.

## 24. Performance
Lightweight cards, no heavy computation; progress ring animation should not cause jank (use Compose's animation APIs efficiently, avoid recomposition storms).

## 25. Security
N/A beyond standard entitlement checks.

## 26. Library Requirements
Compose Multiplatform, existing navigation library.

## 27. Testing
- Compose UI: mission card renders correctly for incomplete/partial/completed states.
- Compose UI: quiz widget renders correctly for not-started/completed states; tapping completed quiz does not relaunch it.
- Unit: `completed_today` flag correctly drives replay-blocking (server-authoritative, not locally inferred).
- Compose UI: both widgets hide on `Error` state.

## 28. Documentation
KDoc on both Composables explicitly noting that `completed`/`completedToday` are server-authoritative fields the client must never infer locally, and that the Daily Quiz is not-replayable-by-default (a deliberate product decision, not an oversight) — both are easy to regress silently in future edits without this call-out.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Mission & Quiz Models**
- Objective: Typed models for both widgets.
- Why Required: Type-safe mapping from B-01's response.
- Existing Architecture to Follow: K-01 data-model conventions.
- Existing Files to Reuse: `SectionState`.
- Files to Create: `models/MissionItem.kt`, `models/DailyQuizSummary.kt`
- Files to Modify: `HomeUiState.kt`
- Implementation Details: `MissionItem(contentId, type, title, progress, completed)`; `DailyQuizSummary(quizId, questionCount, completedToday)`.
- Business Rules: `completed`/`completedToday` are server-authoritative fields.
- Validation: N/A.
- Error Handling: N/A.
- Security: N/A.
- Performance: `@Immutable`.
- Localization: `title` pre-localized.
- RTL: N/A.
- Analytics: N/A.
- Tests: Mapping unit tests.
- Documentation: KDoc.
- Dependencies: K-01 Task 01.
- Do Not Change: N/A.
- Expected Result: Models defined.
- Definition of Done: Unit tests pass.

**Task 02 — Build `TodayMissionCard` Composable**
- Objective: Mission card UI with progress ring and completed state.
- Why Required: Primary UI deliverable (Edge Case 6).
- Existing Architecture to Follow: `:core:design-system` card tokens.
- Existing Files to Reuse: K-01 shimmer.
- Files to Create: `components/TodayMissionCard.kt`
- Files to Modify: `HomeScreen.kt`
- Implementation Details: Progress ring bound to `progress`; completed state swaps to a positive-reinforcement visual (not a muted/disabled look).
- Business Rules: Never shows a "new mission available" affordance when `completed=true` same day.
- Validation: N/A.
- Error Handling: Hides on `Error`.
- Security: N/A.
- Performance: Efficient ring animation.
- Localization: String resources.
- RTL: Ring rendering verified.
- Analytics: `today_mission_viewed/started/completed`.
- Tests: Compose UI tests for all three states (incomplete/partial/completed).
- Documentation: KDoc.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Working card.
- Definition of Done: Tests pass.

**Task 03 — Build `DailyQuizWidget` Composable with Replay-Blocking**
- Objective: Quiz widget UI with server-authoritative completed state.
- Why Required: Edge Case 11.
- Existing Architecture to Follow: `:core:design-system` card tokens; existing Quiz Player navigation entry point.
- Existing Files to Reuse: K-01 shimmer, existing Quiz Player module.
- Files to Create: `components/DailyQuizWidget.kt`
- Files to Modify: `HomeScreen.kt`
- Implementation Details: Renders question-count/time-estimate when not completed; celebratory checkmark state when `completedToday=true`, tap in this state shows a "come back tomorrow" message rather than relaunching the quiz (unless a future retry-for-mastery flag is explicitly enabled — out of scope here, default OFF).
- Business Rules: `completedToday` is authoritative, not locally cached/inferred.
- Validation: N/A.
- Error Handling: Hides on `Error`.
- Security: N/A.
- Performance: N/A.
- Localization: String resources.
- RTL: N/A.
- Analytics: `daily_quiz_widget_viewed`, `daily_quiz_started_from_home`.
- Tests: Compose UI tests for not-started/completed states; explicit test that tapping a completed quiz does not launch the Quiz Player.
- Documentation: KDoc calling out the default-not-replayable design decision.
- Dependencies: Task 01.
- Do Not Change: Do not default to replayable without an explicit product decision.
- Expected Result: Working widget.
- Definition of Done: Tests pass, including the non-replay assertion.

## 30. Definition of Done
Both widgets correctly reflect server-authoritative completion state, never re-assign/replay same-day, and hide gracefully on error; all tests green.

## 31. Final Verification Checklist
- [ ] Mission completed state shows positive reinforcement, no re-assignment same day
- [ ] Quiz completed state blocks replay by default (server-authoritative flag)
- [ ] Both widgets hide gracefully on respective service error
- [ ] Progress ring and checkmark render correctly across all states
- [ ] All tests pass
