# K-07 — Parent Concept Summary Report

## 1. Feature Context
NoorHeroes — Feature A.8 Daily Quiz & Quiz Completion Engine. Source PRD §1.18 Screen Inventory item 15, §2.2, FR-6, Edge Case 10. Header cross-reference: "Feeds into: ... C.22 Parent Progress Reports."

## 2. Parent Feature
A.8 — Daily Quiz & Quiz Completion Engine

## 3. Sub-feature
K-07 — Parent Concept Summary Report (Parent Area, In-App)

## 4. Objective
Render the quiz-specific concept-level summary within the Parent Area (Parent Dashboard → Child Progress), consuming B-07's API, showing concepts practiced/mastered rather than a raw score, and linking into the broader concept-detail drill-in shared with A.5's own mastery reporting screen.

## 5. Business Requirements
FR-6 (concept-level, not score-level, headline), Acceptance Criteria (§1.9: report lists concepts like "Practicing: Surah Al-Fatiha recitation"), Edge Case 10 (multi-domain attribution displayed distinctly per skill), §1.12 Empty States (first-time-learner framing).

## 6. Existing Architecture
This screen is one contributing panel within the platform's broader Parent Progress Report surface (C.22, Parent Area — In-App PRD category 19–26) — confirm the exact existing parent-dashboard/progress-report module name and navigation entry point from C.22's own blueprint before wiring; do not invent a new standalone parent-facing module if C.22 already owns the container screen. This sub-feature builds the quiz/concept-specific panel and its data-loading logic, consistent with how A.5 built its own mastery-summary panel for the same container.

## 7. Existing Code to Reuse
- Existing Parent-session PIN/biometric gate state check (A.1/C.19, per A2-K08 precedent — do not re-implement)
- C.22's Parent Progress Report container screen/navigation (confirm interface before wiring)
- A.5's equivalent concept-summary panel component, if a shared panel-layout component already exists there — reuse rather than fork

## 8. Files to Create
- `feature/parent-dashboard/src/commonMain/kotlin/.../quiz/QuizConceptSummaryPanel.kt`
- `feature/parent-dashboard/src/commonMain/kotlin/.../quiz/QuizConceptSummaryViewModel.kt`
- `feature/parent-dashboard/src/commonMain/kotlin/.../quiz/QuizConceptSummaryUiState.kt`
- `feature/parent-dashboard/src/commonTest/kotlin/.../QuizConceptSummaryViewModelTest.kt`
- `feature/parent-dashboard/src/androidUiTest/kotlin/.../QuizConceptSummaryNoScoreHeadlineTest.kt`

## 9. Files to Modify
- C.22's Parent Progress Report container screen (external) — register this panel as the quiz-specific contribution, confirm exact integration point with that feature's blueprint before modifying

## 10. Backend Requirements
Consumes B-07 (`GET /v1/children/{id}/quiz-concept-summary?period=weekly`).

## 11. KMP Requirements
- Renders a concept list (`skill`, `status`, `recent_accuracy_trend`) with **no raw numeric score as the visual headline** — concept status is the primary visual element
- Multi-domain sessions display each skill's contribution as a distinct row, never a merged/ambiguous combined item (Edge Case 10)
- First-time-learner (zero quiz history) state renders distinct first-time framing copy, not a stark "no data" empty state
- Tapping a concept row navigates to Concept Detail Drill-in (shared component with A.5 §1.18 — reuse, do not fork)
- `period` selector (e.g., weekly) if the container screen supports period switching

## 12. NextJS Requirements
N/A.

## 13. API Contract
Per B-07 §13.

## 14. Database Requirements
N/A (read-only remote data; no local caching required beyond standard short-TTL in-memory state, given weekly-cadence parent access pattern).

## 15. Validation
N/A (display-only; data correctness owned by B-07).

## 16. Authentication
Inherits active Parent-session state (no PIN re-entry if already authenticated in an active Parent session, consistent with A2-K08 precedent).

## 17. Authorization
N/A at this layer (server-enforced family/child ownership check in B-07).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| B-07 unavailable | Friendly "concept summary will be ready again soon" message, does not block the rest of the Parent Progress Report |
| Zero quiz history | First-time framing panel, not a blank/error state |
| Skill Mastery status enrichment degraded (per B-07 §18) | Panel still renders skill names with accuracy-trend data, no blank rows |

## 19. Offline First
N/A (Parent Area is an online, low-frequency-access surface; not part of the child's offline quiz-taking flow).

## 20. Local Data
N/A.

## 21. Localization / 22. RTL
Concept/status/trend labels fully localized (EN/HI/AR/UR); RTL layout for the panel, consistent with the rest of the Parent Progress Report container.

## 23. Analytics
`parent_quiz_summary_viewed`.

## 24. Performance
Single API call per panel load; no heavy client-side aggregation (all rollup logic owned server-side by B-07).

## 25. Security
No new sensitive data handling; standard parent-session-scoped access to their own family's child data only.

## 26. Library Requirements
Jetpack Compose, existing `:core:network` client — no new dependencies.

## 27. Testing
- UI: **signature test** — assert the panel's headline visual element is the concept/status list, not a raw numeric score (structural/semantics-tree assertion)
- UI: multi-domain summary displays each skill as a distinct row
- UI: first-time-learner state renders distinct framing, not a blank/error empty state
- Unit: ViewModel correctly maps B-07's response to `QuizConceptSummaryUiState`

## 28. Documentation
Panel doc cross-references B-07's "no raw score as headline" contract and documents where this panel plugs into C.22's broader Parent Progress Report container, flagging the exact integration point as confirmed-not-assumed at implementation time.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm C.22 Container Integration Point**
Task ID: K-07-T01. Implementation Details: read C.22's actual blueprint/module before wiring — do not invent the container screen's interface. Definition of Done: integration point confirmed and documented.

**Task 02 — Implement QuizConceptSummaryViewModel**
Task ID: K-07-T02. Files to Create: `QuizConceptSummaryViewModel.kt`, `QuizConceptSummaryUiState.kt`. Definition of Done: correctly maps B-07 response, unit tests pass.

**Task 03 — Implement QuizConceptSummaryPanel Composable**
Task ID: K-07-T03. Files to Create: `QuizConceptSummaryPanel.kt`. Business Rules: FR-6, no raw-score headline. Tests: `QuizConceptSummaryNoScoreHeadlineTest.kt` (signature test). Definition of Done: signature test passes.

**Task 04 — Implement First-Time-Learner State**
Task ID: K-07-T04. Definition of Done: distinct framing verified, not a blank/error state.

**Task 05 — Wire Concept Detail Drill-in Navigation**
Task ID: K-07-T05. Dependencies: shared component with A.5 §1.18. Definition of Done: tapping a concept row navigates correctly, no forked drill-in component.

**Task 06 — Register Panel in C.22 Container**
Task ID: K-07-T06. Files to Modify: C.22's container screen. Definition of Done: panel appears correctly within the broader Parent Progress Report.

**Task 07 — Add Localization/RTL**
Task ID: K-07-T07. Definition of Done: RTL layout verified, all 4 locales reviewed.

**Task 08 — Add Tests**
Task ID: K-07-T08. Definition of Done: full coverage per §27.

**Task 09 — Final Code Review**
Task ID: K-07-T09. Definition of Done: §31 checklist fully checked.

## 30. Definition of Done
Panel renders concept-level summary with no raw-score headline (signature test passing), multi-domain attribution displayed distinctly, first-time-learner framing correct, integrated into C.22's Parent Progress Report container.

## 31. Final Verification Checklist
- [ ] No raw numeric score rendered as the panel's visual headline (signature test passing)
- [ ] Multi-domain session displays each skill as a distinct row, never merged
- [ ] First-time-learner state distinct from a blank/error empty state
- [ ] Concept Detail Drill-in reuses A.5's shared component, not a forked implementation
- [ ] Integration point with C.22's container confirmed against that feature's actual blueprint, not assumed
- [ ] RTL layout verified
