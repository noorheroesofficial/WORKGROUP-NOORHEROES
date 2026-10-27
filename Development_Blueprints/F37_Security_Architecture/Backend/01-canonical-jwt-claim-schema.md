# B-01 — Canonical JWT Claim Schema

## 1. Feature Context
NoorHeroes is a cross-platform (FastAPI backend, KMP Android/iOS app, Next.js Admin Portal) Islamic learning app for children, built on a family-trust model: a parent authenticates, a child operates under a PIN/biometric-gated profile, and admins/scholars operate a separate elevated-trust portal. This blueprint implements the single foundational primitive every authenticated request in the platform depends on: the JWT token-claim schema. Note: this feature contains no school/institutional/madarsa-tier logic and none is to be added.

## 2. Parent Feature
F.37 — Security Architecture (Cross-Cutting). Source: `PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F37_Security_Architecture.md`.

## 3. Sub-feature
B-01 — Canonical JWT Claim Schema (Backend / FastAPI).

## 4. Objective
Define a single shared Pydantic model for JWT claims (`sub`, `family_id`, `mode`, optional `child_id`, `scopes`, `device_id`, `auth_time`, `consent_version`, `session_id`), imported and used by **every** token-issuing and token-validating code path in the backend — parent login, child-mode selection, and PIN/biometric step-up elevation alike — so no feature-specific or divergent token schema can ever be introduced.

## 5. Business Requirements
- FR-1 (JWT Authentication Flow): OTP → access/refresh token pair → device/session record → optional step-up token → optional child-mode token, all built on this one claim schema.
- FR-2 (canonical claim set, hard requirement): `sub`, `family_id`, `mode`, optional `child_id`, `scopes`, `device_id`, `auth_time`, `consent_version`, `session_id` — no other claim shape is permitted anywhere in the platform.
- Acceptance Criterion (PRD §1.9): "Given a parent authenticates, when the flow completes, then the token issued contains exactly the canonical claim set... no feature-specific variant token schema exists anywhere in the platform."
- This is the architectural origin point every other feature (A.1 onboarding, C.19 Parent PIN Gate, E.28 Admin Auth/RBAC) already assumes and builds on; this blueprint's job is to make that assumption structurally true rather than a convention.

## 6. Existing Architecture
Per `FAST-API-INSTRUCTIONS.md` (Modular Monolith, 12 bounded contexts):
- `src/noorheroes/core/security.py` — houses `create_access_token(claims: JwtClaims)`, which mints signed HS256 JWT access tokens. This is the canonical location for the shared schema.
- `src/noorheroes/core/deps.py` — houses `get_current_parent`, `get_current_child`, `get_current_admin` (JWT-authenticating FastAPI dependencies) and an RBAC-scope-verification-dependency factory. These must decode against the same schema `create_access_token` encodes.
- `identity` bounded context (§5.1) is the JWT-issuing authority per the PRD (§3.1: "Identity & Family Service").
- Routing matrix rule (`FAST-API-INSTRUCTIONS.md` §8): API routers must use `Depends(get_current_parent)` — direct JWT parsing in a router is an explicitly prohibited pattern ("Bypasses authentication security checks").

## 7. Existing Code to Reuse
- `core/security.py::create_access_token` — extend/anchor to the shared schema; do not create a parallel token-minting function.
- `core/deps.py::get_current_parent` / `get_current_child` / `get_current_admin` — update to decode against the shared schema, do not fork new dependency functions.
- `common/base_service.py`, `common/base_repository.py` — no change needed, referenced only if session persistence touches claims.
- KMP counterpart to keep in sync (read-only reference, not modified by this backend task): `core-security`'s `JwtClaimsDecoder` (`com.noorheroes.core.security.auth`), which decodes claims unverified client-side — its expected field set must match this schema exactly.

## 8. Files to Create
- `src/noorheroes/core/schemas/jwt_claims.py` — the single shared `JwtClaims` Pydantic model (or equivalent canonical location under `core/` if `core/security.py` is preferred as the single file; follow whichever the existing `core/` layout already favors for schema-vs-logic separation).
- `tests/core/test_jwt_claims_schema.py` — schema validation unit tests.
- `tests/architecture/test_single_jwt_schema.py` — the architectural/code-search test (mandatory, see §27).

## 9. Files to Modify
- `src/noorheroes/core/security.py` — `create_access_token` to accept/return the shared `JwtClaims` model exclusively.
- `src/noorheroes/core/deps.py` — `get_current_parent`, `get_current_child`, `get_current_admin`, and the RBAC-scope dependency factory to decode via the shared schema.
- Any child-mode-token-issuing code path (child-selection endpoint, likely within `identity` context) and any step-up-elevation code path (PIN/biometric confirmation endpoint) — both must construct `JwtClaims` via the shared model, not ad hoc dicts.

## 10. Backend Requirements
- `JwtClaims` is a Pydantic model (Pydantic v2 style, consistent with the rest of the schema layer) with fields: `sub: str`, `family_id: str`, `mode: Literal["parent", "child", "admin"]` (confirm exact literal set against `identity` context's existing mode semantics before finalizing — do not invent values not already used elsewhere in the codebase), `child_id: str | None = None`, `scopes: list[str]`, `device_id: str`, `auth_time: datetime`, `consent_version: str`, `session_id: str`.
- `create_access_token(claims: JwtClaims) -> str` signs the model's serialized payload; no code path constructs a JWT payload dict independently of this model.
- Decoding (`get_current_parent` et al.) deserializes the verified JWT payload directly into `JwtClaims`, rejecting (401) any payload that fails model validation (missing required field, wrong type).
- No new bounded context is introduced; this lives in `core/`, consumed by `identity` and every other context via `Depends(...)`.

## 11. KMP Requirements
Read-only alignment check, not implementation in this blueprint (K-01 and KMP's own `core-security`/`core-network` modules own the client side): confirm `JwtClaimsDecoder` in `core-security` (`com.noorheroes.core.security.auth`) expects exactly these nine fields, flag any client-side drift as a follow-up ticket rather than silently ignoring it.

## 12. NextJS Requirements
N/A for token issuance — the Admin Portal's own session model (`getDashboardSession()`, `useAdminSession()`) consumes admin-mode tokens issued via this same schema; no Admin Portal code changes are required by this specific blueprint, but its authors should be aware admin tokens must also conform.

## 13. API Contract
No new public endpoint is introduced. This blueprint changes the internal shape of tokens issued by the existing endpoints already specified in the PRD (§3.4): `POST /api/v1/auth/register`, `POST /api/v1/auth/login`, `POST /api/v1/auth/refresh`, `POST /api/v1/auth/logout`. Request/response bodies for those endpoints are unchanged by this blueprint; only the internal JWT payload shape is standardized. Do not invent new fields beyond the nine specified — if a consuming feature believes it needs an additional claim, that is out of scope here and must be raised against this canonical schema deliberately, not added silently.

## 14. Database Requirements
No new table. `parent_sessions` (owned by A.1/C.19, referenced by this document at PRD §4.2) stores `session_id`, `parent_id`, `refresh_hash`, `device_id`, `auth_time`, `consent_version`, `revoked` — field names should align with the claim names in `JwtClaims` (`session_id`, `device_id`, `auth_time`, `consent_version`) to avoid a mapping-layer mismatch. Do not modify PostgreSQL credentials or connection configuration.

## 15. Validation
- Reject `JwtClaims` construction with any required field missing or empty.
- Reject `mode` values outside the confirmed literal set.
- Reject `child_id` present when `mode != "child"` (or clarify via a model validator if child_id is legitimately allowed alongside a parent-mode token per an existing feature's design — verify against C.19 before assuming either way; do not guess).
- Reject decode of a JWT payload with extra/unexpected top-level fields beyond the nine (defensive schema strictness).

## 16. Authentication
This blueprint **is** the authentication token contract. All decoding must occur inside `get_current_parent` / `get_current_child` / `get_current_admin` (or a shared internal decode helper they all call) — never inline JWT parsing inside a router, per the explicit prohibition in `FAST-API-INSTRUCTIONS.md` §8.

## 17. Authorization
`scopes` on the decoded `JwtClaims` feeds the RBAC-scope-verification-dependency factory (`core/deps.py`); this blueprint does not implement authorization logic itself (that's B-06's domain-service re-verification and E.28's RBAC matrix) but must expose `scopes` in a shape those consumers can rely on without reinterpretation.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Token payload fails `JwtClaims` validation | 401, generic auth-failure error envelope (never leak which field failed, to avoid schema-probing) |
| Token signature invalid | 401 |
| Token expired (`auth_time` + TTL elapsed) | 401, distinct error code consumable by client for silent-refresh triggering |
| `mode` claim outside known set | 401, logged as a potential tampering/compromise signal |

## 19. Offline First
N/A — server-side schema definition. Client-side offline handling of cached claims is owned by KMP's `core-security`/`core-datastore`, out of scope here.

## 20. Local Data
N/A (backend-only blueprint).

## 21. Localization
N/A — claims are machine-readable identifiers, not user-facing strings.

## 22. RTL
N/A.

## 23. Analytics
Emit `auth_token_issued` (per PRD §1.19) whenever `create_access_token` succeeds, tagged with `mode`; do not log full claim payloads (PII-adjacent: `family_id`, `child_id`) to analytics or general logs — log only non-identifying metadata (mode, scope count, issuance timestamp).

## 24. Performance
Model validation on every request (via `get_current_parent` et al.) must remain O(1) and allocation-light — Pydantic v2's compiled validators are expected to be sufficient; no external I/O inside claim validation itself.

## 25. Security
- This is the platform's single highest-leverage schema: a bug here has platform-wide blast radius. Treat any change to `JwtClaims` as requiring the same review rigor as the PRD's "Go/No-Go" bar (§15.3): Security Engineering + Platform Architecture sign-off.
- Never log raw JWT strings.
- `sub`, `family_id`, `child_id` are effectively PII-adjacent identifiers; redact in structured logs per the existing `StructuredLoggingMiddleware` redaction pattern.

## 26. Library Requirements
Pydantic v2 (already the project's schema library per `FAST-API-INSTRUCTIONS.md`), existing JWT library already used by `core/security.py` (do not introduce a second JWT library — reuse whatever `create_access_token` currently depends on, e.g. `python-jose` or `PyJWT`; confirm the existing import before adding anything new).

## 27. Testing
- **Unit:** `JwtClaims` accepts a fully-populated valid payload; rejects missing `sub`/`family_id`/`scopes`/`device_id`/`auth_time`/`consent_version`/`session_id`; accepts `child_id=None`.
- **Unit:** `create_access_token` output decodes back into an equivalent `JwtClaims` instance (round-trip).
- **Integration:** login flow, child-mode-selection flow, and step-up-elevation flow each issue a token that independently decodes into a valid `JwtClaims`.
- **Architectural (CI-blocking):** `tests/architecture/test_single_jwt_schema.py` performs a code-search/AST scan across `src/noorheroes/` confirming no other module defines a class/dict literal used as a token-claim payload outside `JwtClaims` (e.g., no second `TypedDict`/Pydantic model with overlapping purpose). This test must fail the build if a divergent schema is introduced.
- **Negative:** decode of a tampered/extra-field payload is rejected.

## 28. Documentation
Update the backend API documentation (OpenAPI-adjacent internal docs referenced by `FAST-API-INSTRUCTIONS.md`) with a "Canonical Token Claims" section pointing at `JwtClaims` as the single source of truth, cross-referenced from `core/security.py` and `core/deps.py` docstrings.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define the Shared JwtClaims Schema**
- Task ID: B-01-T01
- Objective: Create the canonical `JwtClaims` Pydantic model.
- Why This Is Required: Every other task in this blueprint and every other feature in the platform depends on this single model existing first.
- Existing Architecture to Follow: `core/` schema conventions already used elsewhere in the codebase; Pydantic v2 style.
- Existing Files to Reuse: none yet (this is the origin point) — but check `core/security.py` for any existing partial claims dict to migrate from rather than duplicate.
- Files to Create: `src/noorheroes/core/schemas/jwt_claims.py`.
- Files to Modify: none yet.
- Implementation Details: define the nine fields per §10; add a model validator enforcing `child_id` is only set when `mode == "child"` once that rule is confirmed against C.19.
- Business Rules: FR-2's exact claim set, no more, no fewer fields.
- Validation: as in §15.
- Error Handling: raise `pydantic.ValidationError` on construction failure; caller (Task 03) maps this to a 401.
- Security: no default values that could silently under-populate a security-relevant field (e.g., no default empty `scopes` list unless explicitly correct for a specific mode).
- Performance: keep the model free of custom `__init__` overrides; rely on Pydantic's generated validators.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A at this task.
- Tests: unit tests per §27's first bullet, written in this same task.
- Documentation: docstring on the model listing each field's meaning and owning claim (`sub` = parent/admin user id, etc.).
- Dependencies: none.
- Do Not Change: do not touch `core/security.py` or `core/deps.py` yet.
- Expected Result: `JwtClaims` importable from `core.schemas.jwt_claims`, fully unit-tested in isolation.
- Definition of Done: model exists, passes its own unit tests, reviewed against PRD FR-2 field-for-field.

**Task 02 — Migrate Token Issuance to the Shared Schema**
- Task ID: B-01-T02
- Objective: Update `create_access_token` to accept and encode `JwtClaims` exclusively.
- Why This Is Required: Token issuance is the first of two halves (issuance + validation) that must agree on schema.
- Existing Architecture to Follow: `core/security.py`'s existing signing mechanism (HS256 per `FAST-API-INSTRUCTIONS.md` §2).
- Existing Files to Reuse: `core/security.py::create_access_token`.
- Files to Create: none.
- Files to Modify: `src/noorheroes/core/security.py`.
- Implementation Details: change the function signature to `create_access_token(claims: JwtClaims) -> str`; serialize via `claims.model_dump(mode="json")` (or project-consistent equivalent) before signing.
- Business Rules: no code path may pass a raw dict to the signer.
- Validation: rely on `JwtClaims` construction (Task 01) having already validated the payload; this task does not re-validate.
- Error Handling: propagate `ValidationError` upward unchanged (caller's responsibility).
- Security: confirm signing key handling is unchanged (do not touch secret-management code).
- Performance: no additional overhead beyond existing signing cost.
- Localization / RTL: N/A.
- Analytics: emit `auth_token_issued` here, tagged with `claims.mode`.
- Tests: round-trip unit test per §27.
- Documentation: update function docstring.
- Dependencies: Task 01.
- Do Not Change: signing algorithm, key rotation logic, token TTL values (out of scope for this blueprint).
- Expected Result: every internal caller of `create_access_token` now passes a `JwtClaims` instance.
- Definition of Done: function signature updated, all existing call sites updated to match (see Task 04), round-trip test passing.

**Task 03 — Migrate Token Validation Dependencies**
- Task ID: B-01-T03
- Objective: Update `get_current_parent`, `get_current_child`, `get_current_admin`, and the RBAC-scope dependency factory in `core/deps.py` to decode into `JwtClaims`.
- Why This Is Required: Validation is the second half of the issuance/validation contract; both must reference the same model.
- Existing Architecture to Follow: `core/deps.py`'s existing per-mode dependency pattern (`FAST-API-INSTRUCTIONS.md` §2).
- Existing Files to Reuse: `core/deps.py`.
- Files to Create: none.
- Files to Modify: `src/noorheroes/core/deps.py`.
- Implementation Details: decode JWT, construct `JwtClaims` from the payload (letting Pydantic validation reject malformed payloads), then branch per-mode logic (`ParentSessionContext`, `ChildSessionContext`, `AdminSessionContext`) off the validated model rather than off raw dict access.
- Business Rules: reject (401) any payload that fails `JwtClaims` validation before any mode-specific logic runs.
- Validation: as in §15.
- Error Handling: map `ValidationError`/signature-error/expiry to the 401 table in §18.
- Security: log validation failures as potential-tampering signals when the failure is schema-shape-related (not simple expiry).
- Performance: keep decode+validate on the hot request path lightweight; no synchronous DB call inside this dependency beyond what already exists.
- Localization / RTL: N/A.
- Analytics: N/A at this task (issuance-side event already covers the meaningful signal).
- Tests: integration tests per §27 (login/child-mode/step-up flows).
- Documentation: update docstrings for all three dependencies.
- Dependencies: Task 01, Task 02.
- Do Not Change: RBAC scope-checking logic itself (out of scope — only the claims-decoding step feeding it changes).
- Expected Result: all three dependencies and the scope-factory operate on `JwtClaims` instances.
- Definition of Done: integration tests passing for all three token-issuing flows.

**Task 04 — Migrate Remaining Token-Issuing Call Sites (Child-Mode, Step-Up)**
- Task ID: B-01-T04
- Objective: Update the child-mode-selection endpoint and the PIN/biometric step-up endpoint (within `identity` context) to construct `JwtClaims` via the shared model.
- Why This Is Required: FR-2 requires zero exceptions — every issuing path, not just login.
- Existing Architecture to Follow: `identity` bounded context conventions (§5.1 of `FAST-API-INSTRUCTIONS.md`).
- Existing Files to Reuse: whichever `identity` context service currently issues these two token types.
- Files to Create: none.
- Files to Modify: identified `identity` context service/router file(s) — locate via search for existing child-mode-token and step-up-token issuance logic before editing (do not guess the file path; confirm it against the actual `identity` context layout).
- Implementation Details: replace ad hoc claim construction with `JwtClaims(...)` + `create_access_token`.
- Business Rules: child-mode token must carry only child-safe `scopes` (cross-ref PRD FR-5); step-up token must carry a short TTL reflected in `auth_time` handling (cross-ref C.19, do not redefine TTL here).
- Validation: as in §15.
- Error Handling: as in §18.
- Security: confirm child-mode scopes list is the restricted set, not a copy of the parent token's full scopes.
- Performance: N/A beyond existing.
- Localization / RTL: N/A.
- Analytics: `auth_child_mode_token_issued`, `auth_step_up_token_issued` per PRD §1.19.
- Tests: integration tests confirming both flows issue schema-conformant tokens.
- Documentation: update relevant `identity` context docs.
- Dependencies: Task 01–03.
- Do Not Change: the actual PIN/biometric verification logic itself (owned by C.19), only how the resulting token is constructed.
- Expected Result: zero token-issuing code paths remain outside the shared schema.
- Definition of Done: architectural test (Task 05) passes with these paths included in scope.

**Task 05 — Architectural Test: Single-Schema Enforcement**
- Task ID: B-01-T05
- Objective: Write the CI-blocking test proving no divergent token-claim schema exists anywhere in the backend.
- Why This Is Required: PRD §5 explicitly calls for "a test confirming no other module defines its own divergent token-claim schema" as a hard requirement, not a convention.
- Existing Architecture to Follow: project's existing test/CI conventions.
- Existing Files to Reuse: none.
- Files to Create: `tests/architecture/test_single_jwt_schema.py`.
- Files to Modify: none.
- Implementation Details: AST-scan or import-graph scan of `src/noorheroes/` for any class resembling a token-claims payload (heuristic: Pydantic models/TypedDicts with 2+ field-name overlaps against `JwtClaims`'s field set, defined outside `core/schemas/jwt_claims.py`) and fail if found.
- Business Rules: zero tolerance per PRD §1.4 metrics table.
- Validation: N/A (this is the validator).
- Error Handling: test fails the build with a clear message identifying the offending file/class.
- Security: this test is itself a security control — do not allow it to be skipped/xfailed without Security Engineering sign-off per §25.
- Performance: test should run fast enough for every CI run (no full-repo deep AST walk beyond `src/noorheroes/`).
- Localization / RTL / Analytics: N/A.
- Tests: this task's deliverable is itself a test.
- Documentation: add to CI documentation as a mandatory, non-bypassable gate (per PRD §10 DevOps Requirements).
- Dependencies: Tasks 01–04 (needs the real end-state codebase to validate against).
- Do Not Change: N/A.
- Expected Result: CI fails if any future PR introduces a second claims schema.
- Definition of Done: test passes against the current codebase and is wired into CI as blocking.

## 30. Definition of Done
`JwtClaims` exists as the sole token-claims model; `create_access_token` and all three `get_current_*` dependencies use it exclusively; child-mode and step-up issuance paths use it; all unit, integration, and architectural tests pass; CI gate is blocking; documentation updated; no PostgreSQL/Redis credentials touched.

## 31. Final Verification Checklist
- [x] `JwtClaims` model matches PRD FR-2's exact nine-field set, no more, no fewer
- [x] `create_access_token` accepts only `JwtClaims`
- [x] `get_current_parent` / `get_current_child` / `get_current_admin` all decode via `JwtClaims`
- [x] Child-mode and step-up token issuance paths migrated
- [x] Architectural single-schema test passes and is CI-blocking
- [x] No raw JWT or full-claims payload appears in logs
- [x] Unit + integration test suite green
- [x] Documentation updated with the canonical schema reference
- [x] No PostgreSQL/Redis credential or connection-config changes introduced
