# B-08 — Delivery, Engagement & Binding Health Reporting API

## 1. Feature Context
Part of Feature B.17 — Notifications (Child-Facing). Provides the read-only reporting surface consumed by N-04 (Delivery/Engagement Report) and N-05 (Device Binding Health Monitor), giving visibility into the health of the exclusive-binding architecture and the calibration of quiet-hours/frequency policies.

## 2. Parent Feature
B.17 Notifications (Child-Facing) — Backend (FastAPI)

## 3. Sub-feature
B-08 Delivery, Engagement & Binding Health Reporting API

## 4. Objective
Implement read-only aggregate reporting endpoints surfacing sent/delivered/opened rates per category, suppression-reason breakdown, fatigue-backoff trigger frequency, and binding-switch/misdelivery-prevention health metrics.

## 5. Business Requirements
- `notification_suppressed` tagged by `suppression_reason` gives clear visibility distinguishing healthy suppression (quiet hours, stale condition) from potential calibration issues (frequency cap too aggressive) (PRD §11.1).
- Funnel: `notification_intent_created` → `notification_sent` → `notification_delivered` → `notification_opened` → `notification_deep_link_resolved`, comparable across notification classes for calibration (PRD §11.2).
- Device Binding Health Monitor surfaces binding-switch latency and a count of misdelivery-risk events correctly prevented by the send-time re-check — a positive integrity signal (PRD §8, mirrors B.15's duplicate-prevention monitor pattern).

## 6. Existing Architecture
- Extends `src/noorheroes/modules/notifications/` (`FAST-API-INSTRUCTIONS.md` §5.8).
- Read-only aggregation over tables owned by B-01/B-02/B-03/B-05 — this sub-feature must not write to any of those tables, only query and aggregate.

## 7. Existing Code to Reuse
- `BaseService`.
- Existing Admin RBAC dependencies (`product_admin`, `content_editor`, `trust_safety` roles).

## 8. Files to Create
- `src/noorheroes/modules/notifications/reporting_service.py` — `NotificationReportingService(BaseService)`.
- Extend `schemas.py`: `DeliveryEngagementReportResponse`, `BindingHealthReportResponse`.
- Extend `api.py`: `GET /v1/admin/notifications/reports/delivery-engagement`, `GET /v1/admin/notifications/reports/binding-health`.
- `tests/modules/notifications/test_reporting_service.py`.

## 9. Files to Modify
None outside this module.

## 10. Backend Requirements
- `get_delivery_engagement_report(date_range, category?, locale?)` — aggregates `notification_deliveries`/`notification_intents` into sent/delivered/opened rates, suppression-reason breakdown, fatigue-backoff trigger frequency.
- `get_binding_health_report(date_range)` — aggregates `device_profile_bindings`/audit logs of the B-03 send-time binding re-check into switch-latency percentiles and a "misdelivery-risk events correctly prevented" count (i.e., count of intents suppressed with `suppression_reason=binding_inactive`, framed positively as prevention, not failure).
- Cache expensive aggregate queries in Redis with a short TTL, invalidated on schedule rather than per-write (acceptable staleness of a few minutes for a reporting dashboard).
- Support pagination for any list-shaped sub-results; support date-range/category/locale filtering.

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
Consumed by N-04 Delivery & Engagement Report Dashboard and N-05 Device Binding Health Monitor.

## 13. API Contract

**Required API — Admin API**
- **HTTP Method:** GET
- **Endpoint:** `/v1/admin/notifications/reports/delivery-engagement?from=...&to=...&category=...`
- **Response 200:** `{ "funnel": {"created": 1000, "sent": 950, "delivered": 920, "opened": 340}, "suppression_breakdown": {"quiet_hours": 20, "frequency_cap": 15, ...}, "fatigue_backoff_count": 42 }`
- **Authentication:** Bearer (admin session)
- **Authorization:** `product_admin` or `content_editor`
- **Error Responses:** `401`, `403`, `422` invalid date range

- **HTTP Method:** GET
- **Endpoint:** `/v1/admin/notifications/reports/binding-health?from=...&to=...`
- **Response 200:** `{ "switch_latency_p50_ms": 120, "switch_latency_p95_ms": 340, "misdelivery_risk_events_prevented": 7 }`
- **Authentication:** Bearer (admin session)
- **Authorization:** `product_admin` or `trust_safety`

## 14. Database Requirements
Read-only aggregate queries over `notification_intents`, `notification_deliveries`, `device_profile_bindings` (all owned by earlier sub-features); no new tables.

## 15. Validation
Date range must be well-formed and not exceed a reasonable maximum window (e.g., 1 year) to bound query cost.

## 16. Authentication
Bearer JWT via admin session dependency.

## 17. Authorization
`product_admin`/`content_editor` for delivery-engagement report; `product_admin`/`trust_safety` for binding-health report.

## 18. Error Handling
| Scenario | System Behavior |
|---|---|
| Unauthorized/forbidden role | `401`/`403` |
| Invalid or excessive date range | `422` |
| Query timeout on large aggregation | `504`-equivalent with a clear error; consider pre-aggregation job for very large ranges (future optimization, not blocking for launch) |
| Cache miss | Falls through to live aggregate query, then populates cache |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Report data itself is numeric/structural; the NextJS admin UI (N-04/N-05) owns any localized labels.

## 22. RTL
N/A (backend).

## 23. Analytics
This endpoint is a consumer of the notification event taxonomy (PRD §1.19), not a producer of new events.

## 24. Performance
Aggregate queries must avoid N+1 patterns; use indexed columns (`status`, `created_at`, `sent_at`) already defined in B-01/B-02/B-05; Redis caching for repeat dashboard loads within a short TTL window.

## 25. Security
Read-only surface; no mutation risk. Ensure no raw child-identifying data leaks into aggregate report payloads — all metrics are counts/rates/percentiles only.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Redis (cache), Pydantic v2, pytest.

## 27. Testing
- Unit: aggregation logic against fixture data with known expected funnel/breakdown values.
- Integration: full report endpoint returning correct shape and RBAC enforcement.
- Performance: query executes within an acceptable bound against a realistically-sized fixture dataset.

## 28. Documentation
OpenAPI docs describing each metric's definition and calculation basis, so admin consumers correctly interpret the numbers.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement Delivery/Engagement Aggregation Query**
- Files to Create: `reporting_service.py` (partial).
- Implementation Details: funnel + suppression-breakdown + fatigue-backoff aggregation.
- Tests: unit test against known fixture data.

**Task 02 — Implement Binding Health Aggregation Query**
- Files to Modify: `reporting_service.py`.
- Implementation Details: switch-latency percentiles, misdelivery-risk-prevented count (positive framing).
- Tests: unit test against known fixture data.

**Task 03 — Add Redis Caching Layer**
- Files to Modify: `reporting_service.py`.
- Performance: short-TTL cache for repeat dashboard loads.
- Tests: cache-hit/miss test.

**Task 04 — Wire Admin API Endpoints with RBAC**
- Files to Modify: `api.py`, `schemas.py`.
- Authentication/Authorization: per §17.
- Tests: endpoint integration + RBAC-rejection tests.

**Task 05 — Write Full Test Suite & Documentation**
- Tests: per §27.
- Documentation: per §28.

## 30. Definition of Done
- Both reporting endpoints return correctly-aggregated, correctly-scoped data with enforced RBAC.
- Caching reduces repeat-load query cost without introducing stale-beyond-acceptable data.

## 31. Final Verification Checklist
- [ ] Delivery/engagement funnel numbers match expected values against fixture data
- [ ] Suppression-reason breakdown correctly categorizes all suppression types
- [ ] Binding-health latency percentiles and misdelivery-prevention count are accurate
- [ ] RBAC correctly restricts each report to its designated roles
- [ ] No raw child-identifying data appears in any report payload
- [ ] Caching layer functions correctly with acceptable staleness bounds
- [ ] Full test suite passes
