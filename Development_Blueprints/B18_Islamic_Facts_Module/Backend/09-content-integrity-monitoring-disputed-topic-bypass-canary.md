# B-09 — Content Integrity Monitoring & Disputed-Topic Bypass Canary

## 1. Feature Context
Part of Feature B.18 (Islamic Facts Module). This sub-feature was missing from the initial breakdown: PRD §10 (DevOps Requirements) specifies two production monitoring/alerting guarantees that are distinct from B-01's unit-level approval-gate test and B-06's endpoint-level bypass-prevention test — a **periodic production integrity audit** and a **production-sampling canary** — neither of which is a one-time CI gate; both must run continuously against live data.

## 2. Parent Feature
B.18 — Islamic Facts Module

## 3. Sub-feature
1.9 Content Integrity Monitoring & Disputed-Topic Bypass Canary (ID: B-09)

## 4. Objective
Implement two scheduled monitoring jobs: (1) a periodic integrity audit that alerts if any published fact is ever detected without a corresponding valid, non-revoked `scholar_approval` row, and (2) a disputed-topic AI-assist bypass canary that periodically samples production AI-assist calls to confirm the hard-disable (B-06) has never been circumvented.

## 5. Business Requirements
- §10 DevOps Requirements: "Alert if any published fact is ever detected (via a periodic integrity audit) without a corresponding valid, non-revoked `scholar_approval` row — a P0 content-governance violation given the platform's zero-tolerance stance on unreviewed content reaching children."
- §10 DevOps Requirements: "Alert if the Disputed-Topic AI-assist hard-disable is ever bypassed in production sampling (a content-governance canary)."
- §15.2 Rollback Plan: rollback triggers include "any confirmed instance of an unapproved/revoked fact reaching a child (P0)" and "any confirmed AI-generated content on a disputed topic reaching a child-facing surface (P0)" — this sub-feature is the detection mechanism that would trigger those rollback conditions.
- §12.9 Security Checklist (Pre-Launch) items 1–2 (approval-gate and bypass verification) are one-time pre-launch tests (covered by B-01/B-06); this sub-feature is their **ongoing production equivalent**, not a duplicate.

## 6. Existing Architecture
Reuses the platform's existing scheduled-job/cron infrastructure (the same mechanism used by A.2/B-07's nightly `prune_fact_history` job, and any existing platform-wide alerting/monitoring pipeline — e.g., OpenTelemetry alerting per `FAST-API-INSTRUCTIONS.md`'s stated observability stack). No new job scheduler or alerting system is introduced.

## 7. Existing Code to Reuse
- Existing job-scheduler registration mechanism (confirm exact existing pattern — likely Celery, per `FAST-API-INSTRUCTIONS.md`'s stated stack — before inventing a new scheduling approach).
- Existing OpenTelemetry/alerting integration for P0-severity alerts (confirm the platform's existing alert-routing destination — e.g., PagerDuty/Slack — before assuming a new channel is needed).
- B-01's `FactVersionRepository`, `ScholarApprovalRepository` (for the integrity audit query).
- B-06's AI-assist endpoint and its disputed-topic check (for the canary's sampling target).

## 8. Files to Create
- `src/noorheroes/modules/content/jobs/fact_integrity_audit.py` — periodic job querying for published `fact_version` rows lacking a valid non-revoked `scholar_approval`.
- `src/noorheroes/modules/content/jobs/disputed_topic_bypass_canary.py` — periodic job sampling recent AI-assist call logs for any disputed-topic fact where the call was not rejected.
- `tests/modules/content/test_fact_integrity_audit_job.py`.
- `tests/modules/content/test_disputed_topic_bypass_canary_job.py`.

## 9. Files to Modify
- Existing job-scheduler registration file — register both new jobs with an appropriate cadence (recommend hourly for the integrity audit given P0 severity; daily for the bypass canary, sampling-based by nature).

## 10. Backend Requirements
- **Integrity audit job:** query for any `fact_version` with `status='published'` lacking a joined `scholar_approval` row where `approved=true AND revoked_at IS NULL` (the inverse of B-01's approval-gate join) — any result is a P0 finding, since it should be structurally impossible given B-01's enforcement; a non-empty result indicates the enforcement itself has a bug or was bypassed at the database level.
- **Bypass canary job:** sample a percentage of recent AI-assist endpoint call logs (or, if full logging isn't already in place, add lightweight structured logging to B-06's AI-assist gate for exactly this purpose — confirm existing logging coverage before assuming it needs to be added); cross-reference each sampled call's topic against the current disputed-topic flag; any call that proceeded (was not rejected) for a currently-flagged topic is a P0 finding.
- Both jobs emit alerts via the platform's existing alerting integration on any finding — P0 severity, routed to the same on-call destination as other P0 content-governance alerts.
- Both jobs are read-only with respect to content data — they detect and alert, they do not attempt automatic remediation (a detected violation requires human/scholar review, not an automated fix).

## 11. KMP Requirements
N/A — backend-only monitoring.

## 12. NextJS Requirements
N/A directly — alert output surfaces via the platform's existing alerting channel, not a new admin dashboard page (out of scope; if the platform later wants an admin-visible audit history, that would be a separate, explicitly-scoped addition, not assumed here).

## 13. API Contract
No new endpoints — these are background jobs, not API-triggered.

## 14. Database Requirements
Read-only queries against B-01's `fact_version`/`scholar_approval` tables (integrity audit) and B-06's AI-assist call log (bypass canary, confirm exact log storage — could be application logs, not necessarily a database table).

## 15. Validation
N/A — monitoring jobs, no user input.

## 16. Authentication / 17. Authorization
N/A — internal scheduled jobs, not user-facing endpoints; run with the platform's existing service-level job credentials, no elevated/new permissions required.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Job itself fails to run (infra issue) | Job-scheduler's existing failure alerting applies (a missed audit run is itself worth surfacing, distinct from a content-integrity finding) |
| Query finds a violation | P0 alert fired with the specific `fact_id`/`version_id` (integrity audit) or call log reference (canary) for immediate investigation |
| No violations found | No alert (silent success is the expected steady state) |

## 19-22. Offline First / Local Data / Localization / RTL
N/A — backend scheduled jobs.

## 23. Analytics
The findings themselves ARE the signal — no separate product-analytics event; alert payloads should be structured enough to be queryable/dashboardable if the platform's alerting tool supports that.

## 24. Performance
Integrity audit query indexed on the same `(fact_id, locale, age_band, status)` index B-01 already defines — low-cost periodic query, not expected to be a performance concern even hourly. Bypass canary is sampling-based by design, bounded cost regardless of total AI-assist call volume.

## 25. Security
This sub-feature exists specifically to catch security/content-governance failures that structural enforcement (B-01/B-06) was supposed to prevent — it is a defense-in-depth layer, not a substitute for B-01/B-06's primary enforcement. A finding here indicates a bug in that primary enforcement and should be treated as a P0 incident, not merely a data cleanup task.

## 26. Library Requirements
Existing platform job-scheduler (Celery, per `FAST-API-INSTRUCTIONS.md`) and alerting integration (OpenTelemetry-based) — no new libraries.

## 27. Testing
- Unit: integrity audit job correctly identifies a fixture published-but-unapproved fact version (constructed by directly manipulating test-database state to bypass B-01's normal enforcement, simulating what a real bug would produce).
- Unit: integrity audit job produces zero findings against a fixture catalog with correctly-enforced approval gates.
- Unit: bypass canary job correctly identifies a fixture AI-assist call log entry that proceeded despite a disputed-topic flag.
- Unit: bypass canary job produces zero findings against a fixture log with correctly-rejected calls.
- Integration: both jobs' alert payloads contain sufficient detail (fact_id/version_id or call reference) for immediate investigation.

## 28. Documentation
Document both jobs' cadence, alert destination, and on-call runbook expectations (what an on-call engineer should do upon receiving each alert type) in the platform's existing operational runbook location.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm Existing Job Scheduler & Alerting Integration**
Objective: Identify the platform's actual existing cron/job mechanism and alert-routing destination.
Why Required: Rule 30 — do not invent a new scheduling or alerting mechanism when one already exists.
Dependencies: None (research task).
Definition of Done: Confirmed scheduler and alerting integration points.

**Task 02 — Integrity Audit Job**
Objective: `fact_integrity_audit.py`.
Existing Architecture to Follow: Confirmed job-scheduler pattern (Task 01).
Files to Create: `jobs/fact_integrity_audit.py`.
Implementation Details: Inverse of B-01's approval-gate join, per §10.
Dependencies: Task 01, B-01 complete.
Expected Result: Job runs hourly, alerts on any finding.
Definition of Done: Passes Task 05 tests.

**Task 03 — Disputed-Topic Bypass Canary Job**
Objective: `disputed_topic_bypass_canary.py`.
Existing Architecture to Follow: Confirmed alerting integration (Task 01); B-06's AI-assist logging (confirm coverage, add if missing).
Files to Create: `jobs/disputed_topic_bypass_canary.py`.
Dependencies: Task 01, B-06 complete.
Expected Result: Job runs daily, samples AI-assist logs, alerts on any bypass finding.
Definition of Done: Passes Task 05 tests.

**Task 04 — Register Jobs with Scheduler**
Objective: Wire both jobs into the existing scheduler registration.
Files to Modify: existing job-scheduler registration file.
Dependencies: Tasks 02–03.
Definition of Done: Both jobs visible/confirmed in the scheduler's job list in a staging environment.

**Task 05 — Tests**
Objective: Coverage per §27.
Dependencies: Tasks 02–03.
Definition of Done: All green.

**Task 06 — Runbook Documentation**
Objective: Operational runbook entries for both alert types.
Dependencies: Task 05.
Definition of Done: Runbook documented and linked from the alert payload/on-call rotation docs.

## 30. Definition of Done
- Both jobs running on their configured cadence in staging/production.
- Both jobs correctly detect fixture violations and correctly produce zero findings against correctly-enforced state.
- P0 alerts route to the platform's existing on-call destination.
- Operational runbook documented for both alert types.
- This is explicitly a defense-in-depth layer — its existence does not reduce the priority of B-01's/B-06's primary structural enforcement.

## 31. Final Verification Checklist
- [ ] Integrity audit job correctly detects a fixture unapproved-published-fact violation
- [ ] Integrity audit job produces zero false positives against correctly-enforced state
- [ ] Bypass canary job correctly detects a fixture disputed-topic bypass
- [ ] Bypass canary job produces zero false positives against correctly-rejected calls
- [ ] Both jobs registered with the existing scheduler, running on appropriate cadence (hourly / daily)
- [ ] P0 alerts route to the platform's existing on-call/alerting destination
- [ ] Operational runbook documented
- [ ] No new job-scheduler or alerting system introduced — reuses existing platform infrastructure
