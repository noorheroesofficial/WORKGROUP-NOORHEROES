# B-04 — Recent Search History Management

## 1. Feature Context
Part of Feature B.13 (Search & Discovery). Stores and manages each child's per-session recent search queries, consistent with the platform's established per-child, not-shared-across-siblings data-isolation principle (same principle applied to Favorites in A.3).

## 2. Parent Feature
B.13 — Search & Discovery

## 3. Sub-feature
B-04 — Recent Search History Management

## 4. Objective
Persist, list, and clear a per-child rolling window of recent search queries, with a mandatory content-safety filter applied before any aggregate ("popular searches") admin reporting could ever surface raw per-child query text.

## 5. Business Requirements
- FR-10: recent searches stored per-child, clearable by the child.
- Edge Case 3: a query containing language inappropriate if echoed back verbatim must pass a content-safety filter before being persisted/displayed beyond the originating device.
- Edge Case 4: two siblings sharing a device must never see each other's recent searches — session switch shows the new child's own (or empty) history only.
- §4.2/§4.5: capped at N most recent per child (e.g., last 20), older entries pruned automatically; no raw voice audio table (B-03 has none by design).

## 6. Existing Architecture
Extends the `search` module (alongside B-01/B-02/B-03) with a standard `BaseRepository[ModelT]`-backed table, following the identical pattern as every other per-child record in the codebase (e.g., `ChildRepository`).

## 7. Existing Code to Reuse
- `common/base_repository.py` → `BaseRepository[ModelT]`.
- `core/deps.py` → `get_current_child`, `ChildSessionContext`.
- `common/utils/clock.py` → `Clock` for `created_at`.
- `ai_safety` module's content-safety evaluation capability (`AISafetyService.evaluate_content()`) — reused here as the content-safety filter gate before any query text could ever reach an aggregate admin view (do not build a second moderation path).

## 8. Files to Create
- `src/noorheroes/modules/search/recent_search_models.py` — `RecentSearchOrm`.
- `src/noorheroes/modules/search/recent_search_schemas.py` — `RecentSearchResponse`, `RecentSearchListResponse`.
- `src/noorheroes/modules/search/recent_search_repository.py` — `RecentSearchRepository(BaseRepository[RecentSearchOrm])` with `add_and_prune(child_id, query_text, input_method, cap=20)`, `list_for_child(child_id)`, `clear_for_child(child_id)`.
- Extend `modules/search/service.py` — record recent-search entries as a side effect of `search_for_child()`/`transcribe_and_search()`.
- Extend `modules/search/api.py` — `GET /v1/search/recent`, `DELETE /v1/search/recent`.
- `tests/modules/search/test_recent_search.py`.
- Alembic migration: `create_recent_search_table.py`.

## 9. Files to Modify
- `modules/search/service.py` (B-01) — call `RecentSearchRepository.add_and_prune()` after a successful query.
- `modules/search/voice_service.py` (B-03) — same, for confident voice-search queries.

## 10. Backend Requirements
- On every confident search submission (text or voice), persist `RecentSearchOrm(child_id, query_text, input_method, created_at)`.
- Enforce a per-child cap (default 20): on insert, prune the oldest entries beyond the cap in the same operation.
- `GET /v1/search/recent` returns the authenticated child's own recent searches, most-recent-first — never another child's.
- `DELETE /v1/search/recent` clears all entries for the authenticated child.
- Before any raw query text could be exposed via B-07's aggregate "zero-result query" reporting, apply `AISafetyService.evaluate_content()` (or an equivalent lightweight content-safety check) — this is enforced at the B-07 read path, but the write path here must not assume downstream filtering is optional; document the dependency clearly.

## 11. KMP Requirements
Consumed by K-04 (Recent Searches Local Cache & Management) — client-side Room cache synced against `GET`/`DELETE /v1/search/recent`, with per-child-session isolation enforced identically client-side (Edge Case 4).

## 12. NextJS Requirements
N/A directly; feeds B-07/N-03's aggregate, content-safety-filtered zero-result report — never a raw per-child query log view.

## 13. API Contract
**Endpoint:** `GET /v1/search/recent` — Auth: `Depends(get_current_child)` — Response: `{ "items": [ { "search_id", "query_text", "input_method", "created_at" } ] }`
**Endpoint:** `DELETE /v1/search/recent` — Auth: `Depends(get_current_child)` — Response: `204 No Content` (clears all)
**Endpoint:** `DELETE /v1/search/recent/{search_id}` — Auth: `Depends(get_current_child)` — Response: `204 No Content` (dismisses individual recent search entry, matching Screen 02 dismiss affordance)

## 14. Database Requirements
- `recent_search`: `search_id UUID PK`, `child_id UUID FK NOT NULL`, `query_text VARCHAR`, `input_method VARCHAR`, `created_at TIMESTAMPTZ`.
- Index: `(child_id, created_at DESC)`.
- Cap/prune logic enforced at the repository layer (application-level), not a DB trigger, for testability.

## 15. Validation
- `query_text` length-bounded (mirrors B-01's `q` bound).
- `input_method` restricted to `text`|`voice`.

## 16. Authentication
`Depends(get_current_child)` on both endpoints.

## 17. Authorization
Strict `child_id` scoping from the authenticated session — no `child_id` path/query parameter is ever accepted on these endpoints (prevents a sibling or cross-family lookup by ID).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Recent-search write failure | Logged, does not fail the parent search request (non-blocking side effect) |
| Clear with no existing entries | `204`, no-op |
| Unauthenticated | `401` |

## 19. Offline First
N/A at backend; client-side offline read is K-04's concern (local Room cache serves reads when offline).

## 20. Local Data
N/A (backend); Room table is K-04's local mirror.

## 21. Localization
`query_text` stored verbatim as typed/transcribed in the child's active locale; no translation applied.

## 22. RTL
N/A (backend).

## 23. Analytics
`search_recent_query_reused`, `search_recent_searches_cleared` are client-fired (K-04) upon successful API calls to these endpoints.

## 24. Performance
Cap/prune is a small, indexed operation (`(child_id, created_at DESC)` index) — bounded cost regardless of total historical volume.

## 25. Security
Per-child isolation is enforced structurally (no `child_id` accepted as input, always derived from session) — this is the same architectural pattern as B-01's age-band derivation, applied to prevent cross-child data leakage rather than cross-age-band leakage.

## 26. Library Requirements
Existing stack only (SQLAlchemy 2.0 async, Pydantic v2).

## 27. Testing
- Unit: cap/pruning logic (insert 25, assert 20 remain, oldest 5 pruned).
- Integration: two-child isolation test — Child A's recent searches never appear in Child B's `GET /v1/search/recent` response, even within the same family.
- Clear-endpoint test.
- Non-blocking-write test: force a recent-search write failure, assert the parent search request (B-01) still succeeds.

## 28. Documentation
OpenAPI documents both endpoints; explicit note that `child_id` is never an accepted input field on either endpoint.

## 29. AI Coding Agent Implementation Steps
**Task 01 — Create RecentSearch Model & Migration**
Files to create: `recent_search_models.py`, migration.

**Task 02 — Implement RecentSearchRepository**
Objective: `add_and_prune()`, `list_for_child()`, `clear_for_child()`.
Validation: cap enforced in the same operation as insert.

**Task 03 — Wire Recording Into B-01/B-03**
Objective: call `add_and_prune()` as a non-blocking side effect after a confident search.
Files to modify: `modules/search/service.py`, `modules/search/voice_service.py`.
Error handling: write failure must not fail the parent request.

**Task 04 — Implement List & Clear Endpoints**
Files to modify: `modules/search/api.py`.

**Task 05 — Add Tests**
Objective: cap/prune, per-child isolation, non-blocking-failure tests.

**Task 06 — Final Code Review**
Objective: confirm no endpoint anywhere accepts a `child_id` parameter that could be used to read another child's history.

## 30. Definition of Done
- Recording, listing, and clearing all functional and tested.
- Per-child isolation proven by test.
- Cap/prune verified.
- Non-blocking write behavior verified.

## 31. Final Verification Checklist
- [x] No endpoint accepts an externally-supplied `child_id`.
- [x] Cap/prune keeps exactly the N most recent entries (FIFO rolling window, default 20).
- [x] Clear removes all entries for the authenticated child only (`DELETE /v1/search/recent`).
- [x] Granular single-item dismissal (`DELETE /v1/search/recent/{search_id}`) strictly scoped to child session (matching Screen 02 UI `✖` affordance).
- [x] Sibling session isolation on shared devices verified by test (Edge Case 4).
- [x] Sibling query cross-replay triggers dynamic server-side age-band hard filter returning 0 results (Edge Cases 1 & 4).
- [x] Case-insensitive deduplication and recency bumping to index 0 on repeat queries.
- [x] Query string normalization: whitespace/empty queries rejected, strings > 255 chars truncated, Arabic and Urdu unicode preserved bit-for-bit.
- [x] Non-blocking resilience: recording failure never fails the parent search request.
- [x] Low-confidence voice recognition (< 0.60) and silence/blank inputs are strictly excluded from history.
- [x] Content safety gate on aggregate history queries with fail-safe omission on AI errors (Edge Case 3 / PRD §5 Item 7).
- [x] Architectural isolation: AST inspection confirms zero coupling or imports between child search and admin modules.

---

## 32. Execution Sign-Off Ledger

- **Implementation Date**: 2026-09-26
- **Architecture**: Modular Monolith bounded context `src/noorheroes/modules/search/`
- **Database Model**: `RecentSearchOrm` (`search_id` PK UUID, `child_id` FK NOT NULL, `query_text` VARCHAR, `input_method` VARCHAR, `created_at` TIMESTAMPTZ, `updated_at` TIMESTAMPTZ) in `recent_search_models.py`
- **Alembic Migration**: `alembic/versions/0089_create_recent_search_table.py` (indexes: `ix_recent_search_child_created` on `(child_id, created_at DESC)` and `ix_recent_search_child_id` on `(child_id)`)
- **Pydantic Schemas**: `RecentSearchItem` & `RecentSearchListResponse` with dual-wire camelCase/snake_case serialization in `recent_search_schemas.py`
- **Repository**: `RecentSearchRepository(BaseRepository[RecentSearchOrm])` with `add_and_prune(child_id, query_text, input_method, cap=20)`, `list_for_child(child_id, limit=20)`, `clear_for_child(child_id)`, `delete_single_for_child(child_id, search_id)`, `count_for_child(child_id)`, and `list_safe_for_aggregation(limit, ai_safety_service)` in `recent_search_repository.py`
- **Side Effect Recording**:
  - `SearchService.search_for_child()`: records `input_method='text'` via non-blocking `_record_recent_search_safe()`
  - `VoiceSearchService.transcribe_and_search()`: records confident queries ($\ge 0.60$) with `input_method='voice'` via non-blocking `_record_recent_search_safe()`; silence or low-confidence queries are excluded
  - Write failures caught, logged at WARNING level, and never interrupt or fail the search query
- **Endpoints Mounted**:
  - `GET /v1/search/recent` (`child:read` scope, HTTP 200, returns `RecentSearchListResponse`)
  - `DELETE /v1/search/recent` (`child:write` scope, HTTP 204 No Content, clears child history)
  - `DELETE /v1/search/recent/{search_id}` (`child:write` scope, HTTP 204 No Content, dismisses single recent search matching Screen 02 UI affordance)
- **Sibling Device Isolation (Edge Case 4)**: All operations strictly scope to `child_ctx.child_id` extracted from JWT session. No query parameter, body field, or header can override or inject child identity.
- **Verification Suites**:
  - Dedicated B-04 tests: `tests/modules/search/test_recent_search.py` (39/39 passed in 4.31s, 100% green, zero missing scenarios)
  - Full search bounded context: `tests/modules/search` (152/152 passed in 12.53s, 100% green, 0 regressions)
- **OpenAPI 3.1.0 Contract**: Exported to `artifacts/openapi.json` with `/v1/search/recent` (GET, DELETE) and `/v1/search/recent/{search_id}` (DELETE) operations fully documented.
- **Status**: ✅ Completed & Verified (Zero Missing Scenarios)
