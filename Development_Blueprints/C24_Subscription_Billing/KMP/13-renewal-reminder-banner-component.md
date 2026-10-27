# K-13 — Renewal Reminder Banner Component

## 1. Feature Context
An in-app parent-facing banner surfaced on the Parent Dashboard/Notifications area 7 days and 24 hours before an annual plan's renewal date — distinct from K-10, which handles the push-notification tap/deep-link; this component owns the banner's in-app rendering and dismiss/tap behavior.

## 2. Parent Feature
Feature C.24 — Subscription & Billing

## 3. Sub-feature
2.13 Renewal Reminder Banner Component (ID: **K-13**)

## 4. Objective
Build a `RenewalReminderBanner` composable, driven by the parent's subscription state (`renewal_date` proximity), shown on the Parent Dashboard 7 days and 24 hours before an annual plan's renewal, tapping through to the Subscription landing screen.

## 5. Business Requirements
- FR-4: "Renewal reminder → annual plans notify 7 days and 24 hours before renewal."
- §1.18 Screen 16: Renewal Reminder Banner (7-day/24-hour, parent-facing) — Component, Entry: Parent Dashboard/Notifications, Exit: Subscription landing.
- §1.10 Edge Case #7: this is a parent-facing notification type, unaffected by the child's own bedtime/quiet-hours configuration — governed by the Parent Area's own notification preferences (C.25), not C.23.

## 6. Existing Architecture
Rendered within C.20's Parent Dashboard landing screen (a banner slot/region), sourced from K-01's `SubscriptionUiState.renewalDate` — this component does not own dashboard layout, only the banner content and its display-trigger logic.

## 7. Existing Code to Reuse
- C.20's Parent Dashboard landing screen banner-slot pattern (confirm exact insertion point against C.20's implementation before wiring — Do Not Guess).
- K-01's `SubscriptionViewModel`/`SubscriptionUiState` for `renewal_date` and `plan` (annual vs. monthly) data.
- `:core:design-system` banner/alert component.

## 8. Files to Create
- `feature/subscription/ui/components/RenewalReminderBanner.kt`
- `feature/subscription/viewmodel/RenewalReminderViewModel.kt`
- `test/feature/subscription/RenewalReminderBannerTest.kt`

## 9. Files to Modify
- C.20's Parent Dashboard landing screen — add the banner slot rendering `RenewalReminderBanner` when applicable (coordinate with C.20's own blueprint for the exact slot/composition point)

## 10. KMP Requirements
- `RenewalReminderViewModel` derives banner visibility from `renewal_date` (only for annual-plan subscribers): show at the 7-day mark and again at the 24-hour mark; each window shown once per renewal cycle (dismissible, does not reappear after dismissal within the same window, but does reappear for the next window/next renewal cycle).
- Banner copy distinguishes the 7-day vs. 24-hour variant ("Your plan renews in 7 days" vs. "Your plan renews tomorrow").
- Tap navigates to Subscription landing (K-01); dismiss (×) hides the banner for the current window only.
- Explicitly unaffected by any child-bedtime/quiet-hours configuration (Edge Case #7) — this banner's visibility logic must not import or check C.23's restriction-engine state at all.
- Never rendered in any child-mode-reachable view (Parent Dashboard is already parent-session-gated per C.20, so this is inherited, not a new guarantee to build).

## 11. Required API
None new directly — sourced from K-01's already-fetched `GET /v1/parent/subscription` (B-05) `renewal_date`/`plan` fields.

## 12. Offline First
Renders from K-01's last-cached subscription state; dismissal state persisted locally (survives offline/online transitions within the same renewal window).

## 13. Local Data
Local persistence of per-window dismissal state (e.g., `:core:datastore` key `renewal_banner_dismissed_{subscription_id}_{window}`), cleared/reset at the start of each new renewal cycle.

## 14. Localization
Banner copy for both the 7-day and 24-hour variants fully localized EN/HI/AR/UR.

## 15. RTL
Banner layout, dismiss icon position, and text alignment mirror correctly in RTL.

## 16. Analytics
`renewal_reminder_shown` per §1.19, fired on banner presentation (with window — 7-day/24-hour — as a parameter).

## 17. Performance
Pure derived-state computation from already-fetched data; no additional network call.

## 18. Security
No new security surface; inherits C.20's existing parent-session-only gate on the Dashboard it's embedded in.

## 19. Testing
- Unit test: banner visibility correctly triggers at the 7-day and 24-hour marks for annual-plan subscribers only (monthly-plan subscribers never see this banner).
- Unit test: dismissal hides the banner for the current window only, reappears for the next window/cycle.
- Unit test: banner visibility logic has zero dependency on C.23's restriction-engine/bedtime state (Edge Case #7 — explicit isolation test).
- UI test: tap navigates to Subscription landing.

## 20. AI Coding Agent Implementation Steps

**Task 01 — Implement `RenewalReminderViewModel`**
Objective: derive 7-day/24-hour visibility windows and dismissal state from subscription data. Files to Create: `RenewalReminderViewModel.kt`. Dependencies: K-01.

**Task 02 — Implement `RenewalReminderBanner` Composable**
Objective: banner UI with both copy variants, tap/dismiss handling. Files to Create: `RenewalReminderBanner.kt`. Dependencies: Task 01.

**Task 03 — Implement Local Dismissal Persistence**
Objective: per-window dismissal state survives app restarts, resets each renewal cycle. Files to Modify: `RenewalReminderViewModel.kt`. Dependencies: Task 01.

**Task 04 — Wire into C.20's Parent Dashboard**
Objective: insert the banner slot into the Dashboard landing screen (coordinate with C.20's blueprint). Files to Modify: C.20's Dashboard landing screen. Dependencies: Task 02.

**Task 05 — Add Analytics & Test Suite**
Objective: `renewal_reminder_shown`, coverage per §19, including the explicit C.23-isolation test. Dependencies: Tasks 01–04.

## 21. Final Verification Checklist
- [ ] Banner shows only for annual-plan subscribers at 7-day and 24-hour marks
- [ ] Dismissal scoped to current window only, reappears next cycle
- [ ] Zero dependency on C.23 bedtime/quiet-hours state (Edge Case #7 verified)
- [ ] Tap routes correctly to Subscription landing
- [ ] RTL layout verified

## 22. Definition of Done
`RenewalReminderBanner` correctly surfaces on the Parent Dashboard at the 7-day and 24-hour marks for annual-plan subscribers, dismissible per-window, fully independent of child-bedtime configuration, routing taps into Subscription landing.
