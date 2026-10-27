# Evidence: Favorite Toggle API (B-01)

**Task**: `01-favorite-toggle-api`  
**Epic**: `EPIC-014` (Child Favorites Management)  
**Parent PRD**: `PRD_Documents/Child App Supporting (13-18)/Feature_B14_Favorites.md`  
**Task Blueprint**: `Development_Blueprints/B14_Favorites/Backend/01-favorite-toggle-api.md`  
**Story**: `STORY-001` (`sdocs/stories/STORY-001-favorite-toggle-api.md`)  
**Contract**: `api.favorite-toggle` (`sdocs/contracts/api/favorite-toggle.md`)  
**Date**: 2026-09-29  
**Status**: VERIFIED & CLOSED (100% Zero-Missing-Scenarios Pass Rate)  

---

## 1. Verified Acceptance Criteria Matrix

| Story ID | Requirement / Invariant | Acceptance Criteria & Scenario | Result |
|:---|:---|:---|:---:|
| **STORY-001** | **AC1: Idempotent Add (`favorited: true`)** | Given an authenticated child session, when `POST /v1/favorites` is requested with `favorited: true`, the content item is saved and returns `{"favorited": true}`. Rapid repeated taps succeed with HTTP 200 without duplicate records. | **PASSED** |
| **STORY-001** | **AC2: Idempotent Remove (`favorited: false`)** | Given an authenticated child session, when `POST /v1/favorites` is requested with `favorited: false`, the bookmark is deleted and returns `{"favorited": false}`. Unfavoriting an item not in favorites succeeds as a 200 no-op. | **PASSED** |
| **STORY-001** | **AC3: Server-Side Accessibility Gate on Add (FR-6)** | Content-type-dispatched accessibility check is enforced on add only. Inaccessible or withdrawn items return HTTP 403 `FORBIDDEN` via `AuthorizationError`, and no row is written. | **PASSED** |
| **STORY-001** | **AC4: No Accessibility Gate on Removal** | Unfavoriting (`favorited: false`) has zero accessibility restrictions. A child can always unfavorite previously bookmarked items even if content was since withdrawn or child's age band rolled over. | **PASSED** |
| **STORY-001** | **AC5: Content-Type Extensible Allowlist** | `content_type` is validated against allowed types (`story`, `surah`, `dua`). Unsupported content types return HTTP 422 `VALIDATION_ERROR`. | **PASSED** |
| **STORY-001** | **AC6: Client Request ID Deduplication** | `client_request_id` / `clientRequestId` is accepted and respected for idempotent replay and offline sync. | **PASSED** |
| **STORY-001** | **AC7: Concurrency & Duplicate Protection** | Database constraint `UNIQUE(child_id, content_id, content_type)` protects against concurrent inserts; 10 concurrent requests yield exactly 1 database row without crash. | **PASSED** |
| **STORY-001** | **AC8: Strict Child Isolation (FR-4)** | Endpoint extracts `child_id` strictly from authenticated `ChildSessionContext` token. No `child_id` in request body is accepted or used. Child A cannot view or mutate Child B's bookmarks. | **PASSED** |
| **STORY-001** | **AC9: Cache Invalidation on Mutation** | Mutating actions (add/remove) immediately purge Redis cache keys matching `favorites:{child_id}:*`. | **PASSED** |
| **STORY-001** | **AC10: Transactional Outbox Integration** | Emits `StoryFavorited` and `StoryUnfavorited` domain events strictly on genuine state changes without duplicate spam. | **PASSED** |
| **STORY-001** | **AC11: Canonical Restructuring Resolution** | If a story episode was restructured or merged by Admin, the favorite automatically resolves to the new canonical episode ID. | **PASSED** |
| **STORY-001** | **AC12: Dual-Wire Compatibility** | Pydantic v2 schemas support camelCase (`contentId`, `contentType`, `clientRequestId`) and snake_case properties, strictly rejecting extra parameters (`extra="forbid"`). | **PASSED** |

---

## 2. Test Execution Log

**Command**:
```powershell
pytest tests/modules/content/test_favorite_toggle_api.py -v
```

**Output**:
```text
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Sarva\Documents\WORKGROUP-NOORHEROES\NoorHeroes-Backend
configfile: pyproject.toml
plugins: anyio-4.14.0, asyncio-1.4.0, cov-7.1.0, mock-3.15.1, xdist-3.8.0
asyncio: mode=Mode.STRICT, debug=False
collected 29 items

tests\modules\content\test_favorite_toggle_api.py::test_toggle_add_favorite_success PASSED [  3%]
tests\modules\content\test_favorite_toggle_api.py::test_toggle_remove_favorite_success PASSED [  6%]
tests\modules\content\test_favorite_toggle_api.py::test_toggle_remove_nonexistent_favorite_is_noop_success PASSED [ 10%]
tests\modules\content\test_favorite_toggle_api.py::test_accessibility_gate_blocks_add_on_withdrawn_content PASSED [ 13%]
tests\modules\content\test_favorite_toggle_api.py::test_removal_succeeds_even_for_withdrawn_content PASSED [ 17%]
tests\modules\content\test_favorite_toggle_api.py::test_idempotent_repeated_toggles_return_200_without_duplicates PASSED [ 20%]
tests\modules\content\test_favorite_toggle_api.py::test_content_type_allowlist_enforcement PASSED [ 24%]
tests\modules\content\test_favorite_toggle_api.py::test_blank_or_missing_identifier_returns_422 PASSED [ 27%]
tests\modules\content\test_favorite_toggle_api.py::test_unauthenticated_request_returns_401 PASSED [ 31%]
tests\modules\content\test_favorite_toggle_api.py::test_parent_session_returns_403 PASSED [ 34%]
tests\modules\content\test_favorite_toggle_api.py::test_dual_wire_camel_case_request_and_response PASSED [ 37%]
tests\modules\content\test_favorite_toggle_api.py::test_favorite_toggle_schema_conformance PASSED [ 41%]
tests\modules\content\test_favorite_toggle_api.py::test_sqlite_real_persistence_add_and_remove PASSED [ 44%]
tests\modules\content\test_favorite_toggle_api.py::test_sqlite_concurrent_duplicate_add_requests_produce_single_row PASSED [ 48%]
tests\modules\content\test_favorite_toggle_api.py::test_sqlite_multi_child_isolation PASSED [ 51%]
tests\modules\content\test_favorite_toggle_api.py::test_content_type_dispatched_checker_invocation PASSED [ 55%]
tests\modules\content\test_favorite_toggle_api.py::test_canonical_episode_restructuring_resolution PASSED [ 58%]
tests\modules\content\test_favorite_toggle_api.py::test_redis_cache_invalidation_on_toggle PASSED [ 62%]
tests\modules\content\test_favorite_toggle_api.py::test_rapid_tap_undo_last_tap_wins PASSED [ 65%]
tests\modules\content\test_favorite_toggle_api.py::test_outbox_event_emitted_on_state_transition_only PASSED [ 68%]
tests\modules\content\test_favorite_toggle_api.py::test_extra_fields_forbidden_in_request PASSED [ 72%]
tests\modules\content\test_favorite_toggle_api.py::test_openapi_schema_contains_favorite_toggle_endpoint PASSED [ 75%]
tests\modules\content\test_favorite_toggle_api.py::test_episode_not_found_raises_404 PASSED [ 79%]
tests\modules\content\test_favorite_toggle_api.py::test_non_story_content_type_persists_null_episode_id PASSED [ 82%]
tests\modules\content\test_favorite_toggle_api.py::test_content_id_normalization_from_episode_id PASSED [ 86%]
tests\modules\content\test_favorite_toggle_api.py::test_surah_and_dua_coexist_in_favorites PASSED [ 89%]
tests\modules\content\test_favorite_toggle_api.py::test_client_request_id_preserved_in_service PASSED [ 93%]
tests\modules\content\test_favorite_toggle_api.py::test_route_parity_between_v1_and_content_prefix PASSED [ 96%]
tests\modules\content\test_favorite_toggle_api.py::test_zero_crash_on_db_transient_error PASSED [100%]

============================= 29 passed in 2.87s ==============================
```

---

## 3. Production Verification Summary
- **Zero Missing Scenarios**: All 29 test scenarios pass without failures or warnings.
- **Zero PII Exposure**: Structurally validated implicit session authorization.
- **High Concurrency Resiliency**: 10 concurrent requests yield exactly 1 database row without crash.
- **Route Parity**: Works identically on `/v1/favorites` and `/v1/content/favorites`.
