# Phase 0 — Conventional Commits, SemVer & Branching Policy

`Development_Blueprints.Phase0_Project_Repo_Foundation.Repo.03-conventional-commits-semver-branching-policy.md`

**Module:** Repo (cross-cutting — applies to `backend/`, `admin-web/`, `mobile/`, `infra/`, `docs/`, and the repo root)
**Phase:** 0 — Project & Repository Foundation
**Status:** ✅ **Implemented & Verified** (2026-08-27)
**Depends on:** Phase 0 item 01 (`Repo.01-monorepo-scaffold-workspace-structure.md` — monorepo skeleton, already complete)
**Consumed by:** Phase 1 Infra/CI items (`backend.yml`, `admin-web.yml`, `mobile.yml`, `openapi-sync.yml`) which append their own job names to this file's required-status-checks list; Phase 12 `CrossPlatform.01-definition-of-done-ga-gate-checklist.md`, which references this file's branch-protection config as one of its GA-gate checks.
**Source of truth:** `NoorHeroes_Final_Development_Prompt.md` §4 ("Code Quality: Linting, Formatting, Static Analysis, Git Hooks") and §6 ("CI/CD Pipeline" → "Branching/versioning strategy"); `NoorHeroes_Consolidated_Blueprint_v6.md` (referenced for cross-context consistency; it does not define its own competing branching/commit policy).

---

## 1. Objective and Purpose

The NoorHeroes monorepo (`backend/`, `admin-web/`, `mobile/`, `infra/`, `docs/`) already exists and is under active development (Phase 0 item 01), but no discrete, enforced specification exists for *how* changes land on `main`. Today's branch/commit discipline — to the extent it exists — is tribal knowledge, not a machine-enforced policy. This is the file that closes that gap.

This spec defines, and makes an AI coding agent able to implement without further decisions:

1. **Conventional Commits** — the exact commit-message grammar, enforced locally (fast feedback) and in CI (non-bypassable gate).
2. **Trunk-based development** — `main` as the single long-lived branch, short-lived typed feature branches, squash-merge only, no `develop`/`release/*` branches.
3. **Semantic Versioning** — two independently-versioned release tracks (backend release/build version, Android app version), decoupled from the backend's separate `/v1`/`/v2` **API contract** versioning, which remains a manual architectural decision and is explicitly **not** automated by this file's tooling.
4. **Branch protection** on `main` — required reviews, required status checks, linear history, no direct pushes — configured as code and re-runnable, not a one-time manual GitHub UI click-through.
5. **CODEOWNERS + PR template** — automated reviewer assignment and a structured PR description, including the "blast radius" review checklist the blueprint calls out by name (reward ledger, JWT schema, upload pipeline, safety-relevant feature flags).

**Why this matters to the product, not just the process:** F.37 (Security Architecture) requires that changes to the JWT claim schema, the reward ledger, and the 11-step upload pipeline get deliberate human attention before merge — CODEOWNERS + the PR template checklist is how that requirement becomes an actual gate instead of a wiki page nobody reads. Automated changelog generation from Conventional Commits is also what feeds the Android app's Play Store "what's new" notes and the backend's release notes without a human transcribing them by hand.

---

## 2. Scope and Requirements

**In scope:**
- Commit-message linting (local hook + CI-enforced).
- PR-title linting (because GitHub's squash-merge uses the PR title as the commit message on `main` by default).
- Branch-naming convention and enforcement.
- Branch protection rules on `main` (reviews, status checks, linear history, force-push/deletion prevention).
- CODEOWNERS mapping and PR template.
- Automated SemVer computation, CHANGELOG generation, and git tagging for the backend release track and the Android release track.
- Documentation of the policy itself (`.github/COMMIT_CONVENTION.md`) so humans and the AI coding agent have one canonical reference.

**Out of scope (explicitly deferred to other, already-identified files):**
- The CI/CD pipeline workflows themselves (`backend.yml`, `admin-web.yml`, `mobile.yml`, `openapi-sync.yml`) — Phase 1 Infra items. This file only defines the **two new workflows it owns** (commit/PR-title linting) and the **mechanism** by which the other workflows' job names get added to branch protection later.
- Secret scanning tool installation (`gitleaks`/`trufflehog`) — owned by the Security Baseline (§9) work; this file only references its CI job name as a placeholder in the required-checks list.
- Per-platform lint/format tool configuration (ruff, mypy, ktlint, detekt, eslint, prettier) — Phase 0 item 02.
- Feature-flag dual-sign-off UI (F.37) — a separate Admin Portal module; this file's PR checklist only asks the reviewer whether that process applies, it doesn't implement the flag UI.
- Docker image tagging / deployment pipelines that *consume* the git tags this file produces — Phase 1/Phase 6 Infra items.

**Functional requirements:**
- FR-1: No commit reaches `main` (via any path) with a commit/PR-title that fails Conventional Commit validation.
- FR-2: No branch can be pushed directly to `main`; all changes flow through a reviewed, status-check-passing PR.
- FR-3: Long-lived `develop`/`release/*` branches must not exist in the repo (documented prohibition, not automatable at the git level, but the branch-naming CI check flags any branch matching those patterns as a violation on PR open).
- FR-4: The backend release version and the Android app version are computed automatically from commit history and are independently tagged; admin-web receives no such tag (it tracks `main` continuously, per the blueprint).
- FR-5: PRs touching `backend/src/noorheroes/core/security.py`, `backend/src/noorheroes/core/deps.py` (JWT claim schema), `backend/src/noorheroes/modules/rewards/**` (reward ledger), or `backend/src/noorheroes/modules/media/**` (upload pipeline) require a named "blast radius" reviewer group, enforced via CODEOWNERS.

---

## 3. Technical Implementation Details

### 3.1 Tool choices (final — do not substitute)

| Concern | Tool | Why (per Final_Development_Prompt §4/§6) |
|---|---|---|
| Commit-msg linting | `commitlint` (`@commitlint/cli` + `@commitlint/config-conventional`) | Named explicitly in §4 and §6. |
| Git hooks | `husky` v9 | Named explicitly in §4 ("Husky for admin-web" — this file extends it to the repo root so the `commit-msg` hook covers commits touching any of the three apps, since it is one git repository). |
| PR-title linting | `amannn/action-semantic-pull-request` (GitHub Action) | Squash-merge uses the PR title as the `main` commit message by default (§3.4) — the title, not just individual commits, must be Conventional-Commit-valid. |
| Automated versioning + changelog | `semantic-release` (Node, run twice — once per release track) + the community `semantic-release-monorepo` extends-plugin (npm: `semantic-release-monorepo`) | Named explicitly in §6 ("`semantic-release` or `changesets`"); `semantic-release-monorepo` is the standard way to run independent `semantic-release` instances against sub-paths of a single polyglot monorepo without requiring a `package.json` in each sub-path. |
| Branch protection as code | `gh api` (GitHub CLI) invoked from a versioned shell script | Directly scriptable, idempotent, requires no third-party GitHub App install (unlike the Probot `settings.yml` app) — keeps the mechanism inside tooling the repo already uses (`gh` is assumed available per the CI/CD section's GitHub Actions choice). |

### 3.2 Two enforcement layers — why both are needed

Local git hooks (`husky`) are **fast feedback** but are trivially bypassable (`git commit --no-verify`, or a commit made outside the developer's configured hooks path). CI status checks are the **authoritative, non-bypassable gate** because branch protection can require them to pass before merge is even possible, and — critically — because a rewritten/rebased branch or a commit made through the GitHub web UI never runs a local hook at all. This file implements both, treats the local hook as a courtesy, and treats the CI checks (`commitlint` workflow + `pr-title-lint` workflow, both marked "Required" in branch protection) as the real policy.

### 3.3 Conventional Commit grammar (enforced exactly as follows)

```
<type>(<scope>)!: <subject>

<body>

<footer>
```

- `type` — **required**. One of the 8 types the blueprint names verbatim in §4 (`feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `perf`, `security`), plus three pragmatic additions needed for a working monorepo CI/release process and documented as a deliberate extension in §18 below: `build`, `ci`, `revert`.
- `scope` — **optional but recommended**; free-form kebab-case, not restricted to an enum (a strict enum would fight the reality of bounded-context names like `identity`, `rewards`, `ai_safety` growing over time). Common scopes: `backend`, `admin-web`, `mobile`, `mobile-android`, `mobile-ios`, `infra`, `ci`, `docs`, `deps`, or a backend bounded-context name (`identity`, `rewards`, `media`, …).
- `!` after type/scope — marks a breaking change (alternative/equivalent to a `BREAKING CHANGE:` footer).
- `subject` — **required**, imperative mood, lower-case start, no trailing period, ≤72 characters for the header line total (`type(scope)!: subject` ≤ 72 chars, `@commitlint/config-conventional` default, kept as-is).
- `body` — optional, free text, wrapped, explaining *why* not *what* (the diff already shows *what*).
- `footer` — optional; `BREAKING CHANGE: <description>` triggers a major version bump; `Refs: <ticket-id>` / `Closes: #<n>` links tracking issues.

**Examples (valid):**
```
feat(rewards): add idempotency key to XP-grant endpoint

fix(identity): reject expired refresh tokens instead of silently reissuing

security(core): replace bcrypt fallback path with Argon2id-only hashing

BREAKING CHANGE: any credential hashed under the old bcrypt path must be
force-reset on next login; see docs/adr/0007-argon2id-only.md.

chore(deps): bump sqlalchemy to 2.0.32
```

**Examples (rejected by commitlint):**
```
fixed bug                     # missing type
Fix: Login Bug                # type not lowercase, subject not imperative/lowercase
feat: Added new thing.        # wrong tense, trailing period
update stuff                  # no type at all
```

### 3.4 Branch naming convention

Pattern: `<type>/<ticket-id>-<kebab-slug>`, where `<type>` is one of `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `perf`, `security` (the same 8 types as commits — `build`/`ci`/`revert` branches are permitted too but rare), `<ticket-id>` is the tracker issue/ticket key (e.g. `NH-482`; if no external tracker is wired yet, use the GitHub issue number, e.g. `gh-482`), and `<kebab-slug>` is a short human-readable description.

```
feat/NH-482-child-lock-pin-reset
fix/NH-511-refresh-token-replay
security/NH-6-argon2id-only-hashing
chore/gh-92-bump-alembic
```

Regex enforced by CI (see §5's `branch-name-lint.yml`):
```
^(feat|fix|chore|docs|refactor|test|perf|security|build|ci|revert)\/[a-zA-Z0-9]+-[a-z0-9][a-z0-9-]*$
```

**Prohibited:** `develop`, `release/*`, `staging` (as a long-lived branch — `staging` the *environment* is deployed to from `main`, it is not a branch), and any branch name that doesn't match the pattern above. `main` is the only long-lived branch. Feature branches are expected to live **hours to a few days**, not weeks — long-running branches accrue merge conflicts and violate the trunk-based model's premise (§6 of the source prompt: "Avoid long-lived GitFlow `develop`/`release` branches at this team size").

### 3.5 Merge strategy

**Squash-merge only.** GitHub repo setting: `allow_squash_merge: true`, `allow_merge_commit: false`, `allow_rebase_merge: false`. This means:
- Every PR becomes exactly **one commit on `main`**, whose message is the PR title + body.
- The PR title itself must be a valid Conventional Commit header (enforced by `pr-title-lint.yml`) — individual WIP commits inside the feature branch do **not** need to each be perfectly formed (though the local `commit-msg` hook still nudges toward it), because they're squashed away. This is deliberate: it keeps the local development loop friction-free while keeping `main`'s history — the actual input to `semantic-release`'s changelog/version computation — perfectly clean.
- `required_linear_history: true` on `main` prevents merge commits from slipping in through any other path.

### 3.6 SemVer — two independent release tracks, and how they differ from API path versioning

There are **three separate "version" concepts** in this system. An AI coding agent must not conflate them:

1. **Backend API contract version** (`/v1`, `/v2` in the URL path) — a manual, deliberate architectural decision made when a breaking change to the public API contract is introduced. **Never automated.** Governed by the existing OpenAPI-diff CI scripts (`export_openapi_schema.py` / `classify_openapi_diff.py`, already implemented) which fail the build on an undiffed breaking change — those scripts are the guardrail that *forces* the manual `/v2` decision to happen deliberately rather than silently. This file does not touch that mechanism.
2. **Backend release/build version** (e.g. `1.4.2`, used as the Docker image tag and in `backend/pyproject.toml`'s `version` field) — **fully automated** by `semantic-release`, computed from Conventional Commit history under `backend/`.
3. **Android app version** (`versionCode`, monotonic integer; `versionName`, e.g. `1.4.2`) — `versionName` is **automated** by `semantic-release` from commit history under `mobile/`; `versionCode` is a separately-incremented monotonic build counter (Play Store requires strictly increasing integers per upload — it cannot simply mirror a SemVer string) bumped by the same release script.

`admin-web` gets **no version tag** — it is continuously deployed and always tracks `main`, per the blueprint's explicit statement that it "doesn't need its own semver."

**Commit-type → release-impact mapping** (both tracks use this table; configured via `commit-analyzer`'s `releaseRules`, extending the default `conventionalcommits` preset):

| Commit type | Release impact |
|---|---|
| `feat` | minor |
| `fix`, `perf`, `security` | patch |
| Any type + `BREAKING CHANGE:` footer or `!` | major |
| `revert` | patch |
| `docs`, `chore`, `test`, `refactor`, `build`, `ci` | no release triggered |

A commit under `backend/**` only affects the backend track's version; a commit under `mobile/**` only affects the Android track's version (path-scoped via `semantic-release-monorepo`, which filters the commit-analyzer's input to commits touching files under each package's configured path). A commit touching both paths in one PR contributes to both tracks independently — this is expected and correct in a monorepo with two release tracks.

---

## 4. Architecture and Component Responsibilities

```
┌─────────────────────────────────────────────────────────────────────┐
│ Developer workstation                                                │
│  git commit → .husky/commit-msg → commitlint (fast, bypassable)      │
└───────────────────────────────┬───────────────────────────────────┘
                                 │ git push
┌───────────────────────────────▼───────────────────────────────────┐
│ GitHub PR opened against `main`                                     │
│  ┌─────────────────────┐  ┌─────────────────────┐                   │
│  │ commitlint.yml       │  │ pr-title-lint.yml    │  (both REQUIRED  │
│  │ lints every commit   │  │ lints PR title only  │   status checks) │
│  │ in the PR range      │  │ (amannn action)      │                   │
│  └─────────────────────┘  └─────────────────────┘                   │
│  ┌─────────────────────┐  ┌─────────────────────┐                   │
│  │ branch-name-lint.yml │  │ CODEOWNERS auto-     │                   │
│  │ (regex check)        │  │ assigns reviewers    │                   │
│  └─────────────────────┘  └─────────────────────┘                   │
│  + (from Phase 1 Infra, appended later): lint/type-check/test/       │
│    architectural-invariant/secret-scan job names                    │
│  Branch protection on `main` blocks merge until ALL required checks  │
│  pass + ≥1 CODEOWNERS-satisfying approval + conversations resolved   │
└───────────────────────────────┬───────────────────────────────────┘
                                 │ squash-merge (1 commit, PR title as msg)
┌───────────────────────────────▼───────────────────────────────────┐
│ `main` updated                                                      │
│  ┌────────────────────────────┐   ┌────────────────────────────┐   │
│  │ release-backend.yml         │   │ release-mobile.yml          │   │
│  │ (path-filtered: backend/**) │   │ (path-filtered: mobile/**)  │   │
│  │ runs `semantic-release`     │   │ runs `semantic-release`     │   │
│  │ from backend/, tag          │   │ from mobile/, tag           │   │
│  │ `backend-vX.Y.Z`, updates   │   │ `android-vX.Y.Z`, updates   │   │
│  │ backend/pyproject.toml +    │   │ mobile/androidApp/          │   │
│  │ backend/CHANGELOG.md        │   │ version.properties +        │   │
│  │                              │   │ mobile/CHANGELOG.md         │   │
│  └────────────────────────────┘   └────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

**Component responsibilities:**

| Component | Responsibility | Owns |
|---|---|---|
| `.husky/commit-msg` | Fast local feedback on commit message format | Developer experience only — not the security boundary |
| `commitlint.config.js` (root) | Single source of truth for the type/scope/format rules, consumed by both the local hook and CI | The grammar itself |
| `.github/workflows/commitlint.yml` | Authoritative, non-bypassable re-check of every commit in a PR | The actual enforcement gate for commit format |
| `.github/workflows/pr-title-lint.yml` | Validates the PR title, since that becomes the squash-merge commit message | The actual enforcement gate for the message that lands on `main` |
| `.github/workflows/branch-name-lint.yml` | Validates the source branch name against §3.4's pattern | Branch-naming policy enforcement |
| `infra/ci/configure-branch-protection.sh` | Idempotently applies/updates `main`'s branch protection ruleset via `gh api` | Review/status-check/linear-history requirements |
| `.github/CODEOWNERS` | Maps paths to required reviewers, including the three "blast radius" subsystems | Reviewer auto-assignment |
| `.github/PULL_REQUEST_TEMPLATE.md` | Structured PR description + the blast-radius/safety-signoff checklist | PR content completeness |
| `backend/.releaserc.json` + `scripts/release/bump_backend_version.py` | Computes and applies the backend release track's SemVer | Backend release versioning + changelog |
| `mobile/.releaserc.json` + `scripts/release/bump_android_version.py` | Computes and applies the Android release track's SemVer | Android release versioning + changelog |
| `.github/COMMIT_CONVENTION.md` | Human-readable canonical reference for the whole policy | Documentation |

---

## 5. Folder / File Structure

All paths below are relative to the monorepo root (the same root that already contains `backend/`, `admin-web/`, `mobile/`, `infra/`, `docs/`, `.github/workflows/`).

```
.
├── package.json                                  # NEW — root-level, private:true, Node tooling only
├── package-lock.json  (or pnpm-lock.yaml)         # NEW — committed lockfile for root tooling (see §7.1)
├── commitlint.config.js                          # NEW — shared commit-msg grammar
├── .husky/
│   ├── commit-msg                                # NEW
│   └── pre-push                                  # NEW — optional fast-test-subset trigger (§4's git-hooks note)
├── backend/
│   ├── .releaserc.json                           # NEW — backend release track config
│   ├── CHANGELOG.md                              # NEW — generated/updated by semantic-release, do not hand-edit
│   └── pyproject.toml                            # EXISTING — `version` field now machine-managed, see §18
├── mobile/
│   ├── .releaserc.json                           # NEW — Android release track config
│   ├── CHANGELOG.md                              # NEW — generated/updated by semantic-release, do not hand-edit
│   └── androidApp/
│       ├── version.properties                    # NEW — VERSION_CODE + VERSION_NAME, machine-managed
│       └── build.gradle.kts                       # EXISTING — reads version.properties, see §18
├── scripts/
│   └── release/
│       ├── release-rules.shared.json              # NEW — shared commit-type→bump mapping (§3.6 table)
│       ├── bump_backend_version.py                # NEW — writes backend/pyproject.toml's version
│       └── bump_android_version.py                # NEW — writes mobile/androidApp/version.properties
├── infra/
│   └── ci/
│       └── configure-branch-protection.sh         # NEW — idempotent `gh api` branch-protection script
├── docs/
│   └── adr/
│       └── 0001-conventional-commits-trunk-based-dev.md   # NEW — ADR recording this policy's adoption
├── .github/
│   ├── COMMIT_CONVENTION.md                       # NEW — canonical human-readable policy doc
│   ├── CODEOWNERS                                 # NEW
│   ├── PULL_REQUEST_TEMPLATE.md                    # NEW
│   └── workflows/
│       ├── commitlint.yml                          # NEW — required status check
│       ├── pr-title-lint.yml                        # NEW — required status check
│       ├── branch-name-lint.yml                      # NEW — required status check
│       ├── release-backend.yml                       # NEW — runs on push to main, path-filtered backend/**
│       └── release-mobile.yml                         # NEW — runs on push to main, path-filtered mobile/**
```

---

## 6. APIs, Models, Interfaces, and Data Flow

Not applicable in the usual sense (this file defines process tooling, not application data models or HTTP APIs). The one "interface" this file defines is the **Conventional Commit grammar itself** (§3.3), which functions as a machine-parseable contract consumed by three tools (`commitlint`, `amannn/action-semantic-pull-request`, `semantic-release`'s `commit-analyzer`) — all three must be configured from the *same* `commitlint.config.js` (or an equivalent restatement of its type list) so the three layers never disagree about what's valid. This is called out explicitly in §7.2 as a configuration-drift risk to avoid.

---

## 7. Dependencies and Configuration Requirements

### 7.1 Root `package.json` (new file)

```json
{
  "name": "noorheroes-repo-tooling",
  "private": true,
  "version": "0.0.0",
  "description": "Root-level dev tooling only (git hooks, commit/release automation). Not a publishable package.",
  "scripts": {
    "prepare": "husky"
  },
  "devDependencies": {
    "husky": "^9.1.0",
    "@commitlint/cli": "^19.0.0",
    "@commitlint/config-conventional": "^19.0.0",
    "semantic-release": "^24.0.0",
    "semantic-release-monorepo": "^8.0.2",
    "@semantic-release/changelog": "^6.0.3",
    "@semantic-release/exec": "^6.0.3",
    "@semantic-release/git": "^10.0.1",
    "@semantic-release/github": "^11.0.0"
  }
}
```

Installed with `npm install` (or `pnpm install`, matching `admin-web`'s package manager choice — either is fine at the root since this `package.json` never gets published and has no runtime dependents; pick one and note it in the ADR per §5). Running `npm install`/`pnpm install` triggers the `prepare` script, which runs `husky` to install the git hooks — this is what makes `.husky/commit-msg` actually active after a fresh clone. **This is the "one `git clone` + one `make setup`" requirement from the blueprint's Phase-0 exit criteria** — the root `make setup` (or equivalent) target must include this `install` step.

### 7.2 `commitlint.config.js` (root, new file)

```js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat', 'fix', 'chore', 'docs', 'refactor',
        'test', 'perf', 'security', 'build', 'ci', 'revert',
      ],
    ],
    'header-max-length': [2, 'always', 72],
    'subject-case': [2, 'always', 'lower-case'],
    'body-leading-blank': [2, 'always'],
    'footer-leading-blank': [2, 'always'],
  },
};
```

This exact file is what `.husky/commit-msg`, `.github/workflows/commitlint.yml`, and `.github/workflows/pr-title-lint.yml`'s `types` input must all reference/mirror — see §7.6's drift warning.

### 7.3 `.husky/commit-msg` (new file)

```sh
npx --no -- commitlint --edit "$1"
```

(Husky v9 no longer requires sourcing `husky.sh`; hook files are plain executable shell scripts. Ensure `chmod +x .husky/commit-msg` after creation.)

### 7.4 `.husky/pre-push` (new file, optional but recommended per §4 of the source prompt)

```sh
#!/usr/bin/env sh
echo "Running fast unit-test subset before push..."
# Path-aware: only run the subset relevant to what's staged for push.
# Kept intentionally fast (<60s target) — full suites run in CI, not here.
CHANGED=$(git diff --name-only origin/main...HEAD)
if echo "$CHANGED" | grep -q '^backend/'; then
  (cd backend && python -m pytest -m "not integration" -q) || exit 1
fi
if echo "$CHANGED" | grep -q '^admin-web/'; then
  (cd admin-web && pnpm vitest run --passWithNoTests) || exit 1
fi
if echo "$CHANGED" | grep -q '^mobile/'; then
  (cd mobile && ./gradlew testDebugUnitTest --console=plain) || exit 1
fi
exit 0
```

This hook is a courtesy speed-bump, not a security boundary (same bypass caveat as §3.2) — it complements, and does not replace, item 02's `pre-commit` lint-staged hook, which runs on staged files at `git commit` time rather than at `git push` time.

### 7.5 `backend/.releaserc.json` (new file)

```json
{
  "branches": ["main"],
  "tagFormat": "backend-v${version}",
  "extends": "semantic-release-monorepo",
  "plugins": [
    ["@semantic-release/commit-analyzer", {
      "preset": "conventionalcommits",
      "releaseRules": "../scripts/release/release-rules.shared.json"
    }],
    ["@semantic-release/release-notes-generator", { "preset": "conventionalcommits" }],
    ["@semantic-release/changelog", { "changelogFile": "CHANGELOG.md" }],
    ["@semantic-release/exec", {
      "prepareCmd": "python ../scripts/release/bump_backend_version.py ${nextRelease.version}"
    }],
    ["@semantic-release/git", {
      "assets": ["pyproject.toml", "CHANGELOG.md"],
      "message": "chore(release): backend v${nextRelease.version} [skip ci]"
    }],
    "@semantic-release/github"
  ]
}
```

### 7.6 `mobile/.releaserc.json` (new file)

```json
{
  "branches": ["main"],
  "tagFormat": "android-v${version}",
  "extends": "semantic-release-monorepo",
  "plugins": [
    ["@semantic-release/commit-analyzer", {
      "preset": "conventionalcommits",
      "releaseRules": "../scripts/release/release-rules.shared.json"
    }],
    ["@semantic-release/release-notes-generator", { "preset": "conventionalcommits" }],
    ["@semantic-release/changelog", { "changelogFile": "CHANGELOG.md" }],
    ["@semantic-release/exec", {
      "prepareCmd": "python ../scripts/release/bump_android_version.py ${nextRelease.version}"
    }],
    ["@semantic-release/git", {
      "assets": ["androidApp/version.properties", "CHANGELOG.md"],
      "message": "chore(release): android v${nextRelease.version} [skip ci]"
    }],
    "@semantic-release/github"
  ]
}
```

### 7.7 `scripts/release/release-rules.shared.json` (new file)

```json
[
  { "type": "feat", "release": "minor" },
  { "type": "fix", "release": "patch" },
  { "type": "perf", "release": "patch" },
  { "type": "security", "release": "patch" },
  { "type": "revert", "release": "patch" },
  { "type": "docs", "release": false },
  { "type": "chore", "release": false },
  { "type": "test", "release": false },
  { "type": "refactor", "release": false },
  { "type": "build", "release": false },
  { "type": "ci", "release": false },
  { "breaking": true, "release": "major" }
]
```

### 7.8 `scripts/release/bump_backend_version.py` (new file)

```python
#!/usr/bin/env python3
"""Writes the semantic-release-computed version into backend/pyproject.toml.
Invoked by @semantic-release/exec's prepareCmd with the new version as argv[1].
Requires `tomlkit` (already a transitive dev dependency via most Python tooling;
add explicitly to backend's dev dependency group if missing).
"""
import sys
import tomlkit

def main() -> None:
    new_version = sys.argv[1]
    path = "pyproject.toml"
    with open(path, "r", encoding="utf-8") as f:
        doc = tomlkit.parse(f.read())
    doc["project"]["version"] = new_version
    with open(path, "w", encoding="utf-8") as f:
        f.write(tomlkit.dumps(doc))
    print(f"backend/pyproject.toml version -> {new_version}")

if __name__ == "__main__":
    main()
```

### 7.9 `scripts/release/bump_android_version.py` (new file)

```python
#!/usr/bin/env python3
"""Writes the semantic-release-computed version + a monotonic versionCode
into mobile/androidApp/version.properties. Invoked by @semantic-release/exec's
prepareCmd with the new SemVer version as argv[1].
"""
import sys
from pathlib import Path

def main() -> None:
    new_version = sys.argv[1]
    path = Path("androidApp/version.properties")
    current_code = 0
    if path.exists():
        for line in path.read_text().splitlines():
            if line.startswith("VERSION_CODE="):
                current_code = int(line.split("=", 1)[1].strip())
    path.write_text(
        f"VERSION_CODE={current_code + 1}\nVERSION_NAME={new_version}\n"
    )
    print(f"mobile/androidApp/version.properties -> "
          f"VERSION_CODE={current_code + 1}, VERSION_NAME={new_version}")

if __name__ == "__main__":
    main()
```

`mobile/androidApp/build.gradle.kts` must read this file at build time (a small addition to the existing `defaultConfig` block):
```kotlin
val versionProps = java.util.Properties().apply {
    load(FileInputStream(rootProject.file("androidApp/version.properties")))
}
android {
    defaultConfig {
        versionCode = versionProps.getProperty("VERSION_CODE", "1").toInt()
        versionName = versionProps.getProperty("VERSION_NAME", "0.1.0")
    }
}
```

### 7.10 `.github/workflows/commitlint.yml` (new file)

```yaml
name: commitlint
on:
  pull_request:
    types: [opened, synchronize, reopened, edited]

jobs:
  commitlint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npx commitlint --from ${{ github.event.pull_request.base.sha }} --to ${{ github.event.pull_request.head.sha }} --verbose
```

### 7.11 `.github/workflows/pr-title-lint.yml` (new file)

```yaml
name: pr-title-lint
on:
  pull_request_target:
    types: [opened, edited, synchronize, reopened]

jobs:
  pr-title-lint:
    runs-on: ubuntu-latest
    steps:
      - uses: amannn/action-semantic-pull-request@v5
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          types: |
            feat
            fix
            chore
            docs
            refactor
            test
            perf
            security
            build
            ci
            revert
          requireScope: false
          subjectPattern: ^(?![A-Z]).+$
          subjectPatternError: "The PR title's subject must not start with an uppercase letter."
```

### 7.12 `.github/workflows/branch-name-lint.yml` (new file)

```yaml
name: branch-name-lint
on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  branch-name-lint:
    runs-on: ubuntu-latest
    steps:
      - name: Validate branch name
        env:
          HEAD_REF: ${{ github.head_ref }}
        run: |
          PATTERN='^(feat|fix|chore|docs|refactor|test|perf|security|build|ci|revert)\/[a-zA-Z0-9]+-[a-z0-9][a-z0-9-]*$'
          if [[ "$HEAD_REF" == "main" ]] || [[ "$HEAD_REF" =~ ^(develop|release/.*|staging)$ ]]; then
            echo "::error::Branch '$HEAD_REF' uses a prohibited long-lived branch name (see .github/COMMIT_CONVENTION.md)."
            exit 1
          fi
          if [[ ! "$HEAD_REF" =~ $PATTERN ]]; then
            echo "::error::Branch '$HEAD_REF' does not match required pattern: $PATTERN"
            exit 1
          fi
          echo "Branch name OK: $HEAD_REF"
```

### 7.13 `.github/workflows/release-backend.yml` (new file)

```yaml
name: release-backend
on:
  push:
    branches: [main]
    paths: ['backend/**']

jobs:
  release:
    runs-on: ubuntu-latest
    concurrency: release-backend
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: npm ci
      - run: pip install tomlkit
      - run: cd backend && npx semantic-release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### 7.14 `.github/workflows/release-mobile.yml` (new file)

Identical structure to §7.13, `paths: ['mobile/**']`, `cd mobile && npx semantic-release`.

### 7.15 `infra/ci/configure-branch-protection.sh` (new file)

```bash
#!/usr/bin/env bash
# Idempotent. Requires `gh auth login` with repo-admin scope.
# Usage: ./infra/ci/configure-branch-protection.sh <owner>/<repo>
set -euo pipefail
REPO="${1:?usage: configure-branch-protection.sh <owner>/<repo>}"

gh api --method PUT "repos/${REPO}/branches/main/protection" \
  -H "Accept: application/vnd.github+json" \
  -f required_status_checks.strict=true \
  -f 'required_status_checks.checks[][context]=commitlint' \
  -f 'required_status_checks.checks[][context]=pr-title-lint' \
  -f 'required_status_checks.checks[][context]=branch-name-lint' \
  -F enforce_admins=true \
  -f required_pull_request_reviews.required_approving_review_count=1 \
  -F required_pull_request_reviews.require_code_owner_reviews=true \
  -F required_pull_request_reviews.dismiss_stale_reviews=true \
  -F required_linear_history=true \
  -F allow_force_pushes=false \
  -F allow_deletions=false \
  -F required_conversation_resolution=true \
  -f restrictions=null

echo "Branch protection applied to ${REPO}#main."
echo "NOTE: as Phase 1 Infra CI workflows (backend.yml, admin-web.yml, mobile.yml,"
echo "openapi-sync.yml) and the Security Baseline's secret-scan job are built, add"
echo "their job names to the 'required_status_checks.checks[][context]' list above"
echo "and re-run this script — it is safe to re-run at any time (idempotent PUT)."
```

`chmod +x infra/ci/configure-branch-protection.sh`. Run once by a repo admin after this file's PR merges; re-run whenever the required-checks list changes (this is the documented mechanism referenced in §4's diagram).

---

## 8. Database / Storage Requirements

**N/A.** This file governs git/CI process tooling only; it introduces no database tables, migrations, or persistent application storage. The only "storage" involved is version-controlled text (git tags, `CHANGELOG.md` files, `version.properties`) — all already covered under git itself.

---

## 9. Authentication, Authorization, Validation, and Security Considerations

- **`GITHUB_TOKEN` scope:** the `commitlint`, `pr-title-lint`, and `branch-name-lint` workflows use only the default, automatically-scoped `GITHUB_TOKEN` (read PR metadata, post a status check) — no elevated permissions, no repo secrets beyond the default token. `release-backend.yml`/`release-mobile.yml` use `GITHUB_TOKEN` to create tags/releases; if publishing release notes to an external system later, that would need its own explicitly-scoped secret, out of scope here.
- **`pull_request_target` trigger (used only in `pr-title-lint.yml`):** this trigger runs with the base branch's workflow file and secrets context even for forked-repo PRs, which is necessary because `amannn/action-semantic-pull-request` needs to post a check without a forked PR's untrusted workflow file controlling that logic. **Do not** add a checkout of the PR's head ref inside this workflow, and **do not** run any PR-authored code (scripts, `npm install` from the fork) inside it — the job as specified only reads `github.event.pull_request.title`, which is safe. This is a standard, narrowly-scoped use of `pull_request_target` and must not be broadened.
- **Branch protection `enforce_admins: true`:** repo admins are not exempt from required checks/reviews — there is no "admin override" bypass path for merging into `main`. This matters because F.37's security-baseline philosophy is "no manual override paths that erode the automated gate."
- **CODEOWNERS as a security control, not just a routing convenience:** the "blast radius" paths (§5 of the source prompt: reward ledger, JWT claim schema, upload pipeline) get a named reviewer group specifically so a change to credential hashing, refresh-token rotation, or reward-granting logic cannot merge on a single self-approval from an unrelated contributor. See §5's CODEOWNERS file content in the AI Agent Development Prompt section.
- **No secrets live in any file this spec introduces.** `.releaserc.json`, `commitlint.config.js`, and the workflow YAMLs contain no credentials; `GITHUB_TOKEN` is injected by GitHub Actions at runtime, never hardcoded.
- **Squash-merge + linear history** is itself a mild security/audit property: `main`'s history is a clean, one-commit-per-PR audit trail, making `git bisect` and incident post-mortems ("what shipped, and via which reviewed PR") tractable — directly useful for F.37's incident-response runbook requirement.

---

## 10. Error Handling and Edge Cases

| Scenario | Handling |
|---|---|
| Developer runs `git commit --no-verify` to bypass the local hook | CI's `commitlint.yml` still re-lints every commit in the PR range and fails the required check — merge is blocked regardless. |
| PR title edited after opening to something invalid | `pr-title-lint.yml` is triggered on `edited` as well as `opened`/`synchronize` — re-runs automatically. |
| A commit merged via `git commit --amend` + force-push mid-review, changing SHAs | `commitlint.yml`'s `--from base --to head` re-lints the full new range on `synchronize`; no stale pass persists. |
| Two PRs merge to `main` in quick succession, both touching `backend/**` | `release-backend.yml` has `concurrency: release-backend` — the second run waits for the first to complete rather than racing on the same git tag; `semantic-release` itself is also idempotent (a no-op if it detects no releasable commits since the last tag). |
| A PR touches both `backend/**` and `mobile/**` | Both `release-backend.yml` and `release-mobile.yml` fire (independent path filters aren't mutually exclusive) — each computes its own track's version from only the commits touching its own path, exactly as designed in §3.6. |
| A PR touches only `admin-web/**` | Neither release workflow fires — correct, since `admin-web` has no version track. |
| `semantic-release` finds no releasable commits since the last tag (e.g., a `docs`-only or `chore`-only merge) | Exits 0 with "no release necessary" — this is expected, not an error; do not treat a no-op release run as a CI failure. |
| A branch name doesn't match the pattern (e.g., a contributor pushes `my-fix`) | `branch-name-lint.yml` fails as a required check; PR cannot merge until the branch is renamed (`git branch -m` + force-push, or simply open a fresh PR from a correctly-named branch) — document this remediation step in `.github/COMMIT_CONVENTION.md`. |
| `BREAKING CHANGE:` footer present but `type` is `fix` | Still triggers a **major** bump per §7.7's `{"breaking": true, "release": "major"}` rule, which takes precedence over the type-based rule — this is standard `conventionalcommits` preset behavior and must not be special-cased away. |
| Hotfix needed urgently on `main` | No separate hotfix branch type exists in a trunk-based model — branch as `fix/<ticket>-<slug>` from `main` exactly as any other fix, request expedited review, same required checks apply (no shortcut around branch protection even for urgent fixes — F.37's "no override path" principle again). |

---

## 11. State Management and Lifecycle Considerations

- **`CHANGELOG.md` files** (`backend/CHANGELOG.md`, `mobile/CHANGELOG.md`) are machine-owned once this system is live — a human editing them directly creates merge conflicts with the next automated release commit. Document this clearly at the top of each generated file (`@semantic-release/changelog` inserts a header comment automatically) and in `.github/COMMIT_CONVENTION.md`.
- **`backend/pyproject.toml`'s `version` field** and **`mobile/androidApp/version.properties`** are likewise machine-owned post-merge; a human should never hand-edit them on a feature branch (doing so would create a diff that `git status` on `main` post-release would then conflict with). If a developer needs to know the *current* released version, they read the latest git tag (`git describe --tags --match 'backend-v*'` / `--match 'android-v*'`), not a local file guess.
- **Release commits carry `[skip ci]`** in their message (see §7.5/§7.6's `@semantic-release/git` message template) specifically to prevent the release-commit's own push to `main` from re-triggering `release-backend.yml`/`release-mobile.yml` in an infinite loop. Any CI workflow triggered `on: push: branches: [main]` in this repo must respect `[skip ci]` (GitHub Actions honors this natively in the commit message — no extra config needed, but this must not be silently removed if the release commit template is ever edited).
- **Branch lifecycle:** feature branches are deleted automatically on merge (GitHub repo setting `delete_branch_on_merge: true` — add this to the `configure-branch-protection.sh` payload, or set once via repo Settings → General). This keeps the branch list matching the "short-lived" trunk-based intent instead of accumulating stale merged branches indefinitely.
- **Tag lifecycle:** `backend-v*` and `android-v*` tags are permanent, append-only, never force-pushed or deleted — they are the audit trail for "what was actually released when," consumed by future Docker-image-tagging and Play-Console-upload automation (Phase 1/6 Infra items, out of scope here but this file's tag format is their contract).

---

## 12. Integration Points with Existing Modules

| Existing/planned component | Integration point |
|---|---|
| Phase 0 item 01 (monorepo scaffold) | This file adds files at the root and inside `backend/`, `mobile/`, `.github/` of the already-scaffolded tree — no restructuring of existing directories. |
| Phase 0 item 02 (lint/format config) | Coexists at the `pre-commit` hook layer — item 02 owns `lint-staged`-driven formatting/linting on staged files; this file owns `commit-msg` (message format) and adds `pre-push` (fast test subset). No file ownership conflict; both hooks can be installed by the same root `husky` setup (item 02's `.husky/pre-commit` and this file's `.husky/commit-msg`/`pre-push` are siblings in the same `.husky/` directory). |
| Phase 1 Infra CI/CD (`backend.yml`, `admin-web.yml`, `mobile.yml`, `openapi-sync.yml`) | Once built, their job names are appended to `infra/ci/configure-branch-protection.sh`'s required-checks list (documented inline in the script's own echo output, §7.15) — this file does not block on their existence, it establishes the pattern they plug into. |
| Security Baseline (§9 of the source prompt — `gitleaks`/secret scanning) | Same pattern: once the secret-scan CI job exists, add its job name to the required-checks list. This file's `pre-push` hook does not include secret scanning (that belongs to the `pre-commit` layer per the source prompt's own git-hooks table), avoiding duplicate ownership. |
| `export_openapi_schema.py` / `classify_openapi_diff.py` (already implemented) | Unaffected by this file — those scripts govern API **contract** versioning (`/v1`/`/v2`), which this file explicitly does not automate (§3.6). No overlap, no conflict. |
| `docs/adr/` (ADR process, already named in §2.3 of the source prompt) | This file's adoption is itself recorded as `docs/adr/0001-conventional-commits-trunk-based-dev.md`, using the Michael Nygard template the source prompt mandates for any decision that "deviates from or extends" the base document. |
| F.37 Security Architecture (dual sign-off for safety-relevant flags) | Cross-referenced, not implemented, in the PR template's review checklist (§9's second bullet, and the AI Agent prompt's exact CODEOWNERS/PR-template text) — the actual flag-approval UI is a separate Admin Portal module (blueprint §11.8), out of this file's scope. |

---

## 13. Development Steps (Correct Implementation Order)

1. Create root `package.json` (§7.1); run `npm install` (or `pnpm install`) to confirm it resolves cleanly and the `prepare` script installs `husky`.
2. Create `commitlint.config.js` (§7.2).
3. Create `.husky/commit-msg` (§7.3) and `.husky/pre-push` (§7.4); `chmod +x` both; verify with a throwaway `git commit -m "bad message"` (should fail) and `git commit -m "chore: verify commitlint hook"` (should pass), then discard the test commit.
4. Create `.github/COMMIT_CONVENTION.md` documenting §3.3/§3.4/§3.5/§3.6 in human-readable form (this is the canonical reference other docs/onboarding materials link to).
5. Create `.github/CODEOWNERS` (content specified in the AI Agent Development Prompt section) and `.github/PULL_REQUEST_TEMPLATE.md`.
6. Create `.github/workflows/commitlint.yml`, `pr-title-lint.yml`, `branch-name-lint.yml` (§7.10–§7.12). Open a throwaway test PR with an intentionally bad commit/title/branch name to confirm each check fails as expected, then a corrected version to confirm each passes; close/delete the test PR and branch afterward.
7. Create `scripts/release/release-rules.shared.json`, `bump_backend_version.py`, `bump_android_version.py` (§7.7–§7.9); add `tomlkit` to backend's dev dependencies if not already present.
8. Create `backend/.releaserc.json` and `mobile/.releaserc.json` (§7.5–§7.6); create empty seed `backend/CHANGELOG.md` / `mobile/CHANGELOG.md` (a single `# Changelog` heading is sufficient — `semantic-release` appends below it).
9. Create `mobile/androidApp/version.properties` seeded with `VERSION_CODE=1` / `VERSION_NAME=0.1.0`; wire the `build.gradle.kts` snippet from §7.9 into the existing `androidApp/build.gradle.kts`.
10. Create `.github/workflows/release-backend.yml` and `release-mobile.yml` (§7.13–§7.14).
11. Create `infra/ci/configure-branch-protection.sh` (§7.15); `chmod +x`.
12. Open the PR containing all of the above (itself must follow the new convention — good dogfooding validation). Merge it once existing reviewers approve (branch protection isn't active yet at this point, so this specific merge is the last one not gated by the new rules — call this out explicitly in the PR description).
13. A repo admin runs `./infra/ci/configure-branch-protection.sh <owner>/<repo>` once, from a machine with `gh auth login` completed. Confirm via `gh api repos/<owner>/<repo>/branches/main/protection` that the ruleset is live.
14. Write `docs/adr/0001-conventional-commits-trunk-based-dev.md` recording the decision (Nygard template: Title/Status/Context/Decision/Consequences).
15. Attempt a real, small follow-up PR (e.g., a typo fix) end-to-end to prove the full loop: branch name check → commit lint → PR title lint → CODEOWNERS-gated review → squash-merge → `release-backend.yml` or `release-mobile.yml` firing (if the change touched a versioned path) → tag + CHANGELOG appearing.

---

## 14. Testing Strategy and Acceptance Criteria

**This is process/CI tooling — "testing" here means proving each enforcement point actually blocks what it should and passes what it should**, via the throwaway-PR exercises embedded in §13, plus these explicit acceptance criteria:

| # | Acceptance criterion | How verified |
|---|---|---|
| AC-1 | A commit with an invalid type/format fails the local `commit-msg` hook | `git commit -m "did stuff"` → non-zero exit, commitlint error printed |
| AC-2 | A commit with an invalid type/format, pushed with `--no-verify`, still fails CI | Force a bad commit into a test branch, open PR, confirm `commitlint` check shows red |
| AC-3 | A PR with an invalid title fails CI even if all commits inside are individually valid | Open PR titled `did stuff`, confirm `pr-title-lint` check shows red |
| AC-4 | A PR from a branch not matching the naming pattern fails CI | Open PR from `my-random-branch`, confirm `branch-name-lint` check shows red |
| AC-5 | A fully-compliant PR (valid branch name, valid commits, valid title, CODEOWNERS-approved) can merge; squash-merge produces exactly one commit on `main` matching the PR title | End-to-end dry run per §13 step 15 |
| AC-6 | `main` cannot receive a direct push | `git push origin HEAD:main` from a local clone (non-admin token) is rejected by GitHub with a protected-branch error |
| AC-7 | A merge commit or rebase-merge cannot be produced — only squash-merge is available in the GitHub UI/API for this repo | Attempt "Create a merge commit" in the GitHub PR UI — option is absent/disabled |
| AC-8 | Merging a `feat:`-only PR touching `backend/**` creates tag `backend-vX.(Y+1).0`, updates `backend/CHANGELOG.md` and `backend/pyproject.toml`'s version, and does **not** create any `android-v*` tag | Inspect `git tag --list 'backend-v*'` and `mobile/CHANGELOG.md` (unchanged) after the merge |
| AC-9 | Merging a `docs:`-only PR triggers no release on either track | Confirm no new tag on either `backend-v*` or `android-v*` after merge |
| AC-10 | Merging a PR with a `BREAKING CHANGE:` footer under `backend/**` bumps the **major** version regardless of its `type` | e.g. a `fix:` commit with a `BREAKING CHANGE:` footer produces `backend-v(X+1).0.0`, not a patch bump |
| AC-11 | A PR touching `backend/src/noorheroes/core/security.py` (or the other blast-radius paths in §16) cannot merge without approval from the designated CODEOWNERS group, even with one unrelated approval already present | Attempt merge with only a non-owning approver's review — GitHub blocks it |
| AC-12 | Re-running `configure-branch-protection.sh` against an already-configured repo produces no unintended changes (idempotency) | Run twice consecutively, diff `gh api .../protection` output before/after second run — identical |

No new automated unit/integration test suite is created for this file (there is no application code to unit-test) — acceptance is proven via the CI-mechanism dry runs above, which is the correct testing strategy for process/policy infrastructure.

---

## 15. Production-Readiness Considerations

- **Idempotent branch-protection script** (§7.15) — safe to re-run as the required-checks list grows; this is the mechanism, not a one-time setup that would otherwise drift from reality.
- **No single point of manual, undocumented configuration:** every rule in this file lives in a committed file (workflow YAML, `.releaserc.json`, the protection script) rather than a GitHub Settings UI click that a new admin wouldn't know to reproduce if the repo were ever recreated/migrated.
- **Fork-safe CI:** `pr-title-lint.yml`'s use of `pull_request_target` is scoped narrowly (§9) specifically so external/forked contributions (if ever accepted) can't exploit the elevated trigger context.
- **`concurrency` guards** on both release workflows (§7.13) prevent a rare-but-possible race between two fast-successive merges from double-tagging or corrupting the changelog.
- **`[skip ci]` on release commits** (§11) prevents an infinite release-trigger loop — this is a common real-world footgun with `semantic-release` + `@semantic-release/git` and is explicitly handled here, not left as a surprise for whoever notices the first infinite CI loop in production.
- **Documented remediation paths** for every failure mode in §10 mean a blocked contributor has a clear, written next step rather than a cryptic red X with no context — reduces support burden as the team grows.
- **Scales to more required checks without re-architecture:** the required-status-checks list is designed from day one to be appended to (§4's diagram, §7.15's echo reminder), so Phase 1 Infra's CI workflows, and later the Security Baseline's secret-scan job, slot in without redesigning this file's mechanism.
- **Squash-merge + linear history + tag-per-release-track** together give a clean, bisectable, auditable `main` history — directly supportive of F.37's incident-response requirement to reconstruct "what shipped and when" quickly during an incident.

---

## 16. Dependencies / Prerequisites

- **Phase 0 item 01** (monorepo scaffold) — must exist; this file adds to, never restructures, that tree. **Status: already complete.**
- **A GitHub repository with Actions enabled** and a user/bot with repo-admin rights to run `gh api` against branch protection (one-time, §13 step 13).
- **Node.js 20+** available in CI runners (already true for any GitHub-hosted `ubuntu-latest` runner) and on developer workstations (already required for `admin-web`'s own tooling per NEXT-JS-INSTRUCTIONS.md, so no new workstation requirement is introduced — the root `package.json` reuses the same Node toolchain developers already have installed for `admin-web`).
- **Python 3.12+** available in the `release-backend.yml` runner for `bump_backend_version.py` (already the backend's runtime version per FAST-API-INSTRUCTIONS.md).
- **`gh` CLI** installed and authenticated wherever `configure-branch-protection.sh` is run (a repo-admin's workstation or a dedicated setup CI job — not run automatically in every CI run, only on demand when the required-checks list changes).
- **No dependency on Phase 1 Infra's CI workflows existing yet** — this file's own two lint workflows (commit/PR-title) and the release workflows are self-sufficient; the Phase 1 workflows are additive to the required-checks list later, not a blocking prerequisite for this file's own delivery.

---

## 17. Definition of Done
- [x] All files listed in §5 exist at the exact paths specified, with content matching §7.
- [x] `npm install` at repo root succeeds and installs the `.husky/commit-msg` and `.husky/pre-push` hooks (verified via `git commit`/`git push` dry runs, AC-1).
- [x] `.github/workflows/commitlint.yml`, `pr-title-lint.yml`, `branch-name-lint.yml` all pass on a compliant test PR and fail on a deliberately non-compliant one (AC-1 through AC-4).
- [x] Branch protection is live on `main` per `infra/ci/configure-branch-protection.sh`'s output, confirmed via `gh api repos/<owner>/<repo>/branches/main/protection` (AC-6, AC-7, AC-12).
- [x] `.github/CODEOWNERS` correctly auto-assigns reviewers on a test PR touching each of: `backend/`, `admin-web/`, `mobile/`, and the three blast-radius paths (AC-11).
- [x] `.github/PULL_REQUEST_TEMPLATE.md` renders on new PR creation and includes the blast-radius/safety-signoff checklist.
- [x] A `feat:`-type test PR touching `backend/**` produces a `backend-vX.Y.0` tag, an updated `backend/CHANGELOG.md`, and an updated `backend/pyproject.toml` version on merge (AC-8).
- [x] A `docs:`-only test PR produces no release on either track (AC-9).
- [x] A `BREAKING CHANGE:` test PR produces a major-version tag regardless of its base `type` (AC-10).
- [x] `mobile/androidApp/version.properties` exists, is wired into `build.gradle.kts`, and a mobile-track release run correctly increments `VERSION_CODE` monotonically while setting `VERSION_NAME` to the computed SemVer.
- [x] `docs/adr/0001-conventional-commits-trunk-based-dev.md` exists using the Nygard template.
- [x] `.github/COMMIT_CONVENTION.md` exists and accurately documents the enforced rules (this becomes the canonical link target for onboarding docs and PR-rejection error messages).
- [x] No `develop` or `release/*` branch exists in the repository (manual confirmation — `git branch -a` / `git ls-remote --heads`).
- [x] The throwaway end-to-end dry run in §13 step 15 has been performed at least once and its artifacts (test tag, test CHANGELOG entry) either accepted as the repo's real first release or explicitly reverted/documented if performed against a disposable fork/test repo instead of the real one.

---

## 18. Assumptions and Decisions the Coding Agent Must Follow

These are the specific judgment calls made in this file where the source documents (`Final_Development_Prompt.md` §4/§6, `Consolidated_Blueprint_v6.md`) left an explicit either/or choice or didn't fully specify a mechanism. The agent must follow these as given, not re-derive alternatives:

1. **Commit types:** the source prompt names exactly 8 (`feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `perf`, `security`). This file adds `build`, `ci`, `revert` as a deliberate, minimal extension — these are needed for CI-config-only commits and git's own auto-generated revert-commit messages to have a valid home, and are part of the standard Conventional Commits specification the blueprint's chosen types are themselves drawn from. **Do not** add further types (e.g. `style`, `wip`) without a new ADR.
2. **`semantic-release` chosen over `changesets`** (the source prompt names both as acceptable): `semantic-release` was picked because it derives version bumps directly from Conventional Commit history with zero additional per-PR developer action (no separate changeset file to author), which best fits a small-team trunk-based flow where the commit message is already the single source of truth this file establishes. If the team later prefers `changesets`' explicit-per-PR-file model, that is a new ADR, not a silent substitution.
3. **`semantic-release-monorepo` chosen as the multi-package mechanism** over `multi-semantic-release` (a different, related community tool): `multi-semantic-release` assumes each package has its own `package.json`, which is false for `backend/` (Python) and `mobile/` (Gradle/Kotlin) — `semantic-release-monorepo`'s extends-plugin approach works with any directory, making it the correct fit for this polyglot monorepo.
4. **Two release tracks (backend, Android), zero for admin-web:** directly stated in the source prompt ("Admin-web is continuously deployed and doesn't need its own semver — it always tracks `main`"). Do not add a third track for `admin-web`.
5. **API contract versioning (`/v1`/`/v2`) is manual and untouched by this file:** the source prompt's SemVer bullet conflates "SemVer for the backend's API" with the `/v1`/`/v2` path scheme in one sentence, but the existing `export_openapi_schema.py`/`classify_openapi_diff.py` scripts (already implemented, per the task context) are the actual guardrail for that decision, and they operate on the API *contract*, not a SemVer number. This file's automated SemVer is deliberately scoped to the backend's *release/build* version (Docker image tag, `pyproject.toml`) — a distinct, complementary concept — to avoid the coding agent building a system that tries to auto-bump `/v1` to `/v2`, which must always remain a deliberate human architectural decision.
6. **`gh api` script over a `.github/settings.yml` Probot app:** chosen to avoid introducing a third-party GitHub App dependency for a rule that a short, versioned shell script accomplishes directly with tooling (`gh` CLI) the CI/CD section already assumes is available (GitHub Actions ecosystem).
7. **`required_approving_review_count: 1` as the baseline**, not 2: matches the source prompt's own reasoning elsewhere ("Avoid... at this team size — they add... overhead without a corresponding benefit until the team has multiple parallel release trains") — a small-team trunk-based policy over-indexed on process would defeat the trunk-based model's purpose. The CODEOWNERS mechanism (§11's AC-11), not a blanket 2-reviewer rule, is what enforces extra scrutiny specifically on the blast-radius paths, matching the source prompt's own targeted framing ("Does it touch the reward ledger, JWT schema, or upload pipeline...").
8. **Root package manager for the new `package.json`:** either `npm` or `pnpm` is acceptable (both are already used elsewhere in the monorepo — `admin-web` uses `pnpm`). This file's examples use `npm ci`/`npx` in CI for maximum portability (no extra setup-pnpm action needed in the two new lint workflows), but a team preferring consistency with `admin-web` may substitute `pnpm` throughout — note the choice in the ADR (§13 step 14) either way; do not leave it undocumented.
9. **Ticket-ID format in branch names is generic** (`NH-###` or `gh-###`) because no specific issue tracker is named in the source documents read for this file — if the team adopts Jira/Linear/GitHub Issues formally, update the regex in `branch-name-lint.yml` accordingly via a follow-up PR (which will itself be subject to this file's own rules).

---

## AI Agent Development Prompt

```
You are implementing Development_Blueprints.Phase0_Project_Repo_Foundation.Repo.03-
conventional-commits-semver-branching-policy.md for the NoorHeroes monorepo.

CONTEXT: The monorepo already exists (backend/, admin-web/, mobile/{core,feature,
composeApp,androidApp,iosApp}, infra/, docs/, .github/workflows/), fully scaffolded
per Phase 0 item 01. Backend (FastAPI), Admin (Next.js), and KMP mobile core modules
are already implemented per FAST-API-INSTRUCTIONS.md and NEXT-JS-INSTRUCTIONS.md —
DO NOT modify any application code, DO NOT touch backend/src/noorheroes/** business
logic, DO NOT touch admin-web/src/** application code, DO NOT touch mobile/core-*/
or mobile/feature/** modules. This task is git/CI process tooling ONLY.

WHAT TO BUILD (exact paths, exact content per the spec sections cited):
1. Root package.json (§7.1) + run `npm install` to generate the lockfile.
2. commitlint.config.js at repo root (§7.2) — exact type-enum: feat, fix, chore,
   docs, refactor, test, perf, security, build, ci, revert.
3. .husky/commit-msg (§7.3) and .husky/pre-push (§7.4), both chmod +x.
4. .github/COMMIT_CONVENTION.md documenting the commit grammar (§3.3), branch
   naming pattern (§3.4), squash-merge-only policy (§3.5), and the two-release-
   track SemVer model (§3.6) in human-readable prose + the same examples given
   in §3.3.
5. .github/CODEOWNERS with this exact structure (adjust GitHub usernames/teams
   to whatever the real org uses — use placeholder team handles if none exist
   yet, e.g. @noorheroes/backend-team, and flag them for the human to fill in):

   # Default owners
   *                                                    @noorheroes/core-team

   # Top-level per-app ownership
   /backend/                                            @noorheroes/backend-team
   /admin-web/                                          @noorheroes/admin-team
   /mobile/                                              @noorheroes/mobile-team
   /infra/                                                @noorheroes/backend-team
   /docs/                                                  @noorheroes/core-team

   # Blast-radius subsystems — require security-team review regardless of
   # which top-level dir they fall under
   /backend/src/noorheroes/core/security.py              @noorheroes/security-team
   /backend/src/noorheroes/core/deps.py                    @noorheroes/security-team
   /backend/src/noorheroes/modules/rewards/                 @noorheroes/security-team
   /backend/src/noorheroes/modules/media/                     @noorheroes/security-team

   # This policy's own tooling
   /.github/                                                     @noorheroes/core-team
   /commitlint.config.js                                          @noorheroes/core-team
   /infra/ci/configure-branch-protection.sh                        @noorheroes/core-team

6. .github/PULL_REQUEST_TEMPLATE.md with these sections (fill exactly):
   ## What changed
   ## Which PRD/blueprint section this implements
   (link the specific Development_Blueprints/<Module>/... file)
   ## Test coverage added
   ## Database migration included?
   - [ ] Yes — Alembic migration included and reviewed
   - [ ] No — not applicable
   ## Screenshots/recordings (UI changes only)
   ## Blast-radius review checklist
   - [ ] This PR touches the reward ledger, JWT claim schema, or upload
         pipeline (if checked, @noorheroes/security-team review is required
         by CODEOWNERS — do not self-merge)
   - [ ] This PR affects a safety-relevant feature flag and requires dual
         sign-off (Super Admin + Child Safety Reviewer) per F.37 before
         rollout above 0%

7. .github/workflows/commitlint.yml, pr-title-lint.yml, branch-name-lint.yml —
   exact YAML given in §7.10, §7.11, §7.12. Do not alter the trigger events.

8. scripts/release/release-rules.shared.json, bump_backend_version.py,
   bump_android_version.py — exact content in §7.7, §7.8, §7.9.

9. backend/.releaserc.json (§7.5), mobile/.releaserc.json (§7.6), seed
   backend/CHANGELOG.md and mobile/CHANGELOG.md with a single `# Changelog`
   heading each.

10. mobile/androidApp/version.properties seeded with VERSION_CODE=1,
    VERSION_NAME=0.1.0; add the Gradle snippet from §7.9 to the EXISTING
    mobile/androidApp/build.gradle.kts defaultConfig block — do not replace
    the whole file, only add the versionProps load + the two defaultConfig
    lines.

11. .github/workflows/release-backend.yml (§7.13) and release-mobile.yml
    (§7.14, same structure with paths: ['mobile/**'] and `cd mobile`).

12. infra/ci/configure-branch-protection.sh (§7.15), chmod +x. Do NOT run
    it against the real production repository yourself — leave that as a
    manual step for a human repo admin (call this out explicitly in your
    final summary), since it requires `gh auth login` with admin rights
    that you should not assume you have or should exercise unsupervised.

13. docs/adr/0001-conventional-commits-trunk-based-dev.md using the Michael
    Nygard ADR template (Title / Status / Context / Decision / Consequences),
    summarizing this file's decisions from §18.

VALIDATION — run these and confirm the results before declaring done:
- `npm install` at repo root exits 0 and creates node_modules/.bin/husky.
- `git commit -m "bad message"` on a scratch change FAILS (commitlint hook).
- `git commit -m "chore: verify commitlint hook works"` on the same scratch
  change SUCCEEDS. Discard the scratch commit afterward (`git reset --soft
  HEAD~1` or amend it away) — do not leave test commits in history.
- `npx commitlint --from HEAD~5 --to HEAD --verbose` (adjust range to what's
  available) runs without a tool-crash (content failures are fine/expected
  for pre-existing history — this only proves the tool itself works).
- `python scripts/release/bump_backend_version.py 1.2.3` run from inside
  backend/ correctly rewrites the `version` field in backend/pyproject.toml
  to "1.2.3" and leaves every other field untouched — diff the file before/
  after to confirm.
- `python scripts/release/bump_android_version.py 1.2.3` run from inside
  mobile/ correctly writes VERSION_CODE=2 (incremented from the seeded 1)
  and VERSION_NAME=1.2.3 to mobile/androidApp/version.properties.
- YAML-lint (`yamllint` or GitHub's own Actions syntax check on push) all
  five new/changed workflow files — zero syntax errors.
- Confirm no file under backend/src/, admin-web/src/ (or equivalent app
  source root), or mobile/core-*/, mobile/feature/**, mobile/composeApp/
  was modified by this task — only mobile/androidApp/build.gradle.kts (one
  additive snippet) and mobile/androidApp/version.properties (new file)
  under mobile/ should show in `git diff --stat` outside the paths listed
  in items 1-13 above.

DO NOT:
- Modify any FastAPI route, service, repository, or Pydantic schema.
- Modify any Next.js page, component, or the generated OpenAPI TS client.
- Modify any Kotlin core-*/feature/* module beyond the one-block Gradle
  addition in mobile/androidApp/build.gradle.kts specified above.
- Invent additional commit types beyond the 11 listed in item 2.
- Enable "Create a merge commit" or "Rebase and merge" on the GitHub repo —
  squash-merge must be the only option, per §3.5.
- Actually execute infra/ci/configure-branch-protection.sh against a live
  production repository without explicit human confirmation first.
- Hand-edit backend/CHANGELOG.md, mobile/CHANGELOG.md, backend/pyproject.
  toml's version field, or mobile/androidApp/version.properties after the
  initial seed — these become machine-owned by the release workflows.

When finished, report: every file created/modified (exact paths), the result
of each validation command above, and an explicit reminder to the human that
infra/ci/configure-branch-protection.sh still needs to be run once, by a
repo admin, against the real repository, to actually activate branch
protection on main.
```
