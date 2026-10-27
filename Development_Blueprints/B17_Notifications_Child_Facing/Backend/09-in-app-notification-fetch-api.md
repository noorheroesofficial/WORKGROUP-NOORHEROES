# B-09 — In-App Notification Fetch API

## 1. Feature Context
Part of Feature B.17 — Notifications (Child-Facing). Gap identified during blueprint audit: in-app (non-push) notifications exist for some triggers (e.g., "Tomorrow's episode is ready") and surface within the app's own UI rather than as a device push, but still pass through the same policy engine for consent/eligibility purposes (FR-13). Unlike push, which is delivered to the device via FCM, an in-app banner has no delivery mechanism of its own — the client must be able to **pull** currently-eligible in-app notifications when a relevant screen (e.g., Home) loads. This read endpoint was implied by FR-13 and Screen Inventory §1.18 item 6 but not enumerated in the original API List (§3.4) or Service Breakdown (§3.3); it is required for K-03 (In-App Notification Banner) to function and is added here as B-09.

## 2. Parent Feature
B.17 Notifications (Child-Facing) — Backend (FastAPI)

## 3. Sub-feature
B-09 In-App Notification Fetch API

## 4. Objective
Implement `GET /v1/notifications/in-app` returning the set of currently-eligible, policy-approved, unexpired, undismissed in-app-class notification intents for the authenticated child, so K-03's `InAppNotificationBanner` can render them without requiring a push-style delivery mechanism.

## 5. Business Requirements
- In-app notifications pass through the same policy engine for consent/eligibility purposes as push notifications (FR-13) — this endpoint must only return intents that have already passed B-03's Policy Engine evaluation (i.e., intents with `status='sent'` and `notification_type` tagged as an in-app-eligible class), never re-deriving eligibility independently at fetch time.
- Reflects the same "no billing/sensitive analytics" content-safety guarantee as push copy, since the returned copy is the same B-04-governed, rendered template output.
- A dismissed banner for a specific trigger instance does not reappear (K-03's client-side dismissal), but the server does not need to track dismissal state itself — dismissal is a client-local concern (per K-03 §20 Local Data); this endpoint simply returns all currently-eligible instances and lets the client filter out ones it has already dismissed.

## 6. Existing Architecture
- Extends `src/noorheroes/modules/notifications/` (`FAST-API-INSTRUCTIONS.md` §5.8), reusing the existing `NotificationRouter`/`NotificationResponse` schema shape rather than inventing a parallel response format.
- Reads from `notification_intents`/`notification_deliveries` (B-02/B-05) — this endpoint is a read-only projection over data already produced by the existing pipeline; it creates no new intents and performs no new policy evaluation.

## 7. Existing Code to Reuse
- `NotificationResponse` schema (existing, per `FAST-API-INSTRUCTIONS.md` §5.8) — extend rather than duplicate.
- `get_current_child` dependency.
- B-02's `NotificationIntentRepository`, B-05's `NotificationDelivery` model.

## 8. Files to Create
- `src/noorheroes/modules/notifications/in_app_fetch_service.py` — `InAppNotificationFetchService(BaseService)`.
- Extend `schemas.py`: `InAppNotificationListResponse`.
- Extend `api.py`: `GET /v1/notifications/in-app`.
- `tests/modules/notifications/test_in_app_fetch_service.py`.

## 9. Files to Modify
None outside this module.

## 10. Backend Requirements
- `InAppNotificationFetchService.get_eligible(child_id)` queries `notification_intents` joined to `notification_deliveries` for `status='sent'`, `notification_type IN (in-app-eligible types)`, `target_child_id=child_id`, not yet expired (a reasonable TTL per type, e.g., "tomorrow's episode is ready" expires once tomorrow's episode airs or is opened).
- Returns already-rendered copy (from B-04's template output persisted at send time — no re-rendering at fetch time, ensuring the client always sees exactly what was policy-approved and rendered, not a live re-render that could drift).
- No new policy evaluation occurs in this endpoint — it is strictly a read projection over already-`sent` intents.

## 11. KMP Requirements
`InAppNotificationRepository` (K-03) calls this endpoint to populate `InAppNotificationBanner`.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract

**Required API — User API**
- **HTTP Method:** GET
- **Endpoint:** `/v1/notifications/in-app`
- **Response 200:** `{ "notifications": [ { "instance_id": "uuid", "type": "new_content", "rendered_copy": "Tomorrow's episode is ready!", "destination": "story_detail", "expires_at": "iso8601" } ] }`
- **Authentication:** Bearer (child-mode session)
- **Authorization:** returns only intents targeting the authenticated child
- **Validation:** N/A (read-only, no request body)
- **Error Responses:** `401` unauthorized

## 14. Database Requirements
Read-only query over existing `notification_intents`/`notification_deliveries` (B-02/B-05); no new tables. If per-type expiry isn't already derivable from existing columns, add `notification_intents.expires_at` (nullable) via a small migration.

## 15. Validation
Only returns intents belonging to the authenticated child; never another child's in-app notifications, even on a shared device (consistent with B-01's binding-exclusivity principle, applied here at the session level).

## 16. Authentication
Bearer JWT via `get_current_child`.

## 17. Authorization
Scoped strictly to the authenticated child's own `target_child_id`.

## 18. Error Handling
| Scenario | System Behavior |
|---|---|
| No eligible in-app notifications | `200` with an empty `notifications` array, not an error |
| Unauthorized/expired session | `401` |
| Database failure | `500`, client falls back to K-03's "banner does not render" behavior |

## 19. Offline First
N/A (backend); client caches last-fetched result locally per K-03 §19/§20.

## 20. Local Data
N/A (backend); dismissal filtering happens client-side per K-03.

## 21. Localization
Returns pre-rendered, already-localized copy per the child's current locale (same B-04 rendering pipeline as push).

## 22. RTL
N/A (backend); text direction already correct from B-04's rendered output.

## 23. Analytics
None directly (K-03 emits `in_app_notification_banner_shown`/`_tapped` client-side); this endpoint is a passive data source.

## 24. Performance
Lightweight, indexed query (`target_child_id`, `status`, `expires_at`); cacheable for a short TTL since Home-screen loads may call this frequently.

## 25. Security
Strictly scoped to the authenticated child; never returns another family member's or another child's in-app notifications.

## 26. Library Requirements
FastAPI, SQLAlchemy 2.0 async, Pydantic v2, pytest.

## 27. Testing
- Unit: query correctly filters by child, status, and non-expired.
- Integration: full flow — intent created (B-02) → policy-approved (B-03) → rendered (B-04) → fetched via this endpoint → correct shape returned.
- Integration: a notification intended for Child A is never returned when Child B's session calls this endpoint on a shared device.

## 28. Documentation
OpenAPI docs for the new endpoint; note in `FAST-API-INSTRUCTIONS.md`-style module documentation that this is a read-only projection, never a policy re-evaluation point.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Add expires_at Column (if not already derivable)**
- Files to Create: migration (only if needed after confirming existing schema).
- Definition of Done: per-type expiry is queryable.

**Task 02 — Implement InAppNotificationFetchService**
- Files to Create: `in_app_fetch_service.py`.
- Implementation Details: query per §10, reuse rendered copy from delivery record.
- Tests: unit tests for filtering logic.

**Task 03 — Implement GET /v1/notifications/in-app Endpoint**
- Files to Modify: `api.py`, `schemas.py`.
- Authentication/Authorization: `get_current_child`, strict child-scoping.
- Tests: endpoint integration tests, including the cross-child-isolation test.

**Task 04 — Wire K-03's InAppNotificationRepository to This Endpoint**
- Files to Modify (KMP side, coordinate with K-03): `InAppNotificationRepository.kt`.
- Definition of Done: K-03's blueprint §13 reference is now concrete rather than an open coordination item.

**Task 05 — Write Full Test Suite & Documentation**
- Tests: per §27.
- Documentation: per §28.

## 30. Definition of Done
- Endpoint returns only the authenticated child's currently-eligible, already-policy-approved, already-rendered in-app notifications.
- No new policy evaluation logic duplicated in this endpoint.
- K-03 can now be implemented against a concrete, documented contract.

## 31. Final Verification Checklist
- [ ] Endpoint returns only in-app-eligible, `status='sent'` intents for the authenticated child
- [ ] No re-evaluation of policy occurs at fetch time (strictly a read projection)
- [ ] Cross-child isolation verified on a shared-device scenario
- [ ] Expired in-app notifications are excluded from the response
- [ ] Returned copy exactly matches what was policy-approved and rendered at send time
- [ ] Full test suite passes; OpenAPI documentation updated
