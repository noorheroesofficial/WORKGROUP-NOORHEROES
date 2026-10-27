# K-12 — Parent Quran & Arabic Progress Report (In-App)

## 1. Feature Context
Part of Feature A.5 (Quran & Arabic Learning). Parent-Area screens showing concept-level Quran/Arabic/Tajweed progress and consistency, backed by B-08.

## 2. Parent Feature
A.5 — Quran & Arabic Learning

## 3. Sub-feature
K-12 — Parent Quran & Arabic Progress Report (In-App)

## 4. Objective
Render the Parent Progress Report and Concept Detail drill-in screens using B-08's concept-level data, with a proper empty state for zero-activity children.

## 5. Business Requirements
- FR-17: parent-facing reports show concepts/skills, not just a raw score.
- Acceptance Criteria: report lists mastered/in-progress concepts and consistency trends, not merely a percentage.
- Empty State: "Once [Child] starts practicing, you'll see their progress here."

## 6. Existing Architecture
`feature-learn` module conventions, but this screen lives within the app's existing Parent Area navigation graph (per PRD screen inventory: "Parent Dashboard → Child Progress → Learning") — confirm the exact existing Parent Area module/route structure before wiring, rather than assuming a `feature-learn`-local placement.

## 7. Existing Code to Reuse
- Existing Parent Area navigation graph and shared parent-session auth handling (used across other parent-facing progress reports in the app, e.g., A.3's Parent Story Insights `09-parent-story-insights-in-app.md` — reuse its established parent-report screen pattern/layout conventions if suitable, rather than inventing a new one).
- `get_current_parent`-equivalent client-side session context (parent-mode auth token attached automatically by `core-network`).

## 8. Files to Create
- `feature-learn/.../parentreport/ParentLearningReportScreen.kt` + ViewModel
- `feature-learn/.../parentreport/ConceptDetailScreen.kt` + ViewModel
- `feature-learn-domain/.../GetLearningReportUseCase.kt`
- `feature-learn/src/commonTest/kotlin/.../ParentLearningReportTest.kt`

## 9. Files to Modify
- `LearnRoute` or the existing Parent Area route module (per Task 01's confirmation) — add report/detail destinations.
- Parent Dashboard → Child Progress navigation — add a "Learning" entry point.

## 10. Backend Requirements
Consumes B-08 (`GET /v1/children/{id}/learning-report`) exclusively.

## 11. KMP Requirements
- **Parent Learning Report screen**: lists mastered/in-progress/needs-refresh concepts with plain-language labels and a consistency trend visualization — never a single raw percentage as the headline (mirroring B-08's schema constraint at the UI layer too, i.e., no numeric score prominently displayed even if a raw number happened to leak into the payload).
- **Concept Detail screen**: drill-in from the report list, showing per-concept detail.
- **Empty state**: "Once [Child] starts practicing, you'll see their progress here" for zero-activity children — reuses the report screen's own empty-state handling rather than a separate screen.
- **Error handling**: report fetch failure shows a graceful retry state, not a broken/blank screen.

## 12. NextJS Requirements
N/A.

## 13. API Contract
`GET /v1/children/{id}/learning-report` per B-08 §13.

## 14. Database Requirements
No local persistence required — this is a parent-session, infrequently-accessed, always-fresh-fetch screen (no offline requirement per PRD).

## 15. Validation
N/A client-side.

## 16. Authentication
Reuses existing parent-session auth via `core-network`.

## 17. Authorization
N/A beyond authenticated parent session with the child already resolved to their family (server-enforced by B-08).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Report fetch failure | Graceful retry state |
| Zero-activity child | Empty-state framing, not a broken/blank view |

## 19. Offline First
N/A (parent-session screen, connectivity assumed, no offline requirement specified in PRD).

## 20. Local Data
N/A.

## 21. Localization
Concept labels/trend copy localized via `core-common/localization`.

## 22. RTL
Full RTL layout.

## 23. Analytics
`parent_progress_report_viewed`, `parent_concept_detail_viewed` via `AnalyticsTracker`.

## 24. Performance
Lightweight, infrequent-access screen — no special performance concerns.

## 25. Security
Parent-session auth only; no child-session token accepted. No recitation audio/raw-confidence data ever surfaced (inherited from B-08's design).

## 26. Library Requirements
Koin, Ktor, Compose Multiplatform.

## 27. Testing
- Unit: report rendering never surfaces a raw percentage as the headline UI element.
- Integration: zero-activity empty state renders correctly.
- Integration: report fetch failure shows graceful retry, not a crash/blank screen.

## 28. Documentation
KDoc noting the "no raw score as headline" UI constraint mirrors B-08's API-level constraint and must not regress even if a numeric field is ever added to the payload for internal use.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm Existing Parent Area Navigation Structure**
- Task ID: K-12-T01
- Objective: Verify the existing Parent Dashboard → Child Progress route structure before wiring new destinations.
- Dependencies: None (verification task, per Rule 30).
- Definition of Done: Structure confirmed and documented in §6/§9.

**Task 02 — Implement `GetLearningReportUseCase`**
- Task ID: K-12-T02
- Dependencies: B-08.
- Definition of Done: Use case unit-tested.

**Task 03 — Build `ParentLearningReportScreen`**
- Task ID: K-12-T03
- Implementation Details: Concept lists, consistency trend, empty state, error/retry state.
- Dependencies: K-12-T02.
- Definition of Done: Screen renders correctly across all states in Compose Preview.

**Task 04 — Build `ConceptDetailScreen`**
- Task ID: K-12-T04
- Dependencies: K-12-T03.
- Definition of Done: Drill-in navigation works correctly.

**Task 05 — Wire Navigation Entry Point**
- Task ID: K-12-T05
- Files to Modify: Parent Dashboard → Child Progress navigation (per Task 01's confirmed structure).
- Dependencies: K-12-T01, K-12-T03.
- Definition of Done: "Learning" entry point correctly navigates to the report screen.

**Task 06 — Tests**
- Task ID: K-12-T06
- Dependencies: K-12-T01–T05.
- Definition of Done: All green in CI.

## 30. Definition of Done
Parent Learning Report and Concept Detail screens live, concept-level (never raw-score-headline) presentation, correct empty/error states, fully tested.

## 31. Final Verification Checklist
- [ ] No raw percentage/score ever rendered as the headline UI element
- [ ] Zero-activity empty state matches PRD copy intent
- [ ] Report fetch failure handled gracefully, no blank/broken screen
- [ ] Correctly wired into existing Parent Area navigation structure
- [ ] RTL/localization verified
- [ ] Full test suite green in CI
