# B-03 — Notification Policy Engine (Send-Time Evaluation)

## 1. Feature Context
Part of Feature B.17 — Notifications (Child-Facing). The single most important architectural principle in this entire service: **every policy/eligibility/binding check happens at actual send time, never relying on a stale intent-creation-time snapshot** (PRD §3.5, §5 backend prompt preamble). Alongside B-01, this is one of the two highest-priority guarantees in the feature (PRD §5).

## 2. Parent Feature
B.17 Notifications (Child-Facing) — Backend (FastAPI)

## 3. Sub-feature
B-03 Notification Policy Engine (Send-Time Evaluation)

## 4. Objective
Implement the `PolicyEngine` that evaluates every pending `notification_intent` at actual delivery-attempt time against consent, quiet hours/bedtime, frequency budget, locale/age eligibility, and the device's **currently active binding** — never against stale intent-creation-time state.

## 5. Business Requirements
- Parent controls per-child reminders and quiet hours; every reminder type is individually toggleable per child, quiet-hours/bedtime windows configured per child (FR-3, cross-ref C.23).
- Maximum frequency and fatigue budgets are server-enforced — never solely a client-side mute, never bypassable by any trigger path (FR-4).
- Every child-targeted notification passes a server-side policy check against `screen_time_policies` before send; client-side mute alone is never trusted (FR-10).
- Per-category daily/weekly frequency caps prevent fatigue; engagement nudges back off automatically after repeated non-opens (FR-11).
- Quiet-hours config changed after intent creation but before send must be respected using the **current** configuration at send time (Edge Case 6).
- Active binding changed after intent creation but before send must be re-checked at send time; the notification must never be delivered to whichever profile happens to be active now if that's not the intended target (Edge Case 1).
- A stale streak-risk (or similar) condition that resolved before send must result in suppression (Edge Case 7) — defense-in-depth alongside B-02's early cancellation.
- A child's age-band eligibility must be re-checked at send time using current data, not intent-creation-time data (Edge Case 11).

## 6. Existing Architecture
- Extends `src/noorheroes/modules/notifications/` (`FAST-API-INSTRUCTIONS.md` §5.8).
- Reads `screen_time_policies` owned by C.23 Parental Controls — read-only dependency, never modified here.
- Uses Redis for frequency-budget counters (per-category, per-child, sliding window), consistent with the project's existing Redis usage pattern (`FAST-API-INSTRUCTIONS.md` §1 infrastructure layer).

## 7. Existing Code to Reuse
- `BaseService`.
- C.23's `screen_time_policies` read accessor (reuse existing repository method rather than querying the table directly, if one exists; otherwise coordinate the read-only contract with the C.23 module owner).
- B-01's `DeviceBindingRepository.get_active_binding()`.

## 8. Files to Create
- `src/noorheroes/modules/notifications/policy_engine.py` — `PolicyEngine` with `evaluate(intent) -> PolicyDecision`.
- `src/noorheroes/modules/notifications/fatigue_backoff.py` — `FatigueBackoffTracker` (per-category/per-child open/non-open history, Redis-backed).
- `src/noorheroes/modules/notifications/delivery_worker.py` — Celery worker consuming `pending` intents and invoking `PolicyEngine.evaluate()`.
- `tests/modules/notifications/test_policy_engine.py`.

## 9. Files to Modify
- `src/noorheroes/modules/notifications/intent_repository.py` — add `mark_suppressed(intent_id, reason)`, `mark_processing(intent_id)`.

## 10. Backend Requirements
- `PolicyEngine.evaluate(intent)` performs, in order, at the moment of actual delivery attempt: (1) consent/per-category opt-in check, (2) quiet-hours/bedtime check against current `screen_time_policies`, (3) frequency-budget check (Redis counter), (4) age/locale eligibility check against current child data, (5) currently-active-binding check against B-01's live binding state, (6) stale-condition re-check where the trigger type supports one.
- Every check queries **live, current** state — no check may read a value cached from intent-creation time.
- On any failing check, `mark_suppressed(intent_id, reason)` with `suppression_reason` one of `quiet_hours|frequency_cap|consent|stale_condition|binding_inactive`.
- On full pass, hand off to B-04 (Template Renderer) then B-05 (Delivery Adapter).
- `FatigueBackoffTracker`: track non-open rate per category/child over a rolling window; if it exceeds a configurable threshold, automatically extend the minimum interval before the next eligible send for that category, until engagement resumes (FR-11).
- Redis or PostgreSQL failure during evaluation must fail **safe** (suppress) rather than fail-open (never send unpoliced).

## 11. KMP Requirements
Not applicable directly — client never participates in this evaluation.

## 12. NextJS Requirements
Not applicable directly; suppression-reason breakdown surfaces via N-04 (consumes B-08).

## 13. API Contract
**Internal only — not directly client-callable.** Invoked by `delivery_worker.py` Celery task consuming `notification_intents` with `status='pending'`.

- **Authentication:** N/A (internal worker).
- **Result:** intent transitions to `sent` (handed to B-05) or `suppressed` (with `suppression_reason`).

## 14. Database Requirements
- Uses `notification_intents` (B-02), `notification_preferences` (existing model, extended if needed with `channel`/`type`/`quiet_hours` per PRD §4.2), `device_profile_bindings` (B-01).
- Redis keys: `fatigue:{child_id}:{category}` (non-open counter), `freq_budget:{child_id}:{category}:{window}` (send counter).

## 15. Validation
- All five/six policy dimensions evaluated on every intent, in the documented order, with no short-circuit that skips the binding re-check (the highest-stakes check).

## 16. Authentication
N/A — internal worker process.

## 17. Authorization
N/A.

## 18. Error Handling
| Scenario | System Behavior |
|---|---|
| Redis unavailable during frequency-budget check | Fail-safe: suppress with `suppression_reason=frequency_cap` (conservative default), log as degraded-mode event |
| PostgreSQL unavailable during quiet-hours/binding lookup | Fail-safe: suppress, retry intent on next worker cycle rather than sending unpoliced |
| Concurrent evaluation of the same intent (worker race) | Idempotency via `status='processing'` claim before evaluation; a second worker sees `processing` and skips |
| Quiet-hours config changed after intent creation | Re-evaluated against current config; respected immediately (Edge Case 6) |
| Active binding changed after intent creation | Re-evaluated against current binding; notification not misdelivered (Edge Case 1) |
| Underlying condition resolved before send | Suppressed with `suppression_reason=stale_condition` (Edge Case 7) |

## 19. Offline First
N/A (backend).

## 20. Local Data
N/A.

## 21. Localization
Age/locale eligibility check consumes the child's current locale; does not itself render copy (B-04's responsibility).

## 22. RTL
N/A.

## 23. Analytics
`notification_suppressed` (`suppression_reason`), `notification_fatigue_backoff_applied`.

## 24. Performance
Frequency-budget and fatigue-backoff checks use Redis for O(1) lookups; policy evaluation must not introduce N+1 queries per intent — batch-load `screen_time_policies`/binding state where evaluating many intents per worker cycle.

## 25. Security
This engine is the sole enforcement point preventing quiet-hours/bedtime bypass and cross-profile misdelivery at send time — no trigger source (scheduled, event-driven, or admin campaign per B-07) may have a "fast path" that skips it (PRD §1.8 NFR, §12.1).

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Redis (`redis-py` async), Celery, Pydantic v2, pytest, pytest-asyncio.

## 27. Testing
- Unit: each policy dimension evaluated in isolation with mocked dependencies.
- Integration: create intent for Child A → change Child A's quiet-hours config before the delivery worker processes it → process → assert suppression reflects the **new** configuration (PRD §5 backend prompt item 2, mandatory).
- Integration: create intent targeting Child A's binding → switch installation's active binding to Child B before the worker processes it → assert the notification is **not** delivered to that installation (PRD §5 backend prompt item 3, mandatory, highest priority alongside B-01's atomicity test).
- Integration: simulate N consecutive non-opens → assert next eligible send for that category is delayed beyond normal cadence (PRD §5 backend prompt item 4).
- Failure-mode: simulate Redis/PostgreSQL unavailability → assert fail-safe suppression, never fail-open delivery.

## 28. Documentation
Document the "always re-check at send time" principle prominently at the top of `policy_engine.py`; document the evaluation order and each `suppression_reason` meaning.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement Consent & Per-Category Opt-In Check**
- Objective: First policy dimension.
- Files to Create: `policy_engine.py` (partial).
- Business Rules: FR-3.
- Tests: unit test for opted-out category.

**Task 02 — Implement Quiet-Hours/Bedtime Check Against Current Config**
- Objective: Second policy dimension, reading live `screen_time_policies`.
- Business Rules: FR-10.
- Tests: the mandatory PRD §5 item 2 integration test (change config after intent creation, before send).
- Definition of Done: test passes; config is read live, never from a cached/stale value.

**Task 03 — Implement Frequency Budget & Fatigue Backoff**
- Files to Create: `fatigue_backoff.py`.
- Business Rules: FR-4, FR-11.
- Implementation Details: Redis-backed counters, configurable backoff threshold.
- Tests: PRD §5 item 4 integration test (N consecutive non-opens → delayed next send).

**Task 04 — Implement Age/Locale Eligibility Re-Check**
- Objective: Fourth policy dimension using current child data (Edge Case 11).
- Tests: unit test for birthday-rollover scenario.

**Task 05 — Implement Currently-Active-Binding Re-Check**
- Objective: Fifth, highest-stakes policy dimension.
- Why Required: PRD's second-highest-priority guarantee in the entire service (§5, alongside B-01 item 1).
- Existing Files to Reuse: `DeviceBindingRepository.get_active_binding()` (B-01).
- Tests: the mandatory PRD §5 item 3 integration test (switch binding before delivery worker processes intent → assert non-misdelivery).
- Do Not Change: this check must never be short-circuited or made optional by any calling code path.
- Definition of Done: test passes; this is a CI-blocking gate per DevOps §10.

**Task 06 — Implement Stale-Condition Re-Check & Suppression Recording**
- Objective: Sixth dimension; record `suppression_reason` on any failure.
- Tests: Edge Case 7 scenario test.

**Task 07 — Implement Delivery Worker Orchestration**
- Files to Create: `delivery_worker.py`.
- Implementation Details: claim intent (`status='processing'`), run full `PolicyEngine.evaluate()`, hand off to B-04/B-05 on pass or mark suppressed on fail.
- Error Handling: fail-safe suppression on infra failure (§18).
- Tests: worker-race idempotency test.

**Task 08 — Add Analytics, Logging, and CI Gate Wiring**
- Analytics: `notification_suppressed`, `notification_fatigue_backoff_applied`.
- Documentation: per §28.
- CI: wire Task 02 and Task 05 tests as mandatory, non-bypassable CI gates (DevOps §10).
- Definition of Done: full suite green; CI gate active.

## 30. Definition of Done
- All six policy dimensions implemented and evaluated at actual send time against live state.
- Both mandatory PRD §5 integration tests (stale-config suppression, stale-binding non-misdelivery) pass and are CI-blocking.
- Fatigue backoff correctly delays repeat non-openers.
- Fail-safe behavior verified under Redis/PostgreSQL outage simulation.

## 31. Final Verification Checklist
- [ ] Every policy dimension reads live/current state, never intent-creation-time snapshots
- [ ] Quiet-hours config change after intent creation is respected at send time
- [ ] Active binding change after intent creation prevents misdelivery at send time
- [ ] Frequency budget and fatigue backoff correctly throttle repeat non-openers
- [ ] Age/locale eligibility re-checked against current child data
- [ ] Stale-condition intents are suppressed, not sent with inaccurate copy
- [ ] Infra failures (Redis/PostgreSQL) fail safe (suppress), never fail open
- [ ] Both mandatory concurrency/staleness integration tests pass and are CI-blocking
- [ ] `suppression_reason` correctly tagged and queryable for reporting (feeds B-08/N-04)
