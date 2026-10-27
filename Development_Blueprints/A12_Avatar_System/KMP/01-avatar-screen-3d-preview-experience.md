# K-01 — Avatar Screen & 3D Preview Experience

## 1. Feature Context
NoorHeroes KMP app (Android/iOS). Primary screen for Feature A.12 — Avatar System: the 3D avatar preview plus the segmented owned/locked items grid entry surface, reachable from Rewards Hub and the Profile tab's avatar thumbnail.

## 2. Parent Feature
A.12 Avatar System — KMP App (Android/iOS)

## 3. Sub-feature
K-01 Avatar Screen & 3D Preview Experience

## 4. Objective
Build the `AvatarScreen` Composable and `AvatarViewModel` rendering the 3D preview, owned-items grid, and locked-item teasers with full loading/offline/asset-failure states, backing FR-1, NFR Performance (screen load p95 < 1s), and Edge Cases 2, 7, 9.

## 5. Business Requirements
- Screen renders 3D avatar preview, owned-items grid (grouped by slot), and locked-item teasers in one unified browsing surface (FR-1).
- A new child always has a well-defined default equipped state in every slot — never a null/undefined slot render (Edge Case 2).
- Full reset on multi-child session switch — zero visual/data carryover between siblings sharing a device (Edge Case 7).
- Per-item asset load failure shows a graceful placeholder/retry, never a broken image or crash; 3D preview falls back to the last successfully-rendered equipped state (Edge Case 9).
- 3D preview has a screen-reader text-description fallback describing the currently-equipped look (NFR Accessibility).
- Screen load p95 < 1s on low-end Android (NFR Performance).

## 6. Existing Architecture
NoorHeroes KMP app: Clean Architecture, Compose Multiplatform UI, **Koin** for DI, **Ktor** for networking, **Room** (`BundledSQLiteDriver`) for local caching, navigation via the project's custom `Navigator`/`Route`/`NavigationAction` pattern, analytics via the `AnalyticsTracker` interface (`logEvent(name, params)`) — all per the conventions established by the A.7 Habit Tracker KMP blueprints (K-01), which corrected the PRD draft's Android-only Hilt/Retrofit/raw-NavController assumptions to the project's actual multiplatform stack. New feature module: `feature-avatar` (UI) + `feature-avatar-domain` (use cases), following the `feature-habits`/`feature-habits-domain` and `feature-learn`/`feature-learn-domain` naming convention. 3D rendering: the PRD's Android §6.1 specifies "Filament or a lightweight glTF-based renderer wrapped in `AndroidView`/Compose interop" — since this is genuinely new rendering capability with no existing project precedent (no other feature blueprint references 3D rendering), this sub-feature introduces a `Avatar3DRenderer` abstraction in `feature-avatar` wrapping the chosen engine behind a Compose-friendly interface, isolating the rest of the module from the specific rendering library choice.

## 7. Existing Code to Reuse
- `core-common` `di`/`error`/`result`/`datetime` packages
- `core-network` Ktor client setup
- `core-database` Room/`BundledSQLiteDriver` setup
- `core-navigation` `Navigator`/`Route` pattern
- `core-analytics` `AnalyticsTracker`
- `core-design-system` tokens (warm radial-glow staging environment per PRD §2.1, to be extended with avatar-specific tokens per Task 04 below)

## 8. Files to Create
- `feature-avatar/src/commonMain/kotlin/.../screen/AvatarScreen.kt` (Composable)
- `feature-avatar/src/commonMain/kotlin/.../screen/AvatarViewModel.kt`
- `feature-avatar/src/commonMain/kotlin/.../screen/AvatarUiState.kt`
- `feature-avatar/src/commonMain/kotlin/.../render/Avatar3DRenderer.kt` (expect/actual or interface + platform-specific glTF/Filament wrapper)
- `feature-avatar/src/androidMain/kotlin/.../render/Avatar3DRendererAndroid.kt`
- `feature-avatar/src/iosMain/kotlin/.../render/Avatar3DRendererIos.kt`
- `feature-avatar/src/commonMain/kotlin/.../data/InventoryRepository.kt`
- `feature-avatar-domain/src/commonMain/kotlin/.../GetChildInventoryUseCase.kt`
- `feature-avatar/src/commonTest/kotlin/.../AvatarViewModelTest.kt`
- `feature-avatar/src/androidInstrumentedTest/kotlin/.../AvatarScreenUiTest.kt`

## 9. Files to Modify
- App-level Koin module registration — wire `feature-avatar`/`feature-avatar-domain` DI graph
- `core-navigation` `Route` registry — add Avatar Screen route, reachable from Rewards Hub and Profile tab
- Multi-child session-switch handler (existing platform-wide session-isolation mechanism) — register `AvatarViewModel` state reset on child-switch, consistent with how other per-child screens already hook into this mechanism

## 10. Backend Requirements
Consumes `GET /v1/children/{id}/inventory` (B-01).

## 11. KMP Requirements
- `AvatarViewModel` exposes `StateFlow<AvatarUiState>` covering: `avatarBase`, `ownedItemsBySlot: Map<Slot, List<OwnedItem>>`, `lockedItems: List<LockedItem>`, `equippedBySlot: Map<Slot, ItemId>`, `loadState` (Loading/Default/Offline/Error).
- Default-equipped-state guarantee: `AvatarUiState` initialization never renders a slot with a null/undefined equipped value — if the backend response is somehow incomplete, the ViewModel falls back to a documented default rather than an undefined render (defensive client-side guard even though B-01 guarantees this server-side).
- 3D preview rotation via simple swipe/drag gesture on `Avatar3DRenderer`'s Compose wrapper, with a non-gesture rotation-arrow button alternative for accessibility.
- Per-item asset load failure: `Avatar3DRenderer` and grid item composables catch load failures independently, each falling back to its own placeholder/retry state without affecting sibling items or the overall screen.
- 3D preview accessibility fallback: a `contentDescription`/semantics property describing the current equipped combination in plain text (e.g., "Currently wearing: Garden Explorer outfit, Golden Glow").
- Tablet responsive layout: preview and grid side-by-side; mobile: preview-on-top/grid-below.
- Segmented/tabbed control for slot categories (Outfits/Glow/Accessories).

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
`GET /v1/children/{id}/inventory` (B-01).

## 14. Database Requirements (Local)
Room table `avatar_inventory_cache` mirroring the last-fetched inventory response (owned items, locked items, equipped state per slot) for offline/instant-load display — write path (equip/unequip outbox) is owned separately by K-06.

## 15. Validation
Unit test asserting `AvatarUiState`'s default-equipped-state fallback triggers correctly when fed a fixture response missing an equipped item in one slot (defensive-guard test, since this should be structurally impossible per B-01 but must be verified client-side too, per Edge Case 2's "never render an undefined equipped state" requirement).

## 16. Authentication
Reuses shared `core-network` Bearer token attachment (child-mode session).

## 17. Authorization
N/A at UI layer (enforced server-side, B-01).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Network failure on inventory load | Show cached `avatar_inventory_cache` with a small persistent offline indicator |
| Individual item asset fails to load | Per-item placeholder/retry state; rest of grid unaffected |
| 3D preview asset fails to load | Falls back to last successfully-rendered equipped state, never a broken/blank render |
| New child, no prior cache | Render default-equipped state from the fresh inventory response, no "empty" framing needed (every child starts with a base equipped look) |

## 19. Offline First
Last-synced inventory (owned items, equipped state) renders fully offline from `avatar_inventory_cache`; locked-item criteria display uses cached catalog data too (auto-unlock evaluation itself requires connectivity, but viewing/equipping owned items never blocks offline).

## 20. Local Data
```
Remote Data (GET /v1/children/{id}/inventory)
   ↓
InventoryRepository
   ↓
Room avatar_inventory_cache
   ↓
AvatarUiState (default-equipped-state guarded)
```

## 21. Localization
Item/base names and locked-item criteria descriptions resolved via backend-provided translation keys or pre-resolved strings (English, Hindi, Arabic, Urdu) — no hardcoded user-facing strings.

## 22. RTL
Segmented slot-category control and grid layout mirror correctly for RTL locales (Arabic/Urdu); verified via a dedicated RTL layout test. 3D preview staging itself (a centered radial-glow composition) is inherently direction-neutral.

## 23. Analytics
`avatar_screen_viewed` fired via `AnalyticsTracker.logEvent()` on screen entry.

## 24. Performance
Skeleton 3D-preview placeholder + grid shimmer during load; row/grid-item-scoped recomposition only (avoid whole-screen recomposition on a single item's asset-load-failure state change); screen load budget p95 < 1s on low-end Android — the 3D renderer must be lightweight per PRD §6.1's explicit low-end-device performance commitment.

## 25. Security
No new sensitive data handling at this layer.

## 26. Library Requirements
Compose Multiplatform, Koin, Ktor, Room (`BundledSQLiteDriver`), kotlinx-coroutines, a lightweight glTF/Filament-based 3D rendering library wrapped via `AndroidView`/UIKit interop.

## 27. Testing
- Unit: `AvatarViewModel`'s default-equipped-state fallback guard.
- Unit: multi-child session-switch triggers full state reset (no carryover from a previous child's `AvatarUiState`).
- UI: 3D preview accessibility fallback text renders and updates correctly for the current equipped state.
- UI: per-item asset-load-failure placeholder renders without affecting sibling grid items.
- UI: offline indicator renders when cached data is served without connectivity.
- Accessibility: rotation-arrow alternative reachable and functional without gesture input.

## 28. Documentation
KDoc on `AvatarViewModel` explaining the default-equipped-state defensive guard and its relationship to B-01's server-side guarantee (defense-in-depth, not redundant distrust).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Scaffold `feature-avatar`/`feature-avatar-domain` Modules**
- Objective: establish the new feature module pair.
- Why Required: no dedicated Avatar System module exists yet.
- Existing Architecture to Follow: `feature-habits`/`feature-habits-domain` module-pair convention (A.7 K-01).
- Files to Create: module `build.gradle.kts` files, package skeleton.
- Files to Modify: root `settings.gradle.kts`; Koin app-module registration.
- Dependencies: `core-common`, `core-network`, `core-database`, `core-design-system`, `core-navigation`, `core-analytics`.
- Definition of Done: modules compile and are wired into the app's DI graph.

**Task 02 — Implement `Avatar3DRenderer` Abstraction**
- Objective: platform-agnostic wrapper interface around the chosen glTF/Filament rendering library, exposed as a Compose-friendly composable.
- Why Required: no existing project precedent for 3D rendering; isolating the rendering-library choice behind an interface protects the rest of the module from a future library swap.
- Files to Create: `Avatar3DRenderer.kt` (common interface/expect), `Avatar3DRendererAndroid.kt`, `Avatar3DRendererIos.kt`
- Implementation Details: expose `render(equippedItems: EquippedState)`, `onLoadFailure` callback, rotation-gesture handling.
- Performance: lightweight asset loading, low-end-device budget per PRD §6.1.
- Tests: platform-specific smoke test that the renderer initializes without crashing given a fixture equipped state.
- Definition of Done: renderer displays a fixture avatar on both platforms.

**Task 03 — Implement `InventoryRepository` + `GetChildInventoryUseCase`**
- Objective: domain-layer read of the inventory, cached to Room.
- Existing Architecture to Follow: repository pattern from `core-data`/`CORE_DATA_INSTRUCTIONS.md`, mirroring `HabitRepository` (A.7 K-01).
- Files to Create: `InventoryRepository.kt`, `GetChildInventoryUseCase.kt`
- Implementation Details: Ktor call to `GET /v1/children/{id}/inventory`, cached to Room `avatar_inventory_cache`.
- Tests: repository unit tests (mocked Ktor client).
- Definition of Done: use case returns correctly-cached, correctly-mapped domain model, including default-equipped-state guard.

**Task 04 — Extend `core-design-system` with Avatar-Specific Tokens**
- Objective: warm radial-glow staging tokens, locked-item desaturated-silhouette tokens (shared with K-03), reusable as themed components.
- Files to Modify: `core-design-system` token definitions.
- Definition of Done: tokens available for reuse across K-01/K-02/K-03/K-05.

**Task 05 — Build `AvatarScreen` Composable**
- Objective: UI implementation of all documented states.
- Existing Files to Reuse: `core-design-system` tokens from Task 04.
- Files to Create: `AvatarScreen.kt`, `AvatarUiState.kt`
- Implementation Details: segmented slot control, owned/locked unified grid, tablet side-by-side layout, offline indicator, asset-failure placeholders.
- Localization/RTL: per §21/§22.
- Analytics: `avatar_screen_viewed` on screen entry.
- Tests: Compose UI tests for each documented state.
- Definition of Done: all documented states render correctly, accessibility labels verified.

**Task 06 — Implement `AvatarViewModel` with Default-State Guard**
- Objective: core ViewModel logic including the defensive default-equipped-state fallback.
- Files to Create: `AvatarViewModel.kt`
- Business Rules: Edge Case 2 (never undefined equipped state), Edge Case 7 (full reset on child switch).
- Tests: default-state-guard unit test; multi-child-switch reset unit test.
- Definition of Done: both tests pass.

**Task 07 — Wire Navigation & Multi-Child Session-Switch Hook**
- Files to Modify: `core-navigation` `Route` registry; existing session-isolation mechanism.
- Definition of Done: screen reachable via Rewards Hub and Profile tab; `AvatarViewModel` state confirmed reset on child switch via integration test.

**Task 08 — Final Code Review**
- Do Not Change: existing `core-design-system` tokens unrelated to Avatar; existing session-isolation mechanism's core logic (only register a new hook, don't rewrite it).
- Expected Result: PR merge-ready.

## 30. Definition of Done
Avatar Screen live with correct default-equipped-state guarantee, full multi-child session reset, all documented UI states, accessibility fallback, and full localization/RTL support, meeting the p95 < 1s load budget.

## 31. Final Verification Checklist
- [ ] `feature-avatar`/`feature-avatar-domain` modules scaffolded and DI-wired
- [ ] `Avatar3DRenderer` abstraction renders on both Android and iOS
- [ ] Default-equipped-state guard verified (never an undefined slot render)
- [ ] Multi-child session switch triggers full state reset (no carryover)
- [ ] Per-item asset-load-failure isolated to that item, 3D preview falls back gracefully
- [ ] 3D preview accessibility fallback text correct and updates with equipped state
- [ ] Rotation-arrow non-gesture alternative functional
- [ ] Localization (EN/HI/AR/UR) and RTL verified
- [ ] Analytics event wired via `AnalyticsTracker`
- [ ] Screen load performance meets p95 < 1s budget on low-end Android target
