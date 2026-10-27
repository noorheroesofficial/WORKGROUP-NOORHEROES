# K-03 — In-App Notification Banner Component

## 1. Feature Context
Part of Feature B.17 — Notifications (Child-Facing). In-app (non-push) notifications exist for some triggers (e.g., "Tomorrow's episode is ready") and surface within the app's own UI rather than as a device push, but still pass through the same policy engine for consent/eligibility purposes (FR-13).

## 2. Parent Feature
B.17 Notifications (Child-Facing) — KMP App (Android/iOS)

## 3. Sub-feature
K-03 In-App Notification Banner Component

## 4. Objective
Implement `InAppNotificationBanner`, a reusable, dismissible Compose component embedded on Home and other relevant feature screens, with per-trigger-instance dismissal persistence.

## 5. Business Requirements
- A lightweight, dismissible card-style banner (consistent with Home's card-based widget language, A.2 §2.1) rather than a disruptive modal interrupt — feels like a natural part of the Home/feature surface (PRD §2.1).
- A dismissed banner for a specific trigger instance does not reappear even after navigating away and back (PRD §6.10).
- In-app notifications still pass through the same policy engine for consent/eligibility purposes as push notifications (FR-13).

## 6. Existing Architecture
- Lives in `:core:notifications`/`:core:design-system` per PRD §6.1–6.2 (`InAppNotificationBanner` is a reusable Composable embedded on Home and other relevant screens, not a dedicated full feature screen).
- Follows Home's card component pattern (A.2) for visual consistency — reuse existing card primitives from `:core:design-system` rather than building a new card style.
- Follows `CORE_DESIGNSYSTEM_INSTRUCTIONS.md` token usage for spacing/color/typography.

## 7. Existing Code to Reuse
- Home's existing card-based widget components (A.2).
- `:core:design-system` design tokens and dismissible-card primitives (if any already exist).

## 8. Files to Create
- `core-notifications/src/commonMain/kotlin/.../banner/InAppNotificationBanner.kt` — Composable.
- `core-notifications/src/commonMain/kotlin/.../banner/InAppNotificationRepository.kt` — fetches eligible in-app notifications, tracks dismissal state.
- `core-notifications/src/commonMain/kotlin/.../banner/BannerDismissalStore.kt` — persists per-trigger-instance dismissal.
- `core-notifications/src/commonTest/kotlin/.../banner/InAppNotificationBannerTest.kt` (UI test).

## 9. Files to Modify
- Home screen composable (A.2) — embed `InAppNotificationBanner` in its content area.

## 10. Backend Requirements
Consumes B-09's `GET /v1/notifications/in-app` endpoint, which returns the authenticated child's currently-eligible, already-policy-approved, already-rendered in-app-class notification intents (FR-13).

## 11. KMP Requirements
- Render dismissible card-style banner on Home/relevant feature screens for eligible in-app-only triggers.
- Persist per-trigger-instance dismissal (a dismissed banner for a specific trigger instance does not reappear even after navigating away and back) — this is the sub-feature's mandatory, PRD-specified behavior (PRD §7 Android prompt item 4).
- Navigate to relevant destination on banner tap.
- Handle empty state (no eligible in-app notification — banner simply does not render, no placeholder).
- Support localization (EN/HI/AR/UR) and RTL layout.
- Prevent unnecessary recomposition on unrelated Home-screen state changes (stable/immutable state modeling for the banner's own state).

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
Consumes B-09's `GET /v1/notifications/in-app` exactly as documented in that blueprint's §13: `{ "notifications": [ { "instance_id", "type", "rendered_copy", "destination", "expires_at" } ] }`.

## 14. Database Requirements
Local dismissal-state persistence via `:core:datastore`, keyed by trigger-instance id, per `CORE_DATASTORE_INSTRUCTIONS.md`.

## 15. Validation
Dismissal state must be keyed uniquely per trigger instance (not per notification type generally), so a new instance of the same type (e.g., tomorrow's "episode ready" banner, distinct from today's) is not incorrectly suppressed by yesterday's dismissal.

## 16. Authentication
Uses the existing authenticated child/parent session via `:core:network`.

## 17. Authorization
N/A client-side.

## 18. Error Handling
| Scenario | System Behavior |
|---|---|
| No eligible in-app notification | Banner does not render (clean empty state, not a placeholder) |
| Fetch failure | Banner silently does not render rather than showing an error state (non-critical, non-blocking UI element) |
| Dismissal-state write failure | Retried locally; worst case the banner reappears once more rather than crashing |

## 19. Offline First
Banner content reflects last-synced local state if offline; dismissal persists locally regardless of connectivity.

## 20. Local Data
Dismissal state persisted locally via `:core:datastore`; survives app restart.

## 21. Localization
All banner copy sourced from localized string resources (EN/HI/AR/UR); no hardcoded text (PRD §19).

## 22. RTL
Banner layout mirrors correctly for AR/UR, consistent with the provided Figma RTL mockup (PRD §2.5).

## 23. Analytics
`in_app_notification_banner_shown`, `in_app_notification_banner_tapped`.

## 24. Performance
Banner must not trigger unnecessary recomposition of the surrounding Home screen; use stable/immutable data classes for its state per `CORE_UI_INSTRUCTIONS.md` Compose performance conventions.

## 25. Security
No billing/sensitive-analytics content in banner copy — governed by the same B-04 template blocklist as push notifications for any in-app-class child-facing template.

## 26. Library Requirements
Kotlin Multiplatform, Jetpack Compose, Koin, `:core:datastore`, kotlin.test/JUnit, Compose UI testing.

## 27. Testing
- UI test: **mandatory** — dismissal persistence (a dismissed banner for a specific trigger instance does not reappear after navigating away and back) (PRD §7 Android prompt item 4).
- Unit: empty-state (no eligible notification) renders nothing.
- UI test: RTL rendering correctness for AR/UR.
- Unit: recomposition-stability test (banner does not recompose on unrelated Home state changes).

## 28. Documentation
Document the dismissal-state keying strategy (per trigger-instance, not per type) in `BannerDismissalStore.kt`'s KDoc.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement InAppNotificationRepository**
- Files to Create: `InAppNotificationRepository.kt`.
- Implementation Details: fetch eligible in-app-class notifications for the current child via B-09's `GET /v1/notifications/in-app`.
- Tests: unit tests with fake data source.

**Task 02 — Implement BannerDismissalStore**
- Files to Create: `BannerDismissalStore.kt`.
- Why Required: PRD §7 Android prompt item 4, mandatory dismissal-persistence behavior.
- Implementation Details: `:core:datastore`-backed, keyed by trigger-instance id.
- Tests: mandatory dismissal-persistence UI test.

**Task 03 — Implement InAppNotificationBanner Composable**
- Files to Create: `InAppNotificationBanner.kt`.
- Existing Files to Reuse: Home's card component pattern (A.2), `:core:design-system` tokens.
- Localization/RTL: per §21/§22.
- Tests: RTL rendering test.

**Task 04 — Embed Banner into Home Screen**
- Files to Modify: Home screen composable (A.2).
- Definition of Done: banner renders correctly within Home's existing layout, non-intrusively.

**Task 05 — Implement Recomposition Stability**
- Files to Modify: `InAppNotificationBanner.kt`.
- Performance: stable/immutable state modeling.
- Tests: recomposition-count test.

**Task 06 — Add Analytics Instrumentation**
- Analytics: `in_app_notification_banner_shown`/`_tapped`.
- Tests: event-firing verification.

**Task 07 — Write Full Test Suite & Documentation**
- Tests: per §27.
- Documentation: per §28.

## 30. Definition of Done
- Banner renders correctly for eligible in-app notifications and correctly withholds rendering when none are eligible.
- Dismissal persists per-trigger-instance, verified by the mandatory UI test.
- Fully localized and RTL-correct.

## 31. Final Verification Checklist
- [ ] Banner renders only when an eligible in-app notification exists
- [ ] Dismissal persists per-trigger-instance across navigation, verified by UI test
- [ ] Tapping the banner navigates to the correct destination
- [ ] Banner is fully localized across EN/HI/AR/UR with correct RTL mirroring
- [ ] No unnecessary recomposition triggered on unrelated Home-screen state changes
- [ ] Analytics events fire correctly on show/tap
- [ ] Full test suite passes
