# B-03 — Google OAuth Parent Authentication API

> **Status:** COMPLETED / VERIFIED  
> **Implementation Artifacts:**  
> - Infrastructure Verifier: `src/noorheroes/infrastructure/oauth/google_oauth_verifier.py`  
> - Schemas: `src/noorheroes/modules/identity/google_auth_schemas.py`  
> - Service Layer: `src/noorheroes/modules/identity/otp_service.py` (`authenticate_via_google`)  
> - Router: `src/noorheroes/modules/identity/api.py` (`POST /v1/identity/auth/google`) & `src/noorheroes/api/v1/router.py` (`POST /v1/auth/google`)  
> - Test Suites: `tests/infrastructure/oauth/test_google_oauth_verifier.py`, `tests/modules/identity/test_google_auth_service.py`, `tests/modules/identity/test_google_auth_api.py` (26/26 tests passing)

## 1. Feature Context
Alternate parent-identity path alongside OTP (B-02). Maps to the exact same downstream flow (consent if new, Profile Picker if returning) so the client and rest of the backend never need to branch on auth method past this point. Apple Login is explicitly out of scope (FR-6).

## 2. Parent Feature
Feature A.1 — Splash, Language Selection, Authentication & Onboarding

## 3. Sub-feature
1.3 Google OAuth Parent Authentication API (ID: **B-03**)

## 4. Objective
Implement `POST /v1/identity/auth/google`, verifying the Google ID token server-side (signature/audience/issuer) and producing the identical `TokenResponse` shape as OTP verification success.

## 5. Business Requirements
- FR-6: Google Login is a supported identity method; Apple Login is explicitly not supported — do not implement it, do not add a placeholder for it.
- FR-21: Google Login must map to the same downstream flow as OTP-verified users (consent still required if new; profile picker if returning).
- Edge Case: Parent attempts Google login on an account linked to a deleted/soft-deleted family → recovery/reactivation flow triggers instead of fresh registration, with Support escalation if the retention window has lapsed.

## 6. Existing Architecture
Extends `IdentityService`/`IdentityRouter`. Reuses the same token-issuance and new-vs-returning branching logic built in B-02 (Task 07) — this endpoint must call the *same* internal "issue session for parent" helper, not a duplicate implementation, to guarantee identical downstream behavior.

## 7. Existing Code to Reuse
- `modules/identity/service.py` — the shared "issue session for parent_id, determine next_step" helper introduced in B-02 Task 07
- `core/security.py::create_access_token`
- `core/exceptions.py::AuthenticationError`

## 8. Files to Create
- `src/noorheroes/infrastructure/oauth/google_oauth_verifier.py` — `GoogleOAuthVerifier`
- `src/noorheroes/modules/identity/google_auth_schemas.py` — `GoogleAuthRequest`
- `tests/modules/identity/test_google_auth_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/identity/api.py` — add `POST /v1/identity/auth/google`
- `src/noorheroes/modules/identity/service.py` — add `authenticate_via_google(id_token, device_id)` calling the shared session-issuance helper
- `src/noorheroes/core/settings.py` — add `GOOGLE_OAUTH_CLIENT_ID` config key (name only)

## 10. Backend Requirements
- Verify the Google ID token's signature, audience (must match the configured client ID), and issuer directly against Google's public keys — never trust client-decoded claims.
- Extract `sub` (Google user ID) and verified email from the token.
- Look up or create a `parent`/`auth_identifier` record keyed on the Google `sub` (or verified email, matching whichever lookup strategy B-02's `AuthIdentifierRepository` already established — reuse it, do not create a parallel identity table).
- If the matched family is soft-deleted, route to reactivation flow instead of treating as new registration.
- Delegate to the shared session-issuance helper for token minting and `next_step` determination.

## 11. API Contract

### `POST /v1/identity/auth/google`
- Auth: Google ID token in body. Request: `{id_token, device_id}`. Response 200: identical shape to `/otp/verify` success — `{access_token, refresh_token, is_new_family, next_step}`. Errors: `401 INVALID_GOOGLE_TOKEN`.

## 12. Database Requirements
No new tables. Reuses `auth_identifier` (B-02) with `identifier_type = "google"` and `identifier_value_hash` derived from the Google `sub`. Reuses `parent`, `family` from the existing `identity` schema.

## 13. Validation
- `id_token` must be present and non-empty.
- Reject tokens whose audience does not match the configured Google OAuth client ID.

## 14. Authentication
Pre-auth endpoint — the Google ID token itself is the credential being verified.

## 15. Authorization
N/A — session issuance only, same as B-02.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| Invalid token signature/audience/issuer | `401 INVALID_GOOGLE_TOKEN` |
| Google verification API timeout/outage | `503`, non-blocking client error, never expose raw Google error text |
| Account linked to soft-deleted family | Route to reactivation flow, not fresh registration; escalate to Support if retention window lapsed |

## 17. Security
- Server-side signature/audience/issuer verification only — client-decoded JWT claims are never trusted for identity assertions.
- Same refresh-token binding/rotation rules as B-02.

## 18. Analytics
Emit `login_started` with `method=google` via `OutboxWriter`; downstream `onboarding_completed`/consent events are shared with B-02's taxonomy.

## 19. Performance
Google token verification typically network-bound (call to Google's public key endpoint or cached JWKS) — cache Google's public keys with standard JWKS cache-control headers to avoid a network round-trip on every login.

## 20. Library Requirements
- `google-auth` (Python) for ID token verification — do not hand-roll JWT signature verification for this.

## 21. Testing
- Unit: audience mismatch rejection, issuer mismatch rejection, expired-token rejection.
- Integration: new-user Google login → consent-required next_step; returning-user Google login → profile_picker; soft-deleted-family login → reactivation flow.

## 22. Documentation
Document `GOOGLE_OAUTH_CLIENT_ID` env var name in module README.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Implement `GoogleOAuthVerifier`**
Objective: Server-side Google ID token verification. Why: FR-6/security requirement — never trust client claims. Follow: `infrastructure/` service pattern. Create: `google_oauth_verifier.py`. Implementation: use `google-auth` library's `verify_oauth2_token`, check audience against configured client ID. Security: reject on any verification exception, never partially trust a token. Tests: mismatched audience/issuer/expired cases (mocked). Definition of Done: verifier rejects all three tampering scenarios in tests.

**Task 02 — Add `authenticate_via_google()` to IdentityService**
Objective: Bridge verified Google identity to the shared session-issuance helper from B-02. Why: guarantees identical downstream behavior to OTP path. Reuse: B-02's shared helper (do not duplicate next_step logic). Business Rules: soft-deleted family → reactivation flow, not fresh registration. Tests: new/returning/reactivation branches. Dependencies: B-02 Task 07. Definition of Done: all three branches tested.

**Task 03 — Add Router Endpoint**
Objective: Wire `POST /v1/identity/auth/google`. Follow: existing router conventions, no DB access in router. Definition of Done: endpoint live, documented, returns `TokenResponse`-shaped body.

**Task 04 — Add Unit & Integration Tests**
Objective: Full coverage per §21. Definition of Done: all cases green in CI.

**Task 05 — Update OpenAPI Documentation**
Objective: Regenerate schema, confirm non-breaking diff. Definition of Done: diff classifier passes.

**Task 06 — Final Code Review**
Objective: Confirm no parallel/duplicate identity or token-issuance logic was introduced. Definition of Done: checklist in §24 checked.

## 24. Final Verification Checklist
- [x] Signature/audience/issuer verified server-side via `google-auth`, never client claims
- [x] Apple Login not implemented anywhere in this change
- [x] Session issuance reuses B-02's shared helper (no duplicated next_step logic)
- [x] Soft-deleted family routes to reactivation, not fresh registration
- [x] `GOOGLE_OAUTH_CLIENT_ID` referenced by name only, no secret committed
- [x] Unit + integration tests green (26/26 tests passing)

## 25. Definition of Done
`POST /v1/identity/auth/google` is live, verifies tokens server-side, and produces token/next-step responses indistinguishable in shape from B-02's OTP path, ready for K-04 (KMP Google Sign-In flow) to integrate against.
