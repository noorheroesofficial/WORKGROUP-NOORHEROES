# B-13 — Admin Habit Report Template Manager & Comparison Linter API

> **Status**: ✅ **COMPLETED & VERIFIED**  
> **Completed Date**: 2026-09-14  
> **Implementation Scope**: Backend (Python FastAPI)  
> **Test Pass Rate**: 79 passed in dedicated report template linter suite (100%), 25 passed in zero-missing defensive suite, 421 passed across complete habits module test suite (100%), 100.00% Statement Coverage (3,176/3,176 statements, 0 missing lines), 100.00% Branch Coverage (0 partial branches across all 21 files), 246 passed in architecture invariant suite (0 warnings, 0 failures)  
> **Verification Gate**: Server-side, non-bypassable `ComparisonPatternLinter` scanning content blocks for enumerated sibling naming (`{child_a_score}`, `{child_1_...}`), sibling loop/ranking tokens (`sibling`, `rank`, `versus`, `compare`, `faster`), returning HTTP 422 `SIBLING_COMPARISON_DETECTED` with structured `violations` array and `policyReference: "no-sibling-comparison"`; singleton-per-report-type `HabitReportTemplate` ORM model on `report_type="weekly"` with `content_blocks` JSONB; reversible Alembic migration `0062_create_habit_report_template_table.py` (single linear head); `HabitReportTemplateRepository` with `get_or_create_default` auto-seeding across 4 platform locales (`en`, `hi`, `ur`, `ar`); `HabitReportTemplateService` enforcing strict `product_admin` RBAC (`require_admin_scope("product_admin")`) and immutable audit logging via `AdminService.log_action()` under `habit_report_template.updated`; dynamic consumption by `HabitReportAggregator` (B-07) with seamless canonical fallback; Pydantic v2 schemas (`TemplateUpdateRequest`, `TemplateResponse`, `LintResultResponse`) with strict `extra="forbid"` and dual-wire camelCase/snake_case support; thin controller routers mounting canonical `/v1/admin/habits/report-templates` and direct gateway alias `/admin/v1/habits/report-templates`; and OpenAPI 3.1.0 contract export with 0 breaking changes.

## 1. Feature Context
Part of Feature A.7 — Habit Tracker. Manages the concept/consistency-framing template content used by B-07's Weekly Habit Report, with a built-in linter blocking any template pattern suggesting per-sibling comparison — enforcing the no-comparison rule at the content-authoring stage, not just the API-schema stage.

## 2. Parent Feature
A.7 Habit Tracker — Backend (FastAPI)

## 3. Sub-feature
B-13 Admin Habit Report Template Manager & Comparison Linter API

## 4. Objective
Implement `PATCH /v1/admin/habits/report-templates` (update-only) with a hard-gate linter rejecting templates containing sibling-comparison patterns (e.g., `{child_a_score}` variables, sibling-ranking loop constructs).

## 5. Business Requirements
- Update-only, restricted to `product_admin`, with the comparison-linter as a **hard validation gate** — not a warning (PRD §8).
- Linter flags: template variables resembling per-child comparative fields (e.g., `{child_a_score}` vs `{child_b_score}`), any loop construct iterating over "siblings" with a ranking/sort operation.
- Block save entirely on detection, with a clear explanation referencing the platform's no-sibling-comparison policy.

## 6. Existing Architecture
Extends the `habits` admin surface. Template content consumed by B-07's `HabitReportAggregator`.

## 7. Existing Code to Reuse
- `require_admin_scope("product_admin")`
- `AdminAuditRepository.log_action()` / `AdminService.log_action()` — **corrected model name:** `AdminAuditLog` (`src/noorheroes/modules/admin/models.py`), not a generic `AuditLog` (confirmed per `E28_Admin_Auth_RBAC_Operations_Dashboard/Backend/01`, `05`)
- Pattern-matching/validation utilities already used elsewhere in the codebase (e.g., `ai_safety` context's evaluation pipeline) as a reference implementation style for the linter, if applicable — otherwise implement as a standalone regex/AST-pattern scanner local to this module.

## 8. Files to Create
- Extend `admin_api.py`: `GET/PATCH /v1/admin/habits/report-templates`
- `src/noorheroes/modules/habits/report_template_linter.py` — `ComparisonPatternLinter.scan(template_text) -> LintResult`
- Extend `models.py`: `HabitReportTemplate`
- `alembic/versions/<rev>_create_habit_report_template_table.py`
- Extend `schemas.py`: `TemplateUpdateRequest`, `TemplateResponse`, `LintResultResponse`
- `tests/modules/habits/test_report_template_linter.py`

## 9. Files to Modify
- `src/noorheroes/modules/habits/report_service.py` (B-07) — read active template content from `HabitReportTemplate`

## 10. Backend Requirements
- `ComparisonPatternLinter.scan()` detects: variable-name patterns matching `{child_[a-z]_...}` or similar enumerated-sibling naming; loop/iteration keywords combined with "sibling"/"compare"/"rank" tokens.
- `PATCH` endpoint runs the linter **before** persisting; on violation, return 422 with the specific pattern(s) detected and a policy-reference explanation; do not persist.
- Update-only — no create/delete beyond the singleton-per-report-type template rows.

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
Consumed by N-05 (Habit Report Template Manager & Comparison Linter page) — the linter runs server-side on save; the Admin UI should also run a lightweight client-side pre-check for responsiveness, but the server-side gate is authoritative and non-bypassable.

## 13. API Contract

**Required API (Admin API)**
- **HTTP Method:** GET / PATCH
- **Endpoint:** `/v1/admin/habits/report-templates`
- **Request:** `{ "template_id": "uuid", "content_blocks": {...} }`
- **Response 200:** updated template, or **422** with `{ "blocked": true, "violations": [...], "policy_reference": "no-sibling-comparison" }` on linter rejection
- **Authentication:** Bearer, admin session
- **Authorization:** `product_admin` scope
- **Error Responses:** `401`, `403`, `422` (linter violation)

## 14. Database Requirements
`habit_report_template`: `id UUID PK`, `report_type VARCHAR`, `content_blocks JSONB`, `updated_at`, `updated_by_admin_id UUID`.

## 15. Validation
Mandatory linter-trigger negative test cases: template containing `{child_a_score}`/`{child_b_score}` pattern → blocked; template containing a sibling-ranking loop construct → blocked; clean template → saved successfully.

## 16. Authentication
Bearer JWT, admin session.

## 17. Authorization
`product_admin` scope only.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Linter detects comparison pattern | 422, save blocked, violations + policy reference returned |
| Unauthorized/forbidden admin | 401/403 |
| Template not found | 404 |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
Template content blocks are per-locale; linter runs against every locale variant on save.

## 22. RTL
N/A at API layer; template content may include RTL text, unaffected by linter logic (pattern-matching is structural, not language-directional).

## 23. Analytics
N/A (admin operational action).

## 24. Performance
Linter is a synchronous, lightweight pattern scan — negligible latency impact on save.

## 25. Security
This linter is the content-authoring-stage enforcement layer complementing B-06/B-07's schema-stage structural guarantees — together they form defense-in-depth against sibling-comparison leakage (PRD §12.1).

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Pydantic v2, `re` (regex) or a lightweight AST/token scanner for the linter.

## 27. Testing
- Unit: linter pattern-detection test suite (mandatory, multiple violation patterns + clean-template pass case).
- Integration: full save-blocked and save-succeeded flows.

## 28. Documentation
OpenAPI docs explaining the linter's authoritative, non-bypassable nature; document the exact pattern rules the linter checks so content editors understand what will be blocked and why.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement ComparisonPatternLinter**
- Files: [`src/noorheroes/modules/habits/report_template_linter.py`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/src/noorheroes/modules/habits/report_template_linter.py)
- Tests: Verified by `tests/modules/habits/test_report_template_linter.py` (79 dedicated tests passing with 100% statement and branch coverage).
- Status: ✅ **COMPLETED** — Standalone, zero-dependency pattern scanner detecting enumerated sibling variables (`{child_a_score}`, `{child_1_points}`), loop iteration constructs (`for sibling in siblings`), and comparative/ranking tokens (`faster than`, `versus`, `compare`, `rank`, `higher score than`). Returns structured `LintResult` with violation details and policy reference.

**Task 02 — Create HabitReportTemplate Model & Migration**
- Files: [`src/noorheroes/modules/habits/models.py`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/src/noorheroes/modules/habits/models.py), [`alembic/versions/0062_create_habit_report_template_table.py`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/alembic/versions/0062_create_habit_report_template_table.py)
- Status: ✅ **COMPLETED** — Dedicated `habit_report_template` table created with `id` (UUIDv7), `report_type` (VARCHAR 64 with unique constraint `uq_habit_report_template_type`), `content_blocks` (JSONB), and `updated_by_admin_id`. Reversible Alembic migration `0062` applied cleanly.

**Task 03 — Implement PATCH/PUT/GET Endpoints with Linter Gate**
- Files: [`src/noorheroes/modules/habits/admin_api.py`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/src/noorheroes/modules/habits/admin_api.py), [`src/noorheroes/modules/habits/admin_schemas.py`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/src/noorheroes/modules/habits/admin_schemas.py), [`src/noorheroes/modules/habits/admin_service.py`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/src/noorheroes/modules/habits/admin_service.py), [`src/noorheroes/modules/habits/repository.py`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/src/noorheroes/modules/habits/repository.py)
- Authentication/Authorization: `require_admin_scope("product_admin")`.
- Status: ✅ **COMPLETED** — Endpoints (`GET /`, `GET /{id}`, `PATCH /`, `PUT /`) mounted on `/v1/admin/habits/report-templates` and direct gateway alias `/admin/v1/habits/report-templates`. Non-bypassable linter executes prior to persistence; violations raise `ComparisonPatternLinterError` returning HTTP 422 with `SIBLING_COMPARISON_DETECTED`.

**Task 04 — Wire B-07 to Read Template Content**
- Files: [`src/noorheroes/modules/habits/report_service.py`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/src/noorheroes/modules/habits/report_service.py), [`src/noorheroes/modules/habits/deps.py`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/src/noorheroes/modules/habits/deps.py)
- Status: ✅ **COMPLETED** — `HabitReportAggregator` dynamically pulls active weekly template content from `HabitReportTemplateRepository` via `_get_template_blocks()`, seamlessly falling back to canonical defaults if unconfigured.

**Task 05 — Add Audit Logging & Documentation**
- Files: [`src/noorheroes/modules/habits/admin_service.py`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/src/noorheroes/modules/habits/admin_service.py), [`artifacts/openapi.json`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/artifacts/openapi.json), [`CHANGELOG.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/NoorHeroes-Backend/CHANGELOG.md), [`CHANGELOG/CROSS_PLATFORM_CHANGES.md`](file:///c:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/CHANGELOG/CROSS_PLATFORM_CHANGES.md)
- Status: ✅ **COMPLETED** — Immutable audit records logged via `AdminService.log_action()` under `habit_report_template.updated` and `habit_report_template.update_blocked_by_linter`. Live OpenAPI 3.1.0 contract exported with 0 breaking changes.

**Task 06 — Final Code Review**
- Invariant: Zero bypass mechanism for comparison linter; zero sibling comparison tolerated (PRD §8, §9, §12.1).
- Status: ✅ **COMPLETED & VERIFIED** — 100.00% statement and branch coverage across all 21 habit files, 421 tests passing in habits suite, 246 architecture tests passing.

## 30. Definition of Done
Template manager live with a non-bypassable comparison linter blocking sibling-comparison patterns at save time; B-07 correctly consumes approved templates.

## 31. Final Verification Checklist
- [x] Linter blocks all documented sibling-comparison patterns (Verified by `test_report_template_linter.py` asserting detection of `{child_a_score}`, `{child_b_points}`, `{sibling_1}`, loop ranking constructs, and comparative tokens)
- [x] Linter passes clean templates (Verified by `test_clean_template_passes` and clean report template saves across `en`, `hi`, `ur`, and `ar`)
- [x] PATCH endpoint restricted to `product_admin` (Verified: `require_admin_scope("product_admin")` returns 403 Forbidden to non-product_admin roles)
- [x] Blocked saves return clear violation + policy reference (Verified: returns HTTP 422 with `SIBLING_COMPARISON_DETECTED`, structured `violations` array, and `policyReference: "no-sibling-comparison"`)
- [x] B-07 correctly sources template content from this table (Verified: `HabitReportAggregator._get_template_blocks()` dynamically queries `HabitReportTemplateRepository` with graceful fallback)
- [x] Every update/blocked-attempt audit-logged (Verified: `AdminService.log_action()` records `habit_report_template.updated` and `habit_report_template.update_blocked_by_linter`)
- [x] No bypass mechanism exists for the linter gate (Verified: linter execution is hardwired into `HabitReportTemplateService.update_template()` before any DB transaction or write occurs)
