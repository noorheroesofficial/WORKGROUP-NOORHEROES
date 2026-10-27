# K-07 — Onboarding Draft Persistence, Resume & Offline Sync

> **Status:** ✅ **Implemented & Verified** (Live simulator verified on Android `emulator-5554` with live FastAPI backend)

## 1. Feature Context
The cross-cutting resilience layer underlying K-02 through K-06: a shared, nav-graph-scoped `OnboardingViewModel` that debounce-persists every field change, restores on process death, and resumes deep links — ensuring a parent is never forced to restart onboarding from Splash after a kill, crash, or network loss.

## 2. Parent Feature
Feature A.1 — Splash, Language Selection, Authentication & Onboarding

## 3. Sub-feature
2.7 Onboarding Draft Persistence, Resume & Offline Sync (ID: **K-07**)

## 4. Objective
Implement the shared `OnboardingViewModel` (draft state + persistence), deep-link resume validation, and the 30-day-background token-refresh-then-resume path, that K-03 and K-06 integrate with rather than building their own storage.

## 5. Business Requirements
- FR-16: Onboarding must be resumable from the last completed step after app kill, crash, or network loss — never restarted from scratch.
- Edge Case: Parent closes app mid-onboarding (after OTP, before Add Child) → reopens exactly at Add Child, not Splash.
- Edge Case: Connectivity lost exactly between OTP verify success and consent screen render → on reconnect, re-fetch session state via bootstrap and resume at the correct step (token already issued server-side).
- Edge Case: App backgrounded mid-Add-Child for >30 days → session token expired; silent refresh if valid, else re-login, then resume Add Child with previously entered draft data restored locally.
- §6.4 (Android Requirements): `OnboardingState` held in a shared ViewModel scoped to the nav graph, persisted to DataStore after every field change (debounced 500ms), restored via `SavedStateHandle` first, DataStore fallback second, cleared only on graph exit.
- §6.8: `noorheroes://onboarding/resume` deep link validated server-side via the existing session/registration token before resuming any step.

## 6. Existing Architecture
**Resolved architecture decision — persistence backing store:** `core-datastore`'s own instructions (`CORE_DATASTORE_INSTRUCTIONS.md`, §"What NOT to Add Here") are explicit: "❌ Complex Data: Use `core-database` (Room) for searchable or relational datasets" and "❌ Heavy Data: Do not store JSON blobs or large lists. Use `core-database`." The onboarding draft — registration fields, current step, and a *list* of per-child Add-Child sub-drafts each with its own idempotency key — is exactly the "complex/relational/list" shape that rule describes, not a simple key-value preference. Decision: this sub-feature uses `core-database` (Room) via a new `OnboardingDraftEntity` + DAO, following the exact `SafeDatabaseHelper.withTransaction()` write pattern `core-database` already documents for every other write path (e.g., `SyncQueueEntity`). `core-datastore`'s `PreferenceManager` is used only for the single, genuinely-simple "last completed step" marker if a fast synchronous read is needed at Splash-routing time — the full structured draft itself lives in Room.

## 7. Existing Code to Reuse
- `core-ui`: `BaseViewModel` (as the base for the graph-scoped `OnboardingViewModel`)
- `core-navigation`: `Navigator`, `Route` (for the deep-link resume target and `requiredAuthState` guard)
- `core-database`: `SafeDatabaseHelper.withTransaction()`, `SyncQueueDao`-equivalent DAO pattern — the confirmed backing store per §6
- `core-network`: `ConnectivityObserver` (auto-flush-on-reconnect trigger)

## 8. Files to Create
- `feature/onboarding/state/OnboardingViewModel.kt` — nav-graph-scoped shared ViewModel
- `feature/onboarding/state/OnboardingDraftState.kt` — the full draft data class (registration fields, current step, per-child Add-Child drafts, idempotency keys)
- `core-database/entity/OnboardingDraftEntity.kt`, `core-database/dao/OnboardingDraftDao.kt` — new Room entity/DAO, per §6's resolved decision
- `feature/onboarding/data/OnboardingDraftRepository.kt` — persistence abstraction wrapping `OnboardingDraftDao` via `SafeDatabaseHelper`
- `feature/onboarding/navigation/OnboardingResumeDeepLinkHandler.kt`
- `test/feature/onboarding/OnboardingViewModelTest.kt`
- `test/core-database/OnboardingDraftDaoTest.kt`
- `androidTest/feature/onboarding/OnboardingResumeIntegrationTest.kt` (Robolectric process-death simulation)

## 9. Files to Modify
- `core-navigation/Route.kt` — add `OnboardingResumeDeepLinkRoute` with `requiredAuthState` validation
- All K-02/K-03/K-05/K-06 ViewModels — inject/read from the shared `OnboardingViewModel` instance (scoped via the nav graph's `ViewModelStoreOwner`) rather than holding independent local draft state

## 10. KMP Requirements
- `OnboardingViewModel` is scoped to the onboarding nav graph (survives individual screen navigation within it, cleared only on graph exit — i.e., on reaching Profile Picker, per §6.3's "back-stack popped entirely, no back-navigation into onboarding after completion").
- Every field change across K-02/K-03/K-06 updates `OnboardingDraftState` and triggers a 500ms-debounced persist to the chosen store — debounce must coalesce rapid keystrokes into a single write, not write on every character.
- Restoration priority: `SavedStateHandle` first (same-process configuration change / low-memory kill), `OnboardingDraftRepository` (persisted store) second (full process death) — implement as a single `restore()` function trying both in order, never both simultaneously causing a merge-conflict.
- 30-day-background handling: on resume, check token validity; if expired, attempt silent refresh via `AuthRepository`; if refresh also fails, route to Login (K-03) with a "session expired" toast, but preserve the persisted draft locally so Add Child data is restored *after* re-authentication, not lost.
- Deep link `noorheroes://onboarding/resume`: validate the carried session/registration token server-side (via a bootstrap or equivalent existing-session check) *before* resuming any step — never trust the deep link's implicit "just resume" instruction without re-validating.
- Reconnect-triggered resume: on `ConnectivityObserver` reporting back online after a mid-flow drop (e.g., between OTP-verify and consent), re-fetch session state (bootstrap) and resume at the server-confirmed correct step, not just the client's last-known local step (server is the source of truth for *which* step is actually next, since some state — e.g., token issuance — is already committed server-side even if the client didn't see the response).

## 11. Required API
- `GET /v1/identity/bootstrap` (B-01) — used for the reconnect-resume re-sync check
- Whichever token-refresh endpoint the existing `AuthRepository` already exposes (existing, not new)

## 12. Local Data
Full onboarding draft: registration field values, current step marker, per-child Add-Child sub-drafts (including each child's reused idempotency key), consent toggle states pre-submission. Cleared entirely only on successful graph exit (Profile Picker reached).

## 13. Offline First
This entire sub-feature exists to make offline/interrupted onboarding safe — no user-entered data is ever lost to a network blip, app kill, or backgrounding, short of the user explicitly abandoning the flow or the 30-day token-expiry-with-failed-refresh case (which still preserves the draft, just requires re-auth).

## 14. Analytics
`onboarding_abandoned` (last_step, time_in_funnel_seconds) — emitted by whichever mechanism detects abandonment (likely a process-lifecycle hook or a server-side funnel-timeout inference by B-07's analytics rollup, not necessarily a client-side event at all if the client can't reliably detect "abandonment" vs. "backgrounded"; clarify this event's actual emission point during implementation rather than assuming client-side).

## 15. Performance
Debounce is critical here — verify with a test that rapid sequential field edits (e.g., typing a nickname character-by-character) result in a single persisted write, not N writes.

## 16. Testing
- Unit: debounce-coalescing (rapid edits → one write); restoration priority (`SavedStateHandle` vs. persisted-store precedence in both possible availability combinations); draft-cleared-only-on-graph-exit assertion.
- Integration (Robolectric, shared with K-03/K-06): full process-death-mid-Add-Child → relaunch → exact resume at Add Child with all previously entered fields intact, including the reused idempotency key.
- Integration: deep-link resume with a valid vs. invalid/expired token (invalid → routes to re-auth, never resumes blind).
- Integration: 30-day-expiry simulation — silent refresh success path and silent refresh failure path, both preserving the draft.

## 17. AI Coding Agent Implementation Steps

**Task 01 — Create `OnboardingDraftEntity` and `OnboardingDraftDao`**
Objective: Build the Room entity/DAO per §6's resolved decision (Room, not DataStore, for this structured/multi-child data shape). Follow: existing `core-database` entity/DAO conventions (mirrors `SyncQueueEntity`'s structure — a `familyId`-or-session-scoped row with a serialized nested payload for the per-child sub-drafts, indexed appropriately). Files to Create: `OnboardingDraftEntity.kt`, `OnboardingDraftDao.kt`. Tests: DAO round-trip test for the full nested shape (multiple child sub-drafts, each with its own idempotency key). Definition of Done: entity/DAO correctly persist and restore the complete nested draft shape via Room, not a JSON-blob-in-DataStore workaround.

**Task 02 — Implement `OnboardingDraftRepository`**
Objective: Persistence abstraction wrapping `OnboardingDraftDao` via `SafeDatabaseHelper.withTransaction()` (the same transactional-write pattern every other `core-database` write path already uses). Tests: write/read round-trip for the full draft shape including nested per-child data, executed through the repository (not the DAO directly, to confirm the transaction wrapper works end-to-end). Dependencies: Task 01. Definition of Done: repository correctly serializes/deserializes the complete `OnboardingDraftState` through `SafeDatabaseHelper`.

**Task 03 — Implement `OnboardingViewModel` with Debounced Persistence**
Objective: Nav-graph-scoped shared ViewModel, 500ms-debounced writes, `SavedStateHandle`-then-repository restoration priority. Follow: `BaseViewModel`, Kotlin Flow `debounce()` operator. Tests: debounce-coalescing test, restoration-priority test. Dependencies: Task 02. Definition of Done: rapid-edit test confirms single write; both restoration-source combinations tested.

**Task 04 — Wire K-02/K-03/K-05/K-06 to the Shared ViewModel**
Objective: Refactor those sub-features' local draft handling (if any was built ahead of this task) to read/write through the shared `OnboardingViewModel` instead. Files to Modify: relevant ViewModels from K-03/K-06 specifically (K-02 has minimal draft needs). Tests: cross-screen state continuity test (enter data on screen A, navigate to B and back, data intact). Dependencies: Task 03. Definition of Done: no sub-feature ViewModel holds its own independent persisted draft store.

**Task 05 — Implement 30-Day-Background Token Refresh & Resume**
Objective: On resume, check token validity, attempt silent refresh, fall back to re-login while preserving the draft. Follow: existing `AuthRepository` refresh mechanism. Tests: both refresh-success and refresh-failure paths, both preserving the draft. Dependencies: Task 03. Definition of Done: draft survives a simulated 30-day gap with failed refresh, re-populated correctly after re-login.

**Task 06 — Implement Deep Link Resume with Server-Side Validation**
Objective: `noorheroes://onboarding/resume` validated via bootstrap/existing session check before resuming any step — never blind-trust the deep link. Follow: `core-navigation`'s `Route.requiredAuthState` guard pattern. Tests: valid-token-resumes vs. invalid-token-routes-to-reauth. Dependencies: Task 03, B-01. Definition of Done: invalid/expired deep-link tokens never bypass re-authentication.

**Task 07 — Implement Reconnect-Triggered Server-State Resync**
Objective: On `ConnectivityObserver` reporting back online mid-flow, re-fetch bootstrap and resume at the *server-confirmed* step, not blindly the client's last local step. Follow: `ConnectivityObserver.observeConnectivity()`. Tests: simulated mid-flow disconnect/reconnect where the server already committed a step the client didn't locally record. Dependencies: Task 03, B-01. Definition of Done: server-side state wins over stale local state on reconnect.

**Task 08 — Add Full Test Suite**
Objective: Complete coverage per §16, including the joint Robolectric integration tests referenced by K-03/K-06. Definition of Done: all green in CI.

**Task 09 — Final Code Review**
Objective: Confirm the draft is persisted via Room (`OnboardingDraftEntity`/`OnboardingDraftDao`) throughout, not a DataStore JSON blob anywhere; confirm draft is cleared only on graph exit; confirm no sub-feature built a competing local draft mechanism. Definition of Done: checklist in §18 checked.

## 18. Final Verification Checklist
- [x] Draft persisted via `core-database` (Room), not a JSON blob in `core-datastore` — resolved per §6, no longer an open decision
- [x] Debounce coalesces rapid edits into a single write (tested)
- [x] Restoration tries `SavedStateHandle` first, persisted store second, never both simultaneously
- [x] Draft cleared only on successful graph exit (Profile Picker reached)
- [x] Deep-link resume always re-validates server-side before resuming any step
- [x] Reconnect-triggered resume trusts server state over stale local state
- [x] 30-day-background expiry preserves the draft through both refresh-success and refresh-failure paths
- [x] No K-02/K-03/K-05/K-06 ViewModel holds an independent, competing draft store

## 19. Definition of Done
A single, well-tested, nav-graph-scoped draft persistence layer exists and is the sole source of truth for onboarding resumability across all other KMP sub-features in this feature — a parent never loses entered data or restarts from Splash after any kill, crash, network loss, or extended backgrounding. **(STATUS: IMPLEMENTED & VERIFIED)**
