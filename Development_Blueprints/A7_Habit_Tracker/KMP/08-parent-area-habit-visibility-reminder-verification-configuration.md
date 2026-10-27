# K-08 — Parent Area — Habit Visibility, Reminder & Verification Configuration

## 1. Feature Context
NoorHeroes KMP app, Parent Area (gated by C.19 Parent PIN/Biometric). Lets parents configure which habits their child sees, reminder timing, and optional co-verification.

## 2. Parent Feature
A.7 Habit Tracker — KMP App (Android/iOS)

## 3. Sub-feature
K-08 Parent Area — Habit Visibility, Reminder & Verification Configuration

## 4. Objective
Build the Habit Visibility/Age-Scoping Configuration screen, Habit Reminder Settings screen, and Parent Verification Pending Item widget, framing verification as supportive co-participation, never surveillance (FR-5, FR-6, FR-15).

## 5. Business Requirements
- Only parent-enabled habits are ever visible to the child (FR-5) — configuration changes take effect immediately on the child's next checklist load.
- Verification framed as "Mark this together," never "checking up" language or iconography (FR-6).
- Reminder settings respect quiet-hours/bedtime windows configured via C.23's `BedtimeSettingsScreen`/`BedtimeSettingsViewModel` — this screen only sets habit-specific reminder timing preferences within those bounds.
- Screen gated behind `ParentGateLauncher.requireParentAuth()` (C.19, per §6/§7 corrected API).

## 6. Existing Architecture
**Corrected assumption:** there is no single shared "Parent Area" module. The confirmed convention across sibling blueprints is one dedicated feature module per parent-facing feature area, gated via the consolidated `:core:auth` module's Parent Gate — e.g. `:feature:parental-controls` (C.23), `:feature:parent-dashboard` (C.20), `:feature:reports` (C.22), per `C19_Parent_PIN_Biometric_Gate/KMP/03-parent-profile-gate-grace-window-management.md`, `C20_Parent_Dashboard/KMP/01-parent-dashboard-landing-screen.md`, `C22_Per_Child_Reports/KMP/01-per-child-report-screen-and-state-architecture.md`, `C23_Parental_Controls/KMP/01-controls-landing-navigation.md`. Following this convention, K-08's screens live within `feature-habits`'s own parent-facing package (e.g. `feature-habits/src/commonMain/kotlin/.../parent/`), not a shared Parent Area module — consistent with how each sibling feature owns its own parent-facing screens rather than centralizing them.

## 7. Existing Code to Reuse
- **C.19 Parent Gate (corrected API):** `ParentGateLauncher.requireParentAuth(triggerContext)` from `:core:auth`, plus `GraceWindowManager` for elevation-window reuse — confirmed exact API per `C19_Parent_PIN_Biometric_Gate/KMP/03-parent-profile-gate-grace-window-management.md`, used as this screen's route guard instead of a vague "session-elevation check."
- **C.23 configuration-screen pattern (confirmed concrete precedent):** `feature/parental-controls/.../ui/ScreenTimeSettingsScreen.kt` + `ScreenTimeSettingsViewModel.kt` + `ScreenTimePolicyUiState.kt` (`C23_Parental_Controls/KMP/02-screen-time-settings-usage-display.md`), built on a `Repository interface + Impl` pattern (`ControlsRepository`/`ControlsRepositoryImpl` in `core/data/`) — mirror this exact screen/viewmodel/uistate/repository naming convention for `HabitVisibilityConfigScreen`/`HabitReminderSettingsScreen`.
- **C.23 quiet-hours/bedtime source of truth (corrected — not "A.12"):** `BedtimeSettingsScreen.kt`/`BedtimeSettingsViewModel.kt` (`C23_Parental_Controls/KMP/03-quiet-hours-bedtime-settings.md`, reusing A.4's bedtime time-picker component) — the original "C.23/A.12" reference was a mislabel; A.12 is Avatar System, not Notifications. Quiet-hours bounds are owned by C.23 alone.
- `feature-habits-domain`'s `HabitRepository` (K-01) extended with parent-scoped configuration calls

## 8. Files to Create
- `feature-habits/src/commonMain/kotlin/.../parent/HabitVisibilityConfigScreen.kt`
- `feature-habits/src/commonMain/kotlin/.../parent/HabitReminderSettingsScreen.kt`
- `feature-habits/src/commonMain/kotlin/.../parent/ParentVerificationPendingWidget.kt`
- `feature-habits-domain/src/commonMain/kotlin/.../SubmitVerificationUseCase.kt`
- `feature-habits/src/commonTest/kotlin/.../HabitVisibilityConfigViewModelTest.kt`

## 9. Files to Modify
- `:feature:parent-dashboard`'s dashboard screen (C.20, per `C20_Parent_Dashboard/KMP/01-parent-dashboard-landing-screen.md`) — add `ParentVerificationPendingWidget` entry point
- `:feature:parental-controls`'s Children navigation (C.23) — add Habit Visibility Configuration entry point routing into `feature-habits`

## 10. Backend Requirements
Consumes `POST /v1/habits/verification` (B-08); habit visibility configuration itself is written via the parent-facing counterpart of B-01's catalog (per-child `HabitDefinition.active`/age-band toggles — confirm the exact admin-vs-parent write path against B-01/B-09 before implementation, since B-01 only specifies the read; a parent-facing write endpoint for per-child visibility may need to be added to B-01's scope if not already covered — flag this as a cross-reference gap to resolve with the backend team rather than guessing the endpoint shape).

## 11. KMP Requirements
- Habit Visibility Configuration: per-habit-type toggle scoped to the child's age band, immediate save.
- Habit Reminder Settings: per-child reminder timing preferences, respecting existing quiet-hours bounds (read-only display of those bounds, not editable here).
- Parent Verification Pending Item: list of pending verification requests with "Mark this together" framing; tapping calls `SubmitVerificationUseCase` → B-08.
- Route guarded by `ParentGateLauncher.requireParentAuth(triggerContext)` (C.19).

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
`POST /v1/habits/verification` (B-08). Habit visibility write endpoint: **flagged as a cross-reference gap** — resolve exact contract with backend before implementation (rule 30: do not guess/invent an endpoint).

## 14. Database Requirements (Local)
None beyond standard cache invalidation of the child's habit catalog cache (K-01) on successful configuration save.

## 15. Validation
Test asserting the child's Habit Builder (K-01) cache is correctly invalidated/refreshed after a parent saves a visibility configuration change.

## 16. Authentication
Shared `core-network` Bearer token attachment, parent-session scoped.

## 17. Authorization
Route requires `ParentGateLauncher.requireParentAuth()` elevation (C.19); parent may only configure their own children.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Save fails (network) | Standard retry affordance, no data loss of the in-progress form state |
| Verification submission fails to deliver | Per B-08, child unaffected; item remains pending, shown again next visit |

## 19. Offline First
Configuration writes are not required to be offline-first (parent-initiated, infrequent action); standard online-required form submission with retry is acceptable, consistent with C.20/C.22/C.23's parent-facing screens.

## 20. Local Data
Read-side cache invalidation only (§14); no dedicated offline write queue needed for this parent-facing configuration screen.

## 21. Localization
All copy, especially verification framing language, fully localized and reviewed for tone (cross-reference B-11's review workflow, since verification copy carries the same ethical-tone sensitivity as mercy-suggestion copy).

## 22. RTL
Toggle rows, settings form, and pending-item widget verified for RTL.

## 23. Analytics
`parent_habit_visibility_configured`, `parent_verification_requested`, `parent_verification_completed` via `AnalyticsTracker`.

## 24. Performance
Standard form-screen performance expectations; no special constraints.

## 25. Security
Route-level `ParentGateLauncher.requireParentAuth()` guard (C.19) is the primary control; verification framing is a child-wellbeing/trust control (FR-6), not just a UX nicety.

## 26. Library Requirements
Compose Multiplatform, Koin, Ktor.

## 27. Testing
- Unit: cache-invalidation-on-save test.
- UI: verification widget copy/iconography never uses surveillance-adjacent language (a text-scan test mirroring K-04's shame-word blocklist approach, applied to a "surveillance-language" blocklist instead: "check up", "monitor", "spy", "watch").
- Integration: full visibility-configuration save → child checklist reflects change.

## 28. Documentation
KDoc noting the verification framing requirement explicitly, referencing FR-6's "never religious policing" constraint.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Resolve Habit Visibility Write Endpoint Contract**
- Objective: Confirm the exact parent-facing write API for per-child habit visibility (flagged gap per §13).
- Why Required: Cannot implement against an invented contract per project rule 30.
- Action: Coordinate with backend team / review B-01/B-09 scope; extend B-01 with a parent-facing PATCH if none exists.
- Definition of Done: contract confirmed and documented before Task 02 proceeds.

**Task 02 — Build Habit Visibility Configuration Screen**
- Files to Create: `HabitVisibilityConfigScreen.kt`
- Existing Files to Reuse: C.23's `ScreenTimeSettingsScreen`/`ScreenTimeSettingsViewModel`/`ScreenTimePolicyUiState` pattern and `ControlsRepository`/`ControlsRepositoryImpl` (per §7).
- Tests: cache-invalidation test.
- Definition of Done: toggles save correctly and invalidate the child's catalog cache.

**Task 03 — Build Habit Reminder Settings Screen**
- Files to Create: `HabitReminderSettingsScreen.kt`
- Business Rules: respects existing quiet-hours bounds (read-only display).
- Definition of Done: settings save correctly within documented bounds.

**Task 04 — Build Parent Verification Pending Widget**
- Files to Create: `ParentVerificationPendingWidget.kt`, `SubmitVerificationUseCase.kt`
- Business Rules: FR-6 framing requirement.
- Tests: surveillance-language blocklist scan test.
- Definition of Done: widget correctly lists and submits verifications with non-surveillance framing.

**Task 05 — Wire into Parent Dashboard & Controls Navigation**
- Files to Modify: Parent Dashboard, Parent Controls → Children navigation.
- Definition of Done: entry points correctly reachable.

**Task 06 — Final Code Review**
- Do Not Change: `:core:auth`'s `ParentGateLauncher`/`GraceWindowManager` gate logic.
- Expected Result: PR merge-ready.

## 30. Definition of Done
Habit configuration screens live within `feature-habits`'s parent-facing package, gated behind `ParentGateLauncher.requireParentAuth()` (C.19), verification framed supportively, visibility changes correctly propagate to the child's checklist.

## 31. Final Verification Checklist
- [ ] Habit visibility write endpoint contract confirmed (not guessed)
- [ ] Visibility changes correctly invalidate/refresh the child's checklist cache
- [ ] Verification widget passes the surveillance-language blocklist scan
- [ ] Route gated behind `ParentGateLauncher.requireParentAuth()` (C.19 Parent PIN/Biometric)
- [ ] Screens live in `feature-habits`'s own parent-facing package, not an invented shared "Parent Area" module
- [ ] Reminder settings respect existing quiet-hours bounds
- [ ] Localization and RTL verified
- [ ] Analytics events wired
