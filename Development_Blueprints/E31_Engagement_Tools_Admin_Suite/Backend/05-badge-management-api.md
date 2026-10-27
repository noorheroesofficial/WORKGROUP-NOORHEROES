# B-05 — Badge Management API

> **Reconciliation note (2026-08-18):** A.11 Rewards System's own blueprint originally specified an equivalent surface at `A11_Rewards_System/Backend/10-admin-badge-achievement-definition-management-api.md` (B-10). That file's `badges` CRUD portion is now marked deprecated in favor of this one — this file (E.31 B-05) is authoritative for badge CRUD + criteria. **Scope gap flagged:** B-10 also specified `achievement_definitions` (cumulative achievement-level) CRUD and a Simulate/dry-run criteria-preview tool, neither of which exists in this file. Confirm with the architecture owner whether to extend this file to cover both, or leave them as a small residual A.11-owned surface (B-10's relevant sections remain valid for that purpose either way).

## 1. Feature Context
Part of **Feature E.31 — Engagement Tools Admin Suite**. Delivers the admin CRUD surface for badges and rule-based criteria consumed by A.11's reward/badge-awarding engine. Source: PRD §1.7 FR-4, §3.4, §5 item 2.

## 2. Parent Feature
Feature E.31 — Engagement Tools Admin Suite

## 3. Sub-feature
1.5 Badge Management API (Backend ID: **B-05**)

## 4. Objective
Let content admins create badges and define/update rule-based criteria, while structurally guaranteeing that a criteria update never revokes an already-awarded badge, and that criteria always reference a real, registered event type.

## 5. Business Requirements
- FR-4 (PRD §1.7): screens — badge library, criteria builder (rule-based), icon/asset upload. CRUD: create badge+criteria, read award count, update criteria (new badges only, not retroactive), retire badge.
- **Hard rule:** criteria changes never revoke already-awarded badges.
- **Hard rule:** criteria must reference an existing, valid event type.
- Edge Case 2 (PRD §1.10): a cosmetic icon change for an already-awarded badge is permitted — the no-retroactivity rule protects *criteria*, not presentation.
- Edge Case 4 (PRD §1.10): an avatar item's unlock rule referencing a later-retired badge degrades gracefully (handled in B-06, but the retire semantics here must support it).

## 6. Existing Architecture
Extends A.11's Reward Service (badge criteria evaluator). FastAPI/SQLAlchemy 2.0/PostgreSQL, Router → Service → Repository layering.

## 7. Existing Code to Reuse
- A.11's existing `badges`/`child_badges` models and badge-award evaluation engine (not reimplemented here — this is authoring only).
- A.11's/platform's event-type registry for criteria validation.
- E.28's audit log + RBAC; E.29's upload-safety pipeline for badge icons.

## 8. Files to Create
- `app/routers/admin/badges_router.py`
- `app/schemas/admin/badge_schemas.py`
- `app/services/admin/badge_admin_service.py`
- `app/repositories/admin/badge_admin_repository.py`
- `tests/admin/test_badge_admin_api.py`

## 9. Files to Modify
- `app/routers/admin/__init__.py`
- `app/core/audit.py` (`badge.created`, `badge.criteria_updated`, `badge.icon_updated`, `badge.retired`)

## 10. Backend Requirements
- **Database:** `badges` (existing A.11, extended with `criteria` JSON/structured column and `active` flag if not present), `child_badges` (existing, read-only reference — never mutated by this layer).
- **Migration:** additive only.
- **Model:** `Badge`, `BadgeCriteriaVersion` (new, if criteria itself needs versioning for audit-trail purposes — PRD requires zero *effect* on `child_badges`, which can be achieved either via immutable evaluation-at-award-time semantics or explicit versioning; implement versioning for full auditability consistent with B-01/B-03's pattern).
- **Schema/DTO:** `BadgeCreate` (name, icon_asset_id, criteria: `{event_type, condition, threshold}`), `BadgeCriteriaUpdate` (new criteria — creates new version), `BadgeIconUpdate` (cosmetic-only, direct mutation permitted), `BadgeRead` (includes `award_count`).
- **Repository:** `create()`, `list_with_award_count()`, `update_criteria()` (versioned insert), `update_icon()` (direct mutation), `retire()`.
- **Service:** validates `event_type` against registry, orchestrates versioning, audit logs, upload-pipeline calls.
- **Router:** `POST /v1/admin/badges`, `GET /v1/admin/badges`, `PATCH /v1/admin/badges/{id}/criteria`, `PATCH /v1/admin/badges/{id}/icon`, `POST /v1/admin/badges/{id}/retire`.
- **Dependency Injection:** `require_role("content_editor")`.
- **Validation:** `event_type` must exist in the registry (reject unrecognized types with `422`); `threshold`/`condition` type-checked against the event type's expected schema.
- **Business Rules:** `update_criteria` never touches `child_badges`; A.11's award-evaluation engine reads the currently-active criteria version only for *future* evaluations — this sub-feature must not trigger any re-evaluation job against existing children.
- **Exception Handling:** `404`, `422 INVALID_EVENT_TYPE`.
- **Logging:** structured logs on every mutation.
- **Caching:** invalidate cached "active badge criteria" list consumed by A.11's evaluation engine.
- **Transaction:** criteria update + audit log in one transaction.
- **Pagination/Filtering/Sorting:** badge library list paginated, filterable by active/retired status.

## 11. KMP Requirements
N/A — admin-only. Badge award/display in the KMP app continues via A.11/A.12's existing child-facing endpoints, which read only the currently-active criteria and current icon.

## 12. NextJS Requirements
Consumed by **N-05 Badge Management UI**, including the structured rule-builder component and the invalid-event-type error state.

## 13. API Contract

### `POST /v1/admin/badges`
- **Request:** `{ "name_key": "seven_day_streak", "icon_asset_id": "uuid", "criteria": { "event_type": "habit_streak", "condition": "gte", "threshold": 7 } }`
- **Response (201):** `BadgeRead`
- **Errors:** `401`, `403`, `422 INVALID_EVENT_TYPE`, `422 ICON_UPLOAD_REJECTED`

### `PATCH /v1/admin/badges/{id}/criteria`
- **Request:** `{ "criteria": { "event_type": "stories_completed", "condition": "gte", "threshold": 5 } }`
- **Response (200):** new criteria version; `child_badges` unaffected
- **Errors:** `404`, `422 INVALID_EVENT_TYPE`

### `PATCH /v1/admin/badges/{id}/icon`
- **Request:** `{ "icon_asset_id": "uuid" }` — cosmetic only, permitted even for already-awarded badges
- **Response (200):** updated `BadgeRead`

### `POST /v1/admin/badges/{id}/retire`
- **Response (200):** `{ "id": "uuid", "active": false }`

## 14. Database Requirements
- `badges`: extended with `active boolean`.
- `badge_criteria_version` (new): `id`, `badge_id FK`, `criteria JSONB`, `effective_from`, `created_by_admin_id`.
- `child_badges`: read-only, no schema change, never mutated by this sub-feature.

## 15. Validation
`event_type` in registry; `condition` ∈ {`gte`, `lte`, `eq`, ...}; `threshold` type matches event type's expected value type.

## 16. Authentication
Admin JWT (E.28).

## 17. Authorization
`content_editor`+.

## 18. Error Handling
| Scenario | Response |
|---|---|
| Unregistered event_type in criteria | `422 INVALID_EVENT_TYPE` |
| Unknown badge id | `404 NOT_FOUND` |
| Icon fails upload-safety pipeline | `422 ICON_UPLOAD_REJECTED` |
| Unauthorized/forbidden | `401`/`403` |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
`name_key`/description reference localization keys, not raw strings.

## 22. RTL
N/A at API layer.

## 23. Analytics
`badge_created`, `badge_criteria_updated` per PRD §1.19.

## 24. Performance
`award_count` aggregation via indexed query on `child_badges(badge_id)`; criteria-active-version cache invalidated on write for A.11's evaluation engine consumption.

## 25. Security
No child PII beyond referencing `child_id` in `child_badges` (unmodified by this layer); every mutation audit-logged.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Pydantic v2, pytest-asyncio.

## 27. Testing
- Unit: event-type validation, versioning logic.
- Integration: signature no-retroactivity test — fixture child's already-awarded `child_badges` row unaffected by subsequent criteria update, even if new criteria wouldn't have qualified them (PRD §5 item 2).
- Edge cases: Edge Case 2 — icon update for already-awarded badge permitted.
- Negative cases: invalid event_type, unauthorized.

## 28. Documentation
OpenAPI docs explicitly distinguishing criteria updates (non-retroactive) from icon updates (retroactive-cosmetic-permitted).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Database Models**
- Task ID: B-05-T01
- Objective: Add `BadgeCriteriaVersion` model and `active` flag on `Badge`.
- Files to Create: `app/models/badge_criteria_version.py`.
- Files to Modify: `app/models/badge.py`.
- Tests: migration test.
- Dependencies: none.
- Do Not Change: `child_badges` schema.
- Definition of Done: migration applies cleanly.

**Task 02 — Repository & Service Layers**
- Task ID: B-05-T02
- Files to Create: `app/repositories/admin/badge_admin_repository.py`, `app/services/admin/badge_admin_service.py`.
- Implementation Details: `update_criteria` always inserts a new version; `update_icon` mutates directly; event-type registry check in service layer before repository call.
- Dependencies: Task 01.
- Definition of Done: unit tests green.

**Task 03 — API Endpoints**
- Task ID: B-05-T03
- Files to Create: `app/routers/admin/badges_router.py`.
- Dependencies: Task 02.
- Definition of Done: integration tests green.

**Task 04 — No-Retroactivity Signature Test**
- Task ID: B-05-T04
- Implementation Details: seed a fixture `child_badges` row awarded under old criteria; PATCH criteria to something the child wouldn't qualify for; re-fetch `child_badges` row and assert it is completely unchanged/still present.
- Tests: `tests/admin/test_badge_admin_api.py::test_criteria_update_does_not_revoke_awarded_badge`.
- Dependencies: Tasks 01–03.
- Definition of Done: test passes, part of CI-blocking suite per PRD §10.

**Task 05 — Icon-Update-Permitted Test (Edge Case 2)**
- Task ID: B-05-T05
- Tests: `test_icon_update_permitted_for_already_awarded_badge`.
- Dependencies: Tasks 01–03.
- Definition of Done: test passes.

**Task 06 — Documentation & Final Review**
- Task ID: B-05-T06
- Dependencies: Tasks 01–05.
- Definition of Done: §31 checklist verified.

## 30. Definition of Done
Criteria-update no-retroactivity proven by regression test; icon-update-permitted behavior proven; event-type validation enforced; all endpoints audited and tested.

## 31. Final Verification Checklist
- [ ] `POST /v1/admin/badges` creates badge with initial criteria version
- [ ] `PATCH .../criteria` creates a new version, never mutates existing
- [ ] Already-awarded `child_badges` rows unaffected by criteria update (regression test green)
- [ ] `PATCH .../icon` permitted for already-awarded badges (cosmetic exception verified)
- [ ] Unregistered `event_type` rejected with `422`
- [ ] Retire sets `active=false`, no cascade into `child_badges`
- [ ] Audit log entries written for every mutation
- [ ] Unauthorized/forbidden paths tested
- [ ] No school/madrasa/institutional-tier logic introduced
- [ ] PostgreSQL/Redis credentials untouched
