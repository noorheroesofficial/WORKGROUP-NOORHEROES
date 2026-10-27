# B-03 — Favorite Data Model Reconciliation & Legacy Migration

## 1. Feature Context
Architecture-improvement prerequisite for Feature B.14 Favorites. Discovered via cross-blueprint research: three incompatible definitions of the "shared `favorite` table" exist across A.3, A.6, and this PRD. This blueprint is the single source of truth that reconciles them and MUST be implemented and merged before B-01, B-02, K-01, K-02, K-03 are built or deployed.

## 2. Parent Feature
B.14 Favorites (`PRD_Documents/Child App — Supporting (13-18)/Feature_B14_Favorites.md`), reconciling `Development_Blueprints/A3_Stories_Module/Backend/09-story-favorites-api.md` and `Development_Blueprints/A6_Dua_Learning/Backend/04-dua-favorites-api.md`.

## 3. Sub-feature
1.3 Favorite Data Model Reconciliation & Legacy Migration — `B-03`

## 4. Objective
Establish one canonical `favorite` table definition and one canonical service/router location, migrate A.3's already-shipped narrow schema to it without data loss, and correct A.6's blueprint file-path references that assume a non-existent module layout.

## 5. Business Requirements
No direct FR — this is an architecture-integrity prerequisite. Indirectly supports FR-4 (per-child isolation) and FR-5 (idempotent toggle) by ensuring both B-01 and B-02 operate against one real, consistent schema instead of two conflicting assumptions.

## 6. Existing Architecture

**As actually built (A.3, `09-story-favorites-api.md`):** `favorite` table = `favorite_id PK`, `child_id FK`, `episode_id FK`, `created_at`. No `content_type` column. `UNIQUE(child_id, episode_id)`. Endpoints on `ContentRouter`: `POST /v1/favorites` (body `{episode_id}`), `DELETE /v1/favorites/{episode_id}`, `GET /v1/favorites` (implicit child from token, no path `id`). Model at `src/noorheroes/modules/content/favorite_models.py::FavoriteOrm`.

**As assumed, not built (A.6, `04-dua-favorites-api.md`):** assumes a generic table already exists with `content_id`, `content_type`, `client_event_id`, at `app/models/favorite.py`, `app/services/favorite_service.py`, `app/routers/favorite_router.py`. This `app/` path convention does not match the real FastAPI structure documented in `FAST-API-INSTRUCTIONS.md` (`src/noorheroes/modules/<context>/`).

**As specified, canonical target (this PRD, §4.1):** `favorite_id PK`, `child_id FK`, `content_id`, `content_type`, `created_at`. Declared "the canonical, complete definition."

**Problem:** three non-identical definitions of the same conceptual table, two of which (A.3 built, A.6 assumed) are mutually incompatible in both schema and file location. Implementing B-01/B-02 against any single one of these without reconciliation will either break A.3's shipped favoriting feature or leave A.6's favoriting feature building against files that don't exist. (The same pattern repeats on the KMP side — see K-01's Existing Architecture section: A.3's `08-story-favorites-parent-gated-sharing.md` built story-specific, non-parameterized UI/data classes, while A.6's `06-dua-favorites-management.md` assumed a shared, parameterized component already existed. This backend blueprint does not own the KMP-side fix, but the two mirror each other.)

**Proposed Improvement:** extend `src/noorheroes/modules/content/favorite_models.py::FavoriteOrm` in place — this is the real, already-migrated table, so it is the correct migration target (not a new table, not a new module). Add `content_id` (nullable initially, then backfilled and constrained), add `content_type` (nullable initially, backfilled to `'story'` for all existing rows, then constrained `NOT NULL` with a `CHECK` allowlist). Retire `episode_id` as a distinct column by treating it as `content_id` going forward for `content_type='story'` rows (confirm with Backend Architect whether to keep `episode_id` as a generated/computed alias for backward-compat call sites, or fully rename — flagged as an open decision, not resolved here). Introduce a dedicated `FavoriteService`/`FavoriteRepository` pair (if not already factored out from A.3's `ContentRouter`-embedded logic) as the single call site for B-01/B-02 and any future content-type integration (games, avatars).

**Impact:** A.3's shipped `POST /v1/favorites` (body `{episode_id}`), `DELETE /v1/favorites/{episode_id}`, `GET /v1/favorites` endpoints must be superseded by B-01/B-02's generic shape — coordinate a deprecation window rather than a hard cutover if A.3's Android client is already live against the old contract. **Recommended default:** treat this as a soft cutover — ship B-01/B-02's generic endpoints alongside A.3's existing ones for one release cycle, route A.3's legacy handlers to internally call the new generic service (so there is only one write path, just two URL shapes), then remove the legacy routes once the KMP app has fully migrated to K-01/K-03. This avoids a hard-break risk without requiring an assumption about A.3's exact release/live status. A.6's blueprint (`04-dua-favorites-api.md`) must be corrected: file references change from `app/models/favorite.py` / `app/services/favorite_service.py` / `app/routers/favorite_router.py` to `src/noorheroes/modules/content/favorite_models.py` / `favorite_service.py` / `content/api.py`. Any other module (A.5 Quran/Arabic) that has not yet built its own favoriting must be pointed at this canonical service from the start — no parallel implementation.

**Implementation:** additive, backward-compatible Alembic migration; backfill script; application-layer cutover of A.3's router to internally delegate to the new generic service (per the recommended soft-cutover above).

**Documentation Update:** correct `Development_Blueprints/A6_Dua_Learning/Backend/04-dua-favorites-api.md` file-path references. Add the canonical `favorite` table definition to a shared architecture reference (recommend adding a "Shared Domain Tables" section to `FAST-API-INSTRUCTIONS.md` or an equivalent shared doc, since this is the second cross-feature-shared table pattern found in the codebase after `reward_ledger`-style shared tables referenced elsewhere).

## 7. Existing Code to Reuse
- `src/noorheroes/modules/content/favorite_models.py::FavoriteOrm` (migration target, not a new model)
- A.3's existing `ContentRouter` favorite endpoints (retained temporarily as thin delegates during the soft-cutover window)
- `common/base_repository.py` conventions for the new `FavoriteRepository`

## 8. Files to Create
- `alembic/versions/xxxx_generalize_favorite_table.py`
- `src/noorheroes/modules/content/favorite_service.py` (if not already factored out separately from `service.py`)
- `src/noorheroes/modules/content/favorite_repository.py` (if not already factored out)
- `tests/modules/content/test_favorite_migration.py`

## 9. Files to Modify
- `src/noorheroes/modules/content/favorite_models.py::FavoriteOrm`
- `src/noorheroes/modules/content/api.py::ContentRouter` (A.3's existing favorite endpoints — converted to thin delegates per the soft-cutover plan)
- `Development_Blueprints/A6_Dua_Learning/Backend/04-dua-favorites-api.md` (documentation correction, not application code)

## 10. Backend Requirements
- Migration must be additive and reversible.
- Backfill must run inside the same migration or a clearly sequenced follow-up data-migration script, not left as a manual/undocumented step.
- No existing favorite row may be lost or orphaned during migration.
- A.3's legacy endpoints become thin delegates to the new `FavoriteService` during the soft-cutover window (see §6), not a second parallel implementation.

## 11. KMP Requirements
None directly — K-01/K-02/K-03 depend on this being complete but contain no code changes of their own here.

## 12. NextJS Requirements
None.

## 13. API Contract
Not applicable — this blueprint is schema/service-layer only. B-01 and B-02 own the resulting API contracts.

## 14. Database Requirements
```sql
ALTER TABLE favorite ADD COLUMN content_id TEXT;
ALTER TABLE favorite ADD COLUMN content_type TEXT;
UPDATE favorite SET content_id = episode_id::text, content_type = 'story' WHERE content_type IS NULL;
ALTER TABLE favorite ALTER COLUMN content_id SET NOT NULL;
ALTER TABLE favorite ALTER COLUMN content_type SET NOT NULL;
ALTER TABLE favorite ADD CONSTRAINT favorite_content_type_check CHECK (content_type IN ('story','surah','dua'));
ALTER TABLE favorite ADD CONSTRAINT favorite_unique_child_content UNIQUE (child_id, content_id, content_type);
CREATE INDEX favorite_child_type_created_idx ON favorite (child_id, content_type, created_at DESC);
```
*(Illustrative SQL derived directly from the PRD's stated canonical schema and the researched existing A.3 schema — exact column types/constraint names must be confirmed against the live `favorite_id`/`child_id`/`episode_id` column types before running, not assumed here.)*

## 15. Validation
Migration dry-run against a staging copy of production data; row-count-before equals row-count-after; zero `NULL` `content_id`/`content_type` post-migration.

## 16. Authentication
N/A (migration-level work).

## 17. Authorization
N/A.

## 18. Error Handling
Migration failure must not leave the table in a partially-altered state — wrap in a transaction where the database supports transactional DDL; provide a documented manual rollback path if not.

## 19. Offline First
N/A.

## 20. Local Data
N/A.

## 21. Localization
N/A.

## 22. RTL
N/A.

## 23. Analytics
N/A.

## 24. Performance
For large `favorite` tables, prefer a batched backfill (chunked `UPDATE`) over a single full-table lock, consistent with standard zero-downtime migration practice — confirm current table size before deciding batching necessity.

## 25. Security
No PII introduced. Do not modify PostgreSQL credentials as part of this migration.

## 26. Library Requirements
Alembic, SQLAlchemy 2.0.

## 27. Testing
- Migration smoke test (upgrade/downgrade both succeed).
- Backfill correctness test: pre-existing A.3 favorite rows have `content_type='story'` and `content_id=episode_id` post-migration.
- Constraint test: `UNIQUE`/`CHECK` reject invalid inserts post-migration.
- Regression test: A.3's existing (now-delegating) endpoints still return identical results during the soft-cutover window.

## 28. Documentation
Migration changelog entry; A.6 blueprint correction (file paths); new "Shared Domain Tables" architecture note (recommended, not mandatory to block this task).

## 29. AI Coding Agent Implementation Steps
**Task 01 — Snapshot Current Schema.** Confirm exact live column types for `favorite_id`, `child_id`, `episode_id` before writing the migration.
**Task 02 — Write Additive Migration.** Add `content_id`/`content_type`, nullable first.
**Task 03 — Write Backfill Script/Statement.** `content_type='story'`, `content_id=episode_id` for existing rows, batched if table is large.
**Task 04 — Constrain Columns.** `NOT NULL`, `CHECK`, `UNIQUE` after backfill completes and is verified.
**Task 05 — Factor Out `FavoriteService`/`FavoriteRepository`.** If not already separated from A.3's inline `ContentRouter` logic.
**Task 06 — Convert A.3's Legacy Endpoints to Delegates.** Per the recommended soft-cutover plan in §6 — confirm with Backend Architect whether a full hard cutover is preferred instead if A.3's client is confirmed not yet live.
**Task 07 — Correct A.6 Blueprint File References.** Documentation-only change to `04-dua-favorites-api.md`.
**Task 08 — Write Migration/Backfill Tests.** Per §27.
**Task 09 — Final Code Review.** Confirm B-01/B-02 can build cleanly against the post-migration schema.

## 30. Definition of Done
Migration applied cleanly to a staging snapshot with zero data loss; backfill-correctness test green; constraint tests green; A.6 blueprint corrected; soft-cutover delegation verified against A.3's existing endpoint behavior.

## 31. Final Verification Checklist
- [ ] Zero orphaned or `NULL` rows post-migration
- [ ] `UNIQUE`/`CHECK` constraints enforced
- [ ] A.3's existing favorite data preserved and correctly typed
- [ ] A.6 blueprint file references corrected
- [ ] A.3's legacy endpoints converted to delegates (soft cutover) or confirmed safe for hard cutover
- [ ] PostgreSQL credentials untouched
- [ ] Rollback path documented
