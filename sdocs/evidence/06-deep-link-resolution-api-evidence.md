# Evidence: Deep Link Resolution API (B-06)

**Task**: `06-deep-link-resolution-api`  
**Epic**: `EPIC-017` (Child-Facing Notifications System)  
**Parent PRD**: `PRD_Documents/Child App Supporting (13-18)/Feature_B17_Notifications_Child_Facing.md`  
**Task Blueprint**: `Development_Blueprints/B17_Notifications_Child_Facing/Backend/06-deep-link-resolution-api.md`  
**Date**: 2026-10-09  
**Status**: VERIFIED & CLOSED (100% Zero-Missing-Scenarios Pass Rate)  

---

## 1. Verified Acceptance Criteria Matrix

| Criterion ID | Requirement / Invariant | Acceptance Criteria & Scenario | Result |
|:---|:---|:---|:---:|
| **AC-01** | **Server-Side Validation Gate (PRD FR-5 / Blueprint B-06 §4/§10)** | Every notification open executes full backend validation (session, child profile, content availability, parent gate). Raw notification payload destination is never trusted without this round-trip. | **PASSED** |
| **AC-02** | **Child Mismatch Protection (PRD §5 Item 5, Edge Case 2)** | When a notification originally targeted to Child A is opened while Child B is active on the device, authoritatively returns `valid=false, reason='child_mismatch', fallbackDestination='who_is_learning'`. Never routes into Child A's state; does not update `opened_at`. | **PASSED** |
| **AC-03** | **Matching Child Resolution & Open Receipt (Blueprint B-06 §10/§23)** | When active child matches intended child, returns `valid=true, destination='...', params={...}`. Automatically updates `notification_deliveries.opened_at` timestamp and status to `'opened'` via `DeliveryAdapter.mark_opened()`. | **PASSED** |
| **AC-04** | **Parent Session on Parent Destination (Blueprint B-06 §10)** | Authenticated parent session opening a parent-targeted notification (`target_binding='parent'`) resolves destination (e.g. `parent_dashboard`) and updates `opened_at`. | **PASSED** |
| **AC-05** | **Parent Session on Child Intent Re-Route (PRD §5 Item 5)** | Authenticated parent session opening a child-exclusive notification re-routes to `who_is_learning` so the parent selects the intended child profile first. | **PASSED** |
| **AC-06** | **Parent Gate & PIN Lock Requirement (PRD FR-5 / Blueprint B-06 §18)** | Child session opening a parent-gated destination (`parent_dashboard`, `billing`, `parent_settings`, etc.) returns `valid=false, reason='requires_lock_gate', fallbackDestination='parent_gate'`. | **PASSED** |
| **AC-07** | **Custom Lock Gate Payload Flags (PRD FR-5)** | Payload flags `requires_lock_gate=true` or `requires_parent_gate=true` enforce lock gate for child callers while passing authenticated parent sessions. | **PASSED** |
| **AC-08** | **Graceful Handling of Withdrawn Content (PRD Edge Case 4)** | Content marked withdrawn or flagged by dynamic availability checker returns `valid=false, reason='content_unavailable', fallbackDestination='home'`, preventing client crashes. | **PASSED** |
| **AC-09** | **Dynamic Content Availability Checker Integration (Blueprint B-06 §10 Item 3)** | Asynchronous content availability checker hook verifies live publication status against destination modules (A.3, A.4, A.6). | **PASSED** |
| **AC-10** | **Broadcast & Family-Wide Notifications (PRD Edge Case 9)** | Notifications with `target_binding='child'` and `target_child_id=None` resolve safely for any active family child without mismatch. | **PASSED** |
| **AC-11** | **Canonical Notification Types Mapping (PRD FR-1, FR-12, FR-13)** | Canonical classes (`streak_risk`, `daily_reminder`, `bedtime_story`, `content_published`, `reward_posted`, `seasonal_event`, `in_app_banner`) default to designated destination screens when omitted in payload. | **PASSED** |
| **AC-12** | **Session Expired Detection (Blueprint B-06 §10/§18)** | Invalid or expired session tokens return `valid=false, reason='session_expired', fallbackDestination='login'`. | **PASSED** |
| **AC-13** | **Unknown Token Handling (Blueprint B-06 §13/§18)** | Unrecognized or expired deep link tokens return HTTP `404 Not Found` with `DEEP_LINK_NOT_FOUND` error envelope. | **PASSED** |
| **AC-14** | **Unauthenticated Call Security Gate (Blueprint B-06 §13)** | Missing Bearer token returns HTTP `401 Unauthorized` (`MISSING_TOKEN`). | **PASSED** |
| **AC-15** | **Dual-Wire camelCase Schema Contract (Blueprint B-06 §13)** | Response serialization supports camelCase (`fallbackDestination`, `deliveryId`) for Kotlin Multiplatform (KMP) and Next.js clients. | **PASSED** |
| **AC-16** | **Transactional Domain Event Emission (Blueprint B-06 §23)** | Emits `NotificationDeepLinkResolved` and `NotificationOpened` events atomically into the transactional outbox. | **PASSED** |
| **AC-17** | **Full Notifications Test Suite** | 37/37 dedicated tests passed for Task B-06, and 408/408 passed across the full notifications test suite. | **PASSED** |

---

## 2. Test Execution Log

### 2.1 Dedicated Task B-06 Test Suite (37 Tests — Zero Missing Scenarios)

**Command**:
```powershell
pytest tests/modules/notifications/test_deep_link_service.py -v
```

**Output**:
```text
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Sarva\Documents\WORKGROUP-NOORHEROES\NoorHeroes-Backend
configfile: pyproject.toml
plugins: anyio-4.14.2, asyncio-1.4.0, cov-7.1.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 37 items

tests\modules\notifications\test_deep_link_service.py::test_resolve_unknown_token_raises_404 PASSED [  2%]
tests\modules\notifications\test_deep_link_service.py::test_resolve_child_mismatch_signals_who_is_learning PASSED [  5%]
tests\modules\notifications\test_deep_link_service.py::test_resolve_child_match_success_marks_opened PASSED [  8%]
tests\modules\notifications\test_deep_link_service.py::test_resolve_parent_session_child_notification_reroutes_who_is_learning PASSED [ 10%]
tests\modules\notifications\test_deep_link_service.py::test_resolve_content_withdrawn_flag_returns_unavailable PASSED [ 13%]
tests\modules\notifications\test_deep_link_service.py::test_resolve_content_availability_checker_hook PASSED [ 16%]
tests\modules\notifications\test_deep_link_service.py::test_resolve_parent_gate_required_from_child_session PASSED [ 18%]
tests\modules\notifications\test_deep_link_service.py::test_resolve_session_expired_returns_login PASSED [ 21%]
tests\modules\notifications\test_deep_link_service.py::test_resolve_via_custom_payload_token PASSED [ 24%]
tests\modules\notifications\test_deep_link_service.py::test_resolve_default_destination_mapping_when_unspecified PASSED [ 27%]
tests\modules\notifications\test_deep_link_service.py::test_resolve_parent_session_parent_notification_success PASSED [ 29%]
tests\modules\notifications\test_deep_link_service.py::test_resolve_content_available_checker_hook_success PASSED [ 32%]
tests\modules\notifications\test_deep_link_service.py::test_resolve_family_wide_notification_without_specific_child PASSED [ 35%]
tests\modules\notifications\test_deep_link_service.py::test_resolve_canonical_notification_types_default_destination[streak_risk-habit_builder] PASSED [ 37%]
tests\modules\notifications\test_deep_link_service.py::test_resolve_canonical_notification_types_default_destination[streak_at_risk-habit_builder] PASSED [ 40%]
tests\modules\notifications\test_deep_link_service.py::test_resolve_canonical_notification_types_default_destination[daily_reminder-home] PASSED [ 43%]
tests\modules\notifications\test_deep_link_service.py::test_resolve_canonical_notification_types_default_destination[daily_reminder_due-home] PASSED [ 45%]
tests\modules\notifications\test_deep_link_service.py::test_resolve_canonical_notification_types_default_destination[bedtime_story-bedtime_player] PASSED [ 48%]
tests\modules\notifications\test_deep_link_service.py::test_resolve_canonical_notification_types_default_destination[bedtime_story_due-bedtime_player] PASSED [ 51%]
tests\modules\notifications\test_deep_link_service.py::test_resolve_canonical_notification_types_default_destination[content_published-story_player] PASSED [ 54%]
tests\modules\notifications\test_deep_link_service.py::test_resolve_canonical_notification_types_default_destination[new_content-story_player] PASSED [ 56%]
tests\modules\notifications\test_deep_link_service.py::test_resolve_canonical_notification_types_default_destination[reward_posted-rewards_wallet] PASSED [ 59%]
tests\modules\notifications\test_deep_link_service.py::test_resolve_canonical_notification_types_default_destination[reward_milestone-rewards_wallet] PASSED [ 62%]
tests\modules\notifications\test_deep_link_service.py::test_resolve_canonical_notification_types_default_destination[seasonal_event-ramadan_hub] PASSED [ 64%]
tests\modules\notifications\test_deep_link_service.py::test_resolve_canonical_notification_types_default_destination[in_app_banner-home] PASSED [ 67%]
tests\modules\notifications\test_deep_link_service.py::test_resolve_custom_lock_gate_payload_flags PASSED [ 70%]
tests\modules\notifications\test_deep_link_service.py::test_resolve_caller_context_is_session_expired_flag PASSED [ 72%]
tests\modules\notifications\test_deep_link_service.py::test_resolve_with_injected_delivery_adapter PASSED [ 75%]
tests\modules\notifications\test_deep_link_service.py::test_api_resolve_unauthenticated_returns_401 PASSED [ 78%]
tests\modules\notifications\test_deep_link_service.py::test_api_resolve_unknown_token_returns_404 PASSED [ 81%]
tests\modules\notifications\test_deep_link_service.py::test_api_resolve_child_mismatch_returns_200_who_is_learning PASSED [ 83%]
tests\modules\notifications\test_deep_link_service.py::test_api_resolve_child_match_returns_200_valid PASSED [ 86%]
tests\modules\notifications\test_deep_link_service.py::test_api_resolve_parent_gate_returns_200_lock_gate PASSED [ 89%]
tests\modules\notifications\test_deep_link_service.py::test_api_resolve_content_unavailable_returns_200_home PASSED [ 91%]
tests\modules\notifications\test_deep_link_service.py::test_api_resolve_session_expired_returns_200_login PASSED [ 94%]
tests\modules\notifications\test_deep_link_service.py::test_api_resolve_parent_session_parent_destination_200 PASSED [ 97%]
tests\modules\notifications\test_deep_link_service.py::test_api_resolve_parent_session_child_notification_returns_200_who_is_learning PASSED [100%]

============================= 37 passed in 14.09s =============================
```

---

### 2.2 Full Notifications Module Regression Suite (408 Tests)

**Command**:
```powershell
pytest tests/modules/notifications/ -q
```

**Output**:
```text
408 passed in 78.43s
============================= 408 passed in 78.43s =============================
```

---

## 3. OpenAPI 3.1.0 Contract Verification

```powershell
python -m src.noorheroes.scripts.classify_openapi_diff --baseline openapi.baseline.json --current artifacts/openapi.json --fail-on-breaking
```

**Output**:
```text
No breaking schema changes detected.
```
