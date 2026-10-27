# Blueprint: Admin AI Report Content-Safety Audit Log API

## 1. Feature Context
Platform: NoorHeroes Backend (FastAPI). Module: `src/noorheroes/modules/dashboard/` (admin-facing read endpoint) or `modules/admin/` if the team's convention is to centralize all admin-only read surfaces there (see Task 01). Serves the one admin-relevant surface this feature introduces: read-only visibility into reports that failed the Content Safety Validator.

## 2. Parent Feature
C.20 — Parent Dashboard.

## 3. Sub-feature
B-06 — Admin AI Report Content-Safety Audit Log API.

## 4. Objective
Provide a read-only, paginated, RBAC-restricted (`trust_safety`/`ai_ops`) endpoint listing `weekly_report`/`ai_insight_report` rows where `content_safety_passed = false`, with masked child identifier, report type, `generated_at`, and a validator-failure-reason tag — with zero edit/override capability.

## 5. Business Requirements
Source: PRD §8, §9, §12.5.
- "This page is for MODEL-QUALITY MONITORING ONLY — it has no edit, approve-anyway, or override capability anywhere; a report that failed validation simply stays blocked, permanently."
- Restricted to `trust_safety`/`ai_ops` roles.
- Masked child identifier (never expose raw child PII to this audit surface beyond what's necessary for pattern investigation).

## 6. Existing Architecture — VERIFIED AGAINST ACTUAL CODEBASE
Confirmed real `core/deps.py::require_admin_scope(required_scope: str)`: a single-scope AND check (`if required_scope not in admin_ctx.scopes and "super_admin" not in admin_ctx.scopes: raise AuthorizationError(...)`) — it does **not** support OR-logic across multiple scopes. There is no separate `trust_safety`/`ai_ops` ROLE concept in the real scope system; scopes are flat, kebab-case, `resource:action` strings (confirmed real examples from `modules/admin/api.py`: `"consent-types:manage"`, `"ai-retention-config:manage"`, `"data-export-monitor:read"`, `"data-requests:read"`) checked individually per route. `require_admin_scope`'s own docstring explicitly states the exact scope catalogue is owned by E.28 (Admin Auth/RBAC, not yet built) and that scope names used ahead of E.28 are placeholders to be reconciled later — this blueprint's scope name must follow the SAME placeholder convention, not invent a `trust_safety`/`ai_ops` role pairing that doesn't match how every other admin route in this codebase is actually scoped.

**Confirmed real `modules/admin/` module (populated, not a stub):** `AdminRouter = APIRouter(prefix="/v1/admin", tags=["admin"])` in `modules/admin/api.py` already hosts C.26's B-05–B-08 admin endpoints (consent-type registry, AI-retention config, data-export metrics, data-request audit) as `@router.get`/`@router.post` handlers directly on ONE shared router file — **this blueprint should add its endpoint to this SAME existing `modules/admin/api.py` router**, following the identical single-scope-string pattern, rather than creating a new, separate admin sub-router in `modules/dashboard/`.

**Confirmed real masking utility:** `modules/admin/masking.py::mask_family_id(family_id: str) -> str` (`"fam_***" + last 4 chars`), explicitly documented as "C.21 B-09's established pattern, reused here per B-08 §7 — not reimplemented as a second helper." This blueprint's child-identifier masking must follow the identical convention — add `mask_child_id()` to this SAME file, not a new/duplicate masking helper elsewhere.

## 7. Existing Code to Reuse
- `get_current_admin` / `AdminSessionContext` (`core/deps.py`).
- `require_admin_scope("content-safety-audit:read")` (`core/deps.py`) — single confirmed scope string, following the real `resource:action` convention; do NOT attempt an OR-across-scopes check (`require_admin_scope` doesn't support it) — E.28's future RBAC matrix will map both a `trust_safety`-equivalent and `ai_ops`-equivalent admin role to this one scope string, which is the correct place to solve the "either role" requirement (role→scope mapping), not this endpoint's own dependency logic.
- `BaseRepository.list_paginated()` pagination pattern (`common/base_repository.py`).
- `mask_family_id()` pattern (`modules/admin/masking.py`) — add `mask_child_id()` alongside it in the same file.
- B-03's/B-04's `WeeklyReportRepository`/`AiInsightReportRepository` (extend with a `list_failed(cursor, limit)` method rather than duplicating query logic).
- **Existing `modules/admin/api.py` `AdminRouter`** — add this endpoint's route directly here (see §6), reusing its established `prefix="/v1/admin"` and per-route `require_admin_scope(...)` pattern exactly as C.26's B-05–B-08 routes already do.

## 8. Files to Create
- `tests/modules/dashboard/test_admin_content_safety_audit_log_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/dashboard/schemas.py` — add `ContentSafetyAuditLogEntryResponse`, `PaginatedContentSafetyAuditLogResponse`
- `src/noorheroes/modules/dashboard/repository.py` — add `list_failed(cursor, limit, report_type=None, date_range=None)` to the relevant repositories
- `src/noorheroes/modules/dashboard/service.py` — add `AdminContentSafetyAuditService` (or method on existing service)
- `src/noorheroes/modules/admin/api.py` — **add this endpoint's route to the EXISTING real `AdminRouter` in this file** (already hosts C.26's B-05–B-08 routes at `prefix="/v1/admin"`) — do not create a new/separate admin sub-router in `modules/dashboard/`
- `src/noorheroes/modules/admin/masking.py` — add `mask_child_id(child_id: str) -> str` alongside the existing `mask_family_id()`, same convention (`"chi_***" + last 4 chars`)

## 10. Backend Requirements
- Route: `GET /v1/admin/content-safety-audit-log`, added directly to the existing `modules/admin/api.py` `AdminRouter` (confirmed real file — prefix `/v1/admin` already applied there, matching C.26's B-05–B-08 route style exactly), requiring `get_current_admin` + `require_admin_scope("content-safety-audit:read")` — a single scope string (confirmed `require_admin_scope` has no OR-across-scopes support; per §6, the "trust_safety or ai_ops" requirement is a future E.28 role→scope mapping concern, not something this endpoint's dependency needs to encode itself).
- Query params: pagination (`cursor`, `limit`), optional filters `report_type` (`weekly_report|ai_insight_report` — full table-name values, confirmed against C.22 N-02's already-written extension, which explicitly widens "C.20's existing `weekly_report`" filter value, not a short `weekly` form), `date_range`.
- Response: masked child identifier via the new `mask_child_id()` (§9, added to the existing `modules/admin/masking.py`), `report_type`, `generated_at`, `failure_reason_tag` (from B-05's recorded failure reasons).
- **Zero mutating endpoints** — no PATCH/POST/DELETE for this resource, anywhere in `modules/admin/api.py`.

## 11. KMP Requirements
N/A — admin-only, not exposed to the mobile app.

## 12. NextJS Requirements
Consumed by N-01 (AI Report Content-Safety Audit Log page).

## 13. API Contract
- **HTTP Method:** GET
- **Endpoint:** `/v1/admin/content-safety-audit-log?cursor=&limit=&report_type=&date_from=&date_to=` (path corrected — lives directly under the existing `AdminRouter`'s `/v1/admin` prefix, per §6/§9, not a separate `/v1/admin/dashboard/...` path)
- **Auth:** Bearer, admin session
- **Authorization:** `require_admin_scope("content-safety-audit:read")` — single confirmed scope string (see §6/§10)
- **Response 200:**
```json
{
  "items": [
    { "masked_child_id": "chi_***a1b2", "report_type": "weekly_report", "generated_at": "ISO-8601", "failure_reason_tag": "possible_diagnosis_language" }
  ],
  "next_cursor": "string|null",
  "has_more": false
}
```
- **Error Responses:** `401` unauthenticated, `403` forbidden (missing `content-safety-audit:read` scope)
- **Admin API:** Yes — distinct from the User API in B-02/B-03; lives on the existing `modules/admin/api.py` router, never the parent-facing `DashboardRouter`.

## 14. Database Requirements
Read-only queries against `weekly_report`/`ai_insight_report` filtered `WHERE content_safety_passed = false`, using indexes already defined in B-04 (`(child_id, period_end DESC)` / `(child_id, generated_at DESC)`) — may need an additional index on `content_safety_passed` if query volume at scale warrants it (confirm with query-plan analysis before adding; do not add speculative indexes).

## 15. Validation
- `report_type` filter restricted to `weekly|ai_insight` literals (the only two types subject to content-safety gating per B-05's scope).
- Pagination params validated per platform's standard cursor-pagination convention.

## 16. Authentication
Bearer admin session (`get_current_admin`).

## 17. Authorization
`trust_safety` or `ai_ops` RBAC scope — this is the primary access control for this endpoint. No other admin role may access it.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Non-admin session | `401` |
| Admin without `trust_safety`/`ai_ops` scope | `403` |
| No failed reports exist | Empty `items: []`, not an error |

## 19. Offline First
N/A (admin web surface, not KMP).

## 20. Local Data
N/A.

## 21. Localization
Admin Portal's own localization system (NextJS `useTranslation()`) handles display copy; this API returns raw `failure_reason_tag` machine-readable strings, translated client-side if needed.

## 22. RTL
N/A (backend).

## 23. Analytics
N/A directly — this is itself a monitoring surface, not a tracked user action.

## 24. Performance
Read-only, low-traffic (internal trust/safety team usage), standard pagination sufficient — no aggressive caching needed given the audit/investigative nature of this data (should reflect near-real-time state).

## 25. Security
- Read-only, zero override capability — a report that failed validation stays blocked permanently, by design (PRD §12.5).
- Masked child identifier (via `mask_child_id()`, `modules/admin/masking.py`) prevents this audit surface from becoming a secondary PII-exposure vector.
- `require_admin_scope("content-safety-audit:read")` is the primary control — a single, confirmed real scope string (see §6); "either trust_safety or ai_ops can access this" is satisfied by E.28 eventually mapping both roles to this one scope, not by this endpoint attempting its own OR-logic.

## 26. Library Requirements
No new dependencies.

## 27. Testing
1. Unit test: admin with `content-safety-audit:read` scope can list failed reports.
2. Unit test: admin with `super_admin` scope can list failed reports (per `require_admin_scope`'s confirmed super_admin-always-passes behavior).
3. Unit test: admin without `content-safety-audit:read` (and without `super_admin`) receives `403`.
4. Unit test: non-admin session receives `401`.
5. Unit test: child identifier is masked via `mask_child_id()` in response.
6. Unit test: pagination and filters (`report_type` = `weekly_report`/`ai_insight_report`, `date_range`) work correctly.
7. Unit test: confirm no mutating route for this resource exists anywhere in `modules/admin/api.py`'s `AdminRouter` (structural test — enumerate this resource's registered methods, assert all are GET).

## 28. Documentation
OpenAPI docstring; note in admin API documentation that this endpoint is read-only by design with no override capability, per PRD §12.5.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm Scope String and Router Placement (Resolved by Direct Code Verification)**
- Task ID: B06-T01
- Objective: Re-verify `require_admin_scope()`'s single-scope-AND semantics and `modules/admin/api.py`'s router structure immediately before implementation (guard against drift since this research pass).
- Why This Is Required: Already confirmed via direct code read: `require_admin_scope(required_scope: str)` checks one scope string (plus an always-passing `"super_admin"` override) — no OR-across-scopes support. `modules/admin/api.py` already exists as a populated `AdminRouter = APIRouter(prefix="/v1/admin", tags=["admin"])` hosting C.26's B-05–B-08 routes in the exact same file. This task is a freshness re-check, not an open investigation.
- Existing Architecture to Follow: `core/deps.py` `require_admin_scope()`; `modules/admin/api.py`'s existing route style.
- Existing Files to Reuse: `core/deps.py`, `modules/admin/api.py`, `modules/admin/masking.py`.
- Files to Create: none (confirmation task).
- Files to Modify: none.
- Implementation Details: Re-read `core/deps.py::require_admin_scope` and `modules/admin/api.py` immediately before Task 02; confirm scope string `"content-safety-audit:read"` doesn't already collide with an existing scope name in `modules/admin/api.py`.
- Business Rules: PRD §8 RBAC restriction.
- Validation: N/A.
- Error Handling: N/A.
- Security: Core access-control decision for this endpoint.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: N/A.
- Documentation: Record re-check result.
- Dependencies: none.
- Do Not Change: Do not modify `require_admin_scope()` itself or any existing route in `modules/admin/api.py`.
- Expected Result: Confirmed implementation path (add to existing router, single scope string).
- Definition of Done: Re-check performed before Task 02.

**Task 02 — Extend Report Repositories with list_failed()**
- Task ID: B06-T02
- Objective: Query method for failed-validation rows.
- Why This Is Required: Data access for this endpoint.
- Existing Architecture to Follow: `BaseRepository.list_paginated()` cursor pattern.
- Existing Files to Reuse: `WeeklyReportRepository`, `AiInsightReportRepository` (from B-03).
- Files to Create: none.
- Files to Modify: `src/noorheroes/modules/dashboard/repository.py`.
- Implementation Details: `list_failed(cursor, limit, report_type=None, date_range=None) -> PageResult[...]` filtering `content_safety_passed=false`, unioned across both tables (or queried per-type if `report_type` filter provided).
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: N/A.
- Security: N/A.
- Performance: Uses existing indexes; consider a combined query strategy (UNION ALL) vs. two separate paginated queries — choose based on the platform's existing multi-table pagination conventions if one exists.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 05.
- Documentation: Docstring.
- Dependencies: B-03, B-04.
- Do Not Change: Do not alter `content_safety_passed=true` query paths used by B-03.
- Expected Result: Method returns correctly filtered/paginated rows.
- Definition of Done: Matches §14.

**Task 03 — Implement Masking Utility and Response Schemas**
- Task ID: B06-T03
- Objective: Build `ContentSafetyAuditLogEntryResponse` with masked child identifier.
- Why This Is Required: PRD explicitly requires masked identifiers, not raw child IDs.
- Existing Architecture to Follow: Check `common/utils/` for an existing masking utility (e.g., a general-purpose PII-masking helper) before writing a new one.
- Existing Files to Reuse: Existing masking utility if found; `common/schemas.py` base model.
- Files to Create: none.
- Files to Modify: `src/noorheroes/modules/dashboard/schemas.py`.
- Implementation Details: Mask child_id consistently (e.g., first 4 chars + asterisks); include `failure_reason_tag` sourced from B-05's recorded reasons.
- Business Rules: PRD §9 (masked identifier, non-reversible in this response).
- Validation: N/A.
- Error Handling: N/A.
- Security: Prevents secondary PII exposure.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 05.
- Documentation: Docstring.
- Dependencies: none.
- Do Not Change: N/A.
- Expected Result: Response never exposes raw child_id.
- Definition of Done: Masking verified in tests.

**Task 04 — Implement Route with RBAC Guard**
- Task ID: B06-T04
- Objective: Expose the endpoint, read-only.
- Why This Is Required: Public (admin) contract delivery.
- Existing Architecture to Follow: The existing real `AdminRouter` in `modules/admin/api.py` (`get_current_admin`, per-route `require_admin_scope(...)`, exactly as its current B-05–B-08 handlers already do).
- Existing Files to Reuse: `modules/admin/api.py`'s existing router instance — add this route to it directly.
- Files to Create: none.
- Files to Modify: `src/noorheroes/modules/admin/api.py` (add this route to the existing `AdminRouter`, NOT a new sub-router in `modules/dashboard/`).
- Implementation Details: `@router.get("/content-safety-audit-log", response_model=PaginatedContentSafetyAuditLogResponse)` with `admin: AdminSessionContext = Depends(require_admin_scope("content-safety-audit:read"))`, matching the exact decorator/dependency style of the existing `list_consent_types`/`get_ai_retention_config` handlers in this same file. GET-only — no other HTTP method added for this resource.
- Business Rules: PRD §8, §9.
- Validation: Query param validation per §15.
- Error Handling: Per §18.
- Security: RBAC scope enforcement; zero mutating capability.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 05.
- Documentation: OpenAPI docstring noting read-only, no-override design.
- Dependencies: Tasks 01–03.
- Do Not Change: Do not add this route under the parent-only `DashboardRouter` (B-01) — it must be a separate, admin-scoped router to avoid conflating parent and admin API surfaces (project instruction: never mix User API and Admin API).
- Expected Result: Endpoint live at correct admin route.
- Definition of Done: Matches §13 contract.

**Task 05 — Write Test Suite**
- Task ID: B06-T05
- Objective: Cover §27 scenarios.
- Why This Is Required: QA and security verification.
- Existing Architecture to Follow: pytest + admin session fixtures.
- Existing Files to Reuse: Existing admin auth test fixtures.
- Files to Create: `tests/modules/dashboard/test_admin_content_safety_audit_log_api.py`.
- Files to Modify: none.
- Implementation Details: 7 test cases per §27, including the structural "no mutating route" test.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: N/A.
- Security: RBAC and no-override tests are security-critical.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test docstrings.
- Dependencies: Tasks 01–04.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 green.

## 30. Definition of Done
Read-only admin endpoint live, RBAC-restricted to `trust_safety`/`ai_ops`, masked child identifiers, zero mutating capability, all tests green.

## 31. Final Verification Checklist
- [ ] Route added to the existing real `modules/admin/api.py` `AdminRouter`, not a new sub-router
- [ ] `require_admin_scope("content-safety-audit:read")` used — single scope string, no invented OR-logic
- [ ] `mask_child_id()` added to the existing `modules/admin/masking.py`, not a new masking file
- [ ] `report_type` filter uses full table names (`weekly_report`/`ai_insight_report`), matching C.22 N-02's confirmed enum
- [ ] Confirmed GET-only for this resource within `AdminRouter`
- [ ] Separate from parent-facing `DashboardRouter` (User API vs Admin API not mixed)
- [ ] No audit_log write needed for this page itself (no mutating actions exist)
