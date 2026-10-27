# Blueprint: Dashboard Report Retrieval API

## 1. Feature Context
Platform: NoorHeroes Backend (FastAPI). Module: `src/noorheroes/modules/dashboard/`. Delivers `GET /v1/parent/dashboard/reports/{type}?child_id=`, serving weekly/monthly/ai_insight/safety reports with graceful delay-handling and premium gating.

## 2. Parent Feature
C.20 — Parent Dashboard.

## 3. Sub-feature
B-03 — Dashboard Report Retrieval API.

## 4. Objective
Serve the full report payload for a given type and child, falling back to the last successfully generated report with an explicit "as of" timestamp when the current period's generation is delayed, and returning a locked/upsell shape (not an error) for non-premium `ai_insight` requests.

## 5. Business Requirements
Source: PRD §1.7 FR-8, FR-11, §3.4 (second endpoint), §4.2, Acceptance Criteria (delayed report), Edge Cases #4, #5.
- Report types: weekly (stories, Quran progress, duas, habit streaks, quiz scores, next-step recommendation), monthly family (aggregate-only cross-child), ai_insight (premium, weekly), safety (on demand).
- Delay handling: never blank/broken — return previous successfully generated report with its original `generated_at` as "as of".
- `ai_insight` non-premium → locked/upsell response shape, not an error (parent-surface monetization touchpoint, explicitly permitted per FR-10, unlike child-facing surfaces).
- Only rows with `content_safety_passed = true` are eligible to be returned (defense-in-depth query filter alongside B-05's write-time gate).

## 6. Existing Architecture
Same FastAPI layering as B-02. Depends on B-04 (AI Report Generation Service) having populated `weekly_report` / `monthly_family_report` / `ai_insight_report` / `safety_report` tables, and B-05 (Content Safety Validator) having set `content_safety_passed`.

**IMPORTANT — reconciled against C.22's already-written blueprints (`Development_Blueprints/C22_Per_Child_Reports/Backend/`), which explicitly build on top of this endpoint's tables/services:** this endpoint (`GET /v1/parent/dashboard/reports/{type}`) serves ONLY the Dashboard landing screen's condensed PREVIEW card (headline insight + trend + delayed/locked framing, consumed by K-03). C.22 independently exposes the FULL, deep-dive version of each report type at its OWN dedicated routes, reusing this same `AIReportGenerationService`/`ContentSafetyValidator`/tables rather than this endpoint: `GET /v1/parent/reports/{child_id}/ai-insight` (C.22 B-06), `GET /v1/parent/reports/{child_id}/safety-report` (C.22 B-04), `GET /v1/parent/reports/{family_id}/monthly-family` (C.22 B-05), and `GET /v1/parent/reports/{child_id}?from=&to=` (C.22 B-01, the general per-child aggregation covering the full weekly trend/habit-calendar/skill-mastery/AI-interaction view). "View full report" (K-03) must link to C.22's routes, not re-request this endpoint with different params. This is a two-tier design (condensed preview here, full depth in C.22), not a duplication — confirm this division of responsibility is preserved rather than collapsed when both features are implemented together.

**Confirmed real entitlement contract (C.24 B-06, `Development_Blueprints/C24_Subscription_Billing/Backend/06-platform-entitlement-check-service.md` — already written):** `GET /v1/entitlements/check?feature=&child_id=`, internally `SubscriptionService.get_entitlement(context, feature, child_id)` (`modules/subscriptions/`, not yet implemented in `backend/src` — stub package only) returning `{ "entitled": bool, "reason": str }`. The `feature` enum is exactly 7 checkpoint values: `catalog`, `search`, `content_detail`, `playback`, `download_manifest`, `ai_features`, `child_profile_activation` — **none of these is literally `ai_insight_report`**. This blueprint's `ai_insight` premium check should call this shared service with `feature="ai_features"` as the closest existing mapping; flag this mapping choice for confirmation with the C.24 team rather than assuming a dedicated `ai_insight_report` checkpoint value will be added, since C.24 B-06 explicitly positions itself as "the sole entitlement-decision authority platform-wide" that other features must not fork.

## 7. Existing Code to Reuse
- `GET /v1/entitlements/check?feature=ai_features&child_id=` (C.24 B-06, the confirmed platform-wide entitlement authority — call this shared endpoint/service, do not fork a local entitlement check).
- `require_parent_session_only` + `require_parent_gate_verified` (B-01) — inherited router-level gate, both already applied.
- Family-ownership validation pattern established in B-02.
- `BaseRepository.list_paginated()` / `get_by_id()` conventions for new report repositories, sorted by `(child_id, period_end DESC)` per PRD §4.2 index spec.

## 8. Files to Create
- `src/noorheroes/modules/dashboard/repository.py` — `WeeklyReportRepository`, `MonthlyFamilyReportRepository`, `AiInsightReportRepository`, `SafetyReportRepository`
- `tests/modules/dashboard/test_dashboard_report_retrieval_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/dashboard/schemas.py` — add `ReportResponse`, `DelayedReportResponse`, `LockedReportResponse`
- `src/noorheroes/modules/dashboard/service.py` — add `get_report(parent_ctx, report_type, child_id)`
- `src/noorheroes/modules/dashboard/api.py` — add `GET /v1/parent/dashboard/reports/{type}`

## 10. Backend Requirements
- Route: `GET /v1/parent/dashboard/reports/{type}?child_id=`, `type` constrained to `weekly|monthly|ai_insight|safety` (Pydantic/FastAPI `Literal` or `Enum`).
- `type == ai_insight`: call the platform-wide entitlement service with `feature="ai_features", child_id=<child_id>` (C.24 B-06 contract, `{entitled, reason}`); if `entitled == false`, return `LockedReportResponse` shape (200, not an error) with `upsell_reason = reason` from the entitlement response.
- Query: fetch most recent report row for `(child_id, period)` where `content_safety_passed = true` (or no such gate for `safety` type, which has no AI-content-safety concern per PRD §4.2 — safety reports are themselves safety-audit data, not AI-narrative content).
- If the CURRENT period's report is missing/not yet generated, query the previous period's row and return `DelayedReportResponse` with `delayed: true`, `last_known_report`, `last_known_as_of = generated_at` of that previous row.
- If a report exists for the current period but has `content_safety_passed = false`, treat identically to "not yet generated" — fall back to the previous passing report (mirrors delay-fallback logic per PRD §5 item 4).
- Family-ownership validation on `child_id` (same as B-02).

## 11. KMP Requirements
Consumed by K-03 (Weekly AI Report Card) via `DashboardRepository.getReport(type, childId)`. Response variants (`full`, `delayed`, `locked`) must map to distinct Compose UI states.

## 12. NextJS Requirements
N/A — no web-portal route.

## 13. API Contract
- **HTTP Method:** GET
- **Endpoint:** `/v1/parent/dashboard/reports/{type}?child_id=` (`type`: weekly|monthly|ai_insight|safety)
- **Auth:** Bearer, parent session only
- **Response 200 (normal):** full report payload per type (`summary_json`/`aggregate_summary_json`/`insight_json`/`ai_usage_summary`+`blocked_requests`)
- **Response 200 (delayed):** `{ "delayed": true, "last_known_report": {...}, "last_known_as_of": "ISO-8601" }`
- **Response 200 (locked, ai_insight non-premium):** `{ "locked": true, "upsell_reason": "premium_required" }`
- **Authentication:** Bearer parent session
- **Authorization:** Family-ownership on `child_id`; `ai_insight` additionally requires premium entitlement check (not a hard auth failure — locked-state response instead)
- **Validation:** `type` must be one of the 4 literal values; `child_id` required
- **Error Responses:** `403 CHILD_MODE_TOKEN_REJECTED`, `403`/`404` cross-family, `422` invalid `type`

## 14. Database Requirements
Reads `weekly_report`, `monthly_family_report`, `ai_insight_report`, `safety_report` (schemas owned by B-04). Query pattern: `WHERE child_id = ? AND content_safety_passed = true ORDER BY period_end DESC LIMIT 1` (or `generated_at DESC` for `safety_report`, which has no period concept per PRD ER diagram).

## 15. Validation
- `type` path param restricted to the 4 literal values (422 on anything else).
- `child_id` required, family-owned.

## 16. Authentication
Bearer parent session (B-01 gate).

## 17. Authorization
Family-ownership check; premium-entitlement soft-check for `ai_insight` (results in locked-state response, not a 403).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Current period not yet generated | `delayed: true` with previous period's report and its `generated_at` |
| Current period generated but failed content-safety | Same as above — treated as not-yet-generated |
| `ai_insight` requested by non-premium account | `locked: true` upsell shape (200, not error) |
| No report has ever been generated for this child/type | Explicit "no report yet" empty variant (mirrors PRD §1.12 empty-state philosophy), not the same as `delayed` |
| Cross-family `child_id` | `403`/`404` |

## 19. Offline First
N/A server-side.

## 20. Local Data
N/A (backend).

## 21. Localization
`upsell_reason` and any narrative text in `summary_json`/`insight_json` sourced as pre-localized content from B-04's generation pipeline, not hardcoded here.

## 22. RTL
N/A (backend).

## 23. Analytics
`ai_insight_locked_state_shown`, `dashboard_report_delayed_state_shown` are fired client-side (K-03) based on which response variant this API returns.

## 24. Performance
Indexed queries per PRD §4.2 (`(child_id, period_end DESC)` / `(child_id, generated_at DESC)`); weekly-report-derived cache TTL longer than timeline (shared with B-02's caching strategy where applicable).

## 25. Security
Content-safety-passed filter is a defense-in-depth read-time check, layered on top of B-05's write-time gate — a report failing validation must never be servable even if a future caching/query-logic bug is introduced elsewhere (PRD §12.2 Security Misconfiguration mitigation).

## 26. Library Requirements
No new dependencies.

## 27. Testing
1. Unit test: normal report retrieval for each of the 4 types.
2. Unit test: delayed-state fallback returns previous period's report with correct `as_of`.
3. Unit test: content-safety-failed current-period report is treated as not-yet-generated (falls back correctly) — mirrors item 3.
4. Unit test: `ai_insight` non-premium returns locked-state shape, not an error.
5. Unit test: `ai_insight` premium returns full content.
6. Unit test: cross-family `child_id` rejected.
7. Unit test: invalid `type` literal returns `422`.
8. Integration test: full request lifecycle through B-01 gate.

## 28. Documentation
OpenAPI docstrings per response variant (use `responses={}` with multiple documented shapes per status code where FastAPI/OpenAPI tooling supports it).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Report Repositories**
- Task ID: B03-T01
- Objective: Data-access layer for the 4 report tables.
- Why This Is Required: Clean separation per platform's Router→Service→Repository layering.
- Existing Architecture to Follow: `BaseRepository[ModelT]` generic pattern.
- Existing Files to Reuse: `common/base_repository.py`.
- Files to Create: `src/noorheroes/modules/dashboard/repository.py`.
- Files to Modify: none.
- Implementation Details: 4 repository classes, each with `get_latest_passing(child_id, period=None)` returning most recent `content_safety_passed=true` row, and `get_latest_any(child_id)` for the "no report ever" empty-state check.
- Business Rules: FR-8, FR-11.
- Validation: N/A.
- Error Handling: Return `None` if no row found (service layer decides empty vs. delayed framing).
- Security: content_safety_passed filter baked into `get_latest_passing`.
- Performance: Uses PRD §4.2 indexes.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: Docstrings citing PRD §4.2.
- Dependencies: B-04's table schemas must exist (migrations).
- Do Not Change: Do not alter `BaseRepository` itself.
- Expected Result: Repositories return correctly filtered rows.
- Definition of Done: Matches §14 query pattern.

**Task 02 — Implement get_report Service Method**
- Task ID: B03-T02
- Objective: Orchestrate delayed-fallback and locked-state logic.
- Why This Is Required: Core business logic distinguishing 3 response variants.
- Existing Architecture to Follow: `BaseService` pattern.
- Existing Files to Reuse: `SubscriptionService.get_entitlement()`.
- Files to Create: none.
- Files to Modify: `src/noorheroes/modules/dashboard/service.py`.
- Implementation Details: Per §10 logic; family-ownership check first (reuse B-02's helper).
- Business Rules: FR-8, FR-10, FR-11, Edge Case #5.
- Validation: `type` literal validated at route layer (Task 04).
- Error Handling: Per §18.
- Security: Premium-gating and content-safety filter enforcement.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: Docstring citing PRD §5 item 3/4/6.
- Dependencies: Task 01.
- Do Not Change: Do not modify `SubscriptionService` internals — consume its public method only.
- Expected Result: Service returns correct variant per scenario.
- Definition of Done: All 3 response variants correctly distinguished.

**Task 03 — Implement Route**
- Task ID: B03-T03
- Objective: Expose `GET /v1/parent/dashboard/reports/{type}`.
- Why This Is Required: Public contract delivery.
- Existing Architecture to Follow: Existing router pattern, `Literal`/`Enum` path param validation.
- Existing Files to Reuse: `api.py` from B-01/B-02.
- Files to Create: none.
- Files to Modify: `src/noorheroes/modules/dashboard/api.py`, `schemas.py`.
- Implementation Details: `type: Literal["weekly", "monthly", "ai_insight", "safety"]` path param; response union modeled via a discriminated schema or `response_model=None` with manual serialization if FastAPI union response modeling is constrained by existing conventions.
- Business Rules: FR-8.
- Validation: `422` on invalid `type` (automatic via `Literal`).
- Error Handling: Per §18.
- Security: Inherits B-01 gate.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: OpenAPI per §28.
- Dependencies: Tasks 01–02.
- Do Not Change: N/A.
- Expected Result: Endpoint live matching §13.
- Definition of Done: Contract verified via OpenAPI export.

**Task 04 — Write Test Suite**
- Task ID: B03-T04
- Objective: Cover §27 scenarios, notably the two PRD-mandated signature tests (delay-fallback, content-safety-fallback).
- Why This Is Required: PRD §5 items 3 and 4 explicitly require these tests.
- Existing Architecture to Follow: pytest fixtures.
- Existing Files to Reuse: Fixture factories from B-02's test suite.
- Files to Create: `tests/modules/dashboard/test_dashboard_report_retrieval_api.py`.
- Files to Modify: none.
- Implementation Details: 8 test cases per §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Exact response shape assertions.
- Security: content-safety-fallback test is security-critical (confirms failed content never served).
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test docstrings.
- Dependencies: Tasks 01–03.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 green, including the two PRD-signature tests.

## 30. Definition of Done
`GET /v1/parent/dashboard/reports/{type}` live for all 4 types, correctly distinguishing normal/delayed/locked/empty variants, content-safety-filtered, premium-gated for `ai_insight`, all tests green.

## 31. Final Verification Checklist
- [ ] Delayed-state fallback returns previous report with correct `as_of`, never blank
- [ ] Content-safety-failed report never served, transparently falls back
- [ ] `ai_insight` non-premium returns locked shape, not an error
- [ ] Family-ownership check independent of B-01's token check
- [ ] Indexes per PRD §4.2 in place
- [ ] No hardcoded narrative strings in this layer
