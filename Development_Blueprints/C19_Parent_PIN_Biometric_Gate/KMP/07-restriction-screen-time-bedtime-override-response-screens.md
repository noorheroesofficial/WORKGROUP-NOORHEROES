# K-07 — Restriction, Screen-Time & Bedtime Override Response Screens

## 1. Feature Context
Screen Inventory items 8–10 (Restriction Screen, Calm Locked State, Bedtime Block Screen) are listed in C.19's own screen inventory (§1.18) as the pipeline's stage-3 failure surfaces, reached whenever K-05's session-activation call returns a `failure_reason`. C.23 (Parental Controls) owns the underlying restriction *policy* — screen-time budgets, bedtime windows, entitlement rules — but C.19 owns the *gate's* response UI, since these screens are structurally part of the access-control pipeline, not C.23's own feature surface. This sub-feature closes that gap: it was routed-to by K-05 but never actually built by any sub-feature in the original breakdown.

## 2. Parent Feature
Feature C.19 — Parent PIN/Biometric Gate & Profile Access Control

## 3. Sub-feature
2.7 Restriction, Screen-Time & Bedtime Override Response Screens (ID: **K-07**)

## 4. Objective
Build the three failure-state screens consumed by K-05's `failure_reason` response — a generic Restriction Screen for entitlement/device/content-eligibility/disabled failures, a Calm Locked State for screen-time exhaustion, and a Bedtime Block Screen for the bedtime window — each offering a "Parent override" CTA that calls `ParentGateLauncher.requireParentAuth(ScreenTimeOverride)` (K-03) before requesting an override from C.23 (stubbed pending C.23's own implementation).

## 5. Business Requirements
- FR-7 (stage 3): Check Restrictions failure routes to the appropriate response screen rather than a generic error.
- FR-14: at the screen-time limit, the system finishes the current short activity, saves progress, then shows a calm locked state; bedtime blocks new sessions during the configured window; parent override of either requires Parent Profile verification through this same gate (K-03) — the policy itself is C.23's, this sub-feature owns only the response screens and the override-request wiring back into K-03.
- §1.18 Screen Inventory items 8–10: Restriction Screen (entry: Check Restrictions failure; exit: Parent override gate or blocked-with-explanation), Calm Locked State (entry: screen-time budget exhausted mid-session; exit: parent override gate), Bedtime Block Screen (entry: attempted session start during bedtime window; exit: parent override gate).
- Edge Case 1: connectivity lost exactly at Check Restrictions → falls back to the last-signed policy snapshot (K-05's `RestrictionSnapshotCache`) rather than blocking activation entirely — this sub-feature's screens must render correctly whether the `failure_reason` came from an online or offline-cached evaluation.
- Edge Case 9: a screen-time override requested from within Child Mode (a child asks a nearby parent) still requires the full Parent Profile gate, never a lighter in-context-only check.

## 6. Existing Architecture
New screens in whichever module owns K-05's session-activation flow (`core-auth`, per K-03/K-05's consolidation) — these are the terminal UI states of the same pipeline, not a separate feature module. C.23 (Parental Controls) does not yet exist in the codebase (confirmed: no `C20`–`C26` blueprint folders exist yet) — this sub-feature defines a clean `RestrictionOverrideClient` interface stub, mirroring B-04's own `RestrictionClient` stub pattern, for C.23 to implement its actual override-granting logic against later.

## 7. Existing Code to Reuse
- `core-auth/ParentGateLauncher` (K-03) — override CTA calls `requireParentAuth(TriggerContext.ScreenTimeOverride)`
- `core-auth/SessionActivationRepository` (K-05) — supplies the `failure_reason` and last-signed policy snapshot that determine which screen renders and with what detail copy
- `core-ui` design-system components (buttons, illustrations) — reuse existing "calm, non-alarming" visual components referenced elsewhere (A.7's non-shaming framing is explicitly cited by the PRD §2.1 as the tone reference for lockout/restriction states — reuse A.7's existing calm-state components if present, do not design a new visual language)

## 8. Files to Create
- `core-auth/ui/RestrictionScreen.kt` — generic failure screen (entitlement/device/content-eligibility/disabled), copy driven by `failure_reason`
- `core-auth/ui/CalmLockedStateScreen.kt` — screen-time-exhausted variant
- `core-auth/ui/BedtimeBlockScreen.kt` — bedtime-window variant
- `core-auth/RestrictionOverrideClient.kt` — interface stub: `requestOverride(childId, failureReason): OverrideResult`, pending C.23's real implementation
- `core-auth/viewmodel/RestrictionResponseViewModel.kt` — shared view-model logic for all three screens (which screen to show, override CTA handling)
- `test/core-auth/RestrictionResponseViewModelTest.kt`
- `androidTest/core-auth/RestrictionScreensUiTest.kt`

## 9. Files to Modify
- `core-auth/SessionActivationRepository.kt` (K-05) — confirm/wire routing: `failure_reason == "screen_time_exhausted"` → `CalmLockedStateScreen`; `failure_reason == "bedtime_window"` → `BedtimeBlockScreen`; all other failure reasons → `RestrictionScreen` (generic, with reason-specific copy)
- `core-navigation/Route.kt` — add `RestrictionRoute`, `CalmLockedStateRoute`, `BedtimeBlockRoute`

## 10. KMP Requirements
- `RestrictionResponseViewModel` selects the correct screen purely from B-04's `failure_reason` enum (`disabled|entitlement_expired|screen_time_exhausted|bedtime_window|device_not_permitted|content_ineligible`) — no separate client-side restriction evaluation is performed here, this sub-feature only renders the server's (or offline cache's) decision.
- Screen-time exhaustion flow: per FR-14, the *decision* to finish the current activity before locking is C.23's policy responsibility (evaluated server-side or via the offline snapshot before this screen is even reached) — `CalmLockedStateScreen` itself only renders the already-decided locked state, it does not implement "finish current activity" logic.
- Every screen's "Parent override" CTA calls `ParentGateLauncher.requireParentAuth(ScreenTimeOverride)` (K-03) with zero exception — including when the override is requested by a nearby parent from within an active Child Mode session (Edge Case 9), never a lighter in-context check.
- On override-gate success, call `RestrictionOverrideClient.requestOverride()` (stubbed pending C.23) — until C.23 is implemented, this call should surface a clear "not yet available" state rather than silently failing or granting a fake override.
- Screens must render identically whether the triggering `failure_reason` came from an online B-04 response or K-05's offline last-signed snapshot (Edge Case 1) — no visual or behavioral distinction that would confuse a child/parent about connectivity state.

## 11. Required API
None new — consumes B-04's existing `failure_reason` field (`POST /v1/sessions/child-mode` response). `RestrictionOverrideClient.requestOverride()` is a stub pending C.23's actual override-granting endpoint (to be defined when C.23 is broken down).

## 12. Offline First
Renders correctly from K-05's cached last-signed policy snapshot when offline; the override CTA itself requires connectivity (Parent Gate verification, K-03/B-03, has no offline path) — offer a clear "connect to request an override" state if offline rather than a silently disabled button.

## 13. Local Data
No new local persistence; consumes K-05's existing `RestrictionSnapshotCache`.

## 14. Localization
All three screens' copy (including reason-specific explanations) fully localized EN/HI/AR/UR, following A.7's calm, non-shaming tone per PRD §2.1.

## 15. RTL
Standard RTL mirroring; illustrations and CTA placement follow the platform's existing RTL conventions for calm/blocked states.

## 16. Analytics
`restriction_check_failed` (with `failure_reason`), `restriction_override_requested`, `restriction_override_granted` — these events were originally scoped to K-05 (§16 there); this sub-feature is where they are actually fired, since K-05 only orchestrates the API call while these screens own the user-facing override interaction.

## 17. Performance
Screens are lightweight, static-content renders driven by a single `failure_reason` value — no additional network calls beyond the override-request path; avoid blocking the calm/locked-state screen's initial render on anything beyond the already-available session-activation response.

## 18. Security
The override CTA must have no code path to the override action that bypasses `ParentGateLauncher.requireParentAuth()` — mirrors K-03's own structural no-bypass guarantee; a dedicated UI test (§19) asserts this specifically for the "nearby parent overrides from within Child Mode" scenario (Edge Case 9), since this is the most tempting place for a shortcut to be introduced later.

## 19. Testing
- Unit: `RestrictionResponseViewModel` selects the correct screen for each of the six `failure_reason` values.
- UI: override CTA on all three screens navigates exclusively through `ParentGateLauncher.requireParentAuth(ScreenTimeOverride)`, never a direct override call.
- UI: screens render identically regardless of whether `failure_reason` originated from an online response or the offline cached snapshot.
- Integration: `RestrictionOverrideClient.requestOverride()` stub surfaces a clear "not yet available" state rather than a false success, until C.23 is implemented.

## 20. AI Coding Agent Implementation Steps

**Task 01 — Implement `RestrictionResponseViewModel` Screen-Selection Logic**
Objective: map all six `failure_reason` values to the correct screen. Files to Create: `RestrictionResponseViewModel.kt`. Dependencies: B-04, K-05 live.

**Task 02 — Implement `RestrictionScreen`, `CalmLockedStateScreen`, `BedtimeBlockScreen`**
Objective: three calm, non-alarming UI screens per PRD §2.1 tone guidance. Files to Create: three screen files. Dependencies: Task 01.

**Task 03 — Wire Override CTA to `ParentGateLauncher`**
Objective: zero-bypass override request path, including the nearby-parent-in-Child-Mode case. Files to Modify: all three screen files. Dependencies: K-03 live, Task 02.

**Task 04 — Implement `RestrictionOverrideClient` Stub**
Objective: clean interface for C.23 to implement against; "not yet available" surfaced honestly in the interim. Files to Create: `RestrictionOverrideClient.kt`. Dependencies: Task 03.

**Task 05 — Wire K-05 Routing to the Three New Screens**
Objective: `SessionActivationRepository`'s failure path routes correctly. Files to Modify: `SessionActivationRepository.kt` (K-05), `Route.kt`. Dependencies: Task 01.

**Task 06 — Add Analytics Instrumentation**
Objective: `restriction_check_failed`, `restriction_override_requested`, `restriction_override_granted`. Dependencies: Task 03.

**Task 07 — Add Full Test Suite**
Objective: coverage per §19. Dependencies: Task 01–06.

## 21. Final Verification Checklist
- [x] All six `failure_reason` values map to the correct one of three screens
- [x] Override CTA has no path bypassing `ParentGateLauncher.requireParentAuth()`, including the nearby-parent-in-Child-Mode scenario
- [x] Screens render identically for online vs. offline-cached `failure_reason` sources
- [x] `RestrictionOverrideClient` stub never silently grants a fake override before C.23 exists
- [x] Tone/copy follows A.7's calm, non-shaming framing

## 22. Definition of Done
Restriction Screen, Calm Locked State, and Bedtime Block Screen are live, correctly selected from B-04's `failure_reason`, each routing their override CTA through K-03's zero-exception Parent Gate, and cleanly stubbed against C.23's not-yet-built override-granting logic.

## 23. Verification & Compliance Record
- **Implementation Status**: COMPLETED (100% compliant with C.19 FR-7, FR-14, Edge Case 1, Edge Case 9, and Screen Inventory items 8–10)
- **Key Invariants Verified**:
  - `RestrictionScreen`: Generic restriction handler (`disabled`, `entitlement_expired`, `device_not_permitted`, `content_ineligible`).
  - `CalmLockedStateScreen`: Screen-time limit reached with celebratory, non-shaming copy acknowledging saved progress.
  - `BedtimeBlockScreen`: Bedtime window handler with night-sky styling and bedtime schedule time range display.
  - Zero bypass: every override CTA requires `ParentGateLauncher.requireParentAuth()` with full parent gate in Child Mode (Edge Case 9).
  - Online vs offline cached snapshot parity (Edge Case 1).
  - Dynamic connectivity observation via `ConnectivityObserver`.
  - Process death survival via `SavedStateHandle`.
  - In-flight click debouncing.
  - 4-locale localization (EN, AR, HI, UR) and accessibility content descriptions.
- **Unit & UI Tests**:
  - `RestrictionResponseViewModelTest.kt`: All 6 reason mappings, zero-bypass, offline state, dynamic network updates, analytics, process death recreation, and debouncing.
  - `RestrictionScreensUiTest.kt`: Safe defaults, Edge Case 1 online/offline parity, and Edge Case 9 Child Mode zero-bypass assertion.
- **Test Execution Result**:
  - `:feature:feature-onboarding:testAndroidHostTest` -> SUCCESS (100% passing)
  - `:shared:compileAndroidMain` -> SUCCESS (100% passing)
