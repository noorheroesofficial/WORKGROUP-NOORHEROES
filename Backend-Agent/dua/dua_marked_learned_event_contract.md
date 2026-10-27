# Domain Event Contract: `dua_marked_learned`

## 1. Context & Purpose
- **Producer:** `dua` Bounded Context (`src/noorheroes/modules/dua/`) — Feature A.6 (Dua Learning / Blueprint B-06).
- **Consumers:**
  - `habits` Bounded Context (Feature A.7 Habit Tracker) — surfaces a contextual habit-reminder suggestion in the child learner's habit dashboard.
  - `rewards` Bounded Context (Feature A.11 Rewards System) — in addition to synchronous in-process points award.
- **Delivery Mechanism:** Transactional Outbox pattern via `common/outbox.py::OutboxWriter` relaying to Kafka topic `events.dua.learned` and Celery worker queues.

---

## 2. Event Envelope & Payload Specification

```json
{
  "event_id": "018f2d5e-8b6b-7123-9c8a-123456789abc",
  "event_type": "dua_marked_learned",
  "aggregate_type": "dua",
  "aggregate_id": "018f2d5e-8b6b-7123-9c8a-987654321def",
  "occurred_at": "2026-09-11T03:00:00.000000Z",
  "payload": {
    "child_id": "018f2d5e-8b6b-7123-9c8a-111111111111",
    "dua_id": "018f2d5e-8b6b-7123-9c8a-987654321def",
    "category": "morning",
    "habit_suggestion_eligible": true,
    "title": "Waking Up Supplication"
  }
}
```

### Field Definitions

| Field | Type | Required | Description |
|---|---|---|---|
| `event_id` | `UUIDv7 / ULID string` | Yes | Unique identifier of the outbox event record. |
| `event_type` | `string` | Yes | Literal `"dua_marked_learned"` (aliases: `"dua.marked_learned"`). |
| `aggregate_type` | `string` | Yes | Literal `"dua"`. |
| `aggregate_id` | `UUIDv7 string` | Yes | Canonical `dua_id`. |
| `occurred_at` | `ISO 8601 UTC string` | Yes | UTC timestamp when the status transition was committed. |
| `payload.child_id` | `UUID string` | Yes | Identifier of the child learner profile. |
| `payload.dua_id` | `UUID string` | Yes | Identifier of the learned dua. |
| `payload.category` | `string` | Yes | Category taxonomy slug (e.g. `'morning'`, `'food'`, `'bedtime'`). |
| `payload.habit_suggestion_eligible` | `boolean` | Yes | Must be `true` for A.7 habit suggestion surfacing (FR-9). |
| `payload.title` | `string` | Yes | Resolved title of the dua (in requested client locale or English fallback). |

---

## 3. Emission Invariants & Gating

1. **Genuine State Transition Only:** Emitted strictly when moving from non-learned (or initial empty state) to `status="learned"` (`was_transition == True`). Repeated idempotent submissions of `learned` do NOT re-emit the event.
2. **Eligibility Flag Fresh Read:** Emitted only if `dua.habit_suggestion_eligible == True`. The flag is evaluated fresh from the database within the transaction, preventing stale cache anomalies if an admin mutates the eligibility toggle.
3. **No Event on Un-mark (Edge Case 11 Guarantee):** When a child toggles a dua to `not_learned`, NO deletion or unlearning event is emitted. Existing habit configurations in Feature A.7 are never forcibly removed or modified when a dua is un-marked.
4. **Transactional Outbox Atomicity:** The outbox record is written inside the exact same database transaction as the `dua_progress` row upsert. If outbox insertion fails, the entire transaction rolls back. Zero partial writes or dual-write anomalies are permitted.
5. **Multi-Language Title Resolution:** The `title` field in the payload resolves the localized title matching the client request locale (`en`, `hi`, `ur`, `ar`), falling back gracefully to English and canonical title.

---

## 4. Consumer Implementation Guidance for Feature A.7 (`habits`)

Feature A.7 (`habits`) context should mirror the established consumer architecture pattern (e.g., `avatars`' `UnlockEvaluationConsumer`):

```python
class DuaLearnedHabitSuggestionConsumer:
    """
    Subscribes to 'dua_marked_learned' events on topic 'events.dua.learned'.
    Surfaces a habit-creation candidate suggestion for the child learner.
    """

    async def handle_event(self, event_envelope: Dict[str, Any]) -> None:
        payload = event_envelope.get("payload", {})
        child_id = payload.get("child_id")
        dua_id = payload.get("dua_id")
        category = payload.get("category")
        eligible = payload.get("habit_suggestion_eligible", False)
        title = payload.get("title", "Dua")

        if not eligible or not child_id or not dua_id:
            return

        # 1. Deduplication check in Redis (e.g., 7-day cooldown per dua suggestion)
        dedup_key = f"noorheroes:habits:suggestion:{child_id}:{dua_id}"
        if await redis.exists(dedup_key):
            return

        # 2. Check if habit of type 'dua' already exists for this dua_id
        existing_habit = await habit_service.find_child_habit(child_id=child_id, source_id=dua_id)
        if existing_habit:
            return

        # 3. Create candidate habit suggestion record (habit_definition.type = 'dua')
        await habit_suggestion_service.create_candidate_suggestion(
            child_id=child_id,
            habit_type="dua",
            source_id=dua_id,
            suggested_title=f"Read {title}",
            category=category,
        )
        await redis.set(dedup_key, "suggested", ex=604800)
```

---

## 5. Idempotency & Delivery Semantics
- **Delivery Guarantee:** At-least-once via transactional outbox relay.
- **Deduplication Key:** `f"noorheroes:habits:dua_suggest:{child_id}:{dua_id}"`.
- **Consumer Contract:** Consumers must be idempotent based on `event_id` and composite key `(child_id, dua_id)`.
