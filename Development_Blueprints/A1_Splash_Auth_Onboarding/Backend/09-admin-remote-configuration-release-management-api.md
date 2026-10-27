# B-09 — Admin Remote Configuration & Release Management API

## 1. Feature Context
Write-side counterpart to B-01: lets admins update `min_supported_version`, `recommended_version`, `maintenance_mode`, and — given its legal weight — publish a new `consent_version` only through a two-admin approval workflow.

## 2. Parent Feature
Feature A.1 — Splash, Language Selection, Authentication & Onboarding

## 3. Sub-feature
1.9 Admin Remote Configuration & Release Management API (ID: **B-09**)

## 4. Objective
Implement Create/Update-only (no delete) remote-config management, with a propose→pending→approve/reject workflow specifically for `consent_version`, requiring a different admin to approve than the one who proposed.

## 5. Business Requirements
- Remote Config Management: admin can update `min_supported_version`, `recommended_version`, `maintenance_mode`, and `consent_version` pointers; publishing a new consent version requires a second-approver workflow given its legal weight.
- CRUD permissions: Remote Config = Create/Update only (no delete — versioned, not destructive).
- Every admin action (config change, risk decision) writes an immutable `audit_log` row with admin_id, action, before/after diff, and timestamp.
- Release plan dependency: feature flag `onboarding_v1_enabled` controls the entire A.1 flow server-side — this panel is also the natural home for that flag if no broader feature-flag admin surface exists yet (flag as a scope question rather than silently expanding beyond the PRD's explicit field list).

## 6. Existing Architecture
Extends `modules/admin/` and directly writes to B-01's `remote_config` table via a **new** write-capable repository method (kept separate from B-01's read-only `RemoteConfigRepository`, per the read/write RBAC-code-review separation already established for the Consent Audit pattern in B-08).

## 7. Existing Code to Reuse
- `modules/admin/service.py::AdminService.log_action()`
- B-01's `RemoteConfigOrm` model (write against it here; do not redefine)
- `core/deps.py::get_current_admin`, `require_admin_scope("admin:write")`

## 8. Files to Create
- `src/noorheroes/modules/admin/remote_config_write_schemas.py` — `RemoteConfigUpdateRequest`, `ConsentVersionProposalRequest`, `ConsentVersionApprovalRequest`
- `src/noorheroes/modules/admin/remote_config_write_repository.py` — `RemoteConfigWriteRepository` (Update-only, plus proposal CRUD)
- `src/noorheroes/modules/admin/remote_config_write_service.py` — `RemoteConfigAdminService(BaseService)`
- `src/noorheroes/modules/admin/consent_version_proposal_models.py` — `ConsentVersionProposalOrm`
- `alembic/versions/xxxx_add_consent_version_proposal_table.py`
- `tests/modules/admin/test_remote_config_admin_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/admin/api.py` — add `GET/PUT /admin/v1/config/remote-config`, `POST /admin/v1/config/consent-version/propose`, `POST /admin/v1/config/consent-version/{proposal_id}/approve`

## 10. Backend Requirements
- `PUT /admin/v1/config/remote-config`: updates `min_supported_version`, `recommended_version`, `maintenance_mode` directly (no approval workflow needed for these — only `consent_version` is legally sensitive enough to require two-admin sign-off per PRD); validates semver format on version fields (reuse B-01's `compare_versions`/semver library for format validation, not for gating logic here).
- `POST /admin/v1/config/consent-version/propose`: creates a `ConsentVersionProposalOrm` row with `status=pending`, `proposed_by_admin_id`.
- `POST /admin/v1/config/consent-version/{proposal_id}/approve`: requires the approving admin's `admin_id` to differ from `proposed_by_admin_id` — reject with `409` if the same admin attempts to approve their own proposal; on approval, writes the new `consent_version` into the live `remote_config` row and marks the proposal `approved`.
- Every mutation (direct config update, propose, approve/reject) writes an `AdminAuditLog` row via `AdminService.log_action()` with before/after diff.
- No delete endpoint anywhere in this sub-feature — config is versioned via new rows/audit history, never destructively removed.

## 11. API Contract

### `GET /admin/v1/config/remote-config`
- Auth: `admin:write`. Response 200: current `remote_config` row.

### `PUT /admin/v1/config/remote-config`
- Auth: `admin:write`. Request: `{min_supported_version?, recommended_version?, maintenance_mode?, otp_health_threshold_pct?}` (never `consent_version` — excluded from this schema). Response 200: updated row. Audit: `AdminAuditLog` row written.
- Note: `otp_health_threshold_pct` (default `95.0`) was added to `remote_config` to resolve B-07/N-02's originally-open question of where the OTP-health alert threshold should be admin-configurable — it updates through this same direct (non-approval) path since it carries no legal weight, unlike `consent_version`.

### `POST /admin/v1/config/consent-version/propose`
- Auth: `admin:write`. Request: `{new_consent_version}`. Response 201: `{proposal_id, status: "pending"}`.

### `POST /admin/v1/config/consent-version/{proposal_id}/approve`
- Auth: `admin:write`, `admin_id != proposed_by_admin_id`. Response 200: `{status: "approved", consent_version}`. Errors: `409 SELF_APPROVAL_REJECTED`.

## 12. Database Requirements
Writes to B-01's `remote_config` table (Update-only). New `consent_version_proposal` table: `proposal_id` PK, `new_consent_version`, `proposed_by_admin_id`, `status` (`pending`/`approved`/`rejected`), `proposed_at`, `decided_by_admin_id`, `decided_at`.

## 13. Validation
Semver format validation on `min_supported_version`/`recommended_version`. `new_consent_version` non-empty string (format is a date-stamp convention per PRD examples, e.g. `2025-11-01` — validate as a reasonable version-string pattern, not necessarily strict semver, since consent versions in the PRD use date-based versioning).

## 14. Authentication
`get_current_admin`.

## 15. Authorization
`admin:write` scope for all four endpoints; additionally, approval requires the approving admin's identity to differ from the proposer's — this is a business-rule check, not a scope check.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| Same admin attempts to approve their own proposal | `409 SELF_APPROVAL_REJECTED` |
| Approving an already-approved/rejected proposal | `409`, no-op on the already-decided state |
| Malformed semver on direct config update | `422` |
| Attempt to set `consent_version` directly via `PUT` | Field not present in schema — physically impossible, not just rejected at runtime |

## 17. Security
Every mutation audit-logged with before/after diff and admin_id — no silent config changes possible. Two-admin approval is enforced server-side (not just a UI convention) — the API itself rejects self-approval.

## 18. Testing
Unit: self-approval rejection, double-approval no-op. Integration: full propose→approve flow updates the live `remote_config.consent_version`; full propose→reject flow leaves live config untouched; audit-log rows correctly capture before/after diff for both the direct-update and approval paths.

## 19. Documentation
Document clearly that only `consent_version` requires the two-approver workflow — other fields update immediately via `PUT`, to avoid confusing future maintainers into thinking all config changes need approval.

## 20. AI Coding Agent Implementation Steps

**Task 01 — Create `consent_version_proposal` Table & Migration**
Objective: Support the propose/approve workflow. Follow: standard migration conventions. Business Rules: `status` enum-like column constrained to `pending`/`approved`/`rejected`. Tests: migration smoke test. Definition of Done: table created cleanly.

**Task 02 — Implement `RemoteConfigWriteRepository`**
Objective: Update-only write access to B-01's `remote_config` row, plus proposal CRUD. Follow: `BaseRepository`, but expose only `update_config()` (no delete) for the config row itself. Tests: update-persists correctly, no delete method exists. Dependencies: B-01's `RemoteConfigOrm`. Definition of Done: repository has zero delete capability on `remote_config`.

**Task 03 — Implement `RemoteConfigAdminService`**
Objective: Direct-update logic + propose/approve business rules including self-approval rejection. Follow: `BaseService`, `AdminService.log_action()` for every mutation. Business Rules: self-approval rejection is the core rule to get right. Tests: full matrix per §18. Dependencies: Tasks 01–02. Definition of Done: self-approval rejection test passes; audit log correctly written for every mutation path.

**Task 04 — Add Router Endpoints**
Objective: Wire all four endpoints under `admin:write`. Follow: existing `AdminRouter` conventions, no DB access in router. Definition of Done: all four live and documented.

**Task 05 — Add Unit & Integration Tests**
Objective: Full coverage per §18. Definition of Done: all green in CI.

**Task 06 — Update OpenAPI Documentation**
Objective: Regenerate, confirm non-breaking diff. Definition of Done: diff classifier passes.

**Task 07 — Final Code Review**
Objective: Confirm no delete endpoint exists anywhere in this sub-feature, confirm self-approval is enforced server-side (not just client-side), confirm every mutation is audit-logged. Definition of Done: checklist in §21 checked.

## 21. Final Verification Checklist
- [x] No delete capability anywhere on `remote_config` or `consent_version_proposal`
- [x] `consent_version` field physically absent from the direct `PUT` schema
- [x] Self-approval rejected server-side with `409`, not just hidden client-side
- [x] Every mutation (direct update, propose, approve, reject) writes an `AdminAuditLog` row with before/after diff
- [x] Semver validation applied to version fields on direct update
- [x] Unit + integration tests green


## 22. Definition of Done
Remote config is admin-manageable via Create/Update-only endpoints, with `consent_version` specifically protected by a server-enforced two-admin approval workflow and full audit logging — ready for N-05 (Remote Configuration & Release Management Panel) to render, and closing the loop with B-01's read path.
