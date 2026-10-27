# K-06 — Child Locks & Sessions Management

## 1. Feature Context
Lets a parent configure each child's independent app lock (none/pattern/PIN/biometric) and view/revoke active devices (PRD C.23 FR-9, FR-10, §1.18 Screens #6–#9).

## 2. Parent Feature
Feature C.23 — Parental Controls (Screen Time, Bedtime, AI Permissions, Content Age Level)

## 3. Sub-feature
2.6 Child Locks & Sessions Management (ID: **K-06**)

## 4. Objective
Build `ChildLocksAndSessionsScreen`, `Set Lock Type` sub-screen, `Active Device List` component, and `Device Revocation Confirmation` modal, reusing C.19's existing session-list/revocation infrastructure in `:core:auth` rather than a parallel client.

## 5. Business Requirements
- FR-9: configure per-child lock; view/revoke active device list; revoking force-logs-out that session.
- FR-10: only salted hashes/OS biometric assertions transmitted; raw values never logged, consistent with C.19's storage rule.
- §7 Android AI Code-Generation Prompt item 5: device revocation calls `DELETE /v1/sessions/{id}` through `:core:auth`'s shared session repository, not a parallel client.

## 6. Existing Architecture
Module `:feature:parental-controls`. Depends on `:core:auth` for both `ChildLockConfigRepository` (new, maps to B-05) and the existing session repository (`AuthRepository.getSessions()`, now backed end-to-end by B-06's resolved `device_sessions`/Redis-denylist design). Reuses C.19's Set Lock Type UI pattern if one already exists in `:core:auth` or a shared onboarding module — confirm before building a parallel screen.

## 7. Existing Code to Reuse
- `:core:auth::AuthRepository.getSessions()` (existing method per `core-security` doc) — reuse for the Active Device List rather than building a new session-fetch path; as of B-06, this now returns real listing data (`device_name`, `last_active_at`) instead of a stub
- `:core:auth::ParentGateLauncher`

**Resolved:** hashing happens **server-side only** (B-05 §10) — the client transmits the raw pattern/PIN value over TLS and B-05 hashes it immediately on receipt. Do **not** hash client-side with `CredentialHasher` for this flow; doing so would produce a hash-of-a-hash mismatch against B-05's stored value. `CredentialHasher` remains reserved for flows that explicitly call for client-side hashing elsewhere in the app (e.g., offline verification caches) — this screen is not one of them.

## 8. Files to Create
- `core/data/src/commonMain/kotlin/.../repository/ChildLockConfigRepository.kt` (interface) + impl
- `feature/parental-controls/src/commonMain/kotlin/.../ui/ChildLocksAndSessionsScreen.kt`
- `feature/parental-controls/src/commonMain/kotlin/.../ui/SetLockTypeScreen.kt`
- `feature/parental-controls/src/commonMain/kotlin/.../ui/ActiveDeviceListComponent.kt`
- `feature/parental-controls/src/commonMain/kotlin/.../ui/DeviceRevocationConfirmationModal.kt`
- `feature/parental-controls/src/commonMain/kotlin/.../viewmodel/ChildLocksAndSessionsViewModel.kt`
- `feature/parental-controls/src/commonTest/kotlin/.../ChildLocksAndSessionsViewModelTest.kt`

## 9. Files to Modify
- `core/data/.../di/RepositoryModule.kt` — register `ChildLockConfigRepository`

## 10. KMP Requirements
- `ChildLockConfigRepository.getLock(childId)`/`setLock(childId, lockType, value?)` mapping to B-05's `GET/PATCH /v1/children/{id}/lock`.
- `ChildLocksAndSessionsViewModel`: loads current lock type + calls `AuthRepository.getSessions()` for the device list, filtered/scoped to the selected child where applicable.
- `SetLockTypeScreen`: pattern/PIN entry UI (reuse existing pattern/PIN input components from C.19's onboarding flow if present) or biometric toggle; on submit, transmits the raw value over TLS to B-05 for server-side hashing (resolved contract — no client-side hashing for this flow).
- `ActiveDeviceListComponent`: renders device name, last-active timestamp, Revoke action per entry.
- Device revocation: `DeviceRevocationConfirmationModal` → on confirm, calls `AuthRepository`'s existing session-revocation method (or the extended one from B-06) — never a parallel network call.
- Save routes through `ParentGateLauncher.requireParentAuth()`.

## 11. API Contract
### Required API (consumed)
- **HTTP Method:** GET/PATCH — **Endpoint:** `/v1/children/{id}/lock` (B-05)
- **HTTP Method:** GET — **Endpoint:** `/v1/sessions` (B-06) — **HTTP Method:** DELETE — **Endpoint:** `/v1/sessions/{id}` (B-06)
- **Authentication:** Bearer (parent), step-up on all mutations

## 12. Database Requirements
N/A — lock hash lives server-side only (per B-05); no local secure cache needed here (offline lock *verification* caching is C.19's own K-06 sub-feature in a different feature/module — note the ID-number collision is between two different features' independent K-06 numbering, not a shared file; no action needed beyond keeping the two modules' file paths distinct, which they already are: `feature/parental-controls/` here vs. C.19's onboarding/auth module).

## 13. Validation
- Lock-type selection UI inherently constrains to the four valid enum values.
- Pattern/PIN entry: minimum length/complexity rules per C.19's existing established UX pattern (reuse, don't reinvent).

## 14. Authentication
Save/revoke routes through `ParentGateLauncher.requireParentAuth(Settings)`.

## 15. Authorization
N/A beyond parent-mode gate; server enforces family ownership.

## 16. Error Handling
| Scenario | UI Behavior |
|---|---|
| Set lock failure | Inline error, form retains entry |
| Revoke failure | Inline error, device remains in list |
| Empty device list | Explicit empty state ("No other active devices") |
| Load failure | Error state with retry |

## 17. Offline First
Both lock configuration and session management require connectivity (server-authoritative); no offline mutation path.

## 18. Local Data
N/A for this sub-feature's own screens (distinct from C.19's offline lock-verification cache, which is a separate concern).

## 19. Localization
All labels, device-list column headers, and confirmation copy localized in EN/HI/AR/UR.

## 20. RTL
Screen list, form, and modal all mirror correctly in RTL.

## 21. Analytics
`child_lock_type_set`, `device_revoked`.

## 22. Performance
Device list is typically small (few devices per family); no pagination needed. `@Immutable` state.

## 23. Security
Raw pattern/PIN transmitted over TLS only, never logged client-side (confirm no client-side logging captures the raw entry field — audit any debug/crash-breadcrumb logging around this screen). Reuses C.19's existing session infrastructure rather than a parallel, potentially inconsistent implementation.

## 24. Library Requirements
Jetpack Compose, Koin, Ktor (via `core-network`/`core-auth`).

## 25. Testing
- Unit: lock-type set flow calls B-05's endpoint with the correct raw (unhashed) value — asserts no `CredentialHasher` call occurs anywhere in this submission path.
- Unit: revocation calls the existing `AuthRepository` session-revocation path, not a parallel client (verified via dependency/mock assertion).
- UI test: empty device list renders correct empty state.
- UI test: revocation confirmation modal required before the DELETE call fires.

## 26. Documentation
KDoc explicitly noting that raw lock values are transmitted over TLS unhashed and hashed server-side (B-05), to prevent a future contributor from "improving security" by adding client-side hashing and breaking the contract.

## 27. AI Coding Agent Implementation Steps

**Task 01 — Implement Submission Path Against B-05's Resolved (Unhashed) Contract**
- Objective: Wire `SetLockTypeScreen`'s submit action to transmit the raw value directly (no client-side hashing) per B-05 §10 — contract is resolved, implement directly rather than re-confirming.

**Task 02 — Wire `AuthRepository.getSessions()` for the Active Device List**
- Objective: Confirm this existing method's response shape now includes B-06's `device_name`/`last_active_at` fields (added by B-06's `device_sessions` table) and map them directly into `ActiveDeviceListComponent`.

**Task 03 — Implement `ChildLockConfigRepository`**
- Files to Create: `repository/ChildLockConfigRepository.kt` + impl

**Task 04 — Implement `ChildLocksAndSessionsViewModel`**
- Files to Create: `viewmodel/ChildLocksAndSessionsViewModel.kt`
- Dependencies: Tasks 01–03.

**Task 05 — Implement `ChildLocksAndSessionsScreen` Composable**

**Task 06 — Implement `SetLockTypeScreen` Composable**
- Implementation Details: Reuse C.19's pattern/PIN entry component if it exists.

**Task 07 — Implement `ActiveDeviceListComponent`**

**Task 08 — Implement `DeviceRevocationConfirmationModal`**

**Task 09 — Add Localization Strings**

**Task 10 — Add Unit Tests**
- Files to Create: `ChildLocksAndSessionsViewModelTest.kt`

**Task 11 — Add UI Tests**

**Task 12 — Final Code Review**
- Objective: Confirm no parallel session client was built; confirm raw-value transmission contract matches B-05 exactly.

## 28. Definition of Done
- Lock configuration and device revocation both work end-to-end against B-05/B-06.
- Device revocation reuses C.19's existing session infrastructure.
- No client-side hashing mismatch with B-05's server-side hashing contract.

## 29. Final Verification Checklist
- [ ] Raw-value (unhashed) transmission implemented per B-05's resolved contract; no `CredentialHasher` call in this path
- [ ] Confirmed reuse of existing `AuthRepository` session methods (now backed by B-06), no parallel client
- [ ] Empty device list state tested
- [ ] Revocation confirmation modal required before DELETE
- [ ] Save/revoke gated by Parent Gate
- [ ] Localization and RTL verified
