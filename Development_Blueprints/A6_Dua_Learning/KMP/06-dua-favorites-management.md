# K-06 — Dua Favorites Management

## 1. Feature Context
NoorHeroes — Feature A.6 Dua Learning. **Scope correction:** `B14_Favorites/KMP/01-shared-favorite-toggle-component.md`, `02-favorites-tab-grid-type-filter.md`, and `03-favorites-repository-offline-sync-layer.md` already implement a shared favorite-toggle component, a shared type-filterable Favorites tab/grid, and a shared offline-sync repository layer. This file integrates with those, matching B-04's backend-side finding that B.14 already owns favoriting end-to-end.

## 2. Parent Feature
A.6 Dua Learning

## 3. Sub-feature
K-06 — Dua Favorites Management (integration with B.14's shared components)

## 4. Objective
Ensure duas are correctly favoritable via B.14's shared toggle component and correctly discoverable via B.14's shared Favorites tab (type-filtered to `dua`), without building a parallel favorites list or toggle button.

## 5. Business Requirements
FR-8; Edge Case 1, Edge Case 9 — all owned by B.14's shared implementation.

## 6. Existing Architecture
`B14_Favorites/KMP/01`'s shared toggle component (used identically by A.3/A.5/A.6 detail screens), `02`'s type-filterable Favorites tab, `03`'s offline-sync repository layer (built on `SyncQueueDao`/`SyncQueueEntity`, consistent with K-07's real offline mechanism).

## 7. Existing Code to Reuse
- B14-K01's shared favorite-toggle composable — mounted in `DuaCardDetailScreen` (K-02), not rebuilt
- B14-K02's shared Favorites tab, filtered by `content_type=dua`
- B14-K03's `FavoritesRepository` offline-sync layer

## 8. Files to Create
- `feature/dua/src/androidUiTest/kotlin/.../DuaFavoritesIntegrationTest.kt` — confirms duas correctly appear in B.14's shared Favorites tab when filtered

## 9. Files to Modify
- `DuaCardDetailScreen.kt` (K-02) — mount B14-K01's shared toggle component with `content_type="dua"`, rather than a locally-built heart icon

## 10. Backend Requirements
Consumes B-04's `DuaAccessChecker` registration (backend-side, already covered in B-04).

## 11. KMP Requirements
- Mount B14-K01's shared toggle on the Dua Card and any dua list item
- Rely on B14-K02's shared Favorites tab for the dua-filtered favorites view — dua's own navigation entry to "Favorites" should route into that shared tab pre-filtered to `dua`, not a locally-built screen
- Withdrawn-favorited-dua handling ("temporarily unavailable") — confirm this is already generic in B14-K02 (likely, since it's the same shape of problem for Stories/Quran/Dua) before adding dua-specific handling

## 12. NextJS Requirements
N/A.

## 13. API Contract
Per B14-B01 §13.

## 14. Database Requirements
None dua-specific — B14-K03's shared offline-sync layer owns local favorite caching.

## 15. Validation
N/A directly.

## 16. Authentication / 17. Authorization
Inherited from B.14's shared components.

## 18. Error Handling
Inherited from B.14's shared toggle/tab — no dua-specific error handling needed unless a gap is found.

## 19. Offline First
Delegated entirely to B14-K03's `FavoritesRepository` offline-sync layer.

## 20. Local Data
Owned by B14-K03.

## 21. Localization / 22. RTL
Inherited from B.14's shared components.

## 23. Analytics
`dua_favorited`/`dua_unfavorited` — confirm whether B14-K01's shared toggle already emits a generic `favorite_toggled` event with `content_type` as a parameter, which may supersede dua-specific event names (align naming with whatever the platform's real analytics taxonomy turns out to be, per `CORE_ANALYTICS_INSTRUCTIONS.md`'s `AnalyticsTracker`).

## 24. Performance
Inherited from B.14's shared components (already handles list virtualization etc.).

## 25. Security
N/A directly.

## 26. Library Requirements
B.14's shared favorites module dependency only.

## 27. Testing
- Integration: favorite a dua via B14-K01's shared toggle → confirm it appears correctly in B14-K02's shared Favorites tab when filtered to `dua`
- Integration: withdraw a favorited dua → confirm B14-K02's existing unavailable-state handling covers it correctly

## 28. Documentation
Record that no local favorites screen/toggle was built — reuse only, matching B-04's backend-side pattern.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Mount Shared Toggle on Dua Card**
Task ID: K-06-T01. Files to Modify: `DuaCardDetailScreen.kt`. Existing Files to Reuse: B14-K01's shared toggle component. Definition of Done: toggle correctly calls B14's real `POST /v1/favorites` with `content_type="dua"`.

**Task 02 — Verify Dua Discoverability in Shared Favorites Tab**
Task ID: K-06-T02. Objective: confirm B14-K02's tab correctly lists/filters dua favorites without any dua-specific code changes needed on that shared component. Definition of Done: integration test passes against the real shared tab.

**Task 03 — Verify Withdrawn-State Handling**
Task ID: K-06-T03. Definition of Done: confirmed generic (or, if genuinely dua-specific, a minimal addition coordinated with B.14's owner).

**Task 04 — Add Tests**
Task ID: K-06-T04. Files to Create: `DuaFavoritesIntegrationTest.kt`. Definition of Done: all §27 scenarios green.

**Task 05 — Add Documentation**
Task ID: K-06-T05. Definition of Done: reuse-only note recorded.

**Task 06 — Final Code Review**
Task ID: K-06-T06. Definition of Done: §31 checklist fully checked; confirm no local favorites list/toggle exists in `feature/dua/`.

## 30. Definition of Done
Duas fully favoritable and discoverable entirely through B.14's shared components, with zero duplicate favorites UI in `feature/dua/`.

## 31. Final Verification Checklist
- [ ] No local favorites list screen built — B14-K02's shared tab reused
- [ ] No local favorite toggle built — B14-K01's shared component reused
- [ ] Dua favorites correctly appear when filtering the shared tab to `content_type=dua`
- [ ] Withdrawn-favorite handling confirmed generic or coordinated, not duplicated

## 32. Addendum — What Changed From the Original Draft
The original draft built a dua-specific Favorites List screen wrapper and toggle logic. The real, already-existing `B14_Favorites/KMP/01–03` blueprints provide a fully shared, cross-feature toggle component, filterable Favorites tab, and offline-sync repository — this file's entire scope is now "mount the shared components correctly," matching the same reuse-only pattern established for badge celebration (K-04) and the backend-side favorites coordination (B-04).
