# Blueprint: Report Content-Safety Audit Log — Extended Scope

## 1. Feature Context
Platform: NoorHeroes Admin Portal (Next.js 15 App Router, TypeScript, TanStack Query, Zod). Extends C.20's existing Content-Safety Audit Log page (C.20 N-01, `01-ai-report-content-safety-audit-log.md`) to cover C.22's deeper report types.

## 2. Parent Feature
C.22 — Per-Child Reports.

## 3. Sub-feature
N-02 — Report Content-Safety Audit Log (Extended Scope).

## 4. Objective
Widen C.20 N-01's existing `ContentSafetyAuditLogResourceClient`/filter scope to include Safety Report, Monthly Family Report, AI Insight Report, and skill drill-down validation events, without duplicating a second audit log page.

## 5. Business Requirements
Source: PRD §8 ("Report Content-Safety Audit Log (Read-only): Shared with C.20's existing page, extended in scope"), §12.9 Security Checklist.
- Read-only table with filtering/sorting/pagination by report type, child, date, `content_safety_passed` status.
- Restricted to `trust_safety`/`ai_ops` roles (shared with C.20).
- No mutating actions exposed on this page — strictly read-only, `ContentSafetyAuditLogResourceClient` remains list-only (C.20 N-01 §10 already implements or throws on `create`/`update`/`delete`).

## 6. Existing Architecture
This is **not** a new page — it is a scope extension to the exact existing page delivered in C.20 N-01, at:
- `src/features/content-safety-audit/api/content-safety-audit-log.client.ts` (extends `BaseResourceClient`, list-only)
- `src/features/content-safety-audit/api/content-safety-audit-log.schema.ts` (Zod schemas)
- `src/features/content-safety-audit/hooks/use-content-safety-audit-log.ts` (React Query hook)
- `src/features/content-safety-audit/components/content-safety-audit-log-table.tsx`
- `src/app/(dashboard)/content-safety-audit-log/page.tsx`

This blueprint's job is to widen that page's `report_type` filter enum and the underlying Zod schema/query to include C.22's report types, reusing 100% of the existing component tree, `RequirePermission` guard, and `DataTable`/`FilterPanel` wiring.

## 7. Existing Code to Reuse
- The entire existing page component tree listed in §6 — reused as-is, modified in place, not duplicated.
- `RequirePermission` (permission string per C.20 N-01 §7 — the same `trust_safety`/`ai_ops` string, unchanged by this extension).
- `usePaginationState`, `useDebouncedValue`, `DataTable`, `FilterPanel`, `SearchBar`, `StatusBadge`, `EmptyState`, `ErrorView`, `LoadingState`, `QueryErrorState`.

## 8. Files to Create
- `src/features/content-safety-audit/__tests__/extended-report-types.test.tsx`

## 9. Files to Modify
- `src/features/content-safety-audit/api/content-safety-audit-log.schema.ts` — widen the `report_type` Zod enum to add `safety_report`, `monthly_family_report`, `ai_insight_report`, `skill_drilldown` alongside C.20's existing `weekly_report` (and any other pre-existing values)
- `src/features/content-safety-audit/components/content-safety-audit-log-table.tsx` (or a co-located `ReportTypeFilter` sub-component, per C.20 N-01's actual internal structure) — add the four new filter options to the report-type `FilterPanel` control
- `src/features/content-safety-audit/api/content-safety-audit-log.client.ts` — confirm the underlying `list()` call already passes through the widened `report_type` filter value to the query string without modification (it should, since C.20 N-01's client is filter-value-agnostic); no client logic change expected, verification only

## 10. Backend Requirements
N/A — consumes C.20 B-06's existing `GET /v1/admin/dashboard/content-safety-audit-log` endpoint (per C.20 N-01 §13's confirmed contract). If that endpoint's `report_type` query-param validation does not yet accept C.22's four additional values, that is a small backend-side enum-widening item owned by extending `modules/dashboard`'s existing audit-log query (C.20 B-06), not a new backend service — flag it if found during Task 02's verification rather than silently working around it client-side.

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
- Widen `content-safety-audit-log.schema.ts`'s `report_type` Zod enum.
- Add the four new options to the existing `FilterPanel` report-type control.
- `DataTable` columns remain unchanged from C.20 N-01 (masked child ID, report type, `generated_at`, failure-reason tag) — no new columns required, only new filterable/displayable `report_type` values.
- Confirm no mutating action is exposed anywhere on this page for any report type, old or new — `ContentSafetyAuditLogResourceClient` stays list-only.

## 13. API Contract
Reuses C.20 B-06's existing endpoint, per `API_ENDPOINTS.DASHBOARD.CONTENT_SAFETY_AUDIT_LOG` → `GET /v1/admin/dashboard/content-safety-audit-log`, response shape `{ items: AuditLogEntry[], next_cursor, has_more }` (C.20 N-01 §13), with the `report_type` query parameter's accepted values widened to include C.22's four additional report types.

## 14. Database Requirements
N/A — reuses C.20's existing audit-log table/view, which should already capture every report type generated through the shared `AIReportGenerationService`/`ContentSafetyValidator` (including C.22's types, since Backend B-04/B-05/B-06 all reuse that same service). No new table.

## 15. Validation
`report_type` filter value validated against the widened Zod enum client-side; invalid/unrecognized values ignored/reset to "all" rather than erroring the page.

## 16. Authentication
Reused from C.20 N-01's existing page (`useAdminSession()`), unchanged.

## 17. Authorization
`RequirePermission` with the same `trust_safety`/`ai_ops` permission string as C.20 N-01 — unchanged by this extension; Backend B-06 independently enforces RBAC server-side.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| New report-type filter value not yet recognized by the backend | `QueryErrorState` or empty result set rather than a page-level crash, until the backend-side enum widening (if needed per §10) ships |
| Standard list/pagination errors | Unchanged from C.20 N-01's existing `QueryErrorState`/`ErrorView` handling |

## 19. Loading States
Unchanged from C.20 N-01's existing `LoadingState`/`DataTable` skeleton behavior.

## 20. Empty States
Unchanged from C.20 N-01's existing `EmptyState` ("No content-safety issues detected" or equivalent calm, factual copy) — generic enough to cover the new report types without modification.

## 21. Pagination
Unchanged from C.20 N-01's existing `usePaginationState` + cursor-based `{ items, next_cursor, has_more }` consumption.

## 22. Filtering
Extended `report_type` filter values per §9/§12; existing child/date/`content_safety_passed` filters unchanged and apply uniformly across old and new report types.

## 23. Sorting
Unchanged from C.20 N-01's existing `DataTable` column sorting.

## 24. Responsive UI
Unchanged from C.20 N-01's existing page.

## 25. Accessibility
Unchanged from C.20 N-01's existing page; new filter options inherit the same accessible `FilterPanel` control pattern.

## 26. Localization
New filter option labels (e.g., "Safety Report," "Monthly Family Report," "AI Insight Report," "Skill Drill-down") added to the existing translation namespace C.20 N-01 already uses for its report-type labels, resolved via `useTranslation()`.

## 27. Testing
1. Unit test: the widened `report_type` Zod schema accepts all four new values alongside C.20's existing ones, and still rejects genuinely invalid values.
2. Unit test: `FilterPanel` renders all four new options.
3. Unit test: selecting a new report-type filter correctly passes the expected query parameter to `content-safety-audit-log.client.ts`'s `list()` call.
4. Integration test: `DataTable` correctly displays rows for each of C.22's report types when present in the API response.
5. **Read-only verification test:** confirm no mutating UI control (edit/delete/approve button) exists anywhere on the page for any report type, old or new.
6. Regression test: C.20's existing `weekly_report` filtering/display continues to work unchanged.

## 28. Documentation
Update the existing page's component-level TSDoc to note the widened `report_type` scope and reference this blueprint alongside C.20 N-01.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Widen the report_type Zod Enum and Filter Options**
- Task ID: N02-T01
- Objective: Add C.22's four report types to the existing schema and filter control.
- Why This Is Required: PRD §8's explicit scope-extension requirement.
- Existing Architecture to Follow: C.20 N-01's existing `content-safety-audit-log.schema.ts` and its `FilterPanel` integration.
- Existing Files to Reuse: The entire existing component/schema, modified in place.
- Files to Create: none.
- Files to Modify: `content-safety-audit-log.schema.ts`, `content-safety-audit-log-table.tsx` (or its `ReportTypeFilter` sub-component).
- Implementation Details: Add `safety_report`, `monthly_family_report`, `ai_insight_report`, `skill_drilldown` to the Zod enum and the filter's option list.
- Business Rules: PRD §8.
- Validation: Zod schema rejects genuinely invalid values while accepting all now-eight (or however many) valid ones.
- Error Handling: Unrecognized values handled gracefully per §18.
- Security: N/A (read-only extension).
- Performance: N/A.
- Localization: New labels added to the existing translation namespace.
- RTL: Inherited from existing component.
- Analytics: N/A.
- Tests: Covered in Task 03.
- Documentation: Updated component TSDoc.
- Dependencies: none.
- Do Not Change: C.20 N-01's existing filter values/behavior for `weekly_report` and any other pre-existing types.
- Expected Result: Filter includes all report types across C.20 and C.22.
- Definition of Done: All four new options render and function correctly, Zod validation covers them.

**Task 02 — Verify Backend Endpoint Coverage for New Report Types**
- Task ID: N02-T02
- Objective: Confirm C.20 B-06's existing `GET /v1/admin/dashboard/content-safety-audit-log` endpoint already returns rows for C.22's report types without modification.
- Why This Is Required: This page must not silently show incomplete data if the backend hasn't been confirmed to cover the new types.
- Existing Architecture to Follow: C.20 B-06's existing audit-log query, sourcing from the shared `AIReportGenerationService`/`ContentSafetyValidator` write path used by Backend B-04, B-05, B-06 of this feature.
- Existing Files to Reuse: none (verification task, not implementation).
- Files to Create: none.
- Files to Modify: none, unless a genuine backend gap is found (§10), in which case flag it explicitly rather than silently working around it client-side.
- Implementation Details: Manual/automated verification that rows for `safety_report`, `monthly_family_report`, `ai_insight_report`, and skill drill-down validation events appear via the existing endpoint.
- Business Rules: PRD §8, §3.5 (mandatory content-safety gate, no parallel path).
- Validation: N/A.
- Error Handling: N/A.
- Security: Confirms no report type bypasses the shared audit trail.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 03 (integration test).
- Documentation: Note findings in this blueprint's implementation notes.
- Dependencies: Backend B-04, B-05, B-06 must be live.
- Do Not Change: N/A.
- Expected Result: Confirmed data coverage, or a flagged gap.
- Definition of Done: Verification complete and documented.

**Task 03 — Write Test Suite**
- Task ID: N02-T03
- Objective: Cover §27.
- Why This Is Required: QA coverage for the scope extension, including regression protection for C.20's existing functionality.
- Existing Architecture to Follow: Existing Jest/React Testing Library conventions used by C.20 N-01's own test file.
- Existing Files to Reuse: C.20 N-01's existing test fixtures for the audit-log page.
- Files to Create: `extended-report-types.test.tsx`.
- Files to Modify: none.
- Implementation Details: 6 test cases per §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert graceful handling.
- Security: Read-only verification test is important (prevents future accidental mutating-action additions).
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test comments.
- Dependencies: Tasks 01–02.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 green, including the C.20 regression test.

## 30. Definition of Done
C.20 N-01's existing `report_type` Zod enum/filter widened to include all four of C.22's report types, backend data coverage verified, page remains strictly read-only via the unchanged list-only `ContentSafetyAuditLogResourceClient`, C.20's existing functionality unaffected, all tests green.

## 31. Final Verification Checklist
- [ ] All four new report types selectable in `FilterPanel` and correctly queried via `content-safety-audit-log.client.ts`
- [ ] Backend data coverage for new report types verified against C.20 B-06's existing endpoint (or gap explicitly flagged)
- [ ] Page remains strictly read-only — `ContentSafetyAuditLogResourceClient` still implements no mutating methods
- [ ] C.20's existing `weekly_report` filtering continues to work unchanged (regression-tested)
- [ ] `trust_safety`/`ai_ops` `RequirePermission` scope unchanged and still enforced
- [ ] New filter labels correctly localized via `useTranslation()`
