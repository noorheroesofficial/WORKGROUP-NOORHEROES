# Blueprint: Dashboard Aggregation API

## 1. Feature Context
Platform: NoorHeroes Backend (FastAPI). Module: `src/noorheroes/modules/dashboard/`. This blueprint delivers the primary read endpoint for the Parent Dashboard landing screen: `GET /v1/parent/dashboard?child_id=`.

## 2. Parent Feature
C.20 — Parent Dashboard.

## 3. Sub-feature
B-02 — Dashboard Aggregation API.

## 4. Objective
Compose a single aggregated read model for the Dashboard landing screen from Mastery (A.9), Reward (A.11), Habit (A.7), Restriction Engine (C.23), and Entitlement (C.24) services, scoped to one child, protected by the B-01 gate plus family-ownership validation.

## 5. Business Requirements
Source: PRD §1.7 FR-1, FR-2, FR-3, FR-7, §3.1, §3.4 (`GET /v1/parent/dashboard`), §3.5, Acceptance Criteria §1.9, Edge Cases §1.10 (#1, #2, #3, #4, #7).
- Components: child selector, weekly report preview, activity timeline preview, screen-time summary, module shortcut grid (grid itself is client-side navigation, not server data).
- `child_id` must belong to the authenticated parent's own family.
- Disabled/archived children remain selectable for read-only viewing (no live-session actions offered).
- Zero-activity child → explicit empty-state payload, not blank/broken.
- Each component degrades independently on individual fetch failure.
- Cache-then-refresh: short-to-medium TTL, weekly-report-derived fields cached longer than activity-timeline fields.

## 6. Existing Architecture — VERIFIED AGAINST ACTUAL CODEBASE
`backend/src/noorheroes/modules/rewards/` today only implements the reward RULE service (`rule_service.py`, `rule_api.py`, admin-facing reward-rule configuration, C.20/A.11's `RewardService.get_balance()` runtime-balance method described in the architecture doc is NOT yet implemented — `rewards/__init__.py` has no such service file). `modules/learning/` and `modules/subscriptions/` are currently stub packages (`__init__.py` only, per direct filesystem check) — `LearningService`/`SubscriptionService` as described in `FAST-API-INSTRUCTIONS.md` do not exist in code yet; they are each owned by their own not-yet-implemented blueprint (A.9 Skill Tree/Mastery Engine, C.24 Subscription & Billing). **Habit tracker (A.7) confirmed real location** (via C.22 B-01's already-written blueprint, which independently confirmed this against A.7's own blueprint set): `src/noorheroes/modules/habits/`, exposing `HabitRepository` (check-in/streak query methods, A.7 B-01–B-03) and `HabitReportAggregator.generate_weekly_report(child_id)` (A.7 B-07, `report_service.py`) — this blueprint's habit-calendar/streak fan-out call should invoke `HabitRepository`'s query methods directly (matching the shape this Dashboard needs), not `HabitReportAggregator`, which returns A.7's own differently-framed weekly-highlights shape. Restriction Engine (C.23) is real in blueprint form only (`Development_Blueprints/C23_Parental_Controls/Backend/`), not yet in `backend/src`. **Conclusion: this sub-feature is being implemented ahead of A.7/A.9/A.11/C.23/C.24's own backend build-out** — its fan-out calls to those services must be written against each service's OWN blueprint-defined contract (confirm the exact method signature in that service's blueprint at implementation time) and must degrade gracefully (per §10 below) if the target service doesn't exist yet in a given environment, rather than hard-failing the whole Dashboard.

## 7. Existing Code to Reuse
- `require_parent_session_only` + `require_parent_gate_verified` (B-01, chained at router-mount level — both already enforced before this handler runs; no redundant per-endpoint check needed here).
- `HabitRepository` (`modules/habits/`, confirmed real per C.22 B-01) for habit-calendar/streak fan-out data.
- `RewardService.get_balance()` / `LearningService.get_child_learning_progress()` / `SubscriptionService.get_entitlement()` — **NOT YET IMPLEMENTED** in `backend/src` as of this blueprint (confirmed via direct filesystem check — see §6); write the fan-out call against each service's own blueprint contract and confirm the exact method signature exists before merging, per Do-Not-Guess.
- `BaseRepository[ModelT].get_by_id()` pattern if a new `DashboardReadModel` repository is needed for cached aggregate storage.
- `ChildRepository.get_child_by_id_and_family()` (`modules/identity/`) for family-ownership validation — confirm this exact method name against `modules/identity/models.py`/`api.py` at implementation time; `identity` is a real, populated module in the codebase (unlike `learning`/`subscriptions`) but this exact method name was not directly verified in this research pass.

## 8. Files to Create
- `src/noorheroes/modules/dashboard/schemas.py` — `DashboardResponse`, `WeeklyReportPreview`, `ActivityTimelineItem`, `ScreenTimeSummary`
- `src/noorheroes/modules/dashboard/service.py` — `DashboardAggregationService(BaseService)`
- `tests/modules/dashboard/test_dashboard_aggregation_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/dashboard/api.py` — add `GET /v1/parent/dashboard` route
- `src/noorheroes/modules/dashboard/deps.py` — add `get_dashboard_aggregation_service()` factory

## 10. Backend Requirements
- Route: `GET /v1/parent/dashboard?child_id=`, dependencies: inherited `require_parent_session_only` (B-01) plus explicit family-ownership check.
- `DashboardAggregationService.get_dashboard(parent_ctx, child_id)`:
  1. Validate `child_id` belongs to `parent_ctx.family_id` via `ChildRepository.get_child_by_id_and_family()`; raise `ChildScopeViolationError` (existing exception, `core/exceptions.py`) if not.
  2. Fan out to Mastery/Learning, Reward, Habit, Restriction, Entitlement services concurrently (`asyncio.gather` with `return_exceptions=True` so one failure doesn't block others — supports per-component graceful degradation).
  3. For a disabled/archived child, still return data but flag `is_read_only: true` and omit any live-action-eligible fields.
  4. For zero-activity, return explicit empty-state shape (not nulls) per component.
  5. Attach `report_as_of` timestamp sourced from the most recent successfully generated weekly report (see B-03/B-04).
- Caching: short-to-medium TTL Redis cache keyed by `(family_id, child_id)`; weekly-report-derived sub-fields cached with a longer TTL than the activity-timeline sub-fields (two cache keys or two TTLs within one cache entry, per architecture team's Redis convention).

## 11. KMP Requirements
Consumed by K-01 (`DashboardRepository.getDashboard(childId)`). Response shape must map cleanly to `DashboardUiState` slices (child switcher, weekly report, timeline, screen-time) so each can be modeled as an independent loading/error slice on the client.

## 12. NextJS Requirements
N/A — no web-portal route exists for this API (FR-12).

## 13. API Contract
- **HTTP Method:** GET
- **Endpoint:** `/v1/parent/dashboard?child_id=`
- **Auth:** Bearer, parent session only (via B-01)
- **Request:** query param `child_id: str` (required)
- **Response 200:**
```json
{
  "child_id": "string",
  "weekly_report_preview": { "headline_insight": "string", "as_of": "ISO-8601", "delayed": false },
  "activity_timeline_preview": [ { "type": "story|habit|lesson|reward", "title": "string", "occurred_at": "ISO-8601" } ],
  "screen_time_summary": { "status_label": "string", "usage_ratio": 0.0 },
  "is_read_only": false,
  "report_as_of": "ISO-8601"
}
```
- **Authentication:** Bearer parent session (B-01 gate)
- **Authorization:** Family-ownership on `child_id`
- **Validation:** `child_id` required, must be a valid identifier owned by the family
- **Error Responses:** `403 CHILD_MODE_TOKEN_REJECTED` (B-01), `403`/`404` for cross-family `child_id` (`ChildScopeViolationError`), `401` for invalid session

## 14. Database Requirements
No new tables for this sub-feature specifically (aggregation is a read-time composition); relies on tables owned by A.7/A.9/A.11/C.23/C.24 and the report tables introduced in B-04.

## 15. Validation
- `child_id` required and must resolve to an active-or-archived child within the authenticated parent's family.
- Reject cross-family `child_id` distinctly from the B-01 child-mode-token rejection (PRD Acceptance Criteria, Edge Case #8 distinction).

## 16. Authentication
Bearer parent session (inherits B-01 router gate).

## 17. Authorization
Family-ownership check on `child_id`, layered on top of B-01's parent-session-only gate — this is an *additional* check, not a replacement.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| `child_id` not in caller's family | `403`/`404` `ChildScopeViolationError` |
| Individual component fetch fails (e.g., Habit service down) | That component returns a graceful "may be unavailable right now" placeholder; other components unaffected |
| Zero activity | Explicit empty-state payload |
| Archived/disabled child selected | Read-only payload, no live-action fields |

## 19. Offline First
N/A server-side; client-side offline caching is K-07's responsibility, consuming this API's response shape.

## 20. Local Data
N/A (backend).

## 21. Localization
Response contains no hardcoded user-facing strings where avoidable — `status_label` and `headline_insight` should be locale-resolved copy keys or pre-localized strings per platform's localization service (`modules/localization/`), consistent with the platform-wide "no unnecessary hardcoded strings" rule.

## 22. RTL
N/A (backend; RTL is a KMP presentation concern).

## 23. Analytics
`parent_dashboard_viewed` is fired client-side on successful load (K-01), not server-side; this API's role is solely to serve the data.

## 24. Performance
- p95 < 600ms from cache (PRD NFR).
- `asyncio.gather` fan-out to avoid serial service calls.
- Redis caching per §10 above.
- Avoid N+1 queries in `ChildRepository` and any per-component data fetch.

## 25. Security
- Family-ownership check prevents cross-family data access (PRD §12.1).
- No new PII surface beyond what underlying domain services already expose.

## 26. Library Requirements
No new dependencies; uses existing `asyncio`, Redis client, SQLAlchemy async session.

## 27. Testing
1. Unit test: successful aggregation for a child with full data across all components.
2. Unit test: cross-family `child_id` rejected.
3. Unit test: one component (e.g., Habit) failing does not block the others (graceful degradation).
4. Unit test: zero-activity child returns explicit empty-state shape.
5. Unit test: archived/disabled child returns `is_read_only: true` with no live-action fields.
6. Integration test: cache hit vs. cache miss timing/behavior.
7. Integration test: full request through B-01 gate + this endpoint.

## 28. Documentation
OpenAPI docstring on the route describing all fields; update dashboard module `README.md`/docstring with the aggregation flow diagram (mirroring PRD §3.2 Mermaid).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Dashboard Response Schemas**
- Task ID: B02-T01
- Objective: Create Pydantic schemas for the aggregated response.
- Why This Is Required: Type-safe, validated API contract.
- Existing Architecture to Follow: Platform's Pydantic v2 camelCase base schema pattern (`common/schemas.py` → `NoorHeroesBaseModel`).
- Existing Files to Reuse: `common/schemas.py` base model.
- Files to Create: `src/noorheroes/modules/dashboard/schemas.py`.
- Files to Modify: none.
- Implementation Details: `DashboardResponse`, `WeeklyReportPreview`, `ActivityTimelineItem`, `ScreenTimeSummary`, all inheriting `NoorHeroesBaseModel`.
- Business Rules: FR-1, FR-7.
- Validation: Field-level types match §13 contract.
- Error Handling: N/A.
- Security: No PII beyond existing exposure.
- Performance: N/A.
- Localization: `headline_insight`/`status_label` typed as pre-localized strings.
- RTL: N/A.
- Analytics: N/A.
- Tests: Schema validation covered implicitly by Task 05 tests.
- Documentation: Docstrings per field.
- Dependencies: none.
- Do Not Change: Existing schemas in other modules.
- Expected Result: Schemas importable.
- Definition of Done: Schemas match §13 contract exactly.

**Task 02 — Implement DashboardAggregationService**
- Task ID: B02-T02
- Objective: Build the composition/fan-out logic.
- Why This Is Required: Core business logic of this sub-feature.
- Existing Architecture to Follow: `BaseService` pattern; `asyncio.gather` fan-out.
- Existing Files to Reuse: `RewardService`, `LearningService`, `SubscriptionService`, `ChildRepository`.
- Files to Create: `src/noorheroes/modules/dashboard/service.py`.
- Files to Modify: none.
- Implementation Details: Per §10 steps 1–5.
- Business Rules: FR-1, FR-2, FR-7, Edge Cases #1–#4, #7.
- Validation: Family-ownership check first.
- Error Handling: Per §18 table.
- Security: `ChildScopeViolationError` enforcement.
- Performance: Concurrent fan-out, cache read-through.
- Localization: Pass through pre-localized copy from source services.
- RTL: N/A.
- Analytics: N/A (client-side).
- Tests: Covered in Task 05.
- Documentation: Docstring citing PRD §3.1/§3.3.
- Dependencies: Task 01, B-01.
- Do Not Change: Do not modify the internals of `RewardService`/`LearningService`/`SubscriptionService` — only consume their public methods.
- Expected Result: Service returns composed `DashboardResponse`.
- Definition of Done: All PRD edge cases #1, #2, #3, #4, #7 handled.

**Task 03 — Implement Redis Caching Layer**
- Task ID: B02-T03
- Objective: Cache-then-refresh with differentiated TTLs.
- Why This Is Required: p95 < 600ms NFR; weekly report data changes weekly, timeline more often.
- Existing Architecture to Follow: `infrastructure/redis.py` `get_redis_pool()`.
- Existing Files to Reuse: Redis pool singleton.
- Files to Create: none.
- Files to Modify: `src/noorheroes/modules/dashboard/service.py`.
- Implementation Details: Cache key `dashboard:{family_id}:{child_id}`; separate TTL for weekly-report sub-object vs. timeline sub-object, or two cache keys composed at read time.
- Business Rules: NFR performance target.
- Validation: N/A.
- Error Handling: Cache miss falls back to live fan-out; cache read failure falls back gracefully to live fetch (never a hard error).
- Security: No sensitive data cached beyond what the API already returns to the authenticated owner.
- Performance: This IS the performance optimization.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 05 (cache hit/miss test).
- Documentation: Comment explaining differentiated TTL rationale.
- Dependencies: Task 02.
- Do Not Change: Do not modify Redis connection credentials/config.
- Expected Result: Cache-then-refresh pattern operational.
- Definition of Done: p95 target achievable under cache-hit conditions.

**Task 04 — Implement Route and Wire Dependencies**
- Task ID: B02-T04
- Objective: Expose `GET /v1/parent/dashboard`.
- Why This Is Required: Public contract delivery.
- Existing Architecture to Follow: Existing router `Depends()` pattern.
- Existing Files to Reuse: `src/noorheroes/modules/dashboard/api.py` (from B-01), `deps.py`.
- Files to Create: none.
- Files to Modify: `api.py`, `deps.py`.
- Implementation Details: `@router.get("", response_model=DashboardResponse)` with `parent_ctx: Annotated[ParentSessionContext, Depends(require_parent_session_only)]`, `child_id: str = Query(...)`, `service: Annotated[DashboardAggregationService, Depends(get_dashboard_aggregation_service)]`.
- Business Rules: FR-1–FR-3.
- Validation: `child_id` required query param.
- Error Handling: Per §18.
- Security: Inherits B-01 gate automatically (router-mounted).
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 05.
- Documentation: OpenAPI summary/description.
- Dependencies: Tasks 01–03, B-01.
- Do Not Change: Do not add a redundant per-endpoint child-mode check (already covered by router-level gate).
- Expected Result: Endpoint live.
- Definition of Done: Matches §13 contract exactly.

**Task 05 — Write Test Suite**
- Task ID: B02-T05
- Objective: Cover all scenarios in §27.
- Why This Is Required: QA §13.2/§13.3/§13.4 requirements.
- Existing Architecture to Follow: pytest + existing async test client fixtures.
- Existing Files to Reuse: Existing fixture factories for family/child/session.
- Files to Create: `tests/modules/dashboard/test_dashboard_aggregation_api.py`.
- Files to Modify: none.
- Implementation Details: 7 test cases per §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert exact error responses.
- Security: Cross-family rejection test is security-critical.
- Performance: Cache timing assertions.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test docstrings.
- Dependencies: Tasks 01–04.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 scenarios covered and green.

## 30. Definition of Done
`GET /v1/parent/dashboard?child_id=` live, gated by B-01, family-ownership validated, all components independently degrading, cached per differentiated TTL, all tests green.

## 31. Final Verification Checklist
- [ ] Family-ownership check independent of and in addition to B-01's token-type check
- [ ] Per-component graceful degradation verified
- [ ] Empty-state and archived/disabled-child variants verified
- [ ] Cache TTL differentiation verified
- [ ] p95 < 600ms achievable under cache-hit load test
- [ ] No hardcoded English strings in response-generating code paths
- [ ] OpenAPI docs reflect full contract
