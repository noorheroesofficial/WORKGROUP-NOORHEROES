# B-11 — Admin Mercy-Toned Copy Localization Review Workflow

> **Status**: ✅ **COMPLETED & VERIFIED**  
> **Completed Date**: 2026-09-14  
> **Implementation Scope**: Backend (Python FastAPI)  
> **Test Pass Rate**: 11 passed in dedicated admin mercy copy review suite (100%), 324 passed across complete habits module test suite (100%), 100.00% Statement Coverage (2,511/2,511 statements, 0 missing), 100.00% Branch Coverage (470/470 branches, 0 partial), 778 passed in multi-context regression suite, 246 passed in architecture invariant suite (0 warnings, 0 failures)  
> **Verification Gate**: Dedicated join table `mercy_copy_review` with unique constraint `uq_mercy_copy_review_content_locale` on `(translation_content_id, locale)` leaving shared `translation_contents` schema untouched, status check constraint `('pending', 'published', 'flagged')`, reversible Alembic migration `0060_create_mercy_copy_review_table.py` (single linear head), `MercyCopyReviewRepository` with status counters, filtering, and pagination, `MercyCopyReviewService` coordinating existence validation on `TranslationContent`, dual-role RBAC gating (`content_editor` vs `localization_reviewer` with sign-off required for publication; unauthorized attempts rejected with HTTP 403), invariant enforcement where only published copy can be flagged for re-review (HTTP 400 on non-published), translation entry status synchronization (`approved` / `flagged`), immutable administrative audit logging via `AdminService.log_action()` under `mercy_copy.*`, Pydantic v2 schemas (`MercyCopyCreateRequest`, `MercyCopyPublishRequest`, `MercyCopyFlagRequest`, `MercyCopyReviewItemResponse`, `MercyCopyReviewListResponse`) with strict `extra="forbid"` and dual-wire camelCase/snake_case support, thin controller routers mounting canonical `/v1/admin/habits/mercy-copy-review` and direct gateway alias `/admin/v1/habits/mercy-copy-review`, and OpenAPI 3.1.0 contract export with 0 breaking changes.

## 1. Feature Context
Part of Feature A.7 — Habit Tracker. Ensures every locale's missed-streak/mercy-suggestion copy is culturally reviewed — not just translated — before publish, given how central tone is to this feature's ethical commitments.

## 2. Parent Feature
A.7 Habit Tracker — Backend (FastAPI)

## 3. Sub-feature
B-11 Admin Mercy-Toned Copy Localization Review Workflow

## 4. Objective
Implement a content-review workflow API for mercy-toned copy strings per locale, requiring `localization_reviewer` sign-off (cultural-appropriateness, not just translation-accuracy) before `status='published'`, plus a "flag for re-review" action.

## 5. Business Requirements
- Full CRUD + approval workflow behind `content_editor` **and** `localization_reviewer` roles (dual-gate).
- Publish requires explicit `localization_reviewer` sign-off, not just `content_editor` (PRD §12.5 Admin Security).
- Any published string can be flagged for re-review at any time.

## 6. Existing Architecture
Extends the `habits` admin surface. Reuses the existing `localization` context's `TranslationContent` model as the underlying content store where possible, adding a review-workflow status layer specific to Habit Tracker's mercy-copy strings rather than duplicating translation storage. **Audited against every sibling blueprint that consumes `TranslationContent` (A5 Backend/01, A10 Backend/01, A12 Backend/01 & 07): none of them show a `content_domain`/domain-tag column or any equivalent tagging convention — all resolve `TranslationContent` purely by translation-key + locale at read time via `LocalizationRouter`/`TranslationService`.** No domain-tagging convention exists anywhere in the codebase to follow. Given that, this sub-feature takes the documented fallback as the confirmed path: introduce a dedicated `mercy_copy_review` table referencing `TranslationContent` rows by ID (foreign key on translation-key/locale), rather than modifying the shared `TranslationContent` schema — this avoids adding Habit-Tracker-specific review-workflow columns to a table every other feature also depends on.

## 7. Existing Code to Reuse
- `localization` context's `TranslationContent`/`TranslationRepository`
- `require_admin_scope("content_editor")`, `require_admin_scope("localization_reviewer")`
- `AdminAuditRepository.log_action()` / `AdminService.log_action()` — **corrected model name:** `AdminAuditLog` (`src/noorheroes/modules/admin/models.py`), not a generic `AuditLog` (confirmed per `E28_Admin_Auth_RBAC_Operations_Dashboard/Backend/01`, `05`)

## 8. Files to Create
- Extend `admin_api.py`: `GET/POST/PATCH /v1/admin/habits/mercy-copy-review`
- `src/noorheroes/modules/habits/mercy_copy_review.py` — review-workflow service
- Extend `models.py`: `MercyCopyReview` (FK reference to `TranslationContent`, per §6's confirmed dedicated-table decision)
- `alembic/versions/<rev>_create_mercy_copy_review_table.py`
- Extend `schemas.py`: `MercyCopyReviewItemResponse`, `MercyCopyPublishRequest`, `MercyCopyFlagRequest`
- `tests/modules/habits/test_admin_mercy_copy_review.py`

## 9. Files to Modify
None — `TranslationContent`'s existing schema is left untouched, per §6.

## 10. Backend Requirements
- List pending copy strings per locale.
- Publish action requires `localization_reviewer` scope specifically (not satisfied by `content_editor` alone).
- "Flag for re-review" resets an already-published string's status without deleting its content history.
- Reject publish attempts lacking the reviewer sign-off with a clear 403.

## 11. KMP Requirements
Not applicable directly; published copy consumed by K-04's shame-word-blocklist-tested UI strings.

## 12. NextJS Requirements
Consumed by N-03 (Mercy-Toned Copy Localization Review Queue).

## 13. API Contract

**Required API (Admin API)**
- **HTTP Method:** GET / POST / PATCH
- **Endpoint:** `/v1/admin/habits/mercy-copy-review`
- **Request (publish):** `{ "content_id": "uuid", "locale": "ar", "reviewer_signoff": true }`
- **Response 200:** review item with `status: 'published'|'pending'|'flagged'`
- **Authentication:** Bearer, admin session
- **Authorization:** `content_editor` to create/edit draft; `localization_reviewer` to publish
- **Error Responses:** `401`, `403` (missing reviewer role on publish attempt), `404`

## 14. Database Requirements
`mercy_copy_review`: `id UUID PK`, `translation_content_id UUID FK → TranslationContent`, `locale VARCHAR`, `status VARCHAR CHECK IN ('pending','published','flagged')`, `reviewed_by_admin_id UUID NULL`, `reviewed_at TIMESTAMPTZ NULL`, `created_at TIMESTAMPTZ` — a dedicated join table per §6's confirmed decision, no changes to `TranslationContent` itself.

## 15. Validation
Reject any publish call not accompanied by a valid `localization_reviewer` session/scope.

## 16. Authentication
Bearer JWT, admin session.

## 17. Authorization
Dual-role gate: `content_editor` for draft CRUD, `localization_reviewer` for publish sign-off.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Publish attempted without reviewer scope | 403, explicit message referencing the sign-off requirement |
| Content not found | 404 |
| Re-review flag on non-published content | 400 (only published content can be flagged for re-review) |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
This endpoint *is* the localization review mechanism — reuses existing `localization` context infrastructure per §6.

## 22. RTL
Review UI (N-03) must render Arabic/Urdu copy correctly for reviewer assessment; this is a client concern, not an API concern.

## 23. Analytics
N/A (admin operational workflow, audit-logged).

## 24. Performance
Low-volume admin workflow; no special performance requirements.

## 25. Security
Dual-role gate is the primary control; audit log captures who approved what and when — important given the feature's ethical-tone commitments are held to security-equivalent rigor.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Pydantic v2.

## 27. Testing
Unit + integration tests for the dual-role gate, publish-without-reviewer-role rejection, flag-for-re-review flow.

## 28. Documentation
OpenAPI docs explaining the cultural-appropriateness (not just translation-accuracy) review intent, referencing PRD §8.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement Dedicated `MercyCopyReview` Table**
- Objective: Persist review-workflow state via a dedicated join table referencing `TranslationContent` (decision confirmed per §6 audit — no domain-tagging convention exists anywhere in the codebase to extend instead).
- Files to Create: `models.py` extension (`MercyCopyReview`), `alembic/versions/<rev>_create_mercy_copy_review_table.py`
- Do Not Change: `TranslationContent`'s existing schema and consumers in other contexts must be unaffected.
- Definition of Done: table created, FK to `TranslationContent` verified, no regression to existing localization functionality.

**Task 02 — Implement Review Workflow Service**
- Files to Create: `mercy_copy_review.py`
- Business Rules: dual-role gate, flag-for-re-review.
- Tests: unit tests for state transitions (`pending → published → flagged → pending`).
- Definition of Done: workflow states behave correctly.

**Task 03 — Implement Admin Endpoints**
- Files to Modify: `admin_api.py`, `schemas.py`
- Authentication/Authorization: dual-role gate per §17.
- Error Handling: per §18.
- Tests: integration tests including the reviewer-role-rejection case.
- Definition of Done: endpoints live, documented.

**Task 04 — Wire Audit Logging**
- Definition of Done: every publish/flag action logged with admin identity.

**Task 05 — Final Code Review**
- Do Not Change: existing `localization` context consumers outside Habit Tracker.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Mercy-copy review workflow live, dual-role-gated, audit-logged, without regressing existing localization infrastructure.

## 31. Final Verification Checklist
- [x] Publish requires `localization_reviewer` scope specifically
- [x] `content_editor`-only publish attempts rejected with 403
- [x] Flag-for-re-review works on published content only
- [x] Existing `localization` context consumers unaffected
- [x] Audit log captures reviewer identity and timestamp
- [x] Tests passing, OpenAPI docs complete

## 32. Technical Implementation & Test Verification Records
- **ORM Model**: `MercyCopyReview` in `src/noorheroes/modules/habits/models.py` (`mercy_copy_review` table, unique constraint on `(translation_content_id, locale)`, check constraint on status).
- **Alembic Migration**: `alembic/versions/0060_create_mercy_copy_review_table.py` (Single linear head, foreign key `CASCADE`, locale/status indexing).
- **Repository**: `MercyCopyReviewRepository` in `src/noorheroes/modules/habits/repository.py` (CRUD, status aggregation counts, filtering, pagination).
- **Domain Service**: `MercyCopyReviewService` in `src/noorheroes/modules/habits/mercy_copy_review.py` (review queue lifecycle, dual-role RBAC verification, re-review flagging invariant, translation synchronization, immutable audit logs).
- **Admin API Controller**: `_mercy_copy_router` mounted on canonical `/v1/admin/habits/mercy-copy-review` and gateway alias `/admin/v1/habits/mercy-copy-review` in `src/noorheroes/modules/habits/admin_api.py`.
- **Pydantic v2 Schemas**: `MercyCopyCreateRequest`, `MercyCopyPublishRequest`, `MercyCopyFlagRequest`, `MercyCopyReviewItemResponse`, `MercyCopyReviewListResponse` in `src/noorheroes/modules/habits/admin_schemas.py`.
- **Closed Domain Exceptions**: `MercyCopyReviewNotFoundError`, `MercyCopyTranslationNotFoundError`, `MercyCopyInvalidStateTransitionError`, `MercyCopyMissingReviewerSignoffError`, `MercyCopyReviewAlreadyExistsError` in `src/noorheroes/modules/habits/exceptions.py`.
- **Dependency Providers**: `get_mercy_copy_review_repository`, `get_mercy_copy_review_service` in `src/noorheroes/modules/habits/deps.py`.
- **Module Interface Exports**: Exported in `src/noorheroes/modules/habits/__init__.py`.
- **Automated Test Results**:
  - `tests/modules/habits/test_admin_mercy_copy_review.py`: 11 passed (100% pass rate)
  - Complete Habits Module Suite (`tests/modules/habits/` across 14 test files): 324 passed in 9.84s (100% pass rate)
  - **Statement Coverage**: 2,511 / 2,511 (100.00%, 0 missing statements)
  - **Branch Coverage**: 470 / 470 (100.00%, 0 partial branches)
  - Cross-module regression (`habits` + `dua`): 778 passed in 36.21s (100% pass rate)
  - Architecture Compliance (`tests/architecture/`): 246 passed, 4 skipped in 27.55s (100% compliant)
- **OpenAPI 3.1.0 Contract Export**:
  - `artifacts/openapi.json` generated with endpoints `/v1/admin/habits/mercy-copy-review` (GET, POST, PATCH), `/v1/admin/habits/mercy-copy-review/publish` (POST), `/v1/admin/habits/mercy-copy-review/flag` (POST, PATCH), `/v1/admin/habits/mercy-copy-review/{id}` (GET), and `/admin/v1/habits/mercy-copy-review/*` aliases.
  - `scripts/classify_openapi_diff.py --base openapi.baseline.json --head artifacts/openapi.json --fail-on-breaking`: 0 breaking changes detected.
