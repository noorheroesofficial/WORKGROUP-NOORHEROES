# K-05 — Session Resume & Cold-Start Profile Resolution

## 1. Feature Context
Covers PRD Edge Case 6, previously unassigned in the initial B.16 breakdown: on a shared device, Child A's Profile is open, the OS backgrounds/kills the app, and it is reopened later. `ChildProfileScreen` must never render from a stale in-memory/cached reference to "whichever child was last drawn" — it must re-resolve against the actual current session on every cold start/process restore, deferring to Who Is Learning if that session is no longer valid.

## 2. Parent Feature
Feature B.16 — Child Profile (Bottom Tab)

## 3. Sub-feature
2.5 Session Resume & Cold-Start Profile Resolution (ID: **K-05**)

## 4. Objective
Ensure `ChildProfileViewModel` initialization always re-derives `child_id` from `:core:auth`'s current, authoritative session state — never from a Compose `rememberSaveable`/process-persisted UI value or a stale cached reference — on every cold start and process restoration, correctly distinguishing "same child, resume normally" from "session expired/changed, redirect to Who Is Learning."

## 5. Business Requirements
- Edge Case 6: two children share a device; Child A's Profile is open, the app is backgrounded/killed by the OS, then reopened later → the app must correctly re-resolve to whichever child's session was actually last active **server-side** (or require re-selection via Who Is Learning if the session has expired), never defaulting to a stale or incorrect child's Profile.
- This reinforces the platform-wide "No Lateral Sibling Access" guarantee at a specific, easy-to-overlook restoration boundary: a naive implementation that restores UI state from process-death savedInstanceState without re-validating against the live session could resurrect the wrong child's Profile.
- Consistent with FR-9's state-clearing requirement — restoration is a different code path from an in-app Switch Profile transition, but must uphold the identical guarantee (no residual/incorrect child data ever rendered).

## 6. Existing Architecture
Builds entirely on `:core:auth`'s existing session-state observable (per `CORE_DATA_INSTRUCTIONS.md`'s `AuthRepository`/`AuthState` pattern — the same mechanism the App Root/Scaffold already uses to route between Parent Mode, Child Mode, and Who Is Learning). K-05 does not introduce a new session-persistence mechanism; it ensures `:feature:profile` correctly *defers to* the existing one on every initialization, rather than trusting any of its own locally-remembered state.

## 7. Existing Code to Reuse
- `:core:auth` — `AuthRepository.observeAuthState()` (or equivalent existing `Flow<AuthState>`) as the single source of truth for "which child session, if any, is currently valid"
- App Root/Scaffold's existing session-based routing logic (the same logic that already decides Parent Mode vs. Child Mode vs. Who Is Learning at app launch) — K-05 aligns `ChildProfileViewModel`'s own initialization with this existing decision rather than making a second, competing decision
- K-01's existing `ChildProfileViewModel` (extended, not replaced) and its existing state-clearing mechanism (reused for the "session changed" branch)

## 8. Files to Create
- `test/feature/profile/ChildProfileSessionResumeTest.kt`
- `androidTest/feature/profile/ChildProfileColdStartRestorationTest.kt`

## 9. Files to Modify
- `feature/profile/viewmodel/ChildProfileViewModel.kt` (K-01) — remove any reliance on `SavedStateHandle`/process-persisted `child_id`-adjacent values for identity purposes; re-subscribe to `:core:auth`'s live session state on `init`
- `feature/profile/data/ProfileRepositoryImpl.kt` (K-01/K-02) — confirm `child_id` resolution reads the *current* session value at call time, not a value captured once and held stale across a process-death/restore cycle

## 10. KMP Requirements
- On `ChildProfileViewModel` construction (which happens fresh on every process restore, per standard Android ViewModel lifecycle — but the risk is specifically in any Compose-level `rememberSaveable` or manually-persisted `SavedStateHandle` value that could reintroduce a stale identity outside the ViewModel's own construction), the **first** action is to collect the current value from `:core:auth`'s session observable — never to trust a previously-serialized `child_id`-shaped value from `SavedStateHandle` as authoritative.
- Three resolution outcomes must be explicitly and distinctly handled:
  1. **Same child, session still valid** → resume normally, K-02's cached stats/K-03's cached locale render immediately (cache-then-refresh, unchanged from K-01/K-02's normal behavior).
  2. **Session expired/invalidated while backgrounded** (e.g., token expiry, parent-side disable per Edge Case 9, or a server-side session invalidation) → redirect to Who Is Learning, reusing K-01's existing disabled-session redirect path rather than inventing a second one.
  3. **A *different* child's session is now the active one** (e.g., another app instance/tab on a shared device switched sessions while this instance was backgrounded) → treat identically to an in-app Switch-Profile-success transition: fully clear any residual composed state and render the newly-active child's Profile from scratch, reusing K-01's/K-04's existing state-clearing mechanism.
- No UI-layer identity value (Compose state, `SavedStateHandle`) may be read as authoritative for "which child" — it may only be used for non-identity transient UI concerns (e.g., scroll position), and even that must be discarded if the resolved session on restore differs from the session at the time that transient state was captured.

## 11. Required API
None new — relies entirely on `:core:auth`'s existing session-validation mechanism (the same one backing K-01's `GET /v1/children/{id}/progress` `409 SESSION_INVALID` handling and A.1's session-refresh/validation calls).

## 12. Offline First
Session-state resolution itself must work correctly even when the device is offline at the moment of resume: `:core:auth`'s locally-cached session state (last known valid session, within its existing grace-period rules per A.1) is used to determine the resume outcome; a full network round-trip is not required simply to redraw the correct cached Profile screen, though a background refresh is still triggered once connectivity is available (consistent with K-02's cache-then-refresh pattern).

## 13. Local Data
No new local persistence introduced by K-05 itself — it is a correctness/ordering guarantee layered on top of K-01's and `:core:auth`'s existing local state, not a new data store.

## 14. Localization
Not applicable — this is a session-identity correctness concern, not a display concern.

## 15. RTL
Not applicable.

## 16. Analytics
No new dedicated events — outcome 2 (session expired on resume) reuses K-01's existing `disabled_session_redirect_triggered` internal signal; outcome 3 (different child now active) reuses the existing child-switch-adjacent event set from K-04 where applicable, so that this restoration path is observable through the same signals as its in-app equivalents rather than a parallel, harder-to-correlate event stream.

## 17. Performance
Session-state re-subscription on `ChildProfileViewModel` construction must be a lightweight `Flow` collection against `:core:auth`'s already-warm state, not a blocking network call on the main thread during cold start — the screen's existing skeleton-loading state (K-01) covers the brief resolution window.

## 18. Security
This is the sub-feature's defining concern: a restoration path that trusts stale UI-layer state instead of re-validating against the live session is a structurally identical risk to the IDOR-class issues guarded against in B-01/B-02 and K-01's structural `child_id`-derivation test — except manifesting at the client's process-lifecycle boundary rather than at an API call boundary. Both must be closed for the platform's "No Lateral Sibling Access" guarantee to hold end-to-end.

## 19. Testing
- Unit: `ChildProfileViewModel` constructed fresh (simulating process restore) with `:core:auth` reporting the *same* child's session still valid → resumes normally, no redirect, cached data renders immediately.
- Unit: `:core:auth` reporting the session as expired/invalidated at restore time → redirects to Who Is Learning via K-01's existing disabled-session path, not a new/duplicate path.
- Unit: `:core:auth` reporting a *different* child's session as now active at restore time → full state-clearing occurs (reusing K-01/K-04's mechanism), new child's Profile renders with zero residual data from the previously-open child.
- Integration (Robolectric or equivalent process-death simulation): simulate an actual Android process-death-and-restore cycle with `SavedStateHandle` populated from the prior instance, assert the restored `ChildProfileScreen` reflects the *live* session outcome, not any value implicitly carried over via `SavedStateHandle`.
- Regression: confirm K-01's/K-02's normal warm-resume (app merely backgrounded briefly, no process death, same child, valid session) behavior is unaffected — K-05 must not introduce unnecessary re-fetches or flicker on the common case.

## 20. AI Coding Agent Implementation Steps

**Task 01 — Audit Existing `ChildProfileViewModel` for Stale-Identity Risk**
Objective: Confirm whether any Compose `rememberSaveable`/`SavedStateHandle` value in K-01's implementation is currently read as identity-authoritative. Why: this task must run before any fix, since the exact risk surface depends on what K-01 actually shipped. Files to Read: `ChildProfileViewModel.kt`, `ChildProfileScreen.kt`. Definition of Done: risk surface documented in the PR description (either "confirmed clean, no stale-identity reads found" or "found N call sites requiring the fix in Task 02").

**Task 02 — Re-Derive `child_id` from Live Session State on Every Construction**
Objective: Ensure `ChildProfileViewModel.init` collects `:core:auth`'s current session observable as the sole identity source. Follow: existing `AuthRepository.observeAuthState()` consumption pattern used by App Root/Scaffold. Files to Modify: `ChildProfileViewModel.kt`. Business Rules: three-outcome resolution per §10. Dependencies: Task 01. Definition of Done: no code path in `:feature:profile` treats a `SavedStateHandle`-restored value as identity-authoritative.

**Task 03 — Implement the Three Resolution Outcomes**
Objective: Same-child-resume, session-expired-redirect, different-child-full-clear, each explicitly branched and each reusing existing K-01/K-04 mechanisms rather than new ones. Files to Modify: `ChildProfileViewModel.kt`. Tests: unit tests per §19 for each of the three outcomes. Dependencies: Task 02.

**Task 04 — Add Process-Death Restoration Integration Test**
Objective: Prove the fix under an actual simulated process-death-and-restore cycle, not just a unit-level construction test. Files to Create: `ChildProfileColdStartRestorationTest.kt`. Dependencies: Task 03. Definition of Done: test fails against the pre-fix implementation (if reproducible) and passes after.

**Task 05 — Add Regression Test for Normal Warm Resume**
Objective: Confirm no new re-fetch/flicker introduced on the common "briefly backgrounded, same child, valid session" case. Files to Create: `ChildProfileSessionResumeTest.kt`. Dependencies: Task 03.

**Task 06 — Final Code Review**
Objective: Confirm zero stale-identity read paths remain anywhere in `:feature:profile`, all three resolution outcomes correctly reuse existing K-01/K-04 mechanisms, and the common warm-resume case is unaffected. Definition of Done: checklist in §21 checked.

## 21. Final Verification Checklist
- [x] No `SavedStateHandle`/`rememberSaveable` value is treated as identity-authoritative anywhere in `:feature:profile`
- [x] `child_id` re-derived from `:core:auth`'s live session state on every `ChildProfileViewModel` construction
- [x] Same-child/valid-session resume renders normally with no unnecessary re-fetch
- [x] Session-expired-at-resume redirects to Who Is Learning via the existing disabled-session path (no duplicate path introduced)
- [x] Different-child-now-active-at-resume triggers full state-clearing identical in effect to an in-app Switch-Profile-success transition
- [x] Process-death-and-restore integration test passes
- [x] Warm-resume regression test confirms no new flicker/re-fetch on the common case

## 22. Definition of Done
`ChildProfileViewModel` correctly re-resolves identity against `:core:auth`'s live session state on every cold start and process restoration — never rendering a stale or incorrect child's Profile — closing PRD Edge Case 6 and completing the full B.16 Child Profile KMP sub-feature set (K-01 through K-05).

**Status:** COMPLETED (Verified via `ChildProfileSessionResumeTest`, `ChildProfileColdStartRestorationTest`, and full suite with 93/93 tests passing in `:feature:feature-profile:testAndroidHostTest`; 100% visual and interactive parity validated on Android simulator across all 8 design screens: Child Profile-01 to 08).
