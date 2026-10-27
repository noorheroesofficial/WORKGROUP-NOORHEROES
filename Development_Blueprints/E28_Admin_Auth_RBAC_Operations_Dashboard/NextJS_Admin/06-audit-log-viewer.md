# N-06 — Audit Log Viewer

## 1. Feature Context
Part of E.28. Screens #17–18 in PRD §1.18. Read-only, queryable view over the immutable audit trail produced by every Admin module via B-05's `AuditLogService`.

## 2. Parent Feature
E.28 — Admin Portal: Authentication, RBAC & Operations Dashboard

## 3. Sub-feature
N-06 — Audit Log Viewer

## 4. Objective
Build a paginated, filterable (actor/resource/action) Audit Log Viewer and Entry Detail screen, correctly handling the pre-deployment empty-range case (Edge Case 8) without error.

## 5. Business Requirements
- FR-12: audit log immutable, queryable by actor/resource/action.
- Edge Case 8: pre-deployment date-range query returns empty, never an error, with a clear coverage-start indicator.
- §1.19: `audit_log_queried` analytics event.

## 6. Existing Architecture
Builds on the existing `GET /v1/admin/audit-logs` route (already present per the FastAPI instructions manual, hardened by B-05) and the standard `DataTable`/`FilterPanel`/`SearchBar` pattern already used for other admin list pages (e.g., Users, Families).

## 7. Existing Code to Reuse
| Component | Location | Reuse For |
|---|---|---|
| `DataTable` | `src/shared/components/` | Audit log entries table |
| `FilterPanel`, `SearchBar` | `src/shared/components/` | Actor/resource/action filters |
| `usePaginationState` | `src/shared/hooks/` | Cursor/page state |
| `formatDate` / `useFormatters()` | `src/shared/utils/`, `src/shared/hooks/` | `occurred_at` display |

## 8. Files to Create
- `src/app/(dashboard)/platform/audit-logs/page.tsx` — Audit Log Viewer
- `src/app/(dashboard)/platform/audit-logs/[logId]/page.tsx` — Audit Entry Detail
- `src/features/audit-log/components/audit-log-table.tsx`
- `src/features/audit-log/components/audit-entry-detail.tsx`
- `src/features/audit-log/hooks/use-audit-logs.ts`
- `src/features/audit-log/api/audit-log.repository.ts`
- `tests/features/audit-log/audit-log-viewer.test.tsx`

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `AUDIT_LOGS.BASE`

## 10. NextJS Requirements
- Audit Log Viewer: paginated table (actor, resource_type/id, action, occurred_at), filterable by actor/resource/action.
- Audit Entry Detail: full metadata view for a single entry.
- Pre-deployment date-range query: render a clear "No audit data recorded before [coverage-start date]" indicator rather than an empty-looking blank state indistinguishable from a genuine zero-result filter.

## 11. API Contract (Consumed)
`GET /v1/admin/audit-logs?actor=&resource=&action=&cursor=&limit=` (B-05).

## 12. Database Requirements
N/A (frontend).

## 13. Validation
Filter inputs validated client-side (e.g., valid date range) before submission.

## 14. Authentication
Assumes established session.

## 15. Authorization
Role-scoped per resource type (via B-03) — some roles may only query audit entries for resource types relevant to their own scope.

## 16. Error Handling
Standard `QueryErrorState`/`ErrorView` for network/server failures; Edge Case 8's empty-pre-deployment-range is explicitly **not** treated as an error state.

## 17. Offline First
N/A.

## 18. Local Data
None persisted.

## 19. Localization
All labels, resource-type/action display names localized.

## 20. RTL
Table layout and filter panel mirrored correctly for RTL locales.

## 21. Analytics
Fire `audit_log_queried` on each filter/query submission.

## 22. Performance
Cursor-based pagination (matches B-05's keyset pagination), avoiding OFFSET-based performance issues on a large table.

## 23. Security
Read-only surface; no write affordance anywhere in this UI (no "create audit entry" button should ever exist, consistent with B-05's no-client-write guarantee).

## 24. Library Requirements
No new libraries.

## 25. Testing
- Unit: filter combination handling.
- Unit: pre-deployment empty-range rendering (Edge Case 8) — distinct from a genuine zero-result filter state.
- Integration: full audit-log-query flow (per §6.10 Testing Strategy).

## 26. Documentation
None beyond standard component documentation.

## 27. AI Coding Agent Implementation Steps

**Task 01 — Build Audit Log Table & Filters**
- Task ID: N-06-T01
- Files to Create: `audit-log-table.tsx`, `use-audit-logs.ts`, `audit-logs/page.tsx`.
- Implementation Details: `DataTable` + `FilterPanel` for actor/resource/action.
- Dependencies: B-05 endpoint.
- Definition of Done: Table renders, filters apply correctly, pagination functional.

**Task 02 — Build Audit Entry Detail**
- Task ID: N-06-T02
- Files to Create: `audit-entry-detail.tsx`, `[logId]/page.tsx`.
- Dependencies: Task 01.
- Definition of Done: Detail view renders full entry metadata.

**Task 03 — Implement Pre-Deployment Empty-Range Handling**
- Task ID: N-06-T03
- Objective: Edge Case 8 — clear coverage-start indicator, not a generic empty state.
- Files to Modify: `audit-log-table.tsx`.
- Dependencies: Task 01.
- Definition of Done: Distinct rendering verified between genuine zero-result filter and pre-deployment range.

**Task 04 — Localization, RTL, Accessibility Pass**
- Task ID: N-06-T04
- Dependencies: Tasks 01–02.
- Definition of Done: All labels localized; RTL table mirroring verified.

**Task 05 — Full Test Suite**
- Task ID: N-06-T05
- Files to Create: `tests/features/audit-log/audit-log-viewer.test.tsx`.
- Dependencies: Tasks 01–04.
- Definition of Done: All §25 scenarios green.

## 28. Definition of Done
- Audit Log Viewer and Entry Detail live, role-scoped, filterable, paginated.
- Pre-deployment empty-range handled distinctly from a genuine zero-result filter.
- No write affordance exists anywhere in the UI.

## 29. Final Verification Checklist
- [ ] Filters (actor/resource/action) functional
- [ ] Cursor-based pagination working
- [ ] Pre-deployment empty range rendered distinctly (Edge Case 8)
- [ ] No write/create-entry UI affordance exists anywhere
- [ ] `audit_log_queried` analytics fires on query
- [ ] RTL table layout verified
