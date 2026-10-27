# N-01 — Home Composition Health Monitor

## 1. Feature Context
NoorHeroes Admin Portal (NextJS). Read-only, real-time dashboard showing the live distribution of which Home sections are rendering vs. degraded across the active user base — surfaces product-level upstream health, not just infra metrics.

## 2. Parent Feature
A.2 — Child Home Dashboard & AI Personalization

## 3. Sub-feature
3.1 Home Composition Health Monitor (ID: N-01)

## 4. Objective
Build a dashboard page consuming `GET /admin/v1/home/section-health` (per-region/locale, 1h/24h windows), rendering per-section Content-vs-Hidden/degraded percentages via recharts, with an alert banner when any section's degraded rate exceeds 5% sustained.

## 5. Business Requirements
Per PRD §8, §9 item 1, §10:
- Real-time dashboard (recharts) showing, per region/locale over 1h/24h, the percentage of `/v1/home` responses where each section was Content vs. Hidden/degraded.
- Alert banner if any section's degraded rate exceeds 5% sustained.
- Sourced from a read-only aggregated metrics API.

## 6. Existing Architecture
Follow `noorheroes-admin/NEXT-JS-INSTRUCTIONS.md` for app structure, routing, API-client layer, auth/RBAC, and component conventions. Reuse the existing Admin Portal shell (per PRD §9's explicit instruction: "existing NoorHeroes Admin Portal shell") rather than scaffolding a new app shell.

## 7. Existing Code to Reuse
Existing Admin Portal layout/navigation shell, existing RBAC/auth context, existing recharts wrapper components if already established elsewhere in the admin portal (do not introduce a duplicate charting abstraction).

## 8. Files to Create
- `app/(admin)/home-health/page.tsx`
- `components/home-health/SectionHealthChart.tsx`
- `components/home-health/DegradationAlertBanner.tsx`
- `lib/api/homeHealth.ts` (typed API client for `GET /admin/v1/home/section-health`)
- `types/homeHealth.ts`

## 9. Files to Modify
- Admin Portal navigation/sidebar config — add "Home Composition Monitor" entry

## 10. Backend Requirements
Consumes `GET /admin/v1/home/section-health` (owned by B-01, per B-01 §12). No backend code written here.

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- Page component fetching section-health data (server component or client component with SWR/React Query per existing admin-portal data-fetching convention — follow whatever pattern is already established, do not introduce a second one).
- Chart component (recharts) showing per-section Content vs. Hidden/degraded percentage, filterable by region/locale and 1h/24h window.
- Alert banner component, conditionally rendered when any section's degraded rate exceeds the 5%-sustained-10-minutes threshold (threshold logic likely computed server-side by the metrics API; client renders based on a returned `alert: boolean` flag rather than recomputing sustained-threshold logic client-side, per PRD §10's "sustained 10 minutes" being an inherently time-series/backend concern).

## 13. API Contract
**Endpoint:** `GET /admin/v1/home/section-health` (Admin API)
**Auth:** Admin Bearer session
**Request:** Query params `region`, `locale`, `window` (`1h`|`24h`)
**Response (assumed shape, confirm against actual backend implementation before finalizing types):**
```json
{
  "window": "1h",
  "sections": [
    { "section": "recommended", "content_pct": 92.3, "degraded_pct": 7.7, "alert": true },
    { "section": "habits", "content_pct": 99.8, "degraded_pct": 0.2, "alert": false }
  ]
}
```

## 14. Database Requirements
Not applicable (NextJS reads via API only, no direct DB access).

## 15. Validation
Region/locale/window filter inputs validated client-side (allowed enum values only) before constructing the API request.

## 16. Authentication
Existing Admin Portal Bearer-session auth (reuse existing `useAuth`/session-context hook).

## 17. Authorization
Per PRD §8: no specific RBAC role restriction called out for this monitor (unlike N-03/N-05's `trust_safety` restriction) — confirm against the existing Admin Portal's default authenticated-admin-role gating; do not add a new role requirement not specified in the PRD.

## 18. Error Handling
Loading state (skeleton chart), empty state (no data for selected window/region — explicit message, not a blank chart), error state (API failure — retry affordance, not a raw stack trace).

## 19. Offline First
Not applicable (admin web portal, always-online context).

## 20. Local Data
Not applicable.

## 21. Localization
Admin Portal's existing localization convention applied to UI chrome (labels, filters); underlying data (region/locale names) displayed as-is.

## 22. RTL
Follow existing Admin Portal RTL support convention if the admin portal itself supports RTL locales; otherwise out of scope (confirm against `NEXT-JS-INSTRUCTIONS.md`/existing admin i18n setup rather than assuming).

## 23. Analytics
Not specified as required for internal admin tooling in the PRD; skip unless the existing Admin Portal has a standing convention of instrumenting its own internal tool usage.

## 24. Performance
Chart data fetched on-demand per filter change, not polled aggressively; consider a reasonable refresh interval (e.g., 60s) for the "live" framing without overloading the metrics API — confirm against existing admin-dashboard polling conventions elsewhere in the portal.

## 25. Security
Read-only surface; no mutation actions. Standard admin-session auth applies.

## 26. Library Requirements
Next.js (existing App Router conventions), recharts, existing admin-portal API-client/data-fetching library.

## 27. Testing
- Component test: chart renders correctly with fixture section-health data.
- Component test: alert banner renders when any section has `alert: true`.
- Component test: empty/error/loading states render correctly.
- Integration test: filter changes (region/locale/window) trigger correct API calls.

## 28. Documentation
Page-level README/comment noting this consumes a read-only metrics API and has no write/mutation capability.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Types & API Client**
- Objective: Typed contract for the section-health API.
- Why Required: Type safety across the page/components.
- Existing Architecture to Follow: Existing admin-portal API-client conventions.
- Existing Files to Reuse: Existing typed-fetch wrapper if present.
- Files to Create: `types/homeHealth.ts`, `lib/api/homeHealth.ts`
- Files to Modify: none
- Implementation Details: `SectionHealth { section: string; contentPct: number; degradedPct: number; alert: boolean }`; `getSectionHealth(region, locale, window)`.
- Business Rules: N/A.
- Validation: Enum-validated filter params.
- Error Handling: Typed error result on API failure.
- Security: N/A.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Unit test for the API client (mocked fetch).
- Documentation: JSDoc/TSDoc.
- Dependencies: None (coordinate with B-01's actual response shape once available; treat as provisional until confirmed).
- Do Not Change: N/A.
- Expected Result: Typed client.
- Definition of Done: Unit test passes.

**Task 02 — Build `SectionHealthChart` Component**
- Objective: recharts visualization of per-section health.
- Why Required: Primary UI deliverable.
- Existing Architecture to Follow: Existing admin-portal chart/component conventions.
- Existing Files to Reuse: Existing recharts wrapper if present.
- Files to Create: `components/home-health/SectionHealthChart.tsx`
- Files to Modify: none
- Implementation Details: Stacked/grouped bar chart per section (Content % vs. Degraded %), filterable by region/locale/window props.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Empty-data state handled distinctly from loading.
- Security: N/A.
- Performance: Memoized chart data transformation.
- Localization: Axis/legend labels via string resources if the admin portal is localized.
- RTL: Per §22.
- Analytics: N/A.
- Tests: Component test with fixture data.
- Documentation: TSDoc.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Working chart.
- Definition of Done: Component test passes.

**Task 03 — Build `DegradationAlertBanner` + Page Composition**
- Objective: Alert banner and full page assembly with filters.
- Why Required: PRD §9 item 1 explicit alert requirement.
- Existing Architecture to Follow: Existing admin-portal page/layout conventions.
- Existing Files to Reuse: Admin Portal shell, auth context.
- Files to Create: `components/home-health/DegradationAlertBanner.tsx`, `app/(admin)/home-health/page.tsx`
- Files to Modify: Admin navigation/sidebar config
- Implementation Details: Banner renders when any section in the fetched data has `alert: true`, listing affected sections; page composes filters + chart + banner + loading/empty/error states.
- Business Rules: Banner reflects backend-computed `alert` flag (sustained-threshold logic lives server-side).
- Validation: N/A.
- Error Handling: Full page-level error/loading/empty handling per §18.
- Security: Standard admin-session auth gate on the route.
- Performance: Reasonable polling interval per §24.
- Localization: UI chrome localized per admin-portal convention.
- RTL: Per §22.
- Analytics: N/A.
- Tests: Component tests for banner visibility logic; integration test for filter-driven refetch.
- Documentation: Page comment.
- Dependencies: Tasks 01, 02.
- Do Not Change: N/A.
- Expected Result: Complete monitor page.
- Definition of Done: All tests pass; navigation entry added.

## 30. Definition of Done
Dashboard renders live per-section health with correct filtering, alert banner reflects backend-computed sustained-degradation state, and all states (loading/empty/error) handled gracefully; all tests green.

## 31. Final Verification Checklist
- [ ] Chart renders correct per-section Content vs. Degraded percentages
- [ ] Alert banner appears exactly when backend `alert` flag is true for any section
- [ ] Loading/empty/error states all handled distinctly (no blank/broken UI)
- [ ] Filter changes (region/locale/window) trigger correct, validated API calls
- [ ] Route gated by existing Admin Portal auth
- [ ] All tests pass
