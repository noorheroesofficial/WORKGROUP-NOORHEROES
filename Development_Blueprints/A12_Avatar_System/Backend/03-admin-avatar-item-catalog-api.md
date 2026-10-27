# B-03 — Admin Avatar Item Catalog API

## 1. Feature Context
NoorHeroes Backend (FastAPI). Part of Feature A.12 — Avatar System. Admin-only CRUD for the `avatar_items` catalog (outfits/glow states/accessories), including the validated-schema `unlock_rule` write path that B-01/B-02 depend on for correct read-resolution and event-matching.

## 2. Parent Feature
A.12 Avatar System — Backend (FastAPI)

## 3. Sub-feature
B-03 Admin Avatar Item Catalog API

## 4. Objective
Implement admin CRUD endpoints for `avatar_items` with a validated `unlock_rule` schema that rejects any rule not referencing an existing badge/level/habit-milestone type, and a "Delete" action that retires (never hard-deletes) the item — backing FR-4, FR-10, FR-12, and the PRD's Backend AI Code-Generation Prompt items 3 and 5.

## 5. Business Requirements
- Every `avatar_item`'s `unlock_rule` must map to an existing badge, level threshold, or habit milestone type — admin tooling must reject any arbitrary or opaque unlock condition with no underlying verifiable criteria (FR-4).
- "Delete" is relabeled "Retire" at the API-semantics level: it sets `is_retired=true` only; it never cascade-deletes or otherwise affects existing `child_inventory` rows referencing the item (FR-10).
- Updating an existing item's `unlock_rule` (e.g., changing a streak-length requirement) is non-retroactive — children who already unlocked it under the old rule keep it; the new rule applies only to children who haven't yet unlocked it (Edge Case 11).
- All avatar item assets must pass the modesty/appropriateness review pipeline before becoming purchasable/unlockable by children (FR-12) — this sub-feature creates items in a pending-review state; B-05 owns the approval gate.
- Ownership distribution (read-only aggregate) is a separate concern owned by B-06, not duplicated here.

## 6. Existing Architecture
Extends the `avatars` bounded context established in B-01. Follows the existing Admin route/RBAC pattern used by `AdminRouter`/`ContentRouter` (`require_admin_scope("content:write")`-style dependency, per `FAST-API-INSTRUCTIONS.md` §5.2/§10) and the existing `AdminAuditRepository.log_action()` pattern for immutable audit logging on every mutating action (`FAST-API-INSTRUCTIONS.md` §5.2). The `unlock_rule` validated-schema requirement follows the same "reject non-existent references, don't trust free-form input" principle already established by A.7 B-09's admin habit-type/reward-rule linkage validation.

## 7. Existing Code to Reuse
- `AvatarItem` model, `AvatarRepository` base patterns (B-01)
- `UnlockRuleResolver`'s rule-shape schema (B-01) — the write-path validator in this sub-feature must validate against the identical structured shape the resolver expects to read
- `get_current_admin`/`require_admin_scope()` (`core/deps.py`)
- `AdminAuditRepository.log_action()` (`modules/admin/repository.py`)
- `ContentRepository`'s CRUD-with-pagination pattern (`modules/content/repository.py`) as the reference for list/filter/sort

## 8. Files to Create
- `src/noorheroes/modules/avatars/admin_schemas.py` (`AvatarItemCreateRequest`, `AvatarItemUpdateRequest`, `AvatarItemAdminResponse`, `UnlockRuleSchema` — a discriminated union of `BadgeUnlockRule` | `LevelUnlockRule` | `HabitMilestoneUnlockRule`)
- `src/noorheroes/modules/avatars/unlock_rule_validator.py` (`UnlockRuleValidator.validate(rule, db)` — raises `ValidationError` on non-existent reference)
- `src/noorheroes/modules/avatars/admin_api.py` (`AvatarAdminRouter`)
- `tests/modules/avatars/test_admin_avatar_item_catalog.py`
- `tests/modules/avatars/test_unlock_rule_validation.py`
- `tests/modules/avatars/test_retire_not_delete.py`

## 9. Files to Modify
- `src/noorheroes/modules/avatars/repository.py` — add `create_item()`, `update_item()`, `retire_item()`, `list_items(filters, pagination)`, `get_item_by_id()`
- `main.py` — register `AvatarAdminRouter`

## 10. Backend Requirements
- `POST /v1/admin/avatar-items` and `PATCH /v1/admin/avatar-items/{itemId}` both route through `UnlockRuleValidator.validate()` before persisting — reject with a clear `422`-class validation error if `unlock_rule.badge_id` doesn't exist in `rewards`/badges data, if `unlock_rule.level_threshold` doesn't reference an existing achievement level, or if `unlock_rule.habit_milestone_type` isn't a recognized type from `habits`' milestone-type registry (A.7).
- `unlock_rule` is stored as JSONB but is **never** accepted as free-form JSON from the client — the request schema is a discriminated union (`UnlockRuleSchema`) with exactly three mutually-exclusive shapes, matching the structured builder N-02 exposes.
- `DELETE /v1/admin/avatar-items/{itemId}` (semantically "Retire") sets `is_retired=true` only; does not touch `child_inventory`.
- `unlock_rule` updates on an existing item never retroactively affect children with an existing `child_inventory` row for that item (Edge Case 11) — this is inherently satisfied by the fact that ownership grants are a separate, already-committed table, but must be verified by a regression test, not assumed.
- Every mutating action writes an immutable `AdminAuditLog` row via `AdminAuditRepository.log_action()`.
- List endpoint supports filtering by `slot`/`is_retired`, pagination, and sort by `name`/`created_at`.

## 11. KMP Requirements
Not applicable — this is an admin-only API surface.

## 12. NextJS Requirements
Not applicable directly; consumed by N-02's Item Catalog Editor & Unlock Rule Builder.

## 13. API Contract

**Required API 1**
- **HTTP Method:** POST
- **Endpoint:** `/v1/admin/avatar-items`
- **Request:** `{ "name": "...", "slot": "outfit", "asset_key": "...", "icon": "...", "unlock_rule": { "type": "badge", "badge_id": "uuid" } }`
- **Response 201:** `AvatarItemAdminResponse`
- **Authentication:** Bearer, admin session (`get_current_admin`)
- **Authorization:** `content_editor` scope
- **Validation:** `unlock_rule` validated per §10; `slot` enum-checked
- **Error Responses:** `401`; `403`; `422 INVALID_UNLOCK_RULE_REFERENCE` (non-existent badge/level/milestone); `409` duplicate where applicable

**Required API 2**
- **HTTP Method:** PATCH
- **Endpoint:** `/v1/admin/avatar-items/{itemId}`
- **Request:** partial `AvatarItemUpdateRequest`
- **Response 200:** `AvatarItemAdminResponse`
- **Authentication/Authorization:** same as above
- **Error Responses:** `401`; `403`; `404`; `422 INVALID_UNLOCK_RULE_REFERENCE`

**Required API 3**
- **HTTP Method:** GET
- **Endpoint:** `/v1/admin/avatar-items` (list, paginated, filterable) and `/v1/admin/avatar-items/{itemId}` (single)
- **Authentication/Authorization:** same as above (read scope, may be broader than write scope per organizational RBAC convention)

**Required API 4**
- **HTTP Method:** DELETE
- **Endpoint:** `/v1/admin/avatar-items/{itemId}`
- **Response 200:** `{ "is_retired": true }`
- **Authentication/Authorization:** `content_editor` scope
- **Business Logic:** sets `is_retired=true` only; never deletes the row or cascades to `child_inventory`

## 14. Database Requirements
Extends `avatar_items` from B-01 — no new tables. Adds no new columns beyond what B-01 already defined (`is_retired` already present). Reads `badges`/achievement-level tables (owned by the not-yet-blueprinted A.11 Rewards System) and `habits` milestone-type registry (A.7) for `unlock_rule` reference validation — flagged as a cross-context dependency to reconcile against A.11's actual schema once that blueprint is generated; in the interim, validation queries against the tables as specified in A.11 PRD §4/A.7 PRD §4.

## 15. Validation
- `UnlockRuleValidator.validate()` is the single source of truth for rule-reference validity; both create and update paths must call it — no bypass path.
- Reject `unlock_rule` payloads that don't match exactly one of the three discriminated-union shapes.
- Reject duplicate/conflicting item definitions where the platform's content-governance conventions require it (mirroring `ContentRepository`'s existing duplicate-handling convention).

## 16. Authentication
Bearer JWT, admin session via `get_current_admin`.

## 17. Authorization
`content_editor` role required for all mutating actions; read access may follow a broader admin-role convention per existing `AdminRouter` precedent.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| `unlock_rule` references a non-existent `badge_id` | `422 INVALID_UNLOCK_RULE_REFERENCE`, clear field-level error |
| `unlock_rule` references an unrecognized habit-milestone type | `422 INVALID_UNLOCK_RULE_REFERENCE` |
| Retire action attempted on an already-retired item | Idempotent success (`is_retired` already `true`), not an error |
| Update changes `unlock_rule` after some children already unlocked under the old rule | Update succeeds; existing owners' `child_inventory` rows are untouched (verified by regression test, Edge Case 11) |
| Unauthorized/forbidden request | `401`/`403` |
| Database failure | `500`/`503`, no partial write |

## 19. Offline First / 20. Local Data
N/A (backend, admin-only, online-by-design surface).

## 21. Localization
`name` stored as translation key per B-01's convention, not a raw hardcoded string, consistent with the platform's multi-locale requirement even for admin-authored content that ultimately renders to children in EN/HI/AR/UR.

## 22. RTL
N/A at the API layer.

## 23. Analytics
Not applicable (internal admin tooling); the `AdminAuditLog` is the operational record of truth for catalog changes.

## 24. Performance
Standard paginated list query, indexed on `(slot)`/`(is_retired)` from B-01; no additional performance-critical path here (low-traffic admin surface).

## 25. Security
`UnlockRuleValidator` is the primary integrity control preventing opaque/arbitrary unlock conditions (§12.1 Threat Analysis, PRD). RBAC (`content_editor` scope) is the primary access control. Immutable audit logging on every mutation supports dispute resolution and content-governance review.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 (async), Pydantic v2 (discriminated unions via `Field(discriminator=...)`), Alembic (none new — reuses B-01's tables).

## 27. Testing
- Unit: `UnlockRuleValidator.validate()` for all three valid rule types and their respective invalid/non-existent-reference cases.
- Integration (P0): attempt to create an `avatar_item` with a `unlock_rule` referencing a fake/non-existent `badge_id` → assert rejection (PRD Backend AI Code-Generation Prompt item 3).
- Integration (P0): retire an item a fixture child already owns → confirm that child's `GET /v1/children/{id}/inventory` (B-01) still lists it as owned/equippable (PRD Backend AI Code-Generation Prompt item 5).
- Integration: update `unlock_rule` after some children already unlocked → confirm existing owners unaffected, new rule applies going forward only.
- Integration: full CRUD + pagination/filtering/sorting.

## 28. Documentation
OpenAPI documentation for all four endpoints, including the `UnlockRuleSchema` discriminated-union shape rendered clearly for admin frontend consumption (N-02); update the `avatars` context entry in `FAST-API-INSTRUCTIONS.md`.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define `UnlockRuleSchema` Discriminated Union**
- Task ID: B-03-T01
- Objective: Pydantic v2 discriminated union for `BadgeUnlockRule`/`LevelUnlockRule`/`HabitMilestoneUnlockRule`.
- Existing Architecture to Follow: shared shape with `UnlockRuleResolver` (B-01) — both must agree on the exact JSON structure.
- Files to Create: part of `src/noorheroes/modules/avatars/admin_schemas.py`
- Tests: schema validation unit tests for all three shapes and malformed-shape rejection.
- Definition of Done: schema round-trips and rejects non-matching shapes with clear errors.

**Task 02 — Implement `UnlockRuleValidator`**
- Task ID: B-03-T02
- Objective: `validate(rule, db)` cross-context existence check against badges/achievement-levels/habit-milestone-types.
- Files to Create: `src/noorheroes/modules/avatars/unlock_rule_validator.py`
- Implementation Details: three lookup branches per rule type; raise `ValidationError` with a field-specific message on miss.
- Tests (P0): fake-`badge_id` rejection test; fake-milestone-type rejection test.
- Definition of Done: validator correctly accepts all valid references and rejects all fabricated ones.

**Task 03 — Implement Repository CRUD Methods**
- Task ID: B-03-T03
- Objective: `create_item()`, `update_item()`, `retire_item()`, `list_items()`, `get_item_by_id()`.
- Files to Modify: `src/noorheroes/modules/avatars/repository.py`
- Implementation Details: `retire_item()` sets `is_retired=true` only, single-column update, no cascading query.
- Tests: repository-level tests including the retire-not-delete guarantee.
- Definition of Done: all methods correct against fixture data.

**Task 04 — Implement Admin Endpoints**
- Task ID: B-03-T04
- Objective: Wire `AvatarAdminRouter` with RBAC and audit logging.
- Files to Create/Modify: `src/noorheroes/modules/avatars/admin_api.py`; modify `main.py`.
- Authentication/Authorization: `Depends(get_current_admin)` + `require_admin_scope("content:write")` on mutating routes.
- Implementation Details: every mutating route calls `AdminAuditRepository.log_action()` after a successful operation.
- Tests: integration tests for all four endpoints, RBAC-rejection cases.
- Definition of Done: endpoints live, documented, audit-logged.

**Task 05 — Add Retire-Not-Delete Regression Test (P0)**
- Task ID: B-03-T05
- Files to Create: `tests/modules/avatars/test_retire_not_delete.py`
- Implementation Details: retire an item owned by a fixture child; assert B-01's inventory endpoint still returns it as owned/equippable.
- Definition of Done: test passes, registered as a standing regression test per PRD §13.6.

**Task 06 — Add Unlock-Rule Validation Test Suite (P0)**
- Task ID: B-03-T06
- Files to Create: `tests/modules/avatars/test_unlock_rule_validation.py`
- Definition of Done: fake-reference rejection tests pass, CI-blocking.

**Task 07 — Add Full Admin CRUD Test Suite & Documentation**
- Task ID: B-03-T07
- Files to Create: `tests/modules/avatars/test_admin_avatar_item_catalog.py`
- Documentation: OpenAPI + `FAST-API-INSTRUCTIONS.md` update.
- Definition of Done: suite green, docs complete.

**Task 08 — Final Code Review**
- Task ID: B-03-T08
- Do Not Change: `badges`/achievement-level/habit-milestone-type source tables owned by A.7/A.9/A.11; PostgreSQL credentials.
- Expected Result: PR merge-ready, CI green including both P0 gates.

## 30. Definition of Done
Admin CRUD for `avatar_items` live, RBAC-guarded, audit-logged. `unlock_rule` write path structurally rejects any non-existent badge/level/milestone reference. Retire action never affects existing owners. Non-retroactivity of `unlock_rule` updates verified.

## 31. Final Verification Checklist
- [x] `UnlockRuleSchema` discriminated union matches `UnlockRuleResolver`'s expected shape exactly
- [x] `UnlockRuleValidator` rejects fake badge_id / fake milestone type (CI-blocking test passing)
- [x] Create/Update/List/Get/Retire endpoints live and RBAC-guarded
- [x] Retire sets `is_retired=true` only — regression test confirms existing owners unaffected (CI-blocking)
- [x] `unlock_rule` update non-retroactivity verified (Edge Case 11)
- [x] Every mutating action writes an immutable audit log row
- [x] Pagination/filtering/sorting implemented on list endpoint
- [x] Unit + integration tests passing
- [x] OpenAPI documentation complete
- [x] No PostgreSQL credential changes
- [x] No unrelated existing-context code modified
