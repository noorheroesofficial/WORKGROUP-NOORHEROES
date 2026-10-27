# B-06 — Avatar Item Management API

## 1. Feature Context
Part of **Feature E.31 — Engagement Tools Admin Suite**. Delivers the admin CRUD surface for the avatar item catalog consumed by A.12's Avatar & Inventory Service. Source: PRD §1.7 FR-5, §3.4, §5 item 3.

## 2. Parent Feature
Feature E.31 — Engagement Tools Admin Suite

## 3. Sub-feature
1.6 Avatar Item Management API (Backend ID: **B-06**)

## 4. Objective
Let content admins manage the avatar item catalog (outfits, glow states) with unlock rules mapped to real badges/levels/milestones, while structurally guaranteeing no real-money purchase path can ever be configured for child mode, and that retiring an item never removes it from children who already own it.

## 5. Business Requirements
- FR-5 (PRD §1.7): screens — avatar base library, item catalog, unlock-rule mapping. CRUD: create, read ownership distribution, update unlock rule, retire (owned items remain equippable).
- **Hard rule:** items are never sold for real money in child mode.
- **Hard rule:** unlock rules must map to an existing badge, level, or habit milestone — no arbitrary/opaque unlocks.
- Acceptance Criteria (PRD §1.9): attempting to configure a real-money purchase option for a child-mode avatar item must be impossible — the field/option doesn't exist.
- Edge Case 4 (PRD §1.10): an unlock rule referencing a later-retired badge becomes unresolvable for new unlock evaluation going forward; the item shows "currently unavailable to unlock" gracefully (A.12's established pattern); children who already unlocked it via the badge before retirement keep it.

## 6. Existing Architecture
Extends A.12's Avatar & Inventory Service. FastAPI/SQLAlchemy 2.0/PostgreSQL, Router → Service → Repository layering.

## 7. Existing Code to Reuse
- A.12's existing `avatar_items`/`child_inventory` models and unlock-evaluation logic (not reimplemented here).
- A.12's existing "currently unavailable to unlock" graceful-degradation state handling for dangling unlock-rule references.
- E.28's audit log + RBAC; E.29's upload-safety pipeline for item artwork.

## 8. Files to Create
- `app/routers/admin/avatar_items_router.py`
- `app/schemas/admin/avatar_item_schemas.py`
- `app/services/admin/avatar_item_admin_service.py`
- `app/repositories/admin/avatar_item_admin_repository.py`
- `tests/admin/test_avatar_item_admin_api.py`

## 9. Files to Modify
- `app/routers/admin/__init__.py`
- `app/core/audit.py` (`avatar_item.created`, `avatar_item.unlock_rule_updated`, `avatar_item.retired`, `avatar_item.realmoney_attempt_blocked`)

## 10. Backend Requirements
- **Database:** `avatar_items` (existing A.12, extended with `is_retired` flag if not present), `child_inventory` (existing, read-only reference).
- **Migration:** additive only; **critically, the migration must NOT add any real-money price column** to `avatar_items`.
- **Model:** `AvatarItem` — Pydantic/SQLAlchemy schema for this resource must have **no field at all** representing a real-money price for child-mode purchase.
- **Schema/DTO:** `AvatarItemCreate` (name, category, art_asset_id, `unlock_rule: {type: "badge"|"level"|"habit_milestone", reference_id}`), `AvatarItemUpdate` (unlock rule only), `AvatarItemRead` (includes `ownership_distribution` on the list/detail read).
- **Repository:** `create()`, `list_with_ownership_distribution()`, `update_unlock_rule()`, `retire()`.
- **Service:** validates `unlock_rule.reference_id` resolves to an existing badge/level/milestone at creation/update time; audit logs; upload-pipeline calls for artwork.
- **Router:** `POST /v1/admin/avatar-items`, `GET /v1/admin/avatar-items`, `PATCH /v1/admin/avatar-items/{id}`, `POST /v1/admin/avatar-items/{id}/retire`.
- **Dependency Injection:** `require_role("content_editor")`.
- **Validation:** `unlock_rule.type` ∈ {`badge`, `level`, `habit_milestone`}; `reference_id` must resolve against the corresponding existing table at validation time (badge exists, level exists, or habit milestone exists) — reject with `422` if unresolvable at creation/update time. (Note: a badge retired *after* the unlock rule was set is a distinct, permitted runtime-degradation scenario per Edge Case 4, handled by A.12's existing evaluation logic, not blocked here.)
- **Business Rules:** retire sets `is_retired=true`; A.12's ownership/equip logic (unmodified) continues to allow already-owned items to remain equippable — this sub-feature does not touch that equip-time logic.
- **Exception Handling:** `404`, `422 INVALID_UNLOCK_REFERENCE`.
- **Logging:** structured logs; if any request payload contains an unexpected real-money-price-like field, log it as a security signal (`avatar_item_realmoney_attempt_blocked`) and reject with `422 UNKNOWN_FIELD` (Pydantic's default `extra="forbid"` behavior achieves this structurally).
- **Caching:** invalidate cached "active avatar item catalog" list on write.
- **Transaction:** update + audit log in one transaction.
- **Pagination/Filtering/Sorting:** catalog list paginated, filterable by category/retired status.

## 11. KMP Requirements
N/A — admin-only. The KMP app's avatar equip/unlock experience continues via A.12's existing child-facing endpoints and evaluation engine, including its established "currently unavailable to unlock" graceful state for dangling references.

## 12. NextJS Requirements
Consumed by **N-06 Avatar Item Management UI**, whose form must have zero real-money price input rendered anywhere, mirroring this backend's structural schema absence.

## 13. API Contract

### `POST /v1/admin/avatar-items`
- **Request:**
```json
{
  "name_key": "golden_glow_outfit",
  "category": "glow_state",
  "art_asset_id": "uuid",
  "unlock_rule": { "type": "badge", "reference_id": "uuid" }
}
```
- **Response (201):** `AvatarItemRead` — schema contract-verified to contain no real-money price field
- **Errors:** `401`, `403`, `422 INVALID_UNLOCK_REFERENCE`, `422 ART_UPLOAD_REJECTED`, `422 UNKNOWN_FIELD` (Pydantic `extra="forbid"` rejects any unexpected price-like field)

### `GET /v1/admin/avatar-items`
- Response includes `ownership_distribution: { total_owners, percent_of_active_children }`

### `PATCH /v1/admin/avatar-items/{id}`
- **Request:** `{ "unlock_rule": { "type": "level", "reference_id": "uuid" } }`
- **Response (200):** updated `AvatarItemRead`

### `POST /v1/admin/avatar-items/{id}/retire`
- **Response (200):** `{ "id": "uuid", "is_retired": true }` — owned items remain equippable (unaffected by this call)

## 14. Database Requirements
- `avatar_items`: extended with `is_retired boolean default false`. **No real-money price column added, ever.**
- `child_inventory`: read-only, no schema change.

## 15. Validation
`unlock_rule.type` ∈ registered types; `reference_id` resolves to an existing entity of that type at write time; Pydantic schema uses `model_config = ConfigDict(extra="forbid")` to structurally reject any unrecognized field, including any attempted price field.

## 16. Authentication
Admin JWT (E.28).

## 17. Authorization
`content_editor`+.

## 18. Error Handling
| Scenario | Response |
|---|---|
| `unlock_rule.reference_id` doesn't resolve | `422 INVALID_UNLOCK_REFERENCE` |
| Unrecognized/extra field in request (e.g., a price-like field) | `422 UNKNOWN_FIELD` |
| Art fails upload-safety pipeline | `422 ART_UPLOAD_REJECTED` |
| Unknown item id | `404 NOT_FOUND` |
| Unauthorized/forbidden | `401`/`403` |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
`name_key` references a localization key.

## 22. RTL
N/A at API layer.

## 23. Analytics
`avatar_item_created`, `avatar_item_unlock_rule_updated`, `avatar_item_realmoney_attempt_blocked` (internal/security signal) per PRD §1.19.

## 24. Performance
`ownership_distribution` aggregation via indexed query on `child_inventory(avatar_item_id)`.

## 25. Security
Structural absence of any real-money field is this endpoint's primary child-safety/economy-integrity contribution (PRD §12.7); `extra="forbid"` schema config is the concrete mechanism enforcing it, not just documentation convention.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Pydantic v2 (`ConfigDict(extra="forbid")`), pytest-asyncio.

## 27. Testing
- Unit: unlock-rule reference resolution.
- Integration: signature contract/schema test asserting no real-money field exists anywhere in `AvatarItemCreate`/`AvatarItemUpdate`/`AvatarItemRead` Pydantic schemas (PRD §5 item 3) — e.g., introspect `model_fields` and assert no key matches price-related patterns, and separately assert `extra="forbid"` rejects an injected `price_usd` field with `422`.
- Edge cases: Edge Case 4 — unlock rule referencing a later-retired badge; confirm this sub-feature's own endpoints don't error (retirement happens via B-05, this test confirms B-06's read/update paths tolerate a dangling reference gracefully, consistent with A.12).
- Negative cases: invalid unlock reference, unauthorized.

## 28. Documentation
OpenAPI docs explicitly noting the structural absence of any monetary field for this resource, as a documented security/child-safety guarantee.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Database Model**
- Task ID: B-06-T01
- Objective: Add `is_retired` flag; confirm no price column exists or is added.
- Files to Modify: `app/models/avatar_item.py`.
- Tests: migration test; schema-introspection test confirming no monetary column.
- Dependencies: none.
- Do Not Change: `child_inventory` schema, A.12's equip-time logic.
- Definition of Done: migration applies cleanly.

**Task 02 — Schema with Structural Real-Money Exclusion**
- Task ID: B-06-T02
- Objective: Build Pydantic schemas with `extra="forbid"` and no monetary field.
- Files to Create: `app/schemas/admin/avatar_item_schemas.py`.
- Tests: `test_no_realmoney_field_in_schema` (introspects `model_fields`), `test_extra_price_field_rejected` (posts an unexpected `price_usd` field, expects `422`).
- Dependencies: Task 01.
- Definition of Done: both tests green — this is the PRD's signature guarantee for this sub-feature.

**Task 03 — Repository & Service Layers**
- Task ID: B-06-T03
- Files to Create: `app/repositories/admin/avatar_item_admin_repository.py`, `app/services/admin/avatar_item_admin_service.py`.
- Implementation Details: unlock-rule reference resolution against badge/level/milestone tables.
- Dependencies: Tasks 01–02.
- Definition of Done: unit tests green.

**Task 04 — API Endpoints**
- Task ID: B-06-T04
- Files to Create: `app/routers/admin/avatar_items_router.py`.
- Dependencies: Task 03.
- Definition of Done: integration tests green.

**Task 05 — Documentation & Final Review**
- Task ID: B-06-T05
- Dependencies: Tasks 01–04.
- Definition of Done: §31 checklist verified.

## 30. Definition of Done
Contract test proves structural real-money-field absence; unlock-rule validation enforced; retire preserves ownership/equippability; all endpoints audited and tested.

## 31. Final Verification Checklist
- [ ] `AvatarItemCreate`/`Update`/`Read` schemas contain zero real-money/price fields (contract test green)
- [ ] Posting an unexpected price-like field is rejected with `422` (`extra="forbid"` verified)
- [ ] Unlock rule validated against existing badge/level/milestone at write time
- [ ] Retire sets `is_retired=true`, does not affect `child_inventory` ownership/equippability
- [ ] Ownership distribution read endpoint functional
- [ ] Audit log entries written for every mutation
- [ ] Unauthorized/forbidden paths tested
- [ ] No school/madrasa/institutional-tier logic introduced
- [ ] PostgreSQL/Redis credentials untouched
