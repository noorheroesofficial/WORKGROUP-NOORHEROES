# Blueprint: Skill Mastery Grid & Skill Detail Drill-Down

## 1. Feature Context
Platform: NoorHeroes KMP App. Module: `:feature:reports`. Delivers the Skill Mastery Grid component within `PerChildReportScreen` (K-01) and the `SkillDetailScreen` it navigates to.

## 2. Parent Feature
C.22 — Per-Child Reports.

## 3. Sub-feature
K-02 — Skill Mastery Grid & Skill Detail Drill-Down.

## 4. Objective
Render the Skill Mastery Grid reusing A.9's six-state visual tokens recontextualized for a parent audience, and implement `SkillDetailScreen` with a DTO structurally guaranteed to carry no numeric score/confidence field.

## 5. Business Requirements
Source: PRD §1.7 FR-12, §1.9 Acceptance Criteria, §1.10 Edge Case #5, §2.1, §6.2, §7 item 2.
- Grid reuses A.9's six-state visual language (Locked/Ready/Learning/Practicing/Mastered/Needs Refresh), same color/iconography system as the child-facing Skill Tree, labeled with brief parent-oriented descriptions.
- Drill-down shows parent-friendly state language, never a raw numeric mastery score (FR-12).
- Unengaged skill/domain shows a clear "not started" state, not an empty/confusing detail view (Edge Case #5).

## 6. Existing Architecture
Reuses A.9's `SkillStateVisualMapper`/`SkillTreeStateRenderer` (`:core:mastery-engine`) as-is — this blueprint does not define a second visual language for the same six states. `PerChildReportViewModel` (K-01) supplies `skillMasterySummary` as one of its four state slices; this sub-feature renders that slice and owns navigation into the drill-down.

## 7. Existing Code to Reuse
- `SkillStateVisualMapper.map(state: SkillState): SkillStateVisualTokens` and the `SkillTreeStateRenderer` Composable — both in `:core:mastery-engine` (A.9 K-03), the platform's single centralized state-to-visual-token mapping for all six canonical states. This grid must call into these directly, not redefine a second mapping inside `:feature:reports` (mirrors A.9 K-03's own explicit instruction not to duplicate this mapping per-feature-module).
- `PerChildReportUiState.skillMasterySummary` slice (K-01).
- `Navigator` (`core-navigation`) for drill-down navigation.
- `NoorResult<T>`, `DispatcherProvider`, `BaseViewModel`.

## 8. Files to Create
- `feature/reports/src/commonMain/kotlin/.../SkillMasteryGrid.kt` (Composable)
- `feature/reports/src/commonMain/kotlin/.../SkillDetailRoute.kt`
- `feature/reports/src/commonMain/kotlin/.../SkillDetailScreen.kt`
- `feature/reports/src/commonMain/kotlin/.../SkillDetailViewModel.kt`
- `feature/reports/src/commonMain/kotlin/.../SkillDetailUiState.kt`
- `feature/reports/src/commonTest/kotlin/.../SkillDetailDtoNoRawScoreStructuralTest.kt`
- `feature/reports/src/commonTest/kotlin/.../SkillDetailViewModelTest.kt`

## 9. Files to Modify
- `ReportRepository.kt` (K-01) — add `getSkillDetail(childId, skillId): NoorResult<SkillDetailData>`
- Navigation graph — register `SkillDetailRoute`

## 10. KMP Requirements
- `SkillMasteryGrid` composable: renders a grid of skill tiles, each delegating to `SkillTreeStateRenderer` (`:core:mastery-engine`, A.9 K-03) for its `state` visual treatment, with a short parent-oriented label (e.g., "Practicing," "Mastered") composed alongside it; tapping a tile navigates to `SkillDetailRoute(childId, skillId)`.
- `SkillDetailUiState`: `sealed interface { object Loading; data class Content(val stateLabel: String, val lastPracticedAt: Instant?); object NotStarted; data class Error(val error: AppError) }` — **no field of numeric type anywhere in this hierarchy**.
- `SkillDetailViewModel(reportRepository, dispatchers) : BaseViewModel()` — fetches on init via `SkillDetailRoute.skillId`/`childId` nav args.
- `NotStarted` state renders a clear, non-alarming "not started" screen (Edge Case #5), distinct from `Error`.

## 11. Files to Create — continued
`SkillDetailScreen`: header with skill name/icon, state badge rendered via `SkillTreeStateRenderer` for the current state, `last_practiced_at` (formatted per locale) or "Not started yet" copy, back navigation to `PerChildReportScreen`.

## 12. NextJS Requirements
N/A.

## 13. API Mapping
`ReportRepository.getSkillDetail(childId, skillId)` → `GET /v1/parent/reports/{child_id}/skills/{skill_id}` (Backend B-02).

## 14. Database Requirements (Local)
Drill-down responses cached via `:core:offline-cache` keyed by `(childId, skillId)`, short TTL (this is point-in-time snapshot data, not live-updating).

## 15. Validation
`skillId`/`childId` required nav args; unknown `skillId` surfaces `Error` (mapped from the backend's `404`).

## 16. Authentication
Inherits `PerChildReportRoute`'s Parent Gate requirement (drill-down is only reachable from within the gated report screen).

## 17. Authorization
Server-enforced (Backend B-02); client reflects `403`/`404` as `Error`.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Unengaged skill | `NotStarted` state, not `Error` (Edge Case #5) |
| Unknown `skillId` | `Error` with a "skill not found" message |
| Network failure | `Error` with retry |

## 19. Offline First
Cached drill-down data rendered read-only offline; no offline mutation path (this is a read-only screen).

## 20. Local Data
Short-TTL cache per `(childId, skillId)`.

## 21. Localization
`stateLabel` is already locale-resolved server-side (Backend B-02); "Not started yet"/date formatting done client-side per locale (including Hijri-aware date display if the platform's date formatting convention requires it — confirm against `CORE_COMMON_INSTRUCTIONS.md`'s `LocalDateProvider`).

## 22. RTL
Grid layout and detail screen mirror correctly for Arabic/Urdu; skill tile icon/label order respects RTL reading direction.

## 23. Analytics
`skill_mastery_grid_viewed` fired when the grid renders with content; `skill_detail_drilldown_viewed` fired on `SkillDetailScreen` load.

## 24. Performance
Grid uses `LazyVerticalGrid` (or platform-equivalent) with stable keys per skill to avoid unnecessary recomposition on unrelated state changes elsewhere in `PerChildReportUiState`.

## 25. Security
No numeric score/confidence field declared anywhere in `SkillDetailUiState`/DTO — enforced via a reflection-based structural test mirroring A.9's existing child-facing pattern, applied here to this module's DTOs.

## 26. Library Requirements
No new dependencies.

## 27. Testing
1. **Structural test:** reflection scan of `SkillDetailUiState`/`SkillDetailData` confirms no field of numeric/score/confidence type exists.
2. UI test: all six mastery states render the correct A.9 token in the grid.
3. UI test: unengaged skill renders `NotStarted`, not an empty/broken view.
4. Unit test: navigation from grid tile to `SkillDetailRoute` passes correct `skillId`/`childId`.
5. Integration test: full grid-to-detail-to-back flow.

## 28. Documentation
KDoc on `SkillDetailUiState` explicitly noting the no-numeric-field guarantee and citing FR-12.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define SkillDetailUiState with Structural No-Score Guarantee**
- Task ID: K02-T01
- Objective: Data model with no numeric field possible.
- Why This Is Required: FR-12's client-side enforcement point, mirroring Backend B-02's schema guarantee.
- Existing Architecture to Follow: A.9's existing reflection-test pattern.
- Existing Files to Reuse: none new.
- Files to Create: `SkillDetailUiState.kt`, `SkillDetailDtoNoRawScoreStructuralTest.kt`.
- Files to Modify: none.
- Implementation Details: Per §10.
- Business Rules: FR-12.
- Validation: N/A.
- Error Handling: `NotStarted`/`Error` variants distinct.
- Security: This IS the security control.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task's structural test is itself a deliverable.
- Documentation: KDoc citing FR-12.
- Dependencies: none.
- Do Not Change: A.9's child-facing mastery DTOs.
- Expected Result: State model compiles, structural test passes.
- Definition of Done: Reflection test green and CI-wired.

**Task 02 — Implement SkillMasteryGrid Composable Reusing A.9 Tokens**
- Task ID: K02-T02
- Objective: Render the grid using A.9's existing six-state visual tokens.
- Why This Is Required: Visual consistency mandate (PRD §2.1) — must not invent a second visual language.
- Existing Architecture to Follow: `SkillTreeStateRenderer`/`SkillStateVisualMapper` (`:core:mastery-engine`, A.9 K-03).
- Existing Files to Reuse: `:core:mastery-engine`'s `SkillTreeStateRenderer.kt`/`SkillStateVisualMapper.kt`.
- Files to Create: `SkillMasteryGrid.kt`.
- Files to Modify: `PerChildReportScreen.kt` (K-01) to host this component.
- Implementation Details: Per §10.
- Business Rules: PRD §2.1.
- Validation: N/A.
- Error Handling: N/A (grid itself has no error state beyond K-01's slice-level error).
- Security: N/A.
- Performance: `LazyVerticalGrid` with stable keys.
- Localization: Parent-oriented short labels from string resources.
- RTL: Verified mirroring.
- Analytics: `skill_mastery_grid_viewed`.
- Tests: Covered in Task 05.
- Documentation: KDoc.
- Dependencies: Task 01, K-01.
- Do Not Change: A.9's visual token definitions.
- Expected Result: Grid renders all six states correctly.
- Definition of Done: Visual parity with A.9's tokens confirmed.

**Task 03 — Implement SkillDetailViewModel and Repository Method**
- Task ID: K02-T03
- Objective: Fetch and expose skill detail state including the not-started case.
- Why This Is Required: Core presentation logic for the drill-down.
- Existing Architecture to Follow: `BaseViewModel`, `NoorResult<T>`.
- Existing Files to Reuse: `ReportRepository` (K-01, extend).
- Files to Create: `SkillDetailViewModel.kt`.
- Files to Modify: `ReportRepository.kt`.
- Implementation Details: Per §10, §18.
- Business Rules: FR-12, Edge Case #5.
- Validation: N/A.
- Error Handling: Per §18.
- Security: N/A.
- Performance: N/A.
- Localization: N/A at this layer.
- RTL: N/A.
- Analytics: `skill_detail_drilldown_viewed`.
- Tests: Covered in Task 05.
- Documentation: KDoc.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: ViewModel correctly emits all states.
- Definition of Done: Not-started case verified distinct from error.

**Task 04 — Implement SkillDetailScreen Composable**
- Task ID: K02-T04
- Objective: User-facing drill-down screen.
- Why This Is Required: Delivers the sub-feature.
- Existing Architecture to Follow: `:core:design-system`.
- Existing Files to Reuse: A.9 state badge component.
- Files to Create: `SkillDetailScreen.kt`, `SkillDetailRoute.kt`.
- Files to Modify: Navigation graph.
- Implementation Details: Per §11.
- Business Rules: FR-12.
- Validation: N/A.
- Error Handling: Per §18 UI mapping.
- Security: N/A.
- Performance: N/A.
- Localization: Full string-resource coverage.
- RTL: Verified mirroring.
- Analytics: N/A (ViewModel-level).
- Tests: Covered in Task 05.
- Documentation: KDoc.
- Dependencies: Task 03.
- Do Not Change: N/A.
- Expected Result: Screen renders correctly.
- Definition of Done: Matches §2.2 PRD requirements.

**Task 05 — Write Test Suite**
- Task ID: K02-T05
- Objective: Cover §27.
- Why This Is Required: QA coverage, structural test is highest priority.
- Existing Architecture to Follow: Kotlin test + Compose UI test.
- Existing Files to Reuse: A.9's reflection-test utility if present.
- Files to Create: `SkillDetailViewModelTest.kt` (structural test created in Task 01).
- Files to Modify: none.
- Implementation Details: 5 test cases per §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert exact transitions.
- Security: Structural test is critical.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test KDoc.
- Dependencies: Tasks 01–04.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 green.

## 30. Definition of Done
Skill Mastery Grid renders A.9's six states with parent-oriented labels, drill-down `SkillDetailScreen` shows parent-friendly state language with zero numeric fields (structurally verified), not-started state correctly distinguished from errors, all tests green.

## 31. Final Verification Checklist
- [ ] Reflection-based test confirms no numeric score/confidence field in `SkillDetailUiState`/DTO
- [ ] All six A.9 visual tokens reused, not reinvented
- [ ] Not-started state distinct from error state (Edge Case #5)
- [ ] Navigation correctly passes `childId`/`skillId`
- [ ] Localization and RTL mirroring verified
