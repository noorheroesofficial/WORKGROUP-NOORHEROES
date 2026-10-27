# K-05 — Permanent Deletion Warning & Confirmation Flow

## 1. Feature Context
Part of Feature C.21 — Multi-Child Management. The single most serious-toned screen in the Parent Area — deliberately sober, minimal, and friction-free in the right direction (no dark patterns).

## 2. Parent Feature
C.21 Multi-Child Management

## 3. Sub-feature
**K-05 — Permanent Deletion Warning & Confirmation Flow**

## 4. Objective
Guarantee that `acknowledged_warning: true` is sent to the backend only after a genuine, informed, unhurried confirmation — never from any other code path — while giving the parent an equally easy way to cancel as to confirm.

## 5. Business Requirements
- FR-5: full step-up → warning → confirm → execute flow.
- §2.2 Screen: Permanent Deletion — Irreversible-Data Warning — two equally-sized buttons, no artificial delay/countdown, warning text as focal screen-reader content.
- Android AI Prompt items 3-4: exact warning text, equally-sized buttons differing only in semantic color (UI test asserting equal measured bounds); `acknowledged_warning: true` sent ONLY after "Permanently Delete" tap (test confirming no other code path sends true).
- Edge Case #3: back out before final confirmation → no deletion occurs, profile unaffected.
- Edge Case #9: deleting the only remaining active child → allowed, gentle informational note only.

## 6. Existing Architecture
Multi-step Compose flow within `:feature:child-management`: Step-Up Gate (shared with C.19) → Irreversible-Data Warning screen → Deletion Success Confirmation.

## 7. Existing Code to Reuse
- `ParentGateLauncher.requireParentAuth()` (C.19) — the Step-Up Gate step is entirely reused, not reimplemented.
- `FamilyRepository.deleteChild()` — new thin wrapper over B-06.
- `Error` design-system token (`CORE_DESIGNSYSTEM_INSTRUCTIONS.md`) — reused for the warning's visual treatment, not a bespoke color.

## 8. Files to Create
- `feature/child-management/src/commonMain/kotlin/.../DeletionWarningScreen.kt`
- `feature/child-management/src/commonMain/kotlin/.../DeletionSuccessScreen.kt`

## 9. Files to Modify
- `core-data/.../FamilyRepositoryImpl.kt` — add `deleteChild(childId, acknowledgedWarning: Boolean)`.
- `ChildManagementViewModel.kt` — add the deletion-funnel state machine.

## 10. Backend Requirements
Consumes B-06 exclusively.

## 11. KMP Requirements
- `acknowledged_warning: true` is a literal that exists in exactly one place in the codebase: the "Permanently Delete" button's `onClick` handler. No other call site constructs this payload with `true`.
- Two buttons (Cancel / Permanently Delete) must be measured-equal in size — build via a shared `Row` with `Modifier.weight(1f)` on both, not manually sized, to make equal sizing structurally guaranteed rather than incidentally true.
- No artificial delay/countdown gating the Confirm button's tappability — it must be interactive immediately on screen render.
- Cancel at any point (including system back gesture) returns to K-01's list with zero server-side effect.
- On the only-remaining-active-child case, render a gentle informational note inline on the warning screen itself (not a separate blocking dialog) — informational, never a hard block.
- On success, route to Deletion Success Confirmation, then back to K-01's list with the deleted child removed from the rendered set.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
Consumes B-06's contract as documented in that blueprint.

## 14. Database Requirements
Local Room row for the deleted child removed (or marked `deletion_pending`, matching backend status) immediately on success, feeding K-09's cache-invalidation.

## 15. Validation
None — the "validation" here is entirely the human confirmation step itself.

## 16. Authentication
Parent session + step-up required to even reach the warning screen.

## 17. Authorization
Step-up gate is the first step of this flow, non-optional.

## 18. Error Handling
| Scenario | UI Behavior |
|---|---|
| Network failure on confirm | Inline retry, warning screen remains, no partial state |
| Step-up cancelled | Return to list, no warning screen shown |
| Cancel tapped on warning screen | Return to list, no server call made at all |

## 19. Offline First
Entire flow blocked while offline — deletion requires connectivity throughout.

## 20. Local Data
Child row removed/marked from local cache only after server confirms success — never optimistically, given irreversibility.

## 21. Localization
The exact warning text ("Deleted data cannot be recovered. This action is permanent.") is a translated string, not hardcoded — translated meaning preserved exactly across EN/HI/AR/UR, reviewed for tone (sober, not alarmist) in each locale per §2.5's Arabic RTL prompt example.

## 22. RTL
Full RTL layout for the warning screen — text alignment, button order (visually mirrored but logically Cancel-then-Confirm preserved for screen readers), per §2.5's explicit Arabic RTL wireframe description.

## 23. Analytics
Full funnel: `child_delete_initiated` → `child_delete_warning_shown` → (`child_delete_confirmed` → `child_delete_completed`) OR `child_delete_canceled`.

## 24. Performance
Lightweight, single-purpose screens; no heavy computation.

## 25. Security
This screen is the client-side half of B-06's double-gate guarantee — the UI test confirming `acknowledged_warning: true` originates from exactly one call site is the definitive control verifying no accidental/automated path can trigger real deletion.

## 26. Library Requirements
No new libraries.

## 27. Testing
- **Highest-priority UI test (Android AI Prompt item 3):** Cancel and Permanently Delete buttons have equal measured bounds.
- **Highest-priority UI test (Android AI Prompt item 4):** grep/static-analysis-style test or runtime assertion confirming no code path other than the confirm button's handler constructs `acknowledgedWarning = true`.
- UI test: no artificial delay before Confirm is tappable (assert enabled state immediately on composition).
- UI test: Cancel/back-gesture at every step results in zero server calls.
- Integration test: full deletion completes, child removed from K-01's list.
- Integration test: cancellation at the final step leaves the profile completely unaffected (per Edge Case #3, PRD §13.2 Test Case #3 equivalent).
- UI test: only-remaining-active-child informational note renders inline, non-blocking.

## 28. Documentation
Document prominently in KDoc that `acknowledgedWarning = true` must never be introduced at any other call site — flag this file for extra scrutiny in code review given its irreversibility.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Repository Wrapper**
- **Objective:** `deleteChild(childId, acknowledgedWarning)` in `:core:data`.
- **Files to Modify:** `FamilyRepositoryImpl.kt`.
- **Tests:** Unit test confirming the payload is passed through unmodified (no default-`true` anywhere in this layer).
- **Definition of Done:** Repository layer never supplies a default value for `acknowledgedWarning` — it must always be explicitly passed by the caller.

**Task 02 — Deletion Warning Screen**
- **Objective:** Build the sober, equal-button warning screen.
- **Files to Create:** `DeletionWarningScreen.kt`.
- **Implementation Details:** `Row(Modifier.fillMaxWidth()) { Button(Modifier.weight(1f)) { Cancel }; Button(Modifier.weight(1f)) { PermanentlyDelete } }`; `acknowledgedWarning = true` literal exists only in the second button's `onClick`.
- **Tests:** Both highest-priority UI tests from §27.
- **Definition of Done:** Both tests pass; code review confirms the single-call-site guarantee.

**Task 03 — Step-Up Gate Integration & Full Funnel**
- **Objective:** Wire the Step-Up Gate → Warning → Success sequence with full analytics.
- **Files to Modify:** `ChildManagementViewModel.kt`.
- **Files to Create:** `DeletionSuccessScreen.kt`.
- **Definition of Done:** Full funnel analytics fire correctly at each step; cancellation at any point produces zero server-side effect.

**Task 04 — Only-Remaining-Active-Child Informational Note**
- **Objective:** Render the gentle note without blocking.
- **Files to Modify:** `DeletionWarningScreen.kt`.
- **Definition of Done:** Note renders inline when applicable, never gates the Confirm button.

## 30. Definition of Done
Both highest-priority security/UX guarantees (equal buttons, single-call-site acknowledgment) are test-verified; full funnel analytics correct; cancellation is provably a no-op.

## 31. Final Verification Checklist
- [ ] Equal-button-size test passes
- [ ] Single-call-site `acknowledgedWarning: true` guarantee verified
- [ ] No artificial delay before Confirm is tappable
- [ ] Full deletion + cancellation flows both integration-tested
- [ ] Only-remaining-active-child note is informational, non-blocking
- [ ] Full localization and RTL verified for the warning text specifically
- [ ] Full analytics funnel fires correctly
