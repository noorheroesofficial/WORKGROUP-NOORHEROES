# B-01 — Plan/Pricing/Entitlement Management API

## 1. Feature Context
The authoring surface for plans and pricing, whose defining discipline is non-retroactivity: an entitlement change touches only new subscribers unless a distinct, explicitly-confirmed, higher-friction action says otherwise — and deactivating a plan never touches an existing subscriber's entitlement at all.

## 2. Parent Feature
E.33 — Subscription Management & Billing Ops

## 3. Sub-feature
1.1 Plan/Pricing/Entitlement Management API (ID: **B-01**)

## 4. Objective
Build create/update/deactivate/reactivate endpoints for `plan`, with entitlement updates defaulting to new-subscribers-only scope and requiring an explicit `apply_to_existing=true` flag for the broader, higher-friction path.

## 5. Business Requirements
- FR-2/FR-7/FR-8: create plan; update plan entitlements (new subscribers only by default); deactivate a plan (existing subscribers keep entitlements); reactivate restores prior configuration.
- FR-8: entitlement updates apply only to new subscribers unless the distinct `apply_to_existing=true` action is explicitly taken.
- Edge Case 2: reactivation restores the plan's prior configuration, distinct from creating a new plan.
- Edge Case 4: concurrent plan edits use standard last-write-wins semantics (lower stakes than C.21's optimistic-concurrency child-state protection).

## 6. Existing Architecture
Extends C.24's existing `subscriptions` bounded context `Plan Service` — this sub-feature adds admin-authoring endpoints, it does not reimplement C.24's entitlement-determination or consumer-facing `/v1/billing/plans` contract.

## 7. Existing Code to Reuse
- C.24: `app/subscriptions/services/plan_service.py::PlanService` (extended, not duplicated)
- `app/shared/base_service.py::BaseService`, `app/shared/base_repository.py::BaseRepository`
- E.28's `AuditLogService.log_action()`, `require_admin_scope()`

## 8. Files to Create
- `app/subscriptions/routers/admin_plan_router.py`
- `app/subscriptions/schemas/admin_plan_schema.py` — `PlanCreate`, `PlanEntitlementUpdate` (with `apply_to_existing: bool = False`), `PlanDeactivateRequest`

## 9. Files to Modify
- `app/subscriptions/services/plan_service.py` — add `update_entitlements()` (scope-aware), `deactivate()`, `reactivate()` methods
- `app/subscriptions/routers/__init__.py` — register admin router

## 10. Backend Requirements
- `PlanService.update_entitlements(plan_id, new_entitlements, apply_to_existing=False)`: when `apply_to_existing` is `False` (the default), only the plan's own "effective entitlement set for new subscriptions" pointer is updated — existing `subscription` rows retain a reference to the entitlement snapshot in effect at their own subscribe time (versioned entitlement snapshot, not a live FK to the plan's mutable current state). When `True`, a distinct, separately-logged bulk-update path applies the new entitlements to existing subscribers too.
- `PlanService.deactivate(plan_id)`: sets `plan.active=false`; existing subscriptions are entirely unaffected (they reference their own entitlement snapshot, not `plan.active`); new subscription attempts against this plan are rejected at the consumer-facing purchase-initiation layer (C.24, cross-checked here).
- `PlanService.reactivate(plan_id)`: sets `plan.active=true`, restoring the plan's last configuration — distinct code path from `create()`, confirmed by a dedicated test that reactivation preserves the original `plan_id` and historical subscriber references.

## 11. Required API / API Contract
`POST /v1/admin/plans` `{name, pricing, entitlements, child_capacity}` → `201`.
`PATCH /v1/admin/plans/{id}` `{entitlements, apply_to_existing?: false}` → `200`.
`POST /v1/admin/plans/{id}/deactivate` → `200`.
`POST /v1/admin/plans/{id}/reactivate` → `200`.

## 12. Database Requirements
Extends C.24's `plan` table (no schema change needed if entitlements are already versioned per-subscription at `subscription.entitlement_snapshot_id`; confirm against C.24's schema — if `subscription` currently FKs live to `plan.entitlements`, this sub-feature's migration introduces the snapshot table/column to make non-retroactivity structurally true rather than merely convention-enforced).

## 13. Validation
`apply_to_existing` defaults to `False`, must be explicit `True` (not truthy-coerced from arbitrary values) to take the broader path. Entitlement fields validated against C.24's existing entitlement schema.

## 14. Authentication
`get_current_admin`.

## 15. Authorization
`require_admin_scope("billing_ops")` for all four endpoints (mutating actions restricted per PRD §1.15).

## 16. Error Handling
`404` for unknown plan; `409` for reactivating an already-active plan; standard validation `422`.

## 17. Security
Non-retroactivity is enforced structurally via the entitlement-snapshot mechanism, not merely by an application-layer default — mandatory test confirms an existing subscriber's entitlement is genuinely unaffected by a default (non-`apply_to_existing`) entitlement update, verified by re-reading the subscriber's own snapshot reference rather than trusting the plan's mutable current state.

## 18. Analytics
`plan_created`, `plan_entitlement_updated`, `plan_deactivated`, `plan_reactivated` events per §1.19.

## 19. Performance
Indexed on `plan.id`, `plan.active`.

## 20. Library Requirements
FastAPI, Pydantic v2, SQLAlchemy 2.0 async, Alembic. No new libraries.

## 21. Testing
Unit: `apply_to_existing` explicit-True-only gating. Integration: **mandatory** — existing subscriber's entitlement unaffected by a default entitlement update; **mandatory** — `apply_to_existing=true` correctly updates existing subscribers, only when explicitly present; deactivate leaves existing subscribers unaffected while blocking new subscriptions; reactivate restores prior configuration under the same `plan_id`.

## 22. Documentation
OpenAPI docstrings; note on `PATCH` that omitting `apply_to_existing` (or setting it `false`) is the safe, default, non-retroactive path.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Confirm/Extend Entitlement-Snapshot Schema**
Objective: Ensure `subscription` references an immutable entitlement snapshot at subscribe-time rather than a live FK to `plan`. Files: migration if needed. Tests: snapshot-immutability test. Definition of Done: structural non-retroactivity confirmed.

**Task 02 — Define Schemas**
Objective: `PlanCreate`, `PlanEntitlementUpdate` (`apply_to_existing: bool = False`), `PlanDeactivateRequest`. Files: `schemas/admin_plan_schema.py`. Dependencies: Task 01. Tests: schema validation. Definition of Done: schema used by Task 04.

**Task 03 — Extend `PlanService`**
Objective: `update_entitlements()`, `deactivate()`, `reactivate()` methods. Files: `services/plan_service.py`. Dependencies: Task 01, Task 02. Tests: **mandatory** — existing-subscriber-unaffected-by-default-update test. Definition of Done: test passes.

**Task 04 — Implement Router Endpoints**
Objective: Wire all four endpoints, `billing_ops`-scope-gated. Files: `routers/admin_plan_router.py`. Dependencies: Task 03. Tests: endpoint integration tests. Definition of Done: tests pass.

**Task 05 — Implement the `apply_to_existing=true` Broader Path**
Objective: Distinct, separately-logged bulk-update logic. Dependencies: Task 03. Tests: **mandatory** — broader-application test confirms existing subscribers updated only when flag explicitly present. Definition of Done: test passes.

**Task 06 — Wire Audit Logging**
Objective: Log create/update/deactivate/reactivate with before/after entitlement state. Dependencies: Task 04. Tests: audit-entry test. Definition of Done: test passes.

**Task 07 — Add Full Test Suite**
Objective: Complete coverage per §21, both mandatory tests included. Definition of Done: all green in CI.

**Task 08 — Final Code Review**
Objective: Confirm non-retroactivity is structural (snapshot-based), not merely a default parameter value that could be bypassed by a future caller. Definition of Done: checklist in §24 checked.

## 24. Final Verification Checklist
- [ ] Entitlement updates default to new-subscribers-only via a structural snapshot mechanism — mandatory test passing
- [ ] `apply_to_existing=true` broader path works only when explicitly present — mandatory test passing
- [ ] Deactivation never affects existing subscribers, blocks only new subscriptions
- [ ] Reactivation restores prior configuration under the same `plan_id`
- [ ] `billing_ops` scope enforced on all four endpoints

## 25. Definition of Done
Plans are authored and modified with non-retroactivity enforced structurally, not conventionally — existing subscribers are provably unaffected by routine plan edits or deactivation, matching the platform's broader non-retroactive-restriction philosophy.
