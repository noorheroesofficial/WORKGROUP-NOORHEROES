# Phase 1 — Docker Compose Local Development Stack

| Field | Value |
|---|---|
| Blueprint ID | `Development_Blueprints.Phase1_Infra_Config.Infra.03-docker-compose-local-dev-stack.md` |
| Phase | Phase 1 — Infrastructure & Configuration |
| Category | Infra |
| Depends on | Phase 1, item 01 — `Infra.01-environment-tiers-provisioning.md` (defines the `local` environment tier this stack implements) |
| Consumed by | Every Backend/CrossPlatform blueprint whose test suite or manual verification step assumes a working local Postgres/Redis/object-storage substrate; Phase 1 `CI_CD.06` (must NOT reuse this file — see §12) |
| Status | NEW — must be authored |

---

## 1. Objective and Purpose

Give every backend engineer — and every automated process that is not the pytest/Testcontainers suite — a single, reproducible, one-command local development environment that mirrors the real backend's runtime dependencies closely enough to develop and manually exercise features end-to-end on a laptop:

- PostgreSQL 16, matching the `PostgreSQL 16+` production target.
- Redis, matching its four production roles (API cache, rate-limit counters, Celery broker, step-up/OTP session state).
- An R2-compatible (S3 API-compatible) object-storage emulator, so the media upload pipeline's presigned-URL flow can be exercised without a real Cloudflare R2 bucket or network egress.
- The FastAPI backend itself, running with hot-reload so code edits on the host are reflected in the running process within seconds, no rebuild required.

This file's scope is **strictly the local developer inner-loop**. It is not the CI environment (owned by `CI_CD.06-ci-pipeline-lint-test-build-stages.md`), not the staging/production topology (owned by `Infra.04-terraform-iac-baseline-staging.md`), and it must not be confused with the Testcontainers-based integration test harness that already ships inside the backend (`tests/conftest.py`, confirmed built per `FAST-API-INSTRUCTIONS.md` §"Testing infrastructure"). §12 below draws that boundary explicitly because it is the single most common way this kind of file gets misused.

## 2. Scope and Requirements

**In scope:**
- `infra/docker-compose.yml` — the compose file itself, with `postgres`, `redis`, `minio`, `minio-init`, `backend`, and an optional `backend-worker` (Celery) service.
- `backend/Dockerfile.dev` — a dev-only image definition distinct from the production `backend/Dockerfile` (multi-stage builder, owned by the CI build stage / `Infra.04`).
- `backend/docker-entrypoint.dev.sh` — the dev container's entrypoint (runs Alembic migrations, then execs the container command).
- `infra/.env.example` — the checklist of every environment variable this stack requires, with safe non-secret local defaults.
- Root-level `Makefile` `dev*` targets wrapping the compose commands into a documented, memorable workflow.
- The environment-variable contract between this stack and the already-implemented `Settings` class (`src/noorheroes/core/settings.py`) and `R2StorageService` (`src/noorheroes/infrastructure/storage/storage.py`) — see §6.

**Explicitly out of scope (owned elsewhere, do not build here):**
- CI's ephemeral Postgres/Redis provisioning (`docker-compose.ci.yml` and/or Testcontainers-in-CI) — `CI_CD.06`.
- Staging/production infrastructure, managed Postgres/Redis/R2, Terraform — `Infra.04`.
- Secrets-manager wiring, `gitleaks`/`trufflehog` scanning — `Infra.02`.
- Observability stack (Prometheus/Grafana/Sentry/OTel collector) — `Infra.05`. This file disables/no-ops telemetry export in local dev (see §7) rather than standing up a local observability stack.
- The 11-step content upload validation pipeline's actual scanning logic — that is application code owned by its own Backend blueprint; this file only provides the object-storage substrate it writes to.
- Any change to `backend/src/noorheroes/**` application code. This file is infrastructure plumbing around the existing, already-implemented backend — see §18's "do not touch" list.

## 3. Technical Implementation Details

| Concern | Decision | Rationale |
|---|---|---|
| Postgres image | `postgres:16-alpine` | Matches "PostgreSQL 16+"; Alpine variant keeps the pull small for a stack developers rebuild often. |
| Redis image | `redis:7-alpine` | Matches the stack table's "Redis (latest stable)" at the 7.x line; AOF persistence enabled so a `docker compose restart` doesn't cold-drop rate-limit/session state mid-session. |
| Object storage emulator | **MinIO** (`minio/minio`, S3-API-compatible server + `minio/mc` CLI for bootstrap) | Cloudflare does not ship a standalone, backend-agnostic local R2 emulator — its "local dev" tooling (`wrangler`/Miniflare) targets Cloudflare Workers projects, not a Python service calling out via `boto3`/`aioboto3`. R2's entire local-dev story, by Cloudflare's own design, **is** "point an S3-compatible client at an S3-compatible server," which is exactly what `R2StorageService` already does per `FAST-API-INSTRUCTIONS.md` §4 ("Cloudflare R2 presigned uploads" via the S3-compatible endpoint). MinIO is the de facto standard S3-compatible dev/test server: single static binary, official Docker image, a web console for developers to inspect uploaded objects, and first-class presigned-URL (SigV4) support identical in shape to R2's. It is a drop-in swap of `R2_ENDPOINT_URL`, nothing in `R2StorageService` should need to branch on "is this R2 or MinIO." |
| Backend dependency manager | **`uv`** | The stack document leaves this as "`uv` or Poetry — pick one." This file picks `uv` for faster container builds/rebuilds during the hot-reload inner loop and its built-in lockfile audit. This is a decision this blueprint makes on the team's behalf — see §18 if the real `backend/pyproject.toml` already commits to Poetry, this must be reconciled, not silently overridden. |
| Backend dev image | `backend/Dockerfile.dev`, single-stage, `python:3.12-slim` base | Distinct from the production `backend/Dockerfile` (multi-stage builder + slim runtime, per Final_Development_Prompt §7). The dev image optimizes for rebuild speed and bind-mount compatibility, not final image size or attack surface — it never ships anywhere. |
| Hot reload mechanism | Host bind-mount of `backend/` into the container at `/app`, `uvicorn --reload --reload-dir /app/src` | Editing a file on the host is visible inside the container immediately (no rebuild); Uvicorn's reloader watches `/app/src` and restarts the ASGI app process on change. |
| Dependency-install isolation | A **named volume** at `/app/.venv`, mounted *after* (and therefore layered on top of) the `../backend:/app` bind mount | Without this, the host bind mount would hide the `.venv` that `uv sync` built into the image during `docker build`, since the host's `backend/` directory has no `.venv` of its own (it's git-ignored). The named volume preserves the container-built virtualenv across the bind mount. |
| Migrations on container start | `docker-entrypoint.dev.sh` runs `uv run alembic upgrade head` before exec-ing the container's `CMD`, gated by `RUN_MIGRATIONS_ON_BOOT` (default `true` for `backend`, `false` for `backend-worker`) | Removes "did you remember to migrate" as a local-dev failure mode; a `false` override exists for anyone who wants manual control, and prevents two containers racing on the same migration at boot. |
| Background jobs | Optional `backend-worker` service (Celery), gated behind a Compose **profile** (`worker`), not started by plain `docker compose up` | The backend's own stack table requires Celery + Redis broker for background jobs (localization translation tasks, notification dispatch, etc.), so a working local stack needs a way to run one — but most day-to-day API/DB work doesn't need it running, and it adds a second image build. `docker compose --profile worker up` opts in explicitly. See §18 — this is an addition beyond the four services named in this file's objective, included because omitting it would leave every Celery-dependent feature untestable locally with no documented path to test it. |

## 4. Architecture and Component Responsibilities

```text
┌───────────────────────────────────────────────────────────────────────────┐
│                    developer machine (docker compose)                     │
│                                                                             │
│  ┌───────────┐   ┌──────────┐   ┌────────────────────┐                   │
│  │ postgres  │   │  redis   │   │       minio          │                   │
│  │ :5432     │   │  :6379   │   │ :9000 (S3 API)        │                   │
│  │           │   │          │   │ :9001 (web console)   │                   │
│  └─────┬─────┘   └────┬─────┘   └──────────┬─────────────┘                 │
│        │              │                     │  (bootstrapped by)          │
│        │              │            ┌────────┴─────────┐                   │
│        │              │            │   minio-init      │  (runs once,     │
│        │              │            │  (minio/mc)        │   creates       │
│        │              │            └────────────────────┘   bucket, exits)│
│        │              │                     │                             │
│        ▼              ▼                     ▼                             │
│  ┌─────────────────────────────────────────────────────────────────┐     │
│  │                          backend                                  │     │
│  │   FastAPI + Uvicorn --reload, bind-mounted src/, :8000            │     │
│  │   entrypoint: alembic upgrade head → exec uvicorn                 │     │
│  └─────────────────────────────────────────────────────────────────┘     │
│                              │  (profile: worker, optional)               │
│                              ▼                                            │
│                    ┌───────────────────┐                                  │
│                    │  backend-worker    │  Celery worker, same image      │
│                    │  (Celery)          │  consumes redis broker db 1     │
│                    └───────────────────┘                                  │
│                                                                             │
│  all six services join network: noorheroes-dev-network                    │
└───────────────────────────────────────────────────────────────────────────┘
```

Component responsibilities:

- **`postgres`** — the single source of truth for all relational state; owns the `noorheroes` database the backend's Alembic migrations target.
- **`redis`** — single Redis instance, logically partitioned by **DB index** for local dev simplicity (DB 0 = app cache/rate-limit/session, DB 1 = Celery broker, DB 2 = Celery result backend). Production may use separate managed Redis instances/clusters per role (that's `Infra.04`'s decision) — local dev collapses them into one container to keep the stack lean.
- **`minio`** — the S3-compatible object store standing in for Cloudflare R2. Owns the `noorheroes-media-dev` bucket (configurable) that `MediaAsset`/`R2StorageService` write to.
- **`minio-init`** — a one-shot bootstrap container (not a long-running service) that creates the bucket and sets its access policy, then exits `0`. Exists because MinIO does not auto-create buckets on first boot the way some managed S3 providers do.
- **`backend`** — the FastAPI app itself (`src.noorheroes.main:app`), hot-reloading, listening on `:8000`, exposing `/healthz` and `/readyz` (both already implemented per `FAST-API-INSTRUCTIONS.md` §"Health Probes").
- **`backend-worker`** (optional, `worker` profile) — the same image as `backend`, running `celery worker` instead of `uvicorn`, so Celery-backed features (localization translation tasks, notification dispatch, reconciliation jobs) are exercisable locally.

## 5. Folder/File Structure

```text
noorheroes/
├── backend/
│   ├── Dockerfile                    # production multi-stage build — EXISTING, do not modify here
│   ├── Dockerfile.dev                # NEW — this blueprint
│   ├── docker-entrypoint.dev.sh      # NEW — this blueprint
│   ├── pyproject.toml                # EXISTING — read, not modified, by this blueprint
│   ├── uv.lock                       # EXISTING/expected — see §18 if absent
│   └── src/noorheroes/...            # EXISTING — bind-mounted read/write into the backend container
├── infra/
│   ├── docker-compose.yml            # NEW — this blueprint
│   ├── .env.example                  # NEW — this blueprint
│   ├── .env                          # developer-created (git-ignored), copied from .env.example
│   ├── docker-compose.staging.yml    # owned by Infra.04 — not touched here
│   └── ci/                           # owned by CI_CD.06 — not touched here
└── Makefile                          # NEW file, or NEW targets appended to an existing root Makefile — this blueprint
```

`infra/docker-compose.yml` is the canonical location per the monorepo tree already fixed in `NoorHeroes_Final_Development_Prompt.md` §2.1 (`infra/docker-compose.yml # local dev: postgres, redis, backend, admin-web`). This blueprint does not add `admin-web` to the compose file (that service's Dockerfile/dev workflow is Next.js-specific and is not part of this file's objective, which names only Postgres/Redis/R2-emulation/backend hot-reload) — see §18 for the explicit decision and how to extend the file later without restructuring it.

## 6. APIs, Models, Interfaces, and Data Flow

This file introduces no new application APIs — it wires the environment that the already-implemented `R2StorageService`, `get_db_session`, and Redis pool consume. The one non-obvious interface contract worth specifying precisely is the **dual-endpoint pattern** for S3-compatible presigned URLs, because a naive single-`R2_ENDPOINT_URL` local setup silently produces broken URLs.

**The problem:** `R2StorageService.generate_presigned_upload_url()` must sign a URL with SigV4, which cryptographically binds the signature to a specific `Host`. That signed URL is then handed to a client *outside* the Docker network (a developer's browser, Postman, the mobile app/emulator, or `admin-web` running via `next dev` on the host) to `PUT` the file directly to MinIO. If the backend signs the URL using the Docker-internal service name (`http://minio:9000`), that hostname is unresolvable from outside the Compose network and the upload fails with a DNS error — but if the backend is instead configured to always use `http://localhost:9000`, server-side calls the backend itself makes to MinIO (e.g., a Celery worker fetching an object to run the AV/safety scan steps) fail, because `localhost` inside a container refers to the container itself, not the `minio` service.

**The resolution — two endpoint variables, one bucket:**

| Env var | Value in local dev | Used for |
|---|---|---|
| `R2_ENDPOINT_URL` | `http://minio:9000` | Every **server-side** S3 operation the backend/worker performs directly against the object store (existence checks, `GET`/`HEAD`, downloading an object for the upload-pipeline's scanning steps). Network-reachable from inside the Compose network. |
| `R2_PRESIGN_ENDPOINT_URL` | `http://localhost:${MINIO_API_HOST_PORT}` (default `http://localhost:9000`) | The endpoint used **only** to construct the boto3/aioboto3 client instance passed into `generate_presigned_upload_url()` (and any presigned-GET equivalent). Generating a presigned URL is a local, offline cryptographic signing operation — boto3 never actually dials `R2_PRESIGN_ENDPOINT_URL` to produce it — so the backend container does not need network reachability to `localhost:9000`; it only needs that string to be the *correct* externally-reachable host for the signature to validate when the external client later performs the real `PUT` against it. |

If `R2StorageService` currently takes a single `endpoint_url` constructor argument, add a second, narrowly-scoped client (or a second constructor parameter, e.g. `presign_endpoint_url: str | None = None`, falling back to `endpoint_url` when unset so this remains a no-op in every environment except local dev) used exclusively inside the presign method. Do not change the method signatures or return types callers already depend on — see §18.

**Mobile-emulator note (edge case, not this file's primary surface):** Android emulator's `localhost` resolves to the emulator itself, not the host machine — a device/emulator testing this flow needs `R2_PRESIGN_ENDPOINT_URL`-equivalent overridden to `http://10.0.2.2:9000` (Android's standard host-loopback alias) rather than `localhost`. iOS Simulator shares the host's network namespace, so `localhost` works unmodified there. This is a mobile-app-side configuration concern (`local.properties`/`BuildConfig`, per the environment-tiers table), not something this compose file changes — noted here only so the person configuring mobile local-dev doesn't have to re-derive it.

**End-to-end data flow this stack enables (application logic already implemented, not built by this file):**

```text
1. POST /v1/media/upload/initiate  (parent JWT)
       └─ MediaRouter → MediaService.initiate_upload()
             ├─ validates MIME/size/category
             ├─ R2StorageService.generate_presigned_upload_url()
             │     signed against R2_PRESIGN_ENDPOINT_URL (http://localhost:9000 in dev)
             ├─ MediaRepository.add()  → MediaAsset row, status="pending_upload"
             └─ returns MediaAssetResponse { presigned_url, asset_id }
2. Client performs PUT directly to presigned_url — hits MinIO directly,
   never touches the backend process for the bytes themselves.
3. (Elsewhere, out of this file's scope) the 11-step upload validation
   pipeline / a Celery task later fetches the object using R2_ENDPOINT_URL
   (http://minio:9000, internal) to run AV scan, safety classifiers, etc.
```

## 7. Dependencies and Configuration Requirements

### 7.1 `infra/docker-compose.yml`

```yaml
name: noorheroes-dev

networks:
  noorheroes-dev-network:
    name: noorheroes-dev-network
    driver: bridge

volumes:
  postgres_data:
    name: noorheroes_postgres_data
  redis_data:
    name: noorheroes_redis_data
  minio_data:
    name: noorheroes_minio_data
  backend_venv:
    name: noorheroes_backend_venv

x-backend-env: &backend-env
  ENVIRONMENT: local
  DATABASE_URL: postgresql+asyncpg://${POSTGRES_USER:-noorheroes}:${POSTGRES_PASSWORD:-noorheroes_dev_password}@postgres:5432/${POSTGRES_DB:-noorheroes}
  REDIS_URL: redis://redis:6379/0
  CELERY_BROKER_URL: redis://redis:6379/1
  CELERY_RESULT_BACKEND: redis://redis:6379/2
  R2_ENDPOINT_URL: http://minio:9000
  R2_PRESIGN_ENDPOINT_URL: http://localhost:${MINIO_API_HOST_PORT:-9000}
  R2_ACCESS_KEY_ID: ${MINIO_ROOT_USER:-minioadmin}
  R2_SECRET_ACCESS_KEY: ${MINIO_ROOT_PASSWORD:-minioadmin123}
  R2_BUCKET_NAME: ${R2_BUCKET_NAME:-noorheroes-media-dev}
  R2_REGION: us-east-1
  JWT_SECRET_KEY: ${JWT_SECRET_KEY:-local-dev-insecure-secret-do-not-use-in-staging-or-prod}
  CORS_ALLOW_ORIGINS: "*"
  SENTRY_DSN: ""
  OTEL_SDK_DISABLED: "true"
  LOG_LEVEL: DEBUG
  RUN_MIGRATIONS_ON_BOOT: "true"

services:
  postgres:
    image: postgres:16-alpine
    container_name: noorheroes-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-noorheroes}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-noorheroes_dev_password}
      POSTGRES_DB: ${POSTGRES_DB:-noorheroes}
    ports:
      - "${POSTGRES_HOST_PORT:-5432}:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]
      interval: 5s
      timeout: 5s
      retries: 10
      start_period: 10s
    networks: [noorheroes-dev-network]

  redis:
    image: redis:7-alpine
    container_name: noorheroes-redis
    restart: unless-stopped
    command: ["redis-server", "--appendonly", "yes"]
    ports:
      - "${REDIS_HOST_PORT:-6379}:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 10
      start_period: 5s
    networks: [noorheroes-dev-network]

  minio:
    image: minio/minio:RELEASE.2024-01-16T16-07-38Z
    container_name: noorheroes-minio
    restart: unless-stopped
    command: ["server", "/data", "--console-address", ":9001"]
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER:-minioadmin}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD:-minioadmin123}
    ports:
      - "${MINIO_API_HOST_PORT:-9000}:9000"
      - "${MINIO_CONSOLE_HOST_PORT:-9001}:9001"
    volumes:
      - minio_data:/data
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:9000/minio/health/live || exit 1"]
      interval: 5s
      timeout: 5s
      retries: 10
      start_period: 10s
    networks: [noorheroes-dev-network]

  minio-init:
    image: minio/mc:RELEASE.2024-01-13T08-44-48Z
    container_name: noorheroes-minio-init
    depends_on:
      minio:
        condition: service_healthy
    entrypoint: >
      /bin/sh -c "
      mc alias set local http://minio:9000 ${MINIO_ROOT_USER:-minioadmin} ${MINIO_ROOT_PASSWORD:-minioadmin123} &&
      mc mb --ignore-existing local/${R2_BUCKET_NAME:-noorheroes-media-dev} &&
      mc anonymous set download local/${R2_BUCKET_NAME:-noorheroes-media-dev} &&
      echo 'MinIO bucket bootstrap complete.'
      "
    networks: [noorheroes-dev-network]
    restart: "no"

  backend:
    build:
      context: ../backend
      dockerfile: Dockerfile.dev
    container_name: noorheroes-backend
    restart: unless-stopped
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      minio-init:
        condition: service_completed_successfully
    ports:
      - "${BACKEND_HOST_PORT:-8000}:8000"
    volumes:
      - ../backend:/app
      - backend_venv:/app/.venv
    environment: *backend-env
    command: >
      uv run uvicorn src.noorheroes.main:app
      --host 0.0.0.0 --port 8000 --reload --reload-dir /app/src
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:8000/healthz || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 10
      start_period: 20s
    networks: [noorheroes-dev-network]

  backend-worker:
    build:
      context: ../backend
      dockerfile: Dockerfile.dev
    container_name: noorheroes-backend-worker
    restart: unless-stopped
    profiles: ["worker"]
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      minio-init:
        condition: service_completed_successfully
    volumes:
      - ../backend:/app
      - backend_venv:/app/.venv
    environment:
      <<: *backend-env
      RUN_MIGRATIONS_ON_BOOT: "false"
    command: ["uv", "run", "celery", "-A", "src.noorheroes.core.celery_app", "worker", "--loglevel=INFO"]
    networks: [noorheroes-dev-network]
```

> **Pin freshness note:** `postgres:16-alpine`, `redis:7-alpine`, `minio/minio:RELEASE.2024-01-16T16-07-38Z`, and `minio/mc:RELEASE.2024-01-13T08-44-48Z` are known-good baselines as of this document's authoring. Per `NoorHeroes_Final_Development_Prompt.md` §1's own instruction to "re-verify nothing here has been superseded... before committing to it," check each tag against its vendor's current release feed at implementation time and update this file plus `infra/.env.example` together, recording the change as a one-line ADR if the bump is non-trivial (e.g., a Postgres major-version bump).

### 7.2 `backend/Dockerfile.dev`

```dockerfile
# Local-development-only image. NOT used for staging/production builds — see backend/Dockerfile
# (multi-stage builder + slim runtime, owned by the CI build stage / Infra.04) for that image.
# This image trades final image size/attack-surface for fast rebuilds and live hot-reload via
# the bind-mounted source volume defined in infra/docker-compose.yml.

FROM python:3.12-slim

# curl: container healthcheck. build-essential + libpq-dev: safety net for any dependency
# that needs to compile a C extension (most, e.g. asyncpg, ship manylinux wheels and won't need
# this, but a dev image failing to build because of a transitively-added source dependency is a
# worse failure mode than a slightly larger image).
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Pinned uv binary — re-verify against astral-sh's current release at implementation time.
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /usr/local/bin/

WORKDIR /app

# Lockfile-only copy first so `uv sync` is Docker-layer-cached across rebuilds that don't touch
# dependencies. The bind mount at container *run* time overlays this COPY with live source —
# this build-time COPY exists so `docker compose build` alone still produces a runnable image.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

COPY . .
RUN uv sync --frozen

COPY docker-entrypoint.dev.sh /usr/local/bin/docker-entrypoint.dev.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.dev.sh

ENTRYPOINT ["docker-entrypoint.dev.sh"]
CMD ["uv", "run", "uvicorn", "src.noorheroes.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "/app/src"]
```

### 7.3 `backend/docker-entrypoint.dev.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

if [ "${RUN_MIGRATIONS_ON_BOOT:-true}" = "true" ]; then
  echo "[docker-entrypoint.dev] Running Alembic migrations (alembic upgrade head)..."
  uv run alembic upgrade head
  echo "[docker-entrypoint.dev] Migrations complete."
else
  echo "[docker-entrypoint.dev] RUN_MIGRATIONS_ON_BOOT=false — skipping migrations."
fi

exec "$@"
```

### 7.4 `infra/.env.example`

```dotenv
# Copy this file to infra/.env before running `make dev` / `docker compose up`:
#     cp infra/.env.example infra/.env
#
# Every value below is a non-secret, local-only default. Never reuse any of these values in
# CI, Dev/QA, Staging, or Production — those tiers are provisioned by Infra.01, and their
# secrets are managed per Infra.02 (gitleaks/trufflehog scanning + a real secrets manager),
# not this file. infra/.env is git-ignored; this .env.example file is the committed checklist.
# The compose file also has inline defaults matching these, so the stack still runs with zero
# .env file present — copying this file is for the ability to override values, not a hard
# requirement to start the stack.

# --- Postgres ---
POSTGRES_USER=noorheroes
POSTGRES_PASSWORD=noorheroes_dev_password
POSTGRES_DB=noorheroes
POSTGRES_HOST_PORT=5432

# --- Redis ---
REDIS_HOST_PORT=6379

# --- MinIO (R2-compatible object storage emulator) ---
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin123
MINIO_API_HOST_PORT=9000
MINIO_CONSOLE_HOST_PORT=9001
R2_BUCKET_NAME=noorheroes-media-dev

# --- Backend ---
BACKEND_HOST_PORT=8000
JWT_SECRET_KEY=local-dev-insecure-secret-do-not-use-in-staging-or-prod
```

### 7.5 Root `Makefile` targets

```makefile
COMPOSE := docker compose -f infra/docker-compose.yml --env-file infra/.env

.PHONY: dev dev-build dev-down dev-destroy dev-logs dev-ps dev-shell dev-migrate dev-worker

dev: ## Start postgres, redis, minio, backend (hot reload) in the foreground
	$(COMPOSE) up --build

dev-build: ## Rebuild the backend dev image without starting the stack
	$(COMPOSE) build backend

dev-down: ## Stop the stack; volumes (DB/Redis/MinIO data) are preserved
	$(COMPOSE) down

dev-destroy: ## Stop the stack AND delete all volumes — full reset, all local data is lost
	$(COMPOSE) down -v

dev-logs: ## Tail backend logs
	$(COMPOSE) logs -f backend

dev-ps: ## Show stack container status
	$(COMPOSE) ps

dev-shell: ## Open a shell inside the running backend container
	$(COMPOSE) exec backend bash

dev-migrate: ## Run Alembic migrations manually against the running stack
	$(COMPOSE) exec backend uv run alembic upgrade head

dev-worker: ## Start the stack plus the Celery worker (optional profile)
	$(COMPOSE) --profile worker up --build
```

**Zero-to-running developer workflow:**

```bash
git clone <repo> && cd noorheroes
cp infra/.env.example infra/.env
make dev
# … stack builds and starts; backend becomes healthy once
#   Postgres/Redis/MinIO are healthy, migrations have run, and /healthz returns 200 …
curl -sf http://localhost:8000/healthz && echo OK
```

## 8. Database/Storage Requirements

- **Postgres**: a single database (`POSTGRES_DB`, default `noorheroes`) is created automatically by the official image's first-boot `initdb` from `POSTGRES_USER`/`POSTGRES_PASSWORD`/`POSTGRES_DB`. Schema is entirely owned by the backend's existing Alembic migration chain (`backend/alembic/`) — this file does not define or hand-write any schema; `docker-entrypoint.dev.sh` simply runs `alembic upgrade head` against whatever migrations already exist in the repo at container start.
- **Redis**: no schema; keys are namespaced by the application (rate-limit counters, cache entries, session/step-up markers) and by Celery (broker/result backend on separate logical DB indices 1/2, per §4). AOF persistence (`appendonly yes`) means Redis state survives a plain `docker compose restart`/`down` (without `-v`), which materially helps when debugging a rate-limit or cache-related bug across a few restarts.
- **MinIO**: one bucket, `R2_BUCKET_NAME` (default `noorheroes-media-dev`), created by `minio-init` with public-read (`mc anonymous set download`) so locally-uploaded media can be fetched back over HTTP the same way a CDN-fronted R2 bucket would serve it in production, without needing a second presigned-GET round trip for every read during manual testing. **Do not carry the public-read bucket policy forward to any real environment** — Terraform-provisioned staging/production R2 buckets (`Infra.04`) must use CDN/signed-URL access per the stack's own security posture (`Cloudflare CDN, signed URLs/cookies`), never a public bucket policy; this is a local-dev-only convenience.
- **Volumes and persistence** are covered in full in §11.

## 9. Authentication, Authorization, Validation, and Security Considerations

This stack **does not implement** any authentication/authorization logic — that is entirely the already-built `core/deps.py`/`core/security.py` code, running unmodified inside the `backend` container. What this file is responsible for is not undermining that code's security posture even in a throwaway local environment:

- **`JWT_SECRET_KEY` default is intentionally a clearly-labeled dummy value** (`local-dev-insecure-secret-do-not-use-in-staging-or-prod`). It signs tokens that are only ever verified by this same local backend process, so its weakness is inconsequential *as long as it is never reused elsewhere*. Flag this literal string for `Infra.02`'s gitleaks/trufflehog allowlist (it will otherwise look like a leaked secret pattern to a naive scanner) rather than disabling the scan.
- **MinIO root credentials** (`minioadmin`/`minioadmin123`) are equally dummy, bound only to `localhost`/the Compose network, never to a publicly reachable endpoint. Same rule: never reuse in any other tier.
- **CORS is wide open (`CORS_ALLOW_ORIGINS=*`)** in this stack only, so `admin-web`'s `next dev` server (or any host-side tool) can call the API without CORS friction during local development. This must never be the value in any non-local `Settings` configuration — confirm the `Settings` class's default (not this file's override) is restrictive outside `Environment.LOCAL`.
- **No TLS.** Every service in this stack talks plain HTTP/plain TCP on `localhost`. This is acceptable and expected for a local-only stack (see §15) and must never be read as a template for staging/production, where TLS termination is Nginx/Kong/Envoy's job per the stack table.
- **The dev image runs as root** inside the container (no `USER` directive in `Dockerfile.dev`). This is a deliberate, scoped exception: running as a non-root UID that doesn't match the host developer's UID is a common source of bind-mount permission friction on Linux (files the container creates become unwritable/undeletable by the host user without a manual `chown`), and this image is never deployed anywhere a root-inside-container posture matters. The production `backend/Dockerfile` (out of scope here) is expected to run as a non-root user — do not copy this exception into it.
- **Object-storage bucket is public-read** in this stack (§8) — a deliberate, documented, dev-only relaxation, not a security decision to replicate elsewhere.
- Validation of the compose file's own correctness (`docker compose config` parses cleanly, no unresolved required variables) is part of the acceptance criteria in §14, not a security control per se, but it is the first line of defense against a malformed env var silently disabling a security-relevant default.

## 10. Error Handling and Edge Cases

| Situation | Cause | Resolution |
|---|---|---|
| `bind: address already in use` on `up` | Another process (a native Postgres/Redis install, another project's compose stack) already holds `5432`/`6379`/`9000`/`9001`/`8000` on the host | Override the conflicting `*_HOST_PORT` variable in `infra/.env` (e.g. `POSTGRES_HOST_PORT=5433`) — the container-internal port and every other service's DNS-based reference to it (`postgres:5432`, `minio:9000`) is unaffected, only the host-side publish mapping changes. |
| Backend container starts, dependency `ImportError` on a package that was added to `pyproject.toml` on the host but not yet installed in the image | The bind mount overlays source, but does **not** re-run `uv sync` — installed packages live in the `backend_venv` named volume, frozen at last `docker build`/`uv sync` | Run `make dev-build` (rebuilds the image, re-running `uv sync --frozen`) or `docker compose exec backend uv sync` for a same-session fix without a full rebuild. Either requires `uv.lock` to already reflect the new dependency (`uv add <pkg>` on the host, or `uv lock` after a manual `pyproject.toml` edit) — this stack does not auto-update the lockfile. |
| `backend_venv` volume becomes stale/corrupted after repeated dependency churn | Long-lived named volume accumulates partial installs across many `uv sync` runs during active development | `docker volume rm noorheroes_backend_venv` (safe — DB/MinIO data untouched) then `make dev-build`; or the blunt `make dev-destroy` if you're fine losing DB/Redis/MinIO data too. |
| Backend container stuck in a restart loop, logs show an Alembic error | A migration fails to apply (bad migration, DB in an unexpected state from manual tinkering) | `make dev-logs` to read the Alembic traceback; fix the migration or the DB state (`make dev-shell` → `uv run alembic downgrade -1`, or `make dev-destroy` to nuke the DB volume and start clean); `restart: unless-stopped` retries automatically once the fix lands. |
| Presigned upload `PUT` fails with a DNS/connection error from a browser or Postman | `R2_PRESIGN_ENDPOINT_URL` was left pointing at the Docker-internal `http://minio:9000` instead of `http://localhost:9000` (see §6) | Confirm the env var split from §6 is actually wired into `R2StorageService`'s presign code path, not just present-but-unused in the container's environment. |
| Presigned upload fails specifically from an Android emulator, works fine from a browser | Android emulator's `localhost` refers to the emulator, not the host machine | Mobile-side config must use `10.0.2.2` instead of `localhost` for this flow (see §6's mobile-emulator note) — not a compose-file change. |
| `minio-init` container exits non-zero / bucket never appears | Race or transient MinIO startup failure before `mc alias set` runs, despite the `service_healthy` gate | `docker compose logs minio-init`; safe to simply rerun with `docker compose up minio-init` (idempotent — `mc mb --ignore-existing` and `mc anonymous set` are safe to repeat). |
| Files the backend container creates (e.g., `__pycache__`) show up root-owned on the host and resist a normal `rm` | Dev image runs as root (§9) | Either `sudo rm -rf backend/**/__pycache__` occasionally, or add a `.dockerignore`/`.gitignore` entry so it's cosmetic-only and never committed; do not "fix" this by switching the dev image to non-root without re-testing bind-mount write access end-to-end. |
| A pytest run using the existing Testcontainers harness appears to hang or fails to bind a port | Misdiagnosed as a conflict with this compose stack | It almost never is — see §12; Testcontainers allocates ephemeral host ports per container, distinct from this stack's fixed `5432`/`6379`. If it genuinely hangs, the far more likely cause is Docker Engine itself not running/reachable (Testcontainers needs the Docker socket) — verify with `docker info` before assuming a port collision with this stack. |
| `docker compose up` succeeds with zero `.env` file present | Every variable in `x-backend-env` and each service's `environment`/`ports` block has a `${VAR:-default}` fallback | Working as designed — flagged here only so it's understood as intentional (§9's dummy-secret defaults), not a bug that the stack "should" have failed loudly without a `.env` file. |

## 11. State Management and Lifecycle Considerations

- **`docker compose up` / `make dev`**: starts all default-profile services; `backend`/`backend-worker` wait on `postgres`/`redis`/`minio-init` via `depends_on: condition: service_healthy` / `service_completed_successfully`, so a fresh `up` on an empty machine deterministically orders "databases ready → bucket bootstrapped → migrations run → app serves traffic," never a race.
- **`docker compose down` / `make dev-down`**: stops and removes containers, **preserves** the four named volumes (`postgres_data`, `redis_data`, `minio_data`, `backend_venv`). A subsequent `up` resumes with the same DB rows, Redis keys, and uploaded MinIO objects intact — this mirrors how a developer expects to pause work for the day and resume it, not lose their local dataset every time.
- **`docker compose down -v` / `make dev-destroy`**: additionally deletes all four named volumes — full reset. Use this deliberately (a corrupted local DB, a schema you want to rebuild from a clean migration history, switching branches with divergent migrations). This is the local-dev equivalent of "delete my dev database," not something any other command in this file does implicitly.
- **Restart policy**: `unless-stopped` on every long-running service (not `minio-init`, which is intentionally `restart: "no"` — a one-shot job re-running forever would be a bug, not a feature). This means a host reboot with Docker configured to start on boot will bring the whole stack back up unattended, matching "individual developer machines" convenience expectations from the environment-tiers table.
- **Hot reload lifecycle**: Uvicorn's `--reload` watches `/app/src` (the bind-mounted host `backend/src/`) and restarts the ASGI app process — not the container — on file change. Container-level state (the `backend_venv` volume, any long-lived connections the *old* process held) is unaffected; only the Python process restarts, typically sub-second for this codebase's size.
- **Migration idempotency**: `alembic upgrade head` is safe to run on every container start (including every `docker compose restart backend`) because Alembic no-ops when the DB is already at head. This is why running it unconditionally in the entrypoint (rather than only on first-ever start) is the correct default, not wasted work.
- **Data does NOT survive** an explicit volume deletion, a `docker system prune --volumes`, or a fresh clone onto a different machine — this stack is single-machine, disposable-by-design local state, never a backup of anything.

## 12. Integration Points with Existing Modules

**Backend application code (`src/noorheroes/**`)** — this stack's `backend`/`backend-worker` services run that code entirely unmodified, importing it as `src.noorheroes.main:app` / `src.noorheroes.core.celery_app`, matching the module paths already documented in `FAST-API-INSTRUCTIONS.md` (e.g., its own `python -m src.noorheroes.scripts.export_openapi_schema` invocation convention, confirming `src` is imported relative to the `backend/` working directory — which is exactly `WORKDIR /app` in `Dockerfile.dev`, with `backend/` bind-mounted to `/app`).

**R2 media pipeline** — this stack supplies the object-storage substrate (`R2_ENDPOINT_URL`/`R2_PRESIGN_ENDPOINT_URL` pointed at MinIO) that `R2StorageService` and `MediaService.initiate_upload()` already use; the 11-step content-safety pipeline that later consumes uploaded objects is unaffected by whether the endpoint is real R2 or MinIO, by design — that is precisely why the dual-endpoint, S3-API-compatible approach was chosen over a bespoke R2-specific mock.

**Testcontainers-based integration test suite (`backend/tests/conftest.py`) — the critical distinction this file must not blur:**

| | This compose stack (`infra/docker-compose.yml`) | Testcontainers (`backend/tests/conftest.py`, already implemented) |
|---|---|---|
| Lifecycle | Long-running; started once (`docker compose up`), stays up across many dev-loop iterations | Ephemeral per pytest session/run — containers are created and torn down by the test process itself via `testcontainers-python` |
| Ports | Fixed, host-published (`5432`, `6379`, ... configurable in `infra/.env`) | Dynamically allocated free host ports per container instance, resolved programmatically inside the test fixtures (never hardcoded) |
| Data | Persistent across restarts (named volumes, §11) | Always starts from a fresh, empty container; discarded at teardown, never shared between test runs |
| Who starts it | The developer, explicitly (`make dev`) | pytest itself, automatically, whenever the integration test suite runs |
| Purpose | Manual/interactive local development: running the API, hitting endpoints by hand, exercising `admin-web`/mobile against a real backend, Celery task debugging | Automated, hermetic, reproducible integration tests — must pass identically on a clean CI runner with nothing else running |

**They do not depend on each other and must never be made to.** A developer can run `pytest` (Testcontainers-backed) at any time — with this compose stack up, down, or never started at all — and get identical results, because Testcontainers' dynamic port allocation means there is no collision even if both happen to be running Postgres/Redis simultaneously on the same machine. Do not "optimize" this by pointing the test suite's `DATABASE_URL`/`REDIS_URL` at this compose stack's fixed ports — that would silently make CI (which has no such stack running) diverge from local test runs, and would let stale data from a developer's long-running dev database leak into what must be hermetic tests.

**CI (`docker-compose.ci.yml`, `CI_CD.06`, not built by this file)** similarly must not import or extend `infra/docker-compose.yml` — CI's ephemeral provisioning is that file's own responsibility, kept intentionally separate so a change to the dev-convenience stack (e.g., adding `backend-worker`) can never accidentally change what CI spins up.

**`admin-web`** is not a service in this compose file (see §5/§18) — it is expected to run via its own `pnpm dev`/`next dev` on the host, pointed at `http://localhost:8000` (this stack's published backend port) via its own env config. This keeps admin-web's genuinely separate build/dev toolchain (Node/pnpm, not Docker) out of this file's scope while still working against this stack's backend out of the box, since `CORS_ALLOW_ORIGINS=*` (§9) already permits it.

## 13. Development Steps in the Correct Implementation Order

1. Confirm `backend/pyproject.toml` exists and inspect whether it already commits to `uv` or Poetry (per `NoorHeroes_Final_Development_Prompt.md` §3, the decision was left open). If it already uses Poetry, reconcile per §18 before proceeding — do not silently introduce a second, conflicting dependency manager.
2. Add `backend/Dockerfile.dev` (§7.2) and `backend/docker-entrypoint.dev.sh` (§7.3, `chmod +x` on the host before committing so the executable bit survives Git).
3. Create `infra/` if it does not yet exist (it is named in the monorepo tree but may not be physically present until `Infra.01`/this file creates it); add `infra/docker-compose.yml` (§7.1).
4. Add `infra/.env.example` (§7.4); do **not** commit an actual `infra/.env` — add `infra/.env` to the repo's root `.gitignore` if not already covered by a broader `.env` ignore rule.
5. Add or extend the root `Makefile` with the `dev*` targets (§7.5).
6. `cp infra/.env.example infra/.env`, then `make dev` from a clean checkout and confirm the ordering in §11 happens without manual intervention: Postgres/Redis/MinIO become healthy → `minio-init` completes and exits `0` → `backend` runs `alembic upgrade head` → `backend` becomes healthy → `curl localhost:8000/healthz` returns `200`.
7. Confirm the dual-endpoint presign pattern from §6: call `POST /v1/media/upload/initiate` (with a valid parent JWT obtained via the existing auth endpoints) and verify the returned `presigned_url` host is `localhost:<MINIO_API_HOST_PORT>`, then actually perform the `PUT` from the host (e.g., via `curl`) and confirm the object appears in the MinIO console (`http://localhost:9001`) inside the configured bucket.
8. If `R2StorageService` does not yet support a distinct presign-endpoint override, add the minimal constructor/parameter change described in §6 — this is the one application-code touch this blueprint may require, scoped exactly to that method's client construction, nothing else in `R2StorageService` or any caller's signature changes.
9. Verify `make dev-worker` starts `backend-worker` cleanly alongside the default services and that it does **not** re-run migrations (`RUN_MIGRATIONS_ON_BOOT=false` takes effect — check its logs for the "skipping migrations" line).
10. Verify `make dev-down` then `make dev` round-trips without data loss (a row inserted before `dev-down` is still present after the next `make dev`), and separately that `make dev-destroy` then `make dev` produces a fully empty, freshly-migrated database.
11. Run the existing Testcontainers-backed `pytest` suite **both** with this stack up and with it fully stopped (`make dev-down`) and confirm identical pass/fail results in both cases, proving the isolation described in §12.
12. Document the working `make dev` flow in the repo's top-level README (a one-paragraph "local development" section pointing at this file) if no such section exists yet — this blueprint's Definition of Done (§17) requires the workflow to be discoverable, not just functional.

## 14. Testing Strategy and Acceptance Criteria

| # | Check | Command | Expected result |
|---|---|---|---|
| 1 | Compose file is syntactically valid and every required variable resolves | `docker compose -f infra/docker-compose.yml config` | Exits `0`, prints the fully-resolved config with no `WARN` about missing required variables |
| 2 | Fresh stack boots cleanly from an empty checkout | `cp infra/.env.example infra/.env && make dev` | All services reach a healthy/completed state; no container in a restart loop after 60s |
| 3 | Postgres reachable and correct DB present | `docker compose -f infra/docker-compose.yml exec postgres psql -U noorheroes -d noorheroes -c '\dt'` | Lists the tables created by `alembic upgrade head` (non-empty once migrations exist) |
| 4 | Redis reachable | `docker compose -f infra/docker-compose.yml exec redis redis-cli ping` | `PONG` |
| 5 | MinIO bucket exists and is bootstrapped | `docker compose -f infra/docker-compose.yml logs minio-init` | Contains `MinIO bucket bootstrap complete.`; `minio-init` container status is `Exited (0)` |
| 6 | Backend liveness | `curl -sf -o /dev/null -w '%{http_code}' http://localhost:8000/healthz` | `200` |
| 7 | Backend readiness (proves DB + Redis connectivity from inside the app) | `curl -sf -o /dev/null -w '%{http_code}' http://localhost:8000/readyz` | `200` |
| 8 | Hot reload works | Edit a route's response string in `backend/src/noorheroes/...`, save, re-`curl` that route within ~5s, no manual restart | Response reflects the edit without running any `docker compose` command |
| 9 | Presigned upload round-trip | Perform §13 step 7's `POST /v1/media/upload/initiate` → `PUT` → MinIO console check | Object visible in the bucket under the returned `asset_id`-derived key |
| 10 | Migrations re-run safely | `make dev-shell` → `uv run alembic upgrade head` a second time while stack is already running | Exits `0`, no-ops (already at head), no error |
| 11 | Data persists across `dev-down`/`dev` | Insert a row (or note an object in MinIO) → `make dev-down` → `make dev` → re-query | Row/object still present |
| 12 | Full reset works | `make dev-destroy` → `make dev` | Database is empty except for the fresh migration history; MinIO bucket is empty (re-bootstrapped) |
| 13 | Optional worker profile | `make dev-worker` | `backend-worker` container reaches a running state, logs show Celery connected to the Redis broker, and logs confirm migrations were skipped |
| 14 | Testcontainers isolation (this file must not break it) | Run the existing `pytest` integration suite with the stack up, then again with `make dev-down` | Identical results in both runs; no port-binding errors attributable to this stack in either run |
| 15 | Zero-`.env` fallback | `rm infra/.env` (or never create it) → `make dev` | Stack still starts successfully using the compose file's inline defaults |

**Definition of "acceptance":** all 15 checks pass on a clean checkout on at least one Linux and one macOS (or equivalent) development machine, run by someone who has never seen this stack before, using only this document plus a `git clone` and a working Docker Engine/Compose install — no undocumented tribal knowledge required.

## 15. Production-Readiness Considerations

**This entire file is dev-only and never ships to production. Say this plainly wherever this blueprint is referenced elsewhere in the project:**

- `infra/docker-compose.yml` is not deployed anywhere; it has no staging/production analog by design (that is `docker-compose.staging.yml` / Terraform-managed infrastructure, owned by `Infra.04`, using genuinely managed Postgres/Redis/R2 rather than containers-on-a-laptop).
- `backend/Dockerfile.dev` is never built or referenced by any CI/CD pipeline stage that produces a deployable artifact — the CI build stage (`CI_CD.06`) builds `backend/Dockerfile` (the production multi-stage image), not this file.
- Every credential in this file (`JWT_SECRET_KEY`, MinIO root user/password, Postgres password) is a hardcoded, publicly-visible-in-this-document dummy value. **None of it is a template to "just change the values" for a real environment** — real environments get real secrets from a real secrets manager per `Infra.02`, provisioned through entirely different mechanisms (env injection at deploy time, not a checked-in `.env.example`).
- MinIO stands in for Cloudflare R2 locally; it is never itself deployed as the production object store. The dual-endpoint presign pattern (§6) exists specifically because it's a workable *local* solution — production's single R2 endpoint plus CDN/signed-URL delivery (per the stack table) does not need this split at all, since there's no Docker-network-vs-host distinction in a real deployment.
- Running as root inside the dev image (§9) and CORS-wide-open (§9) are both exceptions that must not appear in `backend/Dockerfile`/any non-local `Settings` configuration — flagged twice in this document (§9 and here) because it is the single easiest mistake for this exception to quietly leak into a "just copy the dev config" shortcut later.
- If a future need arises to demo this stack somewhere semi-persistent (a shared internal demo box, not production), that is a distinct, deliberately-scoped exception requiring its own review — not something this file's existence implicitly authorizes.

## 16. Dependencies and Prerequisites

- **Docker Engine** ≥ 24.x with the Compose V2 plugin (`docker compose`, not the standalone legacy `docker-compose` v1 binary — this file's syntax, `profiles` and `depends_on: condition:`, requires Compose V2's Compose Specification support).
- **`make`** available on the developer's `PATH` (pre-installed on macOS/Linux; Windows developers use WSL2, which is already an implicit requirement for running Linux containers with reasonable performance).
- At least **~2 GB of free disk** for the four named volumes plus pulled images on first run (Postgres/Redis/MinIO/MinIO-client/python:3.12-slim-based backend image).
- Outbound network access to `docker.io`/`ghcr.io` on first `make dev` (to pull `postgres`, `redis`, `minio`, `minio/mc`, `python:3.12-slim`, `ghcr.io/astral-sh/uv`) — no other outbound access is required to run this stack; it is fully self-contained/offline-capable after the first successful pull.
- `backend/pyproject.toml` and (if the dependency-manager decision in §18 is upheld) `backend/uv.lock` must already exist in the repo — this file's `Dockerfile.dev` copies and `uv sync`s them, it does not generate them.
- Completion of `Infra.01-environment-tiers-provisioning.md` conceptually (the `local` tier's existence/definition), though this file's own artifacts can be authored in parallel — the dependency is about the environment-tier *concept* being settled (naming, `Environment.LOCAL` enum value already exists per `core/settings.py`), not a hard build-order blocker.

## 17. Definition of Done

- [ ] `infra/docker-compose.yml`, `infra/.env.example`, `backend/Dockerfile.dev`, `backend/docker-entrypoint.dev.sh` exist at the exact paths specified in §5, committed to the repo.
- [ ] Root `Makefile` exposes `dev`, `dev-build`, `dev-down`, `dev-destroy`, `dev-logs`, `dev-ps`, `dev-shell`, `dev-migrate`, `dev-worker`.
- [ ] All 15 checks in §14 pass on a clean checkout.
- [ ] The dual-endpoint presign pattern (§6) is verified working end-to-end (§13 step 7), including confirming (or adding, per §13 step 8) `R2StorageService` support for it.
- [ ] Testcontainers-backed `pytest` suite passes identically whether this stack is running or fully stopped (§12, §14 check 14) — no coupling introduced between the two.
- [ ] No change was made to `backend/Dockerfile` (production image), any file under `infra/k8s/`, `infra/terraform/`, `infra/docker-compose.staging.yml`, or `infra/ci/` — this file's blast radius is exactly the paths in §5.
- [ ] No `Settings`/`R2StorageService` default behavior was changed for any non-`local` environment.
- [ ] `infra/.env` is confirmed git-ignored (not committed), while `infra/.env.example` is committed and current.
- [ ] A short "local development" pointer exists in the repo's top-level README (§13 step 12).
- [ ] Every hardcoded dev-only secret-shaped value in this file's artifacts is either already gitleaks-allowlisted or flagged as needing to be, coordinated with whoever implements `Infra.02`.

## 18. Assumptions or Decisions the Coding Agent Must Follow

1. **`uv` is the backend dependency manager for this file's purposes.** `NoorHeroes_Final_Development_Prompt.md` §3 explicitly leaves this open ("`uv` (fast, lockfile-based) or Poetry — pick one"). This blueprint picks `uv`. If, at implementation time, `backend/pyproject.toml` already contains Poetry-specific configuration (a `[tool.poetry]` table) rather than a PEP 621 `[project]` table `uv` expects, treat that as a real conflict to resolve explicitly (raise it, don't silently dual-wield both tools) rather than forcing this file's choice through — but do not default to Poetry without confirming the mismatch first.
2. **MinIO is the R2 emulator**, not a hand-rolled S3-compatible mock, not Cloudflare's `wrangler`/Miniflare tooling. Justification is in §3/§7.1's pin-freshness note. Do not substitute a different S3-compatible server (e.g., `localstack`) without updating this document — LocalStack's S3 implementation is heavier (full AWS-service emulation) for a need that is purely "one S3-compatible bucket."
3. **`backend-worker` (Celery) is an addition beyond the four services named in this blueprint's stated objective** (Postgres, Redis, R2 emulation, backend hot-reload). It is included, gated behind the `worker` Compose profile so it never starts by accident, because the backend's own stack requires Celery for entire feature families (localization tasks, notification dispatch) that would otherwise have zero local-dev story. If a reviewer decides this is out of scope, it is the one component of this file that can be removed without touching any other section's correctness — nothing else in this document depends on `backend-worker` existing.
4. **`admin-web` is deliberately not a service in this compose file**, even though the monorepo tree's own comment (`NoorHeroes_Final_Development_Prompt.md` §2.1) lists `infra/docker-compose.yml # local dev: postgres, redis, backend, admin-web`. This blueprint's explicit objective names only "Local Postgres 16, Redis, R2-compatible object-storage emulation, and backend hot-reload" — admin-web's Next.js dev workflow (`pnpm dev`, no Docker needed for hot reload the way Python needs a container) is a different enough toolchain that bundling it here would be scope creep against this file's stated objective. `admin-web` can be added as an additional service in a future revision of this same file (`node:XX-alpine`-based, per the stack table) without restructuring anything above — the `noorheroes-dev-network` and `CORS_ALLOW_ORIGINS=*` are already set up to accommodate it either way (containerized or host-run).
5. **The dual-endpoint presign pattern (§6) may require a small, scoped change to `R2StorageService`** if it does not already expose a way to sign presigned URLs against a different endpoint than the one used for direct object operations. This is the only application-code touch this blueprint authorizes, and it must be additive (a new optional constructor/parameter defaulting to current behavior) — never a change to any existing method signature, return type, or non-local-environment behavior.
6. **Exact environment-variable names** (`DATABASE_URL`, `REDIS_URL`, `R2_ENDPOINT_URL`, `R2_PRESIGN_ENDPOINT_URL`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET_NAME`, `R2_REGION`, `JWT_SECRET_KEY`, `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`) are this blueprint's best-effort naming following the already-documented `Settings`/`R2StorageService` responsibilities in `FAST-API-INSTRUCTIONS.md`, since that document doesn't enumerate the actual Pydantic field names. **Before wiring the compose file's `environment:` block against the real `Settings` class, diff these names against `src/noorheroes/core/settings.py`'s actual field names** (Pydantic Settings' default env-var mapping is the upper-snake-case of the field name) and rename only the *keys* in `x-backend-env`/`.env.example` to match — never change what each variable's *value* represents.
7. **Image tags are pinned baselines, explicitly flagged as re-verify-before-use** (§7.1's pin-freshness note) — do not treat the specific dated MinIO release tags or the `uv` image tag as immutable; re-pin to current stable releases at implementation time per the source document's own stated pinning discipline, and keep this file's tags in sync with whatever gets pinned.
8. **Migrations run automatically on every `backend` container start**, gated by `RUN_MIGRATIONS_ON_BOOT` (default `true`), not left as a manual step. If the team later decides automatic migrations-on-boot is undesirable even for local dev (e.g., wanting explicit control before every reload), flip the compose file's default to `false` and update `make dev`'s documented workflow to add a `make dev-migrate` step — but do not remove the entrypoint script's capability to do either, since `backend-worker` relies on being able to explicitly opt out (`RUN_MIGRATIONS_ON_BOOT: "false"`) regardless of what `backend`'s default is.

---

## AI Agent Development Prompt

Implement the local Docker Compose development stack for the NoorHeroes backend exactly as specified in this document. Follow it precisely — do not redesign the architecture, rename the chosen services, or "improve" the approach with a different toolset.

**What to build, and exactly where:**
1. `infra/docker-compose.yml` — use the full YAML in §7.1 verbatim as your starting point (adjust only the image-tag pins per §7.1's freshness note and the env-var names per §18 item 6, after diffing against the real `src/noorheroes/core/settings.py`).
2. `backend/Dockerfile.dev` — use §7.2 verbatim.
3. `backend/docker-entrypoint.dev.sh` — use §7.3 verbatim; `chmod +x` it.
4. `infra/.env.example` — use §7.4 verbatim.
5. Root `Makefile` — add the targets in §7.5 (create the file if it doesn't exist, append the targets if it does — do not remove any existing targets).

**Conventions to follow:**
- The backend's existing bounded-context module layout, entrypoint (`src.noorheroes.main:app`), and health-probe routes (`/healthz`, `/readyz`) are already implemented and documented in `FAST-API-INSTRUCTIONS.md` — this stack runs that code unmodified; it does not restructure it.
- Dependency manager is `uv` (§18 item 1) — reconcile with `backend/pyproject.toml` first if it's already Poetry-configured; don't silently introduce a second tool.
- Object storage emulator is MinIO, S3-API-compatible, standing in for Cloudflare R2 (§3) — do not substitute LocalStack or a custom mock.
- Implement the dual-endpoint presign pattern from §6 exactly (`R2_ENDPOINT_URL` for server-to-storage calls, `R2_PRESIGN_ENDPOINT_URL` for the client that signs presigned URLs) — this is the one subtle correctness requirement in this file most likely to be gotten wrong if skimmed.

**What NOT to change:**
- `backend/Dockerfile` (the production multi-stage image) — untouched.
- Anything under `infra/k8s/`, `infra/terraform/`, `infra/docker-compose.staging.yml`, `infra/ci/` — all owned by other blueprints (`Infra.04`, `CI_CD.06`).
- Any `Settings`/`R2StorageService` default behavior for non-`local` environments.
- The Testcontainers-based `backend/tests/conftest.py` harness — do not point it at this compose stack's fixed ports, do not make it depend on this stack being up in any way (§12).
- Any existing method signature on `R2StorageService` — the one permitted change is an additive, optional presign-endpoint override (§18 item 5), never a breaking change to an existing caller.

**How to verify you're done (run every one of these before considering the task complete):**
```bash
docker compose -f infra/docker-compose.yml config                 # (1) valid, no missing-var warnings
cp infra/.env.example infra/.env && make dev                      # (2) fresh boot, no restart loops
curl -sf -o /dev/null -w '%{http_code}\n' http://localhost:8000/healthz   # (3) must print 200
curl -sf -o /dev/null -w '%{http_code}\n' http://localhost:8000/readyz    # (4) must print 200
docker compose -f infra/docker-compose.yml logs minio-init | grep 'bootstrap complete'  # (5) must match
make dev-worker                                                   # (6) worker starts, migrations skipped in its logs
make dev-down && make dev                                         # (7) prior data still present after restart
make dev-destroy && make dev                                      # (8) fully clean DB + empty bucket after
pytest                                                             # (9, from backend/) passes with this stack up
make dev-down && pytest                                           # (10) passes identically with this stack down
```
All ten must succeed. Then work through §14's full 15-item table and §17's Definition of Done checklist explicitly before marking this blueprint complete.
