# K-05 — Parent PIN Setup & Biometric Enrollment Flow

> **Status:** ✅ **Implemented & Verified** (Live simulator verified on Android `emulator-5554` with live FastAPI backend)

## 1. Feature Context
Immediately post-verification for new users: set a local PIN and optionally enroll biometric unlock. This PIN subsequently gates Settings, purchases, and parent-mode from the child throughout the app's lifetime.

## 2. Parent Feature
Feature A.1 — Splash, Language Selection, Authentication & Onboarding

## 3. Sub-feature
2.5 Parent PIN Setup & Biometric Enrollment Flow (ID: **K-05**)

## 4. Objective
Build PIN Setup (set + confirm) and Biometric Enrollment screens using `core-security`'s `CredentialHasher`/`BiometricGate`, submitting the PIN to B-04, with the biometric hardware check hiding (not disabling) the enrollment option when unavailable.

## 5. Business Requirements
- FR-11: PIN 4–6 digits, parent's choice; no "weak/strong" judgment shown to the user.
- FR-12: Optional OS-level biometric enrollment; biometric data never transmitted to servers.
- Permission State: if device has no biometric hardware, the option is hidden, not shown-disabled.
- Screen note: Confirm must exactly match Set; mismatch clears the Confirm field only (not the whole form).

## 6. Existing Architecture
`core-security`'s `BiometricGate` (expect class, cross-platform biometric prompt bridge), `CredentialHasher` (local hash for on-device verification cache, distinct from B-04's server-side Argon2id hash — the client also needs a local verification path so parent-mode can be unlocked offline).

## 7. Existing Code to Reuse
- `core-security`: `BiometricGate.authenticate()`, `CredentialHasher.hash()/verify()`, `ProgressiveLockoutPolicy`
- `core-ui`: `NoorPinInput` (same component K-03 uses/extends for OTP — reuse here for PIN entry, confirming it supports a "set then confirm" two-pass mode)
- `core-network`: `AuthApiService` (add `setPin()`)

## 8. Files to Create
- `feature/onboarding/ui/ParentPinSetupScreen.kt`
- `feature/onboarding/ui/BiometricEnrollmentScreen.kt`
- `feature/onboarding/viewmodel/PinSetupViewModel.kt` (+ State/Event)
- `core-network/api/PinDtos.kt` — `PinSetRequestDto`, `PinSetResponseDto`
- `core-security/ParentPinLocalStore.kt` — new (see §7's resolved decision; no existing equivalent found)
- `test/feature/onboarding/PinSetupViewModelTest.kt`
- `test/core-security/ParentPinLocalStoreTest.kt`
- `androidTest/feature/onboarding/ParentPinSetupScreenTest.kt`

## 9. Files to Modify
- `core-network/api/AuthApiService.kt` — add `suspend fun setPin(pin: String): NoorResult<PinSetResponseDto>`
- `core-navigation/Route.kt` — add `ParentPinSetupRoute`, `BiometricEnrollmentRoute`

## 10. KMP Requirements
- PIN pad: set pass (4–6 digits, parent chooses length) then confirm pass; on mismatch, clear only the confirm entry, keep the set value, show inline error — never reset the whole flow.
- No weak/strong strength indicator UI — the server's `weak_pin_warning` (if `true`) surfaces as a neutral informational note at most, never a blocking judgment (per FR-11's "parent's choice" principle); confirm this matches B-04's soft-warning contract.
- On PIN submit success, call the new `ParentPinLocalStore.saveLocalPinHash()` (§7) to store an on-device verification hash (separate from the server's copy) so parent-mode unlock can work fully offline.
- Biometric enrollment: check hardware/enrollment availability via `BiometricGate` before rendering the screen at all — if unavailable, skip directly to Add Child (K-06), never show a disabled biometric option.
- On `BiometricResult.Success`, store the enrollment preference locally (no server round-trip needed — biometric data itself never leaves the device); on `BiometricResult.Error`/cancellation, fall back gracefully to "Skip" without treating it as a hard failure.

## 11. Required API
- `POST /v1/identity/auth/pin` (B-04)

## 12. Local Data
On-device PIN verification hash (via `CredentialHasher`, `core-security`-managed secure storage — not plain `DataStore`) for offline parent-mode unlock; biometric-enrollment-enabled boolean preference (via `PreferenceManager` or `core-security`'s equivalent secure flag).

## 13. Localization / RTL
Standard localization for all copy; RTL mirroring for the PIN pad layout (digit grid stays LTR-numeric per standard convention, similar to the OTP-cell-order rule in K-03 — verify this explicitly) and the biometric prompt copy.

## 14. Analytics
Emit `pin_setup_started`, `pin_setup_completed` (biometric_offered), `biometric_enrollment_offered`, `biometric_enrollment_completed`, `biometric_enrollment_skipped` via `AnalyticsTracker`.

## 15. Security
Raw PIN held in Compose state only as long as needed to hash it — cleared from state immediately after both the server call and local-hash storage complete (no lingering plaintext in ViewModel state after submission finishes). Biometric result data never serialized/transmitted anywhere.

## 16. Testing
- Unit: confirm-mismatch clears only the confirm field; biometric-hardware-absent hides (not disables) the enrollment screen entirely (route-skip assertion); local PIN hash written only after server success (never before, to avoid a client/server hash mismatch on partial failure).
- UI: PIN pad interaction states (empty, partial, mismatch-error, success); biometric prompt trigger and cancellation handling.
- Accessibility: PIN pad buttons have clear numeric labels, biometric prompt is a native OS surface (accessibility inherited from the platform).

## 17. AI Coding Agent Implementation Steps

**Task 01 — Add `setPin()` to `AuthApiService`**
Objective: Network contract for B-04. Follow: existing `safeCall` pattern. Files to Create: `PinDtos.kt`. Definition of Done: typed call available, tested.

**Task 02 — Implement `ParentPinLocalStore`**
Objective: Build the on-device parent-PIN hash-and-verify store. **Resolved architecture decision:** re-checking both `CORE_SECURITY_INSTRUCTIONS.md` and `CORE_DATA_INSTRUCTIONS.md` confirms `ChildLockRepository.verifyChildLock()` (core-data) is specifically documented for *child*-lock entry (a different credential, a different table, per `core-database`'s `ChildLockDao`) — not the parent's own PIN. `core-security` documents `AuthState.Parent.elevatedUntil`/`isElevated(clock)` for *step-up freshness tracking* (i.e., "has the parent re-verified recently"), and `CredentialHasher` for the hash/verify *primitive* itself, but no existing repository or store persists the parent's own local PIN hash for offline verification. This is a genuine, confirmed gap, not an unconfirmed one — no such store exists today. Resolution: build a new `ParentPinLocalStore` in `core-security` (co-located with `CredentialHasher`/`TokenStore`, following `TokenStore`'s existing "secure platform storage" pattern — Android `EncryptedSharedPreferences`/iOS Keychain, the same backing mechanism `DatabaseKeyProvider` already uses) exposing `saveLocalPinHash(hash: String)` / `verifyLocalPin(input: String): Boolean`, internally calling `CredentialHasher.hash()`/`.verify()`. A successful local verify also updates `AuthState.Parent.elevatedUntil` via the existing `MutableAuthStateHolder` (do not invent a second elevation-tracking mechanism — this store only owns the hash, `AuthStateHolder` still owns elevation state). Files to Create: `core-security/ParentPinLocalStore.kt`. Tests: hash/verify round-trip; verify-failure does not update `elevatedUntil`; verify-success does. Definition of Done: no second, divergent local-hash store exists anywhere in the codebase — this is the single source of truth for the parent's own on-device PIN verification.

**Task 03 — Implement `PinSetupViewModel`**
Objective: Set→confirm PIN flow, submit to B-04, write local verification hash on success. Follow: `BaseViewModel`. Business Rules: mismatch clears confirm only; local hash written only post-server-success. Security: raw PIN cleared from state immediately after use. Tests: full matrix per §16. Dependencies: Tasks 01–02. Definition of Done: log/state-inspection test confirms no lingering plaintext PIN.

**Task 04 — Implement `ParentPinSetupScreen`**
Objective: PIN pad UI, no strength judgment, neutral biometric-offer transition. Follow: `NoorPinInput` (extended if needed), `NoorHeroesTheme`. Tests: covered by Task 03/06. Dependencies: Task 03. Definition of Done: UI matches PRD screen spec (no strength indicator anywhere).

**Task 05 — Implement Biometric Availability Check & Enrollment Screen**
Objective: Hide (not disable) when hardware/enrollment absent; `BiometricGate.authenticate()` trigger with graceful cancellation handling. Follow: `core-security`'s `BiometricGate`. Tests: hardware-absent route-skip assertion; cancellation-is-not-a-hard-failure assertion. Dependencies: Task 03. Definition of Done: navigation graph never renders the biometric screen when hardware is absent.

**Task 06 — Add Analytics Instrumentation**
Objective: All events in §14. Follow: `AnalyticsTracker`, ViewModel-only. Definition of Done: one call site per event.

**Task 07 — Add Full Test Suite**
Objective: Complete coverage per §16. Definition of Done: all green in CI.

**Task 08 — Final Code Review**
Objective: Confirm zero plaintext PIN persistence anywhere client-side, confirm biometric hide-not-disable behavior, confirm local/server hash write ordering is correct (server-success-first). Definition of Done: checklist in §18 checked.

## 18. Final Verification Checklist
- [x] PIN confirm-mismatch clears only the confirm field
- [x] No PIN-strength judgment UI anywhere
- [x] Biometric enrollment screen is skipped entirely (not shown-disabled) when hardware/enrollment is absent
- [x] Local on-device PIN verification hash written only after server-side success
- [x] Raw PIN cleared from ViewModel state immediately after use — verified by a test
- [x] Biometric result data never transmitted or persisted beyond a local enabled/disabled flag
- [x] All analytics events in §14 emitted correctly

## 19. Definition of Done
Parent PIN Setup and Biometric Enrollment are live against B-04, PIN plaintext never lingers client-side, biometric availability correctly gates screen visibility, and the flow hands off cleanly to K-06 (Add Child). **(STATUS: IMPLEMENTED & VERIFIED)**
