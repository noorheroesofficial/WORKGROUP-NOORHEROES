# Blueprint: Weekly AI Report Card Preview

## 1. Feature Context
Platform: NoorHeroes KMP App. Module `:feature:parent-dashboard`. Renders the highest-conversion, trust-centerpiece component of the Dashboard.

## 2. Parent Feature
C.20 — Parent Dashboard.

## 3. Sub-feature
K-03 — Weekly AI Report Card Preview.

## 4. Objective
Render the Weekly AI Report card with headline insight, trend-line visual, "View full report" link, and its 3 variant states: normal, report-delayed ("as of" framing), and AI Insight locked/upsell (non-premium) — each fed by B-03's report-retrieval API.

## 5. Business Requirements
Source: PRD §1.7 FR-8, FR-9, FR-10, FR-11, §1.10 Edge Case #5, §2.1, §2.2, §7 (Android AI Code-Gen Prompt items 3–4).
- Calm, trend-oriented visual language — never pass/fail or letter-grade styling (FR-9).
- Data-freshness "as of" label on every load (§2.1).
- Delayed state shows previous report with explicit "as of [date]", never blank.
- AI Insight locked/upsell state for non-premium — this is the ONLY context in the entire app where a billing/upsell element is permitted to render in a screen reachable from a session (verified Parent Mode only), explicitly exempt from the platform-wide no-billing-content-to-child rule, but must be structurally proven never reachable from a child-mode session path.

## 6. Existing Architecture
Builds on K-01's ViewModel/state architecture. Consumes `DashboardRepository.getReport(type, childId)` (interface defined in K-01, backed by B-03).

## 7. Existing Code to Reuse
- K-01's `DashboardRepository` interface, `ParentDashboardViewModel`.
- `:core:design-system` trend-line chart primitive (confirm existence/name before use — if none exists, this is a legitimate new design-system addition, flagged for design-system team coordination rather than a one-off local chart component).
- `Navigator` (`core-navigation`) for "View full report" → C.22 navigation, and locked-state CTA → `:feature:subscription` (C.24).

## 8. Files to Create
- `feature/parent-dashboard/src/commonMain/kotlin/.../WeeklyReportCard.kt`
- `feature/parent-dashboard/src/commonTest/kotlin/.../WeeklyReportCardStateTest.kt`
- `feature/parent-dashboard/src/commonTest/kotlin/.../AiInsightLockedStateReachabilityTest.kt`

## 9. Files to Modify
- `DashboardUiState.kt` — add `weeklyReportState: ComponentState<WeeklyReportPreview>` with variants `Normal`, `Delayed(asOf)`, `Locked(upsellReason)`
- `ParentDashboardViewModel.kt` — fetch report via `getReport("weekly", childId)` and `getReport("ai_insight", childId)`

## 10. KMP Requirements
- `WeeklyReportCard` Composable renders headline insight + trend-line + "View full report" link (→ `Navigator.navigateTo(PerChildReportRoute(childId))`, C.22 — **confirmed exact signature**: `@Serializable data class PerChildReportRoute(val childId: String) : Route`, per C.22 K-01's already-written blueprint, which explicitly cross-references `ParentDashboardRoute`/`BaseAuthState.Parent` as the pattern it mirrors) in the `Normal` state. Per B-03's corrected scope note (backend), this link takes the parent to C.22's FULL depth report screen — this card itself only ever shows the condensed Dashboard preview.
- `Delayed` state: same card shell, but content replaced with previous period's summary and a clearly-labeled "as of [date]" badge, never a blank/broken card.
- `Locked` state (ai_insight specifically, distinct sub-slice from the weekly summary): upsell CTA linking to `:feature:subscription` (C.24) via `Navigator`.
- Structural test: confirm this locked-state composable is unreachable from any code path originating in a child-mode session (PRD Android AI Code-Gen Prompt item 3) — since `:feature:parent-dashboard` itself is only reachable via the Parent Gate, this test reinforces rather than contradicts the platform-wide rule.
- Accessibility: trend chart must have a text-equivalent summary (not relying on visual-only interpretation) per PRD §2.2.

## 11. Files/Screens
Composable within K-01's `ParentDashboardScreen`; "View full report" navigates externally to C.22 (not owned here).

## 12. NextJS Requirements
N/A.

## 13. API Contract
Consumes `GET /v1/parent/dashboard/reports/weekly?child_id=` and `GET /v1/parent/dashboard/reports/ai_insight?child_id=` (B-03) via `DashboardRepository.getReport(type, childId)`.

## 14. Database Requirements
N/A new — cached via K-07.

## 15. Validation
N/A beyond what B-03 already validates server-side.

## 16. Authentication
Inherits K-01's Parent Gate.

## 17. Authorization
Inherits K-01's family/child scoping; `ai_insight` premium-gating is server-driven (B-03 returns the locked shape), this component only renders what the API returns — never performs its own client-side entitlement check that could drift from the server's source of truth.

## 18. Error Handling
Independent slice per K-01's architecture — a weekly-report fetch failure doesn't block the AI-insight sub-slice or other Dashboard components.

## 19. Offline First
Cached via K-07; offline render shows last-cached report with "may be outdated" indicator, distinct from the "delayed" (server-side generation lag) state — the two must be visually distinguishable so parents don't conflate "app is offline" with "your weekly report is late."

## 20. Local Data
Cached report content via Room (K-07).

## 21. Localization
Headline insight and trend labels come pre-localized from B-04's generation pipeline (server-side); this component must not re-translate or hardcode fallback English text.

## 22. RTL
Trend-line chart and "as of" badge must mirror correctly; date formatting via `Instant.toLocalizedDateString()` (`core-common` ext function) for correct locale-aware date display.

## 23. Analytics
`weekly_report_card_viewed`, `weekly_report_card_tapped`, `ai_insight_locked_state_shown`, `dashboard_report_delayed_state_shown` (PRD §1.19).

## 24. Performance
Trend-chart rendering should not block card skeleton dismissal; use stable/immutable chart-data models to avoid recomposition thrashing.

## 25. Security
Locked-state upsell CTA is the sole exception to the platform-wide no-billing-content-to-child rule; the reachability structural test (Task 03) is this component's most important security-adjacent guarantee.

## 26. Library Requirements
No new dependencies unless the trend-line chart primitive requires one not already present in `:core:design-system` (flag rather than invent).

## 27. Testing
1. Unit test: normal-state renders headline + trend-line + link.
2. Unit test: delayed-state renders previous report with correct "as of" framing, never blank.
3. UI test: locked-state composable tree contains an upsell CTA linking to `:feature:subscription`.
4. **Structural test (mandatory):** locked-state/this entire module is never reachable via any code path originating from an active child-mode session.
5. Unit test: independent failure isolation (weekly-report fetch failure doesn't affect timeline/screen-time components).
6. Accessibility test: trend chart has a text-equivalent summary.

## 28. Documentation
KDoc citing PRD §7 items 3–4 and the explicit platform-wide-rule-exemption rationale.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Extend State and Fetch Logic**
- Task ID: K03-T01
- Objective: Add weekly/ai_insight report fetching to the ViewModel.
- Why This Is Required: Data plumbing for this component.
- Existing Architecture to Follow: K-01's independent-slice pattern.
- Existing Files to Reuse: `DashboardRepository.getReport()`.
- Files to Create: none.
- Files to Modify: `DashboardUiState.kt`, `ParentDashboardViewModel.kt`.
- Implementation Details: Per §10.
- Business Rules: FR-8, FR-11.
- Validation: N/A.
- Error Handling: Independent slice.
- Security: N/A.
- Performance: N/A.
- Localization: N/A (state only).
- RTL: N/A.
- Analytics: Fetch triggers `weekly_report_card_viewed` on successful render.
- Tests: Covered in Task 04.
- Documentation: KDoc.
- Dependencies: K-01.
- Do Not Change: N/A.
- Expected Result: State populated correctly for all 3 variants.
- Definition of Done: Matches §10.

**Task 02 — Build WeeklyReportCard Composable (3 Variants)**
- Task ID: K03-T02
- Objective: Visual rendering of normal/delayed/locked states.
- Why This Is Required: UI delivery.
- Existing Architecture to Follow: `:core:design-system`, trend-oriented visual language (FR-9).
- Existing Files to Reuse: Design-system card/chart primitives.
- Files to Create: `WeeklyReportCard.kt`.
- Files to Modify: `ParentDashboardScreen.kt`.
- Implementation Details: Per §10.
- Business Rules: FR-9, FR-10, FR-11.
- Validation: N/A.
- Error Handling: N/A.
- Security: N/A.
- Performance: Stable chart-data model.
- Localization: Pre-localized content from server, no client-side hardcoding.
- RTL: Mirrors correctly; localized date formatting.
- Analytics: `weekly_report_card_tapped`, `ai_insight_locked_state_shown`, `dashboard_report_delayed_state_shown`.
- Tests: Covered in Task 04.
- Documentation: KDoc.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: All 3 variants render correctly.
- Definition of Done: Matches PRD §2.2/§1.18 rows 3, 7, 11.

**Task 03 — Structural Reachability Test for Locked State**
- Task ID: K03-T03
- Objective: Prove locked-state upsell is never reachable from child-mode.
- Why This Is Required: PRD Android AI Code-Gen Prompt item 3 explicit mandate.
- Existing Architecture to Follow: Reflection/navigation-graph analysis pattern used elsewhere (B.16/C.19-style structural tests).
- Existing Files to Reuse: Navigation graph test utilities if present.
- Files to Create: `AiInsightLockedStateReachabilityTest.kt`.
- Files to Modify: none.
- Implementation Details: Assert `ParentDashboardRoute`'s `requiredAuthState` (and therefore this component, nested within it) cannot be satisfied by a child-mode `BaseAuthState`.
- Business Rules: Platform-wide no-billing-to-child rule, with this component as the sole exemption.
- Validation: N/A.
- Error Handling: N/A.
- Security: This IS the security-critical test.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the test.
- Documentation: Test KDoc citing the exemption rationale.
- Dependencies: K-01 (Route definition).
- Do Not Change: N/A.
- Expected Result: Test proves unreachability.
- Definition of Done: Test passes and would fail if `requiredAuthState` were ever loosened.

**Task 04 — Write Remaining Test Suite**
- Task ID: K03-T04
- Objective: Cover remaining §27 items.
- Why This Is Required: QA coverage.
- Existing Architecture to Follow: Existing Compose/Kotlin test conventions.
- Existing Files to Reuse: Fake repository test doubles.
- Files to Create: `WeeklyReportCardStateTest.kt`.
- Files to Modify: none.
- Implementation Details: Items 1, 2, 3, 5, 6 from §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: N/A.
- Security: N/A.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test KDoc.
- Dependencies: Tasks 01–03.
- Do Not Change: N/A.
- Expected Result: All pass.
- Definition of Done: 100% of §27 green.

## 30. Definition of Done
All 3 card variants render correctly, delayed-state never blank, locked-state upsell CTA present and structurally proven unreachable from child-mode, analytics firing, all tests green.

## 31. Final Verification Checklist
- [ ] Trend-oriented visual language, no pass/fail styling anywhere
- [ ] Delayed state always shows previous report, never blank
- [ ] Locked-state reachability structural test passing
- [ ] Text-equivalent accessibility summary present for trend chart
- [ ] RTL and localized date formatting verified
