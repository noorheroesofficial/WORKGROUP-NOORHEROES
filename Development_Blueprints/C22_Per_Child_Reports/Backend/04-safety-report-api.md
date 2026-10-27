# Blueprint: Safety Report API

## 1. Feature Context
Platform: NoorHeroes Backend (FastAPI). Module: `src/noorheroes/modules/dashboard/`, sourcing from `src/noorheroes/modules/ai_safety/`. Delivers the on-demand `GET /v1/parent/reports/{child_id}/safety-report` endpoint.

## 2. Parent Feature
C.22 — Per-Child Reports.

## 3. Sub-feature
B-04 — Safety Report API.

## 4. Objective
Produce, on demand, a full transparency report — AI usage history, blocked requests, content flags, profile-setting changes — for one child, governed by the same Content Safety Validator gate as every other report type in this feature, with a clean/reassuring zero-events state.

## 5. Business Requirements
Source: PRD §1.6 User Story 8, §1.7 FR-6 (Safety report — on demand), FR-8, §1.10 Edge Case #3, §3.4.
- Four content areas: `ai_usage_summary`, `blocked_requests`, `content_flags`, `profile_setting_changes`.
- On-demand generation, not a scheduled cadence.
- Zero safety events ever recorded → a clean/reassuring "no safety events recorded" state, never an error or empty-looking broken section (Edge Case #3).
- AI-generated portions (if any narrative summary is included) must never diagnose, compare siblings, or present uncertain conclusions as fact (FR-8, Content Safety Validator).

## 6. Existing Architecture
Reuses C.20's `AI Report Generation Service` and mandatory write-time `Content Safety Validator` gate (C.20 B-04/B-05) — the same canonical `safety_report` table defined in C.20 §4.1 is reused here, not duplicated. Sources `blocked_requests`/`content_flags` from B-03's `ai_safety_event` store and `profile_setting_changes` from C.23's Parental Controls audit trail.

## 7. Existing Code to Reuse
- `AIReportGenerationService` (C.20) — extend with a `generate_safety_report(child_id)` method rather than a new parallel generation service.
- `ContentSafetyValidator` (C.20 B-05) — mandatory write-time gate, reused as-is.
- `require_parent_session_only` (C.20 B-01).
- B-03's `AiSafetyEvent` repository for `blocked_requests`/`content_flags` sourcing.
- C.23 B-03's `parent_overrides` table (`ParentOverrideRepository`, `src/noorheroes/modules/restrictions/`, append-only) — the confirmed source for screen-time/bedtime override entries within `profile_setting_changes`. **Open gap, flagged rather than invented:** C.23 B-04 (AI Permissions & Content Age Level Configuration API) writes directly to `modules/identity/models.py::ChildProfile` and, per its own blueprint, does not yet define a dedicated change-audit trail for those fields — C.23 B-04's blueprint itself flags this as unconfirmed. Until that gap is resolved (either by C.23 B-04 adopting the `admin` context's `AuditLog`-style before/after pattern for parent-initiated changes, or a new `child_profile_change_log` table), this endpoint's `profile_setting_changes` array should be populated from `parent_overrides` only, with AI-permission/content-age-level changes omitted rather than fabricated — do not synthesize entries from `ChildProfile`'s current state alone, since that cannot reconstruct historical changes.

## 8. Files to Create
- `tests/modules/dashboard/test_safety_report_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/dashboard/schemas.py` — add `SafetyReportResponse`
- `src/noorheroes/modules/dashboard/service.py` — add `get_safety_report(parent_ctx, child_id)`
- `src/noorheroes/modules/dashboard/api.py` — add `GET /v1/parent/reports/{child_id}/safety-report`

## 10. Backend Requirements
- Route: `GET /v1/parent/reports/{child_id}/safety-report`, gated by `require_parent_session_only` + family-ownership.
- On request: validate family-ownership, then generate/compose the report on demand (not from a pre-scheduled cadence table row, unlike weekly/monthly):
  1. `ai_usage_summary`: aggregate counts/categories from `ai_safety_event` (B-03).
  2. `blocked_requests`: filter `ai_safety_event` where `category` implies blocking (e.g., `topic_blocked`).
  3. `content_flags`: filter `ai_safety_event` where `concerning = true`.
  4. `profile_setting_changes`: sourced from `parent_overrides` (C.23 B-03) for the child; AI-permission/content-age-level changes omitted pending resolution of the open gap noted in §7.
  5. Run the composed payload through `ContentSafetyValidator` before returning (write-time gate, even though this is a read-composed report, treated with the same governance as generated report types per PRD §3.5).
  6. If all four areas are empty, return the explicit "no safety events recorded" clean state, not a `404` or empty object.

## 11. KMP Requirements
Consumed by K-04 (`SafetyReportScreen`).

## 12. NextJS Requirements
N/A for the parent-facing endpoint; N-02's audit log surfaces this report type in aggregate for trust_safety/ai_ops review.

## 13. API Contract
- **HTTP Method:** GET
- **Endpoint:** `/v1/parent/reports/{child_id}/safety-report`
- **Auth:** Bearer, parent session only
- **Request:** path `child_id: str`
- **Response 200:**
```json
{
  "ai_usage_summary": { "total_interactions": 0, "period_covered": "all_time" },
  "blocked_requests": [ { "date": "ISO-8601", "category": "string", "summary": "string" } ],
  "content_flags": [ { "date": "ISO-8601", "category": "string", "summary": "string", "concerning": true } ],
  "profile_setting_changes": [ { "date": "ISO-8601", "change": "string" } ],
  "is_clean_state": false
}
```
- **Authentication:** Bearer parent session
- **Authorization:** Family-ownership on `child_id`
- **Validation:** `child_id` required
- **Error Responses:** `403`/`404` `ChildScopeViolationError`, `401` invalid session, `503` if `ContentSafetyValidator` gate fails to complete (fallback per §12 pattern, not applicable to this read-composed type since there is no prior "passing" version to fall back to — treat as retryable generation failure)

## 14. Database Requirements
Composes on-the-fly from `ai_safety_event` (B-03) and `parent_overrides` (C.23 B-03) — no new table required for this endpoint's own data. The `safety_report` row referenced in C.20 §4.1/C.22 §4.1 is the `content_safety_passed` audit artifact the Content Safety Validator writes for this report *type* (consistent with every other report type in this feature going through that same gate), not a cache of the report's content itself; this endpoint does not read report content back from that row.

## 15. Validation
`child_id` required, family-owned.

## 16. Authentication
Bearer parent session.

## 17. Authorization
Family-ownership check on `child_id`.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Cross-family `child_id` | `403`/`404` `ChildScopeViolationError` |
| Zero safety events ever | `200` with `is_clean_state: true`, all arrays empty (Edge Case #3) |
| Content Safety Validator fails on the composed payload | `503`, retryable, never serves an unvalidated payload |

## 19. Offline First
N/A server-side; export/share (B-07/B-08) reuse this data, gated identically to online-only per PRD Edge Case #9.

## 20. Local Data
N/A (backend).

## 21. Localization
`summary` fields reuse B-03's locale-resolved templates; `change` descriptions sourced from C.23's localized audit-log copy.

## 22. RTL
N/A (backend).

## 23. Analytics
`safety_report_requested` fired client-side (K-04).

## 24. Performance
On-demand generation p95 within Report NFR; reuses B-03's indexed queries, no full-table scans.

## 25. Security
Mandatory `ContentSafetyValidator` gate applied identically to this report type — no parallel, less-governed generation path (PRD §3.5).

## 26. Library Requirements
No new dependencies.

## 27. Testing
1. Unit test: full report composition with events across all four areas.
2. Unit test: zero-events clean state returned correctly, not an error.
3. Unit test: cross-family `child_id` rejected.
4. Unit test: `ContentSafetyValidator` gate correctly applied before response.
5. Integration test: full on-demand generation request through the gate.

## 28. Documentation
OpenAPI docstring describing on-demand cadence and the clean-state contract.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define SafetyReportResponse Schema**
- Task ID: B04-T01
- Objective: Pydantic schema for the four-area report plus `is_clean_state`.
- Why This Is Required: Type-safe contract.
- Existing Architecture to Follow: `NoorHeroesBaseModel`.
- Existing Files to Reuse: `schemas.py` base.
- Files to Create: none.
- Files to Modify: `schemas.py`.
- Implementation Details: `SafetyReportResponse` per §13.
- Business Rules: FR-6.
- Validation: N/A.
- Error Handling: N/A.
- Security: N/A.
- Performance: N/A.
- Localization: Pre-localized fields.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered by Task 03.
- Documentation: Docstrings.
- Dependencies: none.
- Do Not Change: C.20's `safety_report` schema if reused as-is.
- Expected Result: Schema importable.
- Definition of Done: Matches §13.

**Task 02 — Implement get_safety_report Service Method and Route**
- Task ID: B04-T02
- Objective: Compose the four-area report, apply the Content Safety Validator gate, handle the clean state.
- Why This Is Required: Core business logic.
- Existing Architecture to Follow: `AIReportGenerationService`/`ContentSafetyValidator` reuse pattern from C.20.
- Existing Files to Reuse: B-03's `AiSafetyEvent` repository, C.23's audit trail.
- Files to Create: none.
- Files to Modify: `service.py`, `api.py`.
- Implementation Details: Per §10 steps 1–6.
- Business Rules: FR-6, FR-8, Edge Case #3.
- Validation: Family-ownership.
- Error Handling: Per §18.
- Security: Content Safety Validator gate mandatory.
- Performance: Indexed sourcing from B-03.
- Localization: Reuse templates.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 03.
- Documentation: Docstring.
- Dependencies: Task 01, B-03, C.20 B-04/B-05.
- Do Not Change: `ContentSafetyValidator` internals.
- Expected Result: Endpoint composes and validates correctly.
- Definition of Done: Clean state and populated state both verified.

**Task 03 — Write Test Suite**
- Task ID: B04-T03
- Objective: Cover §27.
- Why This Is Required: QA coverage including Edge Case #3.
- Existing Architecture to Follow: pytest + fixtures.
- Existing Files to Reuse: Family/child/session fixtures, B-03 event fixtures.
- Files to Create: `tests/modules/dashboard/test_safety_report_api.py`.
- Files to Modify: none.
- Implementation Details: 5 test cases per §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert exact responses.
- Security: Content Safety Validator gate test is critical.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test docstrings.
- Dependencies: Tasks 01–02.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 green.

## 30. Definition of Done
`GET /v1/parent/reports/{child_id}/safety-report` live, gated, composes all four content areas, applies the Content Safety Validator, returns the clean state for zero events, all tests green.

## 31. Final Verification Checklist
- [ ] Family-ownership check verified
- [ ] Clean/reassuring zero-events state verified (Edge Case #3)
- [ ] Content Safety Validator gate applied before response
- [ ] `blocked_requests`/`content_flags` sourced exclusively from B-03's structurally redacted store
- [ ] `profile_setting_changes` sourced from C.23's audit trail, not invented
- [ ] OpenAPI docs reflect the on-demand contract
