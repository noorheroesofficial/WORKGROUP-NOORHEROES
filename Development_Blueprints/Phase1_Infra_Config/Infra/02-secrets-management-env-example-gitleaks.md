# Phase 1 — Secrets Management, `.env.example` Convention & Mandatory Secret Scanning

**Blueprint ID:** `Development_Blueprints.Phase1_Infra_Config.Infra.02-secrets-management-env-example-gitleaks`
**Platform:** Infra (repo-wide: `backend/`, `admin-web/`, `mobile/`, `infra/`, `.github/workflows/`)
**Phase:** Phase 1 — Infrastructure & Configuration
**Depends on:** `Development_Blueprints.Phase1_Infra_Config.Infra.01-environment-tiers-provisioning.md` (defines the five environment tiers — Local, CI, Dev/QA, Staging, Production — this document wires secrets into)
**Source of truth:** `NoorHeroes_Final_Development_Prompt.md` §3.3 (Secrets management), §4 (Git hooks), §6 (CI/CD stage 3 + stage 8), §9 (Security Baseline item 7 — "non-bypassable status check"), §14 (open vendor decision); `NoorHeroes_Consolidated_Blueprint_v6.md` §13.3 / F.37 (managed secret storage with rotation)
**Status:** NEW — this file does not exist in the corpus today; authored to close the gap identified in the Consolidated Execution Blueprint §2 (Phase 1, all 10 items open)

**Do not re-litigate:** backend `pydantic-settings`-based `Settings` (see `FAST-API-INSTRUCTIONS.md` §2's `core/settings.py`) and admin-web's Zod-validated `src/lib/env.ts` (see `noorheroes-admin/NEXT-JS-INSTRUCTIONS.md` §2's Configuration Management row) already exist and already work. This document does not replace either — it (a) defines the `.env.example` convention both must stay in sync with, (b) wires a managed secrets service into Staging/Production so neither file ever reads a real secret from a plaintext `.env` in those tiers, and (c) makes gitleaks + trufflehog secret scanning a mandatory, non-bypassable gate at both commit time and CI time. Every existing `Settings` field name, `Environment` enum value, and Zod schema shape in those two modules is treated as fixed and must not be renamed by this work.

---

## 1. Objective and purpose

Prevent a credential (database password, JWT signing key, R2 access key, AI provider API key, OAuth client secret, push-notification service-account key) from ever reaching a git commit, a CI log, or a container image in plaintext — while giving every developer and every deployment tier a single, predictable place to discover *which* environment variables a given app needs (`*/.env.example`) and *where* the real value for that variable comes from at runtime (a local `.env` file, a CI-injected secret, or a managed secrets service read at boot).

Concretely, this blueprint delivers three things, per Final_Development_Prompt §3.3:

1. **The `.env.example` convention** — one committed, always-current, git-tracked example file per app (`backend/.env.example`, `admin-web/.env.example`, `mobile/local.properties.example`) that is the single checklist of every configuration variable that app's typed config layer (`Settings` / `env.ts` / Gradle `BuildConfig`) requires, with a CI check that fails the build the moment the example file and the typed config layer drift apart.
2. **A secrets-manager wiring strategy** — GCP Secret Manager as the managed secrets service for Dev/QA, Staging, and Production, read at application boot via the platform SDK (never baked into a container image, never passed as a build argument), with an explicit, versioned manifest (`infra/secrets/manifest.yaml`) naming every secret that must exist in each tier.
3. **Mandatory, non-bypassable secret scanning** — gitleaks as a pre-commit hook (blocks a secret from ever being committed) and as a required GitHub Actions status check on every push and pull request (blocks a secret from ever being merged), with trufflehog running a verified-secrets-only pass as a second, independent CI gate. Both are configured as required status checks with "Include administrators" enabled in branch protection, so no role — including a repo admin — can merge past a failed scan.

The purpose is architectural, not procedural: this is Security Baseline item 7 from Final_Development_Prompt §9 ("Wire SAST, dependency scanning, container scanning, and secret scanning into CI as required, non-bypassable status checks"), which §9's preamble explicitly calls **prerequisite infrastructure, not a feature to schedule later**. No feature branch, including Phase 2's security-baseline branches (canonical JWT schema, refresh-token rotation, Argon2id hashing), should be able to merge without this gate already active, because every one of those branches touches credential material.

---

## 2. Scope and requirements

**In scope:**
- `.env.example` files for `backend/` and `admin-web/`, and the Gradle equivalent (`local.properties.example`) for `mobile/`.
- A drift-check (CI job + local script) proving each example file's keys are a 1:1 match against the app's typed config schema (`Settings` fields, `env.ts` Zod schema keys, referenced `BuildConfig` fields).
- Root-level `.gitleaks.toml` secret-scanning ruleset, tuned with NoorHeroes-specific allowlists (lockfiles, generated OpenAPI clients, Firebase config files that are not secrets) and custom rules (internal token/key shapes used by this codebase).
- Root-level `.pre-commit-config.yaml` wiring the gitleaks pre-commit hook (protects staged changes before they're ever committed), applied repo-wide so it also covers `infra/`, `docs/`, and `mobile/` — surfaces Husky (admin-web) does not reach.
- `.github/workflows/secret-scan.yml` — a dedicated, always-triggered (not path-filtered) workflow running gitleaks (blocking) and trufflehog verified-only (blocking) on every push and pull request, registered as required status checks.
- The GCP Secret Manager wiring: `backend/src/noorheroes/core/secrets_bootstrap.py` (new), a minimal integration point into `main.py`'s startup sequence, and `infra/secrets/manifest.yaml` (the canonical secret-name ↔ env-var-name ↔ environment-tier ↔ owner registry).
- Repository hygiene: `.gitignore` entries guaranteeing `.env`, `.env.local`, `local.properties`, `*.pem`, `*.key`, and service-account JSON files are never tracked.
- A secret-rotation runbook stub (`docs/runbooks/secret-rotation.md`) that Production readiness (§15 below) depends on.

**Out of scope (owned by other Phase 1 items or later phases):**
- Provisioning the actual GCP project, VPC, IAM bindings, or the Secret Manager resources themselves — that's Terraform's job (`Development_Blueprints.Phase1_Infra_Config.Infra.04-terraform-iac-baseline-staging.md`, item 04). This document defines the manifest item 04's Terraform must satisfy; it does not write the `.tf` resource blocks for the secrets themselves beyond a minimal stub proving the wiring compiles.
- The five environment tiers' compute/network topology — that's item 01, this document's declared dependency.
- SAST (Bandit/Semgrep), dependency scanning, and container/image scanning — those are Security Baseline item 7's other three pillars, covered by `07-ci-pipeline-security-scan-stages.md`. This document only owns the *secret*-scanning pillar.
- Choosing the final email provider (SES/SendGrid/Postmark), the final LLM provider, or the final analytics vendor — those remain the open decisions Final_Development_Prompt §14 already flags. This document's `.env.example` lists the *variable names* for whichever is chosen, not the vendor choice itself.

---

## 3. Technical implementation details

### 3.1 Tool choice — gitleaks (primary) + trufflehog (secondary, verified-only)

Final_Development_Prompt §3.3 says "`gitleaks` or `trufflehog`"; §6's CI stage 3 explicitly names gitleaks. This blueprint resolves that as: **gitleaks is the primary, required tool everywhere (pre-commit and CI); trufflehog runs as a second, independent CI job in verified-only mode.** Rationale:

| Criterion | gitleaks | trufflehog |
|---|---|---|
| Speed (matters for pre-commit, blocks every `git commit`) | Single static Go binary, regex-based, sub-second on a typical diff | Slower — performs live verification calls against provider APIs |
| Pre-commit fit | Purpose-built `protect --staged` mode scans only the staged diff | Not designed for a sub-second staged-diff hook |
| False-positive rate | Higher (regex/entropy heuristics) — needs an allowlist | Near-zero on verified secrets (it confirms the credential is live) — but blind to secrets for providers it has no verifier for |
| CI fit | Fast, cheap, blocks on every pattern match | Slower but authoritative — a trufflehog verified hit means the leaked credential is *live right now*, which should page on-call, not just fail a PR |

Net effect: gitleaks is the fast, broad, pre-commit-friendly net that catches a secret before it leaves a laptop. trufflehog's verified-only CI job is a second, slower, higher-confidence net that catches anything gitleaks' regexes missed and — critically — tells you whether a leaked secret is still *active*, which changes the incident-response response (rotate immediately vs. just purge history). Both are mandatory; neither is a substitute for the other.

### 3.2 `.env.example` convention

Rules, enforced by the drift-check in §3.3:
- Every key in a typed config schema (a `Settings` field in `backend/src/noorheroes/core/settings.py`, a key in `admin-web/src/lib/env.ts`'s Zod object) MUST have a corresponding line in that app's `.env.example`.
- Every line in `.env.example` is `KEY=placeholder-or-safe-default`, never a real value. Non-secret operational defaults (e.g., `REDIS_URL=redis://localhost:6379/0` for local dev) are fine as literal values since they're not credentials; anything that is a credential gets an obviously-fake placeholder (e.g., `JWT_SIGNING_KEY=changeme-generate-with-openssl-rand-hex-32`) that will not work if accidentally left in place, and a comment noting where the real value comes from per tier.
- `.env.example` is grouped into commented sections mirroring the `Settings` class's logical groupings (App, Database, Redis/Celery, Auth/JWT, Object Storage, AI Providers, Email, Push, Observability, Secrets Provider) so it doubles as onboarding documentation, not just a flat key list.
- `.env` (the real, developer-local file) is git-ignored. `.env.example` is the only committed artifact. A new developer's setup path is: `cp backend/.env.example backend/.env`, fill in local-safe values (most defaults already work against the `docker-compose.yml` stack from item 03), never fill in a real Staging/Production secret into a local `.env`.

### 3.3 `.env.example` ↔ typed-config drift check

A drift check runs both as a fast local script (so a developer can self-check before pushing) and as a CI job (so it's enforced, not just suggested):

- **Backend:** `backend/scripts/check_env_example_sync.py` imports `Settings` (via `Settings.model_fields` — Pydantic v2 exposes the field name set without needing real env values, since every required-secret field must have a safe default or be `Optional` for this introspection to succeed; if a field genuinely has no safe default, mark it `exclude=True`-equivalent in a small `ENV_EXAMPLE_IGNORE` set at the top of the script with an inline reason, rather than silently skipping the check), computes the uppercased field-name set, parses `backend/.env.example` for its `KEY=` lines, and asserts the two sets are equal. Non-zero exit + a diff-style message (`Settings has X with no .env.example line`, `.env.example has Y with no matching Settings field`) on mismatch.
- **Admin-web:** `admin-web/scripts/check-env-example-sync.ts` imports the Zod object schema from `src/lib/env.ts` (via `schema.shape` / `schema.keyof().options`), does the same set-diff against `admin-web/.env.example`.
- Both scripts are wired into the CI backend/admin-web workflows as an early, cheap step (fits into pipeline stage 1 "Lint & format check" per Final_Development_Prompt §6 — cheapest stage first) and are documented in this file's Files to Create list (§5) rather than owned by the CI-pipeline blueprint (item 06/07), since the check's *logic* belongs with the `.env.example` convention this document owns; item 06 only needs to add one `run:` line invoking the already-written script.

### 3.4 Secrets-manager wiring: GCP Secret Manager, read at boot

**Vendor choice: GCP Secret Manager.** Final_Development_Prompt §14 and Consolidated_Blueprint_v6 §13.3/§2597 both explicitly leave the KMS/secrets-manager vendor as an **Assumed Requirement** for the infra team to confirm. This blueprint makes the concrete default decision the coding agent must implement against (see §18 Assumptions), justified by: §7 names Google Cloud Run as the first-listed managed-container target ("AWS ECS Fargate, Google Cloud Run, or a managed Kubernetes"), and GCP Secret Manager has zero additional infrastructure to stand up when the compute target is already Cloud Run (same IAM model, same project, native `--set-secrets` integration for the parts of the stack that don't need SDK-level rotation logic). If the infra team confirms AWS Fargate instead, only §3.4's `secrets_bootstrap.py` provider implementation and `infra/secrets/manifest.yaml`'s `provider:` field change — the `Settings` class, the `.env.example` contract, and every call site remain untouched, because the injection mechanism is isolated behind one bootstrap function.

**Mechanism — "read at boot via the platform SDK," per §3.3's literal requirement:**

1. `infra/secrets/manifest.yaml` is the canonical registry: for each logical secret (e.g. `jwt-signing-key`), it lists the target env var name (`JWT_SIGNING_KEY`), which environment tiers it applies to (`staging`, `production` — never `local`/`ci`, which use `.env` / GitHub Actions Secrets respectively per §3.5), the GCP Secret Manager resource name pattern (`noorheroes-{env}-{secret-id}`), and an owning team/rotation-cadence note.
2. `backend/src/noorheroes/core/secrets_bootstrap.py` exposes one function, `load_secrets_into_environ(environment: Environment) -> None`. For `Environment.LOCAL` and any environment where `SECRETS_PROVIDER=env` (the default, see §3.6), it is a no-op — the process environment (populated by `.env` via `python-dotenv`, or by CI's injected GitHub Actions Secrets) is trusted as-is. For `Environment.STAGING` / `Environment.PRODUCTION` (or any tier where `SECRETS_PROVIDER=gcp_secret_manager`), it reads `infra/secrets/manifest.yaml`, and for every manifest entry whose `environments` list includes the current tier, calls the `google-cloud-secret-manager` client's `access_secret_version` for `projects/{GCP_PROJECT_ID}/secrets/noorheroes-{env}-{secret-id}/versions/latest`, and sets `os.environ[env_var_name]` to the returned payload — **before** `Settings()` is ever instantiated.
3. `main.py`'s module-level bootstrap sequence (or the earliest point before `get_settings()`/the `settings` singleton is first constructed — confirm the exact singleton-construction call site in the existing `main.py`/`core/settings.py` before editing, per §9's "do not touch existing call sites blindly" convention) calls `load_secrets_into_environ(Environment(os.environ["ENVIRONMENT"]))` as the very first line of `lifespan()`'s startup half, ahead of `init_telemetry()` — so a missing/misconfigured secret fails loudly at container boot (crash-and-restart-loop, visible in the platform's health check) rather than silently propagating an empty credential into a running app.
4. This satisfies "never bakes secrets into container images": the container image contains zero secret values at build time; it contains only `secrets_bootstrap.py`'s code and the `manifest.yaml`'s *names*. The container's runtime service account (Cloud Run's attached IAM service account) is the only thing granted `roles/secretmanager.secretAccessor`, scoped per-secret (not project-wide) — see §9 Security.
5. **Rotation without redeploy is explicitly NOT delivered by this blueprint at MVP** — `load_secrets_into_environ` runs once, at boot. A rotated secret takes effect on the next deploy/restart, not live. This is a stated MVP trade-off (see §18 Assumptions) consistent with Final_Development_Prompt §7's "scheduled, tested restore drills" cadence-based operational model rather than a zero-downtime-rotation requirement; flag it explicitly in the secret-rotation runbook (§15) as a known limitation with a documented forced-restart step.

**Admin-web's variant:** Next.js's standalone server (per its own multi-stage Dockerfile, §7) reads `process.env` directly at runtime for every *server-only* variable — Cloud Run's native `--set-secrets=VAR=secret-name:latest` deploy-time flag is sufficient here (no bootstrap code needed, since Next.js doesn't have a single central `Settings`-style singleton constructed once at import time the way `pydantic-settings` does; `src/lib/env.ts`'s Zod parse already runs per-process-start against whatever `process.env` Cloud Run has already populated by the time the Node process starts). **Critical exception — `NEXT_PUBLIC_*` variables are inlined into the client JS bundle at *build* time, not read at runtime.** This means: (a) a `NEXT_PUBLIC_*` variable's value must be present in the CI build environment before `next build` runs, sourced from GitHub Actions Secrets/Variables (not GCP Secret Manager, since the build happens in CI, not on Cloud Run), and (b) **no secret may ever be assigned to a `NEXT_PUBLIC_*`-prefixed variable** — anything with that prefix ships to every browser that loads the admin portal. This is called out again in §9 Security as a hard rule, not a style preference.

### 3.5 Per-tier injection mechanism (ties to item 01's five tiers)

| Tier | Source of real secret values | Mechanism |
|---|---|---|
| Local | Developer's own `.env` (git-ignored, hand-filled from `.env.example`) | `python-dotenv` loads `backend/.env` before `Settings()` construction (already the existing pattern per FAST-API-INSTRUCTIONS.md); Next.js auto-loads `admin-web/.env.local` |
| CI | GitHub Actions repository/organization Secrets, referenced as `${{ secrets.NAME }}` in workflow `env:` blocks | Non-sensitive fixed values for ephemeral Testcontainers/`docker-compose.ci.yml` Postgres/Redis (these are throwaway per-run credentials, not real secrets — safe to hardcode in `docker-compose.ci.yml`, see item 06); real third-party sandbox/test API keys (if any integration test needs one) come from GitHub Secrets, never committed |
| Dev/QA (shared) | GCP Secret Manager, `noorheroes-devqa-*` secrets | Same `secrets_bootstrap.py` path as Staging/Production — Dev/QA is treated as secrets-manager-backed too, since it's long-lived and shared (per item 01), unlike CI's ephemeral per-run nature |
| Staging | GCP Secret Manager, `noorheroes-staging-*` secrets | `secrets_bootstrap.py`, read at boot |
| Production | GCP Secret Manager, `noorheroes-production-*` secrets | `secrets_bootstrap.py`, read at boot; additionally: access to `noorheroes-production-*` secrets is restricted to the Production service account and a minimal on-call human IAM group — see §9 |

### 3.6 `SECRETS_PROVIDER` — the switch

A new `Settings` field, `secrets_provider: Literal["env", "gcp_secret_manager"] = "env"`, is the single switch `secrets_bootstrap.py` reads (via `os.environ.get("SECRETS_PROVIDER", "env")`, read *before* full `Settings` construction since it gates whether secrets need injecting before `Settings()` can even succeed — this is why it's read directly from `os.environ`, not from an already-constructed `Settings` instance, and is itself documented as non-secret in `.env.example`). `.env.example` ships `SECRETS_PROVIDER=env` (the correct default for local/CI); Staging/Production's actual deploy configuration (Cloud Run env var, set by Terraform/item 04 or the deploy workflow, item 08) sets `SECRETS_PROVIDER=gcp_secret_manager`.

---

## 4. Architecture and component responsibilities

```
┌────────────────────────────────────────────────────────────────────────┐
│  DEVELOPER MACHINE                                                      │
│  backend/.env (gitignored) ──┐                                          │
│  admin-web/.env.local (gitignored) ──┤                                  │
│  mobile/local.properties (gitignored) ┘                                 │
│           │                                                             │
│           ▼  git commit                                                 │
│  .pre-commit-config.yaml → gitleaks protect --staged (BLOCKS commit)    │
└────────────────────────────────────────────────────────────────────────┘
                              │  git push
                              ▼
┌────────────────────────────────────────────────────────────────────────┐
│  GITHUB ACTIONS (CI)                                                    │
│  .github/workflows/secret-scan.yml                                      │
│    job: gitleaks-scan   (required status check, blocking)               │
│    job: trufflehog-verified-scan (required status check, blocking)      │
│  .github/workflows/backend.yml / admin-web.yml                          │
│    step: check_env_example_sync.py / check-env-example-sync.ts          │
│    env: ${{ secrets.* }}  ← GitHub Actions Secrets (CI-tier values)     │
└────────────────────────────────────────────────────────────────────────┘
                              │  merge to main → deploy
                              ▼
┌────────────────────────────────────────────────────────────────────────┐
│  DEV/QA · STAGING · PRODUCTION (Cloud Run)                              │
│  Container image  (built with ZERO secret values baked in)              │
│           │  boot                                                       │
│           ▼                                                             │
│  main.py::lifespan() → secrets_bootstrap.load_secrets_into_environ()    │
│           │  reads infra/secrets/manifest.yaml                          │
│           ▼                                                             │
│  GCP Secret Manager  (noorheroes-{env}-{secret-id}, latest version)     │
│           │  os.environ[VAR] = value                                    │
│           ▼                                                             │
│  core/settings.py::Settings()  ← unchanged, reads os.environ as always  │
└────────────────────────────────────────────────────────────────────────┘
```

**Component responsibilities:**

| Component | Owns | Does NOT own |
|---|---|---|
| `.gitleaks.toml` | Detection rules, allowlists, custom NoorHeroes secret-shape patterns | Enforcement wiring (that's the pre-commit config + CI workflow) |
| `.pre-commit-config.yaml` | Local, pre-commit-time enforcement (fast fail before commit exists) | CI-time enforcement (separate, cannot be bypassed by `--no-verify`) |
| `.github/workflows/secret-scan.yml` | CI-time enforcement, the actual non-bypassable gate (branch protection points here) | Formatting/lint/test CI jobs (those live in `backend.yml`/`admin-web.yml`/`mobile.yml`) |
| `backend/.env.example` / `admin-web/.env.example` / `mobile/local.properties.example` | The checklist of required config keys per app | The real values (never — these are examples only) |
| `check_env_example_sync.py` / `.ts` | Proving the checklist stays honest | Anything about *value* correctness (that's each field's own Pydantic/Zod validator, already owned by the existing `Settings`/`env.ts`) |
| `infra/secrets/manifest.yaml` | The registry of which secret exists in which tier, and its target env var name | Provisioning the actual GCP Secret Manager resource (Terraform's job, item 04) |
| `secrets_bootstrap.py` | Reading manifest-listed secrets into `os.environ` at boot, for Staging/Production/Dev-QA | Anything about how `Settings` interprets those values once present (unchanged, existing `core/settings.py` responsibility) |

---

## 5. Folder/file structure

```
noorheroes/
├── .gitleaks.toml                                  # NEW — root, repo-wide scan rules + allowlist
├── .pre-commit-config.yaml                         # NEW — root, gitleaks + (existing ruff/mypy hooks referenced, not owned here)
├── .gitignore                                       # MODIFY — add secret-bearing file patterns (§9)
├── .github/
│   └── workflows/
│       └── secret-scan.yml                          # NEW — gitleaks + trufflehog required status checks
├── backend/
│   ├── .env.example                                  # NEW
│   ├── scripts/
│   │   └── check_env_example_sync.py                 # NEW
│   └── src/noorheroes/
│       ├── core/
│       │   ├── settings.py                           # MODIFY — add `secrets_provider` field only; do not rename existing fields
│       │   └── secrets_bootstrap.py                   # NEW
│       └── main.py                                    # MODIFY — one call added at top of lifespan() startup
├── admin-web/
│   ├── .env.example                                   # NEW
│   ├── scripts/
│   │   └── check-env-example-sync.ts                  # NEW
│   └── src/lib/
│       └── env.ts                                     # MODIFY — additive only (§12); existing exported shape unchanged
├── mobile/
│   └── local.properties.example                       # NEW
├── infra/
│   └── secrets/
│       └── manifest.yaml                              # NEW — canonical secret registry, consumed by secrets_bootstrap.py and by item 04's Terraform
└── docs/
    └── runbooks/
        └── secret-rotation.md                          # NEW — rotation cadence + forced-restart procedure stub
```

---

## 6. APIs, models, interfaces, and data flow

This is an infra blueprint, not a feature with HTTP endpoints — "APIs" here means the internal contracts other blueprints/modules rely on.

**`infra/secrets/manifest.yaml` schema** (the contract Terraform/item 04 and `secrets_bootstrap.py` both read):

```yaml
# infra/secrets/manifest.yaml
version: 1
secrets:
  - id: jwt-signing-key              # → GCP resource: noorheroes-{env}-jwt-signing-key
    env_var: JWT_SIGNING_KEY
    environments: [devqa, staging, production]
    owner: backend-platform
    rotation_cadence_days: 90
    description: "HS256 signing key for JwtClaims (F37 B-01)."
  - id: database-url
    env_var: DATABASE_URL
    environments: [devqa, staging, production]
    owner: backend-platform
    rotation_cadence_days: 180
    description: "Async SQLAlchemy connection string, includes DB credential."
  - id: r2-secret-access-key
    env_var: R2_SECRET_ACCESS_KEY
    environments: [devqa, staging, production]
    owner: backend-platform
    rotation_cadence_days: 180
    description: "Cloudflare R2 S3-compatible secret key."
  - id: openai-api-key
    env_var: OPENAI_API_KEY
    environments: [staging, production]
    owner: ai-safety
    rotation_cadence_days: 365
    description: "AI provider key — see Final_Development_Prompt §14, vendor TBC."
  # ... one entry per credential-bearing var in backend/.env.example; see §7 for the full var list.
```

**`secrets_bootstrap.py` interface:**

```python
# backend/src/noorheroes/core/secrets_bootstrap.py
def load_secrets_into_environ(environment: Environment) -> None:
    """
    No-op for Environment.LOCAL or when SECRETS_PROVIDER=env.
    Otherwise: reads infra/secrets/manifest.yaml, filters entries whose
    `environments` includes `environment`, fetches each from GCP Secret
    Manager (latest version), and sets os.environ[entry.env_var].
    Raises SecretsBootstrapError (a new, narrow exception — not a generic
    Exception) on any missing/inaccessible secret, causing the app to
    fail startup rather than run with a missing credential.
    """
```

**Data flow (Staging/Production boot):**
`main.py` module import → `lifespan()` startup begins → `load_secrets_into_environ(Environment.STAGING)` → manifest parsed → for each matching entry, `secretmanager.SecretManagerServiceClient().access_secret_version(name=...)` → `os.environ[entry.env_var] = response.payload.data.decode("utf-8")` → (all entries processed) → `get_settings()` / `Settings()` constructed for the first time, reading the now-fully-populated `os.environ` exactly as it already does today → `init_telemetry()` and the rest of `lifespan()` proceed unchanged.

**Data flow (secret-scan CI gate):**
`git push` / PR opened → GitHub Actions triggers `secret-scan.yml` (no path filter — every push, unlike the path-filtered `backend.yml`/`admin-web.yml`/`mobile.yml`, since a secret can land in any file in any app) → `gitleaks-scan` job runs `gitleaks detect --source . --config .gitleaks.toml --report-format sarif --report-path gitleaks.sarif --exit-code 1` → SARIF uploaded via `github/codeql-action/upload-sarif` for inline PR annotations → job exit code determines the GitHub commit status → `trufflehog-verified-scan` job runs `trufflehog github --repo=$REPO --only-verified --fail` in parallel → both statuses must be green for the branch-protection rule to allow merge.

---

## 7. Dependencies and configuration requirements

### 7.1 New tool dependencies

| Tool | Version pin | Installed via |
|---|---|---|
| gitleaks | Pin to a specific tagged release (e.g. `v8.21.x` — confirm latest stable at implementation time; do not float `latest` in CI, pin exactly, bump deliberately via a dependency PR) | `pre-commit`'s hook manager (auto-installs the pinned gitleaks binary); CI job uses the official `gitleaks/gitleaks-action` pinned to the same version tag so pre-commit and CI never disagree on findings |
| trufflehog | Pin to a specific tagged release | `trufflesecurity/trufflehog` official GitHub Action, pinned |
| `pre-commit` (Python framework) | Already a dev dependency per Final_Development_Prompt §4; add to `backend/pyproject.toml`'s dev-dependency group if not already present, since it's now the mechanism securing the *whole* repo, not just backend | `uv`/Poetry dev group |
| `google-cloud-secret-manager` (Python) | Latest stable, added to `backend/pyproject.toml` main dependencies (needed at runtime in Staging/Production, not just dev) | `uv add google-cloud-secret-manager` |
| `PyYAML` | Only if not already a transitive dependency — needed by `secrets_bootstrap.py` and both `check_env_example_sync` scripts to parse `manifest.yaml` | `uv add pyyaml` if missing |

### 7.2 `backend/.env.example` — full contents

```dotenv
# ============================================================
# NoorHeroes Backend — Local Environment Configuration
# Copy to .env and fill in local-safe values. NEVER commit .env.
# Every key below MUST have a matching field in core/settings.py —
# enforced by scripts/check_env_example_sync.py in CI.
# ============================================================

# --- App ---
ENVIRONMENT=local                              # local | development | staging | production (Environment enum)
APP_NAME=noorheroes-backend
DEBUG=true
API_V1_PREFIX=/v1

# --- Secrets provider switch (see §3.6) ---
SECRETS_PROVIDER=env                           # env | gcp_secret_manager — Staging/Prod deploy config overrides this to gcp_secret_manager
GCP_PROJECT_ID=                                # only required when SECRETS_PROVIDER=gcp_secret_manager

# --- Database (Async SQLAlchemy 2.x) ---
DATABASE_URL=postgresql+asyncpg://noorheroes:noorheroes@localhost:5432/noorheroes
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# --- Redis (cache, rate-limit counters, Celery broker/result backend, OTP/step-up session state) ---
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# --- Auth / JWT (F37 B-01/B-02/B-04) ---
JWT_SIGNING_KEY=changeme-generate-with-openssl-rand-hex-32     # CREDENTIAL — real value never lives here past local dev
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_TTL_SECONDS=900
JWT_REFRESH_TOKEN_TTL_SECONDS=2592000
ARGON2_TIME_COST=3
ARGON2_MEMORY_COST_KIB=65536
ARGON2_PARALLELISM=4

# --- Object storage (Cloudflare R2, S3-compatible) ---
R2_ACCOUNT_ID=changeme
R2_ACCESS_KEY_ID=changeme                       # CREDENTIAL
R2_SECRET_ACCESS_KEY=changeme                    # CREDENTIAL
R2_BUCKET_NAME=noorheroes-media-local
R2_PUBLIC_CDN_URL=https://cdn.local.noorheroes.example

# --- AI providers (F35 — vendor confirmed per Final_Development_Prompt §14; keep only the active one populated) ---
AI_PROVIDER=openai                               # openai | claude | gemini | deepseek
OPENAI_API_KEY=                                   # CREDENTIAL — leave blank locally unless testing AI features
ANTHROPIC_API_KEY=                                # CREDENTIAL
GOOGLE_AI_API_KEY=                                # CREDENTIAL
DEEPSEEK_API_KEY=                                 # CREDENTIAL

# --- Email (OTP fallback + transactional — vendor TBC per §14; keep only the active one populated) ---
EMAIL_PROVIDER=ses                                # ses | sendgrid | postmark
SES_ACCESS_KEY_ID=                                # CREDENTIAL
SES_SECRET_ACCESS_KEY=                            # CREDENTIAL
SES_REGION=us-east-1
SENDGRID_API_KEY=                                 # CREDENTIAL
POSTMARK_SERVER_TOKEN=                            # CREDENTIAL

# --- Google OAuth (Login with Google, per A.1) ---
GOOGLE_OAUTH_CLIENT_ID=
GOOGLE_OAUTH_CLIENT_SECRET=                       # CREDENTIAL

# --- Push notifications (FCM) ---
FCM_SERVICE_ACCOUNT_JSON_PATH=./secrets/fcm-service-account.local.json   # local-only file path, never committed

# --- Observability ---
SENTRY_DSN=                                       # CREDENTIAL-adjacent (treat as sensitive; DSNs are effectively write-only but scope-limit exposure)
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318

# --- CORS / rate limiting (non-secret, tuning-only) ---
CORS_ALLOWED_ORIGINS=http://localhost:3000
RATE_LIMIT_DEFAULT_PER_MINUTE=60
```

### 7.3 `admin-web/.env.example` — full contents

```dotenv
# ============================================================
# NoorHeroes Admin Portal — Local Environment Configuration
# Copy to .env.local. NEVER commit .env.local.
# NEXT_PUBLIC_* vars are inlined into the CLIENT BUNDLE at build
# time — NEVER put a secret behind a NEXT_PUBLIC_ prefix.
# Every key below MUST have a matching key in src/lib/env.ts's
# Zod schema — enforced by scripts/check-env-example-sync.ts in CI.
# ============================================================

# --- Public (client-bundle-safe, build-time-inlined) ---
NEXT_PUBLIC_APP_ENV=local
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_SENTRY_DSN=

# --- Server-only (runtime, never sent to the browser) ---
API_INTERNAL_BASE_URL=http://localhost:8000        # used by Server Components / route handlers calling the backend directly
SESSION_COOKIE_SIGNING_SECRET=changeme-generate-with-openssl-rand-hex-32   # CREDENTIAL — signs the httpOnly session cookie
SENTRY_AUTH_TOKEN=                                  # CREDENTIAL — CI/build-time only, for sourcemap upload; never needed locally
```

### 7.4 `mobile/local.properties.example` — contents

```properties
# NoorHeroes Mobile — Local Gradle Properties
# Copy to local.properties (already gitignored by the default Android
# Gradle .gitignore; verify it is NOT removed by any future .gitignore edit).
# These map to BuildConfig fields via the dev/staging/prod build
# variants (Final_Development_Prompt §13.1's Configuration management row)
# — no .env file is used on the mobile side; this is the Gradle-native
# equivalent of the same convention.

# Base API URL per build variant (overridable locally for pointing at
# a developer's own backend instance instead of the shared dev/QA one)
NOORHEROES_DEV_API_BASE_URL=http://10.0.2.2:8000

# Google OAuth Android client ID (public identifier, not a secret, but
# kept out of version control alongside the rest of this file for
# consistency and because per-developer values differ)
NOORHEROES_GOOGLE_OAUTH_ANDROID_CLIENT_ID=changeme
```

---

## 8. Database/storage requirements

No new database tables. Two storage-adjacent items:

- **GCP Secret Manager** itself is the "storage" this blueprint wires in — each entry in `infra/secrets/manifest.yaml` corresponds to one Secret Manager secret (with automatic version history GCP already provides; no custom versioning logic needed).
- **`infra/secrets/manifest.yaml`** is itself a git-tracked, plaintext YAML file — by construction, it never contains a secret *value*, only secret *names* and metadata (owner, rotation cadence, target env var, applicable tiers). This is safe to commit and is itself covered by the gitleaks scan (as a sanity backstop, not because it's expected to ever trigger a finding).

---

## 9. Authentication, authorization, validation, and security considerations

- **IAM least privilege:** each environment tier's Cloud Run service account is granted `roles/secretmanager.secretAccessor` on *only* the specific secrets listed for that tier in `infra/secrets/manifest.yaml` (per-secret IAM binding, not a project-wide role) — Production's service account must never have read access to Staging secrets or vice versa. This binding is provisioned by Terraform (item 04), driven by the manifest this document owns.
- **Production secret access for humans:** direct human access to `noorheroes-production-*` secrets (e.g., via `gcloud secrets versions access` for manual rotation) is restricted to a minimal on-call/platform-owner IAM group, and every access is visible in GCP Cloud Audit Logs (Data Access logs must be explicitly enabled for the Secret Manager API, since they're off by default) — this audit trail is a direct input to the "Security Posture Dashboard" named in Final_Development_Prompt §8's Admin observability row.
- **`NEXT_PUBLIC_*` hard rule (repeated from §3.4 because it is the single most common real-world Next.js secrets leak):** no secret, ever, behind a `NEXT_PUBLIC_` prefix. `check-env-example-sync.ts` additionally asserts (as a second check beyond pure key-set equality) that no `NEXT_PUBLIC_*` key in `.env.example` is present in a small hardcoded "known-sensitive-name" pattern list (`*_SECRET`, `*_KEY`, `*_TOKEN`, `*_PASSWORD`) as a lightweight guardrail — this is a heuristic backstop, not a substitute for gitleaks, which is the authoritative scanner.
- **`.gitignore` additions (this blueprint modifies the root `.gitignore`):**
  ```gitignore
  # Secrets & local environment — never commit
  .env
  .env.local
  .env.*.local
  backend/.env
  admin-web/.env.local
  local.properties
  mobile/local.properties
  **/*.pem
  **/*.key
  **/google-services-account*.json
  **/*-service-account*.json
  secrets/
  ```
  Note explicitly: `google-services.json` / `GoogleService-Info.plist` (Firebase *client* config, not a service-account credential) are **not** added to this ignore list — Google's own guidance treats those as safe-to-commit app identifiers, not secrets; only the Admin-SDK *service-account* JSON (used server-side by `core-notifications`'/backend's FCM integration) is secret and matched by the `*-service-account*.json` pattern above. Do not conflate the two when implementing.
- **`.gitleaks.toml` allowlist requirements** — without these, gitleaks will false-positive-block the repo on day one:
  ```toml
  # .gitleaks.toml (excerpt — allowlist section)
  [allowlist]
  paths = [
    '''pnpm-lock\.yaml''',
    '''uv\.lock''',
    '''.*\.example$''',        # .env.example / local.properties.example — placeholders only, but see below
    '''.*/openapi\.json$''',   # generated OpenAPI schema exports
    '''.*/gradle/libs\.versions\.toml''',
  ]
  ```
  Even though `.env.example` files are allowlisted by path, every credential-shaped placeholder inside them (§7.2–7.4) is deliberately written as an obvious non-secret (`changeme-...`, empty string) specifically so that if the allowlist entry is ever accidentally narrowed or removed, gitleaks still finds nothing real to flag — defense in depth, not reliance on the allowlist alone.
- **Custom gitleaks rules** for NoorHeroes-specific credential shapes not covered by gitleaks' default ruleset (extend, do not replace, the default `gitleaks.toml` base config via `[extend] useDefault = true`):
  ```toml
  [[rules]]
  id = "noorheroes-jwt-signing-key-assignment"
  description = "Hardcoded JWT_SIGNING_KEY value outside .env.example"
  regex = '''JWT_SIGNING_KEY\s*=\s*['"]?[A-Za-z0-9+/=_-]{32,}['"]?'''
  path = '''\.py$|\.ts$|\.kt$'''

  [[rules]]
  id = "noorheroes-r2-secret-key-assignment"
  description = "Hardcoded R2/S3-compatible secret access key"
  regex = '''R2_SECRET_ACCESS_KEY\s*=\s*['"]?[A-Za-z0-9+/=_-]{20,}['"]?'''
  path = '''\.py$|\.ts$|\.kt$'''
  ```
  These two rules exist specifically because they're the platform's two most catastrophic single-secret leaks (JWT signing key = full auth bypass across every family account; R2 secret key = read/write access to all uploaded child-facing media) — the default gitleaks ruleset's generic "generic-api-key" entropy rule already covers most other cases, but explicit rules give a clearer PR annotation for these two.
- **Redaction cross-check:** the existing `StructuredLoggingMiddleware` (backend) and admin-web's `logger.ts` PII-redaction pattern (both already implemented per the Core setup manuals) must also redact any value matching the same shapes these gitleaks rules target, so a secret that somehow reaches a runtime log line (e.g., an exception's `repr()` including a config object) doesn't leak via Sentry/log aggregation even after passing the git-level scan. This is a cross-reference, not new work owned by this blueprint — flag it as a follow-up verification item if the redaction rule set doesn't already cover `JWT_SIGNING_KEY`/`R2_SECRET_ACCESS_KEY`-shaped values.

---

## 10. Error handling and edge cases

| Scenario | Behavior |
|---|---|
| `load_secrets_into_environ` cannot reach GCP Secret Manager (network, IAM misconfiguration) at boot | Raise `SecretsBootstrapError`, crash the process before `Settings()` is constructed — never start serving traffic with a partially-populated environment. Cloud Run's health check then reports the revision unhealthy; this is the intended fail-closed behavior. |
| A manifest entry references a secret that doesn't exist yet in GCP Secret Manager for that tier | Same as above — `access_secret_version` raises `NotFound`, wrapped into `SecretsBootstrapError` naming the missing secret id, never silently defaulted to an empty string. |
| A developer's local `.env` is missing a key present in `.env.example` | `Settings()` construction fails with Pydantic's own validation error (existing behavior, unchanged) — this blueprint does not add new local-dev validation beyond what `pydantic-settings` already provides; `.env.example`'s drift-check (§3.3) is a *CI-time* documentation-honesty check, not a substitute for that runtime validation. |
| `.env.example` and `Settings`/`env.ts` drift (a field added to one, not the other) | CI fails at the drift-check step (§3.3), before any test/build step runs — this is the primary edge case this whole convention exists to prevent from going unnoticed. |
| gitleaks flags a true positive already merged to `main` (discovered later, e.g., by trufflehog's verified scan after a rule update) | The CI job fails on that commit's re-scan (gitleaks/trufflehog scan the current tree, not just the diff, on a scheduled/nightly re-run — see §11); this is treated as a P1 incident per the secret-rotation runbook (§15), not just a code-review comment — the leaked credential must be rotated, not merely removed from the current file (git history still contains it). |
| gitleaks/trufflehog produces a false positive (e.g., a test fixture UUID that happens to match an entropy threshold) | Fixed via an explicit, narrowly-scoped `.gitleaks.toml` allowlist entry (path- or fingerprint-based, using gitleaks' `--baseline-path` mechanism for a per-finding fingerprint allowlist rather than a broad path exclusion) added in the same PR, with a one-line justification comment — never via `git commit --no-verify` or disabling the CI job. |
| A developer runs `git commit --no-verify` to bypass the local pre-commit hook | The CI-level `secret-scan.yml` gate still catches it — this is exactly why pre-commit alone is insufficient and CI enforcement (§3.1) is mandatory, not optional defense-in-depth. |
| A repo admin attempts to merge a PR with a failing `secret-scan.yml` status | Blocked — branch protection's "Include administrators" is enabled specifically to remove this escape hatch (§11). |

---

## 11. State management and lifecycle considerations

- **`secrets_bootstrap.py` has no persistent state of its own** — it runs once per process boot, mutates `os.environ` in place, and its effect (populated env vars) lives for the lifetime of that single process. A rolling deploy naturally picks up new secret versions because each new revision's containers re-run the boot sequence.
- **Secret Manager version lifecycle:** every manifest entry always resolves `versions/latest`. When a secret is rotated (a new version added in GCP Secret Manager), it takes effect only on the *next* container boot — this blueprint does not implement a "disable old version" step; that remains a manual/runbook step (§15) so an in-flight rolling deploy during rotation doesn't have some replicas fail mid-rollout. Disabling (not destroying) the previous version is the recommended runbook action, taken only after confirming all replicas are on the new version.
- **CI job lifecycle:** `secret-scan.yml`'s jobs are stateless per-run — no caching of previous findings across runs is required for correctness (gitleaks scans the current diff/tree fresh each time), though caching the gitleaks/trufflehog binary download (via `actions/cache` or the official action's built-in caching) is a reasonable performance optimization, not a correctness requirement.
- **Pre-commit hook lifecycle:** installed once per developer clone via `pre-commit install` (part of the repo's `make setup`/onboarding step, cross-referenced from item 03's Docker Compose onboarding flow) — a hook that isn't installed locally is not a gap in this blueprint's guarantee, because the CI gate is the actual non-bypassable backstop (§3.1); the pre-commit hook is a fast-feedback convenience layer on top of it, not the enforcement mechanism itself.

---

## 12. Integration points with existing modules

- **Backend `pydantic-settings` `Settings`/`Environment` (already built, `core/settings.py`):** this blueprint adds exactly one new field, `secrets_provider: Literal["env", "gcp_secret_manager"] = "env"`, and does not rename, remove, or change the type of any existing field. The existing `Environment` StrEnum (`LOCAL, DEVELOPMENT, STAGING, PRODUCTION`) is reused as-is by `secrets_bootstrap.py`'s tier check — do not introduce a second environment-tier enum. If `Settings` currently uses `SettingsConfigDict(env_file=".env")`, that continues to work unchanged for local dev; `secrets_bootstrap.py` runs *before* `Settings()` is constructed specifically so that by the time `pydantic-settings` reads `os.environ`/the `.env` file, GCP-sourced values are already present and simply look like ordinary env vars to `Settings` — zero changes to `Settings`'s own field-reading logic are required.
- **Admin-web Zod `env.ts` (already built):** additive only — add the new keys from §7.3 to the existing Zod object schema, in the same style as existing keys (confirm whether the existing schema is a flat `z.object({...})` or split public/server schemas before editing, and follow whichever pattern is already there rather than introducing a second pattern). Do not change how `env.ts` is imported/consumed elsewhere in the codebase (`src/lib/env.ts`'s existing export shape — e.g. a single parsed `env` object — must remain the single import surface every other module already uses).
- **Mobile `core-security` (Keychain/Keystore-backed TokenStore, already built):** no code change required by this blueprint. The integration point is purely conventional: this document establishes that build-time configuration (API base URLs, OAuth client IDs — non-secret identifiers) flows through Gradle `local.properties`/`BuildConfig`, while genuinely sensitive *runtime* material (the parent's JWT, refresh token, PIN hash) continues to be written exclusively through `core-security`'s existing secure-storage abstraction, never through `local.properties`/`BuildConfig` (which are readable in a decompiled APK) and never through a `.env`-style mechanism on-device. This blueprint does not introduce any new on-device secret storage — it only extends the existing `.env.example`-equivalent *build-time config checklist* convention to mobile via `local.properties.example`.
- **Mobile `core-datastore` (already built):** unaffected — `core-datastore` is Multiplatform-Settings-backed for non-sensitive preferences and remains out of scope for this document, which concerns build-time/deploy-time secrets, not on-device app state.
- **CI/CD pipeline (item 06/07/08, not yet built):** this blueprint's `secret-scan.yml` is a *separate*, always-triggered workflow file, not a job appended inside `backend.yml`/`admin-web.yml`/`mobile.yml`. Item 06 ("CI stages 1–7") should add the `check_env_example_sync`/`check-env-example-sync` step calls (§3.3) into its own lint-stage job, referencing the scripts this document creates — item 06 does not need to re-implement secret scanning, only wire in the two drift-check script invocations.
- **Terraform IaC (item 04, not yet built):** consumes `infra/secrets/manifest.yaml` as its source list for which `google_secret_manager_secret` resources to declare and which `google_secret_manager_secret_iam_member` bindings to create per tier's service account. This document does not write those `.tf` resource blocks (beyond the minimal stub in §13 step 8) — that's item 04's deliverable, driven by this manifest.

---

## 13. Development steps in the correct implementation order

1. **Author `.gitleaks.toml`** (§9) at repo root, including the allowlist and the two custom rules. Run `gitleaks detect --source . --config .gitleaks.toml` locally against the current tree and resolve every finding (fix real ones, allowlist confirmed false positives) before proceeding — the repo must start from a clean baseline.
2. **Author `.pre-commit-config.yaml`** at repo root with (at minimum) the gitleaks hook:
   ```yaml
   repos:
     - repo: https://github.com/gitleaks/gitleaks
       rev: v8.21.2  # pin exact tag at implementation time
       hooks:
         - id: gitleaks
           name: gitleaks (secret scan, staged changes)
           entry: gitleaks protect --staged --redact -v --config=.gitleaks.toml
           language: golang
           pass_filenames: false
   ```
   (Other hooks — ruff, mypy, ESLint/Prettier via a mirror hook or left to Husky — are not this document's concern; add this repo block alongside whatever item 02/Phase 0's existing `.pre-commit-config.yaml`, if any, already contains, rather than overwriting it.)
3. **Update `.gitignore`** with the patterns from §9.
4. **Write `backend/.env.example`** (§7.2), cross-checked field-by-field against the *actual current* `Settings` class (read the real file, not just this document's assumed field list, before finalizing — this document's names are the intended convention, but the existing `Settings` implementation is authoritative for exact field names already in use).
5. **Write `admin-web/.env.example`** (§7.3), similarly cross-checked against the actual current `src/lib/env.ts`.
6. **Write `mobile/local.properties.example`** (§7.4).
7. **Write `check_env_example_sync.py` and `check-env-example-sync.ts`** (§3.3); run both locally and confirm they pass against the just-written example files.
8. **Write `infra/secrets/manifest.yaml`** (§6), enumerating every credential-bearing var from steps 4–5 that applies to Dev/QA/Staging/Production. Add a minimal `infra/terraform/secrets.tf.stub` (or clearly marked placeholder, not wired into any `terraform apply` yet) proving the manifest's shape is Terraform-consumable, explicitly deferring the real module to item 04.
9. **Write `backend/src/noorheroes/core/secrets_bootstrap.py`** (§6), including the `SecretsBootstrapError` exception and the `env`/`gcp_secret_manager` branch.
10. **Modify `backend/src/noorheroes/core/settings.py`** to add the single `secrets_provider` field.
11. **Modify `backend/src/noorheroes/main.py`** to call `load_secrets_into_environ(...)` as the first line of `lifespan()`'s startup sequence, ahead of `init_telemetry()`.
12. **Modify `admin-web/src/lib/env.ts`** to add the new keys from §7.3, additive-only.
13. **Write `.github/workflows/secret-scan.yml`** (§14 Testing has the concrete job spec) with both the gitleaks and trufflehog jobs.
14. **Write `docs/runbooks/secret-rotation.md`** (§15).
15. **Configure GitHub branch protection** on `main` (and any long-lived release branch, if the team uses one — per Final_Development_Prompt §6, trunk-based dev means this is likely just `main`): require the `gitleaks-scan` and `trufflehog-verified-scan` status checks, enable "Include administrators," enable "Require branches to be up to date before merging." This is a GitHub repository setting, not a file in the repo, but is a mandatory, verifiable step in this blueprint's Definition of Done (§17) — document the exact settings screenshot/confirmation in the PR that implements this blueprint.
16. **Run the full local onboarding flow end-to-end** (`cp .env.example .env` for backend and admin-web, `pre-commit install`, attempt a commit with a deliberately fake secret staged, confirm it's blocked, remove it, commit successfully) to prove the whole chain works before declaring this blueprint done.

---

## 14. Testing strategy and acceptance criteria

**`.github/workflows/secret-scan.yml` — concrete job spec:**

```yaml
name: Secret Scan
on:
  push:
    branches: ["**"]
  pull_request:
    branches: ["main"]

permissions:
  contents: read
  security-events: write   # required for SARIF upload

jobs:
  gitleaks-scan:
    name: gitleaks-scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0   # full history — gitleaks needs it to scan the actual diff range, not just the checked-out ref
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITLEAKS_CONFIG: .gitleaks.toml
        # gitleaks-action fails the step (and therefore the required check) on any finding by default

  trufflehog-verified-scan:
    name: trufflehog-verified-scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: trufflesecurity/trufflehog@main
        with:
          extra_args: --only-verified --fail
```

Both job names (`gitleaks-scan`, `trufflehog-verified-scan`) are the exact strings entered into GitHub's branch-protection "required status checks" list — record them verbatim so the protection rule doesn't silently stop matching after a job rename.

**Test coverage this blueprint must ship with:**

| Test | Type | Location | Asserts |
|---|---|---|---|
| `test_check_env_example_sync_backend_passes` | Unit/script test | `backend/tests/scripts/test_check_env_example_sync.py` | Running the sync script against the real `backend/.env.example` + real `Settings` exits 0 |
| `test_check_env_example_sync_backend_catches_drift` | Unit/script test | same file | A deliberately-mutated copy (temp file with one key removed) causes the script to exit non-zero with a message naming the missing key |
| `check-env-example-sync` admin-web equivalents | Vitest | `admin-web/tests/scripts/check-env-example-sync.test.ts` | Same two assertions, admin-web side |
| `test_secrets_bootstrap_noop_for_local` | Unit | `backend/tests/core/test_secrets_bootstrap.py` | `load_secrets_into_environ(Environment.LOCAL)` makes zero network calls (mock the Secret Manager client, assert `access_secret_version` never called) |
| `test_secrets_bootstrap_env_provider_noop` | Unit | same file | With `SECRETS_PROVIDER=env` set regardless of tier, still a no-op |
| `test_secrets_bootstrap_gcp_provider_populates_environ` | Unit | same file | With a mocked Secret Manager client and `SECRETS_PROVIDER=gcp_secret_manager`, every manifest entry for `Environment.STAGING` results in the corresponding `os.environ` key being set to the mocked payload |
| `test_secrets_bootstrap_missing_secret_raises` | Unit | same file | Mocked client raising `NotFound` propagates as `SecretsBootstrapError`, and `Settings()` is never reached (assert via a spy/mock that a hypothetical downstream call didn't happen) |
| **Canary test — gitleaks actually blocks a real secret shape** | Integration, run in an isolated temp git repo (NOT the real repo — never actually commit a real-looking secret to the real history) | `scripts/test_gitleaks_canary.sh` (or CI-only ephemeral step) | Initialize a scratch git repo in a temp dir, copy in the real `.gitleaks.toml`, stage a file containing a fake-but-shape-correct value matching the `noorheroes-jwt-signing-key-assignment` custom rule, run `gitleaks protect --staged`, assert non-zero exit. This is the direct analog of F37's "architectural test" pattern (per FAST-API-INSTRUCTIONS.md-adjacent blueprints' convention) applied to secret scanning — it proves the rule actually fires, not just that the config file parses. |
| **CI required-status-check verification (manual, one-time, documented in the implementing PR)** | Manual acceptance step | N/A | Open a throwaway PR against a scratch branch containing a deliberately fake secret; confirm both `gitleaks-scan` and `trufflehog-verified-scan` (for a verifiable test credential, if using trufflehog's verification requires a real-but-revoked test key — coordinate with a disposable/sandboxed provider key if exercising the verified-only path) report failure and the PR's merge button is disabled; confirm a repo admin also cannot force-merge. Delete the branch after. |

**Acceptance criteria (all must hold before this blueprint is considered implemented):**
- `backend/.env.example` and `admin-web/.env.example` exist, are non-empty, and `check_env_example_sync`/`check-env-example-sync` both pass against the current `Settings`/`env.ts`.
- `pre-commit install` + a staged fake secret → commit blocked locally.
- A pushed branch with a fake secret → both `secret-scan.yml` jobs fail, PR merge button disabled, confirmed unbypassable by an admin account.
- `secrets_bootstrap.py`'s full unit-test suite (above) passes.
- `infra/secrets/manifest.yaml` lists every credential-bearing key from `backend/.env.example` §7.2 that applies to Dev/QA/Staging/Production.
- No real secret value exists anywhere in the git history introduced by this blueprint's own implementing PR (self-audit via `gitleaks detect` against the PR's own diff before requesting review).

---

## 15. Production-readiness considerations

- **Rotation cadence:** per `infra/secrets/manifest.yaml`'s `rotation_cadence_days` field — 90 days for the JWT signing key and any credential with direct auth-bypass blast radius, 180 days for storage/database credentials, 365 days for lower-risk third-party API keys, and **immediate** (out-of-band, not on the scheduled cadence) rotation for any secret a gitleaks/trufflehog CI run confirms was exposed, per §10's edge case. `docs/runbooks/secret-rotation.md` must document the exact `gcloud secrets versions add` + service restart sequence per secret, and must explicitly state the "no live rotation" limitation from §3.4 point 5 so on-call staff know a restart is required, not optional.
- **Audit logging:** enable GCP Cloud Audit Logs' Data Access logs for the Secret Manager API (off by default, must be explicitly turned on per §9) — this is a Terraform (item 04) deliverable but is *specified* here as a hard requirement of this blueprint's threat model, since without it a compromised service account's secret reads are invisible.
- **Backup/DR interaction:** Final_Development_Prompt §7 requires tested restore drills for the database; when a restore drill provisions a fresh Staging/Dev-QA database instance, `DATABASE_URL`'s secret value in GCP Secret Manager must be updated to point at the restored instance *before* the next deploy — call this out explicitly in the restore-drill runbook (owned by a different blueprint, cross-reference only) as a dependency on this document's secrets wiring.
- **Cost/quota:** GCP Secret Manager billing is per-secret-version-access; `secrets_bootstrap.py`'s read-once-at-boot design keeps this bounded and predictable (one access per secret per container cold start, not per-request) — do not refactor to a per-request secret fetch without re-evaluating this cost model.
- **Vendor-lock exit path:** because every call site reads from `os.environ` via the unchanged `Settings` class, and `secrets_bootstrap.py` is the single isolated integration point with the GCP SDK, migrating to AWS Secrets Manager (if the infra team's final vendor decision per §14 differs from this document's GCP default) is a change confined to `secrets_bootstrap.py` + `infra/secrets/manifest.yaml`'s `provider` field + the Terraform module — explicitly not a `Settings`/`env.ts`/application-code change. Confirm this isolation is preserved during implementation; it is the primary reason this architecture is safe to build against an as-yet-unconfirmed vendor choice.
- **Incident response tie-in:** a confirmed secret leak (via trufflehog's verified-only signal, or manual discovery) triggers the same incident-response runbook process Final_Development_Prompt §9 item 9 requires generally — this blueprint's runbook stub (§13 step 14) is the secret-specific playbook that runbook references, not a replacement for it.

---

## 16. Dependencies/prerequisites

- **Hard dependency:** item 01 (`01-environment-tiers-provisioning.md`) — this document assumes the five tiers (Local, CI, Dev/QA, Staging, Production) already exist as named concepts with known GCP project boundaries (or equivalent) before `infra/secrets/manifest.yaml`'s `environments` field and `secrets_bootstrap.py`'s tier-branching logic can be finalized against real project IDs.
- **Soft dependency (parallelizable, but this document's manifest is the input):** item 04 (`04-terraform-iac-baseline-staging.md`) — Terraform needs this document's `infra/secrets/manifest.yaml` to know what to provision; this document does not need Terraform to already exist to be authored (the bootstrap code can be written and unit-tested against a mocked Secret Manager client before real GCP resources exist), but the *end-to-end* Staging boot flow (§4's architecture diagram) cannot be exercised for real until item 04 has created the actual secrets.
- **Consumed by:** item 06/07 (CI pipeline blueprints) wire this document's drift-check scripts and reference this document's `secret-scan.yml` as the canonical example of a "required, non-bypassable status check" pattern they should replicate for SAST/dependency/container scanning (Security Baseline item 7's other three pillars).
- **Consumed by:** Phase 2's F37 Security Architecture backend blueprints (already existing in the corpus, e.g. B-01 canonical JWT schema, B-02 refresh-token rotation, B-04 credential hashing) — every one of those blueprints' `JWT_SIGNING_KEY`/credential-adjacent configuration must resolve through this document's `.env.example`/`secrets_bootstrap.py` path, not through an ad hoc local constant.

---

## 17. Definition of Done

- [ ] `.gitleaks.toml` exists, extends the default ruleset, includes the allowlist (§9) and both custom rules, and `gitleaks detect` returns zero findings against the current repo tree.
- [ ] `.pre-commit-config.yaml` includes the pinned gitleaks hook; `pre-commit install` + a staged fake secret is locally blocked.
- [ ] `.github/workflows/secret-scan.yml` exists with both `gitleaks-scan` and `trufflehog-verified-scan` jobs, triggered on every push and PR (no path filter).
- [ ] Both jobs are configured as required status checks in `main`'s branch protection, with "Include administrators" enabled — verified by a documented manual test (a repo admin cannot merge past a failing scan).
- [ ] `backend/.env.example`, `admin-web/.env.example`, `mobile/local.properties.example` exist, are non-empty, and match this document's §7 content (or the real current `Settings`/`env.ts` field set, if it has since diverged from this document's assumed names — the drift-check scripts are the authoritative arbiter, not this document's literal text).
- [ ] `check_env_example_sync.py` / `check-env-example-sync.ts` exist, pass against the real config, and are wired into CI (via item 06, cross-referenced, or as a standalone step added by this blueprint's own PR if item 06 doesn't yet exist).
- [ ] `infra/secrets/manifest.yaml` exists, lists every credential-bearing backend var applicable to Dev/QA/Staging/Production.
- [ ] `backend/src/noorheroes/core/secrets_bootstrap.py` exists, is unit-tested per §14's table, and is wired into `main.py`'s `lifespan()` ahead of `init_telemetry()`.
- [ ] `Settings` gains exactly one new field (`secrets_provider`); no existing field renamed or removed.
- [ ] `admin-web/src/lib/env.ts` gains the new keys additively; existing exported shape/import surface unchanged.
- [ ] `.gitignore` updated per §9; a local `.env`/`local.properties` genuinely cannot be `git add`-ed without `--force`.
- [ ] `docs/runbooks/secret-rotation.md` exists and documents the rotation + forced-restart procedure and the "no live rotation at MVP" limitation.
- [ ] The canary test (§14) proves the custom gitleaks rules actually fire, not just that the config parses.
- [ ] No real secret exists anywhere in the git history introduced by this blueprint's implementing PR.

---

## 18. Assumptions or decisions the coding agent must follow

1. **Secrets-manager vendor is GCP Secret Manager**, chosen because Cloud Run is Final_Development_Prompt §7's first-listed managed-compute target and GCP Secret Manager requires zero additional infrastructure alongside it. This is this document's concrete implementation default for the "Assumed Requirement" Final_Development_Prompt §14 and Consolidated_Blueprint_v6 §2597/§2612 explicitly leave open — implement against it, but keep the isolation described in §15's "vendor-lock exit path" so a later confirmed switch to AWS Secrets Manager (if the infra team decides otherwise) touches only `secrets_bootstrap.py` and the manifest's `provider` field.
2. **gitleaks is the primary, blocking tool everywhere; trufflehog runs verified-only, also blocking, as a second independent CI gate.** Do not treat trufflehog as optional/advisory — Final_Development_Prompt §3.3's "mandatory" language applies to the secret-scanning *outcome* (nothing leaks), and a two-tool gate is this document's chosen way to satisfy "gitleaks or trufflehog" robustly, per the task's instruction to "specify both with roles" when justified.
3. **`secrets_bootstrap.py` reads secrets once, at process boot.** Live/hot rotation without a restart is explicitly out of scope for this MVP-stage blueprint; do not build a background refresh loop or a Redis-cached secret layer unless a future blueprint explicitly supersedes this one.
4. **Every credential-bearing `.env.example` line uses an obviously-fake placeholder value, never blank-but-plausible or a realistic-looking dummy.** This is a deliberate defense-in-depth choice (§9) independent of the gitleaks allowlist.
5. **The exact field names in `Settings`/`env.ts` in this document (§7) are this document's best-effort reconstruction from the Core setup manuals, which do not enumerate every field verbatim.** Before implementing, the coding agent MUST read the actual current `backend/src/noorheroes/core/settings.py` and `admin-web/src/lib/env.ts` files and reconcile any naming difference — treat those two files as authoritative over this document's assumed names, and update `.env.example`/the manifest to match reality, not the other way around.
6. **AI provider and email provider vendor choices remain open** per Final_Development_Prompt §14 — this document's `.env.example` lists variable names for all plausible candidates (OpenAI/Claude/Gemini/DeepSeek; SES/SendGrid/Postmark) with a single active-provider switch (`AI_PROVIDER`, `EMAIL_PROVIDER`); do not delete the non-chosen candidates' variable names from `.env.example` until the vendor decision is formally confirmed elsewhere, since removing them prematurely would itself be an undocumented scope decision this blueprint isn't authorized to make.
7. **This document does not implement Terraform resources** beyond a minimal placeholder proving the manifest is consumable — do not build out a full `infra/terraform/` module as part of this blueprint; that is item 04's explicit ownership.
8. **Branch protection settings are a GitHub repository configuration, not a file**, and must be applied manually (or via a documented `gh api`/Terraform-for-GitHub call, if the team later automates repo settings) — this document's Definition of Done requires the setting to be *verified*, not merely described.

---

## AI Agent Development Prompt

You are implementing **Phase 1, Infra item 02** of the NoorHeroes monorepo: secrets management, the `.env.example` convention, and mandatory gitleaks + trufflehog secret scanning.

**Stack:** FastAPI backend (`backend/`, `pydantic-settings`-based `core/settings.py` already exists — do not rewrite it), Next.js 15 App Router admin (`admin-web/`, Zod-validated `src/lib/env.ts` already exists — do not rewrite it), Kotlin Multiplatform mobile (`mobile/`, Gradle-based config, `core-security`/`core-datastore` already built — do not modify them), monorepo root (`backend/`, `admin-web/`, `mobile/`, `infra/`, `docs/`, `.github/workflows/`).

**Before writing any code:** read the *actual current* `backend/src/noorheroes/core/settings.py` and `admin-web/src/lib/env.ts` in full. This document's §7 env-var lists are a best-effort reconstruction and are subordinate to whatever those two files actually contain today — reconcile any difference in favor of the real files, per §18 Assumption 5.

**What to build, in this order** (full detail in §13 of this document):
1. `.gitleaks.toml` (root) — extend gitleaks' default ruleset, add the allowlist and two custom rules from §9, verify zero findings against the current tree.
2. `.pre-commit-config.yaml` (root) — add the pinned gitleaks `protect --staged` hook from §13 step 2, additive to any existing pre-commit config already present.
3. Update root `.gitignore` per §9.
4. `backend/.env.example`, `admin-web/.env.example`, `mobile/local.properties.example` — content per §7, reconciled against the real `Settings`/`env.ts` per the note above.
5. `backend/scripts/check_env_example_sync.py` and `admin-web/scripts/check-env-example-sync.ts` — the drift-check scripts from §3.3; each must exit non-zero with a clear message on any key mismatch.
6. `infra/secrets/manifest.yaml` — the secret registry from §6, covering every credential-bearing backend var applicable to Dev/QA/Staging/Production.
7. `backend/src/noorheroes/core/secrets_bootstrap.py` — `load_secrets_into_environ(environment: Environment) -> None` per the interface in §6, `SecretsBootstrapError` exception, no-op for local/`SECRETS_PROVIDER=env`, GCP Secret Manager read for `gcp_secret_manager`.
8. Add exactly one field to `Settings`: `secrets_provider: Literal["env", "gcp_secret_manager"] = "env"`. Do not touch any other field.
9. Modify `backend/src/noorheroes/main.py`: call `load_secrets_into_environ(...)` as the first line of `lifespan()`'s startup half, before `init_telemetry()`.
10. Add the new keys from §7.3 to `admin-web/src/lib/env.ts`, additive only — do not change its existing export shape.
11. `.github/workflows/secret-scan.yml` — exact job spec in §14, both jobs required, no path filter, triggered on every push and PR.
12. `docs/runbooks/secret-rotation.md` — rotation cadence table (from the manifest) plus the forced-restart procedure and the explicit "no live rotation at MVP" note.
13. Write every test in §14's table, including the canary test proving the custom gitleaks rules actually fire (run it in an isolated temp git repo — never stage a real-looking secret in the actual repository's history).
14. Configure GitHub branch protection on `main`: require `gitleaks-scan` and `trufflehog-verified-scan` status checks, enable "Include administrators." Document that this was done (this is a repo setting, not a diffable file).

**Hard requirements — do not deviate:**
- Never place a secret value in any committed file, including `.env.example` placeholders (§18 Assumption 4) — every placeholder must be obviously fake.
- Never rename or remove an existing `Settings` field or an existing `env.ts` schema key — additive changes only.
- Never modify `core-security` or `core-datastore` in the mobile module.
- Never assign a secret to a `NEXT_PUBLIC_*`-prefixed variable in admin-web — this is a hard, non-negotiable rule (§9), not a lint suggestion.
- Both `gitleaks-scan` and `trufflehog-verified-scan` must be blocking, required status checks with admin bypass disabled — a passing pre-commit hook alone does not satisfy this blueprint's Definition of Done.
- Do not build a live/hot secret-rotation mechanism — read-once-at-boot is the explicit, documented MVP scope (§18 Assumption 3).
- Do not write Terraform resource definitions beyond the minimal stub described in §13 step 8 — full IaC is item 04's scope, not this blueprint's.

**How to verify you're done:** walk every checkbox in this document's §17 Definition of Done in order, in a single pass, and confirm each is literally true against the repository state you produced — including the manual branch-protection verification (open a scratch PR with a deliberately fake secret, confirm both jobs fail and merge is blocked even for an admin account, then delete the scratch branch). Run every test listed in §14's table and confirm all pass. Run `gitleaks detect --source . --config .gitleaks.toml` against the full repository one final time and confirm zero findings before considering this blueprint complete.
