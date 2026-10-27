# N-04 — Risk & Fraud Review Queue

## 1. Feature Context
Trust & Safety's action queue: paginated flagged registration attempts (VOIP numbers, high-velocity device fingerprints) with an Approve/Block decision action, every decision immutably audit-logged.

## 2. Parent Feature
Feature A.1 — Splash, Language Selection, Authentication & Onboarding

## 3. Sub-feature
3.4 Risk & Fraud Review Queue (ID: **N-04**)

## 4. Objective
Build a paginated `DataTable` of flagged attempts against B-08's risk-queue endpoint, with an Approve/Block `ConfirmationDialog` action wired to the decision endpoint, gated behind `trust_safety` permission.

## 5. Business Requirements
- Risk/Fraud Review Queue: flagged registration attempts (VOIP numbers, high-velocity device fingerprints, device fingerprint reuse count) surfaced for manual review/allow/block; every decision audit-logged with the reviewing admin's ID.
- CRUD permissions: Risk Queue = Read + Update (decision field) only — no delete.

## 6. Existing Architecture
`src/features/risk-review/` module; `DataTable` for the paginated list; `ConfirmationDialog` for the decision action, following the exact `DeleteFamilyButton` structural pattern from the architecture doc (state → dialog → mutation), adapted for a non-destructive but still consequential action.

## 7. Existing Code to Reuse
- `src/shared/components/data-table.tsx::DataTable`
- `src/shared/components/confirmation-dialog.tsx::ConfirmationDialog`
- `src/shared/hooks/use-pagination-state.ts::usePaginationState`
- `src/shared/components/require-permission.tsx::RequirePermission`
- `src/shared/components/status-badge.tsx::StatusBadge` (for risk-signal badges: VOIP flag, velocity flag)

## 8. Files to Create
- `src/app/(dashboard)/risk-review/page.tsx`
- `src/features/risk-review/api/risk-review-repository.ts` — `RiskReviewRepositoryImpl.list(filters)`, `.decide(attemptId, decision)`
- `src/features/risk-review/hooks/use-risk-queue.ts`, `use-risk-decision.ts`
- `src/features/risk-review/components/risk-decision-dialog.tsx`
- `src/features/risk-review/components/risk-signal-badges.tsx`
- `src/features/risk-review/types/risk-flag.ts` — Zod schema

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `RISK_REVIEW.QUEUE`, `RISK_REVIEW.DECISION`
- `src/shared/components/dashboard-shell.tsx` — nav item gated by `trust_safety`

## 10. NextJS Requirements
- `useRiskQueue(filters)`: paginated React Query hook via `usePaginationState`, filters for status (pending/decided).
- `useRiskDecision()`: mutation hook calling `POST /admin/v1/risk/{attempt_id}/decision`; on success, invalidates the queue query so the decided item disappears/updates without a full page reload.
- `RiskDecisionDialog`: `ConfirmationDialog`-based Approve/Block action with a required reason field for Block (optional for Approve, per B-08's schema); `isDanger` styling for Block specifically.
- `RiskSignalBadges`: renders VOIP flag / velocity flag / device-fingerprint-reuse-count as `StatusBadge`-style indicators in the table row, not buried in an expandable detail only.
- Table columns: risk score, signals (badges), status, decided-by (if applicable), action button.

## 11. Required API
- `GET /admin/v1/risk/queue` (B-08) — Auth: `trust_safety`
- `POST /admin/v1/risk/{attempt_id}/decision` (B-08) — Auth: `trust_safety`

## 12. Authentication / Authorization
`RequirePermission permission="trust_safety"` on the page; the decision mutation itself relies on the backend's own scope check as the actual authority (defense in depth — UI hiding is not the security boundary).

## 13. Loading / Empty / Error States
Loading skeleton via `DataTable`'s built-in loading prop; empty state for zero pending flags ("no items need review" — a positive, not alarming, empty state); error state with retry.

## 14. Responsive UI / Accessibility
Table responsive per existing `DataTable` behavior; decision dialog keyboard-accessible, focus-trapped, per existing `ConfirmationDialog` conventions.

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()` for all labels, risk-score formatting, and timestamps.

## 16. Security
Decision action must never be reachable without going through the confirmation dialog (no direct one-click Approve/Block on the table row) — this is a consequential, audit-logged action and deserves the same friction pattern as `DeleteFamilyButton`.

## 17. Testing
Unit: pagination-to-query-param mapping; decision-requires-dialog-confirmation assertion (no direct-row-action bypass); Block-requires-reason validation; query-invalidation-on-decision-success test.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schema & Add API Endpoints**
Objective: Contracts for both list and decision endpoints. Files to Create/Modify: `types/risk-flag.ts`, `api-endpoints.ts`. Tests: schema validation for both request/response shapes. Definition of Done: typed, validated contracts for both operations.

**Task 02 — Implement `RiskReviewRepositoryImpl`**
Objective: `list()` and `decide()` methods. Follow: existing repository conventions (list mirrors `FamilyResourceClient.list()`, decide mirrors `FamilyResourceClient.suspend()`'s custom-action pattern). Tests: mocked-fetch tests for both methods. Dependencies: Task 01. Definition of Done: both methods typed and tested.

**Task 03 — Implement `useRiskQueue` and `useRiskDecision` Hooks**
Objective: Paginated list query + decision mutation with query invalidation on success. Follow: `useFamilyList()`/`useSuspendFamily()`-equivalent patterns. Tests: invalidation-on-success test. Dependencies: Task 02. Definition of Done: queue list correctly refreshes after a decision without a manual page reload.

**Task 04 — Implement `RiskSignalBadges` and Table Columns**
Objective: Visual risk-signal indicators inline in the table. Follow: `StatusBadge`. Tests: covered by Task 06. Dependencies: Task 03. Definition of Done: signals visible without expanding a detail row.

**Task 05 — Implement `RiskDecisionDialog`**
Objective: Approve/Block confirmation with required-reason-for-Block validation. Follow: `ConfirmationDialog`, `isDanger` styling for Block. Tests: reason-required-for-block validation test; no-bypass-of-dialog test. Dependencies: Task 03. Definition of Done: no code path allows a decision without passing through this dialog.

**Task 06 — Implement the Page**
Objective: Compose `RequirePermission` + `DataTable` + pagination + `RiskDecisionDialog`. Files to Create: `page.tsx`. Dependencies: Tasks 04–05. Definition of Done: full page smoke test against a mocked API.

**Task 07 — Add Full Test Suite**
Objective: Complete coverage per §17. Definition of Done: all green in CI.

**Task 08 — Final Code Review**
Objective: Confirm no direct-row decision bypass exists, confirm `trust_safety` gating, confirm query invalidation correctness. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] Decision action always requires passing through `RiskDecisionDialog` — no direct-row shortcut
- [ ] Block requires a reason; Approve does not
- [ ] Queue list correctly refreshes/invalidates after a successful decision
- [ ] Risk signals visible inline in the table, not hidden behind an extra click
- [ ] Page gated behind `trust_safety` permission
- [ ] All labels/timestamps localized and locale-formatted

## 20. Definition of Done
The Risk & Fraud Review Queue is live, reads/writes against B-08, enforces the confirmation-dialog friction pattern for every decision, and correctly reflects decision outcomes without a manual refresh.
