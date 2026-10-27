# B-01 — Content Item & Version Management API

## 1. Feature Context
The canonical authoring/versioning store for every content type NoorHeroes ships (Story, Episode, Video, Audio, Text, Lesson, Quiz, Fact, Dua, Habit Template, Mission, Reward). Its single defining guarantee: a published version is never mutated in place — every edit is a new version requiring its own review cycle, enforced at the database permission layer, not just application logic.

## 2. Parent Feature
E.29 — Content CMS & Scholar Review Workflow

## 3. Sub-feature
1.1 Content Item & Version Management API (ID: **B-01**)

## 4. Objective
Implement a new `content_cms` bounded context with `content_item`/`content_version` CRUD, append-only versioning, and full version-history/diff retrieval, with published-version mutation structurally impossible at the database role-grant level.

## 5. Business Requirements
- FR-1: content model supports all 12 content types with locale, age band, difficulty, duration, free/premium flag, seasonal windows, sources, scholar notes, learning objectives, moral lesson, media tracks, captions, transcripts, thumbnails, download policy, versioning, preview, scheduling, rollback, archive.
- FR-12: editing a published item creates a new version, never mutates the published version in place.
- Edge Case 4: editing episode N after N+1 is published creates a new draft version for N; N+1's live publish state is unaffected.
- Edge Case 8: concurrent edits to the same draft version — second save rejected with "this has changed, please refresh."

## 6. Existing Architecture
New `modules/content_cms/` bounded context, following the platform's existing 10-context modular-monolith layering (Router → Service → Repository → Postgres, `BaseService`/`BaseRepository`). Reuses E.28's `AuditLogService.log_action()` (internal-only, per E.28's B-05) for every transition — this module writes no audit log of its own.

## 7. Existing Code to Reuse
- `common/base_service.py`, `common/base_repository.py`
- `modules/admin/audit/service.py::AuditLogService.log_action()` (E.28 B-05, internal-only call)
- `core/deps.py::get_current_admin`, `require_admin_scope()`
- `core/exceptions.py`

## 8. Files to Create
- `src/noorheroes/modules/content_cms/models.py` — `ContentItemOrm`, `ContentVersionOrm`
- `alembic/versions/xxxx_create_content_item_version.py` — includes the `REVOKE UPDATE` grant on already-published `content_version` rows (see Task 03)
- `src/noorheroes/modules/content_cms/schemas.py` — `ContentCreateRequest`, `ContentUpdateRequest`, `ContentResponse`, `ContentVersionResponse`, `VersionDiffResponse`
- `src/noorheroes/modules/content_cms/repository.py` — `ContentItemRepository`, `ContentVersionRepository`
- `src/noorheroes/modules/content_cms/service.py` — `ContentService(BaseService)`
- `src/noorheroes/modules/content_cms/api.py` — `ContentRouter`
- `tests/modules/content_cms/test_content_service.py`
- `tests/modules/content_cms/test_content_api.py`
- `tests/modules/content_cms/test_published_version_permission_lockout.py`

## 9. Files to Modify
- `src/noorheroes/main.py` — register `ContentRouter` under `/v1/admin/content`

## 10. Backend Requirements
- `ContentService.create_draft(payload)`: creates `content_item` (if new) + `content_version` at `version_number=1, status=draft`.
- `ContentService.update(content_id, payload, actor_id)`: if the current version's `review_stage`/parent item `status != 'published'`, updates the existing draft row (with optimistic-concurrency check via a `updated_at`/version token — reject stale writes with `409 STALE_VERSION`); if the current version **is** published, inserts a brand-new `content_version` row at `version_number+1, status=draft` instead — never an UPDATE against the published row.
- `ContentService.get_versions(content_id)`: full ordered version list; `ContentService.diff(version_id_a, version_id_b)`: structural diff of `content_json` between two versions.
- `ContentService.archive(content_id, actor_id, reason)`: sets `status=archived`, preserves all version/review rows — no delete path exists.
- Every mutation calls `AuditLogService.log_action(actor_id, resource_type="content_item", resource_id, action, metadata)`.

## 11. API Contract

### `POST /v1/admin/content`
- Auth: `content_editor`+ role. Request: content-type-specific payload. Response 201: created draft.

### `GET /v1/admin/content`
- Auth: `content_editor`+ role. Response 200: paginated, filterable content list.

### `PATCH /v1/admin/content/{id}`
- Auth: `content_editor`+ role. Business Rule: against a `published` item, always creates a new version (FR-12). Response 200: updated/new version. Errors: `409 STALE_VERSION` (Edge Case 8).

### `GET /v1/admin/content/{id}/versions`
- Auth: `content_editor`+ role. Response 200: full version history with diff-capable pairs.

## 12. Database Requirements
- `content_item`: CHECK `content_type IN ('story','episode','video','audio','text','lesson','quiz','fact','dua','habit_template','mission','reward')`; CHECK `status IN ('draft','in_review','scheduled','published','suspended','archived')`; index `(content_type, status)`.
- `content_version`: FK `content_id`, `last_edited_by`; `UNIQUE(content_id, version_number)`; index `(content_id, version_number DESC)`.
- **Database-level permission lockout**: the application's DB role has `UPDATE` privilege on `content_version` revoked specifically for rows where the joined `content_item.status = 'published'` — implemented via a `BEFORE UPDATE` trigger/rule (since column-level or row-level conditional grants aren't natively expressible as a simple `REVOKE`) that raises an exception on any attempted UPDATE of a published version's row; migration must include this trigger, not just the table DDL.

## 13. Validation
- `content_type` restricted to the 12 canonical values.
- Optimistic-concurrency token (e.g., `updated_at` or a `version_token` field) required on every `PATCH`, compared server-side before accepting the write.

## 14. Authentication
Admin Bearer via `get_current_admin`.

## 15. Authorization
`require_admin_scope("content_editor")` (or higher) on all mutating routes; read routes may allow a broader scope per E.28's existing convention.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| PATCH against a published item | New version created, not an in-place update |
| Direct UPDATE attempted against a published `content_version` row (any code path) | Rejected by the database trigger — this is the actual enforcement point, tested independently of the application layer |
| Concurrent stale-token PATCH | `409 STALE_VERSION`, "this has changed, please refresh" |
| Unknown content ID | `404 CONTENT_NOT_FOUND` |
| Invalid `content_type` | `422` |
| Database failure | `503`, logged |

## 17. Security
- Published-version immutability is enforced at the database layer (trigger-based permission lockout), not merely application logic — defense against any future application bug ever mutating provenance-critical history.
- No delete capability exists anywhere in this module — archive only.

## 18. Analytics
Internal admin action — audited via `AuditLogService`, not the child-facing analytics taxonomy. `content_draft_created` is emitted as an audit-log entry, not a separate analytics event pipeline (this module has no consumer-facing analytics surface).

## 19. Performance
Version-history/diff queries indexed on `(content_id, version_number DESC)`; diff computation is a pure in-memory structural comparison of two `content_json` blobs, not a database-side operation.

## 20. Library Requirements
No new libraries — standard SQLAlchemy 2.0 async, Alembic, Postgres triggers.

## 21. Testing
- Unit: append-only versioning logic, optimistic-concurrency rejection, content-type enum validation.
- **Mandatory permission-lockout test**: attempt a direct SQL `UPDATE` against a published `content_version` row (bypassing the ORM/service layer entirely) and confirm the database itself rejects it — per PRD backend AI-prompt requirement #3, mirroring A.11's reward-ledger pattern.
- Integration: full draft → new-version-on-published-edit → version-history-with-diff flow.

## 22. Documentation
Update OpenAPI schema; document the trigger-based permission-lockout mechanism in the module README as a permanent architectural invariant.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Create `ContentItemOrm`/`ContentVersionOrm` Models & Migration**
Objective: Base tables per the PRD ER diagram. Follow: existing SQLAlchemy/Alembic conventions. Business Rules: CHECK constraints on `content_type`/`status`; `UNIQUE(content_id, version_number)`. Tests: migration smoke test. Definition of Done: clean migration.

**Task 02 — Implement `ContentItemRepository`/`ContentVersionRepository`**
Objective: CRUD + version-history queries. Follow: `BaseRepository`. Tests: version-ordering test. Definition of Done: repository methods covered.

**Task 03 — Implement Database-Level Published-Version Permission Lockout**
Objective: `BEFORE UPDATE` trigger/rule rejecting any UPDATE against a `content_version` row whose parent `content_item.status = 'published'`. Follow: Postgres trigger conventions, added via the same migration as Task 01 (or a follow-up migration). Business Rules: this is the actual enforcement point, not a UI/application convenience. Tests: **mandatory** — direct SQL UPDATE bypass test confirming database-level rejection. Definition of Done: bypass test passes, confirming zero application-layer dependency for this guarantee.

**Task 04 — Implement `ContentService` with Append-Only Update Logic**
Objective: draft-vs-published branching in `update()`, optimistic-concurrency check, archive. Dependencies: Task 01–03. Tests: stale-token rejection, published-edit-creates-new-version. Definition of Done: tests pass.

**Task 05 — Implement Version Diff**
Objective: structural diff between two `content_json` blobs. Dependencies: Task 02. Tests: diff correctness on a fixture pair. Definition of Done: test passes.

**Task 06 — Wire `AuditLogService.log_action()` on Every Mutation**
Objective: internal-only audit call, no local audit table. Dependencies: E.28 B-05. Tests: audit row exists after create/update/archive. Definition of Done: test passes.

**Task 07 — Add Router Endpoints**
Objective: Wire all four endpoints with `content_editor`+ scope. Tests: covered by Task 08. Definition of Done: endpoints live, documented.

**Task 08 — Add Unit & Integration Tests**
Objective: Full coverage per §21, including the mandatory permission-lockout bypass test. Definition of Done: all green in CI.

**Task 09 — Update OpenAPI Documentation**
Objective: Regenerate/diff-classify; document the trigger-based lockout invariant. Definition of Done: non-breaking diff confirmed.

**Task 10 — Final Code Review**
Objective: Confirm zero code path can UPDATE a published `content_version` row, confirm archive is the only removal affordance. Definition of Done: checklist in §24 fully checked.

## 24. Final Verification Checklist
- [ ] PATCH against a published item always creates a new version, never mutates in place
- [ ] Direct database UPDATE against a published `content_version` row is rejected at the trigger/permission layer, independent of the application code
- [ ] Concurrent stale-token PATCH rejected with `409 STALE_VERSION`
- [ ] Version history/diff retrievable for any two versions of an item
- [ ] Archive preserves all version/review rows — no delete path exists anywhere
- [ ] Every mutation writes an audit entry via `AuditLogService.log_action()` (E.28, internal-only)
- [ ] No PostgreSQL/Redis credentials modified

## 25. Definition of Done
Content items and versions are durably, append-only managed with database-enforced published-version immutability — the foundational data layer every other E.29 sub-feature (media, review workflow, publish, Quran, rewards) builds directly on top of.
