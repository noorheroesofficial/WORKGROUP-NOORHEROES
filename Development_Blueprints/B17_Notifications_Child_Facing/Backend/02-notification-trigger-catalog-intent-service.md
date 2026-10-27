# B-02 — Notification Trigger Catalog & Intent Service

## 1. Feature Context
Part of Feature B.17 — Notifications (Child-Facing). Implements the first stage of the canonical Notification Flow (PRD §1.17/§3.2): domain events or schedules create a notification intent, which the Policy Engine (B-03) later evaluates.

## 2. Parent Feature
B.17 Notifications (Child-Facing) — Backend (FastAPI)

## 3. Sub-feature
B-02 Notification Trigger Catalog & Intent Service

## 4. Objective
Implement the `NotificationIntentService`, consuming domain events/schedules from A.4 (bedtime story), A.7 (daily reminder, streak-risk), A.11 (reward/milestone), content-publish (A.3/A.5/A.6), and the seasonal calendar job, and creating `notification_intents` rows for the Policy Engine to evaluate.

## 5. Business Requirements
- Child-facing notification classes: approved learning reminder (daily reminder), bedtime story, streak-at-risk, new content, seasonal event, and child-side reward/milestone copy (FR-1).
- Trigger conditions (FR-12): daily reminder fires when the daily goal is unmet by a configurable threshold hour; streak risk fires on late-day inactivity with an active streak; bedtime story fires 30 minutes before configured bedtime (midnight-crossing-safe, cross-ref A.4); new content fires on publish within the child's age/locale eligibility; reward notifications fire on a notify-worthy Reward Service ledger entry; seasonal notifications fire via an Islamic-calendar scheduling job targeting parent + active children.
- In-app (non-push) notifications also exist for some triggers (e.g., "Tomorrow's episode is ready") and pass through the same policy engine for consent/eligibility purposes (FR-13).
- An intent whose underlying condition resolves before send (e.g., streak no longer at risk) must be canceled/suppressed rather than sent with stale copy (Edge Case 7).

## 6. Existing Architecture
- Extends `src/noorheroes/modules/notifications/` per `FAST-API-INSTRUCTIONS.md` §5.8.
- Consumes Kafka topic `notification-triggers`, published to by A.4/A.7/A.11/content-publish/seasonal-scheduler domain services — this sub-feature is the consumer side only; publishing from those feature modules is each feature's own responsibility (already established for A.7 §PRD `streak_state_changed` and similar events) and is out of scope here except for the consumer contract this service exposes.
- Reuse Celery for the scheduled triggers (daily reminder threshold check, bedtime story 30-minutes-before job, seasonal calendar job), consistent with the existing Celery usage pattern in the `localization` context (`FAST-API-INSTRUCTIONS.md` §5.6 task examples).

## 7. Existing Code to Reuse
- `BaseService`, `BaseRepository[ModelT]`.
- Existing Celery worker configuration/patterns from `localization` context tasks.
- A.7's `Streak` state (read-only consumption for streak-risk trigger).

## 8. Files to Create
- `src/noorheroes/modules/notifications/intent_service.py` — `NotificationIntentService(BaseService)`.
- `src/noorheroes/modules/notifications/intent_repository.py` — `NotificationIntentRepository(BaseRepository[NotificationIntent])`.
- `src/noorheroes/modules/notifications/trigger_consumer.py` — Kafka consumer for `notification-triggers` topic.
- `src/noorheroes/modules/notifications/tasks.py` — Celery tasks: `evaluate_daily_reminder_threshold_task()`, `evaluate_bedtime_story_trigger_task()`, `evaluate_seasonal_calendar_task()`.
- Extend `models.py`: `NotificationIntent`.
- `alembic/versions/<rev>_create_notification_intent_table.py`.
- `tests/modules/notifications/test_intent_service.py`.

## 9. Files to Modify
- None outside this module — publishing to `notification-triggers` is owned by A.4/A.7/A.11/content/localization modules, not modified here.

## 10. Backend Requirements
- `create_intent(event_or_schedule_ref, notification_type, target_child_id, payload)` — idempotent creation; dedupe on `(target_child_id, notification_type, trigger_window)` to prevent double-fire.
- `cancel_intent_if_stale(intent_id)` — invoked by a lightweight re-check just before Policy Engine hand-off (Edge Case 7); the authoritative stale-condition check itself lives in the Policy Engine (B-03) at send time per the "always re-check at send time" principle, but this service supports early cancellation when the domain event source itself signals resolution (e.g., A.7 publishes a `streak_risk_resolved` event).
- Scheduled Celery tasks fire within their configured time window with minute-level accuracy (NFR, PRD §1.8).
- Bedtime-story trigger's "30 minutes before bedtime" calculation must correctly handle a bedtime window crossing midnight, consistent with A.4's established midnight-crossing-window logic (Edge Case 3) — reuse A.4's bedtime-window utility rather than reimplementing.

## 11. KMP Requirements
Not applicable — server-side only.

## 12. NextJS Requirements
Not applicable directly; intent volume/suppression visibility surfaces via N-04 Delivery & Engagement Report Dashboard (consumes B-08).

## 13. API Contract

**Required API — Internal, not directly client-callable**
- **Trigger:** Kafka message on `notification-triggers` topic, or Celery scheduled task firing.
- **Consumer Contract:** `{ "event_type": "streak_risk|daily_reminder_due|bedtime_story_due|content_published|reward_posted|seasonal_event", "child_id": "uuid", "payload": {...} }`
- **Result:** `notification_intents` row created with `status='pending'`.
- **Authentication:** N/A (internal service-to-service, trusted topic).
- **Error Responses:** malformed payload → dead-letter queue with logged error, never a silent drop.

## 14. Database Requirements
- `notification_intents`: `intent_id UUID PK`, `event_or_schedule_ref VARCHAR`, `target_binding VARCHAR`, `notification_type VARCHAR`, `target_child_id UUID`, `payload JSONB`, `status VARCHAR CHECK IN ('pending','processing','sent','suppressed','canceled')`, `created_at TIMESTAMPTZ`; index `(status, created_at)`.

## 15. Validation
- Reject/dead-letter malformed event payloads (missing `child_id` or unrecognized `event_type`).
- Dedupe key prevents duplicate intents for the same child/type/window.

## 16. Authentication
N/A — internal event-driven service.

## 17. Authorization
N/A.

## 18. Error Handling
| Scenario | System Behavior |
|---|---|
| Malformed/unknown event payload | Routed to dead-letter queue with structured error log; consumer continues processing subsequent messages |
| Downstream event source outage (A.4/A.7/A.11 unavailable) | Scheduled Celery tasks continue operating independently; missed real-time events are not retroactively reconstructed (logged as a gap for monitoring) |
| Duplicate event for same trigger window | Deduped at intent-creation time, no duplicate intent created |
| Stale condition signaled before send | Intent status set to `canceled`, never reaches delivery |

## 19. Offline First
N/A (backend).

## 20. Local Data
N/A.

## 21. Localization
Intent `payload` carries locale-neutral data only (ids, counts, timestamps); copy rendering (localized) happens downstream in B-04 Template Governance.

## 22. RTL
N/A.

## 23. Analytics
`notification_intent_created` (`type`, `target_binding`).

## 24. Performance
Kafka consumer processes messages asynchronously without blocking; scheduled tasks batch-evaluate eligible children per threshold hour rather than per-child polling, to handle simultaneous large batches (DevOps §10).

## 25. Security
No sensitive/billing data included in intent `payload` for child-facing types — enforced at the boundary before payload is persisted, complementing B-04's template-level blocklist.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Celery, Kafka client (`aiokafka` or existing project standard), Pydantic v2, pytest.

## 27. Testing
- Unit: intent creation/dedup logic per trigger type.
- Unit: bedtime-story midnight-crossing calculation (reusing/mirroring A.4's test fixtures).
- Integration: full event → intent pipeline via test Kafka topic.
- Integration: scheduled task fires within configured window (minute-level accuracy assertion).

## 28. Documentation
Document the consumer contract schema and each trigger's condition formula (§5) in module-level docstrings; cross-reference PRD FR-12.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create NotificationIntent Model & Migration**
- Files to Create: `models.py` extension, migration.
- Definition of Done: table created with `status` CHECK constraint.

**Task 02 — Implement NotificationIntentRepository**
- Files to Create: `intent_repository.py`.
- Implementation Details: `create_if_not_exists()` (dedupe), `get_pending()`, `mark_canceled()`.
- Tests: unit tests.

**Task 03 — Implement Kafka Trigger Consumer**
- Files to Create: `trigger_consumer.py`.
- Implementation Details: consume `notification-triggers`, validate payload, call `NotificationIntentService.create_intent()`.
- Error Handling: dead-letter queue routing per §18.
- Tests: integration test with a test topic/fixture events.

**Task 04 — Implement Scheduled Celery Tasks**
- Files to Create: `tasks.py`.
- Implementation Details: `evaluate_daily_reminder_threshold_task()`, `evaluate_bedtime_story_trigger_task()` (reusing A.4 midnight-crossing utility), `evaluate_seasonal_calendar_task()`.
- Business Rules: FR-12 trigger conditions.
- Tests: unit tests per task; integration test for minute-level scheduling accuracy.

**Task 05 — Implement Stale-Condition Early Cancellation**
- Files to Modify: `intent_service.py`.
- Implementation Details: `cancel_intent_if_stale()` invoked on resolution-signaling events (e.g., `streak_risk_resolved`).
- Tests: unit test for cancellation path.

**Task 06 — Add Analytics & Logging**
- Files to Modify: `intent_service.py`.
- Analytics: `notification_intent_created` per §23.
- Definition of Done: verified via event-bus test double.

**Task 07 — Write Tests & Documentation**
- Tests: full suite per §27.
- Documentation: docstrings per §28.
- Definition of Done: all green, documented.

## 30. Definition of Done
- All six trigger types create correctly-scoped intents.
- Dedup prevents double-fire; stale intents are cancelable pre-send.
- Scheduled triggers fire within their configured window with minute-level accuracy.
- Bedtime-story midnight-crossing logic verified consistent with A.4.

## 31. Final Verification Checklist
- [ ] Each of the six trigger classes (FR-1) creates a correctly-scoped intent
- [ ] Dedup key prevents duplicate intents per child/type/window
- [ ] Malformed events are dead-lettered, not silently dropped
- [ ] Bedtime-story trigger correctly handles midnight-crossing bedtime windows
- [ ] Scheduled tasks fire within their configured time window (minute-level accuracy)
- [ ] Stale-condition early cancellation works for at least the streak-risk case
- [ ] No sensitive/billing content present in child-facing intent payloads
- [ ] Full test suite passes
