# B-05 — Admin Bedtime Configuration Analytics API

> **Status:** Implemented & Verified (100% Green, 198 Admin Tests + 125 Bedtime Tests Passing, 0 Regressions, 0 Warnings)  
> **Parent Feature:** Feature A.4 — Audio Bedtime Player & Bedtime Mode  
> **Sub-feature ID:** B-05 (1.5 Admin Bedtime Configuration Analytics API)  
> **Authoritative Specification:** `FAST-API-INSTRUCTIONS.md` §5.2, §6, §7, §8, §9 (Scenario 13), §15 & `MASTER-README.md` §11.31  
> **Last Verified:** 2026-09-07  

## 1. Feature Context
A read-only, strictly-aggregated analytics endpoint giving the Admin Portal visibility into bedtime-window adoption, sleep-timer-ceiling calibration, and ritual-completion trends across the user base — without ever exposing individual-child-level rows, sourced from B-01's `bedtime_config` and B-04's `bedtime_session_log`.

## 2. Parent Feature
Feature A.4 — Audio Bedtime Player & Bedtime Mode

## 3. Sub-feature
1.5 Admin Bedtime Configuration Analytics API (ID: **B-05**)

## 4. Objective
Build `GET /admin/v1/bedtime/analytics`, returning pre-aggregated adoption-rate, sleep-timer-ceiling distribution, and ritual-completion-rate trend data, enforced as aggregate-only at the query layer (never row-level), gated by the existing Admin Portal RBAC.

## 5. Business Requirements
- §8 Admin Requirements: "Bedtime Configuration Analytics (Read-only): Aggregate, privacy-safe view of bedtime-window adoption rates, average sleep-timer-ceiling settings across the user base, and ritual-completion-rate trends... never exposing individual child detail."
- §9 (Admin AI prompt item 2): endpoint returns pre-aggregated data; NEVER exposes any individual `child_id`-level row; enforced by the backing API only returning pre-aggregated data, not raw per-child rows.

## 6. Existing Architecture
Follows the existing Admin Portal API convention already established by A.3's admin analytics endpoints (e.g., the Download Manifest Health Monitoring API) — `modules/admin/bedtime_analytics/` sub-package within the existing admin API surface, gated by the same `require_admin_role()` dependency pattern used across all `/admin/v1/*` routes.

## 7. Existing Code to Reuse
- `core/deps.py::require_admin_role(role="...")` (confirm exact signature against an existing admin-gated endpoint, e.g., A.3's admin catalog management API, and mirror it)
- `modules/bedtime/models.py::BedtimeConfigOrm`, `BedtimeSessionLogOrm` (B-01, B-04) — read-only queries against these, no new tables
- Existing admin router registration pattern (`modules/admin/api.py` or equivalent aggregator)

## 8. Files Created
- `src/noorheroes/modules/admin/bedtime_analytics/__init__.py`
- `src/noorheroes/modules/admin/bedtime_analytics/schemas.py` — `BedtimeAnalyticsResponse`, `AnalyticsBucketEnum`, `AdoptionRatePoint`, `CeilingDistributionBucket`, `RitualCompletionRatePoint` (strict `extra="forbid"`, camelCase wire aliasing)
- `src/noorheroes/modules/admin/bedtime_analytics/service.py` — `BedtimeAnalyticsService` (100% database-layer SQL aggregation via `COUNT`, `GROUP BY`, `CASE WHEN`, dialect-aware `func.to_char` on Postgres and `func.strftime` on SQLite, 365-day query ceiling enforcement)
- `src/noorheroes/modules/admin/bedtime_analytics/api.py` — `admin_bedtime_analytics_router` (dual-mounted `GET /v1/admin/bedtime/analytics` and `GET /admin/v1/bedtime/analytics`, thin controller invariant with 0 `if/elif` statements)
- `tests/modules/admin/test_bedtime_analytics_api.py` — 25 comprehensive test scenarios (happy paths, boundaries, roles, buckets, empty dataset, real SQLite DB)
- `tests/modules/admin/test_bedtime_analytics_privacy.py` — 9 dedicated structural and content privacy & PII exclusion test scenarios (34 tests total, 0 warnings)

## 9. Files Modified
- `main.py` — mount `admin_v1_bedtime_analytics_router`
- `src/noorheroes/modules/admin/api.py` — mount `admin_bedtime_analytics_router` under `/v1/admin/bedtime`
- `src/noorheroes/modules/admin/deps.py` — configure RBAC scope allowlist (`admin:read`, `content_editor`, `product_admin`)
- `src/noorheroes/modules/admin/README.md` — Section 10 documentation
- `FAST-API-INSTRUCTIONS.md` — Section 5.2, 6, 7, 8, 9 (Scenario 13), 15
- `MASTER-README.md` — Section 11.31, Table of Contents, Route Catalog, Production Security Checklist
- `docs/TESTING.md` — Section 2, 4.13
- `docs/NoorHeroes_Consolidated_Execution_Blueprint.md` — Section 0.5, row 156
- `artifacts/openapi.json` — exported OpenAPI schema with zero breaking changes

## 10. Backend Requirements
- Adoption rate: `COUNT(bedtime_config WHERE window_start IS NOT NULL) / COUNT(all children)` over a requested date range, bucketed (e.g., weekly).
- Sleep-timer-ceiling distribution: `GROUP BY sleep_timer_ceiling_minutes` histogram bucketed into sensible ranges (e.g., 5–15, 16–30, 31–45, 46–60, 60+).
- Ritual-completion-rate trend: `bedtime_session_log` `GROUP BY session_date` aggregate count / active-child-count, over the requested range.
- All three queries use SQL-level `GROUP BY`/`COUNT`/`AVG` aggregation — the service layer never fetches per-child rows into application memory and aggregates in Python (this would risk an accidental row-level leak in a future code change; aggregation must happen in the database).

## 11. API Contract

### `GET /admin/v1/bedtime/analytics?start_date=&end_date=&bucket=weekly`
- Auth: Bearer (admin session, `content_editor` or `product_admin` role — confirm minimum required role against existing admin analytics endpoints and mirror it, likely a read-level analytics role rather than `product_admin`).
- Response 200: `{ "adoption_rate_trend": [{ "period": "2026-W30", "rate": 0.42 }, ...], "sleep_timer_ceiling_distribution": [{ "bucket": "16-30", "count": 812 }, ...], "ritual_completion_rate_trend": [{ "period": "2026-08-10", "rate": 0.71 }, ...] }`.
- Errors: `401 UNAUTHORIZED`, `403 FORBIDDEN` (insufficient admin role), `422 INVALID_DATE_RANGE`.

## 12. Database Requirements
No new tables. Read-only aggregate queries against `bedtime_config` and `bedtime_session_log` (B-01, B-04). Consider a materialized/cached aggregate refresh if query cost against a large user base becomes significant (not required for initial implementation, but the service method should be structured so caching can be added without an API contract change).

## 13. Validation
- `start_date`/`end_date` must be valid dates, `start_date <= end_date`, and the range capped at a sane maximum (e.g., 12 months) to bound query cost.
- `bucket` restricted to an enum (`daily`, `weekly`, `monthly`).

## 14. Authentication
Bearer, admin session only — reuses the existing Admin Portal auth dependency, no new auth mechanism.

## 15. Authorization
Gated by the existing Admin Portal role context; the response schema itself structurally cannot carry a `child_id` field, so even a role-check bypass could not leak individual-child data through this endpoint's response shape.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| No data in the requested range | `200` with empty trend arrays, not an error |
| Invalid date range | `422 INVALID_DATE_RANGE` |
| Insufficient admin role | `403 FORBIDDEN` |
| Database failure | `503`, structured error, logged with correlation ID |

## 17. Security
- Aggregate-only enforcement is structural (schema has no per-child field) and query-level (SQL `GROUP BY`, never row-level fetch-then-aggregate) — defense in depth against a future accidental regression.
- Standard Admin Portal RBAC and audit-logging conventions apply to read access on sensitive analytics surfaces if the existing convention logs analytics-page views (confirm and mirror; do not add a new audit mechanism if request logging already covers this).

## 18. Analytics
This endpoint is itself an analytics-serving surface; no additional business event emission required beyond standard admin-API access logging already in place.

## 19. Performance
- Aggregate SQL queries with appropriate indexes (`bedtime_session_log(child_id, session_date)` from B-04 supports the completion-rate query; consider an index on `bedtime_config.sleep_timer_ceiling_minutes` if the ceiling-distribution query becomes slow at scale).
- Response caching (short TTL, e.g., 15–30 min) acceptable given this is a trend dashboard, not real-time data.

## 20. Library Requirements
No new third-party libraries.

## 21. Testing
- Unit: aggregation math correctness against a seeded fixture (known adoption rate, known distribution, known completion rate).
- **Privacy test (dedicated suite):** assert the response payload, serialized to JSON, contains no `child_id`-shaped UUID matching any seeded child's actual ID — a structural/content-based leak-detection test, not just a schema-shape assertion.
- Integration: `403` for insufficient role; `422` for invalid date range; empty-range handling.

## 22. Documentation
Update OpenAPI schema; run `classify_openapi_diff.py`.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Define `BedtimeAnalyticsResponse` Schema** `[COMPLETED]`
Objective: Pre-aggregated response shapes with no per-child field anywhere. Files created: `src/noorheroes/modules/admin/bedtime_analytics/schemas.py`. Schemas: `BedtimeAnalyticsResponse`, `AnalyticsBucketEnum`, `AdoptionRatePoint`, `CeilingDistributionBucket`, `RitualCompletionRatePoint`. Enforces Pydantic v2 `extra="forbid"` and camelCase wire aliasing. Definition of Done: verified by structural extra-field rejection and camelCase serialization tests.

**Task 02 — Implement `BedtimeAnalyticsService` with SQL-Level Aggregation** `[COMPLETED]`
Objective: Three aggregate queries (adoption rate, ceiling distribution, completion-rate trend), all using `GROUP BY`/`COUNT`/`CASE WHEN` at the database layer with zero row-level child loading into application memory. Files created: `src/noorheroes/modules/admin/bedtime_analytics/service.py`. Features: dialect-aware date formatting (`to_char` on PostgreSQL, `strftime` on SQLite), 365-day query ceiling enforcement with 422 `INVALID_DATE_RANGE`, and safe fallback for empty ranges (200 OK with empty trends and zeroed 5 standard ceiling intervals `5-15`, `16-30`, `31-45`, `46-60`, `60+`). Definition of Done: verified by SQLite relational integration tests.

**Task 03 — Implement the Router Endpoint** `[COMPLETED]`
Objective: Gated by the existing admin-role dependency (`require_any_scope("admin:read", "content_editor", "product_admin")`). Files created: `src/noorheroes/modules/admin/bedtime_analytics/api.py`. Mounted canonical `GET /v1/admin/bedtime/analytics` and alias `GET /admin/v1/bedtime/analytics`. Thin controller invariant: strictly 0 `if/elif` statements. Multi-language error localization across `en`, `hi`, `ur`, `ar`. Definition of Done: tests pass.

**Task 04 — Write the Dedicated Privacy-Boundary Test Suite** `[COMPLETED]`
Objective: Confirm no per-child identifier ever appears in the serialized response across all three aggregate sections. Files created: `tests/modules/admin/test_bedtime_analytics_privacy.py` (9 dedicated scenarios). Verifies structural schema immunity and regex UUID scan on wire JSON ensuring zero PII leak. Definition of Done: all 9 privacy tests pass and gate CI.

**Task 05 — Add Full Test Suite** `[COMPLETED]`
Objective: Complete coverage per §21. Files created: `tests/modules/admin/test_bedtime_analytics_api.py` (25 scenarios) and `tests/modules/admin/test_bedtime_analytics_privacy.py` (9 scenarios) for total 34 dedicated test cases. Definition of Done: 100% green across all 198 admin module tests with 0 warnings.

**Task 06 — Update OpenAPI Documentation** `[COMPLETED]`
Objective: Regenerate and export OpenAPI 3.1.0 specifications. Exported to `artifacts/openapi.json` with operation ID `get_bedtime_configuration_analytics` under tags `Admin Portal`, `Admin Bedtime Analytics`. Definition of Done: additive/non-breaking diff confirmed.

**Task 07 — Final Code Review** `[COMPLETED]`
Objective: Confirm every query path aggregates in SQL, never in application code after a per-row fetch; confirm the response schema structurally cannot carry per-child data. Definition of Done: checklist in §24 fully checked and verified.

## 24. Final Verification Checklist
- [x] All three aggregate metrics computed via SQL `GROUP BY`/`COUNT`/`AVG`, never Python-side aggregation of per-row fetches
- [x] Response schema has no field capable of carrying a `child_id` or other individual identifier
- [x] Dedicated privacy-boundary test passes and is a required CI gate
- [x] `403` enforced for insufficient admin role
- [x] Empty-range/no-data periods return `200` with empty arrays, not an error
- [x] OpenAPI diff confirmed additive/non-breaking

## 25. Definition of Done
The Admin Portal can display bedtime-window adoption, sleep-timer-ceiling calibration, and ritual-completion trends entirely from pre-aggregated, privacy-safe data — with a dedicated automated test guaranteeing no individual child's data can ever surface through this endpoint.
