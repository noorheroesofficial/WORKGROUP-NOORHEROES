# K-03 — Game Evidence & Reward Delegation

## 1. Feature Context
Part of **A.10 Games Module**. Covers the client-side delegation of session-completion evidence and reward submission to the existing shared `MasteryRepository`/`RewardRepository` — this module must contain zero parallel evidence-scoring or reward-calculation logic (PRD §6.4, §7 item 3).

## 2. Parent Feature
A.10 Games Module — KMP App (Android/iOS)

## 3. Sub-feature
**2.3 Game Evidence & Reward Delegation** `[K-03]`

## 4. Objective
On natural session completion, `GameSessionViewModel` calls the existing `MasteryRepository.submitEvidence()` (`:core:mastery-engine`, A.9) and `RewardRepository` (A.11) with correctly-shaped parameters, verified via structural reuse tests confirming no new, parallel submission logic exists anywhere in `:feature:games` (PRD §7 item 3).

## 5. Business Requirements
- FR-5: every completed session emits skill evidence via the shared A.9 contract — first-class, not a lesser signal.
- FR-6: participation reward accuracy-independent.
- §6.4 State Management: `GameSessionWrapper`'s ViewModel delegates to shared repository interfaces rather than implementing its own submission logic.
- §6.7 Offline Support: completion while offline queues evidence/reward submission via the shared outbox pattern already established in A.8/A.9.

## 6. Existing Architecture
**Unknown / Assumption flagged:** `:core:mastery-engine` (`MasteryRepository`) is referenced throughout the A.10 PRD as an existing A.9 module, but is not present in the currently reviewed `core-data`/`core-common` instruction docs (which document `AuthRepository`, `SyncQueue`, `PlaybackSyncRepository`, `HabitsRewardsRepository`, `ContentRepository`, `FamilyRepository` — no `MasteryRepository`). This blueprint defines the **calling contract** this module depends on (`MasteryRepository.submitEvidence(childId, evidence): NoorResult<Unit>`) and assumes it will exist per A.9's own KMP blueprint, following the exact same `NoorResult<T>`/`SyncQueue` conventions documented for `HabitsRewardsRepository.checkInHabit()` — the closest existing precedent for an accuracy-independent, offline-queueable reward-adjacent write action. **Do not implement a local stand-in for `MasteryRepository` — this module must fail its dependency check / block on integration until A.9's real implementation exists, not silently substitute mock logic in production code.**

## 7. Existing Code to Reuse
- `HabitsRewardsRepository.checkInHabit()` pattern (`core-data`) — structural precedent for "offline-queueable, accuracy/completion-triggered reward write."
- `SyncQueue.enqueue()` (`core-data/sync`) — used internally by `MasteryRepository`/`RewardRepository` implementations, not called directly by this feature module (this module calls the repository interface only, per the layer rule "Feature Modules → core-data, never → core-network/core-database directly").
- `NoorResult<T>` / `Outcome` (`core-common/result`).
- Idempotency key generation via `Ulid`/`generate_uuid4`-equivalent (`core-common/id`) for `client_request_id`.

## 8. Files to Create
```
feature/games/src/commonMain/kotlin/com/noorheroes/feature/games/session/GameSessionCompletionHandler.kt
feature/games/src/commonTest/kotlin/com/noorheroes/feature/games/session/GameEvidenceRewardDelegationTest.kt
feature/games/src/commonTest/kotlin/com/noorheroes/feature/games/session/StructuralReuseVerificationTest.kt
```

## 9. Files to Modify
```
feature/games/src/commonMain/kotlin/com/noorheroes/feature/games/session/GameSessionViewModel.kt  # wire completion handler
```
**Do Not Change:** `MasteryRepository`/`RewardRepository` implementations themselves — call their existing public interfaces only. No new evidence-scoring or reward-calculation code may be added anywhere in `:feature:games`.

## 10. Backend Requirements
None implemented here; the client-side counterpart to B-03's orchestration endpoint. `GameSessionCompletionHandler` calls `POST /v1/games/{game_id}/sessions/{session_id}/complete` (B-03) via `GamesRepository.completeSession()`, which internally triggers the server-side delegation to Mastery/Reward.

## 11. KMP Requirements
- `GameSessionCompletionHandler.onSessionComplete(gameId, sessionId, responses)`:
  1. Generates `client_request_id` (idempotency key) via existing ID utility.
  2. Calls `GamesRepository.completeSession(gameId, sessionId, responses, clientRequestId)` → internally calls B-03.
  3. On success, surfaces the reward result to `SessionCompletionScreen` for display.
  4. Does **not** independently call `MasteryRepository`/`RewardRepository` from this module — B-03's backend orchestration is the single source of truth for evidence/reward side effects (avoids client-side double-submission risk); this module's role is purely to invoke the completion endpoint and surface its result.

**Confirmed resolution to the PRD §6.4/§7 item 3 framing (previously flagged for architecture-owner confirmation):** `Feature_A9_Skill_Tree_Mastery_Engine.md` §3.4 states `POST /v1/mastery/evidence` is explicitly "internal, called by the Quiz Service on attempt completion" — i.e., backend-to-backend only. A.9's own KMP requirements (§6.4–§6.5) confirm `:core:mastery-engine`'s public client surface exposes only *read* methods (`MasteryRepository.getResult()`, `.getSkillStates()`); no client-callable `submitEvidence()` method is specified anywhere in A.9's Android contract. This is now a confirmed fact, not an assumption: there is no legitimate client-side entry point for evidence submission to call in the first place. The single-call design via `GamesRepository.completeSession()` → B-03 (which internally calls `POST /v1/mastery/evidence` server-side) is therefore the only correct integration point, matching A.8's identical pattern (its KMP layer likewise never calls a client-side mastery-submission method). No further architecture-owner sign-off is required on this point.

## 12. NextJS Requirements
N/A.

## 13. API Contract
Consumes `POST /v1/games/{game_id}/sessions/{session_id}/complete` exactly as defined in B-03 §13.

## 14. Database Requirements
N/A directly; offline queuing of the completion call is owned by K-05's outbox integration.

## 15. Validation
`client_request_id` generated once per session-completion attempt and reused on retry (never regenerated) to preserve idempotency across retries/offline-queue replay.

## 16. Authentication
Relies on existing child-session-scoped network client.

## 17. Authorization
N/A beyond B-03's server-side session-ownership check.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Completion API call fails (network) | Session Completion screen still shown to the child (non-blocking per PRD §1.11); call queued for retry via the shared outbox pattern (K-05) |
| Completion API returns `409` (already completed) | Treated as success client-side (idempotent-equivalent outcome), no error shown to child |
| Completion API returns `403`/`404` (session ownership/not-found) | Logged as an anomaly (should not occur in normal flow), generic fallback shown |

## 19. Offline First
```
GameSessionCompletionHandler
   ↓ (on natural completion)
GamesRepository.completeSession()
   ↓
SyncQueue.enqueue() [if offline] — reused via core-data's existing outbox pattern (K-05 owns full offline integration)
   ↓ (on reconnect)
Idempotent replay via client_request_id
```

## 20. Local Data
N/A directly (owned by K-05).

## 21. Localization
Reward-amount display text localized (number formatting per locale via `core-common/format`).

## 22. RTL
Reward display mirrors correctly for RTL locales.

## 23. Analytics
- `game_session_completed` (with `duration_ms`; `accuracy_percent` kept internal per PRD §1.19, not exposed in client-facing analytics payload beyond what's needed).
- `game_evidence_submitted` — fired on confirmed successful delegation (i.e., after B-03 returns success, not merely on request-send).
- `game_reward_awarded` — fired with the reward amount returned by B-03.

## 24. Performance
Single API call per completion (no redundant client-side evidence/reward calls) — this is itself a performance and correctness property given the discrepancy resolved in §11.

## 25. Security
No client-side reward or evidence calculation exists to secure — by design, all calculation happens server-side (B-03), eliminating an entire class of client-tampering risk.

## 26. Library Requirements
Kotlinx Coroutines/Flow, Kotlinx Serialization. No new dependencies.

## 27. Testing
- **Structural reuse-verification test (primary):** confirm `GameSessionCompletionHandler` and `GameSessionViewModel` contain no direct calls to `MasteryRepository`/`RewardRepository` — only to `GamesRepository.completeSession()` — using Mockito/MockK verification asserting zero interactions with those repositories.
- Unit: `client_request_id` generated once and reused across retries (not regenerated).
- Unit: `409` response treated as success client-side.
- Integration: offline completion queues via `SyncQueue`, replays idempotently on reconnect (coordinated with K-05).
- Integration: reward display correctly reflects the amount returned by B-03 regardless of session accuracy (low-accuracy fixture test).

## 28. Documentation
KDoc explicitly documenting the resolved discrepancy in §11 — why this module does not call `MasteryRepository`/`RewardRepository` directly, to prevent a future well-intentioned "fix" from reintroducing duplicate submission.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Extend GamesRepository with completeSession()**
- Objective: `suspend fun completeSession(gameId, sessionId, responses, clientRequestId): NoorResult<GameSessionCompletionResult>`.
- Definition of Done: maps B-03's `200`/`409`/`403`/`404`/`502` responses to appropriate `NoorResult`/`AppError` outcomes.

**Task 02 — Implement GameSessionCompletionHandler**
- Objective: Orchestrates idempotency-key generation + single `completeSession()` call per §11.
- Definition of Done: structural reuse-verification test (Task 05) passes.

**Task 03 — Wire Into GameSessionViewModel**
- Objective: On natural session end (not abandonment — see K-04), invoke `GameSessionCompletionHandler.onSessionComplete()`.
- Definition of Done: verified only called on natural completion path, not abandonment (cross-verified with K-04's tests).

**Task 04 — Implement Idempotency Key Reuse**
- Objective: Generate once, persist for the session's lifetime, reuse on any retry.
- Definition of Done: unit test confirms no regeneration across simulated retries.

**Task 05 — Add Structural Reuse-Verification Test (Primary Deliverable)**
- Objective: `StructuralReuseVerificationTest.kt` — Mockito/MockK verification of zero direct `MasteryRepository`/`RewardRepository` interactions from this module.
- Definition of Done: this test is treated as release-blocking, mirroring the backend's equivalent test in B-03.

**Task 06 — Add Error-Handling Tests**
- Objective: `409`-as-success, network-failure-queues-for-retry, `403`/`404` anomaly logging.

**Task 07 — Wire Analytics Events**
- Objective: `game_session_completed`, `game_evidence_submitted`, `game_reward_awarded` fired at the correct points (post-confirmation, not pre-request).

**Task 08 — Add Remaining Tests**
- Objective: Full suite per §27.

**Task 09 — Document the Discrepancy Resolution**
- Objective: KDoc explaining why direct Mastery/Reward repository calls were intentionally avoided.

**Task 10 — Final Code Review**
- Objective: Confirm zero parallel evidence/reward logic exists anywhere in `:feature:games`; confirm the §11 discrepancy has been explicitly signed off by the architecture owner before merge.
- Definition of Done: review checklist (§31) fully checked, including explicit confirmation of the §11 design resolution.

## 30. Definition of Done
- Session completion triggers exactly one API call (B-03), no direct client-side Mastery/Reward repository calls.
- Structural reuse-verification test passing and treated as release-blocking.
- Idempotency key generated once, reused correctly across retries.
- Reward display confirmed accuracy-independent via test.
- §11 discrepancy explicitly flagged and resolved with architecture-owner sign-off before merge.

## 31. Final Verification Checklist
- [ ] Structural reuse-verification test passing (zero direct Mastery/Reward repository calls from this module)
- [ ] Idempotency key generated once, reused on retry (not regenerated)
- [ ] `409` (already-completed) handled as success client-side
- [ ] Offline completion queues correctly and replays idempotently on reconnect
- [ ] Reward display confirmed accuracy-independent (low-accuracy fixture test)
- [ ] §11 PRD-vs-backend-contract discrepancy explicitly confirmed with architecture owner
- [ ] Analytics events fire only after confirmed success, not on request-send
- [ ] No files outside declared scope modified

---

## 32. Cross-Platform Dependencies
- Backend Dependency: B-03 (single orchestrated completion call — the only call this module makes).
- KMP Dependency: K-02 (invokes this handler on natural completion), K-04 (abandonment path must guarantee this handler is never called).
- Admin Dependency: None.
- Database Dependency: None client-side (server owns `mastery_evidence_log`/reward-ledger tables).
- External Service Dependency: None.
- Figma Dependency: None (logic-only module; visual result is rendered by K-02).
