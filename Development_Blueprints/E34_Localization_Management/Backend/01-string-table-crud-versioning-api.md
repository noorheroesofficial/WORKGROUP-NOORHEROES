# B-01 — String Table CRUD & Versioning API

## 1. Feature Context
The authoring surface for every translated string in the platform: creating keys, editing translations, and validating ICU plural/gender/date syntax before it can ever be saved — with every update producing a new version rather than mutating an already-published row.

## 2. Parent Feature
E.34 — Localization Management

## 3. Sub-feature
1.1 String Table CRUD & Versioning API (ID: **B-01**)

## 4. Objective
Build create/list/update/deprecate endpoints for `locale_string`/`locale_string_version`, validating ICU message-format syntax at submission and always creating a new version on update.

## 5. Business Requirements
- FR-2: create locale key; read coverage; update translation (versioned); deprecate unused key.
- FR-8: ICU plural/gender/date formatting rules supported per locale, not a single-string-per-key model.
- FR-11: updating a translation creates a new version — never an in-place edit of an already-published, currently-served string.
- §5 Backend AI prompt item 4/5: ICU syntax validated at submission, rejecting malformed rules before save; update always creates a new version row with status reset to `draft`, prior published version remains servable until the new one publishes.
- Edge Case 6: concurrent edits to the same key/locale use last-write-wins, both attempts preserved in version history.

## 6. Existing Architecture
New `localization` bounded context (or extends `content` per `FAST-API-INSTRUCTIONS.md`'s 10-context map — confirm placement; default to a new `localization` context given its distinct string-table domain), `app/localization/routers/admin_string_router.py`.

## 7. Existing Code to Reuse
- `app/shared/base_service.py::BaseService`, `app/shared/base_repository.py::BaseRepository`
- E.28's `AuditLogService.log_action()`, `require_admin_scope()`
- E.29's append-only versioning pattern (`content_version`) as the structural template for `locale_string_version`

## 8. Files to Create
- `app/localization/routers/admin_string_router.py`
- `app/localization/services/string_table_service.py`
- `app/localization/repositories/locale_string_repository.py`
- `app/localization/schemas/locale_string_schema.py`
- `app/localization/validators/icu_syntax_validator.py` — ICU message-format parser/validator
- `alembic/versions/xxxx_create_locale_string_tables.py`

## 9. Files to Modify
- `app/localization/routers/__init__.py` — register router

## 10. Backend Requirements
- `StringTableService.create_key()`: creates a `locale_string` row plus an initial `locale_string_version` at `status='draft'`.
- `StringTableService.update_translation()`: NEVER updates an existing `locale_string_version` row in place — always inserts a new version row at `status='draft'`, leaving the prior `status='published'` version fully intact and servable (B-02 continues serving it until the new version completes review).
- `IcuSyntaxValidator.validate()`: parses the submitted `value_icu` string against ICU MessageFormat grammar, raising a structured validation error identifying the specific malformed segment — called synchronously at submission time, before any DB write.
- `StringTableService.deprecate()`: sets `locale_string.deprecated=true`, never deletes the row (preserves historical reference for any content version still keyed to it, per §4.4).

## 11. Required API / API Contract
`POST /v1/admin/locales/strings` `{key, locale_code, value_icu}` → `201`.
`GET /v1/admin/locales/strings?locale=&status=` → list.
`PATCH /v1/admin/locales/strings/{id}` `{value_icu}` → `200` (creates new version).
`DELETE /v1/admin/locales/strings/{id}` (deprecate, soft) → `200`.

## 12. Database Requirements
`locale_string(string_id PK, key, locale_code FK, current_published_version_id, deprecated)`, `UNIQUE(key, locale_code)`.
`locale_string_version(version_id PK, string_id FK, value_icu, status, review_stage, created_at)`, `CHECK status IN ('draft','machine_assisted','editorial_review','scholar_review','published')`. Index `(string_id, created_at DESC)`.

## 13. Validation
ICU syntax validated synchronously at submission (mandatory, before any write); `key`/`locale_code` required; `locale_code` must reference an existing `locale` row.

## 14. Authentication
`get_current_admin`.

## 15. Authorization
`require_admin_scope("localization_manager")`.

## 16. Error Handling
`422 INVALID_ICU_SYNTAX` with the specific malformed segment identified; `404` for unknown string/key; `409` for duplicate `(key, locale_code)` on create.

## 17. Security
ICU validation happening before any persistence is this sub-feature's key correctness guarantee — mandatory test confirms a malformed plural rule is rejected at submission and never reaches any version-status row, draft or otherwise. Versioning-not-mutation is the second guarantee — mandatory test confirms an update to a published string produces a new `draft`-status row while the prior published row remains byte-for-byte unchanged and still queryable.

## 18. Analytics
`string_key_created`, `translation_updated` (with `locale`, `review_stage`), `string_key_deprecated` per §1.19.

## 19. Performance
Indexed on `(string_id, created_at DESC)`, `(locale_code)`.

## 20. Library Requirements
FastAPI, Pydantic v2, SQLAlchemy 2.0 async, Alembic, an ICU MessageFormat parsing library (e.g., `pyicu`/`babel`'s message-format support, confirmed against the platform's existing dependency set — reuse whatever the consumer-facing localization stack (A.10-equivalent) already uses rather than introducing a second ICU library).

## 21. Testing
Unit: ICU syntax validator (valid and malformed fixtures). Integration: **mandatory** — malformed ICU syntax rejected at submission, never persisted in any form; **mandatory** — update to a published string creates a new `draft` version while the prior published version remains unchanged and servable; concurrent-edit-both-preserved-in-history test.

## 22. Documentation
OpenAPI docstrings; ICU syntax examples in the endpoint description.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Write Migration for `locale_string`/`locale_string_version`**
Objective: Tables with status `CHECK`, unique constraint, indexes. Files: `alembic/versions/xxxx_create_locale_string_tables.py`. Tests: migration up/down test. Definition of Done: schema created.

**Task 02 — Implement `IcuSyntaxValidator`**
Objective: ICU MessageFormat parsing with structured error identification. Files: `validators/icu_syntax_validator.py`. Tests: **mandatory** — valid/malformed fixture tests. Definition of Done: tests pass.

**Task 03 — Define Schemas**
Objective: `LocaleStringCreate`, `TranslationUpdate`, `LocaleStringDetail`. Files: `schemas/locale_string_schema.py`. Dependencies: Task 01, Task 02. Tests: validation tests. Definition of Done: tests pass.

**Task 04 — Implement `LocaleStringRepository`**
Objective: CRUD + version-insert-only update pattern. Files: `repositories/locale_string_repository.py`. Dependencies: Task 01. Tests: repository tests. Definition of Done: tests pass.

**Task 05 — Implement `StringTableService`**
Objective: Create/update(always-new-version)/deprecate logic, ICU validation wired before persistence. Files: `services/string_table_service.py`. Dependencies: Task 02, Task 04. Tests: **mandatory** — versioning-not-mutation test. Definition of Done: test passes.

**Task 06 — Implement Router Endpoints**
Objective: Wire all four endpoints, `localization_manager`-scope-gated. Files: `routers/admin_string_router.py`. Dependencies: Task 05. Tests: endpoint integration tests. Definition of Done: tests pass.

**Task 07 — Wire Audit Logging**
Objective: Log create/update/deprecate. Dependencies: Task 06. Tests: audit-entry test. Definition of Done: test passes.

**Task 08 — Add Full Test Suite**
Objective: Complete coverage per §21, both mandatory tests included. Definition of Done: all green in CI.

**Task 09 — Final Code Review**
Objective: Confirm zero code path mutates an existing version row in place, and zero path persists unvalidated ICU syntax. Definition of Done: checklist in §24 checked.

## 24. Final Verification Checklist
- [ ] ICU syntax validated and rejected-if-malformed at submission, before any persistence — mandatory test passing
- [ ] Every update creates a new version row; prior published version remains unchanged and servable — mandatory test passing
- [ ] Deprecation is a soft flag, never a delete
- [ ] Concurrent edits preserve both attempts in version history
- [ ] `localization_manager` scope enforced

## 25. Definition of Done
Strings are authored with genuine ICU-format rigor and a provably append-only versioning discipline — the foundation B-02's Delivery API and B-05's review workflow both depend on.
