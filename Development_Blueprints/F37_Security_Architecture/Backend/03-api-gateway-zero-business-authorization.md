# B-03 — API Gateway Zero-Business-Authorization Architecture

## 1. Feature Context
The NoorHeroes platform's single most important architectural principle (per PRD §3.5): the API Gateway never makes a business-authorization decision. This blueprint implements and — critically — architecturally *proves* that boundary, so a gateway misconfiguration can never become a system-wide authorization bypass. No school/institutional/madarsa logic applies.

## 2. Parent Feature
F.37 — Security Architecture (Cross-Cutting).

## 3. Sub-feature
B-03 — API Gateway Zero-Business-Authorization Architecture (Backend / FastAPI + Gateway layer).

## 4. Objective
Configure the API Gateway layer to perform only network/transport-layer checks, and implement a CI-blocking architectural test confirming zero business-authorization logic exists in gateway-layer code, per PRD FR-4 and the §5 Backend AI Code-Generation Prompt item 3.

## 5. Business Requirements
- FR-4: "The API Gateway performs no business authorization decisions on its own — every domain service rechecks ownership and scope independently."
- NFR (§1.8): "Service-Layer-Only Authorization... a structural defense-in-depth principle applied uniformly."
- Acceptance Criterion §1.9: "Given a request reaches the API Gateway, when it's routed to a domain service, then the gateway has made no business-authorization decision of its own."
- Edge Case §1.10.1: a temporary gateway WAF-rule lapse must not itself cause an authorization bypass — the domain service's own check (B-06) remains authoritative regardless of gateway state.
- Success Metric §1.4: "Authorization-bypass incidents via gateway misconfiguration: 0 (hard, zero-tolerance)."

## 6. Existing Architecture
- PRD §3.1/§3.2/§3.3: the gateway sits in front of every one of the 12 bounded contexts (`identity`, `admin`, `ai_safety`, `content`, `learning`, `localization`, `media`, `notifications`, `rewards`, `subscriptions`, `habits`, `avatars` per `FAST-API-INSTRUCTIONS.md` §5) and is responsible only for TLS termination, rate limiting, WAF, bot/credential-stuffing detection, and request/correlation IDs.
- `infrastructure/` middleware layer (`FAST-API-INSTRUCTIONS.md` §4): `RequestIdMiddleware`, `StructuredLoggingMiddleware`, `RateLimitMiddleware`/`SlidingWindowRateLimiter` — these are the legitimate gateway-layer-equivalent concerns already present in-process; if the actual infrastructure gateway is a separate reverse-proxy (Nginx/Envoy per PRD §5's stack line), this blueprint's architectural test must cover both the external gateway config and this in-process middleware layer, since either could theoretically host a stray authorization check.
- B-06 (Domain-Service Independent Child-Scoped Re-Verification) is this blueprint's direct counterpart — B-03 proves the gateway does *not* authorize, B-06 proves the domain service *does*.

## 7. Existing Code to Reuse
- `infrastructure/middleware/rate_limit.py` — confirm this file contains only rate-limiting logic, no ownership/scope checks, as part of this blueprint's audit.
- `RequestIdMiddleware`, `StructuredLoggingMiddleware` — audit for scope creep, do not rewrite unless a violation is found.

## 8. Files to Create
- `tests/architecture/test_gateway_zero_authorization.py` — the mandatory CI-blocking architectural test.
- `docs/architecture/gateway-defense-in-depth.md` — the diagram/documentation deliverable (§9 Admin Prompt-adjacent, but this is a backend/platform doc, not an admin UI).

## 9. Files to Modify
- Gateway configuration files (Nginx/Envoy config or equivalent, wherever the project's actual gateway config lives — locate via the existing infra/deploy directory before assuming a path; do not invent a config file location) — audit and, if any business-logic rule is found (e.g., a path-based rule that inspects a `child_id` or ownership claim), remove it and relocate the check to the owning domain service.
- Any middleware currently registered before domain-service routing that inspects request bodies/params for anything beyond rate-limit keys, WAF signatures, or correlation IDs.

## 10. Backend Requirements
- Gateway/edge layer responsibilities, exhaustively: TLS termination; rate limiting at device/IP/phone/account dimensions (delegates to B-07's configuration); WAF rule evaluation; bot/credential-stuffing detection; request/correlation-ID assignment (`RequestIdMiddleware`).
- Gateway/edge layer must **never**: inspect JWT claims for ownership/scope decisions, query the database for family/child relationships, or make any allow/deny decision based on *who* is asking versus *what* they're asking for beyond raw rate/WAF signals.
- The architectural test scans `src/noorheroes/infrastructure/` (and any actual external gateway config, if version-controlled in this repo) for patterns indicating business-authorization logic: DB queries, references to `family_id`/`child_id`/`scopes` ownership comparisons, or calls into domain-context service functions.

## 11. KMP Requirements
N/A — this is a pure backend/infrastructure boundary; the client is unaware of the gateway/domain-service split.

## 12. NextJS Requirements
N/A — same reasoning; the Admin Portal calls the same gateway-fronted API surface as any other client.

## 13. API Contract
No new endpoint. This blueprint constrains *where* authorization logic may live for every existing endpoint across all 12 bounded contexts; it does not change any request/response shape.

## 14. Database Requirements
None introduced. The architectural test must confirm the gateway/middleware layer performs **no** database queries related to ownership/scope (a gateway making a DB call for authorization purposes is itself a violation of this principle, even if the *answer* it computes happens to be correct).

## 15. Validation
N/A in the traditional sense — this blueprint's "validation" is the architectural test itself validating the codebase's structure.

## 16. Authentication
The gateway may validate that a request carries *a* token (structural presence check, e.g., "is there a Bearer header") but must not decode/interpret its claims for authorization purposes — that decoding-for-authorization happens exclusively in `core/deps.py`'s `get_current_*` dependencies (B-01) and each domain service's own re-check (B-06).

## 17. Authorization
This blueprint is the negative space of authorization — proving where it must *not* occur. Positive authorization enforcement is B-06's responsibility entirely.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Gateway-layer rate limit / WAF trip | Gateway itself returns 429/403 (legitimate gateway-layer response) |
| Gateway-layer code found performing a business-authorization check (test failure) | CI build fails, PR blocked |
| Simulated gateway-layer gap (e.g., WAF rule temporarily lapses) | Request still correctly rejected by the domain service's own re-check (validated via B-06's simulated-bypass test, cross-referenced here) |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
N/A.

## 22. RTL
N/A.

## 23. Analytics
Emit `authorization_gateway_passthrough` (internal, per PRD §1.19) confirming no gateway-layer business-authorization decision was made for a given request — useful as a continuous production signal, not just a CI-time test.

## 24. Performance
Keeping the gateway free of business logic is itself a performance win (no DB round-trip at the edge); this blueprint should not introduce any new latency, only remove/prevent scope creep.

## 25. Security
- This is one of the two highest-priority guarantees in the entire F.37 deliverable per PRD §5 ("items 3... treated as the two highest-priority guarantees in this entire deliverable").
- Any confirmed violation (business-authorization logic found at the gateway layer) is a P0 rollback trigger per PRD §15.2.

## 26. Library Requirements
No new library. If the actual external gateway is Nginx/Envoy (PRD §5 stack line), no application-level library is needed for this blueprint's backend half; the architectural test is pure Python/AST tooling already available to the project's test suite.

## 27. Testing
- **Architectural (CI-blocking, mandatory):** `tests/architecture/test_gateway_zero_authorization.py` — code-search/dependency-graph scan of `infrastructure/` (and any in-repo gateway config) confirming zero references to ownership/scope-comparison logic or domain-context service calls.
- **Manual/config audit:** one-time audit of the actual external gateway configuration (Nginx/Envoy rules) for any embedded business logic, documented as part of this blueprint's completion even if not automatable in CI.
- **Regression:** re-run the architectural test on every release touching gateway configuration or `infrastructure/middleware/`.
- **Cross-referenced simulation test:** B-06's "simulated gateway bypass" test is the complementary proof that even a gateway failure doesn't create a real bypass — do not duplicate that test here, only reference it.

## 28. Documentation
`docs/architecture/gateway-defense-in-depth.md` — the Mermaid diagram from PRD §3.2, plus a plain-language explanation of "what belongs at the gateway vs. what belongs in the domain service," intended as the onboarding reference for any future engineer tempted to add a convenience check at the gateway layer.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Audit Existing Gateway/Middleware Layer**
- Task ID: B-03-T01
- Objective: Manually and programmatically inventory everything currently running at the gateway/edge and in `infrastructure/middleware/`.
- Why This Is Required: Cannot write a meaningful architectural test without first knowing the current actual state — do not assume compliance, verify it.
- Existing Architecture to Follow: `FAST-API-INSTRUCTIONS.md` §4 middleware list.
- Existing Files to Reuse: `infrastructure/middleware/rate_limit.py`, `RequestIdMiddleware`, `StructuredLoggingMiddleware` source.
- Files to Create: none yet (audit notes can live in the Task 03 documentation deliverable).
- Files to Modify: none yet.
- Implementation Details: read every middleware registered in `main.py`'s app lifespan/middleware stack; read the actual external gateway config if present in-repo.
- Business Rules: N/A (audit only).
- Validation: N/A.
- Error Handling: N/A.
- Security: flag, don't yet fix, anything suspicious.
- Performance: N/A.
- Localization / RTL / Analytics: N/A.
- Tests: none yet.
- Documentation: audit notes feed Task 03.
- Dependencies: none.
- Do Not Change: nothing yet — this is read-only.
- Expected Result: a clear inventory of what currently runs at the gateway/middleware layer.
- Definition of Done: inventory complete, any violations flagged for Task 02.

**Task 02 — Remediate Any Found Violations**
- Task ID: B-03-T02
- Objective: If Task 01 found any business-authorization logic at the gateway/middleware layer, remove it and relocate the equivalent check into the owning domain service (coordinating with B-06).
- Why This Is Required: The architectural test (Task 04) will fail otherwise, and more importantly the actual security guarantee would be false.
- Existing Architecture to Follow: domain-service pattern for wherever the check is relocated.
- Existing Files to Reuse: N/A, case-by-case.
- Files to Create: none prescribed — depends entirely on audit findings.
- Files to Modify: whichever file(s) Task 01 flagged.
- Implementation Details: case-by-case; if nothing was found, this task is a no-op and should be explicitly marked "no violations found" rather than skipped silently.
- Business Rules: the relocated check must still function identically from the end-user's perspective (no behavior regression) — only its *location* changes.
- Validation: as owned by wherever it's relocated to.
- Error Handling: preserve existing error responses for the affected endpoint(s).
- Security: this is itself a security fix if violations exist.
- Performance: N/A.
- Localization / RTL / Analytics: N/A.
- Tests: add/update tests for the relocated logic at its new home.
- Documentation: note the remediation in Task 03's doc.
- Dependencies: Task 01.
- Do Not Change: nothing outside the flagged violation's scope.
- Expected Result: gateway/middleware layer is clean, or confirmed already clean.
- Definition of Done: no remaining violations per a re-run of Task 01's audit.

**Task 03 — Write the Defense-in-Depth Documentation**
- Task ID: B-03-T03
- Objective: Produce `docs/architecture/gateway-defense-in-depth.md`.
- Why This Is Required: Prevents future scope creep by making the boundary explicit and discoverable.
- Existing Architecture to Follow: PRD §3.2 Mermaid diagram as the visual basis.
- Existing Files to Reuse: none.
- Files to Create: `docs/architecture/gateway-defense-in-depth.md`.
- Files to Modify: none.
- Implementation Details: include the Mermaid diagram, a "belongs at gateway" vs. "belongs at domain service" checklist, and a pointer to the Task 04 test as the enforcement mechanism.
- Business Rules: N/A.
- Validation / Error Handling: N/A.
- Security: N/A.
- Performance: N/A.
- Localization / RTL / Analytics: N/A.
- Tests: N/A.
- Documentation: this task's entire deliverable.
- Dependencies: Task 01, Task 02.
- Do Not Change: N/A.
- Expected Result: living architectural reference doc.
- Definition of Done: doc merged and linked from the `identity`/`infrastructure` context READMEs.

**Task 04 — Write the CI-Blocking Architectural Test**
- Task ID: B-03-T04
- Objective: Implement `tests/architecture/test_gateway_zero_authorization.py`.
- Why This Is Required: This is the actual, durable enforcement mechanism — documentation and one-time audits are not sufficient on their own (per PRD §5, this must be a code-search/dependency-graph check, CI-blocking).
- Existing Architecture to Follow: project's existing test/CI tooling (AST scanning, import-graph analysis — use whatever static-analysis approach the codebase already favors; do not introduce a new heavyweight static-analysis dependency without checking for an existing one first).
- Existing Files to Reuse: none.
- Files to Create: `tests/architecture/test_gateway_zero_authorization.py`.
- Files to Modify: CI pipeline config to mark this test as blocking (per PRD §10: "mandatory, non-bypassable CI gates").
- Implementation Details: scan `infrastructure/` for DB session usage, `family_id`/`child_id`/`scopes` comparison patterns, or imports from domain-context service modules; fail with a clear message naming the offending file/line.
- Business Rules: zero tolerance (§1.4 metric).
- Validation: this test is the validator.
- Error Handling: clear, actionable failure message.
- Security: this test itself must not be skippable/xfailed without Security Engineering sign-off.
- Performance: fast enough to run on every CI invocation.
- Localization / RTL / Analytics: N/A.
- Tests: this task's deliverable is a test.
- Documentation: link from Task 03's doc.
- Dependencies: Task 01, Task 02 (needs the remediated, clean codebase to validate against).
- Do Not Change: N/A.
- Expected Result: any future PR introducing gateway-layer business authorization fails CI immediately.
- Definition of Done: test passes against current codebase, wired as a blocking CI gate.

## 30. Definition of Done
Gateway/middleware layer audited and confirmed (or remediated) to contain zero business-authorization logic; defense-in-depth documentation published; CI-blocking architectural test in place and passing; cross-referenced against B-06's simulated-bypass test.

## 31. Final Verification Checklist
- [ ] Gateway/middleware layer performs only TLS, rate limiting, WAF, bot detection, correlation IDs
- [ ] Zero DB queries or ownership/scope comparisons at the gateway/middleware layer
- [ ] Architectural CI-blocking test in place and passing
- [ ] Defense-in-depth documentation published with the PRD §3.2 diagram
- [ ] Cross-reference to B-06's simulated-gateway-bypass test confirmed valid
- [ ] `authorization_gateway_passthrough` event emitted in production for ongoing signal
- [ ] No PostgreSQL/Redis credential changes introduced
