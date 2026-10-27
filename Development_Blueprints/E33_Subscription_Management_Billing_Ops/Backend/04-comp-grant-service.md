# B-04 — Comp Grant Service

## 1. Feature Context
The platform's one sanctioned exception mechanism for granting entitlement outside a real purchase — deliberately isolated in its own table with no shared identifier namespace with `billing_events`, so no future join or report can ever accidentally count a goodwill credit as real revenue.

## 2. Parent Feature
E.33 — Subscription Management & Billing Ops

## 3. Sub-feature
1.4 Comp Grant Service (ID: **B-04**)

## 4. Objective
Build `POST /v1/admin/subscriptions/{id}/comp-grant` writing exclusively to a new, structurally distinct `comp_grant` table, plus the effective-entitlement resolution logic consulted by C.24's `GET /v1/entitlements/check` for correctly resolving comp-grant-vs-billing-event precedence.

## 5. Business Requirements
- FR-6: comp grants are a distinct, separately-logged mechanism, never written to `billing_events`, always carrying a reason code and issuing-admin attribution, always clearly labeled as an exception.
- §5 Backend AI prompt item 2 (second-highest-priority guarantee): comp grants write exclusively to the new table; a test must confirm a comp grant never appears in any query selecting from `billing_events`, and that the two tables share no FK or identifier namespace.
- §5 item 3: effective-entitlement resolution favors the most current/privileged of comp-grant vs. billing-event state when both exist (Edge Case 1) — never a conflict error.
- Edge Case 5: attribution survives the issuing admin's later account disable (E.32's disable-never-deletes-attribution principle).

## 6. Existing Architecture
`subscriptions` bounded context, `app/subscriptions/services/comp_grant_service.py`, consulted by (but not embedded into) C.24's existing `EntitlementResolutionService`.

## 7. Existing Code to Reuse
- E.28's `AuditLogService.log_action()`
- C.24's `EntitlementResolutionService` interface — this sub-feature adds a comp-grant-aware resolution step, called by C.24's existing `GET /v1/entitlements/check`, not a parallel duplicate endpoint

## 8. Files to Create
- `app/subscriptions/routers/comp_grant_router.py`
- `app/subscriptions/services/comp_grant_service.py`
- `app/subscriptions/repositories/comp_grant_repository.py`
- `app/subscriptions/schemas/comp_grant_schema.py` — `CompGrantCreate` (`reason_code` required)
- `alembic/versions/xxxx_create_comp_grant_table.py`

## 9. Files to Modify
- `app/subscriptions/routers/__init__.py` — register router
- C.24's `app/subscriptions/services/entitlement_resolution_service.py` — add a comp-grant-consulting step to `resolve_effective_entitlement()`, additive only, no change to its existing billing-event-derived logic

## 10. Backend Requirements
- `CompGrantService.issue()`: validates `reason_code` is present, writes a `comp_grant` row with `issued_by`, `issued_at`, `expires_at` (`issued_at + duration_days`) — never touches `billing_events` in any code path.
- `comp_grant` table has zero foreign key to `billing_event` and uses its own `grant_id` PK namespace, distinct from `billing_event.event_id` — confirmed by a mandatory schema-introspection test.
- `EntitlementResolutionService.resolve_effective_entitlement()` (extended): when both an active comp grant and a real billing-event-derived state exist for the same subscription, the real billing-event-derived state takes precedence going forward — the comp grant's remaining value simply becomes moot, never a raised conflict.

## 11. Required API / API Contract
`POST /v1/admin/subscriptions/{id}/comp-grant` `{reason_code, entitlement_level, duration_days}` → `201`.

## 12. Database Requirements
`comp_grant(grant_id PK, subscription_id FK, reason_code, entitlement_level, duration_days, issued_by FK, issued_at, expires_at)`, `CHECK (reason_code IS NOT NULL)`. Index `(subscription_id, issued_at DESC)`. Retained indefinitely (§4.5, matching C.24's `invoice` retention standard). No FK to `billing_event`.

## 13. Validation
`reason_code` required, non-empty, validated against a known reason-code enum/registry. `duration_days` positive integer.

## 14. Authentication
`get_current_admin`.

## 15. Authorization
`require_admin_scope("billing_ops")` — comp-grant issuance is restricted specifically to `billing_ops`, distinct from the broader `support`+ read-only visibility elsewhere in this module (principle of least privilege, PRD §12.5).

## 16. Error Handling
`422` for missing/invalid `reason_code`; `404` for unknown subscription.

## 17. Security
This sub-feature's core guarantee (structural separation from `billing_events`) is verified by a mandatory test querying `billing_events` for any row matching a known comp-grant ID and confirming none exists, plus a schema-level test confirming no FK/shared-namespace path exists between the two tables. The precedence-resolution logic is verified by a mandatory fixture test: an active comp grant followed by a genuine billing event resolves cleanly to the billing-event-derived state.

## 18. Analytics
`comp_grant_issued` (with `reason_code`), `comp_grant_viewed` per §1.19; comp-grant issuance-rate spike alerting (§10 DevOps).

## 19. Performance
Indexed lookups on `subscription_id`.

## 20. Library Requirements
FastAPI, Pydantic v2, SQLAlchemy 2.0 async, Alembic. No new libraries.

## 21. Testing
Unit: `reason_code` validation. Integration: **mandatory** — comp grant never appears in any `billing_events` query, and the two tables share no FK/identifier namespace (schema-introspection test); **mandatory** — fixture subscription with an active comp grant that then receives a genuine billing event resolves to the billing-event-derived state without a conflict error; attribution remains queryable after the issuing admin is disabled (cross-ref E.32 B-07).

## 22. Documentation
OpenAPI docstring stating explicitly that this endpoint never writes to `billing_events` and that comp grants are always excluded from real-revenue reporting.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Write Migration for `comp_grant`**
Objective: Structurally distinct table, no FK to `billing_event`, `CHECK (reason_code IS NOT NULL)`. Files: `alembic/versions/xxxx_create_comp_grant_table.py`. Tests: migration test + schema-introspection test confirming no shared namespace with `billing_event`. Definition of Done: both tests pass.

**Task 02 — Define Schemas**
Objective: `CompGrantCreate` with required `reason_code`. Files: `schemas/comp_grant_schema.py`. Dependencies: Task 01. Tests: validation tests. Definition of Done: tests pass.

**Task 03 — Implement `CompGrantRepository`**
Objective: Insert-only-in-practice repository (no update endpoint specified by PRD) writing exclusively to `comp_grant`. Files: `repositories/comp_grant_repository.py`. Dependencies: Task 01. Tests: **mandatory** — write-path-never-touches-billing_events test. Definition of Done: test passes.

**Task 04 — Implement `CompGrantService`**
Objective: Issue logic with reason-code validation. Files: `services/comp_grant_service.py`. Dependencies: Task 03. Tests: issuance tests. Definition of Done: tests pass.

**Task 05 — Extend `EntitlementResolutionService` with Precedence Logic**
Objective: Additive comp-grant-consulting step favoring real billing-event state when both exist. Dependencies: Task 04, C.24. Tests: **mandatory** — comp-grant-then-real-billing-event precedence fixture test. Definition of Done: test passes.

**Task 06 — Implement the Router Endpoint**
Objective: `POST` endpoint, `billing_ops`-scope-gated. Files: `routers/comp_grant_router.py`. Dependencies: Task 04. Tests: endpoint integration tests. Definition of Done: tests pass.

**Task 07 — Wire Audit Logging**
Objective: Log every issuance with attribution. Dependencies: Task 06. Tests: audit-entry test. Definition of Done: test passes.

**Task 08 — Add Full Test Suite**
Objective: Complete coverage per §21, all mandatory tests included. Definition of Done: all green in CI.

**Task 09 — Final Code Review**
Objective: Confirm zero code path writes a comp grant to `billing_events`, and confirm the precedence logic never raises a conflict for the dual-state scenario. Definition of Done: checklist in §24 checked.

## 24. Final Verification Checklist
- [ ] `comp_grant` table structurally separate from `billing_event` (no FK, no shared namespace) — mandatory test passing
- [ ] Comp grant issuance requires a `reason_code` — hard, zero-tolerance
- [ ] Dual-state (comp-grant + real billing event) resolves to billing-event precedence without conflict — mandatory test passing
- [ ] Attribution survives issuing-admin disable
- [ ] `billing_ops` scope enforced

## 25. Definition of Done
Comp grants are issued through a provably isolated mechanism that can never be conflated with real revenue at the data-model level, with correct precedence resolution when a real purchase later supersedes a comp grant.
