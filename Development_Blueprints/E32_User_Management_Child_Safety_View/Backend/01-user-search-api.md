# B-01 — User Search API

## 1. Feature Context
The single entry point for support/moderation staff to locate a user record by any of four identifier types, returning masked-by-default summaries — never raw PII in a search result list.

## 2. Parent Feature
E.32 — User Management & Child Safety View

## 3. Sub-feature
1.1 User Search API (ID: **B-01**)

## 4. Objective
Build `GET /v1/admin/users/search` accepting parent ID, family ID, subscription ID, or support case ID, returning a masked result summary list, role-scoped to `support`+ roles.

## 5. Business Requirements
- Search by parent ID, family ID, subscription ID, or support case ID.
- Results return masked summary fields only (name-initial, masked email/phone) — full PII masking is B-02's responsibility, applied to every field this endpoint returns.
- No match returns an empty result set, not a 404 (a search is not a lookup-by-known-ID).
- Accessible to any authenticated operator with `support` role or above.

## 6. Existing Architecture
`identity` bounded context, `app/identity/routers/admin_user_router.py`, following `FAST-API-INSTRUCTIONS.md`'s Router→Service→Repository layering. Reuses E.28's `require_admin_scope()` and `get_current_admin`.

## 7. Existing Code to Reuse
- `app/shared/base_service.py::BaseService`
- `app/shared/base_repository.py::BaseRepository`
- `app/identity/dependencies.py::get_current_admin`, `require_admin_scope()`
- `app/admin/services/audit_log_service.py::AuditLogService.log_action()` (E.28 — every search is logged)

## 8. Files to Create
- `app/identity/routers/admin_user_router.py` (new endpoint added to existing router if present; otherwise created)
- `app/identity/services/user_search_service.py`
- `app/identity/repositories/user_search_repository.py`
- `app/identity/schemas/user_search_schema.py` — `UserSearchQuery`, `UserSearchResultItem` (masked shape only)

## 9. Files to Modify
- `app/identity/routers/__init__.py` — register route if new router file

## 10. Backend Requirements
- `UserSearchService.search()`: dispatches to the correct repository lookup based on which identifier field is populated (exactly one of `parent_id`/`family_id`/`subscription_id`/`support_case_id` required — reject multiple or zero).
- `UserSearchRepository`: four narrow lookup methods, each returning the minimal joined row set needed for a masked summary — never a `SELECT *` that could leak PII fields into a serialization bug.
- Every result field is passed through B-02's masking service before serialization — this endpoint never independently decides what is safe to show.
- Logs every search via `AuditLogService.log_action()` with the query type and requesting admin, not the query value itself (avoid logging PII-adjacent search terms in plaintext where the identifier itself could be sensitive).

## 11. Required API / API Contract
`GET /v1/admin/users/search?parent_id=&family_id=&subscription_id=&support_case_id=`
Response: `200 { "results": [ { "parent_id", "masked_name", "masked_email", "masked_phone", "family_id", "account_status" } ] }` (empty array for no match), `400` for zero-or-multiple identifiers provided, `401`/`403` for auth/scope failure.

## 12. Database Requirements
No new tables. Read-only queries against existing `parent_account`, `family`, `subscription` (E.33-owned, read via FK), `support_case` (B-08) tables. Indexes confirmed to exist on `parent_account.id`, `family.id` for lookup performance; add index on `support_case.id` if missing.

## 13. Validation
Pydantic schema enforces exactly-one-identifier-populated via a model validator; reject empty/whitespace identifier strings.

## 14. Authentication
`get_current_admin` dependency; standard admin JWT/session validation per E.28.

## 15. Authorization
`require_admin_scope("support")` — minimum role for any search; broader roles (moderator/admin/scholar) inherit access per E.28's role hierarchy.

## 16. Error Handling
`400` for malformed/ambiguous query; `403` for insufficient scope; results are never a `404` for no-match (empty list is the correct "not found" representation for a search).

## 17. Security
Every returned field routes through B-02's masking service — this endpoint has no independent PII-rendering path. Search audit-logged without the raw identifier value in cases where the identifier itself is PII-adjacent (e.g., avoid logging a raw phone number used as a search term).

## 18. Analytics
Log search volume by identifier type (for support-tooling usage metrics), not raw query content.

## 19. Performance
Indexed lookups only; no full-table scans. Result set capped (a given identifier resolves to at most one family/parent, so pagination is not required).

## 20. Library Requirements
FastAPI, Pydantic v2, SQLAlchemy 2.0 async, per `FAST-API-INSTRUCTIONS.md` conventions. No new libraries.

## 21. Testing
Unit: exactly-one-identifier validation, dispatch-to-correct-lookup logic. Integration: search-by-each-of-four-identifier-types, no-match returns empty list not 404, masking applied to every returned field (mandatory — mock B-02 and assert it was called for each result), audit log entry created per search, scope enforcement (`support` role passes, unauthenticated fails).

## 22. Documentation
OpenAPI docstrings; note in the endpoint description that all returned fields are masked by default and require an unmask grant (B-03) to view in full.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Define Schemas**
Objective: `UserSearchQuery` with exactly-one-identifier validator, `UserSearchResultItem`. Files: `schemas/user_search_schema.py`. Tests: validator unit tests. Definition of Done: schema rejects zero/multiple identifiers.

**Task 02 — Implement `UserSearchRepository`**
Objective: Four narrow lookup methods against existing tables. Files: `repositories/user_search_repository.py`. Dependencies: Task 01. Tests: each lookup type returns correct minimal row set. Definition of Done: tests pass.

**Task 03 — Implement `UserSearchService`**
Objective: Dispatch logic + mandatory routing of every result through B-02's masking service. Files: `services/user_search_service.py`. Dependencies: Task 02, B-02. Tests: **mandatory** — masking service invoked for every returned field. Definition of Done: test passes.

**Task 04 — Implement the Router Endpoint**
Objective: `GET /v1/admin/users/search` wired to service, scope-gated. Files: `routers/admin_user_router.py`. Dependencies: Task 03. Tests: endpoint integration tests. Definition of Done: tests pass.

**Task 05 — Wire Audit Logging**
Objective: Log every search via `AuditLogService.log_action()`, excluding raw PII-adjacent query values. Dependencies: Task 04. Tests: audit-entry-created test. Definition of Done: test passes.

**Task 06 — Add Full Test Suite**
Objective: Complete coverage per §21. Definition of Done: all green in CI.

**Task 07 — Final Code Review**
Objective: Confirm zero unmasked field can reach the response without passing through B-02. Definition of Done: checklist in §24 checked.

## 24. Final Verification Checklist
- [ ] Exactly-one-identifier validation enforced
- [ ] No-match returns empty list, not 404
- [ ] Every result field passes through B-02's masking service — mandatory test passing
- [ ] Search audit-logged without raw PII-adjacent query values
- [ ] `support`+ scope enforced

## 25. Definition of Done
Operators can locate a user by any of four identifiers and receive a masked, audit-logged result set with zero independent PII-rendering path outside B-02.
