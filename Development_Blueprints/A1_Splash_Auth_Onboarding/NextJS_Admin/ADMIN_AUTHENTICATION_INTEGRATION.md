# NoorHeroes Admin Portal — Next.js 15 Authentication & 2FA Integration Specification
**Document ID:** `SPEC-E28-NEXTJS-ADMIN-AUTH-INTEGRATION`  
**Reference Backend Spec:** `docs/Development_Blueprints/A1_Splash_Auth_Onboarding/Backend/ADMIN_AUTHENTICATION_IMPLEMENTATION.md`  
**Standard Blueprint ID:** `docs/Development_Blueprints/A1_Splash_Auth_Onboarding/NextJS_Admin/06-admin-authentication-2fa-integration.md` (N-06)  
**Target Repository:** `noorheroes-admin` (Next.js 15 App Router)  
**Status:** Implementation Ready  

---

## 1. Integration Scope & Architecture Overview

This document provides the complete integration specification connecting the Next.js 15 Admin Portal frontend (`noorheroes-admin`) to the backend Admin Authentication and 2-Factor Authentication (2FA) API specified in `ADMIN_AUTHENTICATION_IMPLEMENTATION.md`.

### Key Integration Principles
1. **Isolated Admin Identity Surface**: The Admin Portal exclusively communicates with `/v1/admin/auth/*`. It never calls parent/child routes (`/v1/identity/auth/*`).
2. **Zero-Exception 2FA Enforcement**: Every moderator+ role must complete TOTP authentication. If an account has `twoFaEnrolled == false`, the client forces redirection to the 2FA enrollment wizard.
3. **Zero Token Persistence**: Access tokens are kept strictly in React memory/Context to protect against XSS token harvesting. Refresh tokens are maintained via HttpOnly cookies.
4. **Step-Up 2FA Elevation**: Sensitive operations (e.g. Consent Audit Viewer, kill switches) seamlessly prompt for a fresh 6-digit TOTP code via a non-blocking modal, setting a 15-minute elevation window.
5. **Multi-Language & RTL**: Fully localized in English (`en`), Arabic (`ar` with full RTL layout), Urdu (`ur`), and Hindi (`hi`).

---

## 2. API Endpoint Mapping

| Backend Endpoint | HTTP Method | Next.js Repository Method | Description & Trigger |
|---|---|---|---|
| `/v1/admin/auth/login` | `POST` | `AdminAuthRepository.login(credentials)` | Initial email + password validation. Returns `twoFaChallengeId` and `twoFaEnrolled` status. |
| `/v1/admin/auth/2fa/enroll` | `POST` | `AdminAuthRepository.enroll2FA(challengeId)` | Generates TOTP Base32 secret, Base64 QR code data URL, and 10 single-use backup codes. |
| `/v1/admin/auth/2fa/verify` | `POST` | `AdminAuthRepository.verify2FA(challengeId, code)` | Validates 6-digit TOTP code. Mints `noorheroes-admin` access & refresh tokens. |
| `/v1/admin/auth/2fa/recover` | `POST` | `AdminAuthRepository.recover2FA(challengeId, code)` | Consumes a single-use backup code (`A1B2-C3D4`) when mobile device is lost. Forces re-enrollment. |
| `/v1/admin/auth/elevate` | `POST` | `AdminAuthRepository.elevateSession(code)` | Re-authenticates an active session with fresh TOTP code for high-risk operations (15-min TTL). |
| `/v1/admin/auth/refresh` | `POST` | `AdminAuthRepository.refreshToken(token)` | Exchanges expired access token for a new pair without re-prompting for credentials. |
| `/v1/admin/auth/logout` | `POST` | `AdminAuthRepository.logout()` | Invalidation of active admin session in Redis denylist. |
| `/v1/admin/auth/me` | `GET` | `AdminAuthRepository.getProfile()` | Fetches current admin user profile, role, and granted scopes for navigation shell. |

---

## 3. Screen Inventory & Component Hierarchy

### Screen 1: Admin Login (`/login`)
- **Route**: `src/app/(auth)/login/page.tsx`
- **Component**: `src/features/auth/components/admin-sign-in-form.tsx`
- **Fields**: Email (`input[type=email]`), Password (`input[type=password]`).
- **Behaviors**:
  - Submits to `/v1/admin/auth/login`.
  - If `twoFaEnrolled == true`: Navigates to `/2fa/verify` passing `twoFaChallengeId` in router state.
  - If `twoFaEnrolled == false`: Navigates to `/2fa/enroll` passing `twoFaChallengeId` in router state.
  - Uniform "Invalid email or password" error on failure (no user enumeration).

### Screen 2: 2FA Setup & QR Enrollment (`/2fa/enroll`)
- **Route**: `src/app/(auth)/2fa/enroll/page.tsx`
- **Component**: `src/features/auth/components/two-factor-qr-enrollment.tsx`
- **Elements**:
  - Base64 PNG QR Code image for Google Authenticator / Authy / 1Password scanning.
  - Manual entry string (Base32 secret) with one-click copy button.
  - Grid of 10 single-use backup codes (format: `XXXX-XXXX`).
  - "Download Codes (.txt)" and "Copy to Clipboard" buttons.
  - Acknowledgment checkbox: *"I have securely saved these backup codes."*
  - Segmented 6-digit input for initial code confirmation.
- **Behaviors**:
  - Calls `/v1/admin/auth/2fa/verify` with initial code to confirm enrollment.
  - On success: Saves access token to session store, redirects to `/dashboard`.

### Screen 3: 2FA Verification Challenge (`/2fa/verify`)
- **Route**: `src/app/(auth)/2fa/verify/page.tsx`
- **Component**: `src/features/auth/components/two-factor-verify-form.tsx`
- **Elements**:
  - Segmented 6-digit input (`two-factor-segmented-input.tsx`) with auto-advance and clipboard paste support.
  - Active challenge countdown timer (300s).
  - Attempt counter warning (max 3 attempts).
  - Secondary link: *"Lost your authenticator device? Use a backup code."* leading to `/2fa/recover`.

### Screen 4: Emergency Backup Code Recovery (`/2fa/recover`)
- **Route**: `src/app/(auth)/2fa/recover/page.tsx`
- **Component**: `src/features/auth/components/two-factor-recovery-form.tsx`
- **Elements**:
  - 8-character segmented or formatted text input (`A1B2-C3D4`).
  - Explanation: *"Entering a valid backup code will immediately reset your 2FA device and require setting up a new authenticator."*
- **Behaviors**:
  - Calls `/v1/admin/auth/2fa/recover`.
  - On success: Automatically redirects to `/2fa/enroll` to set up a new Google Authenticator configuration.

### Component: Step-Up 2FA Elevation Modal
- **Component**: `src/features/auth/components/step-up-elevation-modal.tsx`
- **Hook**: `src/features/auth/hooks/use-elevated-admin-session.ts`
- **Usage**:
  - Wraps sensitive action handlers or routes (e.g. Consent Audit Viewer N-03, Feature Flag Kill Switch).
  - Displays modal prompt requesting current 6-digit TOTP code without kicking the user out of their active screen.
  - Calls `/v1/admin/auth/elevate`.
  - On success: Grants 15-minute elevation window (`elevatedUntil`) and executes the deferred action.

---

## 4. Frontend Types & Zod Contract

```typescript
// src/features/auth/types/admin-auth.ts
import { z } from 'zod';

export const AdminLoginRequestSchema = z.object({
  email: z.string().email(),
  password: z.string().min(1),
});
export type AdminLoginRequest = z.infer<typeof AdminLoginRequestSchema>;

export const AdminLoginResponseSchema = z.object({
  status: z.string(),
  requires2Fa: z.boolean(),
  twoFaEnrolled: z.boolean(),
  twoFaChallengeId: z.string(),
  expiresInSeconds: z.number(),
  message: z.string(),
});
export type AdminLoginResponse = z.infer<typeof AdminLoginResponseSchema>;

export const TwoFAEnrollResponseSchema = z.object({
  secretKey: z.string(),
  provisioningUri: z.string(),
  qrCodeDataUrl: z.string(),
  backupCodes: z.array(z.string()).length(10),
  expiresInSeconds: z.number(),
  instructions: z.string(),
});
export type TwoFAEnrollResponse = z.infer<typeof TwoFAEnrollResponseSchema>;

export const TwoFAVerifyRequestSchema = z.object({
  twoFaChallengeId: z.string(),
  totpCode: z.string().regex(/^\d{6}$/),
});
export type TwoFAVerifyRequest = z.infer<typeof TwoFAVerifyRequestSchema>;

export const AdminSessionTokenResponseSchema = z.object({
  accessToken: z.string(),
  tokenType: z.literal('bearer'),
  expiresIn: z.number(),
  refreshToken: z.string(),
  admin: z.object({
    adminId: z.string(),
    email: z.string(),
    fullName: z.string(),
    role: z.string(),
    scopes: z.array(z.string()),
  }),
});
export type AdminSessionTokenResponse = z.infer<typeof AdminSessionTokenResponseSchema>;

export const AdminElevateResponseSchema = z.object({
  elevated: z.boolean(),
  expiresInSeconds: z.number(),
  elevatedUntil: z.string(),
  message: z.string(),
});
export type AdminElevateResponse = z.infer<typeof AdminElevateResponseSchema>;
```

---

## 5. Implementation Roadmap (Tasks)

1. **Task 01**: Register endpoints in `src/shared/constants/api-endpoints.ts`.
2. **Task 02**: Add types & Zod schemas in `src/features/auth/types/admin-auth.ts`.
3. **Task 03**: Implement `AdminAuthRepositoryImpl` in `src/features/auth/api/admin-auth-repository.ts`.
4. **Task 04**: Build accessible 6-box input `two-factor-segmented-input.tsx`.
5. **Task 05**: Build `two-factor-qr-enrollment.tsx` and route `/2fa/enroll`.
6. **Task 06**: Build `two-factor-verify-form.tsx` and route `/2fa/verify`.
7. **Task 07**: Build `two-factor-recovery-form.tsx` and route `/2fa/recover`.
8. **Task 08**: Implement `useElevatedAdminSession` hook and `StepUpElevationModal`.
9. **Task 09**: Wire elevation hook into `src/features/consent-audit/components/step-up-gate.tsx`.
10. **Task 10**: Write unit and component integration tests.
