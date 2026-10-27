# Blueprint: Admin FAQ Content Management API

## 1. Feature Context
Platform: NoorHeroes Backend (FastAPI, Modular Monolith). Extends the `support` bounded context (created in B-03) with the admin-authoring surface for `faq_article`. This blueprint fills a gap C.25's own PRD left unspecified: §3.4's API List documents only the **public-facing** `GET /v1/support/faq*` routes; no admin CRUD contract exists anywhere in C.25, E.28–E.34, or the master screen catalog (confirmed by project-wide search — see N-01's original §13 flag). This blueprint resolves that gap so N-01 (FAQ Content Management, Admin Portal) is implementable.

## 2. Parent Feature
C.25 — Notifications (Parent) & Support.

## 3. Sub-feature
B-05 — Admin FAQ Content Management API.

## 4. Objective
Implement `GET/POST /v1/admin/support/faq` and `GET/PATCH /v1/admin/support/faq/{id}` for admin CRUD over `faq_article`, gated by RBAC, writing to the **exact same table** B-03 serves read-only — no schema fork, no parallel content model.

## 5. Business Requirements
Source: PRD §1.7 FR-10 (admin-authored, scholar-reviewed FAQ content); §1.8 Self-Serve Effectiveness ("admin tooling supporting content-gap identification"); §4.2 (`faq_article`/`faq_feedback` schema); N-01's blueprint (`NextJS_Admin/01-faq-content-management.md`, which this backend blueprint backs).
- FAQ content is admin-authored; publishing an article makes it immediately visible via B-03's public `GET /v1/support/faq` — this endpoint is the sole write path into that table.
- Content that is "Islamic-content-adjacent" is scholar-reviewed per FR-10 — if the platform's existing content-review-workflow (E.29's Content CMS/Scholar Review Workflow) already has a generic review-status mechanism, this endpoint should route through it rather than building a second, divergent review flow (flagged for confirmation in Task 04, consistent with N-01's own flag on this point).
- Deleting FAQ content is never a hard delete — `published=false` retains the historical record (§4.4: "`faq_article.published = false` used to retire content without deleting the historical record of what was once published").
- Feedback aggregation (`faq_feedback`) surfaces per-article "helpful" rate to admins as a content-gap signal — this endpoint exposes that aggregate, it does not let admins edit/delete individual feedback rows (feedback remains append-only and admin-read-only).

## 6. Existing Architecture
Extends B-03's `support` module scaffold exactly (`models.py`/`schemas.py`/`repository.py`/`service.py`/`api.py`, `SupportRouter`). Per `FAST-API-INSTRUCTIONS.md` §5.2 `admin` context: `AdminAuditLog`, `AdminService.log_action()` — this blueprint's mutating actions should write through the existing admin audit-logging pattern, not invent a parallel one.

## 7. Existing Code to Reuse
- `FaqArticle`/`FaqFeedback` ORM models and `FaqRepository` (B-03) — extend `FaqRepository` with admin-scoped methods (`create_article`, `update_article`, `get_article_including_unpublished`, `get_feedback_summary`) rather than forking a second repository over the same table.
- `get_current_admin()` / `AdminSessionContext` / `require_admin_scope()` (`core/deps.py`).
- `AdminService.log_action()` (`modules/admin/service.py`) or the platform's equivalent per-mutation audit pattern — confirm exact call signature before wiring (do not invent a new audit mechanism if this one already covers cross-module admin mutations).
- `NoorHeroesBaseModel` for all new schemas.

## 8. Files to Create
- `tests/modules/support/test_admin_faq_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/support/schemas.py` — add `AdminFaqArticleCreateRequest`, `AdminFaqArticleUpdateRequest`, `AdminFaqArticleResponse` (includes `published`, unlike the public-facing summary/detail schemas), `FaqFeedbackSummaryResponse`.
- `src/noorheroes/modules/support/repository.py` — extend `FaqRepository` with admin-scoped methods that do **not** filter on `published=true` (admins must see drafts).
- `src/noorheroes/modules/support/service.py` — add `FaqService.admin_create_article()`, `admin_update_article()`, `admin_list_articles()`, `get_feedback_summary()`.
- `src/noorheroes/modules/support/api.py` — add admin routes to `SupportRouter` (or a dedicated `AdminSupportRouter` sub-mount, consistent with how other contexts separate public vs. admin routes — confirm the platform's existing convention, e.g. `IdentityRouter`'s single-router-multiple-auth-levels pattern per `FAST-API-INSTRUCTIONS.md` §6, before choosing router-splitting vs. single-router-mixed-auth).

## 10. Backend Requirements
- `GET /v1/admin/support/faq?locale=&published=`: paginated list, **not** filtered to `published=true` by default (admins need to see drafts) — `published` becomes an optional filter, not an implicit constraint.
- `POST /v1/admin/support/faq`: creates a new `faq_article` row; `published` defaults to `false` (drafts are the safe default — an article must be explicitly published, never accidentally live on creation).
- `GET /v1/admin/support/faq/{id}`: returns the article regardless of `published` state (unlike B-03's public detail endpoint, which 404s on unpublished).
- `PATCH /v1/admin/support/faq/{id}`: partial update of `title`/`body`/`locale`/`published`; publishing (`published: false → true`) writes an `AdminAuditLog` entry (a meaningful state change, consistent with the platform's general mutation-auditing convention).
- `GET /v1/admin/support/faq/{id}/feedback-summary`: returns `{ helpful_count, unhelpful_count, total_count }` aggregated from `faq_feedback` — read-only, no mutation of individual feedback rows exposed anywhere in this API.
- RBAC: `content_editor` scope required for all admin FAQ routes (mirrors N-01's client-side `RequirePermission` gate — this is the actual security boundary the client-side check defers to).

## 11. KMP Requirements
N/A.

## 12. NextJS Requirements
Consumed directly by N-01's `FaqArticleResourceClient` — this blueprint is the authoritative resolution of N-01's originally-flagged API contract gap (§13 of that blueprint).

## 13. API Contract
### `GET /v1/admin/support/faq?locale=&published=&page=&limit=`
- **Auth:** Bearer admin session + `content_editor` scope
- **Response 200:** `{ items: [ { article_id, title, body, locale, published, updated_at } ], total, page, limit, totalPages }`

### `POST /v1/admin/support/faq`
- **Request:** `{ title, body, locale, published: false }` (`published` optional, defaults `false`)
- **Response 201:** Created `AdminFaqArticleResponse`.

### `GET /v1/admin/support/faq/{id}`
- **Response 200:** Full article regardless of `published` state.
- **Response 404:** Article truly does not exist.

### `PATCH /v1/admin/support/faq/{id}`
- **Request:** Partial `{ title?, body?, locale?, published? }`
- **Response 200:** Updated `AdminFaqArticleResponse`.
- **Business Logic:** A `published: false → true` transition writes an audit log entry.

### `GET /v1/admin/support/faq/{id}/feedback-summary`
- **Response 200:** `{ helpful_count, unhelpful_count, total_count }`

## 14. Database Requirements
No new tables — writes/reads the exact `faq_article`/`faq_feedback` tables B-03 defined (§4.2). No schema change required beyond what B-03 already established.

## 15. Validation
`title`/`body` non-empty; `locale` validated against `SupportedLanguage`; `published` boolean. Reject a `PATCH` that would leave `title`/`body` empty on an already-published article (an empty published article is a content-safety concern, not just a data-integrity one).

## 16. Authentication
`get_current_admin()`.

## 17. Authorization
`require_admin_scope("content_editor")` (or the platform's exact scope-string convention — confirm against existing admin scope names, e.g. `admin:write`, before inventing `content_editor` as a literal string if a different naming convention is already established).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Non-admin or wrong-scope token | `403` |
| Article not found | `404` |
| Empty `title`/`body` on publish | `422` |
| Invalid `locale` | `422` |
| DB failure | `500` via standard `DomainError` handler |

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
`locale` field per-article, matching B-03's model exactly.

## 22. RTL
N/A (backend).

## 23. Analytics
Audit log entry on publish transitions (§10); no separate analytics event required beyond the platform's standard admin-action audit trail.

## 24. Performance
Reuses B-03's `(locale, published)` index; admin list queries may need an additional plain `updated_at` index if admin sorting/filtering patterns differ materially from the public search's needs — confirm via the actual query patterns N-01's `DataTable` uses before adding a speculative index.

## 25. Security
- `published=true` gating remains B-03's exclusive concern for the **public** endpoint — this admin endpoint deliberately does not apply that filter, and must never be reachable without the `content_editor` scope.
- Audit logging on publish transitions provides accountability for what became publicly visible and when.

## 26. Library Requirements
No new dependencies.

## 27. Testing
1. Unit test: `POST` creates a draft (`published=false`) by default.
2. Unit test: admin `GET` list/detail returns unpublished articles (unlike B-03's public endpoints).
3. Unit test: `PATCH published: false → true` writes an audit log entry.
4. Unit test: non-`content_editor` admin token rejected with `403`.
5. Unit test: `GET .../feedback-summary` correctly aggregates `faq_feedback` rows.
6. Integration test: an article created/edited here is correctly served (once published) by B-03's public `GET /v1/support/faq` — confirms no schema fork, single source of truth.
7. Test: empty `title`/`body` on a publish attempt returns `422`.

## 28. Documentation
OpenAPI descriptions for all five admin routes; docstring noting this is the sole write path into `faq_article`/`faq_feedback` is read-only here.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Extend FaqRepository with Admin-Scoped Methods**
- Task ID: B05-T01
- Objective: Data-access methods that do not apply the `published=true` filter.
- Why This Is Required: Admins need draft visibility; B-03's existing methods are public-gated by design and must not be altered to leak drafts publicly.
- Existing Architecture to Follow: B-03's `FaqRepository` structure.
- Existing Files to Reuse: `modules/support/repository.py`.
- Files to Create: none.
- Files to Modify: `modules/support/repository.py`.
- Implementation Details: `admin_list_articles(locale, published, cursor, limit)`, `admin_get_article(id)` (no published filter), `create_article(...)`, `update_article(id, ...)`, `get_feedback_summary(article_id)`.
- Business Rules: §10.
- Validation: N/A.
- Error Handling: Returns `None` for not-found.
- Security: These methods must never be called from B-03's public routes.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: Docstrings distinguishing these from B-03's public-gated methods.
- Dependencies: B-03.
- Do Not Change: Do not alter B-03's public-facing repository methods.
- Expected Result: Admin methods return drafts correctly.
- Definition of Done: No accidental `published=true` filter leaks into these methods.

**Task 02 — Implement Admin Service Methods with Audit Logging**
- Task ID: B05-T02
- Objective: Business logic, including the publish-transition audit write.
- Why This Is Required: Accountability for content going live.
- Existing Architecture to Follow: `AdminService.log_action()` pattern.
- Existing Files to Reuse: `modules/admin/service.py` (or equivalent shared audit utility — confirm exact API).
- Files to Create: none.
- Files to Modify: `modules/support/service.py`.
- Implementation Details: `admin_create_article()`, `admin_update_article()` (detects `published: false→true` transition and logs it), `get_feedback_summary()`.
- Business Rules: §10.
- Validation: Empty title/body rejection on publish.
- Error Handling: `422` on validation failure.
- Security: Audit logging is the accountability mechanism here.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: Docstrings.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Publish transitions are always logged.
- Definition of Done: Audit entry confirmed in Task 04's test.

**Task 03 — Add Admin FAQ Routes with RBAC Gate**
- Task ID: B05-T03
- Objective: Expose all five endpoints, `content_editor`-scoped.
- Why This Is Required: Core deliverable, resolves N-01's contract gap.
- Existing Architecture to Follow: `require_admin_scope()` pattern; router-splitting/mixed-auth convention (confirm against existing multi-auth-level routers before choosing an approach, per §9's note).
- Existing Files to Reuse: `modules/support/api.py`.
- Files to Create: none.
- Files to Modify: `modules/support/api.py`, `modules/support/schemas.py`.
- Implementation Details: Per §13.
- Business Rules: N/A.
- Validation: Pydantic schemas.
- Error Handling: Per §18.
- Security: `require_admin_scope("content_editor")` (or confirmed equivalent scope string) on every route.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: OpenAPI.
- Dependencies: Task 02.
- Do Not Change: Do not alter B-03's public routes on the same router.
- Expected Result: All 5 routes live.
- Definition of Done: Matches §13 exactly.

**Task 04 — Write Test Suite**
- Task ID: B05-T04
- Objective: Cover §27.
- Why This Is Required: Standard coverage plus the single-source-of-truth integration guarantee.
- Existing Architecture to Follow: pytest conventions.
- Existing Files to Reuse: Existing admin-auth test fixtures.
- Files to Create: `tests/modules/support/test_admin_faq_api.py`.
- Files to Modify: none.
- Implementation Details: All 7 cases from §27, notably case 6 (cross-endpoint integration with B-03).
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert exact status codes.
- Security: RBAC-scope test is security-critical.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test docstrings.
- Dependencies: Tasks 01–03.
- Do Not Change: N/A.
- Expected Result: All pass.
- Definition of Done: 100% of §27 green.

## 30. Definition of Done
Admin FAQ CRUD (`GET/POST /v1/admin/support/faq`, `GET/PATCH /v1/admin/support/faq/{id}`, `GET .../feedback-summary`) live, `content_editor`-scoped, writing to the exact same `faq_article`/`faq_feedback` tables B-03 serves publicly, publish transitions audited, all tests green — resolves N-01's originally-flagged API contract gap.

## 31. Final Verification Checklist
- [ ] Draft articles (`published=false`) visible via admin endpoints, invisible via B-03's public endpoints (tested)
- [ ] Publish transition writes an audit log entry (tested)
- [ ] `content_editor` scope enforced on all 5 routes
- [ ] No schema fork — same `faq_article`/`faq_feedback` tables as B-03
- [ ] "Delete" never implemented as a hard delete anywhere in this API
- [ ] Feedback rows remain admin-read-only (no edit/delete endpoint exists for `faq_feedback`)
- [ ] No PostgreSQL/Redis credential files touched
