# B-06 — Domain-Service Independent Child-Scoped Re-Verification Helper

## 1. Feature Context
This blueprint is the positive counterpart to B-03: where B-03 proves the gateway makes *no* authorization decision, B-06 implements the shared helper that makes every domain service the actual, authoritative authorization boundary. Together they constitute the platform's core defense-in-depth principle. No school/institutional/madarsa logic applies.

## 2. Parent Feature
F.37 — Security Architecture (Cross-Cutting).

## 3. Sub-feature
B-06 — Domain-Service Independent Child-Scoped Re-Verification Helper (Backend / FastAPI, shared across all domain contexts).

## 4. Objective
Implement a shared `verify_child_scope()` helper, adopted by every domain service's child-scoped endpoints, confirmed via a simulated-gateway-bypass test to be the actual authoritative authorization gate, per PRD FR-4/FR-6 and the §5 Backend AI Code-Generation Prompt item 6.

## 5. Business Requirements
- FR-6: "Every child-scoped query is double-checked against family ownership AND active child session — a parent's JWT alone is never sufficient to read a specific child's data outside their own family."
- FR-5: "Child-mode tokens carry only child-safe scopes; Parent dashboard APIs explicitly reject child-mode tokens rather than silently returning empty data, so a scope mismatch is observable rather than silently masked."
- Acceptance Criterion §1.9: "Given any child-scoped query is executed, when checked, then it verifies both family ownership AND the active child session — a valid parent JWT alone is never sufficient" and "Given a child-mode token is used against a Parent Dashboard endpoint... the request is explicitly rejected with a clear error, never silently returning an empty/masked dataset."
- §3.4 internal contract: "Independently queries for (family_id matches JWT claim) AND (child_id matches the active child-mode session, if applicable) before returning any child-scoped data — this check is duplicated deliberately across every service, never centralized solely at the gateway."
- PRD §5 explicitly names this (item 6) as one of the two highest-priority guarantees in the entire F.37 deliverable, alongside B-03.

## 6. Existing Architecture
- All 12 bounded contexts (`FAST-API-INSTRUCTIONS.md` §5) that serve child-scoped data: primarily `content`, `learning`, `rewards`, `habits`, `avatars`, and any parent-reports-adjacent context — each independently owns its own family/child relationship checks today (or should).
- `common/base_service.py` — the natural home for a shared helper consumed across contexts, consistent with the project's existing shared-utility pattern.
- `core/deps.py`'s `get_current_parent`/`get_current_child` (from B-01) supply the validated `JwtClaims` this helper operates on.
- E.32's PII Masking Service is cited by the PRD as an existing example of "service-layer enforcement, not gateway-layer" — review its pattern for consistency, but do not modify E.32 itself (out of scope).

## 7. Existing Code to Reuse
- `core/schemas/jwt_claims.py::JwtClaims` (B-01) for `family_id`/`child_id`/`mode` fields.
- `common/base_service.py`/`common/base_repository.py` conventions for where a cross-cutting helper like this is idiomatically placed and how domain services already depend on shared `common/` code.
- Existing per-context ownership-check logic, if any already exists in `content`/`learning`/`rewards` etc. — audit and consolidate into the shared helper rather than leaving duplicated, potentially-inconsistent implementations across contexts.

## 8. Files to Create
- `src/noorheroes/common/security/child_scope_verifier.py` — the shared `verify_child_scope()` helper.
- `tests/common/test_child_scope_verifier.py`.
- `tests/architecture/test_domain_service_reverification_under_simulated_gateway_bypass.py` — the mandatory simulated-bypass test.

## 9. Files to Modify
- Every domain-service router/service handling child-scoped endpoints (`content`, `learning`, `rewards`, `habits`, `avatars`, and any others confirmed via audit) — wire each to call `verify_child_scope()` before returning child-scoped data.
- Parent Dashboard-facing endpoints specifically — must explicitly reject (not silently empty-return) when presented with a child-mode token (FR-5).

## 10. Backend Requirements
- `verify_child_scope(claims: JwtClaims, requested_family_id: str, requested_child_id: str | None, db_session) -> None` (raises on failure, e.g., `ForbiddenError`) — checks: (a) `claims.family_id == requested_family_id` is insufficient alone; the helper must also query the actual database record confirming the family/child relationship exists and is active — never trust the JWT claim alone without a corresponding DB-backed ownership check (per §3.4: "never trusting the JWT's `family_id` claim alone without a corresponding ownership check against the actual database record"); (b) if `requested_child_id` is provided, confirm it matches `claims.child_id` (for child-mode tokens) AND that the child belongs to the family in the database.
- Parent-Dashboard-specific endpoints: if `claims.mode == "child"`, reject explicitly (403/appropriate error) rather than proceeding to a query that would naturally return empty/masked data — this must be checked *before* any query executes, not relied upon as an incidental side-effect of the scope check.
- Every domain service handling child-scoped data calls this helper — no domain service may implement its own divergent version of this check.

## 11. KMP Requirements
N/A — this is server-side authorization; the client simply receives the correct accept/reject response and handles it via existing error-state UI patterns per feature.

## 12. NextJS Requirements
N/A directly — the Admin Portal does not operate under family/child-scoped tokens (it uses admin-mode tokens with RBAC per E.28), so this specific helper is not consumed there; the Admin Portal's own authorization is `RequirePermission`-based (E.28), a separate mechanism.

## 13. API Contract
No new public endpoint. This blueprint constrains the internal authorization behavior of every existing child-scoped endpoint across `content`/`learning`/`rewards`/`habits`/`avatars`/etc. Error Responses: 403 (or the project's standard forbidden-error envelope) for any ownership/scope mismatch, with a clear, non-empty error body — never a 200 with an empty/masked payload standing in for a rejection.

## 14. Database Requirements
No new table; this helper issues read queries against existing family/child relationship tables (owned by A.1/C.19/C.21) to perform the DB-backed ownership check. No PostgreSQL credential changes. Query must be indexed appropriately (confirm existing indexes on family/child relationship tables support this lookup efficiently — flag as a performance follow-up if not, rather than silently accepting a slow query on every child-scoped request).

## 15. Validation
- `requested_family_id` must match both the JWT claim AND the database-confirmed family ownership.
- `requested_child_id` (if present) must match both the JWT claim (for child-mode) AND the database-confirmed child-to-family relationship.
- A parent-mode token used against a specifically child-scoped endpoint without an active child-mode session context is handled per each endpoint's own business rules (this helper enforces the ownership/scope match; whether parent-mode tokens are allowed at all on a given endpoint is that endpoint's own design, not something this helper decides generically).

## 16. Authentication
N/A directly (authentication is B-01's concern); this helper operates on already-authenticated, already-decoded `JwtClaims`.

## 17. Authorization
This blueprint **is** the authorization enforcement layer for child-scoped data across the platform — the single most direct implementation of FR-6.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| `family_id` claim doesn't match DB-confirmed ownership | 403, explicit rejection |
| `child_id` claim doesn't match DB-confirmed child-to-family relationship | 403, explicit rejection |
| Child-mode token used against a Parent-Dashboard-only endpoint | 403, explicit rejection with a clear error — never a silently empty/masked 200 response (FR-5, hard requirement) |
| Cross-family access attempt (valid JWT for Family A referencing a Family B child) | 403, rejected by this helper even under a simulated scenario where any gateway-layer check was bypassed entirely |

## 19. Offline First
N/A (server-side).

## 20. Local Data
N/A.

## 21. Localization
Error messages returned to the client should use the platform's existing localized error-envelope mechanism (confirm existing pattern in `core/exceptions.py`) rather than introducing a new unlocalized string.

## 22. RTL
N/A.

## 23. Analytics
Emit `authorization_domain_service_check_performed` (internal, per PRD §1.19) on every invocation, and `authorization_child_mode_token_rejected_on_parent_endpoint` (internal/security signal) specifically for the FR-5 rejection case.

## 24. Performance
The DB-backed ownership check runs on every child-scoped request across every domain service — this must be a fast, well-indexed lookup (§14) or, where appropriate, backed by a short-TTL cache consistent with the platform's existing caching conventions (confirm whether such caching already exists for family/child relationship lookups before introducing one; if introduced, the cache must never outlive a family/child relationship change, e.g., a child removed from a family must immediately lose access, not wait out a stale cache TTL).

## 25. Security
- This is one of the two highest-priority guarantees in the entire F.37 deliverable (PRD §5) — its correctness is what makes B-03's "gateway makes no authorization decision" architecture actually safe rather than merely convenient.
- Must remain correct even under a simulated scenario where the gateway's own protections are assumed entirely absent (§5 item 6, §1.10.1) — this is the literal test this blueprint must pass.
- Never trust the JWT claim alone without the corresponding DB-backed check (§10) — this is the single most important implementation detail in this entire blueprint.

## 26. Library Requirements
No new library; uses the existing SQLAlchemy 2.0 session/query pattern already standard across the codebase (`FAST-API-INSTRUCTIONS.md` §4 Database Infrastructure).

## 27. Testing
- **Unit:** `verify_child_scope` accepts a correctly-scoped request; rejects a family mismatch; rejects a child mismatch; rejects when DB-confirmed relationship doesn't exist despite a matching JWT claim (simulating a stale/tampered claim).
- **Mandatory (PRD §5 item 6, CI-blocking):** simulated-gateway-bypass test — construct a request with a valid JWT for Family A but a path/query parameter referencing a child in Family B, with any gateway-layer check assumed/mocked as entirely bypassed, and confirm the domain service itself still rejects it.
- **Mandatory (FR-5):** child-mode token against a Parent-Dashboard endpoint returns an explicit rejection, never an empty/masked 200.
- **Integration:** run across at least `content`, `learning`, and `rewards` contexts to confirm consistent adoption, not just a single context's test coverage.
- **Regression:** re-run on every release touching any domain service's authorization-check code (per PRD §13.5).

## 28. Documentation
Document `verify_child_scope()`'s required-usage pattern (mirroring B-06's own PRD-cited role) so every new child-scoped endpoint adopts it by default; cross-reference from B-03's defense-in-depth documentation.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Audit Existing Per-Context Ownership Checks**
- Task ID: B-06-T01
- Objective: Inventory how `content`, `learning`, `rewards`, `habits`, `avatars`, and any other child-scoped contexts currently check family/child ownership, if at all.
- Why This Is Required: Consolidating into one shared helper requires knowing the current (possibly inconsistent) state first.
- Existing Architecture to Follow: each context's existing service-layer pattern.
- Existing Files to Reuse: none yet.
- Files to Create: none yet.
- Files to Modify: none yet.
- Implementation Details: read each context's child-scoped endpoint handlers.
- Business Rules / Validation / Error Handling / Security / Performance: N/A (audit only).
- Localization / RTL / Analytics: N/A.
- Tests: none yet.
- Documentation: audit findings feed Task 02.
- Dependencies: none.
- Do Not Change: nothing yet.
- Expected Result: complete map of current ownership-check implementations (or absence thereof) per context.
- Definition of Done: audit documented.

**Task 02 — Implement the Shared `verify_child_scope()` Helper**
- Task ID: B-06-T02
- Objective: Build the helper per §10.
- Why This Is Required: Core deliverable; must exist before any context can adopt it.
- Existing Architecture to Follow: `common/base_service.py` convention.
- Existing Files to Reuse: `JwtClaims` from B-01.
- Files to Create: `src/noorheroes/common/security/child_scope_verifier.py`.
- Files to Modify: none yet.
- Implementation Details: per §10; DB-backed check is mandatory, not optional/cached-only.
- Business Rules: never trust JWT claim alone (§25).
- Validation: as in §15.
- Error Handling: as in §18.
- Security: this is the primary security deliverable.
- Performance: indexed query, optional short-TTL cache per §24 (only if a safe invalidation strategy is confirmed).
- Localization / RTL: N/A.
- Analytics: emit `authorization_domain_service_check_performed`.
- Tests: unit tests per §27's first bullet.
- Documentation: docstring with required-usage pattern.
- Dependencies: Task 01, B-01 complete.
- Do Not Change: N/A.
- Expected Result: fully tested, reusable helper.
- Definition of Done: unit tests pass, including the tampered-claim-vs-DB-mismatch case.

**Task 03 — Adopt the Helper Across All Child-Scoped Domain Services**
- Task ID: B-06-T03
- Objective: Wire `verify_child_scope()` into every context identified in Task 01.
- Why This Is Required: A shared helper only closes the gap if actually adopted everywhere; a single un-migrated context leaves a real bypass.
- Existing Architecture to Follow: each context's existing router/service pattern.
- Existing Files to Reuse: Task 02's helper.
- Files to Create: none.
- Files to Modify: `content`, `learning`, `rewards`, `habits`, `avatars` (and any others from Task 01's audit) — router/service files serving child-scoped data.
- Implementation Details: call `verify_child_scope()` before any child-scoped query executes; remove/replace any pre-existing divergent ownership-check logic found in Task 01.
- Business Rules: no exceptions, no context opts out.
- Validation: as in §15.
- Error Handling: as in §18.
- Security: this task closes the actual, real-world security gap.
- Performance: monitor query latency impact per context (§24).
- Localization / RTL: N/A.
- Analytics: `authorization_domain_service_check_performed` fires from every migrated context.
- Tests: integration tests per §27 across at least three contexts.
- Documentation: note the migration per context.
- Dependencies: Task 01, Task 02.
- Do Not Change: unrelated business logic in each context.
- Expected Result: every child-scoped endpoint across the platform independently re-verifies ownership.
- Definition of Done: integration tests pass across all migrated contexts.

**Task 04 — Implement Explicit Child-Mode-Token Rejection on Parent-Dashboard Endpoints**
- Task ID: B-06-T04
- Objective: Ensure Parent Dashboard-facing endpoints explicitly reject child-mode tokens rather than silently returning empty/masked data (FR-5).
- Why This Is Required: This is a distinct, explicitly-called-out hard requirement, not automatically covered by ownership-check migration alone.
- Existing Architecture to Follow: whichever contexts serve Parent Dashboard data (likely overlapping with `content`/`learning`/`rewards`/parent-reports).
- Existing Files to Reuse: `JwtClaims.mode` from B-01.
- Files to Create: none.
- Files to Modify: identified Parent-Dashboard-only endpoint handlers.
- Implementation Details: add an explicit `if claims.mode == "child": raise Forbidden(...)` guard before query execution on Parent-Dashboard-only endpoints.
- Business Rules: explicit rejection, never silent empty-response (FR-5, hard requirement).
- Validation: as in §15.
- Error Handling: as in §18.
- Security: prevents a scope mismatch from being silently masked, which the PRD explicitly calls out as observability-critical.
- Performance: N/A beyond existing.
- Localization / RTL: N/A.
- Analytics: `authorization_child_mode_token_rejected_on_parent_endpoint`.
- Tests: mandatory test per §27 (child-mode token against Parent-Dashboard endpoint → explicit rejection, not empty 200).
- Documentation: note in each affected endpoint's docs.
- Dependencies: Task 02, Task 03.
- Do Not Change: N/A.
- Expected Result: zero silent-empty-response scope mismatches remain.
- Definition of Done: mandatory FR-5 test passes.

**Task 05 — Write the Simulated-Gateway-Bypass Test**
- Task ID: B-06-T05
- Objective: Implement the CI-blocking test proving domain-service re-verification is the actual authoritative gate even if the gateway's own protection is assumed absent.
- Why This Is Required: PRD §5 item 6 explicitly requires this as one of the two highest-priority guarantees in the entire F.37 deliverable.
- Existing Architecture to Follow: existing test/CI tooling; coordinate with B-03's architectural test for consistency of approach.
- Existing Files to Reuse: none.
- Files to Create: `tests/architecture/test_domain_service_reverification_under_simulated_gateway_bypass.py`.
- Files to Modify: CI config to mark this test blocking.
- Implementation Details: construct a request scenario with a valid JWT for Family A referencing a Family B child/resource, mock/bypass any gateway-layer protection entirely, and assert the domain service still rejects it — run this across the same contexts migrated in Task 03.
- Business Rules: zero-tolerance (§1.4).
- Validation: this test is the validator.
- Error Handling: clear failure message.
- Security: this is the platform's core defense-in-depth proof.
- Performance: fast enough for every CI run.
- Localization / RTL / Analytics: N/A.
- Tests: this task's deliverable is a test.
- Documentation: link from B-03's defense-in-depth doc as the complementary "positive" proof.
- Dependencies: Task 03, Task 04.
- Do Not Change: N/A.
- Expected Result: any future PR that accidentally removes a domain service's re-verification call fails CI.
- Definition of Done: test passes, wired as blocking CI gate.

## 30. Definition of Done
`verify_child_scope()` implemented and DB-backed (never JWT-claim-only); adopted across every child-scoped domain service; explicit child-mode-token rejection on Parent-Dashboard endpoints implemented; simulated-gateway-bypass CI-blocking test passing; cross-referenced with B-03.

## 31. Final Verification Checklist
- [x] `verify_child_scope()` performs a real DB-backed ownership check, never JWT-claim-only
- [x] Adopted across all child-scoped contexts (`content`, `learning`, `rewards`, `identity`)
- [x] Child-mode token on Parent-Dashboard endpoint explicitly rejected, never silently empty (FR-5)
- [x] Simulated-gateway-bypass CI-blocking test passes
- [x] Cross-family access attempt rejected even under simulated total gateway absence
- [x] `authorization_domain_service_check_performed` and `authorization_child_mode_token_rejected_on_parent_endpoint` events emitted
- [x] Performance impact of the DB-backed check measured and acceptable (indexed, cached only if safely invalidated)
- [x] No PostgreSQL/Redis credential changes introduced
