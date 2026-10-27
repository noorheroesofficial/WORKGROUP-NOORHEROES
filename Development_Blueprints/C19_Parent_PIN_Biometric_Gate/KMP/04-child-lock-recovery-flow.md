# K-04 — Child Lock Recovery Flow

## 1. Feature Context
The "Ask a grown-up" path a child follows when they forget their lock. **Partially exists** as `LockRecoveryScreen` (A.1 K-08), which already requires "full Parent Profile re-verification" before proceeding. This sub-feature hardens that flow to call K-03's consolidated `ParentGateLauncher` (rather than any prior inline gate) and B-02's scoped `recovery_token` API, and ensures an abandoned recovery leaves the child's lock untouched.

## 2. Parent Feature
Feature C.19 — Parent PIN/Biometric Gate & Profile Access Control

## 3. Sub-feature
2.4 Child Lock Recovery Flow (ID: **K-04**)

## 4. Objective
Wire `LockRecoveryScreen` to call `ParentGateLauncher.requireParentAuth(PinReset)` (K-03) then B-02's `POST /v1/children/{id}/lock/recover`, presenting a new-lock-configuration screen on success, and guaranteeing the original lock configuration is untouched if the parent abandons the flow.

## 5. Business Requirements
- FR-6: recovery never routes through a generic bypass — always via verified Parent Profile.
- Edge Case 4: parent backs out before resetting the new lock → child's original lock configuration remains unchanged and functional.

## 6. Existing Architecture
`feature/onboarding/ui/LockRecoveryScreen.kt` (A.1 K-08) already implements the "requires full Parent Profile re-verification" gate inline. This sub-feature replaces that inline call with K-03's consolidated `ParentGateLauncher`, removing the duplicate gate logic K-03 Task 01 was scoped to extract.

## 7. Existing Code to Reuse
- `feature/onboarding/ui/LockRecoveryScreen.kt` (A.1 K-08 — extend)
- `core-auth/ParentGateLauncher` (K-03)
- `core-network`'s API client, extended with `recoverChildLock(childId)` → B-02

## 8. Files to Create
- `feature/onboarding/viewmodel/LockRecoveryViewModel.kt` (if not already extracted from `ChildLockViewModel` in K-08 — confirm)
- `test/feature/onboarding/LockRecoveryAbandonmentTest.kt`

## 9. Files to Modify
- `feature/onboarding/ui/LockRecoveryScreen.kt` — replace inline gate call with `ParentGateLauncher.requireParentAuth(TriggerContext.PinReset)`
- `feature/onboarding/viewmodel/*` — wire `recoverChildLock()` call to B-02 on gate success

## 10. KMP Requirements
- Recovery screen is reachable only from K-02's "Ask a grown-up" link.
- On tap: `ParentGateLauncher.requireParentAuth(PinReset)` → on success, call B-02's `POST /v1/children/{id}/lock/recover` → on success, present new-lock-configuration UI (reuse A.1's existing lock-configuration component from onboarding's per-child lock setup, do not build a second one).
- On gate cancel/failure: return to K-02's lock screen unchanged, no partial state.
- On recovery-token issuance followed by parent abandoning before completing the new-lock setup: no lock-config mutation occurs (guaranteed server-side per B-02's design — the token itself never mutates anything until explicitly used against the lock-set endpoint), verified client-side by confirming the original `ChildLock` state is unchanged on screen re-entry.

## 11. Required API
`POST /v1/children/{id}/lock/recover` (B-02).
**User API**

## 12. Offline First
Not applicable — recovery is an online-only, parent-present flow (mirrors B-02's design).

## 13. Local Data
No new local persistence; consumes existing `ChildLockRepository` to refresh cached lock state after a successful reset.

## 14. Localization
Recovery screen copy, new-lock-setup copy fully localized EN/HI/AR/UR.

## 15. RTL
Standard RTL mirroring for recovery flow screens.

## 16. Analytics
`lock_recovery_initiated` (on Parent Gate success + B-02 call), plus whatever completion event the existing lock-configuration component already emits on a successful reset.

## 17. Performance
No specific performance constraints beyond standard screen-transition latency.

## 18. Security
No path from `LockRecoveryScreen` to the new-lock-configuration screen may skip `ParentGateLauncher.requireParentAuth()` — structural test required, mirroring K-03's own no-bypass guarantee.

## 19. Testing
- Integration: full recovery flow — Parent Gate success → `recovery_token` issued → new lock set → child can log in with new lock.
- Integration: abandoned recovery (parent backs out post-token, pre-reset) → original lock configuration unchanged (highest-priority test, Edge Case 4).
- UI: Parent Gate cancel/failure returns to K-02 unchanged.

## 20. AI Coding Agent Implementation Steps

**Task 01 — Replace Inline Gate Call with `ParentGateLauncher`**
Objective: remove duplicate gate logic, route through K-03. Files to Modify: `LockRecoveryScreen.kt`. Dependencies: K-03 live.

**Task 02 — Wire `recoverChildLock()` to B-02**
Objective: call `POST /v1/children/{id}/lock/recover` on gate success. Files to Modify: `LockRecoveryViewModel.kt`. Dependencies: Task 01, B-02 live.

**Task 03 — Wire New-Lock-Configuration Screen on Success**
Objective: reuse existing onboarding lock-config component, do not duplicate. Files to Modify: `LockRecoveryScreen.kt`. Dependencies: Task 02.

**Task 04 — Add Abandonment Test**
Objective: prove original lock config survives an abandoned flow. Files to Create: `LockRecoveryAbandonmentTest.kt`. Dependencies: Task 03.

**Task 05 — Add Full Test Suite**
Objective: coverage per §19. Dependencies: Task 01–04.

## 21. Final Verification Checklist
- [x] No path skips `ParentGateLauncher.requireParentAuth()` before recovery
- [x] Abandoned recovery leaves original lock configuration unchanged
- [x] New-lock-configuration screen reuses the existing onboarding component, no duplicate UI
- [x] Gate cancel/failure returns cleanly to K-02

## 22. Definition of Done
`LockRecoveryScreen` (A.1 K-08, hardened here) routes exclusively through K-03's consolidated Parent Gate and B-02's scoped recovery token, with a proven guarantee that abandonment never mutates the child's original lock configuration.

## 23. Verification Record
- **Date**: 2026-09-22
- **Author**: Antigravity (Sarvare Alam)
- **Status**: PASSED
- **Test Results**:
  - `:feature:feature-onboarding:testAndroidHostTest`: 100% Passed (`LockRecoveryViewModelTest`, `LockRecoveryAbandonmentTest`, `ChildLockCooldownUiTest`, etc.)
  - `:core:core-security:testAndroidHostTest`: 100% Passed (`ParentGateLauncherTest`, `GraceWindowManagerTest`, `ParentGateLauncherStructuralTest`)
  - `:shared:testAndroidHostTest`: 100% Passed
- **Key Invariants Verified**:
  - **FR-6**: `ParentGateLauncher.requireParentAuth(TriggerContext.PinReset)` verified and enforced before child lock recovery.
  - **B-02 Integration**: Scoped short-lived `recovery_token` fetched via `FamilyApiService.recoverChildLock(childId)`.
  - **Edge Case 4**: Backing out / canceling at any point before saving new lock leaves child's original credentials, DAO state, and attempt counters 100% untouched.
  - **100% Token Purity**: Fully styled using `NoorHeroesTheme.colors`, `typography`, `spacing`, `shapes`, and `sizes`.
  - **Localization**: Localized across EN, AR, UR, and HI.
