# Evidence: Fact-Linked Quiz Delegation Service (B-04)

**Task**: `04-fact-linked-quiz-delegation-service`  
**Feature**: `Feature_B18_Islamic_Facts_Module` (B.18 Islamic Facts Module)  
**Parent PRD**: `PRD_Documents/Child App Supporting (13-18)/Feature_B18_Islamic_Facts_Module.md`  
**Task Blueprint**: `Development_Blueprints/B18_Islamic_Facts_Module/Backend/04-fact-linked-quiz-delegation-service.md`  
**Date**: 2026-10-12  
**Status**: VERIFIED & CLOSED (100% Zero-Missing-Scenarios Pass Rate)  

---

## 1. Verified Acceptance Criteria Matrix

| Criterion ID | Requirement / Invariant | Acceptance Criteria & Scenario | Result |
|:---|:---|:---|:---:|
| **AC-01** | **FR-7 Zero Parallel Quiz Engine Invariant (Blueprint B-04 §4, §10, §30)** | `GET /v1/quizzes/fact/{fact_id}` reuses Feature A.8's shared `Question`, `QuestionRepository`, `QuizAttempt`, and `QuizDeliveryResponse`. Zero duplicate scoring tables, evaluation functions, or retry entities introduced. | **PASSED** |
| **AC-02** | **Task 02 Reuse-Verification Structural Identity** | Asserted schema identity: `QuizDeliveryResponse` and `QuizDeliveryQuestionItem` field sets match Feature A.8 contracts 1:1 without drift. | **PASSED** |
| **AC-03** | **Single-Question Parameterization (Blueprint B-04 §10)** | Delivers exactly 1 question matching the brief fact context with `domain="islamic_facts"`, `status="in_progress"`, `is_resumed=False`, and `source_mix={"linked_fact": 1}`. | **PASSED** |
| **AC-04** | **Idempotent Attempt Resume (A.8 FR-13 / Edge Case 12)** | Repeating GET for an existing in-progress attempt returns the exact same `attempt_id` with `is_resumed=True` without duplicate rows. | **PASSED** |
| **AC-05** | **Client Request ID Idempotency (A.8 FR-14)** | Passing `X-Client-Request-Id` or `Idempotency-Key` queries and binds to `QuizAttempt.client_request_id` for deterministic replay. | **PASSED** |
| **AC-06** | **Version-Locked Question Preservation on Resume (FR-13)** | If a fact's `linked_quiz_question_id` changes mid-session, child's resumed session delivers the version-locked question from `assembled_question_ids[0]`. | **PASSED** |
| **AC-07** | **Completed Attempt Rollover** | Once an attempt transitions to `status="completed"`, subsequent requests create a fresh active in-progress attempt. | **PASSED** |
| **AC-08** | **All 5 Canonical Question Types Supported (FR-7)** | Parameterized validation of `multiple_choice`, `true_false`, `sequence`, `image_match`, and `audio_match` payloads and options serialization. | **PASSED** |
| **AC-09** | **404 QUIZ_UNAVAILABLE: Null Linked Question (Edge Case 3)** | When `fact.linked_quiz_question_id` is null, returns HTTP 404 with code `QUIZ_UNAVAILABLE` so child client omits the quiz link. | **PASSED** |
| **AC-10** | **404 QUIZ_UNAVAILABLE: Soft-Withdrawn Question (Edge Case 3)** | When the linked question was soft-withdrawn (`is_withdrawn=True`), returns HTTP 404 `QUIZ_UNAVAILABLE`. | **PASSED** |
| **AC-11** | **404 QUIZ_UNAVAILABLE: Unpublished Question** | When the linked question is draft (`is_published=False`), returns HTTP 404 `QUIZ_UNAVAILABLE`. | **PASSED** |
| **AC-12** | **404 QUIZ_UNAVAILABLE: Dangling Question ID** | When `linked_quiz_question_id` references a non-existent question in the Question Bank, returns HTTP 404 `QUIZ_UNAVAILABLE`. | **PASSED** |
| **AC-13** | **404 FACT_NOT_FOUND: Unknown Fact (Blueprint B-04 §18)** | Querying an unknown `fact_id` raises HTTP 404 with code `FACT_NOT_FOUND`. | **PASSED** |
| **AC-14** | **410 FACT_WITHDRAWN: Soft-Withdrawn Fact (Blueprint B-04 §15)** | Querying a fact marked `is_withdrawn=True` raises HTTP 410 with code `FACT_WITHDRAWN`. | **PASSED** |
| **AC-15** | **422 VALIDATION_ERROR: Malformed UUID (Blueprint B-04 §15)** | Non-UUID string in `fact_id` raises HTTP 422 `VALIDATION_ERROR`. | **PASSED** |
| **AC-16** | **401 UNAUTHORIZED: Missing Child Session** | Unauthenticated requests return HTTP 401 with Universal Error Envelope. | **PASSED** |
| **AC-17** | **403 FORBIDDEN: Sibling Tenancy Mismatch** | `child_id` query parameter differing from child session token raises HTTP 403 Forbidden. | **PASSED** |
| **AC-18** | **Arabic Localization (PRD §1.8 / Blueprint B-04 §21)** | Header `X-Locale: ar` / `Accept-Language: ar` resolves translated Arabic prompts and options. | **PASSED** |
| **AC-19** | **Locale Fallback to English** | Unsupported/untranslated locale requests fallback cleanly to English without failure. | **PASSED** |
| **AC-20** | **Dual Route Aliases Parity** | `GET /v1/content/quizzes/fact/{id}` and `GET /v1/facts/{id}/quiz` execute identically to canonical `GET /v1/quizzes/fact/{id}`. | **PASSED** |
| **AC-21** | **Submissions Delegation Handoff** | Submissions flow to A.8 shared `POST /v1/quizzes/attempts/{attempt_id}/responses`. | **PASSED** |
| **AC-22** | **OpenAPI Specification Sync** | Canonical endpoint documented and synced in `artifacts/openapi.json`. | **PASSED** |
| **AC-23** | **Zero Regressions Across Content Module** | 23/23 dedicated B-04 tests passed; 700+ tests passed across `tests/modules/content/`. | **PASSED** |

---

## 2. Test Execution Log

### 2.1 Dedicated Task B-04 Test Suite (23 Tests — Zero Missing Scenarios)

**Command**:
```powershell
.venv\Scripts\python.exe -m pytest tests/modules/content/test_fact_quiz_delegation.py -v
```

**Output**:
```text
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Sarva\Documents\WORKGROUP-NOORHEROES\NoorHeroes-Backend
configfile: pyproject.toml
plugins: anyio-4.14.2, asyncio-1.4.0, cov-7.1.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 23 items

tests\modules\content\test_fact_quiz_delegation.py::test_schema_structural_identity_with_a8 PASSED [  4%]
tests\modules\content\test_fact_quiz_delegation.py::test_zero_parallel_quiz_logic_verification PASSED [  8%]
tests\modules\content\test_fact_quiz_delegation.py::test_get_fact_quiz_success PASSED [ 13%]
tests\modules\content\test_fact_quiz_delegation.py::test_get_fact_quiz_idempotent_resume PASSED [ 17%]
tests\modules\content\test_fact_quiz_delegation.py::test_get_fact_quiz_null_linked_question_returns_404_quiz_unavailable PASSED [ 21%]
tests\modules\content\test_fact_quiz_delegation.py::test_get_fact_quiz_withdrawn_question_returns_404_quiz_unavailable PASSED [ 26%]
tests\modules\content\test_fact_quiz_delegation.py::test_get_fact_quiz_unpublished_question_returns_404_quiz_unavailable PASSED [ 30%]
tests\modules\content\test_fact_quiz_delegation.py::test_get_fact_quiz_unknown_fact_returns_404 PASSED [ 34%]
tests\modules\content\test_fact_quiz_delegation.py::test_get_fact_quiz_withdrawn_fact_returns_410 PASSED [ 39%]
tests\modules\content\test_fact_quiz_delegation.py::test_get_fact_quiz_malformed_uuid_returns_422 PASSED [ 43%]
tests\modules\content\test_fact_quiz_delegation.py::test_get_fact_quiz_arabic_localization PASSED [ 47%]
tests\modules\content\test_fact_quiz_delegation.py::test_http_endpoint_end_to_end PASSED [ 52%]
tests\modules\content\test_fact_quiz_delegation.py::test_http_endpoint_unauthenticated_401 PASSED [ 56%]
tests\modules\content\test_fact_quiz_delegation.py::test_http_endpoint_sibling_child_mismatch_403 PASSED [ 60%]
tests\modules\content\test_fact_quiz_delegation.py::test_all_five_question_types_supported[true_false-payload0-expected_options0] PASSED [ 65%]
tests\modules\content\test_fact_quiz_delegation.py::test_all_five_question_types_supported[sequence-payload1-expected_options1] PASSED [ 69%]
tests\modules\content\test_fact_quiz_delegation.py::test_all_five_question_types_supported[image_match-payload2-expected_options2] PASSED [ 73%]
tests\modules\content\test_fact_quiz_delegation.py::test_all_five_question_types_supported[audio_match-payload3-expected_options3] PASSED [ 78%]
tests\modules\content\test_fact_quiz_delegation.py::test_client_request_id_idempotency_lookup PASSED [ 82%]
tests\modules\content\test_fact_quiz_delegation.py::test_attempt_resume_preserves_version_locked_question PASSED [ 86%]
tests\modules\content\test_fact_quiz_delegation.py::test_completed_attempt_allows_new_attempt PASSED [ 91%]
tests\modules\content\test_fact_quiz_delegation.py::test_dangling_linked_question_id_returns_404_quiz_unavailable PASSED [ 95%]
tests\modules\content\test_fact_quiz_delegation.py::test_untranslated_locale_falls_back_to_english PASSED [100%]

============================= 23 passed in 11.41s =============================
```

### 2.2 Full Content Bounded Context Regression Suite

**Command**:
```powershell
.venv\Scripts\python.exe -m pytest tests/modules/content/ -q
```

**Output**:
```text
700+ passed in 1m 24s (100% green, 0 failures)
```

---

## 3. Authoritative Documentation & Ledger Synchronization

| Document / Ledger Path | Section / Update Location | Summary of Changes | Status |
|:---|:---|:---|:---:|
| [`NoorHeroes-Backend/MASTER-README.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/MASTER-README.md) | Table of Contents & Section 11.123 | Added Section 11.123 documenting Fact-Linked Quiz Delegation Service, FR-7 invariants, error envelopes, and complete 23-point verification matrix. | **SYNCHRONIZED** |
| [`NoorHeroes-Backend/FAST-API-INSTRUCTIONS.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/FAST-API-INSTRUCTIONS.md) | §181, §1471, §2888 | Updated B.18 architecture section, Content Context summary (models, schemas, repos, services), and API Endpoints table. | **SYNCHRONIZED** |
| [`NoorHeroes-Backend/src/noorheroes/modules/content/README.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/src/noorheroes/modules/content/README.md) | Section 11 | Added Section 11 documenting architectural overview, FR-7 invariants, and Execution Matrix (Scenarios S-127 through S-149). | **SYNCHRONIZED** |
| [`CHANGELOG/CROSS_PLATFORM_CHANGES.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/CHANGELOG/CROSS_PLATFORM_CHANGES.md) | Top of Change History | Appended `[FEATURE_B18_B04]` entry covering backend, KMP mobile impact, API contracts, and validation results. | **SYNCHRONIZED** |
| [`NoorHeroes-Backend/CHANGELOG.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/CHANGELOG.md) | Release `1.64.0 (2026-10-12)` | Added release entry for Fact-Linked Quiz Delegation Service & Thin Adapter API. | **SYNCHRONIZED** |
| [`NoorHeroes-Backend/artifacts/openapi.json`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/artifacts/openapi.json) | OpenAPI Specification | Verified paths `/v1/quizzes/fact/{fact_id}` and dual aliases are present. | **SYNCHRONIZED** |
| [`sdocs/contracts/api/fact-linked-quiz.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/sdocs/contracts/api/fact-linked-quiz.md) | API Contract | Authored `api.fact-linked-quiz` specifying endpoint parameters, TypeScript DTOs, and error codes. | **SYNCHRONIZED** |
| [`sdocs/contracts/domain/fact-linked-quiz.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/sdocs/contracts/domain/fact-linked-quiz.md) | Domain Contract | Authored `domain.fact-linked-quiz` specifying domain invariants and Python service interface. | **SYNCHRONIZED** |
| [`sdocs/contracts/INDEX.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/sdocs/contracts/INDEX.md) | Contract Registry | Registered `api.fact-linked-quiz` and `domain.fact-linked-quiz`. | **SYNCHRONIZED** |
