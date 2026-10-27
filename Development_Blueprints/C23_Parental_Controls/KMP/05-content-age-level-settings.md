# K-05 — Content Age Level Settings

## 1. Feature Context
Lets a parent override a child's system-derived age-band content eligibility in either direction, above or below the DOB-derived default (PRD C.23 FR-8, Edge Case 8, §1.18 Screen #5/#17).

## 2. Parent Feature
Feature C.23 — Parental Controls (Screen Time, Bedtime, AI Permissions, Content Age Level)

## 3. Sub-feature
2.5 Content Age Level Settings (ID: **K-05**)

## 4. Objective
Build `ContentAgeLevelSettingsScreen` with a band-selection control and confirmation modal, saving the override via `ControlsRepository.updateContentAgeLevel()`, gated by the Parent Gate.

## 5. Business Requirements
- FR-8: override adjusts the eligible band itself; downstream systems respect it exactly as the DOB-derived default.
- Edge Case 8: override below DOB-derived band fully supported, symmetric to above-band overrides — no asymmetric restriction on direction.

## 6. Existing Architecture
Module `:feature:parental-controls`. Extends `ControlsRepository` with `updateContentAgeLevel()` mapping to B-04's content fields.

## 7. Existing Code to Reuse
- `ControlsRepository` (K-02/K-04, extended)
- `:core:common::model::ChildProfile.ageBand` (existing `AgeBand` enum: `4 to 6`, `6 to 9`, `9 to 12`, `12 to 15`, `15 to 18+`) — reuse this exact enum, do not define a parallel one
- `:core:auth::ParentGateLauncher`

## 8. Files to Create
- `feature/parental-controls/src/commonMain/kotlin/.../ui/ContentAgeLevelSettingsScreen.kt`
- `feature/parental-controls/src/commonMain/kotlin/.../ui/ContentAgeLevelOverrideConfirmationModal.kt`
- `feature/parental-controls/src/commonMain/kotlin/.../viewmodel/ContentAgeLevelSettingsViewModel.kt`
- `feature/parental-controls/src/commonTest/kotlin/.../ContentAgeLevelSettingsViewModelTest.kt`

## 9. Files to Modify
- `core/data/.../repository/ControlsRepository.kt` — add `updateContentAgeLevel(childId, override: AgeBand?)`

## 10. KMP Requirements
- `ContentAgeLevelSettingsViewModel`: loads the child's DOB-derived default band and any active override; displays both distinctly ("Default for age: 6 to 9" vs. "Currently set to: 4 to 6 (override)").
- Band-selection control lists all `AgeBand` values without restricting direction (confirm the exact enum/display range against `:core:common::model` — do not invent new band labels).
- Save opens `ContentAgeLevelOverrideConfirmationModal` before committing, per PRD §1.18 Screen #17.
- Save routes through `ParentGateLauncher.requireParentAuth()`.
- "Clear override" action resets to DOB-derived default.

## 11. API Contract
### Required API (consumed)
- **HTTP Method:** PATCH
- **Endpoint:** `/v1/family/children/{id}/settings` (content fields) (B-04)
- **Request:** `{ "content_age_level_override"?: "6 to 9" | null }`
- **Error Responses:** 401, 403, 404, 422 (invalid band value)

## 12. Database Requirements
N/A.

## 13. Validation
- Selected band must be one of the platform's defined `AgeBand` enum values — client-side selection control inherently constrains this (no free-text entry).

## 14. Authentication
Save routes through `ParentGateLauncher.requireParentAuth(Settings)`.

## 15. Authorization
N/A beyond parent-mode gate.

## 16. Error Handling
| Scenario | UI Behavior |
|---|---|
| Save failure | Inline error, modal remains open with selection preserved |
| Load failure | Error state with retry |

## 17. Offline First
Save requires connectivity; view current override from cache with staleness indicator when offline.

## 18. Local Data
Lightweight display-only cache, consistent with prior settings screens.

## 19. Localization
Age-band labels and the confirmation modal copy localized in EN/HI/AR/UR.

## 20. RTL
Band-selection control and modal mirror correctly in RTL.

## 21. Analytics
`content_age_level_overridden` on successful save.

## 22. Performance
Trivial form screen.

## 23. Security
No sensitive data; relies on `ParentGateLauncher`. Confirms client never bypasses the platform's hard age-band-exclusion filters elsewhere — this screen only ever sets the eligible band, never a content-safety bypass flag.

## 24. Library Requirements
Jetpack Compose, Koin.

## 25. Testing
- Unit: override below DOB-derived band accepted and saved identically to an above-band override (symmetric handling).
- Unit: "clear override" correctly resets to null/DOB-derived default.
- UI test: confirmation modal appears before save commits.

## 26. Documentation
KDoc noting explicitly that this screen adjusts the eligible band only, and that downstream content-filtering (B.13, A.5) must treat the override identically to the DOB-derived default — no special-casing anywhere else in the app.

## 27. AI Coding Agent Implementation Steps

**Task 01 — Confirm `AgeBand` Enum Values**
- Objective: Reuse the exact existing `core-common::model::AgeBand` enum; do not define a parallel band representation.

**Task 02 — Extend `ControlsRepository`**
- Files to Modify: `ControlsRepository.kt`
- Implementation Details: Add `updateContentAgeLevel()`.

**Task 03 — Implement `ContentAgeLevelSettingsViewModel`**
- Files to Create: `viewmodel/ContentAgeLevelSettingsViewModel.kt`
- Dependencies: Task 01, 02.

**Task 04 — Implement `ContentAgeLevelSettingsScreen` Composable**
- Files to Create: `ui/ContentAgeLevelSettingsScreen.kt`

**Task 05 — Implement Override Confirmation Modal**
- Files to Create: `ui/ContentAgeLevelOverrideConfirmationModal.kt`

**Task 06 — Add "Clear Override" Action**

**Task 07 — Add Localization Strings**

**Task 08 — Add Unit Tests**
- Files to Create: `ContentAgeLevelSettingsViewModelTest.kt`
- Coverage: symmetric above/below-band override handling.

**Task 09 — Add UI Tests**

**Task 10 — Final Code Review**
- Objective: Confirm no parallel age-band enum was introduced; confirm this screen never touches any hard content-safety-filter flag directly.

## 28. Definition of Done
- Override works symmetrically in both directions.
- Confirmation modal gates every save.
- Reuses the platform's existing `AgeBand` enum exactly.

## 29. Final Verification Checklist
- [ ] Reuses existing `AgeBand` enum, no duplicate defined
- [ ] Above-band and below-band overrides both tested
- [ ] Confirmation modal required before save
- [ ] Clear-override action tested
- [ ] Save gated by Parent Gate
- [ ] Localization and RTL verified
