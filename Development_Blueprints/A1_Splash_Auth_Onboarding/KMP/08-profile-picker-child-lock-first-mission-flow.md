# K-08 — Profile Picker, Child Lock & First Mission Flow

> **Status:** ✅ **Implemented & Verified** (Live simulator verified on Android `emulator-5554` with live FastAPI backend)

## 1. Feature Context
The routing hub every returning session lands on: pick a child (or Parent Profile), pass through the child's lock if configured, and — on a child's very first session — see a First Mission recommendation before normal Child Home content.

## 2. Parent Feature
Feature A.1 — Splash, Language Selection, Authentication & Onboarding

## 3. Sub-feature
2.8 Profile Picker, Child Lock & First Mission Flow (ID: **K-08**)

## 4. Objective
Build Profile Picker, Child Lock Screen, Lock Recovery, and First Mission screens against B-06's children list, using `core-security`'s `BiometricGate`/`CredentialHasher` for on-device lock verification and `core-data`'s `ChildLockRepository.verifyChildLock()` for the offline-tolerant entitlement-grace-period check.

## 5. Business Requirements
- Screen note: disabled children hidden from Profile Picker, visible only inside Parent Profile.
- Screen note: "Forgot lock" routes to Parent Profile verification only — never a generic bypass.
- Empty State: zero-children Profile Picker (post-deletion edge case) → "Add Child" as primary tile, friendly illustration, no error framing.
- First Mission: first-session-only, never reappears.
- §6.4 (core-data): `ChildLockRepository.verifyChildLock()` performs local hash verification and validates the cached entitlement snapshot is within the allowed grace period (e.g., 7 days) — reuse this exactly, do not build a parallel lock-check.

## 6. Existing Architecture
`core-data`'s `ChildLockRepository` (referenced in `core-data`'s own documentation as the existing mechanism for "Child Mode" entry) — this sub-feature is largely UI wiring on top of an already-designed data-layer capability, not new lock logic.

## 7. Existing Code to Reuse
- `core-data`: `ChildLockRepository.verifyChildLock()` (existing — per `core-data`'s own docs, §8 "Handling Child Mode Entry")
- `core-security`: `BiometricGate`, `CredentialHasher`, `ProgressiveLockoutPolicy`
- `core-ui`: `ProfilePickerTile` (existing component — reuse directly, do not rebuild)
- `core-data`: `FamilyRepository.observeChildren()` (existing `Flow<List<Child>>`)
- `core-navigation`: `Navigator`, `Route`

## 8. Files to Create
- `feature/onboarding/ui/ProfilePickerScreen.kt`
- `feature/onboarding/ui/ChildLockScreen.kt`
- `feature/onboarding/ui/LockRecoveryScreen.kt`
- `feature/onboarding/ui/FirstMissionScreen.kt`
- `feature/onboarding/viewmodel/ProfilePickerViewModel.kt`, `ChildLockViewModel.kt` (+ State/Event)
- `test/feature/onboarding/ProfilePickerViewModelTest.kt`, `ChildLockViewModelTest.kt`
- `androidTest/feature/onboarding/ProfilePickerScreenTest.kt`

## 9. Files to Modify
- `core-navigation/Route.kt` — add `ProfilePickerRoute`, `ChildLockRoute`, `LockRecoveryRoute`, `FirstMissionRoute`
- `core-datastore` or `core-database` — add a `firstMissionShown` per-child flag (confirm existing `ChildProfileEntity` doesn't already have a suitable field before adding a new one)

## 10. KMP Requirements
- `ProfilePickerViewModel` observes `FamilyRepository.observeChildren()` (existing reactive Flow) — filters out disabled children from the main grid (disabled children remain visible only within Parent Profile's own child-management view, which is out of scope here).
- Empty state (zero active children): render "Add Child" as the primary, prominent tile with friendly illustration — never render an error state for this specific, expected post-deletion scenario.
- Tile tap → check the tapped child's lock configuration (from `ChildProfile`/`ChildLock` data) → if configured, route to `ChildLockScreen`; if not, route straight to Child Home.
- `ChildLockViewModel.verify()` delegates entirely to `ChildLockRepository.verifyChildLock()` — do not reimplement local hash comparison or entitlement-grace-period logic in this ViewModel.
- Repeated lock failures → `ProgressiveLockoutPolicy` tiers (existing: 4th attempt 30s, 5th 5m, 6+ escalating) → after lockout or explicit "Forgot lock" tap, route to `LockRecoveryScreen`, which requires full Parent Profile re-verification (existing Parent-mode PIN/biometric gate, K-05's mechanism) — never a shortcut.
- First Mission: check a per-child "first mission shown" flag (local, since this is a first-session-only UI delight, not a server-tracked requirement) before rendering; set the flag immediately after first display so it never reappears, even across reinstalls if the flag can reasonably be synced — otherwise accept it as device-local-only and document that tradeoff explicitly.

## 11. Required API
- `GET /v1/identity/family/children` (B-06) — via existing `FamilyRepository.observeChildren()`

## 12. Local Data
Reuses existing `ChildProfileEntity`/`ChildLockDao` (per `core-database`'s existing schema) and `ChildLockRepository`'s cached entitlement snapshot (existing 7-day grace period mechanism) — this sub-feature adds only the new `firstMissionShown` flag if no equivalent exists.

## 13. Offline First
`ChildLockRepository.verifyChildLock()` is already documented as offline-tolerant (local hash + cached entitlement snapshot within grace period) — Profile Picker and Child Lock must both function fully offline as a result, consistent with existing architecture; do not introduce a network dependency into this flow that the existing repository doesn't already have.

## 14. Localization / RTL
Child name/avatar tiles render in the family's configured languages (per-child `preferred_language`, potentially differing from the parent's own selected app language) — verify tile grid RTL-mirrors correctly (grid flow direction, not just per-tile text).

## 15. Analytics
Emit `profile_picker_viewed` (child_count), `child_profile_selected` (child_id hashed, age_band), `child_lock_success`/`child_lock_failed` (lock_type), `lock_recovery_initiated`, `first_mission_shown` (content_id).

## 16. Performance
`ProfilePickerTile` grid must avoid unnecessary recomposition on unrelated state changes — use stable/immutable `Child` model (already `@Immutable` per `core-common`'s existing model conventions) and key the `LazyRow`/`LazyGrid` items by child ID.

## 17. Security
Lock verification never performs a raw plaintext comparison client-side — delegates entirely to `CredentialHasher`/`ChildLockRepository`'s existing hash-based verification. Lock Recovery never exposes a path that bypasses full Parent Profile re-verification.

## 18. Testing
- Unit: disabled-children-filtered-from-grid assertion; empty-state-not-error-state assertion for zero active children; lock-configured-vs-not routing branch; lockout-tier progression matches `ProgressiveLockoutPolicy` exactly; first-mission-shown-once assertion.
- UI: tile grid states (populated, empty/Add-Child-primary, loading); lock screen PIN/pattern/biometric variants per `lock_type`.
- Integration: full offline lock-verification path (airplane mode simulated) succeeds within the entitlement grace period, fails gracefully outside it.

## 19. AI Coding Agent Implementation Steps

**Task 01 — Wire Against `ChildLockRepository.verifyChildLock()`'s Documented Behavior**
Objective: Confirm the exact call signature (parameter/return types) of `verifyChildLock()` from the actual `core-data`/`core-database` source before wiring the ViewModel. **Resolved — existence and behavior already confirmed:** `CORE_DATA_INSTRUCTIONS.md`'s "Handling 'Child Mode' Entry" usage scenario explicitly documents this method as performing local hash verification plus a cached-entitlement-snapshot grace-period check (e.g., 7 days) — this is not in question. What remains genuinely open is only the *exact Kotlin signature* (parameter names/types, `NoorResult<T>` wrapping, suspend-vs-Flow), which the architecture doc's prose doesn't spell out precisely enough to write a compiling call site from documentation alone. Action: read the actual `ChildLockRepository`/`ChildLockDao` source file to pin down the exact signature before Task 04. Definition of Done: exact signature recorded in this task's notes; Task 04 calls the real method, not a guessed one.

**Task 02 — Implement `ProfilePickerViewModel`**
Objective: Observe `FamilyRepository.observeChildren()`, filter disabled children, drive empty-state-vs-populated rendering. Follow: `BaseViewModel`, existing reactive Flow pattern. Tests: filter and empty-state assertions. Definition of Done: zero-active-children renders the Add-Child-primary empty state, never an error.

**Task 03 — Implement `ProfilePickerScreen` with Existing `ProfilePickerTile`**
Objective: Grid layout reusing the existing `core-ui` component. Follow: `NoorHeroesTheme`, stable-keyed `LazyGrid`. Tests: covered by Task 02/08. Dependencies: Task 02. Definition of Done: no custom tile component built where `ProfilePickerTile` already suffices.

**Task 04 — Implement `ChildLockViewModel` Delegating to `ChildLockRepository`**
Objective: Thin ViewModel wrapping `verifyChildLock()`, surfacing `ProgressiveLockoutPolicy` state to the UI. Follow: `BaseViewModel`, existing lockout-tier constants — do not hardcode duplicate tier values. Tests: lockout-tier-progression-matches-policy-exactly assertion. Dependencies: Task 01. Definition of Done: zero reimplementation of hash-comparison or grace-period logic in this ViewModel.

**Task 05 — Implement Lock Screen Variants (PIN/Pattern/Biometric)**
Objective: Render the correct input UI per `lock_type`. Follow: `NoorPinInput`, `NoorPatternInput`, `BiometricGate`. Tests: per-variant UI test. Dependencies: Task 04. Definition of Done: all three `lock_type` values render correctly.

**Task 06 — Implement Lock Recovery via Full Parent Verification**
Objective: "Forgot lock" routes only through K-05's existing Parent Profile PIN/biometric gate, never a shortcut. Follow: existing Parent-mode verification entry point. Tests: no-bypass-path assertion. Dependencies: Task 04, K-05. Definition of Done: recovery is provably equivalent in strength to a normal Parent Profile unlock.

**Task 07 — Implement First Mission Screen and Once-Only Flag**
Objective: First-session-only content reveal. Follow: confirm/add the per-child flag per §9. Tests: shown-once assertion, including across a simulated re-launch. Dependencies: Task 01 (confirm no existing flag first). Definition of Done: flag set immediately on first display, screen never reappears in the same install.

**Task 08 — Add Analytics Instrumentation**
Objective: All events in §15. Follow: `AnalyticsTracker`, ViewModel-only, hashed `child_id`. Definition of Done: one call site per event, no raw child_id in any event payload.

**Task 09 — Add Full Test Suite**
Objective: Complete coverage per §18, including the offline-lock-verification integration test. Definition of Done: all green in CI.

**Task 10 — Final Code Review**
Objective: Confirm zero reimplementation of existing `core-data`/`core-security` lock logic, confirm Lock Recovery has no bypass path, confirm disabled-children filtering is correct. Definition of Done: checklist in §20 checked.

## 20. Final Verification Checklist
- [x] Disabled children hidden from the main Profile Picker grid
- [x] Zero-active-children renders as a friendly empty state, never an error
- [x] Lock verification delegates entirely to existing `ChildLockRepository`/`CredentialHasher` — no reimplementation
- [x] Lockout tiers match `ProgressiveLockoutPolicy` exactly, no duplicated/hardcoded values
- [x] "Forgot lock" always routes through full Parent Profile re-verification, no bypass
- [x] First Mission shown exactly once per child, flag set immediately on display
- [x] Full offline lock verification works within the existing entitlement grace period
- [x] `child_id` is hashed in all analytics events, never raw

## 21. Definition of Done
Profile Picker, Child Lock, Lock Recovery, and First Mission are live, correctly reusing existing `core-data`/`core-security` lock infrastructure rather than duplicating it, fully offline-tolerant, and this screen closes the loop on the entire A.1 onboarding feature — a returning parent now lands here directly from K-01's bootstrap routing. **(STATUS: IMPLEMENTED & VERIFIED)**
