# K-07 — Parent Ramadan Settings Card & Dashboard Tab

## 1. Feature Context
The parent-facing control surface for the entire season — per-child fasting-approach configuration, Fasting Tracker visibility, reminders, invites — plus the Ramadan Dashboard tab that only appears within C.20's existing Parent Dashboard shell during the active window, never as a permanent addition to the parent's navigation.

## 2. Parent Feature
F.36 — Ramadan Mode

## 3. Sub-feature
2.7 Parent Ramadan Settings Card & Dashboard Tab (ID: **K-07**)

## 4. Objective
Build the Ramadan Settings Card (Parent Area) and the conditionally-rendered Ramadan Dashboard Tab within C.20's existing shell.

## 5. Business Requirements
- §1.18 Screens 15-16: Ramadan Settings Card (Parent), Ramadan Dashboard Tab (Parent).
- FR-9/FR-10: three parent-configurable fasting approaches per child; parent toggle to exclude a child entirely.
- §1.15: Fasting Tracker visibility hidden, not shown-disabled, per child.
- §6.3: Ramadan Dashboard tab is conditionally rendered within C.20's existing shell, active window only.
- Edge Case 3: fasting-approach change mid-Ramadan preserves prior entries.

## 6. Existing Architecture
`:feature:ramadan` module; Ramadan Dashboard Tab follows C.20's existing card pattern per §2.4's wireframe description, injected into C.20's Parent Dashboard shell as a conditional tab, not a separate top-level destination.

## 7. Existing Code to Reuse
- C.20's Parent Dashboard shell/tab-injection mechanism
- A.7's existing habit/approach-configuration UI pattern (structural reference for the fasting-approach selector)
- `:core:design-system`'s card component

## 8. Files to Create
- `feature/ramadan/presentation/parentsettings/RamadanSettingsCardScreen.kt`
- `feature/ramadan/presentation/parentsettings/RamadanSettingsViewModel.kt`
- `feature/ramadan/presentation/dashboard/RamadanDashboardTab.kt`
- `feature/ramadan/domain/usecase/UpdateFastingApproachUseCase.kt`
- `feature/ramadan/domain/usecase/UpdateTrackerVisibilityUseCase.kt`

## 9. Files to Modify
- C.20's Parent Dashboard shell — register the conditional Ramadan tab, gated on K-01's shared phase state being within the active window

## 10. KMP Requirements
- **UI/Screen:** Settings Card with per-child fasting-approach radio-group selector (full fast / practice / education-only) and a separate Fasting Tracker visibility toggle; Dashboard Tab following C.20's card pattern.
- **State/ViewModel:** `RamadanSettingsViewModel` holds per-child approach/visibility state, synced to/from the backend (approach configuration lives in A.7's store per B-04's §6 architecture note).
- **Conditional rendering:** the Dashboard Tab is present in C.20's tab list only while K-01's shared `RamadanCampaignViewModel` reports an active-window phase — absent entirely outside the window, not merely disabled.
- **Mid-season change handling:** UI clearly communicates that changing the approach only affects future nights, consistent with Edge Case 3 and B-04's server-side rule — never implies past entries will be altered.
- **Loading/Empty/Error:** loading state for settings fetch; error state with retry for save failures.

## 11. NextJS Requirements
N/A.

## 12. API Contract
Approach/visibility configuration endpoints — **flagged, do not guess:** PRD §3.4 does not enumerate a dedicated settings-write endpoint separately from B-04's fasting-log validation logic; confirm against A.7's existing habit-configuration API surface (referenced in B-04 §6/§7) before implementation, per B-04's own flagged item. `GET /v1/ramadan/family-aggregate` (B-06, consumed by the Dashboard Tab for the aggregate summary card).

## 13. Database Requirements
No new local table required beyond a settings-state cache consistent with A.7's existing local-cache pattern for habit configuration.

## 14. Validation
Client-side form validation on the approach selector (single-select enforced); server remains the authority.

## 15. Authentication
Standard authenticated parent session.

## 16. Authorization
Parent may only configure their own family's children.

## 17. Error Handling
Save failure → clear retry affordance, previous saved state remains displayed (no optimistic-update ghosting of an unsaved change).

## 18. Offline First
Settings changes queue via B.15's outbox pattern if offline, consistent with the rest of the module; Dashboard Tab's summary data falls back to K-08's cached family-aggregate.

## 19. Local Data
Local cache of per-child approach/visibility settings for fast Settings Card load.

## 20. Localization
Approach labels ("Full Fast," "Practice," "Education Only"), toggle labels, and Dashboard Tab copy fully localized across En/Hi/Ar/Ur.

## 21. RTL
Full RTL layout for the radio-group selector and Dashboard Tab card.

## 22. Analytics
`ramadan_fasting_approach_changed` per §1.19, emitted on save from this screen (the single emission point for this event, per B-04's cross-reference note).

## 23. Performance
Dashboard Tab's conditional presence/absence in C.20's tab list must not cause a layout shift or flicker across app sessions when the window opens/closes — verified with a UI test capturing the transition.

## 24. Security
Settings mutation requires only a standard authenticated parent session (no elevated Parent Gate needed, distinct from certificate/card generation) — consistent with B-04's authorization model.

## 26. Library Requirements
Kotlin, Jetpack Compose, Hilt, Retrofit + OkHttp, Room/SQLDelight. No new libraries.

## 27. Testing
Unit: approach-selector state management, mid-season-change messaging logic. UI test: **mandatory** — Fasting Tracker visibility toggle rendering is hidden-not-disabled consistent with K-03's contract; Dashboard Tab presence/absence correctly gated by K-01's shared phase state. Integration: settings save → reflected correctly in K-03's Fasting Tracker on next load.

## 28. Documentation
KDoc noting the Dashboard Tab must be entirely absent (not disabled) outside the active window, mirroring the Fasting Tracker's own hidden-not-disabled discipline.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm the Settings API Contract**
Objective: Identify the exact endpoint against A.7's existing habit-configuration surface (do not guess). Files to Read: A.7's habits-context API. Definition of Done: contract documented before Task 02.

**Task 02 — Implement `UpdateFastingApproachUseCase` and `UpdateTrackerVisibilityUseCase`**
Objective: Write paths for approach/visibility settings. Files to Create: `domain/usecase/UpdateFastingApproachUseCase.kt`, `domain/usecase/UpdateTrackerVisibilityUseCase.kt`. Dependencies: Task 01. Tests: use-case unit tests. Definition of Done: tests pass.

**Task 03 — Implement `RamadanSettingsViewModel`**
Objective: Per-child settings state management. Files to Create: `presentation/parentsettings/RamadanSettingsViewModel.kt`. Dependencies: Task 02. Tests: state-management unit tests. Definition of Done: tests pass.

**Task 04 — Build `RamadanSettingsCardScreen`**
Objective: Approach selector + visibility toggle UI. Files to Create: `presentation/parentsettings/RamadanSettingsCardScreen.kt`. Dependencies: Task 03. Tests: **mandatory** — hidden-not-disabled toggle test. Definition of Done: test passes.

**Task 05 — Build `RamadanDashboardTab` with Conditional Registration**
Objective: C.20-pattern card, gated on active-window phase. Files to Create: `presentation/dashboard/RamadanDashboardTab.kt`. Files to Modify: C.20's shell. Dependencies: K-01, B-06. Tests: **mandatory** — presence/absence gating test, no layout shift. Definition of Done: test passes.

**Task 06 — Wire Settings-to-Tracker Sync**
Objective: Confirm K-03's Fasting Tracker reflects settings changes on next load. Dependencies: Task 04, K-03. Tests: integration test. Definition of Done: test passes.

**Task 07 — Add Localization, Analytics, and Full Test Suite**
Objective: Complete §20/§22/§27 coverage, both mandatory tests included. Definition of Done: all green in CI.

**Task 08 — Final Code Review**
Objective: Confirm the Dashboard Tab's conditional logic mirrors K-03's hidden-not-disabled discipline exactly. Definition of Done: checklist in §30 checked.

## 30. Final Verification Checklist
- [ ] Fasting Tracker visibility toggle is hidden-not-disabled consistent with K-03
- [ ] Dashboard Tab present/absent correctly by active-window phase, no layout shift — mandatory test passing
- [ ] Mid-season approach change UI never implies past-entry alteration
- [ ] Settings changes correctly reflected in K-03 on next load

## 31. Definition of Done
Parents have full, clear, correctly-time-gated control over each child's Ramadan participation, with every setting change respecting the platform's anti-shaming, no-retroactive-alteration philosophy.
