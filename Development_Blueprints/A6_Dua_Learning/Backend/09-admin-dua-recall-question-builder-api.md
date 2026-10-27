# B-09 — Admin Dua Recall Question Authoring API

## 1. Feature Context
NoorHeroes — Feature A.6 Dua Learning. Implements administrative authoring, editing, inspection, and deletion of dua recall quiz questions backing PRD §4.1, §4.2, and Admin Requirements §8. As resolved in B-03 §6/§21, recall questions for Duas are scoped to the dedicated `dua_recall_question` table in `modules/dua/` (migration `0052_add_dua_progress_and_recall_tables.py`) rather than generic polymorphic question engines.

## 2. Parent Feature
A.6 Dua Learning

## 3. Sub-feature
B-09 — Admin Dua Recall Question Authoring API (`src/noorheroes/modules/dua/admin_api.py` and `admin_service.py`)

## 4. Objective
Provide a robust, 6-route administrative CRUD suite for `content_editor`-scoped administrators to manage dua recall questions:
- Create, list, inspect, replace (PUT), partially update (PATCH), and cascade-delete questions.
- Enforce pedagogical bounds: strictly 2–4 candidate options, whitespace trimming, option uniqueness, valid `correct_index` within option bounds, and length constraints.
- Calculate and return localized non-blocking guideline soft warnings (`soft_warning`) whenever a dua has more than 3 recall questions per PRD FR-6 (1–3 questions guideline).
- Guarantee cascade deletion of child `dua_recall_attempt` rows when a question is deleted, preventing foreign-key orphan integrity violations.
- Maintain immutable `AdminAuditRecord` audit trails with detailed before/after diffs and optimistic concurrency version increments (`version += 1`).
- Support multiple admin URL prefixes for seamless frontend routing (`/v1/admin/dua`, `/admin/v1/dua`, `/admin/v1/content/dua`).

## 5. Business Requirements
- PRD FR-6: 1–3 recall questions recommended per dua; surface a soft warning (non-blocking) when count > 3.
- PRD §4.1 & §4.2: Recall question authoring (question text, 2–4 options, correct answer index, optional explanation).
- Admin Requirements §8: Audit logging of all authoring changes, role-based access control (`content_editor`).

## 6. Architecture & Clean Architecture Layering
- **API Layer**: `src/noorheroes/modules/dua/admin_api.py` mounts the 6 CRUD routes with multi-prefix aliases, RBAC gating via `require_admin_scope("content_editor")`, and comprehensive OpenAPI 3.1.0 response declarations.
- **Application / Service Layer**: `DuaAdminContentService` in `src/noorheroes/modules/dua/admin_service.py` handles business logic, soft warning generation, 4-language localization, audit trail dispatch, and Redis cache invalidation.
- **Domain / Repository Layer**: `DuaRecallQuestionRepository` in `src/noorheroes/modules/dua/repository.py` handles isolated persistence and filtering strictly by `dua_id` and `question_id`.
- **Database Schema**: `dua_recall_question` and `dua_recall_attempt` tables created via Alembic migration `0052_add_dua_progress_and_recall_tables.py`.

## 7. Existing Code Reused
- `src/noorheroes/modules/dua/repository.py`: `DuaRecallQuestionRepository` and `DuaRecallAttemptRepository`.
- `src/noorheroes/modules/dua/models.py`: `DuaRecallQuestion` and `DuaRecallAttempt` ORM models.
- `src/noorheroes/modules/admin/audit/service.py`: `AdminAuditService` for persistent `AdminAuditRecord` recording.
- `src/noorheroes/core/i18n.py`: 4-language translation helpers (`get_translation`) for warning messages and errors.
- `src/noorheroes/core/auth/dependencies.py`: `require_admin_scope("content_editor")` security dependency.

## 8. Files Created / Modified
- Modified: `src/noorheroes/modules/dua/admin_api.py` (6 endpoints with aliases)
- Modified: `src/noorheroes/modules/dua/admin_service.py` (authoring business methods, soft-warning logic, cascade deletions)
- Modified: `src/noorheroes/modules/dua/admin_schemas.py` (Pydantic v2 validation models and 8 OpenAPI status response models)
- Modified: `src/noorheroes/modules/dua/repository.py` (question listing, finding, deletion methods)
- Modified: `src/noorheroes/core/i18n.py` (added `DUA_RECALL_GUIDELINE_WARNING` and admin question error keys)
- Created: `tests/modules/dua/test_admin_dua_recall_questions.py` (24 dedicated test cases)

## 9. API Contract

### Endpoints (mounted under `/v1/admin/dua`, `/admin/v1/dua`, and `/admin/v1/content/dua`):
1. `GET /v1/admin/dua/{id}/questions`
   - Returns list of questions for the dua, question count, and `soft_warning` string if count > 3.
2. `POST /v1/admin/dua/{id}/questions`
   - Creates a new question. Status 201 Created. Returns created question and updated `soft_warning` if count > 3.
3. `GET /v1/admin/dua/{id}/questions/{question_id}`
   - Retrieves single question detail. Status 200 OK. Returns 404 if question or dua does not exist.
4. `PUT /v1/admin/dua/{id}/questions/{question_id}`
   - Full replacement update. Increments `version += 1`. Logs audit record with diff. Status 200 OK.
5. `PATCH /v1/admin/dua/{id}/questions/{question_id}`
   - Partial update (selective fields: `question_text`, `options`, `correct_index`, `explanation`). Increments `version += 1`. Status 200 OK.
6. `DELETE /v1/admin/dua/{id}/questions/{question_id}`
   - Deletes question and cascades deletion of all associated `dua_recall_attempt` rows. Returns `{ "success": true, "question_id": ... }`.

### OpenAPI Response Status Codes Declared:
- `200 OK` / `201 Created`: Successful retrieval, creation, modification, or deletion.
- `400 Bad Request`: `OPTIONS_COUNT_INVALID`, `OPTION_TEXT_BLANK`, `CORRECT_INDEX_OUT_OF_BOUNDS`, `OPTIONS_MUST_BE_UNIQUE`.
- `401 Unauthorized`: Missing or invalid bearer token.
- `403 Forbidden`: Authenticated user lacks `content_editor` scope.
- `404 Not Found`: `DUA_NOT_FOUND` or `QUESTION_NOT_FOUND`.
- `422 Unprocessable Entity`: Schema structural violation (e.g. invalid JSON types).
- `429 Too Many Requests`: Rate limiting ceiling exceeded.
- `500 Internal Server Error`: Unhandled server exception with correlation ID.

## 10. Validation Rules
- **Options Count**: Between 2 and 4 options inclusive (`ck_options_count`).
- **Option Text**: Stripped of leading/trailing whitespace; non-empty strings.
- **Option Uniqueness**: All options must be unique after whitespace trimming (`OPTIONS_MUST_BE_UNIQUE`).
- **Correct Index**: Must satisfy `0 <= correct_index < len(options)`.
- **Question Text**: 1 to 1000 characters, non-blank.
- **Explanation**: Optional, up to 2000 characters.
- **Guideline Warning**: Non-blocking warning added to response if `total_questions > 3`.

## 11. Database Schema
```sql
CREATE TABLE dua_recall_question (
    id VARCHAR(36) PRIMARY KEY,
    dua_id VARCHAR(36) NOT NULL REFERENCES dua(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    options JSONB NOT NULL,
    correct_index INTEGER NOT NULL,
    explanation TEXT,
    version INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);
CREATE INDEX ix_dua_recall_question_dua_id ON dua_recall_question(dua_id);
```
Cascaded rows on deletion:
```sql
DELETE FROM dua_recall_attempt WHERE question_id = :question_id;
DELETE FROM dua_recall_question WHERE id = :question_id AND dua_id = :dua_id;
```

## 12. Security & RBAC
- Authenticated via JWT bearer token.
- Role-based authorization enforced via `require_admin_scope("content_editor")`.
- Rejects unauthenticated requests (HTTP 401).
- Rejects non-admin tokens or admin roles lacking `content_editor` scope (HTTP 403).

## 13. Localization & RTL
- 4 languages supported: English (`en`), Hindi (`hi`), Urdu (`ur`), Arabic (`ar`).
- Soft warning text dynamically localized based on `Accept-Language` header:
  - `en`: `"Pedagogical guideline recommends 1–3 recall questions per dua. Currently configured: {count} questions."`
  - `hi`: `"शैक्षणिक दिशानिर्देश प्रति दुआ 1-3 स्मरण प्रश्नों की सिफारिश करते हैं। वर्तमान में कॉन्फ़िगर किए गए: {count} प्रश्न।"`
  - `ur`: `"تعلیمی رہنمائی کے مطابق فی دعا 1 سے 3 سوالات تجویز کیے جاتے ہیں۔ فی الوقت ترتیب دیے گئے: {count} سوالات۔"`
  - `ar`: `"توصي المبادئ التوجيهية التعليمية بـ 1-3 أسئلة استرجاع لكل دعاء. الأسئلة المكونة حالياً: {count}."`

## 14. Testing Suite
Implemented in `tests/modules/dua/test_admin_dua_recall_questions.py` — **24/24 tests passing**:
1. `test_create_and_list_questions`: Full lifecycle verification of creation and listing.
2. `test_soft_warning_above_three_questions`: Validates soft warning appears when count > 3.
3. `test_soft_warning_localization`: Validates localized warnings across `en`, `hi`, `ur`, `ar`.
4. `test_create_validation_too_few_options`: Rejects < 2 options with 400.
5. `test_create_validation_too_many_options`: Rejects > 4 options with 400.
6. `test_create_validation_correct_index_out_of_bounds`: Rejects out-of-range index with 400.
7. `test_create_validation_blank_question_text`: Rejects whitespace-only question text.
8. `test_create_validation_blank_option_text`: Rejects whitespace-only options.
9. `test_get_single_question_success_and_not_found`: Verifies 200 retrieval and 404 for missing IDs.
10. `test_update_question_put_and_patch`: Full PUT and partial PATCH updates with version bump.
11. `test_delete_question_and_verify_cascade`: Verifies deletion cascades cleanly and purges attempts.
12. `test_rbac_content_editor_required`: Verifies 401 unauthenticated and 403 on insufficient scope.
13. `test_cross_feature_sync_with_b03_quiz_gating`: Verifies B-03 quiz gating reflects newly created questions.
14. `test_duplicate_options_rejection`: Rejects identical candidate options with 400 `OPTIONS_MUST_BE_UNIQUE`.
15. `test_duplicate_options_with_whitespace_rejection`: Rejects duplicates after whitespace stripping.
16. `test_patch_validation_options_and_correct_index_mismatch`: Rejects incompatible partial updates.
17. `test_patch_empty_payload_no_op`: Verifies empty PATCH is a safe no-op.
18. `test_question_text_max_length_boundary`: Validates boundary at 1000 characters and rejects 1001.
19. `test_option_text_max_length_boundary`: Validates boundary at 500 characters and rejects 501.
20. `test_explanation_max_length_boundary`: Validates boundary at 2000 characters and rejects 2001.
21. `test_version_increment_monotonicity`: Verifies version increments strictly sequentially.
22. `test_admin_audit_log_record_diffs`: Inspects `AdminAuditRecord` state diffs for before/after snapshots.
23. `test_delete_cascades_child_attempts_in_db`: Tests real DB cascade deletion with existing `DuaRecallAttempt` rows.
24. `test_admin_router_prefix_aliases`: Verifies canonical and legacy routes (`/admin/v1/content/dua`, etc.).

## 15. AI Coding Agent Implementation Steps

**Task 01 — Apply B-03's Ownership Decision**
Task ID: B-09-T01. Completed: Dedicated `dua_recall_question` tables and repositories are maintained in `modules/dua/` per PRD §4.1/§4.2 and migration `0052_add_dua_progress_and_recall_tables.py`.

**Task 02 — Implement 6-Route Authoring Suite**
Task ID: B-09-T02. Completed: Full 6-route CRUD suite implemented in `src/noorheroes/modules/dua/admin_api.py` and `src/noorheroes/modules/dua/admin_service.py` (`GET`, `POST`, `GET {id}`, `PUT`, `PATCH`, `DELETE`) with multi-prefix aliases, soft-warning calculations, transactional audit logging, optimistic concurrency, and strict option validation.

**Task 03 — Add Comprehensive Tests**
Task ID: B-09-T03. Completed: `tests/modules/dua/test_admin_dua_recall_questions.py` authoring test suite (24/24 passing in 2.67s) covering edge cases, DB cascades, partial updates, whitespace trimming, boundaries, audit diffs, and security.

**Task 04 — Final Code Review & Architecture Invariants**
Task ID: B-09-T04. Completed: All checklist items verified green. Clean Architecture layering verified across all 237 tests in `tests/architecture/`. Combined admin Dua suite: 77/77 tests passing. Full Dua module: 356/356 tests passing.

## 16. Definition of Done
Recall question authoring for Duas is fully implemented in `src/noorheroes/modules/dua/admin_api.py` and `admin_service.py`, scoped to `dua_recall_question`, seamlessly integrated with B-03 delivery, fully audited with transactional records and before/after diffs, strictly localized across 4 languages (`en`, `hi`, `ur`, `ar`), and verified with zero gaps across 24 dedicated tests, 77 admin suite tests, and 356 Dua module tests.

## 17. Final Verification Checklist
- [x] B-03's ownership decision applied consistently (dedicated `dua_recall_question` table per PRD §4.1/§4.2 and migration 0052)
- [x] Full 6-route CRUD suite (`GET`, `POST`, `GET {id}`, `PUT`, `PATCH`, `DELETE`) with router aliases
- [x] Cascade deletion of `dua_recall_attempt` child records on question deletion
- [x] Soft guideline warning (> 3 questions) localized in `en`, `hi`, `ur`, `ar`
- [x] Strict option bounds (2–4 unique options, whitespace trimmed, valid `correct_index`)
- [x] Transactional audit trail (`AdminAuditRecord`) with before/after state diffs
- [x] `content_editor` RBAC scope enforced via `require_admin_scope("content_editor")`
- [x] Question count correctly reflected in B-03's `total_available`
- [x] 24/24 tests passing in `test_admin_dua_recall_questions.py`
- [x] 77/77 tests passing in combined admin Dua suite
- [x] 356/356 tests passing across all Dua module suites
- [x] 237 architectural invariant tests passing with zero layering violations
