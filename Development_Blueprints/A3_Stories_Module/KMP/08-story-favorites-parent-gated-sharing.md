# K-08 — Story Favorites & Parent-Gated Sharing

## 1. Feature Context
Favoriting is low-friction and optimistic; sharing is deliberately high-friction — every share attempt routes through the existing Parent PIN/Biometric Gate before any link or card is generated, with no direct ungated share path anywhere in child mode.

## 2. Parent Feature
Feature A.3 — Stories Module (Animated Storytelling System)

## 3. Sub-feature
2.8 Story Favorites & Parent-Gated Sharing (ID: **K-08**)

## 4. Objective
Build the Favorites List screen (optimistic toggle + retry) and the Share flow (parent gate → approved share card preview), consuming B-09 and reusing the existing Parent PIN/Biometric Gate component from A.1/C.19.

## 5. Business Requirements
- FR-13: sharing opens a parent gate and produces an approved deep link or parent-facing card — direct ungated sharing never available in child mode.
- FR-14: no open comment system; only moderated child-safe reaction stickers or parent-facing feedback.
- Edge Case 11: favorite reference resolves to the new canonical content ID after admin restructuring, never a broken reference.

## 6. Existing Architecture
`feature:stories` module, reusing the existing Parent PIN/Biometric Gate component (established in A.1/C.19 — must be located and reused, never rebuilt).

## 7. Existing Code to Reuse
- Existing Parent PIN/Biometric Gate component (A.1/C.19 — exact name to confirm in codebase)
- `feature/stories/data/StoryCatalogRepository.kt` (K-01, pattern reference for optimistic-update handling)
- `core-designsystem`: card/modal components

## 8. Files to Create
- `feature/stories/ui/FavoritesListScreen.kt`
- `feature/stories/ui/ShareStoryMomentGate.kt`
- `feature/stories/ui/ApprovedShareCardPreview.kt`
- `feature/stories/data/FavoriteRepository.kt` (B-09 client, optimistic-update-friendly)
- `feature/stories/viewmodel/FavoritesViewModel.kt` (+ State/Event files)
- `feature/stories/viewmodel/ShareFlowViewModel.kt` (+ State/Event files)
- `test/feature/stories/FavoritesViewModelTest.kt`
- `androidTest/feature/stories/ShareGateFlowTest.kt`

## 9. Files to Modify
- `core-navigation/Route.kt` — add `FavoritesListRoute`

## 10. KMP Requirements
- `FavoriteRepository.toggleFavorite(episodeId)`: optimistic local state update immediately on tap, reconciled/rolled-back on API failure (retry affordance shown on failure, not a silent revert).
- `FavoritesViewModel`: renders `is_available: false` items (withdrawn content) with a "no longer available" treatment rather than removing them or crashing on a broken reference; resolves restructured content to the canonical ID transparently per B-09's response shape.
- `ShareFlowViewModel`: on Share tap, invokes the existing Parent PIN/Biometric Gate component — no share card/link is generated or even requested from any API until the gate resolves successfully. Cancel at the gate returns cleanly to the player with zero residual share state.
- No open comment/reaction system exists anywhere in this sub-feature — only the parent-gated share path and (if in scope elsewhere) moderated reaction stickers, never a public comment field.

## 11. Required API
**User API** — B-09 `POST /v1/favorites`, `DELETE /v1/favorites/{episode_id}`, `GET /v1/favorites`.

## 12. Offline First
Favorite toggles queue via the shared `OfflineEventOutbox` (K-07) when offline, applied optimistically to local state immediately.

## 13. Local Data
Favorites list cached locally (via `core-datastore`) for instant render on Favorites List screen open, refreshed from B-09 on entry.

## 14. Localization
Favorites List and Share Gate copy sourced from shared localization resources.

## 15. RTL
Favorites list item layout, share card preview layout mirror correctly.

## 16. Analytics
Emit `story_favorited`, `story_unfavorited`, `story_share_gate_opened`, `story_share_completed` via `AnalyticsTracker`.

## 17. Performance
Optimistic favorite toggle must feel instant (<16ms UI response) — the network call happens asynchronously after the local state update, never blocking the tap response.

## 18. Security
- No share card/deep-link generation occurs before the Parent Gate resolves successfully — this is the feature's core child-safety control for this sub-feature and must have zero bypass path (verified by an explicit UI test asserting no network call to any share-related endpoint fires before gate success).
- No child-facing input surface for open comments exists anywhere in this module.

## 19. Testing
- Unit: optimistic-toggle-with-rollback-on-failure logic, withdrawn/restructured favorite resolution.
- UI: **mandatory security test** — assert zero share-related API call occurs before the Parent Gate resolves; cancel-at-gate leaves zero residual state.
- Accessibility: Favorites List item labeling, Share Gate focus management (gate modal traps focus appropriately).

## 20. AI Coding Agent Implementation Steps

**Task 01 — Add `FavoritesListRoute`**
Objective: Route registration. Follow: existing `Route` pattern. Definition of Done: route compiles.

**Task 02 — Implement `FavoriteRepository` with Optimistic Updates**
Objective: Immediate local state update, rollback-with-retry-affordance on API failure. Follow: `core-network` conventions. Tests: rollback test. Definition of Done: test passes.

**Task 03 — Implement `FavoritesViewModel` and `FavoritesListScreen`**
Objective: List rendering with withdrawn/restructured-content handling, empty state. Dependencies: Task 02. Tests: withdrawn-item-rendering test. Definition of Done: test passes.

**Task 04 — Locate and Wire the Existing Parent PIN/Biometric Gate Component**
Objective: Confirm the exact existing component from A.1/C.19 and integrate it into the share flow — do not build a new gate. Definition of Done: component identified and reused, documented in code comments for future maintainers.

**Task 05 — Implement `ShareFlowViewModel` with Gate-First Enforcement**
Objective: Zero share-related network activity before gate success. Dependencies: Task 04. Tests: mandatory security test per §19 (network-call-timing assertion). Definition of Done: security test passes.

**Task 06 — Implement `ShareStoryMomentGate` and `ApprovedShareCardPreview`**
Objective: Gate-triggering UI and post-gate share card preview screen. Dependencies: Task 05. Tests: cancel-leaves-zero-residual-state test. Definition of Done: test passes.

**Task 07 — Add Analytics Instrumentation**
Objective: Four events per §16. Tests: fake-tracker assertions. Definition of Done: exactly one call site per event.

**Task 08 — Full RTL and Accessibility Pass**
Objective: Verify mirroring and focus management. Tests: per §19. Definition of Done: baselines captured, focus-trap test passes.

**Task 09 — Add Full Test Suite**
Objective: Complete coverage per §19. Definition of Done: all green.

**Task 10 — Final Code Review**
Objective: Confirm the gate-before-any-share-network-call guarantee holds with zero exceptions anywhere in the code path; confirm no open comment/reaction input surface exists. Definition of Done: checklist in §21 checked.

## 21. Final Verification Checklist
- [ ] Favorite toggle is optimistic, instant, with rollback-and-retry on failure
- [ ] Withdrawn favorited content shows "no longer available", never a broken reference or crash
- [ ] Restructured/merged favorited content resolves to the new canonical ID transparently
- [ ] Zero share-related API call fires before the Parent PIN/Biometric Gate resolves successfully (mandatory security test)
- [ ] Cancel at the gate leaves zero residual share state
- [ ] No open comment/public-reaction input surface exists anywhere in this module
- [ ] All four analytics events fire correctly
- [ ] Full RTL mirroring verified

## 22. Definition of Done
Favorites are instant and resilient, and sharing is impossible without first clearing the existing Parent PIN/Biometric Gate — with zero bypass path, satisfying FR-13/FR-14's child-safety guarantees.
