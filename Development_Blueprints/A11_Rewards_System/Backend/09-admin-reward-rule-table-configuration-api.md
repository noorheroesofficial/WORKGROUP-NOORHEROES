# B-09 — Admin Reward Rule Table Configuration API (Admin)

> **⚠ DEPRECATED — superseded by `E31_Engagement_Tools_Admin_Suite/Backend/03-xp-rule-management-api.md`.** Feature E.31's PRD explicitly frames itself as "the admin-authoring layer atop A.11's already-hardened Reward Service," and its B-03 covers this exact same versioned XP-rule-table CRUD surface, built with awareness of this dependency. Do not implement this file — implement E.31 B-03 instead, which reuses `RewardService`/`reward_rule_version` exactly as this file specified. This file is retained for historical/design-rationale reference only (its business requirements and versioning-immutability rules remain valid and were carried into E.31 B-03).

## 1. Feature Context
Part of Feature A.11 — Rewards System. Admin-side CRUD for the activity-type → XP/Noor-Heroes-Points reward-rule table that B-01's award engine resolves against.

## 2. Parent Feature
A.11 Rewards System — Backend (FastAPI)

## 3. Sub-feature
B-09 Admin Reward Rule Table Configuration API (Admin)

## 4. Objective
Implement admin CRUD for versioned reward rules per activity type, per FR-7's representative defaults and PRD §8.

## 5. Business Requirements
- Editing a rule creates a **new version**, never mutates a version already used to compute past ledger entries (immutability of historical rule versions).
- Per-age-band overrides and per-activity-type `daily_cap` are configurable.
- Restricted to `economy_design`/`product_admin` role.
- Every mutation writes an immutable `audit_log` row.

## 6. Existing Architecture
Extends the `rewards` bounded context's admin surface, reusing `require_admin_scope("economy_design")`/`require_admin_scope("product_admin")` and the existing audit-log infrastructure already used across other admin CRUD modules (e.g., content/localization admin flows).

## 7. Existing Code to Reuse
- `get_current_admin`, `require_admin_scope` dependencies.
- Existing `audit_log` write helper (reused from wherever other admin mutations already write it — confirm the exact shared utility before adding a parallel one).

## 8. Files to Create
- `src/noorheroes/modules/rewards/models.py` — extend with `RewardRule` (versioned).
- `alembic/versions/<rev>_create_reward_rule_table.py`
- `tests/modules/rewards/test_reward_rule_versioning.py`
- `tests/modules/rewards/test_reward_rule_admin_rbac.py`

## 9. Files to Modify
- `src/noorheroes/modules/rewards/schemas.py` — `RewardRuleCreateRequest`, `RewardRuleResponse`.
- `src/noorheroes/modules/rewards/service.py` — `create_rule_version()`, `list_rule_versions(activity_type)`.
- `src/noorheroes/modules/rewards/api.py` — add admin routes under `/v1/admin/rewards/rules`.

## 10. Backend Requirements
- `reward_rules`: versioned rows keyed by `(activity_type, version)`, never updated in place — a new row is inserted for each edit, with the previous version's `valid_to` set (or an equivalent versioning scheme consistent with how B-01 resolves "active version at completion time").
- Validate positive XP/points values, non-overlapping effective windows per `activity_type`.
- RBAC: `economy_design`/`product_admin` only.

## 11. KMP Requirements
Not applicable (admin-only); indirectly consumed via B-01's rule resolution.

## 12. NextJS Requirements
Consumed by N-01 (Reward Rule Table Editor).

## 13. API Contract

**Required API**
- **HTTP Method:** GET / POST
- **Endpoint:** `/v1/admin/rewards/rules`, `/v1/admin/rewards/rules/{activity_type}/versions`
- **Auth:** Bearer, admin session, `economy_design`/`product_admin` scope.
- **Request (POST):** `{ "activity_type":"...", "xp_value":30, "noor_points_value":15, "age_band_overrides":{...}, "daily_cap":5 }`
- **Response 201:** created rule version with an assigned `version` identifier.
- **Error Responses:** `401`/`403` insufficient scope; `422` invalid payload.

## 14. Database Requirements
`reward_rules`: `id UUID PK`, `activity_type VARCHAR`, `version VARCHAR`, `xp_value INT`, `noor_points_value INT`, `age_band_overrides JSONB`, `daily_cap INT`, `valid_from TIMESTAMPTZ`, `valid_to TIMESTAMPTZ NULL`, `created_by UUID FK`. Index `(activity_type, valid_from)`.

## 15. Validation
Test: editing a rule creates a new version row; the previous version remains unchanged and still resolvable for historical ledger entries computed under it.

## 16. Authentication
Bearer JWT, admin session.

## 17. Authorization
`require_admin_scope("economy_design")` or `require_admin_scope("product_admin")`.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Attempt to mutate a version already in use | Rejected; a new version must be created instead |
| Unauthorized/forbidden request | 401/403 |
| Invalid payload (negative values, overlapping windows) | 422 with field-level errors |

## 19. Offline First
N/A (admin web).

## 20. Local Data
N/A.

## 21. Localization
Admin UI localization is N-01's concern; this API returns raw values only.

## 22. RTL
N/A (backend).

## 23. Analytics
N/A (internal admin action; audit-logged instead).

## 24. Performance
Low-traffic admin endpoint; no special performance requirements beyond standard CRUD latency.

## 25. Security
Version-immutability prevents retroactive tampering with historical reward calculations — a trust/auditability property, not just a UX one.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, PostgreSQL, Pydantic v2.

## 27. Testing
- Unit: versioning-immutability logic.
- Integration: full create-new-version flow, RBAC rejection tests.

## 28. Documentation
OpenAPI docs; update Admin module reference in `NEXT-JS-INSTRUCTIONS.md`-adjacent backend contract notes if such a shared contract doc exists.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create `RewardRule` Model & Migration**
- Files to Create: model + migration.
- Definition of Done: table created with versioning fields.

**Task 02 — Implement Versioned Create/List Service Methods**
- Files to Modify: `service.py`
- Business Rules: version-immutability.
- Tests: versioning test (mandatory).
- Definition of Done: new-version-only edit pattern verified.

**Task 03 — Implement Admin Endpoints with RBAC**
- Files to Modify: `api.py`
- Authentication/Authorization: per §16/§17.
- Tests: RBAC rejection tests.
- Definition of Done: endpoints live, correctly scoped.

**Task 04 — Wire Audit Logging**
- Implementation Details: every mutation writes an immutable audit_log row.
- Definition of Done: verified via test.

**Task 05 — Add Documentation & Final Review**
- Documentation: OpenAPI docs.
- Do Not Change: version-immutability guarantee.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Admin rule-table CRUD live, versioned, RBAC-protected, audit-logged.

## 31. Final Verification Checklist
- [ ] New rule edits always create a new version, never mutate an in-use one
- [ ] RBAC restricts to `economy_design`/`product_admin`
- [ ] Audit log entry written per mutation
- [ ] Validation rejects invalid/negative/overlapping rule payloads
- [ ] OpenAPI documentation complete
