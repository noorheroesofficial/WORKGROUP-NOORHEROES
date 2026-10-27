# B-04 — Admin Favoriting Pattern Monitor API

## 1. Feature Context
Part of Feature B.14 Favorites. Read-only, aggregate-only reporting endpoint giving Content/Editorial a privacy-safe view of platform-wide favoriting patterns.

## 2. Parent Feature
B.14 Favorites (`PRD_Documents/Child App — Supporting (13-18)/Feature_B14_Favorites.md`)

## 3. Sub-feature
1.4 Admin Favoriting Pattern Monitor API — `B-04`

## 4. Objective
Provide `GET /admin/v1/favorites/pattern-report`, an aggregate, per-child-anonymous report of most/least favorited content, filterable by content type and date range, for the NextJS Favoriting Pattern Monitor Dashboard (N-01).

## 5. Business Requirements
- PRD §8: "Aggregate, privacy-safe (never per-child) reporting on which content items are most/least frequently favorited platform-wide — a content-curation signal for editorial."
- PRD §9 (Admin AI Code-Generation Prompt): "NEVER exposes any per-child favorite list or identity — only aggregate counts per `content_id`."
- CRUD permissions: read-only behind `content_editor` role; no mutation capability on this endpoint.

## 6. Existing Architecture
Admin endpoints live under the `admin` bounded context / an `admin/v1` route prefix, gated by `Depends(get_current_admin)` and `require_admin_scope(scope)` per the researched auth pattern. `content_editor` is an established role already used in other admin surfaces (confirmed via B.13's NextJS blueprints).

## 7. Existing Code to Reuse
- `core/deps.py::get_current_admin`, `require_admin_scope`
- `favorite` table (canonical shape, post-B-03) — read-only aggregate query, no new table
- Existing admin reporting/aggregation query patterns if present elsewhere in the `admin` module (confirm exact precedent before implementation — not independently verified in this pass)

## 8. Files to Create
- `src/noorheroes/modules/admin/favorites_report_schemas.py` — `FavoritingPatternReportResponse`
- `tests/modules/admin/test_favorites_pattern_report_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/admin/api.py` (or equivalent admin router) — add `GET /admin/v1/favorites/pattern-report`
- `src/noorheroes/modules/content/favorite_repository.py` — add an aggregate query method (e.g. `count_by_content(content_type, date_range)`), reusing the same repository as B-01/B-02 rather than duplicating query logic

## 10. Backend Requirements
- Aggregate `COUNT(*)` grouped by `content_id`/`content_type`, filterable by `content_type` and a date range on `favorite.created_at`.
- Response must never include `child_id` or any per-child breakdown.
- Read-only — no corresponding write/mutation endpoint exists or should be added under this blueprint.

## 11. KMP Requirements
None — admin-only feature.

## 12. NextJS Requirements
Consumed by N-01. Contract only in this blueprint.

## 13. API Contract
**Required API:** Favoriting Pattern Report (Admin, read-only)
**HTTP Method:** `GET`
**Endpoint:** `/admin/v1/favorites/pattern-report`
**Request:** query params `content_type` (optional), `date_from`/`date_to` (optional)
**Response 200:** aggregate list of `{content_id, content_type, favorite_count}` — **exact response field names/pagination shape are not specified in the PRD** beyond "aggregate counts per content_id"; confirm the precise contract with the Admin API owner before implementation rather than inventing field names here.
**Authentication:** Admin bearer.
**Authorization:** `content_editor` role required.
**Validation:** `content_type` allowlist if provided; `date_from` ≤ `date_to` if both provided.
**Error Responses:** `401` unauthorized, `403` forbidden (wrong/missing role), `422` invalid filter params.

*Contract source: PRD §8/§9. This is flagged as a partial contract — do not proceed to implementation without confirming the exact response schema, consistent with rule 17's "do not invent API fields."*

## 14. Database Requirements
Read-only query against `favorite` table (post-B-03 canonical shape). Recommend a covering index on `(content_type, content_id)` if aggregate queries prove slow at scale — evaluate against actual table size before adding, not pre-emptively.

## 15. Validation
`content_type` allowlist; date range sanity check.

## 16. Authentication
Admin bearer JWT via `Depends(get_current_admin)`.

## 17. Authorization
`require_admin_scope("content_editor")` or equivalent role check — read-only scope, no write scope should be attached.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Unauthorized admin request | `401` |
| Wrong admin role | `403` |
| Invalid filter params | `422` |
| Database failure | `500`, logged, no partial/inconsistent aggregate returned |

## 19. Offline First
N/A (admin web context).

## 20. Local Data
N/A.

## 21. Localization
Admin Portal localization scope not specified in this PRD — confirm whether NextJS Admin is EN-only before assuming any localization requirement here (not assumed).

## 22. RTL
Same as above — not specified, confirm before assuming.

## 23. Analytics
No dedicated analytics event specified in the PRD for this admin endpoint; standard admin-access audit logging applies if the platform has one (not independently verified — no mutation occurs, so PRD §9 explicitly states "No audit logging needed for this page since it performs no mutating actions").

## 24. Performance
Aggregate query over potentially large `favorite` table — ensure it's indexed and does not do a full sequential scan; avoid recomputing on every request if traffic to this admin page is frequent (short-TTL cache is a reasonable future optimization, not required by the PRD at this stage).

## 25. Security
Zero per-child data exposure is the defining security property of this endpoint (PRD §12.5). No secrets touched. Do not modify PostgreSQL/Redis credentials.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 (async), Pydantic v2.

## 27. Testing
- Unit: aggregation correctness (counts match known fixture data).
- Unit: response never contains a `child_id` field or per-child array under any input.
- Integration: `content_editor` role required; other roles rejected.
- Integration: filter by `content_type` and date range narrows results correctly.

## 28. Documentation
OpenAPI schema for the endpoint; explicitly document the zero-per-child-data guarantee in the endpoint description for future maintainers.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Confirm B-03 Migration Applied.** Precondition, same as B-01/B-02.
**Task 02 — Confirm Exact Response Schema with Admin API Owner.** Do not proceed past this task on assumed field names.
**Task 03 — Add Aggregate Repository Method.** Reuse `FavoriteRepository`, do not duplicate query logic in the admin module.
**Task 04 — Add Admin Router Endpoint.** `GET /admin/v1/favorites/pattern-report`.
**Task 05 — Enforce `content_editor` Role.** Via existing `require_admin_scope` pattern.
**Task 06 — Add Filtering.** `content_type`, date range.
**Task 07 — Write Tests.** Per §27, with the zero-per-child-leakage test treated as highest priority.
**Task 08 — Update OpenAPI Documentation.**
**Task 09 — Final Code Review.** Confirm no write path was accidentally introduced.

## 30. Definition of Done
Aggregate correctness test green; zero-per-child-leakage test green; RBAC test green; OpenAPI updated; response schema confirmed against actual Admin API contract (not left as an assumption).

## 31. Final Verification Checklist
- [ ] Response contains only aggregate counts, never per-child data
- [ ] `content_editor` role enforced, read-only
- [ ] Filtering by content_type and date range functions correctly
- [ ] No mutation endpoint introduced
- [ ] Exact response schema confirmed with Admin API owner before merge
- [ ] PostgreSQL/Redis credentials untouched
