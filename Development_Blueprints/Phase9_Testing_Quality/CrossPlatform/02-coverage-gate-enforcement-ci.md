# Phase 9 — Coverage Gate Enforcement in CI

`Development_Blueprints.Phase9_Testing_Quality.CrossPlatform.02-coverage-gate-enforcement-ci.md`

**Module:** CrossPlatform (`backend/`, `admin-web/`, `mobile/`, `.github/workflows/`)
**Phase:** Phase 9 — Testing & Quality Hardening
**Depends on:** Phase 1 `CI_CD.06` (`ci-pipeline-lint-test-build-stages.md` — specifically each app's `unit-test` job, Stage 4 of the 13-stage pipeline, which is the exact job this file modifies); every feature phase (A/B/C/D/E/F blueprints) — a coverage gate against a codebase with no real `service.py`/`src/features/**`/ViewModel content to measure is vacuous, so this file assumes the application code those phases build already exists
**Consumed by:** none currently named in the corpus. A future coverage-trend/badge-dashboard item (not yet specced) would consume this file's artifact outputs (§11) without needing to change anything this file builds.
**Source of truth:** `NoorHeroes_Final_Development_Prompt.md` §5 ("Testing Strategy (cross-platform)" table, specifically the **Coverage gates** row: *"≥80% on `domain/` service-layer code (CI-enforced via `pytest-cov` threshold) | ≥70% on `src/features/` | ≥70% on each `core-*`/`feature/*` module's ViewModel/service layer"*) and §6 (13-stage CI/CD pipeline, Stage 4 = Unit tests); `FAST-API-INSTRUCTIONS.md` §1 (module layering: `api.py` → `service.py` → `repository.py` → infra) and §5 (the 12 bounded contexts); `NEXT-JS-INSTRUCTIONS.md` §2 (Feature Container → Feature Hook → Repository/`BaseResourceClient` layering inside `src/features/*`); `CORE_UI_INSTRUCTIONS.md` §3–§4 (`BaseViewModel`, the `com.noorheroes.core.ui.viewmodel` package convention extended project-wide in this file's mobile scope)
**Status:** NEW — this file does not exist in the corpus today; Phase 9 (testing/quality hardening) is a confirmed, total gap

**Do not re-litigate:** the backend (FastAPI, 12 bounded contexts, Testcontainers-based `conftest.py`), the Admin Portal (Next.js App Router, generated OpenAPI TypeScript client, feature-sliced `src/features/`), and the KMP/CMP mobile app (all `core-*`/`feature/*` modules, `BaseViewModel` via `core-ui`) are **fully implemented**. Phase 1's `CI_CD.06` already stood up the six-job-per-app pipeline (`lint → static-analysis → unit-test → integration-test → architectural-invariant → build-artifact`) and, inside each app's `unit-test` job, a **first-pass, intentionally-flagged-as-incomplete** coverage step: backend's `--cov-fail-under=80` measured the *entire* `src/noorheroes` package (an aggregate that, per that file's own §9, "could hide a fully-untested `rewards/service.py` behind well-tested `identity/service.py`"), admin-web's `--coverage.thresholds.lines=70`/`functions=70` measured the *entire* codebase (not `src/features/` specifically), and mobile had **no coverage gate at all**. This document does not rebuild the pipeline `CI_CD.06` already built — it makes three narrow, surgical edits to that file's three `unit-test` jobs (and one new coverage config file per stack) so each gate measures exactly the layer Final_Development_Prompt §5 names, at exactly the threshold it names, and fails CI when unmet.

---

## 1. Objective and Purpose

Close the gap between Final_Development_Prompt §5's coverage-gates row and what `CI_CD.06` actually shipped. Concretely, after this file's implementation:

- **Backend:** a PR that adds an untested branch to any bounded context's `service.py` (business logic — `identity`, `admin`, `ai_safety`, `content`, `learning`, `localization`, `media`, `notifications`, `rewards`, `subscriptions`, `habits`, `avatars`) and drags the *domain/service layer's own* coverage below 80% fails `Backend CI`'s `Unit Tests (pytest)` job, at a step distinct from and diagnosable separately from a genuine test failure. A PR that only touches `api.py`/`repository.py`/`models.py`/`schemas.py`/migrations does **not** move that percentage and is never falsely blocked.
- **Admin-web:** a PR that adds an untested branch inside `src/features/**` and drags that slice's coverage below 70% fails `Admin Web CI`'s `Unit Tests (vitest)` job. A PR touching only `src/lib/api-client/**` (generated), `src/components/**` (shared design system), or `src/app/**` (route shells) does not move that percentage.
- **Mobile:** a PR that adds an untested branch inside any `core-*`/`feature/*` module's `BaseViewModel` subclass and drags the aggregate ViewModel-layer coverage below 70% fails `Mobile CI`'s `Unit Tests (JVM)` job at a new, dedicated Kover verification step. A PR touching only a `@Composable` function does not move that percentage — consistent with the existing "business logic (including analytics) lives in the ViewModel, never duplicated in the Composable" convention this project already follows for `core-analytics`.

Each gate is a **required, non-bypassable CI check** (per Final_Development_Prompt §5's "CI-enforced" language) — not a warning, not an informational report. This file's job is precise scoping (§2), the actual config block syntax (§5/§7), the exact CI step edits (§7), and the edge cases that make a poorly-scoped coverage gate worse than no gate at all (§10).

**What this file is not:** it does not build the test-running mechanism (pytest, Vitest, JUnit5/MockK all already run real tests today per `CI_CD.06`), it does not write new application tests to raise coverage to the target (that is every feature phase's own ongoing responsibility, enforced going forward by this gate), and it does not stand up a coverage-trend dashboard or hosted badge service (§11).

## 2. Scope and Requirements

**In scope — the precise file-level definition of "counts toward the gate" per stack, which is this file's single most load-bearing decision:**

### 2.1 Backend — ≥80%, domain/service layer

| | Pattern | Rationale |
|---|---|---|
| **Included** | `backend/src/noorheroes/modules/*/service.py` (all 12 bounded contexts) | This is the literal "domain/service layer" per `FAST-API-INSTRUCTIONS.md` §1's layering diagram: *"DOMAIN SERVICE LAYER — BaseService Subclasses, Business Rules, Entitlements, Outbox Events."* This is where business rules, authorization re-checks, reward-ledger math, and domain-event emission live — the highest-blast-radius code named repeatedly across Final_Development_Prompt §2.3/§9. |
| **Included** | `backend/src/noorheroes/common/base_service.py` | Every `service.py` subclasses `BaseService`; its shared logic (transaction boundary helpers, outbox emission plumbing) is exercised transitively by every module's service tests and folded into the same aggregate — not gated as an independently-reported percentage. |
| **Excluded** | `backend/src/noorheroes/modules/*/api.py` | Thin FastAPI routers — no business logic per the architecture doc; covered by Stage 5's `httpx.AsyncClient` API/contract tests, not this unit-coverage gate. |
| **Excluded** | `backend/src/noorheroes/modules/*/repository.py` | Data-access layer only; covered by Stage 5's Testcontainers integration tests, which exercise real Postgres — a unit-coverage percentage on a DB-access file that is by design untestable without a DB would be a meaningless number. |
| **Excluded** | `backend/src/noorheroes/modules/*/models.py`, `schemas.py`, `events.py` | Declarative SQLAlchemy ORM models, Pydantic schemas, and event dataclasses — no branching logic to cover; counting these would dilute the denominator with lines nobody can meaningfully "under-test." |
| **Excluded** | `backend/alembic/versions/**` | Generated/scaffolded migrations, per this file's brief — never hand-authored business logic. |
| **Excluded** | `backend/src/noorheroes/infrastructure/**`, `backend/src/noorheroes/core/**`, `backend/src/noorheroes/workers/**`, `backend/src/noorheroes/scripts/**` | Infra clients, security/settings/gateway plumbing, Celery task glue, and admin scripts — covered by their own architectural/integration tests (per Final_Development_Prompt §5's Architectural row and `CI_CD.06`'s Stage 6 seed tests), intentionally not folded into this specific gate so a change to, say, `core/security.py` cannot silently move the domain-service percentage. |
| **Excluded** | `backend/tests/**`, any `__init__.py` | Test code and empty package markers. |

### 2.2 Admin-web — ≥70%, `src/features/`

| | Pattern | Rationale |
|---|---|---|
| **Included** | `admin-web/src/features/**/*.{ts,tsx}` | Per `NEXT-JS-INSTRUCTIONS.md` §2's layering: Feature Container/Page Component, Feature Custom Hook (`src/features/*/hooks/*`), and the Repository/`BaseResourceClient` layer living at `src/features/<feature>/api/*` are all *hand-authored* feature logic — the "service/repository layer for a stateless frontend" per Final_Development_Prompt §2's dependency-inversion row. This is the layer Final_Development_Prompt §5 names verbatim (`src/features/`). |
| **Excluded** | `admin-web/src/lib/api-client/**` | The **generated** OpenAPI TypeScript client, regenerated by `CI_CD.06`'s `openapi-sync.yml` workflow whenever `backend/` changes. Gating generated code that a human never hand-edits would produce false negatives on every schema change unrelated to actual feature-logic quality — excluded structurally, not special-cased at report time. |
| **Excluded** | `admin-web/src/components/**` | Shared design-system components (shadcn/ui-based per Final_Development_Prompt §1) — cross-feature, not feature-specific business logic; visual composition, not the layer §5 names. |
| **Excluded** | `admin-web/src/app/**` | Route/page shells and layouts — thin composition wiring `DashboardShell`/`RequirePermission` around feature containers; covered by Playwright E2E (Stage 4 E2E row) and the RBAC-boundary architectural test, not this unit gate. |
| **Excluded** | `admin-web/src/lib/auth/**` | RBAC guard middleware — covered by `CI_CD.06`'s Stage 6 `rbac-route-guard.spec.ts` architectural test specifically, so it is not double-counted here. |
| **Excluded** | `*.test.ts(x)`, `*.spec.ts(x)`, `*.stories.tsx`, `*.d.ts`, `**/__mocks__/**` | Test/story/type-declaration/mock files. |

### 2.3 Mobile — ≥70%, ViewModel/service layer per `core-*`/`feature/*` module

| | Pattern | Rationale |
|---|---|---|
| **Included** | Every class extending `BaseViewModel<State, Event>` (`core-ui`'s architectural base, per `CORE_UI_INSTRUCTIONS.md` §4) across every `core-*` and `feature/*` module's `commonMain`, i.e. any Kotlin source file in a package matching `com.noorheroes.<module>.viewmodel.**` — extending project-wide the exact package convention `core-ui` itself already documents (`com.noorheroes.core.ui.viewmodel`, §3). | This is the literal "ViewModel/service layer" Final_Development_Prompt §5 names for mobile — the layer holding reducer logic (`updateState`), suspended business operations (`launchSafely`), and the analytics/event-emission calls the project's own convention keeps out of Composables. |
| **Excluded** | Any `@Composable`-annotated function or file, and any file/package matching `*.ui.*`, `*.screen.*`, `*.component.*`, or a filename ending `Screen.kt`/`Content.kt` | Per the existing "never duplicate analytics in Composables" convention: Composables are declarative view code, and business/analytics logic is deliberately pushed into the ViewModel instead. Measuring Composable coverage would be measuring UI-rendering paths, not business logic — the wrong signal for this gate, and one that would create pressure to add fake logic-shaped code to Composables just to "earn" coverage, which is the opposite of the convention this project has already committed to. |
| **Excluded** | `**/di/**` (Koin module wiring), `expect`/`actual` platform-bridge stubs with no branching logic, SQLDelight-generated interfaces, KSP-generated code, `ComposableSingletons$*`/lambda-synthetic classes the Compose compiler emits | Declarative wiring and generated code — same "no meaningful percentage to earn" reasoning as backend's `models.py`/`schemas.py` exclusion. |
| **Excluded** | `commonTest`/`androidUnitTest`/`iosTest` source itself | Test code. |
| **Deliberately deferred, not included in v1** | A broader `com.noorheroes.*.service.*` package convention for non-ViewModel business/use-case classes | See §18 item 2 — kept out of the v1 gate to keep the Kover rule mechanically unambiguous; broadening is a documented follow-up once such a package convention is confirmed to actually exist consistently across modules, not silently assumed here. |

**Explicitly not rebuilt here (already owned elsewhere):**
- The `unit-test`/`integration-test`/`architectural-invariant`/`build-artifact` job *bodies* other than the specific coverage-related steps this file adds/replaces — `CI_CD.06` owns everything else in those jobs, and this file's diffs (§7) touch nothing beyond the named steps.
- Any new required-status-check name — this file's edits happen **inside** `CI_CD.06`'s existing `Backend CI / Unit Tests (pytest)`, `Admin Web CI / Unit Tests (vitest)`, and `Mobile CI / Unit Tests (JVM)` jobs, so `Repo.03`'s branch-protection required-check list needs zero changes.
- Application source code itself — this file adds coverage *configuration* (`pyproject.toml`, `vitest.config.ts`, `build.gradle.kts`/Kover) and CI *step* edits, never a change to `service.py`/`src/features/**`/ViewModel logic.
- `openapi-sync.yml`, the `integration-test` jobs, `secret-scan.yml`, or anything Stage 8+ owns — untouched.

## 3. Technical Implementation Details

### 3.1 Tool choices (already fixed by Final_Development_Prompt §5/§1, not re-decided here)

| Stack | Tool | Metric collected |
|---|---|---|
| Backend | `pytest-cov` (wrapping `coverage.py`) — already the pinned tool per Final_Development_Prompt §1.2's testing-stack table | Line coverage (§18 item 1) |
| Admin-web | Vitest's built-in coverage (`@vitest/coverage-istanbul` provider) | Lines, functions, statements, branches (§18 item 1) |
| Mobile | Kover Gradle Plugin (`org.jetbrains.kotlinx.kover`) | Line coverage of JVM/Android bytecode (§18 item 1; iOS-native coverage is a known limitation, §2.3) |

### 3.2 The one-run, two-report pattern (backend)

Coverage is collected **once** per `pytest` invocation (instrumenting the whole `src/noorheroes` tree costs nothing extra to widen vs. narrow), then **reported twice** from the same `.coverage` data file: once unscoped (for visibility/artifact purposes, never gates), once scoped via `coverage report --include=...` (the actual gate). This avoids running the test suite twice just to get two different denominators — `coverage.py`'s `report`/`xml` subcommands can be invoked repeatedly against one data file with different `--include` filters without re-executing any test.

### 3.3 Vitest's native `coverage.include`/`coverage.thresholds` replaces the CLI-flag approach

`CI_CD.06` originally passed thresholds as CLI flags (`--coverage.thresholds.lines=70`). This file moves scoping and thresholds into `vitest.config.ts`'s `test.coverage` block instead (§5.2), because Vitest's CLI flags cannot express an `include` glob restricted to `src/features/**` as cleanly as the config object can, and because config-file-driven thresholds are visible to a developer running `pnpm vitest run --coverage` locally without needing to remember CI-only flags — the local and CI experience stay identical, mirroring the same "CI and laptop are the same claim" principle `CI_CD.06` §12 already established for the backend's Testcontainers harness.

### 3.4 Mobile gets a genuinely new mechanism, not a refinement

Unlike backend/admin-web, `CI_CD.06` shipped **zero** coverage tooling for mobile. This file introduces the Kover Gradle Plugin from scratch: adds the coordinate to `mobile/gradle/libs.versions.toml`, applies it at the root `build.gradle.kts` plus every `core-*`/`feature/*` module, configures a merged multi-module report (Kover's `kover(project(":..."))` dependency mechanism — a Kover report task can only aggregate modules explicitly declared as report dependencies), and adds a `koverVerify` rule scoped per §2.3.

## 4. Architecture and Component Responsibilities

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ CI_CD.06's existing `unit-test` job, per app — UNTOUCHED job name/needs/    │
│ required-status-check string; only the internal step list changes          │
└───────────────┬───────────────────────┬───────────────────────┬────────────┘
                 ▼                       ▼                       ▼
        Backend CI /             Admin Web CI /            Mobile CI /
        Unit Tests (pytest)      Unit Tests (vitest)        Unit Tests (JVM)
                 │                       │                       │
   1. pytest tests/unit         1. vitest run --coverage   1. ./gradlew testDebugUnitTest
      --cov=src/noorheroes         (thresholds + include       (unchanged from CI_CD.06)
      --cov-report= (data only)    live in vitest.config.ts,
   2. coverage xml -o             §5.2 — no CLI flags)      2. ./gradlew koverXmlReport
      coverage.xml (artifact,                                  (merged multi-module report)
      NOT gated)                                            3. ./gradlew koverVerify
   3. coverage report                                           (THE GATE — fails build)
      --include="modules/*/
      service.py,common/
      base_service.py"
      --fail-under=80
      (THE GATE — fails build)

  Component responsibilities:
  ├─ backend/pyproject.toml [tool.coverage.*]   → defines source/omit/exclude_lines (§5.1)
  ├─ admin-web/vitest.config.ts test.coverage    → defines include/exclude/thresholds (§5.2)
  ├─ mobile/build.gradle.kts (root) kover{}       → defines merged-report membership + filters + verify rule (§5.3)
  └─ Each app's unit-test job step list           → invokes the above; the LAST coverage-related
                                                      step in each job is the one whose failure
                                                      IS the gate — distinguishable by name from
                                                      every step before it (§10)
```

| Component | Responsibility |
|---|---|
| `backend/pyproject.toml`'s `[tool.coverage.run]`/`[tool.coverage.report]` | Declares which files are ever instrumented (`source`) and which subset the gate's `--include` filter narrows to at report time. Does **not** itself set `fail_under` for the gate (that is a CLI override on the specific gate step, §7.1) — this keeps the informational full-repo report from accidentally inheriting a threshold that only makes sense for the narrow domain/service slice. |
| `admin-web/vitest.config.ts`'s `test.coverage` | Owns both scoping (`include`/`exclude`) and the threshold (`thresholds`) in one place — Vitest's coverage step fails the `vitest run` process itself when a threshold is unmet, so there is no separate "gate step" the way backend/mobile need one; the single `vitest run --coverage` invocation *is* the gate. |
| `mobile/build.gradle.kts`'s `kover { }` extension (root project) | Declares merged-report membership (every `core-*`/`feature/*` subproject), the include/exclude filters (§2.3), and the `verify { rule { ... } }` bound that `koverVerify` enforces. |
| `koverVerify` Gradle task | The actual gate — a distinct, separately-invoked Gradle task from `testDebugUnitTest`, so its failure is attributable in the job log to "coverage below threshold," not conflated with a test assertion failure. |

## 5. Folder/File Structure

```text
noorheroes/
├── backend/
│   ├── pyproject.toml                 # MODIFIED — add [tool.coverage.run]/[tool.coverage.report] (§7.1)
│   └── src/noorheroes/
│       ├── modules/*/service.py       # EXISTING — the measured domain/service layer, untouched by this file
│       └── common/base_service.py     # EXISTING — measured, untouched
├── admin-web/
│   ├── vitest.config.ts               # MODIFIED — add/extend test.coverage block (§7.2)
│   └── src/features/**                # EXISTING — the measured slice, untouched by this file
├── mobile/
│   ├── gradle/libs.versions.toml      # MODIFIED — add the Kover Gradle Plugin coordinate (§7.3)
│   ├── build.gradle.kts               # MODIFIED — apply Kover at root + merged-report/filter/verify config (§7.3)
│   ├── core/*/build.gradle.kts        # MODIFIED — apply the Kover plugin (one-line `alias(libs.plugins.kover)`) per module
│   └── feature/*/build.gradle.kts     # MODIFIED — same one-line plugin application per module
└── .github/workflows/
    ├── backend.yml                    # MODIFIED — unit-test job's step list only (§7.1)
    ├── admin-web.yml                  # MODIFIED — unit-test job's step list only (§7.2)
    └── mobile.yml                     # MODIFIED — unit-test job's step list only (§7.3)
```

No new top-level file is created by this blueprint — every change is either a modification to an existing `CI_CD.06`-authored workflow, or a new configuration *block* inside an existing, already-present config file (`pyproject.toml`, `vitest.config.ts`, `build.gradle.kts`).

## 6. APIs, Models, Interfaces, and Data Flow

This file introduces no runtime API, database model, or client-facing interface — it is CI-internal tooling. Its "data flow" is the coverage-artifact pipeline, identical in shape across all three stacks:

```text
Test execution (instruments source) → coverage data file → two reports:
                                        ├─ full-repo report  → uploaded as a 14-day
                                        │  (informational,      workflow artifact
                                        │   never gates)         (§11 — the durable
                                        │                         record a future
                                        └─ scoped report        trend/badge feature
                                           (--include=...,       could read without
                                            --fail-under=N)       any change here)
                                           → THE GATE
```

| Stack | Raw data file | Full-repo report (artifact) | Scoped report (the gate) |
|---|---|---|---|
| Backend | `.coverage` (SQLite, `coverage.py`) | `coverage.xml` (Cobertura-style XML) | `coverage report --include=...` (text, stdout + exit code) |
| Admin-web | Istanbul's internal coverage map | `coverage/lcov-report/`, `coverage/coverage-final.json` | Vitest's own threshold check (stdout + non-zero exit) |
| Mobile | Kover's binary `.ic` files per module | `build/reports/kover/report.xml` (merged) | `koverVerify`'s rule evaluation (stdout + non-zero exit) |

No schema is defined by this file for these formats — `coverage.xml`, Istanbul's `lcov`, and Kover's XML are each that tool's own standard, unmodified output shape.

## 7. Dependencies, Configuration, and the Exact CI Step Edits

### 7.1 Backend — `pyproject.toml` addition and `backend.yml` step-list replacement

**`backend/pyproject.toml`** (new section; add alongside the existing `[tool.ruff]`/`[tool.mypy]`/`[tool.pytest.ini_options]` sections `CI_CD.06` §13 step 1 already confirmed present):

```toml
[tool.coverage.run]
branch = false
source = ["src/noorheroes/modules", "src/noorheroes/common"]
data_file = ".coverage"
relative_files = true
omit = [
    "*/tests/*",
    "*/__init__.py",
]

[tool.coverage.report]
show_missing = true
precision = 1
skip_empty = true
exclude_lines = [
    "pragma: no cover",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
    "def __repr__",
    "\\.\\.\\.$",
]
# Deliberately no `fail_under` here — the informational full-repo report (Stage 4's
# `coverage.xml` artifact) must never silently gate the build; the domain/service-layer
# gate's --fail-under=80 is passed explicitly as a CLI override on the one step that IS
# the gate (see backend.yml's replaced unit-test job below), so a future contributor
# reading this file in isolation is not misled into thinking 80% applies repo-wide.
```

**`backend.yml`'s `unit-test` job** — replace `CI_CD.06` §7.1's single coverage step with:

```yaml
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
      - name: pytest (unit, parallelized) — collect coverage data
        run: uv run pytest tests/unit -n auto --cov=src/noorheroes --cov-report=
      - name: Full-repo coverage report (informational artifact, not gated)
        run: uv run coverage xml -o coverage.xml
      - name: Coverage gate — domain/service layer ≥80%
        run: |
          uv run coverage report \
            --include="src/noorheroes/modules/*/service.py,src/noorheroes/common/base_service.py" \
            --fail-under=80 --show-missing --precision=1
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: backend-unit-coverage
          path: backend/coverage.xml
          retention-days: 14
```

The job's `name:` (`Unit Tests (pytest)`), `needs:`, and therefore its required-status-check string (`Backend CI / Unit Tests (pytest)`) are **unchanged** from `CI_CD.06` — only the step bodies inside it change. `--cov-report=` (empty value) on the first step suppresses pytest-cov's default inline report so the two `coverage`-CLI steps that follow have exclusive, deliberate control over what gets reported and gated.

### 7.2 Admin-web — `vitest.config.ts` coverage block and `admin-web.yml` step simplification

**`admin-web/vitest.config.ts`** (extend the existing config `CI_CD.06`'s `pnpm vitest run --coverage` step already assumes is present):

```ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    // ...existing test config (environment, setupFiles, etc.) unchanged...
    coverage: {
      provider: "istanbul",
      reporter: ["text", "html", "json-summary", "lcov"],
      include: ["src/features/**/*.{ts,tsx}"],
      exclude: [
        "src/features/**/*.test.{ts,tsx}",
        "src/features/**/*.spec.{ts,tsx}",
        "src/features/**/*.stories.tsx",
        "src/features/**/*.d.ts",
        "src/features/**/__mocks__/**",
      ],
      thresholds: {
        lines: 70,
        functions: 70,
        statements: 70,
        branches: 70,
        // Global (repo-wide-within-`include`) thresholds, not per-file — see §18 item 3.
      },
    },
  },
});
```

**`admin-web.yml`'s `unit-test` job** — replace `CI_CD.06` §7.2's coverage step with the plain, un-flagged invocation (scoping/thresholds now live entirely in config, per §3.3):

```yaml
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
      - name: vitest (unit, coverage-gated on src/features/**)
        run: pnpm vitest run --coverage
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: admin-web-unit-coverage
          path: admin-web/coverage
          retention-days: 14
```

Vitest exits non-zero when any configured threshold is unmet, so this single step *is* both the test run and the gate — no separate "report" step is needed the way backend's `coverage.py` CLI requires.

### 7.3 Mobile — Kover from scratch: version catalog, root config, per-module application, `mobile.yml` new steps

**`mobile/gradle/libs.versions.toml`** (additions):

```toml
[versions]
kover = "0.8.3"  # re-verify current stable at implementation time, per this project's
                  # established pin-freshness convention (CI_CD.06 §18 item 5)

[plugins]
kover = { id = "org.jetbrains.kotlinx.kover", version.ref = "kover" }
```

**`mobile/build.gradle.kts`** (root project — apply the plugin and configure the merged report):

```kotlin
plugins {
    // ...existing root plugins...
    alias(libs.plugins.kover)
}

dependencies {
    // Every core-* and feature/* module participates in the merged report.
    // New modules must be added here explicitly — Kover does not auto-discover
    // subprojects; see §18 item 4 for the maintenance implication.
    listOf(
        ":core:core-common", ":core:core-ui", ":core:core-designsystem",
        ":core:core-navigation", ":core:core-network", ":core:core-database",
        ":core:core-datastore", ":core:core-logger", ":core:core-crash",
        ":core:core-analytics", ":core:core-security", ":core:core-notifications",
        // feature/* modules — extend this list as each is extracted per
        // Final_Development_Prompt §2.1's "start as packages, extract incrementally" note
        ":feature:feature-onboarding", ":feature:feature-home", ":feature:feature-stories",
        ":feature:feature-learn", ":feature:feature-habits", ":feature:feature-rewards",
        ":feature:feature-parent-dashboard", ":feature:feature-subscription",
    ).forEach { modulePath -> kover(project(modulePath)) }
}

kover {
    reports {
        filters {
            includes {
                packages("com.noorheroes.*.viewmodel")
            }
            excludes {
                packages(
                    "com.noorheroes.*.ui",
                    "com.noorheroes.*.screen",
                    "com.noorheroes.*.component",
                    "com.noorheroes.*.di",
                )
                classes(
                    "*ComposableSingletons*",
                    "*\$\$serializer",
                    "*_Factory",
                )
                annotatedBy("androidx.compose.runtime.Composable")
            }
        }
        verify {
            rule("ViewModel layer coverage ≥ 70%") {
                bound { minValue = 70 }
            }
        }
    }
}
```

**Every `core-*`/`feature/*` module's `build.gradle.kts`** (one-line addition per module):

```kotlin
plugins {
    // ...existing module plugins (kotlin-multiplatform, compose, etc.)...
    alias(libs.plugins.kover)
}
```

**`mobile.yml`'s `unit-test` job** — add three steps after `CI_CD.06` §7.3's existing `testDebugUnitTest` step:

```yaml
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
      - name: Generate merged Kover XML report (ViewModel layer)
        run: ./gradlew koverXmlReport --no-daemon
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: mobile-kover-report
          path: "mobile/build/reports/kover/report.xml"
          retention-days: 14
      - name: Coverage gate — ViewModel layer ≥70%
        run: ./gradlew koverVerify --no-daemon
```

`koverVerify` is deliberately the **last** step — it depends on the same instrumented test execution `testDebugUnitTest` already produced, so no tests re-run; its failure is attributable in the job log specifically to the "Coverage gate" step name, not conflated with `testDebugUnitTest`'s own pass/fail.

## 8. Database/Storage Requirements

None. All three gates operate entirely on CI-runner-local files (`.coverage`, Istanbul's in-memory coverage map, Kover's `.ic` binary files) that exist only for the lifetime of a single job run. The only persisted output is the artifact upload (§7.1–§7.3), retained 14 days on GitHub's artifact storage — matching `CI_CD.06`'s existing artifact-retention convention exactly, not a new policy.

## 9. Authentication, Authorization, Validation, and Security Considerations

- **No secrets, credentials, or PII flow through any coverage tool** — `.coverage`/Istanbul/Kover data is purely structural (which lines executed), never captures request payloads, test fixture content, or environment values.
- **Non-bypassability:** these gates run as steps *inside* the existing, already-required `Unit Tests (...)` job for each app (§2's "no new required-status-check name" note) — since that job is already on `Repo.03`'s required-checks list (per `CI_CD.06` §13's hand-off table), a coverage-gate failure blocks merge through the exact same branch-protection mechanism as any other test failure, with zero additional configuration needed on `Repo.03`'s side.
- **No silent threshold bypass mechanism exists in any of the three configs above** — no `--no-cov-on-fail`, no `continue-on-error: true`, no `if: always()` on the gate steps themselves (only the artifact-upload steps carry `if: always()`, so an artifact is still captured for debugging even when the gate fails). Lowering a threshold to unblock a PR is a decision that must be visible as a diff to `pyproject.toml`/`vitest.config.ts`/`build.gradle.kts` in that PR, reviewable by CODEOWNERS like any other change — never a hidden CI-only override.
- **Emergency-hotfix path:** per §15, the sanctioned way to ship an urgent fix that cannot practically be fully tested in time is a scoped, inline, reviewed exception (`# pragma: no cover` / an Istanbul `/* istanbul ignore next */` comment / a Kover `excludes` addition for one named class) with a linked follow-up issue — never a global `fail_under`/`thresholds`/`bound` reduction.

## 10. Error Handling and Edge Cases

| Scenario | Behavior / Resolution |
|---|---|
| **A PR that legitimately doesn't touch coverage-relevant code** (e.g., only edits `api.py`, `models.py`, a `docs/**` file, or a Composable) | The gate's numerator and denominator are both computed strictly from the `--include`/`include`/`packages()` filter (§2). A file outside that filter contributes nothing to either side of the percentage, so it is structurally impossible for such a PR to move the measured percentage — it is never falsely blocked. This is a property of the scoping design, not a special-cased exemption bolted on afterward. |
| **A PR that touches an *included* file (e.g., `rewards/service.py`) and adds new, untested lines** | The percentage can legitimately drop and the gate can legitimately fail — this is the gate working as intended, not a false positive. The resolution is adding a test, not adjusting the threshold (§9). |
| **Generated-code false negatives** (a generated OpenAPI TS client regeneration, an Alembic migration, Kover-instrumented Compose-compiler synthetic classes) | Prevented **structurally**, not tolerated-then-corrected: every category of generated code is already in the `omit`/`exclude`/`excludes{}` list in §2 and §7, so it never enters either tool's measured file set in the first place. If a future generator's output pattern is *not* yet covered by these exclusion lists (e.g., a new KSP processor introduced by a later phase), that is a genuine gap in this file's exclusion patterns to extend — not something to work around by inflating the numerator elsewhere. |
| **Flaky-test-driven false coverage drops** | A flaky test failure fails the *test-execution* step (`pytest tests/unit`, `vitest run`, `testDebugUnitTest`) itself, which runs **before** any coverage-report/gate step in the same job — per GitHub Actions' default step-failure behavior, the job stops at that step and the coverage-report/gate steps never execute at all that run. There is therefore no scenario where a flaky test produces a *misleading* coverage percentage; it produces no coverage report at all for that run, surfacing as a test failure, not a coverage failure. Apply `CI_CD.06` §10's existing flaky-test quarantine mechanism (`@pytest.mark.flaky` / `.fixme` with a tracked issue / `@Ignore("NH-xxx: flaky, see issue")`) — a *retried* flaky test (via `pytest-rerunfailures`, already wired for the integration-test job) still executes its body and still contributes coverage once it passes; a fully `@pytest.mark.skip`-quarantined test genuinely stops contributing coverage for the code path only it exercised, which is a legitimate, visible "this is currently untested in CI" signal to act on, not a bug to mask. |
| **Initial rollout finds the codebase currently *below* the target threshold** for a given layer (a realistic possibility even after all feature phases, since no prior gate enforced this) | Do not fabricate compliance by silently lowering `fail_under`/`thresholds`/`bound` to whatever the current number happens to be without tracking it. Instead: measure the actual current percentage at implementation time, set the gate's threshold to that *measured* value **rounded down to the nearest whole percent**, open a tracked backlog issue titled "Raise `<layer>` coverage gate to the Final_Development_Prompt §5 target of `<N>`%," and land the true target as a follow-up PR once real tests close the gap. This ratchet is itself part of this blueprint's Definition of Done (§17) if — and only if — the measured baseline is confirmed below target; if the baseline already meets or exceeds target, land the true 80/70/70 values directly with no ratchet needed. |
| **A dependency-only PR** (e.g., a `uv.lock`/`pnpm-lock.yaml`/`libs.versions.toml` bump with no source change) | No included file changes, so no percentage moves; the gate passes trivially (assuming the prior baseline was already passing) — expected, not a gap. |

## 11. State Management and Lifecycle Considerations

- **Every coverage-gate run is stateless and idempotent**, matching `CI_CD.06` §11's principle for the rest of the pipeline: each run recomputes coverage from scratch against that run's own test execution; there is no persisted "previous run's percentage" this file compares against, and no run-to-run delta/regression-detection logic is built here.
- **Coverage trend tracking over time and badge publishing are explicitly out of scope for this baseline.** Final_Development_Prompt §5/§8 name no specific vendor for a coverage-history dashboard (unlike, say, Sentry for error tracking or Prometheus/Grafana for metrics), so this file does not invent one. What this file *does* provide, durably, is the raw material a future phase would need: `coverage.xml` (backend), `coverage/lcov-report/` + `coverage/coverage-final.json` (admin-web), and `build/reports/kover/report.xml` (mobile) are all uploaded as workflow artifacts on **every** run (14-day retention, §7). A future item wiring these into Codecov/Coveralls, a GitHub Pages badge generator reading `coverage.xml`'s `line-rate` attribute, or an internal dashboard can consume these artifacts (or add a lightweight upload step pointing at the same generated files) without any change to this file's gate mechanism, config files, or CI step structure — the gate and the trend-reporting concern are cleanly decoupled by design.
- **No manual approval or lifecycle state is introduced.** Unlike Stage 11's human promotion gate (owned by `CI_CD.09`), a coverage-gate failure is resolved the same way any other automated CI failure is: fix the code (add tests) and push again. There is no "coverage exception approval workflow" UI or persisted state — the one sanctioned exception path (§9's inline `pragma`/`ignore` comments) is itself just a code change, reviewed like any other.

## 12. Integration Points with Existing Modules

- **`CI_CD.06`'s `unit-test` job, all three apps — the single integration point this entire file exists to modify.** No other job in any of the three workflows is touched: `lint`, `static-analysis`, `integration-test`, `architectural-invariant`, and `build-artifact` are all byte-for-byte unchanged from `CI_CD.06`'s implementation. This file's diffs are scoped exclusively to the step list inside each `unit-test` job (§7).
- **Required-status-check names are unchanged** (§2, §7) — `Repo.03`'s branch-protection configuration needs **zero** updates as a result of this file's implementation; the same three job names (`Backend CI / Unit Tests (pytest)`, `Admin Web CI / Unit Tests (vitest)`, `Mobile CI / Unit Tests (JVM)`) that were already required continue to be the same required checks, now doing more (coverage-gated) work inside.
- **`openapi-sync.yml` is untouched and unrelated** — its own `git diff --exit-code` check against the generated client (`CI_CD.06` §7.4) is a *different* kind of gate (contract drift, not test coverage) and this file's admin-web exclusion of `src/lib/api-client/**` (§2.2) means the two mechanisms never interact.
- **Three separate tools, reported consistently:** despite `coverage.py`, Istanbul, and Kover being unrelated tools with different CLIs and config surfaces, this file keeps the developer- and reviewer-facing experience consistent across all three: (a) every gate's failing step has a name containing the words "Coverage gate" or is otherwise unambiguously the coverage step (never a bare `run: <tool> test` whose failure could be test-failure or coverage-failure), (b) every gate uploads its report as a workflow artifact under a `<app>-*coverage*`/`<app>-kover-report` name with the same 14-day retention `CI_CD.06` already established for PR-scoped artifacts, and (c) every gate's threshold number is a first-class, greppable value in its stack's native config file (`pyproject.toml`, `vitest.config.ts`, `build.gradle.kts`) rather than buried in a CI YAML `run:` string — so "what is our current coverage bar for X" has exactly one place to look per stack, not two.
- **`CORE_UI_INSTRUCTIONS.md`'s `BaseViewModel`/package-convention** — this file's mobile scoping (§2.3) is not an invented convention; it is a direct, literal extension of the package naming `core-ui` already documents for itself (`com.noorheroes.core.ui.viewmodel`) to every other module. No change to `core-ui` or any ViewModel implementation is made or required by this file.

## 13. Development Steps in the Correct Implementation Order

1. Confirm `backend/pyproject.toml` does not already define a conflicting `[tool.coverage.*]` section (`CI_CD.06`'s baseline only referenced `--cov`/`--cov-fail-under` as CLI flags, so a conflict is unlikely but must be checked, not assumed) — add §7.1's block.
2. Replace `backend.yml`'s `unit-test` job step list with §7.1's version. Push to a scratch branch; open a throwaway PR; confirm the job still passes against the current, already-implemented backend codebase (if it does not — see §10's "initial rollout below target" edge case before proceeding).
3. Confirm `admin-web/vitest.config.ts` exists with a working `test` block (per `CI_CD.06`'s assumption that `pnpm vitest run --coverage` already works) — extend it with §7.2's `coverage` block.
4. Replace `admin-web.yml`'s `unit-test` step with §7.2's simplified version. Verify on a scratch PR, same as step 2.
5. Add the Kover Gradle Plugin coordinate to `mobile/gradle/libs.versions.toml` (§7.3).
6. Apply `alias(libs.plugins.kover)` to the root `build.gradle.kts` and to every `core-*`/`feature/*` module's `build.gradle.kts` (§7.3) — confirm the module list in root's `kover(project(...))` dependency block (§7.3) matches the *actual* current set of Gradle modules (cross-check against `mobile/settings.gradle.kts`'s `include(...)` calls; do not assume the illustrative list in §7.3 is exhaustive or current).
7. Author the root `kover { reports { filters { ... } verify { ... } } }` block (§7.3) exactly as specified, re-verifying the Kover DSL syntax against the actually-pinned Kover version's documentation (the DSL has changed across Kover's 0.6→0.7→0.8 releases; §18 item 5's note applies here specifically).
8. Add the three new steps to `mobile.yml`'s `unit-test` job (§7.3). Verify on a scratch PR.
9. For each stack, deliberately introduce one untested branch in an *included* file on a separate scratch branch and confirm the gate fails at the expected, distinctly-named step (§14's acceptance checks 1/3/4) — then deliberately touch only an *excluded* file and confirm the gate is unaffected (§14's checks 2/5).
10. Measure the actual, current coverage percentage for each of the three scoped layers against the real (already-implemented) codebase. If any is below its Final_Development_Prompt §5 target, apply the ratchet procedure in §10's edge-case row (temporary threshold + tracked follow-up issue) instead of landing a threshold the codebase cannot currently pass.
11. Delete all scratch branches/PRs used for steps 2, 4, 8, and 9's verification once each is confirmed.
12. If any ratchet from step 10 was applied, file the tracked follow-up issue referenced there before considering this blueprint done.

## 14. Testing Strategy and Acceptance Criteria

| # | Check | How to verify | Expected result |
|---|---|---|---|
| 1 | Backend gate blocks a real domain-service coverage regression | Add an untested `if`/`else` branch to `identity/service.py` that drags the scoped (`modules/*/service.py` + `base_service.py`) percentage below 80% | `Backend CI / Unit Tests (pytest)` fails specifically at the "Coverage gate — domain/service layer ≥80%" step; the preceding "pytest (unit, parallelized)" and "Full-repo coverage report" steps still show green, proving the failure is the scoped gate, not a test failure or the informational report |
| 2 | Backend gate does not falsely block excluded-file-only changes | Open a PR touching only `identity/api.py` (adding a comment, no logic change) | All `unit-test` steps pass; the reported scoped percentage is byte-identical to the pre-PR baseline |
| 3 | Admin-web gate blocks a real `src/features/` coverage regression | Add an untested branch to `src/features/commerce/hooks/useRefund.ts` that drags `src/features/**`'s aggregate below 70% | `Admin Web CI / Unit Tests (vitest)` fails; the failure output names the specific threshold(s) missed (Vitest's own coverage-failure output format) |
| 4 | Admin-web gate does not falsely block excluded-file-only changes | Open a PR touching only `src/components/Button.tsx` | `unit-test` passes; `src/features/**`'s reported percentage is unchanged |
| 5 | Mobile gate blocks a real ViewModel-layer coverage regression | Add an untested branch to a `commonMain` `BaseViewModel` subclass (e.g., `HabitsViewModel`) that drags the merged `com.noorheroes.*.viewmodel` percentage below 70% | `Mobile CI / Unit Tests (JVM)` fails at the "Coverage gate — ViewModel layer ≥70%" step; `testDebugUnitTest` and `koverXmlReport` steps still show green |
| 6 | Mobile gate does not falsely block Composable-only changes | Open a PR touching only a `@Composable` function in a `*Screen.kt` file | `unit-test` passes; the merged ViewModel percentage is unchanged |
| 7 | Required-status-check names are unchanged post-implementation | Compare `Repo.03`'s registered required-checks list before and after this file's implementation | Identical set of three `Unit Tests (...)` check strings — no re-registration needed |
| 8 | Flaky test does not produce a misleading coverage result | On a scratch branch, make one already-quarantined-eligible test intermittently fail (simulate via a timing assertion), observe two consecutive runs | Coverage-gate steps either don't run at all (test step failed first) or run against a full, successful test pass (if the flaky test was quarantined/retried and passed) — never a partial/misleading percentage from a run where the test step itself failed |
| 9 | Baseline reconciliation (if applicable per §10/§13 step 10) | Run each gate against the real, current codebase with the *true* Final_Development_Prompt §5 targets (80/70/70), not a ratcheted value | Either all three pass outright, or every layer currently below target has a documented ratchet value plus a linked tracked issue — no layer is silently under-target with no threshold enforcing anything |

**Definition of "acceptance":** all 9 checks pass, demonstrated on real scratch PRs against a real GitHub repository (not simulated), by someone who has not seen this file before, using only this document plus `CI_CD.06`'s already-implemented workflows and the already-implemented application code.

## 15. Production-Readiness Considerations

- **Instrumentation overhead is accepted, not optimized away.** `coverage.py`'s line-tracing (~10–20% slower test runs), Istanbul's AST instrumentation, and Kover's bytecode instrumentation are all modest, well-understood costs already implicitly paid the moment `CI_CD.06`'s baseline `--cov`/`--coverage`/(newly, here) Kover-enabled test runs execute — this file adds zero *additional* test executions (§3.2, §7.3's "last step, no re-run" note), so there is no incremental performance regression beyond what enabling coverage collection at all already costs.
- **A ratcheted, below-target threshold (§10) must carry a tracked, linked follow-up issue and must never become the new permanent target by omission.** Treat an open ratchet issue as a Definition-of-Done blocker for closing out this blueprint's own tracking ticket, even though the CI gate itself will happily stay green at the ratcheted value indefinitely if nobody revisits it.
- **Never disable a gate to unblock an urgent hotfix.** The sanctioned emergency path is the scoped, reviewed, inline exception described in §9/§15's earlier note (a named `pragma`/`ignore` comment with a linked justification) — a global threshold reduction to "get CI green" defeats the purpose of building this file at all and must be treated as a CODEOWNERS-blocking request, not a quick fix.
- **This file assumes GitHub-hosted `ubuntu-latest` runners for all three workflows**, matching `CI_CD.06`'s own assumption (§3.4 of that file) — no change to runner sizing/OS is introduced by adding coverage collection.
- **Kover's DSL and the Kotlin/Compose Multiplatform Gradle plugin ecosystem move quickly** — re-verify `org.jetbrains.kotlinx.kover`'s pinned version and exact `kover { }`/`verify { }` block syntax against the plugin's current documentation at implementation time (§18 item 5), the same discipline `CI_CD.06` §18 item 5 already establishes for every other pinned Action/tool version in this project.

## 16. Dependencies and Prerequisites

- **`CI_CD.06` must already be implemented and merged** — this file's every edit is a diff against `backend.yml`/`admin-web.yml`/`mobile.yml`'s `unit-test` jobs as `CI_CD.06` built them; without those jobs existing first, there is nothing to modify.
- **Real application code from the feature phases must already exist** — `src/noorheroes/modules/*/service.py` for all 12 bounded contexts, `admin-web/src/features/**`, and mobile `BaseViewModel` subclasses across `core-*`/`feature/*` modules must be substantively implemented (per this project's stated repository status) for any of these percentages to be meaningful; a gate against near-empty source directories is vacuous.
- **`backend/pyproject.toml` must already have working `[tool.pytest.ini_options]`** (confirmed present per `CI_CD.06` §13 step 1) — this file only adds `[tool.coverage.*]` alongside it.
- **`admin-web/vitest.config.ts` must already exist with a working `test` runner configuration** — this file only extends its `coverage` sub-block.
- **`mobile/gradle/libs.versions.toml` and `mobile/settings.gradle.kts` must already enumerate the real, current set of `core-*`/`feature/*` modules** — §13 step 6 depends on this being accurate at implementation time, not on the illustrative list in §7.3.
- **`Repo.03`'s branch protection must already register the three `Unit Tests (...)` required-check strings** (per `CI_CD.06`'s hand-off) — this file relies on that existing registration to make the gate actually block merge; it registers nothing new itself.

## 17. Definition of Done

- [ ] `backend/pyproject.toml` has the `[tool.coverage.run]`/`[tool.coverage.report]` block from §7.1, and `backend.yml`'s `unit-test` job matches §7.1's step list exactly (job `name:`/`needs:` unchanged from `CI_CD.06`).
- [ ] `admin-web/vitest.config.ts` has the `test.coverage` block from §7.2, and `admin-web.yml`'s `unit-test` job matches §7.2's simplified step list.
- [ ] `mobile/gradle/libs.versions.toml` has the Kover plugin coordinate; root `build.gradle.kts` and every `core-*`/`feature/*` module's `build.gradle.kts` apply it; the root `kover { }` block matches §7.3's filters/verify rule; `mobile.yml`'s `unit-test` job has the three added steps.
- [ ] All 9 checks in §14 pass, verified via real scratch PRs.
- [ ] No new required-status-check name was introduced anywhere; `Repo.03`'s branch-protection configuration required zero changes (§14 check 7).
- [ ] Every exclusion pattern in §2 is implemented exactly as specified in the three config files (spot-check: generated OpenAPI client, Alembic migrations, and Composable files are confirmed absent from their respective tool's measured file set, not merely assumed excluded).
- [ ] If the real, current codebase measured below any target at implementation time, a ratchet threshold is in place with a linked, tracked follow-up issue (§10, §13 step 10, §15) — otherwise the true 80/70/70 values are landed directly.
- [ ] No change was made to any application source file (`service.py`, `src/features/**`, ViewModel classes) — only configuration files and CI step lists, per §2's "explicitly not rebuilt" list.
- [ ] No change was made to `CI_CD.06`'s `lint`, `static-analysis`, `integration-test`, `architectural-invariant`, or `build-artifact` jobs in any of the three workflows, nor to `openapi-sync.yml` or `secret-scan.yml`.

## 18. Assumptions or Decisions the Coding Agent Must Follow

1. **Line coverage, not branch coverage, is the metric for backend and mobile; admin-web gates all four Istanbul metrics (lines/functions/statements/branches) uniformly at 70.** Final_Development_Prompt §5 does not specify a metric. Line coverage is `coverage.py`'s and Kover's simplest, lowest-overhead default and avoids the extra instrumentation cost/DSL complexity of branch-mode; Istanbul reports all four metrics by default at near-zero extra cost, and gating only one of the four there would leave an obvious blind spot (a function whose one giant branch is untested could still show 100% "function" coverage while genuinely broken business logic goes unexercised). This asymmetry across stacks is a deliberate, documented choice — not an inconsistency to "fix" by forcing all three onto the same metric.
2. **Mobile's v1 gate scope is ViewModel classes only** (`com.noorheroes.*.viewmodel` packages), **not** a broader `com.noorheroes.*.service.*` convention for non-ViewModel business/use-case classes, even though Final_Development_Prompt §5's row text says "ViewModel/service layer." This project's mobile architecture docs (`CORE_UI_INSTRUCTIONS.md`, `CORE_DATA_INSTRUCTIONS.md`) establish `BaseViewModel` and `*Repository` naming conventions but do not establish a distinct, consistently-applied "service" package/class convention outside `core-ui`'s own base class. Rather than invent one, this file scopes tightly to what the codebase's actual, confirmed convention supports mechanically today. Broadening the Kover `includes { packages(...) }` filter to a `.service.` convention is a valid, welcome follow-up **once** an implementer confirms such a convention actually exists consistently across modules at implementation time — do not silently expand scope based on this document's text alone.
3. **All three gates apply a global (aggregate-within-scope) threshold, never a per-file threshold.** A single under-tested file cannot fail the gate on its own as long as the rest of the scoped layer comfortably clears the bar — this is the standard behavior of `coverage report --fail-under`, Vitest's default (non-`perFile`) threshold mode, and Kover's default `bound` evaluation, and matches how Final_Development_Prompt §5 phrases each target ("≥80% on `domain/`", not "≥80% on every file in `domain/`"). Do not add `perFile: true` (Vitest) or an equivalent per-class Kover rule without an explicit, separate decision — doing so retroactively fails many currently-acceptable individual files and is a materially different (stricter) policy than what was asked for.
4. **The root `build.gradle.kts` `kover(project(":..."))` module list (§7.3) must be kept in sync with the actual module graph by hand** — Kover's merged-report mechanism requires each participating subproject to be explicitly declared; there is no auto-discovery. A newly-extracted `feature/*` module (per Final_Development_Prompt §2.1's "start as a package, extract to a real Gradle module incrementally" allowance) that is not added to this list silently drops out of the coverage gate's denominator — flagged here explicitly so it isn't discovered as a surprise gap later. Adding a module-graph-sync check to CI (e.g., diffing `settings.gradle.kts`'s `include(...)` list against the `kover(project(...))` list) is a reasonable future hardening, not required by this baseline.
5. **The Kover version (`0.8.3` in §7.3) and its exact DSL block syntax are a known-good baseline as of this document's authoring — re-verify both against the plugin's current documentation at implementation time**, per `CI_CD.06` §18 item 5's identical instruction for every other pinned tool/action version in this project. The Kover Gradle Plugin's configuration DSL has changed shape across its 0.6→0.7→0.8 line; do not assume the exact block in §7.3 is forward-compatible without checking.
6. **No coverage-trend dashboard, badge, or history mechanism is built by this file** (§11) — only the raw artifact outputs a future item could consume. Do not scope-creep this blueprint into standing up Codecov/Coveralls/a custom dashboard; that is explicitly deferred, undecided future work with no named vendor in the source documents.

---

## AI Agent Development Prompt

Implement coverage-gate enforcement for the NoorHeroes monorepo's CI pipeline exactly as specified in this document. `CI_CD.06`'s six-job-per-app pipeline (`lint → static-analysis → unit-test → integration-test → architectural-invariant → build-artifact`) already exists and works; the backend, admin-web, and mobile application code already exists and works. You are editing **only** the `unit-test` job in each of `backend.yml`/`admin-web.yml`/`mobile.yml`, plus adding a coverage-configuration block to one existing config file per stack — nothing else.

**What to build, and exactly where:**
1. `backend/pyproject.toml` — add the `[tool.coverage.run]`/`[tool.coverage.report]` block from §7.1. Replace `backend.yml`'s `unit-test` job step list with §7.1's three-step coverage sequence (collect → informational report → scoped gate), keeping the job's `name:`/`needs:` exactly as `CI_CD.06` defined them.
2. `admin-web/vitest.config.ts` — add the `test.coverage` block from §7.2 (`include: ["src/features/**/*.{ts,tsx}"]`, four thresholds at 70). Simplify `admin-web.yml`'s `unit-test` step to the plain `pnpm vitest run --coverage` invocation from §7.2 — scoping and thresholds now live in config, not CLI flags.
3. `mobile/gradle/libs.versions.toml`, root `build.gradle.kts`, and every `core-*`/`feature/*` module's `build.gradle.kts` — add and apply the Kover Gradle Plugin per §7.3, including the merged-report module list (verify it against the actual current module graph, don't trust the illustrative list verbatim), the `viewmodel`-package include filter, the Composable/DI/generated-code exclude filters, and the `verify { rule { bound { minValue = 70 } } }` block. Add the three new steps (`koverXmlReport`, artifact upload, `koverVerify`) to `mobile.yml`'s `unit-test` job.

**Conventions to follow (do not deviate without the documented justification each requires):**
- Backend/mobile gate on **line** coverage; admin-web gates all four Istanbul metrics at 70 uniformly. This asymmetry is deliberate (§18 item 1).
- Backend's exclusion set: `api.py`, `repository.py`, `models.py`, `schemas.py`, `events.py`, `infrastructure/`, `core/`, `workers/`, `scripts/`, Alembic migrations — only `modules/*/service.py` and `common/base_service.py` count.
- Admin-web's exclusion set: `src/lib/api-client/**` (generated), `src/components/**` (shared design system), `src/app/**` (route shells), `src/lib/auth/**` (covered by the architectural RBAC test) — only `src/features/**` counts.
- Mobile's exclusion set: every `@Composable` function/file, `di/**`, generated/synthetic code — only `com.noorheroes.*.viewmodel` classes count. Do **not** broaden to a `.service.` package convention without first confirming it exists (§18 item 2).
- Thresholds are **global within scope**, never per-file (§18 item 3).
- Required-status-check names must not change — you are editing existing job internals, not creating new jobs. If your diff changes a job's `name:` field, you have gone out of scope; revert and re-check against §7's exact YAML.

**What NOT to change:**
- Any application source file under `backend/src/`, `admin-web/src/`, or `mobile/**` — this blueprint is CI/config-only.
- `CI_CD.06`'s `lint`, `static-analysis`, `integration-test`, `architectural-invariant`, or `build-artifact` jobs, in any of the three workflows.
- `openapi-sync.yml`, `secret-scan.yml`, or anything under `infra/`.
- `Repo.03`'s branch-protection configuration — no new required-check registration is needed or should be attempted.

**How to verify you're done (walk through all of these before considering the task complete):**
1. Run all three modified workflows on the real, current codebase and record the actual measured percentage for each of the three scoped layers. If any is below its target (80/70/70), apply §10's ratchet procedure and file the tracked follow-up issue — do not land a threshold the codebase cannot currently pass, and do not silently under-report a lower number as if it were the target.
2. On separate scratch branches, deliberately drag each layer's scoped coverage below its threshold (one untested branch in an included file) and confirm the corresponding job fails at the specific, distinctly-named coverage-gate step — not at test execution, not at a different step.
3. On separate scratch branches, touch only an excluded file per stack (a router, a generated client file, a Composable) and confirm the gate is entirely unaffected — same percentage, same pass result.
4. Confirm no required-status-check name changed by diffing `Repo.03`'s registered list before and after.
5. Confirm all three coverage artifacts (`coverage.xml`, `admin-web/coverage/`, `mobile/build/reports/kover/report.xml`) are present as workflow-run artifacts with 14-day retention on a normal passing run.
6. Walk every checkbox in §17's Definition of Done in order and confirm each is literally true against the repository state you produced.
