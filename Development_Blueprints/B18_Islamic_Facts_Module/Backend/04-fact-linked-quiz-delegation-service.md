# B-04 — Fact-Linked Quiz Delegation Service

## 1. Feature Context
Part of Feature B.18 (Islamic Facts Module). A thin delegation layer routing a fact's single linked question through A.8's existing Quiz Engine — this sub-feature deliberately contains almost no new logic; its entire purpose is to prevent a parallel quiz implementation from being built.

## 2. Parent Feature
B.18 — Islamic Facts Module

## 3. Sub-feature
1.4 Fact-Linked Quiz Delegation Service (ID: B-04) — **User API**

## 4. Objective
Implement `GET /v1/quizzes/fact/{fact_id}` as a thin parameterization of A.8's shared question-set assembly contract, with zero parallel quiz/scoring/retry logic.

## 5. Business Requirements
- FR-7: a fact's linked quiz item routes through the shared Quiz Engine (A.8) using the same five-question-type contract, parameterized for this context (typically 1 question); this module does not implement a parallel quiz mechanism.
- Edge Case 3: linked quiz question later withdrawn → already-recorded responses preserved for history but excluded from mastery/reward calculation (per A.8 FR-11/A.9 FR-10); this module's responsibility is simply to stop offering the link.
- Edge Case 9: offline, quiz needing online question-set assembly not pre-downloaded → clear "needs internet" state, not silent failure.

## 6. Existing Architecture
Delegates entirely to A.8's existing `QuestionSetAssemblyService` and `QuizDeliveryService` (A.8 B-02/B-03 in that feature's own breakdown). This sub-feature adds a single thin router function that constructs the appropriate `QuizContext` (domain=`islamic_facts`, question_count=1) and forwards the call — no new service class beyond a router-level adapter function.

## 7. Existing Code to Reuse
- A.8's `QuestionSetAssemblyService.assemble(context: QuizContext) -> QuizResponse` — the exact same method used by A.5/A.6/A.9's other domains.
- A.8's existing withdrawal-exclusion handling (question withdrawn → excluded from assembly automatically, per A.8's own FR-11).
- `core/deps.py` → `get_current_child`.

## 8. Files to Create
- `src/noorheroes/modules/content/api/facts_quiz_router.py` — thin adapter route `GET /v1/quizzes/fact/{fact_id}`.
- `tests/modules/content/test_fact_quiz_delegation.py` — reuse-verification test.

## 9. Files to Modify
- `src/noorheroes/api/router.py` — register the adapter route (or nest under existing `facts_router`).

## 10. Backend Requirements
- `GET /v1/quizzes/fact/{fact_id}`, auth `Depends(get_current_child)`.
- Resolves `fact.linked_quiz_question_id` via B-01's `FactRepository`.
- Constructs `QuizContext(domain="islamic_facts", question_ids=[linked_quiz_question_id], count=1)` and forwards to A.8's `QuestionSetAssemblyService.assemble()` — identical call shape used by other domains (A.5 Dua Recall, A.9, etc.).
- If `linked_quiz_question_id` is null or the question is withdrawn (A.8 handles withdrawal exclusion internally), respond with a `404 QUIZ_UNAVAILABLE` so the client hides/removes the quiz entry point (Edge Case 3).
- No local scoring, retry-set, or completion logic — response flows back through A.8's existing submission endpoint (`POST /v1/quizzes/{id}/responses`, unchanged, used as-is).

## 11. KMP Requirements
Consumed by K-02, which launches `:core:quiz-engine`'s existing `QuizSessionScreen`.

## 12. NextJS Requirements
N/A.

## 13. API Contract
**Endpoint:** `GET /v1/quizzes/fact/{fact_id}`
**Auth:** Bearer, child-mode
**Response 200:** Identical shape to A.8's general quiz-question-set contract (see A.8 B-03's API Contract), parameterized to 1 question.
**Error Codes:** `404 QUIZ_UNAVAILABLE` (no linked question, or linked question withdrawn), `404` (unknown fact_id), `401`.

## 14. Database Requirements
Reads only `fact.linked_quiz_question_id` (B-01); no writes. All quiz-domain persistence remains entirely within A.8's existing tables.

## 15. Validation
`fact_id` must be a valid UUID and resolve to a non-withdrawn fact; the linked question ID is passed through to A.8 without local re-validation of question content (A.8 owns that validation).

## 16. Authentication
`Depends(get_current_child)`.

## 17. Authorization
Standard child-session; no additional scoping.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| No `linked_quiz_question_id` set | `404 QUIZ_UNAVAILABLE` |
| Linked question withdrawn | `404 QUIZ_UNAVAILABLE` (A.8 signals withdrawal, this layer translates to a consistent facts-scoped error) |
| Unknown fact_id | `404` |
| A.8 assembly service failure | Propagates A.8's own error handling unchanged (no duplicate error-handling logic introduced here) |

## 19. Offline First
N/A — backend endpoint; offline "needs internet" UX is K-02's concern.

## 20. Local Data
N/A.

## 21. Localization
Delegated entirely to A.8's existing localized question content.

## 22. RTL
N/A at API layer.

## 23. Analytics
None emitted here directly; `fact_quiz_started`/`fact_quiz_completed` are K-02 client-side events tied to the shared quiz-engine's existing event pipeline.

## 24. Performance
Negligible overhead — single lookup plus a pass-through call to an already-optimized A.8 service.

## 25. Security
No new attack surface; inherits A.8's existing authorization/validation for quiz content.

## 26. Library Requirements
None new — reuses A.8's existing service/client code.

## 27. Testing
- Reuse-verification integration test: confirm this endpoint's response is byte-for-byte structurally identical (same schema) to a direct call into A.8's `QuestionSetAssemblyService`, proving no parallel implementation exists.
- Unit: `404 QUIZ_UNAVAILABLE` when `linked_quiz_question_id` is null.
- Unit: `404 QUIZ_UNAVAILABLE` when linked question is withdrawn.

## 28. Documentation
OpenAPI docstring noting this is a thin delegation to A.8's contract, with a cross-reference link to A.8's own quiz API documentation (avoid documentation duplication/drift).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement Adapter Route**
Objective: `GET /v1/quizzes/fact/{fact_id}` thin adapter.
Why Required: Provides the fact-scoped entry point without duplicating quiz logic.
Existing Architecture to Follow: A.8's `QuestionSetAssemblyService.assemble()` contract.
Existing Files to Reuse: A.8's service/client code (import, do not copy).
Files to Create: `api/facts_quiz_router.py`.
Business Rules: FR-7 (no parallel quiz mechanism).
Error Handling: §18.
Dependencies: B-01, A.8's existing `QuestionSetAssemblyService`.
Do Not Change: Any A.8 file — this is additive-only, consumption-side.
Expected Result: Adapter route functioning end-to-end.
Definition of Done: Passes Task 02 tests.

**Task 02 — Reuse-Verification Test**
Objective: Prove structural identity with A.8's contract.
Files to Create: `tests/modules/content/test_fact_quiz_delegation.py`.
Dependencies: Task 01.
Expected Result: Test asserts schema equivalence and confirms no local scoring logic exists.
Definition of Done: Test green, code review confirms zero duplicated quiz logic.

**Task 03 — Documentation**
Dependencies: Task 02.
Definition of Done: OpenAPI docs cross-reference A.8, no drift.

## 30. Definition of Done
- Zero parallel quiz/scoring/retry logic introduced.
- Withdrawal handled by translating A.8's signal, not reimplementing withdrawal logic.
- Reuse-verification test passes and is part of the CI-blocking suite for this module (alongside B-01's approval-gate test and B-05's domain-registration test).

## 31. Final Verification Checklist
- [ ] No new quiz scoring/retry/state-machine code introduced anywhere in this sub-feature
- [ ] Reuse-verification test confirms identical schema to A.8's own contract
- [ ] `404 QUIZ_UNAVAILABLE` verified for null and withdrawn linked-question cases
- [ ] Documentation cross-references A.8 rather than duplicating it
