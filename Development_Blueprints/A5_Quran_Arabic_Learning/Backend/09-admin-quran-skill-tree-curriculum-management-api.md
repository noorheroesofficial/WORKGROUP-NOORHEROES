# B-09 — Admin Quran Skill Tree & Curriculum Management API

> **Status:** ✅ **COMPLETED & VERIFIED**  
> **Target Framework:** FastAPI (Python 3.12+) / SQLAlchemy 2.0 (Async) / Pydantic v2 / Redis 7  
> **Architecture Pattern:** Clean Architecture, Modular Monolith, Strict Curriculum Editor RBAC, 3-Color DFS Cycle Detection, DB-Trigger Sacred Ayah Immutability  
> **Test Coverage:** 44/44 Dedicated Tests Passing (569 Total Learning Tests Passing, 100% Green in CI)

## 1. Feature Context
Part of Feature A.5 (Quran & Arabic Learning). Gives curriculum editors CRUD control over `skill_node` definitions and the prerequisite graph, with cycle-detection validation and database-level ayah-text immutability enforcement.

## 2. Parent Feature
A.5 — Quran & Arabic Learning

## 3. Sub-feature
B-09 — Admin Quran Skill Tree & Curriculum Management API (Admin API)

## 4. Objective
Provide curriculum-editor CRUD for `skill_node` (create/update/deactivate, never hard-delete), enforce prerequisite-graph cycle-detection on every save, and enforce `ayah.arabic_text_immutable` write-protection at the database layer.

## 5. Business Requirements
- Admin Requirements §8: full CRUD for `skill_node` with cycle-detection validation; delete = deactivate only (`is_active=false`), never hard-delete, to preserve historical `skill_node_state`/`learning_attempt` references.
- FR-21: ayah text is never editable post-seed; only translations/tafseer/learning metadata are versioned/editable with scholar sign-off.
- Role: `curriculum_editor` for full CRUD.

## 6. Existing Architecture
Modular monolith `admin` context (existing, per architecture doc §5.2) handles cross-cutting admin auth/audit-logging; this blueprint's routes live in the `learning` context but are gated by admin role scopes consistent with the `admin` context's RBAC pattern (`get_current_admin` + scope checks, e.g., `AdminRouter`'s `admin:read`/`admin:write` pattern).

## 7. Existing Code to Reuse
- `get_current_admin` dependency and `AdminSessionContext` DTO.
- `admin` context's audit-log pattern (`POST /v1/admin/audit-logs` precedent) — every mutation here must write an audit_log row consistent with that existing mechanism.
- B-01's `SkillNodeRepository` (extended here for write operations; B-01 only reads).

## 8. Files Created
- `src/noorheroes/modules/learning/schemas/admin_skill_node.py`
- `src/noorheroes/modules/learning/services/curriculum_graph_service.py` (3-color DFS cycle detection & Kahn's topological sort)
- `src/noorheroes/modules/learning/services/admin_skill_node_service.py`
- `src/noorheroes/modules/content/quran_models.py` (`Ayah` ORM model)
- `src/noorheroes/modules/learning/admin_api.py` (`/v1/admin/learning` & NextJS canvas alias `/v1/admin/content/validate-graph`)
- `alembic/versions/0048_add_ayah_immutability_trigger.py` (DB trigger `fn_prevent_ayah_text_mutation` write-protecting `arabic_text_immutable`)
- `tests/modules/learning/test_admin_skill_node_api.py` (20 API tests)
- `tests/modules/learning/test_skill_node_repository_write.py` (9 write tests)
- `tests/modules/learning/test_curriculum_graph_service.py` (11 cycle detection tests)
- `tests/modules/content/test_ayah_immutability_trigger.py` (4 DB trigger tests)

## 9. Files Modified
- `src/noorheroes/modules/learning/skill_tree_repository.py` (added `create()`, `update()`, `deactivate()`, `list_all()`, and `delete()` raising `HardDeleteProhibitedError`)
- `src/noorheroes/core/exceptions.py` (added `CurriculumCycleDetectedError`, `HardDeleteProhibitedError`, `InvalidAyahReferenceError`, `InvalidPrerequisiteNodeError`)
- `src/noorheroes/core/i18n.py` (added 4-language translations across `en`, `hi`, `ur`, `ar`)
- `src/noorheroes/modules/learning/deps.py` (added `get_curriculum_graph_service` and `get_admin_skill_node_service`)
- `src/noorheroes/api/v1/router.py` (mounted admin learning router)
- `src/noorheroes/main.py` (added OpenAPI tags for Admin Quran Skill Tree)
- `FAST-API-INSTRUCTIONS.md` (updated Sections 5.2, 5.5, 6, 8, 9, 11, 12, 15)
- `MASTER-README.md` (added Section 11.42 and Scenario Matrix S-168 to S-191)
- `src/noorheroes/modules/learning/README.md` (added Section 2.17, Scenarios S-168 to S-188, 569 test breakdown)
- `docs/NoorHeroes_Consolidated_Execution_Blueprint.md` (updated Phase 6 overview, Item 178 row, next item pointer, and Phase 5 gate checklist)

## 10. Backend Requirements
- **Create/Update `skill_node`**: `node_type`, `related_ayah_id`, `track`, `prerequisite_node_ids` — validated via `curriculum_editor` role.
- **Cycle detection**: `CurriculumGraphService.validate_no_cycle(node_id, proposed_prerequisites)` — topological sort over the full graph including the proposed change; on cycle detection, reject the save and return the cycle path (list of node IDs forming the cycle) in the error response, not a generic failure.
- **Deactivate**: sets `is_active=false`; never a hard `DELETE` — historical `skill_node_state`/`learning_attempt` FK references remain valid.
- **Ayah immutability enforcement**: a PostgreSQL trigger (or equivalent DB-layer mechanism) on the `ayah` table that raises an exception on any `UPDATE` targeting `arabic_text_immutable` post-initial-insert — enforced at the database layer, not just role-based access control, so it cannot be bypassed by any future code path or admin role.
- **Scholar sign-off gating**: translation/tafseer/learning-metadata edits (on the existing Quran Management module, extended per N-02) require a sign-off flag before publish — this blueprint's `skill_node` linkage fields reference that existing workflow rather than reimplementing it.
- **Audit logging**: every mutating action writes an immutable audit_log row (`admin_id`, action, before/after diff, timestamp), consistent with the existing `admin` context pattern.

## 11. KMP Requirements
N/A (admin-only feature).

## 12. NextJS Requirements
Consumed by `N-01 Skill Tree / Curriculum Builder` (graph-editing UI) and `N-02 Quran Content Management Extension` (skill-node linkage fields on Quran Management).

## 13. API Contract

**`POST /v1/admin/learning/skill-nodes`** (create)
- **Auth:** `get_current_admin`, requires `curriculum_editor` role
- **Request:** `{ "node_type": "...", "related_ayah_id": "uuid", "track": "quran|arabic|tajweed", "prerequisite_node_ids": ["uuid"] }`
- **Response 201:** created `skill_node` object
- **Error Responses:** `401`, `403` (wrong role), `409` (cycle detected — includes cycle path), `422` (invalid ayah reference/track)

**`PUT /v1/admin/learning/skill-nodes/{node_id}`** (update)
- Same auth/validation; cycle-detection re-run on every update.

**`POST /v1/admin/learning/skill-nodes/{node_id}/deactivate`**
- Sets `is_active=false`; no request body required beyond the path param.

**`POST /v1/admin/content/validate-graph`** (standalone cycle-check, used by N-01's UI before final save)
- **Request:** proposed graph delta
- **Response 200/409:** `{ "valid": true }` or `{ "valid": false, "cycle_path": ["uuid", "uuid", "uuid"] }`

## 14. Database Requirements
Extends B-01's `skill_node` table (no schema change needed beyond what B-01 defined, assuming `is_active` already present). New: PostgreSQL trigger function on `ayah.arabic_text_immutable` rejecting post-seed `UPDATE`. Reuses the existing admin `audit_log` table (no new schema — confirm exact table name/shape against the `admin` context before writing to it).

## 15. Validation
- `related_ayah_id` must reference an existing ayah.
- `track` enum validated.
- `prerequisite_node_ids` must reference existing, active nodes.
- Cycle-detection is mandatory on every create/update that touches `prerequisite_node_ids`.

## 16. Authentication
Bearer JWT, `get_current_admin`.

## 17. Authorization
`curriculum_editor` role required for all mutating routes; the standalone graph-validation endpoint may be usable by any authenticated admin role (read-only check) if the NextJS UI needs to pre-validate before role-gated save — confirm against N-01's actual UX flow.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Cycle detected | `409`, cycle path returned, save rejected |
| Direct `UPDATE` attempt on `ayah.arabic_text_immutable` | Rejected at the database trigger layer, not just application validation |
| Unauthorized/forbidden request | `401`/`403` |
| Invalid ayah/prerequisite reference | `422` |
| Attempted hard-delete | No such route exists — only deactivate is exposed |

## 19. Offline First
N/A (admin backend).

## 20. Local Data
N/A (admin backend).

## 21. Localization
`node_type`/track labels are identifiers; display-string localization owned by N-01's UI layer.

## 22. RTL
N/A at API layer.

## 23. Analytics
N/A (admin audit logging, not child-behavior analytics).

## 24. Performance
Cycle detection must run efficiently even as the curriculum graph grows (topological sort is O(V+E); ensure no accidental O(V²) implementation for large node counts).

## 25. Security
Database-level immutability trigger is the primary defense for ayah-text tampering — explicitly called out as stronger than role-based access control alone, per the PRD's threat-analysis section. `curriculum_editor` role strictly enforced with no override path.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0, Pydantic v2, Alembic (for the trigger migration). No new third-party dependencies.

## 27. Testing
- Unit: cycle-detection algorithm against known cyclic/acyclic graph fixtures.
- Unit: deactivate never issues a `DELETE` statement (verify via query-log/mock assertion).
- Integration: create/update `skill_node` with valid data succeeds.
- Integration: create/update introducing a cycle is rejected with the correct cycle path.
- Integration: direct database `UPDATE` attempt on `ayah.arabic_text_immutable` is rejected by the trigger (test connects with the app's DB role and issues the UPDATE directly, bypassing the ORM, to prove the DB-layer enforcement).
- Integration: unauthorized/forbidden role rejected.
- Integration: every mutation produces a corresponding audit_log row with before/after diff.

## 28. Documentation
OpenAPI docstrings for all routes; explicit note that deactivation is the only removal mechanism and why (historical reference integrity).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Extend `SkillNodeRepository` with Write Operations**
- Task ID: B-09-T01
- Status: Completed ✅
- Files to Modify: `src/noorheroes/modules/learning/skill_tree_repository.py`.
- Implementation Details: `create()`, `update()`, `deactivate()`, `list_all()`; `delete()` unconditionally raises `HardDeleteProhibitedError`.
- Dependencies: B-01-T04.
- Definition of Done: Repository unit tests pass; confirmed no hard delete is permitted.

**Task 02 — Implement `CurriculumGraphService` (Cycle Detection)**
- Task ID: B-09-T02
- Status: Completed ✅
- Files to Create: `src/noorheroes/modules/learning/services/curriculum_graph_service.py`.
- Implementation Details: 3-color DFS cycle detection over full prerequisite graph including proposed changes; returns exact directed cycle path on failure.
- Dependencies: B-01-T04.
- Definition of Done: Unit tests (Task 06) pass against cyclic/acyclic fixtures (11 passing tests).

**Task 03 — Implement Ayah Immutability DB Trigger**
- Task ID: B-09-T03
- Status: Completed ✅
- Task Name: Write-Protect `ayah.arabic_text_immutable`
- Objective: Enforce content-integrity at the database layer, not just application code.
- Files to Create: `alembic/versions/0048_add_ayah_immutability_trigger.py`, `src/noorheroes/modules/content/quran_models.py`.
- Implementation Details: `CREATE TRIGGER` (`fn_prevent_ayah_text_mutation` / `BEFORE UPDATE OF arabic_text_immutable`) raising exception on raw SQL `UPDATE` post-seed; tested directly bypassing ORM.
- Security: This is a P0 content-integrity control per PRD FR-21.
- Dependencies: None.
- Definition of Done: Direct-SQL UPDATE test (Task 06) confirms rejection.

**Task 04 — Implement `AdminSkillNodeService`**
- Task ID: B-09-T04
- Status: Completed ✅
- Files to Create: `src/noorheroes/modules/learning/services/admin_skill_node_service.py`, `src/noorheroes/modules/learning/schemas/admin_skill_node.py`.
- Implementation Details: Orchestrates create/update/deactivate + cycle-check + atomic `AdminAuditRecord` logging with before/after diffs + track prerequisite matching + foreign Ayah validation + Redis cache purging.
- Dependencies: B-09-T01, B-09-T02.
- Definition of Done: Unit tests pass.

**Task 05 — Wire Admin Router with RBAC**
- Task ID: B-09-T05
- Status: Completed ✅
- Files to Create/Modify: `src/noorheroes/modules/learning/admin_api.py`, `src/noorheroes/api/v1/router.py`, `main.py`.
- Implementation Details: `get_current_admin` + `curriculum_editor` role check on all mutating routes; standalone `/validate-graph` route and NextJS Admin Portal alias `/admin/content/validate-graph`.
- Dependencies: B-09-T04.
- Definition of Done: Endpoints reachable, RBAC verified.

**Task 06 — Tests**
- Task ID: B-09-T06
- Status: Completed ✅
- Objective: Full coverage per §27, including direct-SQL immutability-trigger test.
- Files: `test_admin_skill_node_api.py`, `test_skill_node_repository_write.py`, `test_curriculum_graph_service.py`, `test_ayah_immutability_trigger.py`.
- Dependencies: B-09-T01–T05.
- Definition of Done: All 44 dedicated tests green in CI; 569 total learning tests passing.

**Task 07 — API Documentation**
- Task ID: B-09-T07
- Status: Completed ✅
- Dependencies: B-09-T05.
- Definition of Done: OpenAPI docs complete covering 10 status codes (200, 201, 400, 401, 403, 404, 409, 422, 429, 500), deactivate-only rationale documented across `FAST-API-INSTRUCTIONS.md`, `MASTER-README.md`, and `learning/README.md`.

## 30. Definition of Done
✅ **FULLY ACHIEVED**: Admin CRUD live with `curriculum_editor` RBAC, 3-color DFS cycle-detection returning exact cycle path on every graph mutation, sacred ayah-text immutability enforced at database trigger layer, deactivate-only removal, atomic audit logging with diffs, live Redis cache purging, fully tested (44 dedicated tests, 569 learning tests) and documented across `FAST-API-INSTRUCTIONS.md`, `MASTER-README.md`, and `learning/README.md`.

## 31. Final Verification Checklist
- [x] No hard-delete route/method exists for `skill_node` anywhere in the codebase
- [x] Cycle detection runs on every create/update touching prerequisites, returns the cycle path on rejection
- [x] Direct database `UPDATE` on `ayah.arabic_text_immutable` rejected at the trigger layer (verified via direct-SQL test bypassing the ORM)
- [x] `curriculum_editor` role strictly enforced, no bypass path
- [x] Every mutation produces an audit_log row with before/after diff
- [x] Full test suite green in CI
