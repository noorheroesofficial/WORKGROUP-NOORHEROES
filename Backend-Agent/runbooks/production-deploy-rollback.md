> [!NOTE]
> **@deprecated**: For production promotion gates, zero-downtime rolling cutover, and post-deploy Sentry verification, see [`NoorHeroes-Backend/MASTER-README.md`](../../NoorHeroes-Backend/MASTER-README.md#15-production-deployment-strategy--operations).

# NoorHeroes Runbook: Production Promotion, Deployment & Automated Rollback Procedures

**Scope:** Production Environment CI/CD Pipeline (Stages 11, 12 & 13)  
**File ID:** `docs/runbooks/production-deploy-rollback.md`  
**Related Blueprint:** `Development_Blueprints.Phase1_Infra_Config.CI_CD.09-ci-pipeline-manual-promotion-production-deploy.md`  
**Target Tier:** Production (`noorheroes-prod` GCP project, `noorheroes-api-prod`, `noorheroes-admin-prod`)  
**Companion Manual:** `infra/ci/README.md`

---

## 1. Overview & Architecture

Production deployments enforce a human-gated, staging-verified promotion architecture across Stages 11 through 13:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PRODUCTION PROMOTION, ROLLING CUTOVER & SENTRY VERIFICATION DAG             │
│                                                                             │
│  Stage 11: Manual Promotion Gate (`promote-and-deploy-production-backend`)   │
│    ├── Declared via native GitHub `environment: production`                  │
│    ├── Enforces required review by `release-managers` team (Eng Lead+On-Call)│
│    ├── 24-hour approval timeout ceiling (`timeout-minutes: 1440`)            │
│    └── Dispatches Slack #deploys card (`gate-open` with release changelog)   │
│                                │                                             │
│                                ▼ (Human Approves in Actions UI)              │
│  Stage 12: Production Rolling Deploy & Traffic Cutover                       │
│    ├── 1. Artifact Resolution: `resolve-promotion-artifact.sh` (manifest)   │
│    ├── 2. WIF Auth (`prod-deploy-sa@noorheroes-prod.iam.gserviceaccount.com`)│
│    ├── 3. Pre-Cutover DB Migration: `run-production-migration.sh`            │
│    │      └── Cloud Run Job: `noorheroes-migrate-prod` (alembic upgrade head)│
│    ├── 4. Deploy Candidate Revision: `gcloud run deploy --no-traffic`        │
│    ├── 5. Pre-Cutover Health Probes: `verify-candidate-health.sh` (3 retries)│
│    │      └── Probes candidate revision /healthz and /readyz before cutover   │
│    ├── 6. 100% Traffic Cutover: `gcloud run services update-traffic`         │
│    ├── 7. Register Sentry Release: `sentry-release-mark-deployed.sh`         │
│    └── 8. Create GitHub Deployment Record (`state: success`)                 │
│                                │                                             │
│                                ▼                                             │
│  Stage 13: Post-Deploy Verification (`post-deploy-verify-production-backend`)│
│    ├── 1. Immediate Live Smoke Test: `smoke-test.sh https://api.noorheroes` │
│    ├── 2. 10-Minute Sentry Watchdog: `sentry_post_deploy_watch.py`           │
│    │      ├── Sample Rate: 60s intervals across 600s window                  │
│    │      ├── Absolute Event Floor: 50 unhandled events (noise protection)   │
│    │      └── Relative Multiplier: 3.0x pre-deploy baseline                  │
│    ├── 3. Clean Window: Emit `deploy-stable` Slack notification              │
│    └── 4. Anomaly Breach / 3x API Outage:                                    │
│           ├── Traffic-Only Rollback: `rollback-production.sh`                │
│           ├── P0 Incident Page: `page-oncall.sh` (Slack + PagerDuty)         │
│           ├── Dispatches `rollback` Slack notification card with reason      │
│           └── Updates GitHub Deployment Status to `failure`                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Reviewer List & Segregation of Duties (§9.1)

1. **Reviewer Team**: The `production` GitHub Environment must be configured with a named team: `release-managers` (composed of the Engineering Lead and the active On-Call Rotation Lead).
2. **Segregation of Duties**: An engineer who authored or merged a pull request cannot be the sole approver of that release in the production promotion gate.
3. **Approval Checklist**:
   - Verify that Stage 10 Staging Smoke Tests passed 100%.
   - Review the changelog diff link provided in the `#deploys` Slack notification.
   - Confirm no conflicting maintenance or major operational incidents are active.

---

## 3. 24-Hour Approval Timeout Ceiling (§10)

The manual gate job declares `timeout-minutes: 1440` (24 hours).
- If a promotion request is not reviewed within 24 hours, GitHub Actions automatically cancels the run.
- **Rationale**: An artifact approved after 24+ hours is potentially stale relative to active development on `main`.
- **Resolution**: Re-trigger the workflow to re-verify against the latest staging state.

---

## 4. Production Database Migration Strategy & Zero-Downgrade Invariant (§8.1)

### 4.1 Additive-First (Expand/Contract) Discipline
- **Pre-Cutover Execution**: `noorheroes-migrate-prod` Cloud Run Job executes `alembic upgrade head` **before** candidate traffic cutover while the old revision is still serving 100% of traffic.
- **Backward Compatibility**: Any new database column must be nullable or possess a safe server-side default so the existing revision can perform INSERT/UPDATE operations without violating constraints.
- **Contract Step**: Dropping or renaming columns must occur in a future PR after the release that ceases reading/writing that column has run in production.

### 4.2 Strict Zero-Downgrade Invariant
> [!CRITICAL]
> **Rollback NEVER executes `alembic downgrade`.**
> If Stage 12 pre-cutover health check fails or Stage 13 Sentry watchdog trips, the rollback engine (`rollback-production.sh`) shifts 100% traffic back to the previous Cloud Run revision. The previous revision is guaranteed to operate safely against the additive schema.
> Schema reversals must be fixed forward via a new commit and pull request.

---

## 5. Manual Break-Glass Rollback Procedure (§15)

In the event of an operational anomaly where the automated CI/CD watchdog must be supplemented or executed manually:

### Prerequisites
- Google Cloud SDK (`gcloud`) installed and authenticated.
- IAM permissions: `roles/run.admin` or impersonation rights for `prod-deploy-sa@noorheroes-prod.iam.gserviceaccount.com`.

### Execution Command
```bash
# Shift 100% traffic on backend Cloud Run service to the previous stable revision
./infra/ci/rollback-production.sh backend

# Shift 100% traffic on admin-web service to the previous stable revision
./infra/ci/rollback-production.sh admin

# Confirm recovery with live smoke probe
./infra/ci/smoke-test.sh https://api.noorheroes.com
```

`rollback-production.sh` is fully idempotent: running it multiple times is safe and will not corrupt traffic splits.

---

## 6. Sentry Post-Deploy Watchdog Parameters (§6.3)

$$\text{Rollback Triggered} = (\text{current\_errors} > \text{ABSOLUTE\_EVENT\_FLOOR}) \land (\text{current\_errors} > \text{baseline} \times \text{RELATIVE\_MULTIPLIER})$$

| Parameter | Default Value | Environment Variable Override | Purpose |
|---|---|---|---|
| **Watch Window** | `600s` (10 minutes) | `SENTRY_WATCH_WINDOW_SECONDS` | Total observation duration following cutover |
| **Poll Interval** | `60s` (1 minute) | `SENTRY_POLL_INTERVAL_SECONDS` | Frequency of Sentry API anomaly sampling |
| **Absolute Floor** | `50` events | `SENTRY_ABSOLUTE_EVENT_FLOOR` | Minimum unhandled events required before tripping |
| **Relative Multiplier** | `3.0x` baseline | `SENTRY_RELATIVE_MULTIPLIER` | Spike threshold relative to pre-deploy rate |
| **Fail-Safe Limit** | `3` attempts | `SENTRY_MAX_API_FAILURES` | Consecutive API errors before fail-safe rollback |
| **Degraded Mode Flag** | `true` (enabled) | `SENTRY_WATCH_ENABLED` | Set `false` during initial bootstrap if Sentry is unconfigured |

---

## 7. Testing & Verification Guide

```bash
# 1. Run all Sentry watchdog unit tests (13 tests)
./.venv/bin/pytest tests/core/test_sentry_post_deploy_watch.py -v

# 2. Run CI/CD architectural & pipeline invariant tests (18 tests)
./.venv/bin/pytest tests/architecture/test_production_deploy_pipeline.py tests/architecture/test_cicd_pipeline.py -v

# 3. Validate bash script syntax for all 10 operational scripts
bash -n infra/ci/*.sh

# 4. Dry-run execution test across all scripts
DRY_RUN=true SENTRY_WATCH_ENABLED=false ./infra/ci/resolve-promotion-artifact.sh backend
DRY_RUN=true ./infra/ci/run-production-migration.sh backend test-digest
DRY_RUN=true ./infra/ci/verify-candidate-health.sh https://candidate---test.run.app
DRY_RUN=true ./infra/ci/smoke-test.sh https://api.noorheroes.com
DRY_RUN=true ./infra/ci/rollback-production.sh backend
DRY_RUN=true ./infra/ci/page-oncall.sh backend test-reason
DRY_RUN=true ./infra/ci/notify-slack.sh gate-open backend v1.0.0
```

---

## 8. On-Call Triage & Root Cause Investigation

### 8.1 If Pre-Cutover Migration Job Fails (`noorheroes-migrate-prod`)
- **Symptom:** GitHub Actions Stage 12 fails at step `Run production Alembic migration`.
- **Impact:** Traffic was never shifted. Old revision continues serving traffic unharmed.
- **Triage Steps:**
  1. Inspect Cloud Run Job execution logs in GCP Cloud Logging:
     ```bash
     gcloud logging read 'resource.type="cloud_run_job" AND resource.labels.job_name="noorheroes-migrate-prod"' --limit=50 --project=noorheroes-prod
     ```
  2. Identify the Alembic migration revision ID and SQL error (e.g. lock timeout, missing prerequisite column).
  3. Fix the migration script in a new PR; do NOT attempt manual schema hacking in production Cloud SQL.

### 8.2 If Candidate Revision Probe Fails (`verify-candidate-health.sh`)
- **Symptom:** Candidate `/healthz` or `/readyz` fails 3 retries before traffic cutover.
- **Impact:** Traffic was never shifted. The failing revision remains untrafficked (`--tag candidate`).
- **Triage Steps:**
  1. Inspect Cloud Run candidate revision logs:
     ```bash
     gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="noorheroes-api-prod"' --limit=50 --project=noorheroes-prod
     ```
  2. Check for startup crashes, missing environment secrets, or failing database/Redis readiness probes.

### 8.3 If Sentry Watchdog Trips Rollback (`sentry_post_deploy_watch.py`)
- **Symptom:** Stage 13 watchdog detects $>50$ events and $>3.0\times$ baseline error rate. Automated rollback shifts 100% traffic to previous revision.
- **Impact:** Production service restored to previous stable revision.
- **Triage Steps:**
  1. Open the Sentry Issues dashboard for release `backend-vX.Y.Z`:
     ```
     https://sentry.io/organizations/noorheroes/issues/?query=release:backend-vX.Y.Z
     ```
  2. Filter by `is:unhandled` to identify the crashing exception stack trace.
  3. Verify that traffic split is 100% on the previous revision:
     ```bash
     gcloud run services describe noorheroes-api-prod --project=noorheroes-prod --region=us-central1 --format='value(status.traffic)'
     ```

### 8.4 Post-Rollback Fix-Forward Protocol
1. **Never Downgrade Schema:** Database schema remains in the migrated state.
2. **Reproduce Locally:** Replicate the unhandled exception using unit or integration tests (`pytest`).
3. **Fix and Re-promote:** Merge a bugfix PR through the standard 13-stage CI/CD pipeline.

---

## 9. Local Gate Bypass & Staging Prerequisite Reference

> [!IMPORTANT]
> **Local Gate Pass / Offline Verification**:
> If executing or debugging Stage 11/12 scripts without access to live GCS staging markers:
> 1. Generate a local `promotion-manifest-backend.json` in the root directory matching your current commit SHA (`$(git rev-parse HEAD)`).
> 2. Or pass `DRY_RUN=true`:
>    ```bash
>    DRY_RUN=true SENTRY_WATCH_ENABLED=false ./infra/ci/resolve-promotion-artifact.sh backend
>    ```
> For full instructions on configuring the staging environment to publish live markers, see [staging-deploy-rollback.md#7-staging-environment-setup--upload-procedure](staging-deploy-rollback.md#7-staging-environment-setup--upload-procedure).


