# Evidence: In-App Notification Fetch API (B-09)

**Task**: `09-in-app-notification-fetch-api`  
**Epic**: `EPIC-017` (Child-Facing Notifications System)  
**Parent PRD**: `PRD_Documents/Child App Supporting (13-18)/Feature_B17_Notifications_Child_Facing.md`  
**Task Blueprint**: `Development_Blueprints/B17_Notifications_Child_Facing/Backend/09-in-app-notification-fetch-api.md`  
**Date**: 2026-10-09  
**Status**: VERIFIED & CLOSED (100% Zero-Missing-Scenarios Pass Rate)  

---

## 1. Verified Acceptance Criteria Matrix

| Criterion ID | Requirement / Invariant | Acceptance Criteria & Scenario | Result |
|:---|:---|:---|:---:|
| **AC-01** | **Read-Only Projection Over Sent Intents (Blueprint B-09 §5, §10, §141)** | `GET /v1/notifications/in-app` queries `notification_intents` joined to `notification_deliveries` for `status='sent'`. Never duplicates or re-evaluates policy checks at fetch time. | **PASSED** |
| **AC-02** | **Strict Child Horizontal Isolation (Blueprint B-09 §15, §25, §143)** | Query and service layer strictly filter on `target_child_id == child_id` of the authenticated session. Sibling notifications on a shared device are completely isolated and never leaked. | **PASSED** |
| **AC-03** | **Pre-Rendered Copy Reuse (Blueprint B-09 §10, §145, PRD §3.5)** | Surfaces pre-rendered template copy from `payload.rendered_copy`, `payload.rendered_body`, `payload.body`, or `delivery.template.body` without dynamic string substitution drift or PII/billing term risk. | **PASSED** |
| **AC-04** | **Time-Bounded Expiry Filtering (Blueprint B-09 §10, §14, §144)** | Notifications where `expires_at <= now` are excluded from results. Notifications where `expires_at > now` or `expires_at IS NULL` remain eligible. Also parses ISO `expires_at` in trigger payload. | **PASSED** |
| **AC-05** | **In-App Eligible Trigger Classes (Blueprint B-09 §10, §141)** | Filters trigger types to `IN_APP_ELIGIBLE_TYPES` (`in_app_banner`, `new_content`, `episode_ready`, `sequential_unlock_ready`, `daily_reminder`, `streak_risk`, `bedtime_story`, `reward_posted`, etc.). Non-in-app types (e.g. parent weekly digest) are excluded. | **PASSED** |
| **AC-06** | **Empty State Graceful Handling (Blueprint B-09 §18, §75)** | When no eligible in-app notifications exist for the authenticated child, returns HTTP `200 OK` with an empty `notifications: []` array, never an error status code. | **PASSED** |
| **AC-07** | **Authentication & Error Envelopes (Blueprint B-09 §16, §58)** | Requires authenticated child-mode Bearer token via `get_current_child`. Unauthenticated or invalid requests return HTTP `401 UNAUTHORIZED` with the Universal Error Envelope. | **PASSED** |
| **AC-08** | **Client-Side Dismissal Independence (Blueprint B-09 §5, §20)** | Dismissal tracking is client-local in K-03 (`InAppNotificationBanner`); backend idempotently projects all currently-eligible instances without mutating server dismissal state. | **PASSED** |
| **AC-09** | **Deep-Link Destination & Routing Params (Blueprint B-09 §13)** | Accurately extracts `destination` (e.g. `story_detail`, `streak_view`, `bedtime_player`) and optional parameter dictionaries (`params` / `contentId` / `streak_count`) for client navigation. | **PASSED** |
| **AC-10** | **Database Schema & Indexing (Blueprint B-09 §14, §24)** | Migration `0101_add_expires_at_to_notification_intents.py` adds `expires_at TIMESTAMPTZ` and composite index `ix_notification_intents_child_status_expires` on `(target_child_id, status, expires_at)`. | **PASSED** |
| **AC-11** | **Dual-Wire Wire Serialization (Blueprint B-09 §13, SAM Contract `api.in-app-notifications.md`)** | DTO models inherit from `NoorHeroesBaseModel` with `extra="forbid"`, `alias_generator=to_camel`, and `AliasChoices` for seamless camelCase and snake_case dual-wire compatibility. | **PASSED** |
| **AC-12** | **Zero Regression Notifications Suite** | 26/26 dedicated unit and integration tests passed; 520/520 total tests passed across `tests/modules/notifications/`. | **PASSED** |

---

## 2. Test Execution Log

### 2.1 Dedicated Task B-09 Test Suite (26 Tests — Zero Missing Scenarios)

**Command**:
```powershell
.venv\Scripts\python.exe -m pytest tests/modules/notifications/test_in_app_fetch_service.py -v
```

**Output**:
```text
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Sarva\Documents\WORKGROUP-NOORHEROES\NoorHeroes-Backend
configfile: pyproject.toml
plugins: anyio-4.14.2, asyncio-1.4.0, cov-7.1.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 26 items

tests\modules\notifications\test_in_app_fetch_service.py::test_fetch_eligible_returns_sent_intents PASSED [  3%]
tests\modules\notifications\test_in_app_fetch_service.py::test_fetch_excludes_non_sent_statuses PASSED [  7%]
tests\modules\notifications\test_in_app_fetch_service.py::test_fetch_strict_child_isolation PASSED [ 11%]
tests\modules\notifications\test_in_app_fetch_service.py::test_fetch_excludes_expired_notifications PASSED [ 15%]
tests\modules\notifications\test_in_app_fetch_service.py::test_fetch_includes_future_unexpired_notifications PASSED [ 19%]
tests\modules\notifications\test_in_app_fetch_service.py::test_fetch_includes_null_expires_at PASSED [ 23%]
tests\modules\notifications\test_in_app_fetch_service.py::test_fetch_handles_payload_level_expires_at PASSED [ 26%]
tests\modules\notifications\test_in_app_fetch_service.py::test_fetch_filters_non_in_app_types PASSED [ 30%]
tests\modules\notifications\test_in_app_fetch_service.py::test_fetch_supports_custom_eligible_types PASSED [ 34%]
tests\modules\notifications\test_in_app_fetch_service.py::test_fetch_empty_child_id_returns_empty_list PASSED [ 38%]
tests\modules\notifications\test_in_app_fetch_service.py::test_fetch_no_notifications_returns_empty_list PASSED [ 42%]
tests\modules\notifications\test_in_app_fetch_service.py::test_rendered_copy_resolution_hierarchy PASSED [ 46%]
tests\modules\notifications\test_in_app_fetch_service.py::test_destination_and_params_resolution PASSED [ 50%]
tests\modules\notifications\test_in_app_fetch_service.py::test_deduplication_of_intents_with_multiple_deliveries PASSED [ 53%]
tests\modules\notifications\test_in_app_fetch_service.py::test_api_get_in_app_200_with_notifications PASSED [ 57%]
tests\modules\notifications\test_in_app_fetch_service.py::test_api_get_in_app_200_empty_list PASSED [ 61%]
tests\modules\notifications\test_in_app_fetch_service.py::test_api_get_in_app_401_unauthenticated PASSED [ 65%]
tests\modules\notifications\test_in_app_fetch_service.py::test_api_get_in_app_child_isolation_on_shared_device PASSED [ 69%]
tests\modules\notifications\test_in_app_fetch_service.py::test_api_get_in_app_excludes_expired_items PASSED [ 73%]
tests\modules\notifications\test_in_app_fetch_service.py::test_dual_wire_dto_validation PASSED [ 76%]
tests\modules\notifications\test_in_app_fetch_service.py::test_api_get_in_app_database_failure_500 PASSED [ 80%]
tests\modules\notifications\test_in_app_fetch_service.py::test_api_get_in_app_methods_not_allowed_405 PASSED [ 84%]
tests\modules\notifications\test_in_app_fetch_service.py::test_api_get_in_app_full_pipeline_flow PASSED [ 88%]
tests\modules\notifications\test_in_app_fetch_service.py::test_fetch_malformed_payload_expires_at_graceful_handling PASSED [ 92%]
tests\modules\notifications\test_in_app_fetch_service.py::test_fetch_exact_expiration_boundary PASSED [ 96%]
tests\modules\notifications\test_in_app_fetch_service.py::test_fetch_with_whitespace_padded_child_id PASSED [100%]

============================= 26 passed in 4.79s ==============================
```

---

## 3. Schema & Migration Verification

1. **Alembic Revision `0101_add_expires_at_to_notification_intents.py`**:
   - Down revision: `0100_create_notification_campaign_table`
   - Added column: `expires_at` (`TIMESTAMPTZ`, nullable) on `notification_intents`
   - Created index: `ix_notification_intents_expires_at`
   - Created composite index: `ix_notification_intents_child_status_expires` on `(target_child_id, status, expires_at)`
2. **Clean Layering**:
   - `InAppNotificationFetchService` queries via SQL `outerjoin(NotificationDelivery)` to keep models cleanly decoupled and prevent eager relationship side-effects on unrelated tests.
