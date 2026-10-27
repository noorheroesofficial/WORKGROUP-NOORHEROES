# B-02 — Active-Subscription Search & Detail API

## 1. Feature Context
The investigation surface for Billing Ops: search by any of three identifiers, then a read-only detail view whose billing-event/comp-grant timeline is unambiguous by construction — every entry carries a server-provided `type` field so the two can never be confused at the data layer, let alone the UI layer.

## 2. Parent Feature
E.33 — Subscription Management & Billing Ops

## 3. Sub-feature
1.2 Active-Subscription Search & Detail API (ID: **B-02**)

## 4. Objective
Build `GET /v1/admin/subscriptions/search` and `GET /v1/admin/subscriptions/{id}`, the latter returning a unified, chronologically interleaved, `type`-tagged timeline of billing events and comp grants.

## 5. Business Requirements
- Search by family/parent/subscription ID.
- Detail response includes current state/plan and a full timeline merging `billing_event` (C.24) and `comp_grant` (B-04) entries in true chronological order, each unambiguously tagged.
- Read-only — no mutation path exists on this endpoint; the only mutating action reachable from this view is the separate comp-grant issuance (B-04).
- Edge Case 7: a family with both real billing history and comp grants across different periods must show a correctly interleaved, not separately grouped, timeline.

## 6. Existing Architecture
`subscriptions` bounded context, `app/subscriptions/routers/admin_subscription_router.py`, reading from C.24's existing `billing_event` table and B-04's new `comp_grant` table via a merge-and-sort query, never a duplicated entitlement-state computation.

## 7. Existing Code to Reuse
- C.24: `app/subscriptions/repositories/billing_event_repository.py` (read-only reuse)
- E.28's `AuditLogService.log_action()`
- E.32's search-endpoint pattern (B-01 of E.32) as the structural template for multi-identifier search

## 8. Files to Create
- `app/subscriptions/routers/admin_subscription_router.py`
- `app/subscriptions/services/subscription_search_service.py`
- `app/subscriptions/repositories/subscription_search_repository.py`
- `app/subscriptions/schemas/subscription_detail_schema.py` — `SubscriptionTimelineEntry` with a required, non-optional `type: Literal["billing_event", "comp_grant"]` discriminator field

## 9. Files to Modify
- `app/subscriptions/routers/__init__.py` — register router

## 10. Backend Requirements
- `SubscriptionSearchService.search()`: dispatches on exactly one of `family_id`/`parent_id`/`subscription_id`.
- `SubscriptionSearchService.get_detail()`: fetches billing events from C.24's table and comp grants from B-04's table independently, merges by timestamp, and serializes each through a discriminated-union schema so the `type` field is structurally always present — never inferred from which table a row happened to come from at the API-response layer (the discriminator is set explicitly during merge, not left implicit).
- No write method exists anywhere in this service, by construction (mirrors E.32 B-04's read-only entitlement-inspector guarantee).

## 11. Required API / API Contract
`GET /v1/admin/subscriptions/search?query=&type=family_id|parent_id|subscription_id` → `200` list.
`GET /v1/admin/subscriptions/{id}` → `200 { "state", "plan", "timeline": [ { "type": "billing_event"|"comp_grant", ... } ] }`.

## 12. Database Requirements
No new tables — reads C.24's `billing_event` and B-04's `comp_grant`.

## 13. Validation
Exactly-one-identifier-type validator for search.

## 14. Authentication
`get_current_admin`.

## 15. Authorization
`require_admin_scope("support")` for search/detail (read-only visibility per PRD §1.15's broader `support`+ access pattern, distinct from `billing_ops`-restricted mutation).

## 16. Error Handling
`400` for ambiguous search query; `404` for unknown subscription detail; empty list (not `404`) for no search matches.

## 17. Security
This endpoint is provably read-only (no write/update method exists in the service, structural guarantee). The `type` discriminator is set explicitly at merge time, never left to client-side inference — mandatory test confirms a fixture timeline with both entry types round-trips with correct, unambiguous `type` values.

## 18. Analytics
`subscription_search_performed`, `subscription_detail_viewed`, `billing_event_viewed` per §1.19.

## 19. Performance
Indexed merge query on `(subscription_id, created_at)` across both source tables; timeline paginated if volume warrants (confirm against expected billing-event frequency — likely unnecessary given monthly/annual billing cadence, but design the query to support a `limit`/`offset` if needed later).

## 20. Library Requirements
FastAPI, Pydantic v2 (discriminated union), SQLAlchemy 2.0 async. No new libraries.

## 21. Testing
Unit: exactly-one-identifier validation, chronological merge-and-sort logic. Integration: **mandatory** — fixture subscription with both billing events and comp grants across different periods returns a correctly interleaved, unambiguously-typed timeline (Edge Case 7); **mandatory** — structural test confirming zero write/update method exists in this service. Search-by-each-identifier-type tests.

## 22. Documentation
OpenAPI docstring noting the timeline's `type` field is the sole, authoritative way to distinguish entry kinds.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Define the Discriminated-Union Timeline Schema**
Objective: `SubscriptionTimelineEntry` with a required `type` literal. Files: `schemas/subscription_detail_schema.py`. Tests: schema validation. Definition of Done: schema used by Task 03.

**Task 02 — Implement `SubscriptionSearchRepository`**
Objective: Multi-identifier lookup, plus independent billing-event and comp-grant fetches for detail. Files: `repositories/subscription_search_repository.py`. Dependencies: Task 01. Tests: repository tests. Definition of Done: tests pass.

**Task 03 — Implement `SubscriptionSearchService` with Merge-and-Sort**
Objective: Chronological interleave with explicit `type` tagging at merge time. Files: `services/subscription_search_service.py`. Dependencies: Task 02. Tests: **mandatory** — interleaved-timeline-with-both-types test. Definition of Done: test passes.

**Task 04 — Implement Router Endpoints**
Objective: Wire search and detail endpoints, `support`-scope-gated. Files: `routers/admin_subscription_router.py`. Dependencies: Task 03. Tests: endpoint integration tests. Definition of Done: tests pass.

**Task 05 — Confirm Read-Only Guarantee**
Objective: **Mandatory** structural test confirming no write/update method exists anywhere in this service. Dependencies: Task 03. Definition of Done: test passes.

**Task 06 — Add Full Test Suite**
Objective: Complete coverage per §21, both mandatory tests included. Definition of Done: all green in CI.

**Task 07 — Final Code Review**
Objective: Confirm the `type` discriminator is never left to implicit inference anywhere in the merge path. Definition of Done: checklist in §24 checked.

## 24. Final Verification Checklist
- [ ] Timeline correctly interleaves billing events and comp grants in true chronological order — mandatory test passing
- [ ] `type` field always explicitly set at merge time, never implicit — mandatory test passing
- [ ] Zero write/update method exists in this service — mandatory structural test passing
- [ ] Search supports all three identifier types with exactly-one-identifier validation

## 25. Definition of Done
Billing Ops can search and inspect any subscription's full, correctly interleaved, unambiguously-typed billing history through a provably read-only API.
