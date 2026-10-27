# K-05 — Notifications Cross-Platform Analytics Instrumentation

## 1. Feature Context
Part of Feature B.17 — Notifications (Child-Facing). Provides the complete client-side analytics event taxonomy (PRD §1.19) feeding the funnel analysis consumed by B-08/N-04 (`notification_intent_created → notification_sent → notification_delivered → notification_opened → notification_deep_link_resolved`).

## 2. Parent Feature
B.17 Notifications (Child-Facing) — KMP App (Android/iOS)

## 3. Sub-feature
K-05 Notifications Cross-Platform Analytics Instrumentation

## 4. Objective
Implement `NotificationAnalytics`, firing every client-observable event from the PRD's event taxonomy at the correct point in K-01/K-02/K-03/K-04's flows, with correct parameters and no duplicate/missing fires.

## 5. Business Requirements
- Full event list (PRD §1.19): `notification_opened`, `notification_deep_link_resolved`, `notification_deep_link_offline_shown`, `notification_deep_link_content_unavailable_shown`, `notification_binding_activated`, `notification_binding_deactivated`, `push_token_refreshed`, `in_app_notification_banner_shown`, `in_app_notification_banner_tapped` (client-observable subset; `notification_intent_created`, `notification_suppressed`, `notification_sent`, `notification_delivered`, `notification_fatigue_backoff_applied`, `push_token_invalidated` are server-emitted per B-02/B-03/B-05 and out of scope here).
- Events must carry required parameters (`type`, `target_binding` where applicable) consistent with the server-side taxonomy so funnel analysis (PRD §11.2) correctly joins client and server events.

## 6. Existing Architecture
- Uses `:core:analytics` per `CORE_ANALYTICS_INSTRUCTIONS.md` — reuse the existing analytics-event-firing abstraction rather than a new one.
- `NotificationAnalytics` is a thin wrapper coordinating calls from K-01 (binding events), K-02 (deep-link/open events), K-03 (banner events).

## 7. Existing Code to Reuse
- `:core:analytics`'s event-firing interface/abstraction.

## 8. Files to Create
- `core-notifications/src/commonMain/kotlin/.../analytics/NotificationAnalytics.kt`.
- `core-notifications/src/commonTest/kotlin/.../analytics/NotificationAnalyticsTest.kt`.

## 9. Files to Modify
- `DeviceBindingManager.kt` (K-01) — call `NotificationAnalytics.trackBindingActivated()`/`trackBindingDeactivated()`.
- `DeepLinkResolutionHandler.kt` (K-02) — call `trackOpened()`, `trackDeepLinkResolved()`, `trackOfflineShown()`, `trackContentUnavailableShown()`.
- `InAppNotificationBanner.kt` (K-03) — call `trackBannerShown()`, `trackBannerTapped()`.

## 10. Backend Requirements
None directly — this is a pure client-side event-emission sub-feature; server-side event definitions are owned by B-02/B-03/B-05.

## 11. KMP Requirements
- Fire `notification_opened` on successful tap-to-resolve.
- Fire `notification_deep_link_resolved` with `destination` and outcome.
- Fire `notification_deep_link_offline_shown`/`notification_deep_link_content_unavailable_shown` at the corresponding K-02 states.
- Fire `notification_binding_activated`/`notification_binding_deactivated` on K-01's profile switch.
- Fire `in_app_notification_banner_shown`/`in_app_notification_banner_tapped` from K-03.
- Fire `push_token_refreshed` on K-01's token rotation handling.
- Prevent duplicate event firing on rapid repeated taps/navigations (coordinate with K-02's debounce, §18 K-02).

## 12. NextJS Requirements
Not applicable — consumed downstream by N-04's reporting dashboard via the server-side event/delivery tables, not directly by this client module.

## 13. API Contract
No new API — events flow through `:core:analytics`'s existing event-bus/ingestion pipeline.

## 14. Database Requirements
N/A (event-stream only, no local persistence beyond `:core:analytics`'s own buffering/retry, if any).

## 15. Validation
Every event fires with all required parameters populated (no null/missing `type` where required).

## 16. Authentication
N/A (uses `:core:analytics`'s existing authenticated event pipeline).

## 17. Authorization
N/A.

## 18. Error Handling
| Scenario | System Behavior |
|---|---|
| Analytics event-firing call fails (network/buffer full) | Handled by `:core:analytics`'s existing retry/buffering — this module does not implement its own retry logic |
| Duplicate trigger (e.g., rapid double-tap) | Deduped by the debounce already implemented in K-02/K-03; this module does not re-implement dedup, only fires when instructed |

## 19. Offline First
Relies on `:core:analytics`'s existing offline-buffering behavior, if present; not re-implemented here.

## 20. Local Data
N/A.

## 21. Localization
N/A (event names/parameters are not user-facing).

## 22. RTL
N/A.

## 23. Analytics
This entire sub-feature *is* the analytics instrumentation layer; see §11/§5 for the full event list.

## 24. Performance
Event-firing calls must be fire-and-forget (non-blocking) with respect to the UI thread/navigation flow.

## 25. Security
Event parameters must never include billing/sensitive-analytics content in violation of the same content-safety principle applied to notification copy (B-04) — parameters are structural/technical (ids, types, booleans), never free-text copy.

## 26. Library Requirements
Kotlin Multiplatform, `:core:analytics`, kotlin.test/JUnit.

## 27. Testing
- Unit: each event fires exactly once per correct trigger, with correct parameters, verified via a fake `:core:analytics` test double.
- Unit: no duplicate firing on rapid repeated taps (coordinated with K-02/K-03 debounce tests).
- Integration: full funnel trace (open → resolve → destination) produces the expected ordered event sequence.

## 28. Documentation
Document the complete event-to-trigger-point mapping table in `NotificationAnalytics.kt`'s KDoc, cross-referencing PRD §1.19.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement NotificationAnalytics Wrapper**
- Files to Create: `NotificationAnalytics.kt`.
- Existing Files to Reuse: `:core:analytics` event-firing interface.
- Implementation Details: one method per event, each accepting only the documented required parameters.

**Task 02 — Wire Binding Events into K-01**
- Files to Modify: `DeviceBindingManager.kt`.
- Analytics: `notification_binding_activated`/`_deactivated`, `push_token_refreshed`.
- Tests: unit test verifying calls fire on each transition.

**Task 03 — Wire Deep-Link Events into K-02**
- Files to Modify: `DeepLinkResolutionHandler.kt`.
- Analytics: `notification_opened`, `notification_deep_link_resolved`, offline/unavailable variants.
- Tests: unit test per resolution outcome.

**Task 04 — Wire Banner Events into K-03**
- Files to Modify: `InAppNotificationBanner.kt`.
- Analytics: `in_app_notification_banner_shown`/`_tapped`.
- Tests: unit test for show/tap.

**Task 05 — Implement Duplicate-Fire Prevention Coordination**
- Files to Modify: `NotificationAnalytics.kt` (or callers).
- Tests: rapid-repeat-tap dedup test.

**Task 06 — Write Full Test Suite & Documentation**
- Tests: per §27, including the full-funnel integration trace test.
- Documentation: per §28.

## 30. Definition of Done
- Every client-observable event in the PRD's taxonomy fires at the correct point with correct parameters.
- No duplicate or missing events across the K-01/K-02/K-03 flows.
- Full-funnel event trace verified end-to-end.

## 31. Final Verification Checklist
- [ ] All nine client-observable events fire correctly at their designated trigger points
- [ ] Event parameters match the PRD §1.19 taxonomy exactly
- [ ] No duplicate events fire on rapid repeated user actions
- [ ] Full funnel trace (open → resolve → destination) produces the expected event sequence
- [ ] No billing/sensitive-analytics content present in any event parameter
- [ ] Full test suite passes
