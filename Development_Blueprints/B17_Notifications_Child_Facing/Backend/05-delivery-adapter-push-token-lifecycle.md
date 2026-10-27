# B-05 — Delivery Adapter & Push Token Lifecycle Management

## 1. Feature Context
Part of Feature B.17 — Notifications (Child-Facing). Final stage of the Notification Flow (PRD §1.17): sends the rendered, policy-passed notification via FCM/email and manages the push-token lifecycle (rotation, invalidation).

## 2. Parent Feature
B.17 Notifications (Child-Facing) — Backend (FastAPI)

## 3. Sub-feature
B-05 Delivery Adapter & Push Token Lifecycle Management

## 4. Objective
Implement the `DeliveryAdapter` that sends policy-approved, rendered notifications via FCM (and email where applicable), records delivery/open receipts, and manages `push_tokens` lifecycle (detect invalid/rotated tokens, exclude dead tokens from future sends).

## 5. Business Requirements
- A push token becomes invalid (app uninstalled, OS-rotated token) — the Lifecycle stage must detect and remove invalid tokens, refresh rotated ones, and avoid repeatedly attempting delivery to a dead token (Edge Case 10, FR-8 architecture).
- Delivery via FCM push or email (FR-2 step 4); a receipt event updates delivery analytics (FR-2 step 5).
- Notification intent-to-delivery latency p95 < 30s for real-time triggers (e.g., streak-risk); scheduled triggers fire within their configured window with minute-level accuracy (PRD §1.8 NFR — the accuracy requirement is owned by B-02's scheduling, latency is this sub-feature's responsibility once policy-approved).

## 6. Existing Architecture
- Extends `src/noorheroes/modules/notifications/` (`FAST-API-INSTRUCTIONS.md` §5.8), building on the existing `NotificationService.dispatch_notification()` method as the integration point for actual send execution — do not create a parallel, duplicate dispatch path.
- Standard FCM SDK integration per infrastructure layer conventions.

## 7. Existing Code to Reuse
- `NotificationService.dispatch_notification()` — extend into the full adapter, or have it delegate to the new `DeliveryAdapter`.
- B-01's `push_tokens` table/repository for lifecycle state updates.

## 8. Files to Create
- `src/noorheroes/modules/notifications/delivery_adapter.py` — `DeliveryAdapter` with `send_fcm()`, `send_email()`.
- `src/noorheroes/modules/notifications/token_lifecycle.py` — `PushTokenLifecycleManager` (`mark_invalid()`, `refresh_rotated()`).
- Extend `models.py`: `NotificationDelivery`.
- `alembic/versions/<rev>_create_notification_delivery_table.py`.
- `tests/modules/notifications/test_delivery_adapter.py`.
- `tests/modules/notifications/test_token_lifecycle.py`.

## 9. Files to Modify
- `src/noorheroes/modules/notifications/service.py` — wire `dispatch_notification()` to delegate to `DeliveryAdapter` for the actual send call.

## 10. Backend Requirements
- `DeliveryAdapter.send_fcm(token, rendered_copy, deep_link_token)` — calls FCM SDK; on success, creates a `notification_deliveries` row with `status='sent'`, `sent_at=now()`.
- On FCM response indicating an invalid/unregistered token, call `PushTokenLifecycleManager.mark_invalid(token_id)`, setting `push_tokens.state='invalid'`; this token is excluded from all future delivery attempts.
- On FCM response indicating a rotated token, call `refresh_rotated(old_token_id, new_fcm_token)`.
- Retry transient (non-terminal) delivery failures with exponential backoff, bounded retry count.
- Batch-send support for large simultaneous fan-outs (e.g., daily-reminder threshold-hour batch from B-02).
- `notification_deliveries.opened_at` updated via the deep-link resolution flow (B-06) calling back into this table on successful open.

## 11. KMP Requirements
Client-side FCM SDK registration/receipt handled by K-01; this backend sub-feature is the send-side counterpart.

## 12. NextJS Requirements
Delivery success/failure/token-health metrics surface via N-04/N-05 (consumed through B-08).

## 13. API Contract
**Internal only — not directly client-callable.** Invoked by the Policy Engine (B-03) on a passing intent.

- **Input:** policy-approved intent + rendered copy (from B-04) + target token(s) (from B-01's active binding).
- **Output:** `notification_deliveries` row created; `notification_intents.status` set to `sent`.

## 14. Database Requirements
- `notification_deliveries`: `delivery_id UUID PK`, `intent_id UUID FK`, `template_id UUID FK`, `recipient_ref VARCHAR`, `status VARCHAR CHECK IN ('sent','delivered','failed','opened')`, `sent_at TIMESTAMPTZ`, `opened_at TIMESTAMPTZ NULL`; index `(recipient_ref, sent_at DESC)`.
- Uses `push_tokens` (B-01) for lifecycle state transitions.

## 15. Validation
- Never attempt delivery to a token with `state='invalid'`.
- Bounded retry count for transient failures (no infinite retry loop).

## 16. Authentication
N/A — internal service.

## 17. Authorization
N/A.

## 18. Error Handling
| Scenario | System Behavior |
|---|---|
| FCM reports token invalid/unregistered | `push_tokens.state` set to `invalid`; no further attempts to this token |
| FCM reports token rotated | New token captured and associated; old token marked `rotated` |
| Transient FCM/network failure | Retried with exponential backoff up to a bounded count, then marked `failed` and logged |
| FCM outage / rate-limit response | Batched, throttled retry; alert if failure-rate spikes (DevOps §10) |
| Content withdrawn after send | Not this sub-feature's concern — handled by B-06's deep-link revalidation on open |

## 19. Offline First
N/A (backend); the OS-level FCM offline queuing behavior is outside this feature's direct control but compatible with it (PRD §1.14).

## 20. Local Data
N/A.

## 21. Localization
Delivers pre-rendered, already-localized copy from B-04; performs no localization itself.

## 22. RTL
N/A (text direction already correct from B-04's rendered output).

## 23. Analytics
`notification_sent`, `notification_delivered`, `push_token_invalidated`, `push_token_refreshed`.

## 24. Performance
p95 intent-to-delivery latency < 30s for real-time triggers (PRD §1.8); batch sends for large simultaneous fan-outs must not create a delivery-queue backlog beyond the latency target.

## 25. Security
No sensitive/billing content passes through this adapter beyond what B-04 already validated; delivery payloads carry only the rendered copy and deep-link token, never raw PII beyond what's already governed.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Firebase Admin SDK (FCM), Celery (batch/retry orchestration), pytest.

## 27. Testing
- Unit: `send_fcm()` success/failure/retry paths.
- Unit: token lifecycle state transitions (`active→invalid`, `active→rotated`).
- Integration: simulated token-invalid FCM response → assert `push_tokens.state='invalid'` and no further delivery attempts target that token (PRD §5 backend prompt item 7, mandatory).
- Load: simulated large simultaneous batch (daily-reminder fan-out) meeting the p95 latency target.

## 28. Documentation
Document the FCM error-code-to-lifecycle-action mapping table in `token_lifecycle.py`.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Create NotificationDelivery Model & Migration**
- Files to Create: `models.py` extension, migration.

**Task 02 — Implement DeliveryAdapter.send_fcm()**
- Files to Create: `delivery_adapter.py`.
- Existing Files to Reuse: `NotificationService.dispatch_notification()` as the delegation point.
- Implementation Details: FCM SDK call, delivery record creation, error-code branching.
- Tests: unit tests for success/failure paths.

**Task 03 — Implement PushTokenLifecycleManager**
- Objective: Detect and act on invalid/rotated tokens.
- Files to Create: `token_lifecycle.py`.
- Why Required: PRD §5 backend prompt item 7, standard FCM lifecycle hygiene.
- Tests: the mandatory simulated-invalid-token test asserting no further delivery attempts to that token.

**Task 04 — Implement Retry with Exponential Backoff**
- Files to Modify: `delivery_adapter.py`.
- Implementation Details: bounded retry count for transient failures.
- Tests: retry-exhaustion test.

**Task 05 — Implement Batch Send Support**
- Files to Modify: `delivery_adapter.py`.
- Performance: batch-send for large simultaneous fan-outs.
- Tests: load test meeting p95 < 30s target.

**Task 06 — Wire Open-Receipt Update from Deep Link Resolution**
- Files to Modify: `delivery_adapter.py` or a shared repository method.
- Implementation Details: expose `mark_opened(delivery_id)` for B-06 to call.
- Tests: integration test for open-receipt update.

**Task 07 — Add Analytics, Monitoring, and Documentation**
- Analytics: per §23.
- Monitoring: alert hook for delivery-failure-rate spikes (DevOps §10).
- Documentation: per §28.

## 30. Definition of Done
- FCM delivery, retry, and token lifecycle management fully implemented and tested.
- Invalid tokens are detected and permanently excluded from future attempts.
- p95 delivery latency target met under simulated batch load.

## 31. Final Verification Checklist
- [ ] `send_fcm()` correctly creates delivery records and handles success/failure branches
- [ ] Invalid/unregistered tokens are marked and never retried
- [ ] Rotated tokens are correctly captured and associated
- [ ] Transient failures retry with bounded exponential backoff
- [ ] Batch sends meet the p95 < 30s latency target under simulated load
- [ ] Open-receipt update path is callable from B-06's deep-link resolution
- [ ] Analytics events fire correctly for sent/delivered/token-invalidated/token-refreshed
- [ ] Full test suite passes
