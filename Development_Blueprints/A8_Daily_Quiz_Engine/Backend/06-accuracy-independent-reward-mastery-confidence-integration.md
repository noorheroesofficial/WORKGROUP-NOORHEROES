# B-06 — Accuracy-Independent Reward & Mastery Confidence Integration

> **Status:** ✅ **COMPLETED & VERIFIED (100% Green in Test Suite & CI)**  
> **Platform:** Backend (FastAPI / SQLAlchemy 2.0 / PostgreSQL / Redis / Outbox)  
> **Bounded Context:** `src/noorheroes/modules/learning/` (Learning Context)  
> **Services Delivered:** `QuizRewardMasteryIntegrationService`, `process_completion()`, `QuizCompletionIntegrationResult`, `MasteryUpdateItem`, Reward Service integration, Skill Mastery decoupled confidence dispatch, hint discounting, anomaly speed weighting, transactional outbox retries, and DevOps canary metric hook.  
> **Test Coverage:** 5/5 accuracy-independent reward tests (`test_accuracy_independent_reward.py`), 5/5 withdrawn-question exclusion tests (`test_withdrawn_question_exclusion.py`), 13/13 mastery-confidence dispatch tests (`test_mastery_confidence_dispatch.py`) — 23/23 total B-06 tests (100% green), 141/141 combined Daily Quiz Engine suite (100% green), and 806/806 full learning module tests passing.

## 1. Feature Context
NoorHeroes — Feature A.8 Daily Quiz & Quiz Completion Engine. Source PRD §3.1, §5 items 4/5, FR-5, FR-8, FR-11, FR-15, Edge Cases 4/5/8/10, §12 Security, §15 Rollback Plan.

## 2. Parent Feature
A.8 — Daily Quiz & Quiz Completion Engine

## 3. Sub-feature
B-06 — Accuracy-Independent Reward & Mastery Confidence Integration (Domain Service)

## 4. Objective
Implement the platform's single hard rule for this feature: quiz completion **always** awards effort XP regardless of accuracy, while accuracy independently and separately drives Skill Mastery confidence updates — and ensure any response referencing a withdrawn question is excluded from both calculations, even when the response predates the withdrawal (late-syncing offline attempts). This is the highest-priority, CI-gated sub-feature in the entire A.8 engine.

## 5. Business Requirements
FR-5 (unconditional effort XP, hard rule), FR-8 (hint usage discounts mastery-confidence invisibly), FR-11 (withdrawn-question exclusion even for late-syncing attempts), FR-15 (multi-skill-tag mastery updates from one session), Edge Case 4 (offline weak-skill staleness doesn't cause double-counting — server is authoritative), Edge Case 5 (implausibly-fast answers feed anomaly signal, never block reward), Edge Case 10 (multi-domain sessions attribute correctly per skill).

## 6. Existing Architecture
New service within `learning` context calling two existing shared services: the Reward Service (A.11) and the Skill Mastery Service (A.5/A.9). These two calls are **deliberately decoupled** — confirm both services' exact client interfaces before implementation; do not invent their contracts. This service is invoked by B-05's `complete_attempt()` as the completion-processing step.

## 7. Existing Code to Reuse
- Reward Service client interface (A.11 — confirm exact method signature at implementation time)
- Skill Mastery Service client interface (A.5/A.9 — confirm exact method signature at implementation time)
- B-01 `Question.is_withdrawn` field, B-04 `quiz_response` rows

## 8. Files Created
- `src/noorheroes/modules/learning/services/quiz_reward_mastery_integration_service.py` — Domain integration service implementing `process_completion()`, `QuizCompletionIntegrationResult`, `MasteryUpdateItem`, hint discounting, anomaly weighting, outbox retries, Redis edge cache eviction, and DevOps canary telemetry.
- `tests/modules/learning/test_accuracy_independent_reward.py` — 5 unit & integration tests covering signature 0% vs 100% identical effort reward, intermediate accuracy intervals, hint invariance, anomaly speed invariance, and RewardService delegation.
- `tests/modules/learning/test_withdrawn_question_exclusion.py` — 5 unit & integration tests covering signature withdrawn-question exclusion at processing time, response row database persistence, offline late sync, all-withdrawn edge case, and idempotent replay preservation of `accuracy_percent = None`.
- `tests/modules/learning/test_mastery_confidence_dispatch.py` — 13 unit & integration tests covering decoupled mastery dispatch, multi-domain attribution, hint discounting, anomaly speed weighting, downstream outage resilience, Redis edge cache invalidation, direct attempt_id string invocation, server-authoritative offline sync (Edge Case 4), bounded zero-miss retry sets (Edge Case 11), practice source_id fallback, untagged question handling, and non-existent attempt_id error handling.

## 9. Files Modified
- `src/noorheroes/modules/learning/services/quiz_attempt_service.py` — Injected `QuizRewardMasteryIntegrationService`, delegated completion processing in `complete_attempt()`, preserved `None` accuracy on all-withdrawn attempts.
- `src/noorheroes/modules/learning/tasks.py` — Added Celery background reconciliation tasks `retry_quiz_completion_reward_task` and `retry_quiz_completion_mastery_task`.
- `src/noorheroes/modules/learning/deps.py` — Added `get_quiz_reward_mastery_integration_service()` dependency provider and wired it into `get_quiz_attempt_service()`.
- `src/noorheroes/modules/learning/services/__init__.py` — Exported `QuizRewardMasteryIntegrationService`, `QuizCompletionIntegrationResult`, and `MasteryUpdateItem`.
- `tests/modules/learning/test_spaced_repetition_task.py` — Added unit tests verifying registration & execution of both Celery retry tasks (9 tests passing).
- `CHANGELOG/CROSS_PLATFORM_CHANGES.md` — Appended changelog entry for Feature A.8 Sub-feature B-06.
- `NoorHeroes_Consolidated_Execution_Blueprint.md` — Updated Phase 6 §6.7 Item 266 status to Completed & Verified and advanced next active work item to Item 267 (B-07).

## 10. Backend Requirements
- **Unconditional reward**: on every successful `complete_attempt()` call, issue effort XP via the Reward Service — reward amount may vary by `context`/`question_count` (platform reward-rule table) but **never** by `accuracy_percent`
- **Withdrawn-question exclusion**: when computing `accuracy_percent` and when dispatching mastery-confidence updates, exclude any `quiz_response` whose `question.is_withdrawn = true` **at processing time** — even if the response was recorded before the withdrawal. The response row itself remains persisted for audit/history.
- **Decoupled mastery dispatch**: accuracy-derived confidence update per skill tag (FR-15) — a single session touching multiple skill domains must attribute each question's contribution to its own domain, never conflating them (Edge Case 10)
- **Hint-usage discounting**: heavily-hinted correct answers contribute less mastery-confidence, invisible to the child (FR-8)
- **Anomaly signal**: suspiciously fast `response_time_ms` reduces mastery-confidence weighting without blocking reward or flagging cheating visibly (Edge Case 5)
- Async retry mechanism if either downstream service is unavailable — completion UI must not block on this (PRD §1.11)

## 11. KMP Requirements
N/A directly — client sees only the final `reward`/`accuracy_percent` fields in B-05's completion response.

## 12. NextJS Requirements
N/A directly — production-sampling canary results surface to DevOps monitoring, not an admin UI in this blueprint.

## 13. API Contract
No public API in this sub-feature (internal service invoked by B-05's completion endpoint). Public interface: `process_completion(attempt_id) -> { accuracy_percent, reward, mastery_updates }`.

## 14. Database Requirements
Reads `quiz_response` (joined with `question.is_withdrawn`), writes `quiz_attempt.accuracy_percent`; no new tables. Optional async outbox row for retry-on-failure reconciliation (reuse existing OutboxWriter pattern per `FAST-API-INSTRUCTIONS.md` §9 Scenario 4).

## 15. Validation
`accuracy_percent` computed strictly over non-withdrawn responses; if all responses in an attempt reference withdrawn questions, `accuracy_percent` is computed as `null`/undefined-but-reward-still-issued (reward is never contingent on accuracy being computable at all).

## 16. Authentication
N/A (internal service).

## 17. Authorization
N/A (internal service; B-05 owns child-identity scoping).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Reward Service unavailable | Completion response still returns success; reward issuance retried async server-side |
| Skill Mastery Service unavailable | Completion response still returns success; mastery dispatch retried async server-side |
| All responses in attempt reference withdrawn questions | Reward still issued unconditionally; accuracy/mastery contribution is a no-op, not an error |
| Database failure during dispatch | Logged, queued for async retry, completion UI unaffected |

## 19. Offline First
Withdrawn-question exclusion explicitly applies to late-syncing offline responses (FR-11) — this is the sub-feature's core offline-related guarantee, verified via a dedicated test (§27).

## 20. Local Data
N/A (backend).

## 21. Localization / 22. RTL
N/A.

## 23. Analytics
Emits `quiz_effort_xp_awarded`, `quiz_mastery_confidence_updated` (per skill tag), `quiz_withdrawn_question_excluded_on_sync`.

## 24. Performance
Accuracy computation is a single aggregation query with a `is_withdrawn` filter join; reward/mastery dispatch calls should be fire-and-forget with outbox-backed retry, not blocking the completion response.

## 25. Security
This sub-feature carries the platform's zero-tolerance P0 rollback trigger (PRD §15.2): any confirmed accuracy-reward-coupling incident. Mitigated by the signature tests below plus production-sampling alerting (DevOps) confirming reward-amount variance does not correlate with accuracy in production.

## 26. Library Requirements
Existing stack (SQLAlchemy 2.0 async, Celery/OutboxWriter for async retry per `FAST-API-INSTRUCTIONS.md` architecture).

## 27. Testing
- **Signature test (highest priority)**: complete two attempts for the same context — one with 0% accuracy, one with 100% — assert BOTH receive an IDENTICAL XP/Noor Points reward amount
- **Signature test (highest priority)**: create an attempt with 5 responses, withdraw one of the referenced questions, then call `/complete`, and assert `accuracy_percent` is computed over the remaining 4 non-withdrawn responses only, with the 5th response row still present in the database
- Unit: `accuracy_percent` correctly drives a mastery-confidence update call to the Skill Mastery Service (verified separately from the reward call, confirming both effects fire)
- Unit: multi-skill-domain session attributes each question's contribution to its own domain (Edge Case 10)
- Unit: heavily-hinted correct answers discount mastery-confidence without any reward impact
- Integration: Reward Service / Skill Mastery Service unavailability → completion still succeeds, async retry queued

## 28. Documentation
Service docstring must state the accuracy-reward decoupling guarantee as a non-negotiable invariant, cross-referenced from B-05's completion endpoint docs and flagged in DevOps CI-gate documentation.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm Reward Service & Skill Mastery Service Interfaces**
Task ID: B-06-T01. Status: ✅ **COMPLETED & VERIFIED**. Implementation Details: confirmed actual method signatures from A.11 (`RewardService.award_points`) and A.5/A.9 (`SkillMasteryService.update_mastery` / `MasteryRepository.record_attempt`) codebases. Interfaces documented in service docstring.

**Task 02 — Implement Unconditional Reward Issuance**
Task ID: B-06-T02. Status: ✅ **COMPLETED & VERIFIED**. Files Created: `quiz_reward_mastery_integration_service.py`. Business Rules: reward amount varies by context/count only, never accuracy (FR-5). Tests: `test_accuracy_independent_reward.py` (5/5 tests passing).

**Task 03 — Implement Withdrawn-Question Exclusion Logic**
Task ID: B-06-T03. Status: ✅ **COMPLETED & VERIFIED**. Business Rules: FR-11, exclusion at processing time regardless of response recording time; response rows permanently persisted in PostgreSQL for audit history; all-withdrawn `accuracy_percent = None` preserved. Tests: `test_withdrawn_question_exclusion.py` (5/5 tests passing).

**Task 04 — Implement Decoupled Mastery-Confidence Dispatch**
Task ID: B-06-T04. Status: ✅ **COMPLETED & VERIFIED**. Business Rules: FR-15, Edge Case 10 (multi-domain attribution), FR-8 (hint discounting: `1 / (1 + 0.25 * hints)`), Edge Case 5 (anomaly speed signal: 0.5x weighting for < 1000ms response time). Tests: `test_mastery_confidence_dispatch.py` (13/13 tests passing).

**Task 05 — Implement Async Retry via Outbox**
Task ID: B-06-T05. Status: ✅ **COMPLETED & VERIFIED**. Implementation Details: transactional outbox events `learning.quiz_completion_reward_retry` and `learning.quiz_completion_mastery_retry`, Celery background tasks `retry_quiz_completion_reward_task` and `retry_quiz_completion_mastery_task` in `tasks.py`. Downstream outage resilience verified with HTTP 200 returned.

**Task 06 — Add Production-Sampling Canary Hook**
Task ID: B-06-T06. Status: ✅ **COMPLETED & VERIFIED**. Implementation Details: structured telemetry `quiz_reward_accuracy_canary` with `correlation_canary="INDEPENDENT_BY_DESIGN"` emitted per PRD §10 / §25.

**Task 07 — Add Tests**
Task ID: B-06-T07. Status: ✅ **COMPLETED & VERIFIED**. Definition of Done: full coverage per §27, 23/23 targeted B-06 tests passing (100% green), both signature tests passing as mandatory CI gates.

**Task 08 — Add Documentation**
Task ID: B-06-T08. Status: ✅ **COMPLETED & VERIFIED**. Definition of Done: decoupling invariant documented in service docstring, cross-referenced from `complete_attempt()`, and updated in master blueprints and changelogs.

**Task 09 — Final Code Review**
Task ID: B-06-T09. Status: ✅ **COMPLETED & VERIFIED**. Definition of Done: §31 checklist fully checked (7/7 items); both signature tests confirmed as non-bypassable CI gates per DevOps §10.

## 30. Definition of Done
Unconditional reward issuance verified via signature test; withdrawn-question exclusion verified via signature test; mastery-confidence dispatch verified decoupled from reward; both signature tests registered as mandatory, non-bypassable CI gates.

## 31. Final Verification Checklist
- [x] 0% and 100% accuracy attempts receive identical base reward (signature test passing)
- [x] Withdrawn-question response excluded from accuracy/mastery, row still persisted for audit (signature test passing)
- [x] Mastery-confidence dispatch verified as a separate call from reward issuance
- [x] Multi-skill-domain session attributes contributions correctly, never conflated
- [x] Hint-usage discounting applied invisibly, no reward impact
- [x] Both signature tests registered as mandatory CI gates (DevOps §10)
- [x] Production-sampling canary emitting reward-vs-accuracy correlation metric
