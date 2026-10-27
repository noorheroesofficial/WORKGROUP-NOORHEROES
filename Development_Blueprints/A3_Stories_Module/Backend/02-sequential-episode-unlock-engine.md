# B-02 — Sequential Episode Unlock Engine

## 1. Feature Context
The trust-critical core of the Stories Module: a server-authoritative engine that decides whether a given child may access a given episode's media. Episode 1 is unlocked by default; Episode N+1 unlocks only after Episode N reaches its configured completion threshold. This engine is consumed internally by B-01 (catalog annotation), B-03 (progress updates), B-04 (completion → next-unlock), B-07 (manifest re-validation), and B-08 (download manifest filtering) — it is never called directly by a client.

## 2. Parent Feature
Feature A.3 — Stories Module (Animated Storytelling System)

## 3. Sub-feature
1.2 Sequential Episode Unlock Engine (ID: **B-02**)

## 4. Objective
Implement the Unlock Engine as a pure, deterministic function of `episode_progress` + `unlock_threshold_config`, backed by a persisted, independently queryable `episode_unlock_state` table that is written on every relevant progress update (not lazily computed only at read time), inside the existing `content` module.

## 5. Business Requirements
- FR-4: Sequential unlock — Episode 1 unlocked by default; Episode N+1 unlocks only after Episode N reaches its per-series-configured completion threshold (playback %, final interaction, or quiz completion).
- FR-6: Rewatching a completed episode never re-locks it.
- Edge Case 1: offline completion at the threshold boundary → local unlock recorded immediately; server authoritative on reconnect sync, but a child is never abruptly re-locked once unlocked locally without explanation.
- Edge Case 2: unlock-threshold config changed after a child already unlocked Episode 3 under the old rule → previously unlocked episodes stay unlocked; only future episodes governed by the new threshold.
- Acceptance Criteria: manifest issuance (B-07) MUST re-validate unlock state at issuance time — never trust a client-supplied claim.

## 6. Existing Architecture
Lives inside the existing `content` module as an internal service class (`UnlockEngine`), not a new bounded context and not a new router (no public endpoints — internal only, called in-process by B-01/B-03/B-04/B-07/B-08). Follows the existing `BaseService`/`BaseRepository` layering and Postgres-as-source-of-truth pattern; no Redis caching of unlock state (correctness over latency for an access-control decision).

## 7. Existing Code to Reuse
- `modules/content/repository.py` pattern (extend with `EpisodeProgressRepository`, `EpisodeUnlockStateRepository`)
- `common/base_service.py`, `common/base_repository.py`
- `core/exceptions.py` (`ValidationError`)
- `common/outbox.py::OutboxWriter` (for `episode_unlocked` event)

## 8. Files to Create
- `src/noorheroes/modules/content/unlock_models.py` — `EpisodeProgressOrm`, `EpisodeUnlockStateOrm`
- `alembic/versions/xxxx_add_episode_progress_unlock_state.py`
- `src/noorheroes/modules/content/unlock_repository.py` — `EpisodeProgressRepository`, `EpisodeUnlockStateRepository`
- `src/noorheroes/modules/content/unlock_engine.py` — `UnlockEngine(BaseService)`
- `tests/modules/content/test_unlock_engine.py`

## 9. Files to Modify
- None outside this sub-feature's own new files; B-01/B-03/B-04/B-07/B-08 blueprints each add their own call sites into `UnlockEngine` (documented in their respective "Files to Modify" sections, not duplicated here).

## 10. Backend Requirements
- `UnlockEngine.evaluate(child_id, episode_id, progress) -> UnlockDecision`: pure function — given `episode_progress.furthest_position_seconds` (or interaction/quiz completion flags) and `story_episode.unlock_threshold_config`, deterministically compute whether the *next* episode in sequence should be unlocked.
- `UnlockEngine.persist_unlock(child_id, episode_id)`: writes/upserts `episode_unlock_state.unlocked=true, unlocked_at=now()` — called on every qualifying progress update, not only lazily at read time. Idempotent (upsert on `UNIQUE(child_id, episode_id)`).
- `UnlockEngine.get_unlock_state(child_id, episode_id)` / `get_unlock_states_bulk(child_id, episode_ids)`: read-only queries against `episode_unlock_state`, defaulting Episode 1 of any series to `unlocked=true` without a row (implicit default, materialized lazily on first read if absent).
- Config-change immutability: `evaluate()` never re-evaluates or revokes an already-persisted `unlocked=true` row; a threshold-config change only affects future `evaluate()` calls for episodes not yet unlocked.
- Fail-closed for never-seen episodes on internal error (treat as locked, surface a retryable error to the caller); fail-open (serve cached `episode_unlock_state` row) for already-unlocked episodes on the same error.

## 11. API Contract
No public HTTP endpoints. Internal service contract:
```
UnlockEngine.evaluate(child_id: UUID, episode_id: UUID, progress: EpisodeProgressOrm) -> UnlockDecision
UnlockEngine.persist_unlock(child_id: UUID, episode_id: UUID) -> None
UnlockEngine.get_unlock_state(child_id: UUID, episode_id: UUID) -> UnlockState
UnlockEngine.get_unlock_states_bulk(child_id: UUID, episode_ids: list[UUID]) -> dict[UUID, UnlockState]
```

## 12. Database Requirements
- `episode_progress`: FK `child_id`, `episode_id`; `UNIQUE(child_id, episode_id)`; index `(child_id, updated_at DESC)`.
- `episode_unlock_state`: FK `child_id`, `episode_id`; `UNIQUE(child_id, episode_id)`; index `(child_id, episode_id)`.
- Both tables retained indefinitely (core progress history feeding Parent Insights/B-10); never purged except on account deletion.

## 13. Validation
- `unlock_threshold_config` JSONB validated against one of exactly three shapes (`playback_percentage`, `final_interaction`, `quiz_completion`) at write time by B-11 (admin), read defensively here (unknown shape → fail-closed, log for investigation, never crash).

## 14. Authentication
N/A — internal service, no direct HTTP surface; authorization is enforced by the calling endpoint (B-01/B-03/B-04/B-07/B-08).

## 15. Authorization
N/A — see above. Callers are responsible for confirming `child_id` belongs to the requesting session before invoking the engine.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| Never-seen episode + engine error | Fail closed — treat as locked, return retryable error to caller |
| Already-unlocked episode + engine error | Fail open — serve cached `episode_unlock_state` row, log the underlying error |
| Threshold config changed after unlock | No retroactive re-lock; only future evaluations affected |
| Malformed `unlock_threshold_config` | Fail closed for that episode, log for admin/content-editor investigation |
| Concurrent progress updates for same child+episode | Upsert with row-level lock / `ON CONFLICT` semantics — no lost-update race |

## 17. Security
- No client input directly drives unlock decisions — `evaluate()` only ever consumes server-persisted `episode_progress`, never a client-asserted position/completion flag.
- `episode_unlock_state` is the single source of truth consulted by B-07 at manifest-issuance time; no other code path may grant media access.

## 18. Analytics
Emit via `OutboxWriter`: `episode_unlocked` (with `episode_number`) — fired exactly once per genuine unlock transition (idempotent persist must not re-fire the event on repeated upserts of an already-unlocked row).

## 19. Performance
- `get_unlock_states_bulk()` is a single indexed query across all requested episode IDs — never a per-episode loop query (required by B-01 Task 04).
- `persist_unlock()` upsert uses the `UNIQUE(child_id, episode_id)` constraint via `ON CONFLICT DO NOTHING`/`DO UPDATE` semantics rather than read-then-write.

## 20. Library Requirements
No new third-party libraries — SQLAlchemy 2.0 async, existing Postgres.

## 21. Testing
- Unit: threshold evaluation correctness for all three `unlock_threshold_config` modes; config-change-after-unlock immutability (the Edge Case 2 guarantee); implicit Episode-1-unlocked default; idempotent `persist_unlock()` (no duplicate `episode_unlocked` event on repeated calls).
- Integration: bulk-state read correctness against a seeded multi-episode, multi-child fixture; concurrent progress-update race test (two simultaneous heartbeats for the same child+episode do not corrupt unlock state).

## 22. Documentation
Internal module README section documenting the fail-open/fail-closed matrix and the "never revoke an already-unlocked episode" invariant, since every downstream blueprint (B-01, B-03, B-04, B-07, B-08) depends on this guarantee.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Create `EpisodeProgressOrm` and `EpisodeUnlockStateOrm` Models & Migration**
Objective: Add the two tables per the PRD ER diagram. Why: no existing schema tracks per-child-per-episode progress or unlock state. Follow: existing SQLAlchemy/Alembic conventions. Create: `unlock_models.py`, migration file. Business Rules: `UNIQUE(child_id, episode_id)` on both tables. Do Not Change: `story_episode` (B-01) beyond the FK relationship already defined there. Tests: migration up/down smoke test. Definition of Done: clean migration on fresh DB and staging dry-run.

**Task 02 — Implement `EpisodeProgressRepository` and `EpisodeUnlockStateRepository`**
Objective: Data access with upsert-safe writes. Follow: `BaseRepository`. Implementation: `upsert_progress()`, `get_progress()`, `upsert_unlock_state()`, `get_unlock_state()`, `get_unlock_states_bulk()`. Tests: upsert idempotency, bulk read correctness. Definition of Done: repository methods covered.

**Task 03 — Implement `UnlockEngine.evaluate()` as a Pure Function**
Objective: Deterministic threshold evaluation for all three `unlock_threshold_config` modes. Business Rules: never revoke an already-unlocked episode. Tests: unit tests per mode, plus the config-change-after-unlock immutability case (explicit fixture: unlock under old config, change config, re-evaluate, assert still unlocked). Dependencies: Task 01, 02. Definition of Done: all threshold-mode tests and the immutability test pass.

**Task 04 — Implement `persist_unlock()` and Implicit Episode-1 Default**
Objective: Idempotent write path + implicit unlock for the first episode of any series without requiring a materialized row. Business Rules: idempotent — repeated calls never re-fire `episode_unlocked`. Tests: repeated-call idempotency, Episode-1-default-without-row. Definition of Done: idempotency test passes.

**Task 05 — Implement Bulk Read (`get_unlock_states_bulk`)**
Objective: Single-query batch read for B-01's catalog annotation use case. Business Rules: no N+1 — one query regardless of episode count. Tests: assert query count via SQL echo/test harness for a 10-episode series. Definition of Done: single-query assertion passes.

**Task 06 — Wire `episode_unlocked` Analytics Event**
Objective: Emit via `OutboxWriter` on genuine transitions only. Dependencies: Task 04. Tests: event fires exactly once per real unlock, not on idempotent re-persists. Definition of Done: event-count assertion passes.

**Task 07 — Add Unit & Integration Tests**
Objective: Full coverage per §21, including the concurrent-update race test. Files: `test_unlock_engine.py`. Definition of Done: all cases green in CI.

**Task 08 — Final Code Review**
Objective: Confirm no client-supplied data ever drives `evaluate()`, confirm fail-open/fail-closed matrix matches §16 exactly, confirm this engine has zero public HTTP surface. Definition of Done: checklist in §24 fully checked.

## 24. Final Verification Checklist
- [ ] Episode 1 unlocked by default for every series without requiring a materialized row
- [ ] Episode N+1 unlock strictly gated on Episode N's configured threshold (all three modes tested)
- [ ] Config change after unlock never retroactively re-locks an already-unlocked episode (explicit test)
- [ ] `persist_unlock()` idempotent; `episode_unlocked` event fires exactly once per genuine transition
- [ ] `get_unlock_states_bulk()` executes as a single query regardless of episode count
- [ ] Fail-closed for never-seen episodes, fail-open for already-unlocked episodes, on internal error
- [ ] No public HTTP endpoint exists for this engine — internal service only
- [ ] Concurrent progress-update race test passes with no lost updates
- [ ] No PostgreSQL/Redis credentials modified

## 25. Definition of Done
The Unlock Engine deterministically and durably tracks per-child episode unlock state, is safely consumable in bulk, and provides the single source of truth every other Stories backend sub-feature (B-01, B-03, B-04, B-07, B-08) relies on for access-control decisions.
