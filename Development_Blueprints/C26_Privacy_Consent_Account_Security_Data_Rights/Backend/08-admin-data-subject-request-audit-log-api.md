# B-08 — Admin Data Subject Request Audit Log API

## 1. Feature Context
Part of Feature C.26's Admin Requirements (§8). A read-only, paginated view over every `data_request` record (export and delete) for Support/Trust & Safety/Compliance, mirroring C.21 B-09's Deletion Case Audit API pattern exactly.

## 2. Parent Feature
C.26 Privacy, Consent, Account Security & Data Rights (Settings)

## 3. Sub-feature
**B-08 — Admin Data Subject Request Audit Log API**

## 4. Objective
Implement `GET /v1/admin/data-requests` as a strictly read-only, paginated, filterable view over B-03's `data_request` table, with masked family identifiers, no override/restore capability anywhere — following the exact same read-only-by-construction pattern C.21 B-09 established for `child_deletion_case`.

## 5. Business Requirements
- §8: "Data Subject Request Audit Log (Read-only): Visibility into every `data_request` for compliance reporting (cross-ref C.21's similarly-patterned Deletion Case Audit Log)."
- CRUD permissions: Read-only behind `support`/`trust_safety`/`compliance`.

## 6. Existing Architecture
Directly mirrors C.21 B-09 ("Admin Deletion Case Audit API") — same masking approach, same pagination pattern, same role set family (`support`/`trust_safety` there, extended here to also include `compliance`). Reads B-03's `data_request` table exclusively; **B-03 must be built first** since this sub-feature has no independent data source.

## 7. Existing Code to Reuse
- `modules/data_rights/repository.py::DataRequestRepository` (B-03) — add `list_paginated(filters)` read method here, not a duplicate repository.
- `modules/admin/api.py` — existing `AdminRouter` RBAC pattern.
- C.21 B-09's masking utility for family/parent identifiers, if implemented as a shared helper — reuse it rather than writing a second masking function.

## 8. Files to Create
- `src/noorheroes/modules/admin/data_request_audit_schemas.py`
- `tests/modules/admin/test_data_request_audit_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/data_rights/repository.py` — add `list_paginated(type, status, page, page_size)`.
- `src/noorheroes/modules/admin/api.py` — add `GET /v1/admin/data-requests`.

## 10. Backend Requirements
- Paginated list of `data_request` rows: masked family identifier, `type` (`export`/`delete`), `status`, `requested_at`, `completed_at`.
- Filter by `type` and `status`; sort by `requested_at`/`completed_at`.
- Strictly read-only — this router file/module must expose no create/update/delete method against `data_request` anywhere.
- `support`/`trust_safety`/`compliance` roles only.

## 11. API Contract

### `GET /v1/admin/data-requests?type=&status=&page=&page_size=`
- **Auth:** `support`/`trust_safety`/`compliance` role
- **Response 200:** `{ "items": [ { "request_id": "...", "family_id_masked": "fam_***a1b2", "type": "export", "status": "ready", "requested_at": "...", "completed_at": "..." } ], "total": 42, "page": 1, "page_size": 20 }`

## 12. Database Requirements
None new — reads B-03's `(family_id, requested_at DESC)` index; add a supplementary index on `(type, status)` only if query-plan analysis shows it's needed.

## 13. Validation
`type` in `('export','delete')` if provided; `status` in `('preparing','ready','failed')` if provided; `page`/`page_size` bounded.

## 14. Authentication
Existing admin session mechanism.

## 15. Authorization
`support`/`trust_safety`/`compliance` role only, read-only.

## 16. Error Handling
| Scenario | Response |
|---|---|
| Unauthorized role | `403` |
| Invalid filter value | `422` |
| Out-of-range page | `200` with empty `items`, not an error |

## 17. Offline First
N/A.

## 18. Local Data
N/A.

## 19. Localization
N/A — admin UI (N-04) localizes labels; this API returns raw codes/timestamps.

## 20. RTL
N/A backend.

## 21. Analytics
Not specified; this endpoint is itself a compliance-reporting surface.

## 22. Performance
Server-side pagination, indexed query, never a full-table client-side dump.

## 23. Security
- Masked family identifiers only, consistent with C.21 B-09's established masking pattern.
- No mutation surface exists anywhere in this sub-feature — verified by a negative test, mirroring C.21 N-01's "no restore/delete/edit affordance" backend-side equivalent.

## 24. Library Requirements
No new libraries.

## 25. Testing
- Unit: non-authorized roles rejected.
- Integration: pagination, filtering by `type`/`status`, sorting.
- Negative: no create/update/delete route exists anywhere in this sub-feature's router additions (code-inspection-backed test, mirroring the `never`-generic pattern used on the NextJS side).
- Integration: family identifiers are masked in every response, never raw.

## 26. Documentation
OpenAPI states explicitly this is intentionally read-only, cross-referencing C.21 B-09's identical pattern and B-03 as its sole data source.

## 27. AI Coding Agent Implementation Steps

**Task 01 — Confirm B-03 Exists**
- **Objective:** This sub-feature has no independent data source; confirm B-03's `data_request` table is live before starting.

**Task 02 — Add `list_paginated()` to `DataRequestRepository`**
- **Files to Modify:** `modules/data_rights/repository.py`.

**Task 03 — Implement Masking Utility (Reuse or Create)**
- **Objective:** Reuse C.21 B-09's masking helper if it exists as a shared utility; otherwise implement a small, shared one here rather than a feature-local duplicate.

**Task 04 — Implement Endpoint with RBAC**
- **Files to Modify:** `admin/api.py`.
- **Tests:** RBAC, masking, pagination, filtering.

**Task 05 — Full Test Suite & Documentation**

## 28. Definition of Done
A strictly read-only, paginated, masked, role-restricted audit view over `data_request` is live, structurally incapable of mutation, mirroring C.21 B-09's established pattern.

## 29. Final Verification Checklist
- [ ] B-03 confirmed live before implementation
- [ ] Strictly read-only — no mutation route exists anywhere in this sub-feature
- [ ] Family identifiers masked in every response
- [ ] `support`/`trust_safety`/`compliance` roles enforced
- [ ] Pagination and filtering verified
- [ ] Masking utility reused from C.21 B-09 if available, not duplicated
- [ ] No PostgreSQL/Redis credential changes
