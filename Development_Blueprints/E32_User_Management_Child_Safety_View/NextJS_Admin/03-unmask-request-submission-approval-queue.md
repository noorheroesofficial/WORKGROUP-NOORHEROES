# N-03 — Unmask Request Submission & Approval Queue

## 1. Feature Context
The UI half of B-03's maker-checker gate: a submission form carrying a required justification and explicit scope, and an approval queue whose Approve action is disabled — with a clear explanation, never silently — the instant the current admin matches the request's own requester.

## 2. Parent Feature
E.32 — User Management & Child Safety View

## 3. Sub-feature
2.3 Unmask Request Submission & Approval Queue (ID: **N-03**)

## 4. Objective
Build the Unmask Request Submission form and the Approval Queue/Detail screens against B-03, deriving the self-approval UI block exclusively from the server's `requested_by` field compared to the current admin identity — the same pattern E.29's N-04 established for scholar review.

## 5. Business Requirements
- Submission requires justification (min length) and explicit scope (`parent_id` or `child_id`), pre-fillable from N-01/N-02's entry points.
- Approval queue lists pending requests; detail view shows justification, scope, requester.
- Approve/Reject actions are disabled with an explanatory message when `requested_by === current admin id` (mirrors N-04's `isSelfEdited` pattern from E.29, applied here as `isSelfRequested`).
- "Nothing pending" empty state when the queue is clear.

## 6. Existing Architecture
`src/features/unmask-workflow/` module, following the same segregation-of-duties UI pattern established in E.29's `src/features/scholar-review/components/segregation-of-duties-block.tsx`.

## 7. Existing Code to Reuse
- `src/shared/components/require-permission.tsx::RequirePermission`
- `src/shared/hooks/use-pagination-state.ts::usePaginationState`
- `src/shared/components/confirmation-dialog.tsx::ConfirmationDialog`
- E.29 N-04's `SegregationOfDutiesBlock` pattern (reused conceptually — same derivation-from-server-field approach, adapted field name)

## 8. Files to Create
- `src/app/(dashboard)/unmask-requests/new/page.tsx`
- `src/app/(dashboard)/unmask-requests/page.tsx` — queue
- `src/app/(dashboard)/unmask-requests/[id]/page.tsx` — detail
- `src/features/unmask-workflow/api/unmask-request-repository.ts`
- `src/features/unmask-workflow/hooks/use-unmask-queue.ts`, `use-unmask-detail.ts`, `use-submit-unmask-request.ts`, `use-submit-unmask-decision.ts`
- `src/features/unmask-workflow/components/unmask-request-form.tsx`
- `src/features/unmask-workflow/components/self-request-block.tsx` — the disabled-with-explanation state
- `src/features/unmask-workflow/components/decision-action-bar.tsx` — Approve/Reject, self-request-aware
- `src/features/unmask-workflow/types/unmask-request.ts` — Zod schema

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `UNMASK_REQUESTS.*` endpoints
- `src/shared/components/dashboard-shell.tsx` — nav item under "Users" group

## 10. NextJS Requirements
- `DecisionActionBar`: computes `isSelfRequested = requestDetail.requested_by === adminAuthContext.currentAdmin.id` — the **only** source of the block decision, never a separate client heuristic; when true, renders `SelfRequestBlock` (disabled buttons + explanatory message) instead of active Approve/Reject buttons.
- `UnmaskRequestForm`: `justification` textarea with min-length validation, `scope` pre-filled (and locked) when navigated from N-01/N-02's entry point.
- Queue empty state: "Nothing pending."

## 11. Required API
**Admin API** — B-03: `POST /v1/admin/unmask-requests`, `GET /v1/admin/unmask-requests`, `GET /v1/admin/unmask-requests/{id}`, `PATCH /v1/admin/unmask-requests/{id}/approve`, `PATCH /v1/admin/unmask-requests/{id}/reject`.

## 12. Authentication / Authorization
`useAdminSession()` base auth; `RequirePermission permission="support"` for submission and viewing; approve/reject also gated to `support`+ (any operator other than the requester, per B-03's role-symmetric maker-checker).

## 13. Loading / Empty / Error States
Submission validation errors (justification too short, missing scope); queue loading skeleton, "Nothing pending" empty state; `409 SELF_APPROVAL_NOT_ALLOWED` surfaced as the `SelfRequestBlock` state, not a generic error toast.

## 14. Responsive UI / Accessibility
Self-request block message is programmatically associated with the disabled buttons (`aria-describedby`), not conveyed by disabled-styling alone.

## 15. Localization / RTL
Standard `useTranslation()`/`useFormatters()`.

## 16. Security
The `isSelfRequested` UI hint is the load-bearing defense-in-depth layer alongside B-03's dual-layer backend enforcement — tested explicitly with a fixture where `requested_by` matches the current admin, mirroring E.29 N-04's mandatory test pattern exactly.

## 17. Testing
Unit: `isSelfRequested` derivation logic. UI: **mandatory** — a fixture request where `requested_by` matches the current admin renders the Approve/Reject bar in a disabled state with an explanatory message instead of active buttons. Integration: full submit → queue-shows-pending → different-admin-approves → grant-created flow; full submit → same-admin-attempts-approve → blocked flow.

## 18. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schema & Add API Endpoints**
Objective: `unmask-request.ts` schema. Files: `types/unmask-request.ts`, `api-endpoints.ts`. Tests: schema validation. Definition of Done: schema used by Task 03.

**Task 02 — Implement `UnmaskRequestRepositoryImpl`**
Objective: Repository for B-03's five endpoints. Tests: mocked-fetch tests. Dependencies: Task 01. Definition of Done: tests pass.

**Task 03 — Implement `UnmaskRequestForm`**
Objective: Justification + scope form, pre-fill support from entry points. Dependencies: Task 02. Tests: min-length validation test. Definition of Done: test passes.

**Task 04 — Implement `DecisionActionBar` with Mandatory Self-Request Hint**
Objective: `isSelfRequested` derivation exclusively from server data + `AdminAuthContext`. Dependencies: Task 02. Tests: **mandatory** — self-requested-fixture disables action bar test. Definition of Done: test passes.

**Task 05 — Implement `SelfRequestBlock`**
Objective: Clear, explanatory blocked-state message (never a bare disabled button). Dependencies: Task 04. Tests: message-content test. Definition of Done: test passes.

**Task 06 — Implement the Submission, Queue, and Detail Pages**
Objective: Compose all components with loading/empty/error states. Dependencies: Tasks 03–05. Tests: full-page smoke tests. Definition of Done: tests pass.

**Task 07 — Add Full Test Suite**
Objective: Complete coverage per §17, including the mandatory self-request UI test. Definition of Done: all green in CI.

**Task 08 — Final Code Review**
Objective: Confirm the self-request hint has zero alternate derivation path outside the server-`requested_by`-vs-`AdminAuthContext` comparison, and that it mirrors E.29 N-04's pattern precisely. Definition of Done: checklist in §19 checked.

## 19. Final Verification Checklist
- [ ] Self-request UI hint derives exclusively from server `requested_by` vs. current admin identity — mandatory test passing
- [ ] Blocked state shows a clear explanation, never a bare disabled button
- [ ] Justification enforces a minimum length
- [ ] Queue empty state matches "Nothing pending" copy
- [ ] Approve/Reject wire correctly to B-03

## 20. Definition of Done
Operators have a full submission-to-approval workspace whose UI-level self-approval guard is provably server-sourced, never a client-side guess — the primary human interface to E.32's most safety-critical backend guarantee (B-03).
