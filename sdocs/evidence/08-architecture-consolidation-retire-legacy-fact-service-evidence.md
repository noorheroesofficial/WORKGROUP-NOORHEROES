# Evidence: Architecture Consolidation & Retire Legacy Fact Service (B-08)

**Task**: `08-architecture-consolidation-retire-legacy-fact-service`  
**Feature**: `Feature_B18_Islamic_Facts_Module` (B.18 Islamic Facts Module)  
**Parent PRD**: `PRD_Documents/Child App Supporting (13-18)/Feature_B18_Islamic_Facts_Module.md`  
**Task Blueprint**: `Development_Blueprints/B18_Islamic_Facts_Module/Backend/08-architecture-consolidation-retire-legacy-fact-service.md`  
**Date**: 2026-10-13  
**Status**: VERIFIED & CLOSED (100% Zero-Missing-Scenarios Pass Rate, 84/84 Tests Green)  

---

## 1. Verified Acceptance Criteria Matrix

| Criterion ID | Requirement / Invariant | Acceptance Criteria & Scenario | Result |
|:---|:---|:---|:---:|
| **AC-01** | **Consolidated Daily Fact Ownership (Blueprint B-08 §1, §14)** | Feature B.18's `FactSelectionService` (`src/noorheroes/modules/content/services/fact_selection_service.py`) is the authoritative sole owner of `GET /v1/facts/daily`. | **PASSED** |
| **AC-02** | **Legacy Fact Service Retirement** | Legacy `FactService`, `FactRepository`, and `HomeFactHistory` in `src/noorheroes/modules/facts/` emit `DeprecationWarning` upon instantiation. | **PASSED** |
| **AC-03** | **Shared Calendar Engine Preservation** | `IslamicCalendarService` remains active, authoritative, and untouched for Hijri date calculations and greeting occasion resolution without deprecation warnings. | **PASSED** |
| **AC-04** | **Defensive Occasion Resolution Gate** | `FactSelectionService` invokes `IslamicCalendarService.resolve_occasion()` with defensive `isinstance(..., str)` checks across all selection branches, preserving child greetings (e.g. "Jummah Mubarak"). | **PASSED** |
| **AC-05** | **Home Section 10 Feed Repointing** | `IslamicCalendarClient` in `src/noorheroes/modules/home/clients/islamic_calendar_client.py` repointed to query B.18's `/v1/facts/daily` with `surface="home_card"`. | **PASSED** |
| **AC-06** | **Runtime Cutover Feature Flag** | Managed by `settings.b18_facts_cutover_enabled: bool = True`. Default is enabled. | **PASSED** |
| **AC-07** | **Alembic Data Migration 0104** | Migration `0104_migrate_home_fact_history_to_fact_seen_log.py` decomposes JSON arrays into relational `fact_seen_log` rows with foreign key safety stubs. | **PASSED** |
| **AC-08** | **Non-Destructive Legacy Retention** | Migration 0104 preserves `home_fact_history` table and original rows completely intact as a rollback safety net. | **PASSED** |
| **AC-09** | **Reversible Rollback Isolation** | `downgrade()` deletes only rows matching `migrated_legacy_%`, guaranteeing zero collateral damage to post-cutover organic child history. | **PASSED** |
| **AC-10** | **Superset Wire Contract Parity** | `DailyFactResponse` includes `factId`/`fact_id`, `text`, `topic`, `scholarApproved`, `occasion`, `isEvergreen`, `sourceCitation`, `category`. | **PASSED** |
| **AC-11** | **Sibling Tenancy Isolation (403 Forbidden)** | Mismatched `child_id` query parameter returns HTTP 403 `SessionChildMismatchError`. Matching or omitted parameter returns HTTP 200 OK. | **PASSED** |
| **AC-12** | **HTTP Method Gates (405 Method Not Allowed)** | POST, PUT, DELETE, PATCH on `/v1/facts/daily` return HTTP 405 Method Not Allowed. | **PASSED** |
| **AC-13** | **Auth Scope Gate (401 / 403)** | Unauthenticated requests return HTTP 401; parent-only session returns HTTP 403 Forbidden. | **PASSED** |
| **AC-14** | **Router Mounting Authority** | `api_v1_router` unmounts legacy `facts_router` and mounts `content_facts_router`; preserves `v1_admin_facts_router` for `/v1/admin/occasions`. | **PASSED** |

---

## 2. Test Execution Logs

### 2.1 Dedicated Task B-08 Zero-Missing Scenarios Suite (23 Tests)

**Command**:
```powershell
.venv\Scripts\python.exe -m pytest tests/modules/content/test_consolidation_zero_missing_scenarios.py -v
```

**Results**:
- 23 passed, 0 failed in 50.51s (100% green).
- Scenarios verified: `S-264` through `S-286`.

### 2.2 Comprehensive B-08 Regression Suite (84 Tests)

**Command**:
```powershell
.venv\Scripts\python.exe -m pytest tests/modules/content/test_consolidation_zero_missing_scenarios.py tests/modules/content/test_legacy_fact_history_migration.py tests/integration/test_home_fact_card_regression.py tests/integration/test_fact_daily_flow.py tests/modules/content/test_fact_daily_selection.py tests/modules/content/test_admin_fact_crud.py -v
```

**Results**:
- 84 passed, 0 failed in 97.42s (100% green).

### 2.3 Entire Feature B.18 Module Battery (248 Tests across Tasks B-01..B-08)

**Command**:
```powershell
.venv\Scripts\python.exe -m pytest tests/modules/content/test_fact_approval_gate.py tests/modules/content/test_fact_versioning_immutability.py tests/unit/test_fact_b01_migration.py tests/modules/content/test_fact_daily_selection.py tests/modules/content/test_fact_dedup_relaxation.py tests/modules/content/test_fact_seasonal_fallback.py tests/modules/content/test_fact_detail_retrieval.py tests/modules/content/test_fact_related_content_withdrawal.py tests/modules/content/test_fact_quiz_delegation.py tests/modules/content/test_admin_fact_crud.py tests/modules/content/test_scholar_approval_workflow.py tests/modules/content/test_disputed_topic_ai_assist_bypass.py tests/modules/content/test_admin_fact_zero_missing_scenarios.py tests/modules/content/test_fact_engagement_monitoring.py tests/modules/content/test_fact_engagement_zero_missing_scenarios.py tests/modules/content/test_legacy_fact_history_migration.py tests/integration/test_home_fact_card_regression.py tests/integration/test_fact_daily_flow.py tests/modules/content/test_consolidation_zero_missing_scenarios.py -q
```

**Results**:
- 248 passed, 0 failed in 108.41s (100% green).

---

## 3. Documentation Synchronized

| Document | Section | Update Scope | Status |
|:---|:---|:---|:---:|
| [`NoorHeroes-Backend/MASTER-README.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/MASTER-README.md) | §11.127 | Full Task B-08 architecture specification, invariants, and Scenarios S-255..S-286 table. | **SYNCHRONIZED** |
| [`NoorHeroes-Backend/FAST-API-INSTRUCTIONS.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/FAST-API-INSTRUCTIONS.md) | §5.4, §5.20 | Updated B-08 consolidation details, deprecation notices, and test verification references. | **SYNCHRONIZED** |
| [`NoorHeroes-Backend/CHANGELOG.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/CHANGELOG.md) | Release 1.68.0 | Added detailed release notes covering 84 passing test cases and zero missing scenarios. | **SYNCHRONIZED** |
| [`src/noorheroes/modules/content/README.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/src/noorheroes/modules/content/README.md) | §15.1..§15.5 | Added B-08 architectural invariants, migration 0104 spec, and zero-missing scenarios table. | **SYNCHRONIZED** |
| [`src/noorheroes/modules/facts/README.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/src/noorheroes/modules/facts/README.md) | Header & §5 | Deprecation notice for legacy fact service; documented active calendar & occasion routes. | **SYNCHRONIZED** |
| [`CHANGELOG/CROSS_PLATFORM_CHANGES.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/CHANGELOG/CROSS_PLATFORM_CHANGES.md) | Top of Change History | Appended `[FEATURE_B18_B08]` entry covering cross-platform impacts and contract guarantees. | **SYNCHRONIZED** |
| [`artifacts/openapi.json`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/artifacts/openapi.json) | `/v1/facts/daily` | OpenAPI schema contracts fully synced with dual-wire camelCase/snake_case serialization. | **SYNCHRONIZED** |
