# K-01 — Ramadan Countdown, Prep Checklist & Themed Home

## 1. Feature Context
The entry point into the entire Ramadan Mode experience: a 14-day pre-Ramadan countdown, a Parent Prep Checklist, and the seasonal re-theming of Home — all driven entirely by B-01's server-computed lifecycle phase, with zero local Hijri-date computation anywhere in this module.

## 2. Parent Feature
F.36 — Ramadan Mode

## 3. Sub-feature
2.1 Ramadan Countdown, Prep Checklist & Themed Home (ID: **K-01**)

## 4. Objective
Implement `RamadanCampaignViewModel` and its three Composables (Countdown, Prep Checklist, Themed Home overlay) deriving all state exclusively from B-01's `GET /v1/ramadan/campaign-status` response.

## 5. Business Requirements
- FR-5: Home re-themes during the activation window.
- §6.4: `RamadanCampaignViewModel` derives phase/night/suppression state entirely from server responses — never independently computing Hijri dates client-side.
- §7 Android AI prompt item 1 (mandatory): no Hijri-calculation library or hardcoded Laylatul-Qadr night list exists in this module's source.
- §1.12/§1.13: empty state (mid-Ramadan family join → "not applicable"), loading state (themed transition entering the window).

## 6. Existing Architecture
`:feature:ramadan` KMP module (Kotlin, Jetpack Compose, MVVM, Clean Architecture) per §6.1, depending on `:core:design-system`, `:core:network`, `:core:offline-cache`. Home re-theme is a design-token overlay applied to A.2's existing Home Composable tree, per `CORE_DESIGNSYSTEM_INSTRUCTIONS.md` — not a duplicated screen.

## 7. Existing Code to Reuse
- A.2's Home Composable/ViewModel (re-themed via token overlay, not forked)
- `:core:design-system`'s theming/token-swap mechanism (per `CORE_DESIGNSYSTEM_INSTRUCTIONS.md`)
- `:core:network`'s Retrofit/OkHttp client setup (per `CORE_NETWORK_INSTRUCTIONS.md`)
- `:core:navigation`'s existing nav-graph pattern (per `CORE_NAVIGATION_INSTRUCTIONS.md`)

## 8. Files to Create
- `feature/ramadan/presentation/countdown/RamadanCountdownScreen.kt`
- `feature/ramadan/presentation/countdown/RamadanCountdownViewModel.kt`
- `feature/ramadan/presentation/prepchecklist/PrepChecklistScreen.kt`
- `feature/ramadan/presentation/home/RamadanHomeThemeOverlay.kt`
- `feature/ramadan/presentation/campaign/RamadanCampaignViewModel.kt`
- `feature/ramadan/domain/usecase/GetCampaignStatusUseCase.kt`
- `feature/ramadan/data/repository/RamadanRepositoryImpl.kt`
- `feature/ramadan/data/remote/RamadanApi.kt`

## 9. Files to Modify
- A.2's Home Composable — add conditional Ramadan theme-overlay application point
- `:core:navigation`'s nav-graph — register Ramadan Countdown/Prep-Checklist routes

## 10. KMP Requirements
- **UI/Screen:** Countdown screen (days-remaining display), Prep Checklist screen (parent-facing setup steps), Home theme overlay (lantern/crescent-moon design tokens applied over A.2's existing layout).
- **ViewModel/State:** `RamadanCampaignViewModel` exposes an immutable, stable `RamadanCampaignState` (phase, current_night, hijri_start_date, eid_date) derived solely from `GetCampaignStatusUseCase` — no local date math anywhere.
- **Use Case/Repository:** `GetCampaignStatusUseCase` → `RamadanRepository.getCampaignStatus()` → `RamadanApi` (B-01).
- **Navigation:** Countdown/Prep-Checklist reachable from Home when phase is `pre_ramadan_countdown`; Home overlay applies automatically once phase is `active` or later.
- **Local Database:** cache last-known `RamadanCampaignState` in `:core:offline-cache` (per `CORE_DATABASE_INSTRUCTIONS.md`) for offline/cold-start display.
- **Offline First:** last-cached phase renders immediately on app open while a fresh fetch runs in the background; graceful fallback to standard (non-Ramadan) Home if no cached state and the fetch fails.
- **Empty State:** family joining mid-Ramadan — prior nights rendered as "not applicable," not missed (this sub-feature owns the Home-level messaging for that state; K-02 owns the Journey-Map-level rendering).
- **Loading State:** themed transition animation entering the activation window.
- **Error State:** `campaign-status` fetch failure with no cache → standard Home renders, no broken/blank Ramadan UI.

## 11. NextJS Requirements
N/A — this sub-feature is child/parent-app only.

## 12. API Contract
`GET /v1/ramadan/campaign-status` (B-01) → `{ phase, current_night, hijri_start_date, eid_date }`. No request parameters accepted client-side (region is server-resolved).

## 13. Database Requirements
Local cache table/entity: `RamadanCampaignCacheEntity(phase, current_night, hijri_start_date, eid_date, cached_at)` in the offline-cache local database (Room/SQLDelight per `CORE_DATABASE_INSTRUCTIONS.md`).

## 14. Validation
N/A client-side beyond standard response-schema validation (Retrofit + kotlinx.serialization per `CORE_NETWORK_INSTRUCTIONS.md`).

## 15. Authentication
Standard authenticated parent/child session token attached via `:core:network`'s existing interceptor — no Ramadan-specific auth handling.

## 16. Authorization
N/A beyond standard session validity.

## 17. Error Handling
Network failure → fall back to cached state, then to standard Home if no cache exists; never show a broken/partial Ramadan UI.

## 18. Offline First
Covered in §10 — cached phase state renders immediately; background refresh reconciles.

## 19. Local Data
`RamadanCampaignCacheEntity` per §13, invalidated/refreshed on every successful `campaign-status` fetch.

## 20. Localization
Countdown copy, checklist item text, and theme-overlay labels fully localized across English, Hindi, Arabic, Urdu via `:core:design-system`'s string-resource mechanism — zero hardcoded user-facing strings.

## 21. RTL
Full RTL mirroring for Arabic/Urdu — countdown layout, checklist item ordering, and theme-overlay iconography placement all direction-aware per `CORE_DESIGNSYSTEM_INSTRUCTIONS.md`.

## 22. Analytics
`ramadan_countdown_viewed`, `ramadan_prep_checklist_completed`, `ramadan_home_themed_viewed` per §1.19, fired via `:core:analytics`'s existing event-logging mechanism (per `CORE_ANALYTICS_INSTRUCTIONS.md`).

## 23. Performance
Theme-overlay application must not force a full Home recomposition — token swap only; `RamadanCampaignState` is `@Immutable`/`@Stable`-annotated to prevent unnecessary recomposition; countdown timer updates use a coroutine `Flow` with appropriate cancellation on screen exit (no leaked timers, per `CORE_CRASH_INSTRUCTIONS.md`'s ANR-prevention guidance).

## 24. Security
No sensitive data handled beyond the existing authenticated session; no local Hijri computation eliminates a class of client-side date-manipulation risk entirely.

## 26. Library Requirements
Kotlin, Jetpack Compose, Hilt, Retrofit + OkHttp, Room/SQLDelight (per existing `:core:offline-cache` choice) — no new libraries; explicitly no Hijri-calendar library in this module.

## 27. Testing
Unit: `RamadanCampaignViewModel` state derivation from mocked API responses for all six phases. **Mandatory structural test:** confirm no Hijri-calculation library import and no hardcoded Laylatul-Qadr night list exists anywhere in `:feature:ramadan`'s source (§7 Android AI prompt item 1). UI test: Countdown/Prep-Checklist/Home-overlay render correctly per phase; offline-cache fallback test.

## 28. Documentation
KDoc on `RamadanCampaignViewModel` explicitly stating it must never perform local date computation.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Scaffold `:feature:ramadan` Module**
Objective: Module skeleton with correct Gradle dependencies (`:core:reward-client`, `:core:design-system`, `:core:network`, `:core:offline-cache`). Files to Create: module `build.gradle.kts`. Definition of Done: module builds, dependencies resolve.

**Task 02 — Implement `RamadanApi` and `RamadanRepositoryImpl`**
Objective: Retrofit interface + repository wrapping B-01's endpoint. Files to Create: `data/remote/RamadanApi.kt`, `data/repository/RamadanRepositoryImpl.kt`. Existing Files to Reuse: `:core:network`'s client setup. Tests: repository unit tests with mocked responses. Definition of Done: tests pass.

**Task 03 — Implement Local Cache Entity and DAO**
Objective: `RamadanCampaignCacheEntity` persistence. Files to Create: cache entity/DAO in `:core:offline-cache`. Dependencies: Task 02. Tests: cache read/write tests. Definition of Done: tests pass.

**Task 04 — Implement `GetCampaignStatusUseCase`**
Objective: Cache-first, network-refresh use case. Files to Create: `domain/usecase/GetCampaignStatusUseCase.kt`. Dependencies: Task 02, Task 03. Tests: cache-fallback test. Definition of Done: test passes.

**Task 05 — Implement `RamadanCampaignViewModel`**
Objective: Immutable/stable state derivation, zero local date math. Files to Create: `presentation/campaign/RamadanCampaignViewModel.kt`. Dependencies: Task 04. Tests: **mandatory** — structural no-Hijri-library test; phase-derivation unit tests for all six phases. Definition of Done: both pass.

**Task 06 — Build Countdown, Prep Checklist, and Home Overlay Composables**
Objective: Three Composables consuming the ViewModel's state. Files to Create: `presentation/countdown/RamadanCountdownScreen.kt`, `presentation/prepchecklist/PrepChecklistScreen.kt`, `presentation/home/RamadanHomeThemeOverlay.kt`. Files to Modify: A.2's Home Composable (add overlay hook). Dependencies: Task 05. Tests: UI tests for phase-driven rendering. Definition of Done: tests pass.

**Task 07 — Wire Navigation**
Objective: Register routes in `:core:navigation`'s nav-graph. Files to Modify: nav-graph file. Dependencies: Task 06. Tests: navigation tests. Definition of Done: tests pass.

**Task 08 — Add Localization Strings (En/Hi/Ar/Ur) and RTL Verification**
Objective: Zero hardcoded strings, full RTL mirroring. Dependencies: Task 06. Tests: RTL layout test. Definition of Done: test passes.

**Task 09 — Add Analytics Instrumentation**
Objective: Wire the three §1.19 events. Dependencies: Task 06. Tests: analytics-event-fired test. Definition of Done: test passes.

**Task 10 — Add Full Test Suite and Final Code Review**
Objective: Complete coverage per §27, including the mandatory structural test. Definition of Done: all green in CI; checklist in §30 checked.

## 30. Final Verification Checklist
- [ ] No Hijri-calculation library or hardcoded Laylatul-Qadr night list anywhere in module source — mandatory structural test passing
- [ ] All state derived from server response, verified across all six phases
- [ ] Offline cache-first rendering with graceful fallback to standard Home
- [ ] Full En/Hi/Ar/Ur localization and RTL mirroring
- [ ] No unnecessary recomposition from the theme-overlay swap

## 31. Definition of Done
The Ramadan experience's entry point renders entirely from server-derived state, with zero client-side date computation and a graceful fallback path when the network or cache can't supply that state.
