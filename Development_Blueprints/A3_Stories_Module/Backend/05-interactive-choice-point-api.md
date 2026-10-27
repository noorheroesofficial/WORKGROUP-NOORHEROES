# B-05 — Interactive Choice Point API

## 1. Feature Context
Records which values-based choice a child selected at a scripted in-story branch point. The endpoint is explicitly non-blocking for playback — the client always mirrors branch logic deterministically offline; this API exists for analytics/sync/editorial-signal purposes, not real-time gating.

## 2. Parent Feature
Feature A.3 — Stories Module (Animated Storytelling System)

## 3. Sub-feature
1.5 Interactive Choice Point API (ID: **B-05**)

## 4. Objective
Implement `POST /v1/content/{id}/choice` inside the existing `content` module to durably record choice events with debounce-safe handling and offline-sync tolerance, without ever becoming a playback-blocking dependency.

## 5. Business Requirements
- FR-7: Story Player supports in-story interactive choice overlays.
- Edge Case 3: rapid repeated taps on a choice moment must be debounced/queued so no choice is silently dropped or double-counted.
- §3.4 API note: client-side deterministic branch logic mirrors this server call so playback is never blocked waiting on it.
- §11.3 Dashboard Metrics: choice-point selection distribution is a valuable editorial signal — data integrity matters even though the call is non-blocking.

## 6. Existing Architecture
Extends the existing `content` module. Router → Service → Repository → Postgres, no new bounded context.

## 7. Existing Code to Reuse
- `common/base_service.py`, `common/base_repository.py`
- `core/deps.py::get_current_child`
- `core/exceptions.py`

## 8. Files to Create
- `src/noorheroes/modules/content/choice_models.py` — `ChoicePointOrm`, `ChoiceEventOrm`
- `alembic/versions/xxxx_add_choice_point_choice_event.py`
- `src/noorheroes/modules/content/choice_schemas.py` — `ChoiceRequest`, `ChoiceResponse`
- `src/noorheroes/modules/content/choice_repository.py` — `ChoiceEventRepository`
- `src/noorheroes/modules/content/choice_service.py` — `ChoiceService(BaseService)`
- `tests/modules/content/test_choice_service.py`
- `tests/modules/content/test_choice_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/content/api.py::ContentRouter` — add `POST /v1/content/{id}/choice`

## 10. Backend Requirements
- `ChoiceService.record_choice(child_id, choice_point_id, selected_option_id, client_event_id)`: idempotent on `client_event_id`; validates `selected_option_id` exists among the choice point's configured `options` (max 3, enforced at write time by B-11 — this service defensively validates against whatever is stored, never assumes exactly 3).
- Returns `branch_content_ref` for the given `choice_point_id`/`selected_option_id` pair so the client can confirm/reconcile against its own deterministic mirror (informational, not authoritative for playback continuation).
- Debounce tolerance: duplicate `client_event_id` within the same choice point is a no-op returning the original result; this is the server-side complement to the client's own input debouncing (Edge Case 3).

## 11. API Contract

### `POST /v1/content/{id}/choice`
- Auth: Bearer (child-mode). Request: `{ "choice_point_id": "cp_2", "selected_option_id": "opt_b", "client_event_id": "uuid..." }`. Response 200: `{ "branch_content_ref": "branch_b_segment" }`. Errors: `400 INVALID_OPTION`, `404 CHOICE_POINT_NOT_FOUND`, `401 UNAUTHORIZED`.

## 12. Database Requirements
- `choice_point`: FK `episode_id`; `options` JSONB (owned/written by B-11, read-only here).
- `choice_event`: FK `choice_point_id`, `child_id`; index `(child_id, choice_point_id)`.

## 13. Validation
- `selected_option_id` must exist within the referenced `choice_point.options`.
- `client_event_id` required, valid UUID.

## 14. Authentication
Bearer child-mode session via `get_current_child`.

## 15. Authorization
Choice point's parent episode must belong to a series the child is entitled to (defense in depth — not the primary access-control layer, which is B-07's manifest).

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| Unknown `choice_point_id` | `404 CHOICE_POINT_NOT_FOUND` |
| `selected_option_id` not among configured options | `400 INVALID_OPTION` |
| Duplicate `client_event_id` | No-op, original result returned |
| Network failure client-side | Non-issue for this endpoint by design — client already branched locally; event queues for later sync |
| Database failure | `503`, logged, does not block client playback since call is fire-and-forget from the player's perspective |

## 17. Security
- No reward, unlock, or access-control side effects flow from this endpoint — isolates blast radius of any client tampering with choice data to analytics/editorial signal only.

## 18. Analytics
Emit via `OutboxWriter`: `story_choice_made` (with `choice_id`, `branch_taken`).

## 19. Performance
- Single-row insert, no downstream orchestration — must remain lightweight since it is called at every scripted choice moment across all active sessions.

## 20. Library Requirements
No new libraries.

## 21. Testing
- Unit: option validation, idempotent replay, unknown choice-point handling.
- Integration: offline-queued choice events synced in bulk on reconnect (batch endpoint behavior or repeated single calls — verify no data loss and no duplication).

## 22. Documentation
Update OpenAPI schema; note explicitly in the module README that this endpoint is non-blocking/informational relative to client-side branch logic.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Create `ChoicePointOrm` and `ChoiceEventOrm` Models & Migration**
Objective: Add the two tables per the PRD ER diagram. Follow: existing SQLAlchemy/Alembic conventions. Do Not Change: `story_episode` beyond the new FK relationship. Tests: migration smoke test. Definition of Done: clean migration.

**Task 02 — Implement `ChoiceEventRepository`**
Objective: Idempotent insert data access. Follow: `BaseRepository`. Implementation: `insert_if_absent()`. Tests: duplicate insert no-op. Definition of Done: test passes.

**Task 03 — Implement `ChoiceService.record_choice()`**
Objective: Validate option membership, idempotent recording, return `branch_content_ref`. Dependencies: Task 01–02. Tests: invalid-option rejection, idempotent replay, unknown-choice-point 404. Definition of Done: tests pass.

**Task 04 — Add Router Endpoint**
Objective: Wire `POST /v1/content/{id}/choice` into `ContentRouter`. Tests: covered by Task 05. Definition of Done: endpoint live, documented.

**Task 05 — Add Unit & Integration Tests**
Objective: Full coverage per §21. Definition of Done: all green in CI.

**Task 06 — Update OpenAPI Documentation**
Objective: Regenerate/diff-classify; document non-blocking nature explicitly. Definition of Done: non-breaking diff confirmed.

**Task 07 — Final Code Review**
Objective: Confirm this endpoint has zero reward/unlock side effects and never becomes a playback-blocking dependency in downstream code. Definition of Done: checklist in §24 fully checked.

## 24. Final Verification Checklist
- [ ] `selected_option_id` validated against the choice point's actual configured options
- [ ] Idempotent on `client_event_id` replay
- [ ] Unknown choice point returns `404`, not a silent failure
- [ ] Endpoint has zero reward/unlock side effects
- [ ] Offline-queued choice events sync without loss or duplication
- [ ] `story_choice_made` analytics event includes `choice_id` and `branch_taken`
- [ ] No PostgreSQL/Redis credentials modified

## 25. Definition of Done
Choice-point selections are durably recorded, idempotent, and available as an editorial/analytics signal without ever becoming a dependency the Story Player must wait on.
