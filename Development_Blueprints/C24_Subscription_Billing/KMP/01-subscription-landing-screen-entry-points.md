# K-01 — Subscription Landing Screen & Entry Points

## 1. Feature Context
The primary Subscription & Billing screen: plan card, entitlement list, invoice history entry, "Manage on Play Store" deep link, and cancel action. Reached from the Parent Dashboard module shortcut, a paywall upsell, or Settings — never a standalone tab.

## 2. Parent Feature
Feature C.24 — Subscription & Billing

## 3. Sub-feature
2.1 Subscription Landing Screen & Entry Points (ID: **K-01**)

## 4. Objective
Build `SubscriptionLandingScreen` + `SubscriptionViewModel` in a new `:feature:subscription` module, rendering current entitlement/plan state sourced exclusively from the backend (never a locally-computed "purchased" flag), with loading/error/offline states and the three defined entry points wired.

## 5. Business Requirements
- FR-11: components are plan card, entitlement list, invoice history link, "Manage on Play Store" deep link, cancel action.
- Entry points: Parent Dashboard module shortcut (C.20), paywall upsell, Settings. Exit points: Plan Comparison, Invoice History, Cancel Flow, external Play Store billing sheet.
- `SubscriptionViewModel` derives state from `GET /v1/parent/subscription` (B-05) only — never independently caches a "purchased" state from the Play Billing SDK.

## 6. Existing Architecture
New Kotlin/Compose module `:feature:subscription` (MVVM, Clean Architecture), depends on `:core:auth`, `:core:design-system`, `:core:network`. Follows the same module-scaffolding pattern as C.20's `:feature:dashboard` (Parent Dashboard landing + module shortcut grid entry pattern).

## 7. Existing Code to Reuse
- `:core:design-system` tokens (A.1 §2.1) and Parent-Mode formal visual register (C.19 §2.1).
- C.20's module shortcut grid component (entry point into this screen).
- `:core:network` Retrofit/OkHttp client scaffolding, Hilt DI conventions.
- `:core:auth` parent-session token handling.

## 8. Files to Create
- `feature/subscription/ui/SubscriptionLandingScreen.kt`
- `feature/subscription/viewmodel/SubscriptionViewModel.kt`
- `feature/subscription/data/SubscriptionRepository.kt` (interface + impl, `getPlans()`/`subscribe()`/`cancel()`/`getInvoices()` stubs wired here, implemented fully in K-02/K-04/K-05/K-06)
- `feature/subscription/navigation/SubscriptionRoute.kt`
- `test/feature/subscription/SubscriptionViewModelTest.kt`

## 9. Files to Modify
- `core-navigation/Route.kt` — register `SubscriptionRoute`, deep link `noorheroes://parent/subscription`
- C.20's module shortcut grid — wire Subscription shortcut destination

## 10. KMP Requirements
- `SubscriptionViewModel` calls `SubscriptionRepository` backed by `GET /v1/parent/subscription`; UI state is a sealed `SubscriptionUiState` (Loading/Success/Error/Offline).
- Offline: render last-cached entitlement state (via `:core:data` local cache), disable purchase/cancel-triggering actions with a clear "requires connection" indicator.
- Cancel/"Manage on Play Store" actions route to K-06; plan-card upgrade/trial CTA routes to K-02.
- Stable/immutable `SubscriptionUiState` data class to avoid unnecessary recomposition.

## 11. Required API
`GET /v1/parent/subscription` (B-05). **User API.**

## 12. Offline First
Last-cached entitlement state renders via `:core:data` local persistence; purchase/upgrade/cancel actions require connectivity and are disabled offline with explicit messaging (PRD §1.14).

## 13. Local Data
New local cache entry for the subscription/entitlement snapshot (`:core:database` or `:core:datastore`, per existing offline-caching convention — confirm exact mechanism against C.20 K-07's dashboard offline-caching implementation before choosing).

## 14. Localization
All screen copy (plan name, entitlement list, action labels) fully localized EN/HI/AR/UR; no hardcoded strings.

## 15. RTL
Plan card, entitlement checklist, and action button layout mirror correctly in RTL.

## 16. Analytics
`subscription_screen_viewed` on screen composition, with entry-point source as a parameter (dashboard/upsell/settings).

## 17. Performance
Stable UI state class; avoid recomposition on unrelated ViewModel state changes; skeleton loading state while entitlement data loads.

## 18. Security
No billing/subscription composable reachable from any child-mode-session-scoped navigation graph (structural guarantee enforced/tested in K-08).

## 19. Testing
- Unit: `SubscriptionViewModel` state derivation from mocked `GET /v1/parent/subscription` responses (loading/success/error).
- UI: skeleton loading state renders correctly.
- UI: offline state disables purchase/cancel CTAs with correct messaging.
- Integration: deep link `noorheroes://parent/subscription` navigates correctly from a cold start.

## 20. AI Coding Agent Implementation Steps

**Task 01 — Scaffold `:feature:subscription` Module**
Objective: create module with Hilt DI, dependencies wired. Files to Create: module `build.gradle.kts`, package scaffolding. Dependencies: none.

**Task 02 — Implement `SubscriptionRepository` (Landing Subset)**
Objective: `getSubscriptionStatus()` wrapping `GET /v1/parent/subscription`. Files to Create: `SubscriptionRepository.kt`. Dependencies: Task 01.

**Task 03 — Implement `SubscriptionViewModel`**
Objective: sealed `SubscriptionUiState`, offline-cache-aware loading. Files to Create: `SubscriptionViewModel.kt`. Dependencies: Task 02.

**Task 04 — Implement `SubscriptionLandingScreen` Composable**
Objective: plan card, entitlement list, invoice/cancel/manage-billing entry points. Files to Create: `SubscriptionLandingScreen.kt`. Dependencies: Task 03.

**Task 05 — Wire Navigation & Deep Link**
Objective: register route, deep link, entry points from C.20's shortcut grid, paywall upsell, Settings. Files to Modify: `core-navigation/Route.kt`, C.20's shortcut grid. Dependencies: Task 04.

**Task 06 — Add Analytics & Test Suite**
Objective: `subscription_screen_viewed` instrumentation, coverage per §19. Dependencies: Tasks 01–05.

## 21. Final Verification Checklist
- [ ] Entitlement state sourced exclusively from backend response, never a local SDK-derived flag
- [ ] Offline state renders last-cached data with purchase actions disabled
- [ ] All three entry points (Dashboard, upsell, Settings) verified
- [ ] Deep link verified from cold start
- [ ] No hardcoded strings; RTL layout verified

## 22. Definition of Done
`SubscriptionLandingScreen` live in `:feature:subscription`, reachable from all three entry points and the deep link, rendering server-sourced entitlement state with correct loading/offline/error handling.
