# Evidence: Fact Content, Versioning & Scholar-Approval Model (B-01)

**Task**: `01-fact-content-versioning-scholar-approval-model`  
**Feature**: `Feature_B18_Islamic_Facts_Module` (B.18 Islamic Facts Module)  
**Parent PRD**: `PRD_Documents/Child App Supporting (13-18)/Feature_B18_Islamic_Facts_Module.md`  
**Task Blueprint**: `Development_Blueprints/B18_Islamic_Facts_Module/Backend/01-fact-content-versioning-scholar-approval-model.md`  
**Date**: 2026-10-11  
**Status**: VERIFIED & CLOSED (100% Zero-Missing-Scenarios Pass Rate)  

---

## 1. Verified Acceptance Criteria Matrix

| Criterion ID | Requirement / Invariant | Acceptance Criteria & Scenario | Result |
|:---|:---|:---|:---:|
| **AC-01** | **Structural Approval Gate Join Invariant (Blueprint B-01 §4, §10)** | `FactVersionRepository.get_published_version()` performs a mandatory SQL join requiring `fact_version.status = 'published' AND scholar_approval.approved = true AND scholar_approval.revoked_at IS NULL`. Zero ability to resolve unapproved/draft/revoked version for children. | **PASSED** |
| **AC-02** | **Version Immutability (FR-11)** | Editing published content drafts a new `fact_version` row; published rows are never mutated in-place. | **PASSED** |
| **AC-03** | **Soft-Delete Preservation (§4.4)** | Facts soft-withdraw via `is_withdrawn = true`, preserving child `fact_seen_log` history. | **PASSED** |
| **AC-04** | **Append-Only Engagement Log (§4.5)** | `fact_seen_log` records child engagement timestamp for 30-day deduplication window. | **PASSED** |
| **AC-05** | **Alembic Migration 0102** | Clean migration chain: creates `fact`, `fact_version`, `scholar_approval`, `fact_seen_log` with indexes and check constraints. | **PASSED** |

---

## 2. Test Execution Logs

**Test Suites**:
- `tests/modules/content/test_fact_approval_gate.py`
- `tests/modules/content/test_fact_versioning_immutability.py`
- `tests/unit/test_fact_b01_migration.py`

**Command**:
```powershell
.venv\Scripts\python.exe -m pytest tests/modules/content/test_fact_approval_gate.py tests/modules/content/test_fact_versioning_immutability.py tests/unit/test_fact_b01_migration.py -v
```

**Results**: 100% passing, 0 failures.

---

## 3. Documentation Synchronized

- [`NoorHeroes-Backend/MASTER-README.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/MASTER-README.md) (§11.120)
- [`sdocs/contracts/domain/fact-versioning-approval.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/sdocs/contracts/domain/fact-versioning-approval.md)
- [`sdocs/contracts/INDEX.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/sdocs/contracts/INDEX.md)
