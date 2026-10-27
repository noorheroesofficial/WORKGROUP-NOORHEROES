# Evidence: Download Manifest Issuance API (B-01)

**Task**: `01-download-manifest-issuance-api`  
**Epic**: `EPIC-015` (Offline Downloads & Sync Engine)  
**Parent PRD**: `PRD_Documents/Child App Supporting (13-18)/Feature_B15_Offline_Downloads_Sync.md`  
**Task Blueprint**: `Development_Blueprints/B15_Offline_Downloads_Sync/Backend/01-download-manifest-issuance-api.md`  
**Date**: 2026-09-29  
**Status**: VERIFIED & CLOSED (100% Pass Rate)

---

## 1. Verified Acceptance Criteria Matrix

| Criterion ID | Requirement / Invariant | Acceptance Criteria & Scenario | Result |
|:---|:---|:---|:---:|
| **AC-01** | **Download Manifest Issuance (Blueprint B-01 §10 / §13)** | `POST /v1/downloads/manifest` issues chunked signed CDN URLs with checksums and expiry timestamps. | **PASSED** |
| **AC-02** | **Unique Constraint Dedup (Blueprint B-01 §5 / §14, PRD Edge Case 3)** | Re-requesting manifest for `complete` download resolves existing record without duplicate row or `IntegrityError`. | **PASSED** |
| **AC-03** | **Resumable Download Continuation (Blueprint B-01 §5 / §10, PRD FR-6)** | Downloads in `in_progress` or `failed` state reuse `download_id` and reissue signed chunk URLs. | **PASSED** |
| **AC-04** | **Per-Child Storage Cap Gate (Blueprint B-01 §5 / §10, PRD FR-3)** | Exceeding parent-configured storage cap rejects with HTTP `403 DOWNLOAD_CAP_REACHED` and writes ZERO rows. | **PASSED** |
| **AC-05** | **Parental Lockout Gate (Blueprint B-01 §5 / §10, PRD Edge Case 11)** | Parental controls disabling offline downloads rejects with HTTP `403 DOWNLOADS_DISABLED_BY_PARENT`. | **PASSED** |
| **AC-06** | **Subscription Entitlement Gate (Blueprint B-01 §5 / §10, PRD FR-2)** | Accessing premium content on free tier without entitlement rejects with HTTP `403 ENTITLEMENT_REQUIRED`. | **PASSED** |
| **AC-07** | **Child Session Auth & Sibling Isolation (Blueprint B-01 §16 / §17, PRD FR-12)** | Requires child Bearer token (`Depends(get_current_child)`); parent tokens and cross-family sessions rejected. | **PASSED** |
| **AC-08** | **Validation & Enum Constraints (Blueprint B-01 §15)** | Validates `content_type` against allow-list and checks UUID formatting (`422` on invalid). | **PASSED** |
| **AC-09** | **Anti-Caching Transport Headers (Blueprint B-01 §10)** | Injects `Cache-Control: private, no-store, no-cache, must-revalidate` and `Pragma: no-cache`. | **PASSED** |
| **AC-10** | **Transactional Outbox Eventing (Blueprint B-01 §10)** | Emits `DownloadManifestIssued` outbox event for B-07 operational monitoring. | **PASSED** |

---

## 2. Test Execution Log (45 Tests Passed)

**Command**:
```powershell
python -m pytest tests/modules/downloads/test_manifest_issuance_api.py tests/modules/downloads/test_manifest_dedup_and_cap.py -v
```

**Output**:
```text
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Sarva\Documents\WORKGROUP-NOORHEROES\NoorHeroes-Backend
configfile: pyproject.toml
plugins: anyio-4.14.2, asyncio-1.4.0, cov-7.1.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 45 items

tests\modules\downloads\test_manifest_issuance_api.py .................. [ 40%]
.....                                                                    [ 51%]
tests\modules\downloads\test_manifest_dedup_and_cap.py ................. [ 88%]
.....                                                                    [100%]

============================= 45 passed in 4.30s ==============================
```

---

## 3. Architectural & Ledger Cross-References
- **Alembic Migration**: `alembic/versions/0092_create_download_record_table.py`.
- **Contract Specification**: `sdocs/contracts/api/download-manifest.md`.
- **Cross-Platform Ledger**: Entry `[FEATURE_B15_B01]` in `CHANGELOG/CROSS_PLATFORM_CHANGES.md`.
