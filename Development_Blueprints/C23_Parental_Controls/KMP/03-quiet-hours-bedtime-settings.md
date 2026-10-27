# K-03 — Quiet Hours / Bedtime Settings

## 1. Feature Context
Lets a parent configure a bedtime window during which new sessions can't start, supporting midnight-crossing windows (PRD C.23 §1.18 Screen #3, §3.4).

## 2. Parent Feature
Feature C.23 — Parental Controls (Screen Time, Bedtime, AI Permissions, Content Age Level)

## 3. Sub-feature
2.3 Quiet Hours / Bedtime Settings (ID: **K-03**)

## 4. Objective
Build `BedtimeSettingsScreen` with two time-pickers (`bedtime_start`, `bedtime_end`) that correctly accept and serialize midnight-crossing windows (e.g., 20:00→07:00), saving through `ControlsRepository.updateRestrictions()` gated by the Parent Gate.

## 5. Business Requirements
- FR-2 item 5: bedtime evaluated continuously, not locked in at session start — a bedtime-window change takes effect immediately regardless of when configured, distinct from the daily-limit's "applies next session" pattern (Edge Case 5).
- §3.4: `GET/PATCH /v1/children/{id}/restrictions` (bedtime fields).
- §5 item 4 (backend prompt, reused client-side): midnight-crossing windows like 20:00–07:00 must be valid and mean overnight, never "negative duration."

## 6. Existing Architecture
Reuses A.4's established bedtime-configuration time-picker pattern and midnight-crossing validation logic exactly (PRD explicitly cross-references this) — **do not reimplement bedtime-window validation from scratch; extend/reuse A.4's existing component if one exists in `:feature:audio-bedtime-player` or a shared location**.

## 7. Existing Code to Reuse
- A.4's bedtime time-picker component and midnight-crossing validation logic (confirm exact module location before building a parallel implementation)
- `ControlsRepository` (from K-02, extended here with bedtime fields)
- `:core:auth::ParentGateLauncher`

## 8. Files to Create
- `feature/parental-controls/src/commonMain/kotlin/.../ui/BedtimeSettingsScreen.kt`
- `feature/parental-controls/src/commonMain/kotlin/.../viewmodel/BedtimeSettingsViewModel.kt`
- `feature/parental-controls/src/commonTest/kotlin/.../BedtimeSettingsViewModelTest.kt`

## 9. Files to Modify
- `core/data/.../repository/ControlsRepository.kt` — confirm `updateRestrictions()` already accepts bedtime fields (added in K-02); no interface change expected, only new call sites here.

## 10. KMP Requirements
- `BedtimeSettingsViewModel`: loads policy via existing `ControlsRepository.getRestrictions()`; local form state for `bedtimeStart`/`bedtimeEnd`.
- Time-picker validation: accept `start > end` as a valid overnight window (e.g., 20:00 start, 07:00 end) — must not reject this as "end before start."
- Plain-language effect description beneath the control: "New sessions won't start during this window" (per §2.1 Settings Form Visual Language).
- Save routes through `ParentGateLauncher.requireParentAuth()` before PATCH.
- Loading/saving/saved-confirmation/no-window-set empty states.

## 11. API Contract
### Required API (consumed)
- **HTTP Method:** GET/PATCH
- **Endpoint:** `/v1/children/{id}/restrictions` (bedtime fields) (B-01)
- **Request (PATCH):** `{ "bedtime_start"?: "20:00", "bedtime_end"?: "07:00" }`
- **Authentication:** Bearer (parent), step-up on PATCH

## 12. Database Requirements
N/A (no local persistence beyond cache staleness pattern, consistent with K-02).

## 13. Validation
- Both `bedtime_start` and `bedtime_end` must be provided together if either is set (avoid a half-configured window) — client-side guard before enabling Save.
- Accept and correctly serialize midnight-crossing input (e.g., 20:00/07:00) without treating it as invalid.

## 14. Authentication
Save routes through `ParentGateLauncher.requireParentAuth(Settings)`.

## 15. Authorization
N/A beyond parent-mode gate; server enforces family ownership.

## 16. Error Handling
| Scenario | UI Behavior |
|---|---|
| Only one of start/end set | Save disabled with inline hint |
| Save failure | Inline error, form retains values |
| Load failure | Error state with retry |

## 17. Offline First
Save requires connectivity; view-only from cache with staleness indicator when offline.

## 18. Local Data
Same lightweight display-only cache pattern as K-02.

## 19. Localization
Time format respects locale (12h/24h per platform convention); plain-language description text localized in EN/HI/AR/UR.

## 20. RTL
Time-picker layout mirrors correctly in RTL.

## 21. Analytics
`bedtime_policy_configured` on successful save.

## 22. Performance
Trivial form screen; no special concerns beyond standard `@Immutable` state practice.

## 23. Security
No sensitive data; relies on `ParentGateLauncher`.

## 24. Library Requirements
Jetpack Compose, Koin, `kotlinx.datetime` (`LocalTime`).

## 25. Testing
- Unit: input `20:00` start / `07:00` end accepted and correctly serialized (not treated as negative duration).
- Unit: input `09:00` start / `17:00` end (same-day window) accepted correctly.
- Unit: only-one-field-set prevents save.
- UI test: plain-language description renders correctly.

## 26. Documentation
KDoc explaining the midnight-crossing acceptance rule explicitly, referencing A.4's established precedent.

## 27. AI Coding Agent Implementation Steps

**Task 01 — Locate and Confirm A.4's Bedtime Time-Picker Component**
- Objective: Reuse rather than reimplement midnight-crossing validation logic.
- Why This Is Required: Rule 30 — avoid duplicating existing architecture; the PRD explicitly states this logic pattern is reused from A.4.

**Task 02 — Implement `BedtimeSettingsViewModel`**
- Files to Create: `viewmodel/BedtimeSettingsViewModel.kt`
- Dependencies: Task 01, `ControlsRepository` (K-02).

**Task 03 — Implement `BedtimeSettingsScreen` Composable**
- Files to Create: `ui/BedtimeSettingsScreen.kt`
- Implementation Details: Reuse A.4's time-picker component if confirmed available; wire Parent Gate before save.

**Task 04 — Add Plain-Language Effect Description**
- Implementation Details: Localized string beneath the time-picker.

**Task 05 — Add Localization Strings**

**Task 06 — Add Unit Tests**
- Files to Create: `BedtimeSettingsViewModelTest.kt`
- Coverage: midnight-crossing and same-day window serialization.

**Task 07 — Add UI Tests**

**Task 08 — Final Code Review**
- Objective: Confirm no duplicate bedtime-validation logic was written; confirm reuse of A.4's pattern.

## 28. Definition of Done
- Midnight-crossing and same-day bedtime windows both save and load correctly.
- Save always routes through the Parent Gate.
- Reuses A.4's existing validation logic rather than duplicating it.

## 29. Final Verification Checklist
- [ ] Midnight-crossing window (20:00→07:00) tested and correct
- [ ] Same-day window tested and correct
- [ ] Confirmed reuse of A.4's time-picker/validation pattern (not reimplemented)
- [ ] Save gated by Parent Gate
- [ ] Localization and RTL verified
