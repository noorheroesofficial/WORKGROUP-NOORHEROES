# B-06 — Item Ownership Distribution Analytics API

## 1. Feature Context
NoorHeroes Backend (FastAPI). Part of Feature A.12 — Avatar System. Read-only aggregate analytics endpoint surfacing how many children own vs. have equipped a given `avatar_item`, used as a content-popularity signal for future asset investment (PRD §8, §11.3).

## 2. Parent Feature
A.12 Avatar System — Backend (FastAPI)

## 3. Sub-feature
B-06 Item Ownership Distribution Analytics API

## 4. Objective
Implement `GET /v1/admin/avatar-items/{itemId}/ownership-distribution` returning aggregate owned/equipped counts, never individual child identities, backing PRD §8's "Read ownership distribution... a content-popularity signal" and §11.3 Dashboard Metrics.

## 5. Business Requirements
- Aggregate-only response — never lists individual child identities (privacy-by-design, mirroring the platform's Family Board "combined progress only, never per-sibling breakdown" principle applied here to per-item ownership).
- Read-only; this sub-feature introduces no mutating action.
- Supports the "most/least-popular equipped items" and "locked-item-teaser engagement rate by unlock-criteria-type" dashboard metrics (PRD §11.3) at the per-item level; cross-item/cohort aggregation is a NextJS/dashboard-layer concern (N-04), not re-implemented here.

## 6. Existing Architecture
Extends the `avatars` bounded context established in B-01. Follows the existing Admin read-only aggregate pattern (mirrors `RewardsRouter`'s balance-aggregation style query, per `FAST-API-INSTRUCTIONS.md` §5.9, adapted from "sum of ledger entries for one child" to "count of `child_inventory` rows for one item").

## 7. Existing Code to Reuse
- `ChildInventory` model (B-01)
- `get_current_admin`/`require_admin_scope()` (`core/deps.py`)
- Redis pool accessor pattern (`localization` context) — reused here for aggregate-query caching

## 8. Files to Create
- `src/noorheroes/modules/avatars/analytics_schemas.py` (`OwnershipDistributionResponse`)
- `src/noorheroes/modules/avatars/analytics_api.py` (`AvatarAnalyticsRouter`)
- `tests/modules/avatars/test_ownership_distribution_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/avatars/repository.py` — add `get_ownership_distribution(item_id)` (aggregate `COUNT(*)` and `COUNT(*) FILTER (WHERE equipped)` grouped by `avatar_item_id`)
- `main.py` — register `AvatarAnalyticsRouter`

## 10. Backend Requirements
- Single aggregation query per item: total owned count, total currently-equipped count — no per-child row ever included in the response payload.
- Cached via short-to-medium-TTL Redis (aggregate counts don't need real-time precision), invalidated opportunistically or left to TTL expiry given the low-stakes nature of a popularity signal.
- Query must avoid N+1 (single grouped aggregate query against the indexed `(child_id, equipped)`/`avatar_item_id` columns from B-01, not a per-child loop).

## 11. KMP Requirements
Not applicable — admin-only surface.

## 12. NextJS Requirements
Not applicable directly; consumed by N-04's Item Ownership Distribution Dashboard.

## 13. API Contract

**Required API**
- **HTTP Method:** GET
- **Endpoint:** `/v1/admin/avatar-items/{itemId}/ownership-distribution`
- **Request:** none (path param `itemId`)
- **Response 200:** `{ "item_id": "uuid", "owned_count": 1245, "equipped_count": 312 }`
- **Authentication:** Bearer, admin session (`get_current_admin`)
- **Authorization:** `content_editor` or `trust_safety` scope
- **Validation:** `itemId` must reference an existing `avatar_items` row
- **Error Responses:** `401`; `403`; `404` unknown item; `500`

## 14. Database Requirements
Reads `child_inventory` (B-01) — no new tables, no new columns. Relies on existing `(child_id)`/`(child_id, equipped)` indexes; if per-item aggregate query volume warrants it, an additional index on `(avatar_item_id)` may be added in this task's migration (not present in B-01's original index set, which was optimized for per-child lookups rather than per-item aggregation).

## 15. Validation
- Reject requests for a non-existent `itemId` with `404`.
- Confirm via a dedicated test that the response schema structurally cannot include a child identifier field (schema-level guarantee, not just a runtime check).

## 16. Authentication
Bearer JWT, admin session via `get_current_admin`.

## 17. Authorization
`content_editor` or `trust_safety` scope required.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Unknown `itemId` | `404` |
| Zero owners (newly-created item) | Return `{ "owned_count": 0, "equipped_count": 0 }`, not an error |
| Database failure | `500`/`503`, cached last-known aggregate preferred over hard failure where a cache entry exists |
| Unauthorized/forbidden request | `401`/`403` |

## 19. Offline First / 20. Local Data
N/A (backend, admin-only, online-by-design surface).

## 21. Localization / 22. RTL
N/A (numeric aggregate response only).

## 23. Analytics
This endpoint *is* an analytics surface (§11.3 Dashboard Metrics); it does not itself emit further analytics events.

## 24. Performance
Indexed aggregate query (§14); Redis caching to keep repeated admin-dashboard polling cheap, per the platform's general "cache aggregate reads, never cache mutating writes" convention.

## 25. Security
Aggregate-only response is the primary privacy control — no individual child identity is queryable through this endpoint by design, verified by a structural schema test (§15) rather than relying solely on manual review.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 (async), Pydantic v2, Redis (existing pool).

## 27. Testing
- Unit: `get_ownership_distribution()` aggregation correctness against fixture `child_inventory` rows.
- Integration: full request → response for an item with owners, an item with zero owners, an unknown item (`404`).
- Schema-scan: assert `OwnershipDistributionResponse` contains no child-identifying field.
- Performance: confirm the aggregate query is a single round trip (no N+1) under a fixture set of 1000+ `child_inventory` rows for one item.

## 28. Documentation
OpenAPI documentation for the endpoint; update the `avatars` context entry in `FAST-API-INSTRUCTIONS.md`.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement `get_ownership_distribution` Repository Method**
- Task ID: B-06-T01
- Objective: single grouped aggregate query returning owned/equipped counts for one `item_id`.
- Existing Architecture to Follow: `BaseRepository[ModelT]` query-method convention.
- Files to Modify: `src/noorheroes/modules/avatars/repository.py`
- Performance: single query, indexed; add `(avatar_item_id)` index in this task's migration if not already sufficiently covered.
- Tests: unit test against fixture data with known counts.
- Definition of Done: correct counts for populated and empty fixtures.

**Task 02 — Define `OwnershipDistributionResponse` Schema**
- Task ID: B-06-T02
- Objective: strictly-typed aggregate-only response schema.
- Files to Create: `src/noorheroes/modules/avatars/analytics_schemas.py`
- Tests: schema-scan test confirming no child-identifying field exists.
- Definition of Done: schema matches §13 contract exactly.

**Task 03 — Implement the Endpoint**
- Task ID: B-06-T03
- Objective: wire `AvatarAnalyticsRouter` with RBAC and optional Redis caching.
- Files to Create/Modify: `src/noorheroes/modules/avatars/analytics_api.py`; modify `main.py`.
- Authentication/Authorization: `Depends(get_current_admin)` + `require_admin_scope(...)`.
- Error Handling: per §18 table.
- Tests: integration tests per §27.
- Definition of Done: endpoint live, documented, auth-enforced, cached.

**Task 04 — Add Full Test Suite & Documentation**
- Task ID: B-06-T04
- Files to Create: `tests/modules/avatars/test_ownership_distribution_api.py`
- Documentation: OpenAPI + `FAST-API-INSTRUCTIONS.md` update.
- Definition of Done: suite green, docs complete.

**Task 05 — Final Code Review**
- Task ID: B-06-T05
- Do Not Change: `child_inventory` table structure beyond the optional new index; PostgreSQL/Redis credentials.
- Expected Result: PR merge-ready, CI green.

## 30. Definition of Done
`GET /v1/admin/avatar-items/{itemId}/ownership-distribution` live, authenticated, authorized, tested, documented, returning aggregate-only counts with zero individual child identities ever exposed.

## 31. Final Verification Checklist
- [ ] Aggregate query returns correct owned/equipped counts, single round trip, indexed
- [ ] Response schema structurally excludes any child-identifying field (schema-scan test passing)
- [ ] Unknown item returns `404`; zero-owner item returns zero counts, not an error
- [ ] Redis caching implemented with sensible TTL
- [ ] Unit + integration tests passing
- [ ] OpenAPI documentation complete
- [ ] No PostgreSQL/Redis credential changes
- [ ] No unrelated existing-context code modified
