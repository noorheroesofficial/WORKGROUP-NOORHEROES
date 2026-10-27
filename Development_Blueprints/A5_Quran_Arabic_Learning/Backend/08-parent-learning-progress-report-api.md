# B-08 — Parent Quran & Arabic Learning Progress Report API

> **Status:** ✅ **COMPLETED & VERIFIED**  
> **Target Framework:** FastAPI (Python 3.12+) / SQLAlchemy 2.0 (Async) / Pydantic v2 / Redis 7  
> **Architecture Pattern:** Clean Architecture, Modular Monolith, Strict Family-Scoped Domain Verification  
> **Test Coverage:** 47/47 Tests Passing (100% Green in CI)

## 1. Feature Context
Part of Feature A.5 (Quran & Arabic Learning). Gives parents a concept-level view of their child's Quran/Arabic/Tajweed progress and consistency, explicitly avoiding a raw score as the headline.

## 2. Parent Feature
A.5 — Quran & Arabic Learning

## 3. Sub-feature
B-08 — Parent Quran & Arabic Learning Progress Report API (User API — parent)

## 4. Objective
Return a concept-level (mastered/in-progress/needs-refresh) progress summary and consistency trend for a child, structured so no single raw aggregate score is the headline metric.

## 5. Business Requirements
- FR-17: parent-facing Quran/Quiz reports must show concepts/skills, not just a raw numeric score.
- Acceptance Criteria: Parent Quran Progress Report lists mastered/in-progress concepts and consistency trends, not merely a percentage with no context.
- Empty State: zero-activity child → "Once [Child] starts practicing, you'll see their progress here."

## 6. Existing Architecture
Same `learning` bounded context; parent-facing endpoints use `get_current_parent` (returns `ParentSessionContext`) rather than `get_current_child`.

## 7. Existing Code to Reuse
- `SkillNodeStateRepository` (from B-01) for concept-level rollup.
- `LearningAttemptRepository` (from B-03) and `RecitationFeedbackLogRepository` (from B-04) for consistency-trend computation.
- `get_current_parent` dependency.

## 8. Files to Create
- `src/noorheroes/modules/learning/schemas/learning_report.py`
- `src/noorheroes/modules/learning/services/parent_report_aggregator.py`
- `tests/modules/learning/test_parent_report_aggregator.py`
- `tests/modules/learning/test_learning_report_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/learning/api.py` — add `GET /v1/children/{id}/learning-report`.

## 10. Backend Requirements
- **Router**: `GET /v1/children/{id}/learning-report`, `get_current_parent`.
- **Service**: `ParentReportAggregator.build_report(child_id)` — groups `skill_node_state` rows by state into human-readable concept lists (`mastered`, `in_progress` = `learning`+`practicing`, `needs_refresh`), each entry carrying a plain-language label (not a raw node ID), and computes a consistency trend (e.g., practice-days-per-week over a rolling window) from `learning_attempt`/`recitation_feedback_log` timestamps — never a single raw percentage as the headline field.
- **Contract discipline**: response schema must have no top-level numeric "score" field — enforced by a contract test, per FR-17's explicit requirement.

## 11. KMP Requirements
N/A directly; consumed by `K-12 Parent Quran & Arabic Progress Report (In-App)`.

## 12. NextJS Requirements
N/A.

## 13. API Contract

**`GET /v1/children/{id}/learning-report`**
- **Auth:** Bearer (parent session)
- **Response 200:** Concept-level summary (mastered/in-progress/needs-refresh lists with plain-language labels), consistency trend — explicitly structured to avoid a single raw aggregate score as the headline.
- **Authentication:** Bearer JWT, parent-mode
- **Authorization:** `{id}` (child_id) must belong to the authenticated parent's family
- **Validation:** `{id}` must be a valid UUID resolving to an active child in the family
- **Error Responses:** `401`, `403` (child not in caller's family), `404` (unknown child), `500`

## 14. Database Requirements
No new tables — reads existing `skill_node_state`, `learning_attempt`, `recitation_feedback_log` (from B-01/B-03/B-04). Read-only aggregation query, no writes.

## 15. Validation
`{id}` must resolve to an active child belonging to the authenticated parent's family.

## 16. Authentication
Bearer JWT, `get_current_parent`.

## 17. Authorization
Family-scoped child check — reject cross-family access as `403`, consistent with the pattern in B-01/B-02.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Zero activity yet | `200` with empty-but-valid concept lists, framed for the "Once [Child] starts practicing..." empty state client-side |
| Cross-family `{id}` | `403` |
| Unknown child | `404` |
| DB failure | `500`, logged |

## 19. Offline First
N/A (backend).

## 20. Local Data
N/A (backend).

## 21. Localization
Concept plain-language labels resolved via the existing `localization` context in the parent's locale.

## 22. RTL
N/A at API layer.

## 23. Analytics
No server-side event emission; client fires `parent_progress_report_viewed`/`parent_concept_detail_viewed` per K-12.

## 24. Performance
Aggregation query should avoid N+1 across `skill_node_state`/`learning_attempt`; consider a short-TTL cache keyed `learning_report:{child_id}` given this is a read-heavy, infrequently-changing view (target ≥30% weekly parent view rate per PRD success metric).

## 25. Security
Parent-session auth only; no child-session token accepted on this route. No recitation audio or raw confidence scores ever surfaced (only categorical/consistency data, consistent with B-04's zero-retention design).

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0, Pydantic v2. No new dependencies.

## 27. Testing
- Unit: concept-grouping logic (mastered/in-progress/needs-refresh) with plain-language label resolution.
- Unit: consistency-trend computation against known attempt-history input vectors.
- Contract test: response schema asserted to have no top-level numeric "score" field.
- Integration: zero-activity child returns valid empty-state-ready payload.
- Integration: cross-family `{id}` rejected with `403`.

## 28. Documentation
OpenAPI docstring explicitly notes the "no raw score as headline" design constraint per FR-17, so future contributors don't regress it.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create Response Schema**
- Task ID: B-08-T01
- Status: Completed ✅
- Files Created: `src/noorheroes/modules/learning/schemas/learning_report.py` (and `learning_report_schemas.py`).
- Implementation Details: Strict Pydantic v2 schemas (`ConceptProgressItem`, `WeeklyConsistencyItem`, `ConsistencyTrend`, `LearningReportSummary`, `ParentLearningReportResponse`) with `extra="forbid"`, camelCase wire serialization, and zero top-level numeric score fields, per FR-17.
- Dependencies: None.
- Definition of Done: Schema review confirms 100% compliance.

**Task 02 — Implement `ParentReportAggregator`**
- Task ID: B-08-T02
- Status: Completed ✅
- Files Created: `src/noorheroes/modules/learning/services/parent_report_aggregator.py`.
- Existing Files Reused: B-01's `SkillNodeStateRepository`, B-03's `LearningAttemptRepository`, B-04's `RecitationFeedbackLogRepository`.
- Implementation Details: Single-query joined concept grouping, 4-week practice consistency trend calculation, same-day activity collapse, active streak preservation, culturally localized anonymous child name fallback (`PARENT_LEARNING_REPORT_DEFAULT_CHILD`), localized empty state (`en`, `hi`, `ur`, `ar`), and 60s Redis edge caching (`learning_report:{child_id}:{locale}`) with outage degradation.
- Dependencies: B-08-T01, B-01-T04, B-03-T03, B-04-T01.
- Definition of Done: Unit tests (Task 04) pass (23/23 tests passing).

**Task 03 — Wire Router with Parent Auth**
- Task ID: B-08-T03
- Status: Completed ✅
- Files Modified: `src/noorheroes/modules/learning/api.py`, `src/noorheroes/api/v1/router.py`.
- Implementation Details: Mounted canonical `GET /v1/children/{id}/learning-report` and module parity alias `GET /v1/learning/children/{id}/learning-report`, guarded with `get_current_parent` and family-scoping check.
- Dependencies: B-08-T02.
- Definition of Done: Endpoints live, cross-family test passes, 100% wire parity.

**Task 04 — Tests**
- Task ID: B-08-T04
- Status: Completed ✅
- Objective: Full coverage per §27, including schema contract tests, boundary tests, localization headers, and outage resilience.
- Dependencies: B-08-T01–T03.
- Definition of Done: All 47 dedicated tests green in CI (23 aggregator + 24 API tests).

**Task 05 — API Documentation**
- Task ID: B-08-T05
- Status: Completed ✅
- Dependencies: B-08-T03.
- Definition of Done: OpenAPI docs complete covering 8 status codes (200, 400, 401, 403, 404, 422, 429, 500), FR-17 constraint documented across `FAST-API-INSTRUCTIONS.md`, `MASTER-README.md`, and `learning/README.md`.

## 30. Definition of Done
✅ **FULLY ACHIEVED**: Endpoints live, concept-level report with no headline raw score, correct empty-state and cross-family handling, fully tested (47 dedicated tests) and authoritative documentation synchronized.

## 31. Final Verification Checklist
- [x] Response has no top-level numeric "score" field (contract test enforced)
- [x] Mastered/in-progress/needs-refresh lists use plain-language labels, not raw node IDs
- [x] Consistency trend reflects practice frequency, not just app-open counts
- [x] Zero-activity child returns a valid, empty-state-ready payload
- [x] Cross-family `{id}` access rejected with `403`
- [x] No recitation audio, transcript, or raw confidence data ever surfaced
- [x] Full test suite green in CI
