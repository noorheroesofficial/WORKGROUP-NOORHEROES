# B-02 — Question-Set Assembly Engine

> **Status:** ✅ **COMPLETED & VERIFIED (100% Green in Test Suite & CI)**  
> **Platform:** Backend (FastAPI / SQLAlchemy 2.0 / PostgreSQL / Redis)  
> **Bounded Context:** `src/noorheroes/modules/learning/` (Learning Context)  
> **Services Delivered:** `QuizAssemblyService`, `WeakSkillPoolProvider`, `AssembledQuizSet`, `WeakSkillCandidate`  
> **Test Coverage:** 22/22 unit & integration tests (`tests/modules/learning/test_quiz_assembly_service.py`), 45/45 quiz engine suite tests passing in 0.48s.

## 1. Feature Context
NoorHeroes — Feature A.8 Daily Quiz & Quiz Completion Engine. Source PRD §3.1, §3.2, §5 item 1, FR-1, Edge Cases 1/2/6/7.

## 2. Parent Feature
A.8 — Daily Quiz & Quiz Completion Engine

## 3. Sub-feature
B-02 — Question-Set Assembly Engine (Domain Service)

## 4. Objective
Implement a deterministic, explainable question-set assembly function that mixes recently-learned content and weak-skill pools into a balanced set, parameterized by `(child_id, context, target_question_count)`, forming the core selection logic every context-specific delivery endpoint (B-03) calls into.

## 5. Business Requirements
FR-1 (exactly 5 for Daily Quiz, context-parameterized elsewhere), Edge Case 1 (empty weak-skill pool fallback), Edge Case 2 (deterministic prioritization when weak-skill candidates exceed slots), Edge Case 6 (avoid exact-repeat within a short window across contexts), Edge Case 7 (media-load-failure backfill/graceful reduction), NFR performance target (assembly p95 < 500ms).

## 6. Existing Architecture
New domain service within the existing `learning` context (`src/noorheroes/modules/learning/services/`), following the Domain Service Layer pattern (`BaseService` subclasses, business rules) documented in `FAST-API-INSTRUCTIONS.md` §1. Reads from B-01's `Question`/`QuestionSkillTag` repository and from the Skill Mastery Service (A.5/A.9) for weak-skill pool data — does not duplicate mastery-state storage.

## 7. Existing Code to Reuse
- B-01 `QuestionRepository.find_by_type_and_status()`, `find_by_skill_tags()`
- Skill Mastery Service client/interface (A.5/A.9 — confirm exact interface at implementation time; do not invent its contract)
- Redis client (`core/deps.py` Redis pool) for assembly-result caching

## 8. Files to Create
- `src/noorheroes/modules/learning/services/quiz_assembly_service.py`
- `src/noorheroes/modules/learning/services/weak_skill_pool_provider.py`
- `src/noorheroes/modules/learning/services/__init__.py`
- `tests/modules/learning/test_quiz_assembly_service.py`
- `tests/modules/learning/fixtures/deterministic_weak_skill_fixture.py`
- `tests/modules/learning/fixtures/__init__.py`

## 9. Files to Modify
- `src/noorheroes/core/exceptions.py` (added `AssemblyUnavailableError` HTTP 503, `InvalidQuizContextError` HTTP 400)
- `src/noorheroes/core/i18n.py` (added `ASSEMBLY_UNAVAILABLE` localization across `en`, `hi`, `ur`, `ar`)
- `src/noorheroes/modules/learning/repositories/question_repository.py` (added `get_by_ids`, `find_published_questions`)
- `src/noorheroes/modules/learning/deps.py` (registered `get_weak_skill_pool_provider`, `WeakSkillPoolProviderDep`, `get_quiz_assembly_service`, `QuizAssemblyServiceDep`)
- `src/noorheroes/modules/learning/schemas.py` (re-exported `AssembledQuizSet`, `WeakSkillCandidate`)
- `src/noorheroes/modules/learning/__init__.py` (re-exported assembly services and models)

## 10. Backend Requirements
- `assemble(child_id, context, target_question_count) -> list[question_id]` — deterministic, no random selection
- Mix ratio: recent-content pool + weak-skill pool (exact split e.g. 3 recent / 2 weak for Daily Quiz's 5, per PRD §3.4 example `source_mix`)
- Fallback to default foundational-question mix when weak-skill pool is empty (Edge Case 1) — must still return exactly `target_question_count` questions
- Deterministic priority ordering (e.g., recency-of-weakness descending) when weak-skill candidates exceed available slots (Edge Case 2)
- Avoid selecting the exact same `question_id` for the same child within a short time window (e.g., same hour) across different contexts (Edge Case 6)
- Support backfill when a question is excluded post-assembly due to client-reported media failure (Edge Case 7) — assembly service exposes a `backfill_one(exclude_question_id, ...)` method

## 11. KMP Requirements
N/A directly — consumed via B-03's API response.

## 12. NextJS Requirements
N/A directly — aggregate output surfaced read-only via N-04's distribution monitor (B-07's endpoint reads this service's historical output, not live internals).

## 13. API Contract
No public API in this sub-feature (internal service, invoked by B-03). Exposes `assemble()` and `backfill_one()` as the module's public interface.

## 14. Database Requirements
Reads `question`, `question_skill_tag` (B-01); no new tables. May persist assembly-audit rows for QA explainability (optional: `quiz_assembly_log` — confirm against Skill Mastery Service's existing weak-skill audit trail before adding a parallel table).

## 15. Validation
`target_question_count` must be a positive integer; `context` must be one of the four known values (`home_daily`, `story_post`, `learn_practice`, `dua_recall`); assembly must never return fewer than `target_question_count` unless the entire bank for that context is genuinely smaller (documented degraded case, logged as a warning).

## 16. Authentication
N/A (internal service, not directly exposed).

## 17. Authorization
N/A (internal service; B-03 owns child-identity scoping before calling in).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Skill Mastery Service unavailable | Fall back to cached/default deterministic set (per PRD §1.11) rather than blocking quiz access |
| Weak-skill pool empty | Fallback foundational mix (Edge Case 1) |
| Question bank insufficient for context | Return best-effort smaller set, log warning, never throw a hard error to the caller |
| Database failure during pool query | Propagate as a typed `AssemblyUnavailableError` for B-03 to translate into its graceful-fallback response |

## 19. Offline First
N/A directly (server-side); assembly output is what K-06 bundles into offline content packages via B-03/B-08-equivalent download-manifest integration (owned by each consuming feature's own offline spec, e.g. A.3/A.5/A.6).

## 20. Local Data
N/A (backend).

## 21. Localization / 22. RTL
N/A (assembly selects `question_id`s only; localized content resolution happens at B-03's response-building step using B-01's payload).

## 23. Analytics
Assembly `source_mix` (recent vs. weak-skill counts) is returned to B-03 for inclusion in the `quiz_started` event payload; feeds N-04's aggregate topic-distribution dashboard.

## 24. Performance
p95 < 500ms hard target (PRD §1.8 NFR); Redis caching of per-child-per-context in-progress assembly result (paired with B-03's idempotent-resume requirement — the assembly is computed once per attempt, not per GET call); indexed repository queries only, no full-table scans.

## 25. Security
No new attack surface (internal service); determinism requirement itself is a QA/debugging integrity control, not a security control, but is treated with equivalent rigor per PRD §5 item 1.

## 26. Library Requirements
SQLAlchemy 2.0 async, Redis (existing pool), existing stack — no new dependencies.

## 27. Testing
- Unit: identical input state → identical assembled set every time (no randomness) — the signature test for this sub-feature
- Unit: weak-skill pool empty → fallback foundational mix, exactly `target_question_count` returned
- Unit: weak-skill candidates > slots → deterministic priority ordering verified against a fixed fixture
- Unit: exact-repeat avoidance within short time window across two contexts
- Integration: against staging deterministic weak-skill-pool fixture (DevOps §10 requirement)
- Performance: p95 < 500ms under representative load

## 28. Documentation
Service docstring must explicitly document the determinism guarantee and the priority-ordering algorithm in plain language, since QA/debugging trust in this system depends on it being explainable (PRD Edge Case 2).

## 29. AI Coding Agent Implementation Steps

**Task 01 — Implement Weak-Skill Pool Provider**
Task ID: B-02-T01. Files to Create: `weak_skill_pool_provider.py`. Dependencies: Skill Mastery Service interface (A.5/A.9). Definition of Done: returns ranked weak-skill candidates for a given child, empty-pool case handled.
- **Status:** ✅ Completed & Verified (`WeakSkillPoolProvider` computes priority scores and recency with Redis caching and graceful fallback).

**Task 02 — Implement Recent-Content Pool Query**
Task ID: B-02-T02. Implementation Details: query recently-learned content via B-01 repository scoped by recency. Definition of Done: returns deterministic ordering for identical input state.
- **Status:** ✅ Completed & Verified (`_query_recent_content_questions` maps child practice recency to candidate questions).

**Task 03 — Implement Deterministic Assembly Algorithm**
Task ID: B-02-T03. Files to Create: `quiz_assembly_service.py`. Business Rules: Edge Cases 1/2/6. Tests: determinism test (signature test). Definition of Done: same input → same output, verified by repeated test runs.
- **Status:** ✅ Completed & Verified (`QuizAssemblyService.assemble()` achieves 100% reproducible selection with zero variance).

**Task 04 — Implement Media-Failure Backfill Method**
Task ID: B-02-T04. Implementation Details: `backfill_one()` per Edge Case 7. Definition of Done: backfill returns a valid replacement or gracefully reduces set size.
- **Status:** ✅ Completed & Verified (`backfill_one()` replaces failed questions deterministically or returns None on bank exhaustion).

**Task 05 — Add Redis Caching Layer**
Task ID: B-02-T05. Performance: p95 < 500ms target. Definition of Done: cache hit path verified in performance test.
- **Status:** ✅ Completed & Verified (in-progress attempt caching and 1-hour cross-context rolling exclusion window verified).

**Task 06 — Add Tests & Deterministic Fixture**
Task ID: B-02-T06. Files to Create: `test_quiz_assembly_service.py`, `deterministic_weak_skill_fixture.py`. Definition of Done: full coverage per §27.
- **Status:** ✅ Completed & Verified (22/22 unit & integration tests passing in 0.48s).

**Task 07 — Add Documentation**
Task ID: B-02-T07. Definition of Done: determinism/priority-ordering explainability documented per §28.
- **Status:** ✅ Completed & Verified (exhaustive docstrings and algorithms documented across service classes).

**Task 08 — Final Code Review**
Task ID: B-02-T08. Definition of Done: §31 checklist fully checked.
- **Status:** ✅ Completed & Verified (all 6 items verified).

## 30. Definition of Done
`assemble()` and `backfill_one()` merged, deterministic across repeated calls with identical input, fallback behavior verified for empty weak-skill pools, p95 latency target met in performance testing, ready for B-03 to consume.

## 31. Final Verification Checklist
- [x] Determinism verified: identical input state always produces identical assembled set
- [x] Empty weak-skill pool falls back to foundational mix without returning < target count
- [x] Deterministic priority ordering verified against fixed fixture when weak-skill candidates exceed slots
- [x] Exact-repeat avoidance within short time window verified across two contexts
- [x] p95 < 500ms verified under load
- [x] Skill Mastery Service unavailability degrades gracefully, does not block quiz access
