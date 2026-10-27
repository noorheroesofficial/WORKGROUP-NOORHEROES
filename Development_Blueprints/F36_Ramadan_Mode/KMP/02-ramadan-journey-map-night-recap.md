# K-02 — Ramadan Journey Map & Night Recap

## 1. Feature Context
The child's central 30-night progress visualization — the Lantern Progress Path — showing lit/unlit lantern states, special Laylatul Qadr markers, and a "tonight's mission" call-to-action, followed by a Night Recap after each completion.

## 2. Parent Feature
F.36 — Ramadan Mode

## 3. Sub-feature
2.2 Ramadan Journey Map & Night Recap (ID: **K-02**)

## 4. Objective
Build the Journey Map Composable rendering 30 lantern nodes from B-01/B-05 server state, plus the Night Recap screen, with full offline support and accessibility.

## 5. Business Requirements
- §1.18 Screens 3-4: Ramadan Journey Map (Lantern Progress Path), Night Recap.
- §2.2: node states — Default, Tonight's-mission-available, Night-completed, Laylatul-Qadr-active, Missed-night-still-completable; each lantern node's state announced clearly via screen reader (explicit accessibility requirement).
- Edge Case 5: missed nights remain completable retroactively, never locked out.
- §2.5: full image-generation prompt provided for this screen (En + Ar RTL).

## 6. Existing Architecture
`:feature:ramadan` module; Journey Map conceptually related to A.9's Skill Tree path pattern per §2.4 wireframe description — reuse A.9's path/node Composable pattern where structurally applicable rather than building a new list/graph layout from scratch.

## 7. Existing Code to Reuse
- A.9's Skill Tree path/node Composable pattern (structural reference)
- `:core:reward-client`'s `RewardRepository.reportCompletion()` (A.11) — completion triggers route through this, not a local call
- `:core:offline-sync`'s outbox pattern (B.15)

## 8. Files to Create
- `feature/ramadan/presentation/journeymap/RamadanJourneyMapScreen.kt`
- `feature/ramadan/presentation/journeymap/RamadanJourneyMapViewModel.kt`
- `feature/ramadan/presentation/journeymap/LanternNode.kt`
- `feature/ramadan/presentation/nightrecap/NightRecapScreen.kt`
- `feature/ramadan/domain/usecase/GetJourneyMapUseCase.kt`
- `feature/ramadan/domain/usecase/CompleteMissionUseCase.kt`

## 9. Files to Modify
- `:core:navigation`'s nav-graph — register Journey Map/Night Recap routes and `noorheroes://ramadan/night/{n}` deep link

## 10. KMP Requirements
- **UI/Screen:** 30-node Lantern Progress Path with the five states from §2.2; Night Recap screen shown immediately after a completion.
- **State/ViewModel:** `RamadanJourneyMapViewModel` derives node states from B-01's phase/night plus B-05's per-mission completion records — no local determination of which nights are Laylatul Qadr (server-flagged only, consumed from B-03's `gamification_suppressed` via K-04's shared state).
- **Use Case/Repository:** `GetJourneyMapUseCase`, `CompleteMissionUseCase` → `RamadanRepository`; `CompleteMissionUseCase` delegates the actual reward-eligible call to `:core:reward-client`'s `RewardRepository.reportCompletion()`.
- **Offline First/Sync/Retry:** pre-downloaded map/current-night content functions offline (B.15 pattern); completion actions taken offline queue via B.15's outbox and sync on reconnect, reconciling against B-05's idempotent server state (safe replay).
- **Loading/Empty/Error State:** loading skeleton for the 30-node map; empty/not-applicable rendering for pre-join nights (consistent with K-01); error state falls back to last-cached map.
- **Deep Linking:** `noorheroes://ramadan/night/{n}` opens directly to that night's position on the map.

## 11. NextJS Requirements
N/A.

## 12. API Contract
`GET /v1/ramadan/missions/{night}` (B-03, for tonight's mission detail hand-off to K-03); `POST /v1/ramadan/missions/{night}/complete` (B-05's proposed contract, pending real sign-off — see B-05 §11) → `{ mission_id, child_id, completed_at, already_completed, reward }`. `CompleteMissionUseCase` treats `already_completed: true` as a normal success response (safe-replay UX, never an error toast), matching B-05's idempotent-replay guarantee.

## 13. Database Requirements
Local cache: `RamadanJourneyProgressCacheEntity(child_id, mission_id, night_number, completed_at, synced)` for offline-first rendering and outbox reconciliation.

## 14. Validation
N/A beyond standard response validation.

## 15. Authentication
Standard child session token via `:core:network`.

## 16. Authorization
N/A beyond standard session validity — child views only their own progress.

## 17. Error Handling
Map-fetch failure → render last-cached state with a subtle "offline/stale" indicator rather than a blank screen.

## 18. Offline First
Covered in §10 — this is one of the module's two primary offline-first surfaces (alongside K-03).

## 19. Local Data
`RamadanJourneyProgressCacheEntity` per §13; outbox entries for unsynced completions per B.15's existing pattern.

## 20. Localization
"Night X of 30" counter, node state labels, and Night Recap copy fully localized across En/Hi/Ar/Ur.

## 21. RTL
Full RTL mirroring of the path layout direction for Arabic/Urdu, per the §2.5 Arabic image-generation prompt provided in the PRD.

## 22. Analytics
`ramadan_journey_map_viewed`, `ramadan_night_mission_completed`, `ramadan_lantern_lit` per §1.19.

## 23. Performance
30-node list uses stable, keyed Composable items to avoid full-list recomposition on a single-node state change; avoid main-thread work during node-state diffing; large-list scroll performance verified on lower-end devices per `CORE_CRASH_INSTRUCTIONS.md`'s ANR-prevention guidance.

## 24. Security
No sensitive data; completion calls authenticated via existing session token, never accepting a client-supplied reward amount or badge ID.

## 26. Library Requirements
Kotlin, Jetpack Compose, Hilt, Retrofit + OkHttp, Room/SQLDelight. No new libraries.

## 27. Testing
Unit: node-state derivation for all five states across the 30-night range. UI test: **mandatory** — each lantern node's state is exposed via `contentDescription`/semantics for screen-reader announcement (§2.2 explicit accessibility requirement). Integration: **mandatory** — full mission-completion → `RewardRepository.reportCompletion()` → lantern-lit flow (§6.10); offline queue-then-sync reconciliation test.

## 28. Documentation
KDoc noting the Journey Map's structural reuse of A.9's path pattern and the mandatory accessibility contract per node.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement `GetJourneyMapUseCase` and Repository Wiring**
Objective: Combine B-01 phase/night with B-05 completion records into map state. Files to Create: `domain/usecase/GetJourneyMapUseCase.kt`. Tests: use-case unit tests. Definition of Done: tests pass.

**Task 02 — Implement Local Cache Entity and Outbox Integration**
Objective: Offline-first read + queued-completion write. Files to Create: cache entity, outbox wiring in `:core:offline-sync`. Dependencies: Task 01. Tests: offline read/write tests. Definition of Done: tests pass.

**Task 03 — Implement `RamadanJourneyMapViewModel`**
Objective: Stable, immutable 30-node state derivation. Files to Create: `presentation/journeymap/RamadanJourneyMapViewModel.kt`. Dependencies: Task 01, Task 02. Tests: five-state derivation unit tests. Definition of Done: tests pass.

**Task 04 — Build `LanternNode` Composable with Accessibility**
Objective: Per-node semantics/`contentDescription` for all five states. Files to Create: `presentation/journeymap/LanternNode.kt`. Dependencies: Task 03. Tests: **mandatory** — accessibility semantics test. Definition of Done: test passes.

**Task 05 — Build `RamadanJourneyMapScreen`**
Objective: 30-node scrollable path layout, RTL-aware. Files to Create: `presentation/journeymap/RamadanJourneyMapScreen.kt`. Dependencies: Task 04. Tests: RTL layout test. Definition of Done: test passes.

**Task 06 — Implement `CompleteMissionUseCase` via `:core:reward-client`**
Objective: Completion routes exclusively through `RewardRepository.reportCompletion()`, calling B-05's proposed `POST /v1/ramadan/missions/{night}/complete` (§12) and treating `already_completed: true` as a normal success. Files to Create: `domain/usecase/CompleteMissionUseCase.kt`. Dependencies: B-05's proposed contract (flag for re-verification once signed off). Tests: **mandatory** — exact call-path test; idempotent-replay-renders-as-success test. Definition of Done: tests pass.

**Task 07 — Build Night Recap Screen**
Objective: Post-completion recap. Files to Create: `presentation/nightrecap/NightRecapScreen.kt`. Dependencies: Task 06. Tests: UI test. Definition of Done: test passes.

**Task 08 — Wire Navigation and Deep Link**
Objective: `noorheroes://ramadan/night/{n}`. Files to Modify: nav-graph. Dependencies: Task 05, Task 07. Tests: deep-link test. Definition of Done: test passes.

**Task 09 — Add Analytics, Localization, and Full Test Suite**
Objective: Complete §21/§22/§27 coverage. Definition of Done: all green in CI.

**Task 10 — Final Code Review**
Objective: Confirm no local determination of Laylatul Qadr nights; confirm offline-sync reconciliation is idempotent-safe against B-05. Definition of Done: checklist in §30 checked.

## 30. Final Verification Checklist
- [ ] All five node states render correctly and are screen-reader announced — mandatory test passing
- [ ] Full mission-completion → reward-engine → lantern-lit flow verified — mandatory test passing
- [ ] Offline queue-then-sync reconciles correctly against B-05's idempotent server state
- [ ] Missed nights remain visibly, functionally completable, never locked out
- [ ] Full RTL mirroring verified against the provided Arabic image-generation prompt

## 31. Definition of Done
Children see a clear, accessible, offline-resilient 30-night progress map that never shames a missed night and always routes rewards through the platform's one existing engine.
