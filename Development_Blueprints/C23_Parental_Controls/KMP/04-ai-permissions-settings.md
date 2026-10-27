# K-04 — AI Permissions Settings

## 1. Feature Context
Lets a parent disable AI entirely, restrict voice interaction, set language limits, or choose "curated only" mode per child — every toggle here must be structurally restriction-only (PRD C.23 FR-6, FR-7, §1.18 Screen #4/#16).

## 2. Parent Feature
Feature C.23 — Parental Controls (Screen Time, Bedtime, AI Permissions, Content Age Level)

## 3. Sub-feature
2.4 AI Permissions Settings (ID: **K-04**)

## 4. Objective
Build `AiPermissionsSettingsScreen` whose ViewModel state is structurally incapable of representing "grant capability beyond default" — the absence of a restrictive toggle means "use platform default," never an explicit "grant extra" value.

## 5. Business Requirements
- FR-6: disable AI entirely, restrict voice interaction, set language limits, "curated only" mode.
- FR-7 (hard ceiling): no toggle combination may expand capability beyond the platform-wide age-band default.
- §7 Android AI Code-Generation Prompt item 4: model UI state such that no possible toggle combination serializes to a request field value outside the documented restriction-only enum/boolean space.

## 6. Existing Architecture
Module `:feature:parental-controls`. Extends `ControlsRepository` with `updateAiPermissions()` mapping to B-04's `PATCH /v1/family/children/{id}/settings` (AI fields).

## 7. Existing Code to Reuse
- `ControlsRepository` (K-02, extended)
- `:core:auth::ParentGateLauncher`
- `:core:design-system` toggle/switch components

## 8. Files to Create
- `feature/parental-controls/src/commonMain/kotlin/.../ui/AiPermissionsSettingsScreen.kt`
- `feature/parental-controls/src/commonMain/kotlin/.../ui/CuratedOnlyModeExplainer.kt`
- `feature/parental-controls/src/commonMain/kotlin/.../viewmodel/AiPermissionsSettingsViewModel.kt`
- `feature/parental-controls/src/commonMain/kotlin/.../model/AiPermissionsUiState.kt`
- `feature/parental-controls/src/commonTest/kotlin/.../AiPermissionsSettingsViewModelTest.kt`

## 9. Files to Modify
- `core/data/.../repository/ControlsRepository.kt` — add `updateAiPermissions(childId, aiEnabled?, voiceInteractionEnabled?, curatedOnlyMode?, languageLimit?)`

## 10. KMP Requirements
- `AiPermissionsUiState`: models each toggle as a **nullable boolean meaning "no override, use platform default"** vs. an explicit `false` meaning "restrict below default" — there is no representable `true`-beyond-default state in the type itself (e.g., if platform default for the age band is `false`, the UI toggle for that setting should not even render as togglable to `true`; confirm platform default via a read of the resolved effective settings, not a client-side guess).
- Fetch resolved effective AI settings (including the platform default for the child's age band) so the UI can render each toggle with the correct enabled/disabled affordance — this likely requires the settings-read response to include both "current value" and "platform ceiling" (coordinate with B-04's response shape; PRD's request/response examples show only currentvalue fields, so confirm this gap with backend before finalizing UI logic).
- "Curated Only" Mode Explainer component: static informational copy, no user input.
- Save routes through `ParentGateLauncher.requireParentAuth()`.

## 11. API Contract
### Required API (consumed)
- **HTTP Method:** PATCH (and GET for current state, via existing family/child settings read)
- **Endpoint:** `/v1/family/children/{id}/settings` (AI fields) (B-04)
- **Request:** `{ "ai_enabled"?: bool, "voice_interaction_enabled"?: bool, "curated_only_mode"?: bool, "language_limit"?: string|null }`
- **Error Responses:** 401, 403, 404, 422 (includes ceiling-violation rejection per B-04)

## 12. Database Requirements
N/A.

## 13. Validation
- Client mirrors B-04's server-side ceiling validation as a UX affordance (disable/hide toggles that would exceed default) but never as the sole enforcement — server remains authoritative; a 422 ceiling-violation response must still be handled gracefully even if the UI theoretically prevents it.

## 14. Authentication
Save routes through `ParentGateLauncher.requireParentAuth(Settings)`.

## 15. Authorization
N/A beyond parent-mode gate.

## 16. Error Handling
| Scenario | UI Behavior |
|---|---|
| Server rejects a ceiling-violating combination (422) | Inline error, revert toggle to last-known-valid state |
| Load failure | Error state with retry |
| Save failure (network) | Inline error, form retains values |

## 17. Offline First
Save requires connectivity; view current settings from cache with staleness indicator when offline.

## 18. Local Data
Lightweight display-only cache, consistent with K-02/K-03.

## 19. Localization
All toggle labels, descriptions, and the Curated Only explainer copy localized in EN/HI/AR/UR.

## 20. RTL
Toggle rows mirror correctly in RTL.

## 21. Analytics
`ai_permissions_configured` with `setting: ai_disabled|voice_restricted|curated_only|language_limit` param per changed field.

## 22. Performance
`@Immutable` state; avoid recomposition storms across the toggle group by scoping state narrowly per toggle.

## 23. Security
This screen is a defining child-safety UI surface — the structural restriction-only design is the primary client-side safety guarantee, tested explicitly (see §25).

## 24. Library Requirements
Jetpack Compose, Koin.

## 25. Testing
- Unit: enumerate all possible `AiPermissionsUiState` toggle combinations; confirm every one serializes to a request body within the documented restriction-only space (no representable "expand beyond default" value).
- Unit: server-side 422 ceiling rejection handled gracefully with toggle revert.
- UI test: toggles reflect resolved effective default correctly (once the platform-default-in-response gap from §10 is resolved with backend).

## 26. Documentation
KDoc on `AiPermissionsUiState` explaining the "nullable = platform default, explicit false = restrict further" modeling and why no "expand" value exists in the type.

## 27. AI Coding Agent Implementation Steps

**Task 01 — Resolve Platform-Default Visibility Gap**
- Objective: Confirm with backend (B-04) whether the settings-read response includes the platform's age-band default alongside the current value, or whether the client needs a separate read. Do not guess; coordinate before building the UI's enabled/disabled toggle affordances.

**Task 02 — Define `AiPermissionsUiState`**
- Files to Create: `model/AiPermissionsUiState.kt`
- Implementation Details: Structurally restriction-only per §10.

**Task 03 — Extend `ControlsRepository`**
- Files to Modify: `ControlsRepository.kt`
- Implementation Details: Add `updateAiPermissions()`.

**Task 04 — Implement `AiPermissionsSettingsViewModel`**
- Files to Create: `viewmodel/AiPermissionsSettingsViewModel.kt`
- Dependencies: Tasks 01–03.

**Task 05 — Implement `AiPermissionsSettingsScreen` Composable**
- Files to Create: `ui/AiPermissionsSettingsScreen.kt`

**Task 06 — Implement `CuratedOnlyModeExplainer` Component**
- Files to Create: `ui/CuratedOnlyModeExplainer.kt`

**Task 07 — Add Localization Strings**

**Task 08 — Add Exhaustive Toggle-Combination Unit Test**
- Files to Create: `AiPermissionsSettingsViewModelTest.kt`
- Objective: The single highest-priority test on this screen — enumerate and assert every combination.

**Task 09 — Add 422-Rejection-Handling Test**

**Task 10 — Final Code Review**
- Objective: Confirm no toggle in the actual rendered UI can represent an "expand beyond default" state under any circumstance.

## 28. Definition of Done
- Every toggle combination verified structurally restriction-only.
- Server-side ceiling rejection handled gracefully.
- Platform-default visibility gap resolved with backend before UI ships.

## 29. Final Verification Checklist
- [ ] Platform-default data source confirmed with backend (not guessed)
- [ ] Exhaustive toggle-combination test passes
- [ ] 422 ceiling-rejection handled gracefully in UI
- [ ] Curated Only explainer renders correctly
- [ ] Save gated by Parent Gate
- [ ] Localization and RTL verified
