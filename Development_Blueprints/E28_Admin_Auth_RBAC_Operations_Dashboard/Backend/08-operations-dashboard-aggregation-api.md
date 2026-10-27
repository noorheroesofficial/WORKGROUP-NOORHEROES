# B-08 — Operations Dashboard Aggregation API

## 1. Feature Context
Part of E.28. The landing surface every admin sees: eight canonical widgets composed from every domain service plus the engineering observability stack, fed by the same operational signals engineers see — no separate, disconnected "engineering-only" monitoring view (FR-7, FR-8).

## 2. Parent Feature
E.28 — Admin Portal: Authentication, RBAC & Operations Dashboard

## 3. Sub-feature
B-08 — Operations Dashboard Aggregation API

## 4. Objective
Implement `GET /v1/admin/dashboard` composing all 8 canonical widgets via independently-fallible parallel sub-queries, so that one widget's data-source failure never blocks the others, each failed widget explicitly flagged `data_unavailable=true` (FR-7, FR-8, Edge Case 5, §5 Backend AI prompt item 6).

## 5. Business Requirements
- FR-7: eight canonical widgets — active families/children; learning/story completion; content awaiting review; safety/moderation alerts; subscription health/webhook failures; notification performance; AI refusal/escalation rates; failed jobs/incidents.
- FR-8: same operational signals engineers see, appropriately role-scoped — no disconnected engineering-only view.
- FR-10: SLOs/alerting for auth, home feed, progress sync, media startup, receipt validation, content publication — surfaced in the service-health widget.
- FR-11: runbooks linked for OTP provider outage, store webhook delay, CDN issue, harmful AI response, data breach, accidental content publication.
- Edge Case 5: monitoring data source outage → explicit "monitoring data temporarily unavailable" state per affected widget, never silently stale or hidden.
- Success Metric: incident-detection-to-admin-visibility latency ≤ 2 minutes.

## 6. Existing Architecture
This is the most cross-cutting sub-feature in E.28 — it reads from every domain service (`identity`, `content`, `learning`, `subscriptions`, `notifications`, `ai_safety`, plus Celery job status and the engineering observability/monitoring stack) without owning any of that data itself. Depends on B-03 (role-scoped widget visibility) and, for freshness, Redis caching.

Per FastAPI instructions §5, the relevant existing services this widget composition reads from (read-only, no new write paths into any of them):
- `identity` (`FamilyAccount`, `ChildProfile` counts) → active families/children widget
- `learning` (`QuizAttempt`, `LearningProgress`) → learning/story completion widget
- `content` (`ContentItem` review-status) → content awaiting review widget
- `ai_safety` (`SafetyAuditLog`) → AI refusal/escalation rates widget
- `subscriptions` (`SubscriptionPlan`, entitlement/webhook state) → subscription health widget
- `notifications` (dispatch success/failure) → notification performance widget
- Celery/`outbox_relay` job status + engineering observability stack → failed jobs/incidents and service health widgets

## 7. Existing Code to Reuse
| Component | Location | Reuse For |
|---|---|---|
| `get_redis_pool()` | `infrastructure/redis.py` | Dashboard response caching (near-real-time, not per-request recompute) |
| Domain repositories (`ChildRepository`, `QuizAttemptRepository`, `ContentRepository`, `SafetyAuditRepository`, `SubscriptionRepository`, `NotificationRepository`) | respective `modules/*/repository.py` | Read-only aggregate queries per widget |
| `require_admin_permission` | B-03 | Role-scoped widget visibility |
| `retry_with_backoff` | `common/utils/retry.py` | Optional resilience wrapper around the engineering-observability-stack call, not for masking genuine failures |

## 8. Files to Create
- `src/noorheroes/modules/admin/dashboard/schemas.py` — `DashboardResponse`, one schema per widget (`ActiveFamiliesWidget`, `LearningCompletionWidget`, `ContentReviewWidget`, `SafetyAlertsWidget`, `SubscriptionHealthWidget`, `NotificationPerformanceWidget`, `AIRefusalWidget`, `FailedJobsWidget`), each with a `data_unavailable: bool` field
- `src/noorheroes/modules/admin/dashboard/service.py` — `DashboardAggregationService`
- `src/noorheroes/modules/admin/dashboard/api.py` — `GET /v1/admin/dashboard`
- `tests/modules/admin/dashboard/test_dashboard_aggregation.py`
- `tests/modules/admin/dashboard/test_widget_independent_failure.py`

## 9. Files to Modify
None outside this new submodule — read-only cross-context queries only, no existing module's write path touched.

## 10. Backend Requirements
- **`GET /v1/admin/dashboard`:** composes the 8 widget payloads via `asyncio.gather(..., return_exceptions=True)` (or equivalent structured-concurrency pattern) so each sub-query is independently fallible; a failed sub-query is caught and converted to `{ "data_unavailable": true }` for that widget only, never raised to fail the whole response.
- **Role scoping (FR-8):** widget-level detail may be filtered/redacted per requesting admin's role (e.g., a Support Agent might see aggregate counts but not drill-down detail a Super Admin sees) — resolved via B-03's permission matrix.
- **Runbook linking (FR-11):** the incident/service-health widget payload includes a `runbook_url` field per known incident type where a runbook exists (OTP provider outage, store webhook delay, CDN issue, harmful AI response, data breach, accidental content publication) — sourced from a static, versioned runbook registry (a simple config/lookup table, not a new CMS).
- **Freshness (§1.4 target ≤2min):** cache dashboard composite in Redis with a short TTL (e.g., 60–90s) refreshed on read-through, balancing near-real-time freshness against the cost of re-querying 8 domains on every single dashboard view.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
Consumed by `N-03 — Operations Dashboard Widgets`.

## 13. API Contract
### `GET /v1/admin/dashboard`
- **Auth:** `get_current_admin`
- **Authorization:** role-scoped widget visibility/detail (B-03)
- **Response 200:**
```json
{
  "active_families": { "count": 12034, "data_unavailable": false },
  "learning_completion": { "completion_rate": 0.62, "data_unavailable": false },
  "content_awaiting_review": { "count": 14, "data_unavailable": false },
  "safety_alerts": { "open_count": 2, "data_unavailable": false },
  "subscription_health": { "webhook_failure_rate": 0.001, "data_unavailable": false },
  "notification_performance": { "delivery_rate": 0.98, "data_unavailable": false },
  "ai_refusal_rate": { "rate": 0.03, "data_unavailable": true },
  "failed_jobs": { "incidents": [ { "id": "...", "type": "otp_provider_outage", "runbook_url": "..." } ], "data_unavailable": false }
}
```
- **Error Responses:** `401`, `403` (though most role-scoping manifests as reduced widget detail, not a blanket 403, per FR-8's "same signals, appropriately role-scoped" philosophy)

## 14. Database Requirements
Read-only aggregate queries across existing domain tables; no new write tables beyond an optional static runbook-registry lookup table if not implemented as static config.

## 15. Validation
N/A (GET, no request body beyond optional query params for widget-specific filters, e.g., date range for completion rate).

## 16. Authentication
Delegated to B-01/B-02.

## 17. Authorization
Role-scoped detail per widget (B-03); the endpoint itself is reachable by any authenticated admin, with each widget's payload shape adjusted per role.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| One widget's underlying data source fails | That widget flagged `data_unavailable=true`; other 7 widgets return normally |
| Entire monitoring/observability stack outage | All engineering-sourced widgets (service health, job failures) flagged `data_unavailable=true`; domain-sourced widgets (families, completion, etc.) unaffected since they query different systems |
| Zero active incidents | Calm "All systems normal" — represented as an empty `incidents` array, not an error or missing field |

## 19. Offline First
N/A (server-side aggregation endpoint).

## 20. Local Data
N/A.

## 21. Localization
Widget labels/incident-type display text localized client-side; backend returns stable identifiers/codes.

## 22. RTL
N/A at backend layer.

## 23. Analytics
Supports `operations_dashboard_viewed`, `incident_viewed`, `service_health_viewed`, `job_failure_viewed` (client-fired).

## 24. Performance
- Parallel, independently-fallible sub-queries (`asyncio.gather` with `return_exceptions=True`) — this is the core performance/resilience requirement, not merely a nice-to-have.
- Redis-cached composite response with short TTL to meet the ≤2-minute freshness target without re-querying 8 systems on every page load.
- Avoid N+1 queries within each individual widget's own aggregation logic (use existing repository aggregate methods, add new ones if a repository lacks a needed count/aggregate query).

## 25. Security
No new sensitive data exposure beyond what each source domain already permits for the requesting admin's role — B-08 must not widen access beyond what B-03's permission matrix already grants for each underlying resource; it composes, does not elevate.

## 26. Library Requirements
No new libraries — `asyncio.gather` is stdlib.

## 27. Testing
- Unit: each widget's individual aggregation query.
- **Signature test (mandatory):** simulate a failure in one widget's underlying data source and confirm the other 7 widgets still return successfully with the failed one flagged `data_unavailable=true`, never blocking the whole response (§5 Backend AI prompt item 6).
- Integration: full dashboard fetch, role-scoped detail variation across at least two different fixture roles.
- Load/latency test: confirm response time supports the ≤2-minute freshness target under the caching strategy.

## 28. Documentation
OpenAPI schema for the dashboard endpoint including all 8 widget shapes; internal doc listing each widget's underlying data source and the runbook registry.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Widget Response Schemas**
- Task ID: B-08-T01
- Objective: Pydantic schemas for all 8 widgets, each including `data_unavailable: bool`.
- Files to Create: `dashboard/schemas.py`.
- Definition of Done: Schemas compile; `data_unavailable` present on every widget type.

**Task 02 — Implement Per-Widget Aggregation Queries**
- Task ID: B-08-T02
- Objective: One aggregation method per widget, each reading from its respective existing repository.
- Files to Create: `dashboard/service.py` (individual private methods, e.g., `_get_active_families()`, `_get_learning_completion()`, etc.).
- Implementation Details: Reuse existing repositories (§6); add new aggregate-count methods to those repositories only if a needed query doesn't already exist (mark any such repository extension explicitly in the PR).
- Performance: Each method must be independently awaitable and independently fallible.
- Dependencies: None beyond existing domain repositories.
- Definition of Done: Each widget method unit-tested in isolation.

**Task 03 — Implement Parallel, Independently-Fallible Composition**
- Task ID: B-08-T03
- Objective: `DashboardAggregationService.get_dashboard()` composing all 8 via `asyncio.gather(..., return_exceptions=True)`.
- Implementation Details: Catch each widget's exception individually, convert to `data_unavailable=true` for that widget only.
- Security/Reliability: This is the feature's core resilience guarantee.
- Tests: **Signature test** — simulate one widget's failure, confirm other 7 succeed (§5 item 6).
- Dependencies: Task 02.
- Definition of Done: Signature test passes.

**Task 04 — Implement Role-Scoped Widget Detail**
- Task ID: B-08-T04
- Objective: Adjust widget payload detail per requesting admin's role (FR-8).
- Files to Modify: `dashboard/service.py`.
- Dependencies: Task 03, B-03 Task 04.
- Tests: Role-scoped detail variation test across two fixture roles.
- Definition of Done: Detail correctly reduced/expanded per role without ever exposing more than B-03's matrix permits.

**Task 05 — Implement Runbook Linking**
- Task ID: B-08-T05
- Objective: Attach `runbook_url` to known incident types (FR-11).
- Implementation Details: Static registry (config dict or small lookup table) mapping incident type → runbook URL for the six named runbooks.
- Dependencies: Task 02 (failed jobs/incidents widget).
- Definition of Done: Each of the six named incident types resolves to a runbook link when applicable.

**Task 06 — Implement Redis Caching for Freshness**
- Task ID: B-08-T06
- Objective: Meet ≤2-minute incident-visibility latency without excessive recompute cost.
- Implementation Details: Cache the composite response with a short TTL; cache invalidation/refresh strategy documented.
- Performance: Balances freshness vs. load.
- Dependencies: Task 03.
- Definition of Done: Latency test confirms freshness target met.

**Task 07 — Implement `GET /v1/admin/dashboard` Router**
- Task ID: B-08-T07
- Files to Create: `dashboard/api.py`.
- Dependencies: Tasks 01–06, B-03 Task 05.
- Definition of Done: Integration tests pass.

**Task 08 — Full Test Suite + Documentation**
- Task ID: B-08-T08
- Dependencies: Tasks 01–07.
- Definition of Done: All §27 scenarios green; OpenAPI updated with runbook registry documented.

## 30. Definition of Done
- All 8 widgets composed via independently-fallible parallel queries.
- One widget's failure never blocks the others; flagged `data_unavailable=true`.
- Role-scoped detail correctly applied.
- Runbooks linked for the six named incident types.
- Freshness target (≤2 min) met via caching.

## 31. Final Verification Checklist
- [ ] Signature test passes: one widget failure doesn't block the other 7
- [ ] All 8 canonical widgets present in the response shape
- [ ] `data_unavailable` flag correctly set on failure, never silently stale/hidden
- [ ] Zero-incidents state renders as empty array, not error
- [ ] Role-scoped detail verified across at least two fixture roles
- [ ] Six named runbooks correctly linked where applicable
- [ ] Caching strategy meets ≤2-minute freshness target
- [ ] No widget exposes data beyond what B-03's permission matrix already grants
