# Blueprint: Notifications Inbox Screen & Read-State Sync

## 1. Feature Context
Platform: NoorHeroes KMP App (Kotlin Multiplatform, Compose, Android/iOS). New module `:feature:parent-notifications-support`, depends on `:core:notifications` (B.17's shared module — reused, not forked), `:core:auth`, `:core:design-system`, `:core:network`, `:core:database`. This blueprint delivers the Notifications Inbox screen shell that K-02 through K-04 sit alongside within the same feature module.

## 2. Parent Feature
C.25 — Notifications (Parent) & Support.

## 3. Sub-feature
K-01 — Notifications Inbox Screen & Read-State Sync.

## 4. Objective
Build `NotificationsInboxScreen` (Compose) and `NotificationsInboxViewModel`, offline-first over a local cache with staleness indication, wired to B-01's API, and routing every notification tap through `:core:notifications`'s existing `DeepLinkResolutionHandler` — never a separate parent-specific deep-link path.

## 5. Business Requirements
Source: PRD §6.1–§6.3, §6.5, §6.7–§6.8; §1.10 Edge Case 6; §1.11 Error Handling; §1.12–§1.13 Empty/Loading States; §1.19 Events.
- `NotificationsInboxScreen` shows read/unread state (bold vs. regular, small dot indicator) and category-icon badges (system/safety/marketing), consistent with recognizable inbox UX conventions (§2.1).
- Filter chips: All/System/Safety/Marketing.
- Offline: renders from cache with a staleness indicator; mark-as-read actions taken offline queue and sync on reconnect (Edge Case 6, §1.14).
- Deep-link taps reuse `:core:notifications`'s existing `DeepLinkResolutionHandler` (B.17 §6.3) — this feature does **not** implement a separate, weaker deep-link path (FR-12).
- Reached from the Parent Dashboard's bell icon and push-notification taps (§6.3), and Settings.

## 6. Existing Architecture
Per `CORE_NOTIFICATIONS_INSTRUCTIONS.md`: `NotificationHandler` interface is the sole abstraction for push token/payload handling — this blueprint does **not** touch that interface; it consumes notification *history* via a REST repository, a distinct concern from `core-notifications`'s push-delivery abstraction. Per `CORE_DATA_INSTRUCTIONS.md`/`CORE_COMMON_INSTRUCTIONS.md` (referenced pattern, not re-read this pass — confirm exact API names before implementation): `NoorResult<T>` standard fallible-operation wrapper, `DispatcherProvider` for coroutine dispatching, `Route` sealed interface with `requiredAuthState`/`analyticsName`, `BaseViewModel` base class with `navigator: Lazy<Navigator>`. Per C.20's K-01 (`ParentDashboardViewModel`) precedent: derive `familyId`/parent session exclusively from `:core:auth`'s `AuthStateProvider` — never accept it as an external parameter.

## 7. Existing Code to Reuse
- `AuthStateProvider`/`AuthRepository` (`:core:auth`) for deriving the active parent session — never accept `family_id`/`parent_id` as a constructor or method parameter.
- `NoorResult<T>` for all repository calls.
- `DeepLinkResolutionHandler` (`:core:notifications`, B.17 §6.3) — reused as-is for every notification tap.
- `BaseViewModel`, `Route` pattern, `Navigator` (`:core:navigation`).
- Design tokens and Parent-Mode formal visual register (`:core:design-system`, established in C.19 §2.1).
- Room (local persistence) per platform's offline-first repository convention, mirroring C.20's K-07 caching approach.

## 8. Files to Create
- `feature/parent-notifications-support/src/commonMain/kotlin/.../NotificationsInboxRoute.kt`
- `feature/parent-notifications-support/src/commonMain/kotlin/.../NotificationsInboxScreen.kt`
- `feature/parent-notifications-support/src/commonMain/kotlin/.../NotificationsInboxViewModel.kt`
- `feature/parent-notifications-support/src/commonMain/kotlin/.../NotificationsInboxUiState.kt`
- `feature/parent-notifications-support/src/commonMain/kotlin/.../NotificationsRepository.kt` (interface)
- `feature/parent-notifications-support/src/commonMain/kotlin/.../local/NotificationCacheDao.kt` (Room DAO interface/actual per platform's KMP-SQLite convention)
- `feature/parent-notifications-support/src/commonMain/kotlin/.../di/ParentNotificationsSupportModule.kt` (Koin module — shared root for K-01 through K-04)
- `feature/parent-notifications-support/src/commonTest/kotlin/.../NotificationsInboxViewModelTest.kt`
- `feature/parent-notifications-support/src/commonTest/kotlin/.../NotificationsRepositoryFamilyScopeStructuralTest.kt`

## 9. Files to Modify
- App-level Koin DI root registration — include `ParentNotificationsSupportModule`.
- Navigation graph registration — register `NotificationsInboxRoute`.
- Parent Dashboard's bell icon (C.20's `ParentDashboardScreen`) — wire navigation to `NotificationsInboxRoute` (coordinate with C.20's module shortcut grid if not already wired).

## 10. KMP Requirements
- `Route`: `@Serializable data object NotificationsInboxRoute : Route { override val requiredAuthState = /* confirm exact parent-authenticated BaseAuthState subclass before hardcoding, per C.20 K-01's same caveat */; override val analyticsName = "parent_notifications_inbox" }`.
- `NotificationsInboxUiState`: `filter: NotificationFilter` (All/System/Safety/Marketing), `items: List<NotificationItemState>` (each carrying `id`, `type`, `title`, `read`, `deepLink`, `occurredAt`), `isStale: Boolean`, `loadState: sealed interface { Loading; Content; Error(val error: AppError) }` — all `@Immutable`/`@Stable` per `core-common`'s modeling convention.
- `NotificationsInboxViewModel(notificationsRepository: NotificationsRepository, authStateProvider: AuthStateProvider, dispatchers: DispatcherProvider, deepLinkResolutionHandler: DeepLinkResolutionHandler) : BaseViewModel()`.
- On init: derive parent session from `authStateProvider`; load cached items immediately (fast path), then trigger a network refresh; on refresh success, update cache and clear `isStale`; on refresh failure, keep cached items with `isStale = true`.
- Filter changes re-query the local cache synchronously (no network round-trip needed for filtering already-fetched data) — but reduce to a `type` query param on the next network refresh so server-side filtering remains available for large histories.
- `markRead(id)`: optimistic local update immediately; if online, calls `NotificationsRepository.markRead(id)`; if offline, enqueues the action (e.g., via a local outbox/queue table) for sync on reconnect.
- `onNotificationTapped(item)`: delegates to `deepLinkResolutionHandler.resolve(item.deepLink)` — this ViewModel contains **no** independent deep-link parsing/navigation logic of its own.

## 11. Files to Create — Screen Composable
`NotificationsInboxScreen`: filter-chip row (All/System/Safety/Marketing) at top; vertical list below with bold/regular read-state distinction, small unread dot, category-icon badge (shield/bell/tag), timestamp; skeleton shimmer during `Loading`; staleness banner when `isStale = true`; empty state ("Nothing here yet") when `items` is empty and not loading.

## 12. NextJS Requirements
N/A.

## 13. API Contract
Consumes `GET /v1/parent/notifications?type=&read_status=` and `POST /v1/parent/notifications/{id}/mark-read` (B-01) via `NotificationsRepository.getInbox(filter): NoorResult<List<NotificationItem>>` / `markRead(id): NoorResult<Unit>`.

## 14. Database Requirements
Local Room (or KMP-SQLite per platform convention) cache table mirroring the inbox item shape, plus a small outbox/queue table for offline mark-read actions (`notification_id`, `queued_at`, `synced: Boolean`). This blueprint defines the `NotificationsRepository` interface only; the concrete Room-backed implementation follows the same interface/implementation split established in C.20's K-01/K-07 relationship (interface here, persistence-specific implementation is this same blueprint's Task 04 since K-01 owns both here, unlike C.20 which split it across two blueprints — confirm this consolidation is acceptable given C.25's smaller inbox-only scope, or split into a dedicated caching sub-task if the module's size warrants it during implementation).

## 15. Validation
`NotificationsRepository`'s public methods must accept no externally-supplied `family_id`/`parent_id` parameter — family scope is always implicit via the authenticated session (enforced by Task 05's structural test, mirroring C.20's K-01 pattern).

## 16. Authentication
Reachable only via an authenticated parent session (`requiredAuthState` on the `Route`).

## 17. Authorization
Family scope derived exclusively from `:core:auth` — no cross-family data ever requested or cached.

## 18. Error Handling
- Fetch failure → cached last-known list shown with a staleness indicator (Edge Case 6, §1.11), never a blank screen if cache has content.
- Mark-as-read failure (network) → optimistic local update stands, queued for retry, never blocks further interaction (§1.11).
- Empty cache + fetch failure → standard error state with retry action.

## 19. Offline First
Inbox renders from Room cache immediately on screen entry; network refresh happens in the background; mark-as-read queues offline and syncs on reconnect (§1.14) — this is this blueprint's primary offline-first deliverable within the feature.

## 20. Local Data
Room-backed cache (or platform's KMP-SQLite equivalent) is this blueprint's own responsibility (unlike C.20 where caching was split into a separate K-07 blueprint) — `NotificationsRepository`'s implementation directly composes network + local cache reads/writes behind the single interface, keeping the ViewModel persistence-agnostic.

## 21. Localization
No hardcoded strings — all copy (filter chip labels, empty state, staleness banner) resolved via the platform's localization package, supporting English/Hindi/Arabic/Urdu.

## 22. RTL
Filter-chip row and list-item layout (icon badge, text, timestamp) must mirror correctly in RTL (Arabic/Urdu); verify via Compose RTL preview.

## 23. Analytics
`notifications_inbox_viewed` (on stable render), `notification_marked_read`, `notification_filtered_by_type`, `notification_deep_link_opened` (§1.19) — fire via the platform's existing analytics API (confirm exact firing convention against `CORE_ANALYTICS_INSTRUCTIONS.md` before implementation rather than inventing one).

## 24. Performance
- `@Immutable`/`@Stable` state classes to prevent unnecessary recomposition per list-item update.
- Cache-first render avoids a loading flash on every screen entry when cached data exists.
- Coroutine cancellation handled correctly on ViewModel clear (`viewModelScope`/`appScope` convention).

## 25. Security
Session-derived family scope prevents any cross-family notification history exposure; no sensitive data beyond what B-01 already returns.

## 26. Library Requirements
No new third-party libraries — Koin, Kotlin Coroutines/Flow, Compose Multiplatform, Room/KMP-SQLite per existing platform conventions.

## 27. Testing
1. Unit test: cache-first load shows cached items immediately, then updates on successful network refresh.
2. Unit test: network failure with existing cache → `isStale = true`, cached items remain visible (not blanked).
3. Unit test: mark-as-read while offline queues the action and applies an optimistic local update immediately.
4. Unit test: queued mark-as-read actions sync on reconnect.
5. **Structural test (mandatory):** confirm no public method on `NotificationsRepository` accepts an externally-supplied `family_id`/`parent_id` parameter.
6. Unit test: notification tap calls `deepLinkResolutionHandler.resolve()` — no independent deep-link logic exists in the ViewModel.
7. UI test: filter chips correctly narrow the visible list; empty state renders when appropriate.
8. UI test: skeleton shimmer renders during initial load with no cache present.

## 28. Documentation
KDoc on `NotificationsInboxViewModel` and `NotificationsRepository` citing PRD §6.1–§6.3, §6.7; author attribution per platform convention.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Route and UiState Models**
- Task ID: K01-T01
- Objective: Type-safe navigation destination and immutable state model.
- Why This Is Required: Foundation for screen and ViewModel.
- Existing Architecture to Follow: `Route` sealed interface pattern; C.20 K-01's `DashboardUiState` slice-modeling style as a reference (though this screen is single-list rather than multi-component-sliced).
- Existing Files to Reuse: `Route`, `BaseAuthState` hierarchy.
- Files to Create: `NotificationsInboxRoute.kt`, `NotificationsInboxUiState.kt`.
- Files to Modify: none.
- Implementation Details: Per §10; confirm exact `BaseAuthState` subclass name before hardcoding.
- Business Rules: §6.3 Navigation Flow.
- Validation: N/A.
- Error Handling: N/A.
- Security: `requiredAuthState` guard.
- Performance: `@Immutable` state classes.
- Localization: N/A (no strings in these files).
- RTL: N/A.
- Analytics: `analyticsName = "parent_notifications_inbox"`.
- Tests: Covered in Task 05.
- Documentation: KDoc.
- Dependencies: None.
- Do Not Change: Do not modify `Route` interface itself or other existing routes.
- Expected Result: Route and state types compile.
- Definition of Done: Matches §10.

**Task 02 — Define NotificationsRepository Interface**
- Task ID: K01-T02
- Objective: Data-access contract, family-scope-safe by construction.
- Why This Is Required: Decouples ViewModel from network/cache implementation.
- Existing Architecture to Follow: `core-data` repository interface pattern.
- Existing Files to Reuse: `NoorResult<T>`.
- Files to Create: `NotificationsRepository.kt` (interface).
- Files to Modify: none.
- Implementation Details: `interface NotificationsRepository { suspend fun getInbox(filter: NotificationFilter): NoorResult<List<NotificationItem>>; suspend fun markRead(id: String): NoorResult<Unit>; fun observeCached(): Flow<List<NotificationItem>> }` — no `familyId`/`parentId` parameter anywhere.
- Business Rules: §6.5.
- Validation: N/A.
- Error Handling: `NoorResult` convention.
- Security: No externally-supplied family scope — the structural guarantee.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 05 (structural test).
- Documentation: KDoc.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Interface compiles.
- Definition of Done: No method signature accepts `familyId`/`parentId`.

**Task 03 — Implement NotificationsInboxViewModel**
- Task ID: K01-T03
- Objective: Core state-management and offline-sync logic.
- Why This Is Required: Central orchestrator of the screen.
- Existing Architecture to Follow: `BaseViewModel`, `AuthStateProvider`, `DispatcherProvider` injection conventions.
- Existing Files to Reuse: `BaseViewModel`, `AuthStateProvider`, `DispatcherProvider`, `DeepLinkResolutionHandler`.
- Files to Create: `NotificationsInboxViewModel.kt`.
- Files to Modify: none.
- Implementation Details: Per §10; cache-first load, background refresh, optimistic mark-read with offline queueing, filter handling, deep-link delegation.
- Business Rules: §6.7, Edge Case 6.
- Validation: N/A.
- Error Handling: Per §18.
- Security: Session-derived family scope only.
- Performance: Parallel cache/network reads where sensible, `@Stable` state.
- Localization: N/A (ViewModel has no strings).
- RTL: N/A.
- Analytics: Fire `notifications_inbox_viewed`, `notification_marked_read`, `notification_filtered_by_type`, `notification_deep_link_opened`.
- Tests: Covered in Task 05.
- Documentation: KDoc, author tag.
- Dependencies: Tasks 01–02, 04.
- Do Not Change: Do not modify `BaseViewModel` or `DeepLinkResolutionHandler`.
- Expected Result: ViewModel functional against a fake `NotificationsRepository`.
- Definition of Done: All Task 05 tests pass.

**Task 04 — Implement Room-Backed NotificationsRepository and Offline Outbox**
- Task ID: K01-T04
- Objective: Concrete persistence + network-backed implementation of the interface, plus the offline mark-read queue.
- Why This Is Required: Delivers the offline-first guarantee.
- Existing Architecture to Follow: Platform's Room/KMP-SQLite conventions (confirm exact DB setup pattern against `CORE_DATABASE_INSTRUCTIONS.md` before implementation — not read in this pass, do not invent table/DAO naming conventions).
- Existing Files to Reuse: `:core:network` API client conventions for calling B-01's endpoints.
- Files to Create: `local/NotificationCacheDao.kt`.
- Files to Modify: `NotificationsRepository.kt` (add the concrete implementation class alongside the interface, or in a separate `NotificationsRepositoryImpl.kt` per platform convention — confirm file-splitting convention before implementation).
- Implementation Details: Cache table mirrors inbox item shape; outbox table tracks queued mark-read actions with a `synced` flag; a sync worker (triggered on reconnect, e.g., via `:core:network`'s connectivity observer) drains the outbox.
- Business Rules: §1.14, Edge Case 6.
- Validation: N/A.
- Error Handling: Sync retries on failure, never silently drops a queued action.
- Security: N/A.
- Performance: Indexed local queries.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 05.
- Documentation: KDoc.
- Dependencies: Task 02.
- Do Not Change: N/A.
- Expected Result: Repository correctly persists and syncs.
- Definition of Done: Offline mark-read actions survive app restart and sync correctly on reconnect.

**Task 05 — Implement Screen Composable and Write Test Suite**
- Task ID: K01-T05
- Objective: Visual delivery plus full test coverage.
- Why This Is Required: Core deliverable and PRD-mandated test coverage.
- Existing Architecture to Follow: `:core:design-system` tokens, Parent-Mode formal visual register (C.19 §2.1); Kotlin test + Compose UI testing conventions.
- Existing Files to Reuse: Design-system components — confirm exact component names against `CORE_DESIGNSYSTEM_INSTRUCTIONS.md` before use rather than inventing names.
- Files to Create: `NotificationsInboxScreen.kt`, `NotificationsInboxViewModelTest.kt`, `NotificationsRepositoryFamilyScopeStructuralTest.kt`.
- Files to Modify: Navigation graph registration; Koin DI root; C.20's Dashboard bell-icon navigation wiring.
- Implementation Details: Per §11 (screen layout) and §27 (8 test cases).
- Business Rules: §2.1, §2.3.
- Validation: N/A.
- Error Handling: Per-state rendering (loading/content/error/stale/empty).
- Security: Structural test is security-critical.
- Performance: Stable keys for list items, no unnecessary recomposition.
- Localization: All strings via localization package.
- RTL: Layout mirrors correctly.
- Analytics: N/A (fired from ViewModel).
- Tests: This task includes the tests.
- Documentation: KDoc.
- Dependencies: Tasks 01–04.
- Do Not Change: N/A.
- Expected Result: Screen renders correctly across all states; all 8 tests pass.
- Definition of Done: 100% of §27 green.

## 30. Definition of Done
`:feature:parent-notifications-support` module compiles with a functional, offline-first `NotificationsInboxScreen`/`NotificationsInboxViewModel`, session-derived family scoping structurally enforced, deep-link taps routed exclusively through the shared `DeepLinkResolutionHandler`, all tests green.

## 31. Final Verification Checklist
- [ ] Structural test confirms no externally-supplied `family_id`/`parent_id` anywhere in `NotificationsRepository`
- [ ] Cache-first render with staleness indicator on fetch failure
- [ ] Offline mark-read queues and syncs correctly on reconnect
- [ ] Notification tap uses `DeepLinkResolutionHandler` exclusively, no parallel deep-link logic
- [ ] All state classes `@Immutable`/`@Stable`
- [ ] No hardcoded strings
- [ ] RTL layout verified via preview
