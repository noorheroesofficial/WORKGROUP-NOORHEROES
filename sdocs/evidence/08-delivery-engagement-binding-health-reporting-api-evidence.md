# Evidence: Delivery, Engagement & Binding Health Reporting API (B-08)

**Task**: `08-delivery-engagement-binding-health-reporting-api`  
**Epic**: `EPIC-017` (Child-Facing Notifications System)  
**Parent PRD**: `PRD_Documents/Child App Supporting (13-18)/Feature_B17_Notifications_Child_Facing.md`  
**Task Blueprint**: `Development_Blueprints/B17_Notifications_Child_Facing/Backend/08-delivery-engagement-binding-health-reporting-api.md`  
**Date**: 2026-10-09  
**Status**: VERIFIED & CLOSED (100% Zero-Missing-Scenarios Pass Rate)  

---

## 1. Verified Acceptance Criteria Matrix

| Criterion ID | Requirement / Invariant | Acceptance Criteria & Scenario | Result |
|:---|:---|:---|:---:|
| **AC-01** | **Delivery & Engagement Funnel Pipeline (Blueprint B-08 §10, §13, PRD §11.2)** | Aggregates 5-stage funnel: `created -> sent -> delivered -> opened -> deepLinkResolved`. Dispatched volume reflects true transport dispatches. | **PASSED** |
| **AC-02** | **Suppression Breakdown Categorization (Blueprint B-08 §5, §10, PRD §11.1)** | Categorizes all suppressed intents across policy cancellation reasons: `quiet_hours`, `frequency_cap`, `binding_inactive`, `stale_condition`, `consent`. | **PASSED** |
| **AC-03** | **Fatigue Backoff Trigger Frequency (Blueprint B-08 §10, §13, PRD §11.3)** | Aggregates frequency backoff delay events triggered by repeated non-opens from outbox telemetry and policy suppression state. | **PASSED** |
| **AC-04** | **Funnel Conversion Rates & Ratios (Blueprint B-08 §10, §13)** | Calculates conversion ratios: `sent_rate` (`sent/created`), `delivered_rate` (`delivered/sent`), `open_rate` (`opened/delivered`), and `deep_link_resolution_rate` (`deepLinkResolved/opened`) with division-by-zero protection. | **PASSED** |
| **AC-05** | **Category & Locale Filtering (Blueprint B-08 §10, §13)** | Supports query parameter filtering by trigger category (e.g. `daily_reminder`, `streak_risk`) and template locale (`en`, `ar`, `ur`). Echoes filters in response payload. | **PASSED** |
| **AC-06** | **Device Profile Binding Health Metrics (Blueprint B-08 §5, §10, PRD §8)** | Computes 50th percentile (median) and 95th percentile switch latency durations in milliseconds using linear interpolation across sample window. | **PASSED** |
| **AC-07** | **Misdelivery-Risk Prevention Positive Signal (Blueprint B-08 §5, §10, §13, PRD §8)** | Surfaces positive integrity counter `misdeliveryRiskEventsPrevented` for intents safely suppressed at send-time because the device active profile switched away (`binding_inactive`). | **PASSED** |
| **AC-08** | **Chronological Date Range Validation (Blueprint B-08 §15, §18)** | Enforces $to \ge from$ chronological ordering. Inverted date ranges return HTTP 422 Unprocessable Entity (`INVALID_DATE_RANGE`). Equal dates ($from = to$) are accepted. | **PASSED** |
| **AC-09** | **Maximum Permitted Window Constraint (Blueprint B-08 §15, §18)** | Enforces a maximum permitted query window of 1 year (366 days). Ranges exceeding 366 days return HTTP 422 Unprocessable Entity (`INVALID_DATE_RANGE`). | **PASSED** |
| **AC-10** | **Timezone Normalization (Blueprint B-08 §10, §15)** | Normalizes non-UTC timezone offsets (e.g. IST +05:30) to UTC before query execution and cache key derivation. | **PASSED** |
| **AC-11** | **Short-TTL Redis Caching Layer (Blueprint B-08 §10, §18, §24)** | Caches aggregate query results in Redis for 300 seconds (5 minutes) with structured cache keys, avoiding repeated database load on dashboard refreshes. | **PASSED** |
| **AC-12** | **Fail-Safe Cache Degradation (Blueprint B-08 §18)** | Redis connectivity outages or serialization failures gracefully degrade to direct PostgreSQL query execution without failing the request (returns 200 OK). | **PASSED** |
| **AC-13** | **Admin RBAC Scope Enforcement (Blueprint B-08 §16, §17)** | `GET /delivery-engagement` restricted to `product_admin` and `content_editor`. `GET /binding-health` restricted to `product_admin` and `trust_safety`. Superadmin and wildcard (`*`) access permitted. | **PASSED** |
| **AC-14** | **Authentication & Error Envelopes (Blueprint B-08 §13, §18)** | Unauthenticated requests return HTTP 401 Unauthorized (`AUTHENTICATION_REQUIRED`). Unauthorized roles return HTTP 403 Forbidden (`INSUFFICIENT_PERMISSIONS`). | **PASSED** |
| **AC-15** | **Read-Only HTTP Method Enforcement (Blueprint B-08 §6, §25)** | Read-only endpoints strictly reject mutating HTTP methods (`POST`, `PUT`, `DELETE`, `PATCH`) with HTTP 405 Method Not Allowed. | **PASSED** |
| **AC-16** | **Zero Child PII Invariant (Blueprint B-08 §25, PRD §12.6)** | Strict privacy guarantee: aggregate numeric counts, rates, and latency metrics only. Zero child profile IDs, parent IDs, device tokens, or personal identifiers are exposed. | **PASSED** |
| **AC-17** | **Dual-Wire Contract Parity (SAM Contract `admin-notification-reports.md`)** | Pydantic v2 schemas configured with `NoorHeroesBaseModel`, `extra="forbid"`, `alias_generator=to_camel`, `AliasChoices`, and `serialization_alias` for seamless camelCase wire serialization. | **PASSED** |
| **AC-18** | **Zero Regression Notifications Test Suite** | 30/30 dedicated reporting tests passed, and 494/494 tests passed across the entire notifications bounded context suite. | **PASSED** |

---

## 2. Test Execution Log

### 2.1 Dedicated Task B-08 Reporting Service Test Suite (30 Tests — Zero Missing Scenarios)

**Command**:
```powershell
.venv\Scripts\python.exe -m pytest tests/modules/notifications/test_reporting_service.py -v
```

**Output**:
```text
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Sarva\Documents\WORKGROUP-NOORHEROES\NoorHeroes-Backend
configfile: pyproject.toml
plugins: anyio-4.14.2, asyncio-1.4.0, cov-7.1.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 30 items

tests\modules\notifications\test_reporting_service.py::test_delivery_engagement_funnel_and_breakdown_aggregation PASSED [  3%]
tests\modules\notifications\test_reporting_service.py::test_delivery_engagement_category_filter PASSED [  6%]
tests\modules\notifications\test_reporting_service.py::test_binding_health_report_aggregation PASSED [ 10%]
tests\modules\notifications\test_reporting_service.py::test_binding_health_empty_samples PASSED [ 13%]
tests\modules\notifications\test_reporting_service.py::test_date_range_validation_inverted PASSED [ 16%]
tests\modules\notifications\test_reporting_service.py::test_date_range_validation_exceeds_max_window PASSED [ 20%]
tests\modules\notifications\test_reporting_service.py::test_redis_caching_layer PASSED [ 23%]
tests\modules\notifications\test_reporting_service.py::test_redis_failure_fail_safe PASSED [ 26%]
tests\modules\notifications\test_reporting_service.py::test_api_get_delivery_engagement_report_success PASSED [ 30%]
tests\modules\notifications\test_reporting_service.py::test_api_get_delivery_engagement_report_rbac_forbidden PASSED [ 33%]
tests\modules\notifications\test_reporting_service.py::test_api_get_delivery_engagement_report_invalid_date_range PASSED [ 36%]
tests\modules\notifications\test_reporting_service.py::test_api_get_binding_health_report_success PASSED [ 40%]
tests\modules\notifications\test_reporting_service.py::test_api_get_binding_health_report_rbac_forbidden PASSED [ 43%]
tests\modules\notifications\test_reporting_service.py::test_no_child_identifying_data_in_reports PASSED [ 46%]
tests\modules\notifications\test_reporting_service.py::test_validate_date_range_timezone_conversion PASSED [ 50%]
tests\modules\notifications\test_reporting_service.py::test_validate_date_range_equal_dates PASSED [ 53%]
tests\modules\notifications\test_reporting_service.py::test_binding_health_single_latency_sample PASSED [ 56%]
tests\modules\notifications\test_reporting_service.py::test_binding_health_even_latency_samples PASSED [ 60%]
tests\modules\notifications\test_reporting_service.py::test_delivery_engagement_locale_filter PASSED [ 63%]
tests\modules\notifications\test_reporting_service.py::test_api_get_delivery_engagement_content_editor_access PASSED [ 66%]
tests\modules\notifications\test_reporting_service.py::test_api_get_binding_health_product_admin_access PASSED [ 70%]
tests\modules\notifications\test_reporting_service.py::test_api_missing_date_params_422 PASSED [ 73%]
tests\modules\notifications\test_reporting_service.py::test_api_excessive_date_range_422 PASSED [ 76%]
tests\modules\notifications\test_reporting_service.py::test_api_http_methods_not_allowed_405 PASSED [ 80%]
tests\modules\notifications\test_reporting_service.py::test_api_reports_unauthenticated_401 PASSED [ 83%]
tests\modules\notifications\test_reporting_service.py::test_api_get_delivery_engagement_report_contract_fields_and_echo PASSED [ 86%]
tests\modules\notifications\test_reporting_service.py::test_api_get_binding_health_report_contract_fields PASSED [ 90%]
tests\modules\notifications\test_reporting_service.py::test_api_superadmin_and_wildcard_scope_access PASSED [ 93%]
tests\modules\notifications\test_reporting_service.py::test_empty_dataset_zero_metrics_handling PASSED [ 96%]
tests\modules\notifications\test_reporting_service.py::test_record_switch_latency_naive_datetime_handling PASSED [100%]

============================= 30 passed in 4.73s ==============================
```

---

### 2.2 Full Notifications Context Regression Test Suite (494 Tests)

**Command**:
```powershell
.venv\Scripts\python.exe -m pytest tests/modules/notifications/ -q
```

**Output**:
```text
494 passed in 44.82s
```

---

## 3. OpenAPI 3.1.0 Contract Verification

**Command**:
```powershell
.venv\Scripts\python.exe -m src.noorheroes.scripts.export_openapi_schema --out artifacts/openapi.json
```

**Output**:
```text
Successfully exported OpenAPI schema to: C:\Users\Sarva\Documents\WORKGROUP-NOORHEROES\NoorHeroes-Backend\artifacts\openapi.json
```

**Registered Endpoints in OpenAPI Specification**:
- `GET /v1/admin/notifications/reports/delivery-engagement`
  - Parameters: `from`, `to`, `category`, `locale`
  - Responses: `200` (`DeliveryEngagementReportResponse`), `401`, `403`, `422`
- `GET /v1/admin/notifications/reports/binding-health`
  - Parameters: `from`, `to`
  - Responses: `200` (`BindingHealthReportResponse`), `401`, `403`, `422`
