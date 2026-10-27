# K-01 — Quran Learning Home (Skill Tree Map)

## 1. Feature Context
Part of Feature A.5 (Quran & Arabic Learning). This is the Learn Tab's entry screen — the child's orientation point for the whole learning journey, rendering the skill-tree map backed by B-01.

## 2. Parent Feature
A.5 — Quran & Arabic Learning

## 3. Sub-feature
K-01 — Quran Learning Home (Skill Tree Map)

## 4. Objective
Render a scrollable/zoomable skill-tree map purely from server data (B-01's `GET /v1/learning/paths`), with distinct visual states per node, correct locked-node unlock-condition display, offline/cached fallback, and full accessibility/RTL/localization support.

## 5. Business Requirements
- FR-1: skill-tree map with mastery indicators, mode selectors, placement-check option for new learners.
- FR-2: node states rendered exactly as `Locked/Ready/Learning/Practicing/Mastered/Needs Refresh`; locked nodes show the specific unlock condition.
- FR-3: progress shown via visual indicators (ring, label) without exposing the raw composite score.
- UX §2.1: node-state visual language — Locked (greyed, padlock), Ready (outlined, pulse), Learning (partial ring), Practicing (filled ring), Mastered (gold ring+check), Needs Refresh (amber ring+icon).
- Acceptance Criteria: first-time child sees placement-check offer before Surah 1 default; locked-node tap shows specific unlock condition.
- Loading State: skeleton node-grid shimmer. Error State: cached last-known tree with "may be slightly out of date" indicator.

## 6. Existing Architecture
NoorHeroes KMP app: Clean Architecture, Jetpack Compose Multiplatform UI, **Koin** for DI (not Hilt — corrects the PRD draft's Android-only assumption; Koin is the project's actual multiplatform DI per `core-common`'s `di` package and `core-network`/`core-data`'s Koin modules), **Ktor** for networking (not Retrofit+OkHttp — per `core-network`), **Room** for local caching (per `core-database`, KMP-multiplatform Room with `BundledSQLiteDriver`), navigation via the project's custom `Navigator`/`Route`/`NavigationAction` pattern (per `core-navigation`, not raw Compose `NavController` calls from ViewModels), analytics via the `AnalyticsTracker` interface (`logEvent(name, params)`, per `core-analytics`). New feature module: `feature-learn` (UI) + `feature-learn-domain` (use cases), following the existing `feature-onboarding`/`feature-onboarding-domain` naming convention.

## 7. Existing Code to Reuse
- `core-navigation`'s `Navigator` interface and `Route` sealed-class pattern — define `LearnRoute.SkillTree`, `LearnRoute.PlacementCheck`, etc.
- `core-analytics`'s `AnalyticsTracker` for all event firing.
- `core-data`'s repository pattern (`XyzRepositoryImpl` in `core-data/repository/`) — implement `LearningRepository` there, exposing `Outcome<SkillTree>` per the shared `Outcome` monad from `core-common/result`.
- `core-database`'s `SafeDatabaseHelper`/DAO pattern for cached skill-tree persistence (Room entity + DAO in `core-database`).
- `core-designsystem` tokens (existing Global Design System) extended with new node-state and feedback-iconography tokens.
- `core-common/error`'s `AppError` hierarchy for error-state mapping.

## 8. Files to Create
- `feature-learn/src/commonMain/kotlin/.../skilltree/SkillTreeScreen.kt` (Composable)
- `feature-learn/src/commonMain/kotlin/.../skilltree/SkillTreeViewModel.kt`
- `feature-learn/src/commonMain/kotlin/.../skilltree/SkillTreeUiState.kt`
- `feature-learn-domain/src/commonMain/kotlin/.../GetSkillTreeUseCase.kt`
- `core-data/src/commonMain/kotlin/.../repository/LearningRepository.kt` (interface) + `LearningRepositoryImpl.kt`
- `core-network/src/commonMain/kotlin/.../api/LearningApi.kt` (Ktor client interface for `GET /v1/learning/paths`)
- `core-database/src/commonMain/kotlin/.../entity/SkillNodeCacheEntity.kt` + DAO
- `core-navigation/src/commonMain/kotlin/.../route/LearnRoute.kt`
- `feature-learn/src/commonTest/kotlin/.../SkillTreeViewModelTest.kt`
- `feature-learn/src/androidInstrumentedTest/kotlin/.../SkillTreeScreenUiTest.kt`

## 9. Files to Modify
- App-level Koin module registration (wire new `feature-learn` module's DI graph).
- Top-level `NavHost`/`NavigationHandler` — register `LearnRoute` destinations.
- Bottom-nav "Learn" tab entry point — route to `LearnRoute.SkillTree` as start destination.

## 10. Backend Requirements
Consumes B-01 (`GET /v1/learning/paths?track=quran&child_id=`) exclusively for skill-tree data — this screen performs zero client-side mastery computation; the server response is always authoritative on every fetch.

## 11. KMP Requirements
- **Composable**: scrollable/zoomable organically-curved path (not rigid grid) connecting node icons, grouped by Surah/topic, horizontal branching for parallel tracks (Arabic Letters alongside Quran/Surah track).
- **Mastery summary header**: e.g., "12 skills mastered," sourced directly from the response payload's `mastery_summary`.
- **Node visual states**: six distinct, non-color-only treatments per §2.1 design tokens.
- **Locked-node tap**: shows the specific `unlock_condition` text from the response, never a generic lock message.
- **Mode-selector entry point**: opens the Mode Selector Sheet (modal, routes into K-05/K-06/K-07 game/lesson modes).
- **Placement-check re-offer**: prominent for first-time users (zero progress), subtle for returning low-activity users — logic driven by whether `mastery_summary.mastered_count == 0` and no prior placement-check completion flag.
- **`SkillTreeViewModel`**: mirrors backend node states client-side for instant UI response, treats server as authoritative on every fetch — contains NO client-side mastery-score calculation logic whatsoever.
- **Offline/error fallback**: on fetch failure, render the last Room-cached response with a "may be slightly out of date" indicator, never a blank/broken map.
- **Tablet responsive reflow**: wider node spacing, same logical structure — implemented via `WindowSizeClass`-aware layout, consistent with existing responsive patterns in `core-designsystem`.
- **Accessibility**: tree navigable linearly via screen reader in a logical reading order independent of visual spatial layout; each node's state announced via `contentDescription`/semantics.
- **Deep link**: `noorheroes://learn/node/{node_id}` resolves to `LearnRoute.SkillTree(focusNodeId = node_id)` via `core-navigation`'s route parsing, used by Home's "Continue Learning" entry point.

## 12. NextJS Requirements
N/A (consumer of B-09-managed `skill_node` definitions indirectly via B-01; no direct admin dependency at this screen).

## 13. API Contract
`GET /v1/learning/paths?track=quran&child_id={child_id}` — per B-01 §13. Client-side: `LearningApi.getSkillTree(track, childId): SkillTreeDto` via Ktor, mapped to domain `SkillTree` model in `LearningRepositoryImpl`.

## 14. Database Requirements
Room entity `SkillNodeCacheEntity` (mirrors the DTO shape) in `core-database`, written on every successful fetch, read as the offline/error fallback source. No sensitive data — pure progress-display cache, safe to persist locally without special encryption beyond the app's standard local-storage posture.

## 15. Validation
N/A client-side beyond standard null/empty-state handling; all authoritative validation happens server-side (B-01).

## 16. Authentication
Reuses the existing child-session auth token attached automatically by `core-network`'s `HttpClient` configuration (existing interceptor, not reimplemented here).

## 17. Authorization
N/A beyond the existing authenticated child session — no additional client-side authorization logic required.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Network/API failure | Render last Room-cached skill tree with "may be slightly out of date" indicator |
| Zero cached data + fetch failure (true first-run offline) | Friendly empty/error state, retry action, never a crash |
| `403`/`401` (session issue) | Delegate to app-level session-expiry handling (existing global auth-error interceptor in `core-network`) |

## 19. Offline First
Downloaded/cached skill-tree data fully viewable offline (read-only); actions requiring connectivity (attempt submission, recitation) are gated at the destination screens (K-03/K-05/K-06/K-07), not here.

## 20. Local Data
Remote (B-01) → `LearningRepositoryImpl` → Room cache (`SkillNodeCacheEntity`) → `SkillTreeViewModel` → UI. Cache invalidated/refreshed on every successful remote fetch (read-through, not offline-write pattern, since this data is server-authoritative).

## 21. Localization
Surah/topic/node labels resolved via the existing `core-common/localization` reactive provider; supports English, Hindi, Arabic, Urdu per app-wide requirement.

## 22. RTL
Full RTL layout support for Arabic locale — the organically-curved path direction, node ordering, and text alignment must mirror correctly; verified against the app's existing RTL-support patterns in `core-designsystem`.

## 23. Analytics
Fires via `AnalyticsTracker.logEvent()`: `learn_tab_viewed`, `skill_node_viewed`, `skill_node_locked_tapped`, `skill_node_started` — parameters limited to node/track identifiers, no PII.

## 24. Performance
- Target p95 render < 800ms (cached).
- Prevent unnecessary recomposition: `SkillTreeUiState` uses stable/immutable data classes; node list keyed by `node_id` in `LazyColumn`/custom layout to avoid full-tree recomposition on partial updates.
- Avoid main-thread blocking during Room cache reads (use `Dispatchers.IO`/coroutine-based DAO calls per `core-common/coroutines` dispatcher abstraction).

## 25. Security
No sensitive data rendered on this screen (no audio, no raw scores). Standard authenticated-session data exposure only.

## 26. Library Requirements
Koin (DI), Ktor (networking), Room (local cache, KMP multiplatform), Kotlinx Serialization (DTOs), Compose Multiplatform. No Hilt, no Retrofit, no SQLDelight — these were incorrectly assumed in the original PRD draft's Android-specific code-gen prompt and are corrected here to match the actual existing architecture.

## 27. Testing
- Unit: `SkillTreeViewModel` state mapping is render-only (assert no mastery-score computation occurs client-side — inspect that the ViewModel never derives a `state` value, only passes through the server's `state` field).
- Unit: locked-node display logic always surfaces the server-provided `unlock_condition`, never a hardcoded generic message.
- UI test: tablet reflow renders wider node spacing without altering logical node order.
- UI test: screen-reader traversal order is linear/logical, independent of visual spatial layout.
- Integration: offline/error fallback renders cached data with the correct "may be slightly out of date" indicator.

## 28. Documentation
KDoc on `SkillTreeViewModel` explicitly documenting the "render-only, never compute" contract, since this is a load-bearing architectural constraint for future contributors.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define `LearnRoute` Navigation Contract**
- Task ID: K-01-T01
- Objective: Add type-safe routes for the Learn tab's screen graph.
- Existing Architecture to Follow: `core-navigation`'s `Route` sealed-interface pattern.
- Files to Create: `core-navigation/.../route/LearnRoute.kt`.
- Dependencies: None.
- Definition of Done: `LearnRoute.SkillTree`, `.PlacementCheck`, etc. compile and are usable by `Navigator`.

**Task 02 — Implement `LearningApi` Ktor Client**
- Task ID: K-01-T02
- Files to Create: `core-network/.../api/LearningApi.kt`.
- Implementation Details: `suspend fun getSkillTree(track: String, childId: String): SkillTreeDto` per B-01's contract; reuses existing `HttpClient` factory and auth interceptor.
- Dependencies: B-01 (backend contract must be finalized/stable).
- Definition of Done: API call succeeds against a mocked/staging backend.

**Task 03 — Implement `SkillNodeCacheEntity` & DAO**
- Task ID: K-01-T03
- Files to Create: `core-database/.../entity/SkillNodeCacheEntity.kt`, DAO.
- Existing Files to Reuse: `SafeDatabaseHelper` for write operations.
- Dependencies: None.
- Definition of Done: Room schema compiles, DAO CRUD unit-tested.

**Task 04 — Implement `LearningRepository`/`LearningRepositoryImpl`**
- Task ID: K-01-T04
- Files to Create: `core-data/.../repository/LearningRepository.kt` (interface) + impl.
- Implementation Details: Fetch-then-cache pattern; returns `Outcome<SkillTree>`; on network failure, falls back to DAO-cached read.
- Dependencies: K-01-T02, K-01-T03.
- Definition of Done: Repository unit tests cover success, network-failure-with-cache, and network-failure-no-cache paths.

**Task 05 — Implement `GetSkillTreeUseCase`**
- Task ID: K-01-T05
- Files to Create: `feature-learn-domain/.../GetSkillTreeUseCase.kt`.
- Dependencies: K-01-T04.
- Definition of Done: Use case unit-tested.

**Task 06 — Implement `SkillTreeViewModel`**
- Task ID: K-01-T06
- Files to Create: `feature-learn/.../skilltree/SkillTreeViewModel.kt`, `SkillTreeUiState.kt`.
- Implementation Details: Render-only state mapping (no mastery computation); loading/default/error/first-time states; analytics event firing; injects `Navigator` for locked-node-tap and mode-selector navigation.
- Existing Files to Reuse: `AnalyticsTracker`.
- Dependencies: K-01-T05.
- Definition of Done: Unit tests (Task 09) pass.

**Task 07 — Build `SkillTreeScreen` Composable**
- Task ID: K-01-T07
- Files to Create: `feature-learn/.../skilltree/SkillTreeScreen.kt`.
- Implementation Details: Organically-curved path layout, six node-state visual treatments per design tokens, mastery summary header, mode-selector entry, placement-check re-offer banner, tablet-responsive layout, screen-reader semantics.
- Existing Files to Reuse: `core-designsystem` tokens (extended with node-state/feedback-iconography tokens per Task 08).
- Dependencies: K-01-T06.
- Definition of Done: Screen renders correctly across all documented states (loading/default/error/first-time) in Compose Preview.

**Task 08 — Extend Design System Tokens**
- Task ID: K-01-T08
- Objective: Add node-state and feedback-iconography tokens to `core-designsystem`.
- Files to Modify: `core-designsystem` token definitions.
- Dependencies: None (can run in parallel with Task 07).
- Definition of Done: Tokens available and used consistently by Task 07 and downstream K-blueprints (K-04's feedback iconography reuses these).

**Task 09 — Unit & UI Tests**
- Task ID: K-01-T09
- Objective: Full coverage per §27.
- Dependencies: K-01-T01–T08.
- Definition of Done: All tests green in CI.

**Task 10 — Wire Deep Link & Bottom-Nav Entry**
- Task ID: K-01-T10
- Files to Modify: Top-level `NavHost`, bottom-nav configuration.
- Implementation Details: `noorheroes://learn/node/{node_id}` deep link resolves via `LearnRoute` parsing.
- Dependencies: K-01-T01, K-01-T07.
- Definition of Done: Deep link manually verified to land on the correct focused node.

## 30. Definition of Done
Skill Tree screen renders correctly across all six node states, purely from server data, with correct offline/error fallback, full accessibility/RTL/localization, tablet responsiveness, and analytics — fully tested and documented.

## 31. Final Verification Checklist
- [ ] Zero client-side mastery-score computation anywhere in `SkillTreeViewModel` (render-only verified)
- [ ] All six node states render with distinct, non-color-only visual treatments
- [ ] Locked-node tap always shows the specific server-provided unlock condition
- [ ] Offline/error fallback shows cached data with "may be slightly out of date" indicator, never blank
- [ ] Tablet reflow preserves logical node order
- [ ] Screen-reader traversal is linear and logical
- [ ] RTL layout verified for Arabic locale
- [ ] Deep link `noorheroes://learn/node/{node_id}` resolves correctly
- [ ] Uses Koin/Ktor/Room per actual project architecture (not Hilt/Retrofit as in the earlier PRD draft)
- [ ] Full test suite green in CI
