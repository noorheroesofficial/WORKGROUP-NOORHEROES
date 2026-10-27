# K-04 — Notification Destination Routing Integration

## 1. Feature Context
Part of Feature B.17 — Notifications (Child-Facing). This feature doesn't itself define new deep-link schemes beyond routing into each destination feature's already-established scheme (PRD §6.8) — this sub-feature is the integration glue ensuring every notification class lands correctly on its owning feature's existing navigation graph.

## 2. Parent Feature
B.17 Notifications (Child-Facing) — KMP App (Android/iOS)

## 3. Sub-feature
K-04 Notification Destination Routing Integration

## 4. Objective
Wire each notification class's resolved destination (from K-02's `DeepLinkResolutionHandler`) into the correct destination feature's existing navigation graph — A.4 Bedtime Player, A.7 Habit Builder, A.11 Rewards Wallet/Achievements, and A.3/A.5/A.6 content detail screens.

## 5. Business Requirements
- Bedtime Story notification tap → A.4 Bedtime Player (PRD Screen Inventory §1.18 item 7).
- Streak-Risk notification tap → A.7 Habit Builder (item 8).
- New Content notification tap → relevant content detail in A.3/A.5/A.6 (item 9).
- Reward/Milestone notification tap → A.11 Rewards Wallet/Achievements (item 10).
- Seasonal notification tap → appropriate seasonal-mode destination (cross-ref C.36 Ramadan Mode where applicable).
- Each destination's own existing deep-link scheme (`noorheroes://habits`, `noorheroes://rewards`, etc.) is reused, never redefined by this feature (PRD §6.8).

## 6. Existing Architecture
- Depends on K-02's `DeepLinkResolutionHandler` for the validated destination string, then hands off to `:core:navigation`'s existing routing graph — this sub-feature adds no new deep-link scheme definitions, only route-mapping/wiring.
- Each destination feature (A.3/A.4/A.5/A.6/A.7/A.11) owns its own screen and error/empty/withdrawn-content states; this sub-feature must not duplicate that logic.

## 7. Existing Code to Reuse
- A.4's Bedtime Player navigation entry point.
- A.7's Habit Builder navigation entry point.
- A.11's Rewards Wallet/Achievements navigation entry point.
- A.3/A.5/A.6's content-detail navigation entry points.
- `:core:navigation`'s existing deep-link-scheme registry.

## 8. Files to Create
- `core-notifications/src/commonMain/kotlin/.../routing/NotificationDestinationRouter.kt` — maps resolved `destination` string → the correct feature's navigation route.
- `core-notifications/src/commonTest/kotlin/.../routing/NotificationDestinationRouterTest.kt`.

## 9. Files to Modify
- `:core:navigation`'s route registry — ensure each destination feature's existing route is reachable from `NotificationDestinationRouter` (registration/wiring only, no new route definitions).

## 10. Backend Requirements
Consumes the `destination` field from B-06's `GET /v1/notifications/resolve` response.

## 11. KMP Requirements
- Route each of the five notification classes to its correct destination feature's existing screen.
- Handle destination-feature-specific error states (e.g., content withdrawn) via K-02's shared fallback rather than a per-destination custom error path.
- Verify each destination's own deep-link scheme is honored without modification.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
No new API — consumes B-06's existing `destination` field.

## 14. Database Requirements
N/A.

## 15. Validation
`NotificationDestinationRouter` must have an exhaustive mapping covering every `destination` value B-06 can return; an unmapped/unknown destination falls back gracefully to Home rather than crashing.

## 16. Authentication
N/A (uses the already-resolved, already-validated session from K-02).

## 17. Authorization
N/A (already enforced upstream by B-06/K-02).

## 18. Error Handling
| Scenario | System Behavior |
|---|---|
| Unknown/unmapped destination value | Graceful fallback to Home, logged as a data/configuration issue for investigation |
| Destination feature's own content unavailable | Handled by K-02's shared `content_unavailable` fallback, not duplicated here |

## 19. Offline First
N/A (routing occurs only after K-02's successful online resolution).

## 20. Local Data
N/A.

## 21. Localization
N/A (routing logic only; destination screens own their own localized content).

## 22. RTL
N/A (routing logic only).

## 23. Analytics
No new events; destination-feature's own screen-view analytics fire naturally once navigation completes.

## 24. Performance
Routing lookup is a simple map/when-based dispatch — O(1), no measurable overhead.

## 25. Security
Routing occurs only after K-02's full validation chain completes — this sub-feature never independently re-interprets a raw, unvalidated destination claim.

## 26. Library Requirements
Kotlin Multiplatform, `:core:navigation`, kotlin.test/JUnit.

## 27. Testing
- Unit: exhaustive mapping test — every possible `destination` value from B-06 routes to the correct feature screen.
- Integration: end-to-end test per destination type — notification tap → resolve → correct screen loads (one test per class: bedtime, streak-risk, new-content, reward, seasonal).
- Regression: this suite re-runs whenever any destination feature's navigation graph changes (PRD §6.10).

## 28. Documentation
Document the full destination-to-route mapping table in `NotificationDestinationRouter.kt`'s KDoc, cross-referencing PRD Screen Inventory §1.18 items 7–10.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement NotificationDestinationRouter Mapping**
- Files to Create: `NotificationDestinationRouter.kt`.
- Existing Files to Reuse: each destination feature's navigation entry point.
- Implementation Details: exhaustive `when`/map over known `destination` values.
- Tests: exhaustive mapping unit test.

**Task 02 — Wire Bedtime Story Routing**
- Existing Files to Reuse: A.4 Bedtime Player entry point.
- Tests: integration test, tap → resolve → Bedtime Player loads.

**Task 03 — Wire Streak-Risk Routing**
- Existing Files to Reuse: A.7 Habit Builder entry point.
- Tests: integration test.

**Task 04 — Wire New Content Routing**
- Existing Files to Reuse: A.3/A.5/A.6 content-detail entry points.
- Tests: integration test per content type.

**Task 05 — Wire Reward/Milestone Routing**
- Existing Files to Reuse: A.11 Rewards Wallet/Achievements entry point.
- Tests: integration test.

**Task 06 — Wire Seasonal Routing**
- Existing Files to Reuse: seasonal-mode destination (cross-ref C.36 Ramadan Mode).
- Tests: integration test.

**Task 07 — Implement Unknown-Destination Fallback**
- Files to Modify: `NotificationDestinationRouter.kt`.
- Error Handling: graceful fallback to Home, logged.
- Tests: unknown-destination fallback test.

**Task 08 — Write Full Regression Suite & Documentation**
- Tests: per §27, wired to re-run on any destination-feature navigation change.
- Documentation: per §28.

## 30. Definition of Done
- All five notification classes route correctly to their owning destination feature's existing screen.
- No new deep-link scheme was introduced; only existing schemes are wired.
- Unknown destinations fall back gracefully.

## 31. Final Verification Checklist
- [ ] Bedtime Story notification correctly opens A.4 Bedtime Player
- [ ] Streak-Risk notification correctly opens A.7 Habit Builder
- [ ] New Content notification correctly opens the relevant A.3/A.5/A.6 content detail
- [ ] Reward/Milestone notification correctly opens A.11 Rewards Wallet/Achievements
- [ ] Seasonal notification correctly opens the appropriate seasonal destination
- [ ] Unknown/unmapped destination falls back to Home rather than crashing
- [ ] No destination feature's own deep-link scheme was modified or duplicated
- [ ] Full integration test suite passes for all five classes
