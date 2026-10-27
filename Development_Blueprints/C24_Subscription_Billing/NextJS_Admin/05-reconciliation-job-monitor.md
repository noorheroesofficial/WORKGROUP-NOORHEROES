# N-05 — Reconciliation Job Monitor

## 1. Feature Context
A read-only table of B-04's Reconciliation Job run history and any drift corrections made — the platform's billing-integrity health signal, mirroring the reconciliation-job-monitoring pattern established elsewhere (B.15/A.11). **Note:** full detail owned by E.33; this blueprint implements C.24's own ownership sketch (§8).

## 2. Parent Feature
Feature C.24 — Subscription & Billing

## 3. Sub-feature
3.5 Reconciliation Job Monitor (ID: **N-05**)

## 4. Objective
Build a `product_admin`/`trust_safety`-restricted, read-only table of B-04's reconciliation job run history and drift corrections (masked family identifier, before/after state, timestamp).

## 5. Business Requirements
- §8 Admin Requirements: Reconciliation Job Monitor — read-only, `product_admin`/`trust_safety` role, visibility into run history and drift corrections.
- §1.4 Success Metrics: webhook reconciliation job success rate = 100% (hard target) — this dashboard is the primary visibility tool for that metric.
- §10 DevOps: "Alert on drift-correction volume spiking unexpectedly" — this dashboard is where that signal becomes visually inspectable, not just an alert.

## 6. Existing Architecture
`src/features/commerce/` (extends N-01–N-04's feature folder), reusing the reconciliation-job-monitor UI pattern already established for B.15/A.11 if one exists (confirm and reuse rather than building a divergent pattern — Do Not Guess if not found, build fresh following the existing Admin Portal table conventions).

## 7. Existing Code to Reuse
- `src/shared/components/data-table.tsx` with sorting/pagination.
- Existing job-run-history UI pattern from B.15/A.11 if present.

## 8. Files to Create
- `src/features/commerce/api/reconciliation-monitor-repository.ts`
- `src/features/commerce/hooks/use-reconciliation-runs.ts`
- `src/features/commerce/components/reconciliation-job-monitor-table.tsx`
- `src/app/(dashboard)/commerce/reconciliation/page.tsx`

## 9. Files to Modify
- Sidebar navigation config — add "Reconciliation Monitor" under Commerce, `product_admin`/`trust_safety`-gated

## 10. NextJS Requirements
- `useReconciliationRuns(pagination)`: paginated list of job runs — run timestamp, subscriptions checked, corrections made, success/failure status.
- Drill-down per run showing individual corrections: masked family identifier, before/after state, corrected_at timestamp (sourced from B-04's audit records).
- Visual flag/highlight on runs with unusually high correction volume (supporting the "spike investigation" DevOps alert use case) or on any failed/skipped run.

## 11. Required API
Reconciliation job run-history/correction-log read endpoint — exact contract owned by E.33's backend specification, sourced from B-04's audit records. **Admin API.**

## 12. Validation
Pagination params bounded to reasonable page sizes; no client-side filtering that could hide a failed run by accident (failed runs always visible by default, not filtered out).

## 13. Authentication
Existing Admin Portal auth context (Bearer session).

## 14. Authorization
`product_admin`/`trust_safety` role, read-only, enforced via `RequirePermission` and server-side check.

## 15. Error Handling
Empty state for "no reconciliation runs yet" (unlikely in production but valid for a fresh environment); API failure shows a retryable error state.

## 16. Loading States
Table skeleton while run history loads; drill-down panel skeleton while correction detail loads.

## 17. Responsive UI
Table collapses to a card layout on narrow viewports, consistent with N-01/N-02's existing table responsive pattern.

## 18. Accessibility
Table semantics for run history and correction detail; failed/flagged runs distinguishable by more than color alone (icon + text label).

## 19. Localization
Admin Portal typically EN-only for internal tooling (confirm against `NEXT-JS-INSTRUCTIONS.md`).

## 20. Testing
- Unit: `useReconciliationRuns` hook success/empty/error branches, pagination behavior.
- Component: failed/high-correction-volume runs visually flagged correctly.
- Component: masked family identifier displayed, not full PII.
- RBAC: non-`product_admin`/`trust_safety` users blocked from the route.

## 21. AI Coding Agent Implementation Steps

**Task 01 — Implement `ReconciliationMonitorRepositoryImpl`**
Objective: typed paginated run-history API client. Files to Create: `reconciliation-monitor-repository.ts`. Dependencies: backend endpoint live (E.33, sourced from B-04).

**Task 02 — Implement `useReconciliationRuns` Hook**
Objective: paginated query hook. Files to Create: `use-reconciliation-runs.ts`. Dependencies: Task 01.

**Task 03 — Implement `ReconciliationJobMonitorTable` Component**
Objective: run-history table + correction drill-down, with failed/spike flagging. Files to Create: `reconciliation-job-monitor-table.tsx`. Dependencies: Task 02.

**Task 04 — Wire Page Route & Navigation**
Objective: `/commerce/reconciliation` page, RBAC-gated nav entry. Files to Create/Modify: page file, sidebar nav config. Dependencies: Task 03.

**Task 05 — Add Full Test Suite**
Objective: coverage per §20. Dependencies: Tasks 01–04.

## 22. Definition of Done
`product_admin`/`trust_safety` roles can view a read-only, paginated reconciliation job run history with drill-down into individual drift corrections, with failed runs and correction-volume spikes visually flagged.

## 23. Final Verification Checklist
- [ ] Run history and per-correction drill-down both render correctly from B-04's audit data
- [ ] Failed runs always visible by default, never accidentally filtered out
- [ ] High-correction-volume runs visually flagged
- [ ] Family identifiers displayed masked, not full PII
- [ ] `product_admin`/`trust_safety` role enforced client- and server-side
