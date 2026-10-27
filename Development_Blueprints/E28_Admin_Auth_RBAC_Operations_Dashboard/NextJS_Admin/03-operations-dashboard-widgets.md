# N-03 — Operations Dashboard Widgets

## 1. Feature Context
Part of E.28. Screen #5 in PRD §1.18, the default landing surface for every admin. Extends the existing `DashboardRepositoryImpl`/`useDashboardStats()` pattern into the full 8-widget composite specified in PRD §2.2.

## 2. Parent Feature
E.28 — Admin Portal: Authentication, RBAC & Operations Dashboard

## 3. Sub-feature
N-03 — Operations Dashboard Widgets

## 4. Objective
Render each of the 8 widgets with an independently loading/error/content state, such that one widget's data-fetch failure never blocks the other 7 from rendering their own successful fetches (PRD §7 Frontend AI prompt item 5).

## 5. Business Requirements
- FR-7: 8 canonical widgets.
- FR-8: same signals engineers see, role-scoped.
- Edge Case 5: monitoring-source outage → explicit "data temporarily unavailable" per widget, never silently stale/hidden.
- §1.12: zero active incidents → calm "All systems normal" state.
- §1.13: per-widget independent skeleton loading, mirroring C.20's Parent Dashboard pattern.
- §2.2: accessibility — key figures screen-reader-readable as plain text/numbers, not chart-only; responsive grid reflow.

## 6. Existing Architecture
- `DashboardRepositoryImpl`/`useDashboardStats()` already exist per the NextJS instructions manual — currently a single aggregate stats fetch. N-03 must decide: extend `useDashboardStats()` into 8 independently-fetched/independently-failable queries, or keep one API call (per B-08's single `GET /v1/admin/dashboard` endpoint which itself composes server-side with per-widget `data_unavailable` flags) and simply render each widget's slice of that one response independently. **Decision: reuse the single-request pattern (matches B-08's contract) — `useDashboardStats()` extended to fetch the full 8-widget payload in one React Query call, with each widget component reading its own slice and independently handling that slice's `data_unavailable` flag; this satisfies "independent loading/error/content state" at the render level even though the fetch itself is a single request, consistent with B-08's server-side per-widget fallibility already doing the hard resilience work.**
- `DataTable`, `EmptyState`, `ErrorView`, `LoadingState`, `QueryErrorState` — all directly reusable for widget content/empty/error/loading states.

## 7. Existing Code to Reuse
| Component | Location | Reuse For |
|---|---|---|
| `useDashboardStats()` | `src/features/dashboard/hooks/` | Extend to full 8-widget payload |
| `DashboardRepositoryImpl` | `src/features/dashboard/api/` | Extend `getStats()` to the new shape |
| `LoadingState` | `src/shared/components/` | Per-widget skeleton |
| `EmptyState` | `src/shared/components/` | "All systems normal" / "Nothing pending" style empty states |
| `ErrorView` | `src/shared/components/` | Per-widget "data unavailable" state |
| `useFormatters()` | `src/shared/hooks/` | Number/date formatting within widgets |

## 8. Files to Create
- `src/app/(dashboard)/operate/page.tsx` — Operations Dashboard route (default landing)
- `src/features/dashboard/components/widget-grid.tsx`
- `src/features/dashboard/components/widgets/active-families-widget.tsx`
- `src/features/dashboard/components/widgets/learning-completion-widget.tsx`
- `src/features/dashboard/components/widgets/content-review-widget.tsx`
- `src/features/dashboard/components/widgets/safety-alerts-widget.tsx`
- `src/features/dashboard/components/widgets/subscription-health-widget.tsx`
- `src/features/dashboard/components/widgets/notification-performance-widget.tsx`
- `src/features/dashboard/components/widgets/ai-refusal-widget.tsx`
- `src/features/dashboard/components/widgets/failed-jobs-widget.tsx`
- `src/features/dashboard/components/widget-unavailable-state.tsx` — shared "data temporarily unavailable" presentational component
- `tests/features/dashboard/widget-independent-failure.test.tsx`

## 9. Files to Modify
- `src/features/dashboard/hooks/use-dashboard-stats.ts` — extend response typing to the 8-widget shape (including `data_unavailable` per widget)
- `src/features/dashboard/api/dashboard.repository.ts` — extend Zod schema validation for the new response shape

## 10. NextJS Requirements
- 8 widget cards in a responsive grid (multi-column desktop → stacked single-column at narrower viewports).
- Each widget independently renders: loading skeleton, "data unavailable" state (if `data_unavailable=true`), or populated content — never a global all-or-nothing render.
- Incident widget: calm "All systems normal" empty state when zero active incidents; each incident links to its runbook where `runbook_url` is present.
- Key figures rendered as real DOM text/numbers (not canvas-only chart labels) for screen-reader accessibility.

## 11. API Contract (Consumed)
`GET /v1/admin/dashboard` (B-08) → 8-widget composite payload, each with a `data_unavailable: boolean` field.

## 12. Database Requirements
N/A (frontend).

## 13. Validation
Zod schema validates the 8-widget response shape; a malformed/missing widget key in the response is treated as that widget's `data_unavailable=true` fallback, not a whole-page crash (defensive parsing).

## 14. Authentication
Assumes an established session (N-01) and passes through the standard `apiClient` Bearer-token injection.

## 15. Authorization
Widget-level detail may vary per role (per B-08's role-scoped composition) — the frontend simply renders whatever shape the server returns for the current admin, no client-side role branching needed for content (only for whether the Dashboard route itself is reachable at all, via N-02's nav-permission gating).

## 16. Error Handling
- Per-widget `data_unavailable=true` → render `WidgetUnavailableState`, never silently show stale/zero data as if current (Edge Case 5).
- Whole-request failure (e.g., network down) → `QueryErrorState` with retry, applied to the entire grid (a genuinely different failure mode than a single widget being flagged unavailable server-side).
- Zero incidents → `EmptyState` "All systems normal", not a blank gap.

## 17. Offline First
N/A (per PRD §6.7).

## 18. Local Data
None persisted; React Query cache only, standard TTL/staleness per existing `useDashboardStats()` configuration.

## 19. Localization
Widget titles/labels via `useTranslation()`; numbers/dates via `useFormatters()`.

## 20. RTL
Widget grid must reflow correctly for RTL locales; sparkline/chart elements (if any) must not visually break in RTL (test explicitly, since charts are a common RTL failure point).

## 21. Analytics
Fire `operations_dashboard_viewed` on mount; `incident_viewed`, `service_health_viewed`, `job_failure_viewed` on respective widget/detail interactions.

## 22. Performance
- Single React Query fetch for the full payload (avoids 8 separate HTTP round trips); per-widget rendering is a pure client-side split of that one response.
- Memoize widget components to avoid unnecessary re-renders when unrelated parent state changes.
- Consider a short client-side polling interval or manual refresh affordance to support the ≤2-minute freshness target (coordinate with B-08's server-side cache TTL — client polling interval should not undercut the server cache's effectiveness).

## 23. Security
No sensitive data handling beyond what's already gated by session/route access; widget content trusted from the authenticated API response, standard XSS-safe rendering (no `dangerouslySetInnerHTML` for any widget text).

## 24. Library Requirements
No new libraries — reuses existing chart/sparkline approach if one already exists in the codebase (check for an existing charting library before introducing a new one; if none exists, a lightweight sparkline can be hand-rolled with SVG rather than pulling in a full charting library for 8 small widgets).

## 25. Testing
- **Mandatory test (§7 item 5):** simulate one widget's data fetch failing (via a malformed/`data_unavailable=true` slice in a mocked response) and confirm the other 7 render normally from their own successful data.
- Unit: each widget component's loading/error/content state rendering.
- Unit: incident widget's empty state and runbook-link rendering.
- Accessibility: screen-reader text presence for all key figures.
- Responsive: grid reflow snapshot test at desktop and narrow viewport widths.

## 26. Documentation
Document the widget-grid extension pattern for E.29–E.34 authors, in case any future module wants to contribute an additional dashboard widget (out of E.28's own scope to design that extensibility mechanism fully, but the 8 hardcoded widgets here should not structurally block a future generalized widget-registry approach).

## 27. AI Coding Agent Implementation Steps

**Task 01 — Extend Dashboard Data Layer to the 8-Widget Shape**
- Task ID: N-03-T01
- Files to Modify: `use-dashboard-stats.ts`, `dashboard.repository.ts`.
- Implementation Details: Zod schema for the full B-08 response shape; defensive parsing so a missing/malformed widget key degrades to `data_unavailable=true` rather than throwing.
- Dependencies: B-08 endpoint available.
- Definition of Done: Hook returns typed, validated 8-widget data.

**Task 02 — Build `WidgetUnavailableState` Shared Component**
- Task ID: N-03-T02
- Files to Create: `widget-unavailable-state.tsx`.
- Implementation Details: Presentational "data temporarily unavailable" card, reused by all 8 widgets.
- Dependencies: None.
- Definition of Done: Renders correctly in isolation.

**Task 03 — Build Each of the 8 Widget Components**
- Task ID: N-03-T03
- Files to Create: the 8 widget component files listed in §8.
- Implementation Details: Each reads its own slice of the shared query result; renders loading/unavailable/content independently; key figures as plain text.
- Accessibility: Screen-reader-readable figures.
- Tests: Per-widget render tests (loading, unavailable, populated).
- Dependencies: Task 01, Task 02.
- Definition of Done: All 8 widgets render correctly in isolation with mocked data.

**Task 04 — Build the Widget Grid & Dashboard Page**
- Task ID: N-03-T04
- Files to Create: `widget-grid.tsx`, `operate/page.tsx`.
- Implementation Details: Responsive grid layout composing all 8 widget components.
- Dependencies: Task 03.
- Definition of Done: Page renders full 8-widget grid, responsive at desktop and narrow viewports.

**Task 05 — Independent-Failure Signature Test**
- Task ID: N-03-T05
- Objective: Prove one widget's failure never blocks the others.
- Files to Create: `tests/features/dashboard/widget-independent-failure.test.tsx`.
- Implementation Details: Mock a response where one widget key has `data_unavailable=true`; assert the other 7 render their populated content states correctly.
- Dependencies: Task 04.
- Definition of Done: Test passes; this is the canonical proof point for PRD §7 item 5.

**Task 06 — Incident Widget Empty State & Runbook Linking**
- Task ID: N-03-T06
- Objective: "All systems normal" empty state; runbook links rendered when present.
- Files to Modify: `failed-jobs-widget.tsx`.
- Dependencies: Task 03.
- Definition of Done: Zero-incidents state and runbook-link rendering both verified.

**Task 07 — Localization, RTL, Accessibility, Analytics Pass**
- Task ID: N-03-T07
- Dependencies: Task 04.
- Definition of Done: All widget text localized; RTL reflow verified; analytics events firing.

**Task 08 — Full Test Suite + Documentation**
- Task ID: N-03-T08
- Dependencies: Tasks 01–07.
- Definition of Done: All §25 scenarios green.

## 28. Definition of Done
- All 8 widgets rendering independently loading/unavailable/content states.
- Zero-incidents calm empty state present.
- Full responsive/RTL/accessibility/localization coverage.
- Signature independent-failure test passing.

## 29. Final Verification Checklist
- [ ] Signature test passes: one widget's `data_unavailable=true` doesn't block the other 7
- [ ] All 8 canonical widgets present and correctly labeled
- [ ] "All systems normal" empty state renders on zero incidents
- [ ] Runbook links render where `runbook_url` is present
- [ ] Key figures are screen-reader-readable plain text, not chart-only
- [ ] Responsive grid reflow verified desktop → narrow viewport
- [ ] RTL layout verified for AR/UR
- [ ] `operations_dashboard_viewed` and related analytics events fire correctly
