# B-03 — XP Rule Management API

> **Reconciliation note (2026-08-18):** A.11 Rewards System's own blueprint originally specified an equivalent admin surface at `A11_Rewards_System/Backend/09-admin-reward-rule-table-configuration-api.md` (B-09). That file is now marked deprecated in favor of this one — this file (E.31 B-03) is authoritative for versioned XP-rule admin CRUD.

## 1. Feature Context
Part of **Feature E.31 — Engagement Tools Admin Suite**. Delivers the admin surface for the versioned XP rule table (per activity type), split out from reward-ledger concerns (see **B-04 Reward Ledger & Manual Grant API**) because the PRD treats XP Rule Table (Screen #7) and XP Rule Editor (Screen #8) as distinct authoring surfaces from the read-only Ledger Viewer (#9) and Manual Reward Grant Tool (#10). Source: `PRD_Documents/Admin & Scholar Portal (28-34)/Feature_E31_Engagement_Tools_Admin_Suite.md` §1.7 FR-3 (XP-rule portion), §1.18 Screens 7–8, §3.4.

## 2. Parent Feature
Feature E.31 — Engagement Tools Admin Suite

## 3. Sub-feature
1.3 XP Rule Management API (Backend ID: **B-03**)

## 4. Objective
Give content admins a versioned XP-rule table per activity type, with a structural guarantee that any update always creates a new effective-dated rule version rather than mutating a rule that has already been applied to historical `reward_ledger` entries — the same non-retroactivity discipline already established for habit templates (B-01) and badge criteria (B-05).

## 5. Business Requirements
- FR-3 (PRD §1.7, XP-rule portion): screens — XP rule table (per activity type). CRUD: create XP rule; update XP rule (versioned).
- **Hard rule:** `PATCH` to an XP rule always creates a new versioned rule (A.11's `reward_rule_version` pattern), never mutates a rule already applied historically.
- Cross-cutting concern (PRD §3.5): "No-retroactivity via versioning, not mutation: XP rules and badge criteria both use the 'new version, never edit the old' pattern."

## 6. Existing Architecture
Extends A.11's Reward Service. FastAPI/SQLAlchemy 2.0/PostgreSQL, Router → Service → Repository layering, consistent with B-01/B-05's versioning pattern.

## 7. Existing Code to Reuse
- A.11's existing `reward_rule_version` table and versioning pattern (reused, not reinvented, per PRD §3.5).
- E.28's audit log client and `require_role("content_editor")` RBAC dependency.

## 8. Files to Create
- `app/routers/admin/xp_rules_router.py`
- `app/schemas/admin/xp_rule_schemas.py`
- `app/services/admin/xp_rule_admin_service.py`
- `app/repositories/admin/xp_rule_admin_repository.py`
- `tests/admin/test_xp_rule_admin_api.py`

## 9. Files to Modify
- `app/routers/admin/__init__.py`
- `app/core/audit.py` (`xp_rule.created`, `xp_rule.updated`)

## 10. Backend Requirements
- **Database:** `reward_rule_version` (existing A.11 table), keyed by `activity_type`, reused as-is.
- **Migration:** none required if A.11 already versions this table; otherwise additive migration to introduce versioning.
- **Model:** `RewardRuleVersion`.
- **Schema/DTO:** `XPRuleCreate` (`activity_type`, `xp_value`), `XPRuleUpdate` (`xp_value` — always creates a new version), `XPRuleRead` (includes `effective_from`, `version_history` summary).
- **Repository:** `create_xp_rule_version()`, `list_xp_rules()` (current effective version per activity type), `list_version_history(activity_type)`, `deactivate_xp_rule()`.
- **Service:** `XPRuleAdminService` — validates `activity_type` against the registry, orchestrates versioned insert, audit-logs.
- **Router:** `GET /v1/admin/xp-rules`, `POST /v1/admin/xp-rules`, `PATCH /v1/admin/xp-rules/{id}`, `GET /v1/admin/xp-rules/{id}/history`.
- **Dependency Injection:** `require_role("content_editor")`.
- **Authentication/Authorization:** admin JWT; `content_editor`+.
- **Validation:** `activity_type` must exist in the platform's activity-type registry; `xp_value` positive integer within configured bounds.
- **Business Rules:** `PATCH` always inserts a new `RewardRuleVersion` row with `effective_from = now()`; historical `reward_ledger` entries reference the rule version active at the time XP was awarded and are never recalculated.
- **Exception Handling:** `404` unknown activity_type/rule id, `422` invalid `xp_value`/`activity_type`.
- **Logging:** structured logs on create/update including `admin_id`, `activity_type`, old/new `xp_value`.
- **Caching:** invalidate any Redis-cached "current XP rules by activity type" map consumed by A.11's reward-issuance engine on write.
- **Transaction:** version insert + audit log write in a single transaction.
- **Pagination/Filtering/Sorting:** rule list filterable by `activity_type`; version history paginated.

## 11. KMP Requirements
N/A — admin-only. The KMP app never calls `/v1/admin/*`; A.11's existing reward-issuance engine reads the currently-effective XP rule transparently at check-in/activity time.

## 12. NextJS Requirements
Consumed by **N-03 XP Rule Management UI**, which must display the "changes apply only going forward; past awards are never affected" helper text on the rule editor.

## 13. API Contract

### `POST /v1/admin/xp-rules`
- **Authorization:** `content_editor`+
- **Request:** `{ "activity_type": "quran_verse_memorized", "xp_value": 25 }`
- **Response (201):** `XPRuleRead`
- **Errors:** `401`, `403`, `422 VALIDATION_ERROR`, `409 DUPLICATE_ACTIVITY_TYPE`

### `GET /v1/admin/xp-rules`
- Response: current effective rule per `activity_type`, paginated.

### `PATCH /v1/admin/xp-rules/{id}`
- **Request:** `{ "xp_value": 30 }`
- **Response (200):** new `RewardRuleVersion`, `effective_from` timestamp — never mutates a prior version
- **Errors:** `404`, `422`

### `GET /v1/admin/xp-rules/{id}/history`
- **Response (200):** full version history for the given activity type, read-only.

## 14. Database Requirements
`reward_rule_version`: existing A.11 table reused; index `(activity_type, effective_from DESC)`.

## 15. Validation
`activity_type` registered; `xp_value` positive integer within bounds.

## 16. Authentication
Admin JWT (E.28).

## 17. Authorization
`content_editor`+.

## 18. Error Handling
| Scenario | Response |
|---|---|
| Unregistered `activity_type` | `422 VALIDATION_ERROR` |
| Unknown rule id | `404 NOT_FOUND` |
| Unauthorized/forbidden | `401`/`403` |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
`activity_type` display labels localized in the UI layer; backend stores the registry key only.

## 22. RTL
N/A at API layer.

## 23. Analytics
`xp_rule_created`, `xp_rule_updated` (PRD §1.19).

## 24. Performance
Redis-cached "current XP rules" map invalidated on write, read by A.11's high-throughput reward-issuance path.

## 25. Security
Non-retroactivity is structurally guaranteed via versioning, not a validated-but-mutable field — consistent with the platform's broader non-retroactive-restriction philosophy (PRD §1.8).

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Pydantic v2, pytest-asyncio.

## 27. Testing
- Unit: `activity_type` validation, versioning logic.
- Integration: signature no-retroactivity test — update `xp_value` for an activity type, verify a fixture historical `reward_ledger` entry predating the change retains its original awarded XP.
- Negative cases: invalid `activity_type`, unauthorized.

## 28. Documentation
OpenAPI docs explicitly stating the versioned, non-retroactive nature of XP rule updates.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm/Extend Versioning Model**
- Task ID: B-03-T01
- Objective: Confirm `reward_rule_version` supports per-activity-type versioning; extend if needed.
- Files to Modify: `app/models/reward_rule_version.py` (if changes needed).
- Tests: migration test.
- Dependencies: none.
- Do Not Change: `reward_ledger` schema.
- Definition of Done: model supports versioned lookups by `activity_type`.

**Task 02 — Repository & Service Layers**
- Task ID: B-03-T02
- Files to Create: `app/repositories/admin/xp_rule_admin_repository.py`, `app/services/admin/xp_rule_admin_service.py`.
- Implementation Details: `create_xp_rule_version` always INSERTs.
- Dependencies: Task 01.
- Definition of Done: unit tests green.

**Task 03 — API Endpoints**
- Task ID: B-03-T03
- Files to Create: `app/routers/admin/xp_rules_router.py`.
- Dependencies: Task 02.
- Definition of Done: integration tests green.

**Task 04 — Non-Retroactivity Signature Test**
- Task ID: B-03-T04
- Implementation Details: seed a fixture `reward_ledger` entry tied to a rule version predating "now"; PATCH `xp_value`; re-fetch fixture entry and assert it is unchanged.
- Tests: `tests/admin/test_xp_rule_admin_api.py::test_xp_rule_update_does_not_affect_historical_ledger_entries`.
- Dependencies: Tasks 01–03.
- Definition of Done: test passes, CI-blocking per PRD §10.

**Task 05 — Documentation & Final Review**
- Task ID: B-03-T05
- Dependencies: Tasks 01–04.
- Definition of Done: §31 checklist verified.

## 30. Definition of Done
XP rule CRUD implemented and versioned; non-retroactivity proven by regression test; audit logging in place; cache invalidation verified.

## 31. Final Verification Checklist
- [ ] `POST /v1/admin/xp-rules` creates a rule with an initial version
- [ ] `PATCH .../{id}` always inserts a new version, never mutates
- [ ] Historical `reward_ledger` entries unaffected by XP-value update (regression test green)
- [ ] Version history endpoint returns full audit trail
- [ ] Redis cache invalidated on write
- [ ] Audit log entries written for every mutation
- [ ] Unauthorized/forbidden paths tested
- [ ] No school/madrasa/institutional-tier logic introduced
- [ ] PostgreSQL/Redis credentials untouched
