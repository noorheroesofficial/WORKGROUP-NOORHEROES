# B-09 — Story Favorites API

## 1. Feature Context
A simple, low-risk CRUD surface letting a child bookmark stories/episodes, with careful handling of two edge cases: duplicate favoriting and favorites pointing at content that has since been withdrawn or restructured (merged/re-categorized).

## 2. Parent Feature
Feature A.3 — Stories Module (Animated Storytelling System)

## 3. Sub-feature
1.9 Story Favorites API (ID: **B-09**)

## 4. Objective
Implement favorites CRUD inside the existing `content` module with duplicate prevention, optimistic-update-friendly responses, and resolution of favorites referencing restructured or withdrawn content.

## 5. Business Requirements
- Edge Case 11: a favorited story later re-categorized/merged into a different series by Admin → favorite reference resolves to the new canonical content ID, never a silent 404.
- §4.4 Soft Delete Rules: `favorite` rows referencing a withdrawn episode remain, but the UI shows "no longer available" rather than breaking the list.

## 6. Existing Architecture
Extends the existing `content` module. Router → Service → Repository → Postgres.

## 7. Existing Code to Reuse
- `common/base_service.py`, `common/base_repository.py`
- `core/deps.py::get_current_child`

## 8. Files to Create
- `src/noorheroes/modules/content/favorite_models.py` — `FavoriteOrm`
- `alembic/versions/xxxx_add_favorite.py`
- `src/noorheroes/modules/content/favorite_schemas.py` — `FavoriteRequest`, `FavoriteListResponse`
- `src/noorheroes/modules/content/favorite_repository.py` — `FavoriteRepository`
- `src/noorheroes/modules/content/favorite_service.py` — `FavoriteService(BaseService)`
- `tests/modules/content/test_favorite_service.py`
- `tests/modules/content/test_favorite_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/content/api.py::ContentRouter` — add `POST /v1/favorites`, `DELETE /v1/favorites/{episode_id}`, `GET /v1/favorites`

## 10. Backend Requirements
- `FavoriteService.add_favorite(child_id, episode_id)`: upsert semantics — adding an already-favorited episode is a no-op success, not a duplicate error (client-friendly idempotency for optimistic UI).
- `FavoriteService.list_favorites(child_id)`: joins against `story_episode` to attach current withdrawal status; if a favorited episode's canonical content ID has changed due to admin restructuring (per B-11's content-merge workflow), resolve to the new ID transparently rather than surfacing a broken reference.
- `FavoriteService.remove_favorite(child_id, episode_id)`: idempotent — removing a non-existent favorite is a success no-op.

## 11. API Contract

### `POST /v1/favorites`
- Auth: Bearer (child-mode). Request: `{ "episode_id": "..." }`. Response 200: `{ "favorited": true }`. Errors: `404 EPISODE_NOT_FOUND`, `401 UNAUTHORIZED`.

### `DELETE /v1/favorites/{episode_id}`
- Auth: Bearer (child-mode). Response 200: `{ "favorited": false }`.

### `GET /v1/favorites`
- Auth: Bearer (child-mode). Response 200: paginated favorites list, each item annotated with `is_available: bool` (false if withdrawn) and canonical `episode_id` (resolved if restructured).

## 12. Database Requirements
- `favorite`: `UNIQUE(child_id, episode_id)`; index `(child_id)`.

## 13. Validation
- `episode_id` must reference an existing `story_episode` row (withdrawn is allowed — favoriting withdrawn content isn't possible going forward, but existing favorites of now-withdrawn content are preserved per §4.4).

## 14. Authentication
Bearer child-mode session via `get_current_child`.

## 15. Authorization
No additional RBAC beyond authenticated child session; favorites are strictly scoped to the requesting child (no cross-child visibility).

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| Duplicate favorite | No-op success, not an error |
| Remove non-existent favorite | No-op success |
| Favorited content later withdrawn | Row preserved, `is_available: false` in list response |
| Favorited content restructured/merged | Resolved transparently to new canonical ID, never a broken reference or 404 |
| Database failure | `503`, logged |

## 17. Security
No PII beyond existing child/episode references; no new security surface.

## 18. Analytics
Emit via `OutboxWriter`: `story_favorited`, `story_unfavorited`.

## 19. Performance
- `list_favorites()` is a single joined query, not N+1 lookups per favorite for availability/canonical-ID resolution.

## 20. Library Requirements
No new libraries.

## 21. Testing
- Unit: duplicate-add idempotency, remove-idempotency, withdrawn-content availability flagging.
- Integration: restructured-content resolution (favorite added pre-merge, verify it resolves to the new canonical ID post-merge, seeded against B-11's merge workflow output).

## 22. Documentation
Update OpenAPI schema.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Create `FavoriteOrm` Model & Migration**
Objective: Add the `favorite` table with the uniqueness constraint. Follow: existing SQLAlchemy/Alembic conventions. Tests: migration smoke test, unique-constraint verification. Definition of Done: clean migration.

**Task 02 — Implement `FavoriteRepository`**
Objective: Upsert-safe, idempotent-remove data access, plus a joined list query resolving withdrawal/canonical-ID state. Follow: `BaseRepository`. Tests: idempotency, joined-resolution correctness. Definition of Done: repository methods covered.

**Task 03 — Implement `FavoriteService`**
Objective: Business logic wrapping the repository with the idempotency and resolution guarantees. Dependencies: Task 01–02. Tests: all §21 unit cases. Definition of Done: tests pass.

**Task 04 — Add Router Endpoints**
Objective: Wire the three endpoints into `ContentRouter`. Tests: covered by Task 05. Definition of Done: endpoints live, documented.

**Task 05 — Add Unit & Integration Tests**
Objective: Full coverage per §21, including the restructured-content resolution integration test. Definition of Done: all green in CI.

**Task 06 — Update OpenAPI Documentation**
Objective: Regenerate/diff-classify. Definition of Done: non-breaking diff confirmed.

**Task 07 — Final Code Review**
Objective: Confirm no favorite ever silently breaks/404s after admin content restructuring. Definition of Done: checklist in §24 fully checked.

## 24. Final Verification Checklist
- [ ] Duplicate favorite add is idempotent (no error)
- [ ] Duplicate favorite remove is idempotent (no error)
- [ ] Withdrawn favorited content shows `is_available: false`, never disappears/breaks
- [ ] Restructured/merged content resolves favorites to the new canonical ID transparently
- [ ] Favorites strictly scoped per child, no cross-child leakage
- [ ] No PostgreSQL/Redis credentials modified

## 25. Definition of Done
Favorites are durable, idempotent, and resilient to both content withdrawal and content restructuring — never presenting a broken reference to the child.
