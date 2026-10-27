# N-06 — Habit Engagement Health & Abuse Monitoring Dashboard

## 1. Feature Context
NoorHeroes Admin Portal. Operational dashboard surfacing the integrity/fairness monitoring signals defined in PRD §10 DevOps requirements — the operational counterpart to B-02's reward-farming prevention and B-04's timezone-abuse-resistance guarantees.

## 2. Parent Feature
A.7 Habit Tracker — NextJS Admin

## 3. Sub-feature
N-06 Habit Engagement Health & Abuse Monitoring Dashboard

## 4. Objective
Build a `product_admin`-restricted dashboard displaying `habit_log` unique-constraint-violation rate, Streak Service impossible-transition alerts, `change_count_30d` threshold-breach rate, and core engagement/consistency metrics.

## 5. Business Requirements
- Surfaces integrity signals operators need without requiring direct database/log access.
- `habit_log` unique-constraint-violation rate spikes may indicate a client bug generating excessive duplicate-check-in attempts (PRD §10).
- Streak Service producing an "impossible" transition in production is a critical invariant-violation alert (cross-ref B-03).
- `change_count_30d` threshold-breach rate trending up may indicate a timezone-abuse pattern worth investigation (cross-ref B-04).
- Also displays product-health metrics: daily-active-check-in rate, streak-state distribution, Mercy Day/shield utilization trend, Family Garden participation rate (PRD §11.3).

## 6. Existing Architecture
`src/app/(dashboard)/habits/monitoring/page.tsx`, `src/features/habit-monitoring/{api,hooks,components}`. Consumes read-only aggregate/metrics endpoints — if no existing metrics/monitoring API pattern exists elsewhere in the Admin Portal, this sub-feature's backend dependency (B-02/B-03/B-04's alerting hooks) must expose read endpoints for these aggregates; flag this as a cross-reference requirement rather than assuming the data is already queryable.

## 7. Existing Code to Reuse
`DataTable`, chart components if the Admin Portal already has a charting library integrated elsewhere (reuse rather than introduce a new one), `useAdminSession`, `RequirePermission`.

## 8. Files to Create
- `src/app/(dashboard)/habits/monitoring/page.tsx`
- `src/features/habit-monitoring/api/habit-monitoring-repository.ts`
- `src/features/habit-monitoring/hooks/use-habit-integrity-signals.ts`
- `src/features/habit-monitoring/hooks/use-habit-engagement-metrics.ts`
- `src/features/habit-monitoring/components/IntegritySignalsPanel.tsx` (constraint-violation rate, impossible-transition alerts, timezone-breach rate)
- `src/features/habit-monitoring/components/EngagementMetricsPanel.tsx` (daily-active rate, streak-state distribution, Mercy Day utilization, Family Garden participation)

## 9. Files to Modify
- Admin Portal sidebar/navigation config — add "Habit Monitoring" entry, `product_admin`-only visibility

## 10. Backend Requirements
Requires read-only aggregate endpoints exposing: `habit_log` unique-constraint-violation rate trend, Streak Service impossible-transition alert log, `change_count_30d` threshold-breach rate trend, and the §11.3 engagement metrics — **flagged as a cross-reference gap**: confirm with the backend team whether B-02/B-03/B-04 expose these as queryable admin endpoints, or whether a new lightweight `/v1/admin/habits/monitoring` aggregation endpoint must be added; do not assume an endpoint shape that hasn't been confirmed (rule 30).

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- Integrity Signals Panel: trend charts/tables for constraint-violation rate, impossible-transition alert list, timezone-breach rate.
- Engagement Metrics Panel: daily-active-check-in rate, streak-state distribution (active/at_risk/broken/recovery breakdown), Mercy Day/shield utilization trend, Family Garden participation rate.
- Filtering by date range; pagination on any list-based signal (e.g., impossible-transition alert log).
- `RequirePermission` strictly `product_admin`-scoped.
- Loading, empty (no alerts = good news, framed positively), error states.

## 13. API Contract
**Re-audited, still genuinely unresolved at the exact-shape level, but with confirmed precedent for the approach:** B-02/B-03/B-04 currently only wire structured logging and alert hooks (log lines, periodic canary checks) — no admin-readable endpoint exists yet to back this dashboard. Two sibling blueprints establish the correct pattern to follow rather than waiting for B-02/03/04 to expose data directly: `E28_Admin_Auth_RBAC_Operations_Dashboard/Backend/08-operations-dashboard-aggregation-api.md`'s `GET /v1/admin/dashboard` composed-widget aggregation endpoint, and `A11_Rewards_System/Backend/14-admin-reconciliation-incident-log-api.md`'s `GET /v1/admin/rewards/reconciliation-incidents` read-only incident-viewer endpoint. **Resolution:** build a new dedicated `GET /v1/admin/habits/monitoring` aggregation endpoint (backend scope, not yet in this blueprint set) following the E28/A11 precedent, rather than assuming B-02/03/04 will expose raw data directly.

## 14. Database Requirements
N/A (frontend only; backend aggregation logic lives in B-02/B-03/B-04).

## 15. Validation
N/A beyond standard date-range filter validation.

## 16. Authentication
`useAdminSession`.

## 17. Authorization
`RequirePermission` strictly `product_admin`.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Monitoring API unavailable | Dashboard shows a clear "monitoring data temporarily unavailable" state, not a blank/broken page |
| Zero alerts in the impossible-transition log | Framed as a positive "no issues detected" state, not an empty-table dead-end |

## 19. Offline First
Not applicable.

## 20. Local Data
Not applicable.

## 21. Localization
**Confirmed:** Admin Portal supports multi-locale via `useTranslation()`/`updateLanguagePreference('hi'|'ar'|'en')` (`NEXT-JS-INSTRUCTIONS.md`) — dashboard labels/metric names must use `useTranslation()`, not hardcoded English.

## 22. RTL
**Confirmed:** drive layout via `useLocalization()`'s RTL status; charts/tables must mirror correctly.

## 23. Analytics
Not applicable (this page *is* the analytics/monitoring surface for operators).

## 24. Performance
Dashboard queries should be scoped to reasonable date ranges by default (e.g., last 30 days) to avoid expensive unbounded aggregation queries.

## 25. Security
`product_admin`-only access reflects the sensitivity of abuse-pattern data; client-side guard is defense-in-depth, backend must independently enforce this scope on any new monitoring endpoint.

## 26. Library Requirements
Next.js App Router, React Query, existing Admin Portal charting library (if any) or a minimal table-based fallback if no charting library is yet integrated.

## 27. Testing
Component tests for both panels; hook tests for metrics fetching; RBAC-guard test; empty/positive-state rendering test.

## 28. Documentation
Document the exact metrics displayed and their source (B-02/B-03/B-04) for future maintainers, plus the resolution of the §10/§13 API-contract cross-reference gap once confirmed.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Backend Monitoring Endpoint Following E28/A11 Precedent**
- Objective: Resolve the flagged API-contract gap (§13) by specifying a new `GET /v1/admin/habits/monitoring` endpoint modeled on `E28_Admin_Auth_RBAC_Operations_Dashboard/Backend/08-operations-dashboard-aggregation-api.md`'s composed-widget pattern and `A11_Rewards_System/Backend/14-admin-reconciliation-incident-log-api.md`'s read-only incident-viewer pattern.
- Action: Author the backend endpoint spec (this becomes a new B-14 sub-feature of A7 if formalized) aggregating: `habit_log` unique-constraint-violation rate (B-02), Streak Service impossible-transition alerts (B-03), `change_count_30d` threshold-breach rate (B-04), and the §11.3 engagement metrics.
- Definition of Done: endpoint contract specified and documented, following the confirmed E28/A11 precedent rather than an invented shape.

**Task 02 — Scaffold `habit-monitoring` Feature Module**
- Files to Create: `types.ts`, `api/habit-monitoring-repository.ts`
- Definition of Done: module compiles with typed API client matching the confirmed contract.

**Task 03 — Implement Metrics Hooks**
- Files to Create: `hooks/use-habit-integrity-signals.ts`, `use-habit-engagement-metrics.ts`
- Definition of Done: hooks correctly fetch and shape both signal categories.

**Task 04 — Build Integrity Signals & Engagement Metrics Panels**
- Files to Create: `IntegritySignalsPanel.tsx`, `EngagementMetricsPanel.tsx`
- Implementation Details: trend visualization, positive-framed empty states.
- Tests: component tests for both panels.
- Definition of Done: panels render correctly with real and empty data.

**Task 05 — Wire Page Route with Strict RBAC Guard**
- Files to Create: `page.tsx`
- Files to Modify: sidebar/navigation config.
- Definition of Done: route only accessible to `product_admin`.

**Task 06 — Final Code Review**
- Expected Result: PR merge-ready.

## 30. Definition of Done
Habit Engagement Health & Abuse Monitoring dashboard live, `product_admin`-restricted, correctly surfacing both integrity signals and engagement metrics against a confirmed backend contract.

## 31. Final Verification Checklist
- [ ] Backend monitoring endpoint contract confirmed (not assumed)
- [ ] Integrity Signals Panel displays constraint-violation rate, impossible-transition alerts, timezone-breach rate
- [ ] Engagement Metrics Panel displays daily-active rate, streak-state distribution, Mercy Day utilization, Family Garden participation
- [ ] Dashboard restricted to `product_admin` role
- [ ] Empty/zero-alert states framed positively
- [ ] Date-range filtering implemented with sensible default scope
- [ ] Tests passing
