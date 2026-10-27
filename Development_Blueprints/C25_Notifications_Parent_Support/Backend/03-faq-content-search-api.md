# Blueprint: FAQ Content & Search API

## 1. Feature Context
Platform: NoorHeroes Backend (FastAPI, Modular Monolith). This blueprint introduces a **new 11th bounded context**, `support`, mounted at `src/noorheroes/modules/support/`, following the exact same `models.py`/`schemas.py`/`repository.py`/`service.py`/`api.py` layout as the existing 10 contexts (`FAST-API-INSTRUCTIONS.md` §5, §14). It delivers the FAQ half of the Support Center; B-04 delivers the ticket half in the same context.

## 2. Parent Feature
C.25 — Notifications (Parent) & Support.

## 3. Sub-feature
B-03 — FAQ Content & Search API.

## 4. Objective
Implement `GET /v1/support/faq?q=`, `GET /v1/support/faq/{id}`, and the "Was this helpful?" feedback capture, serving **exclusively** from admin-authored, `published=true` `faq_article` rows — with a structurally provable guarantee that this endpoint never calls any AI-generation provider.

## 5. Business Requirements
Source: PRD §1.7 FR-10; §1.10 Edge Case 4; §3.4; §4.2; §5 Backend AI Code-Generation Prompt item 3.
- "The FAQ search is content-governed (admin-authored, scholar-reviewed where Islamic-content-adjacent) — never an AI-freeform-generated answer presented as official guidance" (FR-10) — this is a structural, testable guarantee, not a UI convention.
- Zero-results search → the client shows a "no results, contact Support" fallback (Edge Case 4); this endpoint's obligation is simply to return an empty list cleanly, never an error.
- `faq_article.published` gates visibility in the public search endpoint (§4.2) — unpublished/draft content must never leak through this endpoint under any query.
- Works for "any parent, even pre-subscription" (§3.4) — public or Bearer auth, not subscription-gated.

## 6. Existing Architecture
Per `FAST-API-INSTRUCTIONS.md` §14 New Feature Step-by-Step Guide: model → schema → repository → service (with `OutboxWriter.emit()` where domain events matter — not applicable here, FAQ content has no downstream event consumers) → deps factory → route. Per §11 Layer Rules: no direct DB access in routers, no manual commits in services/repositories, no naked exceptions.

## 7. Existing Code to Reuse
- `BaseRepository[ModelT]` for standard CRUD/pagination (`get_by_id`, `list_paginated`).
- `BaseService` for the service base class.
- `NoorHeroesBaseModel` (Pydantic v2 camelCase base) for all new schemas.
- `core/exceptions.py` `DomainError` subclasses (`NotFoundError` for a missing article ID).
- Existing localization infrastructure's `locale` value set (`localization` context's `SupportedLanguage`) — reuse the platform's canonical locale codes for `faq_article.locale` rather than inventing a separate locale enum.

## 8. Files to Create
- `src/noorheroes/modules/support/__init__.py`
- `src/noorheroes/modules/support/models.py` — `FaqArticle`, `FaqFeedback` ORM models
- `src/noorheroes/modules/support/schemas.py` — `FaqArticleSummaryResponse`, `FaqArticleDetailResponse`, `FaqFeedbackRequest`
- `src/noorheroes/modules/support/repository.py` — `FaqRepository`
- `src/noorheroes/modules/support/service.py` — `FaqService(BaseService)`
- `src/noorheroes/modules/support/api.py` — `SupportRouter` (FAQ routes; B-04 adds ticket routes to the same router)
- `src/noorheroes/modules/support/deps.py` — `get_faq_service()` factory
- `alembic/versions/xxxx_create_faq_article_faq_feedback.py`
- `tests/modules/support/test_faq_api.py`
- `tests/modules/support/test_faq_no_ai_structural.py`

## 9. Files to Modify
- Root API aggregator (e.g., `src/noorheroes/api/router.py`) — mount `SupportRouter` under `/v1/support`, joining the existing 10-context registration pattern as the 11th.

## 10. Backend Requirements
- `FaqArticle`: `article_id` (PK), `title`, `body`, `locale`, `published` (bool), `updated_at` — per PRD §4.2 exactly.
- `FaqFeedback`: `feedback_id` (PK), `article_id` (FK), `helpful` (bool), `created_at` — append-only, no update/delete method exposed anywhere in the repository.
- `GET /v1/support/faq?q=`: full-text or `ILIKE`-based search over `title`/`body`, filtered to `published = true` and optionally `locale`; returns `{ "articles": [ { "id", "title", "summary" } ] }`.
- `GET /v1/support/faq/{id}`: full article body; `404` if not found OR if `published = false` (an unpublished article must behave as if it doesn't exist to this endpoint — never a "found but hidden" distinction that could leak existence).
- `FaqRepository` must have **no code path** that imports or calls `infrastructure/ai/*` (`AIProviderFactory`, `OpenAIProvider`, etc.) — this is the structural guarantee tested in Task 05.
- Feedback capture: simple append; no rate-limiting required beyond the platform's default `RateLimitMiddleware`.

## 11. KMP Requirements
N/A for backend scope — consumed by K-03's `SupportRepository.searchFaq()`.

## 12. NextJS Requirements
N/A for backend scope — N-01 (FAQ Content Management) requires new admin-scoped CRUD endpoints (`POST/PATCH /v1/admin/support/faq`) not specified in C.25's own §3.4 API list; those are explicitly out of scope for this blueprint and must be defined precisely when N-01 is generated, not assumed here.

## 13. API Contract
### `GET /v1/support/faq?q=`
- **Auth:** Public or Bearer (works for any parent, even pre-subscription)
- **Query Params:** `q: string` (search term), `locale: string` (optional)
- **Response 200:** `{ "articles": [ { "id": "string", "title": "string", "summary": "string" } ] }`

### `GET /v1/support/faq/{id}`
- **Response 200:** Full article content + a "Was this helpful?" feedback capture affordance (i.e., the response includes the article body; feedback is a separate `POST`).
- **Response 404:** Article not found or not published.

### `POST /v1/support/faq/{id}/feedback`
- **Request:** `{ "helpful": true }`
- **Response 200:** `{ "recorded": true }`

## 14. Database Requirements
New tables per PRD §4.2:
- `faq_article`: Index `(locale, published)`.
- `faq_feedback`: FK `article_id`; Index `(article_id, created_at DESC)`; append-only.
Retention: standard analytics-retention window for `faq_feedback` aggregation (§4.5).

## 15. Validation
- `locale` (if provided) validated against the platform's `SupportedLanguage` code set.
- `helpful` must be a boolean.
- Search query `q` length-bounded (prevent pathological queries) per standard input validation practice.

## 16. Authentication
Public or Bearer — `GET` routes accept unauthenticated requests; `POST /feedback` may be public too (per §3.4's "works for any parent, even pre-subscription" framing) unless abuse patterns require requiring at least a session — default to public with standard rate limiting, escalate to Bearer-required only if abuse is observed.

## 17. Authorization
No RBAC needed — content is either published (visible to all) or not (visible to none via this endpoint).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Zero search results | `200` with `{ "articles": [] }`, never an error |
| Article not found or unpublished | `404` |
| Invalid `locale` value | `422` |
| DB failure | `500` via standard `DomainError` handler |

## 19. Offline First
N/A server-side; K-03 requires connectivity for FAQ search per PRD §1.14.

## 20. Local Data
N/A.

## 21. Localization
`faq_article.locale` drives which locale's content is served; this is the platform's actual localization mechanism for FAQ content (distinct from the AI-translation pipeline used elsewhere — FAQ content is admin-authored per-locale, not machine-translated, consistent with FR-10's content-governance requirement).

## 22. RTL
N/A (backend); article `body` content itself may contain Arabic/Urdu text requiring RTL rendering client-side (K-03's concern).

## 23. Analytics
No server-side emission required; `faq_search_performed`, `faq_article_viewed`, `faq_zero_results_shown`, `faq_marked_unhelpful` (§1.19) are client-fired (K-03). Server-side structured logging of search-query volume/zero-result queries is a genuine value-add for admin content-gap tooling (N-01) — log `{event: "faq_search_query_logged", q, locale, result_count}` for this purpose.

## 24. Performance
- `(locale, published)` index supports the primary filter path.
- Consider a simple `ILIKE`/trigram index for search if PostgreSQL's `pg_trgm` extension is already available on the platform; otherwise a straightforward `ILIKE '%q%'` is acceptable at this feature's expected content volume (FAQ article counts are typically in the dozens-to-low-hundreds, not requiring a dedicated search engine).
- No N+1 risk — single-table queries.

## 25. Security
- The **structural no-AI-call guarantee** (Task 05) is this sub-feature's primary security/trust control, preventing a future accidental regression where search results get "enhanced" by an LLM and presented as official guidance.
- Standard `RateLimitMiddleware` applied to the public search/feedback endpoints to prevent abuse.

## 26. Library Requirements
No new dependencies (or `pg_trgm` if adopted for search, confirmed against existing PostgreSQL extension availability first — do not assume it's enabled).

## 27. Testing
1. Unit test: `GET /v1/support/faq?q=` returns only `published=true` rows.
2. Unit test: an unpublished/draft article is never returned by either the search or detail endpoint (both return as if it doesn't exist).
3. Unit test: zero-match search returns `200` with an empty array.
4. Unit test: `locale` filter correctly narrows results.
5. **Structural test (mandatory):** static-analysis or import-graph assertion confirming `modules/support/repository.py` and `modules/support/service.py` have zero import of `infrastructure/ai/*` — this endpoint's implementation has no code path that calls any AI-generation service (§5 item 3).
6. Integration test: feedback capture writes an append-only `faq_feedback` row correctly.
7. Integration test: detail endpoint returns `404` for both a genuinely missing ID and an unpublished one (indistinguishable response).

## 28. Documentation
- OpenAPI descriptions for all three endpoints.
- Module-level docstring in `modules/support/service.py` explicitly citing FR-10 and stating "this service must never import or call any AI provider" as a standing constraint for future contributors.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create Support Module Scaffold, Models, and Migration**
- Task ID: B03-T01
- Objective: Stand up the new `support` bounded context following the platform's exact 10-context pattern as an 11th.
- Why This Is Required: No existing context owns FAQ/ticket data; PRD introduces genuinely new tables.
- Existing Architecture to Follow: §14 New Feature Step-by-Step Guide; any existing context's file layout as the direct template (e.g., `modules/rewards/` for structural mirroring).
- Existing Files to Reuse: `infrastructure/db/base.py` (`Base`, `TimestampMixin`).
- Files to Create: `modules/support/__init__.py`, `modules/support/models.py`, Alembic migration.
- Files to Modify: none.
- Implementation Details: `FaqArticle`/`FaqFeedback` per §4.2 exactly; migration creates both tables with the specified indexes.
- Business Rules: §4.2 constraints.
- Validation: N/A.
- Error Handling: N/A.
- Security: N/A.
- Performance: Indexes as specified.
- Localization: `locale` column.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: Docstrings.
- Dependencies: None.
- Do Not Change: Do not touch any of the existing 10 contexts' migrations.
- Expected Result: Tables exist, migration applies cleanly.
- Definition of Done: Schema matches §4.2 exactly.

**Task 02 — Implement FaqRepository**
- Task ID: B03-T02
- Objective: Data-access layer, `published`-gated by construction.
- Why This Is Required: Core query logic for both FAQ endpoints.
- Existing Architecture to Follow: `BaseRepository[ModelT]`.
- Existing Files to Reuse: `common/base_repository.py`.
- Files to Create: `modules/support/repository.py`.
- Files to Modify: none.
- Implementation Details: `search_articles(q, locale) -> list[FaqArticle]` (WHERE `published=true` always applied, never optional/bypassable), `get_published_article(id) -> FaqArticle | None`, `add_feedback(article_id, helpful) -> FaqFeedback`.
- Business Rules: FR-10, §4.2.
- Validation: N/A.
- Error Handling: Returns `None` for not-found/unpublished (service maps to 404).
- Security: `published=true` filter is non-optional in every read method's SQL — no method signature offers a way to bypass it.
- Performance: Uses `(locale, published)` index.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 04.
- Documentation: Docstrings.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Repository has zero AI-provider imports.
- Definition of Done: Matches §10.

**Task 03 — Implement FaqService and Routes**
- Task ID: B03-T03
- Objective: Business logic and public API surface.
- Why This Is Required: Core deliverable.
- Existing Architecture to Follow: `BaseService`, `deps.py` factory pattern, router registration pattern.
- Existing Files to Reuse: `core/exceptions.py` (`NotFoundError`).
- Files to Create: `modules/support/service.py`, `modules/support/api.py`, `modules/support/deps.py`, `modules/support/schemas.py`.
- Files to Modify: root API aggregator.
- Implementation Details: Per §13 API Contract exactly; mount `SupportRouter` at `/v1/support`.
- Business Rules: FR-10, Edge Case 4.
- Validation: `locale`/`helpful` schema validation.
- Error Handling: Per §18.
- Security: Public rate-limited endpoints via existing `RateLimitMiddleware`.
- Performance: N/A.
- Localization: `locale` query param.
- RTL: N/A.
- Analytics: Log search-query volume per §23.
- Tests: Covered in Task 04.
- Documentation: OpenAPI.
- Dependencies: Task 02.
- Do Not Change: N/A.
- Expected Result: All 3 endpoints live.
- Definition of Done: Matches §13 exactly.

**Task 04 — Write Standard Test Suite**
- Task ID: B03-T04
- Objective: Cover §27 items 1–4, 6–7.
- Why This Is Required: Standard coverage plus the published-gating guarantee.
- Existing Architecture to Follow: pytest conventions.
- Existing Files to Reuse: none new beyond standard fixtures.
- Files to Create: `tests/modules/support/test_faq_api.py`.
- Files to Modify: none.
- Implementation Details: Cases 1–4, 6–7 from §27.
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert exact status codes.
- Security: Published-gating tests are security/trust-critical.
- Performance: N/A.
- Localization: Locale-filter test.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the tests.
- Documentation: Test docstrings.
- Dependencies: Tasks 01–03.
- Do Not Change: N/A.
- Expected Result: All pass.
- Definition of Done: Cases 1–4, 6–7 green.

**Task 05 — Write Structural No-AI-Call Test**
- Task ID: B03-T05
- Objective: Prove, at the code level, that this endpoint's implementation never invokes an AI provider.
- Why This Is Required: PRD §5 item 3 mandates this exact structural test as a top guarantee.
- Existing Architecture to Follow: Python `ast`/import-graph introspection, or a simpler `importlib`-based check confirming `infrastructure.ai` is absent from `sys.modules` dependencies of `modules.support.repository`/`modules.support.service` at import time.
- Existing Files to Reuse: none.
- Files to Create: `tests/modules/support/test_faq_no_ai_structural.py`.
- Files to Modify: none.
- Implementation Details: Parse the source files (or inspect their compiled import table) for any `from ...infrastructure.ai import ...` or `import ...infrastructure.ai` statement; fail the test if found.
- Business Rules: FR-10.
- Validation: N/A.
- Error Handling: N/A.
- Security: This is the single highest-priority test in this sub-feature.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: This task IS the test.
- Documentation: Test docstring explicitly citing FR-10.
- Dependencies: Tasks 01–03.
- Do Not Change: N/A.
- Expected Result: Test passes now and will fail (correctly, as a regression signal) if anyone later wires AI generation into FAQ search.
- Definition of Done: Structural test green and treated as CI-mandatory alongside Task 04's suite.

## 30. Definition of Done
`support` bounded context stood up with `faq_article`/`faq_feedback` tables; `GET /v1/support/faq`, `GET /v1/support/faq/{id}`, `POST /v1/support/faq/{id}/feedback` live, serving exclusively published content with a structurally-proven zero-AI-generation guarantee, all tests green.

## 31. Final Verification Checklist
- [ ] Unpublished articles never returned by search or detail endpoint (tested)
- [ ] Structural no-AI-import test passes
- [ ] Zero-results search returns `200` with empty array
- [ ] `faq_feedback` is append-only (no update/delete method exists)
- [ ] `support` module follows the exact 10-context file layout convention
- [ ] No PostgreSQL/Redis credential files touched
- [ ] Root API aggregator correctly mounts `SupportRouter` alongside the existing 10 contexts
