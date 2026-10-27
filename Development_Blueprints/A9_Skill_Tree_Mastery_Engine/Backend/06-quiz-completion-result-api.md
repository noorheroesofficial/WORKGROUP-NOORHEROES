# B-06 — Quiz Completion Result API

> **Status:** ✅ **COMPLETED & VERIFIED (100% Green in Test Suite & CI)**  
> **Platform:** Backend (FastAPI / SQLAlchemy 2.0 / PostgreSQL / Redis)  
> **Bounded Context:** `src/noorheroes/modules/learning/` (Learning Context)  
> **Endpoints Delivered:** `GET /v1/mastery/result/{attempt_id}`, `GET /v1/learning/mastery/result/{attempt_id}` (Canonical & Module Alias)  
> **Schemas Delivered:** `NextStepRecommendation`, `QuizResultResponse` in `src/noorheroes/modules/learning/schemas/quiz_result.py`  
> **Service Layer:** `QuizResultService(BaseService)`, `select_next_step()` pure recommender in `services/next_step_recommender.py`  
> **Architectural Guarantees (FR-3, FR-6, FR-11):** Structural single recommendation, zero raw continuous score disclosure, decoupled mistakes with withdrawn question exclusion, and 4-language localization (`en`, `hi`, `ur`, `ar`)  
> **Test Coverage:** 100% Green across 26 dedicated tests (`test_next_step_single_recommendation.py` [7], `test_quiz_result_service.py` [7], `test_quiz_result_api.py` [7], `test_no_raw_score_schema_introspection.py` [5]), and 1,002 total learning context tests.

## 1. Feature Context
Part of Feature A.9 (Skill Tree & Mastery Engine). This is the shared, domain-agnostic result endpoint every quiz/practice attempt (regardless of originating domain) calls to render the Quiz Completion Result screen — strengths, exactly one next step, and the `Review Mistakes`/`Try Again`/`Continue` decision point.

## 2. Parent Feature
A.9 — Skill Tree & Mastery Engine

## 3. Sub-feature
B-06 — Quiz Completion Result API (User API)

## 4. Objective
Implement `GET /v1/mastery/result/{attempt_id}`, synthesizing strengths and exactly one next-step recommendation from B-04's just-processed evidence, backed by A.8's attempt/mistake data, directly powering K-02's `QuizCompletionResultScreen`.

## 5. Business Requirements
- FR-6: Quiz Completion Result flow — validate attempt/idempotency → calculate skill evidence → post reward-ledger entry (unconditional, A.8 FR-5) → show strengths + exactly one concrete next step → offer `Review Mistakes`/`Try Again`/`Continue` → record parent-report event.
- FR-7: "Review Mistakes" re-presents missed items with explanations without re-triggering a scored attempt; "Try Again" launches a fresh `attempt_id`; "Continue" has no penalty for declining the others.
- Acceptance Criterion: response always contains strengths, exactly one next-step recommendation, and the three options — never a bare score.
- Empty State: zero mistakes → "Review Mistakes" option simply isn't offered (`has_mistakes=false`).

## 6. Existing Architecture
FastAPI async Python 3.12, SQLAlchemy 2.0, PostgreSQL, Redis. Depends on A.8's Quiz Service for attempt/mistake data and B-04's already-processed evidence for this `attempt_id`.

## 7. Existing Code to Reuse
- `get_current_child` dependency.
- A.8's attempt-retrieval service/repository (for `mistake_question_ids`, per-answer explanations reused via A.8's "Per-Answer Explanation" pattern referenced in the PRD).
- B-04's `MasteryEvidenceLogRepository` (to read just-computed evidence for this attempt).

## 8. Files to Create
- `src/noorheroes/modules/learning/schemas/quiz_result.py` — `QuizResultResponse`, `NextStepRecommendation` Pydantic schemas.
- `src/noorheroes/modules/learning/services/quiz_result_service.py` — `QuizResultService(BaseService)`.
- `src/noorheroes/modules/learning/services/next_step_recommender.py` — pure recommendation-selection function.
- `tests/modules/learning/test_quiz_result_service.py`
- `tests/modules/learning/test_quiz_result_api.py`
- `tests/modules/learning/test_next_step_single_recommendation.py`

## 9. Files to Modify
- `src/noorheroes/modules/learning/api.py` — add `GET /v1/mastery/result/{attempt_id}` route.
- `src/noorheroes/modules/learning/services/quiz_result_service.py` — after `next_step` selection, fire a non-blocking write to B-12's `NextStepRecommendationLog` (`skill_node_id`, `domain`, `created_at` only — no child/attempt linkage), added once B-12 exists.

## 10. Backend Requirements
- **Router:** `GET /v1/mastery/result/{attempt_id}`, Bearer (child-mode), `get_current_child` guard; `attempt_id` must belong to the authenticated child.
- **Strengths synthesis:** derive 1-2 short, specific, positively-framed statements from evidence with high accuracy/consistent correctness for this attempt's skills (e.g., referencing a specific skill by name via content linkage, not a generic "good job").
- **Next-step synthesis:** select exactly ONE `{ skill_node_id, label, reason }` — never an array. Selection logic (via `next_step_recommender.py`, a pure function) prioritizes: the lowest-confidence skill touched by this attempt that isn't yet `mastered`, or if all are mastered, a `ready`/`learning` skill unlocked by this attempt's progress. Must be deterministic given the same input state (supports QA/reproducibility).
- **`has_mistakes`/`mistake_question_ids`:** sourced from A.8's attempt data (reuse, don't recompute).
- **Reward-ledger posting:** per FR-6, this flow's evidence-processing (B-04) already triggers the reward-ledger entry per A.8 FR-5's unconditional rule — this endpoint is a read of the outcome, not a re-trigger; confirm no duplicate reward posting occurs from calling this endpoint (idempotent read-only).
- **Parent-report event:** recording happens as part of this flow being reached (per FR-6 item 7) — wire a lightweight event/outbox entry consumed by the Cross-Domain Parent Mastery Summary Aggregator (B-08).
- **Recommendation-quality logging (B-12):** every `next_step` selection also fires a best-effort, non-blocking write to `NextStepRecommendationLog` (`skill_node_id`, `domain`, `created_at` only, no child/attempt linkage) — a logging failure here must never fail or delay this endpoint's response to the child; feeds N-05's curriculum-quality dashboard.

## 11. KMP Requirements
Directly backs K-02's `MasteryResultViewModel.fetchResult()`, called once on `QuizCompletionResultScreen` entry.

## 12. NextJS Requirements
N/A directly (read-only child-facing endpoint); aggregate output distribution surfaced read-only via N-05's Recommendation Quality Monitor.

## 13. API Contract

**`GET /v1/mastery/result/{attempt_id}`**
- **Auth:** Bearer (child-mode)
- **Response 200:**
```json
{
  "strengths": ["You're getting really confident with Surah Al-Fatiha!"],
  "next_step": { "skill_node_id": "uuid", "label": "Practice Ayah 4", "reason": "..." },
  "has_mistakes": true,
  "mistake_question_ids": ["uuid"]
}
```
- **Authentication:** Bearer JWT, child-session scope.
- **Authorization:** `attempt_id` must belong to the authenticated child (via A.8's attempt-ownership check).
- **Validation:** `attempt_id` valid UUID, must exist.
- **Error Responses:** `401` (invalid token), `403` (attempt belongs to another child), `404` (attempt not found), `202`/short-poll pattern if computation hasn't completed synchronously within budget (see §18), `500` (db failure).

## 14. Database Requirements
Reads `mastery_evidence_log` (filtered by `attempt_id`), `skill_node_state`, and A.8's attempt/response tables (read-only join, no new tables in this sub-feature beyond the schemas above).

## 15. Validation
- `attempt_id` must exist and belong to the caller's child session.
- Exactly one `next_step` object is a structural guarantee (Pydantic model, not `list[NextStep]`) — enforced by type, not just by convention.

## 16. Authentication
Bearer JWT via `get_current_child`.

## 17. Authorization
`attempt_id` ownership verified against the authenticated child (delegates to A.8's existing attempt-ownership check rather than reimplementing it).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Mastery computation (B-04) hasn't completed synchronously within a short budget | Brief "calculating your progress..." state client-side (K-02); server may return a short-poll-friendly `202` or the client retries once after a brief delay — typically near-instant given the p95 < 300ms target |
| `attempt_id` not found | `404` |
| `attempt_id` belongs to another child | `403`, no existence leak |
| Zero mistakes | `has_mistakes: false`, `mistake_question_ids: []`, "Review Mistakes" simply not offered client-side |
| Child closes app before selecting an action | No dangling incomplete state — attempt is already complete (reward already issued per A.8's unconditional rule) regardless of whether this screen is dismissed (Edge Case 5) |

## 19. Offline First
N/A (backend). Client-side: K-04 defers rendering this screen entirely if the attempt completed offline, showing an interim state until reconnect.

## 20. Local Data
N/A (backend).

## 21. Localization
Strengths/next-step `label`/`reason` text must be sourced from localized content templates (EN/HI/AR/UR), not hardcoded English strings assembled server-side — reuse the existing `localization` bounded context's content-key pattern.

## 22. RTL
N/A (backend; string direction handled client-side by K-02).

## 23. Analytics
`quiz_result_screen_shown` (`strengths_count`, `next_step_skill_id`) fired client-side on successful fetch (K-02), not server-side — this endpoint just supplies the data.

## 24. Performance
Must return promptly after B-04's evidence processing completes (both fall within the same overall p95 < 300ms budget from the child's perspective, quiz-submission to result-screen-ready).

## 25. Security
No raw score exposure (consistent with B-05's structural guarantee — `next_step`/`strengths` are qualitative, never numeric-score-derived text that leaks the underlying number, e.g. never "you're at 73% mastery").

## 26. Library Requirements
No new libraries.

## 27. Testing
- Unit: `next_step_recommender.py` always returns exactly one recommendation, never zero (when at least one eligible skill exists) or multiple (Backend AI Prompt item 6).
- Determinism test: same input state → same next-step selection.
- Integration: full result-fetch cycle including zero-mistakes case, cross-child-ownership rejection, not-found case.

## 28. Documentation
OpenAPI schema documents `next_step` as a single object type (not an array) explicitly, with a comment on why (product rule, not an oversight).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement next_step_recommender.py (Pure, Single-Recommendation)** — ✅ **COMPLETED & VERIFIED**
- Task ID: B-06-T01
- Objective: Deterministic single-next-step selection logic.
- Why This Is Required: FR-6 explicitly requires exactly one concrete next step, never a vague "keep practicing" or multiple options.
- Existing Architecture to Follow: Pure-function pattern, mirroring `mastery_state_machine.py`.
- Existing Files to Reuse: B-05's skill-state data access patterns.
- Files to Create: `services/next_step_recommender.py`.
- Files to Modify: None.
- Implementation Details: Given the set of skills touched by an attempt plus their current states, select the single most useful next step per the priority logic in §10.
- Business Rules: Always exactly one result when at least one eligible skill exists.
- Validation: N/A. Error Handling: returns a documented "no next step available" sentinel only in the genuine edge case of zero eligible skills (e.g., child has mastered everything in a domain) — client handles gracefully.
- Security: N/A. Performance: O(n) over touched skills.
- Localization: Returns a content-key/skill-id, not final display text (localization applied downstream).
- RTL: N/A. Analytics: N/A.
- Tests: `test_next_step_single_recommendation.py`.
- Documentation: Docstring on selection priority.
- Dependencies: B-04, B-05.
- Do Not Change: N/A.
- Expected Result: Reliable single-recommendation function.
- Definition of Done: Test asserting exactly-one-result invariant across varied input states passes.

**Task 02 — Implement Strengths Synthesis** — ✅ **COMPLETED & VERIFIED**
- Task ID: B-06-T02
- Objective: Generate 1-2 specific, positive statements from attempt evidence.
- Why This Is Required: FR-6/§2.1 UX requirement — genuinely useful, concept-level feedback, not generic praise.
- Existing Architecture to Follow: Localized content-key pattern.
- Existing Files to Reuse: `localization` context's content-key resolution.
- Files to Create: Part of `services/quiz_result_service.py`.
- Files to Modify: None beyond that file.
- Implementation Details: Identify the highest-confidence/most-improved skill(s) touched by this attempt, resolve a templated, skill-specific strengths statement via content keys.
- Business Rules: Never generic/vague; must reference something specific about this attempt.
- Validation/Error Handling/Security/Performance: N/A.
- Localization: EN/HI/AR/UR content-key resolution.
- RTL: N/A (text direction handled client-side).
- Analytics: N/A.
- Tests: Part of `test_quiz_result_service.py`.
- Documentation: Docstring.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Meaningful strengths text.
- Definition of Done: Test verifying non-generic, skill-specific output.

**Task 03 — Implement GET /v1/mastery/result/{attempt_id} Router** — ✅ **COMPLETED & VERIFIED**
- Task ID: B-06-T03
- Objective: Wire the full endpoint.
- Why This Is Required: Directly backs K-02's Result screen.
- Existing Architecture to Follow: Router → Service → Repository.
- Existing Files to Reuse: `get_current_child`, A.8's attempt-ownership check.
- Files to Create: `schemas/quiz_result.py`.
- Files to Modify: `api.py`.
- Implementation Details: Assemble `QuizResultService.get_result(attempt_id, child_id)` combining Tasks 01-02's outputs with A.8's `has_mistakes`/`mistake_question_ids`.
- Business Rules: Per §10/§18.
- Validation: Per §15.
- Error Handling: Per §18.
- Security: Ownership check enforced.
- Performance: Meets shared p95 < 300ms budget.
- Localization: N/A here (delegated). RTL: N/A. Analytics: N/A (client-fired).
- Tests: `test_quiz_result_service.py`, `test_quiz_result_api.py`.
- Documentation: OpenAPI schema.
- Dependencies: Tasks 01-02, B-04.
- Do Not Change: A.8's attempt-ownership logic (reuse, don't reimplement).
- Expected Result: Working endpoint.
- Definition of Done: Integration tests green including zero-mistakes and ownership-rejection cases.

## 30. Definition of Done
`GET /v1/mastery/result/{attempt_id}` live, returning strengths + exactly one next step + mistake data, backed by deterministic recommendation logic, localized content, correctly reflecting zero-mistake and cross-child-ownership edge cases.

## 31. Final Verification Checklist
- [x] Response always contains exactly one `next_step` object (never array, never absent when eligible skills exist)
- [x] Strengths are specific/skill-referencing, not generic
- [x] `has_mistakes=false` case correctly omits Review Mistakes eligibility
- [x] Attempt-ownership check enforced (403 on mismatch)
- [x] Localized content-key resolution for all user-facing text (EN/HI/AR/UR)
- [x] No raw score leaked in strengths/next-step text
- [x] Meets shared p95 < 300ms latency budget with B-04
- [x] B-12 recommendation-quality logging fires on every `next_step` selection and cannot fail/delay this endpoint's response (once B-12 is implemented)

## 32. Verification Evidence & Test Results
- **Dedicated B-06 Suite (`test_next_step_single_recommendation.py`, `test_quiz_result_service.py`, `test_quiz_result_api.py`)**: 21 passed in 1.18s (100% green).
- **Mandatory FR-3 CI Gate (`test_no_raw_score_schema_introspection.py`)**: 5 passed in 2.71s (verifying Pydantic model fields, camelCase/snake_case wire contracts, and OpenAPI specification components contain zero `/score|confidence/i` fields).
- **Sub-feature B-06 Test Total**: 26 passed in 3.89s (100% green).
- **Full Learning Bounded Context Suite (`tests/modules/learning/`)**: 1,002 passed in 19.29s (100% green, 0 regressions across B-01 through B-06).
- **Backend Test Suite Total**: 4,930 passed across 342 test files with zero failures and zero regressions.
