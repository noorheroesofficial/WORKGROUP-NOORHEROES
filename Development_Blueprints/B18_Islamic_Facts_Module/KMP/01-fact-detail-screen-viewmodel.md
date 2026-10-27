# K-01 — Fact Detail Screen & ViewModel

## 1. Feature Context
Part of Feature B.18 (Islamic Facts Module). The primary KMP surface — a thin, lightweight feature module rendering the full fact context reached from Home's card or a spaced-repetition prompt.

## 2. Parent Feature
B.18 — Islamic Facts Module

## 3. Sub-feature
2.1 Fact Detail Screen & ViewModel (ID: K-01)

## 4. Objective
Build `FactDetailScreen` (Compose) and `FactDetailViewModel` in a new `:feature:facts` module, rendering the fact restatement, explanation, sources, scholar-approval badge, jurisprudential-scope note, and conditionally-rendered Related Content/Linked Quiz cards based on API availability flags.

## 5. Business Requirements
- FR-2, FR-6: fact cards display age band, topic, source, scholar approval, explanation, related story, quiz; explanation distinct from fact text ("why," not just "what").
- Acceptance Criteria: Fact Detail shows explanation, source references, scholar-approval indicator, related content/quiz link.
- §2.2 Screen-Level Design: single-column reading layout, states (Default/Loading/Offline/Related-unavailable/Quiz-unavailable), accessibility (source citations and approval badge screen-reader-readable, not icon-only), responsive (tablet wider reading column).
- §6.10 Testing Strategy: conditional rendering never attempts navigation for an unavailable reference.

## 6. Existing Architecture
New lightweight module `:feature:facts`, Kotlin, Jetpack Compose, MVVM, Clean Architecture, depending on `:core:quiz-engine` (A.8), `:core:mastery-engine` (A.9), `:core:design-system`, `:core:network`, `:core:offline-cache` — per PRD §6.1. Deliberately thin: no parallel quiz or mastery logic.

## 7. Existing Code to Reuse
- A.3/A.5's existing scholar-approval badge component from `:core:design-system` (reuse, do not redefine locally).
- A.8's explanation-card visual pattern (per-answer-explanation pedagogy, A.8 §2.1) — reuse for the fact explanation section's visual treatment.
- Global Design System tokens (A.1 §2.1).
- Existing `available`/presence-flag conditional-rendering convention (mirrors B.14 Favorites' resolution approach).

## 8. Files to Create
- `feature-facts/src/commonMain/kotlin/.../FactDetailScreen.kt`
- `feature-facts/src/commonMain/kotlin/.../FactDetailViewModel.kt`
- `feature-facts/src/commonMain/kotlin/.../FactDetailUiState.kt`
- `feature-facts-domain/src/commonMain/kotlin/.../GetFactDetailUseCase.kt`
- `feature-facts-data/src/commonMain/kotlin/.../FactsRepository.kt`, `FactsRepositoryImpl.kt`
- `feature-facts/src/commonTest/kotlin/.../FactDetailViewModelTest.kt`
- `feature-facts/src/commonTest/kotlin/.../FactDetailScreenUiTest.kt`

## 9. Files to Modify
- `:core:navigation`'s route registry — add `FactDetail` destination.
- DI module (Koin/Hilt-equivalent per platform convention) — register `:feature:facts` bindings.

## 10. Backend Requirements
Consumes B-03 (`GET /v1/facts/{id}`) via `FactsRepository.getFactDetail(factId)`. No backend code produced here.

## 11. KMP Requirements
- `FactDetailViewModel` fetches detail on screen entry, exposes `FactDetailUiState` (Loading/Success/Error/Offline).
- Screen renders: fact restatement header, explanation body, source citation block (smaller, clearly-distinguished reference style), scholar-approval badge (version/date, tap-to-expand micro-explainer), jurisprudential-scope note (calm informational style, not alarm styling) when present.
- Related Content card and Linked Quiz card rendered **only** when their respective `available`/presence flags are true — an unavailable reference is not rendered disabled, it is not rendered at all.
- Loading state: skeleton card shimmer.
- Offline state: cached last-known data with staleness indicator (via `:core:offline-cache`, K-03).
- Tablet: wider single reading column with Related Content/Quiz cards alongside rather than stacked below (responsive rule per §2.2).
- Accessibility: source citations and scholar-approval badge fully screen-reader-readable (semantic content descriptions, not icon-only).
- Prevent unnecessary recomposition: `FactDetailUiState` modeled as an immutable/stable data class.

## 12. NextJS Requirements
N/A.

## 13. API Contract
Consumes B-03's contract exactly (§13 of B-03's blueprint) — no local reshaping beyond mapping to the KMP domain model.

## 14. Database Requirements
No new local persistence in this sub-feature; caching handled by K-03.

## 15. Validation
Client-side: `factId` non-null before triggering fetch; malformed navigation args handled gracefully (error state, not a crash).

## 16. Authentication
Reuses existing child-session auth token attached by `:core:network`'s interceptor.

## 17. Authorization
N/A beyond authenticated child session.

## 18. Error Handling
- Network failure with no cache: friendly retry state.
- Network failure with cache present: staleness-indicated cached view (K-03 dependency).
- Fact withdrawn (`410`): "This fact is no longer available" friendly message, not a generic error.
- Related-content/quiz link with `available: false`: section simply omitted, no error shown for that section specifically.

## 19. Offline First
Daily fact and Fact Detail cached for offline viewing (K-03); this sub-feature consumes that cache via `FactsRepository`, offline-first read pattern: local cache → remote refresh → UI update.

## 20. Local Data
Room-backed cache (K-03) exposed through `FactsRepository`; this ViewModel is cache-source-agnostic (repository abstracts local vs. remote).

## 21. Localization
All display strings (labels: "Related Story," "Quick Quiz," "Scholar Approved," etc.) sourced from the platform's localization resource system — English, Hindi, Arabic, Urdu. Fact text/explanation/sources come pre-localized from the API per the child's locale.

## 22. RTL
Full RTL layout correctness for Arabic — verified via the Figma Arabic RTL mockup (§2.5 Prompt 2); Compose `LocalLayoutDirection` respected throughout, no hardcoded start/end assumptions.

## 23. Analytics
`fact_detail_viewed`, `fact_explanation_viewed`, `fact_source_viewed`, `fact_related_content_tapped` (fired on tap of the Related Content card, before navigating away) fired via `FactsAnalytics`, using the existing `CORE_ANALYTICS_INSTRUCTIONS.md` event-emission pattern.

**Cross-reference note:** `fact_of_day_shown` and `fact_card_tapped` (PRD §1.19) are fired by the Home Fact of the Day card itself, which is owned by `:feature:home` (A.2), not this module — this screen's ViewModel/analytics wiring does not duplicate those two events; confirm with A.2's implementation that they are wired on the card, not assumed to be emitted here.

## 24. Performance
- Immutable/stable `FactDetailUiState` to minimize recomposition.
- Image/icon assets loaded via existing `:core:design-system` image-loading utility (no ad-hoc network image loading).
- Coroutine cancellation on screen exit via `viewModelScope`.

## 25. Security
No new sensitive data handling; standard child-session-scoped network calls.

## 26. Library Requirements
Kotlin, Jetpack Compose, Hilt (or platform DI equivalent), Retrofit+OkHttp (via `:core:network`), Room (via `:core:offline-cache`) — no new libraries beyond existing platform stack.

## 27. Testing
- Unit: `FactDetailViewModel` state transitions (Loading → Success/Error/Offline).
- UI test: tapping a related-content card with `available=false` is impossible because the card is not rendered at all (not rendered-but-disabled).
- UI test: scholar-approval badge renders correctly with version/date metadata, verified screen-reader-readable.
- UI test: RTL layout snapshot for Arabic.

## 28. Documentation
KDoc on `FactDetailViewModel` and `FactsRepository` documenting the conditional-rendering contract (never render an unavailable reference).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Scaffold `:feature:facts` Module**
Objective: Create module structure (`commonMain`, `androidMain`, `iosMain`, `commonTest`) with Clean Architecture layering matching existing feature modules.
Existing Architecture to Follow: An existing thin feature module's structure (e.g., `:feature:favorites` from B.14) as the closest reference.
Dependencies: None.
Definition of Done: Module builds empty, wired into the multi-module project.

**Task 02 — `FactsRepository` + Data Layer**
Objective: `FactsRepository.getFactDetail(factId)`, `getDailyFact()` interfaces + impl calling B-02/B-03 via `:core:network`.
Files to Create: `feature-facts-data/.../FactsRepository.kt`, `FactsRepositoryImpl.kt`.
Dependencies: Task 01, B-02/B-03 deployed (or contract-mocked for parallel development).
Definition of Done: Repository returns typed domain models from raw API responses.

**Task 03 — Domain Use Case**
Objective: `GetFactDetailUseCase`.
Dependencies: Task 02.
Definition of Done: Use case testable in isolation.

**Task 04 — ViewModel + UI State**
Objective: `FactDetailViewModel`, `FactDetailUiState`.
Dependencies: Task 03.
Definition of Done: State transitions correct per Task 07 unit tests.

**Task 05 — Compose Screen**
Objective: `FactDetailScreen` rendering all sections per §11.
Existing Files to Reuse: `:core:design-system`'s scholar-approval badge, A.8's explanation-card pattern.
Dependencies: Task 04.
Definition of Done: Visual match against Figma mockup (§2.5), passes Task 07 UI tests.

**Task 06 — Navigation Registration**
Objective: Register `FactDetail` destination in `:core:navigation`.
Files to Modify: navigation route registry.
Dependencies: Task 05.
Definition of Done: Screen reachable via route.

**Task 07 — Tests**
Objective: Full coverage per §27.
Dependencies: Tasks 01–06.
Definition of Done: All green.

**Task 08 — Documentation**
Dependencies: Task 07.
Definition of Done: KDoc complete.

## 30. Definition of Done
- `FactDetailScreen` renders all required sections, correctly conditional on availability flags.
- Zero navigation possible to an unavailable related-content/quiz reference.
- RTL and all four locales verified.
- Accessibility verified (screen-reader-readable citations/badge).
- Tests green, documentation complete.

## 31. Final Verification Checklist
- [ ] Conditional rendering verified: unavailable references never rendered (not disabled, absent)
- [ ] Scholar-approval badge screen-reader-readable, not icon-only
- [ ] RTL layout verified for Arabic
- [ ] All four locales (EN/HI/AR/UR) verified
- [ ] Recomposition minimized via immutable state
- [ ] Offline cached state renders with staleness indicator
- [ ] Reuses existing badge/explanation-card components, no local reinvention
- [ ] Analytics events firing correctly, including `fact_related_content_tapped`
- [ ] Confirmed `fact_of_day_shown`/`fact_card_tapped` are owned/emitted by A.2's Home card, not duplicated here
