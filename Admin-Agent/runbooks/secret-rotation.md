# NoorHeroes Operational Runbook — Secret Rotation & Emergency Exposure Protocol

**Document ID:** `RUNBOOK-SEC-01`  
**Applies To:** All operational tiers (`dev-qa`, `staging`, `production`)  
**Source Blueprint:** `Development_Blueprints.Phase1_Infra_Config.Infra.02-secrets-management-env-example-gitleaks.md`  
**Classification:** Internal Confidential / Platform Security  

---

## 1. Overview & Architecture Constraints

NoorHeroes utilizes **GCP Secret Manager** as the central, managed secret storage for cloud environments.

### Architectural Invariants
1. **Read-Once-at-Boot (MVP Invariant)**: Secrets are fetched from GCP Secret Manager and injected into `process.env` / `os.environ` once during container startup.
2. **No Hot/Live Secret Reloading**: A new secret version does **not** dynamically hot-reload into running container replicas. A rolling restart or new Cloud Run deployment is **mandatory** for rotated secrets to take effect.
3. **Fail-Closed Boot Guard**: Missing or inaccessible secrets immediately abort container initialization, failing platform health checks and preventing traffic routing to unconfigured containers.
4. **Never Bake Secrets into Container Images**: Docker images contain zero secret values or embedded tokens at build time.

---

## 2. Standard Secret Rotation Cadence

Per `infra/secrets/manifest.yaml`, the platform enforces the following rotation schedule:

| Secret Identifier | Environment Variable | Target Tiers | Owner | Cadence | Blast Radius & Impact |
|---|---|---|---|---|---|
| `jwt-signing-key` | `JWT_SIGNING_KEY` | `devqa`, `staging`, `production` | backend-platform | **90 days** | Critical: Signs user/family JWT tokens. |
| `session-cookie-signing-secret` | `SESSION_COOKIE_SIGNING_SECRET` | `devqa`, `staging`, `production` | admin-platform | **90 days** | Critical: Signs admin `httpOnly` session cookies. |
| `nextauth-secret` | `NEXTAUTH_SECRET` | `devqa`, `staging`, `production` | admin-platform | **90 days** | Critical: Admin auth session validation. |
| `database-url` | `DATABASE_URL` | `devqa`, `staging`, `production` | backend-platform | **180 days** | High: Database connection and credentials. |
| `r2-secret-access-key` | `R2_SECRET_ACCESS_KEY` | `devqa`, `staging`, `production` | backend-platform | **180 days** | High: Media asset storage read/write access. |
| `sentry-auth-token` | `SENTRY_AUTH_TOKEN` | `devqa`, `staging`, `production` | platform-infra | **365 days** | Low: CI sourcemap artifact upload token. |
| `openai-api-key` | `OPENAI_API_KEY` | `staging`, `production` | ai-safety | **365 days** | Medium: AI provider API access. |
| `ses-secret-access-key` | `SES_SECRET_ACCESS_KEY` | `staging`, `production` | backend-platform | **365 days** | Medium: Transactional email delivery. |
| `google-oauth-client-secret` | `GOOGLE_OAUTH_CLIENT_SECRET` | `devqa`, `staging`, `production` | backend-platform | **365 days** | Medium: Google OAuth token exchange. |
| `fcm-service-account-key` | `FCM_SERVICE_ACCOUNT_KEY` | `devqa`, `staging`, `production` | backend-platform | **365 days** | Medium: Push notifications dispatch. |

---

## 3. Standard Step-by-Step Rotation Procedure

Follow this procedure for scheduled rotations or maintenance.

### Step 1: Generate or Obtain New Secret Material
Generate high-entropy cryptographic strings using standard tooling:
```bash
# Generate 256-bit (32-byte) hex string for JWT or Session Cookie signing:
openssl rand -hex 32
```

### Step 2: Add New Secret Version in GCP Secret Manager
```bash
# Syntax: gcloud secrets versions add <SECRET_NAME> --data-file=<FILE_PATH> --project=<PROJECT_ID>
# Example: Adding a new version for staging admin session secret
gcloud secrets versions add noorheroes-staging-session-cookie-signing-secret \
  --data-file=/path/to/new-secret.txt \
  --project=noorheroes-staging
```

Verify that the new version is in state `ENABLED`:
```bash
gcloud secrets versions list noorheroes-staging-session-cookie-signing-secret \
  --project=noorheroes-staging
```

### Step 3: Trigger Rolling Container Restart
Because secrets are evaluated at process boot, force a rolling redeployment of the relevant service:
```bash
# Cloud Run rolling update / restart
gcloud run services update noorheroes-admin-web \
  --region=us-central1 \
  --project=noorheroes-staging \
  --update-env-vars=RESTART_TRIGGER=$(date +%s)
```

### Step 4: Verify Deployment & Health Status
1. Check Cloud Run revision health status:
   ```bash
   gcloud run services describe noorheroes-admin-web \
     --region=us-central1 \
     --project=noorheroes-staging
   ```
2. Monitor Cloud Logging for boot errors or secret initialization failures.
3. Perform synthetic smoke tests against `/api/health` and verify administrative login.

### Step 5: Disable (Do Not Destroy) Previous Secret Version
Once all active instances have transitioned to the new revision:
```bash
# Disable previous version (e.g., version 1)
gcloud secrets versions disable 1 \
  --secret=noorheroes-staging-session-cookie-signing-secret \
  --project=noorheroes-staging
```
> [!WARNING]
> Keep the disabled version for at least 48 hours to permit fast rollback before permanently destroying it via `gcloud secrets versions destroy`.

---

## 4. Emergency Secret Exposure Protocol (P1 Incident)

If Gitleaks or TruffleHog in CI, or a security audit, confirms a credential leak:

1. **Immediate Escalation**: Open a P1 security incident ticket and notify the platform security on-call engineer.
2. **Generate Replacement**: Generate a fresh secret immediately.
3. **Deploy Version to GCP Secret Manager**: Follow Step 2 above to push the new version.
4. **Forced Immediate Restart**: Execute Step 3 across all affected services simultaneously.
5. **Immediate Invalidation**: For leaked JWT or Session secrets, revoke all active sessions in the database / Redis blocklist.
6. **Immediately Destroy Compromised Version**: Permanently destroy the leaked secret version in Secret Manager and revoke upstream provider credentials (e.g., AWS IAM access keys, AI API tokens).
7. **Audit Review**: Inspect GCP Cloud Audit Data Access logs for Secret Manager access patterns during the exposure window.
