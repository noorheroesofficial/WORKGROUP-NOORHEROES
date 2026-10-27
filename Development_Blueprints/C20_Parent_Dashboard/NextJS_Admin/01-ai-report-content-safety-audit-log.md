# Blueprint: AI Report Content-Safety Audit Log

## 1. Feature Context
Platform: NoorHeroes Admin Portal (Next.js 15 App Router, TypeScript, TanStack Query, Zod). This is the single admin-facing surface introduced by C.20 — a read-only monitoring page, zero mutating capability.

## 2. Parent Feature
C.20 — Parent Dashboard.

## 3. Sub-feature
N-01 — AI Report Content-Safety Audit Log.

## 4. Objective
Build a read-only, paginated, filterable admin page listing reports that failed the Content Safety Validator (B-05), restricted to `trust_safety`/`ai_ops` roles, for model-quality monitoring only — no edit/approve-anyway/override capability anywhere.

## 5. Business Requirements
Source: PRD §8, §9.
- Paginated table of `weekly_report`/`ai_insight_report` rows where `content_safety_passed = false`.
- Show masked child identifier, report type, `generated_at`, validator-failure-reason tag.
- MODEL-QUALITY MONITORING ONLY — no edit, approve-anyway, or override capability.
- Restricted to `trust_safety`/`ai_ops` roles.
- No audit_log writes needed for this page (no mutating actions exist).

## 6. Existing Architecture
Per `NEXT-JS-INSTRUCTIONS.md`: strict layering UI Component → Custom React Query Hook → Repository/`BaseResourceClient` → `apiClient` → Backend REST API. `RequirePermission` component for RBAC guarding, `DataTable` for paginated tables, `useAdminSession()` for role/permission context, `FilterPanel`/`SearchBar` for list-page headers, `EmptyState`/`ErrorView`/`LoadingState`/`QueryErrorState` for standard list states, `useTranslation()`/`useFormatters()` for localization/date formatting.

## 7. Existing Code to Reuse
- `BaseResourceClient` — extend for a new `ContentSafetyAuditLogResourceClient` (list-only; do not implement `create`/`update`/`delete` methods, or override them to throw/no-op if the base class requires implementing the full interface).
- `DataTable`, `FilterPanel`, `SearchBar`, `StatusBadge`, `EmptyState`, `ErrorView`, `LoadingState`, `QueryErrorState` (`src/shared/components/`).
- `RequirePermission` for RBAC guarding — **verified real usage**: `permission` is a plain `string` prop (no `AdminPermission` enum type exists in the codebase; `noorheroes-admin/src/features/auth/hooks/use-admin-session.ts` defines `AdminClaims.permissions: string[]` and `hasPermission(admin, permission: string)` as free-form string matching, confirmed by the real usage `<RequirePermission permission="content:write">` in `src/app/(dashboard)/content/page.tsx`). Use `permission="content-safety-audit:read"` — the exact same string as the backend's confirmed `require_admin_scope("content-safety-audit:read")` (B-06), keeping frontend/backend permission strings aligned by construction.
- `usePaginationState`, `useDebouncedValue` for table state management.
- `useTranslation()`, `useFormatters()` for all display copy and date formatting.
- `API_ENDPOINTS` registry pattern — **verified real structure** (`src/shared/constants/api-endpoints.ts`): a flat `export const API_ENDPOINTS = { CONTENT: {...}, QUESTIONS: {...}, ... } as const` object; no `DASHBOARD` key exists yet. Add `DASHBOARD: { CONTENT_SAFETY_AUDIT_LOG: "/v1/admin/content-safety-audit-log" }` (path corrected — per B-06's confirmed real route living directly under the existing `AdminRouter`'s `/v1/admin` prefix, not a separate `/v1/admin/dashboard/...` path).

## 8. Files to Create
- `src/features/content-safety-audit/api/content-safety-audit-log.client.ts` (extends `BaseResourceClient`, list-only)
- `src/features/content-safety-audit/api/content-safety-audit-log.schema.ts` (Zod schemas)
- `src/features/content-safety-audit/hooks/use-content-safety-audit-log.ts` (React Query hook)
- `src/features/content-safety-audit/components/content-safety-audit-log-table.tsx`
- `src/app/(dashboard)/content-safety-audit-log/page.tsx`
- `src/features/content-safety-audit/__tests__/content-safety-audit-log.test.tsx`

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `DASHBOARD: { CONTENT_SAFETY_AUDIT_LOG: "/v1/admin/content-safety-audit-log" }` to the existing flat `API_ENDPOINTS` object (real structure confirmed — see §7), alongside the existing `CONTENT`/`QUESTIONS`/`MEDIA`/`REVIEWS`/`QURAN_PROPOSALS`/`REWARD_RULES` keys
- `src/shared/components/dashboard-shell.tsx` (or sidebar nav config) — add nav entry, guarded by `RequirePermission`

## 10. NextJS Requirements
- `ContentSafetyAuditLogResourceClient extends BaseResourceClient<AuditLogEntry, never, never, AuditLogQueryFilters>` — implements only `list(filters, signal)`; `create`/`update`/`delete` either unimplemented (if `BaseResourceClient` allows partial implementation) or explicitly throw a "not supported" error, defensively preventing any future accidental mutating call.
- `useContentSafetyAuditLog(filters)` React Query hook wrapping `.list()`.
- Page component: `FilterPanel` (report-type filter with values `weekly_report`/`ai_insight_report` — full table names, matching C.22 N-02's already-written extension of this exact page, which widens this same enum to add `safety_report`/`monthly_family_report`/`skill_drilldown`; date-range filter) + `SearchBar` if applicable + `DataTable` (columns: masked child ID, report type, generated_at, failure-reason tag badge) + pagination via `usePaginationState`.
- Wrap the entire page/nav-entry in `<RequirePermission permission="content-safety-audit:read">` — plain string, matching backend's confirmed `require_admin_scope("content-safety-audit:read")` (B-06) exactly; no `AdminPermission` enum type exists in this codebase (confirmed — `permission` is a free-form `string` prop, see §7), so no type needs updating.
- Zero mutating UI elements anywhere on this page — no edit buttons, no "approve" actions, no delete/dismiss controls.

## 11. KMP Requirements
N/A.

## 12. Files/Screens
Single admin page: AI Report Content-Safety Audit Log (list view only, no detail/edit sub-routes). **Confirmed to be the exact page C.22 N-02 (`Development_Blueprints/C22_Per_Child_Reports/NextJS_Admin/02-report-content-safety-audit-log-extended-scope.md`, already written) extends in place** — that blueprint explicitly names every file this blueprint creates (§8/§9 of this document) as the page it widens, validating this file-path/component structure end-to-end.

## 13. API Contract
- **HTTP Method:** GET
- **Endpoint:** per `API_ENDPOINTS.DASHBOARD.CONTENT_SAFETY_AUDIT_LOG` → backend's `/v1/admin/content-safety-audit-log` (B-06, path corrected — lives on the existing `AdminRouter`'s `/v1/admin` prefix, not `/v1/admin/dashboard/...`)
- **Auth:** Bearer admin session (handled transparently by `apiClient`)
- **Response:** `{ items: AuditLogEntry[], next_cursor, has_more }` per B-06 §13 contract; `report_type` values are full table names (`weekly_report`, `ai_insight_report`, ...)
- **Admin API:** Yes.

## 14. Database Requirements
N/A (frontend only; backend owns persistence via B-04/B-05/B-06).

## 15. Validation
Zod schema validates the API response shape (`content-safety-audit-log.schema.ts`) per platform's "Repository validates responses using Zod schemas" convention — reject/error on shape mismatch rather than silently rendering malformed data.

## 16. Authentication
Standard Admin Portal session (`useAdminSession()`), access token in memory, refresh via existing `httpOnly` cookie flow — no new auth mechanism.

## 17. Authorization
`RequirePermission permission="content-safety-audit:read"` guard restricting both the nav entry and the page route itself (the `trust_safety`/`ai_ops` PRD role language maps onto this one confirmed permission/scope string; E.28's future RBAC matrix grants it to both roles) — backend (B-06) independently enforces this via `require_admin_scope("content-safety-audit:read")`, per platform's "Do NOT bypass RequirePermission... ensure backend endpoints enforce permissions" principle (client-side guard is UX, not the security boundary).

## 18. Error Handling
- `QueryErrorState` on API failure with retry.
- `EmptyState` when no failed reports exist ("No content-safety issues detected" or similar calm, factual copy — not alarming).
- `RequirePermission`'s `fallback` prop renders an access-denied state for admins without the required role, rather than a raw 403 error page.

## 19. Offline First
N/A — Admin Portal is not an offline-first surface (standard web app behavior, React Query's default retry/cache policy suffices).

## 20. Local Data
N/A (React Query cache only, no persistent local storage per platform's zero-token/zero-localStorage-persistence principle — this applies to auth tokens specifically, but the same caution applies broadly; use React Query's in-memory cache, not `localStorage`).

## 21. Localization
All display copy (column headers, empty-state text, filter labels) via `useTranslation()`; dates via `useFormatters().formatDate()`.

## 22. RTL
Admin Portal's existing RTL support (if the platform's admin i18n includes Arabic/Urdu admin locales — confirm against existing localization scope; if Admin Portal is English-only by platform convention, this is N/A and should be explicitly noted as such rather than assumed).

## 23. Analytics
N/A — internal monitoring tool, not a tracked end-user analytics surface (though basic admin-portal-wide usage analytics, if any exist platform-wide, apply uniformly and aren't feature-specific here).

## 24. Performance
Standard `DataTable` pagination (server-side, via cursor) avoids loading the full failed-report history at once; React Query caching avoids redundant refetches on tab-revisit within its stale-time window.

## 25. Security
- Read-only page, zero mutating UI, matching backend's zero-mutating-endpoint guarantee (B-06).
- Masked child identifier displayed as returned by the backend — this page must NOT attempt to "unmask" or cross-reference to reveal the underlying child identity (no client-side lookup added).
- RBAC enforced both client-side (UX) and server-side (actual security boundary, B-06).

## 26. Library Requirements
No new dependencies — uses existing TanStack Query, Zod, existing shared component library.

## 27. Testing
1. Unit test: `ContentSafetyAuditLogResourceClient.list()` correctly calls the endpoint and validates response via Zod.
2. Unit test: page renders `DataTable` with correct columns.
3. Unit test: `RequirePermission` blocks access for admins without `content-safety-audit:read` permission, shows fallback.
4. Unit test: empty state renders when no failed reports exist.
5. Unit test: error state renders with retry on API failure.
6. Unit test: pagination and filters (`report_type`, `date_range`) function correctly.
7. **Structural test:** confirm no mutating UI element (edit/approve/delete button) exists anywhere in the rendered component tree for this page.

## 28. Documentation
Component-level JSDoc/comment noting the read-only, no-override design intent, citing PRD §8/§9.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Add API Endpoint Constant and Zod Schema**
- Task ID: N01-T01
- Objective: Type-safe, validated API contract on the frontend.
- Why This Is Required: Platform convention — all endpoints centrally registered, all responses Zod-validated.
- Existing Architecture to Follow: `API_ENDPOINTS` registry, existing Zod schema patterns (e.g., `paginatedUsersSchema`).
- Existing Files to Reuse: `src/shared/constants/api-endpoints.ts` pattern.
- Files to Create: `content-safety-audit-log.schema.ts`.
- Files to Modify: `api-endpoints.ts`.
- Implementation Details: Zod schema matching B-06 §13 response shape exactly.
- Business Rules: N/A.
- Validation: This IS the validation layer.
- Error Handling: N/A.
- Security: N/A.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: JSDoc.
- Dependencies: B-06's finalized contract.
- Do Not Change: Do not modify unrelated endpoint constants.
- Expected Result: Schema and endpoint constant available.
- Definition of Done: Matches B-06 contract exactly.

**Task 02 — Build ContentSafetyAuditLogResourceClient and React Query Hook**
- Task ID: N01-T02
- Objective: Data-access layer, list-only.
- Why This Is Required: Platform's strict layering requirement.
- Existing Architecture to Follow: `BaseResourceClient`, existing hook patterns (`useFamilyList`, `useUsers`).
- Existing Files to Reuse: `BaseResourceClient`, `apiClient`.
- Files to Create: `content-safety-audit-log.client.ts`, `use-content-safety-audit-log.ts`.
- Files to Modify: none.
- Implementation Details: List-only client; `create`/`update`/`delete` either unimplemented or defensively throwing.
- Business Rules: PRD §9 (no override capability).
- Validation: Via Task 01's Zod schema.
- Error Handling: Standard `apiClient`/`parseApiError` handling.
- Security: List-only enforcement at the client layer as defense-in-depth (backend is the real boundary).
- Performance: React Query caching/stale-time per platform defaults.
- Localization: N/A (data layer).
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: JSDoc.
- Dependencies: Task 01.
- Do Not Change: Do not modify `BaseResourceClient` itself.
- Expected Result: Hook returns paginated data correctly.
- Definition of Done: Matches PRD §9's read-only mandate.

**Task 03 — Build Page and Table Component with RBAC Guard**
- Task ID: N01-T03
- Objective: Visual delivery, RBAC-restricted.
- Why This Is Required: Core deliverable.
- Existing Architecture to Follow: `DataTable`, `FilterPanel`, `RequirePermission`, existing directory-page pattern (`NEXT-JS-INSTRUCTIONS.md` §11 Pattern 1).
- Existing Files to Reuse: `DataTable`, `FilterPanel`, `SearchBar`, `EmptyState`, `ErrorView`, `LoadingState`, `RequirePermission`, `usePaginationState`, `useDebouncedValue`, `useTranslation`, `useFormatters`.
- Files to Create: `content-safety-audit-log-table.tsx`, `page.tsx`.
- Files to Modify: `dashboard-shell.tsx` (nav entry only — no permission-type file to modify, since `permission` is a plain string prop with no backing enum, confirmed in §7/§10).
- Implementation Details: Per §10 above, mirroring the `NEXT-JS-INSTRUCTIONS.md` §11 Pattern 1 example structure exactly (columns, filters, pagination wiring).
- Business Rules: PRD §8, §9.
- Validation: N/A (handled upstream).
- Error Handling: Per §18.
- Security: `RequirePermission` guard; zero mutating elements.
- Performance: N/A.
- Localization: All copy via `useTranslation()`.
- RTL: Per §22.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: Component comment per §28.
- Dependencies: Task 02.
- Do Not Change: Do not modify unrelated pages/nav entries.
- Expected Result: Page renders correctly, RBAC-gated, zero mutating UI.
- Definition of Done: Matches PRD §8/§9 exactly.

**Task 04 — Write Test Suite**
- Task ID: N01-T04
- Objective: Cover §27, notably the structural no-mutating-UI test.
- Why This Is Required: PRD explicitly requires zero override capability, verifiable in code.
- Existing Architecture to Follow: Existing React Testing Library/Jest (or platform's chosen test framework) conventions.
- Existing Files to Reuse: Existing test utilities/mocks for `apiClient`, `useAdminSession`.
- Files to Create: `content-safety-audit-log.test.tsx`.
- Files to Modify: none.
- Implementation Details: 7 cases per §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: N/A.
- Security: RBAC test and no-mutating-UI structural test are security-critical.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test comments.
- Dependencies: Tasks 01–03.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 green.

## 30. Definition of Done
Read-only, paginated, RBAC-restricted AI Report Content-Safety Audit Log page live, zero mutating capability anywhere, all tests green including the structural no-mutating-UI test.

## 31. Final Verification Checklist
- [ ] Zero edit/approve/delete controls anywhere on this page (structural test passing)
- [ ] `RequirePermission permission="content-safety-audit:read"` matches backend's `require_admin_scope("content-safety-audit:read")` exactly
- [ ] `report_type` filter uses full table names (`weekly_report`/`ai_insight_report`), consistent with C.22 N-02's already-written extension of this same page
- [ ] Masked child identifier displayed as-is, no client-side unmasking attempted
- [ ] Zod schema matches B-06's contract exactly
- [ ] All display copy localized, no hardcoded English strings
- [ ] Nav entry itself is permission-guarded, not just the page route
