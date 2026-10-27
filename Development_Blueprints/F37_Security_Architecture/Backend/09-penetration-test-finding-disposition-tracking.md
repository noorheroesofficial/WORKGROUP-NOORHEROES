# B-09 — Penetration-Test Finding Disposition Tracking

## 1. Feature Context
This sub-feature was identified as missing during a re-scan of the F.37 PRD against the original B-01–B-08/K-01/N-01 breakdown: the PRD explicitly requires every penetration-test finding to carry a documented disposition (§1.10 edge case 5), and explicitly names a `penetration_test_findings` reference table as N-01's data source (§9), but no blueprint previously implemented the table, the logging mechanism, or the disposition workflow itself — only N-01's read-only display of it was scoped. No school/institutional/madarsa logic applies.

## 2. Parent Feature
F.37 — Security Architecture (Cross-Cutting).

## 3. Sub-feature
B-09 — Penetration-Test Finding Disposition Tracking (Backend / FastAPI, `admin` context).

## 4. Objective
Implement the `penetration_test_findings` data model, a way to log findings (manually by Security Engineering, or via CI/CD pen-test-tool integration where available), and an explicit disposition workflow (fixed / risk-accepted / compensating-control) so that, per PRD FR-11/§1.10.5, every finding has a documented disposition and none goes unaddressed silently.

## 5. Business Requirements
- FR-11: "SAST, dependency scanning, container scanning, and regular penetration testing as part of CI/CD and a recurring security calendar."
- Edge Case §1.10.5: "A penetration test discovers a finding that, while technically valid, would require disproportionate effort relative to its actual risk to remediate immediately → findings are triaged by severity with defined remediation SLAs..., but every finding still requires a documented disposition (fixed, risk-accepted-with-sign-off, or compensating-control-applied) — never a finding that simply goes unaddressed without an explicit decision."
- §9 (Admin AI Code-Generation Prompt, verbatim): "recent penetration-test findings with their disposition status (fixed/risk-accepted/compensating-control), sourced from a `penetration_test_findings` reference table."
- §10 (DevOps Requirements): "Recurring (at minimum quarterly) penetration testing per the documented security calendar, with findings tracked to disposition."
- §11.3 (Dashboard Metrics): "penetration-test finding volume/severity/disposition trend."
- Security Checklist §12.9 implicitly requires this data to exist and be reviewable, consistent with the checklist's overall audit posture.
- Analytics §1.19: `penetration_test_finding_logged`, `penetration_test_finding_disposition_recorded` — these two events are explicitly named in the PRD's own event taxonomy but were not wired to any implementing blueprint prior to this one; this is itself confirming evidence the gap is real, not invented.

## 6. Existing Architecture
- `admin` bounded context (`FAST-API-INSTRUCTIONS.md` §5.2) — the natural home, consistent with B-08's incident/audit-adjacent data and N-01's admin-only consumption.
- `common/base_service.py`/`common/base_repository.py` pattern for the new repository/service.
- Coordinates with B-08 (shares the same "security posture" data domain and the same N-01 consumer) and DevOps's CI/CD scanning pipeline (SAST/dependency/container scanning per FR-11) as a possible future automated-ingestion source — this blueprint implements manual logging first; automated CI ingestion is explicitly flagged as a future enhancement, not assumed to exist yet (do not guess at a CI tool integration that hasn't been confirmed).

## 7. Existing Code to Reuse
- `admin` context's existing router/service/repository conventions.
- `core/deps.py`'s admin-authentication/RBAC-scope dependency factory (from B-01) for gating the write/disposition-update endpoints to `super_admin`/`security` roles.
- B-08's `RateLimitExceededError`-adjacent `core/exceptions.py` pattern for any new error types (e.g., an "already-dispositioned finding" conflict error).

## 8. Files to Create
- `src/noorheroes/admin/models/penetration_test_finding.py` — the ORM model.
- `migrations/xxxx_create_penetration_test_findings.py` — table migration.
- `src/noorheroes/admin/services/penetration_test_finding_service.py` — logging + disposition-workflow logic.
- `src/noorheroes/admin/api/penetration_test_findings.py` — router (log finding, update disposition, list findings).
- `tests/admin/test_penetration_test_findings.py`.

## 9. Files to Modify
- `admin` context router registration to include the new router.
- N-01's repository/hook (cross-reference only — N-01's pen-test-findings panel now has a real backend to call; update N-01's §13 API Contract from "flagged, not yet confirmed" to this blueprint's concrete contract, see §13 below and the corresponding N-01 edit).

## 10. Backend Requirements
- `PenetrationTestFinding` model: id, title, description, severity (`critical`/`high`/`medium`/`low`), discovered_at, discovered_by (free text or a reference to the pen-test vendor/tool), status (`open`/`dispositioned`), disposition (`fixed`/`risk_accepted`/`compensating_control`, nullable until set), disposition_notes (required once disposition is set — a disposition without a rationale is not acceptable per the PRD's "documented disposition" language), disposition_recorded_by (admin user id), disposition_recorded_at, remediated_at (nullable, set only when disposition == `fixed`).
- `POST /api/v1/admin/security/pentest-findings` — log a new finding (severity, title, description, discovered_at, discovered_by required).
- `PATCH /api/v1/admin/security/pentest-findings/{id}/disposition` — record a disposition; **reject if `disposition_notes` is empty** (structural enforcement of "every finding still requires a documented disposition," not merely a UI convention).
- `GET /api/v1/admin/security/pentest-findings` — paginated list, filterable by severity/status/disposition (this is N-01's data source).
- No finding may be deleted (append-only-in-spirit, consistent with the platform's audit-log philosophy in B-08) — a mis-logged finding is corrected via a documented amendment/note, not deletion, to preserve a complete historical record for any future compliance inquiry (§12.8 of the PRD).

## 11. KMP Requirements
N/A — admin/security-engineering-only surface, no mobile app relevance.

## 12. NextJS Requirements
N-01's pen-test-findings panel (already scoped in that blueprint) is this blueprint's direct consumer via the `GET` endpoint below; no additional NextJS work is introduced by this blueprint beyond what N-01 already specifies, but N-01's API Contract section should be updated to point at this concrete endpoint rather than remain flagged as pending (see the corresponding N-01 edit).

## 13. API Contract
**Auth model resolved against E.28's actual RBAC architecture** (see B-08 §13 for the full resolution): E.28's 9 admin roles are content editor, publisher, scholar reviewer, child-safety reviewer, support agent, billing ops, analyst, localization manager, and super admin — no literal "security" role exists, despite F.37's own shorthand phrasing implying one. Authorization here follows E.28 FR-5's actual model — role + resource_scope + action — using role `super_admin` with resource_scope `security_posture` for read access, and a stricter `security_posture:write`-equivalent resource_scope/action pair for the write endpoints below (logging a finding and recording a disposition are more consequential than reading the dashboard, so this blueprint deliberately splits read vs. write resource_scope grants rather than reusing one scope for both — confirm this split against E.28's actual permission-granularity conventions before finalizing, since E.28's documented examples group some read/write pairs under a single role tier like `admin+` rather than separate scopes).

`POST /api/v1/admin/security/pentest-findings`
- Auth: Bearer admin JWT (E.28's admin-auth namespace) + role `super_admin` + resource_scope `security_posture`, action `write`.
- Request: `{ "title": "string", "description": "string", "severity": "critical|high|medium|low", "discovered_at": "iso8601", "discovered_by": "string" }`.
- Response 201: the created finding, `status: "open"`, `disposition: null`.
- Validation: all fields required; `severity` must be one of the four enum values.

`PATCH /api/v1/admin/security/pentest-findings/{id}/disposition`
- Auth: same as above (`security_posture`, action `write`).
- Request: `{ "disposition": "fixed|risk_accepted|compensating_control", "disposition_notes": "string (required, non-empty)", "remediated_at": "iso8601|null" }`.
- Response 200: updated finding, `status: "dispositioned"`.
- Validation: `disposition_notes` required and non-empty (§10 hard rule); `remediated_at` only meaningful when `disposition == "fixed"`.
- Error Responses: 404 (finding not found), 422 (missing/empty `disposition_notes`), 409 (attempting to re-disposition an already-dispositioned finding without an explicit amendment flag — decide and document whether re-disposition is allowed at all, or only via a documented amendment path, rather than silently allowing silent overwrite of a prior disposition's audit trail).

`GET /api/v1/admin/security/pentest-findings`
- Auth: role `super_admin` + resource_scope `security_posture`, action `read` (shared read gate with B-08's two read endpoints for consistency — same resource_scope, different action-level grant than the write endpoints above).
- Query params: `page`, `page_size`, `severity` (optional filter), `status` (optional filter), `disposition` (optional filter).
- Response 200: `{ "items": [{ "finding_id": "uuid", "title": "string", "severity": "string", "discovered_at": "iso8601", "status": "string", "disposition": "string|null", "disposition_notes": "string|null" }], "total": int, "page": int, "page_size": int }`.

Per E.28 FR-6, both write endpoints must be service-layer-audited (a finding created or dispositioned is exactly the kind of sensitive mutation E.28's audit-everything principle targets) — write to E.28's shared `audit_log` table, not a local F.37-specific log, so this activity appears in the platform's single Audit Log Viewer (E.28 §1.18) rather than a second, disconnected trail.

## 14. Database Requirements
New `penetration_test_findings` table per §10's field list. Indexed on `(status, severity)` for the dashboard trend metric (§11.3) and on `discovered_at` for chronological listing. No PostgreSQL credential changes.

## 15. Validation
- `disposition_notes` is mandatory and non-empty whenever a disposition is recorded — this is the single most important validation rule in this blueprint, directly implementing the PRD's "never a finding that simply goes unaddressed without an explicit decision" requirement.
- `severity` and `disposition` are closed enums, not free text, to keep the dashboard's trend metrics (§11.3) meaningful.

## 16. Authentication
Standard admin JWT per B-01's canonical schema; no new authentication mechanism.

## 17. Authorization
Write endpoints (`POST`, `PATCH`) restricted to `super_admin` role + `security_posture` resource_scope, action `write`; list endpoint restricted to the same resource_scope, action `read` — both gated server-side, independent of any frontend RBAC check, per B-06's platform-wide principle, and per E.28's actual role+resource_scope+action model rather than an invented colon-scope string.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| `disposition_notes` missing/empty on a `PATCH` disposition call | 422, rejected — a finding cannot be silently marked dispositioned without a rationale |
| Attempt to disposition an already-dispositioned finding | 409, unless an explicit, documented amendment path is designed (decide and document, don't silently allow overwrite) |
| Finding not found | 404 |
| Unauthorized/forbidden role | 401/403 |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Admin-only internal tooling; `severity`/`disposition` enum values can remain technical/English internally, with N-01's presentation layer handling any display-level localization per its own §21.

## 22. RTL
N/A at the backend layer (NextJS's concern per N-01).

## 23. Analytics
Emit `penetration_test_finding_logged` on creation and `penetration_test_finding_disposition_recorded` on disposition — both explicitly named in PRD §1.19 and previously unwired to any implementation; this blueprint closes that gap.

## 24. Performance
Standard paginated-list performance considerations; finding volume is expected to be low (quarterly-cadence pen tests per §10), so no special optimization beyond standard indexing is anticipated.

## 25. Security
- The mandatory `disposition_notes` field is itself a security-process control, not merely a data-quality nicety — it is the mechanism that makes "every finding requires a documented disposition" actually enforceable rather than aspirational.
- Consider whether `penetration_test_findings` (like `audit_logs` in B-08) warrants its own append-only/tamper-evident enforcement at the database-role level, given its compliance relevance (§12.8) — flag this as a coordination point with B-08's audit-log pattern rather than assuming either way without confirming the desired rigor level with Security Engineering.

## 26. Library Requirements
No new library; standard FastAPI/SQLAlchemy/Pydantic stack already used across the `admin` context.

## 27. Testing
- **Unit:** finding creation validates required fields and severity enum.
- **Unit:** disposition update rejects empty/missing `disposition_notes`.
- **Integration:** full log → list → disposition-update flow.
- **RBAC test:** `security_posture` resource_scope with action `write` required for `POST`/`PATCH`; action `read` sufficient for `GET`; both independently rejected for a `super_admin` token lacking the `security_posture` resource_scope grant, and for any of E.28's other 8 roles by default.
- **Negative:** attempt to disposition an already-dispositioned finding without the designed amendment path → rejected per §18.

## 28. Documentation
Document the disposition workflow and its mandatory-notes rule in the `admin` context's API documentation; cross-reference from N-01's documentation now that a real data source exists.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define the `PenetrationTestFinding` Model & Migration**
- Task ID: B-09-T01
- Objective: Create the table and ORM model per §10/§14.
- Why This Is Required: Foundational data structure for everything else in this blueprint.
- Existing Architecture to Follow: `admin` context model conventions.
- Existing Files to Reuse: none.
- Files to Create: `src/noorheroes/admin/models/penetration_test_finding.py`, the migration file.
- Files to Modify: none yet.
- Implementation Details: per §10's field list, §14's indexing.
- Business Rules: `disposition_notes` nullable at the DB level (required only once a disposition is being recorded) but application-layer-enforced as non-empty at disposition time.
- Validation: DB-level enum constraints for `severity`/`disposition`/`status`.
- Error Handling: N/A at this task.
- Security: N/A beyond §25's flagged append-only consideration (decide and note, don't implement without confirming rigor level).
- Performance: indexes per §14.
- Localization / RTL / Analytics: N/A.
- Tests: migration/model tests.
- Documentation: docstrings.
- Dependencies: none.
- Do Not Change: N/A.
- Expected Result: table and model exist.
- Definition of Done: migration applies cleanly, model tests pass.

**Task 02 — Implement Finding Logging & Disposition Service/Endpoints**
- Task ID: B-09-T02
- Objective: Implement `POST`/`PATCH` endpoints per §13.
- Why This Is Required: Core write-path deliverable.
- Existing Architecture to Follow: `admin` context service/router pattern; `core/deps.py` RBAC dependency factory.
- Existing Files to Reuse: Task 01's model, `core/deps.py`.
- Files to Create: `penetration_test_finding_service.py`, the `POST`/`PATCH` router handlers.
- Files to Modify: `admin` router registration.
- Implementation Details: per §10/§13/§15; mandatory `disposition_notes` enforcement.
- Business Rules: no deletion, only documented amendment (decide and implement the amendment path, or explicitly restrict to single-disposition-only pending Security Engineering guidance).
- Validation: per §15.
- Error Handling: per §18.
- Security: `super_admin` role + `security_posture` resource_scope (action `write`) enforcement, per the resolved E.28 model in §13.
- Performance: N/A beyond standard.
- Localization / RTL: N/A.
- Analytics: `penetration_test_finding_logged`, `penetration_test_finding_disposition_recorded`.
- Tests: per §27 (unit, integration, negative).
- Documentation: API docs.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: findings can be logged and dispositioned with the mandatory-notes rule enforced.
- Definition of Done: §27's unit/integration/negative tests pass.

**Task 03 — Implement the Paginated List Endpoint (N-01's Data Source)**
- Task ID: B-09-T03
- Objective: Implement `GET /api/v1/admin/security/pentest-findings` per §13.
- Why This Is Required: This is the endpoint N-01's pen-test-findings panel actually calls — closes the previously-flagged N-01 gap.
- Existing Architecture to Follow: same pagination convention as B-08's Task 04 endpoints, for consistency.
- Existing Files to Reuse: Task 01's model, Task 02's service.
- Files to Create: the `GET` router handler.
- Files to Modify: none beyond router registration (Task 02 covers this file already).
- Implementation Details: per §13; filters on severity/status/disposition.
- Business Rules: read-only.
- Validation: pagination/filter param bounds-checking.
- Error Handling: 401/403 for unauthorized; 422 for invalid filter values.
- Security: `security_posture` resource_scope, action `read`, matching B-08's read endpoints' gating model.
- Performance: indexed query per §14.
- Localization / RTL: N/A.
- Analytics: N/A (read endpoint, no write event).
- Tests: RBAC test, pagination/filter tests.
- Documentation: API docs; cross-reference from N-01.
- Dependencies: Task 01, Task 02.
- Do Not Change: N/A.
- Expected Result: N-01's pen-test-findings panel has a real, working data source.
- Definition of Done: tests pass, contract matches §13 exactly (confirm against N-01's expected shape before considering this fully done).

## 30. Definition of Done
`penetration_test_findings` table and model created; log/disposition/list endpoints implemented with mandatory-notes enforcement on disposition; RBAC-gated server-side via `super_admin` role + `security_posture` resource_scope (read/write actions split); analytics events wired; N-01's previously-unconfirmed pen-test-findings data source now concrete and consumable.

## 31. Final Verification Checklist
- [ ] `penetration_test_findings` table created with the full field set per §10
- [ ] `POST` (log finding) validates required fields and severity enum
- [ ] `PATCH` (disposition) rejects empty/missing `disposition_notes` — the core enforcement mechanism
- [ ] No finding can be deleted; amendment path (if any) explicitly designed and documented, not left ambiguous
- [ ] `GET` list endpoint paginated, filterable, matches N-01's expected contract shape
- [ ] `super_admin` role + `security_posture` resource_scope (read/write actions split) enforced server-side on all three endpoints — never an invented "security" role
- [ ] Write endpoints' mutations are service-layer-audited into E.28's shared `audit_log` (per E.28 FR-6), not a separate F.37-local log
- [ ] `penetration_test_finding_logged` and `penetration_test_finding_disposition_recorded` events wired
- [ ] Append-only/tamper-evident rigor level for this table explicitly decided with Security Engineering (not silently assumed)
- [ ] No PostgreSQL/Redis credential changes introduced
