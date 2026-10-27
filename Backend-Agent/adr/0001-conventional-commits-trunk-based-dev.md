> [!NOTE]
> **@deprecated**: For production release workflows and commit guidelines, see [`NoorHeroes-Backend/MASTER-README.md`](../../NoorHeroes-Backend/MASTER-README.md#20-developer-onboarding--workflow).

# ADR 0001: Conventional Commits, Trunk-Based Development & Automated SemVer

## Status
Accepted

## Context
The NoorHeroes Backend codebase is scaling toward multiple bounded contexts, automated CI/CD pipelines, and multi-platform consumer clients (Mobile App, Admin Web Portal). Prior to this policy, commit messaging, branch management, and release versioning were informal tribal practices without machine-enforced gates.

To support robust delivery, auditability, reproducible builds, and automated changelogs:
1. Changes landing on `main` must follow a standard structured grammar to enable automated release analysis and changelog generation.
2. The branching model must prevent integration friction and merge hell associated with long-lived feature/release branches.
3. High-risk subsystem changes (JWT auth, reward ledger, media upload pipeline) must receive mandatory domain/security team review before merge.
4. Release versioning must be automated and decoupled from manual `/v1`/`/v2` REST API contract versioning.

## Decision
We adopt:
1. **Conventional Commits v1.0.0**: Enforced via `commitlint` locally (Husky v9) and authoritatively in CI (`commitlint.yml` and `pr-title-lint.yml`). The allowed types are: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `perf`, `security`, `build`, `ci`, `revert`.
2. **Trunk-Based Development with Squash-Merge Only**:
   - `main` is the sole long-lived trunk.
   - Prohibited long-lived branches: `develop`, `release/*`, `staging`.
   - Feature branches are short-lived (`<type>/<ticket-id>-<kebab-slug>`).
   - Every PR is squash-merged, deriving the commit message from the PR title and ensuring linear git history.
3. **Automated Semantic Versioning via `semantic-release`**:
   - Commits to `main` evaluate release rules via `@semantic-release/commit-analyzer`.
   - Automated generation of `CHANGELOG.md`.
   - Automated bumping of `pyproject.toml` version via `scripts/release/bump_backend_version.py`.
   - Immutable tagging (`backend-vX.Y.Z`).
4. **Mandatory CODEOWNERS Review for Blast-Radius Paths**:
   - `src/noorheroes/core/security.py` & `src/noorheroes/core/deps.py`
   - `src/noorheroes/modules/rewards/**`
   - `src/noorheroes/modules/media/**`
5. **Idempotent Branch Protection as Code**:
   - Configured via `infra/ci/configure-branch-protection.sh` using GitHub CLI (`gh api`), enforcing status checks, reviews, linear history, and admin enforcement.

## Consequences

### Positive
- **Deterministic Release Notes & Changelogs**: Changes are documented automatically without manual authoring.
- **Auditability**: Clean, single-commit-per-PR linear history on `main` makes `git bisect` and post-incident analysis straightforward.
- **Security & Safety Guardrails**: High-risk subsystems cannot be merged without designated team approvals.
- **Friction-Free Local Iteration**: Developers can create WIP commits on feature branches because squash-merge enforces grammar at the PR title level upon merge.

### Negative / Trade-offs
- Contributors must learn Conventional Commit syntax and branch naming conventions.
- `CHANGELOG.md` and `pyproject.toml`'s `version` field become machine-managed and must not be edited manually on feature branches.
- Requires Node.js 20 runtime in CI runners to execute `commitlint` and `semantic-release`.
