# B-05 — Support-Safe Metadata Correction API

## 1. Feature Context
A narrow correction surface for non-PII account metadata (e.g., display name typo, timezone, locale preference) whose request schema structurally excludes every PII field, so no future field addition can accidentally reopen a PII-write path for support staff.

## 2. Parent Feature
E.32 — User Management & Child Safety View

## 3. Sub-feature
1.5 Support-Safe Metadata Correction API (ID: **B-05**)

## 4. Objective
Build `PATCH /v1/admin/users/{parent_id}/metadata` accepting only an explicit allowlist of non-PII fields, rejecting any unrecognized or PII-shaped field at the schema level.

## 5. Business Requirements
- Support staff may correct a narrow set of non-sensitive metadata fields on a parent account.
- The schema is a strict allowlist — new fields on the underlying `parent_account` model do not automatically become editable here.
- No PII field (email, phone, legal name, address) is ever reachable through this endpoint.

## 6. Existing Architecture
`identity` bounded context, `app/identity/routers/user_metadata_router.py`.

## 7. Existing Code to Reuse
- `app/shared/base_service.py::BaseService`
- E.28's `AuditLogService.log_action()`

## 8. Files to Create
- `app/identity/routers/user_metadata_router.py`
- `app/identity/services/user_metadata_correction_service.py`
- `app/identity/schemas/user_metadata_schema.py` — explicit allowlist Pydantic model (`display_name`, `timezone`, `locale_preference` — confirmed against PRD; extend only with explicit non-PII fields)

## 9. Files to Modify
- `app/identity/routers/__init__.py` — register router

## 10. Backend Requirements
- `UserMetadataSchema` uses `model_config = ConfigDict(extra="forbid")` so any field not explicitly declared is rejected at the request-parsing layer, not silently ignored or passed through.
- Service applies only the allowlisted fields to the `parent_account` row — no dynamic/reflective field-setting from the request body.
- Every correction is audit-logged with before/after values for the changed fields (values are non-PII by construction, safe to log in full).

## 11. Required API / API Contract
`PATCH /v1/admin/users/{parent_id}/metadata` `{display_name?, timezone?, locale_preference?}` → `200` with updated summary. `422` for any unrecognized field (Pydantic `extra="forbid"` violation).

## 12. Database Requirements
No new tables — updates existing `parent_account` columns already covered by the allowlist.

## 13. Validation
`extra="forbid"` on the Pydantic schema (mandatory); field-level validation per type (`timezone` against IANA tz database, `locale_preference` against supported-locales list from A.10-equivalent config).

## 14. Authentication
`get_current_admin`.

## 15. Authorization
`require_admin_scope("support")`.

## 16. Error Handling
`422` for schema violations (including any attempted PII field); `404` for unknown `parent_id`.

## 17. Security
The `extra="forbid"` allowlist schema is this endpoint's core guarantee, verified by a mandatory schema-introspection test asserting the model's field set contains zero PII-shaped field names (checked against B-02's `PiiFieldMap` declared-PII field list, to keep the two in sync automatically rather than by convention).

## 18. Analytics
Log correction volume by field type for support-tooling usage metrics.

## 19. Performance
Single-row update, indexed on `parent_account.id`.

## 20. Library Requirements
FastAPI, Pydantic v2 (`extra="forbid"`). No new libraries.

## 21. Testing
Unit: allowlist-only field acceptance, `extra="forbid"` rejection of unknown fields. Integration: **mandatory** — schema-introspection test confirming zero overlap between this schema's field names and B-02's `PiiFieldMap` PII field list; full correction → audit-log-with-before/after-values flow.

## 22. Documentation
OpenAPI docstring explicitly listing the exact editable field set and stating that this list is intentionally minimal and PII-free.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Define the Allowlist Schema with `extra="forbid"`**
Objective: `UserMetadataSchema` with exactly the non-PII allowlisted fields. Files: `schemas/user_metadata_schema.py`. Tests: unknown-field-rejected test. Definition of Done: test passes.

**Task 02 — Implement `UserMetadataCorrectionService`**
Objective: Apply only allowlisted fields, no dynamic field-setting. Files: `services/user_metadata_correction_service.py`. Dependencies: Task 01. Tests: field-application tests. Definition of Done: tests pass.

**Task 03 — Implement the Router Endpoint**
Objective: `PATCH` endpoint wired to service. Files: `routers/user_metadata_router.py`. Dependencies: Task 02. Tests: endpoint integration tests. Definition of Done: tests pass.

**Task 04 — Cross-Check Against B-02's PII Field Map**
Objective: **Mandatory** test confirming zero field-name overlap between this schema and `PiiFieldMap`. Dependencies: B-02, Task 01. Definition of Done: test passes.

**Task 05 — Wire Audit Logging with Before/After Values**
Objective: Log every correction with changed-field values. Dependencies: Task 03. Tests: audit-entry-content test. Definition of Done: test passes.

**Task 06 — Add Full Test Suite**
Objective: Complete coverage per §21. Definition of Done: all green in CI.

**Task 07 — Final Code Review**
Objective: Confirm the allowlist remains minimal and confirm `extra="forbid"` is genuinely enforced (not silently dropped by a permissive parent schema class). Definition of Done: checklist in §24 checked.

## 24. Final Verification Checklist
- [ ] Schema uses `extra="forbid"` — unknown fields rejected at parse time
- [ ] Zero field-name overlap with B-02's `PiiFieldMap` — mandatory cross-check test passing
- [ ] Every correction audit-logged with before/after values
- [ ] `support`+ scope enforced

## 25. Definition of Done
Support staff can correct a minimal, provably PII-free set of account metadata fields, with the safety property enforced structurally by schema, not by convention or code review alone.
