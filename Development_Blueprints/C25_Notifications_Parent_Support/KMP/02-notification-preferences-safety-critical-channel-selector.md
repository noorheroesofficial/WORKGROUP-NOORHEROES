# Blueprint: Notification Preferences & Safety-Critical Channel Selector

## 1. Feature Context
Platform: NoorHeroes KMP App. Same module as K-01: `:feature:parent-notifications-support`. This blueprint delivers the client half of the feature's core guarantee (server half is B-02): a safety-critical category must render as non-fully-disableable, driven **entirely** by server data, never a client-side hardcoded category list.

## 2. Parent Feature
C.25 — Notifications (Parent) & Support.

## 3. Sub-feature
K-02 — Notification Preferences & Safety-Critical Channel Selector.

## 4. Objective
Build `NotificationPreferencesScreen` and `NotificationPreferencesViewModel` that render each category's control (simple toggle vs. channel-selector) based exclusively on the server's `safety_critical` boolean field for that category — with zero hardcoded category-name checks anywhere in this screen's source.

## 5. Business Requirements
Source: PRD §6.4, §6.10; §2.2 Screen-Level Design (Notification Preferences); §7 Android AI Code-Generation Prompt items 1–2.
- "`NotificationPreferencesViewModel` renders safety-critical categories with a distinct UI component (a channel-selector, never a simple toggle) derived from the server's `safety_critical` flag on each category — the client never hardcodes which categories are safety-critical" (§6.4) — this is the platform's explicit anti-hardcoding requirement, structurally testable.
- The distinction between a true on/off toggle and a channel-selector-only control is conveyed via both visual styling and accessible label text ("Safety alerts: always on, choose delivery method"), never ambiguous to a screen-reader user (§2.2 Accessibility).
- The channel-selector must disallow submitting an empty channel selection client-side, mirroring — but not replacing — the backend's own authoritative validation (§7 item 2).
- Category list grouped System/Safety/Marketing (§2.2 Components); quiet-hours time-range picker applies only to non-safety-critical categories.

## 6. Existing Architecture
Same as K-01 (`CORE_NOTIFICATIONS_INSTRUCTIONS.md`, `core-data`/`core-common` patterns referenced but not re-read this pass — confirm exact class names before implementation). Shares the `:feature:parent-notifications-support` module and its Koin DI root (`ParentNotificationsSupportModule`, established in K-01) rather than creating a second DI module for the same feature.

## 7. Existing Code to Reuse
- `AuthStateProvider` for session derivation (no externally-supplied `family_id`).
- `NoorResult<T>` for repository calls.
- `BaseViewModel`, `Route` pattern (`:core:navigation`).
- Design tokens, Parent-Mode formal visual register (`:core:design-system`), specifically whatever safety-critical visual-distinction tokens (e.g., a "Required"/"Safety" tag component) already exist or are newly defined per this feature's UX spec (§2.1: "a small 'Required' or 'Safety' tag... the toggle replaced by a channel-selector control").
- K-01's Koin module (`ParentNotificationsSupportModule`) — add this screen's dependencies to the same module rather than duplicating DI setup.

## 8. Files to Create
- `feature/parent-notifications-support/src/commonMain/kotlin/.../NotificationPreferencesRoute.kt`
- `feature/parent-notifications-support/src/commonMain/kotlin/.../NotificationPreferencesScreen.kt`
- `feature/parent-notifications-support/src/commonMain/kotlin/.../NotificationPreferencesViewModel.kt`
- `feature/parent-notifications-support/src/commonMain/kotlin/.../NotificationPreferencesUiState.kt`
- `feature/parent-notifications-support/src/commonMain/kotlin/.../NotificationPreferencesRepository.kt` (interface)
- `feature/parent-notifications-support/src/commonMain/kotlin/.../components/CategoryChannelSelector.kt` (channel-selector control)
- `feature/parent-notifications-support/src/commonMain/kotlin/.../components/QuietHoursPicker.kt`
- `feature/parent-notifications-support/src/commonTest/kotlin/.../NotificationPreferencesViewModelTest.kt`
- `feature/parent-notifications-support/src/commonTest/kotlin/.../SafetyCriticalControlRenderingTest.kt`

## 9. Files to Modify
- `di/ParentNotificationsSupportModule.kt` (K-01) — register this blueprint's ViewModel/repository.
- Navigation graph — register `NotificationPreferencesRoute`, reachable from `NotificationsInboxScreen` (K-01) and Settings.

## 10. KMP Requirements
- `Route`: `@Serializable data object NotificationPreferencesRoute : Route { override val requiredAuthState = /* same parent-authenticated class as K-01 */; override val analyticsName = "parent_notification_preferences" }`.
- `NotificationPreferencesUiState`: `categories: List<CategoryPreferenceState>` where each `CategoryPreferenceState` carries `category: String`, `displayNameKey: String` (localization key, resolved client-side from the category code — do not accept display strings from the server; resolve via a category-code-to-localization-key mapping that itself may need a fallback/"unknown category" default rather than crashing on an unrecognized future code), `safetyCritical: Boolean`, `enabled: Boolean`, `channels: List<Channel>`, `quietHours: QuietHours?`. All `@Immutable`/`@Stable`.
- `NotificationPreferencesViewModel(preferencesRepository: NotificationPreferencesRepository, authStateProvider: AuthStateProvider, dispatchers: DispatcherProvider) : BaseViewModel()`.
- Rendering rule (the core guarantee): the Composable layer selects `Toggle` vs. `CategoryChannelSelector` purely by reading `category.safetyCritical` from the fetched state — **no** `if (category == "billing_failure")`-style branch anywhere in this module.
- `toggleCategory(category, enabled)`: client-side guard — if `category.safetyCritical && enabled == false`, do not call the repository; instead surface the "Safety alerts: always on" messaging inline and fire `safety_critical_category_disable_attempt_blocked` (this is a UX affordance, not a security boundary — the backend's `422` remains authoritative for any path that bypasses this client check).
- `updateChannels(category, channels)`: client-side guard — if `category.safetyCritical && channels.isEmpty()`, disable/reject the Save action rather than submitting.
- `updateQuietHours(category, range)`: only invocable for non-safety-critical categories (control not rendered at all for safety-critical ones).

## 11. Files to Create — Screen Composable
`NotificationPreferencesScreen`: category list grouped under "Safety & Account" and "Marketing" section headers; each row renders either a standard toggle switch (non-safety-critical) or `CategoryChannelSelector` with a "Required"/"Safety" tag (safety-critical); quiet-hours picker shown only for non-safety-critical rows; Default/Saving/Saved-confirmation states per row or globally (confirm UX granularity against the Figma when available — default to per-row saving indicators for the clearest feedback).

## 12. NextJS Requirements
N/A.

## 13. API Contract
Consumes `GET/PATCH /v1/parent/notification-preferences` (B-02) via `NotificationPreferencesRepository.getPreferences(): NoorResult<List<CategoryPreference>>` / `updatePreference(category, enabled, channels, quietHours): NoorResult<CategoryPreference>`, surfacing the backend's `422 SAFETY_CRITICAL_CANNOT_DISABLE` error distinctly (mapped to a specific `AppError` subtype the ViewModel can pattern-match on to show the correct inline messaging, separate from generic network/validation errors).

## 14. Database Requirements
No local persistence required for this screen's own data (preferences are always fetched fresh on screen entry; unlike K-01's inbox, offline caching is not a stated requirement here per PRD §1.14, which scopes offline behavior to the inbox specifically) — confirm this scoping is correct before assuming preferences load only online; if preferences must also render from cache offline, this needs a Room-backed repository mirroring K-01's Task 04 pattern, added as an amendment rather than assumed here.

## 15. Validation
Client-side pre-submission checks (safety-critical disable attempt, empty-channels attempt) are UX conveniences only; the server (B-02) remains the authoritative validation boundary — this screen must correctly surface a server-side `422` even if a client-side check is somehow bypassed or has a gap.

## 16. Authentication
Reachable only via an authenticated parent session.

## 17. Authorization
Family/parent scope derived exclusively from `:core:auth`.

## 18. Error Handling
- `422 SAFETY_CRITICAL_CANNOT_DISABLE` from the server → inline messaging distinct from generic save-failure ("Safety alerts can't be turned off — choose a delivery method instead"), never a raw/generic error toast for this specific case.
- Generic save failure (network) → standard retry affordance, does not lose the user's in-progress selection.
- Fetch failure on screen entry → standard error state with retry.

## 19. Offline First
Per §14 — confirm scope before implementation; default assumption is preferences require connectivity to view/edit (consistent with the PRD's explicit offline-first callout being scoped to the inbox only).

## 20. Local Data
N/A unless the §14 scoping question resolves to "yes, cache preferences too."

## 21. Localization
All category display names, section headers, the "Required"/"Safety" tag text, and accessible labels resolved via localization keys — category codes themselves are never displayed raw; support English/Hindi/Arabic/Urdu.

## 22. RTL
Toggle/channel-selector rows, section headers, and the safety tag must mirror correctly in RTL.

## 23. Analytics
`notification_preferences_viewed`, `notification_category_toggled`, `notification_quiet_hours_set`, `safety_critical_category_disable_attempt_blocked` (§1.19) — the last fires both on client-side interception and (if distinguishable) on a server-side `422` bounce-back, giving product visibility into how often parents attempt this regardless of which layer catches it.

## 24. Performance
`@Immutable`/`@Stable` state per category row to avoid list-wide recomposition on a single row's save-state change; per-row (not global) saving indicators support this.

## 25. Security
No security-relevant logic on the client beyond UX — the actual guarantee lives in B-02's server-side enforcement; this screen must never claim or imply it is itself the security boundary in code comments or logic structure.

## 26. Library Requirements
No new third-party libraries.

## 27. Testing
1. **UI test (mandatory, highest priority):** using two fixture categories, one `safetyCritical=true` and one `false`, assert the correct distinct control type (channel-selector vs. toggle) renders for each — with no hardcoded category-name checks anywhere in the screen's source (§7 item 1; verify via code review/lint if a structural test isn't feasible for UI-layer branching, otherwise a thorough behavioral test covering this exact distinction across multiple fixture category codes, including a hypothetical unseen-before code, to prove the logic branches on the flag, not the name).
2. UI test: attempting to submit an empty channel selection for a safety-critical category disables/rejects the Save action client-side (§7 item 2).
3. UI test: attempting to toggle a safety-critical category off surfaces the "Safety alerts: always on" messaging inline rather than silently failing.
4. Unit test: a `422 SAFETY_CRITICAL_CANNOT_DISABLE` server response is correctly mapped to the distinct inline-messaging error path.
5. Unit test: quiet-hours control is not rendered/available for safety-critical categories.
6. Accessibility test: screen-reader label text correctly distinguishes toggle vs. channel-selector rows.
7. UI test: RTL layout preview for category rows and the safety tag.

## 28. Documentation
KDoc on `NotificationPreferencesViewModel` explicitly stating the anti-hardcoding constraint ("this screen must never branch on a specific category code — always on `safetyCritical`") citing PRD §6.4/§7 item 1.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Route and UiState Models**
- Task ID: K02-T01
- Objective: Type-safe navigation destination and server-driven state model.
- Why This Is Required: Foundation, and the place where the anti-hardcoding contract is established at the type level.
- Existing Architecture to Follow: `Route` pattern; K-01's state-modeling style.
- Existing Files to Reuse: `Route`, `BaseAuthState`.
- Files to Create: `NotificationPreferencesRoute.kt`, `NotificationPreferencesUiState.kt`.
- Files to Modify: none.
- Implementation Details: `CategoryPreferenceState` carries `safetyCritical: Boolean` as the single source of truth for rendering branch logic; no companion "known safety-critical codes" list anywhere.
- Business Rules: §6.4.
- Validation: N/A.
- Error Handling: N/A.
- Security: N/A.
- Performance: `@Immutable` classes.
- Localization: `displayNameKey` resolved separately, not server-supplied display text.
- RTL: N/A.
- Analytics: `analyticsName = "parent_notification_preferences"`.
- Tests: Covered in Task 05.
- Documentation: KDoc.
- Dependencies: None.
- Do Not Change: N/A.
- Expected Result: Types compile.
- Definition of Done: `CategoryPreferenceState` has no category-name-keyed fields/lists.

**Task 02 — Define NotificationPreferencesRepository Interface**
- Task ID: K02-T02
- Objective: Data-access contract.
- Why This Is Required: Decouples ViewModel from network implementation; models the distinct `422` error type.
- Existing Architecture to Follow: `core-data` repository interface pattern; `NoorResult<T>`.
- Existing Files to Reuse: `NoorResult<T>`, `AppError` hierarchy.
- Files to Create: `NotificationPreferencesRepository.kt` (interface).
- Files to Modify: none.
- Implementation Details: `interface NotificationPreferencesRepository { suspend fun getPreferences(): NoorResult<List<CategoryPreference>>; suspend fun updatePreference(category: String, enabled: Boolean?, channels: List<Channel>?, quietHours: QuietHours?): NoorResult<CategoryPreference> }`; map the backend's `422 SAFETY_CRITICAL_CANNOT_DISABLE` to a distinct `AppError.SafetyCriticalCannotDisable` subtype.
- Business Rules: §6.4.
- Validation: N/A.
- Error Handling: Distinct error subtype for the safety-critical rejection.
- Security: N/A.
- Performance: N/A.
- Localization: N/A.
- RTL: N/A.
- Analytics: N/A.
- Tests: Covered in Task 05.
- Documentation: KDoc.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Interface compiles.
- Definition of Done: Distinct error type modeled correctly.

**Task 03 — Implement NotificationPreferencesViewModel**
- Task ID: K02-T03
- Objective: State management with client-side UX guards.
- Why This Is Required: Central orchestrator.
- Existing Architecture to Follow: `BaseViewModel`, `AuthStateProvider`, `DispatcherProvider`.
- Existing Files to Reuse: `BaseViewModel`, `AuthStateProvider`, `DispatcherProvider`.
- Files to Create: `NotificationPreferencesViewModel.kt`.
- Files to Modify: none.
- Implementation Details: Per §10; client-side guards for disable-attempt and empty-channels, both clearly UX-layer only.
- Business Rules: §6.4, §7 items 1–2.
- Validation: Client-side pre-checks, server remains authoritative.
- Error Handling: `AppError.SafetyCriticalCannotDisable` mapped to distinct UI messaging.
- Security: N/A (UX layer; real boundary is server-side).
- Performance: `@Stable` state.
- Localization: N/A (ViewModel has no strings).
- RTL: N/A.
- Analytics: Fire the 4 events per §23.
- Tests: Covered in Task 05.
- Documentation: KDoc, author tag, anti-hardcoding note per §28.
- Dependencies: Tasks 01–02.
- Do Not Change: N/A.
- Expected Result: ViewModel functional against a fake repository.
- Definition of Done: All Task 05 tests pass.

**Task 04 — Implement CategoryChannelSelector and QuietHoursPicker Components**
- Task ID: K02-T04
- Objective: The visually-distinct safety-critical control and the quiet-hours picker.
- Why This Is Required: Core UX deliverable proving the toggle-vs-selector distinction.
- Existing Architecture to Follow: `:core:design-system` component conventions — confirm exact primitive component names before use.
- Existing Files to Reuse: Design-system dropdown/multi-select and time-range-picker primitives if they exist.
- Files to Create: `components/CategoryChannelSelector.kt`, `components/QuietHoursPicker.kt`.
- Files to Modify: none.
- Implementation Details: `CategoryChannelSelector` shows a "Required"/"Safety" tag plus a channel dropdown/multi-select (never a boolean toggle) with Save disabled when zero channels selected; accessible label text per §2.2.
- Business Rules: §2.1, §2.2 Accessibility.
- Validation: Empty-channel-selection guard.
- Error Handling: N/A (presentational).
- Security: N/A.
- Performance: N/A.
- Localization: All labels via localization keys.
- RTL: Mirrors correctly.
- Analytics: N/A.
- Tests: Covered in Task 05.
- Documentation: KDoc.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Components render correctly and are reusable.
- Definition of Done: Matches §2.2 exactly.

**Task 05 — Implement Screen Composable and Write Test Suite**
- Task ID: K02-T05
- Objective: Full screen assembly and test coverage, including the mandatory anti-hardcoding UI test.
- Why This Is Required: Core deliverable and PRD's top-priority test for this sub-feature.
- Existing Architecture to Follow: `:core:design-system` tokens, Parent-Mode visual register; Compose UI testing conventions.
- Existing Files to Reuse: Design-system section-header/card components.
- Files to Create: `NotificationPreferencesScreen.kt`, `NotificationPreferencesViewModelTest.kt`, `SafetyCriticalControlRenderingTest.kt`.
- Files to Modify: `di/ParentNotificationsSupportModule.kt`, navigation graph.
- Implementation Details: Per §11 and §27 (7 test cases, with case 1 as the mandatory structural/behavioral centerpiece).
- Business Rules: §2.2.
- Validation: N/A.
- Error Handling: Per-row error/saving states.
- Security: Test 1 is the security/trust-critical test for this blueprint.
- Performance: Per-row `@Stable` state.
- Localization: All strings via localization package.
- RTL: Layout mirrors correctly.
- Analytics: N/A (fired from ViewModel).
- Tests: This task includes the tests.
- Documentation: KDoc.
- Dependencies: Tasks 01–04.
- Do Not Change: N/A.
- Expected Result: Screen renders correctly; all 7 tests pass.
- Definition of Done: 100% of §27 green, including the multi-fixture-category rendering test.

## 30. Definition of Done
`NotificationPreferencesScreen`/`NotificationPreferencesViewModel` live, rendering toggle-vs-channel-selector purely from the server's `safety_critical` flag with zero hardcoded category logic anywhere, client-side UX guards mirroring (not replacing) B-02's server-side validation, all tests green.

## 31. Final Verification Checklist
- [ ] No hardcoded category-name checks anywhere in this module's source (code-reviewed and test-verified)
- [ ] Channel-selector renders for `safetyCritical=true`, toggle for `false` (tested with fixture data)
- [ ] Save blocked client-side on empty-channel selection for safety-critical categories
- [ ] Server `422 SAFETY_CRITICAL_CANNOT_DISABLE` surfaces distinct, clear inline messaging
- [ ] Accessible labels distinguish control types for screen readers
- [ ] All state classes `@Immutable`/`@Stable`
- [ ] No hardcoded strings; RTL layout verified
