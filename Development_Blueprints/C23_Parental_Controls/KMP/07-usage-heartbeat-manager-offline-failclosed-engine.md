# K-07 — Usage Heartbeat Manager & Offline Fail-Closed Engine

## 1. Feature Context
The shared, Child-Mode-consumed engine that sends periodic usage heartbeats to B-02, derives limit/bedtime state exclusively from server responses, and fails closed to a conservative state when offline beyond the signed policy token's grace period (PRD C.23 §5/§7 Backend/Android AI Code-Generation Prompts).

## 2. Parent Feature
Feature C.23 — Parental Controls (Screen Time, Bedtime, AI Permissions, Content Age Level)

## 3. Sub-feature
2.7 Usage Heartbeat Manager & Offline Fail-Closed Engine (ID: **K-07**)

## 4. Objective
Implement `UsageHeartbeatManager` in a new shared `:core:restriction-engine` module, consumed by the Child Mode app shell (not by `:feature:parental-controls`, which owns configuration screens only), sending periodic heartbeats and deriving `minutes_used_today`/`minutes_remaining`/`limit_reached`/`bedtime_active` exclusively from B-02's server responses.

## 5. Business Requirements
- FR-3 (client-side mirror): never derive usage values from local-clock arithmetic.
- FR-4: offline mode enforces the last signed policy rather than unlimited use.
- Edge Case 4: offline beyond grace period fails closed to the most conservative state (treat as limit reached).
- §7 item 1: fall back to the LAST SERVER-REPORTED value (never a locally-extrapolated guess) if heartbeats are temporarily failing.
- §7 item 2: offline fail-closed transition tested against an expired grace window.

## 6. Existing Architecture
New shared module `:core:restriction-engine`, sitting alongside `:core:data`/`:core:network` in the dependency graph, consumed by the Child Mode app shell. Depends on `:core:common` (`LocalDateProvider`, `NoorResult`, `DispatcherProvider`), `:core:network`, `:core:datastore` (for the signed policy token cache — small, non-relational, appropriate for `PreferenceManager` rather than `core-database`).

## 7. Existing Code to Reuse
- `:core:common::LocalDateProvider` — for any date-boundary logic needed around the token expiry check (never `Clock.System.now()` directly)
- `:core:common::DispatcherProvider` — coroutine dispatching, never hardcoded `Dispatchers.IO`
- `:core:datastore::PreferenceManager` — caching the last server-reported usage snapshot and the signed policy token
- `:core:common::NoorResult<T>`/`Outcome` — error handling pattern

## 8. Files to Create
- `core/restriction-engine/src/commonMain/kotlin/.../UsageHeartbeatManager.kt`
- `core/restriction-engine/src/commonMain/kotlin/.../model/HeartbeatState.kt`
- `core/restriction-engine/src/commonMain/kotlin/.../PolicyTokenStore.kt` (wraps `PreferenceManager` with typed access to the signed token + expiry)
- `core/restriction-engine/src/commonMain/kotlin/.../di/RestrictionEngineModule.kt`
- `core/restriction-engine/src/commonTest/kotlin/.../UsageHeartbeatManagerTest.kt`

## 9. Files to Modify
- Child Mode app shell (root Composable/ViewModel that hosts active child sessions) — inject `UsageHeartbeatManager`, start/stop heartbeat loop on session enter/exit, observe `HeartbeatState` to drive K-08's enforcement UI

## 10. KMP Requirements
- `UsageHeartbeatManager.start(childId: String)`: launches a coroutine (scoped to the active child session, cancelled on session exit — no leaked jobs) sending a heartbeat every 30–60s of foreground active time via `ControlsRepository`-adjacent network call to B-02.
- On each successful response: update `HeartbeatState` (`minutesUsedToday`, `minutesRemaining`, `limitReached`, `bedtimeActive`, `warningThresholdCrossed`) **exclusively** from the response payload — no local arithmetic derivation anywhere in this class.
- On heartbeat failure: retain the **last server-reported** `HeartbeatState` (do not locally extrapolate a new value); retry with backoff.
- Persist the signed policy token (and its `expires_at`) from each successful response into `PolicyTokenStore`.
- On heartbeat failure while offline: check `PolicyTokenStore`'s cached token expiry against `LocalDateProvider`'s current time; if expired, transition `HeartbeatState` to a conservative fail-closed state (`limitReached = true`) regardless of the last known server-reported value.
- Expose `HeartbeatState` as a `Flow` for the Child Mode shell and K-08's enforcement UI to observe.
- Coroutine cancellation safety: heartbeat loop must be cancelled cleanly on session exit/background to prevent leaked jobs or continued heartbeats for an inactive session.

## 11. API Contract
### Required API (consumed)
- **HTTP Method:** POST — **Endpoint:** `/v1/children/{id}/usage-heartbeats` (B-02)
- **Request:** `{ "foreground_seconds_since_last_heartbeat": int, "client_timestamp": "ISO8601" }`
- **Response:** `{ "minutes_used_today", "minutes_remaining", "limit_reached", "warning_threshold_crossed", "bedtime_active", "signed_policy_token", "policy_token_expires_at" }`
- **Authentication:** Bearer (child-mode)

## 12. Database Requirements
N/A (backend-side only); client-side uses `core-datastore` preferences, not `core-database`, for the lightweight token/state cache.

## 13. Validation
N/A — this layer trusts and forwards server responses; no independent validation logic beyond null/malformed-response defensive handling.

## 14. Authentication
Uses the active child-mode session token (already established by C.19's session activation).

## 15. Authorization
N/A beyond the existing child-mode session token.

## 16. Error Handling
| Scenario | Behavior |
|---|---|
| Heartbeat network failure (transient) | Retain last server-reported state; retry with backoff |
| Heartbeat failure beyond signed token's grace window | Fail closed: `limitReached = true` regardless of prior state |
| Malformed/unexpected response | Log via `NoorHeroesLogger`, retain last known-good state, do not crash |

## 17. Offline First
This is the platform's canonical offline-first restriction-enforcement flow: Remote Data (B-02 heartbeat response) → `PolicyTokenStore` (local signed-token cache) → `HeartbeatState` Flow → UI (K-08). Offline reads fall back to the cached signed token within its grace period; beyond that, fail closed.

## 18. Local Data
`PolicyTokenStore` (via `core-datastore::PreferenceManager`) persists: last `HeartbeatState` snapshot, signed policy token, token expiry timestamp.

## 19. Localization
N/A (data/logic layer only; K-08 owns display).

## 20. RTL
N/A.

## 21. Analytics
Surfaces the underlying state that K-08 uses to fire `restriction_warning_notification_fired`, `restriction_limit_reached`, `restriction_offline_grace_expired_failclosed` — this layer itself does not fire analytics events directly (keeps analytics ownership at the UI layer per platform convention, confirm against `core-common`'s analytics instrumentation pattern).

## 22. Performance
This is the platform's highest-frequency background operation on the child-mode client. Must never block the main thread; must use `DispatcherProvider.io` for network calls; must not cause excessive recomposition in observers (expose `HeartbeatState` as a stable, `@Immutable` data class).

## 23. Security
The core client-side trust boundary: this class must contain zero local-clock-based derivation of usage values anywhere — code review must verify this explicitly, not just rely on tests, since a single stray `Clock.System.now()` subtraction would silently reintroduce the exact vulnerability this feature exists to close.

## 24. Library Requirements
Kotlin Coroutines, Ktor (via `core-network`), `core-datastore`, Koin.

## 25. Testing
- Unit: confirm `HeartbeatState` is derived exclusively from server responses — no test path should be able to produce a state value through local arithmetic.
- Unit: simulated heartbeat failure retains last server-reported value (not a locally extrapolated guess).
- Unit: simulated expired grace window transitions to fail-closed (`limitReached = true`).
- Unit: coroutine cancellation on session exit — confirm no lingering heartbeat job after `stop()`.
- Load/soak test: sustained heartbeat loop over a long simulated session without memory growth (leak check).

## 26. Documentation
KDoc stating explicitly, at the top of `UsageHeartbeatManager.kt`: "This class MUST NEVER derive minutesUsedToday/minutesRemaining/limitReached from local device time. All such values come exclusively from the server's heartbeat response."

## 27. AI Coding Agent Implementation Steps

**Task 01 — Create `:core:restriction-engine` Module Scaffold**
- Objective: New shared KMP module, wired into the multi-module build alongside existing `:core:*` modules.

**Task 02 — Define `HeartbeatState` Model**
- Files to Create: `model/HeartbeatState.kt`
- Implementation Details: `@Immutable` data class per §10 fields.

**Task 03 — Implement `PolicyTokenStore`**
- Files to Create: `PolicyTokenStore.kt`
- Dependencies: `core-datastore::PreferenceManager`.

**Task 04 — Implement `UsageHeartbeatManager` Core Loop**
- Files to Create: `UsageHeartbeatManager.kt`
- Dependencies: Tasks 02, 03; B-02's heartbeat endpoint via `core-network`.
- Implementation Details: Per §10 — this is the highest-priority task in this file; write and test the server-time-only derivation guarantee before anything else.

**Task 05 — Implement Offline Fail-Closed Transition**
- Dependencies: Task 03, 04.

**Task 06 — Implement Retry/Backoff on Transient Failure**

**Task 07 — Wire into Child Mode App Shell**
- Files to Modify: Child Mode root shell ViewModel/Composable.
- Implementation Details: Start on session enter, stop on session exit — coroutine-scoped correctly to avoid leaks.

**Task 08 — Register Koin Module**
- Files to Create: `di/RestrictionEngineModule.kt`

**Task 09 — Add Server-Time-Only Derivation Test**
- Files to Create: `UsageHeartbeatManagerTest.kt`
- Objective: Highest-priority test in this file.

**Task 10 — Add Fail-Closed and Last-Known-Value Tests**

**Task 11 — Add Coroutine Cancellation/Leak Tests**

**Task 12 — Final Code Review**
- Objective: Explicit grep/audit for any `Clock.System.now()` or local-arithmetic usage inside this class — must be zero occurrences.

## 28. Definition of Done
- Zero local-clock-derived usage values anywhere in this module (code-review confirmed).
- Offline fail-closed transition verified by test.
- No coroutine leaks across session enter/exit cycles.
- Wired correctly into the Child Mode app shell.

## 29. Final Verification Checklist
- [ ] No local-clock arithmetic used for usage-value derivation (grep-audited)
- [ ] Last-server-reported-value fallback tested
- [ ] Offline fail-closed transition tested against expired grace window
- [ ] Coroutine cancellation on session exit tested
- [ ] `HeartbeatState` is `@Immutable` and recomposition-safe
- [ ] Wired into Child Mode app shell correctly
