# K-07 — Habit Reminder Deep Link & Quiet-Hours Landing

## 1. Feature Context
NoorHeroes KMP app. Owns the deep-link destinations for streak-risk and habit-reminder push notifications; suppression logic itself belongs to the shared Notification Service (A.12).

## 2. Parent Feature
A.7 Habit Tracker — KMP App (Android/iOS)

## 3. Sub-feature
K-07 Habit Reminder Deep Link & Quiet-Hours Landing

## 4. Objective
Implement deep-link routing for `noorheroes://habits`, `noorheroes://habits/garden`, `noorheroes://habits/streak-risk`, landing notification taps on the correct Habit Tracker screens (FR-15 cross-reference).

## 5. Business Requirements
- Notification-tap deep links land on the correct destination screen (Habit Builder, Noor Garden, or a streak-risk-focused view).
- Quiet-hours/bedtime-window suppression is enforced **server-side by the Notification Service** — this sub-feature must not duplicate that suppression logic client-side (PRD §6.9).

## 6. Existing Architecture
Uses the project's custom `Navigator`/`Route`/`NavigationAction` pattern (`core-navigation`) for deep-link resolution — reuse the existing deep-link dispatch mechanism already established for other features (e.g., A.4 Bedtime's `noorheroes://bedtime` handling) as the reference pattern, rather than building a parallel deep-link parser.

## 7. Existing Code to Reuse
- `core-navigation` deep-link resolver/dispatcher (reused across all features)
- Existing push-notification landing infrastructure owned by A.12 Notifications

## 8. Files to Create
- `feature-habits/src/commonMain/kotlin/.../navigation/HabitDeepLinkHandler.kt`
- `feature-habits/src/commonTest/kotlin/.../HabitDeepLinkRoutingTest.kt`

## 9. Files to Modify
- `core-navigation` deep-link registry — register the three `noorheroes://habits*` patterns
- A.12's notification-tap handler — route Habit-Tracker-owned notification categories to `HabitDeepLinkHandler`

## 10. Backend Requirements
None directly; consumes notification payloads dispatched by the existing shared Notification Service (A.12 backend, not part of this feature's backend scope).

## 11. KMP Requirements
- `noorheroes://habits` → Habit Builder (K-01)
- `noorheroes://habits/garden` → Noor Garden Personal (K-05)
- `noorheroes://habits/streak-risk` → Streak State Detail / AtRisk-focused view (K-04)
- No client-side quiet-hours suppression logic — trust the server-side Notification Service entirely for delivery timing.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
None directly (notification dispatch owned by A.12's backend); this sub-feature only owns client-side routing of already-delivered notification taps.

## 14. Database Requirements (Local)
None.

## 15. Validation
Unit test asserting each of the three deep-link patterns routes to the correct destination screen.

## 16. Authentication
N/A (routing layer only; underlying screens enforce their own auth per K-01/K-04/K-05).

## 17. Authorization
N/A.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Deep link received with an unknown/malformed path | Fall back to Habit Builder (safe default), not a crash or blank screen |
| Target child/session no longer valid | Route to standard auth/session-recovery flow (existing app-wide pattern), not a Habit-Tracker-specific error |

## 19. Offline First
N/A (navigation routing only).

## 20. Local Data
N/A.

## 21. Localization
N/A (routing logic, no user-facing strings).

## 22. RTL
N/A.

## 23. Analytics
Notification-tap-to-landing funnel tracking (coordinates with A.12's existing notification analytics; no new Habit-Tracker-specific event beyond what the destination screens themselves already fire, e.g. `habit_builder_viewed`).

## 24. Performance
Deep-link resolution must be near-instant; no blocking network calls in the routing path itself.

## 25. Security
Deep-link handler validates the resolved route against the current authenticated session before navigating (standard app-wide deep-link security pattern, reused not reinvented).

## 26. Library Requirements
`core-navigation`, Koin.

## 27. Testing
Unit tests for all three deep-link patterns; integration test for malformed-path fallback behavior.

## 28. Documentation
KDoc explicitly noting quiet-hours suppression is intentionally NOT implemented here — it is owned by A.12's Notification Service — to prevent future duplicate/conflicting suppression logic.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Register Deep-Link Patterns**
- Objective: Wire the three `noorheroes://habits*` patterns into `core-navigation`'s registry.
- Files to Modify: `core-navigation` deep-link registry.
- Definition of Done: patterns registered and resolvable.

**Task 02 — Implement `HabitDeepLinkHandler`**
- Files to Create: `HabitDeepLinkHandler.kt`
- Implementation Details: routes per §11; safe fallback to Habit Builder on malformed input.
- Tests: mandatory routing tests for all three patterns plus fallback case.
- Definition of Done: all tests pass.

**Task 03 — Wire A.12's Notification-Tap Handler**
- Files to Modify: A.12 notification-tap handler.
- Do Not Change: do not implement quiet-hours suppression logic in this feature's code.
- Definition of Done: Habit-Tracker-owned notification categories correctly dispatch to `HabitDeepLinkHandler`.

**Task 04 — Final Code Review**
- Expected Result: PR merge-ready.

## 30. Definition of Done
All three deep-link patterns correctly route to their destination screens with safe fallback behavior; no client-side quiet-hours logic duplicated.

## 31. Final Verification Checklist
- [ ] `noorheroes://habits`, `/garden`, `/streak-risk` all route correctly
- [ ] Malformed/unknown deep link falls back to Habit Builder, not a crash
- [ ] No client-side quiet-hours suppression logic implemented
- [ ] Session validation applied before navigation
- [ ] Tests passing for all patterns
