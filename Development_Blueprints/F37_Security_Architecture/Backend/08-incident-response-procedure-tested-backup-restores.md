# B-08 — Incident Response Procedure & Tested Backup Restores

## 1. Feature Context
NoorHeroes must never discover, mid-emergency, that its backups don't actually restore or that its incident-response plan is untested. This blueprint implements the scheduled backup-restore verification job, database-role-level append-only audit logging, and the documented, parent-notification-inclusive incident-response runbook. No school/institutional/madarsa logic applies.

## 2. Parent Feature
F.37 — Security Architecture (Cross-Cutting).

## 3. Sub-feature
B-08 — Incident Response Procedure & Tested Backup Restores (Backend / FastAPI + DevOps).

## 4. Objective
Implement a scheduled backup-restore verification job, a documented incident-response runbook with parent-notification steps, and database-role-level append-only enforcement for audit logs, per PRD FR-14 and the §5/§10 requirements.

## 5. Business Requirements
- FR-14: "Immutable or tamper-evident audit logs (append-only at the database-role level, not just the application level); tested backup restores — a backup that has never been restored is not a verified backup; a documented incident-response procedure with parent-notification steps for any data-breach scenario."
- NFR §1.8: "Tested, Not Theoretical, Backup Restores: A backup is only considered verified once an actual restore has been successfully performed against it."
- Success Metric §1.4: "Backup-restore verification success rate: 100% (a backup that has never been restored is not considered verified)."
- Edge Case §1.10.6: an incident initially assessed as low-severity must still fully invoke the procedure to confirm that assessment, never shortcut it.
- Edge Case §1.10.7: a backup found non-restorable during a test is itself a critical incident requiring immediate remediation and root-cause investigation, never simply noted for later.
- Success Metric §1.4: "Incident-response procedure tabletop-exercise frequency: At least annually, with documented findings actioned."

## 6. Existing Architecture
- `audit_logs` table already exists (E.28's table, per PRD §4.3), referenced here as needing database-role-level append-only enforcement, not application-level-only.
- DevOps/infra backup tooling (PostgreSQL automated backups, per PRD §10: "PostgreSQL automated backups with tested restore drills") — this blueprint's job is the *verification job* and its scheduling, not standing up backups from scratch (assume automated backup creation already exists; confirm before assuming).
- `FAST-API-INSTRUCTIONS.md` §5.6 references Celery Tasks (`localization` context) as an existing scheduled-task mechanism — reuse the same scheduling infrastructure for the backup-restore verification job rather than introducing a new one.

## 7. Existing Code to Reuse
- Existing Celery task infrastructure/scheduler (confirm the exact existing pattern under `localization`'s Celery Tasks or wherever the project's scheduled-job convention lives) for the periodic restore-verification job.
- Existing PostgreSQL backup mechanism (DevOps-owned, likely outside the `src/noorheroes/` application code — coordinate rather than reimplement).
- `core/exceptions.py` pattern for any new incident-related exception/alert types.

## 8. Files to Create
- `src/noorheroes/scripts/verify_backup_restore.py` (per `FAST-API-INSTRUCTIONS.md` §6 "Administrative Scripts" convention — `src/noorheroes/scripts/`) — the scheduled restore-verification job.
- `docs/security/incident-response-runbook.md` — the documented procedure, including parent-notification steps.
- `docs/security/tabletop-exercise-log.md` — tracking template for annual tabletop exercises and their findings.
- `migrations/xxxx_audit_logs_append_only_role_constraint.py` (or equivalent Alembic migration naming convention already used in the project) — the database-role-level enforcement.
- `tests/scripts/test_backup_restore_verification.py`.
- `tests/db/test_audit_log_append_only_enforcement.py`.

## 9. Files to Modify
- Database role/permission configuration for whatever role the application connects as — REVOKE `UPDATE`/`DELETE` on `audit_logs` for that role (and any other role capable of writing to it), leaving only `INSERT` and `SELECT`. Do not modify PostgreSQL connection credentials themselves — only the granted privileges on this specific table for the existing role(s).
- CI/DevOps scheduling configuration to register the new backup-restore verification job on a recurring cadence.

## 10. Backend Requirements
- `verify_backup_restore()`: triggers a restore of the most recent backup into an isolated verification environment (not production), runs a defined set of sanity checks (schema present, row counts within expected bounds, a known-good sample query succeeds), records the result (pass/fail, timestamp, details) to a `backup_restore_tests` reference table (create if not already present — confirm against N-01's assumption that this table exists, since N-01's Security Posture Dashboard reads from it).
- On verification failure: treat as a critical incident per §1.10.7 — do not merely log and continue; trigger the alerting path (§10 DevOps: "Alert on a backup-restore test failing") and open a root-cause investigation ticket/record.
- `audit_logs` append-only enforcement: a database migration that revokes `UPDATE`/`DELETE` grants on `audit_logs` from the application's DB role, so that even a fully compromised application code path cannot alter or delete an existing audit entry — this must be enforced at the PostgreSQL role/privilege level, not merely by omitting UPDATE/DELETE methods from the application's repository class (§1's "strongest possible enforcement" framing).
- Incident-response runbook: a living document (not application code) covering: incident classification/severity, immediate containment steps, investigation steps, the explicit parent-notification decision tree and messaging template, regulatory/compliance notification considerations (flagged as a Legal/Compliance coordination point, not something this blueprint's author should draft alone), and post-incident review requirements.

## 11. KMP Requirements
N/A — this blueprint is entirely backend/DevOps/process; no client code changes.

## 12. NextJS Requirements
N/A directly for this blueprint, but its output tables (`backup_restore_tests`, tabletop-exercise history, incident log) are consumed read-only by N-01's Security Posture Dashboard — confirm the exact schema of these tables against N-01's blueprint expectations so the two remain in sync.

## 13. API Contract
**Defined (previously flagged as N-01's concern — resolved here since this blueprint owns the underlying data).**

**Auth model resolved against E.28's actual RBAC architecture (previously a proposed `security:read` scope-string guess — corrected).** E.28's PRD (`Feature_E28_Admin_Auth_RBAC_Operations_Dashboard.md` §1.1) enumerates its actual 9 admin roles explicitly: content editor, publisher, scholar reviewer, child-safety reviewer, support agent, billing ops, analyst, localization manager, and **super admin** — there is no role literally named "security" anywhere in E.28's role taxonomy, despite F.37 §8/§9's own shorthand phrasing ("Restricted to `super_admin`/`security` roles"). E.28's actual authorization model (FR-5) is multi-dimensional — **role + resource_scope + region + locale + action**, via the `role_permission` table (`permission_key`, `resource_scope`, `region`, ...), not a flat role-name-or-scope-string check. Resolution: gate these endpoints on **role = `super_admin`** (confirmed to exist) **AND resource_scope = `security_posture`** — `super_admin` has this resource_scope by default; any other admin needing access is granted the same `security_posture` resource_scope through E.28's existing maker-checker role-permission workflow, never by inventing a new "security" role. **Flag for stakeholder awareness:** F.37's own PRD text should probably be corrected to stop implying a standalone "security" role exists — this is a documentation inconsistency between F.37 and E.28, not something this blueprint set can silently paper over.

`GET /api/v1/admin/security-posture/backup-restore-history`
- Auth: Bearer admin JWT (E.28's separate admin-auth namespace, never the parent/child token namespace) + role `super_admin` + resource_scope `security_posture` (per the resolution above), checked via `core/deps.py`'s RBAC-scope-verification-dependency factory (B-01).
- Query params: `page` (int, default 1), `page_size` (int, default 20, max 100).
- Response 200: `{ "items": [{ "test_id": "uuid", "run_at": "iso8601", "success": true, "duration_seconds": 42, "details": "string|null" }], "total": int, "page": int, "page_size": int }`.
- Error Responses: 401 (no/invalid token), 403 (authenticated but lacking the `security_posture` resource_scope), 422 (invalid pagination params).

`GET /api/v1/admin/security-posture/incident-tabletop-history`
- Auth: same as above.
- Query params: `page`, `page_size` (same defaults).
- Response 200: `{ "items": [{ "exercise_id": "uuid", "conducted_at": "iso8601", "findings_actioned": true, "summary": "string" }], "total": int, "page": int, "page_size": int }`.
- Error Responses: same pattern as above.

Both endpoints are read-only (admin-portal-consumed, N-01's dependency); no request body; both draw from tables this blueprint creates/owns (`backup_restore_tests`, and a new `incident_tabletop_exercises` table — see §14). Per E.28 FR-6, any access to these endpoints (a "sensitive read") should itself be service-layer-audited, consistent with E.28's own audit-everything principle for admin-portal reads of this nature — confirm with E.28's owners whether all reads or only mutation-adjacent reads require this, rather than assuming either way.

## 14. Database Requirements
- New (or confirmed-existing) `backup_restore_tests` table: id, run timestamp, pass/fail, details/error, duration.
- New `incident_tabletop_exercises` table (not previously specified — added to back the §13 read endpoint and the §1.4 "at least annually, with documented findings actioned" success metric): id, conducted_at, findings_actioned (bool), summary, facilitator, participants (or a simple text list, format TBD with Trust & Safety), created_at.
- `audit_logs` — no schema change, but a role-privilege migration removing `UPDATE`/`DELETE` grants from the application role.
- Do not modify PostgreSQL connection credentials; only table-level privilege grants for the existing application role.

## 15. Validation
- Restore-verification job's sanity checks must be specific and meaningful (not merely "the restore command exited 0") — schema presence, referential-integrity spot-check, row-count sanity bounds, and a known-good query against a stable reference table.

## 16. Authentication
N/A — this is an internal scheduled job and a documentation deliverable, not a user-facing feature.

## 17. Authorization
The database-role-privilege change is itself an authorization control (removing the application's own ability to mutate/delete audit history) — this is the one place in this blueprint where "authorization" is the literal subject matter.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Restore verification fails (backup not actually restorable) | Critical incident: alert immediately, block marking the backup as verified, open root-cause investigation (§1.10.7, never "noted and left for a future cycle") |
| Restore verification job itself crashes/times out (infra issue, not a backup-quality issue) | Distinguish this from an actual failed restore in logging/alerting — both need attention, but conflating them would misdiagnose root cause |
| Attempt to `UPDATE`/`DELETE` `audit_logs` as the application role | Rejected at the PostgreSQL privilege level (permission denied), not merely blocked in application code |
| Incident initially scoped as "non-sensitive" | Procedure still fully invoked to confirm this before concluding parent notification isn't warranted (§1.10.6) |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
The incident-response runbook's parent-notification messaging template should be prepared for translation into the platform's supported languages (English, Hindi, Arabic, Urdu) ahead of an actual incident — draft the template with localization in mind (clear, simple sentence structure) even if this blueprint doesn't produce the translated versions itself; flag translation as a Legal/Compliance + Localization team follow-up.

## 22. RTL
N/A for this blueprint's own deliverables (no UI); relevant only to however the eventual parent-notification message is rendered in-app/email, which is out of this blueprint's scope.

## 23. Analytics
Emit `backup_restore_test_completed` (with `success: bool`), `incident_response_procedure_invoked`, `incident_parent_notification_sent`, per PRD §1.19.

## 24. Performance
The restore-verification job must run against an isolated environment, never production, to avoid any production performance/availability impact; schedule during a low-traffic window if the restore process is resource-intensive.

## 25. Security
- Audit-log append-only enforcement at the database-role level is explicitly called out (§1) as the strongest possible enforcement specifically because it holds even under a fully compromised application layer — do not settle for application-level-only enforcement (e.g., simply "not exposing an update method") as a substitute.
- The incident-response runbook itself should be stored somewhere accessible during an actual incident (not solely dependent on systems that might be part of the incident) — flag this operational consideration to DevOps/Security Engineering rather than assuming a default location is adequate.

## 26. Library Requirements
No new library required beyond whatever the project's existing Celery/task-scheduling stack already provides, and the project's existing Alembic (or equivalent) migration tooling for the role-privilege change.

## 27. Testing
- **Unit:** restore-verification job's sanity-check logic (mocked restore target).
- **Integration:** the migration correctly revokes `UPDATE`/`DELETE` on `audit_logs` for the application role — test by attempting both operations as that role and confirming rejection, while confirming `INSERT`/`SELECT` still succeed.
- **Scheduled-job test:** confirm the job is actually registered and fires on the intended cadence (not just that the function works when called manually).
- **Failure-path test:** simulate a failed restore and confirm the critical-incident alerting path triggers (per §1.10.7), not merely a logged warning.

## 28. Documentation
`docs/security/incident-response-runbook.md` and `docs/security/tabletop-exercise-log.md` are themselves the primary documentation deliverables of this blueprint; additionally document the `audit_logs` role-privilege change and its rationale directly in the migration file's comments so a future engineer doesn't "fix" a permission-denied error by re-granting UPDATE/DELETE without understanding why it was revoked.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement the Backup-Restore Verification Job**
- Task ID: B-08-T01
- Objective: Build `verify_backup_restore()` and its scheduled execution.
- Why This Is Required: Core deliverable; "a backup that has never been restored is not a verified backup" (§1.4).
- Existing Architecture to Follow: existing Celery task-scheduling pattern.
- Existing Files to Reuse: existing backup-creation tooling (confirm existence/location first, coordinate rather than duplicate).
- Files to Create: `src/noorheroes/scripts/verify_backup_restore.py`, `backup_restore_tests` table migration if not already present.
- Files to Modify: scheduling configuration.
- Implementation Details: per §10; isolated verification environment, specific sanity checks per §15.
- Business Rules: failure is a critical incident (§1.10.7), not a routine log entry.
- Validation: as in §15.
- Error Handling: as in §18.
- Security: verification environment must not expose production data beyond what's already access-controlled equivalently.
- Performance: scheduled off-peak per §24.
- Localization / RTL: N/A.
- Analytics: `backup_restore_test_completed`.
- Tests: per §27.
- Documentation: note the job's schedule and sanity-check criteria.
- Dependencies: confirmed existing backup-creation mechanism.
- Do Not Change: the backup-creation mechanism itself (out of scope, DevOps-owned).
- Expected Result: recurring, real (not theoretical) restore verification.
- Definition of Done: job runs on schedule, tests pass, alerting confirmed on simulated failure.

**Task 02 — Enforce Database-Role-Level Append-Only Audit Logs**
- Task ID: B-08-T02
- Objective: Migrate `audit_logs` privileges so the application role cannot `UPDATE`/`DELETE`.
- Why This Is Required: FR-14's "strongest possible enforcement" requirement — application-level-only enforcement is explicitly called out as insufficient.
- Existing Architecture to Follow: existing migration tooling and `audit_logs` table (E.28-owned, do not alter its schema, only its role privileges).
- Existing Files to Reuse: `audit_logs` table definition (read, not modify schema).
- Files to Create: the role-privilege migration file.
- Files to Modify: none in application code (this is a database-level change only).
- Implementation Details: `REVOKE UPDATE, DELETE ON audit_logs FROM <app_role>;` (exact role name confirmed from existing DB config, not guessed).
- Business Rules: append-only, no exceptions, no admin-code-path override that re-grants privileges dynamically.
- Validation: N/A.
- Error Handling: N/A (this task creates the enforcement, doesn't handle runtime errors from it beyond what Task 03's test covers).
- Security: this is the primary security deliverable of this task.
- Performance: no impact (privilege grants don't affect query performance).
- Localization / RTL / Analytics: N/A.
- Tests: per §27's integration test.
- Documentation: migration file comments explaining rationale (§28).
- Dependencies: none beyond the existing `audit_logs` table.
- Do Not Change: `audit_logs` schema, PostgreSQL connection credentials.
- Expected Result: `UPDATE`/`DELETE` on `audit_logs` structurally impossible for the application role.
- Definition of Done: integration test confirms rejection of UPDATE/DELETE, confirms INSERT/SELECT still function.

**Task 03 — Author the Incident-Response Runbook & Tabletop Tracking**
- Task ID: B-08-T03
- Objective: Produce `docs/security/incident-response-runbook.md` and `docs/security/tabletop-exercise-log.md`.
- Why This Is Required: FR-14's documented, parent-notification-inclusive procedure and the annual-tabletop-exercise success metric (§1.4) both require this concrete artifact, not merely an implicit understanding.
- Existing Architecture to Follow: N/A (new process documentation) — coordinate structure with Legal/Compliance and Trust & Safety stakeholders per PRD §1.5.
- Existing Files to Reuse: none.
- Files to Create: `docs/security/incident-response-runbook.md`, `docs/security/tabletop-exercise-log.md`.
- Files to Modify: none.
- Implementation Details: severity classification, containment steps, investigation steps, parent-notification decision tree + message template (draft, Legal/Compliance to finalize wording), regulatory-notification checklist (flagged for Legal/Compliance ownership), post-incident review template.
- Business Rules: edge case §1.10.6 — the procedure must be *fully invoked* even for an apparently-low-severity incident before concluding parent notification isn't warranted; state this explicitly in the runbook so it isn't shortcut under time pressure.
- Validation: N/A.
- Error Handling: N/A.
- Security: store the runbook somewhere accessible during an actual incident (§25) — flag as an operational/DevOps coordination point.
- Performance: N/A.
- Localization: draft parent-notification template with future translation in mind (§21).
- RTL: N/A.
- Analytics: reference `incident_response_procedure_invoked`/`incident_parent_notification_sent` as the events that should fire when this runbook is actually executed (wiring those events into whatever incident-tracking tool is used is a coordination point, not necessarily new application code — confirm with DevOps).
- Tests: N/A (documentation deliverable); the tabletop exercise itself is the "test" of this document, tracked in the log.
- Documentation: this task's deliverable is documentation itself.
- Dependencies: none technically, but requires Security Engineering/Trust & Safety/Legal sign-off per PRD §15.3.
- Do Not Change: N/A.
- Expected Result: a real, usable runbook ready before it's ever needed, plus a tracking mechanism for the required annual tabletop cadence.
- Definition of Done: runbook reviewed and signed off by the stakeholders named in PRD §1.5; first tabletop exercise scheduled.

**Task 04 — Implement the Admin-Read Endpoints for N-01's Security Posture Dashboard**
- Task ID: B-08-T04
- Objective: Implement `GET /api/v1/admin/security-posture/backup-restore-history` and `GET /api/v1/admin/security-posture/incident-tabletop-history` per §13.
- Why This Is Required: N-01 (NextJS Admin) has no data source for its backup-restore-history and tabletop-history panels without these; previously flagged as pending, now defined and owed by this blueprint since it owns the underlying tables.
- Existing Architecture to Follow: `admin` bounded context's existing router pattern; auth per the resolved role+resource_scope model in §13 above (`super_admin` role + `security_posture` resource_scope, not a colon-scope string).
- Existing Files to Reuse: `backup_restore_tests` table/repository (Task 01), new `incident_tabletop_exercises` table (this task).
- Files to Create: `incident_tabletop_exercises` table migration; `admin` context router additions for both endpoints; their repository/service methods (paginated list queries).
- Files to Modify: `admin` context router registration.
- Implementation Details: per §13's exact request/response contract; both endpoints paginated, read-only, RBAC-gated.
- Business Rules: read-only, no mutation.
- Validation: pagination params bounds-checked (§13's 422 case).
- Error Handling: per §13's error table.
- Security: gated by `super_admin` role + `security_posture` resource_scope, independently enforced server-side (never trust a frontend-only gate, consistent with B-06's principle).
- Performance: paginated queries, indexed on `run_at`/`conducted_at` for sort order.
- Localization / RTL: N/A (backend contract only; NextJS owns presentation localization).
- Analytics: N/A beyond existing `backup_restore_test_completed` write-side event.
- Tests: endpoint integration tests (pagination, RBAC rejection for a token lacking the `security_posture` resource_scope, empty-list case).
- Documentation: OpenAPI/internal API docs for both new endpoints.
- Dependencies: Task 01 (backup_restore_tests), Task 03 (tabletop process/table).
- Do Not Change: N/A.
- Expected Result: N-01's two backend-dependent panels have a real, working, RBAC-gated data source.
- Definition of Done: integration tests pass, including the RBAC-rejection case.

## 30. Definition of Done
Backup-restore verification job scheduled and running with real (non-theoretical) restores; `audit_logs` append-only enforced at the database-role level; incident-response runbook authored, reviewed, and stored accessibly; tabletop-exercise tracking mechanism in place with the first exercise scheduled; N-01's backup-restore-history and incident-tabletop-history read endpoints implemented and RBAC-gated.

## 31. Final Verification Checklist
- [ ] Backup-restore verification job performs an actual restore, not a simulated/theoretical check
- [ ] Verification failure triggers immediate critical-incident alerting and root-cause investigation, never a silent log
- [ ] `audit_logs` `UPDATE`/`DELETE` structurally rejected at the PostgreSQL role-privilege level
- [ ] `INSERT`/`SELECT` on `audit_logs` confirmed still functional after the privilege change
- [ ] Incident-response runbook includes explicit parent-notification steps and decision tree
- [ ] Runbook explicitly requires full procedure invocation even for apparently-low-severity incidents
- [ ] Tabletop-exercise tracking mechanism in place, annual cadence scheduled
- [ ] `backup_restore_test_completed`, `incident_response_procedure_invoked`, `incident_parent_notification_sent` events wired
- [ ] `GET .../backup-restore-history` and `GET .../incident-tabletop-history` implemented, paginated, RBAC-gated server-side
- [ ] No PostgreSQL/Redis credential changes introduced (only `audit_logs` table-level privilege grants)
