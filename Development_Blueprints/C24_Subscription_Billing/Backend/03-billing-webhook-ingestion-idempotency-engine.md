# Blueprint: Billing Webhook Ingestion & Idempotency Engine

## 1. Feature Context
Platform: NoorHeroes Backend (FastAPI). Module: `src/noorheroes/modules/subscriptions/`. Delivers the Webhook Receiver: `POST /api/v1/billing/webhooks/play`, the second of the two highest-priority integrity guarantees in the Billing Service (alongside B-02's receipt validation).

## 2. Parent Feature
C.24 — Subscription & Billing.

## 3. Sub-feature
B-03 — Billing Webhook Ingestion & Idempotency Engine.

## 4. Objective
Ingest signed Google Play/App Store webhooks, verify signatures, drive subscription state-machine transitions, and guarantee idempotent processing on `provider_event_id` so a replayed delivery is always a safe no-op.

## 5. Business Requirements
Source: PRD §1.7 FR-2, FR-6, §3.4 (`POST /api/v1/billing/webhooks/play`), §5 AI Code-Gen Prompt item 2, Edge Case #9.
- Idempotent on `provider_event_id` — DB-level `UNIQUE` constraint is the idempotency backbone, not application-level deduplication alone.
- Drives all canonical state-machine transitions: `Trial→ActivePaid`, `ActivePaid→RenewalPending`, `RenewalPending→ActivePaid|PastDue`, `PastDue→ActivePaid|Free`, `ActivePaid→Canceled`, `Canceled→Free`, `ActivePaid→DowngradeScheduled`, `DowngradeScheduled→Free`.
- Illegal transitions must be unreachable — the state machine is a pure function validating only exact legal transitions.
- Not user-facing; authenticated by webhook signature verification, not a user session.

## 6. Existing Architecture
Per `FAST-API-INSTRUCTIONS.md` §5.10: extends `subscriptions` module. Requires a new `SubscriptionStateMachine` pure-function component (not yet in inventory — build fresh, do not guess an existing implementation). Webhook signature verification requires a new `infrastructure/store_billing/webhook_verifier.py` client.

## 7. Existing Code to Reuse
- `SubscriptionRepository` — extend with `find_by_provider_event_id()`, `record_webhook_event()`, `apply_state_transition()`.
- `SubscriptionService(BaseService)` — extend with `process_webhook(payload, signature)`.
- Analytics Event Bus client (existing platform-wide event emission pattern, used elsewhere e.g. C.20's reward events).

## 8. Files to Create
- `src/noorheroes/modules/subscriptions/state_machine.py` — `SubscriptionStateMachine` (pure function, exhaustive legal-transition table)
- `src/noorheroes/infrastructure/store_billing/webhook_verifier.py` — signature verification
- `src/noorheroes/modules/subscriptions/models.py` — add `BillingWebhookEvent` model (if absent)
- `tests/modules/subscriptions/test_billing_webhook_ingestion_idempotency.py`

## 9. Files to Modify
- `src/noorheroes/modules/subscriptions/schemas.py` — add `WebhookPayload`
- `src/noorheroes/modules/subscriptions/service.py` — add `process_webhook()`
- `src/noorheroes/modules/subscriptions/repository.py` — add webhook-event and state-transition methods
- `src/noorheroes/modules/subscriptions/api.py` — add `POST /api/v1/billing/webhooks/play` route
- Alembic migration — add `billing_webhook_event` table with `UNIQUE(provider_event_id)`

## 10. Backend Requirements
- Route: `POST /api/v1/billing/webhooks/play`, no user auth — webhook signature verification instead.
- `SubscriptionService.process_webhook(payload, signature)`:
  1. Verify signature via `WebhookVerifier.verify(payload, signature)`; reject with `401` on failure.
  2. Attempt insert into `billing_webhook_event` keyed on `provider_event_id`. On `UNIQUE` constraint violation, return `200` immediately without reprocessing (idempotent no-op) and log `webhook_processing_idempotent_skip`.
  3. On successful insert (first delivery), resolve the target subscription via `subscription_id`/receipt reference.
  4. Call `SubscriptionStateMachine.transition(current_state, event_type)` — a pure function returning the new state or raising `IllegalTransitionError` if the event doesn't map to a legal transition from the current state.
  5. Persist the new state via `apply_state_transition()`.
  6. If the transition reduces `child_capacity` below the family's `active_child_count`, delegate to B-07 (Plan-Capacity Downgrade Orchestration) — do not implement disable logic here.
  7. Emit `webhook_received`, and the relevant lifecycle event (`trial_auto_converted`, `payment_failed`, `grace_period_entered`, etc.) to the Analytics Event Bus.

## 11. KMP Requirements
Indirect — this endpoint drives the server-side state that `GET /v1/parent/subscription` (B-05) later reflects to the client. No direct KMP call to this endpoint (webhook is store-to-server only).

## 12. NextJS Requirements
Indirect — N-02/N-05 read the resulting state-transition history and webhook-event log for support investigation.

## 13. API Contract
- **HTTP Method:** POST
- **Endpoint:** `/api/v1/billing/webhooks/play`
- **Auth:** Webhook signature verification (store-specific signing scheme)
- **Request:** Provider-defined webhook payload (Google Play RTDN / App Store Server Notification format) containing `provider_event_id`, `event_type`, subscription reference
- **Response 200:** `{ "received": true }` (both for first-time processing and idempotent replay)
- **Authentication:** Signature verification (not a Bearer session)
- **Authorization:** N/A (trust boundary is the signature, not a user identity)
- **Validation:** Payload schema-validated after signature verification passes
- **Error Responses:** `401` invalid signature; `422` malformed payload (valid signature but unparseable); `409` mapped internally to a safe `200` no-op for idempotent replay (never surfaced as an error to the store's retry logic, to avoid triggering unnecessary re-delivery storms)

## 14. Database Requirements
New/confirmed table `billing_webhook_event` (PRD §4.2): `event_id` PK, `provider_event_id` **UNIQUE**, `subscription_id` FK, `event_type`, `processing_status`, `received_at`; index `(subscription_id, received_at DESC)`. Append-only, no deletion lifecycle (§4.4/§4.5).

## 15. Validation
- Signature must verify before any payload parsing.
- `provider_event_id` required and used as the idempotency key.
- `event_type` must map to a known transition trigger; unknown event types are logged and safely ignored (not an error, given store webhook vocabularies may expand).

## 16. Authentication
Webhook signature verification (store-specific — Google Play RTDN JWT or App Store Server Notification signed payload).

## 17. Authorization
N/A — trust boundary is cryptographic signature verification, not a user/session identity.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Invalid signature | `401`, event not recorded |
| Duplicate `provider_event_id` | `200` safe no-op, logged as `webhook_processing_idempotent_skip` (Edge Case #9) |
| Illegal state transition per state machine | Event recorded with `processing_status=rejected`, alertable, does NOT crash the request (return `200` to avoid store retry storms, but flag for manual investigation) |
| Unknown `event_type` | Recorded, safely ignored, logged |
| DB failure during processing | `503`, store will retry per its own delivery guarantees |

## 19. Offline First
N/A (server-to-server webhook).

## 20. Local Data
N/A (backend).

## 21. Localization
N/A — internal/no user-facing content.

## 22. RTL
N/A.

## 23. Analytics
`webhook_received`, `webhook_processing_idempotent_skip` (internal), plus the resulting lifecycle event (`trial_auto_converted`, `payment_failed`, `payment_recovered`, `grace_period_entered`, `grace_period_expired`) per §1.19.

## 24. Performance
- Webhook Receiver must be highly available (PRD §10 DevOps) — this is a billing-correctness-critical ingestion point.
- DB-level `UNIQUE` constraint check is fast (indexed) and is the primary defense, not an application-level lock.
- Process synchronously within the request (webhook payloads are small; no need to queue for this ingestion step, though downstream heavy work like report regeneration should be dispatched async if applicable).

## 25. Security
- Signature verification is mandatory and non-bypassable — no webhook processed without a verified signature.
- No PII beyond what the store payload itself contains (subscription/receipt references).
- Rollback strategy (PRD §15.2) treats any confirmed duplicate-webhook-processing entitlement drift as a P0 incident.

## 26. Library Requirements
Google Play RTDN / App Store Server Notification signature verification library (JWT verification or equivalent, per chosen store SDK — confirm exact package before adding).

## 27. Testing
1. Unit test: same webhook payload fired twice → state transitions exactly once, second call returns `200` no-op (Edge Case #9, PRD §5 item 2 — CI-blocking).
2. Unit test: invalid signature → `401`, no state change.
3. Exhaustive unit tests: every legal transition in the canonical diagram succeeds.
4. Exhaustive unit tests: illegal transitions (e.g., `Free→ActivePaid` directly) are rejected/unreachable.
5. Unit test: capacity-reducing transition delegates to B-07 rather than disabling children inline.
6. Integration test: full webhook-to-state-transition flow against a store sandbox fixture sequence, including deliberately duplicated/out-of-order deliveries.
7. Integration test: unknown `event_type` safely ignored, no crash.

## 28. Documentation
OpenAPI docstring noting webhook-signature auth model; module documentation includes the full legal-transition table as a reference for future maintainers.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement Webhook Signature Verifier**
- Task ID: B03-T01
- Objective: `WebhookVerifier.verify(payload, signature)`.
- Why This Is Required: Non-bypassable trust boundary for this endpoint.
- Existing Architecture to Follow: New `infrastructure/store_billing/` client module (shared with B-02's receipt validator).
- Existing Files to Reuse: `infrastructure/store_billing/` package scaffold from B-02.
- Files to Create: `infrastructure/store_billing/webhook_verifier.py`.
- Files to Modify: none.
- Implementation Details: JWT/signature verification per store's documented scheme.
- Business Rules: FR-2/FR-6.
- Validation: Reject on any verification failure, no partial trust.
- Error Handling: Typed `InvalidSignatureError`.
- Security: This IS the security boundary.
- Performance: Fast, synchronous cryptographic check.
- Localization/RTL/Analytics: N/A.
- Tests: Covered in Task 05.
- Documentation: Docstring on signing scheme assumptions.
- Dependencies: none.
- Do Not Change: Do not weaken verification for testing convenience in production code paths (use dependency override in tests only).
- Expected Result: Reliable verify/reject signal.
- Definition of Done: Invalid signature reliably rejected.

**Task 02 — Implement Idempotent Webhook Event Table & Insert Logic**
- Task ID: B03-T02
- Objective: `billing_webhook_event` table with `UNIQUE(provider_event_id)`; insert-or-detect-duplicate logic.
- Why This Is Required: The idempotency backbone (PRD §5 item 2).
- Existing Architecture to Follow: Alembic migration pattern, `BaseRepository`.
- Existing Files to Reuse: existing migration conventions.
- Files to Create: Alembic migration; `models.py` addition.
- Files to Modify: `repository.py`.
- Implementation Details: DB-level constraint is authoritative; catch `IntegrityError` on violation and treat as safe no-op, not an application error.
- Business Rules: FR-6, Edge Case #9.
- Validation: `provider_event_id` non-null, indexed unique.
- Error Handling: `IntegrityError` → no-op path, not propagated as 500.
- Security: Prevents double-processing-driven entitlement drift.
- Performance: Indexed unique constraint, O(1) lookup via index.
- Localization/RTL/Analytics: N/A.
- Tests: Covered in Task 05.
- Documentation: Migration comment explaining idempotency role.
- Dependencies: Task 01.
- Do Not Change: Do not implement deduplication purely at the application layer without the DB constraint — the DB constraint is mandatory.
- Expected Result: Duplicate `provider_event_id` insert reliably detected.
- Definition of Done: Duplicate-fire test passes.

**Task 03 — Implement Subscription State Machine (Pure Function)**
- Task ID: B03-T03
- Objective: `SubscriptionStateMachine.transition(current_state, event_type) -> new_state`.
- Why This Is Required: PRD §5 item 3 — exhaustive, exact legal-transition enforcement.
- Existing Architecture to Follow: Pure function, no side effects, easily exhaustively testable.
- Existing Files to Reuse: none (new component).
- Files to Create: `modules/subscriptions/state_machine.py`.
- Files to Modify: none.
- Implementation Details: Explicit transition table matching PRD §1.17 Mermaid diagram exactly (12 legal transitions); raise `IllegalTransitionError` for anything else.
- Business Rules: FR-2, canonical state machine.
- Validation: Exhaustive table, no wildcard/catch-all transitions.
- Error Handling: `IllegalTransitionError` typed and distinct.
- Security: Prevents entitlement being pushed into an invalid state via a crafted/unexpected event sequence.
- Performance: O(1) dict lookup.
- Localization/RTL/Analytics: N/A.
- Tests: Covered in Task 05 (exhaustive legal + illegal transition tests).
- Documentation: Table documented inline matching PRD diagram.
- Dependencies: none.
- Do Not Change: Do not add transitions not present in the canonical diagram without a PRD update.
- Expected Result: Correct, exhaustively-tested transition function.
- Definition of Done: All 12 legal transitions pass; representative illegal transitions rejected.

**Task 04 — Implement process_webhook Orchestration & Route**
- Task ID: B03-T04
- Objective: Wire signature verification → idempotent insert → state machine → persistence → capacity-check delegation → analytics.
- Why This Is Required: Full end-to-end webhook processing per §10.
- Existing Architecture to Follow: `SubscriptionService`, existing router pattern.
- Existing Files to Reuse: Tasks 01–03 components, B-07 (capacity delegation, referenced not reimplemented).
- Files to Create: none.
- Files to Modify: `service.py`, `api.py`, `schemas.py`.
- Implementation Details: Per §10 steps 1–7 exactly, in order.
- Business Rules: FR-2, FR-6.
- Validation: Per §15.
- Error Handling: Per §18.
- Security: Signature check is step 1, non-skippable.
- Performance: Synchronous processing, fast path.
- Localization/RTL: N/A.
- Analytics: Emit per §23.
- Tests: Covered in Task 05.
- Documentation: OpenAPI + module docstring.
- Dependencies: Tasks 01–03.
- Do Not Change: Do not reimplement child-disabling logic here — delegate to B-07 only.
- Expected Result: Full webhook flow operational.
- Definition of Done: Matches §13 exactly.

**Task 05 — Write Test Suite (Idempotency Priority)**
- Task ID: B03-T05
- Objective: Cover all 7 scenarios in §27, with the duplicate-delivery test treated as CI-blocking.
- Why This Is Required: Second of the two highest-priority guarantees in the service (PRD §5).
- Existing Architecture to Follow: pytest, async test client, store sandbox webhook fixtures.
- Existing Files to Reuse: Fixture factories for subscription state.
- Files to Create: `tests/modules/subscriptions/test_billing_webhook_ingestion_idempotency.py`.
- Files to Modify: none.
- Implementation Details: 7 test cases per §27, including deliberately duplicated/out-of-order fixture sequences (per PRD §15.2 rollback-testing requirement).
- Business Rules: N/A.
- Validation: N/A.
- Error Handling: Assert exact status codes/no-op behavior.
- Security: Duplicate-processing test is CI-blocking.
- Performance: N/A.
- Localization/RTL: N/A.
- Analytics: Assert correct event emission exactly once per real transition.
- Tests: This task IS the tests.
- Documentation: Test docstrings.
- Dependencies: Tasks 01–04.
- Do Not Change: N/A.
- Expected Result: All tests pass.
- Definition of Done: 100% of §27 covered and green; duplicate-delivery test marked CI-blocking.

## 30. Definition of Done
`POST /api/v1/billing/webhooks/play` live, signature-verified, idempotent on `provider_event_id` at the DB layer, drives only exact legal state transitions, delegates capacity-driven disabling to B-07, all tests green with the duplicate-delivery test as a non-bypassable CI gate.

## 31. Final Verification Checklist
- [ ] Duplicate `provider_event_id` delivery verified as a safe no-op (state changes exactly once)
- [ ] Invalid signature rejected before any processing
- [ ] Exhaustive legal-transition table matches PRD §1.17 diagram exactly
- [ ] Illegal transitions verified unreachable
- [ ] Capacity-reducing transitions delegate to B-07, no local disable logic
- [ ] No raw payload PII logged beyond necessary references
- [ ] OpenAPI docs reflect webhook-signature auth model
