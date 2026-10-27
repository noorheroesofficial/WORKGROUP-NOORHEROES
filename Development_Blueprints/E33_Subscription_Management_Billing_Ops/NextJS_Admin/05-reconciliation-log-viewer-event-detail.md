# N-05 — Reconciliation Log Viewer & Event Detail

## 1. Feature Context
The operational-monitoring and dispute-investigation surface for drift correction, rendering each event's before/after state with the same diff-view clarity established by E.29's content-review diff pattern.

## 2. Parent Feature
E.33 — Subscription Management & Billing Ops

## 3. Sub-feature
2.5 Reconciliation Log Viewer & Event Detail (ID: **N-05**)

## 4. Objective
Build the Reconciliation Log Viewer and Reconciliation Event Detail screens against B-05, rendering a clear before/after comparison for each drift-correction entry.

## 5. Business Requirements
- §1.18 screens 10–11: Reconciliation Log Viewer, Reconciliation Event Detail (before/after state).
- FR-9: every drift-correction event shown with before/after entitlement state, affected subscription, timestamp.
- §2.1: Reconciliation Drift Visual Cue uses a clear before/after comparison display, similar to E.29's diff-view pattern.
- §7 Frontend AI prompt item 4: render a clear before/after comparison for each drift-correction entry, tested with fixture before/after values.
- §1.12: "No drift detected — all entitlements in sync" empty state.

## 6. Existing Architecture
`src/features/reconciliation-log/` module.

## 7. Existing Code to Reuse
- `src/shared/components/data-table.tsx::DataTable`
- E.29 N-04's `VersionDiffPanel` diff-rendering pattern (conceptually reused — before/after comparison chip styling, not the component itself given the different domain: entitlement state strings, not content text)
- `src/shared/hooks/use-pagination-state.ts::usePaginationState`

## 8. Files to Create
- `src/app/(dashboard)/commerce/reconciliation/page.tsx`
- `src/app/(dashboard)/commerce/reconciliation/[id]/page.tsx`
- `src/features/reconciliation-log/api/reconciliation-log-repository.ts`
- `src/features/reconciliation-log/hooks/use-reconciliation-log.ts`, `use-reconciliation-event-detail.ts`
- `src/features/reconciliation-log/components/date-range-filter.tsx`
- `src/features/reconciliation-log/components/before-after-comparison-chip.tsx`
- `src/features/reconciliation-log/types/reconciliation.ts` — Zod schema

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `RECONCILIATION.*` endpoints
- `src/shared/components/dashboard-shell.tsx` — nav item under "Commerce" group

## 10. NextJS Requirements
- `BeforeAfterComparisonChip`: struck-through "before" state, arrow, highlighted "after" state — per the PRD's own mockup description ("past_due" struck through, arrow, "active_paid" highlighted in green).
- Log list filterable by `date_from`/`date_to`; expandable rows reveal the comparison chip inline (per the mockup's "one row expanded" pattern).

## 11. Required API
**Admin API** — B-05: `GET /v1/admin/reconciliation-log?date_from=&date_to=`.

## 12. Authentication / Authorization
`useAdminSession()` base auth; `RequirePermission permission="billing_ops"`.

## 13. Loading / Empty / Error States
Log loading skeleton; **"No drift detected — all entitlements in sync"** calm empty state (exact PRD framing, §1.12) for periods with zero drift; invalid date-range validation error.

## 14. Responsive UI / Accessibility
Before/after chip conveys the change via text labels ("Before: past_due, After: active_paid") in addition to color/strikethrough styling.

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()`.

## 16. Security
Strictly read-only screen — no mutating action exists anywhere in this module, consistent with B-05's observational-only backend guarantee.

## 17. Testing
Unit: date-range filter validation. UI: **mandatory** — before/after comparison renders correctly using fixture state values (e.g., `past_due` → `active_paid`), per §7 item 4. Integration: full log-list → expand-row → comparison-chip-displays flow; empty-period shows the exact "No drift detected" copy.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schema & Add API Endpoints**
Objective: `reconciliation.ts` schema. Files: `types/reconciliation.ts`, `api-endpoints.ts`. Tests: schema validation. Definition of Done: schema used by Task 03.

**Task 02 — Implement `ReconciliationLogRepositoryImpl`**
Objective: Repository for B-05's log endpoint. Tests: mocked-fetch tests. Dependencies: Task 01. Definition of Done: tests pass.

**Task 03 — Implement `BeforeAfterComparisonChip`**
Objective: Struck-through/arrow/highlighted comparison display. Dependencies: Task 02. Tests: **mandatory** — fixture-before/after-values-render-correctly test. Definition of Done: test passes.

**Task 04 — Implement `DateRangeFilter` and the Log List**
Objective: Filterable, expandable-row list. Dependencies: Task 03. Tests: filter tests. Definition of Done: tests pass.

**Task 05 — Implement the Log Viewer and Event Detail Pages**
Objective: Compose components with loading/empty/error states, including the exact "No drift detected" copy. Dependencies: Task 04. Tests: full-page smoke tests. Definition of Done: tests pass.

**Task 06 — Add Full Test Suite**
Objective: Complete coverage per §17, including the mandatory fixture-rendering test. Definition of Done: all green in CI.

**Task 07 — Final Code Review**
Objective: Confirm the comparison chip conveys change via text, not color/strikethrough alone. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] Before/after comparison renders correctly for fixture drift events — mandatory test passing
- [ ] Empty state uses the exact "No drift detected — all entitlements in sync" copy
- [ ] Comparison conveyed via text labels, not color/strikethrough alone
- [ ] `billing_ops` scope enforced, strictly read-only

## 20. Definition of Done
Billing Ops can review every reconciliation drift-correction event with an immediately legible before/after comparison, supporting both routine monitoring and dispute investigation.
