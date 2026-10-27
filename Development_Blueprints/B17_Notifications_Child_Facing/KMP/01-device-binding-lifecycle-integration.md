# K-01 — Device Binding Lifecycle Integration

## 1. Feature Context
Part of Feature B.17 — Notifications (Child-Facing). Firebase issues one token per app installation, not per child; the client's responsibility is to ensure the backend's exclusive active-profile binding (B-01) is always kept in sync with whichever profile is actually active, with zero forgettable/skippable code paths (FR-8/FR-9).

## 2. Parent Feature
B.17 Notifications (Child-Facing) — KMP App (Android/iOS)

## 3. Sub-feature
K-01 Device Binding Lifecycle Integration

## 4. Objective
Implement `DeviceBindingManager` inside the shared `:core:notifications`/`:core:auth` layer so that every profile-switch transition (Child A → Child B, Child → Parent, Parent → Child, logout) bundles a call to `PATCH /v1/devices/{id}/active-profile` as part of the same transition, never a separate, forgettable step.

## 5. Business Requirements
- The binding update is bundled into the existing session/state-clearing transition flow already established in A.1/B.16 — not a separate, easily-forgotten extra step (PRD §6.4).
- Two devices belonging to the same family may have independent bindings; logout revokes all bindings for that session/device (FR-9).
- A device with no active binding (e.g., immediately post-logout, before a new profile is selected) is the expected, safe default state.

## 6. Existing Architecture
- Extends `core-notifications` module (`com.noorheroes.core.notifications.handler` / `.di`) per `CORE_NOTIFICATIONS_INSTRUCTIONS.md` — `NotificationHandler` interface and `NoOpNotificationHandler` already exist; `DeviceBindingManager` is new but must follow the same DI/Koin injection pattern (`notificationsModule`, platform-specific overrides).
- Token retrieval uses the existing `NotificationHandler.getPushToken()` suspend function — do not access `FirebaseMessaging`/`UNUserNotificationCenter` directly from shared code (hard rule per `CORE_NOTIFICATIONS_INSTRUCTIONS.md` §7).
- Must be invoked from within `:core:auth`'s existing session-switch suspend function/transaction-equivalent, per PRD §6.4.

## 7. Existing Code to Reuse
- `NotificationHandler.getPushToken()`.
- `:core:auth`'s existing profile-switch/session-clearing flow (A.1/B.16).
- `notificationsModule` Koin DI setup.

## 8. Files to Create
- `core-notifications/src/commonMain/kotlin/.../binding/DeviceBindingManager.kt` — `switchActiveProfile(target: BindingTarget)`.
- `core-notifications/src/commonMain/kotlin/.../binding/DeviceBindingRepository.kt` — `registerToken()`, `updateActiveProfile()`.
- `core-notifications/src/commonMain/kotlin/.../binding/BindingTarget.kt` — sealed class (`Parent`, `Child(childId)`, `None`).
- `core-notifications/src/commonTest/kotlin/.../binding/DeviceBindingManagerTest.kt`.

## 9. Files to Modify
- `:core:auth`'s session-switch suspend function — inject `DeviceBindingManager.switchActiveProfile()` call into the same transition (Child A→B, Child→Parent, Parent→Child, logout→None).
- `notificationsModule` (Koin) — register `DeviceBindingManager`/`DeviceBindingRepository` bindings.

## 10. Backend Requirements
Calls `POST /v1/devices` (B-01) on app start/token refresh and `PATCH /v1/devices/{id}/active-profile` (B-01) on every profile switch.

## 11. KMP Requirements
- `DeviceBindingManager.switchActiveProfile(target)` is **always** called as part of the same transition flow that handles session switching in `:core:auth` — every code path that switches the active child/parent session triggers exactly one call, with no session-switch path existing that skips it (PRD §7 Android prompt item 1, mandatory).
- Handle token refresh/rotation from the OS; re-register via `POST /v1/devices` on rotation.
- Handle binding-update API failure with retry-with-backoff; do not silently drop the update.
- Handle offline binding-update attempt by queueing for retry on reconnect (via `:core:network`'s existing offline-outbox pattern if one exists, e.g. reusing A.7's offline-checkin-outbox pattern structurally).
- Clear local binding state on logout (`target = None`).
- Prevent Context leaks — no raw platform `Context`/`UIApplicationDelegate` reference passed into the common `DeviceBindingManager` interface; platform token retrieval stays behind `NotificationHandler`.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
Consumes B-01's `POST /v1/devices` and `PATCH /v1/devices/{id}/active-profile` exactly as documented in that blueprint's §13 — no new contract defined here.

## 14. Database Requirements
Local persistence of pending/queued binding-update requests (for offline retry) via `:core:datastore`, per `CORE_DATASTORE_INSTRUCTIONS.md` conventions.

## 15. Validation
Exactly one binding-update call must fire per session-switch event — verified by the mandatory unit test in §27.

## 16. Authentication
Uses the existing authenticated session's Bearer token via `:core:network`'s standard auth-interceptor pattern.

## 17. Authorization
N/A client-side (enforced server-side by B-01).

## 18. Error Handling
| Scenario | System Behavior |
|---|---|
| Binding-update API call fails | Retry with backoff; log failure; do not silently proceed as if bound |
| Offline at time of profile switch | Queue the binding-update request; flush on reconnect |
| Token refresh/rotation | Re-register via `POST /v1/devices`; existing binding remains valid, target unchanged |
| Logout | Local binding state cleared; server-side binding revoked via existing logout flow (coordinate with A.1's logout endpoint, which should itself trigger deactivation, or this manager explicitly calls the deactivation as part of logout's transition) |

## 19. Offline First
Binding-update requests queue for retry when offline; the app does not block the profile-switch UX on this network call completing (optimistic local switch, background-synced binding).

## 20. Local Data
Pending binding-update queue persisted via `:core:datastore` to survive process death before retry succeeds.

## 21. Localization
N/A (no user-facing copy in this sub-feature).

## 22. RTL
N/A.

## 23. Analytics
Consumes/triggers `notification_binding_activated`/`notification_binding_deactivated` (emitted server-side by B-01 on successful switch); client may additionally log a local diagnostic event for retry/failure visibility.

## 24. Performance
Binding-update call must not block the profile-switch UI transition; runs as a background coroutine within the same transition scope.

## 25. Security
No `Context`/native token object leaves platform-specific code; all shared logic interacts only through `NotificationHandler`'s defined interface (`CORE_NOTIFICATIONS_INSTRUCTIONS.md` §8 Avoid — Context Leaks).

## 26. Library Requirements
Kotlin Multiplatform, Koin (DI), Ktor/Retrofit+OkHttp (per `CORE_NETWORK_INSTRUCTIONS.md`), kotlinx.coroutines, kotlin.test/JUnit for common tests.

## 27. Testing
- Unit: **mandatory** — every code path that performs a session switch in `:core:auth` triggers exactly one `DeviceBindingManager.switchActiveProfile()` call; assert no session-switch path exists that skips it (PRD §7 Android prompt item 1).
- Unit: token-refresh handling correctly re-registers.
- Unit: offline queue-and-retry logic.

## 28. Documentation
Document in `DeviceBindingManager.kt`'s class-level KDoc that this call must never be decoupled from the session-switch transition, cross-referencing PRD §6.4 and FR-8/FR-9.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define BindingTarget Sealed Class & DeviceBindingRepository**
- Files to Create: `BindingTarget.kt`, `DeviceBindingRepository.kt`.
- Implementation Details: `registerToken()` → `POST /v1/devices`; `updateActiveProfile(target)` → `PATCH /v1/devices/{id}/active-profile`.
- Tests: unit tests with a fake network client.

**Task 02 — Implement DeviceBindingManager**
- Files to Create: `DeviceBindingManager.kt`.
- Existing Files to Reuse: `NotificationHandler.getPushToken()`.
- Implementation Details: `switchActiveProfile(target)` orchestrates repository call with retry/offline-queue handling.
- Tests: unit tests for success/failure/offline paths.

**Task 03 — Wire into :core:auth Session-Switch Flow**
- Files to Modify: `:core:auth`'s session-switch function.
- Why Required: PRD §7 Android prompt item 1, the mandatory no-skip guarantee.
- Implementation Details: inject `DeviceBindingManager` call into the same suspend function/transaction as session-state clearing.
- Do Not Change: existing session-clearing logic itself, only add the binding call alongside it.
- Tests: the mandatory "no session-switch path skips this call" test — enumerate all switch entry points.

**Task 04 — Implement Offline Queue & Retry**
- Files to Modify: `DeviceBindingManager.kt`.
- Existing Architecture to Follow: A.7's offline-checkin-outbox pattern (structural reuse).
- Tests: queue-persistence-across-process-death test.

**Task 05 — Register Koin DI Bindings**
- Files to Modify: `notificationsModule`.
- Definition of Done: `DeviceBindingManager` injectable wherever `:core:auth` needs it.

**Task 06 — Write Full Test Suite & Documentation**
- Tests: per §27.
- Documentation: per §28.

## 30. Definition of Done
- Every profile-switch code path (Child↔Child, Child↔Parent, logout) triggers exactly one binding-update call, verified by an exhaustive test enumerating all switch entry points.
- Offline/failure handling never silently drops a binding update.
- No Context/native token leaks into shared code.

## 31. Final Verification Checklist
- [ ] `switchActiveProfile()` called from every session-switch entry point, with zero skippable paths
- [ ] Token registration/refresh correctly re-registers with backend
- [ ] Offline binding-update requests queue and retry successfully on reconnect
- [ ] Logout clears local binding state and triggers server-side revocation
- [ ] No raw platform Context/token object crosses into shared `commonMain` code
- [ ] Full unit test suite passes, including the mandatory no-skip-path test
