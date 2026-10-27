# B-01 — Dua Catalog & Content Delivery API

> **Status:** **Implemented & Verified**  
> **Implementation Date:** September 2026  
> **Test Coverage:** 100% pass across unit, integration, API, free-tier isolation, and architecture suites (`pytest tests/modules/dua/` & `pytest tests/architecture/`).

## 1. Feature Context
NoorHeroes — Feature A.6 Dua Learning. Source PRD: `PRD_Documents/Child App (1-12)/Feature_A6_Dua_Learning.md` §3.4/§3.5/§4. Cross-referenced by `A8_Daily_Quiz_Engine/Backend/03-context-parameterized-quiz-delivery-api.md` (which delegates its `NOT_YET_LEARNED` gate to this module's sibling B-02) and `B14_Favorites/Backend/01-favorite-toggle-api.md` (which already treats `content_type=dua` as a first-class favoritable type). This blueprint has been re-derived against the real architecture in `FAST-API-INSTRUCTIONS.md` — see §32 for what changed from the original draft.

## 2. Parent Feature
A.6 Dua Learning

## 3. Sub-feature
B-01 — Dua Catalog & Content Delivery API (User API)

## 4. Objective
Serve the dua category list and individual Dua Card content (Arabic text, transliteration, translation, audio) to the child-facing app. Rather than forcing dua's genuinely distinct schema (Arabic/transliteration/translation/source-citation/versioning) into the generic `content` context's `ContentItem` model, this establishes a **new bounded context, `src/noorheroes/modules/dua/`**, following the identical Router → Service → Repository → Model layering used by every other context (`FAST-API-INSTRUCTIONS.md` §1) — the same precedent set when `habits` (A.7) and `avatars` (A.12) were established rather than crammed into `content`.

## 5. Business Requirements
FR-1, FR-2, FR-4, FR-13; Acceptance criteria: category list renders exactly the baseline six categories plus approved additions; Dua Card renders all four elements without extra taps; free-tier accounts get full access with zero paywall (PRD §1.9). NFR: catalog list p95 < 600ms cached.

## 6. Existing Architecture
Modular Monolith, `src/noorheroes/modules/*` (per `FAST-API-INSTRUCTIONS.md` §1/§5). 12 established contexts (`identity`, `admin`, `ai_safety`, `content`, `learning`, `localization`, `media`, `notifications`, `rewards`, `subscriptions`, `habits`, `avatars`) plus `downloads` (established by B.15). **No `dua` context exists yet — this sub-feature establishes it.** Auth via `Depends(get_current_child)` → `ChildSessionContext(family_id, child_id, session_id)`. Errors via `core/exceptions.py` `DomainError` subclasses (`NotFoundError`→404, `ValidationError`→422). Entitlement/tier gating lives in the `subscriptions` context (`SubscriptionService.get_entitlement()`); the always-free-tier rule for this content type means `dua`'s routes simply never call into that service at all, rather than calling it and special-casing the result.

## 7. Existing Code to Reuse
- `common/base_service.py::BaseService` — `DuaService` base class
- `common/base_repository.py::BaseRepository[ModelT]`, `PageResult[ModelT]` — `DuaRepository(BaseRepository[Dua])`, cursor-based `list_paginated(cursor, limit)`, not offset pagination
- `infrastructure/db/base.py::Base`, `TimestampMixin` (`created_at`, `updated_at`, `version`) — optimistic-lock version column
- `core/deps.py::get_current_child`
- `core/exceptions.py::NotFoundError`, `ValidationError`
- `common/utils/ids.py::generate_ulid()` — primary key generation, matching platform-wide ID convention
- `localization` context's `TranslationContent`/`TranslationService`/`LocaleManager` pattern (per A7-B01's precedent: "follow the existing `LocalizationRouter`/`TranslationService` pattern rather than inlining hardcoded strings") — reused for per-locale transliteration/translation resolution, not a bespoke locale mechanism

## 8. Files to Create
- `src/noorheroes/modules/dua/models.py` — `Dua(Base, TimestampMixin)`, `DuaContentVersion(Base, TimestampMixin)`
- `src/noorheroes/modules/dua/schemas.py` — `DuaSummaryResponse`, `DuaDetailResponse`
- `src/noorheroes/modules/dua/repository.py` — `DuaRepository(BaseRepository[Dua])`
- `src/noorheroes/modules/dua/service.py` — `DuaService(BaseService)`
- `src/noorheroes/modules/dua/api.py` — `DuaRouter`
- `alembic/versions/xxxx_create_dua_schema.py`
- `tests/modules/dua/test_dua_catalog_api.py`
- `tests/modules/dua/test_always_free_tier_regression.py`

## 9. Files to Modify
- `main.py` — register `DuaRouter` alongside the other domain routers
- `FAST-API-INSTRUCTIONS.md` §5 — add a `5.13 dua Context` entry (or next free index; confirm against whatever B.15's `downloads` context was numbered) and §6 — add `DuaRouter` to the API Routers manual, following the exact documentation convention used for `habits`/`avatars`/`downloads`

## 10. Backend Requirements
- `GET /v1/catalog?type=dua&category=&locale=` → paginated `DuaSummaryResponse[]` via `DuaService.list_catalog(category, locale, cursor, limit)`
- `GET /v1/catalog/dua/{id}` → `DuaDetailResponse` via `DuaService.get_by_id(dua_id, locale)`
- Serve only the latest `published` `DuaContentVersion` row per dua+locale
- **Always-free-tier rule**: these two routes never call `SubscriptionService.get_entitlement()` or any `subscriptions`-context dependency, under any code path — enforced by the absence of that dependency, not a bypass flag (a flag can be flipped on by accident; a dependency that was never wired in cannot)
- Redis cache-aside, 1-hour TTL, invalidated on publish

## 11. KMP Requirements
N/A directly (consumed by K-01, K-02). Response shape must match `DuaRepository.getCatalog()` / `getDuaDetail()` in the KMP blueprint.

## 12. NextJS Requirements
N/A (this is the read API; admin authoring is B-08).

## 13. API Contract

### `GET /v1/catalog?type=dua&category={category}&locale={locale}&cursor={cursor}&limit={limit}`
- **Auth:** Bearer (child-mode) via `Depends(get_current_child)`
- **Response 200:**
```json
{
  "items": [ { "id": "dua_...", "category": "morning", "title": "...", "preview": "..." } ],
  "next_cursor": "...",
  "has_more": false
}
```
*(shape matches `common/base_repository.py::PageResult[ModelT]`, not an offset/page envelope)*
- **Error Responses:** `401` (via `AuthenticationError`), `422 INVALID_CATEGORY` (via `ValidationError`)

### `GET /v1/catalog/dua/{id}`
- **Response 200:**
```json
{
  "id": "dua_...", "category": "morning", "arabic_text": "...", "transliteration": "...",
  "translation": "...", "audio_url": "https://cdn.../audio.mp3", "source_citation": "...",
  "age_min": null, "age_max": null
}
```
- **Error Responses:** `401`, `404` (via `NotFoundError`), `410 CONTENT_WITHDRAWN` for archived duas — a `DuaWithdrawnError(DomainError)` subclass, distinct from `NotFoundError`, following the same withdrawn-vs-not-found distinction A.3's Stories module already established

## 14. Database Requirements
New schema in the `dua` context: `dua` table — `dua_id ULID PK`, `category_key VARCHAR FK → dua_category.category_key` (see B-11), `source_citation`, `is_withdrawn`, `age_min`, `age_max`, `habit_suggestion_eligible BOOLEAN DEFAULT true`, `created_at`, `updated_at`, `version` (via `TimestampMixin`). `dua_content_version` table — `version_id ULID PK`, `dua_id FK`, `locale`, `arabic_text`, `transliteration`, `translation`, `audio_asset_key`, `status CHECK IN ('draft','pending_review','published','archived')`, `created_at`; index `(dua_id, locale, status, created_at DESC)`.

## 15. Validation
`category` validated against `dua_category` (B-11), not a hardcoded list. `id` must resolve to an existing dua; `is_withdrawn=true` → `410`.

## 16. Authentication
Bearer JWT, child-mode session, via `Depends(get_current_child)`.

## 17. Authorization
No role/tier restriction. `subscriptions` context is architecturally never consulted by this router — this is the exemption mechanism (see §10).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Catalog fetch DB failure | 5xx; client (K-01) falls back to cache |
| Redis unavailable | Fall through to DB, log warning, no request failure |
| Withdrawn dua requested | `410` via `DuaWithdrawnError` |
| Unknown category | `422 INVALID_CATEGORY` via `ValidationError` |

## 19. Offline First
N/A server-side; response shape must be cacheable/deterministic for K-01's offline-first design.

## 20. Local Data
N/A (backend).

## 21. Localization
`locale` param resolves the returned `DuaContentVersion` row via the `localization` context's existing resolution pattern; Arabic text is locale-independent.

## 22. RTL
N/A at API layer.

## 23. Analytics
Client-emitted (`dua_learning_landing_viewed` etc., K-01); no server-side duplicate.

## 24. Performance
Cursor-based pagination (`BaseRepository.list_paginated`), avoiding the N+1 offset-scan problem entirely. Redis cache-aside, 1-hour TTL.

## 25. Security
Always-free-tier guarantee proven by *absence* of a `subscriptions`-context dependency in this router's dependency graph — the P0 regression test asserts this via response-shape equivalence across tier fixtures, and a static-analysis/import-check test asserting `dua/api.py` never imports from `modules/subscriptions/`.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Pydantic v2, Redis, Alembic — existing platform stack only.

## 27. Testing
- Unit: category validation against `dua_category`, locale fallback, withdrawn→410 mapping
- Integration: catalog list → detail fetch round trip
- **P0 regression**: parameterized across free/trial-expired/premium fixtures, asserting identical response shape; plus a static import-check that `modules/dua/api.py` has no dependency edge to `modules/subscriptions/`
- Negative: deliberately wire the subscriptions dependency into a test-only branch and confirm the import-check test correctly fails (test-of-the-test)

## 28. Documentation
OpenAPI docstrings; add `5.13 dua Context` (or correct next index) to `FAST-API-INSTRUCTIONS.md` §5, matching the exact format of the existing `5.11 habits`/`5.12 avatars` entries (Location, Established By, Models, Schemas, Repositories, Service, Router, Note).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Establish the `dua` Bounded Context Skeleton**
Task ID: B-01-T01. Objective: create `src/noorheroes/modules/dua/{__init__.py,models.py,schemas.py,repository.py,service.py,api.py}` following the exact file layout of `modules/habits/`. Why Required: no `dua` context exists yet. Existing Architecture to Follow: `modules/habits/` and `modules/downloads/` as the two most recent precedents for "establish a new context." Definition of Done: package imports cleanly, empty router registers in `main.py` without error.

**Task 02 — Create Models**
Task ID: B-01-T02. Files to Create/Modify: `models.py`. Implementation Details: `Dua(Base, TimestampMixin)`, `DuaContentVersion(Base, TimestampMixin)` per §14. Definition of Done: models import cleanly.

**Task 03 — Create Migration**
Task ID: B-01-T03. Files to Create: `alembic/versions/xxxx_create_dua_schema.py`. Definition of Done: `alembic upgrade head` succeeds; `dua_category` FK deferred until B-11's table exists (coordinate ordering, or create both tables in this migration and have B-11 add rows/CRUD only).

**Task 04 — Create Schemas**
Task ID: B-01-T04. Files to Create: `schemas.py` — `DuaSummaryResponse`, `DuaDetailResponse`. Definition of Done: schemas match §13 exactly.

**Task 05 — Implement Repository**
Task ID: B-01-T05. Files to Create: `repository.py` — `DuaRepository(BaseRepository[Dua])` extending with `list_by_category(category, locale, cursor, limit)`, `get_detail(dua_id, locale)`. Existing Architecture to Follow: `BaseRepository[ModelT]` conventions (`get_by_id`, `list_paginated`). Definition of Done: repository tests green, no N+1 on latest-version resolution.

**Task 06 — Implement Service**
Task ID: B-01-T06. Files to Create: `service.py` — `DuaService(BaseService)`. Business Rules: withdrawn dua raises a `DuaWithdrawnError`. Definition of Done: service tests green including Redis-failure fallback.

**Task 07 — Implement Router**
Task ID: B-01-T07. Files to Create: `api.py` — `DuaRouter`, `Depends(get_current_child)`. Files to Modify: `main.py`. Definition of Done: both endpoints reachable, matching §13 exactly.

**Task 08 — Verify Always-Free-Tier Isolation**
Task ID: B-01-T08. Objective: confirm `modules/dua/` has zero import edges into `modules/subscriptions/`. Security: this is the P0 requirement. Definition of Done: static import-check test passes; regression suite passes across all tier fixtures.

**Task 09 — Add Validation & Error Handling**
Task ID: B-01-T09. Definition of Done: §18 scenarios all produce correct responses.

**Task 10 — Add Tests**
Task ID: B-01-T10. Files to Create: both test files listed in §8. Definition of Done: CI-blocking regression suite green.

**Task 11 — Update Architecture Documentation**
Task ID: B-01-T11. Files to Modify: `FAST-API-INSTRUCTIONS.md`. Definition of Done: `5.13 dua Context` entry added matching the `habits`/`avatars` format.

**Task 12 — Final Code Review**
Task ID: B-01-T12. Definition of Done: §31 checklist fully checked.

## 30. Definition of Done
`dua` bounded context established and registered; both endpoints live and matching contract; always-free-tier guarantee proven by dependency-graph absence, not a bypass flag; architecture doc updated.

## 31. Final Verification Checklist
- [x] `src/noorheroes/modules/dua/` established following the `habits`/`downloads` precedent
- [x] `GET /v1/catalog?type=dua` and `GET /v1/catalog/dua/{id}` match §13 exactly, including cursor-based pagination shape
- [x] Zero import edges from `modules/dua/` to `modules/subscriptions/`, verified by static test
- [x] `410` (not `404`) for withdrawn duas
- [x] `FAST-API-INSTRUCTIONS.md` §5/§6 updated with the new context entry
- [x] No changes to PostgreSQL/Redis credentials
- [x] No changes to any other bounded context's behavior

## 32. Addendum — What Changed From the Original Draft
The original version of this file used generic paths (`app/services/dua_catalog_service.py`, `app/middleware/entitlement_middleware.py`) that don't exist in this codebase. This rewrite grounds it in the real `src/noorheroes/modules/<context>/` modular-monolith layout, real base classes (`BaseService`, `BaseRepository[ModelT]`), real auth (`get_current_child`), real exceptions, cursor-based pagination, and establishes `dua` as its own bounded context rather than inventing a parallel generic "Content & Catalog Service." The always-free-tier guarantee is now framed as a dependency-graph property (no edge to `subscriptions`) rather than a middleware bypass flag, which is a stronger and more testable guarantee. See B-11 for the category-model addendum, which still applies unchanged.

## 33. Implementation & Verification Summary
- **Bounded Context**: Established `src/noorheroes/modules/dua/` adhering to Clean Architecture with 14 modular files (`models.py`, `schemas.py`, `repository.py`, `service.py`, `events.py`, `deps.py`, `cache.py`, `access.py`, `exceptions.py`, `api.py`, `admin_schemas.py`, `admin_service.py`, `admin_api.py`, `__init__.py`).
- **Database Tables & Migrations**: Migrations `0051_create_dua_schema.py` and `0052_add_dua_progress_and_recall_tables.py` creating `dua_category`, `dua`, `dua_content_version`, `dua_progress`, `dua_recall_question`, and `dua_recall_attempt` tables with UUIDv7 PKs, indexes, and constraints.
- **Endpoints Delivered**:
  - `GET /v1/catalog?type=dua` & canonical alias `GET /v1/dua/catalog` (cursor-based pagination).
  - `GET /v1/catalog/dua/{id}` & canonical alias `GET /v1/dua/{id}` (4-element Dua Card with Arabic, transliteration, translation, audio).
  - `GET /v1/dua/categories` (active taxonomy listing with localized labels).
  - `410 CONTENT_WITHDRAWN` returned for retired duas via `DuaWithdrawnError`.
- **Always-Free-Tier Verified**: Zero imports from `src.noorheroes.modules.subscriptions`, verified by static analysis and regression tests in `test_always_free_tier_regression.py`.
- **Redis Cache-Aside**: 1-hour TTL on catalog, detail, and categories with fail-open fallback.
- **Documentation**: Fully synchronized in `FAST-API-INSTRUCTIONS.md` (§5.14, §6.14, Route Catalog, Table Inventory, Migrations Catalog).
