# K-05 — Parent-Gated Achievement Sharing Flow

## 1. Feature Context
Part of Feature A.11 — Rewards System. Lets a parent generate and share a PII-free achievement card via the OS share sheet, gated behind PIN/biometric step-up verification.

## 2. Parent Feature
A.11 Rewards System — KMP App (Android/iOS)

## 3. Sub-feature
K-05 Parent-Gated Achievement Sharing Flow

## 4. Objective
Build the Shareable Achievement Card Preview and Parent Gate modal (§1.18 #8–9), routing to the OS share sheet only after verification succeeds, backing FR-12.

## 5. Business Requirements
- Card preview never renders any PII (child ID, DOB, location).
- Parent Gate appears before card generation; cancel returns to Achievements without generating a card.
- OS share sheet invoked only after the gate passes.

## 6. Existing Architecture
`feature-rewards` module. Reuses the platform's existing PIN/biometric elevated-session flow (already built for A.1's Parent PIN/Biometric Gate) rather than building a new verification UI.

## 7. Existing Code to Reuse
- A.1's Parent PIN/Biometric elevated-session Composable/flow (reused, not reimplemented).
- K-01's `AchievementSharingRepository`.
- Platform OS share-sheet intent/API (native per-platform, invoked via `expect`/`actual`).

## 8. Files to Create
- `feature-rewards/src/commonMain/kotlin/.../sharing/ShareCardPreviewScreen.kt`
- `feature-rewards/src/commonMain/kotlin/.../sharing/ShareCardViewModel.kt`
- `feature-rewards/src/commonMain/kotlin/.../sharing/ShareCardUiState.kt`
- `feature-rewards/src/commonTest/kotlin/.../sharing/ShareCardPiiExclusionUiTest.kt`
- `feature-rewards/src/commonTest/kotlin/.../sharing/ShareCardViewModelTest.kt`
- `feature-rewards/src/commonTest/kotlin/.../sharing/ShareCardTestFakes.kt`
- `core-navigation/src/commonMain/kotlin/.../navigation/RewardsRoutes.kt`
- `core-ui/src/commonMain/kotlin/.../component/ParentPinGateModal.kt`
- `core-ui/src/commonMain/kotlin/.../platform/ShareSheetLauncher.kt`
- `core-ui/src/androidMain/kotlin/.../platform/ShareSheetLauncher.android.kt`
- `core-ui/src/iosMain/kotlin/.../platform/ShareSheetLauncher.ios.kt`

## 9. Files to Modify
- `core-navigation` `Route.kt` — extracted modular rewards routes to keep < 500 lines.
- `feature-rewards` `BadgeDetailScreen.kt` — wired share button callback with badge title and emblem.
- `feature-profile` `ParentPinGateModal.kt` — delegated to canonical `core-ui` modal.
- `feature-rewards` `RewardsModule.kt` — registered `ShareCardViewModel`.
- `shared` `AppRoot.kt` & `DummyUI.kt` — registered destination `composable<ShareCardPreviewRoute>`.
- `core-common` `strings_rewards.xml` — localized across EN, AR, HI, UR (192 keys total, 100% parity).

## 10. Backend Requirements
Consumes B-08 (`POST /v1/achievements/{id}/share-card`).

## 11. KMP Requirements
- `ShareCardViewModel` triggers the existing A.1 Parent Gate flow before calling `AchievementSharingRepository`; on gate cancel, returns to Achievements with no API call made.
- Card preview Composable renders only the fields present in `ShareCardResponse` (image URL) — no client-side compositing of additional child data onto the card.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
`POST /v1/achievements/{id}/share-card` (B-08), called only after the elevated-session gate passes.

## 14. Database Requirements (Local)
None — share-card generation is always online, no local caching of generated cards.

## 15. Validation
UI test asserting the card preview screen never renders any element bound to child ID/DOB/location data — since the response itself excludes these fields (B-08 §15), this is primarily a regression guard against a future client-side compositing mistake.

## 16. Authentication
Reuses shared `core-network` Bearer token attachment (parent session).

## 17. Authorization
Requires the existing elevated-session gate (A.1) to have been freshly passed before the API call fires.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Gate cancelled | Return to Achievements, no API call made |
| Card generation API failure | Retry affordance shown, no partial/broken card displayed |
| Share-sheet invocation failure (platform-level) | Graceful fallback message, card remains available to retry sharing |

## 19. Offline First
Requires connectivity; no offline path for this flow (matches B-08 §19).

## 20. Local Data
N/A (no local persistence of generated cards).

## 21. Localization
Card preview surrounding UI (buttons, gate copy) localized EN/HI/AR/UR; card image text itself is server-rendered per B-08 §21 in the active locale.

## 22. RTL
Preview screen layout mirrors correctly for Arabic/Urdu.

## 23. Analytics
`achievement_share_gate_opened` (on gate modal open), `achievement_share_completed` (on successful share-sheet invocation, tied to a confirmed card-generation response).

## 24. Performance
N/A beyond standard screen-transition budgets; card generation latency handled via a loading state.

## 25. Security
Reuses the existing, already-audited A.1 elevated-session mechanism rather than building a parallel verification path — reduces security-review surface area.

## 26. Library Requirements
Compose Multiplatform, Koin, platform share-sheet API (`expect`/`actual`).

## 27. Testing
- Unit: gate-cancel-returns-without-API-call test.
- UI: PII-exclusion regression guard test (mandatory).
- Integration: gate pass → card generation → share-sheet invocation flow.

## 28. Documentation
KDoc noting this flow deliberately reuses A.1's existing gate rather than introducing a second verification implementation.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Wire Existing A.1 Parent Gate into This Flow**
- Objective: reuse, not reimplement, elevated-session verification.
- Existing Files to Reuse: A.1's Parent PIN/Biometric gate Composable/flow.
- Files to Create: `ShareCardViewModel.kt` (orchestrates gate → API call sequencing).
- Do Not Change: A.1's gate implementation itself.
- Definition of Done: gate correctly gates the API call; cancel path makes no call.

**Task 02 — Implement `ShareCardPreviewScreen`**
- Files to Create: `ShareCardPreviewScreen.kt`
- Implementation Details: renders only `ShareCardResponse` fields; loading/error states.
- Tests: PII-exclusion regression UI test (mandatory).
- Definition of Done: test passing.

**Task 03 — Wire OS Share Sheet Invocation**
- Implementation Details: platform `expect`/`actual` share-sheet call, invoked only post-gate.
- Definition of Done: share sheet correctly invoked with the card image URL.

**Task 04 — Wire Navigation & Analytics**
- Files to Modify: `core-navigation` `Route` registry.
- Analytics: `achievement_share_gate_opened`, `achievement_share_completed`.
- Definition of Done: navigation and analytics verified.

**Task 05 — Final Code Review**
- Expected Result: PR merge-ready.

## 30. Definition of Done
Share flow live, correctly gated, PII-exclusion regression-guarded, share-sheet invocation verified.

## 31. Final Verification Checklist
- [x] Gate reused from A.1, not reimplemented
- [x] Cancel path makes no API call
- [x] PII-exclusion regression UI test passes
- [x] Share sheet invoked only after successful gate + card generation
- [x] Localization/RTL verified (EN, AR, HI, UR 100% synchronized)
- [x] Analytics events fire correctly (`achievement_share_gate_opened`, `achievement_share_completed`)

## 32. Implementation Summary
- **Module & Package**: `feature:feature-rewards` (`com.noorheroes.feature.rewards.sharing`), `core:core-ui` (`com.noorheroes.core.ui.component`, `com.noorheroes.core.ui.platform`), `core:core-navigation` (`com.noorheroes.core.navigation`).
- **Core Architecture & MVI Flow**:
  - `ShareCardPreviewRoute` registered with modular `RewardsRoutes.kt` (82 lines), reducing `Route.kt` to 412 lines (well below the 500-line ceiling).
  - Canonical `ParentPinGateModal` consolidated in `core-ui` (250 lines), removing code duplication across `feature-profile` and `feature-rewards`.
  - Platform-agnostic `ShareSheetLauncher` with `expect`/`actual` on Android (`Intent.ACTION_SEND` chooser) and iOS (`UIActivityViewController`).
  - MVI Uni-directional Architecture: `ShareCardUiState` (immutable), `ShareCardEvent`, `ShareCardEffect`, and `ShareCardViewModel` managing state transitions.
- **Strict Security & PII Protection**:
  - Step-up verification using `ParentGateLauncher(TriggerContext.AchievementShare)`.
  - Gate dismissal/cancel immediately returns navigation without invoking backend card generation API.
  - Zero PII inclusion in card DTO, JSON serialization, and preview screen: no child ID, family ID, DOB, age, or location rendered or shared.
- **Design System Rule Compliance (`rule.md`)**:
  - 100% NoorTheme tokens: `NoorTheme.colors`, `NoorTheme.typography`, `NoorTheme.spacing`, `NoorTheme.radii`, `NoorTheme.elevation`.
  - Zero raw `.dp`, zero raw `.sp`, zero raw `Color(0x...)`, zero raw Material3 components.
  - Line count budget: All files strictly `< 500 lines`.
  - Author attribution: `@author Sarvare Alam` on all created artifacts.
- **Full 4-Locale Support**:
  - 16 new string keys synchronized across EN, AR, HI, UR in `core/core-common/src/commonMain/composeResources/values*/strings_rewards.xml` (192 keys total per locale).
- **UI Fidelity & Visual Alignment**:
  - Faithfully reproduces `Parent Gate-01.png` and `Parent Gate-02.png` (teal shield badge, PIN boxes with mask toggle, error state banner with red border, and recovery info card).
  - Aligns with `Achievements-01.png` through `Achievements-04.png`, with seamless navigation from `BadgeDetailScreen` into `ShareCardPreviewRoute` forwarding badge ID, title, and emblem.
  - Server-rendered card preview via `NoorImageWithPlaceholder` with milestone emblem fallback when offline.
  - Fallback error alert `NoorAlert(tone = AlertTone.Error)` if native share sheet invocation fails on the platform.
- **Validation & Test Execution**:
  - Unit Tests: `ShareCardViewModelTest` (8/8 passed).
  - UI / PII Guard Tests: `ShareCardPiiExclusionUiTest` (4/4 passed).
  - Full module suite: `:feature:feature-rewards:testAndroidHostTest` (70/70 passed, 0 failures).
  - Cross-platform KMP builds: `:core:core-ui:compileKotlinIosSimulatorArm64`, `:feature:feature-rewards:compileKotlinIosSimulatorArm64`, `:androidApp:compileDevDebugKotlin`, and `:shared:compileKotlinIosSimulatorArm64` compiled successfully.


