# B-14 — Admin Withdrawn Content Management API

## 1. Feature Context
Lets Content Editors/Trust & Safety pull content from circulation without ever deleting it — preserving every child's progress/completion/favorite history against the withdrawn episode while making it immediately unavailable and cache-invalidated.

## 2. Parent Feature
Feature A.3 — Stories Module (Animated Storytelling System)

## 3. Sub-feature
1.14 Admin Withdrawn Content Management API (ID: **B-14**)

## 4. Objective
Implement `PATCH /admin/v1/content/{id}` inside the existing `content` + `admin` modules to set `story_episode.is_withdrawn=true` with a required reason, trigger immediate cache/CDN invalidation, and support a future "Restore" action — gated by `content_editor`/`trust_safety` RBAC.

## 5. Business Requirements
- §8 Admin Requirements: Withdrawn Content Manager marks `is_withdrawn=true` (never hard-delete), required reason field, immediate cache/CDN invalidation trigger.
- §9 Admin AI Code-Generation Prompt: `PATCH /admin/v1/content/{id}` with `{ is_withdrawn: true, reason }`; withdrawn items show a status pill and remain visible for future "Restore".
- §4.4 Soft Delete Rules / Edge Case 10: withdrawn content becomes unavailable/non-discoverable while referencing history (progress, completions, favorites) remains intact.

## 6. Existing Architecture
Extends the existing `content` module's write path (alongside B-11) and the `admin` module's audit pattern. Triggers the same cache-invalidation mechanism B-01 already wires for catalog-publish events.

## 7. Existing Code to Reuse
- `modules/content/story_repository.py::StoryEpisodeRepository` (B-01/B-11, add `set_withdrawn()`)
- `modules/admin/service.py::AdminService.log_action()`
- `infrastructure/redis.py::get_redis_pool` (cache invalidation, same mechanism as B-01's publish-event invalidation)
- `core/deps.py::require_admin_scope()`

## 8. Files to Create
- `src/noorheroes/modules/content/withdrawal_schemas.py` — `WithdrawContentRequest`, `RestoreContentRequest`
- `src/noorheroes/modules/content/withdrawal_service.py` — `WithdrawalService(BaseService)`
- `tests/modules/content/test_withdrawal_service.py`
- `tests/modules/content/test_withdrawal_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/content/api.py::ContentRouter` — add `PATCH /admin/v1/content/{id}`, `POST /admin/v1/content/{id}/restore`
- `src/noorheroes/modules/content/story_repository.py::StoryEpisodeRepository` — add `set_withdrawn()`, `restore()`

## 10. Backend Requirements
- `WithdrawalService.withdraw(episode_id, admin_id, reason)`: requires non-empty `reason`; sets `is_withdrawn=true`; immediately invalidates the B-01 catalog cache entries touching this episode's series (targeted invalidation, not a full cache flush); writes audit log.
- `WithdrawalService.restore(episode_id, admin_id)`: sets `is_withdrawn=false`; same cache-invalidation trigger; audit log written.
- Withdrawal never touches `episode_progress`, `story_completion`, or `favorite` rows — those remain exactly as-is, satisfying the history-preservation requirement.
- Mid-playback withdrawal: this endpoint's effect (B-07 returning `410`/safe-stop on next manifest/heartbeat check) is handled entirely by B-07's existing withdrawn-precedence logic — this sub-feature only needs to flip the flag and invalidate caches correctly for that downstream behavior to activate.

## 11. API Contract

### `PATCH /admin/v1/content/{id}`
- Auth: Admin Bearer + `content_editor` or `trust_safety` scope. Request: `{ "is_withdrawn": true, "reason": "..." }`. Response 200: updated content record with `status: withdrawn`. Errors: `422 REASON_REQUIRED`, `404 CONTENT_NOT_FOUND`.

### `POST /admin/v1/content/{id}/restore`
- Auth: Admin Bearer + `content_editor` or `trust_safety` scope. Response 200: updated content record with `status: published` (or prior status). Errors: `404 CONTENT_NOT_FOUND`.

## 12. Database Requirements
- Writes to `story_episode.is_withdrawn` (owned by B-01's migration) — no new tables.

## 13. Validation
- `reason` required, non-empty, on withdrawal (not required on restore).

## 14. Authentication
Admin Bearer via `get_current_admin`.

## 15. Authorization
`require_admin_scope("content_editor")` OR `require_admin_scope("trust_safety")`.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| Missing/empty reason on withdrawal | `422 REASON_REQUIRED` |
| Unknown content ID | `404 CONTENT_NOT_FOUND` |
| Unauthorized/forbidden role | `401`/`403` |
| Cache invalidation fails after successful DB write | Withdrawal still succeeds (DB is source of truth); log a warning for ops to manually flush if needed — never roll back a successful withdrawal due to a cache-layer hiccup |
| Database failure | `503`, logged |

## 17. Security
- `content_editor`/`trust_safety` RBAC enforced at the API layer, matching N-05's frontend gating.
- Full audit trail (admin_id, reason, before/after status, timestamp) on every withdrawal/restore.
- No hard-delete capability exists — architecturally impossible to remove history through this path.

## 18. Analytics
Internal admin action — audited via `AdminAuditLog`, not the child-facing analytics taxonomy.

## 19. Performance
Low-volume admin operation; cache invalidation should be targeted (specific keys for the affected series/episode) rather than a full-cache flush, to avoid unnecessary cold-cache load on unrelated catalog traffic.

## 20. Library Requirements
No new libraries.

## 21. Testing
- Unit: reason-required validation, targeted cache-invalidation key correctness.
- Integration: withdraw → confirm `GET /v1/content/{id}` (B-01) returns `410` immediately post-withdrawal (cache correctly bypassed/invalidated); confirm `episode_progress`/`story_completion`/`favorite` rows for that episode are untouched; restore → confirm content reappears in catalog listings.

## 22. Documentation
Update OpenAPI schema.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Extend `StoryEpisodeRepository` with `set_withdrawn()`/`restore()`**
Objective: Flag-flip methods, no schema change needed (column already exists from B-01). Follow: `BaseRepository`. Tests: flag flips correctly both directions. Definition of Done: repository methods covered.

**Task 02 — Implement `WithdrawalService`**
Objective: Reason-validated withdrawal/restore with targeted cache invalidation and audit logging. Dependencies: Task 01, `AdminService.log_action()`, B-01's cache-invalidation mechanism. Business Rules: history tables (`episode_progress`, `story_completion`, `favorite`) never touched. Tests: history-preservation assertion, targeted-invalidation assertion. Definition of Done: tests pass.

**Task 03 — Add Router Endpoints**
Objective: Wire `PATCH /admin/v1/content/{id}` and `POST /admin/v1/content/{id}/restore` with `content_editor`/`trust_safety` scope. Tests: covered by Task 05. Definition of Done: endpoints live, documented.

**Task 04 — Wire End-to-End Cache-Invalidation Confirmation**
Objective: Integration test confirming B-01's `GET /v1/content/{id}` returns `410` immediately after withdrawal (no stale cache serving the old state). Dependencies: B-01. Definition of Done: test passes.

**Task 05 — Add Unit & Integration Tests**
Objective: Full coverage per §21. Definition of Done: all green in CI.

**Task 06 — Update OpenAPI Documentation**
Objective: Regenerate/diff-classify. Definition of Done: non-breaking diff confirmed.

**Task 07 — Final Code Review**
Objective: Confirm history tables are provably untouched by withdrawal, confirm cache invalidation is immediate and targeted. Definition of Done: checklist in §24 fully checked.

## 24. Final Verification Checklist
- [ ] Withdrawal requires a non-empty reason
- [ ] `is_withdrawn=true` triggers immediate, targeted cache/CDN invalidation (confirmed via B-01 returning `410` right after)
- [ ] `episode_progress`, `story_completion`, `favorite` rows referencing the withdrawn episode remain fully intact
- [ ] Restore correctly reverses withdrawal and reinstates catalog visibility
- [ ] `content_editor`/`trust_safety` RBAC enforced at the API layer
- [ ] Every withdrawal/restore writes an immutable audit log row
- [ ] No hard-delete code path exists anywhere in this API
- [ ] No PostgreSQL/Redis credentials modified

## 25. Definition of Done
Content can be pulled from circulation and restored through a reason-required, audited, cache-correct, history-preserving workflow — satisfying Edge Case 10 and giving B-07's withdrawn-precedence logic an immediately-consistent flag to act on.
