# Blueprint: FAQ Content Management

## 1. Feature Context
Platform: NoorHeroes Admin Portal (Next.js 15 App Router, TypeScript, TanStack Query, Zod). This is a genuinely new admin surface — no existing feature owns `faq_article`/`faq_feedback` CRUD (confirmed via project-wide search: not present in E.28–E.34, not present in any existing `Development_Blueprints` folder, and distinct from the generic `cms_pages` table referenced in the platform's master screen catalog for unrelated static content).

## 2. Parent Feature
C.25 — Notifications (Parent) & Support.

## 3. Sub-feature
N-01 — FAQ Content Management.

## 4. Objective
Build a CRUD admin page for `faq_article` (list, create, edit, publish/unpublish) gated behind `content_editor`, with an admin-visible "helpful" feedback-rate signal per article to support self-serve-effectiveness content-gap identification.

## 5. Business Requirements
Source: PRD §1.7 FR-10; §1.8 Self-Serve Effectiveness ("admin tooling supporting content-gap identification from search-then-ticket patterns"); §4.2.
- FAQ content is admin-authored and, "scholar-reviewed where Islamic-content-adjacent" (FR-10) — this admin surface is the authoring point for content later served read-only by B-03.
- `faq_article.published` gates public visibility — an admin must be able to author a draft and publish only when ready.
- Self-serve effectiveness is measured via the FAQ self-serve resolution rate metric (§1.4: target ≥50%), "with admin tooling supporting content-gap identification from search-then-ticket patterns" — this page's helpful-rate display is this feature's concrete admin-tooling contribution to that goal.

## 6. Existing Architecture
Per `NEXT-JS-INSTRUCTIONS.md`: strict layering UI Component → Custom React Query Hook → Repository/`BaseResourceClient` → `apiClient` → Backend REST API; `RequirePermission` for RBAC; `DataTable`/`FilterPanel`/`SearchBar` for list pages; `EmptyState`/`ErrorView`/`LoadingState`/`QueryErrorState` for standard states; `useTranslation()`/`useFormatters()` for localization; `CmsRepositoryImpl` (existing, for the unrelated `cms_pages` table) as a structural reference for how a content-CRUD repository is typically built in this codebase, even though this is a distinct table/feature.

## 7. Existing Code to Reuse
- `BaseResourceClient<TEntity, TCreate, TUpdate, TFilters>` — extend for `FaqArticleResourceClient`, implementing the full CRUD set (`list`, `get`, `create`, `update`, `delete`/archive-via-`published=false`).
- `DataTable`, `FilterPanel`, `SearchBar`, `StatusBadge`, `EmptyState`, `ErrorView`, `LoadingState`, `QueryErrorState`, `ConfirmationDialog` (`src/shared/components/`).
- `RequirePermission` for RBAC guarding.
- `usePaginationState`, `useDebouncedValue`.
- `useTranslation()`, `useFormatters()`.
- `API_ENDPOINTS` registry pattern (`src/shared/constants/api-endpoints.ts`) — add `SUPPORT.FAQ_ARTICLES`.
- `CmsRepositoryImpl`'s general shape as a structural style reference (not a shared implementation — this is a distinct table).

## 8. Files to Create
- `src/features/faq-content/api/faq-article.client.ts` (extends `BaseResourceClient`)
- `src/features/faq-content/api/faq-article.schema.ts` (Zod schemas)
- `src/features/faq-content/hooks/use-faq-articles.ts`
- `src/features/faq-content/hooks/use-faq-article-mutations.ts` (create/update/publish-toggle)
- `src/features/faq-content/components/faq-article-table.tsx`
- `src/features/faq-content/components/faq-article-form.tsx`
- `src/features/faq-content/components/faq-feedback-rate-badge.tsx`
- `src/app/(dashboard)/faq-articles/page.tsx`
- `src/app/(dashboard)/faq-articles/[id]/page.tsx` (edit)
- `src/app/(dashboard)/faq-articles/new/page.tsx` (create)
- `src/features/faq-content/__tests__/faq-article-management.test.tsx`

## 9. Files to Modify
- `src/shared/constants/api-endpoints.ts` — add `SUPPORT.FAQ_ARTICLES` endpoint constant.
- `src/shared/components/dashboard-shell.tsx` (or sidebar nav config) — add "FAQ Content" nav entry under a Support/Content group, guarded by `RequirePermission`.
- `AdminPermission` type — add `faq_articles:read`/`faq_articles:write` (or the platform's exact permission-string convention) if not already present.

## 10. NextJS Requirements
- `FaqArticleResourceClient extends BaseResourceClient<FaqArticle, FaqArticleCreateInput, FaqArticleUpdateInput, FaqArticleQueryFilters>` — full CRUD (list, get, create, update; "delete" implemented as a `published=false` update rather than a hard delete, consistent with B-03's retention model where unpublished content is retained, not destroyed).
- `useFaqArticles(filters)` list hook; `useFaqArticle(id)` detail hook; `useCreateFaqArticle()`/`useUpdateFaqArticle()`/`useTogglePublish()` mutation hooks.
- List page: `FilterPanel` (locale filter, published/draft filter) + `SearchBar` + `DataTable` (columns: title, locale, published `StatusBadge`, updated_at, helpful-rate badge) + pagination.
- Create/edit form: title, body (rich-text or plain textarea per platform's existing content-editing convention — confirm against `CmsRepositoryImpl`'s associated form component before choosing a new rich-text library; do not add a new dependency if an existing content-editing pattern already covers this), locale selector (reusing `LanguageSelector`/existing locale value set), published toggle with a `ConfirmationDialog` on publish (since publishing makes content live to all parents/pre-subscription users).
- Scholar-review gate: if the platform has an existing content-review-workflow status field/component (confirm against E.29's Content CMS/Scholar Review Workflow feature before inventing a parallel one — FAQ content that is "Islamic-content-adjacent" per FR-10 should route through whatever review mechanism E.29 already established, rather than this blueprint building a second, divergent review workflow). Flag this integration point explicitly for confirmation before implementation rather than assuming a specific mechanism.
- Wrap the page/nav-entry in `<RequirePermission permission="faq_articles:read">` (list) and gate mutation controls behind `faq_articles:write`.

## 11. KMP Requirements
N/A.

## 12. Files/Screens
FAQ Content list page, create page, edit page — three routes under `(dashboard)/faq-articles/`.

## 13. API Contract
**Resolved by `Backend/05-admin-faq-content-management-api.md` (B-05)** — the gap flagged at this blueprint's original generation is now closed.
- **List:** `GET /v1/admin/support/faq?locale=&published=&page=&limit=` → `{ items: [ { article_id, title, body, locale, published, updated_at } ], total, page, limit, totalPages }`
- **Create:** `POST /v1/admin/support/faq` → `{ title, body, locale, published? }` (defaults `published:false`)
- **Detail:** `GET /v1/admin/support/faq/{id}` (returns regardless of `published` state, unlike B-03's public endpoint)
- **Update:** `PATCH /v1/admin/support/faq/{id}` → partial `{ title?, body?, locale?, published? }`
- **Feedback summary:** `GET /v1/admin/support/faq/{id}/feedback-summary` → `{ helpful_count, unhelpful_count, total_count }`
- **Auth:** Bearer admin session + `content_editor` scope (B-05 §17 — confirm exact scope string against the platform's live scope taxonomy before hardcoding).
- **Admin API:** Yes.

## 14. Database Requirements
N/A (frontend only; backend owns `faq_article`/`faq_feedback` persistence per B-03).

## 15. Validation
Zod schema (`faq-article.schema.ts`) validates title (non-empty, length-bounded), body (non-empty), locale (against the platform's `SupportedLanguage` code set), published (boolean) — reject/error on shape mismatch from the API rather than silently rendering malformed data, per platform convention.

## 16. Authentication
Standard Admin Portal session (`useAdminSession()`), no new auth mechanism.

## 17. Authorization
`RequirePermission` guarding both the nav entry and the page routes (`faq_articles:read` for viewing, `faq_articles:write` for create/edit/publish) — backend independently enforces this via RBAC scope (coordinate exact permission-string naming with whichever backend endpoint ultimately implements this, per §13's flagged gap).

## 18. Error Handling
- `QueryErrorState` on list/detail fetch failure with retry.
- `EmptyState` when no FAQ articles exist yet ("No FAQ articles yet — create your first one").
- Form validation errors surfaced inline per field via Zod/react-hook-form (or the platform's existing form-handling convention — confirm against an existing create/edit form, e.g. any Settings form, before choosing a form library).
- Publish-toggle failure → error toast/inline message, published state does not optimistically flip until confirmed.

## 19. Offline First
N/A — standard web app behavior.

## 20. Local Data
N/A — React Query cache only, no `localStorage` persistence.

## 21. Localization
All admin UI chrome copy via `useTranslation()`; the FAQ article's own `body`/`title` content is itself the multi-locale data being managed (one row per `locale` per logical FAQ topic, per B-03's schema) — the admin form itself may benefit from a locale-switcher within the edit view if managing translations of the "same" FAQ topic across locales is a workflow requirement; confirm this UX pattern (separate rows vs. a single multi-locale-tab form) against Figma/product intent before assuming one over the other, since B-03's schema (`locale` as a plain column, not a translation-group FK) suggests separate independent rows per locale is the simpler, schema-accurate default.

## 22. RTL
Admin Portal's RTL support scope is unconfirmed (NEXT-JS-INSTRUCTIONS.md documents no explicit Arabic/Urdu admin locale) — treat as N/A unless confirmed otherwise, and explicitly note this rather than assuming Admin Portal RTL support exists.

## 23. Analytics
N/A — internal admin tool, not a tracked end-user analytics surface (consistent with C.20's N-01 precedent for internal monitoring pages).

## 24. Performance
Standard `DataTable` server-side pagination avoids loading the full FAQ article history at once; React Query caching avoids redundant refetches within its stale-time window.

## 25. Security
- `RequirePermission` client-side guard is UX only; the actual security boundary is server-side RBAC enforcement on the (to-be-defined) admin FAQ endpoints.
- Publish action requires `faq_articles:write` — a read-only admin must never be able to make draft content publicly visible.
- No PII in this data model (FAQ content is generic help content, not user data).

## 26. Library Requirements
No new dependencies unless a rich-text editor is genuinely required and none exists in the codebase yet (confirm against existing content-editing forms first, per §10's note, before adding one).

## 27. Testing
1. Unit test: `FaqArticleResourceClient.list()`/`.create()`/`.update()` correctly call their endpoints and validate responses via Zod.
2. Unit test: list page renders `DataTable` with correct columns including the helpful-rate badge.
3. Unit test: `RequirePermission` blocks access for admins without `faq_articles:read`/`write`, shows fallback.
4. Unit test: create/edit form validation rejects empty title/body.
5. Unit test: publish-toggle requires confirmation via `ConfirmationDialog` before making a draft article live.
6. Unit test: empty state renders when no articles exist.
7. Unit test: error state renders with retry on API failure.

## 28. Documentation
Component-level JSDoc noting this is the authoring surface for content B-03 serves read-only, and the flagged dependency on the not-yet-fully-specified admin FAQ API contract (§13).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement API Endpoint Constant and Zod Schema Against B-05's Confirmed Contract**
- Task ID: N01-T01
- Objective: Type-safe, validated contract matching B-05 exactly.
- Why This Is Required: B-05 (`Backend/05-admin-faq-content-management-api.md`) now defines the authoritative admin FAQ contract — this task wires the frontend to it precisely, with no further guessing.
- Existing Architecture to Follow: `API_ENDPOINTS` registry; existing Zod schema patterns.
- Existing Files to Reuse: `src/shared/constants/api-endpoints.ts`.
- Files to Create: `faq-article.schema.ts`.
- Files to Modify: `api-endpoints.ts`.
- Implementation Details: `GET/POST /v1/admin/support/faq`, `GET/PATCH /v1/admin/support/faq/{id}`, `GET /v1/admin/support/faq/{id}/feedback-summary` per B-05 §13 exactly, including the `feedback-summary` endpoint this task's original scope had not anticipated.
- Business Rules: Must match B-05's `AdminFaqArticleResponse`/`FaqFeedbackSummaryResponse` shapes exactly.
- Validation: This IS the validation layer.
- Error Handling: N/A.
- Security: N/A.
- Performance: N/A.
- Localization: `locale` field validated against `SupportedLanguage`.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: JSDoc citing B-05.
- Dependencies: B-05 (implemented).
- Do Not Change: Do not modify unrelated endpoint constants.
- Expected Result: Schema and endpoint constants available.
- Definition of Done: Contract matches B-05's actual response shapes exactly.

**Task 02 — Build FaqArticleResourceClient and React Query Hooks**
- Task ID: N01-T02
- Objective: Full CRUD data-access layer.
- Why This Is Required: Platform's strict layering requirement.
- Existing Architecture to Follow: `BaseResourceClient`, existing hook patterns.
- Existing Files to Reuse: `BaseResourceClient`, `apiClient`.
- Files to Create: `faq-article.client.ts`, `use-faq-articles.ts`, `use-faq-article-mutations.ts`.
- Files to Modify: none.
- Implementation Details: Full CRUD; "delete" maps to a `published=false` PATCH, not a hard DELETE call.
- Business Rules: Retention model — never hard-delete FAQ content via this UI.
- Validation: Via Task 01's Zod schema.
- Error Handling: Standard `apiClient`/`parseApiError` handling.
- Security: N/A (client layer; backend is the real boundary).
- Performance: React Query caching/stale-time per platform defaults.
- Localization: N/A (data layer).
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: JSDoc.
- Dependencies: Task 01.
- Do Not Change: Do not modify `BaseResourceClient` itself.
- Expected Result: Hooks return/mutate data correctly.
- Definition of Done: Matches §10.

**Task 03 — Build List, Create, and Edit Pages with RBAC Guard**
- Task ID: N01-T03
- Objective: Visual delivery, RBAC-restricted, including the publish-confirmation flow.
- Why This Is Required: Core deliverable.
- Existing Architecture to Follow: `DataTable`, `FilterPanel`, `RequirePermission`, `ConfirmationDialog`, existing directory-page pattern (`NEXT-JS-INSTRUCTIONS.md` §11 Pattern 1).
- Existing Files to Reuse: `DataTable`, `FilterPanel`, `SearchBar`, `EmptyState`, `ErrorView`, `LoadingState`, `RequirePermission`, `ConfirmationDialog`, `usePaginationState`, `useDebouncedValue`, `useTranslation`, `useFormatters`.
- Files to Create: `faq-article-table.tsx`, `faq-article-form.tsx`, `faq-feedback-rate-badge.tsx`, `page.tsx` (list), `[id]/page.tsx` (edit), `new/page.tsx` (create).
- Files to Modify: `dashboard-shell.tsx` (nav entry), `AdminPermission` type.
- Implementation Details: Per §10; publish-toggle wrapped in `ConfirmationDialog`.
- Business Rules: FR-10.
- Validation: Via form + Zod.
- Error Handling: Per §18.
- Security: `RequirePermission` guard on both read and write actions distinctly.
- Performance: N/A.
- Localization: All copy via `useTranslation()`.
- RTL: N/A per §22 (flagged, not assumed).
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: Component comment per §28.
- Dependencies: Task 02.
- Do Not Change: Do not modify unrelated pages/nav entries.
- Expected Result: Pages render correctly, RBAC-gated.
- Definition of Done: Matches §10, §18.

**Task 04 — Write Test Suite**
- Task ID: N01-T04
- Objective: Cover §27.
- Why This Is Required: Standard coverage, notably the publish-confirmation and RBAC guards.
- Existing Architecture to Follow: Existing test conventions (React Testing Library/Jest or platform's chosen framework).
- Existing Files to Reuse: Existing test utilities/mocks for `apiClient`, `useAdminSession`.
- Files to Create: `faq-article-management.test.tsx`.
- Files to Modify: none.
- Implementation Details: All 7 cases from §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: N/A.
- Security: RBAC and publish-confirmation tests are security-relevant.
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
FAQ Content Management (list/create/edit/publish) live, RBAC-restricted to `content_editor`/`faq_articles:write`, publish action confirmation-gated, helpful-rate signal visible per article, all tests green — pending backend confirmation of the admin FAQ API contract flagged in §13.

## 31. Final Verification Checklist
- [ ] Admin FAQ API contract matches B-05's implementation exactly (including `feedback-summary`)
- [ ] `RequirePermission` correctly restricts read vs. write actions separately
- [ ] Publish action requires explicit confirmation
- [ ] "Delete" maps to `published=false`, never a hard delete
- [ ] Zod schema matches the confirmed backend contract exactly
- [ ] Nav entry itself is permission-guarded, not just the page route
- [ ] Scholar-review-workflow integration point confirmed against E.29 (or explicitly deferred) rather than a divergent workflow invented here
