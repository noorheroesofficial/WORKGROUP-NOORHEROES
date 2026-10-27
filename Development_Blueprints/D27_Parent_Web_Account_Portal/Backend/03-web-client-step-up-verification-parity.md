# B-03 — Web Client Step-Up Verification Parity

## 1. Feature Context
Part of Feature D.27 — Parent Web Account Portal. FR-3 requires that every sensitive web-portal action (billing, consent, export, deletion, device-revoke) be gated behind fresh step-up verification, with security assurance equivalent to the Mobile App's PIN/biometric gate — but using a web-appropriate credential (OTP/password/passkey) instead of a PIN prompt. Investigation of the actual server-side step-up mechanism surfaces a genuine, previously unflagged architecture gap that this sub-feature must resolve, not silently assume away.

## 2. Parent Feature
D.27 Parent Web Account Portal (`account.noorheroes.com`)

## 3. Sub-feature
**B-03 — Web Client Step-Up Verification Parity**

## 4. Objective
Determine and implement how a web-portal step-up action (OTP/password/passkey re-verification) produces the exact same server-side elevation guarantee — the short-lived, hard-TTL "Parent Gate verified" marker consumed by `require_elevated_session` — that the Mobile App's `POST /v1/auth/pin/verify` (C.19 B-03) already produces, without introducing a server-side fast-path or weakening the freshness guarantee for either client type.

## 5. Business Requirements
- FR-3: sensitive web actions require recent OTP/password/passkey or equivalent step-up authentication — "the web-surface equivalent of C.19's mobile step-up gate."
- NFR "Step-Up Parity": "The web portal's step-up mechanism... provides equivalent security assurance to the mobile app's PIN/biometric gate for the same class of sensitive actions."
- §5 Backend AI Code-Generation Prompt, item 4: "Ensure step-up verification calls made by this client work correctly against the EXISTING step-up service without any web-specific modification to that service's own logic — write an integration test confirming a step-up flow initiated from a request bearing the web portal's origin/client-type metadata behaves identically (in terms of freshness/expiry rules) to one initiated from the mobile app."
- C.19 B-03's own hard rule, inherited here unchanged: **zero server-side fast-path, for any trigger context, ever** — this sub-feature must not create an exception to that rule for the web client type.

## 6. Existing Architecture — Investigated, Gap Found
The PRD assumes a generic "step-up service (C.19)" exists that the web portal can call directly with a different credential type. Investigation of C.19 B-03 ("Parent Profile Gate Verification API") shows the actual, only implemented step-up endpoint is `POST /v1/auth/pin/verify`, which:
1. Verifies a **PIN** (Argon2id hash comparison against `parent_pin`, A.1 B-04's table) — there is no OTP-based or passkey-based re-verification endpoint anywhere in the reviewed backend that produces the same elevation marker.
2. On success, sets the short-lived Parent-Gate-verified session marker (Redis key `parent_gate:{parent_id}:{device_id}`, hard server-side TTL) that `require_elevated_session` (`core/deps.py`) consults.

The PRD's own text acknowledges the credential type differs ("OTP/password/passkey re-verification rather than the mobile app's PIN/biometric") but does not identify that **no endpoint currently exists** to produce this marker via OTP. A.1 B-02 ("Parent Registration & OTP Authentication API") issues OTP for initial login/registration only — it is not documented as setting the `parent_gate` elevation marker, and doing so implicitly would blur "logging in" with "stepping up," which is a meaningfully different security event.

**This is a genuine architecture gap, flagged per rule 24/30, not silently resolved:**

```
Existing Architecture
   → POST /v1/auth/pin/verify (C.19 B-03) sets parent_gate marker via PIN comparison
   → No equivalent OTP/password/passkey-based endpoint exists
        ↓
Problem
   → D.27's web portal has no PIN to verify (parents are not expected to
     re-enter a mobile-app PIN in a browser context per the PRD's own
     framing), yet every sensitive web action requires the same elevation
     marker `require_elevated_session` checks
        ↓
Proposed Improvement (two options, requires product/architecture decision — Task 01)
   Option A: Extend PinService with a parallel `verify_via_otp()` path — a
     dedicated `POST /v1/auth/step-up/otp/verify` endpoint that re-sends
     and re-verifies a short OTP challenge (reusing A.1 B-02's existing OTP
     issuance/hashing/lockout infrastructure), and on success sets the
     identical `parent_gate:{parent_id}:{device_id}` marker via the same
     code path C.19 B-03 uses — client-type/credential-type is metadata
     only, never a fast-path.
   Option B: Treat "passkey" as the primary long-term web credential
     (WebAuthn), with OTP as the fallback; this requires new passkey
     enrollment/verification infrastructure not present anywhere in the
     reviewed codebase, a materially larger scope than Option A.
        ↓
Impact
   → Option A reuses ~90% of existing infrastructure (OTP issuance,
     hashing, lockout, marker-setting code path) with one new endpoint and
     one new schema; Option B is a net-new credential system.
        ↓
Implementation (this blueprint proceeds on Option A as the
   recommended, lower-risk path per rule 30's reuse-first principle;
   Task 01 requires written confirmation before Task 02 proceeds)
        ↓
Documentation Update
   → C.19's blueprint set should be cross-referenced/updated once this
     decision is made, since the elevation-marker-issuance responsibility
     becomes shared between C.19 B-03 (PIN path) and this sub-feature
     (OTP path) rather than owned solely by C.19.
```

## 7. Existing Code to Reuse
- `core/deps.py::require_elevated_session` — consumed unchanged; this sub-feature's entire purpose is to produce the marker it already checks, not to modify it.
- `modules/identity/pin_service.py::PinService.verify()` (C.19 B-03) — the exact marker-setting code path (Redis key format, TTL, no-fast-path logic) is reused/mirrored, not reimplemented from scratch.
- A.1 B-02's OTP issuance/hashing/lockout infrastructure (`otp_service.py`, `otp_hasher.py` per B-02's file layout) — reused for the step-up OTP challenge itself, avoiding a second OTP implementation.
- `core/exceptions.py::AuthorizationError`, `RateLimitExceededError`.

## 8. Files to Create
- `src/noorheroes/modules/identity/step_up_schemas.py` — `StepUpOtpRequest`, `StepUpOtpVerifyRequest`, `StepUpVerifyResponse`
- `tests/modules/identity/test_step_up_otp_service.py`
- `tests/modules/identity/test_step_up_marker_parity.py`

## 9. Files to Modify
- `src/noorheroes/modules/identity/pin_service.py` — extract the marker-setting logic from `PinService.verify()` (C.19 B-03) into a shared helper (e.g. `elevate_parent_gate(parent_id, device_id)`) callable from both the PIN path and the new OTP step-up path, so the two never drift.
- `src/noorheroes/modules/identity/service.py` (or a new `step_up_service.py`) — add `StepUpService.request_otp_challenge(parent_ctx)` and `StepUpService.verify_otp_challenge(parent_ctx, code)`, reusing A.1 B-02's OTP primitives.
- `src/noorheroes/modules/identity/api.py` — add `POST /v1/auth/step-up/otp/request`, `POST /v1/auth/step-up/otp/verify`.

## 10. Backend Requirements
- `StepUpService.request_otp_challenge(parent_ctx)`: issues a short-lived OTP via the existing A.1 B-02 mechanism, tagged as a step-up challenge (distinct purpose/audience claim from a login OTP, so a leaked login OTP cannot be replayed as a step-up pass, and vice versa).
- `StepUpService.verify_otp_challenge(parent_ctx, code)`:
  1. Verify the OTP via the existing hashing/comparison logic (A.1 B-02's pattern).
  2. Honor lockout unconditionally (mirrors C.19 B-03 — correct code during active lockout still fails).
  3. **Zero fast-path** — every call performs a genuine check, regardless of client origin metadata (`client_surface: web_portal`), mirroring C.19 B-03's explicit "no `trigger_context` value causes a skipped or cached verification" rule, extended to "no `client_surface` value" either.
  4. On success, call the shared `elevate_parent_gate(parent_id, device_id)` helper — issuing the identical Redis marker/TTL that C.19 B-03's PIN path issues. `device_id` for a web session is the browser/session identifier established at login (B-01/N-03), not a mobile device ID.
  5. On failure, standard lockout/retry behavior identical to A.1 B-02.
- The shared `elevate_parent_gate()` helper must be the **only** code path either verification method (PIN or OTP) is permitted to call to set the marker — enforced by code review and by Task 06's parity test, so the two paths cannot silently diverge in TTL or marker format over time.

## 11. API Contract

### `POST /v1/auth/step-up/otp/request`
- **Auth:** Bearer (parent)
- **Response 200:** `{ "challenge_sent": true }`
- **Error Responses:** `429 RATE_LIMIT_EXCEEDED` (existing OTP rate-limit pattern, reused)

### `POST /v1/auth/step-up/otp/verify`
- **Auth:** Bearer (parent)
- **Request:** `{ "code": "..." }`
- **Response 200:** `{ "verified": true, "grace_window_started_at": "..." }` (shape mirrors C.19 B-03's `PinVerifyResponse` for frontend-handling consistency) or `{ "verified": false, "attempts_remaining": N }`
- **Error Responses:** `401 UNAUTHORIZED`, `423 LOCKED_RETRY_COOLDOWN`

## 12. Database Requirements
No new PostgreSQL table — reuses A.1 B-02's existing OTP storage/hashing table (exact name to be confirmed from B-02's blueprint) with a `purpose` or `audience` discriminator column added if not already present, distinguishing "login" OTPs from "step-up" OTPs so one cannot be replayed as the other. Reuses the existing `parent_gate:{parent_id}:{device_id}` Redis marker namespace unchanged (C.19 B-03).

## 13. Validation
`code` must match the existing OTP format validation (A.1 B-02's pattern, e.g. 6-digit numeric) before hash comparison is attempted.

## 14. Authentication
`Depends(get_current_parent)` on both endpoints — a parent must already hold a valid Bearer session before requesting or verifying a step-up challenge; step-up elevates an existing session, it does not authenticate a new one.

## 15. Authorization
Self-only — `parent_id` always derived from the bearer token, never from the request body, mirroring C.19 B-03's explicit rule.

## 16. Error Handling
| Scenario | Response |
|---|---|
| Wrong OTP code | `200 {verified: false, attempts_remaining}` |
| Correct code during active lockout | `423 LOCKED_RETRY_COOLDOWN` |
| OTP request rate-limit exceeded | `429`, existing pattern |
| Step-up requested without a valid parent session | `401` |

## 17. Offline First
Not applicable — step-up is inherently online-only for both mobile and web clients.

## 18. Local Data
Not applicable (backend).

## 19. Localization
Not applicable (backend) — OTP delivery message localization is owned by A.1 B-02's existing notification pipeline, reused unchanged.

## 20. RTL
Not applicable (backend).

## 21. Analytics
Backing source for the web portal's `web_step_up_required_shown`, `web_step_up_succeeded`, `web_step_up_failed` events (§1.19); `client_surface: web_portal` recorded server-side for B-04's audit trail, for observability only — never for branching verification logic.

## 22. Performance
Mirrors C.19 B-03's p95 < 150ms target for the verify call; OTP request/verify is on the critical path of every sensitive web action, so no redundant round-trips beyond the two calls (request, verify) already required by the OTP pattern itself.

## 23. Security
- **Zero fast-path, for any `client_surface` value, is the entire point of this sub-feature** — directly inherits C.19 B-03's "highest-priority test" framing.
- Step-up OTPs must be purpose-scoped (distinct from login OTPs) so a captured login OTP cannot be replayed to elevate an already-authenticated session, and vice versa.
- The shared `elevate_parent_gate()` helper is the single point of control for marker issuance — auditable, testable in one place, and structurally prevents the PIN and OTP paths from silently diverging in TTL or format.
- This endpoint's existence and correctness is the precondition for every one of B-01's step-up-gated allowlist entries (billing cancel, consent withdraw, export request, deletion request, device revoke) to be genuinely secure rather than trivially bypassable.

## 24. Library Requirements
Reuses A.1 B-02's existing OTP library/infrastructure (SMS/email delivery provider, hashing) — no new library introduced.

## 25. Testing
- Unit: step-up OTP verify performs a genuine check on every call, regardless of `client_surface` metadata — no fast-path (mirrors C.19 B-03 Task 04's highest-priority test).
- Unit: correct code during active lockout is still rejected.
- Integration: successful step-up OTP verify sets a `parent_gate` marker that is byte-for-byte structurally identical (same Redis key format, same TTL policy) to the one C.19 B-03's PIN verify sets — the core parity test for this entire sub-feature (§5's cited requirement).
- Integration: a login-purpose OTP cannot be replayed against the step-up verify endpoint, and vice versa (purpose-scoping test).
- Integration: `parent_id` cannot be spoofed via request body.
- Regression: any future change to C.19 B-03's marker format/TTL must fail this sub-feature's parity test until mirrored here too (structural coupling made visible via a shared test fixture).

## 26. Documentation
OpenAPI must state explicitly that this endpoint produces the identical elevation guarantee as C.19 B-03's PIN verification, and that `client_surface`/`trigger_context` metadata is audit-only and never alters verification behavior. Cross-reference C.19 B-03 and this file from each other once both exist.

## 27. AI Coding Agent Implementation Steps

**Task 01 — Confirm the Step-Up Architecture Decision (blocking)**
- **Objective:** Obtain written product/architecture confirmation of Option A (extend OTP infrastructure with a step-up-purpose endpoint) versus Option B (passkey/WebAuthn) versus any other approach, per §6.
- **Why This Is Required:** The PRD assumes an OTP-based step-up mechanism exists; it does not. Building against an assumed mechanism would violate rule 30.
- **Definition of Done:** Written confirmation obtained; this blocks all subsequent tasks.

**Task 02 — Extract Shared `elevate_parent_gate()` Helper**
- **Files to Modify:** `pin_service.py` (C.19 B-03).
- **Objective:** Isolate the marker-setting logic so both PIN and OTP step-up paths call one function, never two divergent implementations.
- **Dependencies:** Task 01; coordinate as a cross-feature change with C.19's owning team since this modifies C.19 B-03's existing file.

**Task 03 — Add OTP Purpose/Audience Discriminator**
- **Files to Modify:** A.1 B-02's OTP model/schema (exact file per that blueprint).
- **Objective:** Distinguish login-purpose from step-up-purpose OTPs so one cannot be replayed as the other.

**Task 04 — Implement `StepUpService`**
- **Files to Create/Modify:** `step_up_service.py` or extend `service.py`.
- **Implementation Details:** `request_otp_challenge()`, `verify_otp_challenge()` per §10.
- **Dependencies:** Tasks 02, 03.

**Task 05 — Implement Router Endpoints**
- **Files to Modify:** `api.py`.
- **Implementation Details:** `POST /v1/auth/step-up/otp/request`, `POST /v1/auth/step-up/otp/verify`.

**Task 06 — Write the Marker-Parity Test (highest priority)**
- **Files to Create:** `test_step_up_marker_parity.py`.
- **Definition of Done:** Proves the OTP path's marker is structurally identical to the PIN path's marker.

**Task 07 — Write No-Fast-Path and Purpose-Scoping Tests**
- **Files to Create:** `test_step_up_otp_service.py`.

**Task 08 — Documentation & Cross-Reference**
- **Definition of Done:** OpenAPI updated; C.19 B-03 cross-referenced.

## 28. Definition of Done
A web-originated OTP re-verification produces the exact same, independently-audited elevation guarantee as the Mobile App's PIN verification — same marker format, same hard TTL, same zero-fast-path rule — with the underlying architecture gap (no prior OTP-based step-up endpoint) explicitly resolved via written decision (Task 01) rather than silently assumed.

## 29. Final Verification Checklist
- [ ] Task 01's architecture decision obtained and documented before implementation began
- [ ] `elevate_parent_gate()` shared helper used by both PIN (C.19 B-03) and OTP (this sub-feature) paths — no divergent implementation
- [ ] Marker-parity test passes (identical Redis key format/TTL across both paths)
- [ ] No fast-path exists for any `client_surface` or `trigger_context` value
- [ ] Login-purpose and step-up-purpose OTPs cannot be cross-replayed
- [ ] `parent_id` always derived from bearer token
- [ ] No PostgreSQL/Redis credential changes
