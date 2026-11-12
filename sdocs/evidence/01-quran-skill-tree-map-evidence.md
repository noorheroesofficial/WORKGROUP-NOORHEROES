# Evidence: Quran & Arabic Skill Tree Map (Task K-01 / Feature A.5)

**Task**: `01-quran-skill-tree-map`  
**Parent PRD**: `PRD_Documents/Child App (1-12)/Feature_A5_Quran_Arabic_Learning.md`  
**Task Blueprint**: `Development_Blueprints/A5_Quran_Arabic_Learning/KMP/01-quran-skill-tree-map.md`  
**Consolidated Blueprint**: `NoorHeroes_Consolidated_Execution_Blueprint.md`  
**Design Reference Mockups**:
- `Screens/Mobile App/Learn/Skill Tree-01.png` (Online Returning Learner Top)
- `Screens/Mobile App/Learn/Skill Tree-02.png` (Online Returning Learner Scrolled + Placement Banner)
- `Screens/Mobile App/Learn/Skill Tree-03.png` (Loading Shimmer Skeleton Top)
- `Screens/Mobile App/Learn/Skill Tree-04.png` (Loading Shimmer Skeleton Scrolled + Bottom Placeholder)
- `Screens/Mobile App/Learn/Skill Tree-05.png` (First-Time Learner, 0 Progress Top)
- `Screens/Mobile App/Learn/Skill Tree-06.png` (First-Time Learner Scrolled + Placement Banner)
- `Screens/Mobile App/Learn/Skill Tree-07.png` (Offline Cached Fallback Top)
- `Screens/Mobile App/Learn/Skill Tree-08.png` (Offline Cached Fallback Scrolled + Reconnect CTA)  
**Date**: 2026-11-10  
**Status**: 100% AUDITED, VERIFIED & PASSING (`454/454` FULL SUITE PASSING; `0` STATIC AUDIT VIOLATIONS)

---

## 1. Verified Backend Contract, Concurrency, Offline/Search & Screen Inventory

### Backend Parity, Locale Forwarding & Auth/Race Hardening (Post-Audit Remediation)
- **Dual camelCase + snake_case Wire Codecs (`SkillTreeDtos.kt` — 236 lines)**: `NetworkJson` enforces `useAlternativeNames = false`; added custom `KSerializer`s (`MasterySummaryDtoSerializer`, `SkillNodeDtoSerializer`, `SkillTreeResponseDtoSerializer`) wrapping dual-field `*Wire` surrogates so both FastAPI `BaseSchema` camelCase (`domain`, `masterySummary`, `masteredCount`, `totalCount`, `nodeId`, `nodeType`, `subtitle`, `masteryScore`, `unlockCondition`, `prerequisiteNodeIds`, `lastPracticedAt`, `orderIndex`) and legacy snake_case decode deterministically, mapping `domain -> track` and preserving server `subtitle` (`SkillNode.subtitle`). Verified by `SkillTreeBackendParityContractTest` (`2/2`).
- **API Query, Locale Headers & Debug Fallback (`LearningApi.kt` — 57 lines, `HttpClientFactory.kt` — 335 lines)**: `LearningApi.getSkillTree(track, childId, locale)` emits both `domain` and `track` query parameters + `child_id` and forwards non-blank `Accept-Language` + `X-Locale` headers; `LocalDevFallbackHttpClientEngine` (`resolveLearningPathsFallbackJson(domain)`) serves domain-specific camelCase JSON with unique node UUIDs across `arabic`, `tajweed`, and `quran`.
- **ViewModel Locale, Cancellation & Auth Switching (`SkillTreeViewModel.kt` — 370 lines, `LearnModule.kt` — 53 lines, `GetSkillTreeUseCase.kt` — 33 lines)**: Injected optional `LocalizationProvider` (`getOrNull()`), cancelled overlapping `loadJob`s with post-await `getActiveChildId() == childId && state.value.activeTrack == track` checks, overrode `onAuthContextChanged` to cancel stale loads and automatically reload on sibling switch or clear nodes + set `SkillTreeErrorReason.NO_ACTIVE_CHILD` on logout, and replaced hardcoded English fallbacks with localized `SkillTreeErrorReason` enum states (preserving `CancellationException` rethrow in `LearningRepositoryImpl.kt`).
- **Empty-Cache Offline Honesty, Inline Search & RTL Icons (`SkillTreeScreen.kt` — 322 lines, `SkillTreeSearchAndStatusCards.kt` — 249 lines, `SkillTreeDialogs.kt` — 168 lines)**: Gated offline banners, `"Cached"` pills, hidden track dots, and `"Start with Al-Fatiha"` strictly on `hasCachedNodesOffline` (`(isOffline || isCachedFallback) && nodes.isNotEmpty()`) while empty-cache failures render `SkillTreeErrorState` with localized `SkillTreeErrorReason` copy (`values`, `values-ar`, `values-hi`, `values-ur`, `103` keys each). Wired the header Search button -> inline `SkillTreeSearchBar` filtering `SkillTreeUiState.visibleNodes`, and replaced `"▶"` in `PracticeModeCard` with `Icons.AutoMirrored.Rounded.KeyboardArrowRight`.

### Screen 01: `Skill Tree-01.png` (Online Returning Learner Top)
- **Top App Bar (`SkillTreeTopBar` in `SkillTreeHeaders.kt`)**:
  - Editorial serif title `"Quran Learning"` rendered via `NoorHeroesTheme.typography.brandSmall` (`FontWeight.Bold`, `semantics { heading() }`), backed by split `resolveTypography` (`Resolution.kt` keeps `brandSmall`..`brandHero` & `arBrand` on `FontFamily.Serif` while interface styles consume bundled Poppins sans via `rememberNoorSansFontFamily()` in `TypographyResources.kt` and `AppRoot.kt`).
  - Circular search button (`sizes.touchTarget`, `shapes.circle`, `surface`, `borderSubtle`) with Material `Icons.Rounded.Search` vector icon and localized `skill_tree_search_description`.
- **Mastery Status Header (`SkillTreeMasteryHeader` in `SkillTreeHeaders.kt`)**:
  - Golden badge pill (`nodeMasteredContainer`, `nodeMastered` border, `"⭐ X skills mastered"` via `skill_tree_skills_mastered_badge`, `streakSupport` text).
  - Right-aligned interactive `TrackDot` buttons (`"quran"`, `"arabic"`, `"tajweed"`), each wrapped in `noorHeroesTouchTarget()` with `Role.Tab` semantics.
- **Canvas, Sparkles & S-Curve Path (`SkillTreePathConnector.kt`, `SkillTreeScreen.kt`)**:
  - Warm `background` canvas with ornamental 8-point starbursts (`SkillTreeSparkleDecoration`, `clearAndSetSemantics {}`).
  - `CurvedSegmentConnector` renders row-local continuous cubic-bezier dashed connectors (`nodePathLine`) joining `[index - 1]`, `[index]`, and `[index + 1]` cleanly across `LazyColumn` scroll offsets and RTL layout direction via `calculateCurveOffsetFraction(index)` (centered `0f` at index `0`, organic alternation `±(0.76f + 0.14f * cos(index * 1.1f))` across `NoorHeroesTheme.spacing.skillTreeCurveAmplitude`).
- **Curved Node Items (`SkillNodeItem` in `SkillTreeComponents.kt`)**:
  - Uniform single-line `title` and localized `subtitle` (`resolveNodeSubtitleSpec` / `resolveLocalizedNodeSubtitle`) so row heights stay identical and S-curve segments join seamlessly.
  - `MASTERED` ("Al-Fatiha", "Al-Ikhlas"): double gold rings (`nodeMastered`), `nodeMasteredContainer` interior, top-right gold `Icons.Rounded.Check` badge.
  - `LEARNING` / `PRACTICING` ("Al-Asr", "Al-Falaq", "Al-Nas"): `Canvas` circular progress ring (`drawArc` from `-90f` clockwise over subtle track arc), optional focus halo (`shouldHighlightNodeHalo` + `nodeReadyContainer`), plus top-right `Icons.Rounded.PlayArrow` badge on `PRACTICING` nodes.
- **Persistent 5-Tab Child Bottom Navigation Shell (`LearnNavGraph.kt`, `PlaceholderScreens.kt`, `Navigation.kt`)**:
  - `QuranSkillTreeRoute` hosts `SkillTreeScreen(modifier = Modifier.weight(1f))` above `ChildMainBottomNavBar(selectedTab = ChildBottomTab.LEARN)` (`HOME`, `LEARN`, `STORIES`, `REWARDS`, `PROFILE`) backed by `NoorBottomNavBar` (`HorizontalDivider` `borderSubtle`, `heightIn(min = counter)`, icon+label `NoorTabItem`).

### Screen 02: `Skill Tree-02.png` (Online Returning Learner Scrolled)
- **Node State Treatments (`SkillTreeComponents.kt`)**:
  - `NEEDS_REFRESH` ("Tajweed 1"): double amber ring (`nodeNeedsRefresh`), soft parchment fill (`nodeNeedsRefreshContainer = PrimitiveColors.Parchment` in `NoorColorScheme.kt` Light, with Dark/NightSky/Garden variants in `DefaultPalettes.kt`), center rounded `radius12` info badge with `Icons.Rounded.Refresh`.
  - `LOCKED` ("Al-Kawthar"): neutral `nodeLockedContainer` fill with empty center and top-right bordered `Icons.Rounded.Lock` badge in `nodeMastered` gold.
- **Bottom Placement Card (`SkillTreePlacementPromptCard` in `SkillTreePlacementBanners.kt`)**:
  - `surface` rounded card (`shapes.radius16`) with dashed border (`drawBehind` `PathEffect.dashPathEffect`) and inline `primary` CTA routing to `PlacementCheckRoute` (single-dispatch navigation via `SkillTreeUiEvent.TakePlacementCheck`).

### Screens 03 & 04: `Skill Tree-03.png` & `Skill Tree-04.png` (Loading Shimmer Skeleton)
- **Top Skeleton (`SkillTreeLoadingHeaderSkeleton` in `SkillTreePathConnector.kt`)**:
  - Rendered inside `Scaffold.topBar` during initial fetch (`isInitialLoading && !isOfflineOrCached`): title pill shimmer + circular search placeholder + mastery badge pill shimmer + 3 track-dot placeholders.
- **Body Skeleton (`SkillTreeLoadingSkeleton` in `SkillTreePathConnector.kt`)**:
  - 4 curved S-connector skeleton nodes (`calculateCurveOffsetFraction` + `CurvedSegmentConnector` + `NoorSkeleton` circle, title bar, subtitle bar) followed by a dashed-border bottom card shimmer placeholder matching `Skill Tree-04.png`.

### Screens 05 & 06: `Skill Tree-05.png` & `Skill Tree-06.png` (First-Time Learner, 0 Progress)
- **Mastery Header & Card (`SkillTreeHeaders.kt`)**:
  - `masteredCount == 0` displays green `"🌱 Just getting started"` pill (`successSurface` / `success`) and renders `StartWithFatihaCard` (`🪔`, bold `h3` title, localized subtitle).
- **Nodes & Bottom Banner (`SkillTreeComponents.kt`, `SkillTreePlacementBanners.kt`)**:
  - First node (`SkillNodeState.READY`) renders cyan halo aura, reduced-motion-aware pulse (`LocalAdaptiveContext.current.accessibility.reduceMotion`), teal ring (`nodeReady`), and top-right `Icons.Rounded.PlayArrow` badge; downstream nodes render `LOCKED`; scrolled bottom shows *"Not sure where to start? Take a placement check →"*.

### Screens 07 & 08: `Skill Tree-07.png` & `Skill Tree-08.png` (Offline Cached Fallback)
- **Top Red Alert Banner (`SkillTreeOfflineBanner` in `SkillTreeHeaders.kt` & `SkillTreeScreen.kt`)**:
  - Full-width `errorContainer` banner extending cleanly behind status bar via `.noorHeroesSafeArea(bottom = false)`, displaying `Icons.Rounded.WifiOff`, `"Offline — showing cached progress"`, and compact `Retry` pill (`Icons.Rounded.Refresh`) with `noorHeroesTouchTarget()`.
- **Header & Sync Warning (`SkillTreeTopBar`, `SkillTreeMasteryHeader`, `SkillTreeOfflineSyncWarningCard`)**:
  - Search circle replaced with red-outlined `WifiOff` + `"Cached"` pill (`skill_tree_cached_pill`); `SkillTreeMasteryHeader(..., isOffline = true)` hides track selector dots; `SkillTreeOfflineSyncWarningCard` displays `WifiOff` + `warning` notice (`skill_tree_offline_sync_warning`).
- **Bottom Offline Placement Gate (`SkillTreeOfflinePlacementCard` in `SkillTreePlacementBanners.kt`)**:
  - Centered `"Placement check requires internet connection"` notice card plus full-width `PrimaryButton` (`"Try reconnecting"` with `Icons.Rounded.Refresh` `leadingIcon`).

---

## 2. Design System, Layer Purity & File Line Count Audit (`rule.md`)

Static audit executed after all code and documentation edits (`recheck_zero_gaps.py`, exit code `0`, `0` violations across `90` changed/untracked files in `NoorHeroes/`):

| Rule | Requirement | Audited Metric | Result |
| :--- | :--- | :---: | :---: |
| **Rule 1 (Zero Hardcoded Literals)** | No `Color(0x...)`, `Color.*`, `PrimitiveColors.*`, `.dp`, `.sp`, `RoundedCornerShape`, `CircleShape`, or M3 `Card`/`Button`/`AlertDialog` in feature UI | `0` violations across 90 files | **100% COMPLIANT** |
| **Rule 2 (Localization Parity)** | 100% key and format specifier parity across `values`, `values-ar`, `values-hi`, `values-ur` | `103/103` keys + identical `%1$d`/`%1$s` specifiers | **100% COMPLIANT** |
| **Rule 3 (Pure Architecture Layers)** | Zero `androidx.compose.*` / `core.designsystem.*` imports in models, DAO, DTO, API, Repository, UseCase, ViewModel, routes | `0` violations across pure layers | **100% COMPLIANT** |
| **Rule 5 (Touch Targets & A11y)** | $\ge 48\text{dp}$ touch targets, headings, non-color-only state badges, RTL mirroring, reduced-motion awareness | Verified in `SkillTree*.kt` | **100% COMPLIANT** |
| **Rule 8 (File Line Ceiling)** | Every `.kt`/`.xml`/updated `.md` touched/created strictly $< 500$ lines | Max audited file: `OnboardingNavGraph.kt` (`494` lines); K-01 UI max: `SkillTreeComponents.kt` (`478` lines) | **100% COMPLIANT** |

### Audited K-01 & Supporting Line Count Inventory (All $< 500$ Lines)
```text
core/core-common/src/commonMain/composeResources/{values,values-ar,values-hi,values-ur}/strings_learn.xml: 107 lines each (103 keys)
core/core-common/src/commonMain/kotlin/com/noorheroes/core/common/config/HttpQueryConstants.kt: 59 lines
core/core-common/src/commonMain/kotlin/com/noorheroes/core/common/model/SkillTreeModels.kt: 90 lines
core/core-network/src/commonMain/kotlin/com/noorheroes/core/network/api/LearningApi.kt: 57 lines
core/core-network/src/commonMain/kotlin/com/noorheroes/core/network/model/learning/SkillTreeDtos.kt: 236 lines
core/core-network/src/commonMain/kotlin/com/noorheroes/core/network/client/HttpClientFactory.kt: 335 lines
core/core-network/src/commonTest/kotlin/com/noorheroes/core/network/api/SkillTreeBackendParityContractTest.kt: 192 lines
core/core-data/src/commonMain/kotlin/com/noorheroes/core/data/repository/{LearningRepository.kt,LearningRepositoryImpl.kt}: 97 / 253 lines
core/core-data/src/androidHostTest/kotlin/com/noorheroes/core/data/repository/LearningRepositoryZeroMissingScenariosTest.kt: 299 lines
core/core-designsystem/src/commonMain/kotlin/com/noorheroes/core/designsystem/tokens/{Tokens.kt,Resolution.kt,NoorColorScheme.kt,AdaptiveHelpers.kt}: 466 / 309 / 200 / 49 lines
core/core-designsystem/src/commonMain/kotlin/com/noorheroes/core/designsystem/tokens/themes/DefaultPalettes.kt: 294 lines
core/core-designsystem/src/commonTest/kotlin/com/noorheroes/core/designsystem/tokens/ResolutionTest.kt: 140 lines
core/core-ui/src/commonMain/kotlin/com/noorheroes/core/ui/{component/Navigation.kt,foundation/TypographyResources.kt}: 281 / 27 lines
feature/feature-learn/README.md: 106 lines
feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/di/LearnModule.kt: 53 lines
feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/domain/GetSkillTreeUseCase.kt: 33 lines
feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/ui/skilltree/SkillTreeComponents.kt: 478 lines
feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/ui/skilltree/SkillTreeHeaders.kt: 451 lines
feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/ui/skilltree/SkillTreePathConnector.kt: 411 lines
feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/ui/skilltree/SkillTreeViewModel.kt: 370 lines
feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/ui/skilltree/SkillTreeScreen.kt: 322 lines
feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/ui/skilltree/SkillTreeSearchAndStatusCards.kt: 249 lines
feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/ui/skilltree/SkillTreePlacementBanners.kt: 168 lines
feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/ui/skilltree/SkillTreeDialogs.kt: 168 lines
feature/feature-learn/src/commonMain/kotlin/com/noorheroes/feature/learn/ui/skilltree/SkillTreeUiState.kt: 94 lines
feature/feature-learn/src/commonTest/kotlin/com/noorheroes/feature/learn/ui/skilltree/SkillTreeZeroMissingScenariosTest.kt: 451 lines
feature/feature-learn/src/commonTest/kotlin/com/noorheroes/feature/learn/ui/skilltree/SkillTreeEdgeCasesAndParityTest.kt: 250 lines
feature/feature-learn/src/commonTest/kotlin/com/noorheroes/feature/learn/ui/SkillTreeAndPlacementUiParityTest.kt: 129 lines
shared/src/commonMain/kotlin/com/noorheroes/app/navigation/LearnNavGraph.kt: 109 lines
shared/src/commonMain/kotlin/com/noorheroes/app/presentation/{AppRoot.kt,PlaceholderScreens.kt}: 251 / 341 lines
```

---

## 3. Zero-Missing Scenarios Verification Matrix

- **API Contract & Dev Fallback (`SkillTreeBackendParityContractTest` — 2/2, `HttpClientFactoryTest` — 17/17)**: Dual FastAPI camelCase (`domain`, `masterySummary`, `subtitle`, `nodeId`) + legacy snake_case deserialization under `useAlternativeNames = false`; dual `domain` + `track` query params; `Accept-Language` + `X-Locale` forwarding; per-track `/learning/paths?domain=...` debug fallback payloads.
- **Data & Offline Caching (`LearningRepositoryImplTest` — 3/3, `LearningRepositoryZeroMissingScenariosTest` — 10/10, `LearningRepositoryPlacementTest` — 7/7)**: Online fetch-then-cache updates; Room cache fallback (`isCachedFallback = true`); empty cache propagation; multi-track isolation across `(child_id, track)`; corrupted cache safety; server-authoritative mastery summary; idempotent cache writes; multi-child cache isolation; locale forwarding to `LearningApi`; `CancellationException` propagation; reactive `observeCachedSkillTree`.
- **ViewModel & Presentation (`SkillTreeViewModelTest` — 9/9, `SkillTreeZeroMissingScenariosTest` — 25/25, `SkillTreeEdgeCasesAndParityTest` — 7/7)**: Loading -> ready transitions; track switching with stale-list clearing; locked-node server unlock dialog; ready-node mode selector sheet; first-time vs returning banner visibility; deep-link `focusNodeId` -> `ScrollToNode` over `visibleNodes`; single-dispatch placement CTA navigation; empty/maintenance/unauthenticated error states (`SkillTreeErrorReason`); locale forwarding & override; track-switch & sibling-switch in-flight `loadJob` cancellation; logout reset; search toggle/filter/clear; server `subtitle` surfacing.
- **UI Parity & Design System (`SkillTreeScreenUiTest` — 16/16, `SkillTreeAndPlacementUiParityTest` — 4/4, `ResolutionTest` — 8/8)**:
  - `calculateCurveOffsetFraction`: centered `0f` start, bounded `[-1f, 1f]` left/right alternation matching `Skill Tree-01..08.png`.
  - `shouldHighlightNodeHalo`: explicit deep-link focus override, `READY`/`PRACTICING` + first `LEARNING` aura rules.
  - `resolveNodeSubtitleSpec` & `resolveNodeGlyph`: verified surah ayahs/letters/Tajweed subtitle classification, server subtitle fallback for custom nodes, and RTL vector icons.
  - `ResolutionTest`: split editorial `FontFamily.Serif` on `brandSmall`..`brandHero` even when `BrandOverride(fontFamily = ...)` supplies sans-serif UI typography.

---

## 4. Empirical Build & Test Results

Executed across all affected KMP modules + Android application compile/DI check after the final KMP code & documentation edit:

```powershell
$env:JAVA_HOME = 'C:\Program Files\Java\jdk-21'; cd NoorHeroes; .\gradlew.bat :core:core-common:testAndroidHostTest :core:core-designsystem:testAndroidHostTest :core:core-database:testAndroidHostTest :core:core-network:testAndroidHostTest :core:core-data:testAndroidHostTest :core:core-ui:testAndroidHostTest :core:core-navigation:testAndroidHostTest :feature:feature-learn:testAndroidHostTest :shared:testAndroidHostTest :androidApp:compileDevDebugKotlin :androidApp:testDevDebugUnitTest --console=plain
```

**Observed Result**: `BUILD SUCCESSFUL in 45s` (`344 actionable tasks: 34 executed, 1 from cache, 309 up-to-date`).

**JUnit XML Totals (`0` failures, `0` errors, `0` skipped)**:
- `:core:core-common:testAndroidHostTest`: **88/88** passed (23 suites)
- `:core:core-designsystem:testAndroidHostTest`: **31/31** passed (7 suites; `ResolutionTest` **8/8**)
- `:core:core-database:testAndroidHostTest`: **31/31** passed (8 suites)
- `:core:core-network:testAndroidHostTest`: **79/79** passed (17 suites; `SkillTreeBackendParityContractTest` 2/2, `HttpClientFactoryTest` 17/17)
- `:core:core-data:testAndroidHostTest`: **80/80** passed (12 suites; `LearningRepositoryZeroMissingScenariosTest` 10/10)
- `:core:core-ui:testAndroidHostTest`: **19/19** passed (4 suites)
- `:core:core-navigation:testAndroidHostTest`: **7/7** passed (1 suite)
- `:feature:feature-learn:testAndroidHostTest`: **107/107** passed (8 suites: `SkillTreeScreenUiTest` 16/16, `SkillTreeViewModelTest` 9/9, `SkillTreeZeroMissingScenariosTest` 25/25, `SkillTreeEdgeCasesAndParityTest` 7/7, `SkillTreeAndPlacementUiParityTest` 4/4, `PlacementCheckViewModelTest` 12/12, `PlacementCheckZeroMissingScenariosTest` 22/22, `PlacementCheckEdgeCasesTest` 12/12)
- `:shared:testAndroidHostTest`: **11/11** passed (5 suites: `EndToEndOnboardingProfileRewardsQaTest` 5/5, `LearnNavigationHelperTest` 2/2, `AnalyticsCompositionTest` 2/2, `SharedCommonTest` 1/1, `SharedLogicAndroidHostTest` 1/1)
- `:androidApp:testDevDebugUnitTest`: **1/1** passed (`KoinModuleCheckTest`) + `:androidApp:compileDevDebugKotlin` clean
- **Grand Total**: **454/454 passing (`100%` green)**

*Verification scope note*: Windows host unit tests, Koin graph validation, and Android debug Kotlin compilation are empirically verified; live Android device/emulator screenshot UI tests (`androidDeviceTest`) and macOS/Xcode iOS compilation/runtime were not executed on this Windows host.

---

## 5. Protected Boundaries Integrity
- `PRD_Documents/`: **Untouched** (0 modified, 0 created, 0 deleted).
- `Development_Blueprints/`: **Untouched** (0 modified, 0 created, 0 deleted).
- `Screens/`: **Untouched** (0 modified, 0 created, 0 deleted).
- `NoorHeroes/docs/prompt-kmp.md`: **Untouched**.
