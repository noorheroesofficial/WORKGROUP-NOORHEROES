# K-02 — Favorites Tab: Saved Item Grid & Type Filter

## 1. Feature Context
Part of Feature B.14 Favorites. Owns the Favorites tab's content within the shared "Favorites & Downloads" screen shell (shell itself owned by B.15) — the grid, type filter, and per-item states.

## 2. Parent Feature
B.14 Favorites (`PRD_Documents/Child App — Supporting (13-18)/Feature_B14_Favorites.md`)

## 3. Sub-feature
2.2 Favorites Tab — Saved Item Grid & Type Filter — `K-02`

## 4. Objective
Render the child's saved-item grid with type filtering, reusing the established browse-grid visual language from B.13 Search Results and A.3 Stories Library, handling loading/empty/offline/unavailable states gracefully.

## 5. Business Requirements
- FR-1: saved-item grid + type filter.
- FR-2: open item, remove from favorites.
- FR-7: "no longer available" state for withdrawn content, no broken link.
- FR-8: type filtering with B.13's shared iconography.
- Edge Case 4: graceful pagination for large lists, no hard cap.
- §1.18 Screen Inventory items 2, 3, 5, 6, 7.

## 6. Existing Architecture
Compose screen within the shared tabbed shell (co-owned with B.15). Visual grid pattern already established for B.13 Search Results (`02-text-search-query-results-experience.md`) and A.3 Stories Library (`01-stories-library-category-discovery.md`) — this screen must reuse that grid component, not reimplement it.

**Resolved research finding — a real, pre-existing favorites-specific screen must be superseded here, not just the generic grid pattern reused:** A.3's `08-story-favorites-parent-gated-sharing.md` already built `feature/stories/ui/FavoritesListScreen.kt` (story-specific, not generic). This K-02 screen is the canonical replacement for it going forward — do not leave both in place. A.6's `06-dua-favorites-management.md` assumed a shared/parameterized version of that screen already existed; once K-02 ships, correct that blueprint's reference to point here.

## 7. Existing Code to Reuse
- Grid/card component from B.13 Search Results and/or A.3 Stories Library (confirm single canonical shared grid component before building a third copy)
- Type-filter chip component from B.13 (`02-text-search-query-results-experience.md`)
- `FavoriteToggleButton` (K-01) — reused inline on each grid card for the remove action
- Skeleton/shimmer loading component (existing design system pattern)
- `core-auth/SessionActivationRepository.currentSession` (`StateFlow<ChildSession?>`) — for re-subscribing correctly on session switch, coordinated with K-04

## 8. Files to Create
- `FavoritesTabScreen.kt` (Composable, within the shared `FavoritesAndDownloadsScreen` shell)
- `FavoritesTabViewModel.kt`
- `FavoritesTabState.kt` / `FavoritesTabEvent.kt`
- UI tests: `FavoritesTabScreenTest.kt`

## 9. Files to Modify
- `FavoritesAndDownloadsScreen.kt` (shell, co-owned with B.15) — register the Favorites tab content
- Remove `feature/stories/ui/FavoritesListScreen.kt` (A.3's superseded bespoke screen, confirmed via §6) once this screen is live
- `Development_Blueprints/A6_Dua_Learning/KMP/06-dua-favorites-management.md` — documentation correction, repoint at this screen

## 10. Backend Requirements
None directly (consumes B-02 via K-03).

## 11. KMP Requirements
- 2-column grid mobile, 3–4 column tablet.
- Type-filter chip row: All/Stories/Surahs/Duas.
- Remove-from-favorites directly on the card (long-press or inline heart) — no forced navigation into the detail screen.
- Tap card → navigate to content-type-appropriate detail screen (deep link dispatch).
- Skeleton shimmer while loading.
- Empty state: "Tap the heart on any story, surah, or dua to save it here."
- Per-item "no longer available" state — no navigation attempt on tap of such an item.
- Fully functional offline from cache.
- Reset completely on child-session switch (delegates isolation guarantee to K-04).

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
Consumes B-02 (`GET /v1/children/{id}/favorites?type=`) via `FavoritesRepository.getFavorites(type)` (K-03). No direct network call from this screen/ViewModel.

## 14. Database Requirements
Reads from local cache populated by K-03 (offline-first).

## 15. Validation
Type filter selection is a closed set (All/Stories/Surahs/Duas) — no free-text input to validate.

## 16. Authentication
Relies on active child session (enforced upstream by K-03/K-04).

## 17. Authorization
N/A at this screen's layer — enforced server-side by B-02 and structurally by K-03/K-04's session-derivation guarantee.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Fetch failure | Render cached last-known list with a staleness indicator, never a blank/broken screen |
| Withdrawn item tapped | Inline "no longer available" explanation, no navigation attempt |
| Empty list | Friendly guided empty state, not an error |
| Offline | Fully render from cache, no error banner |

## 19. Offline First
Grid renders fully from cache when offline (PRD §1.14); no network call blocks initial render.

## 20. Local Data
Consumes K-03's local cache; this screen owns no direct persistence of its own.

## 21. Localization
All copy (filter labels, empty-state text, "no longer available" text) localized EN/HI/AR/UR — no hardcoded user-facing strings.

## 22. RTL
Grid mirrors correctly in RTL layout (Arabic/Urdu), consistent with B.13/A.3's existing RTL-tested grid pattern.

## 23. Analytics
`favorites_tab_viewed`, `favorites_type_filter_applied`, `favorite_item_opened`, `favorite_item_unavailable_shown`, `favorites_offline_state_shown` (PRD §1.19).

## 24. Performance
Lazy-loading/pagination for large favorites lists (Edge Case 4) — no hard cap by design, so the grid must scale gracefully rather than degrade. Avoid unnecessary recomposition on filter changes by keying grid items stably (`content_id`+`content_type`).

## 25. Security
No sensitive data rendered beyond the child's own favorited content metadata (title, thumbnail) — already scoped server-side by B-02.

## 26. Library Requirements
Existing Compose + design-system grid/chip components; no new library.

## 27. Testing
- Unit: filter logic (All/Stories/Surahs/Duas scoping).
- Unit: empty/offline/unavailable state selection logic.
- UI test: tapping an `available:false` item shows the inline state and fires no navigation event (PRD §7 item 3).
- UI test: type filter correctly narrows the rendered grid.
- Integration: full add (from any of the three content types) → tab reflects it → remove flow.

## 28. Documentation
Screen-level KDoc noting the shared-shell coordination point with B.15.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Confirm Shared Shell Contract with B.15.** Tab registration API/interface for `FavoritesAndDownloadsScreen` — do not build a standalone shell here if B.15 already owns it (confirm current B.15 build status before proceeding).
**Task 02 — Build `FavoritesTabScreen` Composable.** Grid + filter chip row.
**Task 03 — Build `FavoritesTabViewModel`.** State/Event handling, wired to `FavoritesRepository.getFavorites()`.
**Task 04 — Implement Loading/Empty/Offline/Unavailable States.**
**Task 05 — Embed `FavoriteToggleButton` (K-01) on Each Card.** For the inline remove action.
**Task 06 — Implement Card-Tap Navigation.** Deep link dispatch by `content_type`, gated on `available:true`.
**Task 07 — Wire Analytics.** Per §23.
**Task 08 — Localize All Copy.** EN/HI/AR/UR, RTL-verified.
**Task 09 — Write Tests.** Per §27.
**Task 10 — Final Code Review.** Confirm grid component is reused, not reimplemented, from B.13/A.3.

## 30. Definition of Done
Grid renders correctly across all states (loading/empty/offline/unavailable/populated); no-navigation-on-unavailable-tap test green; filter test green; analytics events verified; RTL rendering verified.

## 31. Final Verification Checklist
- [ ] Grid/card component reused from B.13/A.3, not duplicated
- [ ] Type filter functions correctly
- [ ] Unavailable items show inline state with no navigation
- [ ] Offline rendering fully functional from cache
- [ ] All copy localized, RTL-verified
- [ ] Analytics events fire correctly
- [ ] Pagination/lazy-load verified for large lists
