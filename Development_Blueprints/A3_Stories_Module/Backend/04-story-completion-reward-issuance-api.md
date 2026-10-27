# B-04 — Story Completion & Reward Issuance API

## 1. Feature Context
The single highest-risk endpoint in the module: finalizes a story/episode as complete, awards XP/Noor Heroes Points/badges exactly once, advances the Unlock Engine, and synchronously (with a hard timeout) requests the moral summary. Any double-award or unlock-bypass here is a P0 incident per the PRD's rollback plan.

## 2. Parent Feature
Feature A.3 — Stories Module (Animated Storytelling System)

## 3. Sub-feature
1.4 Story Completion & Reward Issuance API (ID: **B-04**)

## 4. Objective
Implement `POST /v1/content/{id}/complete` as an idempotent, transactional orchestration across `content` (Unlock Engine), `rewards` (`RewardService`), and `ai_safety` (Moral Summary Service, B-06) — enforced by a database-level uniqueness constraint, not application logic alone.

## 5. Business Requirements
- FR-9: on completion, award reward → show moral summary → optionally show quiz → offer AI Next Learning.
- Acceptance Criteria: firing the same completion request 5 times concurrently results in exactly one reward grant (hard requirement, CI-gated per PRD DevOps §10).
- Edge Case 12: idempotency/event-ordering logic so a stale retried event never regresses the furthest-valid state.
- Error Handling: quiz-service unavailability must never block reward issuance.

## 6. Existing Architecture
Orchestrates existing `rewards` (`RewardService.award_points()`), `content` (`UnlockEngine` from B-02), and `ai_safety` (B-06's moral summary service) — all already-scaffolded bounded contexts. This sub-feature adds the orchestration endpoint/service inside `content`, calling into the other two via their existing service interfaces (in-process calls within the modular monolith, not new network hops).

## 7. Existing Code to Reuse
- `modules/rewards/service.py::RewardService.award_points()`
- `modules/content/unlock_engine.py::UnlockEngine` (B-02)
- `modules/ai_safety/*` moral summary service (B-06)
- `common/base_service.py`, `core/exceptions.py`
- `infrastructure/db/` transaction/session management

## 8. Files to Create
- `src/noorheroes/modules/content/completion_models.py` — `StoryCompletionOrm`
- `alembic/versions/xxxx_add_story_completion.py`
- `src/noorheroes/modules/content/completion_schemas.py` — `CompletionRequest`, `CompletionResponse`
- `src/noorheroes/modules/content/completion_repository.py` — `StoryCompletionRepository`
- `src/noorheroes/modules/content/completion_service.py` — `CompletionService(BaseService)`
- `tests/modules/content/test_completion_service.py`
- `tests/modules/content/test_completion_api.py`
- `tests/modules/content/test_completion_concurrency.py`

## 9. Files to Modify
- `src/noorheroes/modules/content/api.py::ContentRouter` — add `POST /v1/content/{id}/complete`

## 10. Backend Requirements
- `CompletionService.complete_episode(child_id, episode_id, completion_method, final_position_seconds, client_event_id)`: wrapped in a single DB transaction; `INSERT ... ON CONFLICT (content_id, child_id, client_event_id) DO NOTHING` (or equivalent) on `story_completion` as the idempotency gate — if the insert is a no-op (row already existed), return the original stored result rather than re-running the award chain.
- On successful first-time insert: call `RewardService.award_points()`, call `UnlockEngine.persist_unlock()` for the next episode if threshold met, call B-06's moral summary chain with a hard 600ms timeout (fallback per B-06's contract on timeout/failure — never let AI latency delay this response beyond budget).
- Quiz-service unavailability is independent of this endpoint's success — the response's `moral_summary` still returns; quiz is a separate client-driven step (B-?, shared with A.8) not blocked by this call.
- `is_preview` claim propagation: if the caller's token carries `is_preview=true` (from B-13), skip both the `RewardService.award_points()` call and the `UnlockEngine.persist_unlock()` call entirely — write the `story_completion` row flagged `is_preview=true` for audit purposes only.

## 11. API Contract

### `POST /v1/content/{id}/complete`
- Auth: Bearer (child-mode, or preview-token per B-13). Request: `{ "completion_method": "playback_threshold"|"final_interaction"|"quiz_completion", "final_position_seconds": 480, "client_event_id": "uuid..." }`. Response 200: `{ "completed": true, "reward": { "xp": 50, "noor_points": 20, "badge_id": null }, "next_episode_unlocked": "ep_004", "moral_summary": { "source": "ai"|"human_fallback", "text": "..." } }`. Idempotency: `client_event_id` enforced unique via DB constraint — replays return the original result. Errors: `400 INVALID_PAYLOAD`, `401 UNAUTHORIZED`, `404 EPISODE_NOT_FOUND`.

## 12. Database Requirements
- `story_completion`: FK `child_id`, `episode_id`; `UNIQUE(client_event_id)` for idempotency (per PRD §4.2); also enforce `UNIQUE(content_id, child_id, client_event_id)` per the backend AI-prompt's stated constraint shape; append-only/immutable — no updates after insert.
- Index `(child_id, completed_at DESC)`.

## 13. Validation
- `completion_method` restricted to the three defined enum values.
- `client_event_id` required, valid UUID — request rejected (`400`) if missing, never silently generated server-side.

## 14. Authentication
Bearer child-mode session, or a valid preview-session token per B-13 (mutually exclusive claim handling — never both).

## 15. Authorization
Episode must belong to a series the requesting child (or preview session's target content) is entitled to.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| Duplicate `client_event_id` (replay) | Return original stored result, zero side effects re-run |
| Concurrent duplicate requests (race) | DB unique constraint guarantees exactly one insert wins; losers read back the winner's result |
| AI moral summary timeout/failure | Immediate fallback to human-reviewed moral (B-06 contract) — response never delayed beyond 600ms budget |
| Quiz service unavailable | Irrelevant to this endpoint — response completes normally |
| `is_preview=true` | Reward and unlock steps explicitly skipped; completion row flagged and audited |
| Database transaction failure | `503`, full rollback, logged with correlation ID |

## 17. Security
- Idempotency enforced at the database constraint layer, not application logic alone (defense against replay/race exploitation).
- `is_preview` claim checked from the verified token, never from a client-supplied request body field.
- No reward/unlock side effects possible without passing through this single orchestration path.

## 18. Analytics
Emit via `OutboxWriter`: `story_completion_threshold_reached`, `story_completed`, `story_reward_awarded`, `story_badge_unlocked`, `moral_summary_shown` (with `source: ai|human_fallback`), `episode_unlocked`.

## 19. Performance
- Single DB transaction covering completion-insert + reward-award + unlock-persist; moral-summary call has its own bounded 600ms timeout and does not hold the DB transaction open while waiting (fetch/store the moral summary result after the core transaction commits, or use a short-lived nested scope — implementation detail for the coding agent to resolve consistent with existing transaction-management patterns).
- No blocking calls beyond the bounded AI timeout.

## 20. Library Requirements
No new libraries; relies on existing Postgres unique-constraint + SQLAlchemy transaction management.

## 21. Testing
- Unit: idempotent replay returns original result; `is_preview` skip logic; completion_method validation.
- Integration: **mandatory concurrency test** — fire the same completion request 5 times concurrently, assert exactly one `story_completion` row and one reward grant exist afterward (per PRD backend AI-prompt requirement #2).
- Integration: preview-session isolation test — confirm zero reward/unlock-state change for the real `child_id` when `is_preview=true`.
- Integration: AI-timeout chaos test — kill the moral-summary dependency mid-call, confirm response still returns within budget with fallback moral.

## 22. Documentation
Update OpenAPI schema; document the idempotency constraint and the `is_preview` skip contract prominently in the module README, since B-13 depends on this exact behavior.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Create `StoryCompletionOrm` Model & Migration**
Objective: Add the append-only `story_completion` table with the idempotency unique constraint. Why: no existing table enforces completion idempotency. Follow: existing SQLAlchemy/Alembic conventions. Business Rules: `UNIQUE(client_event_id)` and `UNIQUE(content_id, child_id, client_event_id)`; append-only (no update method exposed by the repository). Do Not Change: `episode_progress`/`episode_unlock_state` schemas (B-02). Tests: migration smoke test, constraint-violation-on-duplicate-insert test. Definition of Done: clean migration, constraint verified.

**Task 02 — Implement `StoryCompletionRepository`**
Objective: Insert-with-conflict-handling data access. Follow: `BaseRepository`. Implementation: `insert_if_absent()` returning `(row, was_created: bool)`. Tests: duplicate insert returns `was_created=False` with the original row. Definition of Done: test passes.

**Task 03 — Implement `CompletionService.complete_episode()` Core Orchestration**
Objective: Transactional idempotency gate + reward + unlock orchestration. Dependencies: Task 01–02, `RewardService` (existing), `UnlockEngine` (B-02). Business Rules: reward/unlock only run on genuine first-time insert. Tests: single-request happy path, replay no-op. Definition of Done: tests pass.

**Task 04 — Wire AI Moral Summary Call with Hard Timeout**
Objective: Call B-06's service with a 600ms budget, fallback on timeout/failure. Dependencies: B-06. Tests: AI-timeout chaos test (kill dependency, assert fallback used, assert response time within budget). Definition of Done: chaos test passes.

**Task 05 — Implement `is_preview` Claim Handling**
Objective: Skip reward/unlock when the verified token carries `is_preview=true`; still write an audited completion row. Dependencies: B-13's token issuance contract. Tests: preview-session isolation integration test (zero reward/unlock change for real child). Definition of Done: isolation test passes.

**Task 06 — Add Router Endpoint**
Objective: Wire `POST /v1/content/{id}/complete` into `ContentRouter`. Tests: covered by Task 08. Definition of Done: endpoint live, documented.

**Task 07 — Implement Mandatory Concurrency Test**
Objective: Fire 5 concurrent identical requests, assert exactly one reward granted (PRD backend AI-prompt requirement #2, CI gate per DevOps §10). Definition of Done: test passes reliably (no flakiness) and is registered as a required CI check.

**Task 08 — Add Remaining Unit & Integration Tests**
Objective: Full coverage per §21. Definition of Done: all green in CI.

**Task 09 — Update OpenAPI Documentation**
Objective: Regenerate/diff-classify; document idempotency and preview-skip contracts. Definition of Done: non-breaking diff confirmed.

**Task 10 — Final Code Review**
Objective: Confirm idempotency is DB-constraint-enforced (not just application-logic-enforced), confirm `is_preview` propagation is airtight, confirm AI timeout never exceeds budget. Definition of Done: checklist in §24 fully checked.

## 24. Final Verification Checklist
- [ ] 5 concurrent identical completion requests → exactly one `story_completion` row, one reward grant (CI-gated)
- [ ] Idempotency enforced via database unique constraint, not application logic alone
- [ ] `is_preview=true` → zero reward, zero unlock-state change, completion row still written and audited
- [ ] AI moral summary call never delays response beyond 600ms budget; fallback verified via chaos test
- [ ] Quiz-service unavailability never blocks reward issuance
- [ ] `next_episode_unlocked` correctly reflects Unlock Engine's decision
- [ ] All analytics events in §18 emitted via `OutboxWriter`
- [ ] No PostgreSQL/Redis credentials modified

## 25. Definition of Done
Story completion is transactionally safe, database-enforced idempotent, correctly orchestrates reward issuance and unlock advancement, correctly isolates admin preview sessions from real rewards, and never blocks on AI or quiz availability — satisfying the PRD's zero-tolerance P0 rollback triggers for reward-duplication and unlock-bypass.
