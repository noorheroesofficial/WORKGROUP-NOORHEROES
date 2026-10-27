> [!NOTE]
> **@deprecated**: For secrets bootstrapping, rotation schedules, and Google Cloud Secret Manager integration, see [`NoorHeroes-Backend/MASTER-README.md`](../../NoorHeroes-Backend/MASTER-README.md#5-environment-configuration-contract).

# Secrets Lifecycle, Rotation & Emergency Response Runbook

**Document ID:** `docs/runbooks/secret-rotation.md`  
**Applicable Tiers:** `dev-qa`, `staging`, `production`  
**Governing Blueprints:**
- `Development_Blueprints.Phase1_Infra_Config.Infra.02-secrets-management-env-example-gitleaks.md`
- `Development_Blueprints.Phase1_Infra_Config.Infra.01-environment-tiers-provisioning.md`
- `NoorHeroes_Consolidated_Blueprint_v6.md` §13.3 & §F.37 (Security Architecture)

---

## 1. Overview & Threat Model

NoorHeroes enforces centralized, versioned secrets management using **Google Cloud Secret Manager**.
Secrets are **never** baked into container images, committed to version control, or passed via plaintext environment files in non-local tiers.

### Fundamental Architectural Invariants:
1. **Zero Plaintext Secrets in SCM**: Enforced locally via `gitleaks` pre-commit hook and in CI via mandatory non-bypassable `gitleaks-scan` and `trufflehog-verified-scan` status checks.
2. **Read-Once-at-Boot**: The backend bootloader (`src/noorheroes/core/secrets_bootstrap.py`) reads `infra/secrets/manifest.yaml` and populates `os.environ` once during `lifespan()` startup.
3. **No Live In-Memory Hot Rotation at MVP**: Rotated secrets take effect on the **next container boot/restart**. A rolling restart is required after adding a new secret version.
4. **Least-Privilege IAM**: Each environment tier's Cloud Run runtime service account is granted `roles/secretmanager.secretAccessor` strictly scoped per-secret for its specific tier.

---

## 2. Managed Secrets Inventory & Rotation Cadence

The canonical registry of all managed secrets is maintained in [`infra/secrets/manifest.yaml`](../../NoorHeroes-Backend/infra/secrets/manifest.yaml).

| Secret ID | Target Environment Variable | Rotation Cadence | Owning Subsystem | Blast Radius & Description |
|---|---|---|---|---|
| `jwt-signing-key` | `JWT_SIGNING_KEY` | **90 days** | `backend-platform` | Critical: Signs parent & child JWT access/refresh tokens. |
| `jwt-admin-signing-key` | `JWT_ADMIN_SIGNING_KEY` | **90 days** | `backend-platform` | Critical: Signs Admin Portal session tokens. |
| `secret-key` | `SECRET_KEY` | **90 days** | `backend-platform` | High: Fallback application secret key. |
| `database-url` | `DATABASE_URL` | **180 days** | `backend-platform` | Critical: Full database connection string with credentials. |
| `postgres-password` | `POSTGRES_PASSWORD` | **180 days** | `backend-platform` | High: Postgres user password for migrations and maintenance. |
| `redis-password` | `REDIS_PASSWORD` | **180 days** | `backend-platform` | High: Redis authentication token for cache & Celery. |
| `r2-access-key-id` | `R2_ACCESS_KEY_ID` | **180 days** | `backend-platform` | High: Cloudflare R2 S3-compatible Access Key ID. |
| `r2-secret-access-key` | `R2_SECRET_ACCESS_KEY` | **180 days** | `backend-platform` | Critical: Cloudflare R2 Secret Key (access to media assets). |
| `openai-api-key` | `OPENAI_API_KEY` | **365 days** | `ai-safety` | Medium: OpenAI API key for LLM moderation & personalization. |
| `anthropic-api-key` | `ANTHROPIC_API_KEY` | **365 days** | `ai-safety` | Medium: Claude API key for secondary LLM operations. |
| `gemini-api-key` | `GEMINI_API_KEY` | **365 days** | `ai-safety` | Medium: Gemini API key for multilingual content. |
| `deepseek-api-key` | `DEEPSEEK_API_KEY` | **365 days** | `ai-safety` | Medium: DeepSeek API key for quiz engine. |
| `sentry-dsn` | `SENTRY_DSN` | **365 days** | `observability-infra` | Low: Sentry ingestion endpoint. |

---

## 3. Scheduled Secret Rotation Procedure

Scheduled rotations are performed during standard maintenance windows or off-peak hours.

### Step 1: Generate Cryptographically Secure Secret Value
```bash
# For 256-bit cryptographic keys (JWT signing keys, session secrets):
NEW_SECRET_VALUE=$(openssl rand -hex 32)
```

### Step 2: Upload New Secret Version to GCP Secret Manager
```bash
TIER="staging"  # or "production", "devqa"
SECRET_ID="jwt-signing-key"
GCP_PROJECT="noorheroes-${TIER}"

echo -n "${NEW_SECRET_VALUE}" | gcloud secrets versions add "noorheroes-${TIER}-${SECRET_ID}" \
  --project="${GCP_PROJECT}" \
  --data-file=-
```

### Step 3: Trigger a Rolling Restart of Cloud Run Service
Because secrets are loaded once at process boot, force a new revision to deploy the new secret version to active instances:
```bash
gcloud run services update "noorheroes-api-${TIER}" \
  --project="${GCP_PROJECT}" \
  --region="us-central1" \
  --update-env-vars="DEPLOY_TIMESTAMP=$(date +%s)"
```

### Step 4: Verify Deployment Health
```bash
# Check service status and readiness probe
curl -f -i "https://${TIER}.api.noorheroes.com/readyz"
```

### Step 5: Disable (Do Not Immediately Destroy) Old Secret Version
Keep previous version in `DISABLED` state for 24 hours to accommodate any in-flight requests or rolling rollbacks:
```bash
OLD_VERSION=1  # Replace with the previous version number

gcloud secrets versions disable "${OLD_VERSION}" \
  --secret="noorheroes-${TIER}-${SECRET_ID}" \
  --project="${GCP_PROJECT}"
```

---

## 4. Emergency Secret Compromise / Leaked Secret Response

If a secret is flagged by `trufflehog`, `gitleaks`, or manual discovery as exposed or compromised:

> [!CAUTION]
> **P1 Incident Procedure**: Immediate out-of-band rotation required within 60 minutes.

### Phase 1: Containment & Immediate Version Deployment (< 15 mins)
1. Generate and upload a fresh credential into GCP Secret Manager immediately following **Section 3, Steps 1–3**.
2. Force immediate traffic migration to the new Cloud Run revision.

### Phase 2: Invalidation of Compromised Credential (< 30 mins)
1. Revoke the compromised API key / token at the upstream vendor dashboard (e.g., OpenAI, Cloudflare R2, AWS/GCP IAM).
2. For database passwords:
   - Alter PostgreSQL user password on Cloud SQL.
   - Update `database-url` and `postgres-password` secrets.
   - Restart backend instances.

### Phase 3: Immediate Invalidation of Active User Sessions (for JWT keys)
If `jwt-signing-key` was compromised:
1. Rotating `jwt-signing-key` immediately invalidates all existing parent/child access tokens (which will fail signature verification with `InvalidTokenError`).
2. Blacklist all refresh tokens in Redis / database to force re-authentication.

### Phase 4: Forensic Audit (< 4 hours)
1. Inspect GCP Cloud Audit Logs (Data Access logs for Secret Manager API) to identify unauthorized reads.
2. Search application access logs for anomalies during the exposure window.

---

## 5. Verification Checklist

- [ ] New secret version exists in GCP Secret Manager and is in `ENABLED` state.
- [ ] Backend instances booted cleanly without `SecretsBootstrapError`.
- [ ] `/healthz` and `/readyz` endpoints return `200 OK`.
- [ ] User authentication flow (login, token refresh) functions as expected.
- [ ] Deprecated secret version is disabled after grace period.
