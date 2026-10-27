# B-10 — Admin Badge & Achievement Definition Management API (Admin)

> **⚠ PARTIALLY DEPRECATED — badge CRUD superseded by `E31_Engagement_Tools_Admin_Suite/Backend/05-badge-management-api.md`.** Confirmed by inspection: E.31 B-05 covers `badges` CRUD + rule-based criteria against A.11's badge-awarding engine, but contains **no** `achievement_definitions` (cumulative achievement-level) CRUD and **no** Simulate/dry-run criteria-preview tool — both remain gaps not covered by E.31. Do not implement this file's badge-CRUD portion (§8/§9's badge-specific tasks) — implement E.31 B-05 instead. **This file's `achievement_definitions` CRUD and Simulate-tool sections remain A.11-owned and should still be implemented** (as a smaller, focused sub-feature scoped to just those two items) unless the architecture owner decides to fold them into E.31 B-05 instead — flagged for that explicit decision.

## 1. Feature Context
Part of Feature A.11 — Rewards System. Admin CRUD for `badges`/`achievement_definitions`, plus a non-mutating "Simulate" dry-run tool.

## 2. Parent Feature
A.11 Rewards System — Backend (FastAPI)

## 3. Sub-feature
B-10 Admin Badge & Achievement Definition Management API (Admin)

## 4. Objective
Implement admin CRUD for badge/achievement definitions and a dry-run criteria simulator, per PRD §8/§9, restricted to `content_editor`.

## 5. Business Requirements
- CRUD for `badges` (code, `criteria_json`, `locale_key`, optional `season_id`) and `achievement_definitions` (`criteria_json`, linked `badge_id`, `xp_value`).
- "Simulate" tool: given a fixture activity history, preview whether criteria would trigger — explicitly non-mutating, writes no real data.
- Prevent duplicate `badges.code`.

## 6. Existing Architecture
Extends the `rewards` bounded context's admin surface, reusing B-04's models (`Badge`, `AchievementDefinition`) and its evaluation logic (`badge_engine.py`) for the simulate tool — the simulator calls the same evaluation function B-04 uses in production, against a fixture input, rather than reimplementing criteria logic separately.

## 7. Existing Code to Reuse
- B-04's `badge_engine.evaluate_badges()` (called in dry-run mode with a fixture context, never persisting).
- `require_admin_scope("content_editor")`.

## 8. Files to Create
- `tests/modules/rewards/test_badge_definition_crud.py`
- `tests/modules/rewards/test_badge_simulate_no_writes.py`
- `tests/modules/rewards/test_badge_duplicate_code_rejected.py`

## 9. Files to Modify
- `src/noorheroes/modules/rewards/schemas.py` — `BadgeCreateRequest`, `AchievementDefinitionCreateRequest`, `SimulateRequest/Response`.
- `src/noorheroes/modules/rewards/service.py` — `create_badge()`, `create_achievement_definition()`, `simulate_criteria()`.
- `src/noorheroes/modules/rewards/api.py` — add admin routes under `/v1/admin/rewards/badges`, `/v1/admin/rewards/achievements`.

## 10. Backend Requirements
- `UNIQUE(badges.code)` enforced at the DB layer (already present per B-04 §14) and re-validated with a friendly error at the API layer.
- `criteria_json` validated against a defined structural schema before save (reject malformed JSON early, not just at evaluation time).
- `simulate_criteria()` calls `badge_engine.evaluate_badges()` in a read-only/dry-run mode — no `child_badges`/`achievement_progress` row is ever written by this path; enforced by passing a non-persisting evaluation flag or by running against an in-memory fixture context rather than a real `child_id`.
- RBAC: `content_editor` only.

## 11. KMP Requirements
Not applicable (admin-only).

## 12. NextJS Requirements
Consumed by N-02 (Badge & Achievement Definition Manager).

## 13. API Contract

**Required API**
- **HTTP Method:** GET / POST / PATCH
- **Endpoint:** `/v1/admin/rewards/badges`, `/v1/admin/rewards/achievements`
- **Auth:** Bearer, admin session, `content_editor` scope.
- **Error Responses:** `409` duplicate `code`; `422` invalid `criteria_json`.

**Required API — Simulate**
- **HTTP Method:** POST
- **Endpoint:** `/v1/admin/rewards/badges/{id}/simulate`
- **Request:** `{ "fixture_activity_history": [...] }`
- **Response 200:** `{ "would_trigger": true, "explanation": "..." }` — dry-run only, no persistence.

## 14. Database Requirements
Reuses B-04's `badges`/`achievement_definitions` tables; no new tables in this task.

## 15. Validation
Test: `simulate_criteria()` call, when inspected, results in zero new rows in `child_badges`/`achievement_progress` regardless of fixture input.

## 16. Authentication
Bearer JWT, admin session.

## 17. Authorization
`require_admin_scope("content_editor")`.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Duplicate badge code | 409, clear message |
| Malformed `criteria_json` | 422, field-level errors, rejected before save |
| Simulate called with an invalid fixture shape | 422, no evaluation attempted |
| Unauthorized/forbidden request | 401/403 |

## 19. Offline First
N/A (admin web).

## 20. Local Data
N/A.

## 21. Localization
`locale_key` stored, resolved to display text elsewhere (client-side/admin-UI-side); this API stores keys only.

## 22. RTL
N/A (backend).

## 23. Analytics
N/A; mutations audit-logged instead.

## 24. Performance
Low-traffic admin endpoint.

## 25. Security
Simulate tool's non-mutating guarantee is a trust property for admin users — verified by an automated no-writes test, not just documentation.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, PostgreSQL (JSONB), Pydantic v2, JSON-schema validation for `criteria_json`.

## 27. Testing
- Unit: `criteria_json` schema validation.
- Integration: full CRUD flow, duplicate-code rejection, simulate dry-run correctness and no-writes guarantee (mandatory).

## 28. Documentation
Document the `criteria_json` DSL for content authors with worked examples (cross-ref B-04 §28).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement Badge/Achievement CRUD Service Methods**
- Files to Modify: `service.py`
- Business Rules: duplicate-code rejection, `criteria_json` schema validation.
- Tests: CRUD + duplicate-rejection tests.
- Definition of Done: correct create/read/update behavior.

**Task 02 — Implement Simulate Dry-Run Tool**
- Files to Modify: `service.py`
- Existing Files to Reuse: `badge_engine.evaluate_badges()` (B-04), called in non-persisting mode.
- Tests: no-writes guarantee test (mandatory).
- Do Not Change: never let the simulate path share a persistence code path with the real evaluation trigger.
- Definition of Done: no-writes test passing.

**Task 03 — Implement Admin Endpoints with RBAC**
- Files to Modify: `api.py`
- Authentication/Authorization: per §16/§17.
- Tests: RBAC tests.
- Definition of Done: endpoints live.

**Task 04 — Add Documentation & Final Review**
- Documentation: `criteria_json` DSL doc.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Badge/achievement admin CRUD live; simulate tool verifiably non-mutating; RBAC-protected.

## 31. Final Verification Checklist
- [x] Duplicate badge code rejected with 409
- [x] `criteria_json` schema-validated before save
- [x] Simulate tool produces zero persisted writes under any fixture input
- [x] RBAC restricts to `content_editor`
- [x] OpenAPI documentation complete
