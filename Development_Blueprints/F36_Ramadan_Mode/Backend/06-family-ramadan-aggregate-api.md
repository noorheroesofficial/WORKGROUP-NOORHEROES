# B-06 — Family Ramadan Aggregate API

## 1. Feature Context
Gives parents a warm, family-wide view of Ramadan progress without ever exposing a per-child comparison structure — the response DTO's absence of a per-child array is a structural, contract-level guarantee against sibling-comparison, not a UI-only convention.

## 2. Parent Feature
F.36 — Ramadan Mode

## 3. Sub-feature
1.6 Family Ramadan Aggregate API (ID: **B-06**)

## 4. Objective
Build `GET /v1/ramadan/family-aggregate`, returning an aggregate-only family rollup with no per-child array field.

## 5. Business Requirements
- §3.4: Response — aggregate-only family rollup, no per-child array field.
- §5 Backend AI prompt item 5: NO per-child-array field, structural test mirroring A.7/A.11's pattern.
- Edge Case 4: two children on different fasting approaches → Family Aggregate reflects each child's own scope without implying comparison.
- §1.12 Empty States: new family joining mid-Ramadan → prior nights marked "not applicable," not missed.

## 6. Existing Architecture
`ramadan` bounded context, `app/ramadan/routers/family_aggregate_router.py`, following the same no-sibling-comparison DTO pattern already established in A.7's and A.11's own family-aggregate endpoints (reuse their structural approach, do not invent a new one).

## 7. Existing Code to Reuse
- A.7's / A.11's existing family-aggregate DTO pattern (structural precedent — confirm exact class before implementation)
- `app/shared/base_service.py::BaseService`
- `core/deps.py::get_current_parent`

## 8. Files to Create
- `app/ramadan/routers/family_aggregate_router.py`
- `app/ramadan/services/family_aggregate_service.py`
- `app/ramadan/repositories/family_aggregate_repository.py` (or query methods added to `journey_progress_repository.py`/`fasting_log_repository.py` — prefer reusing existing repositories over a new one if the aggregate query is a simple `GROUP BY`)
- `app/ramadan/schemas/family_aggregate_schema.py`

## 9. Files to Modify
- `app/ramadan/routers/__init__.py` — register router

## 10. Backend Requirements
- `FamilyAggregateService.get_aggregate(family_id)`: queries `ramadan_journey_progress` and `fasting_logs` across all children in the family, returning only aggregate figures (e.g., total nights completed family-wide, participation rate) — no `children: [...]` array with individual completion counts.
- Empty state: a family with no prior activity (new/mid-season join) returns nights as "not applicable" for the pre-join period rather than a zero/missed count.
- Divergent-approach handling: aggregate computation must not implicitly rank or compare — e.g., avoid any "child X completed more than child Y" derivable field.

## 11. Required API / API Contract
`GET /v1/ramadan/family-aggregate` → `200` aggregate-only rollup, **no per-child array field**. **Auth:** `get_current_parent`. **Validation:** N/A (no request body). **Error Responses:** `200` with zeroed/not-applicable aggregate for a family with no Ramadan activity — never an error for the empty case.

## 12. Database Requirements
Reads `ramadan_journey_progress`, `fasting_logs`, and family/child membership (A.1) — no new table required beyond what B-04/B-05 already created.

## 13. Validation
N/A beyond standard auth — this is a read-only aggregation endpoint.

## 14. Authentication
`get_current_parent`.

## 15. Authorization
Parent may only view their own family's aggregate.

## 16. Error Handling
No Ramadan activity for the family → `200` with an empty/not-applicable aggregate payload, not a `404`.

## 17. Offline First
K-08 (client) may cache the last-fetched aggregate for offline display; this endpoint is the sync source.

## 18. Local Data
N/A server-side.

## 19. Localization
N/A — numeric/aggregate data only; display strings client-side.

## 20. RTL
N/A.

## 21. Analytics
`ramadan_family_report_viewed` per §1.19.

## 22. Performance
Cache the computed aggregate with a short TTL (invalidated on new completion/log-write events from B-04/B-05) given it changes at most nightly per family.

## 23. Security
The absence of a per-child array field is enforced at the schema/DTO level, not just by omission in the service logic — mandatory structural test.

## 26. Library Requirements
FastAPI, Pydantic v2, SQLAlchemy 2.0 async, Redis (caching). No new libraries.

## 27. Testing
Unit: aggregate-computation correctness for a multi-child, divergent-approach family (Edge Case 4). Integration: **mandatory** — reflection/structural test confirming the response schema has no per-child-array field (Backend AI prompt item 5); empty-state test for a new/mid-season-joining family.

## 28. Documentation
OpenAPI docstring explicitly stating the no-per-child-array guarantee as a contract property.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm A.7/A.11's Existing Aggregate DTO Pattern**
Objective: Identify the exact structural precedent to mirror. Files to Read: A.7's and A.11's family-aggregate schema files. Definition of Done: pattern documented before Task 02 proceeds.

**Task 02 — Define the Aggregate Response Schema**
Objective: `FamilyAggregateResponse` with zero per-child-array fields. Files to Create: `schemas/family_aggregate_schema.py`. Dependencies: Task 01. Tests: **mandatory** — schema-introspection test confirming no per-child-array field exists. Definition of Done: test passes.

**Task 03 — Implement Aggregate Query Logic**
Objective: `GROUP BY`-style aggregation across `ramadan_journey_progress`/`fasting_logs` for the family. Files to Create: `repositories/family_aggregate_repository.py` (or extend existing repositories). Tests: multi-child aggregation test. Definition of Done: tests pass.

**Task 04 — Implement `FamilyAggregateService`**
Objective: Orchestrates the aggregate query, handles the empty/not-applicable state. Files to Create: `services/family_aggregate_service.py`. Dependencies: Task 03. Tests: empty-state test. Definition of Done: test passes.

**Task 05 — Implement the Router Endpoint**
Objective: `GET /v1/ramadan/family-aggregate`. Files to Create: `routers/family_aggregate_router.py`. Files to Modify: `routers/__init__.py`. Dependencies: Task 04. Tests: endpoint integration tests. Definition of Done: tests pass.

**Task 06 — Add Caching with Invalidation**
Objective: Short-TTL cache invalidated on new completion/log-write. Dependencies: Task 05. Tests: cache-invalidation test. Definition of Done: test passes.

**Task 07 — Add Full Test Suite**
Objective: Complete coverage per §27, including the mandatory structural test. Definition of Done: all green in CI.

**Task 08 — Final Code Review**
Objective: Confirm no code path anywhere in this endpoint's response construction could leak per-child comparative data. Definition of Done: checklist in §30 checked.

## 30. Final Verification Checklist
- [ ] Response schema has no per-child-array field — mandatory structural test passing
- [ ] Divergent-approach families aggregate without implying comparison
- [ ] Empty/new-family state returns "not applicable," not zero/missed
- [ ] Caching invalidates correctly on new activity

## 31. Definition of Done
Parents get a warm, honest family-wide Ramadan view with a structurally-guaranteed absence of sibling comparison data.
