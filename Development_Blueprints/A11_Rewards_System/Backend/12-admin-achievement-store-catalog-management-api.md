# B-12 — Admin Achievement Store Catalog Management API (Admin)

## 1. Feature Context
Part of Feature A.11 — Rewards System. Admin CRUD for `catalog_items`, with "delete" implemented strictly as deactivation to preserve existing ownership records.

## 2. Parent Feature
A.11 Rewards System — Backend (FastAPI)

## 3. Sub-feature
B-12 Admin Achievement Store Catalog Management API (Admin)

## 4. Objective
Implement admin CRUD for `catalog_items` (B-06's table), restricted to `content_editor`, per PRD §8/§9.

## 5. Business Requirements
- CRUD for `catalog_items` (type, `price_points`, `eligibility_json`, `active`).
- Delete = `active=false` only — never a hard delete, preserving existing `child_inventory` ownership.
- `price_points > 0` validated.

## 6. Existing Architecture
Extends the `rewards` bounded context's admin surface, reusing B-06's `CatalogItem` model directly.

## 7. Existing Code to Reuse
- B-06's `CatalogItem` model.
- `require_admin_scope("content_editor")`.

## 8. Files to Create
- `tests/modules/rewards/test_catalog_admin_crud.py`
- `tests/modules/rewards/test_catalog_deactivate_preserves_ownership.py`

## 9. Files to Modify
- `src/noorheroes/modules/rewards/schemas.py` — `CatalogItemCreateRequest`, `CatalogItemAdminResponse`.
- `src/noorheroes/modules/rewards/service.py` — `create_catalog_item()`, `deactivate_catalog_item()`.
- `src/noorheroes/modules/rewards/api.py` — add admin routes under `/v1/admin/rewards/catalog-items`.

## 10. Backend Requirements
- No hard-delete endpoint exists for `catalog_items` at all — only a `PATCH .../deactivate` action, structurally preventing accidental data loss.
- `price_points > 0` validated at both the schema and DB CHECK-constraint layers.
- RBAC: `content_editor` only.

## 11. KMP Requirements
Not applicable (admin-only); consumed indirectly via B-06's user-facing catalog read.

## 12. NextJS Requirements
Consumed by N-04 (Achievement Store Catalog Manager).

## 13. API Contract

**Required API**
- **HTTP Method:** GET / POST / PATCH
- **Endpoint:** `/v1/admin/rewards/catalog-items`, `/v1/admin/rewards/catalog-items/{id}/deactivate`
- **Auth:** Bearer, admin session, `content_editor` scope.
- **Error Responses:** `422` invalid `price_points`; no `DELETE` route exists.

## 14. Database Requirements
Reuses B-06's `catalog_items` table; no new columns beyond admin-attribution fields if not already present.

## 15. Validation
Test: deactivating an item leaves all existing `child_inventory` rows referencing it fully intact and equippable-eligible (equip logic itself owned by A.12, but ownership-record integrity is this task's responsibility).

## 16. Authentication
Bearer JWT, admin session.

## 17. Authorization
`require_admin_scope("content_editor")`.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Invalid `price_points` (≤0) | 422 |
| Attempt to hard-delete | No such route exists — 404 by design, not a soft-blocked 403 |
| Unauthorized/forbidden request | 401/403 |

## 19. Offline First
N/A (admin web).

## 20. Local Data
N/A.

## 21. Localization
Item type/category keys stored; localized display text resolved elsewhere.

## 22. RTL
N/A (backend).

## 23. Analytics
N/A; mutations audit-logged.

## 24. Performance
Low-traffic admin endpoint.

## 25. Security
Structural absence of a hard-delete route is the primary defense against accidental ownership-record breakage.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, PostgreSQL, Pydantic v2.

## 27. Testing
- Unit: `price_points` validation.
- Integration: full CRUD + deactivate flow, ownership-preservation test (mandatory).

## 28. Documentation
OpenAPI docs explicitly noting no hard-delete route exists by design.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement Catalog CRUD + Deactivate Service Methods**
- Files to Modify: `service.py`
- Business Rules: `price_points > 0`, deactivate-only removal.
- Tests: CRUD + ownership-preservation tests.
- Definition of Done: correct behavior verified.

**Task 02 — Implement Admin Endpoints with RBAC**
- Files to Modify: `api.py`
- Authentication/Authorization: per §16/§17.
- Tests: RBAC tests.
- Definition of Done: endpoints live, no DELETE route present.

**Task 03 — Add Documentation & Final Review**
- Documentation: OpenAPI notes per §28.
- Do Not Change: never add a hard-delete route to this module.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Admin catalog CRUD live; deactivate-only removal verified to preserve ownership; RBAC-protected.

## 31. Final Verification Checklist
- [ ] No hard-delete route exists for `catalog_items`
- [ ] Deactivation preserves all existing `child_inventory` rows
- [ ] `price_points > 0` validated at schema and DB layers
- [ ] RBAC restricts to `content_editor`
- [ ] OpenAPI documentation complete
