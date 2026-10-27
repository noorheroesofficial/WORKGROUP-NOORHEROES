# Phase 0 — Cross-Cutting Coding Standards, Linting & Formatting Configuration

`Development_Blueprints.Phase0_Project_Repo_Foundation.Repo.02-coding-standards-linting-formatting-config.md`

**Module:** Repo (cross-cutting code quality and linting governance)  
**Phase:** 0 — Project & Repository Foundation  
**Status:** ✅ **Implemented & Verified**  
**Depends on:** Phase 0 item 01 (`Repo.01-monorepo-scaffold-workspace-structure.md`)  
**Consumed by:** Phase 0 item 03 (Git hooks), Phase 1 CI/CD pipelines (`CI_CD.06-ci-pipeline-lint-test-build-stages.md`), and all engineering contributions  
**Source of truth:** `DEVELOPMENT-RULES.md`; `NoorHeroes_Consolidated_Execution_Blueprint.md` §1; `NoorHeroes-Backend/pyproject.toml`; `noorheroes-admin/.eslintrc.json`  

---

## 1. Objective and Purpose

Establish uniform, automated, non-bypassable code formatting, static analysis, and quality standards across all three software platforms in the monorepo:
1. **Python / FastAPI Backend:** `ruff` (formatting, imports, and linting), `mypy` (strict static typing), and `bandit` (security vulnerability scanning).
2. **Kotlin Multiplatform Mobile:** `ktlint` and `Spotless` (formatting and style guide enforcement), `detekt` (code smells, complexity, and architectural invariant enforcement).
3. **TypeScript / Next.js Admin & Web:** `ESLint` (React, Next.js, and TypeScript rules), `Prettier` (formatting), and `TypeScript` compiler strict mode (`tsc --noEmit`).

---

## 2. Platform-Specific Tooling & Invariants

### 2.1 Python / FastAPI (`NoorHeroes-Backend/`)
- **Formatter & Linter:** `ruff` configured in `pyproject.toml`:
  - Line length: 100 characters.
  - Target Python version: 3.11+.
  - Rule sets enabled: `E` (pycodestyle errors), `F` (Pyflakes), `I` (isort imports), `B` (flake8-bugbear), `UP` (pyupgrade), `S` (flake8-bandit security).
- **Type Checker:** `mypy --strict`:
  - Disallow untyped defs, require explicit optional handling, strict dictionary typing.
- **Architectural Rules:**
  - Routers must never call repositories directly; all data access routes through Domain Services.
  - Pydantic v2 schemas used for all request/response serialization; raw ORM models never returned to API callers.

### 2.2 Kotlin Multiplatform (`NoorHeroes/`)
- **Formatter:** `Spotless` with `ktlint` engine:
  - Max line length: 120 characters.
  - Trailing commas required on multi-line parameter lists.
- **Static Analysis:** `detekt`:
  - Enforce immutability (`val` over `var` wherever possible).
  - Enforce unidirectional data flow (UDF) in CMP ViewModels (`StateFlow<UiState>`).
  - Strict absence of Android SDK imports inside `commonMain` (ensuring iOS binary portability).

### 2.3 TypeScript / Next.js (`noorheroes-admin/` & `Parent Web Portal`)
- **Linter:** `ESLint` with `@typescript-eslint/recommended`, `eslint-config-next`, and `tailwindcss` plugins.
- **Formatter:** `Prettier`:
  - Single quotes, trailing commas (`es5`), 2 spaces indentation, 100 characters print width.
- **Strict Typing:** `tsconfig.json`:
  - `"strict": true`, `"noImplicitAny": true`, `"strictNullChecks": true`.
  - Zero use of `any`; all API responses typed via generated Zod/TypeScript contracts.

---

## 3. Pre-Commit & CI Automation

1. **Local Pre-Commit Hook:**
   - Pre-commit configuration (`.pre-commit-config.yaml`) runs `ruff check`, `ruff format`, `ktlint`, and `prettier` on staged files.
   - Fast execution (< 3 seconds) providing immediate developer feedback.
2. **Non-Bypassable CI Gate (Stage 1 of Pipeline):**
   - GitHub Actions workflow executes complete lint and type check on every PR before test suites execute.
   - Any lint failure, unformatted file, or static typing error immediately fails the CI build and blocks merge.

---

## 4. Verification and Acceptance Criteria

- [x] Ruff configuration verified in `NoorHeroes-Backend/pyproject.toml`.
- [x] Strict TypeScript configuration verified in `noorheroes-admin/tsconfig.json`.
- [x] Kotlin linting scripts configured in `NoorHeroes/build.gradle.kts`.
- [x] CI pipeline Stage 1 executes lint and static analysis across all three platforms.
