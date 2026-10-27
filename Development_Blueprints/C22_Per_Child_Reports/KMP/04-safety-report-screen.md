# Blueprint: Safety Report Screen

## 1. Feature Context
Platform: NoorHeroes KMP App. Module: `:feature:reports`. Delivers `SafetyReportScreen`, the on-demand full transparency report screen.

## 2. Parent Feature
C.22 — Per-Child Reports.

## 3. Sub-feature
K-04 — Safety Report Screen.

## 4. Objective
Render the on-demand Safety Report (AI usage summary, blocked requests, content flags, profile-setting changes) with a clean, reassuring state for zero events, reached from the Per-Child Report or Parent Dashboard.

## 5. Business Requirements
Source: PRD §1.6 User Story 8, §1.10 Edge Case #3, §1.18 Screen Inventory #10/#18, §6.2.
- Four content sections: AI usage summary, blocked requests, content flags, profile-setting changes.
- Requested on demand, not auto-loaded on a schedule.
- Zero safety events ever → clean/reassuring "no safety events recorded" state, never an error or empty-looking broken section (Edge Case #3).

## 6. Existing Architecture
Consumes Backend B-04's `GET /v1/parent/reports/{child_id}/safety-report` directly. Independent screen from `PerChildReportScreen` (K-01), reached via its own entry point per PRD §1.18.

## 7. Existing Code to Reuse
- `Navigator`, `BaseViewModel`, `NoorResult<T>`, `DispatcherProvider`.
- `:core:design-system` section/card components.

## 8. Files to Create
- `feature/reports/src/commonMain/kotlin/.../SafetyReportRoute.kt`
- `feature/reports/src/commonMain/kotlin/.../SafetyReportScreen.kt`
- `feature/reports/src/commonMain/kotlin/.../SafetyReportViewModel.kt`
- `feature/reports/src/commonMain/kotlin/.../SafetyReportUiState.kt`
- `feature/reports/src/commonTest/kotlin/.../SafetyReportViewModelTest.kt`

## 9. Files to Modify
- `ReportRepository.kt` — add `getSafetyReport(childId): NoorResult<SafetyReportData>`

## 10. KMP Requirements
- `SafetyReportUiState`: `sealed interface { object Loading; data class Content(val data: SafetyReportData); object CleanState; data class Error(val error: AppError) }`.
- `SafetyReportData(aiUsageSummary, blockedRequests: List<...>, contentFlags: List<...>, profileSettingChanges: List<...>)`.
- `SafetyReportScreen`: four labeled sections; when the backend response indicates all-empty, render `CleanState` — a distinct, reassuring composable, not the same "empty list" treatment used for a partial-data error.
- On-demand trigger: screen fetches on entry (`LaunchedEffect`/ViewModel `init`), no scheduled background refresh.

## 11. Files to Create — continued
Entry points wired from `PerChildReportScreen` (K-01) and Parent Dashboard (`:feature:parent-dashboard`, C.20) per PRD §1.18 screen inventory row #10.

## 12. NextJS Requirements
N/A.

## 13. API Mapping
`ReportRepository.getSafetyReport(childId)` → `GET /v1/parent/reports/{child_id}/safety-report` (Backend B-04).

## 14. Database Requirements (Local)
Cached via `:core:offline-cache` for read-only offline viewing (K-09); on-demand generation itself requires connectivity for a fresh fetch.

## 15. Validation
`childId` required nav arg.

## 16. Authentication
Inherits Parent Gate requirement.

## 17. Authorization
Server-enforced; client reflects `403`/`404` as `Error`.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Zero events across all four sections | `CleanState`, reassuring framing, not `Error` |
| Network failure | `Error` with retry |
| Partial data (e.g., only `blockedRequests` populated) | `Content` renders populated sections normally, empty sections show a neutral "none" sub-label, not a broken layout |

## 19. Offline First
Cached read-only rendering offline; fresh on-demand generation requires connectivity.

## 20. Local Data
Cached `SafetyReportData` per `childId`.

## 21. Localization
All section labels and entry summaries locale-resolved (server-side for `summary` fields per B-04, client-side for section headers/labels).

## 22. RTL
Four-section layout, list rows, and icons mirror correctly for Arabic/Urdu.

## 23. Analytics
`safety_report_requested` fired on screen entry/fetch trigger.

## 24. Performance
No special performance concerns beyond standard list rendering; sections independently composable to avoid unnecessary recomposition across unrelated sections.

## 25. Security
Renders only categorical/summary data sourced from Backend B-04 (itself sourced from B-03's structurally redacted store) — no raw content ever displayed.

## 26. Library Requirements
No new dependencies.

## 27. Testing
1. Unit test: clean state renders correctly for zero events across all sections.
2. Unit test: populated state renders all four sections with correct data.
3. Unit test: partial-population state (some sections empty) renders correctly, not as a broken layout.
4. UI test: clean state visually distinct from an error state (reassuring vs. alarming framing).
5. Integration test: full on-demand fetch-and-render flow.

## 28. Documentation
KDoc explaining the clean-state vs. error-state distinction and citing Edge Case #3.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define SafetyReportUiState and Repository Method**
- Task ID: K04-T01
- Objective: Data model and network fetch, distinguishing `CleanState` from `Error`.
- Why This Is Required: Edge Case #3's core enforcement point.
- Existing Architecture to Follow: `NoorResult<T>` pattern.
- Existing Files to Reuse: `ReportRepository` (extend).
- Files to Create: `SafetyReportUiState.kt`.
- Files to Modify: `ReportRepository.kt`.
- Implementation Details: Per §10.
- Business Rules: Edge Case #3.
- Validation: N/A.
- Error Handling: `CleanState`/`Error` are distinct sealed variants.
- Security: N/A.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 03.
- Documentation: KDoc.
- Dependencies: Backend B-04 live.
- Do Not Change: N/A.
- Expected Result: State model compiles.
- Definition of Done: Matches Backend B-04's contract.

**Task 02 — Implement SafetyReportViewModel and Screen**
- Task ID: K04-T02
- Objective: On-demand fetch, render four sections plus clean state.
- Why This Is Required: Delivers the sub-feature.
- Existing Architecture to Follow: `BaseViewModel`, `:core:design-system` section components.
- Existing Files to Reuse: Design-system card/list components.
- Files to Create: `SafetyReportViewModel.kt`, `SafetyReportScreen.kt`, `SafetyReportRoute.kt`.
- Files to Modify: Navigation graph; `PerChildReportScreen.kt`, Parent Dashboard entry point.
- Implementation Details: Per §10, §18.
- Business Rules: Edge Case #3.
- Validation: N/A.
- Error Handling: Per §18.
- Security: N/A.
- Performance: Independent section composables.
- Localization: Full string-resource coverage.
- RTL: Verified mirroring.
- Analytics: `safety_report_requested`.
- Tests: Covered in Task 03.
- Documentation: KDoc.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Screen renders correctly across all states.
- Definition of Done: Clean state visually distinct from error, verified.

**Task 03 — Write Test Suite**
- Task ID: K04-T03
- Objective: Cover §27.
- Why This Is Required: QA coverage for Edge Case #3.
- Existing Architecture to Follow: Kotlin test + Compose UI test.
- Existing Files to Reuse: none new.
- Files to Create: `SafetyReportViewModelTest.kt`.
- Files to Modify: none.
- Implementation Details: 5 test cases per §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert exact states.
- Security: N/A.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test KDoc.
- Dependencies: Tasks 01–02.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 green.

## 30. Definition of Done
`SafetyReportScreen` live, on-demand fetch functional, all four sections render correctly, clean/reassuring zero-events state distinct from error state, all tests green.

## 31. Final Verification Checklist
- [ ] Clean state verified visually and semantically distinct from error state (Edge Case #3)
- [ ] All four sections render independently
- [ ] Partial-population state does not appear broken
- [ ] Localization and RTL mirroring verified
- [ ] Reachable from both `PerChildReportScreen` and Parent Dashboard entry points
