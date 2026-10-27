# K-13 — Parent AI/Microphone Permission Control (In-App)

## 1. Feature Context
Part of Feature A.5 (Quran & Arabic Learning), cross-referencing C.23 (Parental Controls). Lets a parent enable/disable AI pronunciation coaching/microphone features per child, which K-04's record-button gating and B-04's server-side enforcement both depend on.

## 2. Parent Feature
A.5 — Quran & Arabic Learning (cross-ref C.23 — Parental Controls)

## 3. Sub-feature
K-13 — Parent AI/Microphone Permission Control (In-App)

## 4. Objective
Provide the per-child AI/Microphone toggle within Parental Controls, persisted server-side, with mid-session-change handling that never leaves a child on a broken control.

## 5. Business Requirements
- FR-13: parent can disable microphone/AI per child (not just globally); when disabled, all recitation practice defaults to listen-and-self-assess app-wide for that child, no UI bypass path.
- Edge Case 2: mid-session disable applies at next session per the standing Parent Dashboard rule, but must never leave the child stuck on a broken control if it does interrupt mid-session.
- Permission States §1.15: OS-level permission + parent-level toggle both gate recording UI; either false routes to listen-only.

## 6. Existing Architecture
This screen lives within the app's existing Parental Controls module (owned by C.23, not newly created here) — confirm the exact existing Parental Controls screen/repository structure before wiring this feature-specific toggle into it, per Rule 30. `ParentalControlsRepository` (referenced throughout this feature's other blueprints, e.g., K-03, K-04) is assumed to already exist as part of C.23's implementation.

## 7. Existing Code to Reuse
- C.23's existing `ParentalControlsRepository` and Parental Controls screen/navigation structure — this blueprint adds a per-child AI/Mic toggle entry to that existing surface, not a new standalone screen architecture.
- `core-network`'s parent-session auth handling.

## 8. Files to Create
- `feature-learn/.../parentalcontrols/AiMicPermissionToggleSection.kt` (Composable section embedded within C.23's existing Parental Controls screen, not a standalone screen)
- `feature-learn-domain/.../UpdateAiMicPermissionUseCase.kt`
- `feature-learn/src/commonTest/kotlin/.../AiMicPermissionToggleTest.kt`

## 9. Files to Modify
- C.23's existing `ParentalControlsRepository` — extend with `getAiMicPermission(childId)`/`setAiMicPermission(childId, enabled)` if not already generically supported.
- C.23's existing Parental Controls screen — embed the new toggle section.

## 10. Backend Requirements
Consumes the existing Parental Controls service/table referenced throughout B-04's design (the exact endpoint is owned by C.23 — confirm its contract before assuming a shape; this blueprint does not introduce a new backend endpoint, it uses C.23's existing one).

## 11. KMP Requirements
- **Toggle rendering**: per-child AI/Microphone toggle within the existing Parental Controls surface.
- **Persistence**: writes via `ParentalControlsRepository`, confirmed server-side (the write must succeed against the backend before the UI reflects the new state — no optimistic-only update that could desync from B-04's server-side enforcement).
- **Scope enforcement**: when disabled, this is the single source of truth K-04's record-button gating reads from — no separate/duplicate toggle-reading logic anywhere else in the app.
- **Mid-session handling (Edge Case 2)**: the toggle change itself doesn't need special mid-session logic here — this is K-04's responsibility (re-checking on app-state resume) — this screen's job is simply to persist the change correctly and promptly.
- **Save failure**: clear error state, retry option, toggle UI does not silently appear to have saved if the write failed.

## 12. NextJS Requirements
N/A.

## 13. API Contract
Existing Parental Controls read/write endpoint (owned by C.23 — confirm exact contract, do not assume/invent).

## 14. Database Requirements
No new local persistence — reads/writes go directly through the existing `ParentalControlsRepository`, which may have its own caching strategy already established by C.23 (reuse it, don't duplicate).

## 15. Validation
N/A beyond standard toggle-state handling.

## 16. Authentication
Reuses existing parent-session auth.

## 17. Authorization
N/A beyond authenticated parent session with the child already resolved to their family (server-enforced).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Toggle save failure | Clear error state, retry option, UI does not falsely show success |
| Toggle read failure on screen load | Retry option, does not default to a silently-incorrect state |

## 19. Offline First
N/A (parent-session, connectivity-required write action).

## 20. Local Data
N/A beyond whatever caching C.23's existing `ParentalControlsRepository` already implements.

## 21. Localization
Toggle label/description localized via `core-common/localization`.

## 22. RTL
Full RTL layout, consistent with the rest of Parental Controls.

## 23. Analytics
`parent_ai_mic_permission_toggled` via `AnalyticsTracker`.

## 24. Performance
Lightweight, no special concerns.

## 25. Security
This toggle is a UX-layer convenience for K-04's client-side gating — the authoritative enforcement is always B-04's server-side re-validation on every recitation request, so a failure/inconsistency in this screen's persistence cannot be exploited to bypass the actual safety control (defense in depth, per B-04's design).

## 26. Library Requirements
Koin, Ktor, Compose Multiplatform.

## 27. Testing
- Unit: toggle write correctly calls `ParentalControlsRepository.setAiMicPermission()` and only reflects UI success after server confirmation (no optimistic-only update).
- Integration: toggle change is correctly readable by K-04's gating logic on next check (cross-feature consistency test).
- UI test: save failure shows a clear error state, not a false-success UI.

## 28. Documentation
KDoc noting this is the single source of truth for the per-child AI/Mic setting that K-04 reads — any future duplicate toggle-reading path elsewhere in the app is an architecture violation.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm C.23's Existing Parental Controls Structure**
- Task ID: K-13-T01
- Objective: Verify `ParentalControlsRepository`'s existing contract and the Parental Controls screen's existing composition structure before embedding this toggle.
- Dependencies: None (verification task, per Rule 30 — C.23 is a separate feature this blueprint depends on, not something to re-architect here).
- Definition of Done: Structure confirmed and documented in §6/§9.

**Task 02 — Extend `ParentalControlsRepository` (if needed)**
- Task ID: K-13-T02
- Files to Modify: C.23's existing repository (only if per-child AI/Mic support doesn't already generically exist there).
- Dependencies: K-13-T01.
- Definition of Done: `getAiMicPermission`/`setAiMicPermission` available and tested.

**Task 03 — Implement `UpdateAiMicPermissionUseCase`**
- Task ID: K-13-T03
- Dependencies: K-13-T02.
- Definition of Done: Use case unit-tested.

**Task 04 — Build `AiMicPermissionToggleSection` and Embed in C.23's Screen**
- Task ID: K-13-T04
- Files to Modify: C.23's existing Parental Controls screen.
- Dependencies: K-13-T01, K-13-T03.
- Definition of Done: Toggle renders and persists correctly within the existing Parental Controls surface.

**Task 05 — Cross-Feature Consistency Test with K-04**
- Task ID: K-13-T05
- Objective: Verify a toggle change here is correctly observed by K-04's record-button gating.
- Dependencies: K-13-T04, K-04.
- Definition of Done: Integration test confirms consistency.

**Task 06 — Tests**
- Task ID: K-13-T06
- Dependencies: K-13-T01–T05.
- Definition of Done: All green in CI.

## 30. Definition of Done
Per-child AI/Mic toggle live within C.23's existing Parental Controls surface, server-confirmed persistence, correctly consumed by K-04 as the single source of truth, fully tested.

## 31. Final Verification Checklist
- [ ] Toggle is embedded within C.23's existing Parental Controls surface, not a duplicate standalone screen
- [ ] Write only reflects UI success after server confirmation (no optimistic-only update)
- [ ] K-04's gating logic correctly reads this toggle as its single source of truth
- [ ] Save failure shows a clear error state, no false-success UI
- [ ] RTL/localization verified
- [ ] Full test suite green in CI
