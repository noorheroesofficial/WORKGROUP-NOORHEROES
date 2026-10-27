# B-05 — Parent Area Search API

## 1. Feature Context
Part of Feature B.13 (Search & Discovery). A distinct, parent-session-scoped search surface allowing a parent to search their own family's child reports, stories, and habits — architecturally and structurally separate from B-01 (child search) and B-06 (admin search).

## 2. Parent Feature
B.13 — Search & Discovery

## 3. Sub-feature
B-05 — Parent Area Search API

## 4. Objective
Implement `GET /v1/parent/search` as an entirely separate endpoint/code path from `GET /v1/search`, scoped exclusively to the authenticated parent's own `family_id`, with zero code path touching the general content-catalog search index (`search_index_entry`).

## 5. Business Requirements
- FR-11: parent-facing search surface within the Parent Area, distinct from child search, scoped to parent-session-authenticated data only.
- Acceptance Criteria: results scoped only to the parent's own family — never another family's data, never the unrestricted Admin search surface.
- Edge Case 9: query terms that happen to match general-catalog content terms must not resolve against the catalog — Parent Area search is scoped strictly to the family's own reports/progress/habit data.
- §5 item 5 (PRD backend prompt): entirely separate endpoint/service from `GET /v1/search`; a parent's request can never return another family's data; no code path touches the general content catalog search index at all.

## 6. Existing Architecture
New endpoint inside the `search` module, but implemented with **zero dependency on `SearchRepository`/`search_index_entry`** (B-01/B-02's components) — it queries `learning` (`QuizAttemptRepository`, `LearningProgressResponse` source data), `rewards`, and any habit-tracking repository directly, scoped by `family_id`, following the same repository-composition pattern already used elsewhere (e.g., `LearningService` composing multiple repositories).

## 7. Existing Code to Reuse
- `core/deps.py` → `get_current_parent`, `ParentSessionContext` (`family_id`).
- `learning` module's `QuizAttemptRepository.get_child_progress()` — reused for progress/report matches.
- `identity` module's `ChildRepository.get_by_family_id()` — to resolve which children's records are in-scope for the search.
- Habit-tracking repository (A.7 — Habit Tracker/`Habit OS` backend context, per its own blueprint) for habit-record matches.

## 8. Files to Create
- `src/noorheroes/modules/search/parent_search_schemas.py` — `ParentSearchResultItem`, `ParentSearchResponse`.
- `src/noorheroes/modules/search/parent_search_service.py` — `ParentSearchService(BaseService)` with `search_family_data(parent_ctx, query) -> ParentSearchResponse` — a standalone class with **no import of `SearchService`/`SearchRepository`**.
- Extend `modules/search/api.py` — `GET /v1/parent/search` route.
- `tests/modules/search/test_parent_search_api.py`.
- `tests/modules/search/test_parent_search_isolation.py`.

## 9. Files to Modify
- `modules/search/deps.py` — add `get_parent_search_service` factory.

## 10. Backend Requirements
- `GET /v1/parent/search?q=`, `Depends(get_current_parent)` — `family_id` derived from `ParentSessionContext`, never from a query/path parameter.
- Query fans out (in parallel or sequential composed calls) to: child progress/report data (`learning`), habit records (A.7's habit repository), and reward/points summaries if relevant to the query — all filtered by the resolved `family_id`.
- Response items are typed by source (`report`|`story_activity`|`habit`) with a link/reference back to the relevant detail screen.
- Zero results → `200`, empty array — same graceful pattern as B-01.

## 11. KMP Requirements
Consumed by the existing Parent Area module's search entry point (an existing surface per the PRD's screen inventory — `Parent Area Search`); this blueprint does not create new KMP screens, only the backend contract it calls.

## 12. NextJS Requirements
N/A — this is a **User API** (parent-facing), not an Admin API; do not confuse with B-06.

## 13. API Contract
**Endpoint:** `GET /v1/parent/search`
**Auth:** Bearer, parent-mode (`Depends(get_current_parent)`)
**Query Params:** `q: str`
**Response 200:**
```json
{ "results": [ { "source_type": "habit", "child_id": "...", "title": "...", "reference_id": "..." } ], "result_count": 3 }
```
**Error Responses:** `401` unauthenticated/non-parent token, `422` missing `q`.

## 14. Database Requirements
No new tables — reads existing `learning`, `rewards`, and habit-tracking tables, all already scoped by `family_id`/`child_id` foreign keys.

## 15. Validation
`q` required, length-bounded, same pattern as B-01.

## 16. Authentication
`Depends(get_current_parent)` — rejects child-mode or admin-mode tokens.

## 17. Authorization
`family_id` exclusively server-derived from `ParentSessionContext`; the query composition layer must filter every underlying repository call by this `family_id` — no underlying query is permitted to run unscoped.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Zero results | `200`, empty array |
| Unauthenticated/wrong session mode | `401` |
| One of the fanned-out source repositories fails | Partial results returned from the sources that succeeded, logged, not a hard `500` (graceful degradation, consistent with platform philosophy) |

## 19. Offline First
N/A (backend); Parent Area's existing offline handling (if any) is out of this blueprint's scope.

## 20. Local Data
N/A.

## 21. Localization
Result titles/labels returned in the parent's active locale, consistent with existing report/progress endpoints.

## 22. RTL
N/A (backend).

## 23. Analytics
`parent_search_performed` — fired client-side on successful call to this endpoint.

## 24. Performance
Fan-out queries should be issued concurrently (async `asyncio.gather`-style) rather than sequentially, bounded by the number of source repositories (small, fixed count).

## 25. Security
**This endpoint's defining guarantee is architectural isolation from B-01.** No import, call, or shared query-building function exists between `ParentSearchService` and `SearchService`/`SearchRepository` — verified by the same module-dependency-graph test pattern used for B-06's isolation from B-01.

## 26. Library Requirements
Existing stack only.

## 27. Testing
- Unit: `family_id` scoping applied to every fanned-out repository call.
- Integration: **cross-family isolation test** — Family A's parent query never returns Family B's data, even with identical query text.
- **Architectural separation test:** module-dependency-graph check confirming `parent_search_service.py` has zero import of `modules/search/service.py`/`repository.py` (B-01's components).
- Partial-failure graceful-degradation test.

## 28. Documentation
OpenAPI documents this as a distinct, family-scoped endpoint; explicit note distinguishing it from `GET /v1/search` (child) and `GET /admin/v1/search` (admin).

## 29. AI Coding Agent Implementation Steps
**Task 01 — Define Parent Search Schemas**
Files to create: `parent_search_schemas.py`.

**Task 02 — Implement ParentSearchService (Isolated)**
Objective: fan-out query composition across `learning`/habit/`rewards` repositories, strictly `family_id`-scoped.
Do not change: import nothing from B-01's `SearchService`/`SearchRepository`.
Files to create: `parent_search_service.py`.

**Task 03 — Implement API Endpoint**
Files to modify: `modules/search/api.py`, `modules/search/deps.py`.

**Task 04 — Add Cross-Family Isolation Test**
Files to create: `test_parent_search_isolation.py`.

**Task 05 — Add Architectural Separation Test**
Objective: module-dependency-graph check, same pattern as B-06's Task in that blueprint.

**Task 06 — Add Full Test Suite & Docs**

**Task 07 — Final Code Review**
Objective: confirm zero shared query function with B-01; confirm `family_id` never accepted as client input.

## 30. Definition of Done
- Endpoint live, matches §13 contract.
- Cross-family isolation proven by test.
- Architectural separation from B-01 proven by test.

## 31. Final Verification Checklist
- [x] `family_id` always server-derived, never client-supplied.
- [x] Zero shared code path with B-01 (`GET /v1/search`).
- [x] Zero shared code path with B-06 (`GET /admin/v1/search`).
- [x] Cross-family data leakage impossible — verified by test.
- [x] Partial source-repository failure degrades gracefully, not a hard 500.

## 32. Verification and Test Results
- **Implementation Status:** COMPLETE & VERIFIED
- **Schema File:** `src/noorheroes/modules/search/parent_search_schemas.py`
- **Service File:** `src/noorheroes/modules/search/parent_search_service.py`
- **Dependency Factory:** `src/noorheroes/modules/search/deps.py` (`get_parent_search_service`)
- **Route Mounted:** `src/noorheroes/modules/search/api.py` (`GET /v1/parent/search`)
- **Automated Tests:**
  - `tests/modules/search/test_parent_search_api.py` (16 tests passed, including multilingual Arabic, inactive habits, boundary limits, and relevance ranking)
  - `tests/modules/search/test_parent_search_isolation.py` (7 tests passed, including AST import isolation verification)
  - Total Parent Search Tests: 23 tests passed (100% green)
  - Full module regression suite: `pytest tests/modules/search` (175 tests passed, 100% green)
- **OpenAPI Schema:** Exported to `artifacts/openapi.json` with endpoint `GET /v1/parent/search`.
