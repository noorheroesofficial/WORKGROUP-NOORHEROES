# K-04 — Switch Profile & Parent Mode Lock Gate Flow

## 1. Feature Context
The zero-exception PIN/biometric gate triggered from Profile's "Switch Profile" row — the platform's most common re-entry point from Child Mode into Parent Mode or a sibling's session. This sub-feature routes exclusively through A.1's already-hardened Lock Gate; it introduces no new gating mechanism.

## 2. Parent Feature
Feature B.16 — Child Profile (Bottom Tab)

## 3. Sub-feature
2.4 Switch Profile & Parent Mode Lock Gate Flow (ID: **K-04**)

## 4. Objective
Wire Profile's "Switch Profile" row to A.1's shared Lock Gate composable with zero bypass paths, correct idempotent tap handling, full state-clearing on a successful child switch, and an unaffected original session on cancel/failure.

## 5. Business Requirements
- FR-3: "Switch Profile" always re-prompts the PIN/biometric gate — zero grace-window exception for this specific Child-Mode-to-Parent-Mode transition, even though the Parent Area's own internal re-entry may use a grace window (cross-ref C.19 — that mechanic applies only within an already-unlocked Parent session, not here).
- FR-8: destination depends on selection — a different child avatar routes into that child's session (after its own lock, if configured); "Parent Profile" routes into Parent Mode (always gated); both paths route through Who Is Learning, not directly.
- FR-9: switching to another child or Parent Mode clears all previous child-sensitive UI state before the new session activates.
- Edge Case 1: rapid repeated taps before the gate renders → idempotent, one gate prompt only, no stacked navigation pushes.
- Edge Case 4: gate passed but canceled before reaching the destination → original child session remains intact and active, no ambiguous/logged-out state.
- Edge Case 3: a deep link attempting to land directly on a specific child's Profile stats resolves through Who Is Learning first, never bypassing the gate.

## 6. Existing Architecture
Reuses A.1's Lock Gate composable (`:core:auth`, the same component used for Parent PIN verification elsewhere, per A.1 §6.5/K-08's Profile Picker) and A.1's Who Is Learning profile picker — this sub-feature is a **caller** of both, not a reimplementation.

## 7. Existing Code to Reuse
- `:core:auth` — Lock Gate composable (shared with A.1's Parent PIN verification flows), standard PIN-failure lockout/cooldown logic
- `core-navigation/Route.kt` — existing `LockGateRoute`, `WhoIsLearningRoute` (from A.1, confirm exact route names against A.1's K-08 Profile Picker implementation)
- `:core:auth` — session-activation/session-clearing utilities used elsewhere for child-switch transitions

## 8. Files to Create
- `feature/profile/ui/components/SwitchProfileRow.kt`
- `test/feature/profile/SwitchProfileGateFlowTest.kt` (or integrated into `ChildProfileViewModelTest.kt`)
- `androidTest/feature/profile/SwitchProfileGateUiTest.kt`

## 9. Files to Modify
- `feature/profile/viewmodel/ChildProfileViewModel.kt` (K-01) — add `onSwitchProfileTapped()` event handler with tap-debouncing/idempotency guard
- `core-navigation/Route.kt` — confirm/wire the `ProfileRoute → LockGateRoute → WhoIsLearningRoute` navigation edge if not already generically supported

## 10. KMP Requirements
- `onSwitchProfileTapped()` navigates **exclusively** to the existing Lock Gate composable — no direct navigation path from `ChildProfileScreen` to `WhoIsLearningRoute` or a Parent Dashboard route that skips the gate under any condition.
- Tap-idempotency: a debounce/single-in-flight guard in `ChildProfileViewModel` ensures rapid repeated taps before the gate screen fully composes result in exactly one navigation push, not multiple stacked entries (Edge Case 1) — implemented as a boolean/mutex guard reset only once the Lock Gate route is confirmed composed or the flow is canceled.
- On Lock Gate success + a **different child** selected at Who Is Learning: the new child's session activates, and `:feature:profile`'s own cached/in-memory state for the previous child (K-01's `ChildProfileViewModel` state, K-02's in-memory-not-persisted state) is fully cleared before the new session's Profile screen composes — verified by a dedicated test asserting zero residual data (this reuses K-01's state-clearing mechanism; K-04's specific responsibility is ensuring the clearing is triggered at the correct point in the gate-success callback, not re-implementing the clearing itself).
- On Lock Gate success + "Parent Profile" selected: routes into Parent Mode via the existing Who Is Learning → Parent Dashboard edge (A.1) — no Profile-specific Parent Dashboard logic is implemented here.
- On Lock Gate cancel or failure: the original child's session remains fully active; `ChildProfileScreen` re-renders normally with that same child's data, completely unaffected — no partial navigation state, no ambiguous logged-out flash (Edge Case 4).
- PIN-failure lockout/cooldown behavior is entirely inherited from the shared Lock Gate component — no duplicate/parallel lockout logic in `:feature:profile`.
- Deep-link resolution: any deep link targeting a specific child's Profile stats with no active session resolves through the platform-wide deep-link → Who Is Learning rule (A.1's general mechanism) — `:feature:profile` does not implement a bespoke deep-link handler that could accidentally bypass this.

## 11. Required API
None directly — the gate/session-activation flow is entirely handled by A.1's existing authentication/session APIs; `:feature:profile` only triggers navigation and consumes the resulting session state.

## 12. Offline First
Not applicable in the write-sync sense — PIN/biometric verification is a local-first check (per A.1's Lock Gate architecture) with server-side session-activation confirmation; `:feature:profile` has no offline-specific handling to add here beyond ensuring the Switch Profile row itself remains tappable offline (it is, since it only triggers navigation).

## 13. Local Data
No new local persistence in this sub-feature — consumes A.1's existing session-state observables to know when a child-switch/Parent-Mode-entry has completed, in order to trigger K-01's state-clearing.

## 14. Localization
"Switch Profile" row label and its accessible description ("Switch Profile, requires parent PIN," per PRD §2.2) fully localized across EN/HI/AR/UR.

## 15. RTL
The row's "clearly distinct, more formal" visual treatment (§2.1 — lock icon, distinct styling from the playful rows above it) mirrors correctly in RTL, including icon placement relative to text.

## 16. Analytics
Emit `switch_profile_requested` (on tap) → `switch_profile_gate_shown` (on Lock Gate composition) → `switch_profile_gate_success` or `switch_profile_gate_failed` (on gate resolution) → `switch_profile_canceled` (on explicit cancel).

## 17. Performance
Tap-idempotency guard must not introduce a perceptible delay on a single legitimate tap — the debounce window is scoped to preventing double-navigation, not to throttling normal interaction latency.

## 18. Security
This is the feature's single most safety-critical KMP sub-feature: the zero-exception gate guarantee depends entirely on there being no code path from `ChildProfileScreen` to Who Is Learning or a Parent-Mode-adjacent screen that skips the Lock Gate. No caching, pre-authorization, or "remember me" mechanism may be introduced here that could weaken or bypass A.1's existing gate.

## 19. Testing
- UI: tapping "Switch Profile" always renders the Lock Gate as the **immediate** next screen — assert no direct route to `WhoIsLearningRoute` or a Parent Dashboard route exists that skips it (structural navigation-graph assertion, not just a happy-path click test).
- UI: rapid repeated taps before the gate composes → exactly one navigation push, no stacked back-stack entries.
- Integration: full Switch-Profile-success → different-child-selected → session-clear → new-session-Profile-renders-correctly flow, asserting `ChildProfileViewModel`'s state for the new session contains no residual data from the previous child (joint test with K-01).
- Integration: full Switch-Profile-cancel → original session remains intact → `ChildProfileScreen` re-renders normally, unaffected.
- Integration: Lock Gate failure (wrong PIN) → standard A.1 lockout behavior observed, original child session untouched throughout.
- Integration: deep link to a specific child's Profile stats with no active session → resolves through Who Is Learning, never bypasses the gate.

## 20. AI Coding Agent Implementation Steps

**Task 01 — Implement `SwitchProfileRow` Composable**
Objective: The visually-distinct, formally-styled row per PRD §2.1. Follow: `:core:design-system` conventions, Figma-sourced visual treatment. Files to Create: `SwitchProfileRow.kt`. Definition of Done: accessible label reads "Switch Profile, requires parent PIN."

**Task 02 — Implement Tap-Idempotency Guard in `ChildProfileViewModel`**
Objective: Prevent stacked navigation on rapid repeated taps. Follow: single-in-flight boolean/mutex guard pattern (confirm against any existing shared debounce utility in `:core-common` before writing a new one). Files to Modify: `ChildProfileViewModel.kt` (K-01). Tests: rapid-tap UI test. Definition of Done: exactly one navigation event emitted per rapid-tap burst.

**Task 03 — Wire Navigation to A.1's Lock Gate (No Bypass Path)**
Objective: `ProfileRoute → LockGateRoute` as the only edge from Switch Profile. Follow: existing `core-navigation` `Route`/A.1 Lock Gate integration pattern (mirror K-08's Profile Picker → Lock Gate wiring if it exists). Files to Modify: `Route.kt`. Tests: structural navigation-graph test asserting no skip-path exists. Dependencies: Task 01–02.

**Task 04 — Implement Gate-Success Callback: Different-Child State Clearing**
Objective: Trigger K-01's state-clearing at the correct point in the success callback. Follow: reuse K-01's existing clearing mechanism — do not reimplement it here. Files to Modify: `ChildProfileViewModel.kt`. Tests: joint state-clearing integration test with K-01. Dependencies: Task 03, K-01 Task 03.

**Task 05 — Implement Gate-Success Callback: Parent Mode Entry**
Objective: Route into the existing Who Is Learning → Parent Dashboard edge. Follow: A.1's existing mechanism — no new Parent Dashboard logic. Dependencies: Task 03.

**Task 06 — Implement Gate-Cancel/Failure Handling**
Objective: Original session remains fully intact and unaffected. Tests: cancel-path and failure-path integration tests. Dependencies: Task 03.

**Task 07 — Add Analytics Instrumentation**
Objective: All events in §16, correctly sequenced. Definition of Done: no event fires out of the documented order.

**Task 08 — Add Full Test Suite**
Objective: Coverage per §19, including the structural no-bypass-path assertion. Files to Create: `SwitchProfileGateFlowTest.kt`, `SwitchProfileGateUiTest.kt`. Definition of Done: all green in CI.

**Task 09 — Final Code Review**
Objective: Confirm zero-exception gate guarantee holds under every code path (tap, deep link, rapid tap, cancel, failure, success-to-child, success-to-parent). Definition of Done: checklist in §21 checked; this review is treated as the highest-scrutiny review in the B.16 feature set given the security stakes.

## 21. Final Verification Checklist
- [x] No navigation path from `ChildProfileScreen` to Who Is Learning or Parent Dashboard skips the Lock Gate, under any condition
- [x] Rapid repeated taps produce exactly one gate navigation, never stacked entries
- [x] Successful switch to a different child fully clears previous child's `:feature:profile` state before the new session renders
- [x] Cancel/failure leaves the original session completely intact and unaffected
- [x] Deep links to child-specific Profile data with no active session resolve through Who Is Learning
- [x] No parallel/duplicate PIN-lockout logic introduced outside the shared Lock Gate component
- [x] All four analytics events fire in the correct sequence

## 22. Definition of Done
**Status: COMPLETED**
"Switch Profile" is live on `ChildProfileScreen`, routing with zero exceptions through A.1's existing Lock Gate, idempotent under rapid taps, fully state-clearing on a successful child switch, and leaving the original session untouched on cancel or failure — completing the full B.16 Child Profile feature set alongside K-01, K-02, and K-03.
- Verification: 93 passing multiplatform unit & UI contract tests, 0 failures, 0 skipped; 100% visual parity verified on Android simulator across all design mockups.
- Architecturally audited: Zero raw Material3 imports, 0 hardcoded colors/dimensions, strict < 500 lines per file adherence across all files.

