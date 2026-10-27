# K-01 — Shared Favorite Toggle Component

## 1. Feature Context
Part of Feature B.14 Favorites. A single reusable Compose component embedded identically in Story Detail (A.3), Surah Learning (A.5), and Dua Learning (A.6) detail screens — one implementation, not three bespoke ones.

## 2. Parent Feature
B.14 Favorites (`PRD_Documents/Child App — Supporting (13-18)/Feature_B14_Favorites.md`)

## 3. Sub-feature
2.1 Shared Favorite Toggle Component — `K-01`

## 4. Objective
Implement `FavoriteToggleButton`, an optimistic, idempotent, offline-tolerant heart-icon toggle, shared across all three content-type detail screens via one component and one underlying repository call.

## 5. Business Requirements
- FR-5: idempotent, optimistic toggle — rapid taps never produce inconsistent state.
- §1.4: toggle latency p95 < 200ms (optimistic, near-instant).
- §2.1: filled/warm-gold when favorited, outlined when not, brief "pop" micro-animation.
- §7 Android AI Code-Generation Prompt items 1–2: `client_request_id` generated once per action and reused on retry; optimistic flip with rollback on rejection.

## 6. Existing Architecture
KMP shared module structure (`core-common`, `core-data`, `core-network`, `core-designsystem`, `core-auth`, feature modules referenced as `feature/stories`, `feature/dua-learning` etc. in existing blueprints). DI via Koin, constructor injection preferred, `koinInject()` in Compose. `NoorResult<T>` (`Outcome<T, AppError>`) is the standard return type. Analytics via `AnalyticsTracker.logEvent(name, params)`, injected into ViewModels. RTL handled via `Modifier.noorHeroesSafeArea()`.

**Resolved research finding — module placement is settled, but not in favor of `core-designsystem`:** `CORE_DESIGNSYSTEM_INSTRUCTIONS.md` §12 explicitly states core-designsystem "must never depend on any feature or domain module" and to "avoid adding icons or strings to this module unless they are truly global tokens." Since this component embeds domain logic (`content_id`/`content_type`, a repository call, offline queueing), it cannot live in `core-designsystem`. **Recommended module: a new `core-favorites` module**, following the same pattern as the existing `core-auth` module (a small, cross-cutting, non-designsystem module consumed by multiple feature modules) rather than `core-designsystem`. No doc defines a "lightweight shared client module" convention explicitly, so this is a recommendation for Android Architect sign-off, not an assumed fact — but it is grounded in the one hard constraint that *is* documented (§12's prohibition), which rules out the PRD's other suggested option.

**Resolved research finding — real consolidation target confirmed, not hypothetical:** `Development_Blueprints/A3_Stories_Module/KMP/08-story-favorites-parent-gated-sharing.md` already ships story-specific, non-parameterized files: `feature/stories/ui/FavoritesListScreen.kt`, `FavoritesViewModel.kt`, `FavoriteRepository.kt` — none of it framed as shared. Meanwhile `Development_Blueprints/A6_Dua_Learning/KMP/06-dua-favorites-management.md` explicitly *assumes* a shared, parameterized version of that component already exists ("Reuses A.3's shared Favorites List component, parameterized by `content_type=dua`") and even carries its own unresolved task to confirm that assumption. **Both must be superseded by K-01/K-02/K-03** — A.3's bespoke files retired in favor of this shared component, and A.6's blueprint corrected to point at the new `core-favorites` module once built, mirroring B-03's backend-side reconciliation.

## 7. Existing Code to Reuse
- `core-designsystem` icon/animation primitives (exact heart-icon asset TBD from Figma — not assumed here); domain logic itself does not belong in this module (see above)
- `core-data`'s `SyncQueueDao`/`SyncQueueEntity` (statuses `PENDING`/`IN_FLIGHT`/`FAILED`/`DEAD_LETTER`)
- `core-auth/SessionActivationRepository` — `activate(childId): Result<ChildSession>`, `currentSession: StateFlow<ChildSession?>` (confirmed via `C19_Parent_PIN_Biometric_Gate/KMP/05-session-activation-cross-profile-state-clearing.md` §8) — the active-child-session accessor this component's ViewModel should read from, rather than accepting a `child_id` parameter from the embedding screen
- `AnalyticsTracker` (existing, injected)
- `NoorResult<T>` / `Outcome<T, AppError>`
- Navigator/Route pattern is not directly relevant here (this is an inline toggle, not a navigation action)

## 8. Files to Create
- New `core-favorites` module (recommended location, see §6): `FavoriteToggleButton.kt` (Composable)
- `core-favorites/FavoriteToggleViewModel.kt` (or shared ViewModel-scoped utility per PRD §6.4)
- `core-favorites/FavoritesAnalytics.kt` (event-firing wrapper, per PRD §6.6)
- Unit tests: `FavoriteToggleViewModelTest.kt`

## 9. Files to Modify
- Story Detail screen (A.3), Surah Learning screen (A.5), Dua Learning screen (A.6) — embed `FavoriteToggleButton`
- **Confirmed removal targets:** `feature/stories/ui/FavoritesListScreen.kt`, `FavoritesViewModel.kt`, `FavoriteRepository.kt` (A.3's `08-story-favorites-parent-gated-sharing.md`) — these are real, already-specified bespoke files that must be retired/consolidated into this shared component, not a hypothetical risk
- `Development_Blueprints/A6_Dua_Learning/KMP/06-dua-favorites-management.md` — documentation correction, repoint its "reuse A.3's shared component" assumption at the new `core-favorites` module once built

## 10. Backend Requirements
None directly (consumes B-01 via K-03's repository).

## 11. KMP Requirements
- Heart icon renders filled (warm-gold) when favorited, outlined when not, with a brief pop micro-animation on toggle.
- Tap generates `client_request_id` (UUID) once per toggle action; the same id is reused if the request is retried, never regenerated.
- Optimistic update: icon flips immediately on tap, before server confirmation.
- Rollback: if the server rejects (inaccessible-content edge case), the icon reverts to its prior state.
- Offline: toggle queues into `SyncQueueDao` (`PENDING`), auto-flushed on reconnect via the existing `core-data` sync mechanism.
- Structurally embedded identically across all three content-type detail screens — no per-feature reimplementation.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
Consumes B-01 (`POST /v1/favorites`) via K-03's `FavoritesRepository.toggle()`. No direct network call from the Composable/ViewModel — always routed through the repository layer.

## 14. Database Requirements
Local: `SyncQueueDao`/`SyncQueueEntity` entry per queued offline toggle, keyed by `client_request_id`.

## 15. Validation
`content_id`/`content_type` passed in from the embedding screen's existing content context — no user input to validate at this component's boundary.

## 16. Authentication
Relies on the active child session already established by the app; no separate auth handling in this component.

## 17. Authorization
N/A at the UI layer — enforced server-side by B-01.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Network failure | Optimistic state retained, retried via `SyncQueue`, never surfaced as a child-facing error |
| Server rejects (inaccessible content) | Roll back icon to prior state, no error dialog (rare tampered-state edge case) |
| Rapid repeated taps | Idempotent — same `client_request_id` reused on retry, no duplicate network calls fired for the same logical action |

## 19. Offline First
Toggle queues locally when offline (optimistic update shown immediately), syncs via `SyncQueue` on reconnect, consistent with PRD §1.8 and Edge Case 5.

## 20. Local Data
`SyncQueueEntity` (offline outbox); no separate local favorite-state cache owned by this component (K-03 owns the broader cache).

## 21. Localization
Accessibility label/tooltip text ("Save"/"Remove from favorites") localized EN/HI/AR/UR — no other user-facing string in this component.

## 22. RTL
Icon placement and pop-animation direction must be RTL-safe via `Modifier.noorHeroesSafeArea()` or equivalent existing RTL-handling pattern.

## 23. Analytics
`favorite_added` / `favorite_removed`, both tagged with `content_type`/`content_id`, fired identically regardless of which detail screen embeds the component (PRD §1.19, §6.6).

## 24. Performance
Stable/immutable state parameters to prevent unnecessary recomposition on every parent screen recomposition; animation must not block the main thread; toggle latency p95 < 200ms is a UX target satisfied by the optimistic-update pattern itself (no network wait before visual feedback).

## 25. Security
No sensitive data handled. `client_request_id` is a random UUID, not a sensitive value.

## 26. Library Requirements
Koin, Compose animation APIs, existing `core-data` SyncQueue infrastructure. No new library introduced.

## 27. Testing
- Unit: `client_request_id` generated once, reused on retry (not regenerated) — per PRD §7 item 1.
- Unit: rollback-on-rejection sets icon back to prior state — per PRD §7 item 2.
- UI test: tap toggles icon state visually.
- UI test: rapid repeated taps produce one final consistent state, no duplicate outbox entries.

## 28. Documentation
Component-level KDoc explaining the shared-embedding contract (must be used identically by all three content types, not reimplemented).

## 29. AI Coding Agent Implementation Steps
**Task 01 — Create `core-favorites` Module.** Per §6's resolved recommendation (not `core-designsystem`, which is architecturally prohibited from holding domain logic) — get final Android Architect sign-off on the module name before wiring Gradle dependencies.
**Task 02 — Build `FavoriteToggleButton` Composable.** Filled/outline states, pop animation.
**Task 03 — Build `FavoriteToggleViewModel`.** Optimistic state, `client_request_id` generation/reuse logic.
**Task 04 — Wire to `FavoritesRepository.toggle()`.** Via K-03 (built in parallel or after — confirm sequencing; K-01 can stub the repository interface if K-03 isn't merged yet).
**Task 05 — Implement Rollback Logic.** On rejected server response.
**Task 06 — Implement Offline Queueing.** Via `SyncQueueDao`.
**Task 07 — Wire Analytics.** `FavoritesAnalytics` firing `favorite_added`/`favorite_removed`.
**Task 08 — Add Accessibility Labels.** Localized, screen-reader operable.
**Task 09 — Embed in All Three Detail Screens and Retire Legacy Files.** Story Detail, Surah Learning, Dua Learning — remove A.3's `FavoritesListScreen.kt`/`FavoritesViewModel.kt`/`FavoriteRepository.kt` (confirmed bespoke, per §9) and correct A.6's `06-dua-favorites-management.md` blueprint reference.
**Task 10 — Write Tests.** Per §27.
**Task 11 — Final Code Review.** Confirm no per-feature duplicate toggle logic remains.

## 30. Definition of Done
Component renders and toggles correctly in all three embedding contexts from one shared implementation; `client_request_id` reuse test green; rollback test green; offline-queue test green; analytics events verified identical across all three screens.

## 31. Final Verification Checklist
- [ ] One shared component, no per-feature duplication
- [ ] `client_request_id` generated once, reused on retry
- [ ] Optimistic update + rollback-on-rejection verified
- [ ] Offline queueing via `SyncQueue` verified
- [ ] Analytics events consistent across all three embedding screens
- [ ] Accessibility labels localized and screen-reader operable
- [ ] RTL-safe rendering verified
