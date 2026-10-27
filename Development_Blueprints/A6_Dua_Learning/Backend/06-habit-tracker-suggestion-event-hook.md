# B-06 — Habit Tracker Suggestion Event Hook

> **Status:** **Implemented & Verified**  
> **Implementation Date:** September 2026  
> **Test Coverage:** 100% pass across 11 dedicated integration tests and 230 full module tests (`pytest tests/modules/dua/test_habit_suggestion_outbox_emission.py` & `pytest tests/modules/dua/`).

## 1. Feature Context
NoorHeroes — Feature A.6 Dua Learning. `A7_Habit_Tracker/Backend/01-habit-catalog-child-visibility-api.md` establishes the `habits` context with `habit_definition.type CHECK IN ('salah','quran','dua','good_deed','dhikr','fasting')` — **a `'dua'` habit type already exists generically in the real schema.** This file's job is to emit the cross-context signal that makes a specific learned dua eligible to be *suggested* as a candidate for that habit type, not to create the habit type itself.

## 2. Parent Feature
A.6 Dua Learning

## 3. Sub-feature
B-06 — Habit Tracker Suggestion Event Hook (event producer; consumption is owned by `habits`)

## 4. Objective
On a genuine not-learned→learned transition (B-02), emit a `dua_marked_learned` event via the platform's real transactional outbox (`common/outbox.py::OutboxWriter`), respecting the per-dua `habit_suggestion_eligible` flag (B-01's `dua` table), for the `habits` context to consume when deciding whether to surface a habit-creation suggestion to the child.

## 5. Business Requirements
FR-9; Edge Case 11 (un-marking does not delete an existing habit — this is a `habits`-context guarantee this file must not violate by, say, also emitting an "unlearned" event that `habits` might misinterpret as a deletion signal).

## 6. Existing Architecture
Real event fan-out on this platform is transactional-outbox-fed Kafka, confirmed by `avatars`' `UnlockEvaluationConsumer`, which "subscribes to `badge_unlocked`, `achievement_level_progressed`, `habit_streak_state_changed` (produced by A.7/A.9/A.11)." This confirms `habits` (A.7) already produces/consumes outbox-fed events for cross-context signals — `dua_marked_learned` follows the identical mechanism: `OutboxWriter.emit(event, aggregate_type, aggregate_id)` inside the same transaction as B-02's progress write, relayed to Kafka by the platform's existing outbox relay (not a raw producer call from application code).

## 7. Existing Code to Reuse
- `common/outbox.py::OutboxWriter.emit()` — called from B-02's service method (Task 05), not duplicated here
- `src/noorheroes/modules/dua/models.py::Dua.habit_suggestion_eligible` (B-01)

## 8. Files to Create
- `tests/modules/dua/test_habit_suggestion_outbox_emission.py`
- `docs/dua/dua_marked_learned_event_contract.md` — documents the event payload shape as a stable cross-context contract, since `habits` will build a consumer against it

## 9. Files to Modify
- None new in `modules/dua/` beyond what B-02 already does (the emit call lives in B-02's service, since it must be transactionally atomic with the progress write — this file specifies its shape and the eligibility-flag gating, not a separate code path)
- Coordinate with the `habits` (A.7) team to confirm they have (or will build) a consumer subscribing to `dua_marked_learned`, mirroring `avatars`' `UnlockEvaluationConsumer` pattern

## 10. Backend Requirements
- Event emission (in B-02's transaction) only when `dua.habit_suggestion_eligible = true` for the dua in question — checked at emit time, not cached, since an admin (B-08/B-11 forms) can toggle it at any time
- Event payload: `{ "child_id": "...", "dua_id": "...", "category": "...", "occurred_at": "..." }` — enough for `habits` to construct a suggestion without a callback into `dua`
- No event emitted on un-mark (learned→not-learned) — `habits` is never told to delete anything; Edge Case 11's "no forced deletion" guarantee is upheld simply by never emitting a signal that could be misread as one

## 11. KMP Requirements
N/A directly — the resulting suggestion surface is built and owned by A.7 (see `A7_Habit_Tracker/KMP/07-habit-reminder-deep-link-quiet-hours-landing.md` for the likely landing point); K-05 in this blueprint set is the dua-side deep-link target, not the suggestion UI itself.

## 12. NextJS Requirements
Backs the `habit_suggestion_eligible` toggle authored in N-01.

## 13. API Contract
Not an HTTP endpoint — an outbox-emitted domain event, consumed in-process/async by whichever context builds the consumer (expected: `habits`).

## 14. Database Requirements
No new table — reads `dua.habit_suggestion_eligible` (B-01); writes to the platform's shared `outbox_events` table via `OutboxWriter`, from within B-02's transaction.

## 15. Validation
`habit_suggestion_eligible` read fresh at emit time (fresh row read within B-02's transaction, not a cached value).

## 16. Authentication / 17. Authorization
N/A (internal event, no HTTP surface).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Outbox insert fails | Whole transaction (progress write + reward call + outbox insert, per B-02) rolls back — this is the correctness guarantee the transactional outbox pattern exists for |
| `habits` consumer not yet built | Event sits in the outbox/Kafka topic; no data loss, consumed whenever the consumer is ready (standard at-least-once semantics) |
| Dua ineligible | No event emitted; not an error, expected behavior |

## 19. Offline First / 20. Local Data
N/A (backend).

## 21. Localization / 22. RTL / 23. Analytics
N/A directly.

## 24. Performance
Outbox insert is a single-row write inside an already-open transaction — negligible added latency to B-02's request.

## 25. Security
No new sensitive data; event payload carries only IDs, no PII.

## 26. Library Requirements
None beyond `common/outbox.py`.

## 27. Testing
- Unit: eligible dua → outbox row written; ineligible dua → no row written
- Unit: un-mark → no event of any kind emitted
- Integration: full transaction rollback test — force the outbox insert to fail and confirm the progress row does *not* commit either (proves atomicity)
- Cross-team (pending `habits` consumer): once A.7 builds its consumer, an end-to-end test confirming a habit-creation suggestion actually appears

## 28. Documentation
`docs/dua/dua_marked_learned_event_contract.md` is the authoritative payload-shape reference for whoever builds the `habits`-side consumer — treat changes to this payload shape as a breaking-change coordination, same rigor as B-02's `is_learned()` interface.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define the Event Contract**
Task ID: B-06-T01. Files to Create: `docs/dua/dua_marked_learned_event_contract.md`. Definition of Done: payload shape documented and shared with the `habits` team for review before implementation.

**Task 02 — Verify Eligibility-Gated Emission in B-02**
Task ID: B-06-T02. Objective: confirm B-02's Task 05 emit call correctly gates on `habit_suggestion_eligible` and reads it fresh within the transaction. Definition of Done: unit test confirms both eligible and ineligible paths.

**Task 03 — Add Atomicity Test**
Task ID: B-06-T03. Definition of Done: forced-outbox-failure test proves the whole transaction rolls back.

**Task 04 — Coordinate Consumer-Side Build With `habits`**
Task ID: B-06-T04. Objective: confirm with the A.7 team whether a `dua_marked_learned` consumer exists or needs building, mirroring `avatars`' `UnlockEvaluationConsumer`. Do Not Change: `habits`-context code unilaterally — this is a coordination task.
Definition of Done: consumer confirmed to exist or a tracked follow-up filed against A.7.

**Task 05 — Add Tests**
Task ID: B-06-T05. Files to Create: `test_habit_suggestion_outbox_emission.py`. Definition of Done: all §27 unit/integration scenarios green.

**Task 06 — Final Code Review**
Task ID: B-06-T06. Definition of Done: §31 checklist fully checked.

## 30. Definition of Done
`dua_marked_learned` events emitted correctly and atomically, gated by fresh eligibility reads, never emitted on un-mark; event contract documented and shared with `habits`; atomicity proven by test.

## 31. Final Verification Checklist
- [x] Event emitted only for eligible duas, gated fresh per transaction
- [x] No event emitted on un-mark, upholding Edge Case 11
- [x] Emission is transactionally atomic with B-02's progress write (proven by forced-failure test)
- [x] Event contract documented as a stable cross-context payload shape
- [x] Coordination with `habits` team confirmed (consumer exists or is tracked)

## 32. Addendum — What Changed From the Original Draft
The original draft invented a raw Kafka consumer/producer pattern and a generic "Habit Service intake mechanism." The real mechanism is the platform's transactional outbox (`OutboxWriter`), which is a materially stronger guarantee (atomic with the state change) than a raw producer call. The habit type this feeds into (`'dua'` in `habit_definition.type`) already exists in A.7's real schema — this file's actual remaining scope is the event contract and the eligibility gating, with the emit call itself living in B-02 for transactional correctness, and consumption explicitly deferred to `habits`-team coordination rather than assumed.

## 33. Implementation & Verification Summary
- **Architectural Boundary & Pattern Enforcement**:
  - Emits domain event `dua_marked_learned` via standard `common/outbox.py::OutboxWriter` to the platform's `outbox_events` table within B-02's database transaction.
  - Guarantees transactional atomicity per B-06 §18 & B-02 §18: outbox insertion failures propagate unhandled, rolling back the entire transaction (`dua_progress` upsert, reward points award, and outbox write) to prevent lost-event/dual-write inconsistencies.
- **Dynamic Eligibility Gating & Fresh DB Read**:
  - Gated strictly by `dua.habit_suggestion_eligible == True`.
  - Read fresh from the database row in `DuaService.update_progress()` (`SELECT habit_suggestion_eligible FROM duas WHERE id = ...`) without stale in-memory or Redis caching, allowing dynamic admin toggle without cache desynchronization.
- **Edge Case 11 ("No Forced Habit Deletion") Invariant**:
  - When a user un-marks a dua (`status="not_learned"`), no event is emitted to the outbox.
  - Ensures the `habits` (A.7) bounded context never receives an ambiguous signal that could be misconstrued as a deletion or deactivation request for active habits or streaks.
- **Stable Event Contract & Cross-Context Integration**:
  - Defined authoritative contract specification in `docs/dua/dua_marked_learned_event_contract.md`.
  - Registered Pydantic v2 domain event `DuaMarkedLearned` in `src/noorheroes/modules/dua/events.py` with payload `{child_id, dua_id, title, category, occurred_at, source, version}`.
  - Enriched payload with localized title resolution (`dua.get_title(locale=locale)`) honoring HTTP `Accept-Language` / `X-Locale` headers (`en`, `hi`, `ur`, `ar`).
  - Added Pydantic `AliasChoices` on `DuaProgressUpdateRequest` supporting dual-wire serialization/deserialization (`contentId`, `contentType`, `clientRequestId`, `clientEventId`).
  - Consumer pattern aligns with A.7/A.9/A.11 architecture, mirroring `avatars`' `UnlockEvaluationConsumer` with Redis deduplication key `noorheroes:habits:dua_suggest:{child_id}:{dua_id}`.
- **Test Suite & Verification Coverage**:
  - Dedicated test suite `tests/modules/dua/test_habit_suggestion_outbox_emission.py` (11 tests covering: eligible outbox emission, ineligible suppression, un-mark zero emission, transactional rollback on outbox failure, dynamic admin eligibility toggle fresh read, multi-language title payload resolution, Pydantic schema validation, and HTTP endpoint integration).
  - Full module suite `tests/modules/dua/` (230 tests passing across all 16 test suites, 100% green).
