# K-03 — Locked Item Detail & Unlock Criteria Flow

## 1. Feature Context
NoorHeroes KMP app (Android/iOS). Part of Feature A.12 — Avatar System. Implements the locked-item teaser and Locked Item Detail screen: transparent unlock-criteria display, non-committal preview, and direct navigation to the unlocking activity.

## 2. Parent Feature
A.12 Avatar System — KMP App (Android/iOS)

## 3. Sub-feature
K-03 Locked Item Detail & Unlock Criteria Flow

## 4. Objective
Build the locked-item teaser component and Locked Item Detail screen rendering server-resolved unlock criteria, a non-committal preview action, and a direct deep link to the unlocking activity, backing FR-2, FR-7, and Edge Cases 3, 5.

## 5. Business Requirements
- Locked items display specific unlock criteria text (e.g., "7-day streak"), never a generic lock icon with no explanation (FR-7).
- Locked-item visual language is a soft greyscale/desaturated silhouette — never a harsh blackout or "?" mystery-box treatment, which could imply gacha-style randomness contrary to the platform's anti-loot-box principle (PRD §2.1).
- Criteria text is always visible beneath the item, not hidden behind an additional tap (PRD §2.1).
- Locked Item Detail offers a "Preview" action (non-committal try-on) with zero persistent side effects — closing without equipping leaves the actually-equipped state unchanged (Edge Case 5).
- Locked Item Detail offers a "Go to [Activity]" action deep-linking directly to the relevant unlocking feature (FR-2).
- A locked item whose criteria reference a deprecated badge/level gracefully shows "currently unavailable to unlock" rather than a broken reference (Edge Case 3).
- Criteria text is rendered exclusively from the server-provided `unlock_rule_description` string — the client never parses or renders raw JSON (mirrors B-01's server-resolution guarantee).

## 6. Existing Architecture
Extends `feature-avatar`/`feature-avatar-domain` established in K-01/K-02. Locked-content transparency principle established in A.3/A.5 (per PRD §2 header note) — this sub-feature follows the same "always show the specific criteria, never a mystery lock" pattern already used for Story episode unlocks (A.3) and Quran skill-tree node unlocks (A.5). Deep-link routing follows the project's existing `noorheroes://` scheme handler (per `core-navigation`'s deep-link dispatch, already used by A.7 K-01's `noorheroes://habits` target).

## 7. Existing Code to Reuse
- `AvatarViewModel`/`AvatarUiState` (K-01) — `lockedItems` list already sourced here
- `core-navigation` `Navigator`/deep-link dispatch pattern
- `core-design-system` locked-item desaturated-silhouette tokens (established in K-01 Task 04)
- `core-analytics` `AnalyticsTracker`

## 8. Files to Create
- `feature-avatar/src/commonMain/kotlin/.../locked/LockedItemTeaser.kt` (Composable)
- `feature-avatar/src/commonMain/kotlin/.../locked/LockedItemDetailScreen.kt` (Composable)
- `feature-avatar/src/commonMain/kotlin/.../locked/LockedItemDetailViewModel.kt`
- `feature-avatar/src/commonTest/kotlin/.../LockedItemPreviewNoPersistenceTest.kt`
- `feature-avatar/src/androidInstrumentedTest/kotlin/.../LockedItemCriteriaTextUiTest.kt`

## 9. Files to Modify
- `core-navigation` `Route` registry — add Locked Item Detail route, parameterized by `itemId`

## 10. Backend Requirements
Consumes `unlock_rule_description`/`unlock_rule_available` fields already present in `GET /v1/children/{id}/inventory`'s `locked_items` array (B-01) — no new backend call.

## 11. KMP Requirements
- `LockedItemTeaser` renders the item's desaturated silhouette, name, and `unlock_rule_description` text directly beneath — never behind a second tap.
- `LockedItemDetailScreen` shows the full criteria, a "Preview" button, and a "Go to [Activity]" primary button.
- "Preview" action: temporarily renders the previewed item in K-01's `Avatar3DRenderer` via a local-only, non-persisted UI state flag (`previewedItemId: ItemId?` in `AvatarUiState` or a scoped child state) — this flag is never written to `avatar_inventory_cache` or sent to the server; on screen dismiss, the preview flag is cleared and the actually-equipped state (from K-02) renders again.
- "Go to [Activity]" resolves a deep-link target from the item's `unlock_rule` type (badge → relevant feature, level → relevant feature, habit-milestone → `noorheroes://habits` per A.7's established target) and navigates via `Navigator`.
- `unlock_rule_available: false` renders a distinct "currently unavailable to unlock" visual variant instead of the standard criteria text, without blocking the rest of the screen (Edge Case 3).
- Criteria text rendering must never attempt to parse the string as JSON or apply any client-side interpretation — it is treated as an opaque, already-localized display string.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
No new endpoint; consumes `locked_items[].unlock_rule_description`, `.unlock_rule_available` already present in B-01's `GET /v1/children/{id}/inventory` response.

## 14. Database Requirements (Local)
No new local table; locked-item data is part of the same `avatar_inventory_cache` (K-01) already caching the full inventory response.

## 15. Validation
Unit test asserting the "Preview" action produces zero persistent state change — after previewing an item and then dismissing without equipping, re-reading `AvatarUiState.equippedBySlot` must exactly match its pre-preview value (Edge Case 5, mandatory).

## 16. Authentication
Reuses shared `core-network` Bearer token attachment (inherited from K-01's already-authenticated inventory fetch; no separate auth call here).

## 17. Authorization
N/A at UI layer.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| `unlock_rule_available: false` | "Currently unavailable to unlock" variant rendered gracefully, rest of screen unaffected |
| Deep-link target for "Go to [Activity]" fails to resolve (unknown/removed feature route) | Standard deep-link fallback (existing platform-wide deep-link error handling, not re-implemented here) |
| Preview action attempted on an already-equipped item's slot | Preview simply shows the target item in place of the current one temporarily; no error, treated as a normal preview |

## 19. Offline First
Locked-item criteria display uses cached catalog data (`avatar_inventory_cache`, K-01) and works fully offline; only the "Go to [Activity]" deep-link's destination feature may itself require connectivity, which is that destination feature's own concern, not this sub-feature's.

## 20. Local Data
Reads directly from `AvatarUiState.lockedItems` (populated by K-01's `InventoryRepository`); no separate local write path for this sub-feature beyond the transient, non-persisted `previewedItemId` flag.

## 21. Localization
`unlock_rule_description` and "currently unavailable to unlock" copy resolved via backend-provided translation keys / pre-resolved strings (English, Hindi, Arabic, Urdu).

## 22. RTL
Locked Item Detail layout (illustration, criteria text, action buttons) mirrors correctly for RTL locales; verified via a dedicated RTL layout test.

## 23. Analytics
`avatar_locked_item_viewed`, `avatar_locked_item_previewed`, `avatar_locked_item_unlock_activity_navigated` fired via `AnalyticsTracker.logEvent()`.

## 24. Performance
Locked-item grid rendering uses the same item/slot-scoped recomposition discipline as K-02's owned-items grid; preview toggling re-renders only the 3D preview component, not the full screen.

## 25. Security
No new sensitive data handling; criteria text is treated as an opaque server-provided string, never executed/parsed/evaluated client-side (defense against any theoretical injection via a compromised criteria string).

## 26. Library Requirements
Compose Multiplatform, Koin, `core-navigation`'s deep-link dispatcher.

## 27. Testing
- Unit (P0): preview action has zero persistent side effects — assert `equippedBySlot` unchanged after preview-then-dismiss.
- UI (P0): regex assertion that the displayed criteria text never contains raw JSON-like patterns (curly braces, quoted keys) — confirms exclusive reliance on the server-resolved description string.
- UI: "currently unavailable to unlock" variant renders correctly for a fixture item with `unlock_rule_available: false`.
- Integration: "Go to [Activity]" navigates to the correct deep-link target for each of the three unlock-rule types (badge/level/habit-milestone).

## 28. Documentation
KDoc on `LockedItemDetailViewModel` explaining the non-persistence guarantee of the preview flag and its explicit separation from K-02's equipped-state model.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Build `LockedItemTeaser` Composable**
- Objective: grid-embeddable desaturated-silhouette teaser with always-visible criteria text.
- Existing Files to Reuse: `core-design-system` locked-item tokens (K-01 Task 04).
- Files to Create: `LockedItemTeaser.kt`
- Implementation Details: criteria text directly beneath item, no additional-tap requirement.
- Localization/RTL: per §21/§22.
- Tests: UI test confirming criteria text visibility without interaction.
- Definition of Done: teaser renders correctly within K-01's grid.

**Task 02 — Implement `LockedItemDetailViewModel` with Non-Persistent Preview**
- Objective: preview-state management guaranteeing zero persistence.
- Files to Create: `LockedItemDetailViewModel.kt`
- Implementation Details: `previewedItemId` held in a scoped, screen-local state only, never written to `AvatarUiState.equippedBySlot` or any repository/cache.
- Tests (P0): preview-then-dismiss non-persistence test.
- Do Not Change: do not route preview actions through `EquipItemUseCase` (K-02) under any circumstance — this would violate the non-persistence guarantee.
- Definition of Done: P0 test passes.

**Task 03 — Build `LockedItemDetailScreen` Composable**
- Objective: full detail screen with criteria, Preview, and "Go to [Activity]" actions.
- Files to Create: `LockedItemDetailScreen.kt`
- Implementation Details: deep-link resolution per unlock-rule type; "currently unavailable" variant handling.
- Localization/RTL: per §21/§22.
- Analytics: `avatar_locked_item_viewed`, `avatar_locked_item_previewed`, `avatar_locked_item_unlock_activity_navigated`.
- Tests: JSON-pattern-absence regex UI test (P0); deep-link navigation integration tests.
- Definition of Done: screen renders and navigates correctly for all fixture unlock-rule types.

**Task 04 — Wire Navigation Route**
- Files to Modify: `core-navigation` `Route` registry.
- Definition of Done: Locked Item Detail reachable from `LockedItemTeaser` tap, parameterized correctly by `itemId`.

**Task 05 — Final Code Review**
- Do Not Change: K-02's `EquipItemUseCase`/equipped-state model (preview must remain fully isolated from it).
- Expected Result: PR merge-ready.

## 30. Definition of Done
Locked-item teasers and detail screen live, always showing specific unlock criteria, with a verifiably non-persistent preview action and correct deep-link navigation to the unlocking activity for all three unlock-rule types.

## 31. Final Verification Checklist
- [ ] Criteria text always visible beneath teaser, never hidden behind an extra tap
- [ ] Preview action verified to have zero persistent side effects (P0 test passing)
- [ ] Criteria text never rendered from raw JSON (regex UI test passing, P0)
- [ ] "Currently unavailable to unlock" variant renders correctly for deprecated references
- [ ] "Go to [Activity]" correctly deep-links for badge/level/habit-milestone rule types
- [ ] Localization (EN/HI/AR/UR) and RTL verified
- [ ] Analytics events wired via `AnalyticsTracker`
- [ ] Preview state fully isolated from K-02's equipped-state model
