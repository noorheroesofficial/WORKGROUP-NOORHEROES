# B-06 — Deep Link Resolution API

## 1. Feature Context
Part of Feature B.17 — Notifications (Child-Facing). Deep links validate session, child, content availability, and parent gate — tapping any notification re-runs the exact same checks normal in-app navigation would, never granting a shortcut past any of them (FR-5).

## 2. Parent Feature
B.17 Notifications (Child-Facing) — Backend (FastAPI)

## 3. Sub-feature
B-06 Deep Link Resolution API

## 4. Objective
Implement `GET /v1/notifications/resolve`, re-running full session/child/content/parent-gate validation on every notification open, and correctly signaling a re-route through "Who Is Learning" when the notification's intended child no longer matches the device's currently active session.

## 5. Business Requirements
- Deep links validate session, child, content availability, and parent gate on every open (FR-5).
- A notification originally intended for Child A opened while Child B's session is active must correctly re-route through Who Is Learning rather than resolving into Child A's content under Child B's session (PRD §5 backend prompt item 5, Edge Case 2).
- Content withdrawn after a promoting notification was already sent must be gracefully handled (not a crash), consistent with the platform's withdrawn-content UX pattern (Edge Case 4, A.3/A.6).
- Tapped while offline requires a clear "reconnect to open this" client state — this API's contract must support a client that has no connectivity by design (never attempting a client-only/local resolution) (Edge Case 5).

## 6. Existing Architecture
- Extends `src/noorheroes/modules/notifications/` (`FAST-API-INSTRUCTIONS.md` §5.8).
- Reuses A.1's session-validation and Lock/Parent-Gate primitives (`get_current_child`/`get_current_parent`, and any existing `requires_lock_gate` check used elsewhere in A.1/B.16) rather than reimplementing gate logic.
- Reuses each destination feature's own content-availability check (A.3/A.4/A.5/A.6/A.7/A.11) via their existing service-layer "is this content currently available" methods, rather than duplicating availability logic in this module.

## 7. Existing Code to Reuse
- `get_current_child`, `get_current_parent` from `src/noorheroes/core/deps.py`.
- A.1/B.16's Lock Gate check primitive.
- Destination-feature content-availability service methods (A.3/A.4/A.5/A.6/A.7/A.11).

## 8. Files to Create
- `src/noorheroes/modules/notifications/deep_link_service.py` — `DeepLinkResolutionService`.
- Extend `schemas.py`: `DeepLinkResolveResponse`.
- Extend `api.py`: `GET /v1/notifications/resolve`.
- `tests/modules/notifications/test_deep_link_service.py`.

## 9. Files to Modify
- `src/noorheroes/modules/notifications/delivery_adapter.py` (B-05) — call `mark_opened(delivery_id)` on successful resolution.

## 10. Backend Requirements
- Given `deep_link_token`, look up the originating `notification_deliveries`/`notification_intents` row to determine intended `target_child_id` and `destination`.
- Re-validate: (1) session validity (current Bearer token), (2) intended child matches the currently active session's child — if not, return a re-route signal to Who Is Learning rather than the original destination, (3) content availability via the destination feature's own current-state check, (4) any applicable parent-gate requirement for that destination.
- Return `{ "valid": true, "destination": "..." }` on full pass, or `{ "valid": false, "reason": "content_unavailable|session_expired|requires_lock_gate|child_mismatch", "fallback_destination": "..." }` on any failed check.
- On successful resolution, call `DeliveryAdapter.mark_opened(delivery_id)` to record `notification_deliveries.opened_at`.

## 11. KMP Requirements
`DeepLinkResolutionHandler` (K-02) calls this endpoint on every notification tap before any navigation occurs.

## 12. NextJS Requirements
Not applicable directly.

## 13. API Contract

**Required API — User API**
- **HTTP Method:** GET
- **Endpoint:** `/v1/notifications/resolve?deep_link_token=...`
- **Response 200 (valid):** `{ "valid": true, "destination": "habit_builder", "params": {...} }`
- **Response 200 (invalid):** `{ "valid": false, "reason": "content_unavailable|session_expired|requires_lock_gate|child_mismatch", "fallback_destination": "who_is_learning|home|..." }`
- **Authentication:** Bearer (whichever session is currently active on the device)
- **Authorization:** N/A beyond the child-match check itself (which is the core business logic, not a rejection)
- **Validation:** `deep_link_token` must resolve to a known delivery record
- **Error Responses:** `401` no/expired session, `404` unknown/expired deep-link token

## 14. Database Requirements
Reads `notification_deliveries`, `notification_intents` (for intended `target_child_id`/`destination`); no new tables.

## 15. Validation
`deep_link_token` must map to an existing delivery record; unknown tokens return `404`, not a silent generic fallback (to aid debugging/monitoring, while the client still shows a graceful UX state).

## 16. Authentication
Bearer JWT via whichever session (parent or child) is currently active on the device.

## 17. Authorization
The core check is the child-match comparison itself (§10 item 2) — this is business logic producing a re-route signal, not a `403`.

## 18. Error Handling
| Scenario | System Behavior |
|---|---|
| Session expired/invalid | `reason: session_expired`, `fallback_destination` provided |
| Intended child ≠ currently active session's child | `reason: child_mismatch`, `fallback_destination: who_is_learning` (Edge Case 2, mandatory test) |
| Content withdrawn since send | `reason: content_unavailable`, `fallback_destination` to a suggested alternative, consistent with A.3/A.6 withdrawn-content pattern (Edge Case 4) |
| Parent gate required for destination | `reason: requires_lock_gate` |
| Unknown/expired deep-link token | `404 Not Found` |

## 19. Offline First
This API requires connectivity by design (server-side validation is mandatory); the client shows a "reconnect to open this" state on request failure rather than attempting local-only resolution (Edge Case 5, PRD §1.14).

## 20. Local Data
N/A (backend); no server-side caching of resolution results, since results must reflect current state on every call.

## 21. Localization
`fallback_destination`/`reason` are machine-readable keys; client (K-02) owns localized copy for each state.

## 22. RTL
N/A (backend).

## 23. Analytics
`notification_deep_link_resolved`.

## 24. Performance
Resolution must complete quickly (single-digit-second budget) since it blocks a user-facing loading state on the client; avoid N+1 queries across the delivery→intent→destination-availability lookup chain.

## 25. Security
This is the primary defense against a deep-link-based gate bypass — the raw notification payload's destination claim is never trusted; every open re-runs full server-side validation (PRD §12.1, §12.2 Broken Access Control mitigation).

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Pydantic v2, pytest.

## 27. Testing
- Unit: each validation dimension in isolation.
- Integration: notification originally intended for Child A opened while Child B's session is active → assert `child_mismatch` + `who_is_learning` re-route (PRD §5 backend prompt item 5, mandatory).
- Integration: content withdrawn after send → graceful `content_unavailable` response, not a crash.
- Integration: unknown deep-link token → `404`.

## 28. Documentation
OpenAPI docs enumerating every `reason`/`fallback_destination` value and its meaning.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement Deep-Link Token Lookup**
- Files to Create: `deep_link_service.py` (partial).
- Implementation Details: resolve `deep_link_token` → delivery/intent record → intended `target_child_id`/`destination`.
- Error Handling: `404` for unknown tokens.

**Task 02 — Implement Session & Child-Match Validation**
- Objective: The feature's core re-route logic.
- Why Required: PRD §5 backend prompt item 5, mandatory test target.
- Business Rules: FR-5, Edge Case 2.
- Tests: the mandatory child-mismatch → who-is-learning re-route test.

**Task 03 — Implement Content Availability Check**
- Existing Files to Reuse: destination-feature content-availability service methods (A.3/A.4/A.5/A.6/A.7/A.11).
- Tests: withdrawn-content scenario test (Edge Case 4).

**Task 04 — Implement Parent-Gate Check**
- Existing Files to Reuse: A.1/B.16 Lock Gate primitive.
- Tests: unit test for gate-required destinations.

**Task 05 — Implement GET /v1/notifications/resolve Endpoint**
- Files to Modify: `api.py`, `schemas.py`.
- Authentication: Bearer, current active session.
- Error Handling: full response-shape matrix per §18.
- Tests: full endpoint integration tests.

**Task 06 — Wire Open-Receipt Recording**
- Files to Modify: `delivery_adapter.py` (B-05).
- Implementation Details: call `mark_opened(delivery_id)` on successful resolution.
- Tests: integration test verifying `opened_at` is set.

**Task 07 — Add Analytics, Documentation, and Full Test Suite**
- Analytics: `notification_deep_link_resolved`.
- Documentation: per §28.
- Tests: per §27.

## 30. Definition of Done
- Every notification open re-runs full session/child/content/gate validation with no shortcut.
- Child-mismatch scenario correctly re-routes through Who Is Learning.
- Withdrawn content and unknown tokens are handled gracefully, never crashing the client.

## 31. Final Verification Checklist
- [ ] Raw notification payload destination is never trusted without this server round-trip (enforced client-side by K-02, verified here by contract)
- [ ] Session validity re-checked on every resolution
- [ ] Child-mismatch correctly signals re-route to Who Is Learning
- [ ] Content availability re-checked against current state, not send-time state
- [ ] Parent-gate requirement correctly signaled when applicable
- [ ] Unknown/expired deep-link tokens return 404, not a silent fallback
- [ ] Open receipt (`opened_at`) recorded on successful resolution
- [ ] Full test suite passes, including the mandatory child-mismatch re-route test
