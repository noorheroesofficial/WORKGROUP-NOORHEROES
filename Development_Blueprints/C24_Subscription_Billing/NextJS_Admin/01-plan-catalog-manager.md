# N-01 — Plan Catalog Manager

## 1. Feature Context
Admin CRUD surface for plan definitions (pricing, child capacity, included features) — the write side of B-01's public, cached `GET /api/v1/billing/plans` read endpoint. Part of the Admin Portal's "Commerce" navigation group. **Note:** E.33 (Subscription Management & Billing Ops) is the canonical, fully-detailed admin specification; this blueprint implements C.24's own ownership sketch (§8) and should be reconciled against E.33's exact field/screen detail during implementation.

## 2. Parent Feature
Feature C.24 — Subscription & Billing

## 3. Sub-feature
3.1 Plan Catalog Manager (ID: **N-01**)

## 4. Objective
Build a `product_admin`/`commerce_admin`-restricted CRUD interface for plan definitions, ensuring every mutation invalidates B-01's Redis cache and never retroactively affects existing subscribers' entitlements.

## 5. Business Requirements
- §8 Admin Requirements: Plan Catalog Manager — full CRUD, changes drive `GET /api/v1/billing/plans`'s cached response.
- Deactivating a plan never affects existing subscribers' entitlements — only new subscribers are affected (cross-ref E.33 §1.2 "plan/entitlement changes never retroactively affect already-existing subscribers").
- Every mutating action writes an immutable `audit_log` row.

## 6. Existing Architecture
`src/features/subscriptions-admin/` (or `commerce/`, per the Admin Portal's existing "Commerce" nav-group convention — confirm exact feature-folder naming against E.33's implementation before diverging). Layering: UI Components → React Query Hooks → Repository/`BaseResourceClient` → `apiClient` → Backend REST API, per `NEXT-JS-INSTRUCTIONS.md` §2.

## 7. Existing Code to Reuse
- `src/shared/components/require-permission.tsx::RequirePermission`
- `src/lib/api-client.ts::apiClient`
- `src/shared/components/data-table.tsx` (or equivalent existing table component) for the plan list view
- Existing form/validation pattern (Zod schemas + form component) used elsewhere in the Admin Portal

## 8. Files to Create
- `src/features/commerce/api/plan-catalog-repository.ts` — `PlanCatalogRepositoryImpl` (CRUD methods)
- `src/features/commerce/hooks/use-plan-catalog.ts` — list/create/update/deactivate React Query hooks
- `src/features/commerce/components/plan-catalog-table.tsx`
- `src/features/commerce/components/plan-form-dialog.tsx`
- `src/app/(dashboard)/commerce/plans/page.tsx`

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add plan CRUD endpoint constants
- Admin Portal sidebar navigation config — add "Plan Catalog" under Commerce, `RequirePermission`-gated

## 10. NextJS Requirements
- `usePlanCatalog()`: query hook listing all plans (active + deactivated, admin view shows both, unlike B-01's public active-only response).
- `useCreatePlan()`/`useUpdatePlan()`/`useDeactivatePlan()`: mutation hooks, each invalidating both the local React Query cache and triggering the backend's Redis cache-bust for `billing:plans:catalog`.
- `PlanFormDialog`: Zod-validated form (plan_code, display_name, monthly_price, annual_price, child_capacity, included_features); create vs. edit mode.
- Deactivate is a distinct, non-destructive action (not a delete) — confirmation dialog explicitly states existing subscribers keep their entitlements.
- Every mutation shows a loading state on submit and a clear success/error toast.

## 11. Required API
Plan CRUD endpoints extending B-01 (`GET /api/v1/billing/plans`) with admin-scoped create/update/deactivate mutations — exact contract owned by E.33's backend specification; confirm field names against E.33 before finalizing the Zod schema. **Admin API.**

## 12. Validation
- `plan_code` unique, immutable after creation (changing it would break existing subscriber references).
- `monthly_price`/`annual_price` non-negative; `child_capacity` positive integer.
- `included_features` non-empty for any paid plan.

## 13. Authentication
Existing Admin Portal auth context (Bearer session).

## 14. Authorization
Full CRUD restricted to `product_admin`/`commerce_admin` role, enforced via `RequirePermission` (UI) and server-side role check (authoritative).

## 15. Error Handling
- Duplicate `plan_code` on create → inline field error.
- Deactivate attempt on a plan with active subscribers → allowed (per business rule — existing subscribers unaffected), but confirmation copy makes this explicit.
- Network/API failure → toast error, form state preserved for retry.

## 16. Loading States
Table skeleton while plan list loads; form submit button shows a spinner during mutation.

## 17. Responsive UI
Table adapts to a card layout on narrow viewports, consistent with existing Admin Portal table responsive patterns.

## 18. Accessibility
Form fields properly labeled, keyboard-navigable; table sortable/filterable via accessible controls.

## 19. Localization
Admin Portal is typically EN-only for internal tooling (confirm against `NEXT-JS-INSTRUCTIONS.md`'s localization scope for admin-facing surfaces before assuming otherwise).

## 20. Testing
- Unit: `usePlanCatalog`/`useCreatePlan`/`useUpdatePlan`/`useDeactivatePlan` hook success/error branches.
- Component: form validation (duplicate plan_code, negative price, etc.).
- Integration: full create → list-refresh → cache-invalidation-triggers-B-01-refresh flow against a mocked backend.
- RBAC: non-`commerce_admin` users see the nav item hidden/disabled and cannot reach the page directly (route-guard test).

## 21. AI Coding Agent Implementation Steps

**Task 01 — Implement `PlanCatalogRepositoryImpl`**
Objective: typed CRUD API client. Files to Create: `plan-catalog-repository.ts`. Dependencies: backend plan-CRUD endpoints live (E.33).

**Task 02 — Implement React Query Hooks**
Objective: list/create/update/deactivate hooks with cache invalidation. Files to Create: `use-plan-catalog.ts`. Dependencies: Task 01.

**Task 03 — Implement `PlanCatalogTable` & `PlanFormDialog`**
Objective: list view + create/edit form UI. Files to Create: both component files. Dependencies: Task 02.

**Task 04 — Wire Page Route & Navigation**
Objective: `/commerce/plans` page, `RequirePermission`-gated nav entry. Files to Create/Modify: page file, sidebar nav config. Dependencies: Task 03.

**Task 05 — Add Full Test Suite**
Objective: coverage per §20. Dependencies: Tasks 01–04.

## 22. Definition of Done
`product_admin`/`commerce_admin` roles can fully manage the plan catalog through a validated form and table UI, with every mutation invalidating B-01's cache and never retroactively affecting existing subscribers, fully audited.

## 23. Final Verification Checklist
- [ ] Plan mutations invalidate B-01's Redis cache correctly
- [ ] Deactivation confirmed non-retroactive for existing subscribers (confirmation copy explicit)
- [ ] `commerce_admin`/`product_admin` role enforced both client- and server-side
- [ ] Every mutation writes an audit_log row
- [ ] Duplicate plan_code rejected with clear inline error
