# B-02 — Unlock Evaluation Engine

## 1. Feature Context
NoorHeroes Backend (FastAPI). Part of Feature A.12 — Avatar System. Internal event-driven service (no direct client endpoint) that subscribes to badge/level/habit-milestone events from A.7/A.9/A.11 and evaluates `avatar_items.unlock_rule` criteria to drive criteria-based auto-unlocking, distinct from A.11's Noor-Heroes-Points purchase acquisition path.

## 2. Parent Feature
A.12 Avatar System — Backend (FastAPI)

## 3. Sub-feature
B-02 Unlock Evaluation Engine

## 4. Objective
Implement a Kafka consumer that subscribes to `badge_unlocked`, `achievement_level_progressed`, and `habit_streak_state_changed` events, evaluates all non-retired `avatar_items` whose `unlock_rule` matches, and idempotently grants `child_inventory` ownership plus a notification trigger — backing FR-8, FR-9, and the PRD's Backend AI Code-Generation Prompt item 4 (treated as highest priority alongside B-01's items 1–2).

## 5. Business Requirements
- When a child's activity causes a locked item's criteria to become met, the item is auto-unlocked and a notification is sent — the child never manually "claims" an avatar-item unlock (FR-8).
- Character Evolution progression (FR-9) — Quran skills, story morals, kindness actions, and habit consistency — feeds this same evaluation path via the shared event topics.
- Event processing must be idempotent: the same event processed twice (simulating Kafka at-least-once redelivery) must result in exactly one `child_inventory` row and exactly one notification trigger, never two (PRD Backend AI Code-Generation Prompt item 4).
- A broken habit streak never retroactively re-locks a previously-unlocked item — this engine only grants, it never revokes (Edge Case 6, consistent with the platform's "unlocks are sticky" principle).
- Auto-unlock notification delivery failure must never affect the underlying grant — the `child_inventory` row is unaffected; the child simply discovers the item next time they open the Avatar screen (§1.11 Error Handling table).

## 6. Existing Architecture
Extends the `avatars` bounded context established in B-01 (`src/noorheroes/modules/avatars/`). This engine is a standing Kafka consumer process, not an HTTP-triggered service — it follows the same consumer-framework convention referenced by the A.6 Dua Learning blueprint's `dua_marked_learned_consumer.py` (existing consumer base class/framework), but is implemented under the `avatars` module rather than a generic `app/consumers/` path, consistent with this project's `src/noorheroes/modules/*` bounded-context convention (per `FAST-API-INSTRUCTIONS.md` §1). The event topics themselves (`badge_unlocked`, `achievement_level_progressed`) are owned/produced by the not-yet-blueprinted A.11 Rewards System and by A.9's Skill Tree Mastery Engine (`habit_streak_state_changed` is produced by A.7's `HabitStreakStateMachine`, per the A.7 B-03 blueprint) — this sub-feature is a **consumer only** and must not redefine or duplicate those topics' producers.

## 7. Existing Code to Reuse
- `AvatarRepository`/`ChildInventory` model (B-01)
- `UnlockRuleResolver`'s rule-parsing logic (B-01) — reused here for rule-to-event matching, not just display-description resolution
- Existing Kafka consumer base class/framework (project-wide convention referenced by A.6 B-05)
- `OutboxWriter`/notification-trigger pattern used by `notifications` context (`NotificationService.dispatch_notification()`, per `FAST-API-INSTRUCTIONS.md` §5.8)
- `retry_with_backoff` (`common/utils/retry.py`)

## 8. Files to Create
- `src/noorheroes/modules/avatars/consumers.py` (`UnlockEvaluationConsumer`)
- `src/noorheroes/modules/avatars/unlock_matcher.py` (`UnlockRuleMatcher.find_matching_items(event)`)
- `tests/modules/avatars/test_unlock_evaluation_engine.py`
- `tests/modules/avatars/test_unlock_idempotency.py`

## 9. Files to Modify
- `src/noorheroes/modules/avatars/repository.py` — add `grant_ownership_if_absent(child_id, item_id)` (idempotent `INSERT ... ON CONFLICT (child_id, avatar_item_id) DO NOTHING`, returning whether a row was actually inserted)
- Consumer registry/startup wiring (wherever existing consumers are registered at app/worker startup, per the existing Kafka consumer framework)

## 10. Backend Requirements
- `UnlockEvaluationConsumer` subscribes to `badge_unlocked`, `achievement_level_progressed`, `habit_streak_state_changed` topics.
- For each event, `UnlockRuleMatcher.find_matching_items(event)` queries all non-retired `avatar_items` whose `unlock_rule` references the event's specific badge_id / level_threshold / habit_milestone_type+threshold, returning the matching set (may be empty, zero, or multiple items).
- For each matching item, call `AvatarRepository.grant_ownership_if_absent(child_id, item_id)` — an idempotent `INSERT ... ON CONFLICT (child_id, avatar_item_id) DO NOTHING`.
- Only if a new row was actually inserted (not a no-op conflict), trigger a notification via `NotificationService.dispatch_notification()` — this is the mechanism that prevents duplicate notifications on event redelivery.
- Kafka offset commit occurs only after the grant+notification-trigger step completes successfully (at-least-once semantics; idempotency at the DB layer compensates for any redelivery-driven reprocessing).
- Malformed/unprocessable events are logged and routed to a dead-letter queue, never crash the consumer or block subsequent messages.

## 11. KMP Requirements
N/A directly — consumed indirectly via K-04's diffing-based auto-unlock detection against B-01's `GET /v1/children/{id}/inventory` response.

## 12. NextJS Requirements
N/A directly — staging environment support for injecting fixture events onto these Kafka topics (enabling QA of auto-unlock without organically earning badges) is a DevOps/QA concern per PRD §10, not a NextJS Admin UI concern for this sub-feature.

## 13. API Contract
No new client-facing endpoint — this sub-feature is purely a Kafka consumer plus an internal call into `AvatarRepository`'s write path established in B-01. No new HTTP contract.

## 14. Database Requirements
Reuses `avatar_items` (read, for `unlock_rule` matching) and `child_inventory` (write, idempotent insert) from B-01 — no new tables. Relies on B-01's `UNIQUE(child_id, avatar_item_id)` constraint as the idempotency mechanism.

## 15. Validation
Event payload must include a valid `child_id` and the relevant criteria identifier (`badge_id`, level identifier, or habit-milestone type+value); malformed events are logged and dropped to the dead-letter queue rather than crashing the consumer or silently skipping without a trace.

## 16. Authentication
N/A (internal service-to-service Kafka consumer, not a user-facing endpoint); topic access controlled by existing broker ACLs.

## 17. Authorization
N/A (internal consumer; no user-initiated request path).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Same `badge_unlocked` event processed twice (redelivery) | Idempotent `ON CONFLICT DO NOTHING` insert → exactly one `child_inventory` row, exactly one notification triggered |
| Event references a since-deprecated/retired badge/milestone | No matching `avatar_items` found (or matcher treats as no-op); no crash, no dangling grant |
| Notification dispatch fails after a successful grant | Grant (the `child_inventory` row) is unaffected; item discoverable on next `GET inventory` call regardless (§1.11) |
| Malformed event payload | Logged, routed to dead-letter queue, consumer continues processing subsequent messages |
| Consumer crash mid-processing | Kafka offset not yet committed; event reprocessed on restart; idempotent insert prevents any resulting duplicate |
| Retired `avatar_item` still referenced by an active `unlock_rule` | Excluded from matching (`is_retired=true` items are never newly granted, per FR-10's "new acquisition only" scope) |

## 19. Offline First / 20. Local Data
N/A (backend internal service).

## 21. Localization / 22. RTL
N/A (no user-facing text produced directly here; the auto-unlock notification's copy is owned by the `notifications` context/K-04's celebration UI).

## 23. Analytics
Contributes the underlying state change that K-04 detects client-side to fire `avatar_item_auto_unlocked`; server-side grant events are logged for the Dashboard Metrics in PRD §11.3 (locked-item-teaser-engagement-rate by unlock-criteria-type).

## 24. Performance
Consumer must keep pace with event volume produced by A.7/A.9/A.11; `unlock_matcher` query indexed on `avatar_items(is_retired)` plus JSONB containment/path queries on `unlock_rule` — avoid full-table scans by indexing the JSONB fields actually queried (e.g., a GIN index on `unlock_rule` if query patterns require it). Monitored for consumer lag per PRD §10 DevOps Requirements (a stuck/slow consumer is a trust/satisfaction issue, not just a performance nuisance).

## 25. Security
Idempotent grant insertion (§10, §14) is this sub-feature's core integrity guarantee — protected by a CI-blocking duplicate-event test (§27). No new attack surface (internal consumer, no client-reachable endpoint).

## 26. Library Requirements
Existing Kafka consumer framework, SQLAlchemy 2.0 async — no new external dependencies.

## 27. Testing
- Unit: `UnlockRuleMatcher.find_matching_items()` correctness for all three rule types (badge / level / habit-milestone), including zero-match and multi-match cases.
- Unit/Integration (P0): process the same `badge_unlocked` event twice → assert exactly one `child_inventory` row exists and exactly one notification was triggered, not two (PRD Backend AI Code-Generation Prompt item 4, CI-blocking per PRD §10).
- Integration: retired-item exclusion from matching; deprecated-reference event produces no crash and no dangling grant.
- Integration: malformed event routed to dead-letter queue without blocking subsequent messages.
- Integration: broken-streak event (Edge Case 6) never triggers a revocation — engine has no revoke code path to test against, verified by absence-of-behavior assertion.

## 28. Documentation
Document the consumer's topic subscriptions, the idempotency-key strategy (DB unique constraint, not an application-level dedup cache), and the grant-before-notify ordering guarantee in the shared Avatar & Inventory Service architecture notes; update `FAST-API-INSTRUCTIONS.md`'s `avatars` context entry (established in B-01) with the consumer's presence.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement `grant_ownership_if_absent` Repository Method**
- Task ID: B-02-T01
- Objective: Idempotent `INSERT ... ON CONFLICT (child_id, avatar_item_id) DO NOTHING`, returning whether a row was actually inserted.
- Why This Is Required: this is the sole mechanism preventing duplicate grants/notifications under Kafka's at-least-once delivery semantics.
- Existing Architecture to Follow: `BaseRepository[ModelT]` mutation pattern from B-01.
- Files to Modify: `src/noorheroes/modules/avatars/repository.py`
- Implementation Details: use SQLAlchemy's `insert(...).on_conflict_do_nothing(index_elements=[...]).returning(...)` (PostgreSQL dialect) to detect actual-insert vs. no-op in one round trip.
- Tests: unit test asserting correct true/false return for fresh-insert vs. conflict cases.
- Definition of Done: method reliably distinguishes new-grant from already-owned, single query, no race condition under concurrent calls.

**Task 02 — Implement `UnlockRuleMatcher`**
- Task ID: B-02-T02
- Objective: `find_matching_items(event)` querying `avatar_items` for `unlock_rule` matches against an incoming event's criteria.
- Existing Architecture to Follow: reuses `UnlockRuleResolver`'s rule-shape knowledge from B-01 (same structured schema: `badge_id` | `level_threshold` | `habit_milestone_type`+`threshold`).
- Files to Create: `src/noorheroes/modules/avatars/unlock_matcher.py`
- Implementation Details: filter `is_retired=false`; match by JSONB field equality/containment per rule type.
- Performance: index the queried JSONB paths if match volume requires it.
- Tests: unit tests per rule type, zero-match, multi-match.
- Definition of Done: matcher returns the correct item set for all three rule-type fixtures.

**Task 03 — Implement `UnlockEvaluationConsumer`**
- Task ID: B-02-T03
- Objective: Kafka consumer subscribing to the three named topics, orchestrating matcher → grant → notification-trigger → offset commit.
- Existing Architecture to Follow: existing project Kafka consumer base class/framework.
- Files to Create: `src/noorheroes/modules/avatars/consumers.py`
- Implementation Details: for each event, call matcher, then for each matched item call `grant_ownership_if_absent`; only on `True` (new insert) call `NotificationService.dispatch_notification()`; commit offset only after this sequence completes without unhandled exception.
- Business Rules: FR-8, FR-9.
- Error Handling: malformed events → dead-letter queue, log, continue; DB failure mid-processing → do not commit offset, allow reprocessing.
- Tests: integration test with a mocked Kafka client feeding fixture events.
- Definition of Done: consumer correctly grants and notifies exactly once per genuinely-new unlock across all fixture scenarios.

**Task 04 — Add Idempotent Redelivery Test (P0)**
- Task ID: B-02-T04
- Objective: CI-blocking test proving redelivery-safety.
- Files to Create: `tests/modules/avatars/test_unlock_idempotency.py`
- Implementation Details: feed the identical `badge_unlocked` event twice through the consumer; assert exactly one `child_inventory` row and exactly one notification-dispatch call.
- Definition of Done: test passes and is registered as a mandatory, non-bypassable CI gate per PRD §10.

**Task 05 — Add Full Consumer Test Suite**
- Task ID: B-02-T05
- Files to Create: `tests/modules/avatars/test_unlock_evaluation_engine.py`
- Implementation Details: cover all three event types, retired-item exclusion, deprecated-reference no-crash, dead-letter routing.
- Definition of Done: full suite green.

**Task 06 — Wire Consumer Registration & Monitoring**
- Task ID: B-02-T06
- Objective: Register the consumer at worker startup; add consumer-lag monitoring hook per PRD §10.
- Files to Modify: existing consumer registry/startup wiring.
- Definition of Done: consumer runs as a standing process; lag metric exposed for alerting.

**Task 07 — Add Documentation**
- Task ID: B-02-T07
- Definition of Done: topic subscriptions, idempotency strategy, and grant-before-notify ordering documented in the `avatars` context architecture notes and `FAST-API-INSTRUCTIONS.md`.

**Task 08 — Final Code Review**
- Task ID: B-02-T08
- Do Not Change: event-topic producers owned by A.7/A.9/A.11; PostgreSQL/Kafka credentials.
- Expected Result: PR merge-ready, CI green including the P0 idempotency gate.

## 30. Definition of Done
Consumer reliably grants `child_inventory` ownership and triggers exactly one notification per genuinely-new unlock, across all three event types, with zero duplicate grants/notifications under simulated redelivery. Malformed events never crash the consumer. Retired items are never newly granted.

## 31. Final Verification Checklist
- [x] Consumer subscribes to `badge_unlocked`, `achievement_level_progressed`, `habit_streak_state_changed`
- [x] `UnlockRuleMatcher` correctly matches all three rule types
- [x] `grant_ownership_if_absent` is a single idempotent DB operation, race-safe under concurrent calls
- [x] Notification triggered only on genuinely-new grant, never on conflict no-op
- [x] Redelivery test (same event twice → one grant, one notification) passes and is CI-blocking
- [x] Malformed events routed to dead-letter queue without crashing the consumer
- [x] Retired items excluded from new-grant matching
- [x] Consumer-lag monitoring hook present
- [x] No PostgreSQL/Kafka credential changes
- [x] No unrelated existing-context or event-producer code modified
