# N-01 — Web Portal Allowlist Monitor (Read-Only)

## 1. Feature Context
Part of Feature D.27's Admin Requirements (§8). The one addition D.27 makes to the existing `noorheroes-admin` NextJS Admin Portal: a read-only visibility page confirming, in production, that the structural CORS/route exclusion built in B-01/B-02 is actually holding — a security-health signal, not a management tool.

## 2. Parent Feature
D.27 Parent Web Account Portal (`account.noorheroes.com`)

## 3. Sub-feature
**N-01 — Web Portal Allowlist Monitor (Read-Only)**

## 4. Objective
Build a strictly read-only `noorheroes-admin` page displaying the live gateway/middleware allowlist configuration for the `account.noorheroes.com` origin and a paginated log of rejected out-of-allowlist requests, gated to `product_admin`/`trust_safety`/`security` roles, with zero mutating capability anywhere on the page.

## 5. Business Requirements
- §8 Admin Requirements: "Web Portal Origin/Route Allowlist Monitor (Read-only): Visibility into the gateway's CORS/route-allowlist configuration for this origin, and any rejected-request attempts from it targeting an out-of-scope route."
- §8 CRUD permissions: "Read-only behind `product_admin`/`trust_safety`/`security` role; the allowlist configuration itself is a deployment/infrastructure artifact, not an admin-UI-editable resource."
- §9 Admin AI Code-Generation Prompt: "sourced directly from the live gateway configuration, not a separately-maintained admin-entered copy... This page has NO edit capability."

## 6. Existing Architecture
Built inside the existing `noorheroes-admin` codebase, following `NEXT-JS-INSTRUCTIONS.md`'s established layering exactly: UI Component → Custom React Query Hook → Repository/`BaseResourceClient` → `apiClient` → Backend REST API. Reuses `DashboardShell`, `RequirePermission`, `DataTable`, `EmptyState`, `ErrorView`, `LoadingState` — no new layout or table primitive is introduced. This page is read-only by construction, mirroring the structural-mutation-guard pattern already used elsewhere in sibling admin blueprints (e.g. C.21 N-01, C.26 N-03) via `never` generics on `BaseResourceClient`'s create/update/delete type parameters.

## 7. Existing Code to Reuse
- `BaseResourceClient` (extended with `never` generics on create/update/delete — read-only by structural guarantee, not just by omission).
- `DataTable`, `EmptyState`, `ErrorView`, `LoadingState`, `RequirePermission`, `DashboardShell` (`src/shared/components/`).
- `useAdminSession()` for role/permission context.
- `usePaginationState` for the rejected-requests log table.
- `hasPermission(admin, permission)` utility for the RBAC check.

## 8. Files to Create
- `src/features/web-portal-monitor/api/web-portal-monitor-client.ts`
- `src/features/web-portal-monitor/api/schemas.ts`
- `src/features/web-portal-monitor/hooks/use-web-portal-allowlist.ts`
- `src/features/web-portal-monitor/hooks/use-web-portal-rejected-requests.ts`
- `src/app/(dashboard)/security/web-portal-monitor/page.tsx`

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `API_ENDPOINTS.WEB_PORTAL_MONITOR.ALLOWLIST`, `API_ENDPOINTS.WEB_PORTAL_MONITOR.REJECTED_REQUESTS`, pointing at B-04's `GET /v1/admin/web-portal-monitor/allowlist` and `GET /v1/admin/web-portal-monitor/rejected-requests`.
- Sidebar navigation (`DashboardShell`'s nav config) — add "Web Portal Monitor" under a Security section, wrapped in `RequirePermission`.

## 10. Backend Requirements
Consumes B-04 exclusively: `GET /v1/admin/web-portal-monitor/allowlist`, `GET /v1/admin/web-portal-monitor/rejected-requests`.

## 11. KMP Requirements
Not applicable.

## 12. NextJS Requirements
- `WebPortalMonitorClient extends BaseResourceClient<..., never, never, RejectedRequestFilters>` — `never` generics on create/update, structurally preventing any mutation code from ever being written against this resource (mirrors C.21 N-01/C.26 N-03's established pattern in this codebase).
- Page layout: an "Allowlist" panel (static-ish table of `{method, path, owningFeature}`, refetched per the header's existing Reload convention — no client-side caching beyond React Query's standard staleTime) and a "Rejected Requests" panel (paginated `DataTable` of `{route, origin, occurredAt}`).
- Empty state: "No rejected requests in this range" when the log is empty — this is the expected, healthy state, and the page's copy should reflect that framing (an empty rejected-requests log is good news, not a missing-data problem).
- `RequirePermission permission="web-portal-monitor:read"` — confirm/add to the `AdminPermission` catalog, mapped to backend `product_admin`/`trust_safety`/`security` scopes.
- No form, no create/edit modal, no delete action anywhere on this page — verified structurally (via the `never` generics) and by a negative UI test.

## 13. API Contract
Consumes B-04's contract as documented in that blueprint (`GET /v1/admin/web-portal-monitor/allowlist`, `GET /v1/admin/web-portal-monitor/rejected-requests`).

## 14. Database Requirements
Not applicable.

## 15. Validation
Pagination parameters only (`page`, `limit`) on the rejected-requests query — no other user-editable input exists on this page.

## 16. Authentication
`useAdminSession()`.

## 17. Authorization
`RequirePermission permission="web-portal-monitor:read"`, restricted to `product_admin`/`trust_safety`/`security` per PRD §8. Backend enforcement (B-04) is the authoritative gate; this is the UI-level companion, never relied upon alone.

## 18. Error Handling
- `QueryErrorState` on allowlist or rejected-requests fetch failure, with retry.
- `EmptyState` for zero rejected requests (framed as healthy/expected, not an error).
- `LoadingState` on initial fetch.
- If the allowlist source is unavailable (B-04's `503`), display a clear "live configuration unavailable" message — never fall back to a stale cached allowlist presented as current.

## 19. Offline First
Not applicable (admin web app).

## 20. Local Data
Not applicable.

## 21. Localization
Table headers, empty-state copy, and page title via `useTranslation()`; timestamps via `useFormatters()`.

## 22. RTL
Full RTL layout including table column order.

## 23. Analytics
Not specified in the PRD; this page is itself a security-observability surface rather than a product-analytics-instrumented one.

## 24. Performance
Low-traffic, admin-only page; standard `DataTable` pagination, no special optimization required given expected data volume (rejected requests should be rare by design).

## 25. Security
- Structural read-only guarantee via `never` generics — the same pattern already established and tested in this codebase for comparable monitor-only pages (C.21 N-01, C.26 N-03).
- No mutating network call exists anywhere in this feature's code — verified by a negative test scanning for any POST/PATCH/DELETE call in the `web-portal-monitor` feature directory.
- Displays only route/origin/timestamp metadata — never request bodies or credentials, consistent with B-04's redaction guarantee.

## 26. Library Requirements
No new libraries — reuses the existing `DataTable`, React Query, and Zod validation stack already used throughout `noorheroes-admin`.

## 27. Testing
- Unit: `WebPortalMonitorClient` Zod schema validation for both endpoints.
- Integration/UI: allowlist panel renders correctly from fixture data.
- Integration/UI: rejected-requests table paginates correctly.
- Integration/UI: empty state renders with the "healthy" framing when zero rejected requests exist.
- Negative test: no POST/PATCH/DELETE network call exists anywhere in this feature's code (structural read-only verification).
- Integration/UI: `RequirePermission` correctly restricts access to `product_admin`/`trust_safety`/`security`.

## 28. Documentation
Document on the page itself (or adjacent help text) that an empty rejected-requests log is the expected, healthy state, and that this page has intentionally no edit capability by design, not by omission.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm `AdminPermission` Catalog Entry**
- **Objective:** Add or confirm `web-portal-monitor:read` in the existing permission catalog, mapped to the correct backend roles.

**Task 02 — Resource Client with `never` Mutation Generics**
- **Files to Create:** `web-portal-monitor-client.ts`, `schemas.ts`.

**Task 03 — Query Hooks**
- **Files to Create:** `use-web-portal-allowlist.ts`, `use-web-portal-rejected-requests.ts`.

**Task 04 — Monitor Page**
- **Files to Create:** `page.tsx`.
- **Tests:** the structural read-only negative test.

**Task 05 — Sidebar Navigation Wiring**
- **Files to Modify:** `DashboardShell`'s nav config, gated by `RequirePermission`.

**Task 06 — Localization, RTL, Empty-State Copy**

**Task 07 — Full Test Suite & Documentation**

## 30. Definition of Done
`product_admin`/`trust_safety`/`security` roles can see the live, current CORS/route allowlist for `account.noorheroes.com` and any rejected out-of-allowlist attempts, on a page with zero mutating capability, structurally guaranteed via `never` generics and a negative test.

## 31. Final Verification Checklist
- [ ] `never` generics used for create/update/delete
- [ ] No POST/PATCH/DELETE call exists anywhere in this feature's code (negative test passes)
- [ ] Allowlist panel sourced from the live configuration, not a stale/hand-maintained copy
- [ ] `RequirePermission` correctly restricts to `product_admin`/`trust_safety`/`security`
- [ ] Empty rejected-requests state framed as healthy, not an error
- [ ] Full localization and RTL verified
