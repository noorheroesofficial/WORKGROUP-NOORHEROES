# B-11 — Admin Mission & Weekly Challenge Scheduler API (Admin)

> **⚠ DEPRECATED — superseded by `E31_Engagement_Tools_Admin_Suite/Backend/02-challenge-mission-management-api.md`.** E.31 B-02 covers daily mission, weekly challenge, and seasonal event CRUD against A.11's `missions` table, with the same archive-not-disappear (`ends_at`-computed status) design this file specified. Do not implement this file — implement E.31 B-02 instead. Retained for historical/design-rationale reference only.

## 1. Feature Context
Part of Feature A.11 — Rewards System. Admin CRUD for scheduling Daily/Weekly/Seasonal missions, with automatic archive-on-expiry (no manual archive action).

## 2. Parent Feature
A.11 Rewards System — Backend (FastAPI)

## 3. Sub-feature
B-11 Admin Mission & Weekly Challenge Scheduler API (Admin)

## 4. Objective
Implement admin CRUD for `missions` (B-05's table), restricted to `content_editor`, per PRD §8/§9.

## 5. Business Requirements
- CRUD for `missions` (`type`, `eligibility_json`, `criteria_json`, `reward_json`, `starts_at`, `ends_at`).
- No manual "archive" action — expired missions automatically display archived based on `ends_at`.
- `starts_at < ends_at` validated; no overlapping daily-mission scheduling per age band (avoid ambiguous "which 3 daily missions today" states).

## 6. Existing Architecture
Extends the `rewards` bounded context's admin surface, reusing B-05's `Mission` model directly (no new table).

## 7. Existing Code to Reuse
- B-05's `Mission` model.
- `require_admin_scope("content_editor")`.

## 8. Files to Create
- `tests/modules/rewards/test_mission_scheduler_crud.py`
- `tests/modules/rewards/test_mission_schedule_overlap_validation.py`

## 9. Files to Modify
- `src/noorheroes/modules/rewards/schemas.py` — `MissionCreateRequest`, `MissionAdminResponse`.
- `src/noorheroes/modules/rewards/service.py` — `create_mission()`, `list_missions_admin()` (with computed `status` field: active/scheduled/archived).
- `src/noorheroes/modules/rewards/api.py` — add admin routes under `/v1/admin/rewards/missions`.

## 10. Backend Requirements
- `status` is computed at read time from `starts_at`/`ends_at` vs. current time — never a stored, manually-toggled flag.
- Validate `starts_at < ends_at`.
- Validate no overlapping `daily` missions for the same age band beyond the intended 3-per-day design (reject a scheduling change that would create ambiguity in "today's 3 missions").
- RBAC: `content_editor` only.

## 11. KMP Requirements
Not applicable (admin-only); consumed indirectly via B-05's user-facing read.

## 12. NextJS Requirements
Consumed by N-03 (Mission & Weekly Challenge Scheduler).

## 13. API Contract

**Required API**
- **HTTP Method:** GET / POST / PATCH
- **Endpoint:** `/v1/admin/rewards/missions`
- **Auth:** Bearer, admin session, `content_editor` scope.
- **Request (POST):** `{ "type":"daily", "eligibility_json":{...}, "criteria_json":{...}, "reward_json":{...}, "starts_at":"...", "ends_at":"..." }`
- **Response 200 (list):** includes computed `status: "active"|"scheduled"|"archived"` per row.
- **Error Responses:** `422` invalid schedule (bad ordering, overlap).

## 14. Database Requirements
Reuses B-05's `missions` table; no new columns beyond what B-05 already defines, unless a `created_by`/admin-attribution column is needed (add if not already present).

## 15. Validation
Test: a mission with `ends_at` in the past is returned with `status: "archived"` automatically, with no admin action required.

## 16. Authentication
Bearer JWT, admin session.

## 17. Authorization
`require_admin_scope("content_editor")`.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| `starts_at >= ends_at` | 422 |
| Overlapping daily-mission schedule creating ambiguity | 422 with a clear conflict message |
| Unauthorized/forbidden request | 401/403 |

## 19. Offline First
N/A (admin web).

## 20. Local Data
N/A.

## 21. Localization
Mission title/description keys stored; localized text resolved elsewhere.

## 22. RTL
N/A (backend).

## 23. Analytics
N/A; mutations audit-logged.

## 24. Performance
Low-traffic admin endpoint.

## 25. Security
No manual archive/delete path prevents accidental loss of historical mission data relied upon for the archive-not-disappear child-facing guarantee (B-05 FR-10).

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, PostgreSQL, Pydantic v2.

## 27. Testing
- Unit: computed-status logic, overlap-validation logic.
- Integration: full CRUD flow, RBAC rejection tests.

## 28. Documentation
OpenAPI docs noting `status` is always computed, never manually settable.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement Mission CRUD Service Methods**
- Files to Modify: `service.py`
- Business Rules: schedule validation, computed status.
- Tests: CRUD + overlap-validation tests.
- Definition of Done: correct create/read/update behavior, no manual archive field.

**Task 02 — Implement Admin Endpoints with RBAC**
- Files to Modify: `api.py`
- Authentication/Authorization: per §16/§17.
- Tests: RBAC tests.
- Definition of Done: endpoints live.

**Task 03 — Add Documentation & Final Review**
- Documentation: OpenAPI notes per §28.
- Do Not Change: B-05's `missions` table shape beyond additive columns.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Admin mission scheduler live, RBAC-protected, computed-status archive behavior verified.

## 31. Final Verification Checklist
- [ ] `status` always computed from `starts_at`/`ends_at`, never manually toggled
- [ ] Schedule validation rejects invalid ordering/overlap
- [ ] RBAC restricts to `content_editor`
- [ ] No manual delete/archive action exists on this endpoint
- [ ] OpenAPI documentation complete
