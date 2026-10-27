# K-09 — Parent Bedtime Ritual Status Widget

## 1. Feature Context
The lightweight, non-invasive "Bedtime story completed tonight ✓" indicator a parent sees on their Dashboard — listed in the PRD's screen inventory (§1.18, item 16) as an A.4-owned component (unlike item 17, the window/ceiling configuration screen, which is explicitly cross-ref'd away to Feature C.23). B-04 built the backend endpoint this consumes, but no client-side component existed to render it — this sub-feature closes that gap.

## 2. Parent Feature
Feature A.4 — Audio Bedtime Player & Bedtime Mode

## 3. Sub-feature
2.9 Parent Bedtime Ritual Status Widget (ID: **K-09**)

## 4. Objective
Build `BedtimeRitualStatusWidget`, a small Composable placed on the Parent Dashboard (A.2's screen — this sub-feature contributes the component, not a new page) that reads B-04's `GET /v1/children/{id}/bedtime-ritual-status` and renders a simple completion indicator, with an optional drill-in link to A.3's Story Insights for full detail.

## 5. Business Requirements
- FR-12: parent sees a lightweight "bedtime ritual happened" indicator, non-invasive (completion fact only, not full listening transcript/analytics), on their Dashboard.
- §1.9 Acceptance Criteria: "Given a parent views their Dashboard, when they check 'Bedtime Ritual' status, then they see a simple completion indicator (e.g., 'Bedtime story completed tonight ✓') without exposing a full play-by-play transcript... unless they explicitly drill into Story Insights (A.3)."
- §1.18 Screen Inventory item 16: Component (Parent Area), entry point Parent Dashboard, exit point "Story Insights (A.3) for full detail, if parent drills in."
- §12.6: this widget's data source (`bedtime_session_log`) stores only a boolean + date by design — the widget itself must not attempt to render or request anything beyond that.
- §19 (B-04's analytics requirement): `parent_bedtime_ritual_status_viewed` fired when the widget is viewed.

## 6. Existing Architecture
A.2's Home Dashboard / Parent Dashboard module already exists as the host surface for widgets of this kind (confirm the exact existing Parent Dashboard widget-hosting convention — e.g., a widget-registration or slot pattern used by other Parent Dashboard components — and place this widget using that same convention rather than modifying the Dashboard's own layout logic directly).

## 7. Existing Code to Reuse
- Parent Dashboard's existing widget-hosting/slot pattern (confirm exact location — likely within A.2's module or a shared `feature/parent-dashboard/` package)
- `core-network`'s API client conventions (mirror K-07's `BedtimeRepository` client-construction pattern for a new, small read-only client)
- A.3's Story Insights navigation entry point (the drill-in destination — reuse the existing route, do not create a new Story Insights screen)
- `core-designsystem`'s standard (non-bedtime-themed) component tokens — this widget lives on the Parent Dashboard, a standard-mode surface, and must **not** apply K-03's calm/dimmed Bedtime Mode theme overrides (those are scoped to the child's playback session, not parent-facing UI)

## 8. Files to Create
- `feature/bedtime-audio/widget/BedtimeRitualStatusWidget.kt`
- `feature/bedtime-audio/data/BedtimeRitualStatusRepository.kt` (B-04 client: `getStatus(childId, date): BedtimeRitualStatus`)
- `test/feature/bedtime-audio/BedtimeRitualStatusWidgetTest.kt`
- `androidTest/feature/bedtime-audio/BedtimeRitualStatusWidgetUiTest.kt`

## 9. Files to Modify
- Parent Dashboard's widget-hosting composable/registry (A.2) — register `BedtimeRitualStatusWidget` as one of the dashboard's widgets, following the exact existing registration convention

## 10. KMP Requirements
- `BedtimeRitualStatusRepository.getStatus(childId, date = today)`: thin client for B-04's endpoint, no local caching required beyond standard short-TTL request de-duplication (this is a low-frequency, low-cost read — a full offline-cache layer is not warranted, unlike K-07's config, which many other modules depend on repeatedly).
- Widget renders exactly what §1.9's acceptance criteria specifies: a simple completion indicator (e.g., "Bedtime story completed tonight ✓" if `ritual_completed: true`, or a neutral/no-indicator state if `false` — confirm the PRD's implied behavior for the false case is "no alarming negative indicator," consistent with the feature's overall non-invasive, non-shaming tone toward missed nights).
- Drill-in: tapping/clicking the widget (only when `ritual_completed: true`, or generally — confirm against Screen Inventory's stated exit point) navigates to A.3's existing Story Insights screen for full detail — this widget itself never renders duration, content title, or any other listening detail beyond the boolean fact.
- Widget uses standard (non-bedtime) `core-designsystem` visual tokens — this is parent-facing daytime UI, not a Bedtime Mode surface, and must not inherit K-03's dimmed theme overrides.
- Loading state: brief skeleton/placeholder while the status fetch resolves; error state: silently omit the widget or show a neutral "unable to load" placeholder rather than a jarring error banner on the Dashboard (a single non-critical widget failing should not disrupt the rest of the Dashboard).

## 11. Required API
**Admin/Parent API** — B-04 `GET /v1/children/{id}/bedtime-ritual-status?date=`.

## 12. Offline First
Not a primary concern for this widget (Parent Dashboard is typically viewed with connectivity); on fetch failure, degrade to the neutral "unable to load" placeholder described above rather than blocking the Dashboard.

## 13. Local Data
No new local persistence — a simple in-memory/session-scoped fetch per Dashboard view is sufficient given the low read frequency.

## 14. Localization
"Bedtime story completed tonight ✓" and neutral/placeholder copy sourced from shared localization resources across EN/HI/AR/UR.

## 15. RTL
Widget layout (icon/checkmark placement relative to text) mirrors correctly for Arabic/Urdu.

## 16. Analytics
`BedtimeAnalytics`: `parent_bedtime_ritual_status_viewed` fired when the widget successfully renders on the Parent Dashboard (client-side emission, complementing/confirming B-04's note that this event is tied to the endpoint being called by the widget).

## 17. Performance
Single lightweight read per Dashboard view; no polling — the widget fetches once per Dashboard mount, not on a recurring timer.

## 18. Security
- Parent-session-only (inherits the Parent Dashboard's existing auth context — no separate auth check needed in this widget beyond what hosting the widget on an already-parent-gated Dashboard provides).
- Renders strictly the boolean+date fact B-04 returns — no code path in this widget can request or display more detailed data (there is no more detailed field in B-04's response to accidentally expose).

## 19. Testing
- Unit: widget correctly renders the "completed" state vs. the neutral/no-indicator state based on `ritual_completed`.
- Unit: fetch-failure renders the neutral placeholder, not an error that disrupts the Dashboard.
- UI: drill-in tap navigates to A.3's Story Insights screen.
- UI: widget renders using standard (non-bedtime) theme tokens regardless of whether the child is currently in an active Bedtime Mode session elsewhere in the app (theme independence test — this widget's theme must never accidentally inherit K-03's overrides).
- Integration: `parent_bedtime_ritual_status_viewed` fires exactly once per successful widget render.

## 20. AI Coding Agent Implementation Steps

**Task 01 — Implement `BedtimeRitualStatusRepository`**
Objective: Thin client for B-04's endpoint. Files to create: `BedtimeRitualStatusRepository.kt`. Follow: `core-network` conventions. Tests: fetch success/failure handling. Definition of Done: tests pass.

**Task 02 — Implement `BedtimeRitualStatusWidget` Composable**
Objective: Completed/neutral states, loading skeleton, neutral failure placeholder, standard (non-bedtime) theme tokens. Files to create: `BedtimeRitualStatusWidget.kt`. Dependencies: Task 01. Tests: state-rendering tests, theme-independence test. Definition of Done: tests pass.

**Task 03 — Wire the Story Insights Drill-In**
Objective: Tap navigates to A.3's existing Story Insights route — no new detail screen built here. Dependencies: Task 02, A.3's existing route. Tests: navigation test. Definition of Done: test passes.

**Task 04 — Register the Widget on the Parent Dashboard**
Objective: Follow A.2's existing widget-hosting/registration convention. Files to modify: Parent Dashboard's widget registry. Dependencies: Task 02. Definition of Done: widget appears correctly on the Dashboard in a manual/smoke check.

**Task 05 — Add Analytics Instrumentation**
Objective: `parent_bedtime_ritual_status_viewed` fired once per successful render. Dependencies: Task 02. Tests: fake-tracker assertion. Definition of Done: test passes.

**Task 06 — Add Full Test Suite**
Objective: Complete coverage per §19. Definition of Done: all green.

**Task 07 — Final Code Review**
Objective: Confirm the widget renders strictly boolean+date-derived UI with no path to expose detailed content/duration; confirm it never inherits Bedtime Mode's dimmed theme. Definition of Done: checklist in §21 checked.

## 21. Final Verification Checklist
- [ ] Widget renders "completed" vs. neutral state correctly from B-04's boolean response
- [ ] No code path in the widget can render duration, content title, or any data beyond the boolean+date fact
- [ ] Fetch failure degrades to a neutral placeholder, never a Dashboard-disrupting error
- [ ] Drill-in navigates to A.3's existing Story Insights screen, no duplicate detail screen created
- [ ] Widget uses standard (non-bedtime) theme tokens, verified independent of any active Bedtime Mode session elsewhere in the app
- [ ] `parent_bedtime_ritual_status_viewed` fires exactly once per successful render
- [ ] Widget registered via A.2's existing Dashboard widget-hosting convention, no Dashboard layout logic modified directly

## 22. Definition of Done
Parents can see a simple, non-invasive "Bedtime story completed tonight ✓" indicator on their Dashboard, sourced entirely from B-04's privacy-minimal endpoint, with an optional drill-in to A.3's existing Story Insights — closing the PRD's screen-inventory gap left open when only the backend half (B-04) of this feature was originally built.
