# K-02 — Deep Link Resolution & Navigation Interception

## 1. Feature Context
Part of Feature B.17 — Notifications (Child-Facing). Tapping any notification re-runs the exact same checks normal in-app navigation would, never granting a shortcut past any of them (FR-5) — this sub-feature is the client-side enforcement point ensuring the raw notification payload is never trusted directly.

## 2. Parent Feature
B.17 Notifications (Child-Facing) — KMP App (Android/iOS)

## 3. Sub-feature
K-02 Deep Link Resolution & Navigation Interception

## 4. Objective
Implement `DeepLinkResolutionHandler` to intercept every notification-tap intent, always call `GET /v1/notifications/resolve` (B-06) before any navigation occurs, and correctly handle every possible resolution outcome (valid destination, lock-gate required, content unavailable, session-expired/child-mismatch re-route, offline).

## 5. Business Requirements
- A notification tap launches the app (or brings it to foreground) with a deep-link payload → `DeepLinkResolutionHandler` calls `GET /v1/notifications/resolve` → routes to the resolved destination, the offline/unavailable fallback, or Who Is Learning, never directly trusting the raw notification payload's destination claim without this server round-trip (PRD §6.3).
- Deep links tapped offline show a clear "reconnect to open this" state, never a crash or confusing partial navigation (Edge Case 5).
- A brief, branded loading indicator during resolution rather than a jarring blank screen (PRD §2.1).

## 6. Existing Architecture
- Lives in `:core:notifications` as a navigation-layer component, per PRD §6.1 (module `:core:notifications`, depends on `:core:design-system`, `:core:network`, `:core:auth`).
- Intercepts notification-tap intents before `:core:navigation`'s standard routing takes over.
- Routes through the shared Lock Gate component from `:core:auth`/A.1 when `requires_lock_gate` is signaled — reuse that existing component, do not build a parallel gate.
- Routes to "Who Is Learning" using the existing screen/flow from A.1/B.16 — reuse, don't duplicate.

## 7. Existing Code to Reuse
- Shared Lock Gate component (`:core:auth`, A.1/B.16).
- Who Is Learning screen/flow (A.1/B.16).
- `:core:design-system` loading/error state components.
- `:core:network` for the resolve API call.

## 8. Files to Create
- `core-notifications/src/commonMain/kotlin/.../deeplink/DeepLinkResolutionHandler.kt`.
- `core-notifications/src/commonMain/kotlin/.../deeplink/NotificationRepository.kt` — `resolveDeepLink(token): DeepLinkResolution`.
- `core-notifications/src/commonMain/kotlin/.../deeplink/DeepLinkResolution.kt` — sealed class (`Valid`, `RequiresLockGate`, `ContentUnavailable`, `SessionExpiredOrMismatch`, `Offline`).
- `core-notifications/src/commonMain/kotlin/.../deeplink/DeepLinkResolutionScreen.kt` — Compose loading/offline/unavailable states.
- `core-notifications/src/commonTest/kotlin/.../deeplink/DeepLinkResolutionHandlerTest.kt`.

## 9. Files to Modify
- `:core:navigation`'s intent-handling entry point — route all notification-tap intents through `DeepLinkResolutionHandler` first.

## 10. Backend Requirements
Consumes B-06's `GET /v1/notifications/resolve` contract exactly as documented.

## 11. KMP Requirements
- Intercept **all** notification-tap intents; always call `GET /v1/notifications/resolve` before any navigation occurs — the raw notification payload's claimed destination is never directly used for navigation without first passing through this server-validated resolution call (PRD §7 Android prompt item 2, mandatory).
- Handle `valid` → navigate to resolved destination.
- Handle `requires_lock_gate` → route through the shared Lock Gate first, then to the resolved destination.
- Handle `content_unavailable` → show the graceful fallback with a suggested alternative, consistent with A.3/A.6's withdrawn-content UX pattern.
- Handle `session_expired`/`child_mismatch` → route to Who Is Learning.
- Handle offline (resolve call fails due to connectivity) → show "Connect to the internet to open this" with a retry action, never a crash or silently-stuck spinner.
- Prevent duplicate navigation on rapid repeated taps (debounce).

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
Consumes B-06's `GET /v1/notifications/resolve` exactly as documented in that blueprint's §13.

## 14. Database Requirements
N/A (stateless per-tap resolution; no local persistence required).

## 15. Validation
Every notification-tap code path must route through this handler — no alternate navigation path may bypass it.

## 16. Authentication
Uses the existing authenticated session's Bearer token via `:core:network`.

## 17. Authorization
N/A client-side (server-enforced by B-06).

## 18. Error Handling
| Scenario | System Behavior |
|---|---|
| Resolve call fails due to no connectivity | "Connect to the internet to open this" state with retry action |
| `content_unavailable` response | Graceful fallback with suggested alternative |
| `session_expired`/`child_mismatch` response | Route to Who Is Learning |
| `requires_lock_gate` response | Route through shared Lock Gate, then resolved destination |
| Rapid repeated taps on the same/different notifications | Debounced; only one resolution/navigation proceeds at a time |

## 19. Offline First
Deep-link resolution requires connectivity by design (server-side validation is mandatory); the offline state shown is a clear, honest prompt rather than any local-only resolution attempt (PRD §6.7).

## 20. Local Data
N/A.

## 21. Localization
Loading/offline/unavailable copy fully localized (EN/HI/AR/UR) via `:core:design-system` string resources — no hardcoded strings.

## 22. RTL
Loading/offline/unavailable screens correctly mirror for AR/UR per `CORE_DESIGNSYSTEM_INSTRUCTIONS.md` RTL conventions.

## 23. Analytics
`notification_opened`, `notification_deep_link_resolved`, `notification_deep_link_offline_shown`, `notification_deep_link_content_unavailable_shown`.

## 24. Performance
Resolution loading state must render immediately (no blank frame) while the network call is in flight; avoid unnecessary recomposition during the loading→resolved transition.

## 25. Security
This handler is the client-side enforcement of "never trust the raw payload" — the mandatory unit test (§27) proves no navigation path exists that skips the server round-trip (PRD §12.1 Broken Access Control mitigation, client side).

## 26. Library Requirements
Kotlin Multiplatform, Jetpack Compose, Koin, Ktor/Retrofit+OkHttp, kotlinx.coroutines, kotlin.test/JUnit, Compose UI testing.

## 27. Testing
- Unit: **mandatory** — parameterized test covering all resolve-response variants (`valid`, `requires_lock_gate`, `content_unavailable`, `session_expired`/`child_mismatch`, network failure) and asserting correct handling for each (PRD §7 Android prompt item 3).
- Unit: **mandatory** — raw notification payload's claimed destination is never directly used for navigation without first passing through resolution (PRD §7 Android prompt item 2).
- UI test: **mandatory** — simulated airplane mode on a notification tap renders the offline state, never a crash or stuck spinner (PRD §7 Android prompt item 5).

## 28. Documentation
Document in `DeepLinkResolutionHandler.kt`'s KDoc that this is the sole authorized entry point for notification-tap navigation, cross-referencing PRD FR-5.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define DeepLinkResolution Sealed Class**
- Files to Create: `DeepLinkResolution.kt`.
- Implementation Details: model all five outcome variants.

**Task 02 — Implement NotificationRepository.resolveDeepLink()**
- Files to Create: `NotificationRepository.kt`.
- Existing Files to Reuse: `:core:network` client conventions.
- Tests: unit tests with a fake network client covering all response shapes.

**Task 03 — Implement DeepLinkResolutionHandler Interception**
- Objective: Intercept all notification-tap intents.
- Why Required: PRD §7 Android prompt item 2, mandatory.
- Files to Create: `DeepLinkResolutionHandler.kt`.
- Files to Modify: `:core:navigation` intent entry point.
- Tests: mandatory "never navigate without resolution" test.

**Task 04 — Implement Response-Variant Routing Logic**
- Objective: Correct handling for all five outcomes.
- Why Required: PRD §7 Android prompt item 3, mandatory.
- Existing Files to Reuse: shared Lock Gate, Who Is Learning flow.
- Tests: mandatory parameterized test.

**Task 05 — Implement Loading/Offline/Content-Unavailable Compose States**
- Files to Create: `DeepLinkResolutionScreen.kt`.
- Existing Files to Reuse: `:core:design-system` components, A.3/A.6 withdrawn-content pattern.
- Localization/RTL: per §21/§22.
- Tests: mandatory offline-state UI test (simulated airplane mode).

**Task 06 — Implement Debounce for Rapid Repeated Taps**
- Files to Modify: `DeepLinkResolutionHandler.kt`.
- Tests: rapid-tap debounce test.

**Task 07 — Add Analytics Instrumentation**
- Analytics: per §23.
- Tests: event-firing verification test.

**Task 08 — Write Full Test Suite & Documentation**
- Tests: per §27.
- Documentation: per §28.

## 30. Definition of Done
- Every notification-tap intent is intercepted and resolved server-side before navigation, with no bypass path.
- All five resolution outcomes handled correctly, verified by the mandatory parameterized test.
- Offline state renders correctly and is verified via a simulated-airplane-mode UI test.

## 31. Final Verification Checklist
- [ ] All notification-tap intents route through `DeepLinkResolutionHandler` — no alternate path exists
- [ ] Raw payload destination is never used directly for navigation
- [ ] `valid`, `requires_lock_gate`, `content_unavailable`, `session_expired`/`child_mismatch`, and offline outcomes all handled correctly
- [ ] Offline state shows a clear reconnect prompt, verified via simulated airplane-mode test
- [ ] Rapid repeated taps do not cause duplicate navigation
- [ ] Loading/offline/unavailable states are localized and RTL-correct
- [ ] Analytics events fire correctly for each outcome
- [ ] Full test suite passes, including both mandatory PRD-specified tests
