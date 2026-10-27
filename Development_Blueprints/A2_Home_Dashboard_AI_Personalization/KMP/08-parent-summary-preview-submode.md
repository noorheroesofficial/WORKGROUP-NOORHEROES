# K-08 — Parent Summary Preview Sub-Mode

## 1. Feature Context
NoorHeroes Child App (KMP). Renders a condensed, read-only Home preview overlay when a Parent Profile views a child's Home via "Preview [Child]" from the Parent Dashboard.

## 2. Parent Feature
A.2 — Child Home Dashboard & AI Personalization

## 3. Sub-feature
2.8 Parent Summary Preview Sub-Mode (ID: K-08)

## 4. Objective
Build the Parent Summary Preview overlay that renders a condensed "today's progress" widget when a parent is in an active Parent session, without re-prompting for PIN and without exposing the child's interactive habit-check-in controls.

## 5. Business Requirements
Per PRD FR-14, §1.9 Acceptance Criteria, §1.18 Screen 17:
- Visible only when the Parent Profile views a child's Home in "preview" sub-mode, not visible to the child.
- Shows today's completed activities and healthy-usage status.
- Does not require full Parent PIN re-entry if already in an active Parent session.
- Renders the condensed Parent Summary widget overlay, not the child's literal habit-check-in controls.

## 6. Existing Architecture
Reuses A.1/C.19's existing Parent PIN/Biometric Gate session-state mechanism (do not re-implement PIN checking here) and Parent Dashboard navigation entry point (C.20, external to this sub-feature).

## 7. Existing Code to Reuse
Existing Parent-session state check (from C.19 Parent PIN/Biometric Gate); K-01's `HomeUiState` data (read-only reuse — this overlay derives its condensed view from the same underlying data, not a duplicate fetch, where feasible).

## 8. Files to Create
- `feature/home/src/commonMain/kotlin/.../components/ParentSummaryPreviewOverlay.kt`
- `feature/home/src/commonMain/kotlin/.../models/ParentPreviewSummary.kt`

## 9. Files to Modify
- Parent Dashboard navigation (C.20, external) — wire "Preview [Child]" entry point to launch Home in preview sub-mode
- `HomeScreen.kt` (K-01) — accept a `previewMode: Boolean` parameter that swaps interactive child controls for the read-only overlay

## 10. Backend Requirements
Consumes the same `GET /v1/home` response (B-01) as the child-mode view; no new backend endpoint required for this sub-feature specifically (the underlying data is identical, only the client-side rendering mode differs) — confirm this assumption holds; if a genuinely different, more privacy-conscious payload is required for parent-preview context, flag for a backend follow-up rather than silently over-fetching child-mode-only fields.

## 11. KMP Requirements
- `HomeScreen(previewMode: Boolean = false)` — when `true`, renders `ParentSummaryPreviewOverlay` instead of the full interactive section stack.
- Overlay shows: today's completed activities summary, healthy-usage status (e.g., screen-time-within-limits indicator) — condensed, not the full section-by-section child view.
- No interactive habit-check-in controls rendered in this mode (read-only).
- No PIN re-prompt if `ParentSessionState.isActive == true` (checked via existing C.19 session mechanism) — reuse, do not duplicate the check.
- "Back to Parent Dashboard" exit action.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
Reuses `GET /v1/home` per B-01 §13 (same contract as child-mode); no distinct parent-preview endpoint introduced unless a backend follow-up (per §10) determines one is needed.

## 14. Database Requirements
Not applicable directly (reads same `HomeUiState`-shaped data).

## 15. Validation
Preview mode must never expose the child's actual interactive controls (e.g., tapping a "completed activity" in the summary must not trigger a habit check-in mutation) — this is a rendering-mode distinction enforced by using a distinct, non-interactive Composable (`ParentSummaryPreviewOverlay`), not by disabling interactive controls after the fact.

## 16. Authentication
Reuses the parent's existing authenticated session (Bearer token scoped to the parent, with child-preview authorization — confirm the exact token/claim shape used for "parent viewing child X" against C.19/C.20's existing implementation rather than assuming).

## 17. Authorization
Parent must have an active, verified Parent session (per C.19) and be authorized for the specific `family_id`/`child_id` being previewed; reuse existing authorization checks from C.19/C.20 rather than introducing a new check.

## 18. Error Handling
Same per-section graceful degradation as child-mode Home (inherits `HomeUiState`'s existing Loading/Content/Error/Hidden handling), condensed into the summary view.

## 19. Offline First
Not a primary offline scenario for this sub-feature (parent preview is a lower-frequency, typically-online interaction); if offline, reuse K-07's existing cache-or-network behavior as-is rather than building a parallel path.

## 20. Local Data
Reuses K-07's `HomeLocalCache` read path if available; no new local storage introduced.

## 21. Localization
Overlay copy via string resources, parent-facing tone (per A.1's parent-facing localization conventions, distinct from child-facing copy tone).

## 22. RTL
Overlay layout mirrors correctly per existing parent-facing screen RTL conventions (from A.1's Parent PIN Setup/Add Child screens).

## 23. Analytics
`parent_preview_child_home_opened`.

## 24. Performance
Reuses existing `HomeUiState` data where possible rather than triggering a second independent fetch, to avoid redundant network/cache load when a parent previews immediately after (or during) an active child session.

## 25. Security
No interactive child-mode mutation paths reachable from this overlay (§15); reuses existing Parent session/authorization checks rather than introducing a new, potentially weaker check.

## 26. Library Requirements
Compose Multiplatform, existing navigation library, existing Parent-session state provider (from C.19).

## 27. Testing
- Compose UI: preview overlay renders condensed summary correctly, with no interactive habit-check-in controls present in the semantics tree.
- Integration: active Parent session does not trigger a PIN re-prompt when entering preview mode.
- Integration: preview mode correctly blocks any attempt to trigger a child-mode mutation (e.g., simulate a tap on a summary item, assert no `POST /v1/habits/check-ins` call is made).

## 28. Documentation
KDoc explaining the rendering-mode distinction (`previewMode` flag) and why it uses a dedicated non-interactive Composable rather than disabling controls on the standard child view, to prevent a future regression where an interactive control accidentally leaks into preview mode.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define `ParentPreviewSummary` Model**
- Objective: Condensed data shape for the overlay.
- Why Required: Type-safe, minimal-surface data for the preview view.
- Existing Architecture to Follow: K-01 data-model conventions.
- Existing Files to Reuse: `HomeUiState`.
- Files to Create: `models/ParentPreviewSummary.kt`
- Files to Modify: none
- Implementation Details: `data class ParentPreviewSummary(completedActivitiesToday: List<String>, healthyUsageStatus: UsageStatus)` derived from existing `HomeUiState` fields (mission/quiz/habit completion flags, screen-time status if available from C.23 integration).
- Business Rules: Read-only, derived — no independent mutation-capable fields.
- Validation: N/A.
- Error Handling: N/A.
- Security: No mutation-capable fields by construction.
- Performance: Derived via a pure mapping function from existing state, not a new fetch.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Unit test for the derivation mapping.
- Documentation: KDoc.
- Dependencies: K-01 Task 01.
- Do Not Change: N/A.
- Expected Result: Model defined.
- Definition of Done: Unit test passes.

**Task 02 — Build `ParentSummaryPreviewOverlay` Composable + `previewMode` Wiring**
- Objective: Non-interactive overlay UI and `HomeScreen` mode-switching.
- Why Required: Core deliverable of this sub-feature.
- Existing Architecture to Follow: `:core:design-system` tokens; existing C.19 Parent-session state provider.
- Existing Files to Reuse: `HomeUiState`, C.19 session-state check.
- Files to Create: `components/ParentSummaryPreviewOverlay.kt`
- Files to Modify: `HomeScreen.kt` (add `previewMode` parameter), Parent Dashboard navigation entry point
- Implementation Details: `HomeScreen(previewMode: Boolean = false)` — when `true`, renders `ParentSummaryPreviewOverlay(summary, onBack)` instead of the interactive section stack; overlay checks `ParentSessionState.isActive` (existing C.19 mechanism) before rendering, skipping any PIN prompt when already active.
- Business Rules: No interactive controls in this Composable at all (not disabled — absent).
- Validation: N/A.
- Error Handling: Inherits existing per-section degradation, condensed.
- Security: No PIN re-prompt when session already active; reuses existing authorization check for parent-viewing-child access.
- Performance: Reuses existing `HomeUiState` fetch where available.
- Localization: Parent-facing string resources.
- RTL: Verified per existing parent-facing screens.
- Analytics: `parent_preview_child_home_opened` fired on entry.
- Tests: Compose UI test confirming zero interactive-control nodes in the semantics tree; integration test confirming no mutation call is ever triggered from this overlay; integration test confirming no PIN re-prompt when session is active.
- Documentation: KDoc per §28.
- Dependencies: Task 01.
- Do Not Change: Do not reuse the standard interactive habit-checklist Composable "with controls disabled" — use a distinct non-interactive Composable.
- Expected Result: Working, safely non-interactive preview overlay.
- Definition of Done: All three test scenarios above pass.

## 30. Definition of Done
Parent preview overlay renders a condensed, strictly non-interactive summary without re-prompting for PIN in an active session, and cannot trigger any child-mode mutation; all tests green.

## 31. Final Verification Checklist
- [ ] Overlay contains zero interactive child-mode controls in its semantics tree
- [ ] No PIN re-prompt occurs when entering preview during an active Parent session
- [ ] No mutation API call (e.g., habit check-in) can be triggered from the overlay, verified by test
- [ ] Authorization reuses existing C.19/C.20 checks, no new/weaker check introduced
- [ ] RTL and parent-facing localization verified
- [ ] All tests pass
