# K-05 — Session Activation & Cross-Profile State Clearing

## 1. Feature Context
Stages 3–4 of the pipeline on the client: after a lock/gate passes, call B-04's session-activation API, then clear every other feature module's cached state for the previous profile before the new profile's Home renders. This is the client-side half of the platform's sibling-isolation guarantee and is the mechanism B.16 K-04 explicitly delegates to.

## 2. Parent Feature
Feature C.19 — Parent PIN/Biometric Gate & Profile Access Control

## 3. Sub-feature
2.5 Session Activation & Cross-Profile State Clearing (ID: **K-05**)

## 4. Objective
Implement `SessionActivationRepository`, calling B-04's `POST /v1/sessions/child-mode`, storing the returned session token as the single source of truth for the active `child_id`, and clearing all other feature modules' cached/in-memory state for the previous profile before navigating to the new profile's Home.

## 5. Business Requirements
- FR-7 (stages 3-4): Check Restrictions then Activate Context (session creation, notification-binding switch, cache-clear).
- FR-8: sibling progress must never be returned to child-mode API calls — client must never retain stale cached data from the previous child that could leak into new-child UI even momentarily.
- FR-9: switching to a different child clears all previous child-sensitive UI state **before** activating the new scoped session.
- Edge Case 2: switching between a locked and unlocked sibling always re-runs the full pipeline including state-clearing, for every switch.

## 6. Existing Architecture
New component in `core-auth` (or `core-data`, confirm against KMP Core Architecture doc's convention for session-scoped orchestration) — `SessionActivationRepository` centralizes what B.16 K-04 previously described as "K-01's state-clearing mechanism," generalizing it so it applies platform-wide (A.2–A.12, B.13–B.18), not just Profile.

## 7. Existing Code to Reuse
- `core-network`'s API client, extended with `activateChildSession(childId)` → B-04
- `core-data`'s existing per-feature cache-clearing hooks (B.16 K-01's `ChildProfileViewModel` clearing pattern, generalized here rather than duplicated per-module)
- `core-auth/ParentGateLauncher`, `GraceWindowManager` (K-03) — consumed as the preceding gate step, not reimplemented

## 8. Files to Create
- `core-auth/SessionActivationRepository.kt` — `activate(childId): Result<ChildSession>`, exposes `currentSession: StateFlow<ChildSession?>`
- `core-auth/SessionTokenStore.kt` — secure storage for the active session token (Keystore-backed, mirrors K-06's pattern)
- `test/core-auth/SessionActivationRepositoryTest.kt`
- `test/core-auth/CrossProfileStateClearingTest.kt`

## 9. Files to Modify
- Each feature module with child-scoped cached state (starting with B.16's `ChildProfileViewModel`/K-01, extending to other modules as they are built) — register a state-clearing callback with `SessionActivationRepository` rather than implementing ad-hoc clearing per module
- `core-navigation` — session-activation success triggers navigation to the new profile's Home, failure (restriction failure) triggers the appropriate restriction/locked/bedtime screen

## 10. KMP Requirements
- `SessionActivationRepository.activate(childId)`:
  1. Call B-04's `POST /v1/sessions/child-mode`.
  2. On `403 RESTRICTION_FAILED`, surface the specific `failure_reason` to the caller for routing to the correct screen (Restriction Screen / Calm Locked State / Bedtime Block Screen) — never a generic error.
  3. On success: store the new `session_token` in `SessionTokenStore`, invoke all registered state-clearing callbacks for the **previous** profile, update `currentSession`, then signal navigation-ready.
  4. Trigger B.17's device-binding switch consumption (the binding switch itself happens server-side per B-04; client confirms the new binding is reflected in notification-handling state).
- State-clearing callbacks must complete (or be guaranteed to complete) before the new profile's Home screen composes — no window where stale previous-child data could render.
- Two-devices-independent-binding: `SessionTokenStore` is local to this device only, no cross-device synchronization.

## 11. Required API
`POST /v1/sessions/child-mode` (B-04).
**User API**

## 12. Offline First
When offline, restriction evaluation falls back to the last-signed policy snapshot cached from the most recent successful online activation (per FR-15) — `SessionActivationRepository` must cache and version this snapshot, exposing it to the offline path without a network round-trip.

## 13. Local Data
`SessionTokenStore` — Keystore-backed active session token. Last-signed restriction/policy snapshot cached per child for offline fallback (versioned, so a stale snapshot is detectable).

## 14. Localization
Restriction/Calm-Locked/Bedtime-Block screen copy fully localized EN/HI/AR/UR (screens themselves may be owned by C.23; this sub-feature only routes to them with the correct `failure_reason`).

## 15. RTL
N/A directly — this sub-feature is orchestration logic, not UI; downstream screens handle their own RTL.

## 16. Analytics
`restriction_check_failed` (with `failure_reason`), `restriction_override_requested`, `restriction_override_granted`, `session_activated`, `previous_profile_cache_cleared`.

## 17. Performance
State-clearing must not introduce a perceptible delay on Home-screen composition — clearing callbacks should be lightweight (in-memory state resets), not blocking I/O; any necessary I/O (e.g., clearing a local DB cache) should be dispatched off the main thread without blocking navigation.

## 18. Security
This is the client-side half of the sibling-isolation guarantee (server-side owned by B-04). No feature module may cache child-scoped data without registering a corresponding clearing callback — a structural/lint-style check is recommended (out of scope to build here, but flag as a follow-up) to catch modules that introduce child-scoped `StateFlow`/cache without registration.

## 19. Testing
- Integration: full switch → different-child-selected → session-clear → new-session-Home-renders flow, asserting zero residual data across at least B.16's `ChildProfileViewModel` (joint test with B.16 K-01/K-04).
- Integration: restriction failure routes to the correct screen per `failure_reason`.
- Integration: offline activation uses the last-signed policy snapshot, versioned correctly.
- Unit: `SessionTokenStore` never persists the token in plaintext.

## 20. AI Coding Agent Implementation Steps

**Task 01 — Implement `SessionTokenStore`**
Objective: Keystore-backed secure token storage. Files to Create: `SessionTokenStore.kt`. Dependencies: none.

**Task 02 — Implement `SessionActivationRepository.activate()`**
Objective: full orchestration per §10. Files to Create: `SessionActivationRepository.kt`. Dependencies: Task 01, B-04 live.

**Task 03 — Implement State-Clearing Callback Registration**
Objective: generalize B.16 K-01's clearing pattern into a registerable callback mechanism. Files to Modify: B.16's `ChildProfileViewModel.kt` (register callback), `SessionActivationRepository.kt` (registry). Dependencies: Task 02.

**Task 04 — Implement Offline Last-Signed-Policy Caching**
Objective: versioned snapshot cache for offline restriction fallback. Files to Modify: `SessionActivationRepository.kt`. Dependencies: Task 02.

**Task 05 — Add Cross-Profile State-Clearing Test**
Objective: zero-residual-data guarantee, joint with B.16. Files to Create: `CrossProfileStateClearingTest.kt`. Dependencies: Task 03.

**Task 06 — Add Full Test Suite & Analytics**
Objective: coverage per §19, events per §16. Dependencies: Task 01–05.

## 21. Final Verification Checklist
- [x] Every switch clears all registered previous-profile state before new Home renders
- [x] Restriction failures route to the correct specific screen, never a generic error
- [x] Session token stored via Keystore, never plaintext
- [x] Offline activation uses a versioned last-signed policy snapshot
- [x] No cross-device session-state synchronization exists

## 22. Definition of Done
`SessionActivationRepository` is the platform's single orchestration point for stage 3–4 of the C.19 pipeline, calling B-04, clearing all registered previous-profile state before rendering the new profile, and falling back correctly to a versioned offline policy snapshot when disconnected.

## 23. Verification & Compliance Record
- **Implementation Status**: COMPLETED (100% compliant with C.19 FR-7, FR-8, FR-9, and Edge Case 2)
- **Key Invariants Verified**:
  - `SessionActivationRepository.activate(childId)` orchestrates B-04 `POST /v1/sessions/child-mode`.
  - Zero lateral sibling leakage: all registered `ProfileStateClearingListener` callbacks complete before new profile Home renders.
  - Active session token stored securely via Keystore-backed `SessionTokenStore` (never plaintext).
  - Versioned last-signed restriction policy snapshot fallback enforced offline (FR-15).
  - Specific routing for 403 `RESTRICTION_FAILED` failure reasons to K-07 response screens.
- **Unit & Integration Tests**:
  - `SessionActivationRepositoryTest.kt`: Online activation, 403 restriction mapping, offline snapshot fallback, stale snapshot rejection, and clear active session.
  - `CrossProfileStateClearingTest.kt`: Guaranteed previous profile state clearing across profile switches.
- **Test Execution Result**:
  - `:core:core-data:testAndroidHostTest` -> SUCCESS (100% passing)
  - `:shared:testAndroidHostTest` -> SUCCESS (100% passing)
