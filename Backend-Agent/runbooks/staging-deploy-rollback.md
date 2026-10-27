> [!NOTE]
> **@deprecated**: For deployment topologies, rollback strategies, and Kubernetes probe specifications, see [`NoorHeroes-Backend/MASTER-README.md`](../../NoorHeroes-Backend/MASTER-README.md#15-production-deployment-strategy--operations).

# NoorHeroes Runbook: Staging Deployment, Smoke Testing & Rollback Procedures

**Scope:** Staging Environment CI/CD Pipeline (Stages 9 & 10)  
**File ID:** `docs/runbooks/staging-deploy-rollback.md`  
**Related Blueprint:** `Development_Blueprints.Phase1_Infra_Config.CI_CD.08-ci-pipeline-deploy-staging-e2e-smoke.md`  
**Target Tier:** Staging (`noorheroes-staging`, GCP project `noorheroes-staging`)  

---

## 1. Overview & Architecture

Every merge to `main` triggers automated CI/CD stages culminating in a verified Staging deployment:
1. **Stage 9 (`deploy-staging`):**
   - Retrieves previous last-known-good image tags from `gs://noorheroes-tfstate/deploy-state/staging-last-good.json`.
   - Executes pre-deploy database migrations via the `noorheroes-migrate-staging` Cloud Run Job (`alembic upgrade head`) within the private VPC.
   - Generates Terraform execution plan with immutable image tags (`backend:<sha>`, `admin-web:<sha>`).
   - Runs `infra/terraform/ci/deploy-staging-guardrail.sh` to prevent accidental deletion/replacement of stateful resources (Cloud SQL, R2 Media Bucket).
   - Applies the Terraform plan to deploy new Cloud Run revisions.
   - Publishes outputs (`backend_service_url`, `admin_web_service_url`, `cdn_admin_fqdn`) and registers a GitHub Deployment.
2. **Stage 10 (`e2e-smoke-staging`):**
   - Runs probe smoke tests against the live deployment (`GET /healthz`, `GET /readyz`).
   - Incorporates single-retry cold-start tolerance (`tenacity`-wrapped fixture).
   - On full pass, writes `gs://noorheroes-tfstate/deploy-state/staging-last-good.json` and marks the GitHub Deployment as `success`.
   - Serves as the mandatory hard gate for production promotion in Stage 11 (`CI_CD.09` / [`production-deploy-rollback.md`](production-deploy-rollback.md)).
3. **Rollback (`rollback-on-smoke-failure`):**
   - Triggers automatically if Stage 10 fails after a successful Stage 9 deployment.
   - Re-applies Terraform using previous last-known-good image tags, preventing state drift.

---

## 2. Last-Known-Good Marker Contract

**GCS Storage URI:**  
`gs://noorheroes-tfstate/deploy-state/staging-last-good.json`

**Schema:**
```json
{
  "git_sha": "a1b2c3d4e5f6789012345678901234567890abcd",
  "backend_image": "us-central1-docker.pkg.dev/noorheroes-staging/noorheroes-containers/backend:a1b2c3d4e5f6789012345678901234567890abcd",
  "admin_web_image": "us-central1-docker.pkg.dev/noorheroes-staging/noorheroes-containers/admin-web:a1b2c3d4e5f6789012345678901234567890abcd",
  "deployed_at": "2026-08-24T14:03:11Z",
  "smoke_passed_at": "2026-08-24T14:06:52Z",
  "github_run_id": "10234567890"
}
```

> [!IMPORTANT]
> The marker is **only** written after all Stage 10 smoke tests pass. Production promotion (`CI_CD.09`) treats this marker as the sole source of truth for candidate promotion.

---

## 3. Automated Rollback Behavior

When Stage 10 smoke tests fail:
1. `rollback-on-smoke-failure` triggers automatically.
2. It executes `terraform apply` targeting `infra/terraform/environments/staging` with:
   ```bash
   terraform apply -auto-approve \
     -var="backend_image=${PREVIOUS_BACKEND_IMAGE}" \
     -var="admin_web_image=${PREVIOUS_ADMIN_IMAGE}"
   ```
3. Database migrations are **not** rolled back because all Alembic migrations are strictly additive-first (per project invariant).
4. GitHub Deployment status is marked as `failure` with an explanatory note.

---

## 4. Break-Glass Manual Rollback (Emergency Fallback)

If Terraform is unavailable (e.g. state lock held by a hung runner), follow this manual procedure:

### Step 4.1: Instant Traffic Shift via `gcloud`
Authenticate and switch Cloud Run traffic to the previous healthy revision:

```bash
# 1. Identify previous revision
gcloud run revisions list \
  --service=noorheroes-api-staging \
  --region=us-central1 \
  --project=noorheroes-staging

# 2. Shift 100% traffic to previous healthy revision
gcloud run services update-traffic noorheroes-api-staging \
  --to-revisions=<PREVIOUS_HEALTHY_REVISION>=100 \
  --region=us-central1 \
  --project=noorheroes-staging

gcloud run services update-traffic noorheroes-admin-staging \
  --to-revisions=<PREVIOUS_HEALTHY_ADMIN_REVISION>=100 \
  --region=us-central1 \
  --project=noorheroes-staging
```

### Step 4.2: Reconcile Terraform State (Mandatory)
A bare `gcloud` traffic update induces drift between Terraform state and live infrastructure. As soon as the blocker clears, reconcile state by re-running Terraform with the previous known-good image:

```bash
cd infra/terraform/environments/staging
terraform init
terraform apply -auto-approve \
  -var="backend_image=<PREVIOUS_BACKEND_IMAGE>" \
  -var="admin_web_image=<PREVIOUS_ADMIN_IMAGE>"
```

---

## 5. On-Call Troubleshooting Guide

### 5.1 Pre-Deploy Migration Job Fails (`noorheroes-migrate-staging`)
- **Symptom:** Workflow fails at `gcloud run jobs execute noorheroes-migrate-staging`.
- **Cause:** Syntax error in Alembic migration, unhandled lock conflict, or schema incompatibility.
- **Action:**
  1. Inspect Cloud Run Job execution logs in GCP Cloud Logging:
     ```bash
     gcloud logging read 'resource.type="cloud_run_job" AND resource.labels.job_name="noorheroes-migrate-staging"' --limit=50 --project=noorheroes-staging
     ```
  2. Note that `deploy-staging` aborted before `terraform apply`, so the old application revision continues serving unharmed.
  3. Fix the Alembic migration on a branch and merge a fix PR.

### 5.2 Plan Blocked by Guardrail Script
- **Symptom:** `deploy-staging-guardrail.sh` exits with code 1.
- **Cause:** Terraform plan indicates deletion or replacement of `module.database.google_sql_database_instance.staging` or `module.storage.cloudflare_r2_bucket.staging_media`.
- **Action:**
  1. Review plan details in workflow run summary.
  2. Verify why Terraform proposed replacing the protected resource (e.g., changes to immutable instance flags or tier naming).
  3. Adjust Terraform configuration to avoid destructive replacement.

### 5.3 Smoke Test Cold-Start Timeout
- **Symptom:** Smoke probe test fails on initial attempt.
- **Cause:** Scale-to-zero Cloud Run container startup latency.
- **Action:**
  - The suite already includes `tenacity`-based retry tolerance (1 retry with 5s backoff).
  - If cold starts consistently exceed 15s, verify database connection pooling initialization or adjust `backend_min_instances = 1` in `infra/terraform/environments/staging/terraform.tfvars`.

### 5.4 Manual Re-run of Staging Deployment
To manually trigger a deployment or re-verify staging:
```bash
gh workflow run deploy-staging.yml --ref main
```
Or via GitHub Actions UI: Actions → **Deploy Staging** → **Run workflow** (branch: `main`).

---

## 6. Local Testing & Promotion Gate Bypass

> [!IMPORTANT]
> **Local Gate Pass & Offline Development**:
> For local testing, sandbox environments, or verifying Stage 11/12 scripts without live GCP staging resources:
> 1. **Local Manifest**: Generate a `promotion-manifest-backend.json` file in the project root matching your current commit SHA:
>    ```json
>    {
>      "app": "backend",
>      "git_sha": "9ea0ed40a5face1dc8a9a683f84fb5d2f0b086e5",
>      "image_digest": "us-central1-docker.pkg.dev/noorheroes-prod/noorheroes-images/backend@sha256:9ea0ed40a5face1dc8a9a683f84fb5d2f0b086e5",
>      "backend_image": "us-central1-docker.pkg.dev/noorheroes-prod/noorheroes-images/backend:9ea0ed40a5face1dc8a9a683f84fb5d2f0b086e5",
>      "release_version": "backend-v1.1.0",
>      "staging_verified_at": "2026-08-28T20:56:00Z",
>      "staging_smoke_test_passed": true
>    }
>    ```
> 2. **Dry-Run Flag**: Pass `DRY_RUN=true` to automatically bypass GCS fetch and generate a mock in-memory manifest:
>    ```bash
>    DRY_RUN=true SENTRY_WATCH_ENABLED=false ./infra/ci/resolve-promotion-artifact.sh backend
>    ```

---

## 7. Staging Environment Setup & Upload Procedure

To complete a fresh or updated Staging environment setup and ensure the Stage 10 GCS marker (`staging-last-good.json`) is published:

### Step 1: Configure GitHub Repository Variables & Secrets
Navigate to **GitHub Repository Settings → Secrets and variables → Actions**:
1. **Variables (Repository)**:
   - `WIF_PROVIDER`: Full GCP Workload Identity Provider resource string (e.g., `projects/<PROJECT_NUM>/locations/global/workloadIdentityPools/github-pool/providers/github-provider`).
   - `PROD_WIF_PROVIDER`: Production WIF Provider resource string.
2. **IAM Permissions**:
   - Ensure the service account `terraform-ci-runner@noorheroes-staging.iam.gserviceaccount.com` has roles:
     - `roles/storage.objectAdmin` on bucket `gs://noorheroes-tfstate`
     - `roles/run.admin` in `noorheroes-staging`
     - `roles/iam.serviceAccountUser`

### Step 2: Initialize Infrastructure via Terraform
Before automated deployments can apply updates:
```bash
cd infra/terraform/environments/staging
terraform init
terraform plan -out=tfplan.binary
terraform apply tfplan.binary
```

### Step 3: Deploy Pre-Migration Cloud Run Job
Ensure the database migration runner job exists in Staging:
```bash
gcloud run jobs create noorheroes-migrate-staging \
  --project=noorheroes-staging \
  --region=us-central1 \
  --image=us-central1-docker.pkg.dev/noorheroes-staging/noorheroes-containers/backend:latest \
  --command=alembic \
  --args=upgrade,head \
  --set-env-vars="ENVIRONMENT=staging"
```

### Step 4: Trigger & Verify Automated Staging Pipeline (Stages 9 & 10)
Push your changes to `main` or dispatch manually:
```bash
gh workflow run deploy-staging.yml --ref main
```
1. **Stage 9 (`deploy-staging`)**: Executes `noorheroes-migrate-staging` and updates Cloud Run services (`noorheroes-api-staging`, `noorheroes-admin-staging`).
2. **Stage 10 (`e2e-smoke-staging`)**: Executes `pytest tests/smoke/` against the live staging URL.
3. **Marker Publication**: On 100% test success, the workflow writes `staging-last-good.json` to `gs://noorheroes-tfstate/deploy-state/staging-last-good.json`.

### Step 5: Verify GCS Marker
Confirm the marker is active and readable:
```bash
gcloud storage cat gs://noorheroes-tfstate/deploy-state/staging-last-good.json
```
Once verified, the Stage 11/12 production promotion gate is unlocked for that commit.

