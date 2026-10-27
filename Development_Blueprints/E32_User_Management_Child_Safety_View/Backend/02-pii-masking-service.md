# B-02 — PII Masking Service

## 1. Feature Context
The platform's single, mandatory pass-through for every PII-bearing field rendered anywhere in the User Management surface — masked by default, per-request grant-checked, never session-cached, and structurally excluded rather than conventionally hidden.

## 2. Parent Feature
E.32 — User Management & Child Safety View

## 3. Sub-feature
1.2 PII Masking Service (ID: **B-02**)

## 4. Objective
Build a shared `PiiMaskingService` invoked by every read path that touches parent/child PII (B-01 search, Parent Account Detail, Child-Safety View), checking for an active `unmask_grant` on a strictly per-request basis and substituting structural placeholders when none exists.

## 5. Business Requirements
- PII masked by default on every user-facing read.
- Unmask state is never cached at the session level — every single request re-checks grant validity against `unmask_grant.expires_at`.
- Masking is structural (the schema/serializer physically excludes or replaces the field), not a convention the client is trusted to honor.
- The instant a grant expires, the very next request reverts to masked output automatically — no explicit "re-mask" action needed.
- A grant scoped to one child/parent must never unmask an unrelated record, even for the same admin.

## 6. Existing Architecture
`identity` bounded context (masking is a cross-cutting concern consumed by `identity`, `content` (child-safety flags), and `admin` contexts), `app/identity/services/pii_masking_service.py`.

## 7. Existing Code to Reuse
- `app/shared/base_service.py::BaseService`
- E.28's `AuditLogService.log_action()` — every masked-data access logged, not just unmask events (per PRD)

## 8. Files to Create
- `app/identity/services/pii_masking_service.py` — `PiiMaskingService.mask_or_reveal(record, field_map, requesting_admin, scope)`
- `app/identity/repositories/unmask_grant_repository.py` — read-only grant lookup used by this service (write path owned by B-03)
- `app/identity/schemas/pii_field_map.py` — declares which fields on each model are PII and their masked-placeholder format

## 9. Files to Modify
- `app/identity/services/user_search_service.py` (B-01) — route results through this service
- Parent/Child account detail read services — route through this service

## 10. Backend Requirements
- `mask_or_reveal()`: for each request, queries `unmask_grant` for an active (non-expired, scope-matching) grant belonging to the requesting admin and the exact target record; if found, returns real values; otherwise returns masked placeholders (`"J***"`, `"j***@***.com"`, `"***-***-1234"` style, per field type).
- No in-process or Redis cache of "this admin currently has an active grant" — the check is a fresh DB read every call, since grants are time-boxed and must revert precisely at expiry, not at the next cache-refresh interval.
- Field-level exclusion: `PiiFieldMap` declares PII fields structurally (e.g., `raw_email`, `raw_phone`, `full_legal_name`) — serializers reference this map so a new field added to a model does not accidentally bypass masking by omission; default is masked unless explicitly declared safe.
- Every access (masked or unmasked) logs via `AuditLogService.log_action()`, distinguishing `pii_view_masked` vs `pii_view_unmasked` action types.
- Grant scope enforcement: a grant's `scope` (e.g., specific `parent_id` or `child_id`) is compared exactly against the record being rendered — no broader "this admin has some active grant" check.

## 11. Required API / API Contract
Internal service, no dedicated HTTP endpoint — consumed by B-01, and by Parent Account Detail / Child-Safety View read services (owned by this feature's other backend sub-features' underlying read paths, largely reused from C.19/C.21).

## 12. Database Requirements
Reads `unmask_grant` (owned by B-03: `id`, `admin_id`, `scope_type`, `scope_id`, `expires_at`, `created_from_request_id`). No new tables owned by B-02 itself.

## 13. Validation
Internal method signatures only; no external request validation (not a router-facing endpoint).

## 14. Authentication
N/A directly — operates on an already-authenticated `requesting_admin` object passed by the caller.

## 15. Authorization
Grant-scope check is itself the authorization gate for unmasking; masked output requires no special authorization (any `support`+ role can see masked summaries).

## 16. Error Handling
Never raises on missing grant — returns masked output as the correct default behavior, not an error condition.

## 17. Security
This is the platform's highest-priority guarantee for this feature. Mandatory isolation tests: (a) an expired grant reverts to masked on the very next call; (b) a grant scoped to child A never unmasks child B's record; (c) no caching layer retains a stale "unmasked" decision past a grant's `expires_at`; (d) a newly-added PII field on a model defaults to masked unless explicitly whitelisted in `PiiFieldMap` (schema-level test, not convention-trust).

## 18. Analytics
Log masked-vs-unmasked view counts per admin (supports the Unmask Workflow's oversight/audit reporting, not exposed as end-user analytics).

## 19. Performance
Grant lookup indexed on `(admin_id, scope_type, scope_id, expires_at)`; single indexed query per request, no N+1 across a result list (batch-check grants for a list of records in one query where B-01 returns multiple rows).

## 20. Library Requirements
FastAPI, Pydantic v2, SQLAlchemy 2.0 async. No new libraries.

## 21. Testing
Unit: masked-placeholder formatting per field type, field-map default-masked-unless-whitelisted logic. Integration: **mandatory** — expired-grant-reverts-on-next-call test; **mandatory** — cross-scope grant does not leak to unrelated record test; batch-check performance test for multi-row results; audit log entry created for both masked and unmasked views.

## 22. Documentation
Docstring on `PiiFieldMap` explaining the default-masked-unless-whitelisted convention, since this is the single most important safety property in the module for future engineers to preserve.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Define `PiiFieldMap`**
Objective: Declarative, default-masked-unless-whitelisted field map per model. Files: `schemas/pii_field_map.py`. Tests: default-masked test for an undeclared field. Definition of Done: test passes.

**Task 02 — Implement `UnmaskGrantRepository` (Read-Only)**
Objective: Indexed grant lookup by `(admin_id, scope_type, scope_id)`, filtered to non-expired. Files: `repositories/unmask_grant_repository.py`. Dependencies: B-03's `unmask_grant` table. Tests: expiry-filter test. Definition of Done: test passes.

**Task 03 — Implement `PiiMaskingService.mask_or_reveal()`**
Objective: Per-request grant check, masked-placeholder substitution, no caching. Files: `services/pii_masking_service.py`. Dependencies: Task 01, Task 02. Tests: **mandatory** — expired-grant-reverts test, cross-scope-isolation test. Definition of Done: both mandatory tests pass.

**Task 04 — Wire Audit Logging for Every Access**
Objective: `pii_view_masked`/`pii_view_unmasked` log entries. Dependencies: Task 03. Tests: log-entry-created test for both paths. Definition of Done: test passes.

**Task 05 — Integrate into B-01 and Account Detail Read Paths**
Objective: Route all PII-bearing reads through this service. Dependencies: Task 03, B-01. Tests: integration test confirming B-01 results are masked without an active grant. Definition of Done: test passes.

**Task 06 — Add Batch-Check Support for List Results**
Objective: Single indexed query for grant-checking multiple records at once. Dependencies: Task 02. Tests: N+1-avoidance test (query count assertion). Definition of Done: test passes.

**Task 07 — Add Full Test Suite**
Objective: Complete coverage per §21, both mandatory tests included. Definition of Done: all green in CI.

**Task 08 — Final Code Review**
Objective: Confirm zero caching layer exists anywhere in this service's call path; confirm every PII field on every consuming model routes through `PiiFieldMap`. Definition of Done: checklist in §24 checked.

## 24. Final Verification Checklist
- [ ] Grant check is a fresh per-request DB read, never cached — mandatory test passing
- [ ] Expired grant reverts to masked on the very next call — mandatory test passing
- [ ] Grant scope isolation confirmed (child A grant never unmasks child B) — mandatory test passing
- [ ] New/undeclared PII fields default to masked, not safe
- [ ] Every access (masked or unmasked) is audit-logged

## 25. Definition of Done
Every PII-bearing read in the User Management surface is provably masked-by-default, per-request grant-checked, and audit-logged, with zero caching path that could serve stale unmasked data past a grant's expiry.
