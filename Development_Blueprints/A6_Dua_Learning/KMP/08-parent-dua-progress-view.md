# K-08 — Parent Dua Progress View

## 1. Feature Context
NoorHeroes — Feature A.6 Dua Learning. Source PRD user story 9. Sibling features build their own feature-specific parent progress screens within the shared Parent Area shell (e.g. `A5_Quran_Arabic_Learning/KMP/12-parent-progress-report-in-app.md`, `A8_Daily_Quiz_Engine/KMP/07-parent-concept-summary-report.md`) rather than a single generic cross-feature report screen — this file follows that same established pattern, not a shared component.

## 2. Parent Feature
A.6 Dua Learning

## 3. Sub-feature
K-08 — Parent Dua Progress View

## 4. Objective
Add a Duas entry to the existing Parent Area → Child Progress → Learning navigation, rendering B-07's concept-level progress data, following the same structural pattern as A5-KMP/12 and A8-KMP/07.

## 5. Business Requirements
User story 9; empty state per PRD §1.12.

## 6. Existing Architecture
Parent Area shell (existing), navigation via the real `Navigator`/`NavigationAction` (not a bespoke API). Parent-session auth inherited from `core/network`'s existing parent-mode interceptor.

## 7. Existing Code to Reuse
- Parent Area's existing Child Progress → Learning navigation shell
- Empty-state/list-item components from A5-KMP/12 or A8-KMP/07 if they're already generic enough to reuse directly (confirm before building dua-specific equivalents)
- `Navigator.navigateTo()`

## 8. Files to Create
- `feature/dua/src/commonMain/kotlin/.../parent/ParentDuaProgressScreen.kt`
- `feature/dua/src/commonMain/kotlin/.../parent/ParentDuaProgressViewModel.kt`
- `feature/dua/src/commonTest/kotlin/.../ParentDuaProgressViewModelTest.kt`
- `feature/dua/src/androidUiTest/kotlin/.../ParentDuaProgressEmptyStateTest.kt`

## 9. Files to Modify
- Parent Area's navigation registry — add the Duas entry point via `NavigationAction`

## 10. Backend Requirements
Consumes B-07 (`GET /v1/children/{id}/dua-progress`).

## 11. KMP Requirements
- `ParentDuaProgressViewModel` fetches and exposes the concept-level list with `learned_status`, `learned_at`, `habit_reminder_linked`
- Multi-child selector reused from the existing Parent Area pattern
- Empty state per PRD §1.12
- Cached last-known state with staleness indicator on failure, via `SafeDatabaseHelper`

## 12. NextJS Requirements
N/A.

## 13. API Contract
Per B-07 §13.

## 14. Database Requirements
Local cache of last-fetched progress per child, via `getRoomDatabase()`.

## 15. Validation
N/A beyond existing child-selection validity.

## 16. Authentication
Existing parent-session bearer.

## 17. Authorization
Enforced server-side by B-07; client reflects the authenticated parent session only.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| API failure | Cached last-known state with staleness indicator |
| Zero learned duas | Empty state per §1.12 |

## 19. Offline First
Read-only cached rendering; no offline write actions originate from this screen.

## 20. Local Data
Cached progress list per child.

## 21. Localization / 22. RTL
Full localization/RTL for parent-facing copy.

## 23. Analytics
`parent_dua_progress_viewed` via `AnalyticsTracker`.

## 24. Performance
Standard list rendering, consistent with sibling parent progress screens' existing conventions.

## 25. Security
No new sensitive surface; relies entirely on B-07's server-side family-membership enforcement.

## 26. Library Requirements
Existing Parent Area module dependencies only.

## 27. Testing
- Unit: ViewModel fetch/empty-state logic
- UI: empty and populated states
- Integration: API-failure fallback to cached state with staleness indicator

## 28. Documentation
Brief integration note on Parent Area navigation registration, cross-referencing A5-KMP/12's/A8-KMP/07's structural pattern.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm Reusable Components**
Task ID: K-08-T01. Objective: check whether A5-KMP/12's or A8-KMP/07's empty-state/list-item components are generic enough to reuse directly before building dua-specific ones. Definition of Done: documented decision.

**Task 02 — Register Navigation Entry**
Task ID: K-08-T02. Files to Modify: Parent Area navigation registry. Definition of Done: reachable via `Navigator`.

**Task 03 — Implement ViewModel**
Task ID: K-08-T03. Definition of Done: unit tests pass.

**Task 04 — Implement Screen**
Task ID: K-08-T04. Dependencies: Task 01. Definition of Done: renders correctly across states.

**Task 05 — Implement Cached Fallback**
Task ID: K-08-T05. Definition of Done: staleness-indicator test passes.

**Task 06 — Add Analytics & Tests**
Task ID: K-08-T06. Definition of Done: all §27 scenarios covered.

**Task 07 — Add Documentation**
Task ID: K-08-T07. Definition of Done: integration note written.

**Task 08 — Final Code Review**
Task ID: K-08-T08. Definition of Done: §31 checklist fully checked.

## 30. Definition of Done
Parent Dua Progress view functional, reachable, handles empty/error states, follows the same structural pattern as sibling parent-progress screens.

## 31. Final Verification Checklist
- [ ] Reachable via Parent Area → Child Progress → Learning → Duas
- [ ] Empty state matches PRD copy
- [ ] Populated state shows `learned_status`/`learned_at`/habit-linkage
- [ ] API failure falls back to cached state with staleness indicator
- [ ] Reuses sibling components where genuinely generic, per Task 01's decision

## 32. Addendum — What Changed From the Original Draft
Corrected to use the real `Navigator`/`NavigationAction` API and `getRoomDatabase()`/`SafeDatabaseHelper` for local caching, and to explicitly check for reusable components from A5-KMP/12 and A8-KMP/07 (the real sibling parent-progress screens) before assuming this needs to be built entirely from scratch.
