# Blueprint: AI Safety Event Taxonomy Management

## 1. Feature Context
Platform: NoorHeroes Admin Portal (Next.js 15 App Router, TypeScript, TanStack Query, Zod). Delivers the admin page for CRUD on `ai_safety_event` category definitions and their pre-templated `summary_text` patterns, consuming Backend B-09.

## 2. Parent Feature
C.22 — Per-Child Reports.

## 3. Sub-feature
N-01 — AI Safety Event Taxonomy Management.

## 4. Objective
Build a `content_editor`/`trust_safety`-restricted admin page for full CRUD on the category/template library that governs `ai_safety_event.summary_text` generation, following the Admin Portal's exact established layering (UI Component → React Query Hook → Repository/`BaseResourceClient` → `apiClient` → Backend REST API) rather than a bespoke structure.

## 5. Business Requirements
Source: PRD §8, §9, §12.5.
- CRUD for category definitions and pre-templated `summary_text` patterns.
- Each template field validated to contain only placeholder-style variables from an allowed list — no free-form text injection point.
- Restricted to `content_editor`/`trust_safety` roles.
- Every change writes an `audit_log` row (server-side, per Backend B-09; this page surfaces confirmation of that write, it does not perform it).

## 6. Existing Architecture
Per `NEXT-JS-INSTRUCTIONS.md` §2/§3: strict layering UI Component → Custom React Query Hook → Repository/`BaseResourceClient` → `apiClient` (`src/lib/api-client.ts`) → Backend REST API. `RequirePermission` component for RBAC guarding (`src/shared/components/`), `DataTable` for paginated tables, `usePaginationState`/`useDebouncedValue` for table state, `FilterPanel`/`SearchBar`/`StatusBadge`/`EmptyState`/`ErrorView`/`LoadingState`/`QueryErrorState` (`src/shared/components/`) for standard list-page states, `useTranslation()`/`useFormatters()` for localization/date formatting, `useAdminSession()` for role/permission context. This blueprint follows the exact same structure C.20 N-01 (Content-Safety Audit Log) already established for an analogous admin list+CRUD page, adding one new feature module rather than a new architectural pattern.

## 7. Existing Code to Reuse
- `BaseResourceClient` — extend for `AiSafetyTaxonomyResourceClient`, this time implementing the full `list`/`get`/`create`/`update` interface (unlike C.20 N-01's list-only client, since this page is genuine CRUD).
- `DataTable`, `FilterPanel`, `SearchBar`, `StatusBadge`, `EmptyState`, `ErrorView`, `LoadingState`, `QueryErrorState` (`src/shared/components/`).
- `RequirePermission` for RBAC guarding — confirm the exact permission string(s) against the `AdminPermission` type; if `content_editor`/`trust_safety`-scoped strings for this specific resource don't yet exist, add them to `AdminPermission` (coordinate the string values with Backend B-09's `require_admin_scope("content_editor")`/`require_admin_scope("trust_safety")` so frontend permission strings and backend scope strings stay consistent, per C.20 N-01's established practice).
- `usePaginationState`, `useDebouncedValue` for table state management.
- `useTranslation()`, `useFormatters()` for all display copy.
- `API_ENDPOINTS` registry (`src/shared/constants/api-endpoints.ts`) — add an `AI_SAFETY.TAXONOMY` entry.
- `useAdminSession()` for role/permission context.

## 8. Files to Create
- `src/features/ai-safety-taxonomy/api/ai-safety-taxonomy.client.ts` (extends `BaseResourceClient`, full CRUD)
- `src/features/ai-safety-taxonomy/api/ai-safety-taxonomy.schema.ts` (Zod schemas)
- `src/features/ai-safety-taxonomy/hooks/use-ai-safety-taxonomy.ts` (React Query list/detail hooks)
- `src/features/ai-safety-taxonomy/hooks/use-ai-safety-taxonomy-mutations.ts` (create/update/disable mutations)
- `src/features/ai-safety-taxonomy/components/ai-safety-taxonomy-table.tsx`
- `src/features/ai-safety-taxonomy/components/ai-safety-taxonomy-form.tsx`
- `src/features/ai-safety-taxonomy/lib/template-placeholder-validator.ts`
- `src/app/(dashboard)/ai-safety-taxonomy/page.tsx` (list)
- `src/app/(dashboard)/ai-safety-taxonomy/new/page.tsx` (create)
- `src/app/(dashboard)/ai-safety-taxonomy/[category]/page.tsx` (edit)
- `src/features/ai-safety-taxonomy/__tests__/ai-safety-taxonomy-form.test.tsx`
- `src/features/ai-safety-taxonomy/__tests__/rbac-enforcement.test.tsx`

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `AI_SAFETY.TAXONOMY` endpoint constant, matching Backend B-09's `/v1/admin/ai-safety/categories` routes
- `src/shared/components/dashboard-shell.tsx` (or sidebar nav config) — add nav entry, guarded by `RequirePermission`

## 10. NextJS Requirements
- `AiSafetyTaxonomyResourceClient extends BaseResourceClient<AiSafetyCategory, AiSafetyCategoryCreateInput, AiSafetyCategoryUpdateInput, AiSafetyCategoryQueryFilters>` — implements `list(filters, signal)`, `get(category, signal)`, `create(input)`, `update(category, input)`, plus a `disable(category)` method for the soft-disable action (Backend B-09's `POST .../disable` doesn't map to a standard REST verb, so this is an explicit extra method on the client, not a shoehorned `update`).
- `useAiSafetyTaxonomyList(filters)` / `useAiSafetyTaxonomyDetail(category)` React Query hooks wrapping `.list()`/`.get()`; `useCreateAiSafetyCategory()` / `useUpdateAiSafetyCategory()` / `useDisableAiSafetyCategory()` mutation hooks, each invalidating the list query cache on success.
- List page: `FilterPanel` (active/inactive filter) + `SearchBar` (category name) + `DataTable` (columns: category, summary_text_template preview, is_active `StatusBadge`, updated_at) + pagination via `usePaginationState`, consuming the cursor-paginated `{ items, next_cursor, has_more }` shape (Backend B-09 §13).
- Create/edit form: React Hook Form + the same Zod schema used for response validation (`ai-safety-taxonomy.schema.ts`), with `template-placeholder-validator.ts` providing live inline validation as the admin types — this client-side check mirrors Backend B-09's server-side placeholder allow-list but is UX-only; the server remains the authoritative boundary.
- Wrap the page/nav-entry/mutating controls in `<RequirePermission permission="...">` per §7's coordinated permission string.
- Confirmation toast after successful save/disable (implicitly confirming the server-side `audit_log` write happened).

## 11. Backend Requirements
N/A — this blueprint is the consumer of Backend B-09, not a backend deliverable itself.

## 12. KMP Requirements
N/A.

## 13. API Contract
**Admin API** (consumed, defined in Backend B-09), reached via `API_ENDPOINTS.AI_SAFETY.TAXONOMY`:
- `GET /v1/admin/ai-safety/categories` → `{ items, next_cursor, has_more }`
- `POST /v1/admin/ai-safety/categories`
- `GET /v1/admin/ai-safety/categories/{category}`
- `PATCH /v1/admin/ai-safety/categories/{category}`
- `POST /v1/admin/ai-safety/categories/{category}/disable`

All calls carry the admin Bearer access token transparently via `apiClient` (in-memory token, `httpOnly` cookie refresh flow — no new auth mechanism).

## 14. Database Requirements
N/A (frontend only; backend owns persistence via Backend B-09).

## 15. Validation
Zod schema (`ai-safety-taxonomy.schema.ts`) validates every API response shape per the platform's "Repository validates responses using Zod schemas" convention — reject/error on shape mismatch rather than silently rendering malformed data. `template-placeholder-validator.ts` provides the client-side placeholder-allow-list check on the form.

## 16. Authentication
Standard Admin Portal session (`useAdminSession()`), access token in memory, refresh via the existing `httpOnly` cookie flow — reused as-is.

## 17. Authorization
`RequirePermission` guards both the nav entry and the page routes (list/create/edit), restricted to the `content_editor`/`trust_safety`-scoped permission string coordinated with Backend B-09's RBAC scopes; per the platform's "Do NOT bypass `RequirePermission`... ensure backend endpoints enforce permissions" principle, this is a UX guard, not the security boundary — Backend B-09 independently enforces RBAC.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Duplicate category on create | Inline form error via the `409` response, "Category already exists" |
| Invalid template (client-side check) | Inline error before submission, submission blocked |
| Invalid template (server rejects despite client pass) | Server `422` surfaced as an inline form error, not a silent failure |
| Unauthorized/forbidden | `RequirePermission`'s `fallback` prop renders an access-denied state, not a raw 403 page |
| Network/API failure | `QueryErrorState` with retry |

## 19. Loading States
`LoadingState`/`DataTable`'s built-in skeleton while the list loads; disabled form with spinner while a mutation is in flight.

## 20. Empty States
`EmptyState`: "No AI safety categories defined yet" with a "New Category" CTA for permitted roles.

## 21. Pagination
`usePaginationState` driving the cursor-based `{ items, next_cursor, has_more }` response shape, consistent with every other admin list page (confirmed via C.20 N-01), not an offset/`page`-based assumption.

## 22. Filtering
`FilterPanel` for `is_active` status; `SearchBar` with `useDebouncedValue` for category-name search (list is expected to stay small; server-side filtering beyond this is a future optimization if the category count grows).

## 23. Sorting
Sortable by `category`, `updated_at`, `is_active` via `DataTable`'s built-in column sorting.

## 24. Responsive UI
`DataTable`'s existing responsive collapse-to-card behavior on narrow viewports, reused as-is.

## 25. Accessibility
Form fields labeled per the platform's existing form-accessibility convention; `DataTable` provides ARIA roles; validation errors announced to screen readers; keyboard-navigable throughout.

## 26. Localization
`useTranslation()`/`useFormatters()` for all UI chrome. The `summary_text_template` **content** itself is data the admin is authoring, not UI chrome — its own multi-locale strategy is a genuinely open cross-feature question (Backend B-09 §21 flags the same gap on the data-model side), not invented here.

## 27. Testing
1. Unit test: create form submits correctly with a valid template.
2. Unit test: `template-placeholder-validator.ts` rejects a disallowed pattern before submission.
3. Unit test: duplicate-category `409` renders correctly as an inline form error.
4. **RBAC test:** roles without the coordinated permission string cannot access the page or see mutating controls; `RequirePermission`'s `fallback` renders.
5. Integration test: full create → edit → disable lifecycle through the UI, verifying cache invalidation after each mutation.
6. Accessibility test: form and table pass automated a11y checks (e.g., axe).

## 28. Documentation
TSDoc on the resource client and hooks; admin-facing help text on the form explaining the placeholder-allow-list constraint in plain language for content editors.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Zod Schemas and AiSafetyTaxonomyResourceClient**
- Task ID: N01-T01
- Objective: Type-safe, response-validated contract matching Backend B-09.
- Why This Is Required: Foundation for the rest of the page, following the platform's mandatory Repository-validates-with-Zod convention.
- Existing Architecture to Follow: `BaseResourceClient`, `apiClient` (`src/lib/api-client.ts`).
- Existing Files to Reuse: `BaseResourceClient`, `API_ENDPOINTS` registry.
- Files to Create: `ai-safety-taxonomy.schema.ts`, `ai-safety-taxonomy.client.ts`.
- Files to Modify: `src/shared/constants/api-endpoints.ts`.
- Implementation Details: Full CRUD client per §10, cursor-paginated list response schema.
- Business Rules: PRD §8.
- Validation: Zod schemas match Backend B-09 §13 exactly.
- Error Handling: `apiClient`'s standard HTTP error handling, reused.
- Security: N/A.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 05.
- Documentation: TSDoc.
- Dependencies: Backend B-09 live.
- Do Not Change: `BaseResourceClient`'s core interface.
- Expected Result: Client/schemas compile and match the contract.
- Definition of Done: Matches Backend B-09 §13 exactly, including the cursor-pagination shape.

**Task 02 — Implement React Query Hooks**
- Task ID: N01-T02
- Objective: List/detail queries plus create/update/disable mutations with cache invalidation.
- Why This Is Required: The platform's mandatory Repository → React Query Hook layering.
- Existing Architecture to Follow: Existing feature-module hook conventions (e.g., C.20 N-01's `use-content-safety-audit-log.ts`).
- Existing Files to Reuse: `usePaginationState`, `useDebouncedValue`.
- Files to Create: `use-ai-safety-taxonomy.ts`, `use-ai-safety-taxonomy-mutations.ts`.
- Files to Modify: none.
- Implementation Details: Per §10.
- Business Rules: PRD §8.
- Validation: N/A.
- Error Handling: React Query's standard error/retry surfaced via `QueryErrorState`.
- Security: N/A.
- Performance: Cache invalidation on mutation success.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 05.
- Documentation: TSDoc.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Hooks correctly wrap the resource client.
- Definition of Done: Cache invalidation verified after each mutation type.

**Task 03 — Implement Table, Form, and Page Components**
- Task ID: N01-T03
- Objective: List page with `DataTable`/`FilterPanel`/`SearchBar`, create/edit form with client-side placeholder validation.
- Why This Is Required: User-facing delivery of this sub-feature.
- Existing Architecture to Follow: `DataTable`, `FilterPanel`, `SearchBar`, `StatusBadge`, `EmptyState`, `ErrorView`, `LoadingState`, `QueryErrorState` (`src/shared/components/`).
- Existing Files to Reuse: All of the above shared components, reused not reimplemented.
- Files to Create: `ai-safety-taxonomy-table.tsx`, `ai-safety-taxonomy-form.tsx`, `template-placeholder-validator.ts`, the three `page.tsx` files.
- Files to Modify: none.
- Implementation Details: Per §10, §19–23.
- Business Rules: PRD §8, §9.
- Validation: `template-placeholder-validator.ts` mirrors Backend B-09's server-side allow-list.
- Error Handling: Per §18.
- Security: Client validation is UX-only; server remains authoritative.
- Performance: N/A.
- Localization: Full `useTranslation()` coverage.
- RTL: Inherited from shared components.
- Analytics: N/A.
- Tests: Covered in Task 05.
- Documentation: TSDoc.
- Dependencies: Task 02.
- Do Not Change: Shared component internals.
- Expected Result: Full CRUD UI functional.
- Definition of Done: Matches §10 exactly.

**Task 04 — Wire RequirePermission RBAC Guard**
- Task ID: N01-T04
- Objective: Restrict page/nav-entry/mutating controls to the coordinated `content_editor`/`trust_safety` permission string.
- Why This Is Required: PRD §8's explicit role restriction.
- Existing Architecture to Follow: `RequirePermission`, `AdminPermission` type, `useAdminSession()`.
- Existing Files to Reuse: `RequirePermission` component.
- Files to Create: none.
- Files to Modify: The three `page.tsx` files, `dashboard-shell.tsx`/sidebar nav config.
- Implementation Details: Coordinate the permission string value with Backend B-09's scope names before hardcoding either side.
- Business Rules: PRD §8.
- Validation: N/A.
- Error Handling: `RequirePermission`'s `fallback` renders access-denied.
- Security: This is a primary UX-layer control (backend remains the actual boundary).
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 05.
- Documentation: TSDoc.
- Dependencies: Task 03.
- Do Not Change: `RequirePermission`'s internals.
- Expected Result: Unauthorized users see a graceful blocked state.
- Definition of Done: Task 05's RBAC test passes.

**Task 05 — Write Test Suite**
- Task ID: N01-T05
- Objective: Cover §27.
- Why This Is Required: QA coverage including RBAC and validation.
- Existing Architecture to Follow: Existing Jest/React Testing Library conventions used by other feature modules (e.g., C.20 N-01's test file).
- Existing Files to Reuse: Existing test fixtures/mocks for admin sessions.
- Files to Create: `ai-safety-taxonomy-form.test.tsx`, `rbac-enforcement.test.tsx`.
- Files to Modify: none.
- Implementation Details: 6 test cases per §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert exact UI states.
- Security: RBAC test is critical.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test comments.
- Dependencies: Tasks 01–04.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 green.

## 30. Definition of Done
AI Safety Event Taxonomy Management page live at `src/app/(dashboard)/ai-safety-taxonomy/`, full CRUD functional via `AiSafetyTaxonomyResourceClient`, client-side placeholder validation mirrors server rules, RBAC restricted via `RequirePermission`, all tests green.

## 31. Final Verification Checklist
- [ ] `AiSafetyTaxonomyResourceClient` extends `BaseResourceClient` with full CRUD, following the platform's exact layering
- [ ] List consumes the cursor-paginated `{ items, next_cursor, has_more }` shape, not an offset/`page` assumption
- [ ] Client-side placeholder validation mirrors Backend B-09's allow-list rules
- [ ] RBAC verified via `RequirePermission`, with the permission string coordinated against Backend B-09's scope names
- [ ] Duplicate-category and invalid-template server errors surface correctly as inline form errors
- [ ] Accessibility checks pass
