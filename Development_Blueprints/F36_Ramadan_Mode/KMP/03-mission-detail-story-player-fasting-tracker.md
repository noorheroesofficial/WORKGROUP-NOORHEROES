# K-03 — Mission Detail, Story Player & Fasting Tracker

## 1. Feature Context
The night's actual content experience — story/lesson, dua of the night, and an optional fasting-log entry point — with the Fasting Tracker rendered strictly according to parent permission (hidden, not disabled) and a fast local UX check that never even offers a disallowed status.

## 2. Parent Feature
F.36 — Ramadan Mode

## 3. Sub-feature
2.3 Mission Detail, Story Player & Fasting Tracker (ID: **K-03**)

## 4. Objective
Build the Mission Detail screen, reuse A.3's Story Player, and implement the Fasting Tracker Toggle & Log component with client-side approach-aware UX and mission completion routed through `:core:reward-client`.

## 5. Business Requirements
- §1.18 Screens 5-7: Mission Detail (Ramadan), Ramadan Story Player, Fasting Tracker Toggle & Log.
- §1.15: Fasting Tracker visibility is parent-permissioned per child; hidden, not shown-disabled, if not enabled.
- §7 Android AI prompt item 2 (mandatory): mission completion calls `RewardRepository.reportCompletion()`.
- §7 Android AI prompt item 5 (mandatory): no "fasted_full" option offered for an `education_only` child.

## 6. Existing Architecture
`:feature:ramadan` module; Story Player reuses A.4's/A.3's existing player Composable and lifecycle-safe media handling — no new player implementation.

## 7. Existing Code to Reuse
- A.3's Story Player Composable/ViewModel
- A.4's media-playback lifecycle pattern (coroutine cancellation, memory-safe handling)
- `:core:reward-client`'s `RewardRepository.reportCompletion()`
- A.7's existing habit-log form component pattern (structural reference for the Fasting Tracker UI)

## 8. Files to Create
- `feature/ramadan/presentation/missiondetail/MissionDetailScreen.kt`
- `feature/ramadan/presentation/missiondetail/MissionDetailViewModel.kt`
- `feature/ramadan/presentation/fastingtracker/FastingTrackerComponent.kt`
- `feature/ramadan/domain/usecase/GetMissionDetailUseCase.kt`
- `feature/ramadan/domain/usecase/SubmitFastingLogUseCase.kt`
- `feature/ramadan/domain/usecase/CompleteMissionUseCase.kt` (shared with K-02, defined once)

## 9. Files to Modify
- `:core:navigation`'s nav-graph — register Mission Detail route from Journey Map

## 10. KMP Requirements
- **UI/Screen/Component:** Mission Detail screen composing Story Player + Dua-of-the-Night display + conditional Fasting Tracker entry point.
- **State/ViewModel:** `MissionDetailViewModel` holds the current night's content (from B-03), the child's `fasting_approach` and tracker-enabled flag (from K-07's synced parent settings), and completion state.
- **Fasting Tracker visibility:** rendered conditionally — entirely absent from the composition tree (not merely `enabled = false`) when the parent hasn't enabled it for the child, per §1.15's explicit hidden-not-disabled rule.
- **Fast local UX check (mandatory):** the tracker's status-selection UI offers only options allowed by the child's current `fasting_approach` — an `education_only` child is never shown a `fasted_full`/`fasted_practice` control at all (§7 item 5). This is a UX convenience only; B-04 is the actual authority and re-validates server-side.
- **Mission completion:** calls `CompleteMissionUseCase` → `:core:reward-client`'s `RewardRepository.reportCompletion()` exclusively (§7 item 2, mandatory).
- **Offline First:** pre-downloaded story/dua content playable offline; fasting-log submissions queue via B.15's outbox when offline.
- **Loading/Empty/Error:** loading state while fetching B-03's mission content; error state falls back to a retry prompt, never a blank player.

## 11. NextJS Requirements
N/A.

## 12. API Contract
`GET /v1/ramadan/missions/{night}` (B-03), `POST /v1/ramadan/fasting-logs` (B-04), `POST /v1/ramadan/missions/{night}/complete` (B-05's proposed contract, pending real sign-off — see B-05 §11; shared `CompleteMissionUseCase` with K-02, single definition, not duplicated here).

## 13. Database Requirements
Local cache for pre-downloaded mission content (story/dua assets) per B.15's existing offline-download pattern; outbox entries for queued fasting-log submissions.

## 14. Validation
Client-side approach-aware option filtering per §10 — mirrors but does not replace B-04's server-side enforcement.

## 15. Authentication
Standard child session token.

## 16. Authorization
Child may only submit fasting logs for themselves; tracker visibility gated by the parent-configured flag synced from K-07.

## 17. Error Handling
Fasting-log submission rejected server-side (e.g., a race where the parent just tightened the approach) → clear, child-safe, non-shaming error message, never a raw error code shown to the child.

## 18. Offline First
Covered in §10 — story/dua content and fasting-log submission both support offline-first operation via B.15's existing patterns.

## 19. Local Data
Cached mission content per night; outbox entries for fasting logs pending sync.

## 20. Localization
Story/dua text (already multi-locale via E.29's content pipeline), fasting-tracker labels, and UI copy fully localized across En/Hi/Ar/Ur.

## 21. RTL
Full RTL layout for Mission Detail and Fasting Tracker for Arabic/Urdu.

## 22. Analytics
`ramadan_fasting_log_entry_added`, `ramadan_fasting_approach_changed` (the latter observed, not emitted, by this module — cross-ref K-07) per §1.19.

## 23. Performance
Story Player reuses A.4's coroutine-cancellation-safe lifecycle handling to prevent leaked media resources on screen exit (per `CORE_CRASH_INSTRUCTIONS.md`); Fasting Tracker's conditional composition avoids recomposition thrash when the enabled-flag changes.

## 24. Security
Fasting Tracker's client-side option-filtering is UX-only; the module must never assume it is a security boundary — every submission still round-trips through B-04's server-side check.

## 26. Library Requirements
Kotlin, Jetpack Compose, Hilt, Retrofit + OkHttp, Room/SQLDelight. Reuses A.3/A.4's existing media-playback library — no new player library.

## 27. Testing
Unit: approach-aware option-filtering logic for all three approach levels. UI test: **mandatory** — no `fasted_full` option renders for an `education_only` child (§7 item 5). Integration: **mandatory** — mission completion calls `RewardRepository.reportCompletion()` via the exact shared call path (§7 item 2); Fasting Tracker fully absent from composition (not just disabled) when parent hasn't enabled it.

## 28. Documentation
KDoc noting the Fasting Tracker's hidden-not-disabled contract and its client-side-only enforcement status.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement `GetMissionDetailUseCase`**
Objective: Fetch B-03's mission content with offline-cache fallback. Files to Create: `domain/usecase/GetMissionDetailUseCase.kt`. Tests: use-case unit tests. Definition of Done: tests pass.

**Task 02 — Implement `MissionDetailViewModel`**
Objective: Combine content, approach/enabled-flag state, completion state. Files to Create: `presentation/missiondetail/MissionDetailViewModel.kt`. Dependencies: Task 01, K-07's synced settings state. Tests: state-derivation unit tests. Definition of Done: tests pass.

**Task 03 — Build `MissionDetailScreen` Reusing A.3's Story Player**
Objective: Compose Story Player + dua display + conditional tracker entry point. Files to Create: `presentation/missiondetail/MissionDetailScreen.kt`. Existing Files to Reuse: A.3's Story Player. Dependencies: Task 02. Tests: UI rendering tests. Definition of Done: tests pass.

**Task 04 — Implement `FastingTrackerComponent` with Approach-Aware Filtering**
Objective: Hidden-not-disabled visibility; option-filtering by approach. Files to Create: `presentation/fastingtracker/FastingTrackerComponent.kt`. Dependencies: Task 02. Tests: **mandatory** — no-`fasted_full`-for-`education_only` UI test; hidden-not-disabled composition test. Definition of Done: both pass.

**Task 05 — Implement `SubmitFastingLogUseCase`**
Objective: Calls B-04, queues via B.15's outbox when offline. Files to Create: `domain/usecase/SubmitFastingLogUseCase.kt`. Dependencies: Task 04. Tests: offline-queue test. Definition of Done: test passes.

**Task 06 — Implement Shared `CompleteMissionUseCase`**
Objective: Routes exclusively through `RewardRepository.reportCompletion()`, calling B-05's proposed `POST /v1/ramadan/missions/{night}/complete` (shared with K-02, single definition — do not re-implement in this module). Files to Create: `domain/usecase/CompleteMissionUseCase.kt` (only if not already created by K-02's Task 06; otherwise import). Dependencies: B-05's proposed contract (flag for re-verification once signed off). Tests: **mandatory** — exact call-path test. Definition of Done: test passes.

**Task 07 — Wire Navigation from Journey Map**
Objective: Route registration. Files to Modify: nav-graph. Dependencies: Task 03. Tests: navigation test. Definition of Done: test passes.

**Task 08 — Add Localization, Analytics, and Full Test Suite**
Objective: Complete §20/§22/§27 coverage, both mandatory tests included. Definition of Done: all green in CI.

**Task 09 — Final Code Review**
Objective: Confirm the Fasting Tracker's server round-trip is never bypassed and confirm hidden-not-disabled is enforced by composition, not a disabled-state prop. Definition of Done: checklist in §30 checked.

## 30. Final Verification Checklist
- [ ] No `fasted_full`/`fasted_practice` option rendered for an `education_only` child — mandatory test passing
- [ ] Mission completion calls `RewardRepository.reportCompletion()` via the exact shared path — mandatory test passing
- [ ] Fasting Tracker fully absent from composition (not disabled) when parent hasn't enabled it
- [ ] Story Player reuses A.3/A.4's lifecycle-safe playback with no leaked resources
- [ ] Offline-queued fasting logs sync and reconcile correctly

## 31. Definition of Done
Each night's content experience plays reliably offline-first, and its optional fasting log is presented with a UX that respects — but never substitutes for — the server's actual parent-configured enforcement.
