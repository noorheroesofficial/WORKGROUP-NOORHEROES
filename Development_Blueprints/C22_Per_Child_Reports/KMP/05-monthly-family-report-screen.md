# Blueprint: Monthly Family Report Screen

## 1. Feature Context
Platform: NoorHeroes KMP App. Module: `:feature:reports`. Delivers the cross-child, aggregate-only Monthly Family Report screen.

## 2. Parent Feature
C.22 — Per-Child Reports.

## 3. Sub-feature
K-05 — Monthly Family Report Screen.

## 4. Objective
Render the monthly family-level aggregate report (family streaks, content favorites, learning consistency) with a UI structurally incapable of rendering a per-child comparison layout, matching Backend B-05's aggregate-only schema.

## 5. Business Requirements
Source: PRD §1.7 FR-6, FR-8, §1.18 Screen Inventory #11.
- Cross-child aggregate summary: family streaks, content favorites, learning consistency.
- Never compares siblings (FR-8) — this is a UI-layer restatement of the backend's structural guarantee (B-05).
- Reached from Parent Dashboard or Per-Child Report cross-link.

## 6. Existing Architecture
Consumes Backend B-05's `GET /v1/parent/reports/{family_id}/monthly-family` directly. Independent from `PerChildReportScreen`, scoped to `familyId` (derived from `:core:auth`, never per-child).

## 7. Existing Code to Reuse
- `AuthStateProvider` for `familyId` derivation (never passed as a raw external parameter).
- `Navigator`, `BaseViewModel`, `NoorResult<T>`.
- `:core:design-system` aggregate-summary card components.

## 8. Files to Create
- `feature/reports/src/commonMain/kotlin/.../MonthlyFamilyReportRoute.kt`
- `feature/reports/src/commonMain/kotlin/.../MonthlyFamilyReportScreen.kt`
- `feature/reports/src/commonMain/kotlin/.../MonthlyFamilyReportViewModel.kt`
- `feature/reports/src/commonMain/kotlin/.../MonthlyFamilyReportUiState.kt`
- `feature/reports/src/commonTest/kotlin/.../MonthlyFamilyReportNoSiblingComparisonStructuralTest.kt`
- `feature/reports/src/commonTest/kotlin/.../MonthlyFamilyReportViewModelTest.kt`

## 9. Files to Modify
- `ReportRepository.kt` — add `getMonthlyFamilyReport(familyId): NoorResult<MonthlyFamilyReportData>`

## 10. KMP Requirements
- `MonthlyFamilyReportUiState`: `sealed interface { object Loading; data class Content(val data: MonthlyFamilyReportData); object NotYetAvailable; data class Error(val error: AppError) }`.
- `MonthlyFamilyReportData(familyStreakDays: Int, contentFavorites: List<String>, learningConsistencySummary: String, asOf: Instant)` — **no field shaped as a per-child list/map**, mirroring Backend B-05's structural guarantee.
- `MonthlyFamilyReportScreen`: renders the three aggregate fields as summary cards; explicitly no per-child breakdown table, chart, or list anywhere in the composable tree.
- `NotYetAvailable` state (family too new / mid-month) renders a clear "check back after month-end" message, not an error.

## 11. Files to Create — continued
Entry points wired from Parent Dashboard (`:feature:parent-dashboard`) and `PerChildReportScreen` (K-01) per PRD §1.18.

## 12. NextJS Requirements
N/A.

## 13. API Mapping
`ReportRepository.getMonthlyFamilyReport(familyId)` → `GET /v1/parent/reports/{family_id}/monthly-family` (Backend B-05).

## 14. Database Requirements (Local)
Cached via `:core:offline-cache` keyed by `familyId`.

## 15. Validation
`familyId` derived internally from `:core:auth`, never passed as a nav arg from an untrusted source.

## 16. Authentication
Inherits Parent Gate requirement.

## 17. Authorization
Server-enforced (family-membership check, Backend B-05); client reflects `403` as `Error`.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| `report_available: false` from backend | `NotYetAvailable` state, not `Error` |
| Network failure | `Error` with retry |
| Backend fallback to last passing report | Transparent to the client — same `Content` rendering path |

## 19. Offline First
Cached read-only rendering offline.

## 20. Local Data
Cached `MonthlyFamilyReportData` per `familyId`.

## 21. Localization
`learningConsistencySummary` and `contentFavorites` labels locale-resolved server-side.

## 22. RTL
Summary card layout mirrors correctly for Arabic/Urdu.

## 23. Analytics
`monthly_family_report_viewed` fired on successful content load.

## 24. Performance
Lightweight screen (three aggregate fields), no special performance concerns.

## 25. Security
UI structurally cannot render a per-child comparison because the underlying `MonthlyFamilyReportData` model has no such field — verified by a reflection-based structural test, the primary trust control for this screen alongside Backend B-05's own schema test.

## 26. Library Requirements
No new dependencies.

## 27. Testing
1. **Structural test:** reflection scan of `MonthlyFamilyReportData` confirms no field shaped as a per-child list/map/array of child-keyed objects.
2. Unit test: `NotYetAvailable` state renders correctly, distinct from `Error`.
3. Unit test: populated state renders all three aggregate fields.
4. UI test: no per-child breakdown UI element exists anywhere in the screen's composable tree (rendering-level check complementing the data-level structural test).
5. Integration test: full fetch-and-render flow.

## 28. Documentation
KDoc explicitly citing FR-8 and the aggregate-only design constraint.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define MonthlyFamilyReportUiState with Structural No-Sibling-Comparison Guarantee**
- Task ID: K05-T01
- Objective: Data model with no per-child field possible.
- Why This Is Required: FR-8's client-side enforcement point, mirroring Backend B-05.
- Existing Architecture to Follow: Reflection-test pattern established elsewhere in the app (e.g., K-02's no-score test).
- Existing Files to Reuse: none new.
- Files to Create: `MonthlyFamilyReportUiState.kt`, `MonthlyFamilyReportNoSiblingComparisonStructuralTest.kt`.
- Files to Modify: none.
- Implementation Details: Per §10.
- Business Rules: FR-8.
- Validation: N/A.
- Error Handling: `NotYetAvailable`/`Error` distinct.
- Security: This IS the security control.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task's structural test is itself a deliverable.
- Documentation: KDoc citing FR-8.
- Dependencies: Backend B-05 live.
- Do Not Change: N/A.
- Expected Result: State model compiles, structural test passes.
- Definition of Done: Reflection test green and CI-wired.

**Task 02 — Implement MonthlyFamilyReportViewModel and Screen**
- Task ID: K05-T02
- Objective: Fetch and render the aggregate report.
- Why This Is Required: Delivers the sub-feature.
- Existing Architecture to Follow: `BaseViewModel`, `AuthStateProvider` derive-internally pattern.
- Existing Files to Reuse: `:core:design-system` summary-card components.
- Files to Create: `MonthlyFamilyReportViewModel.kt`, `MonthlyFamilyReportScreen.kt`, `MonthlyFamilyReportRoute.kt`.
- Files to Modify: `ReportRepository.kt`, navigation graph, Parent Dashboard entry point.
- Implementation Details: Per §10, §18.
- Business Rules: FR-6, FR-8.
- Validation: N/A.
- Error Handling: Per §18.
- Security: No per-child UI element present.
- Performance: N/A.
- Localization: Full string-resource coverage.
- RTL: Verified mirroring.
- Analytics: `monthly_family_report_viewed`.
- Tests: Covered in Task 03.
- Documentation: KDoc.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Screen renders correctly across all states.
- Definition of Done: Not-yet-available state verified distinct from error.

**Task 03 — Write Test Suite**
- Task ID: K05-T03
- Objective: Cover §27, with the structural test as a CI-blocking gate.
- Why This Is Required: FR-8 verification at the client layer.
- Existing Architecture to Follow: Kotlin test + Compose UI test.
- Existing Files to Reuse: none new.
- Files to Create: `MonthlyFamilyReportViewModelTest.kt`.
- Files to Modify: none.
- Implementation Details: 5 test cases per §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert exact states.
- Security: Structural test is critical.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test KDoc.
- Dependencies: Tasks 01–02.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 green, structural test CI-blocking.

## 30. Definition of Done
`MonthlyFamilyReportScreen` live, aggregate-only rendering verified structurally, not-yet-available state correctly distinguished from error, all tests green.

## 31. Final Verification Checklist
- [ ] Structural test confirms no per-child comparison field in `MonthlyFamilyReportData`
- [ ] No per-child breakdown UI element anywhere in the composable tree
- [ ] `NotYetAvailable` state distinct from `Error`
- [ ] `familyId` derived internally, never passed as an untrusted parameter
- [ ] Localization and RTL mirroring verified
