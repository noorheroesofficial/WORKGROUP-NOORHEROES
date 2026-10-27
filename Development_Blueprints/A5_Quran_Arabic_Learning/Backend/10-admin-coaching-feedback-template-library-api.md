# B-10 — Admin Coaching Feedback Template Library API

> **Status:** ✅ **COMPLETED & VERIFIED**  
> **Target Framework:** FastAPI (Python 3.12+) / SQLAlchemy 2.0 (Async) / Pydantic v2 / Redis 7  
> **Architecture Pattern:** Clean Architecture, Modular Monolith, Strict Content Editor RBAC, Zero-Bypass Multi-Lingual Theological Judgment Blocklist Validator (en/hi/ur/ar), Dual-Path Audit Logging (AdminAuditRecord: accepted vs rejected_blocklist_violation), Permanent Hard-Delete Prohibition (HTTP 405), Live B-04 In-Memory Runtime Propagation  
> **Test Coverage:** 80/80 Dedicated Tests Passing (671 Total Learning Tests Passing, 45 AI Safety & trigger Tests Passing, 100% Green in CI)

## 1. Feature Context
Part of Feature A.5 (Quran & Arabic Learning). Manages the AI Pronunciation coaching-feedback text templates that B-04 selects from, enforcing a hard, non-bypassable blocklist against religious-judgment language at save time.

## 2. Parent Feature
A.5 — Quran & Arabic Learning

## 3. Sub-feature
B-10 — Admin Coaching Feedback Template Library API (Admin API)

## 4. Objective
Provide CRUD for coaching feedback templates with mandatory blocklist content-safety validation that cannot be bypassed by any admin role, plus rejected-attempt audit logging for content-safety monitoring.

## 5. Business Requirements
- Admin Requirements §8: full CRUD behind `content_editor` role + mandatory blocklist validation enforced as a hard, non-bypassable rule — a template containing a blocked term cannot be saved as active, regardless of admin role.
- §5 item 4 (Backend AI prompt): `FEEDBACK_TEMPLATE_LIBRARY` must never contain language implying religious/worship acceptance or rejection (banned substrings: "accepted", "rejected", "valid prayer", "invalid", etc.); an automated content-safety test loading the entire library must be a mandatory CI gate.

## 6. Existing Architecture
Modular monolith; content-safety validation logic follows the existing `ai_safety` context's evaluation pattern (`POST /v1/ai-safety/evaluate`, per architecture doc §5.3/§6 item 3) — this blueprint's blocklist validator should be implemented as a reusable service callable both from this admin write-path and from B-04's read-path CI test, avoiding two divergent implementations of "what counts as blocked language."

## 7. Existing Code to Reuse
- `ai_safety` context's evaluation service pattern.
- `get_current_admin`, admin `audit_log` mechanism (same as B-09).

## 8. Files Created
- `src/noorheroes/modules/learning/feedback_template_models.py` (`FeedbackTemplate` ORM model mapped to `feedback_templates` with UUIDv7 PK, DB check constraints, dual-key serialization, zero audio columns)
- `src/noorheroes/modules/learning/feedback_template_repository.py` (`FeedbackTemplateRepository` with soft-deactivation and prohibited hard-delete raising `HardDeleteProhibitedError`)
- `src/noorheroes/modules/learning/schemas/feedback_template.py` (Pydantic v2 schemas: `FeedbackTemplateCreateRequest`, `FeedbackTemplateUpdateRequest`, `FeedbackTemplateResponse`, `FeedbackTemplateListResponse`, `FeedbackBlocklistResponse`, and granular OpenAPI 3.1.0 response dicts)
- `src/noorheroes/modules/ai_safety/religious_judgment_blocklist_validator.py` (`ReligiousJudgmentBlocklistValidator` with zero-bypass multi-lingual validation and NextJS N-03 catalog helper)
- `src/noorheroes/modules/learning/services/feedback_template_service.py` (`FeedbackTemplateService` orchestrating CRUD, non-bypassable blocklist validation, dual-path `AdminAuditRecord` persistence, and live runtime cache updates)
- `src/noorheroes/modules/learning/admin_api.py` (`LearningAdminRouter` with endpoints for feedback templates and blocklist catalog)
- `alembic/versions/0049_add_feedback_templates.py` (Alembic migration creating `feedback_templates` table, check constraints, and composite indices)
- `tests/modules/learning/test_feedback_template_models.py` (8 tests)
- `tests/modules/learning/test_feedback_template_repository.py` (6 tests)
- `tests/modules/learning/test_admin_feedback_template_api.py` (24 tests)
- `tests/modules/ai_safety/test_feedback_template_blocklist.py` (22 tests)
- `tests/modules/ai_safety/test_religious_judgment_blocklist_validator.py` (20 tests)

## 9. Files Modified
- `src/noorheroes/modules/learning/feedback_template_library.py` (added dynamic in-memory propagation, fallback resolution, and exported `FEEDBACK_TEMPLATES`)
- `src/noorheroes/modules/learning/deps.py` (registered `get_feedback_template_repository` and `get_feedback_template_service`)
- `src/noorheroes/core/exceptions.py` (added `ReligiousJudgmentBlocklistViolationError`, `FeedbackTemplateNotFoundError`, and `HardDeleteProhibitedError`)
- `src/noorheroes/core/i18n.py` (added 4-language translations for `RELIGIOUS_JUDGMENT_BLOCKLIST_VIOLATION`, `FEEDBACK_TEMPLATE_NOT_FOUND`, and `HARD_DELETE_PROHIBITED` across `en`, `hi`, `ur`, `ar`)
- `src/noorheroes/api/v1/router.py` (mounted `admin_learning_router` under `/v1`)
- `src/noorheroes/main.py` (added OpenAPI tags for Admin Coaching Feedback Templates)
- `FAST-API-INSTRUCTIONS.md` (updated Sections 5.2, 5.5, 6, 6.7, 7, 8, 9 Scenario 24, 10, 11 Rules 12/13, 12, 15)
- `MASTER-README.md` (added Section 11.43 and Scenarios S-192 to S-204)
- `docs/NoorHeroes_Consolidated_Execution_Blueprint.md` (updated Phase 6 Overview, Item 179 row, next pointer to Item 180, and Phase 5 gate checklist)
- `src/noorheroes/modules/learning/README.md` (added Section 2.18, Scenarios S-189 to S-202, and 716 test matrix metrics: 671 learning tests across 40 files + 45 AI safety & trigger tests, 100% green)

## 10. Backend Requirements
- **Model**: `feedback_template` (`id`, `confidence_band`, `locale`, `text`, `is_active`, `created_at`, `updated_at`).
- **Blocklist validator**: `ReligiousJudgmentBlocklistValidator.validate(text) -> ValidationResult` — checks against a maintained blocklist (banned substrings: "accepted", "rejected", "valid prayer", "invalid", and any additional maintained terms), sourced from a configurable list (exposed via `GET /admin/v1/config/feedback-blocklist` for the NextJS editor to fetch and pre-check client-side — server-side check is still authoritative and mandatory).
- **Save enforcement**: on create/update, run the validator; if any match, reject the save entirely for **every** admin role — no override/bypass parameter exists anywhere in the request schema or service logic.
- **Rejected-attempt audit logging**: a blocklist rejection still writes an audit_log entry (marked as a rejected attempt) for content-safety monitoring, separate from normal accepted-mutation audit entries.
- **CI-blocking content-safety test**: a test loading the entire live template library and asserting zero matches against the blocklist — this must be wired as a mandatory, non-bypassable CI gate on any PR touching this service (DevOps cross-reference).

## 11. KMP Requirements
N/A (admin-only; consumed indirectly via B-04's runtime template selection).

## 12. NextJS Requirements
Consumed by `N-03 Coaching Feedback Template Library Manager`.

## 13. API Contract

**`POST /v1/admin/learning/feedback-templates`**
- **Auth:** `get_current_admin`, requires `content_editor` role
- **Request:** `{ "confidence_band": "high|medium|low", "locale": "en|hi|ar|ur", "text": "..." }`
- **Response 201:** created template, OR `422` with the matched blocked term highlighted if validation fails
- **Error Responses:** `401`, `403`, `422` (blocklist match — response includes the matched term(s) for editor feedback)

**`PUT /v1/admin/learning/feedback-templates/{id}`** — same validation applied on every update.

**`GET /v1/admin/config/feedback-blocklist`**
- Returns the maintained blocklist term list, for the NextJS editor's client-side pre-check (server-side check in the above routes remains authoritative regardless).

## 14. Database Requirements
`feedback_template` table: `id PK`, `confidence_band`, `locale`, `text`, `is_active BOOLEAN`, `created_at`, `updated_at`. No blob/audio-adjacent columns (this table only ever holds text). Reuses existing admin `audit_log` table for both accepted-mutation and rejected-attempt entries (add an `outcome` or `action_type` discriminator if the existing audit_log schema doesn't already support a rejected-attempt category — confirm against the `admin` context's actual schema before assuming).

## 15. Validation
- `confidence_band` and `locale` enum-validated.
- `text` non-empty, run through the blocklist validator on every create/update — no path exists to save without this check.

## 16. Authentication
Bearer JWT, `get_current_admin`.

## 17. Authorization
`content_editor` role required for CRUD; the blocklist-fetch endpoint may be readable by any authenticated admin role.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Blocklist match on save | `422`, matched term(s) highlighted in response, save rejected for every role, rejected-attempt audit entry written |
| Blocklist-config fetch failure (client-side pre-check) | Client falls back to relying on server-side authoritative check (no degraded server-side enforcement ever occurs) |
| Unauthorized/forbidden | `401`/`403` |
| Invalid `confidence_band`/`locale` | `422` |

## 19. Offline First
N/A (admin backend).

## 20. Local Data
N/A (admin backend).

## 21. Localization
`locale` field is a first-class part of the template model — templates are authored per-locale, not auto-translated, given the theological-safety sensitivity of the copy.

## 22. RTL
N/A at API layer; Arabic/Urdu locale template text itself must be authored correctly RTL by the content editor (UI concern, owned by N-03).

## 23. Analytics
N/A (admin audit logging only).

## 24. Performance
Template library is small and infrequently updated — no special caching required beyond B-04's existing template-selection read pattern.

## 25. Security
This is the second most safety-critical control in the feature after B-04's zero-retention guarantee — the blocklist enforcement has zero bypass path for any role, verified via CI-blocking test and negative-path integration tests attempting to bypass via direct API calls (not just the UI).

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0, Pydantic v2. No new dependencies (blocklist matching is simple substring/regex logic, no ML/NLP library required per the PRD's stated approach).

## 27. Testing
- Unit: blocklist validator against known-bad phrases ("accepted", "rejected", "valid prayer", "invalid", and maintained list) and known-good coaching phrases (no false positives on benign text).
- Integration: attempt to save a blocklisted template via the Admin API directly (bypassing any UI) — rejected server-side, for every simulated admin role, confirming no override parameter exists.
- Integration: rejected attempt writes a distinct audit_log entry.
- CI-blocking: full live-library scan test (also referenced from B-04) — zero matches.
- Integration: accepted template becomes selectable by B-04's `FeedbackTemplateLibrary` immediately.

## 28. Documentation
OpenAPI docstring explicitly states there is no bypass path for any admin role, and links to the CI-blocking test as the enforcement mechanism.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create `feedback_template` Model & Migration**
- Task ID: B-10-T01
- Status: Completed ✅
- Files Created: `src/noorheroes/modules/learning/feedback_template_models.py`, `alembic/versions/0049_add_feedback_templates.py`.
- Implementation Details: UUIDv7 PK, DB check constraints on `confidence_band` (`high`, `medium`, `low`, `needs_coaching`) and `locale` (`en`, `hi`, `ur`, `ar`), dual-key dictionary serialization (`id` and `template_id`), zero audio/blob columns.
- Dependencies: None.
- Definition of Done: Migration applies cleanly; model tests pass (8 tests).

**Task 02 — Implement `ReligiousJudgmentBlocklistValidator`**
- Task ID: B-10-T02
- Status: Completed ✅
- Files Created: `src/noorheroes/modules/ai_safety/religious_judgment_blocklist_validator.py`.
- Existing Architecture to Follow: `ai_safety` context's existing evaluation-service pattern.
- Implementation Details: Zero-bypass multi-lingual validation across `en`, `hi`, `ur`, `ar`; normalized substring/token scanning against banned theological judgment terms; NextJS N-03 client pre-check catalog helper (`get_feedback_blocklist_terms()`).
- Business Rules: Zero bypass parameter anywhere in the function signature or call graph for any administrative role.
- Dependencies: None.
- Definition of Done: Unit tests pass against known-bad/known-good phrase sets with 0 false positives (20 validator tests + 22 safety tests = 42 tests).

**Task 03 — Implement `FeedbackTemplateRepository`**
- Task ID: B-10-T03
- Status: Completed ✅
- Files Created: `src/noorheroes/modules/learning/feedback_template_repository.py`.
- Implementation Details: Async SQLAlchemy 2.0 CRUD; soft-deactivation (`is_active=False`); hard `delete()` unconditionally raises `HardDeleteProhibitedError`.
- Dependencies: B-10-T01.
- Definition of Done: Repository unit tests pass (6 tests).

**Task 04 — Implement `FeedbackTemplateService`**
- Task ID: B-10-T04
- Status: Completed ✅
- Files Created: `src/noorheroes/modules/learning/services/feedback_template_service.py` (with module re-export in `admin_feedback_template_service.py`).
- Implementation Details: Orchestrates non-bypassable blocklist validation, repository persistence, dual-path `AdminAuditRecord` logging (`accepted` vs `rejected_blocklist_violation` with matched terms and candidate text), and live in-memory runtime updates to B-04's `FeedbackTemplateLibrary`.
- Dependencies: B-10-T02, B-10-T03.
- Definition of Done: Service and integration tests pass.

**Task 05 — Wire Admin Router with RBAC**
- Task ID: B-10-T05
- Status: Completed ✅
- Files Created/Modified: `src/noorheroes/modules/learning/admin_api.py`, `src/noorheroes/api/v1/router.py`, `main.py`.
- Implementation Details: `content_editor` role check via `require_admin_role("content_editor")` on all mutating routes; `DELETE` route returning HTTP 405 `HARD_DELETE_PROHIBITED`; pre-check catalog mounted at `GET /admin/v1/config/feedback-blocklist` and canonical `/v1/admin/config/feedback-blocklist`.
- Dependencies: B-10-T04.
- Definition of Done: Endpoints reachable, RBAC verified.

**Task 06 — Tests**
- Task ID: B-10-T06
- Status: Completed ✅
- Objective: Full coverage per §27, including the CI-blocking live-library scan.
- Files Created: `tests/modules/learning/test_admin_feedback_template_api.py` (24 tests), `tests/modules/learning/test_feedback_template_models.py` (8 tests), `tests/modules/learning/test_feedback_template_repository.py` (6 tests), `tests/modules/ai_safety/test_feedback_template_blocklist.py` (22 tests), `tests/modules/ai_safety/test_religious_judgment_blocklist_validator.py` (20 tests).
- Dependencies: B-10-T01–T05.
- Definition of Done: All 80 dedicated tests green in CI; CI-blocking full library scan gate configured and passing (671 total learning tests passing, 100% green).

**Task 07 — API Documentation**
- Task ID: B-10-T07
- Status: Completed ✅
- Dependencies: B-10-T05.
- Definition of Done: OpenAPI 3.1.0 specifications complete covering 10 status codes (`200`, `201`, `400`, `401`, `403`, `404`, `405`, `422`, `429`, `500`), zero-bypass architectural guarantee documented across `FAST-API-INSTRUCTIONS.md`, `MASTER-README.md`, and `learning/README.md`.

## 30. Definition of Done
✅ **FULLY ACHIEVED**: Admin CRUD live with `content_editor` RBAC, non-bypassable blocklist enforcement with zero bypass for any admin role across 4 languages (`en`, `hi`, `ur`, `ar`), dual-path audit logging (`accepted` vs `rejected_blocklist_violation`), permanent hard-delete prohibition (HTTP 405 / `HardDeleteProhibitedError`), live B-04 in-memory runtime propagation, NextJS N-03 client pre-check catalog, CI-blocking content-safety test wired as a mandatory gate, fully tested (80 dedicated tests, 671 total learning module tests, 45 AI safety tests) and documented across `FAST-API-INSTRUCTIONS.md`, `MASTER-README.md`, and `learning/README.md`.

## 31. Final Verification Checklist
- [x] Blocklist validator rejects all known-bad phrases and does not false-positive on known-good coaching copy
- [x] No override/bypass parameter exists in any code path for any admin role
- [x] Rejected-attempt audit entries distinct from accepted-mutation entries
- [x] CI-blocking full-library scan test passes and is a mandatory, non-bypassable gate
- [x] `content_editor` role strictly enforced
- [x] Accepted templates immediately selectable by B-04
- [x] Full test suite green in CI
