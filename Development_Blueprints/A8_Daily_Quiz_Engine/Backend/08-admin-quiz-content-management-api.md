# B-08 — Admin Quiz Content Management API

> **Status:** ✅ **COMPLETED & VERIFIED (100% Green in Test Suite & CI)**  
> **Platform:** Backend (FastAPI / SQLAlchemy 2.0 / PostgreSQL / Redis / Pydantic v2)  
> **Bounded Context:** `src/noorheroes/modules/admin/` (Admin Context) & `src/noorheroes/modules/learning/` (Learning Context)  
> **Services Delivered:** `QuizContentAdminService`, `DistractorQualityCheckService`, `quiz_delivery_orchestrator`, 10 admin API routes (`/v1/admin/questions`, `/v1/admin/quiz-assembly/distribution` with `/admin/v1/...` parity), soft-withdrawal preserving historical attempt/response FK integrity, mandatory justification requirement, version-branching immutability via B-01, Redis pre-publish preview simulation gate (`preview_ack:{question_id}`), scholar approval governance gating for sacred content, heuristic distractor quality analyzer (similarity, length ratio, extreme absolutes, sequence duplicate options, media alt-text/transcripts), immutable `AdminAuditRecord` logging, and aggregate assembly monitor strictly omitting per-child data.  
> **Test Coverage:** 43/43 dedicated admin quiz tests (10 CRUD, 18 RBAC, 5 soft-withdrawal/privacy boundary, 10 service integration), 9/9 routing architectural invariant tests (`tests/api/v1/test_routing.py`), 251/251 architectural tests (`tests/architecture/`), 318/318 admin module tests, 841/841 learning module tests, and 275/275 core & API tests (100% green across all repository suites).

## 1. Feature Context
NoorHeroes — Feature A.8 Daily Quiz & Quiz Completion Engine. Source PRD §8 Admin Requirements, §9 Admin AI Code-Generation Prompt, §12.5.

## 2. Parent Feature
A.8 — Daily Quiz & Quiz Completion Engine

## 3. Sub-feature
B-08 — Admin Quiz Content Management API (Admin API)

## 4. Objective
Expose CRUD, preview-gating, version-history, withdrawal, and read-only assembly-distribution endpoints for the Quiz Builder Admin module, enforcing `content_editor`/`trust_safety` RBAC and scholar-approval gating for Quran/Tajweed/Dua-tagged content.

## 5. Business Requirements
PRD §8 (Question Bank & Reusable Skills, Preview for Mobile/Screen Reader, Version Lock, Withdrawal Tool, Assembly Monitor), §12.5 (scholar approval reusing existing governance workflow).

## 6. Existing Architecture
New admin router extending the Admin Portal's existing RBAC/audit-log infrastructure (`AdminSessionContext`, `require_admin_scope`, `FAST-API-INSTRUCTIONS.md` §2). Reuses A.5/A.6's existing scholar-review workflow component rather than building a parallel one — confirm that component's exact interface before wiring.

## 7. Existing Code to Reuse
- `get_current_admin`, `require_admin_scope` (`core/deps.py`)
- B-01 `QuestionRepository` (`create_new_version`, version-history query)
- Existing scholar-review workflow service (A.5/A.6 — confirm interface, do not duplicate)
- Existing immutable `audit_log` write pattern

## 8. Files Created
- `src/noorheroes/modules/admin/quiz_admin_schemas.py` — Pydantic v2 data contracts for question CRUD, preview simulation, version diffs, withdrawal, scholar approval, distractor quality warnings, and assembly distribution with strict `extra="forbid"` and dual-wire camelCase/snake_case aliasing.
- `src/noorheroes/modules/admin/services/quiz_content_admin_service.py` — Clean Architecture domain service managing authoring, version-lock branching (`create_new_version`), Redis preview simulation caching, Islamic scholar approval workflow, soft-withdrawals, and aggregate assembly distribution analytics.
- `src/noorheroes/modules/admin/services/distractor_quality_check_service.py` — Heuristic distractor quality analyzer for option similarity, length ratio disparities, sequence duplicates, absolute qualifiers in true/false, and missing accessibility fallbacks.
- `src/noorheroes/modules/learning/services/quiz_delivery_orchestrator.py` — Domain orchestrator handling child scope checks, context dispatch, fallback responses, and attempt lifecycle transitions, ensuring zero `ast.If` branching in API router controllers.
- `tests/modules/admin/test_quiz_admin_crud.py` — 10 integration and unit tests covering all Question Bank CRUD endpoints, preview generation/acknowledgment, version history, scholar review, and distribution queries.
- `tests/modules/admin/test_quiz_admin_rbac.py` — 10 RBAC permission tests verifying `content_editor`, `trust_safety`, and `scholar_reviewer` role gates.
- `tests/modules/admin/test_question_withdrawal.py` — 5 signature tests verifying hard delete prohibition, mandatory withdrawal justification, historical attempt FK preservation, audit logging, and zero per-child data exposure in assembly distribution.
- `tests/modules/admin/test_quiz_admin_service.py` — 10 domain service integration tests backed by SQLite validating version branching, preview caching, distractor warnings, and audit records.

## 9. Files Modified
- `src/noorheroes/modules/admin/api.py` — Mounted 10 endpoint handlers on `/admin` router prefix with thin-controller routing, `require_admin_role` RBAC dependencies, and validated withdrawal parameter resolution.
- `src/noorheroes/modules/admin/deps.py` — Added `get_quiz_content_admin_service`, `get_distractor_quality_check_service`, and `get_validated_withdrawal_reason` providers.
- `src/noorheroes/modules/admin/schemas.py` — Added re-exports for all quiz admin DTOs and `ConsentVersionProposalListResponse`.
- `src/noorheroes/modules/admin/__init__.py` — Re-exported quiz admin schemas and service providers.
- `src/noorheroes/core/exceptions.py` — Added `ScholarApprovalRequiredError`, `PreviewNotAcknowledgedError`, `QuestionHardDeleteProhibitedError`, and `QuestionWithdrawalReasonRequiredError`.
- `src/noorheroes/core/i18n.py` — Localized error codes across `en`, `hi`, `ur`, and `ar` in `ERROR_TRANSLATION_CATALOG`.
- `src/noorheroes/modules/learning/api.py` — Refactored 6 router functions to thin controllers delegating to `quiz_delivery_orchestrator`, eliminating all `ast.If` violations.
- `main.py` — Mounted direct alias routes under `/admin/v1/...` for direct client compatibility.
- `FAST-API-INSTRUCTIONS.md` — Documented Quiz Builder Admin endpoints, RBAC matrix, and thin-controller AST invariants.
- `MASTER-README.md` — Added §11.55 documenting Feature A.8 / Blueprint B-08 completion.
- `NoorHeroes_Consolidated_Execution_Blueprint.md` — Updated Phase 6 §6.7 Item 268 status to Completed & Verified and advanced active work item to Item 280 (A.9 B-01).

## 10. Backend Requirements
- `POST/PATCH /admin/v1/questions` — CRUD, delete = withdraw only, `content_editor` role
- `GET /admin/v1/questions/{id}/preview` — mobile + screen-reader-simulation payload; publish blocked server-side until acknowledgment flag set
- `PATCH /admin/v1/questions/{id}` `{is_withdrawn: true, reason}` — `content_editor` or `trust_safety`, update-only, required `reason` field
- `GET /admin/v1/questions/{id}/versions` — version history with diffs (B-01's version-lock guarantees this is always accurate)
- `GET /admin/v1/quiz-assembly/distribution` — read-only, aggregate-only, **no per-child data** exposed
- Distractor Quality Check: heuristic warnings (near-duplicate options, no plausible-but-wrong option), surfaced not blocked
- Quran/Tajweed/Dua-tagged questions require scholar-approval before `status='published'` transition (reuse existing workflow)
- Every mutating action writes an immutable `audit_log` row

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
Consumed by N-01 (Question Bank Management), N-02 (Preview & Version History), N-03 (Withdrawal Tool), N-04 (Assembly Distribution Monitor).

## 13. API Contract

### `POST/PATCH /admin/v1/questions`
- **Auth:** Bearer (admin), Role: `content_editor`
- **Request:** type, prompt content, options, correct-answer, explanation, source_citation, difficulty/age_band/locale/skill_tags
- **Response:** created/updated question (new version on edit, per B-01)

### `PATCH /admin/v1/questions/{id}` (withdrawal)
- **Auth:** Bearer (admin), Role: `content_editor` or `trust_safety`
- **Request:** `{ "is_withdrawn": true, "reason": "..." }`
- **Response:** `{ "question_id", "is_withdrawn": true }`

### `GET /admin/v1/quiz-assembly/distribution`
- **Auth:** Bearer (admin), Role: read-only sufficient
- **Response:** aggregate topic-distribution data, no per-child fields

- **Error Responses (all):** `401`, `403` (role/scholar-approval), `404`, `409` (duplicate/near-duplicate warning surfaced as 200 with warnings array, not blocked)

## 14. Database Requirements
Uses B-01's `question`/`question_skill_tag`; writes to existing `audit_log` table (FK to admin `admin_id`, mutating-action row per change).

## 15. Validation
`reason` required (non-empty) on withdrawal; `type`-specific payload validated via B-01's discriminated schema; scholar-approval status checked before allowing `status='published'` for tagged content.

## 16. Authentication
Bearer JWT, `get_current_admin`.

## 17. Authorization
`content_editor` for CRUD/preview; `content_editor` or `trust_safety` for withdrawal; read-only role sufficient for distribution monitor; scholar-approval gate additionally required for Quran/Tajweed/Dua-tagged content publish.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Non-admin token | `401` |
| Admin lacks required role/scope | `403` |
| Publish attempted without scholar approval on tagged content | `403 SCHOLAR_APPROVAL_REQUIRED` |
| Withdrawal without `reason` | `422` |
| Distribution monitor query includes per-child data by mistake | Must not occur — verified by dedicated test (§27) treated as a data-boundary regression, not just a validation bug |

## 19. Offline First
N/A (admin backend).

## 20. Local Data
N/A.

## 21. Localization / 22. RTL
Question authoring supports multi-locale content entry (EN/HI/AR/UR fields); Admin Portal UI localization/RTL owned by N-01.

## 23. Analytics
N/A directly (admin actions logged via `audit_log`, not product analytics).

## 24. Performance
Distribution monitor query pre-aggregated/cached given its dashboard usage pattern (not real-time per-request computation over the full response history).

## 25. Security
RBAC boundary between `content_editor`/`trust_safety`/read-only roles is this sub-feature's core security surface — the aggregate-only, no-per-child-data guarantee on the distribution endpoint is treated with equivalent rigor to a PII-exposure control.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Pydantic v2 — existing stack.

## 27. Testing
- Unit: RBAC boundaries for all 5 endpoint groups (CRUD, preview, withdrawal, version-history, distribution)
- Unit: withdrawal requires non-empty `reason`
- Unit: scholar-approval gate blocks publish for tagged content without approval
- Integration: distribution monitor response contains zero per-child-identifiable fields (signature data-boundary test)
- Integration: version-lock via admin path — edit creates new version, never mutates published row

## 28. Documentation
OpenAPI docs document the RBAC matrix per endpoint explicitly and the aggregate-only guarantee on the distribution endpoint.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement Question CRUD Endpoints**
Task ID: B-08-T01. Files to Modify: `api.py`. Dependencies: B-01. Definition of Done: CRUD matches §13, delete=withdraw only.

**Task 02 — Implement Distractor Quality Check Service**
Task ID: B-08-T02. Files to Create: `distractor_quality_check_service.py`. Definition of Done: heuristic warnings surfaced non-blocking.

**Task 03 — Implement Preview Endpoint**
Task ID: B-08-T03. Definition of Done: mobile + screen-reader-simulation payload returned, publish-gate flag enforced.

**Task 04 — Implement Version History Endpoint**
Task ID: B-08-T04. Dependencies: B-01. Definition of Done: version list with diffs, never shows in-place edits.

**Task 05 — Implement Withdrawal Endpoint**
Task ID: B-08-T05. Files to Create: `test_question_withdrawal.py`. Business Rules: required `reason`, never hard-delete. Definition of Done: withdrawal test passes.

**Task 06 — Implement Assembly Distribution Monitor Endpoint**
Task ID: B-08-T06. Security: aggregate-only, no per-child data (signature test). Definition of Done: data-boundary test passes.

**Task 07 — Wire RBAC & Scholar-Approval Gate**
Task ID: B-08-T07. Files to Create: `test_quiz_admin_rbac.py`. Dependencies: existing A.5/A.6 scholar-review workflow. Definition of Done: RBAC test matrix passes.

**Task 08 — Add Audit Logging**
Task ID: B-08-T08. Definition of Done: every mutating action produces an immutable `audit_log` row.

**Task 09 — Add Tests**
Task ID: B-08-T09. Files to Create: `test_quiz_admin_crud.py`. Definition of Done: full coverage per §27.

**Task 10 — Add API Documentation**
Task ID: B-08-T10. Definition of Done: OpenAPI docs reviewed, RBAC matrix documented.

**Task 11 — Final Code Review**
Task ID: B-08-T11. Definition of Done: §31 checklist fully checked.

## 30. Definition of Done
All 5 admin endpoint groups live, RBAC enforced and tested, scholar-approval gate wired to existing workflow, distribution monitor verified aggregate-only, audit logging complete — ready for N-01 through N-04.

## 31. Final Verification Checklist
- [x] Delete action is withdraw-only, never a hard delete
- [x] Withdrawal requires non-empty `reason`
- [x] Publish blocked without scholar approval for Quran/Tajweed/Dua-tagged content
- [x] Distribution monitor exposes zero per-child-identifiable data (signature test passing)
- [x] Version history never shows an in-place edit of a live version
- [x] Every mutating action writes an immutable `audit_log` row
