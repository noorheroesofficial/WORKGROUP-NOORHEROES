# K-03 — Parent Registration, Consent & OTP Verification Flow

> **Status:** ✅ **Implemented & Verified** (Live simulator verified on Android `emulator-5554` with live FastAPI backend)

## 1. Feature Context
The trust-critical, legally-weighted core of onboarding: phone/email registration with granular consent capture, then OTP verification. Highest-risk screens for accessibility regressions and the primary funnel drop-off point (target ≤15% drop-off at OTP).

## 2. Parent Feature
Feature A.1 — Splash, Language Selection, Authentication & Onboarding

## 3. Sub-feature
2.3 Parent Registration, Consent & OTP Verification Flow (ID: **K-03**)

## 4. Objective
Build Registration+Consent, Consent Detail Modal, OTP Verification, and OTP Fallback Offer screens against B-02's API, with derived-state Submit gating, auto-advancing OTP cells, server-driven countdown, and full accessibility/RTL coverage.

## 5. Business Requirements
- FR-5: 3 required + 3 optional consent checkboxes; Submit disabled until all required boxes checked.
- FR-7: OTP 6 digits, paste support, auto-submit on 6th digit, server-authoritative resend countdown.
- FR-9: Enumeration-safe — generic error messaging only, never signal identifier existence pre-verification.
- Edge Case: SMS arrives after a second code requested — both codes remain valid within their own TTL.
- Edge Case: Device clock skew — client must not compute its own OTP expiry; display is driven by server-provided `expires_at`/`resend_available_at`.
- Loading State: OTP send button spinner + disable re-tap; 10s timeout shows retry.
- Accessibility: each consent row independently focusable/toggleable, full label read; OTP cells labeled "Digit 1 of 6"; errors announced via live region.

## 6. Existing Architecture
`core-network`'s `AuthApiService` (extend with `register()`, `requestOtp()`, `verifyOtp()`, `startRecovery()`); `core-ui`'s `NoorPinInput` (existing OTP/PIN component, extended — see §7's resolved decision — do not build a new digit-cell component from scratch); `core-security`'s `AuthRepository`/`AuthStateHolder` for post-verify session transition.

## 7. Existing Code to Reuse
- `core-ui/component`: `NoorPinInput` — **resolved architecture decision:** `CORE_UI_INSTRUCTIONS.md`'s component inventory describes this component only as "secure PIN/OTP entry with automatic masking," with no mention of paste-distribution, auto-advance-focus, or auto-submit-on-Nth-digit in its documented capability list. Treat these three OTP-specific behaviors as **not present today** and build them as an extension of the existing component (never a forked parallel component) — see Task 03 for the extension plan and its backward-compatibility constraint for other existing consumers (e.g., K-05's 4–6 digit PIN entry, which must keep working unchanged).
- `core-network`: `AuthApiService`, `safeCall`
- `core-security`: `AuthRepository.login()`/`verifyOtp()` interface shape (extend to match B-02's actual contract), `MutableAuthStateHolder` (data-layer only, never called from ViewModel directly — go through `AuthRepositoryImpl`)
- `core-ui`: `PrimaryButton` (loading-state support), `NoorToggle` (consent checkboxes), `BaseViewModel`

## 8. Files to Create
- `feature/onboarding/ui/RegistrationConsentScreen.kt`
- `feature/onboarding/ui/ConsentDetailModal.kt`
- `feature/onboarding/ui/OtpVerificationScreen.kt`
- `feature/onboarding/ui/OtpFallbackOfferScreen.kt`
- `feature/onboarding/viewmodel/RegistrationViewModel.kt`, `OtpVerificationViewModel.kt` (+ State/Event)
- `core-network/api/OtpDtos.kt` — `RegisterRequestDto`, `OtpRequestDto`, `OtpVerifyDto`, `TokenResponseDto`
- `test/feature/onboarding/RegistrationViewModelTest.kt`, `OtpVerificationViewModelTest.kt`
- `androidTest/feature/onboarding/RegistrationConsentScreenTest.kt`, `OtpVerificationScreenTest.kt`

## 9. Files to Modify
- `core-network/api/AuthApiService.kt` — add `register()`, `requestOtp()`, `verifyOtp()`, `startRecovery()`
- `core-security/AuthRepository.kt`/`AuthRepositoryImpl` — extend `login()`/`verifyOtp()` to match B-02's actual multi-step contract (registration_token → otp_id → tokens), update `MutableAuthStateHolder` transition on verify success
- `core-navigation/Route.kt` — add `RegistrationConsentRoute`, `OtpVerificationRoute`, `OtpFallbackOfferRoute`, `ForgotAccessRoute`

## 10. KMP Requirements
- Registration screen: phone/email segmented input, Google entry point (hands off to K-04), 6 consent rows; Submit `enabled` state is a `combine()` of the three required-consent `BooleanState`s — never a manually-set flag that can drift.
- OTP screen: `NoorPinInput` (or extended variant) with 6 cells, auto-advance focus, single-paste-event distribution across all 6 cells, auto-submit on 6th digit entry; countdown text driven by the server's `resend_available_at` timestamp (compute remaining seconds client-side from that timestamp, never from a client-started timer alone — resync on any resume).
- SMS auto-read (Android): via SMS Retriever API specifically (scoped permission, not broad SMS read) — if permission denied or unavailable, fall back to manual entry only, never block the flow.
- Lockout UI: after 5 failed attempts (server returns `423`), replace resend/retry UI with lockout messaging + estimated cooldown (derived from server response) + Support link.
- Fallback-channel offer: triggered only after a `503 OTP_PROVIDER_UNAVAILABLE` signal from `requestOtp()`, never speculatively shown.
- Enumeration-safety on the client: registration/recovery error messaging must be generic ("Something went wrong, please try again") — never differentiate "identifier exists" vs "identifier doesn't exist" in any client-rendered copy.
- Offline mid-flow: preserve all entered registration fields locally (in ViewModel state, debounced-persisted per K-07's draft mechanism — this sub-feature integrates with K-07 rather than building its own separate draft store).

## 11. Required API
- `POST /v1/identity/auth/register` (B-02)
- `POST /v1/identity/auth/otp/request` (B-02)
- `POST /v1/identity/auth/otp/verify` (B-02)
- `POST /v1/identity/auth/recovery/start` (B-02)

## 12. Offline First
Registration form remains fillable offline; Submit disabled with "Connect to the internet to continue" helper text replacing the spinner state — no silent failure.

## 13. Local Data
Integrates with K-07's `OnboardingViewModel`-scoped draft persistence for registration field values (not a separate DataStore key set) — see K-07 for the shared mechanism.

## 14. Localization
Full localization of registration/consent/OTP copy required; consent text specifically requires scholar/legal-reviewed translation (not machine translation) given its legal weight, per PRD §2.1.

## 15. RTL
Full mirroring including OTP cell layout — digit-entry order is explicitly preserved left-to-right even in RTL context (standard OTP UX convention), while the rest of the screen (labels, buttons, back arrow) mirrors normally. This is an explicitly called-out test case — do not let Compose's default RTL mirroring flip the OTP cell order.

## 16. Analytics
Emit `login_started` (method), `registration_started` (identifier_type), `consent_toggle_changed` (consent_key, new_value), `consent_full_text_opened` (document_type), `registration_submitted` (required_consents_complete), `otp_requested`, `otp_resend_requested`, `otp_verification_attempted`, `otp_verification_succeeded`, `otp_verification_failed`, `otp_lockout_triggered`, `otp_fallback_channel_offered`, `account_recovery_started`.

## 17. Performance
OTP send button disables re-tap for the request duration; 10s client-side timeout surfaces a retry option (does not cancel the in-flight request, just offers the user a retry affordance). Avoid recomposition on every digit keystroke beyond the single cell being edited.

## 18. Security
PIN/OTP digits never logged client-side (verify no `Log.d`/`println` of the code anywhere in the ViewModel or Composable). Certificate pinning inherited from `core-network`'s existing pinned `HttpClientEngine` — confirm this path isn't bypassed.

## 19. Testing
- Unit: Submit-enabled derived-state correctness (all combinations of the 3 required toggles); OTP auto-submit-on-6th-digit; paste-distribution-across-6-cells; countdown computed from server timestamp, not local timer drift; lockout-UI-trigger-at-423.
- UI: empty/error/loading/success states for Registration and OTP screens (Compose Test); RTL OTP-cell-order preservation test (explicit, per PRD).
- Accessibility (TalkBack traversal, highest priority per PRD): Registration consent rows read as "Required: I agree to..., toggle, currently off"; OTP cells read as "Digit 1 of 6"; live-region announcement on OTP error.

## 20. AI Coding Agent Implementation Steps

**Task 01 — Extend `AuthApiService` and Add OTP DTOs**
Objective: Network contract for B-02's four endpoints. Follow: existing `safeCall` pattern. Files to Create: `OtpDtos.kt`. Files to Modify: `AuthApiService.kt`. Tests: DTO round-trip tests against B-02's documented JSON shapes. Definition of Done: all four calls typed and tested.

**Task 02 — Extend `AuthRepository`/`AuthRepositoryImpl` for Multi-Step OTP Flow**
Objective: Bridge registration_token → otp_id → tokens into the existing `AuthRepository` interface shape, updating `MutableAuthStateHolder` on verify success. Follow: `core-security`'s existing auth-state transition pattern — do not bypass `MutableAuthStateHolder` from the ViewModel. Tests: state-transition tests (Unauthenticated → Parent on verify success). Dependencies: Task 01. Definition of Done: `AuthStateHolder` correctly reflects `Parent` state immediately after a successful verify, observable by the rest of the app.

**Task 03 — Extend `NoorPinInput` with Auto-Advance, Paste-Distribution, and Auto-Submit**
Objective: Add the three OTP-specific behaviors confirmed absent from `NoorPinInput`'s documented capability set (§7): auto-advance focus per digit, single-paste-event distribution across all cells, and an `onComplete` callback fired automatically on the Nth digit. Files to Modify: `core-ui`'s `NoorPinInput` component (cross-module change — coordinate carefully, this is a shared component consumed elsewhere). Implementation: add new optional constructor parameters (e.g., `autoAdvance: Boolean = false`, `onComplete: ((String) -> Unit)? = null`) so existing callers that only want masked entry (like K-05's PIN pad, which explicitly does *not* want auto-submit) are entirely unaffected by default — the new behaviors must be opt-in, not a change to the component's default behavior. Tests: paste-distribution unit/UI test; auto-advance-focus test; regression test confirming K-05's existing (or planned) usage renders identically with the new parameters left at their defaults. Definition of Done: `NoorPinInput` gains the three OTP behaviors as opt-in parameters with zero behavioral change for non-OTP callers.

**Task 04 — Implement `RegistrationViewModel` and Screen**
Objective: Registration+Consent screen with derived-state Submit gating. Follow: `BaseViewModel`, `combine()` for required-consent state. Business Rules: enumeration-safe generic error copy only. Tests: full Submit-gating matrix. Dependencies: Tasks 01–02. Definition of Done: Submit never enables via any path other than all-three-required-true.

**Task 05 — Implement `ConsentDetailModal`**
Objective: Scrollable legal text modal with visible version stamp, single source of truth shared with the full ToS/Privacy/Child-Data documents. Follow: `NoorBottomSheet` or `NoorDialog` pattern from `core-ui`. Tests: version-stamp-visible assertion. Dependencies: Task 04. Definition of Done: modal content source matches the full-document screens exactly (no content duplication/drift).

**Task 06 — Implement `OtpVerificationViewModel` and Screen**
Objective: Server-driven countdown, auto-submit, lockout UI, SMS Retriever integration. Follow: `BaseViewModel`, Android `SmsRetrieverClient` (scoped API only). Business Rules: countdown computed from `resend_available_at`, resynced on resume; lockout only from server `423`, never client-guessed. Tests: full matrix per §19. Dependencies: Tasks 01–03. Definition of Done: countdown survives app backgrounding/foregrounding without drifting from server time.

**Task 07 — Implement `OtpFallbackOfferScreen`**
Objective: Triggered only on `503 OTP_PROVIDER_UNAVAILABLE`. Follow: modal/inline pattern per screen inventory. Tests: trigger-only-on-503 assertion (never speculative). Dependencies: Task 06. Definition of Done: fallback offer never appears absent the specific server signal.

**Task 08 — RTL OTP-Cell-Order Verification**
Objective: Explicit test confirming OTP digit order stays LTR even under RTL `LayoutDirection`. Follow: Compose preview + instrumented test with forced RTL locale. Tests: the explicit PRD-called-out test case. Dependencies: Task 06. Definition of Done: test passes under `ar`/`ur` locale configuration.

**Task 09 — Accessibility Pass**
Objective: TalkBack traversal order and labeling for Registration and OTP screens specifically (PRD-flagged as highest-risk). Follow: `semantics {}` blocks matching the exact label text in the PRD (§2.4). Tests: accessibility traversal test. Dependencies: Tasks 04, 06. Definition of Done: matches PRD-specified label strings exactly.

**Task 10 — Add Analytics Instrumentation**
Objective: All events in §16. Follow: `AnalyticsTracker`, ViewModel-only. Tests: fake-tracker assertions. Dependencies: Tasks 04, 06. Definition of Done: one call site per event.

**Task 11 — Integrate with K-07 Draft Persistence**
Objective: Registration field values participate in the shared `OnboardingViewModel`-scoped draft, not a separate store. Dependencies: K-07 (may need to be sequenced together or this task deferred until K-07 lands). Definition of Done: offline-entered registration data survives a process kill, verified by an integration test shared with K-07's suite.

**Task 12 — Add Full Test Suite**
Objective: Complete coverage per §19. Definition of Done: all green in CI.

**Task 13 — Final Code Review**
Objective: Confirm enumeration-safe copy throughout, zero OTP/PIN logging, RTL OTP-order correctness, accessibility labels match spec. Definition of Done: checklist in §21 checked.

## 21. Final Verification Checklist
- [x] Submit button enabled only via derived `combine()` state of all three required consents
- [x] OTP auto-advance, paste-distribution, and auto-submit-on-6th-digit all functional
- [x] Countdown driven by server `resend_available_at`, resynced on resume, never local-timer-only
- [x] Lockout UI appears only on server `423`, never client-guessed
- [x] Fallback-channel offer appears only on server `503 OTP_PROVIDER_UNAVAILABLE`
- [x] All client-rendered error copy is enumeration-safe (generic, never existence-revealing)
- [x] OTP digit order stays LTR under RTL layout — explicit test passes
- [x] TalkBack labels match PRD spec exactly for consent rows and OTP cells
- [x] No OTP/PIN digits logged anywhere in the client
- [x] All analytics events in §16 emitted correctly

## 22. Definition of Done
Registration, Consent, and OTP Verification are live against B-02, fully accessible, fully RTL-correct on the OTP-order edge case, enumeration-safe end-to-end, and transition `AuthStateHolder` correctly on success — handing off to K-05 (PIN Setup) for new users or K-08 (Profile Picker) for returning users. **(STATUS: IMPLEMENTED & VERIFIED)**
