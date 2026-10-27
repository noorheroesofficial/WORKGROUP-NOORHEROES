# B-08 — Admin Consent Audit & Risk Review API

## 1. Feature Context
Two related, RBAC-separated admin surfaces: a read-only consent-history audit viewer for compliance staff, and a flagged-registration risk/fraud review queue for trust & safety staff. Both write immutable audit trails of admin activity.

## 2. Parent Feature
Feature A.1 — Splash, Language Selection, Authentication & Onboarding

## 3. Sub-feature
1.8 Admin Consent Audit & Risk Review API (ID: **B-08**)

## 4. Objective
Implement read-only consent-ledger search (`compliance_read` role + step-up MFA) and a flagged-attempt review queue with approve/block decisions (`trust_safety` role), both fully audit-logged via the existing `AdminAuditRepository`.

## 5. Business Requirements
- Consent Audit Viewer: search by masked parent identifier/family ID, view full immutable consent history for compliance/support — never shows raw plaintext identifiers, masked only.
- §12.5: Admin Consent Audit Viewer requires `compliance_read` role + step-up MFA re-auth if session older than 15 minutes.
- CRUD permissions: Consent Audit = Read-only, no Update/Delete role exists for any admin role, ever.
- Risk/Fraud Review Queue: flagged registration attempts (VOIP numbers, high-velocity device fingerprints) surfaced for manual review/allow/block; every decision audit-logged with the reviewing admin's ID.
- CRUD permissions: Risk Queue = Read + Update (decision field) only.

## 6. Existing Architecture
Extends `modules/admin/` (`AdminService`, `AdminAuditRepository.log_action()`, `AdminRouter`). Reads from B-05's `consent_record` (read-only, respecting its append-only nature — this endpoint never writes to `consent_record` itself) and B-02's risk-flag data (from B-02 Task 09).

## 7. Existing Code to Reuse
- `modules/admin/repository.py::AdminAuditRepository.log_action()`, `list_logs()`
- `modules/admin/service.py::AdminService.log_action()`
- `core/deps.py::get_current_admin`, `require_admin_scope`
- **Resolved architecture decision — step-up mechanism:** `FAST-API-INSTRUCTIONS.md` §2 documents `require_elevated_session(parent, redis)` as taking a `parent: ParentSessionContext` argument specifically — it is the parent-app step-up dependency (used for PIN/biometric re-verification on the mobile side), not an admin-side mechanism, and it cannot be reused as-is for `AdminSessionContext`. No admin-side step-up dependency exists today. Resolution: this sub-feature adds a new `require_elevated_admin_session(admin: AdminSessionContext, redis) -> AdminSessionContext` in `core/deps.py`, built by mirroring `require_elevated_session`'s existing Redis-marker-based structure (same TTL-marker pattern, same `AuthorizationError` raise on missing/expired marker) but keyed on `admin_id` instead of `parent_id`. This is a new, small, pattern-consistent addition — not a parallel invention.
- B-05's `ConsentRepository.get_latest_for_family()` / a new read method for full history (read-only consumer)

## 8. Files to Create
- `src/noorheroes/modules/admin/consent_audit_schemas.py` — `ConsentAuditSearchResponse`
- `src/noorheroes/modules/admin/consent_audit_service.py` — `ConsentAuditService(BaseService)` (read-only)
- `src/noorheroes/modules/admin/risk_review_models.py` — `RiskFlagOrm` (if not already created in B-02 Task 09)
- `src/noorheroes/modules/admin/risk_review_schemas.py` — `RiskQueueItemResponse`, `RiskDecisionRequest`
- `src/noorheroes/modules/admin/risk_review_service.py` — `RiskReviewService(BaseService)`
- `src/noorheroes/modules/admin/risk_review_repository.py` — `RiskFlagRepository`
- `tests/modules/admin/test_consent_audit_api.py`
- `tests/modules/admin/test_risk_review_api.py`
- `tests/core/test_require_elevated_admin_session.py` — dedicated boundary test for the new admin step-up dependency

## 9. Files to Modify
- `src/noorheroes/modules/admin/api.py` — add `GET /admin/v1/consent/audit`, `GET /admin/v1/risk/queue`, `POST /admin/v1/risk/{attempt_id}/decision`
- `src/noorheroes/core/deps.py` — add `require_elevated_admin_session(admin, redis)` (new — see §7); extend `require_admin_scope` to support `compliance_read` and `trust_safety` scope strings if not already present

## 10. Backend Requirements
- Consent Audit: `search(family_id | masked_identifier)` returns the full ordered `consent_record` history for a family — masked identifiers only, joining through `auth_identifier.identifier_value_masked`, never `identifier_value_hash` reversed or raw values.
- Consent Audit gate: apply the new `require_elevated_admin_session` dependency (see §7's resolved decision) — if the admin's Redis-tracked elevation marker is older than 15 minutes or absent, require re-auth before returning results.
- Risk Queue: list flagged attempts from `RiskFlagOrm` (created in B-02 Task 09) with score/signals; `POST .../decision` updates the flag's decision field only (Read + Update permission model — no delete), writes an `AdminAuditLog` row via `AdminService.log_action()` with admin_id, action, before/after diff.

## 11. API Contract

### `GET /admin/v1/consent/audit?family_id=&identifier=`
- Auth: `get_current_admin` + `compliance_read` + step-up MFA (<15min). Response 200: ordered list of consent_record entries (version, decision, region, timestamp), masked identifiers only.

### `GET /admin/v1/risk/queue`
- Auth: `get_current_admin` + `trust_safety`. Response 200: paginated flagged attempts `{attempt_id, risk_score, signals: {voip_flag, velocity_flag, device_fingerprint_reuse_count}, status}`.

### `POST /admin/v1/risk/{attempt_id}/decision`
- Auth: `get_current_admin` + `trust_safety`. Request: `{decision: "approve"|"block", reason?}`. Response 200: `{updated: true}`. Audit: writes `AdminAuditLog`.

## 12. Database Requirements
Read-only against `consent_record` (B-05) via `auth_identifier` join for masking. Read+Update against `risk_flag` (B-02 Task 09) — Update limited to the `decision`/`status`/`reviewed_by_admin_id` columns only, never the original signal data.

## 13. Validation
`family_id`/`identifier` search must require at least one parameter (no unfiltered full-table listing). `decision` must be one of `approve`/`block`.

## 14. Authentication
`get_current_admin`; Consent Audit additionally requires step-up MFA re-auth within a 15-minute freshness window.

## 15. Authorization
- Consent Audit: `compliance_read` scope only.
- Risk Queue: `trust_safety` scope only.
- Neither scope grants the other's access — verify strict separation in tests.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| Admin lacks `compliance_read` | `403` |
| Admin lacks `trust_safety` | `403` |
| Session older than 15 min on Consent Audit | `403`/step-up-required response prompting re-auth, not silently degraded data |
| Decision on an already-decided attempt | `409`, existing decision preserved, no silent overwrite |

## 17. Security
- Zero raw/plaintext identifiers ever returned by Consent Audit — masked only, enforced at the schema layer (field simply doesn't exist for raw values).
- Strict RBAC separation between `compliance_read` and `trust_safety` — a compliance-only admin cannot approve/block risk attempts, and vice versa.
- Every risk decision is immutably audit-logged with reviewer identity.

## 18. Testing
Unit: masking logic never leaks raw identifiers even under a malformed/edge-case search input. Integration: step-up-required-after-15-minutes enforcement; RBAC cross-scope rejection (compliance admin attempting risk decision → 403, and vice versa); decision audit-log row correctness (before/after diff, admin_id).

## 19. Documentation
Document the two distinct RBAC scopes and their strict non-overlap explicitly in the module README — this separation is a compliance requirement, not an implementation detail.

## 20. AI Coding Agent Implementation Steps

**Task 01 — Confirm/Extend Admin Step-Up MFA Mechanism**
Objective: Implement `require_elevated_admin_session(admin, redis)` in `core/deps.py`. Why: confirmed via `FAST-API-INSTRUCTIONS.md` that the existing `require_elevated_session(parent, redis)` is scoped to `ParentSessionContext` only — no admin-side equivalent exists, so this is a build task, not a discovery task. Follow: mirror the existing function's Redis-marker structure exactly (same TTL-marker read/write pattern, same `AuthorizationError` raise on missing/expired marker), substituting `admin_id` for `parent_id` as the Redis key component. Tests: session-age boundary test (14min59s passes, 15min01s requires re-auth); marker-absent-entirely case (never-elevated admin) also requires re-auth. Definition of Done: `require_elevated_admin_session` is unit-tested at the exact 15-minute boundary and is structurally consistent with (not a divergent reimplementation of) the existing parent-side function.

**Task 02 — Implement Consent Audit Search (Read-Only)**
Objective: `ConsentAuditService.search()` joining `consent_record`+`auth_identifier` for masked results. Follow: `BaseService`, strictly read-only repository calls into B-05's read methods. Security: no raw identifier ever touches the response schema. Tests: masking correctness, empty-search-param rejection. Dependencies: Task 01, B-05. Definition of Done: masking verified by a test that seeds a raw identifier and asserts it never appears in any response field.

**Task 03 — Implement Risk Queue List & Decision**
Objective: `RiskReviewService` list + decision-update methods, `RiskFlagRepository` with Update limited to decision fields. Follow: `BaseService`/`BaseRepository`, `AdminService.log_action()` for the audit trail. Business Rules: `trust_safety`-only, immutable audit log per decision, no delete capability. Tests: full decision-flow test with audit-log assertion. Dependencies: B-02 Task 09 (`RiskFlagOrm` must already exist). Definition of Done: decision correctly persisted and audit-logged with reviewer identity.

**Task 04 — Add Router Endpoints with Strict Scope Separation**
Objective: Wire all three endpoints with distinct `require_admin_scope` gates. Follow: existing `AdminRouter` conventions. Tests: cross-scope rejection test (Task 05). Definition of Done: all three endpoints live, each gated to exactly one scope.

**Task 05 — Add Unit & Integration Tests**
Objective: Full coverage per §18, especially the RBAC cross-scope rejection tests. Definition of Done: all green in CI.

**Task 06 — Update OpenAPI Documentation**
Objective: Regenerate, confirm non-breaking diff. Definition of Done: diff classifier passes.

**Task 07 — Final Code Review**
Objective: Confirm zero raw-identifier leakage paths, strict RBAC separation, and that Consent Audit performs no writes whatsoever to `consent_record`. Definition of Done: checklist in §21 checked.

## 21. Final Verification Checklist
- [x] Consent Audit is 100% read-only against `consent_record` — no write path exists
- [x] Raw/plaintext identifiers never appear in any Consent Audit response
- [x] Step-up MFA enforced at exactly the 15-minute freshness boundary
- [x] `compliance_read` and `trust_safety` scopes are strictly non-overlapping (tested both directions)
- [x] Every risk decision writes an immutable `AdminAuditLog` row with reviewer admin_id
- [x] Risk Queue Update path touches only decision-related columns, never original signal data
- [x] Unit + integration tests green

## 22. Definition of Done
Consent Audit and Risk Review are live, RBAC-separated, fully audit-logged, and leak zero raw PII — ready for N-03 (Consent Audit Viewer) and N-04 (Risk & Fraud Review Queue) to render.
