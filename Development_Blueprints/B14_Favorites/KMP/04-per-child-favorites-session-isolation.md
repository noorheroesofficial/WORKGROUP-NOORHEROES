# K-04 — Per-Child Favorites Session Isolation & Cache Invalidation

## 1. Feature Context
Part of Feature B.14 Favorites. Elevated to its own sub-feature because FR-4 designates per-child favorites isolation a hard, zero-exception platform guarantee with a PRD-mandated dedicated test — not folded into K-02/K-03 given its signature-guarantee status, consistent with how the platform treats other per-child isolation guarantees (A.7/A.11 Family Board pattern).

## 2. Parent Feature
B.14 Favorites (`PRD_Documents/Child App — Supporting (13-18)/Feature_B14_Favorites.md`)

## 3. Sub-feature
2.4 Per-Child Favorites Session Isolation & Cache Invalidation — `K-04`

## 4. Objective
Guarantee that switching the active child session on a shared device fully resets the Favorites experience to the newly active child's own data, with zero visual or data carryover, and that no code path can accidentally request or cache another child's favorites.

## 5. Business Requirements
- FR-4: favorites are strictly per-child, never shared across siblings, no UI surface anywhere merges them.
- Edge Case 3: switching Child A → Child B mid-session must fully reset the Favorites grid with zero carryover.
- Edge Case 8: Parent Preview mode is a legitimate single-child-scoped view, not a violation of FR-4.
- §6.10: UI test confirming switching the active child session and reopening Favorites shows only the newly-active child's favorites.

## 6. Existing Architecture
Builds directly on K-03's repository (no-external-`child_id` guarantee) and the app's existing "Switch Profile" session-management flow. **Resolved research finding — full trigger chain confirmed:** `SwitchProfileRow` UI → `ChildProfileViewModel.onSwitchProfileTapped()` → A.1 Lock Gate → `core-auth/SessionActivationRepository`'s registered state-clearing callbacks (confirmed via `B16_Child_Profile/KMP/04-switch-profile-parent-mode-gate-flow.md` and `C19_Parent_PIN_Biometric_Gate/KMP/05-session-activation-cross-profile-state-clearing.md` §9). This is not documented in `CORE_NAVIGATION_INSTRUCTIONS.md` itself (zero matches for "switch"/"profile" there) — the mechanism lives in the auth/profile feature blueprints, not the navigation core doc.

## 7. Existing Code to Reuse
- K-03's `FavoritesRepository` (session-derived `child_id`)
- `core-auth/SessionActivationRepository`'s state-clearing callback registration (confirmed mechanism, per §6) — register Favorites' cache-purge callback here, do not build a parallel switch-detection mechanism
- `SyncQueueDao` (for purging any stale queued actions tied to a now-inactive child, if applicable — see §18)

## 8. Files to Create
- Integration/UI test suite: `FavoritesSessionIsolationTest.kt` (CI-blocking per PRD DevOps requirements)

## 9. Files to Modify
- K-03's `FavoritesRepository`/local cache layer — hook into the existing session-switch event to trigger a full cache purge
- K-02's `FavoritesTabViewModel` — ensure it re-subscribes to the newly active session's data rather than retaining stale state across a switch

## 10. Backend Requirements
Relies on B-02's server-side strict `child_id` scoping as the ultimate backstop; this sub-feature is the client-side complement, not a replacement for server-side enforcement.

## 11. KMP Requirements
- On session-switch event, fully purge/reset the local favorites cache (no stale rows from the prior child visible even momentarily).
- `FavoritesTabViewModel` must not retain in-memory state across a session switch — re-initialize on the new session.
- Parent Preview mode must be recognized as a distinct, legitimate, single-child-scoped context — not treated as a second "active child" requiring isolation from itself, and never allowed to render more than one child's favorites simultaneously or comparatively.
- No repository or ViewModel method anywhere in K-02/K-03 may accept an externally-supplied `child_id` (re-verified here as a cross-cutting regression check, building on K-03's own guarantee).

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
No new endpoint — relies on B-02's existing strict scoping.

## 14. Database Requirements
Local cache purge on session-switch; no schema change beyond what K-03 already defines.

## 15. Validation
N/A (behavioral/session guarantee, not input validation).

## 16. Authentication
Relies on the existing session-switch mechanism's own re-authentication/re-scoping of the bearer token to the newly active child.

## 17. Authorization
**This sub-feature's defining property.** Client-side structural guarantee that no favorites data or in-flight request from Child A's session can leak into Child B's rendered UI after a switch, complementing B-02's server-side enforcement.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Session switch occurs mid-fetch (race condition) | In-flight request for the prior child is discarded/ignored on response; only the new session's request result is rendered |
| Stale queued `SyncQueue` action tied to a since-switched-away child | **Recommended default (not fully confirmed by an explicit doc statement, but grounded in real precedent):** still flush it. Other outbox entities in the codebase (`EquipOutboxEntry`, `HabitCheckInOutboxEntity`) are keyed by `child_id`, not "current session," and are not documented as being purged on switch — only Favorites' own *cache* is purged on switch (§9), not its outbox. Treat the queued favorite-toggle as still valid and eligible to flush whenever its owning child is reachable, active or not; get final sign-off from Android Architect before shipping since this is a recommendation extrapolated from precedent, not a literal documented rule. |

## 19. Offline First
Cache purge-on-switch must work correctly even while offline (no dependency on a network round trip to know a switch occurred — the switch event itself is local).

## 20. Local Data
Full local favorites cache purge on switch is this sub-feature's primary local-data responsibility.

## 21. Localization
N/A.

## 22. RTL
N/A.

## 23. Analytics
No new dedicated event beyond what K-02 already fires; optionally confirm whether a session-switch analytics event already exists platform-wide that this should correlate with (not independently verified — flagged, not assumed).

## 24. Performance
Cache purge must be near-instant (synchronous or fire-and-forget-but-guaranteed-before-next-render) to avoid a visible flash of stale data during the switch transition.

## 25. Security
This is fundamentally a security/privacy sub-feature — the client-side half of the platform's most safety-critical guarantee for this feature (child data never crossing sibling boundaries).

## 26. Library Requirements
Existing session-management infrastructure; no new library.

## 27. Testing
- Integration/UI test: switch Child A → Child B → reopen Favorites tab → assert only Child B's items render, zero Child A carryover (PRD §6.10, CI-blocking).
- Regression test: switch Child A → Child B → Child A → assert correct restoration with no residual state from the intermediate switch.
- Test: Parent Preview mode renders exactly one child's favorites, never a combined/comparative view.
- Test: in-flight request from a just-switched-away session does not populate the new session's UI.

## 28. Documentation
Explicitly document this as a CI-blocking, P0-severity guarantee in the module's test suite documentation, matching the PRD's rollback-trigger severity classification (§15.2: "any confirmed cross-child favorites leakage" is treated as P0).

## 29. AI Coding Agent Implementation Steps
**Task 01 — Register with `SessionActivationRepository`'s State-Clearing Callbacks.** Confirmed mechanism (§6/§7) — no discovery work needed, just registration.
**Task 02 — Hook Cache Purge into Session-Switch Event.** Full purge of K-03's local favorites cache via the Task 01 callback.
**Task 03 — Guard Against In-Flight Request Leakage.** Discard/ignore responses for requests initiated under a now-inactive session.
**Task 04 — Verify Parent Preview Mode Handling.** Confirm it renders single-child-scoped data only, never comparative.
**Task 05 — Confirm `SyncQueue` Flush-on-Stale-Session Behavior.** Apply the recommended default in §18 (still flush, keyed by `child_id` not session); get Android Architect sign-off before finalizing since it's precedent-based, not literally documented.
**Task 06 — Write CI-Blocking Isolation Test.** Per §27, treated as the highest-priority test in this entire feature.
**Task 07 — Final Code Review.** Cross-check K-02/K-03 for any remaining externally-passable `child_id` parameter.

## 30. Definition of Done
Switch-profile isolation test green and marked CI-blocking; regression restoration test green; Parent Preview test green; in-flight-request-discard test green.

## 31. Final Verification Checklist
- [ ] Full cache purge on session switch verified
- [ ] Zero visual/data carryover confirmed via CI-blocking test
- [ ] Parent Preview mode confirmed single-child-scoped only
- [ ] In-flight stale-session requests cannot populate the new session's UI
- [ ] No externally-passable `child_id` anywhere in K-02/K-03 (regression-checked)
- [ ] Treated with P0 severity in test/CI configuration, matching PRD §15.2
