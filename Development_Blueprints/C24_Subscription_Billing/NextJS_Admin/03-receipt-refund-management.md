# N-03 — Receipt & Refund Management

## 1. Feature Context
A `commerce_admin`-restricted view of receipts and refund records associated with a subscription — tracking/reflecting refunds (which are themselves typically initiated through the store), not a refund-initiation tool. **Note:** full detail owned by E.33; this blueprint implements C.24's own ownership sketch (§8).

## 2. Parent Feature
Feature C.24 — Subscription & Billing

## 3. Sub-feature
3.3 Receipt & Refund Management (ID: **N-03**)

## 4. Objective
Build a read-focused (with limited tracking-action capability) view of a subscription's receipts and any associated refund records, restricted to `commerce_admin`, fully audited.

## 5. Business Requirements
- §8 Admin Requirements: Receipt/Refund Management — view receipts, process refunds per store policy (refunds themselves typically initiated through the store; this tool tracks/reflects them).
- No refund-initiation capability that bypasses store policy — this tool never becomes an alternative payment/refund processor.

## 6. Existing Architecture
`src/features/commerce/` (extends N-01/N-02's feature folder), embedded as a panel/tab within N-02's Subscription Detail view rather than a fully separate top-level page (confirm placement — E.33 may specify a standalone page; reconcile before implementation).

## 7. Existing Code to Reuse
- N-02's `SubscriptionDetailPanel` (embed as a tab/section within it).
- `src/shared/components/data-table.tsx` for receipt/refund list.

## 8. Files to Create
- `src/features/commerce/api/receipt-refund-repository.ts`
- `src/features/commerce/hooks/use-receipt-refund.ts`
- `src/features/commerce/components/receipt-refund-panel.tsx`

## 9. Files to Modify
- `src/features/commerce/components/subscription-detail-panel.tsx` (N-02) — add Receipt/Refund tab

## 10. NextJS Requirements
- `useReceiptRefundHistory(subscriptionId)`: list of receipts and any tracked refund records for the subscription.
- Refund records displayed as read/tracked entries (status, amount, date), not editable payment data.
- No form or action exists here that initiates a store-side refund directly — any "track a refund" action explicitly records that a refund was processed *through the store*, not a NoorHeroes-initiated payment reversal.

## 11. Required API
Receipt/refund read (and limited refund-tracking-record) endpoints — exact contract owned by E.33's backend specification. **Admin API.**

## 12. Validation
Any refund-tracking-record entry (if a manual "log this refund" action exists) requires an amount and a reference to the store-side refund event — never freeform without a store reference.

## 13. Authentication
Existing Admin Portal auth context (Bearer session).

## 14. Authorization
Restricted to `commerce_admin` role only (narrower than N-02's `support`/`commerce_admin`), enforced via `RequirePermission` and server-side check.

## 15. Error Handling
Empty state for a subscription with no receipts/refunds yet (new subscriber); API failure shows a retryable error state.

## 16. Loading States
Panel skeleton while receipt/refund data loads within N-02's detail view.

## 17. Responsive UI
Follows N-02's existing detail-panel responsive behavior.

## 18. Accessibility
Table semantics for receipt/refund list; proper labeling for any tracking-action form.

## 19. Localization
Admin Portal typically EN-only for internal tooling (confirm against `NEXT-JS-INSTRUCTIONS.md`).

## 20. Testing
- Unit: hook success/empty/error branches.
- Component: panel renders receipt/refund list correctly, distinguishes real revenue from any tracked comp/refund entries.
- RBAC: non-`commerce_admin` users cannot see this tab/panel even if they can access the parent Subscription Lookup page.

## 21. AI Coding Agent Implementation Steps

**Task 01 — Implement `ReceiptRefundRepositoryImpl`**
Objective: typed read API client. Files to Create: `receipt-refund-repository.ts`. Dependencies: backend endpoints live (E.33).

**Task 02 — Implement `useReceiptRefundHistory` Hook**
Objective: query hook for the panel. Files to Create: `use-receipt-refund.ts`. Dependencies: Task 01.

**Task 03 — Implement `ReceiptRefundPanel` Component**
Objective: list UI, embedded in N-02's detail view. Files to Create: `receipt-refund-panel.tsx`. Dependencies: Task 02.

**Task 04 — Wire into Subscription Detail Panel**
Objective: add as a `commerce_admin`-gated tab. Files to Modify: `subscription-detail-panel.tsx`. Dependencies: Task 03.

**Task 05 — Add Full Test Suite**
Objective: coverage per §20. Dependencies: Tasks 01–04.

## 22. Definition of Done
`commerce_admin` role can view a subscription's receipt and refund history within the Subscription Lookup detail view, with zero capability to initiate payments/refunds outside store policy, fully audited.

## 23. Final Verification Checklist
- [ ] Read-only receipt/refund display verified (no bypass-store-policy action exists)
- [ ] `commerce_admin`-only role enforcement (narrower than N-02) verified client- and server-side
- [ ] Empty state renders correctly for a new subscriber
- [ ] Any refund-tracking action requires a store-side reference, never freeform
