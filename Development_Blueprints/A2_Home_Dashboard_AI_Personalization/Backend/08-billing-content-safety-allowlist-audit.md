# B-08 — Billing-Content Safety Allowlist & Compliance Audit

## 1. Feature Context
NoorHeroes Child App, Feature A.2. This is the cross-cutting, P0, zero-tolerance guarantee of the entire Home feature: no billing, subscription, paywall, or upsell content can ever reach a child session (FR-9). This sub-feature formalizes and continuously verifies the allowlist pattern introduced in B-01.

## 2. Parent Feature
A.2 — Child Home Dashboard & AI Personalization

## 3. Sub-feature
1.8 Billing-Content Safety Allowlist & Compliance Audit (ID: B-08)

## 4. Objective
Finalize the response-shaping allowlist as a mandatory, non-bypassable CI gate; implement production-sampling continuous audit; wire audit results into a queryable log for N-05 (Billing-Content Safety Audit Log Viewer); establish the emergency-bypass approval process restricted to the `trust_safety` role.

## 5. Business Requirements
Per PRD §5 item 10, §10 (DevOps), §12, §15.2:
- Automated content-safety-audit test suite issues `GET /v1/home` across a fixture matrix (age, subscription tier, locale) and asserts zero blocklist-term matches; runs on every PR touching the Home Aggregation Service, Recommendation Service, or shared response-shaping models — CI-blocking, non-skippable, no engineer override.
- Only a designated Trust & Safety lead can approve an emergency bypass, logged.
- Production sampling-based safety audit job runs periodically post-deploy; automatic rollback if it ever fails.
- Any single confirmed instance of billing content reaching a real child session triggers an immediate full rollback + incident review (zero tolerance).

## 6. Existing Architecture
Builds directly on B-01 Task 06 (content-safety audit test harness) and B-01's response-shaping Pydantic allowlist (B-01 Task 01). Follow existing CI/CD pipeline conventions (GitHub Actions/GitLab CI/whichever the platform uses — confirm from existing `.ci` config before adding a new pipeline mechanism).

## 7. Existing Code to Reuse
- `tests/integration/test_home_content_safety_audit.py` (established in B-01 Task 06) — extended here, not duplicated.
- Existing CI pipeline configuration files.
- Existing audit-log storage pattern if one exists elsewhere in the platform (e.g., A.1's Consent Ledger append-only pattern) — reuse the append-only-log architectural style for consistency.

## 8. Files to Create
- `app/models/safety_audit_run.py`
- `alembic/versions/xxxx_create_safety_audit_run_table.py`
- `app/jobs/production_safety_sampling_audit.py`
- `app/services/safety_audit_service.py`
- CI pipeline config addition (e.g., `.github/workflows/home-safety-audit.yml` or platform-equivalent) marking the suite as required/non-skippable
- `tests/integration/test_home_content_safety_audit_full_matrix.py` (extends B-01's harness with the complete fixture matrix: free/premium/trial-expired × EN/HI/AR/UR)

## 9. Files to Modify
- `tests/integration/test_home_content_safety_audit.py` (from B-01) — extend blocklist coverage and fixture matrix rather than duplicate the file
- CI branch-protection configuration (require this check to pass before merge)

## 10. Backend Requirements
- Blocklist term set: `["subscribe","upgrade","$","price","billing","trial","renew"]` minimum, case-insensitive, recursive JSON string scan — extend with localized equivalents for AR/HI/UR if translated billing terminology exists in the platform's terminology glossary (coordinate with Localization team; do not invent unverified translations).
- `safety_audit_run` table logs every CI and production-sampling run: `run_id, timestamp, commit_sha, run_type (ci|production_sample), pass, failing_terms jsonb, sample_size`.
- Production sampling job periodically calls `GET /v1/home` against a sampled set of real (or synthetic staging-mirrored) sessions and runs the same blocklist scan, writing results to `safety_audit_run`.
- Emergency bypass: a documented, logged process (not a code flag) requiring `trust_safety` role sign-off — implement as an audit-logged manual override recorded in `safety_audit_run` with an `override_by`/`override_reason` field, never a silent skip.

## 11. KMP Requirements
Mirrors client-side in K-01 (Compose UI semantics-tree blocklist scan) — this backend sub-feature and K-01's client-side test are complementary defense-in-depth layers, not substitutes for each other.

## 12. NextJS Requirements
N-05 (Billing-Content Safety Audit Log Viewer) reads from `safety_audit_run` — this sub-feature owns the table/write path; N-05 owns the read-only UI.

## 13. API Contract
No new public client-facing endpoint. Internal/admin-only read access to `safety_audit_run` is exposed via an admin API for N-05:
- `GET /admin/v1/home/safety-audit-runs` — Auth: Admin Bearer, `trust_safety` role required — Response: paginated audit run history.

## 14. Database Requirements
`safety_audit_run(run_id PK, timestamp, commit_sha, run_type, pass boolean, failing_terms jsonb, sample_size, override_by nullable, override_reason nullable)`; index on `(timestamp DESC)`, `(pass)`.

## 15. Validation
Blocklist scan must recursively traverse the full JSON response (nested objects/arrays), not just top-level string fields — a term buried in a nested `reason_tag` or content title must still be caught.

## 16. Authentication
Admin endpoint requires Bearer (admin session) per existing Admin Portal auth.

## 17. Authorization
`GET /admin/v1/home/safety-audit-runs` restricted to `trust_safety` RBAC role, consistent with PRD §12.5.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| CI safety-audit suite fails | Build fails red, PR blocked, no override available to engineers |
| Production-sampling audit fails | Automatic rollback triggered; incident review opened |
| Emergency bypass requested | Requires logged `trust_safety` sign-off; recorded in `safety_audit_run`, never silent |

## 19. Offline First
Not applicable.

## 20. Local Data
Not applicable (backend); see K-01 for the client-side mirrored test.

## 21. Localization
Blocklist should ideally cover localized billing terminology (AR/HI/UR) if verified translations are available; flag as a follow-up item if not currently available rather than guessing translations.

## 22. RTL
N/A (backend).

## 23. Analytics
Audit run outcomes feed N-01's section-health context indirectly (billing-leak is the most severe "degraded" signal possible) — coordinate metric naming with N-01 if a shared dashboard view is desired, though N-05 is the primary consumer.

## 24. Performance
Production-sampling job must not materially increase load on the Home Aggregation Service — use a small, statistically reasonable sample rate (confirm exact rate with Trust & Safety/DevOps rather than guessing a number arbitrarily; default to a conservative low sample rate at launch, e.g., low single-digit percentage of traffic, adjustable via config).

## 25. Security
This entire sub-feature IS a security control. The non-bypassable CI gate and the logged emergency-override process are the key security properties — do not implement any silent/unlogged way to skip the audit.

## 26. Library Requirements
Existing CI/CD tooling, pytest, SQLAlchemy/Alembic, existing job scheduler for the production-sampling job.

## 27. Testing
- Integration: full fixture matrix (tier × locale) confirmed zero blocklist matches.
- Integration: intentionally inject a billing term into a mocked upstream response, confirm the audit suite catches it (a test that verifies the test itself is effective — a "canary" test).
- Integration: CI pipeline configuration confirmed to block merge on failure (verified via a deliberately-failing branch in a controlled test, or pipeline-config review).
- Unit: recursive nested-JSON blocklist scan correctness.

## 28. Documentation
Document the emergency-bypass process explicitly (who can approve, how it's logged, that it is never silent) in both code comments and the platform's operational runbook/documentation set.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create `safety_audit_run` Table + Migration**
- Objective: Persistent audit-run log.
- Why Required: Foundation for both CI-run logging and production-sampling logging, and the data source for N-05.
- Existing Architecture to Follow: Alembic/SQLAlchemy conventions; append-only-log style from A.1's Consent Ledger.
- Existing Files to Reuse: Base model class.
- Files to Create: `app/models/safety_audit_run.py`, `alembic/versions/xxxx_create_safety_audit_run_table.py`
- Files to Modify: none
- Implementation Details: Fields per §14.
- Business Rules: Append-only; overrides recorded, never silent deletion of a failing run record.
- Validation: N/A.
- Error Handling: N/A.
- Security: Append-only design prevents tampering with historical audit evidence.
- Performance: Indexed for N-05's paginated queries.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Migration test.
- Documentation: Docstring.
- Dependencies: None.
- Do Not Change: Do not modify PostgreSQL credentials.
- Expected Result: Table created.
- Definition of Done: Migration passes.

**Task 02 — Extend Content-Safety Audit Suite to Full Fixture Matrix**
- Objective: Complete the blocklist-scan test suite across all tiers/locales.
- Why Required: PRD §5 item 10 requires the full matrix, not a partial one.
- Existing Architecture to Follow: Extends B-01 Task 06's harness.
- Existing Files to Reuse: `tests/integration/test_home_content_safety_audit.py` from B-01.
- Files to Create: `tests/integration/test_home_content_safety_audit_full_matrix.py`
- Files to Modify: `tests/integration/test_home_content_safety_audit.py` (parametrize fully rather than fork a duplicate suite)
- Implementation Details: Parametrize over `{free, premium, trial_expired} x {en, hi, ar, ur}` fixture child profiles; recursive JSON stringify + blocklist regex scan (case-insensitive).
- Business Rules: Zero tolerance — any match fails the test.
- Validation: N/A.
- Error Handling: N/A.
- Security: This is the control itself.
- Performance: N/A (test-time only).
- Localization: Matrix explicitly covers all four supported locales.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task is the test suite; additionally write a canary test that injects a known billing term into a mocked upstream and confirms the suite catches it.
- Documentation: Comment block on zero-tolerance policy and canary-test rationale.
- Dependencies: B-01 (Task 06), B-02 through B-07 (so the full response has real content to scan).
- Do Not Change: Do not narrow the blocklist without logged Trust & Safety sign-off.
- Expected Result: Full-matrix suite passing.
- Definition of Done: Suite green; canary test proves suite catches injected violations.

**Task 03 — Wire CI Pipeline as Non-Skippable Gate**
- Objective: Make the audit suite a mandatory, non-bypassable CI check.
- Why Required: PRD §10 explicit DevOps requirement — no override flag for engineers.
- Existing Architecture to Follow: Existing CI/CD pipeline config format on this platform.
- Existing Files to Reuse: Existing workflow/pipeline files.
- Files to Create: CI workflow file (path depends on platform's existing CI tool)
- Files to Modify: Branch-protection settings (require this check) — document the required manual repo-settings change if it cannot be done via config-as-code
- Implementation Details: Trigger on any PR touching Home Aggregation Service, Recommendation Service, or shared response-shaping models (path-based trigger filters); mark check as required in branch protection.
- Business Rules: No skip label/flag available to engineers.
- Validation: N/A.
- Error Handling: Failing check blocks merge.
- Security: This is the enforcement mechanism.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Verify via a deliberately-failing test branch that the pipeline correctly blocks merge.
- Documentation: Runbook entry for the emergency-bypass process (Task 04).
- Dependencies: Task 02.
- Do Not Change: N/A.
- Expected Result: CI gate live.
- Definition of Done: Verified blocking behavior on a controlled failing branch.

**Task 04 — Implement Production-Sampling Audit Job + Emergency Bypass Logging**
- Objective: Continuous post-deploy verification and a logged (never silent) override path.
- Why Required: PRD §10, §15.2 — production sampling with auto-rollback, and a Trust & Safety-only bypass.
- Existing Architecture to Follow: Existing job-scheduler pattern; existing deployment-rollback mechanism (confirm how rollback is currently triggered on this platform — feature flag flip vs. deployment rollback — reuse that exact mechanism).
- Existing Files to Reuse: Existing job scheduler, existing rollback tooling.
- Files to Create: `app/jobs/production_safety_sampling_audit.py`, `app/services/safety_audit_service.py`
- Files to Modify: Deployment/rollback trigger integration point
- Implementation Details: Job samples a small percentage of live/staging-mirrored `GET /v1/home` traffic, runs the blocklist scan, writes `safety_audit_run` rows; on failure, triggers the existing rollback mechanism automatically and pages Trust & Safety.
- Business Rules: Emergency bypass requires `override_by` (trust_safety role) and `override_reason`, both mandatory, both logged in `safety_audit_run` — never a silent skip.
- Validation: Sample rate configurable, defaulting conservatively.
- Error Handling: Job failure itself (not audit failure) must not silently disable future runs — alert on job-execution failure separately from audit-content failure.
- Security: This is the continuous-verification control (§12.9 pre-launch checklist item).
- Performance: Conservative sample rate to avoid meaningfully increasing load.
- Localization: N/A.
- RTL: N/A.
- Analytics: Job results feed N-05.
- Tests: Integration test simulating a sampling run that finds a violation, asserting rollback trigger fires; unit test for the override-logging path (both fields mandatory, rejected if either is missing).
- Documentation: Full runbook entry describing rollback trigger conditions and the bypass approval flow.
- Dependencies: Task 01; existing rollback tooling.
- Do Not Change: Do not allow a bypass without both `override_by` and `override_reason` populated.
- Expected Result: Production-sampling job live with auto-rollback and logged-bypass support.
- Definition of Done: Simulated-violation integration test confirms rollback trigger; bypass-logging test confirms no silent overrides possible.

## 30. Definition of Done
CI gate is mandatory and non-bypassable except via a fully logged Trust & Safety override; production sampling runs continuously with auto-rollback on failure; full fixture-matrix audit suite passes; all audit history is queryable for N-05.

## 31. Final Verification Checklist
- [x] Full fixture-matrix content-safety audit suite passes (tier × locale)
- [x] Canary test proves the suite actually catches injected violations
- [x] CI check is required/non-skippable in branch protection
- [x] Production-sampling job runs on schedule and writes to `safety_audit_run`
- [x] Simulated production violation triggers automatic rollback
- [x] Emergency bypass requires both `override_by` and `override_reason`, always logged
- [x] `GET /admin/v1/home/safety-audit-runs` restricted to `trust_safety` role
- [x] All tests pass

## 32. Implementation Summary

- **Status**: Completed & Verified
- **Implementation Date**: 2026-09-25
- **Alembic Migration**: `alembic/versions/0086_create_safety_audit_run_table.py` creating append-only `safety_audit_run` table with btree indexes on `(timestamp DESC)` and `(pass)`.
- **Core Domain Module**: `src/noorheroes/modules/home/`
  - `models.py`: `SafetyAuditRunOrm` append-only entity with JSON failure term storage and override tracking.
  - `schemas.py`: Pydantic V2 schemas (`SafetyAuditRunResponse`, `SafetyAuditRunListResponse`, `SafetyAuditEmergencyBypassRequest`, `AuditViolationRecord`, etc.).
  - `safety_audit.py`: Recursive nested JSON scanner (`find_billing_violations_structured`) with case-insensitive token pattern scanning across keys, values, and lists.
  - `services/safety_audit_service.py`: `SafetyAuditService` handling run recording, paginated historical querying, emergency bypass validation (`override_by` + `override_reason`), and automated emergency rollback alerting.
  - `tasks.py`: Celery task `home.production_safety_sampling_audit` scheduled hourly in `core/celery_app.py`.
  - `admin_router.py`: Direct `/admin/v1/home/safety-audit-runs` and canonical `/v1/admin/home/safety-audit-runs` query and override endpoints.
- **Backwards Compatibility Facades**:
  - `app/models/safety_audit_run.py`
  - `app/services/safety_audit_service.py`
  - `app/jobs/production_safety_sampling_audit.py`
  - `docs/runbooks/billing-content-safety-emergency-bypass.md`
- **CI/CD Pipeline Gate**:
  - `.github/workflows/home-safety-audit.yml`: Mandatory blocking status check running full matrix safety suite.
- **Test Suites (52 Tests Passed - Zero Missing Scenarios)**:
  - `tests/unit/test_safety_audit_migration.py` (2 unit tests: 0086 migration upgrade & downgrade DDL)
  - `tests/unit/test_safety_audit_service.py` (11 unit tests: run recording pass/fail, query filtering by type/pass/date, pagination, emergency bypass validation & error paths, rollback alerting)
  - `tests/integration/test_home_content_safety_audit.py` (18 integration tests: core allowlist scan, token extraction, canary injection)
  - `tests/integration/test_home_content_safety_audit_full_matrix.py` (14 integration tests: 12-cell matrix {free, premium, trial_expired} x {en, ar, ur, hi}, canary injection test, scanner unit cases)
  - `tests/integration/test_safety_audit_admin_api.py` (5 integration tests: admin query flow, RBAC trust_safety enforcement, append-only DELETE 405 rejection, emergency bypass override, immutable audit logging)
  - `tests/integration/test_production_sampling_audit_job.py` (2 integration tests: clean production sampling run, simulated violation triggering auto-rollback & alert)

