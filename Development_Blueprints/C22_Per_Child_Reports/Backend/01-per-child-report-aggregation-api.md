# Blueprint: Per-Child Report Aggregation API

## 1. Feature Context
Platform: NoorHeroes Backend (FastAPI). Module: `src/noorheroes/modules/dashboard/` (extended from C.20, not duplicated). This blueprint delivers the primary read endpoint for the full-depth Per-Child Report screen: `GET /v1/parent/reports/{child_id}?from=&to=`.

## 2. Parent Feature
C.22 — Per-Child Reports.

## 3. Sub-feature
B-01 — Per-Child Report Aggregation API.

## 4. Objective
Compose a single, date-range-consistent aggregated read model — weekly trend chart, habit calendar, skill mastery summary, AI interaction summary — for the full Per-Child Report screen, reusing C.20's Parent-Session-Only Gate and family-ownership pattern, extending (not forking) the Dashboard Aggregation Service.

## 5. Business Requirements
Source: PRD C.22 §1.7 FR-1, FR-3, FR-4, FR-7, FR-9, FR-14, §1.9 Acceptance Criteria, §1.10 Edge Case #1, §3.1, §3.4, §3.5.
- Components: weekly trend chart, habit calendar, skill mastery summary, AI interaction summary, `report_as_of` freshness label.
- A single `from`/`to` date range applies consistently across every component — never per-component independent filtering (FR-14).
- Delayed-analytics and no-activity states shown explicitly, never a blank/broken chart (FR-4).
- A date range spanning before the child's account existed shows "no activity" only for the valid portion, with the account-start boundary communicated (Edge Case 1).
- Content tone: trend language and recommendations, never judgmental grades (FR-7, shared with C.20).

## 6. Existing Architecture
Per `FAST-API-INSTRUCTIONS.md`: Router → Service → Repository layering; `BaseService`/`BaseRepository` generics; Redis via `infrastructure/redis.py`. Per C.20 Blueprint B-02 (`02-dashboard-aggregation-api.md`): `DashboardAggregationService` already fans out to `RewardService`, `LearningService` (mastery/quiz progress), `SubscriptionService` (entitlement) via `asyncio.gather(return_exceptions=True)`, keyed by `(family_id, child_id)` Redis cache with differentiated TTLs. This blueprint extends that same service class with the deeper report shape rather than creating a parallel aggregation path. Habit tracker (A.7) and AI Safety Event Store (B-03 of this feature) services are additional fan-out targets.

## 7. Existing Code to Reuse
- `require_parent_session_only` (C.20 B-01, `modules/dashboard/deps.py`) — router-level gate, do not reimplement.
- `ChildRepository.get_child_by_id_and_family()` (`modules/identity/`) — family-ownership validation.
- `DashboardAggregationService` (C.20 B-02, `modules/dashboard/service.py`) — extend with a new `get_per_child_report(parent_ctx, child_id, date_from, date_to)` method; do not duplicate the fan-out/cache pattern.
- `LearningService.get_child_learning_progress()`, `RewardService.get_balance()` — reused for trend chart/skill summary inputs.
- `ChildScopeViolationError` (`core/exceptions.py`).
- Habit tracker service (A.7) — confirmed against A.7's own blueprint set: lives in the `habits` bounded context (`src/noorheroes/modules/habits/`), exposing `HabitRepository`/`Streak` data (A.7 B-01–B-03) and `HabitReportAggregator.generate_weekly_report(child_id)` (A.7 B-07, `report_service.py`). This blueprint's habit-calendar fan-out call should invoke `HabitRepository`'s check-in/streak query methods directly (day-by-day calendar shape) rather than `HabitReportAggregator`, which returns A.7's own highlights-framed weekly report shape — the two serve different response shapes for the same underlying data.

## 8. Files to Create
- `tests/modules/dashboard/test_per_child_report_aggregation_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/dashboard/schemas.py` — add `PerChildReportResponse`, `TrendChartData`, `HabitCalendarData`, `SkillMasterySummaryItem`, `AiInteractionSummary`
- `src/noorheroes/modules/dashboard/service.py` — add `get_per_child_report()` to `DashboardAggregationService`
- `src/noorheroes/modules/dashboard/api.py` — add `GET /v1/parent/reports/{child_id}` route
- `src/noorheroes/modules/dashboard/deps.py` — no new factory needed; reuse `get_dashboard_aggregation_service()`

## 10. Backend Requirements
- Route: `GET /v1/parent/reports/{child_id}?from=&to=`, dependencies: `require_parent_session_only` (C.20 B-01) plus explicit family-ownership check.
- `DashboardAggregationService.get_per_child_report(parent_ctx, child_id, date_from, date_to)`:
  1. Validate `child_id` belongs to `parent_ctx.family_id`; raise `ChildScopeViolationError` if not.
  2. Resolve the effective query range: if `date_from` precedes the child's `created_at`, clamp the effective range to `created_at..date_to` and set `range_clamped_at_account_start: true` in the response (Edge Case 1) rather than erroring on the impossible pre-existence portion.
  3. Fan out concurrently (`asyncio.gather(return_exceptions=True)`) to: `LearningService` (trend chart + skill mastery summary), habit tracker service (habit calendar), AI Safety Event Store repository (B-03, AI interaction summary).
  4. Apply the resolved `(date_from, date_to)` range identically to every fan-out call — a single range object passed to all four calls, never four independently-derived ranges.
  5. For zero activity in range, each affected component returns its explicit empty-state shape (not null).
  6. Attach `report_as_of` from the most recent successfully generated weekly report (C.20 B-04 pattern) to signal delayed-analytics framing when applicable.
- Caching: Redis key `per_child_report:{family_id}:{child_id}:{date_from}:{date_to}`, short-to-medium TTL, distinct from C.20's dashboard-preview cache key (different granularity of data).

## 11. KMP Requirements
Consumed by K-01 (`ReportRepository.getReport(childId, from, to)`). Response shape must map to independent `ComponentState` slices per component (trend chart, habit calendar, skill mastery, AI interaction summary) so the client models each as an independently-resolving loading/content/error/empty slice, matching the single-range-applied-to-all-components contract.

## 12. NextJS Requirements
N/A — no Admin Portal route consumes this endpoint (PRD §2.3: Per-Child Report is parent-app-only).

## 13. API Contract
- **HTTP Method:** GET
- **Endpoint:** `/v1/parent/reports/{child_id}?from=&to=`
- **Auth:** Bearer, parent session only (C.20 B-01 gate)
- **Request:** path `child_id: str` (required); query `from: date` (required), `to: date` (required)
- **Response 200:**
```json
{
  "child_id": "string",
  "range_clamped_at_account_start": false,
  "trend_chart": { "points": [ { "date": "ISO-8601", "value": 0 } ], "empty": false },
  "habit_calendar": { "days": [ { "date": "ISO-8601", "status": "checked_in|missed|no_data" } ], "empty": false },
  "skill_mastery_summary": [ { "skill_id": "string", "state": "practicing", "state_label": "string" } ],
  "ai_interaction_summary": { "concerning_count": 0, "total_count": 0, "empty": false },
  "report_as_of": "ISO-8601"
}
```
- **Authentication:** Bearer parent session (B-01 gate)
- **Authorization:** Family-ownership on `child_id`
- **Validation:** `from`/`to` required and well-formed; `from` clamped to `created_at` rather than rejected
- **Error Responses:** `403 CHILD_MODE_TOKEN_REJECTED` (B-01), `403`/`404` `ChildScopeViolationError` for cross-family `child_id`, `401` invalid session, `422` malformed date range

## 14. Database Requirements
No new tables specific to this endpoint; reads from A.7 (habit), A.9 (mastery, via `skill_report_snapshot` introduced in B-02 of this feature), A.11 (reward), and `ai_safety_event` (B-03 of this feature). Relies on `weekly_report` (C.20 §4.1) for `report_as_of`.

## 15. Validation
- `child_id` required, must resolve within the authenticated parent's family.
- `from`/`to` required, `from <= to`.
- `from` earlier than child `created_at` is clamped, not rejected (Edge Case 1).

## 16. Authentication
Bearer parent session (inherits C.20 B-01 router gate).

## 17. Authorization
Family-ownership check on `child_id`, additive to B-01's gate, mirroring C.20 B-02's pattern exactly.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| `child_id` not in caller's family | `403`/`404` `ChildScopeViolationError` |
| One component's upstream service fails | That component returns a graceful unavailable placeholder; others unaffected |
| Zero activity in range | Explicit empty-state payload per affected component |
| `from` precedes account creation | Range clamped to `created_at..to`, `range_clamped_at_account_start: true` |
| Report generation delayed | `report_as_of` reflects last successful generation, not current time |

## 19. Offline First
N/A server-side; client-side caching is K-09's responsibility, consuming this response shape.

## 20. Local Data
N/A (backend).

## 21. Localization
`state_label` and any status copy are locale-resolved via `modules/localization/`, never hardcoded English.

## 22. RTL
N/A (backend; RTL is a KMP presentation concern).

## 23. Analytics
`per_child_report_viewed` / `report_date_range_filtered` fired client-side (K-01), not server-side.

## 24. Performance
- p95 < 700ms from cache (PRD NFR).
- `asyncio.gather` fan-out, no serial service calls.
- Redis caching per §10.
- Avoid N+1 queries in habit-calendar and skill-mastery-summary fan-out calls.

## 25. Security
- Family-ownership check prevents cross-family data access.
- AI interaction summary counts only, no raw content surfaced at this aggregation layer (detail sourced from B-03's structurally redacted store).

## 26. Library Requirements
No new dependencies; uses existing `asyncio`, Redis client, SQLAlchemy async session.

## 27. Testing
1. Unit test: successful aggregation for a child with full data across all four components.
2. Unit test: cross-family `child_id` rejected.
3. Unit test: one component (e.g., habit service) failing does not block the others.
4. Unit test: zero-activity child returns explicit empty-state shape per component.
5. Unit test: `from` before `created_at` clamps range and sets `range_clamped_at_account_start: true`.
6. Unit test: identical `(from, to)` applied to all four fan-out calls (no component receives a different range).
7. Integration test: cache hit vs. cache miss timing.
8. Integration test: full request through B-01 gate + this endpoint.

## 28. Documentation
OpenAPI docstring describing all fields including `range_clamped_at_account_start`; update `modules/dashboard/README.md` with the extended aggregation flow (mirroring PRD §3.2 Mermaid).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Per-Child Report Response Schemas**
- Task ID: B01-T01
- Objective: Create Pydantic schemas for the aggregated response.
- Why This Is Required: Type-safe, validated API contract distinct from C.20's lighter dashboard-preview shape.
- Existing Architecture to Follow: `NoorHeroesBaseModel` (`common/schemas.py`).
- Existing Files to Reuse: `common/schemas.py`.
- Files to Create: none.
- Files to Modify: `src/noorheroes/modules/dashboard/schemas.py`.
- Implementation Details: `PerChildReportResponse`, `TrendChartData`, `HabitCalendarData`, `SkillMasterySummaryItem`, `AiInteractionSummary`.
- Business Rules: FR-1, FR-4, FR-14.
- Validation: Fields match §13 contract exactly.
- Error Handling: N/A.
- Security: No raw AI content field in `AiInteractionSummary`.
- Performance: N/A.
- Localization: `state_label`/status fields typed as pre-localized strings.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered by Task 05.
- Documentation: Field-level docstrings.
- Dependencies: none.
- Do Not Change: C.20's existing `DashboardResponse` schema.
- Expected Result: Schemas importable.
- Definition of Done: Matches §13 contract exactly.

**Task 02 — Extend DashboardAggregationService with get_per_child_report**
- Task ID: B01-T02
- Objective: Build the range-resolution, fan-out, and clamping logic.
- Why This Is Required: Core business logic distinguishing this endpoint from C.20's preview.
- Existing Architecture to Follow: `asyncio.gather(return_exceptions=True)` fan-out pattern from C.20 B-02.
- Existing Files to Reuse: `LearningService`, habit tracker service, `ChildRepository`.
- Files to Create: none.
- Files to Modify: `src/noorheroes/modules/dashboard/service.py`.
- Implementation Details: Per §10 steps 1–6.
- Business Rules: FR-1, FR-4, FR-14, Edge Case #1.
- Validation: Family-ownership check first; range clamp logic second.
- Error Handling: Per §18.
- Security: `ChildScopeViolationError` enforcement.
- Performance: Concurrent fan-out, single range object shared across calls.
- Localization: Pass through pre-localized copy from source services.
- RTL: N/A.
- Analytics: N/A (client-side).
- Tests: Covered in Task 05.
- Documentation: Docstring citing PRD §3.1/§3.3/FR-14.
- Dependencies: Task 01, C.20 B-01/B-02.
- Do Not Change: Do not modify `RewardService`/`LearningService` internals — consume public methods only.
- Expected Result: Service returns a composed, range-consistent `PerChildReportResponse`.
- Definition of Done: Edge Case #1 and FR-14 both verifiably enforced.

**Task 03 — Implement Redis Caching Layer**
- Task ID: B01-T03
- Objective: Cache-then-refresh keyed by `(family_id, child_id, date_from, date_to)`.
- Why This Is Required: p95 < 700ms NFR under repeated date-range views.
- Existing Architecture to Follow: `infrastructure/redis.py` pool singleton, C.20 B-02's TTL-differentiation convention.
- Existing Files to Reuse: Redis pool singleton.
- Files to Create: none.
- Files to Modify: `src/noorheroes/modules/dashboard/service.py`.
- Implementation Details: Cache key includes the resolved (post-clamp) range, not the raw requested range, so clamped and unclamped requests for the same effective window share a cache entry.
- Business Rules: NFR performance target.
- Validation: N/A.
- Error Handling: Cache read/write failure falls back gracefully to live fetch.
- Security: No sensitive data cached beyond what the authenticated owner already receives.
- Performance: This IS the optimization.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 05.
- Documentation: Comment explaining cache-key resolution-order rationale.
- Dependencies: Task 02.
- Do Not Change: Redis connection credentials/config.
- Expected Result: Cache-then-refresh operational.
- Definition of Done: p95 target achievable under cache-hit conditions.

**Task 04 — Implement Route and Wire Dependencies**
- Task ID: B01-T04
- Objective: Expose `GET /v1/parent/reports/{child_id}`.
- Why This Is Required: Public contract delivery.
- Existing Architecture to Follow: Existing router `Depends()` pattern from C.20 B-02.
- Existing Files to Reuse: `modules/dashboard/api.py`, `deps.py`.
- Files to Create: none.
- Files to Modify: `api.py`.
- Implementation Details: `@router.get("/reports/{child_id}", response_model=PerChildReportResponse)` with `parent_ctx: Annotated[ParentSessionContext, Depends(require_parent_session_only)]`, `date_from: date = Query(..., alias="from")`, `date_to: date = Query(..., alias="to")`.
- Business Rules: FR-1, FR-3, FR-14.
- Validation: Query params required; `from <= to`.
- Error Handling: Per §18.
- Security: Inherits B-01 gate automatically.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 05.
- Documentation: OpenAPI summary/description.
- Dependencies: Tasks 01–03.
- Do Not Change: Do not add a redundant per-endpoint child-mode check.
- Expected Result: Endpoint live.
- Definition of Done: Matches §13 contract exactly.

**Task 05 — Write Test Suite**
- Task ID: B01-T05
- Objective: Cover all scenarios in §27.
- Why This Is Required: QA coverage for the aggregation contract and Edge Case #1.
- Existing Architecture to Follow: pytest + existing async test client fixtures.
- Existing Files to Reuse: Existing family/child/session fixture factories.
- Files to Create: `tests/modules/dashboard/test_per_child_report_aggregation_api.py`.
- Files to Modify: none.
- Implementation Details: 8 test cases per §27.
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
- Definition of Done: 100% of §27 scenarios green.

## 30. Definition of Done
`GET /v1/parent/reports/{child_id}?from=&to=` live, gated by C.20 B-01, family-ownership validated, single date range applied identically across all four components, account-start clamping verified, cached per differentiated key, all tests green.

## 31. Final Verification Checklist
- [ ] Family-ownership check independent of and additive to B-01's token-type check
- [ ] Single `(from, to)` range verifiably applied to all four fan-out calls (FR-14)
- [ ] Account-start clamping verified (Edge Case #1)
- [ ] Per-component graceful degradation verified
- [ ] Empty-state variants verified for each component
- [ ] Cache key includes resolved (post-clamp) range
- [ ] p95 < 700ms achievable under cache-hit load test
- [ ] No hardcoded English strings in response-generating code paths
- [ ] OpenAPI docs reflect full contract
