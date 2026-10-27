# Blueprint: Monthly Family Report API

## 1. Feature Context
Platform: NoorHeroes Backend (FastAPI). Module: `src/noorheroes/modules/dashboard/`. Delivers `GET /v1/parent/reports/{family_id}/monthly-family` — the cross-child, aggregate-only monthly summary.

## 2. Parent Feature
C.22 — Per-Child Reports.

## 3. Sub-feature
B-05 — Monthly Family Report API.

## 4. Objective
Serve a monthly, cross-child aggregate report (family streaks, content favorites, learning consistency) with a response schema that structurally prevents any per-child comparison array, enforcing FR-8's "never compare siblings" rule at the data-contract level.

## 5. Business Requirements
Source: PRD §1.7 FR-6 (Monthly family report — monthly cadence), FR-8, §3.4, §4.1 (reuses C.20's canonical `monthly_family_report` table).

- Content: cross-child progress summary, family streaks, content favorites, learning consistency — aggregate-only, no per-child breakdown array.
- Monthly cadence, async-generated (mirrors C.20's weekly report generation pattern).
- Content Safety Validator gate applied — never compare siblings, never diagnose, never present uncertain conclusions as fact.

## 6. Existing Architecture
Reuses the canonical `monthly_family_report` table defined in C.20 §4.1 and C.20's `AIReportGenerationService`/`ContentSafetyValidator`. This blueprint's only new contribution is the read endpoint and its aggregate-only response schema — no new generation pipeline.

## 7. Existing Code to Reuse
- `AIReportGenerationService` (C.20) — reused generation pipeline, extended with a monthly-family report type if not already implemented in C.20's scope.
- `ContentSafetyValidator` (C.20 B-05).
- `require_parent_session_only` (C.20 B-01).
- `FamilyRepository` for family-ownership/membership validation.

## 8. Files to Create
- `tests/modules/dashboard/test_monthly_family_report_api.py`
- `tests/modules/dashboard/test_monthly_family_report_no_sibling_comparison_structural.py`

## 9. Files to Modify
- `src/noorheroes/modules/dashboard/schemas.py` — add `MonthlyFamilyReportResponse`
- `src/noorheroes/modules/dashboard/service.py` — add `get_monthly_family_report(parent_ctx, family_id)`
- `src/noorheroes/modules/dashboard/api.py` — add `GET /v1/parent/reports/{family_id}/monthly-family`

## 10. Backend Requirements
- Route: `GET /v1/parent/reports/{family_id}/monthly-family`, gated by `require_parent_session_only` + family-membership check (the requesting parent must belong to `family_id`).
- Response schema `MonthlyFamilyReportResponse` contains only aggregate fields (`family_streak_days`, `content_favorites: list[str]`, `learning_consistency_summary: str`, `as_of`) — **no field shaped as `per_child: list[...]` or any structure allowing a child-by-child comparison array to exist**.
- Retrieve the latest generated `monthly_family_report` row for the family; if `content_safety_passed = false`, fall back to the most recent passing row (mirrors C.20's established read-API fallback pattern).
- If no report has been generated yet (e.g., family created mid-month), return an explicit "report not yet available, check back after month-end" state rather than an error.

## 11. KMP Requirements
Consumed by K-05 (`Monthly Family Report Screen`).

## 12. NextJS Requirements
N/A.

## 13. API Contract
- **HTTP Method:** GET
- **Endpoint:** `/v1/parent/reports/{family_id}/monthly-family`
- **Auth:** Bearer, parent session only
- **Request:** path `family_id: str`
- **Response 200:**
```json
{
  "family_id": "string",
  "family_streak_days": 0,
  "content_favorites": ["string"],
  "learning_consistency_summary": "string",
  "as_of": "ISO-8601",
  "report_available": true
}
```
- **Authentication:** Bearer parent session
- **Authorization:** Requesting parent must belong to `family_id`
- **Validation:** `family_id` required
- **Error Responses:** `403` if parent does not belong to `family_id`, `401` invalid session

## 14. Database Requirements
Reuses `monthly_family_report` (C.20 §4.1) — no new table. Read-only from this blueprint's perspective.

## 15. Validation
`family_id` required and must match the authenticated parent's own family (not a `child_id`-based check, since this is a family-level, not child-level, report).

## 16. Authentication
Bearer parent session.

## 17. Authorization
Family-membership check on `family_id` (distinct from the family-ownership-on-`child_id` pattern used elsewhere — this is a direct family match).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Parent does not belong to `family_id` | `403` |
| No report generated yet | `200` with `report_available: false` and a clear "check back after month-end" framing |
| Latest report failed content-safety validation | Falls back to last passing report (C.20 pattern) |

## 19. Offline First
N/A server-side; K-05/K-09 handle client-side caching.

## 20. Local Data
N/A (backend).

## 21. Localization
`learning_consistency_summary` and `content_favorites` labels are pre-localized via `modules/localization/`.

## 22. RTL
N/A (backend).

## 23. Analytics
`monthly_family_report_viewed` fired client-side (K-05).

## 24. Performance
Single indexed lookup on `monthly_family_report` by `family_id`, p95 within Report NFR.

## 25. Security
Aggregate-only schema is the primary control preventing sibling comparison (FR-8) — enforced by a dedicated structural test, not just a code-review convention.

## 26. Library Requirements
No new dependencies.

## 27. Testing
1. Unit test: successful retrieval of the latest passing report.
2. Unit test: parent not belonging to `family_id` rejected with `403`.
3. Unit test: no report generated yet returns `report_available: false`, not an error.
4. Unit test: fallback to last passing report when the latest failed content-safety validation.
5. **Structural test:** assert `MonthlyFamilyReportResponse` has no field shaped as a per-child array/list of child-keyed objects.
6. Integration test: full request through the gate.

## 28. Documentation
OpenAPI docstring explicitly noting the aggregate-only, no-sibling-comparison contract.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define MonthlyFamilyReportResponse Schema**
- Task ID: B05-T01
- Objective: Aggregate-only Pydantic schema.
- Why This Is Required: FR-8's structural enforcement point for this report type.
- Existing Architecture to Follow: `NoorHeroesBaseModel`.
- Existing Files to Reuse: `schemas.py` base; C.20's `monthly_family_report` table columns.
- Files to Create: none.
- Files to Modify: `schemas.py`.
- Implementation Details: Fields per §13, deliberately excluding any per-child structure.
- Business Rules: FR-8.
- Validation: N/A.
- Error Handling: N/A.
- Security: No per-child comparison field declared.
- Performance: N/A.
- Localization: Pre-localized fields.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered by Task 03's structural test.
- Documentation: Docstring citing FR-8.
- Dependencies: none.
- Do Not Change: C.20's `monthly_family_report` table.
- Expected Result: Schema importable.
- Definition of Done: Matches §13, no per-child field present.

**Task 02 — Implement get_monthly_family_report Service Method and Route**
- Task ID: B05-T02
- Objective: Retrieve latest passing report with fallback and not-yet-available handling.
- Why This Is Required: Core read logic.
- Existing Architecture to Follow: C.20's read-API fallback pattern.
- Existing Files to Reuse: `FamilyRepository`.
- Files to Create: none.
- Files to Modify: `service.py`, `api.py`.
- Implementation Details: Per §10.
- Business Rules: FR-6, FR-8.
- Validation: Family-membership check.
- Error Handling: Per §18.
- Security: Family-membership enforcement.
- Performance: Indexed lookup.
- Localization: Pre-localized fields passed through.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 03.
- Documentation: Docstring.
- Dependencies: Task 01, C.20 B-04/B-05.
- Do Not Change: `AIReportGenerationService` internals.
- Expected Result: Endpoint returns correct report or not-available state.
- Definition of Done: Fallback and not-available paths both verified.

**Task 03 — Write Test Suite Including Structural No-Sibling-Comparison Test**
- Task ID: B05-T03
- Objective: Cover §27, with the structural test as a CI-blocking gate.
- Why This Is Required: FR-8 enforcement verification.
- Existing Architecture to Follow: pytest + reflection-based field scanning.
- Existing Files to Reuse: Family/parent fixtures.
- Files to Create: `test_monthly_family_report_api.py`, `test_monthly_family_report_no_sibling_comparison_structural.py`.
- Files to Modify: none.
- Implementation Details: 6 test cases per §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert exact responses.
- Security: Structural test is critical.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test docstrings.
- Dependencies: Tasks 01–02.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 green, structural test CI-blocking.

## 30. Definition of Done
`GET /v1/parent/reports/{family_id}/monthly-family` live, gated by family-membership, aggregate-only response schema verified structurally, fallback behavior verified, all tests green.

## 31. Final Verification Checklist
- [ ] Structural test confirms no per-child comparison array field
- [ ] Family-membership check verified (not child-ownership)
- [ ] Content-safety fallback to last passing report verified
- [ ] Not-yet-available state verified for a family with no generated report
- [ ] OpenAPI docs state the aggregate-only contract explicitly
