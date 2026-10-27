# B-09 — Admin Deletion Case Audit API

> ✅ **UPDATE (resolved via cross-document search of `Feature_E28_Admin_Auth_RBAC_Operations_Dashboard.md` and `Feature_C24_Subscription_Billing.md`):** `support` and `trust_safety` are confirmed as **real, precedented role names** — C.24 §8 itself gates an endpoint "behind `product_admin`/`trust_safety`", and E.28 FR-4 lists "Support Agent" as one of nine defined portal roles. Critically, **no `resource:action` scope-string convention (e.g. `support:read`) is documented anywhere in the project** — every precedent found uses **bare role-name gating** applied directly to endpoints (e.g. `"Auth: super_admin"`). This blueprint is updated to use bare role names via the existing `require_admin_scope(required_scope: str)` factory (passing the role name itself, not a fabricated `resource:action` string). Path: `/v1/admin/...` is confirmed as the codebase's actual convention (`FAST-API-INSTRUCTIONS.md`'s documented `AdminRouter`), taking priority over an inconsistent `/api/v1/admin/...` variant that appears elsewhere in PRD prose only. **Still open:** no existing PII-masking utility was found in the searched docs — confirm against the actual codebase (not just PRD prose) before Task 02.

## 1. Feature Context
Part of Feature C.21 — Multi-Child Management's Admin Requirements (§8): a read-only Support/Trust & Safety surface over the deletion audit trail created by B-06.

## 2. Parent Feature
C.21 Multi-Child Management

## 3. Sub-feature
**B-09 — Admin Deletion Case Audit API** (`GET /v1/admin/child-deletion-cases`)

## 4. Objective
Give Support/Trust & Safety staff full, read-only visibility into every `child_deletion_case` record for investigation and compliance purposes, with zero ability to restore or override a deletion.

## 5. Business Requirements
- §8: "Deletion Case Audit Viewer (Read-only): Search by masked identifier, view the full `child_deletion_case` lifecycle. No override/restore capability."
- CRUD permissions: Read-only behind `support`/`trust_safety`.

## 6. Existing Architecture
Follows the existing `admin` bounded context pattern (`AdminRouter`, `AdminAuditRepository`, `require_admin_scope`) per `FAST-API-INSTRUCTIONS.md` §5.2/§6.2.

## 7. Existing Code to Reuse
- `get_current_admin` / `AdminSessionContext` (`core/deps.py`).
- `require_admin_scope(required_scope: str)` — reuse the factory pattern, but pass the confirmed bare role names `"support"` / `"trust_safety"` as the argument (`Depends(require_admin_scope("support"))`), not an invented `support:read`-style string.
- `BaseRepository.list_paginated()` (`common/base_repository.py`) — reuse cursor-based pagination rather than building a new pagination mechanism.

## 8. Files to Create
- `modules/identity/admin_deletion_audit_repository.py` — placed under `identity` since `child_deletion_case` is an `identity`-context table (per the existing convention that repositories live alongside the models they query, as seen with `ChildRepository`); `modules/admin/` remains reserved for the general `AdminAuditLog` cross-cutting concern, not domain-specific audit views.

## 9. Files to Modify
- `modules/identity/api.py` — add the audit-viewer route (module placement now resolved: `identity`, not `admin`, matching the table's own bounded context).
- `modules/identity/schemas.py` — add `ChildDeletionCaseResponse`.
- `tests/modules/identity/test_child_deletion_case_audit.py` — new test module.

## 10. Backend Requirements
- List `child_deletion_case` rows with pagination (reuse `PageResult`/`list_paginated`).
- Support search by masked identifier — "masked" implies the response and search input never expose the raw `child_id`/PII directly; confirm the exact masking scheme against the platform's existing PII-masking utility (search codebase for an existing masking helper before writing a new one).
- Strictly read-only: no PATCH/DELETE/PUT route exists on this resource under any RBAC scope.

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
N-01 (Deletion Case Audit Viewer) is the sole consumer of this API.

## 13. API Contract

**`GET /v1/admin/child-deletion-cases`**
- **Auth:** Bearer (admin) + `support` or `trust_safety` role (via `require_admin_scope("support")` / `require_admin_scope("trust_safety")` — either role grants access, checked as an OR).
- **Request (query params):** `cursor?`, `limit?`, `search?` (masked-identifier search).
- **Response 200:**
```json
{
  "items": [{
    "caseId": "uuid",
    "childIdentifierMasked": "string",
    "initiatedByParentIdMasked": "string",
    "requestedAt": "timestamp",
    "retentionExpiresAt": "timestamp",
    "purgedAt": "timestamp|null",
    "status": "pending|purged"
  }],
  "nextCursor": "string|null",
  "hasMore": "bool"
}
```
- **Error Responses:** `401`, `403` (missing scope).

## 14. Database Requirements
Reads only from `child_deletion_case` (created by B-06); no schema changes.

## 15. Validation
Query-param validation for `limit` bounds (e.g., max page size 100, consistent with existing admin list endpoints).

## 16. Authentication
Bearer admin session via `get_current_admin`.

## 17. Authorization
`support` or `trust_safety` role, confirmed as real precedented role names (C.24 §8, E.28 FR-4) — no `resource:action` scope convention exists in this codebase to layer on top, so bare role gating is the correct, non-invented approach.

## 18. Error Handling
| Scenario | Response |
|---|---|
| Missing/invalid admin token | `401` |
| Valid admin, missing required scope | `403` |
| No matching records | `200` with empty `items` |

## 19. Offline First
Not applicable — Admin Portal is not offline-first.

## 20. Local Data
Not applicable.

## 21. Localization
Admin Portal strings/dates formatted via `useFormatters()`/`useTranslation()` client-side (N-01); this API returns raw ISO timestamps, not pre-localized strings.

## 22. RTL
Not applicable backend.

## 23. Analytics
Not specified in PRD for this admin surface.

## 24. Performance
Cursor-based pagination on an indexed `(child_id)` column (per §4.2); add a supporting index for the search-by-masked-identifier path if the masking scheme requires a computed/indexed column.

## 25. Security
- Strictly read-only — the absence of any mutating route is itself the primary security control (§12.5: "The DOB Change Support Tool is the only legitimate immutability bypass" — this endpoint has no bypass at all).
- Masked-identifier search prevents casual PII exposure to support staff who don't need the raw identifier for routine searching.

## 26. Library Requirements
No new libraries.

## 27. Testing
- Unit: masking scheme correctly obscures raw identifiers in the response.
- Integration: pagination correctness.
- Integration: search-by-masked-identifier returns expected matches.
- Integration: `403` for an admin session lacking the required scope.
- Integration: confirm no route exists that can mutate `child_deletion_case` (a negative test asserting `405`/`404` on PATCH/DELETE to this path).

## 28. Documentation
Document explicitly in OpenAPI that this endpoint has no write counterpart by design.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm Masking Scheme Against the Actual Codebase (BLOCKING, narrowed scope)**
- **Objective:** Path, module placement, and RBAC role names are now resolved (see the update note at the top of this file) — the one remaining open item is whether an existing PII-masking utility already exists in the actual FastAPI codebase (not just PRD prose, which did not surface one).
- **Action:** Search the live codebase for an existing masking helper before writing a new one; if none exists, propose a minimal one here (e.g., `mask_uuid(value: str) -> str` showing only the last 4 characters) and note it as newly introduced, not silently assumed to already exist.
- **Definition of Done:** Masking scheme documented and either confirmed-existing or explicitly-new before Task 02.

**Task 02 — Repository & Response Schema**
- **Objective:** Implement the read-only repository query and response DTO.
- **Files to Modify:** per Task 01's placement decision.
- **Implementation Details:** Reuse `BaseRepository.list_paginated()`; apply the confirmed masking function at the schema-serialization boundary, never storing masked values in the DB itself.
- **Tests:** Unit tests for masking and pagination.
- **Definition of Done:** Response never leaks raw `child_id`/`parent_id` outside of what masking permits.

**Task 03 — Router with RBAC Scope**
- **Objective:** Wire the route behind the confirmed scope(s).
- **Files to Modify:** admin API router file.
- **Tests:** Scope-enforcement integration tests (positive and negative).
- **Definition of Done:** No route reachable without the correct scope; no mutating verb exists on this path.

## 30. Definition of Done
Read-only audit viewer, correctly scoped, correctly paginated, with confirmed masking and zero mutating capability.

## 31. Final Verification Checklist
- [ ] Masking scheme confirmed against the live codebase (reused if existing, clearly flagged if newly introduced)
- [ ] `support`/`trust_safety` role gating tested (positive and negative) via `require_admin_scope`
- [ ] No mutating route exists on this resource
- [ ] Pagination correctness tested
- [ ] Endpoint lives at `/v1/admin/child-deletion-cases` under the `identity` module (placement rationale documented)
