# B-03 — Playback Progress & Heartbeat Tracking API

## 1. Feature Context
Records ongoing playback position during a story session so the Unlock Engine (B-02) can evaluate threshold progress in near-real-time and so "Continue Watching" can resume correctly. Must resist scrub-to-end gaming on `scrub_restricted` series while never blocking playback on a network round-trip.

## 2. Parent Feature
Feature A.3 — Stories Module (Animated Storytelling System)

## 3. Sub-feature
1.3 Playback Progress & Heartbeat Tracking API (ID: **B-03**)

## 4. Objective
Implement `POST /v1/playback/{content_id}` inside the existing `learning`/`content` modules to persist throttled heartbeat events, enforce monotonic-position validation with anomaly flagging, and trigger B-02's Unlock Engine on qualifying updates.

## 5. Business Requirements
- FR-8: every interaction tracked via `POST /v1/playback/{id}` events.
- Edge Case 1: offline heartbeat/completion reconciliation — server authoritative on conflict.
- Edge Case 12: out-of-order retried events resolved via `client_event_id` + timestamp ordering, never regressing furthest-valid state.
- Error Handling table: position must be monotonically non-decreasing unless `event_type=seek`; anomalous heartbeats logged for fraud review, never silently trusted as completion signal.

## 6. Existing Architecture
Extends the existing `learning` context pattern (`QuizAttemptRepository`/`LearningService`) alongside `content`'s `EpisodeProgressRepository` from B-02. Router → Service → Repository → Postgres; no new bounded context.

## 7. Existing Code to Reuse
- `modules/content/unlock_repository.py::EpisodeProgressRepository` (B-02)
- `modules/content/unlock_engine.py::UnlockEngine` (B-02)
- `common/base_service.py`, `core/exceptions.py`
- `core/deps.py::get_current_child`

## 8. Files to Create
- `src/noorheroes/modules/content/playback_schemas.py` — `HeartbeatRequest`, `HeartbeatResponse`
- `src/noorheroes/modules/content/playback_service.py` — `PlaybackService(BaseService)`
- `tests/modules/content/test_playback_service.py`
- `tests/modules/content/test_playback_api.py`

## 9. Files to Modify
- `src/noorheroes/modules/content/api.py::ContentRouter` — add `POST /v1/playback/{content_id}`

## 10. Backend Requirements
- `PlaybackService.record_heartbeat(child_id, episode_id, position_seconds, client_event_id, event_type)`: reject (not crash) position regressions unless `event_type="seek"`; write anomalous regressions to a fraud/abuse review log table instead of updating `episode_progress`.
- On each accepted heartbeat, upsert `episode_progress.furthest_position_seconds` and conditionally call `UnlockEngine.evaluate()`/`persist_unlock()` when the configured `playback_percentage` threshold is crossed.
- Idempotent on `client_event_id` per session — replayed heartbeats are acknowledged without double-processing.
- Out-of-order protection: a retried/late heartbeat with an older timestamp than the currently stored furthest position must never regress state.

## 11. API Contract

### `POST /v1/playback/{content_id}`
- Auth: Bearer (child-mode). Request: `{ "event_type": "heartbeat"|"seek", "position_seconds": 142, "client_event_id": "uuid..." }`. Response 200: `{ "acknowledged": true }`. Validation: position monotonically non-decreasing per session unless `event_type="seek"`. Errors: `400 INVALID_PAYLOAD`, `401 UNAUTHORIZED`, `404 EPISODE_NOT_FOUND`.

## 12. Database Requirements
- Reuses `episode_progress` (B-02) — no new table for accepted heartbeats.
- New lightweight `playback_anomaly_log` table (child_id, episode_id, reported_position, expected_max_position, client_event_id, created_at) for the fraud/abuse review queue.

## 13. Validation
- `position_seconds` non-negative integer; `client_event_id` valid UUID; `event_type` restricted to `heartbeat`/`seek`.

## 14. Authentication
Bearer child-mode session via `get_current_child`.

## 15. Authorization
Episode must belong to a series the requesting child has entitlement to view (checked, not silently trusted).

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| Position regression without `event_type=seek` | Rejected — logged to `playback_anomaly_log`, `episode_progress` unchanged, response still `200 acknowledged:true` (never block/crash the client) |
| Retried/duplicate `client_event_id` | Idempotent no-op, original result semantics preserved |
| Out-of-order late heartbeat | Ignored if older than current furthest position |
| Unknown episode | `404 EPISODE_NOT_FOUND` |
| Database failure | `503`, logged with correlation ID |

## 17. Security
- Heartbeats never directly determine completion/reward (that is B-04's job) — this endpoint only updates progress and conditionally triggers unlock evaluation, limiting blast radius of any client tampering.
- Anomaly log entries reviewed by a fraud/abuse process (out of scope here) rather than auto-blocking the child in real time.

## 18. Analytics
Emit via `OutboxWriter`: `story_playback_heartbeat` (sampled/aggregated downstream given high volume, per PRD §11.1).

## 19. Performance
- Heartbeat writes are the highest-volume endpoint in the module — must be a single upsert, no read-then-write round trip where avoidable.
- No synchronous call chain beyond `episode_progress` upsert + conditional Unlock Engine evaluation.

## 20. Library Requirements
No new libraries.

## 21. Testing
- Unit: monotonicity enforcement, seek override, anomaly logging, idempotency on replay.
- Integration: high-frequency heartbeat burst test (throttling/upsert correctness under load), out-of-order event resolution against a multi-event fixture.

## 22. Documentation
Update OpenAPI schema; document the anomaly-log table's purpose for the future fraud-review consumer.

## 23. AI Coding Agent Implementation Steps

**Task 01 — Create `playback_anomaly_log` Model & Migration**
Objective: Persist rejected/anomalous heartbeats for review. Follow: existing SQLAlchemy/Alembic conventions. Do Not Change: `episode_progress` schema (owned by B-02). Tests: migration smoke test. Definition of Done: clean migration.

**Task 02 — Implement `PlaybackService.record_heartbeat()`**
Objective: Monotonicity + idempotency + anomaly logging. Dependencies: B-02's `EpisodeProgressRepository`, `UnlockEngine`. Business Rules: never regress `episode_progress` on an anomalous event; still return `200` to the client. Tests: all §21 unit cases. Definition of Done: tests pass.

**Task 03 — Add Router Endpoint**
Objective: Wire `POST /v1/playback/{content_id}` into `ContentRouter`. Tests: covered by Task 05. Definition of Done: endpoint live, documented.

**Task 04 — Wire Conditional Unlock Evaluation**
Objective: Call `UnlockEngine.evaluate()`/`persist_unlock()` only when the `playback_percentage` threshold is newly crossed on this heartbeat. Dependencies: Task 02, B-02. Tests: unlock triggered exactly once at threshold crossing, not on every subsequent heartbeat past it. Definition of Done: test passes.

**Task 05 — Add Unit & Integration Tests**
Objective: Full coverage per §21. Definition of Done: all green in CI.

**Task 06 — Update OpenAPI Documentation**
Objective: Regenerate/diff-classify. Definition of Done: non-breaking diff confirmed.

**Task 07 — Final Code Review**
Objective: Confirm this endpoint never itself grants rewards/completions (that remains B-04's exclusive responsibility). Definition of Done: checklist in §24 fully checked.

## 24. Final Verification Checklist
- [x] Position regression rejected (logged, not applied) unless `event_type=seek`
- [x] Idempotent on `client_event_id` replay
- [x] Out-of-order/late heartbeats never regress stored state
- [x] Unlock Engine triggered exactly once per genuine threshold crossing
- [x] High-frequency heartbeat burst does not degrade write performance
- [x] This endpoint never issues rewards or completion state directly
- [x] No PostgreSQL/Redis credentials modified

## 25. Definition of Done
Heartbeat tracking is live, resistant to naive scrub-to-end gaming, idempotent, and correctly feeds the Unlock Engine — providing the progress signal B-04's completion flow and B-01's "Continue Watching" resumption both depend on.
