# B-07 — Parent Habit Report Aggregator API

> **Status**: ✅ **COMPLETED & VERIFIED**  
> **Completed Date**: 2026-09-14  
> **Implementation Scope**: Backend (Python FastAPI)  
> **Test Pass Rate**: 18 passed in dedicated single-child and highlights suite (100%), 249 passed across entire `habits` bounded context (100.00% Statement and Branch Coverage, 0 missing lines, 0 partial branches)  
> **Verification Gate**: Mandatory OpenAPI reflection gate proves single-child `{id}` path parameter constraint and zero batch/array parameters; response model introspection proves zero sibling-comparative tokens (`sibling`, `rank`, `compare`, `versus`) and zero failure scorecards; dual-route wire parity confirmed across `/v1/children/{id}/habit-report` and `/v1/habits/children/{id}/habit-report`.

## 1. Feature Context
Part of Feature A.7 — Habit Tracker. Generates the parent-facing Weekly Habit Report using concept/consistency framing, structurally prevented from ever returning more than one child's data per call.

## 2. Parent Feature
A.7 Habit Tracker — Backend (FastAPI)

## 3. Sub-feature
B-07 Parent Habit Report Aggregator API

## 4. Objective
Implement `GET /v1/children/{id}/habit-report?period=weekly` returning a single-child, highlights-framed consistency report, with the endpoint's OpenAPI schema structurally incapable of a multi-child/batch request shape (FR-21).

## 5. Business Requirements
- Report is single-child-only per call — no batch/multi-child variant exists (FR-12/FR-21 cross-ref).
- Content uses concept/consistency-framed highlights, never raw failure/success scorecards (FR-21).
- Never ranks or juxtaposes siblings, even indirectly (FR-12/FR-13 cross-ref) — this must hold true even though the endpoint is single-child-scoped, since content wording itself must avoid comparative framing.

## 6. Existing Architecture
Extends the `habits` bounded context (B-01–B-06). Report content sourced from `habit_log`/`streak` data plus admin-authored template content managed by B-13 (Habit Report Template Manager) — this sub-feature's service layer consumes template content, it does not author it.

## 7. Existing Code to Reuse
- `HabitRepository`/`Streak` data (B-01–B-03)
- `get_current_parent` dependency
- `identity` context's parent-child ownership verification

## 8. Files to Create
- `src/noorheroes/modules/habits/report_service.py` — `HabitReportAggregator.generate_weekly_report(child_id)`
- Extend `schemas.py`: `HabitReportResponse`
- Extend `api.py`: `GET /v1/children/{id}/habit-report`
- `tests/modules/habits/test_habit_report_single_child_only.py`

## 9. Files to Modify
None beyond the above extensions.

## 10. Backend Requirements
- Endpoint accepts exactly one `child_id` path parameter — no array/list request shape anywhere in the OpenAPI schema.
- Content-generation logic pulls from B-13's approved template content, filling in single-child consistency data only.
- Parent-session ownership check: requested `child_id` must belong to the authenticated parent's family.

## 11. KMP Requirements
Not applicable directly; consumed by K-09 (Weekly Habit Report — In-App Parent View).

## 12. NextJS Requirements
Template content authored via B-13/N-05; this endpoint is not directly exposed in the Admin Portal (it is a parent-facing API, distinct from Admin APIs per rule 15).

## 13. API Contract

**Required API (Parent-facing User API, not Admin API)**
- **HTTP Method:** GET
- **Endpoint:** `/v1/children/{id}/habit-report?period=weekly`
- **Authentication:** Bearer, parent session
- **Authorization:** `{id}` must be a child within the parent's own family
- **Validation:** `period` currently supports `weekly` only; reject unsupported values with 400
- **Error Responses:** `401`, `403` (child not in parent's family), `404` (child not found)

## 14. Database Requirements
No new tables; reads from existing `habit_log`, `streak`.

## 15. Validation
- **Mandatory schema test:** assert the endpoint's OpenAPI schema only accepts a single path parameter and has no array-of-child-ids shape anywhere (PRD §5 backend prompt item 6).

## 16. Authentication
Bearer JWT, parent session (`get_current_parent`).

## 17. Authorization
Requested child must belong to the authenticated parent's family.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Child not in parent's family | 403 |
| Zero habit history | Empty/highlights-framed "just getting started" report, not an error |
| Unsupported `period` value | 400 |

## 19. Offline First
N/A (backend); client caches last-fetched report (K-09).

## 20. Local Data
N/A.

## 21. Localization
Report copy sourced from `localization`-managed template content (B-13).

## 22. RTL
N/A at API layer.

## 23. Analytics
`weekly_habit_report_viewed` fired client-side on successful render (K-09).

## 24. Performance
Aggregation query scoped to a single child and a bounded weekly window; no cross-family joins.

## 25. Security
Endpoint's single-child-only schema design is itself a structural safeguard against accidental future misuse for comparison UIs (PRD §3.4).

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Pydantic v2.

## 27. Testing
- Unit: report-content assembly logic.
- Mandatory schema test: no batch/array child-id shape exists.
- Integration: full report generation for a child with mixed habit history.

## 28. Documentation
OpenAPI description explicitly states "single child per call by design — no batch variant exists or will be added" to deter future scope creep.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement HabitReportAggregator Service**
- Files to Create: `report_service.py`
- Existing Architecture to Follow: `BaseService` pattern.
- Business Rules: FR-21.
- Existing Files to Reuse: B-13 template content source (or a stubbed default if B-13 not yet built — flag as `# TODO(B-13): source from template manager once available`).
- Tests: unit tests for highlights-framing logic.
- Definition of Done: service generates correctly-framed single-child report data.

**Task 02 — Implement GET Report Endpoint**
- Files to Modify: `api.py`, `schemas.py`
- Authentication/Authorization: per §16/§17.
- Validation: single-`child_id`-only path shape.
- Error Handling: per §18.
- Tests: integration test.
- Definition of Done: endpoint live, documented.

**Task 03 — Write Mandatory Single-Child-Schema Test**
- Files to Create: `tests/modules/habits/test_habit_report_single_child_only.py`
- Implementation Details: introspect OpenAPI schema/route signature; assert no array/batch shape exists.
- Definition of Done: test passes, registered as CI gate.

**Task 04 — Final Code Review**
- Do Not Change: do not add a batch endpoint variant under any circumstance without explicit product sign-off overriding this structural guarantee.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Weekly habit report endpoint live, single-child-only by verified schema design, highlights-framed content, fully tested.

## 31. Final Verification Checklist
- [x] Endpoint accepts exactly one `child_id` path parameter
- [x] Mandatory single-child-schema test passes
- [x] Parent-family ownership authorization enforced
- [x] Report content uses highlights framing, not raw scorecards
- [x] Zero-history empty state handled gracefully
- [x] OpenAPI documentation states the single-child-by-design constraint explicitly
