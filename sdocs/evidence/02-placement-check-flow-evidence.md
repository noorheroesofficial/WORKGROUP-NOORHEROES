# Evidence: Placement Check Flow (Task K-02 / Feature A.5)

**Task**: `02-placement-check-flow`  
**Parent PRD**: `PRD_Documents/Child App (1-12)/Feature_A5_Quran_Arabic_Learning.md`  
**Task Blueprint**: `Development_Blueprints/A5_Quran_Arabic_Learning/KMP/02-placement-check-flow.md`  
**Backend Alignment**: `NoorHeroes-Backend/src/noorheroes/modules/learning/api.py`, `placement_check_schemas.py`, `placement_check_service.py` (`GET /v1/learning/placement-check/questions`, `POST /v1/learning/placement-check`)  
**Design Reference Mockups**:
- `Screens/Mobile App/Quiz Engine/Quiz Question-01.png` (Interactive diagnostic question card, metadata chips, choice badges)
- `Screens/Mobile App/Quiz Engine/Quiz Question-02.png`, `03.png`, `04.png` (Selected choice border/elevation confirmation & sticky bottom bar with directional arrow CTA)
- `Screens/Mobile App/Quiz Engine/Quiz Complete-01.png`, `02.png` (Full-bleed dark-teal celebration hero, confetti accent canvas, serif headline, progress strip, sticky primary CTA)
- `Screens/Mobile App/Learn/Feedback.png` (Tajweed/coaching accent notice card framing)
- `Screens/Mobile App/Learn/Skill Tree-02.png`, `05.png`, `06.png`, `08.png` (K-01 entry & offline placement gates)  
**Date**: 2026-11-10  
**Status**: AUDITED, TESTED & PASSING (`454/454` VERIFIED TESTS ACROSS 10 MODULES; `0` STATIC AUDIT VIOLATIONS)

---

## 1. Key Fixes & Backend/UI Alignment Implemented

1. **HTTP `Accept-Language`, `X-Locale` & Local Dev Fallback (`HttpClientFactory.kt`, `ContentLearningApiService.kt`, `HttpClientFactoryTest.kt`)**:
   - Moved fallback `Accept-Language` injection from Ktor `defaultRequest` into `CONNECTIVITY_CHECK` `onRequest` (`if (request.headers[ACCEPT_LANGUAGE] == null)`), ensuring localized requests (`ar`, `ur`, `hi`) transmit clean single-value `Accept-Language` and `X-Locale` headers while blank/`null` locales fall back cleanly to `"en"`.
   - Active child language is read dynamically from `LocalizationProvider` inside `PlacementCheckViewModel` and forwarded through `SubmitPlacementCheckUseCase` and `LearningRepository.submitPlacementCheck(childId, responses, locale)`.
   - Added debug-build `LocalDevFallbackHttpClientEngine` fallbacks for `/learning/placement-check/questions`, `/learning/placement-check`, and `/learning/paths` (returning 3 distinct UUID nodes matching `provisionalStates`), plus `enableInspektify: Boolean = true` parameter in `provideHttpClient`.
   - Eliminated a concurrent `401` timing race in `HttpClientFactoryTest.kt` (`concurrent 401s trigger exactly one refresh call`) via suspending `delay(50)` token transition (`"old"` -> `"new"`), conditional `MockEngine` `200 OK` on `"Bearer new"`, and scoped `awaitAll(async { ... }, async { ... })` verification (`17/17` green).

2. **Full FastAPI `_envelope` 409/422 Parity & Granular Error Mapping (`PlacementCheckDtos.kt`, `ContentLearningApiService.kt`, `PlacementCheckViewModel.kt`)**:
   - Normalized `200 OK` and `409 Conflict` payloads across camelCase, snake_case, flat `error.details`, nested `error.details.priorResult` / `prior_result`, root `detail`/`details`, and envelope metadata (`requestId`, `traceId`, `timestamp`).
   - Verified via `PlacementCheckBackendParityContractTest` that Pydantic/validation HTTP `422` envelopes containing JSON-array `details` map cleanly to `AppError.Validation` without JSON parsing crashes, and wire JSON request payloads match backend schemas.
   - Mapped `AppError.Auth.RestrictionFailed` & `AppError.Auth.Forbidden` (with `CHILD_SCOPE_VIOLATION` distinguished cleanly) to `PlacementErrorReason.ACCESS_RESTRICTED` / `MISSING_CHILD`, `AppError.RateLimited` to `PlacementErrorReason.RATE_LIMITED`, `AppError.NotFound` to `PlacementErrorReason.MISSING_CHILD`, preserved safe `AppError.Server.Maintenance` messages, and hid raw technical strings on `AppError.Unknown` (`95/95` localized keys across `en`, `ar`, `hi`, `ur`).

3. **Cross-Track K-01 Room Cache Invalidation & Concurrency Safety (`SkillNodeCacheDao.kt`, `LearningRepositoryImpl.kt`, `PlacementCheckViewModel.kt`)**:
   - Added `SkillNodeCacheDao.clearAllNodesForChild(childId)` so placement completion invalidates Quran, Arabic, and Tajweed tracks together (`skill_node_cache` rows cleared cleanly per `childId`) with `CancellationException` propagation and non-fatal legacy path refresh.
   - Tracked and cancelled both `loadJob` and `submitJob` inside `PlacementCheckViewModel` (`onAuthContextChanged`, `loadQuestions`, `startFromBeginning`), scoped `SavedStateHandle` persistence strictly by `KEY_CHILD_ID` (`isSavedProgressForActiveChild` prevents cross-sibling process-death leaks across `scenario004`–`007`, `010`, and `scenario034`), added post-await `resolveChildId() == childId` ownership checks before emitting state/navigation, and guarded duplicate `Submit` and `StartFromBeginning` rapid double-taps (`hasBypassedToDefault`).
   - Selecting an option or advancing immediately dismisses any prior `PlacementErrorReason.VALIDATION` banner.

4. **Quiz Question & Completion Visual Parity (`Quiz Question-01..04.png`, `Quiz Complete-01..02.png`)**:
   - **Full-Bleed Completion Routing (`PlacementCheckScreen.kt` — 298 lines)**: Hoisted `state.isCompleted` outside `.noorHeroesSafeArea()` + `widthIn(max = NoorHeroesTheme.sizes.formMax)` so the celebration banner extends full-bleed across the top status bar and tablet widths, while loading, empty/offline, and question steps remain safe-area protected and centered within `formMax`.
   - **Celebration Hero & Summary Layout (`PlacementCheckCompletionCard.kt` — 308 lines)**: Pinned full-bleed `colors.primary` hero with `.noorHeroesSafeArea(bottom = false)`, deterministic `Canvas` confetti dots (`colors.accent` / `colors.nodeReady`), editorial serif `NoorHeroesTheme.typography.brandSmall` celebration headline, translucent completed-count pill, `formMax`-capped scrollable summary + Edge Case 9 Tajweed provisional notice cards, and sticky `formMax` bottom actions (`.noorHeroesSafeArea(top = false)`) featuring `Icons.Rounded.PlayArrow` `leadingIcon` on `PrimaryButton`.
   - **Metadata Pill & Bottom CTA Polish (`PlacementCheckComponents.kt` — 409 lines, `PlacementCheckStatusCards.kt` — 334 lines)**: Removed border stroke on the `"Multiple Choice"` pill (`surfaceSunken` fill only, matching `Quiz Question-01..02.png`), added RTL-aware `Icons.AutoMirrored.Rounded.ArrowForward` `trailingIcon` to `PlacementBottomBar`'s `PrimaryButton` (`Next Question →` / `Submit →`, matching `Quiz Question-03..04.png`), and paired bundled Poppins sans typography (`AppRoot.kt` / `TypographyResources.kt`) with serif editorial display headlines (`Resolution.kt`).
   - **Shared `BackPressHandler` & A11y (`core:core-ui`)**: Promoted cross-platform `@Composable expect fun BackPressHandler` into `core:core-ui` (`com.noorheroes.core.ui.foundation`), handled `totalSteps > 10` fallback indicator & empty question option lists (`canAdvanceCurrentStep`), grouped choices in `selectableGroup()`, and annotated `heading()` / `LiveRegionMode.Polite` / `Role.RadioButton`.

5. **Single-Dispatch Navigation, 5-Tab Child Bottom Nav Integration & Deep Links**:
   - Fixed double-navigation dispatch on `TakePlacementCheck` in `LearnModule.kt` and `SkillTreeViewModel.kt`; `LearnNavGraph.learnNavGraph` (`navigateToFreshSkillTree`) pops stale `QuranSkillTreeRoute`/`PlacementCheckRoute` entries with `launchSingleTop = true` and forwards `recommendedStartingNodes.firstOrNull()` as `focusNodeId`.
   - Wired `ChildBottomTab.LEARN` -> `QuranSkillTreeRoute()` across `ChildMainBottomNavBar` (`PlaceholderScreens.kt`, `LearnNavGraph.kt`, `OnboardingNavGraph.kt`, `RewardsNavGraph.kt`, `AppRoot.kt`) and verified all 5 child tabs in `EndToEndOnboardingProfileRewardsQaTest` Scenario 3.
   - Added `LearnDeepLinkParser` (`noorheroes://learn`, `noorheroes://learn/placement-check`, `noorheroes://learn/node/{node_id}` with strict host boundary), shared `LearnNavigationHelper`, `AndroidManifest.xml` intent filters, `MainActivity.kt` intent/URI dispatch, and `NoorHeroesApp.kt` (`handleDeepLinkIOS`).

---

## 2. Design System, Layer Purity & File Line Count Audit (`rule.md`)

Static audit executed after all code and documentation edits (`recheck_zero_gaps.py`, exit code `0`, `0` violations across `90` changed/untracked files in `NoorHeroes/`):

| Rule | Requirement | Audited Metric | Result |
| :--- | :--- | :---: | :---: |
| **Rule 1 (Zero Raw Literals)** | No `Color(0x...)`, `Color.*`, `PrimitiveColors.*`, `.dp`, `.sp`, `RoundedCornerShape`, `CircleShape`, or M3 `Card`/`Button`/`AlertDialog` imports in feature UI | `0` violations across 90 files | **100% COMPLIANT** |
| **Rule 2 (4-Locale + Format Parity)** | Equal string key sets & `%1$d`/`%1$s` format placeholders across `values`, `values-ar`, `values-hi`, `values-ur` | `103/103` unique keys + identical placeholders | **100% COMPLIANT** |
| **Rule 3 (Pure Architecture Layers)** | Zero `androidx.compose.*` or `core.designsystem.*` imports in DAO, DTO, API, Repository, UseCase, ViewModel, Navigation routes/helpers | `0` violations across pure layers | **100% COMPLIANT** |
| **Rule 5 (Touch Targets & A11y)** | $\ge 48\text{dp}$ targets, `Role.RadioButton`, `selectableGroup`, `heading()`, `LiveRegionMode.Polite`, RTL Material icons, `noorHeroesSafeArea`, `formMax`, `BackPressHandler` | Verified in `PlacementCheck*.kt` | **100% COMPLIANT** |
| **Rule 8 (File Line Ceiling)** | Every touched/created file strictly $< 500$ lines | Max file: `OnboardingNavGraph.kt` (`494` lines); K-02 test max: `PlacementCheckZeroMissingScenariosTest.kt` (`473` lines); UI max: `PlacementCheckComponents.kt` (`409` lines) | **100% COMPLIANT** |
| **Protected Directories** | Zero edits in `PRD_Documents/`, `Development_Blueprints/`, `Screens/`, `NoorHeroes/docs/prompt-kmp.md` | `0` modified/deleted/created | **100% COMPLIANT** |

### Key Audited File Line Counts (All $< 500$ Lines)
- `core/core-common/src/commonMain/composeResources/{values,values-ar,values-hi,values-ur}/strings_learn.xml`: 107 lines each (103 keys)
- `core/core-designsystem/src/commonMain/kotlin/com/noorheroes/core/designsystem/tokens/{Tokens.kt,Resolution.kt,NoorColorScheme.kt}`: 466 / 309 / 200 lines
- `core/core-designsystem/src/commonMain/kotlin/com/noorheroes/core/designsystem/tokens/themes/DefaultPalettes.kt`: 294 lines
- `core/core-designsystem/src/commonTest/kotlin/com/noorheroes/core/designsystem/tokens/ResolutionTest.kt`: 140 lines
- `core/core-ui/{build.gradle.kts,CORE_UI_INSTRUCTIONS.md}`: 33 / 263 lines
- `core/core-ui/src/commonMain/kotlin/com/noorheroes/core/ui/{component/Navigation.kt,foundation/BackPressHandler.kt,foundation/TypographyResources.kt}`: 281 / 19 / 27 lines
- `core/core-ui/src/{androidMain,iosMain}/kotlin/com/noorheroes/core/ui/foundation/BackPressHandler.{android,ios}.kt`: 12 / 11 lines
- `core/core-database/src/commonMain/kotlin/com/noorheroes/core/database/dao/SkillNodeCacheDao.kt`: 46 lines
- `core/core-network/src/commonMain/kotlin/com/noorheroes/core/network/{model/learning/PlacementCheckDtos.kt,api/ContentLearningApiService.kt,client/HttpClientFactory.kt}`: 146 / 262 / 335 lines
- `core/core-network/src/commonTest/kotlin/com/noorheroes/core/network/{api/PlacementCheckApiServiceTest.kt,api/PlacementCheckBackendParityContractTest.kt,client/HttpClientFactoryTest.kt}`: 396 / 188 / 477 lines
- `core/core-data/src/commonMain/kotlin/com/noorheroes/core/data/repository/{LearningRepository.kt,LearningRepositoryImpl.kt}`: 97 / 253 lines
- `core/core-data/src/androidHostTest/kotlin/com/noorheroes/core/data/repository/LearningRepositoryPlacementTest.kt`: 243 lines
- `feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/{di/LearnModule.kt,domain/SubmitPlacementCheckUseCase.kt}`: 53 / 86 lines
- `feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/ui/placement/{PlacementCheckUiState.kt,PlacementCheckViewModel.kt,PlacementCheckScreen.kt,PlacementCheckComponents.kt,PlacementCheckStatusCards.kt,PlacementCheckCompletionCard.kt}`: 93 / 441 / 298 / 409 / 334 / 308 lines
- `feature/feature-learn/src/commonTest/kotlin/com/noorheroes/feature/learn/ui/{SkillTreeAndPlacementUiParityTest.kt,placement/PlacementCheckTestFakes.kt,placement/PlacementCheckViewModelTest.kt,placement/PlacementCheckZeroMissingScenariosTest.kt,placement/PlacementCheckEdgeCasesTest.kt}`: 129 / 250 / 274 / 473 / 401 lines
- `core/core-navigation/src/commonMain/kotlin/com/noorheroes/core/navigation/LearnRoutes.kt`: 76 lines
- `shared/build.gradle.kts` & `shared/src/commonMain/kotlin/com/noorheroes/app/{navigation/LearnNavGraph.kt,navigation/LearnNavigationHelper.kt,navigation/OnboardingNavGraph.kt,navigation/RewardsNavGraph.kt,presentation/PlaceholderScreens.kt,presentation/AppRoot.kt}`: 81 / 109 / 70 / 494 / 254 / 341 / 251 lines
- `shared/src/iosMain/kotlin/com/noorheroes/app/NoorHeroesApp.kt` & `shared/src/commonTest/.../{LearnNavigationHelperTest.kt,EndToEndOnboardingProfileRewardsQaTest.kt}`: 78 / 101 / 226 lines
- `androidApp/src/main/{AndroidManifest.xml,kotlin/com/noorheroes/app/MainActivity.kt}`: 47 / 196 lines

---

## 3. Zero-Missing Scenarios Verification Matrix

- **API, Network & Local Dev Fallback (`PlacementCheckApiServiceTest` — 10/10, `PlacementCheckBackendParityContractTest` — 3/3, `HttpClientFactoryTest` — 17/17)**: Single-value localized `Accept-Language` & `X-Locale` headers; camelCase/snake_case 200 & 409 normalization; Pydantic array-`details` 422 mapping; FastAPI `_envelope` support; debug-build domain-aware local fallback; deterministic single-refresh under concurrent 401s.
- **Repository & Cache Invalidation (`LearningRepositoryPlacementTest` — 7/7)**: Locale forwarding; cross-track Room invalidation (`clearAllNodesForChild`); child partition isolation; non-fatal cache refresh errors.
- **Domain, ViewModel, UI Parity, Concurrency, Error Mapping, Navigation & DI (`PlacementCheckViewModelTest` — 12/12, `PlacementCheckZeroMissingScenariosTest` — 22/22, `PlacementCheckEdgeCasesTest` — 12/12, `SkillTreeScreenUiTest` — 16/16, `SkillTreeAndPlacementUiParityTest` — 4/4, `ResolutionTest` — 8/8, `LearnNavigationHelperTest` — 2/2, `EndToEndOnboardingProfileRewardsQaTest` — 5/5, `KoinModuleCheckTest` — 1/1)**: S-A05-K02-001 through S-A05-K02-034 (including cross-child `SavedStateHandle` `KEY_CHILD_ID` leak protection), 5-tab child bottom navigation shell, deep-link routing, and Quiz Question/Completion design parity.

---

## 4. Empirical Build & Test Results

Executed after the final KMP code & documentation edit:

```powershell
$env:JAVA_HOME = 'C:\Program Files\Java\jdk-21'; cd NoorHeroes; .\gradlew.bat :core:core-common:testAndroidHostTest :core:core-designsystem:testAndroidHostTest :core:core-database:testAndroidHostTest :core:core-network:testAndroidHostTest :core:core-data:testAndroidHostTest :core:core-ui:testAndroidHostTest :core:core-navigation:testAndroidHostTest :feature:feature-learn:testAndroidHostTest :shared:testAndroidHostTest :androidApp:compileDevDebugKotlin :androidApp:testDevDebugUnitTest --console=plain
```

**Observed Gradle Result**: `BUILD SUCCESSFUL in 45s` (`344 actionable tasks: 34 executed, 1 from cache, 309 up-to-date`).

**JUnit XML Suite Verification Summary (`0` failures, `0` errors, `0` skipped)**:
- `:core:core-common:testAndroidHostTest`: **88/88** passed across 23 test suites.
- `:core:core-designsystem:testAndroidHostTest`: **31/31** passed across 7 test suites (`ResolutionTest`: **8/8**).
- `:core:core-database:testAndroidHostTest`: **31/31** passed across 8 test suites.
- `:core:core-network:testAndroidHostTest`: **79/79** passed across 17 test suites (`PlacementCheckApiServiceTest`: 10/10, `PlacementCheckBackendParityContractTest`: 3/3, `SkillTreeBackendParityContractTest`: 2/2, `HttpClientFactoryTest`: 17/17, `ContentLearningApiServiceImplTest`: 2/2).
- `:core:core-data:testAndroidHostTest`: **80/80** passed across 12 test suites (`LearningRepositoryPlacementTest`: 7/7, `LearningRepositoryImplTest`: 3/3, `LearningRepositoryZeroMissingScenariosTest`: 10/10).
- `:core:core-ui:testAndroidHostTest`: **19/19** passed across 4 test suites.
- `:core:core-navigation:testAndroidHostTest`: **7/7** passed across 1 test suite (`NavigatorIntegrationTest`: 7/7).
- `:feature:feature-learn:testAndroidHostTest`: **107/107** passed across 8 test suites (`PlacementCheckViewModelTest`: 12/12, `PlacementCheckZeroMissingScenariosTest`: 22/22, `PlacementCheckEdgeCasesTest`: 12/12, `SkillTreeScreenUiTest`: 16/16, `SkillTreeViewModelTest`: 9/9, `SkillTreeZeroMissingScenariosTest`: 25/25, `SkillTreeEdgeCasesAndParityTest`: 7/7, `SkillTreeAndPlacementUiParityTest`: **4/4**).
- `:shared:testAndroidHostTest`: **11/11** passed across 5 test suites (`LearnNavigationHelperTest`: 2/2, `EndToEndOnboardingProfileRewardsQaTest`: 5/5, `AnalyticsCompositionTest`: 2/2, `SharedCommonTest`: 1/1, `SharedLogicAndroidHostTest`: 1/1).
- `:androidApp:testDevDebugUnitTest` (`KoinModuleCheckTest`): **1/1** passed (full Robolectric Koin graph verification) + `:androidApp:compileDevDebugKotlin` clean.
- **Grand Total**: **454/454 verified tests passing (`100%` green)**.

*Verification scope note*: On-device Compose UI instrumentation tests (`androidDeviceTest`), iOS/Xcode compilation, and live backend staging integration were not executed in this Windows host environment.
