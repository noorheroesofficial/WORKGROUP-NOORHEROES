# Phase 1 — Environment Tiers & Provisioning

**Blueprint ID:** `Development_Blueprints.Phase1_Infra_Config.Infra.01-environment-tiers-provisioning`
**Platform:** Infra
**Phase:** Phase 1 — Infrastructure & Configuration
**Depends on:** Phase 0 — Repo Foundation (monorepo scaffold, CI skeleton, coding standards) — **already complete**
**Consumed by:** `Infra.02` (secrets management), `Infra.03` (local Docker Compose stack), `Infra.04` (Terraform IaC baseline), `Infra.05` (observability bootstrap), `CI_CD.06`–`CI_CD.10` (all CI/CD pipeline stages), and every later feature blueprint that declares an environment variable, a migration, or a deploy target.
**Governing source documents:** `NoorHeroes_Final_Development_Prompt.md` §3 (Environment, Dependency & Secrets Management), §7 (Docker, Deployment & Infrastructure); `NoorHeroes_Consolidated_Blueprint_v6.md` §2.9 (Infrastructure), §19 (Deployment & Infrastructure), §14.7 (Disaster Recovery); `FAST-API-INSTRUCTIONS.md` (`core/settings.py`, `Environment` StrEnum); `noorheroes-admin/NEXT-JS-INSTRUCTIONS.md` (Zod env validation, zero-token-persistence architecture).

---

## 1. Objective and Purpose

Define and provision the **five environment tiers** — **Local, CI, Dev-QA, Staging, Production** — that every other piece of NoorHeroes infrastructure, CI/CD stage, and feature blueprint is built on top of. This file is the single source of truth for:

- What each tier is *for*, who/what runs in it, and how long it lives.
- What infrastructure each tier runs on (local Docker, ephemeral CI runners, managed cloud).
- The **naming and isolation scheme** that keeps the tiers from ever touching each other's data, secrets, or traffic.
- What artifact is built once and **promoted** unchanged between tiers (backend/admin-web container images) versus what is **rebuilt per tier** (mobile build variants).
- The exact `Settings`/env-var contract each tier must satisfy so the already-implemented `pydantic-settings` `Settings` class (`src/noorheroes/core/settings.py`) and the already-implemented Next.js Zod env validation boot correctly in every tier without code changes.

This file does **not** build the secrets-rotation mechanism (`Infra.02`), the local Compose stack's service definitions (`Infra.03`), the Terraform modules themselves (`Infra.04`), the observability collectors (`Infra.05`), or any CI/CD pipeline stage (`CI_CD.06`–`10`) — it defines the tier model and contracts those files implement against. Treat every cross-reference below as "owned elsewhere, contract fixed here."

**Why this matters first:** per `NoorHeroes_Final_Development_Prompt.md` §10 (Phase 0 exit criteria) and the Repository Foundation status, backend/mobile/admin-web application code is already built and tested against a *local* environment only. Nothing in the corpus provisions Dev-QA, Staging, or Production, and no naming/isolation convention exists yet for any of them. Every later Terraform module, CI/CD deploy stage, and secrets policy needs this contract to target — building any of those first would mean inventing (and likely re-inventing, inconsistently) the tier model ad hoc.

---

## 2. Scope and Requirements

### 2.1 In scope

- The definitive list and definition of the 5 tiers (§4).
- Cloud provider/topology recommendation and resource-naming convention for Dev-QA/Staging/Production (§4, §5).
- The `infra/environments/{local,ci,dev-qa,staging,production}/` folder layout and what file belongs in each (§5).
- The full `Settings`-class configuration contract (env var names, types, per-tier example values) that backend code must read (§6, §7).
- The Next.js Admin Portal's equivalent env contract (§6, §12).
- The mobile Gradle build-variant → tier mapping (§12).
- Database/Redis/object-storage isolation per tier (§8).
- Auth/security posture differences (and *non*-differences — Staging must not be weaker than Production) per tier (§9).
- Tier lifecycle (creation, redeploy cadence, teardown, data reset policy) (§11).
- Promotion mechanics: what artifact moves from Staging to Production and what does not (§4.6, §13).

### 2.2 Out of scope (owned by sibling files — do not duplicate)

| Concern | Owning file |
|---|---|
| `.env.example` content, secret rotation policy, gitleaks/trufflehog wiring | `Infra.02-secrets-management-env-example-gitleaks.md` |
| Local Docker Compose service definitions (Postgres/Redis/R2-emulation/hot-reload) | `Infra.03-docker-compose-local-dev-stack.md` |
| Terraform module code, GCP/AWS resource provisioning, remote state backend | `Infra.04-terraform-iac-baseline-staging.md` |
| OpenTelemetry/Prometheus/Grafana/Sentry wiring | `Infra.05-observability-stack-bootstrap.md` |
| CI pipeline stage implementation (lint→test→build, security scans, staging deploy, prod promotion) | `CI_CD.06`–`CI_CD.09` |
| Feature-flag platform + dual-sign-off gate | `CI_CD.10-feature-flag-platform-dual-signoff-config.md` |
| Blue/green and canary production deploy mechanics | `Phase11_CICD_Deployment.Infra.01-blue-green-canary-deployment-strategy.md` |
| Kubernetes migration path | `Phase11_CICD_Deployment.Infra.02-k8s-migration-path-cloud-run-to-k8s.md` |

### 2.3 Requirements this file must satisfy

1. Name all 5 tiers explicitly and unambiguously (no synonyms drifting in later files).
2. Give every tier a concrete infra target — no tier is left as "TBD."
3. Define a resource-naming convention collision-proof across all 5 tiers.
4. Reconcile the 5-tier operational model with the **already-implemented** 4-value `Environment` StrEnum (`LOCAL`, `DEVELOPMENT`, `STAGING`, `PRODUCTION`) in `core/settings.py` — **without modifying that enum** (see §18, Decision 1).
5. Specify exactly which config values differ per tier and which must never differ (e.g., JWT algorithm is constant; JWT signing key is tier-unique).
6. Define what "promotion" means for each of the three consuming platforms (backend, admin-web, mobile) since they are not identical.

---

## 3. Technical Implementation Details

### 3.1 Design principles (apply to every decision below)

- **Blast-radius containment over convenience.** Dev-QA, Staging, and Production are hard-isolated (separate cloud projects, separate databases, separate secrets, separate object-storage buckets). A compromised or misconfigured Dev-QA credential must be structurally incapable of touching Staging or Production data.
- **Staging must be a valid security-testing target.** Per `NoorHeroes_Final_Development_Prompt.md` §7 and `NoorHeroes_Consolidated_Blueprint_v6.md` §19.1, Staging exists to run penetration tests and incident-response tabletop drills. This means Staging runs the **exact same auth/authorization code path as Production, with zero test-only bypasses** — any test-mode convenience (fixed OTP, mocked MFA, etc.) is permitted in Local/CI/Dev-QA only, never in Staging or Production. This is a hard rule, not a convention (see §9.4).
- **One build, many deploys — for backend and admin-web.** A container image is built exactly once per commit SHA in CI and the *same immutable image* is deployed to Dev-QA, then Staging, then (on manual promotion) Production. Nothing is rebuilt from source between tiers. Mobile does not follow this model — see §4.6.
- **No tier invents its own config schema.** Every tier reads the same `Settings` class / same Zod schema; only *values* differ per tier via env injection, never the schema shape. A field that exists in Production's config must exist (even if empty/mocked) in every other tier's config — this is what keeps `Settings()` from raising `ValidationError` unpredictably per tier.
- **Fail closed on missing config, never fail open.** A required setting missing at boot crashes the process in every tier including Local — matching the platform's existing "fail closed" posture for the content-safety pipeline (`NoorHeroes_Consolidated_Blueprint_v6.md` §13.5).
- **Synthetic data only below Production.** Dev-QA and Staging are seeded exclusively with anonymized/synthetic data generated by the backend's existing `factory_boy`/`polyfactory` test factories (`tests/conftest.py`). Real parent/child PII is never copied into Dev-QA or Staging under any circumstance — this is a COPPA/GDPR data-minimization requirement, not an operational preference.

### 3.2 The 5 tiers, one line each

| # | Tier | Slug | Lives on |
|---|---|---|---|
| 1 | **Local** | `local` | Individual developer machine, Docker Compose |
| 2 | **CI** | `ci` | Ephemeral GitHub Actions runner, per-workflow-run containers |
| 3 | **Dev-QA** | `dev-qa` | Shared, persistent cloud environment (Cloud Run/Fargate + managed Postgres/Redis) |
| 4 | **Staging** | `staging` | Persistent cloud environment mirroring Production topology at smaller scale |
| 5 | **Production** | `production` | Persistent cloud environment, live traffic |

---

## 4. Architecture and Component Responsibilities

### 4.1 Cloud provider and topology

The source stack target names **Cloud Run** first among the acceptable managed-container platforms (`NoorHeroes_Final_Development_Prompt.md` §7: "AWS ECS Fargate, Google Cloud Run, or a managed Kubernetes"). This file uses **Google Cloud Platform (Cloud Run)** as the concrete worked example throughout — the AWS Fargate equivalent is given alongside every GCP-specific resource so a team choosing AWS instead can substitute directly. **The binding provider decision is owned by `Infra.04`** (Terraform baseline); this file's naming/isolation model is provider-agnostic in structure and must not be contradicted by whichever provider `Infra.04` ultimately selects.

**Topology: hub-and-spoke, one project per persistent tier.**

```mermaid
flowchart TB
    subgraph HUB["noorheroes-platform (hub project)"]
        AR["Artifact Registry\nnoorheroes-images"]
        DNS["Cloud DNS zone\nnoorheroes.com"]
        CISA["CI deploy service account\n(Workload Identity Federation)"]
    end

    subgraph DEVQA["noorheroes-devqa (spoke project)"]
        CRD["Cloud Run: noorheroes-api-devqa\nnoorheroes-admin-devqa"]
        PGD["Cloud SQL: noorheroes-pg-devqa"]
        RD["Memorystore: noorheroes-redis-devqa"]
    end

    subgraph STG["noorheroes-staging (spoke project)"]
        CRS["Cloud Run: noorheroes-api-staging\nnoorheroes-admin-staging"]
        PGS["Cloud SQL: noorheroes-pg-staging"]
        RS["Memorystore: noorheroes-redis-staging"]
    end

    subgraph PROD["noorheroes-prod (spoke project)"]
        CRP["Cloud Run: noorheroes-api-prod\nnoorheroes-admin-prod"]
        PGP["Cloud SQL: noorheroes-pg-prod"]
        RP["Memorystore: noorheroes-redis-prod"]
    end

    AR -->|pulls image by SHA| CRD
    AR -->|pulls image by SHA| CRS
    AR -->|pulls exact promoted SHA| CRP
    CISA -.->|deploys via WIF, no long-lived keys| CRD
    CISA -.->|deploys via WIF, no long-lived keys| CRS
    CISA -.->|deploys via manual-gated WIF| CRP

    R2[("Cloudflare R2\n(separate account, not GCP)\nnoorheroes-media-devqa\nnoorheroes-media-staging\nnoorheroes-media-prod")]
    CRD -.-> R2
    CRS -.-> R2
    CRP -.-> R2
```

- **Hub project (`noorheroes-platform`):** holds the shared Artifact Registry repo (one repo, images tagged per app + git SHA), the Cloud DNS zone for `noorheroes.com`, and the CI deploy identity (Workload Identity Federation — GitHub Actions authenticates without a long-lived JSON key). Nothing customer-facing runs here.
- **Spoke projects (`noorheroes-devqa`, `noorheroes-staging`, `noorheroes-prod`):** one GCP project per persistent tier. Each spoke project has its own VPC, its own Cloud SQL instance, its own Memorystore Redis instance, its own IAM bindings, and its own Secret Manager secrets. A credential scoped to the Dev-QA project has **zero** IAM permissions in the Staging or Prod projects — this is enforced at the IAM/organization-policy level, not by convention.
- **AWS equivalents** (if `Infra.04` selects AWS instead): hub → a shared "tooling" AWS account with ECR + Route 53 hosted zone; spokes → one AWS account (or at minimum one VPC + IAM boundary) per tier, ECS Fargate services, RDS Postgres, ElastiCache Redis, Secrets Manager, cross-account deploy role assumed via GitHub's OIDC provider (the IAM equivalent of GCP's WIF).
- **Local and CI have no cloud project.** They are covered entirely by Docker Compose (`Infra.03`) and ephemeral CI-runner containers respectively — see §4.2–§4.3.

### 4.2 Local tier — architecture

Runs entirely on the developer's machine via `infra/docker-compose.yml` (already named in the existing monorepo tree, service definitions owned by `Infra.03`). Components: Postgres 16, Redis, the FastAPI backend (hot-reload via `uvicorn --reload`), the Next.js admin-web (hot-reload via `next dev`), and a local S3-compatible R2 emulator (MinIO or `cloudflare/wrangler r2` dev mode — final choice owned by `Infra.03`). The Android app is **not** containerized; it runs on an emulator/device and points at the host machine's exposed backend port.

Isolation: per-developer machine boundary. No shared state between developers. Docker Compose project name defaults to the directory name (`noorheroes`), so two developers on the same LAN never collide — each `docker compose` invocation is scoped to that developer's own Docker daemon.

### 4.3 CI tier — architecture

Runs entirely inside a single GitHub Actions job's ephemeral runner (see `NoorHeroes_Final_Development_Prompt.md` §6). Two acceptable mechanisms, matching the already-documented backend testing harness:

- **Testcontainers** (preferred, matches `tests/conftest.py`'s already-built fixtures): the test suite itself spins up a throwaway Postgres and Redis container per test session via the `testcontainers` Python library, on host-assigned random ports. No `docker-compose.ci.yml` orchestration needed for these — the test process owns the container lifecycle directly.
- **`docker-compose.ci.yml`** (owned by `Infra.03`/`CI_CD.06`): used for any CI job that needs a longer-lived multi-service stack (e.g., an API-contract test hitting a running `uvicorn` process rather than an in-process `TestClient`). Uses `tmpfs` volumes only — nothing persists past `docker compose down -v` at job end.

Every CI run gets a **fresh** Postgres/Redis with zero data carried over from any previous run — this is what makes CI runs reproducible and immune to state leakage between PRs (`NoorHeroes_Final_Development_Prompt.md` §3: "no shared mutable state between runs"). CI has no persistent cloud footprint of its own; the only cloud interaction a CI job has is (a) pulling/pushing images to the hub project's Artifact Registry, and (b) — for the Dev-QA/Staging deploy stages owned by `CI_CD.08` — authenticating via Workload Identity Federation to deploy into those spoke projects. CI itself has no dedicated GCP project.

### 4.4 Dev-QA tier — architecture

Runs in the `noorheroes-devqa` GCP spoke project: Cloud Run services for backend + admin-web, one Cloud SQL Postgres instance, one Memorystore Redis instance, one dedicated Cloudflare R2 bucket. Purpose: integration testing and manual QA sign-off ahead of a release, per `NoorHeroes_Final_Development_Prompt.md` §3. Deploy cadence is **decoupled from the merge-to-main pipeline** (see §11.2 and Decision 5 in §18) — Dev-QA does not need to track every single commit, only a periodically-refreshed target QA can rely on staying put during a manual test pass.

### 4.5 Staging tier — architecture

Runs in the `noorheroes-staging` GCP spoke project, structurally identical to Production (same Cloud Run service definitions, same Cloud SQL machine tier *scaled down*, same Memorystore tier scaled down, same IAM/WAF/rate-limit configuration) so that penetration tests and incident-response tabletop drills exercise the real production code path (`NoorHeroes_Consolidated_Blueprint_v6.md` §19.1). Auto-deploys on every merge to `main` (pipeline stage 9 of the 13-stage CI/CD pipeline, `CI_CD.08`). Runs the automated E2E smoke suite (stage 10) immediately after deploy.

**Reconciling `infra/docker-compose.staging.yml`:** the existing monorepo tree (`NoorHeroes_Final_Development_Prompt.md` §2.1) already names `infra/docker-compose.staging.yml`. This file is **not** the deployment mechanism for the Staging tier — the Staging tier is a managed Cloud Run environment provisioned by Terraform (`Infra.04`) and deployed by CI (`CI_CD.08`), exactly like Production. `docker-compose.staging.yml` is repurposed as a **local reproduction harness**: a developer who needs to debug a Staging-only issue can run `docker compose -f infra/docker-compose.yml -f infra/docker-compose.staging.yml up` to get a local stack configured with Staging-equivalent env values (feature flags, rate-limit thresholds, CORS origins) without touching the real Staging database. See Decision 3 in §18.

### 4.6 Production tier — architecture

Runs in the `noorheroes-prod` GCP spoke project. Deploy requires the manual promotion gate (pipeline stage 11) — a human clicks "deploy" in the GitHub Actions UI (a `production` GitHub Environment with required reviewers). The artifact deployed is the **exact same container image digest** already running in Staging and already verified by the E2E smoke suite — Production is never built from source directly. Blue/green or canary rollout mechanics (5% → 25% → 100%) are owned by `Phase11_CICD_Deployment.Infra.01`; this file only establishes that Production's deploy input is an immutable, pre-verified artifact, never a fresh build.

**What "promotion" means per platform:**

| Platform | Unit promoted | Mechanism |
|---|---|---|
| Backend (FastAPI) | Container image, tagged `backend:{git-sha}` in Artifact Registry | Same image redeployed to Dev-QA → Staging → (manual gate) → Production. Config differs only via env vars/secrets injected by Cloud Run per project. |
| Admin-web (Next.js) | Container image, tagged `admin-web:{git-sha}` (Next.js `standalone` output) | Identical promotion model to backend. |
| Mobile (Android/KMP) | **Not promoted as a binary.** Each tier is a distinct signed build from a distinct Gradle product flavor (`dev`/`qa`/`staging`/`prod`) built fresh for that tier. | The `prod` flavor's release build is what ships to Play Console, using Play Console's own staged rollout (5%→25%→100%) — a separate mechanism from the backend/admin-web image promotion described above. See §12.3. |

---

## 5. Folder / File Structure

Extends the existing `infra/` tree from `NoorHeroes_Final_Development_Prompt.md` §2.1 (do not restructure what already exists there — add to it):

```
infra/
├── docker-compose.yml                  # EXISTING — local dev stack (owned by Infra.03)
├── docker-compose.staging.yml          # EXISTING — repurposed: local reproduction of Staging-equivalent
│                                        #   config only (see §4.5); NOT the Staging deploy mechanism
├── environments/                       # NEW — this file's primary deliverable
│   ├── local/
│   │   ├── README.md                     # what Local is, how to boot it, links to Infra.03
│   │   └── backend.env.example           # NOT the real .env.example (that's Infra.02's job) —
│   │                                     #   this is the Local-tier-specific subset/defaults
│   ├── ci/
│   │   ├── README.md                     # what CI tier is, ephemerality guarantees
│   │   └── backend.env.ci.example        # env values a CI job injects (non-secret placeholders)
│   ├── dev-qa/
│   │   ├── README.md                     # purpose, deploy cadence, data-reset policy
│   │   ├── backend.env.dev-qa.example    # non-secret config values (secrets live in Secret Manager,
│   │   │                                 #   see Infra.02) — this file documents KEYS and NON-SECRET
│   │   │                                 #   values only (URLs, flags, limits), never real credentials
│   │   ├── admin-web.env.dev-qa.example
│   │   └── terraform.tfvars.example      # non-secret Terraform input variables for this tier
│   │                                     #   (module code itself lives in infra/terraform/, owned by Infra.04)
│   ├── staging/
│   │   ├── README.md
│   │   ├── backend.env.staging.example
│   │   ├── admin-web.env.staging.example
│   │   └── terraform.tfvars.example
│   └── production/
│       ├── README.md
│       ├── backend.env.production.example
│       ├── admin-web.env.production.example
│       └── terraform.tfvars.example
├── terraform/                          # EXISTING (empty until Infra.04) — modules consume
│                                        #   infra/environments/<tier>/terraform.tfvars
├── k8s/                                 # EXISTING — untouched, Phase 6 (Scale) only
└── ci/                                  # EXISTING — shared CI config fragments (owned by CI_CD.06+)
```

**Rule enforced by this structure:** any `*.env*.example` file under `infra/environments/` contains **keys and non-secret values only** — URLs, feature-flag defaults, numeric limits, log levels. Real secret values (DB passwords, JWT signing keys, R2 access keys) are never committed anywhere, including as "examples" — they live exclusively in the secret store defined per tier in §8.4/§9.3, whose lifecycle is `Infra.02`'s responsibility. This file's `*.example` files exist so a developer or CI job can see *which keys* a tier expects without ever seeing a real value.

---

## 6. APIs, Models, Interfaces, and Data Flow

### 6.1 The `Environment` enum contract (backend)

`src/noorheroes/core/settings.py` already implements:

```python
class Environment(StrEnum):
    LOCAL = "local"
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
```

This enum has **4 values**, not 5. This file's 5 operational tiers map onto it as follows (do not add a 5th enum value — see Decision 1, §18):

| Operational tier | `Environment` value at runtime | Rationale |
|---|---|---|
| Local | `local` | 1:1 |
| CI | `local` | CI is an ephemeral, code-identical rerun of "local" behavior (debug on, permissive CORS, no external secrets) — distinguished from a developer's Local only by *which* env values are injected (CI's DB/Redis point at the ephemeral CI containers), never by application logic branching |
| Dev-QA | `development` | Dev-QA is the "shared development/QA" target the `DEVELOPMENT` value was named for |
| Staging | `staging` | 1:1 |
| Production | `production` | 1:1 |

Any code that branches on `settings.environment` therefore has exactly 4 cases to handle, and CI is guaranteed to exercise the same code path as Local (the cheapest, fastest-iterating tier) — this is intentional: CI should catch Local-tier bugs, not a mysterious fifth behavior no developer ever runs locally.

### 6.2 `Settings` field contract

The exact field names below are this file's concrete proposal (the source `FAST-API-INSTRUCTIONS.md` manual documents that `Settings` exists and is a `pydantic-settings`-based singleton, but does not enumerate field names). **If `core/settings.py` already defines different exact field names for any of these, keep the existing names — this table exists so no tier is left without a defined value for a concern that must exist; field-name reconciliation is additive only, never a rename of already-implemented fields.**

| Field | Type | Local | CI | Dev-QA | Staging | Production |
|---|---|---|---|---|---|---|
| `environment` | `Environment` | `local` | `local` | `development` | `staging` | `production` |
| `debug` | `bool` | `true` | `true` | `true` | `false` | `false` |
| `database_url` | `PostgresDsn` | `postgresql+asyncpg://noorheroes:noorheroes@localhost:5432/noorheroes` | Testcontainers-assigned, injected at runtime | Cloud SQL private-IP DSN, from Secret Manager | Cloud SQL private-IP DSN, from Secret Manager | Cloud SQL private-IP DSN, from Secret Manager |
| `database_pool_size` | `int` | `5` | `5` | `10` | `20` | `40` |
| `redis_url` | `RedisDsn` | `redis://localhost:6379/0` | Testcontainers-assigned | Memorystore private-IP URL, from Secret Manager | same pattern | same pattern |
| `celery_broker_url` | `RedisDsn` | same Redis, db `1` | same Redis, db `1` | same Memorystore, db `1` | same pattern | same pattern |
| `jwt_signing_key` | `SecretStr` | fixed dev-only value in `.env.example` (never used outside Local) | random-per-run, generated in CI job | Secret Manager, tier-unique | Secret Manager, tier-unique | Secret Manager, tier-unique, highest rotation priority |
| `jwt_algorithm` | `str` | `HS256` | `HS256` | `HS256` | `HS256` | `HS256` — **constant across all tiers, never a per-tier variable** |
| `jwt_access_token_ttl_seconds` | `int` | `900` | `900` | `900` | `900` | `900` — constant |
| `jwt_refresh_token_ttl_seconds` | `int` | `2592000` (30d) | `2592000` | `2592000` | `2592000` | `2592000` — constant |
| `r2_account_id` / `r2_access_key_id` / `r2_secret_access_key` | `SecretStr` | MinIO/emulator dummy creds | MinIO/emulator dummy creds | Secret Manager, scoped to `noorheroes-media-devqa` bucket only | Secret Manager, scoped to `noorheroes-media-staging` bucket only | Secret Manager, scoped to `noorheroes-media-prod` bucket only |
| `r2_bucket_name` | `str` | `noorheroes-media-local` (emulator) | `noorheroes-media-ci` (emulator) | `noorheroes-media-devqa` | `noorheroes-media-staging` | `noorheroes-media-prod` |
| `r2_endpoint_url` | `str` | `http://localhost:9000` (MinIO) | `http://minio:9000` (compose service name) | Cloudflare R2 account endpoint | Cloudflare R2 account endpoint | Cloudflare R2 account endpoint |
| `cdn_base_url` | `str` | `http://localhost:9000` | `http://minio:9000` | `https://cdn-devqa.noorheroes.com` | `https://cdn-staging.noorheroes.com` | `https://cdn.noorheroes.com` |
| `cors_allowed_origins` | `list[str]` | `["http://localhost:3000"]` | `["http://localhost:3000"]` | `["https://admin-devqa.noorheroes.com"]` | `["https://admin-staging.noorheroes.com"]` | `["https://admin.noorheroes.com", "https://account.noorheroes.com"]` |
| `rate_limit_enabled` | `bool` | `false` (or relaxed) | `false` | `true` | `true` | `true` — Staging/Prod always match |
| `sentry_dsn` | `str \| None` | `None` | `None` | tier-specific project DSN | tier-specific project DSN | tier-specific project DSN |
| `otel_exporter_otlp_endpoint` | `str \| None` | `None` (no-op tracer) | `None` | collector endpoint, `noorheroes-devqa` | collector endpoint, `noorheroes-staging` | collector endpoint, `noorheroes-prod` |
| `log_level` | `str` | `DEBUG` | `DEBUG` | `INFO` | `INFO` | `WARNING` (app), `INFO` (security/audit events always logged regardless) |
| `secrets_backend` | `Literal["dotenv","gcp_secret_manager"]` | `dotenv` | `dotenv` (CI injects via GitHub Actions secrets → env, no Secret Manager call) | `gcp_secret_manager` | `gcp_secret_manager` | `gcp_secret_manager` |
| `gcp_project_id` | `str \| None` | `None` | `None` | `noorheroes-devqa` | `noorheroes-staging` | `noorheroes-prod` |
| `test_mode_auth_bypass_enabled` | `bool` | `true` (opt-in per test) | `true` | `true` (QA automation only) | **`false` — hard-coded false, not configurable via env in this tier** | **`false` — hard-coded false, not configurable via env in this tier** |

The last row is deliberately phrased as "hard-coded false, not configurable via env" — see §9.4 for why this must be a compile-time/deploy-time guarantee, not merely a default.

### 6.3 Admin-web env contract (Next.js)

Per `NEXT-JS-INSTRUCTIONS.md`, the Admin Portal validates its environment via a Zod schema (fails the build fast on a missing/malformed var) and never talks to Postgres directly — all data access is server-side calls to the FastAPI backend, matching the zero-token-persistence architecture (access tokens live only in server memory; refresh tokens are `httpOnly` cookies the backend sets directly).

| Var | Scope | Local | CI | Dev-QA | Staging | Production |
|---|---|---|---|---|---|---|
| `API_BASE_URL` | server-only | `http://localhost:8000/v1` | `http://localhost:8000/v1` (or the CI backend container's compose DNS name) | `https://api-devqa.noorheroes.com/v1` | `https://api-staging.noorheroes.com/v1` | `https://api.noorheroes.com/v1` |
| `NEXT_PUBLIC_APP_ENV` | public (browser-visible label only, never a secret) | `local` | `local` | `dev-qa` | `staging` | `production` |
| `NEXT_PUBLIC_SENTRY_DSN` | public | empty | empty | tier DSN | tier DSN | tier DSN |
| `SENTRY_DSN` (server) | server-only | empty | empty | tier DSN | tier DSN | tier DSN |
| `SESSION_COOKIE_DOMAIN` | server-only | `localhost` | `localhost` | `admin-devqa.noorheroes.com` | `admin-staging.noorheroes.com` | `admin.noorheroes.com` |

`NEXT_PUBLIC_APP_ENV` exists specifically so the Admin Portal can render a persistent "You are in Staging" banner — required so an operator can never mistake Staging for Production during a pen-test drill or QA session (a direct mitigation for the accidental-content-publication runbook named in `NoorHeroes_Consolidated_Blueprint_v6.md` §20.3).

---

## 7. Dependencies and Configuration Requirements

### 7.1 Tooling prerequisites (once, per operator/CI runner)

- Terraform ≥ 1.7 (module code owned by `Infra.04`; this file's `terraform.tfvars.example` files are its input contract).
- `gcloud` CLI (or `aws` CLI if the team selects AWS in `Infra.04`), authenticated with permission to create/read the hub + 3 spoke projects.
- Docker + Docker Compose v2 (Local/CI, owned by `Infra.03`).
- GitHub repository admin access, to configure the `staging`, `production`, and (optionally) `dev-qa` **GitHub Environments** with their protection rules and environment-scoped secrets (§9.3).
- DNS control over `noorheroes.com` (Cloud DNS zone lives in the hub project; delegate the zone from the domain registrar once).
- A Cloudflare account with R2 enabled (separate from the GCP/AWS account entirely — R2 buckets and API tokens are provisioned per tier, see §8.3).

### 7.2 GitHub Environments configuration (this is what implements the manual-promotion gate)

| GitHub Environment name | Maps to tier | Protection rule | Secrets scope |
|---|---|---|---|
| *(none — CI has no GitHub Environment)* | CI | n/a | Repo-level `Actions secrets`, only test/dummy values |
| `dev-qa` | Dev-QA | none (auto-deploy on schedule/dispatch) | Environment secrets scoped to `noorheroes-devqa` |
| `staging` | Staging | none (auto-deploy on merge to `main`) | Environment secrets scoped to `noorheroes-staging` |
| `production` | Production | **required reviewers ≥ 1**, deployment branch restricted to `main` only | Environment secrets scoped to `noorheroes-prod` |

This table is the concrete implementation of `NoorHeroes_Final_Development_Prompt.md` §6 pipeline stage 11 ("Manual promotion gate to production — a human clicks deploy"). The full pipeline stage wiring is `CI_CD.09`'s responsibility; this file fixes which GitHub Environment name corresponds to which tier's isolation boundary so that file doesn't have to invent it.

---

## 8. Database / Storage Requirements

### 8.1 PostgreSQL

| Tier | Instance | Isolation | Backup |
|---|---|---|---|
| Local | Docker Compose Postgres 16 container, named volume | Per-developer machine | None (disposable) |
| CI | Testcontainers/Compose Postgres 16, `tmpfs`, ephemeral | Per-job, destroyed at job end | None (disposable) |
| Dev-QA | Cloud SQL for PostgreSQL 16, instance `noorheroes-pg-devqa`, single logical DB `noorheroes` | Own Cloud SQL instance in `noorheroes-devqa` project, private VPC only, no public IP | Automated daily snapshot, 7-day retention, **not** subject to the RPO/RTO drill requirement (synthetic data only — see §8.5) |
| Staging | Cloud SQL for PostgreSQL 16, instance `noorheroes-pg-staging` | Own instance in `noorheroes-staging` project, private VPC only | Automated daily snapshot + point-in-time recovery enabled, included in restore-drill rotation (mirrors Prod procedure so drills are realistic) |
| Production | Cloud SQL for PostgreSQL 16, instance `noorheroes-pg-prod`, HA (regional) configuration | Own instance in `noorheroes-prod` project, private VPC only, no public IP ever | Continuous WAL archiving + automated daily snapshot, point-in-time recovery, monthly tested restore drill (§8.5) |

Alembic migrations run as a **distinct pipeline step**, never auto-applied silently (`NoorHeroes_Consolidated_Blueprint_v6.md` §19.2) — the migration-runner mechanics belong to `CI_CD.08`/`CI_CD.09`; this file only fixes that each tier's migration step targets that tier's own Cloud SQL instance and never another tier's.

### 8.2 Redis

| Tier | Instance | Databases used |
|---|---|---|
| Local | Compose Redis container | db 0 = cache/rate-limit, db 1 = Celery broker/result backend, db 2 = auth denylist/OTP session state |
| CI | Ephemeral Testcontainers/Compose Redis | same db layout |
| Dev-QA | Memorystore instance `noorheroes-redis-devqa` | same db layout |
| Staging | Memorystore instance `noorheroes-redis-staging` | same db layout |
| Production | Memorystore instance `noorheroes-redis-prod`, HA tier | same db layout |

Per `NoorHeroes_Final_Development_Prompt.md` §21 cost guidance, one Redis instance serves cache + rate-limit + Celery-broker workloads combined per tier at this scale — split into separate instances only if a real eviction-pressure conflict is observed (an `Infra.04`/ops decision, not a Phase-1 default).

### 8.3 Object storage (Cloudflare R2)

One R2 bucket per persistent tier, each with its own scoped API token (least privilege — a Dev-QA token cannot read/write the Staging or Production bucket):

| Tier | Bucket | Public marketing-asset path |
|---|---|---|
| Local | MinIO/emulator bucket `noorheroes-media-local` (owned by `Infra.03`) | n/a |
| CI | MinIO/emulator bucket `noorheroes-media-ci` | n/a |
| Dev-QA | `noorheroes-media-devqa` | `noorheroes-media-devqa/public/` |
| Staging | `noorheroes-media-staging` | `noorheroes-media-staging/public/` |
| Production | `noorheroes-media-prod` | `noorheroes-media-prod/public/` |

Per `NoorHeroes_Consolidated_Blueprint_v6.md` §13.6, the public marketing-asset path is a **separate, clearly delineated prefix** from authenticated child-facing content within each tier's bucket, so a misconfiguration in one cannot expose the other — this separation is per-tier, not shared across tiers.

### 8.4 Secret store

| Tier | Backend |
|---|---|
| Local | `.env` file, git-ignored (`Infra.02` owns `.env.example` content) |
| CI | GitHub Actions repository-level `Actions secrets` (test/dummy values only — no real vendor credentials ever needed for unit/integration tests against ephemeral containers) |
| Dev-QA | GCP Secret Manager in `noorheroes-devqa`, read by Cloud Run's native Secret Manager env-var binding at container start |
| Staging | GCP Secret Manager in `noorheroes-staging`, same binding mechanism |
| Production | GCP Secret Manager in `noorheroes-prod`, same binding mechanism, highest rotation priority (see `Infra.02`) |

### 8.5 Data-reset and DR policy per tier

- **Local/CI:** fully disposable, no policy needed.
- **Dev-QA:** persistent between deploys; full reseed (synthetic data only, via the backend's existing test factories run as a seed script) on a **weekly** schedule to prevent unbounded QA data growth/drift, plus on-demand reseed via a manual workflow.
- **Staging:** persistent between deploys; Alembic migrations apply forward only, no destructive reseed by default. An on-demand "reset to clean synthetic baseline" runbook operation exists for use immediately before a pen-test cycle or IR tabletop drill, so drills start from a known state.
- **Production:** the durable system of record. RPO/RTO targets and drill cadence — see §15.5/§18 Decision 4 (numeric targets are still an **open decision pending stakeholder confirmation** per both source documents; this file adopts `NoorHeroes_Final_Development_Prompt.md`'s proposed **RPO ≤ 15 minutes (continuous WAL archiving) / RTO ≤ 1 hour** as the working target, with `NoorHeroes_Consolidated_Blueprint_v6.md`'s looser **RPO ≤ 1 hour / RTO ≤ 4 hours** as the documented fallback minimum if the tighter target proves operationally unachievable at current team size — both are provisional until the first DR drill, per §14.7 of the Blueprint).

---

## 9. Authentication, Authorization, Validation, and Security Considerations

### 9.1 Constant across every tier (never a per-tier variable)

- The canonical JWT claim schema (`sub, family_id, mode, child_id?, scopes, device_id, auth_time, consent_version, session_id`) — one Pydantic model, one definition, in every tier.
- JWT algorithm (`HS256`) and token TTLs (§6.2 table).
- Argon2id for every PIN/pattern credential hash, in every tier, including Local/CI — a fast-hash function must never exist anywhere in the credential path regardless of tier (`NoorHeroes_Final_Development_Prompt.md` §9 item 4). The architectural test proving this (owned by the Security Baseline blueprint) runs against every tier's built artifact, not just Production's.
- The gateway-makes-zero-authorization-decisions rule and the domain-service re-verification rule apply identically in every tier — there is no "relaxed auth mode" tier. What varies is *credential delivery convenience* (§9.4), never *authorization logic*.

### 9.2 Per-tier JWT signing keys

Every persistent tier (Dev-QA, Staging, Production) has its **own, independently generated** JWT signing key, stored only in that tier's Secret Manager. A token minted in Staging must be structurally incapable of validating against Production's key (and vice versa) — this is what makes a Staging credential leak a Staging-only incident, never a Production one.

### 9.3 IAM boundary per tier

- Each spoke GCP project (`noorheroes-devqa`/`-staging`/`-prod`) has its own IAM policy. A human or service account granted access to Dev-QA is **not** automatically granted access to Staging or Production — these are separate grants, reviewed separately.
- Admin/scholar MFA/passkey enforcement (`NoorHeroes_Final_Development_Prompt.md` §9 item 8) is **required from the first admin account created in any persistent tier** — Dev-QA included. Local/CI test fixtures may use a mocked MFA assertion for automated test speed (this is test-harness convenience, not a relaxed production code path — the mock lives in `tests/conftest.py`, never in application code).
- Production access for a human operator uses just-in-time IAM elevation (break-glass), not a standing role — mechanics owned by `Infra.02`/ops runbooks; this file only fixes that Production's IAM boundary is the strictest of the three spoke projects.

### 9.4 Test-mode auth conveniences — where they are and are not allowed

This is the single most important security rule this file establishes, because it directly protects Staging's validity as a pen-test target (§3.1):

| Tier | Fixed/test OTP allowed? | Mocked MFA allowed? | Rationale |
|---|---|---|---|
| Local | Yes (`test_mode_auth_bypass_enabled=true`) | Yes, for automated test fixtures | Fast local iteration |
| CI | Yes | Yes | Fast, deterministic automated runs |
| Dev-QA | Yes, but **behind a feature flag additionally gated on `environment != "production"` AND `environment != "staging"`** — i.e. a double guard, not just the flag | Yes, for QA automation scripts only, never for real admin/scholar accounts | QA needs deterministic OTP for scripted flows, but the double guard means this code path is structurally unreachable if ever mis-deployed to Staging/Production |
| Staging | **No — hard `false`, not configurable via env or flag** | **No — real MFA required for every admin/scholar account, same as Production** | Staging must be a faithful pen-test target |
| Production | **No — hard `false`** | **No — real MFA required** | Live traffic |

The "hard `false`, not configurable via env" requirement means: the bypass code path must be compiled/deployed out entirely for Staging and Production builds (or, at minimum, gated by a check that reads a value which cannot be set via any env var reachable in those tiers' Secret Manager/Cloud Run config — e.g., an `if settings.environment in (Environment.STAGING, Environment.PRODUCTION): raise RuntimeError(...)` guard at the top of the bypass function itself, so even a misconfigured flag cannot activate it). This is exactly the kind of rule the architectural-test suite (`NoorHeroes_Final_Development_Prompt.md` §5) should assert automatically — see §14.3.

### 9.5 CORS

`cors_allowed_origins` (§6.2) is an explicit allowlist per tier, never a wildcard, in every tier including Local (Local allows only `http://localhost:3000`). Staging and Production allowlists are reviewed the same way a firewall rule would be — any addition requires the same PR review rigor as a security-relevant change (`NoorHeroes_Final_Development_Prompt.md` §4's CODEOWNERS review checklist already covers "does this PR touch `core/security`").

---

## 10. Error Handling and Edge Cases

- **Missing required env var at boot, any tier:** `Settings()` raises a `pydantic.ValidationError`; the process must not start with a silently-defaulted value for any field marked required. This applies identically in Local — a new developer with an incomplete `.env` gets a clear startup failure naming the missing key, not a confusing runtime error three requests later.
- **Tier/config mismatch guard:** at boot, before serving traffic, the app asserts an internal consistency check and refuses to start if it fails — e.g., `environment == PRODUCTION` but `debug == True`, or `environment in (STAGING, PRODUCTION)` but the JWT signing key matches the known Local-tier placeholder value from `.env.example`. This is a defense against accidentally deploying a Local/Dev-QA configuration bundle into a Staging/Production Cloud Run revision.
- **CI job attempts to reach a real cloud resource:** CI jobs must never hold credentials capable of reaching the Dev-QA/Staging/Production spoke projects for anything except the explicit, narrowly-scoped deploy step (`CI_CD.08`/`09`, via Workload Identity Federation). A CI job's default `GITHUB_TOKEN`/test env has no path to any spoke project's Secret Manager or database — verified by the architectural test in §14.3.
- **Terraform state lock contention:** Terraform remote state (owned by `Infra.04`, e.g. a GCS bucket with native state locking) must reject a second concurrent `apply` against the same tier's state rather than silently corrupting it — an `Infra.04` requirement, noted here because it's a direct consequence of persistent tiers being shared, mutable infrastructure (unlike Local/CI).
- **Dev-QA nightly redeploy colliding with an active QA test session:** the scheduled Dev-QA redeploy (§11.2) posts a notification (Slack/GitHub) at least 15 minutes before running, and the redeploy workflow supports a manual "skip tonight" override so an in-progress QA pass isn't disrupted mid-session.
- **Partial/failed migration in a persistent tier:** the migration-runner step (owned by `CI_CD.08`/`09`) must leave the tier in a state where the *previous* application version can still run against the *not-yet-migrated* or *partially-migrated* schema — this is an additive-migration-first discipline (never drop/rename a column in the same migration that also stops the old code from reading it), applicable to every persistent tier, most strictly enforced for Production per `NoorHeroes_Final_Development_Prompt.md` §2.3 ("Alembic, one migration per PR... never edited after merge").
- **A tier's resource-naming collision:** the naming convention in §5/§8 (`noorheroes-{resource}-{tier-slug}`) is deliberately collision-proof across all 5 tiers and across GCP/Cloudflare (two independent namespaces) — a CI check (§14.3) can grep Terraform/Compose files for any resource name lacking the correct tier suffix and fail the build.

---

## 11. State Management and Lifecycle Considerations

### 11.1 Lifecycle summary

| Tier | Created | Redeployed | Torn down |
|---|---|---|---|
| Local | `docker compose up` (developer-initiated) | On demand, any time | `docker compose down` / never (developer's own machine) |
| CI | Automatically, at workflow-run start | N/A — new instance every run | Automatically, at workflow-run end (`docker compose down -v` / Testcontainers auto-cleanup) |
| Dev-QA | Once, via Terraform (`Infra.04`) | Scheduled nightly + on-demand (`workflow_dispatch`) — decoupled from the merge-to-main pipeline | Never (persistent); only reseeded (§8.5), not destroyed |
| Staging | Once, via Terraform | Automatically, on every merge to `main` (pipeline stage 9) | Never (persistent) |
| Production | Once, via Terraform | Only via manual promotion gate (pipeline stage 11), deploying an already-Staging-verified artifact | Never (persistent) |

### 11.2 Why Dev-QA's cadence is decoupled from Staging's

The 13-stage CI/CD pipeline (`NoorHeroes_Final_Development_Prompt.md` §6) names only Staging as the automatic merge-to-main deploy target — Dev-QA is not part of that mandatory pipeline. This file adopts a **scheduled nightly + on-demand** cadence for Dev-QA specifically so a QA tester has a stable target that doesn't change mid-test-pass on every single merge, while Staging (whose job is to mirror what's about to ship) tracks `main` exactly (see Decision 5, §18).

### 11.3 Config lifecycle within a running process

`Settings` is instantiated once per process at boot (already the documented pattern — `settings` singleton / `get_settings()`) and is immutable for the life of that process in every tier; a config change in any persistent tier requires a new deploy (new Cloud Run revision), never a hot-reload of secrets into a running container — this matches Cloud Run's own revision model and avoids any tier ever running with a config value that doesn't match what's recorded against its deployed revision.

---

## 12. Integration Points with Existing Modules

### 12.1 Backend (`pydantic-settings`)

No code change to `core/settings.py`'s existing structure is required — this file's contract is additive (new/confirmed field names, §6.2) and operates entirely through environment injection. Every backend module that already calls `get_settings()` continues to work unchanged in every tier; the only thing that changes per tier is *which values* Cloud Run (or Compose, or the CI job) injects into the process's environment before `Settings()` is instantiated.

### 12.2 Admin-web (Next.js Zod env validation + `src/proxy.ts`)

The already-implemented Zod-validated env schema consumes exactly the vars in §6.3. `src/proxy.ts` (the middleware checking session-cookie presence and injecting `X-Request-ID`) is tier-agnostic — it never needs to know which tier it's running in; only `API_BASE_URL` changes, which the middleware already treats as configuration, not a hardcoded value. `NEXT_PUBLIC_APP_ENV` is the one new addition this file specifies (§6.3) — a single extra public var powering the "you are in Staging" banner (§6.3 rationale).

### 12.3 Mobile (Gradle build variants)

Per `NoorHeroes_Final_Development_Prompt.md` §13.1 ("Configuration management" row), mobile already commits to Gradle build variants exposing base URL/feature-flag defaults via `expect`/`actual` `BuildConfig`-equivalent constants consumed by `core-network`. This file fixes the variant-to-tier mapping:

| Gradle product flavor | Tier it targets | Backend base URL consumed by `core-network` |
|---|---|---|
| `dev` | Local | `http://10.0.2.2:8000/v1` (Android emulator loopback) — overridable to a LAN IP via `local.properties` for physical-device testing against a developer's own machine |
| `qa` | Dev-QA | `https://api-devqa.noorheroes.com/v1` |
| `staging` | Staging | `https://api-staging.noorheroes.com/v1` |
| `prod` | Production | `https://api.noorheroes.com/v1` |

**CI has no dedicated mobile flavor.** Per `NoorHeroes_Final_Development_Prompt.md` §1.1/§6, Maestro/UI Automator E2E is explicitly deferred post-MVP — CI's mobile jobs run unit tests (JUnit5/MockK), `kotlin.test`, ktlint/detekt, and Compose Multiplatform UI Test against fake repositories/a fake Ktor engine, none of which contact a live backend. These jobs compile the `dev` flavor's sources (cheapest, no live network dependency) purely to get a working build to test against — see Decision 6, §18.

The `prod` flavor's signed release build is the only one that reaches Play Console, using Play Console's own staged rollout — a mechanism independent of (and not to be confused with) the backend/admin-web container-image promotion path described in §4.6.

---

## 13. Development Steps in Order

1. **Confirm cloud provider** (GCP vs. AWS) with the team/stakeholders if not already decided — this file's worked examples assume GCP; flip to the AWS equivalents column throughout if AWS is chosen. This decision blocks `Infra.04` and should be made before, not during, Terraform authoring.
2. **Create the hub project** (`noorheroes-platform` or AWS tooling account): Artifact Registry repo, Cloud DNS zone delegation for `noorheroes.com`, CI Workload Identity Federation provider.
3. **Create the three spoke projects** (`noorheroes-devqa`, `noorheroes-staging`, `noorheroes-prod`), each with its own VPC — empty of workloads at this point; Terraform module code that populates them is `Infra.04`'s job, but the *projects themselves* (the isolation boundary) are this file's deliverable.
4. **Provision the `infra/environments/{local,ci,dev-qa,staging,production}/` folder** per §5, with each tier's `README.md` and non-secret `*.env*.example` files populated from the §6 tables.
5. **Register the four `GitHub Environments`** (`dev-qa`, `staging`, `production`, plus repo-level secrets for CI) per §7.2, with `production`'s required-reviewer protection rule turned on from the start (never "add the gate later").
6. **Create per-tier Cloudflare R2 buckets and scoped API tokens** (§8.3) — `noorheroes-media-devqa`, `-staging`, `-prod`, each with its own token, none able to read another tier's bucket.
7. **Generate and store per-tier JWT signing keys** in each spoke project's Secret Manager (§9.2) — independently random per tier, never derived from or equal to another tier's key or the Local-tier placeholder.
8. **Wire the tier→`Environment` enum mapping** (§6.1) into the deploy configuration for each tier (i.e., make sure Cloud Run's env injection for the Dev-QA service sets `ENVIRONMENT=development`, not `dev-qa` or any other string not in the existing 4-value enum).
9. **Implement the boot-time consistency guard** (§10) and the hard `test_mode_auth_bypass_enabled=false` guard for Staging/Production (§9.4).
10. **Hand off to `Infra.02`** (secrets rotation/gitleaks), `Infra.03` (local Compose service definitions), `Infra.04` (Terraform modules that actually populate the spoke projects with Cloud Run/Cloud SQL/Memorystore resources using this file's naming convention), and `Infra.05` (observability endpoints per tier) — each of those files should be authored *against* this file's tier/naming contract, not before it.
11. **Run the Phase-0 "hello family" vertical slice** (already defined as Phase 0's exit criteria in `NoorHeroes_Final_Development_Prompt.md` §13.4) through Dev-QA once the above is wired, as the first live proof the tier model actually works end-to-end outside Local.

---

## 14. Testing Strategy and Acceptance Criteria

### 14.1 Automated checks (CI-blocking)

1. **`.env.example` / `Settings` field-name drift check:** a script asserts every field `Settings` declares as required has a corresponding key documented in `infra/environments/local/backend.env.example` (owned jointly with `Infra.02`) — fails CI if they drift, keeping the "checklist of required vars" promise from `NoorHeroes_Final_Development_Prompt.md` §3 actually enforced rather than aspirational.
2. **Resource-naming convention check:** a grep-based CI script scans Terraform/Compose files for any GCP/R2 resource name that doesn't match `noorheroes-{resource}-{tier-slug}` for one of the 5 defined slugs — fails the build on a naming drift (directly supports the Error Handling item in §10).
3. **Tier/`Environment`-enum consistency test:** a backend test instantiates `Settings` with each of the 4 `Environment` values and asserts the derived behavior matches §6.2's table (e.g., `debug=False` whenever `environment in (STAGING, PRODUCTION)`, `rate_limit_enabled=True` whenever `environment != LOCAL`).
4. **Staging/Production auth-bypass architectural test:** the single most important test this file requires — assert that `test_mode_auth_bypass_enabled` cannot be made truthy when `environment in (STAGING, PRODUCTION)` regardless of what any env var or flag claims, by directly invoking the guard function with a forged/malicious config object in the test, not just checking the default. This is a CI-blocking, separately-named required status check, matching the pattern already established for the platform's other architectural invariants (`NoorHeroes_Final_Development_Prompt.md` §5).
5. **IAM cross-project isolation check:** an `Infra.04`-adjacent test (can be authored here as a placeholder, fully implemented once Terraform exists) asserting no IAM binding in the Dev-QA project grants any principal access to the Staging or Production project.

### 14.2 Manual acceptance criteria (Phase 1 exit gate for this file)

- A brand-new developer can `git clone` + follow `infra/environments/local/README.md` and have a working Local stack within one `docker compose up` (validated jointly with `Infra.03`).
- A CI run on a trivial PR completes lint→test→build with a fresh, isolated Postgres/Redis and zero cross-run state leakage, confirmed by running the same PR's CI twice and diffing DB state (should be identical both times).
- `terraform plan` against a freshly created Dev-QA spoke project (once `Infra.04` exists) produces a plan with zero resources referencing another tier's name.
- The `production` GitHub Environment cannot be deployed to without an explicit human approval click, verified by attempting an automated deploy and confirming it blocks pending review.
- `NEXT_PUBLIC_APP_ENV`-driven banner renders correctly in a Staging build and is verifiably absent/different in a Production build.

---

## 15. Production-Readiness Considerations

1. **Cost shape per tier:** Local/CI cost nothing beyond compute-minutes already budgeted for developer machines/CI runners. Dev-QA is sized for intermittent load — Cloud Run `min_instances=0` (scale-to-zero between QA sessions) is appropriate and cost-correct here, unlike Staging/Production. Staging runs `min_instances=1` (avoid cold-start skew that would distort pen-test/tabletop timing measurements). Production runs `min_instances≥2` across zones for HA from day one.
2. **Health probes:** the already-implemented `/healthz` (liveness) and `/readyz` (readiness — checks DB/Redis connectivity) endpoints are wired as Cloud Run startup/liveness probes identically in Dev-QA/Staging/Production; this is a direct reuse of existing backend infrastructure, not new work.
3. **Immutable artifact promotion (§4.6)** is itself a production-readiness property: Production never runs code that wasn't already verified running in Staging under the same container digest.
4. **No tier is a single point of naming ambiguity:** every resource, secret, and config value in every tier carries an explicit tier suffix (§5/§8) — this is what makes an incident responder's first question ("which environment is this?") answerable from the resource name alone, before even opening a dashboard.
5. **DR drill cadence** (§8.5) must actually run monthly for Production per `NoorHeroes_Final_Development_Prompt.md` §10 ("Ongoing / Long-term Maintenance") — this file establishes the target; scheduling the recurring drill itself is an ops/runbook responsibility outside this file's scope but downstream of it.
6. **Kubernetes migration path is explicitly deferred** (`infra/k8s/` stays empty until Phase 6/Scale, per `NoorHeroes_Consolidated_Blueprint_v6.md` §19.3) — this file's tier model does not assume or require K8s at any point; the eventual migration (`Phase11...Infra.02`) re-targets the same 5-tier naming convention onto K8s namespaces rather than replacing it.

---

## 16. Dependencies / Prerequisites

- Phase 0 (repo foundation) complete — monorepo scaffold, per-platform lint/format tooling, CI skeleton. **Already confirmed complete** per the Repository Foundation status; no blocking dependency remains here.
- Cloud provider account access (GCP org or AWS org) with permission to create new projects/accounts.
- Cloudflare account with R2 enabled and DNS access for `noorheroes.com` (or the ability to delegate a subdomain to Cloud DNS).
- GitHub repository admin rights (to configure Environments, branch protection, and Workload Identity Federation / OIDC trust).
- Team/stakeholder confirmation of the cloud-provider choice (§13 step 1) and the RPO/RTO targets (§8.5) — both flagged as open decisions in the source documents; this file proposes concrete working defaults but does not treat them as finalized.

---

## 17. Definition of Done

This file's deliverable (the tier model + provisioning) is done when:

- [ ] All 5 tiers are named, defined, and mapped to concrete infrastructure with no "TBD" left in this document.
- [ ] The hub project + 3 spoke GCP projects (or AWS equivalent) exist, empty of application workloads, with correct IAM isolation between them.
- [ ] `infra/environments/{local,ci,dev-qa,staging,production}/` exists with populated `README.md` and non-secret `*.env*.example` files per §5/§6.
- [ ] The 4 `GitHub Environments` (repo-level for CI, `dev-qa`, `staging`, `production`) exist with the protection rules in §7.2, `production`'s required-reviewer gate active.
- [ ] Per-tier R2 buckets and scoped API tokens exist for Dev-QA/Staging/Production, each provably unable to access another tier's bucket.
- [ ] Per-tier JWT signing keys are generated and stored, independently random, never shared across tiers or with the Local placeholder.
- [ ] The `Environment`-enum mapping (§6.1) is wired into each tier's deploy config, and the consistency-guard test (§10, §14.1 item 3) passes.
- [ ] The Staging/Production hard auth-bypass-disabled guarantee (§9.4) is implemented and covered by the architectural test in §14.1 item 4.
- [ ] All acceptance criteria in §14.2 pass.
- [ ] This file has been handed off as the fixed contract for `Infra.02`, `Infra.03`, `Infra.04`, `Infra.05`, and `CI_CD.06`–`10` to build against, with no contradiction between this file and any of those once authored.

---

## 18. Assumptions or Decisions the Coding Agent Must Follow

1. **CI tier reuses `Environment.LOCAL`; Dev-QA reuses `Environment.DEVELOPMENT`.** The already-implemented `Environment` StrEnum in `core/settings.py` has exactly 4 values. Do not add a 5th value (e.g. `CI` or `DEV_QA`) to that enum — extend behavior via which env values are injected per tier (§6.1), never by widening the enum.
2. **GCP (Cloud Run/Cloud SQL/Memorystore/Secret Manager/Artifact Registry) is this file's worked example and default recommendation**, because Cloud Run is named first in the source stack target. The binding provider decision belongs to `Infra.04` — if that file selects AWS instead, substitute the AWS-equivalents named alongside each GCP resource throughout this file; the tier/naming/isolation *model* does not change either way.
3. **`infra/docker-compose.staging.yml`** (already named in the existing monorepo tree) is a **local reproduction harness for Staging-equivalent config**, not the Staging tier's actual deployment mechanism. The real Staging tier is a managed Cloud Run environment provisioned by Terraform and deployed by CI, structurally identical to Production. This reconciles `NoorHeroes_Consolidated_Blueprint_v6.md` §19.3's "Docker Compose for local development and staging" wording with `NoorHeroes_Final_Development_Prompt.md` §3/§7's "Staging mirrors prod topology" requirement.
4. **RPO ≤ 15 minutes / RTO ≤ 1 hour** is adopted as the working Production DR target (from `NoorHeroes_Final_Development_Prompt.md` §7), with `NoorHeroes_Consolidated_Blueprint_v6.md` §14.7's looser RPO ≤ 1 hour / RTO ≤ 4 hours documented as the fallback minimum if the tighter target proves operationally unachievable. Both remain **provisional pending stakeholder confirmation and the first DR drill** — do not treat either as final without that confirmation.
5. **Dev-QA's deploy cadence is scheduled nightly + on-demand `workflow_dispatch`, decoupled from the merge-to-main → Staging auto-deploy pipeline.** Neither source document states Dev-QA's trigger explicitly (the 13-stage pipeline names only Staging as the automatic merge target) — this is a Phase-1 gap-fill decision, made so QA has a stable, predictable target.
6. **Mobile has no dedicated CI-tier build flavor.** CI mobile jobs compile and test against the `dev` flavor's sources (unit tests, ktlint/detekt, Compose Multiplatform UI Test against fakes) with no live backend dependency, consistent with Maestro/E2E being explicitly deferred post-MVP.
7. **Hub-and-spoke GCP project topology (1 shared platform project + 3 workload projects for Dev-QA/Staging/Production)** is this file's chosen isolation boundary. The source documents say only "separate GCP projects or namespaces" as an example without mandating a specific topology — this is a concrete decision filling that gap, and `Infra.04` must implement against it rather than inventing an alternative topology.
8. **Do not modify `core/settings.py`'s existing `Environment` enum, the JWT claim schema, the Argon2id hashing utility, or any other already-implemented Security Baseline component** described in `FAST-API-INSTRUCTIONS.md` — this file's job is provisioning environments *around* that already-correct code, not changing it.
9. **Field names in §6.2/§6.3 are this file's concrete proposal, not a mandate to rename already-implemented fields.** If `core/settings.py` or the admin-web Zod schema already use different exact names for an equivalent concern, keep the existing names and treat this file's table as satisfied by the existing field under its existing name — reconciliation is additive (fill genuine gaps), never a rename of working code.

---

## AI Agent Development Prompt

Use this prompt verbatim (or lightly adapted) to hand this file to a coding agent for implementation.

```
You are implementing the environment-tier provisioning layer for NoorHeroes, a FastAPI + Kotlin
Multiplatform + Next.js Admin monorepo. Follow the specification in
Development_Blueprints.Phase1_Infra_Config.Infra.01-environment-tiers-provisioning.md exactly.

STACK CONTEXT (already built — do not re-implement or restructure):
- Backend: FastAPI, async SQLAlchemy 2.x/Alembic, pydantic-settings `Settings` singleton at
  `src/noorheroes/core/settings.py` with an existing 4-value `Environment` StrEnum
  (LOCAL, DEVELOPMENT, STAGING, PRODUCTION), structlog + X-Request-ID correlation middleware,
  domain-error hierarchy, transactional outbox, Testcontainers-based test harness,
  /healthz + /readyz health probes.
- Admin-web: Next.js 15 App Router, TypeScript, Zod-validated env parsing, zero-token-persistence
  auth (access tokens in server memory only, httpOnly refresh cookies), src/proxy.ts middleware.
- Mobile: Kotlin Multiplatform / Compose Multiplatform, Koin DI, Gradle Version Catalog,
  core-network module consuming a BuildConfig-equivalent base URL per Gradle product flavor.

WHAT TO BUILD:
1. The `infra/environments/{local,ci,dev-qa,staging,production}/` folder tree exactly as specified
   in §5 — README.md + non-secret *.env*.example files per tier, populated from the field tables
   in §6.2 and §6.3. Do NOT put real secret values in any of these files — keys and non-secret
   values (URLs, flags, numeric limits, log levels) only.
2. The GCP hub-and-spoke project topology from §4.1: one `noorheroes-platform` hub project
   (Artifact Registry, Cloud DNS, CI Workload Identity Federation) and three spoke projects
   (`noorheroes-devqa`, `noorheroes-staging`, `noorheroes-prod`), each with its own VPC and IAM
   boundary. (If the team has confirmed AWS instead of GCP, substitute the AWS-equivalents named
   throughout the source file — do not invent a third option.)
3. The resource-naming convention `noorheroes-{resource}-{tier-slug}` for every cloud resource,
   with `{tier-slug}` ∈ {local, ci, dev-qa, staging, production} exactly as used in this file.
4. Per-tier Cloudflare R2 buckets (`noorheroes-media-devqa/-staging/-prod`) with independently
   scoped API tokens — verify no token from one tier can read/write another tier's bucket.
5. Per-tier JWT signing keys in each spoke project's Secret Manager — independently random,
   never shared across tiers, never equal to the Local-tier placeholder value.
6. The four GitHub Environments (repo-level secrets for CI; `dev-qa`, `staging`, `production` as
   named GitHub Environments) with the protection rules in §7.2 — `production` MUST have at least
   one required reviewer configured from the moment it is created, never added later.
7. The tier → `Environment`-enum runtime mapping from §6.1 (Local→local, CI→local, Dev-QA→development,
   Staging→staging, Production→production) wired into each tier's deploy configuration.
8. The boot-time configuration consistency guard described in §10 (refuse to start if
   environment==PRODUCTION but debug==True, or if a Staging/Production JWT signing key matches
   the known Local placeholder).
9. The hard, non-configurable-via-env `test_mode_auth_bypass_enabled=false` guarantee for Staging
   and Production described in §9.4 — implement this as a guard inside the bypass code path itself
   (e.g., raise if `settings.environment in (Environment.STAGING, Environment.PRODUCTION)`), not
   merely as a default value that could be overridden by a misconfigured env var or flag.
10. The Gradle product-flavor → tier → base-URL mapping from §12.3 (dev/qa/staging/prod flavors).

HARD REQUIREMENTS — DO NOT VIOLATE:
- Do NOT add a 5th value to the existing `Environment` StrEnum in `core/settings.py`. CI reuses
  LOCAL; Dev-QA reuses DEVELOPMENT. This is a fixed decision (§18, Decision 1) — do not "fix" it
  by widening the enum.
- Do NOT rename any field that already exists in `core/settings.py` or the admin-web Zod env
  schema to match this file's field-name tables (§6.2/§6.3) — those tables are additive gap-fill
  proposals; if a field already exists under a different name, use the existing name.
- Do NOT put real secret values (DB passwords, JWT keys, R2 credentials) into any file committed
  to the repository, including files literally named `*.example` — those contain keys and
  non-secret values only. Real secrets belong exclusively in the per-tier secret store (§8.4).
- Do NOT treat `infra/docker-compose.staging.yml` as the Staging tier's deployment mechanism —
  it is a local reproduction harness only (§4.5, §18 Decision 3). The real Staging tier deploys
  via Cloud Run/Terraform/CI, identically in shape to Production.
- Do NOT allow any test-mode OTP bypass or mocked MFA to be reachable when
  `environment in (STAGING, PRODUCTION)`, under any configuration. This must be provably true by
  a test that forges a malicious config object and asserts the guard still rejects it (§14.1 item 4)
  — not merely a test of the default configuration.
- Do NOT modify the already-implemented JWT claim schema, Argon2id hashing utility, gateway/
  domain-service authorization split, or transactional outbox — this task provisions environments
  around that code, it does not change it.
- Do NOT build the Terraform module code, the local Docker Compose service definitions, the
  secrets-rotation/gitleaks wiring, the observability collector wiring, or any CI/CD pipeline
  stage — those belong to `Infra.02`, `Infra.03`, `Infra.04`, `Infra.05`, and `CI_CD.06`–`CI_CD.10`
  respectively. This task's output is the contract those files build against, not their content.

VERIFICATION — write and run these before declaring the task done:
1. A test instantiating `Settings` (or the tier config loader) with each of the 4 `Environment`
   values, asserting `debug`, `rate_limit_enabled`, and `cors_allowed_origins` match §6.2's table
   for that value.
2. A test/script asserting `test_mode_auth_bypass_enabled` cannot be made truthy when
   `environment in (STAGING, PRODUCTION)`, using a forged config object, not just the default.
3. A grep-based CI script asserting every provisioned cloud resource name matches
   `noorheroes-{resource}-{tier-slug}` for one of the 5 defined slugs.
4. A script asserting every required `Settings` field has a corresponding key documented in
   `infra/environments/local/backend.env.example` (field-name drift check).
5. Manual verification that attempting to deploy to the `production` GitHub Environment without
   an approval blocks, and that a Dev-QA-scoped credential cannot read the Staging or Production
   Secret Manager/Cloud SQL instance (IAM isolation check).
6. Confirm `terraform plan` (once `Infra.04` exists) against a freshly created spoke project
   produces zero resources referencing another tier's name.

Report back: which of the 18 numbered file-tree items in §5 were created, the exact GCP (or AWS)
project/account IDs provisioned, and the pass/fail result of each of the 6 verification steps above.
```
