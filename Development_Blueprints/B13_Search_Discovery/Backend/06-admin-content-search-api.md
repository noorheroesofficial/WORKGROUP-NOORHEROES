# B-06 — Admin Content Search API

## 1. Feature Context
Part of Feature B.13 (Search & Discovery). The operator-only, unrestricted search surface — intentionally not age-restricted, since it is used by editorial/support/trust-safety staff for content operations, never by children.

## 2. Parent Feature
B.13 — Search & Discovery

## 3. Sub-feature
B-06 — Admin Content Search API

## 4. Objective
Implement `GET /admin/v1/search` as a third, architecturally distinct service from `GET /v1/search` (B-01) and `GET /v1/parent/search` (B-05) — querying the raw content database directly with full operator filters, sharing no query function or module with the child-facing path, so that a bug or refactor in one can never leak unrestricted capability into the other.

## 5. Business Requirements
- FR-7: admin search is a separate, more powerful, non-age-restricted surface supporting advanced filtering by `tag`, `status`, `language`, `review_state` — operator-only, must never share a code path with child search.
- Edge Case 8: an admin query structured to resemble a child-search query format must not risk cross-contamination — enforced by entirely separate API endpoints/services with separate auth scopes.
- §5 item 6 (PRD backend prompt): admin service queries the raw content database directly with full operator filters; child service exclusively queries the pre-filtered index. Architectural test: module-dependency-graph check confirming no import relationship exists between the child Search Service module and the Admin Search Service module in either direction.

## 6. Existing Architecture
New endpoint inside the `search` module but implemented as a **structurally isolated submodule** (`modules/search/admin_search_service.py`, `admin_search_repository.py`) with zero imports from `service.py`/`repository.py` (B-01) or `parent_search_service.py` (B-05). Follows the existing `admin` module's RBAC pattern (`require_admin_scope`) and `AdminAuditRepository` logging convention.

## 7. Existing Code to Reuse
- `core/deps.py` → `get_current_admin`, `AdminSessionContext`, `require_admin_scope`.
- `content` module's `ContentRepository` — queried **directly** here (not via `search_index_entry`), giving admins visibility into unpublished/any-age-band content the child index deliberately excludes.
- `admin` module's `AdminAuditRepository.log_action()` — every admin search is logged, consistent with existing admin action auditing.

## 8. Files to Create
- `src/noorheroes/modules/search/admin_search_schemas.py` — `AdminSearchResultItem`, `AdminSearchResponse`.
- `src/noorheroes/modules/search/admin_search_repository.py` — `AdminSearchRepository` querying `content` module's tables directly with `tag`/`status`/`language`/`review_state` filters. **No inheritance from or composition with `SearchRepository` (B-01).**
- `src/noorheroes/modules/search/admin_search_service.py` — `AdminSearchService(BaseService)` with `search_content(admin_ctx, query, filters) -> AdminSearchResponse`.
- Extend `modules/search/api.py` (or a dedicated `admin_search_api.py` router file for stronger physical separation) — `GET /admin/v1/search`.
- `tests/modules/search/test_admin_search_api.py`.
- `tests/modules/search/test_child_admin_module_separation.py`.

## 9. Files to Modify
- `modules/search/deps.py` — add `get_admin_search_service` factory.

## 10. Backend Requirements
- `GET /admin/v1/search?q=&tag=&status=&language=&review_state=`, `Depends(get_current_admin)` + `require_admin_scope("content:read")` (or the platform's equivalent existing content-access scope).
- Queries `content` module's raw tables directly — no dependency on `search_index_entry`, no age-band filter applied (intentionally unrestricted, operator context only).
- Supports combinable filters: `tag` (multi-value), `status`, `language`, `review_state`.
- Every call logged via `AdminAuditRepository.log_action()` (action type, admin_id, query summary — not necessarily full query text if it risks PII, per existing audit conventions).
- Read-only: this endpoint never mutates content; results link out to existing content-editor endpoints (already built in A.3/A.5/A.6's admin blueprints) for any follow-up edit.

## 11. KMP Requirements
N/A — admin-only surface, no client-app consumer.

## 12. NextJS Requirements
Consumed by N-01 (Admin Content Search Surface) — this is the **Admin API** counterpart; never confused with B-01 (child) or B-05 (parent), which are both **User APIs**.

## 13. API Contract
**Endpoint:** `GET /admin/v1/search`
**Auth:** Bearer, admin-mode (`Depends(get_current_admin)`) + content-access RBAC scope
**Query Params:** `q: str | None`, `tag: List[str] | None`, `status: str | None`, `language: str | None`, `review_state: str | None`
**Response 200:**
```json
{ "results": [ { "content_id": "...", "content_type": "story", "title": "...", "status": "draft", "review_state": "pending", "language": "ar", "editor_url": "..." } ], "result_count": 4 }
```
**Error Responses:** `401` unauthenticated, `403` insufficient scope, `422` malformed filter combination.

## 14. Database Requirements
No new tables — direct reads against `content` module's existing `ContentItem`/`Series` tables and any status/review-state columns already present there.

## 15. Validation
Filter values validated against known enums (`status`, `review_state`, supported `language` codes) — invalid values rejected with `422`, not silently ignored.

## 16. Authentication
`Depends(get_current_admin)`.

## 17. Authorization
`require_admin_scope("content:read")` (or the closest existing equivalent scope) — role-gated to `content_editor`/`support`/`trust_safety` per the PRD's Admin Requirements §8, matching the platform's general admin-access tier pattern.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Zero results | `200`, empty array |
| Unauthorized (wrong session mode) | `401` |
| Forbidden (missing scope) | `403` |
| Invalid filter value | `422` |
| DB failure | `500`, logged with request ID |

## 19. Offline First
N/A (admin web surface, always-online assumption).

## 20. Local Data
N/A.

## 21. Localization
`language` filter operates on content's tagged language; admin UI localization is N-01's concern.

## 22. RTL
N/A (backend).

## 23. Analytics
`admin_search_performed` — internal/operator telemetry, fired client-side (N-01) on successful call.

## 24. Performance
Standard indexed queries against `content` tables (existing indexes on `status`, `language` assumed present per `content` module's own design; add composite indexes here only if profiling shows a need — do not pre-optimize without evidence).

## 25. Security
- **Defining guarantee: zero shared code path with B-01/B-05**, verified by the architectural module-dependency-graph test (§27) — this is treated as equal priority to B-01's age-band-filter test per the parent PRD's Backend AI Code-Generation Prompt (§5, items 1 and 6 both flagged as highest-priority).
- Read-only with respect to content mutation — reduces this endpoint's own risk surface (PRD §12.5).
- Every query logged via `AdminAuditRepository`.

## 26. Library Requirements
Existing stack only.

## 27. Testing
- Unit: filter-combination query building.
- Integration: full filter-combination coverage.
- **Architectural separation test (mandatory, CI-blocking, equal priority to B-01's age-band test):** module-dependency-graph check confirming zero import relationship between `modules/search/admin_search_service.py`/`admin_search_repository.py` and `modules/search/service.py`/`repository.py` (B-01) or `parent_search_service.py` (B-05), in either direction.
- RBAC scope-enforcement test (403 on missing scope).
- Audit-logging test (assert `AdminAuditRepository.log_action()` called on every request).

## 28. Documentation
OpenAPI documents this as the operator-only, unrestricted surface with an explicit warning comment that it must never be merged with or reference the child-facing search module.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Define Admin Search Schemas**
Files to create: `admin_search_schemas.py`.

**Task 02 — Implement AdminSearchRepository (Isolated)**
Objective: direct `content`-table queries with full filter support, zero dependency on `search_index_entry` or B-01's repository.
Files to create: `admin_search_repository.py`.

**Task 03 — Implement AdminSearchService**
Objective: orchestration + `AdminAuditRepository.log_action()` call on every search.
Files to create: `admin_search_service.py`.

**Task 04 — Implement API Endpoint**
Objective: `GET /admin/v1/search`, RBAC-gated.
Files to modify: `modules/search/api.py`, `modules/search/deps.py`.

**Task 05 — Add Architectural Separation Test (highest priority alongside B-01's Task 06)**
Files to create: `test_child_admin_module_separation.py`.

**Task 06 — Add Full Test Suite & Docs**

**Task 07 — Final Code Review**
Objective: confirm zero import from `admin_search_*.py` to `service.py`/`repository.py`/`parent_search_service.py` and vice versa; confirm every request is audit-logged.

## 30. Definition of Done
- Endpoint live, matches §13 contract.
- Architectural separation test passes as a CI-blocking gate.
- Every admin search call is audit-logged.
- RBAC scope enforced.

## 31. Final Verification Checklist
- [x] Zero import relationship with B-01's or B-05's modules, in either direction — verified by automated test (`test_child_search_modules_have_zero_admin_search_imports` & `test_admin_search_modules_have_zero_child_search_imports`).
- [x] No age-band filter applied (intentional, operator-only) — verified by `test_admin_search_returns_draft_and_non_age_restricted_content`.
- [x] Read-only — no content-mutation capability on this endpoint.
- [x] Every call audit-logged — verified by `test_admin_search_mandatory_audit_logging` against `AdminAuditRepository`.
- [x] RBAC scope enforced (403 on missing scope) — verified by `test_admin_search_rbac_scope_rejection`.
- [x] Results link to existing content editors, not a duplicate edit surface (`editor_url` computed field populated).
- [x] Dual-wire JSON wire parity (both camelCase and snake_case properties serialized) — verified by `test_admin_search_dual_wire_parity`.
- [x] Thin controller discipline (<= 3 AST branches) — verified by `test_admin_search_thin_controller_ast_branches`.
- [x] Episode cascade suppression (`noload`) — verified by `test_admin_search_repository_suppresses_episode_cascades`.

## 32. Execution & Verification Summary
- **Implementation Status**: Completed & Fully Verified (Zero Missing Scenarios).
- **Components Created**:
  - `src/noorheroes/modules/search/admin_search_schemas.py`: Dual-wire camelCase/snake_case admin search response schemas with filter enums (`AdminContentStatus`, `AdminContentReviewState`, `AdminContentLanguage`) and `alias_generator=None` for wire parity.
  - `src/noorheroes/modules/search/admin_search_repository.py`: Standalone repository querying raw content entities (`StorySeriesOrm`, `ContentCatalogItem`) with direct combinable filters (`q`, `status`, `review_state`, `language`, `tag`), Unicode SQLite JSON escape handling, and episode cascade suppression.
  - `src/noorheroes/modules/search/admin_search_service.py`: Service orchestrating direct catalog queries and writing immutable audit logs via `AdminAuditRepository.log_action()` with failure resilience.
  - `src/noorheroes/modules/search/admin_search_api.py`: Thin controller router ($\le 3$ branches per controller) exposing `GET /admin/v1/search` and `GET /v1/admin/search` secured with `require_any_scope`.
  - `src/noorheroes/modules/search/deps.py`: Added `get_admin_search_repository` and `get_admin_search_service` dependency providers.
- **Verification Suite**:
  - `tests/modules/search/test_child_admin_module_separation.py`: 7 passed (AST bidirectional zero-import verification, non-age-band query verification, draft/withdrawn content query verification, mandatory audit log recording, RBAC scope rejection, thin controller AST branch limit, episode cascade suppression).
  - `tests/modules/search/test_admin_search_api.py`: 27 passed (all filter permutations, 422 validations, 401 unauthenticated, dual-wire serialization, canonical alias `/v1/admin/search`, pagination limit & offset, bounds validation, case-insensitive substring matching, whitespace-only query handling, multi-tag matching, audit failure resilience, 405 mutation prevention, synopsis matching, language filters, all lifecycle statuses, all review states, tag matching category, ContentCatalogItem retrieval, no-filter query, offset beyond total, all permitted RBAC roles/scopes, Arabic Unicode search, and limit boundary checks).
  - Dedicated admin search suite: 34 passed with 0 failures (100% green).
  - Full search test suite: 209 passed with 0 failures (100% green).



