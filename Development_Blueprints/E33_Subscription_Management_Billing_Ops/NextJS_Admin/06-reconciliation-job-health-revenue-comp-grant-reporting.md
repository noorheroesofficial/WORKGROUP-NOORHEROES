# N-06 — Reconciliation Job Health Monitor & Revenue vs. Comp-Grant Reporting

## 1. Feature Context
The final two screens of this module: an operational view of the reconciliation job's own reliability, and a Finance-facing report whose entire purpose is keeping comp grants visibly and permanently separate from real revenue.

## 2. Parent Feature
E.33 — Subscription Management & Billing Ops

## 3. Sub-feature
2.6 Reconciliation Job Health Monitor & Revenue vs. Comp-Grant Reporting (ID: **N-06**)

## 4. Objective
Build the Reconciliation Job Health Monitor and the Revenue vs. Comp-Grant Reporting View against B-05, with comp-grant figures always excluded from — and visually distinct from — real-revenue figures.

## 5. Business Requirements
- §1.18 screen 12: Reconciliation Job Health Monitor (run history, failures), cross-ref E.28's job-failure widget.
- §1.18 screen 13: Revenue vs. Comp-Grant Reporting View (Finance-facing, read-only).
- §11.5: comp grants always cleanly excluded from real-revenue reporting, never inflating MRR/ARR figures.
- Edge Case 3: a missed job run is an alertable incident; the health monitor must reflect this honestly, never silently.

## 6. Existing Architecture
`src/features/reconciliation-job-health/` and `src/features/revenue-reporting/` modules.

## 7. Existing Code to Reuse
- E.28's existing job-failure monitoring widget (reused/cross-referenced, not reimplemented)
- `src/shared/components/data-table.tsx::DataTable`

## 8. Files to Create
- `src/app/(dashboard)/commerce/reconciliation/health/page.tsx`
- `src/app/(dashboard)/commerce/revenue-report/page.tsx`
- `src/features/reconciliation-job-health/api/job-health-repository.ts`
- `src/features/reconciliation-job-health/hooks/use-job-health.ts`
- `src/features/reconciliation-job-health/components/job-run-history-table.tsx`
- `src/features/revenue-reporting/api/revenue-report-repository.ts`
- `src/features/revenue-reporting/hooks/use-revenue-report.ts`
- `src/features/revenue-reporting/components/revenue-vs-comp-grant-chart.tsx` — comp-grant figures rendered in a visually separate series/section, never summed into the revenue total

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `RECONCILIATION_HEALTH.*`, `REVENUE_REPORT.*` endpoints
- `src/shared/components/dashboard-shell.tsx` — nav items under "Commerce" group

## 10. NextJS Requirements
- `JobRunHistoryTable`: last-successful-run timestamp prominently displayed, failure count highlighted; a missed/failed run is never rendered as if it were a successful "no drift" outcome — the UI distinguishes "job ran, found nothing" from "job did not run."
- `RevenueVsCompGrantChart`: two visually distinct series/sections — real revenue and comp-grant value — with comp-grant figures explicitly labeled as non-revenue everywhere they appear, and the total revenue figure structurally computed excluding comp-grant values (client-side aggregation, if any, never sums the two series together).

## 11. Required API
**Admin API** — B-05: `GET /v1/admin/reconciliation-job/health`. A revenue-reporting read endpoint (owned within B-02/B-04's existing data, aggregated server-side or client-side from subscription-search and comp-grant data — confirmed as reusing existing read paths, no new backend sub-feature required for this reporting view per PRD §8's "no further meta-layer" statement).

## 12. Authentication / Authorization
`useAdminSession()` base auth; `RequirePermission permission="billing_ops"` for job health; Finance-facing revenue report may extend to a `finance` role if distinct from `billing_ops` in E.28's registry (confirm against live role registry; default to `billing_ops`/`super_admin` if no separate `finance` role exists).

## 13. Loading / Empty / Error States
Job health loading skeleton; "No runs in this period" state distinct from an actual failure state; revenue report loading skeleton.

## 14. Responsive UI / Accessibility
Job-failure state uses both an icon and explicit text ("Job did not run as scheduled"), not color alone; revenue vs. comp-grant chart legend clearly text-labeled, not color-coded alone.

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()`.

## 16. Security
Comp-grant figures never being summed into the real-revenue total is this screen's defining guarantee — mandatory test confirms the displayed total-revenue figure is computed exclusively from real billing-event-derived data, with a fixture comp-grant value present but confirmed absent from that total.

## 17. Testing
Unit: revenue-total computation excludes comp-grant values. UI: **mandatory** — fixture data with both real revenue and comp-grant value renders the total as real-revenue-only, with comp-grant value shown separately and clearly labeled; job health correctly distinguishes "no drift found" from "job did not run." Integration: full health-check display flow; full revenue-report rendering flow with mixed fixture data.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schemas & Add API Endpoints**
Objective: `job-health.ts`, `revenue-report.ts` schemas. Files: `types/*.ts`, `api-endpoints.ts`. Tests: schema validation. Definition of Done: schemas used by Tasks 03/05.

**Task 02 — Implement `JobHealthRepositoryImpl` and `RevenueReportRepositoryImpl`**
Objective: Repositories for both read endpoints. Tests: mocked-fetch tests. Dependencies: Task 01. Definition of Done: tests pass.

**Task 03 — Implement `JobRunHistoryTable`**
Objective: Distinguishes missed-run from no-drift-found. Dependencies: Task 02. Tests: missed-run-vs-no-drift distinction test. Definition of Done: test passes.

**Task 04 — Implement `RevenueVsCompGrantChart` with Excluded-Total Guarantee**
Objective: Two-series display, comp-grant never summed into revenue total. Dependencies: Task 02. Tests: **mandatory** — total-excludes-comp-grant test with mixed fixture data. Definition of Done: test passes.

**Task 05 — Implement the Job Health and Revenue Report Pages**
Objective: Compose components with loading/empty/error states. Dependencies: Tasks 03–04. Tests: full-page smoke tests. Definition of Done: tests pass.

**Task 06 — Add Full Test Suite**
Objective: Complete coverage per §17, both mandatory tests included. Definition of Done: all green in CI.

**Task 07 — Final Code Review**
Objective: Confirm zero code path sums comp-grant value into the displayed revenue total, in this component or any shared aggregation utility it depends on. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] Revenue total structurally excludes comp-grant value — mandatory test passing
- [ ] Comp-grant figures visually and textually distinct wherever shown
- [ ] Job health distinguishes "no drift found" from "job did not run" — mandatory test passing
- [ ] `billing_ops` scope enforced

## 20. Definition of Done
Finance and Billing Ops have honest, clearly-separated visibility into reconciliation-job reliability and revenue-vs-comp-grant figures, with zero risk of comp grants inflating reported revenue.
