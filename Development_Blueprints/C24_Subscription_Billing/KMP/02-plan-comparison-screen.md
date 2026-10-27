# K-02 — Plan Comparison Screen

## 1. Feature Context
Three-card plan comparison (Free Family Starter / Mobile Family / Premium Family) with a monthly/annual toggle that recalculates displayed pricing and savings, reached from the Subscription landing screen.

## 2. Parent Feature
Feature C.24 — Subscription & Billing

## 3. Sub-feature
2.2 Plan Comparison Screen (ID: **K-02**)

## 4. Objective
Build `PlanComparisonScreen` rendering the three canonical plans from `GET /api/v1/billing/plans` (B-01), with a working monthly/annual toggle, current-plan highlighting, child-capacity callouts, and fully accessible pricing/savings text.

## 5. Business Requirements
- FR-1: exact plan definitions (Free $0/1 child, Mobile Family $3/mo or $30/yr–16.7% savings/4 children, Premium Family $5.99/mo or $59/yr–17.9% savings/8 children).
- §2.2: three plan cards, monthly/annual toggle, feature checklists, child-capacity callout, current-plan indicator; stacked on mobile, 3-column on tablet.
- Accessibility: pricing/savings fully screen-reader-readable, not visual-badge-only.

## 6. Existing Architecture
Part of `:feature:subscription` (K-01). Consumes `SubscriptionRepository.getPlans()`, extends the module scaffolded in K-01.

## 7. Existing Code to Reuse
- `:core:design-system` card/toggle/checklist components.
- A.3/A.10's "locked, not hidden" visual pattern reference for consistency of premium-content framing (not directly reused here, but the visual language this screen sets is what K-08's lock-icon component elsewhere mirrors).
- `SubscriptionRepository` (K-01, extend with `getPlans()`).

## 8. Files to Create
- `feature/subscription/ui/PlanComparisonScreen.kt`
- `feature/subscription/ui/components/PlanCard.kt`
- `feature/subscription/viewmodel/PlanComparisonViewModel.kt`
- `test/feature/subscription/PlanComparisonViewModelTest.kt`

## 9. Files to Modify
- `feature/subscription/data/SubscriptionRepository.kt` — implement `getPlans()` wrapping `GET /api/v1/billing/plans`
- `feature/subscription/navigation/SubscriptionRoute.kt` — add `PlanComparisonRoute`

## 10. KMP Requirements
- `PlanComparisonViewModel` loads plan catalog once, holds `isAnnualToggleActive: Boolean` state; toggling recalculates displayed price/savings client-side from already-fetched data (no re-fetch on toggle).
- Current-plan card visually highlighted based on the parent's active `plan` (from K-01's `SubscriptionUiState`, passed in or re-queried).
- Each `PlanCard` action ("Start Free" / "Start Trial" / "Upgrade") navigates to K-03 (Trial/Upgrade Disclosure) with the selected plan code as a nav argument.

## 11. Required API
`GET /api/v1/billing/plans` (B-01, public, cached). **User API** (public, no auth).

## 12. Offline First
Renders last-cached plan catalog if offline (catalog changes rarely, safe to cache with a longer TTL client-side); toggle interaction works fully offline since it's local recalculation only.

## 13. Local Data
Cache the plan catalog response locally (`:core:datastore` or in-memory singleton with TTL, per existing convention) to avoid re-fetching on every screen visit.

## 14. Localization
Plan names, feature checklist items, pricing/currency, and savings percentage formatted per locale (EN/HI/AR/UR); date/number formatting via platform locale utilities.

## 15. RTL
Three-card layout and toggle mirror correctly in RTL; checkmark icons flip position appropriately.

## 16. Analytics
`plan_comparison_viewed` on screen composition.

## 17. Performance
Toggle recalculation is pure client-side arithmetic on already-fetched data — no network call, no perceptible lag; stable state class prevents unnecessary card recomposition.

## 18. Security
No billing action is taken directly on this screen (navigation-only to K-03) — no receipt/purchase logic lives here.

## 19. Testing
- Unit: `PlanComparisonViewModel` toggle recalculation produces correct monthly/annual figures for all three plans.
- UI: current-plan card correctly highlighted for each of the three possible current plans.
- UI: screen-reader accessibility test confirms pricing/savings text is announced, not just visually badged.
- UI: responsive layout test (stacked mobile vs. 3-column tablet).

## 20. AI Coding Agent Implementation Steps

**Task 01 — Implement `SubscriptionRepository.getPlans()`**
Objective: wrap `GET /api/v1/billing/plans` with local caching. Files to Modify: `SubscriptionRepository.kt`. Dependencies: K-01.

**Task 02 — Implement `PlanComparisonViewModel`**
Objective: load catalog, manage toggle state, compute derived pricing. Files to Create: `PlanComparisonViewModel.kt`. Dependencies: Task 01.

**Task 03 — Implement `PlanCard` Component**
Objective: reusable card per plan with checklist, capacity badge, CTA. Files to Create: `PlanCard.kt`. Dependencies: none.

**Task 04 — Implement `PlanComparisonScreen` Composable**
Objective: toggle + three-card layout, responsive rules, accessibility labels. Files to Create: `PlanComparisonScreen.kt`. Dependencies: Tasks 02–03.

**Task 05 — Wire Navigation to K-03**
Objective: each CTA navigates to Trial/Upgrade Disclosure with plan code argument. Files to Modify: `SubscriptionRoute.kt`. Dependencies: Task 04.

**Task 06 — Add Analytics & Test Suite**
Objective: `plan_comparison_viewed`, coverage per §19. Dependencies: Tasks 01–05.

## 21. Final Verification Checklist
- [ ] Three plans render with exact PRD pricing/capacity/savings figures
- [ ] Annual toggle recalculates correctly without a network re-fetch
- [ ] Current-plan highlighting correct for all three plan states
- [ ] Pricing/savings fully screen-reader accessible
- [ ] Responsive stacked/3-column layout verified
- [ ] RTL layout verified

## 22. Definition of Done
`PlanComparisonScreen` renders all three plans accurately with working monthly/annual toggle, correct current-plan highlighting, full accessibility, and routes each CTA into K-03.
