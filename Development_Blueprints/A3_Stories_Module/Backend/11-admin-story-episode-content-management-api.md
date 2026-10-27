# B-11 — Admin Story & Episode Content Management API

## 1. Feature Context
The editorial backbone: creates and versions story series/episodes, configures unlock thresholds, bedtime eligibility, and choice points (hard-capped at 3 options, mirrored in the Android player and the admin UI). Delete is always "Archive" — no hard delete exists anywhere in this surface.

## 2. Parent Feature
Feature A.3 — Stories Module (Animated Storytelling System)

## 3. Sub-feature
1.11 Admin Story & Episode Content Management API (ID: **B-11**)

## 4. Objective
Implement admin CRUD for `story_series`/`story_episode`/`choice_point` inside the existing `content` + `admin` modules, gated by the `content_editor` RBAC role, with a draft → pending_review → published versioning workflow and full audit logging.

## 5. Business Requirements
- §8 Admin Requirements: create draft + version, configure `unlock_threshold_config`, mark `is_bedtime_eligible`, define choice-point options (max 3), scholar-approval workflow status; delete = archive only.
- §9 Admin AI Code-Generation Prompt: choice-point builder hard-caps at 3 options server-side, matching Android/backend constraints exactly; new version → `status=pending_review`; only approved version → `status=published`.
- CRUD permissions: full CRUD (delete = archive only) behind `content_editor` role.

## 6. Existing Architecture
Extends the existing `content` module's write path and the existing `admin` module's audit-logging pattern (`AdminAuditRepository.log_action()`). Router → Service → Repository → Postgres, `require_admin_scope("content_editor")` dependency mirroring the existing `admin:write` scope pattern.

## 7. Existing Code to Reuse
- `modules/admin/service.py::AdminService.log_action()` (audit logging — reuse for every mutation)
- `core/deps.py::get_current_admin`, `require_admin_scope()`
- `modules/content/story_repository.py::StoryEpisodeRepository` (B-01, extend with write methods)
- `common/base_service.py`, `common/base_repository.py`

## 8. Files to Create
- `src/noorheroes/modules/content/admin_content_schemas.py` — `SeriesCreateRequest`, `EpisodeCreateRequest`, `EpisodeUpdateRequest`, `ChoicePointBuilderRequest` (hard-validates ≤3 options), `VersionSubmitRequest`
- `src/noorheroes/modules/content/admin_content_service.py` — `AdminContentService(BaseService)`
- `tests/modules/content/test_admin_content_service.py`
- `tests/modules/content/test_admin_content_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/content/api.py::ContentRouter` — add admin-scoped routes under `/v1/admin/content/...`
- `src/noorheroes/modules/content/story_repository.py::StoryEpisodeRepository` — add `create()`, `update()`, `archive()`, `get_version_history()`

## 10. Backend Requirements
- `AdminContentService.create_draft(series_id, episode_payload)`: creates a new `story_episode` version at `status=draft`; `ChoicePointBuilderRequest` schema-level validation rejects a 4th option (`max_items=3` on the Pydantic list field) before it ever reaches the database.
- `AdminContentService.submit_for_review(episode_id, version_id)`: transitions `status=pending_review`; only a scholar-approved version (workflow state owned by B-12's review process for morals, and a separate content-approval workflow here for the episode itself) may transition to `status=published`.
- `AdminContentService.archive(episode_id)`: sets `status=archived` — no delete method exists in the repository or service at all (not merely unused; the DELETE HTTP verb is never wired to this router).
- Every mutation calls `AdminService.log_action(admin_id, action, before, after)` before returning.
- Duplicate `episode_number` within a series rejected at the service layer (defense in depth alongside the `UNIQUE(series_id, episode_number)` DB constraint from B-01).

## 11. API Contract

### `POST /v1/admin/content/series`
- Auth: Admin Bearer + `content_editor` scope. Request: series metadata. Response 201: created series (draft).

### `POST /v1/admin/content/series/{series_id}/episodes`
- Auth: Admin Bearer + `content_editor` scope. Request: episode metadata incl. `unlock_threshold_config`, `is_bedtime_eligible`, `choice_points` (≤3 options each). Response 201: created episode (draft).

### `PATCH /v1/admin/content/episodes/{episode_id}`
- Auth: Admin Bearer + `content_editor` scope. Request: partial update, creates a new version. Response 200: updated episode version.

### `POST /v1/admin/content/episodes/{episode_id}/submit-review`
- Auth: Admin Bearer + `content_editor` scope. Response 200: `{ status: "pending_review" }`.

### `POST /v1/admin/content/episodes/{episode_id}/publish`
- Auth: Admin Bearer + `content_editor` scope. Precondition: version must be in an approved state. Response 200: `{ status: "published" }`. Errors: `409 VERSION_NOT_APPROVED`.

### `POST /v1/admin/content/episodes/{episode_id}/archive`
- Auth: Admin Bearer + `content_editor` scope. Response 200: `{ status: "archived" }`. (This is the only "delete" surface — relabeled, soft-only.)

### `GET /v1/admin/content/episodes/{episode_id}/versions`
- Auth: Admin Bearer + `content_editor` scope. Response 200: version history/diff.

## 12. Database Requirements
- Writes to `story_series`, `story_episode`, `choice_point` (all owned/created in B-01/B-05's migrations; this sub-feature adds no new tables, only the write-path service/routes, plus a `status`/version-tracking column set on `story_episode` if not already present from B-01 — coding agent should confirm and add `status` (`draft|pending_review|published|archived`) and `version_number` columns via a migration here if B-01 did not already include them).
- `alembic/versions/xxxx_add_story_episode_status_version.py` (if needed per above).

## 13. Validation
- Choice-point options: schema-enforced `max_items=3`, plus a service-layer assertion as defense in depth.
- `unlock_threshold_config`: validated against exactly the three supported shapes (`playback_percentage`, `final_interaction`, `quiz_completion`) — malformed config rejected at write time (`422`), preventing B-02 from ever encountering an unrecognized shape.
- Duplicate `episode_number` within a series rejected (`409 DUPLICATE_EPISODE_NUMBER`).

## 14. Authentication
Admin Bearer via `get_current_admin`.

## 15. Authorization
`require_admin_scope("content_editor")` on every mutating route; read-only version-history route may allow a broader admin scope if consistent with existing patterns (coding agent to confirm against `admin` module conventions).

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| 4th choice-point option submitted | `422` at schema validation, never reaches the service layer |
| Duplicate episode number in series | `409 DUPLICATE_EPISODE_NUMBER` |
| Publish attempted on unapproved version | `409 VERSION_NOT_APPROVED` |
| Invalid `unlock_threshold_config` shape | `422 INVALID_UNLOCK_CONFIG` |
| Unauthorized/forbidden admin request | `401`/`403` |
| Database failure | `503`, logged, audit log NOT written for a failed mutation (only successful mutations are audited) |

## 17. Security
- `content_editor` RBAC enforced at the router dependency layer (API-level, not just UI-level) — defense in depth with N-01's frontend button-disabling.
- Full immutable audit trail (admin_id, action, before/after diff, timestamp) on every mutation via `AdminService.log_action()`.
- No delete capability exists anywhere in this API surface — architecturally impossible to hard-delete content through this path.

## 18. Analytics
Internal admin action — audited via `AdminAuditLog` (§17), not the child-facing analytics taxonomy.

## 19. Performance
Admin write volume is low relative to read-heavy child-facing endpoints — no special caching/performance requirements beyond standard indexed writes.

## 20. Library Requirements
No new libraries.

## 21. Testing
- Unit: 3-option cap enforcement (schema + service layer), duplicate-episode-number rejection, unlock-config-shape validation, publish-without-approval rejection.
- Integration: full draft → pending_review → published lifecycle; audit log written on every successful mutation and absent on failed ones; archive never physically removes the row (verify row still exists post-archive with `status=archived`).

## 22. Documentation
Update OpenAPI schema; document the versioning state machine (`draft → pending_review → published`, `* → archived`) in the module README.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Add `status`/`version_number` Columns to `story_episode` (if not present) & Migration**
Objective: Support the versioning workflow. Follow: existing Alembic conventions. Do Not Change: existing `story_episode` columns from B-01 beyond this additive change. Tests: migration smoke test. Definition of Done: clean migration.

**Task 02 — Implement Admin Content Schemas with 3-Option Cap**
Objective: `admin_content_schemas.py` with `max_items=3` on `ChoicePointBuilderRequest.options`. Tests: schema rejects a 4th option. Definition of Done: test passes.

**Task 03 — Extend `StoryEpisodeRepository` with Write Methods**
Objective: `create()`, `update()` (versioned), `archive()`, `get_version_history()`. Follow: `BaseRepository`. Business Rules: no `delete()` method exists. Tests: archive preserves the row. Definition of Done: repository methods covered.

**Task 04 — Implement `AdminContentService`**
Objective: Business logic for the full draft→review→publish→archive lifecycle, unlock-config validation, duplicate-episode-number rejection, audit-log wiring. Dependencies: Task 01–03, `AdminService.log_action()`. Tests: all §21 unit cases. Definition of Done: tests pass.

**Task 05 — Add Router Endpoints**
Objective: Wire all six admin routes under `require_admin_scope("content_editor")`. Tests: covered by Task 07. Definition of Done: endpoints live, documented, RBAC-gated.

**Task 06 — Wire Audit Logging on Every Mutation**
Objective: Call `AdminService.log_action()` with before/after diff on every successful create/update/submit/publish/archive. Tests: audit row exists after each mutation type, absent after a failed one. Definition of Done: test passes.

**Task 07 — Add Unit & Integration Tests**
Objective: Full coverage per §21, including the full lifecycle integration test. Definition of Done: all green in CI.

**Task 08 — Update OpenAPI Documentation**
Objective: Regenerate/diff-classify; document the versioning state machine. Definition of Done: non-breaking diff confirmed.

**Task 09 — Final Code Review**
Objective: Confirm no delete/DELETE-verb code path exists anywhere in this router; confirm the 3-option cap is enforced at both schema and service layers matching N-01's frontend and K-04's Android assertion exactly. Definition of Done: checklist in §24 fully checked.

## 24. Final Verification Checklist
- [ ] A 4th choice-point option is rejected at schema validation, never persisted
- [ ] No delete/DELETE-verb capability exists anywhere in this router — archive is the only removal path
- [ ] Duplicate episode numbers within a series rejected
- [ ] `unlock_threshold_config` validated against exactly the three supported shapes at write time
- [ ] Publish blocked (`409`) unless the version is in an approved state
- [ ] Every successful mutation writes an immutable audit log row (admin_id, action, before/after, timestamp)
- [ ] `content_editor` RBAC enforced at the API layer, not just the UI
- [ ] Archived content rows remain queryable (never physically removed)
- [ ] No PostgreSQL/Redis credentials modified

## 25. Definition of Done
Content editors can fully manage the story/episode catalog through a versioned, audited, archive-only workflow with a server-enforced 3-option choice-point cap — the exact data-integrity guarantees B-01 through B-08 assume are true of the content they read.
