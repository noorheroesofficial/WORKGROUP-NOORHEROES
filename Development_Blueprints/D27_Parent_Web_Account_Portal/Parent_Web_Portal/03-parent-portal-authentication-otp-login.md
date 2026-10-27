# N-03 — Parent Web Portal Authentication & OTP Login

## 1. Feature Context
Part of Feature D.27 — Parent Web Account Portal. The entry point to the entire portal: a parent already registered on the Mobile App logs into `account.noorheroes.com` using the same phone/email OTP identity established by A.1 — with an unrecognized device/browser always requiring full OTP, never silently trusted.

## 2. Parent Feature
D.27 Parent Web Account Portal (`account.noorheroes.com`)

## 3. Sub-feature
**N-03 — Parent Web Portal Authentication & OTP Login**

## 4. Objective
Build the Login/OTP screen against A.1's existing, already-hardened OTP identity service, correctly handling the returning-parent (not new-registration) path, and correctly wiring N-02's `SessionContext` on success.

## 5. Business Requirements
- FR-1: Login/OTP is screen #1 of the 8 canonical screens.
- §1.9 Acceptance Criteria: "Given a parent visits `account.noorheroes.com`, when they log in via phone/email OTP, then they reach the portal's account home, never the Mobile App's Parent Dashboard or any child data."
- Edge Case 1: "A parent logs into the web portal on a device/browser that has never been seen before → treated as a new session requiring full OTP verification, not silently trusted based on any mobile-app-side device trust."
- §1.19 Events: `web_portal_login_attempted`, `web_portal_login_succeeded`, `web_portal_login_failed_unrecognized_device`.

## 6. Existing Architecture — Investigated, Two Gaps Found
Investigation of A.1 B-02 ("Parent Registration & OTP Authentication API") surfaces two discrepancies between the PRD's assumed contract and the actual implementation, both flagged rather than silently resolved:

1. **Path mismatch.** PRD §3.4 lists `POST /v1/auth/otp/request` / `POST /v1/auth/otp/verify`. A.1 B-02's actual, implemented routes are `POST /v1/identity/auth/otp/request` / `POST /v1/identity/auth/otp/verify` (mounted under `IdentityRouter`, prefixed `/v1/identity/...` per `FAST-API-INSTRUCTIONS.md` §6). B-01's allowlist entry (and this screen's `apiClient` function) must target the **actual** `/v1/identity/auth/otp/*` paths, not the PRD's shorthand. This must be corrected in B-01's allowlist configuration as a follow-up.
2. **Register vs. login semantics.** A.1 B-02's documented flow (`POST /v1/identity/auth/register` → `POST /v1/identity/auth/otp/request` → `POST /v1/identity/auth/otp/verify`) is framed around **new registration**, distinguishing new vs. returning users only *after* OTP verification (`is_new_family`/`next_step` in the verify response) — there is no separately named "login" endpoint in the reviewed A.1 blueprint. It is not yet confirmed whether an already-registered parent visiting the web portal is expected to call the same `register` → `otp/request` → `otp/verify` sequence (with the service's existing enumeration-safe/idempotent handling of an already-existing identifier), or whether a distinct login-only entry point is expected. This is flagged for Task 01 rather than assumed.

## 7. Existing Code to Reuse
- A.1 B-02's `OtpAuthService` (`register()`, `request_otp()`, `verify_otp()`) — called via N-02's `apiClient`, zero modification to the service itself.
- N-02's `apiClient`, `SessionContext`, `PortalShell`.
- The same enumeration-safe, timing-attack-resistant behavior A.1 B-02 already guarantees (identical response shape/latency regardless of whether the identifier exists) — this sub-feature adds no new logic here, it is a pure consumer.

## 8. Files to Create
- `noorheroes-account-portal/src/app/(portal)/login/page.tsx`
- `noorheroes-account-portal/src/features/auth/api/auth-client.ts` — `requestOtp()`, `verifyOtp()` named functions only.
- `noorheroes-account-portal/src/features/auth/components/otp-input.tsx`
- `noorheroes-account-portal/src/features/auth/hooks/use-login-flow.ts`
- `noorheroes-account-portal/tests/features/auth/login-flow.test.tsx`

## 9. Files to Modify
- N-02's `allowed-endpoints.ts` — register the (path-corrected, per §6) OTP request/verify endpoints.
- N-02's `session-context.tsx` — wire population of `SessionContext` on successful `verify_otp`.

## 10. Backend Requirements
Consumes A.1 B-02 exclusively (`POST /v1/identity/auth/otp/request`, `POST /v1/identity/auth/otp/verify`, and — pending Task 01's resolution — possibly `POST /v1/identity/auth/register`), no new backend logic.

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- Login screen: identifier input (phone/email), OTP request trigger, 6-digit OTP input with paste/auto-submit support (mirroring the Mobile App's UX per the Dual-User Design Rule), resend countdown sourced from the server's authoritative `resend_available_at` (never a client-only timer, consistent with A.1 B-02's server-authoritative cooldown).
- On successful verify: populate `SessionContext`, redirect to Portal Account Home — never to any child-data or dashboard route (Acceptance Criteria).
- Unrecognized device/browser: no special client-side handling needed beyond calling the existing endpoints — the server-side "always full OTP, no silent trust" guarantee (A.1's existing behavior) is sufficient; this screen must not attempt to cache or bypass OTP based on any local storage flag (would violate Edge Case 1 and N-02's Zero Token Persistence principle).
- Loading state during OTP request/verify; error state for invalid/expired OTP, lockout (`423`), and provider-unavailable (`503`, offering the fallback channel per A.1 B-02's existing pattern).
- Fire `web_portal_login_attempted` on submit, `web_portal_login_succeeded` on verify success, `web_portal_login_failed_unrecognized_device` is server-observed (B-04) rather than a distinct client-fireable event in most cases — confirm exact client-vs-server firing split against A.1's analytics conventions.

## 13. API Contract
Consumes A.1 B-02's contract as documented in that blueprint, at the corrected `/v1/identity/auth/otp/*` paths per §6.

## 14. Database Requirements
Not applicable (frontend).

## 15. Validation
Client-side format validation only (identifier shape, 6-digit OTP shape) as a UX convenience — all authoritative validation happens server-side per A.1 B-02.

## 16. Authentication
This screen *is* the authentication entry point — no prior session required to reach it.

## 17. Authorization
Not applicable — pre-authentication screen.

## 18. Error Handling
| Scenario | UI Behavior |
|---|---|
| Invalid/expired OTP | Inline error, remaining-attempts messaging if provided by the API |
| Lockout (`423`) | Clear cooldown messaging, matching A.1's existing UX pattern |
| OTP provider unavailable (`503`) | Offer fallback channel (SMS↔email), per A.1 B-02's existing behavior |
| Missing required consents | Not applicable to login (consents are captured at A.1 registration time, not re-collected here) — confirm this assumption in Task 01 alongside the register-vs-login question |

## 19. Offline First
Not applicable — login requires connectivity.

## 20. Local Data
No OTP code, token, or identifier persisted in browser storage; `SessionContext` (in-memory) is populated only after successful verification, consistent with N-02's Zero Token Persistence principle.

## 21. Localization
Full EN/HI/AR/UR localization of all login screen copy; RTL layout for Arabic/Urdu.

## 22. RTL
Full RTL layout, including OTP input direction (numeric input remains LTR-read within an RTL page shell, consistent with standard RTL numeric-field conventions).

## 23. Analytics
`web_portal_login_attempted`, `web_portal_login_succeeded`, `web_portal_login_failed_unrecognized_device` (§1.19), all tagged `client_surface: web_portal` via N-02's analytics wrapper.

## 24. Performance
p95 page load < 1.5s (§1.8); OTP request/verify latency is bounded by A.1 B-02's existing backend performance, not this sub-feature's concern.

## 25. Security
- Relies entirely on A.1 B-02's existing enumeration-safe, timing-attack-resistant, rate-limited implementation — this sub-feature introduces no new security logic, only a consuming UI.
- No silent device-trust bypass — every login is a full OTP verification, matching Edge Case 1's explicit requirement.
- Zero Token Persistence in Browser Storage (N-02's principle) applies from the moment of successful verification onward.

## 26. Library Requirements
No new libraries beyond N-02's established stack (React Query, Zod).

## 27. Testing
- Integration: full login flow (request → verify → redirect to Account Home) against A.1 B-02's contract (mocked/staged).
- Integration: invalid OTP shows inline error without granting session.
- Integration: lockout and provider-unavailable states handled per A.1's existing response shapes.
- Integration: successful login never redirects anywhere other than Portal Account Home (Acceptance Criteria negative-path test: confirm no redirect target could ever resolve to a child-data route).
- Unit: resend countdown is driven by server `resend_available_at`, not a client-only timer that could drift or be manipulated.

## 28. Documentation
Document the Task 01 register-vs-login and path-correction findings prominently in this feature's README so a future maintainer does not assume the PRD's literal `/v1/auth/otp/*` paths are correct.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Resolve Register-vs-Login Semantics and Path Correction (blocking)**
- **Objective:** Confirm whether returning parents call the same `register` → `otp/request` → `otp/verify` sequence as new registrants (relying on A.1 B-02's existing idempotent/enumeration-safe handling), or a distinct login-only endpoint is required; confirm the correct `/v1/identity/auth/otp/*` paths are used everywhere (this file, B-01's allowlist).
- **Why This Is Required:** Per §6, the PRD's assumed contract does not match A.1 B-02's actual implementation in two ways.
- **Definition of Done:** Written confirmation obtained; blocks Task 02.

**Task 02 — Build `auth-client.ts`**
- **Files to Create:** `auth-client.ts`.
- **Dependencies:** Task 01.

**Task 03 — Build Login Screen & OTP Input**
- **Files to Create:** `page.tsx`, `otp-input.tsx`, `use-login-flow.ts`.

**Task 04 — Wire `SessionContext` Population**
- **Files to Modify:** `session-context.tsx`.

**Task 05 — Error/Loading States**

**Task 06 — Localization, RTL, Analytics Wiring**

**Task 07 — Full Test Suite**

**Task 08 — Update B-01's Allowlist Path Correction**
- **Objective:** Ensure the gateway/middleware allowlist reflects the corrected `/v1/identity/auth/otp/*` paths, not the PRD's shorthand.

## 30. Definition of Done
A parent can log into the web portal using the identical, already-hardened A.1 OTP identity service, with unrecognized devices always requiring full verification, session state held only in memory, and redirect always landing on Portal Account Home — with the two flagged contract discrepancies (path, register-vs-login semantics) resolved in writing before implementation.

## 31. Final Verification Checklist
- [ ] Task 01's register-vs-login and path-correction questions resolved in writing
- [ ] Correct `/v1/identity/auth/otp/*` paths used in this screen's `apiClient` calls and in B-01's allowlist
- [ ] No silent device-trust bypass — every login requires full OTP
- [ ] Session state held only in memory (no browser storage persistence)
- [ ] Successful login always redirects to Portal Account Home, never a child-data route
- [ ] Full localization and RTL verified
