# K-07 — Settings Exit Actions — Logout Guard & Account Deletion Entry Point

## 1. Feature Context
Part of Feature C.26. The two "leaving" actions on the Settings surface: logging out (with a data-loss-prevention check) and entering the account-deletion flow (a pure hand-off, not a reimplementation).

## 2. Parent Feature
C.26 Privacy, Consent, Account Security & Data Rights (Settings)

## 3. Sub-feature
**K-07 — Settings Exit Actions — Logout Guard & Account Deletion Entry Point**

## 4. Objective
Implement a logout confirmation gated on unsynced offline downloads (B.15), and an Account Deletion entry point that hands off to C.21's existing deletion flow behind a step-up gate — introducing no local reimplementation of either downstream concern.

## 5. Business Requirements
- FR-4: logout requires confirmation if any unsynced offline downloads exist.
- FR-3: export/deletion require step-up; deletion shows the 7-day grace period explicitly (owned by C.21, this screen only requires step-up before linking in).
- §1.18 Screen Inventory #17–18: Account Deletion Entry Point (component), Logout Confirmation (modal).

## 6. Existing Architecture
Within `:feature:parent-settings`. The unsynced-downloads check queries `:core:download-manager`/`:core:offline-sync`'s existing pending-sync state (owned by B.15) — confirm the exact existing query method before wiring, per rule 30. The deletion entry point navigates directly into C.21's existing deletion flow (per C.21 K-05, reached via `ParentGateLauncher.requireParentAuth()` first) — this sub-feature adds zero deletion logic itself.

**Note on scope ambiguity (flag, do not silently resolve):** the C.26 PRD describes this entry point as leading to "C.21's Account Deletion Flow," but the reviewed C.21 blueprints (B-06/K-05) implement **per-child profile deletion**, not whole-family-account deletion. If C.26's "Delete Account" is intended as a distinct, family-level action (closing the entire NoorHeroes account, not just removing one child), no such flow currently exists in the reviewed blueprints — confirm with the team whether "Account Deletion" here means "delete all children via C.21's existing per-child flow" or a genuinely new family-account-closure flow before implementing Task 03.

## 7. Existing Code to Reuse
- `:core:download-manager`/`:core:offline-sync`'s pending-sync query (B.15) — confirm exact method name.
- `ParentGateLauncher.requireParentAuth()` (C.19).
- C.21 K-05's deletion flow entry point/navigation route (or a to-be-confirmed family-level equivalent, per §6's flagged ambiguity).

## 8. Files to Create
- `feature/parent-settings/src/commonMain/kotlin/.../LogoutConfirmationDialog.kt`
- `feature/parent-settings/src/commonMain/kotlin/.../AccountDeletionEntryPoint.kt`

## 9. Files to Modify
- `SettingsScreen.kt` (K-01) — add the Logout action and Account Deletion entry point.

## 10. Backend Requirements
None new — this sub-feature calls existing B.15/C.19/C.21 client repositories only.

## 11. KMP Requirements
- On "Logout" tap: query B.15's pending-sync state; if any unsynced downloads exist, show `LogoutConfirmationDialog` first; if none, log out immediately — both paths tested independently.
- On "Delete Account" tap: route through `ParentGateLauncher.requireParentAuth()`, then navigate into C.21's existing flow (or the to-be-confirmed family-level flow per §6) — this component performs navigation only, no deletion logic.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
None new — consumes B.15's local pending-sync state and C.19/C.21's existing contracts only.

## 14. Database Requirements
None new.

## 15. Validation
None.

## 16. Authentication
Standard parent session for logout; step-up required before the deletion entry point hands off.

## 17. Authorization
Step-up gate before deletion hand-off; logout requires no special authorization.

## 18. Error Handling
| Scenario | UI Behavior |
|---|---|
| Pending-sync query fails | Fail safe — show the confirmation dialog rather than silently logging out (never risk silent data loss on a query failure) |
| Step-up cancelled on deletion entry | Return to Settings, no navigation into C.21's flow |

## 19. Offline First
Pending-sync check and logout both function offline (local state query, local session clear); the deletion entry point's downstream flow (C.21) requires connectivity, as established in that blueprint.

## 20. Local Data
Reads B.15's existing local pending-sync state only; writes nothing new.

## 21. Localization
Confirmation dialog text and deletion entry point label fully localized.

## 22. RTL
Full RTL layout for the confirmation dialog.

## 23. Analytics
`logout_unsynced_downloads_confirmation_shown`, `account_deletion_entry_point_tapped`.

## 24. Performance
Trivial — a single local state query and two lightweight composables.

## 25. Security
The deletion entry point's step-up gate is this sub-feature's only security-relevant control; it must never allow navigation into the deletion flow without a fresh step-up pass, consistent with FR-3.

## 26. Library Requirements
No new libraries.

## 27. Testing
- Integration test: no pending syncs → logs out immediately, no dialog shown.
- Integration test: pending syncs exist → confirmation dialog shown first, logout only proceeds on confirm.
- Integration test: pending-sync query failure → fails safe to showing the dialog, never silently logs out.
- Integration test: deletion entry point requires step-up before navigating into C.21's (or the confirmed family-level) flow.

## 28. Documentation
Document the §6 scope ambiguity prominently in code comments and the module README until resolved — do not let a future maintainer assume "Delete Account" definitely means "delete all children" without an explicit product decision on record.

## 29. AI Coding Agent Implementation Steps

**Task 00 — Confirm "Account Deletion" Scope (blocking)**
- **Objective:** Resolve whether this entry point targets C.21's existing per-child flow or a distinct, not-yet-built family-account-closure flow.
- **Definition of Done:** Written product/architecture confirmation obtained.

**Task 01 — Confirm B.15's Pending-Sync Query Method**
- **Objective:** Locate the exact existing method before wiring a guessed one.

**Task 02 — Logout Guard Implementation**
- **Files to Create:** `LogoutConfirmationDialog.kt`.
- **Tests:** both logout paths, plus the fail-safe-on-query-failure test.

**Task 03 — Account Deletion Entry Point**
- **Files to Create:** `AccountDeletionEntryPoint.kt`.
- **Dependencies:** Task 00.
- **Definition of Done:** Navigates only after step-up succeeds; zero deletion logic implemented locally.

**Task 04 — Wire Both Actions into `SettingsScreen`**

**Task 05 — Localization, RTL, Analytics, Full Test Suite**

## 30. Definition of Done
Logout correctly gates on unsynced downloads with a fail-safe default, and the Account Deletion entry point correctly hands off behind step-up — with the family-vs-per-child deletion scope ambiguity explicitly resolved (not assumed) before the entry point's final destination is wired.

## 31. Final Verification Checklist
- [ ] "Account Deletion" scope ambiguity resolved and documented (Task 00), not silently assumed
- [ ] Logout with pending syncs shows confirmation; without, logs out immediately
- [ ] Pending-sync query failure fails safe (shows dialog), never silently logs out
- [ ] Deletion entry point requires fresh step-up before navigating
- [ ] Zero deletion logic implemented locally in this sub-feature
- [ ] Full localization and RTL verified
