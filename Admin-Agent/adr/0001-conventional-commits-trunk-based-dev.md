# 1. Conventional Commits, SemVer & Branching Policy

Date: 2026-08-27

## Status

Accepted

## Context

As the NoorHeroes ecosystem scales across frontend, backend, and mobile applications, development discipline and merge standards must be formalized and automated as code rather than relying on tribal knowledge or manual review vigilance.

Without formal enforcement:
1. Commit messages become inconsistent, making `git bisect`, security audits, and automated changelog generation error-prone or impossible.
2. Long-lived feature branches drift, accumulating merge conflicts and delaying delivery.
3. Merge strategies risk producing tangled merge bubbles or non-linear history on `main`.
4. High-risk security boundaries (such as authentication tokens, proxy middleware, and API client boundaries) could merge without required security reviews.

## Decision

We adopt a comprehensive Conventional Commits, Trunk-Based Development, and Automated Branch Protection policy for `noorheroes-admin` (`admin-web`):

1. **Conventional Commits Grammar:**
   - Enforce Conventional Commits v1.0.0 grammar (`<type>(<scope>)!: <subject>`) with a maximum header length of 72 characters and lowercase imperative subject.
   - Enforce exactly 11 standard commit types: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `perf`, `security`, `build`, `ci`, `revert`.
   - Implement local fast feedback via `.husky/commit-msg` using `commitlint` and authoritative non-bypassable verification in CI via `.github/workflows/commitlint.yml`.

2. **Branch Naming Standard:**
   - Enforce branch naming pattern `^(feat|fix|chore|docs|refactor|test|perf|security|build|ci|revert)\/[a-zA-Z0-9]+-[a-z0-9][a-z0-9-]*$` in CI via `.github/workflows/branch-name-lint.yml`.
   - Strictly prohibit long-lived `develop`, `release/*`, and `staging` branches.

3. **Trunk-Based Development & Squash-Merge Policy:**
   - `main` is the only long-lived branch.
   - All PRs merge into `main` exclusively via **Squash-Merge**, creating exactly one clean commit per PR.
   - PR titles are verified via `amannn/action-semantic-pull-request` (`.github/workflows/pr-title-lint.yml`) because GitHub uses the PR title as the commit message on `main`.
   - Linear history is strictly required on `main`.

4. **Continuous Deployment & SemVer Strategy:**
   - `admin-web` is continuously deployed on push to `main` and tracks `main` continuously without standalone SemVer tag releases.

5. **CODEOWNERS & Blast-Radius Review Checklist:**
   - Assign `@noorheroes/core-team` and `@noorheroes/admin-team` for general code review.
   - Mandate `@noorheroes/security-team` approval for blast-radius paths (`src/lib/api-client.ts`, `src/lib/auth-token.api.ts`, `src/proxy.ts`, `src/features/auth/**`).
   - Standardize PR descriptions using `.github/PULL_REQUEST_TEMPLATE.md`.

6. **Branch Protection as Code:**
   - Provide `infra/ci/configure-branch-protection.sh` using GitHub CLI (`gh api`) to idempotently enforce required checks, reviews, linear history, and administrator enforcement on `main`.

## Consequences

### Positive
- **Auditable History:** Clean, linear git history on `main` where each commit represents a single atomic, reviewed, and tested pull request.
- **Fast Developer Feedback:** Developers receive immediate local feedback on commit messages and pre-push unit tests before waiting for CI.
- **Security & Blast-Radius Governance:** Critical token, proxy, and auth changes cannot merge without explicit security review.
- **Reproducible Infrastructure:** Branch protection settings are defined as code in version control rather than manual GitHub UI clicks.

### Negative / Trade-offs
- Contributors must adhere to strict branch naming and commit syntax; commits or PR titles with improper capitalization or missing types will be blocked by CI until corrected.
