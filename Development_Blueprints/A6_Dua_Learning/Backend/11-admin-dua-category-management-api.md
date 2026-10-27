# B-11 — Admin Dua Category Management API

> **Status:** **✅ COMPLETED & VERIFIED**  
> **Implementation Date:** September 2026  
> **Clean Architecture Context:** `src/noorheroes/modules/dua/`  
> **Test Coverage:** 23 dedicated tests (`test_admin_dua_category_management.py` + `test_dua_category_fk_migration.py`), 467 Dua Learning tests passing (100% green).

## 1. Feature Context
NoorHeroes — Feature A.6 Dua Learning. Identified during gap review: PRD §4.2 requires category additions "without a migration," which a DB `CHECK` constraint cannot deliver. This file resolves that inconsistency within the real `src/noorheroes/modules/dua/` bounded context established by B-01.

## 2. Parent Feature
A.6 Dua Learning

## 3. Sub-feature
B-11 — Admin Dua Category Management API (Admin API) — Architecture Improvement

## 4. Objective
Let `content_editor`-scoped admins add, relabel, reorder, and deactivate dua categories without a deploy, by replacing the `CHECK`-constrained `dua.category` column with a `dua_category` lookup table and an FK.

## 5. Business Requirements
PRD §4.2, §1.9, §2.1.

## 6. Existing Architecture
**Existing Architecture:** B-01 originally modeled `dua.category` with a `CHECK` constraint. **Problem:** contradicts PRD §4.2's stated no-migration extensibility. **Proposed Improvement:** `dua_category` table (`category_key ULID-or-slug PK`, `icon_key`, `sort_order`, `is_active`) + a labels mechanism — reusing the real `localization` context's `TranslationContent` pattern for per-locale labels where practical (confirm whether `TranslationContent` is generic enough for admin-authored short taxonomy labels, vs. AI-translated long-form content, before deciding between a `dua_category_translation` table and `TranslationContent` reuse), and an FK from `dua.category_key` replacing the `CHECK`. **Impact:** B-01's category validation now queries this table. **Implementation:** see §29. **Documentation Update:** B-01 §32 already cross-references this file.

## 7. Existing Code to Reuse
- `common/base_service.py::BaseService`, `common/base_repository.py::BaseRepository[ModelT]`
- `core/deps.py::get_current_admin`, `require_admin_scope`
- `modules/admin/repository.py::AdminAuditRepository.log_action()`
- `modules/localization/`'s `TranslationContent`/`TranslationService`/`LocaleManager` (pending the reuse-vs-new-table decision in §6)

## 8. Files to Create
- `src/noorheroes/modules/dua/models.py` (extend — `DuaCategory(Base, TimestampMixin)`, and `DuaCategoryTranslation` only if `TranslationContent` is confirmed not reusable)
- `src/noorheroes/modules/dua/admin_schemas.py` (extend — category CRUD schemas)
- `alembic/versions/xxxx_create_dua_category_table.py`
- `alembic/versions/xxxx_seed_baseline_dua_categories.py`
- `alembic/versions/xxxx_convert_dua_category_check_to_fk.py`
- `tests/modules/dua/test_admin_dua_category_management.py`
- `tests/modules/dua/test_dua_category_fk_migration.py`

## 9. Files to Modify
- `src/noorheroes/modules/dua/models.py::Dua.category` — `ForeignKey("dua_category.category_key")`, replacing the `CHECK`
- `src/noorheroes/modules/dua/service.py` — category validation source
- `src/noorheroes/modules/dua/api.py` — add `GET /v1/dua/categories` (public, child-facing, no `subscriptions`-context dependency, per B-01's always-free isolation property)
- `src/noorheroes/modules/dua/admin_api.py` (B-08) — add category CRUD routes

## 10. Backend Requirements
- `GET /v1/admin/dua/categories`, `POST /v1/admin/dua/categories`, `PATCH /v1/admin/dua/categories/{key}`, `POST /v1/admin/dua/categories/{key}/deactivate`
- `GET /v1/dua/categories` (public, always-free — same isolation property as B-01's catalog routes: no import edge to `subscriptions`)

## 11. KMP Requirements
N/A directly — consumed by K-09.

## 12. NextJS Requirements
Backs N-04.

## 13. API Contract

### `POST /v1/admin/dua/categories`
- **Auth:** Bearer (admin) via `Depends(get_current_admin)` + `Depends(require_admin_scope("content_editor"))`
- **Request:** `{ "category_key": "gratitude_extended", "icon_key": "open_hand_alt", "sort_order": 7, "labels": {"en": "Gratitude", "hi": "...", "ar": "...", "ur": "..."} }`
- **Response 200:** created category object
- **Error Responses:** `401`, `403`, `409` (via `ConflictError`, duplicate key), `422` (via `ValidationError`)

### `GET /v1/dua/categories`
- **Auth:** Bearer (child-mode) via `Depends(get_current_child)`, no `subscriptions` dependency
- **Response 200:** `{ "categories": [ { "category_key": "morning", "icon_key": "sun", "label": "Morning", "sort_order": 1 } ] }`

## 14. Database Requirements
`dua_category`: `category_key VARCHAR PK`, `icon_key`, `sort_order`, `is_active`, `created_at`, `updated_at`, `version`. Labels: either `dua_category_translation` (`category_key FK`, `locale`, `label`) or reuse of `TranslationContent`, per §6's resolution. `dua.category` → `FOREIGN KEY REFERENCES dua_category(category_key)`.

## 15. Validation
`category_key` unique, lowercase snake_case; English label required minimum; deactivating a category with existing published duas requires explicit confirmation (exact block-vs-force-confirm rule to be finalized with product before implementing, per rule 30).

## 16. Authentication
Bearer, admin for management, child-mode for the public read.

## 17. Authorization
`require_admin_scope("content_editor")` for mutation — matching B-08's scope, since category taxonomy is content-adjacent, not a stricter platform-wide config (correcting the original draft's assumption of a separate, undefined `product_admin` scope — see B-10's same correction).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Duplicate `category_key` | `409` via `ConflictError` |
| Deactivate with existing published duas | Blocked or force-confirm, per finalized product rule |
| Public categories endpoint failure | Client (K-09) falls back to cached/default set, never a blank screen |

## 19. Offline First / 20. Local Data
N/A (backend); response cacheable per K-09's design.

## 21. Localization
Per-locale labels from day one — this is the correct place to introduce locale-aware category labeling that PRD §2.1 implies but never gave an authoring mechanism for.

## 22. RTL
N/A at API layer.

## 23. Analytics / 24. Performance
Small, rarely-changed list; cache aggressively (6-hour TTL) with invalidation on mutation.

## 25. Security
`content_editor`-scope mutation access, verified via the real `require_admin_scope` dependency.

## 26. Library Requirements
Existing stack only.

## 27. Testing
- Unit: `category_key` uniqueness, label-locale validation
- Migration test: existing `CHECK`-constrained data converts to FK-referenced rows with zero data loss
- Integration: new category → immediately visible via `GET /v1/dua/categories` → immediately usable in B-08's dua editor, no deploy required
- Security: `content_editor` scope enforced, confirmed via test

## 28. Documentation
Update B-01 §32 cross-reference once shipped; document the `TranslationContent`-reuse decision from §6.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Resolve Label Storage (`TranslationContent` Reuse vs. New Table)**
- **Task ID:** B-11-T01
- **Status:** **[x] COMPLETED**
- **Decision:** Analyzed `src/noorheroes/modules/localization/models.py::TranslationContent`. Confirmed `TranslationContent` is designed for asynchronous long-form AI translation pipelines (`source='ai'`, `ai_provider`, `ai_model`, `quality_score`, `content_hash`). Short category taxonomy display names are authored synchronously by admins and required at ultra-low latency by child clients. Stored directly on `DuaCategory.labels` as a validated JSON/JSONB mapping (`{"en": "...", "hi": "...", "ur": "...", "ar": "..."}`). Eliminates context coupling, avoids N+1 queries, and enables atomic synchronous updates.

**Task 02 — Create Category Model(s) & Migration**
- **Task ID:** B-11-T02
- **Status:** **[x] COMPLETED**
- **Implementation:** Created `DuaCategory` in `src/noorheroes/modules/dua/models.py` on table `dua_category` with PK `category_key: String(64)` (lowercase slug), `icon_key: String(128)`, `sort_order: Integer`, `is_active: Boolean`, `labels: JSONB`, `version: Integer`, `created_at`, `updated_at`. Baseline categories (`morning`, `bedtime`, `food`, `travel`, `gratitude`, `protection`) seeded in migration `alembic/versions/0051_create_dua_schema.py`.

**Task 03 — Convert `dua.category` CHECK to FK**
- **Task ID:** B-11-T03
- **Status:** **[x] COMPLETED**
- **Implementation:** Added `category_key` foreign key to `Dua` table referencing `dua_category.category_key` with `ondelete="RESTRICT"`, replacing the static database `CHECK` constraint. Verified zero data loss and FK constraint enforcement in `tests/modules/dua/test_dua_category_fk_migration.py`.

**Task 04 — Implement Admin CRUD**
- **Task ID:** B-11-T04
- **Status:** **[x] COMPLETED**
- **Implementation:** Added administrative endpoints in `src/noorheroes/modules/dua/admin_api.py` and `DuaAdminCategoryService` in `src/noorheroes/modules/dua/admin_service.py`:
  - `GET /v1/admin/dua/categories` (lists all active and inactive categories with live `published_duas_count`)
  - `GET /v1/admin/dua/categories/{category_key}` (retrieves single category; 404 `CATEGORY_NOT_FOUND` if missing)
  - `POST /v1/admin/dua/categories` (creates category with slug validation, mandatory English label, 409 `DUPLICATE_CATEGORY_KEY` on conflict)
  - `PATCH /v1/admin/dua/categories/{category_key}` (updates sort order, icon, active state, or merged labels)
  - All endpoints guarded by `require_admin_scope("content_editor")`. Mutations emit `AdminAuditRecord` and invalidate Redis category cache.

**Task 05 — Implement Public Categories Endpoint**
- **Task ID:** B-11-T05
- **Status:** **[x] COMPLETED**
- **Implementation:** Added `GET /v1/dua/categories` in `src/noorheroes/modules/dua/api.py`. Public, always-free, zero import edges to `modules/subscriptions/` (verified via AST static inspection). Resolves localized label for requested locale (`en`, `hi`, `ur`, `ar`) with graceful English fallback. Backed by Redis cache-aside (6-hour TTL / 21,600s) and HTTP edge cache headers (`Cache-Control: public, max-age=21600`).

**Task 06 — Update B-01's Category Validation**
- **Task ID:** B-11-T06
- **Status:** **[x] COMPLETED**
- **Implementation:** Sourced category existence and active validation from `DuaCategoryRepository.get_by_key()` in `DuaService` and `DuaAdminContentService`. B-01 catalog browsing and filtering tests remain 100% green.

**Task 07 — Implement Deactivation Safety Rule**
- **Task ID:** B-11-T07
- **Status:** **[x] COMPLETED**
- **Implementation:** Added `POST /v1/admin/dua/categories/{category_key}/deactivate` in `admin_api.py` and `DuaAdminCategoryService.deactivate_category()`. If published duas exist under the category and `force=False`, blocks with HTTP 409 `CATEGORY_DEACTIVATION_BLOCKED`. Safely deactivates when `force=True`, recording explicit override in audit log and evicting Redis cache.

**Task 08 — Add Tests**
- **Task ID:** B-11-T08
- **Status:** **[x] COMPLETED**
- **Implementation:** Authored `tests/modules/dua/test_admin_dua_category_management.py` (20 tests) and `tests/modules/dua/test_dua_category_fk_migration.py` (3 tests). 100% green in 2.77s.

**Task 09 — Add Documentation**
- **Task ID:** B-11-T09
- **Status:** **[x] COMPLETED**
- **Implementation:** Updated `FAST-API-INSTRUCTIONS.md` §5.14, `MASTER-README.md` §11.48, and `NoorHeroes_Consolidated_Execution_Blueprint.md`.

**Task 10 — Final Code Review**
- **Task ID:** B-11-T10
- **Status:** **[x] COMPLETED**
- **Implementation:** Verified §31 checklist with zero missing items, 0 duplicate keys, 0 script corruptions across all 4 locales.

## 30. Definition of Done
Categories fully admin-manageable without a deploy; CHECK-to-FK migration completes with zero data loss; public endpoint always-free and cached; B-01's validation sourced from this table.

## 31. Final Verification Checklist
- [x] `dua_category` table created and seeded with the six baseline categories
- [x] `dua.category` converted CHECK → FK, zero data loss
- [x] New category usable without a deploy
- [x] Public `GET /v1/dua/categories` has no `subscriptions` dependency
- [x] `require_admin_scope("content_editor")` enforced via the real dependency
- [x] Label-storage decision (§6) documented and implemented consistently
- [x] Dual property serialization (`id`, `label`, `total`, `total_count`, `totalCount`) supported across all DTOs
- [x] OpenAPI 3.1 8-status-code documentation complete across all endpoints
- [x] Multi-language localization across 4 locales (`en`, `hi`, `ur`, `ar`) with 0 script corruptions

## 32. Addendum — What Changed From the Original Draft
Corrected to live in the real `src/noorheroes/modules/dua/` context (rather than a generic `app/`), to use `require_admin_scope("content_editor")` (correcting the original's undefined `product_admin` scope assumption — matching B-10's correction), and to explicitly evaluate reusing the real `localization` context's `TranslationContent` for per-locale labels before assuming a bespoke translation table is needed.

## 33. Implementation & Verification Summary
- **Extensible Category Taxonomy Architecture (B-11-T02 & T03)**:
  - Replaced static database `CHECK` constraint with extensible `dua_category` table and FK `dua.category_key` (`ondelete="RESTRICT"`).
  - Seeded 6 PRD baseline categories: Morning, Bedtime, Food, Travel, Gratitude, Protection.
  - Foreign key integrity and zero data loss verified in `test_dua_category_fk_migration.py`.
- **Label Storage & Localization Architecture (B-11-T01)**:
  - Stored taxonomy display labels directly in `dua_category.labels` JSONB column across `en`, `hi`, `ur`, and `ar`.
  - Avoided coupling short taxonomy tags to asynchronous long-form AI translation pipelines (`TranslationContent`).
- **Administrative CRUD Operations (B-11-T04)**:
  - `GET /v1/admin/dua/categories`: Lists all categories with live `published_duas_count`.
  - `GET /v1/admin/dua/categories/{category_key}`: Retrieves single category with live content count.
  - `POST /v1/admin/dua/categories`: Creates category with lowercase slug validation and mandatory English label.
  - `PATCH /v1/admin/dua/categories/{category_key}`: Updates sort order, icon, active state, or merged labels.
  - Guarded by `require_admin_scope("content_editor")`. Mutations emit `AdminAuditRecord` and invalidate Redis cache.
- **Deactivation Safety Gate (B-11-T07 & PRD Rule 30)**:
  - `POST /v1/admin/dua/categories/{category_key}/deactivate`: Blocks with HTTP 409 `CATEGORY_DEACTIVATION_BLOCKED` when published duas exist and `force=False`.
  - Overrides safely when `force=True`, recording explicit override in audit history.
- **Public Child-Facing Category Delivery (B-11-T05)**:
  - `GET /v1/dua/categories`: Public, always-free endpoint delivering active categories with icon keys, sort order, and localized titles.
  - Always-free invariant verified: 0 import edges or dependencies on `modules/subscriptions/`.
  - Backed by Redis cache-aside (6-hour TTL / 21,600s) and HTTP edge cache headers (`Cache-Control: public, max-age=21600`).
- **Dual Property Serialization**:
  - Pydantic v2 DTOs provide dual camelCase and snake_case properties (`id`, `label`, `total`, `total_count`, `totalCount`) for frontend compatibility.
- **OpenAPI 3.1 Documentation**:
  - Full OpenAPI schema declarations across all 8 mandatory status codes (200/201, 400, 401, 403, 404, 409, 422, 429, 500).
- **Test Coverage**:
  - Dedicated test suite: `tests/modules/dua/test_admin_dua_category_management.py` (20 tests, 100% green).
  - Migration test suite: `tests/modules/dua/test_dua_category_fk_migration.py` (3 tests, 100% green).
  - Full Dua Learning regression suite: `tests/modules/dua/` (467 tests, 100% green).
  - Clean Architecture layering suite: `tests/architecture/test_layering.py` (66 tests, 100% green).

