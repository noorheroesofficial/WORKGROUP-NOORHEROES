# K-02 — Screen-Time Settings & Usage Display

## 1. Feature Context
Lets a parent configure a daily screen-time limit and warning threshold for a specific child, with the current day's usage shown for context (PRD C.23 §2.2 "Screen Time Settings", §1.18 Screen #2).

## 2. Parent Feature
Feature C.23 — Parental Controls (Screen Time, Bedtime, AI Permissions, Content Age Level)

## 3. Sub-feature
2.2 Screen-Time Settings & Usage Display (ID: **K-02**)

## 4. Objective
Build `ScreenTimeSettingsScreen` with a daily-limit time-picker/slider, warning-threshold dropdown, and current-usage-today indicator, saving through `ControlsRepository.updateRestrictions()` gated by `ParentGateLauncher.requireParentAuth()`.

## 5. Business Requirements
- FR-1, FR-2: Screen Time is a canonical Controls section; policy load happens at child session start (read side owned here for display, enforcement owned by K-07).
- §2.2: daily limit time-picker/slider, warning-threshold configuration, current-usage-today indicator.
- §1.12 Empty State: no policy configured → explicit "no limit set" indicator, never ambiguous blank field.
- Edge Case 10: a 0-minute limit is a valid, acceptable configuration with no special warning beyond standard save confirmation.

## 6. Existing Architecture
Module `:feature:parental-controls`. Depends on `:core:auth` (`ParentGateLauncher.requireParentAuth(Settings)`), `:core:data` (new `ControlsRepository` interface + impl in `:core:data`), `:core:network`.

## 7. Existing Code to Reuse
- `:core:auth::ParentGateLauncher.requireParentAuth()`
- `:core:common::NoorResult<T>`/`Outcome` error handling pattern
- `:core:common::LocalDateProvider.currentFamilyLocalDate()` (for "today" usage display, never raw device clock)
- `:core:design-system` time-picker/slider components (confirm exact names before inventing new ones)

## 8. Files to Create
- `core/data/src/commonMain/kotlin/.../repository/ControlsRepository.kt` (interface) + `ControlsRepositoryImpl.kt`
- `feature/parental-controls/src/commonMain/kotlin/.../ui/ScreenTimeSettingsScreen.kt`
- `feature/parental-controls/src/commonMain/kotlin/.../viewmodel/ScreenTimeSettingsViewModel.kt`
- `feature/parental-controls/src/commonMain/kotlin/.../model/ScreenTimePolicyUiState.kt`
- `feature/parental-controls/src/commonTest/kotlin/.../ScreenTimeSettingsViewModelTest.kt`

## 9. Files to Modify
- `core/data/src/commonMain/kotlin/.../di/RepositoryModule.kt` — register `ControlsRepository`
- `core/network/.../ApiService.kt` (or equivalent) — add `getRestrictions()`/`updateRestrictions()` calls to `GET/PATCH /v1/children/{id}/restrictions` (B-01)

## 10. KMP Requirements
- `ControlsRepository.getRestrictions(childId): NoorResult<RestrictionsPolicy>` — maps B-01's response DTO to the domain model.
- `ControlsRepository.updateRestrictions(childId, dailyLimitMinutes?, warningThresholdMinutes?): NoorResult<RestrictionsPolicy>`.
- `ScreenTimeSettingsViewModel`: loads policy on init; on save, calls `ParentGateLauncher.requireParentAuth()` first, then on success calls `updateRestrictions()`; exposes `UiState` (`Loading`, `Loaded(policy, usageToday)`, `Saving`, `SavedConfirmation`, `Error`).
- Current-usage-today value: **resolved** — B-01's `GET /v1/children/{id}/restrictions` response now includes a read-only `minutes_used_today` field (sourced server-side from B-02's `screen_time_usage_daily`, always present as a non-null integer, `0` if no usage yet today). No separate call needed; `getRestrictions()` returns both policy and today's usage in one response.
- No-limit-set state renders an explicit "No limit set" label, not a blank/zero field.
- `daily_limit_minutes = 0` renders and saves correctly with standard confirmation (no special-case warning UI).

## 11. API Contract
### Required API (consumed)
- **HTTP Method:** GET/PATCH
- **Endpoint:** `/v1/children/{id}/restrictions` (B-01)
- **Request (PATCH):** `{ "daily_limit_minutes"?: int, "warning_threshold_minutes"?: int }`
- **Response:** `{ "daily_limit_minutes": int|null, "warning_threshold_minutes": int|null, "bedtime_start": "...", "bedtime_end": "...", "minutes_used_today": int, "updated_at": "..." }`
- **Authentication:** Bearer (parent)
- **Authorization:** family ownership, step-up on PATCH
- **Error Responses:** 401, 403, 404, 422 (per B-01)

## 12. Database Requirements
N/A — no local persistence beyond in-memory ViewModel state and standard offline-cache staleness indicator (§17).

## 13. Validation
- Client-side pre-validates `daily_limit_minutes >= 0` and `warning_threshold_minutes <= daily_limit_minutes` before enabling Save, mirroring B-01's server-side rules (defense in depth, not a replacement for server validation).

## 14. Authentication
Every save routes through `ParentGateLauncher.requireParentAuth(Settings)` before the PATCH call fires.

## 15. Authorization
N/A beyond parent-mode gate; server enforces family ownership.

## 16. Error Handling
| Scenario | UI Behavior |
|---|---|
| Load failure | `Error` state with retry |
| Save failure (network) | Inline error, form retains entered values |
| Save failure (422 validation) | Inline field-level error message |
| Step-up cancelled by parent | Return to form unsaved, no error toast (user-initiated cancellation) |

## 17. Offline First
Controls configuration screens require connectivity to save (server-authoritative, per PRD §1.14); viewing current settings may render from cache with a staleness indicator (e.g., "last updated X ago, may be outdated").

## 18. Local Data
Optional lightweight cache of the last-loaded policy in `:core:datastore` (via `PreferenceManager`, not `core-database`, since this is small non-relational data) for the staleness-indicator offline view — not authoritative, display-only.

## 19. Localization
All labels, the plain-language effect description ("New sessions won't start during this window" — bedtime-specific, but the equivalent screen-time description belongs here), and the no-limit-set text sourced from string resources in EN/HI/AR/UR.

## 20. RTL
Time-picker/slider and usage indicator must mirror correctly in RTL locales.

## 21. Analytics
`screen_time_policy_configured` on successful save.

## 22. Performance
`@Immutable` UI state class; avoid recomposition on every keystroke in the slider by debouncing local state before triggering any derived calculation.

## 23. Security
No sensitive data handled directly; relies entirely on `ParentGateLauncher`'s existing step-up flow.

## 24. Library Requirements
Jetpack Compose, Koin, Ktor (via `core-network`), `kotlinx.datetime`.

## 25. Testing
- Unit: ViewModel state transitions (Loading → Loaded → Saving → SavedConfirmation).
- Unit: `daily_limit_minutes = 0` accepted and displayed without special-case warning.
- Unit: no-limit-set state renders correctly when policy fields are null.
- UI test: save flow requires and correctly routes through `ParentGateLauncher`.
- UI test: RTL layout for slider/time-picker.

## 26. Documentation
KDoc on `ControlsRepository` documenting the mapping between domain model and B-01's wire contract.

## 27. AI Coding Agent Implementation Steps

**Task 01 — Define `ControlsRepository` Interface**
- Files to Create: `core/data/.../repository/ControlsRepository.kt`

**Task 02 — Implement `ControlsRepositoryImpl`**
- Files to Create: `ControlsRepositoryImpl.kt`
- Dependencies: `:core:network` API client wired to B-01's endpoints.

**Task 03 — Add Network Layer Calls**
- Files to Modify: network API service interface — add `getRestrictions`/`updateRestrictions`.

**Task 04 — Map `minutes_used_today` from B-01's Response**
- Objective: Extend the DTO→domain mapping in `ControlsRepositoryImpl` to surface `minutes_used_today` directly from `getRestrictions()`'s response — no supplementary call needed (resolved; see §10).

**Task 05 — Define `ScreenTimePolicyUiState`**
- Files to Create: `model/ScreenTimePolicyUiState.kt`
- Implementation Details: `@Immutable` sealed state class.

**Task 06 — Implement `ScreenTimeSettingsViewModel`**
- Files to Create: `viewmodel/ScreenTimeSettingsViewModel.kt`
- Dependencies: Tasks 01–05.

**Task 07 — Implement `ScreenTimeSettingsScreen` Composable**
- Files to Create: `ui/ScreenTimeSettingsScreen.kt`
- Implementation Details: Wire to `ParentGateLauncher` before invoking save.

**Task 08 — Add Localization Strings**

**Task 09 — Add Unit Tests**
- Files to Create: `ScreenTimeSettingsViewModelTest.kt`

**Task 10 — Add UI Tests**

**Task 11 — Final Code Review**

## 28. Definition of Done
- Screen loads, displays, and saves policy correctly including the 0-minute and no-limit-set edge cases.
- Save always routes through the Parent Gate.
- Fully localized and RTL-correct.

## 29. Final Verification Checklist
- [ ] Load/save flows tested including error paths
- [ ] 0-minute limit handled without special-case warning
- [ ] No-limit-set state explicit, never blank
- [ ] Save gated by `ParentGateLauncher`
- [ ] `minutes_used_today` correctly mapped from B-01's response and displayed
- [ ] RTL and localization verified
