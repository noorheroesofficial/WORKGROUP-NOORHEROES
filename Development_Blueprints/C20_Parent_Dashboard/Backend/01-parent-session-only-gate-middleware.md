# Blueprint: Parent-Session-Only Gate Middleware

## 1. Feature Context
Platform: NoorHeroes Backend (FastAPI, Modular Monolith). New bounded context: `dashboard`, mounted at `src/noorheroes/modules/dashboard/`. This blueprint delivers the single most important guarantee of the entire Parent Dashboard feature: no child-mode session token may ever successfully call any Dashboard endpoint.

## 2. Parent Feature
C.20 — Parent Dashboard (`PRD_Documents/Parent Area — In-App (19-26)/Feature_C20_Parent_Dashboard.md`)

## 3. Sub-feature
B-01 — Parent-Session-Only Gate Middleware

## 4. Objective
Implement a router-mount-level FastAPI dependency/middleware that inspects the authenticated session and immediately rejects (`403 CHILD_MODE_TOKEN_REJECTED`) any request to the `dashboard` module's routes carrying a child-mode token — structurally, so a newly added route cannot forget to add its own check.

## 5. Business Requirements
Source: PRD §1.7 FR-6, §3.5, §5 (Backend AI Code-Generation Prompt item 1), §12.2, §15.2.
- FR-6: "The Parent Progress Dashboard exists only in the Mobile App and is hidden in every child profile session... Parent dashboard APIs reject any child-mode token outright." This is a P0, zero-exception architectural rule enforced at the API layer.
- Must be applied at router-mount level (dependency list on `APIRouter`), not per-handler, so it cannot be bypassed by a future endpoint.
- Distinct error code `403 CHILD_MODE_TOKEN_REJECTED` required for monitoring/log traceability, separate from generic 401/403 (ordinary expired/revoked-session rejection is a different, additional check — see B-02).

## 6. Existing Architecture — VERIFIED AGAINST ACTUAL CODEBASE (`backend/src/noorheroes/`)
The generic 10-bounded-context inventory in `FAST-API-INSTRUCTIONS.md` describes the target architecture, but the actual implemented modules today are narrower: `access_gate`, `admin`, `ai_safety`, `content`, `data_rights`, `identity`, `learning` (stub — `__init__.py` only), `localization`, `media`, `notifications`, `review`, `rewards`, `subscriptions` (stub — `__init__.py` only). `main.py` currently wires only the E.29 (Content CMS/Review) and C.26 (Privacy/Consent) routers; no `dashboard` module exists yet, confirming this is greenfield.
- Confirmed real `core/deps.py` contents: `ParentSessionContext(family_id, parent_sub, session_id, scopes)`, `ChildSessionContext(family_id, child_id, session_id)`, `AdminSessionContext`, `get_current_parent()`/`get_current_child()`/`get_current_admin()` (each decodes the bearer token via `decode_token()` from `core/security.py` and raises the SAME generic `AuthenticationError` (401) for BOTH an invalid/expired token AND a wrong-mode token — e.g. `get_current_parent()` raises plain 401 for a child-mode token, it does NOT already distinguish "child-mode" from "invalid"). This confirms this blueprint's own `require_parent_session_only()` must decode the token itself (reusing `decode_token()`) rather than calling `get_current_parent()`, precisely so it can raise the distinct `403 CHILD_MODE_TOKEN_REJECTED` PRD requires instead of `get_current_parent()`'s generic 401.
- Confirmed real `core/exceptions.py`: `DomainError` base has `status_code`/`error_code` class attributes and a registered `@app.exception_handler(DomainError)` in `main.py` producing `{"error": {"code": ..., "message": ..., **context}}` — this blueprint's `ChildModeTokenRejectedError` must follow this exact envelope shape (not the `{"error_code": ..., "message": ...}` shape assumed in earlier drafts of this document).
- **Confirmed real grace-window gate dependency (use this, do not reinvent):** `noorheroes.modules.identity.parent_gate.require_parent_gate_verified` — already implemented and reused by C.23 B-06 (`modules/access_gate/api.py`) and C.26. It wraps `get_current_parent()`, checks an in-memory marker store (`is_verified(parent_sub)`, TTL `PARENT_GATE_TTL_SECONDS = 600` i.e. 10 minutes — this IS the PRD's "short grace window" per FR-5), and raises `AuthorizationError("Step-up verification required (PIN/biometric)")` if not currently verified. Its own docstring flags it as a deliberately Redis-shaped in-memory stand-in pending real C.19 build-out and a real Redis instance — reuse it as-is; do not fork a second copy for C.20.

## 7. Existing Code to Reuse
- `ParentSessionContext`, `ChildSessionContext` DTOs (`core/deps.py`) — reuse as-is; do not redefine.
- `decode_token()` (`core/security.py`) — call directly inside `require_parent_session_only()` to read the `mode` claim before `get_current_parent()`'s coarser check would apply.
- `require_parent_gate_verified` (`noorheroes.modules.identity.parent_gate`) — reuse for grace-window/step-up enforcement, layered ON TOP OF this blueprint's own child-mode-token check (see §10).
- `AuthorizationError`/`AuthenticationError` exception bases (`core/exceptions.py`) — extend, do not replace; follow the `status_code`/`error_code` class-attribute pattern exactly.
- `RequestIdMiddleware` / `StructuredLoggingMiddleware` pattern (`infrastructure/`) as the template for how request-scoped middleware/dependencies are structured in this codebase.

## 8. Files to Create
- `src/noorheroes/modules/dashboard/__init__.py`
- `src/noorheroes/modules/dashboard/deps.py` — `require_parent_session_only()` dependency + `ChildModeTokenRejectedError` exception
- `src/noorheroes/modules/dashboard/api.py` — `DashboardRouter = APIRouter(dependencies=[Depends(require_parent_session_only)])` (empty route stub for this blueprint; B-02/B-03 populate it)
- `tests/modules/dashboard/test_parent_session_only_gate.py`

## 9. Files to Modify
- `src/noorheroes/core/exceptions.py` — add `ChildModeTokenRejectedError(AuthorizationError)` with `error_code="CHILD_MODE_TOKEN_REJECTED"`
- `src/noorheroes/api/router.py` (or equivalent root API aggregator, per existing 10-context registration pattern) — mount `DashboardRouter` under `/v1/parent/dashboard`

## 10. Backend Requirements
- `require_parent_session_only()`: FastAPI dependency, added to `APIRouter(dependencies=[...])` at router-mount level (not per-endpoint), so every current and future route under this router inherits the check automatically.
- Internally: call `decode_token(credentials.credentials)` directly (same helper `get_current_parent`/`get_current_child` use internally) and branch on the decoded `mode` claim — if `mode == "child"`, raise `ChildModeTokenRejectedError` immediately, before any query params or handler body execute; if `mode == "parent"`, construct and return a `ParentSessionContext` (mirrors `get_current_parent()`'s own construction logic) so downstream handlers can `Depends(require_parent_session_only)` directly; if the token fails to decode at all or `mode` is neither, raise `AuthenticationError` (401) — distinct code path, not conflated with child-mode rejection (PRD Edge Case 8).
- **Layer the grace-window gate on top:** chain `require_parent_gate_verified` (`noorheroes.modules.identity.parent_gate`, confirmed real implementation — see §6) after `require_parent_session_only` at router-mount level, i.e. `APIRouter(dependencies=[Depends(require_parent_session_only), Depends(require_parent_gate_verified)])`. This enforces PRD FR-5's "re-entry always requires the PIN/biometric gate unless within the short grace window" on every Dashboard call, not just initial navigation — reusing the confirmed 600-second in-memory marker, not a new mechanism.
- `ChildModeTokenRejectedError` must serialize to HTTP `403` via the app's actual registered `@app.exception_handler(DomainError)` envelope: `{"error": {"code": "CHILD_MODE_TOKEN_REJECTED", "message": "..."}}` (confirmed shape from `main.py`, not the flat `{"error_code": ...}` shape assumed in an earlier draft of this blueprint).

## 11. KMP Requirements
N/A — this is a backend-only structural guarantee. KMP's obligation (enforced in K-01) is simply: never call this API from a child-mode session context; the Android app has no code path that does so because `:feature:parent-dashboard` is reachable only through `:core:auth`'s Parent Gate.

## 12. NextJS Requirements
N/A — Parent Dashboard has no web-portal surface at all (PRD FR-12); no NextJS work in this sub-feature.

## 13. API Contract
No public endpoint added by this blueprint itself — it is middleware applied to the router that B-02/B-03 populate. Error contract (confirmed envelope shape from `main.py`'s registered `DomainError` handler):
- **Error Response (403, child-mode token):** `{ "error": { "code": "CHILD_MODE_TOKEN_REJECTED", "message": "This endpoint is not available in Child Mode." } }`
- **Error Response (403, grace window expired):** `{ "error": { "code": "FORBIDDEN", "message": "Step-up verification required (PIN/biometric)" } }` (from `require_parent_gate_verified`'s existing `AuthorizationError`)
- **Error Response (401):** standard `AuthenticationError` envelope for expired/invalid/revoked sessions (unchanged from platform baseline).

## 14. Database Requirements
None. No schema changes.

## 15. Validation
- Session token type must resolve to exactly one of `ParentSessionContext` / `ChildSessionContext` / invalid — no ambiguous third state.
- Dependency must execute before any query-parameter parsing in downstream handlers (guaranteed by FastAPI's `dependencies=[...]` at router level, which runs prior to path-operation-specific dependencies).

## 16. Authentication
Reuses the platform's existing JWT verification (`core/security.py`, `core/deps.py`). No new auth mechanism introduced.

## 17. Authorization
This entire sub-feature *is* an authorization control. No RBAC scopes required beyond "must not be a child-mode session."

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Child-mode token on any dashboard route | `403 CHILD_MODE_TOKEN_REJECTED` |
| Expired/revoked parent token | `401` standard `AuthenticationError` (distinct from above) |
| Valid parent token | Pass-through, `ParentSessionContext` injected |

## 19. Offline First
N/A — server-side middleware.

## 20. Local Data
N/A.

## 21. Localization
N/A — error code is a machine-readable string; client (KMP) owns any user-facing copy.

## 22. RTL
N/A.

## 23. Analytics
Emit a structured log / security signal on every `ChildModeTokenRejectedError` occurrence (family_id if resolvable, route path, timestamp) to support the DevOps P0 alert requirement (§10: "Alert on any production-sampling-detected instance of a child-mode token successfully reaching a Dashboard endpoint" — this log is the detection input for that alert, since in the correct-behavior case the request never "reaches" a handler).

## 24. Performance
Negligible overhead — a single token-type check reusing already-decoded JWT claims, no additional DB/Redis round trip beyond existing auth verification.

## 25. Security
This is the P0 security control for the entire feature (PRD §12.1, §12.2). OWASP Broken Access Control mitigation via structural, router-level enforcement rather than a per-endpoint convention that could be forgotten.

## 26. Library Requirements
No new dependencies. Uses existing FastAPI, PyJWT/JOSE (whichever the platform's `core/security.py` already uses), pytest.

## 27. Testing
1. Unit test: `require_parent_session_only()` rejects a `ChildSessionContext`-shaped token with `403 CHILD_MODE_TOKEN_REJECTED`.
2. Unit test: passes through a valid `ParentSessionContext`.
3. Unit test: raises standard `401 AuthenticationError` for expired/malformed token (distinct assertion from the 403 case).
4. **Structural/signature test (mandatory):** register a NEW dummy route on `DashboardRouter` inside the test file itself, with zero endpoint-specific auth code, and confirm a child-mode token is still rejected against it — proving the protection is structural, not per-handler.
5. Integration test: full request lifecycle through the mounted router confirms rejection prior to any handler logic executing (assert handler function is never invoked, e.g., via a call-counter stub route).

## 28. Documentation
- Add `DashboardRouter` and `require_parent_session_only` entries to the module's own `README.md` (if the module convention includes one) or equivalent inline docstring per existing module conventions.
- OpenAPI: document `403 CHILD_MODE_TOKEN_REJECTED` as a standard response on the router's `responses={}` declaration so it's visible in generated API docs for all mounted routes.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Add ChildModeTokenRejectedError Exception**
- Task ID: B01-T01
- Objective: Define the distinct exception type for this rejection reason.
- Why This Is Required: PRD explicitly requires a distinct error code from generic 401/403 for log/monitoring traceability.
- Existing Architecture to Follow: `core/exceptions.py` `DomainError` hierarchy pattern.
- Existing Files to Reuse: `core/exceptions.py` (`AuthorizationError` as base).
- Files to Create: none.
- Files to Modify: `src/noorheroes/core/exceptions.py`.
- Implementation Details: `class ChildModeTokenRejectedError(AuthorizationError): error_code = "CHILD_MODE_TOKEN_REJECTED"`. Ensure the existing global exception handler maps `error_code` to the response body's `error_code` field.
- Business Rules: Must map to HTTP 403.
- Validation: N/A.
- Error Handling: N/A (this IS the error type).
- Security: N/A.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: Docstring on the class citing PRD FR-6.
- Dependencies: None.
- Do Not Change: Do not modify other existing exception subclasses.
- Expected Result: New exception class importable from `core.exceptions`.
- Definition of Done: Class exists, inherits correctly, maps to 403 via existing handler.

**Task 02 — Implement require_parent_session_only Dependency**
- Task ID: B01-T02
- Objective: Build the gate dependency function.
- Why This Is Required: Core mechanism of this sub-feature.
- Existing Architecture to Follow: `core/deps.py` dependency-function pattern (`get_current_parent`, `get_current_child`).
- Existing Files to Reuse: `core/deps.py` session-resolution logic (reuse the same token decode path, do not duplicate JWT parsing).
- Files to Create: `src/noorheroes/modules/dashboard/deps.py`.
- Files to Modify: none.
- Implementation Details: Resolve session context from the bearer token; branch on type (`ParentSessionContext` → return it; `ChildSessionContext` → raise `ChildModeTokenRejectedError`; invalid/expired → propagate existing `AuthenticationError`).
- Business Rules: FR-6, zero exceptions.
- Validation: Session type must be unambiguous.
- Error Handling: Per §18 table above.
- Security: Core control of this blueprint.
- Performance: Reuse already-decoded claims; no extra I/O.
- Localization: N/A.
- RTL: N/A.
- Analytics: Log rejection events (see Task 05).
- Tests: Covered in Task 04.
- Documentation: Docstring with PRD citation.
- Dependencies: Task 01.
- Do Not Change: Do not alter `get_current_parent`/`get_current_child` themselves — this is a new, additive dependency.
- Expected Result: `require_parent_session_only` importable and usable in `Depends()`.
- Definition of Done: Function correctly discriminates all three token states.

**Task 03 — Mount DashboardRouter with Router-Level Dependency**
- Task ID: B01-T03
- Objective: Apply the gate at router-mount level so it is structurally non-bypassable.
- Why This Is Required: PRD explicitly requires this NOT be a per-endpoint check.
- Existing Architecture to Follow: Existing 10-context router registration pattern in the root API aggregator.
- Existing Files to Reuse: Root router aggregator file.
- Files to Create: `src/noorheroes/modules/dashboard/api.py`, `src/noorheroes/modules/dashboard/__init__.py`.
- Files to Modify: root API aggregator (e.g., `src/noorheroes/api/router.py`).
- Implementation Details: `DashboardRouter = APIRouter(prefix="/v1/parent/dashboard", dependencies=[Depends(require_parent_session_only), Depends(require_parent_gate_verified)], responses={403: {"description": "Child-mode token rejected or step-up verification required"}})`, importing `require_parent_gate_verified` from `noorheroes.modules.identity.parent_gate` (confirmed real module — do not reimplement). Mount into `main.py` alongside the existing E.29/C.26 routers (`app.include_router(dashboard_router)` — this module's routes already bake their full `/v1/parent/dashboard` prefix into the `APIRouter`, matching the C.26 routers' no-additional-prefix convention observed in `main.py`).
- Business Rules: FR-6.
- Validation: N/A.
- Error Handling: N/A.
- Security: This IS the structural enforcement point.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: OpenAPI `responses` declaration.
- Dependencies: Task 02.
- Do Not Change: Do not add per-endpoint auth checks that duplicate this — future sub-features (B-02, B-03, B-06) must rely on this router-level gate.
- Expected Result: Router mounted and protected.
- Definition of Done: Router appears in OpenAPI schema under `/v1/parent/dashboard` prefix with the gate applied.

**Task 04 — Write Structural and Unit Tests**
- Task ID: B01-T04
- Objective: Prove the protection is structural, not per-handler, plus standard unit coverage.
- Why This Is Required: PRD's Backend AI Code-Generation Prompt item 1 mandates this exact test.
- Existing Architecture to Follow: `pytest` + existing test fixture patterns for auth in this codebase.
- Existing Files to Reuse: Existing JWT/session test fixtures/factories if present.
- Files to Create: `tests/modules/dashboard/test_parent_session_only_gate.py`.
- Files to Modify: none.
- Implementation Details: Include the 5 test cases listed in §27 above, notably adding a new dummy route with zero endpoint-specific auth code inside the test and confirming rejection.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert exact error_code strings.
- Security: This is the CI-blocking security gate (DevOps §10 mandatory, non-bypassable).
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test docstrings explaining intent per PRD citation.
- Dependencies: Tasks 01–03.
- Do Not Change: N/A.
- Expected Result: All 5 test cases pass.
- Definition of Done: Test suite green; CI configured to treat this suite as a mandatory, non-bypassable gate per DevOps requirement §10.

**Task 05 — Add Security Logging for Rejection Events**
- Task ID: B01-T05
- Objective: Emit structured log entries on every rejection for P0 alerting.
- Why This Is Required: DevOps §10 P0 alert requirement depends on this signal.
- Existing Architecture to Follow: Existing structured logging pattern (`StructuredLoggingMiddleware`).
- Existing Files to Reuse: Platform logger utility.
- Files to Create: none.
- Files to Modify: `src/noorheroes/modules/dashboard/deps.py`.
- Implementation Details: On `ChildModeTokenRejectedError` raise, log `{event: "dashboard_child_mode_token_rejected", route, family_id_if_resolvable, timestamp}` — matches analytics event name in PRD §1.19.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: N/A.
- Security: PII-safe logging (mask sensitive identifiers per platform logging convention).
- Performance: Non-blocking log call.
- Localization: N/A.
- RTL: N/A.
- Analytics: `dashboard_child_mode_token_rejected` internal/security signal (PRD §1.19).
- Tests: Add assertion in Task 04's suite that the log call fires.
- Documentation: Note in module docstring.
- Dependencies: Task 02.
- Do Not Change: N/A.
- Expected Result: Every rejection is observable in logs/monitoring.
- Definition of Done: Log line emitted and asserted in tests.

## 30. Definition of Done
- `DashboardRouter` exists, mounted at `/v1/parent/dashboard`, protected by `require_parent_session_only` at router-mount level.
- A child-mode token against any current or hypothetically-new route under this router receives `403 CHILD_MODE_TOKEN_REJECTED`.
- Expired/invalid tokens receive standard `401`, distinctly.
- All 5 tests in §27 pass, including the structural dummy-route test.
- Rejection events are logged for alerting.
- CI treats this test suite as a mandatory, non-bypassable gate.

## 31. Final Verification Checklist
- [ ] Router-level (not per-endpoint) dependency confirmed via code review
- [ ] Structural dummy-route test present and passing
- [ ] `403 CHILD_MODE_TOKEN_REJECTED` distinct from generic `401`/`403`
- [ ] Expired/revoked-token path unaffected and distinct
- [ ] Logging emits on every rejection
- [ ] No PostgreSQL/Redis credential files touched
- [ ] No existing exception subclasses modified/removed
- [ ] OpenAPI schema reflects the 403 response on the router
