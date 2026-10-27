# Blueprint: AI Interaction History Screen

## 1. Feature Context
Platform: NoorHeroes KMP App. Module: `:feature:reports`, deep-linking into `:feature:parental-controls` (C.23). Delivers `AiInteractionHistoryScreen`.

## 2. Parent Feature
C.22 — Per-Child Reports.

## 3. Sub-feature
K-03 — AI Interaction History Screen.

## 4. Objective
Render a calm, transparent, deliberately non-chat-styled list of AI safety-event flags, with a structural guarantee that no chat-bubble/message-thread layout pattern ever exists in this screen's composable tree, and route concerning entries directly to AI Controls (C.23).

## 5. Business Requirements
Source: PRD §1.7 FR-5, FR-13, §1.9 Acceptance Criteria, §2.1, §2.2, §6.2, §6.3, §7 item 3.
- Chronological list of flag/event entries (date, category, brief description, resolution status).
- A clear "Adjust AI Controls" action for any concerning entry, deep-linking into C.23 with `childId` pre-selected.
- Never styled to resemble a chat-transcript UI — deliberately avoiding any visual implication that raw conversational content exists to scroll through.
- Clean "No AI interactions recorded" empty state, neutral not alarming.

## 6. Existing Architecture
Consumes Backend B-03's `GET /v1/children/{id}/ai-history` directly (not routed through K-01's aggregation call, since this is a full-screen deep-dive beyond the summary shown on `PerChildReportScreen`). Deep-links into `:feature:parental-controls` (C.23), an existing module per PRD §6.3.

## 7. Existing Code to Reuse
- `Navigator` (`core-navigation`) for the deep link into `:feature:parental-controls`.
- `NoorResult<T>`, `BaseViewModel`, `DispatcherProvider`.
- `:core:design-system` list-row components (reused, not a new chat-UI component).

## 8. Files to Create
- `feature/reports/src/commonMain/kotlin/.../AiInteractionHistoryRoute.kt`
- `feature/reports/src/commonMain/kotlin/.../AiInteractionHistoryScreen.kt`
- `feature/reports/src/commonMain/kotlin/.../AiInteractionHistoryViewModel.kt`
- `feature/reports/src/commonMain/kotlin/.../AiInteractionHistoryUiState.kt`
- `feature/reports/src/commonTest/kotlin/.../AiInteractionHistoryViewModelTest.kt`
- `feature/reports/src/commonTest/kotlin/.../AiInteractionHistoryNoChatUiStructuralTest.kt`

## 9. Files to Modify
- `ReportRepository.kt` — add `getAiHistory(childId, from, to): NoorResult<List<AiInteractionEntry>>`

## 10. KMP Requirements
- `AiInteractionHistoryUiState`: `sealed interface { object Loading; data class Content(val entries: List<AiInteractionEntry>); object Empty; data class Error(val error: AppError) }`.
- `AiInteractionEntry(date: Instant, category: String, summary: String, concerning: Boolean)`.
- `AiInteractionHistoryScreen`: renders `entries` as a **flat vertical list of rounded card rows only** — icon + date + category label + one-line summary — explicitly **no** two-column, alternating-alignment, or bubble-shaped row composable anywhere in this screen's tree.
- Concerning entries (`concerning == true`) render an "Adjust AI Controls" text link beneath the row, tapping which calls `Navigator.navigate(ParentalControlsDeepLink(childId))` (C.23).
- Empty state: neutral "No AI interactions recorded" framing, not alarming.

## 11. Files to Create — continued
`AiInteractionHistoryViewModel(reportRepository, dispatchers) : BaseViewModel()` — fetches on init via route's `childId`/date-range args (may inherit the currently selected range from `PerChildReportScreen` via nav args, or default to the platform's standard window if reached via other entry points).

## 12. NextJS Requirements
N/A.

## 13. API Mapping
`ReportRepository.getAiHistory(childId, from, to)` → `GET /v1/children/{id}/ai-history?from=&to=` (Backend B-03).

## 14. Database Requirements (Local)
Cached via `:core:offline-cache`, read-only offline per K-09.

## 15. Validation
`childId` required nav arg.

## 16. Authentication
Inherits Parent Gate requirement (reachable only from within `PerChildReportScreen`'s AI Interaction Log link, per K-01).

## 17. Authorization
Server-enforced; client reflects `403`/`404` as `Error`.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Zero entries | `Empty` state, neutral framing |
| Network failure | `Error` with retry |
| Deep-link into C.23 fails (e.g., module not installed/reachable) | Graceful error toast, does not crash the screen |

## 19. Offline First
Read-only cached rendering offline; concerning-flag deep link to C.23 remains available offline (C.23 itself handles its own connectivity requirements for the control-adjustment action).

## 20. Local Data
Cached entry list per `(childId, from, to)`.

## 21. Localization
`category`/`summary` are already locale-resolved server-side (Backend B-03); date formatting client-side per locale.

## 22. RTL
List-row layout, icon placement, and the "Adjust AI Controls" link all mirror correctly for Arabic/Urdu.

## 23. Analytics
`ai_interaction_history_viewed` on screen load; `ai_interaction_concerning_flag_acted_on` when the "Adjust AI Controls" link is tapped.

## 24. Performance
`LazyColumn` (or platform-equivalent) with stable keys per entry; no image-heavy content in this screen (icon-only), keeping recomposition light.

## 25. Security
No user-generated/raw text ever rendered — every field is either a controlled category enum's mapped label or a pre-templated summary string sourced from Backend B-03's structurally redacted store. The structural UI test (§27) is this screen's primary trust control, verifying the deliberate absence of any chat-like layout pattern.

## 26. Library Requirements
No new dependencies.

## 27. Testing
1. **Structural UI test:** assert no two consecutive rows are rendered with alternating left/right alignment or any bubble-shaped background resembling a conversation.
2. Unit test: concerning entries render the "Adjust AI Controls" link; non-concerning entries do not.
3. Unit test: empty state renders neutral "No AI interactions recorded" framing.
4. Unit test: deep link to C.23 passes the correct `childId`.
5. Accessibility test: each entry's category/description fully screen-reader-readable.

## 28. Documentation
KDoc explicitly stating the deliberate non-chat-UI design constraint and citing FR-5.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define AiInteractionHistoryUiState and Repository Method**
- Task ID: K03-T01
- Objective: Data model and network fetch.
- Why This Is Required: Foundation for the screen.
- Existing Architecture to Follow: `NoorResult<T>` pattern.
- Existing Files to Reuse: `ReportRepository` (extend).
- Files to Create: `AiInteractionHistoryUiState.kt`.
- Files to Modify: `ReportRepository.kt`.
- Implementation Details: Per §10.
- Business Rules: FR-5, FR-13.
- Validation: N/A.
- Error Handling: `Empty`/`Error` variants.
- Security: N/A at this layer (enforced by data source, B-03).
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: KDoc.
- Dependencies: Backend B-03 live.
- Do Not Change: N/A.
- Expected Result: State model and repository method compile.
- Definition of Done: Matches Backend B-03's response contract.

**Task 02 — Implement AiInteractionHistoryViewModel**
- Task ID: K03-T02
- Objective: Fetch and expose history state.
- Why This Is Required: Core presentation logic.
- Existing Architecture to Follow: `BaseViewModel`.
- Existing Files to Reuse: none new.
- Files to Create: `AiInteractionHistoryViewModel.kt`.
- Files to Modify: none.
- Implementation Details: Per §10, §18.
- Business Rules: FR-5, FR-13.
- Validation: N/A.
- Error Handling: Per §18.
- Security: N/A.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: Fires `ai_interaction_history_viewed`.
- Tests: Covered in Task 04.
- Documentation: KDoc.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: ViewModel emits correct states.
- Definition of Done: Empty/Content/Error all verified.

**Task 03 — Implement AiInteractionHistoryScreen with Deliberate Non-Chat Layout**
- Task ID: K03-T03
- Objective: Flat list-row UI, concerning-entry action link, deep link to C.23.
- Why This Is Required: PRD's explicit, repeated design constraint (§2.1, §7 item 3) — this is a trust-critical visual decision, not a cosmetic one.
- Existing Architecture to Follow: `:core:design-system` list-row components (existing, generic ones — not chat-specific components from elsewhere in the app, if any exist).
- Existing Files to Reuse: Design-system card/list components.
- Files to Create: `AiInteractionHistoryScreen.kt`, `AiInteractionHistoryRoute.kt`.
- Files to Modify: Navigation graph; `PerChildReportScreen.kt` (K-01) to link into this screen.
- Implementation Details: Per §10.
- Business Rules: FR-5.
- Validation: N/A.
- Error Handling: Per §18.
- Security: The layout constraint itself is a trust/security-adjacent requirement.
- Performance: `LazyColumn` with stable keys.
- Localization: Full string-resource coverage.
- RTL: Verified mirroring.
- Analytics: N/A (ViewModel-level).
- Tests: Covered in Task 04.
- Documentation: KDoc citing the non-chat-UI constraint explicitly.
- Dependencies: Task 02.
- Do Not Change: N/A.
- Expected Result: Screen renders correctly, deliberately non-chat-styled.
- Definition of Done: Structural UI test (Task 04) passes.

**Task 04 — Write Test Suite Including Structural Non-Chat-UI Test**
- Task ID: K03-T04
- Objective: Cover §27, with the structural UI test as the defining verification for this screen.
- Why This Is Required: FR-5's visual-layer enforcement.
- Existing Architecture to Follow: Compose UI test conventions (semantics tree inspection).
- Existing Files to Reuse: none new.
- Files to Create: `AiInteractionHistoryViewModelTest.kt`, `AiInteractionHistoryNoChatUiStructuralTest.kt`.
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
- Documentation: Test KDoc citing FR-5.
- Dependencies: Tasks 01–03.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 green, structural test CI-blocking.

## 30. Definition of Done
`AiInteractionHistoryScreen` live, flat list-row design verified structurally non-chat-like, concerning-entry deep link to C.23 functional, empty state neutral and reassuring, all tests green.

## 31. Final Verification Checklist
- [ ] Structural UI test confirms no chat-bubble/alternating-alignment layout anywhere in the composable tree
- [ ] Concerning entries correctly link to C.23 with `childId` pre-selected
- [ ] Empty state framing verified neutral, not alarming
- [ ] Each entry fully screen-reader-accessible
- [ ] Localization and RTL mirroring verified
