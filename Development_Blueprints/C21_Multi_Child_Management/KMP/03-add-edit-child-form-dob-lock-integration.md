# K-03 — Add/Edit Child Form Integration (DOB Lock Handling)

## 1. Feature Context
Part of Feature C.21 — Multi-Child Management. Reuses A.1's shared Add/Edit Child form (`KMP/06-add-child-profile-flow.md`), extending it for the ongoing-management context with DOB-lock rendering and duplicate-nickname handling.

## 2. Parent Feature
C.21 Multi-Child Management

## 3. Sub-feature
**K-03 — Add/Edit Child Form Integration (DOB Lock Handling)**

## 4. Objective
Reuse the existing shared child form for both "+ Add Child" and per-child "Edit" from the management surface, correctly locking the DOB field once `dobLockedAt` is set, enforcing step-up before every mutating call, and surfacing duplicate-nickname/step-up-expiry errors inline.

## 5. Business Requirements
- FR-6: reuses A.1's field set.
- FR-7: DOB immutable after first save except via Support.
- FR-9: duplicate nicknames rejected inline with differentiation guidance.
- Edge Case #1: DOB edit attempt post-lock → field locked/read-only with explanation.
- Edge Case #7: step-up expires mid-form → fresh step-up prompt on save attempt, not silent failure.
- Android AI Prompt items 1-2: every mutating action requires `ParentGateLauncher.requireParentAuth` first; DOB field read-only whenever `dobLockedAt` is non-null.

## 6. Existing Architecture
Reuses `AddEditChildScreen` from A.1 (`KMP/06-add-child-profile-flow.md`), parameterized by an `entryContext: ChildFormEntryContext` (`Onboarding | Management`) so the same Composable serves both flows without duplication.

## 7. Existing Code to Reuse
- `AddEditChildScreen` (A.1) — the entire form UI and field-level validation; this sub-feature only adds parameterization, not a new screen.
- `ParentGateLauncher.requireParentAuth()` (C.19) — reused unmodified.
- `FamilyRepository` create/update methods (K-01's Task 01 extended to add `updateChild()`/`createChild()` wrapping B-02/B-03).

## 8. Files to Create
None if A.1's screen already supports parameterization; otherwise:
- `feature/child-management/src/commonMain/kotlin/.../ChildFormEntryContext.kt` (if not already defined in the shared onboarding module).

## 9. Files to Modify
- `AddEditChildScreen.kt` (A.1, shared module) — add `entryContext` parameter if not already present; render DOB field as read-only + tappable explanation whenever `dobLockedAt != null`, regardless of entry context.
- `core-data/.../FamilyRepositoryImpl.kt` — add `createChild()`/`updateChild()` wrapping B-03/B-02.
- `feature/child-management/.../ChildManagementViewModel.kt` — wire navigation into the shared form for both Add and Edit entry points.

## 10. Backend Requirements
Consumes B-02 (edit) and B-03 (create) exclusively.

## 11. KMP Requirements
- Every call to `createChild()`/`updateChild()` on the repository must be preceded by a successful `ParentGateLauncher.requireParentAuth()` call — enforced at the ViewModel layer, verified by a dedicated test asserting no repository method is reachable without it.
- DOB field: `enabled = (dobLockedAt == null)`; when disabled and tapped, show the DOB Locked-Field Explanation component (bottom sheet or inline expandable, per Figma).
- Duplicate-nickname: on `409 DUPLICATE_NICKNAME` from the repository call, surface an inline field-level error with differentiation guidance copy (not a generic toast).
- Step-up expiry mid-form: if `requireParentAuth()`'s cached grace window has lapsed by the time Save is tapped, re-trigger the step-up flow transparently before retrying the save — never silently fail or silently save without a valid step-up.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
Consumes B-02/B-03 contracts as documented in those blueprints.

## 14. Database Requirements
Local Room `Child` entity updated optimistically on successful save, matching K-09's cache-invalidation contract.

## 15. Validation
Client-side field validation mirrors but does not replace server-side validation (per the general principle that server-side is authoritative) — required fields, daily-goal bounds, nickname non-empty.

## 16. Authentication
Parent session required to reach the form at all.

## 17. Authorization
Step-up required before every save (create or edit) — no exceptions.

## 18. Error Handling
| Scenario | UI Behavior |
|---|---|
| `422 DOB_IMMUTABLE` (should be unreachable given client-side lock, but handle defensively) | Inline error, field forced read-only |
| `409 DUPLICATE_NICKNAME` | Inline field error with differentiation guidance |
| `403 PLAN_CAPACITY_EXCEEDED` (create only) | Route to K-07's blocked state |
| Step-up expired | Transparent re-prompt, then retry save |
| Network failure | Inline retry affordance, form state preserved |

## 19. Offline First
Save is blocked entirely while offline (mutating action); form data is retained locally so the parent doesn't lose entered data while reconnecting.

## 20. Local Data
Optimistic local update on success; rollback on failure per standard `SyncQueue`-adjacent error handling (though this call is synchronous/immediate, not queued, given it requires a live step-up token).

## 21. Localization
All labels, placeholders, and the DOB-lock explanation copy sourced from the localization dictionary across EN/HI/AR/UR.

## 22. RTL
Form layout, DOB picker, avatar grid, and interest chips all correctly mirrored under RTL.

## 23. Analytics
`child_edit_started`, `child_edit_saved`, `child_duplicate_nickname_rejected`, `child_dob_edit_attempted_blocked`, `child_add_initiated`, `child_add_completed`.

## 24. Performance
Reuses the existing A.1 form's performance characteristics; no new heavy computation introduced by this integration.

## 25. Security
Step-up-before-mutation is the primary control (Android AI Prompt item 1) — the write test for "no mutating method callable without a preceding step-up call" is the definitive security gate for this sub-feature.

## 26. Library Requirements
No new libraries — reuses A.1's existing form stack (Hilt/Koin, Retrofit/Ktor, Room).

## 27. Testing
- UI test: DOB field read-only when `dobLockedAt` non-null; editable when null (both existing-child and new-child cases, per Android AI Prompt item 2).
- UI test: no mutating repository method callable without a preceding `requireParentAuth()` call (Android AI Prompt item 1).
- UI test: duplicate-nickname inline error rendering.
- UI test: step-up-expiry mid-form triggers re-prompt, not silent failure.
- Unit: `ChildFormEntryContext` correctly parameterizes Add vs. Edit behavior without duplicating the screen.

## 28. Documentation
KDoc documenting the `entryContext` parameterization pattern so future features extending this shared form understand the contract.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Repository Wiring (`createChild`/`updateChild`)**
- **Objective:** Wrap B-02/B-03 in `:core:data`.
- **Files to Modify:** `FamilyRepositoryImpl.kt`.
- **Implementation Details:** Both methods require a step-up token parameter, sourced from `ParentGateLauncher`, passed through to `:core:network`'s request headers.
- **Tests:** Repository unit tests with a fake network layer for both success and `409`/`422`/`403` error paths.
- **Definition of Done:** Repository methods correctly propagate all documented backend error codes as typed `AppError` variants.

**Task 02 — DOB-Lock Rendering & Step-Up Gate**
- **Objective:** Extend `AddEditChildScreen` with lock rendering and the mandatory pre-save step-up call.
- **Files to Modify:** `AddEditChildScreen.kt`.
- **Implementation Details:** `enabled = dobLockedAt == null` on the DOB field; `ParentGateLauncher.requireParentAuth()` awaited before every `createChild`/`updateChild` call.
- **Security:** Write the "no mutating call without step-up" test first (TDD) to lock in the guarantee.
- **Tests:** Both UI tests per §27, item 1 and 2.
- **Definition of Done:** Both tests pass; verified on both new-child and existing-child (locked) cases.

**Task 03 — Duplicate-Nickname & Step-Up-Expiry Error Handling**
- **Objective:** Inline error surfaces for both cases.
- **Files to Modify:** `AddEditChildScreen.kt`, its ViewModel.
- **Implementation Details:** Map `409 DUPLICATE_NICKNAME` to a field-level error state; on step-up-expiry detection (a `401` from the mutating call specifically attributable to step-up), transparently re-invoke `requireParentAuth()` then retry the same save payload once.
- **Tests:** Both scenarios per §27.
- **Definition of Done:** Neither error case results in silent failure or silent success without proper handling.

## 30. Definition of Done
Shared form correctly serves both entry contexts; DOB lock, duplicate-nickname, and step-up-expiry are all handled per spec; step-up-before-mutation is provably enforced.

## 31. Final Verification Checklist
- [ ] DOB field lock behavior verified for both locked and unlocked cases
- [ ] No mutating repository call reachable without a preceding step-up call (tested)
- [ ] Duplicate-nickname inline error verified
- [ ] Step-up-expiry mid-form re-prompt verified (no silent failure/save)
- [ ] Plan-capacity-exceeded routes correctly to K-07
- [ ] Full localization and RTL verified
- [ ] Form reused (not duplicated) from A.1
