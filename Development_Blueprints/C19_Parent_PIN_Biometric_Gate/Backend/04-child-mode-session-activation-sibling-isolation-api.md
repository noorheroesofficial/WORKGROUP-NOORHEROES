# B-04 — Child-Mode Session Activation & Sibling Isolation API

> **Status:** ✅ **Implemented & Verified** (Production Ready)  
> **Module Location:** `src/noorheroes/modules/access_gate/`  
> **Test Suites:** `tests/modules/access_gate/test_session_service.py` (13 tests), `tests/modules/access_gate/test_session_api.py` (15 tests), `tests/modules/access_gate/test_sibling_isolation.py` (8 tests) — **36/36 passed (100%)** (all 95 `access_gate` tests passing)  
> **Core Dependencies Added:** `require_child_session`, `require_child_session_for` (`src/noorheroes/core/deps.py`)  
> **Documentation:** `FAST-API-INSTRUCTIONS.md` §5.12/§6.12/`core/deps.py`, `MASTER-README.md` §11.8, `NoorHeroes_Consolidated_Execution_Blueprint.md` §0.5/§5.2 Item 71  

## 1. Feature Context

Stages 3–4 of the canonical four-stage pipeline (Check Restrictions, Activate Context). This is the platform's structural defense against cross-sibling data leakage: every downstream child-scoped API call must be traceable back to a session token strictly bound to one `child_id`, with family ownership alone explicitly insufficient authorization. This is flagged by the PRD as one of the two highest-priority guarantees in the entire service.

## 2. Parent Feature
Feature C.19 — Parent PIN/Biometric Gate & Profile Access Control

## 3. Sub-feature
1.4 Child-Mode Session Activation & Sibling Isolation API (ID: **B-04**)

## 4. Objective
Implement `POST /v1/sessions/child-mode`, running the full restriction-evaluation stage before issuing a session token strictly bound to `family_id` + `child_id` + device ID, with a specific failure reason per distinct restriction failure, and enforce that this binding is checked on every downstream child-scoped call.

## 5. Business Requirements
- FR-7 (stages 3–4): Check Restrictions (disabled status, entitlement, screen-time, bedtime, device, content eligibility) then Activate Context (session creation, notification-binding switch, previous-cache-clear signal).
- FR-8: sibling progress must never be returned to child-mode API calls — the platform-wide "No Lateral Sibling Access" rule originates here.
- FR-9: switching to a different child clears previous child-sensitive UI state before the new session activates (client-side, KMP K-05, triggered by this API's response).
- FR-15: offline restriction checks fall back to the last-signed policy snapshot; this endpoint is the online, authoritative path.
- Edge Case 1: connectivity lost exactly at "Check Restrictions" → falls back to last-signed policy snapshot rather than blocking activation entirely.

## 6. Existing Architecture
New `Session Activation Service` in `modules/access_gate`, orchestrating calls to the Restriction Engine (owned by C.23 — **not yet implemented**; this sub-feature must define a clean interface/stub against which C.23 will later provide the real implementation), Entitlement Service, and B.17's Device Profile Binding Service.

## 7. Existing Code to Reuse
- `modules/access_gate/lock_repository.py` (B-01) — for confirming a preceding successful lock verification where applicable
- B.17's `modules/notifications/binding_service.py::DeviceBindingService` (confirm exact module path against B.17's implementation before wiring)
- `core/deps.py::get_current_parent`

## 8. Files to Create
- `src/noorheroes/modules/access_gate/session_schemas.py` — `ChildSessionRequest`, `ChildSessionResponse`
- `src/noorheroes/modules/access_gate/session_service.py` — `SessionActivationService`
- `src/noorheroes/modules/access_gate/restriction_client.py` — thin interface to the Restriction Engine (stub against C.23 contract; **do not implement restriction business logic here** — that is C.23's ownership)
- `src/noorheroes/modules/access_gate/session_token.py` — child-mode session token issuance/validation utility, strictly scoped to `{family_id, child_id, device_id}`
- `src/noorheroes/core/deps.py` (extend) — `require_child_session(expected_child_id)` dependency for downstream endpoints
- `tests/modules/access_gate/test_session_service.py`
- `tests/modules/access_gate/test_session_api.py`
- `tests/modules/access_gate/test_sibling_isolation.py` — dedicated fixture-sibling test file per PRD's explicit instruction

## 9. Files to Modify
- `src/noorheroes/modules/access_gate/api.py` — add `POST /v1/sessions/child-mode`
- `src/noorheroes/core/deps.py` — add `require_child_session` for reuse by every other child-scoped module (B.16, A.2–A.12, B.13–B.18)

## 10. Backend Requirements
- `SessionActivationService.activate(parent_ctx, child_id)`:
  1. Validate family ownership of `child_id` → `404` otherwise.
  2. Call `RestrictionClient.evaluate(child_id)` → returns a structured result with a specific `failure_reason` enum (`disabled|entitlement_expired|screen_time_exhausted|bedtime_window|device_not_permitted|content_ineligible`) or `passed`.
  3. On any failure, return `403` with the specific `failure_reason` — never a generic error.
  4. On pass: issue a `session_token` (signed JWT recommended) with claims `{family_id, child_id, device_id, exp}`.
  5. Trigger `DeviceBindingService.switch_binding(device_id, child_id)` (B.17 reuse).
  6. Return `{session_token, restrictions, expires_at}` — response also signals the client to clear the previous profile's cache (client-driven, per FR-9; this endpoint's response is the trigger, the clearing itself is KMP K-05's responsibility).
- `require_child_session(expected_child_id)` dependency: decodes `session_token` from the bearer header, verifies `child_id` claim **exactly matches** the `expected_child_id` path/query parameter of the calling endpoint — family ownership match alone is explicitly **not** sufficient; the token's `child_id` claim must equal the requested resource's `child_id`.

## 11. API Contract

### `POST /v1/sessions/child-mode`
- **Auth:** Bearer (parent/device context, post-lock-verification if applicable)
- **Request:** `{ "child_id": "..." }`
- **Response 200:** `{ "session_token": "...", "restrictions": {...}, "expires_at": "..." }`
- **Response 403:** `{ "error": "RESTRICTION_FAILED", "failure_reason": "screen_time_exhausted" }` (one of the six enum values)
- **Error Responses:** `401 UNAUTHORIZED`, `404 CHILD_NOT_FOUND`, `403 RESTRICTION_FAILED`

## 12. Database Requirements
No new persistent table for the session token itself (stateless signed JWT recommended); if server-side revocation is required, a lightweight `child_session` Redis entry keyed by token ID with TTL = `expires_at`. Restriction/entitlement data is owned by C.23/Entitlement Service, not this sub-feature.

## 13. Validation
`child_id` required, must be a valid UUID owned by the caller's family.

## 14. Authentication
Bearer token for the parent/device context requesting activation (this endpoint issues the *child-mode* token; it itself is called with the parent-level/device-level token).

## 15. Authorization
Family ownership of `child_id` for issuance. For all **downstream** child-scoped endpoints: `require_child_session` enforces exact `child_id` claim match — this is the platform's core sibling-isolation mechanism and must be adopted by every module exposing child-scoped data (B.16, A.2–A.12, B.13, B.14, B.18, etc.) as those modules are built or retrofitted.

## 16. Error Handling
| Scenario | Response |
|---|---|
| Any restriction check fails | `403` with specific `failure_reason` |
| Unknown/not-owned `child_id` | `404 CHILD_NOT_FOUND` |
| Restriction Engine (C.23) unavailable | `503`, with client falling back to offline last-signed policy per FR-15 (client-side responsibility) |
| Session token used for a different `child_id` than issued | `403 SESSION_CHILD_MISMATCH` — this is the sibling-isolation guarantee, tested explicitly |

## 17. Offline First
This endpoint is the online, authoritative path. KMP falls back to the last-signed policy snapshot for restriction checks when offline (FR-15); this endpoint does not need offline support itself, but must sign/version its restriction responses so the client can cache and later validate a "last-signed" snapshot.

## 18. Analytics
Feeds `restriction_check_failed`, `restriction_override_requested/granted`, `session_activated` (KMP K-05). `failure_reason` distribution feeds the Admin Health Monitor (B-06).

## 19. Performance
This is the highest-traffic endpoint in the feature (called on every profile selection). Target p95 < 250ms including Restriction Engine round-trip; use async I/O throughout, avoid N+1 queries when evaluating multiple restriction dimensions (batch-fetch entitlement + screen-time + bedtime config in one query where the schema allows).

## 20. Security
- **Strict session-to-`child_id` binding is this sub-feature's single most important guarantee** — family ownership match is explicitly insufficient; the CI-blocking test uses fixture sibling children in the same family to prove this (PRD §5 item 5).
- Session tokens are short-lived and scoped to exactly one device + one child.
- No restriction/entitlement internals are exposed beyond the specific `failure_reason` enum (no raw policy data leaked to a locked-out client).

## 21. Library Requirements
FastAPI, SQLAlchemy 2.0, PyJWT (or existing token utility), Redis (optional, for revocation), pytest, pytest-asyncio.

## 22. Testing
- Unit: each of the six `failure_reason` values returns the correct specific response.
- Unit: successful activation issues a token with correct `{family_id, child_id, device_id}` claims.
- **Integration (CI-blocking, highest priority): using two fixture sibling children in the same family, a session token issued for child A is rejected with `403 SESSION_CHILD_MISMATCH` when used against any endpoint scoped to child B — proving family ownership alone is not sufficient authorization.**
- Integration: `require_child_session` dependency correctly rejects mismatched claims across at least one real downstream endpoint (e.g., B.16's progress-summary API once available).
- Integration: Restriction Engine unavailability returns `503` cleanly.

## 23. Documentation
OpenAPI docs enumerate all six `failure_reason` values with descriptions. Document `require_child_session` as the mandatory dependency for any new child-scoped endpoint added anywhere in the codebase, with a code example.

## 24. AI Coding Agent Implementation Steps

**Task 01 — Define Restriction Engine Client Interface**
Objective: clean interface (`RestrictionClient.evaluate(child_id) -> RestrictionResult`) stubbed pending C.23. Files to Create: `restriction_client.py`. Definition of Done: interface documented for C.23 to implement against.

**Task 02 — Implement Child-Mode Session Token Issuance/Validation**
Objective: signed JWT with `{family_id, child_id, device_id, exp}` claims. Files to Create: `session_token.py`. Dependencies: none.

**Task 03 — Implement `require_child_session` Dependency**
Objective: exact `child_id` claim match enforcement, reusable across all future child-scoped modules. Files to Modify: `core/deps.py`. Dependencies: Task 02.

**Task 04 — Implement `SessionActivationService.activate()`**
Objective: full stage-3/4 orchestration per §10. Files to Create: `session_service.py`. Dependencies: Task 01, Task 02, B.17 binding-switch reuse.

**Task 05 — Write Sibling-Isolation CI-Blocking Test**
Objective: fixture sibling children, cross-child session rejection. Files to Create: `test_sibling_isolation.py`. Dependencies: Task 03, Task 04.

**Task 06 — Implement `POST /v1/sessions/child-mode` Router**
Objective: wire schemas, all error paths. Files to Create: `session_schemas.py`. Files to Modify: `api.py`. Dependencies: Task 04.

**Task 07 — Add Full Test Suite & API Docs**
Objective: coverage per §22, including all six failure-reason unit tests. Dependencies: Task 06.

## 25. Definition of Done
`POST /v1/sessions/child-mode` is live, runs the full restriction stage with specific failure reasons, issues strictly-scoped session tokens, and `require_child_session` is available and proven (via fixture siblings) to reject cross-child access even within the same family.

## 26. Final Verification Checklist
- [x] Fixture-sibling cross-child-session test passes and is wired into CI as non-bypassable
- [x] Each of the six `failure_reason` values is independently tested
- [x] Session token claims are exactly `{family_id, child_id, device_id, exp}`, nothing broader
- [x] `require_child_session` documented as mandatory for all future child-scoped endpoints
- [x] Restriction Engine unavailability degrades to `503`, not a silent pass-through
