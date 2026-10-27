# B-08 — Offline Download Manifest API

## 1. Feature Context
Builds the manifest used by the KMP app's `DownloadRepository` to cache episodes for offline playback. Must include only currently-unlocked episodes at generation time — never pre-bundling locked future episodes — and must respect a parent's download policy as two distinct controls: "allow new downloads" and "revoke existing offline content."

## 2. Parent Feature
Feature A.3 — Stories Module (Animated Storytelling System)

## 3. Sub-feature
1.8 Offline Download Manifest API (ID: **B-08**)

## 4. Objective
Implement `POST /v1/downloads/manifest` inside the existing `media` module, filtering strictly to `episode_unlock_state.unlocked = true` rows via B-02, gated by parent download-policy checks, with resumable manifest semantics and a scheduled purge job.

## 5. Business Requirements
- FR-15: offline download manifests include only currently-unlocked episodes at manifest-generation time.
- Acceptance Criteria: a manifest for a 5-episode series with 2 unlocked returns exactly those 2 episodes' media, not all 5.
- Edge Case 7: parent disables downloads entirely while in-progress downloads exist → halted gracefully, not silently failed; already-completed downloads remain playable until parent explicitly additionally revokes offline access.
- §4.5 Retention: `download_manifest_record` purged after `expires_at` + 7 days grace.

## 6. Existing Architecture
Extends the existing `media` module alongside B-07's manifest service, sharing the CDN signing infrastructure but issuing multi-episode manifests rather than a single playback URL. Calls B-02's `UnlockEngine.get_unlock_states_bulk()` for filtering.

## 7. Existing Code to Reuse
- `modules/media/manifest_service.py::ManifestService` (extend with a download-specific method, do not fork a parallel service)
- `modules/content/unlock_engine.py::UnlockEngine.get_unlock_states_bulk()` (B-02)
- `modules/subscriptions/service.py::SubscriptionService.get_entitlement()`
- `common/base_service.py`

## 8. Files to Create
- `src/noorheroes/modules/media/download_models.py` — `DownloadManifestRecordOrm`
- `alembic/versions/xxxx_add_download_manifest_record.py`
- `src/noorheroes/modules/media/download_schemas.py` — `DownloadManifestRequest`, `DownloadManifestResponse`
- `src/noorheroes/modules/media/download_repository.py` — `DownloadManifestRepository`
- `src/noorheroes/modules/media/download_policy_models.py` — `DownloadPolicyOrm` (parent-configured `allow_new_downloads`, `offline_access_revoked` flags, FK `family_id`)
- `src/noorheroes/scripts/purge_expired_download_manifests.py` — scheduled purge job
- `tests/modules/media/test_download_manifest_service.py`
- `tests/modules/media/test_download_manifest_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/media/api.py::MediaRouter` — add `POST /v1/downloads/manifest`

## 10. Backend Requirements
- `ManifestService.build_download_manifest(child_id, content_id, quality)`: fetches all episodes for the series, calls `get_unlock_states_bulk()`, filters to `unlocked=true` only, issues per-episode signed media URLs (reusing B-07's signing path) with an appropriate longer-lived expiry suited to download completion windows (not the 15-min playback TTL — download URLs need enough time to actually transfer; document the chosen value and rationale).
- Checks `DownloadPolicyOrm.allow_new_downloads` for the family — if false, return `403 DOWNLOADS_DISABLED_BY_PARENT` before any manifest work.
- `offline_access_revoked` is a separate flag checked by the client/download-manager layer (K-07) to halt/remove already-downloaded content — this API's concern is only gating *new* manifest generation.
- Persist `download_manifest_record` (manifest_id, child_id, content_id, included_episode_ids, expires_at) for audit/health-monitoring (feeds B-15).

## 11. API Contract

### `POST /v1/downloads/manifest`
- Auth: Bearer (child-mode). Request: `{ "content_id": "series_...", "quality": "standard" }`. Response 200: `{ "manifest_id": "...", "episodes": [ { "episode_id": "ep_001", "media_urls": {...}, "expires_at": "..." } ] }`. Validation: only currently-unlocked episodes included; parent download-policy checked. Errors: `403 DOWNLOADS_DISABLED_BY_PARENT`.

## 12. Database Requirements
- `download_manifest_record`: FK `child_id`, `content_id`; index `(child_id, expires_at)`; purged after `expires_at` + 7 days grace (scheduled job).
- `download_policy` (new, parent-scoped): FK `family_id`; `allow_new_downloads` (default true), `offline_access_revoked` (default false).

## 13. Validation
- `content_id` must reference an existing, non-withdrawn series.
- `quality` restricted to defined enum values matching what the CDN/media pipeline actually supports.

## 14. Authentication
Bearer child-mode session via `get_current_child`.

## 15. Authorization
Family-level `download_policy` check is the authorization gate; no separate RBAC beyond that.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| Parent disabled new downloads | `403 DOWNLOADS_DISABLED_BY_PARENT` |
| Manifest generation fails mid-build (partial CDN signing failure) | Clear retry option surfaced to client; partial downloads resumable, not restarted from zero (client-side resumability per K-07, this API supports it by keeping `manifest_id` stable across retries for the same request) |
| Series has zero currently-unlocked episodes | `200` with empty `episodes` array — client shows an appropriate state, not an error |
| Database failure | `503`, logged with correlation ID |

## 17. Security
- Same signed-URL discipline as B-07 (no permanently public media URLs); download-scoped URLs use a longer TTL appropriate to transfer time but are still time-limited, never indefinite.
- `download_policy` is parent-controlled and can only be modified via the existing parent-authenticated settings surface (out of scope here — this API only reads it).

## 18. Analytics
Emit via `OutboxWriter`: `story_download_started` (on manifest issuance — actual completion/failure events are emitted client-side per K-07, correlated by `manifest_id`).

## 19. Performance
- Manifest build uses `get_unlock_states_bulk()` (single query) rather than per-episode unlock checks — mirrors B-01's N+1-avoidance requirement.
- Manifest generation is bursty (clusters around new-content-release moments and weekends per PRD DevOps §10) — must not hold long-lived DB locks during the CDN-signing loop.

## 20. Library Requirements
No new libraries — reuses existing CDN signing infrastructure and a standard scheduled-job mechanism already used elsewhere in `scripts/`.

## 21. Testing
- Unit: unlock-filtering correctness (5-episode series, 2 unlocked → exactly 2 in manifest — the PRD's explicit acceptance test), download-policy gating.
- Integration: manifest regenerated after completing an episode online includes the newly-unlocked next episode; purge job correctness against `expires_at` + 7-day-grace fixture data.

## 22. Documentation
Update OpenAPI schema; document the download-URL TTL rationale (distinct from B-07's 15-minute playback TTL) and the purge job's schedule.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Create `DownloadManifestRecordOrm` and `DownloadPolicyOrm` Models & Migration**
Objective: Add the manifest-audit and parent-policy tables. Follow: existing SQLAlchemy/Alembic conventions. Business Rules: `download_policy` defaults to `allow_new_downloads=true, offline_access_revoked=false`. Do Not Change: existing family/subscription tables. Tests: migration smoke test. Definition of Done: clean migration.

**Task 02 — Implement `DownloadManifestRepository`**
Objective: Data access for manifest records and policy reads. Follow: `BaseRepository`. Tests: policy read, manifest-record insert. Definition of Done: repository methods covered.

**Task 03 — Implement `build_download_manifest()` with Unlock Filtering**
Objective: Bulk-unlock-filtered, policy-gated manifest assembly reusing B-07's signing path. Dependencies: B-02's `get_unlock_states_bulk()`, B-07's signing infrastructure. Business Rules: only unlocked episodes included — explicit test against the PRD's 5-episode/2-unlocked scenario. Tests: unlock-filtering test, policy-gating test. Definition of Done: PRD acceptance scenario test passes exactly.

**Task 04 — Add Router Endpoint**
Objective: Wire `POST /v1/downloads/manifest` into `MediaRouter`. Tests: covered by Task 06. Definition of Done: endpoint live, documented.

**Task 05 — Implement Scheduled Purge Job**
Objective: `purge_expired_download_manifests.py` removing rows past `expires_at` + 7-day grace. Follow: existing `scripts/` conventions. Tests: purge boundary correctness (exactly at grace-period edge). Definition of Done: test passes, job registered in the scheduler.

**Task 06 — Add Unit & Integration Tests**
Objective: Full coverage per §21. Definition of Done: all green in CI.

**Task 07 — Update OpenAPI Documentation**
Objective: Regenerate/diff-classify; document TTL rationale and purge schedule. Definition of Done: non-breaking diff confirmed.

**Task 08 — Final Code Review**
Objective: Confirm the unlock-filtering test matches the PRD's exact acceptance criteria wording, confirm `download_policy` checks precede any CDN work. Definition of Done: checklist in §24 fully checked.

## 24. Final Verification Checklist
- [ ] Manifest for a 5-episode series with 2 unlocked returns exactly 2 episode entries (exact PRD acceptance test)
- [ ] `403 DOWNLOADS_DISABLED_BY_PARENT` returned before any CDN signing work when policy disallows
- [ ] `offline_access_revoked` is a separate flag from `allow_new_downloads`, not conflated
- [ ] Manifest regeneration after an unlock picks up the newly-unlocked episode
- [ ] `download_manifest_record` purged after `expires_at` + 7 days via scheduled job
- [ ] Download-URL TTL documented and distinct from B-07's 15-minute playback TTL
- [ ] No PostgreSQL/Redis credentials modified

## 25. Definition of Done
Offline download manifests are strictly unlock-aware, parent-policy-gated, auditable, and self-purging — giving K-07's `DownloadRepository` integration exactly the entitled, currently-unlocked episode set and nothing more.
