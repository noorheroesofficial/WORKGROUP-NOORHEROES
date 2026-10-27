# N-02 — Subscription & Entitlement Lookup

## 1. Feature Context
Support-facing search tool: find any subscription by family/parent/subscription identifier, view its current state, full state-transition history, and any reconciliation corrections applied to it. **Note:** full detail owned by E.33; this blueprint implements C.24's own ownership sketch (§8).

## 2. Parent Feature
Feature C.24 — Subscription & Billing

## 3. Sub-feature
3.2 Subscription & Entitlement Lookup (ID: **N-02**)

## 4. Objective
Build a search-and-detail view letting `support`/`commerce_admin` roles find a subscription and inspect its full state and billing-event history for ticket resolution, sourced from B-03's `billing_webhook_event` log and B-04's reconciliation-correction records.

## 5. Business Requirements
- §8 Admin Requirements: Subscription/Entitlement Lookup — read-only + limited correction actions, `support`/`commerce_admin` role.
- E.33 §1.3: search by family/parent/subscription identifier, see full state and billing-event history.
- Subscription-search-to-resolution time target ≤ 5 minutes (E.33 §1.4).

## 6. Existing Architecture
`src/features/commerce/` (extends N-01's feature folder), following E.32's sibling account-search pattern (per PRD cross-ref) — reuse E.32's search-input/results-list UI pattern rather than building a divergent one.

## 7. Existing Code to Reuse
- E.32's account-search component pattern (sibling search UX).
- `src/shared/components/data-table.tsx` for state-transition history.
- `src/shared/components/require-permission.tsx::RequirePermission`.

## 8. Files to Create
- `src/features/commerce/api/subscription-lookup-repository.ts`
- `src/features/commerce/hooks/use-subscription-lookup.ts`
- `src/features/commerce/components/subscription-search-bar.tsx`
- `src/features/commerce/components/subscription-detail-panel.tsx`
- `src/app/(dashboard)/commerce/subscriptions/page.tsx`

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add lookup endpoint constants
- Sidebar navigation config — add "Subscription Lookup" under Commerce

## 10. NextJS Requirements
- `useSubscriptionSearch(query)`: search by masked family/parent identifier or subscription ID.
- `useSubscriptionDetail(id)`: full state, state-transition history (sourced from `billing_webhook_event`), and any reconciliation corrections (from B-04) applied to this specific subscription.
- Identifiers displayed masked per admin display conventions (consistent with N-02's `support` role exposure level, not full PII).
- Empty/no-results state distinct from loading state.

## 11. Required API
Subscription lookup/history endpoints (admin-scoped, exact contract owned by E.33's backend specification — confirm before finalizing). **Admin API.**

## 12. Validation
Search query minimum length before triggering a request (avoid overly broad/expensive queries); identifier format validated client-side where a specific format (UUID) is expected.

## 13. Authentication
Existing Admin Portal auth context (Bearer session).

## 14. Authorization
`support`/`commerce_admin` role required, enforced via `RequirePermission` and server-side authoritative check.

## 15. Error Handling
No-results state (not an error) with a clear "no matching subscription found" message; network/API failure shows a retry-eligible error state.

## 16. Loading States
Search-in-progress spinner; detail-panel skeleton while history loads.

## 17. Responsive UI
Search bar + results list collapse to a single-column stacked layout on narrow viewports.

## 18. Accessibility
Search input properly labeled; results list keyboard-navigable; state-transition history table accessible (proper table semantics, not div-based).

## 19. Localization
Admin Portal typically EN-only for internal tooling (confirm against `NEXT-JS-INSTRUCTIONS.md` before assuming otherwise).

## 20. Testing
- Unit: search hook success/no-results/error branches.
- Component: detail panel renders state-transition history and reconciliation corrections correctly.
- Integration: full search → select → detail-view flow against a mocked backend.
- RBAC: non-`support`/`commerce_admin` users blocked from the route.

## 21. AI Coding Agent Implementation Steps

**Task 01 — Implement `SubscriptionLookupRepositoryImpl`**
Objective: typed search/detail API client. Files to Create: `subscription-lookup-repository.ts`. Dependencies: backend lookup endpoints live (E.33).

**Task 02 — Implement React Query Hooks**
Objective: search + detail hooks. Files to Create: `use-subscription-lookup.ts`. Dependencies: Task 01.

**Task 03 — Implement Search Bar & Detail Panel Components**
Objective: UI per §10. Files to Create: both component files. Dependencies: Task 02.

**Task 04 — Wire Page Route & Navigation**
Objective: `/commerce/subscriptions` page, RBAC-gated nav entry. Files to Create/Modify: page file, sidebar nav config. Dependencies: Task 03.

**Task 05 — Add Full Test Suite**
Objective: coverage per §20. Dependencies: Tasks 01–04.

## 22. Definition of Done
`support`/`commerce_admin` roles can search for any subscription by masked identifier and view its full state, transition history, and reconciliation corrections, meeting the ≤5-minute resolution-time target for typical tickets.

## 23. Final Verification Checklist
- [ ] Search returns correct results by family/parent/subscription identifier
- [ ] State-transition history and reconciliation corrections both visible in detail view
- [ ] Identifiers displayed masked, not full PII
- [ ] `support`/`commerce_admin` role enforced client- and server-side
- [ ] No-results state distinct from error state
