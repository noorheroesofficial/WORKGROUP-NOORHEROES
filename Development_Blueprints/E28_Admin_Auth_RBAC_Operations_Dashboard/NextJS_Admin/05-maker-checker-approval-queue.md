# N-05 — Maker-Checker Approval Queue & Proposal Detail

## 1. Feature Context
Part of E.28. Screens #15–16 in PRD §1.18. Gives a designated approver a complete view of pending high-risk changes; disables/hides the approve action when the current admin is the proposer (PRD §7 Frontend AI prompt item 4).

## 2. Parent Feature
E.28 — Admin Portal: Authentication, RBAC & Operations Dashboard

## 3. Sub-feature
N-05 — Maker-Checker Approval Queue & Proposal Detail

## 4. Objective
Build the Approval Queue and Proposal Detail screens with proposer/approver identities always visibly distinct, and the approval action rendered unavailable whenever the current admin's identity matches the proposal's proposer — a UX-layer reinforcement of B-04's server-side self-approval rejection.

## 5. Business Requirements
- FR-3(b): no admin can be the sole approver of a change to their own role/proposal.
- Edge Case 1: cross-session self-approval rejected by identity, not session.
- Edge Case 2: redundant approval on an already-resolved proposal is a no-op, not an error.
- §1.12: zero pending approvals → "Nothing pending" empty state.
- §2.1/§2.2: clearly state-labeled workflow (Pending → Approved/Rejected); proposer/approver identities visibly distinct; full diff/comparison in Proposal Detail.

## 6. Existing Architecture
No existing approval-queue UI pattern in the codebase — new feature module, built from `DataTable`, `ConfirmationDialog`, `StatusBadge` primitives already present.

## 7. Existing Code to Reuse
| Component | Location | Reuse For |
|---|---|---|
| `DataTable` | `src/shared/components/` | Approval Queue list |
| `StatusBadge` | `src/shared/components/` | Pending/Approved/Rejected labels |
| `ConfirmationDialog` | `src/shared/components/` | Approve/Reject confirmation |
| `useAdminSession()` | `src/features/auth/hooks/` | Current admin identity for the approve-hiding check |
| `EmptyState` | `src/shared/components/` | "Nothing pending" |
| `usePaginationState`, `useDebouncedValue` | `src/shared/hooks/` | Queue filtering by proposal type |

## 8. Files to Create
- `src/app/(dashboard)/platform/approvals/page.tsx` — Approval Queue
- `src/app/(dashboard)/platform/approvals/[proposalId]/page.tsx` — Proposal Detail
- `src/features/maker-checker/components/approval-queue-table.tsx`
- `src/features/maker-checker/components/proposal-detail.tsx`
- `src/features/maker-checker/components/proposal-diff-view.tsx`
- `src/features/maker-checker/hooks/use-approval-queue.ts`
- `src/features/maker-checker/hooks/use-approve-proposal.ts`
- `src/features/maker-checker/api/maker-checker.repository.ts`
- `tests/features/maker-checker/self-approval-hidden.test.tsx`

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `CHANGE_PROPOSALS.APPROVE(id)`, `CHANGE_PROPOSALS.LIST`

## 10. NextJS Requirements
- Approval Queue: list of pending proposals (type, proposer, summary, time pending), filterable by type, tappable into Proposal Detail.
- Proposal Detail: full diff/comparison of the proposed change; proposer identity clearly labeled; Approve/Reject actions.
- **Hard requirement (§7 item 4):** when `proposal.proposed_by === current_admin.admin_id`, the approve action is not rendered as available (disabled or absent, per the PRD's own "disable OR hide" wording — choose hide, consistent with the platform's general "hide, don't show-disabled" pattern established in N-02).
- Redundant-approval no-op: if a second admin's approval attempt returns the already-resolved state, the UI reflects the resolved state gracefully (e.g., "This proposal was already resolved by [approver]"), not an error toast.

## 11. API Contract (Consumed)
- `GET /v1/admin/change-proposals?status=&proposal_type=&cursor=&limit=` (B-04 Task 08) — Approval Queue list, defaults to `status=pending`
- `GET /v1/admin/change-proposals/{id}` (B-04 Task 08) — Proposal Detail, including nested approvals
- `POST /v1/admin/change-proposals/{id}/approve` (B-04 Task 05)

## 12. Database Requirements
N/A (frontend).

## 13. Validation
N/A (read + single-action submission).

## 14. Authentication
Assumes established session.

## 15. Authorization
Approver role appropriate to the proposal type (per B-03's permission matrix, typically `super_admin`).

## 16. Error Handling
- Redundant-approval no-op → graceful "already resolved" message, not an error toast (Edge Case 2).
- `403 SAME_ADMIN_CANNOT_APPROVE_OWN_PROPOSAL` from the server → should be effectively unreachable given the UI hides the action, but handled gracefully as defense-in-depth if somehow triggered (e.g., a race where the admin's own identity resolution was stale).
- Standard network/error handling via `QueryErrorState`.

## 17. Offline First
N/A.

## 18. Local Data
None persisted.

## 19. Localization
All labels/messages localized, including proposal-type display names and diff-view labels.

## 20. RTL
Diff/comparison view must render correctly in RTL — verify before/after value alignment doesn't visually invert confusingly.

## 21. Analytics
Fire `maker_checker_proposal_approved`, `maker_checker_proposal_rejected` on action; `maker_checker_redundant_approval_noop` (internal) when the no-op path is hit.

## 22. Performance
Standard pagination on the Approval Queue; Proposal Detail's diff view should render efficiently even for larger `proposed_change` jsonb payloads (e.g., a full permission-matrix change) — consider a collapsible/summarized diff for very large payloads.

## 23. Security
The approve-hiding logic must use the current admin's actual authenticated identity (`useAdminSession()`), never a client-editable value; this is UX-only reinforcement — B-04's server-side identity comparison remains the real guarantee, and this file's tests must not claim otherwise.

## 24. Library Requirements
No new libraries, unless a dedicated JSON-diff-rendering utility is needed for the Proposal Detail view (evaluate a lightweight diff library only if hand-rolled before/after rendering proves visually inadequate for nested jsonb structures).

## 25. Testing
- **Mandatory test (§7 item 4):** using a fixture proposal where `proposed_by` equals the current admin's own id, confirm no approve action is rendered as available.
- Unit: redundant-approval no-op handling renders the resolved state gracefully.
- Integration: full role-change-proposal → second-admin-approval → applied-change flow using two distinct fixture admins (per §6.10 Testing Strategy).
- UI test: Approval Queue empty state ("Nothing pending").

## 26. Documentation
Note the self-approval-hiding pattern in the manual as the template for any future high-risk approval UI.

## 27. AI Coding Agent Implementation Steps

**Task 01 — Build Approval Queue List**
- Task ID: N-05-T01
- Files to Create: `approval-queue-table.tsx`, `use-approval-queue.ts`, `approvals/page.tsx`.
- Implementation Details: `DataTable` of pending proposals with type filter.
- Dependencies: B-04 list endpoint.
- Definition of Done: Queue renders, filterable, empty state correct.

**Task 02 — Build Proposal Detail & Diff View**
- Task ID: N-05-T02
- Files to Create: `proposal-detail.tsx`, `proposal-diff-view.tsx`, `[proposalId]/page.tsx`.
- Implementation Details: Full before/after comparison of `proposed_change`.
- Dependencies: Task 01.
- Definition of Done: Detail view renders a clear diff for at least role-permission-change and feature-flag-change proposal types.

**Task 03 — Implement Approve/Reject Actions**
- Task ID: N-05-T03
- Files to Create: `use-approve-proposal.ts`.
- Implementation Details: `ConfirmationDialog`-wrapped approve/reject, calling B-04's endpoint.
- Analytics: `maker_checker_proposal_approved`, `maker_checker_proposal_rejected`.
- Dependencies: Task 02, B-04 endpoint.
- Definition of Done: Both actions functional end-to-end.

**Task 04 — Self-Approval Hiding (Signature Test)**
- Task ID: N-05-T04
- Objective: Hide approve action when current admin is the proposer.
- Files to Create: `tests/features/maker-checker/self-approval-hidden.test.tsx`.
- Implementation Details: Compare `proposal.proposed_by` to `useAdminSession().admin.admin_id`; conditionally omit the approve control.
- Dependencies: Task 02, Task 03.
- Definition of Done: Signature test passes using a fixture proposal with `proposed_by` equal to the current admin.

**Task 05 — Redundant-Approval No-Op Handling**
- Task ID: N-05-T05
- Objective: Graceful UI for Edge Case 2.
- Files to Modify: `use-approve-proposal.ts`.
- Implementation Details: Detect the no-op response shape and render "already resolved by [approver]" rather than an error.
- Dependencies: Task 03.
- Definition of Done: No-op test passes.

**Task 06 — Two-Fixture-Admin Integration Test**
- Task ID: N-05-T06
- Objective: Full role-change-proposal → second-admin-approval → applied-change flow (§6.10).
- Dependencies: Tasks 01–05, N-04 (proposal creation), B-04.
- Definition of Done: End-to-end integration test passes using two distinct fixture admin identities.

**Task 07 — Localization, RTL, Accessibility Pass**
- Task ID: N-05-T07
- Dependencies: Tasks 01–03.
- Definition of Done: All labels localized; RTL diff-view alignment verified.

**Task 08 — Full Test Suite + Documentation**
- Task ID: N-05-T08
- Dependencies: Tasks 01–07.
- Definition of Done: All §25 scenarios green.

## 28. Definition of Done
- Approval Queue and Proposal Detail live, approver-role-gated.
- Approve action hidden for the proposer's own proposals, proven by a dedicated test.
- Redundant-approval no-op handled gracefully.
- Full two-fixture-admin integration flow passing.

## 29. Final Verification Checklist
- [ ] Signature test passes: approve action hidden when current admin is the proposer
- [ ] Redundant-approval no-op renders gracefully, not as an error
- [ ] Two-fixture-admin end-to-end approval flow passes
- [ ] "Nothing pending" empty state renders correctly
- [ ] Proposer/approver identities always visibly distinct in the UI
- [ ] RTL diff-view alignment verified
- [ ] `maker_checker_proposal_approved`/`_rejected` analytics fire correctly
