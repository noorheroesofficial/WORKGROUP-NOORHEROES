# B-01 — Web Portal CORS & Origin Allowlist Configuration

## 1. Feature Context
Part of Feature D.27 — Parent Web Account Portal (`account.noorheroes.com`). D.27 introduces **zero new backend business logic**; it is a second, narrower frontend client authenticating and operating against services already specified by A.1, C.19/C.23, C.21, C.24, C.25, and C.26. This sub-feature is the single highest-priority backend deliverable in the entire document: the API Gateway configuration that permits `account.noorheroes.com` to call an explicit, narrow allowlist of existing endpoints — and structurally rejects everything else, especially `POST /api/v1/billing/subscribe` (store-policy compliance, zero-tolerance) and any child-scoped route.

## 2. Parent Feature
D.27 Parent Web Account Portal (`account.noorheroes.com`)

## 3. Sub-feature
**B-01 — Web Portal CORS & Origin Allowlist Configuration**

## 4. Objective
Configure the API Gateway's CORS policy so that `https://account.noorheroes.com` (and its staging equivalent) is accepted as a valid cross-origin caller **only** for the explicit endpoint allowlist enumerated in PRD §3.4, with every other route — most critically the billing purchase-initiation endpoint and all child-scoped routes — rejected at the gateway layer regardless of the request's own credential validity.

## 5. Business Requirements
- FR-2: the web portal must never be able to initiate an app-store purchase; `POST /api/v1/billing/subscribe` must be unreachable from this origin (store-policy compliance, zero-exception rule).
- FR-4/FR-5: child progress, reports, AI history, screen-time controls, child selectors, and any child-level delete/disable action are structurally absent — not merely hidden in the UI. `GET /v1/parent/dashboard` and all `GET /v1/children/*` routes must be unreachable from this origin.
- NFR "Structural Scope Exclusion": the guarantee must be enforced independently of the frontend's own restraint (defense in depth, paired with N-02's frontend-level `apiClient` scope restriction).
- §3.5 Cross-Cutting API Concerns: CORS/origin allowlisting is this document's stated sole backend contribution.
- §12.9 Security Checklist: "Gateway-level CORS/route allowlist verified to reject every out-of-scope route, including purchase-initiation" is the first pre-launch gate.

## 6. Existing Architecture
No existing per-client-origin CORS allowlist pattern is described in `FAST-API-INSTRUCTIONS.md` — the reviewed architecture manual documents authentication (`get_current_parent`/`get_current_admin`), RBAC scopes (`require_admin_scope`), and rate limiting (`RateLimitMiddleware`), but no origin-scoped route allowlist. **This is confirmed as new gateway configuration, not a reuse of an existing mechanism** — consistent with the PRD's own framing ("the only backend-adjacent work this document specifies"). It sits in front of, not inside, the 10 existing bounded-context routers (`identity`, `access_gate`/`admin`, `content`, `learning`, `localization`, `media`, `notifications`, `rewards`, `subscriptions`, plus C.26's `data_rights` context once built) — this sub-feature adds no code to any of those modules.

**Flagged, not guessed:** the PRD's API List (§3.4) references `GET /v1/sessions` / `DELETE /v1/sessions/{id}` as "C.19's exact session-list/revocation contract." Investigation of the reviewed blueprints (C.23 Backend B-06 — Active Device Sessions & Revocation API) shows this contract is actually owned by C.23 (built on top of C.19 B-04's session-activation primitive) and is scoped to **child-mode device sessions across a family's children**, not a parent's own browser/login sessions. Whether D.27's "Devices and Sessions" screen (N-05) is intended to reuse this exact child-mode-session contract, or requires a distinct parent-account-session list that does not yet exist in the reviewed codebase, is an open scope question carried into N-05 and must be resolved before this allowlist entry is finalized as pointing at `GET/DELETE /v1/sessions`.

**Path corrections found during N-03/N-04/N-07/N-10's screen-level investigation (applied below, §10 is now the corrected version of this allowlist, superseding the PRD's §3.4 shorthand):**
- OTP: the PRD's `POST /v1/auth/otp/request` / `POST /v1/auth/otp/verify` do not exist at that path. A.1 B-02 actually mounts these under `IdentityRouter` at `POST /v1/identity/auth/otp/request` / `POST /v1/identity/auth/otp/verify` (confirmed against A.1 B-02 §8/§10 directly, N-03 §6).
- Consent: the PRD's `PATCH /v1/parent/consents` does not exist. C.26 B-01 implements `GET /v1/parent/consents` (read) and `POST /v1/parent/consents/{id}/withdraw` (the only write path) — no PATCH endpoint anywhere in that blueprint (N-07 §6).
- FAQ: the PRD's bare `GET /v1/support/faq` is the search endpoint with a required `q` query param (`GET /v1/support/faq?q=`), and article detail is a separate route `GET /v1/support/faq/{id}` — both must be allowlisted individually, not one path (N-10 §6, C.25 B-03).
- PIN/password reset: the PRD's FR-6 ("password/PIN reset, the same underlying credential as the mobile app's Parent PIN") maps to A.1 B-04's `POST /v1/identity/auth/pin` (reset path, `require_elevated_session`-gated) — this endpoint was not named by path anywhere in the PRD's §3.4 list at all and must be added to the allowlist (N-04 §6/Task 01).

## 7. Existing Code to Reuse
- API Gateway configuration layer (external to the FastAPI app itself — confirm the actual gateway product/config format in use, e.g. an API Gateway service, Kong, or a reverse-proxy layer in front of the FastAPI app; `FAST-API-INSTRUCTIONS.md` does not document this layer, so its exact location must be confirmed against actual infrastructure/DevOps configuration before implementation, per rule 30).
- `src/noorheroes/infrastructure/middleware/rate_limit.py`'s `RateLimitMiddleware` pattern — as a structural reference for how existing app-level middleware is registered, in case CORS/origin enforcement is implemented as FastAPI middleware rather than (or in addition to) gateway-layer config.
- `src/noorheroes/core/exceptions.py::AuthorizationError` — reused as the exception type for an in-app enforcement layer, if applicable.

## 8. Files to Create
- Gateway/infrastructure CORS configuration artifact (exact file/location to be confirmed against the actual deployed gateway product — do not invent a path; e.g. if Kong, a declarative config YAML; if a reverse proxy, its config block; if enforced in-app, a new `src/noorheroes/infrastructure/middleware/web_portal_origin.py`).
- `tests/infrastructure/test_web_portal_cors_allowlist.py`
- `tests/infrastructure/test_web_portal_billing_subscribe_rejection.py`

## 9. Files to Modify
- Gateway/infrastructure deployment configuration (staging + production) to add the `account.noorheroes.com` origin entry.
- `main.py` — only if CORS is (also) enforced in-app via FastAPI's `CORSMiddleware` as a second layer; confirm whether the platform already registers `CORSMiddleware` for the existing `noorheroes-admin` origin, and extend rather than duplicate that registration.

## 10. Backend Requirements
- Define the explicit allowlist for the `account.noorheroes.com` origin, scoped to exactly (**corrected paths, superseding PRD §3.4's shorthand — see §6**):
  - `POST /v1/identity/auth/otp/request`, `POST /v1/identity/auth/otp/verify` (A.1 B-02 — corrected path, not `/v1/auth/otp/*`)
  - `POST /v1/identity/auth/pin` (A.1 B-04, reset path, `require_elevated_session`-gated — added; absent from the PRD's own §3.4 list by name, see N-04 §6/Task 01)
  - Step-up OTP endpoint(s) (**B-03, net-new**: `POST /v1/auth/step-up/otp/request`, `POST /v1/auth/step-up/otp/verify` — pending B-03 Task 01's architecture confirmation)
  - `GET /v1/sessions`, `DELETE /v1/sessions/{id}` (C.23 B-06 — **BLOCKED, pending scope resolution per §6/N-05 Task 01; do not finalize this entry until resolved**)
  - `POST /v1/parent/deletion-request`, `GET /v1/parent/deletion-status` (**BLOCKED, existence as family-level routes unconfirmed — see N-09 Task 01, shared with C.26 K-07's identical open question; C.21's reviewed blueprints implement only per-child deletion**)
  - `GET /v1/parent/subscription`, `POST /v1/parent/subscription/cancel`, `GET /v1/parent/subscription/invoices/{invoice_id}` (C.24 B-05 — confirmed correct; `POST /v1/parent/subscription/restore` exists on this same router but is deliberately **excluded**, never allowlisted, per FR-8/N-06 §6)
  - `GET /v1/support/faq?q=` (search), `GET /v1/support/faq/{id}` (detail), `POST /v1/support/tickets`, `GET /v1/support/tickets` (C.25 B-03/B-04 — corrected: two distinct FAQ routes, not one bare path)
  - `GET /v1/parent/consents` (read), `POST /v1/parent/consents/{id}/withdraw` (C.26 B-01 — corrected: no `PATCH` endpoint exists), `POST /v1/data-requests/exports`, `GET /v1/data-requests/{id}` (C.26 B-03)
- Explicitly configure rejection (not silent 404, but a deliberate CORS/403 rejection distinguishable in logs) for any request from this origin to a route outside the above list — with `POST /api/v1/billing/subscribe`, `POST /v1/parent/subscription/restore`, `GET /v1/parent/dashboard`, and `GET /v1/children/*` enumerated as named negative-test targets given their business criticality.
- Configure a staging-equivalent origin (e.g. `staging.account.noorheroes.com`) with an identical allowlist.
- Correctly handle CORS preflight (`OPTIONS`) requests for every allowlisted route.
- **Two entries above remain BLOCKED pending written resolution (N-05 Task 01, N-09 Task 01) and must not be deployed to production until resolved** — this allowlist may be built and tested against every other confirmed route in the interim.

## 11. API Contract
Not applicable — this sub-feature introduces no new endpoints. It is exclusively a cross-cutting access-control configuration over the existing endpoints enumerated in §10, each already contractually defined in its owning feature's blueprint (A.1, C.19/C.23, C.21, C.24, C.25, C.26).

## 12. Database Requirements
None — no new tables. If enforcement decisions are logged, they are recorded via B-04's audit mechanism, not a new schema owned by this sub-feature.

## 13. Validation
- Origin header must exactly match the configured allowlist (`https://account.noorheroes.com`, staging equivalent) — no wildcard subdomain matching.
- Route-path matching must be exact-or-explicitly-parameterized (e.g. `DELETE /v1/sessions/{id}` matches a path parameter, not an open wildcard suffix).

## 14. Authentication
Not applicable directly (this sub-feature operates ahead of/alongside authentication, at the origin/routing level) — every allowlisted endpoint retains its own existing authentication requirement (`Depends(get_current_parent)` etc.) unchanged.

## 15. Authorization
Not applicable directly — this is origin-level access control, distinct from and layered in front of each endpoint's existing per-request authorization (family ownership, step-up, RBAC scopes), none of which this sub-feature modifies.

## 16. Error Handling
| Scenario | System Behavior |
|---|---|
| Request from `account.noorheroes.com` to a non-allowlisted route | Rejected at the gateway layer (CORS/403), before reaching the service layer; logged with origin + attempted route |
| Request from `account.noorheroes.com` to `POST /api/v1/billing/subscribe` | Rejected — treated as the highest-priority negative test in this entire sub-feature |
| Preflight (`OPTIONS`) request for an allowlisted route | Standard CORS preflight response permitting the follow-up request |
| Preflight (`OPTIONS`) request for a non-allowlisted route | Rejected, consistent with the actual request's rejection |
| Malformed or spoofed `Origin` header | Treated as non-matching; rejected, never defaulted to allow |

## 17. Offline First
Not applicable (backend infrastructure configuration).

## 18. Local Data
Not applicable (backend).

## 19. Localization
Not applicable (backend).

## 20. RTL
Not applicable (backend).

## 21. Analytics
Not applicable directly — rejected-request events feed B-04's audit/alerting, not a product analytics event.

## 22. Performance
Allowlist matching must be O(1) (hash/set lookup keyed by origin+route), evaluated on every request from this origin without introducing meaningful gateway latency; this is a low-traffic surface (§1.4 "Page load p95 < 1.5s" applies to the frontend, but the gateway check itself must not be a bottleneck for any caller).

## 23. Security
- This is the single most important control in the entire D.27 feature: a two-layer defense (this gateway-level allowlist, paired with N-02's independent frontend-level `apiClient` scope restriction) against child-data or purchase-capability leakage onto a second client surface.
- Explicit allowlist (default-deny), never an implicit default-allow list that silently exposes a newly added platform route to this origin.
- `POST /api/v1/billing/subscribe` rejection is the top pre-launch security gate per PRD §12.9 and §15.2 (rollback trigger).

## 24. Library Requirements
Whatever CORS/gateway configuration mechanism the platform's existing infrastructure already uses (confirm exact product/library before introducing a new one) — no new library should be required for a configuration-only change; if in-app enforcement is layered on top, FastAPI's built-in `CORSMiddleware` (Starlette) is the existing-ecosystem choice, not a third-party addition.

## 25. Testing
- Integration: request from `account.noorheroes.com` origin to every allowlisted route succeeds (once authenticated) exactly as it would from any other permitted origin.
- Integration: request from `account.noorheroes.com` to `POST /api/v1/billing/subscribe` is rejected — the highest-priority test in this sub-feature, per PRD §5's code-generation prompt item 3.
- Integration: request from `account.noorheroes.com` to `POST /v1/parent/subscription/restore` is rejected (deliberately excluded despite living on the same allowlisted router as `GET /v1/parent/subscription`).
- Integration: request from `account.noorheroes.com` to `GET /v1/parent/dashboard` and to `GET /v1/children/{id}` (any child-scoped route) is rejected.
- Integration: request from `account.noorheroes.com` to `PATCH /v1/parent/consents` (a route that does not exist) returns a standard 404/405, not a misleading allow — confirms the allowlist was corrected to the actual `GET`/`POST .../withdraw` shape, not the PRD's shorthand.
- Integration (schema enumeration): a test that walks the platform's full OpenAPI schema and asserts every route is either explicitly on the allowlist or explicitly rejected for this origin — no route may fall through to an ambiguous default-allow state (mirrors B-02's middleware-level version of this same guarantee; this test operates at the gateway-config level).
- Integration: preflight (`OPTIONS`) behavior matches the actual request's allow/reject outcome for a sample of both allowlisted and non-allowlisted routes.
- Regression: this suite re-runs on every deploy touching gateway/CORS configuration (CI-blocking, per PRD §10 DevOps Requirements) and every time a new route is added to the platform's OpenAPI schema.

## 26. Documentation
Document the full allowlist (with source blueprint citation per route, e.g. "`GET /v1/parent/subscription` — C.24 B-05") in the gateway configuration's own comments/README, and cross-reference this file from B-02's route-capability allowlist documentation so the two do not drift independently.

## 27. AI Coding Agent Implementation Steps

**Task 01 — Confirm Gateway/Infrastructure Layer**
- **Objective:** Identify the actual product/mechanism enforcing CORS ahead of the FastAPI app (dedicated API Gateway, reverse proxy, or in-app `CORSMiddleware`) before writing configuration against an assumed layer.
- **Why This Is Required:** `FAST-API-INSTRUCTIONS.md` does not document this layer; rule 30 prohibits inventing infrastructure that may not match the actual deployment.
- **Definition of Done:** Confirmed target configuration surface, documented in this task's outcome.

**Task 02 — Resolve the C.23 B-06 Session-Contract Scope Question**
- **Objective:** Determine whether `GET/DELETE /v1/sessions` (child-mode device sessions per C.23 B-06) is the correct allowlist target for N-05's "Devices and Sessions" screen, or whether a distinct parent-account-session endpoint is required and does not yet exist.
- **Why This Is Required:** Per §6, the PRD's own citation ("C.19's session-list contract") does not match the actual owning implementation's scope (child-mode sessions, not parent login sessions) found in C.23 B-06.
- **Definition of Done:** Written confirmation of which contract this allowlist entry targets, obtained before finalizing the allowlist.

**Task 03 — Resolve the C.21 Family-Level Deletion Endpoint Question**
- **Objective:** Confirm whether `POST /v1/parent/deletion-request` / `GET /v1/parent/deletion-status` exist (or are planned) as family-level account-deletion endpoints, distinct from C.21's reviewed per-child deletion endpoints.
- **Why This Is Required:** C.26 KMP K-07 already flagged this exact ambiguity for the Mobile App; D.27 inherits the identical unresolved question for its own Deletion Request & Status screen (N-09).
- **Definition of Done:** Written product/architecture confirmation obtained; this blocks finalizing the allowlist entry for these two routes.

**Task 04 — Define the Explicit Allowlist Configuration**
- **Files to Create:** Gateway/infrastructure config artifact (per Task 01's confirmed location).
- **Implementation Details:** Enumerate exactly the routes in §10, each annotated with its owning blueprint reference.
- **Dependencies:** Tasks 01–03.

**Task 05 — Implement Default-Deny Enforcement**
- **Implementation Details:** Any route not explicitly present in the Task 04 allowlist is rejected for this origin — implemented as default-deny, not default-allow-minus-exclusions.

**Task 06 — Staging-Equivalent Origin Configuration**
- **Definition of Done:** Staging origin present with an identical allowlist to production.

**Task 07 — Write the Full Allowlist/Rejection Test Suite**
- **Files to Create:** `test_web_portal_cors_allowlist.py`, `test_web_portal_billing_subscribe_rejection.py`.
- **Implementation Details:** Per §25, including the full-OpenAPI-schema enumeration test.
- **Definition of Done:** All tests green; `billing/subscribe` and child-scoped rejection tests treated as release-blocking.

**Task 08 — CI Gate Wiring**
- **Definition of Done:** This suite runs on every deploy touching gateway/CORS config (PRD §10).

**Task 09 — Documentation & Cross-Reference**
- **Definition of Done:** Allowlist documented with per-route blueprint citations; cross-referenced from B-02.

## 28. Definition of Done
`account.noorheroes.com` can reach exactly the explicit, documented allowlist of existing endpoints and nothing else, verified by an automated test that enumerates the platform's full route set (no ambiguous default-allow), with `POST /api/v1/billing/subscribe` and all child-scoped routes proven unreachable — and the two flagged scope ambiguities (C.23 B-06 session-contract fit, C.21 family-level deletion endpoint existence) are resolved in writing, not silently assumed, before the allowlist is finalized.

## 29. Final Verification Checklist
- [ ] Gateway/infrastructure layer confirmed (Task 01) before configuration was written
- [ ] `POST /api/v1/billing/subscribe` rejection verified by an automated, CI-blocking test
- [ ] `POST /v1/parent/subscription/restore` rejection verified (deliberately excluded, same router as an allowlisted route)
- [ ] `GET /v1/parent/dashboard` and `GET /v1/children/*` rejection verified
- [ ] `PATCH /v1/parent/consents` confirmed absent from the allowlist (route does not exist; corrected from PRD §3.4)
- [ ] OTP allowlist entries use `/v1/identity/auth/otp/*`, not the PRD's `/v1/auth/otp/*` shorthand
- [ ] FAQ allowlist has two distinct entries (`/v1/support/faq?q=` search, `/v1/support/faq/{id}` detail), not one bare path
- [ ] `POST /v1/identity/auth/pin` (reset) added to the allowlist (was absent from the PRD's own §3.4 list)
- [ ] Full-OpenAPI-schema enumeration test passes — no route falls through to ambiguous default-allow
- [ ] Staging origin allowlist matches production allowlist
- [ ] C.23 B-06 session-contract scope question resolved in writing (Task 02) — entry remains BLOCKED until then
- [ ] C.21 family-level deletion endpoint existence confirmed in writing (Task 03) — entry remains BLOCKED until then
- [ ] No PostgreSQL/Redis credential changes
