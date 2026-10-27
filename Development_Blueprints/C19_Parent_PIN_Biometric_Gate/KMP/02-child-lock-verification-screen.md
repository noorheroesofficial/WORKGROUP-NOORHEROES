# K-02 — Child Lock Verification Screen

## 1. Feature Context
Verifies a child's configured lock (Pattern/PIN/Fingerprint) against B-01's server-authoritative API, with an offline-tolerant local fallback. **This screen already exists** as `ChildLockScreen` (A.1 K-08), backed by `core-security`'s `BiometricGate`/`CredentialHasher`/`ProgressiveLockoutPolicy` and `core-data`'s `ChildLockRepository.verifyChildLock()`. This sub-feature hardens it to C.19's exact lockout-honored-during-cooldown and biometric-fallback guarantees.

## 2. Parent Feature
Feature C.19 — Parent PIN/Biometric Gate & Profile Access Control

## 3. Sub-feature
2.2 Child Lock Verification Screen (ID: **K-02**)

## 4. Objective
Harden `ChildLockScreen` so that on `423 LOCKED_RETRY_COOLDOWN` from B-01, the input pad becomes fully non-interactive until the countdown expires — including against a programmatically "correct" submission — and biometric failure/unavailability falls back to PIN entry without a dead end.

## 5. Business Requirements
- FR-5: Pattern/PIN compared via salted slow hash; Fingerprint uses OS assertion only.
- FR-6: failure/unavailability falls back to the child's own PIN/pattern, or recovers via verified Parent Profile (K-04) — never a generic bypass.
- FR-15: offline verification uses the locally cached salted hash.
- Edge Case 7: correct pattern entered during an active lockout countdown is still honored as locked.
- Edge Case 3: parent's enrolled biometric changes at OS level → graceful fallback to PIN, never permanent lockout (this specific edge case is about the *parent's* biometric in §1.10 item 3, but the same fallback principle applies to a child's fingerprint lock per FR-6).

## 6. Existing Architecture
`feature/onboarding/ui/ChildLockScreen.kt` + `ChildLockViewModel.kt` (A.1 K-08), delegating to `core-data/ChildLockRepository.verifyChildLock()` (local hash + entitlement-grace-period check) and `core-security`'s `BiometricGate`/`ProgressiveLockoutPolicy`. This sub-feature does not reimplement local hash comparison — it hardens the UI-state machine around lockout and fallback.

## 7. Existing Code to Reuse
- `feature/onboarding/ui/ChildLockScreen.kt`, `ChildLockViewModel.kt` (A.1 K-08 — extend, do not recreate)
- `core-data/ChildLockRepository.verifyChildLock()` (existing local hash + grace-period logic)
- `core-security/BiometricGate`, `ProgressiveLockoutPolicy` (existing: 4th attempt 30s, 5th 5m, 6+ escalating — per K-08 §10)
- `core-network`'s API client, extended to call B-01's `POST /v1/children/{id}/lock/verify` when online

## 8. Files to Create
- `test/feature/onboarding/ChildLockCooldownUiTest.kt` — input-pad-non-interactive-during-lockout assertion

## 9. Files to Modify
- `feature/onboarding/viewmodel/ChildLockViewModel.kt` — wire online path to B-01's `POST /v1/children/{id}/lock/verify`, keep `ChildLockRepository.verifyChildLock()` as the offline fallback; on `423`, transition to a `Lockout` state that disables all input handlers, not just visually greys them out
- `feature/onboarding/ui/ChildLockScreen.kt` — ensure the numeric/pattern input composables read `enabled = state !is Lockout` at the component level, not just apply a visual overlay

## 10. KMP Requirements
- Online path calls B-01's server-authoritative endpoint; offline path uses the existing `ChildLockRepository.verifyChildLock()` cached-hash comparison — both paths converge on the same `ChildLockViewModel` state machine (`Idle → Verifying → Success | Failed(attemptsRemaining) | Lockout(countdown)`).
- `Lockout` state must make the input pad **structurally non-interactive** (component-level `enabled = false`), not merely visually disabled — a UI test submits a "correct" value programmatically during lockout and asserts no verification call is even dispatched.
- Biometric failure/unavailable → `BiometricFallbackToPin` state, offering standard PIN entry, never terminating the flow.
- "Ask a grown-up" recovery link always visible, routes to K-04.
- Non-gesture accessible alternative for pattern entry (existing requirement, confirm K-08 covers it).

## 11. Required API
`POST /v1/children/{id}/lock/verify` (B-01) — online path only; offline path uses existing local repository.

## 12. Offline First
`ChildLockRepository.verifyChildLock()` (existing) provides the offline cached-hash fallback; this sub-feature's responsibility is ensuring the ViewModel correctly selects online-vs-offline path based on connectivity state and that lockout state is consistent across both (a lockout triggered offline should not be silently bypassed once connectivity returns, and vice versa — reconcile against B-01's server state on reconnect).

## 13. Local Data
Reuses existing `ChildLockRepository` cache (Android Keystore-backed per K-06); no new local data introduced here.

## 14. Localization
Lock screen copy, retry counter, "Ask a grown-up" link fully localized EN/HI/AR/UR (confirm K-08 coverage extends to lockout-state copy specifically).

## 15. RTL
Numeric keypad and pattern grid mirror correctly in RTL where applicable (numeric pad typically stays LTR for digit order by platform convention — confirm against Global Design System tokens).

## 16. Analytics
`lock_screen_shown`, `lock_verification_succeeded`, `lock_verification_failed`, `lock_lockout_triggered`, `biometric_fallback_to_pin`.

## 17. Performance
Local verification p95 < 200ms fully on-device (NFR); no network round-trip required for the lock check itself when offline.

## 18. Security
- Lockout is enforced at the component level, not just the ViewModel's business logic — this closes any potential race where a stale UI event could slip through during the transition to `Lockout` state.
- Cached hash comparison never logs the raw submitted value.

## 19. Testing
- Unit: `ProgressiveLockoutPolicy` tier escalation (30s/5m/escalating) honored regardless of credential correctness.
- UI: input pad is non-interactive during active lockout, including a programmatic "correct" submission attempt (highest-priority test, mirrors B-01's server-side guarantee on the client).
- UI: biometric failure → PIN fallback rendered, never a dead-end screen.
- Integration: offline verification → online reconciliation on reconnect.

## 20. AI Coding Agent Implementation Steps

**Task 01 — Wire Online Verification Path to B-01**
Objective: `ChildLockViewModel` calls `POST /v1/children/{id}/lock/verify` when online, existing repository when offline. Files to Modify: `ChildLockViewModel.kt`. Dependencies: B-01 live.

**Task 02 — Harden Lockout State to Component-Level Non-Interactivity**
Objective: `enabled = false` at the input-composable level during `Lockout`. Files to Modify: `ChildLockScreen.kt`. Dependencies: Task 01.

**Task 03 — Implement Biometric-Fallback-to-PIN State**
Objective: graceful, non-dead-end fallback. Files to Modify: `ChildLockViewModel.kt`, `ChildLockScreen.kt`. Dependencies: Task 01.

**Task 04 — Add Cooldown UI Test**
Objective: prove the structural non-interactivity guarantee. Files to Create: `ChildLockCooldownUiTest.kt`. Dependencies: Task 02.

**Task 05 — Add Analytics Instrumentation**
Objective: all five events per §16. Dependencies: Task 01–03.

**Task 06 — Add Full Test Suite**
Objective: coverage per §19. Dependencies: Task 01–05.

## 21. Final Verification Checklist
- [x] Input pad structurally non-interactive during lockout (component-level, not visual-only via `enabled` parameter on `NoorPatternInput` and `NumericKeypad`, plus early-return rejection in `ChildLockViewModel`)
- [x] Biometric failure always falls back to PIN, never a dead end (verified in `ChildLockCooldownUiTest` and `ChildLockViewModelTest`)
- [x] Offline and online verification paths converge on one consistent state machine (`FamilyApiService.verifyChildLock` online -> `ChildLockRepository.verifyChildLock` offline)
- [x] "Ask a grown-up" link always visible and routes to K-04 (`ChildLockEvent.NavigateToLockRecovery`)
- [x] No raw credential value ever logged (credentials passed only in verified hash / SSL POST payloads; analytics strictly carries `child_id_hash` and `lock_type`)

## 22. Definition of Done
`ChildLockScreen` (A.1 K-08, hardened here) verifies against B-01 when online and the existing local cache when offline, structurally enforces lockout non-interactivity, and gracefully falls back from biometric to PIN without a dead end. Verified with 100% test pass rate across `:feature:feature-onboarding:allTests` and `:shared:allTests`.

## 23. Verification & Compliance Record
- **Implementation Status**: COMPLETED (100% compliant with C.19 FR-5, FR-6, FR-15, Edge Cases 3 & 7, and visual assets)
- **Visual Design Matching**:
  - `Screens/Mobile App/Parent Area/Profile Lock.png` (Uniform warm off-white canvas, circular child avatar with rose badge, 4-dot PIN indicator with brand teal and subtle border unfilled state, 3x4 numeric keypad with localized TalkBack/VoiceOver semantics, pill-shaped "Ask a grown-up for help" recovery link)
- **Architecture & Hardening**:
  - `ChildLockViewModel`: Online server-authoritative API `FamilyApiService.verifyChildLock` (`POST /v1/family/children/{childId}/lock/verify`), graceful fallback to local salted slow hash `ChildLockRepository.verifyChildLock` when offline.
  - HTTP 423 `LOCKED_RETRY_COOLDOWN` and `ProgressiveLockoutPolicy` (30s, 5m, escalating) cooldown ticker.
  - Structural non-interactivity: Component-level `enabled` parameter on `NumericKeypad`, `NoorPatternInput`, and biometric trigger surface, plus early-return rejection in `ChildLockViewModel.onDigitEntered` / `onPatternEntered` preventing programmatic submission during active cooldown.
  - Biometric fallback: Failure or unavailability transitions to child's PIN entry without terminating the flow or displaying a dead-end screen (FR-6, Blueprint Task 03).
  - 100% token purity: Zero hardcoded colors or sizing (`NoorHeroesTheme.colors.surfaceSubtle`, `NoorHeroesTheme.colors.border`, `NoorHeroesTheme.colors.avatarBgRose`, `NoorHeroesTheme.colors.avatarBorderRose`, `NoorHeroesTheme.sizes.touchIos`).
  - 4-Language localization: EN, AR, HI, UR strings with proper RTL layout support.
- **Unit, UI, & Structural Tests**:
  - `ChildLockCooldownUiTest.kt`: Validates programmatic rejection during lockout, biometric fallback to PIN without dead ends, 423 server cooldown triggers lockout, ask grown-up navigation, and analytics.
  - `ChildLockViewModelTest.kt`: Validates online/offline verification paths, progressive lockout escalation, first mission vs child home routing, and analytics.
- **Test Execution Result**:
  - `:core:core-designsystem:allTests` -> SUCCESS (0 failures)
  - `:feature:feature-onboarding:allTests` -> SUCCESS (0 failures)
  - `:shared:allTests` -> SUCCESS (0 failures)
