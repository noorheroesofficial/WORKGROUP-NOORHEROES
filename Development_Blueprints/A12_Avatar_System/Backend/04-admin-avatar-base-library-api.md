# B-04 — Admin Avatar Base Library API

## 1. Feature Context
NoorHeroes Backend (FastAPI). Part of Feature A.12 — Avatar System. Admin-only CRUD for the `avatars` base library (the set of selectable base characters), which A.1's Add Child flow references at child-profile creation time. This sub-feature does not implement base selection itself (owned by A.1) — only the catalog admins manage.

## 2. Parent Feature
A.12 Avatar System — Backend (FastAPI)

## 3. Sub-feature
B-04 Admin Avatar Base Library API

## 4. Objective
Implement admin CRUD endpoints for the `avatars` base library (`name`, `base_asset_key`), backing FR-11 and PRD §8 Admin Requirements "Avatar Base Library: CRUD for `avatars`."

## 5. Business Requirements
- Full CRUD for avatar base entries, restricted to `content_editor` role (PRD §8 CRUD permissions table).
- Every base asset must pass the same modesty/appropriateness review pipeline used elsewhere (FR-12) — base creation here produces a pending-review entry; approval is B-05's concern, mirroring the item-catalog flow.
- Base entries referenced by an existing `ChildProfile.avatar_id` (A.1) must never be hard-deleted — this sub-feature does not expose a delete-by-removal action, only update, consistent with the platform's general non-destructive-catalog-change principle already established for `avatar_items` (FR-10).

## 6. Existing Architecture
Extends the `avatars` bounded context established in B-01. Follows the identical Admin RBAC/audit-logging pattern used by B-03. `avatars.avatar_id` is referenced by A.1's `ChildProfile.avatar_id` foreign key (per A.1 PRD's Add Child flow) — this cross-context reference must be respected: no hard-delete action is exposed on this API surface.

## 7. Existing Code to Reuse
- `Avatar` model (B-01)
- `get_current_admin`/`require_admin_scope()` (`core/deps.py`)
- `AdminAuditRepository.log_action()` (`modules/admin/repository.py`)
- `AvatarAdminRouter`'s RBAC/audit-logging pattern (B-03) as the direct structural reference

## 8. Files to Create
- `src/noorheroes/modules/avatars/admin_schemas.py` — add `AvatarBaseCreateRequest`, `AvatarBaseUpdateRequest`, `AvatarBaseAdminResponse` (same file B-03 creates; this task extends it)
- `tests/modules/avatars/test_admin_avatar_base_library.py`

## 9. Files to Modify
- `src/noorheroes/modules/avatars/repository.py` — add `create_avatar_base()`, `update_avatar_base()`, `list_avatar_bases()`, `get_avatar_base_by_id()`
- `src/noorheroes/modules/avatars/admin_api.py` — add avatar-base routes to the existing `AvatarAdminRouter` established in B-03

## 10. Backend Requirements
- `POST /v1/admin/avatars` creates a base entry (`name`, `base_asset_key`) in a pending-review state (consistent with B-05's review workflow).
- `PATCH /v1/admin/avatars/{avatarId}` updates an existing base entry.
- `GET /v1/admin/avatars` (list, paginated) / `GET /v1/admin/avatars/{avatarId}` (single).
- No delete/retire action exposed on this endpoint set — base entries referenced by `ChildProfile.avatar_id` must remain permanently resolvable; if a base needs to be sunset from new-selection availability, that is expressed via a `status`/`selectable` flag update (PATCH), never a destructive action.
- Every mutating action writes an immutable `AdminAuditLog` row.

## 11. KMP Requirements
Not applicable — admin-only surface. Base *selection* by the child/parent at profile creation is A.1's existing `GET` catalog consumption, unaffected by this sub-feature.

## 12. NextJS Requirements
Not applicable directly; consumed by N-01's Avatar Base Library Management page.

## 13. API Contract

**Required API 1**
- **HTTP Method:** POST
- **Endpoint:** `/v1/admin/avatars`
- **Request:** `{ "name": "...", "base_asset_key": "..." }`
- **Response 201:** `AvatarBaseAdminResponse`
- **Authentication:** Bearer, admin session
- **Authorization:** `content_editor` scope
- **Error Responses:** `401`; `403`; `409` duplicate name/key where applicable; `422` invalid payload

**Required API 2**
- **HTTP Method:** PATCH
- **Endpoint:** `/v1/admin/avatars/{avatarId}`
- **Request:** partial `AvatarBaseUpdateRequest`
- **Response 200:** `AvatarBaseAdminResponse`
- **Error Responses:** `401`; `403`; `404`; `422`

**Required API 3**
- **HTTP Method:** GET
- **Endpoint:** `/v1/admin/avatars` (paginated list) and `/v1/admin/avatars/{avatarId}` (single)
- **Authentication/Authorization:** admin session, read scope

## 14. Database Requirements
Extends `avatars` from B-01 — no new tables, no new columns beyond what B-01 defined. If a "selectable at child-creation" toggle is required by product (not explicitly specified in the PRD beyond base CRUD), add `selectable BOOLEAN DEFAULT true` in this task's migration rather than guessing a broader schema.

## 15. Validation
- Reject duplicate `name`/`base_asset_key` combinations where the platform's content-governance conventions require uniqueness (mirroring `avatar_items`' duplicate-handling convention referenced in B-03).
- No delete endpoint exists on this router — this absence is itself a deliberate, testable property (mirrors FR-3's "no upload path" testable-absence pattern).

## 16. Authentication
Bearer JWT, admin session via `get_current_admin`.

## 17. Authorization
`content_editor` role required for all mutating actions.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Attempt to reference a non-existent `avatarId` on update | `404` |
| Duplicate base name/key | `409` |
| Unauthorized/forbidden request | `401`/`403` |
| Database failure | `500`/`503` |

## 19. Offline First / 20. Local Data
N/A (backend, admin-only, online-by-design surface).

## 21. Localization
`name` stored as translation key, consistent with B-01/B-03's convention.

## 22. RTL
N/A at the API layer.

## 23. Analytics
Not applicable; `AdminAuditLog` is the operational record of truth.

## 24. Performance
Low-traffic admin surface; standard paginated list, no special performance requirements beyond existing conventions.

## 25. Security
RBAC (`content_editor` scope) is the primary control; absence of a delete endpoint is a structural safeguard against orphaning `ChildProfile.avatar_id` references.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 (async), Pydantic v2.

## 27. Testing
- Unit: repository CRUD methods.
- Integration: full create/update/list/get flow; duplicate-name rejection; unauthorized/forbidden rejection; confirm no delete route is registered on the router (schema-scan/route-introspection test).
- Regression: confirm A.1's Add Child avatar-base-selection consumer is unaffected by this sub-feature's additions.

## 28. Documentation
OpenAPI documentation for all endpoints; update the `avatars` context entry in `FAST-API-INSTRUCTIONS.md`.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement Avatar Base Repository Methods**
- Task ID: B-04-T01
- Objective: `create_avatar_base()`, `update_avatar_base()`, `list_avatar_bases()`, `get_avatar_base_by_id()`.
- Existing Architecture to Follow: `AvatarRepository` pattern established in B-01, extended per B-03's item-CRUD structure.
- Files to Modify: `src/noorheroes/modules/avatars/repository.py`
- Tests: repository-level tests.
- Definition of Done: methods correct against fixture data; no delete method exists.

**Task 02 — Define Admin Schemas**
- Task ID: B-04-T02
- Objective: `AvatarBaseCreateRequest`/`AvatarBaseUpdateRequest`/`AvatarBaseAdminResponse`.
- Files to Modify: `src/noorheroes/modules/avatars/admin_schemas.py`
- Tests: schema validation unit tests.
- Definition of Done: schemas match §13 contract.

**Task 03 — Implement Endpoints on `AvatarAdminRouter`**
- Task ID: B-04-T03
- Objective: Add POST/PATCH/GET routes to the router established in B-03.
- Files to Modify: `src/noorheroes/modules/avatars/admin_api.py`
- Authentication/Authorization: `Depends(get_current_admin)` + `require_admin_scope("content:write")`.
- Implementation Details: audit-log every mutation.
- Tests: integration tests for all endpoints.
- Definition of Done: endpoints live, documented, audit-logged.

**Task 04 — Add No-Delete-Route Regression Test**
- Task ID: B-04-T04
- Files to Create: `tests/modules/avatars/test_admin_avatar_base_library.py`
- Implementation Details: route-introspection test asserting no `DELETE /v1/admin/avatars/{avatarId}` route is registered.
- Definition of Done: test passes and guards against future accidental addition of a destructive delete path.

**Task 05 — Add Full CRUD Test Suite & Documentation**
- Task ID: B-04-T05
- Documentation: OpenAPI + `FAST-API-INSTRUCTIONS.md` update.
- Definition of Done: suite green, docs complete.

**Task 06 — Final Code Review**
- Task ID: B-04-T06
- Do Not Change: `ChildProfile.avatar_id` foreign-key relationship owned by A.1; PostgreSQL credentials.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Admin CRUD for the `avatars` base library live, RBAC-guarded, audit-logged, with no destructive delete path exposed. A.1's existing base-selection consumer unaffected.

## 31. Final Verification Checklist
- [x] Create/Update/List/Get endpoints live and RBAC-guarded
- [x] No delete route registered (regression test passing)
- [x] Duplicate name/key rejected with `409`
- [x] Every mutating action writes an immutable audit log row
- [x] A.1's Add Child avatar-base consumer unaffected (regression test)
- [x] Unit + integration tests passing
- [x] OpenAPI documentation complete
- [x] No PostgreSQL credential changes
- [x] No unrelated existing-context code modified
