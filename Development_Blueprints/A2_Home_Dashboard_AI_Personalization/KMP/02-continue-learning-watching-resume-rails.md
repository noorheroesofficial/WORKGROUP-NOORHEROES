# K-02 — Continue Learning & Continue Watching Resume Rails

## 1. Feature Context
NoorHeroes Child App (KMP). Renders the "Continue Learning" and "Continue Watching" horizontal rails within `HomeScreen` (K-01).

## 2. Parent Feature
A.2 — Child Home Dashboard & AI Personalization

## 3. Sub-feature
2.2 Continue Learning & Continue Watching Resume Rails (ID: K-02)

## 4. Objective
Build the two resume rails as independent section Composables plugging into K-01's `HomeUiState`, consuming B-05's `/v1/progress/resume` data (via B-01's aggregated response), with correct empty/error/offline behavior.

## 5. Business Requirements
Per PRD FR-3, §2.2, §2.3:
- Type-segmented rails (no cross-type dedup bleed).
- Section omitted entirely (not empty placeholder) when nothing in progress.
- Section hides on error, other sections unaffected.
- Offline: shows only downloaded resumable items.
- Tap routes to Story Detail/Quran Lesson/Quiz Player with entitlement + download-availability check.
- Withdrawn-content tap → graceful "no longer available" + silent cache removal.

## 6. Existing Architecture
Plugs into K-01's `SectionState<T>` model. Follow `CORE_UI_INSTRUCTIONS.md` and `CORE_NAVIGATION_INSTRUCTIONS.md` for rail Composables and typed navigation events.

## 7. Existing Code to Reuse
K-01's `SectionState`, shimmer skeleton pattern, `HomeUiState` shape; `:core:design-system` card/rail tokens.

## 8. Files to Create
- `feature/home/src/commonMain/kotlin/.../components/ContinueLearningRail.kt`
- `feature/home/src/commonMain/kotlin/.../components/ContinueWatchingRail.kt`
- `feature/home/src/commonMain/kotlin/.../models/ResumeItem.kt`
- `feature/home/src/androidInstrumentedTest/.../ContinueLearningRailTest.kt`

## 9. Files to Modify
- `HomeScreen.kt` (K-01) — slot in both rail Composables at their fixed order position
- `HomeUiState.kt` (K-01) — add `continueLearning`/`continueWatching` fields if not already scaffolded

## 10. Backend Requirements
Consumes `continue_learning`/`continue_watching` sections from B-01's `GET /v1/home` response (sourced from B-05).

## 11. KMP Requirements
- Horizontal rail Composable with progress-bar overlay per card.
- Omit rail entirely (`SectionState.Hidden`) when the item list is empty — not an empty rail shell.
- Filter to downloaded-only items when `HomeUiState` indicates offline mode (coordinate flag/source with K-07).
- Tap handler performs entitlement + download-availability check before navigating (reuse existing entitlement-check utility from the platform if one exists, e.g., from Subscription/Entitlement feature — do not reimplement).
- Withdrawn-content tap: catch a specific "content unavailable" signal from the navigation/detail-fetch call, show a toast, and remove the item from local state/cache.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
Reads `sections.continue_learning.items[]` / `sections.continue_watching.items[]` from B-01's response (see B-01 §13); item shape includes `content_id`, `type`, `title`, `progress`.

## 14. Database Requirements
Not applicable directly (local cache is K-07's scope); this sub-feature reads from `HomeUiState`, not directly from Room.

## 15. Validation
Distinguish `SectionState.Hidden` (nothing in progress) from `SectionState.Error` (Progress Service failure) — both result in no visible content, but only `Error` should log/telemetry-flag as a degradation event.

## 16. Authentication
N/A (inherits session from K-01/network layer).

## 17. Authorization
N/A at UI layer.

## 18. Error Handling
Section hides silently on `Error` state (no error banner shown to child, per PRD §2.2 table: "Section hides on error"). Withdrawn-content tap shows a graceful toast, not a raw error.

## 19. Offline First
Rail filters to downloaded-only items when offline; non-downloaded resumable items are simply excluded from the rail in offline mode (not shown disabled) per K-01/K-07's offline state contract.

## 20. Local Data
Reads download-availability status from the existing offline-download feature's local store (`:core:offline-cache` or equivalent — reuse Feature B.15 Offline Downloads & Sync's existing local data layer if already implemented; do not create a parallel download-status store).

## 21. Localization
Card titles/labels via string resources; content titles are pre-localized from the backend.

## 22. RTL
Rail scroll direction mirrors correctly in RTL locales (verify horizontal scroll gesture direction, not just text alignment).

## 23. Analytics
`continue_learning_viewed`, `continue_learning_resumed`, `continue_watching_resumed` fired on view/tap respectively, per `CORE_ANALYTICS_INSTRUCTIONS.md` conventions.

## 24. Performance
Rail uses lazy horizontal list (`LazyRow` or equivalent) to avoid rendering off-screen cards; image loading (thumbnails) via the platform's existing image-loading library (Coil per PRD §7, or KMP equivalent) with placeholder/skeleton during load.

## 25. Security
N/A beyond standard entitlement checks (no new security surface).

## 26. Library Requirements
Compose Multiplatform, existing image-loading library, existing navigation library.

## 27. Testing
- Compose UI: rail renders correctly with 1, multiple, and zero items (zero → section hidden entirely).
- Compose UI: error state hides section without visible error UI.
- Unit: offline filtering logic (downloaded-only inclusion).
- Integration: withdrawn-content tap shows toast and removes item from local list.

## 28. Documentation
KDoc explaining the Hidden-vs-Error distinction for this section specifically, since it's a common source of confusion (empty-because-nothing-in-progress vs. empty-because-service-failed look identical to the child but must be handled differently for telemetry).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define `ResumeItem` Model + State Mapping**
- Objective: Typed model for rail items.
- Why Required: Type-safe mapping from B-01's response.
- Existing Architecture to Follow: K-01's data-model conventions.
- Existing Files to Reuse: `SectionState` from K-01.
- Files to Create: `models/ResumeItem.kt`
- Files to Modify: `HomeUiState.kt`
- Implementation Details: `data class ResumeItem(contentId, contentType, title, progressPercent, thumbnailUrl, isDownloaded)`.
- Business Rules: `contentType` drives routing target.
- Validation: N/A.
- Error Handling: N/A.
- Security: N/A.
- Performance: `@Immutable`.
- Localization: `title` pre-localized.
- RTL: N/A.
- Analytics: N/A.
- Tests: Unit test for DTO-to-model mapping including null/empty handling.
- Documentation: KDoc.
- Dependencies: K-01 Task 01.
- Do Not Change: N/A.
- Expected Result: Model defined.
- Definition of Done: Mapping unit test passes.

**Task 02 — Build Rail Composables**
- Objective: `ContinueLearningRail` and `ContinueWatchingRail` Composables.
- Why Required: Primary UI deliverable.
- Existing Architecture to Follow: `:core:design-system` card/rail tokens.
- Existing Files to Reuse: K-01 shimmer skeleton.
- Files to Create: `components/ContinueLearningRail.kt`, `components/ContinueWatchingRail.kt`
- Files to Modify: `HomeScreen.kt`
- Implementation Details: `LazyRow` of cards with progress-bar overlay; renders nothing when `SectionState.Hidden`; shimmer during `Loading`.
- Business Rules: Section omitted entirely (no card) when empty, not a placeholder.
- Validation: N/A.
- Error Handling: Silent hide on `Error`.
- Security: N/A.
- Performance: Lazy list, image placeholder during load.
- Localization: String-resource labels.
- RTL: Verified scroll-direction mirroring.
- Analytics: `continue_learning_viewed`/`continue_watching_resumed` wired via `LaunchedEffect`/click handler.
- Tests: Compose UI tests for item counts 0/1/many and error-hide behavior.
- Documentation: KDoc.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Rails render correctly.
- Definition of Done: Compose UI tests pass.

**Task 03 — Implement Tap Navigation with Entitlement + Withdrawn-Content Handling**
- Objective: Correct routing and graceful withdrawn-content handling.
- Why Required: Edge Case 12 (withdrawn content), PRD §2.3 routing table.
- Existing Architecture to Follow: `CORE_NAVIGATION_INSTRUCTIONS.md` typed navigation events; existing entitlement-check utility.
- Existing Files to Reuse: Existing entitlement/download-availability check (from Subscription/Offline-Downloads features).
- Files to Create: none (logic added to rail Composables/ViewModel interaction)
- Files to Modify: `ContinueLearningRail.kt`, `ContinueWatchingRail.kt`, `HomeViewModel.kt` (K-01)
- Implementation Details: On tap, check entitlement + (if offline) download-availability before navigating; on detail-fetch returning "unavailable," show toast + remove item from `HomeUiState` locally without a full reload.
- Business Rules: Never a dead navigation to a withdrawn item.
- Validation: N/A.
- Error Handling: Graceful toast, not raw error.
- Security: Reuses existing entitlement enforcement (no bypass introduced here).
- Performance: Local state update avoids full Home reload for a single removed item.
- Localization: Toast text via string resources.
- RTL: N/A.
- Analytics: `continue_learning_resumed`/`continue_watching_resumed` on successful navigation.
- Tests: Integration test for withdrawn-content flow.
- Documentation: KDoc.
- Dependencies: Tasks 01, 02.
- Do Not Change: N/A.
- Expected Result: Working tap-to-navigate flow.
- Definition of Done: Withdrawn-content integration test passes.

## 30. Definition of Done
Both rails render correctly with proper empty/error/offline handling, correct tap routing with entitlement checks, and graceful withdrawn-content recovery; all tests green.

## 31. Final Verification Checklist
- [ ] Rails omitted entirely (not empty shell) when nothing in progress
- [ ] Rails hide silently on Progress Service error
- [ ] Offline mode filters to downloaded-only items
- [ ] Withdrawn-content tap shows graceful toast and removes item locally
- [ ] Type-segmentation confirmed (no learning/watching cross-bleed)
- [ ] RTL scroll direction verified
- [ ] All tests pass
