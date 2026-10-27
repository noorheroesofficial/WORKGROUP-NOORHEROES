# B-01 — Child Profile Directory API

## 1. Feature Context
Part of **Feature C.21 — Multi-Child Management**, the ongoing family-management surface reachable from the Parent Dashboard (C.20). This sub-feature is the read/list entry point every other C.21 mutation flows back to.

## 2. Parent Feature
C.21 Multi-Child Management (`PRD_Documents/Parent Area — In-App (19-26)/Feature_C21_Multi_Child_Management.md`)

## 3. Sub-feature
**B-01 — Child Profile Directory API** (`GET /v1/family/children`, extends the existing A.1 endpoint)

## 4. Objective
Return every child profile belonging to the authenticated parent's family — active and disabled alike — ordered by `display_order`, with enough fields for the KMP Child Management List (K-01) to render status, avatar, age, and read-only affordances without a second round trip.

## 5. Business Requirements
- FR-1: list must expose child list cards (avatar, age, status) and support a per-child action menu downstream.
- Acceptance Criteria (§1.9): "Given a parent opens Child Management, then it lists every child (active and disabled), with disabled children clearly marked."
- Non-Functional: list load p95 < 500ms (§1.8).

## 6. Existing Architecture
Follows the FastAPI modular monolith (`FAST-API-INSTRUCTIONS.md`): Router → Service → Repository → PostgreSQL, request-scoped `AsyncSession` via `get_db_session`, parent identity via `get_current_parent` → `ParentSessionContext`. Lives in the existing `identity` bounded context (`src/noorheroes/modules/identity/`).

## 7. Existing Code to Reuse
- `IdentityService.list_children_for_parent(family_id)` — already implemented in A.1; extend, do not duplicate.
- `ChildRepository.get_by_family_id()` — already implemented; extend to include disabled rows and order by `display_order`.
- `ParentSessionContext` / `Depends(get_current_parent)` — reuse as-is.
- `ChildProfileResponse` schema — extend, do not fork a parallel schema.

## 8. Files to Create
None — this is a pure extension of existing A.1 files. No new files required.

## 9. Files to Modify
- `src/noorheroes/modules/identity/repository.py` — extend `ChildRepository.get_by_family_id()` to order by `display_order` and include `status='disabled'` rows (currently likely filters to active only).
- `src/noorheroes/modules/identity/service.py` — extend `list_children_for_parent()` to pass through `status` and `dob_locked_at`.
- `src/noorheroes/modules/identity/schemas.py` — add `status: ChildStatus` and `dob_locked_at: datetime | None` and `display_order: int` to `ChildProfileResponse`.
- `src/noorheroes/modules/identity/api.py` — no route signature change; response model gains fields only (non-breaking).
- `tests/modules/identity/test_children_directory.py` — extend/create test module.

## 10. Backend Requirements
- Endpoint remains `GET /v1/family/children`, `Depends(get_current_parent)`.
- Response is a list of `ChildProfileResponse`, ordered by `display_order ASC`.
- Every child in the family is returned regardless of `status` (`active`, `disabled`; `deletion_pending`/`deleted` children are excluded — they no longer belong in this list per §4.5 soft-delete rules).
- Single query, no N+1: select all columns needed for the card (avatar reference, nickname, dob → derived age, status, display_order) in one `ChildRepository` call.

## 11. KMP Requirements
- `ChildManagementViewModel` (K-01) calls the repository method that wraps this endpoint through `:core:data`'s `FamilyRepository.observeChildren()` / `refreshChildren()` pair (offline-first, per `CORE_DATA_INSTRUCTIONS.md`).
- Response shape must map cleanly onto the Room entity used for local caching so K-09's sync layer does not need a translation shim beyond the standard DTO → Entity mapper.

## 12. NextJS Requirements
Not applicable — this is a parent-facing (User API) endpoint with no Admin Portal consumer.

## 13. API Contract

**`GET /v1/family/children`**
- **Auth:** Bearer (parent session) — `Depends(get_current_parent)`. No step-up required (read-only).
- **Request:** none (no query params in the current PRD-published contract; do not add pagination unless a future contract adds it — families are small, bounded lists).
- **Response 200:**
```json
[
  {
    "childId": "uuid",
    "nickname": "string",
    "dob": "date",
    "dobLockedAt": "timestamp|null",
    "status": "active|disabled",
    "displayOrder": 0,
    "avatarId": "string",
    "createdAt": "timestamp",
    "updatedAt": "timestamp"
  }
]
```
- **Error Responses:** `401` (missing/invalid bearer token).

## 14. Database Requirements
- Table: `child` (existing, per §4.2). No migration required for this sub-feature alone — `display_order` and `status` columns are assumed present from B-03/B-04/B-07's migrations; if B-01 is implemented first, add these columns here (see Task 01 below) rather than duplicating them later.
- Index: `(family_id, display_order)` — required for ordered retrieval performance at p95 < 500ms.

## 15. Validation
- No request-body validation (GET-only).
- Response-level: never leak children belonging to another family — enforced by filtering strictly on `parent_ctx.family_id`, never a client-supplied family ID.

## 16. Authentication
Bearer JWT via `get_current_parent`. Standard parent session is sufficient; this is a read endpoint and does not require step-up.

## 17. Authorization
Implicit family-scoping: the repository query always filters by `family_id` derived from the authenticated `ParentSessionContext`, never from client input. No RBAC scopes beyond "is an authenticated parent."

## 18. Error Handling
| Scenario | Response |
|---|---|
| Missing/invalid bearer token | `401` (`AuthenticationError`) |
| Family has zero children | `200` with `[]` |
| Database unavailable | `503`/`500` per existing global exception handler, logged with request ID |

## 19. Offline First
This endpoint is the remote-refresh source for K-09's offline-first repository. The client always renders from local cache first, then reconciles with this endpoint's response — no server-side change needed to support that beyond stable, complete field data.

## 20. Local Data
N/A on the backend side; see K-09 for the Room schema this response hydrates.

## 21. Localization
`nickname` is user-entered free text, not translated. No localized string fields are returned by this endpoint.

## 22. RTL
N/A — backend has no directional concerns.

## 23. Analytics
None server-side; `child_management_viewed` is fired client-side in K-01 upon successful load.

## 24. Performance
- Single indexed query on `(family_id, display_order)`.
- No pagination needed given realistic family sizes (bounded by subscription tier capacity, typically ≤ 10).
- Target: p95 < 500ms end-to-end (§1.8).

## 25. Security
- Strict family-scoping prevents cross-family enumeration (`ChildScopeViolationError` is not reachable here since the query is server-derived, not client-supplied — document this as a defense-in-depth note).
- No PII beyond what the parent already owns is exposed.

## 26. Library Requirements
No new libraries. Uses existing FastAPI, SQLAlchemy 2.0 async, Pydantic v2 stack.

## 27. Testing
- Unit: `ChildRepository.get_by_family_id()` returns disabled rows, ordered correctly.
- Unit: `list_children_for_parent()` maps `status`/`dob_locked_at`/`display_order` into the response DTO.
- Integration: authenticated parent with 3 active + 2 disabled children receives all 5, correctly ordered.
- Integration: parent with zero children receives `[]`.
- Integration: unauthenticated request receives `401`.
- Integration: family A's parent never receives family B's children (cross-family isolation test).

## 28. Documentation
Update the endpoint's OpenAPI `description` to state it now includes disabled children, and regenerate `openapi.json` via `scripts/export_openapi_schema.py`.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Extend Child ORM Model**
- **Objective:** Ensure `Child` ORM model exposes `status`, `display_order`, `dob_locked_at` columns.
- **Why Required:** The directory response depends on these fields existing; other B-0x sub-features write to them, this one is the first to read them.
- **Existing Architecture to Follow:** `TimestampMixin` pattern in `infrastructure/db/base.py`.
- **Existing Files to Reuse:** `modules/identity/models.py`.
- **Files to Modify:** `modules/identity/models.py`.
- **Implementation Details:** Add `status: Mapped[str]` (CHECK constraint `active|disabled|deletion_pending|deleted`), `display_order: Mapped[int]`, `dob_locked_at: Mapped[datetime | None]` if not already present from A.1.
- **Business Rules:** Default `status='active'`; `display_order` defaults to insertion order.
- **Validation:** DB-level CHECK constraint on `status`.
- **Do Not Change:** Do not alter existing `dob`, `nickname`, `family_id` columns.
- **Expected Result:** Model reflects the full lifecycle schema from §4.2.
- **Definition of Done:** Alembic migration generated and applied cleanly against a fresh DB.

**Task 02 — Extend Repository Query**
- **Objective:** `ChildRepository.get_by_family_id()` returns all non-deleted statuses, ordered by `display_order`.
- **Files to Modify:** `modules/identity/repository.py`.
- **Implementation Details:** `select(Child).where(Child.family_id == family_id, Child.status.in_(["active", "disabled"])).order_by(Child.display_order.asc())`.
- **Performance:** Confirm the `(family_id, display_order)` index is used via `EXPLAIN`.
- **Tests:** Unit test with mixed-status fixture data.
- **Definition of Done:** Query returns correct ordering and excludes `deletion_pending`/`deleted`.

**Task 03 — Extend Response Schema & Service**
- **Objective:** Surface `status`, `displayOrder`, `dobLockedAt` in `ChildProfileResponse`.
- **Files to Modify:** `modules/identity/schemas.py`, `modules/identity/service.py`.
- **Implementation Details:** Pydantic v2 `NoorHeroesBaseModel` subclass fields with camelCase aliasing per existing convention.
- **Tests:** Schema serialization unit test.
- **Definition of Done:** Response matches §13 contract exactly.

**Task 04 — Integration Tests & OpenAPI Update**
- **Objective:** Full-path verification and documentation refresh.
- **Files to Create:** `tests/modules/identity/test_children_directory.py`.
- **Implementation Details:** Cover all §27 test cases including cross-family isolation.
- **Documentation:** Run `export_openapi_schema.py`; diff-check via `classify_openapi_diff.py` to confirm non-breaking change.
- **Definition of Done:** All tests green; OpenAPI diff shows additive-only change.

## 30. Definition of Done
- Endpoint returns active + disabled children, correctly ordered, within performance target.
- No cross-family data leakage possible.
- All new fields documented in OpenAPI.
- Full unit + integration test coverage per §27.

## 31. Final Verification Checklist
- [ ] `status`, `display_order`, `dob_locked_at` present on `Child` model and migrated
- [ ] Repository query ordered by `display_order`, includes disabled, excludes deleted
- [ ] Response schema matches §13 contract
- [ ] Cross-family isolation test passes
- [ ] p95 < 500ms verified against realistic fixture data
- [ ] OpenAPI regenerated and diff reviewed as non-breaking
- [ ] No new libraries introduced
- [ ] PostgreSQL/Redis credentials untouched
