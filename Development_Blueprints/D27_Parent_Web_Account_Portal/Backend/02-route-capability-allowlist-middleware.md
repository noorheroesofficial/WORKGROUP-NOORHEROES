# B-02 — Route-Capability Allowlist Middleware

## 1. Feature Context
Part of Feature D.27 — Parent Web Account Portal. Where B-01 configures the gateway-level CORS/origin allowlist, B-02 is the in-application enforcement layer that makes the same allowlist a hard, testable, code-level guarantee — so that the exclusion of child-scoped and purchase-initiation routes from `account.noorheroes.com` does not depend solely on gateway configuration remaining correct forever.

## 2. Parent Feature
D.27 Parent Web Account Portal (`account.noorheroes.com`)

## 3. Sub-feature
**B-02 — Route-Capability Allowlist Middleware**

## 4. Objective
Implement an in-application FastAPI middleware that independently re-enforces the origin-to-route allowlist defined in B-01, so that origin-based access control exists at two independent layers (gateway + application), and provide a CI-enforced test that walks the live OpenAPI schema to guarantee every route has an explicit allow/deny classification for this origin — never an unclassified route that silently falls through.

## 5. Business Requirements
- NFR "Structural Scope Exclusion": "a structural guarantee enforced by the frontend's own architecture, not just route-guarding" — B-02 is the backend half of this same structural guarantee, paired with B-01 at the gateway and N-02 at the frontend.
- §5 Backend AI Code-Generation Prompt, item 2: "a comprehensive route-capability allowlist as actual configuration and a test that enumerates every route in the platform's full OpenAPI schema and asserts that each one is EITHER on this explicit allowlist OR explicitly rejected for that origin, with no route accidentally falling through to an ambiguous default-allow state."
- §12.1 Threat Analysis: "mitigated by the gateway-level CORS/route allowlist PLUS the frontend's own independently-restricted `apiClient` scope — defense in depth at two separate layers." B-02 is the backend-side second layer completing this defense-in-depth model (gateway + application + frontend = three layers total once N-02 is built).

## 6. Existing Architecture
Follows the platform's existing middleware registration pattern (`src/noorheroes/infrastructure/middleware/rate_limit.py::RateLimitMiddleware`, registered via `app.add_middleware(...)` per `FAST-API-INSTRUCTIONS.md` §4/§12). B-02 is a new middleware module in the same `infrastructure/middleware/` package, evaluated on every incoming request ahead of route dispatch — consistent with how `RequestIdMiddleware` and `StructuredLoggingMiddleware` are already layered in `main.py`'s middleware stack. It does not replace B-01's gateway-level control; it is an intentionally redundant second check, per the NFR's "not just route-guarding" requirement.

## 7. Existing Code to Reuse
- `src/noorheroes/infrastructure/middleware/rate_limit.py` — structural reference for how existing middleware is implemented and registered in this codebase.
- `src/noorheroes/scripts/export_openapi_schema.py` — the existing script that exports `openapi.json`; reused as the input source for the route-enumeration test (Task 03) rather than re-deriving the route list by hand.
- `src/noorheroes/scripts/classify_openapi_diff.py` — the existing baseline-diff tool; extended (not duplicated) to also flag when a newly added route lacks an explicit allow/deny classification for the `account.noorheroes.com` origin.
- `src/noorheroes/core/exceptions.py::AuthorizationError` — reused as the exception raised on a middleware-level rejection.

## 8. Files to Create
- `src/noorheroes/infrastructure/middleware/web_portal_route_allowlist.py` — the middleware class and the allowlist data structure it consults.
- `src/noorheroes/infrastructure/middleware/route_allowlist_registry.py` — the explicit `{route: classification}` mapping (mirrors B-01's allowlist so both layers can be tested for consistency).
- `tests/infrastructure/test_web_portal_route_allowlist_middleware.py`
- `tests/infrastructure/test_openapi_route_classification_completeness.py`

## 9. Files to Modify
- `main.py` — register `WebPortalRouteAllowlistMiddleware` in the app's middleware stack, positioned ahead of route dispatch (alongside `RequestIdMiddleware`/`RateLimitMiddleware`).
- `src/noorheroes/scripts/classify_openapi_diff.py` — extend to flag any new route missing an explicit allow/deny classification for this origin (fails CI rather than silently passing).

## 10. Backend Requirements
- `route_allowlist_registry.py` defines a data structure (e.g. `dict[str, RouteClassification]` keyed by `(method, path_template)`) with every platform route explicitly marked `ALLOWED_FOR_WEB_PORTAL` or `DENIED_FOR_WEB_PORTAL` — sourced from B-01's same allowlist so the two never diverge (single source of truth, imported by both the gateway config generator and this middleware, if the gateway config can consume a shared Python-defined registry; otherwise, keep the two allowlists textually identical and covered by a cross-consistency test).
- **Corrected paths (applied to B-01 after this file was first written; mirror exactly, do not use the PRD §3.4 shorthand):** `POST /v1/identity/auth/otp/request`, `POST /v1/identity/auth/otp/verify` (not `/v1/auth/otp/*`); `POST /v1/identity/auth/pin` (reset, added — was unnamed in the PRD); `GET /v1/support/faq?q=` and `GET /v1/support/faq/{id}` as two distinct entries (not one bare path); `GET /v1/parent/consents` + `POST /v1/parent/consents/{id}/withdraw` (no `PATCH` entry exists). `POST /v1/parent/subscription/restore` and `POST /api/v1/billing/subscribe` must be explicitly `DENIED_FOR_WEB_PORTAL`, not merely absent, since `restore` lives on the same router as an allowlisted route and could otherwise be mistaken for in-scope.
- **Two entries remain `BLOCKED` in B-01 pending written resolution** — `GET/DELETE /v1/sessions` (N-05 Task 01, C.23 B-06 scope question) and `POST /v1/parent/deletion-request`/`GET /v1/parent/deletion-status` (N-09 Task 01, shared with C.26 K-07). This registry must mark both `DENIED_FOR_WEB_PORTAL` (fail-closed default) until each is resolved and explicitly flipped to `ALLOWED_FOR_WEB_PORTAL` — never provisionally allowed while the question is still open.
- `WebPortalRouteAllowlistMiddleware.dispatch(request, call_next)`:
  1. If `request.headers["Origin"] != "https://account.noorheroes.com"` (or its staging equivalent), pass through unmodified — this middleware only acts on requests from this specific origin.
  2. Resolve the matched route template for the incoming request.
  3. Look up the route in `route_allowlist_registry`. If `ALLOWED_FOR_WEB_PORTAL`, proceed to `call_next(request)`. If `DENIED_FOR_WEB_PORTAL` or **absent from the registry entirely**, reject immediately with `403 FORBIDDEN` and a structured `AuthorizationError` — an unclassified route must be treated as denied, never allowed, so a newly added platform route is safe by default.
  4. Log every rejection (route, origin, timestamp) for B-04's audit trail.
- A startup-time (or CI-time) completeness check: every route registered on the FastAPI app must have a corresponding entry in `route_allowlist_registry` — fail fast (raise at app startup, or fail the CI schema-enumeration test) rather than allow an unclassified route to exist silently in production.

## 11. API Contract
Not applicable — this sub-feature adds no new endpoints; it is cross-cutting middleware over all existing endpoints.

## 12. Database Requirements
None — the allowlist is code-defined configuration, not a database-backed resource (consistent with PRD §12.5: "the allowlist configuration itself is a deployment/infrastructure artifact, not an admin-UI-editable resource").

## 13. Validation
Route-template matching must account for path parameters correctly (e.g. `DELETE /v1/sessions/{id}` must match any concrete `{id}` value, not require an exact literal-string match).

## 14. Authentication
Not applicable directly — this middleware runs origin/route classification ahead of, and independently of, each endpoint's own authentication dependency, which remains unchanged.

## 15. Authorization
This middleware itself is the authorization layer for origin-vs-route access; it raises `AuthorizationError` (403) on any non-allowlisted match, distinct from and additional to each endpoint's own family-ownership/RBAC authorization checks.

## 16. Error Handling
| Scenario | Response |
|---|---|
| Request from `account.noorheroes.com` to an allowlisted route | Passes through to normal route handling |
| Request from `account.noorheroes.com` to a denied or unclassified route | `403 FORBIDDEN`, `AuthorizationError`, logged for audit |
| Request from any other origin | Middleware passes through unmodified (out of scope for this origin-specific control) |
| New platform route added without an allowlist classification | CI-blocking failure (Task 06's completeness test), not a silent production gap |

## 17. Offline First
Not applicable (backend).

## 18. Local Data
Not applicable (backend).

## 19. Localization
Not applicable (backend).

## 20. RTL
Not applicable (backend).

## 21. Analytics
Rejection events feed B-04's audit/alerting pipeline, not a product analytics event.

## 22. Performance
Dict/hash-keyed lookup, O(1) per request; negligible overhead, evaluated only for requests actually bearing the web-portal origin header (early-exit for all other traffic).

## 23. Security
- This is the application-layer half of the two-layer (soon three-layer, once N-02 ships) defense-in-depth model — its most important property is failing closed: an unclassified route is denied, not allowed.
- The completeness check (Task 06) is what prevents this guarantee from silently decaying as the platform's route surface grows over time.

## 24. Library Requirements
No new libraries — implemented as a Starlette/FastAPI `BaseHTTPMiddleware` subclass, consistent with the existing `RateLimitMiddleware` pattern already in the codebase.

## 25. Testing
- Unit: middleware allows a request matching an `ALLOWED_FOR_WEB_PORTAL` route.
- Unit: middleware denies a request matching a `DENIED_FOR_WEB_PORTAL` route.
- Unit: middleware denies a request matching a route **absent** from the registry (fail-closed behavior — the highest-priority test in this sub-feature).
- Unit: middleware passes through unmodified for non-web-portal origins.
- Integration: full OpenAPI schema enumeration — every route returned by `export_openapi_schema.py`'s output has an explicit entry in `route_allowlist_registry` (completeness test; fails CI if any route is missing).
- Integration: B-01's gateway allowlist and B-02's application-level registry are cross-checked for consistency (same set of `ALLOWED_FOR_WEB_PORTAL` routes in both places).
- Regression: this suite re-runs on every deploy and on every PR that modifies any router's route set.

## 26. Documentation
`route_allowlist_registry.py` must be self-documenting (each entry annotated with its owning blueprint reference, matching B-01's documentation convention) so the two allowlists can be manually cross-checked as well as automatically tested.

## 27. AI Coding Agent Implementation Steps

**Task 01 — Define `route_allowlist_registry.py`**
- **Files to Create:** `route_allowlist_registry.py`.
- **Implementation Details:** Mirror B-01's finalized allowlist (post Task 02/03 scope resolutions from B-01) exactly.
- **Dependencies:** B-01 Tasks 02–04 (scope resolutions and final allowlist) must be complete first.

**Task 02 — Implement `WebPortalRouteAllowlistMiddleware`**
- **Files to Create:** `web_portal_route_allowlist.py`.
- **Implementation Details:** Origin check, route-template resolution, allow/deny/fail-closed logic per §10.

**Task 03 — Register Middleware in `main.py`**
- **Files to Modify:** `main.py`.
- **Definition of Done:** Middleware active in the stack, positioned correctly relative to `RequestIdMiddleware`/`RateLimitMiddleware`.

**Task 04 — Startup/CI Completeness Check**
- **Objective:** Ensure every registered FastAPI route has a `route_allowlist_registry` entry.
- **Files to Modify:** `classify_openapi_diff.py` (extend), or a new startup assertion.

**Task 05 — Fail-Closed Unit Tests**
- **Files to Create:** `test_web_portal_route_allowlist_middleware.py`.
- **Tests:** Allow, deny, and — critically — unclassified-route-denied cases.

**Task 06 — OpenAPI Schema Enumeration Completeness Test**
- **Files to Create:** `test_openapi_route_classification_completeness.py`.
- **Definition of Done:** CI-blocking; fails if any live route lacks a registry entry.

**Task 07 — Cross-Consistency Test Against B-01**
- **Definition of Done:** B-01's gateway allowlist and B-02's registry provably describe the same allowed-route set.

**Task 08 — Documentation**
- **Definition of Done:** Registry entries annotated with owning-blueprint citations.

## 28. Definition of Done
A second, independent, fail-closed enforcement layer exists inside the application itself, provably covering every route on the platform (via the OpenAPI completeness test) with no route ever defaulting to allowed, and provably consistent with B-01's gateway-level allowlist.

## 29. Final Verification Checklist
- [ ] Unclassified-route-denied (fail-closed) test passes
- [ ] OpenAPI schema enumeration completeness test passes and is CI-blocking
- [ ] Middleware correctly no-ops for non-web-portal origins
- [ ] Registry cross-checked for consistency against B-01's gateway allowlist, including the corrected paths (OTP prefix, consent withdraw shape, FAQ two-route split, PIN reset addition)
- [ ] `POST /v1/parent/subscription/restore` and `POST /api/v1/billing/subscribe` explicitly `DENIED_FOR_WEB_PORTAL`, not merely absent
- [ ] `GET/DELETE /v1/sessions` and the deletion-request/status routes marked `DENIED_FOR_WEB_PORTAL` (fail-closed) until their respective Task 01s resolve
- [ ] `classify_openapi_diff.py` extended to catch future unclassified routes
- [ ] No PostgreSQL/Redis credential changes
