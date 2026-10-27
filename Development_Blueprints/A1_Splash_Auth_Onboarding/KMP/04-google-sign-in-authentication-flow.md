# K-04 — Google Sign-In Authentication Flow

> **Status:** ✅ **Implemented & Verified** (Live simulator verified on Android `emulator-5554` with live FastAPI backend)

## 1. Feature Context
Alternate identity path from the Login/Registration screen, bypassing OTP entirely. Maps to the identical downstream state transition as OTP verification.

## 2. Parent Feature
Feature A.1 — Splash, Language Selection, Authentication & Onboarding

## 3. Sub-feature
2.4 Google Sign-In Authentication Flow (ID: **K-04**)

## 4. Objective
Trigger native Google Sign-In, forward the ID token to B-03, and route through the same `AuthStateHolder` transition K-03 established for OTP success.

## 5. Business Requirements
- FR-6: Google Login supported; Apple Login explicitly not supported — do not add any Apple Sign-In UI or capability.
- FR-21: Google Login maps to the same downstream flow as OTP-verified users.
- Edge Case: Google account linked to a deleted/soft-deleted family → reactivation flow triggers instead of fresh registration.

## 6. Existing Architecture
Extends `core-security`'s `AuthRepository` (the same `verifyOtp()`-equivalent session-issuance path extended in K-03 Task 02) with a `loginWithGoogle(idToken, deviceId)` method calling B-03.

## 7. Existing Code to Reuse
- `core-security/AuthRepository`, `MutableAuthStateHolder` (K-03 Task 02's extended session-issuance path — reuse directly, do not duplicate)
- `core-network/AuthApiService` (add `googleAuth()`)
- Platform Google Sign-In SDK (Android: Credential Manager / Google Identity Services; iOS: Google Sign-In SDK) behind a KMP `expect`/`actual` abstraction

## 8. Files to Create
- `core-network/api/GoogleAuthDto.kt`
- `feature/onboarding/auth/GoogleSignInLauncher.kt` (`expect` class/interface)
- `feature/onboarding/auth/GoogleSignInLauncher.android.kt`, `.ios.kt` (`actual` implementations)
- `feature/onboarding/viewmodel/GoogleSignInHandler.kt` (thin coordinator invoked from `RegistrationViewModel`/`LoginViewModel`)
- `test/feature/onboarding/GoogleSignInHandlerTest.kt`

## 9. Files to Modify
- `core-network/api/AuthApiService.kt` — add `suspend fun googleAuth(idToken: String, deviceId: String): NoorResult<TokenResponseDto>`
- `core-security/AuthRepository.kt`/`AuthRepositoryImpl` — add `loginWithGoogle()`
- `feature/onboarding/ui/RegistrationConsentScreen.kt` (K-03) — wire the existing "Continue with Google" button to `GoogleSignInLauncher`

## 10. KMP Requirements
- `GoogleSignInLauncher` is a platform abstraction (`expect`/`actual`) — Android uses Credential Manager/Google Identity Services, iOS uses the native Google Sign-In SDK; both return a raw ID token string to common code, which forwards it to `AuthRepository.loginWithGoogle()`.
- On success, `AuthStateHolder` transitions identically to the OTP path — downstream routing (`next_step`) reuses the exact same handling K-03 built.
- On cancellation (user dismisses the native picker), return to the Login/Registration screen state with no error banner (cancellation is not an error).
- On reactivation-required response, route to a reactivation-confirmation UI rather than silently treating it as fresh registration.

## 11. Required API
- `POST /v1/identity/auth/google` (B-03)

## 12. Localization / RTL
Google's native sign-in UI is platform-rendered (not custom-built) — no RTL/localization work needed beyond ensuring the "Continue with Google" button itself (built in K-03) is correctly mirrored, which K-03 already covers.

## 13. Analytics
Emit `login_started` (method=google) via `AnalyticsTracker` — same event K-03 already defines, just a different `method` value; do not create a parallel event name.

## 14. Security
ID token is forwarded to the backend immediately and not persisted client-side beyond the in-flight call — no caching of raw Google tokens in `DataStore`/`Room`.

## 15. Testing
- Unit: success → `AuthStateHolder` transition matches K-03's OTP-success transition exactly; cancellation → no error state, no analytics failure event; reactivation-required → routes to reactivation UI, not fresh registration.
- Integration: full tap-to-Profile-Picker happy path with a mocked Google credential provider.

## 16. AI Coding Agent Implementation Steps

**Task 01 — Add `googleAuth()` to `AuthApiService`**
Objective: Network contract for B-03. Follow: existing `safeCall` pattern. Files to Create: `GoogleAuthDto.kt`. Tests: DTO round-trip test. Definition of Done: typed call available.

**Task 02 — Implement `GoogleSignInLauncher` expect/actual**
Objective: Platform-specific native sign-in trigger returning a raw ID token to common code. Follow: KMP `expect`/`actual` pattern per `core-common`'s platform-abstraction conventions (mirrors `PermissionManager`'s Android/iOS split). Files to Create: three files (common + two actuals). Tests: platform-specific instrumented tests where feasible; common-code unit test with a fake launcher. Definition of Done: both platforms compile and produce a token via their native SDKs.

**Task 03 — Extend `AuthRepository.loginWithGoogle()`**
Objective: Bridge to B-03, reuse K-03's session-issuance/state-transition path exactly. Follow: `core-security` conventions. Tests: state-transition-matches-OTP-path assertion. Dependencies: Tasks 01–02, K-03 Task 02. Definition of Done: identical `AuthStateHolder` outcome to a successful OTP verify.

**Task 04 — Wire the Existing Google Button (from K-03) to the Launcher**
Objective: Connect K-03's UI entry point to `GoogleSignInHandler`. Files to Modify: `RegistrationConsentScreen.kt`. Tests: covered by Task 05. Definition of Done: tap triggers the native picker.

**Task 05 — Add Unit & Integration Tests**
Objective: Full coverage per §15. Definition of Done: all green, including the cancellation-is-not-an-error case.

**Task 06 — Final Code Review**
Objective: Confirm no Apple Sign-In artifacts were introduced, no raw token persistence, reactivation path correctly distinguished from fresh registration. Definition of Done: checklist in §17 checked.

## 17. Final Verification Checklist
- [x] No Apple Sign-In UI or capability added anywhere
- [x] Success path produces an identical `AuthStateHolder` transition to OTP success
- [x] Cancellation is handled as a neutral state, not an error
- [x] Reactivation-required response routes to a distinct reactivation UI, not fresh registration
- [x] Raw Google ID token never persisted client-side beyond the in-flight request
- [x] `login_started` (method=google) emitted correctly

## 18. Definition of Done
Google Sign-In is live on both Android and iOS via a shared KMP abstraction, produces identical downstream session state to OTP verification, and correctly handles cancellation and reactivation edge cases. **(STATUS: IMPLEMENTED & VERIFIED)**
