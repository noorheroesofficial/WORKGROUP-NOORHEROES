# K-08 — Trial-Cancellation Forced-Selection Screen

> ✅ **UPDATE (resolved via cross-document search of `Feature_C24_Subscription_Billing.md`):** C.24's own Screen Inventory confirms this screen is a **"shared trigger, owned by C.21"** — meaning C.24 surfaces the downgrade/cancellation moment in its own flow and hands off into this KMP screen; C.21 owns the screen and its backend endpoint outright. C.24 additionally documents a **"Deterministic-Fallback Notice (24h, cross-ref C.21)"** — confirming a concrete 24-hour selection window rather than an undefined/immediate one. B-08 has been updated accordingly with a `GET`/`POST` endpoint pair. Remaining open item: whether the exact hand-off mechanism into this screen is a Dashboard banner, a push-notification deep link, or an app-launch interstitial is still not stated verbatim in either PRD — resolve with the C.24 KMP implementer, but every other blocking question from the original draft is now answered.

## 1. Feature Context
Part of Feature C.21 — Multi-Child Management, triggered by a C.24 plan-downgrade event rather than a direct Child Management action.

## 2. Parent Feature
C.21 Multi-Child Management (cross-cutting with C.24)

## 3. Sub-feature
**K-08 — Trial-Cancellation Forced-Selection Screen**

## 4. Objective
When a plan downgrade leaves the family over capacity, present the parent with a clear, unavoidable-but-not-hostile screen to choose which one child remains active, while a safe server-side default (B-08) prevents any undefined state if the parent hasn't yet responded.

## 5. Business Requirements
- FR-10: parent selects the one child who remains active on trial-cancellation downgrade; all others disabled, retaining data.
- §1.18 #17: Trial-Cancellation Forced-Selection Screen — entry: Plan downgrade event; exit: Child Management List (others now disabled).
- Edge Case #5: safe default (most-recently-active child) applies if the parent hasn't completed selection — this screen's absence or delay must never produce an undefined UI state.

## 6. Existing Architecture
New screen in `:feature:child-management`, entered via a shared trigger surfaced by C.24 (exact UI mechanism — Dashboard banner vs. deep link vs. interstitial — still to be confirmed with C.24's KMP implementer; the screen and its data contract are no longer blocked regardless of which mechanism is chosen).

## 7. Existing Code to Reuse
- `ParentGateLauncher.requireParentAuth()` — step-up for the selection action.
- `FamilyRepository` — extended with `getDowngradeSelectionStatus()`/`submitDowngradeSelection()` wrapping B-08's confirmed `GET`/`POST` pair, following the same wrapper pattern as K-04/K-05.

## 8. Files to Create
- `feature/child-management/src/commonMain/kotlin/.../TrialCancellationForcedSelectionScreen.kt`

## 9. Files to Modify
- `core-navigation/.../Route.kt` — add `DowngradeSelectionRoute`.
- `core-data/.../FamilyRepositoryImpl.kt` — add the two B-08 wrapper methods.
- Whichever surface C.24's implementer confirms as the hand-off point (Dashboard banner component, most likely, per C.20's existing module-shortcut-grid pattern).

## 10. Backend Requirements
Consumes B-08's confirmed `GET /v1/parent/children/downgrade-selection` (pending-state + deadline) and `POST /v1/parent/children/downgrade-selection` (submission).

## 11. KMP Requirements
- Screen presents the family's currently-active-and-over-capacity children as selectable cards; parent taps one to designate "remains active."
- Renders a visible 24-hour countdown derived from `selectionDeadline` in the `GET` response, so the parent understands the window is time-boxed, not indefinite (this is new relative to the original draft, which had no confirmed deadline to render).
- Step-up required before submitting the selection.
- If the safe default has already applied server-side (parent opened the screen after the 24h window, or `GET` returns `pending: false`), the screen reflects the current state as informational rather than presenting a stale selection prompt — read from `GET`'s response, not from a blank/assumed state.
- On submission, all non-selected children show as disabled immediately upon return to K-01's list.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
Consumes B-08's confirmed contract (see that blueprint §13):
```
GET /v1/parent/children/downgrade-selection → { pending, selectionDeadline, eligibleChildIds } | { pending: false }
POST /v1/parent/children/downgrade-selection → { keepActiveChildId } → { keptActiveChildId, disabledChildIds, children }
```

## 14. Database Requirements
Local Room state reflects whatever the family's current active/disabled split is, sourced from B-01 as with every other screen in this feature.

## 15. Validation
Selection must be exactly one child from the currently-active, over-capacity set.

## 16. Authentication
Parent session required.

## 17. Authorization
Step-up required for the selection submission.

## 18. Error Handling
| Scenario | UI Behavior |
|---|---|
| Screen opened after safe default already applied (`pending: false`) | Reflect current state informationally; no selection prompt shown |
| Submission after the 24h deadline (`409 SELECTION_WINDOW_EXPIRED`) | Inline message explaining the window closed and the safe default is now active, with a path to standard Enable (K-04) if the parent wants a different child |
| Network failure on submit | Inline retry, no local state assumed changed until success |
| Capacity changed again mid-flow (`409 CAPACITY_CHANGED`) | Re-fetch `GET` state and re-render before allowing retry |

## 19. Offline First
Selection submission requires connectivity; the screen can render its current-state view from cached data while offline, but cannot submit a change.

## 20. Local Data
Reflects the same `Child` cache K-01/K-09 already maintain — no separate local store.

## 21. Localization
All copy, including the safe-default explanation if shown, localized across EN/HI/AR/UR.

## 22. RTL
Selection-card grid mirrored correctly under RTL.

## 23. Analytics
`trial_cancellation_forced_selection_shown`, `trial_cancellation_forced_selection_completed`.

## 24. Performance
Lightweight screen; no heavy computation.

## 25. Security
Step-up required on the selection submission, consistent with the feature's blanket mutating-action rule.

## 26. Library Requirements
No new libraries anticipated.

## 27. Testing
- Unit: screen correctly reflects a pre-existing safe-default state (`pending: false`) rather than presenting a misleading blank slate.
- Unit: 24h countdown renders correctly from `selectionDeadline`.
- UI test: selection submission requires step-up.
- UI test: post-deadline submission shows the correct explanatory message, not a generic error.
- UI test: full localization and RTL rendering.
- Integration test: submission correctly disables all non-selected children and updates K-01's list.

## 28. Documentation
Document that the hand-off trigger mechanism (Dashboard banner vs. deep link vs. interstitial) is the one remaining item to confirm with C.24's KMP implementer — everything else in this file is implementation-ready.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm Hand-Off Trigger Mechanism (BLOCKING, narrowed scope)**
- **Objective:** Determine the concrete UI mechanism C.24 uses to surface this screen (Dashboard banner is the most likely candidate given C.20's existing module-shortcut pattern, but confirm rather than assume).
- **Definition of Done:** Trigger mechanism documented here; everything else (endpoint contract, 24h window, screen behavior) is already confirmed and does not block on this.

**Task 02 — Repository Wrappers**
- **Objective:** `getDowngradeSelectionStatus()`/`submitDowngradeSelection()` in `:core:data`, wrapping B-08's `GET`/`POST`.
- **Files to Modify:** `FamilyRepositoryImpl.kt`.
- **Tests:** Unit tests for both success and error-code propagation (`409 SELECTION_WINDOW_EXPIRED`, `409 CAPACITY_CHANGED`).
- **Definition of Done:** Both methods correctly surface typed errors the UI can distinguish.

**Task 03 — Screen Build**
- **Objective:** Build the selection UI with the 24h countdown and both pending/resolved states.
- **Files to Create:** `TrialCancellationForcedSelectionScreen.kt`.
- **Definition of Done:** Screen correctly renders "selection pending with countdown," "already resolved by safe default," and "already resolved by prior parent selection" states.

**Task 04 — Submission Wiring & Navigation**
- **Objective:** Wire the step-up-gated submission and register the route/hand-off entry point (per Task 01's confirmed mechanism).
- **Definition of Done:** Full integration test passing, including the post-deadline rejection path.

## 30. Definition of Done
Screen correctly and gracefully handles pending, safe-default-resolved, and parent-resolved states with an accurate 24h countdown; submission is step-up gated; fully localized and RTL-correct.

## 31. Final Verification Checklist
- [ ] Hand-off trigger mechanism confirmed with C.24's KMP implementer
- [ ] 24h countdown renders correctly from `selectionDeadline`
- [ ] Screen correctly distinguishes pending vs. safe-default-resolved vs. parent-resolved states
- [ ] Step-up enforced on submission
- [ ] Post-deadline submission shows the correct explanatory message
- [ ] Full localization and RTL verified
