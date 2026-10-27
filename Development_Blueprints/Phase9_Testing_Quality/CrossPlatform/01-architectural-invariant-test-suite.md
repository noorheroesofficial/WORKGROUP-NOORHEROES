# Phase 9 — Consolidated Architectural-Invariant Test Suite (CI-Blocking)

## 0. Document Metadata

| Field | Value |
|---|---|
| Phase | Phase 9 — Testing & Quality Hardening (Cross-Platform) |
| Blueprint ID | Phase9_Testing_Quality.CrossPlatform.01 |
| Surface | Backend (Python/FastAPI) — the suite itself is backend-only; it is *consumed* by the cross-platform CI pipeline |
| Depends on | Phase 2 F.37 Security Architecture, all nine backend blueprints (`Development_Blueprints/F37_Security_Architecture/Backend/01`–`09`) — **already fully implemented**, per `FAST-API-INSTRUCTIONS.md` |
| Populates | Phase 1 CI pipeline stage 6, "Architectural invariant tests" placeholder job (`NoorHeroes_Final_Development_Prompt.md` §6, stage 6) |
| Status of underlying code | Complete. Status of this test suite | **Not yet built — this document specifies it in full.** |

---

## 1. Objective and Purpose

NoorHeroes' entire security posture rests on five specific, named architectural guarantees, each already implemented by an F.37 backend blueprint (B-01, B-03, B-04, B-05, B-06). Each of those blueprints already specifies its own *local* unit/integration tests (e.g., B-04's "malformed stored hash returns `False`, never raises"). This document does **not** duplicate those local tests. Its job is narrower and more critical:

> Consolidate the five specific, PRD-named **architectural invariants** — the structural, whole-codebase guarantees that no unit test can catch because they are about *where code is allowed to live and what order it is allowed to run in*, not what a single function returns — into **one single, CI-blocking pytest suite** that runs as its own required, separately-named status check (`NoorHeroes_Final_Development_Prompt.md` §6, stage 6), per §5's "Architectural (CI-blocking, non-negotiable per F.37)" test-type row.

The five invariants, verbatim from `NoorHeroes_Final_Development_Prompt.md` §5 and cross-referenced against their owning blueprints:

1. **gateway-zero-business-authorization** (owns: B-03) — the API gateway/`infrastructure/` middleware layer contains zero business-authorization logic.
2. **domain-service child-scoped-reverification** (owns: B-06) — every child-scoped domain service independently re-verifies family ownership + active child session, and this survives a simulated total gateway bypass.
3. **JWT-claim-schema conformance** (owns: B-01) — `JwtClaims` in `core/schemas/jwt_claims.py` is the sole token-claim schema in the codebase; no divergent shape exists.
4. **credential-hashing-is-not-fast-hash** (owns: B-04) — no fast general-purpose hash function (`hashlib.sha256`, `md5`, etc.) appears anywhere in the credential-storage code path.
5. **upload-pipeline-step-ordering** (owns: B-05) — no asset can reach transcode/child-delivery storage without having passed all 11 pipeline steps, strictly in order, regardless of upload source.

**Why this must be one suite, not five scattered files living inside each blueprint's own test tree:** per `NoorHeroes_Final_Development_Prompt.md` §6 stage 6, CI must run "an explicit, separately-named, required-status-check job so a failure here is unmissable in the PR UI, distinct from a generic 'tests failed'." A single `tests/architectural/` package with a dedicated pytest marker (`@pytest.mark.architectural`) and a dedicated CI job (`architectural-invariants`) is the only way to get that unmissable, unified signal — five independent test files scattered under `tests/core/`, `tests/media/`, etc. would each need separate CI wiring and could each be silently skipped independently. This blueprint's job is that consolidation, not re-implementing logic B-01–B-06 already built.

---

## 2. Scope and Requirements

### 2.1 In scope
- A new top-level test package: `backend/tests/architectural/` (five test modules + shared fixtures/helpers).
- A dedicated pytest marker (`architectural`) registered in `pyproject.toml`/`pytest.ini`.
- A dedicated, required-status-check CI job (`architectural-invariants`) in the backend's GitHub Actions workflow, positioned as CI stage 6 per `NoorHeroes_Final_Development_Prompt.md` §6.
- Reusable AST/static-analysis scanning helpers, shared by the four invariants that need static analysis (gateway-authz, JWT-schema, credential-hashing, and partially upload-ordering), so the four static scans don't each hand-roll their own AST walker.
- Reusable simulated-gateway-bypass request fixtures for the domain-service-reverification invariant.
- A documented, explicit **non-bypass policy**: this suite may never be marked `xfail`, `skip`, or excluded from a CI run without a recorded Security Engineering sign-off (per each source blueprint's own §25 "Security" section, e.g., B-03 §27: "this test itself must not be skippable/xfailed without Security Engineering sign-off").

### 2.2 Out of scope (already exists, do not re-build)
- The underlying implementations: `JwtClaims`, `create_access_token`, `get_current_parent/child/admin`, `verify_child_scope()`, `hash_credential`/`verify_credential`, `run_upload_pipeline()`, `RateLimitMiddleware` — all already built per Phase 2/F.37.
- Each blueprint's own local unit/integration test files (e.g., `tests/core/test_jwt_claims_schema.py`, `tests/common/test_credential_hasher.py`, `tests/common/test_child_scope_verifier.py`, `tests/media/test_upload_pipeline_source_agnostic.py`) — these continue to exist and run under the normal "Unit tests"/"Integration tests" CI stages (stages 4–5), not this suite.
- Any individual blueprint's own architectural test file if one already physically exists on disk from that blueprint's own implementation work (e.g., B-03's `tests/architecture/test_gateway_zero_authorization.py`, B-01's `tests/architecture/test_single_jwt_schema.py`, B-04's `tests/architecture/test_no_fast_hash_in_credential_path.py`, B-06's `tests/architecture/test_domain_service_reverification_under_simulated_gateway_bypass.py`, B-05's `tests/media/test_upload_pipeline_ordering.py`). **This blueprint's job is to consolidate these into the canonical `tests/architectural/` package** (see §5 folder structure and §13 development steps for the exact migration approach — rename/move, do not duplicate).
- Rate limiting invariants (B-07), incident-response/backup-restore testing (B-08), and pentest-finding tracking (B-09) — not part of the named five-invariant list in §5's Architectural test-type row; they have their own testing concerns elsewhere in Phase 9 and are not this document's responsibility.
- KMP's `core-security` architectural scan (F37/KMP/01) and the Admin Portal's Playwright RBAC-boundary tests — separate platforms, separate CI jobs, explicitly out of scope per `NoorHeroes_Final_Development_Prompt.md` §5's table (this document covers only the "Backend" column's Architectural row).

### 2.3 Non-functional requirements
- The whole suite must complete in well under a minute on CI hardware (per each source blueprint's own performance requirement, e.g., B-01 §27: "test should run fast enough for every CI run (no full-repo deep AST walk beyond `src/noorheroes/`)"). No network calls, no live DB/Redis dependency for the four purely-static invariants; the one invariant requiring runtime behavior (domain-service reverification) uses `httpx.AsyncClient` against the in-process FastAPI app with a Testcontainers-backed or SQLite-in-memory-backed test DB, consistent with the project's existing integration-test tooling (`NoorHeroes_Final_Development_Prompt.md` §5).
- Zero flakiness tolerance: these are structural assertions over source code and deterministic request/response behavior — a flaky architectural test is a bug in the test, not the codebase, and must be fixed immediately, never retried-until-green.
- The suite must produce a failure message that names the exact offending file, line, and invariant violated (every source blueprint requires this — see each blueprint's own §18 Error Handling row "clear, actionable failure message").

---

## 3. Technical Implementation Details (per invariant)

### 3.1 Invariant 1 — `gateway-zero-business-authorization`

**What it asserts:** Nothing under `src/noorheroes/infrastructure/` (the in-process gateway-equivalent middleware layer: `RequestIdMiddleware`, `StructuredLoggingMiddleware`, `RateLimitMiddleware`/`SlidingWindowRateLimiter`) — and, if version-controlled in-repo, any external gateway config (Nginx/Envoy) — contains any of:
- a SQLAlchemy `AsyncSession`/`Session` usage or any DB-query construct;
- a reference to `family_id`, `child_id`, or `scopes` used in a *comparison* (ownership/scope-matching) expression;
- an import from any `src/noorheroes/modules/<context>/service.py` (i.e., a call into any of the 12 domain-context services) or any `modules/*` service class.

**What it would catch if violated:** A future PR that "helpfully" adds a convenience `if family_id != request.state.family_id: raise` check directly in `RateLimitMiddleware` or a new gateway-layer middleware — exactly the scope-creep the PRD's Edge Case §1.10.1 warns against, and precisely the failure mode that would make a gateway misconfiguration a system-wide authorization bypass (the platform's declared zero-tolerance metric, `NoorHeroes_Final_Development_Prompt.md` §0: "Authorization-bypass incidents via gateway misconfiguration: 0 (hard, zero-tolerance)").

**How it's implemented:** Python's built-in `ast` module (no new dependency — B-03 §26 explicitly directs "the architectural test is pure Python/AST tooling already available to the project's test suite"). Walk every `.py` file under `src/noorheroes/infrastructure/` (excluding `infrastructure/ai/`, `infrastructure/db/`, `infrastructure/redis.py` connection-setup code, and `infrastructure/storage`/`R2StorageService`/`CDNService` — these are legitimate infra plumbing, not authz-adjacent; scope the scan precisely to files that sit in the *request-handling* path: middleware modules and any gateway-config files). For each module:
- Parse to an AST; walk all `Attribute`/`Compare`/`Call` nodes.
- Flag any `Import`/`ImportFrom` node whose module path matches `src.noorheroes.modules.*` (or the project's actual import alias, e.g., `noorheroes.modules.*`).
- Flag any `Compare` node where either operand's source text (via `ast.unparse`) contains the substrings `family_id`, `child_id`, or `scopes`.
- Flag any `Call` node whose callee resolves (via a small allowlisted-name check) to a known SQLAlchemy session method (`execute`, `scalar`, `scalars`, `get`) — this catches "gateway queries the DB for ownership" even without an explicit `AsyncSession` import alias match.
- If any in-repo external gateway config exists (Nginx/Envoy `.conf`/`.yaml` under, e.g., `infra/gateway/` — confirm actual path via the project's infra/deploy directory before assuming; do not invent a path, and if no such file is version-controlled, this half of the scan is a documented no-op, not a silent pass), grep it for `family_id`/`child_id`/`scope` tokens in routing rules.

### 3.2 Invariant 2 — `domain-service child-scoped-reverification`

**What it asserts:** For a request carrying a **valid, correctly-signed JWT for Family A**, but a path/query parameter referencing a **child belonging to Family B**, every child-scoped domain-service endpoint (`content`, `learning`, `rewards`, `habits`, `avatars`, and any other context confirmed to serve child-scoped data) rejects the request with 403 — **even when any gateway-layer protection is assumed/mocked as entirely absent**. Additionally: a child-mode token presented against a Parent-Dashboard-only endpoint is explicitly rejected (403 with a non-empty error body), never silently answered with an empty/masked 200.

**What it would catch if violated:** A developer removing (accidentally, in a refactor, or via a well-intentioned "the gateway already checks this" shortcut) the `verify_child_scope()` call from one context's router/service — the exact "single un-migrated context leaves a real bypass" failure B-06 §Task-03 names directly. It would also catch a context silently returning `[]`/`null` for a scope mismatch instead of an explicit 403 (the FR-5 "never silently returning an empty/masked dataset" failure mode).

**How it's implemented:** This is the one invariant that is *runtime*, not purely static — because "the domain service re-verifies independently of the gateway" is a behavioral claim, not a structural one, it must be proven by exercising the real request path. Using `httpx.AsyncClient(app=app, base_url="http://test")` against the actual FastAPI app instance (no gateway process in front of it in the test — this **is** the simulated bypass: there is no separate gateway/WAF layer to even bypass in-process, so the test's premise is satisfied by construction, and is additionally reinforced by monkey-patching/stubbing `RateLimitMiddleware`/`StructuredLoggingMiddleware` to a pass-through no-op for the duration of these specific test cases, so the test provably exercises zero gateway-layer participation):
1. Seed two families (Family A, Family B) each with one child, via the test DB fixture (Testcontainers Postgres, per `NoorHeroes_Final_Development_Prompt.md` §5's Integration row).
2. Mint a valid JWT for a Family A parent via the real `create_access_token(JwtClaims(...))`.
3. For each migrated context's child-scoped GET/POST endpoint, issue a request using Family A's token but Family B's `child_id` in the path/query/body.
4. Assert HTTP 403 and a specific `ChildScopeViolationError`-shaped error envelope (per `FAST-API-INSTRUCTIONS.md` §2's documented `ChildScopeViolationError` — "Cross-family child profile access attempt").
5. Separately: mint a child-mode token, hit a confirmed Parent-Dashboard-only endpoint, assert 403 with a non-empty body (never 200 with `{}`/`[]`).
6. Parametrize steps 3–5 across at least `content`, `learning`, and `rewards` (B-06 §27's explicit minimum context coverage), plus `habits` and `avatars` since those are also named as child-scoped contexts in B-06 §9.

### 3.3 Invariant 3 — `JWT-claim-schema conformance`

**What it asserts:** `src/noorheroes/core/schemas/jwt_claims.py::JwtClaims` is the **only** Pydantic model or `TypedDict` anywhere under `src/noorheroes/` whose field set meaningfully overlaps a token-claims payload shape. No second, divergent claims schema exists anywhere — not in a specific bounded context, not as a "simplified" variant for one flow.

**What it would catch if violated:** A developer building a new feature (e.g., a future notifications-preview token) who defines their own `class NotificationPreviewClaims(BaseModel): sub: str; family_id: str; ...` instead of reusing/extending `JwtClaims` — precisely the "no feature-specific variant token schema exists anywhere in the platform" acceptance criterion from B-01 §5's Acceptance Criterion.

**How it's implemented:** AST-scan (same `ast`-module approach as §3.1) across all of `src/noorheroes/` for `ClassDef` nodes whose base classes include `pydantic.BaseModel` or `typing.TypedDict`, excluding `core/schemas/jwt_claims.py` itself. For each candidate class, extract its declared field names (`AnnAssign` nodes in the class body) and compute overlap against `JwtClaims`'s canonical nine-field set (`sub`, `family_id`, `mode`, `child_id`, `scopes`, `device_id`, `auth_time`, `consent_version`, `session_id`). Flag any class with **2 or more** overlapping field names (B-01 §27's own stated heuristic: "Pydantic models/TypedDicts with 2+ field-name overlaps against `JwtClaims`'s field set, defined outside `core/schemas/jwt_claims.py`"). A second, complementary check: AST-scan for any `dict`/`Dict[str, Any]` literal constructed and passed directly as an argument to a JWT-encoding call (`jwt.encode(...)` or the project's actual signing-library call inside `core/security.py`) from **outside** `core/security.py::create_access_token` — this catches the "ad hoc dict payload, no model at all" variant of the same violation that a class-based scan alone would miss.

### 3.4 Invariant 4 — `credential-hashing-is-not-fast-hash`

**What it asserts:** No `hashlib.sha256`, `hashlib.sha1`, `hashlib.md5`, or other general-purpose fast-hash construct (also cover `hmac.new(..., hashlib.sha256, ...)` used as a *credential* hash, not as an HMAC-signature primitive elsewhere in the codebase — see the scope note below) appears anywhere within the credential-storage code path: `common/security/credential_hasher.py` itself, and every call site that sets/verifies a parent PIN or child lock pattern/PIN.

**What it would catch if violated:** A regression where a future PR "temporarily" swaps in `hashlib.sha256(pin.encode()).hexdigest()` for local dev convenience and that change survives to a merged PR — the exact brute-force-feasibility risk FR-10 exists to eliminate.

**How it's implemented:** A scoped `hashlib`/fast-hash import-and-call scan (B-04 §27's own directive: "scope the scan to the relevant modules — parent-PIN and child-lock storage/verification files — rather than the entire repo, to avoid false positives from unrelated hashing use elsewhere, e.g., non-credential checksum use"). Concretely:
1. Maintain an explicit, reviewed **credential-path file allowlist** as a constant in the test module (e.g., `CREDENTIAL_PATH_FILES = ["src/noorheroes/common/security/credential_hasher.py", "src/noorheroes/modules/identity/service.py", ...]`) populated from B-04 Task 01's audit output (the audit is B-04's own deliverable, already complete per this document's stated assumption that all nine backend blueprints are implemented — this test simply re-reads that already-established file list; if the audit's file list is not recorded anywhere accessible, the test author must re-derive it via `grep -rl "pin\|lock_pattern" src/noorheroes/ --include=*.py` cross-referenced with actual PIN/pattern model field usage before finalizing the constant — **do not guess this list, confirm it against the real repository**).
2. AST-scan each allowlisted file for `Import`/`ImportFrom` nodes naming `hashlib` (or `Attribute` access `hashlib.sha256`/`hashlib.md5`/`hashlib.sha1` even via a module-level `import hashlib` elsewhere in the file) and for any `Call` node whose callee is one of those attributes.
3. Positive-control assertion in the same test: confirm `argon2`/the project's confirmed Argon2 binding **is** imported in `credential_hasher.py` — a scan that finds "no fast hash" because the file was accidentally emptied is not a passing scan; assert the correct primitive is present, not merely the absence of the wrong one.

### 3.5 Invariant 5 — `upload-pipeline-step-ordering`

**What it asserts:** No code path can reach a transcode call, or move an asset into child-delivery storage, without `PipelineResult.steps_completed == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]` (all ten pre-review steps, strictly in that order) first — for **every** `UploadSource` value identically, with zero source-specific branching anywhere in `run_upload_pipeline()`.

**What it would catch if violated:** A seasonal-content deadline pressure scenario (PRD Edge Case §1.10.4, cross-referenced in B-05 §25) where a developer adds `if source == UploadSource.ADMIN_CMS: skip_to_step(8)` as a "trusted internal source" shortcut — the platform's declared zero-tolerance metric ("Content reaching child-delivery storage without completing all 11 upload-pipeline steps: 0 (hard, zero-tolerance)," `NoorHeroes_Final_Development_Prompt.md` §0).

**How it's implemented:** Two complementary techniques, both required (a pure code-search test alone is insufficient here because ordering is a runtime property, and a pure runtime test alone would miss a *dormant* shortcut path that exists in code but isn't exercised by the specific fixture used):
1. **Runtime ordering assertion** (primary): construct a deliberately-instrumented `UploadedAsset` fixture and a `run_upload_pipeline()` invocation with each step's underlying scanner/classifier call mocked to record its own invocation order into a shared list. Run once per `UploadSource` enum value using an *identical* input asset. Assert: (a) the recorded order is exactly `[1..10]` for every source; (b) `PipelineResult.steps_completed` matches that list; (c) no transcode call (mock/spy the transcode entry point) is invoked before step 10's completion is recorded; (d) the recorded step sequence and final `PipelineResult.status` are byte-for-byte identical across all `UploadSource` values given the same input (the "source-agnostic" half of B-05 §27's mandatory test, folded into this same runtime check for suite cohesion — do not re-implement it as a fully separate test file if this consolidated one already proves it, though B-05's own `tests/media/test_upload_pipeline_source_agnostic.py` may continue to exist for its own more granular per-step assertions; this suite's version is the CI-blocking summary check).
2. **Negative "no shortcut" static scan** (secondary, defense-in-depth against a dormant/never-exercised shortcut branch): AST-scan `src/noorheroes/media/pipeline/upload_validation_pipeline.py` for any `if`/`match` statement whose condition references `source`/`UploadSource` and whose body contains a call to a step-execution function, a `return`, or a `continue`/`break` that would skip any of steps 1–10 or jump directly toward a transcode/promotion call — flag any such conditional as a violation regardless of whether the current test fixtures happen to exercise it.
3. **Fault-injection variant** (see §14.2): a mutation test that patches `run_upload_pipeline()`'s step list to omit step 4 (AV scan) and asserts the ordering test in (1) fails loudly — proving the test itself has teeth, not just green-by-default coverage.

---

## 4. Architecture and Component Responsibilities

```
backend/
  src/noorheroes/                      # already-implemented production code (Phase 2/F.37) — read-only from this suite's perspective
    core/
      schemas/jwt_claims.py            # JwtClaims (Invariant 3 target)
      security.py                      # create_access_token (Invariant 3 target)
      deps.py                          # get_current_parent/child/admin (Invariant 2/3 consumer)
    common/security/
      child_scope_verifier.py          # verify_child_scope() (Invariant 2 target)
      credential_hasher.py             # hash_credential/verify_credential (Invariant 4 target)
    infrastructure/                    # middleware layer (Invariant 1 target)
    media/pipeline/
      upload_validation_pipeline.py    # run_upload_pipeline() (Invariant 5 target)
      steps/
    modules/<12 contexts>/             # domain services (Invariant 2 consumers)

  tests/
    architectural/                     # <-- THIS BLUEPRINT'S DELIVERABLE
      __init__.py
      conftest.py                      # shared fixtures: AST-scan helper, seeded two-family DB fixture, JWT-minting helpers, gateway-bypass httpx client fixture
      _ast_scan_utils.py               # shared AST-walking helpers (import-scan, call-scan, class-field-overlap-scan) reused by 4 of the 5 test modules — avoids five hand-rolled AST walkers
      test_gateway_zero_authz.py                 # Invariant 1
      test_child_scoped_reverification.py         # Invariant 2
      test_jwt_claim_schema.py                    # Invariant 3
      test_credential_hashing_not_fast.py          # Invariant 4
      test_upload_pipeline_ordering.py             # Invariant 5
```

**Component responsibilities:**
- `_ast_scan_utils.py` — the single shared static-analysis toolkit. Owns: `scan_directory_for_imports(path, forbidden_module_prefixes)`, `scan_directory_for_calls(path, forbidden_callables)`, `scan_directory_for_comparisons(path, forbidden_identifiers)`, `find_classes_with_field_overlap(path, base_classes, reference_fields, min_overlap, exclude_paths)`, `find_conditional_step_skips(path, guard_identifier)`. Each returns a list of `Violation(file: Path, line: int, message: str)` dataclasses so every test module renders failures identically.
- `conftest.py` — owns the two runtime fixtures used only by Invariant 2 and (partially) Invariant 5: a seeded two-family/two-child Postgres Testcontainers fixture (`two_family_fixture`), and a bare `httpx.AsyncClient` wired directly to the FastAPI `app` instance with gateway-equivalent middleware stubbed to pass-through (`gateway_bypassed_client`). Also owns `mint_parent_jwt(family_id)`, `mint_child_jwt(family_id, child_id)`, `mint_admin_jwt(scopes)` thin wrappers around the real `create_access_token`/`JwtClaims`.
- Each `test_*.py` module owns only: the specific forbidden-pattern list for its invariant, and its own assertions/parametrization — no module re-implements AST walking.

---

## 5. Folder/File Structure

Exact file layout (all paths relative to the backend package root, consistent with `FAST-API-INSTRUCTIONS.md`'s existing `src/noorheroes/` / `tests/` split):

```
backend/tests/architectural/__init__.py
backend/tests/architectural/conftest.py
backend/tests/architectural/_ast_scan_utils.py
backend/tests/architectural/test_gateway_zero_authz.py
backend/tests/architectural/test_child_scoped_reverification.py
backend/tests/architectural/test_jwt_claim_schema.py
backend/tests/architectural/test_credential_hashing_not_fast.py
backend/tests/architectural/test_upload_pipeline_ordering.py
```

**Migration note on pre-existing per-blueprint architectural test files:** if B-01/B-03/B-04/B-05/B-06's own implementation work already produced `tests/architecture/test_single_jwt_schema.py`, `tests/architecture/test_gateway_zero_authorization.py`, `tests/architecture/test_no_fast_hash_in_credential_path.py`, `tests/architecture/test_domain_service_reverification_under_simulated_gateway_bypass.py`, and/or `tests/media/test_upload_pipeline_ordering.py` on disk (note the pre-existing directory is `tests/architecture/`, singular — this blueprint's canonical package is `tests/architectural/`, plural, to avoid an ambiguous partial-migration state where both directories exist and it's unclear which is authoritative), **move and consolidate their logic into the five files above, then delete the old files** (do not leave both trees present — a developer must never wonder which of two nearly-identically-named test files is the CI-blocking one). If B-05's `tests/media/test_upload_pipeline_source_agnostic.py` already exists with its own granular per-step source-agnostic assertions, it may remain in place under `tests/media/` as a non-architectural-marker integration test (it continues running under CI stage 5, Integration tests) — only its *ordering*-specific, CI-blocking-critical assertions get consolidated into `tests/architectural/test_upload_pipeline_ordering.py`.

---

## 6. APIs, Models, Interfaces, and Data Flow

This suite introduces no new production API, model, or endpoint — it is a pure test/CI artifact. Its "interface" surface is entirely internal to the test package:

```python
# tests/architectural/_ast_scan_utils.py

@dataclass(frozen=True)
class Violation:
    file: Path
    line: int
    message: str

def scan_directory_for_imports(
    root: Path, forbidden_module_prefixes: list[str], exclude: list[Path] | None = None
) -> list[Violation]: ...

def scan_directory_for_comparisons(
    root: Path, forbidden_identifiers: list[str], exclude: list[Path] | None = None
) -> list[Violation]: ...

def scan_directory_for_calls(
    root: Path, forbidden_callable_names: list[str], exclude: list[Path] | None = None
) -> list[Violation]: ...

def find_classes_with_field_overlap(
    root: Path, base_class_names: list[str], reference_fields: set[str],
    min_overlap: int, exclude: list[Path] | None = None
) -> list[Violation]: ...
```

```python
# tests/architectural/conftest.py

@pytest.fixture
async def two_family_fixture(db_session) -> TwoFamilyFixture:
    """Seeds Family A (+ child A1) and Family B (+ child B1) via the real repository layer."""
    ...

@pytest.fixture
async def gateway_bypassed_client(app) -> AsyncIterator[httpx.AsyncClient]:
    """httpx.AsyncClient against the real FastAPI app with RateLimitMiddleware/
    StructuredLoggingMiddleware monkey-patched to pass-through no-ops, proving
    the domain-service check is what rejects the request, not a gateway artifact."""
    ...

def mint_parent_jwt(family_id: str, scopes: list[str] | None = None) -> str: ...
def mint_child_jwt(family_id: str, child_id: str) -> str: ...
```

**Data flow for Invariant 2's runtime check** (the only invariant with real request/response flow):
```
test → mint_parent_jwt(family_id="fam_A") → gateway_bypassed_client.get(
         f"/v1/content/catalog?child_id={fam_B_child_id}",
         headers={"Authorization": f"Bearer {token}"})
       → FastAPI app (middleware stubbed pass-through)
       → ContentRouter → get_current_parent (decodes JwtClaims)
       → ContentService → verify_child_scope(claims, requested_family_id="fam_A", requested_child_id=fam_B_child_id, db)
       → DB-backed ownership query finds no fam_A ⇄ fam_B_child relationship
       → raises ChildScopeViolationError
       → maps to HTTP 403
       ← test asserts response.status_code == 403 and error envelope is non-empty
```

---

## 7. Dependencies and Configuration Requirements

- **No new third-party library.** Static-analysis invariants use Python's stdlib `ast` module exclusively (explicitly directed by B-01 §26/B-03 §26/B-04's parallel guidance: reuse existing tooling, do not introduce a new heavyweight static-analysis dependency).
- Runtime invariant (Invariant 2) reuses the project's already-standard `httpx.AsyncClient` (per `NoorHeroes_Final_Development_Prompt.md` §5's "API/contract" test-type row) and Testcontainers-backed Postgres (per the same table's "Integration" row) — no new test infra.
- `pytest.ini` / `pyproject.toml` `[tool.pytest.ini_options]` must register the new marker:
  ```ini
  markers =
      architectural: CI-blocking architectural-invariant tests (tests/architectural/) — never skip/xfail without Security Engineering sign-off
  ```
- Every test function/class in `tests/architectural/` is decorated `@pytest.mark.architectural` (or the whole package is auto-marked via a `conftest.py` `pytest_collection_modifyitems` hook keyed on path — prefer the path-based auto-mark so no individual test author can forget the decorator and accidentally exclude a test from the CI-blocking run).
- CI config addition (backend workflow, e.g. `.github/workflows/backend.yml`), inserted as pipeline stage 6 per `NoorHeroes_Final_Development_Prompt.md` §6:
  ```yaml
  architectural-invariants:
    name: "Architectural Invariants (CI-blocking, F.37)"
    needs: [integration-tests]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up environment
        run: ./scripts/setup-backend-ci.sh   # same setup as other backend jobs
      - name: Run architectural invariant suite
        run: uv run pytest tests/architectural/ -m architectural -v --no-header
        # NOTE: -m architectural is redundant with the path filter here (defense-in-depth
        # against a future test accidentally landing in this dir unmarked, or a marked
        # test accidentally landing outside this dir) — both must independently narrow
        # to exactly these five files' contents.
  ```
  This job must be added to the repository's branch-protection **required status checks** list for `main` — a green CI run with this job merely present-but-not-required does not satisfy `NoorHeroes_Final_Development_Prompt.md` §10's "mandatory, non-bypassable CI gates."

---

## 8. Database/Storage Requirements

- Four of the five invariants (gateway-authz, JWT-schema, credential-hashing, upload-ordering's static half) require **no database at all** — pure source-tree scans.
- Invariant 2 (child-scoped reverification) and Invariant 5's runtime half require a real, ephemeral Postgres instance via Testcontainers (consistent with `NoorHeroes_Final_Development_Prompt.md` §5's Integration-test row: "pytest + Testcontainers (real Postgres/Redis)") — reuse the project's existing Testcontainers fixture setup from `tests/conftest.py` at the repo root rather than standing up a parallel DB-fixture mechanism inside `tests/architectural/`.
- No schema changes, no new tables, no migrations — this suite only reads/writes through existing repositories (`UserRepository`, `ChildRepository`, `ContentRepository`, etc.) to seed its two-family fixture.
- No production data is ever touched; the fixture DB is created and torn down per test session, per the project's existing CI ephemeral-DB convention (`NoorHeroes_Final_Development_Prompt.md` §3: "no shared mutable state between runs").

---

## 9. Authentication, Authorization, Validation, and Security Considerations

This entire suite exists to protect security guarantees, so precision here matters more than in a typical test blueprint.

**What each invariant protects against, restated as an attack/failure scenario:**

| Invariant | What it protects against |
|---|---|
| gateway-zero-business-authorization | A gateway-layer authorization bug becoming a *platform-wide* bypass — because the gateway fronts all 12 bounded contexts, one gateway mistake would otherwise compromise every context simultaneously, versus a domain-service bug which is contained to that one context. |
| domain-service child-scoped-reverification | A parent (or a compromised/leaked parent JWT) from Family A reading, modifying, or deleting Family B's child data — the single most severe child-safety/privacy failure mode in the product, given the product serves children ages 3–16. |
| JWT-claim-schema conformance | A divergent, less-carefully-reviewed token schema being introduced for "just one feature" that omits a security-relevant claim (e.g., a token schema missing `consent_version` or `auth_time` used to bypass consent/step-up checks elsewhere in the platform). |
| credential-hashing-is-not-fast-hash | Offline brute-force of parent PIN / child lock-pattern hashes in the event of any future data exfiltration — a fast hash makes an exfiltrated hash table crackable in commodity GPU-hours; Argon2id makes it computationally infeasible at scale. |
| upload-pipeline-step-ordering | Unsafe, unmoderated, or malware-bearing content reaching a child's screen — given the product is explicitly child-facing (ages 3–16), a shortcut here is a direct child-safety incident, not merely a data-integrity bug. |

**Authentication:** the suite mints real, correctly-signed JWTs via the project's actual `create_access_token`/`JwtClaims` (never hand-crafted token strings) — this ensures the test exercises the real signing/decoding path, not a stub that could silently diverge from production behavior.

**Authorization:** Invariant 2 is itself the authorization-boundary test; it must never mock/stub `verify_child_scope()` itself (mocking the function under test would make the test tautological) — only the gateway-equivalent middleware may be stubbed, and only to prove its *absence* doesn't matter.

**Validation:** every static scan must have at least one intentional "known-good" fixture asset that exercises the *legitimate* pattern near the forbidden one (e.g., a legitimate `family_id` reference inside a *domain service* file, outside the scanned `infrastructure/` scope) to prove the scan's scope boundary is correct and not accidentally over broad (which would produce false positives that erode trust in the gate and invite exactly the "just add `# noqa`" bypass culture this suite exists to prevent).

**Security considerations specific to this suite itself:**
- The suite's own source code (`tests/architectural/`) is itself security-sensitive: a broadened `exclude` list, a narrowed `forbidden_module_prefixes` list, or a silently-added `pytest.mark.skip` inside any of these five files *is* a security regression, equivalent in severity to weakening the invariant it tests. Treat any diff touching `tests/architectural/` with the same review rigor B-01 §25 demands for `JwtClaims` itself (Security Engineering + Platform Architecture sign-off).
- Never log secrets/tokens from within these tests beyond what pytest's own failure output already captures structurally (test JWTs are synthetic/ephemeral per-test, so this is a lower-stakes concern than production logging, but still avoid printing full token strings in assertion messages — print decoded claim summaries instead).

---

## 10. Error Handling and Edge Cases

| Scenario | Required suite behavior |
|---|---|
| A static scan finds zero violations (expected steady state) | Test passes silently; no violation list printed. |
| A static scan finds one or more violations | Test fails with `pytest.fail(f"{invariant_name} violated:\n" + "\n".join(f"  {v.file}:{v.line} — {v.message}" for v in violations))` — every violation listed, not just the first (a developer fixing one at a time should see the full remaining list on the next run, but the *first* failing run should already show everything found). |
| `tests/architectural/` scan target directory (`src/noorheroes/infrastructure/`, etc.) doesn't exist at the expected path (e.g., a future refactor renames it) | Test must **fail loudly with a distinct "scan target not found" error**, never silently pass with zero violations found — a missing directory is not proof of compliance, and a silently-vacuous scan is worse than no scan (see §14.2's mutation-test requirement, which specifically guards against this). |
| Invariant 2's `two_family_fixture` DB seed fails (Testcontainers startup issue) | Test errors (not "fails" in the assertion sense) with the underlying Testcontainers error surfaced verbatim — do not swallow and report as an invariant violation, since that would misattribute an infra flake as a security regression. |
| A context legitimately has no child-scoped endpoints yet (future context added, not yet wired to `verify_child_scope()`) | The context-parametrization list in `test_child_scoped_reverification.py` is an explicit, reviewed allowlist of contexts *known* to serve child-scoped data (`content`, `learning`, `rewards`, `habits`, `avatars`) — a new context is **not** automatically included until a human explicitly adds it here, with a corresponding PR-review checklist item (§4's CODEOWNERS review checklist, `NoorHeroes_Final_Development_Prompt.md` §4: "Does this change... touch the reward ledger, JWT schema, or upload pipeline") extended to also ask "does this PR add a new child-scoped context? If so, has it been added to `test_child_scoped_reverification.py`'s context list?" |
| The suite itself is accidentally excluded from a CI run (e.g., a path-filter misconfiguration in the workflow file skips it for a PR that doesn't touch `backend/`) | Out of this test suite's own power to prevent directly — mitigated at the CI-config level (§7) by making `architectural-invariants` a required status check regardless of path filters, not a conditionally-triggered job. |
| `ast.parse()` fails on a source file (syntax error) | Bubble up as a test error (not a silent skip of that file) — a file that doesn't even parse cannot have been validated by any other CI stage either, so this should already be caught by earlier stages (lint/type-check), but the architectural scan must not mask it by skipping. |

---

## 11. State Management and Lifecycle Considerations

- This suite is **stateless between runs** — no persisted state, no accumulated history, no "last known good" baseline file to diff against (unlike, say, a visual-regression suite). Each run scans the current working tree fresh.
- The `two_family_fixture` (Invariant 2) is created and torn down per test session (or per test function, whichever matches the project's existing Testcontainers fixture scope convention in the root `tests/conftest.py` — reuse that scope, do not introduce a different lifecycle here for consistency and to avoid doubling CI runtime with a redundant container spin-up).
- JWTs minted within this suite are short-lived, synthetic, and never touch the real Redis refresh-token-denylist infrastructure (B-02) — Invariant 2's tests use access tokens only, not the full refresh-rotation lifecycle, since that lifecycle is B-02's own concern and already covered by B-02's own tests.
- No caching of scan results across test runs — every CI invocation performs a full fresh AST walk of the (small, scoped) target directories; given the non-functional requirement in §2.3 (whole suite under a minute), caching would be premature optimization that risks masking a stale-cache false pass.

---

## 12. Integration Points with Existing Modules

Each test module imports and exercises the **real, already-implemented** production classes — never a reimplementation or a mock of the thing being verified:

| Test module | Real production symbols imported/exercised |
|---|---|
| `test_gateway_zero_authz.py` | No direct import (it's a source-tree scan of `src/noorheroes/infrastructure/`, not a runtime exercise) — but its `exclude`/scope list must be kept in sync with the real `infrastructure/` module list from `FAST-API-INSTRUCTIONS.md` §4 (`RequestIdMiddleware`, `StructuredLoggingMiddleware`, `RateLimitMiddleware`, `SlidingWindowRateLimiter`, `R2StorageService`, `CDNService`, AI provider infra). |
| `test_child_scoped_reverification.py` | `src.noorheroes.core.security.create_access_token`, `src.noorheroes.core.schemas.jwt_claims.JwtClaims`, `src.noorheroes.core.deps.get_current_parent`/`get_current_child`, `src.noorheroes.common.security.child_scope_verifier.verify_child_scope`, the real FastAPI `app` instance from `main.py`, and each named context's real router (`ContentRouter`, `LearningRouter`, `RewardsRouter`, `HabitsRouter`, `AvatarsRouter`). |
| `test_jwt_claim_schema.py` | `src.noorheroes.core.schemas.jwt_claims.JwtClaims` (as the reference field set), scans everything else. |
| `test_credential_hashing_not_fast.py` | `src.noorheroes.common.security.credential_hasher.hash_credential`/`verify_credential` (positive-control import-presence check), scans the credential-path allowlist for the negative check. |
| `test_upload_pipeline_ordering.py` | `src.noorheroes.media.pipeline.upload_validation_pipeline.run_upload_pipeline`, `src.noorheroes.media.pipeline.models.UploadSource`/`UploadedAsset`/`PipelineResult`. |

**Cross-references to the individual F.37 blueprints' own tests** (not duplicated, only referenced): this suite's `test_child_scoped_reverification.py` module docstring must explicitly cross-reference B-06's own `tests/common/test_child_scope_verifier.py` unit tests (family-mismatch/child-mismatch/stale-claim cases) as "the unit-level counterpart to this file's system-level simulated-bypass proof" — same pattern for the other four, so a future reader lands on the right file for the right *kind* of test (unit vs. this suite's structural/system-level proof).

---

## 13. Development Steps in the Correct Implementation Order

Per the task's explicit risk-based ordering directive — JWT schema and credential hashing first since they gate everything else, then gateway-authz, then child-scoped-reverification, then upload-pipeline-ordering:

**Step 1 — Scaffold the shared package and AST toolkit**
Create `tests/architectural/__init__.py`, `_ast_scan_utils.py` (all four scan-helper functions from §6), and `conftest.py`'s non-DB fixtures (JWT-minting helpers). Register the `architectural` pytest marker. No invariant-specific test yet — this step must be fully unit-tested in isolation (the scan helpers themselves need a small self-test fixture directory under `tests/architectural/_fixtures/` with deliberately-violating and deliberately-clean sample files, so the toolkit's correctness doesn't depend on the real codebase's current compliance state).

**Step 2 — Invariant 3: JWT-claim-schema conformance**
Implement `test_jwt_claim_schema.py` using the field-overlap scanner from Step 1. This is first among the five because every other invariant's test fixtures (JWT minting in Step 1's `conftest.py`) implicitly depend on `JwtClaims` being the sole, trustworthy schema — if this invariant were broken, every other test's JWTs might not represent the real production token shape.

**Step 3 — Invariant 4: credential-hashing-is-not-fast-hash**
Implement `test_credential_hashing_not_fast.py`, including the credential-path file allowlist (confirmed against the real repository per §3.4, not guessed) and the positive-control Argon2-import check. Second because credential compromise is the platform's other "gates everything else" risk (a broken credential hash undermines every session that credential protects).

**Step 4 — Invariant 1: gateway-zero-business-authorization**
Implement `test_gateway_zero_authz.py` using the import/comparison/call scanners against `src/noorheroes/infrastructure/`. Third because it's the platform's declared highest-priority guarantee (tied with Invariant 2) and is purely static (no DB fixture dependency), so it can land before the runtime-dependent Invariant 2.

**Step 5 — Invariant 2: domain-service child-scoped-reverification**
Implement the `two_family_fixture` and `gateway_bypassed_client` fixtures in `conftest.py` (the only runtime/DB-dependent fixtures in this suite), then `test_child_scoped_reverification.py`. Fourth — the platform's other declared highest-priority guarantee, placed after Invariant 1 because it is the more complex, runtime-dependent build and benefits from Invariant 1's simpler static-scan pattern already being proven out in this same PR/branch.

**Step 6 — Invariant 5: upload-pipeline-step-ordering**
Implement `test_upload_pipeline_ordering.py`'s runtime ordering assertion (primary) and static negative-scan (secondary). Last among the five per the task's explicit ordering — still zero-tolerance, but not one of the platform's declared *two* highest-priority guarantees (B-05 §25 explicitly self-corrects on this point: "this pipeline (item 5) is still a hard requirement but not in that specific top-two... do not overstate its relative priority").

**Step 7 — Consolidation and cutover**
Locate and migrate any pre-existing per-blueprint architectural test files (per §5's migration note) into the five canonical files, deleting the old `tests/architecture/` (singular) directory once migration is verified complete via a diff review confirming no assertion was dropped in the move.

**Step 8 — CI wiring**
Add the `architectural-invariants` job (§7) to the backend GitHub Actions workflow as stage 6, mark it a required status check in branch protection, and confirm a deliberately-broken PR (see §14.2) actually blocks merge end-to-end, not just fails the job.

---

## 14. Testing Strategy and Acceptance Criteria

**Acceptance criterion for this entire blueprint:** the suite passes cleanly against the current (already-compliant, per Phase 2) codebase, is wired as a required CI status check, and — critically — **each of the five tests fails when its invariant is deliberately violated**. A suite that only ever passes is unverified; §14.2 below is not optional polish, it is the actual proof this blueprint did its job.

### 14.1 Steady-state acceptance
- All five `test_*.py` modules pass against the current `main` branch with zero violations found.
- The suite completes in under 60 seconds on standard CI hardware (per §2.3).
- The suite is registered as a required, separately-named status check, distinct in the PR UI from the generic test job (per §7's CI config).
- No test in the suite is marked `skip`/`xfail`/`skipif` anywhere (grep-verified as part of this suite's own CI job, ironically using the same AST-scan toolkit from §6 against `tests/architectural/` itself — a fitting, low-cost self-check).

### 14.2 Mutation/fault-injection verification (required for at least 2 of the 5, per the task's explicit requirement — this blueprint specifies it for all 5, since a security-critical suite with unverified negative cases is incomplete)

| Invariant | Deliberate violation to inject (temporarily, on a throwaway branch, never merged) | Expected result |
|---|---|---|
| gateway-zero-authz | Add `if request.state.family_id != claims.family_id: raise Forbidden()` directly inside `RateLimitMiddleware.__call__` | `test_gateway_zero_authz.py` fails, naming the exact file/line of the injected comparison. |
| child-scoped-reverification | Comment out the `verify_child_scope(...)` call inside `ContentService`'s child-scoped read method | `test_child_scoped_reverification.py`'s Family-A-token-against-Family-B-child case for the `content` context fails (returns 200 with Family B's data, or a non-403 status), while other unaffected contexts in the same parametrized run continue to pass — proving the test isolates per-context, not just suite-wide. |
| JWT-claim-schema | Add a second Pydantic model `class LegacyTokenClaims(BaseModel): sub: str; family_id: str; scopes: list[str]` anywhere under `src/noorheroes/modules/` | `test_jwt_claim_schema.py` fails, naming `LegacyTokenClaims` and its file/line, listing the 3 overlapping field names. |
| credential-hashing-not-fast | Replace `hash_credential`'s Argon2id call with `hashlib.sha256(raw.encode()).hexdigest()` inside `credential_hasher.py` | `test_credential_hashing_not_fast.py` fails both on the new forbidden-call detection *and* the positive-control Argon2-import-presence check (belt-and-suspenders — losing either signal alone should still catch this). |
| upload-pipeline-step-ordering | Add `if source == UploadSource.ADMIN_CMS: steps_completed = [1,2,3,8,9,10]` (skip steps 4–7) inside the orchestrator | `test_upload_pipeline_ordering.py`'s runtime ordering assertion fails for the `ADMIN_CMS` parametrization specifically, and the source-agnostic byte-for-byte comparison against `SCHOLAR_SUBMISSION`'s (unmodified) step list also fails — two independent assertions catch the same injected bug, which is the intended defense-in-depth of this suite's own design. |

Each mutation-test run above must be performed once during this blueprint's implementation (documented in the PR description as evidence, per each source blueprint's "Definition of Done" pattern of proving the negative case, e.g., B-06 §27: "Mandatory... simulated-gateway-bypass test") and does **not** need to be re-run on every future CI invocation — it is a one-time proof that the suite has teeth, performed once at build time and whenever the suite's own detection logic is later modified.

### 14.3 Regression policy
Per each source blueprint's own §27 "Regression" guidance (B-03: "re-run... on every release touching gateway configuration or `infrastructure/middleware/`"; B-06: "re-run on every release touching any domain service's authorization-check code"; etc.) — since this suite already runs on **every** CI invocation regardless of what changed (it is not path-filtered to skip on unrelated PRs, per §10's edge case), this consolidated suite structurally satisfies all five blueprints' individual regression requirements simultaneously; no separate regression-scheduling mechanism is needed beyond "this job runs on every PR."

---

## 15. Production-Readiness Considerations

- **No PR touching security-sensitive code may bypass this suite.** This is the suite's entire reason for existing as a *consolidated, unmissable* job rather than five easy-to-overlook scattered tests. The required-status-check configuration (§7) is what makes this non-negotiable, not merely a documentation convention.
- **No bypass without recorded sign-off.** If a genuine false positive is ever found (§2.3/§9's validation-of-scan-scope requirement exists precisely to minimize this risk), the fix is to narrow the scan's `exclude` list with a code comment explaining exactly why, reviewed by Security Engineering — never to add a blanket `skip`/`xfail`, and never to silently loosen a `forbidden_module_prefixes`/`forbidden_identifiers` list without the same review rigor.
- **This suite is itself part of the platform's "highest blast radius" subsystem list.** `NoorHeroes_Final_Development_Prompt.md` §4 already names "reward ledger, JWT schema, or upload pipeline" as requiring elevated PR-review scrutiny; a PR touching `tests/architectural/` itself must be added to that same elevated-scrutiny CODEOWNERS list, since weakening this suite is functionally equivalent to weakening the five invariants it protects.
- **Runtime cost must stay bounded as the platform grows.** As more bounded contexts are added (a 13th, 14th context), Invariant 2's context-parametrization list (§10's edge-case table) grows linearly — this is intentional and acceptable; the suite's sub-60-second budget (§2.3) should be re-verified periodically as this list grows, and if it ever threatens that budget, parallelize the parametrized cases (pytest-xdist) rather than removing coverage.
- **This suite has no feature flag and cannot be disabled via configuration.** Unlike a business feature, an architectural invariant test is not something any runtime flag should be able to turn off — its only "off switch" is a source-code PR to this very file tree, which is exactly the elevated-review gate described above.

---

## 16. Dependencies/Prerequisites

- Phase 2 F.37 Security Architecture backend blueprints B-01 through B-06, fully implemented (confirmed per this document's stated context — `FAST-API-INSTRUCTIONS.md` reflects their completed state).
- The project's existing pytest + Testcontainers + `httpx.AsyncClient` test infrastructure (already standard per `NoorHeroes_Final_Development_Prompt.md` §5), including the root-level `tests/conftest.py`'s DB fixture machinery, reused rather than duplicated.
- The backend's existing GitHub Actions workflow file (`backend.yml` or equivalent) into which stage 6 is inserted.
- Branch-protection admin access to mark the new job a required status check (an infrastructure/DevOps prerequisite, not a code prerequisite — flag this explicitly to whoever merges this blueprint's PR, since the code alone does not enforce non-bypassability without this repository-settings step).

---

## 17. Definition of Done

- [ ] `tests/architectural/` package created with `__init__.py`, `conftest.py`, `_ast_scan_utils.py`, and all five `test_*.py` modules.
- [ ] All five invariants implemented per §3's technical specification, each importing/exercising the real production symbols listed in §12.
- [ ] `architectural` pytest marker registered and auto-applied to every test under `tests/architectural/`.
- [ ] Suite passes cleanly against the current, already-F.37-compliant codebase.
- [ ] Each of the five invariants' mutation/fault-injection check (§14.2) performed once and confirmed to fail as expected; evidence documented in the implementing PR's description.
- [ ] Any pre-existing per-blueprint architectural test files migrated into this canonical package and the old `tests/architecture/` (singular) directory removed, per §5's migration note.
- [ ] `architectural-invariants` CI job added as pipeline stage 6, named distinctly from generic test jobs, and configured as a required branch-protection status check on `main`.
- [ ] Suite completes in under 60 seconds on CI hardware.
- [ ] No test in the suite carries `skip`/`xfail`/`skipif`, verified by the suite's own self-check (§14.1).
- [ ] `tests/architectural/` added to the elevated-scrutiny CODEOWNERS/review-checklist list alongside the reward ledger, JWT schema, and upload pipeline (§15).
- [ ] No PostgreSQL/Redis credential or connection-configuration changes introduced (consistent with every one of B-01/B-03/B-04/B-05/B-06's own Definition of Done constraints).

---

## 18. Assumptions or Decisions the Coding Agent Must Follow

1. **The five underlying implementations (B-01, B-03, B-04, B-05, B-06) are complete and correct as of the start of this work.** This blueprint does not re-implement `JwtClaims`, `verify_child_scope()`, `hash_credential`/`verify_credential`, `run_upload_pipeline()`, or the `infrastructure/` middleware layer — it only writes tests against them. If, while implementing these tests, an actual violation is discovered in the production code (not the test), stop and flag it as a Phase 2 regression requiring separate remediation — do not silently "fix" production code as a side effect of a testing-blueprint task, and do not weaken the test to accommodate a discovered production gap.
2. **Do not weaken any of the five invariants to make a test pass.** If a test is failing because a genuine violation exists in production code, the fix is to fix the production code (flagged per point 1), never to narrow the test's scan scope, add an exclusion, or soften an assertion threshold (e.g., changing the field-overlap `min_overlap` from 2 to 3 to make a near-miss pass) without the Security Engineering sign-off this document requires throughout §9 and §15.
3. **Use Python's stdlib `ast` module for all static analysis; do not add a new static-analysis dependency** (no `libcst`, no third-party AST-diffing library) unless an exhaustive check of `pyproject.toml`/existing lockfile confirms the project already depends on one for an unrelated reason — the five source blueprints are unanimous on this point (B-01 §26, B-03 §26, B-04's parallel guidance).
4. **The credential-path file allowlist (§3.4) must be confirmed against the real repository, never guessed.** Locate every actual PIN/pattern hashing/verification call site via search before finalizing the constant list.
5. **The child-scoped context list for Invariant 2 (`content`, `learning`, `rewards`, `habits`, `avatars`) is the confirmed minimum per B-06's own text** — if the real repository's audit (B-06 Task 01) identified additional child-scoped contexts beyond these five, include them; do not narrow this list without re-confirming against that audit.
6. **`tests/architectural/` (plural) is the canonical package name**, distinct from any pre-existing `tests/architecture/` (singular) directory from individual blueprints' own implementation work — consolidate into the plural form and remove the singular one, per §5.
7. **Never mock or stub the function under test.** Invariant 2 may stub gateway-equivalent middleware (to prove its absence doesn't matter) but must never stub `verify_child_scope()` itself; Invariant 4's positive-control check must call the real `hash_credential`, not a mock.
8. **This suite must run on every CI invocation, not be path-filtered to skip on PRs that "don't look security-related."** A refactor anywhere in `src/noorheroes/` could theoretically introduce a violation; do not add a path filter that could cause this job to be silently skipped for a PR that happens to touch, say, only `modules/rewards/` but inadvertently imports something from a scanned path.
9. **Where any technical ambiguity remains** (e.g., the exact in-repo path of an external gateway config file, if one exists) — confirm against the actual repository structure before writing the scan; do not invent a path, per B-03 §9's own explicit instruction ("locate via the existing infra/deploy directory before assuming a path; do not invent a config file location").

---

## AI Agent Development Prompt

You are implementing the **consolidated, CI-blocking architectural-invariant test suite** for NoorHeroes — a child-safety-critical Islamic learning platform. The five security guarantees this suite protects (zero gateway authorization, domain-service child-scope re-verification, single canonical JWT schema, Argon2id-only credential hashing, and 11-step upload-pipeline step ordering) are already fully implemented in production code per Phase 2 (F.37 Security Architecture, blueprints B-01/B-03/B-04/B-05/B-06 — read `FAST-API-INSTRUCTIONS.md` and the individual blueprint files under `Development_Blueprints/F37_Security_Architecture/Backend/` before writing a single line of test code, so you know exactly what real symbols you're importing).

**What to build**, exactly per this document's §4–§13:
1. `backend/tests/architectural/__init__.py`, `_ast_scan_utils.py` (four reusable AST-scan helper functions), `conftest.py` (JWT-minting helpers, `two_family_fixture`, `gateway_bypassed_client`).
2. Five test modules, in this exact implementation order (§13): `test_jwt_claim_schema.py` → `test_credential_hashing_not_fast.py` → `test_gateway_zero_authz.py` → `test_child_scoped_reverification.py` → `test_upload_pipeline_ordering.py`.
3. Migrate/delete any pre-existing per-blueprint `tests/architecture/` (singular) files into this canonical `tests/architectural/` (plural) package.
4. Register the `architectural` pytest marker; wire the `architectural-invariants` CI job as backend pipeline stage 6 (exact YAML in §7); mark it a required branch-protection status check.

**What NOT to change:**
- Do not modify `JwtClaims`, `create_access_token`, `get_current_parent/child/admin`, `verify_child_scope()`, `hash_credential`/`verify_credential`, `run_upload_pipeline()`, or any `infrastructure/` middleware file. If your testing work surfaces an apparent production defect in one of these, **stop, do not fix it silently, and report it as a separate finding** — this task is test-authorship, not remediation.
- Do not weaken, narrow, or add exclusions to any of the five invariants' detection logic to make a test pass. A failing test in this suite means either (a) a real production violation exists — report it, don't hide it — or (b) your scan scope is genuinely wrong — fix the scope with a documented rationale, don't just shrink the forbidden-pattern list until it's green.
- Do not add `skip`/`xfail`/`skipif` anywhere in this suite for any reason without explicit human sign-off recorded in the PR description.
- Do not introduce a new static-analysis or AST-diffing dependency; use Python's stdlib `ast` module only.
- Do not mock/stub the actual function under test in any invariant (only gateway-equivalent middleware may be stubbed, and only in Invariant 2, and only to prove its absence doesn't matter).

**How to verify your work is complete:**
1. Run `uv run pytest tests/architectural/ -m architectural -v` — all five modules pass cleanly against the current codebase.
2. Confirm suite runtime is under 60 seconds.
3. For each of the five invariants, perform the mutation/fault-injection check from §14.2 on a throwaway local branch (never commit the injected violation): temporarily reintroduce the exact violation described, confirm the corresponding test fails with a clear file/line message naming the violation, then revert. Document each of the five confirmations in your PR description as evidence the suite has teeth, not just green-by-default coverage.
4. Confirm the `architectural-invariants` job appears as a distinctly-named, separate status check in a test PR's UI (not folded into a generic "tests" check), and confirm it is listed under the repository's required status checks for `main`.
5. Confirm no `skip`/`xfail`/`skipif` decorator appears anywhere under `tests/architectural/` (this suite's own AST toolkit can self-check this — a fitting final validation step).
6. Walk through the Definition of Done checklist in §17 line by line before declaring this blueprint complete.

If anything in the source blueprints (B-01/B-03/B-04/B-05/B-06) or `FAST-API-INSTRUCTIONS.md` conflicts with an assumption in this document — an actual file path, class name, or context list that differs from what's written here — **the real repository is authoritative; confirm against it and adjust the test's scan targets accordingly, but do not weaken what is being asserted.**
