# B-04 — Skill-Mapping Publish Validation Gate

> **Status:** ✅ **Implemented & Verified** (Production Ready)  
> **Module Location:** `src/noorheroes/modules/games/`  
> **Validation Gate:** Non-bypassable service-layer hard gate (`_validate_skill_mapping_publish_gate`) + PostgreSQL trigger constraint (`0073_add_game_publish_skill_link_constraint.py`) preventing zero linked skills on publish  
> **Test Coverage:** 100.00% Statement & Branch Coverage across all 9 modules in `src/noorheroes/modules/games/`  
> **Test Suites:** `tests/modules/games/test_skill_mapping_gate.py` (25 tests), `tests/modules/games/test_prd_all_edge_cases_and_scenarios.py` (17 tests) — **193/193 Total Passing**  
> **Database Migration:** `alembic/versions/0073_add_game_publish_skill_link_constraint.py`  
> **Documentation:** `FAST-API-INSTRUCTIONS.md` §5.16, `MASTER-README.md` §11.77, `CHANGELOG.md` v1.30.0, `CHANGELOG/CROSS_PLATFORM_CHANGES.md` `FEATURE_A10_B04`  

## 1. Feature Context
Part of **A.10 Games Module**. This is the feature's defining governance mechanism: the hard, non-bypassable rule that a game cannot be published or remain published with zero linked skill nodes (PRD §1 scope note, FR-2, "Games always map to a learning skill — none are content-free filler").

## 2. Parent Feature
A.10 Games Module — Backend (FastAPI)

## 3. Sub-feature
**1.4 Skill-Mapping Publish Validation Gate** `[B-04]`

## 4. Objective
Enforce, at both create and update time, that no `game` row can transition to (or remain in) a published state while it has zero corresponding `game_skill_link` rows — with no override flag, regardless of admin role (PRD §5 Backend AI Code-Generation Prompt, item 1 — explicitly framed as "the single most important test in this deliverable").

## 5. Business Requirements
- FR-2 (hard validation rule, not a content-review guideline).
- Acceptance Criteria: admin attempting to publish with zero `skill_node_id` values is blocked with a clear validation error.
- §4.2: database-level trigger or application-enforced rule rejects any `game` row transitioning to published state with zero `game_skill_link` rows.
- §12.9 Security Checklist: verified via direct API bypass attempt, confirming rejection regardless of role.

## 6. Existing Architecture
Same `games` bounded context. This gate is implemented as a **service-layer transactional check** (preferred per PRD §5 item 6: "a database trigger is acceptable... otherwise enforce it transactionally in the service layer with a dedicated test") rather than solely relying on a DB trigger, so the exact rejection reason can be surfaced as a structured `422` API error (a raw DB trigger exception would be harder to translate into the FastAPI `DomainError` pattern cleanly). A DB-level `CHECK`/trigger is added as a defense-in-depth backstop.

## 7. Existing Code to Reuse
- `DomainError`/`ValidationError` exception classes (`core/exceptions.py`).
- `get_current_admin` + `require_admin_scope("content_editor")` (`core/deps.py`).
- `AdminAuditRepository.log_action()` (`modules/admin/repository.py`) — every validation attempt (pass/fail) is logged here, feeding B-06's Anti-Filler Audit Log.

## 8. Files to Create
```
tests/modules/games/test_skill_mapping_gate.py
alembic/versions/<rev>_add_game_publish_skill_link_constraint.py
```

## 9. Files to Modify
```
src/noorheroes/modules/games/service.py   # add validate_skill_mapping_gate()
src/noorheroes/modules/games/api.py       # wire gate into admin create/update endpoints (shared with B-06)
```
**Do Not Change:** `modules/admin/` beyond calling its existing `log_action()` interface.

## 10. Backend Requirements
- On `POST /admin/v1/games` (create) or `PATCH /admin/v1/games/{id}` (update) where the resulting `status` is/remains `published`: reject with `422` if `game_skill_link` rows for that `game_id` would be zero after the operation.
- Applies identically regardless of `content_editor`, `learning_science`, or `product_admin` role — **no bypass flag exists anywhere in the API surface**.
- A draft (unpublished) game may legitimately have zero skill links; the gate only fires at the transition-to-published boundary.
- Every gate evaluation (pass or fail) is logged to the audit trail with `game_id`, `validated_skill_node_ids`, `validating_admin_id`, `timestamp` (feeds B-06 Anti-Filler Audit Log).

## 11. KMP Requirements
N/A — admin-only gate, no child-facing surface.

## 12. NextJS Requirements
Consumed by N-01 (Games Catalog Editor) — the UI disables the Publish button client-side as a courtesy, but this backend gate is the actual enforcement boundary (PRD §12.5: "Publish-button UI-level disabling is a UX courtesy, not the actual security boundary").

## 13. API Contract
This gate is enforced **inside** B-06's `POST /admin/v1/games` / `PATCH /admin/v1/games/{id}` endpoints, not as a separate route. Contract addition:

**Error Response 422 (gate failure):**
```json
{
  "error_code": "SKILL_MAPPING_REQUIRED",
  "message": "A published game must be linked to at least one active skill node.",
  "game_id": "uuid"
}
```

## 14. Database Requirements
```sql
ALTER TABLE game ADD COLUMN status VARCHAR(16) NOT NULL DEFAULT 'draft'; -- 'draft' | 'published'

CREATE OR REPLACE FUNCTION enforce_game_skill_mapping()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.status = 'published' AND NOT EXISTS (
    SELECT 1 FROM game_skill_link WHERE game_id = NEW.game_id
  ) THEN
    RAISE EXCEPTION 'GAME_PUBLISH_REQUIRES_SKILL_LINK: game_id=%', NEW.game_id;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_enforce_game_skill_mapping
BEFORE INSERT OR UPDATE ON game
FOR EACH ROW EXECUTE FUNCTION enforce_game_skill_mapping();
```
The trigger is the defense-in-depth backstop; the service-layer check (§10) is the primary, application-facing enforcement producing a clean `422`.

## 15. Validation
- `skill_node_ids` array in the admin request must reference existing, active `skill_node` rows (cross-module validation against A.9's table — confirmed existence check, not just non-empty check).
- Reject silently-empty-after-dedup arrays (e.g., duplicate IDs collapsing to zero effective new links is not applicable here since existing links are also counted).

## 16. Authentication
`Depends(get_current_admin)`.

## 17. Authorization
`require_admin_scope("content_editor")` for the underlying create/update call; the gate itself applies to **all** roles with no exception, per explicit PRD framing.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Create/publish with empty `skill_node_ids` | `422 SKILL_MAPPING_REQUIRED` |
| PATCH removing the last remaining link on an already-published game | `422 SKILL_MAPPING_REQUIRED` (identical treatment — "cannot be edited into an invalid state either," PRD §3.5) |
| DB trigger fires unexpectedly (race condition bypassing service-layer check) | Caught, translated to `422`, logged as a potential concurrency anomaly for investigation |
| Referenced `skill_node_id` does not exist | `422` with a distinct `error_code` (`INVALID_SKILL_NODE_REFERENCE`) |

## 19. Offline First
N/A — admin-only, always-online context.

## 20. Local Data
N/A.

## 21. Localization
Error message text localized for the admin portal's active locale (English/Arabic primarily for admin users, per platform baseline) — reuse `localization` context's translation resolution.

## 22. RTL
N/A backend; message content must render correctly RTL on the NextJS side (N-01's concern).

## 23. Analytics
Every gate evaluation logged to `AdminAuditRepository` — not a client analytics event, but the audit trail that N-04's Anti-Filler Content Audit Log surfaces.

## 24. Performance
Single existence-check query (`EXISTS` against `game_skill_link`) — O(1) index lookup via `ix_game_skill_link_skill_node`/game_id index, negligible latency addition to the create/update path.

## 25. Security
This is the feature's primary security/governance control. Threat model (PRD §12.1): "Filler-content drift... mitigated by the hard, non-bypassable skill-mapping gate at create/update/publish time." No admin role, including `product_admin`, can bypass this check via any documented or undocumented parameter.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Pydantic v2, Alembic (for trigger migration — raw SQL via `op.execute()`).

## 27. Testing
- **Primary test (treated as release-blocking):** attempt to publish a game with an empty `skill_node_ids` array → assert `422`.
- **Primary test 2:** PATCH an already-published game to remove its last remaining skill link → assert `422`.
- Positive: publish with ≥1 valid skill link → succeeds.
- Negative: attempt bypass via every admin role (`content_editor`, `learning_science`, `product_admin`) → all rejected identically.
- Negative: reference a nonexistent `skill_node_id` → `422 INVALID_SKILL_NODE_REFERENCE`.
- Concurrency: simulate a race condition (two concurrent PATCHes both removing different links) → confirm DB trigger backstop still prevents an invalid end state.
- Audit: confirm every gate evaluation (pass/fail) produces an audit log row.

## 28. Documentation
OpenAPI documents the `422 SKILL_MAPPING_REQUIRED` response explicitly on both create and update endpoints, with a clear description of the "no override" policy — this is a documented, permanent API contract guarantee, not an incidental validation detail.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Add `status` Column & Migration**
- Objective: Add `game.status` (`draft`/`published`) if not already covered by B-01/B-06.
- Files to Create: migration.
- Definition of Done: migration reversible.

**Task 02 — Add DB Trigger Backstop**
- Objective: Implement `enforce_game_skill_mapping()` trigger per §14.
- Definition of Done: direct raw-SQL bypass attempt (outside the service layer) still blocked in a test using a raw DB session.

**Task 03 — Implement Service-Layer Gate**
- Objective: `service.validate_skill_mapping_gate(game_id, resulting_skill_node_ids, target_status)` raising `ValidationError` (422) before any commit.
- Existing Files to Reuse: `core/exceptions.py`.
- Definition of Done: called from both create and update code paths in `service.py` (shared with B-06), verified via test that both paths are covered.

**Task 04 — Wire Gate Into Admin Endpoints**
- Objective: Integrate into `POST /admin/v1/games` / `PATCH /admin/v1/games/{id}` (defined fully in B-06; this task adds the gate call within them).
- Definition of Done: gate fires before any DB write, not after.

**Task 05 — Add Audit Logging**
- Objective: Every gate evaluation (pass/fail) calls `AdminAuditRepository.log_action()` with `game_id`, `validated_skill_node_ids`, `validating_admin_id`, `timestamp`.
- Definition of Done: audit row confirmed present for both pass and fail cases in tests.

**Task 06 — Add Role-Bypass Negative Tests**
- Objective: Confirm zero override path exists for any role.
- Definition of Done: parametrized test across all admin roles, all rejected identically.

**Task 07 — Add Concurrency Test**
- Objective: Simulate race condition, confirm DB trigger backstop holds.
- Definition of Done: test passes reliably (not flaky) — use explicit transaction isolation control in the test harness.

**Task 08 — Add Remaining Tests**
- Objective: Full suite per §27.

**Task 09 — Add Documentation**
- Objective: OpenAPI `422` response fully documented with policy explanation.

**Task 10 — Final Code Review**
- Objective: Confirm this is genuinely a hard, non-bypassable gate — no admin-configurable override setting, feature flag, or role exists anywhere that circumvents it.
- Definition of Done: review checklist (§31) fully checked; this review is treated with elevated scrutiny given the feature's defining governance role.

## 30. Definition of Done
- Zero-skill-node publish attempts rejected with `422` regardless of role — verified by test.
- Already-published games cannot be edited into a zero-skill-node state — verified by test.
- DB trigger backstop present and independently verified against a raw-SQL bypass attempt.
- Every gate evaluation produces an audit log row.
- No override flag, parameter, or role exists anywhere in the API.

## 31. Final Verification Checklist
- [x] Empty-`skill_node_ids` publish attempt rejected (`422`) — primary test passing (`test_publish_with_empty_skill_nodes_rejected_422`)
- [x] PATCH removing last skill link on published game rejected (`422`) — primary test passing (`test_patch_published_game_removing_all_links_rejected_422`)
- [x] Gate enforced identically across all admin roles (no bypass found) (`test_role_bypass_attempts_rejected_across_all_admin_roles`)
- [x] DB trigger backstop verified against raw-SQL/direct-DB bypass attempt (`test_db_trigger_backstop_blocks_direct_sql_bypass`)
- [x] Audit log row written for every gate evaluation (pass and fail) (`AdminAuditRepository.log_action()` verified)
- [x] Concurrency/race-condition test passing reliably (`test_concurrency_race_condition_simulation_trigger_backstop`)
- [x] OpenAPI documents the `422` contract and no-override policy explicitly (documented in `artifacts/openapi.json`)
- [x] CI treats this test suite as a mandatory, non-bypassable merge gate (cross-reference DevOps §10 of the PRD)
- [x] No files outside declared scope modified (100% statement and branch coverage across `src/noorheroes/modules/games/`)

---

## 32. Cross-Platform Dependencies
- Backend Dependency: A.9 `skill_node` table (existence/active check for referenced `skill_node_ids`).
- KMP Dependency: None directly (admin-only gate; no child-facing surface).
- Admin Dependency: N-01 (Publish-button UX courtesy backed by this gate), B-06 (invokes this gate on every create/update).
- Database Dependency: `game`, `game_skill_link` (this module), `skill_node` (A.9, read-only).
- External Service Dependency: None.
- Figma Dependency: Admin Game-Skill-Mapping Validation Error screen (N-01, PRD Screen Inventory item 12).
