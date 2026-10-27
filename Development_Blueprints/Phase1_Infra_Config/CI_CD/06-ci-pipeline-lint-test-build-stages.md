# Phase 1 — CI Pipeline: Lint, Static Analysis, Test & Build Stages (1–7 of 13)

`Development_Blueprints.Phase1_Infra_Config.CI_CD.06-ci-pipeline-lint-test-build-stages.md`

**Module:** CI_CD (cross-cutting: `backend/`, `admin-web/`, `mobile/`, `.github/workflows/`)
**Phase:** Phase 1 — Infrastructure & Configuration
**Depends on:** Phase 1 item 02 (`Infra.02-secrets-management-env-example-gitleaks.md` — this file's Stage 1 lint jobs invoke the `.env.example` drift-check scripts that item 02 already builds, and this file's required-status-check list is additive to item 02's already-required `gitleaks-scan`/`trufflehog-verified-scan` checks); Phase 1 item 03 (`Infra.03-docker-compose-local-dev-stack.md` — this file's Stage 5 integration-test jobs reuse the same Testcontainers pattern already proven by `backend/tests/conftest.py`, and explicitly do **not** reuse item 03's `infra/docker-compose.yml`, per that file's own §12 boundary); Phase 0 item 03 (`Repo.03-conventional-commits-semver-branching-policy.md` — this file supplies the concrete job names that get appended to that file's `main` branch-protection required-status-checks list, and consumes its SemVer tags for artifact versioning in Stage 7)
**Consumed by:** `CI_CD.07` (security scan stage — container/dependency scanning, Stage 8 of 13, not built here); `CI_CD.08` (staging deploy + E2E smoke, Stages 9–10 of 13); `CI_CD.09` (manual promotion gate + production deploy, Stages 11–13 of 13); `Development_Blueprints.Phase9_CrossPlatform.CrossPlatform.01` (the real architectural-invariant test suite — Stage 6's job wiring built here is the empty vessel that file populates with the actual F.37 invariant tests, see §5's placeholder design)
**Source of truth:** `NoorHeroes_Final_Development_Prompt.md` §1.2/§1.3 (backend/admin-web tool choices), §4 (linting tooling table), §5 (Testing Strategy table — coverage gates, architectural test list), §6 (the 13-stage CI/CD pipeline, quoted in full in §1 below); `FAST-API-INSTRUCTIONS.md` §6 ("Administrative Scripts": `export_openapi_schema.py`, `classify_openapi_diff.py`) and §1 (module/layer layout referenced by the architectural-invariant placeholder)
**Status:** NEW — this file does not exist in the corpus today; Phase 1 CI/CD is a confirmed, total gap

**Do not re-litigate:** the backend (FastAPI, 12 bounded contexts, Testcontainers-based `conftest.py`, `export_openapi_schema.py`/`classify_openapi_diff.py`), the Admin Portal (Next.js App Router, Zod validation, a generated OpenAPI TypeScript client), and the KMP/CMP mobile app (all `core-*` modules + `kmpplayer`, Gradle-based) are **fully implemented**. This document builds none of that application code. It builds the CI harness that lints, statically analyzes, tests, and packages what already exists — every `run:` step below invokes a command against code this document treats as fixed.

---

## 1. Objective and Purpose

Give the NoorHeroes monorepo a working, GitHub-Actions-based CI pipeline covering **stages 1 through 7 of the 13-stage pipeline** defined in `NoorHeroes_Final_Development_Prompt.md` §6:

1. Lint & format check
2. Static analysis / type check (mypy / `tsc --noEmit` / detekt)
3. Secret scan (gitleaks)
4. Unit tests (parallelized)
5. Integration tests (Testcontainers-backed for backend; MSW-backed for admin-web)
6. Architectural invariant tests (CI-blocking, separately-named required status check)
7. Build artifact (Docker image for backend/admin-web; APK/AAB for Android)

Stages 8–13 are explicitly **out of scope** for this file and are owned elsewhere:

| Stage(s) | Name | Owning file |
|---|---|---|
| 8 | Container/dependency scan (Trivy/Grype; `pip-audit`/`pnpm audit`/Gradle dependency check) | `CI_CD.07` (security scan) |
| 9–10 | Deploy to staging; E2E smoke tests against staging | `CI_CD.08` (staging deploy/smoke) |
| 11–13 | Manual promotion gate; production deploy; post-deploy smoke + Sentry release health check | `CI_CD.09` (manual promotion/prod deploy) |

Today, **none of this exists**. There is no `.github/workflows/` content beyond what item 02 (`secret-scan.yml`) has already built. A trivial one-line PR against `backend/`, `admin-web/`, or `mobile/` currently triggers nothing — no lint feedback, no test run, no build validation. This file closes that gap: after implementation, opening a PR against any of the three apps triggers a deterministic, fail-fast, required-status-check-gated pipeline that a reviewer and `Repo.03`'s branch-protection rule can both trust.

**What "done" looks like, concretely:** a developer pushes a one-line typo fix to `backend/src/noorheroes/modules/rewards/service.py`. Within minutes, GitHub shows six required checks running against `Backend CI`, each individually pass/fail-visible in the PR's checks tab, in this order: lint → static analysis → unit tests → integration tests → architectural invariant tests → build artifact. `admin-web` and `mobile` workflows do not even trigger (path-filtered, nothing under their trees changed). Merge is blocked until every triggered required check is green.

## 2. Scope and Requirements

**In scope:**
- `.github/workflows/backend.yml` — Stages 1–2, 4–7 for `backend/` (Stage 3 is referenced, not re-implemented — see §2's "explicitly not rebuilt" note below).
- `.github/workflows/admin-web.yml` — Stages 1–2, 4–7 for `admin-web/`.
- `.github/workflows/mobile.yml` — Stages 1–2, 4–7 for `mobile/`.
- `.github/workflows/openapi-sync.yml` — the shared workflow named in Final_Development_Prompt §6's pipeline intro: regenerates `admin-web`'s TypeScript client from the backend's OpenAPI schema whenever `backend/` changes, and fails the build on an undiffed breaking change.
- The Stage 6 architectural-invariant **placeholder** test file per app (one real, minimal, passing seed test each — not a fake/`exit 0` stub — see §5) plus the job wiring that `Development_Blueprints.Phase9_CrossPlatform.CrossPlatform.01` will later extend with the full F.37 invariant suite.
- Caching strategy for all three toolchains (`uv`, `pnpm`, Gradle).
- The concrete list of required-status-check strings this file produces, handed off to `Repo.03`'s branch-protection script (`infra/ci/configure-branch-protection.sh`) as documented input — this file does **not** call `gh api` itself; that mechanism belongs to `Repo.03`.

**Explicitly not rebuilt here (already owned elsewhere):**
- **Stage 3, secret scanning itself.** `Infra.02` already builds a dedicated, always-triggered `.github/workflows/secret-scan.yml` running `gitleaks-scan` and `trufflehog-verified-scan` as independent required status checks on every push/PR, per that file's own §11 integration note: *"item 06 ('CI stages 1–7') should add the `check_env_example_sync`/`check-env-example-sync` step calls into its own lint-stage job... item 06 does not need to re-implement secret scanning, only wire in the two drift-check script invocations."* This file honors that boundary exactly: `backend.yml`'s and `admin-web.yml`'s `lint` jobs each gain one extra `run:` step invoking the already-written drift-check script (§4.1), and Stage 3 in every stage-diagram in this document is drawn as a pass-through reference to `secret-scan.yml`, never a job this file defines.
- **Stage 8+ (container/dependency scan, staging deploy, promotion, prod deploy)** — see the table in §1.
- **Application code changes** to `backend/src/noorheroes/**`, `admin-web/src/**`, or `mobile/**` — this file only adds CI plumbing around existing, working code. The one narrow exception is the Stage 6 placeholder test *files themselves* (new, additive test files under each app's existing test tree — never a change to non-test source).
- **The production `backend/Dockerfile` / admin-web's production `Dockerfile`** — both already exist per the monorepo tree (`Final_Development_Prompt.md` §2.1, confirmed again by `Infra.03`'s §5: *"`backend/Dockerfile` # production multi-stage build — EXISTING, do not modify here"*). Stage 7 in this file builds and (on `main`) pushes those existing Dockerfiles; it does not author them.
- **Android app signing keystore provisioning** — this file consumes a keystore via GitHub Secrets (§9) but does not generate, rotate, or store that keystore; that is a one-time manual/`Infra.02`-adjacent secrets-provisioning action, referenced not owned.

## 3. Technical Implementation Details

### 3.1 Tool choices per app, confirmed against source docs (no substitutions)

| App | Lint (Stage 1) | Static analysis (Stage 2) | Unit test (Stage 4) | Integration test (Stage 5) | Build artifact (Stage 7) |
|---|---|---|---|---|---|
| `backend/` | `ruff check .` + `ruff format --check .` | `mypy --strict` + `bandit -r src/` | `pytest tests/unit -n auto --cov` | `pytest tests/integration -n auto` (Testcontainers, real Postgres+Redis) | `docker build` (multi-stage `backend/Dockerfile`) → GHCR |
| `admin-web/` | `eslint` (`next/core-web-vitals` + `typescript-eslint` strict) + `prettier --check` | `tsc --noEmit` (build-blocking) | `vitest run --coverage` | `vitest run` against RTL + MSW-mocked API | `docker build` (Next.js standalone output) → GHCR |
| `mobile/` | `ktlintCheck` | `detekt` + `lint` (Android Lint) | `testDebugUnitTest` (JUnit5 + MockK) | `testDebugUnitTest --tests "*IntegrationTest"` (Robolectric-backed, see §3.3) | `assembleDebug` (PR) / `bundleRelease` (main) |

### 3.2 Dependency-manager / package-manager decisions (resolving Final_Development_Prompt §3's open choices)

Final_Development_Prompt §3 leaves the backend and admin-web package managers as "pick one." `Infra.03` already made the backend choice for local dev; this file adopts the **same** choice for CI so the two never diverge:

- **Backend: `uv`** (matches `Infra.03` §18 item 1's decision — reconcile against `backend/pyproject.toml`'s actual `[project]`/`[tool.poetry]` table at implementation time exactly as that file's own caveat describes; do not re-decide independently here).
- **Admin-web: `pnpm`** (explicitly named in Final_Development_Prompt §3: *"`pnpm` (faster, disk-efficient over `npm`) with `pnpm-lock.yaml` committed"* — no ambiguity to resolve).
- **Mobile: Gradle + Version Catalog** (`gradle/libs.versions.toml`) — no ambiguity, already the stack's only choice.

### 3.3 Mobile integration tests run on the JVM (Robolectric), not a real emulator — a deliberate scope decision

Final_Development_Prompt §5's Mobile Integration row specifies: *"Instrumented tests against an in-memory SQLDelight DB, fake Ktor engine."* Nothing in that description requires a physical/virtual Android device — an in-memory SQLDelight driver and a fake (`MockEngine`) Ktor client are both pure-JVM concerns. This file therefore runs these tests via **Robolectric** on `testDebugUnitTest` (fast, no emulator boot, no KVM/hardware-acceleration requirement on the GitHub-hosted runner) rather than `connectedDebugAndroidTest` against `reactivecircus/android-emulator-runner`. A true on-device instrumented suite (screenshot/E2E, per Final_Development_Prompt §1.1/§5) is explicitly **deferred post-MVP** by the source document itself — this decision is consistent with that deferral, not a new one. If a future need arises for real-emulator instrumented tests before that deferral lifts, that is a scoped addition to `mobile.yml`'s integration-test job, not a restructuring of this file. See §18 item 4.

### 3.4 Runner OS, JDK, concurrency

- All three workflows run on `ubuntu-latest` GitHub-hosted runners. Mobile does not need macOS at this stage — CMP's Android target builds identically to any other Gradle/Kotlin project on Linux; the future iOS target (out of scope until CMP iOS work begins) is the only thing that would require a macOS runner, and that is not part of Phase 1.
- Mobile jobs install **Temurin JDK 17** (`actions/setup-java@v4`) ahead of any Gradle invocation — AGP 8.x and current Kotlin/Compose Multiplatform tooling require JDK 17+; GitHub's `ubuntu-latest` image ships multiple JDKs but does not default to 17, so this must be explicit, not assumed.
- Every workflow sets a `concurrency` group keyed on `${{ github.workflow }}-${{ github.ref }}` with `cancel-in-progress: true` — a second push to the same PR branch cancels the in-flight run for the first, avoiding wasted runner-minutes on superseded commits (this matters specifically because Stage 7's Docker/Gradle builds are the most expensive steps in each pipeline).

## 4. Architecture and Component Responsibilities

```text
┌──────────────────────────────────────────────────────────────────────────────────┐
│ PR opened / pushed against `backend/**`, `admin-web/**`, or `mobile/**`            │
└───────────────┬───────────────────────┬───────────────────────┬──────────────────┘
                 │ (path-filtered)       │ (path-filtered)       │ (path-filtered)
                 ▼                       ▼                       ▼
        ┌────────────────┐      ┌────────────────┐      ┌────────────────┐
        │  backend.yml    │      │ admin-web.yml   │      │  mobile.yml     │
        └────────┬────────┘      └────────┬────────┘      └────────┬────────┘
                 │  needs: chain (fail fast, cheapest first)         │
                 ▼                       ▼                       ▼
      1  lint ─────────────────  lint ─────────────────  lint
         │ (+ env-sync check)      │ (+ env-sync check)      │ (ktlintCheck)
      2  static-analysis ───────  static-analysis ───────  static-analysis
         (mypy + bandit)           (tsc --noEmit)            (detekt + lint)
      3  [secret-scan.yml — separate, always-triggered workflow, Infra.02 — not a `needs:` dependency of this chain]
      4  unit-test ─────────────  unit-test ─────────────  unit-test
         (pytest -n auto)          (vitest --coverage)       (testDebugUnitTest)
      5  integration-test ──────  integration-test ──────  integration-test
         (pytest + Testcontainers) (vitest + RTL/MSW)        (Robolectric)
      6  architectural-invariant  architectural-invariant  architectural-invariant
         [PLACEHOLDER — seed test, Phase9.CrossPlatform.01 extends]
      7  build-artifact ────────  build-artifact ────────  build-artifact
         (docker build → GHCR)     (docker build → GHCR)     (assembleDebug/bundleRelease)

        ┌─────────────────────────────────────────────────────────────┐
        │ .github/workflows/openapi-sync.yml (triggered on backend/** )│
        │  generate-and-diff: export_openapi_schema.py → diff via      │
        │  classify_openapi_diff.py → regenerate admin-web's TS client │
        │  → fail build if an undiffed BREAKING change is detected     │
        └─────────────────────────────────────────────────────────────┘

  All required-status-check names below feed into Repo.03's branch-protection
  required-checks list (that file's mechanism, this file's job names as input).
```

**Component responsibilities:**

| Component | Responsibility |
|---|---|
| `backend.yml` / `admin-web.yml` / `mobile.yml` | Own Stages 1, 2, 4, 5, 6, 7 for their app, as one linear `needs:`-chained job DAG per app (fail fast — a `lint` failure skips every later job automatically via `needs:` propagation, no wasted compute on a doomed PR). |
| `openapi-sync.yml` | Owns the backend↔admin-web API-contract synchronization named in Final_Development_Prompt §6's pipeline intro — distinct from, and additional to, the per-app Stages 1–7. |
| `secret-scan.yml` (Infra.02, referenced not owned) | Owns Stage 3 in full. This file's only touchpoint is the two `check-env-example-sync` script invocations added to the `lint` jobs (§4.1) — a narrower, additive concern (env-var drift, not secret content) that legitimately belongs in the lint stage rather than the secret-scan workflow. |
| Each app's `architectural-invariant` job | Runs today's seed test (§5) and is the fixed integration point `Development_Blueprints.Phase9_CrossPlatform.CrossPlatform.01` targets — that file adds test files under the same directories this file creates, changing zero YAML in this file's workflows. |
| `Repo.03`'s `infra/ci/configure-branch-protection.sh` | Not modified by this file, but consumes this file's job-name output (§13) as the required-status-checks list to register. |

### 4.1 The one `secret-scan`-adjacent step this file does own

Per `Infra.02`'s explicit hand-off, each of `backend.yml`'s and `admin-web.yml`'s `lint` jobs gets exactly one additional step:

```yaml
      - name: Check .env.example is in sync with typed config
        run: uv run python -m src.noorheroes.scripts.check_env_example_sync   # backend.yml
        # admin-web.yml equivalent:
        # run: pnpm check-env-example-sync
```

This step's script is authored and owned by `Infra.02` (§3.3 of that file); this file only adds the `run:` line invoking it, exactly as that file's §11 instructs.

## 5. APIs, Models, Interfaces, and Data Flow — the Stage 6 placeholder design

This is the section that most needs precision, because "architectural invariant test placeholder" is easy to build wrong in either direction: a job that always trivially passes teaches the team the check is decorative (dangerous once `Phase9.CrossPlatform.01` lands real, high-stakes tests into the same slot); a job that always fails blocks every PR indefinitely until a much later phase ships. Neither is acceptable. The correct design, used identically for all three apps:

**Each app gets one real, minimal, currently-passing invariant test — not a no-op — that is a genuine, useful instance of the F.37 invariant category, small enough to write today, and structured so `Phase9.CrossPlatform.01` adds sibling test functions to the same file/directory rather than replacing anything.**

| App | Placeholder test file | What it actually asserts today | F.37 category it seeds |
|---|---|---|---|
| `backend/` | `backend/tests/architectural/test_jwt_schema_singularity.py` | Exactly one class named `JwtClaims` (or equivalent canonical claims model) is importable from the codebase — implemented via an AST/`ast.walk` scan of `src/noorheroes/**/*.py` asserting the count of top-level class definitions named `JwtClaims` equals exactly 1, and that it lives at the expected canonical path (`src/noorheroes/core/security.py` or wherever `create_access_token`'s `claims: JwtClaims` parameter type is actually defined per `FAST-API-INSTRUCTIONS.md` §2). | "Test confirming the JWT claim schema has exactly one canonical definition" — the third item in Final_Development_Prompt §5's Architectural test row. |
| `admin-web/` | `admin-web/tests/architectural/rbac-route-guard.spec.ts` (Playwright) | The `(support)` route group's middleware guard actually rejects a forged JWT whose `scopes` claim omits `admin:write` — i.e., a `403`/redirect happens before any Server Component under `(support)` renders, proven with one seeded low-privilege token against one representative Publisher-only route. | Seeds the "RBAC-boundary Playwright tests" row — a Support Agent token cannot reach a Publisher-only mutation. |
| `mobile/` | `mobile/core/core-security/src/commonTest/kotlin/ArchitecturalInvariantTest.kt` | A source-scan test (not a runtime test) walking `core-*`/`feature/*` `commonMain` source files and asserting zero matches for a raw `SharedPreferences.putString`/`NSUserDefaults` call whose argument name matches a `pin|password|credential|hash` pattern outside `core-security/`. | "Test confirming no raw `SharedPreferences.putString`/`NSUserDefaults` call touches PIN/pattern/hash-typed variables outside `core-security`'s abstraction" — the mobile row's exact wording in Final_Development_Prompt §5. |

Each seed test is deliberately chosen because (a) it is independently valuable today, not manufactured busywork, (b) it requires zero new application code to pass — it only inspects/exercises what already exists, and (c) it is exactly the pattern `Phase9.CrossPlatform.01`'s remaining invariant tests (gateway-zero-authorization, Argon2id-only hashing, upload-pipeline ordering, gateway-bypass simulation) will follow, so that file's job is "add more files to this directory," never "rewrite this job's YAML."

**Job-level framing, identical across all three workflows:** the job step list includes a clearly-worded, non-alarming banner step before running the actual test command:

```yaml
      - name: Architectural invariant suite status
        run: |
          echo "::notice::Running the Phase 1 seed invariant test only."
          echo "::notice::The full F.37 architectural invariant suite is built by Development_Blueprints.Phase9_CrossPlatform.CrossPlatform.01 — this job's test count will grow, its job name and required-status-check status will not change."
```

This keeps the job's required-status-check identity (§13) stable across the months between this file's implementation and Phase 9's, so `Repo.03`'s branch protection never needs a required-check rename mid-project.

## 6. Folder/File Structure

```text
noorheroes/
├── .github/
│   └── workflows/
│       ├── backend.yml                # NEW — this blueprint
│       ├── admin-web.yml              # NEW — this blueprint
│       ├── mobile.yml                 # NEW — this blueprint
│       ├── openapi-sync.yml           # NEW — this blueprint
│       └── secret-scan.yml            # EXISTING (Infra.02) — not touched here
├── backend/
│   ├── tests/
│   │   ├── unit/                      # EXISTING — this file only invokes it
│   │   ├── integration/               # EXISTING — this file only invokes it
│   │   ├── conftest.py                # EXISTING — Testcontainers harness, not modified
│   │   └── architectural/             # NEW (this blueprint) — Stage 6 placeholder lives here
│   │       └── test_jwt_schema_singularity.py   # NEW
│   ├── src/noorheroes/scripts/
│   │   ├── export_openapi_schema.py   # EXISTING — invoked by openapi-sync.yml
│   │   └── classify_openapi_diff.py   # EXISTING — invoked by openapi-sync.yml
│   ├── pyproject.toml                 # EXISTING — read (ruff/mypy/pytest config sections), not restructured
│   └── Dockerfile                     # EXISTING — built (not authored) by backend.yml's build-artifact job
├── admin-web/
│   ├── tests/
│   │   ├── unit/                      # EXISTING
│   │   ├── integration/               # EXISTING (RTL + MSW)
│   │   └── architectural/             # NEW (this blueprint)
│   │       └── rbac-route-guard.spec.ts         # NEW
│   ├── src/lib/api-client/            # EXISTING — regenerated in place by openapi-sync.yml
│   ├── package.json                   # EXISTING — read for existing `lint`/`test`/`build` scripts; new scripts appended, not replaced
│   └── Dockerfile                     # EXISTING
├── mobile/
│   ├── core/core-security/src/commonTest/kotlin/
│   │   └── ArchitecturalInvariantTest.kt        # NEW (this blueprint)
│   ├── gradle/libs.versions.toml      # EXISTING — read, not modified
│   └── build.gradle.kts               # EXISTING — a `detekt`/`ktlint` plugin block may need to be confirmed present (§14 step 2), not authored fresh
└── docs/adr/                          # any ADR this blueprint's implementation produces (e.g. Ruff-only vs Ruff+Black) lands here per Final_Development_Prompt §2.3
```

## 7. Dependencies, Configuration, and the Full Workflow YAML

### 7.1 `.github/workflows/backend.yml`

```yaml
name: Backend CI

on:
  push:
    branches: [main]
    paths: ["backend/**", ".github/workflows/backend.yml"]
  pull_request:
    paths: ["backend/**", ".github/workflows/backend.yml"]

concurrency:
  group: backend-ci-${{ github.ref }}
  cancel-in-progress: true

defaults:
  run:
    working-directory: backend

env:
  UV_VERSION: "0.5.11"   # re-verify current stable at implementation time, per Final_Development_Prompt §1's pinning discipline

jobs:
  lint:
    name: Lint & Format (ruff)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
        with:
          version: ${{ env.UV_VERSION }}
          enable-cache: true
          cache-dependency-glob: "backend/uv.lock"
      - run: uv sync --frozen
      - name: ruff check
        run: uv run ruff check . --output-format=github
      - name: ruff format --check
        run: uv run ruff format --check .
      - name: Check .env.example is in sync with typed config
        run: uv run python -m src.noorheroes.scripts.check_env_example_sync   # owned by Infra.02, invoked here per §4.1

  static-analysis:
    name: Static Analysis (mypy + bandit)
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
        with:
          version: ${{ env.UV_VERSION }}
          enable-cache: true
          cache-dependency-glob: "backend/uv.lock"
      - run: uv sync --frozen
      - name: mypy --strict
        run: uv run mypy --strict src/
      - name: bandit
        run: uv run bandit -r src/ -ll -c pyproject.toml

  unit-test:
    name: Unit Tests (pytest)
    needs: static-analysis
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
        with:
          version: ${{ env.UV_VERSION }}
          enable-cache: true
          cache-dependency-glob: "backend/uv.lock"
      - run: uv sync --frozen
      - name: pytest (unit, parallelized)
        run: |
          uv run pytest tests/unit -n auto \
            --cov=src/noorheroes --cov-report=xml --cov-report=term-missing \
            --cov-fail-under=80
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: backend-unit-coverage
          path: backend/coverage.xml
          retention-days: 14

  integration-test:
    name: Integration Tests (pytest + Testcontainers)
    needs: static-analysis
    runs-on: ubuntu-latest   # Docker Engine is preinstalled — Testcontainers needs no `services:` block, no DIND setup
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
        with:
          version: ${{ env.UV_VERSION }}
          enable-cache: true
          cache-dependency-glob: "backend/uv.lock"
      - run: uv sync --frozen
      - name: pytest (integration, Testcontainers-backed)
        run: uv run pytest tests/integration -n auto --reruns 1 --reruns-delay 3 -m "not flaky"
        # --reruns 1: absorbs a single transient container-startup flake (§10); -m "not flaky"
        # excludes tests explicitly quarantined per §10's flaky-test policy, never a blanket retry-until-green.
        env:
          TESTCONTAINERS_RYUK_DISABLED: "false"   # keep Ryuk's reaper on — ensures orphaned containers are cleaned up even on a cancelled run

  architectural-invariant:
    name: Architectural Invariant Tests [PLACEHOLDER]
    needs: [unit-test, integration-test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
        with:
          version: ${{ env.UV_VERSION }}
          enable-cache: true
          cache-dependency-glob: "backend/uv.lock"
      - run: uv sync --frozen
      - name: Architectural invariant suite status
        run: |
          echo "::notice::Running the Phase 1 seed invariant test only."
          echo "::notice::The full F.37 suite is built by Development_Blueprints.Phase9_CrossPlatform.CrossPlatform.01."
      - name: Run architectural invariant tests
        run: uv run pytest tests/architectural -v

  build-artifact:
    name: Build Docker Image
    needs: architectural-invariant
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - name: Log in to GHCR
        if: github.event_name == 'push'
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - name: Build (and push on main only)
        uses: docker/build-push-action@v6
        with:
          context: backend
          file: backend/Dockerfile
          push: ${{ github.event_name == 'push' }}
          tags: |
            ghcr.io/${{ github.repository_owner }}/noorheroes-backend:sha-${{ github.sha }}
            ${{ github.event_name == 'push' && format('ghcr.io/{0}/noorheroes-backend:latest', github.repository_owner) || '' }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
      - name: Sanity-run built image (PR validation only)
        if: github.event_name == 'pull_request'
        run: docker run --rm ghcr.io/${{ github.repository_owner }}/noorheroes-backend:sha-${{ github.sha }} python -c "import src.noorheroes.main" || true
        # Best-effort import smoke check — never blocks the job on this alone; the real gate is the build succeeding at all.
```

### 7.2 `.github/workflows/admin-web.yml`

```yaml
name: Admin Web CI

on:
  push:
    branches: [main]
    paths: ["admin-web/**", ".github/workflows/admin-web.yml"]
  pull_request:
    paths: ["admin-web/**", ".github/workflows/admin-web.yml"]

concurrency:
  group: admin-web-ci-${{ github.ref }}
  cancel-in-progress: true

defaults:
  run:
    working-directory: admin-web

jobs:
  lint:
    name: Lint & Format (eslint + prettier)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "22"
          cache: pnpm
          cache-dependency-path: admin-web/pnpm-lock.yaml
      - run: pnpm install --frozen-lockfile
      - name: eslint
        run: pnpm eslint . --max-warnings=0
      - name: prettier --check
        run: pnpm prettier --check .
      - name: Check .env.example is in sync with typed config
        run: pnpm check-env-example-sync   # owned by Infra.02, invoked here per §4.1

  static-analysis:
    name: Type Check (tsc --noEmit)
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "22"
          cache: pnpm
          cache-dependency-path: admin-web/pnpm-lock.yaml
      - run: pnpm install --frozen-lockfile
      - run: pnpm tsc --noEmit

  unit-test:
    name: Unit Tests (vitest)
    needs: static-analysis
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "22"
          cache: pnpm
          cache-dependency-path: admin-web/pnpm-lock.yaml
      - run: pnpm install --frozen-lockfile
      - name: vitest (unit, coverage-gated)
        run: pnpm vitest run --coverage --coverage.thresholds.lines=70 --coverage.thresholds.functions=70
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: admin-web-unit-coverage
          path: admin-web/coverage
          retention-days: 14

  integration-test:
    name: Integration Tests (RTL + MSW)
    needs: static-analysis
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "22"
          cache: pnpm
          cache-dependency-path: admin-web/pnpm-lock.yaml
      - run: pnpm install --frozen-lockfile
      - name: vitest (integration, MSW-mocked API)
        run: pnpm vitest run --config vitest.integration.config.ts

  architectural-invariant:
    name: Architectural Invariant Tests [PLACEHOLDER]
    needs: [unit-test, integration-test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "22"
          cache: pnpm
          cache-dependency-path: admin-web/pnpm-lock.yaml
      - run: pnpm install --frozen-lockfile
      - run: npx playwright install --with-deps chromium
      - name: Architectural invariant suite status
        run: |
          echo "::notice::Running the Phase 1 seed invariant test only."
          echo "::notice::The full RBAC-boundary suite is built by Development_Blueprints.Phase9_CrossPlatform.CrossPlatform.01."
      - name: Run architectural invariant tests
        run: pnpm playwright test tests/architectural

  build-artifact:
    name: Build Docker Image
    needs: architectural-invariant
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - name: Log in to GHCR
        if: github.event_name == 'push'
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v6
        with:
          context: admin-web
          file: admin-web/Dockerfile
          push: ${{ github.event_name == 'push' }}
          tags: |
            ghcr.io/${{ github.repository_owner }}/noorheroes-admin-web:sha-${{ github.sha }}
            ${{ github.event_name == 'push' && format('ghcr.io/{0}/noorheroes-admin-web:latest', github.repository_owner) || '' }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### 7.3 `.github/workflows/mobile.yml`

```yaml
name: Mobile CI

on:
  push:
    branches: [main]
    paths: ["mobile/**", ".github/workflows/mobile.yml"]
  pull_request:
    paths: ["mobile/**", ".github/workflows/mobile.yml"]

concurrency:
  group: mobile-ci-${{ github.ref }}
  cancel-in-progress: true

defaults:
  run:
    working-directory: mobile

jobs:
  lint:
    name: Lint & Format (ktlint)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { distribution: temurin, java-version: "17" }
      - uses: gradle/actions/setup-gradle@v4
      - run: ./gradlew ktlintCheck --no-daemon

  static-analysis:
    name: Static Analysis (detekt + Android Lint)
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { distribution: temurin, java-version: "17" }
      - uses: gradle/actions/setup-gradle@v4
      - run: ./gradlew detekt lint --no-daemon
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: mobile-detekt-report
          path: "mobile/**/build/reports/detekt/*.html"
          retention-days: 14

  unit-test:
    name: Unit Tests (JVM)
    needs: static-analysis
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { distribution: temurin, java-version: "17" }
      - uses: gradle/actions/setup-gradle@v4
      - name: Run all module unit tests (parallelized by Gradle's own workers)
        run: ./gradlew testDebugUnitTest --parallel --no-daemon
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: mobile-unit-test-results
          path: "mobile/**/build/test-results/testDebugUnitTest/*.xml"
          retention-days: 14

  integration-test:
    name: Integration Tests (Robolectric)
    needs: static-analysis
    runs-on: ubuntu-latest   # Robolectric is a JVM library — no emulator/KVM required, see §3.3
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { distribution: temurin, java-version: "17" }
      - uses: gradle/actions/setup-gradle@v4
      - name: Run Robolectric-backed integration tests
        run: ./gradlew testDebugUnitTest --tests "*IntegrationTest" --parallel --no-daemon

  architectural-invariant:
    name: Architectural Invariant Tests [PLACEHOLDER]
    needs: [unit-test, integration-test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { distribution: temurin, java-version: "17" }
      - uses: gradle/actions/setup-gradle@v4
      - name: Architectural invariant suite status
        run: |
          echo "::notice::Running the Phase 1 seed invariant test only."
          echo "::notice::The full no-raw-credential-prefs suite is built by Development_Blueprints.Phase9_CrossPlatform.CrossPlatform.01."
      - run: ./gradlew :core-security:allTests --tests "*ArchitecturalInvariantTest" --no-daemon

  build-artifact:
    name: Build APK/AAB
    needs: architectural-invariant
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { distribution: temurin, java-version: "17" }
      - uses: gradle/actions/setup-gradle@v4
      - name: Build debug APK (every PR)
        run: ./gradlew :androidApp:assembleDebug --no-daemon
      - uses: actions/upload-artifact@v4
        with:
          name: noorheroes-debug-apk
          path: "mobile/androidApp/build/outputs/apk/debug/*.apk"
          retention-days: 14
      - name: Decode release keystore
        if: github.event_name == 'push'
        run: echo "${{ secrets.ANDROID_KEYSTORE_BASE64 }}" | base64 -d > /tmp/release.keystore
      - name: Build signed release AAB (main only)
        if: github.event_name == 'push'
        env:
          ANDROID_KEYSTORE_PATH: /tmp/release.keystore
          ANDROID_KEYSTORE_PASSWORD: ${{ secrets.ANDROID_KEYSTORE_PASSWORD }}
          ANDROID_KEY_ALIAS: ${{ secrets.ANDROID_KEY_ALIAS }}
          ANDROID_KEY_PASSWORD: ${{ secrets.ANDROID_KEY_PASSWORD }}
        run: ./gradlew :androidApp:bundleRelease --no-daemon
      - uses: actions/upload-artifact@v4
        if: github.event_name == 'push'
        with:
          name: noorheroes-release-aab
          path: "mobile/androidApp/build/outputs/bundle/release/*.aab"
          retention-days: 90
```

### 7.4 `.github/workflows/openapi-sync.yml`

```yaml
name: OpenAPI Client Sync

on:
  pull_request:
    paths: ["backend/**", ".github/workflows/openapi-sync.yml"]
  push:
    branches: [main]
    paths: ["backend/**"]

concurrency:
  group: openapi-sync-${{ github.ref }}
  cancel-in-progress: true

jobs:
  generate-and-diff:
    name: Generate & Diff OpenAPI Client
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
        with: { enable-cache: true, cache-dependency-glob: "backend/uv.lock" }
      - working-directory: backend
        run: uv sync --frozen
      - name: Export current OpenAPI schema
        working-directory: backend
        run: uv run python -m src.noorheroes.scripts.export_openapi_schema --out ../openapi.current.json
      - name: Classify diff against baseline
        working-directory: backend
        run: |
          uv run python -m src.noorheroes.scripts.classify_openapi_diff \
            --baseline ../openapi.baseline.json --current ../openapi.current.json \
            --fail-on-breaking
        # classify_openapi_diff.py (existing) exits non-zero on an undiffed breaking change,
        # per Final_Development_Prompt §6's pipeline intro requirement. `openapi.baseline.json`
        # is committed at repo root and only ever updated by a PR that explicitly acknowledges
        # a breaking change (e.g. bumping /v1 → /v2) — see §10's edge-case row.
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with: { node-version: "22", cache: pnpm, cache-dependency-path: admin-web/pnpm-lock.yaml }
      - working-directory: admin-web
        run: pnpm install --frozen-lockfile
      - name: Regenerate admin-web's TypeScript client
        working-directory: admin-web
        run: pnpm generate:api-client --input ../openapi.current.json
      - name: Fail if regenerated client differs from committed client (on PR)
        if: github.event_name == 'pull_request'
        run: |
          git diff --exit-code -- admin-web/src/lib/api-client/generated/ || \
          (echo "::error::admin-web's generated OpenAPI client is stale — run 'pnpm generate:api-client' locally and commit the diff." && exit 1)
      - name: Commit regenerated client (on main, non-breaking changes only)
        if: github.event_name == 'push' && success()
        run: |
          git config user.name "noorheroes-ci"
          git config user.email "ci@noorheroes.internal"
          git add admin-web/src/lib/api-client/generated/ openapi.baseline.json
          git diff --cached --quiet || git commit -m "chore(admin-web): regenerate OpenAPI client [skip ci]"
          git push
```

## 8. Database/Storage Requirements

- **Backend unit tests (Stage 4):** no database — service-layer logic is exercised with repository mocks per Final_Development_Prompt §5's Unit row (`"service-layer logic isolated from DB via repository mocks"`). No CI service container needed.
- **Backend integration tests (Stage 5):** real, **ephemeral** PostgreSQL 16 and Redis containers, provisioned entirely by the existing `backend/tests/conftest.py` Testcontainers harness at test-collection time — **not** by a GitHub Actions `services:` block and **not** by `Infra.03`'s `infra/docker-compose.yml` (that file's own §12 explicitly forbids this file from pointing at it — see this file's own §12 below). `ubuntu-latest` ships Docker Engine pre-installed, so `testcontainers-python` works with zero additional runner configuration; `integration-test`'s job steps in §7.1 install nothing beyond the Python toolchain. Each CI run's containers are created and destroyed within that single job's lifetime — no state persists between runs, matching the "no shared mutable state between runs" requirement in Final_Development_Prompt §3's environment table.
- **admin-web integration tests (Stage 5):** no real network, no database — MSW (Mock Service Worker) intercepts `fetch`/XHR calls at the module level inside the Vitest/jsdom process. No CI service container needed.
- **Mobile integration tests (Stage 5):** in-memory SQLDelight driver (JVM in-memory JDBC, not a container, not a file-backed DB) plus a fake Ktor `MockEngine` — no external service, no container.
- **Stage 6 architectural placeholder (all three apps):** none of the three seed tests (§5) touch a database — they are source-scan/route-guard checks, deliberately chosen to need nothing beyond what's already available in the `static-analysis`/`unit-test` job environment.

## 9. Authentication, Authorization, Validation, and Security Considerations

- **`GITHUB_TOKEN` scoping:** every job that needs to push to GHCR declares `permissions: { contents: read, packages: write }` explicitly at the job level (not workflow-default `permissions: write-all`) — least-privilege, matching the repo-wide default GitHub now recommends and explicit enough that a future job added to these files doesn't inherit unintended write access.
- **Android signing secrets:** `ANDROID_KEYSTORE_BASE64`, `ANDROID_KEYSTORE_PASSWORD`, `ANDROID_KEY_ALIAS`, `ANDROID_KEY_PASSWORD` are GitHub Actions repository secrets (never committed, never printed — `base64 -d` output is redirected straight to a file, never echoed). The decoded keystore file is written to `/tmp/` on an ephemeral runner that is destroyed at job end; it is never uploaded as a workflow artifact or cached. Provisioning the actual keystore file/secret values is out of this file's scope (§2) — coordinate with whoever owns Android release signing key custody.
- **No production credentials of any kind appear in `backend.yml`/`admin-web.yml`'s test jobs** — Stage 4/5 tests run against Testcontainers-provisioned ephemeral databases with throwaway, CI-only credentials (matching Final_Development_Prompt §3's "these are throwaway per-run credentials, not real secrets — safe to hardcode," per `Infra.02`'s own note on this exact point) and MSW-mocked/fake network layers; no `.env`, no GCP Secret Manager call, no real third-party API key is exercised in Stages 1–7 at all.
- **`fail-under` coverage gates are security-relevant, not just quality-relevant, on two specific paths:** the backend's `--cov-fail-under=80` threshold is scoped at the whole-package level in this baseline implementation but must, per Final_Development_Prompt §5's coverage-gates row, specifically guarantee `domain/` service-layer coverage — implementers must confirm `backend/pyproject.toml`'s `[tool.coverage.run]`/`[tool.pytest.ini_options]` `--cov` target (or a dedicated `--cov=src/noorheroes/modules` invocation) actually measures the `service.py` layer per bounded context, not just an aggregate that could hide a fully-untested `rewards/service.py` behind well-tested `identity/service.py`. Flagged here because reward-ledger and JWT-adjacent service code are explicitly named in Final_Development_Prompt §2.3 as "highest blast radius" — an aggregate-only coverage gate is a real gap, not a nitpick.
- **The `check-env-example-sync` steps (§4.1) are a validation control, not a scanning control** — they catch "a new required config var was added to `Settings`/`env.ts` but `.env.example` wasn't updated," a correctness/onboarding issue. They are not a substitute for `secret-scan.yml`'s actual content-based scanning and must never be described as such in a PR review comment or documentation cross-reference.
- **Stage 6 placeholder tests must never be written as `assert True`/`pass`-only stubs** (§5) — an always-green architectural-invariant job that asserts nothing is a worse security posture than no job at all, because it creates false confidence that the category is covered.

## 10. Error Handling and Edge Cases

| Situation | Cause | Resolution |
|---|---|---|
| `lint` job fails | Real lint/format violation | Job fails fast (it's first in the `needs:` chain); every downstream job for that app is skipped automatically by GitHub Actions' `needs:` semantics — no wasted runner-minutes on `static-analysis`/`unit-test`/etc. |
| `integration-test` fails once, transiently, with a Testcontainers "container failed to start" error | Docker daemon cold-start contention on a shared runner, or a slow image pull on first use | `pytest-rerunfailures`'s `--reruns 1 --reruns-delay 3` (already wired in §7.1) absorbs exactly one such transient failure. This is a narrow, capped retry — not a loop, not applied to every test (the `-m "not flaky"` marker exclusion in the same command is the deliberate quarantine mechanism for tests that fail for a *known, tracked* reason, distinct from this blanket-but-single retry for infra flakiness). |
| A specific test is flaky for a known-but-not-yet-fixed reason (e.g., a timing-sensitive assertion) | Legitimate test-quality debt, not infra flakiness | Mark it `@pytest.mark.flaky` (backend) / `test.skip`/`.fixme` with a tracked issue link (admin-web/Playwright) / `@Ignore("NH-xxx: flaky, see issue")` (mobile) — excluded from the blocking run via the marker filter already in the integration-test step, but **must** carry a linked tracking issue in the skip reason string; an unmarked, silently-skipped test is a Definition-of-Done violation (§17). |
| `unit-test`'s coverage gate fails (`--cov-fail-under=80` / vitest `--coverage.thresholds`) | New code added without corresponding tests | Job fails, blocking merge — this is intended behavior per Final_Development_Prompt §5's coverage-gates row, not a bug to work around with a lowered threshold. |
| `openapi-sync.yml`'s `classify_openapi_diff.py` step fails on a PR | A backend change altered the OpenAPI contract in a way the script classifies as breaking, without an accompanying `/v2` path-version bump | This is the deliberate guardrail named in Final_Development_Prompt §6's pipeline intro ("fails the build on an undiffed breaking change") and cross-referenced by `Repo.03`'s §3.6 as the mechanism forcing the manual `/v1`→`/v2` decision to happen deliberately. Resolution is either (a) the change genuinely isn't breaking and the script's classification needs a narrower allowlist entry (rare, requires justification in the PR), or (b) the author introduces the `/v2` path version deliberately and updates `openapi.baseline.json` in the same PR. |
| `openapi-sync.yml`'s "Commit regenerated client" step on `main` produces an unexpected diff | The generated TS client changed in a way not caught by the PR-time check (e.g., a race between two merged PRs) | The `[skip ci]` commit re-triggers no further workflow run; a follow-up PR against `admin-web/` (if any consumer code needs updating for the new client shape) goes through the normal `admin-web.yml` pipeline as usual — this is expected, not an error state. |
| `build-artifact` (backend/admin-web) Docker layer cache (`type=gha`) is cold (first run, or after GitHub's 7-day/10 GB cache eviction) | Normal GitHub Actions cache lifecycle | Build takes longer but still succeeds — this is a performance characteristic, not a failure mode; do not add retry logic here, a cold cache is not flaky, it's just slow once. |
| Mobile `build-artifact`'s `bundleRelease` step fails specifically on `main` but `assembleDebug` passed on the same commit | Signing secrets missing/misconfigured (§9), or a Play Store-specific Gradle signing-config assertion failing | `assembleDebug` (unsigned/debug-signed, runs on every PR) succeeding while `bundleRelease` (real signing, `main`-only) fails isolates the problem to the signing configuration specifically, not the app's buildability — check secret values and the `signingConfigs` block in `androidApp/build.gradle.kts` before assuming a code regression. |
| A PR touches both `backend/**` and `admin-web/**` in one commit | Cross-cutting change (e.g., a new endpoint plus its consuming admin UI) | Both `backend.yml` and `admin-web.yml` trigger independently (path filters are not mutually exclusive), plus `openapi-sync.yml` triggers from the `backend/**` change — all three run in parallel; required-status-check gating (§13) waits on all of them, exactly as intended for a change with this blast radius. |
| A PR touches only `docs/**` or `infra/terraform/**` | No app code changed | None of `backend.yml`/`admin-web.yml`/`mobile.yml`/`openapi-sync.yml` trigger at all (path-filtered) — this is correct, not a gap; branch protection's required checks apply only to checks that were actually triggered for a given PR's changed files, per GitHub's own semantics for path-filtered required checks (confirm this is configured as "required if triggered," not "required unconditionally," when `Repo.03`'s script registers these check names — see §13's note). |

## 11. State Management and Lifecycle Considerations

- **Every job in every workflow is stateless across runs** — no CI-side database, no persisted queue, no manual approval state exists anywhere in Stages 1–7 (the first manual gate in the full 13-stage pipeline is Stage 11, owned by `CI_CD.09`). A re-run of a failed job (GitHub's native "Re-run failed jobs" UI action) is always safe and idempotent.
- **Build-artifact versioning/tagging (Stage 7's most stateful concern):** every image/APK is tagged with the immutable `sha-${{ github.sha }}` on every run (PR or `main`), so any two builds are always distinguishable and traceable to an exact commit. On `main` only, the backend and admin-web images additionally receive a floating `:latest` tag (consumed by `CI_CD.08`'s staging deploy, not built here), and the mobile release AAB is uploaded as a workflow artifact (90-day retention — long enough to bridge to `CI_CD.09`'s manual promotion step, per that file's ownership of the actual Play Console upload). This file does **not** apply `Repo.03`'s SemVer tags (`backend-vX.Y.Z`, `android-vX.Y.Z`) directly — those are computed by `semantic-release` in `Repo.03`'s own `release-backend.yml`/`release-mobile.yml` workflows, which run *after* this file's `build-artifact` jobs succeed on `main` (a `workflow_run` trigger or equivalent hand-off, owned by `Repo.03`, not this file) and then re-tag/promote the already-built `sha-`-tagged image rather than rebuilding.
- **PR-time artifacts (debug APK, coverage reports, detekt reports) use a shortened 14-day retention** — they exist to help a reviewer/debugger inspect a specific PR's output, not as a long-term archive; GitHub's default 90-day retention would accumulate unnecessary storage across a high-PR-velocity monorepo. The `main`-branch release AAB (§7.3) is the one artifact given a longer, 90-day retention, reflecting its role as a bridge to a later, human-gated promotion step.
- **Cache lifecycle:** `uv`'s cache (`astral-sh/setup-uv`'s `enable-cache: true`), `pnpm`'s cache (`actions/setup-node`'s `cache: pnpm`), and Gradle's cache (`gradle/actions/setup-gradle`'s built-in remote/local cache) are all keyed off their respective lockfiles (`uv.lock`, `pnpm-lock.yaml`, `gradle/libs.versions.toml` + wrapper checksum). A dependency bump invalidates exactly the affected cache, not the other two apps' caches — each app's cache is independent, matching the monorepo's independent-deployability principle (Final_Development_Prompt §2.1).

## 12. Integration Points with Existing Modules

- **`backend/tests/conftest.py` (Testcontainers harness) — the single most important integration point in this file.** `integration-test` (§7.1) invokes `pytest tests/integration` with **zero** CI-specific environment configuration beyond what `conftest.py` already provides — no `DATABASE_URL`/`REDIS_URL` override, no GitHub Actions `services:` block, nothing this file adds that the local `pytest` invocation from a developer's own machine wouldn't also use. This is a deliberate, load-bearing design choice: it guarantees "the test passes in CI" and "the test passes on my laptop" are the *same claim*, not two claims that happen to usually agree. Do not special-case CI inside `conftest.py` to work around anything this file's job environment lacks — if a genuine gap is found (e.g., a resource limit the runner hits that a laptop doesn't), fix the runner's job configuration (e.g., a larger `runs-on` sizing), not the test harness's portability.
- **`Infra.03`'s `infra/docker-compose.yml` — explicitly NOT an integration point.** Per that file's own §12 boundary table, this file's `integration-test` job must never point at, extend, or reuse that compose stack's fixed ports/services. The two are fully decoupled: this file provisions ephemeral, dynamically-ported containers per run via Testcontainers; `Infra.03` provisions a long-running, fixed-port stack for interactive local development. A future maintainer conflating the two (e.g., "optimizing" CI by starting `infra/docker-compose.yml` once and pointing tests at its fixed ports) would silently reintroduce shared mutable state between CI runs — exactly what Final_Development_Prompt §3's CI environment row prohibits.
- **`export_openapi_schema.py` / `classify_openapi_diff.py`** — both already implemented per `FAST-API-INSTRUCTIONS.md` §6 ("Administrative Scripts"), invoked verbatim by `openapi-sync.yml` (§7.4) via the exact module-path convention that document specifies (`python -m src.noorheroes.scripts.<name>`), run here via `uv run python -m ...` since `uv` is this file's chosen invocation wrapper.
- **Admin-web's generated OpenAPI TS client (`src/lib/api-client/`)** — regenerated by `openapi-sync.yml`, never by `admin-web.yml` itself; `admin-web.yml`'s own jobs only ever consume the client as already-generated, committed source.
- **`Infra.02`'s `secret-scan.yml`, `.gitleaks.toml`, and drift-check scripts** — referenced, not duplicated, per §2/§4.1 above.
- **`Repo.03`'s branch protection, CODEOWNERS, and SemVer release workflows** — this file is the primary *producer* of required-check names `Repo.03` consumes (§13); it is a *consumer* of `Repo.03`'s CODEOWNERS-driven review assignment (unaffected by anything in this file) and of `Repo.03`'s commit/PR-title linting (which runs in `Repo.03`'s own workflows, entirely independent of the six jobs this file defines).
- **Mobile's existing Gradle module graph (`core-*`, `feature/*`, `composeApp`)** — `mobile.yml`'s `unit-test`/`integration-test` jobs invoke root-level Gradle tasks (`testDebugUnitTest`) that Gradle itself fans out across every module in the existing multi-module graph; this file does not enumerate modules individually and does not need updating when a new `feature/*` module is added, as long as that module participates in the root `testDebugUnitTest` task graph the way every other module already does.

## 13. Development Steps in the Correct Implementation Order

1. Confirm `backend/pyproject.toml` already has `[tool.ruff]`, `[tool.mypy]`, `[tool.bandit]`, and `[tool.pytest.ini_options]` sections (or add minimal ones if genuinely absent) — this file's `run:` commands assume config lives there, not in separate `.ruff.toml`/`mypy.ini` files, matching the "one `pyproject.toml`" convention implied by `FAST-API-INSTRUCTIONS.md`'s file layout.
2. Confirm `mobile/build.gradle.kts` (root) already applies the `ktlint` and `detekt` Gradle plugins repo-wide (Final_Development_Prompt §1.1 names both as chosen tools) — add the plugin blocks if genuinely absent; do not restructure the existing module graph to do so.
3. Author `backend/tests/architectural/test_jwt_schema_singularity.py`, `admin-web/tests/architectural/rbac-route-guard.spec.ts`, and `mobile/core/core-security/src/commonTest/kotlin/ArchitecturalInvariantTest.kt` per §5's design — run each locally first and confirm it passes against the current, already-implemented codebase before wiring it into CI (a placeholder that fails on day one is a broken placeholder, not an aspirational one).
4. Author `.github/workflows/backend.yml` (§7.1) in full; push to a scratch branch; open a throwaway PR; confirm all six jobs trigger, run in the documented `needs:` order, and pass.
5. Author `.github/workflows/admin-web.yml` (§7.2); repeat step 4's verification.
6. Author `.github/workflows/mobile.yml` (§7.3); repeat step 4's verification, paying particular attention to JDK/Gradle cache warm-up time on the first run.
7. Author `.github/workflows/openapi-sync.yml` (§7.4); seed `openapi.baseline.json` at repo root from the current schema (`uv run python -m src.noorheroes.scripts.export_openapi_schema --out openapi.baseline.json`, committed once as the starting baseline); confirm the workflow triggers correctly on a `backend/**`-only PR and does *not* trigger on an `admin-web/**`-only or `mobile/**`-only PR.
8. Deliberately introduce one lint violation, one type error, one failing unit test, and one breaking OpenAPI change (each on a separate scratch branch) and confirm each is caught by exactly the job/workflow expected — this is the acceptance test in §14, not optional manual spot-checking.
9. Compile the full required-status-check name list (§13's own output, consumed by `Repo.03`) and hand it to whoever implements/re-runs `Repo.03`'s `infra/ci/configure-branch-protection.sh` — this file's implementation is not complete until those checks are actually registered as required on `main` (verified per §17).
10. Delete all scratch branches/PRs used for steps 4–9's verification once each is confirmed.

**Required-status-check names this file produces (hand-off table for `Repo.03`):**

| Workflow display name | Job display name | Full required-check string |
|---|---|---|
| Backend CI | Lint & Format (ruff) | `Backend CI / Lint & Format (ruff)` |
| Backend CI | Static Analysis (mypy + bandit) | `Backend CI / Static Analysis (mypy + bandit)` |
| Backend CI | Unit Tests (pytest) | `Backend CI / Unit Tests (pytest)` |
| Backend CI | Integration Tests (pytest + Testcontainers) | `Backend CI / Integration Tests (pytest + Testcontainers)` |
| Backend CI | Architectural Invariant Tests [PLACEHOLDER] | `Backend CI / Architectural Invariant Tests [PLACEHOLDER]` |
| Backend CI | Build Docker Image | `Backend CI / Build Docker Image` |
| Admin Web CI | Lint & Format (eslint + prettier) | `Admin Web CI / Lint & Format (eslint + prettier)` |
| Admin Web CI | Type Check (tsc --noEmit) | `Admin Web CI / Type Check (tsc --noEmit)` |
| Admin Web CI | Unit Tests (vitest) | `Admin Web CI / Unit Tests (vitest)` |
| Admin Web CI | Integration Tests (RTL + MSW) | `Admin Web CI / Integration Tests (RTL + MSW)` |
| Admin Web CI | Architectural Invariant Tests [PLACEHOLDER] | `Admin Web CI / Architectural Invariant Tests [PLACEHOLDER]` |
| Admin Web CI | Build Docker Image | `Admin Web CI / Build Docker Image` |
| Mobile CI | Lint & Format (ktlint) | `Mobile CI / Lint & Format (ktlint)` |
| Mobile CI | Static Analysis (detekt + Android Lint) | `Mobile CI / Static Analysis (detekt + Android Lint)` |
| Mobile CI | Unit Tests (JVM) | `Mobile CI / Unit Tests (JVM)` |
| Mobile CI | Integration Tests (Robolectric) | `Mobile CI / Integration Tests (Robolectric)` |
| Mobile CI | Architectural Invariant Tests [PLACEHOLDER] | `Mobile CI / Architectural Invariant Tests [PLACEHOLDER]` |
| Mobile CI | Build APK/AAB | `Mobile CI / Build APK/AAB` |
| OpenAPI Client Sync | Generate & Diff OpenAPI Client | `OpenAPI Client Sync / Generate & Diff OpenAPI Client` |

(Plus `gitleaks-scan` and `trufflehog-verified-scan`, already required by `Infra.02` — listed here only for completeness of the full merge-gate picture, not re-registered by this file.)

## 14. Testing Strategy and Acceptance Criteria

| # | Check | How to verify | Expected result |
|---|---|---|---|
| 1 | A trivial one-line PR against `backend/` triggers exactly the six `Backend CI` jobs, in order, and nothing else | Open a scratch PR touching one comment in `backend/src/noorheroes/main.py` | `Backend CI`'s six jobs run and pass; `Admin Web CI`/`Mobile CI`/`OpenAPI Client Sync` do not trigger |
| 2 | A trivial one-line PR against `admin-web/` triggers exactly the six `Admin Web CI` jobs | Same pattern against `admin-web/src/app/layout.tsx` | `Admin Web CI` runs and passes; the other three do not trigger |
| 3 | A trivial one-line PR against `mobile/` triggers exactly the six `Mobile CI` jobs | Same pattern against a `commonMain` file | `Mobile CI` runs and passes; the other three do not trigger |
| 4 | A `backend/` PR that changes an endpoint's request schema triggers `OpenAPI Client Sync` in addition to `Backend CI` | Add a field to a Pydantic request schema | Both workflows trigger; `OpenAPI Client Sync` regenerates and diffs cleanly (non-breaking addition) |
| 5 | Lint failure blocks all downstream jobs | Introduce a deliberate `ruff` violation | `lint` fails; `static-analysis`/`unit-test`/`integration-test`/`architectural-invariant`/`build-artifact` all show as skipped, not failed, not run |
| 6 | Coverage gate blocks merge | Add an untested function dragging backend coverage under 80% | `unit-test` fails on the `--cov-fail-under=80` step specifically, distinguishable in the log from a genuine test failure |
| 7 | Integration tests actually exercise real Postgres/Redis | Add (temporarily, for this verification) an assertion in an integration test that queries `pg_catalog` for the live server version | Passes, proving a real Postgres instance (not a mock) backs the test |
| 8 | Stage 6 placeholder is real, not a stub | Deliberately violate the seed invariant on a scratch branch (e.g., add a second `JwtClaims` class for the backend case) | `architectural-invariant` job fails with a clear assertion message identifying the violation |
| 9 | Breaking OpenAPI change is caught | Remove a required field from a response schema on a scratch branch, without updating `openapi.baseline.json` | `OpenAPI Client Sync`'s `generate-and-diff` job fails on the `classify_openapi_diff.py` step |
| 10 | Build artifacts are produced and tagged correctly | Merge a trivial PR to `main` | `ghcr.io/.../noorheroes-backend:sha-<sha>` and `:latest` both exist; same for admin-web; a debug APK and (given signing secrets present) a release AAB are both uploaded as workflow artifacts |
| 11 | Docker/Gradle caching measurably speeds up a second run | Run the same workflow twice in a row with no dependency changes | Second run's dependency-install/build steps show a cache hit in the log and complete meaningfully faster than the first |
| 12 | Concurrency cancellation works | Push two commits to the same PR branch in quick succession | The first run's jobs show as cancelled, not failed, once the second run starts |
| 13 | Required-status-check gating actually blocks merge | With `Repo.03`'s branch protection configured using this file's §13 list, open a PR with a deliberate lint failure | GitHub's merge button is disabled, showing the specific failing required check |

**Definition of "acceptance":** all 13 checks pass, demonstrated on real scratch PRs against a real GitHub repository (not simulated), by someone who has not seen this file before, using only this document plus the already-implemented application code.

## 15. Production-Readiness Considerations

- **This file's build-artifact outputs are consumed, not deployed, by anything downstream of it.** `CI_CD.08`'s staging deploy pulls `:latest`/`sha-`-tagged images this file pushes; `CI_CD.09`'s production deploy pulls whatever `Repo.03`'s release workflows re-tag after this file's build succeeds. Nothing in this file talks to staging or production infrastructure directly — no deploy credentials, no Terraform state, no Kubernetes/Cloud Run API calls appear anywhere in `backend.yml`/`admin-web.yml`/`mobile.yml`/`openapi-sync.yml`.
- **Runner cost/time budget:** six sequential jobs per app (worst case, on the critical path) means a PR's full pipeline latency is the sum of `lint → static-analysis → max(unit-test, integration-test) → architectural-invariant → build-artifact`. If this becomes a developer-experience bottleneck once the team is large, the documented, low-risk optimization is loosening `static-analysis`'s `needs: lint` to run both in parallel from the start (both only ever depend on a clean checkout, never on each other's output) — flagged here as an explicit, pre-approved future change, not something to silently do now, since the "cheapest stage first, fail fast" ordering in Final_Development_Prompt §6 is itself a deliberate choice this file should not casually override without measuring the actual bottleneck first.
- **The `[PLACEHOLDER]` suffix in Stage 6's job display names is intentional and must survive to production use of this pipeline** — it is a truth-in-labeling signal to every reviewer that this specific required check does not yet enforce the full F.37 invariant set, preventing the false confidence flagged in §9. Do not remove the suffix as a "cosmetic cleanup" — its removal is `Phase9.CrossPlatform.01`'s job to do, once it has actually populated the suite it names.
- **GHCR image retention policy** is not configured by this file (GitHub's default indefinite retention for container images applies) — flag for a future Infra item once image storage costs matter; not a Phase 1 blocker.
- **This file assumes a single GitHub repository, single default branch (`main`), GitHub-hosted runners only** — no self-hosted runner pool, no GitLab-CI translation is provided (Final_Development_Prompt §6 explicitly allows either but this document commits to GitHub Actions per the monorepo's existing `.github/workflows/` folder, confirmed in the task's own framing).

## 16. Dependencies and Prerequisites

- Completion of `Infra.02` (secrets/`.env.example`/gitleaks) — specifically, the `check_env_example_sync`/`check-env-example-sync` scripts this file's `lint` jobs invoke (§4.1) must already exist; this file's `lint` jobs will fail at that step if they don't.
- Completion (or at least the artifact/paths existing) of `Infra.03` — not a hard blocker for this file's own jobs (§12 establishes full decoupling), but the "development steps" in §13 assume a working local dev loop exists for engineers verifying this file's changes end-to-end.
- `Repo.03`'s CODEOWNERS/PR-template/branch-protection mechanism must exist for this file's required-check names (§13) to actually gate anything — until `Repo.03` registers them, these checks run and report status but do not block a merge.
- Backend `pyproject.toml`, admin-web `package.json`, and mobile `build.gradle.kts`/`libs.versions.toml` must already define the underlying tool configurations (ruff rules, eslint config, detekt rules, etc.) this file's commands invoke — this file wires *invocation*, not *configuration*, of those tools; genuinely absent configuration (§13 steps 1–2) is the one class of "application-adjacent" file this blueprint may need to touch.
- A GitHub repository with Actions enabled, `GITHUB_TOKEN` with package-write permission available (default for public/private repos with Packages enabled), and (for Stage 7's mobile release path) the four `ANDROID_*` signing secrets already provisioned in repository settings.

## 17. Definition of Done

- [ ] `.github/workflows/backend.yml`, `admin-web.yml`, `mobile.yml`, `openapi-sync.yml` exist at the paths in §6, matching the YAML in §7 (adjusted only for confirmed tool-version pins per §3.4/§7.1's note).
- [ ] All six jobs per app-workflow (`lint`, `static-analysis`, `unit-test`, `integration-test`, `architectural-invariant`, `build-artifact`) exist, are correctly `needs:`-chained per the DAG in §4, and are named exactly as listed in §13's hand-off table.
- [ ] `backend/tests/architectural/test_jwt_schema_singularity.py`, `admin-web/tests/architectural/rbac-route-guard.spec.ts`, and `mobile/core/core-security/.../ArchitecturalInvariantTest.kt` exist, pass against the current codebase, and are not `assert True`/no-op stubs (§5, §9).
- [ ] `openapi.baseline.json` exists at repo root, seeded from the current backend schema; `openapi-sync.yml` correctly fails a deliberately-introduced breaking change (§14 check 9) and correctly passes a non-breaking one (§14 check 4).
- [ ] All 13 checks in §14 pass, verified via real scratch PRs.
- [ ] The `lint` jobs' `check-env-example-sync` steps (§4.1) are wired and passing against `Infra.02`'s actual script names/paths (confirmed, not assumed, at implementation time).
- [ ] `secret-scan.yml` (Infra.02) is unmodified by this work; this file adds zero new secret-scanning logic.
- [ ] `infra/docker-compose.yml` (Infra.03) is unmodified by this work and is not referenced by any `integration-test` job (§12).
- [ ] Backend/admin-web Docker builds succeed and push to GHCR with both `sha-<sha>` and `latest` tags on `main`; mobile produces a debug APK on every PR and a signed release AAB on `main` (given signing secrets present).
- [ ] The §13 required-status-check name list is handed off to (and, ideally, confirmed registered by) `Repo.03`'s branch-protection script; §14 check 13 passes against the real repository.
- [ ] No change was made to any application source file under `backend/src/`, `admin-web/src/` (outside the new `tests/architectural/` files and any genuinely-missing tool-config additions per §13 steps 1–2), or `mobile/**` (outside the new `ArchitecturalInvariantTest.kt` and any genuinely-missing Gradle plugin blocks).
- [ ] No change was made to `backend/Dockerfile`, `admin-web/Dockerfile`, `infra/k8s/`, `infra/terraform/`, `infra/docker-compose.staging.yml`, or any file owned by `CI_CD.07`/`CI_CD.08`/`CI_CD.09`.

## 18. Assumptions or Decisions the Coding Agent Must Follow

1. **Three separate top-level workflow files, not a single GitHub Actions reusable workflow (`workflow_call`), realize the "reusable structure" this file's brief asks for.** Final_Development_Prompt §6 itself describes the three apps' pipelines as *"conceptually identical"* — this file honors that by using one identical job-id sequence (`lint → static-analysis → unit-test → integration-test → architectural-invariant → build-artifact`) and one identical `needs:`-chain shape across all three files, rather than a literal parameterized `workflow_call` template. The three toolchains' actual commands (`ruff` vs `eslint` vs `ktlint`) differ enough that a single generic reusable workflow would need so many pass-through inputs it would obscure more than it shares. If a future maintainer wants to genuinely DRY this into a `workflow_call` template, that is a valid refactor of this file's *implementation*, not a change to its *architecture* (the six-stage, `needs:`-chained shape must be preserved).
2. **Ruff is the backend's sole formatter (no Black).** Final_Development_Prompt §1.2/§4 leaves this open ("decide once at setup, don't run both formatters"). This file commits to Ruff-only (`ruff format --check`) for both lint and format in Stage 1 — if `backend/pyproject.toml` already configures Black at implementation time, that is a real conflict to resolve explicitly (write a one-line ADR per Final_Development_Prompt §2.3), not to silently dual-wield.
3. **Bandit runs in Stage 2 (static analysis), not deferred to Stage 8.** Final_Development_Prompt §9's Security Baseline item 7 calls SAST tooling (Bandit/Semgrep) prerequisite CI infrastructure; this file interprets "static analysis / type check" (Stage 2's own name) as the natural home for a SAST tool, distinct from Stage 8's dependency/container vulnerability scanning (`pip-audit`/`pnpm audit`/Trivy/Grype), which stays with `CI_CD.07` as the task's own scope boundary states. Admin-web's equivalent (Semgrep) is *not* added in this baseline implementation, since Final_Development_Prompt §1.3's admin-web tool table does not name it explicitly the way §1.2 names Bandit for the backend — flagged as an open, low-risk addition for whoever implements `CI_CD.07`, not manufactured here without a clear source-doc anchor.
4. **Mobile integration tests run via Robolectric on the JVM, never a real/virtual device, at this phase.** See §3.3's full justification. Do not add `reactivecircus/android-emulator-runner` or any KVM-dependent step to `mobile.yml` without first confirming the GitHub-hosted runner tier in use actually supports hardware-accelerated emulation (many do not, and emulator boot time would dominate this job's runtime) — that is a scoped, deliberate future addition, not an oversight in this baseline.
5. **`astral-sh/setup-uv@v5`, `pnpm/action-setup@v4`, `gradle/actions/setup-gradle@v4`, `docker/build-push-action@v6`, and all other pinned Action versions in §7 are known-good baselines as of this document's authoring — re-verify each against its marketplace listing's current major version at implementation time**, per Final_Development_Prompt §1's own "re-verify nothing here has been superseded" instruction, exactly as `Infra.03`'s §7.1 pin-freshness note already established the norm for this project's other infrastructure files.
6. **The Stage 6 placeholder's exact seed-test content (§5) is this file's judgment call, chosen to be genuinely useful and directly traceable to a named row in Final_Development_Prompt §5's architectural test table.** An implementer may substitute a different, equally-real seed test per app if a better one becomes apparent at implementation time (e.g., the JWT class is actually named something other than `JwtClaims` once `core/security.py` is inspected directly) — but must not substitute a no-op, and must keep the job's display name (`... [PLACEHOLDER]`) and required-status-check identity stable regardless of which specific seed assertion backs it, so `Phase9.CrossPlatform.01`'s later hand-off is unaffected.
7. **GHCR (`ghcr.io`), not Docker Hub or a cloud-vendor registry, is this file's chosen image registry**, using the repository's own built-in `GITHUB_TOKEN` rather than a separate registry credential — the simplest option requiring zero additional secret provisioning, appropriate for Phase 1's CI-pipeline-only scope. `CI_CD.08`/`CI_CD.09` may re-point staging/production deploys at a different registry if the eventual cloud platform (Cloud Run/ECS Fargate, per Final_Development_Prompt §7) requires it — that is those files' decision to make, not a constraint this file imposes on them.

---

## AI Agent Development Prompt

Implement the Phase 1 CI pipeline (Stages 1–7 of the 13-stage pipeline defined in `NoorHeroes_Final_Development_Prompt.md` §6) for the NoorHeroes monorepo exactly as specified in this document. The backend, admin-web, and mobile application code already exists and works — you are building CI plumbing around it, not writing feature code.

**What to build, and exactly where:**
1. `.github/workflows/backend.yml` — use the YAML in §7.1 as your starting point; verify every pinned tool/action version against its current release before finalizing (§18 item 5).
2. `.github/workflows/admin-web.yml` — §7.2, same verification discipline.
3. `.github/workflows/mobile.yml` — §7.3, same verification discipline.
4. `.github/workflows/openapi-sync.yml` — §7.4; seed `openapi.baseline.json` at repo root as step 7 of §13 describes.
5. `backend/tests/architectural/test_jwt_schema_singularity.py`, `admin-web/tests/architectural/rbac-route-guard.spec.ts`, `mobile/core/core-security/src/commonTest/kotlin/ArchitecturalInvariantTest.kt` — the Stage 6 seed tests, per §5's design table. Each must genuinely pass against the current codebase and genuinely fail if the invariant it checks is violated (§14 check 8) — verify both directions before considering it done.

**Conventions to follow:**
- Package managers are fixed: `uv` (backend, matching `Infra.03`'s decision), `pnpm` (admin-web), Gradle Version Catalog (mobile) — do not substitute Poetry/npm/yarn/Maven.
- Job order within each app-workflow is a strict `needs:`-chain: lint → static-analysis → unit-test/integration-test (parallel siblings, both depending on static-analysis) → architectural-invariant → build-artifact. Do not reorder or parallelize `lint`/`static-analysis` without the explicit, documented justification in §15.
- Stage 3 (secret scanning) is **not** a job you add to these workflows — it is `secret-scan.yml`, already built by `Infra.02`. Your only touchpoint is the one `check-env-example-sync` step per §4.1, added to each `lint` job.
- Stage 6 job display names carry a literal `[PLACEHOLDER]` suffix — keep it; it is a deliberate truth-in-labeling signal, not a typo to clean up (§15).
- Coverage gates are real and enforced in this baseline: backend `--cov-fail-under=80`, admin-web `--coverage.thresholds.lines=70`/`functions=70` — do not lower these to make a job pass; add tests instead.

**What NOT to change:**
- Any application source file under `backend/src/`, `admin-web/src/`, or `mobile/**`, other than the three new architectural-invariant test files above and any genuinely-missing tool-config blocks confirmed absent per §13 steps 1–2.
- `backend/Dockerfile`, `admin-web/Dockerfile` (production images — built, not authored, by Stage 7).
- `infra/docker-compose.yml` (Infra.03) — never referenced by `integration-test` jobs (§12); the backend's Testcontainers harness in `backend/tests/conftest.py` is the only integration-test infrastructure this file touches, and it is invoked unmodified.
- `.github/workflows/secret-scan.yml`, `.gitleaks.toml`, or any other `Infra.02` artifact.
- Anything under `infra/k8s/`, `infra/terraform/`, `infra/docker-compose.staging.yml` — all out of scope (owned by later Infra/CI_CD items).

**How to verify you're done (walk through all of these before considering the task complete):**
1. Open four separate scratch PRs — one touching only `backend/`, one only `admin-web/`, one only `mobile/`, one touching a backend request schema — and confirm the trigger/skip pattern in §14 checks 1–4 holds exactly.
2. On separate scratch branches, deliberately break: a lint rule, the coverage gate, the Stage 6 seed invariant (for each app), and the OpenAPI contract without updating the baseline. Confirm each failure is caught by exactly the job/workflow named in §14 checks 5, 6, 8, 9 — not by some other, unrelated job.
3. Merge a trivial PR to `main` and confirm the build-artifact outputs described in §14 check 10 actually appear (GHCR images with both tags; debug APK and signed release AAB as workflow artifacts).
4. Confirm caching (§14 check 11) and concurrency-cancellation (§14 check 12) behavior with two back-to-back runs.
5. Hand the §13 required-status-check name table to whoever runs `Repo.03`'s `configure-branch-protection.sh`, then confirm §14 check 13: a PR with a deliberate failure cannot be merged, including by a repo admin.
6. Walk every checkbox in §17's Definition of Done in order and confirm each is literally true against the repository state you produced.
