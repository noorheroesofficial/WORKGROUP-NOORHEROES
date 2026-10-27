# N-04 — Reward Ledger & Manual Grant UI

> **Reconciliation note (2026-08-18):** supersedes `A11_Rewards_System/NextJS_Admin/05-reward-ledger-audit-viewer.md` (now deprecated). Note: A.11's separate Reconciliation Incident Log (`06-reconciliation-incident-log.md`, N-06) is a distinct, non-duplicated surface and remains A.11-owned — not covered by this file.

## 1. Feature Context
Part of **Feature E.31 — Engagement Tools Admin Suite**. Delivers the Admin Portal screens for the read-only reward ledger and the audited manual reward-grant tool, consuming **B-04 Reward Ledger & Manual Grant API**. Split from XP Rule authoring (see **N-03 XP Rule Management UI**) per PRD §1.18's distinct screen grouping. Source: PRD §1.18 Screens 9–10, §2.1 (Ledger Visual Cue), §6.

## 2. Parent Feature
Feature E.31 — Engagement Tools Admin Suite

## 3. Sub-feature
3.4 Reward Ledger & Manual Grant UI (Admin ID: **N-04**)

## 4. Objective
Render the Reward Ledger Viewer with absolutely no edit/delete affordances anywhere in its UI — reinforcing visually that it is a permanent record — and give support/billing-ops agents a manual grant tool that requires a reason code before submission is possible.

## 5. Business Requirements
- Screen Inventory (PRD §1.18): #9 Reward Ledger Viewer (read-only, append-only), #10 Manual Reward Grant Tool (audited).
- Append-Only Ledger Visual Cue (PRD §2.1): no edit/delete affordances anywhere in the Ledger Viewer UI.

## 6. Existing Architecture
React + TypeScript, Admin Portal shell from E.28, E.29's read-only audit-style screen pattern reused for the Ledger Viewer.

## 7. Existing Code to Reuse
E.28 shell/design tokens; E.29's established read-only audit-screen visual pattern (reused for Ledger Viewer, not reinvented).

## 8. Files to Create
- `app/(admin)/engagement/rewards/ledger/page.tsx`
- `app/(admin)/engagement/rewards/ledger/manual-grant/page.tsx`
- `components/engagement/rewards/RewardLedgerViewer.tsx`
- `components/engagement/rewards/ManualGrantForm.tsx`
- `repositories/admin/RewardLedgerAdminRepository.ts`
- `types/admin/rewardLedger.ts`
- `__tests__/engagement/rewards/RewardLedgerViewer.test.tsx`
- `__tests__/engagement/rewards/ManualGrantForm.test.tsx`

## 9. Files to Modify
- `components/shell/EngagementNavGroup.tsx`
- `lib/analytics/EngagementAdminAnalytics.ts`

## 10. Backend Requirements
Consumes **B-04** endpoints: `GET /v1/admin/reward-ledger`, `POST /v1/admin/reward-ledger/manual-grant`.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- **Page:** Reward Ledger Viewer, Manual Reward Grant Tool.
- **Route:** `/engagement/rewards/ledger`, `/engagement/rewards/ledger/manual-grant`.
- **Component:** `RewardLedgerViewer` (strictly read-only rendering — no row action menu, no edit icon, no delete icon anywhere in the DOM), `ManualGrantForm` (reason-code required field, idempotency-key auto-generated or admin-supplied).
- **API Client:** `RewardLedgerAdminRepository`.
- **Type Definition:** `RewardLedgerEntry`, `ManualGrantInput`.
- **Form:** React Hook Form + Zod; `ManualGrantForm` requires `reason_code` (dropdown of registered codes) before submit is enabled.
- **Validation:** client mirrors backend's mandatory `reason_code`/`idempotency_key` requirements.
- **Authentication/Authorization:** `support`/`billing_ops` role gate specifically on the Manual Grant Tool route/action — a `content_editor`-only admin should not even see this route in navigation.
- **Loading/Empty/Error States:** standard.
- **Pagination:** ledger viewer paginated by `child_id` context.
- **Filtering:** ledger by `reason_type`, date range, `child_id`.
- **Responsive/Accessibility/RTL:** standard.
- **Analytics:** `manual_reward_grant_issued`.
- **Performance:** ledger list virtualized for large per-child histories.
- **Testing:** UI test confirming zero edit/delete controls anywhere in Ledger Viewer's rendered DOM (signature test, PRD §2.1); UI test confirming manual grant blocks submission without a reason code.

## 13. API Contract
Reuses B-04's contract verbatim (see `Backend/04-reward-ledger-manual-grant-api.md` §13).

## 14. Database Requirements
N/A.

## 15. Validation
`reason_code` required before Manual Grant submit is enabled; `idempotency_key` auto-generated client-side (UUID) if not manually supplied, to prevent accidental double-submission on network retry.

## 16. Authentication
Inherits E.28 session.

## 17. Authorization
Ledger Viewer: any admin role with Engagement/Support visibility. Manual Grant Tool: `support`/`billing_ops` only — route itself should redirect/403 for other roles, and the navigation entry point should be hidden entirely for non-eligible roles (defense-in-depth alongside backend's own `403`).

## 18. Error Handling
| Scenario | UI Behavior |
|---|---|
| Manual grant submitted without reason code | Client blocks submit; server `422 REASON_CODE_REQUIRED` also handled as a fallback message |
| Duplicate idempotency key (network retry) | UI shows the original grant result, not an error — "This grant was already processed" |
| `403 FORBIDDEN` on manual grant | Redirect with "This action requires Support or Billing Ops role" message |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
`reason_code` dropdown labels localized; ledger entry descriptions resolve through localization keys where applicable.

## 22. RTL
Full RTL support.

## 23. Analytics
`manual_reward_grant_issued` (with `reason_code` param).

## 24. Performance
Ledger virtualization for large histories; debounced child-search input on the ledger filter.

## 25. Security
The Ledger Viewer's structural absence of edit/delete UI controls is a direct visual reinforcement of the backend's DB-permission-level append-only guarantee (B-04) — this is treated as a security-relevant UI requirement, not merely cosmetic, per PRD §2.1's explicit "Append-Only Ledger Visual Cue" requirement.

## 26. Library Requirements
React, TypeScript, React Hook Form, Zod, `crypto.randomUUID()` for client-side idempotency-key generation, React Query, Jest/RTL.

## 27. Testing
- **UI test (signature):** Reward Ledger Viewer's rendered output contains zero edit/delete/action-menu elements for any ledger row, verified via DOM query assertion (PRD §2.1).
- **Integration:** manual grant flow — reason code required, idempotency-key replay handled gracefully.
- **Unit:** form validation.

## 28. Documentation
Document the Ledger Viewer's "no mutation UI, ever" design constraint prominently in the component's own file header comment, to prevent a future well-intentioned developer from adding an edit button.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Types & API Client**
- Task ID: N-04-T01
- Files to Create: `types/admin/rewardLedger.ts`, `repositories/admin/RewardLedgerAdminRepository.ts`.
- Dependencies: B-04.
- Definition of Done: typed repository unit-tested against mocked API.

**Task 02 — Reward Ledger Viewer**
- Task ID: N-04-T02
- Files to Create: `app/(admin)/engagement/rewards/ledger/page.tsx`, `components/engagement/rewards/RewardLedgerViewer.tsx`.
- Implementation Details: read-only rendering; no action column at all in the table definition.
- Dependencies: Task 01.
- Definition of Done: signature zero-edit-delete-controls UI test passes.

**Task 03 — Manual Reward Grant Tool**
- Task ID: N-04-T03
- Files to Create: `app/(admin)/engagement/rewards/ledger/manual-grant/page.tsx`, `components/engagement/rewards/ManualGrantForm.tsx`.
- Implementation Details: role-gated route (`support`/`billing_ops` only); reason-code dropdown required; auto-generated idempotency key.
- Dependencies: Task 01, Task 02.
- Definition of Done: role-gating test passes; reason-code-required test passes.

**Task 04 — Permission Gating & Accessibility**
- Task ID: N-04-T04
- Dependencies: Tasks 02–03.
- Definition of Done: accessibility audit passes; role-based navigation visibility verified.

**Task 05 — Tests & Documentation**
- Task ID: N-04-T05
- Dependencies: Tasks 01–04.
- Definition of Done: §31 checklist verified.

## 30. Definition of Done
Ledger Viewer structurally has zero mutation UI; Manual Grant Tool enforces reason-code and role restrictions; all screens tested.

## 31. Final Verification Checklist
- [ ] Reward Ledger Viewer has zero edit/delete/action controls anywhere (signature test green)
- [ ] Manual Grant Tool requires reason code before submit
- [ ] Manual Grant Tool route restricted to `support`/`billing_ops`, hidden from other roles in navigation
- [ ] Idempotency-key replay handled gracefully in the UI
- [ ] Loading/empty/error states implemented
- [ ] Responsive, accessible, RTL-supported
- [ ] Analytics events fire correctly
- [ ] No school/madrasa/institutional-tier logic introduced
