# B-07 — Admin Fact Engagement Monitoring API

## 1. Feature Context
Part of Feature B.18 (Islamic Facts Module). Read-only aggregated analytics surface for editorial content-quality decisions — not a mutation API.

## 2. Parent Feature
B.18 — Islamic Facts Module

## 3. Sub-feature
1.7 Admin Fact Engagement Monitoring API (ID: B-07) — **Admin API**

## 4. Objective
Implement `GET /v1/admin/facts/engagement` returning aggregated view/quiz-engagement rates per fact and per topic, sourced from the Analytics Event Bus, to inform editorial catalog-completeness and content-quality decisions.

## 5. Business Requirements
- §8 Admin Requirements: Fact Engagement Monitor (read-only), aggregate view of fact-view/quiz-engagement rates per fact/topic.
- §11.3 Dashboard Metrics: per-topic engagement rate, AI-fallback-used rate, scholar-approval-revocation frequency.

## 6. Existing Architecture
Read-only aggregation service within `content` bounded context, querying pre-aggregated analytics data (existing Analytics Event Bus / warehouse read-model, confirm exact existing aggregation infrastructure before assuming a new one is needed — likely the same pattern used by other admin engagement dashboards in the platform).

## 7. Existing Code to Reuse
- Existing analytics aggregation/read-model pattern used by other admin engagement dashboards (confirm exact table/service before building a new aggregation pipeline).
- `core/deps.py` → `get_current_admin`, `require_admin_scope("content_editor")`.

## 8. Files to Create
- `src/noorheroes/modules/content/api/admin_fact_analytics_router.py` — `GET /v1/admin/facts/engagement`.
- `src/noorheroes/modules/content/services/fact_engagement_service.py`.
- `tests/modules/content/test_fact_engagement_monitoring.py`.

## 9. Files to Modify
- `src/noorheroes/api/router.py` — register route.

## 10. Backend Requirements
- `GET /v1/admin/facts/engagement?topic=&date_from=&date_to=&page=&page_size=`, role `content_editor` (read-only).
- Returns per-fact and per-topic aggregates: view rate, quiz-engagement rate, computed from existing analytics event data (`fact_of_day_shown`, `fact_card_tapped`, `fact_detail_viewed`, `fact_quiz_started`, `fact_quiz_completed`).
- Supports date-range filtering and pagination for large catalogs.
- Cached with a short TTL (aggregate data does not need real-time freshness).

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
Consumed by N-05 (Fact Engagement Monitor Dashboard).

## 13. API Contract
**Endpoint:** `GET /v1/admin/facts/engagement`
**Auth:** Bearer, admin (`content_editor` scope, read-only)
**Query Params:** `topic` (optional), `date_from`, `date_to`, `page`, `page_size`
**Response 200:**
```json
{
  "items": [ { "fact_id": "...", "topic": "...", "view_rate": 0.52, "quiz_engagement_rate": 0.35 } ],
  "page": 1, "page_size": 20, "total_count": 134
}
```
**Error Responses:** `403` (wrong role), `422` (invalid date range).

## 14. Database Requirements
Read-only queries against the existing analytics read-model/warehouse; no new write tables owned by this sub-feature (aggregation only).

## 15. Validation
`date_from <= date_to`; `page_size` capped at a reasonable max (e.g., 100) to prevent unbounded queries.

## 16. Authentication
`Depends(get_current_admin)`.

## 17. Authorization
`require_admin_scope("content_editor")`, read-only — no mutation capability on this endpoint.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Wrong role | `403` |
| Invalid date range | `422` |
| Analytics backend unavailable | `503` with friendly error, or cached last-known aggregate if available |

## 19-22. Offline/Local Data/Localization/RTL
N/A — admin read-only dashboard endpoint.

## 23. Analytics
This endpoint itself is a consumer of analytics data, not an emitter.

## 24. Performance
Cached aggregate query (short TTL); pagination prevents unbounded result sets for large catalogs.

## 25. Security
Read-only; no mutation risk. Standard admin RBAC.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 — existing platform dependencies.

## 27. Testing
- Unit: date-range validation.
- Unit: pagination correctness.
- Integration: aggregate values match expected computation from fixture event data.

## 28. Documentation
OpenAPI docstring documenting the read-only nature and source event types.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm Existing Analytics Read-Model**
Objective: Identify the platform's existing aggregation infrastructure for admin engagement dashboards.
Dependencies: None.
Definition of Done: Confirmed data source, avoiding a duplicate aggregation pipeline.

**Task 02 — Implement Aggregation Service**
Files to Create: `services/fact_engagement_service.py`.
Dependencies: Task 01.
Definition of Done: Correct per-fact/per-topic aggregates computed.

**Task 03 — Implement Endpoint**
Files to Create: `api/admin_fact_analytics_router.py`.
Dependencies: Task 02.
Definition of Done: Passes Task 04 tests.

**Task 04 — Tests**
Dependencies: Task 03.
Definition of Done: All green.

**Task 05 — Documentation**
Dependencies: Task 04.
Definition of Done: OpenAPI docs accurate.

## 30. Definition of Done
Read-only aggregation endpoint functioning, cached, paginated, tested, documented.

## 31. Final Verification Checklist
- [ ] Read-only, no mutation path
- [ ] Pagination and date-range validation correct
- [ ] Aggregates verified against fixture data
- [ ] No duplicate analytics-aggregation pipeline built
- [ ] Documentation updated
