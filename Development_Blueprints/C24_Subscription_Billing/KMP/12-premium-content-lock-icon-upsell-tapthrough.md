# K-12 — Premium Content Lock Icon & Upsell Tap-Through

## 1. Feature Context
A reusable, shared UI component: a small, friendly lock badge overlaid on an otherwise fully-visible premium content card in parent-approved discovery contexts (never hidden entirely), tapping through to the Subscription upsell rather than a dead end.

## 2. Parent Feature
Feature C.24 — Subscription & Billing

## 3. Sub-feature
2.12 Premium Content Lock Icon & Upsell Tap-Through (ID: **K-12**)

## 4. Objective
Build a shared `PremiumLockBadge` component and its tap-through handler, consumed by A.3/A.10 (and any other content-catalog feature) to mark premium content as locked-not-hidden for Free-plan families, routing to Subscription on tap.

## 5. Business Requirements
- FR-14: "Premium content items remain visible with a lock icon in parent-approved discovery contexts — never hidden entirely. Locking never deletes progress. Free plan always supports basic Islamic education."
- §2.1: "Lock Icon Treatment — consistent with A.3/A.10's existing 'locked, not hidden' premium-content visual pattern — a small, friendly lock badge on an otherwise fully-visible content card, tapping through to the upsell rather than a dead end."
- §1.10 Edge Case #6: browsing premium content on Free plan shows the lock icon in the relevant parent-approved discovery context, tapping routes to Subscription upsell — never silently absent from a catalog/browse view.

## 6. Existing Architecture
Shared component placed in `:core:design-system` or a dedicated `:core:entitlement-ui` module (consumed cross-feature by A.3/A.10's content-card composables) — not owned by any single content feature, since it's C.24's entitlement-gating visual contract applied wherever premium content appears.

## 7. Existing Code to Reuse
- K-07's `EntitlementRepository.check(CONTENT_DETAIL or CATALOG, childId)` — determines lock state per content item.
- A.3/A.10's existing content-card component (extend with the lock badge overlay, do not fork a separate locked-card variant).

## 8. Files to Create
- `core/designsystem/components/PremiumLockBadge.kt`
- `feature/subscription/navigation/PremiumUpsellTapHandler.kt` — shared tap-through-to-Subscription-landing handler
- `test/core/designsystem/PremiumLockBadgeTest.kt`

## 9. Files to Modify
- A.3's Stories content-card composable — add `PremiumLockBadge` overlay for locked items (coordinate with A.3's own blueprint; this file defines the shared component's contract)
- A.10's Games content-card composable — same integration point

## 10. KMP Requirements
- `PremiumLockBadge(isLocked: Boolean)` renders a small lock icon overlay only when `isLocked=true`; the underlying content card (title, thumbnail, metadata) remains fully visible and rendered identically to an unlocked card otherwise — locking never removes the card from a catalog/list view.
- Tap on a locked card routes through `PremiumUpsellTapHandler`, which navigates to the Subscription landing screen (K-01) with an upsell context flag (for potential contextual messaging on arrival) rather than attempting to open the content itself.
- Locked state is derived exclusively from `EntitlementRepository.check()` (K-07) — no content feature independently determines lock status.
- Never applied within a child-mode session (locked-content upsell messaging is a parent-mode-only concept; child-mode content gating, if any, is a distinct concern owned by the content feature itself, not this badge).

## 11. Required API
None directly — consumes K-07's `EntitlementRepository.check()` (backed by B-06).

## 12. Offline First
Lock state renders from K-07's cached entitlement result when offline; tap-through to Subscription still works offline (K-01 renders last-cached state).

## 13. Local Data
None new — relies entirely on K-07's existing cache.

## 14. Localization
Any lock-badge accessibility label/tooltip ("Premium content — tap to upgrade") fully localized EN/HI/AR/UR.

## 15. RTL
Badge overlay position mirrors correctly in RTL (e.g., top-right in LTR becomes top-left in RTL, consistent with existing card-overlay conventions).

## 16. Analytics
`premium_lock_icon_tapped` per §1.19, fired on tap-through.

## 17. Performance
Lightweight overlay composable; lock-state derivation should not trigger a per-card network call — batch/cache via K-07 to avoid N+1 entitlement checks across a large catalog grid.

## 18. Security
Reachable only from parent-approved discovery contexts, never child mode — verify via K-08's extended structural test that this badge's upsell tap-handler is not wired into any child-mode-reachable content screen.

## 19. Testing
- Unit test: badge renders lock overlay only when `isLocked=true`; card remains fully visible either way.
- UI test: tap on a locked card routes to Subscription landing, never attempts to open the content.
- UI test: batch entitlement-check performance for a grid of many content items (no N+1 network calls).
- Structural test (extends K-08): confirm no child-mode-reachable content screen wires this upsell tap-handler.

## 20. AI Coding Agent Implementation Steps

**Task 01 — Implement `PremiumLockBadge` Component**
Objective: overlay composable per §10. Files to Create: `PremiumLockBadge.kt`. Dependencies: none.

**Task 02 — Implement `PremiumUpsellTapHandler`**
Objective: shared tap-through navigation to K-01 with upsell context. Files to Create: `PremiumUpsellTapHandler.kt`. Dependencies: K-01.

**Task 03 — Integrate into A.3/A.10 Content Cards**
Objective: wire the badge and tap handler into existing content-card composables (coordinate with A.3/A.10 blueprints). Files to Modify: A.3/A.10 content-card files. Dependencies: Tasks 01–02, K-07.

**Task 04 — Batch Entitlement-Check Optimization**
Objective: avoid N+1 checks across a catalog grid. Files to Modify: `PremiumLockBadge.kt` or its consuming ViewModel layer. Dependencies: Task 01, K-07.

**Task 05 — Extend K-08 Structural Test & Add Analytics/Test Suite**
Objective: `premium_lock_icon_tapped`, coverage per §19, extended child-mode-invisibility check. Dependencies: Tasks 01–04.

## 21. Final Verification Checklist
- [ ] Locked content always visible in catalog/browse views, never hidden
- [ ] Lock state derived exclusively from `EntitlementRepository.check()`, no independent per-feature logic
- [ ] Tap-through routes to Subscription landing, never attempts content playback
- [ ] No N+1 entitlement-check calls across a content grid
- [ ] Extended K-08 test confirms zero child-mode reachability
- [ ] RTL badge placement verified

## 22. Definition of Done
`PremiumLockBadge` and its tap-through handler are live as a shared component consumed by A.3/A.10, showing locked content visibly (never hidden) and routing taps into Subscription, verified unreachable from child mode.
