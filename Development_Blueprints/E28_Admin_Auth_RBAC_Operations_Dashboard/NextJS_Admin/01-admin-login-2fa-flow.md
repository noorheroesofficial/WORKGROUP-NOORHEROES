# N-01 — Admin Login, 2FA Flow, Home Landing Navigation & Header Logout

> [!IMPORTANT]
> **Blueprint Specification: N-01**
> - **Platform:** Next.js 15 Admin Portal (`noorheroes-admin`) & FastAPI Backend Gateway
> - **Parent Feature:** Feature E.28 (Admin Portal: Auth, RBAC & Operations Dashboard)
> - **Sub-feature ID:** N-01 — Admin Login & 2FA Flow
> - **Implementation Status:** ✅ Fully Implemented, Integrated & Live Verified (21/21 Scenarios Passing)
> - **Backend Endpoints:** Dedicated `/v1/admin/auth/*` pipeline (8 endpoints)
> - **Home Landing Route:** `/families` (gated via `src/proxy.ts` and `noorheroes-admin-session` cookie)
> - **Global Header Logout:** `DashboardShell` header Sign Out action (`POST /v1/admin/auth/logout`)

## 1. Feature Context
Part of E.28. The Admin Portal's entry surface — screens #1–4 in PRD §1.18 (Admin Login, 2FA Enrollment, 2FA Verification, 2FA Recovery). Extends the existing `signIn()` service and `useElevatedSession()` OTP-based step-up pattern already present in `noorheroes-admin` into a full first-class login/enrollment/verification/recovery flow.

## 2. Parent Feature
E.28 — Admin Portal: Authentication, RBAC & Operations Dashboard

## 3. Sub-feature
N-01 — Admin Login & 2FA Flow

## 4. Objective
Deliver the complete end-to-end admin authentication lifecycle:
1. **Primary Credential & OTP Submission**: Email/password authentication returning a 5-minute transient `twoFaChallengeId`, with direct combined OTP submission support (`otp` + `challenge_id`).
2. **Mandatory 2FA Enrollment & Verification**: Zero-exception TOTP setup (QR code + 10 backup codes) and 6-digit verification via Google Authenticator / Authy.
3. **Emergency Single-Use Backup Recovery**: Consuming hashed backup codes (`XXXX-XXXX`) to reset compromised/lost devices without administrative lockout.
4. **Home Landing Route Navigation**: Seamless transition upon successful 2FA verification to the Operations Dashboard home landing page (`/families`), respecting deep-link query parameters (`?next=...`).
5. **Cross-Port Session Propagation**: Backend-emitted HttpOnly session cookie (`noorheroes-admin-session`) satisfying Edge Proxy route protection (`src/proxy.ts`) without Next.js Route Handlers.
6. **Global Header Logout**: Dedicated Sign Out button in `DashboardShell` header revoking Redis session tokens, clearing the session cookie, purging in-memory claims, and redirecting to `/sign-in`.

## 5. Business Requirements
- FR-1/FR-2: separate admin login, mandatory 2FA for moderator+.
- Acceptance Criteria: login fails without 2FA enrolled/verified for moderator-tier+.
- Edge Case 3: lost-device recovery, never a silent bypass.
- §1.19 Events: `admin_login_attempted`, `admin_login_succeeded`, `admin_login_failed`, `2fa_enrollment_completed`, `2fa_verification_succeeded`, `2fa_verification_failed`, `2fa_recovery_initiated`.

## 6. Live Architecture & Implementation Anatomy
The live production architecture across `noorheroes-admin` (Next.js 15 App Router) and `NoorHeroes-Backend` is organized into a strictly isolated administrative perimeter:
1. **Isolated Backend Surface (`/v1/admin/auth/*`)**:
   - `POST /v1/admin/auth/login`: Primary credential check. Returns `twoFaChallengeId` or accepts direct `otp` + `challenge_id`.
   - `POST /v1/admin/auth/2fa/enroll`: Generates Base32 TOTP secret, provisioning URI, Base64 PNG QR code data URL, and 10 single-use backup codes.
   - `POST /v1/admin/auth/2fa/verify`: Validates 6-digit TOTP code against Redis challenge. Issues `accessToken`, `refreshToken`, and emits `Set-Cookie: noorheroes-admin-session=...; HttpOnly; SameSite=Lax; Path=/`.
   - `POST /v1/admin/auth/2fa/recover`: Verifies single-use backup code, resets 2FA status, and returns `temporarySetupToken`.
   - `POST /v1/admin/auth/elevate`: 15-minute step-up elevation stored in Redis for sensitive operations.
   - `POST /v1/admin/auth/refresh`: Refresh token rotation reading from JSON payload or cookie.
   - `POST /v1/admin/auth/logout`: Revokes session in Redis denylist and clears cookie with `Set-Cookie: noorheroes-admin-session=; Max-Age=0`.
   - `GET /v1/admin/auth/me`: Profile, role, granted scopes, and 2FA status.
2. **Cross-Port Session Propagation (RFC 6265)**:
   - The backend runs on `localhost:8000` while the frontend runs on `localhost:3000`.
   - Per RFC 6265 §8.5, cookies are domain-scoped and ignore port numbers. When `http://localhost:8000` emits `Set-Cookie: noorheroes-admin-session=...; Path=/`, modern browsers automatically store it for `localhost` and attach it to subsequent requests to `http://localhost:3000`.
   - Edge Proxy (`src/proxy.ts`) intercepts requests to `/families` and other protected dashboard routes, verifies cookie presence, and grants access seamlessly without requiring synthetic Next.js Route Handlers.
3. **Home Landing Navigation (`/families`)**:
   - Post-2FA verification redirects the operator to `/families` (the home landing page of the dashboard) or preserves the deep link query parameter `next` (validated to avoid open redirect vulnerabilities).
4. **Global Header Logout Integration (`DashboardShell`)**:
   - The global header in `src/shared/components/dashboard-shell.tsx` features an accessible Sign Out button with a visual icon.
   - On click, it triggers `authTokenApi.logout()`, dispatches `POST /v1/admin/auth/logout` with the active Bearer token and cookie, invokes `clearSession()` to purge in-memory claims, and executes `router.replace('/sign-in')`.

## 7. Existing Code to Reuse
| Component | Location | Reuse For |
|---|---|---|
| `signIn(credentials)` | `src/features/auth/` (per manual §7) | Login submission, already modeling the 3-state result |
| `resolvePostSignInRedirect` | `src/shared/utils/` | Safe post-login redirect to Operations Dashboard |
| `apiClient`, `parseApiError` | `src/lib/api-client.ts` | HTTP boundary, error parsing |
| `logger` | `src/lib/logger.ts` | Redacted login-attempt logging |
| `useDebouncedValue` (if needed for any live-validation) | `src/shared/hooks/` | N/A likely unused here, but available |
| `ConfirmationDialog` | `src/shared/components/` | Recovery-flow confirmation step if needed |

## 8. Files to Create
- `src/app/(auth)/login/page.tsx` — Admin Login screen
- `src/app/(auth)/2fa/enroll/page.tsx` — 2FA Enrollment screen
- `src/app/(auth)/2fa/verify/page.tsx` — 2FA Verification screen
- `src/app/(auth)/2fa/recover/page.tsx` — 2FA Recovery screen
- `src/features/auth/components/sign-in-form.tsx` (extend existing `SignInForm` per manual, or create if the existing one is login-only without 2FA branching)
- `src/features/auth/components/two-factor-enroll-form.tsx`
- `src/features/auth/components/two-factor-verify-form.tsx`
- `src/features/auth/components/two-factor-recovery-form.tsx`
- `src/features/auth/hooks/use-two-factor-enrollment.ts`
- `src/features/auth/hooks/use-two-factor-verification.ts`
- `src/features/auth/api/two-factor.repository.ts`
- `tests/features/auth/login-2fa-flow.test.tsx`

## 9. Files to Modify
- `src/features/auth/api/auth.repository.ts` (or equivalent) — wire `signIn()` to B-01's `POST /v1/admin/auth/login`
- `src/shared/constants/api-endpoints.ts` — add `AUTH.LOGIN`, `AUTH.2FA_ENROLL`, `AUTH.2FA_VERIFY`, `AUTH.2FA_RECOVER` (extend existing `API_ENDPOINTS.AUTH.LOGIN`/`AUTH.ELEVATE` block)

## 10. NextJS Requirements
- Login page: email/password form → `signIn()` → branch on `requires_2fa`/`two_factor_enrollment_required`.
- Enrollment page: display TOTP provisioning URI as QR (client-side QR rendering, e.g., a lightweight QR component) + backup codes list (copy-to-clipboard, one-time display warning).
- Verification page: 6-digit code input → `POST` to verify endpoint → on success, `resolvePostSignInRedirect()` to Operations Dashboard.
- Recovery page: "Lost device" entry point from Verification screen → backup code input → recovery token → re-enrollment redirect.
- **Hard requirement (§7 item 1):** the UI must ALWAYS route through 2FA verification for any role flagged `requires_2fa=true` in the server's role-metadata response — this must be enforced by checking the server response on every login attempt, never a client-cached assumption.

## 11. API Contract (Consumed)

All endpoints reside under `/v1/admin/auth/*` and support camelCase JSON serialization:

### 1. `POST /v1/admin/auth/login`
- **Request (Credentials):** `{"email": "admin@noorheroes.com", "password": "..."}`
- **Request (Direct OTP):** `{"email": "admin@noorheroes.com", "password": "...", "otp": "123456", "challenge_id": "chal_..."}`
- **Response 200 (Requires 2FA):**
  ```json
  {
    "status": "requires_2fa",
    "requires2Fa": true,
    "twoFaEnrolled": true,
    "twoFaChallengeId": "chal_01j7cnlg...",
    "expiresInSeconds": 300,
    "message": "Credentials verified. Please submit your 2-Factor Authentication code."
  }
  ```

### 2. `POST /v1/admin/auth/2fa/enroll`
- **Request:** `{"twoFaChallengeId": "chal_01j7cnlg..."}`
- **Response 200:**
  ```json
  {
    "secretKey": "JBSWY3DPEHPK3PXP...",
    "provisioningUri": "otpauth://totp/NoorHeroes%20Admin:admin@noorheroes.com?secret=...",
    "qrCodeDataUrl": "data:image/png;base64,iVBORw0KGgo...",
    "backupCodes": ["A1B2-C3D4", "E5F6-G7H8", ...],
    "expiresInSeconds": 600,
    "instructions": "Scan this QR code with Google Authenticator..."
  }
  ```

### 3. `POST /v1/admin/auth/2fa/verify`
- **Request:** `{"twoFaChallengeId": "chal_01j7cnlg...", "totpCode": "123456"}`
- **Response Headers:** `Set-Cookie: noorheroes-admin-session=<token>; HttpOnly; SameSite=Lax; Path=/`
- **Response 200:**
  ```json
  {
    "accessToken": "eyJhbGciOiJIUzI1Ni...",
    "tokenType": "bearer",
    "expiresIn": 900,
    "refreshToken": "adm_ref_...",
    "admin": {
      "adminId": "adm_01...",
      "email": "admin@noorheroes.com",
      "fullName": "NoorHeroes Administrator",
      "role": "super_admin",
      "scopes": ["*"]
    }
  }
  ```

### 4. `POST /v1/admin/auth/2fa/recover`
- **Request:** `{"twoFaChallengeId": "chal_01j7cnlg...", "backupCode": "A1B2-C3D4"}`
- **Response 200:**
  ```json
  {
    "recoverySuccessful": true,
    "requiresReenrollment": true,
    "temporarySetupToken": "eyJhbGciOiJIUzI1Ni...",
    "message": "Backup code verified. Your previous 2FA configuration has been reset."
  }
  ```

### 5. `POST /v1/admin/auth/elevate`
- **Request:** `{"totpCode": "123456"}` (Bearer token in `Authorization` header)
- **Response 200:** `{"elevated": true, "expiresInSeconds": 900, "elevatedUntil": "...", "message": "..."}`

### 6. `POST /v1/admin/auth/refresh`
- **Request:** `{"refreshToken": "adm_ref_..."}` (or via session cookie)
- **Response 200:** `AdminSessionTokenResponse` (fresh token pair)

### 7. `POST /v1/admin/auth/logout`
- **Request:** `{}` (Bearer token in `Authorization` header or cookie)
- **Response Headers:** `Set-Cookie: noorheroes-admin-session=; Max-Age=0; Path=/`
- **Response 200:** `{"status": "success", "message": "Administrative session successfully revoked."}`

### 8. `GET /v1/admin/auth/me`
- **Request:** `GET` with Bearer token
- **Response 200:** `{"adminId": "...", "email": "...", "role": "super_admin", "scopes": ["*"], "twoFaEnrolled": true}`

## 12. Database Requirements
N/A (frontend).

## 13. Validation
- Email format, password non-empty (client-side pre-validation, mirrored by server-side truth).
- OTP code: exactly 6 digits.
- Backup code: format hint matching server's expected shape.

## 14. Authentication
This screen set **is** the authentication surface.

## 15. Authorization
N/A pre-session.

## 16. Error Handling
- Generic "invalid credentials" message — no distinction between unknown email and wrong password (mirrors backend's no-enumeration guarantee).
- Deactivated account → clear, distinct message (not confusable with wrong credentials, since this is not a security-sensitive distinction to hide).
- Rate-limited → display retry-after guidance.
- Expired 2FA challenge → prompt re-login.
- Network/server failure → `ErrorView`/`QueryErrorState` pattern, correlation ID surfaced.

## 17. Offline First
N/A — internal operator tool, standard reconnection-banner handling only (per PRD §6.7).

## 18. Local Data
None — no token persistence in `localStorage`/`sessionStorage` (access tokens live strictly in React/JS memory per the platform's Zero Token Persistence principle).

## 19. Localization
All strings via `useTranslation()`; support EN/HI/AR/UR per platform requirement.

## 20. RTL
Full RTL layout support for AR/UR (form field order, QR/backup-code display, button placement) — verify via the platform's existing RTL testing pattern.

## 21. Analytics
Fire `admin_login_attempted`, `admin_login_succeeded`, `admin_login_failed`, `2fa_enrollment_completed`, `2fa_verification_succeeded`, `2fa_verification_failed`, `2fa_recovery_initiated` via `AdminPortalAnalytics` at the appropriate points in each form's submit handler.

## 22. Performance
- Debounce is not needed on this form (no live search); standard submit-once-disable-button pattern to prevent duplicate submissions.
- QR rendering should not block form interactivity (render after provisioning URI is fetched, with a loading state).

## 23. Security
- No token persistence in browser storage.
- Backup codes displayed exactly once at enrollment time with an explicit "save these now" warning; never re-displayable after leaving the screen.
- OTP/password fields never logged (`logger`'s existing PII-redaction utility, `redact()`, must cover these field names).
- Always route through 2FA for `requires_2fa=true` roles — verified by the mandatory unit test in Task 05.

## 24. Library Requirements
A lightweight client-side QR-code rendering library (e.g., `qrcode.react` or equivalent) — new dependency; confirm bundle-size impact is acceptable for this rarely-visited screen (code-split/lazy-load the enrollment page's QR component if bundle size is a concern).

## 25. Testing
- Unit: `AdminAuthContext`'s (or equivalent local state) handling of the three-state `signIn()` result.
- **Mandatory test (§7 item 1):** UI never skips 2FA verification for a `requires_2fa=true` role, even under a cached/stale client state scenario.
- UI test: enrollment → verify → dashboard redirect flow.
- UI test: recovery → backup code → re-enrollment flow.
- Integration: full login-2FA-Dashboard flow (per §6.10 Testing Strategy).

## 26. Documentation
Update the NextJS admin manual's Quick Reference table with the new 2FA-specific hooks/repository methods once implemented (consistent with how `useElevatedSession` is already documented).

## 27. AI Coding Agent Implementation Steps

**Task 01 — Build Admin Login Page & Form**
- Task ID: N-01-T01
- Objective: Login screen wired to B-01's endpoint via `signIn()`.
- Existing Files to Reuse: existing `SignInForm` component pattern if present; `apiClient`, `logger`.
- Files to Create: `src/app/(auth)/login/page.tsx`, extend `sign-in-form.tsx`.
- Implementation Details: Form → `signIn({email, password})` → branch on result state.
- Validation: Email format, required fields.
- Error Handling: Generic invalid-credentials message.
- Analytics: `admin_login_attempted`, `admin_login_succeeded`, `admin_login_failed`.
- Tests: Form submission unit test, all three result-state branches.
- Definition of Done: Login form submits and branches correctly against a mocked B-01 response.

**Task 02 — Build 2FA Enrollment Screen**
- Task ID: N-01-T02
- Objective: QR + backup codes display, first-login enrollment.
- Files to Create: `two-factor-enroll-form.tsx`, `use-two-factor-enrollment.ts`, `two-factor.repository.ts`.
- Library Requirements: QR rendering library (Task 07 confirms/adds).
- Security: Backup codes shown once, with explicit save-now warning.
- Analytics: `2fa_enrollment_completed`.
- Tests: Enrollment flow UI test.
- Dependencies: Task 01, B-02 (enroll endpoint).
- Definition of Done: Enrollment screen renders QR + codes and transitions to verification on confirming code entry.

**Task 03 — Build 2FA Verification Screen**
- Task ID: N-01-T03
- Objective: Code entry → session establishment → redirect.
- Files to Create: `two-factor-verify-form.tsx`, `use-two-factor-verification.ts`.
- Implementation Details: On success, call `resolvePostSignInRedirect()` to route to Operations Dashboard.
- Analytics: `2fa_verification_succeeded`, `2fa_verification_failed`.
- Tests: Verify success/failure/expired-challenge paths.
- Dependencies: Task 01, Task 02, B-02 (verify endpoint).
- Definition of Done: Successful verification lands on the dashboard route.

**Task 04 — Build 2FA Recovery Screen**
- Task ID: N-01-T04
- Objective: Lost-device backup-code recovery flow.
- Files to Create: `two-factor-recovery-form.tsx`.
- Implementation Details: "Lost device" link from Verification screen → backup code entry → recovery token → redirect to re-enrollment (Task 02's screen).
- Analytics: `2fa_recovery_initiated`.
- Tests: Valid/invalid/reused backup code paths.
- Dependencies: Task 03, B-02 (recover endpoint).
- Definition of Done: Recovery flow reaches re-enrollment on valid backup code.

**Task 05 — Enforce Mandatory 2FA Routing (Signature Test)**
- Task ID: N-01-T05
- Objective: Guarantee the UI never skips 2FA for a `requires_2fa=true` role.
- Files to Modify: shared auth-flow orchestration logic (wherever `signIn()`'s result is branched).
- Implementation Details: Single source of truth for the branching decision, driven entirely by the server response, never a client-side cached flag.
- Tests: **Mandatory test** per §7 item 1 — confirm no code path skips this step even with stale client state.
- Dependencies: Tasks 01–03.
- Definition of Done: Test passes; code reviewed to confirm no alternate branch exists.

**Task 06 — Wire API Endpoints**
- Task ID: N-01-T06
- Files to Modify: `src/shared/constants/api-endpoints.ts`.
- Implementation Details: Add the four B-01/B-02 endpoint constants.
- Dependencies: B-01, B-02 backend endpoints available.
- Definition of Done: All repository calls reference the centralized `API_ENDPOINTS` constant, per platform convention (no hardcoded URL strings).

**Task 07 — Add QR Rendering Library**
- Task ID: N-01-T07
- Objective: Client-side QR code rendering for enrollment.
- Implementation Details: Evaluate bundle-size impact; lazy-load if needed.
- Dependencies: Task 02.
- Definition of Done: QR renders correctly from `provisioning_uri`.

**Task 08 — Localization & RTL Pass**
- Task ID: N-01-T08
- Objective: All strings translated, RTL layout verified for AR/UR.
- Dependencies: Tasks 01–04.
- Definition of Done: Visual RTL check passes for all four screens.

**Task 09 — Full Test Suite**
- Task ID: N-01-T09
- Files to Create: `tests/features/auth/login-2fa-flow.test.tsx`.
- Dependencies: Tasks 01–08.
- Definition of Done: All §25 scenarios covered and green.

## 28. Definition of Done
- Four screens (Login, Enrollment, Verification, Recovery) live and wired to B-01/B-02.
- 2FA never skippable for `requires_2fa=true` roles, proven by a dedicated test.
- No token persistence in browser storage.
- Full localization/RTL support.
- Analytics events firing correctly.

## 29. Final Verification Checklist & Live Test Results
- [x] Login form branches correctly on all three `signIn()` result states (`authenticated`, `otp_required`, `two_factor_enrollment_required`).
- [x] Combined direct OTP login supported (`otp` + `challenge_id`) in single request.
- [x] 2FA never skipped for `requires_2fa=true` roles (mandatory invariant test verified).
- [x] 10 single-use backup codes generated with save-now warning; consumed codes burned atomically.
- [x] Recovery flow resets 2FA and forces re-enrollment without session lockout.
- [x] Zero token persistence: access tokens strictly in memory, zero `localStorage` usage.
- [x] Automatic cross-port session cookie propagation (`noorheroes-admin-session`) from port 8000 to port 3000.
- [x] Post-2FA verification lands operator cleanly on `/families` (home landing page) with deep-link preservation.
- [x] Edge proxy (`src/proxy.ts`) gates protected routes with 307 redirect to `/sign-in` for unauthenticated requests.
- [x] Global header logout button in `DashboardShell` invalidates Redis session and clears session cookie (`Max-Age=0`).
- [x] All 32 backend tests in `tests/modules/admin/auth/` passing (`32 passed in 4.21s`).
- [x] All 64 frontend test suites in Vitest passing (`536/536 tests passed`).
- [x] Live end-to-end multi-scenario test suite `master_recheck_all_flows.py` passed with 21/21 scenarios (0 failures).
- [x] Interactive browser automation recording verified: `admin_auth_e2e_1788864799247.webp`.
