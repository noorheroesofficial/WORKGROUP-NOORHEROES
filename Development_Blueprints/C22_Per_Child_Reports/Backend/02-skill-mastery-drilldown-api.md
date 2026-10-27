# Blueprint: Skill Mastery Drill-Down API

## 1. Feature Context
Platform: NoorHeroes Backend (FastAPI). Module: `src/noorheroes/modules/dashboard/`. Delivers `GET /v1/parent/reports/{child_id}/skills/{skill_id}` — the parent-facing skill detail drill-down reached from the Skill Mastery Grid.

## 2. Parent Feature
C.22 — Per-Child Reports.

## 3. Sub-feature
B-02 — Skill Mastery Drill-Down API.

## 4. Objective
Return a parent-friendly skill state (never a raw numeric score) for one skill, sourced from A.9's Mastery Engine, structurally enforcing FR-12's no-raw-score-for-parents rule via a schema that has no field capable of holding a numeric score.

## 5. Business Requirements
Source: PRD §1.7 FR-12, §1.9 Acceptance Criteria ("parent-friendly state language... rather than a raw numeric mastery score"), §1.10 Edge Case #5, §3.4.
- Response contains `state` (Locked/Ready/Learning/Practicing/Mastered/Needs Refresh) and a pre-mapped `state_label` only.
- A skill/domain the child hasn't engaged with returns an explicit "not started" state, not an empty/confusing detail view (Edge Case 5).
- Consistent with A.9 FR-3's child-facing no-raw-score rule, extended here to the parent-facing surface per FR-7's "never judgmental grades" framing.

## 6. Existing Architecture
Per A.9 (Skill Tree & Mastery Engine) blueprints: the six-state mastery model (`Locked`/`Ready`/`Learning`/`Practicing`/`Mastered`/`Needs Refresh`) and its structural no-raw-score guarantee already exist for the child-facing surface. This endpoint is a new parent-facing read path over the same underlying mastery state, not a new mastery computation. `skill_report_snapshot` (introduced by B-03/B-01 dependency chain of this feature, see §4.5 of the PRD) stores point-in-time state/state_label pairs for report-rendering consistency.

## 7. Existing Code to Reuse
- `require_parent_session_only` (C.20 B-01).
- `ChildRepository.get_child_by_id_and_family()` for family-ownership validation.
- A.9's mastery state → state_label mapping table/function — reuse the existing mapping, do not redefine a second parent-facing mapping that could drift from the child-facing one.
- A.9's `learning` bounded context (`src/noorheroes/modules/learning/`) owns the `skill_node_state` table and its query surface, established by A.9 B-05 (Skill State Query API) — the six-state (`Locked`/`Ready`/`Learning`/`Practicing`/`Mastered`/`Needs Refresh`) enum and its per-skill current-state lookup live there. This endpoint should query `skill_node_state` via that existing service (or the `skill_report_snapshot` point-in-time table this feature introduces, populated from it) rather than a generically-named `LearningService`.

## 8. Files to Create
- `tests/modules/dashboard/test_skill_mastery_drilldown_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/dashboard/schemas.py` — add `SkillDetailResponse`
- `src/noorheroes/modules/dashboard/service.py` — add `get_skill_detail(parent_ctx, child_id, skill_id)`
- `src/noorheroes/modules/dashboard/api.py` — add `GET /v1/parent/reports/{child_id}/skills/{skill_id}`
- `src/noorheroes/modules/dashboard/models.py` — add `SkillReportSnapshot` SQLAlchemy model (if not already introduced by a prior sub-feature; coordinate with B-01)

## 10. Backend Requirements
- Route: `GET /v1/parent/reports/{child_id}/skills/{skill_id}`, gated by `require_parent_session_only` + family-ownership.
- `DashboardAggregationService.get_skill_detail()`:
  1. Validate `child_id` belongs to `parent_ctx.family_id`.
  2. Look up the skill's current state via `LearningService`/A.9 mastery lookup, or the latest `skill_report_snapshot` row for point-in-time consistency with the broader report view.
  3. If the skill has never been engaged (no snapshot/state record exists), return `state: "not_started"` with a neutral `state_label` — not a 404 or empty body.
  4. Map `state` → `state_label` using A.9's existing state-to-copy mapping.
  5. Return `last_practiced_at` (nullable for not-started).
- `skill_report_snapshot` table: `snapshot_id`, `child_id` FK, `skill_id` FK, `state`, `state_label`, `last_practiced_at`, `snapshot_at`; index `(child_id, skill_id, snapshot_at DESC)`; **no raw numeric score column** (PRD §4.2).

## 11. KMP Requirements
Consumed by K-02 (`SkillDetailScreen`). DTO must declare no numeric score/confidence field — reflection test on the client mirrors this endpoint's schema test.

## 12. NextJS Requirements
N/A.

## 13. API Contract
- **HTTP Method:** GET
- **Endpoint:** `/v1/parent/reports/{child_id}/skills/{skill_id}`
- **Auth:** Bearer, parent session only
- **Request:** path `child_id: str`, `skill_id: str`
- **Response 200:**
```json
{
  "skill_id": "string",
  "state": "practicing",
  "state_label": "Getting more confident",
  "last_practiced_at": "ISO-8601 | null"
}
```
- **Authentication:** Bearer parent session
- **Authorization:** Family-ownership on `child_id`
- **Validation:** `skill_id` must reference a valid skill in the platform's skill taxonomy (A.9)
- **Error Responses:** `403`/`404` `ChildScopeViolationError`, `404` unknown `skill_id`, `401` invalid session

## 14. Database Requirements
`skill_report_snapshot` table per §4.2 of the PRD ER diagram: FK `child_id`, `skill_id`; no raw numeric score column; index `(child_id, skill_id, snapshot_at DESC)`. Append-only, no soft-delete (point-in-time snapshots).

## 15. Validation
- `child_id` required, family-owned.
- `skill_id` must exist in the skill taxonomy; unknown `skill_id` → `404`, not a silent "not_started".

## 16. Authentication
Bearer parent session.

## 17. Authorization
Family-ownership check, additive to B-01's gate.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Cross-family `child_id` | `403`/`404` `ChildScopeViolationError` |
| Unknown `skill_id` | `404` |
| Skill never engaged | `200` with `state: "not_started"`, not an error (Edge Case #5) |
| Mastery service unavailable | `503` with graceful client-facing message |

## 19. Offline First
N/A server-side; K-02 caches drill-down responses per its offline-cache module.

## 20. Local Data
N/A (backend).

## 21. Localization
`state_label` sourced from the localization service's locale-resolved copy table, keyed by `state`, not hardcoded per-request string concatenation.

## 22. RTL
N/A (backend).

## 23. Analytics
`skill_detail_drilldown_viewed` fired client-side (K-02).

## 24. Performance
p95 within the parent Report load NFR (< 700ms); single indexed lookup on `skill_report_snapshot` or direct mastery-service call, no N+1 across skills (this endpoint serves one skill at a time by design).

## 25. Security
No numeric score/confidence field anywhere in the response model — enforced by schema-introspection test, the primary security/trust control of this endpoint per FR-12.

## 26. Library Requirements
No new dependencies.

## 27. Testing
1. Unit test: each of the six mastery states returns correct `state_label`.
2. Unit test: unengaged skill returns `not_started` state, not an error.
3. Unit test: unknown `skill_id` returns `404`.
4. Unit test: cross-family `child_id` rejected.
5. Schema-introspection test: no numeric score/confidence field exists anywhere in `SkillDetailResponse`.
6. Integration test: full drill-down request through the gate.

## 28. Documentation
OpenAPI docstring explicitly noting the structural no-raw-score guarantee, referencing A.9's established pattern.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define SkillDetailResponse Schema and SkillReportSnapshot Model**
- Task ID: B02-T01
- Objective: Create the Pydantic response schema and, if not already present, the `SkillReportSnapshot` SQLAlchemy model + Alembic migration.
- Why This Is Required: Structural enforcement of FR-12's no-raw-score rule requires the schema itself to have no such field, not just an unused one.
- Existing Architecture to Follow: `NoorHeroesBaseModel`; A.9's existing mastery-state enum.
- Existing Files to Reuse: A.9 state-to-label mapping.
- Files to Create: none (schema addition).
- Files to Modify: `schemas.py`, `models.py`, new Alembic migration.
- Implementation Details: `SkillDetailResponse(skill_id, state, state_label, last_practiced_at)`.
- Business Rules: FR-12.
- Validation: Field types match §13.
- Error Handling: N/A.
- Security: No numeric field declared.
- Performance: Indexed FK columns.
- Localization: `state_label` pre-localized.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered by Task 04's schema-introspection test.
- Documentation: Docstring citing FR-12.
- Dependencies: A.9's mastery-state enum must exist.
- Do Not Change: A.9's child-facing mastery schemas.
- Expected Result: Schema and model importable, migration applies cleanly.
- Definition of Done: No numeric field present, confirmed by manual review before Task 04's automated test.

**Task 02 — Implement get_skill_detail Service Method**
- Task ID: B02-T02
- Objective: Resolve current state, mapping to label, handling the not-started case.
- Why This Is Required: Core business logic.
- Existing Architecture to Follow: `BaseService` pattern.
- Existing Files to Reuse: `LearningService` mastery lookup, A.9 state-label mapping.
- Files to Create: none.
- Files to Modify: `service.py`.
- Implementation Details: Per §10 steps 1–5.
- Business Rules: FR-12, Edge Case #5.
- Validation: Family-ownership first, skill-existence second.
- Error Handling: Per §18.
- Security: N/A beyond schema guarantee.
- Performance: Single lookup, no fan-out needed.
- Localization: Reuse existing mapping table.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: Docstring.
- Dependencies: Task 01.
- Do Not Change: A.9's internal mastery computation logic.
- Expected Result: Correct state/label/not-started handling.
- Definition of Done: All six states plus not-started verified.

**Task 03 — Implement Route**
- Task ID: B02-T03
- Objective: Expose `GET /v1/parent/reports/{child_id}/skills/{skill_id}`.
- Why This Is Required: Public contract delivery.
- Existing Architecture to Follow: Router `Depends()` pattern.
- Existing Files to Reuse: `api.py`, `deps.py`.
- Files to Create: none.
- Files to Modify: `api.py`.
- Implementation Details: Path params `child_id`, `skill_id`; `Depends(require_parent_session_only)`.
- Business Rules: FR-12.
- Validation: Per §15.
- Error Handling: Per §18.
- Security: Inherits gate.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: OpenAPI summary.
- Dependencies: Tasks 01–02.
- Do Not Change: N/A.
- Expected Result: Endpoint live.
- Definition of Done: Matches §13 exactly.

**Task 04 — Write Test Suite Including Schema-Introspection Test**
- Task ID: B02-T04
- Objective: Cover §27, with the schema-introspection test treated as the highest-priority guarantee for this endpoint.
- Why This Is Required: FR-12 is a hard, zero-exception rule.
- Existing Architecture to Follow: pytest + reflection-based field scanning (mirrors A.9's existing pattern).
- Existing Files to Reuse: A.9's schema-introspection test utility if one exists.
- Files to Create: `tests/modules/dashboard/test_skill_mastery_drilldown_api.py`.
- Files to Modify: none.
- Implementation Details: 6 test cases per §27, including a reflection test asserting no field matches `/score|confidence|percent|numeric/i` on `SkillDetailResponse`.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert exact error responses.
- Security: The reflection test is security/trust-critical.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test docstrings.
- Dependencies: Tasks 01–03.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 green, schema-introspection test is CI-blocking.

## 30. Definition of Done
`GET /v1/parent/reports/{child_id}/skills/{skill_id}` live, gated, returns parent-friendly state/label with no numeric score field structurally possible, not-started state handled, all tests green.

## 31. Final Verification Checklist
- [ ] No numeric score/confidence field anywhere in `SkillDetailResponse` (schema-introspection test, CI-blocking)
- [ ] All six mastery states plus not-started verified
- [ ] Family-ownership check verified
- [ ] Unknown `skill_id` returns `404`
- [ ] `state_label` sourced from locale-resolved copy, not hardcoded
- [ ] OpenAPI docs reflect the structural no-raw-score guarantee
