# Evidence: Child Favorites Listing & Type-Filtered Retrieval API (B-02)

**Task**: `02-child-favorites-listing-api`  
**Epic**: `EPIC-014` (Child Favorites Management)  
**Parent PRD**: `PRD_Documents/Child App Supporting (13-18)/Feature_B14_Favorites.md`  
**Task Blueprint**: `Development_Blueprints/B14_Favorites/Backend/02-child-favorites-listing-api.md`  
**Story**: `STORY-003` (`sdocs/stories/STORY-003-favorites-listing-api.md`)  
**Contract**: `api.favorites-listing` (`sdocs/contracts/api/favorites-listing.md`)  
**Date**: 2026-09-29  
**Status**: VERIFIED & CLOSED (100% Zero-Missing-Scenarios Pass Rate)  

---

## 1. Verified Acceptance Criteria Matrix

| Story ID | Requirement / Invariant | Acceptance Criteria & Scenario | Result |
|:---|:---|:---|:---:|
| **STORY-003** | **AC1: Own Child Session (200 OK)** | Given an authenticated child session, when `GET /v1/children/{id}/favorites` is requested with `{id}` matching the active session's child ID, returns HTTP 200 with standard `PageResult` envelope (`items`, `nextCursor`, `hasMore`). | **PASSED** |
| **STORY-003** | **AC2: Sibling Mismatch Gate (403 Forbidden)** | **CI-Blocking Signature Gate**: When `{id}` in the path does NOT match the authenticated child ID (`session.child_id`), request is strictly rejected with HTTP 403 `FORBIDDEN` ("Cannot access favorites of another child"), never silently rescoped. | **PASSED** |
| **STORY-003** | **AC3: Auth Guards (401 / 403)** | Unauthenticated requests return HTTP 401 `UNAUTHENTICATED`. Parent-mode tokens return HTTP 403 `FORBIDDEN`. | **PASSED** |
| **STORY-003** | **AC4: Type Filtering (`story`, `surah`, `dua`)** | When query parameter `type` is supplied, returns only bookmarks matching that content type. Normalized case-insensitively with whitespace trimming. | **PASSED** |
| **STORY-003** | **AC5: Invalid Type Rejection (422)** | When unsupported `type` parameter is provided (e.g. `podcast`, `video`, `quiz`), returns HTTP 422 `VALIDATION_ERROR` in the Universal Error Envelope. | **PASSED** |
| **STORY-003** | **AC6: Restructured Canonical Resolution** | When an episode was restructured into a canonical ID, listing resolves to canonical `content_id` and updated title while preserving `original_episode_id`. | **PASSED** |
| **STORY-003** | **AC7: Withdrawn Content Preservation** | Withdrawn content remains in the favorites listing with `available: false` / `is_available: false`; underlying database row is NEVER deleted. | **PASSED** |
| **STORY-003** | **AC8: Cascading Parent Series Withdrawal** | When an episode is active (`is_withdrawn: false`) but its parent series is withdrawn (`is_withdrawn: true`), resolves `available: false`. | **PASSED** |
| **STORY-003** | **AC9: Canonical Series Withdrawal** | When a canonical target episode's parent series is withdrawn, resolves `available: false`. | **PASSED** |
| **STORY-003** | **AC10: Withdrawn Dua Resolution** | Withdrawn Duas resolve to `available: false` with localized title, preserving the favorite record. | **PASSED** |
| **STORY-003** | **AC11: Orphan / Purged Content Degradation** | Missing catalog rows degrade gracefully to `available: false` with fallback title (`"Story Episode"`, `"Dua"`), never raising 500 errors. | **PASSED** |
| **STORY-003** | **AC12: Dynamic Surah Access Checker Dispatch** | Dispatches to registered surah access checkers dynamically for availability resolution. | **PASSED** |
| **STORY-003** | **AC13: Keyset Cursor Pagination** | Keysets paginate deterministically on `(created_at DESC, id DESC)` with zero duplicate rows across pages. Limit clamped to `[1, 50]`. | **PASSED** |
| **STORY-003** | **AC14: Malformed Cursor Rejection** | Malformed base64 cursor strings are rejected with `ValidationError` (`code: "INVALID_CURSOR"`, HTTP 422). | **PASSED** |
| **STORY-003** | **AC15: Mutating HTTP Methods (405)** | Non-GET mutating verbs (`POST`, `PUT`, `DELETE`, `PATCH`) return HTTP 405 Method Not Allowed in the canonical error envelope. | **PASSED** |
| **STORY-003** | **AC16: Redis Short-TTL Caching & Resiliency** | Caches responses under `favorites:{child_id}:{type}:{cursor}:{limit}` with 60s TTL. Instant cache purge on toggle mutations. Degrades gracefully to DB reads on Redis failure. | **PASSED** |
| **STORY-003** | **AC17: Multi-Child SQLite Tenancy Isolation** | Verified in real in-memory SQLite: Child A and Child B queries are strictly isolated; zero data leakage. | **PASSED** |

---

## 2. Test Execution Log

**Command (Dedicated Task B-02 Suite)**:
```powershell
pytest tests/modules/content/test_favorites_listing_api.py -v
```

**Output**:
```text
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Sarva\Documents\WORKGROUP-NOORHEROES\NoorHeroes-Backend
configfile: pyproject.toml
plugins: anyio-4.14.0, asyncio-1.4.0, cov-7.1.0, mock-3.15.1, xdist-3.8.0
asyncio: mode=Mode.STRICT, debug=False
collected 40 items

tests\modules\content\test_favorites_listing_api.py::test_sibling_id_access_attempt_returns_403 PASSED [  2%]
tests\modules\content\test_favorites_listing_api.py::test_matching_child_id_succeeds_with_page_result PASSED [  5%]
tests\modules\content\test_favorites_listing_api.py::test_unauthenticated_request_returns_401 PASSED [  7%]
tests\modules\content\test_favorites_listing_api.py::test_parent_session_returns_403 PASSED [ 10%]
tests\modules\content\test_favorites_listing_api.py::test_filter_by_valid_content_type[story] PASSED [ 12%]
tests\modules\content\test_favorites_listing_api.py::test_filter_by_valid_content_type[surah] PASSED [ 15%]
tests\modules\content\test_favorites_listing_api.py::test_filter_by_valid_content_type[dua] PASSED [ 17%]
tests\modules\content\test_favorites_listing_api.py::test_type_filter_case_insensitivity_and_whitespace PASSED [ 20%]
tests\modules\content\test_favorites_listing_api.py::test_invalid_type_filter_returns_422[podcast] PASSED [ 22%]
tests\modules\content\test_favorites_listing_api.py::test_invalid_type_filter_returns_422[book] PASSED [ 25%]
tests\modules\content\test_favorites_listing_api.py::test_invalid_type_filter_returns_422[video] PASSED [ 27%]
tests\modules\content\test_favorites_listing_api.py::test_invalid_type_filter_returns_422[123] PASSED [ 30%]
tests\modules\content\test_favorites_listing_api.py::test_invalid_type_filter_returns_422[invalid] PASSED [ 32%]
tests\modules\content\test_favorites_listing_api.py::test_invalid_type_filter_returns_422[stories] PASSED [ 35%]
tests\modules\content\test_favorites_listing_api.py::test_invalid_type_filter_returns_422[duas] PASSED [ 37%]
tests\modules\content\test_favorites_listing_api.py::test_invalid_type_filter_returns_422[surahs] PASSED [ 40%]
tests\modules\content\test_favorites_listing_api.py::test_type_filter_all_returns_all_items PASSED [ 42%]
tests\modules\content\test_favorites_listing_api.py::test_pagination_parameters_forwarded PASSED [ 45%]
tests\modules\content\test_favorites_listing_api.py::test_empty_favorites_returns_200_with_empty_items PASSED [ 47%]
tests\modules\content\test_favorites_listing_api.py::test_limit_bounds_validation PASSED [ 50%]
tests\modules\content\test_favorites_listing_api.py::test_favorite_schemas_conformance_and_aliases PASSED [ 52%]
tests\modules\content\test_favorites_listing_api.py::test_sqlite_real_persistence_listing_and_ordering PASSED [ 55%]
tests\modules\content\test_favorites_listing_api.py::test_sqlite_withdrawn_content_resolution PASSED [ 57%]
tests\modules\content\test_favorites_listing_api.py::test_sqlite_series_restructuring_canonical_resolution PASSED [ 60%]
tests\modules\content\test_favorites_listing_api.py::test_sqlite_multi_child_database_isolation PASSED [ 62%]
tests\modules\content\test_favorites_listing_api.py::test_sqlite_keyset_pagination_zero_duplicates PASSED [ 65%]
tests\modules\content\test_favorites_listing_api.py::test_redis_caching_and_invalidation PASSED [ 67%]
tests\modules\content\test_favorites_listing_api.py::test_redis_failure_resilience PASSED [ 70%]
tests\modules\content\test_favorites_listing_api.py::test_openapi_schema_contains_child_favorites_endpoint PASSED [ 72%]
tests\modules\content\test_favorites_listing_api.py::test_sqlite_cascading_parent_series_withdrawal_marks_unavailable PASSED [ 75%]
tests\modules\content\test_favorites_listing_api.py::test_sqlite_canonical_series_withdrawal_marks_unavailable PASSED [ 77%]
tests\modules\content\test_favorites_listing_api.py::test_sqlite_withdrawn_dua_resolution PASSED [ 80%]
tests\modules\content\test_favorites_listing_api.py::test_sqlite_orphan_ghost_content_graceful_degradation PASSED [ 82%]
tests\modules\content\test_favorites_listing_api.py::test_surah_access_checker_integration PASSED [ 85%]
tests\modules\content\test_favorites_listing_api.py::test_invalid_cursor_handling_and_rejection PASSED [ 87%]
tests\modules\content\test_favorites_listing_api.py::test_api_invalid_cursor_returns_error_envelope PASSED [ 90%]
tests\modules\content\test_favorites_listing_api.py::test_non_get_methods_return_405[post] PASSED [ 92%]
tests\modules\content\test_favorites_listing_api.py::test_non_get_methods_return_405[put] PASSED [ 95%]
tests\modules\content\test_favorites_listing_api.py::test_non_get_methods_return_405[delete] PASSED [ 97%]
tests\modules\content\test_favorites_listing_api.py::test_non_get_methods_return_405[patch] PASSED [100%]

============================= 40 passed in 6.68s ==============================
```

**Command (Full Favorites Cross-Module Regression Suite — 115 Total Tests)**:
```powershell
pytest tests/modules/content/test_favorites_listing_api.py tests/modules/content/test_favorite_api.py tests/modules/content/test_favorite_toggle_api.py tests/modules/content/test_favorite_migration.py tests/architecture/test_db_config.py -v
```

**Output**:
```text
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Sarva\Documents\WORKGROUP-NOORHEROES\NoorHeroes-Backend
configfile: pyproject.toml
plugins: anyio-4.14.0, asyncio-1.4.0, cov-7.1.0, mock-3.15.1, xdist-3.8.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 115 items

tests\modules\content\test_favorites_listing_api.py ........................................ [ 34%]
tests\modules\content\test_favorite_api.py .........................     [ 56%]
tests\modules\content\test_favorite_toggle_api.py ............................. [ 81%]
tests\modules\content\test_favorite_migration.py .............           [ 93%]
tests\architecture\test_db_config.py ........                            [100%]

============================ 115 passed in 20.37s =============================
```
