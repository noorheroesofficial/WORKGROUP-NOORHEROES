# K-09 — Reward Unlock Animation & Badge Unlock Modal (Shared Components)

## 1. Feature Context
Part of Feature A.11 — Rewards System. The only genuinely cross-feature shared UI this feature contributes — consumed by every other feature module's completion screen (Stories, Learn, Habits, Games, Quiz) whenever a reward is awarded or a badge unlocked.

## 2. Parent Feature
A.11 Rewards System — KMP App (Android/iOS)

## 3. Sub-feature
K-09 Reward Unlock Animation & Badge Unlock Modal (Shared Components)

## 4. Objective
Build the generic in-line Reward Unlock Animation and the Badge Unlock Modal (§1.18 #23–24) as reusable `core-design-system` components, enforcing the platform's anti-dark-pattern, non-randomized reveal rule.

## 5. Business Requirements
- ≤2s, consistent, non-randomized presentation — the same activity type always produces the same visual reveal, never a "surprise" slot-machine-style randomized reveal (§2.1).
- Must not block the completion screen's main thread or delay next-step navigation in the calling feature.
- Reduced-motion accessibility variant.

## 6. Existing Architecture
`core-design-system` module (existing, per `CORE_DESIGNSYSTEM_INSTRUCTIONS.md`). This is the correct placement for a genuinely cross-feature-consumed component, consistent with A.3 K-06's note ("badge/achievement modal component if one exists elsewhere — reuse, do not duplicate") which already anticipated this component originating from A.11.

## 7. Existing Code to Reuse
- `core-design-system`'s existing theming/token infrastructure.
- K-04's badge-tile visual tokens (for the modal's badge-icon presentation).

## 8. Files to Create
- `core/design-system/src/commonMain/kotlin/.../reward/RewardUnlockAnimation.kt`
- `core/design-system/src/commonMain/kotlin/.../reward/BadgeUnlockModal.kt`
- `core/design-system/src/commonMain/kotlin/.../reward/RewardRevealTrigger.kt` (typed trigger API consumed by other feature modules)
- `core/design-system/src/commonTest/kotlin/.../reward/DeterministicRevealTest.kt`
- `core/design-system/src/androidInstrumentedTest/kotlin/.../reward/RewardAnimationPerformanceTest.kt`

## 9. Files to Modify
- `core-design-system`'s public component export surface (add the new components to whatever index/registry pattern the module already uses).
- **Cross-feature integration — resolved:** A.3's `06-story-completion-reward-moral-summary-flow.md` (K-06) has been updated to consume this component directly (`RewardUnlockAnimation`/`BadgeUnlockModal`) and no longer builds a local `AchievementBadgeUnlockModal.kt`; its Task 07 now reads "Wire A.11 K-09's `BadgeUnlockModal` (Reuse Only, No Local Build)." No outstanding coordination item remains for A.3.

## 10. Backend Requirements
N/A directly; triggered by the calling feature's own completion-flow response data (e.g., B-01's `AwardResult`, B-04's `BadgeUnlockResult`), passed in as typed parameters — this component never fetches data itself.

## 11. KMP Requirements
- `RewardUnlockAnimation(xp: Int, noorPoints: Int, activityType: String)` — a pure, stateless Composable; the same `activityType` always renders the identical animation variant (a fixed lookup, not randomized selection).
- `BadgeUnlockModal(badge: BadgeUiModel, onDismiss: () -> Unit)` — dismiss always navigates the calling screen back to its own "next step," or to Achievements if explicitly opened from within the Rewards feature (K-04's usage).
- Both components accept all data as parameters (no internal repository calls), keeping them trivially reusable and testable in isolation.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
None directly — pure presentation components driven by caller-supplied data.

## 14. Database Requirements (Local)
None.

## 15. Validation
Deterministic-reveal unit test: given the same `activityType` input across multiple invocations, assert the selected animation variant/asset reference is identical every time (mandatory, enforces the non-randomized-reveal rule at the component level, not just by convention).

## 16. Authentication
N/A (presentation-only component).

## 17. Authorization
N/A.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Unknown/unmapped `activityType` | Falls back to a defined default animation variant, never crashes or shows a blank state |
| Reduced-motion accessibility setting enabled | Renders the static/reduced-motion variant instead of the full animation |

## 19. Offline First
N/A (no network dependency).

## 20. Local Data
N/A.

## 21. Localization
In-animation/modal text (XP/points labels, badge names) localized via the caller-supplied, already-localized strings — this component does not perform its own translation-key resolution.

## 22. RTL
Animation/modal layout mirrors correctly for Arabic/Urdu; verified via a dedicated RTL snapshot test.

## 23. Analytics
N/A directly (the calling feature fires its own completion-related analytics; this component does not self-instrument).

## 24. Performance
Animation must not block the calling screen's main thread or delay next-step navigation — verified via a dedicated performance/frame-timing test (mandatory, given this component runs inside every feature's hot completion path).

## 25. Security
No sensitive data handling.

## 26. Library Requirements
Compose Multiplatform animation APIs (existing project convention — reuse whatever animation library `core-design-system` already uses elsewhere, do not introduce a new one).

## 27. Testing
- Unit: deterministic-reveal test (mandatory).
- UI: reduced-motion variant rendering, RTL snapshot test.
- Performance: main-thread-non-blocking test (mandatory).

## 28. Documentation
KDoc explicitly stating the anti-dark-pattern rule this component enforces (deterministic, non-randomized reveal), noting A.3's `06-story-completion-reward-moral-summary-flow.md` (K-06) as the first confirmed cross-feature consumer (§9).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement `RewardUnlockAnimation`**
- Files to Create: `RewardUnlockAnimation.kt`
- Business Rules: ≤2s, deterministic reveal per activity type.
- Tests: deterministic-reveal test (mandatory).
- Definition of Done: test passing.

**Task 02 — Implement `BadgeUnlockModal`**
- Files to Create: `BadgeUnlockModal.kt`
- Existing Files to Reuse: K-04's badge-tile tokens.
- Implementation Details: caller-controlled dismiss destination.
- Definition of Done: correct dismiss behavior verified for both Rewards-internal and cross-feature callers.

**Task 03 — Implement Reduced-Motion & RTL Variants**
- Tests: reduced-motion rendering test, RTL snapshot test.
- Definition of Done: both verified.

**Task 04 — Implement Performance Test (Mandatory)**
- Files to Create: `RewardAnimationPerformanceTest.kt`
- Definition of Done: confirms no main-thread blocking / navigation delay.

**Task 05 — Publish Public Component API**
- Files to Modify: `core-design-system` export surface.
- Documentation: coordination note per §9/§28, confirming A.3 K-06 as the first cross-feature consumer.
- Definition of Done: components importable by any feature module; A.3's K-06 (already updated to consume this component, no local placeholder) compiles against the published API.

**Task 06 — Final Code Review**
- Do Not Change: the deterministic-reveal guarantee under any future "make it more exciting" request without explicit governance sign-off (this is a stated anti-dark-pattern commitment, not a stylistic default).
- Expected Result: PR merge-ready.

## 30. Definition of Done
Shared Reward Unlock Animation and Badge Unlock Modal live in `core-design-system`, deterministic-reveal and performance guarantees tested, ready for cross-feature adoption.

## 31. Final Verification Checklist
- [x] Deterministic-reveal test passes (same activity type → same variant, always)
- [x] Reduced-motion variant available and correctly triggered
- [x] Performance test confirms no main-thread blocking / navigation delay
- [x] RTL snapshot test passes
- [x] Components accept all data as parameters (no internal repository/network calls)
- [x] A.3 K-06 updated to consume this component with no local placeholder remaining

## 32. Verification Sign-Off Ledger
- **Status**: COMPLETED & VERIFIED (2026-09-26)
- **Author**: Sarvare Alam
- **Created / Updated Files**:
  - `core/core-designsystem/src/commonMain/kotlin/com/noorheroes/core/designsystem/reward/RewardRevealTrigger.kt` (323 lines): `RewardActivityType`, `RewardAnimationVariant`, `BadgeUnlockUiModel`, `RewardRevealTrigger`, `RewardRevealLayoutSnapshot`, and `DeterministicRewardVariantResolver` (`MAX_REWARD_DURATION_MS = 2000L`, `REDUCED_MOTION_DURATION_MS = 0L`, deterministic `resolveVariant`, and LTR/RTL `buildLayoutSnapshot`).
  - `core/core-designsystem/src/commonMain/kotlin/com/noorheroes/core/designsystem/reward/RewardUnlockAnimation.kt` (399 lines): Stateless, non-blocking `RewardUnlockAnimation(xp, noorPoints, activityType)` Composable with XP effort/progress-bar pill (`RewardXpEffortPill`) vs. Noor Heroes Points spendable coin/currency pill (`RewardPointsCoinPill`), immediate `0ms` tap-through dismissal, reduced-motion static rendering, and RTL horizontal layout mirroring.
  - `core/core-designsystem/src/commonMain/kotlin/com/noorheroes/core/designsystem/reward/BadgeUnlockModal.kt` (320 lines): Shared cross-feature `BadgeUnlockModal(badge, onDismiss)` reusing K-04's badge-tile visual tokens (`emblem`, `radius22`, `primarySubtle`, `primary`) with caller-controlled dismiss destination (supporting both A.3 K-06 completion next-step continuation and A.11 K-04 Achievements return).
  - `core/core-designsystem/src/commonMain/kotlin/com/noorheroes/core/designsystem/theme/NoorHeroesTheme.kt` (170 lines): Published `NoorHeroesTheme.rewards` on `core-designsystem`'s public export surface.
  - `core/core-ui/src/commonMain/kotlin/com/noorheroes/core/ui/component/Rewards.kt` (229 lines): Exported delegating overloads for `RewardUnlockAnimation(xp, noorPoints, activityType)` and `BadgeUnlockModal(badge, onDismiss)`.
  - `feature/feature-rewards/src/commonMain/kotlin/com/noorheroes/feature/rewards/achievements/components/BadgeUnlockModal.kt` (41 lines): Delegated K-04's `BadgeUnlockModal` to `core-designsystem`'s shared `BadgeUnlockModal` to eliminate duplication.
  - `core/core-designsystem/src/commonTest/kotlin/com/noorheroes/core/designsystem/reward/DeterministicRevealTest.kt` (189 lines) & `src/androidInstrumentedTest/kotlin/com/noorheroes/core/designsystem/reward/RewardAnimationPerformanceTest.kt` (85 lines): 9 deterministic-reveal, unknown-fallback, `<=2s` ceiling, reduced-motion, RTL snapshot, caller-controlled dismiss, and single-frame `<16ms` non-blocking performance tests (`0 violations` on `audit_k09.py`).

